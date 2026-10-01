"""Transient phonetic annotation operations; these values are not release data.

Never normalize Hebrew. Display and release boundaries must independently reject
annotation points and retired carriers.
"""

import mb_cmn.hebrew_points as hpo
import mb_cmn.hebrew_punctuation as hpu
import phonetic_mam.core.vowar_and_accar as va

SHEVA_NA = hpo.SHEVA_NA
DAGESH_XAZAQ = hpo.DAGESH_XAZAQ

_LEGACY_SHEVA_NA = hpo.SHEVA + hpu.MCIRC
_LEGACY_DAGESH_XAZAQ = hpo.DAGOMOSD + hpu.UPDOT
_LEGACY_ANNOTATIONS = (
    (_LEGACY_SHEVA_NA, "U+05B0 U+05AF"),
    (_LEGACY_DAGESH_XAZAQ, "U+05BC U+05C4"),
)


def reject_legacy_annotations(value, source):
    """Reject a retired two-character annotation anywhere in loaded JSON."""
    if isinstance(value, str):
        present = [label for pair, label in _LEGACY_ANNOTATIONS if pair in value]
        if present:
            raise ValueError(
                f"{source} contains retired Phonetic MAM annotation pair(s): "
                + ", ".join(present)
            )
    if isinstance(value, list):
        for item in value:
            reject_legacy_annotations(item, source)
    if isinstance(value, dict):
        for item in value.values():
            reject_legacy_annotations(item, source)
    return value


def to_generic_points(he_str):
    return he_str.replace(SHEVA_NA, hpo.SHEVA).replace(DAGESH_XAZAQ, hpo.DAGOMOSD)


def convert_to_repeated_form(he_str):
    plain = to_generic_points(he_str)
    if plain == he_str:
        return None
    spair = SHEVA_NA, "s", hpo.SHEVA
    dpair = DAGESH_XAZAQ, "d", hpo.DAGOMOSD
    assert spair[1] not in he_str and dpair[1] not in he_str
    sparse = he_str
    sparse = sparse.replace(spair[0], spair[1]).replace(dpair[0], dpair[1])
    sparse = va.remove_both_vowar_and_accar(sparse)
    sparse = sparse.replace(spair[1], spair[2]).replace(dpair[1], dpair[2])
    return plain, sparse
