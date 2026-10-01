import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_LIST_ITEM_1_OF_3 = [
    "Thus all three of ",
    sub.three_comma_and(sub.dagesh(), sub.gaya(), sub.paseq()),
    " may be used in the pair ",
    hlp.hbo("וַיֹּאמֶר לֹא"),
    " ",
    hlp.rtn_p(412),
    ".",
]
_LIST_ITEM_2_OF_3 = [
    "The use of $dagesh in ",
    hlp.hbo("בִּן־נּוּן"),
    " can be compared to the use of ",
    sub.paseq(),
    " where the same letter ends one word and starts the next ",
    hlp.rtn_p(284),
    ".",
]
_LIST_ITEM_3_OF_3 = [
    "Certain forms of $dexiq, such as ",
    hlp.hboloc("עָלֶ֣יךָ פָּ֑רֶץ", "@Gen 38:29"),
    " ",
    hlp.rtn_p(405),
    " can be compared to the use of $gaya on an open syllable after the accent ",
    hlp.rtn_p(332),
    " as ",
    hlp.hboloc("עֲבָדֶ֥יךָֽ אֵ֛לֶּה", "@2K 1:13"),
    ". Compare also the use of ",
    sub.mayela(),
    " ",
    hlp.rtn_p(216),
    " in ",
    hlp.hboloc("וּבָ֖אתָ־שָּׁ֑מָּה", "@2K 9:2"),
    " (where $dexiq is used) to the use of $gaya in ",
    hlp.hboloc("וּבָ֖אֽוּ־שָׁ֑מָּה", "@Ez 11:18"),
    " "  # MAM וּבָ֖אוּ־שָׁ֑מָּה
    "in ",
    sub.ms_lenin_18(),
    " (where $gaya is used).",
]
SEC = [
    sub.para(
        [
            "What is the function of $dagesh in its special uses covered in ",
            hlp.rtn(403),
            " and beyond? Its function seems to be analogous to that of $gaya",
            " and ",
            sub.paseq(),
            " since it is used in situations similar to those in which $gaya",
            " and ",
            sub.paseq(),
            " may be used. $Gaya and ",
            sub.paseq(),
            " indicate that words are separated and the reading slowed down.",
        ]
    ),
    sub.unordered_list([_LIST_ITEM_1_OF_3, _LIST_ITEM_2_OF_3, _LIST_ITEM_3_OF_3]),
    sub.para(
        [
            "This comparison suggests that $dagesh is used, like $gaya",
            " and ",
            sub.paseq(),
            ", to mark separation."
            " In cases where the need to emphasize separation became apparent,"
            " the Masoretes sometimes used ",
            sub.paseq(),
            " for this purpose, sometimes $dagesh, and sometimes $gaya",
            " (particularly before gutturals). It can, then, be assumed that",
            " $dagesh is intended to emphasize separation not only in cases like ",
            hlp.hbo("וַיֹּאמֶר לֹא"),
            sub.thspc(),
            " but also where $dexiq is used after ",
            sub.qamets(),
            ", and possibly also after ",
            sub.segol(),
            ".",
        ]
    ),
]
