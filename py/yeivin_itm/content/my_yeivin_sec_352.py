import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp
import py_html.legacy_html as aht_html

_HE_MTG_CGJ_QMTS_RESH_SHEWA = "הֽ͏ָרְ"
_BL_S = sub.ms_b_and_l(), "הָרֲ", sub.ms_s_507(), _HE_MTG_CGJ_QMTS_RESH_SHEWA


def _x_hbox_y_hboy_in_parens(xxx, hbox, yyy, hboy):
    sxxx = aht_html.flatten_nn(xxx)
    syyy = aht_html.flatten_nn(yyy)
    return hlp.paren_tt([*sxxx, " ", hlp.hbo(hbox), ", ", *syyy, " ", hlp.hbo(hboy)])


_CONT_FTNT_IN_TABLE_1 = [
    ["Here $itm claims that there is a $gaya"],
    [" (a right $gaya in fact)"],
    [" on ", sub.he(), " in ", sub.ms_s_507()],
    [" ", hlp.paren_tt(hlp.hbo(_HE_MTG_CGJ_QMTS_RESH_SHEWA))],
    [" but Breuer (in ", hlp.rom("Daʿat Miqra"), ")"],
    [" and the ", sub.mamdoc("A4-Numbers.html#c16v32")],
    [" disagree with $itm on that point."],
]


def _table_1_data():
    ftnt = sub.footnote(_CONT_FTNT_IN_TABLE_1)
    return [
        [
            hlp.lhbo("@Job 31:37", "אֲקָֽרְבֶֽנּוּ׃"),
            sub.xxx_hbo_in_parens("some manuscripts", "רֲ"),
        ],
        # XXX check the answer to the implied question "I wonder ..." below.
        # I wonder whether Aleppo has xaṭef patax. If so, MAM should have varika.
        [
            hlp.lhbo("@Nu 16:32", "כׇּל־הָרְכֽוּשׁ׃"),
            _x_hbox_y_hboy_in_parens(*_BL_S),
            ftnt,
        ],
    ]


_CONT_FTNT_0_IN_TABLE_2 = [
    ["Oddly, $itm provides no examples"],
    [" having ", hlp.hbo("שֲׁ"), sub.thspp()],
]


def _table_2_data():
    ftnt_0 = sub.footnote(_CONT_FTNT_0_IN_TABLE_2)
    ftnt_1 = sub.footnote(sub.surprising_long_xiriq("רִֽצְפַ֥ת"))
    return [
        [hlp.lhbo("@Jer 22:28", "הֽוּטְלוּ֙"), sub.ms_a_x_patax("ט"), ""],
        [hlp.lhbo("@Ez 9:8", "וְנֵֽאשְׁאַ֖ר"), ftnt_0, ""],
        [
            hlp.lhbo("@Est 1:6", "רִֽצְפַ֥ת"),
            sub.xxx_hbo_in_parens("many manuscripts", "צֲ"),
            ftnt_1,
        ],
    ]


_CONT_FTNT_SUBSEC_1 = ["The root ירד is not mentioned in ", hlp.rtn(379), "."]
_FTNT_SUBSEC_1 = sub.footnote(_CONT_FTNT_SUBSEC_1)
_CONT_PARA_SUBSEC_1 = [
    ["and so often in forms from the roots "],
    [hlp.comma_list_of_bdis("ברך", "גרשׁ", "and ירד")],
    [" ", hlp.rtn_p(379), hlp.ftntjoin(".", _FTNT_SUBSEC_1)],
]


_FTNT_LIBERTIES = sub.footnote(
    [
        "I reworded $itm’s inference, which runs “so that it can be assumed"
        " that ...”, as “This makes it likely that ...”."
        " I also added the manuscript annotations in the middle column of"
        " each table below; $itm gives the examples without them.",
    ]
)
_CONT_PARA_1 = [
    ["Generally, when a word has $gaya"],
    [" on a syllable with ", sub.alvb_simshewa(), ","],
    [" that $gaya is musical ", hlp.rtn_p(326), "."],
    [" However, sometimes such a word appears in other manuscripts with a"],
    [" $x_shewa."],
    [" This makes it likely that the $gaya"],
    [" in the manuscript with $simshewa is phonetic rather than musical."],
    [" Some examples before ", sub.resh(), " are:"],
]

_CONT_PARA_LAST = [
    ["and so also in certain circumstances in forms from the roots"],
    [" ", hlp.comma_list_of_bdis("אכל", "הלך"), ", and others ", hlp.rtn_p(380), "."],
]

SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    sub.para(_CONT_PARA_1),
    hlp.table_std(_table_1_data(), coldirs=["rtl", "ltr", "ltr"]),
    sub.para(_CONT_PARA_SUBSEC_1),
    sub.para(["Before letters other than ", sub.resh(), ":"]),
    hlp.table_std(_table_2_data(), coldirs=["rtl", "ltr", "ltr"]),
    sub.para(_CONT_PARA_LAST),
]
