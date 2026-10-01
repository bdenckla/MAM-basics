import yeivin_itm.substitutions as sub
import yeivin_itm.helpers as hlp

_FTNT_LIBERTIES = sub.footnote(
    [
        "I rewrote this section around the $gaya_osr framing of ",
        hlp.rtn(326),
        ", recasting $itm’s rules as a backwards search from the stress syllable."
        " Only the closing sentence stays close to $itm’s wording.",
    ]
)
_DLOC_TWO_IN_EX_27 = hlp.make_dloc("@Ex 27:10", "@Ex 27:11")
_TABLE_1 = hlp.table_std_rtl(
    [
        [
            "i",
            *hlp.lns(
                _DLOC_TWO_IN_EX_27, "הָֽעַמֻּדִ֛ים", hlp.sy6pspe("הָֽ-עַ_-מֻּ-דִ֛ים")
            ),
        ],
        # MAM lacks gaʿya on ה in 27:10 but not 11; see https://github.com/bdenckla/trope/issues/378
        [
            sub.saa(),
            *hlp.lns(
                "@1S 26:19", "מֵֽהִסְתַּפֵּ֜חַ", hlp.sy6ps("מֵֽ-הִסְ-תַּ-פֵּ֜-חַ")
            ),
        ],
        # MAM lacks gaʿya on מ; see https://github.com/bdenckla/trope/issues/379
        [
            sub.saa(),
            *hlp.lns(
                "@Ez 42:5", "מֵֽהַתַּחְתֹּנ֛וֹת", hlp.sy6pe("מֵֽ-הַ-תַּחְ-תֹּ-נ֛וֹת")
            ),
        ],
        # MAM lacks gaʿya on מ; see https://github.com/bdenckla/trope/issues/380
        [
            sub.saa(),
            *hlp.lns(
                "@Gen 23:18", "שַֽׁעַר־עִירֽוֹ׃", hlp.sy6pspe("שַֽׁ-עַר־-עִי-רֽוֹ׃")
            ),
        ],
        ["ii", *hlp.lns("@Gen 9:2", "הָֽאֲדָמָ֛ה", hlp.sy6pspe("הָֽ--אֲדָ-מָ֛ה"))],
        [
            sub.saa(),
            *hlp.lns(
                "@Gen 23:19", "וְאַֽחֲרֵי־כֵן֩", hlp.sy6pspe("וְאַֽ--חֲרֵי־-כֵן֩")
            ),
        ],
        # MAM lacks gaʿya on א; see https://github.com/bdenckla/trope/issues/381
        [
            sub.saa(),
            *hlp.lns("@Gen 23:11", "לֹֽא־אֲדֹנִ֣י", hlp.sy6pspe("לֹֽא־--אֲדֹ-נִ֣י")),
        ],
        [
            sub.saa(),
            *hlp.lns(
                "@Est 8:10",
                "הָֽאֲחַשְׁתְּרָנִ֔ים",
                hlp.sy6pspe("הָֽ-אֲחַשְׁ-תְּרָ-נִ֔ים"),
            ),
        ],
        [
            "iii",
            *hlp.lns("@Gen 18:21", "אֵֽרְדָה־נָּ֣א", hlp.sy6pspe("אֵֽרְ--דָה־-נָּ֣א")),
        ],
        [
            sub.saa(),
            *hlp.lns("@Gen 21:3", "יָֽלְדָה־לּ֥וֹ", hlp.sy6pspe("יָֽלְ--דָה־-לּ֥וֹ")),
        ],
        # MAM lacks gaʿya on yod; see https://github.com/bdenckla/trope/issues/382
        # XXX turn the comment below into a footnote?
        # I removed the אֲשֶׁר־ prefix to save space
    ]
)
_BE_OHEL_YAAKOV_P = (
    "בְּאֹֽהֶל־יַֽעֲקֹ֣ב׀"  # P for printed (as opposed to M for manuscript)
)
_BE_OHEL_YAAKOV_M = (
    "בְּאֹ֥הֶל יַעֲקֹ֣ב׀"  # M for manuscript (as opposed to P for printed)
)
_BE_OHEL_YAAKOV_P_NON_VOWEL = "באֽהל־יֽעק֣ב׀"
_BE_OHEL_YAAKOV_M_NON_VOWEL = "בא֥הל יעק֣ב׀"
_FTNT = sub.footnote(
    [
        "It is unclear from what manuscript, if any, $itm gets this pointing ",
        hlp.paren_tt(hlp.hbo(_BE_OHEL_YAAKOV_P_NON_VOWEL)),
        ". This pointing seems to be typical in the common printed texts."
        " But, in most manuscript traditions"
        " (Tiberian, Yemenite, and Sephardic),"
        " the pointing is ",
        hlp.hbo(_BE_OHEL_YAAKOV_M),
        " ",
        hlp.paren_tt(hlp.hbo(_BE_OHEL_YAAKOV_M_NON_VOWEL)),
        ". Thanks to Avi Kadish for research on this issue.",
    ]
)
_TABLE_2 = hlp.table_std_rtl(
    [
        ["i/iii", *hlp.lns("@Gen 49:18", "לִֽישׁוּעָֽתְךָ֖", "לִֽי-שׁוּ-עָֽתְ--ךָ֖")],
        # See note 1 below
        ["ii/iii", *hlp.lns("@Nu 8:2", "בְּהַֽעֲלֹֽתְךָ֙", "בְּהַֽ--עֲלֹֽתְ--ךָ֙")],
        # See note 1 below
        ["ii/i", *hlp.lns("@Ez 6:9", "תּֽוֹעֲבֹֽתֵיהֶֽם׃", "תּֽוֹ--עֲבֹֽ-תֵי-הֶֽם׃")],
        # MAM lacks gaʿya on ת and ב
        ["i/i", *hlp.lns("@Nu 26:31", "הָֽאַשְׂרִֽאֵלִ֑י", "הָֽ-אַשְׂ-רִֽ-אֵ-לִ֑י")],
        # See note 1 below
        [
            "i/ii",
            *hlp.lns("@Gen 31:33", _BE_OHEL_YAAKOV_P, "בְּאֹֽ-הֶל־-יַֽ--עֲקֹ֣ב׀"),
            _FTNT,
        ],
        #
        # Note 1: MAM lacks gaʿya on ל but this is expected (see "rare in manuscripts" below)
    ]
)
SEC = [
    sub.para(["[", _FTNT_LIBERTIES, "]"]),
    sub.para(
        [
            "Above we showed examples of $gaya_osr"
            " where the distinctive part of each example comes right before the stress syllable. ",
            hlp.paren(
                [
                    "Indeed, using the masoretic notion of a syllable,"
                    " the distinctive part of each example of case (ii)"
                    " reaches ",
                    hlp.emphasis("into"),
                    " the $xatef start of the stress syllable!",
                ]
            ),
            ""
            " But if what comes right before the stress syllable"
            " is not a candidate for $gaya_osr, then $gaya_osr",
            " can also come earlier in the word, as shown in the table below. ",
        ]
    ),
    # sub.para([
    #     'If the second syllable before the stress syllable is '
    #     'closed, and therefore not suitable for this ',sub.gaya(),', but some '
    #     'preceding syllable is open, or has ',
    #     sub.alvfb_shewa(),', then ',sub.gaya(),' is used on that syllable. E.g.:'
    # ]),
    _TABLE_1,
    # sub.para([
    #     'If ',sub.gaya(),' is marked on some syllable of a word, and before '
    #     'that syllable is another on which ',sub.gaya(),' could be marked '
    #     '(as before an accent) according to the rules given above, then the '
    #     'second ',sub.gaya(),' may be marked. E.g.:'
    # ]),
    sub.para(
        [
            "Two $gaya_osr",
            " may be marked on a word"
            " if, moving backwards from the stress syllable,"
            " we find both of the following:",
        ]
    ),
    sub.ordered_list(
        [
            [
                "A syllable on which $gaya_osr",
                " could be marked,"
                " in the fashion we have been discussing so far:"
                " relative to the stress syllable.",
            ],
            [
                "A syllable on which $gaya_osr",
                " could be marked, in a new fashion: relative to the $gaya_osr",
                " already found. I.e., as if the $gaya_osr",
                " already found were the stress syllable.",
            ],
        ]
    ),
    _TABLE_2,
    sub.para(
        [
            "Two $gayas are often marked on the same word in printed texts,"
            " but this is rare in manuscripts.",
        ]
    ),
]
