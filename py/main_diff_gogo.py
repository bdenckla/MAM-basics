"""
Diff two Go (Google Sheets) snapshots of MAM and write the results to JSON.

Compares the 2021-12-07 and 2023-04-06 snapshots, producing a set of
per-verse difference records that describe what changed between the two.
"""

from py_misc import read_books_from_mam_parsed_plain as plain
from py_misc import my_utils_for_mainish as my_utils_fm
import main_parse_go
from pycmn import file_io
from pycmn import bib_locales as tbn
from pydiff_mm import gogo_20211207
from pydiff_mm import gogo_20230406
from pydiff_mm import diff_mm_reduce as red


def _make_row_for_writing(diff):
    bkid = diff["bkid"]
    chnu = diff["cvt"][0]
    vrnu = diff["cvt"][1]
    return {
        "sena": diff["sena"],
        "bcv": tbn.short_bcv((bkid, chnu, vrnu)),
        "field": diff["field"],
        "ga": diff["mama"],  # ga = Google alternate
        "gc": diff["mamb"],  # gc = Google current
        "refine": diff["refine"],
        "refine_cat": diff["refine_cat"],
    }


def _write_diffs(diffs, mam_infos):
    # opq: output path qualifier
    rows_for_writing = tuple(map(_make_row_for_writing, diffs))
    opq_alt = mam_infos["alt"]["mi-out_path_qualifier"]
    opq_cur = mam_infos["cur"]["mi-out_path_qualifier"]
    out_path = _DIFF_OUTPUT_ALT_CUR_JSON_DIC[(opq_alt, opq_cur)]
    file_io.json_dump_to_file_path(rows_for_writing, out_path)


FIOI_DIFF_OUTPUT_ALT_CUR_JSON = (
    "io/diff_go_go/diff_output_mam_go20211207_go20230406.json"
)
_DIFF_OUTPUT_ALT_CUR_JSON_DIC = {
    ("go20211207", "go20230406"): FIOI_DIFF_OUTPUT_ALT_CUR_JSON,
}


def _write_mce_dics_ac(secid, mce_dics_ac, mam_infos):
    # opq: output path qualifier
    for side in "alt", "cur":
        ovs_for_section = []
        for bkid, mce_dic_ac in mce_dics_ac.items():
            ovs_for_book = _out_verses(bkid, mce_dic_ac[side])
            ovs_for_section.extend(ovs_for_book)
        opq = mam_infos[side]["mi-out_path_qualifier"]
        suffix = f"{opq}_{side}_{secid}"
        out_path = f"out/diff_go_go/diff_input_mam_{suffix}.json"
        file_io.json_dump_to_file_path(ovs_for_section, out_path)


def _out_verses(bkid, mce_dic):
    return tuple(_out_verse(bkid, item) for item in mce_dic.items())


def _out_verse(bkid, cvt_and_cell_e):
    cvt, cell_e = cvt_and_cell_e
    chnu, vrnu = tbn.cvt_get_chnu_vrnu(cvt)
    return {"bcv": tbn.short_bcv((bkid, chnu, vrnu)), "cell_e": cell_e}


def _do_one_book_of_tanakh(sebk, verses_ac, sec_diffs, mce_dics_ac):
    bkid = sebk[1]
    my_utils_fm.show_progress_g(__file__, "book", bkid)
    mce_dic_ac = {
        "alt": gogo_20211207.massage(verses_ac["alt"]),
        "cur": gogo_20230406.massage(verses_ac["cur"]),
    }
    mce_dics_ac[bkid] = mce_dic_ac
    bds = red.get_book_diffs_goalt_gocur(sebk, mce_dic_ac)
    red.diffs_struct_extend(sec_diffs, bds)


def _read_section_from_csv(secid, mam_info):
    # Write CSV to JSON and then read it right back in.
    opq = mam_info["mi-out_path_qualifier"]
    outfolder = f"out/go-parsed-alt/{opq}"
    out_paths = main_parse_go.do_one_section(secid, outfolder, mam_info)
    io_books = {}
    for out_paths_for_bk24 in out_paths:
        plain.read_parsed_plain_bk24(out_paths_for_bk24["plain"], io_books)
    return io_books


def _do_one_section_of_tanakh(secid, mam_infos):
    sec_diffs = red.diffs_struct_mk()
    section_alt = _read_section_from_csv(secid, mam_infos["alt"])
    section_cur = _read_section_from_csv(secid, mam_infos["cur"])
    mce_dics_ac = {}
    for bkid in tbn.bk39s_of_sec(secid):
        verses_ac = {
            "alt": section_alt[bkid]["verses_plain"],
            "cur": section_cur[bkid]["verses_plain"],
        }
        _do_one_book_of_tanakh(
            (secid, bkid),
            verses_ac,
            sec_diffs,
            mce_dics_ac,
        )
    return sec_diffs, mce_dics_ac


def main():
    """
    Computes differences between two versions of the MAM CSVs.
    (The MAM CSVs are exported from the MAM Google Sheet.)
    The two versions of the MAM CSVs compared are:
        * 2021-12-07 (the "alternate" ("old") version)
        * 2023-04-06 (the "current" version)
    2021-12-07 corresponds (I think) to the most recent Sefaria
    release, as of this writing.
    2023-04-06 is the current version, as of this writing.
    """
    mam_infos = {
        "alt": {
            "mi-csv_dir": "in/mam-go-2021-12-07",  # CSV dir
            "mi-out_path_qualifier": "go20211207",
            "mi-skip_hard_c_cells": True,
        },
        "cur": {
            "mi-csv_dir": "in/mam-go-2023-04-06",  # CSV dir
            "mi-out_path_qualifier": "go20230406",
        },
    }
    all_diffs = red.diffs_struct_mk()
    for secid in tbn.ALL_SECIDS:
        sec_diffs, mce_dics_ac = _do_one_section_of_tanakh(secid, mam_infos)
        red.diffs_struct_extend(all_diffs, sec_diffs)
        _write_mce_dics_ac(secid, mce_dics_ac, mam_infos)
    _write_diffs(all_diffs["diffs_list"], mam_infos)


if __name__ == "__main__":
    main()
