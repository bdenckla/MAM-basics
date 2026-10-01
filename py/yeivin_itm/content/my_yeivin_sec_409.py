import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_TABLE_DATA = [
    [hlp.hboloc("מַה־יְדַבֵּֽר׃", "@Jer 5:15"), ""],
    [hlp.hboloc("מַה־יְצַוֶּ֥ה", "@Nu 9:8"), ""],
    [
        hlp.hboloc("מַה־יְּדִיד֥וֹת", "@Ps 84:2"),
        sub.dol("exception: $dagesh used unexpectedly"),
    ],
    [
        hlp.hboloc("מַה־שְׁתֵּ֞י", "@Zech 4:12"),
        sub.dol("exception: $dagesh absent unexpectedly"),
    ],
    [hlp.hboloc("מַה־לַתֶּ֥בֶן", "@Jer 23:28"), sub.saa()],
]
SEC = [
    sub.para(
        [
            "As a general rule, $dagesh is used in the first letter of a word following ",
            hlp.hbo("מַה"),
            sub.thspc(),
            " unless this letter is ",
            sub.yod(),
            " with $shewa.",
        ]
    ),
    hlp.table_std(_TABLE_DATA, coldirs=["rtl", "ltr"]),
]
