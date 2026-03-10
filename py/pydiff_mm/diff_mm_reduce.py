""" Exports
        get_book_diffs_ws_go
        get_book_diffs_goalt_gocur
        diffs_struct_mk
        diffs_struct_extend
"""

from pycmn import hebrew_verse_numerals as hvn
from pycmn import bib_locales as tbn
from pycmn import my_diffs
from pycmn import my_utils
from pydiff_mm import diff_mm_wsgo_auto_edits as auto_edits
from pydiff_mm import diff_mm_reduce_refine as refine
from pydiff_mm import diff_mm_reduce_make_comparable as make_comparable
from pyws import ws_unparse


def get_book_diffs_ws_go(sebk, ws_book, go_book):
    """
    This function is given:
        sebk:
            a pair of a Tanakh section ID (secid) and a book ID (bkid)
            e.g. ('Torah', 'Genesis')
        ws_book:
            the Wikisource contents of that book
        go_book:
            the Google contents of that book
    This function returns:
        the WS-Go diffs for that book.
    """
    assert _num_verses_are_equal(ws_book, go_book)
    ws_chapters = ws_book
    book_diffs = diffs_struct_mk()
    for he_chnu, ws_chapter in ws_chapters.items():
        _get_diffs_for_chapter(book_diffs, sebk, he_chnu, ws_chapter, go_book)
    return book_diffs


def get_book_diffs_goalt_gocur(sebk, mce_dic):
    """
    Given massaged cell E dictionary mce_dic, this function
    returns the GoAlt-GoCur diffs for book sebk[1] in section sebk[0]
    (sebk is a pair of a section ID (secid) and a book ID (bkid)).
    """
    book_diffs = diffs_struct_mk()
    mce_dic_alt, mce_dic_cur = mce_dic["alt"], mce_dic["cur"]
    assert len(mce_dic_alt) == len(mce_dic_cur)
    for cvt in mce_dic_alt.keys():
        cvt_af = cvt, "verse-body"
        verse_alt = mce_dic_alt[cvt]
        verse_cur = mce_dic_cur[cvt]
        vds = _get_labeled_diffs_struct(sebk, cvt_af, verse_alt, verse_cur)
        diffs_struct_extend(book_diffs, vds)
    return book_diffs


def diffs_struct_mk(diffs_list=None, srrps_list=None):
    """Make a "diffs struct" """
    return {"diffs_list": diffs_list or [], "srrps_list": srrps_list or []}


def diffs_struct_extend(accum_ds, new_ds):
    """Extends a "diffs struct" """
    accum_ds["diffs_list"].extend(new_ds["diffs_list"])
    accum_ds["srrps_list"].extend(new_ds["srrps_list"])


def _get_chap_body_diffs(io_book_diffs, sebk, he_chnu, ws_body, go_book):
    go_verses = go_book["verses_plain"]
    for he_vrnu, ws_verse in ws_body.items():
        ws_cvb = he_chnu, he_vrnu, ws_verse  # c, v, & body
        _get_verse_diffs(io_book_diffs, sebk, go_verses, ws_cvb)


def _get_chap_prefix_diffs(io_book_diffs, sebk, he_chnu, ws_golike_cp, go_book):
    int_chnu = hvn.STR_TO_INT_DIC[he_chnu]
    go_ni_header = go_book["chapter_prefixes"][int_chnu]
    ni_header_diffs = _get_nonverse_diff(sebk, he_chnu, "0", ws_golike_cp, go_ni_header)
    diffs_struct_extend(io_book_diffs, ni_header_diffs)


def _get_chap_suffix_diffs(io_book_diffs, sebk, he_chnu, ws_golike_cs, go_book):
    int_chnu = hvn.STR_TO_INT_DIC[he_chnu]
    go_cs = go_book["chapter_suffixes"][int_chnu]
    ni_footer_diffs = _get_nonverse_diff(sebk, he_chnu, "תתת", ws_golike_cs, go_cs)
    diffs_struct_extend(io_book_diffs, ni_footer_diffs)


diff_fns_for_ws_chapter_keys = {
    "ws-chap-noinclude-header": None,  # covered by golike_chapter_prefix
    "ws-chap-body": _get_chap_body_diffs,
    "ws-chap-good-ending": None,  # covered by golike_chapter_suffix
    "ws-chap-noinclude-footer": None,  # covered by golike_chapter_suffix
    "ws-chap-category": None,  # there is nothing in go_book corresponding to category
    #
    "golike_chapter_prefix": _get_chap_prefix_diffs,
    "golike_chapter_suffix": _get_chap_suffix_diffs,
}


