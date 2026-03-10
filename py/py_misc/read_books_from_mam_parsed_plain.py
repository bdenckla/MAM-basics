import json
from pycmn import hebrew_verse_numerals as hvn
from pycmn import bib_locales as tbn
from pycmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from pycmn import ws_tmpl1 as wtp1
from pycmn import my_utils
from pycmn.minirow import MinirowExt


def read_parsed_plain_bk39s(bk39ids=None, mam_parsed_path="../MAM-parsed"):
    """Read all bk24s covering bk39ids"""
    real_bk39ids = bk39ids or tbn.ALL_BK39_IDS
    books_out = {}
    # Can we get rid of this "for" loop?
    for bk24id in _bk24ids(real_bk39ids):
        folder = f"{mam_parsed_path}/plain"
        osdf24 = tbn.ordered_short_dash_full_24(bk24id)
        in_path = f"{folder}/{osdf24}.json"
        read_parsed_plain_bk24(in_path, books_out)
    return books_out


def read_parsed_plain_bk24(in_path, io_books):
    """Read MAM-parsed JSON at in_path into io_books."""
    # XXX TODO: what is the maximum verse number?
    # bk39: a book in the "1 of 39" division of books
    with open(in_path, encoding="utf-8") as json_in_fp:
        in_bk24 = json.load(json_in_fp)
    last_real_bcvt = None
    # Can we get rid of this "for" loop?
    for in_bk39 in in_bk24["book39s"]:
        he_bn_sbn = in_bk39["book24_name"], in_bk39["sub_book_name"]
        bk39id = mbkn_a_sbkn.MAM_HBNP_TO_BK39ID[he_bn_sbn]
        out_bk39 = _initial_book(in_bk39)
        my_utils.init_at_key(io_books, bk39id, out_bk39)
        last_real_bcvt = _read_parsed_plain_chapters(
            bk39id, in_bk39["chapters"], last_real_bcvt, io_books
        )


def _make_minirowext(psv_cp, psv_dp, psv_ep):
    return MinirowExt(tuple(psv_cp), tuple(psv_dp), tuple(psv_ep), tuple())


def _good_ending(chapters):
    last_he_chnu = tuple(chapters.keys())[-1]
    last_chapter = chapters[last_he_chnu]
    # Good endings are always wrapped in doc templates,
    # and they are the only thing in the CP of a triple-tav row
    # that is wrapped in a doc template.
    minirow = _make_minirowext(*last_chapter["תתת"])
    # Can we get rid of this "for" loop?
    for idx, wtel in enumerate(minirow.CP):
        if wtel == {"custom_tag": "קטע התחלה=סיום בטוב/"}:
            wteli1 = minirow.CP[idx + 1]
            wteli2 = minirow.CP[idx + 2]
            assert wtp1.is_doc_template(wteli1)
            assert wteli2 == {"custom_tag": "קטע סוף=סיום בטוב/"}
            return wteli1
    return None


def _initial_book(bk39):
    initial_book = {}
    initial_book["good_ending_plain"] = _good_ending(bk39["chapters"])
    initial_book["chapter_prefixes"] = {}
    initial_book["chapter_suffixes"] = {}
    initial_book["verses_plain"] = {}
    return initial_book


_KEY_FOR_ZOT = {"0": "chapter_prefixes", "תתת": "chapter_suffixes"}


def _read_parsed_plain_verse(b_ic_hv, minirow, last_real_bcvt, io_books):
    bk39id, int_chnu, he_vrnu = b_ic_hv
    int_vrnu = hvn.STR_TO_INT_DIC[he_vrnu]
    cvt = tbn.mk_cvtmam(int_chnu, int_vrnu)
    my_utils.init_at_key(io_books[bk39id]["verses_plain"], cvt, minirow)
    if last_real_bcvt is not None:
        _add_next_cp(minirow.CP, last_real_bcvt, io_books)
    return tbn.mk_bcvt(bk39id, cvt)  # last_real_bcvt


def _add_next_cp(next_cp, last_real_bcvt, io_books):
    # overwrite a minirow with a version of itself that has a next_CP
    lrbk39id = tbn.bcvt_get_bk39id(last_real_bcvt)
    lrcvt = tbn.bcvt_get_cvt(last_real_bcvt)
    vepl = io_books[lrbk39id]["verses_plain"]
    lrm = vepl[lrcvt]  # last real minirow
    vepl[lrcvt] = MinirowExt(lrm.CP, lrm.DP, lrm.EP, next_cp)


# Note on he_psv_psn (pseudo-verse's pseudo-number)
#
# Pseudo-numbers are '0' and 'תתת'.
# Aka "zot", aka zero or triple-tav.
# Real numbers are represented as Hebrew numerals, e.g. 'א'.
#
# So, in all:
#
#    '0',
#    'א',
#    'ב',
#    ...
#    'תתת'
#
# (Note that the first element is '0',
# a string consisting of the character for zero,
# not 0, the integer 0.)
#
# Note on cvt (c, v, t)
#     c: chapter number (integer)
#     v: verse number (integer)
#     t: vtrad (versification tradition) (always VT_MAM in this context)


def _read_parsed_plain_chapters(bk39id, chapters, last_real_bcvt, io_books):
    # he_psv_psn: pseudo-verse's pseudo-number. See note above.
    #
    # psv_contents: pseudo-verse contents: a 3-element list,
    #     with the elements being cells C, D, & E, in parsed form.
    # cvt: c, v, t. See note above.
    # Can we get rid of this (nested) "for" loop?
    for he_chnu, ch_contents in chapters.items():
        int_chnu = hvn.STR_TO_INT_DIC[he_chnu]
        for he_psv_psn, psv_contents in ch_contents.items():
            b_ic_hv = bk39id, int_chnu, he_psv_psn
            last_real_bcvt = _read_parsed_plain_psv(
                b_ic_hv, psv_contents, last_real_bcvt, io_books
            )
    return last_real_bcvt


def _read_parsed_plain_psv(b_ic_hv, psv_contents, last_real_bcvt, io_books):
    bk39id, int_chnu, he_psv_psn = b_ic_hv
    minirow = _make_minirowext(*psv_contents)
    if he_psv_psn not in ("0", "תתת"):
        last_real_bcvt = _read_parsed_plain_verse(
            b_ic_hv, minirow, last_real_bcvt, io_books
        )
    else:
        assert not minirow.DP
        assert not minirow.EP
        # zot: zero or triple-tav, i.e. not a real verse number
        zot = he_psv_psn  # we know it is '0' or 'תתת'
        kfz = _KEY_FOR_ZOT[zot]
        my_utils.init_at_key(io_books[bk39id][kfz], int_chnu, minirow.CP)
    return last_real_bcvt


def _bk24ids(bk39ids):
    # We use a dic to preserve order
    dic = {tbn.bk24id(bk39id): 1 for bk39id in bk39ids}
    return tuple(dic.keys())
