import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub


def _naftali(hbo_contents):
    return sub.xxx_hbo_in_parens("bN", hbo_contents)


_FTNT_LIBERTIES = sub.footnote(
    [
        "I framed this section around $shewa-separated ",
        sub.begad_kefat(),
        " pairs, where $itm says “pairs of similar consonants”."
        " I also added the parenthetical note that such a pair would otherwise"
        " have identical or similar sounds, and the framing that presents the"
        " closing bN material as a related quirk rather than as more of the same.",
    ]
)
_TABLE_DATA_GEN_39_12 = [
    ("וַתִּתְפְּשֵׂ֧הוּ בְּבִגְד֛וֹ", "@Gen 39:12"),
    ("הֲלֹ֥א כְּכַרְכְּמִ֖ישׁ", "@Is 10:9"),
    ("וְאִכָּבְדָ֤ה בְּפַרְעֹה֙", "@Ex 14:4"),
]
_TABLE_DATA_LEV_21_13 = [[hlp.hboloc("אִשָּׁ֥ה בִבְתוּלֶ֖יהָ", "@Lev 21:13")]]
_TABLE_DATA_DT_23_8 = [
    ("לֹא־תְתַעֵ֣ב", "@Dt 23:8", "(2× in this verse)"),
    # MAM has לֹֽא־תְתַעֵ֣ב (gaʿya on ל) for instance 1 of 2
    ("וּבְנֵ֣י דְדָ֔ן", "@Gen 25:3", ""),
]
_TABLE_DATA_EZ_17_10 = [[hlp.hboloc("הֲלֹא֩ כְגַ֨עַת", "@Ez 17:10"), _naftali("כְּ")]]
_TABLE_DATA_GEN_19_17 = [
    [hlp.hboloc("וַיְהִי֩ כְהוֹצִיאָ֨ם", "@Gen 19:17"), _naftali("כְּ")]
]
# _FTNT_FOR_JOS_9_1 = sub.footnote([
#     'This case seems doubly-exceptional since the ',sub.kaf(),' '
#     'in question has ',sub.xireq(),' rather than ',"$shewa",'.'
# ])
_TABLE_DATA_GEN_39_15 = [
    [hlp.hboloc("וַיְהִ֣י כְשׇׁמְע֔וֹ", "@Gen 39:15"), _naftali("כְּ")],
    [hlp.hboloc("וַיְהִ֣י כִשְׁמֹ֣עַ", "@Jos 9:1"), _naftali("כִּ")],
]
_THE_3_STD_PAIRS = (
    hlp.hbo("בְב"),
    sub.thspc(),
    " ",
    hlp.hbo("בְפ"),
    sub.thspc(),
    " or ",
    hlp.hbo("כְכ"),
)
SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    sub.para(
        [
            sub.pseudo_heading(
                ["Certain $shewa-separated ", sub.begad_kefat(), " pairs"]
            ),
            ""
            " at the start of the second word also nullify the rule."
            " If the second word starts with ",
            *_THE_3_STD_PAIRS,
            sub.thspc(),
            " the initial ",
            sub.bet(),
            " or ",
            sub.kaf(),
            " has $dagesh even if"
            " the preceding word ends with a vowel and has a conjunctive accent."
            " ",
            hlp.paren(
                [
                    "Note that these pairs would have identical or similar sounds,"
                    " were it not for this exceptional $dagesh.",
                ]
            ),
            " E.g.:",
        ]
    ),
    hlp.table_std_alpha_beta_2col_std(_TABLE_DATA_GEN_39_12, arg_to_troh=None),
    sub.para(
        [
            "When the initial ",
            sub.bet(),
            " or ",
            sub.kaf(),
            " does not have $shewa, it is $dagesh-free,"
            " as expected according to the general rule. E.g.:",
        ]
    ),
    hlp.table_std_rtl(_TABLE_DATA_LEV_21_13),
    sub.para(
        [
            "When other pairs of identical or similar ",
            sub.begad_kefat(),
            " letters occur, even if the first has $shewa, the first is usually $dagesh-free,"
            " as expected according to the general rule. E.g.:",
        ]
    ),
    hlp.table_std_alpha_beta_3col_std(_TABLE_DATA_DT_23_8, arg_to_troh=None),
    sub.para(
        [
            "Some manuscripts expand the set of applicable pairs beyond ",
            *_THE_3_STD_PAIRS,
            sub.thspp(),
            " They may include pairs such as ",
            hlp.hbo("בְמ"),
            " and ",
            hlp.hbo("כְג"),
            " in the set of pairs whose first letter gets $dagesh even though"
            " the preceding word ends with a vowel and has a conjunctive accent."
            " E.g. in the following words, we can see a bA/bN split on this issue,"
            " with bN including ",
            hlp.hbo("כְג"),
            " in the set of applicable pairs:",
        ]
    ),
    hlp.table_std(_TABLE_DATA_EZ_17_10, coldirs=["rtl", "ltr"]),
    sub.para(
        [
            "A related quirk of bN deserves mention here, though"
            " it does not involve initial ",
            sub.begad_kefat(),
            " pairs. ",
            hlp.paren(["It does involve initial ", sub.kaf(), " though."]),
            " According to the general rule, a ",
            sub.begad_kefat(),
            " letter is $dagesh-free if it occurs"
            " at the start of a word following ויהי with a conjunctive accent."
            " However the ",
            sub.sefer_ha_xillufim(),
            " notes seven cases where ben Naftali gives a ",
            sub.kaf(),
            " a $dagesh in such a situation. In three of these cases, the accent on ויהי is ",
            sub.telisha_qetannah(),
            ". E.g.:",
        ]
    ),
    hlp.table_std(_TABLE_DATA_GEN_19_17, coldirs=["rtl", "ltr"]),
    sub.para(["But in the other four cases the accent is another conjunctive. E.g.:"]),
    hlp.table_std(_TABLE_DATA_GEN_39_15, coldirs=["rtl", "ltr"]),
]
