"""The two forms Holman writes inside his prose, where he gives them no lines.

His Joshua, Judges and Samuel messages state the word twice on lines of its own,
``Current UXLC`` or ``Current Text`` and then ``Corrected Text``. His Exodus,
Leviticus and Deuteronomy messages do neither. There the form as it stands sits
in parentheses at the end of the ``Word / Verse`` line, after a reference the
card already carries in its heading, and the form he proposes sits in
parentheses at the end of his ``Suggested Correction`` sentence. Ben asked on
2026-08-11 that those cases read like the others, so the two forms are read out
here and shown as rows of their own.

Reading a form out of prose is a derivation, so every such case declares which
of three shapes its message has and a mismatch raises rather than being guessed
at:

  ``BOTH``                 the form as it stands in the first field, the
                           proposed form in the suggestion sentence.
  ``CURRENT_ONLY``         the form as it stands in the first field, and no
                           proposed form: the message asks only for a note.
  ``PAIR_IN_FIRST_FIELD``  both forms in the first field, ``current / proposed``,
                           with none in the suggestion sentence.

Nothing here is retyped. Each form is lifted from the message text as it was
parsed, and the parenthesised run it comes from must be the only one in its
field, so a hand-typed accent cannot creep in and a second parenthesis cannot be
silently picked between.
"""

from __future__ import annotations

from dataclasses import dataclass
import re

from hkq_cmn.uxlc_email_extract import CorrectionCase

BOTH = "both"
CURRENT_ONLY = "current-only"
PAIR_IN_FIRST_FIELD = "pair-in-first-field"

# Keyed as uxlc_email_extract.CaseRef.key spells a reference. Every case whose
# message has no Corrected Text line must appear here, and no case that has one
# may -- see require_full_coverage.
FORM_SHAPE_BY_REF = {
    "Exodus 7:20.19": BOTH,
    "Exodus 11:6.1": BOTH,
    "Exodus 20:3.2": BOTH,
    "Exodus 38:12.6": BOTH,
    # "Make a note about accent positioning" -- proposes no form.
    "Levit 7:25.6": CURRENT_ONLY,
    "Levit 15:8.2": BOTH,
    # "Make a note about accent positioning" -- proposes no form.
    "Levit 16:21.6": CURRENT_ONLY,
    "Levit 25:20.4": BOTH,
    # "(yaarfu / yaarfu)", the meteg form then the merkha one, in the order his
    # "Change Meteg to Mercha" sentence names them.
    "Deuter 33:28.13": PAIR_IN_FIRST_FIELD,
}

SUGGESTION_LABEL = "Suggested Correction"
# Holman's line stating the form he proposes. His Chronicles message of
# 2026-08-09 calls it "Target Text" and every other message "Corrected Text";
# either way the case states the form itself, so there is nothing to read out of
# its prose and the case does not belong in FORM_SHAPE_BY_REF.
SUGGESTED_TEXT_LABELS = frozenset(("Corrected Text", "Target Text"))

# Any parenthesised run; whether it holds Hebrew is decided afterwards, against
# the codepoint bounds rather than a character class written out in the source.
# The Hebrew block and the presentation forms, as py/tests/test_h_dot_below_nfc.py
# and py/hkq_cmn/extract_docx_notes.py already spell them.
_PARENTHESISED_RE = re.compile(r"\(([^()]*)\)")
_HEBREW_RANGES = ((0x0590, 0x05FF), (0xFB1D, 0xFB4F))
_PAIR_SEPARATOR = "/"


def _has_hebrew(text: str) -> bool:
    return any(
        low <= ord(char) <= high for char in text for low, high in _HEBREW_RANGES
    )


def _parenthesised_hebrew(value: str) -> list[str]:
    return [run.strip() for run in _PARENTHESISED_RE.findall(value) if _has_hebrew(run)]


@dataclass(frozen=True)
class HolmanForms:
    """What a case's rows should show, read out of the message's prose.

    ``suggested`` is None where the message proposes no form. ``suggestion``
    is his sentence with the parenthesised form removed, that form now having
    a row of its own; where there was none to remove it is his sentence
    unchanged.
    """

    current: str
    suggested: str | None
    suggestion: str


