from author_boj_util import (
    author,
    cos_urls,
)
from author_boj_util.job_common import correctly_ignores
from author_boj_util.all_verses_but_this import (
    ptx_is_not_xtf,
    leg_missing_before_g3yh_rby3,
    no_dag_after_mah,
)

RECORD_3405 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "34:5",
    "qr-consensus": "כִּֽי־אָמַ֣ר",
    "qr-lc-proposed": "כִּֽי־אָ֭מַר",
    "qr-what-is-weird": "דחי not מונח",
    "qr-highlight-consensus": 5,
    "qr-highlight-lc-proposed": 4,
    "qr-generic-comment": "See $link_6_17.",
    "qr-lc-loc": {"page": "406B", "column": 2, "line": 8},
    "qr-ac-loc": {"page": "279r", "column": 1, "line": 5, "word": 1},
}

_COMMENT_PARA1 = [
    "Note that consensus has a rare and hard-to-understand",
    " phenomenon called “secondary מרכא” by Breuer."
    #
    " It may seem rather extraordinary to have two מרכא marks on the same word,",
    " but this is actually expected (or at least “allowed”).",
]
_FOI_H2 = "foi-sec-merk.html#intro-poetic/(mer)/(mer),(mer)"
_FOI_H1 = "https://bdenckla.github.io/MAM-basics/MAM-with-doc/foi/"
_FOI_ANC = author.anc_h("here", f"{_FOI_H1}{_FOI_H2}")
_COMMENT_PARA2 = [
    "This is one of about a dozen analogous cases listed",
    [" ", _FOI_ANC, "."],
]
_COS_ENG_ANC = author.anc_h("translation", cos_urls.cos_translation_url())
_COS_HEB_ANC = author.anc_h("original", cos_urls.cos_original_url())
_COMMENT_PARA3 = [
    "See Breuer CoS sections 9.23, 9.24, and 11.20.",
    " (CoS = The Cantillation of Scripture.)",
    [" (Note that an English ", _COS_ENG_ANC, " of CoS is now available,"],
    " a great boon to students of cantillation who cannot easily read",
    [" the ", _COS_HEB_ANC, " in its modern Hebrew.)"],
]
RECORD_3410 = {
    "qr-cv": "34:10",
    "qr-lc-proposed": "אַֽנֲשֵׁ֥י",
    "qr-what-is-weird": "געיה not מרכא (on א)",
    "qr-consensus": "אַ֥נֲשֵׁ֥י",
    "qr-generic-comment": [
        author.para(_COMMENT_PARA1),
        author.para(_COMMENT_PARA2),
        author.para(_COMMENT_PARA3),
        "In μY, the mark in question is absent: the א just has פתח.",
    ],
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "406B", "column": 2, "line": 14},
    "qr-ac-loc": {"page": "279r", "column": 1, "line": 10, "word": 5},
    "qr-noted-by": "tBHQ-zmiscWLC",
}

RECORD_3419_NKR0 = {
    "qr-cv": "34:19",
    "qr-word-id": "NKR0",
    "qr-lc-proposed": "נִּכַּר־",
    "qr-what-is-weird": "נ has דגש",
    "qr-consensus": "נִכַּר־",
    "qr-generic-comment": [
        "The possible דגש is faint.",
        " The adjacent דגש (on כ) and other nearby marks are quite clear,",
        " casting suspicion on the legitimacy of this דגש.",
    ],
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "406B", "column": 2, "line": -2},
    "qr-ac-loc": {"page": "279r", "column": 1, "line": 22, "word": 7},
    "qr-bhq-comment": correctly_ignores("דגש", "34:19"),
    "qr-noted-by": "nBHL-nDM",
}

RECORD_3419_JV3 = {
    "qr-cv": "34:19",
    "qr-word-id": "JV3",
    "qr-lc-proposed": "שׁ֖וֹעַ",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "שׁ֭וֹעַ",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "406B", "column": 2, "line": 26},
    "qr-ac-loc": {"page": "279r", "column": 1, "line": 22, "word": 8},
    "qr-noted-by": "tBHQ-zdexiWLC",
}

_COMMENT_PARA1_3422 = [
    "In μY, the mark we would charitably interpret as דחי",
    " appears more or less centered on the ח",
    " and touches (collides with) an encroaching ל ascender.",
    " Possibly this ascender prevented the דחי",
    " from assuming its expected prepositive position.",
    " And possibly the preceding final נ contributed to the crowding",
    " that forced the דחי forward.",
    " And/or possibly the prepositive position of דחי,",
    " though viewed as a goal by the $naqdan of μY,",
    " was not such a high priority as we would view it as today.",
]
RECORD_3422 = {
    "qr-cv": "34:22",
    "qr-lc-proposed": "חֹ֖שֶׁךְ",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "חֹ֭שֶׁךְ",
    "qr-generic-comment": _COMMENT_PARA1_3422,
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "407A", "column": 1, "line": 3},
    "qr-ac-loc": {"page": "279r", "column": 1, "line": 26, "word": 6},
    "qr-noted-by": "tBHQ-zdexiWLC",
}

