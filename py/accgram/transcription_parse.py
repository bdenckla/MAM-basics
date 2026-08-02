r"""Feed a hand transcription's accents to the prose grammar checker (issue wlc-utils#52).

``printed_decalogue`` grammar-checks the eight IDEALIZED Wikisource strands: fed through
accgram's prose checker, are the printed- and manuscript-tradition Decalogue accentuations
grammatical?  This module asks the same question of what a REAL EDITION prints, by running
the committed hand transcriptions (``edition_transcription``) through the identical pipeline
-- ``printed_decalogue.parse_marks_body``, so the same scanner, the same grammar and the same
status vocabulary answer both.  Both Decalogues are prose; the poetic checker never applies.

WHY A TRANSCRIPTION CAN BE PARSED AT ALL.  A transcription is a stream of accent shorthand
(``mun``, ``zaq``, ``mun_leg``, ``qad+ger``, ``mun-mer``) and the scanner is described as
reading Hebrew text, so an adapter looked as though it might need pointed text the
transcription never captured.  It does not, because the scanner does not read pointed text
either: ``uni_to_marks`` first reduces a verse to a MARK BODY, in which every base letter is
one opaque placeholder and only accents, meteg, paseq, maqaf, space and sof pasuq survive.  A
transcription already records that alphabet minus meteg, so the body is built straight from
it -- one placeholder letter per accent, plus the punctuation the transcription does record.

DROPPING METEG IS HARMLESS, not merely tolerable.  Meteg's M-C digit set (``75``) blocks none
of the four trailing-context lookaheads the scanner rebuilds over the mark alphabet (see
``accent_marks.negated_class``), so its absence cannot change prose tokenization.  The one
place it is load-bearing is the verse-final silluq, and a transcription records that directly
as ``silsof``.  The claim is checked rather than asserted: for every transcription that
diverges from its Wikisource strand NOWHERE, the body built here reproduces that strand's scanner
token stream exactly, positional calls included -- azla vs. qadma, methiga-zaqef, mayela,
legarmeh, and the fused stress-helper pashta and telisha.  See ``test_edition_transcriptions``.

WHAT THIS ADDS OVER THE TOKEN DIFF.  ``edition_transcription.compare`` scores a divergence
accent by accent, and the test module pins whether it leaves the disjunctive skeleton intact.
Both are token-IDENTITY claims; neither says whether the resulting accent sequence is
GRAMMATICAL, and one divergence shows the two come apart.  SimTiq's Exodus appendix taxton
(p. 246) diverges from its Wikisource strand only in conjunctives -- the skeleton is untouched,
which is correct and pinned -- and its third chanted verse is ungrammatical all the same: the
page's
munax on the joined לא of לא־תעשה makes three servi where the grammar takes two, and the
pashta phrase fails.  That chanted verse is ungrammatical without qualification -- a fact about
the accent sequence, not an artifact of this checker.  It is not a verdict that the edition is
in error, and a clean rate is not the objective.

WHAT IT DOES NOT ADD is the legarmeh-vs-paseq distinction, which was once the reason to want
it.  The scanner's LEGARMEH call is purely POSITIONAL -- a munax + U+05C0 before a revia --
so it is blind to which kind an edition prints, exactly as the pre-wlc-utils#74 vendored data was.
The converse is what is worth having: BECAUSE the call is positional, the scanner supplies a
kind where an edition withholds one, which is the whole stroke inventory of the four Koren
transcriptions (Koren has the bar without saying which it is, so every one of its strokes
is transcribed ``[pasoleg]``, kind unspecified, and the round-trip against the reference
compares none of them).  ``scanner_pasoleg_kinds`` is that determination.

WHERE THE VERDICTS ARE RECORDED.  ``TranscriptionResult`` pairs each transcription's verdicts
with the strand's own, chanted verse by chanted verse, and ``payload_objs`` serializes them as
the ``transcriptions`` section of ``out/accgram/printed-decalogue/_printed_decalogue.json``,
beside the ``versions`` section holding the strands'.  The rendered statement of the same
verdicts is a column on each satellite page's per-Decalogue verdict table, whose shared prose
lives in ``transcription_verdict_column``.
"""

from __future__ import annotations

import dataclasses

from accgram import accent_marks as am
from accgram import edition_transcription as et
from accgram import printed_decalogue as pd
from accgram.prose_ply_grammar import build_parser
from accgram.prose_scanner import HasLegarmeh, scan_accents

