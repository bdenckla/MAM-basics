import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_TABLE_1 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Nu 17:23", "וַיָּ֣צֵֽץ צִ֔יץ")],
        [hlp.lhbo("@Is 66:3", "עֹ֣רֵֽף כֶּ֔לֶב")],
        [hlp.lhbo("@Is 66:3", "מְבָ֣רֵֽךְ אָ֑וֶן")],
        [
            hlp.lhbo("@Is 40:7", "נָ֣בֵֽל צִ֔יץ")
        ],  # MAM has maqaf but notes that others have space
        [hlp.lhbo("@Is 40:8", "נָ֣בֵֽל צִ֑יץ")],
        # XXX turn the comment below into a footnote?
        # What is the contrast implied by ITM's "cf. 8" comment on the 40:7 case?
        # (ITM just says "cf. 8" whereas we provide 40:8 and don't say "cf. 8")
        # 40:7 & 40:8 seem pretty analogous to me.
        # The only difference I can see is that 40:8 is on atnax whereas 40:7 is on zaqef
        # is is there some pausal vs. non-pausal distinction expected, but not present?
    ]
)
SEC = [
    sub.para(
        [
            "Where a word ending in a closed syllable pointed with ",
            sub.tsere(),
            " has its stress retracted, and the ",
            sub.tsere(),
            " remains, it is marked by $gaya",
            " ",
            hlp.rtn_p(308, post=", 1c"),
            ". E.g.:",
        ]
    ),
    _TABLE_1,
    sub.para(["This $gaya is marked both in manuscripts and in printed texts."]),
]
