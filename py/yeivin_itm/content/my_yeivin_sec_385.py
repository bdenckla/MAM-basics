import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub
import yeivin_itm.content.my_yeivin_amisc_sec_385_footnotes as ftnts


def _vosq(vosq_struct):  # vocal or silent question
    return hlp.line_break(
        (
            [
                hlp.some_hi_no_loc((vosq_struct["norm"], vosq_struct["star-silent"])),
                sub.thspq(),
            ]
        ),
        (
            [
                hlp.some_hi_no_loc((vosq_struct["norm"], vosq_struct["star-vocal"])),
                sub.thspq(),
            ]
        ),
    )


def _vosq_nl(vosq_struct):
    return vosq_struct["norm"], vosq_struct["loc"]


def _vosq_nsl(vosq_struct, starn):
    return vosq_struct["norm"], vosq_struct[starn], vosq_struct["loc"]


_CF_L20 = hlp.paren(hlp.compare_with(sub.ms_lenin_20(), "מֲמ"))
_PRES = sub.dol(["$gaya present"])
_ABS = sub.dol(["$gaya absent"])
_XS_WHERE_GP = sub.x_shewa(), _PRES
_XS_WHERE_GA = sub.x_shewa(), _ABS
_SS_WHERE_GP = sub.simshewa(), _PRES
_SS_WHERE_GA = sub.simshewa(), _ABS
_CONSISTENT_DATA = [
    ["", hlp.some_hi(("וְהִֽלֲל֖וּ", "וְהִֽ*לֲל֖וּ*", "@Is 62:9")), *_XS_WHERE_GP],
    ["", hlp.some_hi(("מִתּֽוֹכֲךָ֙", "מִתּֽוֹ*כֲךָ֙*", "@Is 58:9")), *_XS_WHERE_GP],
    [_vosq(ftnts.DT_33_2), hlp.hboloc(*_vosq_nl(ftnts.DT_33_2)), *_SS_WHERE_GA],
    [_vosq(ftnts.JER_51_48), hlp.hboloc(*_vosq_nl(ftnts.JER_51_48)), *_SS_WHERE_GA],
]
_INCONSISTENT_DATA = [
    [
        _vosq(ftnts.JER_25_12),
        hlp.hboloc(*_vosq_nl(ftnts.JER_25_12)),
        *_SS_WHERE_GP,
        _CF_L20,
    ],
    ["", hlp.some_hi(ftnts.IS_59_10), *_XS_WHERE_GA],
    ["", hlp.some_hi(ftnts.JER_51_53), *_XS_WHERE_GA],
]
_RESOLUTIONS = [
    [
        hlp.some_hi(_vosq_nsl(ftnts.DT_33_2, "star-silent")),
        sub.dol(["silent: follows a $gaya-free short vowel"]),
    ],
    [
        hlp.some_hi(_vosq_nsl(ftnts.JER_51_48, "star-vocal")),
        sub.dol(["vocal: follows a long vowel"]),
    ],
    [
        hlp.some_hi(_vosq_nsl(ftnts.JER_25_12, "star-vocal")),
        sub.dol(["vocal: follows a $gaya-marked short vowel"]),
    ],
]


def _rule_d1_part_1():
    return hlp.line_break(
        sub.dol(["A $shewa on the first of an identical pair of letters"]),
        sub.dol(
            [
                " is vocal if it follows $gaya",
                hlp.ftntjoin(" or the stress.", ftnts.FTNT_1),
            ]
        ),
    )


_RULE_D1_PART_1_EXAMPLES = [
    hlp.some_hi(("יִֽלְלַ֣ת", "יִֽ*לְלַ֣ת*", "@Zech 11:3")),
    hlp.some_hi(("לָֽקְק֤וּ", "לָֽ*קְק֤וּ*", "@1K 21:19")),
    # MAM has no gaʿya on ל.
]
_RULE_D1_PART_2 = sub.dol(["Otherwise, such a $shewa is silent."])
_RULE_D1_PART_2_EXAMPLES = [
    hlp.some_hi(("הִנְנִ֨י", "*הִנְ*נִ֨י", "@Ex 10:4")),  # I added accent and locale
    hlp.some_hi(("הִנְנ֣וּ", "*הִנְ*נ֣וּ", "@Jos 9:25")),  # I added accent and locale
    # Above, I added accent and locale since stress is at issue
    hlp.some_hi(("חִקְקֵי־אָ֑וֶן", "*חִקְ*קֵי־אָ֑וֶן", "@Is 10:1")),
]


def _rule_d1_part_3():
    return hlp.line_break(
        [
            "Except, in six ",
            hlp.ftntjoin("words", ftnts.FTNT_FOR_THE_SIX),
            sub.dol([" such a $shewa"]),
            hlp.ftntjoin(" is silent", ftnts.FTNT_3),
        ],
        [" even though it follows the stress."],
    )


