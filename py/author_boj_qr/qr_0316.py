from author_boj_util import author
from author_boj_util.num_range import num_range

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
