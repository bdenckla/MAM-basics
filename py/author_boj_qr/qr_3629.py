from author_boj_util.job_common import correctly_ignores

_COMMENT = [
    "The color image strongly suggests that the mark in question is not ink.",
    " A געיה right next to סילוק like that would be extraordinary, by the way,",
    " though no appeal to expectations is needed to dismiss this possible געיה.",
]
RECORD_3629 = {
    "qr-cv": "36:29",
    "qr-lc-proposed": "סֻכָּֽתֽוֹ׃",
    "qr-what-is-weird": "כ has געיה",
    "qr-consensus": "סֻכָּתֽוֹ׃",
    "qr-generic-comment": _COMMENT,
    "qr-highlight": 2,
    "qr-lc-loc": {"page": "407B", "column": 1, "line": -5},
    "qr-ac-loc": {"page": "279v", "column": 2, "line": 13, "word": 4},
    "qr-bhq-comment": correctly_ignores("געיה", "36:29", "large"),
    "qr-noted-by": "nBHL",
}
