"""Ungrammatical structured research notes — gn."""

from __future__ import annotations

from accgram.prose_ob_notes_shared import (
    SOMEWHERE,
    ZARQA_WHIM,
)

BY_REF: dict[str, dict[str, object]] = {
    "gn 17:20": {
        "st-source": "wlc",
        "wlc_focus": "ולישמע֘אל",
        "uxlc_change": "2021.10.19/2021.08.04-1",
        **ZARQA_WHIM,
    },
    "gn 32:24": {
        "st-source": "tbd",
        "wlc_focus": "לו׃",
        "st-summary": SOMEWHERE,
        "comment": (
            "There is also a question of ויקח֔ם vs וי֨קח֔ם (metigah) in this verse, but either option is grammatical."
        ),
    },
    "gn 47:29": {
        "st-source": "wlc",
        "wlc_focus": "ישרא֘ל",
        "uxlc_change": "2021.04.01/2020.12.06-1",
        **ZARQA_WHIM,
    },
}
