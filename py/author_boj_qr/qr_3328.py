from author_boj_util import author

_COMMENT_PARA1 = [
    "Note that above we only show (and are only concerned with) the קרי form.",
]
_COMMENT_PARA2 = [
    "In μA, the letters are so faint as to be almost illegible,",
    " but as is often the case in μA, the pointing is quite clear,",
    " perhaps because it was done in an ink that aged better.",
    " Fortunately it is the pointing, not the letters,",
    " that are at issue here, and in any case,",
    " the pointing allows us to “back-decipher” the letters",
    " and see that the רביע dot in question is indeed present",
    " on top of the (faint) ת.",
]
_COMMENT_PARA3 = [
    "In all three manuscripts,",
    " an orphan חולם dot appears between the ת",
    " and the $yod of the כתיב letters.",
    " It belongs, conceptually, to the $vav of the קרי.",
]
_COMMENT_PARA4 = [
    "In μY, another dot appears above the $yod,",
    " very large compared to the other dots, and oval rather than round.",
    " I am not sure how to interpret it.",
]
RECORD_3328 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "33:28",
    "qr-consensus": "וְ֝חַיָּת֗וֹ",
    "qr-consensus-ketiv": "וחיתי",
    "qr-lc-proposed": "וְ֝חַיָּתוֹ",
    "qr-what-is-weird": "רביע of רביע מוגרש is absent",
    "qr-highlight": 4,
    "qr-lc-loc": {"page": "406B", "column": 1, "line": 24},
    "qr-ac-loc": {"page": "278v", "column": 2, "line": 21, "word": 5},
    "qr-generic-comment": [
        author.para(_COMMENT_PARA1),
        author.para(_COMMENT_PARA2),
        author.para(_COMMENT_PARA3),
        author.para(_COMMENT_PARA4),
    ],
}
