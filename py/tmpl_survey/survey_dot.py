"""Generate a Graphviz dot file showing the template call graph."""

from dataclasses import dataclass
import os
import shutil
import subprocess

from mb_cmn import provenance

_COLUMN_LETTERS = {"C", "D", "E"}
_DEEPLY_DISCARDED = {"מ:הערה"}
_BASE_DISCARDED = {"מ:כפול", "נוסח"}
_DOT_FALLBACK = os.path.join(
    os.environ.get("ProgramFiles", r"C:\Program Files"), "Graphviz", "bin", "dot.exe"
)


def _filter_deeply_discarded(stack_counts):
    """Remove entries where any deeply-discarded template appears in the chain."""
    return {
        key: count
        for key, count in stack_counts.items()
        if key[0] not in _DEEPLY_DISCARDED
        and not any(p in _DEEPLY_DISCARDED for p in key[1].split("/"))
    }


def _edges_from_stack_counts(stack_counts, discarded=None):
    """Extract (caller, callee) -> count from raw stack_counts defaultdict."""
    if discarded is None:
        discarded = _BASE_DISCARDED
    edges = {}
    for key, count in stack_counts.items():
        wtel_subtype, stack_str = key
        parts = [p for p in stack_str.split("/") if p not in discarded]
        caller = parts[-1]
        callee = wtel_subtype
        if callee in discarded:
            continue
        edge = (caller, callee)
        edges[edge] = edges.get(edge, 0) + count
    return edges


def _discarded_for_full_graph(discarded):
    """Base structural discards plus caller-provided full-graph discards."""
    if discarded is None:
        return set(_BASE_DISCARDED)
    return _BASE_DISCARDED | set(discarded)


def _discard_note_text(discarded):
    """Build graph-note text for discarded templates."""
    if not discarded:
        return None
    return ", ".join(sorted(discarded)) + " have been discarded"


def _collapse_equivalent_nodes(edges):
    """Collapse nodes with identical predecessor/successor sets.

    Two non-column nodes are equivalent when they have the same set of
    predecessors and the same set of successors (ignoring edge counts).
    Returns (new_edges, groups) where groups maps each representative node
    to the sorted list of original nodes it stands for.
    """
    predecessors = {}
    successors = {}
    all_nodes = set()
    for caller, callee in edges:
        all_nodes.add(caller)
        all_nodes.add(callee)
        successors.setdefault(caller, set()).add(callee)
        predecessors.setdefault(callee, set()).add(caller)
    for node in all_nodes:
        predecessors.setdefault(node, set())
        successors.setdefault(node, set())

    collapsible = all_nodes - _COLUMN_LETTERS

    sig_to_nodes = {}
    for node in collapsible:
        sig = (frozenset(predecessors[node]), frozenset(successors[node]))
        sig_to_nodes.setdefault(sig, []).append(node)

    node_to_rep = {}
    groups = {}
    for members in sig_to_nodes.values():
        sorted_members = sorted(members)
        rep = sorted_members[0]
        for m in sorted_members:
            node_to_rep[m] = rep
        groups[rep] = sorted_members

    for col in _COLUMN_LETTERS & all_nodes:
        node_to_rep[col] = col

    new_edges = {}
    for (caller, callee), count in edges.items():
        new_caller = node_to_rep[caller]
        new_callee = node_to_rep[callee]
        new_edge = (new_caller, new_callee)
        new_edges[new_edge] = new_edges.get(new_edge, 0) + count

    return new_edges, groups


def _abbreviate_name(name):
    """Abbreviate 'first middle ... last' to 'first … last' for 3+ word names."""
    words = name.split()
    if len(words) <= 2:
        return name
    return f"{words[0]} … {words[-1]}"


def _build_abbreviations(names):
    """Map each name to its abbreviated form, reverting to full where it would collide."""
    raw = {name: _abbreviate_name(name) for name in names}
    by_abbrev = {}
    for name, abbrev in raw.items():
        by_abbrev.setdefault(abbrev, []).append(name)
    for colliders in by_abbrev.values():
        if len(colliders) > 1:
            for name in colliders:
                raw[name] = name
    return raw


def _group_tooltip(members):
    """Return a tooltip listing all members of a collapsed group."""
    return "\n".join(members)


def _dot_quoted(name):
    """Quote a string for use as a dot identifier or label."""
    escaped = name.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _node_attrs(label=None, tooltip=None):
    """Return a dot attribute string for label and optional tooltip."""
    parts = []
    if label is not None:
        parts.append(f"label={_dot_quoted(label)}")
    if tooltip:
        parts.append(f"tooltip={_dot_quoted(tooltip)}")
    return " [" + ", ".join(parts) + "]"


def _focused_group_label(rep, members, target, abbrevs):
    """Return a label for a node in a focused graph."""
    if len(members) > 1 and rep != target:
        return f"direct children of {target}"
    return abbrevs[rep]


def _make_unique_node_id(preferred, used_ids):
    """Return a node id that is unique within the current dot file."""
    if preferred not in used_ids:
        used_ids.add(preferred)
        return preferred
    index = 2
    while True:
        candidate = f"{preferred} ({index})"
        if candidate not in used_ids:
            used_ids.add(candidate)
            return candidate
        index += 1


