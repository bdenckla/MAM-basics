from author_boj_util.job_common import BHQ_COMMENT_CMN_3105_3206
from author_boj_util.author import yyy_dash_nothing
from author_boj_util import author

RECORD_3102 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-noted-by-mam": True,
    "qr-cv": "31:2",
    "qr-consensus": "וּמֶ֤ה",
    "qr-lc-proposed": "וּמֶ֤ה׀",
    "qr-what-is-weird": "לגרמיה is present",
    "qr-highlight-lc-proposed": 4,
    "qr-lc-loc": {"page": "405B", "column": 1, "line": 15},
    "qr-ac-loc": {"page": "277v", "column": 2, "line": 24, "word": 1},
    "qr-generic-comment": [
        "An argument could be made that it is μL not μA that represents the consensus here."
        " For example, the Jerusalem Crown edition, despite normally staying quite close to μA,",
        " has לגרמיה in its body text",
        " and only notes in an appendix that μA has no לגרמיה.",
        #
        " See the $MAM documentation for this word",
        " for a list of where various manuscripts fall on this issue.",
    ],
}

RECORD_3104 = {
    "qr-cv": "31:4",
    "qr-lc-proposed": "ה֖וּא",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "ה֭וּא",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "405B", "column": 1, "line": 17},
    "qr-ac-loc": {"page": "277v", "column": 2, "line": 26, "word": 2},
    "qr-noted-by": "tBHQ-zdexiWLC",
}

_BHQ_COMMENT = [
    *BHQ_COMMENT_CMN_3105_3206,
    " $link_32_6 is similar.",
    " In my opinion $BHQ shows itself to be out of date by continuing to aspire,",
    " as $BHS did,",
    " to reflect all such ordering quirks.",
    " I think the modern consensus is that these orderings are as meaningless as",
    " the variable length of ascenders on ל.",
    " Nonetheless, since $BHQ still aspires to get these orderings right,",
    " it is fair for me to point out when it fails to do so.",
]
RECORD_3105 = {
    "qr-cv": "31:5",
    "qr-lc-proposed": "רַגְלֽ͏ִי׃",
    "qr-what-is-weird": "סילוק precedes חיריק",
    "qr-consensus": "רַגְלִֽי׃",
    "qr-highlight": 3,
    "qr-lc-loc": {"page": "405B", "column": 1, "line": -9, "including-blank-lines": 1},
    "qr-ac-loc": {"page": "277v", "column": 2, "line": 27, "word": 8},
    "qr-uxlc-position-within-verse": 8,
    "qr-bhq-comment": _BHQ_COMMENT,
    "qr-noted-by": "nBHL",
}

_GENCOM_PARA_2 = [
    "The two dots above the מ in the μY image are",
    " the pair of above-dots that is μY’s equivalent of a masorah circle.",
    " See $link_19_16_BMV0PY for another example of this two-dot callout notation.",
]
_BHQCOM_PART_1 = [
    "$BHQ reflects neither μL nor the consensus expectation here.",
    " It reflects μL except it places the סילוק under the א instead of the $vav.",
    #
    " This not only contradicts μL,",
    " but also makes no sense given the רפה on the א.",
    #
    " (Admittedly, the actual location in μL, under the $vav, doesn’t make any sense either.)",
    #
]
_BHQCOM_PART_2 = [
    "I would also argue that this particular רפה should have been shown,",
    " despite the general policy of $BHQ to ignore רפה marks in μL.",
    " In such a confusing word, the reader needs all the detail and context possible,",
    " such as this רפה mark.",
    " See also $link_19_2 for another case where רפה is important.",
]
_BHQCOM_PART_3 = [
    "$BHQ notes that here μL disagrees with μA and μY.",
    #
    " But $BHQ gives the מ in μA and μY a מרכא rather than a סילוק,",
    " which seems more likely a typo than a deliberate choice.",
]
RECORD_3107 = {
    "qr-cv": "31:7",
    "qr-lc-proposed": "מֻאֿוּֽם׃",
    "qr-what-is-weird": ["קובוץ-סילוק not ", yyy_dash_nothing("סילוק")],
    "qr-consensus": "מֽאֿוּם׃",
    "qr-highlight": [1, 3],
    "qr-lc-loc": {"page": "405B", "column": 1, "line": -6, "including-blank-lines": 1},
    "qr-ac-loc": {"page": "278r", "column": 1, "line": 2, "word": 5},
    "qr-generic-comment": [
        "The consensus has סילוק under מ and nothing (אפס (zero)) under $vav.",
        author.para(_GENCOM_PARA_2),
    ],
    "qr-bhq-comment": [
        author.para(_BHQCOM_PART_1),
        author.para(_BHQCOM_PART_2),
        author.para(_BHQCOM_PART_3),
    ],
    "qr-bhq": "מֻאֽוּם׃",
    "qr-noted-by": "nBHL-nDM-nWLC",
    # Above we consider this xBHQ because:
    #    Though it attempts to transcribe the quirk, it does so inaccurately.
    #    Though it notes the quirk, it does so inaccurately.
}

