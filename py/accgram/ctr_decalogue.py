"""Place CTR's two Decalogues among the idealized strands -- the wlc-utils#69 question, for a DIGITAL
edition rather than a hand transcription.

CTR (``ctr_decalogue_fetch.py``) is a VENDORED STRAND: digital, accent-exact Hebrew, so its
marks are compared mechanically against the reference ``printed_decalogue_teamim.json`` rather
than read off a page.  What it turns out to follow is the surprise this module reports:

* CTR's **Exodus 20** has the ta'am **elyon** accents (not the taxton the running text was
  expected to hold) under a punctuation that is NEITHER strand's: sixteen sof pasuqs, the exact
  UNION of the two strands' boundaries (the elyon's 9 and the taxton's 13, sharing 6).  Nothing
  was re-accented to fit them.  At the 9 elyon boundaries CTR has the elyon's silluq; at the 7
  taxton-only ones it has no silluq at all, the mark standing after the elyon's own mid-verse
  disjunctive (revia, revia, revia, atnaxta, revia, segolta, zaqef, on עבדים / על־פני / לארץ /
  לשנאי / לקדשו / כל־מלאכתך / בשעריך).  So only 9 of the 16 are chanted verses; see the naming
  section below.
* CTR's **Deuteronomy 5** is the **taxton**, chanted-verse division and all: thirteen, matching
  ws/dt/taxton/printed boundary for boundary, which is why that book is clean where Exodus is not.

SAY "SOF PASUQ SPAN", NOT "CHANTED VERSE", FOR THE SIXTEEN (Ben, 2026-07-24).  A chanted verse is
a well-formed cantillation unit, which minimally means a SILLUQ on the last word before the sof
pasuq; a span that, in Ben's words, "doesn't even seem to be trying to obey the rules of
cantillation" is only a sof pasuq span.  Splitting at the mark and calling every result a chanted
verse -- which this module did -- begs the question for exactly the seven spans that are the
finding.  ``sof_pasuq_spans`` is named for this, and ``span_silluq_status`` is what checks it.

The claim the page makes needs that check to be REAL: "the accents are the elyon's, silluq
included, but the punctuation is neither strand's" invites the objection that sinks a sloppier
version of it -- silluq IS an accent, so a genuine re-division would have MOVED the silluqs and
the two halves could not come apart.  They come apart here only because CTR moved nothing.  Note
that the glyph comparison below cannot see this on its own: ``word_glyphs`` drops U+05BD, so
139/142 is silluq-BLIND and would agree just as happily if CTR had re-silluqed the seven.

STATE THE DIVISION IN CHANTED VERSES OR SPANS, NEVER IN NUMBERED ONES.  An earlier draft of the
two bullets above described the Exodus division as "the ordinary numbered-verse division -- a sof
pasuq at every numbered verse".  That is both off-subject and false.  Off-subject because these
pages and this comparison are about chanted verse structure only, numbering being a different
concept (Ben, 2026-07-24).  False because Exodus 20:13 holds FOUR sof pasuqs, which is exactly
where three of the sixteen come from -- ``sof_pasuq_spans`` below says so, and the file
contradicted itself for as long as both texts stood.  Issue wlc-utils#69's Result 11 carried the same
phrasing and was corrected with this.

WHY THE COMPARISON IS AT THE GLYPH LEVEL, NOT THE ACCENT LEVEL.  The eight paper Decalogues of
wlc-utils#69 were HAND transcriptions: a reader resolved each mark to an accent, distinguishing a qadma
from a pashta or a yetiv from a mahapakh by grammar and position -- a distinction the two
members of each pair do NOT draw graphically.  CTR gives no such reading.  Worse, its encoding
is nonstandard (see MAM-basics' review of CTR, ``rocc_2_pre_vowel_accents_in_ctr``): it reuses
one code point for a lookalike pair and leans on vowel-relative order, so its bytes recover the
GLYPH reliably but not always the accent.  So CTR is compared at the resolution its data
actually supports -- the visible mark -- by folding each lookalike pair onto one glyph:

    qadma == pashta,  yetiv == mahapakh,  geresh muqdam == geresh   (tipexa/dexi is poetic-only)

This is not a workaround that hides differences: the accents that DISCRIMINATE elyon from taxton
and p-trad from m-trad (geresh vs pazer, revia vs telisha gedola, zaqef vs revia, and the
chanted-verse boundaries) are not lookalike pairs, so folding the pairs leaves every
discriminator intact.  What the fold gives up is exactly the azla-vs-pashta and
mahapakh-vs-yetiv distinction CTR could not have expressed anyway.

WHAT THE VERDICT CLAIMS.  Only what wlc-utils#69 says survives every transcription -- the chanted-verse
boundaries plus the disjunctive skeleton -- read at the glyph level.  CTR's marks agree with
ex/elyon (Exodus) and dt/taxton (Deuteronomy) at all but a few words, and every disagreement is
CONJUNCTIVE: a munax CTR has on a non-final atom of a maqaf compound where the strand has a
meteg, or a munax/merkha swap.  None touches a disjunctive.  The cross-strand re-run -- the same
comparison against the OTHER tradition -- is where the evidence is: agreement collapses, which is
what rules out the clean match being an artifact of the fold.

ONE SCALE HERE TOO, AND THE MAQAFS AGREE (issue wlc-utils#76).  A maqaf sits at the bottom of the same
scale as the accents rather than in a ledger of its own -- it has the weakest SEPARATING force
there is, which is the opposite of being loose, since a maqaf binds its two atoms tightest.
(``printed_decalogue_strands``' ``MAQAF_IS_THE_LAST_RUNG`` states this to the reader, and its
guardrail comment records the second-ledger convention it replaced.)  This comparison already
works that way and needs no rewording: ``compare`` splits each reading on whitespace, so a maqaf
compound is ONE word on both sides, and a maqaf CTR placed otherwise than the Wikisource strand
would break the skeleton alignment and be reported, not quietly excused.  Re-derived 2026-07-26, it never
has to be: the two sides segment into the same words (142 against 142 in Exodus, 164 against
164 in Deuteronomy) and their maqafs match word for word and slot for slot, 27 compounds against
27 and 24 against 24.  So all four residuals are accent differences and nothing else.

Note what the two compound ones are, but do not lean on them: on יהיה־לך and on ובנך־ובתך the
strand has a meteg on the non-final atom and CTR a munax there instead, which is a second accent
on a chanted word.  That is worth recording about CTR and is NOT a precedent for anything -- CTR
is a nonstandard digital encoding this module already distrusts enough to compare at glyph level,
so it is evidence about CTR and about nothing else (Ben, 2026-07-26).  A prose compound carrying
an accent on a non-final atom is rare and wants real evidence; ``edition_transcription``'s "HOW
RARE THAT IS IN PROSE" paragraph is where that stands, along with the printed editions' own
cases, which are primary observation off a page and do carry weight.
"""

