"""Notes on Aliyot — generated HTML document about Torah aliyot in MAM."""

from py_misc import my_html
from pyauthor_util import author

_NDASH = "\N{EN DASH}"
_PRIME = "\N{PRIME}"
_DPRIME = "\N{DOUBLE PRIME}"
_HELLIP = "\N{HORIZONTAL ELLIPSIS}"


def gen_html_file(tdm_ch):
    author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, _CBODY)


def _td(contents, attr=None):
    return my_html.table_datum(author.dollar_sub(contents), attr)


def _th(contents, attr=None):
    return my_html.table_header(author.dollar_sub(contents), attr)


def _tr(cells):
    return my_html.table_row(cells)


def _strong(contents):
    return my_html.htel_mk("strong", flex_contents=author.dollar_sub(contents))


def _rtl(contents):
    return my_html.span(contents, {"dir": "rtl"})


def _bor(contents, **extra):
    """Bordered cell."""
    return _td(contents, {"class": "bordered", **extra})


def _hc(contents, **extra):
    """Horizontally centered cell."""
    return _td(contents, {"class": "hcenter", **extra})


def _hcb(contents, **extra):
    """Horizontally centered, bordered cell."""
    return _td(contents, {"class": "hcenter bordered", **extra})


def _imp(contents):
    """Implicit-label cell."""
    return _td(contents, {"class": "implicit-label"})


def _taamey(contents):
    return my_html.span(contents, {"class": "font-family-taamey-frank-clm-inline"})


###############################################################################
# Content
###############################################################################

_FNAME = "notes_on_aliyot.html"
_TITLE = "Notes on Aliyot"
_H1 = "Notes on $aliyot"

_AUTHOR = "Author: Ben Denckla"
_REVISION = [
    "Revision: 4 Oct 2021 / ",
    _taamey("כ״ח ב\u05bc\u05b0ת\u05b4ש\u05c1\u05b0ר\u05b5י תשפ״ב"),
]

# ── Introduction ──

_INTRO_P1 = [
    "This document describes the $aliyot of the Torah,",
    " as they appear in $MAM (Miqra According to the Masorah).",
    " The $MAM text is annotated with two systems",
    " that hierarchically divide the Torah.",
    " Both systems have the following in common:",
]
_INTRO_UL1 = [
    ["The 5 ", _strong("books"), " of the Torah are at the top of the hierarchy."],
    [
        "The 5,844 ",
        _strong("verses"),
        " of $MAM's Torah are at the bottom of the hierarchy.",
    ],
]
_INTRO_P2 = [
    "Where things get interesting is at the level(s) of hierarchy",
    " between book and verse.",
    " This is where the two systems vary.",
]
_INTRO_UL2 = [
    [
        "One system has 187 ",
        _strong("chapters"),
        " as the sole level of hierarchy between book and verse.",
    ],
    [
        "The other system has the following two levels between book and verse:",
        author.unordered_list(
            [
                [
                    "54 ",
                    _strong("$parashiyot"),
                    " immediately below the level of the book",
                ],
                [
                    "378 ",
                    _strong("$aliyot"),
                    " (7 for each $parashah)",
                    " immediately below the level of the $parashah",
                ],
            ]
        ),
    ],
]
_INTRO_P3 = "Schematically, we can compare these two systems as follows:"
_INTRO_TABLE1 = my_html.table(
    [
        _tr([_hcb("book", colspan="2")]),
        _tr([_hc("chapter", rowspan="2"), _hc("$parashah")]),
        _tr([_hc("$aliyah")]),
        _tr([_hcb("verse", colspan="2")]),
    ]
)
_INTRO_P4 = [
    "These systems reflect quite different notions",
    " of where the significant boundaries of the text lie,",
    ' as illustrated by the following "stats":',
]
_INTRO_UL3 = [
    "Only 32 of the 54 $parashiyot start when a chapter starts.",
    "Only 87 of the 187 chapters start when an $aliyah starts.",
]
_INTRO_P5 = [
    "The $parashah_sl_aliyah system is the focus of this document.",
    " In truth, this system is more complicated than what we have described above.",
    " The two main complications are as follows,",
    " and will be discussed in the next two sections.",
]
_INTRO_UL4 = [
    [
        "While it is true that there are 54 ",
        _strong("single"),
        " $parashiyot,",
        " 7 neighboring pairs of them can be combined to form ",
        _strong("dual"),
        " $parashiyot.",
    ],
    [
        "While it is true that there are exactly 7 ",
        _strong("numbered"),
        " $aliyot for every $parashah, there are ",
        _strong("non-numbered"),
        " $aliyot that don't belong in this hierarchy.",
    ],
]

