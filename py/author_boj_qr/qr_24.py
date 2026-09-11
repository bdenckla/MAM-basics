from author_boj_util.uxlc_change import uxlc_change
from author_boj_util.golinets import golinets_citation
from author_boj_util import author
from author_boj_util.job_common import BHQ_COMMENT_XELSEWHERE_DUBIOUS

_UXLC_CHANGE_2022_02_17_1 = uxlc_change("2022.04.01", "2022.02.17-1")
_ISAIAH = author.anc_h("$Isaiah_13_6", _UXLC_CHANGE_2022_02_17_1)


_COMMENT_PARA_1 = [
    "The writing is not well preserved here:",
    " the letters have been re-inked,",
    " but among the points, only the דגש in the ד has been re-inked.",
    " So, a דגש in the ש could easily have been lost.",
    " But, because other similar words lack דגש in μL",
    [" (e.g., $link_27_13, ", _ISAIAH, ", $Joel_1_15),"],
    " it seems likely that there was never a דגש in the ש to begin with.",
]
_COMMENT_PARA_2 = [
    ["This case and that of $link_27_13 are raised in ", golinets_citation("242")],
    [" $link_21_15 seems possibly analogous, but not mentioned in Golinets."],
]
_COMMENT_PARA_3 = [
    "Aside: note that the final פתח",
    " is charitably transcribed as belonging to the ד rather than the $yod.",
]

RECORD_2401 = {
    "qr-cv": "24:1",
    "qr-lc-proposed": "מִ֭שַׁדַּי",
    "qr-what-is-weird": "ש lacks דגש",
    "qr-consensus": "מִ֭שַּׁדַּי",
    "qr-generic-comment": [
        author.para(_COMMENT_PARA_1),
        author.para(_COMMENT_PARA_2),
        author.para(_COMMENT_PARA_3),
    ],
    "qr-highlight": 2,
    "qr-lc-loc": {"page": "403B", "column": 2, "line": 25},
    "qr-ac-loc": {"page": "276r", "column": 2, "line": 11, "word": 6},
    "qr-noted-by": "nUXLC",
    "qr-uxlc-change-url": uxlc_change("2022.04.01", "2022.02.17-2"),
}

RECORD_2405 = {
    "qr-cv": "24:5",
    "qr-lc-proposed": "בַּֽמִּדְבָּ֗ר",
    "qr-what-is-weird": "געיה not מרכא",
    "qr-consensus": "בַּ֥מִּדְבָּ֗ר",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "404A", "column": 1, "line": 1},
    "qr-ac-loc": {"page": "276r", "column": 2, "line": 16, "word": 3},
    "qr-noted-by": "tBHQ-zUXLC",
    "qr-uxlc-change-url": uxlc_change("2023.10.19", "2023.06.10-31"),
}

RECORD_2413 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "24:13",
    "qr-consensus": "בְּֽמֹרְדֵ֫י א֥וֹר",
    "qr-lc-proposed": "בְּֽמֹרְדֵ֫י־א֥וֹר",
    "qr-what-is-weird": "מקף is present",
    "qr-generic-comment": [
        "Gray מקף in $MAM.",
    ],
    # XXX perhaps MAM should note מקף in L.
    "qr-lc-loc": {"page": "404A", "column": 1, "line": 11},
    "qr-ac-loc": {"page": "276r", "column": 2, "line": 26, "word": 1},
}

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

RECORD_2418 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "24:18",
    "qr-consensus": "לֹא־יִ֝פְנֶ֗ה",
    "qr-lc-proposed": "לֹא־יִ֝פְנֶה",
    "qr-what-is-weird": "רביע of רביע מוגרש is absent",
    "qr-highlight": 6,
    "qr-lc-loc": {"page": "404A", "column": 1, "line": 19},
    "qr-ac-loc": {"page": "276v", "column": 1, "line": 6, "word": 2},
}

_COMMENT = [
    "Perhaps there is some very faint evidence of a third dot that would make a סגול,",
    " but this could be just wishful thinking.",
    " Note that there is a third dot above the two clearer dots,",
    " but I take that to be part of the ע that did not flake off like its neighboring ink did.",
]
_BHQ_COMMENT = [
    "$BHQ silently supplies the סגול that is the consensus expectation.",
    " I.e. despite little or no evidence for it in μL,",
    " $BHQ silently infers a third dot centered below the two clearer dots.",
]
RECORD_2421 = {
    "qr-cv": "24:21",
    "qr-lc-q": "(?)",
    "qr-lc-proposed": "רֹעֵ֣ה",
    "qr-what-is-weird": "צירה not סגול",
    "qr-consensus": "רֹעֶ֣ה",
    "qr-generic-comment": _COMMENT,
    "qr-highlight": 2,
    "qr-lc-loc": {"page": "404A", "column": 1, "line": -6},
    "qr-ac-loc": {"page": "276v", "column": 1, "line": 10, "word": 1},
    "qr-bhq-comment": _BHQ_COMMENT,
    "qr-noted-by": "nBHL-nDM",
}
