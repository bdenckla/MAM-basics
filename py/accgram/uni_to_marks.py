r"""Extract the Unicode **mark sequence** the scanners consume (issue wlc-utils#9, Phase 2).

The prose/poetic scanners (`prose_scanner` / `poetic_scanner`) read each verse
as a stream of single-character *marks* -- one Unicode codepoint per accent
(plus meteg/paseq/sof-pasuq/puncta), one ``LETTER`` placeholder per base letter, and
maqaf (``-``) / space word boundaries -- as defined in `accent_marks`.  This module
produces that mark body straight from the canonical ``-kq-u`` Unicode verses.

It is the partial inverse of `wlc_uword.uword`, but only faithful to what the scanner
and `lexical_validation` actually read:

* **Letters** are opaque filler (the rules key on the marks and the word boundaries),
  so each base letter becomes a single ``LETTER`` placeholder and vowels/points are
  dropped -- real reverse-transliteration is unnecessary.
* **Accents** pass through as their own codepoint.  The five M-C codepoint conflations
  no longer need distinct codes: pashta and telisha qetana keep both their stress-helper
  and their main occurrence (the scanner merges an adjacent same-accent run into one
  token), and the one swallowed secondary -- the non-first of a repeated telisha gedola
  (M-C 44) -- is dropped here.  A telisha gedola that shares a word with a geresh or
  gershayim keeps *both* marks, sequenced in their Unicode (manuscript) order --
  gerstar-then-telg where the pair shares a base letter -- and, where they share a base
  letter, `lexical_validation` whitelists the same-letter pair (`word_to_marks`).
* **Prepositive accents** (yetiv, geresh muqdam, dexi, telisha gedola) are relocated to
  the front of the word's mark sequence, undoing `wlc_uword._PREPOS_PATT`'s move past an
  accent on the first letter, so the scanner reads the accents in M-C order.  The one
  exception is a telg + gerstar word, where the telg stays in document order so the pair
  keeps its Unicode (manuscript) order (`word_to_marks`).
* **Boundaries / punctuation** are reproduced exactly: maqaf -> ``-``, inter-word gaps
  -> space, paseq / sof pasuq / puncta as their own codepoints.
* **Ketiv-qere & notes** reproduce the token stream the M-C source presented: the ketiv
  is a swallowed ``*<letters>`` atom, the qere ``**`` + its pointed body, and
  ``notes`` are appended verbatim (the ``]N`` markers the legarmeh/mayela lookaheads
  key on).

Parity with the Phase-1 outputs is verified by a zero-diff of the git-tracked
``*_ag`` outputs (issue wlc-utils#9, Phase 2; prose became per-verse JSON in wlc-utils#20).
"""

from __future__ import annotations

from collections import OrderedDict
from pathlib import Path

from accgram import accent_marks as am
from accgram import rtms_data

# --- codepoint classification -------------------------------------------------

MAQAF = "־"  # U+05BE; emitted as the boundary mark ``-``

# Cantillation-accent codepoints other than the conflated/positional ones pass
# straight through as their own mark.  Meteg, paseq, sof-pasuq and the puncta are
# kept too (their codepoints are already their marks).
KEPT_NON_ACCENT = frozenset(
    (am.METEG, am.PASEQ, am.SOF_PASUQ, am.UPPER_DOT, am.LOWER_DOT)
)

# Prepositive accents: written at the word's start but relocated by
# `wlc_uword._PREPOS_PATT` to just after the first letter -- a move that can carry
# them past an accent on that first letter, inverting the accent order the scanner
# reads.  We restore M-C order by emitting them at the front of the word's marks.
# Gershayim (M-C 12) is *also* prepositive in M-C, but is deliberately left out: it never
# needs front-loading here (in the telg + gershayim words it partners the telisha gedola,
# and the same-letter pair is handled by the telg!gerstar exception below).  (The secondary
# telisha gedola 44 is prepositive too but is the dropped non-first of a repeat below.)
PREPOSITIVE_MARKS = frozenset((am.YETIV, am.GERESH_MUQDAM, am.DEXI, am.TELISHA_GEDOLA))

# The geresh family (plain geresh, gershayim, and the prose geresh muqdam, which the
# scanner normalizes to a plain geresh).  Used to detect a telg + gerstar word, where the
# telg's prepositive front-loading is suppressed so the scanner reads the two marks in
# their Unicode (manuscript) order -- see `word_to_marks`.
GERESH_FAMILY = frozenset((am.GERESH, am.GERSHAYIM, am.GERESH_MUQDAM))


