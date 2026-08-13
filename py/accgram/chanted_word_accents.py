r"""Survey: chanted words with two or more accent TOKENS, over the prose verses of the Tanakh.

A chanted word normally has one accent.  ``maqaf_nonfinal_accents`` measured one corner of the
exceptions -- an accent on a non-final atom of a maqaf compound -- and left the larger half
unmeasured, because a chanted word can also have two accents while being a single atom, and can
have both of them on a compound's final atom.  This module measures all of it, and sets Yeivin's
own inventory of the phenomenon beside the measurement so each checks the other.

Pure computation and a JSON writer -- no HTML, and DELIBERATELY none.  Run via
``main_accgram.py survey-chanted-word-accents``.  A rendered page of this was built and then
dropped (2026-07-29): ``maqaf-nonfinal-accents.html`` had meanwhile widened to ask the same
question of all three printed compounds, and the plan's own thrust is a chanted-word rule in the
checker rather than a page.  The Yeivin cross-check is recorded here, in the JSON, which is the
form it wanted.  Issue wlc-utils#86 holds the questions the survey raises and does not settle.

THE SURVEY AND THE FLAGGING PATH are both here.  ``build_survey`` measures the three corpora and
sets Yeivin's inventory beside MAM; ``classify_verse`` asks the same question of one verse at a
time, for the two paths that write verdicts -- ``prose_run._verse_record`` and
``printed_decalogue.parse_marks_body``, the second of which carries the eight Wikisource strands
and all twelve hand transcriptions.  It reads its whitelist straight off the entries the survey
checks, keyed on the TOKEN SEQUENCE and never on a verse reference: Yeivin's closed lists are the
differential check the survey runs against him, and a checker that consulted them would name a
chanted word by where it stands rather than by what it has.  What ``classify_verse`` feeds is an
additive field; ``status`` and ``tree`` are left alone, and whether a chanted word no section of
his inventory names should be ungrammatical is a later, separate decision.

TOKENS, NOT MARKS, and that choice is the design.  The prose scanner already fuses several
written pairs into one token: a doubled stress helper (pashta, telisha qetana), the zarqa's own
helper with its zarqa, the same-letter ``mahapakh!qadma`` cluster, munax + U+05C0 as legarmeh, and
qadma...zaqef as ``METHIGAZAQEF``.  It also swallows meteg, emitting ``SILLUQ`` only for a
verse-final U+05BD before sof pasuq.  Counting tokens therefore disposes of every confound that
would otherwise have to be special-cased -- a stress helper written twice is not two accents, and
neither is a metigah-zaqef.  The METHIGAZAQEF fuse crosses a maqaf and stops at a space, so a fused
pair is always one chanted word and the survey never counts one token for two: ITM §223's leading
example is the compound Ex 35:9 ואבני־שהם, while both that section and CoS Ch. 5 §§4-6 restrict
the metigah to the chanted word of the zaqef.  ``_methigazaqef_crossings`` is the
lint that holds the scanner to it.  One confound survives and is handled here: a geresh or gershayim
written twice on one chanted word is ONE accent written twice, and the scanner does not fuse it.
``_fold_repeated_geresh`` folds such a repeat, and ``geresh_folds`` names every place it fired.

ATOM AND CHANTED WORD (issue wlc-utils#81).  An atom is one written word, between spaces or maqafs; a
chanted word is a lone atom or a whole maqaf compound, and is the unit an accent marks.  Yeivin
states outright that the two take the same rules -- ITM §302, quoted in ``YEIVIN_ENTRIES`` -- so
this survey counts both together and records which kind each hit is, rather than treating the
compound as a separate phenomenon.  Maqaf is the last rung of the one scale of separating force
(``maqaf_nonfinal_accents``' ``MAQAF_IS_THE_LAST_RUNG`` in ``printed_decalogue_strands``), not a
second ledger.

THE MARK BODY IS BUILT HERE, ATOM BY ATOM, and the WLC build is checked against
``uni_to_marks.verse_to_marks``.  The scanner reads a mark body, and a token's position is an
offset into it, so the chanted-word boundaries have to be offsets into the same string: a space
ends a chanted word and a maqaf (``-``) is an atom boundary inside one.  ``verse_to_marks``
returns the body alone, with no way back to the Unicode a chanted word came from, so
``_verse_units`` rebuilds it fragment by fragment and keeps each fragment's Unicode beside its
marks.  For WLC the rebuild is asserted equal to ``verse_to_marks``' own output, which makes the
alignment a checked fact rather than a claim.  ``word_to_marks`` is applied per ATOM in all three
corpora, as ``verse_to_marks`` applies it per verse element, so its front-loading of a prepositive
accent never crosses an atom boundary and never moves an accent onto a neighbouring atom.

THE THREE CORPORA, and what each can be asked.  WLC 4.22 and UXLC are diplomatic -- the
Westminster transcription of the Leningrad Codex, and that same transcription corrected -- so
neither is a second hand.  MAM-simple is a consensus text.  A claim about what the accentuation
DOES therefore takes MAM, and the Yeivin cross-check below is run against MAM alone; WLC's and
UXLC's counts are here so the divergence between a manuscript and a consensus text can be read
off, not so that three columns can be averaged.

NOT EVERY MAQAF HERE IS THERE FOR THE SAME REASON, and that is what ``maqaf_after_gaya`` is
about.  Both books describe a maqaf written after a word that already has an accent, where a
gaʿya falls after that accent: Yeivin ITM §357 ("Maqqef after Gaʿya"), Breuer CoS Ch. 1 §43.
What §357 settles is where the non-final atom's accent comes from -- the atom keeps the accent
it has, the gaʿya written after that accent having had to be marked -- and not what the maqaf
signifies, which neither book settles: Yeivin writes these very compounds with a SPACE at §354,
Breuer's Ch. 1 §43 records that "different views have been expressed" and leaves the maqaf out
of the book, and his Ch. 9 §37 points the other way.  Nothing here turns on that.  A compound of
this kind IS a chanted word, on the only test there is for one -- a maqaf is written in it -- so
this survey's mechanical criterion counts it as one compound with two accents.  Thirteen of
MAM's twenty-two compounds with their accents split across atoms are of that kind, across five
different accent pairs, and the signature is checkable: the accented non-final atom also has a
meteg after its accent.  Issue wlc-utils#86.

Prose verses only, routed by ``prose_filter.should_keep_line``.  Yeivin's inventory below is his
prose inventory; the poetic system puts two accents on one chanted word far more readily and
systematically (Breuer, Chapter 9 §§20-26), so a merged count would say nothing about either.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

from accgram import accent_marks as am
from accgram import maqaf_nonfinal_accents as mna
from accgram import prose_filter, rtms_data, uni_to_marks
from accgram.almost_errors_html_shared import accents_and_letters
from accgram.prose_scanner import HasLegarmeh, Token, scan_accents
from wlc_cmn.wlc_book_codes import wlc_bb_codes
from mb_cmn import file_io
from mb_cmn import paths
from mb_cmn import provenance

UNI_MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"

# Token types that terminate or delimit a verse rather than marking a chanted word.  Everything
# else the scanner emits is an accent token, ``SILLUQ`` and ``MAYELA`` and ``LEGARMEH`` included.
_NOT_AN_ACCENT_TOKEN = frozenset(("TILDE", "SOFPASUQ", "MISSING_SOFPASUQ"))

# A geresh or gershayim written twice on one chanted word is one accent written twice, and the
# scanner does not fuse the repeat as it fuses a doubled pashta or telisha qetana.  Folded here,
# and every fold recorded, so the fold can be audited rather than taken on trust.
_FOLDED_WHEN_REPEATED = frozenset(("GERESH", "GERSHAYIM"))

# The mark-body placeholder an empty qere side leaves: a ketiv with no qere (ketiv velo qere).
# The ketiv atoms are written but nothing is chanted in their place, so the placeholder is NOT a
# chanted word, though its ``**`` marker otherwise opens one.  Both unit derivations exclude it
# -- ``_kq_side_frag`` on the fragment path and ``_run_is_a_chanted_word`` on the body-only path
# -- so it stands outside every count, like the swallowed ketiv beside it.
_EMPTY_QERE_PLACEHOLDER = "**qq"

KIND_ATOMIC = "an atomic chanted word"
KIND_COMPOUND_SPLIT = "a maqaf compound, its accents split across atoms"
KIND_COMPOUND_FINAL = "a maqaf compound, its accents all on the final atom"
KIND_COMPOUND_NONFINAL = "a maqaf compound, its accents all on one non-final atom"

CORPUS_KIND = mna.CORPUS_KIND


@dataclass(frozen=True)
class Unit:
    """One space-delimited unit of a verse's mark body, with the Unicode it was built from.

    ``is_word`` is false for the units that are not chanted words at all: a swallowed ketiv, an
    empty-qere placeholder (``_EMPTY_QERE_PLACEHOLDER`` -- a ketiv with no qere), and a
    petuhah/setumah/nun-inversum marker.  They stay in the body because the scanner's lookaheads
    read the characters between two accents, and dropping them could change a token; they are left
    out of every count.
    """

    text: str
    marks: str
    start: int
    is_word: bool

    @property
    def end(self) -> int:
        return self.start + len(self.marks)

    @property
    def is_compound(self) -> bool:
        return am.MAQAF in self.marks


# --- building each corpus's fragments -----------------------------------------
#
# A fragment is one atom's Unicode beside its marks.  ``_verse_units`` joins fragments into units
# by the same rule ``uni_to_marks.verse_to_marks`` uses: a space between two fragments unless the
# earlier one ends with a maqaf, in which case the two are one chanted word.


@dataclass(frozen=True)
class Frag:
    """One atom's Unicode and marks, plus what the joiner needs to know about it.

    ``always_starts_a_unit`` is for the qere of a ketiv-qere element, which
    ``uni_to_marks._kq_to_marks`` separates from its ketiv by a space unconditionally -- even
    where the ketiv ends with a maqaf, as Numbers 23:13's לך־ does.  Without the flag the maqaf
    rule would join them and the rebuilt body would lose that space.
    """

    text: str
    marks: str
    is_word: bool
    always_starts_a_unit: bool = False


def _plain_frag(atom: str) -> Frag:
    return Frag(atom, uni_to_marks.word_to_marks(atom), True)


def _kq_side_frag(side: object, marker: str, *, is_word: bool) -> Frag:
    """One side of a ketiv-qere element as a single fragment, atoms joined by maqaf.

    Mirrors ``uni_to_marks._kq_to_marks``: the ketiv is ``*`` + its atoms, the qere ``**`` + its
    atoms, an empty side becoming the ``*kk`` / ``**qq`` placeholder the Michigan-Claremont source
    used.  Both are one fragment rather than one per atom, so the Unicode side is the whole qere
    -- which is the chanted word the reader wants to see.
    """
    starts = marker == "**"
    words = [w for w in (_kq_word(v) for v in (side or ())) if w[1]]
    if not words:
        # An empty side is a placeholder, not a chanted word, so ``is_word`` is False even on
        # the qere side: ``**qq`` stands for a ketiv with no qere, where nothing is chanted
        # (see ``_EMPTY_QERE_PLACEHOLDER``).
        return Frag("", _EMPTY_QERE_PLACEHOLDER if starts else "*kk", False, starts)
    return Frag(
        UNI_MAQAF.join(w[0] for w in words),
        marker + "-".join(w[1] for w in words),
        is_word,
        starts,
    )


def _kq_word(vel: object) -> tuple[str, str]:
    if isinstance(vel, str):
        return (vel, uni_to_marks.word_to_marks(vel))
    if isinstance(vel, dict):
        word = vel.get("word")
        if isinstance(word, str):
            return (
                word,
                uni_to_marks.word_to_marks(word) + _notes_suffix(vel.get("notes")),
            )
    return ("", "")


def _notes_suffix(notes: object) -> str:
    """The ``]N`` markers appended after a word, as ``uni_to_marks._notes_suffix`` appends them.

    They are kept because the legarmeh and mayela lookaheads key on ``]<digit>``: dropping them
    would let a lookahead run past a blocker it should have stopped at, and a METHIGAZAQEF fuse
    two tokens the checker keeps apart.
    """
    if isinstance(notes, str):
        return notes
    if isinstance(notes, list):
        return "".join(n for n in notes if isinstance(n, str))
    return ""


def _wlc_vel_frags(vel: object) -> list[Frag]:
    if isinstance(vel, str):
        return [_plain_frag(vel)]
    if not isinstance(vel, dict):
        return []
    sam = vel.get("sam_pe_inun")
    if isinstance(sam, str):
        return [Frag("", "N]8" if sam == "N" else sam, False)]
    kq = vel.get("kq")
    if kq is not None:
        ketiv, qere = kq if isinstance(kq, (list, tuple)) and len(kq) == 2 else ([], [])
        return [
            _kq_side_frag(ketiv, "*", is_word=False),
            _kq_side_frag(qere, "**", is_word=True),
        ]
    word = vel.get("word")
    if isinstance(word, str):
        return [
            Frag(
                word,
                uni_to_marks.word_to_marks(word) + _notes_suffix(vel.get("notes")),
                True,
            )
        ]
    return []


def wlc_frags(kq_u_dir: Path) -> dict[str, list[Frag]]:
    index = rtms_data.load_wlc422_index(kq_u_dir)
    out: dict[str, list[Frag]] = {}
    for bcv, verse in index.items():
        vels = verse.get("vels")
        frags = [f for vel in (vels or []) for f in _wlc_vel_frags(vel)]
        body, _units = _verse_units(frags)
        # The rebuild is the check: if it stops matching the body the checker actually scans,
        # every token position below is attributed to the wrong chanted word.
        assert body == uni_to_marks.verse_to_marks(verse), bcv
        out[bcv] = frags
    return out


def _atom_frags(atoms: list[str]) -> list[Frag]:
    return [_plain_frag(a) for a in atoms if a]


def mam_frags(refs_by_book: dict[str, set[tuple[int, int]]]) -> dict[str, list[Frag]]:
    from accgram import mam_simple_verse

    loaded = mam_simple_verse.load_mam_simple_for_refs(
        paths.require_mam_simple_dir(), refs_by_book
    )
    return {
        bcv: _atom_frags(
            [v for v in payload["mam_simple_verse"]["vels"] if isinstance(v, str)]
        )
        for bcv, payload in loaded.items()
    }


def uxlc_frags(uxlc_dir: Path) -> dict[str, list[Frag]]:
    out: dict[str, list[Frag]] = {}
    for path in sorted(uxlc_dir.glob("*.xml")):
        bb = mna.UXLC_FILE_TO_BB.get(path.stem)
        if bb is None:
            raise ValueError(f"unmapped UXLC book file: {path.name}")
        for chapter in ET.parse(path).getroot().iter("c"):
            chnu = int(chapter.get("n"))
            for verse in chapter.iter("v"):
                vrnu = int(verse.get("n"))
                atoms = [mna.uxlc_text(el) for el in verse if el.tag in ("w", "q")]
                out[f"{bb}{chnu}:{vrnu}"] = _atom_frags(atoms)
    return out


# --- assembling a verse's mark body and its chanted words ---------------------


def _verse_units(frags: list[Frag]) -> tuple[str, list[Unit]]:
    """One verse's mark body, and the units it is built from.

    The joining rule is ``uni_to_marks.verse_to_marks``': a space between two fragments unless the
    earlier one ends with a maqaf, in which case the maqaf joins them into one chanted word.
    """
    parts: list[str] = []
    units: list[Unit] = []
    texts: list[list[str]] = []
    marks: list[list[str]] = []
    pos = 0
    open_unit: int | None = None
    prev_ended_maqaf = False
    for frag in frags:
        if not frag.marks:
            continue
        if parts and (not prev_ended_maqaf or frag.always_starts_a_unit):
            parts.append(" ")
            pos += 1
            open_unit = None
        if open_unit is None:
            open_unit = len(units)
            units.append(Unit(text="", marks="", start=pos, is_word=frag.is_word))
            texts.append([])
            marks.append([])
        texts[open_unit].append(frag.text)
        marks[open_unit].append(frag.marks)
        parts.append(frag.marks)
        pos += len(frag.marks)
        prev_ended_maqaf = frag.marks.endswith(am.MAQAF)
    joined = [
        Unit(
            text="".join(texts[i]),
            marks="".join(marks[i]),
            start=unit.start,
            is_word=unit.is_word,
        )
        for i, unit in enumerate(units)
    ]
    return "".join(parts), joined


# --- attributing tokens to chanted words --------------------------------------


def _fold_repeated_geresh(tokens: list[Token]) -> tuple[list[Token], str | None]:
    """Drop the non-first occurrence of a repeated geresh or gershayim within one chanted word.

    Returns the folded token list and, when a fold fired, the unfolded leaf sequence, so the
    place can be named in the JSON rather than silently corrected.
    """
    seen: set[str] = set()
    kept: list[Token] = []
    folded = False
    for token in tokens:
        if token.type in _FOLDED_WHEN_REPEATED and token.type in seen:
            folded = True
            continue
        seen.add(token.type)
        kept.append(token)
    return kept, (" ".join(t.leaf for t in tokens) if folded else None)


def _atom_index(unit: Unit, offset: int) -> int:
    """Which atom of ``unit`` the mark at body offset ``offset`` sits in."""
    return unit.marks.count(am.MAQAF, 0, offset - unit.start)


def _gaya_after_accent(unit: Unit, tokens: list[Token]) -> bool:
    """Does a non-final atom of ``unit`` have a meteg after the accent it carries?

    The signature of ITM §357's maqqef after gaʿya, and of the maqaf Breuer CoS Ch. 1 §43
    describes: an atom that has its own accent, a gaʿya after that accent, and then a maqaf.
    Read off the mark body, since ``uni_to_marks`` keeps meteg there even though the scanner
    emits no token for it.

    ``maqaf_nonfinal_accents.gaya_after_the_nonfinal_accent`` asks the same question of the same
    compound off the Unicode instead, which is what that survey has and this one does not, and
    ANFA-reason (c) there is decided by it.  ``scan_corpus`` asserts that the two agree on every
    split compound of all three corpora, so the mark body and the Unicode cannot answer
    differently and the two surveys cannot part company over one compound.
    """
    last = unit.marks.count(am.MAQAF)
    for token in tokens:
        if _atom_index(unit, token.start) == last:
            continue
        after_accent = token.start - unit.start + 1
        atom_end = unit.marks.index(am.MAQAF, after_accent - 1)
        if am.METEG in unit.marks[after_accent:atom_end]:
            return True
    return False


def _kind_of(unit: Unit, atom_indices: list[int]) -> str:
    if not unit.is_compound:
        return KIND_ATOMIC
    if len(set(atom_indices)) > 1:
        return KIND_COMPOUND_SPLIT
    last = unit.marks.count(am.MAQAF)
    return KIND_COMPOUND_FINAL if atom_indices[0] == last else KIND_COMPOUND_NONFINAL


def _display(unit: Unit) -> str:
    """The chanted word in letters and accents, no vowels, with its maqafs put back.

    ``accents_and_letters`` drops the maqaf along with the vowels, so a compound is reduced atom
    by atom and rejoined -- the same treatment ``maqaf_nonfinal_accents_page.lo_taase_compound``
    gives it.  Lifted from the corpus, never retyped.
    """
    return UNI_MAQAF.join(
        accents_and_letters(atom) for atom in unit.text.split(UNI_MAQAF)
    )


def _methigazaqef_crossings(
    body: str, tokens: list[Token], units: list[Unit]
) -> list[dict]:
    """Every METHIGAZAQEF token whose qadma and zaqef sit in different chanted words.

    A MECHANICAL LINT, and it must read 0 in all three corpora.  ``prose_scanner``'s rule crosses
    a maqaf, so that ITM §223's metigah-zaqef on the compound Ex 35:9 ואבני־שהם is one token, and
    stops at a space, because §223 and CoS Ch. 5 §§4-6 restrict the metigah to the chanted word of
    the zaqef.  A non-zero count therefore means the fuse has reached across a
    chanted-word boundary again -- the regression this function exists to catch -- so the places
    it reaches are named rather than assumed away.  It read 5 in WLC and 3 in UXLC until the space
    went into ``_METHIGA_MID``; the counts themselves live in the JSON, not in this docstring.
    """
    out: list[dict] = []
    for token in tokens:
        if token.type != "METHIGAZAQEF":
            continue
        zaqef_at = body.index(am.ZAQEF_QATAN, token.start)
        if " " not in body[token.start : zaqef_at]:
            continue
        qadma_unit = _unit_at(units, token.start)
        zaqef_unit = _unit_at(units, zaqef_at)
        out.append(
            {
                "qadma_on": _display(qadma_unit) if qadma_unit else "",
                "zaqef_on": _display(zaqef_unit) if zaqef_unit else "",
            }
        )
    return out


def _unit_at(units: list[Unit], offset: int) -> Unit | None:
    for unit in units:
        if unit.start <= offset < unit.end:
            return unit
    return None


def _by_chanted_word(
    units: list[Unit], tokens: list[Token]
) -> list[tuple[Unit, list[Token], str | None]]:
    """Each chanted word of one verse, with the accent tokens that fall inside it.

    The shared core of the survey and the flagging path, so the two cannot come to different
    answers about the same verse.  Each entry is the unit, its tokens after
    ``_fold_repeated_geresh``, and the unfolded sequence where a fold fired.  The tokens the
    callers construct positionally carry ``start`` -1 and the verse terminators stand outside
    any chanted word, so both simply find no unit and drop out.
    """
    accents = [t for t in tokens if t.type not in _NOT_AN_ACCENT_TOKEN]
    by_unit: dict[int, list[Token]] = defaultdict(list)
    for token in accents:
        unit = _unit_at(units, token.start)
        if unit is not None and unit.is_word:
            by_unit[unit.start].append(token)
    out: list[tuple[Unit, list[Token], str | None]] = []
    for unit in units:
        if not unit.is_word:
            continue
        folded, unfolded = _fold_repeated_geresh(by_unit.get(unit.start, []))
        out.append((unit, folded, unfolded))
    return out


# The runs of a mark body that are not chanted words.  ``uni_to_marks`` has a petuhah or setumah
# as a lone ``P`` or ``S`` and a nun inversum as ``N]8``, and a ketiv as ``*`` followed by its
# letters (or ``*kk`` where the ketiv side is empty); the qere after it opens with ``**`` and IS
# a chanted word -- unless it is the ``**qq`` placeholder of a ketiv with no qere, where nothing
# is chanted (see ``_EMPTY_QERE_PLACEHOLDER``).  The only other ASCII in a mark body is the
# ``]N`` note suffix, which never stands alone, so none of these tests can collide with a real
# chanted word.
_SAM_PE_INUN_MARKS = frozenset(("P", "S", "N]8"))


def _run_is_a_chanted_word(marks: str) -> bool:
    if marks in _SAM_PE_INUN_MARKS:
        return False
    if marks == _EMPTY_QERE_PLACEHOLDER:
        return False
    return marks.startswith("**") or not marks.startswith("*")


def units_from_body(body: str) -> list[Unit]:
    """One verse's chanted words, read off the mark body alone.

    ``scan_corpus`` builds its units from the fragments it transcodes, which is what lets it keep
    each chanted word's Unicode beside its marks.  A caller on a verdict path has only the body
    the scanner read -- and that is enough for the boundaries, because ``uni_to_marks`` puts a
    space between two chanted words and nowhere else, so a space-delimited run of a mark body is
    a chanted word.  These units carry no ``text``, so ``_display`` is not available here;
    ``scan_corpus`` asserts on every verse of all three corpora that the two derivations agree.
    """
    units: list[Unit] = []
    pos = 0
    for run in body.split(" "):
        if run:
            units.append(
                Unit(
                    text="",
                    marks=run,
                    start=pos,
                    is_word=_run_is_a_chanted_word(run),
                )
            )
        pos += len(run) + 1
    return units


def _bb_order() -> dict[str, int]:
    return {bb: i for i, bb in enumerate(wlc_bb_codes())}


def _sort_key(bcv: str) -> tuple[int, int, int]:
    bb, chnu, vrnu = mna.split_bcv(bcv)
    return (_bb_order()[bb], chnu, vrnu)


# --- the per-corpus scan ------------------------------------------------------


def scan_corpus(frags_by_bcv: dict[str, list[Frag]]) -> dict:
    """Every prose chanted word of one corpus, and the ones with two or more accent tokens."""
    bcvs = sorted(
        (b for b in frags_by_bcv if prose_filter.should_keep_line(*mna.split_bcv(b))),
        key=_sort_key,
    )
    hits: list[dict] = []
    geresh_folds: list[dict] = []
    crossings: list[dict] = []
    n_verses = n_atomic = n_compound = 0
    n_methigazaqef = 0
    has_legarmeh: HasLegarmeh | None = None
    current_bb: str | None = None
    for bcv in bcvs:
        bb, chnu, vrnu = mna.split_bcv(bcv)
        if bb != current_bb:
            # One instance per book, as ``prose_scanner.scan_book`` holds one: the 17-passage
            # list is walked monotonically and the 1Sam 14:47 counter resets per book.
            has_legarmeh, current_bb = HasLegarmeh(), bb
        n_verses += 1
        body, units = _verse_units(frags_by_bcv[bcv])
        # The flagging path has only the body, and reads the chanted words off it.  Assert here
        # that the two derivations agree, so the field ``classify_verse`` feeds the verdict
        # paths cannot drift from the survey the whitelist is closed against.
        assert units_from_body(body) == [
            Unit(text="", marks=u.marks, start=u.start, is_word=u.is_word)
            for u in units
        ], bcv
        tokens = scan_accents(body, bb, chnu, vrnu, has_legarmeh)
        n_methigazaqef += sum(1 for t in tokens if t.type == "METHIGAZAQEF")
        crossings.extend(
            {"bcv": bcv, **c} for c in _methigazaqef_crossings(body, tokens, units)
        )
        for unit, folded, unfolded in _by_chanted_word(units, tokens):
            if unit.is_compound:
                n_compound += 1
            else:
                n_atomic += 1
            if unfolded is not None:
                geresh_folds.append(
                    {
                        "bcv": bcv,
                        "chanted_word": _display(unit),
                        "as_scanned": unfolded,
                        "as_counted": " ".join(t.leaf for t in folded),
                    }
                )
            if len(folded) < 2:
                continue
            atom_indices = [_atom_index(unit, t.start) for t in folded]
            kind = _kind_of(unit, atom_indices)
            hit = {
                "bcv": bcv,
                "chanted_word": _display(unit),
                "sequence": " ".join(t.leaf for t in folded),
                "kind": kind,
            }
            if kind == KIND_COMPOUND_SPLIT:
                # Only where the accents are split does the question arise, and recording the
                # flag on every hit would put a field on 1,600 of them to say nothing.
                gaya = _gaya_after_accent(unit, folded)
                # The two surveys must not answer one compound differently, ANFA-reason (c) in
                # ``maqaf_nonfinal_accents`` being decided by the same signature read off the
                # Unicode rather than off the mark body.  Asserted rather than assumed: the two
                # derivations have nothing in common but the corpus.
                assert gaya == mna.gaya_after_the_nonfinal_accent(unit.text), (
                    bcv,
                    unit.text,
                )
                hit["gaya_after_the_nonfinal_accent"] = gaya
            hits.append(hit)
    hits.sort(key=lambda h: (h["sequence"], _sort_key(h["bcv"])))
    return {
        "verses": n_verses,
        "chanted_words": n_atomic + n_compound,
        "atomic_chanted_words": n_atomic,
        "maqaf_compounds": n_compound,
        "hits": len(hits),
        "by_kind": dict(Counter(h["kind"] for h in hits).most_common()),
        "by_sequence": dict(Counter(h["sequence"] for h in hits).most_common()),
        "geresh_folds": geresh_folds,
        "methigazaqef": {
            "tokens": n_methigazaqef,
            "crossing_a_chanted_word_boundary": len(crossings),
            "crossings": crossings,
        },
        "occurrences": hits,
    }


# --- Yeivin's prose inventory -------------------------------------------------
#
# Transcribed from the FULL OCR of the book at
# ``../masorah-books/books/itm/md-export-of-docx/`` -- that repo was ``yeivin-itm`` until it was
# renamed on 2026-07-31 -- not from
# the partial adaptation at ``../al-hatorah/py/itm/``, which does not carry all of these sections.
# Each ``quote`` is Yeivin's own wording, so it keeps his romanizations: he spells tifxa with a
# dotted t and a dotted h, and munax with a dotted h, where the rest of this repo spells xet with
# an x.  The spellings themselves stand in the quote strings below, which are values and not
# comments.
#
# ``sequences`` are the scanner's own leaf names, which is what makes an entry checkable: the
# measured hits with that token sequence are the entry's measured set.  ``verses`` is Yeivin's
# closed list where he gives one.  ``exact`` says whether the two sets are expected to be equal;
# where they are not, his list must still be CONTAINED in the measurement, and the surplus is
# reported as ``measured_beyond_yeivin`` rather than passed over.

_ITM = "Yeivin, Introduction to the Tiberian Masorah"


@dataclass(frozen=True)
class YeivinEntry:
    section: str
    names: str
    stated_count: str
    quote: str
    sequences: tuple[str, ...] = ()
    verses: tuple[str, ...] = ()
    exact: bool = False
    note: str = ""


YEIVIN_ENTRIES: tuple[YeivinEntry, ...] = (
    YeivinEntry(
        section="§209",
        names="silluq takes one conjunctive, and no secondary accent",
        stated_count="(a rule, not a count)",
        quote=(
            "Silluq can only be preceded by one conjunctive, and this is merka."  # translit-ok
        ),
        note=(
            "Here so that a silence is checkable rather than assumed. Nothing in this"
            " inventory names a secondary merkha in a silluq's chanted word, and §209 with"
            " §210 is the pair that makes that evidence: §209 is the whole statement of"
            " silluq's conjunctives and adds no secondary, and §210 is the only section"
            " that gives silluq a second mark, which is the mayela. §210's stated"
            " condition excludes the one MAM chanted word at issue on its own terms --"
            " 'In these cases silluq has neither tipexa nor a conjunctive before it' --"
            " where Song 8:6 has the tipexa on אש, one chanted word earlier. Searched over"
            " the full OCR on 2026-08-03, section by section: of the thirteen that name a"
            " secondary accent with a given disjunctive, silluq is in one. Two near misses"
            " are not it, §212's exceptional Micah 6:3, where a merkha is the only accent"
            " between etnaxta and silluq but stands on a chanted word of its own, and"
            " §373's poetic metigah, where the metigah is the secondary mark and the merkha"
            " an ordinary servus. Breuer is silent in the same place: CoS Ch. 3 §39 gives"
            " the silluq's servant across two separate words and §40, the same-word"
            " section, is the mayela's alone, both pinned in masorah-books'"
            " check_cos_claims.py. So ca8:6 שלהבתיה stands in ``mam_residue`` unnamed by"
            " either book -- and it is the one atomic merkha-with-silluq chanted word in"
            " any of the three corpora, which all three have. Issue wlc-utils#86."
        ),
    ),
    YeivinEntry(
        section="§210",
        # "The mayela", never "the mayela tipexa" -- mayela is the name for what would otherwise
        # be a tipexa there, as ``maqaf_nonfinal_accents``' ANFA-reason-(a) bullet sets out.  Yeivin's
        # own quote below is where the reader learns the sign's shape.
        names="the mayela with silluq",
        stated_count="in five places",
        quote=(
            "In five places, the word bearing silluq has, in addition, a secondary accent"
            " like ṭifḥa in form."
        ),
        sequences=("mayela silluq",),
        verses=("lv21:4", "nu15:21", "is8:17", "ho11:6", "1c2:53"),
        exact=True,
        note=(
            "Yeivin adds that the Masorah treats the sign as a conjunctive under the name"
            " mayela, and that the same sign occurs with etnaxta (§216)."
        ),
    ),
    YeivinEntry(
        section="§215",
        names="munax with etnaxta",
        stated_count="in two cases",
        quote=(
            "In two cases munaḥ is used as a secondary accent in the same word as atnaḥ,"
            " marked on an open, syllable suitable for gaʿya (#326)."
        ),
        sequences=("munax atnax",),
        verses=("2s12:25", "1c5:20"),
        exact=True,
    ),
    YeivinEntry(
        section="§216",
        names="the mayela with etnaxta",
        stated_count="in ten or eleven cases",
        quote=(
            "In ten or eleven cases in the Bible, a sign of the same form as ṭifḥa appears"
            " as a secondary accent on the same word as atnaḥ."
        ),
        sequences=("mayela atnax",),
        verses=(
            "gn8:18",
            # The OCR line reads "בשבעת יכם 8:26 2 Nu", which is Numbers 28:26 with the 28
            # broken across the reference: בשבעתיכם stands there and nowhere in Numbers 2.
            "nu28:26",
            "2k9:2",
            "je2:31",
            "ek7:25",
            "ek10:13",
            "ek11:18",
            "da4:9",
            "da4:18",
            "ru1:10",
            "2c20:8",
        ),
        exact=True,
        note=(
            "The count is Yeivin's own 'ten or eleven'; his list has eleven, of which he"
            " says of Ezekiel 10:13 that mayela is not used there in some early"
            " manuscripts."
        ),
    ),
    YeivinEntry(
        section="§219",
        names="munax-zaqef -- a fourth variant of the zaqef melody",
        stated_count="in many cases",
        quote=(
            "In many cases also munaḥ is marked as a secondary accent on the same word as"
            " zaqef and this combination is considered as a fourth variant of the zaqef"
            " melody."
        ),
        sequences=("munax zaqef",),
        note=(
            "§221 gives the conditions: the combination is used when the zaqef word"
            " includes an open syllable suitable for gaʿya which is not the first syllable."
            " By far the largest class here, and open, so there is no list to check against."
        ),
    ),
    YeivinEntry(
        section="§223",
        names="metigah-zaqef",
        stated_count="(no count given)",
        quote=(
            "If the zaqef is not preceded by pashṭa, and if the word bearing zaqef contains"
            " a closed syllable which is separated from the stress syllable by a full"
            " vowel--or at least by a vocal shewa, and if this closed syllable is not the"
            " first in the word, the methigah-zaqef is used."
        ),
        note=(
            "Invisible to this survey by construction: the scanner fuses qadma...zaqef into"
            " one METHIGAZAQEF token, so a metigah-zaqef chanted word has one accent token,"
            " not two. The fuse crosses a maqaf, as this section's leading example Ex 35:9"
            " ואבני־שהם requires, and stops at a space, on this section's 'the word bearing"
            " zaqef' and CoS Ch. 5 §4's 'A methiga will appear in the word of the small"
            " zakef'. So a fused pair is always one chanted word, and"
            " ``crossing_a_chanted_word_boundary`` is 0 in all three corpora -- a lint on the"
            " scanner rather than a measurement of the corpus. The token count is under"
            " ``methigazaqef`` in each corpus."
        ),
    ),
    YeivinEntry(
        section="§233",
        names="merkha with tipexa -- a secondary merkha in the tipexa's chanted word",
        stated_count="in 8 cases",
        quote=(
            "In 8 cases merka occurs as a secondary accent on the same word as ṭifḥa,"  # translit-ok
            " generally on an open syllable suitable for gaʿya."
        ),
        sequences=("merkha tipexa",),
        verses=(
            "lv23:21",
            "2k15:16",
            "je8:18",
            "ek36:25",
            "ek44:6",
            "da5:17",
            "ca6:5",
            "1c15:13",
        ),
        note=(
            "Yeivin's eight are the cases where the merkha is a SECONDARY accent, and all"
            " eight have both marks on ONE atom. The measurement is wider, because it"
            " counts any chanted word with both marks -- including four compounds whose"
            " non-final atom has a merkha of its own, a gaʿya after it and then §357's"
            " maqaf. Those four are not §233 cases and are not §293's habit either; see"
            " ``maqaf_after_gaya``."
        ),
    ),
    YeivinEntry(
        section="§236",
        names="munax with revia",
        stated_count="in five cases",
        quote=(
            "In five cases munaḥ appears as a secondary accent in the same word as revia."
        ),
        sequences=("munax revia",),
        verses=("gn45:5", "ex32:31", "zc7:14", "ec4:10", "da1:7"),
        exact=True,
    ),
    YeivinEntry(
        section="§241",
        names="mahapakh with pashta (Yeivin spells the accent mehuppak)",  # translit-ok
        stated_count="in five cases",
        quote=(
            "In five cases mehuppak appears as a secondary accent on the same word as"  # translit-ok
            " pashṭa. It is marked on an open syllable suitable for gaʿya, which happens to"
            " be formed, in all cases, by the prefixed particle -ש."
        ),
        sequences=("mahapakh pashta",),
        verses=("ca1:7", "ca1:12", "ca3:4", "ec1:7", "ec7:10"),
        note=(
            "This is the section ``maqaf_nonfinal_accents`` used to cite for a secondary"
            " mahapakh in a TEVIR's chanted word; the pairing is with pashta, and the tevir"
            " entry never fired in any corpus. The three MAM chanted words beyond Yeivin's"
            " five all have the mahapakh on a non-final atom and the pashta on the last --"
            " the same shape as §233's surplus, and not the prefixed ־ש his five are about."
            " All three have a gaʿya after that mahapakh and then §357's maqaf, and Yeivin"
            " names one of them, Isaiah 59:16, at §357 itself; Breuer names another,"
            " Isaiah 63:5, at CoS Ch. 1 §43. See ``maqaf_after_gaya``."
        ),
    ),
    YeivinEntry(
        section="§244",
        names="both servi of pashta on one chanted word",
        stated_count="in eight places",
        quote=(
            "In eight places the two servi of pashṭa are marked on the same word, the"
            " second of them marked as a secondary accent generally on an open syllable"
            " suitable for gaʿya (#326)."
        ),
        sequences=("qadma mahapakh", "qadma merkha", "munax mahapakh"),
        verses=(
            "lv25:46",
            "nu20:1",
            "dt8:16",
            "ek43:11",
            "lm4:9",
            "da3:2",
            "er7:24",
            "2c35:25",
        ),
        note=(
            "Not one token sequence but three, because which pair of servi appears is"
            " settled by §240 and §242 (mahapakh or merkha first before pashta; munax or"
            " azla second), and the second servus tokenizes as qadma rather than azla"
            " wherever no geresh follows. ``mam_measured`` is therefore the union of the"
            " three sequences and is NOT a count of §244 cases: those three pairs also"
            " serve other disjunctives, and the surplus under ``measured_beyond_yeivin``"
            " is where they do. What is checked here is that all eight of Yeivin's"
            " chanted words are measured. §245 adds the one where the two servi share a"
            " base letter, Ezekiel 20:31, which the scanner fuses into a single"
            " mahapakh!qadma token and this survey therefore does not see as two."
        ),
    ),
    YeivinEntry(
        section="§253",
        names="merkha-tevir -- a secondary merkha in the tevir's chanted word",
        stated_count="in some hundred cases",
        quote=(
            "In some hundred cases merka is marked as a secondary accent on the same word"  # translit-ok
            " as tevir, (Of the secondary accents, the use of munaḥ-zaqef, #221, is more"
            " frequent)."
        ),
        sequences=("merkha tevir",),
        note=(
            "The measured count falls well short of Yeivin's hundred, and §254 says why:"
            " 'Already in L gaʿya occurs in most of the cases where merka is expected.' A"  # translit-ok
            " meteg is not an accent and emits no token, so wherever the Leningrad Codex"
            " has one the chanted word has a single accent token here. This is also the"
            " section ``maqaf_nonfinal_accents`` should have cited for merkha-tevir."
        ),
    ),
    YeivinEntry(
        section="§256",
        names="both servi of tevir on one chanted word",
        stated_count="in eight cases",
        quote=(
            "In eight cases the two servi of tevir are marked on the same word, with the"
            " azla on an open syllable suitable for gaʿya."
        ),
        sequences=("qadma darga",),
        verses=("jb1:15", "jb1:16", "jb1:17", "jb1:19", "ne11:7", "2c17:8"),
        exact=True,
        note=(
            "The tevir's counterpart of §244, and the section that names Job's four"
            " prose-frame ואמלטה -- his own example, cited as 'Job 1:15, 16, 17, 19'."
            " Six of his eight are listed here. The other two, Isaiah 30:16 ותאמרו and"
            " Isaiah 32:15 יערה, have a merkha as the second servus rather than a darga,"
            " so they measure as ``qadma merkha``, a sequence §244 already claims; a"
            " token sequence is claimed by one section only, so they are recorded in this"
            " note instead of in the list. The six listed are the whole of MAM's"
            " ``qadma darga``."
        ),
    ),
    YeivinEntry(
        section="§268",
        names="azla-geresh on one chanted word",
        stated_count="often",
        quote=(
            "Azla is often marked as a secondary accent on the word bearing geresh. This"
            " occurs under conditions similar to those governing the marking of munaḥ on"
            " the word bearing zaqef, or merka on the word bearing tevir (#221, 253)."  # translit-ok
        ),
        sequences=("azla geresh",),
        note=(
            "The second-largest class measured, and the one the earlier survey's named"
            " configurations left out altogether."
        ),
    ),
    YeivinEntry(
        section="§276",
        names="munax in the chanted word of a pazer",
        stated_count="in one case",
        quote=(
            "In one case, ... (Gen 50:17) the servus munaḥ is marked as a secondary accent"
            " on the word bearing pazer."
        ),
        sequences=("munax pazer",),
        verses=("gn50:17",),
        exact=True,
    ),
    YeivinEntry(
        section="§302",
        names="a maqaf compound is one unit for these rules",
        stated_count="(a rule, not a count)",
        quote=(
            "From the point of view of the accentuation, words joined by maqqef are"
            " considered as a single unit, and are treated so in the marking of"
            " conjunctives, secondary accents, and gaʿya."
        ),
        note=(
            "The warrant for measuring atomic chanted words and maqaf compounds together"
            " rather than as two phenomena. Yeivin's own illustration is אל־האשה taking"
            " munax-zaqef precisely because the maqaf makes the two atoms one unit."
        ),
    ),
    YeivinEntry(
        section="§354",
        names="gaʿya after the accent, on a word with penultimate stress",
        stated_count="(a rule, not a count)",
        quote=(
            "Gaʿya is similarly sometimes used on the last syllable of a word with"
            " penultimate stress if it ends with a guttural and the following word begins"
            " with lamed or nun."
        ),
        note=(
            "Yeivin's three examples are Ruth 1:21, 1 Kings 2:8 and Ezekiel 1:4 ונגה לו,"
            " and he writes all three with a SPACE. MAM has a maqaf after the gaʿya at"
            " Ezekiel 1:4, which is the only reason that compound reaches this survey."
            " See ``maqaf_after_gaya``."
        ),
    ),
    YeivinEntry(
        section="§357",
        names="maqqef after gaʿya",
        stated_count="(a rule, not a count)",
        quote=(
            "In some MSS maqqef is marked -- sometimes consistently, sometimes"
            " sporadically -- after a word marked with gaʿya after the accent. ... The"
            " purpose of this maqqef is to indicate that, even though gaʿya is marked"
            " after the accent, so that the reading of that syllable must be slowed down,"
            " the word must be joined to the following word, and no break should be made"
            " between them."
        ),
        note=(
            "The section that says what thirteen of MAM's twenty-two compounds with their"
            " accents split across atoms are. Yeivin's four examples carry a manuscript"
            " apiece -- Jeremiah 49:23 in C, Numbers 24:22 in S, Isaiah 59:16 in A and C,"
            " Lamentations 5:6 in L3 -- and Isaiah 59:16 is one of the thirteen. A hit of"
            " this kind IS a chanted word, on the only test there is for one -- a maqaf is"
            " written in it -- and it is counted as one here. What §357 settles is where the"
            " second accent token comes from: the non-final atom keeps the accent it has,"
            " the gaʿya written after that accent having had to be marked, so the token is"
            " not a secondary accent of the kind §§233 and 241 are about."
            " WHAT THE MAQAF SIGNIFIES IS NOT SETTLED, by either book, and this note does"
            " not settle it either. Yeivin's 'the word must be joined to the following word'"
            " reads as denying a pause rather than as making one chanted word with one"
            " accent: he writes these very compounds with a SPACE at §354 -- Ezekiel 1:4"
            " ונגה לו, Ruth 1:21 הרע לי, 1 Kings 2:8 ואשבע לו -- where a servant standing on"
            " one chanted word before its mafsik on the next is the ordinary relation."
            " Breuer CoS Ch. 1 §43 says outright that 'different views have been expressed'"
            " about this maqaf and leaves it out of the book, calling the mark a mesharet;"
            " Ch. 9 §37 points the other way, that an ordinary-order mark cannot stand in a"
            " hyphenated word, which would make the mark secondary and the compound one"
            " chanted word after all. Neither book squares the two. None of that bears on"
            " the NAME: what makes a chanted word here is the maqaf on the page, not an"
            " adjudication between §43 and §37. See ``maqaf_after_gaya``."
        ),
    ),
)


# --- Breuer, where he covers the same ground -----------------------------------
#
# Read off the full markdown export at ``../masorah-books/books/cos/md-export-of-docx/``, and
# pinned there by ``py/main_ocr.py cos-check-claims``.  Only three sections, because only three
# are load-bearing for what this survey cannot otherwise say: the one that defines the maqaf of
# ``maqaf_after_gaya``, the one that gives the tipexa's same-word servant, and the one that says
# a secondary mark leaves a maqaf standing.  Each ``quote`` keeps Breuer's romanizations, which
# differ from this repo's for most of the accent names; the spellings themselves stay in the
# quote strings, which are values and not comments.  His English names the maqaf as a hyphen far
# more often than by any transliteration of it, and never by either spelling this repo uses --
# so grep the translator's spelling and the Hebrew as well, or the topic looks absent.

_COS = "Breuer, The Cantillation of Scripture"


@dataclass(frozen=True)
class BreuerEntry:
    section: str
    names: str
    quote: str
    note: str = ""


BREUER_ENTRIES: tuple[BreuerEntry, ...] = (
    BreuerEntry(
        section="Ch. 1 §43",
        names="the maqaf written after a servant that has a gaʿya on its last syllable",
        quote=(
            "In ancient manuscripts there sometimes appears a makaf in other"  # translit-ok
            " circumstances. A makaf of this type appears sometimes after a word"  # translit-ok
            " cantillated with a mesharet, which is accentuated mile'eil, and a ga'aya"  # translit-ok
            " usually appears on its last syllable; e.g.: ותושע־לי (Isa. 63:5). About the"
            " significance of this makaf different views have been expressed. But since"  # translit-ok
            " this makaf does not appear in a regular manner in most of the manuscripts,"  # translit-ok
            " and it is apparently left to the discretion of every nakdan, and since there"
            " is no trace of it in the accepted editions of Scripture, we shall not discuss"
            " it in this book."
        ),
        note=(
            "Breuer defines the configuration exactly as the measurement finds it -- an"
            " ordinary SERVANT, a word accented on its penultimate syllable, a gaʿya on"
            " its last -- names Isaiah 63:5, which is one of the thirteen, and then puts"
            " the whole class outside his book. Yeivin's ITM §357 is the same maqaf. Two"
            " things follow: neither book's inventory of secondary accents is where these"
            " belong, and Breuer's 'no trace of it in the accepted editions' is a"
            " divergence from MAM, which has thirteen of them."
        ),
    ),
    BreuerEntry(
        section="Ch. 3 §28",
        names="the tipexa's servant in its own chanted word",
        quote=(
            "In eight places, the servant of tipekha appears with it in its word. ... The"  # translit-ok
            " servant is merkha - according to the ordinary order of the cantillation"
            " marks (above, §26); and it appears in a syllable fit for a light ga'aya or"  # translit-ok
            " in a syllable fit for the ga'aya of the big vowel."  # translit-ok
        ),
        note=(
            "Breuer's eight are Yeivin's eight at ITM §233, and his criterion says why the"
            " four beyond them are not of this kind: his servant stands on a syllable fit"
            " for a gaʿya, where each of the four instead has its accent on the atom's own"
            " stress with the gaʿya after it."
        ),
    ),
    BreuerEntry(
        section="Ch. 9 §37",
        names="a secondary mark does not cancel the maqaf; an ordinary one does",
        quote=(
            "A cantillation mark, which follows the regular order of the cantillation"
            " marks, cannot appear in a word joined by hyphen to the next one; therefore,"
            " if a hyphenated word receives a cantillation mark, the hyphenation is"
            " immediately cancelled. ... Therefore, we find that all the secondary"
            " cantillation marks in the 21 books appear even in a hyphenated word, and the"
            " hyphen is never cancelled after them. So with the me'ayla that serves before"  # translit-ok
            " a siluk or ethnakhta; e.g.: וקויתי־לו (Isa. 8:17), ויצא־נח (Gen. 8:18); and"  # translit-ok
            " so, too, with the methiga that appears in the word of the small zakef."  # translit-ok
        ),
        note=(
            "The rule that partitions the split compounds, and the two examples Breuer"
            " gives are two of the nine MAM compounds that have no gaʿya after the"
            " non-final accent. At the other thirteen this rule and Ch. 1 §43 pull against"
            " each other, and Breuer does not square them: §37 would make the mark"
            " secondary and the compound one chanted word, where §43 declines to say what"
            " the mark is. ``maqaf_after_gaya`` reports that as a dispute and settles"
            " nothing by it -- the partition there is by the writing, a gaʿya between the"
            " non-final atom's accent and the maqaf."
        ),
    ),
)


def breuer_notes() -> list[dict]:
    return [
        {
            k: v
            for k, v in (
                ("section", e.section),
                ("names", e.names),
                ("quote", e.quote),
                ("source", _COS),
                ("note", e.note),
            )
            if v
        }
        for e in BREUER_ENTRIES
    ]


def _measured(hits: list[dict], sequences: tuple[str, ...]) -> list[dict]:
    wanted = frozenset(sequences)
    return [h for h in hits if h["sequence"] in wanted]


def yeivin_inventory(mam: dict) -> list[dict]:
    """Yeivin's prose inventory, each entry beside what MAM measures for it.

    Where Yeivin gives a closed list this RAISES on drift rather than warning: a warning in a
    generator's output is a warning nobody reads, and the whole value of transcribing the list is
    that it is a differential check against a source outside this repo.  An entry marked ``exact``
    must match his verses exactly; every entry with a list must at least contain them.
    """
    hits = mam["occurrences"]
    rows: list[dict] = []
    for entry in YEIVIN_ENTRIES:
        row: dict = {
            "section": entry.section,
            "names": entry.names,
            "yeivin_count": entry.stated_count,
            "quote": entry.quote,
            "source": _ITM,
        }
        if entry.note:
            row["note"] = entry.note
        if entry.sequences:
            measured = _measured(hits, entry.sequences)
            row["token_sequences"] = list(entry.sequences)
            row["mam_measured"] = len(measured)
            if entry.verses:
                listed = set(entry.verses)
                measured_bcvs = {h["bcv"] for h in measured}
                missing = sorted(listed - measured_bcvs, key=_sort_key)
                extra = [h for h in measured if h["bcv"] not in listed]
                if missing:
                    raise AssertionError(
                        f"ITM {entry.section}: verses Yeivin lists that MAM does not"
                        f" measure for {entry.sequences}: {missing}"
                    )
                if entry.exact and extra:
                    raise AssertionError(
                        f"ITM {entry.section}: Yeivin's list is closed, but MAM measures"
                        f" {[h['bcv'] for h in extra]} beyond it"
                    )
                row["yeivin_verses"] = list(entry.verses)
                row["yeivin_verses_all_measured"] = not missing
                row["yeivin_list_is_closed_and_matches_exactly"] = entry.exact
                if extra:
                    row["measured_beyond_yeivin"] = extra
        rows.append(row)
    return rows


def mam_residue(mam: dict) -> dict:
    """MAM prose chanted words whose token sequence no entry above names.

    The point of the survey stated as a finding: after Yeivin's whole prose inventory, this is
    what the consensus text has left over.  Phase 2's whitelist is keyed on the token pair, so
    this is also the list it will have to either name or flag.
    """
    named = {seq for entry in YEIVIN_ENTRIES for seq in entry.sequences}
    left = [h for h in mam["occurrences"] if h["sequence"] not in named]
    gaya = [h for h in left if h.get("gaya_after_the_nonfinal_accent")]
    telisha = [h for h in left if "telishagedola" in h["sequence"]]
    rest = [h for h in left if h not in gaya and h not in telisha]
    return {
        "what": (
            "MAM prose chanted words with two accent tokens whose token sequence is named"
            " by no section of Yeivin's prose inventory above."
        ),
        "total": len(left),
        "by_sequence": dict(Counter(h["sequence"] for h in left).most_common()),
        "already_documented_elsewhere": (
            "The geresh-family-with-telisha-gedola words are not unaccounted for: they are"
            " the five words ``uni_to_marks.word_to_marks`` keeps both marks on, whitelisted"
            " by ``lexical_validation`` and set out in the telisha gedola exhibit of"
            " gh-pages/wlc/accgram/almost-errors.html. A geresh or gershayim written twice on"
            " one of them is folded above, so each counts as two accents, not three."
        ),
        "accounted_for_by_maqaf_after_gaya": {
            "what": (
                "These are chanted words whose maqaf is the one ITM §357 describes, written"
                " after an atom that has its own accent and a gaʿya after that accent. Each"
                " IS a chanted word -- a maqaf is written in it, which is the whole test --"
                " and each does have two accent tokens. What §357 settles is that the second"
                " token is the non-final atom's retained accent rather than a secondary"
                " accent of the kind §§233 and 241 describe. What that maqaf SIGNIFIES is"
                " unsettled in both books, and nothing here turns on it: Yeivin writes the"
                " same compounds with a space at §354, Breuer CoS Ch. 1 §43 records that"
                " 'different views have been expressed' and leaves it out, and Ch. 9 §37"
                " points the other way. See ``maqaf_after_gaya``."
            ),
            "total": len(gaya),
            "occurrences": gaya,
        },
        "left_over_after_both": {
            "what": (
                "What is left when the telisha gedola words and the maqaf-after-gaʿya"
                " compounds are set aside: the atomic chanted words of MAM's prose verses"
                " that have two accents no section of either book names."
            ),
            "total": len(rest),
            "occurrences": rest,
        },
        "occurrences": left,
    }


# --- the flagging path --------------------------------------------------------


def _build_named_token_sequences() -> dict[str, str]:
    out: dict[str, str] = {}
    for entry in YEIVIN_ENTRIES:
        for sequence in entry.sequences:
            if sequence in out:
                raise AssertionError(
                    f"two ITM sections claim the token sequence {sequence!r}:"
                    f" {out[sequence]} and {entry.section}"
                )
            out[sequence] = entry.section
    return out


# The whitelist, read straight off the inventory above so the two cannot part company: a token
# sequence, and the ITM section that names it.  Configuration-level, as decision 1 of the plan
# settled -- munax with revia is named wherever it stands, not only at §236's five places.  The
# closed lists stay where they are useful, as the survey's differential check against Yeivin;
# they are not consulted here, so nothing on a verdict path turns on a verse reference.
NAMED_TOKEN_SEQUENCES: dict[str, str] = _build_named_token_sequences()


def classify_verse(body: str, tokens: list[Token]) -> list[dict]:
    """One verse's chanted words with two or more accent tokens, each named or left unnamed.

    ``body`` is the mark body the scanner read and ``tokens`` the stream it emitted, so a caller
    passes what it already has.  Each hit carries the chanted word's own run of the body, its
    token sequence, whether it is an atom or a maqaf compound, and the ITM section that names
    the sequence -- ``None`` where no section of Yeivin's prose inventory does.  A ``None`` is
    the finding: it is the pair for which the inventory, closed against MAM in the survey above,
    offers no precedent.

    Nothing here reads a verdict or writes one.  The caller records the result beside
    ``status`` and ``tree``, which stay as the grammar left them.
    """
    hits: list[dict] = []
    units = units_from_body(body)
    for unit, folded, _unfolded in _by_chanted_word(units, tokens):
        if len(folded) < 2:
            continue
        sequence = " ".join(t.leaf for t in folded)
        atom_indices = [_atom_index(unit, t.start) for t in folded]
        hits.append(
            {
                "marks": unit.marks,
                "sequence": sequence,
                "kind": _kind_of(unit, atom_indices),
                "itm_section": NAMED_TOKEN_SEQUENCES.get(sequence),
            }
        )
    return hits


def _split_hits(corpus: dict) -> list[dict]:
    return [h for h in corpus["occurrences"] if h["kind"] == KIND_COMPOUND_SPLIT]


def maqaf_after_gaya(scanned: dict[str, dict]) -> dict:
    """The compounds whose accents are split across atoms, partitioned by ITM §357's signature.

    A compound reaches this survey because a maqaf stands inside it, and the maqafs it finds
    are not all written for the same reason.  Yeivin ITM §357 and Breuer CoS Ch. 1 §43 both
    describe a maqaf written after a word that has its own accent and a gaʿya after that
    accent; §357 gives its purpose as saying the slowed syllable makes no break, and what it
    signifies beyond that is disputed in both books.  The partition here does not depend on
    that: the signature is mechanical -- ``_gaya_after_accent`` -- so it is a measurement
    rather than a reading, and each side of it is set out for the reader to check.

    This replaces the narrower ``merkha_tipexa_discrepancy`` block, whose open question this
    answers: the four MAM chanted words beyond §233's eight are neither §233 cases Yeivin left
    out nor §293's scribal habit.  The §233 and §241 arithmetic is kept below, since it is what
    put the question, and both surpluses turn out to be of the one kind.
    """
    mam = scanned["mam_simple"]
    per_corpus: dict[str, dict] = {}
    for name, corpus in scanned.items():
        split = _split_hits(corpus)
        with_gaya = [h for h in split if h["gaya_after_the_nonfinal_accent"]]
        per_corpus[name] = {
            "accents_split_across_atoms": len(split),
            "of_them_with_a_gaya_after_the_nonfinal_accent": len(with_gaya),
            "with_a_gaya_by_sequence": dict(
                Counter(h["sequence"] for h in with_gaya).most_common()
            ),
            "without_a_gaya_by_sequence": dict(
                Counter(
                    h["sequence"]
                    for h in split
                    if not h["gaya_after_the_nonfinal_accent"]
                ).most_common()
            ),
            "with_a_gaya": with_gaya,
        }

    def _arithmetic(section: str) -> dict:
        entry = next(e for e in YEIVIN_ENTRIES if e.section == section)
        listed = set(entry.verses)
        measured = _measured(mam["occurrences"], entry.sequences)
        beyond = [h for h in measured if h["bcv"] not in listed]
        return {
            "yeivin_stated": entry.stated_count,
            "yeivin_listed": len(listed),
            "mam_measured": len(measured),
            "yeivin_verses_by_kind": dict(
                Counter(h["kind"] for h in measured if h["bcv"] in listed).most_common()
            ),
            "beyond_yeivin": beyond,
            "beyond_yeivin_all_have_a_gaya_after_the_nonfinal_accent": all(
                h.get("gaya_after_the_nonfinal_accent") for h in beyond
            ),
        }

    return {
        "what": (
            "A maqaf written after a word that has its own accent and a gaʿya after that"
            " accent. ITM §357 gives its purpose -- the slowed syllable makes no break --"
            " and CoS Ch. 1 §43 gives its conditions: after a servant, on a word accented"
            " on its penultimate syllable, with the gaʿya on its last. A compound found by"
            " it IS a chanted word, on the only test there is for one -- a maqaf is written"
            " in it -- and it does have two accent tokens. What §357 settles is that the"
            " second token is the non-final atom's retained accent rather than a secondary"
            " accent of the kind §§233 and 241 describe. What the maqaf SIGNIFIES is"
            " unsettled in both books and nothing here turns on it: Yeivin writes the same"
            " compounds with a space at §354, CoS Ch. 1 §43 records that 'different views"
            " have been expressed' and leaves it out of the book, and Ch. 9 §37 points the"
            " other way."
        ),
        "how_it_is_told_apart": (
            "Mechanically, off the mark body: the accented non-final atom also has a meteg"
            " between that accent and the maqaf. Nothing here reads a verse reference. On"
            " MAM the signature partitions the compounds exactly, the nine without it"
            " being the mayela ones and nothing else. It is a signature and not a"
            " definition, though, and Isaiah 8:17 וקויתי־לו is where that shows: WLC and"
            " UXLC have a meteg after the mayela there and MAM has none, so the same"
            " compound answers differently by corpus while staying the mayela case CoS"
            " Ch. 9 §37 names by verse."
        ),
        "verses_the_books_name_that_this_survey_measures": {
            "ITM §354": ["ek1:4"],
            "ITM §357": ["is59:16"],
            "CoS Ch. 1 §43": ["is63:5"],
        },
        "which_corpus_has_it": (
            "MAM's, and hardly L's -- which is what both books' manuscript labels predict."
            " Yeivin's §357 examples are in C, in S, in A and C, and in L3; Breuer's is"
            " ancient manuscripts generally. The counts below are the check on that."
        ),
        "by_corpus": per_corpus,
        "what_the_others_are": (
            "The compounds with no gaʿya after the non-final accent are the mayela ones,"
            " which both books name outright: ITM §§210 and 216, and CoS Ch. 9 §37, whose"
            " two examples -- Isaiah 8:17 וקויתי־לו and Genesis 8:18 ויצא־נח -- are two of"
            " MAM's nine. There a secondary mark stands in a hyphenated atom, and Breuer's"
            " rule at Ch. 9 §37 is that the hyphenation is not cancelled after such a mark."
        ),
        "itm_233_arithmetic": _arithmetic("§233"),
        "itm_241_arithmetic": _arithmetic("§241"),
        "answer": (
            "The four chanted words beyond ITM §233's eight, and the three beyond §241's"
            " five, are neither cases those sections left out nor ITM §293's habit of a"
            " maqaf written after an atom that keeps its own conjunctive. They are §357's"
            " maqaf after gaʿya, and so are the four merkha-with-silluq שלף־חרב and the"
            " one munax-with-zaqef Isaiah 40:7 נבל־ציץ. Both books put the class outside"
            " their inventories of secondary accents -- Yeivin under gaʿya, Breuer by"
            " declining to discuss it -- and between them they name three of the thirteen"
            " by verse. §233's own eight and §241's own five all have both marks on ONE"
            " atom, on a syllable fit for a gaʿya, which is Breuer's stated criterion for"
            " a same-word servant at Ch. 3 §28."
        ),
        "recorded_not_flagged": (
            "Breuer says of this maqaf that 'there is no trace of it in the accepted"
            " editions of Scripture', and MAM has thirteen. That divergence is recorded"
            " here for future research and is not a verdict; nothing in this survey"
            " promotes it to a finding about MAM's accentuation. Issue wlc-utils#86."
        ),
    }


# --- the survey ---------------------------------------------------------------


def build_survey() -> dict:
    """The whole survey: three corpora, prose verses only, plus Yeivin's inventory beside MAM."""
    wlc = wlc_frags(paths.out_dir() / "wlc422-kq-u")
    refs: dict[str, set[tuple[int, int]]] = defaultdict(set)
    for bcv in wlc:
        bb, chnu, vrnu = mna.split_bcv(bcv)
        refs[bb].add((chnu, vrnu))

    corpora = {
        "wlc422": wlc,
        "uxlc": uxlc_frags(paths.in_dir() / "UXLC-39"),
        "mam_simple": mam_frags(dict(refs)),
    }
    scanned = {
        name: {"kind": CORPUS_KIND[name], **scan_corpus(frags)}
        for name, frags in corpora.items()
    }
    return {
        "criterion": (
            "A chanted word -- an atom, or a whole maqaf compound -- carrying two or more"
            " accent TOKENS as the prose scanner emits them. Tokens rather than marks: the"
            " scanner already fuses a doubled stress helper, the zarqa's own helper with"
            " its zarqa, the same-letter mahapakh!qadma cluster, munax with a following U+05C0 as"
            " legarmeh, and qadma...zaqef as metigah-zaqef, and it swallows meteg. A geresh"
            " or gershayim written twice on one chanted word is folded here, since that is"
            " one accent written twice and the scanner does not fuse it."
        ),
        "scope": (
            "Prose verses only, routed by prose_filter.should_keep_line. Yeivin's inventory"
            " below is his prose inventory, and the poetic system puts two accents on one"
            " chanted word far more readily (Breuer, Chapter 9 §§20-26), so a merged count"
            " would say nothing about either."
        ),
        "which_corpus_answers_what": (
            "A claim about what the accentuation does takes MAM, a consensus text, so the"
            " Yeivin cross-check runs against MAM alone. WLC 4.22 and UXLC are the"
            " Westminster transcription of the Leningrad Codex and that transcription"
            " corrected, so they are one hand, not two, and their counts are here to be"
            " read against MAM rather than averaged with it."
        ),
        "yeivin_inventory": yeivin_inventory(scanned["mam_simple"]),
        "breuer_notes": breuer_notes(),
        "maqaf_after_gaya": maqaf_after_gaya(scanned),
        "mam_residue": mam_residue(scanned["mam_simple"]),
        "corpora": scanned,
    }


