import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_DATA_FOR_TABLE = [
    ["פַּעְנֵּ֒חַ֒", "@Gen 41:45", sub.ms_s_507()],  # MAM פַּעְנֵ֒חַ֒
    ["יֶאְשָּׁ֑מוּ", "@Ho 10:2", sub.ms_ny_jts()],  # MAM יֶאְשָׁ֑מוּ
    ["לַחְמְּךָ֖", "@Ez 4:15", sub.ms_ny_jts()],  # MAM לַחְמְךָ֖
]
_DATA_FOR_TABLE = [(hlp.hboloc(r[0], r[1]), r[2]) for r in _DATA_FOR_TABLE]
SEC = [
    sub.para(
        [
            "In most early manuscripts, $dagesh is not used"
            " after a guttural pointed with $simshewa. The ",
            sub.sefer_ha_xillufim(),
            " reports that ben Naftali used $dagesh in the ",
            sub.qof(),
            " of ",
            hlp.hboloc("יַעְקֹּ֔ב", "@Jer 9:3"),
            sub.thspc(),
            " "  # MAM יַעְקֹ֔ב
            "and $dagesh is used here in ",
            sub.ms_cairo(),
            " and ",
            sub.ms_lenin_15(),
            ". Some manuscripts occasionally show $dagesh",
            " in this situation, e.g.:",
        ]
    ),
    hlp.table_std(_DATA_FOR_TABLE, coldirs=["rtl", "ltr"]),
    sub.para_paren(
        [
            "Note the third meaning given for the term $dagesh (דגש) in ",
            hlp.rtn(132),
            ".",
        ]
    ),
    sub.para_paren(
        [
            "It is noteworthy that the $dagesh sign"
            " is used quite commonly in some Palestinian manuscripts"
            " in the situations covered here and in ",
            hlp.rtn(413),
            ". See Revell, 1970, p. 77.",
        ]
    ),
]
