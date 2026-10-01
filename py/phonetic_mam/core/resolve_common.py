import re
import phonetic_mam.core.deep_latin as deeplat
import phonetic_mam.core.udl_char_classes as cc
import phonetic_mam.core.syllables as syl


def yco_nco_sub(patts_and_repls, adl_str):
    # yco: Consonant? Yes.
    # nco: Consonant? No. (A vowel or a mater lectionis.)
    _ambiguous, yco_patt, nco_patt, yco_repl, nco_repl = patts_and_repls
    adl_str = re.sub(yco_patt, yco_repl, adl_str)
    adl_str = re.sub(nco_patt, nco_repl, adl_str)
    # assert ambiguous not in adl_str
    return adl_str


def patts_and_repls_1(amb_unambyco_unambnco):
    ambiguous, unambyco, unambnco = amb_unambyco_unambnco
    yco_patt = ambiguous + _regexp_group(_RE_CLS_VOWEL_OR_STOP)
    nco_patt = ambiguous + "($|" + _RE_CLS_CONOML_INCL_AMB + ")"
    yco_repl = unambyco + r"\1"
    nco_repl = unambnco + r"\1"
    return ambiguous, yco_patt, nco_patt, yco_repl, nco_repl


def patts_and_repls_2(amb_unambyco_unambnco):
    ambiguous, unambyco, unambnco = amb_unambyco_unambnco
    yco_patt = ambiguous + "($|" + _RE_CLS_VOWEL_OR_STOP + ")"
    nco_patt = ambiguous + _regexp_group(_RE_CLS_CONOML_INCL_AMB)
    yco_repl = unambyco + r"\1"
    nco_repl = unambnco + r"\1"
    return ambiguous, yco_patt, nco_patt, yco_repl, nco_repl


def misc_repl_fun(match):
    return _MISC_REPL_STR[match.group()]


def find_concerns_in_atom(udl_str):
    if not udl_str:
        return  # XXX remove this when no longer needed
    if not re.fullmatch(_PATT_OF_A_SUCCESSFULLY_RESOLVED_ATOM, udl_str):
        return f"Atom {udl_str} does not match the pattern of a successfully-resolved atom."
    if not re.fullmatch(_PATT_OF_AN_ATOM_OF_SYLLABLES, udl_str):
        return f"Atom {udl_str} does not match the pattern of an atom of syllables."
    return None


def _regexp_group(inside):
    return f"({inside})"


def _my_trans(string, trans_dic):
    trans_table = str.maketrans(trans_dic)
    return string.translate(trans_table)


def _regexp_class(charseq):
    join_result = "".join(charseq)
    return f"[{join_result}]"