def is_base_letter(ch: str) -> bool:
    return "א" <= ch <= "ת"


def is_accent(ch: str) -> bool:
    """A real accent (U+0591..U+05AE) -- meteg (U+05BD) excluded."""
    return "\N{HEBREW ACCENT ETNAHTA}" <= ch <= "\N{HEBREW ACCENT ZINOR}"


# --- word transcoding ---------------------------------------------------------


def word_to_marks(word: str) -> str:
    """Transcode one Unicode word/atom into its scanner-ready mark string.

    Letters become ``LETTER`` placeholders, points are dropped, accents pass through as
    their codepoints, and maqaf / paseq / sof pasuq / puncta are emitted verbatim.
    Prepositive accents are restored to the front of the mark sequence (see
    `PREPOSITIVE_MARKS`).

    One secondary is dropped here: the non-first of a *repeated* telisha gedola (M-C 44).

    A telisha gedola that shares a word with a geresh or gershayim keeps BOTH marks; this
    is the prose analogue of the poetic dexi + munax whitelist entry -- a legitimate
    same-letter pair spared as a two-token *sequence*, not fused.  For such a telg + gerstar
    word the telisha gedola's prepositive front-loading is **suppressed**, so the scanner
    reads the two marks in their Unicode (manuscript) order: gerstar-then-telg in the three
    same-letter words (Gen 5:29, Zeph 2:15, and -- as a geresh muqdam -- 2 Kings 17:13),
    telg-then-gerstar in the two cross-letter words (Lev 10:4, Ezek 48:10, where the telg
    leads only because it is prepositive and written at the word's front).  The grammar
    accepts both orders (a big telisha freely precedes or follows a geresh -- see
    prose_ply_grammar's geresh_pashta_clause / big_telisha_pashta_clause), so each sequence parses
    cleanly.  Where the two marks share one base letter, the resulting same-letter pair is
    whitelisted in `lexical_validation._WHITELISTED_SAME_LETTER` rather than flagged; the
    cross-letter words already sit on two letters and need no whitelist.  A prose geresh
    muqdam (2 Kings 17:13's companion, and the lone Lev 1:3 case) passes through as its own
    codepoint here and is normalized to a plain geresh by the scanner (see prose_scanner); the
    whitelist therefore lists the raw geresh muqdam codepoint alongside plain geresh.

    Keeping both marks is the most faithful reading -- it preserves both accents the
    manuscript has, where dropping either would discard one.  Preserving the Unicode order
    (rather than floating the prepositive telg to the front) keeps the checker's reading
    faithful to the manuscript, which has the same-letter pairs gerstar-first.  See the
    telisha gedola section of gh-pages/accgram/almost-errors.html (generator:
    accgram/almost_errors.py).
    """
    # Build the ordered mark sequence and the skeleton of letters/maqaf, marking where
    # marks go.  Prepositive accent marks are pulled to the front -- except in a telg +
    # gerstar word, where the telg (and a co-located geresh muqdam) stay in document order
    # so the scanner reads the pair in its Unicode (manuscript) order (see the docstring).
    telg_gerstar = am.TELISHA_GEDOLA in word and any(c in GERESH_FAMILY for c in word)
    skeleton: list[str | None] = []  # str = literal char; None = "a mark slot here"
    prepos_marks: list[str] = []
    other_marks: list[str] = []
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
                    continue  # non-first of a repeated telisha gedola (M-C 44)
                mark = am.TELISHA_GEDOLA
            else:
                mark = ch  # the accent codepoint is its own mark
        elif ch in KEPT_NON_ACCENT:
            mark = ch
        if mark is None:
            continue  # a point/vowel/dagesh/shin-dot/etc. -> dropped (scanner filler)
        skeleton.append(None)
        # In a telg + gerstar word the telg and a co-located geresh muqdam are kept in
        # document order (not front-loaded), preserving the Unicode mark order.
        front_load = mark in PREPOSITIVE_MARKS and not (
            telg_gerstar and mark in (am.TELISHA_GEDOLA, am.GERESH_MUQDAM)
        )
        if front_load:
            prepos_marks.append(mark)
        else:
            other_marks.append(mark)

    marks = iter(prepos_marks + other_marks)
    return "".join(next(marks) if part is None else part for part in skeleton)


def _notes_suffix(notes: object) -> str:
    """The ``]N`` markers appended after a word, verbatim (legarmeh/mayela lookaheads
    key on ``]<digit>``).

    The kq-u loader collapses a ``notes`` list into one string
    (`rtms_data._collapse_wlc_notes_to_string`), so accept either form.
    """
    if isinstance(notes, str):
        return notes
    if isinstance(notes, list):
        return "".join(n for n in notes if isinstance(n, str))
    return ""