# The shorthand a transcription is written in -> the Unicode mark to emit for it.  The
# inverse of ``edition_transcription.ACCENT_ABBREV``, which is many-to-one: ``zar`` stands
# for both U+0598 and U+05AE, and the scanner's ZARQA rule reads U+05AE as the accent with
# U+0598 as its optional stress helper, so U+05AE is the one to emit.  A prose geresh muqdam
# passes through as its own codepoint and the scanner normalizes it to a plain geresh, as it
# does for the two prose occurrences in WLC.
MARK_OF = {
    "etn": am.ATNAX,
    "seg": am.SEGOLTA,
    "zaq": am.ZAQEF_QATAN,
    "zaqg": am.ZAQEF_GADOL,
    "tip": am.TIPEXA,
    "rev": am.REVIA,
    "zar": am.TSINNOR,
    "pash": am.PASHTA,
    "yet": am.YETIV,
    "tev": am.TEVIR,
    "ger": am.GERESH,
    "germ": am.GERESH_MUQDAM,
    "ger2": am.GERSHAYIM,
    "tg": am.TELISHA_GEDOLA,
    "paz": am.PAZER,
    "mun": am.MUNAX,
    "mah": am.MAHAPAKH,
    "mer": am.MERKHA,
    "mer2": am.MERKHA_KEFULA,
    "dar": am.DARGA,
    "qad": am.QADMA,
    "tq": am.TELISHA_QETANA,
}

# The mark that closes a chanted verse.  ``silsof`` is one token on the transcription side --
# silluq and sof pasuq are never apart -- and two marks here, which is also what makes the
# scanner's SILLUQ rule fire: it wants a meteg immediately before a sof pasuq.
SILSOF_MARKS = am.METEG + am.SOF_PASUQ


def _accent_marks(accent: str) -> str:
    """One written accent (an alias resolved, ``mun_leg`` included) -> its mark(s)."""
    head, _, tail = accent.partition(et.UNIT_JOINER)
    head = et.ALIASES.get(head, head)
    if head == "silsof":
        if tail:
            raise ValueError(f"silsof takes no modifier: {accent!r}")
        return SILSOF_MARKS
    try:
        marks = MARK_OF[head]
    except KeyError:
        raise ValueError(f"unknown accent shorthand {head!r} in {accent!r}") from None
    if not tail:
        return marks
    if tail != "leg":
        raise ValueError(f"unknown modifier {tail!r} in {accent!r}")
    # Legarmeh is the accent plus a stroke on the same word, which is exactly the shape the
    # scanner's LEGARMEH rule matches.  Whether it CALLS it legarmeh is its own decision,
    # taken from the following revia and not from this transcription's claim.
    return marks + am.PASEQ


def chunk_to_marks(chunk: str) -> str:
    """One written chunk -> its mark fragment: ONE placeholder letter per accent.

    A word bearing more than one accent keeps the joiner that says which kind of word it is:
    ``mun-mer`` emits a maqaf between its two accents, so the compound stays one chanted word
    for the ``TEXT`` class and the lexical layer, while ``qad+ger`` emits none, being one
    simple word already.

    One letter per accent is a deliberate simplification and the one limit of this adapter:
    the transcriptions' ``+`` means two accents on one WORD, never on one LETTER, so a
    same-letter pair cannot be expressed and the scanner's fused MAHAPAKHQADMA token cannot
    arise from a transcription.  No such pair occurs -- ``qad+ger`` is the corpus's only
    ``+`` -- but a page that printed one would need a notation before it could be parsed.
    """
    frag = ""
    for accent, joiner in et.split_on_joiners(chunk, et.WRITTEN_ACCENT_JOINERS):
        if joiner == et.MAQAF_JOINER:
            frag += am.MAQAF
        frag += am.LETTER + _accent_marks(accent)
    return frag