# ── Dual parashiyot ──

_DUAL_P1 = "The dual $parashiyot are as follows:"
_DUAL_OL1 = [
    f"ויקהל{_NDASH}פקודי",
    f"תזריע{_NDASH}מצ\u05b9רע",
    f"אחרי מות{_NDASH}קד\u05b9שים",
    f"בהר{_NDASH}בח\u05bbק\u05b9תי",
    f"ח\u05bbקת{_NDASH}בלק",
    f"מטות{_NDASH}מסעי",
    f"נ\u05b4צבים{_NDASH}וילך",
]
_DUAL_P2 = [
    "We can think of the dual $parashiyot as forming an alternate hierarchy.",
    " This alternate hierarchy:",
]
_DUAL_UL1 = [
    'retains the 40 "single and unpairable" $parashiyot',
    [
        "uses the 7 dual $parashiyot to fill in the space otherwise occupied",
        ' by the 14 "single but pairable" $parashiyot',
    ],
]
_DUAL_P3 = [
    "The $parashah level of this alternate hierarchy is illustrated by the table below.",
    " To keep the table compact, we use numbers rather than names",
    " to identify the $parashiyot.",
    ' We identify a $parashah by its number within its "parent" book.',
    " Thus ",
    _rtl("בראשית-2"),
    " is ",
    _rtl("נ\u05b9ח"),
    ", ",
    _rtl("בראשית-3"),
    " is ",
    _rtl("לך־לך"),
    ", etc.",
]


def _num_cells(nums):
    return [_td(str(n)) for n in nums]


def _dual_cell(pair):
    return _bor(f"{pair[0]}{_NDASH}{pair[1]}", colspan=str(pair[1] - pair[0] + 1))


_DUAL_TABLE1 = my_html.table(
    [
        _tr([_td("בראשית")] + _num_cells(range(1, 13))),
        _tr([_td("שמות")] + _num_cells(range(1, 10)) + [_dual_cell((10, 11)), _td("")]),
        _tr(
            [_td("ויקרא")]
            + _num_cells(range(1, 4))
            + [
                _dual_cell((4, 5)),
                _dual_cell((6, 7)),
                _td("8"),
                _dual_cell((9, 10)),
                _td(""),
                _td(""),
            ]
        ),
        _tr(
            [_td("במדבר")]
            + _num_cells(range(1, 6))
            + [
                _dual_cell((6, 7)),
                _td("8"),
                _dual_cell((9, 10)),
                _td(""),
                _td(""),
            ]
        ),
        _tr(
            [_td("דברים")]
            + _num_cells(range(1, 8))
            + [_dual_cell((8, 9)), _td("10"), _td("11"), _td("")]
        ),
    ]
)

_DUAL_P4 = "This alternate hierarchy:"
_DUAL_UL2 = [
    "has only 47 rather than 54 divisions in its sub-book level",
    [
        "has only 329 rather than 378 numbered $aliyot",
        " (each dual $parashah still has exactly 7 numbered $aliyot,",
        " just like a single $parashah)",
    ],
]
_DUAL_P5 = [
    "In truth, the way dual $parashiyot are used in practice",
    " is more complicated than this alternate hierarchy would suggest.",
    " The truth is that in any given year,",
    " some dual $parashiyot are used, and others are not.",
    ' But the simplified "all or nothing" model',
    " (use all 7 duals, or use none) suffices for our purposes here.",
]
_DUAL_P6 = [
    "As mentioned above, each dual $parashah has its own 7 numbered $aliyot.",
    " These 7 $aliyot simply consist of 1 to 4 neighboring $aliyot",
    ' from the "single but pairable" halves of the dual $parashah.',
    " The table below shows the partitioning of all 7 dual $parashiyot,",
    " expressed in terms of these constituent $aliyot.",
]


