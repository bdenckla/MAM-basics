"""Ungrammatical structured research notes — lv."""

from __future__ import annotations

from accgram.prose_ob_notes_shared import (
    MISSING_SOF_PASUQ_COMMENT,
    MISSING_SOF_PASUQ_SUMMARY,
    SOMEWHERE,
    TIPEXA,
    ZARQA_WHIM,
)

BY_REF: dict[str, dict[str, object]] = {
    "lv 18:17": {
        "st-source": "tbd",
        "st-summary": MISSING_SOF_PASUQ_SUMMARY,
        "wlc_focus": "הֽוא",
        "BHQ": "?",
        "comment": MISSING_SOF_PASUQ_COMMENT,
    },
    "lv 19:1": {
        "st-source": "tbd",
        "st-summary": MISSING_SOF_PASUQ_SUMMARY,
        "wlc_focus": "לאמֽר",
        "BHQ": "?",
        "comment": MISSING_SOF_PASUQ_COMMENT,
    },
    "lv 26:7": {
        "st-source": "tbd",
        "st-summary": MISSING_SOF_PASUQ_SUMMARY,
        "wlc_focus": "לחֽרב",
        "BHQ": "?",
        "comment": MISSING_SOF_PASUQ_COMMENT,
    },
    "lv 4:2": {
        "st-source": "wlc",
        "wlc_focus": "ישרא֘ל",
        "uxlc_change": "2021.04.01/2020.12.06-5",
        **ZARQA_WHIM,
    },
    "lv 20:2": {
        "st-source": "wlc",
        "wlc_focus": "ישרא֘ל",
        "uxlc_change": "2021.04.01/2020.12.06-6",
        **ZARQA_WHIM,
    },
    "lv 25:20": {
        "st-source": "lc",
        "wlc_focus": "נאכ֤֖ל",
        "st-summary": f"The LC has something like a mahapakh in addition to the expected {TIPEXA}.",
        # The UXLC change here only changes note 'n' to note 'c' (no text
        # change), so we link the note itself rather than the change.
        "uxlc_note_page": "https://tanach.us/Notes/Leviticus/Leviticus.25.20.4-c.html",
        "comment": (
            "The mark in question is not necessarily a mahapakh."
            " In particular, it may be part of a broken masorah circle from the line below."
            " See the UXLC note page."
        ),
    },
    "lv 26:28": {
        "st-source": "tbd",
        "wlc_focus": "חטאתיכם׃",
        "st-summary": SOMEWHERE,
    },
}
