"""Exports maqaf_space_diff"""

from mb_cmn.hebrew_punctuation import MAQ as _MAQAF


def maqaf_space_diff(str1, str2):
    """If the only diffs between str1 and str2 are maqaf/space related, describe them."""
    # Case 1: same length, maqaf↔space swaps at matching positions
    if str1.replace(_MAQAF, " ") == str2.replace(_MAQAF, " "):
        m2s = sum(1 for a, b in zip(str1, str2) if a == _MAQAF and b == " ")
        s2m = sum(1 for a, b in zip(str1, str2) if a == " " and b == _MAQAF)
        if m2s > 0 and s2m > 0:
            return None  # mixed directions, too complex
        if m2s > 0:
            return f"replace {m2s} maqaf mark(s) with space", "maqaf/space"
        if s2m > 0:
            return f"replace {s2m} space(s) with maqaf", "maqaf/space"
    # Case 2: one string is the other plus a trailing maqaf
    if str1 == str2 + _MAQAF:
        return "remove trailing maqaf", "maqaf/space"
    if str1 + _MAQAF == str2:
        return "add trailing maqaf", "maqaf/space"
    return None
