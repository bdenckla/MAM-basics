"""
Exports 2 dicts:
   STR_TO_INT_DIC
   INT_TO_STR_DIC
"""

from itertools import product
from pycmn import hebrew_letters as hl

_HLYOD = hl.YOD
_HLKAF = hl.KAF
_HLLAMED = hl.LAMED
_HLMEM = hl.MEM
_HLNUN = hl.NUN
_HLSAMEKH = hl.SAMEKH
_HLAYIN = hl.AYIN
_HLPE = hl.PE
_HLTSADE = hl.TSADI
_HLQOF = hl.QOF

_HLALEF = hl.ALEF
_HLBET = hl.BET
_HLGIMEL = hl.GIMEL
_HLDALET = hl.DALET
_HLHE = hl.HE
_HLVAV = hl.VAV
_HLZAYIN = hl.ZAYIN
_HLHET = hl.XET
_HLTET = hl.TET

_HUNDREDS = "", _HLQOF
_TENS = (
    "",
    _HLYOD,
    _HLKAF,
    _HLLAMED,
    _HLMEM,
    _HLNUN,
    _HLSAMEKH,
    _HLAYIN,
    _HLPE,
    _HLTSADE,
)
_ONES = (
    "",
    _HLALEF,
    _HLBET,
    _HLGIMEL,
    _HLDALET,
    _HLHE,
    _HLVAV,
    _HLZAYIN,
    _HLHET,
    _HLTET,
)

_SACRED_REMAPS = {
    (_HLYOD + _HLHE): _HLTET + _HLVAV,
    (_HLYOD + _HLVAV): _HLTET + _HLZAYIN,
    (_HLQOF + _HLYOD + _HLHE): _HLQOF + _HLTET + _HLVAV,
    (_HLQOF + _HLYOD + _HLVAV): _HLQOF + _HLTET + _HLZAYIN,
}


def _gen_table():
    hto_triples = tuple(product(_HUNDREDS, _TENS, _ONES))
    strs = tuple("".join(t) for t in hto_triples)
    profane_strs = tuple(_SACRED_REMAPS.get(s, s) for s in strs)
    with_ints = tuple(enumerate(profane_strs))
    return with_ints[1:]  # [1:] removes (0, '')


_INT_STR_PAIRS = _gen_table()
# _STR_INT_PAIRS = map(reversed, _INT_STR_PAIRS)
_STR_INT_PAIRS = [(b, a) for a, b in _INT_STR_PAIRS]
# We do the flip "manually", i.e. we don't use "reversed",
# to make Pylance happy.
STR_TO_INT_DIC = dict(_STR_INT_PAIRS)
INT_TO_STR_DIC = dict(_INT_STR_PAIRS)
