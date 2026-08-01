"""Ungrammatical structured research notes — misc."""

from __future__ import annotations

from accgram.prose_ob_notes_shared import (
    BHS_TRANSCRIBES,
    ETNAXTA,
    MINXAT,
    MISSING_SOF_PASUQ_COMMENT,
    MISSING_SOF_PASUQ_SUMMARY,
    MUNAX,
    TIPEXA,
    TIP_LIKE_INCL,
)

_LM_0505_01 = (
    "The consensus pointing of the last two atoms in this verse is הֽוּנַֽח־לָֽנוּ׃."
    " I.e. ignoring vowel marks, the consensus for the atom in question is הֽונֽח־, i.e. two meteg marks and a maqaf."
)


_LM_0505_02 = (
    "Given this consensus, the most charitable transcription of the LC here is that it is missing the maqaf,"
    " leaving הונח with no accent, only two meteg marks."
    " Even ignoring the consensus, i.e. transcribing “blind,” this is the most charitable transcription."
)


_LM_0505_03 = (
    "Nonetheless, BHQ opts to make הונח “locally legal” by giving it an accent."
    " It gives it an accent by transcribing the second mark"
    f" as a second {TIPEXA} rather than as a meteg. WLC follows BHQ in this, as it explicitly notes with a bracket-Q note."
    " (Hover over the letters of the bracket notes above to decode them.)"
)


_LM_0505_04 = (
    "This makes the chanted word הונח locally legal while rendering the second half of the verse illegal"
    f" by giving the silluq segment two chanted words accented with {TIPEXA}."
    f" (This (short) verse has no {ETNAXTA} segment.)"
)


_LM_0505_05 = (
    f"It is uncharitable to transcribe this mark as a {TIPEXA}."
    " Most likely what happened here is that the scribe forgot to add a maqaf."
    f" It is far less likely that the scribe intended to add a second {TIPEXA},"
    " and a second merkha seems equally implausible."
)


_LM_0505_06 = TIP_LIKE_INCL


_LM_0505_07 = (
    "Side note: there also seems to be some question of whether the נ in הונח should have a dagesh."
    " BHQ claims that manuscripts L34 and Y (in its sigil vocabulary) have this dagesh."
    f" Breuer (in Da-at Miqra) claims that {MINXAT} Shai asserts this dagesh."
)


BY_REF: dict[str, dict[str, object]] = {
    "1s 6:19": {
        "st-source": "tbd",
        "st-summary": MISSING_SOF_PASUQ_SUMMARY,
        "wlc_focus": "גדולֽה",
        "comment": MISSING_SOF_PASUQ_COMMENT,
    },
    "2k 23:36": {
        "st-source": "bhs",
        "st-summary": "BHS transcribes a syllable as having qadma rather than pashta.",
        "wlc_focus": "שנ֨ה",
        "uxlc_change": "2022.12.07/2022.09.01-24",
        "comment": "See the image in the UXLC change to which we link above.",
    },
    "ob 1:1": {
        "st-source": "lc",
        "st-summary": "The LC has no visible accent on עליה.",
        "wlc_focus": "עליה",
        "BHQ": "?",
        "uxlc_note_page": "https://tanach.us/Notes/Obadiah/Obadiah.1.1.17-c.html",
        "comment": "See the image in the UXLC note to which we link above.",
    },
    "mi 2:7": {
        "st-source": "bhs",
        "st-summary": "BHS transcribes a syllable as having qadma rather than pashta.",
        "wlc_focus": "דבר֨י",
        "BHQ": "?",
        "uxlc_change": "2023.04.01/2022.12.12-10",
        "comment": (
            "See the image in the UXLC change to which we link above."
            " The qadma (rather than pashta) on דברי is the cause, but the ERROR does not"
            " land there: with no pashta to head it, the zaqef clause over"
            " הלוא דברי ייטיבו never forms, so the failure surfaces later, on the"
            f" enclosing {TIPEXA} phrase over הלוא דברי ייטיבו עם."
            " The defect itself, though, is fundamentally a pashta-vs-qadma confusion on"
            f" the single mark on דברי; the malformed {TIPEXA} phrase"
            " (tipexa_phrase → ERROR) is only a surface artifact of how the LALR parse"
            f" fails, not a problem with the {TIPEXA} or the chanted words that phrase spans"
            " — flipping that one mark (qadma → pashta) clears the error entirely."
        ),
    },
    "lm 5:5": {
        "st-source": "tbd",
        "st-summary": f"BHQ transcribes a meteg as a {TIPEXA} due to the LC’s missing maqaf.",
        "wlc_focus": "הונ֖ח",
        "img": "LC-432A-col-3-line-17-Lam-5v5.png",
        "comment": (
            _LM_0505_01,
            _LM_0505_02,
            _LM_0505_03,
            _LM_0505_04,
            _LM_0505_05,
            _LM_0505_06,
            _LM_0505_07,
        ),
    },
    "da 2:41": {
        "st-source": "tbd",
        "st-summary": "BHS transcribes a meteg as a merkha due to the LC’s missing maqaf.",
        "wlc_focus": "ד֥י",
        "uxlc_change": "2024.04.01/2023.09.12-3",
        "comment": "See the image in the UXLC change to which we link above.",
    },
    "ne 2:10": {
        "st-source": "bhs",
        "wlc_focus": "ב֥א",
        "st-summary": BHS_TRANSCRIBES,
        "uxlc_change": "2024.04.01/2023.09.14-3",
    },
    "1c 1:53": {
        "st-source": "lc",
        "wlc_focus": "אל֣וף",
        "st-summary": f"The LC has a {MUNAX} where a merkha is expected.",
        "img": "LC-328A-col-1-line-27-1C-1v53.png",
    },
}
