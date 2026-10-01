import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_HBO_PARTS_OF_LBI1 = [
    "תִּֽהְיֶינָה",  # e.g. תִּֽהְיֶ֔ינָה in Is 17:2
    "תִּֽהְיֶה",  # e.g. תִּֽהְיֶ֔ה in Dt 18:13
    "יִֽהְיֶה",  # e.g. יִֽהְיֶ֔ה in 2C 6:28
    "יִֽהְיוּ",  # e.g. יִֽהְי֔וּ in Is 5:9
    "נִֽהְיָתָה",  # e.g. וְנִֽהְיָ֔תָה in Ez 21:12 and Ez 39:8
    "וֶֽהְיֵה",  # e.g. וֶֽהְיֵה־לִי֮ in Jud 17:10
    "וִֽהְיוּ",  # e.g. וִֽהְיוּ֙ in 2S 2:7
    "מִֽהְיוֹתְךָ",  # e.g. מִֽהְיוֹתְךָ֥ in Isa.49.6
    "בִּֽהְיוֹתוֹ",  # e.g. בִּֽהְיוֹת֣וֹ in Ez 15:5
    "לִֽהְיוֹת",  # e.g. לִֽהְיוֹת֙ in Mic 5:1
    "תִּֽהְיוּ",  # e.g. תִּֽהְיוּ֙ in 1S 14:40
]
_HBO_PARTS_OF_LBI2 = [
    "וַֽיְחִי",
    "וַֽיְהִי",
]  # e.g. וַֽיְחִי־שֵׁ֕ת in Gen 5:6  # e.g. וַֽיְהִי֙ in 1C 6:51
_FINAL_TABLE_ROW_DATA = [
    [hlp.lhbo("@Ez 45:8", "יִֽהְיֶה־לּ֥וֹ")],
    [hlp.lhbo("@Jer 7:23", "תִּֽהְיוּ־לִ֣י")],
    [hlp.lhbo("@Gen 1:5", "וַֽיְהִי־עֶ֥רֶב וַֽיְהִי־בֹ֖קֶר")],
]


def _table_of_hbos(hbos):
    return hlp.table_std_rtl(list(map(_table_row_of_single_hbo, hbos)))


def _table_row_of_single_hbo(hbo_string):
    return [hlp.hbo(hbo_string)]


_LIST_BENEATH_ITEM_1 = _table_of_hbos(_HBO_PARTS_OF_LBI1)
_LIST_BENEATH_ITEM_2 = _table_of_hbos(_HBO_PARTS_OF_LBI2)
_TABLE_1 = hlp.table_std_rtl(_FINAL_TABLE_ROW_DATA)
SEC = [
    sub.para_with_romnum_and_initial_uah(
        "ii",
        sub.cmn_354_lcromnum_ii(),
        [
            "$Gaya is used"
            " in many forms from these roots to prevent the slurring over of"
            " the ",
            sub.he(),
            " or ",
            sub.xet(),
            ". It occurs in two classes of forms:",
        ],
    ),
    sub.para(
        [
            "1. Before ",
            sub.he(),
            " or ",
            sub.xet(),
            " with $shewa. E.g.:",
        ]
    ),
    _LIST_BENEATH_ITEM_1,
    sub.para(["and so on (and in the corresponding forms from חיה)."]),
    sub.para(
        [
            "2. Before the ",
            sub.yod(),
            " of the pronomial prefix where it has $shewa, as in",
        ]
    ),
    _LIST_BENEATH_ITEM_2,
    sub.para(
        [
            "This $gaya is most commonly used where the word has a disjunctive accent,"
            " but may also occur with conjunctives."
            " The tendency to mark it differs in different forms,"
            " and it is not consistent in individual manuscripts,"
            " nor is its use uniform in any group of manuscripts,"
            " and it is not in the lists of ",
            sub.xillufim(),
            ". This $gaya is, however, as a rule, marked consistently"
            " when the word in question is joined by $maqqef to an initially-stressed word as",
        ]
    ),
    _TABLE_1,
]
