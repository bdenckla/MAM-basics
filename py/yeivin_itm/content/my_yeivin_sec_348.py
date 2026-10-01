import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_AXP_NUN = sub.ms_a_x_patax("נ")
_AXP_SHIN = sub.ms_a_x_patax("שׁ")
_BXP_TSADE = sub.xxx_hbo_in_parens(sub.ms_b_4445(), "צֲ")
_HE_INT = [sub.he(), " interrogative"]
_DEF_ART = "definite article"
_TABLE_1_DATA = [
    [hlp.lhbo("@1S 18:23", "הַֽנְקַלָּ֤ה"), _AXP_NUN, _HE_INT],
    # _AXP_NUN means א=הַֽנֲקַלָּ֤ה
    [hlp.lhbo("@Gen 27:38", "הַֽבְרָכָ֨ה"), "", sub.saa()],
    ([hlp.lhbo("@Ez 40:43", "וְהַֽשְׁפַתַּ֗יִם"), _AXP_SHIN, _DEF_ART]),
    # _AXP_SHIN means א=וְהַֽשֲׁפַתַּ֗יִם
    ([hlp.lhbo("@Ps 104:18", "לַֽשְׁפַנִּֽים׃"), _AXP_SHIN, sub.saa()]),
    # _AXP_SHIN means א=לַֽשֲׁפַנִּֽים
    ([hlp.lhbo(hlp.make_dloc("@2K 2:1", "@2K 2:11"), "בַּֽסְעָרָ֖ה"), "", sub.saa()]),
    ([hlp.lhbo("@Jer 33:10", "הַֽנְשַׁמּ֗וֹת"), "", sub.saa()]),
    (
        [
            hlp.lhbo(hlp.make_aeloc("@Ex 7:29"), "הַֽצְפַרְדְּעִֽים׃"),
            _BXP_TSADE,
            sub.saa(),
        ]
    ),
    # _BXP_TSADE means B=הַֽצֲפַרְדְּעִֽים:
    # XXX turn the comment below into a footnote?
    # The word above, הַֽצְפַרְדְּעִֽים׃, does not appear elsewhere with that accent (silluq)
    # but does appear elsewhere with other accents
    ([hlp.lhbo("@2K 17:31", "וְהַֽסְפַרְוִ֗ים"), "", sub.saa()]),
    # MAM has no gaʿya in the above, i.e. MAM has וְהַסְפַרְוִ֗ים
]
_TABLE_1 = hlp.table_std(_TABLE_1_DATA, coldirs=["rtl", "ltr", "ltr"])
SEC = [
    sub.para(
        [
            "$Gaya is occasionally marked on initial ",
            sub.he(),
            " with ",
            sub.patax(),
            " before letters other than ",
            sub.mem(),
            ". E.g.:",
        ]
    ),
    _TABLE_1,
]
