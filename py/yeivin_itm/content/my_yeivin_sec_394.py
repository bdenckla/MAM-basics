import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_FTNT_LIBERTIES = sub.footnote(
    [
        "The first two paragraphs below are mine, together with their forward"
        " references. One is on the symmetry of ",
        sub.mappiq(),
        " and ",
        sub.rafe(),
        "; the other is on the $dagesh-like dot in ",
        sub.waw(),
        ". $itm’s section starts at what is here the third paragraph.",
    ]
)
_MSS_L_S = sub.ms_lenin(), " and ", sub.ms_s_507()
_TABLE_DATA = [
    [hlp.hboloc("בׇּהְּשַׁמָּה֙", "@Lev 26:43"), _MSS_L_S],
    # no mappiq in MAM, but yes rafe in MAM: בׇּהְשַׁמָּהֿ֙
    [hlp.hboloc("פְּדַהְּאֵ֖ל", "@Nu 34:28"), sub.ms_s_507()],
    # no mappiq in MAM: פְּדַהְאֵ֖ל
    [hlp.hboloc("בְּתוֹכָֽהְּנָה׃", "@Ez 16:53"), sub.ms_lenin_10()],
    # no mappiq in MAM: בְּתוֹכָֽהְנָה׃
]
SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    sub.para(
        [
            "A $dagesh-like dot inside א or ה is called ",
            sub.mappiq(),
            ", and marks its letter as a consonant rather than a vowel ",
            hlp.paren(sub.mater_lectionis()),
            ". ",
            sub.rafe(cap=True),
            " on א or ה means ",
            hlp.dquotes(["not ", sub.mappiq(), ","]),
            " just as on other letters, ",
            sub.rafe(),
            " means ",
            hlp.dquotes(["not $dagesh."]),
            " I.e. ",
            sub.rafe(),
            " marks א or ה as a vowel ",
            hlp.paren(sub.mater_lectionis()),
            " rather than a consonant. ",
            sub.mappiq(cap=True),
            " and ",
            sub.rafe(),
            " on א and ה will be covered further in (i) and (ii) ",
            hlp.rtn_p(395),
            " respectively.",
        ]
    ),
    sub.para(
        [
            "A $dagesh-like dot in ",
            sub.waw(),
            " is either a $dagesh_xazaq or a ",
            sub.shureq(),
            " dot."
            " It is almost never hard to determine which of these meanings applies."
            " It is almost never necessary to determine the meaning of a ",
            [sub.rafe(), " on ", sub.waw()],
            ", because ",
            [sub.rafe(), " is almost never used on ", sub.waw()],
            ". But, there are exceptional cases motivating the uses of “almost” above."
            " In particular, the meanings of ",
            [hlp.hbo("וּוּ"), " and ", hlp.hbo("וֿוּ")],
            " are unclear, and will be covered in (iii) ",
            hlp.rtn_p(396),
            ".",
        ]
    ),
    sub.para(
        [
            "(i) ",
            sub.he(cap=True),
            " representing a consonant at the end of a word is marked by ",
            sub.mappiq(),
            ". ",
            sub.he(cap=True),
            " representing a vowel at the end of a word"
            " is generally (but not always) marked with ",
            sub.rafe(),
            ". In some manuscripts, consonantal ",
            sub.he(),
            " may be marked with ",
            sub.mappiq(),
            " even within a word, especially where it is pointed with $shewa as",
        ]
    ),
    hlp.table_std(_TABLE_DATA, coldirs=["rtl", "ltr"]),
]
