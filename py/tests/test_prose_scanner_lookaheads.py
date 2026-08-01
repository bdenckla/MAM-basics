"""Unit tests for the four trailing-context scanner rules + has_legarmeh.

Stage 1 / Phase D hardening.  These pin the lex *trailing-context* semantics
that a generated lexer cannot express (silluq, mayela, legarmeh, plus the new-format
chapter lookahead via scan_book) and the stateful `has_legarmeh` counter, so a
regression in any one rule fails here rather than silently across thousands of
verses.

Run:
    .venv/Scripts/python.exe -m pytest py/tests/test_prose_scanner_lookaheads.py -v
"""

from __future__ import annotations

from accgram import accent_marks as am
from accgram.prose_scanner import HasLegarmeh, scan_accents, scan_book


def _types(
    body: str,
    bb: str = "xx",
    chnu: int = 1,
    vrnu: int = 1,
    h: HasLegarmeh | None = None,
) -> list[str]:
    return [t.type for t in scan_accents(body, bb, chnu, vrnu, h or HasLegarmeh())]


# --- silluq (meteg / [^ 379...]* sof-pasuq) ------------------------------------
def test_silluq_fires_immediately_before_sof_pasuq():
    # A meteg/silluq mark directly (modulo plain text) before sof pasuq is silluq.
    assert _types(am.METEG + "D" + am.SOF_PASUQ) == ["SILLUQ", "SOFPASUQ"]
    assert _types(am.METEG + "F" + am.SOF_PASUQ) == ["SILLUQ", "SOFPASUQ"]


def test_silluq_blocked_by_intervening_accent_is_swallowed():
    # atnax is a blocking mark (M-C 92 carries a '9'), so the meteg is a medial
    # metheg -> swallowed, and atnax is emitted instead.
    assert _types(am.METEG + am.ATNAX + ")" + am.SOF_PASUQ) == ["ATNAX", "SOFPASUQ"]


# --- mayela (tipexa / <meteg-only>* (sof-pasuq|atnax)) vs plain tipexa ----------
def test_mayela_when_73_reaches_sof_pasuq_or_atnax():
    # tipexa followed (within the word) only by allowed chars up to sof-pasuq/atnax.
    assert _types(am.TIPEXA + "NA" + am.SOF_PASUQ) == ["MAYELA", "SOFPASUQ"]
    assert _types(am.TIPEXA + "NA" + am.ATNAX + "Z" + am.SOF_PASUQ) == [
        "MAYELA",
        "ATNAX",
        "SOFPASUQ",
    ]


def test_tipexa_when_a_blocking_accent_intervenes():
    # revia is a blocking mark (M-C 81 carries an '8'), so tipexa stays plain.
    assert _types(am.TIPEXA + "NA" + am.REVIA + "C" + am.SOF_PASUQ) == [
        "TIPEXA",
        "REVIA",
        "SOFPASUQ",
    ]


# --- legarmeh (munax{TEXT}paseq / [^12368]*...revia) ---------------------------
def test_legarmeh_when_munax_paseq_precedes_revia():
    assert _types(am.MUNAX + "A" + am.PASEQ + "B" + am.REVIA + "C" + am.SOF_PASUQ) == [
        "LEGARMEH",
        "REVIA",
        "SOFPASUQ",
    ]


def test_munax_when_paseq_not_before_revia_outside_has_legarmeh_passage():
    # No following revia and an ordinary (non-listed) location -> plain munax.
    assert _types(
        am.MUNAX + "A" + am.PASEQ + "B" + am.MAHAPAKH + "C" + am.SOF_PASUQ, "gn", 1, 1
    ) == ["MUNAX", "MAHAPAKH", "SOFPASUQ"]


# --- has_legarmeh: keyed on structured (bb, ch, vs), so all 17 passages fire ----
# A synthetic munax+paseq that does NOT precede revia (so it is legarmeh only because
# the ref is listed), followed by a plain accent and a terminating silluq+sof-pasuq.
_RUTH_1_2 = (
    am.MUNAX + "A" + am.PASEQ + "B" + am.MAHAPAKH + "C" + am.METEG + "D" + am.SOF_PASUQ
)


def test_has_legarmeh_fires_at_listed_passage_not_elsewhere():
    # The munax+paseq is reinterpreted as legarmeh at any listed passage --
    # ru 1:2 *and*, now that detection is decoupled from header spelling, at a
    # ref like lv 10:6 that the old C abbreviation quirk silently missed.
    assert _types(_RUTH_1_2, "ru", 1, 2).count("LEGARMEH") == 1
    assert _types(_RUTH_1_2, "lv", 10, 6).count("LEGARMEH") == 1
    # ... but the very same body at a non-listed ref stays munax.
    assert _types(_RUTH_1_2, "gn", 1, 1).count("LEGARMEH") == 0


# --- has_legarmeh counter logic (now keyed on structured refs) ------------------
def test_has_legarmeh_1sam_14_47_second_occurrence_only():
    # 1Sam 14:47 has two munax+paseq sequences not before revia; only the
    # second counts as legarmeh.  Now live in the new format (keyed on ("1s",
    # 14, 47), not the dead "1Sam 14:47" abbreviation).
    h = HasLegarmeh()
    assert h("1s", 14, 47) is False
    assert h("1s", 14, 47) is True


def test_has_legarmeh_plain_passage_fires_first_time():
    h = HasLegarmeh()
    assert h("gn", 28, 9) is True


def test_has_legarmeh_old_i_is_monotonic():
    # old_i advances to the matched index, so an earlier passage no longer
    # matches afterwards ("assumes the books are in Jewish order").
    h = HasLegarmeh()
    assert h("ru", 1, 2) is True  # index 13
    assert h("gn", 28, 9) is False  # index 0 < old_i -> never revisited


# --- new-format chapter/verse lookahead (via scan_book) ------------------------
def test_scan_book_builds_reference_and_delimits_verses():
    text = f"1:1 {am.MERKHA}A{am.SOF_PASUQ}\n1:2 {am.REVIA}B{am.SOF_PASUQ}\n"
    verses = scan_book(text, "gn")
    # The reference's book label comes from the WLC code ("gn" -> "Genesis"),
    # not from any header line in the text.
    assert [v.reference for v in verses] == ["Genesis 1:1", "Genesis 1:2"]
    # Each verse opens with TILDE and closes with SOFPASUQ.
    assert verses[0].tokens[0].type == "TILDE"
    assert verses[0].tokens[-1].type == "SOFPASUQ"
