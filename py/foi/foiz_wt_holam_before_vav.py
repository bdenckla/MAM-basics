"""Holam before vav, and holam haser for vav, in selected MAM body text.

Use the existing closed qere projection and the MAM body-text convention:
non-trivial qere, parameter 1 (pointed ketiv) of the trivial ketiv/qere
template, the first stress-helper representation, the dalet qamats
alternative, and combined cantillation. Alternatives are not additional
occurrences. Combining marks may intervene; another base letter may not.
The separate U+05BA category requires vav with holam haser for vav and then
another vav as the next base letter. The original pair categories are unchanged.
"""

from hkq_cmn.qere_projection import QereProjectionPolicy, project_qere_atoms
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_letters as hl
from mb_cmn import hebrew_points as hp
from mb_cmn import hebrew_punctuation as hpu
from mb_misc import mb_html
from py_html.hebrew_letter_spacing import iter_atoms
from foi import foi_struct as fct

_POLICY = QereProjectionPolicy(
    name="holam-before-vav-foi",
    trivial_qere_argument_key="1",
    stress_helper_argument_keys=("1",),
    qamats_argument_keys=("ד",),
    dual_cantillation_argument_keys=("כפול",),
)
_ABOVE_POINTS = {
    hp.XOLAM,
    hp.XOLAM_XFV,
    hp.RAFE,
    hp.SHIND,
    hp.SIND,
    hp.VARIKA,
    hpu.UPDOT,
    hpu.MCIRC,
}
_ABOVE_MARKS = ha.UNI_OVER_ACCENTS | _ABOVE_POINTS
HASER_CATEGORY = "Holam haser for vav before vav"


def find_fois_wt(mroge):
    """Return one native FOI row per matching two-letter pair."""
    minirow = mroge.get("mroge-minirow")
    if minirow is None:
        return []  # A repeated good ending is not another occurrence.
    text = "".join(
        item["text"]
        for item in project_qere_atoms(minirow.EP, source=None, policy=_POLICY)
    )
    pairs = [
        _feature(atom, start, end, marks)
        for _, _, atom in iter_atoms(text)
        for start, end, marks in matching_pairs(atom)
    ]
    haser = [
        _feature(atom, start, end, marks, HASER_CATEGORY)
        for _, _, atom in iter_atoms(text)
        for start, end, marks in haser_pairs(atom)
    ]
    return pairs + haser


def haser_pairs(atom):
    """Yield vav with U+05BA followed by vav, retaining all intervening marks."""
    starts = [i for i, char in enumerate(atom) if hl.ALEF <= char <= hl.TAV]
    clusters = list(zip(starts, starts[1:] + [len(atom)]))
    for (start, stop), (next_start, next_stop) in zip(clusters, clusters[1:]):
        if (
            atom[start] == hl.VAV
            and hp.XOLAM_XFV in atom[start + 1 : stop]
            and atom[next_start] == hl.VAV
        ):
            yield start, next_stop, atom[next_start + 1 : next_stop]


def matching_pairs(atom):
    """Yield exact pair ranges and the following vav's original marks."""
    starts = [i for i, char in enumerate(atom) if hl.ALEF <= char <= hl.TAV]
    consonants = "".join(atom[i] for i in starts)
    if consonants.endswith("יהוה"):
        return
    stops = starts[1:] + [len(atom)]
    clusters = list(zip(starts, stops))
    for (start, stop), (vav_start, vav_stop) in zip(clusters, clusters[1:]):
        if (
            atom[start] != hl.VAV
            and hp.XOLAM in atom[start + 1 : stop]
            and atom[vav_start] == hl.VAV
        ):
            yield start, vav_stop, atom[vav_start + 1 : vav_stop]


def _feature(atom, start, end, marks, category=None):
    above = "".join(mark for mark in marks if mark in _ABOVE_MARKS)
    if category is None:
        category = (
            "With an above-mark on vav" if above else "Without an above-mark on vav"
        )
    target = (
        atom[:start],
        mb_html.span_c(atom[start:end], "mam-doc-target-without-callout"),
        atom[end:],
    )
    qualifier = {"vav_marks": marks}
    return ("holam-before-vav", category), fct.make_qtarget(target, qualifier)
