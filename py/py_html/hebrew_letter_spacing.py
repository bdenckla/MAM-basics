"""Conservative screening for cramped pointed-Hebrew text in Taamey D.

This is a typography heuristic, not a collision detector. A narrow letter with
a broad below-letter vowel and a below-letter accent can crowd neighboring ink
even after the font has avoided overlap. The first NAEE trial expands such atoms
by 0.06em. The classifier is independent of edition data and HTML rendering.

HTML conversion sees contiguous text leaves after semantic rendering. Atoms split
by special-letter or vowel-variant spans may be missed or only partly expanded;
single-letter leaves are left alone. No source character or mark order changes.
"""

from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_points as hp
from mb_cmn import unicode_data as ucd
from mb_misc import mb_html

CLASS = "hebrew-expanded-spacing"
NARROW_VOWEL_ACCENT = "narrow-vowel-accent"
ADJACENT_NARROW_BELOW = "adjacent-narrow-below"
QOF_PREDECESSOR_BELOW = "qof-predecessor-below"
_NARROW_LETTERS = frozenset(
    (
        "\N{HEBREW LETTER YOD}",
        "\N{HEBREW LETTER VAV}",
        "\N{HEBREW LETTER FINAL NUN}",
    )
)
_BROAD_BELOW_VOWELS = frozenset(
    (hp.TSERE, hp.SEGOL_V, hp.XSEGOL, hp.XPATAX, hp.XQAMATS, hp.QUBUTS)
)
# The broader narrow-letter class in the frozen Taamey D source's @narlets.
_NARROW_PAIR_LETTERS = _NARROW_LETTERS | frozenset(
    (
        "\N{HEBREW LETTER GIMEL}",
        "\N{HEBREW LETTER ZAYIN}",
        "\N{HEBREW LETTER NUN}",
    )
)
_BELOW_VOWELS = _BROAD_BELOW_VOWELS | frozenset(
    (hp.SHEVA, hp.SHEVA_NA, hp.XIRIQ, hp.PATAX, hp.QAMATS, hp.QAMATS_Q)
)
_BELOW_ACCENTS_OR_METEG = ha.UNI_UNDER_ACCENTS | {hp.MTGOSLQ}
_BELOW_MARKS = _BELOW_VOWELS | _BELOW_ACCENTS_OR_METEG


def _is_letter(char):
    return "א" <= char <= "ת"


def types_for_atom(atom):
    """Identify overlapping crowding families, including additional FOI trial types.

    A matching shape is a candidate for visual judgment. Only the original
    narrow-vowel-accent family currently opts into automatic NAEE expansion.
    """
    clusters = []
    for char in atom:
        if _is_letter(char):
            clusters.append((char, set()))
        elif ucd.is_mark(char) and clusters:
            clusters[-1][1].add(char)
        else:
            return ()
    if len(clusters) < 2:
        return ()
    types = []
    if any(
        letter in _NARROW_LETTERS
        and marks & _BROAD_BELOW_VOWELS
        and marks & ha.UNI_UNDER_ACCENTS
        for letter, marks in clusters
    ):
        types.append(NARROW_VOWEL_ACCENT)
    pairs = tuple(zip(clusters, clusters[1:]))
    if any(
        first in _NARROW_PAIR_LETTERS
        and second in _NARROW_PAIR_LETTERS
        and first_marks & _BELOW_MARKS
        and second_marks & _BELOW_MARKS
        and (first_marks | second_marks)
        & (_BROAD_BELOW_VOWELS | _BELOW_ACCENTS_OR_METEG)
        for (first, first_marks), (second, second_marks) in pairs
    ):
        types.append(ADJACENT_NARROW_BELOW)
    if any(
        second == "\N{HEBREW LETTER QOF}"
        and first_marks & _BELOW_MARKS
        and second_marks & _BELOW_MARKS
        for (_, first_marks), (second, second_marks) in pairs
    ):
        types.append(QOF_PREDECESSOR_BELOW)
    return tuple(types)


def needs_expansion(atom):
    """Apply the active NAEE spacing rule, leaving broader FOI families as trials."""
    return NARROW_VOWEL_ACCENT in types_for_atom(atom)


def iter_atoms(text):
    """Yield start, end and text of Hebrew atoms within a text run."""
    index = 0
    while index < len(text):
        if not _is_letter(text[index]):
            index += 1
            continue
        end = index + 1
        while end < len(text) and (_is_letter(text[end]) or ucd.is_mark(text[end])):
            end += 1
        yield index, end, text[index:end]
        index = end


def html_for_text(text):
    """Wrap selected Hebrew atoms, preserving all characters and separators.

    Spaces, maqaf marks and punctuation stay outside the spacing span. Combining marks,
    including Phonetic MAM's newer Hebrew points, stay with their base letter.
    """
    result = []
    start = 0
    for index, end, atom in iter_atoms(text):
        if needs_expansion(atom):
            if start < index:
                result.append(text[start:index])
            result.append(mb_html.span_c(atom, CLASS))
            start = end
    if not result:
        return text
    if start < len(text):
        result.append(text[start:])
    return tuple(result)
