from itertools import starmap
import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_FTNT_1 = sub.footnote(
    [
        "I read “connected” here to mean"
        " “presumably intended to be pronounced in a connected fashion.”"
    ]
)
_DATA_FOR_TABLE = [
    [hlp.hboloc("רִ֥יב לֹּא־לֽוֹ׃", "@Prov 26:17"), ""],
    [hlp.hboloc("כִּ֛י לֹּ֥א ל֖וֹ", "@Gen 38:9"), "(after a disjunctive)"],
]
_DATA_FOR_TABLE_IN_FTNT_2 = [
    [hlp.hboloc("מִשְׁכָּנ֥וֹת לֹּא־לֽוֹ׃", "@Ḥab 1:6")],
    [hlp.hboloc("הַמַּרְבֶּ֣ה לֹּא־ל֔וֹ", "@Ḥab 2:6")],
]
_FTNT_2 = sub.footnote(
    [
        sub.para(["The other two of the four cases are as follows:"]),
        hlp.table_std_rtl(_DATA_FOR_TABLE_IN_FTNT_2),
    ]
)
_THE_FIVE = [
    (sub.join_with_paseq("וַיֹּ֥אמֶֽר", "לֹ֖א"), "@1K 2:30"),
    (sub.join_with_paseq("וַיֹּ֣אמֶֽר", "לֹ֔א"), "@1K 11:22"),
    (sub.join_with_paseq("וַיֹּ֥אמֶֽר", "לֹֽא׃"), "@Jud 12:5"),
    (sub.join_with_paseq("וַיֹּ֥אמֶר", "לֹ֖א"), "@Gen 18:15"),
    ("וַיֹּ֣אמֶר׀ לֹ֗א", "@Jos 5:14"),
]
_THE_FIVE = list(starmap(hlp.hboloc, _THE_FIVE))
_NO_GAYA = sub.dol(["no $gaya"])
_DATA_FOR_TABLE_FOR_FTNT_FOR_THE_FIVE = [
    [_THE_FIVE[0], sub.ms_aleppo(), sub.gaya(), sub.paseq()],
    [_THE_FIVE[1], sub.ms_aleppo(), sub.saa(), sub.saa()],
    [_THE_FIVE[2], sub.ms_aleppo(), sub.saa(), sub.saa()],
    [_THE_FIVE[3], sub.ms_lenin(), [*_NO_GAYA, "?"], sub.saa()],
    [_THE_FIVE[4], sub.ms_aleppo(), _NO_GAYA, sub.legarmeh()],
]
_FTNT_FOR_THE_FIVE = sub.footnote(
    [
        sub.para(["Those five cases are as follows:"]),
        hlp.table_std(
            _DATA_FOR_TABLE_FOR_FTNT_FOR_THE_FIVE, coldirs=["rtl", "ltr", "ltr", "ltr"]
        ),
        sub.para(
            [
                ["It is hard to say whether ", sub.ms_lenin()],
                [" has a $gaya or not in case 4 of 5 (Gen 18:15)."],
                [" Each of the three dots of the ", sub.segol()],
                [" is visible but faded."],
                [" Also visible but faded is a fourth small mark"],
                [" to the left of (“after”) the ", sub.segol(), "."],
                [" This fourth small mark might be"],
                [" (the remains of) a $gaya but it is hard to say."],
            ]
        ),
    ]
)
SEC = [
    sub.para(
        [
            "In the pair ",
            hlp.hboloc("וַיֹּאמְר֣וּ לֹּ֔א", hlp.make_dloc("@Gen 19:2", "@1S 8:19")),
            sub.thspc(),
            " $dagesh also appears to be used to emphasize the division"
            " between the words. Compare with ",
            hlp.hboloc("וַיֹּ֩אמְרוּ֩ ל֨וֹ", hlp.make_dloc("@Jud 18:19", "@Est 6:13")),
            sub.thspc(),
            " where the pair is ",
            hlp.ftntjoin("connected", _FTNT_1),
            " and $dagesh is not used.",
        ]
    ),
    sub.para(
        [
            "Consider the pair ",
            hlp.hbo("וַיֹּאמֶר לֹא"),
            " where ויאמר has a conjunctive accent. ",
            hlp.paren(
                [
                    "There are five such pairs in the ",
                    hlp.ftntjoin("Bible.", _FTNT_FOR_THE_FIVE),
                ]
            ),
            " The division between ויאמר and לא ",
            hlp.paren_xt(
                [
                    "which contrasts with the connection of the similar-sounding pair ",
                    hlp.hbo("וַיֹּאמֶר לוֹ"),
                ]
            ),
            " is usually emphasized by a $gaya on ",
            sub.mem(),
            " and a ",
            sub.paseq(),
            " ",
            hlp.rtn_p(325),
            ". The Masorah records that ben Naftali uses $dagesh in לא in two of the five cases,"
            " but in the other three cases bN agrees with bA, leaving לא $dagesh-free."
            " It is reported that bN similarly used $dagesh in the ",
            sub.lamed(),
            " of ",
            hlp.hboloc("כִּ֣י׀ לֹּ֗א", "@1S 16:7"),
            sub.thspp(),  # MAM כִּ֣י׀ לֹ֗א
            " The $dagesh in all these cases"
            " presumably serves to emphasize the division between the words.",
        ]
    ),
    sub.para(
        [
            ["In four cases, the ", sub.lamed()],
            [" of לא in the pair לא לו has $dagesh."],
            [" ", hlp.ftntjoin("E.g.:", _FTNT_2)],
        ]
    ),
    hlp.table_std(_DATA_FOR_TABLE, coldirs=["rtl", "ltr"]),
    sub.para(
        [
            "This $dagesh is presumably intended to distinguish לא from לו."
            " In the pair לו לא, i.e. in the pair with the opposite order, no $dagesh is used.",
        ]
    ),
]
