import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_TABLE_1 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Jud 18:12", "וַֽיַּעֲל֗וּ")],
        [hlp.lhbo("@Jud 19:29", "הַֽמַּאֲכֶ֙לֶת֙")],
    ]
)
_TABLE_2 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Dt 31:20", "אֶֽל־הָאֲדָמָ֣ה׀")],
        [hlp.lhbo("@Nu 17:21", "כׇּֽל־נְשִׂיאֵיהֶ֡ם")],
    ]
)
SEC = [
    sub.para(
        [
            "The choice of which of two or more $gaya candidates should be"
            " marked on a word is determined by certain general principles,"
            " although these are affected by many detailed considerations"
            " which cannot be described here."
            " The basic principle is that $gaya_cs is preferred over $gaya_osr. E.g.:",
        ]
    ),
    _TABLE_1,
    sub.para(
        [
            "Here $gaya"
            " is marked on the initial closed syllable (of the regular type), but"
            " $gaya is not marked on the open syllable that follows it ",
            hlp.paren_xt(["the syllable before the ", sub.xatef()]),
            ". So also",
        ]
    ),
    _TABLE_2,
    sub.para(
        [
            "Here $gaya",
            " is marked on the initial closed syllable of non-regular type, but"
            " $gaya is not marked on the open syllable that follows it."
            " This general principle is common to all the early manuscripts.",
        ]
    ),
    sub.para(
        [
            "On the problem of preference"
            " in words which could have more than one $gaya_osr, see ",
            hlp.rtn(328),
            ".",
        ]
    ),
]
