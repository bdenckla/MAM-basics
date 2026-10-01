import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_FTNT_LIBERTIES = sub.footnote(
    [
        "I recast $itm’s running prose here using the label β for the second"
        " word, and restructured its examples into the three tables below,"
        " one per case.",
    ]
)
_DATA_FOR_TABLE_1 = [
    [hlp.hboloc("זֶה־לִּ֞י", "@Gen 31:41"), "simple"],
    [hlp.hboloc("זֶה־בְּנִ֥י", "@1K 3:23"), sub.dol(["starting with $shewa"])],
    [hlp.hboloc("זֶה־שְּׁמִ֣י", "@Ex 3:15"), sub.saa()],
    [hlp.hboloc("וְזֶה־לְּךָ֣", "@Ex 3:12"), sub.dol(["both starting with $shewa"])],
]
_DATA_FOR_TABLE_2 = [
    [hlp.hboloc("וְזֶה־פִּרְיָֽהּ׃", "@Nu 13:27")],
    [hlp.hboloc("וְזֶה־מִּזְבֵּ֥חַ", "@1C 22:1")],
]
_DATA_FOR_TABLE_3 = [
    [hlp.hboloc("זֶה־יִֽהְיֶ֥ה", "@Jos 15:4")],
    [hlp.hboloc("זֶֽה־יָ֝דַ֗עְתִּי", "@Ps 56:10")],
]
SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    sub.para(
        [
            "$Dagesh is used in the first letter of a word β following ",
            hlp.hbo("זֶה"),
            " when the two words are are joined by $maqqef,",
            " and (for the most part) where β is initially stressed. E.g.:",
        ]
    ),
    hlp.table_std(_DATA_FOR_TABLE_1, coldirs=["rtl", "ltr"]),
    sub.para(
        [
            "There are only two cases where $dagesh is used despite β lacking initial stress:",
        ]
    ),
    hlp.table_std_rtl(_DATA_FOR_TABLE_2),
    sub.para(
        [
            "In all other cases, $dagesh is not used if β lacks initial stress. E.g.:",
        ]
    ),
    hlp.table_std_rtl(_DATA_FOR_TABLE_3),
]
