from boj_render import boj_html
from author_boj_util import author
from author_boj_util.common_titles_etc import d5_anchor

RECORD_3812_HMYMY5 = {
    "qr-cv": "38:12",
    "qr-word-id": "HMYMY5",
    "qr-lc-proposed": "הְֽ֭מִיָּמֶיךָ",
    "qr-what-is-weird": "simple שווא not חטף פתח",
    "qr-consensus": "הֲֽ֭מִיָּמֶיךָ",
    "qr-generic-comment": "$link_39_20 is similar",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "408A", "column": 1, "line": -12},
    "qr-ac-loc": {"page": "280r", "column": 2, "line": 6, "word": 5},
    "qr-bhq-comment": [
        "$BHQ notes that here μL disagrees with μA and μY,",
        " which have the consensus pointing.",
    ],
    "qr-noted-by": "nBHQ-nBHL-nDM-nWLC",
}

_GENCOM_1 = [
    "The consensus is that this is one of those כתיב/קרי cases",
    " where the word boundary shifts",
    " from being after a ה to before that ה.",
    [
        " I.e. ",
        author.span_unpointed_tanakh("ידעתה שחר"),
        " becomes ",
        author.span_unpointed_tanakh("ידעת השחר"),
        ".",
    ],
    " I.e. the ה that is at the end of the first word in the כתיב",
    " moves to the start of the second word in the קרי.",
    " Similar cases include",
    [
        " $2Samuel_5_2 (the כתיב is ",
        author.span_unpointed_tanakh("הייתה מוציא"),
        ") and",
    ],
    [
        " $Ezekiel_42_9 (the כתיב is ",
        author.span_unpointed_tanakh("ומתחתה לשכות"),
        ").",
    ],
    " ",
    boj_html.anchor(
        "φ1",
        {"href": "#patah-comparison", "id": "patah-comparison-callout"},
    ),
    " In contrast to the consensus, in going from כתיב to קרי,",
    [" μL can be thought of as having ", boj_html.bold("copied")],
    " the ה to the second word rather than moving it.",
]
_GENCOM_2 = [
    "Aside: the Jerusalem Crown edition, despite normally staying quite close to μA,",
    " found μA’s pointing of the כתיב to be too confusing for its body text,",
    " relegating it to an appendix.",
    #
    " The question is where on the כתיב letters",
    " should we put the פתח that implicitly belongs to the ה of %השחר.",
    #
    " Both μA and μL put this פתח on the ה of %ידעתה.",
    #
    " In its body text, the Jerusalem Crown edition puts the פתח on no letter:",
    " instead, it floats before the ש of %שחר.",
    #
    " A vowel mark floating like this before a כתיב word has manuscript precedent.",
    #
    " I.e. although the Jerusalem Crown edition is diverging from the manuscript here,",
    " it is not diverging from manuscript tradition in general by using this notation.",
    #
    [" For more on orphan pointing, see my ", d5_anchor("../jobn")],
]
_EZEKIEL_COMPARISON = [
    "The similar כתיב/קרי word-boundary shifts have different mark attachments in μA.",
    " In the Job case that is our main focus here, the פתח in question clearly belongs to the ה.",
    " In $Ezekiel_42_9, however, the פתח is unattached;",
    " despite a seemingly-available “mobile ה” to attach it to, the $naqdan avoids doing so.",
    " (We use “mobile ה” to describe the relationship between the כתיב, which is ",
    author.span_unpointed_tanakh("ומתחתה לשכות"),
    ", and the קרי, which is ",
    author.span_unpointed_tanakh("ומתחת הלשכות"),
    ".)",
]
_EZEKIEL_IMG = "../jobn/img/Aleppo-Ezekiel-reference.png"
_EZEKIEL_FIGURE = boj_html.div(
    [
        boj_html.anchor_h(
            boj_html.img(
                {
                    "src": _EZEKIEL_IMG,
                    "alt": "Aleppo Codex, Ezekiel 42:9: the he is visible at the end of"
                    " the first written word; the pataḥ floats in the gap before the next.",
                    "width": "988",
                    "height": "192",
                    "style": "max-width:100%;height:auto",
                }
            ),
            _EZEKIEL_IMG,
        ),
        boj_html.para(
            [
                "μA, Ezekiel 42:9, page 186r. The unattached פתח is visible between ",
                author.span_unpointed_tanakh("ומתחתה"),
                " and ",
                author.span_unpointed_tanakh("לשכות"),
                ". ",
                boj_html.anchor_h(
                    "View in Masoretica",
                    "https://www.masoretica.org/?book=Ezekiel&chapter=42"
                    "&manuscript=aleppo&verse=9",
                ),
                "; select the image for full size.",
            ],
        ),
    ],
    {
        "class": "center",
        "role": "figure",
        "aria-label": "Ezekiel manuscript comparison",
    },
)
_SAMUEL_IMG = "../jobn/img/Aleppo-2Samuel-c5v2.png"
_SAMUEL_COMPARISON = [
    "In $2Samuel_5_2, the corresponding word-pairs are the כתיב of ",
    author.span_unpointed_tanakh("הייתה מוציא"),
    " and the קרי of ",
    author.span_unpointed_tanakh("היית המוציא"),
    ". Here, as in Job, the פתח belongs to the final ה of the first written word.",
    " It is not orphaned between the two words as it is in Ezekiel.",
]
_SAMUEL_FIGURE = boj_html.div(
    [
        boj_html.anchor_h(
            boj_html.img(
                {
                    "src": _SAMUEL_IMG,
                    "alt": "Aleppo Codex, 2 Samuel 5:2: the pataḥ belongs to the final"
                    " he of the first written word, not to the gap between the words.",
                    "width": "858",
                    "height": "208",
                    "style": "max-width:100%;height:auto",
                }
            ),
            _SAMUEL_IMG,
        ),
        boj_html.para(
            [
                "μA, 2 Samuel 5:2, page 58r. The פתח belongs to the final ה of ",
                author.span_unpointed_tanakh("הייתה"),
                ". ",
                boj_html.anchor_h(
                    "View in Masoretica",
                    "https://www.masoretica.org/?book=2+Samuel&chapter=5"
                    "&manuscript=aleppo&verse=2",
                ),
                "; select the image for full size.",
            ]
        ),
    ],
    {
        "class": "center",
        "role": "figure",
        "aria-label": "2 Samuel manuscript comparison",
    },
)
_BHQ_COMMENT_3812_B = [
    "$BHS does not catch this quirk in μL: it reflects the consensus rather than μL.",
    " $BHQ half-fixes the error in $BHS:",
    " it updates its marginal קרי note to reflect μL rather than the consensus,",
    " but it does not correspondingly update its bottom-of-page critical apparatus note.",
    " This is similar to what happened with $link_26_14.",
]
RECORD_3812_YD3F_HJXR = {
    "qr-cv": "38:12",
    "qr-word-id": "YD3F_HJXR",
    "qr-lc-proposed": "יִדַּ֖עְתָּה הַשַּׁ֣חַר",
    "qr-what-is-weird": "ה copied not moved in קרי",
    "qr-consensus": "יִדַּ֖עְתָּ הַשַּׁ֣חַר",
    "qr-consensus-ketiv": "ידעתה שחר",
    "qr-generic-comment": [
        author.para(_GENCOM_1),
        author.para(_GENCOM_2),
    ],
    "qr-footnotes": [
        boj_html.heading_level_2(
            "φ1 — Attachment of the פתח in the parallel passages",
            {"id": "patah-comparison"},
        ),
        author.para(_EZEKIEL_COMPARISON),
        _EZEKIEL_FIGURE,
        author.para(_SAMUEL_COMPARISON),
        _SAMUEL_FIGURE,
        boj_html.para(
            boj_html.anchor_h("Return to the discussion", "#patah-comparison-callout")
        ),
    ],
    "qr-highlight-lc-proposed": 5,
    "qr-lc-loc": {"page": "408A", "column": 1, "line": -11},
    "qr-ac-loc": {"page": "280r", "column": 2, "line": 7, "word": 3},
    "qr-bhq-comment": [author.para(_BHQ_COMMENT_3812_B)],
    "qr-noted-by": "nWLC",
}

