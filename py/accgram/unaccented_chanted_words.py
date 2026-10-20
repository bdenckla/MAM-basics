r"""Chanted words with no accent, read off a verse's mark body: the rule both checkers share.

THE HOLE THIS CLOSES.  Both scanners emit tokens for accent marks alone.  A chanted word with no
accent, one whose atoms have letters, vowels and at most a meteg, produces no token at all: it
drops out of the accent sequence the grammar reads, and a verse can be judged grammatical because
the chanted word that makes it ungrammatical has vanished.  UXLC 2.6's change 2026.08.05-6 at Exodus 38:12 is
the case that exposed it.  WLC 4.22 has a merkha on עַמּוּדֵיהֶ֥ם, so the prose scanner reads the
stretch around it as munax zaqef merkha zaqef, which the grammar rejects, a merkha being no servant
of zaqef.  UXLC 2.6 has a meteg in its place, עַמּוּדֵיהֶֽם, the scanner reads munax zaqef zaqef,
and the verse parsed clean.  MAM has a munax there, עַמּוּדֵיהֶ֣ם, and munax zaqef munax zaqef is
grammatical with every chanted word accented.

THE RULE.  Every chanted word of a verse has an accent: a codepoint in U+0591..U+05AE on one of its
atoms.  Meteg, U+05BD, is not an accent, nor are Unicode PASEQ, sof pasuq and the puncta.  The rule
is about marks, not tokens, so a chanted word whose only accent is a stress helper or a mark the
scanner swallows still has an accent here; the prose lexical layer's other checks, and the poetic
scanner's ``STRAY_ACCENT``, are what judge such a mark.

HOW THE CHANTED WORDS ARE READ OFF THE BODY.  ``uni_to_marks.verse_to_marks`` writes a space between
two chanted words and a maqaf (``-``) between two atoms of one, and writes everything else a verse
has as runs of its own.  Each kind of run and atom is dispatched by name below, and a shape outside
the list raises, as "template dispatch is closed" requires:

1. **Maqaf.**  A maqaf compound is ONE chanted word.  Its non-final atoms need no accent of their
   own; the compound as a whole needs one.  A maqaf joins its atom to the next atom that is read,
   so a maqaf with no atom after it in its run reaches across what follows: two maqaf marks in a
   row, which a qere leaves where one of its words ends with a maqaf, and a maqaf before a space,
   which ``main_uxlc_grammar_test.splice_unit`` leaves where it splices in a word that ends with
   one.
2. **Ketiv.**  A ketiv is written but not read, unpointed and unaccented.  ``*`` opens its run and
   the run is the ketiv to its end, its later atoms, notes and maqaf marks included; ``*kk`` is the
   placeholder of a qere with no ketiv.  No atom of a ketiv belongs to any chanted word.
3. **Qere.**  The qere is read, and ``**`` opens it.  Because the ketiv beside it is not read, a
   maqaf written before a ketiv joins its atom to the next atom that is read: the qere.  ``**qq`` is
   the placeholder of a ketiv with no qere, where nothing is read.  Where an atom with a maqaf
   stands before a ketiv that has no qere, the maqaf joins it to the atom after the ketiv, as
   ``mam_simple_verse`` joins MAM's (its ``kq-k-velo-q-maq`` node yields no boundary).  WLC 4.22
   has one such place, 2 Kings 5:18, where יִסְלַח־ stands before the unread ketiv נא and the
   next read atom is יְהוָ֥ה.  Ben's decision, 2026-10-20, was to keep that join: the qere is
   "all we care about for cantillation grammar purposes", in it יסלח־ is one chanted word with
   the name after it (Phonetic MAM's verse, ``gh-pages/phonetic-mam/tnkh/BD-2Kings/05.html``),
   and "there's no reason for our interpretation of WLC to differ from the consensus text".
4. **Section markers.**  A petuxah or setumah is a lone ``P`` or ``S`` run, a nun inversum
   ``N]8``.  None is an atom.
5. **Silluq.**  The chanted word with the verse's first sof pasuq, or the verse's last chanted word
   where it has none, is the one the scanner reads silluq on, and silluq is written U+05BD.  It is
   exempt, because the grammar requires a silluq there and so already reports a verse whose last
   chanted word lacks one.
6. **Paseq.**  Unicode PASEQ is never an accent, whether it is narrow-sense paseq or legarmeh.  A
   legarmeh's chanted word has an accent all the same: the munax of a prose legarmeh, or the azla
   or mahapakh of a poetic one.  A paseq belongs to the atom before it, so a paseq standing alone
   as a run raises: the scanners' legarmeh rules cannot reach across a space, which is what issue
   #215 found in MAM before ``chanted_word_accents_units._fold_lone_bars``.  A chanted word whose
   only mark is the bar, with no munax (or, in a poetic verse, no azla or mahapakh) before it, has
   no accent, so its verse is reported like any other; UXLC 2.6 has two, at Joshua 14:10 and
   1 Samuel 2:16.  Ben's decision, 2026-10-20, was to report such a word, "a word with only a
   legarmeh (no accent)" in his words, rather than stop the run: his concern was that it not
   "whiff by", as a chanted word with no accent did before this rule.
7. **Notes.**  A ``]N`` note marker is part of the atom it follows, even across a maqaf: a word
   that ends with a maqaf keeps its notes after it, and ``fix_apply`` joins the atom after such
   notes to them without a space where a fix gives a word its maqaf (Genesis 18:18's ``]U``).

NAMES ARE NOT EXEMPT.  A name that WLC writes as two atoms gets no exemption, the first atom
being a chanted word like any other.  Ben's decision, 2026-10-20, in his words: "No exception
for these two names, or for any names."  The two were WLC 4.22's פדה צור at Numbers 7:59 and
צורי שדי at Numbers 10:19, each of which MAM writes as one word.

DUAL CANTILLATION.  ``prose_filter`` keeps the dually cantillated verses of Genesis 35:22 and the
Decalogues out of the corpus scan, so the rule never sees WLC's tangled stream, in which an atom's
two marks serve two strands.  ``dual_cant_detangle`` builds each strand with MAM's punctuation and
supplies a strand's accent from MAM where WLC lacks it, the ``SuppliedMark`` charity.

A LIMIT OF THE BODY.  ``uni_to_marks._kq_to_marks`` joins the words of a qere with maqaf marks,
whether the words are a compound or not, so a qere of two chanted words is read here as one
compound and one of its words could lack an accent unnoticed.  The body cannot say which: a qere
of the two words ``A`` and ``B-`` followed by the atom ``C``, and a qere of the one word ``A-``
followed by the atoms ``B-`` and ``C``, are both ``**A-B-C``.
``tests/test_unaccented_chanted_words.py`` holds this reading of WLC 4.22 to a reading of its
``-kq-u`` verses themselves, which has each qere word apart, so the test fails if the limit ever
changes a result.

WHERE IT IS APPLIED.  The prose checker reads it through ``lexical_validation``, as an
``illegal_mark`` with the code ``no accent``, so ``prose_run``, ``fix_tester``,
``almost_errors_trees`` and ``main_uxlc_grammar_test`` all have it.  The poetic checker reads it
through ``poetic_scanner.scan_verse``, which emits a ``NO_ACCENT`` token for each such chanted
word; the grammar has no terminal for it, so the verse is a NO_PARSE stalled there, as a
``STRAY_ACCENT`` verse is.  Two prose verdict paths apply no lexical layer and have no way to show
such a verdict, the detangled dual-cant strands (``dual_cant_detangle``) and the printed-Decalogue
strands and hand transcriptions (``printed_decalogue.parse_marks_body``); there
``raise_on_unaccented_chanted_words`` makes the case a failure instead of a clean verdict on a
chanted verse the grammar did not wholly see.  Neither path had such a chanted word when this
was written, on 2026-10-20.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from accgram import accent_marks as am

_ACCENT_LO = "\N{HEBREW ACCENT ETNAHTA}"  # U+0591
_ACCENT_HI = "\N{HEBREW ACCENT ZINOR}"  # U+05AE

# The runs that are section markers, rule 4.
_SECTION_RUNS = frozenset(("P", "S", "N]8"))
# The run openers of rules 2 and 3.  Tested qere first, since a qere opener starts with a
# ketiv opener.
_KETIV = "*"
_QERE = "**"
_EMPTY_QERE = "**qq"
_NOTE = "]"
# A run of ``]N`` note markers, the form ``uni_to_marks`` appends them in.
_LEADING_NOTES_RE = re.compile(r"(?:\][A-Za-z0-9])+")


@dataclass(frozen=True)
class Atom:
    """One read atom of a chanted word, as the mark body has it."""

    start: int  # the offset of its first character in the body
    marks: (
        str  # its run of the body: a qere's ``**`` and note markers included, maqaf not
    )
    read_index: int  # its ordinal among the verse's read atoms, from 0


@dataclass(frozen=True)
class ChantedWord:
    """One chanted word: a lone atom, or the atoms of a maqaf compound, in order."""

    atoms: tuple[Atom, ...]

    @property
    def start(self) -> int:
        return self.atoms[0].start

    @property
    def end(self) -> int:
        last = self.atoms[-1]
        return last.start + len(last.marks)

    @property
    def marks(self) -> str:
        return am.MAQAF.join(atom.marks for atom in self.atoms)

    @property
    def has_accent(self) -> bool:
        return any(
            _ACCENT_LO <= ch <= _ACCENT_HI for atom in self.atoms for ch in atom.marks
        )


def chanted_words(body: str) -> list[ChantedWord]:
    """Every chanted word of a verse's mark body, in order, by rules 1 to 4, 6 and 7."""
    words: list[ChantedWord] = []
    pending: list[Atom] = []
    read_index = 0
    run_start = 0
    for run in body.split(" "):
        offset = run_start
        run_start += len(run) + 1
        if not run:
            continue
        if run in _SECTION_RUNS:
            if pending:
                raise ValueError(f"a maqaf joins an atom to a section marker: {body!r}")
            continue
        pieces = run.split(am.MAQAF)
        in_ketiv = False
        for k, piece in enumerate(pieces):
            start = offset
            offset += len(piece) + 1
            read = _is_read_atom(piece, in_ketiv=in_ketiv, after_maqaf=k > 0, body=body)
            if piece.startswith(_KETIV) and not piece.startswith(_QERE):
                in_ketiv = True
            if not read:
                continue
            pending.append(Atom(start=start, marks=piece, read_index=read_index))
            read_index += 1
            if k == len(pieces) - 1:
                # No maqaf after this atom: the chanted word ends here.  An atom with a maqaf
                # after it stays pending, through a ketiv, until the next read atom joins it.
                words.append(ChantedWord(tuple(pending)))
                pending = []
    if pending:
        words.append(ChantedWord(tuple(pending)))
    return words


