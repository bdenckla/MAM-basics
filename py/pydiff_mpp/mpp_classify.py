"""
Classify MPP EP column diffs by analyzing Unicode character differences.

Exports:
    classify_diffs  — add a 'category' field to each diff dict
"""

import difflib
from pycmn import hebrew_points as hpo
from pydiff_mpp.mpp_extract import _collect_template_names

# ── Character classification ─────────────────────────────────


def _char_type(c):
    """Classify a single character by its role in Hebrew text."""
    cp = ord(c)
    if cp == ord(hpo.MTGOSLQ):  # U+05BD meteg/siluq
        return "meteg"
    if cp == ord(hpo.VARIKA):  # U+FB1E varika
        return "varika"
    if 0x0591 <= cp <= 0x05AF:  # cantillation marks (excluding meteg)
        return "accent"
    if cp == ord(hpo.DAGOMOSD):  # U+05BC dagesh/mapiq
        return "dagesh"
    if cp in (ord(hpo.SHIND), ord(hpo.SIND)):  # shin/sin dot
        return "shin-sin-dot"
    if cp == ord(hpo.RAFE):  # U+05BF rafe
        return "rafe"
    vowel_cps = {
        ord(hpo.SHEVA),
        ord(hpo.XSEGOL),
        ord(hpo.XPATAX),
        ord(hpo.XQAMATS),
        ord(hpo.XIRIQ),
        ord(hpo.TSERE),
        ord(hpo.SEGOL_V),
        ord(hpo.PATAX),
        ord(hpo.QAMATS),
        ord(hpo.QAMATS_Q),
        ord(hpo.XOLAM),
        ord(hpo.XOLAM_XFV),
        ord(hpo.QUBUTS),
    }
    if cp in vowel_cps:
        return "vowel"
    if 0x05D0 <= cp <= 0x05EA:
        return "letter"
    if cp == 0x05C0:  # paseq
        return "paseq"
    if cp == 0x05C3:  # sof pasuq
        return "sof-pasuq"
    if cp == 0x05BE:  # maqaf
        return "maqaf"
    if cp == 0x200C:  # ZWNJ
        return "zwnj"
    if c == " ":
        return "space"
    return "other"


# ── Text diff analysis ───────────────────────────────────────


def _get_char_diffs(old_text, new_text):
    """Return (added_types, removed_types) as sets of char type strings."""
    sm = difflib.SequenceMatcher(None, old_text, new_text, autojunk=False)
    added = []
    removed = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "delete":
            removed.extend(old_text[i1:i2])
        elif op == "insert":
            added.extend(new_text[j1:j2])
        elif op == "replace":
            removed.extend(old_text[i1:i2])
            added.extend(new_text[j1:j2])
    added_types = set(_char_type(c) for c in added)
    removed_types = set(_char_type(c) for c in removed)
    return added_types, removed_types


def _has_reuveni(text):
    """Check if text contains the consonant skeleton ראובני."""
    consonants = "".join(c for c in text if 0x05D0 <= ord(c) <= 0x05EA)
    return "ראובני" in consonants


def _classify_text_change(diff):
    """Classify a diff where the body text actually changed."""
    old_text = diff["old_text"]
    new_text = diff["new_text"]
    added, removed = _get_char_diffs(old_text, new_text)
    non_space_added = added - {"space"}
    non_space_removed = removed - {"space"}
    # Pure meteg removal
    if non_space_removed == {"meteg"} and not non_space_added:
        return "meteg-removal"
    # Pure meteg addition
    if non_space_added == {"meteg"} and not non_space_removed:
        return "meteg-addition"
    # Varika (U+FB1E) addition — implicit hataf vowels
    if (
        "varika" in non_space_added
        and non_space_added <= {"varika"}
        and not non_space_removed
    ):
        return "varika"
    if "varika" in non_space_added and non_space_removed <= {"meteg"}:
        return "varika"
    # Rafe (U+05BF) addition — quiescent consonants (ראובני words)
    if (
        "rafe" in non_space_added
        and non_space_added <= {"rafe"}
        and not non_space_removed
    ):
        return "rafe-reuveni"
    if "rafe" in non_space_added and non_space_removed <= {"meteg"}:
        return "rafe-reuveni"
    # Accent replaced with different accent
    if non_space_added == {"accent"} and non_space_removed == {"accent"}:
        return "accent-change"
    # Accent added (no accent removed)
    if "accent" in non_space_added and "accent" not in non_space_removed:
        return "accent-addition"
    # Accent removed (no accent added)
    if "accent" in non_space_removed and "accent" not in non_space_added:
        return "accent-removal"
    # Any change involving paseq (legarmeh / paseq additions, removals, spacing)
    if "paseq" in non_space_added or "paseq" in non_space_removed:
        return "legarmeih-paseq"
    if not non_space_added and not non_space_removed:
        return "legarmeih-paseq"
    # Vowel change
    if non_space_added <= {"vowel"} and non_space_removed <= {"vowel"}:
        return "vowel-change"
    # ZWNJ insertion
    if non_space_added == {"zwnj"} and not non_space_removed:
        return "misc"
    # Sof pasuq change
    if "sof-pasuq" in non_space_added or "sof-pasuq" in non_space_removed:
        return "misc"
    return "misc"


def _classify_structural_change(diff):
    """Classify a diff where structure changed but body text didn't."""
    # Check for legarmeih → paseq pattern by looking at template names
    old_names = set(_collect_template_names(diff["old_ep"]))
    new_names = set(_collect_template_names(diff["new_ep"]))
    _LEGAR = {"מ:לגרמיה", "מ:לגרמיה-2"}
    if _LEGAR & (old_names ^ new_names):
        return "legarmeih-paseq"
    return "template-change"


# ── Public API ───────────────────────────────────────────────


def classify_diffs(diffs):
    """Add a 'category' field to each diff dict."""
    for diff in diffs:
        if diff["text_changed"]:
            diff["category"] = _classify_text_change(diff)
        else:
            diff["category"] = _classify_structural_change(diff)
    return diffs
