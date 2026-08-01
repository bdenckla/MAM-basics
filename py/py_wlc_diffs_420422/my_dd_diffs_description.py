"""Exports get1 & get2"""

import mb_cmn.my_diffs as my_diffs
import mb_cmn.hebrew_points as hpo
from wlc_cmn import legacy_names
import py_wlc_diffs_420422.my_dd_simplify_simple_diffs as ssd
import py_wlc_diffs_420422.my_dd_lett_words as hlw


def get1(str1, str2):
    """
    If possible, get a human-friendly description of the diffs
    between str1 & str2.
    Returns a pair with the following contents:
    Element 1 of the pair is a string describing the diff in detail.
    Element 2 of the pair is a string describing the category, i.e. the kind of diff.
    """
    qc1 = ssd.qualify_code_points(str1)
    qc2 = ssd.qualify_code_points(str2)
    diffs = my_diffs.get(qc1, qc2)
    named_diffs = tuple(map(_get_unicode_names_for_diff, diffs))
    if _letters_differ(str1, str2):
        return _get_dide_incl_letter_changes(str1, str2, named_diffs)
    return ssd.simplify_simple_diffs(named_diffs)


def get2(mlist_a, mlist_b):
    """
    If possible, get a human-friendly description of the diffs
    between mlist1 & mlist2. (mlist: maybe a list, i.e. a list or None)
    """
    rstra = _get_refinable_str(mlist_a)
    rstrb = _get_refinable_str(mlist_b)
    return rstra and rstrb and get1(rstra, rstrb)


def _letters_differ(str1, str2):
    lm1 = hlw.letters_and_maqafs(str1)
    lm2 = hlw.letters_and_maqafs(str2)
    return lm1 != lm2


def _get_dide_incl_letter_changes(_str1, _str2, named_diffs):
    return str(named_diffs), "deep diff"


def _get_refinable_str(mlist):
    if mlist is None:
        return None
    assert isinstance(mlist, list)
    if not len(mlist) == 1:
        return None
    if not isinstance(mlist[0], str):
        return None
    inter = set(_VOWEL_POINTS).intersection(mlist[0])
    if len(inter) == 0:
        return None
    return mlist[0]


def _get_unicode_names_for_diff(diff):
    assert len(diff) == 2  # an "A" side and a "B" side
    return tuple(map(_get_unicode_names_for_side, diff))


def _get_unicode_names_for_side(side):
    return side and tuple(map(_get_unicode_names_for_side_el, side))


def _get_unicode_names_for_side_el(side):
    letter = ssd.qcp_get(side, "letter")
    return ssd.qcp_make(
        legacy_names.legacy_name(ssd.qcp_get(side, "code_point")),
        letter and legacy_names.legacy_name(letter),
        ssd.qcp_get(side, "count"),
    )


_VOWEL_POINTS = (
    hpo.SHEVA,
    hpo.XSEGOL,
    hpo.XPATAX,
    hpo.XQAMATS,
    hpo.XIRIQ,
    hpo.TSERE,
    hpo.SEGOL_V,
    hpo.PATAX,
    hpo.QAMATS,
    hpo.QAMATS_Q,
    hpo.XOLAM,
    hpo.XOLAM_XFV,
    hpo.QUBUTS,
)
