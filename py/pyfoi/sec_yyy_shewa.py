import re
from pycmn import hebrew_accents as ha
from pycmn import hebrew_punctuation as hpu
from pycmn import hebrew_points as hpo
from pycmn import hebrew_letters as hl
from pycmn import uni_heb as uh
from pyfoi import regexp_helpers as rh


def shewa_feature(feature_for_main, cword: str):
    foi_path_for_main, foi_target_for_main = feature_for_main
    fpfm_lvl_1, fpfm_cantsys, *_fpfm_rest = foi_path_for_main
    match = re.search(_SHEWA_FEATURE_PATTERN[fpfm_lvl_1], cword)
    if not match:
        return None
    if ha.TEV in cword:
        return None
    magr1 = match.group(1)
    magr2 = match.group(2)
    magr1_f = _MAGR1_F.get(magr1) or uh.join_shunnas(magr1)  # 'f' for friendly
    addl = _additional_fpe(magr1, magr2)
    foi_path = _FP_LVL_1[fpfm_lvl_1], fpfm_cantsys, f"«{magr1_f}»", *addl
    return foi_path, foi_target_for_main


_MAGR1_F = {
    hl.HE + hpo.SHEVA: "gutt-:",
    hl.XET + hpo.SHEVA: "gutt-:",
}


def _additional_fpe(magr1: str, magr2: str):
    """Additional FOI path element"""
    if magr1 == hpo.SHEVA:
        match_simshewa = re.match(_NEXT_SIMSHEWA_PATTERN, magr2)
        if match_simshewa:
            return ("double shewa",)
        match_bgdkft_d = re.match(_NEXT_BGDKFT_D_PATTERN, magr2)
        if match_bgdkft_d:
            return ("bgdkft-dagesh",)
    return ()


_FULL_VOWELS_CC = r"\u05b4-\u05bb"  # CC: character class
_SHEWAS_CC = r"\u05b0-\u05b3"
_MTG_OR_VAR_CC = hpo.MTGOSLQ_RE + hpo.VARIKA_RE
_FV_OR_MAQ_CC = _FULL_VOWELS_CC + hpu.MAQ_RE + hpu.NU_GMAQ
_SHEWAS = rh.sqb(_SHEWAS_CC)
_MTG_OR_VAR = rh.sqb(_MTG_OR_VAR_CC)
_GUTT_SIMSHEWA = rh.GUTT + hpo.SHEVA_RE
_GFOO = rh.ncpar(f"{_GUTT_SIMSHEWA}|{_SHEWAS}")
_CAPI = f"{_GFOO}{_MTG_OR_VAR}*"  # capture group insides
_BGDKFT_D = r"[בגדכפת]" + hpo.DAGOMOSD_RE
_SHEWA_FEATURE_PATTERN_FOR_SEC_MERK = (
    ha.MER_RE + rh.ngs(rh.nsqb(_FV_OR_MAQ_CC)) + rh.par(_CAPI) + rh.par(".*")
)
_SHEWA_FEATURE_PATTERN_FOR_SEC_MISC = (
    ha.MAH_RE + rh.ngs(rh.nsqb(_FV_OR_MAQ_CC)) + rh.par(_CAPI) + rh.par(".*")
)
_SHEWA_FEATURE_PATTERN = {
    "sec-merk": _SHEWA_FEATURE_PATTERN_FOR_SEC_MERK,
    "sec-misc": _SHEWA_FEATURE_PATTERN_FOR_SEC_MISC,
}
_FP_LVL_1 = {
    "sec-merk": "sec-merk-shewa",
    "sec-misc": "sec-misc-shewa",
}
_NEXT_SIMSHEWA_PATTERN = rh.ngs(rh.nsqb(_FV_OR_MAQ_CC)) + _SHEWAS
_NEXT_BGDKFT_D_PATTERN = rh.ngs(rh.nsqb(_FV_OR_MAQ_CC)) + _BGDKFT_D
