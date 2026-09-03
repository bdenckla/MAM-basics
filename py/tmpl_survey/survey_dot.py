"""Generate a Graphviz dot file showing the template call graph."""

from dataclasses import dataclass
import os
import shutil
import subprocess

from mb_cmn import provenance
from mb_cmn import uni_heb as uh
from tmpl_survey import dot_node_collapse
from tmpl_survey import svg_provenance_norm

_COLUMN_LETTERS = {"C", "D", "E"}
_BASE_DISCARDED = {"מ:כפול", "נוסח"}
_DOT_FALLBACK = os.path.join(
    os.environ.get("ProgramFiles", r"C:/Program Files"), "Graphviz", "bin", "dot.exe"
)
_FOCUS_NODE_ATTR_PARTS = (
    'fillcolor="lightgoldenrod1"',
    'style="filled"',
    "penwidth=2.5",
)
_MIN_STACK_LEN_FOR_NODE_MODE = 3
_MIN_TEMPLATE_STACK_LEN_FOR_NODE_MODE = _MIN_STACK_LEN_FOR_NODE_MODE - 1
_COLUMN_ORDER = ("C", "D", "E")


def _base_template_name(name):
    return name


def _matches_target(name, target):
    return _base_template_name(name) == target


def _is_discarded(name, discarded):
    return _base_template_name(name) in discarded


def _edges_from_stack_counts(stack_counts, discarded=None):
    """Extract node-mode edges aggregated across column-specific variants.

    Column letters are used to partition graph variants but are not rendered
    as graph nodes.
    """
    edges = {}
    for edges_for_column in _edges_by_column_from_stack_counts(
        stack_counts, discarded=discarded
    ).values():
        for edge, count in edges_for_column.items():
            edges[edge] = edges.get(edge, 0) + count
    return edges


def _template_stacks_by_column(stack_counts, discarded=None):
    """Return {column_letter: [(template_stack, count), ...]} from raw records."""
    if discarded is None:
        discarded = _BASE_DISCARDED
    by_column = {}
    for key, count in stack_counts.items():
        stack_top, stack_rest = key
        rest_parts = [
            p for p in stack_rest.split("/") if not _is_discarded(p, discarded)
        ]
        if _is_discarded(stack_top, discarded):
            continue
        stack = (*rest_parts, stack_top)
        if not stack:
            continue
        column = stack[0]
        if column not in _COLUMN_LETTERS:
            continue
        template_stack = stack[1:]
        by_column.setdefault(column, []).append((template_stack, count))
    return by_column


def _edges_by_column_from_stack_counts(stack_counts, discarded=None):
    """Return node-mode edges grouped by source column version."""
    by_column = _template_stacks_by_column(stack_counts, discarded=discarded)
    edges_by_column = {}
    for column, records in by_column.items():
        edges = {}
        for template_stack, count in records:
            if len(template_stack) < _MIN_TEMPLATE_STACK_LEN_FOR_NODE_MODE:
                continue
            for caller, callee in zip(template_stack, template_stack[1:]):
                edge = (caller, callee)
                edges[edge] = edges.get(edge, 0) + count
        edges_by_column[column] = edges
    return edges_by_column


def _column_sort_key(column):
    try:
        return (_COLUMN_ORDER.index(column), column)
    except ValueError:
        return (len(_COLUMN_ORDER), column)


def _sorted_columns(columns):
    return sorted(columns, key=_column_sort_key)


def _with_column_suffix(path, column, needs_disambiguation):
    if not needs_disambiguation:
        return path
    root, ext = os.path.splitext(path)
    return f"{root}-{column.lower()}{ext}"


def _column_versions_for_output(edges_by_column):
    columns = _sorted_columns(edges_by_column.keys())
    if columns:
        return columns
    # Preserve prior behavior for empty inputs by emitting one unsuffixed graph.
    return [None]


def _maybe_remove_legacy_unsuffixed(path, needs_disambiguation):
    if needs_disambiguation and os.path.exists(path):
        os.remove(path)


def _discarded_for_full_graph(discarded):
    """Base structural discards plus caller-provided full-graph discards."""
    if discarded is None:
        return set(_BASE_DISCARDED)
    return _BASE_DISCARDED | set(discarded)


