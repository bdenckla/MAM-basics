import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_FTNT_LIBERTIES = sub.footnote(
    [
        "I expanded $itm’s treatment of ",
        sub.mappiq(),
        " to explain why such a final syllable counts as closed, distinguishing"
        " a naive form of the rule from a full form; $itm states the rule once,"
        " in terms of the final letter. I also labeled the ",
        hlp.hbo("יְהֹוָה"),
        " example as working via the $qere.",
    ]
)
_THE_FULL_FORM = [
    "The full form of the rule is not about the letter that ends the word:"
    " it is about the openness of the syllable that ends the word."
]


def _intro_para():
    ftnt = sub.footnote(
        [
            "Note that this is the naive form of the rule."
            " The naive form of the rule is about the letter that ends the word."
            " ",
            *_THE_FULL_FORM,
        ]
    )
    return sub.para(
        [
            "The Masorah mentions a number of מבטלים:"
            " phenomena which nullify the general rule,"
            " giving a ",
            sub.begad_kefat(),
            " letter a $dagesh despite coming after ",
            sub.comma_list_of_heb_ahw_or_y(),
            hlp.ftntjoin(".", ftnt),
            " These מבטלים are ",
            sub.three_comma_and(sub.mappiq(), sub.paseq(), sub.dexiq()),
            ". They are described below.",
        ]
    )


def _num_1_mappiq_para_1():
    ftnt_1 = sub.footnote(["א not mentioned in $itm; accident or on purpose?"])
    ftnt_2 = sub.footnote(
        [
            "Only the naive form of the rule is broken by such a $dagesh. ",
            *_THE_FULL_FORM,
        ]
    )
    return sub.para(
        [
            "1) ",
            sub.mappiq(cap=True),
            ". Consider a word whose final syllable is closed by a consonantal ",
            sub.comma_list_of_heb_hw_or_y(),
            hlp.ftntjoin(".", ftnt_1),
            " Its final letter is said to be ",
            sub.mappiq(),
            " (מַפִיק), meaning, “pronounced.”"
            " (Indeed, if that letter is ה, it may even bear the mark that goes by the name ",
            sub.mappiq(),
            ".) Though its final syllable may look open at first glance,"
            " it is in fact closed, so"
            " a ",
            sub.begad_kefat(),
            " letter at the start of the next word is given a $dagesh",
            hlp.ftntjoin(".", ftnt_2),
            " E.g.:",
        ]
    )


def _num_1_mappiq_table_1_gen_6_16():
    _hboloc_args_for_ps_2_11 = "יְהֹוָ֣ה בְּיִרְאָ֑ה", "@Ps 2:11"
    ftnt = sub.footnote(
        [
            "For cases after ",
            hlp.hbo("יְהֹוָה"),
            sub.thspc(),
            " like ",
            hlp.hboloc(*_hboloc_args_for_ps_2_11),
            " above, it may be helpful to think of the implied ",
            sub.qere(),
            ", ",
            hlp.hbo("אֲדֹנָי"),
            sub.thspc(),
            " whose final ",
            sub.yod(),
            " is consonantal.",
        ]
    )
    _hbo_ps_2_11_adonai = hlp.paren_tt(hlp.hbo("אֲדֹנָ֣י"))
    table_data = [
        [
            *hlp.alpha_beta("בְּצִדָּ֣הּ תָּשִׂ֑ים", "@Gen 6:16"),
            [sub.mappiq(), " ה (marked as such)"],
        ],
        [*hlp.alpha_beta("יָדָ֣יו תְּבִיאֶ֔ינָה", "@Lev 7:30"), [sub.mappiq(), " ו"]],
        [*hlp.alpha_beta("שָׂרַ֣י גְּבִרְתִּ֔י", "@Gen 16:8"), [sub.mappiq(), " י"]],
        [
            *hlp.alpha_beta(*_hboloc_args_for_ps_2_11),
            [sub.mappiq(), " י via the ", sub.qere()],
        ],
        [_hbo_ps_2_11_adonai, hlp.hbo("בְּיִרְאָ֑ה"), ftnt],
    ]
    return hlp.table_std_alpha_beta_3col(table_data, arg_to_troh=None)


