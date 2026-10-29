from taamey_d.doc.html_helpers import xtable_rtl, xtable_data_cell, xtable_row
from taamey_d.doc.html_helpers import unordered_list


def en_by_two_table(header_cells, word_rows, class_rows, row_tad=True):
    data_rows = (
        _en_by_two_row(word_rows[0], class_rows[0], row_tad),
        _en_by_two_row(word_rows[1], class_rows[1], row_tad),
    )
    sum_of_data_rows = sum(data_rows, tuple())
    return xtable_rtl(header_cells, sum_of_data_rows)


def _en_by_two_row(word_row, class_row, row_tad):
    row_attrs = {"class": "font-family-taamey-d"} if row_tad else {}
    wc_pairs = tuple(zip(word_row, class_row))
    rows = tuple(xtable_data_cell(wcp[0], {"class": wcp[1]}) for wcp in wc_pairs)
    rows2 = tuple((row, "\n    ") for row in rows)
    sum_of_rows2 = sum(rows2, tuple())
    return "\n    ", xtable_row(sum_of_rows2, row_attrs)


def two_by_two(x):
    return (x, x), (x, x)


def one_by_two(x):
    return (x,), (x,)


def two(x):
    return (x, x)
