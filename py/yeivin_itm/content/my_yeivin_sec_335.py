import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_TABLE_1 = hlp.table_std_rtl(
    [[hlp.lhbo("@Ez 34:10", "אא֨א אא֜א וְֽדָרַשְׁתִּ֧י אא֣א אא֗א")]]
)
_TABLE_2 = hlp.table_std_rtl([[hlp.lhbo("@2K 25:19", "אֲֽשֶׁר־ה֥וּא אא֣א׀")]])
_TABLE_3_DATA = [
    [
        hlp.lhbo(hlp.make_aeloc("@Ex 14:11"), "הֲֽמִבְּלִ֤י"),
        sub.mehuppak(),  # translit-ok
    ],
    [hlp.lhbo(hlp.make_aeloc("@Ex 29:23"), "וְֽחַלַּ֨ת"), sub.azla()],
]
_TABLE_3 = hlp.table_std(_TABLE_3_DATA, coldirs=["rtl", "ltr"])
_TABLE_4 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Ps 1:1", "אַ֥שְֽׁרֵי")],
        [hlp.lhbo("@Ps 89:25", "וֶ֥אֱֽמוּנָתִ֣י")],
        [hlp.lhbo("@Ps 64:7", "יַ֥חְפְּֽשׂוּ")],
    ]
)
SEC = [
    sub.para(
        [
            "The above describes $gaya",
            " with $shewa in words with disjunctive accents. This $gaya",
            " also occurs occasionally in"
            " words with conjunctives, especially unusual combinations of"
            " conjunctives. E.g.:",
        ]
    ),
    _TABLE_1,
    # XXX turn the comment below into a footnote?
    # placeholder is dash not א in ITM
    sub.para(
        [
            "where ",
            sub.darga(),
            " follows ",
            sub.geresh(),
            ", and is the second servus before ",
            sub.revia(),
            ", or",
        ]
    ),
    _TABLE_2,
    sub.para(
        [
            "on a word (which is long and starts with $shewa) which has ",
            sub.merka(),  # translit-ok
            " as a servus to ",
            sub.legarmeh(),
            ".",
        ]
    ),
    sub.para(
        [
            "Occasionally $gaya",
            " with $shewa is used in words with other conjunctives, as with",
        ]
    ),
    _TABLE_3,
    sub.para(
        [
            "In the three poetic books there are a few cases of $gaya with $shewa"
            " within a word. E.g.:",
        ]
    ),
    _TABLE_4,
]
