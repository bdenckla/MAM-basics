"""Ungrammatical structured research notes — dt."""

from __future__ import annotations

from py_html import wlc_utils_html

from accgram.prose_ob_notes_shared import (
    MISSING_SOF_PASUQ_COMMENT,
    MISSING_SOF_PASUQ_SUMMARY,
    SOMEWHERE,
    TAXTON,
    TIPEXA,
    ZARQA_WHIM,
)

BY_REF: dict[str, dict[str, object]] = {
    "dt 5:8": {
        # Dual-cantillation detangling (issue #36). dt 5:8 is one of the two-reading
        # Decalogue verses excluded from the normal scan. WLC's "tangled" form for
        # תעשה carries only a merkha on the ש; a better LC transcription reads that
        # vertical bar as a meteg (belonging to the elyon) and supplies a qadma
        # (belonging to the taxton) -- the consensus pointing, under which both the
        # taxton and elyon chanted verses are grammatical, where the merkha makes both
        # ungrammatical. (MAM's taxton has the qadma and its elyon has the meteg, which
        # the scanner swallows, which is why MAM's elyon parses cleanly.) The checker supplies
        # the taxton's qadma (clean, on the supplied-marks page) and emits WLC's actual
        # merkha in the elyon, so only the elyon is a dt 5:8 oddity now. UXLC corrects
        # the merkha to a meteg but supplies a pashta rather than the due qadma; see the
        # linked UXLC note page (its `-t` te'amim note). UXLC has since proposed a pending
        # change (for UXLC 2.6) to change that pashta to the qadma -- exactly the
        # correction this note argues for. Whether the error originates in LC, BHS, or BHQ
        # has not been confirmed -> tbd.
        "st-source": "tbd",
        "wlc_focus": "תעש֥ה־",
        "st-summary": (
            "WLC’s “tangled” form for תעשה carries only"
            " a merkha on the ש, but a better LC transcription would be a meteg (elyon)"
            f" and a qadma ({TAXTON})."
        ),
        "comment": [
            "WLC represents dual cantillation in manuscript (“tangled”) style,"
            f" where both {TAXTON} and elyon marks are superimposed"
            " on the same set of letters.",
            #
            "WLC’s tangled form for תעשה has only a merkha. This could be interpreted"
            f" as both {TAXTON} and elyon having merkha, or one having merkha and the"
            " other having nothing."
            f" We interpret it as elyon having merkha and {TAXTON} having nothing.",
            #
            "Although the LC is in poor shape here"
            " (see the image in the UXLC note),"
            " a better transcription of the LC would have"
            " meteg rather than merkha under the ש,"
            " and would add a qadma over the ש."
            " Admittedly, this is a transcription influenced by the fact that this is the consensus"
            " pointing here."
            " Not surprisingly, this consensus pointing makes"
            f" both the {TAXTON} chanted verse and the elyon chanted verse grammatical, if"
            f" the qadma is taken to belong to the {TAXTON} and the meteg is taken to"
            " belong to the elyon.",
            #
            [
                f"In contrast, as WLC stands neither strand is grammatical: the {TAXTON}"
                " lacks its due qadma, and the elyon carries a merkha where only a meteg"
                f" belongs. The detangler supplies the qadma for the {TAXTON}, making that"
                " strand grammatical (see the ",
                wlc_utils_html.anchor(
                    "supplied-marks page", {"href": "supplied-marks.html"}
                ),
                ") — but leaves WLC’s merkha in the elyon, so the elyon is listed here"
                " among other verses deemed ungrammatical.",
            ],
            #
            "Note that we do not shy away from transcriptions that, while grounded in manuscript"
            " evidence, use context (consensus and grammar) to supplement manuscript"
            " evidence when the manuscript evidence is ambiguous, for example when the"
            " manuscript image is blurry or the manuscript itself is in bad shape.",
            #
            "UXLC goes most of the way towards correcting WLC here. While UXLC does"
            " correct the merkha to be a meteg, unfortunately UXLC adds a pashta rather"
            " than a qadma.",
            #
            "UXLC has now proposed a pending change (slated for UXLC 2.6) that changes"
            " this pashta over the ש to a qadma — exactly the correction we advocate"
            " here. See the “Pending UXLC change” link above.",
            #
            "This error in WLC probably has its source in BHS and/or BHQ, i.e. this error is"
            " unlikely original to WLC, but we have not confirmed that.",
        ],
        # The detangled focus word תעשה in each reading, across the three transcriptions
        # (issue #36). One per-strand table replaces the old combined focus/diff table:
        # the merkha breaks both readings, but the two readings disagree on what is due
        # (taxton: a qadma; elyon: no accent, just a meteg), so splitting clarifies that
        # the elyon correction (merkha→meteg) is agreed by MAM and UXLC while only the
        # taxton correction (qadma vs pashta) is where they part. Keyed by strand_label;
        # each row is (value, desc, source). The WLC value is cross-checked against the
        # detangled stream at render time, so it cannot silently drift.
        "dual_cant_tables": {
            "taxton": [
                {"value": "תעשה", "desc": "no accent", "source": "WLC"},
                {"value": "תעש֨ה", "desc": "qadma", "source": "MAM"},
                {"value": "תעש֙ה", "desc": "pashta", "source": "UXLC"},
            ],
            "elyon": [
                {"value": "תעש֥ה־", "desc": "merkha", "source": "WLC"},
                {"value": "תעשֽה־", "desc": "meteg", "source": "MAM"},
                {"value": "תעשֽה־", "desc": "meteg", "source": "UXLC"},
            ],
        },
        "pending_uxlc_change": "2026.10.19/2026.04.10-10",
        "uxlc_note_page": "https://tanach.us/Notes/Deuteronomy/Deuteronomy.5.8.2-t.html",
    },
    "dt 9:20": {
        "st-source": "tbd",
        "st-summary": MISSING_SOF_PASUQ_SUMMARY,
        "wlc_focus": "ההֽוא",
        "comment": MISSING_SOF_PASUQ_COMMENT,
        "BHQ": "?",
    },
    "dt 13:15": {
        "st-source": "lc",
        "st-summary": "The LC has darga where it should have tevir.",
        "wlc_focus": "וחקרת֧",
        "img": "LC-107B-col-3-line-18-dt-13v15.png",
    },
    "dt 25:9": {
        "st-source": "tbd",
        "st-summary": MISSING_SOF_PASUQ_SUMMARY,
        "wlc_focus": "אחֽיו",
        "comment": MISSING_SOF_PASUQ_COMMENT,
        "BHQ": "?",
    },
    "dt 10:15": {
        "st-source": "tbd",
        "wlc_focus": "הזה׃",
        "st-summary": SOMEWHERE,
    },
    "dt 12:2": {
        "st-source": "tbd",
        "wlc_focus": "רענן׃",
        "st-summary": SOMEWHERE,
    },
    "dt 23:18": {
        "st-source": "tbd",
        "wlc_focus": "ישראל׃",
        "st-summary": SOMEWHERE,
    },
    "dt 24:10": {
        "st-source": "lc",
        "wlc_focus": "ברעך",
        "st-summary": f"The LC has only meteg where meteg-{TIPEXA} is expected.",
        "img": "LC-113A-col-3-line-27-Dt-24v10.png",
        "comment": (
            [
                f"We could also interpret the LC’s mark under the resh as a {TIPEXA} that comes unexpectedly early in the chanted word."
            ],
            [
                "We could also speculate that what seems to be the long descender of the final kaf"
                f" includes a {TIPEXA} placed too early relative to the kaf."
            ],
            [
                "Yet, just as I have criticized some transcriptions as aggresively uncharitable,"
                " there is no doubt such a thing as a transcription that is too aggressively charitable,"
                " and these suggestions above,"
                " i.e. these ways of saving the chanted word from violating the accent grammar,"
                " may be examples of that."
            ],
            [
                f"The most likely explanation is that the LC simply does not have the expected {TIPEXA} anywhere in the chanted word."
            ],
        ),
    },
    "dt 14:24": {
        "st-source": "wlc",
        "wlc_focus": "תוכ֘ל",
        "uxlc_change": "2021.04.01/2020.12.06-8",
        **ZARQA_WHIM,
    },
    "dt 31:7": {
        "st-source": "wlc",
        "wlc_focus": "ישרא֘ל",
        "uxlc_change": "2021.04.01/2020.12.06-9",
        **ZARQA_WHIM,
    },
}