from __future__ import annotations

import argparse
import dataclasses
import difflib
import json
from pathlib import Path

from mb_cmn import paths

from accgram import edition_transcription as et
from accgram import printed_decalogue as pd
from accgram import printed_decalogue_strands as pds

COLON = "\N{COLON}"
VBAR = "\N{VERTICAL LINE}"
SOF_PASUQ = "\N{HEBREW PUNCTUATION SOF PASUQ}"
PASEQ = "\N{HEBREW PUNCTUATION PASEQ}"
# One codepoint, two readings -- meteg or silluq, told apart by context, never by the bytes.
# ``_has_silluq`` is this module's context rule; ``meteg_silluq_context`` is the corpus-wide one.
MTGOSLQ = "\N{HEBREW POINT METEG}"

# Which reference strand each book is compared against first, and which is the cross-strand
# re-run whose collapse is the evidence.  Both are the PRINTED tradition (the p-trad edition).
PRIMARY = {"ex": "elyon", "dt": "taxton"}
CROSS = {"ex": "taxton", "dt": "elyon"}

# Fold each lookalike pair onto one glyph label (the label is arbitrary; only the grouping
# matters).  Everything not here is its own glyph.  See the module docstring.
_GLYPH = {"qad": "pash", "pash": "pash", "yet": "mah", "mah": "mah", "germ": "ger"}

# Unambiguously conjunctive accents.  ``qad`` is not here -- it folds onto ``pash``, whose
# member pashta is disjunctive -- and ``tq`` (telisha qetana) is, distinct from ``tg`` (telisha
# gedola, disjunctive).  Removing these from a word's glyphs leaves its disjunctive skeleton,
# which is what a difference has to leave intact to count as conjunctive-only.
_CONJUNCTIVE_GLYPHS = {"mun", "mer", "mer2", "dar", "tq"}


