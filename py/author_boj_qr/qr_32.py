from author_boj_util.job_common import BHQ_COMMENT_CMN_3105_3206
from author_boj_util.uxlc_change import uxlc_change
from author_boj_util.all_verses_but_this import leg_missing_before_g3yh_rby3

_BHQ_COMMENT = [
    *BHQ_COMMENT_CMN_3105_3206,
    " $link_31_5 is similar and discusses the matter at greater length.",
]
RECORD_3206 = {
    "qr-cv": "32:6",
    "qr-lc-proposed": "יְשִׁישׁ֑͏ִים",
    "qr-what-is-weird": "אתנח precedes חיריק",
    "qr-consensus": "יְשִׁישִׁ֑ים",
    "qr-highlight": 4,
    "qr-lc-loc": {"page": "406A", "column": 1, "line": -6},
    "qr-ac-loc": {"page": "278r", "column": 2, "line": 26, "word": 5},
    "qr-uxlc-position-within-verse": 11,
    "qr-bhq-comment": _BHQ_COMMENT,
    "qr-noted-by": "nBHL",
}

RECORD_3210 = {
    "qr-cv": "32:10",
    "qr-lc-proposed": "דֵּעִ֣י",
    "qr-what-is-weird": "ד has דגש",
    "qr-consensus": "דֵעִ֣י",
    "qr-generic-comment": [
        "There is little or no evidence of a דגש in the ד,",
        " and the consensus has no such דגש.",
    ],
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "406A", "column": 2, "line": 1},
    "qr-ac-loc": {"page": "278v", "column": 1, "line": 3, "word": 6},
    "qr-noted-by": "tBHQ-zUXLC",
    "qr-uxlc-change-url": uxlc_change("2023.10.19", "2023.06.10-40"),
}

RECORD_3211 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "32:11",
    "qr-consensus": "הוֹחַ֨לְתִּי׀",
    "qr-lc-proposed": "הוֹחַ֨לְתִּי",
    "qr-what-is-weird": "לגרמיה is absent",
    "qr-highlight": 7,
    "qr-lc-loc": {"page": "406A", "column": 2, "line": 1},
    "qr-ac-loc": {"page": "278v", "column": 1, "line": 4, "word": 2},
    "qr-generic-comment": leg_missing_before_g3yh_rby3("32:11"),
}
