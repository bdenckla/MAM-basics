import re

import phonetic_mam.core.deut_32_6_haladonai as haladonai
import phonetic_mam.core.distinguished as disting
import mb_cmn.hebrew_letters as hl
import mb_cmn.hebrew_points as hpo
import mb_cmn.hebrew_accents as ha


def get_qere_from_implicit_kq(word):
    """
    Convert from implicit ketiv/qere to explicit ketiv/qere,
    for words such as the following:
        yerushalayim and related,
        yerushalaymah and related,
        adonai spelled YHVH and related,
        elohim spelled YHVH and related,
        hi spelled הוא,
        yissakhar and other "weird" names, and
        "ha ladonai" (a "word" with a space in it!)
    """
    if remapped_word := _WHOLE_WORD_REMAPS.get(word):
        word = remapped_word
    for patt_n_repl in _PATT_REPL_PAIRS:
        if qere := _get_qere_for_one_patt(word, patt_n_repl):
            return qere
    return word


def _yru_repl_fun(match):
    mgd = match.groupdict()
    return mgd["l_PQ_macc"] + hl.YOD + mgd["iM_or_eMaH"]


def _elohim_repl_fun(match):
    mgd = match.groupdict()
    return (
        hl.ALEF
        + mgd["esy_points_after_yod"]
        + hl.LAMED
        + hpo.XOLAM
        + hl.HE
        + hpo.XIRIQ
        + mgd["esy_points_after_xiriq"]
        + hl.YOD
        + hl.FMEM
    )


def _adonai_repl_fun(match):
    mgd = match.groupdict()
    adonai = (
        hl.ALEF
        + mgd["asy_points_after_yod"]
        + hl.DALET
        + hpo.XOLAM
        + mgd["asy_points_after_xolam"]
        + hl.NUN
        + hpo.QAMATS
        + mgd["asy_points_after_qamats"]
        + hl.YOD
    )
    adonai = adonai.replace(disting.SHEVA_NA, hpo.XPATAX)
    adonai = adonai.replace(hpo.SHEVA, hpo.XPATAX)
    return adonai


def _named_group(name, group_body):
    return f"(?P<{name}>{group_body})"


def _named_nonlet(name):
    return _named_group(name, _NONLET)


def _get_qere_for_one_patt(word, patt_n_repl):
    pattern, repl = patt_n_repl
    new_word, nmatches = re.subn(pattern, repl, word)
    if nmatches:
        assert nmatches == 1
        return new_word
    return None


def _named_shorthand_group(name, shorthand):
    longhand = shorthand.translate(_SHORTHAND_TABLE)
    return f"(?P<{name}>{longhand})"


def _maybe_dx(patt):  # maybe dagesh xazaq
    return patt.replace(
        hpo.DAGOMOSD,
        f"(?:{hpo.DAGOMOSD}|{disting.DAGESH_XAZAQ})",
    )


_SHORTHAND_TABLE = str.maketrans(
    {
        "l": hl.LAMED,
        "P": hpo.PATAX,
        "Q": hpo.QAMATS,
        "a": "[" + ha.ACCENTS_AND_MTG + "]",
        "i": hpo.XIRIQ,
        ":": hpo.SHEVA,
        "m": hl.MEM,
        "n": hl.FMEM,
        "h": hl.HE,
    }
)
_CGJ_RE = r"\u034f"
_YRUSHLM_OR_LMH = (
    _named_shorthand_group("l_PQ_macc", "l[PQ]a?")
    + _CGJ_RE
    + "?"
    + _named_shorthand_group("iM_or_eMaH", "in|:mQh")
)
#
# Explanation of the 3 lines above:
#
#    lamed, patax or qamats, 0 or 1 accents
#    0 or 1 CGJs
#    xiriq-final_mem or sheva-mem-qamats-he
_ATT = "א-ת"
_NONLET = f"[^{_ATT}]*"
# 0 to 1 points on yod (beyond the xiriq)
# 1 to 2 points on kaf
_YISSAKHAR = _maybe_dx("(יִ.?שָּׂ)" + "ש" + "(כ..?ר)")
_YISSAKHAR_REPL_STR = r"\1\2"
_YIRIYAH = _maybe_dx("(" + "יִרְאִיָּ" + ".?)" + "י" + "(ה)")
_YIRIYAH_REPL_STR = r"\1\2"
_UMEXIYAEL = _maybe_dx("(וּמְחִיָּ)" + "י" + "(אֵ֗ל)")
_UMEXIYAEL_REPL_STR = r"\1\2"
_HI_SPELLED_HU = "(הִ.?)" + "ו" + "(א)"
_HI_SPELLED_HU_REPL_STR = r"\1" + "י" + r"\2"
_ELOHIM_SPELLED_YHVH = (
    # י.?.?הֹוִ.?ה with some grouping
    # 0 to 2 points after yod (maybe a vowel, maybe an accent)
    # 0 to 1 points after vav + xiriq (maybe an accent)
    # esy: elohim spelled YHVH
    hl.YOD
    + _named_group("esy_points_after_yod", ".?.?")
    + hl.HE
    + hpo.XOLAM
    + hl.VAV
    + hpo.XIRIQ
    + _named_group("esy_points_after_xiriq", ".?")
    + hl.HE
)
_ADONAI_SPELLED_YHVH = (
    hl.YOD
    + _named_nonlet("asy_points_after_yod")
    + hl.HE
    + hpo.XOLAM
    + _named_nonlet("asy_points_after_xolam")
    + hl.VAV
    + hpo.QAMATS
    + _named_nonlet("asy_points_after_qamats")
    + hl.HE
)
_PATT_REPL_PAIRS = (
    (_YRUSHLM_OR_LMH, _yru_repl_fun),
    (_ELOHIM_SPELLED_YHVH, _elohim_repl_fun),
    (_ADONAI_SPELLED_YHVH, _adonai_repl_fun),
    (_YISSAKHAR, _YISSAKHAR_REPL_STR),
    (_YIRIYAH, _YIRIYAH_REPL_STR),
    (_UMEXIYAEL, _UMEXIYAEL_REPL_STR),
    (_HI_SPELLED_HU, _HI_SPELLED_HU_REPL_STR),
    #
)
_WHOLE_WORD_REMAPS = {
    haladonai.POINTED_KETIV_AS_STR: haladonai.POINTED_QERE,
}
