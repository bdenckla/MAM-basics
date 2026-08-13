"""Read the two Decalogues' m-trad strands from BOTH of the repo's sources (issue wlc-utils#68).

The repo holds MAM's manuscript-tradition taxton and elyon Decalogue readings twice over,
and the printed-Decalogue page trio takes the m-trad as its authoritative baseline, so the
two copies had better agree:

* the vendored Hebrew Wikisource data ``in/accgram/printed_decalogue_teamim.json``
  (``tradition: "manuscript"``), which the pages read live; and
* the sibling repo MAM-parsed's ``plus`` subtree, MAM's own parse of its own text.

This module reads each source into the same ``Strand`` shape and diffs them.  Nothing
generates output from it; ``py/tests/test_decalogue_m_trad.py`` is the consumer, so a
refresh of either source that moves a word or a stroke fails the suite rather than
silently invalidating a page's ground-truth claim.

HOW THE STRANDS ARE ENCODED IN THE PLUS TREE.  A verse is a three-cell minirow (C, D, E);
the body text -- and every marker this module cares about -- lives in cell E.  Where the
two strands part company the text sits inside a ``מ:כפול`` template, whose named params are
``כפול`` (the dually-accented text as the great codexes have it), ``א`` (the taxton strand
alone) and ``ב`` (the elyon strand alone).  Text outside any ``מ:כפול`` is shared by both
strands.  Deciding which of ``א``/``ב`` is which needs no appeal to tradition: at Exod 20:2
the ``א`` reading closes on עֲבָדִ֑ים with atnaX and runs on, while ``ב`` closes it with
silluq and sof pasuq -- the taxton and elyon behaviours respectively, and the same pair of
signal accents ``printed_decalogue_strands`` pins the vendored side against.

THE VERTICAL STROKE IS TEMPLATE-BORNE ON BOTH SIDES, NOT LITERAL.  Neither Decalogue holds
a literal U+05C0 anywhere in cell E: every stroke is a ``מ:לגרמיה-2`` (legarmeh) or a
``מ:פסק`` (narrow-sense paseq) template, so the distinction the glyph cannot express is
carried by template identity.  The vendored ``faithful_chanted_verses`` keeps the same
distinction with its own ``{{מ:לגרמיה}}`` / ``{{מ:פסק}}`` (issue wlc-utils#74), where the folded
``chanted_verses`` collapses both to U+05C0.  So the two sources can be checked against
each other at full precision rather than folded together, which is why this module reads
the faithful field and not the folded one.

WHAT "EQUAL" MEANS HERE.  A strand comes back as chanted verses of chanted words, split at
sof pasuq, plus the kind of each stroke in reading order.  Getting there normalizes away
five things, four of them identically on both sides:

* **ketiv/qere is resolved to the qere.**  Deut 5:9's מצותי is a ``כו״ק``; both sides take
  the reading, not the spelling.
* **The qamats variant is resolved to the ד form.**  ``מ:קמץ`` offers a qamats-qatan
  spelling (``ד``) and a plain-qamats one (``ס``); both sides take ``ד``, which is also what
  the vendored folding does.
* **Section divisions are dropped.**  Setumah/petuXah/pisqa markers survive on both sides
  but in different vocabularies (plus writes ``סס``/``ססס``/``פפ``, several of them in cell C
  rather than cell E; the Wikisource base page writes ``{{סס2}}``/``{{ססס}}``/``{{פפ}}``
  inline), so they are not comparable without a mapping this issue does not need.
* **MAM's documentation is dropped.**  ``נוסח`` param 2 is a manuscript note, plus-only.

The fifth is the one asymmetry, and it is the only difference the two sources actually
have.  They put a word's SAME-LETTER MARKS in different orders: MAM-parsed-plus keeps
MAM's own order (shin dot before the vowel, dagesh after it), while the Wikisource base
page is canonically ordered throughout.  It touches 284 of the 613 words and no mark is
added, dropped or altered by it -- only moved within its letter's own run -- so
``compare`` reads both sides in canonical order (NFC, which for Hebrew reorders and never
composes) and ``mark_order_differences`` hands back the untouched pairs so a test can
check that reordering is all that separates them.

What survives is the whole of what the pages actually claim: the chanted-verse
segmentation, every word with every mark on it (accents, vowels, meteg, maqaf, dagesh),
and legarmeh-vs-paseq for each stroke.
"""