def default_json_out_path() -> Path:
    return paths.out_dir() / "accgram" / "chanted-word-accents.json"


def write_json(survey: dict, path: Path) -> None:
    payload = provenance.with_json_provenance(survey, __file__)
    # Through file_io for the temp-file write and the PermissionError retry; it makes
    # the directory too. LF is preserved as maqaf_nonfinal_accents preserves it -- the
    # repo's line-ending policy is LF in the workdir as well as in git, and a plain
    # text-mode write would translate to CRLF on Windows and leave every regeneration
    # looking like a whole-file diff. file_io's default newline="" translates nothing,
    # so it holds the line the old explicit newline="\n" held.
    file_io.json_dump_to_file_path(payload, str(path), indent=1)


def add_args(parser, *, repo_root: Path) -> None:
    # repo_root is unused: the default comes from ``default_json_out_path``, which composes
    # off ``paths.out_dir()`` -- the same value ``run`` falls back to, so the flag's
    # default and its absence can no longer answer differently.  The parameter is kept
    # because the entry point wires every subcommand the same way.
    del repo_root
    parser.add_argument(
        "--json-out",
        type=Path,
        default=default_json_out_path(),
        help="Where to write the survey JSON.",
    )


def run(args) -> None:
    survey = build_survey()
    out_path = getattr(args, "json_out", None) or default_json_out_path()
    write_json(survey, out_path)
    print(f"wrote {out_path}")