def _get_diffs_for_chapter(io_book_diffs, sebk, he_chnu, ws_chapter, go_book):
    for key in ws_chapter:
        diff_fnq = diff_fns_for_ws_chapter_keys[key]
        if diff_fnq is not None:
            diff_fnq(io_book_diffs, sebk, he_chnu, ws_chapter[key], go_book)


def _get_nonverse_diff(sebk, he_chnu, zot, ws_ni_header_or_footer, go_prefix_or_suffix):
    int_chnu = hvn.STR_TO_INT_DIC[he_chnu]
    cvt = int_chnu, zot  # zot: zero or triple-tav
    field = "prefix"  # i.e. column C
    cvt_af = cvt, field
    return _get_labeled_diffs_struct(
        sebk, cvt_af, ws_ni_header_or_footer, go_prefix_or_suffix
    )


def _get_verse_diffs(io_book_diffs, sebk, go_verses, ws_cvb):
    he_chnu, he_vrnu, ws_verse = ws_cvb
    int_chnu = hvn.STR_TO_INT_DIC[he_chnu]
    int_vrnu = hvn.STR_TO_INT_DIC[he_vrnu]
    cvt = tbn.mk_cvtmam(int_chnu, int_vrnu)
    go_verse = go_verses[cvt]
    for field in ("prefix", "location", "verse-body"):
        cvt_af = cvt, field
        verse_diffs = _get_labeled_diffs_struct(
            sebk, cvt_af, ws_verse[field], go_verse[field]
        )
        diffs_struct_extend(io_book_diffs, verse_diffs)


def _num_verses_are_equal(ws_book, go_book):
    ws_chapters = ws_book
    go_verses = go_book["verses_plain"]
    num_verses_in_ws_book = _num_verses_in_ws_chapters(ws_chapters)
    num_verses_in_go_book = len(go_verses)
    return num_verses_in_ws_book == num_verses_in_go_book


def _num_verses_in_ws_chapters(ws_chapters):
    chapter_lens = tuple(_num_verses_in_ws_chapter(c) for c in ws_chapters.values())
    return sum(chapter_lens)


def _num_verses_in_ws_chapter(ws_chapter):
    return len(ws_chapter["ws-chap-body"])


def _str_or_none(obj):
    if obj is None:
        return None
    if isinstance(obj, list) and len(obj) == 1 and isinstance(obj[0], str):
        return obj[0]
    return str(obj)


def _refine_diff(diff):
    val_mama, val_mamb = diff
    refinement = refine.refine(val_mama, val_mamb)
    assert refinement is None or _tup_len(refinement, 2)
    details = refinement and refinement[0]
    category = refinement and refinement[1]
    return {
        "mama": _str_or_none(val_mama),
        "mamb": _str_or_none(val_mamb),
        "refine": _str_or_none(details),
        "refine_cat": _str_or_none(category),
    }


def _tup_len(obj, expected_len):
    return isinstance(obj, tuple) and len(obj) == expected_len


def _get_diff_label(sebk, cvt_af):
    return {"sena": sebk[0], "bkid": sebk[1], "cvt": cvt_af[0], "field": cvt_af[1]}


def _get_labeled_diffs_struct(sebk, cvt_af, wtseq_mama, wtseq_mamb):
    sbcv = _get_diff_label(sebk, cvt_af)
    diffs = _get_wtseq_diffs(wtseq_mama, wtseq_mamb)
    srrps = diffs and auto_edits.get_srrps(wtseq_mama, wtseq_mamb)
    return diffs_struct_mk(
        [{**sbcv, **diff} for diff in diffs], [{**sbcv, **srrp} for srrp in srrps]
    )


def _add_orig(wtseq_mama, wtseq_mamb, diff_dic):
    if not diff_dic:
        return diff_dic
    return {
        **diff_dic,
        "fulla": ws_unparse.unparse(wtseq_mama),
        "fullb": ws_unparse.unparse(wtseq_mamb),
    }


def _get_wtseq_diffs(wtseq_mama, wtseq_mamb):
    taside = make_comparable.make_comparable(wtseq_mama)
    tbside = make_comparable.make_comparable(wtseq_mamb)
    diffs = my_diffs.get(taside, tbside)
    refined = list(map(_refine_diff, diffs))
    return my_utils.sl_map((_add_orig, wtseq_mama, wtseq_mamb), refined)
