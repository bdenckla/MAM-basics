from author_boj_util.job_common import BHQ_COMMENT_LIKE_0409
from author_boj_util.author import nothing_dash_yyy

RECORD_1508 = {
    "qr-cv": "15:8",
    "qr-lc-proposed": "אֱל֣וֹהַ",
    "qr-what-is-weird": "ה lacks מפיק",
    "qr-consensus": "אֱל֣וֹהַּ",
    "qr-highlight": 4,
    "qr-lc-loc": {"page": "401A", "column": 2, "line": -7},
    "qr-ac-loc": {"page": "274r", "column": 1, "line": 9, "word": 2},
    "qr-bhq-comment": BHQ_COMMENT_LIKE_0409,
    "qr-noted-by": "tBHQ-nBHL-nDM",
}

RECORD_1534 = {
    "qr-cv": "15:34",
    "qr-lc-proposed": "שֹֽׁ֥חַד׃",
    "qr-what-is-weird": "מרכא fights סילוק",
    "qr-consensus": "שֹֽׁחַד׃",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "401B", "column": 1, "line": -3},
    "qr-ac-loc": {"page": "274r", "column": 2, "line": 11, "word": 4},
    "qr-bhq-comment": "$BHQ silently ignores the possible מרכא.",
    "qr-noted-by": "nBHL",
}

RECORD_1535 = {
    "qr-cv": "15:35",
    "qr-lc-proposed": "וְיָלֹ֣ד",
    "qr-lc-q": "(?)",
    "qr-what-is-weird": [nothing_dash_yyy("מונח"), " not מונח-געיה"],
    "qr-consensus": "וְיָ֣לֹֽד",
    "qr-extra-letter-spacing": True,
    "qr-generic-comment": [
        "The proposed transcription of μL above shows nothing (אפס (zero)) on $yod and מונח on ל.",
        " (By “nothing” on $yod I mean nothing other than קמץ.)",
        " In contrast, the consensus transcription shows מונח on $yod and געיה on ל.",
        " (The געיה on ל is extraordinary since it follows the accent (מונח).)",
        " The proposed transcription seems far-fetched because"
        " there is little evidence of a מונח in any location on this word.",
        " There is a mark that looks like a פתח between the $yod and the ל,",
        " but that is grammatically implausible.",
    ],
    "qr-highlight": [2, 3],
    "qr-lc-loc": {"page": "401B", "column": 1, "line": -3},
    "qr-ac-loc": {"page": "274r", "column": 2, "line": 12, "word": 1},
    "qr-noted-by": "tBHQ-nDM",
}