def _num_1_mappiq_para_there_are_three_exceptions():
    ftnt_1 = sub.footnote(
        [
            "These are real exceptions, i.e."
            " these are exceptions to the full rather than naive form of the rule."
        ]
    )
    ftnt_2 = sub.footnote(
        [
            "Indeed, ",
            sub.rafe(),
            " is used in some printed editions in these three cases,"
            " even if (as is usually the case)"
            " it is the edition’s policy"
            " to use ",
            sub.rafe(),
            " only in cases deemed exceptional.",
        ]
    )
    return sub.para(
        [
            ["There are three ", hlp.ftntjoin("exceptions", ftnt_1)],
            [" where, although the preceding syllable is closed by a"],
            [" ", sub.waw(), " or ", sub.yod(), ","],
            [" the ", sub.bet(), " or ", sub.tav(), " that follows is nonetheless"],
            [" $dagesh-free", hlp.ftntjoin(":", ftnt_2)],
        ]
    )


_NUM_1_MAPPIQ_TABLE_DATA_2 = [
    ("קַֽו־תֹ֖הוּ", "@Is 34:11"),  # MAM קַֽו־תֹֿ֖הוּ (has rafe noting the exception)
    (
        "שָׁלֵ֣ו בָהּ֒",
        "@Ez 23:42",
    ),  # MAM שָׁלֵ֣ו בָֿהּ֒ (has rafe noting the exception)
    (
        "אֲדֹנָ֥י בָ֝֗ם",
        "@Ps 68:18",
    ),  # MAM אֲדֹנָ֥י בָֿ֝֗ם (has rafe noting the exception)
]
_NUM_1_MAPPIQ_TABLE_IS_34_11 = hlp.table_std_alpha_beta_2col_std(
    _NUM_1_MAPPIQ_TABLE_DATA_2, arg_to_troh=None
)

_NUM_1_MAPPIQ_PARA_IN_SOME_VERSIONS = sub.para(
    [
        "In some versions of this rule, the ",
        sub.yod(),
        " cases are restricted such that $dagesh only comes after ",
        sub.patax(),
        "-",
        sub.yod(),
        " or ",
        sub.qamets(),
        "-",
        sub.yod(),
        ", and not after ",
        sub.xolem(),
        "-",
        sub.yod(),
        ". For example this would yield ",
        hlp.hboloc("גּ֣וֹי גָד֔וֹל", "@Dt 4:8"),
        " rather than the usual ",
        hlp.hbo("גּ֣וֹי גָּד֔וֹל"),
        sub.thspp(),
        " This may reflect a tradition in which ",
        sub.xireq(),
        " was pronounced after final consonantal ",
        sub.yod(),
        ", as is marked in some manuscripts with expanded Tiberian pointing, as ",
        hlp.hbo("גּוֹיִ"),
        sub.thspp(),
    ]
)
_FTNT_EXPLAIN_PASEQ = sub.footnote(sub.explain_paseq())
_NUM_2_PASEQ_PARA = sub.para(
    [
        "2) ",
        sub.paseq(cap=True),
        ". If ",
        sub.paseq(),
        " ",
        hlp.rtn_p(283),
        " separates the words, then the ",
        sub.begad_kefat(),
        " letter is given a $dagesh. ",
        hlp.ftntjoin("E.g.:", _FTNT_EXPLAIN_PASEQ),
    ]
)
_NUM_2_PASEQ_TABLE_DATA = [
    [hlp.hboloc(sub.end_with_paseq("אֹת֣וֹ"), "@Dt 9:21"), hlp.hbo("בָּאֵשׁ֒")],
    # אֹת֣וֹ בִכְנָפָיו֮ Lev 1:17
    [hlp.hboloc(sub.end_with_paseq("עַל־עַמּ֤וֹ"), "@1C 21:3"), hlp.hbo("כָּהֵם֙")],
    # אֶת־עַמּ֣וֹ בַשָּׁלֽוֹם׃ Ps 29:11
]
_NUM_2_PASEQ_TABLE = hlp.table_std_alpha_beta_2col(
    _NUM_2_PASEQ_TABLE_DATA, arg_to_troh=None
)
_NUM_3_DEHIQ_PARA = sub.para(
    [
        "3) $Dexiq ",
        hlp.paren("conjunctive $dagesh"),
        ". See ",
        hlp.rtn(403),
        ".",
    ]
)

SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    _intro_para(),
    _num_1_mappiq_para_1(),
    _num_1_mappiq_table_1_gen_6_16(),
    _num_1_mappiq_para_there_are_three_exceptions(),
    _NUM_1_MAPPIQ_TABLE_IS_34_11,
    _NUM_1_MAPPIQ_PARA_IN_SOME_VERSIONS,
    _NUM_2_PASEQ_PARA,
    _NUM_2_PASEQ_TABLE,
    _NUM_3_DEHIQ_PARA,
]
