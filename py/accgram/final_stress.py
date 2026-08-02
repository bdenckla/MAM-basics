r"""Is a chanted word stressed on its last syllable?

ONE QUESTION, NOT A PHONOLOGY LAYER.  Issue wlc-utils#48 wants syllabification, open-versus-closed
syllables and a short-versus-long vowel determination derived from the pointing, and it says
plainly: do not build that from scratch, reuse ``../al-hatorah/py/aht_phon``.  This module does not
build it.  It answers one question that needs none of what wlc-utils#48 is hard about -- no open/closed, no
short/long, no qamats gadol against qamats qatan: does the accent fall at or after the point where
the chanted word's LAST syllable begins?  An impositive accent is written on the stressed syllable,
so that question and "is this chanted word stressed on its last syllable" are the same question
asked of a text that already has accents on it.

Ben, 2026-07-31, stating the rule this module implements: "if there's only one vowel sound left in
the word, and a geresh is on it, we can assume that the word is finally stressed".

WHY NOT ``aht_phon`` ITSELF.  It cannot be imported here: a cross-repo import would need
``sys.path`` surgery, which this repo forbids outright, and al-hatorah is private besides.  What is
importable is its OUTPUT, which is wlc-utils#48's second path -- and that is what
``py/tests/test_final_stress_vs_phonetic_mam.py`` does, checking every verdict this module reaches
against Phonetic MAM's real stress model.  So the rule here is measured against the engine rather
than standing in for it.

NUCLEI, NOT SYLLABLES.  A syllable's boundaries are the hard part; its NUCLEUS is a point written
in the text.  So the rule finds the last nucleus, backs up to the consonant that carries it, and
asks whether the accent is at or after that consonant.  Nothing else about the chanted word is
looked at, and no syllable but the last one is ever located.  Four things decide what counts as a
nucleus:

* A full vowel or a xataf is one.  So is a SHURUQ -- a vav with a dagesh point, no vowel of its
  own, and no nucleus on the letter before it, which is what tells a shuruq from a doubled vav
  closing the syllable before it (the two vavs of ויצוו differ in exactly that).
* A SHEVA is not, and is ignored rather than judged vocal or silent.  Ignoring it cannot move the
  last nucleus: a vocal sheva is always followed by a full vowel, which is counted in its own
  right, and a silent one closes a syllable that already has its nucleus.  So the
  vocal-versus-silent question, which is real phonology, never arises.
* A FURTIVE PATAX is not: a patax written on the last base letter of an atom, that letter being
  xet, ayin or he, is pronounced before the guttural rather than after it and opens no syllable.
  Without this rule מזבח and רוח both come out penultimately stressed, and both are stressed on
  the last syllable they have.
* A MATER LECTIONIS needs no rule of its own, because nuclei are read off POINTS and not off
  letters: an unpointed alef, he, vav or yod simply has none.

BACKING UP TO THE ONSET is the one place a syllable, rather than a nucleus, has to be located, and
it is needed at both ends.  A xolam male or a shuruq writes the vowel on a VAV that is a mater, so
the nucleus of שלום sits one letter after the consonant whose syllable it is -- and the accent is
on that consonant.  Pulling the other way, an accent is sometimes written on a mater AFTER the
vowel it belongs with: WLC has the ole of לא־היה on the final he, a letter with no point on it at
all.  Asking whether the accent is at or after the last syllable's ONSET reads both cases right,
where asking about the nucleus itself misreads one or the other.

WHAT IT DOES NOT DO.  It says nothing about which syllable is stressed when the mark that would
tell is written at the chanted word's edge instead: ``NOT_IMPOSITIVE`` is the list of those, and
``maqaf_nonfinal_accents.stress_mark_letter`` gives this module no letter for a chanted word whose
last mark is one of them.  A postpositive accent's stress helper does carry the information, and it
is left alone -- reading a helper would mean deciding which of two same-codepoint copies is the
helper, which is the survey's business rather than this module's.
"""

from __future__ import annotations

from accgram import accent_marks as am
from accgram.uni_to_marks import is_base_letter
from mb_cmn import hebrew_points as hpo

MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"

_VAV = "\N{HEBREW LETTER VAV}"

# The three letters a furtive patax is written on, all of them at the end of an atom.
_FURTIVE_HOSTS = frozenset(
    (
        "\N{HEBREW LETTER HET}",
        "\N{HEBREW LETTER AYIN}",
        "\N{HEBREW LETTER HE}",
    )
)

# The two ways a vowel is written on a vav that is a mater rather than a consonant: the xolam of a
# xolam male, and the dagesh point of a shuruq.  A nucleus written either way belongs to the
# consonant before the vav, which is where the accent for that syllable goes.
_ON_A_VAV_MATER = frozenset((hpo.XOLAM, hpo.XOLAM_XFV, hpo.DAGOMOSD))

# Accents written at a fixed EDGE of the chanted word rather than on its stress, so their position
# answers no question about which syllable is stressed.  Moved here from
# ``maqaf_nonfinal_accents``, whose oracle skips exactly these for exactly this reason: which
# accents mark the stress is a fact about stress, and this is the module about stress.
NOT_IMPOSITIVE = frozenset(
    (
        am.PASHTA,
        am.TELISHA_QETANA,
        am.SEGOLTA,
        am.TSINNOR,
        am.TSINNORIT,
        am.YETIV,
        am.DEXI,
        am.TELISHA_GEDOLA,
        am.GERESH_MUQDAM,
    )
)

