import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_TABLE_1_DATA = [
    [hlp.lhbo("@Ez 31:7", "וַיְּיִ֣ף", hlp.hbo_attr_for_els())],
    [hlp.lhbo("@2C 31:7", "לְיִסּ֑וֹד", hlp.hbo_attr_for_els())],
]
_EXPECTED = ["וַיִּ֣יף", "לִיסּ֑וֹד"]
_TABLE_2_DATA = [
    [hlp.lhbo("@1S 2:10", "וִיתֶּן־עֹ֣ז")],  # MAM has וְיִתֶּן־עֹ֣ז
    [hlp.lhbo("@Is 57:13", "וִירָ֖שׁ")],
    # MAM has וְיִירַ֖שׁ
    # (in addition to the expected difference of וְיִ not וִי,
    # (MAM has two yods not one, and MAM has patax not qamats)
]
_TABLE_2 = hlp.table_std_rtl(_TABLE_2_DATA)
SEC = [
    sub.para(
        [
            "Most of the early manuscripts conform to bA in the pointing of these words,"
            " but ",
            sub.ms_cairo(),
            ", and in the main ",
            sub.ms_s_507(),
            ", conform to bN.",
        ]
    ),
    sub.para(
        [
            "There are a few words in the Bible pointed with $shewa before ",
            sub.yod(),
            " with ",
            sub.xireq(),
            " where long /i/ would be expected. E.g.:",
        ]
    ),
    hlp.table_std_rtl(_TABLE_1_DATA),
    sub.para(
        [
            hlp.paren(
                [
                    "The expected pointings would be ",
                    hlp.hbo_els(_EXPECTED[0]),
                    " and ",
                    hlp.hbo(_EXPECTED[1]),
                    ".",
                ]
            ),
            ""
            " This is possibly the result of over-correction: perhaps the long /i/"
            " was avoided even where it should have been used.",
        ]
    ),
    sub.para(
        [
            "In these situations,"
            " manuscripts with expanded Tiberian pointing"
            " use a system related to the system of bN."
            " But these manuscripts use the pointing for long /i/ when any prefix"
            " precedes ",
            sub.yod(),
            " with ",
            sub.xireq(),
            ". Thus, in contrast to the real system of bN, in ",
            sub.ms_reuch(),
            " we find the following:",
        ]
    ),
    _TABLE_2,
]