def _part_row(name, lengths, spans):
    """Build a partitioning-table row: name, lengths string, then numbered bordered cells."""
    cells = [_td(name), _td(lengths)]
    for i, sp in enumerate(spans, 1):
        cells.append(_bor(str(i), colspan=str(sp)))
    return _tr(cells)


_PART_HDR = _tr(
    [_td(""), _td("lengths")]
    + [_td(f"{i}{_PRIME}") for i in range(1, 8)]
    + [_td(f"{i}{_DPRIME}") for i in range(1, 8)]
)
_PART_TABLE = my_html.table(
    [
        _PART_HDR,
        _part_row(
            "ויקהל-פקודי",
            "231-2123",
            [2, 3, 1, 2, 1, 2, 3],
        ),
        _part_row(
            "תזריע-מצ\u05b9רע",
            "321-3122",
            [3, 2, 1, 3, 1, 2, 2],
        ),
        _part_row(
            "אחרי מות-קד\u05b9שים",
            "222-2222",
            [2, 2, 2, 2, 2, 2, 2],
        ),
        _part_row(
            "בהר-בח\u05bbק\u05b9תי",
            "221-4113",
            [2, 2, 1, 4, 1, 1, 3],
        ),
        _part_row(
            "ח\u05bbקת-בלק",
            "222-2222",
            [2, 2, 2, 2, 2, 2, 2],
        ),
        _part_row(
            "מטות-מסעי",
            "231-3122",
            [2, 3, 1, 3, 1, 2, 2],
        ),
        _part_row(
            "נ\u05b4צבים-וילך",
            "312-3212",
            [3, 1, 2, 3, 2, 1, 2],
        ),
    ]
)

_PART_EXPL_P = "Some explanation of the table above:"
_PART_EXPL_UL = [
    [
        "Prime & double prime marks label the halves, making, for example,",
        author.unordered_list(
            [
                f"3{_PRIME} the 3rd $aliyah of the 1st half",
                f"4{_DPRIME} the 4th $aliyah of the 2nd half",
            ]
        ),
    ],
    [
        "In addition to its schematic representation of the partitioning,",
        " the table above also represents the partitioning",
        " in a compact, 7-digit form,",
        " with each digit representing the length of a partition.",
        author.unordered_list(
            [
                "For readability, we have dash-separated the digits into groups of 3 & 4.",
                [
                    "Since the lengths sum to 7,",
                    " we could leave off the last length,",
                    " using only 6 digits, but that seems too implicit.",
                ],
            ]
        ),
    ],
]
_PART_NOTES_P = "Some notes on the data in this table:"
_PART_NOTES_UL = [
    [
        "Only in 2 of the 7 dual $parashiyot is the partitioning uniform",
        " (compactly represented by 222-2222).",
        " Those 2 are אחרי מות-קד\u05b9שים",
        " and ח\u05bbקת-בלק.",
        " Contrast these with the 5 dual $parashiyot with non-uniform partitioning,",
        " e.g. בהר-בח\u05bbק\u05b9תי",
        " (compactly represented by 221-4113).",
    ],
    [
        "One consistent feature of the partitioning is that the 4th",
        " $aliyah always spans the halves of the $parashah.",
        " I.e. the 4th always contains",
        " at least one $aliyah from the 1st half of the $parashah and",
        " at least one $aliyah from the 2nd half of the $parashah.",
    ],
    [
        f"The 4th $aliyah starts with $aliyah 7{_PRIME}",
        " in 6 of the 7 dual $parashiyot.",
        " The exception is בהר-בח\u05bbק\u05b9תי.",
        f" Its 4th $aliyah starts with 6{_PRIME}.",
        " The 4th $aliyah of בהר-בח\u05bbק\u05b9תי",
        " is also exceptional because it is the largest:",
        " it is the only $aliyah consisting of 4 $aliyot from its halves.",
    ],
]

# ── Non-numbered aliyot ──

