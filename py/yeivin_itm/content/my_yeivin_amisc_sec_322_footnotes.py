import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub
import py_html.legacy_html as aht_html

_TEG = "the expected $gaya"
_TGEMOD = "the $gaya expected mainly on disjunctives"
_SLIGHTLY_AFR1_DISJ_SURPRISE_PERCENT = "19%"
_SLIGHTLY_AFR1_DSG_SURPRISE_COUNT = "20"
_SLIGHTLY_AFR1_DSG_ALL_COUNT = "106"
_SLIGHTLY_AFR4_DISJ_SURPRISE_PERCENT = "60%"
_SLIGHTLY_AFR4_DSG_SURPRISE_COUNT = "63"
_SLIGHTLY_AFR4_DSG_ALL_COUNT = "105"
_SLIGHTLY_FR_DISJ_SURPRISE_PERCENT = "6%"
_SLIGHTLY_FR_DSG_SURPRISE_COUNT = "130"
_SLIGHTLY_FR_DSG_ALL_COUNT = "2174"
_SLIGHTLY_GAYA_RATE_REGARDLESS_OF_ACCENT_FOR_FR = "63%"
_SLIGHTLY_GAYA_RATE_REGARDLESS_OF_ACCENT_FOR_AFR1 = "65%"
_SLIGHTLY_GAYA_RATE_REGARDLESS_OF_ACCENT_FOR_AFR4 = "32%"

_HUFT_SLIGHTLY_PARA_MY_RESEARCH_DISAGREES = [
    "My research disagrees with this claim that, "
    "compared to FR disjunctives, "
    "AFR disjunctives show only slightly less tendency to use the expected $gaya",
    ". Of course it is hard to quantitatively define what “slightly” means, "
    "but for any reasonable definition, my research disagrees with this claim. "
    "To be fair to $itm, we should exclude ",
    sub.afr2(),
    " and ",
    sub.afr3(),
    " "
    "from the broader claim about AFR words in general. "
    "We should exclude them for the following reasons:",
]
_HUFT_SLIGHTLY_UL_WARNINGS_ITEM_1 = [
    "For pattern ",
    sub.afr2(),
    ", $itm warns that the number of exceptions is “much greater” than among FR words.",
]
_HUFT_SLIGHTLY_UL_WARNINGS_ITEM_2 = [
    "For pattern ",
    sub.afr3(),
    ", $itm gives the even stronger warning that $gaya"
    " is “generally not marked,” even underlining that phrase.",
]


def _about_p_n_out_of_m(patt, perc, n_cnt, m_cnt):
    return [
        f"I find that about {perc} of ",
        patt,
        " disjunctives " f"({n_cnt} out of {m_cnt}) lack ",
        _TEG,
    ]