def _discarded_for_full_graph_column(full_discarded, column):
    """Return discard set for one full-graph column version.

    Keep C/D unfiltered so their graphs preserve all template nodes/edges.
    Keep legacy filtering for E to preserve readability in the large graph.
    """
    if column in {"C", "D"}:
        return set()
    return set(full_discarded)


def _discard_note_text(discarded):
    """Build graph-note text for discarded templates."""
    if not discarded:
        return None
    return ", ".join(sorted(discarded)) + " have been discarded"


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
                label = f"{abbrevs[rep]}, ..."
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

    One-hop stacks are ignored so focused templates-as-nodes graphs only
    reflect stacks longer than two nodes.
    """
    focused_edges = {}
    for edges_for_column in _focused_edges_by_column_from_stack_counts(
        stack_counts,
        target,
        discarded=discarded,
    ).values():
        for edge, count in edges_for_column.items():
            focused_edges[edge] = focused_edges.get(edge, 0) + count
    return focused_edges


def _focused_edges_by_column_from_stack_counts(stack_counts, target, discarded=None):
    """Return focused node-mode edges grouped by source column version."""
    if discarded is None:
        discarded = set()
    by_column = _template_stacks_by_column(stack_counts, discarded=discarded)
    focused_edges_by_column = {}
    for column, records in by_column.items():
        focused_edges = {}
        has_target = False
        for template_stack, count in records:
            if not any(_matches_target(x, target) for x in template_stack):
                continue
            has_target = True
            if len(template_stack) < _MIN_TEMPLATE_STACK_LEN_FOR_NODE_MODE:
                continue
            for caller, callee in zip(template_stack, template_stack[1:]):
                edge = (caller, callee)
                focused_edges[edge] = focused_edges.get(edge, 0) + count
        if has_target:
            focused_edges_by_column[column] = focused_edges
    return focused_edges_by_column


@dataclass(frozen=True)
class _FocusedTarget:
    tmpl_name: str
    slug: str


# First-pass focused targets for template-specific subset documentation.
# Keep this list intentionally small for now; exhaustive generation is deferred.
_FOCUSED_TARGETS = (
    _FocusedTarget("מ:כפול", "dualcant"),
    _FocusedTarget("כו״ק", uh.he_ascii_slug("כו״ק")),
    _FocusedTarget("מ:דחי", "dexi"),
)


def _generated_by_text(generator_file):
    if generator_file is None:
        return None
    return provenance.generated_by_text(generator_file)


def _full_graph_dot_paths(out_path, columns):
    needs_disambiguation = len(columns) > 1
    return [
        _with_column_suffix(out_path, column, needs_disambiguation)
        for column in columns
    ]


def _write_full_graph_dot_paths(
    stack_counts,
    out_path,
    discarded,
    generated_by,
    collapse_node_groups=None,
    preferred_representatives=None,
    prefer_shortest_representative=False,
):
    full_discarded = _discarded_for_full_graph(discarded)
    edges_by_column_no_discard = _edges_by_column_from_stack_counts(
        stack_counts,
        discarded=set(),
    )
    edges_by_column_with_full_discard = _edges_by_column_from_stack_counts(
        stack_counts,
        discarded=full_discarded,
    )
    columns = _column_versions_for_output(edges_by_column_no_discard)
    needs_disambiguation = len(columns) > 1
    for column in columns:
        column_discarded = _discarded_for_full_graph_column(full_discarded, column)
        if column_discarded:
            edges = edges_by_column_with_full_discard.get(column, {})
        else:
            edges = edges_by_column_no_discard.get(column, {})
        note = _discard_note_text(column_discarded)
        collapsed_edges, groups = dot_node_collapse.collapse_edges_for_output(
            edges,
            _COLUMN_LETTERS,
            collapse_node_groups=collapse_node_groups,
            preferred_representatives=preferred_representatives,
            prefer_shortest_representative=prefer_shortest_representative,
        )
        dot_path = _with_column_suffix(out_path, column, needs_disambiguation)
        with open(dot_path, "w", encoding="utf-8", newline="") as fp:
            _write_dot(
                collapsed_edges,
                groups,
                fp,
                note=note,
                generated_by=generated_by,
            )
    _maybe_remove_legacy_unsuffixed(out_path, needs_disambiguation)
    return _full_graph_dot_paths(out_path, columns)


def _svg_paths_for_dot_paths(dot_paths, dot_base_path, svg_base_path):
    svg_paths = []
    dot_base_root, _ = os.path.splitext(dot_base_path)
    svg_base_root, svg_ext = os.path.splitext(svg_base_path)
    for dot_path in dot_paths:
        dot_root, _ = os.path.splitext(dot_path)
        if dot_root == dot_base_root:
            suffix = ""
        else:
            suffix = dot_root[len(dot_base_root) :]
        svg_paths.append(f"{svg_base_root}{suffix}{svg_ext}")
    return svg_paths


def write_dot_file(
    stack_counts,
    out_path,
    discarded=None,
    generator_file=None,
    collapse_node_groups=None,
    preferred_representatives=None,
    prefer_shortest_representative=False,
):
    """Write a .dot call graph from raw stack_counts accumulator."""
    generated_by = _generated_by_text(generator_file)
    _write_full_graph_dot_paths(
        stack_counts,
        out_path,
        discarded=discarded,
        generated_by=generated_by,
        collapse_node_groups=collapse_node_groups,
        preferred_representatives=preferred_representatives,
        prefer_shortest_representative=prefer_shortest_representative,
    )


def write_dot_and_svg_files(
    stack_counts,
    dot_path,
    svg_path,
    discarded=None,
    generator_file=None,
    collapse_node_groups=None,
    preferred_representatives=None,
    prefer_shortest_representative=False,
):
    """Write column-versioned full .dot files and render matching .svg files."""
    generated_by = _generated_by_text(generator_file)
    dot_paths = _write_full_graph_dot_paths(
        stack_counts,
        dot_path,
        discarded=discarded,
        generated_by=generated_by,
        collapse_node_groups=collapse_node_groups,
        preferred_representatives=preferred_representatives,
        prefer_shortest_representative=prefer_shortest_representative,
    )
    svg_paths = _svg_paths_for_dot_paths(dot_paths, dot_path, svg_path)
    for out_dot_path, out_svg_path in zip(dot_paths, svg_paths):
        render_svg(out_dot_path, out_svg_path, generator_file=generator_file)
    _maybe_remove_legacy_unsuffixed(
        svg_path,
        needs_disambiguation=(len(dot_paths) > 1),
    )


def _identity_groups(edges):
    """Return trivial groups (each node maps to itself) — no collapsing."""
    all_nodes = set()
    for caller, callee in edges:
        all_nodes.add(caller)
        all_nodes.add(callee)
    return {node: [node] for node in all_nodes - _COLUMN_LETTERS}


def _focused_discarded_for_target(target, full_discarded):
    """Return discard set used for a specific focused target."""
    if target in full_discarded:
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
        focused_discarded = _focused_discarded_for_target(target, full_discarded)
        edges_by_column = _focused_edges_by_column_from_stack_counts(
            stack_counts,
            target,
            discarded=focused_discarded,
        )
        note = _discard_note_text(focused_discarded)
        columns = _column_versions_for_output(edges_by_column)
        needs_disambiguation = len(columns) > 1
        base_dot_path = f"{stem}-{slug}-call-graph.dot"
        base_svg_path = f"{svg_stem}-{slug}-call-graph.svg"
        for column in columns:
            edges = edges_by_column.get(column, {})
            groups = _identity_groups(edges)
            dot_path = _with_column_suffix(base_dot_path, column, needs_disambiguation)
            svg_path = _with_column_suffix(base_svg_path, column, needs_disambiguation)
            with open(dot_path, "w", encoding="utf-8", newline="") as fp:
                _write_dot(
                    edges,
                    groups,
                    fp,
                    note=note,
                    focus_target=target,
                    generated_by=generated_by,
                )
            render_svg(dot_path, svg_path, generator_file=generator_file)
        _maybe_remove_legacy_unsuffixed(base_dot_path, needs_disambiguation)
        _maybe_remove_legacy_unsuffixed(base_svg_path, needs_disambiguation)


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
    with open(svg_path, "w", encoding="utf-8", newline="") as svg_fp:
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
            with open(svg_path, "w", encoding="utf-8", newline="") as svg_fp:
                svg_fp.write(normalized_svg_text)
    return True
