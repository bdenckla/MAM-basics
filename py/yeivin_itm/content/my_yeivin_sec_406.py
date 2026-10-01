import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_HBOLOC_ARGS_EX_25_29 = "וְעָשִׂ֨יתָ קְּעָרֹתָ֜יו", "@Ex 25:29"
_HBOLOC_EX_25_29 = hlp.hboloc(*_HBOLOC_ARGS_EX_25_29)
_AB_EX_25_29 = hlp.alpha_beta(*_HBOLOC_ARGS_EX_25_29)
_EX_25_29_STR_WITH_GAYA = "וְעָשִׂ֨יתָ קְּעָֽרֹתָ֜יו"
_FTNT_EX_25_29 = sub.footnote(
    [
        "I’m not clear why $itm lists ",
        _HBOLOC_EX_25_29,
        " as an example here. Unlike the other examples listed here, it lacks the $gaya",
        " under discussion. Perhaps it is listed here only because it ",
        hlp.emphasis("could"),
        " have such a $gaya? I.e. perhaps it is listed here only because ",
        hlp.hbo(_EX_25_29_STR_WITH_GAYA),
        " is possible?"
        " It is also unlike the other examples in that its first syllable starts with a $shewa."
        " But that makes it stand out from the other examples far less than its lack of $gaya."
        " In $itm, this example is introduced by “also,”"
        " which is atypical in lists of examples in $itm."
        " Perhaps this “also” subtly acknowledges these issues?",
    ]
)
_DATA_FOR_TABLE_1 = [
    [
        *hlp.alpha_beta(
            "וְיָרֵ֥אתָ מֵּֽאֱלֹהֶ֖יךָ", hlp.make_dloc("@Lev 19:14", "@Lev 19:32")
        )
    ],
    # MAM lacks the gaʿya in question, i.e. MAM has וְיָרֵ֥אתָ מֵּאֱלֹהֶ֖יךָ
    [*hlp.alpha_beta("וְעָשִׂ֤יתָ סִּֽירֹתָיו֙", "@Ex 27:3")],
    [*hlp.alpha_beta("צָפַ֢נְתָּ לִּֽירֵ֫אֶ֥יךָ", "@Ps 31:20")],
    # MAM lacks the gaʿya in question, i.e. MAM has צָפַ֢נְתָּ לִּירֵ֫אֶ֥יךָ
    [*hlp.alpha_beta("עָשִׂ֤יתָ לִּֽירִיחוֹ֙", "@Jos 8:2")],
    [_AB_EX_25_29[0], [_AB_EX_25_29[1], " ", _FTNT_EX_25_29]],
]
_DATA_FOR_TABLE_2 = [
    ("שָׁ֣מָּה קָֽבְר֞וּ", "@Gen 49:31"),
    ("אָשִׁ֤ירָה לַֽיהֹוָה֙", "@Ex 15:1"),
    ("וְכִעֲסַ֤תָּה צָֽרָתָהּ֙", "@1S 1:6"),
    # MAM lacks the gaʿya in question, i.e. MAM has וְכִעֲסַ֤תָּה צָרָתָהּ֙
    # UXLC has it; does LC in fact have it?
    # Yes, LC has it. See https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F150A.jpg
    # column 3 line 24 of 27.
    ("כּוֹנַ֣נְתָּ מֵֽישָׁרִ֑ים", "@Ps 99:4"),
    # MAM lacks the gaʿya in question, i.e. MAM has כּוֹנַ֣נְתָּ מֵישָׁרִ֑ים
]
SEC = [
    sub.para(
        [
            "Some scholars ",
            hlp.paren([sub.yequtiel_hn(), ", Heidenheim, Baer"]),
            " state that $dexiq is used not only where the first syllable of β"
            " is stressed, but also where that syllable has $gaya_osr",
            " ",
            hlp.rtn_p(326),
            ". In the early manuscripts, $dexiq is used in a few such situations. E.g.:",
        ]
    ),
    hlp.table_std_alpha_beta_2col(_DATA_FOR_TABLE_1),
    sub.para(
        [
            "As a general rule, however, the $dexiq is absent"
            " if the first syllable of the word could have $gaya. E.g.:",
        ]
    ),
    hlp.table_std_alpha_beta_2col_std(_DATA_FOR_TABLE_2),
    sub.para(["Literature. Baer 1880, Dotan, 1969."]),
]
