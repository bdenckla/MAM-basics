import py_wlc_json_and_unicode.wlc_uword as wlc_uword
from mb_cmn.my_utils import dv_dispatch
from mb_cmn.my_utils import sl_map


def convert_p_mdc_to_p_uni(p_mdc):
    """
    Convert "parsed M-C" (parsed Michigan-Claremont) (p_mdc)
    to "parsed Unicode" (p_un)
    """
    return dv_dispatch(_FN_TABLE_TOP, p_mdc)


def _convert_verse(verse):
    return dv_dispatch(_FN_TABLE_VERSE, verse)


def _convert_verse_element(vel):
    if isinstance(vel, str):
        return _FN_TABLE_VERSE_ELEMENT["string"](vel)
    return dv_dispatch(_FN_TABLE_VERSE_ELEMENT, vel)


def _convert_string(word):
    assert isinstance(word, str)
    return wlc_uword.uword(word)


def _convert_kq(ketiv_qere):
    assert isinstance(ketiv_qere, (list, tuple))
    assert len(ketiv_qere) == 2
    ketiv, qere = ketiv_qere
    assert len(ketiv) in (0, 1, 2)
    assert len(qere) in (0, 1, 2)
    return sl_map(_convert_verse_element, ketiv), sl_map(_convert_verse_element, qere)


_FN_TABLE_TOP = {
    "id": lambda x: x,
    "header": lambda x: x,
    "verses": lambda x: sl_map(_convert_verse, x),
}
_FN_TABLE_VERSE = {
    "bcv": lambda x: x,
    "vels": lambda x: sl_map(_convert_verse_element, x),
}
_FN_TABLE_VERSE_ELEMENT = {
    "string": _convert_string,
    "sam_pe_inun": lambda x: x,
    "word": _convert_string,
    "notes": lambda x: x,
    "kq": _convert_kq,
}
