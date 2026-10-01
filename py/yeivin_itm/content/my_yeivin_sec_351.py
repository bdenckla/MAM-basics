import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_TABLE_1 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Is 62:9", "וְהִֽלְל֖וּ")],
        [hlp.lhbo("@Is 64:10", "הִֽלְל֙וּךָ֙")],
        [hlp.lhbo("@Jud 5:11", "מְחַֽצְצִ֗ים")],
        [hlp.lhbo("@2S 16:7", "בְּקַֽלְל֑וֹ")],
        [hlp.lhbo("@1S 2:25", "וּפִֽלְל֣וֹ")],
        [hlp.lhbo("@Ez 31:6", "קִֽנְנוּ֙")],
    ]
)
_TABLE_2 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Ez 4:12", "בְּגֶֽלְלֵי֙")],
        [hlp.lhbo("@2C 20:2", "בְּחַֽצְצ֣וֹן")],
        [hlp.lhbo("@Jud 9:57", "קִֽלְלַ֖ת")],
        [hlp.lhbo("@Mi 6:7", "בְּרִֽבְב֖וֹת")],
        [hlp.lhbo("@Zech 11:3", "יִֽלְלַ֣ת")],
    ]
)
_TABLE_3 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@1K 1:40", "מְחַלְּלִ֣ים")],
        [hlp.lhbo("@Is 34:15", "קִנְּנָ֤ה")],
        [hlp.lhbo("@Ps 95:1", "נְרַנְּנָ֣ה")],
    ]
)
SEC = [
    sub.para(
        [
            "$Gaya is usually marked in this situation whether the"
            " first of the pair was historically doubled"
            " (and has lost this doubling) or not."
            " Thus, historically doubled:",
        ]
    ),
    _TABLE_1,
    sub.para(["With no historical doubling:"]),
    _TABLE_2,
    sub.para(
        [
            "In most such cases ",
            sub.ms_aleppo(),
            " marks a $x_shewa on the first of the pair.",
        ]
    ),
    sub.para(
        [
            "In a few cases of this situation, $gaya is not marked, as ",
            hlp.hbo_varacc("הִנְנִי"),
            " (always), and ",
            hlp.lhbo("@Job 10:15", "אַלְלַ֬י"),
            sub.thspp(),
            " In some similar cases, the first of the pair has $dagesh,"
            " and no $gaya is marked. E.g.:",
        ]
    ),
    _TABLE_3,
]
