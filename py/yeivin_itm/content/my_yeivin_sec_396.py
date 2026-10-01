from urllib import parse

import py_html.legacy_html as aht_html
import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_A_L = sub.ms_a_and_l()
_B_L = sub.ms_b_and_l()
_MSS_L_L13_S1 = sub.ms_lenin(), ", ", sub.ms_lenin_13(), ", ", sub.ms_s1_1053()
_TABLE_DATA_1 = [
    [
        hlp.hboloc("וַיִּֽשְׁתַּחֲוּ֖וּ", "@Dt 29:25"),
        _A_L,
    ],  # MAM וַיִּֽשְׁתַּחֲו֖וּ (no dot on 1st vav)
    [hlp.hboloc("טָוּ֖וּ", "@Ex 35:26"), _B_L],  # MAM טָו֖וּ (no dot on 1st vav)
    [
        hlp.hboloc("וְנִלְוּ֣וּ", "@Jer 50:5"),
        sub.ms_cairo(),
    ],  # MAM וְנִלְו֣וּ (no dot on 1st vav)
]


def _implicit(hbo_contents):
    return [
        "I think $itm is implicitly contrasting ",
        sub.ms_lenin(),
        " with manuscripts that have ",
        sub.waw(),
        " with ",
        sub.qibbuts(),
        " here, e.g. ",
        hlp.hbo(hbo_contents),
        " in ",
        sub.ms_s1_1053(),
        ".",
    ]


def _mamdoc_file_part(doc_page: str, fragment: str) -> str:
    """Build encoded MAM-doc file-part from readable page and fragment."""
    return f"{parse.quote(doc_page)}#{parse.quote(fragment, safe='')}"


def _subsec_for_table_2():
    _HBOLOC_SONG_5_2 = hlp.hboloc("קְוּצּוֹתַ֖י", "@Song 5:2")  # MAM קְוֻצּוֹתַ֖י
    _HBOLOC_SONG_5_11 = hlp.hboloc("קְוּצּוֹתָיו֙", "@Song 5:11")  # MAM קְוֻצּוֹתָיו֙
    _MSL_PAGE_424A = (
        "https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F424A.jpg"
    )
    ftnt_0 = sub.footnote(_implicit("קְוֻצּוֹתַ֖י"))
    ftnt_1 = sub.footnote(
        [
            ["In ", sub.ms_lenin(), ", there is quite possibly a ", sub.qibbuts()],
            [" under the dotted ", sub.waw(), " in ", _HBOLOC_SONG_5_2],
            [
                ", i.e. the word is quite possibly ",
                hlp.hbo("קְוֻּצּוֹתַ֖י"),
                sub.thspp(),
            ],
            [" See ", aht_html.anchor("page 424A", {"href": _MSL_PAGE_424A})],
            ", column 2, line 25 of 26. And see the ",
            sub.mamdoc(_mamdoc_file_part("E1-Song of Songs.html", "c5v2")),
            ".",
        ]
    )
    ftnt_2 = sub.footnote(_implicit("קְוֻצּוֹתָיו֙"))
    data_rows_for_table_2 = [
        [_HBOLOC_SONG_5_2, [ftnt_0, ", ", ftnt_1]],
        [_HBOLOC_SONG_5_11, ftnt_2],
    ]
    return hlp.table_std(data_rows_for_table_2, coldirs=["rtl", "ltr"])


_JER_3_17_MS_L = sub.xxx_hbo_in_parens(sub.ms_lenin(), "וְנִקְוּ֨וּ")
_TABLE_DATA_3 = [
    [hlp.hboloc("וְתַשְׁוֿ֑וּ", "@Is 46:5"), sub.ms_cairo()],  # MAM וְתַשְׁו֑וּ
    [
        hlp.hboloc("וְנִקְוֿ֨וּ", "@Jer 3:17"),
        sub.ms_lenin_15(),
        _JER_3_17_MS_L,
    ],  # MAM וְנִקְו֨וּ
]