_NN_P1 = "A non-numbered $aliyah can have one of two types:"
_NN_UL1 = [
    [
        "One type of non-numbered $aliyah is the $maftir $aliyah.",
        " Every $parashah, be it single or dual, has a $maftir",
        " except וזאת הברכה,",
        " the last $parashah of the Torah.",
        " (As usual things are not quite that simple;",
        " וזאת הברכה",
        " has a $maftir selection associated with it,",
        " but the selection comes from a different $parashah of the Torah.",
        " Thus it might be more accurate to say that",
        " וזאת הברכה",
        " does not have a $maftir ",
        _strong("from within its boundaries"),
        ".)",
    ],
    [
        'The other type of non-numbered $aliyah is a "teaser" $aliyah.',
        " Every $parashah, be it single or dual, has exactly 3 teasers,",
        " identified as follows:",
        author.unordered_list(
            [
                "[כהן]",
                "[לוי]",
                "[ישראל]",
            ]
        ),
    ],
]
_NN_P2 = [
    "(Like $MAM, we always put the name of a teaser in square brackets.",
    " This is to avoid confusion with the 1st three numbered $aliyot,",
    " which are traditionally given to the same three groups",
    " as the teasers: $kohen, $levi, & $yisrael.)",
]
_NN_P3 = [
    "A dual $parashah does not have its own teasers or $maftir.",
    " Rather, it uses the teasers of its 1st $parashah",
    " and it uses the $maftir of its 2nd $parashah.",
]
_NN_P4 = [
    "The [ישראל] teaser is the only type of $aliyah",
    " whose end ever needs to be labelled.",
    " Below are the reasons for this.",
]
_NN_TABLE1 = my_html.table(
    [
        _tr(
            [
                _th(f"The end of a {_HELLIP}"),
                _th(f"never needs to be labelled because it always ends{_HELLIP}"),
            ]
        ),
        _tr(
            [
                _td("numbered $aliyah"),
                _td(
                    [
                        "Either: (1) just before the start of the next numbered $aliyah,",
                        " or (2) when the $parashah ends",
                    ]
                ),
            ]
        ),
        _tr([_td("$maftir"), _td("when the $parashah ends")]),
        _tr(
            [
                _td("[כהן] or [לוי] teaser"),
                _td("just before the start of the next teaser"),
            ]
        ),
    ]
)
_NN_P5 = [
    "In 43 of 54 cases, the [ישראל] teaser ends",
    " when the 1st s-$aliyah ends",
    " (s-$aliyah = $aliyah of a single $parashah).",
    " In other words, in most cases, the 3 teasers",
    " partition the 1st s-$aliyah.",
    " In these common cases,",
    " $MAM does not label the end of the [ישראל] teaser.",
    " Below, we describe the 11 cases that do not follow this pattern.",
    " I.e. below, we describe the 11 cases",
    " in which $MAM does explicitly label",
    " the end of the [ישראל] teaser.",
]
_NN_UL2 = [
    [
        "3 of the 11 cases: The [ישראל] teaser ends ",
        _strong("before"),
        " the 1st s-$aliyah ends. These cases are ",
        _rtl("בראשית"),
        ", ",
        _rtl("כי תשא"),
        ", and ",
        _rtl("נש\u05b9א"),
        ".",
    ],
    [
        "8 of the 11 cases: The [ישראל] teaser ends ",
        _strong("after"),
        " the 1st s-$aliyah ends.",
        author.unordered_list(
            [
                [
                    "3 of these 8 cases: The [ישראל] teaser ends",
                    " somewhere in the middle of the 2nd or 3rd s-$aliyah.",
                    " These cases are ",
                    _rtl("בח\u05bbק\u05b9תי"),
                    ", ",
                    _rtl("דברים"),
                    ", and ",
                    _rtl("ואתחנן"),
                    ". By coincidence, these happen to be the first 3 of the 8 cases,",
                    " in normal reading order.",
                ],
                [
                    "5 of these 8 cases: The [ישראל] teaser ends",
                    " when the 2nd, 3rd, or 4th s-$aliyah ends.",
                    " These cases are ",
                    _rtl("כי־תבוא"),
                    ", ",
                    _rtl("נ\u05b4צבים"),
                    ", ",
                    _rtl("וילך"),
                    ", ",
                    _rtl("האזינו"),
                    ", and ",
                    _rtl("וזאת הברכה"),
                    ".",
                ],
            ]
        ),
    ],
]
_NN_P6 = "The table below presents:"
_NN_UL3 = [
    [
        "a summary row for the 3 cases in which the [ישראל]",
        " teaser ends before the 1st s-$aliyah ends.",
    ],
    [
        "a summary row for the 43 cases in which the [ישראל]",
        " teaser ends when the 1st s-$aliyah ends.",
    ],
    [
        "a row for each of the 8 cases in which the [ישראל]",
        " teaser ends after the 1st s-$aliyah ends.",
    ],
]
_NN_P7 = [
    "Rather than being in normal reading order,",
    " they are presented in an order which more clearly reveals their regularities.",
    " The column labels are really labels of their left side.",
    " The numbers after the dot are not tenths, as in decimal notation.",
    ' Rather, they mean, roughly, "somewhere in the middle of."',
    " For example 1.2 & 1.3 mean",
    ' "somewhere in the middle of $aliyah 1',
    ' and somewhere later in the middle of $aliyah 1."',
    " So, the 3rd row, the row for דברים, can be read as:",
]
_NN_UL4 = [
    "The [לוי] teaser starts at 1.2: somewhere in the middle of $aliyah 1.",
    "The [ישראל] teaser starts at 1.3: somewhere later in the middle of $aliyah 1.",
    "The [ישראל] teaser ends at 2.1: somewhere in the middle of $aliyah 2.",
]
_NN_P8 = [
    "Column labels are repeated at the end of the [ישראל]",
    " teaser, for clarity.",
]

