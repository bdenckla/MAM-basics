from author_boj_util import author
from author_boj_util.job_common import BHQ_COMMENT_XELSEWHERE_DUBIOUS

_COM1 = [
    "I have shown the consensus with רפה to make my point clearer,",
    " but a consensus edition would not typically show it.",
    #
    " (It would, as usual, merely imply it rather than show it.)",
]
_COM2 = [
    "In contrast, I show the רפה on the proposed reading,",
    " because I feel it should be shown in any edition that, like $BHQ, has דגש.",
    " This רפה is important, to highlight the weirdness of the situation.",
    #
    " In other words, by showing the רפה on the proposed reading,",
    " I am sort of charitably transcribing $BHQ.",
]
_COM3 = [
    "A דגש on a letter with רפה doesn’t make sense.",
    " The dot in question is suspiciously larger than nearby ones,",
    " and looks different from them in other ways.",
    #
    " See $link_19_5.",
]
RECORD_2416 = {
    "qr-cv": "24:16",
    "qr-lc-proposed": "יָ֥דְּֿעוּ",
    "qr-lc-q": "(?)",
    "qr-what-is-weird": "דגש fights רפה",
    "qr-consensus": "יָ֥דְֿעוּ",
    "qr-generic-comment": [
        author.para(_COM1),
        author.para(_COM2),
        author.para(_COM3),
    ],
    "qr-highlight": 2,
    "qr-lc-loc": {"page": "404A", "column": 1, "line": -12},
    "qr-ac-loc": {"page": "276v", "column": 1, "line": 3, "word": 5},
    "qr-bhq-comment": BHQ_COMMENT_XELSEWHERE_DUBIOUS,
    "qr-noted-by": "nBHQ",
    "qr-uxlc-needs-fix": True,
}