_DEFAULT_NOTE = object()


def _write_dot(
    edges,
    groups,
    fp,
    note=_DEFAULT_NOTE,
    focus_target=None,
    generated_by=None,
):
    # Build abbreviation map for all non-column nodes
    all_names = set()
    for caller, callee in edges:
        all_names.add(caller)
        all_names.add(callee)
    col_nodes = _COLUMN_LETTERS & all_names
    all_names -= _COLUMN_LETTERS
    abbrevs = _build_abbreviations(all_names)

    if generated_by:
        fp.write(f"// {generated_by}\n")
        fp.write("// Do not edit by hand.\n")
    fp.write("digraph template_call_graph {\n")
    fp.write("    rankdir=LR;\n")
    fp.write('    node [fontname="SBL Hebrew,Helvetica", fontsize=12];\n')
    fp.write('    edge [fontname="Helvetica", fontsize=9];\n')
    if generated_by:
        fp.write(f"    graph [comment={_dot_quoted(generated_by)}];\n")
    fp.write("\n")
    # Column nodes styled distinctly
    if col_nodes:
        fp.write("    // Column nodes\n")
        fp.write("    node [shape=box, style=bold];\n")
        for col in sorted(col_nodes):
            fp.write(f"    {_dot_quoted(col)};\n")
        fp.write("\n")
    # Template nodes (with labels/tooltips as needed)
    fp.write("    // Template nodes\n")
    fp.write('    node [shape=box, style=""];\n')
    node_ids = {}
    used_ids = set(col_nodes)
    for rep, members in sorted(groups.items()):
        label = None
        tooltip = None
        node_id = rep
        if len(members) > 1:
            tooltip = _group_tooltip(members)
            if focus_target is None:
                label = f"{abbrevs[rep]}, …"
                node_id = _make_unique_node_id(label, used_ids)
            else:
                label = _focused_group_label(rep, members, focus_target, abbrevs)
                if rep != focus_target:
                    node_id = _make_unique_node_id(label, used_ids)
        elif abbrevs[rep] != rep:
            label = abbrevs[rep]
            tooltip = rep
        else:
            used_ids.add(node_id)
        node_ids[rep] = node_id
        if label is not None:
            emitted_label = None if label == node_id else label
            fp.write(
                f"    {_dot_quoted(node_id)}{_node_attrs(emitted_label, tooltip)};\n"
            )
    fp.write("\n")
    # Note
    if note is _DEFAULT_NOTE:
        note_text = _discard_note_text(_BASE_DISCARDED)
    else:
        note_text = note
    if note_text:
        fp.write("    // Note\n")
        fp.write(f'    graph [label="{note_text}", labelloc=b, fontsize=10];\n')
        fp.write("\n")
    # Edges sorted for stable output
    fp.write("    // Edges\n")
    for (caller, callee), count in sorted(edges.items()):
        caller_id = node_ids.get(caller, caller)
        callee_id = node_ids.get(callee, callee)
        fp.write(
            f"    {_dot_quoted(caller_id)} -> {_dot_quoted(callee_id)}"
            f' [label="{count}"];\n'
        )
    fp.write("}\n")


def _focused_edges(all_edges, target):
    """Keep only edges on call chains involving target, plus one level past it."""
    predecessors = {}
    successors = {}
    for caller, callee in all_edges:
        predecessors.setdefault(callee, set()).add(caller)
        predecessors.setdefault(caller, set())
        successors.setdefault(caller, set()).add(callee)
        successors.setdefault(callee, set())
    # Find all nodes that can reach target (reverse BFS)
    before = {target}
    frontier = [target]
    while frontier:
        node = frontier.pop()
        for pred in predecessors.get(node, ()):
            if pred not in before:
                before.add(pred)
                frontier.append(pred)
    return {
        edge: count
        for edge, count in all_edges.items()
        if (edge[0] in before and edge[1] in before) or edge[0] == target
    }


def _split_stack_str(stack_str):
    """Return stack elements from a slash-delimited stack string."""
    return tuple(stack_str.split("/"))


def _focused_stack_keys(stack_counts, target):
    """Return raw stack-count keys that belong to a focused target scope.

    Scope has two parts:
    1. Ancestor branch edges that actually lead to a target occurrence.
    2. Descendant edges where the target appears in the stack path.
    """
    target_stacks = [
        _split_stack_str(stack_str)
        for (wtel_subtype, stack_str), _count in stack_counts.items()
        if wtel_subtype == target
    ]

    focused_keys = set()

    for stack_parts in target_stacks:
        focused_keys.add((target, "/".join(stack_parts)))
        for i in range(1, len(stack_parts)):
            callee = stack_parts[i]
            caller_stack = "/".join(stack_parts[:i])
            focused_keys.add((callee, caller_stack))

    for (wtel_subtype, stack_str), _count in stack_counts.items():
        if target in _split_stack_str(stack_str):
            focused_keys.add((wtel_subtype, stack_str))

    return focused_keys


