import py_html.legacy_html as aht_html
import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp
import yeivin_itm.content.my_yeivin_amisc_sec_322_footnotes as ftnts

_PARA_WORDS_WITH_PATTERNS_SIMILAR_TO_THOSE = sub.para(
    [
        ["Words with patterns similar to those described in ", hlp.rtn(319), ","],
        " but showing slight differences in structure,"
        " are still considered to have regular structure,"
        " though their structure is not fully regular."
        " We refer to such words’ structure as “almost fully regular” (AFR)."
        " Words in this category",
        " show slightly less tendency to use $gaya than words with fully regular ",
        hlp.ftntjoin("structure.", ftnts.FTNT_FOR_SLIGHTLY),
        " The following four patterns are included in this category:",
    ]
)
_CONT_FTNT_BUF_NO_VS = [
    ["We now see that in words of fully regular structure, "],
    ["the buffer syllable must not start with a $vocshewa."],
]
_FTNT_BUF_NO_VS = sub.footnote(_CONT_FTNT_BUF_NO_VS)
_AFR1_PARA_AFR1_COLON_WORDS_OF_THIS_PATTERN = sub.para(
    [
        sub.afr1(),
        ": Words of this pattern would conform to ",
        sub.fr1(),
        " or ",
        sub.fr3(),
        " if their buffer syllable did not start with a $vocshewa",
        hlp.ftntjoin2(".", ftnts.FTNT_ON_AFR1, _FTNT_BUF_NO_VS),
        " E.g.:",
    ]
)
_AFR1_TABLE_OF_EXAMPLES = hlp.table_std_rtl(
    [
        [
            *hlp.lns(
                "@Ex 16:23",
                "אֲשֶֽׁר־תְּבַשְּׁלוּ֙",
                hlp.sy3("אֲשֶֽׁר־-תְּבַ_-שְּׁלוּ֙"),
            ),
            aht_html.bdi(["≈", sub.fr1()]),
        ],
        [
            *hlp.lns("@1C 2:3", "הַֽכְּנַעֲנִ֑ית", hlp.sy3("הַֽ_-כְּנַ-עֲנִ֑ית")),
            aht_html.bdi(["≈", sub.fr3()]),
        ],
    ]
)
_CONT_FTNT_BUF_SHORT = [
    ["We now see that in words of fully regular structure, "],
    ["the buffer syllable must have a short vowel."],
]
_FTNT_BUF_SHORT = sub.footnote(_CONT_FTNT_BUF_SHORT)
_AFR2_PARA_AFR2_COLON_WORDS_OF_THIS_PATTERN = sub.para(
    [
        [sub.afr2(), ": Words of this pattern would conform to ", sub.fr3()],
        [" if their buffer syllable did not have a long vowel,"],
        [" such as ", sub.qamets_g()],
        # XXX do research and add footnote here about gadol vs xatuf (qatan)
        [hlp.ftntjoin(".", _FTNT_BUF_SHORT)],
        [" Examples of pattern ", sub.afr2(), " include the following:"],
    ]
)
_FK_8_42_AND_EE_4_7 = hlp.make_dloc("@1K 8:42", "@Ez 4:7")
_JOS_10_36_AE = hlp.make_aeloc("@Jos 10:36")
_FS_17_36_AE = hlp.make_aeloc("@1S 17:36")
_AFR2_TABLE_OF_EXAMPLES = hlp.table_std_rtl(
    [
        [
            sub.qamets(),
            *hlp.lns(
                _JOS_10_36_AE, "וַיִּֽלָּחֲמ֖וּ", hlp.sy5pe("וַ_-יִּֽ_-לָּ-חֲמ֖וּ")
            ),
        ],
        [
            sub.qamets(),
            *hlp.lns("@2K 14:10", "וּֽנְשָׂאֲךָ֖", hlp.sy5pspe("וּֽנְ-שָׂ-אֲךָ֖")),
        ],
        [
            sub.qamets(),
            *hlp.lns(
                "@2S 22:8", "וַיִּֽתְגָּעֲשׁ֖וּ", hlp.sy5pe("וַ_-יִּֽתְ-גָּ-עֲשׁ֖וּ")
            ),
        ],
        [
            sub.qamets(),
            *hlp.lns(_FS_17_36_AE, "אֶֽת־הָאֲרִ֛י", hlp.sy5pspe("אֶֽת־-הָ-אֲרִ֛י")),
        ],
        [
            sub.tsere(),
            *hlp.lns("@Gen 32:27", "אֲשַֽׁלֵּחֲךָ֔", hlp.sy5pspe("אֲשַֽׁ_-לֵּ-חֲךָ֔")),
        ],
        [
            sub.xolem(),
            *hlp.lns(
                _FK_8_42_AND_EE_4_7, "וּֽזְרֹעֲךָ֖", hlp.sy5pspe("וּֽזְ-רֹ-עֲךָ֖")
            ),
        ],
        [
            sub.xolem(),
            *hlp.lns("@Rut 2:20", "מִֽגֹּאֲלֵ֖נוּ", hlp.sy5ps("מִֽ_-גֹּ-אֲלֵ֖-נוּ")),
        ],
        [
            sub.xolem(),
            *hlp.lns("@Lev 23:44", "אֶֽת־מֹעֲדֵ֖י", hlp.sy5pspe("אֶֽת־-מֹ-עֲדֵ֖י")),
        ],
    ]
)
_CONT_AFR2_PARA_2 = [
    ["Words of pattern ", sub.afr2(), " like ", sub.hbo_pat_hapoalim()],
    [" (as ", hlp.hbo("הַכֹּהֲנִים"), ", ", hlp.hbo("הַשֹּׁעֲרִים"), ", etc.)"],
    [" usually do not have $gaya"],
    [" and in general"],
    [" the number of exceptions to the rule among ", sub.afr2(), " words"],
    [" is much greater than among words with fully regular structure."],
]
_CONT_AFR3_PARA_1 = [sub.afr3(), ": Words of this pattern have:"]
_CONT_AFR3_UL_LI_1 = [
    ["Like ", sub.afr2(), ", a buffer syllable that is open and long-vowelled."],
]
_AND_THEREFORE = "and therefore its letter is non-guttural"
_VOC_IS_A_SIM = f", a $vocshewa that is a $simshewa ({_AND_THEREFORE})."
_CONT_AFR3_UL_LI_2 = ["Unlike ", sub.afr2(), _VOC_IS_A_SIM]
_CONT_AFR3_PARA_2 = [
    ["A prototype for this pattern is ", sub.hbo_pat_mitbarekhim(), "."],
    [" In words of this pattern, $gaya"],
    [" is ", hlp.emphasis("generally not marked"), "."],
    [" There are, however, a few exceptions. E.g.:"],
]
_SS_5_1_AND = hlp.make_dloc("@2S 5:1", "@1C 11:1")
_AFR3_TABLE_OF_EXCEPTIONS_WHERE_GAYA_IS_INDEED_MARKED = hlp.table_std_rtl(
    [
        [*hlp.lns(hlp.make_aeloc("@Dt 30:14"), "בִּֽלְבָבְךָ֖", "בִּֽלְ-בָ-בְךָ֖")],
        # XXX turn the comment below into a footnote?
        # Actually Dt 30:14 is וּבִֽלְבָבְךָ֖ so better example locales for בִּֽלְבָבְךָ֖ would have been
        # one of these four: 1C 17:2, 1S 9:19, 2S 7:3, or Ezek 3:10.
        # MAM lacks gaʿya on D9:4 בִּלְבָבְךָ֗; see trope#376 (private tracker).
        # (D9:4 בִּלְבָבְךָ֗ is one of the "and elsewhere" cases.)
        [*hlp.lns(hlp.make_aeloc("@Lev 19:5"), "לִֽרְצֹנְכֶ֖ם", "לִֽרְ-צֹ-נְכֶ֖ם")],
        # XXX turn the comment below into a footnote?
        # "Elsewhere" includes these three: Lev 22:19, Lev 22:29, & Lev 23:11.
        # Actually as far as I could tell, elsewhere is limited to those three.
        [*hlp.lns(_SS_5_1_AND, "וּֽבְשָׂרְךָ֖", "וּֽבְ-שָׂ-רְךָ֖")],
    ]
)
_AFR4_PARA_AFR4_COLON_WORDS_OF_PATTERN_HAVE = sub.para(
    [sub.afr4(), ": Words of this pattern have:"]
)
_SS_STARTS = hlp.paren(
    "The main part of the stress syllable starts with the second letter of this pair."
)
_AFR4_UL_NESTED = sub.unordered_list(
    [
        ["On a letter that is the first of an identical pair. ", _SS_STARTS],
        ["A $xatef on a non-guttural letter."],
    ]
)
_AFR4_UL = sub.unordered_list(
    [
        ["A buffer syllable that is open, with either a short or long vowel."],
        ["A $vocshewa that is one of the following:", _AFR4_UL_NESTED],
    ]
)
_AFR4_PARA_IF_THE_BUFFER_SYLLABLE_HAS_A_SHORT_VOWEL = sub.para(
    [
        "If the buffer syllable has a short vowel, $gaya",
        " is marked as in words with fully regular structure. E.g.:",
    ]
)
_AFR4_TABLE_OF_EXAMPLES_OF_SHORT_BUFFER = hlp.table_std_rtl(
    [
        [*hlp.lns("@Jud 16:24", "וַֽיְהַלְל֖וּ", "וַֽיְ-הַ-לְל֖וּ")],
        [*hlp.lns("@1K 8:30", "יִֽתְפַּלְל֖וּ", "יִֽתְ-פַּ-לְל֖וּ")],
        # XXX turn the comment below into a footnote?
        # The following regex turns up 20 examples (the 2 above plus 18 others):
        # [א-ת][\u05c1\u05c2]?.?\u05bd[א-ת][\u05c1\u05c2]?\u05b0[א-ת][\u05c1\u05c2]?\u05bc?\u05b7([א-ת][\u05c1\u05c2]?)\u05b0\1
        # Among these 18 others are the following two (in Judges) that are
        # interesting because the doubled letter is ק rather than ל:
        # הַֽמְלַקְקִ֤ים הַֽמְלַקְקִים֙
        #
    ]
)
_AFR4_PARA_THE_DEFINITION_OF_FR3 = sub.para_paren(
    [
        ["Technically, the definition of ", sub.fr3()],
        [" overlaps with the definition of ", sub.afr4(), "."],
        [" But, in practice, no words exist that satisfy both definitions,"],
        [" so this is not a problem."],
    ]
)
_AFR4_PARA_IF_THE_BUFFER_SYLLABLE_HAS_A_LONG_VOWEL = sub.para(
    [
        ["If the buffer syllable has a long vowel, the marking of $gaya"],
        [" follows the rules given for ", sub.afr2(), " above. E.g.:"],
    ]
)
_AFR4_TABLE_OF_EXAMPLES_OF_LONG_BUFFER = hlp.table_std_rtl(
    [
        [*hlp.lns("@Zeph 2:1", "הִֽתְקוֹשְׁשׁ֖וּ", hlp.sy4pe("הִֽתְ-קוֹ-שְׁשׁ֖וּ"))],
        [*hlp.lns("@Dt 32:6", "וַֽיְכֹנְנֶֽךָ׃", hlp.sy4("וַֽיְ-כֹ-נְנֶֽ-ךָ׃"))],
        [
            *hlp.lns("@Is 24:19", ftnts.IS_24_19, hlp.sy4pe("הִֽתְ-רֹ-עֲעָ֖ה")),
            ftnts.FTNT_IS_24_19,
        ],
        [
            *hlp.lns("@Jos 22:6", "וַֽיְבָרֲכֵ֖ם", hlp.sy4pe("וַֽיְ-בָ-רֲכֵ֖ם")),
            ftnts.FTNT_JOS_22_6,
        ],
        # MAM וַֽיְבָרְﬞכֵ֖ם (varika-shewa) vs ITM simple shewa
        # See "Big Note" below
    ]
)
_AFR4_PARA_THE_DEFINITION_OF_AFR2_AND_AFR3 = sub.para_paren(
    [
        "The definitions given above for ",
        sub.afr2(),
        " and ",
        sub.afr3(),
        " overlap with the definition of ",
        sub.afr4(),
        ". We can solve this problem by adding that the letter with the",
        " $vocshewa of ",
        sub.afr2(),
        " and ",
        sub.afr3(),
        " cannot be the first of an identical pair.",
    ]
)
_SUMMARY_PARA_THE_FOLLOWING_TABLE_SUMMARIZES_ALL_THIS = sub.para(
    ["The following table summarizes all this."]
)