from __future__ import annotations

import difflib
import json
import re
import unicodedata
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

from mb_cmn.hebrew_punctuation import PASOLEG
from mb_diff_mpu.mpplus_flatten import (
    is_parashah_template,
    is_std_kq_template,
    is_trivial_kq_template,
)
from mb_diff_mpu.mpplus_param_access import MISSING, get_param

from mb_cmn import paths

SOF_PASUQ = "\N{HEBREW PUNCTUATION SOF PASUQ}"
GERSHAYIM = "\N{HEBREW PUNCTUATION GERSHAYIM}"

BOOKS = ("ex", "dt")
READINGS = ("taxton", "elyon")
TRADITION = "manuscript"

# (plus filename, chapter, first verse, last verse) of each Decalogue, in MAM's own verse
# numbering -- which keeps the four short commandments as one numbered verse, so the Exodus
# Decalogue runs 20:2-13 rather than BHS's 20:2-17.  The bounding verses are checked against
# their opening words below, so a renumbering upstream fails loudly instead of silently
# shifting the span.
_SPANS: dict[str, tuple[str, str, int, int]] = {
    "ex": ("A2-Exodus.json", "20", 2, 13),
    "dt": ("A5-Deuter.json", "5", 6, 17),
}

# The letters of the first word of each span's first and last verse.
_SPAN_ANCHORS: dict[str, tuple[str, str]] = {
    "ex": ("אנכי", "לא"),
    "dt": ("אנכי", "ולא"),
}

# מ:כפול's single-strand params: ``א`` is the taxton, ``ב`` the elyon.
_STRAND_PARAM: dict[str, str] = {"taxton": "א", "elyon": "ב"}

# The vertical-stroke templates and the kind each asserts.  ``מ:לגרמיה`` is the vendored
# page's spelling and ``מ:לגרמיה-2`` the plus tree's; mpplus_flatten handles both too.
_STROKE_KINDS: dict[str, str] = {
    "מ:לגרמיה-2": "legarmeh",
    "מ:לגרמיה": "legarmeh",
    "מ:פסק": "paseq",
}

# The vendored page's section-division templates.  ``סס2`` is its own; the rest are the
# names mpplus_flatten's is_parashah_template already knows.
_VENDORED_DIVISIONS = frozenset({"סס2"})

_TEMPLATE_RE = re.compile(r"\{\{([^{}]*)\}\}")


@dataclass(frozen=True)
class Strand:
    """One (book, reading) m-trad strand, from whichever source produced it."""

    source: str  # "MAM-parsed-plus" / "vendored"
    book: str  # "ex" / "dt"
    reading: str  # "taxton" / "elyon"
    verses: tuple[tuple[str, ...], ...]  # chanted verses of chanted words
    stroke_kinds: tuple[str, ...]  # "legarmeh" / "paseq", in reading order

    @property
    def key(self) -> tuple[str, str]:
        return (self.book, self.reading)

    @property
    def label(self) -> str:
        return f"{self.book}/{self.reading}"

    @property
    def words(self) -> tuple[str, ...]:
        return tuple(w for verse in self.verses for w in verse)

    @property
    def canonical_verses(self) -> tuple[tuple[str, ...], ...]:
        """The verses with each word's marks in canonical order -- what ``compare`` reads.

        The two sources order a letter's own marks differently; see the module docstring.
        """
        return tuple(
            tuple(unicodedata.normalize("NFC", w) for w in verse)
            for verse in self.verses
        )


@dataclass(frozen=True)
class Difference:
    """One disagreement between the two sources, for one strand."""

    strand: str  # "<book>/<reading>"
    scope: str  # chanted_verse_count / verse_lengths / words / stroke_kinds
    where: str  # human-readable position
    mam_plus: str
    vendored: str

    def describe(self) -> str:
        return (
            f"{self.strand} {self.scope} at {self.where}: "
            f"MAM-parsed-plus {self.mam_plus} vs vendored {self.vendored}"
        )