# Every point that is a syllable nucleus: the full vowels, the three xatafs, and qamats qatan.
# The sheva is deliberately absent -- see the module docstring on why it needs no verdict.  A
# shuruq is a nucleus too but is not a point of its own, so ``_nuclei`` reads it separately.
_NUCLEUS_POINTS = frozenset(
    (
        hpo.XIRIQ,
        hpo.TSERE,
        hpo.SEGOL_V,
        hpo.PATAX,
        hpo.QAMATS,
        hpo.QAMATS_Q,
        hpo.XOLAM,
        hpo.XOLAM_XFV,
        hpo.QUBUTS,
        hpo.XSEGOL,
        hpo.XPATAX,
        hpo.XQAMATS,
    )
)


def _letters(word: str) -> list[list]:
    """``[base letter, the marks written on it, whether it ends its atom]``, one per base letter.

    Every mark is filed against the letter it follows, the same keying
    ``maqaf_nonfinal_accents._accents_share_a_letter`` uses.  The atom-end flag is what the
    furtive-patax rule needs: a maqaf compound has an atom end in the middle of it, and a
    non-final atom can end in a furtive patax as readily as the compound does.
    """
    out: list[list] = []
    for char in word:
        if is_base_letter(char):
            out.append([char, "", False])
        elif char == MAQAF:
            if out:
                out[-1][2] = True
        elif out:
            out[-1][1] += char
    if out:
        out[-1][2] = True
    return out


def _is_furtive(letter: str, vowels: list[str], atom_final: bool) -> bool:
    """Whether the patax on this letter is the furtive one, which opens no syllable."""
    return atom_final and letter in _FURTIVE_HOSTS and vowels == [hpo.PATAX]


def ends_in_furtive_patax(word: str) -> bool:
    """Whether the chanted word's last letter has a furtive patax on it.

    Public because Phonetic MAM has the furtive patax as a syllable of its own where this module
    counts no nucleus for it, and the differential test has to hold that difference steady rather
    than read it as a disagreement about the stress.
    """
    letters = _letters(word)
    if not letters:
        return False
    letter, marks, atom_final = letters[-1]
    return _is_furtive(letter, [m for m in marks if m in _NUCLEUS_POINTS], atom_final)


def _nuclei(word: str) -> list[tuple[int, int]]:
    """Where each of the chanted word's syllables begins, as ``(letter ordinal, tie-break)``.

    Ordinals count base letters from 1 across the whole chanted word, maqafs included, so a
    compound's atoms number straight through as the one chanted word they are.  The tie-break is
    0 for a syllable whose onset is a written letter and 1 for one whose onset is not, which puts
    the second sort between that letter and the next; ``is_final_stress`` compares an accent's
    ordinal against the pair, and an accent is always written on a letter.

    A syllable with no written onset is what a letter carrying TWO vowels stands for -- the ketiv
    ירושלם, whose lamed has a patax and, past a combining grapheme joiner, the hiriq of the
    unwritten yod the qere reads.  Those are two syllables, la and yim, and the accent on the
    lamed is on the first of them.
    """
    out: list[tuple[int, int]] = []
    previous_has_nucleus = False
    for ordinal, (letter, marks, atom_final) in enumerate(_letters(word), start=1):
        vowels = [mark for mark in marks if mark in _NUCLEUS_POINTS]
        if vowels:
            has_nucleus = not _is_furtive(letter, vowels, atom_final)
            on_a_mater = letter == _VAV and vowels[0] in _ON_A_VAV_MATER
        else:
            # A vav with a dagesh point and no vowel is a shuruq, unless the letter before it has
            # a nucleus -- in which case the dagesh doubles a consonantal vav and opens no
            # syllable of its own.
            has_nucleus = (
                letter == _VAV and hpo.DAGOMOSD in marks and not previous_has_nucleus
            )
            on_a_mater = has_nucleus
            vowels = [hpo.DAGOMOSD] if has_nucleus else []
        if has_nucleus:
            onset = ordinal - 1 if on_a_mater and ordinal > 1 else ordinal
            out.extend((onset, tie) for tie in range(len(vowels)))
        previous_has_nucleus = has_nucleus
    return out


def last_syllable_onset(word: str) -> tuple[int, int] | None:
    """Where the chanted word's last syllable begins -- see ``_nuclei`` for the pair's two parts.

    None for a chanted word with no nucleus at all, which no real one has.
    """
    nuclei = _nuclei(word)
    return nuclei[-1] if nuclei else None


def is_final_stress(word: str, accent_letter: int) -> bool:
    """Whether an accent on the base letter at ordinal ``accent_letter`` is on the last syllable.

    The caller supplies the letter because deciding which mark is the main accent needs what this
    module has no business knowing -- whether a U+05BD is the silluq, which turns on the chanted
    word being the verse's last, and which copy of a doubled mark is the stress helper.
    ``maqaf_nonfinal_accents.stress_mark_letter`` is the caller that answers both.

    A chanted word with no nucleus would leave the accent on nothing, so it stops the build rather
    than being scored either way.
    """
    onset = last_syllable_onset(word)
    assert onset is not None, f"an accent on a chanted word with no vowel: {word!r}"
    return (accent_letter, 0) >= onset
