import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub


def _naftali(hbo_contents):
    return sub.xxx_hbo_in_parens("bN", hbo_contents)


def _asher(hbo_contents):
    return sub.xxx_hbo_in_parens("bA", hbo_contents)


_FTNT_LIBERTIES = sub.footnote(
    [
        "I expanded $itm’s one-clause remark on dissimilation, “in some of them"
        " similar consonants occur together,” into the two-branch analysis"
        " below, distinguishing pairs that are close to each other from pairs in"
        " almost-repeated contexts. I also added the closing paragraph on what"
        " cases 9 and 10 agree on as well as disagree on.",
    ]
)
_FTNT_FOR_EX_15_11 = sub.footnote(
    [
        sub.para(
            [
                "Arguably, case 3, ",
                hlp.hbo("מִ֥י כָּמֹ֖כָה"),
                " (כּמכה),"
                " could be included here as well,"
                " since, famously, it contrasts with ",
                hlp.hboloc("מִֽי־כָמֹ֤כָה", "@Ex 15:11"),
                " (כֿמכה) at the start of the same verse:",
            ]
        ),
        hlp.table_std_rtl(
            [
                [
                    hlp.line_break(
                        hlp.hbo("מִֽי־כָמֹ֤כָה בָּֽאֵלִם֙ יְהֹוָ֔ה"),
                        hlp.hbo("מִ֥י כָּמֹ֖כָה נֶאְדָּ֣ר בַּקֹּ֑דֶשׁ"),
                    )
                ]
            ]
        ),
    ]
)
_TABLE_FOR_1_THRU_7_DATA = [
    ("כִּֽי־גָאֹ֣ה גָּאָ֔ה", hlp.make_dloc("@Ex 15:1", "@Ex 15:21"), "1, 2"),
    ("מִ֥י כָּמֹ֖כָה", "@Ex 15:11", "3"),
    ("יִדְּמ֣וּ כָּאָ֑בֶן", "@Ex 15:16", "4"),
    ("וְשַׂמְתִּ֤י כַּֽדְכֹד֙", "@Is 54:12", "5"),
    ("וְנִלְאֵ֥יתִי כַּֽלְכֵ֖ל", "@Jer 20:9", "6"),
    ("וְחׇכְמָ֥ה כְּחׇכְמַת־", "@Dan 5:11", "7"),
]
_TABLE_FOR_8_DATA = [("ז֣וּ גָּאָ֑לְתָּ", "@Ex 15:13", ["8 ", _naftali("גָ")])]
_TABLE_FOR_9_THRU_13_DATA = [
    [
        hlp.hboloc("אֲדַרְגָּזְרַיָּא֩", "@Dan 3:2"),
        hlp.hbo("גְּדָ֨בְרַיָּ֤א דְּתָבְרַיָּא֙"),
        ["9 ", _asher("גְ")],
    ],
    # MAM אֲדַרְגָּזְרַיָּא֩ גְדָ֨בְרַיָּ֤א דְּתָבְרַיָּא֙
    [
        hlp.hboloc("אֲדַרְגָּזְרַיָּ֣א", "@Dan 3:3"),
        hlp.hbo("גְּדָבְרַיָּא֩ דְּתָ֨בְרַיָּ֜א"),
        ["10 ", _asher("גְ")],
    ],
    # MAM אֲדַרְגָּזְרַיָּ֣א גְדָבְרַיָּא֩ דְּתָ֨בְרַיָּ֜א
    [
        *hlp.alpha_beta("הַשְּׁמִינִ֣י בַּחֲמִשָּֽׁה־", "@1K 12:32"),
        ["11 ", _asher("בַ")],
    ],
    # MAM הַשְּׁמִינִ֣י בַחֲמִשָּֽׁה־
    [
        *hlp.alpha_beta(
            "שַׂבְּכָ֤א פְּסַנְתֵּרִין֙", hlp.make_dloc("@Dan 3:5", "@Dan 3:10")
        ),
        ["12, 13 ", _asher("פְ")],
    ],
    # MAM שַׂבְּכָ֤א פְסַנְתֵּרִין֙
]
_TABLE_FOR_9_FTNT_9_NOT_7 = [
    [hlp.hbo("גדבריָּ֤א דְּתָבְרַיָּא֙")],
    [hlp.hbo("גדבריָּא֩ דְּתָ֨בְרַיָּ֜א")],
]
_GD_DISAGREEMENT = hlp.hbo("גְּד"), sub.thsp(), "/", sub.thsp(), hlp.hbo("גְד")
_FTNT_9_NOT_7 = sub.footnote(
    [
        sub.para(
            [
                "So, arguably, there are nine rather than seven agreed-upon cases."
                " I.e., arguably, we should include the end parts of cases 9 and 10"
                " in the list of agreed-upon exceptions."
                " We might list these agreements as follows,"
                " hiding the ",
                *_GD_DISAGREEMENT,
                " disagreement by limiting the pointing to the relevant end parts:",
            ]
        ),
        hlp.table_std_rtl(_TABLE_FOR_9_FTNT_9_NOT_7),
    ]
)
_FTNT_IN_EX_15 = sub.footnote(
    [
        "Case 8, like cases 1, 3, and 4,"
        " is in the special section of Exodus 15"
        " known variously as ",
        hlp.comma_list_of_bdis("שירת הים", "אז ישיר משה", "or מי כמכה"),
        ". So, this section has not only special layout and special musical motifs,"
        " but also a great concentration of exceptional uses of $dagesh! ",
        hlp.paren(
            "Also, case 2 is from Miriam’s song, which comes almost right after שירת הים."
        ),
    ]
)
SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    sub.para(
        [
            "Besides the categories noted in ",
            hlp.rtn(400),
            " and ",
            hlp.rtn(401),
            ", there are a small number of exceptional cases"
            " in which the general rule is not followed."
            " There is general agreement on seven of these cases,"
            " which are listed in most of the sources:",
        ]
    ),
    hlp.table_std_alpha_beta_3col_std(_TABLE_FOR_1_THRU_7_DATA, arg_to_troh=None),
    sub.para(
        [
            "In some of these seven cases, if the exceptional $dagesh were not present,"
            " identical or similar consonant sounds would occur either:",
        ]
    ),
    sub.unordered_list(
        [
            ["Close to each other, as in ", hlp.hbo("כְח"), " (case 7)."],
            [
                "Or, not so close, but in almost-repeated contexts, as in ",
                hlp.hbo("גָאֹ֣ה גָאָ֔ה"),
                sub.thspc(),
                " ",
                hlp.hbo("כַֽדְכֹד֙"),
                sub.thspc(),
                " and ",
                hlp.hbo("כַֽלְכֵ֖ל"),
                sub.thspc(),
                " ",
                hlp.ftntjoin("(cases 1, 2, 5, and 6).", _FTNT_FOR_EX_15_11),
            ],
        ]
    ),
    sub.para(
        [
            "In these cases, the exceptional $dagesh"
            " may reflect a “need” to dissimilate these sounds.",
        ]
    ),
    sub.para(
        [
            "Ben Asher alone adds one additional case"
            " to the agreed-upon seven cases ",
            hlp.ftntjoin("above:", _FTNT_IN_EX_15),
        ]
    ),
    hlp.table_std_alpha_beta_3col_std(_TABLE_FOR_8_DATA, arg_to_troh=None),
    sub.para(
        [
            "Ben Naftali alone adds five additional cases to the agreed-upon seven cases above:"
        ]
    ),
    hlp.table_std_alpha_beta_3col(_TABLE_FOR_9_THRU_13_DATA, arg_to_troh=None),
    sub.para(
        [
            "Cases 9 and 10 differ in accents only, and"
            " contain not only a disagreement ",
            hlp.paren_tt(_GD_DISAGREEMENT),
            " but also an agreement: both bA and bN give a $dagesh to the ",
            sub.dalet(),
            " of ",
            hlp.hbo("דְּתָבְרַיָּא"),
            hlp.ftntjoin(sub.thspp(), _FTNT_9_NOT_7),
            " This exceptional $dagesh may reflect a “need”"
            " to dissimilate the sounds of the initial $shewa-separated ",
            sub.begad_kefat(),
            " pair ",
            hlp.hbo("דְת"),
            sub.thspc(),
            " like the standard pairs covered in ",
            hlp.rtn(401),
            ".",
        ]
    ),
]
