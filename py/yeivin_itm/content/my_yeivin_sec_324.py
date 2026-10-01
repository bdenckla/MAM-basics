import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_LEV_AND_DT = hlp.make_dloc("@Lev 11:4", "@Dt 14:7")  # also used in 320
_SNDS_AND_FSTC = hlp.make_dloc("@2S 23:16", "@1C 11:18")
_ISE_DT_5_22 = "@Dt 5:22"  # 5:18 in MAM
_GAYA_ON_THE_4TH = "$gaya on the fourth syllable before the stress"
_GAYA_ON_THE_3RD = "$gaya on the third syllable before the stress"
_GAYA_ON_THE_2ND = "$gaya on the second syllable before the stress"
_GAYA_ON_THE_1ST = "$gaya on the syllable right before the stress"
_TABLE_1 = hlp.table_std_rtl(
    [
        [*hlp.lns("@Dt 12:2", "אֶֽת־כׇּל־הַמְּקֹמ֞וֹת", "אֶֽת־-כׇּל־-הַ_-מְּקֹ-מ֞וֹת")],
        ["", "4", "3", "2", "1", ""],
    ]
)
_TABLE_2 = hlp.table_std_rtl(
    [
        hlp.lns("@Jos 13:3", "מִֽן־הַשִּׁיח֞וֹר", "מִֽן־-הַ_-שִּׁי-ח֞וֹר"),
        hlp.lns("@Jud 18:2", "מִֽמִּשְׁפַּחְתָּ֡ם", "מִֽ_-מִּשְׁ-פַּחְ-תָּ֡ם"),
        hlp.lns(_LEV_AND_DT, "אֶֽת־הַ֠גָּמָ֠ל", "אֶֽת־-הַ֠_-גָּ-מָ֠ל"),
        hlp.lns("@Gen 17:20", "וּֽלְיִשְׁמָעֵאל֮", "וּֽלְ-יִשְׁ-מָ-עֵאל֮"),
    ]
)
_TABLE_3 = hlp.table_std_rtl(
    [
        [*hlp.lns("@1S 1:4", "וּֽלְכׇל־בָּנֶ֛יהָ", hlp.sy5("וּֽלְ-כׇל־-בָּ-נֶ֛י-הָ"))],
        [*hlp.lns("@Ex 15:20", "כׇֽל־הַנָּשִׁים֙", hlp.sy5pe("כׇֽל־-הַ_-נָּ-שִׁים֙"))],
    ]
)
_TABLE_4 = hlp.table_std_rtl(
    [
        [*hlp.lns(_ISE_DT_5_22, "אֶֽת־הַדְּבָרִ֣ים", "אֶֽת־-הַ_-דְּבָ-רִ֣ים")],
        [*hlp.lns("@Gen 9:10", "וּֽבְכׇל־חַיַּ֥ת", "וּֽבְ-כׇל־-חַ-יַּ֥ת")],
    ]
)
_TABLE_5 = hlp.table_std_rtl(
    [
        hlp.lns("@Jer 11:9", "נִֽמְצָא־קֶ֙שֶׁר֙", hlp.sy5ps("נִֽמְ-צָא־-קֶ֙-שֶׁר֙")),
        [
            *hlp.lns(
                hlp.make_aeloc("@Lev 23:21"),
                "מִֽקְרָא־קֹ֙דֶשׁ֙",
                hlp.sy5ps("מִֽקְ-רָא־-קֹ֙-דֶשׁ֙"),
            )
        ],
        hlp.lns(
            _SNDS_AND_FSTC,
            "וַיִּֽשְׁאֲבוּ־מַ֙יִם֙",
            hlp.sy5("וַ_-יִּֽשְׁ-אֲבוּ־-מַ֙-יִם֙"),
        ),
    ]
)
_TABLE_6 = hlp.table_std_rtl(
    [
        hlp.lns("@Ex 17:6", "עַֽל־הַצּוּר֮", hlp.sy4ps("עַֽל־-הַ-צּוּר֮")),
        hlp.lns(
            hlp.make_dloc("@Jos 11:4", "@1S 13:5"),
            "עַל־שְׂפַֽת־הַיָּ֖ם",
            hlp.sy4("עַל־-שְׂפַֽת־-הַ-יָּ֖ם"),
        ),
        hlp.lns("@Dt 9:2", "עַֽם־גָּד֥וֹל", hlp.sy4ps("עַֽם־-גָּ-ד֥וֹל")),
    ]
)
_TABLE_7 = hlp.table_std_rtl(
    [
        [*hlp.lns("@Ez 42:1", "וַאֲשֶֽׁר־נֶ֥גֶד", hlp.sy4("וַ-אֲשֶֽׁר־-נֶ֥-גֶד"))],
        [*hlp.lns("@Jud 18:22", "נִֽזְעֲק֔וּ", hlp.sy4pspe("נִֽזְ-עֲק֔וּ"))],
        [*hlp.lns("@2C 30:11", "נִֽכְנְע֔וּ", hlp.sy4pspe("נִֽכְ-נְע֔וּ"))],
        [
            *hlp.lns("@1S 30:28", "בְּשִֽׂפְמ֖וֹת", hlp.sy4pspe("בְּשִֽׂפְ-מ֖וֹת"))
        ],  # SGASS פְ
        [*hlp.lns("@Ho 10:14", "שַֽׁלְמַ֛ן", hlp.sy4pspe("שַֽׁלְ-מַ֛ן"))],  # SGASS לְ
        [*hlp.lns("@Gen 1:11", "תַּֽדְשֵׁ֤א", hlp.sy4pspe("תַּֽדְ-שֵׁ֤א"))],  # SGASS דְ
        [
            *hlp.lns("@2S 22:17", "יַֽמְשֵׁ֖נִי", hlp.sy4ps("יַֽמְ-שֵׁ֖-נִי"))
        ],  # SGASS מְ
        # "SGASS X" means "syllable grouping assumes silent shewa in X"
        # e.g. "SGASS פְ" means "syllable grouping assumes silent shewa in פְ"
    ]
)
SEC = [
    sub.para(
        [
            "The most common use of $gaya_cs is in words of regular structure. "
            # XXX turn the comment below into a footnote?
            # I moved the above sentence here from Section 323 because
            # that section is about words with irregular structure so it didn't make sense to me there.
            "Words with structure which is non-regular",
            sub.emdash(),
            "i.e. words that are not patterned like ",
            hlp.hbo(sub.pat_mitqatlim()[0]),
            " or its variants described above",
            sub.emdash(),
            # removed spurious close paren between "above" and em dash
            "rarely show $gaya_cs. There are no fixed rules for the use of $gaya on such words.",
        ]
    ),
    sub.para(["1) In some 15 cases there is a ", _GAYA_ON_THE_4TH, ". E.g.:"]),
    _TABLE_1,
    sub.para(
        [
            "2) In some 200 cases there is a ",
            _GAYA_ON_THE_3RD,
            ". This occurs mainly when the accent is one of the “high” trilled disjunctives ",
            hlp.rtn_p(195),
            ". E.g., with ",
            sub.gershayim(),
            ", ",
            sub.pazer(),
            ", ",
            sub.telisha_gedolah(),
            ", and ",
            sub.zarqa(),
            ":",
        ]
    ),
    _TABLE_2,
    sub.para(
        [
            "However, ",
            _GAYA_ON_THE_3RD,
            " may occur with other disjunctives, as with ",
            sub.tevir(),
            " and $pashta below:",
        ]
    ),
    _TABLE_3,
    sub.para(
        [
            "And ",
            _GAYA_ON_THE_3RD,
            " may even occur with conjunctives, as with ",
            sub.munax(),
            " and ",
            sub.merka(),  # translit-ok
            " below:",
        ]
    ),
    _TABLE_4,
    sub.para(
        [
            "3) In some 30 cases there is a ",
            _GAYA_ON_THE_2ND,
            sub.emdash(),
            "most commonly on a word with penultimate stress marked with $pashta. E.g.:",
        ]
    ),
    _TABLE_5,
    sub.para(["However, ", _GAYA_ON_THE_2ND, " also occurs with other accents. E.g.:"]),
    _TABLE_6,
    sub.para(
        [
            "This category has a number of words in which"
            " the $gaya could be classified as phonetic ",
            hlp.rtn_p(350),
            ".",
        ]
    ),
    sub.para(
        [
            "4) In some 60 cases there is a ",
            _GAYA_ON_THE_1ST,
            ". In this position $gaya",
            " is rarely marked for musical reasons. E.g.:",
        ]
    ),
    _TABLE_7,
    sub.para(
        [
            "A ",
            _GAYA_ON_THE_1ST,
            " is usually marked for phonetic reasons ",
            hlp.rtn_p(350),
            " and this may be the case even in some of the examples given above.",
        ]
    ),
]