def _focused_stack_counts(stack_counts, target):
    """Filter stack_counts down to focused keys for a target template."""
    focused_keys = _focused_stack_keys(stack_counts, target)
    return {key: count for key, count in stack_counts.items() if key in focused_keys}


@dataclass(frozen=True)
class _FocusedTarget:
    tmpl_name: str
    slug: str
    collapse: bool


# First-pass focused targets for template-specific subset documentation.
# Keep this list intentionally small for now; exhaustive generation is deferred.
_FOCUSED_TARGETS = (
    _FocusedTarget("מ:כפול", "kaful", False),
    _FocusedTarget("נוסח", "nusach", True),
    _FocusedTarget("מ:פסוק", "pasuk", False),
    _FocusedTarget("כו״ק", "kuk", False),
    _FocusedTarget("מ:דחי", "dchi", False),
)


def _generated_by_text(generator_file):
    if generator_file is None:
        return None
    return provenance.generated_by_text(generator_file)


def write_dot_file(
    stack_counts,
    out_path,
    deeply_discard=False,
    discarded=None,
    generator_file=None,
):
    """Write a .dot call graph from raw stack_counts accumulator."""
    generated_by = _generated_by_text(generator_file)
    if deeply_discard:
        stack_counts = _filter_deeply_discarded(stack_counts)
    full_discarded = _discarded_for_full_graph(discarded)
    edges = _edges_from_stack_counts(stack_counts, discarded=full_discarded)
    edges, groups = _collapse_equivalent_nodes(edges)
    note = _discard_note_text(full_discarded)
    with open(out_path, "w", encoding="utf-8") as fp:
        _write_dot(edges, groups, fp, note=note, generated_by=generated_by)


def _identity_groups(edges):
    """Return trivial groups (each node maps to itself) — no collapsing."""
    all_nodes = set()
    for caller, callee in edges:
        all_nodes.add(caller)
        all_nodes.add(callee)
    return {node: [node] for node in all_nodes - _COLUMN_LETTERS}


def write_focused_dot_files(
    stack_counts,
    stem,
    deeply_discard=False,
    svg_stem=None,
    generator_file=None,
):
    """Write per-target focused .dot/.svg call graphs.

    If svg_stem is given, SVG files are written relative to that stem
    instead of the dot stem.
    """
    generated_by = _generated_by_text(generator_file)
    if deeply_discard:
        stack_counts = _filter_deeply_discarded(stack_counts)
    if svg_stem is None:
        svg_stem = stem
    for spec in _FOCUSED_TARGETS:
        target = spec.tmpl_name
        slug = spec.slug
        collapse = spec.collapse
        focused_stack_counts = _focused_stack_counts(stack_counts, target)
        edges = _edges_from_stack_counts(focused_stack_counts, discarded=set())
        edges = _focused_edges(edges, target)
        if collapse:
            edges, groups = _collapse_equivalent_nodes(edges)
        else:
            groups = _identity_groups(edges)
        dot_path = f"{stem}-{slug}-call-graph.dot"
        svg_path = f"{svg_stem}-{slug}-call-graph.svg"
        with open(dot_path, "w", encoding="utf-8") as fp:
            _write_dot(
                edges,
                groups,
                fp,
                note=None,
                focus_target=target,
                generated_by=generated_by,
            )
        render_svg(dot_path, svg_path, generator_file=generator_file)


def _find_dot():
    """Return the path to the dot executable, or None."""
    found = shutil.which("dot")
    if found:
        return found
    if shutil.which(_DOT_FALLBACK):
        return _DOT_FALLBACK
    return None


def _with_svg_comment_inserted(svg_text, comment_text):
    marker = f"<!-- {comment_text} -->"
    if marker in svg_text:
        return svg_text
    svg_tag_index = svg_text.find("<svg ")
    if svg_tag_index == -1:
        raise ValueError("Could not locate <svg ...> tag for provenance insertion")
    return svg_text[:svg_tag_index] + marker + "\n" + svg_text[svg_tag_index:]


def _ensure_svg_comment(svg_path, comment_text):
    marker = f"<!-- {comment_text} -->"
    graphviz_escaped_marker = f"<!-- {comment_text.replace('-', '&#45;')} -->"
    with open(svg_path, "r", encoding="utf-8") as svg_fp:
        svg_text = svg_fp.read()
    if marker in svg_text or graphviz_escaped_marker in svg_text:
        return
    updated_svg_text = _with_svg_comment_inserted(svg_text, comment_text)
    with open(svg_path, "w", encoding="utf-8") as svg_fp:
        svg_fp.write(updated_svg_text)


def render_svg(dot_path, svg_path, generator_file=None):
    """Render a .dot file to SVG. Returns True on success, False if dot is unavailable."""
    dot = _find_dot()
    if dot is None:
        return False
    subprocess.run(
        [dot, "-Tsvg", "-o", svg_path, dot_path],
        check=True,
        encoding="utf-8",
        capture_output=True,
    )
    generated_by = _generated_by_text(generator_file)
    if generated_by is not None:
        _ensure_svg_comment(svg_path, generated_by)
    return True
