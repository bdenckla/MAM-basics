"""Ungrammatical structured research notes — ec."""

from __future__ import annotations

from accgram.prose_ob_notes_shared import (
    TIPEXA,
)

BY_REF: dict[str, dict[str, object]] = {
    "ec 7:21": {
        "st-source": "bhs",
        "st-summary": "BHS transcribes a tevir as a merkha.",
        "wlc_focus": "אש֥ר",
        "BHQ": "?",
        "uxlc_change": "2023.10.19/2023.09.11-18",
        "comment": "See the image in the UXLC change to which we link above.",
    },
    "ec 9:18": {
        "st-source": "wlc",
        "st-summary": f"WLC transcribes a {TIPEXA} as a merkha.",
        "wlc_focus": "יאב֥ד טוב֥ה",
        "BHQ": "?",
        "img": "LC-429A-col-1-line-23-Eccl-9v18.png",
        "uxlc_change": "2022.12.07/2022.10.04-2",
        "comment": (
            (
                "It is very rare for WLC to diverge from BHS like this, without a bracket note."
                " Perhaps WLC agrees with an older BHS? I have only checked the 1984 and 1997 editions of BHS."
            ),
            (
                f"The LC diverges from consensus here by having merkha {TIPEXA} rather than {TIPEXA} merkha,"
                " but that is still accent-grammatical, so that divergence is not relevant here."
            ),
        ),
    },
    "ec 12:14": {
        "st-source": "wlc",
        "wlc_focus": "כ֤י",
        "st-summary": "Defying both BHS and the LC, WLC transcribes a yetiv as a mahapakh.",
        "uxlc_change": "2023.10.19/2023.09.11-25",
        "comment": (
            (
                "It is very rare for WLC to diverge from BHS like this, without a bracket note."
                " Perhaps WLC agrees with an older BHS? I have only checked the 1984 and 1997 editions of BHS."
            ),
        ),
    },
}
