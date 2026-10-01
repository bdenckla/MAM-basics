import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub
import mb_cmn.str_defs as sd

# NDL: norm, dash, locale (arg to trd_norm_and_syl_sep)
# NSL: norm, star, locale (arg to some_hi_lo)
_NDL_EX_8_11 = "הָרְוָחָ֔ה", "הָ-רְוָ-חָ֔ה", "@Ex 8:11"
# MAM has gaʿya on הָ
_NDL_EX_19_2 = "מֵרְפִידִ֗ים", "מֵ-רְפִי-דִ֗ים", "@Ex 19:2"
_NDL_JUD_19_17 = "בִּרְחֹ֣ב", "בִּרְ-חֹ֣ב", "@Jud 19:17"
_NDL_JUD_9_37 = "יוֹרְדִ֔ים", "יוֹרְ-דִ֔ים", "@Jud 9:37"
# MAM has gaʿya on י (yod)
_NSL_EX_23_30 = "אֲגָרְשֶׁ֖נּוּ", "אֲגָ*רְשֶׁ֖*נּוּ", "@Ex 23:30"
_NSL_JUD_11_2 = "וַיְגָרְשׁ֣וּ", "וַיְ*גָרְ*שׁ֣וּ", "@Jud 11:2"
_NSL_PS_34_1 = "וַ֝יְגָרְשֵׁ֗הוּ", "וַ֝יְגָ*רְשֵׁ֗*הוּ", "@Ps 34:1"
_NSL_FSTC_29_20 = (
    "בָּ֥רְכוּ" + sd.NBSP + "נָ֖א",
    "*בָּ֥רְ*כוּ" + sd.NBSP + "נָ֖א",
    "@1C 29:20",
)
_NSL_GEN_27_34 = "בָּרְכֵ֥נִי", "בָּ*רְכֵ֥*נִי", "@Gen 27:34"
_NSL_DAN_4_31 = "בָּרְכֵ֔ת", "*בָּרְ*כֵ֔ת", "@Dan 4:31"
_NSL_GEN_18_21 = "אֵֽרְדָה־נָּ֣א", "אֵֽ*רְדָה־*נָּ֣א", "@Gen 18:21"
_NSL_PS_83_13 = "נִ֣ירְשָׁה לָּ֑נוּ", "נִ֣י*רְשָׁה* לָּ֑נוּ", "@Ps 83:13"
_NSL_JOB_31_37 = "אֲקָֽרְבֶֽנּוּ׃", "אֲקָֽ*רְבֶֽ*נּוּ׃", "@Job 31:37"
_TABLE_1 = hlp.table_std_rtl(
    [
        hlp.norm_and_syl_sep(*_NDL_EX_8_11),
        hlp.norm_and_syl_sep(*_NDL_EX_19_2),
    ]
)
_TABLE_2 = hlp.table_std_rtl(
    [
        hlp.norm_and_syl_sep(*_NDL_JUD_19_17),
        hlp.norm_and_syl_sep(*_NDL_JUD_9_37),
    ]
)
_CONT_TABLE_3_EXCEPT = [
    sub.dol(["Except, in the following word, the $shewa is considered vocal"]),
    sub.dol(
        [
            [" by bA even though the ", sub.shin(), " has ", sub.tsere()],
            [" rather than ", sub.segol(), "."],
        ]
    ),
    sub.dol([" Ben Naftali rejects this exception, considering the $shewa silent."]),
]

_TABLE_3 = hlp.table_std(
    [
        [
            sub.dol(
                [
                    "If the ",
                    sub.shin(),
                    " has ",
                    sub.segol(),
                    ", then a $shewa on the ",
                    sub.resh(),
                    " is vocal.",
                ]
            ),
            hlp.some_hi(_NSL_EX_23_30),
        ],
        [
            [sub.dol(["Otherwise, the $shewa is silent."])],
            hlp.some_hi(_NSL_JUD_11_2),
        ],
        [
            hlp.line_break_seq(_CONT_TABLE_3_EXCEPT),
            hlp.some_hi(_NSL_PS_34_1),
        ],
    ],
    arg_to_troh=["Rules for the root גרשׁ", "Example"],
)
_CONT_TABLE_4_EXCEPT = [
    sub.dol(["Except, in the following word, the $shewa is considered"]),
    sub.dol([" silent even though the accent is on the ", sub.kaf()]),
    sub.dol([" ", hlp.paren(sub.diqduqe_dotan_sec_num(21)), "."]),
    # XXX turn the comment below into a footnote?
    # Does this reference to diqduqe apply to this row,
    # or the whole set of 3 rows (rules)?
]

