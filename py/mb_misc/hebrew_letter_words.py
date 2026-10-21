"""Exports letters_and_maqafs"""

import unicodedata

from mb_cmn import hebrew_punctuation as hpu

_LETTERS = frozenset(chr(cp) for cp in range(0x05D0, 0x05EB))
# Punctuation that ends a chanted word or stands alone between two of them.
_EDGE_PUNCTUATION = frozenset(
    hpu.SOPA + hpu.PASOLEG + "\N{HEBREW PUNCTUATION NUN HAFUKHA}"
)
# A letter's marks: the Hebrew accents and points, the sheva-na and dagesh-xazaq
# annotation points U+05C8 and U+05C9 included, and the combining grapheme joiner
# and varika that MAM places among them.
_MARKS = (
    frozenset(
        [chr(cp) for cp in range(0x0591, 0x05CA)]
        + ["\N{COMBINING GRAPHEME JOINER}", "\N{HEBREW POINT JUDEO-SPANISH VARIKA}"]
    )
    - _EDGE_PUNCTUATION
    - {hpu.MAQ}
)


def letters_and_maqafs(string: str):
    """Return only the letters and maqaf marks in the given string

    I.e. strip any vowel points and/or accents. The string is one chanted word,
    or part of one. A gray maqaf in it is a maqaf. Whitespace, a sof pasuq, the
    paseq/legarmeh glyph and an inverted nun may stand only at either end, and
    any other character raises, so that two words cannot be run together.
    """
    out = []
    for ch in _without_edges(string):
        if ch in _LETTERS or ch == hpu.MAQ:
            out.append(ch)
        elif ch == hpu.NU_GMAQ:
            out.append(hpu.MAQ)
        elif ch not in _MARKS:
            name = unicodedata.name(ch, repr(ch))
            raise ValueError(f"letters_and_maqafs has no rule for {name} in {string!r}")
    return "".join(out)


def _without_edges(string: str) -> str:
    """``string`` without the whitespace and edge punctuation at either end."""
    start, end = 0, len(string)
    while start < end and _is_edge(string[start]):
        start += 1
    while end > start and _is_edge(string[end - 1]):
        end -= 1
    return string[start:end]


def _is_edge(ch: str) -> bool:
    return ch.isspace() or ch in _EDGE_PUNCTUATION
