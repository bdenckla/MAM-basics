import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_DLOC_GEN_AND_LEV = hlp.make_dloc("@Gen 1:18", "@Lev 10:10")
_JER_48_20 = "@Jer 48:20", "וּֽזְעָ֑קוּ"
_FTNT = sub.footnote(
    [sub.irrelevant_ketiv(*_JER_48_20, "וזעקי"), " ", sub.ITM_PRESENTS_KQ_IN_MANU_STYLE]
)
_TABLE_1 = hlp.table_std_rtl(
    [
        [hlp.span_ltr("Before שׁ"), hlp.lhbo("@Jud 5:12", "וּֽשְׁבֵ֥ה")],
        [sub.saa(), hlp.lhbo(hlp.make_aeloc("@2K 19:16"), "וּֽשְׁמָ֔ע")],
        [sub.saa(), hlp.lhbo("@Qoh 9:7", "וּֽשְׁתֵ֥ה")],
        [hlp.span_ltr("Before שׂ"), hlp.lhbo("@Lev 25:34", "וּֽשְׂדֵ֛ה")],
        [hlp.span_ltr("Before ס"), hlp.lhbo("@Is 26:20", "וּֽסְגֹ֥ר")],
        [sub.saa(), hlp.lhbo("@1K 13:7", "וּֽסְעָ֑דָה")],
        [hlp.span_ltr("Before ז"), hlp.lhbo("@Gen 2:12", "וּֽזְהַ֛ב")],
        [sub.saa(), hlp.lhbo(*_JER_48_20), _FTNT],
        [hlp.span_ltr("Before צ"), hlp.lhbo("@Jer 22:20", "וּֽצְעָ֔קִי")],
        [
            hlp.span_ltr("Before ק"),
            hlp.lhbo("@Is 34:16", "וּֽקְרָ֔אוּ"),
            sub.ms_a_x_patax("ק"),
        ],
    ]
)
_TABLE_2 = hlp.table_std_rtl(
    [
        [
            hlp.span_ltr("Before ס"),
            hlp.lhbo("@Is 45:14", "וּֽסְחַר־כּוּשׁ֮"),
            sub.ms_a_x_patax("ס"),
        ],
        [
            sub.saa(),
            hlp.lhbo("@2K 7:18", "וּֽסְאָה־סֹ֙לֶת֙"),
            sub.xxx_hbo_in_parens(sub.ms_s1_1053(), "סֳ"),
        ],
        [
            hlp.span_ltr("Before ת"),
            hlp.lhbo("@Ez 26:21", "וּֽתְבֻקְשִׁ֗י"),
            sub.ms_a_x_patax("ת"),
        ],
        [sub.saa(), hlp.lhbo("@Jer 3:25", "וּֽתְכַסֵּ֘נוּ֮"), sub.ms_a_x_patax("ת")],
        [hlp.span_ltr("Before ל"), hlp.lhbo(_DLOC_GEN_AND_LEV, "וּֽלֲהַבְדִּ֔יל")],
    ]
)
SEC = [
    sub.para_with_romnum_and_initial_uah(
        "ii",
        sub.cmn_347_lcromnum_ii(),
        [
            "$Gaya in this situation is especially common before sibilants "
            # ITM has "sibillants" (double L) in error.
            "but also comes before other letters."
            " Thus, in the syllable right before the stress,",
        ],
    ),
    _TABLE_1,
    sub.para(["In the second syllable before the stress syllable:"]),
    _TABLE_2,
]
