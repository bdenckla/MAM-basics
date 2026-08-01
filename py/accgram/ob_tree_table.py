from __future__ import annotations

from dataclasses import dataclass

from accgram import ob_tree_abbrev
from accgram import ob_tree_parse
from py_html import wlc_utils_html


@dataclass
class _Cell:
    start_col: int
    colspan: int
    text: str
    title_text: str | None = None
    class_name: str | None = None


def render_error_tree_table(
    tree: ob_tree_parse.ErrorTree,
    *,
    gray_leaf_cols: frozenset[int] | None = None,
) -> object:
    """Render the parse tree as an HTML table.

    ``gray_leaf_cols`` (leaf-column indices, left-to-right) de-emphasizes those leaf cells
    and any internal cell whose whole leaf span lies within them -- used by the dt 5:8
    dual-cant display to spotlight the in-focus verse's columns of the elyon tree."""
    if not tree.roots:
        raise ValueError("Cannot render an empty parse tree")

    spans_by_branch: dict[int, int] = {}
    for root in tree.roots:
        _compute_leaf_span(root, spans_by_branch)

    total_cols = sum(spans_by_branch[id(root)] for root in tree.roots)
    if total_cols <= 0:
        raise ValueError("Parse tree has no terminal leaves")

    max_branch_depth = max(_max_branch_depth(root) for root in tree.roots)
    leaf_row_index = max_branch_depth + 1

    rows_by_index: dict[int, list[_Cell]] = {}

    current_col = 0
    for root in tree.roots:
        _emit_branch_cells(
            branch=root,
            start_col=current_col,
            leaf_row_index=leaf_row_index,
            spans_by_branch=spans_by_branch,
            rows_by_index=rows_by_index,
            gray_leaf_cols=gray_leaf_cols,
        )
        current_col += spans_by_branch[id(root)]

    rendered_row_indexes = sorted(rows_by_index)
    if not rendered_row_indexes:
        raise ValueError("Parse tree produced no renderable rows")

    table_rows: list[object] = []
    for row_index in rendered_row_indexes:
        row_cells = sorted(
            rows_by_index.get(row_index, []), key=lambda cell: cell.start_col
        )
        depth_cell_text = "" if row_index == leaf_row_index else str(row_index)
        table_rows.append(
            _render_row(
                row_cells=row_cells,
                total_cols=total_cols,
                depth_cell_text=depth_cell_text,
            )
        )

    return wlc_utils_html.table(
        tuple(table_rows),
        {"class": "goerwitz-obs-error-table"},
    )


def _compute_leaf_span(
    branch: ob_tree_parse.TreeBranch,
    spans_by_branch: dict[int, int],
) -> int:
    span = 0
    for child in branch.children:
        if isinstance(child, ob_tree_parse.TreeLeaf):
            span += 1
        else:
            span += _compute_leaf_span(child, spans_by_branch)

    if span <= 0:
        raise ValueError(
            f"Branch has no leaves: depth={branch.depth}, label={branch.label!r}"
        )

    spans_by_branch[id(branch)] = span
    return span


def _max_branch_depth(branch: ob_tree_parse.TreeBranch) -> int:
    max_depth = branch.depth
    for child in branch.children:
        if isinstance(child, ob_tree_parse.TreeBranch):
            max_depth = max(max_depth, _max_branch_depth(child))
    return max_depth


def _emit_branch_cells(
    *,
    branch: ob_tree_parse.TreeBranch,
    start_col: int,
    leaf_row_index: int,
    spans_by_branch: dict[int, int],
    rows_by_index: dict[int, list[_Cell]],
    gray_leaf_cols: frozenset[int] | None,
) -> None:
    branch_span = spans_by_branch[id(branch)]
    _append_cell(
        rows_by_index,
        row_index=branch.depth,
        cell=_Cell(
            start_col=start_col,
            colspan=branch_span,
            text=ob_tree_abbrev.abbreviate_branch_label(branch.label),
            title_text=branch.label,
            class_name=_gray_class(start_col, branch_span, gray_leaf_cols),
        ),
    )

    child_col = start_col
    for child in branch.children:
        if isinstance(child, ob_tree_parse.TreeLeaf):
            _append_cell(
                rows_by_index,
                row_index=leaf_row_index,
                cell=_Cell(
                    start_col=child_col,
                    colspan=1,
                    text=ob_tree_abbrev.abbreviate_leaf_text(child.text),
                    title_text=child.text,
                    class_name=(
                        "goerwitz-obs-error-cell"
                        if child.has_error
                        else _gray_class(child_col, 1, gray_leaf_cols)
                    ),
                ),
            )
            child_col += 1
            continue

        _emit_branch_cells(
            branch=child,
            start_col=child_col,
            leaf_row_index=leaf_row_index,
            spans_by_branch=spans_by_branch,
            rows_by_index=rows_by_index,
            gray_leaf_cols=gray_leaf_cols,
        )
        child_col += spans_by_branch[id(child)]


def _gray_class(
    start_col: int, span: int, gray_leaf_cols: frozenset[int] | None
) -> str | None:
    """``goerwitz-obs-context-cell`` when this cell's whole leaf span is out of focus."""
    if not gray_leaf_cols:
        return None
    if all((start_col + i) in gray_leaf_cols for i in range(span)):
        return "goerwitz-obs-context-cell"
    return None


def _append_cell(
    rows_by_index: dict[int, list[_Cell]],
    *,
    row_index: int,
    cell: _Cell,
) -> None:
    rows_by_index.setdefault(row_index, []).append(cell)


def _render_row(
    *, row_cells: list[_Cell], total_cols: int, depth_cell_text: str
) -> object:
    td_cells: list[object] = [
        wlc_utils_html.table_datum(
            depth_cell_text,
            {"class": "goerwitz-obs-depth-cell"},
        )
    ]
    cursor = 0
    for cell in row_cells:
        if cell.start_col > cursor:
            td_cells.append(
                wlc_utils_html.table_datum(
                    "",
                    {"colspan": str(cell.start_col - cursor)},
                )
            )
            cursor = cell.start_col

        attrs: dict[str, str] = {}
        if cell.colspan > 1:
            attrs["colspan"] = str(cell.colspan)
        # The title is the un-abbreviated label, shown on hover so an abbreviated
        # cell (e.g. "slq") can be expanded ("silluq").  When the cell text was not
        # abbreviated (e.g. "ERROR", or the illegal_mark descriptor), the title
        # would just duplicate the visible text -- omit it rather than add a no-op
        # hover.
        if cell.title_text is not None and cell.title_text != cell.text:
            attrs["title"] = cell.title_text
        if cell.class_name is not None:
            attrs["class"] = cell.class_name

        td_cells.append(wlc_utils_html.table_datum(cell.text, attrs or None))
        cursor += cell.colspan

    if cursor < total_cols:
        td_cells.append(
            wlc_utils_html.table_datum(
                "",
                {"colspan": str(total_cols - cursor)},
            )
        )

    return wlc_utils_html.table_row(tuple(td_cells))
