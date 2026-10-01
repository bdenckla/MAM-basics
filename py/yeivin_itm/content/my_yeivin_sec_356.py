import mb_cmn.my_utils as my_utils
import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub


def _pseudo_list(items):
    list_of_lists = list(map(_pseudo_list_item, enumerate(items)))
    flat = my_utils.sum_of_seqs(list_of_lists)
    return flat


def _pseudo_list_item(item_enum):
    idx, item = item_enum
    intro, table_rows = item
    para_contents = [f"{idx+1}) ", *intro]
    return [sub.para(para_contents), hlp.table_std_rtl(table_rows)]


_PL_ITEM_1_INTRO = sub.dol(
    [
        "Musical $gaya_cs with regular structure ",
        sub.afr4(),
        " ",
        hlp.rtn_p(322),
        " and $pgaya before an identical pair of letters.",
    ]
)
_PL_ITEM_1_TABLE_ROWS = [
    [hlp.lhbo("@Job 42:10", "בְּהִֽתְפַּֽלְל֖וֹ")],
    [hlp.lhbo("@2C 7:14", "וְיִֽתְפַּֽלְלוּ֙")],
]
_PL_ITEM_2_INTRO = sub.dol(
    [
        "Musical $gaya_os, and $pgaya on forms from היה and חיה.",
    ]
)
_PL_ITEM_2_TABLE_ROWS = [
    [hlp.lhbo("@Ez 13:9", "לֹֽא־יִֽהְי֗וּ"), "", hlp.span_ltr("mus. then phon.")],
    [
        hlp.lhbo("@Ez 36:3", "לִֽהְיֽוֹתְכֶ֤ם"),
        sub.ms_aleppo(),
        hlp.span_ltr("phon. then mus."),
    ],
]
_PL_ITEM_3_INTRO = sub.dol(
    [
        "Phonetic $gaya on ",
        sub.he(),
        " with ",
        sub.patax(),
        " before ",
        sub.mem(),
        ", and $pgaya before an identical pair of letters.",
    ]
)
_PL_ITEM_3_TABLE_ROWS = [
    [hlp.lhbo("@Jud 7:7", "הַֽמְלַֽקְקִים֙"), sub.ms_aleppo()]
    # MAM lacks the gaʿya in question (the gaʿya on ל)
]
_AND_PHON = "and $pgaya on a guttural-closed syllable."
_PL_ITEM_4_INTRO = sub.dol(
    [
        "Musical $gaya_os ",
        hlp.rtn_p(326),
        " ",
        _AND_PHON,
    ]
)
_PL_ITEM_4_TABLE_ROWS = [[hlp.lhbo("@Lam 5:5", "הֽוּנַֽח־לָֽנוּ׃")]]
_PL_ITEM_5_INTRO = sub.dol(
    [
        "Musical $gaya_cs ",
        hlp.rtn_p(323),
        " ",
        _AND_PHON,
    ]
)
_PL_ITEM_5_TABLE_ROWS = [
    [hlp.lhbo("@1C 7:3", "יִֽזְרַֽחְיָ֑ה")],
    [hlp.lhbo("@Is 38:4", "אֶֽל־יְשַֽׁעְיָ֖הוּ")],
    [hlp.lhbo("@Jer 44:17", "וַנִּֽשְׂבַּֽע־לֶ֙חֶם֙")],
    [hlp.lhbo("@Ho 4:17", "הַֽנַּֽח־לֽוֹ׃")],
    [hlp.lhbo(hlp.make_dloc("@1C 2:19", "@2C 11:18"), "וַיִּֽקַּֽח־ל֤וֹ")],
    [hlp.lhbo("@2C 2:7", "וּֽשְׁלַֽח־לִי֩")],
]
_PL_ITEM_6_INTRO = sub.dol(
    [
        "Musical $gaya with $shewa ",
        hlp.rtn_p(333),
        " ",
        _AND_PHON,
    ]
)
_PL_ITEM_6_TABLE_ROWS = [
    [hlp.lhbo("@Neḥ 6:10", "שְֽׁמַֽעְיָ֧ה"), sub.ms_lenin()],  # Aleppo is missing here
    [hlp.lhbo(hlp.make_dloc("@1S 22:12", "@Jer 37:20"), "שְֽׁמַֽע־נָ֖א")],
    [hlp.lhbo("@2C 2:6", "שְֽׁלַֽח־לִ֣י")],
]
SEC = [
    sub.para(
        [
            "In ",
            hlp.rtn(339),
            " we noted that only one $mgaya",
            " was normally marked on a word, even where more than one could be marked."
            " This is not, however, the case where a $pgaya",
            " is involved. In this case two $gayas",
            " are marked on the same word even in manuscripts like ",
            sub.ms_a_and_l(" and "),
            ", where this is otherwise very rare."
            " Examples of different combinations of $gayas",
            " are given below:",
        ]
    ),
    *_pseudo_list(
        [
            (_PL_ITEM_1_INTRO, _PL_ITEM_1_TABLE_ROWS),
            (_PL_ITEM_2_INTRO, _PL_ITEM_2_TABLE_ROWS),
            (_PL_ITEM_3_INTRO, _PL_ITEM_3_TABLE_ROWS),
            (_PL_ITEM_4_INTRO, _PL_ITEM_4_TABLE_ROWS),
            (_PL_ITEM_5_INTRO, _PL_ITEM_5_TABLE_ROWS),
            (_PL_ITEM_6_INTRO, _PL_ITEM_6_TABLE_ROWS),
        ]
    ),
    sub.para(
        [
            "This system of marking the two $gayas",
            " on one word is not"
            " common to all the early manuscripts."
            " In some only one $gaya",
            " is marked, either the musical or the phonetic.",
        ]
    ),
]
