import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_TABLE_1 = hlp.table_std_rtl(
    [
        [
            hlp.lhbo(hlp.make_dloc("@2S 5:24", "@1C 14:15"), "כְּֽשׇׁמְעֲךָ֞")
        ],  # qamats qatan
        [hlp.lhbo("@Jer 34:14", "תְּֽשַׁלְּח֡וּ")],
    ]
)
_TABLE_2 = hlp.table_std_rtl(
    [
        [hlp.lhbo(hlp.make_aeloc("@1K 8:1"), "לְֽהַעֲל֞וֹת")],
        [hlp.lhbo("@Zech 8:23", "וְֽהֶחֱזִ֡יקוּ")],
        [hlp.lhbo("@2C 32:33", "בְּֽמַעֲלֵה֮")],
        [hlp.lhbo("@Ho 8:2", "יְֽדַעֲנ֖וּךָ")],
        [hlp.lhbo("@Dt 7:26", "תְּֽתַעֲבֶ֖נּוּ")],
        [hlp.lhbo("@Ez 48:1", "לְֽבוֹא־חֲמָ֡ת")],
        # XXX ITM has an "also" here before the final example;
        # I removed it because it seemed superfluous, but I wonder ...
    ]
)
_TABLE_3 = hlp.table_std_rtl(
    [
        [hlp.lhbo(hlp.make_aeloc("@Is 28:4"), "וְֽהָ֨יְתָ֜ה")],
        [hlp.lhbo("@Joel 2:17", "וְֽיֹאמְר֞וּ")],
        [hlp.lhbo("@Zech 8:21", "וְֽהָלְכ֡וּ")],
        [hlp.lhbo("@Ez 41:7", "וְֽנָסְבָה֩")],
    ]
)
SEC = [
    sub.para(
        [
            "A special category of words which take $gaya",
            " with $shewa is formed by words of structure similar to the"
            " regular structure of words suitable for $gaya_cs but which have a letter with $shewa"
            " in place of the initial closed syllable, as ",
            sub.pat_meqatlim(),
            " and ",
            sub.pat_mefalpelim(),
            " (like ",
            hlp.hbo(sub.pat_mitqatlim()[0]),
            " and ",
            hlp.hbo(sub.pat_mitpalpelim()[0]),
            " see ",
            hlp.rtn(319),
            "). E.g.:",
        ]
    ),
    _TABLE_1,
    sub.para(
        ["also ", sub.pat_mefaalim(), " (like ", hlp.hbo(sub.pat_mitpaalim()[0]), ")"]
    ),
    _TABLE_2,
    sub.para(
        [
            "This $gaya",
            " may also occur in forms like ",
            sub.pat_mevarekhim(),
            " (like ",
            sub.hbo_pat_mitbarekhim(),
            " which has regular structure, but not fully regular, see ",
            hlp.rtn(322),
            ") as",
        ]
    ),
    _TABLE_3,
]
