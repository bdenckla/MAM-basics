"""Generate a Graphviz dot file showing the template call graph."""

from dataclasses import dataclass
import os
import shutil
import subprocess

from mb_cmn import provenance
from mb_cmn import uni_heb as uh
from tmpl_survey import svg_provenance_norm

_COLUMN_LETTERS = {"C", "D", "E"}
_BASE_DISCARDED = {"מ:כפול", "נוסח"}
_FOCUSED_NO_DISCARD_TARGETS = {"מ:פסוק"}
_NUSACH_FOCUSED_DISCARDED = {
    "כו״ק",
    "מ:קו״כ-אם-2",
    "מ:כו״ק מיוחד",
    "מ:קמץ",
    "מ:דחי",
}
_DOT_FALLBACK = os.path.join(
    os.environ.get("ProgramFiles", r"C:\Program Files"), "Graphviz", "bin", "dot.exe"
)
_FOCUS_NODE_ATTR_PARTS = (
    'fillcolor="lightgoldenrod1"',
    'style="filled"',
    "penwidth=2.5",
)
_EDGE_LABEL_MAX_CHARS = 72
_ONE_HOP_LABEL_MAX_PARTS = 2
_BASE_TEMPLATE_ALIASES = {
    "נוסח@1": "נוסח",
    "נוסח@2": "נוסח",
}


def _base_template_name(name):
    return _BASE_TEMPLATE_ALIASES.get(name, name)


def _matches_target(name, target):
    return _base_template_name(name) == target


def _is_discarded(name, discarded):
    return _base_template_name(name) in discarded


def _edges_from_stack_counts(stack_counts, discarded=None):
    """Extract (caller, callee) -> count from raw stack_counts defaultdict."""
    if discarded is None:
        discarded = _BASE_DISCARDED
    edges = {}
    for key, count in stack_counts.items():
        stack_top, stack_rest = key
        rest_parts = [
            p for p in stack_rest.split("/") if not _is_discarded(p, discarded)
        ]
        caller = rest_parts[-1]
        callee = stack_top
        if _is_discarded(callee, discarded):
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


def _build_adjacency_sets(edges):
    """Return predecessor/successor sets keyed by node."""
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
    return predecessors, successors


def _group_tooltip(members):
    """Return a tooltip listing all members of a collapsed group."""
    return "\n".join(members)


def _dot_quoted(name):
    """Quote a string for use as a dot identifier or label."""
    escaped = name.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _node_attrs(label=None, tooltip=None, extra_parts=None):
    """Return a dot attribute string for label, tooltip, and extra attrs."""
    parts = []
    if label is not None:
        parts.append(f"label={_dot_quoted(label)}")
    if tooltip:
        parts.append(f"tooltip={_dot_quoted(tooltip)}")
    if extra_parts:
        parts.extend(extra_parts)
    return " [" + ", ".join(parts) + "]"


