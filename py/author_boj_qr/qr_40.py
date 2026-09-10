from author_boj_util import author

RECORD_4010 = {
    "qr-cv": "40:10",
    "qr-lc-q": "(?)",
    "qr-lc-proposed": "גָֽא֣וֹן",
    "qr-what-is-weird": "געיה is present (on ג)",
    "qr-consensus": "גָא֣וֹן",
    "qr-generic-comment": "The mark in question could easily be accidental.",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "408B", "column": 2, "line": -11},
    "qr-ac-loc": {"page": "281r", "column": 1, "line": 6, "word": 3},
    "qr-noted-by": "tBHQ-nBHL-nWLC",
}

RECORD_4019_HVA = {
    "qr-cv": "40:19",
    "qr-word-id": "HVA",
    "qr-lc-proposed": "ה֖וּא",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "ה֭וּא",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "408B", "column": 2, "line": 27},
    "qr-ac-loc": {"page": "281r", "column": 1, "line": 16, "word": 1},
    "qr-noted-by": "tBHQ-zdexiWLC",
}

RECORD_4019_H3JV = {
    "qr-noted-by": "nDM",
    "qr-cv": "40:19",
    "qr-word-id": "H3JV",
    "qr-consensus": "הָ֝עֹשׂ֗וֹ",
    "qr-lc-proposed": "הָ֝עֹשׂוֹ",
    "qr-what-is-weird": "רביע of רביע מוגרש is absent",
    "qr-highlight": 3,
    "qr-lc-loc": {"page": "408B", "column": 2, "line": 27},
    "qr-ac-loc": {"page": "281r", "column": 1, "line": 16, "word": 5},
    "qr-generic-comment": [
        "There is a confusing constellation of three dots surrounding the ש in μL,",
        " but only one of those dots, a $sin dot, belongs to the ש.",
        " Working backwards (to the right) from that $sin dot,",
        " the next dot is a “קמץ dot” belonging to the מ of %גרמיו on the line above.",
        " The next dot is a חולם חסר dot belonging to the ע.",
        " (Or, if you prefer an alternative interpretation of חולם חסר dots in general,",
        " the חולם חסר dot belongs to an implicit $vav between the ע and ש.)",
        " The issue at hand is there is no fourth dot",
        " that could be interpreted as a רביע above the ש.",
    ],
}

RECORD_4026 = {
    "qr-cv": "40:26",
    "qr-lc-proposed": "לֶֽחֱיוֹ׃",
    "qr-what-is-weird": "סילוק on ל not $yod",
    "qr-consensus": "לֶחֱיֽוֹ׃",
    "qr-highlight-lc-proposed": 1,
    "qr-highlight-consensus": 3,
    "qr-lc-loc": {"page": "409A", "column": 1, "line": 8},
    "qr-ac-loc": {"page": "281r", "column": 1, "line": 25, "word": 3},
    "qr-noted-by": "tBHQ-nBHL-nDM",
}

_COMMENT_PARA1 = [
    "In μY, the mark we would charitably transcribe as דחי",
    " appears far to the left of where we would expect it,",
    " i.e. far “later” than we would expect it.",
    " Possibly the ל ascender from the line below",
    " encroached on the area where the $naqdan would normally put a דחי;",
    " possibly the descender of the preceding ק was in the way, too.",
    " See $link_35_14 for an analogous case",
    " and some further discussion of this phenomenon",
    " of “late” דחי in general.",
]
_COMMENT_PARA2 = [
    "More significant than the “lateness” of the דחי in μY",
    " is its use of מונח rather than מקף on the previous atom,",
    [" i.e. on ", author.span_unpointed_tanakh("התשחק"), "."],
]
RECORD_4029 = {
    "qr-cv": "40:29",
    "qr-lc-proposed": "בּ֖וֹ",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "בּ֭וֹ",
    "qr-generic-comment": [
        author.para(_COMMENT_PARA1),
        author.para(_COMMENT_PARA2),
    ],
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "409A", "column": 1, "line": 11},
    "qr-ac-loc": {"page": "281r", "column": 1, "line": 27, "word": 5},
    "qr-noted-by": "tBHQ-zdexiWLC",
}
