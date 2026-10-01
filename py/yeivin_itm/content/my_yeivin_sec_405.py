import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_FTNT_LIBERTIES = sub.footnote(
    [
        "I recast $itm’s running prose here as an explicit case analysis:"
        " I label the two words α and β, number the cases 1a through 3h, and"
        " work through each of the three main cases in turn."
        " Each example below is tagged with the case it illustrates."
        " ",
        hlp.rtn(404),
        " uses the same recast.",
    ]
)
_FTNT_PS_119_14 = sub.footnote(
    [
        "It is unclear from what manuscript, if any, $itm gets this exceptional pointing ",
        hlp.paren_tt(hlp.hbo("שֿשתי")),
        ". Perhaps this pointing is from ",
        sub.ms_aleppo(),
        " but the pointing is not clear there in ",
        sub.ms_aleppo(),
        ". The consensus pointing is not exceptional: ",
        hlp.hbo("שּשתי"),
        " ",
        hlp.paren_tt(hlp.hbo("עֵדְוֺתֶ֥יךָ שַּׂ֗שְׂתִּי")),
        ". See the ",
        sub.mamdoc("D1-Psalms.html#c119v14"),
        ".",
    ]
)


def _im_unsure(the_hboloc, the_rule):
    return [
        "I’m unsure whether or not $itm is implying that ",
        the_hboloc,
        " is the only exception to ",
        *the_rule,
        ", or just an example of such an exception.",
    ]


_HBOLOC_ARGS_RUT_4_17 = "וַתִּקְרֶ֤אנָֽה שְׁמוֹ֙", "@Rut 4:17"
_HBOLOC_RUT_4_17 = hlp.hboloc(*_HBOLOC_ARGS_RUT_4_17)
_HBOLOC_ARGS_PS_19_3 = "וְלַ֥יְלָה לְּ֝לַ֗יְלָה", "@Ps 19:3"
_HBOLOC_PS_19_3 = hlp.hboloc(*_HBOLOC_ARGS_PS_19_3)
_FTNT_RUT_4_17 = sub.footnote(_im_unsure(_HBOLOC_RUT_4_17, ["1c"]))
_OTHER_THAN_LEKHA = "other than ", hlp.hbo("לְךָ")
_FTNT_PS_19_3 = sub.footnote(
    _im_unsure(_HBOLOC_PS_19_3, ["1d ", hlp.paren_xt(_OTHER_THAN_LEKHA)])
)


def _nxp(nx_str, paren_inner, paren_func=hlp.paren):
    return nx_str, " ", *paren_func(paren_inner)


