"""Unit tests for the poetic SAT focus-word table logic (issue #10).

poetic_sat builds the genuine goerwitz SAT table for the poetic page. These pin
the two pieces that decide what it shows: the verse-final focus guard
(``focus_word``), which degrades a non-unique final word to None so
build_enriched_row does not abort, and the focus-word filtering of diff rows
(``_focus_only_diff``).

These are data-free unit tests; the end-to-end corpus run is exercised by
``generate-html`` itself.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_poetic_sat.py -v
"""

from __future__ import annotations

from accgram import poetic_sat


def test_focus_word_unique_final_word() -> None:
    assert (
        poetic_sat.focus_word(
            final_word="אדם׃", wlc_verse={"vels": ["מה", "רב", "אדם׃"]}
        )
        == "אדם׃"
    )


def test_focus_word_degrades_when_final_word_not_unique() -> None:
    assert (
        poetic_sat.focus_word(
            final_word="אדם׃", wlc_verse={"vels": ["אדם׃", "רב", "אדם׃"]}
        )
        is None
    )


def test_focus_word_none_without_final_word() -> None:
    assert poetic_sat.focus_word(final_word=None, wlc_verse=None) is None


def test_focus_only_diff_keeps_lone_focus_entry_as_bare_dict() -> None:
    focus_entry = {"wlc422": "אדם׃", "mam_simple": "אדֽם׃"}
    diff = [
        {"wlc422": [], "mam_simple": "־"},
        {"wlc422": "צפנת", "mam_simple": "צפנת"},
        focus_entry,
    ]
    assert poetic_sat._focus_only_diff(diff, wlc_focus="אדם׃") == focus_entry


def test_focus_only_diff_drops_non_focus_entries() -> None:
    diff = {"wlc422": "צפנת", "uxlc": "צפנת"}
    assert poetic_sat._focus_only_diff(diff, wlc_focus="אדם׃") == []
    assert poetic_sat._focus_only_diff([], wlc_focus="אדם׃") == []
    assert poetic_sat._focus_only_diff(None, wlc_focus="אדם׃") == []


def test_focus_only_diff_keeps_multiple_focus_entries_as_list() -> None:
    a = {"wlc422": "אדם׃", "mam_simple": "אדֽם׃"}
    b = {"wlc422": "אדם׃", "uxlc": "אד֯ם׃"}
    assert poetic_sat._focus_only_diff([a, b], wlc_focus="אדם׃") == [a, b]
