import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub
import mb_cmn.str_defs as sd


def _subsec_for_table_1():
    _HBO_STR_NU_25_8 = "אֶל־קֳבָתָ֑הּ"
    ftnt = sub.footnote(
        [
            "In $itm, ",
            hlp.hbo(_HBO_STR_NU_25_8),
            " has no accent. (I show ",
            sub.atnax(),
            ".)",
        ]
    )
    _data_rows_for_table_1 = [
        [hlp.hbo_varacc("דֳּמִי")],
        [hlp.hbo_varacc("צֳרִי")],
        [hlp.hbo_varacc("קֳבֵל")],
        [hlp.hbo_varacc("קֳדָם")],
        [hlp.lhbo("@Nu 25:8", _HBO_STR_NU_25_8), ftnt],
        [hlp.lhbo("@2K 12:19", "וְאֶת־קֳדָשָׁ֔יו")],
    ]
    return hlp.table_std(_data_rows_for_table_1, coldirs=["rtl", "ltr"])


def _subsec_for_intro_for_table_2():
    ftnt = sub.footnote(
        [
            "It is no coincidence that in all the examples below,"
            " this full vowel would be interpreted as ",
            sub.qamets_x_paren_qamets_q(),
            ", and indeed that is how we show it below"
            " (with the characteristic taller shape"
            " used in some recent printed texts"
            " but of course not present in any manuscript tradition).",
        ]
    )
    return sub.para(
        [
            "At the start of a word, with a full vowel ",
            hlp.ftntjoin("sign", ftnt),
            " rather than $xatef (see Dotan, 1972, p. 241–247):",
        ]
    )


def _subsec_for_table_2():
    ftnt = sub.footnote(sub.superfluous_waw("סובאים", "סׇבָאִ֖ים"))
    data_rows_for_table_2 = [
        [hlp.hbo_varacc("קׇדָשִׁים")],
        # Above is the first of many qamats qatan marks in this file.
        [hlp.hbo_varacc("קׇדָמוֹהִי")],
        # MAM has gaʿya on ק in all 3 instances of this I find:
        # Dan 4:5 קׇֽדָמ֥וֹהִי
        # Dan 6:19 קׇֽדָמ֑וֹהִי
        # Dan 6:23 קׇֽדָמ֙וֹהִי֙
        [hlp.lhbo("@1K 12:10", "קׇטׇנִּ֥י")],
        [hlp.lhbo("@Ez 26:9", "קׇבׇלּ֔וֹ")],  # MAM has gaʿya on ק, i.e. קׇֽבׇלּ֔וֹ
        [hlp.lhbo("@2K 15:10", "קׇבׇל־עָ֖ם")],  # MAM has gaʿya on ק, i.e. קׇֽבׇל־עָ֖ם
        [hlp.hbo_varacc("שׇׁרָשָׁיו")],
        [hlp.lhbo("@Ez 23:42", "סׇובָאִ֖ים"), ftnt],
    ]
    return hlp.table_std_rtl(data_rows_for_table_2)


def _subsec_for_table_4():
    ftnt_0 = sub.footnote(sub.superfluous_waw("ואשקולה", "וָאֶשְׁקֳלָ֣ה"))
    hboloc_args_2s = "קׇדְקֳד֔וֹ", "@2S 14:25"
    ftnt_1 = sub.footnote(
        [
            "Here $itm gives no locale for ",
            hlp.hbo(hboloc_args_2s[0]),
            sub.thspp(),
            " I find it (only) at ",
            hlp.isolated_slocale(hboloc_args_2s[1]),
            ".",
        ]
    )
    data_rows_for_table_4 = [
        ["", hlp.lhbo("@Nu 35:20", "יֶהְדֳּפֶ֑נּוּ")],
        [
            ftnt_0,
            hlp.lhbo("@Ezra 8:25", "וָאֶשְׁקֳולָ֣ה"),
            "but",
            hlp.lhbo(
                "@Ezra 8:26", "וָאֶשְׁקֲלָ֨ה"
            ),  # MAM has simple shewa on ק, i.e. וָאֶשְׁקְלָ֨ה
        ],
        [ftnt_1, hlp.hboloc(*hboloc_args_2s)],
        [
            "",
            hlp.lhbo("@Jud 8:7", "הַבַּרְקֳנִֽים׃"),
        ],  # MAM has gaʿya on ה, i.e. הַֽבַּרְקֳנִֽים׃
        ["", hlp.hbo_varacc("מׇרְדֳּכַי")],
    ]
    return hlp.table_std(data_rows_for_table_4, coldirs=["ltr", "rtl", "ltr", "rtl"])


