import py_html.legacy_html as aht_html
import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_LAM_5_6_BASE = "לִשְׂבֹּ֥עַֽ־"
_IS_59_16_BASE = "וַתּ֤וֹשַֽׁע־"
_LAM_5_6_LOCALE_AND_HEBREW = "@Lam 5:6", _LAM_5_6_BASE + "לָֽחֶם׃"
_IS_59_16_LOCALE_AND_HEBREW = "@Is 59:16", _IS_59_16_BASE + "לוֹ֙"
_TH_E = aht_html.table_header("")  # table header [that is] empty
_TABLE_1 = hlp.table_std(
    [
        [
            sub.dol(["$gaya on a final open syllable"]),
            hlp.rtn(332),
            hlp.lhbo("@Jer 49:23", "בּ֤וֹשָֽׁה־חֲמָת֙"),
            sub.ms_cairo(),
            # MAM has space rather than maqqef, i.e. MAM has בּ֤וֹשָֽׁה חֲמָת֙.
            # This is not surprising since the maqqef version is attributed by ITM to C,
            # implying that the maqqef version is not the consensus version.
        ],
        [
            sub.dol(["$gaya on a final closed ", sub.slv()]),
            hlp.rtn(338),
            hlp.lhbo("@Nu 24:22", "לְבָ֣עֵֽר־קָ֑יִן"),
            sub.ms_s_507(),
            # MAM has space rather than maqqef, i.e. MAM has לְבָ֣עֵֽר קָ֑יִן.
            # This is not surprising since the maqqef version is attributed by ITM to S,
            # implying that the maqqef version is not the consensus version.
        ],
        [
            sub.dol(["$pgaya on a guttural-closed syllable"]),
            hlp.rtn(354),
            hlp.lhbo(*_IS_59_16_LOCALE_AND_HEBREW),
            sub.ms_a_and_c(),
        ],
        [
            sub.saa(),
            sub.saa(),
            hlp.lhbo(*_LAM_5_6_LOCALE_AND_HEBREW),
            sub.ms_lenin_13(),
            # MAM has space rather than maqqef, i.e. MAM has לִשְׂבֹּ֥עַֽ לָֽחֶם׃.
            # This is not surprising since the maqqef version is attributed by ITM to L13,
            # implying that the maqqef version is not the consensus version.
        ],
    ],
    arg_to_troh=["context", "sec", "example", ""],
)
SEC = [
    sub.para(
        [
            "In some manuscripts $maqqef is marked",
            sub.emdash(),
            "sometimes consistently, sometimes sporadically",
            sub.emdash(),
            "after a $gaya",
            " after a conjunctive stress. This occurs in the following contexts:",
        ]
    ),
    _TABLE_1,
    sub.para_paren(
        [
            "It may not be clear at first glance that ",
            hlp.hbo(_LAM_5_6_BASE),
            " matches the pattern."
            " But this is just an artifact of the notation for furtive ",
            sub.patax(),
            ". The word’s sequence of sounds matches the pattern. ",
        ]
    ),
    sub.para(
        [
            "The purpose of this $maqqef is to indicate that, even though $gaya",
            " is marked after the stress, so that the reading of"
            " that syllable must be slowed down, the word must be joined to"
            " the next word, and no break should be made between them."
            " That is, $gaya sometimes indicates a pause of some sort. The",
            " $maqqef is used to show that no pause should be made in these cases."
            " As is said in Nutt, 1870, text p. 129 (ascribed to Ḥayyuj) ",
            hlp.dquotes(
                "$Gaya is the opposite of $maqqef,"
                " because $maqqef joins words while $gaya separates them."
            ),
        ]
    ),
]
