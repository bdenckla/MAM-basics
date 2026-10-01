import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_DT_33_2 = {
    "norm": "מֵרִבְבֹ֣ת",
    "star-silent": "מֵ*רִבְ*בֹ֣ת",
    "star-vocal": "מֵרִ*בְבֹ֣ת*",
    "loc": "@Dt 33:2",
}
_JER_51_48 = {
    "norm": "הַשּׁוֹדְדִ֖ים",
    "star-silent": "הַ*שּׁוֹדְ*דִ֖ים",
    "star-vocal": "הַשּׁוֹ*דְדִ֖ים*",
    "loc": "@Jer 51:48",
}
_JER_25_12 = {
    "norm": "לְשִֽׁמְמ֥וֹת",
    "star-silent": "לְ*שִֽׁמְ*מ֥וֹת",
    "star-vocal": "לְשִֽׁ*מְמ֥וֹת*",
    "loc": "@Jer 25:12",
}
_IS_59_10 = "נְגַשֲׁשָׁ֤ה", "נְגַ*שֲׁשָׁ֤ה*", "@Is 59:10"
_JER_51_53 = "שֹׁדֲדִ֛ים", "שֹׁ*דֲדִ֛ים*", "@Jer 51:53"
_HBO_JER_25_12 = hlp.hbo(_JER_25_12["norm"])
_HBO_IS_59_10 = hlp.hbo(_IS_59_10[0])
_HBO_JER_51_53 = hlp.hbo(_JER_51_53[0])
_THE_STUDY_REVEALS_RULE = [
    "The study of the pointing of ",
    sub.ms_aleppo(),
    " in this situation, and "
    "comparison of it with other early manuscripts, reveals a somewhat "
    "different rule",
]
_CONTENTS_COMMON_TO_FTNTS_1_AND_3 = [
    "In $itm it is not explicitly stated that the $shewas",
    " in these six exceptions are silent. "
    "I assume they are silent on the authority of Khan "
    "(The Tiberian Pronunciation Tradition of Biblical Hebrew, volume 1, page 353).",
]
_NORM_AND_STAR_FOR_EXC_3_AND_4 = "מְצָאֻֽנְנִי׃", "מְצָ*אֻֽנְ*נִי׃"
_EXC_1_OF_6 = "יְ֝שַׁחֲרֻ֗נְנִי", "יְ֝שַׁ*חֲרֻ֗נְ*נִי", "@Prov 1:28"
_EXC_2_OF_6 = "יִ֭קְרָאֻנְנִי", "יִ֭קְרָ*אֻנְ*נִי", "@Prov 1:28"
_EXC_3_OF_6 = *_NORM_AND_STAR_FOR_EXC_3_AND_4, "@Prov 1:28"
_EXC_4_OF_6 = *_NORM_AND_STAR_FOR_EXC_3_AND_4, "@Prov 8:17"
_EXC_5_OF_6 = "יְֽכַ֫בְּדָ֥נְנִי", "יְֽכַ֫*בְּדָ֥נְ*נִי", "@Ps 50:23"
_EXC_6_OF_6 = "שַׁחֲרֻֽנְנִי׃", "שַׁ*חֲרֻֽנְ*נִי׃", "@Ho 5:15"
_HUFT_THE_SIX_D_RULE_PART_3_ALL_6_INSTANCES = [
    [hlp.some_hi(_EXC_1_OF_6)],
    [hlp.some_hi(_EXC_2_OF_6)],
    [hlp.some_hi(_EXC_3_OF_6)],
    [hlp.some_hi(_EXC_4_OF_6)],
    [hlp.some_hi(_EXC_5_OF_6)],
    [hlp.some_hi(_EXC_6_OF_6)],
]


_HUFT_THE_SIX_PARA_1 = sub.para(["The six exceptions are as follows:"])
_HUFT_THE_SIX_PARA_2 = sub.para(
    [
        hlp.paren(
            [
                "The first of this list, ",
                hlp.hbo(_EXC_1_OF_6[0]),
                sub.thspc(),
                " is the one given as an example in $itm.",
            ]
        ),
        " ",
        hlp.paren(
            [
                "Only 5 of the 6 exceptions are unique since ",
                hlp.hbo(_EXC_3_OF_6[0]),
                " is in two verses.",
            ]
        ),
        " ",
        hlp.paren(
            [
                "Also note that 3 of the 6 exceptions are in the same verse: ",
                hlp.isolated_slocale("@Prov 1:28"),
                "!",
            ]
        ),
    ]
)

