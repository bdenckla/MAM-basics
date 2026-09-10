from author_boj_util.all_verses_but_this import no_dag_after_mah
from author_boj_util.job_common import BHQ_COMMENT_LIKE_0409

_COMMENT = [
    "Though it is not relevant to the point at hand, which is the presence of a מקף,",
    " note that in μL, the shape we take to be מחפך is touching the bottom of the ל.",
]
_BHQ_COMMENT = [
    "Though it is not relevant to the point at hand,",
    " note that $BHQ continues to fail to distinguish",
    " between גלגל and אתנח הפוך.",
]
RECORD_1604 = {
    "qr-cv": "16:4",
    "qr-lc-proposed": "ל֤וּ־יֵ֪שׁ",
    "qr-what-is-weird": "מקף is present",
    "qr-consensus": "ל֤וּ יֵ֪שׁ",
    "qr-generic-comment": _COMMENT,
    "qr-highlight-lc-proposed": 3,
    "qr-lc-loc": {"page": "401B", "column": 2, "line": 3},
    "qr-ac-loc": {"page": "274r", "column": 2, "line": 16, "word": 5},
    "qr-bhq-comment": _BHQ_COMMENT,
    "qr-noted-by": "tBHQ-nBHL",
}

RECORD_1606 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "16:6",
    "qr-consensus": "מַה־מִּנִּ֥י",
    "qr-lc-proposed": "מַה־מִנִּ֥י",
    "qr-what-is-weird": "מ after %מח lacks דגש",
    "qr-highlight": 4,
    "qr-lc-loc": {"page": "401B", "column": 2, "line": 7, "line2": 8},
    "qr-ac-loc": {"page": "274r", "column": 2, "line": 20, "word": 3},
    "qr-generic-comment": [
        no_dag_after_mah("16:6"),
    ],
}

RECORD_1613 = {
    "qr-cv": "16:13",
    "qr-lc-proposed": "מְרֵרָֽתִי׃",
    "qr-what-is-weird": "סילוק on 2nd ר not ת",
    "qr-consensus": "מְרֵרָתִֽי׃",
    "qr-highlight-lc-proposed": 3,
    "qr-highlight-consensus": 4,
    "qr-lc-loc": {"page": "401B", "column": 2, "line": -10},
    "qr-ac-loc": {"page": "274v", "column": 1, "line": 2, "word": 3},
    "qr-noted-by": "tBHQ-nBHL-nDM",
}

RECORD_1620 = {
    "qr-cv": "16:20",
    "qr-lc-proposed": "אֱ֝ל֗וֹהַ",
    "qr-what-is-weird": "ה lacks מפיק",
    "qr-consensus": "אֱ֝ל֗וֹהַּ",
    "qr-highlight": 4,
    "qr-lc-loc": {"page": "401B", "column": 2, "line": -2},
    "qr-ac-loc": {"page": "274v", "column": 1, "line": 9, "word": 4},
    "qr-bhq-comment": BHQ_COMMENT_LIKE_0409,
    "qr-noted-by": "tBHQ-nBHL-nDM",
}
