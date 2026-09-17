"""Unicode properties with fallbacks for characters newer than Python's UCD."""

import unicodedata

from mb_cmn import hebrew_points as hpo

_FALLBACKS = {
    hpo.SHEVA_NA: ("HEBREW POINT SHEVA NA MUDGASH", "Mn", 10),
    hpo.DAGESH_XAZAQ: ("HEBREW POINT DAGESH HAZAQ MUDGASH", "Mn", 21),
}
_MISSING = object()


def name(character: str, default: object = _MISSING) -> str:
    """Return the Unicode name, including the two Hebrew additions in Unicode 18."""
    if fallback := _FALLBACKS.get(character):
        return fallback[0]
    if default is _MISSING:
        return unicodedata.name(character)
    return unicodedata.name(character, default)


def category(character: str) -> str:
    """Return the general category, including Unicode 18's U+05C8 and U+05C9."""
    if fallback := _FALLBACKS.get(character):
        return fallback[1]
    return unicodedata.category(character)


def combining(character: str) -> int:
    """Return the combining class, including Unicode 18's U+05C8 and U+05C9."""
    if fallback := _FALLBACKS.get(character):
        return fallback[2]
    return unicodedata.combining(character)


def is_mark(character: str) -> bool:
    """Whether ``character`` has a Unicode Mark general category."""
    return category(character).startswith("M")
