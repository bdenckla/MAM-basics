"""Holam on a non-vav letter immediately before vav, in selected MAM qere.

Use the existing closed qere projection and the MAM body-text convention:
non-trivial qere, parameter 1 (pointed ketiv) of the trivial ketiv/qere
template, the first stress-helper representation, the dalet qamats
alternative, and combined cantillation. Alternatives are not additional
occurrences. Combining marks may intervene; another base letter may not.
"""

import json
from functools import cache

from hkq_cmn.qere_projection import QereProjectionPolicy, project_qere_atoms
from mb_cmn import bib_locales as tbn
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_letters as hl
from mb_cmn import hebrew_points as hp
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import paths
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


def find_fois_wt(mroge):
    """Return one native FOI row per matching pair, including repeated atoms."""
    minirow = mroge.get("mroge-minirow")
    if minirow is None:
        return []  # A repeated good ending is not another occurrence.
    text = "".join(
        item["text"]
        for item in project_qere_atoms(minirow.EP, source=None, policy=_POLICY)
    )
    return [
        _feature(atom, start, end, marks, mroge["mroge-bcvt"])
        for _, _, atom in iter_atoms(text)
        for start, end, marks in matching_pairs(atom)
    ]


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


@cache
def _bhl_pages():
    path = paths.in_dir() / "holam-before-vav-bhl-pages.json"
    return json.loads(path.read_text(encoding="utf-8"))["pages"]


def _feature(atom, start, end, marks, bcvt):
    above = "".join(mark for mark in marks if mark in _ABOVE_MARKS)
    category = "With an above-mark on vav" if above else "Without an above-mark on vav"
    target = (
        atom[:start],
        mb_html.span_c(atom[start:end], "mam-doc-target-without-callout"),
        atom[end:],
    )
    qualifier = {
        "vav_marks": marks,
        "bhl": _bhl_pages().get(tbn.short_bcv_of_bcvt(bcvt)),
    }
    return ("holam-before-vav", category), fct.make_qtarget(target, qualifier)
