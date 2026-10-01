import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_FTNT_0 = sub.footnote(sub.explain_paseq())
_FTNT_1 = sub.footnote(sub.surprising_long_xiriq("גּֽוֹיִם־"))
_TABLE_1 = hlp.table_std_rtl(
    [[hlp.lhbo("@Rut 1:11", "הַעֽוֹד־לִ֤י")], [hlp.lhbo("@Job 2:11", "לָנֽוּד־ל֖וֹ")]]
)
_TABLE_2 = hlp.table_std_rtl(
    [
        [hlp.lhbo(hlp.make_aeloc("@Is 8:11"), "הָֽעָם־הַזֶּ֖ה")],
        [hlp.lhbo("@Jos 11:12", "הַמְּלָֽכִים־הָ֠אֵ֠לֶּה")],
        [
            hlp.lhbo("@Dt 7:1", sub.join_with_paseq("גּֽוֹיִם־רַבִּ֣ים", "אא֡א")),
            _FTNT_0,
            _FTNT_1,
        ],
    ]
)
SEC = [
    sub.para(
        "Consider a word which has both of the following"
        " candidate locations for $gaya:",
    ),
    sub.ordered_list(
        [
            sub.gaya_os(),
            ["$gaya on a ", sub.mclv(), " syllable ", hlp.rtn_p(337)],
        ]
    ),
    sub.para(
        [
            "The general rule in such a case is that if the closed syllable"
            " comes right before the stress syllable, $gaya is marked on it. E.g.:",
        ]
    ),
    _TABLE_1,
    sub.para(
        [
            "However, if this is not the case, the $gaya"
            " on the open syllable is preferred. E.g.:",
        ]
    ),
    _TABLE_2,
]
