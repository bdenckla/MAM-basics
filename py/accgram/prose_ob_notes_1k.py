"""Ungrammatical structured research notes — 1k."""

from __future__ import annotations

from accgram.prose_ob_notes_shared import (
    BHS_TRANSCRIBES,
    MUNAX,
    TIPEXA,
)

BY_REF: dict[str, dict[str, object]] = {
    "1k 6:2": {
        "st-source": "bhs",
        "st-summary": f"BHS transcribes a {MUNAX} as a mahapakh.",
        "wlc_focus": "ועשר֤ים",
        "uxlc_change": "2022.12.07/2022.08.31-9",
        "comment": "See the image in the UXLC change to which we link above.",
    },
    "1k 16:33": {
        "st-source": "bhs",
        "st-summary": "BHS’s qadma matches neither the LC nor the consensus.",
        "wlc_focus": "מכ֨ל",
        "uxlc_change": "2022.12.07/2022.08.31-23",
        "comment": (
            "The LC has no visible accent on מכל. See the image in the UXLC change to which we link above."
            " The consensus accents the final syllable with pashta rather than qadma."
        ),
    },
    "1k 19:11": {
        "st-source": "lc",
        "st-summary": "The LC is missing a pashta.",
        "wlc_focus": "הר֨וח",
        "img": "LC-199A-col-3-line-21-1K-19v11.png",
        "comment": "Arguably, WLC and UXLC should code the mark on the resh as a pashta rather than a qadma.",
    },
    "1k 20:29": {
        "st-source": "bhs",
        # One change to how this atom is marked, not two: reading the stroke as a merkha
        # is what costs the maqaf, so it is stated as the exchange it is (issue #76).
        "st-summary": "BHS transcribes a meteg as a merkha, dropping the maqaf that went with it.",
        "wlc_focus": "נ֥כח",
        "uxlc_change": "2022.12.07/2022.08.31-32",
        "comment": (
            ("See the image in the UXLC change to which we link above."),
            (
                "Aside: I am not sure what, if anything, is grammatically “wrong” about a merkha here."
                " Indeed see the MAM doc-note for a list of some of the sources that have merkha."
                " Maybe this merkha is not even what the Goerwitz checker is flagging as wrong."
                " The overall sequence involves merkha kefula;"
                " I wonder whether, because it is so rare, we lack a good sense of"
                " the “legality” of sequences involving it."
                " The sequence in question is"
                f" darga, merkha kefula, something on נכח (the atom in question), and then {TIPEXA}."
            ),
        ),
    },
    "1k 6:3": {
        "st-source": "bhs",
        "wlc_focus": "עשר֣ים",
        "st-summary": BHS_TRANSCRIBES,
        "uxlc_change": "2022.12.07/2022.08.31-10",
    },
    "1k 8:11": {
        "st-source": "bhs",
        "wlc_focus": "מפנ֥י",
        "st-summary": BHS_TRANSCRIBES,
        "uxlc_change": "2022.04.01/2021.11.21-1",
    },
    "1k 20:25": {
        "st-source": "tbd",
        "wlc_focus": "וס֣וס",
        "st-summary": f"The checker may prefer merkha to LC’s {MUNAX}. Or it may not like either.",
        "img": "LC-200A-col-2-line-19-1K-20v25.png",
        "Aleppo img": "AC-1K-20v25.png",
    },
}
