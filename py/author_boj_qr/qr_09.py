from author_boj_util.uxlc_change import uxlc_change
from author_boj_util.job_common import BHQ_COMMENT_0914_AND_0930
from author_boj_util.all_verses_but_this import ptx_is_not_xtf

RECORD_0906 = {
    "qr-cv": "9:6",
    "qr-lc-proposed": "יִתְפַלָּצֽוּן׃",
    "qr-what-is-weird": "פ lacks דגש",
    "qr-consensus": "יִתְפַּלָּצֽוּן׃",
    "qr-generic-comment": [
        "In μL, there is a bump on top of the פ that might be a misplaced דגש.",
        " In μA, too, it is not clear that a דגש is present in the פ.",
        " The text is not in good enough condition to make a strong conclusion one way or the other.",
        " In μA there is a strange horizontal line inside the ת that should be charitably ignored",
        " rather than aggressively interpreted as a דגש.",
        " Same goes for the weird dot inside the ת but lower down.",
    ],
    "qr-highlight": 3,
    "qr-lc-loc": {"page": "399B", "column": 1, "line": 12, "including-blank-lines": 1},
    "qr-ac-loc": {"page": "272v", "column": 1, "line": 2, "word": 2},
    "qr-noted-by": "tBHQ-nWLC",
}

RECORD_0910 = {
    "qr-cv": "9:10",
    "qr-lc-proposed": "וְנִפְלָא֗וֹת",
    "qr-what-is-weird": "$vav lacks גרש מוקדם",
    "qr-consensus": "וְ֝נִפְלָא֗וֹת",
    "qr-generic-comment": [
        "As $UXLC notes, the possible גרש מוקדם appears to be doubled,",
        " possibly as the result of a single stroke whose only remains are its edges.",
    ],
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "399B", "column": 1, "line": 16},
    "qr-ac-loc": {"page": "272v", "column": 1, "line": 6, "word": 1},
    "qr-bhq-comment": [
        "The evidence for this גרש מוקדם is slim,",
        " so $BHQ’s choice to leave it out is reasonable.",
        " Having left it out though,"
        " $BHQ should have noted its absence, i.e. noted the divergence from consensus.",
        #
        " Note that a missing גרש מוקדם is a more serious issue than a missing רביע,",
        " because the רביע is, effectively, just a stress helper.",
        #
        " In contrast, the גרש מוקדם defines the accent to be, overall, רביע מוגרש.",
    ],
    "qr-noted-by": "tBHQ-zUXLC",
    "qr-uxlc-change-url": uxlc_change("2022.10.19", "2022.07.05-3"),
}

RECORD_0914 = {
    "qr-cv": "9:14",
    "qr-lc-q": "(?)",
    "qr-lc-proposed": "עִמּוֹ׃",
    "qr-what-is-weird": "סילוק is missing",
    "qr-consensus": "עִמּֽוֹ׃",
    "qr-highlight": 2,
    "qr-lc-loc": {"page": "399B", "column": 1, "line": 22, "including-blank-lines": 1},
    "qr-ac-loc": {"page": "272v", "column": 1, "line": 11, "word": 2},
    "qr-bhq-comment": BHQ_COMMENT_0914_AND_0930,
    "qr-noted-by": "nBHL",
}

RECORD_0930 = {
    "qr-cv": "9:30",
    "qr-lc-q": "(?)",
    "qr-lc-proposed": "כַּפָּי׃",
    "qr-what-is-weird": "סילוק is missing",
    "qr-consensus": "כַּפָּֽי׃",
    "qr-highlight": 2,
    "qr-lc-loc": {"page": "399B", "column": 2, "line": 15},
    "qr-ac-loc": {"page": "272v", "column": 2, "line": 1, "word": 5},
    "qr-bhq-comment": BHQ_COMMENT_0914_AND_0930,
    "qr-noted-by": "nBHL",
}

RECORD_0935 = {
    "qr-cv": "9:35",
    "qr-lc-proposed": "אַֽ֭דַבְּרָה",
    "qr-what-is-weird": "פתח on א is not חטף",
    "qr-consensus": "אֲֽ֭דַבְּרָה",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "399B", "column": 2, "line": -8},
    "qr-ac-loc": {"page": "272v", "column": 2, "line": 5, "word": 4},
    "qr-noted-by": "tBHQ-nBHL-nDM",
    "qr-generic-comment": ptx_is_not_xtf("9:35"),
}
