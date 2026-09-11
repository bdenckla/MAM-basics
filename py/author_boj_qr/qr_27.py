from author_boj_util.all_verses_but_this import ptx_is_not_xtf
from author_boj_util.uxlc_change import uxlc_change

_COMMENT = [
    "Perhaps there was a מקף",
    " that was ignored during re-inking,",
    " leaving only some very faint evidence of this מקף.",
    " In μA, as in μL, evidence of מקף is minimal.",
    " In μY, the מקף is clear.",
    " By the way, in μL, the evidence for the דחי",
    " on the א of the next word is very faint.",
]
_BHQ_COMMENT = [
    "$BHQ silently supplies the מקף that is the consensus expectation,",
    " despite little or no evidence for it in μL.",
]
RECORD_2702 = {
    "qr-cv": "27:2",
    "qr-lc-proposed": "חַי",
    "qr-what-is-weird": "מקף is absent",
    "qr-consensus": "חַי־",
    "qr-generic-comment": _COMMENT,
    "qr-highlight-consensus": 3,
    "qr-lc-loc": {"page": "404A", "column": 2, "line": -2},
    "qr-ac-loc": {"page": "276v", "column": 2, "line": 11, "word": 1},
    "qr-bhq-comment": _BHQ_COMMENT,
    "qr-noted-by": "nBHL-nDM",
}

RECORD_2709 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "27:9",
    "qr-consensus": "הֲֽ֭צַעֲקָתוֹ",
    "qr-lc-proposed": "הַֽ֭צַעֲקָתוֹ",
    "qr-what-is-weird": "פתח on ה is not חטף",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "404B", "column": 1, "line": 7},
    "qr-ac-loc": {"page": "276v", "column": 2, "line": 20, "word": 1},
    "qr-generic-comment": [
        *ptx_is_not_xtf("27:9"),
        " In μA it is difficult to tell whether the פתח is חטף,"
        " but my guess is that it is not,"
        " i.e. my guess is that it matches μL in this respect.",
    ],
}

RECORD_2713 = {
    "qr-cv": "27:13",
    "qr-lc-proposed": "מִשַׁדַּ֥י",
    "qr-what-is-weird": "ש lacks דגש",
    "qr-consensus": "מִשַּׁדַּ֥י",
    "qr-generic-comment": [
        "See $link_24_1 for discussion of the דגש in ש in %שדי.",
        " In μA, the center of the ש in question is such a blur"
        " that it is impossible to say whether a דגש is there or not.",
    ],
    "qr-highlight": 2,
    "qr-lc-loc": {"page": "404B", "column": 1, "line": 12},
    "qr-ac-loc": {"page": "276v", "column": 2, "line": 25, "word": 6},
    "qr-noted-by": "nUXLC",
    "qr-uxlc-change-url": uxlc_change("2022.04.01", "2022.02.17-3"),
}
