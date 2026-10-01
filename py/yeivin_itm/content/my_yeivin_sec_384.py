import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_FOO1 = "נִ֥בְהָֽל לַה֗וֹן", "נִ֥*בְהָֽל* לַה֗וֹן", "@Prov 28:22"
_FOO2 = "קִ֥רְבַ֥ת אֱלֹהִ֗ים", "קִ֥*רְבַ֥ת* אֱלֹהִ֗ים", "@Ps 73:28"
_FOO3 = "תִּ֥בְחַ֣ר וּתְקָרֵב֮", "תִּ֥*בְחַ֣ר* וּתְקָרֵב֮", "@Ps 65:5"
_FOO4 = "שִׁ֥מְעָֽה תְפִלָּתִ֨י׀", "שִׁ֥*מְעָֽה* תְפִלָּתִ֨י׀", "@Ps 39:13"
_FOO5 = "וְלִ֥שְׁכֵנַ֨י׀", "וְלִ֥*שְׁכֵ*נַ֨י׀", "@Ps 31:12"
_FTNT_PS_31_12 = sub.footnote(
    [
        "This example, ",
        hlp.hbo(_FOO5[0]),
        sub.thspc(),
        ""
        " does not seem to fit the sequence being discussed."
        " In particular, to fit the sequence, the accent, ",
        sub.azla(),
        ", would need to be on ",
        sub.kaf(),
        ", the letter right after the ",
        sub.merka(),  # translit-ok
        " and $shewa part of the sequence."
        " I.e. to fit the sequence, the word would need to be ",
        hlp.hbo("וְלִ֥שְׁכֵ֨נַי׀"),
        " rather than ",
        hlp.hbo(_FOO5[0]),
        sub.thspp(),
    ]
)
_TABLE_1 = hlp.table_std_rtl(
    [
        [hlp.some_hi(_FOO1)],
        [hlp.some_hi(_FOO2)],
        [hlp.some_hi(_FOO3)],
        [hlp.some_hi(_FOO4)],
        [[hlp.some_hi(_FOO5), " ", _FTNT_PS_31_12]],
    ]
)
_TABLE_2 = hlp.table_std_rtl(
    [
        [hlp.some_hi(("שָׁ֥בְרָ֥ה לִבִּ֗י", "*שָׁ֥בְ*רָ֥ה לִבִּ֗י", "@Ps 69:21"))],
        [
            hlp.some_hi(("שׇׁ֥מְרָ֣ה נַפְשִׁי֮", "*שׇׁ֥מְ*רָ֣ה נַפְשִׁי֮", "@Ps 86:2"))
        ],  # qamats qatan
        [hlp.some_hi(("טָ֥מְנֽוּ־גֵאִ֨ים׀", "*טָ֥מְ*נֽוּ־גֵאִ֨ים׀", "@Ps 140:6"))],
        [hlp.some_hi(("יִ֥רְאַ֣ת יְהֹוָה֮", "*יִ֥רְ*אַ֣ת יְהֹוָה֮", "@Prov 8:13"))],
    ]
)
SEC = [
    sub.para_with_initial_uah(
        ["$Shewa in a Particular Poetic Sequence"],
        [
            "$Shewa is vocal in the following sequence particular to the three books:",
        ],
    ),
    sub.unordered_list(
        [
            [sub.merka(cap=True), "."],  # translit-ok
            "$Shewa.",
            "Either the main accent or $gaya.",
        ]
    ),
    sub.para(
        [
            "This sequence occurs mainly among the servi of ",
            sub.revia_gadol(),
            " ",
            hlp.rtn_p(363),
            ", ",
            sub.revia_qatan(),
            " ",
            hlp.rtn_p(368),
            ", ",
            sub.tsinnor(),
            " ",
            hlp.rtn_p(365),
            ", and ",
            sub.legarmeh(),
            " ",
            hlp.rtn_p(370),
            ". According to the ",
            sub.diqduqe_dotan_sec_num(13),
            ", the $shewa is vocal. E.g.:",
        ]
    ),
    _TABLE_1,
    sub.para(
        [
            "There are four exceptions in which $shewa in this sequence is silent:",
        ]
    ),
    _TABLE_2,
]
