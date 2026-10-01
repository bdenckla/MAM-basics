import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_LN_AMOS_8_8 = "@Amos 8:8", "וְנִשְׁקֳעָ֖ה"


_TABLE_1A_DATA = [
    [hlp.hbo_varacc("קֳהָת")],
    [hlp.lhbo("@Ez 32:22", "וְכׇל־קֳהָלָ֔הּ")],  # MAM has simple shewa (with varika?)
]
_NU_4_7 = "הַקֳּעָרֹ֤ת"
_FTNT_0 = sub.footnote(
    [
        "Here $itm gives locale Nu 4:6 for ",
        hlp.hbo(_NU_4_7),
        ", but I only find it in the next verse, i.e. at Nu 4:7."
        " Does Nu 4:6 reflect an alternate verse numbering tradition,"
        " or is it just a typo?",
    ]
)
_TABLE_1B_DATA = [
    [hlp.hbo_varacc("הַקֳּהָתִי")],  # MAM has simple shewa (with varika?)
    [hlp.lhbo("@Nu 4:7", _NU_4_7), _FTNT_0],  # MAM has simple shewa (with varika?)
    [
        hlp.lhbo("@Jer 20:15", "שִׂמֳּחָֽהוּ׃"),
        sub.ms_lenin(),
    ],  # MAM has simple shewa (with varika?)
    [
        hlp.lhbo("@Is 48:8", "פִתֳּחָ֣ה"),
        sub.ms_cairo(),
    ],  # MAM has simple shewa (with varika?)
    [hlp.lhbo("@Is 27:8", "בְּסַאסֳּאָ֖ה")],  # MAM has simple shewa (with varika?)
]
_FTNT_1 = sub.footnote(sub.irrelevant_ketiv(*_LN_AMOS_8_8, "ונשקה"))
_TABLE_1C_DATA = [
    [hlp.lhbo("@1K 4:12", "לְיׇקְמֳעָֽם׃")],  # MAM has simple shewa (with varika?)
    # Above, qamats qatan
    [hlp.lhbo("@Jud 3:26", "הִֽתְמַהְמֳהָ֑ם")],  # MAM has simple shewa (with varika?)
    [hlp.lhbo(*_LN_AMOS_8_8), _FTNT_1],
    # MAM has simple shewa (with varika?), i.e. וְנִשְׁקְעָ֖ה
]
_TABLE_2A_DATA = [
    [hlp.lhbo("@Ez 16:51", "וַתְּצַדֲּקִי֙")],  # MAM has simple shewa (with varika?)
]
_TABLE_2B_DATA = [
    [hlp.lhbo("@1C 5:16", "מִגְרֲשֵׁ֥י")],  # MAM has simple shewa (with varika?)
    [
        hlp.lhbo("@Gen 10:3", "אַשְׁכֲּנַ֥ז"),
        sub.ms_lenin(),
    ],  # MAM has simple shewa (with varika?)
]
_TABLE_1A = hlp.table_std(_TABLE_1A_DATA, coldirs=["rtl", "ltr"])
_TABLE_1B = hlp.table_std(_TABLE_1B_DATA, coldirs=["rtl", "ltr"])
_TABLE_1C = hlp.table_std(_TABLE_1C_DATA, coldirs=["rtl", "ltr"])
_TABLE_2A = hlp.table_std(_TABLE_2A_DATA, coldirs=["rtl", "ltr"])
_TABLE_2B = hlp.table_std(_TABLE_2B_DATA, coldirs=["rtl", "ltr"])
SEC = [
    sub.para_with_romnum_and_initial_uah(
        "ii",
        sub.cmn_388_lcromnum_ii(),
        [
            sub.x_qamets(mwcap="mwcap-type-sentence-case"),
            " is the most common type of $x_shewa used for phonetic reasons. ",
            hlp.paren(
                [
                    "Recall that it is also the most common type of"
                    " $x_shewa used for morphological reasons.",
                ]
            ),
            " It occurs most commonly before a guttural with ",
            sub.qamets(),
            ". However, ",
            sub.x_qamets(),
            " in these cases replaces a $simshewa"
            " which is vocal according to the standard rules, so that"
            " error in pronunciation would not be likely."
            " Presumably the $xatef sign was intended to prevent"
            " incorrect pronunciation resulting from lack of attention."
            " E.g.:",
        ],
    ),
    sub.para(["At the start of a word:"]),
    _TABLE_1A,
    sub.para(["On a letter with $dagesh:"]),
    _TABLE_1B,
    sub.para(["On the second of a pair of letters with $shewa:"]),
    _TABLE_1C,
    sub.para(
        [
            sub.x_patax(mwcap="mwcap-type-sentence-case"),
            " is used similarly, for phonetic reasons, in the following:",
        ]
    ),
    sub.para(["On a letter with $dagesh:"]),
    _TABLE_2A,
    sub.para(["On the second of a pair of letters with $shewa:"]),
    _TABLE_2B,
]
