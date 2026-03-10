"""Generate a Graphviz dot file showing the template call graph."""

import os
import shutil
import subprocess

_COLUMN_LETTERS = {"C", "D", "E"}
_DOT_FALLBACK = os.path.join(
    os.environ.get("ProgramFiles", r"C:\Program Files"), "Graphviz", "bin", "dot.exe"
)


def _edges_from_stack_counts(stack_counts):
    """Extract (caller, callee) -> count from raw stack_counts defaultdict."""
    edges = {}
    for key, count in stack_counts.items():
        wtel_subtype, stack_str = key
        parts = stack_str.split("/")
        if len(parts) >= 2 and parts[1] == "נוסח":
            parts = parts[:1] + parts[2:]
        caller = parts[-1]
        callee = wtel_subtype
        if callee == "נוסח":
            continue
        edge = (caller, callee)
        edges[edge] = edges.get(edge, 0) + count
    return edges


def _dot_quoted(name):
    """Quote a string for use as a dot identifier or label."""
    escaped = name.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _write_dot(edges, fp):
    fp.write("digraph template_call_graph {\n")
    fp.write("    rankdir=LR;\n")
    fp.write('    node [fontname="SBL Hebrew,Helvetica", fontsize=12];\n')
    fp.write('    edge [fontname="Helvetica", fontsize=9];\n')
    fp.write("\n")
    # Column nodes styled distinctly
    fp.write("    // Column nodes\n")
    fp.write("    node [shape=box, style=bold];\n")
    for col in sorted(_COLUMN_LETTERS):
        fp.write(f"    {_dot_quoted(col)};\n")
    fp.write("\n")
    # Template nodes
    fp.write("    // Template nodes\n")
    fp.write('    node [shape=box, style=""];\n')
    fp.write("\n")
    # Note
    fp.write("    // Note\n")
    fp.write('    graph [label="נוסח has been contracted", labelloc=b, fontsize=10];\n')
    fp.write("\n")
    # Edges sorted for stable output
    fp.write("    // Edges\n")
    for (caller, callee), count in sorted(edges.items()):
        fp.write(
            f"    {_dot_quoted(caller)} -> {_dot_quoted(callee)}" f' [label="{count}"];\n'
        )
    fp.write("}\n")


def write_dot_file(stack_counts, out_path):
    """Write a .dot call graph from raw stack_counts accumulator."""
    edges = _edges_from_stack_counts(stack_counts)
    with open(out_path, "w", encoding="utf-8") as fp:
        _write_dot(edges, fp)


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