def chanted_verses(
    transcription: et.Transcription,
) -> list[tuple[tuple[str, ...], str]]:
    """A transcription -> ``(written chunks, scanner mark body)`` per chanted verse.

    Chanted words are space-separated and a verse closes where a word's marks end in sof
    pasuq, mirroring how ``edition_transcription._accent_tokens`` finds the same boundaries
    on the reference side.  A pasoleg aside is folded onto the word it follows, matching both
    WLC's attached convention and ``printed_decalogue._to_vels``; a positional aside such as
    ``[p. 298]`` carries no mark and is skipped.

    The chunks are folded the same way -- ``mer [paseq]`` is one entry, not two -- so a verse's
    chunks stand one for one against its body's chanted words, and can be carried as the
    ``words`` of a ``ChantedVerseResult`` where a strand carries pointed Hebrew.
    """
    verses: list[tuple[tuple[str, ...], str]] = []
    words: list[tuple[str, str]] = []
    for chunk in transcription.chunks:
        if chunk.startswith("["):
            if chunk in et.PASOLEG_ASIDES and words:
                written, marks = words[-1]
                words[-1] = (f"{written} {chunk}", marks + am.PASEQ)
            continue
        words.append((chunk, chunk_to_marks(chunk)))
        if words[-1][1].endswith(am.SOF_PASUQ):
            verses.append(_verse(words))
            words = []
    if words:
        verses.append(_verse(words))
    return verses


def _verse(words: list[tuple[str, str]]) -> tuple[tuple[str, ...], str]:
    return tuple(w for w, _ in words), " ".join(marks for _, marks in words)


def chanted_verse_bodies(transcription: et.Transcription) -> list[str]:
    """A transcription -> one scanner mark body per chanted verse."""
    return [body for _, body in chanted_verses(transcription)]


def check(transcription: et.Transcription, parser=None) -> list[pd.ChantedVerseResult]:
    """Every chanted verse of one transcription, fed to the prose grammar.

    The records are ``printed_decalogue``'s own, so a transcription's verdicts sit beside its
    Wikisource strand's and can be compared field for field.  ``words`` holds the written chunks
    rather than Hebrew words: a transcription has no Hebrew to carry.
    """
    parser = parser or build_parser()
    book = transcription.header["book"]
    return [
        pd.parse_marks_body(body, book, i, parser, chunks)
        for i, (chunks, body) in enumerate(chanted_verses(transcription), start=1)
    ]


# --------------------------------------------------------------------------- #
# One transcription's verdicts, beside its Wikisource strand's (issue wlc-utils#52)
# --------------------------------------------------------------------------- #
@dataclasses.dataclass(frozen=True)
class TranscriptionResult:
    """One hand transcription's grammar verdicts, paired with its Wikisource strand's own.

    The pairing is the point: a page's verdict is only ever interesting against the verdict of
    the Wikisource strand it follows, since four of the twelve transcribed Decalogues follow a
    strand that is itself ungrammatical at its opening chanted verse (the p-trad עליון's merged
    first two commandments).  So "ungrammatical somewhere" is not the finding; ``departures`` is.
    """

    stem: str  # the transcription's filename stem, e.g. "simtiq_ex_taxton"
    edition: str
    pages: str
    key: tuple[str, str, str]  # (book, reading, tradition) -- the strand followed
    chanted_verses: tuple[pd.ChantedVerseResult, ...]
    strand_statuses: tuple[str, ...]  # the strand's own status, verse for verse

    @property
    def ungrammatical(self) -> tuple[pd.ChantedVerseResult, ...]:
        return tuple(cv for cv in self.chanted_verses if cv.status != "clean")

    @property
    def departures(self) -> tuple[tuple[int, str, str], ...]:
        """``(1-based chanted verse, the strand's status, this page's status)``, where they differ."""
        return tuple(
            (cv.index, strand, cv.status)
            for cv, strand in zip(self.chanted_verses, self.strand_statuses)
            if cv.status != strand
        )


def strand_key(strand: pd.VersionResult) -> tuple[str, str, str]:
    """A strand's ``(book, reading, tradition)`` triple -- the form a transcription's key takes."""
    return (strand.book, strand.reading, strand.tradition)


def check_one(
    transcription: et.Transcription, strand: pd.VersionResult, parser=None
) -> TranscriptionResult:
    """One transcription against one strand, chanted verse by chanted verse.

    A chanted verse count that disagrees with the strand's raises rather than being compared
    position by position: a moved boundary would line the two status lists up by accident and
    make every verdict after it a comparison of different verses.  Every committed
    transcription has its Wikisource strand's own count, and ``test_edition_transcriptions``
    pins that independently, so this is a drift guard rather than a case to handle.
    """
    got = tuple(check(transcription, parser))
    want = tuple(cv.status for cv in strand.chanted_verses)
    if len(got) != len(want):
        raise AssertionError(
            f"{transcription.path.stem}: {len(got)} chanted verses against "
            f"{et.strand_name(strand_key(strand))}'s {len(want)} -- a boundary moved, so the "
            "verdicts cannot be compared verse for verse"
        )
    return TranscriptionResult(
        stem=transcription.path.stem,
        edition=transcription.header.get("edition", "?"),
        pages=transcription.header.get("pages", "?"),
        key=transcription.key,
        chanted_verses=got,
        strand_statuses=want,
    )


