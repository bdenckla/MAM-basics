from __future__ import annotations

from accgram import rtms_focus_diff_expand
from accgram import rtms_generated_descriptions
from accgram.prose_ob_notes import get_structured_text
from accgram.prose_ob_notes_shared import ZARQA_WHIM_SUMMARY

_MISSING_SOF_PASUQ_TOKENS = {
    "silluq-no_sof_pasuq",
    "silluq-pasoleg",
}
# A bare "sof_pasuq" descriptor means the verse-final chanted word carries a sof pasuq but
# no accent at all (the silluq is missing). This deliberately excludes the case
# where some other accent stands where a silluq is expected: e.g. a tevir before
# the sof pasuq yields "tevir-sof_pasuq", which is not in this set.
_MISSING_SILLUQ_TOKENS = {
    "sof_pasuq",
}


def row_category(
    row: dict[str, object],
    *,
    structured_text: object = None,
) -> str:
    """Classify an ungrammatical verse along the sof-pasuq/silluq dimension.

    Returns one of "msp" (missing sof pasuq), "msl" (missing silluq, i.e. a sof
    pasuq present but no accent on the word), "zwhim" (a scribal zarqa whim that
    WLC turns into an outright error), or "other". Precedence is
    msp > msl > zwhim > other.
    """
    descriptions = _generated_descriptions(row, structured_text=structured_text)
    if any(description in _MISSING_SOF_PASUQ_TOKENS for description in descriptions):
        return "msp"
    if any(description in _MISSING_SILLUQ_TOKENS for description in descriptions):
        return "msl"
    if _is_zarqa_whim(row, structured_text=structured_text):
        return "zwhim"
    return "other"


def _is_zarqa_whim(
    row: dict[str, object],
    *,
    structured_text: object,
) -> bool:
    if structured_text is None:
        ref = row.get("ref")
        structured_text = (
            get_structured_text().get(ref) if isinstance(ref, str) else None
        )
    if not isinstance(structured_text, dict):
        return False
    return structured_text.get("st-summary") == ZARQA_WHIM_SUMMARY


def _generated_descriptions(
    row: dict[str, object],
    *,
    structured_text: object,
) -> list[str | None]:
    # The structured text is only needed to derive the WLC focus. It lives in the
    # by-book prose_ob_notes set (the default lookup below); callers that already have a
    # row's structured text pass it in explicitly.
    if structured_text is None:
        ref = row.get("ref")
        structured_text = (
            get_structured_text().get(ref) if isinstance(ref, str) else None
        )
    wlc_focus = rtms_focus_diff_expand.structured_wlc_focus(structured_text)
    return [
        rtms_generated_descriptions.try_generated_description(
            description_key=description_key,
            enriched_row=row,
            wlc_focus=wlc_focus,
        )
        for description_key in ("wlc", "uxlc", "mam")
    ]
