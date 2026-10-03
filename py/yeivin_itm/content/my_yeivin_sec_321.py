import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_FTNT_LEV_13_56 = sub.footnote(
    [
        "Here $itm has $pashta; I have ",
        sub.tifxa(),
        ", i.e. $itm has ",
        hlp.hbo("מִן־הַשְּׁתִי֙"),
        sub.thspp(),
        " This seems like an error in $itm,"
        " but fortunately it is irrelevant to the point at hand,",
        " since both accents are disjunctive.",
    ]
)
_FTNT_ABOUT_ARROW = sub.footnote(
    [
        "In this and many tables that follow, I use an upwards arrow (",
        sub.saa(),
        ") to mean “same as the cell above.”",
    ]
)
_TABLE_1_ROWS = [
    [
        hlp.lhbo(hlp.make_dloc("@Ex 7:13", "@Ex 9:35"), "וַיֶּחֱזַק֙"),
        ["bN has ", sub.gaya()],
    ],
    # MAM has vav sans gaʿya, yod with gaʿya in both E7:13 & 9:35; see closed issue trope#375 (private tracker).
    [
        hlp.lhbo("@Lev 13:56", "מִן־הַשְּׁתִ֖י"),
        [sub.saa(), " ", _FTNT_LEV_13_56, ", ", _FTNT_ABOUT_ARROW],
    ],
    [
        hlp.lhbo("@Gen 13:12", "וַיֶּאֱהַ֖ל"),
        ["bA and bN agree on lack of ", sub.gaya()],
    ],
    [hlp.lhbo(hlp.make_dloc("@1K 7:4", "@1K 7:5"), "אֶל־מֶחֱזָ֖ה"), sub.saa()],
]
_TABLE_1 = hlp.table_std(
    _TABLE_1_ROWS,
    coldirs=["rtl", "ltr"],
    arg_to_caption=sub.dol(["Disjunctives lacking $gaya in bA"]),
)
_TABLE_2_ROWS = [
    [hlp.lhbo("@2C 20:17", "הִתְיַצְּב֣וּ"), ["bN has ", sub.gaya()]],
    [hlp.lhbo("@Jer 27:15", "הַֽנִּבְּאִ֥ים"), ["bN has no ", sub.gaya()]],
    [
        hlp.lhbo("@1K 20:29", "וַֽיַּחֲנ֧וּ"),
        ["bA and bN agree on presence of ", sub.gaya()],
    ],
    [
        hlp.lhbo("@2K 25:5", "וַיִּרְדְּפ֤וּ"),
        ["bA and bN agree on lack of ", sub.gaya()],
    ],
]
_TABLE_2 = hlp.table_std(
    _TABLE_2_ROWS, coldirs=["rtl", "ltr"], arg_to_caption="Conjunctives in bA"
)
_TABLE_3 = hlp.table_std_rtl(
    [
        [*hlp.norm_and_syl_sep("וַיֶּחֱזַק֙", "וַ_-יֶּ-חֱזַק֙"), sub.fr3()],
        [*hlp.norm_and_syl_sep("מִן־הַשְּׁתִ֖י", "מִן־-הַ_-שְּׁתִ֖י"), sub.fr1()],
        [*hlp.norm_and_syl_sep("וַיֶּאֱהַ֖ל", "וַ_-יֶּ-אֱהַ֖ל"), sub.fr3()],
        [*hlp.norm_and_syl_sep("אֶל־מֶחֱזָ֖ה", "אֶל־-מֶ-חֱזָ֖ה"), sub.fr3()],
        [*hlp.norm_and_syl_sep("הִתְיַצְּב֣וּ", "הִתְ-יַ_-צְּב֣וּ"), sub.fr1()],
        [*hlp.norm_and_syl_sep("הַֽנִּבְּאִ֥ים", "הַֽ_-נִּ_-בְּאִ֥ים"), sub.fr1()],
        [*hlp.norm_and_syl_sep("וַֽיַּחֲנ֧וּ", "וַֽ_-יַּ-חֲנ֧וּ"), sub.fr3()],
        [*hlp.norm_and_syl_sep("וַיִּרְדְּפ֤וּ", "וַ_-יִּרְ-דְּפ֤וּ"), sub.fr2()],
    ]
)
SEC = [
    sub.para(
        [
            "These exceptions are one of the major subjects of"
            " variation between ben Asher and ben Naftali; and indeed of"
            " marginal notes on variants in general."
            " E.g.:"
        ]
    ),
    _TABLE_1,
    _TABLE_2,
    sub.para(
        [
            "Below is a table"
            " showing the syllable structure of the examples used in the two tables above."
        ]
    ),
    _TABLE_3,
]