def unaccented_chanted_words(body: str) -> list[ChantedWord]:
    """Every chanted word of the body with no accent, the silluq's excepted (rule 5)."""
    words = chanted_words(body)
    silluq_at = _silluq_word_index(words)
    return [
        word for i, word in enumerate(words) if i != silluq_at and not word.has_accent
    ]


def raise_on_unaccented_chanted_words(body: str, where: str) -> None:
    """Raise if ``body`` has a chanted word with no accent, for a path that cannot show one.

    For the verdict paths that apply no lexical layer, named in the module docstring: a chanted
    word with no accent there would leave the grammar a verse it reads as if the chanted word
    were not there, and the clean verdict it might return would be a claim about a different
    verse.  Ben's decision, 2026-10-20: keep this check, which stops the run, until a real case
    appears, rather than give those paths the lexical layer and a status their pages can show.
    """
    words = unaccented_chanted_words(body)
    if words:
        raise ValueError(
            f"{where}: a chanted word with no accent, which this verdict path has no way to"
            f" record (accgram.unaccented_chanted_words): {[w.marks for w in words]}"
        )


def _is_read_atom(piece: str, *, in_ketiv: bool, after_maqaf: bool, body: str) -> bool:
    """Whether ``piece``, one maqaf-delimited piece of a run, is an atom that is read.

    False for every piece of a ketiv (rule 2), for the empty-qere placeholder (rule 3) and for
    the empty piece a maqaf with no atom after it leaves (rule 1).  Raises on every piece no
    rule names.
    """
    if in_ketiv:
        return False
    if after_maqaf:
        # Note markers after a maqaf belong to the atom before it (rule 7); what follows
        # them, if anything, is the piece to classify.
        piece = _LEADING_NOTES_RE.sub("", piece, count=1)
    if piece == _EMPTY_QERE:
        return False
    if piece.startswith(_QERE):
        return True
    if piece.startswith(_KETIV):
        return False
    if not piece:
        return False
    if piece.startswith(_NOTE):
        raise ValueError(f"a note marker with no atom before it: {body!r}")
    if piece in _SECTION_RUNS:
        raise ValueError(f"a section marker joined to an atom by a maqaf: {body!r}")
    if piece.partition(_NOTE)[0] == am.PASEQ:
        raise ValueError(f"a paseq standing alone, belonging to no atom: {body!r}")
    return True


def _silluq_word_index(words: list[ChantedWord]) -> int | None:
    """Rule 5: the chanted word with the first sof pasuq, else the last chanted word."""
    for i, word in enumerate(words):
        if any(am.SOF_PASUQ in atom.marks for atom in word.atoms):
            return i
    return len(words) - 1 if words else None
