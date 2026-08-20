from author_boj_util import author
from author_boj_util.job_common import RECORD_2221_CMN_AB, CAM1753_PAGE_URL_BASE

_COMMENT_2221_A = [
    "A dot under the מ of %עמו is fairly clear.",
    " It is (charitably) not transcribed by $BHL_A,",
    " presumably based on the consensus expectation that it is absent.",
]
_BHQ_COMMENT_2221_A = [
    "$BHQ fails to note that the אתנח it transcribes on %עמו",
    " disagrees with μA and μY.",
]
_COMMENT_2221_A_CALLOUT = [
    "Note that instead of a masorah circle, μY uses a pair of above-dots",
    " as a “callout” for a Masorah parva note;",
    " hence the pair of above-dots above ל in %ושלם.",
    " See $link_19_16_BMV0PY for another example of this two-dot callout notation.",
]
RECORD_2221_3MV = {
    **RECORD_2221_CMN_AB,
    "qr-word-id": "3MV",
    "qr-lc-q": "(?)",
    "qr-lc-proposed": "עִמּ֑וֹ",
    "qr-what-is-weird": "אתנח not מונח",
    "qr-consensus": "עִמּ֣וֹ",
    "qr-generic-comment": [
        author.para(_COMMENT_2221_A),
        author.para(_COMMENT_2221_A_CALLOUT),
    ],
    "qr-highlight": 2,
    "qr-bhq-comment": _BHQ_COMMENT_2221_A,
    "qr-noted-by": "tBHQ-nBHL-nWLC",
    "qr-cam1753-page-url": f"{CAM1753_PAGE_URL_BASE}/n83/mode/1up",
    "qr-ac-loc": {"page": "276r", "column": 1, "line": 10, "word": 3},
}
