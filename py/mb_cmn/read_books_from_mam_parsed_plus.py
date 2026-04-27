import json
from pycmn import hebrew_verse_numerals as hvn
from pycmn import bib_locales as tbn
from pycmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from pycmn.minirow import MinirowExt
from pycmn.my_utils import sl_map
from pycmn.my_utils import sum_of_dics
from pycmn.my_utils import init_at_key


def read_parsed_plus_bk39s(bk39ids=None, mam_parsed_path="../MAM-parsed"):
    """Read all bk24s covering bk39ids"""
    real_bk39ids = bk39ids or tbn.ALL_BK39_IDS
    mapfunc = lambda bk24id: read_parsed_plus_bk24(bk24id, mam_parsed_path)
    lis_books_out_dics = sl_map(mapfunc, _bk24ids(real_bk39ids))
    return sum_of_dics(lis_books_out_dics)


def read_parsed_plus_bk24(bk24id, mam_parsed_path="../MAM-parsed"):
    """Read MAM-parsed JSON at in_path into io_books."""
    # bk39: a book in the "1 of 39" division of books
    osdf24 = tbn.ordered_short_dash_full_24(bk24id)
    in_path = f"{mam_parsed_path}/plus/{osdf24}.json"
    with open(in_path, encoding="utf-8") as json_in_fp:
        in_bk24 = json.load(json_in_fp)
    last_real_bcvt = None
    books_out = {}
    for in_bk39 in in_bk24["book39s"]:
        he_bn_sbn = in_bk39["book24_name"], in_bk39["sub_book_name"]
        bk39id = mbkn_a_sbkn.MAM_HBNP_TO_BK39ID[he_bn_sbn]
        out_bk39 = _initial_book(bk39id, in_bk39)
        init_at_key(books_out, bk39id, out_bk39)
        last_real_bcvt = _read_parsed_plus_chapters(
            bk39id, in_bk39["chapters"], last_real_bcvt, books_out
        )
    return books_out


def _gden_cv_to_bcvt(bk39id, good_ending):
    if good_ending is None:
        return None
    out_ge = dict(good_ending)
    # E.g. good_ending['last_chapnver'] == ['סו', 'כד']
    he_chnu = good_ending["last_chapnver"][0]
    he_vrnu = good_ending["last_chapnver"][1]
    out_ge["last_bcvt"] = tbn.mk_bcvtmam(
        bk39id, hvn.STR_TO_INT_DIC[he_chnu], hvn.STR_TO_INT_DIC[he_vrnu]
    )
    return out_ge


def _make_minirowext(psv_cp, psv_dp, psv_ep):
    return MinirowExt(tuple(psv_cp), tuple(psv_dp), tuple(psv_ep), tuple())


def _initial_book(bk39id, bk39):
    initial_book = {}
    initial_book["good_ending_with_bcvt"] = _gden_cv_to_bcvt(
        bk39id, bk39["good_ending_plus"]
    )
    initial_book["verses_plus"] = {}
    return initial_book


def _read_parsed_plus_verse(b_ic_hv, minirow, last_real_bcvt, io_books):
    bk39id, int_chnu, he_vrnu = b_ic_hv
    int_vrnu = hvn.STR_TO_INT_DIC[he_vrnu]
    bcvt = tbn.mk_bcvtmam(bk39id, int_chnu, int_vrnu)
    init_at_key(io_books[bk39id]["verses_plus"], bcvt, minirow)
    if last_real_bcvt is not None:
        _add_next_cp(minirow.CP, last_real_bcvt, io_books)
    return bcvt  # last_real_bcvt


def _add_next_cp(next_cp, last_real_bcvt, io_books):
    lrbk39id = tbn.bcvt_get_bk39id(last_real_bcvt)
    vepl = io_books[lrbk39id]["verses_plus"]
    lrm = vepl[last_real_bcvt]  # last real minirow
    vepl[last_real_bcvt] = MinirowExt(lrm.CP, lrm.DP, lrm.EP, next_cp)


def _read_parsed_plus_chapters(bk39id, chapters, last_real_bcvt, io_books):
    # he_vrnu: Hebrew verse numeral (א, ...)
    # vr_contents: verse contents: a 3-element list,
    #     with the elements being cells C, D, & E, in parsed form.
    # bcvt: b, c, v, t
    #     b: bk39id (string)
    #     c: chapter number (integer)
    #     v: verse number (integer)
    #     t: vtrad (versification tradition) (always VT_MAM in this context)
    for he_chnu, ch_contents in chapters.items():
        int_chnu = hvn.STR_TO_INT_DIC[he_chnu]
        for he_vrnu, vr_contents in ch_contents.items():
            minirow = _make_minirowext(*vr_contents)
            assert he_vrnu not in ("0", "תתת")
            b_ic_hv = bk39id, int_chnu, he_vrnu
            last_real_bcvt = _read_parsed_plus_verse(
                b_ic_hv, minirow, last_real_bcvt, io_books
            )
    return last_real_bcvt


def _bk24ids(bk39ids):
    # We use a dic to preserve order
    dic = {tbn.bk24id(bk39id): 1 for bk39id in bk39ids}
    return tuple(dic.keys())
