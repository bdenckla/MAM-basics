"""Infer the explicit xataf vowel from a shewa+varika word.

Rules (derived from Yeivin §387–390 and confirmed against all 664 entries):

1. Before guttural (א/ה/ח/ע) + qamats → ḥataf-qamats
2. Before guttural (א/ה/ח/ע) + ḥiriq → ḥiriq (pseudo ḥataf-ḥiriq)
3. Otherwise → ḥataf-pataḥ
"""

from pycmn import hebrew_letters as hle
from pycmn import hebrew_points as hpo

GUTTURALS = frozenset({hle.ALEF, hle.HE, hle.XET, hle.AYIN})

_HEBREW_LETTER_RANGE = range(ord("א"), ord("ת") + 1)

_VOWELS = frozenset(
    {
        hpo.SHEVA,
        hpo.XSEGOL,
        hpo.XPATAX,
        hpo.XQAMATS,
        hpo.XIRIQ,
        hpo.TSERE,
        hpo.SEGOL_V,
        hpo.PATAX,
        hpo.QAMATS,
        hpo.QAMATS_Q,
        hpo.XOLAM,
        hpo.XOLAM_XFV,
        hpo.QUBUTS,
    }
)


def _is_letter(ch):
    return ord(ch) in _HEBREW_LETTER_RANGE


def _next_consonant_and_vowel(word, after_idx):
    """Find the next consonant after after_idx and its vowel.

    Returns (consonant_char, vowel_char) or (None, None).
    """
    cons = None
    for i in range(after_idx + 1, len(word)):
        ch = word[i]
        if _is_letter(ch):
            if cons is not None:
                return cons, None
            cons = ch
        elif cons is not None and ch in _VOWELS:
            return cons, ch
    return cons, None


def _infer_replacement_at(varika_word, varika_idx):
    """Infer what should replace the shewa+varika at varika_idx."""
    cons, vowel = _next_consonant_and_vowel(varika_word, varika_idx)
    if cons in GUTTURALS:
        if vowel in (hpo.QAMATS, hpo.QAMATS_Q):
            return hpo.XQAMATS
        if vowel == hpo.XIRIQ:
            return hpo.XIRIQ
    return hpo.XPATAX


def _varika_positions(varika_word):
    """Return list of (consonant, varika_index) for each varika in the word.

    Handles multiple varikas, e.g. Judges 7:7 הַֽמְﬞלַֽקְﬞקִים֙.
    """
    positions = []
    last_letter = None
    for i, ch in enumerate(varika_word):
        if _is_letter(ch):
            last_letter = ch
        elif ch == hpo.VARIKA:
            positions.append((last_letter, i))
    return positions


def infer_replacement(varika_word):
    """Infer what should replace shewa+varika in the given word.

    Returns the replacement string: a ḥataf vowel, or ḥiriq (for pseudo
    ḥataf-ḥiriq).  Returns None if the word has no varika.

    For words with a single varika only. For multiple varikas, use
    _varika_positions and _infer_replacement_at directly.
    """
    positions = _varika_positions(varika_word)
    if not positions:
        return None
    _cons, vi = positions[0]
    return _infer_replacement_at(varika_word, vi)


def _marks_on_letter(word, letter_occ):
    """Return the set of marks on the letter_occ-th occurrence (0-based) of any letter."""
    cons_idx = -1
    on_target = False
    marks = set()
    for ch in word:
        if _is_letter(ch):
            if on_target:
                return marks
            cons_idx += 1
            on_target = cons_idx == letter_occ
        elif on_target:
            marks.add(ch)
    return marks


def is_inferrable(varika_word, xataf_word):
    """Return True if every inferred ḥataf vowel appears on the relevant
    consonant in the xataf word.

    Checks all varikas in the word — e.g. Judges 7:7 הַֽמְﬞלַֽקְﬞקִים֙
    has two varikas and both must be inferrable.

    The xataf word doesn't have to be the entire varika word with the
    shewa+varika replaced — it just has to contain each consonant that
    carried shewa+varika with the inferred ḥataf vowel among its marks.
    """
    positions = _varika_positions(varika_word)
    if not positions:
        return True
    for cons, vi in positions:
        inferred = _infer_replacement_at(varika_word, vi)
        found = False
        cons_idx = -1
        for ch in xataf_word:
            if _is_letter(ch):
                cons_idx += 1
                if ch == cons:
                    marks = _marks_on_letter(xataf_word, cons_idx)
                    if inferred in marks:
                        found = True
                        break
        if not found:
            return False
    return True
