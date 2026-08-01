"""Tree-generation / "real computing" for the "almost errors" page.

The compute layer behind ``almost_errors_html``: mode-aware ``word_to_marks``
swaps, scan/parse, and the clean/ERROR/NO_PARSE verdicts that drive the
alternate-reading parse trees.  These functions take ``bcv``/``mode`` parameters
and have **zero HTML dependency** -- they only scan and parse the real grammar,
so the page can never drift from the checker's actual behaviour.

All swaps of ``uni_to_marks.word_to_marks`` (and the scanner's fuse rule) are
scoped to a context manager and restored on exit (read-only: no module is left
mutated permanently).
"""

from __future__ import annotations

import contextlib
from typing import NamedTuple

from accgram import accent_marks as am
from accgram import lexical_validation
from accgram import prose_scanner
from accgram import prose_run
from accgram import uni_to_marks
from accgram.prose_ply_grammar import LOCATION_ONLY, parse_tokens
from accgram.prose_scanner import HasLegarmeh, Token, scan_accents
from accgram.tree import print_tree
from accgram.uni_to_marks import (
    KEPT_NON_ACCENT,
    MAQAF,
    PREPOSITIVE_MARKS,
    is_accent,
    is_base_letter,
)

# The geresh family (plain geresh U+059C, gershayim U+059D's plain sibling, and the
# geresh muqdam U+059D promoted/demoted form) the telisha gedola companion-drop concerns.
_GG = frozenset((am.GERESH, am.GERSHAYIM))


# --------------------------------------------------------------------------- #
# Tree generation
# --------------------------------------------------------------------------- #
def _build_word_variant(word: str, mode: str) -> str:
    """``uni_to_marks.word_to_marks``, but for a word carrying BOTH a telisha gedola
    and a geresh-family mark, apply ``mode`` (keep_both / keep_telg / keep_gerstar).

    ``keep_both`` reproduces the checker's real reading (both marks kept, in their Unicode
    (manuscript) order -- identical token stream to the live ``word_to_marks``);
    ``keep_telg`` and ``keep_gerstar`` are the two counterfactual single-mark readings the
    exhibit shows also parse cleanly.  It rebuilds the mark skeleton, dropping the telg or
    the geresh-family companion per ``mode`` (or neither, for keep_both), scoped to words
    holding *both*; every other word is transcoded normally.  As in ``word_to_marks``, the
    telg's prepositive front-loading is suppressed in a telg + gerstar word, so the pair
    keeps its document (manuscript) order.
    """
    has_telg = am.TELISHA_GEDOLA in word
    has_gerstar = any((am.GERESH if c == am.GERESH_MUQDAM else c) in _GG for c in word)
    both = has_telg and has_gerstar
    skeleton: list[str | None] = []
    prepos: list[str] = []
    other: list[str] = []
    telg_seen = 0
    for ch in word:
        if is_base_letter(ch):
            skeleton.append(am.LETTER)
            continue
        if ch == MAQAF:
            skeleton.append(am.MAQAF)
            continue
        mark: str | None = None
        if is_accent(ch):
            if ch == am.TELISHA_GEDOLA:
                telg_seen += 1
                if telg_seen > 1:
                    continue
                if both and mode == "keep_gerstar":
                    continue  # drop the telg
                mark = am.TELISHA_GEDOLA
            else:
                as_geresh = am.GERESH if ch == am.GERESH_MUQDAM else ch
                if as_geresh in _GG:
                    if both and mode == "keep_telg":
                        continue  # drop the geresh-family companion (a counterfactual)
                    mark = as_geresh
                else:
                    mark = ch
        elif ch in KEPT_NON_ACCENT:
            mark = ch
        if mark is None:
            continue
        skeleton.append(None)
        # In a telg + gerstar word the telg is kept in document order (not front-loaded),
        # preserving the Unicode mark order -- mirroring uni_to_marks.word_to_marks.
        front_load = mark in PREPOSITIVE_MARKS and not (
            both and mark == am.TELISHA_GEDOLA
        )
        (prepos if front_load else other).append(mark)
    marks = iter(prepos + other)
    return "".join(next(marks) if p is None else p for p in skeleton)


@contextlib.contextmanager
def _word_to_marks_mode(mode: str):
    """Temporarily swap ``uni_to_marks.word_to_marks`` for the mode-aware variant,
    restoring the original on exit (read-only: the module is never left mutated)."""
    original = uni_to_marks.word_to_marks
    uni_to_marks.word_to_marks = lambda w: _build_word_variant(w, mode)
    try:
        yield
    finally:
        uni_to_marks.word_to_marks = original