_HUFT_SLIGHTLY_PARA_IN_LIGHT_OF_THESE_WARNINGS = [
    "In light of these warnings, it is odd that $itm makes this broad claim about AFR words.",
    " We shall give $itm the benefit of the doubt by assuming that ",
    "it meant to make a less-broad claim that included only ",
    sub.afr1(),
    " and ",
    sub.afr4(),
    ".",
]
_HUFT_SLIGHTLY_PARA_WHILE_I_FIND = [
    "While ",
    _about_p_n_out_of_m(
        "FR",
        _SLIGHTLY_FR_DISJ_SURPRISE_PERCENT,
        _SLIGHTLY_FR_DSG_SURPRISE_COUNT,
        _SLIGHTLY_FR_DSG_ALL_COUNT,
    ),
    ", I find the following for ",
    sub.afr1(),
    " and ",
    sub.afr4(),
    ":",
]
_HUFT_SLIGHTLY_UL_AFR1AFR4_ITEM_1 = [
    _about_p_n_out_of_m(
        sub.afr1(),
        _SLIGHTLY_AFR1_DISJ_SURPRISE_PERCENT,
        _SLIGHTLY_AFR1_DSG_SURPRISE_COUNT,
        _SLIGHTLY_AFR1_DSG_ALL_COUNT,
    ),
    ". Although this shows that ",
    sub.afr1(),
    " shares FR1’s tendency to use ",
    _TEG,
    ", it shows that ",
    sub.afr1(),
    " has more than slightly less of this tendency.",
]
_HUFT_SLIGHTLY_UL_AFR1AFR4_ITEM_2 = [
    _about_p_n_out_of_m(
        sub.afr4(),
        _SLIGHTLY_AFR4_DISJ_SURPRISE_PERCENT,
        _SLIGHTLY_AFR4_DSG_SURPRISE_COUNT,
        _SLIGHTLY_AFR4_DSG_ALL_COUNT,
    ),
    ". This is just plain inconsistent with the claim made by $itm.",
    " This is a disagreement in kind rather than degree. ",
    "Since I find that more than half of the disjunctives lack ",
    _TEG,
    ", I could say that ",
    sub.afr4(),
    " has a mild tendency to ",
    aht_html.emphasis("not"),
    " use ",
    _TEG,
    " on disjunctives!",
]
_HUFT_SLIGHTLY_PARA_FURTHER_RESEARCH = [
    "I need to do further research to understand these discrepancies between "
    "my results and the claims in $itm. In a long footnote in ",
    hlp.rtn(320),
    " I include many possible sources of such discrepancies.",
]
_HUFT_SLIGHTLY_FINALLY_I_SHOULD_NOTE = [
    "Finally, I should note that I have assumed that $itm’s claim is about ",
    _TEG,
    " on disjunctives, "
    "but, technically, the claim is not restricted to disjunctives. "
    "The claim is, literally: "
    "“"
    "Words in this category [(AFR)] "
    "show slightly less tendency to[wards] the use of $gaya",
    " "
    "than words with fully regular structure."
    "” If I test an accent-ignoring version of this claim, "
    f"I find that about {_SLIGHTLY_GAYA_RATE_REGARDLESS_OF_ACCENT_FOR_FR} "
    "of FR words have ",
    _TGEMOD,
    f", about the same ({_SLIGHTLY_GAYA_RATE_REGARDLESS_OF_ACCENT_FOR_AFR1}) "
    "is true for AFR1, "
    "and AFR4 is once again wildly different, with only "
    f"about {_SLIGHTLY_GAYA_RATE_REGARDLESS_OF_ACCENT_FOR_AFR4} "
    "of words having that $gaya",
    ". (I decline to go so far as to assess a version of this claim in which "
    "we also ignore where the $gaya",
    " appears, although, technically, the claim is not restricted to the $gaya",
    " on the main part of the syllable that is two before the stress.)",
]
HUGE_FTNT_REC_FOR_SLIGHTLY = {
    "huge-ftnt-rec-path-rel-web-publish-topdir": "yeivin_itm-huge-ftnt-322.html",
    "huge-ftnt-rec-title": "AFR vs. FR tendency to use the expected gaʿya",
    "huge-ftnt-rec-h1-contents": sub.dol([f"AFR vs. FR tendency to use {_TEG}"]),
    "huge-ftnt-rec-main": [
        sub.para(_HUFT_SLIGHTLY_PARA_MY_RESEARCH_DISAGREES),
        sub.unordered_list(
            [
                _HUFT_SLIGHTLY_UL_WARNINGS_ITEM_1,
                _HUFT_SLIGHTLY_UL_WARNINGS_ITEM_2,
            ]
        ),
        sub.para(_HUFT_SLIGHTLY_PARA_IN_LIGHT_OF_THESE_WARNINGS),
        sub.para(_HUFT_SLIGHTLY_PARA_WHILE_I_FIND),
        sub.unordered_list(
            [
                _HUFT_SLIGHTLY_UL_AFR1AFR4_ITEM_1,
                _HUFT_SLIGHTLY_UL_AFR1AFR4_ITEM_2,
            ]
        ),
        sub.para(_HUFT_SLIGHTLY_PARA_FURTHER_RESEARCH),
        sub.para(_HUFT_SLIGHTLY_FINALLY_I_SHOULD_NOTE),
    ],
}
FTNT_FOR_SLIGHTLY = sub.footnote(
    hlp.ftnt_contents_for_pointer_to_huge(HUGE_FTNT_REC_FOR_SLIGHTLY)
)
# The footnote below is pretty long, and thus maybe should be moved to its own "huge" file.
FTNT_ON_AFR1 = sub.footnote(
    [
        "Here, unlike $itm, I explicitly restrict ",
        sub.afr1(),
        " to be like ",
        sub.fr1(),
        " or ",
        sub.fr3(),
        ". This is only implied by $itm by its choice of examples. "
        "This restriction is also supported by my research into the issue. "
        "I find that if we let ",
        sub.afr1(),
        " include words like ",
        sub.fr2(),
        ", we would “explain” only a single $gaya",
        ", that in ",
        hlp.hboloc("אֶֽל־נְהַר־כְּבָר֙", "@Ez 3:15"),
        ". What’s more, I find that $gaya",
        " to be an outlier: if we let ",
        sub.afr1(),
        " include words like ",
        sub.fr2(),
        ", that would add 16 disjunctively-accented ",
        sub.afr1(),
        " words without such a $gaya",
        ", including ",
        hlp.hboloc("אֶל־נְהַר־כְּבָ֑ר", "@Ez 43:3"),
        sub.thspc(),
        " a chanted word differing only by accent from that one “poster child.” "
        "Although $itm includes ",
        sub.afr3(),
        " in the “almost fully regular” patterns, and $gaya",
        " is rarely marked on ",
        sub.afr3(),
        " words, I see no reason to “pollute” ",
        sub.afr1(),
        " with words whose structure is like that of ",
        sub.fr2(),
        ".",
    ]
)
FTNT_JOS_22_6 = sub.footnote(
    [
        ["In $itm, this example, ", hlp.hbo("וַֽיְבָרֲכֵ֖ם"), sub.thspc()],
        [" is shown with a $simshewa on $resh."],
        [" I.e., this example is shown as ", hlp.hbo("וַֽיְבָרְכֵ֖ם"), sub.thspp()],
        [" This conforms neither to the definition of ", sub.afr4()],
        [" nor to the contents of $ms_aleppo."],
    ]
)

IS_24_19 = "הִֽתְרֹעֲעָ֖ה"
FTNT_IS_24_19 = sub.footnote(
    [
        "I added the example ",
        hlp.hbo(IS_24_19),
        sub.thspp(),
        " It is not present in $itm."
        " I added it so that case of two identical gutturals is represented.",
    ]
)
