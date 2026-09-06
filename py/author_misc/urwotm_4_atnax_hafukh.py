"""Exports gen_html_file.

Ported from the published Google Doc of the same title. The prose is
reproduced verbatim; the only deliberate changes are the ``$`` keys that
``dollar_sub`` requires, and the three intra-series links, which now point at
the sibling pages rather than at the Google Docs.
"""

from mb_author import author
from author_misc import urwotm_common


def anchor():
    return urwotm_common.anchor_part(4)


def gen_html_file(tdm_ch):
    cbody = [
        author.heading_level_1(urwotm_common.heading_1(_PART)),
        author.heading_level_2(urwotm_common.heading_2(_PART)),
        author.para(_PARA_002),
        author.unordered_list(urwotm_common.other_parts(_PART)),
        author.para(_PARA_004),
        author.unordered_list(_LIST_005),
        author.para(_PARA_006),
        author.para(_PARA_007),
        author.unordered_list(_LIST_008),
        author.para(_PARA_013),
        author.unordered_list(_LIST_014),
        author.para(_PARA_015),
        author.para(_PARA_016),
        author.para_for_img("urwotm/Psalm 5v10 -- MAM with doc.png", width_em=80.1),
        author.para(_PARA_018),
        author.para(_PARA_019),
        author.para_for_img("urwotm/Psalm 5v10 -- Aleppo line 1.png", width_em=24.4),
        author.para_for_img("urwotm/Psalm 5v10 -- Aleppo line 2.png", width_em=34.4),
        author.para_for_img("urwotm/Psalm 5v10 -- L.png", width_em=131.3),
        author.para_for_img("urwotm/Psalm 5v10 -- Sassoon 1053.png", width_em=77.1),
        author.para(_PARA_024),
        author.para(_PARA_025),
        author.para_for_img("urwotm/Psalm 5v10 -- BHS.jpg", width_em=82.1),
        author.para(_PARA_027),
        author.unordered_list(_LIST_028),
        author.para(_PARA_035),
        author.para(_PARA_036),
        author.blockquote(_QUOTE_037),
        author.para(_PARA_038),
        author.blockquote(_QUOTE_039),
        author.para(_PARA_040),
        author.blockquote(_QUOTE_041),
        author.para(_PARA_042),
        author.blockquote(_QUOTE_043),
        author.para(_PARA_044),
        author.para(_PARA_045),
        author.para_for_img(
            "urwotm/BHS table of accents 26 galgal -- prose.png", width_em=75.6
        ),
        author.para_for_img(
            "urwotm/BHS table of accents 17 galgal -- poetic.png", width_em=74.9
        ),
        author.para(_PARA_048),
        author.para_for_img(
            "urwotm/BHS table of accents 26 galfukh -- prose.png", width_em=75.1
        ),
        author.para_for_img(
            "urwotm/BHS table of accents 17 galfukh -- poetic.png", width_em=98.9
        ),
        author.para(_PARA_051),
        author.para(_PARA_052),
        author.para(_PARA_053),
    ]
    return author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, cbody)


_PART = 4
_TITLE = urwotm_common.plain_title(_PART)
_FNAME = urwotm_common.FNAMES[_PART]

_URL_BDENCKLA_GITHUB_IO_1 = (
    "https://bdenckla.github.io/MAM-basics/MAM-with-doc/D1-Psalms.html#c5v10"
)
_URL_BDENCKLA_GITHUB_IO_2 = "https://bdenckla.github.io/Taamey_D/"
_URL_TANACH_US_1 = "https://tanach.us/"

