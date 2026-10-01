import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_ISE_JER_31_33 = "@Jer 31:33"  # 31:32 in MAM
_TABLE_2A_DATA = [
    [hlp.lhbo("@Dt 9:27", "קֲשִׁי֙"), sub.ms_lenin_01()]
    # MAM has simple shewa on ק, i.e. קְשִׁי֙
]
_TABLE_2B_DATA = [
    [hlp.lhbo("@Jer 4:7", "מִֽסֻּבֲּכ֔וֹ")]
    # MAM מִֽסֻּבְּﬞכ֔וֹ (varika-shewa) vs ITM xataf patax
]
_TABLE_2C_DATA = [
    [hlp.lhbo("@Ez 35:6", "יִרְדֲּפֶ֑ךָ")],
    # MAM has simple shewa on ד, i.e. יִרְדְּפֶ֑ךָ
    [hlp.lhbo("@Ez 35:6", "יִרְדֲּפֶֽךָ׃")],
    # MAM has simple shewa on ד, i.e. יִרְדְּפֶֽךָ׃
    [hlp.lhbo("@Ez 35:11", "אֶשְׁפֲּטֶֽךָ׃")],
    # MAM has simple shewa on פ, i.e. אֶשְׁפְּטֶֽךָ׃
    [hlp.lhbo(_ISE_JER_31_33, "אֶכְתֲּבֶ֑נָּה"), sub.ms_lenin()],
    # MAM has simple shewa on ת, i.e. אֶכְתְּבֶ֑נָּה
]
_TABLE_1_DATA = [
    [hlp.lhbo("@Dan 4:27", "בֱנַיְתַהּ֙")],
    [hlp.lhbo("@Ezra 4:18", "קֱרִ֖י")],
    [hlp.lhbo("@Dan 2:30", "גֱּלִ֣י"), "but", hlp.lhbo("@Dan 2:19", "גְלִ֑י")],
    [hlp.lhbo("@Dan 7:7", "וּמַדֱּקָ֔ה")],
    [hlp.lhbo("@Dan 7:11", "מְמַלֱּלָ֑ה")],
]
_TABLE_1 = hlp.table_std(_TABLE_1_DATA, coldirs=["rtl", "ltr", "rtl"])
_TABLE_2A = hlp.table_std(_TABLE_2A_DATA, coldirs=["rtl", "ltr"])
_TABLE_2B = hlp.table_std(_TABLE_2B_DATA, coldirs=["rtl", "ltr"])
_TABLE_2C = hlp.table_std(_TABLE_2C_DATA, coldirs=["rtl", "ltr"])
SEC = [
    sub.para(
        [
            "In some cases (as noted above) ",
            sub.x_patax(),
            " occurs where this “morphological” ",
            sub.x_qamets(),
            " is expected."
            " Presumably"
            " this indicates that the original /o/ or /u/ coloring of the vowel"
            " was no longer audible, so it was treated as a ",
            sub.x_patax(),
            " (the normal sound of $shewa). E.g.:",
        ]
    ),
    sub.para(["At the start of a word:"]),
    _TABLE_2A,
    sub.para(["On a letter with $dagesh:"]),
    _TABLE_2B,
    sub.para(["On the second of a pair of letters with $shewa:"]),
    _TABLE_2C,
    sub.para(
        [
            "The “morphological” use of ",
            sub.x_segol(),
            " is rare in Hebrew",
            sub.emdash(),
            "one example is ",
            hlp.lhbo("@2S 6:5", "וּֽבְצֶלְצֱלִֽים׃"),
            " (in ",
            sub.ms_a_and_c(" and "),
            ") but it is more common in Aramaic words. E.g.:",
        ]
    ),
    _TABLE_1,
]
