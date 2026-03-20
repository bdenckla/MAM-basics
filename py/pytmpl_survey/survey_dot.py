"""Generate a Graphviz dot file showing the template call graph."""

import os
import shutil
import subprocess

_COLUMN_LETTERS = {"C", "D", "E"}
_DEEPLY_DISCARDED = {"מ:הערה"}
_DISCARDED = {"מ:כפול", "נוסח", "ש"}
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
        discarded = _DISCARDED
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


def _node_attrs(label, tooltip):
    """Return a dot attribute string for label and optional tooltip."""
    parts = [f"label={_dot_quoted(label)}"]
    if tooltip:
        parts.append(f"tooltip={_dot_quoted(tooltip)}")
    return " [" + ", ".join(parts) + "]"


_DEFAULT_NOTE = object()


def _write_dot(edges, groups, fp, note=_DEFAULT_NOTE):
    # Build abbreviation map for all non-column nodes
    all_names = set()
    for caller, callee in edges:
        all_names.add(caller)
        all_names.add(callee)
    col_nodes = _COLUMN_LETTERS & all_names
    all_names -= _COLUMN_LETTERS
    abbrevs = _build_abbreviations(all_names)

    fp.write("digraph template_call_graph {\n")
    fp.write("    rankdir=LR;\n")
    fp.write('    node [fontname="SBL Hebrew,Helvetica", fontsize=12];\n')
    fp.write('    edge [fontname="Helvetica", fontsize=9];\n')
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
    for rep, members in sorted(groups.items()):
        if len(members) > 1:
            label = f"{abbrevs[rep]}, …"
            tooltip = _group_tooltip(members)
            fp.write(f"    {_dot_quoted(rep)}{_node_attrs(label, tooltip)};\n")
        elif abbrevs[rep] != rep:
            fp.write(f"    {_dot_quoted(rep)}{_node_attrs(abbrevs[rep], rep)};\n")
    fp.write("\n")
    # Note
    if note is _DEFAULT_NOTE:
        note_text = ", ".join(sorted(_DISCARDED)) + " have been discarded"
    else:
        note_text = note
    if note_text:
        fp.write("    // Note\n")
        fp.write(f'    graph [label="{note_text}", labelloc=b, fontsize=10];\n')
        fp.write("\n")
    # Edges sorted for stable output
    fp.write("    // Edges\n")
    for (caller, callee), count in sorted(edges.items()):
        fp.write(
            f"    {_dot_quoted(caller)} -> {_dot_quoted(callee)}"
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


_FOCUSED_TARGETS = [
    ("מ:כפול", "kaful", False),
    ("נוסח", "nusach", True),
]


def write_dot_file(stack_counts, out_path, deeply_discard=False):
    """Write a .dot call graph from raw stack_counts accumulator."""
    if deeply_discard:
        stack_counts = _filter_deeply_discarded(stack_counts)
    edges = _edges_from_stack_counts(stack_counts)
    edges, groups = _collapse_equivalent_nodes(edges)
    with open(out_path, "w", encoding="utf-8") as fp:
        _write_dot(edges, groups, fp)


def _identity_groups(edges):
    """Return trivial groups (each node maps to itself) — no collapsing."""
    all_nodes = set()
    for caller, callee in edges:
        all_nodes.add(caller)
        all_nodes.add(callee)
    return {node: [node] for node in all_nodes - _COLUMN_LETTERS}


def write_focused_dot_files(stack_counts, stem, deeply_discard=False, svg_stem=None):
    """Write per-target focused .dot/.svg call graphs.

    If svg_stem is given, SVG files are written relative to that stem
    instead of the dot stem.
    """
    if deeply_discard:
        stack_counts = _filter_deeply_discarded(stack_counts)
    if svg_stem is None:
        svg_stem = stem
    for target, slug, collapse in _FOCUSED_TARGETS:
        edges = _edges_from_stack_counts(stack_counts, discarded=set())
        edges = _focused_edges(edges, target)
        if collapse:
            edges, groups = _collapse_equivalent_nodes(edges)
        else:
            groups = _identity_groups(edges)
        dot_path = f"{stem}-{slug}-call-graph.dot"
        svg_path = f"{svg_stem}-{slug}-call-graph.svg"
        with open(dot_path, "w", encoding="utf-8") as fp:
            _write_dot(edges, groups, fp, note=None)
        render_svg(dot_path, svg_path)


def _find_dot():
    """Return the path to the dot executable, or None."""
    found = shutil.which("dot")
    if found:
        return found
    if shutil.which(_DOT_FALLBACK):
        return _DOT_FALLBACK
    return None


def render_svg(dot_path, svg_path):
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
    return True