def _focused_group_label(rep, members, target, abbrevs, predecessors, successors):
    """Return a label for a node in a focused graph."""
    if len(members) > 1 and not _matches_target(rep, target):
        predecessor_bases = {
            _base_template_name(x) for x in predecessors.get(rep, set())
        }
        if predecessor_bases == {target} and not successors.get(rep, set()):
            return f"dead-end children of {target}"
        return f"{abbrevs[rep]}, ..."
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
    predecessors, successors = _build_adjacency_sets(edges)
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
        node_attr_parts = None
        if focus_target is not None and any(
            _matches_target(x, focus_target) for x in members
        ):
            node_attr_parts = _FOCUS_NODE_ATTR_PARTS
        if len(members) > 1:
            tooltip = _group_tooltip(members)
            if focus_target is None:
                label = f"{abbrevs[rep]}, …"
                node_id = _make_unique_node_id(label, used_ids)
            else:
                label = _focused_group_label(
                    rep,
                    members,
                    focus_target,
                    abbrevs,
                    predecessors,
                    successors,
                )
                if not _matches_target(rep, focus_target):
                    node_id = _make_unique_node_id(label, used_ids)
        elif abbrevs[rep] != rep:
            label = abbrevs[rep]
            tooltip = rep
        else:
            used_ids.add(node_id)
        node_ids[rep] = node_id
        if label is not None or node_attr_parts is not None:
            emitted_label = None if label == node_id else label
            fp.write(
                f"    {_dot_quoted(node_id)}"
                f"{_node_attrs(emitted_label, tooltip, extra_parts=node_attr_parts)};\n"
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


def _split_stack_rest(stack_rest):
    """Return stack-rest elements from a slash-delimited stack-rest string."""
    return tuple(stack_rest.split("/"))


def _focused_edges_from_stack_counts(stack_counts, target, discarded=None):
    """Build focused edges from only stacks that involve the target.

    For each raw stack-count record where target appears anywhere in the stack
    (stack_rest parts + stack_top), decompose that stack into
    adjacent caller->callee edges and accumulate the record count.

    If discarded is provided, discarded templates are removed from the path
    before edge decomposition, and records whose callee is discarded are
    ignored.
    """
    if discarded is None:
        discarded = set()
    focused_edges = {}
    for (stack_top, stack_rest), count in stack_counts.items():
        rest_parts = [
            p for p in _split_stack_rest(stack_rest) if not _is_discarded(p, discarded)
        ]
        if _is_discarded(stack_top, discarded):
            continue
        stack = (*rest_parts, stack_top)
        if not any(_matches_target(x, target) for x in stack):
            continue
        for caller, callee in zip(stack, stack[1:]):
            edge = (caller, callee)
            focused_edges[edge] = focused_edges.get(edge, 0) + count
    return focused_edges


@dataclass(frozen=True)
class _FocusedTarget:
    tmpl_name: str
    slug: str
    collapse: bool


# First-pass focused targets for template-specific subset documentation.
# Keep this list intentionally small for now; exhaustive generation is deferred.
_FOCUSED_TARGETS = (
    _FocusedTarget("מ:כפול", uh.he_ascii_slug("כפול"), False),
    _FocusedTarget("נוסח", uh.he_ascii_slug("נוסח"), True),
    _FocusedTarget("מ:פסוק", "pasuk", False),
    _FocusedTarget("כו״ק", uh.he_ascii_slug("כו״ק"), False),
    _FocusedTarget("מ:דחי", "dchi", False),
)


def _generated_by_text(generator_file):
    if generator_file is None:
        return None
    return provenance.generated_by_text(generator_file)


def write_dot_file(
    stack_counts,
    out_path,
    discarded=None,
    generator_file=None,
):
    """Write a .dot call graph from raw stack_counts accumulator."""
    generated_by = _generated_by_text(generator_file)
    full_discarded = _discarded_for_full_graph(discarded)
    edges = _edges_from_stack_counts(stack_counts, discarded=full_discarded)
    edges, groups = _collapse_equivalent_nodes(edges)
    note = _discard_note_text(full_discarded)
    with open(out_path, "w", encoding="utf-8") as fp:
        _write_dot(edges, groups, fp, note=note, generated_by=generated_by)


def _edge_template_stacks_from_stack_counts(stack_counts, discarded=None):
    """Extract start/template-stack records used by edge-labeled stack graphs."""
    if discarded is None:
        discarded = set()
    stacks = []
    for (stack_top, stack_rest), count in stack_counts.items():
        if _is_discarded(stack_top, discarded):
            continue
        rest_parts = [
            p for p in _split_stack_rest(stack_rest) if not _is_discarded(p, discarded)
        ]
        if not rest_parts:
            continue
        start = rest_parts[0]
        template_stack = tuple((*rest_parts[1:], stack_top))
        if not template_stack:
            continue
        stacks.append((start, template_stack, count))
    return stacks


def _edge_mode_state_id(start, template_prefix):
    """Return synthetic node id for a partial stack state."""
    return f"{start}::stack::{'/'.join(template_prefix)}"


def _edge_mode_start_id(start, first_hop):
    """Return synthetic node id for a stack start per first hop."""
    return f"{start}::start::{first_hop}"


def _edge_mode_one_hop_start_id(start):
    """Return synthetic node id for the shared one-hop start node."""
    return f"{start}::start"


def _edge_mode_end_id(start, first_hop):
    """Return synthetic node id for a stack-end sink per first hop."""
    return f"{start}::stack-end::{first_hop}"


def _edge_mode_one_hop_end_id(start):
    """Return synthetic node id for the shared one-hop stack-end sink."""
    return f"{start}::stack-end"


def _is_start_to_end_one_hop_edge(edge, starts):
    """Return True when an edge goes directly from a start-node to one-hop sink."""
    src, dst, _tmpl_name = edge
    return src in starts and dst.endswith("::stack-end")


def _format_collapsed_one_hop_label(template_counts):
    """Return a stable full label for collapsed one-hop templates on one edge."""
    parts = [
        f"{tmpl_name} ({count})" for tmpl_name, count in sorted(template_counts.items())
    ]
    return " | ".join(parts)


def _format_collapsed_one_hop_short_label(template_counts, tmpl_abbrevs):
    """Return a stable shortened label for collapsed one-hop templates on one edge."""
    parts = [
        f"{tmpl_abbrevs[tmpl_name]} ({count})"
        for tmpl_name, count in sorted(template_counts.items())
    ]
    return " | ".join(parts)


def _truncate_edge_label(display_label, full_label):
    """Clamp very long edge labels while preserving full text in tooltip."""
    if len(display_label) <= _EDGE_LABEL_MAX_CHARS:
        return display_label
    return display_label[: _EDGE_LABEL_MAX_CHARS - 1] + "…"


def _compact_one_hop_short_label(short_label):
    """Compact long one-hop merged labels to avoid excessively wide diagrams."""
    parts = short_label.split(" | ")
    if (
        len(parts) <= _ONE_HOP_LABEL_MAX_PARTS
        and len(short_label) <= _EDGE_LABEL_MAX_CHARS
    ):
        return short_label
    if len(parts) <= 1:
        return _truncate_edge_label(short_label, short_label)

    max_kept = min(_ONE_HOP_LABEL_MAX_PARTS, len(parts) - 1)
    for keep_count in range(max_kept, 0, -1):
        remaining = len(parts) - keep_count
        candidate = " | ".join([*parts[:keep_count], f"… +{remaining} more"])
        if len(candidate) <= _EDGE_LABEL_MAX_CHARS or keep_count == 1:
            return candidate
    return "…"


def _single_template_edge_label_and_tooltip(tmpl_name, count, tmpl_abbrevs):
    """Return (label, tooltip) for a single-template edge label."""
    full_label = f"{tmpl_name} ({count})"
    short_name = tmpl_abbrevs[tmpl_name]
    short_label = f"{short_name} ({count})"
    display_label = _truncate_edge_label(short_label, full_label)
    if display_label == full_label:
        return display_label, None
    return display_label, full_label


def _write_edge_templates_dot(stacks, fp, note=_DEFAULT_NOTE, generated_by=None):
    """Write edge-labeled DOT where templates are on edges, not nodes."""
    has_child_contexts = set()
    for start, template_stack, _count in stacks:
        for prefix_len in range(1, len(template_stack)):
            has_child_contexts.add((start, template_stack[:prefix_len]))

    start_node_meta = {}
    state_tooltips = {}
    end_tooltips = {}
    edge_counts = {}
    for start, template_stack, count in stacks:
        first_hop = template_stack[0]
        is_one_hop_leaf = (start, (first_hop,)) not in has_child_contexts
        if len(template_stack) == 1 and is_one_hop_leaf:
            start_node = _edge_mode_one_hop_start_id(start)
            start_node_meta.setdefault(
                start_node,
                (start, f"Stack start for {start} (one-hop aggregate)"),
            )
        else:
            start_node = _edge_mode_start_id(start, first_hop)
            start_node_meta.setdefault(
                start_node,
                (start, f"Stack start for {start}/{first_hop}"),
            )
        prev_node = start_node
        for idx, tmpl_name in enumerate(template_stack):
            context_prefix = template_stack[: idx + 1]
            is_last_in_path = idx == len(template_stack) - 1
            if (start, context_prefix) in has_child_contexts:
                if is_last_in_path:
                    # Leaf-only terminal policy: skip rows that stop at non-leaf contexts.
                    continue
                next_node = _edge_mode_state_id(start, context_prefix)
                state_tooltips.setdefault(
                    next_node, f"{start}/{'/'.join(context_prefix)}"
                )
            else:
                if len(context_prefix) == 1:
                    next_node = _edge_mode_one_hop_end_id(start)
                    end_tooltips.setdefault(
                        next_node,
                        f"Stack end for {start}",
                    )
                else:
                    next_node = _edge_mode_end_id(start, first_hop)
                    end_tooltips.setdefault(
                        next_node,
                        f"Stack end for {start}/{first_hop}",
                    )
            edge = (prev_node, next_node, tmpl_name)
            edge_counts[edge] = edge_counts.get(edge, 0) + count
            prev_node = next_node

    if generated_by:
        fp.write(f"// {generated_by}\n")
        fp.write("// Do not edit by hand.\n")
    fp.write("digraph template_call_graph_templates_as_edges {\n")
    fp.write("    rankdir=LR;\n")
    fp.write('    node [fontname="SBL Hebrew,Helvetica", fontsize=12];\n')
    fp.write('    edge [fontname="SBL Hebrew,Helvetica", fontsize=9];\n')
    if generated_by:
        fp.write(f"    graph [comment={_dot_quoted(generated_by)}];\n")
    fp.write("\n")

    if start_node_meta:
        fp.write("    // Stack start nodes\n")
        fp.write("    node [shape=box, style=bold];\n")
        for start_node in sorted(start_node_meta):
            start_label, start_tooltip = start_node_meta[start_node]
            fp.write(
                f"    {_dot_quoted(start_node)}"
                f"{_node_attrs(label=start_label, tooltip=start_tooltip)};\n"
            )
        fp.write("\n")

    if state_tooltips:
        fp.write("    // Internal stack-state nodes\n")
        fp.write(
            '    node [shape=circle, style="", width=0.18, height=0.18, fixedsize=true];\n'
        )
        for node_id in sorted(state_tooltips):
            fp.write(
                f"    {_dot_quoted(node_id)}"
                f"{_node_attrs(label='', tooltip=state_tooltips[node_id])};\n"
            )
        fp.write("\n")

    if end_tooltips:
        fp.write("    // Stack-end nodes\n")
        fp.write(
            '    node [shape=doublecircle, style="", width=0.35, height=0.35, fixedsize=true];\n'
        )
        for end_id in sorted(end_tooltips):
            fp.write(
                f"    {_dot_quoted(end_id)}"
                f"{_node_attrs(label='end', tooltip=end_tooltips[end_id])};\n"
            )
        fp.write("\n")

    if note is _DEFAULT_NOTE:
        note_text = _discard_note_text(_BASE_DISCARDED)
    else:
        note_text = note
    if note_text:
        fp.write("    // Note\n")
        fp.write(f'    graph [label="{note_text}", labelloc=b, fontsize=10];\n')
        fp.write("\n")

    fp.write("    // Edge-labeled templates\n")
    one_hop_counts = {}
    remaining_edges = {}
    start_node_ids = set(start_node_meta)
    for edge, count in edge_counts.items():
        if _is_start_to_end_one_hop_edge(edge, start_node_ids):
            src, dst, tmpl_name = edge
            agg = one_hop_counts.setdefault((src, dst), {})
            agg[tmpl_name] = agg.get(tmpl_name, 0) + count
        else:
            remaining_edges[edge] = count

    edge_template_names = {tmpl_name for (_src, _dst, tmpl_name) in edge_counts}
    tmpl_abbrevs = _build_abbreviations(edge_template_names)

    for (src, dst, tmpl_name), count in sorted(remaining_edges.items()):
        edge_label, edge_tooltip = _single_template_edge_label_and_tooltip(
            tmpl_name,
            count,
            tmpl_abbrevs,
        )
        edge_attr = f"label={_dot_quoted(edge_label)}"
        if edge_tooltip:
            edge_attr += f", tooltip={_dot_quoted(edge_tooltip)}"
        fp.write(f"    {_dot_quoted(src)} -> {_dot_quoted(dst)}" f" [{edge_attr}];\n")

    for (src, dst), template_counts in sorted(one_hop_counts.items()):
        edge_full_label = _format_collapsed_one_hop_label(template_counts)
        edge_label = _format_collapsed_one_hop_short_label(
            template_counts, tmpl_abbrevs
        )
        edge_label = _compact_one_hop_short_label(edge_label)
        edge_label = _truncate_edge_label(edge_label, edge_full_label)
        edge_attr = f"label={_dot_quoted(edge_label)}"
        if edge_label != edge_full_label:
            edge_attr += f", tooltip={_dot_quoted(edge_full_label)}"
        fp.write(f"    {_dot_quoted(src)} -> {_dot_quoted(dst)}" f" [{edge_attr}];\n")
    fp.write("}\n")


def write_edge_template_dot_file(
    stack_counts,
    out_path,
    discarded=None,
    generator_file=None,
):
    """Write a .dot graph where templates are labels on edges, not nodes."""
    generated_by = _generated_by_text(generator_file)
    full_discarded = _discarded_for_full_graph(discarded)
    stacks = _edge_template_stacks_from_stack_counts(
        stack_counts,
        discarded=full_discarded,
    )
    note = _discard_note_text(full_discarded)
    with open(out_path, "w", encoding="utf-8") as fp:
        _write_edge_templates_dot(stacks, fp, note=note, generated_by=generated_by)


def _identity_groups(edges):
    """Return trivial groups (each node maps to itself) — no collapsing."""
    all_nodes = set()
    for caller, callee in edges:
        all_nodes.add(caller)
        all_nodes.add(callee)
    return {node: [node] for node in all_nodes - _COLUMN_LETTERS}


def _focused_discarded_for_target(target, full_discarded):
    """Return discard set used for a specific focused target."""
    if target == "נוסח":
        return set(_NUSACH_FOCUSED_DISCARDED)
    if target in full_discarded or target in _FOCUSED_NO_DISCARD_TARGETS:
        return set()
    return full_discarded


def write_focused_dot_files(
    stack_counts,
    stem,
    svg_stem=None,
    generator_file=None,
    discarded=None,
):
    """Write per-target focused .dot/.svg call graphs.

    If svg_stem is given, SVG files are written relative to that stem
    instead of the dot stem.
    """
    generated_by = _generated_by_text(generator_file)
    full_discarded = _discarded_for_full_graph(discarded)
    if svg_stem is None:
        svg_stem = stem
    for spec in _FOCUSED_TARGETS:
        target = spec.tmpl_name
        slug = spec.slug
        collapse = spec.collapse
        focused_discarded = _focused_discarded_for_target(target, full_discarded)
        edges = _focused_edges_from_stack_counts(
            stack_counts,
            target,
            discarded=focused_discarded,
        )
        note = _discard_note_text(focused_discarded)
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
                note=note,
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
        with open(svg_path, "r", encoding="utf-8") as svg_fp:
            svg_text = svg_fp.read()
        normalized_svg_text = svg_provenance_norm.normalize_generated_by_comment_hyphen(
            svg_text,
            generated_by,
        )
        if normalized_svg_text != svg_text:
            with open(svg_path, "w", encoding="utf-8") as svg_fp:
                svg_fp.write(normalized_svg_text)
    return True
