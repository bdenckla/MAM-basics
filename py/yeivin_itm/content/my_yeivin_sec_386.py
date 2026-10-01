import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_MSS_L_C_S1 = sub.ms_lenin(), ", ", sub.ms_cairo(), ", ", sub.ms_s1_1053()
_CF_1S_28_8 = hlp.compare_with(_MSS_L_C_S1, "קָֽסֳומִי־")
_CF_PS_74_5 = hlp.compare_with(sub.ms_lenin(), "בִּֽסֲבׇךְ־")
# Above is the first of many qamats qatan marks in this file.


_TABLE_1_DATA = [
    [hlp.some_hi(("וּקְטׇרְתִּ֔י", "*וּקְ*טׇרְתִּ֔י", "@Ez 16:18")), "bA"],
    [hlp.some_hi_no_loc(("וּֽקֲטׇרְתִּ֔י", "וּֽ*קֲטׇרְ*תִּ֔י")), "bN and “Tiberias”"],
    # XXX is the shewa in רְ vocal or silent?
    # Not critical to the point at hand, but would be nice to know.
]
_FTNT_FOR_TABLE_2 = sub.footnote(sub.superfluous_waw("קסומי", "קׇסֳמִי־"))
_TABLE_2_DATA = [
    [hlp.some_hi(("כִּקְסׇום־שָׁוְא֙", "*כִּקְ*סׇום־שָׁוְא֙", "@Ez 21:28")), "bA"],
    [hlp.some_hi_no_loc(("כִּֽקֲסׇום־שָׁוְא֙", "כִּֽ*קֲסׇום־*שָׁוְא֙")), "bN"],
    [hlp.some_hi_no_loc(("כִּֽקֳסׇום־שָׁוְא֙", "כִּֽ*קֳסׇום־*שָׁוְא֙")), "R. Pinḥas"],
]
_TABLE_3A_DATA = [
    [hlp.lhbo("@Ez 28:13", "וּבָרֲקַ֖ת"), sub.ms_s1_1053()],
    [hlp.lhbo("@Ps 22:27", "דֹּ֣רֲשָׁ֑יו"), sub.ms_s1_1053()],
]
_A_S1 = sub.ms_a_and_s1()
_TABLE_3B_DATA = [
    [hlp.lhbo("@Joel 3:3", "וְתִֽימֲר֖וֹת"), sub.ms_aleppo()],
    [hlp.lhbo("@Dt 32:36", "אָ֣זֲלַת"), _A_S1],
    [hlp.lhbo("@Dan 4:33", "ה֥וּסֲפַת לִֽי׃"), sub.ms_s1_1053()],
]


def _table_3c_data():
    ftnt = sub.footnote(sub.superfluous_waw("כקסום", "כִּקְסׇם־"))
    return [
        [hlp.lhbo("@1S 28:8", "קׇסֳומִי־נָ֥א"), sub.ms_aleppo(), _CF_1S_28_8, ftnt],
        [hlp.lhbo("@Ps 74:5", "בִּסֲבׇךְ־עֵ֝֗ץ"), sub.ms_aleppo(), _CF_PS_74_5, ""],
    ]


SEC = [
    sub.para(
        [
            "In addition to these rules, a number of cases of ",
            sub.xillufim(),
            " also concern the pronunciation of $shewa within the word. E.g.:",
        ]
    ),
    hlp.table_std(_TABLE_1_DATA, coldirs=["rtl", "ltr"]),
    sub.para([hlp.ftntjoin("And:", _FTNT_FOR_TABLE_2)]),
    hlp.table_std(_TABLE_2_DATA, coldirs=["rtl", "ltr"]),
    sub.para(
        [
            "The manuscripts also show some other words, not mentioned in the"
            " rules given above, in which a $x_shewa is used where a",
            " $silshewa is expected. E.g.:",
        ]
    ),
    sub.para(["On ", sub.resh(), ":"]),
    hlp.table_std(_TABLE_3A_DATA, coldirs=["rtl", "ltr", "ltr"]),
    sub.para(["After $gaya or an accent sign on a long vowel:"]),
    hlp.table_std(_TABLE_3B_DATA, coldirs=["rtl", "ltr", "ltr"]),
    sub.para("After a short vowel with no $pgaya:"),
    hlp.table_std(_table_3c_data(), coldirs=["rtl", "ltr", "ltr", "ltr"]),
    sub.para(
        [
            "It seems probable that, although the rules given above"
            " cover most of the cases in which $shewa"
            " within a word was"
            " considered vocal, they do not cover them all."
            " Apart from those"
            " cases mentioned in the rules, however, and the few exceptional"
            " cases, $shewa"
            " within a word was considered silent, whether it"
            " came after either of the following:",
        ]
    ),
    sub.unordered_list(
        [
            [
                "a short vowel, as ",
                hlp.some_hi(("וַיִּשְׁלַ֤ח", "וַ*יִּשְׁ*לַ֤ח", "@Gen 8:9")),
            ],
            [
                "a long vowel (even if it had $mgaya) as ",
                hlp.some_hi(("שָֽׁמְע֔וּ", "*שָֽׁמְ*ע֔וּ", "@Gen 43:25")),
            ],
        ]
    ),
]
