"""Exports letter_only_diff"""

import re
from pydiff_mm import diff_mm_uni_name


def letter_only_diff(str1, str2):
    """If the only diffs between str1 and str2 are letter substitutions
    (same count and positions of non-letter content), describe them."""
    if _neutralize_letters(str1) != _neutralize_letters(str2):
        return None
    units1 = _extract_letter_units(str1)
    units2 = _extract_letter_units(str2)
    if len(units1) != len(units2):
        return None
    swaps = []
    for u1, u2 in zip(units1, units2):
        if u1 != u2:
            swaps.append((_letter_unit_name(u1), _letter_unit_name(u2)))
    if not swaps:
        return None
    parts = [f"{old} → {new}" for old, new in swaps]
    detail = "replace letter: " + ", ".join(parts)
    return detail, "letter swap"


_LETTER_RE = re.compile(r"[\u05D0-\u05EA]")
_SHINSINDOT_RE = re.compile(r"[\u05C1\u05C2]")


def _neutralize_letters(string):
    """Replace Hebrew letters and shin/sin dots with a common placeholder.
    Shin/sin dots are part of the letter's identity, so they are stripped too."""
    string = string.replace("\u05c1", "").replace("\u05c2", "")
    return _LETTER_RE.sub("א", string)


def _extract_letter_units(string):
    """Extract ordered letter units from a string.
    A letter unit is a Hebrew letter optionally followed by a shin/sin dot."""
    units = []
    i = 0
    while i < len(string):
        if _LETTER_RE.match(string[i]):
            unit = string[i]
            if i + 1 < len(string) and _SHINSINDOT_RE.match(string[i + 1]):
                unit += string[i + 1]
            units.append(unit)
        i += 1
    return units


def _letter_unit_name(unit):
    """Human-friendly name for a letter unit (letter + optional shin/sin dot)."""
    base = diff_mm_uni_name.name(unit[0])
    if len(unit) > 1:
        return f"{base} (with {diff_mm_uni_name.name(unit[1])})"
    return base
