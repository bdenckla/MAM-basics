import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_FTNT_0 = sub.footnote(
    [
        "E.g. ",
        hlp.hboloc("בִישְׂרָאֵ֗ל", "@Gen 34:7"),
        sub.thspc(),
        " ",  # MAM has בְיִשְׂרָאֵ֗ל, as expected
        hlp.hboloc("כִּישְׂרָאֵ֔ל", "@2S 7:23"),
        sub.thspc(),
        " ",  # MAM has כְּיִשְׂרָאֵ֔ל, as expected
        hlp.hboloc("לִישְׂרָאֵ֗ל", "@Ho 7:1"),
        sub.thspp(),  # MAM has לְיִשְׂרָאֵ֗ל, as expected
    ]
)
_FTNT_1 = sub.footnote(
    [
        "Here $itm gives the locale Jud 19:16 for ",
        hlp.hbo("וִיטַ֥ב"),
        " but I do not find it (or anything close to it) there. I found ",
        hlp.hbo("וְיִטַ֥ב"),
        " in 2K 25:24 so that is what I use above (with vowel adjustments).",
    ]
)
_TABLE_1_DATA = [
    [hlp.lhbo("@Jer 25:36", "וִֽילֲלַ֖ת")],  # MAM has simple shewa (with varika?)
    [hlp.lhbo("@Prov 30:17", "לִֽיקְּהַ֫ת־אֵ֥ם")],
    [hlp.lhbo("@Qoh 2:13", "כִּֽיתֲר֥וֹן"), sub.ms_s1_1053()],
    # MAM has simple shewa (with varika?)
]
_TABLE_1 = hlp.table_std(_TABLE_1_DATA, coldirs=["rtl", "ltr"])
SEC = [
    sub.para(
        [
            "According to the rules given in ",
            hlp.rtn(387),
            ", initial $simshewa before ",
            sub.yod(),
            " should sound like an ultra-short ",
            sub.xireq(),
            ". This includes cases where the ",
            sub.yod(),
            " has ",
            sub.xireq(),
            ". E.g., ",
            hlp.hbo("לְיִשְׂרָאֵל"),
            " should sound like /lĭyiśrɔʾel/."
            " However, /ĭyi/ is likely to develop into a single long /i/ vowel,"
            " e.g. /līśrɔʾel/,"
            " and this gave rise to a systematic"
            " variation between ben Asher and ben Naftali."
            " Ben Asher admits the long /i/ in only three words:",
        ]
    ),
    _TABLE_1,
    sub.para(
        [
            ["In these cases the $shewa after the ", sub.yod()],
            [" is vocal, so that the ", sub.xireq()],
            [" occurs in an open syllable."],
            [" In all other cases, bA marks the two vowels"],
            [" ($shewa and ", sub.xireq(), ")"],
            [" separately."],
            [" In contrast, bN requires the single long /i/ vowel"],
            [" in these cases:"],
        ]
    ),
    sub.unordered_list(
        [
            [
                "All prefixed versions of the following four words with exactly one prefix,"
                " where that prefix is the preposition ",
                sub.rom_bkl(),
                ":",
                sub.unordered_list(
                    [
                        [hlp.hbo("יִשְׂרָאֵל"), " ", _FTNT_0],
                        hlp.hbo("יִזְרְעֶאל"),
                        hlp.hbo("יִרְאָה"),
                        hlp.hbo("יִרְאַת"),
                    ]
                ),
            ],
            [
                "Some other specific words, such as:",
                sub.unordered_list(
                    [
                        [hlp.lhbo("@2K 25:24", "וִיטַ֥ב"), " ", _FTNT_1],
                        [
                            hlp.lhbo("@Ps 119:38", "לִירְאָתֶֽךָ׃")
                        ],  # MAM has לְיִרְאָתֶֽךָ׃
                        [hlp.lhbo("@Job 29:21", "וִיחֵ֑לּוּ")],  # MAM has וְיִחֵ֑לּוּ
                    ]
                ),
            ],
        ]
    ),
    sub.para(
        [
            "In all other cases,"
            " Ben Naftali does not require the long /i/ vowel, and so agrees with bA."
            " Notable cases of agreement include words that start in the following two ways:"
        ]
    ),
    sub.unordered_list(
        [
            [
                "With exactly one prefix, where that prefix is not a בכל prefix."
                " E.g., ",
                hlp.hbo("וְיִשְׂרָאֵל"),
                sub.thspp(),
            ],
            ["With two prefixes. E.g., ", hlp.hbo("וּבְיִשְׂרָאֵל"), sub.thspp()],
        ]
    ),
]