_DATA_ROWS_FOR_TABLE_3 = [
    [hlp.lhbo("@Is 27:3", "אֶצֳּרֶֽנָּה׃")],
    [hlp.lhbo("@Nu 23:25", "תִקֳּבֶ֑נּוּ")],
    [hlp.lhbo("@Ex 28:40", "כֻתֳּנֹ֔ת")],
    [hlp.lhbo("@Joel 2:24", "הַגֳּרָנ֖וֹת")],
    [
        hlp.hbo_varacc("שִׁבֳּלִים"),
        "but",
        hlp.lhbo(
            "@Zech 4:12", "שִׁבֲּלֵ֣י"
        ),  # MAM has simple shewa on ב, i.e. שִׁבְּלֵ֣י
    ],
    [
        hlp.hbo_varacc("צִפֳּרִים"),
        "but Aramaic",
        hlp.lhbo("@Dan 4:9", "צִפֲּרֵ֣י"),  # MAM has simple shewa on פ, i.e. צִפְּרֵ֣י
    ],
    [hlp.lhbo("@Is 9:3", "סֻבֳּל֗וֹ")],
]
SEC = [
    sub.para(
        [
            "Only on gutturals does Tiberian pointing regularly distinguish"
            " $vocshewa from $silshewa.",
            " In many cases, however, $shewa on other letters is represented by"
            " $xatef to indicate that it is vocal, in some",
            sub.emdash(),
            "sometimes in most",
            sub.emdash(),
            "of the"
            " manuscripts and printed texts."
            " This may occur either for morphological or for phonetic reasons."
            " This section and the next few will cover these two reasons:",
        ]
    ),
    sub.ordered_list_with_lcromnum(
        [
            sub.cmn_388_lcromnum_i(),
            sub.cmn_388_lcromnum_ii(),
        ]
    ),
    sub.para_with_romnum_and_initial_uah(
        "i",
        sub.cmn_388_lcromnum_i(),
        [
            "This occurs most commonly where the $shewa"
            " derives from an /o/ or /u/ vowel, in which case the sign used is ",
            sub.x_qamets(),
            ". This is especially common on ",
            sub.qof(),
            ", ",
            sub.gimel(),
            ", the other ",
            sub.begad_kefat(),
            " letters, ",
            sub.tet(),
            ", and the sibilants ",
            sub.tsade(),
            " and ",
            sub.shin(),
            ". Presumably the"
            " tendency to preserve the original /o/ or /u/ sound was greater with"
            " them than with other letters."
            " E.g.:",
        ],
    ),
    sub.para(["At the start of a word, with $xatef", sub.hairsp(), ":"]),
    # Above, is nowrap needed?
    _subsec_for_table_1(),
    _subsec_for_intro_for_table_2(),
    _subsec_for_table_2(),
    sub.para(["Within a word", sub.emdash(), "on a letter with $dagesh:"]),
    hlp.table_std(_DATA_ROWS_FOR_TABLE_3, coldirs=["rtl", "ltr", "rtl"]),
    sub.para(["On the second of a pair of letters with $shewa:"]),
    _subsec_for_table_4(),
]
