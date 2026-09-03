"""Which of Daniel Holman's MAM suggestions are about a meteg, and in which direction.

The roster is DERIVED, never assumed.  Holman's 34 MAM suggestions are rendered as
cards M1-M34, and the letter M is the series prefix rather than an abbreviation of
meteg: ``py/py_render/rt_mam_suggestion_card.py`` renders it as ``M{case_number}``.
Thirty of the 34 differ from their comparison form in metegs alone, and the arithmetic
below is what says which thirty.  The other four are the accent-placement records
M17, M24, M32 and M34, whose rulings are in
``py/hkq_cmn/mam_suggestion_dispositions.py``.

``direction`` answers with the edit MAM would take, not with what either text has:

1. ``REMOVAL`` -- MAM has one meteg the comparison form lacks, so applying the
   suggestion removes it.  Twenty-nine records, measured 2026-09-03.
2. ``ADDITION`` -- the comparison form has one meteg MAM lacks, so applying the
   suggestion adds it.  One record, M23 at Isaiah 23:12.

Stripping the FIRST meteg is what the arithmetic does, and that matters wherever a
form has two: a verse-final atom has a meteg serving as silluq after the one the
record names, and M13's atom has a meteg on each of two letters.

WHO READS THIS.  ``py/ws/holman_meteg_edit_spec.py`` builds the Wikisource bot edit
files from the same partition, and
``py/hkq_cmn/verify_meteg_suggestions_vs_mgketer.py`` checks each record against a
mgketer diff card.  Both need the identical roster, so it lives here rather than in
either of them.
"""

from __future__ import annotations

import hkq_paths
from hkq_cmn.json_io import load_json
from mb_cmn import hebrew_points as hpo

METEG = hpo.MTGOSLQ

REMOVAL = "removal"
ADDITION = "addition"


def direction(case) -> str | None:
    """Say ``REMOVAL`` or ``ADDITION``, or None for a record that is not about a meteg."""
    mam, comparison = case["mam_form"], case["comparison_form"]
    if METEG in mam and mam.replace(METEG, "", 1) == comparison:
        return REMOVAL
    if METEG in comparison and comparison.replace(METEG, "", 1) == mam:
        return ADDITION
    return None


def load_all_cases() -> list[dict]:
    """Every MAM-suggestion record, meteg or not, in the tracked derivative."""
    payload = load_json(hkq_paths.mam_suggestions_json_path())
    if not isinstance(payload, dict):
        raise ValueError("the MAM-suggestions derivative's root must be an object")
    return payload["cases"]


def load_meteg_cases() -> list[dict]:
    """The records whose MAM and comparison forms differ by one meteg, in case order."""
    cases = [case for case in load_all_cases() if direction(case) is not None]
    cases.sort(key=lambda case: case["case_number"])
    return cases
