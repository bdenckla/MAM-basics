"""Smoke tests for the by-book prose_ob_notes structured-text dataset.

The structured-text notes live in per-book ob_notes_* modules and are aggregated
by prose_ob_notes.get_structured_text(). These tests check that the aggregator wiring is
intact (every consumer still imports) and that the dataset is populated.
"""

from __future__ import annotations

import importlib

from accgram import prose_ob_notes

# Every module that consumes the structured-text dataset; importing them all is a smoke
# test that the aggregator wiring is intact.
_CONSUMERS = (
    "accgram.research_tao",
    "accgram.ob_report",
    "accgram.rtms_report",
    "accgram.rtms_missing_sof_pasuq_descriptions",
    "accgram.tm_sanity",
)


def test_ob_notes_dataset_is_populated() -> None:
    assert len(prose_ob_notes.get_structured_text()) == 93


def test_consumers_import() -> None:
    for name in _CONSUMERS:
        importlib.import_module(name)
