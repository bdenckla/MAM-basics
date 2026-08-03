"""Exports read"""

import re
import csv

import uxlc_paths


def read():
    """Read BHL Appendix A info from a CSV file"""
    path = uxlc_paths.uxlc_misc_dir() / "BHL Appendix A Psalms.csv"
    with open(path, encoding="utf-8") as csv_in_fp:
        rows = tuple(map(_bhla_row_make, csv.reader(csv_in_fp)))
    dic = {_bhla_row_locale(row): True for row in rows}
    return dic


def _bhla_row_make(list_of_cell_vals):
    return list_of_cell_vals


def _bhla_row_locale(bhla_row):
    # bsccv: book, space, chapter, colon, verse
    # E.g., Ps 7:3
    bsccv = bhla_row[0]
    maybe_wi = bhla_row[1]  # wi: word index
    if maybe_wi and maybe_wi != "-":
        assert re.match(r"\d+", maybe_wi)
        return bsccv + "." + maybe_wi
    return bsccv
