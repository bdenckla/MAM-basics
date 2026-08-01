"""Read the human claim in an ungrammatical verse's structured-text note (ob_notes_*).

The fix-tester cross-checks its mechanical verdict against what the hand-authored
``st-summary``/``comment`` *claims*.  Speculative claims ("I think the checker
wants...", "the scanner prefers merkha rather than munax") are the ones most worth
testing, so this module flags them and makes a best-effort guess at the claim's
direction (does it expect adopting MAM to fix the verse?).  Direction inference
from free prose is unreliable, so it is advisory only -- the report shows it next
to the mechanical result and lets a human adjudicate disagreements.
"""

from __future__ import annotations

# Substrings (case-insensitive) that mark a claim as genuinely speculative /
# hedged.  Deliberately excludes "rather than" and "as a ": those appear in the
# confident descriptive templates (SOMEWHERE, BHS_TRANSCRIBES) and are not hedges.
# "wants" must keep its checker/scanner subject ("the checker wants merkha"):
# bare "wants" also matches confident grammatical claims about the *word*
# ("the word ... wants no stress helper"), which are not hedges.
SPECULATIVE_MARKERS: tuple[str, ...] = (
    "i think",
    "i suspect",
    "checker wants",
    "scanner wants",
    "prefer",  # prefer / prefers / may prefer
    "does not like",
    "doesn't like",
    "may not like",
    "most likely",
    "probably",
    "seems",
    "appears to",
    "there is a question",
    "question of whether",
    "perhaps",
    "maybe",
)

# Markers suggesting the note expects adopting MAM to fix the verse (WLC is wrong).
_EXPECTS_FIX_MARKERS: tuple[str, ...] = (
    "missing",
    "transcribes",
    "rather than",
    "appears",
    "should",
    "wants",
    "as a ",
    "outright error",
    "turns",
)
# Markers suggesting the note thinks WLC is fine / the change would not help.
_REJECTS_FIX_MARKERS: tuple[str, ...] = (
    "is correct",
    "is fine",
    "not an error",
    "no error",
    "is valid",
    "well-formed",
)


def claim_text(structured_text: object) -> str:
    """Flatten ``st-summary`` + ``comment`` to the plain visible text, lowercased."""
    if not isinstance(structured_text, dict):
        return ""
    parts: list[str] = []
    _collect_strings(structured_text.get("st-summary"), parts)
    _collect_strings(structured_text.get("comment"), parts)
    return " ".join(parts).lower()


def is_speculative(structured_text: object) -> bool:
    text = claim_text(structured_text)
    return any(marker in text for marker in SPECULATIVE_MARKERS)


def claimed_outcome(structured_text: object) -> str:
    """Best-effort: 'expects_fix' | 'rejects_fix' | 'unclear' (advisory only)."""
    text = claim_text(structured_text)
    if not text:
        return "unclear"
    rejects = any(marker in text for marker in _REJECTS_FIX_MARKERS)
    expects = any(marker in text for marker in _EXPECTS_FIX_MARKERS)
    if rejects and not expects:
        return "rejects_fix"
    if expects and not rejects:
        return "expects_fix"
    return "unclear"


def _collect_strings(value: object, out: list[str]) -> None:
    """Recursively gather plain str leaves from nested lists/tuples/dicts.

    HTML element objects (e.g. wlc_utils_html.anchor(...)) are opaque and skipped;
    their visible text is not needed for keyword matching, and the surrounding
    plain-string fragments carry the claim's wording.
    """
    if isinstance(value, str):
        if value:
            out.append(value)
    elif isinstance(value, (list, tuple)):
        for item in value:
            _collect_strings(item, out)
    elif isinstance(value, dict):
        for item in value.values():
            _collect_strings(item, out)
