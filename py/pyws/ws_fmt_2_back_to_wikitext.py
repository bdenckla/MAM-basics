""" Exports big_str """

import re
from functools import partial
from pyws import ws_unparse
from pycmn.my_utils import dkv_map
from pycmn.my_utils import dv_dispatch


def big_str(he_chnu, wsf2_chap):
    fn_table = {
        "ws-chap-noinclude-header": _unparse_chap_noinclude_xxx,
        "ws-chap-body": partial(_dt_unparse_chap_body, he_chnu),
        "ws-chap-good-ending": _dt_unparse_chap_good_ending,
        "ws-chap-noinclude-footer": _unparse_chap_noinclude_xxx,
        "ws-chap-category": _dt_unparse_chap_category,
    }
    svd = dv_dispatch(fn_table, wsf2_chap)
    big_str = "".join(svd.values())  # svd: string-valued dict
    assert "¶" not in big_str
    return big_str


def _dt_unparse_chap_body(he_chnu, chap_body):
    svd = dkv_map(_unparse_plb_verse, chap_body)
    body = "".join(svd.values())  # svd: string-valued dict
    return _qeta_wrap(body, f"פרק {he_chnu}")


def _dt_unparse_chap_good_ending(gden):
    body = ws_unparse.unparse(gden)
    return "\n\n" + _qeta_wrap(body, "סיום בטוב")


def _dt_unparse_chap_category(chap_category):
    return "\n" + chap_category  # e.g. '\n[[קטגוריה:משלי א]]'


def _dt_unparse_verse_prefix(verse_prefix):
    return ws_unparse.unparse(verse_prefix)


def _dt_unparse_verse_location(verse_location):
    body = ws_unparse.unparse(verse_location)
    return _qeta_wrap(body, "סימן")


def _dt_unparse_verse_body(he_vrnu, verse_body):
    body = ws_unparse.unparse(verse_body)
    return _qeta_wrap(body, he_vrnu)


def _unparse_chap_noinclude_xxx(chap_noinclude_xxx):
    mapped = list(map(ws_unparse.unparse, chap_noinclude_xxx))
    joined = _join_and_ptrn(mapped)
    return "<noinclude>" + joined + "</noinclude>"


def _unparse_plb_verse(he_vrnu, plb_verse):
    fn_table = {
        "prefix": _dt_unparse_verse_prefix,
        "location": _dt_unparse_verse_location,
        "verse-body": partial(_dt_unparse_verse_body, he_vrnu),
    }
    svd = dv_dispatch(fn_table, plb_verse)
    return _join_and_ptrn(svd.values())  # svd: string-valued dict


def _join_and_ptrn(lis_of_str):  # ptrn: pilcrow to newline
    joined = "".join(lis_of_str)
    return joined.replace("¶", "\n")


def _qeta_wrap(body, right_hand_side):
    start = f"<קטע התחלה={right_hand_side}/>"
    end = f"<קטע סוף={right_hand_side}/>"
    return start + body + end
