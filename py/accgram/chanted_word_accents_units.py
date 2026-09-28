"""Chanted-word units, for the chanted-word-accents survey and the surveys that share them.

Each corpus's fragments, the verse mark body they are joined into, the chanted words read off
that body, and the accent tokens that fall inside each chanted word.  Why the body is rebuilt
atom by atom, and what counts as one accent token, is set out in ``chanted_word_accents``'
module docstring, which is the design of this module too.
"""

from __future__ import annotations

import xml.etree.ElementTree as ET
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from accgram import accent_marks as am
from accgram import maqaf_nonfinal_accents as mna
from accgram import rtms_data, uni_to_marks
from accgram.almost_errors_html_shared import accents_and_letters
from accgram.prose_scanner import Token
from mb_cmn import paths

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


def _fold_lone_bars(vels: list[str], bcv: str) -> list[str]:
    r"""MAM-simple's lone U+05C0 elements, each joined onto the atom it follows.

    MAM-simple sets the bar as an element of its own, where WLC attaches it to the word before it
    and UXLC keeps it inside that word's element after a space.  Taken as it stands the bar
    reaches the mark body as a space-delimited run of its own, and two things follow, both of them
    MAM-only (issue #215).  ``prose_scanner``'s two legarmeh rules are ``munax {TEXT} paseq`` with
    ``{TEXT}`` = ``[^ \r\n-]*``, which cannot cross a space, so the munax and the bar are never in
    one match: MAM had 0 LEGARMEH tokens over the prose verses where WLC 4.22 has 1,167 and UXLC
    1,169.  And ``_run_is_a_chanted_word`` is true of a bare bar, so each one was itself counted
    as a chanted word -- 1,610 of them, in 1,461 prose verses, which is the amount MAM's
    ``chanted_words`` and ``atomic_chanted_words`` were high by.  Both figures were measured
    2026-08-03 and re-measured 2026-08-18; issue #215 has them.

    Backwards is the only direction a bar can fold, a paseq being written after the atom it
    follows, and MAM has no bar that cannot be folded: none starts a verse, follows another bar,
    or follows an element that transcodes to nothing, measured over all 23,213 verses
    ``load_mam_simple_for_refs`` returns, where no other element has a U+05C0 in it either.  One
    that did would leave a lone-bar run behind, so this raises rather than passing one on.

    The space between the two elements is kept in the joined atom's Unicode -- it is what
    MAM-simple has there, and what UXLC's single element has inside it -- and ``word_to_marks``
    drops it, so the mark run is WLC's either way.
    """
    atoms: list[str] = []
    for vel in vels:
        if vel != am.PASEQ:
            atoms.append(vel)
            continue
        before = uni_to_marks.word_to_marks(atoms[-1]) if atoms else ""
        if not before or before.endswith(am.PASEQ):
            raise ValueError(f"{bcv}: a lone U+05C0 with no atom before it to join to")
        atoms[-1] += " " + vel
    return atoms


def _atom_frags(atoms: list[str]) -> list[Frag]:
    return [_plain_frag(a) for a in atoms if a]


def mam_frags(refs_by_book: dict[str, set[tuple[int, int]]]) -> dict[str, list[Frag]]:
    from accgram import mam_simple_verse

    loaded = mam_simple_verse.load_mam_simple_for_refs(
        paths.require_mam_simple_dir(), refs_by_book
    )
    return {
        bcv: _atom_frags(
            _fold_lone_bars(
                [v for v in payload["mam_simple_verse"]["vels"] if isinstance(v, str)],
                bcv,
            )
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
