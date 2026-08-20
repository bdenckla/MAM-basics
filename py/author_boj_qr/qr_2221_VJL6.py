from author_boj_util.job_common import RECORD_2221_CMN_AB

_COMMENT_2221_B = [
    "Perhaps some very faint remains of an אתנח under ל can be seen.",
    " The top dot of the שווא (under the ש) is very faint.",
]
_BHQ_COMMENT_2221_B = [
    "$BHQ (charitably) transcribes the top dot of the שווא",
    " using, as one often has to, faint evidence bolstered by consensus expectations.",
    " $BHQ notes (as does $BHS) that whereas the ל of %ושלם is unpointed in μL,",
    " that ל has קמץ and אתנח in μA and μY.",
]
RECORD_2221_VJL6 = {
    **RECORD_2221_CMN_AB,
    "qr-word-id": "VJL6",
    "qr-lc-proposed": "וּשְׁלם",
    "qr-what-is-weird": "ל lacks קמץ-אתנח",
    "qr-consensus": "וּשְׁלָ֑ם",
    "qr-generic-comment": _COMMENT_2221_B,
    "qr-highlight": 3,
    "qr-lc-loc": {"page": "403B", "column": 1, "line": -6},
    "qr-ac-loc": {"page": "276r", "column": 1, "line": 10, "word": 4},
    "qr-bhq-comment": _BHQ_COMMENT_2221_B,
    "qr-noted-by": "nBHQ-nWLC",
}
