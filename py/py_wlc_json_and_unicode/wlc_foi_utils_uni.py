import re
import mb_cmn.uni_norm_fragile as unf
import mb_cmn.hebrew_accents as ha
import mb_cmn.hebrew_letters as hl
import mb_cmn.hebrew_points as hpo


def ff_init():
    fragile_foi = {
        "ff-counts": {},
        "ff-cases": [],
    }
    fragile_foi["ff-counts"]["misc"] = 0
    for pattkey, _patt in _PATTS:
        fragile_foi["ff-counts"][pattkey] = 0
    return fragile_foi


def collect_uni(io_fois, wlc_id, bcv, velsod):
    word = _get_word(velsod)
    if word is None:
        return
    fcomps = unf.get_fragile_comps(word)
    dropped, dropped_n = fcomps
    if dropped == dropped_n:
        return
    fragile_foi = io_fois["fragile_foi"]
    pattkey_found = None
    for pattkey, patt in _PATTS:
        if re.search(patt, word):
            assert pattkey_found is None
            pattkey_found = pattkey
    ffrec = _mk_ffrec(bcv, word, fcomps, pattkey_found)
    fragile_foi["ff-cases"].append(ffrec)
    count_key = "misc" if pattkey_found is None else pattkey_found
    fragile_foi["ff-counts"][count_key] += 1


_PATAX_OR_QAMATS = f"[{hpo.PATAX+hpo.QAMATS}]"
_UNDER_ACCENTS_STR = "".join(ha.UNI_UNDER_ACCENTS)
_OVER_ACCENTS_STR = "".join(ha.UNI_OVER_ACCENTS)
_SOME_VOWELS_STR = (
    hpo.SHEVA
    + hpo.XPATAX
    + hpo.XIRIQ
    + hpo.TSERE
    + hpo.SEGOL_V
    + hpo.PATAX
    + hpo.QAMATS
    + hpo.QUBUTS
)
#
_UNDER_ACCENT_PATT = f"[{_UNDER_ACCENTS_STR}]"
_OVER_ACCENT_PATT = f"[{_OVER_ACCENTS_STR}]"
_XIRIQ_OR_SHEVA = f"[{hpo.XIRIQ+hpo.SHEVA}]"
_SOME_VOWELS_PATT = f"[{_SOME_VOWELS_STR}]"
#
_LAUY_PATT = hl.LAMED + _PATAX_OR_QAMATS + _UNDER_ACCENT_PATT + _XIRIQ_OR_SHEVA
_LAYS_PATT = hl.LAMED + _PATAX_OR_QAMATS + _XIRIQ_OR_SHEVA + hpo.MTGOSLQ
_LAYO_PATT = hl.LAMED + _PATAX_OR_QAMATS + _XIRIQ_OR_SHEVA + _OVER_ACCENT_PATT
_LAY_PATT = hl.LAMED + _PATAX_OR_QAMATS + _XIRIQ_OR_SHEVA + hl.FMEM
_MTG_VOW_PATT = hpo.MTGOSLQ + _SOME_VOWELS_PATT
_PATTS = [
    ("patt-mtg-vow", _MTG_VOW_PATT),
    ("patt-lauy", _LAUY_PATT),
    ("patt-lays", _LAYS_PATT),
    ("patt-layo", _LAYO_PATT),
    ("patt-lay", _LAY_PATT),
]


def _mk_ffrec(bcv, word, fcomps, pattkey):
    dropped, dropped_n = fcomps
    return {
        "bcv": bcv,
        "word": word,
        "dropped": dropped,
        "dropped_n": dropped_n,
        "pattkey": pattkey,
    }


def _get_word(velsod):
    if isinstance(velsod, dict):
        return velsod.get("word")
    assert isinstance(velsod, str)
    return velsod
