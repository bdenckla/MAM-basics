"""Ungrammatical structured research notes — je."""

from __future__ import annotations

from accgram.prose_ob_notes_shared import (
    BHS_TRANSCRIBES,
    MUNAX,
    TIPEXA,
    TIP_LIKE_INCL,
    ambiguous_mark_context_comment,
    metigah_zaqef_across_a_space_comment,
)
from py_html import wlc_utils_html


def _je_0910_and_11_comment(adjacent_verse_phrase: str):
    return (
        [
            f"The same word, מבלי, appears in the {adjacent_verse_phrase} with analogous transcription problems."
        ],
        [ambiguous_mark_context_comment("מבלי")],
        [
            f" It is aggressively uncharitable to transcribe the mark on מבלי as {TIPEXA}:"
            f" {TIPEXA} is the least likely of the three possible meanings of this mark."
            " Merkha is by far the most likely. If the mark were meteg, we would have to uncharitably"
            " assume that a maqaf is missing."
        ],
    )


_JE_1003_01 = (
    "As in many other cases we see in this document,"
    " BHS seems to be aggressively uncharitable in its transcription of this somewhat-ambiguous vertical line,"
    " avoiding the most likely intended meaning (here meteg)"
    " in favor of a less likely, indeed “illegal” alternative (here merkha)."
    " In this case the mark even lacks any inclination that would suggest merkha."
)


_JE_1003_02 = (
    "As usual, when we say an accent is “illegal” we mean that it does not conform to the consensus grammar of accents,"
    " given the surrounding accent-context."
    " Thus our degree of certainty that an accent is “illegal”"
    " depends on our degree of certainty about the surrounding accent-context."
    " At times, our degree of certainty about the context is not high,"
    f" for example due to ambiguity between merkha and {TIPEXA}."
    " I don’t think that is the case here, but I thought I would bring up the general point anyway."
)


_JE_1003_03 = "Finally, it should be noted that the mark preceding this chanted word’s yod is assumed to be a spacer."


_JE_4417_01 = (
    "A telisha qetanna is a postpositive accent: it belongs on the final letter of its"
    " chanted word. Here, though, it sits on the first letter, the kaf of כִּי, with nothing on the"
    " final yod. Because the grammar checker reads the Unicode-converted source, this"
    " misplacement of the mark is the only defect it can see."
)


_JE_4417_02 = (
    "We detect this in the lexical phase, alongside the unpaired zarqa/tsinnorit stress"
    " helpers, but the violation is really one of grammar within the chanted word: a rule about where"
    " inside one a postpositive accent may fall, not about the alphabet of marks."
    " It is one instance of a broader family of such rules we have not yet"
    " implemented in general — every postpositive accent must fall on its chanted word’s final"
    " letter, every prepositive on its first."
)


_JE_4417_03 = (
    "In the Michigan-Claremont source the defect is actually compound. The mark is coded"
    " 24 — the medial telisha qetanna, properly a stress helper to a following 04 — rather"
    " than 04, the real, postpositive telisha qetanna; and it is written one letter too"
    " early, on the kaf rather than the yod. The Unicode conversion erases the 24-versus-04"
    " distinction (both become the single telisha-qetanna codepoint), so only the"
    " misplacement survives for the checker; but the M-C also carries the additional coding"
    " error of a 24 stress helper with no 04 for it to help. An argument runs the other way,"
    " though: given that the mark is misplaced onto a nonfinal letter, coding it 04 there"
    " would arguably be worse, since as a 24 the chanted word at least obeys the invariant that 04"
    " falls only on a final letter and 24 only on a nonfinal one. It is not important to rank"
    " exactly how flawed this chanted word is."
)


_JE_4417_04 = (
    "The UXLC change linked above moves the telisha qetanna forward one letter, from the kaf"
    " to the yod, leaving a normal postpositive telisha qetanna on כִּי’s final letter. Being"
    " Unicode rather than M-C, UXLC has only the one telisha-qetanna codepoint to begin with,"
    " so there is no 24-versus-04 distinction for it to recode; relocating the mark is the"
    " whole of the fix."
)


