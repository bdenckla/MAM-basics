from author_boj_util.uxlc_change import uxlc_change
from author_boj_util.golinets import golinets_citation
from author_boj_util import author

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