def default_ctr_path() -> Path:
    return paths.in_dir() / "accgram" / "ctr_decalogue.json"


def load_ctr(path: Path | None = None) -> dict:
    path = path or default_ctr_path()
    return json.loads(path.read_text(encoding="utf-8"))


def _normalize(verse: str) -> str:
    """CTR's own punctuation onto the reference's: colon -> sof pasuq, vertical bar -> pasoleg.

    The accents are left as CTR encodes them; folding the lookalike pairs happens per glyph in
    ``word_glyphs``, not here, so the normalized text still carries CTR's real code points.
    """
    verse = verse.replace(" " + VBAR, PASEQ).replace(VBAR, PASEQ)
    return verse.replace(COLON, SOF_PASUQ)


def sof_pasuq_spans(ctr: dict, book: str) -> list[str]:
    """CTR's Decalogue for one book split at sof pasuq -- SPANS, not necessarily chanted verses.

    The neutral name is the point: this splits at the MARK and claims nothing about
    chantability.  A chanted verse needs a silluq before its sof pasuq, and CTR's Exodus has
    sixteen sof pasuqs over an accent stream supplying only nine silluqs, so seven of its spans
    close on a mid-verse disjunctive and are no kind of verse (see the module docstring and
    ``span_silluq_status``).  Deuteronomy's thirteen spans all have a silluq, so there they are
    chanted verses.

    Splitting is still the right recovery step: Exodus 20:13 has three prohibitions each with
    its own colon, so a numbered verse is not a span either.
    """
    verses = ctr["chapters"][book]["decalogue_verses"]
    joined = " ".join(_normalize(verses[k]) for k in verses)
    out: list[str] = []
    cur: list[str] = []
    for ch in joined:
        cur.append(ch)
        if ch == SOF_PASUQ:
            out.append("".join(cur).strip())
            cur = []
    tail = "".join(cur).strip()
    if tail:
        out.append(tail)
    return out


def word_glyphs(word: str) -> tuple[str, ...]:
    """One pointed CHANTED word -> its accent GLYPHS in order, lookalike pairs folded, repeats
    collapsed.  (Chanted word, not atom: ``_flat`` splits on whitespace, so a maqaf compound
    arrives whole and both its atoms' accents are counted here -- issue wlc-utils#81.)

    A doubled postpositive (the accent written at the chanted word's edge and again on the stressed
    syllable) is one glyph, as in ``_accent_tokens``.  A meteg/silluq (U+05BD) is not an accent
    and contributes no glyph, so a verse-final chanted word contributes its accent if any
    and nothing for the silluq -- the chanted-verse boundary is counted separately.
    """
    out: list[str] = []
    prev = None
    for ch in word:
        abbrev = et.ACCENT_ABBREV.get(ch)
        if abbrev is None:
            continue
        glyph = _GLYPH.get(abbrev, abbrev)
        if glyph == prev:
            continue
        prev = glyph
        out.append(glyph)
    return tuple(out)


def _has_silluq(word: str) -> bool:
    """True when this span-final word's U+05BD reads as a silluq rather than an ordinary meteg.

    The context rule, at the resolution this data supports: a silluq is the mark that CLOSES the
    word, so a U+05BD with no accent after it inside the word is a silluq, and one
    with an accent still to come is a meteg.  CTR's לְשֽׂנְאָ֑י is the case that needs the rule --
    its U+05BD sits two letters in, before an etnaxta, so the word has a meteg and no silluq,
    and mere PRESENCE of U+05BD would have called it verse-final.  (Scoped to span-final words
    of these Decalogues; ``meteg_silluq_context.u05bd_is_silluq`` is the corpus-wide version.)
    """
    if MTGOSLQ not in word:
        return False
    return not word_glyphs(word.rsplit(MTGOSLQ, 1)[1])


@dataclasses.dataclass(frozen=True)
class SpanSilluq:
    """One sof pasuq span, judged on the only thing that makes it a chanted verse: a silluq."""

    last_word: str
    skeleton: str
    has_silluq: bool
    final_glyphs: tuple[str, ...]

    @property
    def is_chanted_verse(self) -> bool:
        return self.has_silluq


