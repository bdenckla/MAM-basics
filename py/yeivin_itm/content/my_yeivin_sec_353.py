import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_TABLE_1 = hlp.table_std_rtl(
    [
        [
            hlp.lhbo(hlp.make_dloc("@Ez 26:12", "@Ez 39:10"), "וּבָֽזְזוּ֙"),
            sub.ms_a_x_patax("ז"),
        ],
        [hlp.lhbo("@Is 58:9", "מִתּֽוֹכְךָ֙"), sub.ms_a_x_patax("כ")],
        [hlp.lhbo("@Jer 6:6", "סֹֽלְלָ֑ה"), sub.ms_a_x_patax("ל")],
    ]
)
_TABLE_2 = hlp.table_std(
    [
        ["present", "simple"],
        ["present", sub.xatef()],
        ["absent", "simple"],
        ["absent", sub.xatef()],
    ],
    arg_to_troh=[sub.gaya(), sub.dol(["$shewa notation"])],
)
_CONT_THIS_USAGE = [
    ["This usage of $shewa and $xatef"],
    [" is not consistent, however. Each of the four possible cases occur, at times:"],
]

SEC = [
    sub.para(
        [
            "Even where a long vowel precedes $shewa"
            " on an identical pair of letters, the long vowel is often marked with",
            " $gaya, and the $shewa is a $xatef. E.g.:",
        ]
    ),
    _TABLE_1,
    sub.para_paren(
        ["We consider nonfinal and final forms of the same letter to be identical."]
    ),
    sub.para(_CONT_THIS_USAGE),
    _TABLE_2,
    sub.para(
        [
            "Different methods are used in different manuscripts, and there is no"
            " agreement between them."
            " It appears that the general rule was as follows:",
        ]
    ),
    sub.unordered_list(
        [
            ["$simshewa after a long vowel was silent,"],
            [
                "unless this $shewa"
                " was on the first of an identical pair of letters,"
                " in which case it was vocal."
                " This latter fact could be marked by a",
                " $x_shewa and/or by a $gaya, so",
                sub.unordered_list(
                    [
                        "either one may be used alone,",
                        "but sometimes both are used, and",
                        "sometimes no indication is given.",
                    ]
                ),
            ],
        ]
    ),
    sub.para([hlp.rtn_p(385, "See "), "."]),
]
