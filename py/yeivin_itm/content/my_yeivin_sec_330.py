import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_TABLE_1_DATA = [
    [
        "י(י)ראו",
        ["meaning “fear”"],
        sub.dol([" has $gaya as"]),
        hlp.lhbo("@Gen 20:8", "וַיִּֽירְא֥וּ"),
    ],
    # accent above (merka) added by me  # translit-ok
    [
        "יראו",
        ["meaning “see”"],
        sub.dol([" has no $gaya as"]),
        hlp.lhbo("@Nu 17:24", "וַיִּרְא֥וּ"),
    ],
    # accent above (merka) added by me  # translit-ok
]
_TABLE_1 = hlp.table_std(_TABLE_1_DATA, coldirs=["rtl", "ltr", "ltr", "rtl"])
SEC = [
    sub.para(
        [
            "The use of $gaya_os is not described"
            " in the masoretic literature or in other early sources, and there"
            " are only scattered references to this $gaya.",
            " The ",
            sub.diqduqe_baer(32),
            " says:",
            # XXX add footnote about added accents
        ]
    ),
    _TABLE_1,
    sub.para(
        [
            "The ",
            sub.horayat_d(90, 398),
            " says:",
            # XXX add footnote about added accents
        ]
    ),
    sub.blockquote_p(
        [
            "$Gaya sometimes distinguishes meaning, as in the rule “forms from ירא have",
            " $gaya, forms from ראה do not” and as in ",
            hlp.lhbo("@Neḥ 13:21", "תִּשְׁנ֕וּ"),
            " which means “do again” (שנה) and ",
            # accent above (zaqef gadol) added by me
            hlp.lhbo("@Prov 4:16", "יִֽ֭שְׁנוּ"),
            # accent above (dexi) added by me
            " which means “sleep” (ישן).",
        ]
    ),
    sub.para(
        [
            sub.yequtiel_hn(),
            " was the first to draw up rules for the use of this $gaya,",
            " and he has been followed by later scholars.",
        ]
    ),
]
