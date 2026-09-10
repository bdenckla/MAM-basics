from author_boj_util import author
from author_boj_util.num_range import num_range

RECORD_0303 = {
    "qr-cv": "3:3",
    "qr-lc-proposed": "י֖וֹם",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "י֭וֹם",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "397B", "column": 2, "line": 12},
    "qr-ac-loc": {"page": "270v", "column": 2, "line": 23, "word": 2},
    "qr-noted-by": "tBHQ-zdexiWLC",
}

RECORD_0304 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "3:4",
    "qr-consensus": "מִמַּ֑עַל",
    "qr-lc-proposed": "מִמָּ֑עַל",
    "qr-what-is-weird": "מ has קמץ not פתח",
    "qr-highlight": 2,
    "qr-lc-loc": {"page": "397B", "column": 2, "line": 14},
    "qr-ac-loc": {"page": "270v", "column": 2, "line": 25, "word": 1},
}

RECORD_0316 = {
    "qr-cv": "3:16",
    "qr-lc-proposed": "א֚וֹ",
    "qr-what-is-weird": "יתיב not מהפך",
    "qr-consensus": "א֤וֹ",
    "qr-generic-comment": [
        "The יתיב accent doesn’t make sense here because"
        " this is in the poetic rather than prose section of Job",
        [" ", author.paren(num_range("$plain_3_2", "$plain_42_6")), "."],
    ],
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "398A", "column": 1, "line": 3},
    "qr-ac-loc": {"page": "271r", "column": 1, "line": 11, "word": 1},
    "qr-bhq-comment": [
        "I don’t think $BHQ is really proposing that μL has יתיב here.",
        " This is more likely a typo (inherited from $BHS) than a deliberate choice.",
    ],
    "qr-noted-by": "tBHQ-zmiscWLC",
}
