import re
import mb_cmn.hebrew_letters as hl
import mb_cmn.hebrew_points as hpo
import mb_cmn.hebrew_punctuation as hpu
import phonetic_mam.core.fully_translate as ft
import phonetic_mam.core.distinguished as disting


def get_deeplat_from_cw_ydys(cw_ydys_h: str):
    # deeplat: deep Latin/Greek
    # cw_ydys_h: a string containing a chanted word in yDyS-H format
    # yDyS: Dagesh [distinctions]? Yes. Sheva [distinctions]? Yes.
    # (uses the U+05C8 and U+05C9 annotation points to make those distinctions)
    # yDyS-H: yDyS represented in the Hebrew Unicode block (as opposed to deeplat)
    #
    # The yDyS-H format makes those distinctions as follows:
    #     sheva meaning silent sheva (sheva nax)
    #     U+05C8 (see disting.SHEVA_NA) meaning vocal sheva (sheva na)
    #     dagesh on begadkefat meaning dagesh qal
    #     dagesh on vav meaning shuruq
    #     U+05C9 (see disting.DAGESH_XAZAQ) meaning dagesh xazaq
    #
    assert not re.search(_RE_NOT_HEBREW_OR_NU_GMAQ, cw_ydys_h)
    # assert only Hebrew, i.e. no non-Hebrew
    cw_deeplat = cw_ydys_h
    cw_deeplat = re.sub(_MULTI_UNI_PATT, _multi_uni_repl, cw_deeplat)
    cw_deeplat = cw_deeplat.translate(_TRANS_TABLE_OF_DEEPLAT_FROM_SINGLE_UNI)
    assert not re.search(hpo.RE_YES_HEBREW, cw_deeplat)  # assert no Hebrew
    return cw_deeplat


def get_deeplat_from_cw_ndns_h(cw_ndns_h: str):
    # deeplat: deep Latin/Greek
    # cw_ndns_h: a string containing a chanted word in nDnS-H format
    # nDnS: Dagesh [distinctions]? No. Sheva [distinctions]? No.
    # (ambiguous sheva and ambiguous dagesh)
    # nDnS-H: nDnS represented in the Hebrew Unicode block (as opposed to deeplat)
    assert not re.search(_RE_NOT_HEBREW_OR_NU_GMAQ, cw_ndns_h)  # assert only Hebrew-ish
    cw_deeplat = cw_ndns_h
    cw_deeplat = re.sub(_MULTI_UNI_PATT_NDNS, _multi_uni_repl_ndns, cw_deeplat)
    cw_deeplat = cw_deeplat.translate(_TRANS_TABLE_OF_DEEPLAT_FROM_SINGLE_UNI_NDNS)
    assert not re.search(hpo.RE_YES_HEBREW, cw_deeplat)  # assert only non-Hebrew
    return cw_deeplat


def get_atoms(deeplat_str):
    maqs = BLACK_MAQAF + GRAY_MAQAF
    parts = re.split(f"([{maqs}])", deeplat_str)
    atoms = parts[0::2]
    atom_seps = parts[1::2]
    assert len(atoms) == 1 + len(atom_seps)
    return atoms


def get_he_letters_back(udl):
    # return udl.translate(_TRANS_TABLE_TO_GET_HE_LETTERS_BACK)
    return ft.fully_translate(udl, _TRANS_DIC_TO_GET_HE_LETTERS_BACK)


def _multi_uni_repl(match):
    wmat = match.group()  # the whole match
    return _DIC_OF_DEEPLAT_FROM_MULTI_UNI[wmat]


def _multi_uni_repl_ndns(match):
    wmat = match.group()  # the whole match
    return _DIC_OF_DEEPLAT_FROM_MULTI_UNI_NDNS[wmat]


def _is_gem(multi_uni):
    return disting.DAGESH_XAZAQ in multi_uni


