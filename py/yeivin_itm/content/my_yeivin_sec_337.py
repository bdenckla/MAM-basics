import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_TABLE_1 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Ho 8:7", "אֵֽין־ל֗וֹ")],
        [hlp.lhbo("@Jud 17:7", "גָֽר־שָֽׁם׃")],
        [hlp.lhbo("@Jos 12:16", "בֵּֽית־אֵ֖ל")],
        [hlp.lhbo("@2K 4:26", "רֽוּץ־נָ֣א")],
    ]
)
_TABLE_2 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Gen 41:45", "שֵׁם־יוֹסֵף֮")],
        [hlp.lhbo("@Jos 23:6", "סוּר־מִמֶּ֖נּוּ")],
        [hlp.lhbo("@Jos 15:41", "בֵּית־דָּג֥וֹן")],
        [hlp.lhbo("@Jos 3:3", "בְּרִית־יְהֹוָה֙")],
    ]
)
_TABLE_3 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Jos 9:7", "אִֽישׁ־יִשְׂרָאֵ֖ל")],
        [hlp.lhbo("@Rut 2:23", "קְצִֽיר־הַשְּׂעֹרִ֖ים")],
        [hlp.lhbo(hlp.make_aeloc("@Jud 2:5"), "שֵֽׁם־הַמָּק֥וֹם")],
    ]
)
_PARA_1_OF_FTNT = sub.para(
    [
        "In the heading that precedes this section, we added the $maqqef qualification; ",
        "$itm simply refers to a closed syllable.",
        " But, given the contents of this section, we feel that the $maqqef",
        " qualification is justified and helpful. We similarly added this qualification in ",
        hlp.rtn(317),
        ".",
    ]
)
_PARA_2_OF_FTNT = sub.para(
    [
        hlp.paren(
            [
                "By ",
                hlp.dquotes(sub.maqclo()),
                " we mean having, before a $maqqef, what is referred to in ",
                hlp.rtn(376),
                " as a potential $shewa.",
            ]
        ),
    ]
)
_PARA_3_OF_FTNT = sub.para(
    [
        ["$Gaya on a ", sub.sclv(), " syllable"],
        [" is covered in ", hlp.rtn(326), ". "],
    ]
)
_FTNT = sub.footnote(
    [
        _PARA_1_OF_FTNT,
        _PARA_2_OF_FTNT,
        _PARA_3_OF_FTNT,
    ]
)
SEC = [
    sub.para(
        [
            "$Gaya may be marked in a closed syllable with a long vowel.",
            " In Hebrew such syllables usually have the accent,",
            " and when they do not have the accent they usually have $maqqef.",
            " In this last situation, $gaya",
            " may be marked before either a disjunctive or a conjunctive accent",
            hlp.ftntjoin(".", _FTNT),
        ]
    ),
    sub.para(
        [
            "This $gaya is marked regularly in most printed texts, but"
            " in manuscripts it is usually marked only if the candidate syllable"
            " comes right before the stress syllable. E.g.:",
        ]
    ),
    _TABLE_1,
    sub.para(
        "If the candidate syllable is the second before the stress,"
        " $gaya is usually not marked. E.g.:"
    ),
    _TABLE_2,
    sub.para(
        "If the candidate syllable is the third before the stress, $gaya"
        " is more likely to be marked. E.g.:",
    ),
    _TABLE_3,
    sub.para(
        "In general the use of this $gaya"
        " in the early manuscripts is more regular than the use of $gaya_os,"
        " but less regular than the use of $gaya_cs of the regular type."
        " However, the regularity varies from manuscript to manuscript."
    ),
]