def span_silluq_status(ctr: dict, book: str) -> tuple[SpanSilluq, ...]:
    """Per sof pasuq span: does its last word have a silluq -- i.e. is it a chanted verse at all?

    This is what keeps the page's claim honest.  ``word_glyphs`` drops U+05BD, so the glyph
    comparison is silluq-blind and would report the same 139/142 whether or not CTR had moved
    the silluqs to its own sixteen boundaries.  It did not, and this is where that is checked.
    """
    out: list[SpanSilluq] = []
    for span in sof_pasuq_spans(ctr, book):
        word = span.split()[-1]
        out.append(
            SpanSilluq(
                last_word=word,
                skeleton=pds.base_skeleton(word),
                has_silluq=_has_silluq(word),
                final_glyphs=word_glyphs(word),
            )
        )
    return tuple(out)


def _flat(verses: list[str]) -> list[tuple[str, tuple[str, ...]]]:
    """(consonant skeleton, glyph tuple) per chanted word across a reading's spans.

    Splitting on whitespace really does give CHANTED words, not atoms: a maqaf compound has
    no space in it, so it comes through whole (issue wlc-utils#81)."""
    return [(pds.base_skeleton(w), word_glyphs(w)) for v in verses for w in v.split()]


def _skeleton_glyphs(glyphs: tuple[str, ...]) -> tuple[str, ...]:
    """A chanted word's glyphs with the conjunctives dropped: its disjunctive skeleton at glyph level."""
    return tuple(g for g in glyphs if g not in _CONJUNCTIVE_GLYPHS)


@dataclasses.dataclass(frozen=True)
class WordDiff:
    """One chanted word where CTR's glyphs differ from the strand's."""

    skeleton: str
    ctr: tuple[str, ...]
    strand: tuple[str, ...]

    @property
    def conjunctive_only(self) -> bool:
        """True when the two agree on the disjunctive skeleton -- the difference is conjunctive."""
        return _skeleton_glyphs(self.ctr) == _skeleton_glyphs(self.strand)


@dataclasses.dataclass(frozen=True)
class Comparison:
    book: str
    reading: str
    # Counts of CHANTED words (``_flat``'s unit), not of atoms: a maqaf compound counts once.
    ctr_words: int
    strand_words: int
    agree: int
    diffs: tuple[WordDiff, ...]

    @property
    def disjunctive_skeleton_intact(self) -> bool:
        return all(d.conjunctive_only for d in self.diffs)


def compare(ctr: dict, source: dict, book: str, reading: str) -> Comparison:
    """Glyph-level word-by-word comparison of CTR's ``book`` against one printed strand.

    Aligns by consonant skeleton (difflib), so a differently placed maqaf shows up as an aligned
    region rather than shifting every accent after it, then compares the glyph tuples of the
    words that line up.  Chanted words that do NOT line up are recorded from both sides: a
    CTR-side chanted word against a placeholder strand tuple, and a strand-side chanted word
    against a placeholder CTR tuple.  A placeholder never equals a real glyph tuple, so an
    unaligned chanted word is a diff that also fails ``conjunctive_only`` -- loud, never silent.
    """
    ctr_flat = _flat(sof_pasuq_spans(ctr, book))
    version = next(
        v
        for v in source["versions"]
        if v["book"] == book and v["reading"] == reading and v["tradition"] == "printed"
    )
    strand_flat = _flat(version["chanted_verses"])

    a = [s for s, _ in ctr_flat]
    b = [s for s, _ in strand_flat]
    matcher = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    agree = 0
    diffs: list[WordDiff] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                cs, cg = ctr_flat[i1 + k]
                _, sg = strand_flat[j1 + k]
                if cg == sg:
                    agree += 1
                else:
                    diffs.append(WordDiff(cs, cg, sg))
        else:
            # An unaligned region has two sides, and both are recorded: a "delete" or
            # "replace" opcode has CTR-side chanted words (``i1..i2``), an "insert" or
            # "replace" strand-side ones (``j1..j2``).  Recording only the CTR side, as this
            # loop once did, would leave a chanted word the strand has and CTR lacks out of
            # ``diffs`` -- and out of the pinned counts -- entirely.  Moot at HEAD (the two
            # sides align word for word, so no opcode reaches here), and kept honest for the
            # re-vendor that would change that.
            for x in range(i1, i2):
                cs, cg = ctr_flat[x]
                diffs.append(WordDiff(cs, cg, ("<no aligned strand word>",)))
            for y in range(j1, j2):
                ss, sg = strand_flat[y]
                diffs.append(WordDiff(ss, ("<no aligned CTR word>",), sg))
    return Comparison(
        book=book,
        reading=reading,
        ctr_words=len(ctr_flat),
        strand_words=len(strand_flat),
        agree=agree,
        diffs=tuple(diffs),
    )