_NXP_1A = _nxp("1a", sub.dol(["$dexiq in a simple case"]))
_NXP_1B = _nxp("1b", sub.dol(["$dexiq even in ", sub.resh()]))
_NXP_1C = _nxp("1c", sub.dol(["$dexiq even if β starts with $shewa"]))
_NXP_1D = _nxp("1d", sub.dol(["no $dexiq if β starts with ", hlp.hbo("בְוְכְלְ")]))
_TABLE_1_DATA = [
    ("עָלֶ֣יךָ פָּ֑רֶץ", "@Gen 38:29", _NXP_1A),
    ("הֶ֥רָה נָּֽסוּ׃", "@Gen 14:10", sub.saa()),
    ("מָחַ֤צְתָּ רֹּאשׁ֙", "@Ḥab 3:13", _NXP_1B),
    ("תִּקְרֶ֥אנָה לִ֖י", "@Rut 1:20", "exception to 1a"),
    ("קְרֶ֤אןָ לִי֙", "@Rut 1:20", "exception to 1a"),
    (
        "עֵדְוֺתֶ֥יךָ שַׂ֗שְׂתִּי",
        "@Ps 119:14",
        [hlp.ftntjoin("exception to 1a", _FTNT_PS_119_14)],
    ),
    ("אַ֣רְצָה כְּנַ֔עַן", "@Gen 12:5", _NXP_1C),
    ("הִרְחִ֤יבָה שְּׁאוֹל֙", "@Is 5:14", sub.saa()),
    (*_HBOLOC_ARGS_RUT_4_17, [hlp.ftntjoin("exception to 1c", _FTNT_RUT_4_17)]),
    ("יְדַעְתִּ֣יךָֽ בְשֵׁ֔ם", "@Ex 33:12", _NXP_1D),
    ("קְרָאתִ֥יךָֽ בְצֶ֖דֶק", "@Is 42:6", sub.saa()),
    (
        "חָלִ֨לָה לְּךָ֜",
        "@Gen 18:25",
        sub.dol(["exception to 1d: $dexiq in ", hlp.hbo("לְךָ")]),
    ),
    ("לָקַ֥חְתָּ לְּךָ֖", "@2S 12:9", sub.saa()),
    (
        *_HBOLOC_ARGS_PS_19_3,
        sub.dol(
            [
                "exception to 1d: $dexiq for phonetic ",
                hlp.ftntjoin("reasons", _FTNT_PS_19_3),
            ]
        ),
    ),
]
_ISE_JER_31_26 = "@Jer 31:26"  # 31:25 in MAM
# Uncharacteristically, ITM uses the same versification as MAM here.
# I.e. ITM does not use BHS versification here.
# I.e. ITM says 31:25, not 31:26.
# Nonetheless, I use BHS versification as the primary one, to be consistent
# with the rest of ITM.
_TABLE_2_DATA = [
    ("יָ֣לְדָה בֵּ֔ן", "@Gen 19:38", ["2a"]),
    ("עָ֥רְבָה לִּֽי׃", _ISE_JER_31_26, sub.saa()),
    ("מָ֣לְאָה גַּ֔ת", "@Joel 4:13", sub.saa()),
    ("נֹ֥סְסָה בֽוֹ׃", "@Is 59:19", ["exception to 2a"]),
    ("מָ֪צְאָה בַ֡יִת", "@Ps 84:4", sub.saa()),
    ("וּמָ֣חֲתָה פִ֑יהָ", "@Prov 30:20", sub.saa()),
    ("רָ֣חֲקָה מֶֽנִּי׃", hlp.make_dloc("@Job 21:16", "@Job 22:18"), sub.saa()),
    ("מֹ֣שְׁלָה ל֑וֹ", "@Is 40:10", sub.saa()),
    ("חָ֣רָה לָ֔ךְ", "@Gen 4:6", ["2b"]),
    ("וְעָ֥שָׂה פֶ֖סַח", "@Nu 9:10", sub.saa()),
    ("שִׂ֣יחָה לִֽי׃", "@Ps 119:99", sub.saa()),
    ("עָ֣נָה בִ֔י", "@Rut 1:21", sub.saa()),
]
_FTNT_RUT_2_7 = sub.footnote(["Where’s the $pgaya?"])
_FTNT_JOB_5_23 = sub.footnote(
    [
        "Here $itm shows the pointing of ",
        sub.ms_lenin(),
        ", which lacks the expected $dexiq in לך. The pointing of ",
        sub.ms_aleppo(),
        " has the expected $dexiq, i.e. ",
        sub.ms_aleppo(),
        " has ",
        hlp.hbo("הׇשְׁלְמָה־לָּֽךְ׃"),
        sub.thspp(),
    ]
)
_NXP_3A = _nxp("3a", sub.dol(["$dexiq in a simple case"]))
_NXP_3B = _nxp("3b", sub.dol(["$vshewa after a long vowel"]))
_NXP_3C = _nxp("3c", sub.dol(["$vshewa after $pgaya"]))
_NXP_3D = _nxp("3d", sub.dol(["no $dexiq in exceptional cases"]))
_TABLE_3_ABCD_DATA = [
    ("גְּשָׁה־נָּ֥א", "@Gen 27:26", _NXP_3A),
    ("שְׁבָה־פֹּ֖ה", "@Rut 4:1", sub.saa()),
    ("וְאֶדְרְשָׁה־בָּ֑הּ", "@1S 28:7", sub.saa()),
    ("נִבְחֲרָה־לָּ֑נוּ", "@Job 34:4", sub.saa()),
    ("נִתְּנָה־לּ֛וֹ", "@2K 25:30", sub.saa()),
    ("אֲזַמְּרָה־לָּ֑ךְ", "@Ps 71:23", sub.saa()),
    ######
    ("יָלְדָה־לּ֥וֹ", "@Gen 21:3", _NXP_3B),
    ("וְעָֽנְתָה־בִּ֤י", "@Gen 30:33", sub.saa()),
    ("אֵֽלֲכָה־לִּ֤י", "@Jer 5:5", sub.saa()),
    # MAM אֵֽלְﬞכָה־לִּ֤י (varika-shewa) vs ITM xataf patax
    ######
    ("לֻֽקֳחָה־זֹּֽאת׃", "@Gen 2:23", _NXP_3C),
    # MAM לֻֽקְﬞחָה־זֹּֽאת׃ (varika-shewa) vs ITM xataf qamats
    ("אֲלַקֳּטָה־נָּא֙", "@Rut 2:7", [sub.saa(), " ", _FTNT_RUT_2_7]),
    ######
    ("סְאָה־סֹ֣לֶת", "@2K 7:1", _NXP_3D),
    ("מַחֲלָה־לֵ֑ב", "@Prov 13:12", sub.saa()),
    ("וְאַהֲבָה־שָׁ֑ם", "@Prov 15:17", sub.saa()),
    ("אֲשַׁלְּמָה־רָ֑ע", "@Prov 20:22", sub.saa()),
    ("נִשְׁאֲרָה־בִֽי׃", "@Dan 10:17", sub.saa()),
    ("הׇשְׁלְמָה־לָֽךְ׃", "@Job 5:23", [sub.saa(), " ", _FTNT_JOB_5_23]),
]
_PAREN_INNER_3E = sub.dol(["no $dexiq if no $vshewa"])
_PAREN_INNER_3F = "misc. exceptions to 3e"
_PAREN_INNER_3G = "exceptions to 3e common in some verb forms"
_PAREN_INNER_3H = sub.dol(["$dexiq despite lacking both $vshewa and $maqqef"])
_NXP_3E = _nxp("3e", _PAREN_INNER_3E)
_NXP_3F = _nxp("3f", _PAREN_INNER_3F)
_NXP_3G = _nxp("3g", _PAREN_INNER_3G)
_NXP_3H = _nxp("3h", _PAREN_INNER_3H, hlp.paren_xt)
_PS_116 = "נֶגְדָה־", "*נֶגְ*דָה־", "נָּ֝֗א"
_PS_116_PLAIN = _PS_116[0] + _PS_116[2]
_FTNT_AND_CF = sub.footnote(
    [
        "Here $itm presents this example as “And cf. α-β,” i.e. “And cf. ",
        hlp.hbo(_PS_116_PLAIN),
        ".” I don’t know what motivates this “cf.” (confer/compare),"
        " but it is intriguing.",
    ]
)
_PS_116_ROW = [
    hlp.some_hi((_PS_116[0], _PS_116[1], hlp.make_dloc("@Ps 116:14", "@Ps 116:18"))),
    hlp.hbo(_PS_116[2]),
    [sub.saa(), " ", _FTNT_AND_CF],
]
_TABLE_3_EFGH_DATA = [
    [
        hlp.some_hi(("וּלְדׇבְקָה־", "וּלְ*דׇבְ*קָה־", "@Dt 11:22")),
        hlp.hbo("בֽוֹ׃"),
        _NXP_3E,
    ],
    [hlp.hboloc("צִוָּה־", "@Dt 33:4"), hlp.hbo("לָ֖נוּ"), sub.saa()],
    [hlp.hboloc("אֽוֹיָה־", "@Ps 120:5"), hlp.hbo("לִ֭י"), sub.saa()],
    [
        hlp.some_hi(("עֶרְיָה־", "*עֶרְ*יָה־", "@Mi 1:11")),
        hlp.hbo("בֹ֑שֶׁת"),
        sub.saa(),
    ],
    [hlp.hboloc("נָֽטָה־", "@Gen 33:19"), hlp.hbo("שָׁם֙"), sub.saa()],
    ######
    [hlp.some_hi(("שִׁלְחָה־", "*שִׁלְ*חָה־", "@Ez 17:7")), hlp.hbo("לּ֔וֹ"), _NXP_3F],
    [hlp.hboloc("וּבָ֖אתָ־", "@2K 9:2"), hlp.hbo("שָּׁ֑מָּה"), sub.saa()],
    [
        hlp.some_hi(("וַתֹּאמַ֖רְנָה־", "וַתֹּא*מַ֖רְ*נָה־", "@Rut 1:10")),
        hlp.hbo("לָּ֑הּ"),
        sub.saa(),
    ],
    [
        hlp.some_hi(("אִם־יֶשְׁךָ־", "אִם־*יֶשְׁ*ךָ־", "@Gen 24:42")),
        hlp.hbo("נָּא֙"),
        sub.saa(),
    ],
    ######
    [
        hlp.some_hi(("שִׁמְעָה־", "*שִׁמְ*עָה־", "@Job 32:10")),
        hlp.hbo("לִּ֑י"),
        _NXP_3G,
    ],
    [
        hlp.some_hi(("וּשְׁקָה־", "*וּשְׁ*קָה־", "@Gen 27:26")),
        hlp.hbo("לִּ֖י"),
        sub.saa(),
    ],
    [hlp.hboloc("הָֽבָה־", "@Gen 30:1"), hlp.hbo("לִּ֣י"), sub.saa()],
    [hlp.hboloc("אָֽרָה־", "@Nu 22:6"), hlp.hbo("לִּ֜י"), sub.saa()],
    [hlp.hboloc("קָֽבָה־", "@Nu 22:11"), hlp.hbo("לִּי֙"), sub.saa()],
    [hlp.some_hi(("וּלְכָה־", "*וּלְ*כָה־", "@Nu 22:17")), hlp.hbo("נָּא֙"), sub.saa()],
    [hlp.hboloc("אוֹדִיעָה־", "@Is 5:5"), hlp.hbo("נָּ֣א"), sub.saa()],
    [hlp.hboloc("הַגִּֽידָה־", "@Gen 32:30"), hlp.hbo("נָּ֣א"), sub.saa()],
    _PS_116_ROW,
    ######
    [*hlp.alpha_beta("הוֹשִׁ֘יעָ֥ה נָּ֑א", "@Ps 118:25"), _NXP_3H],
    [*hlp.alpha_beta("הַצְלִ֘יחָ֥ה נָּֽא׃", "@Ps 118:25"), sub.saa()],
]

