import re
from pycmn import uni_heb as uh
from pycmn import hebrew_punctuation as hpu
from pycmn import hebrew_points as hpo
from pycmn import hebrew_accents as ha
from pycmn import str_defs as sd


def massage_ctr_verse(ctr_verse_raw):
    out_1 = ctr_verse_raw
    for old, new in _CTR_REPLACES.items():
        assert new not in out_1, uh.join_shunnas(new)
        out_1 = out_1.replace(old, new)
    out_2 = re.sub(*_ZARQA_RELATED_SUB_ARGS, out_1)
    words = re.split(_SPLIT_PATT, out_2)
    return words


_ENDERS_TUP = "$", " ", hpu.PASOLEG
_ENDERS_STR = "|".join(_ENDERS_TUP)
_ZARQA_RELATED_SUB_ARGS = (ha.ZSH_OR_TSIT + f"({_ENDERS_STR})", ha.Z_OR_TSOR + r"\1")

_SPLITS_TUP = " ", hpu.MAQ, hpu.PASOLEG
_SPLITS_STR = "".join(_SPLITS_TUP)
_SPLIT_PATT = f"([{_SPLITS_STR}]+)"


_SHEVA_AND_XATAFS = hpo.SHEVA, hpo.XSEGOL, hpo.XPATAX, hpo.XQAMATS
_BELOW_VOWS = (
    *_SHEVA_AND_XATAFS,
    hpo.XIRIQ,
    hpo.TSERE,
    hpo.SEGOL_V,
    hpo.PATAX,
    hpo.QAMATS,
    hpo.QUBUTS,
)
_CTR_GER = {ha.GER + v: v + ha.GER_M for v in _BELOW_VOWS}
_CTR_TIP = {ha.TIP + v: v + ha.DEX for v in _BELOW_VOWS}
_CTR_YET = {v + ha.YET: v + ha.MAH for v in _BELOW_VOWS}
_CTR_REPLACES = {
    **_CTR_GER,
    **_CTR_TIP,
    **_CTR_YET,
    "\N{COLON}": hpu.SOPA,
    " \N{VERTICAL LINE}": hpu.PASOLEG,
    sd.ZWJ + hpo.XOLAM: hpo.XOLAM_XFV,
}
