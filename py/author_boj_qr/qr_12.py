from author_boj_util.uxlc_change import uxlc_change

_BHQ_COMMENT = [
    "$BHQ silently supplies the מקף that is the consensus expectation,",
    " despite no evidence for it in μL.",
]
RECORD_1203 = {
    "qr-cv": "12:3",
    "qr-lc-proposed": "וְאֶת",
    "qr-what-is-weird": "מקף is absent",
    "qr-consensus": "וְאֶת־",
    "qr-highlight-consensus": 4,
    "qr-lc-loc": {"page": "400A", "column": 2, "line": -1},
    "qr-ac-loc": {"page": "273r", "column": 2, "line": 1, "word": 1},
    "qr-bhq-comment": _BHQ_COMMENT,
    "qr-noted-by": "nBHL-nDM",
}

RECORD_1209 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "12:9",
    "qr-consensus": "יַד־יְ֝הֹוָ֗ה",
    "qr-intermediate": "יַד־יְ֝הוָ֗ה",
    # qr-intermediate is the consensus with any differences removed
    # that are not important to us here.
    # In this case, the only such difference is the חולם חסר dot’s absence from μL.
    "qr-lc-proposed": "יַד־יְ֝הוָה",
    "qr-what-is-weird": "רביע of רביע מוגרש is absent",
    "qr-highlight": 6,
    "qr-lc-loc": {"page": "400B", "column": 1, "line": 9},
    "qr-ac-loc": {"page": "273r", "column": 2, "line": 9, "word": 2},
    "qr-generic-comment": [
        "The חולם חסר dot’s absence from μL is not important to us here."
    ],
}

RECORD_1216 = {
    "qr-cv": "12:16",
    "qr-lc-proposed": "וְתֽוּשִׁיָּ֑ה",
    "qr-lc-q": "(?)",
    "qr-what-is-weird": "ת has געיה",
    "qr-consensus": "וְתוּשִׁיָּ֑ה",
    "qr-generic-comment": [
        "There is a blob of ink below the ת.",
        " Most likely, this mark is a malformed masorah circle",
        " on the word %מוליך on the line below.",
    ],
    "qr-bhq-comment": [
        "$BHQ seems to transcribe the blob of ink as both",
        " a געיה on ת and a masorah circle on %מוליך.",
        " $BHS did not have this געיה;",
        " I wish $BHQ had left well enough alone.",
    ],
    "qr-highlight": 2,
    "qr-lc-loc": {"page": "400B", "column": 1, "line": -11},
    "qr-ac-loc": {"page": "273r", "column": 2, "line": 16, "word": 6},
    "qr-noted-by": "tBHQ-nWLC",
}

RECORD_1219 = {
    "qr-cv": "12:19",
    "qr-lc-proposed": "וְאֵֽתָנִ֣ים",
    "qr-what-is-weird": "געיה not טרחא",
    "qr-consensus": "וְאֵ֖תָנִ֣ים",
    "qr-highlight": 2,
    "qr-lc-loc": {"page": "400B", "column": 1, "line": 20},
    "qr-ac-loc": {"page": "273r", "column": 2, "line": 20, "word": 1},
    "qr-noted-by": "tBHQ-zUXLC",
    "qr-noted-by-mam": True,
    "qr-uxlc-change-url": uxlc_change("2023.10.19", "2023.06.10-12"),
}
