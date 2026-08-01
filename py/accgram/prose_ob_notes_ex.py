"""Ungrammatical structured research notes — ex."""

from __future__ import annotations

from accgram.prose_ob_notes_shared import (
    BHS_TRANSCRIBES,
    MISSING_SOF_PASUQ_COMMENT,
    MISSING_SOF_PASUQ_SUMMARY,
    MUNAX,
    ZARQA_WHIM,
)

_BAR_INSTEAD_OF_SOF_PASUQ_SUMMARY = "In the place where one would expect a sof pasuq, the LC has a vertical bar somewhat like a paseq or legarmeh."


BY_REF: dict[str, dict[str, object]] = {
    "ex 2:5": {
        "st-source": "tbd",
        "st-summary": MISSING_SOF_PASUQ_SUMMARY,
        "wlc_focus": "ותקחֽה",
        "comment": MISSING_SOF_PASUQ_COMMENT,
    },
    "ex 14:25": {
        "st-source": "tbd",
        "st-summary": MISSING_SOF_PASUQ_SUMMARY,
        "wlc_focus": "במצרֽים",
        "comment": MISSING_SOF_PASUQ_COMMENT,
    },
    "ex 14:29": {
        "st-source": "tbd",
        "st-summary": MISSING_SOF_PASUQ_SUMMARY,
        "wlc_focus": "ומשמאלֽם",
        "comment": MISSING_SOF_PASUQ_COMMENT,
    },
    "ex 34:6": {
        "st-source": "lc",
        "st-summary": _BAR_INSTEAD_OF_SOF_PASUQ_SUMMARY,
        "wlc_focus": "ואמֽת׀",
        "img": "LC-052A-col-2-line-1-Ex-34v6.png",
    },
    "ex 4:10": {
        "st-source": "lc",
        "wlc_focus": "דברך",
        "st-summary": "The LC lacks an accent on this chanted word.",
        # The UXLC change here only adds note 'c' (no text change), so we link
        # the note itself rather than the change.
        "uxlc_note_page": "https://tanach.us/Notes/Exodus/Exodus.4.10.17-c.html",
    },
    "ex 6:6": {
        "st-source": "wlc",
        "wlc_focus": "ישרא֘ל",
        "uxlc_change": "2021.04.01/2020.12.06-2",
        **ZARQA_WHIM,
    },
    "ex 28:1": {
        "st-source": "bhs",
        "wlc_focus": "את֔ו",
        "st-summary": BHS_TRANSCRIBES,
        "uxlc_change": "2022.04.01/2021.11.28-2",
        "comment": ("This is the example given in Goerwitz’s article."),
    },
    "ex 30:12": {
        "st-source": "wlc",
        "wlc_focus": "ישרא֘ל",
        "uxlc_change": "2021.04.01/2020.12.06-3",
        **ZARQA_WHIM,
    },
    "ex 36:2": {
        "st-source": "wlc",
        "wlc_focus": "בצלא֘ל",
        "uxlc_change": "2021.04.01/2020.12.06-4",
        **ZARQA_WHIM,
    },
    "ex 38:12": {
        "st-source": "lc",
        "wlc_focus": "עמודיה֥ם",
        "st-summary": f"The LC has something like a merkha where a {MUNAX} is expected.",
        "img": "LC-055A-col-1-line-3-Ex-38v12.png",
    },
}
