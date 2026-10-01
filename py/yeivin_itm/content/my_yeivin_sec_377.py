import py_html.legacy_html as aht_html
import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub


def hboloc_pp(contents, xloc):
    return hlp.hboloc(contents, xloc, {"class": "pre-or-post"})


_A_L = sub.ms_a_and_l()
_INVIS_ALEF = aht_html.span_c("(אֶ)", "invisible-but-takes-space")
_GRAY_ALEF = aht_html.span_c("(אֶ)", "pre-or-post")
_GRAY_ALEF_XATEF = aht_html.span_c("(אֱ)", "pre-or-post")
_DUAL_SHTAYIM = hlp.line_break(
    [hlp.hbo([_INVIS_ALEF, "שְׁ֚תַּיִם"]), sub.thspq()],
    [hlp.hbo([_GRAY_ALEF, "שְׁתַּ֙יִם֙"]), sub.thspq()],
)
_TABLE_DATA = [
    (hboloc_pp("תְּנוּפָ֗ה", "@Lev 23:17"), _DUAL_SHTAYIM, ""),
    (hboloc_pp("לְאִ֗ישׁ", "@Ez 1:11"), sub.saa(), ""),
    (hboloc_pp("לַדְּלָת֑וֹת", "@Ez 41:24"), sub.saa(), "1st time in this verse"),
    (hboloc_pp("דְּלָת֔וֹת", "@Ez 41:24"), sub.saa(), "2nd time in this verse"),
]
_FTNT_YETIV_POSITION = sub.footnote(
    [
        ["My guess is that bN put ", sub.yetiv(), " in this novel position"],
        [" to try to clarify that the stress was on the syllable whose main part is"],
        [" ", hlp.hbo("תַּ"), sub.thspp()],
        [" I.e. my guess is that this position was meant to mimic the way"],
        [" ", sub.yetiv(), " would appear on a (fictitious) word"],
        [" ", hlp.hbo("תַּ֚יִם"), sub.thspp()],
        [" Unfortunately this also must have looked quite like a"],
        [" ", sub.mehuppak(), ","],  # translit-ok
        [" i.e. must have looked quite like ", hlp.hbo("שְׁ֤תַּיִם"), sub.thspp()],
        [
            " On the bright side, such a ",
            sub.mehuppak(),  # translit-ok
            " on a $shewa is illegal,",
        ],
        [" at least giving the astute reader"],
        [" a clue that something unusual is going on."],
    ]
)
_FTNT_INITIAL_STRESS = sub.footnote(
    [
        "Note that ",
        hlp.hbo("שְׁתַּיִם"),
        " without an initial, implicit helping vowel"
        " has initial stress whether or not"
        " we consider its $shewa"
        " to be vocal. ",
        hlp.paren(
            [
                "As usual, we use the masoretic notion of a syllable,"
                " so initial stress means stress on the first full vowel,"
                " whether or not there is an initial $vocshewa.",
            ]
        ),
        " And, ",
        hlp.hbo("שְׁתַּיִם"),
        " with an initial, implicit helping vowel"
        " still has initial stress if that helping vowel is not a full vowel, e.g."
        " if the pronunciation is more like ",
        hlp.hbo([_GRAY_ALEF_XATEF, "שְׁתַּיִם"]),
        " than ",
        hlp.hbo([_GRAY_ALEF, "שְׁתַּיִם"]),
        " ",
        hlp.paren_xt(["more like ", sub.x_segol(), " than ", sub.segol()]),
        ".",
    ]
)
_FTNT_YETIV_ON_SHEWA = sub.footnote(
    [
        sub.yetiv(cap=True),
        " on an initial $shewa"
        " occurs nowhere else but in these four cases of שתים. In this respect, ",
        sub.yetiv(),
        " differs from the other prose prepositive, ",
        sub.telisha_gedolah(),
        ", because ",
        sub.telisha_gedolah(),
        " often appears on initial $shewa."
        " It even appears in some cases somewhat analogous to שתים such as ",
        hlp.hboloc("שְׁ֠מֹר", hlp.make_dloc("@1K 8:25", "@2C 6:16")),
        " and ",
        hlp.hboloc("שְׁ֠נֵי", "@2S 21:8"),
        sub.thspp(),
        " ",
        hlp.paren(
            [
                "Those examples look like ",
                hlp.hbo("שְׁ֠מֹ֠ר"),
                " and ",
                hlp.hbo("שְׁ֠נֵ֠י"),
                ""
                " when shown with “stress helpers”"
                " for those not used to the masoretic notion of a syllable.",
            ]
        ),
    ]
)
SEC = [
    sub.para(
        [
            "At the start of a word, $shewa"
            " is vocal. The only exception to this is found in the forms of ",
            hlp.hbo("שְׁתַּיִם"),
            sub.thspp(),
            " Here the initial $shewa"
            " is considered silent."
            " According to some sources (e.g. Levi, 1936, p. ט, translation p. 8-star),"
            " this pronunciation was made possible among the Tiberians"
            " by the use of a helping vowel, as ",
            hlp.some_hi_no_loc(("אֶשְׁתַּיִם", "*אֶשְׁ*תַּיִם")),
            " (the first syllable (highlighted) is a closed syllable)."
            # To avoid confusion with asterisk used as a footnote marker,
            # we say "8-star" instead of "8*" as in the original
            " This helping vowel was evidently the source of a ",
            sub.yetiv(),
            " vs. $pashta disagreement"
            " when the word"
            " has no preceding conjunctive, as in the following:",
        ]
    ),
    hlp.table_std_rtl(_TABLE_DATA, coldirs=["rtl", "rtl", "ltr"]),
    sub.unordered_list(
        [
            [
                "Those who pronounced this initial helping vowel"
                " as a full vowel considered the word to be unstressed on"
                " its first syllable, so that the $pashta sign was required.",
            ],
            [
                "Those who did not pronounce the helping vowel as a full"
                " vowel considered the word to be initially ",
                hlp.ftntjoin("stressed,", _FTNT_INITIAL_STRESS),
                " and so marked it with ",
                sub.yetiv(),
                " ",
                hlp.rtn_p(248),
                hlp.ftntjoin(".", _FTNT_YETIV_ON_SHEWA),
                " Even in this there was disagreement, however, as:",
                sub.unordered_list(
                    [
                        [
                            "Ben Asher put the ",
                            sub.yetiv(),
                            " in its normal, prepositive position, before the $shewa,"
                            " as ",
                            hlp.hbo("שְׁ֚תַּיִם"),
                            " (so ",
                            *_A_L,
                            ").",
                        ],
                        [
                            "Ben Naftali put it after the $shewa",
                            hlp.ftntjoin(".", _FTNT_YETIV_POSITION),
                        ],
                    ]
                ),
            ],
        ]
    ),
]
