import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub
import yeivin_itm.content.my_yeivin_amisc_typed_table as tt

_DLOC_TWO_IN_2K_2 = hlp.make_dloc("@2K 2:1", "@2K 2:11")


# tdp: type_defn_pair
# tditc: type_defn_in_type_column
def _tditc(tdp_idx):
    return tt.type_defn_in_type_column(*_TYPE_DEFN_PAIRS[tdp_idx])


def _rtnp(num_of_sec):
    as_rich_text = " ", hlp.rtn_p(num_of_sec)
    return tt.str_cond(as_rich_text)


_TDP0 = [
    [hlp.hbo("הַֽנקלה")],
    [
        "On ",
        sub.he,
        " with ",
        sub.patax,
        " (or ",
        sub.rom_bkl,
        " with the vowel of the definite article) at the start of a word",
        _rtnp(348),
        ".",
    ],
]
_TDP1 = [
    [hlp.hbo("וּֽשלח")],
    ["On conjunctive ", sub.waw, " pointed as ", sub.shureq, _rtnp(349), "."],
]
_TDP2 = [[hlp.hbo("התִֽמלך")], ["On short-vowelled syllables", _rtnp(350), "."]]
_TYPE_DEFN_PAIRS = _TDP0, _TDP1, _TDP2
_DATA_ROWS = [
    [_tditc(0), hlp.some_hi(("הַֽנְקַלָּ֤ה", "הַֽ*נְקַ_*לָּ֤ה", "@1S 18:23"))],
    [sub.saa(), hlp.some_hi(("בַּֽסְעָרָ֖ה", "בַּֽ*סְעָ*רָ֖ה", _DLOC_TWO_IN_2K_2))],
    [
        sub.saa(),
        hlp.some_hi(("בַּֽנְחֻשְׁתַּ֔יִם", "בַּֽ*נְחֻ*שְׁתַּ֔יִם", "@Jud 16:21")),
    ],
    [_tditc(1), hlp.some_hi(("וּֽשְׁלַ֥ח", "וּֽ*שְׁלַ֥ח*", "@2K 9:17"))],
    [
        sub.saa(),
        hlp.some_hi(("וּֽטְהׇר־יָ֝דַ֗יִם", "וּֽ*טְהׇר־*יָ֝דַ֗יִם", "@Job 17:9")),
    ],  # qamats qatan
    [_tditc(2), hlp.some_hi(("הֲתִֽמְלֹ֔ךְ", "הֲתִֽ*מְלֹ֔ךְ*", "@Jer 22:15"))],
    [sub.saa(), hlp.some_hi(("אַֽרְזֵי־אֵֽל׃", "אַֽ*רְזֵי־*אֵֽל׃", "@Ps 80:11"))],
]
_TABLE_1 = hlp.table_std(_DATA_ROWS, coldirs=["rtl", "rtl"], arg_to_troh=["Type"])
SEC = [
    sub.para_with_initial_uah(
        ["$Shewa after Phonetic $Gaya in Other Situations"],
        [
            "$Shewa on other letters is vocal when it follows $pgaya. E.g.:",
        ],
    ),
    _TABLE_1,
    *tt.defn_table(_TYPE_DEFN_PAIRS),
    sub.para_paren(
        [
            "In the case of ",
            hlp.hbo("אַֽרְזֵי־אֵֽל׃"),
            sub.thspc(),
            " bA and bN agree that the $shewa is vocal.",
            # XXX turn the comment below into a footnote?
            # In ITM this just reads "In the latter case, ..."
            # but I infer that this means the Ps 80:11 case.
            # The whole remark seems a little out of place, since
            # bA/bN differences weren't under discussion.
            # XXX ask Avi about this
        ]
    ),
]