_HUFT_D1_RARELY_PARA_1 = sub.para(
    [
        "How did Yeivin determine that Rule D1 is not obeyed in manuscripts "
        "in which $vocshewa is ",
        hlp.emphasis("rarely"),
        " made explicit? "
        "There are two ways I can think of that he might have done this.",
    ]
)
_HUFT_D1_RARELY_LICONT_0 = [
    "One way is by applying a criteria of internal consistency. "
    "What I mean by that is the following.",
    sub.unordered_list(
        [
            [
                "If we assume that the “vocality” of a word’s $shewa"
                " does not vary across verses,"
            ],
            [
                "but we see, in some particular manuscript, that the use of $gaya"
                " in that word does vary across verses,"
            ],
            [
                "then we could say, for that word at least,"
                " that Rule D1 is not obeyed in that manuscript."
                " And, of course, if we see this inconsistent use of $gaya"
                " across many words in that manuscript,"
                " then we could say, for the manuscript as a whole,"
                " that Rule D1 is not obeyed.",
            ],
        ]
    ),
]
_HUFT_D1_RARELY_LICONT_1 = [
    "The other way is by applying a criteria of external consistency. "
    "What I mean by that is the following. "
    "Let’s say we have two manuscripts, ",
    ["a reference one like ", sub.ms_aleppo()],
    [", in which $vocshewa is often made explicit,"],
    " and one under scrutiny, in which that is not the case: ",
    ["usually only $simshewa is used."],
    sub.unordered_list(
        [
            [
                "If we assume that the “vocality” of a word’s $shewa"
                " does not vary across these two manuscripts,",
            ],
            [
                "but we see that the manuscript under scrutiny lacks"
                " $gaya where the reference has $xatef,",
            ],
            [
                "then we could say, for that word at least, "
                "that Rule D1 is not obeyed in the manuscript under scrutiny."
            ],
        ]
    ),
]
_HUFT_D1_OFTEN_PARA_1 = sub.para(
    [
        "How did Yeivin determine that Rule D1 is not obeyed in manuscripts"
        " in which $vocshewa is ",
        hlp.emphasis("often"),
        " made explicit?"
        " To answer that question, we first need to know:"
        " what does it even mean for this rule to be obeyed in such manuscripts?"
        " I ask this second, more basic question because"
        " in my interpretation at least, this rule’s purpose is to resolve"
        " the ambiguity surrounding the “vocality” of $simshewa,"
        " but in many cases these manuscripts have no such ambiguity,"
        " due to their use of $xatef.",
    ]
)
_BODY_OF_FTNT_5_REST_LEVEL_2_LIST_ITEMS = [
    ["It is somewhat strange to say that Rule D1 is not obeyed in such cases."],
    [
        "Rule D1 is not obeyed only if we assume, temporarily, that",
        " $simshewa means $silshewa in such words.",
    ],
    [
        "It is fine to make such assumptions, temporarily, for the purposes of argument, "
        "and indeed that is I think what Yeivin is doing, but he does not make that clear."
    ],
    [
        "Yeivin does an external consistency check on ",
        _HBO_JER_25_12,
        ", using the $xatef of ",
        sub.ms_lenin_20(),
        " to determine that the $simshewa of ",
        _HBO_JER_25_12,
        " is likely vocal. On that basis, ",
        _HBO_JER_25_12,
        " obeys D1!",
    ],
]
_HUFT_D1_OFTEN_REST = [
    sub.para(
        [
            "In words where a $vocshewa sound is already explicitly called for,"
            " i.e. in words where $xatef is used,"
            " it is in some sense “unfair” to expect a $gaya",
            " to redundantly call for a $vocshewa sound."
            " So it is not surprising that, as Yeivin documents here and elsewhere,"
            " we don’t consistently find such redundancy.",
        ]
    ),
    sub.para(
        [
            "The more interesting words are ones in which only $simshewa is used. "
            "In such words, the question becomes: which of the following is true?",
        ]
    ),
    sub.ordered_list(
        [
            [
                "Does $simshewa mean $silshewa in all (or at least most) of these words?",
            ],
            [
                "Or, is $simshewa ambiguous in these words, as it is in"
                " manuscripts that rarely make $vocshewa explicit?",
            ],
        ]
    ),
    sub.para(
        [
            "As Yeivin documents here and elsewhere,"
            " unfortunately the answer is number 2:"
            " although in these manuscripts ",
            sub.xatef(),
            " is often used to unambiguously notate a $vocshewa sound,",
            " $simshewa is still used ambiguously in these manuscripts in"
            " the circumstances under discussion: on the ",
            sub.fip(),
            ".",
        ]
    ),
    sub.para(
        [
            "Let’s return to the basic question of what Yeivin means "
            "when he says that Rule D1 is not obeyed "
            "in manuscripts in which $vocshewa is often made explicit. "
            "What he means, initially at least, is the following:",
        ]
    ),
    sub.ordered_list(
        [
            [
                "“Unfair” or not, for words with ",
                sub.xatef(),
                ", he means that Rule D1 is not obeyed because the redundant",
                " $gaya is sometimes absent. The relevant examples here are ",
                _HBO_IS_59_10,
                " and ",
                _HBO_JER_51_53,
                ".",
                # Above, no need for thin space because of the shape of shin.
            ],
            [
                "For words with $simshewa, he means that Rule D1 is not obeyed because sometimes",
                " $gaya is present. The relevant example here is ",
                _HBO_JER_25_12,
                ".",
                sub.unordered_list(_BODY_OF_FTNT_5_REST_LEVEL_2_LIST_ITEMS),
            ],
        ]
    ),
    sub.para(
        [
            "So Yeivin’s examples merely show that manuscripts like ",
            sub.ms_aleppo(),
            " don’t obey D1 “naively,”"
            " by which I mean that they don’t obey D1"
            " assuming that $simshewa means $silshewa.",
            " But, the real question is whether Rule D1 is obeyed in these words ",
            hlp.emphasis("without"),
            " assuming that $simshewa means $silshewa.",
            " The answer is that Rule D1 is not obeyed in that way either."
            " Yeivin implicitly provides that answer when he goes on to give Rule D2.",
        ]
    ),
]

