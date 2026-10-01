import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_FTNT_LIBERTIES = sub.footnote(
    [
        "I added the opening overview of what this section and the next cover,"
        " and restructured $itm’s prose into the lists and tables below."
        " I also added the remark that $revia is used as a generic accent"
        " in the three numbers listed below.",
    ]
)
_TABLE_1_DATA = [
    [hlp.lhbo("@1C 5:4", "שְׁמַֽעְיָ֥ה"), "within word"],
    [hlp.lhbo("@Is 1:1", "יְשַֽׁעְיָ֣הוּ"), sub.saa()],
    [hlp.lhbo("@Neḥ 11:24", "וּפְתַֽחְיָ֨ה"), sub.saa()],
    [hlp.lhbo("@1K 1:51", "יִשָּׁבַֽע־לִ֤י"), ["before ", sub.maqqef()], "next is ל"],
    [hlp.lhbo("@Jud 14:3", "קַֽח־לִ֔י"), sub.saa(), "next is ל"],
    [hlp.lhbo("@1S 28:22", "שְׁמַֽע־נָ֤א"), sub.saa(), "next is נ"],
]
_TABLE_1 = hlp.table_std(_TABLE_1_DATA, coldirs=["rtl", "ltr", "ltr"])
_TABLE_2 = hlp.table_std_rtl(
    [
        [hlp.lhbo("@Rut 1:21", "הֵ֥רַֽע לִֽי׃"), ["normal vowel"]],
        [hlp.lhbo("@1K 2:8", "וָאֶשָּׁ֨בַֽע ל֤וֹ"), sub.saa()],
        [hlp.lhbo(hlp.make_dloc("@Ez 1:4", "@Ez 1:27"), "וְנֹ֥גַֽהּ ל֖וֹ"), sub.saa()],
        [hlp.lhbo("@Jud 19:25", "לִשְׁמֹ֣עַֽ ל֔וֹ"), ["furtive ", sub.patax()]],
        [hlp.lhbo("@Dt 29:19", "סְלֹ֣חַֽ לוֹ֒"), sub.saa()],
    ]
)
SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    sub.para(
        [
            "This section and the next will cover the following classes of",
            " $pgaya on a short vowel before a guttural:",
        ]
    ),
    sub.ordered_list_with_lcromnum(
        [sub.cmn_354_lcromnum_i(), sub.cmn_354_lcromnum_ii()]
    ),
    sub.para_with_romnum_and_initial_uah(
        "i",
        sub.cmn_354_lcromnum_i(),
        [
            "$Gaya is sometimes marked on a syllable closed by a guttural."
            " The guttural may close the syllable in either of the following two ways:",
        ],
    ),
    sub.unordered_list(
        [
            ["Within a word, i.e. with a $silshewa."],
            [
                "At the end of a word with $maqqef",
                sub.emdash(),
                "especially if the next starts with ",
                sub.lamed(),
                " or ",
                sub.nun(),
                ".",
            ],
        ]
    ),
    sub.para(["For example, "]),
    _TABLE_1,
    sub.para(["This $gaya is consistently used with the following numbers:"]),
    sub.unordered_list(
        [
            hlp.hbo("אַרְבַּֽע־עֶשְׂרֵ֗ה"),
            hlp.hbo("תְּשַֽׁע־עֶשְׂרֵ֗ה"),
            hlp.hbo("שְׁבַֽע־עֶשְׂרֵ֗ה"),
        ]
    ),
    sub.para_paren(["Above, ", sub.revia(), " is used as a generic accent."]),
    sub.para(
        [
            "$Gaya is sometimes similarly used at the end of a word"
            " even if that word is ",
            hlp.emphasis("not"),
            " joined to the next by $maqqef.",
            " In such words, the guttural-closed syllable follows the stress,"
            " which is penultimate."
            " The vowel sound before the guttural sound"
            " may be notated as a furtive ",
            sub.patax(),
            ". E.g.:",
        ]
    ),
    _TABLE_2,
]