RECORD_3115 = {
    "qr-noted-by": "tWLC",
    "qr-cv": "31:15",
    "qr-consensus": "הֲ‍ֽלֹא־בַ֭בֶּטֶן",
    "qr-lc-proposed": "הֲ‍ֽ֝לֹא־בַ֭בֶּטֶן",
    "qr-lc-q": "(?)",
    "qr-what-is-weird": "גרש מוקדם fights דחי",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "405B", "column": 2, "line": 4},
    "qr-ac-loc": {"page": "278r", "column": 1, "line": 11, "word": 1},
    "qr-generic-comment": [
        "A גרש מוקדם accent doesn’t make sense here,",
        " and the color image suggests that the mark is not ink.",
    ],
    "qr-bhq-comment": [
        "$BHQ has wisely removed the גרש מוקדם that $BHS had here.",
        " Unfortunately, as always, $BHQ has not documented this change,",
        " leaving it as a painful “exercise left to the reader” to discover such changes.",
    ],
}

RECORD_3119 = {
    "qr-cv": "31:19",
    "qr-lc-proposed": "א֖וֹבֵד",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "א֭וֹבֵד",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "405B", "column": 2, "line": 9},
    "qr-ac-loc": {"page": "278r", "column": 1, "line": 15, "word": 3},
    "qr-noted-by": "tBHQ-zdexiWLC",
}

RECORD_3120 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "31:20",
    "qr-consensus": "כְּ֝בָשַׂ֗י",
    "qr-lc-proposed": "כְּ֝בָשַׂי",
    "qr-what-is-weird": "רביע of רביע מוגרש is absent",
    "qr-highlight": 3,
    "qr-lc-loc": {"page": "405B", "column": 2, "line": 10},
    "qr-ac-loc": {"page": "278r", "column": 1, "line": 17, "word": 2},
}

RECORD_3128 = {
    "qr-cv": "31:28",
    "qr-lc-proposed": "ה֖וּא",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "ה֭וּא",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "405B", "column": 2, "line": 18},
    "qr-ac-loc": {"page": "278r", "column": 1, "line": 25, "word": 5},
    "qr-noted-by": "tBHQ-zdexiWLC",
}

RECORD_3133 = {
    "qr-cv": "31:33",
    "qr-lc-proposed": "עֲוֺֽנִי׃",
    "qr-what-is-weird": "סילוק on $vav not נ",
    "qr-consensus": "עֲוֺנִֽי׃",
    "qr-highlight-lc-proposed": 2,
    "qr-highlight-consensus": 3,
    "qr-lc-loc": {"page": "405B", "column": 2, "line": -3},
    "qr-ac-loc": {"page": "278r", "column": 2, "line": 4, "word": 3},
    "qr-noted-by": "tBHQ-nBHL-nDM",
}

RECORD_3139 = {
    "qr-cv": "31:39",
    "qr-lc-proposed": "כֹּ֖חָהּ",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "כֹּ֭חָהּ",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "406A", "column": 1, "line": 5},
    "qr-ac-loc": {"page": "278r", "column": 2, "line": 11, "word": 2},
    "qr-noted-by": "tBHQ-zdexiWLC",
}