def _subsec_for_table_4():
    _HBOLOC_GEN_46_13 = hlp.hboloc("וּפֻוָּ֖ה", "@Gen 46:13")  # MAM וּפֻוָ֖ה
    ftnt_0 = sub.footnote(
        [
            "Here $itm doesn’t spell out what different way of pronouncing consonantal ",
            sub.waw(),
            " is shown by ",
            sub.ms_lenin(),
            " in ",
            _HBOLOC_GEN_46_13,
            ". It may be relevant that ",
            sub.ms_lenin(),
            " is an outlier in its use of a dot in ",
            hlp.hbo("וָּ֖"),
            sub.thspc(),
            " with ",
            hlp.hbo("וּפֻוָ֖ה"),
            " being the consensus pointing of this word.",
        ]
    )
    ftnt_1 = sub.footnote(
        [
            "Here $itm doesn’t spell out what different way of pronouncing consonantal ",
            sub.waw(),
            " is shown by רבבן and רוון,"
            " but I think it has to do with"
            " a pronunciation in which ",
            sub.vet(),
            " and ",
            sub.waw(),
            " have distinct sounds. In such a pronunciation, the two ",
            sub.qere(),
            " in the Mp notes he cites would be ",
            hlp.hbo("רִבְֿבָ֖ן"),
            " and ",
            hlp.hbo("רִוְֿוָ֖ן"),
            sub.thspp(),
            " ",
            hlp.paren(
                [
                    "I’m guessing that the ",
                    sub.rafe(),
                    " should be carried over “as is” when forming the pointed ",
                    sub.qere(),
                    ", but I’m not at all sure about that.",
                ]
            ),
        ]
    )
    _THE_WAW_FOLLOWS = (
        "The ",
        sub.waw(),
        " follows a /u/ ",
        hlp.ftntjoin("vowel.", ftnt_0),
    )
    _THE_MP_OF_L = hlp.line_break(
        ["The Mp of ", sub.ms_lenin(), " has רבבן ק̇ בן אשר (as BHK)."],
        ["The Mp of ", sub.ms_lenin_13(), " ", hlp.ftntjoin("has רוון ק̇.", ftnt_1)],
    )
    _TABLE_DATA_4 = [
        [_HBOLOC_GEN_46_13, sub.ms_lenin(), _THE_WAW_FOLLOWS],
        [hlp.hboloc("רִבְֿוָ֖ן", "@Dan 7:10"), _MSS_L_L13_S1, _THE_MP_OF_L],
        # MAM ketiv and qere are רבון and רִבְבָ֖ן
    ]
    return hlp.table_std(_TABLE_DATA_4, coldirs=["rtl", "ltr", "ltr"])


SEC = [
    sub.para(
        [
            "(iii) ",
            sub.waw(cap=True),
            " representing a consonant followed by ",
            sub.shureq(),
            " at the end of a word"
            " is often marked with a dot, possibly"
            " also indicating ",
            sub.shureq(),
            ". E.g.:",
        ]
    ),
    hlp.table_std(_TABLE_DATA_1, coldirs=["rtl", "ltr"]),
    sub.para(
        [
            "This appears to indicate that this ",
            sub.waw(),
            " was assimilated to the following ",
            sub.shureq(),
            ", and pronounced as a long /u/"
            " vowel, i.e. /wu/ became /uu/ or /u/."
            " This phenomenon can occur not only at the end of a word but also"
            " within a word, as in the following words in ",
            sub.ms_lenin(),
            ":",
        ]
    ),
    _subsec_for_table_2(),
    sub.para(
        [
            "In some other cases, consonantal ",
            sub.waw(),
            " before ",
            sub.shureq(),
            " is marked not with a dot but with the ",
            sub.rafe(),
            " sign. E.g.:",
        ]
    ),
    hlp.table_std(_TABLE_DATA_3, coldirs=["rtl", "ltr", "ltr"]),
    sub.para(
        [
            "It is not clear whether this ",
            sub.rafe(),
            " was intended to mark its ",
            sub.waw(),
            " as a consonant or a vowel.",
        ]
    ),
    sub.para(
        [
            "Different ways of pronouncing consonantal ",
            sub.waw(),
            " are recorded in the Masorah also in",
        ]
    ),
    _subsec_for_table_4(),
]