_TABLE_4 = hlp.table_std(
    [
        [
            sub.dol(
                [
                    "If the accent is on the ",
                    sub.bet(),
                    ", $shewa on the ",
                    sub.resh(),
                    " is silent.",
                ]
            ),
            hlp.some_hi(_NSL_FSTC_29_20),
        ],
        [
            sub.dol(
                [
                    "If the accent is on the ",
                    sub.kaf(),
                    ", $shewa on the ",
                    sub.resh(),
                    " is vocal.",
                ]
            ),
            hlp.some_hi(_NSL_GEN_27_34),
        ],
        [
            hlp.line_break_seq(_CONT_TABLE_4_EXCEPT),
            hlp.some_hi(_NSL_DAN_4_31),
        ],
    ],
    arg_to_troh=["Rules for the root ברך", "Example"],
)
_TABLE_5 = hlp.table_std(
    [
        [hlp.some_hi(_NSL_GEN_18_21), [sub.diqduqe(), "."]],
        # XXX turn the comment below into a footnote?
        # Isn't the above covered by "resh is 2nd letter and has tsere before it," e.g.
        # the מֵרְפִידִ֗ים example above?
        [
            hlp.some_hi(_NSL_PS_83_13),
            "Given as a case of agreement between bA and bN.",
        ],
        [
            hlp.some_hi(_NSL_JOB_31_37),
            [
                "According to bA but not bN. ",
                sub.ms_a_and_l(" and "),
                " have ",
                sub.x_patax(),
                ".",
            ],
        ],
    ],
    arg_to_troh=["", "sources and notes"],
)
SEC = [
    sub.para(
        [
            "Within a word, where $shewa"
            " is marked on"
            " a pair of letters, the first is silent and the second vocal."
            " $Shewa on a letter marked with $dagesh is vocal."
            " Apart from these two clear cases, $shewa"
            " within a word is consider silent,"
            " with the exception of several special categories of $shewa"
            " which are noted in various masoretic sources.",
        ]
    ),
    sub.para_with_initial_uah(
        ["$Shewa on ", sub.resh()],
        [
            ["The Masorah gives rules on the subject of"],
            [" $shewa on ", sub.resh(), ","],
            [" but these are not the same in different sources."],
            [" It is said that in nouns, if ", sub.resh()],
            [" is the second letter, and has"],
            [" ", sub.qamets(), " or ", sub.tsere()],
            [" before it, then a $shewa on the ", sub.resh()],
            [" is vocal. E.g.:"],
        ],
    ),
    _TABLE_1,
    sub.para(
        [
            "If it has ",
            sub.xireq(),
            " or ",
            sub.xolem(),
            " before it, however, $shewa on the ",
            sub.resh(),
            " is silent. E.g.:",
        ]
    ),
    _TABLE_2,
    sub.para_paren(
        [
            "From ",
            hlp.hbo(_NDL_JUD_9_37[0]),
            " above, we now see that the real criteria is that ",
            sub.resh(),
            " is the second letter excluding any vowel letter ",
            hlp.paren(sub.mater_lectionis()),
            ".",
        ]
    ),
    sub.para(
        [
            "Rules on $shewa on ",
            sub.resh(),
            " in verb forms are given for the roots גרשׁ and ברך.",
        ]
    ),
    _TABLE_3,
    _TABLE_4,
    sub.para(
        [
            "$Shewa on ",
            sub.resh(),
            " is considered vocal also in the following:",
        ]
    ),
    _TABLE_5,
]