def _asv(start):  # asv: "and short-vowelled"
    return hlp.line_break(start, "short-vowelled")


def _alv(start):  # asv: "and long-vowelled"
    return hlp.line_break(start, "long-vowelled")


_PREC_BY_VS = sub.dol("but starts with a $vocshewa")
_LIKE_FR1_OR_FR3 = "like ", sub.fr1(), " or ", sub.fr3()
_AFR1_BUF = hlp.line_break(_LIKE_FR1_OR_FR3, _PREC_BY_VS)
_NGUTT = "non-guttural"
_YGUTT = "guttural"
_NOT_FIP = ["not the ", sub.fip()]
_SUMMARY_TABLE = hlp.table_std(
    [
        [sub.fr1(), _asv("closed implicitly"), _NGUTT],
        [sub.fr2(), _asv("closed explicitly"), "any"],
        [sub.fr3(), _asv("open"), _YGUTT],
        [sub.afr1(), _AFR1_BUF, _LIKE_FR1_OR_FR3],
        [sub.afr2(), _alv("open"), hlp.line_break_seq([_YGUTT, _NOT_FIP])],
        [sub.afr3(), _alv("open"), hlp.line_break_seq([_NGUTT, _NOT_FIP])],
        [sub.afr4(), "open", ["the ", sub.fip()]],
    ],
    arg_to_troh=[
        "patt.",
        "buffer syllable is ...",
        hlp.line_break("stress syllable’s", sub.dol("$vocshewa letter is ...")),
    ],
)
_SUMMARY_PARA_IN_THE_TABLE_ABOVE_FIP_STANDS_FOR = sub.para_paren(
    ["Above, “FIP” stands for “", sub.fip_explanation(), ".”"]
)
SEC = [
    _PARA_WORDS_WITH_PATTERNS_SIMILAR_TO_THOSE,
    #
    _AFR1_PARA_AFR1_COLON_WORDS_OF_THIS_PATTERN,
    _AFR1_TABLE_OF_EXAMPLES,
    #
    _AFR2_PARA_AFR2_COLON_WORDS_OF_THIS_PATTERN,
    _AFR2_TABLE_OF_EXAMPLES,
    sub.para(_CONT_AFR2_PARA_2),
    #
    sub.para(_CONT_AFR3_PARA_1),
    sub.unordered_list([_CONT_AFR3_UL_LI_1, _CONT_AFR3_UL_LI_2]),
    sub.para(_CONT_AFR3_PARA_2),
    _AFR3_TABLE_OF_EXCEPTIONS_WHERE_GAYA_IS_INDEED_MARKED,
    #
    _AFR4_PARA_AFR4_COLON_WORDS_OF_PATTERN_HAVE,
    _AFR4_UL,
    _AFR4_PARA_IF_THE_BUFFER_SYLLABLE_HAS_A_SHORT_VOWEL,
    _AFR4_TABLE_OF_EXAMPLES_OF_SHORT_BUFFER,
    _AFR4_PARA_THE_DEFINITION_OF_FR3,
    _AFR4_PARA_IF_THE_BUFFER_SYLLABLE_HAS_A_LONG_VOWEL,
    _AFR4_TABLE_OF_EXAMPLES_OF_LONG_BUFFER,
    _AFR4_PARA_THE_DEFINITION_OF_AFR2_AND_AFR3,
    #
    _SUMMARY_PARA_THE_FOLLOWING_TABLE_SUMMARIZES_ALL_THIS,
    _SUMMARY_TABLE,
    _SUMMARY_PARA_IN_THE_TABLE_ABOVE_FIP_STANDS_FOR,
]
# Big Note
#
# The following regex turns up 7 examples (וַֽיְכֹנְנֶֽךָ׃ above plus 6 others):
# [א-ת][\u05c1\u05c2]?.?\u05bd[א-ת][\u05c1\u05c2]?\u05b0[א-ת][\u05c1\u05c2]?\u05bc?[^\u05b7]([א-ת][\u05c1\u05c2]?)\u05b0\1
# The 6 others are as follows:
#     הַֽמְשֹׁרְרִ֑ים (2 times)
#     וּֽמְשֹׁרְר֖וֹת (allowing initial shuruq to start a closed syllable)
#     Gen 49:23 וַֽיְמָרְרֻ֖הוּ
#     Nu 5:19 and Nu 5:24 הַֽמְאָרְרִ֖ים (both cases mentioned in section 382)
#
# The following regex turns up 11 examples (הִֽתְקוֹשְׁשׁ֖וּ above plus 10 others):
# [א-ת].?\u05bd[א-ת]\u05b0[א-ת]\u05bc?וֹ([א-ת][\u05c1\u05c2]?)\u05b0\1
# The 10 others are as follows:
#     1 וּֽמְעוֹנְנִ֖ים (allowing initial shuruq to start a closed syllable)
#     2 מִֽתְנוֹסְס֖וֹת
#     3 הִֽתְפּוֹרְרָה֙
#     4 הִֽתְמוֹטְטָ֖ה
#     5 וְהִֽתְנוֹדְדָ֖ה
#     6 הִֽתְעוֹרְרִ֗י
#     7 וְהִֽתְבּוֹנְנ֖וּ
#     8 וּֽתְרוֹמְמֶ֑ךָּ (allowing initial shuruq to start a closed syllable)
#     9 וַֽיְכוֹנְנֶֽהָ׃
#    10 וַֽיְכוֹנְנ֑וּנִי
