from author_boj_util import author
from author_boj_util.all_verses_but_this import ptx_is_not_xtf

_COMMENT_PARA2 = [
    "In this case, μY agrees with μL against μA:",
    " the פתח in μY is a full פתח, not a חטף פתח.",
    " As for the two other similar cases,",
    " note that μY also agrees with μL against μA in $link_27_9",
    " (to the extent that the μY image permits such a judgement)",
    " but μY agrees with μA against μL in $link_9_35.",
]
_COMMENT_PARA3 = [
    "It is perhaps significant that the cases here and in $link_27_9,",
    " the cases of likely μY/μL agreement,",
    " concern an initial ה whereas $link_9_35 concerns an initial א.",
    " Although for many purposes all four gutturals behave the same,",
    " this may be one of those cases where this is not true.",
]
RECORD_3433_HM3M5 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "34:33",
    "qr-word-id": "HM3M5",
    "qr-consensus": "הֲֽמֵעִמְּךָ֬",
    "qr-lc-proposed": "הַֽמֵעִמְּךָ֬",
    "qr-what-is-weird": "פתח on ה is not חטף",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "407A", "column": 1, "line": 16},
    "qr-ac-loc": {"page": "279r", "column": 2, "line": 11, "word": 6},
    "qr-generic-comment": [
        author.para(ptx_is_not_xtf("34:33")),
        author.para(_COMMENT_PARA2),
        author.para(_COMMENT_PARA3),
    ],
}