_CASE_1 = ["α has penultimate stress normally, i.e. not via accent retraction"]
_CASE_2 = ["α has penultimate stress via accent retraction"]
_CASE_3 = ["α has $maqqef"]


def _digging(further, case_num, case_description):
    return sub.para(
        [
            f"Digging {further} into case ({case_num}) above,"
            " which is the case where ",
            *case_description,
            ":",
        ]
    )


def _digging_further_case_2_list():
    ftnt = sub.footnote(
        [
            "I take this to mean that such a syllable could have $gaya,",
            " in a context where the accent was not retracted.",
        ]
    )
    return sub.ordered_list_with_lcromalpha(
        [
            [
                ["$Dexiq is only used when the retracted stress"],
                [" is on a long vowel followed by some type of $shewa"],
                [" ", hlp.paren_xt("simple or $xatef"), "."],
                [" Such a syllable could have $gaya", hlp.ftntjoin(".", ftnt)],
            ],
            ["Otherwise, $dexiq is absent."],
        ]
    )


SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    sub.para_with_romnum_and_initial_uah(
        "ii", sub.cmn_403_lcromnum_ii(), ["This is used:"]
    ),
    sub.ordered_list_with_warabnum(
        [["When ", *_CASE_1, "."], ["When ", *_CASE_2, "."], ["When ", *_CASE_3, "."]]
    ),
    _digging("further", 1, _CASE_1),
    sub.ordered_list_with_lcromalpha(
        [
            ["$Dexiq is used in simple cases."],
            ["$Dexiq is even used in ", sub.resh(), "."],
            [
                "$Dexiq is even used in many cases where β starts with $shewa.",
            ],
            [
                "But $dexiq is absent if β starts with $shewa on ",
                hlp.comma_list_of_bdis("ב", "ו", "כ", "or ל"),
                ".",
            ],
        ]
    ),
    hlp.table_std_alpha_beta_3col_std(_TABLE_1_DATA),
    _digging("further", 2, _CASE_2),
    _digging_further_case_2_list(),
    hlp.table_std_alpha_beta_3col_std(_TABLE_2_DATA),
    _digging("further", 3, _CASE_3),
    sub.ordered_list_with_lcromalpha(
        [
            [  # a
                "$Dexiq is only used if there’s a $vocshewa attached to the ",
                sub.qamets(),
                " of α.",
            ],
            ["This $vocshewa may come after a long vowel."],  # b
            ["This $vocshewa may come after a $pgaya."],  # c
            ["$Dexiq is absent in some exceptional cases."],  # d
        ]
    ),
    hlp.table_std_alpha_beta_3col_std(_TABLE_3_ABCD_DATA),
    _digging("even further", 3, _CASE_3),
    sub.ordered_list_with_lcromalpha_ws(
        5,
        [
            [  # e
                "As expected, $dexiq is usually absent if α lacks a $vocshewa attached to its ",
                sub.qamets(),
                ".",
            ],
            [  # f
                "But, there are a considerable number of exceptions. ",
                hlp.paren(
                    [
                        "$Dexiq is used despite lacking this $shewa.",
                    ]
                ),
            ],
            [  # g
                "These exceptions are particularly common where"
                " α is a verb form in the long form of the imperfect or imperative."
            ],
            [  # h
                "In a few cases that are even more exceptional, "
                "$dexiq is used despite lacking both $shewa and $maqqef.",
            ],
        ],
    ),
    sub.para(
        [
            "In the table below,"
            " we highlight some syllables to show that"
            " although there is a $shewa"
            " right before the ",
            sub.qamets(),
            ", presumably it is silent, i.e. not attached to the ",
            sub.qamets(),
            ".",
        ]
    ),
    hlp.table_std_alpha_beta_3col(_TABLE_3_EFGH_DATA),
    sub.para(
        [
            "Where β starts with a ",
            sub.begad_kefat(),
            " letter, $dexiq is used as on other letters, so that this $dexiq is regularly listed"
            " among the phenomena which nullify the rules that a ",
            sub.begad_kefat(),
            " letter at the start of a word is $dagesh-free if it follows"
            " a word with a conjunctive accent that ends with an open syllable ",
            hlp.rtn_p(400),
            ".",
        ]
    ),
]