def forms_for_case(case: CorrectionCase) -> HolmanForms | None:
    """The forms read out of this case's prose, or None where it states them.

    None is the Joshua/Judges/Samuel shape, whose Corrected Text line means
    there is nothing to read out.
    """
    shape = FORM_SHAPE_BY_REF.get(case.ref.key)
    if shape is None:
        return None
    first_label, first_value = case.fields[0]
    if shape == PAIR_IN_FIRST_FIELD:
        pair = _sole_parenthesised(first_value, case, first_label)
        current, suggested = _split_pair(pair, case, first_label)
    else:
        current = _sole_parenthesised(first_value, case, first_label)
        suggested = None
    suggestion = _suggestion_value(case)
    if shape == BOTH:
        suggested = _sole_parenthesised(suggestion, case, SUGGESTION_LABEL)
        suggestion = _without_form(suggestion, suggested, case)
    elif _parenthesised_hebrew(suggestion):
        raise ValueError(
            f"{case.ref.key} is declared {shape} in FORM_SHAPE_BY_REF, but its "
            f"{SUGGESTION_LABEL} line has a parenthesised form: "
            f"{suggestion!r}. Declare it {BOTH} instead, or say what the "
            "parentheses hold."
        )
    return HolmanForms(current=current, suggested=suggested, suggestion=suggestion)


def require_full_coverage(cases: list[CorrectionCase]) -> None:
    """Raise unless the table names exactly the cases with no suggested-text line."""
    labels = " or ".join(sorted(SUGGESTED_TEXT_LABELS))
    without_corrected = {
        case.ref.key
        for case in cases
        if not SUGGESTED_TEXT_LABELS.intersection(
            label for label, _value in case.fields
        )
    }
    missing = sorted(without_corrected - set(FORM_SHAPE_BY_REF))
    if missing:
        raise ValueError(
            f"{missing} state no {labels} line and are not in "
            "hkq_cmn/uxlc_holman_forms.FORM_SHAPE_BY_REF, so the card "
            "would show no form at all. Add each with the shape its message has."
        )
    unwanted = sorted(set(FORM_SHAPE_BY_REF) - without_corrected)
    if unwanted:
        raise ValueError(
            f"FORM_SHAPE_BY_REF names {unwanted}, which state a "
            f"{labels} line of their own; drop them from the table "
            "rather than reading their forms out of prose twice."
        )
    unmatched = sorted(set(FORM_SHAPE_BY_REF) - {case.ref.key for case in cases})
    if unmatched:
        raise ValueError(
            f"FORM_SHAPE_BY_REF names cases that no email contains: {unmatched}"
        )


def _suggestion_value(case: CorrectionCase) -> str:
    for label, value in case.fields:
        if label == SUGGESTION_LABEL:
            return value
    raise ValueError(
        f"{case.ref.key} has no {SUGGESTION_LABEL} line, so there is nothing to "
        "read a proposed form out of"
    )


def _sole_parenthesised(value: str, case: CorrectionCase, label: str) -> str:
    matches = _parenthesised_hebrew(value)
    if len(matches) != 1:
        raise ValueError(
            f"{case.ref.key}: the {label} line has {len(matches)} parenthesised "
            f"Hebrew runs, not one: {value!r}. The shape declared in "
            "FORM_SHAPE_BY_REF says which form to read out, and it cannot "
            "choose between two."
        )
    return matches[0].strip()


def _split_pair(pair: str, case: CorrectionCase, label: str) -> tuple[str, str]:
    parts = [part.strip() for part in pair.split(_PAIR_SEPARATOR)]
    if len(parts) != 2 or not all(parts):
        raise ValueError(
            f"{case.ref.key}: the {label} line is declared "
            f"{PAIR_IN_FIRST_FIELD}, so its parentheses should hold two forms "
            f"either side of a {_PAIR_SEPARATOR!r}, but they hold {pair!r}"
        )
    return parts[0], parts[1]


def _without_form(suggestion: str, form: str, case: CorrectionCase) -> str:
    """His sentence with the parenthesised form taken out, and its space with it.

    Taken out rather than left where it is because the form now has a row of
    its own directly above, and printing it twice on one card is the clutter
    the row was meant to remove. The tracked ``emails/<key>.txt`` still holds
    the sentence as it arrived.
    """
    parenthesised = f"({form})"
    if suggestion.count(parenthesised) != 1:
        raise ValueError(
            f"{case.ref.key}: {parenthesised!r} does not occur exactly once in "
            f"{suggestion!r}, so it cannot be taken out without guessing"
        )
    return re.sub(r"\s*" + re.escape(parenthesised), "", suggestion).strip()