def check_all(
    strands: list[pd.VersionResult], parser=None
) -> list[TranscriptionResult]:
    """Every committed transcription against the strand its header names, in filename order."""
    parser = parser or build_parser()
    by_key = {strand_key(vr): vr for vr in strands}
    out: list[TranscriptionResult] = []
    for transcription in et.load_all_transcriptions():
        strand = by_key.get(transcription.key)
        if strand is None:
            raise AssertionError(
                f"{transcription.path.stem}: no vendored strand "
                f"{et.strand_name(transcription.key)} to compare against"
            )
        out.append(check_one(transcription, strand, parser))
    return out


def _chanted_verse_obj(
    cv: pd.ChantedVerseResult, strand_status: str
) -> dict[str, object]:
    """One chanted verse, shaped as ``printed_decalogue._version_obj`` shapes a strand's.

    ``words`` holds the written chunks rather than pointed Hebrew (see ``check``), and
    ``strand_status`` is the extra field a transcription has and a strand does not: the verdict
    of the strand at the same chanted verse, so a departure is readable off one entry.
    """
    return {
        "index": cv.index,
        "words": list(cv.words),
        "marks": cv.body,
        "tokens": list(cv.tokens),
        "status": cv.status,
        "strand_status": strand_status,
        **cv.chanted_word_accents_obj(),
        "tree": cv.tree,
    }


def _transcription_obj(result: TranscriptionResult) -> dict[str, object]:
    book, reading, tradition = result.key
    return {
        "stem": result.stem,
        "edition": result.edition,
        "pages": result.pages,
        "book": book,
        "reading": reading,
        "tradition": tradition,
        "chanted_verse_count": len(result.chanted_verses),
        "ungrammatical_count": len(result.ungrammatical),
        "departures": [
            {"index": index, "strand_status": strand, "status": status}
            for index, strand, status in result.departures
        ],
        "chanted_verses": [
            _chanted_verse_obj(cv, strand)
            for cv, strand in zip(result.chanted_verses, result.strand_statuses)
        ],
    }


def payload_objs(results: list[TranscriptionResult]) -> list[dict[str, object]]:
    """The ``transcriptions`` section of ``_printed_decalogue.json``.

    Kept here rather than in ``printed_decalogue`` so that module needs no import of this one
    (this one imports it, for the shared parse path), and so the section's shape sits beside the
    record it serializes.
    """
    return [_transcription_obj(r) for r in results]


def token_types(body: str, book: str) -> tuple[str, ...]:
    """The scanner's token-type stream for one mark body, TILDE excluded.

    Comparable directly with a ``ChantedVerseResult.tokens`` minus its leading TILDE, which
    is what makes the reference-side control check a one-liner.
    """
    return tuple(t.type for t in scan_accents(body, book, 20, 2, HasLegarmeh()))


def scanner_pasoleg_kinds(transcription: et.Transcription) -> list[str]:
    """The scanner's kind for each pasoleg stroke of a transcription, in reading order.

    ``legarmeh`` where the scanner's positional rule fires -- a munax + stroke before a revia
    -- and ``paseq`` where it does not, the stroke then being swallowed.  This is a
    determination the transcription itself may decline to make: Koren does not distinguish
    the two in print, so all fourteen of its strokes are transcribed kind-unspecified.

    Each stroke is judged with the OTHERS REMOVED, which is sound rather than merely
    convenient: a stroke does not block the legarmeh lookahead's character class, so no
    stroke's call depends on another's presence, and removing them keeps a one-or-zero answer
    per stroke instead of having to align a count of LEGARMEH tokens back onto positions.
    """
    book = transcription.header["book"]
    kinds: list[str] = []
    for body in chanted_verse_bodies(transcription):
        for k in range(body.count(am.PASEQ)):
            kinds.append("legarmeh" if _is_legarmeh(body, k, book) else "paseq")
    return kinds


def _is_legarmeh(body: str, keep: int, book: str) -> bool:
    """Does the scanner call the ``keep``-th stroke of ``body`` a legarmeh?"""
    kept: list[str] = []
    seen = 0
    for ch in body:
        if ch == am.PASEQ:
            if seen == keep:
                kept.append(ch)
            seen += 1
        else:
            kept.append(ch)
    return "LEGARMEH" in token_types("".join(kept), book)
