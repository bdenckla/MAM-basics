"""Exports in_str, in_seq"""

from py_misc import hebrew_letter_names as hln
from pycmn import hebrew_punctuation as hpu
from pycmn import my_utils


def in_str(string):
    """
    Use true Unicode gershayim instead of:
        "Q2": U+201D QUOTATION MARK (ASCII double quote)
        "R2": U+201D RIGHT DOUBLE QUOTATION MARK
    """
    new_string = string
    for x2str, g2str in _X2_STR_TO_G2_STR_PAIRS:
        new_string = new_string.replace(x2str, g2str)
    return new_string


def in_seq(seq):
    """For each el of seq that is a str, use_true_gershayim_in_str"""
    return my_utils.ss_map(_true_in_el, seq)


def _true_in_el(elem):
    return in_str(elem) if isinstance(elem, str) else elem


_Q2_STRS = (
    *hln.LETTER_NAMES_Q2,
    #
    'פת"ח',  # patax?
    'קמ"ץ',  # qamats?
    'מ"מ',  # Mechon Mamre
    'אמ"ת',  # Emet (EMT)
    'מ"ק',  # Masorah qetanah
    'כתי"ל',  # MSL (Manuscript L)
    'כתי"א',  # MSA (Manuscript A)
    'כתי"ת',  # MST (Manuscript T[av])
    'כתי"ש',  # MS$ (Manuscript $[hin] [Shin]) (covers כתי"ש1 too)
    'ע"פ',
    'מ"ס-ל',  # Masorah of [Manuscript] L
    'מ"ש',  # Minxat Shai
    'מ"ג',  # Masorah gedolah + Miqraot Gedolot too?
    'מג"ה',  # Miqraot Gedolot Haketer
    'רמ"ה',  # Ramah?
    'רד"ק',  # Radaq?
)
_Q2_TO_G2 = str.maketrans({'"': hpu.GERSHAYIM})
_Q2_TO_R2 = str.maketrans({'"': "”"})
_Q2_STR_TO_G2_STR_PAIRS = tuple(
    (string, string.translate(_Q2_TO_G2)) for string in _Q2_STRS
)
_R2_STR_TO_G2_STR_PAIRS = tuple(
    (string.translate(_Q2_TO_R2), string.translate(_Q2_TO_G2)) for string in _Q2_STRS
)
_X2_STR_TO_G2_STR_PAIRS = _Q2_STR_TO_G2_STR_PAIRS + _R2_STR_TO_G2_STR_PAIRS
