"""Ungrammatical structured research notes — is."""

from __future__ import annotations

from accgram.prose_ob_notes_shared import (
    MUNAX,
    SOMEWHERE,
)
from py_html import wlc_utils_html

_FOI_CATEGORY_NAME = "⅃-leg...non-revia ((tev)) with 2 (qa,da) intervening"

_FOI_CATEGORY_URL = (
    "https://bdenckla.github.io/MAM-with-doc/foi/foi-pasoleg-1.html"
    "#intro-%E2%85%83-leg...non-revia%C2%ABspace%C2%BB((tev))%C2%ABspace%C2%BB"
    "with%C2%ABspace%C2%BB2%C2%ABspace%C2%BB(qa,da)%C2%ABspace%C2%BBintervening"
)


BY_REF: dict[str, dict[str, object]] = {
    "is 36:2": {
        "st-source": "tbd",
        "st-summary": f"The checker rejects {MUNAX} serving {MUNAX} legarmeh; the servus must be merkha.",
        "wlc_focus": "וישל֣ח",
        "comment": [
            (
                "This verse is the sole member of the FOI category “",
                wlc_utils_html.anchor(_FOI_CATEGORY_NAME, {"href": _FOI_CATEGORY_URL}),
                "”.",
            ),
            "Verified by re-running the checker on a fixed verse: substituting"
            f" merkha for the {MUNAX} servus (the MAM-simple reading) clears the"
            " checker error.",
        ],
    },
    "is 13:7": {
        "st-source": "tbd",
        "wlc_focus": "ימס׃",
        "st-summary": SOMEWHERE,
    },
    "is 45:1": {
        "st-source": "tbd",
        "wlc_focus": "לכ֣ורש",
        # The speculated reading to test: "segol" here is the *accent* segol
        # (segolta, U+0592), not the segol vowel -- the checker validates accents.
        # MAM equals WLC, so the fix-tester exercises this synth_fix: replace the
        # munax (U+05A3) with a segolta (U+0592).
        "synth_fix": "לכ֒ורש",
        "st-summary": (f"The checker requires a segol accent rather than a {MUNAX}."),
        "comment": [
            "Verified by re-running the checker on a fixed verse: replacing the"
            f" {MUNAX} with a segol accent clears the segolta_phrase error. Note that"
            f" MAM, like WLC, has a {MUNAX} here, so this is a checker-vs-consensus tension,"
            " not a quirk in the LC, BHS, or WLC.",
            " The question of whether there should be a legarmeh after לכ֣ורש"
            " (see MAM’s doc-note)"
            " is independent of the checker’s"
            " problem with this verse."
            " Giving the chanted word a legarmeh does not clear the error"
            " (the verse then fails to parse at all)."
            " Only the segol accent resolves it.",
        ],
    },
}
