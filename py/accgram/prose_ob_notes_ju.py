"""Ungrammatical structured research notes — ju."""

from __future__ import annotations

from accgram.prose_ob_notes_shared import (
    MUNAX,
)

_JU_1318_01 = (
    "Color images make it clearer that the mark in question is a speck on the LC vellum rather than a tevir dot made of ink."
    " See the image in the UXLC note to which we link above."
)


_JU_1318_02 = (
    "Even if the editors of BHQ Judges (2011) lacked access to color images,"
    " this was an overly-literal, aggressively uncharitable transcription."
    " Even without color, they should have been aware that this could be"
    " a non-ink speck on the LC vellum or a non-intentional ink dot."
    " They should have found one of these possibilities more likely than a verse-final tevir."
    " A verse-final tevir is rather far-fetched."
)


_JU_1318_03 = (
    "Are they attempting to use typography to create a pseudo-photographic image of the LC,"
    " or are they trying to transcribe the LC “meaningfully,”"
    " using some degree of interpretation to determine the most likely intended meaning of each mark?"
    " (Sometimes, as is the case here, the most likely intended meaning of a mark is no meaning at all!)"
)


BY_REF: dict[str, dict[str, object]] = {
    "ju 13:18": {
        "st-source": "bhs",
        "st-summary": "BHQ transcribes a silluq as a tevir due to a speck.",
        "wlc_focus": "פ֛לאי׃",
        "uxlc_note_page": "https://tanach.us/Notes/Judges/Judges.13.18.10-t.html",
        "comment": (
            _JU_1318_01,
            _JU_1318_02,
            _JU_1318_03,
        ),
    },
    "ju 1:2": {
        "st-source": "lc",
        "wlc_focus": "וי֣אמר",
        "st-summary": f"The LC has {MUNAX} where a merkha is expected.",
        "img": "LC-136A-col-1-line-7-Ju-1v2.png",
    },
    "ju 11:24": {
        "st-source": "bhs",
        "wlc_focus": "אות֥ו תיר֑ש",
        "st-summary": f"BHS transcribes a faded, ambiguous mark as merkha rather than {MUNAX}.",
        "img": "LC-144A-col-1-line-17-Ju-11v24.png",
        "edited img": "LC-144A-col-1-line-17-Ju-11v24-edited.png",
        "pending_uxlc_change": "2026.10.19/2026.04.10-7",
        "comment": (
            [
                "Ignoring the grammar of accents, the faded remains of the mark in question are slightly more plausibly"
                f" interpreted as a {MUNAX} than a merkha."
                f" But the “upright” part of the {MUNAX} is very faint, if it is even there are all and I am not kidding myself,"
                " seeing what I want to see rather than what is actually there."
            ],
            [
                f"Note that a geresh from הוריש on the line below complicates the colliding with the elbow of the proposed {MUNAX}."
            ],
            [
                f"In an image above, I have outlined the proposed {MUNAX} and the colliding geresh."
            ],
            [
                "One of the most extraordinary things about BHS (continued by BHQ) is that, to my knowledge, it never acknowledges"
                " any uncertainty in its transcription of the LC."
                " Yet of course any transcription of the LC is surely fraught with hundreds of serious uncertainties."
                " Although space constraints are extreme in any single-volume Tanakh like BHS,"
                " really the only responsible thing to do for a chanted word like this is to acknowledge the uncertainty somehow,"
                " and either transcribe no accent at all or use context (grammar) combined with the (faint) evidence"
                f" to make a good guess, which in this case would be {MUNAX}."
            ],
            [
                "To transcribe this chanted word as (illegally) accented with merkha"
                " without any acknowledgment of either illegality or uncertainty is,"
                " to me, bordering on irresponsible."
            ],
        ),
    },
    "ju 21:16": {
        "st-source": "bhs",
        "wlc_focus": "ויאמר֨ו",
        "st-summary": "BHS transcribes a syllable as having qadma rather than pashta.",
        "img": "LC-150A-col-1-line-22-Ju-21v16.png",
        "pending_uxlc_change": "2026.10.19/2026.04.10-5",
    },
}