def _vel_to_marks(vel: object) -> str:
    """Transcode one verse element to its mark fragment."""
    if isinstance(vel, str):
        return word_to_marks(vel)
    if not isinstance(vel, dict):
        return ""

    sam = vel.get("sam_pe_inun")
    if isinstance(sam, str):
        # Petuhah/setumah/nun-inversum: a lone P/S/N atom; N re-acquires its ``]8`` note
        # (mirrors wlc_read_and_parse_mdc._distinguish_sam_pe_inun).  Scanner swallows it.
        return "N]8" if sam == "N" else sam

    kq = vel.get("kq")
    if kq is not None:
        return _kq_to_marks(kq)

    word = vel.get("word")
    if isinstance(word, str):
        return word_to_marks(word) + _notes_suffix(vel.get("notes"))
    return ""


def _kq_to_marks(kq: object) -> str:
    """Transcode a ketiv-qere element to ``*<ketiv> **<qere>``.

    The scanner swallows the ketiv whole (``\\*[^* \\r\\n-]+``) and the ``**`` of the
    qere, then scans the (pointed) qere normally -- so only the qere carries grammar-
    visible marks.  An implicit-empty side (qere perpetuum / ketiv-only) emits the
    ``*kk`` / ``**qq`` placeholder the M-C source used, both swallowed.
    """
    ketiv, qere = kq if isinstance(kq, (list, tuple)) and len(kq) == 2 else ([], [])
    ketiv_words = [w for w in (_kq_word(v) for v in ketiv) if w]
    qere_words = [w for w in (_kq_word(v) for v in qere) if w]
    ketiv_part = "*" + "-".join(ketiv_words) if ketiv_words else "*kk"
    qere_part = "**" + "-".join(qere_words) if qere_words else "**qq"
    return f"{ketiv_part} {qere_part}"


def _kq_word(vel: object) -> str:
    if isinstance(vel, str):
        return word_to_marks(vel)
    if isinstance(vel, dict):
        word = vel.get("word")
        if isinstance(word, str):
            return word_to_marks(word) + _notes_suffix(vel.get("notes"))
    return ""


def verse_to_marks(verse: dict) -> str:
    """Transcode one ``-kq-u`` verse ``{bcv, vels}`` into the scanner-ready mark body."""
    vels = verse.get("vels")
    if not isinstance(vels, list):
        return ""
    parts: list[str] = []
    prev_ended_maqaf = False
    for vel in vels:
        frag = _vel_to_marks(vel)
        if not frag:
            continue
        if parts and not prev_ended_maqaf:
            parts.append(" ")
        parts.append(frag)
        prev_ended_maqaf = frag.endswith(am.MAQAF)
    return "".join(parts)


# --- book-text builder (drop-in for split_wlc.split_wlc_to_book_texts) ---------


def build_book_texts(
    wlc422_kq_u_dir: Path,
    keep_line_fn=None,
) -> "OrderedDict[str, str]":
    """Per-book scanner-ready text from the ``-kq-u`` JSON, mirroring the shape
    `split_wlc.split_wlc_to_book_texts` returned from ``wlc422_ps.txt``.

    Each value is normalized ``ch:vr <body>`` lines (the 2-char WLC book code
    dropped), in source order.  ``keep_line_fn(bb, chnu, vrnu)`` (the genre
    filter) may exclude verses.
    """
    index = rtms_data.load_wlc422_index(wlc422_kq_u_dir)

    per_book: OrderedDict[str, list[str]] = OrderedDict()
    for bcv, verse in index.items():
        bb, chnu, vrnu = _split_bcv(bcv)
        if keep_line_fn is not None and not keep_line_fn(bb, chnu, vrnu):
            continue
        body = verse_to_marks(verse)
        per_book.setdefault(bb, []).append(f"{chnu}:{vrnu} {body}")

    book_texts: OrderedDict[str, str] = OrderedDict()
    for bb, lines in per_book.items():
        book_texts[bb] = "".join(f"{ln}\n" for ln in lines)
    return book_texts


def _split_bcv(bcv: str) -> tuple[str, int, int]:
    """``gn1:1`` -> ``("gn", 1, 1)``."""
    bb = bcv[:2]
    chv = bcv[2:]
    ch, _colon, vr = chv.partition(":")
    return bb, int(ch), int(vr)