def _scan_and_parse(bcv: str, body: str, parser, has_legarmeh: HasLegarmeh):
    bb = bcv[:2]
    chnu, vrnu = (int(part) for part in bcv[2:].split(":"))
    tokens = [Token("TILDE", "")] + scan_accents(body, bb, chnu, vrnu, has_legarmeh)
    return parse_tokens(parser, tokens)


def _tree_text(tree) -> str:
    if tree in (None, LOCATION_ONLY):
        return "NO_PARSE"
    return print_tree(tree, 0).rstrip("\n")


def _telg_verdict(tree) -> str:
    if tree in (None, LOCATION_ONLY):
        return "NO_PARSE"
    return "ERROR" if "ERROR" in print_tree(tree) else "clean"


def _telg_tree_text(
    bcv: str, mode: str, index, parser, has_legarmeh: HasLegarmeh
) -> str:
    """Tree text for one telg-exhibit verse under one alternate reading ``mode``."""
    with _word_to_marks_mode(mode):
        body = uni_to_marks.verse_to_marks(index[bcv])
    return _tree_text(_scan_and_parse(bcv, body, parser, has_legarmeh))


def _telg_verdict_for(
    bcv: str, mode: str, index, parser, has_legarmeh: HasLegarmeh
) -> str:
    with _word_to_marks_mode(mode):
        body = uni_to_marks.verse_to_marks(index[bcv])
    return _telg_verdict(_scan_and_parse(bcv, body, parser, has_legarmeh))


def _prose_verse_tree_text(bcv: str, index, parser, has_legarmeh: HasLegarmeh) -> str:
    """The checker's *live* tree text for a prose verse, exactly as prose_run renders it.

    Reuses the prose_run lexical layer (so lv25:20 reads as its ``illegal_mark`` tree,
    grammar skipped) and the same illegal-mark label, so the page can never drift from
    the corpus output."""
    verse = index[bcv]
    body = uni_to_marks.verse_to_marks(verse)
    ungrammatical = lexical_validation.lexical_ungrammatical(body)
    if ungrammatical:
        words = prose_run._ungrammatical_unicode_words(ungrammatical, verse)
        return print_tree(prose_run._illegal_mark_tree(ungrammatical, words), 0).rstrip(
            "\n"
        )
    return _tree_text(_scan_and_parse(bcv, body, parser, has_legarmeh))


def _ek2031_word_variant(word: str, mode: str, base) -> str:
    """``uni_to_marks.word_to_marks``, but for ek20:31's ``נִטְמְאִ֤֨ים`` (the one word
    carrying BOTH a mahapakh and a qadma on a single letter) apply ``mode`` -- one of the
    four alternatives to the fused reading (drop one mark, or keep both as a sequence in
    either order).  ``base`` is the real (pre-swap) ``word_to_marks``, used unchanged for
    ``fused`` and for every word not carrying both marks.

    For ``fused`` (and any non-matching word) the scanner fuses the pair as it normally
    would.  The two ``seq_*`` modes only set the mark *order*; ``seq_mah_qadma`` still
    scans as the fused token unless the caller also suppresses the fuse rule (see
    ``_no_mahapakh_qadma_fuse``)."""
    both = am.MAHAPAKH in word and am.QADMA in word
    if mode == "fused" or not both:
        return base(word)
    skeleton: list[str | None] = []
    prepos: list[str] = []
    other: list[str] = []
    for ch in word:
        if is_base_letter(ch):
            skeleton.append(am.LETTER)
            continue
        if ch == MAQAF:
            skeleton.append(am.MAQAF)
            continue
        mark: str | None = None
        if ch == am.MAHAPAKH:
            if mode == "drop_mahapakh":
                continue
            mark = am.MAHAPAKH
        elif ch == am.QADMA:
            if mode == "drop_qadma":
                continue
            mark = am.QADMA
        elif is_accent(ch):
            mark = ch
        elif ch in KEPT_NON_ACCENT:
            mark = ch
        if mark is None:
            continue
        skeleton.append(None)
        (prepos if mark in PREPOSITIVE_MARKS else other).append(mark)
    if mode in ("seq_qadma_mah", "seq_mah_qadma"):
        mah_i, qad_i = other.index(am.MAHAPAKH), other.index(am.QADMA)
        want_qadma_first = mode == "seq_qadma_mah"
        if (qad_i < mah_i) != want_qadma_first:
            other[mah_i], other[qad_i] = other[qad_i], other[mah_i]
    marks = iter(prepos + other)
    return "".join(next(marks) if p is None else p for p in skeleton)


