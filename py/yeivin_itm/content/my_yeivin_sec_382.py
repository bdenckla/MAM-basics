import yeivin_itm.helpers as hlp
import yeivin_itm.substitutions as sub

_AMOS_6_3 = "הַֽמְנַדִּ֖ים", "הַֽ*מְנַ_*דִּ֖ים", "@Amos 6:3"
_SNDC_32_31 = "הַֽמְשַׁלְּחִ֤ים", "הַֽ*מְשַׁ_*לְּחִ֤ים", "@2C 32:31"
_FSTS_18_7 = "הַֽמְשַׂחֲק֖וֹת", "*הַֽמְ*שַׂחֲק֖וֹת", "@1S 18:7"
_NU_5_24 = "הַֽמְאָרְרִ֖ים", "*הַֽמְ*אָרְרִ֖ים", hlp.make_dloc("@Nu 5:19", "@Nu 5:24")
_DATA_FOR_TABLE_IN_FTNT_NU_5_24 = [
    [hlp.hboloc("הַֽמארר֖ים", hlp.make_dloc("@Nu 5:19", "@Nu 5:24")), "2 cases"],
    [hlp.hboloc("המאֽרר֑ים", "@Nu 5:24"), ""],
    [hlp.hboloc("המאֽררֽים׃", "@Nu 5:18"), ""],
    [hlp.hboloc("המאֽררים֙", "@Nu 5:27"), ""],
    [hlp.hboloc("המארר֤ים", "@Nu 5:22"), ""],
]
_FTNT_NU_5_24 = sub.footnote(
    [
        sub.para(
            [
                "Here $itm gives ",
                hlp.hbo(_NU_5_24[0]),
                ""
                " three locales, including two in Nu 5:24: “Nu 5:19, 24, 24.”"
                " But, the second instance in Nu 5:24 is ",
                hlp.hbo("המְאָֽרְרִ֑ים"),
                sub.thspc(),
                " which, at least in ",
                sub.ms_lenin(),
                ", differs from ",
                hlp.hbo(_NU_5_24[0]),
                " in the following ways:",
            ]
        ),
        sub.unordered_list(
            [
                ["It has a pausal accent ", hlp.paren(sub.atnax()), "."],
                sub.dol(["It has $gaya on א rather than ה."]),
            ]
        ),
        sub.para(
            [
                "One might speculate that the difference in the position of the $gaya",
                " is explained by the pausal vs. non-pausal difference."
                " This idea is strengthened by another nearby example in ",
                sub.ms_lenin(),
                ", ",
                hlp.hboloc("הַמְאָֽרְרִֽים׃", "@Nu 5:18"),
                sub.thspp(),
                " But, yet another nearby example in ",
                sub.ms_lenin(),
                ", ",
                hlp.hboloc("הַמְאָֽרְרִים֙", "@Nu 5:27"),
                sub.thspc(),
                ""
                " spoils the pattern. The table below summarizes the"
                " (somewhat confusing) situation."
                " This table includes an example not mentioned above, ",
                hlp.hboloc("הַמְאָרְרִ֤ים", "@Nu 5:22"),
                sub.thspc(),
                " which, in ",
                sub.ms_lenin(),
                " at least, has no $gaya",
                " in any position. ",
                hlp.paren(
                    [
                        "A $gaya on the ה of that word would be unexpected"
                        " since it would be on a closed syllable before a conjunctive accent."
                        " But, as far as I know,"
                        " there are no firm expectations"
                        " as to whether there should or should not be a",
                        " $gaya on the open syllable starting with א.",
                    ]
                ),
            ]
        ),
        hlp.table_std(_DATA_FOR_TABLE_IN_FTNT_NU_5_24, coldirs=["rtl", "ltr"]),
        sub.para(
            [
                "For completness, and because it may be related, we note that"
                " the notation of the $shewa"
                " on the ",
                sub.resh(),
                " in these words"
                " varies considerably from manuscript to manuscript."
                " See the ",
                sub.mamdoc("A4-Numbers.html#c5v18"),
                ". I.e. some manuscripts ",
                hlp.paren(["notably ", sub.ms_lenin(), " and ", sub.ms_b_4445()]),
                " use ",
                sub.x_patax(),
                " where others use $simshewa."
                " The only word for which there appears to be no variation is"
                " (coincidentally?) the one with a conjunctive accent, ",
                hlp.hboloc("הַמְאָרְרִ֤ים", "@Nu 5:22"),
                sub.thspp(),
                " For this word, all manuscripts documented by ",
                sub.mam(),
                " use $simshewa.",
            ]
        ),
        sub.para(
            [
                "We have used $simshewa throughout this footnote, since, for one thing,"
                " that is what $itm uses for the three words"
                " at the locales “Nu 5:19, 24, 24.”"
                " So our claims about the contents of ",
                sub.ms_lenin(),
                " above are not quite right, because in all cases except ",
                hlp.hboloc("הַמְאָרְרִ֤ים", "@Nu 5:22"),
                sub.thspc(),
                " ",
                sub.ms_lenin(),
                " uses ",
                sub.x_patax(),
                " on ",
                sub.resh(),
                ". Whereas, we have shown $simshewa in all cases.",
            ]
        ),
    ]
)
_BAR = "הַֽמְקַטְּרִ֣ים", "*הַֽמְ*קַטְּרִ֣ים", "@2K 23:5"
_BAR2 = "הַֽמְעֻשָּׁקָ֞ה", "*הַֽמְ*עֻשָּׁקָ֞ה", "@Is 23:12"
_BAR3 = "הַֽמְסֻכָּ֣ן", "הַֽ*מְסֻ_*כָּ֣ן", "@Is 40:20"
_BAR4 = "הַֽמְצַפְצְפִ֖ים", "*הַֽמְ*צַפְצְפִ֖ים", "@Is 8:19"
_BAR5 = "הַֽמְחַכִּ֣ים", "הַֽ*מְחַ_*כִּ֣ים", "@Job 3:21"
SEC = [
    sub.para_with_initial_uah(
        [
            "$Shewa on ",
            sub.mem(cap=True),
            " after initial ",
            sub.he(cap=True),
            " with ",
            sub.patax(cap=True),
        ],
        [hlp.rtn_p(347, pre="cf. ")],
    ),
    sub.para(
        [
            "These rules apply not only to ",
            sub.he(),
            ", but also to ",
            sub.rom_bkl(),
            " representing a preposition with the vowel of the definite article.",
        ]
    ),
    sub.para(
        [
            "Where the ",
            sub.he(),
            " has a $gaya,",
            " if it is a $mgaya, the $shewa that follows is silent, but if it is a",
            " $pgaya, the $shewa that follows is vocal. The ",
            sub.diqduqe_dotan_sec_num(14),
            " states that, as a rule, $gaya",
            " in this situation is phonetic, so the $shewa is vocal.",
        ]
    ),
    sub.para(
        [
            "Various examples of $pgaya are given, mainly in two categories."
            " These categories differ from each other in"
            " the reason that the $gaya",
            " was unlikely to have been musical ",
            hlp.rtn_p(319),
            ":",
        ]
    ),
    sub.ordered_list(
        [
            [
                "Because the word fails to meet the structural criteria. E.g. ",
                hlp.some_hi(_AMOS_6_3),
                ".",
            ],
            [
                "Because, though the word meets the structural criteria,"
                " it fails to meet the accent criteria:"
                " it has a conjunctive accent."
                " E.g. ",
                hlp.some_hi(_SNDC_32_31),
                ".",
            ],
        ]
    ),
    sub.para(
        [
            "In words in these two categories, then,"
            " the $gaya is phonetic and therefore the $shewa is vocal."
            " This is followed by a list of words in which"
            " the $gaya is musical and therefore the $shewa is silent."
            " For most of these words, the fact that the $gaya is musical is not surprising,"
            " because these words meet both the structural and accent criteria"
            " for a $mgaya. E.g., ",
            hlp.some_hi(_FSTS_18_7),
            " (",
            sub.fr3(),
            ") and ",
            hlp.some_hi(_NU_5_24),
            " (",
            sub.afr4(),
            ")",
            hlp.ftntjoin(".", _FTNT_NU_5_24),
        ]
    ),
    sub.para(
        [
            "But for some some of these words, the fact that the $gaya is musical is surprising,"
            " because they fail to meet one or both of the criteria"
            " (structural and accent)"
            " for a $mgaya. ",
        ]
    ),
    sub.para(
        ["Some have a conjunctive accent, as ", hlp.some_hi(_BAR), sub.thspp(), ""]
    ),
    sub.para(
        [
            "And some have non-regular structure, as ",
            hlp.some_hi(_BAR2),
            sub.thspp(),
        ]
    ),
    sub.para(
        [
            "Whether it is surprising or not,"
            " in all these cases the $gaya is musical,"
            " and the $shewa is silent.",
        ]
    ),
    sub.para(
        [
            ["Some sources give rules for determining whether $shewa"],
            [" is vocal or silent in such cases by the number of letters in the word."],
        ]
    ),
    sub.unordered_list(
        [
            [
                "If it has five letters, as ",
                hlp.some_hi(_BAR3),
                sub.thspc(),
                " then the $shewa is vocal.",
            ],
            [
                "If it has six or more letters, ",
                sub.unordered_list(
                    [
                        [
                            "and the accent sign is on the fifth or sixth, as ",
                            hlp.some_hi(_BAR4),
                            sub.thspc(),
                            " then the $shewa is silent,",
                        ],
                        [
                            "but if the accent sign is on the fourth letter, as ",
                            hlp.some_hi(_BAR5),
                            sub.thspc(),
                            " then the $shewa is vocal.",
                        ],
                    ]
                ),
            ],
        ]
    ),
    sub.para(["Some exceptions to these rules are also listed."]),
    sub.para(
        [
            "The rule given in the ",
            sub.diqduqe(),
            ""
            " covers most of the cases, but not all."
            " The other rules, however, cover an even smaller proportion."
            " In some manuscripts, notably in ",
            sub.ms_aleppo(),
            ", the ",
            sub.mem(),
            " in this situation is pointed with ",
            sub.x_patax(),
            " when the $shewa"
            " is vocal, which gives a clear indication of the pronunciation.",
        ]
    ),
]
