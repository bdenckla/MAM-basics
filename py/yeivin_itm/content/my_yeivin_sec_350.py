import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_JER_20_9 = "@Jer 20:9", "כַּֽלְכֵֿ֖ל"
_JER_20_9_MER = "כַּֽלְכֵֿ֥ל"
_PS_17_14_ILUY = "@Ps 17:14", "מִֽמְתִ֬ים"
_FTNT_0 = sub.footnote(
    [
        "Here $itm uses the example ",
        hlp.hboloc("מִֽמְתִ֥ים", "@Ps 17:14"),
        sub.thspp(),
        " This is the first atom of the compound ",
        hlp.hbo("מִֽמְתִ֥ים־יָדְךָ֨׀"),
        sub.thspc(),
        " which is the first chanted word of the verse. This $gaya-",
        sub.merka(),  # translit-ok
        " pointing is disputed; see the ",
        sub.mamdoc("D1-Psalms.html#c17v14"),
        ". Because this pointing is disputed, I use ",
        hlp.lhbo(*_PS_17_14_ILUY),
        " as the example here."
        " It is the third chanted word of the same verse."
        " It differs from $itm’s example only in its accent (",
        sub.illuy(),
        " vs. ",
        sub.merka(),  # translit-ok
        "), and thus seems a better example, since,"
        " as far as I know, there’s no dispute about its pointing.",
    ]
)
_TABLE_1_DATA = [
    [hlp.lhbo("@Jos 11:2", "כִּֽנְר֖וֹת"), sub.ms_a_x_patax("נ")],
    [hlp.lhbo(*_PS_17_14_ILUY), _FTNT_0],
    [hlp.lhbo("@Nu 1:18", "וַיִּתְיַֽלְד֥וּ")],
    [hlp.lhbo("@Jud 16:16", "וַתְּאַֽלְצֵ֑הוּ"), sub.ms_a_x_patax("ל")],
    [hlp.lhbo("@Gen 1:24", "וְחַֽיְתוֹ־אֶ֖רֶץ")],
    [hlp.lhbo("@Gen 2:23", "לֻֽקְחָה־זֹּֽאת׃")],
    [hlp.lhbo("@Ez 7:24", "מְקַֽדְֿשֵׁיהֶֽם׃")],  # rafe not present in MAM
]
_TABLE_1 = hlp.table_std(_TABLE_1_DATA, coldirs=["rtl", "ltr"])
_TABLE_2_DATA = [
    [hlp.lhbo("@1S 5:12", "שַֽׁוְעַ֥ת")],
    [hlp.lhbo("@2S 22:2", "סַֽלְעִ֥י")],
    [hlp.lhbo("@Is 65:8", "הַֽשְׁחִ֥ית")],
    [hlp.lhbo("@Job 1:3", "שִֽׁבְעַ֨ת")],
    [hlp.lhbo("@Gen 21:6", "יִֽצְחַק־לִֽי׃"), sub.xxx_hbo_in_parens("some have", "צֲ")],
    [hlp.lhbo("@1K 17:11", "לִֽקְחִי־נָ֥א")],
]
_TABLE_2 = hlp.table_std(_TABLE_2_DATA, coldirs=["rtl", "ltr"])
_FTNT_1 = sub.footnote(
    [
        "Here $itm has ",
        sub.merka(),  # translit-ok
        ", i.e. ",
        hlp.hbo(_JER_20_9_MER),
        sub.thspp(),
        " I have ",
        sub.tifxa(),
        ".",
    ]
)
_HBO_STR_IS_54 = "כַּֽדְכֹֿד֙"
_FTNT_2 = sub.footnote(
    [
        "In $itm, ",
        hlp.hbo(_HBO_STR_IS_54),
        " has no accent. (I show $pashta.)",
    ]
)
_TABLE_3_DATA = [
    [hlp.lhbo("@Jer 12:16", "דַּֽרְכֵ֨י")],
    [hlp.lhbo(*_JER_20_9), _FTNT_1],  # rafe not present in MAM
    [hlp.lhbo("@Is 54:12", _HBO_STR_IS_54), _FTNT_2],  # rafe not present in MAM
    [hlp.lhbo("@Lev 13:48", "בִֽשְׁתִי֙")],
    [hlp.lhbo("@Is 20:1", "סַֽרְג֖וֹן")],
    [
        hlp.lhbo("@Job 33:25", "רֻֽטְפַ֣שׁ"),
        sub.xxx_hbo_in_parens(sub.ms_a_and_l(), "טֲ"),
    ],
    [hlp.lhbo("@Gen 30:38", "בְּשִֽׁקְת֣וֹת")],
]
_TABLE_3 = hlp.table_std(_TABLE_3_DATA, coldirs=["rtl", "ltr"])
_TABLE_4_DATA = [
    [
        hlp.lhbo("@Dan 9:19", "הַֽקְשִׁ֥יבָה"),
        sub.xxx_hbo_in_parens(sub.ms_lenin(), "קֲ"),
    ],
    [hlp.lhbo("@2S 22:12", "חַֽשְׁרַת־מַ֖יִם"), sub.ms_a_x_patax("שׁ")],
]
_TABLE_4 = hlp.table_std(_TABLE_4_DATA, coldirs=["rtl", "ltr"])
SEC = [
    sub.para_with_romnum_and_initial_uah(
        "iii",
        sub.cmn_347_lcromnum_iii(),
        ["1) Before a letter which has lost its historical doubling:"],
    ),
    _TABLE_1,
    # I did not transcribe "and others." here; it seemed both confusing and redundant.
    sub.para(["2) Before a syllable starting with a guttural:"]),
    _TABLE_2,
    sub.para(
        [
            "3) Before a syllable starting with a ",
            sub.begad_kefat(),
            " letter which is ",
            sub.rafe(),
            ":",
        ]
    ),
    _TABLE_3,
    sub.para(["4) Other situations:"]),
    _TABLE_4,
]