@contextlib.contextmanager
def _ek_word_to_marks_mode(mode: str):
    """Temporarily swap ``uni_to_marks.word_to_marks`` for the ek20:31 variant, restoring
    the original on exit (read-only: the module is never left mutated)."""
    original = uni_to_marks.word_to_marks
    uni_to_marks.word_to_marks = lambda w: _ek2031_word_variant(w, mode, original)
    try:
        yield
    finally:
        uni_to_marks.word_to_marks = original


@contextlib.contextmanager
def _no_mahapakh_qadma_fuse():
    """Temporarily drop the scanner's ``MAHAPAKHQADMA`` fuse rule so a mahapakh-then-qadma
    adjacency scans as two tokens (``MAHAPAKH QADMA``) instead of re-fusing -- the only way
    to observe the ``seq_mah_qadma`` reading as a genuine sequence.  Restored on exit.
    """
    original = prose_scanner._GG_RULES
    prose_scanner._GG_RULES = [r for r in original if r[1] != "MAHAPAKHQADMA"]
    try:
        yield
    finally:
        prose_scanner._GG_RULES = original


def _ek_verdict_for(mode: str, index, parser, has_legarmeh: HasLegarmeh) -> str:
    """``clean`` / ``ERROR`` / ``NO_PARSE`` for ek20:31 under one ``_EK_MODES`` reading."""
    with contextlib.ExitStack() as stack:
        stack.enter_context(_ek_word_to_marks_mode(mode))
        if mode == "seq_mah_qadma":
            stack.enter_context(_no_mahapakh_qadma_fuse())
        body = uni_to_marks.verse_to_marks(index["ek20:31"])
        return _telg_verdict(_scan_and_parse("ek20:31", body, parser, has_legarmeh))


def _telg_gerstar_word(verse: object) -> str | None:
    for word in prose_run._verse_display_words(verse):
        has_telg = am.TELISHA_GEDOLA in word
        has_gerstar = any(
            (am.GERESH if c == am.GERESH_MUQDAM else c) in _GG for c in word
        )
        if has_telg and has_gerstar:
            return word
    return None


class TelgForms(NamedTuple):
    """The Hebrew word forms the telg exhibit table displays for one word."""

    word: str  # the real WLC word, both marks, shown post-charity (geresh muqdam -> geresh)
    keep_telg: str  # the telisha gedola alone (geresh-family companion dropped)
    keep_gerstar: (
        str  # the geresh-family mark alone (telisha gedola dropped), post-charity
    )
    same_letter: bool  # both marks sit on one base letter, so the repeated-word seq is non-trivial


def _telg_marks_share_letter(word: str) -> bool:
    """True if ``word``'s telisha gedola and geresh-family mark hang on the *same* base
    letter (gn5:29 / zp2:15 / 2k17:13) rather than on two letters of one word (lv10:4 /
    ek48:10).  Only same-letter words get a synthesized repeated-word sequence in the
    table; a cross-letter word already carries its two marks in sequence."""
    telg_at: int | None = None
    ger_at: int | None = None
    letter_idx = -1
    for ch in word:
        if is_base_letter(ch):
            letter_idx += 1
        elif ch == am.TELISHA_GEDOLA:
            telg_at = letter_idx
        elif (am.GERESH if ch == am.GERESH_MUQDAM else ch) in _GG:
            ger_at = letter_idx
    return telg_at is not None and telg_at == ger_at


def _telg_word_forms(word: str) -> TelgForms:
    """Derive the exhibit table's Hebrew word forms from a real WLC word carrying both a
    telisha gedola and a geresh-family companion.

    Every form is shown post-charity: a geresh muqdam (2k17:13) is rendered as a plain
    geresh, matching the geresh muqdam charity above.  ``keep_telg`` drops the geresh-family
    mark; ``keep_gerstar`` drops the telisha gedola."""
    post_charity = word.replace(am.GERESH_MUQDAM, am.GERESH)
    keep_telg = "".join(c for c in post_charity if c not in (am.GERESH, am.GERSHAYIM))
    keep_gerstar = post_charity.replace(am.TELISHA_GEDOLA, "")
    return TelgForms(
        word=post_charity,
        keep_telg=keep_telg,
        keep_gerstar=keep_gerstar,
        same_letter=_telg_marks_share_letter(word),
    )