_LEVI = "[לוי]"
_YL = "[י״ל]"


def _teaser_row(name, cells):
    """Build a row of the teaser table: name cell followed by given cells."""
    return _tr([_td(name)] + cells)


_TEASER_HDR = _tr(
    [_td("")]
    + [_td(c) for c in ["1.1", "1.2", "1.3", "2", "2.1", "3", "3.1", "4", "5"]]
)
_TEASER_TABLE = my_html.table(
    [
        _TEASER_HDR,
        _teaser_row(
            "3 cases",
            [_bor(_LEVI), _bor(_YL), _td("1.3")],
        ),
        _teaser_row(
            "43 cases",
            [_td(""), _bor(_LEVI), _bor(_YL), _td("2")],
        ),
        _teaser_row(
            "דברים",
            [_td(""), _bor(_LEVI), _bor(_YL, colspan="2"), _td("2.1")],
        ),
        _teaser_row(
            "ואתחנן",
            [_td(""), _td(""), _bor(_LEVI), _bor(_YL, colspan="1"), _td("2.1")],
        ),
        _teaser_row(
            "כי־תבוא",
            [_td(""), _td(""), _bor(_LEVI), _bor(_YL, colspan="2"), _td("3")],
        ),
        _teaser_row(
            "האזינו",
            [_td(""), _td(""), _bor(_LEVI), _bor(_YL, colspan="2"), _td("3")],
        ),
        _teaser_row(
            "בח\u05bbק\u05b9תי",
            [
                _td(""),
                _td(""),
                _td(""),
                _bor(_LEVI, colspan="2"),
                _bor(_YL, colspan="1"),
                _td("3.1"),
            ],
        ),
        _teaser_row(
            "נ\u05b4צבים",
            [
                _td(""),
                _td(""),
                _td(""),
                _bor(_LEVI, colspan="2"),
                _bor(_YL, colspan="2"),
                _td("4"),
            ],
        ),
        _teaser_row(
            "וזאת הברכה",
            [
                _td(""),
                _td(""),
                _td(""),
                _bor(_LEVI, colspan="2"),
                _bor(_YL, colspan="2"),
                _td("4"),
            ],
        ),
        _teaser_row(
            "וילך",
            [
                _td(""),
                _td(""),
                _td(""),
                _bor(_LEVI, colspan="2"),
                _bor(_YL, colspan="3"),
                _td("5"),
            ],
        ),
    ]
)

