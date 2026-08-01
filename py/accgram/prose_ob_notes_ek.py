"""Ungrammatical structured research notes — ek."""

from __future__ import annotations

from accgram.prose_ob_notes_shared import (
    MISSING_SOF_PASUQ_COMMENT,
    MISSING_SOF_PASUQ_SUMMARY,
    TIPEXA,
    ambiguous_mark_context_comment,
)

BY_REF: dict[str, dict[str, object]] = {
    "ek 11:1": {
        "st-source": "bhs",
        "st-summary": f"BHS transcribes a merkha as a {TIPEXA}.",
        "wlc_focus": "שר֖י",
        "img": "LC-280B-col-3-line-2-Ezek-11v1.png",
        "comment": (
            ambiguous_mark_context_comment("שרי")
            + f" It is aggressively uncharitable to transcribe the mark on שרי as {TIPEXA}:"
            + f" {TIPEXA} is the least likely of the three possible meanings of this mark."
            + " Merkha is by far the most likely. If the mark were meteg, we would have to"
            + " assume that a maqaf is missing."
        ),
    },
    "ek 14:11": {
        "st-source": "tbd",
        "st-summary": "BHS transcribes a meteg as a merkha due to the LC’s missing maqaf.",
        "wlc_focus": "וה֥יו ל֣י",
        "img": "LC-282B-col-2-line-3-Ezek-14v11.png",
        "comment": (
            ambiguous_mark_context_comment("והיו")
            + " The most likely intended meaning of the mark on והיו is meteg, even though that implies that"
            + " a maqaf is missing."
        ),
    },
    "ek 33:20": {
        "st-source": "tbd",
        "st-summary": MISSING_SOF_PASUQ_SUMMARY,
        "wlc_focus": "ישראֽל",
        "comment": MISSING_SOF_PASUQ_COMMENT,
    },
}
