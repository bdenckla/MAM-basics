from author_boj_util.all_verses_but_this import no_dag_after_mah
from author_boj_util.uxlc_change import uxlc_change

RECORD_2107 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "21:7",
    "qr-consensus": "מַ֭דּוּעַ",
    "qr-lc-proposed": "מַ֣דּוּעַ",
    "qr-what-is-weird": "מונח not דחי",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "403A", "column": 1, "line": 16, "including-blank-lines": 1},
    "qr-ac-loc": {"page": "275v", "column": 1, "line": 10, "word": 4},
}

RECORD_2115 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "21:15",
    "qr-consensus": "מַה־שַּׁדַּ֥י",
    "qr-lc-proposed": "מַה־שַׁדַּ֥י",
    "qr-what-is-weird": "ש lacks דגש",
    "qr-generic-comment": [
        no_dag_after_mah("21:15"),
        " Aside: μA lacks the מקף.",
        " Our best guess is that μY has the consensus דגש"
        " but it is only visible as a small bump on the right"
        " of the center arm of the three arms of the שׁ.",
    ],
    "qr-highlight": 4,
    "qr-lc-loc": {"page": "403A", "column": 1, "line": 26},
    "qr-ac-loc": {"page": "275v", "column": 1, "line": 20, "word": 1},
}

_COMMENT = [
    "The dot is suspiciously brown rather than black,",
    " making me wonder whether the $vav was pointed at all.",
]
_BHQ_COMMENT = [
    "$BHQ silently supplies the שווא that is the consensus expectation,",
    " despite little or no evidence for it in μL.",
]
RECORD_2125 = {
    "qr-cv": "21:25",
    "qr-lc-proposed": "וִלֹֽא־",
    "qr-what-is-weird": "חיריק not שווא",
    "qr-consensus": "וְלֹֽא־",
    "qr-generic-comment": _COMMENT,
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "403A", "column": 2, "line": 13},
    "qr-ac-loc": {"page": "275v", "column": 2, "line": 3, "word": 5},
    "qr-bhq-comment": _BHQ_COMMENT,
    "qr-noted-by": "nBHL",
}

RECORD_2134 = {
    "qr-cv": "21:34",
    "qr-lc-proposed": "וּ֝תְשֽׁוּבֹתֵיכֶ֗ם",
    "qr-what-is-weird": "געיה not מרכא",
    "qr-consensus": "וּ֝תְשׁ֥וּבֹתֵיכֶ֗ם",
    "qr-highlight": 3,
    "qr-lc-loc": {"page": "403A", "column": 2, "line": 24},
    "qr-ac-loc": {"page": "275v", "column": 2, "line": 14, "word": 4},
    "qr-noted-by": "tBHQ-zUXLC",
    "qr-uxlc-change-url": uxlc_change("2023.10.19", "2023.06.10-24"),
}