_PARA_002 = """This is the fourth article in a series. The series is about errors in $BHS and/or
$WLC. The other articles in the series are as follows:""".replace(
    "\n", " "
)
_PARA_004 = "This article is about:"
_LIST_005 = [
    "the accent $ah ($AH)",
    "the accent $BHS conflates $AH with, $galgal",
]
_PARA_006 = "($Galgal is also known as $yby)."
_PARA_007 = "Here’s the basic story:"
_LIST_008 = [
    "The $BHS table of accents lists no accent called $ah (“inverted $atnax”).",
    [
        "Yet, $BHS often uses a mark shaped like an inverted $atnax, i.e. a V-shaped",
        " mark.",
    ],
    [
        "In fact, it uses it too often.",
        author.unordered_list(
            [
                [
                    "$BHS uses a V-shaped mark where such a shape appears in L (the Leningrad",
                    " Codex). So far so good.",
                ],
                [
                    "But $BHS also uses that same V-shaped mark where a U-shaped mark occurs in L.",
                    author.unordered_list(
                        [
                            [
                                "This U-shaped mark is known by two names:",
                                author.unordered_list(
                                    [
                                        "$galgal (“wheel”) (a weird name, given its shape)",
                                        "$yby (“moon of a day [in age]”) (a sensible name, given its shape)",
                                    ]
                                ),
                            ],
                            [
                                "The $BHS table of accents lists an accent called “$galgal vel ",
                                urwotm_common.romanized("jèraḥ"),
                                " [$ben_yomo]” but associates it with a V-shaped mark.",
                            ],
                        ]
                    ),
                ],
            ]
        ),
    ],
]
_PARA_013 = "So we can see that $ah and $galgal are conflated by $BHS. In $BHS:"
_LIST_014 = [
    "$icap_Ah exists in shape but not in name.",
    "$Galgal exists in name but not in shape.",
]
_PARA_015 = """The $BHS editors were not the first people to conflate these accents. Indeed, this
conflation precedes the era of printing! But, due to its great popularity, $BHS is
primarily to blame for this conflation’s persistence down to the present time.
Thankfully, this conflation is not universal. As other articles in this series have
shown, there is a sphere of publication and scholarship, mostly Israeli, that has
escaped the great gravitational pull of $BHS and $WLC. In that sphere, there is no
such conflation.""".replace(
    "\n", " "
)
_PARA_016 = [
    "Let’s look at the first few words of Psalm 5:10 in “",
    author.anc_h("$MAM with doc", _URL_BDENCKLA_GITHUB_IO_1),
    "” (Mwd), an edition that takes more care with accents than $BHS does (color",
    " added):",
]
_PARA_018 = """We see that in Mwd, the words אין and קרבם have different accents. The accent on אין
is $galgal and the accent on קרבם is $ah.""".replace(
    "\n", " "
)
_PARA_019 = """Now let’s verify that Mwd corresponds to three great manuscripts. Here are the first
few words of Psalm 5:10 in Ms א, Ms ל, and Ms ש1 (aka שׂ ($sin)) (aka Sassoon 1053).
(Thanks to tanach.us, Sefaria, Bar-Ilan U., and IHBMR for hosting and/or indexing
these images.)""".replace(
    "\n", " "
)
_PARA_024 = """We see that Mwd corresponds to the manuscripts, modulo the shape of $ah. In Mwd,
which uses the Taamey D font, $ah is what we might call a tuning-fork-shaped mark as
opposed to the V-shaped mark we find in the manuscripts. This is like the well-known
difference in the shape of $atnax between some printing traditions and the
manuscript tradition.""".replace(
    "\n", " "
)
_PARA_025 = "Now let’s see what these accents look like in $BHS:"
_PARA_027 = [
    "We see that in $BHS, the words אין and קרבם have accents with the same shape:",
    " an inverted $atnax. The $BHS table of accents identifies this inverted $atnax",
    " shape as “$galgal vel ",
    urwotm_common.romanized("jèraḥ"),
    " [$ben_yomo].” According to modern scholarship, this is wrong.",
]
_LIST_028 = [
    [
        "Only the first of these two accents, the accent on אין, is $galgal.",
        author.unordered_list(
            [
                [
                    "In the poetic books:",
                    author.unordered_list(
                        [
                            "$Galgal is a conjunctive accent that serves $pazer only.",
                            "$Galgal does not serve $oleh_veyored or any other accent.",
                        ]
                    ),
                ],
                [
                    "In the 21 books:",
                    author.unordered_list(
                        [
                            "$Galgal is a conjunctive accent that serves $pazer_gadol (aka $qarney_parah).",
                            "$Galgal does not serve any other accent.",
                        ]
                    ),
                ],
            ]
        ),
    ],
    [
        [
            "The second of these two accents is what modern scholarship calls $atnax ",
            urwotm_common.romanized("hafukh"),
            ".",
        ],
        author.unordered_list(
            [
                "$AH is a conjunctive accent that serves $oleh_veyored only.",
                "$AH does not serve $pazer or any other accent.",
                "$AH appears only in the poetic books.",
            ]
        ),
    ],
]
_PARA_035 = [
    "Perhaps we should think of pre-modern scholarship on this topic as as merely",
    " imprecise, not wrong. In that light, I suggest that when pre-modern",
    " scholarship refers to $galgal or $yby, we should read this as “$galfukh,” a",
    " portmanteau created from $galgal and $atnax ",
    urwotm_common.romanized("hafukh"),
    ". “$Galfukh” is a kind of perpetual $qere for pre-modern scholarship on the",
    " Hebrew Bible.",
]
_PARA_036 = """Once “$galfukh” is substituted in, most of what pre-modern scholarship says about
$galgal is not wrong. It becomes merely imprecise rather than wrong. For instance,
when Wickes says, on page 57 of his treaties on the poetic accents:""".replace(
    "\n", " "
)
_QUOTE_037 = [
    "The servus of Olév’$yored is [...] ",
    author.span_color("$Galgal", "#ff0000"),
    ".",
]
_PARA_038 = "We should read this as:"
_QUOTE_039 = [
    "The servus of Olév’$yored is [...] ",
    author.span_color("$Galfukh", "#6aa84f"),
    ".",
]
_PARA_040 = "Similarly, when Wickes says, on page 88:"
_QUOTE_041 = [
    "When there is ",
    urwotm_common.romanized("one"),
    " [servus of $Pazer,] it is ",
    author.span_color("$Galgal", "#ff0000"),
]
_PARA_042 = """Although that is not wrong even according to modern scholarship, we should read it
as:""".replace(
    "\n", " "
)
_QUOTE_043 = [
    "When there is ",
    urwotm_common.romanized("one"),
    " [servus of $Pazer] it is ",
    author.span_color("$Galfukh", "#6aa84f"),
]
_PARA_044 = """$Galgal as distinct from $AH is not a valid concept in pre-modern scholarship, so we
should never read Wickes as meaning $galgal in the modern sense when he writes
“$galgal.”""".replace(
    "\n", " "
)
_PARA_045 = """Similarly, when reading the $BHS table of accents (both the prose sub-table and the
poetic sub-table):""".replace(
    "\n", " "
)
_PARA_048 = [
    "We should read “$galgal vel ",
    urwotm_common.romanized("jèraḥ"),
    " [$ben_yomo]” as “$galfukh vel $galfukh.” Since “vel” is Latin for “or,” we",
    " algebraically simplify this to “$galfukh,” yielding:",
]
_PARA_051 = [
    "The conflation of $AH and $galgal is further complicated by poor font support",
    " for $galgal. In the ",
    author.anc_h("documentation for my Taamey D font", _URL_BDENCKLA_GITHUB_IO_2),
    " I write, “$BHS is so influential that even its shortcomings still reverberate",
    " through the Biblical world, showing up not only in other editions of the",
    " Hebrew Bible but also in fonts!” To be fair to $BHS, another important",
    " contributor to the poor font support for $galgal was the somewhat-botched way",
    " in which support for a distinct $atnax ",
    urwotm_common.romanized("hafukh"),
    " was added to Unicode.",
]
_PARA_052 = """$WLC faithfully transcribes $BHS with respect to these issues. $WLC uses the code 93
to represent $BHS’s $galfukh accent.""".replace(
    "\n", " "
)
_PARA_053 = [
    "In its 19 Oct 2021 release (version 1.3), $UXLC broke away from its $WLC",
    " roots by starting to distinguish $AH from $galgal. But to make this change",
    " visible in $UXLC’s canonical edition, ",
    author.anc_h("tanach.us", _URL_TANACH_US_1),
    " had to start using a new font. Otherwise, the distinction newly made in the",
    " underlying Unicode would remain invisible, since both $AH and $galgal would",
    " continue to be rendered with the same inverted $atnax shape. That’s how hard",
    " it is to escape the “gravitational pull” of $BHS. Even if you try to",
    " distinguish $AH from $galgal, most fonts will thwart you! With that, I",
    " conclude this article.",
]