# Yes, we know about alphabetic presentation forms.
# We decided not to use them.
# For one thing, we want to represent some things not available as alphabetic presentation forms.
# Notably, we want to distinguish vav-dagesh from shuruq.
# We use what we call "deeplat" (deep Latin/Greek) representation instead.
_ALEF_1MAPIQ_U = hl.ALEF + hpo.DAGOMOSD
_HE_1MAPIQ_U = hl.HE + hpo.DAGOMOSD
_VAV_1DAGOSD_U = hl.VAV + hpo.DAGOMOSD
_TRUESHIN_0DAG_U = hl.SHIN + hpo.SHIND
_SIN_0DAG_U = hl.SHIN + hpo.SIND
#
ALEF_1MAPIQ = "Ɂ"  # U+0241: LATIN CAPITAL LETTER GLOTTAL STOP
ALEF_0MAPIQ_CONOML = "ɂ"  # U+0242: LATIN SMALL LETTER GLOTTAL STOP
ALEF_0MAPIQ_CON = "ʾ"  # U+02BE: MODIFIER LETTER RIGHT HALF RING
ALEF_0MAPIQ_ML = "α"  # U+03B1: GREEK SMALL LETTER ALPHA
# Usually we use Greek letters for ambiguous stuff but α is an exception to that.
BET_1DAG_AMB = "β"  # U+03B2: GREEK SMALL LETTER BETA
BET_1DAG_QAL = "B"
BET_1DAG_XAZAQ = "Ḃ"  # U+1E02: LATIN CAPITAL LETTER B WITH DOT ABOVE
BET_0DAG = "v"  # aka vet
GIMEL_1DAG_AMB = "γ"  # U+03B3: GREEK SMALL LETTER GAMMA
GIMEL_1DAG_QAL = "G"
GIMEL_1DAG_XAZAQ = "Ĝ"  # U+011C: LATIN CAPITAL LETTER G WITH CIRCUMFLEX
GIMEL_0DAG = "g"
DALET_1DAG_AMB = "δ"  # U+03B4: GREEK SMALL LETTER DELTA
DALET_1DAG_QAL = "D"
DALET_1DAG_XAZAQ = "Ď"  # U+010E: LATIN CAPITAL LETTER D WITH CARON
DALET_0DAG = "d"
HE_1MAPIQ = "H"
HE_0MAPIQ_CONOML = "h"  # CONOML: consonant or mater lectionis
HE_0MAPIQ_CON = "Ĥ"  # U+0124: LATIN CAPITAL LETTER H WITH CIRCUMFLEX
HE_0MAPIQ_ML = "ħ"  # U+0127: LATIN SMALL LETTER H WITH STROKE
# Below, "DAGOSD" means "dagesh or shuruq dot"
VAV_1DAGOSD = "ẃ"  # U+1E83: LATIN SMALL LETTER W WITH ACUTE
VAV_1DAG = "W"
VAV_0DAGOSD_CONOML = "w"
VAV_0DAGOSD_CON = "ŵ"  # U+0175: LATIN SMALL LETTER W WITH CIRCUMFLEX
# The vav ML below only appears in the alef-vav double ML
VAV_0DAGOSD_ML = "ẁ"  # U+1E81: LATIN SMALL LETTER W WITH GRAVE
VAV_XOLAM = "O"
SHURUQ = "U"
ZAYIN_1DAG = "Z"
ZAYIN_0DAG = "z"
# _XET_1DAG ...
XET_0DAG = "x"
TET_1DAG = "Θ"  # U+0398: GREEK CAPITAL LETTER THETA
# Usually we use Greek letters for ambiguous stuff but Θ is an exception to that.
TET_0DAG = "θ"  # U+03B8: GREEK SMALL LETTER THETA
# Usually we use Greek letters for ambiguous stuff but θ is an exception to that.
YOD_1DAG = "Y"
YOD_0DAG_CONOML = "y"
YOD_0DAG_CON = "Ŷ"  # U+0176: LATIN CAPITAL LETTER Y WITH CIRCUMFLEX
YOD_0DAG_ML = "ý"  # U+00FD: LATIN SMALL LETTER Y WITH ACUTE
YOD_0DAG_PART2_OF_DIPHTHONG = "ÿ"  # U+00FF: LATIN SMALL LETTER Y WITH DIAERESIS
KAF_1DAG_AMB = "κ"  # U+03BA: GREEK SMALL LETTER KAPPA
KAF_1DAG_QAL = "K"
KAF_1DAG_XAZAQ = "Ǩ"  # U+01E8: LATIN CAPITAL LETTER K WITH CARON
KAF_0DAG = "k"  # aka khaf
LAMED_1DAG = "L"
LAMED_0DAG = "l"
MEM_1DAG = "M"
MEM_0DAG = "m"
NUN_1DAG = "N"
NUN_0DAG = "n"
SAMEKH_1DAG = "S"
SAMEKH_0DAG = "s"
# _AYIN_1DAG ...
AYIN_0DAG = "ʕ"  # U+0295: LATIN LETTER PHARYNGEAL VOICED FRICATIVE
PE_1DAG_AMB = "π"  # U+03C0: GREEK SMALL LETTER PI
PE_1DAG_QAL = "P"
PE_1DAG_XAZAQ = "Ṗ"  # U+1E56: LATIN CAPITAL LETTER P WITH DOT ABOVE
PE_0DAG = "f"  # aka fe
TSADI_1DAG = "Ц"  # U+0426: CYRILLIC CAPITAL LETTER TSE
TSADI_0DAG = "ц"  # U+0446: CYRILLIC SMALL LETTER TSE
QOF_1DAG = "Q"
QOF_0DAG = "q"
RESH_1DAG = "R"
RESH_0DAG = "r"
TRUESHIN_1DAG = "Š"  # U+0160: LATIN CAPITAL LETTER S WITH CARON
TRUESHIN_0DAG = "š"  # U+0161: LATIN SMALL LETTER S WITH CARON
SIN_1DAG = "Ś"  # U+015A: LATIN CAPITAL LETTER S WITH ACUTE
SIN_0DAG = "ś"  # U+015B: LATIN SMALL LETTER S WITH ACUTE
TAV_1DAG_AMB = "τ"  # U+03C4: GREEK SMALL LETTER TAU
TAV_1DAG_QAL = "T"
TAV_1DAG_XAZAQ = "Ť"  # U+0164: LATIN CAPITAL LETTER T WITH CARON
TAV_0DAG = "t"
FKAF_1DAG_AMB = "Κ"  # U+039A: GREEK CAPITAL LETTER KAPPA
FKAF_1DAG_QAL = "Ⓚ"  # U+24C0: CIRCLED LATIN CAPITAL LETTER K
FKAF_1DAG_XAZAQ = "Ḱ"  # U+1E30: LATIN CAPITAL LETTER K WITH ACUTE
FKAF_0DAG = "ⓚ"  # U+24DA: CIRCLED LATIN SMALL LETTER K
# above is aka final khaf
# _FMEM_1DAG ...
FMEM_0DAG = "ⓜ"  # U+24DC: CIRCLED LATIN SMALL LETTER M
# _FNUN_1DAG ...
FNUN_0DAG = "ⓝ"  # U+24DD: CIRCLED LATIN SMALL LETTER N
FPE_1DAG_AMB = "Π"  # U+03A0: GREEK CAPITAL LETTER PI
FPE_1DAG_QAL = "Ⓟ"  # U+24C5: CIRCLED LATIN CAPITAL LETTER P
FPE_0DAG = "ⓕ"  # U+24D5: CIRCLED LATIN SMALL LETTER F
# above is aka final fe
# _FTSADI_1DAG ...
FTSADI_0DAG = "ⓩ"  # U+24E9: CIRCLED LATIN SMALL LETTER Z
#
BLACK_MAQAF = "-"
GRAY_MAQAF = "˜"  # U+02DC: SMALL TILDE
_RE_NOT_HEBREW_OR_NU_GMAQ = f"[^{hpo.RECC_HEBR}{hpu.NU_GMAQ}]"
#
SHEVA_NA = "ə"  # U+0259: LATIN SMALL LETTER SCHWA
SHEVA_NAX = ":"
SHEVA_AMB = ";"
VARIKA_WITH_GENERIC_SHEVA = "^"
VARIKA_WITH_VOCAL_SHEVA = "Ə"
# U+018F: LATIN CAPITAL LETTER SCHWA
XSEGOL = "e"
XPATAX = "a"
XQAMATS = "𝒶"  # U+1D4B6: MATHEMATICAL SCRIPT SMALL A
XIRIQ_Q = "i"
TSERE = "ë"  # U+00EB: LATIN SMALL LETTER E WITH DIAERESIS
SEGOL_V = "E"
PATAX = "A"
QAMATS_G = "𝒜"  # U+1D49C: MATHEMATICAL SCRIPT CAPITAL A
QAMATS_Q = "ℴ"  #  U+2134: SCRIPT SMALL O
XOLAM_HASER = "o"
QUBUTS = "u"
#
XIRIQ_G = "ì"  # U+00EC: LATIN SMALL LETTER I WITH GRAVE
SHURUQ_PART1_OF_YOD_DIPHTHONG = "Ù"  # U+00D9: LATIN CAPITAL LETTER U WITH GRAVE
VAV_XOLAM_PART1_OF_YOD_DIPHTHONG = "Ò"  # U+00D2: LATIN CAPITAL LETTER O WITH GRAVE
#
# FPP: furtive patax pair
FPP_PATAX_MAPIQ_HE = "ḣ"  # U+1E23: LATIN SMALL LETTER H WITH DOT ABOVE
FPP_PATAX_XET = "ẋ"  # U+1E8B: LATIN SMALL LETTER X WITH DOT ABOVE
FPP_PATAX_AYIN = "_"
#
ALEF_SHURUQ_VOWEL = "Ú"  # U+00DA: LATIN CAPITAL LETTER U WITH ACUTE
#
_PAIRS_OF_MULTI_UNI_AND_DEEPLAT = [
    (_ALEF_1MAPIQ_U, ALEF_1MAPIQ),
    (_HE_1MAPIQ_U, HE_1MAPIQ),
    #
    (hl.BET + disting.DAGESH_XAZAQ, BET_1DAG_XAZAQ),
    (hl.GIMEL + disting.DAGESH_XAZAQ, GIMEL_1DAG_XAZAQ),
    (hl.DALET + disting.DAGESH_XAZAQ, DALET_1DAG_XAZAQ),
    (hl.KAF + disting.DAGESH_XAZAQ, KAF_1DAG_XAZAQ),
    (hl.PE + disting.DAGESH_XAZAQ, PE_1DAG_XAZAQ),
    (hl.TAV + disting.DAGESH_XAZAQ, TAV_1DAG_XAZAQ),
    (hl.FKAF + disting.DAGESH_XAZAQ, FKAF_1DAG_XAZAQ),
    #
    (hl.VAV + disting.DAGESH_XAZAQ, VAV_1DAG),
    (hl.ZAYIN + disting.DAGESH_XAZAQ, ZAYIN_1DAG),
    (hl.TET + disting.DAGESH_XAZAQ, TET_1DAG),
    (hl.YOD + disting.DAGESH_XAZAQ, YOD_1DAG),
    (hl.LAMED + disting.DAGESH_XAZAQ, LAMED_1DAG),
    (hl.MEM + disting.DAGESH_XAZAQ, MEM_1DAG),
    (hl.NUN + disting.DAGESH_XAZAQ, NUN_1DAG),
    (hl.SAMEKH + disting.DAGESH_XAZAQ, SAMEKH_1DAG),
    (hl.TSADI + disting.DAGESH_XAZAQ, TSADI_1DAG),
    (hl.QOF + disting.DAGESH_XAZAQ, QOF_1DAG),
    (hl.RESH + disting.DAGESH_XAZAQ, RESH_1DAG),
    (_TRUESHIN_0DAG_U + disting.DAGESH_XAZAQ, TRUESHIN_1DAG),
    (_SIN_0DAG_U + disting.DAGESH_XAZAQ, SIN_1DAG),
    #
    (hl.BET + hpo.DAGOMOSD, BET_1DAG_QAL),
    (hl.GIMEL + hpo.DAGOMOSD, GIMEL_1DAG_QAL),
    (hl.DALET + hpo.DAGOMOSD, DALET_1DAG_QAL),
    (hl.KAF + hpo.DAGOMOSD, KAF_1DAG_QAL),
    (hl.PE + hpo.DAGOMOSD, PE_1DAG_QAL),
    (hl.TAV + hpo.DAGOMOSD, TAV_1DAG_QAL),
    (hl.FKAF + hpo.DAGOMOSD, FKAF_1DAG_QAL),
    (hl.FPE + hpo.DAGOMOSD, FPE_1DAG_QAL),
    #
    (_TRUESHIN_0DAG_U, TRUESHIN_0DAG),
    (_SIN_0DAG_U, SIN_0DAG),
    #
    (hl.VAV + hpo.XOLAM, VAV_XOLAM),
    (_VAV_1DAGOSD_U, SHURUQ),
    (hpo.SHEVA + hpo.VARIKA, VARIKA_WITH_GENERIC_SHEVA),
    (disting.SHEVA_NA + hpo.VARIKA, VARIKA_WITH_VOCAL_SHEVA),
    (disting.SHEVA_NA, SHEVA_NA),
]
#
_PAIRS_OF_MULTI_UNI_AND_DEEPLAT_NDNS = [
    (_ALEF_1MAPIQ_U, ALEF_1MAPIQ),
    (_HE_1MAPIQ_U, HE_1MAPIQ),
    #
    (hl.BET + hpo.DAGOMOSD, BET_1DAG_AMB),
    (hl.GIMEL + hpo.DAGOMOSD, GIMEL_1DAG_AMB),
    (hl.DALET + hpo.DAGOMOSD, DALET_1DAG_AMB),
    (hl.KAF + hpo.DAGOMOSD, KAF_1DAG_AMB),
    (hl.PE + hpo.DAGOMOSD, PE_1DAG_AMB),
    (hl.TAV + hpo.DAGOMOSD, TAV_1DAG_AMB),
    (hl.FKAF + hpo.DAGOMOSD, FKAF_1DAG_AMB),
    (hl.FPE + hpo.DAGOMOSD, FPE_1DAG_AMB),
    #
    (hl.ZAYIN + hpo.DAGOMOSD, ZAYIN_1DAG),
    (hl.TET + hpo.DAGOMOSD, TET_1DAG),
    (hl.YOD + hpo.DAGOMOSD, YOD_1DAG),
    (hl.LAMED + hpo.DAGOMOSD, LAMED_1DAG),
    (hl.MEM + hpo.DAGOMOSD, MEM_1DAG),
    (hl.NUN + hpo.DAGOMOSD, NUN_1DAG),
    (hl.SAMEKH + hpo.DAGOMOSD, SAMEKH_1DAG),
    (hl.TSADI + hpo.DAGOMOSD, TSADI_1DAG),
    (hl.QOF + hpo.DAGOMOSD, QOF_1DAG),
    (hl.RESH + hpo.DAGOMOSD, RESH_1DAG),
    (_TRUESHIN_0DAG_U + hpo.DAGOMOSD, TRUESHIN_1DAG),
    (_SIN_0DAG_U + hpo.DAGOMOSD, SIN_1DAG),
    #
    (_TRUESHIN_0DAG_U, TRUESHIN_0DAG),
    (_SIN_0DAG_U, SIN_0DAG),
    #
    (hl.VAV + hpo.XOLAM, VAV_XOLAM),
    (_VAV_1DAGOSD_U, VAV_1DAGOSD),
]
_PAIRS_OF_SINGLE_UNI_AND_DEEPLAT = [
    (hpu.MAQ, BLACK_MAQAF),
    (hpu.NU_GMAQ, GRAY_MAQAF),
    #
    (hl.ALEF, ALEF_0MAPIQ_CONOML),
    (hl.BET, BET_0DAG),
    (hl.GIMEL, GIMEL_0DAG),
    (hl.DALET, DALET_0DAG),
    (hl.HE, HE_0MAPIQ_CONOML),
    (hl.VAV, VAV_0DAGOSD_CONOML),
    (hl.ZAYIN, ZAYIN_0DAG),
    (hl.XET, XET_0DAG),
    (hl.TET, TET_0DAG),
    (hl.YOD, YOD_0DAG_CONOML),
    (hl.KAF, KAF_0DAG),
    (hl.LAMED, LAMED_0DAG),
    (hl.MEM, MEM_0DAG),
    (hl.NUN, NUN_0DAG),
    (hl.SAMEKH, SAMEKH_0DAG),
    (hl.AYIN, AYIN_0DAG),
    (hl.PE, PE_0DAG),
    (hl.TSADI, TSADI_0DAG),
    (hl.QOF, QOF_0DAG),
    (hl.RESH, RESH_0DAG),
    # shin and sin handled elsewhere
    (hl.TAV, TAV_0DAG),
    #
    (hl.FKAF, FKAF_0DAG),
    (hl.FMEM, FMEM_0DAG),
    (hl.FNUN, FNUN_0DAG),
    (hl.FPE, FPE_0DAG),
    (hl.FTSADI, FTSADI_0DAG),
    #
    (hpo.SHEVA, SHEVA_NAX),
    (hpo.XSEGOL, XSEGOL),
    (hpo.XPATAX, XPATAX),
    (hpo.XQAMATS, XQAMATS),
    (hpo.XIRIQ, XIRIQ_Q),  # we assume all are qatan until later
    (hpo.TSERE, TSERE),
    (hpo.SEGOL_V, SEGOL_V),
    (hpo.PATAX, PATAX),
    (hpo.QAMATS, QAMATS_G),
    (hpo.QAMATS_Q, QAMATS_Q),
    (hpo.XOLAM_XFV, XOLAM_HASER),
    (hpo.XOLAM, XOLAM_HASER),
    (hpo.QUBUTS, QUBUTS),
    #
    (hpo.VARIKA, None),
]
_PAIRS_OF_SINGLE_UNI_AND_DEEPLAT_NDNS = [
    *_PAIRS_OF_SINGLE_UNI_AND_DEEPLAT,
    (hpo.SHEVA, SHEVA_AMB),
]
_DIC_OF_DEEPLAT_FROM_MULTI_UNI = dict(_PAIRS_OF_MULTI_UNI_AND_DEEPLAT)
_DIC_OF_DEEPLAT_FROM_MULTI_UNI_NDNS = dict(_PAIRS_OF_MULTI_UNI_AND_DEEPLAT_NDNS)
_DIC_OF_DEEPLAT_FROM_SINGLE_UNI = dict(_PAIRS_OF_SINGLE_UNI_AND_DEEPLAT)
_DIC_OF_DEEPLAT_FROM_SINGLE_UNI_NDNS = dict(_PAIRS_OF_SINGLE_UNI_AND_DEEPLAT_NDNS)
_TRANS_TABLE_OF_DEEPLAT_FROM_SINGLE_UNI = str.maketrans(_DIC_OF_DEEPLAT_FROM_SINGLE_UNI)
_TRANS_TABLE_OF_DEEPLAT_FROM_SINGLE_UNI_NDNS = str.maketrans(
    _DIC_OF_DEEPLAT_FROM_SINGLE_UNI_NDNS
)
_MULTI_UNIS = [pair[0] for pair in _PAIRS_OF_MULTI_UNI_AND_DEEPLAT]
_MULTI_UNIS_NDNS = [pair[0] for pair in _PAIRS_OF_MULTI_UNI_AND_DEEPLAT_NDNS]
_MULTI_UNI_PATT = "(" + "|".join(_MULTI_UNIS) + ")"
_MULTI_UNI_PATT_NDNS = "(" + "|".join(_MULTI_UNIS_NDNS) + ")"
GEMINATES = {pair[1] for pair in _PAIRS_OF_MULTI_UNI_AND_DEEPLAT if _is_gem(pair[0])}
_TRANS_DIC_TO_GET_HE_LETTERS_BACK = {
    ALEF_0MAPIQ_CON: hl.ALEF,
    ALEF_0MAPIQ_ML: hl.ALEF,
    ALEF_1MAPIQ: hl.ALEF,
    BET_0DAG: hl.BET,
    BET_1DAG_QAL: hl.BET,
    BET_1DAG_XAZAQ: hl.BET,
    GIMEL_0DAG: hl.GIMEL,
    GIMEL_1DAG_QAL: hl.GIMEL,
    GIMEL_1DAG_XAZAQ: hl.GIMEL,
    DALET_0DAG: hl.DALET,
    DALET_1DAG_QAL: hl.DALET,
    DALET_1DAG_XAZAQ: hl.DALET,
    HE_0MAPIQ_CON: hl.HE,
    HE_0MAPIQ_ML: hl.HE,
    HE_1MAPIQ: hl.HE,
    VAV_0DAGOSD_CON: hl.VAV,
    VAV_0DAGOSD_ML: hl.VAV,
    VAV_1DAG: hl.VAV,
    VAV_XOLAM: hl.VAV,
    SHURUQ: hl.VAV,
    ZAYIN_0DAG: hl.ZAYIN,
    ZAYIN_1DAG: hl.ZAYIN,
    XET_0DAG: hl.XET,
    TET_0DAG: hl.TET,
    TET_1DAG: hl.TET,
    YOD_0DAG_CON: hl.YOD,
    YOD_0DAG_ML: hl.YOD,
    YOD_0DAG_PART2_OF_DIPHTHONG: hl.YOD,
    YOD_1DAG: hl.YOD,
    KAF_0DAG: hl.KAF,
    KAF_1DAG_QAL: hl.KAF,
    KAF_1DAG_XAZAQ: hl.KAF,
    LAMED_0DAG: hl.LAMED,
    LAMED_1DAG: hl.LAMED,
    MEM_0DAG: hl.MEM,
    MEM_1DAG: hl.MEM,
    NUN_0DAG: hl.NUN,
    NUN_1DAG: hl.NUN,
    SAMEKH_0DAG: hl.SAMEKH,
    SAMEKH_1DAG: hl.SAMEKH,
    AYIN_0DAG: hl.AYIN,
    PE_0DAG: hl.PE,
    PE_1DAG_QAL: hl.PE,
    PE_1DAG_XAZAQ: hl.PE,
    TSADI_0DAG: hl.TSADI,
    TSADI_1DAG: hl.TSADI,
    QOF_0DAG: hl.QOF,
    QOF_1DAG: hl.QOF,
    RESH_0DAG: hl.RESH,
    RESH_1DAG: hl.RESH,
    TRUESHIN_0DAG: hl.SHIN,
    TRUESHIN_1DAG: hl.SHIN,
    SIN_0DAG: hl.SHIN,
    SIN_1DAG: hl.SHIN,
    TAV_0DAG: hl.TAV,
    TAV_1DAG_QAL: hl.TAV,
    TAV_1DAG_XAZAQ: hl.TAV,
    #
    FKAF_0DAG: hl.FKAF,
    FKAF_1DAG_QAL: hl.FKAF,
    FKAF_1DAG_XAZAQ: hl.FKAF,
    FMEM_0DAG: hl.FMEM,
    FNUN_0DAG: hl.FNUN,
    FPE_0DAG: hl.FPE,
    FPE_1DAG_QAL: hl.FPE,
    FTSADI_0DAG: hl.FTSADI,
    #
    SHEVA_NA: "",
    SHEVA_NAX: "",
    VARIKA_WITH_GENERIC_SHEVA: "",
    VARIKA_WITH_VOCAL_SHEVA: "",
    XSEGOL: "",
    XPATAX: "",
    XQAMATS: "",
    XIRIQ_Q: "",
    TSERE: "",
    SEGOL_V: "",
    PATAX: "",
    QAMATS_G: "",
    QAMATS_Q: "",
    XOLAM_HASER: "",
    QUBUTS: "",
    #
    XIRIQ_G: "",
    SHURUQ_PART1_OF_YOD_DIPHTHONG: hl.VAV,
    VAV_XOLAM_PART1_OF_YOD_DIPHTHONG: hl.VAV,
    #
    FPP_PATAX_MAPIQ_HE: hl.HE,
    FPP_PATAX_XET: hl.XET,
    FPP_PATAX_AYIN: hl.AYIN,
    #
    ALEF_SHURUQ_VOWEL: hl.ALEF + hl.VAV,
}
# _ALL_PAIRS = (
#     _PAIRS_OF_MULTI_UNI_AND_DEEPLAT +
#     _PAIRS_OF_SINGLE_UNI_AND_DEEPLAT
# )
# _TRANS_DIC_TO_GET_HE_LETTERS_BACK = {
#     deeplat: hebrew for hebrew, deeplat in _ALL_PAIRS
# }
_TRANS_TABLE_TO_GET_HE_LETTERS_BACK = str.maketrans(_TRANS_DIC_TO_GET_HE_LETTERS_BACK)
