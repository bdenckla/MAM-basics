import itertools
from pycmn import uni_heb as uh
from pycmn import hebrew_accents as ha
from pycmn import hebrew_points as hpo
from pycmn.my_utils import dk_map


def make(ell, vow=None, acc=None, special=None):
    if special:
        return ell or _EMPTY, vow or _EMPTY, acc or _EMPTY, special
    if acc:
        return ell or _EMPTY, vow or _EMPTY, acc
    if vow:
        return ell or _EMPTY, vow
    return (ell or _EMPTY,)


def makebl(base, layer_l):  # letter
    return _set_tuple_el(base, 0, layer_l)


def makebs(base, layer_s_as_dict):  # special
    return _set_tuple_el(base, 3, tuple(layer_s_as_dict.items()))


def layerl(char):  # letter
    return char[0]


def layerv(char):  # vowel
    return char[1] if len(char) > 1 else _EMPTY


def layera(char):  # accent
    return char[2] if len(char) > 2 else _EMPTY


def layer_s_raw(char):  # special (raw)
    return char[3] if len(char) > 3 else _EMPTY


def layer_s(char):
    raw = layer_s_raw(char)
    # non-tuple cases include None and {} (empty dict)
    return dict(raw) if isinstance(raw, tuple) else raw


def layer_s_ascii_strs(char):
    special = layer_s(char)
    return None if not special else ascii_strs(special)


def layerlt(char):
    return tuplify(layerl(char))


def layervt(char):
    return tuplify(layerv(char))


def layerat(char):
    return tuplify(layera(char))


def ascii_strs(special):
    return tuplify(special.get("ascii_strs"))


def tuplify(generic_x):
    if not generic_x:
        return tuple()
    if isinstance(generic_x, str):
        return (generic_x,)
    assert isinstance(generic_x, tuple)
    return generic_x


def mmcat(char):  # mmcat: multimark category
    vows, accs = layervt(char), layerat(char)
    lenv, lena = len(vows), len(accs)
    assert max(lenv, lena) <= 2
    if lenv != 2 and lena != 2:
        return None
    vava = _vava(vows, accs)
    handler_or_mmc = _VAVA_HANDLERS[vava]
    if handler_or_mmc is None or isinstance(handler_or_mmc, str):
        return handler_or_mmc
    return handler_or_mmc(vava, char, vows, accs)


# MMCAT: multimark category
# multimark: char with 2 vowels and/or 2 accents
# V/vow: vowel
# U/uacc: under-accent
# O/oacc: over-accent
# ∅: placeholder meaning "nothing" (no mark) (U+2205: EMPTY SET)
# In La??, L = lamed
# In La??, a = patax or qamats
# In LaO?, O = over-accent (as it does generally)
# In LaU?, U = under-accent (as it does generally)
# In La?i, i = hiriq
# In La?e, e = sheva
MMCAT_QUPO = "QUPO"  # qamats, uacc, patax, oacc
MMCAT_VUV_LAI = "LaUi"  # core of cmn yerushala[y]im form
MMCAT_VUV_LAE = "LaUe"  # core of rare yerushala[y]emah form
MMCAT_VOV_LAI = "LaOi"  # core of cmn yerushala[y]im form
MMCAT_VOV_LAE = "LaOe"  # core of rare yerushala[y]emah form
MMCAT_VV_LAI = "La∅i"  # core of rare accentless yerushala[y]im form
# There are no instances of what might be called MMCAT_VV_LAE (La∅e).
MMCAT_XUM = "XUM"  # VUM or UM: vow-or-∅, uacc, meteg/silluq
MMCAT_XUN = "XUN"  # VUN or UN: vow-or-∅, uacc, NON-meteg/silluq
MMCAT_XOO = "XOO"  # VOO or OO: vow-or-∅, oacc, oacc
MMCAT_XAA_S = "XAA_S"  # VOU, VUO, OU, UO (S="split" (over & under))


def _set_tuple_el(tup, i, val_at_idx):
    pad = (None,) * (i - len(tup))
    make_args = *tup[:i], *pad, val_at_idx, *tup[i + 1 :]
    return make(*make_args)


def _vava(vows, accs):
    accum = ""
    for vow, acc in itertools.zip_longest(vows, accs):
        if vow:
            accum += "V"
        if acc:
            accum += "U" if _IS_UNDERACC[acc] else "O"
    return accum


def _mmcat_xuu(_1, _2, _3, accs):  # _1, _2, _3 = vava, char, vows
    return MMCAT_XUM if accs[1] == uh.he_char_name(hpo.MTGOSLQ) else MMCAT_XUN


def _mmcat_vxv(vava, char, vows, _):  # _ is accs
    key = vava, layerl(char), vows
    return _VXV_MMCATS[key]


def _mmcat_qupo(_1, _2, vows, _3):  # _1, _2, _3 = vava, char, accs
    assert vows == (_QAMATS, _PATAX)
    return MMCAT_QUPO


_EMPTY = None
_QAMATS = uh.join_shunnas(hpo.QAMATS)
_PATAX = uh.join_shunnas(hpo.PATAX)
_VXV_MMCATS = {
    ("VUV", "l", (_PATAX, "i")): MMCAT_VUV_LAI,
    ("VUV", "l", (_QAMATS, "i")): MMCAT_VUV_LAI,
    ("VUV", "l", (_PATAX, ":")): MMCAT_VUV_LAE,  # Isaiah 36:2
    ("VUV", "l", (_QAMATS, ":")): MMCAT_VUV_LAE,  # 2 Kings 9:28
    ("VOV", "l", (_PATAX, "i")): MMCAT_VOV_LAI,
    ("VOV", "l", (_QAMATS, "i")): MMCAT_VOV_LAI,  # 4 cases, all in Psalms
    ("VOV", "l", (_PATAX, ":")): MMCAT_VOV_LAE,  # 1 Kings 10:2, Ezekiel 8:3
    # There are no instances of ('VOV', 'l', ('T', ':')).
    # I.e. MMCAT_VOV_LAE (LaOe) only exists for A=patax.
    ("VV", "l", (_PATAX, "i")): MMCAT_VV_LAI,  # Psalms 147:12
    # There are no instances of ('VV', 'l', ('T', 'i')).
    # I.e. MMCAT_VV_LAI (La∅i) only exists for A=patax.
    # There are no instances of what might be called MMCAT_VV_LAE (La∅e).
    # I.e. there are no sheva (':') cases for VV.
}
_VAVA_HANDLERS = {
    # 2V cases
    "VUVO": _mmcat_qupo,
    "VUV": _mmcat_vxv,
    "VOV": _mmcat_vxv,
    "VV": _mmcat_vxv,
    # 2 U cases
    "VUU": _mmcat_xuu,
    "UU": _mmcat_xuu,
    # 2 O cases
    "VOO": MMCAT_XOO,
    "OO": MMCAT_XOO,
    # OU & UO CASES
    "VOU": MMCAT_XAA_S,
    "VUO": MMCAT_XAA_S,
    "OU": MMCAT_XAA_S,
    "UO": MMCAT_XAA_S,
}
_IS_UNDERACC_UNI = {
    **{k: False for k in ha.UNI_OVER_ACCENTS},
    **{k: True for k in ha.UNI_UNDER_ACCENTS},
    hpo.MTGOSLQ: True,
}
_IS_UNDERACC = dk_map(uh.he_char_name, _IS_UNDERACC_UNI)