_COMMENT_PARA2_3433_HM3M5 = [
    "In this case, μY agrees with μL against μA:",
    " the פתח in μY is a full פתח, not a חטף פתח.",
    " As for the two other similar cases,",
    " note that μY also agrees with μL against μA in $link_27_9",
    " (to the extent that the μY image permits such a judgement)",
    " but μY agrees with μA against μL in $link_9_35.",
]
_COMMENT_PARA3_3433_HM3M5 = [
    "It is perhaps significant that the cases here and in $link_27_9,",
    " the cases of likely μY/μL agreement,",
    " concern an initial ה whereas $link_9_35 concerns an initial א.",
    " Although for many purposes all four gutturals behave the same,",
    " this may be one of those cases where this is not true.",
]
RECORD_3433_HM3M5 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "34:33",
    "qr-word-id": "HM3M5",
    "qr-consensus": "הֲֽמֵעִמְּךָ֬",
    "qr-lc-proposed": "הַֽמֵעִמְּךָ֬",
    "qr-what-is-weird": "פתח on ה is not חטף",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "407A", "column": 1, "line": 16},
    "qr-ac-loc": {"page": "279r", "column": 2, "line": 11, "word": 6},
    "qr-generic-comment": [
        author.para(ptx_is_not_xtf("34:33")),
        author.para(_COMMENT_PARA2_3433_HM3M5),
        author.para(_COMMENT_PARA3_3433_HM3M5),
    ],
}

RECORD_3433_YJLMNH_1_of_2_FTW = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "34:33",
    "qr-word-id": "YJLMNH_1_of_2_FTW",
    "qr-n_of_m_for_this_word": (1, 2),
    "qr-consensus": "יְשַׁלְּמֶ֨נָּה׀",
    "qr-lc-proposed": "יְשַׁלְמֶ֨נָּה׀",
    "qr-what-is-weird": "ל lacks דגש",
    "qr-highlight": 3,
    "qr-lc-loc": {"page": "407A", "column": 1, "line": 16},
    "qr-ac-loc": {"page": "279r", "column": 2, "line": 11, "word": 7},
}

RECORD_3433_YJLMNH_2_of_2_FTW = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "34:33",
    "qr-word-id": "YJLMNH_2_of_2_FTW",
    "qr-n_of_m_for_this_word": (2, 2),
    "qr-consensus": "יְשַׁלְּמֶ֨נָּה׀",
    "qr-lc-proposed": "יְשַׁלְּמֶ֨נָּה",
    "qr-what-is-weird": "לגרמיה is absent",
    "qr-highlight": 7,
    "qr-lc-loc": {"page": "407A", "column": 1, "line": 18},
    "qr-ac-loc": {"page": "279r", "column": 2, "line": 11, "word": 7},
    "qr-generic-comment": [
        *leg_missing_before_g3yh_rby3("34:33"),
        " In this case here in $plain_34_33, there is an additional mark after the possible erasure.",
        " This mark is hard to interpret.",
    ],
}

RECORD_3433_VMH0YD3F = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "34:33",
    "qr-word-id": "VMH0YD3F",
    "qr-consensus": "וּֽמַה־יָּדַ֥עְתָּ",
    "qr-lc-proposed": "וּֽמַה־יָדַ֥עְתָּ",
    "qr-what-is-weird": "$yod lacks דגש",
    "qr-highlight": 5,
    "qr-lc-loc": {"page": "407A", "column": 1, "line": 18, "line2": 19},
    "qr-ac-loc": {"page": "279r", "column": 2, "line": 13, "word": 1},
    "qr-generic-comment": no_dag_after_mah("34:33"),
}

RECORD_3437 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "34:37",
    "qr-consensus": "יִשְׂפּ֑וֹק",
    "qr-lc-proposed": "יִסְפּ֑וֹק",
    "qr-what-is-weird": "ס not ש",
    # Koren and BHL agree with μL, i.e. they have ס here.
    # JC and Feldheim agree with μA, i.e. they have ש here.
    "qr-highlight": 2,
    "qr-lc-loc": {"page": "407A", "column": 1, "line": 22},
    "qr-ac-loc": {"page": "279r", "column": 2, "line": 18, "word": 2},
    "qr-generic-comment": [
        "Although my focus is pointing rather than spelling,",
        " I am interested in a spelling difference like this,",
        " since it is not just a מלא/חסר difference.",
    ],
}