# --------------------------------------------------------------------------- #
# Shared: text -> chanted verses
# --------------------------------------------------------------------------- #
def to_chanted_verses(text: str) -> tuple[tuple[str, ...], ...]:
    """Whitespace-split ``text`` into chanted verses of chanted words.

    A free-standing stroke folds onto the word before it (WLC's attached convention, and
    ``printed_decalogue._to_vels``'s); a chanted verse ends on the word bearing sof pasuq.
    Both readers pad every stroke with spaces before calling this, so the two sources'
    differing whitespace around a stroke cannot show up as a difference.
    """
    verses: list[tuple[str, ...]] = []
    current: list[str] = []
    for token in text.split():
        if token == PASOLEG:
            if not current:
                raise AssertionError("a chanted verse opens on a vertical stroke")
            current[-1] += PASOLEG
            continue
        current.append(token)
        if token.endswith(SOF_PASUQ):
            verses.append(tuple(current))
            current = []
    if current:
        raise AssertionError(f"trailing words with no sof pasuq: {current}")
    return tuple(verses)


def _padded_stroke() -> str:
    return f" {PASOLEG} "


def _letters(word: str) -> str:
    return "".join(c for c in word if "א" <= c <= "ת")


# --------------------------------------------------------------------------- #
# Source 1: MAM-parsed-plus
# --------------------------------------------------------------------------- #
@lru_cache(maxsize=None)
def _load_plus_book(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _param(tmpl: dict, key: str):
    value = get_param(tmpl, key)
    if value is MISSING:
        raise AssertionError(f"{tmpl['tmpl_name']}: no param {key!r}")
    return value


def _flatten(el, reading: str, parts: list[str], kinds: list[str]) -> None:
    """Append ``el``'s contribution to one strand's body text, tracking stroke kinds."""
    if isinstance(el, str):
        parts.append(el)
        return
    if isinstance(el, list):
        for item in el:
            _flatten(item, reading, parts, kinds)
        return
    if not isinstance(el, dict):
        raise AssertionError(f"unexpected cell-E element {el!r}")
    _flatten_template(el, reading, parts, kinds)


def _flatten_template(
    tmpl: dict, reading: str, parts: list[str], kinds: list[str]
) -> None:
    name = tmpl["tmpl_name"]
    if name == "מ:כפול":
        _flatten(_param(tmpl, _STRAND_PARAM[reading]), reading, parts, kinds)
        return
    if name in _STROKE_KINDS:
        kinds.append(_STROKE_KINDS[name])
        parts.append(_padded_stroke())
        return
    if is_parashah_template(name):
        parts.append(" ")  # a section division; dropped, see the module docstring
        return
    if name == "נוסח":
        _flatten(_param(tmpl, "1"), reading, parts, kinds)  # param 2 is MAM's own note
        return
    if is_std_kq_template(name):
        _flatten(_param(tmpl, "2"), reading, parts, kinds)  # the qere
        return
    if is_trivial_kq_template(name):
        _flatten(_param(tmpl, "1"), reading, parts, kinds)
        return
    if name == "מ:קמץ":
        _flatten(_param(tmpl, "ד"), reading, parts, kinds)
        return
    raise AssertionError(
        f"{name}: no rule for this template in the Decalogue span -- MAM-parsed-plus "
        "grew a construct this module does not know how to read"
    )


def _first_word(cell: list) -> str:
    parts: list[str] = []
    _flatten(cell, "taxton", parts, [])
    words = "".join(parts).split()
    return _letters(words[0]) if words else ""


def _decalogue_cells(book: str, plus_dir: Path) -> list[list]:
    """The cell-E arrays of the book's Decalogue verses, in order."""
    filename, chapter, first, last = _SPANS[book]
    chapters = _load_plus_book(plus_dir / filename)["book39s"][0]["chapters"]
    verses = chapters[chapter]
    cells = [verses[str(n)][2] for n in range(first, last + 1)]
    opening = (_first_word(cells[0]), _first_word(cells[-1]))
    if opening != _SPAN_ANCHORS[book]:
        raise AssertionError(
            f"{book}: {chapter}:{first}-{last} now opens {opening}, expected "
            f"{_SPAN_ANCHORS[book]} -- MAM-parsed-plus renumbered the chapter"
        )
    return cells


def from_mam_plus(book: str, reading: str, plus_dir: Path | None = None) -> Strand:
    """One m-trad Decalogue strand, read from the MAM-parsed-plus tree.

    ``plus_dir`` is the explicit path argument; defaulted, it resolves through
    ``mb_cmn.paths`` and is CHECKED there, so an absent sibling clone fails with the two
    overrides spelled out instead of a bare ``FileNotFoundError`` from ``_load_plus_book``.
    An explicitly passed path is not second-guessed -- the caller named it, and the advice
    ``require_sibling`` gives would be beside the point.
    """
    plus_dir = plus_dir or paths.require_mam_parsed_plus_dir()
    parts: list[str] = []
    kinds: list[str] = []
    for i, cell in enumerate(_decalogue_cells(book, plus_dir)):
        if i:
            # Consecutive numbered verses abut with no space of their own, and an elyon
            # chanted verse regularly runs across several of them.
            parts.append(" ")
        _flatten(cell, reading, parts, kinds)
    return Strand(
        source="MAM-parsed-plus",
        book=book,
        reading=reading,
        verses=to_chanted_verses("".join(parts)),
        stroke_kinds=tuple(kinds),
    )


# --------------------------------------------------------------------------- #
# Source 2: the vendored teamim JSON's faithful_chanted_verses
# --------------------------------------------------------------------------- #
def _resolve_wiki_template(body: str, kinds: list[str]) -> str:
    """One ``{{...}}`` body -> its contribution to the strand's text."""
    fields = body.split("|")
    name = fields[0].strip().replace('"', GERSHAYIM)
    named = dict(
        f.split("=", 1) for f in fields[1:] if "=" in f and not f.startswith("=")
    )
    positional = [f for f in fields[1:] if "=" not in f]
    if name in _STROKE_KINDS:
        kinds.append(_STROKE_KINDS[name])
        return _padded_stroke()
    if name in _VENDORED_DIVISIONS or is_parashah_template(name):
        return " "  # a section division; dropped, see the module docstring
    if name == "מ:קמץ":
        return named["ד"]
    if is_std_kq_template(name):
        return positional[1]  # the qere
    raise AssertionError(
        f"{name}: no rule for this template in the vendored faithful text -- the "
        "Wikisource base page grew a construct this module does not know how to read"
    )


def _resolve_faithful(verse: str, kinds: list[str]) -> str:
    out = _TEMPLATE_RE.sub(lambda m: _resolve_wiki_template(m.group(1), kinds), verse)
    if "{" in out or "}" in out:
        raise AssertionError(f"unresolved markup in vendored faithful text: {out!r}")
    return out


def _vendored_version(source: dict, book: str, reading: str) -> dict:
    return next(
        v
        for v in source["versions"]
        if (v["book"], v["reading"], v["tradition"]) == (book, reading, TRADITION)
    )


def from_vendored(source: dict, book: str, reading: str) -> Strand:
    """One m-trad Decalogue strand, read from the vendored ``faithful_chanted_verses``."""
    version = _vendored_version(source, book, reading)
    faithful = version.get("faithful_chanted_verses")
    if faithful is None:
        raise ValueError(
            f"{book}/{reading}: the vendored source has no faithful_chanted_verses -- "
            "re-vendor via printed_decalogue_fetch.py (issue wlc-utils#74)"
        )
    kinds: list[str] = []
    verses: list[tuple[str, ...]] = []
    for text in faithful:
        resolved = to_chanted_verses(_resolve_faithful(text, kinds))
        if len(resolved) != 1:
            raise AssertionError(
                f"{book}/{reading}: a faithful entry holds {len(resolved)} chanted "
                "verses, expected exactly one"
            )
        verses.append(resolved[0])
    return Strand(
        source="vendored",
        book=book,
        reading=reading,
        verses=tuple(verses),
        stroke_kinds=tuple(kinds),
    )


# --------------------------------------------------------------------------- #
# The comparison
# --------------------------------------------------------------------------- #
def mark_order_differences(
    plus: Strand, vendored: Strand
) -> list[tuple[int, str, str]]:
    """``(1-based word index, plus word, vendored word)`` wherever the raw words differ.

    Raw, i.e. before the canonical reordering ``compare`` applies -- so a caller can check
    for itself that reordering really is all that separates the two, rather than take
    ``compare``'s silence on trust.  Requires the two to have the same word count, which
    ``compare`` is what actually establishes.
    """
    if len(plus.words) != len(vendored.words):
        raise ValueError(
            f"{plus.label}: {len(plus.words)} plus words vs {len(vendored.words)} "
            "vendored -- compare() first"
        )
    return [
        (i, a, b)
        for i, (a, b) in enumerate(zip(plus.words, vendored.words), start=1)
        if a != b
    ]


def _word_locations(strand: Strand) -> list[str]:
    return [
        f"chanted verse {i}, word {j}"
        for i, verse in enumerate(strand.verses, start=1)
        for j, _ in enumerate(verse, start=1)
    ]


def _aligned_differences(
    label: str, scope: str, plus: list[str], vendored: list[str], where: list[str]
) -> list[Difference]:
    """Positional comparison, for sequences already known to be the same length.

    Used for the stroke kinds: difflib is free to align two equal-length runs of
    ``legarmeh``/``paseq`` as a delete plus an insert somewhere else entirely, which
    reports a reclassified stroke at two positions neither of which is the stroke.
    """
    return [
        Difference(strand=label, scope=scope, where=at, mam_plus=a, vendored=b)
        for a, b, at in zip(plus, vendored, where)
        if a != b
    ]


def _opcode_differences(
    label: str, scope: str, plus: list[str], vendored: list[str], where: list[str]
) -> list[Difference]:
    out: list[Difference] = []
    matcher = difflib.SequenceMatcher(a=plus, b=vendored, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            continue
        at = where[i1] if i1 < len(where) else (where[-1] + " (end)" if where else "-")
        out.append(
            Difference(
                strand=label,
                scope=scope,
                where=at,
                mam_plus=" ".join(plus[i1:i2]) or "(nothing)",
                vendored=" ".join(vendored[j1:j2]) or "(nothing)",
            )
        )
    return out


def compare(plus: Strand, vendored: Strand) -> list[Difference]:
    """Every disagreement between the two sources' reading of one strand.

    Words are read in canonical mark order; see ``Strand.canonical_verses``.
    """
    if plus.key != vendored.key:
        raise ValueError(f"comparing {plus.label} against {vendored.label}")
    label = plus.label
    plus_verses, vendored_verses = plus.canonical_verses, vendored.canonical_verses
    out: list[Difference] = []
    if len(plus_verses) != len(vendored_verses):
        out.append(
            Difference(
                strand=label,
                scope="chanted_verse_count",
                where="the strand",
                mam_plus=str(len(plus_verses)),
                vendored=str(len(vendored_verses)),
            )
        )
    out += _opcode_differences(
        label,
        "words",
        [w for verse in plus_verses for w in verse],
        [w for verse in vendored_verses for w in verse],
        _word_locations(plus),
    )
    out += _opcode_differences(
        label,
        "verse_lengths",
        [str(len(v)) for v in plus_verses],
        [str(len(v)) for v in vendored_verses],
        [f"chanted verse {i}" for i, _ in enumerate(plus_verses, start=1)],
    )
    plus_kinds, vendored_kinds = list(plus.stroke_kinds), list(vendored.stroke_kinds)
    kind_where = [f"stroke {i}" for i, _ in enumerate(plus_kinds, start=1)]
    differ = (
        _aligned_differences
        if len(plus_kinds) == len(vendored_kinds)
        else _opcode_differences
    )
    out += differ(label, "stroke_kinds", plus_kinds, vendored_kinds, kind_where)
    return out


def compare_all(source: dict, plus_dir: Path | None = None) -> list[Difference]:
    """Every disagreement, over all four (book, reading) m-trad strands."""
    return [
        d
        for book in BOOKS
        for reading in READINGS
        for d in compare(
            from_mam_plus(book, reading, plus_dir), from_vendored(source, book, reading)
        )
    ]