_JE_4417_05 = [
    "Compare ",
    wlc_utils_html.anchor("je 26:5", {"href": "#obje26v5"}),
    ", a closely analogous case: there an unpaired pashta stress helper sits on the syllable where the real"
    " pashta belongs. In both verses the chanted word is finally stressed (and a single-syllable one"
    " like כי counts as finally stressed), so it needs — and should have — no stress helper at"
    " all. The cure is therefore not to supply the helper a “missing partner” accent, but to"
    " move the mark onto that chanted word’s final letter, where it stops being a stress helper and"
    " simply becomes the real postpositive accent.",
]


_JE_4417_06 = (
    "It remains to be determined whether this error originates in BHS — the more likely"
    " source, as with most errors discussed in this document — or is original to WLC,"
    " which is less likely but not unheard of."
)


BY_REF: dict[str, dict[str, object]] = {
    "je 9:10": {
        "st-source": "bhs",
        "st-summary": f"BHS transcribes a merkha as a {TIPEXA}.",
        "wlc_focus": "מבל֖י",
        "uxlc_change": "2023.04.01/2022.12.10-15",
        "comment": _je_0910_and_11_comment("next verse (11)"),
    },
    "je 9:11": {
        "st-source": "bhs",
        "st-summary": f"BHS transcribes a merkha as a {TIPEXA}.",
        "wlc_focus": "מבל֖י",
        "uxlc_change": "2023.04.01/2022.12.10-16",
        "comment": _je_0910_and_11_comment("previous verse (10)"),
    },
    "je 10:3": {
        "st-source": "bhs",
        "st-summary": "BHS transcribes a meteg as a merkha.",
        "wlc_focus": "יד֥י־",
        "img": "LC-251A-col-3-line-11-Je-10v3.png",
        "pending_uxlc_change": "2026.10.19/2026.04.10-8",
        "comment": (
            _JE_1003_01,
            _JE_1003_02,
            _JE_1003_03,
        ),
    },
    "je 31:32": {
        "st-source": "bhs",
        "st-summary": f"BHS transcribes a {MUNAX} as a {TIPEXA}.",
        "wlc_focus": "מא֖רץ",
        "uxlc_change": "2023.04.01/2022.12.10-41",
        "comment": "See the image in the UXLC change to which we link above.",
    },
    "je 37:10": {
        "st-source": "lc",
        "st-summary": "The LC has no maqaf after ונשארו.",
        "wlc_focus": "ונ֨שארו",
        "uxlc_note_page": "https://tanach.us/Notes/Jeremiah/Jeremiah.37.10.9-t.html",
        "comment": (
            metigah_zaqef_across_a_space_comment("ונ֨שארו־ב֔ם", "ונ֨שארו ב֔ם"),
            (
                "UXLC has read the manuscript here, and its note — to which we link above —"
                " reports that no maqaf occurs at the end of ונשארו, and that the gap between"
                " that atom’s final vav and the bet of בם is very small. The very small gap is"
                " why UXLC files a “t” note, a transcription it records as uncertain, rather"
                " than a change: the maqaf is absent, and the spacing does not read as an"
                " ordinary space either."
            ),
            [
                "Compare ",
                wlc_utils_html.anchor("gn 18:18", {"href": "#obgn18v18"}),
                ", the same shape, where nobody has read the manuscript and the source"
                " therefore stays open.",
            ],
        ),
    },
    "je 48:12": {
        "st-source": "bhs",
        "st-summary": f"BHS transcribes a meteg as a {TIPEXA}.",
        "wlc_focus": "הנ֖ה־",
        "img": "LC-272A-col-3-line-3-Je-48v12.png",
        "comment": (
            "Yet another aggressively uncharitable, overly-literal transcription by BHS."
            + " "
            + TIP_LIKE_INCL
        ),
    },
    "je 49:19": {
        "st-source": "bhs",
        "st-summary": "BHS misses a pashta on אריצנו, transcribing only its stress helper.",
        "wlc_focus": "אריצ֨נו",
        "uxlc_change": "2023.04.01/2022.12.10-60",
        "pending_uxlc_change": "2026.10.19/2026.04.10-3",
        "comment": (
            "See the image in the UXLC change to which we link above."
            " BHS transcribes only the pashta stress helper, not the pashta itself."
            " So, understandably, WLC transcribes this mark as a qadma."
            " The ERROR lands on the zaqef phrase over כי־ארגיעה אריצנו מעליה, which is"
            " where that mark is: with a qadma rather than a pashta on אריצנו, the phrase"
            " never forms."
            " The ERROR has not always landed there. While the checker’s metigah-zaqef fuse"
            " ran across a space, the qadma on אריצנו and the zaqef on מעליה — two chanted"
            " words — fused into one metigah-zaqef token, and the failure surfaced a phrase"
            f" to the left instead, on the {TIPEXA} phrase over אל־נוה איתן כי־ארגיעה. The"
            " fuse now stops at a space, as ITM §223 and CoS Ch. 5 §§4–6 require of a"
            " metigah, so the ERROR and the defect are in one place."
        ),
    },
    "je 26:5": {
        "st-source": "bhs",
        "wlc_focus": "דבר֨י",
        "st-summary": "BHS transcribes a syllable as having qadma rather than pashta.",
        "uxlc_change": "2023.04.01/2022.12.10-28",
        "comment": (
            [
                "In BHS, the mark is “late” on the ר, i.e. it is on the left of the ר rather than in its center."
                " If it were really a qadma, we would expect it to be centered on the ר."
            ],
            [
                " Instead, it looks like an unpaired pashta stress helper."
                " (Some typography centers a pashta stress helper,"
                " making it indistinguishable from a qadma, but BHS aligns them distinctly.)"
                " I.e. in BHS, the mark looks like a pashta stress helper with no real (end-of-chanted-word) pashta to accompany it."
                " (Note that that adding a real pashta to this chanted word would not fix it, since a stress helper on a final syllable makes no sense.)"
            ],
            [
                "So, though above I said “BHS transcribes a syllable as having qadma rather than pashta”,"
                " a more detailed account would be "
                "“BHS transcribes a syllable as having"
                " an unpaired pashta stress helper on its first letter rather than a pashta on its last letter,"
                " and WLC transcribes BHS’s unpaired stress helper as a qadma.”"
            ],
            [
                "Note that originally WLC had no distinction between a qadma and a pashta stress helper,"
                " using code 63 for both,"
                " but later WLC added a separate code for the pashta stress helper, code 33."
                " So WLC may have had no choice but to transcribe BHS’s unpaired stress helper as a qadma,"
                " since it may have had no code for a pashta stress helper at the time."
                " In any case, the serious error is BHS’s transcription, not WLC’s transcription of BHS."
            ],
            [
                "Compare ",
                wlc_utils_html.anchor("je 44:17", {"href": "#obje44v17"}),
                ", another unpaired stress helper — there a telisha qetanna helper (M-C 24)"
                " sitting on the syllable where the real (postpositive) telisha qetanna belongs. There too the"
                " chanted word is finally stressed (a single-syllable one like כי counts as finally"
                " stressed) and so needs no stress helper at all: the cure is to move the mark"
                " onto that chanted word’s final letter, where it becomes the real postpositive accent,"
                " not to add a separate real accent alongside the helper.",
            ],
        ),
    },
    "je 44:17": {
        "st-source": "tbd",
        "st-summary": (
            "A telisha qetanna is placed on a non-final letter rather than on its chanted word’s"
            " final letter."
        ),
        "wlc_focus": "כ֩י",
        "uxlc_change": "2023.04.01/2022.12.10-53",
        "comment": (
            _JE_4417_01,
            _JE_4417_02,
            _JE_4417_03,
            _JE_4417_04,
            _JE_4417_05,
            _JE_4417_06,
        ),
    },
    "je 28:2": {
        "st-source": "bhs",
        "wlc_focus": "שב֞רתי",
        "st-summary": BHS_TRANSCRIBES,
        "uxlc_change": "2023.04.01/2022.12.10-35",
    },
    "je 46:4": {
        "st-source": "bhs",
        "wlc_focus": "בכ֥ובע֑ים",
        "st-summary": "BHS transcribes a meteg as a merkha.",
        "img": "LC-271B-col-1-line-5-Je-46v4.png",
        "pending_uxlc_change": "2026.10.19/2026.04.10-9",
    },
    "je 51:9": {
        "st-source": "bhs",
        "wlc_focus": "רפ֣ינו",
        "st-summary": BHS_TRANSCRIBES,
        "pending_uxlc_change": "2026.10.19/2026.04.10-2",
    },
}