_NN_P9 = [
    "Actually $MAM labels not so much the end of [ישראל]",
    " as the 1st verse after [ישראל].",
    " For this, it uses the label",
    " [ע״כ ישראל],",
    ' meaning "$yisrael until here."',
]
_NN_P10 = [
    "In $MAM, the 1st $aliyah is not labelled ראשון,",
    " nor is it labelled [כהן].",
    " Rather, it is labelled with the name of the single $parashah.",
    " Below is a table showing the 1st few $aliyah labels",
    " $MAM uses for the $parashah נ\u05b9ח.",
    " The table also shows an expanded form of these labels,",
    " where everything is laid out explicitly, albeit with gray used for",
    " the parts that $MAM leaves implicit.",
]

_NOAH = "נ\u05b9ח"
_LABEL_TABLE = my_html.table(
    [
        _tr([_bor("compact form"), _bor("expanded form", colspan="3")]),
        _tr(
            [
                _td(_NOAH),
                _td(_NOAH),
                _imp("ראשון"),
                _imp("[כהן]"),
            ]
        ),
        _tr(
            [
                _td("[לוי]"),
                _imp(_NOAH),
                _td(""),
                _td("[לוי]"),
            ]
        ),
        _tr(
            [
                _td("[ישראל]"),
                _imp(_NOAH),
                _td(""),
                _td("[ישראל]"),
            ]
        ),
        _tr(
            [
                _td("שני"),
                _imp(_NOAH),
                _td("שני"),
                _imp("[ע״כ ישראל]"),
            ]
        ),
        _tr(
            [
                _td("שלישי"),
                _imp(_NOAH),
                _td("שלישי"),
                _td(""),
            ]
        ),
    ]
)

_NN_P11 = [
    "In the $parashiyot עקב",
    " and נ\u05b4צבים,",
    " the $maftir $aliyah is the same as the 7th $aliyah.",
    " Every other $parashah with a $maftir,",
    " be it single or dual,",
    " has that $maftir starting later than the start of the 7th $aliyah.",
]

# ── Body assembly ──

_CBODY = [
    author.heading_level_1(_H1),
    author.para(_AUTHOR),
    author.para(_REVISION),
    # Introduction
    author.heading_level_2("Introduction"),
    author.para(_INTRO_P1),
    author.unordered_list(_INTRO_UL1),
    author.para(_INTRO_P2),
    author.unordered_list(_INTRO_UL2),
    author.para(_INTRO_P3),
    _INTRO_TABLE1,
    author.para(_INTRO_P4),
    author.unordered_list(_INTRO_UL3),
    author.para(_INTRO_P5),
    author.unordered_list(_INTRO_UL4),
    # Dual parashiyot
    author.heading_level_2("Dual $parashiyot"),
    author.para(_DUAL_P1),
    author.ordered_list(_DUAL_OL1),
    author.para(_DUAL_P2),
    author.unordered_list(_DUAL_UL1),
    author.para(_DUAL_P3),
    _DUAL_TABLE1,
    author.para(_DUAL_P4),
    author.unordered_list(_DUAL_UL2),
    author.para(_DUAL_P5),
    author.para(_DUAL_P6),
    _PART_TABLE,
    author.para(_PART_EXPL_P),
    author.unordered_list(_PART_EXPL_UL),
    author.para(_PART_NOTES_P),
    author.unordered_list(_PART_NOTES_UL),
    # Non-numbered aliyot
    author.heading_level_3("Non-numbered $aliyot"),
    author.para(_NN_P1),
    author.unordered_list(_NN_UL1),
    author.para(_NN_P2),
    author.para(_NN_P3),
    author.para(_NN_P4),
    _NN_TABLE1,
    author.para(_NN_P5),
    author.unordered_list(_NN_UL2),
    author.para(_NN_P6),
    author.unordered_list(_NN_UL3),
    author.para(_NN_P7),
    author.unordered_list(_NN_UL4),
    author.para(_NN_P8),
    _TEASER_TABLE,
    author.para(_NN_P9),
    author.para(_NN_P10),
    _LABEL_TABLE,
    author.para(_NN_P11),
    # End
    author.heading_level_3("End of document"),
]