_RULE_D1_PART_3_EXAMPLE = hlp.some_hi(ftnts.EXCEPTION_1_OF_6)


# The following regex "([א-ת][\u05c1\u05c2]?)\u05b0\1\u05b4[^\u0591-\u05af\u05bd]* "
# also turned up these two words, when searching for the six exceptions:
#
# ה֭וֹלְלִים Ps 5:6
# לַ֭הוֹלְלִים Ps 75:5
#
# But these two words seem like false positives due to lack of a dexi stress helper.
#
def _data_for_table_for_rule_d1():
    return [
        [_rule_d1_part_1(), hlp.line_break(*_RULE_D1_PART_1_EXAMPLES)],
        [_RULE_D1_PART_2, hlp.line_break_seq(_RULE_D1_PART_2_EXAMPLES)],
        [_rule_d1_part_3(), _RULE_D1_PART_3_EXAMPLE],
    ]


def _table_for_rule_d1():
    return hlp.table_std(
        _data_for_table_for_rule_d1(),
        coldirs=["ltr", "rtl"],
        arg_to_troh=["", "Example(s)"],
    )


_TABLE_2 = hlp.table_std(_CONSISTENT_DATA, coldirs=["rtl", "rtl", "ltr", "ltr"])
_TABLE_3 = hlp.table_std(
    _INCONSISTENT_DATA, coldirs=["rtl", "rtl", "ltr", "ltr", "ltr"]
)
_TABLE_4 = hlp.table_std(_RESOLUTIONS, coldirs=["rtl", "ltr"])


def _subsec_0():
    return _table_for_rule_d1()


def _subsec_1():
    # I couldn't find a "home" for these callouts,
    # i.e. I couldn't find anything good to "attach" them to.
    # So, for now at least, I just let them float off on their own.
    return sub.para([ftnts.FTNT_D1_RARELY, ", ", ftnts.FTNT_D1_OFTEN])


def _subsec_2():
    return sub.unordered_list(
        [
            [
                "In the case of a short vowel before the ",
                sub.fip(),
                ", Rule D2 is the same as the Rule D1: the $shewa"
                " is silent unless it follows $gaya",
                hlp.ftntjoin(".", ftnts.FTNT_6),
            ],
            [
                "In the case of a long vowel before the ",
                sub.fip(),
                ", Rule D2 rule differs from Rule D1: the $shewa"
                " is vocal, whether it follows $gaya",
                " or not (for ",
                sub.alvb_simshewa(),
                " may always take $gaya",
                " ",
                hlp.rtn_p(326),
                ")",
                hlp.ftntjoin(".", ftnts.FTNT_7),
            ],
        ]
    )


def _subsec_3():
    return sub.para(
        [
            "With this new rule, we are now able to resolve the three vocal/silent questions ",
            hlp.ftntjoin("left open above:", ftnts.FTNT_8),
        ]
    )


SEC = [
    sub.para_with_initial_uah(
        ["$Shewa on the First of an Identical Pair of Letters"],
        [
            "In the ",
            sub.diqduqe_dotan_sec_num(5),
            ", and in other masoretic treatises,"
            " the following rule is given (we’ll call it D1):",
        ],
    ),
    _subsec_0(),
    sub.para(
        [
            "This rule makes no distinction between $gaya",
            " on a short vowel, which is certainly phonetic, and $gaya",
            " on a long vowel, as ",
            hlp.hboloc("צָֽלְלוּ֙", "@Ex 15:10"),
            sub.thspc(),
            " which could be musical.",
        ]
    ),
    sub.para(
        [
            "This rule is not reflected in the manuscripts,"
            " not even in manuscripts in which $vocshewa is often made explicit by the use of",
            " $x_shewa on non-guttural letters.",
            " In such manuscripts, some words’ pointing is consistent with the rule:",
            " $x_shewa is used where $gaya is marked, but not where $gaya is not marked."
            " E.g., in ",
            sub.ms_aleppo(),
            ":",
        ]
    ),
    _TABLE_2,
    sub.para(
        [
            "However, other words’ pointing is not consistent with the rule."
            " E.g., in ",
            sub.ms_aleppo(),
            ":",
        ]
    ),
    _TABLE_3,
    #
    _subsec_1(),
    #
    sub.para(
        [
            *ftnts.THE_STUDY_REVEALS_RULE,
            " (we’ll call it D2). This rule distinguishes between $gaya",
            " on a short vowel and $gaya",
            " on a long vowel. This rule can be stated as follows:",
        ]
    ),
    #
    _subsec_2(),
    #
    _subsec_3(),
    #
    _TABLE_4,
]