def strand_chanted_verse_count(source: dict, book: str, reading: str) -> int:
    version = next(
        v
        for v in source["versions"]
        if v["book"] == book and v["reading"] == reading and v["tradition"] == "printed"
    )
    return sum(1 for cv in version["chanted_verses"] if cv.rstrip().endswith(SOF_PASUQ))


def _report_book(ctr: dict, source: dict, book: str) -> None:
    primary, cross = PRIMARY[book], CROSS[book]
    cmp_primary = compare(ctr, source, book, primary)
    cmp_cross = compare(ctr, source, book, cross)
    spans = span_silluq_status(ctr, book)
    n_cv = len(spans)
    chanted = [s for s in spans if s.is_chanted_verse]

    print(f"\n===== CTR {book.upper()} =====")
    print(f"  sof pasuq spans: CTR {n_cv}")
    print(
        f"     of which chanted verses (silluq before the mark): {len(chanted)}"
        f" -- {n_cv - len(chanted)} span(s) close on no silluq"
    )
    for s in spans:
        if not s.is_chanted_verse:
            print(f"        {s.skeleton:26s} closes on {s.final_glyphs}, no silluq")
    for reading in (primary, cross):
        print(
            f"     strand {book}/{reading}/printed chanted verses: "
            f"{strand_chanted_verse_count(source, book, reading)}"
        )
    for label, cmp in (
        (f"PRIMARY {primary}", cmp_primary),
        (f"cross {cross}", cmp_cross),
    ):
        total = cmp.agree + len(cmp.diffs)
        print(
            f"  vs {label:16s}: glyph-agree {cmp.agree}/{total}"
            f"  ({len(cmp.diffs)} word diffs)"
        )
    print(
        f"  disjunctive skeleton intact vs {primary}: {cmp_primary.disjunctive_skeleton_intact}"
    )
    print(f"  the {len(cmp_primary.diffs)} residual difference(s) vs {primary}:")
    for d in cmp_primary.diffs:
        kind = "conjunctive-only" if d.conjunctive_only else "TOUCHES DISJUNCTIVE"
        print(f"     {d.skeleton:26s} CTR={d.ctr}  {primary}={d.strand}  [{kind}]")

    total = cmp_primary.agree + len(cmp_primary.diffs)
    strand_cv = strand_chanted_verse_count(source, book, primary)
    # The Exodus branch is the finding: same accents, MORE sof pasuqs, and the surplus ones with
    # no silluq under them.  Say punctuation, not "its own verse division" -- CTR did not divide
    # the text a third way, it laid the union of both strands' marks over one strand's accents.
    division = (
        "same chanted verse division"
        if n_cv == strand_cv
        else (
            f"but its own punctuation ({n_cv} sof pasuq spans over the strand's"
            f" {strand_cv} chanted verses, {n_cv - len(chanted)} of them closing on no silluq)"
        )
    )
    print(
        f"  VERDICT: CTR {book} follows {book}/{primary}/printed at the glyph level "
        f"({cmp_primary.agree}/{total} words, disjunctive skeleton intact, "
        f"{len(cmp_primary.diffs)} conjunctive residual(s)), {division}."
    )


def main() -> None:
    import sys

    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(
        description="Report CTR's Decalogues against the strands."
    )
    parser.add_argument("--ctr", type=Path, default=None)
    parser.add_argument("--source", type=Path, default=None)
    args = parser.parse_args()

    ctr = load_ctr(args.ctr)
    source = pd.load_source(args.source or pd.default_source_path())
    print(
        f"CTR retrieved {ctr['provenance']['retrieved']} -- {ctr['provenance']['edition']}"
    )
    for book in ("ex", "dt"):
        _report_book(ctr, source, book)


if __name__ == "__main__":
    main()