_AMB_ML = {
    deeplat.ALEF_0MAPIQ_CONOML,
    deeplat.HE_0MAPIQ_CONOML,
    deeplat.YOD_0DAG_CONOML,
    deeplat.VAV_0DAGOSD_CONOML,
}
BGDKPT_AMB_TO_QX = {
    deeplat.BET_1DAG_AMB: (deeplat.BET_1DAG_QAL, deeplat.BET_1DAG_XAZAQ),
    deeplat.GIMEL_1DAG_AMB: (deeplat.GIMEL_1DAG_QAL, deeplat.GIMEL_1DAG_XAZAQ),
    deeplat.DALET_1DAG_AMB: (deeplat.DALET_1DAG_QAL, deeplat.DALET_1DAG_XAZAQ),
    deeplat.KAF_1DAG_AMB: (deeplat.KAF_1DAG_QAL, deeplat.KAF_1DAG_XAZAQ),
    deeplat.PE_1DAG_AMB: (deeplat.PE_1DAG_QAL, deeplat.PE_1DAG_XAZAQ),
    deeplat.TAV_1DAG_AMB: (deeplat.TAV_1DAG_QAL, deeplat.TAV_1DAG_XAZAQ),
    deeplat.FKAF_1DAG_AMB: (deeplat.FKAF_1DAG_QAL, deeplat.FKAF_1DAG_XAZAQ),
}
BGDKPT_AMB = list(BGDKPT_AMB_TO_QX.keys())
CON_A_OKAY = list(sorted(cc.UNAMB_CONSONANTS)) + BGDKPT_AMB
# CON_A_OKAY: known to be consonants, but some ambiguity within that is okay.
# In particular, begad-kefat letters don't need their dagesh quality (qal vs. xazaq)
# determined.
_CONOML_INCL_AMB = [
    *CON_A_OKAY,
    *cc.UNAMB_MLS,
    *_AMB_ML,
]
_VOWEL_OR_STOP = *cc.UNAMB_VOWELS, deeplat.SHEVA_NAX, deeplat.SHEVA_AMB
_RE_CLS_CONOML_INCL_AMB = _regexp_class(_CONOML_INCL_AMB)
_RE_CLS_VOWEL_OR_STOP = _regexp_class(_VOWEL_OR_STOP)
ALEF_ML_SHURUQ_PATT = (
    _regexp_group(CON_A_OKAY) + deeplat.ALEF_0MAPIQ_CONOML + deeplat.SHURUQ
)
ALEF_ML_SHURUQ_REPL = r"\1" + deeplat.ALEF_SHURUQ_VOWEL
#
_ALEF_0MAPIQ_AUU = (
    deeplat.ALEF_0MAPIQ_CONOML,
    deeplat.ALEF_0MAPIQ_CON,
    deeplat.ALEF_0MAPIQ_ML,
)
_HE_0MAPIQ_AUU = deeplat.HE_0MAPIQ_CONOML, deeplat.HE_0MAPIQ_CON, deeplat.HE_0MAPIQ_ML
_YOD_0DAG_AUU = deeplat.YOD_0DAG_CONOML, deeplat.YOD_0DAG_CON, deeplat.YOD_0DAG_ML
_VAV_0DAGOSD_AUU = (
    deeplat.VAV_0DAGOSD_CONOML,
    deeplat.VAV_0DAGOSD_CON,
    deeplat.VAV_0DAGOSD_ML,
)
#
ALEF_0MAPIQ_PATTS_AND_REPLS = patts_and_repls_1(_ALEF_0MAPIQ_AUU)
HE_0MAPIQ_PATTS_AND_REPLS = patts_and_repls_1(_HE_0MAPIQ_AUU)
YOD_0DAG_PATTS_AND_REPLS = patts_and_repls_1(_YOD_0DAG_AUU)
VAV_0DAGOSD_PATTS_AND_REPLS = patts_and_repls_2(_VAV_0DAGOSD_AUU)
#
# _IAY below is for Ezra 4:12 וּבִֽאישְׁתָּא֙
_IY = deeplat.XIRIQ_Q + deeplat.YOD_0DAG_ML
_IAY = deeplat.XIRIQ_Q + deeplat.ALEF_0MAPIQ_ML + deeplat.YOD_0DAG_ML
_DT_QPUO = deeplat.QAMATS_G + deeplat.PATAX + deeplat.SHURUQ + deeplat.VAV_XOLAM
_DT_DTHONG = f"[{_DT_QPUO}]" + deeplat.YOD_0DAG_ML + "$"
_FP_HX3 = deeplat.HE_1MAPIQ + deeplat.XET_0DAG + deeplat.AYIN_0DAG
_FP_FURTIVE_PATAX = f"[{_FP_HX3}]" + deeplat.PATAX + "$"
_ALTERNATION = "|".join([_IY, _IAY, _DT_DTHONG, _FP_FURTIVE_PATAX])
MISC_PATT = f"(?:{_ALTERNATION})"
#
_DT_QY = deeplat.QAMATS_G + deeplat.YOD_0DAG_ML
_DT_PY = deeplat.PATAX + deeplat.YOD_0DAG_ML
_DT_UY = deeplat.SHURUQ + deeplat.YOD_0DAG_ML
_DT_OY = deeplat.VAV_XOLAM + deeplat.YOD_0DAG_ML
_DT_Y0_P2 = deeplat.YOD_0DAG_PART2_OF_DIPHTHONG
#
_FP_HA = deeplat.HE_1MAPIQ + deeplat.PATAX
_FP_XA = deeplat.XET_0DAG + deeplat.PATAX
_FP_3A = deeplat.AYIN_0DAG + deeplat.PATAX
_MISC_REPL_STR = {
    _IY: deeplat.XIRIQ_G + deeplat.YOD_0DAG_ML,
    _IAY: deeplat.XIRIQ_G + deeplat.ALEF_0MAPIQ_ML + deeplat.YOD_0DAG_ML,
    #
    _DT_QY: deeplat.QAMATS_G + _DT_Y0_P2,
    _DT_PY: deeplat.PATAX + _DT_Y0_P2,
    _DT_UY: deeplat.SHURUQ_PART1_OF_YOD_DIPHTHONG + _DT_Y0_P2,
    _DT_OY: deeplat.VAV_XOLAM_PART1_OF_YOD_DIPHTHONG + _DT_Y0_P2,
    #
    _FP_HA: deeplat.FPP_PATAX_MAPIQ_HE,
    _FP_XA: deeplat.FPP_PATAX_XET,
    _FP_3A: deeplat.FPP_PATAX_AYIN,
}
# cc.UNAMB_VOWELS are vowels
# deeplat.SHEVA_NAX is a stop
# deeplat.SHEVA_AMB is a vowel or a stop
# therefore everything in this list is a vowel, a stop, or a vowel-or-a-stop
#
_PATT_OF_A_SUCCESSFULLY_RESOLVED_ATOM = _my_trans(
    r"U?(cvm*)+(c|[ḣẋ_])?",
    {
        "U": deeplat.SHURUQ,
        "c": cc.RE_CLS_UNAMB_CONSONANT,
        "v": _RE_CLS_VOWEL_OR_STOP,
        "m": cc.RE_CLS_UNAMB_ML,
        "ḣ": deeplat.FPP_PATAX_MAPIQ_HE,
        "ẋ": deeplat.FPP_PATAX_XET,
        "_": deeplat.FPP_PATAX_AYIN,
    },
)
_PATT_OF_AN_ATOM_OF_SYLLABLES = "(?:" + syl.PATT_OF_A_SYLLABLE + ")+"
