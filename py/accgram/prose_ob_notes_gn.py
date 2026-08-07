"""Ungrammatical structured research notes — gn."""

from __future__ import annotations

from accgram.prose_ob_notes_shared import (
    SOMEWHERE,
    ZARQA_WHIM,
    metigah_zaqef_across_a_space_comment,
)
from py_html import wlc_utils_html

BY_REF: dict[str, dict[str, object]] = {
    "gn 17:20": {
        "st-source": "wlc",
        "wlc_focus": "ולישמע֘אל",
        "uxlc_change": "2021.10.19/2021.08.04-1",
        **ZARQA_WHIM,
    },
    "gn 18:18": {
        "st-source": "tbd",
        "st-summary": "A maqaf is missing somewhere in the LC-BHS-WLC pipeline.",
        "wlc_focus": "ונ֨ברכו",
        "comment": (
            metigah_zaqef_across_a_space_comment("ונ֨ברכו־ב֔ו", "ונ֨ברכו ב֔ו"),
            (
                "The verse has another metigah-zaqef, וא֨ברה֔ם, and that one parses clean in"
                " WLC as well: its qadma and its zaqef fall in a single atom, so it needs no"
                " maqaf to be one chanted word."
            ),
            [
                "WLC has a bracket-U note on ונברכו, recording that it agrees with both BHS"
                " 1997 and BHQ on an unexpected reading. So the space is at least as old as"
                " BHS, and is not something WLC alone has. That still does not put the space"
                " in the manuscript: BHS, BHQ and WLC are best taken as one transcription"
                " rather than as three that agree. Nobody has yet read the LC here — folio"
                " 009B — so the source stays open. ",
                wlc_utils_html.anchor("je 37:10", {"href": "#obje37v10"}),
                " has the same shape, and there UXLC has read the manuscript.",
            ],
        ),
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
