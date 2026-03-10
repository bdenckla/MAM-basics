"""
Diff Ws (Wikisource) vs. Go (Google Sheets) versions of MAM and produce
auto-edits output for applying the differences back to the Google Sheet.
"""

from py_misc import my_utils_for_mainish as my_utils_fm
from py_misc import read_books_from_mam_parsed_plain as plain
from pycmn import bib_locales as tbn
from pycmn import file_io
from pycmn import hebrew_verse_numerals as hvn
from pycmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from pycmn import uni_denorm as ud
from pydiff_mm import diff_mm_reduce as red
from pydiff_mm import diff_mm_wsgo_auto_edits as auto_edits
from pydiff_mm import wsgo_go
from pydiff_mm import wsgo_ws
from pyws import ws_get_bk_in_both_fmts as wsin


def _make_dump_diff(diff):
    # Make a diff suitable for dumping to a JSON file.
    bkid = diff["bkid"]
    chnu = diff["cvt"][0]
    vrnu = diff["cvt"][1]
    return {
        "sena": diff["sena"],
        "bcv": tbn.short_bcv((bkid, chnu, vrnu)),
        "field": diff["field"],
        "ws": diff["mama"],
        "go": diff["mamb"],
        "refine": diff["refine"],
        "ws-full": diff["fulla"],
        "go-full": diff["fullb"],
    }


def _do_one_section_of_tanakh(secid):
    sec_diffs = red.diffs_struct_mk()
    books_of_sec = tbn.bk39s_of_sec(secid)
    go_books_raw = plain.read_parsed_plain_bk39s(books_of_sec)
    for bkid in books_of_sec:
        my_utils_fm.show_progress_g(__file__, "book", bkid)
        wsf2_book = wsin.get_bk_in_fmt_2(_IN_PATH, bkid)
        ws_book_raw = wsf2_book
        go_book_raw = go_books_raw[bkid]
        ws_book = wsgo_ws.massage_ws_book(ws_book_raw)
        go_book = wsgo_go.massage_go_book(go_book_raw)
        bds = red.get_book_diffs_ws_go((secid, bkid), ws_book, go_book)
        red.diffs_struct_extend(sec_diffs, bds)
    return sec_diffs


_FIELD_TO_COLUMN = {"prefix": "C", "location": "D", "verse-body": "E"}
_IN_PATH = "in/mam-ws"
_TAB_NAMES_IN_GOOGLE_SHEET = {
    tbn.SEC_TORAH: "תורה",
    tbn.SEC_NEV_RISH: "נביאים ראשונים",
    tbn.SEC_NEV_AX: "נביאים אחרונים",
    tbn.SEC_SIF_EM: 'ספרי אמ"ת',
    tbn.SEC_XAM_MEG: "חמש מגילות",
    tbn.SEC_KET_AX: "כתובים אחרונים",
}


def _bk24na_slash_chap_id(bk39id, chnu):
    # A chapter ID is usually just a Hebrew chapter.
    # But, for book24s with sub-books, the chapter ID
    # includes the sub-book.
    he_chnu = hvn.INT_TO_STR_DIC[chnu]
    mam_he_book_name_pair = mbkn_a_sbkn.BK39ID_TO_MAM_HBNP[bk39id]
    bk24na, sub_bkna = mam_he_book_name_pair
    chap_id = he_chnu if sub_bkna is None else f"{sub_bkna} {he_chnu}"
    return f"{bk24na}/{chap_id}"


def _make_auto_edit(diff):
    secid, bk39id, field = diff["sena"], diff["bkid"], diff["field"]
    chnu, int_vrnu_or_zot = diff["cvt"][0:2]
    dws = ud.give_std_mark_order("".join(diff["ws"]))
    dgo = ud.give_std_mark_order("".join(diff["go"]))
    assert dws != dgo
    auto_edit = {
        "sena": _TAB_NAMES_IN_GOOGLE_SHEET[secid],
        "bk24na_slash_chap_id": _bk24na_slash_chap_id(bk39id, chnu),
        "vrnu": _int_or_zot_to_he(int_vrnu_or_zot),
        "column": _FIELD_TO_COLUMN[field],
        "search_str": dgo,
        "replace_str": dws,
    }
    return auto_edit


def _int_or_zot_to_he(int_vrnu_or_zot):
    if int_vrnu_or_zot == "תתת":
        return "תתת"
    if int_vrnu_or_zot == "0":
        return "0"
    return hvn.INT_TO_STR_DIC[int_vrnu_or_zot]


def _dump_helper(all_diffs, key_for_xxx):
    make_yyy = _MAKE_YYY[key_for_xxx]
    all_diffs_xxx = all_diffs[key_for_xxx]
    out_path_xxx = _OUT_PATHS[key_for_xxx]
    xxx_diffs = tuple(map(make_yyy, all_diffs_xxx))
    file_io.json_dump_to_file_path(xxx_diffs, out_path_xxx)


def almost_main():
    """Compute differences between MAM Wikisource & MAM Google Sheet"""
    auto_edits.self_test()
    all_diffs = red.diffs_struct_mk()
    for secid in tbn.ALL_SECIDS:
        sec_diffs = _do_one_section_of_tanakh(secid)
        red.diffs_struct_extend(all_diffs, sec_diffs)
    #
    _dump_helper(all_diffs, "diffs_list")
    _dump_helper(all_diffs, "srrps_list")


_MAKE_YYY = {
    "diffs_list": _make_dump_diff,
    "srrps_list": _make_auto_edit,
}
_OUT_PATHS = {
    "diffs_list": "out/diff_mamws_mamgo.json",
    "srrps_list": "../mamgo-auto-edits/diff_mamws_mamgo-auto-edits.json",
}


def main():
    """Compute differences between MAM Wikisource & MAM Google Sheet"""
    almost_main()


if __name__ == "__main__":
    main()
