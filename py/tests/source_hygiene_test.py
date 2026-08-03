"""Guard test: source hygiene in hand-authored source (GitHub issues #22, #26).

Run from the repo root:
    .venv/Scripts/python.exe py/main_test.py py/tests/source_hygiene_test.py
On failure the assertion lists each offender as
``path:line  U+XXXX NAME -- detail``.

Pins the live tree (must stay clean) plus synthetic positive/negative controls
for both detectors: #22's orphan-combining-mark rule and #26's
no-decomposed-composite rule. Every synthetic combining mark is built from a
``\\N{...}`` name at runtime and interpolated into a source *string* we hand to
the scanner -- it is never written as an orphan literal, so this test file
itself passes the guard.
"""

import os

import repo_hygiene.source_hygiene as sh

_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(os.path.dirname(_HERE))

_Q = chr(34)  # a double-quote, to embed literals without nesting-quote pain
_DOT_BELOW = "\N{COMBINING DOT BELOW}"  # U+0323, built by name -- not an orphan literal


def test_live_tree_is_clean():
    offenses = sh.scan(_REPO_ROOT)
    assert not offenses, "orphan combining marks found:\n" + "\n".join(
        sh.format_offense(o) for o in offenses
    )


def test_detector_flags_raw_orphan():
    # Source line:  x = "<U+0323>dot"  -- the literal's raw source starts with a mark.
    src = f"x = {_Q}{_DOT_BELOW}dot{_Q}\n"
    offenses = list(sh.find_orphan_combining_marks("synthetic.py", src))
    assert len(offenses) == 1, offenses
    assert offenses[0].codepoint == "U+0323"
    assert offenses[0].uname == "COMBINING DOT BELOW"
    assert offenses[0].line == 1


def test_detector_accepts_named_escape():
    # The approved fix: the SAME character written as a \N{...} escape. Its decoded
    # value is identical to the raw mark, so a value-based check would false-positive;
    # the raw-source check accepts it (the segment starts with a backslash).
    src = 'x = "\\N{COMBINING DOT BELOW}dot"\n'
    assert list(sh.find_orphan_combining_marks("synthetic.py", src)) == []


def test_detector_ignores_base_then_mark():
    # A real Hebrew word: base letter, a joiner, then a combining accent mid-string
    # (cf. fois_mark_grammar_foi.py). The literal starts with a base letter -- not
    # an orphan.
    word = (
        "\N{HEBREW LETTER PE}"
        + "\N{ZERO WIDTH JOINER}"
        + "\N{HEBREW ACCENT GERESH MUQDAM}"
    )
    src = f"x = {_Q}{word}{_Q}\n"
    assert list(sh.find_orphan_combining_marks("synthetic.py", src)) == []


def test_detector_ignores_mark_in_comment():
    # A raw combining mark in a comment is not a string literal -- AST precision
    # means it is not flagged (a naive regex would false-positive here).
    src = f"x = 1  # {_DOT_BELOW} floating in a comment\n"
    assert list(sh.find_orphan_combining_marks("synthetic.py", src)) == []


def test_pragma_suppresses():
    src = f"x = {_Q}{_DOT_BELOW}dot{_Q}  {sh._PRAGMA}\n"
    assert list(sh.find_orphan_combining_marks("synthetic.py", src)) == []


_PRECOMPOSED_H = "\N{LATIN SMALL LETTER H WITH DOT BELOW}"  # U+1E25, built by name


def test_decomposed_composite_flags_decomposed_h():
    # "h" + U+0323 is a decomposed canonical composite -- should compose to U+1E25.
    src = f"x = {_Q}tah{_DOT_BELOW}ton{_Q}\n"
    offenses = list(sh.find_decomposed_composites("synthetic.py", src))
    assert len(offenses) == 1, offenses
    assert offenses[0].codepoint == "U+0323"
    assert offenses[0].uname == "COMBINING DOT BELOW"
    assert "U+1E25" in offenses[0].detail
    assert offenses[0].line == 1


def test_decomposed_composite_accepts_precomposed():
    # The already-composed form is clean -- nothing left to flag.
    src = f"x = {_Q}ta{_PRECOMPOSED_H}ton{_Q}\n"
    assert list(sh.find_decomposed_composites("synthetic.py", src)) == []


def test_decomposed_composite_ignores_reordered_hebrew():
    # A real Hebrew word with points in NON-canonical combining-class order: a
    # letter, then DAGESH (ccc 21), then QAMATS (ccc 18) -- QAMATS should sort
    # first under canonical ordering, so this sequence is reordered relative to
    # NFC. Neither pair composes to a single codepoint (Hebrew letter+point
    # pairs are all composition-excluded), so this must yield 0 offenses --
    # proving the check requires composition, not canonical reordering.
    word = (
        "\N{HEBREW LETTER BET}"
        + "\N{HEBREW POINT DAGESH OR MAPIQ}"
        + "\N{HEBREW POINT QAMATS}"
    )
    src = f"x = {_Q}{word}{_Q}\n"
    assert list(sh.find_decomposed_composites("synthetic.py", src)) == []
