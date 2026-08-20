from boj_render import boj_html
from author_boj_util import author
from author_boj_util.common_titles_etc import d5_anchor

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
    "qr-highlight-lc-proposed": 5,
    "qr-lc-loc": {"page": "408A", "column": 1, "line": -11},
    "qr-ac-loc": {"page": "280r", "column": 2, "line": 7, "word": 3},
    "qr-bhq-comment": [author.para(_BHQ_COMMENT_3812_B)],
    "qr-noted-by": "nWLC",
}
