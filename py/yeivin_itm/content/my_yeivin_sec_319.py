import yeivin_itm.substitutions as sub
import py_html.legacy_html as aht_html
import yeivin_itm.helpers as hlp


def _contents_of_ftnt_on_initial_shuruq_wu(in_lhbo):
    return [
        ["Note that here in ", in_lhbo, " and elsewhere, "],
        ["$itm treats an initial "],
        [sub.shureq(), " as if it started a closed ", sub.ssv(), "."],
        [" Also, contrast with phonetic rather than musical $gaya"],
        [" on initial ", sub.shureq()],
        [" in ", hlp.rtn(349), "."],
    ]


def _atc_for_pat(frn, pat):
    contents = "Pattern ", frn, ", prototype ", hlp.hbo(pat[0])
    attr = {"dir": "ltr"}
    return {"atc-contents": contents, "atc-attr": attr}


_VS_ATTACHED_TO_STRESS = hlp.line_break_seq(
    [
        sub.dol("a stress syllable starting with a $vocshewa"),
        hlp.paren(["notated as ", sub.simple_or_xatef()]),
    ]
)
_LNS_EX_1_10 = "@Ex 1:10", "נִֽתְחַכְּמָ֖ה", "נִֽתְ-חַ_-כְּמָ֖ה"
_SYL_SEP_MITQATLIM = hlp.syl_sep(*sub.pat_mitqatlim())
_TABLE_1_DATA = [
    [_SYL_SEP_MITQATLIM[0], "a closed syllable with a short vowel"],
    [_SYL_SEP_MITQATLIM[1], "a “buffer” syllable"],
    [_SYL_SEP_MITQATLIM[2], _VS_ATTACHED_TO_STRESS],
]
_TABLE_1 = hlp.table_std(_TABLE_1_DATA, coldirs=["rtl", "ltr"])
_TABLE_2 = hlp.table_std_rtl([[*hlp.lns(*_LNS_EX_1_10)]])
# _TABLE_3_H = [
#     "patt.",
#     hlp.line_break("buffer syllable is", "short-vowelled and ..."),
#     [sub.vocshewa(), " letter ..."],
# ]
# _BDX = hlp.paren(["by a ", sub.dagesh_xazaq()])
# _TABLE_3_D = [
#     [sub.fr1(), hlp.line_break("closed implicitly", _BDX), sub.NG_EITHER],
#     [sub.fr2(), "closed explicitly", sub.NGE_OR_YGX],
#     [sub.fr3(), "open", sub.YG_XATEF],
# ]
# _TABLE_3 = hlp.table_stdwh(_TABLE_3_H, _TABLE_3_D)
_TABLE_4_FR1_CONTENTS = [
    [[sub.fr1(), " prototype"], *hlp.norm_and_syl_sep(*sub.pat_mitqatlim())],
    ["", *hlp.lns(*_LNS_EX_1_10)],
]
_TABLE_4_FR2_CONTENTS = [
    [[sub.fr2(), " prototype"], *hlp.norm_and_syl_sep(*sub.pat_mitpalpelim())],
    ["", *hlp.lns("@1S 30:5", "הַֽכַּרְמְלִֽי׃", "הַֽ_-כַּרְ-מְלִֽי׃")],
]
_TABLE_4_FR3_CONTENTS = [
    [[sub.fr3(), " prototype"], *hlp.norm_and_syl_sep(*sub.pat_mitpaalim())],
    ["", *hlp.lns("@Gen 37:9", "מִֽשְׁתַּחֲוִ֖ים", "מִֽשְׁ-תַּ-חֲוִ֖ים")],
]
_TABLE_4_FR1 = hlp.table_std_rtl(_TABLE_4_FR1_CONTENTS)
_TABLE_4_FR2 = hlp.table_std_rtl(_TABLE_4_FR2_CONTENTS)
_TABLE_4_FR3 = hlp.table_std_rtl(_TABLE_4_FR3_CONTENTS)
_TABLE_4 = hlp.table_std_rtl(
    [
        *_TABLE_4_FR1_CONTENTS,
        *_TABLE_4_FR2_CONTENTS,
        *_TABLE_4_FR3_CONTENTS,
    ]
)
_JUD_20_32 = "@Jud 20:32", "וּֽנְתַקְּנ֔וּהוּ"
_FTNT_JUD_20_32 = sub.footnote(
    _contents_of_ftnt_on_initial_shuruq_wu(hlp.lhbo(*_JUD_20_32))
)
_TABLE_5 = hlp.table_std_rtl(
    [
        [*hlp.lns("@Dt 31:22", "וַֽיְלַמְּדָ֖הּ", hlp.sy4pe("וַֽיְ-לַ_-מְּדָ֖הּ"))],
        [*hlp.lns("@Ez 4:8", "מִֽצִּדְּךָ֙", hlp.sy4pe("מִֽ_-צִּ_-דְּךָ֙"))],
        [*hlp.lns(*_JUD_20_32, hlp.sy4("וּֽנְ-תַ_-קְּנ֔וּ-הוּ")), _FTNT_JUD_20_32],
        [*hlp.lns("@1S 9:20", "אֶֽת־לִבְּךָ֛", hlp.sy4pe("אֶֽת־-לִ_-בְּךָ֛"))],
    ],
    arg_to_caption=_atc_for_pat(sub.fr1(), sub.pat_mitqatlim()),
)
_LEV_21_17 = "מִֽזַּרְעֲךָ֞"
_FTNT_LEV_21_17 = sub.footnote(
    [
        ["I added the example ", hlp.hbo(_LEV_21_17), sub.thspp()],
        [" It is not present in $itm."],
        [" I added it so that the guttural ", sub.fr2(), " case is represented."],
    ]
)
_FC_28_13 = "@1C 28:13", "וּֽלְכׇל־מְלֶ֖אכֶת"
_FTNT_FC_28_13 = sub.footnote(
    _contents_of_ftnt_on_initial_shuruq_wu(hlp.lhbo(*_FC_28_13))
)
_TABLE_6 = hlp.table_std_rtl(
    [
        [*hlp.lns("@Gen 49:23", "וַֽיִּשְׂטְמֻ֖הוּ", hlp.sy4("וַֽ_-יִּשְׂ-טְמֻ֖-הוּ"))],
        [
            *hlp.lns(
                "@Gen 49:14", "הַֽמִּשְׁפְּתָֽיִם׃", hlp.sy4("הַֽ_-מִּשְׁ-פְּתָֽ-יִם׃")
            )
        ],
        [*hlp.lns("@2S 23:20", "מִֽקַּבְצְאֵ֑ל", hlp.sy4pe("מִֽ_-קַּבְ-צְאֵ֑ל"))],
        [
            *hlp.lns("@Lev 21:17", _LEV_21_17, hlp.sy4pe("מִֽ_-זַּרְ-עֲךָ֞")),
            _FTNT_LEV_21_17,
        ],
        [*hlp.lns(*_FC_28_13, hlp.sy4("וּֽלְ-כׇל־-מְלֶ֖א-כֶת")), _FTNT_FC_28_13],
        [*hlp.lns("@1C 5:10", "עַֽל־כׇּל־פְּנֵ֖י", hlp.sy4pe("עַֽל־-כׇּל־-פְּנֵ֖י"))],
        [
            *hlp.lns(
                "@Lev 18:17", "אֶֽת־בַּת־בְּנָ֞הּ", hlp.sy4pe("אֶֽת־-בַּת־-בְּנָ֞הּ")
            )
        ],
        [
            *hlp.lns(
                "@Ez 10:15", "בִּֽנְהַר־כְּבָֽר׃", hlp.sy4pe("בִּֽנְ-הַר־-כְּבָֽר׃")
            )
        ],
    ],
    arg_to_caption=_atc_for_pat(sub.fr2(), sub.pat_mitpalpelim()),
)
_G_41_3_AND_NEX_12_40 = hlp.make_dloc("@Gen 41:3", "@Neḥ 12:40")
_SK_11_10_AE = hlp.make_aeloc("@2K 11:10")
_TABLE_7 = hlp.table_std_rtl(
    [
        [*hlp.lns("@Jer 23:17", "לִֽמְנַאֲצַ֔י", hlp.sy4pe("לִֽמְ-נַ-אֲצַ֔י"))],
        [
            *hlp.lns(
                _G_41_3_AND_NEX_12_40,
                "וַֽתַּעֲמֹ֛דְנָה",
                hlp.sy4("וַֽ_-תַּ-עֲמֹ֛דְ-נָה"),
            )
        ],
        [*hlp.lns("@Jud 5:22", "מִֽדַּהֲר֖וֹת", hlp.sy4pe("מִֽ_-דַּ-הֲר֖וֹת"))],
        [*hlp.lns("@Is 57:8", "וַֽתַּעֲלִ֗י", hlp.sy4pe("וַֽ_-תַּ-עֲלִ֗י"))],
        [*hlp.lns(_SK_11_10_AE, "אֶֽת־הַחֲנִית֙", hlp.sy4pe("אֶֽת־-הַ-חֲנִית֙"))],
    ],
    arg_to_caption=_atc_for_pat(sub.fr3(), sub.pat_mitpaalim()),
)
_CONT_FTNT_THIS_CATEGORY = [
    "It is unclear whether “this category of $gaya”"
    " refers to the general category of $gaya"
    " on a closed, short-vowelled syllable"
    " or to the specific category of $gaya"
    " on a word of regular structure."
]
_CONT_FTNT_ABOUT_HEADING = [
    ["The heading that precedes this section is"],
    [" ", hlp.dquotes(sub.TITSEC_HEADING_319), "."],
    [" I added the ", hlp.dquotes("short-vowelled"), " qualification;"],
    [" in $itm it is simply "],
    [hlp.dquotes(sub.TITSEC_HEADING_319_ORIG), "."],
    [" But, from context, I feel that the ", hlp.dquotes("short-vowelled")],
    [" qualification is justified and helpful."],
]
_CONT_FTNT_LIBERTIES = [
    "I have taken significant liberties in my adaptation of this section.",
]
_NON_GUTT = [
    [" it is a non-guttural, it can have either notation for"],
    [" $vocshewa,"],
    [" with the $simshewa notation used"],
    [" in the vast majority of cases and the $x_shewa notation used"],
    [" in the remaining tiny minority of cases."],
]
_GUTT = [
    [" it is a guttural, it will of course have only the"],
    [" $x_shewa notation for $vocshewa."],
]
_CONT_FTNT_FR1_LWVS = [  # LWVS: letter with vocal shewa
    [" In an ", sub.fr1(), " word,"],
    [" the letter with the $vocshewa"],
    [" is always a non-guttural,"],
    [" because it has a $dagesh_xazaq."],
    [" Since"],
    *_NON_GUTT,
]
_CONT_FTNT_FR2_CLOSED = [[" I.e. closed by a letter with a $silshewa or a $maqqef."]]
_CONT_FTNT_FR2_LWVS = [
    [" In an ", sub.fr2(), " word,"],
    [" the letter with the $vocshewa"],
    [" can be any letter, guttural or non-guttural."],
    [" If"],
    *_NON_GUTT,
    [" If"],
    *_GUTT,
]
_CONT_FTNT_FR3_LWVS = [
    [" In an ", sub.fr3(), " word,"],
    [" the letter with the $vocshewa"],
    [" is always a guttural. Since"],
    *_GUTT,
]
_CONT_FTNT_EXAMPLES_CONFORM = [
    ["Each example has a disjunctive accent, "],
    ["and in each example, the initial closed syllable has $gaya,"],
    [" as is generally the case when such a word has a disjunctive accent."],
]
_FTNT_THIS_CATEGORY = sub.footnote(_CONT_FTNT_THIS_CATEGORY)
_FTNT_ABOUT_HEADING = sub.footnote(_CONT_FTNT_ABOUT_HEADING)
_FTNT_LIBERTIES = sub.footnote(_CONT_FTNT_LIBERTIES)
_FTNT_FR1_LWVS = sub.footnote(_CONT_FTNT_FR1_LWVS)
_FTNT_FR2_CLOSED = sub.footnote(_CONT_FTNT_FR2_CLOSED)
_FTNT_FR2_LWVS = sub.footnote(_CONT_FTNT_FR2_LWVS)
_FTNT_FR3_LWVS = sub.footnote(_CONT_FTNT_FR3_LWVS)
_FTNT_EXAMPLES_CONFORM = sub.footnote(_CONT_FTNT_EXAMPLES_CONFORM)
_CONT_PARA_1 = [
    ["A word like ", hlp.hbo(sub.pat_mitqatlim()[0])],
    [" has “regular” structure. It has:"],
]
_CONT_PARA_2 = [
    ["In words of regular structure, the initial closed syllable generally has"],
    [" $gaya if the word has a disjunctive accent. E.g.: "],
]
_CONT_PARA_3 = [
    ["We have seen that"],
    [" a word of regular structure may have its buffer syllable"],
    [" closed implicitly, i.e. closed"],
    [" by a $dagesh_xazaq on the letter with the $vocshewa"],
    [hlp.ftntjoin(".", _FTNT_FR1_LWVS)],
    [" We call this pattern ", sub.fr1(), "."],
    [" The prototype and example we have been using for ", sub.fr1()],
    [" are repeated below:"],
]
_CONT_PARA_4 = [
    ["A word of regular structure may instead have its buffer syllable"],
    [" closed explicitly,"],
    [" i.e. closed by a ", hlp.ftntjoin("letter", _FTNT_FR2_CLOSED)],
    [" right before the letter with the $vocshewa"],
    [hlp.ftntjoin(".", _FTNT_FR2_LWVS)],
    [" We call this pattern ", sub.fr2(), "."],
    [" A prototype and example are as follows:"],
]
_CONT_PARA_5 = [
    ["A word of regular structure may,"],
    [" instead of either of the two options described above,"],
    [" have its buffer syllable"],
    [" left open"],
    [" and have a guttural as the letter with the $vocshewa"],
    [hlp.ftntjoin(".", _FTNT_FR3_LWVS)],
    [" We call this pattern ", sub.fr3(), "."],
    [" A prototype and example are as follows:"],
]
_CONT_PARA_6 = [
    "The prototypes and examples for all three patterns are repeated below:"
]
_CONT_PARA_7 = [
    ["Further examples of all three patterns are shown in the three tables below"],
    [hlp.ftntjoin(".", _FTNT_EXAMPLES_CONFORM)],
]
_CONT_PARA_8 = [
    "This category of ",
    hlp.ftntjoin(sub.gaya(), _FTNT_THIS_CATEGORY),
    " is mentioned in the ",
    sub.diqduqe_dotan_sec_num(15),
    ". An expanded statement is given in the ",
    sub.quntrese(),
    ", as indicated in the notes there, and in Yeivin, 1968, p. 96.",
]
SEC = [
    sub.para(["[", _FTNT_ABOUT_HEADING, ", ", _FTNT_LIBERTIES, "]"]),
    sub.para_with_initial_uah("Regular Structure", _CONT_PARA_1),
    _TABLE_1,
    sub.para(_CONT_PARA_2),
    _TABLE_2,
    sub.para(_CONT_PARA_3),
    _TABLE_4_FR1,
    sub.para(_CONT_PARA_4),
    _TABLE_4_FR2,
    sub.para(_CONT_PARA_5),
    _TABLE_4_FR3,
    sub.para(_CONT_PARA_6),
    _TABLE_4,
    sub.para(_CONT_PARA_7),
    _TABLE_5,
    aht_html.horizontal_rule(),
    _TABLE_6,
    aht_html.horizontal_rule(),
    _TABLE_7,
    sub.para(_CONT_PARA_8),
]