##########  PUBLIC  ##########

FTNT_1 = sub.footnote(
    [
        "I added the qualification “or the stress”;"
        " this qualification is not present in $itm."
        " I added this qualification on the assumption that the",
        " $shewas in the six exceptions are silent,"
        " making them exceptions to this first part of the rule."
        " ",
        *_CONTENTS_COMMON_TO_FTNTS_1_AND_3,
    ]
)
HUGE_FTNT_REC_FOR_THE_SIX = {
    "huge-ftnt-rec-path-rel-web-publish-topdir": "yeivin_itm-huge-ftnt-385-2.html",
    "huge-ftnt-rec-title": "The six exceptions",
    "huge-ftnt-rec-h1-contents": "The six exceptions",
    "huge-ftnt-rec-main": [
        _HUFT_THE_SIX_PARA_1,
        hlp.table_std_rtl(_HUFT_THE_SIX_D_RULE_PART_3_ALL_6_INSTANCES),
        _HUFT_THE_SIX_PARA_2,
    ],
}
FTNT_FOR_THE_SIX = sub.footnote(
    hlp.ftnt_contents_for_pointer_to_huge(HUGE_FTNT_REC_FOR_THE_SIX)
)
FTNT_3 = sub.footnote(_CONTENTS_COMMON_TO_FTNTS_1_AND_3)
HUGE_FTNT_REC_FOR_D1_RARELY = {
    "huge-ftnt-rec-path-rel-web-publish-topdir": "yeivin_itm-huge-ftnt-385-4.html",
    "huge-ftnt-rec-title": "D1 rarely",
    "huge-ftnt-rec-h1-contents": "D1 rarely",
    "huge-ftnt-rec-main": [
        _HUFT_D1_RARELY_PARA_1,
        sub.unordered_list([_HUFT_D1_RARELY_LICONT_0, _HUFT_D1_RARELY_LICONT_1]),
    ],
}
FTNT_D1_RARELY = sub.footnote(
    hlp.ftnt_contents_for_pointer_to_huge(HUGE_FTNT_REC_FOR_D1_RARELY)
)
HUGE_FTNT_REC_FOR_D1_OFTEN = {
    "huge-ftnt-rec-path-rel-web-publish-topdir": "yeivin_itm-huge-ftnt-385-5.html",
    "huge-ftnt-rec-title": "D1 often",
    "huge-ftnt-rec-h1-contents": "D1 often",
    "huge-ftnt-rec-main": [_HUFT_D1_OFTEN_PARA_1, *_HUFT_D1_OFTEN_REST],
}
FTNT_D1_OFTEN = sub.footnote(
    hlp.ftnt_contents_for_pointer_to_huge(HUGE_FTNT_REC_FOR_D1_OFTEN)
)
FTNT_6 = sub.footnote(
    [
        "Presumably, I could add the qualification “or the stress” as I did in Rule D1, "
        "but it is not clear whether that ever happens, in practice."
    ]
)
#
FTNT_7 = sub.footnote(
    [
        "Although $itm does not state it explicitly, "
        "I assume that the same six exceptions of the Rule D1 apply here in Rule D2 as well.",
    ]
)
#
FTNT_8 = sub.footnote(["I added this sentence and the table below it."])

EXCEPTION_1_OF_6 = _EXC_1_OF_6
THE_STUDY_REVEALS_RULE = _THE_STUDY_REVEALS_RULE
DT_33_2 = _DT_33_2
JER_51_48 = _JER_51_48
JER_25_12 = _JER_25_12
IS_59_10 = _IS_59_10
JER_51_53 = _JER_51_53
