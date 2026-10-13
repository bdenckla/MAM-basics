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


def _is_letter(char):
    return "א" <= char <= "ת"


def needs_expansion(atom):
    """Screen a contiguous Hebrew atom; punctuation and single letters do not match."""
    clusters = []
    for char in atom:
        if _is_letter(char):
            clusters.append((char, set()))
        elif ucd.is_mark(char) and clusters:
            clusters[-1][1].add(char)
        else:
            return False
    return len(clusters) > 1 and any(
        letter in _NARROW_LETTERS
        and marks & _BROAD_BELOW_VOWELS
        and marks & ha.UNI_UNDER_ACCENTS
        for letter, marks in clusters
    )


def html_for_text(text):
    """Wrap selected Hebrew atoms, preserving all characters and separators.

    Spaces, maqafs and punctuation stay outside the spacing span. Combining marks,
    including Phonetic MAM's newer Hebrew points, stay with their base letter.
    """
    result = []
    start = index = 0
    while index < len(text):
        if not _is_letter(text[index]):
            index += 1
            continue
        end = index + 1
        while end < len(text) and (_is_letter(text[end]) or ucd.is_mark(text[end])):
            end += 1
        atom = text[index:end]
        if needs_expansion(atom):
            if start < index:
                result.append(text[start:index])
            result.append(mb_html.span_c(atom, CLASS))
            start = end
        index = end
    if not result:
        return text
    if start < len(text):
        result.append(text[start:])
    return tuple(result)