RECORD_3817 = {
    "qr-cv": "38:17",
    "qr-lc-proposed": "צַלְמָּ֣וֶת",
    "qr-what-is-weird": "מ has דגש",
    "qr-consensus": "צַלְמָ֣וֶת",
    "qr-highlight": 3,
    "qr-lc-loc": {"page": "408A", "column": 1, "line": -5},
    "qr-ac-loc": {"page": "280r", "column": 2, "line": 12, "word": 6},
    "qr-noted-by": "nBHQ",
    "qr-uxlc-needs-fix": True,
}

RECORD_3820 = {
    "qr-cv": "38:20",
    "qr-lc-proposed": "תָ֝בִין",
    "qr-what-is-weird": "רביע of רביע מוגרש is absent",
    "qr-consensus": "תָ֝בִ֗ין",
    "qr-generic-comment": [
        "The only mark above the ב is a רפה.",
    ],
    "qr-highlight": 2,
    "qr-lc-loc": {"page": "408A", "column": 1, "line": 24},
    "qr-ac-loc": {"page": "280r", "column": 2, "line": 16, "word": 4},
    "qr-noted-by": "nDM",
}

RECORD_3827 = {
    "qr-cv": "38:27",
    "qr-lc-proposed": "שֹׁ֖אָה",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "שֹׁ֭אָה",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "408A", "column": 2, "line": 6},
    "qr-ac-loc": {"page": "280r", "column": 2, "line": 24, "word": 5},
    "qr-noted-by": "tBHQ-zdexiWLC",
}

RECORD_3829 = {
    "qr-noted-by": "nDM",
    "qr-cv": "38:29",
    "qr-consensus": "שָׁ֝מַ֗יִם",
    "qr-lc-proposed": "שָׁ֝מַיִם",
    "qr-what-is-weird": "רביע of רביע מוגרש is absent",
    "qr-highlight": 2,
    "qr-bhq-comment": [
        "Aside: $BHQ not only has a רביע (against μL)",
        " but also has a printing problem:",
        " the גרש מוקדם overlaps the $shin dot almost completely.",
    ],
    "qr-lc-loc": {"page": "408A", "column": 2, "line": 9},
    "qr-ac-loc": {"page": "280r", "column": 2, "line": 27, "word": 6},
}
