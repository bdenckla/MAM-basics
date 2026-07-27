"""Exports gen_html_file.

Ported from the published Google Doc of the same title. The prose is
reproduced verbatim; the only deliberate changes are the ``$`` keys that
``dollar_sub`` requires, and the three intra-series links, which now point at
the sibling pages rather than at the Google Docs.
"""

from mb_misc import mb_html
from mb_author import author
from author_misc import urwotm_common


def anchor():
    return urwotm_common.anchor_part(2)


def gen_html_file(tdm_ch):
    cbody = [
        author.heading_level_1(urwotm_common.heading_1(_PART)),
        author.heading_level_2(urwotm_common.heading_2(_PART)),
        author.para(_PARA_002),
        author.unordered_list(urwotm_common.other_parts(_PART)),
        author.para(_PARA_004),
        author.para(_PARA_005),
        author.para(_PARA_006),
        author.para(_PARA_007),
        author.std_table(_TABLE_008),
        author.para(_PARA_009),
        author.unordered_list(_LIST_010),
        author.para_for_img(
            "urwotm/2Sam 13v33 and 15v21 אם -- WLC qere ketiv.png", width_em=36.0
        ),
        author.para(_PARA_012),
        author.unordered_list(_LIST_013),
        author.para(_PARA_014),
        author.std_table(_TABLE_015),
        author.para(_PARA_016),
        author.para(_PARA_017),
        author.para(_PARA_018),
        author.para(_PARA_019),
        author.unordered_list(_LIST_020),
        author.para(_PARA_023),
        author.para(_PARA_024),
        author.para_for_img(
            "urwotm/2Sam 15v21 אם -- BHS masorah qetanah.png", width_em=31.5
        ),
        author.para(_PARA_026),
        author.para(_PARA_027, {"class": "center"}),
        author.para(_PARA_028),
        author.unordered_list(_LIST_029),
        author.para(_PARA_030),
        author.para(_PARA_031, {"class": "center"}),
        author.para(_PARA_032),
        author.para(_PARA_033, {"class": "center"}),
        author.para(_PARA_034),
        author.para(_PARA_035, {"class": "center"}),
        author.para(_PARA_036),
        author.para_for_img("urwotm/2Sam אם -- L masorah qetanah.png", width_em=7.0),
        author.para(_PARA_038),
        author.para_for_img(
            "urwotm/Jer 51v3 ידרך -- L masorah gedolah page 274B.png", width_em=131.3
        ),
        author.para_hbo(_HBO_040),
        author.para(_PARA_041),
        author.para(_PARA_042),
        author.para(_PARA_043),
        author.para_for_img("urwotm/2Sam 13v33 כי־אם -- JPS HET.png", width_em=10.6),
        author.para_for_img(
            "urwotm/2Sam 13v33 כי־אם -- JPS HET note.png", width_em=21.3
        ),
        author.para_for_img("urwotm/2Sam 15v21 אם־במקום -- JPS HET.png", width_em=16.0),
        author.para_for_img(
            "urwotm/2Sam 15v21 אם־במקום -- JPS HET note.png", width_em=21.5
        ),
        author.para(_PARA_048),
        author.para(_PARA_049),
        author.para(_PARA_050),
        author.para(_PARA_051),
        author.para(_PARA_052),
        author.para(_PARA_053),
        author.para(_PARA_054),
        author.para(_PARA_055),
        author.para(_PARA_056),
        author.para(_PARA_057),
        author.para(_PARA_058),
        author.para(_PARA_059),
        author.para(_PARA_060),
        author.unordered_list(_LIST_061),
        author.para(_PARA_062),
        author.para_for_img(
            "urwotm/2Sam 15v21 אם -- BHS masorah circles.png", width_em=13.2
        ),
        author.para(_PARA_064),
        author.para_for_img(
            "urwotm/2Sam 15v21 -- BHS masorah qetanah notes.png", width_em=32.2
        ),
        author.para(_PARA_066),
        author.para_for_img(
            "urwotm/2Sam 15v21 ויאמר -- BHS masorah circle.png", width_em=12.4
        ),
        author.para(_PARA_068),
        author.para_for_img(
            "urwotm/2Sam 3v33 ויאמר -- BHS masorah qetanah.png", width_em=41.0
        ),
        author.para(_PARA_070),
        author.para(_PARA_071),
        author.para_for_img(
            "urwotm/Jer 22v12 -- BHS masorah qetanah.png", width_em=25.1
        ),
        author.para(_PARA_073),
        author.para(_PARA_074),
        author.para(_PARA_075),
        author.para(_PARA_076),
        author.para_for_img("urwotm/2Sam 13v33 כי אם -- Aleppo.png", width_em=16.0),
        author.para_for_img("urwotm/2Sam 15v21 אם -- Aleppo.png", width_em=17.9),
        author.para(_PARA_079),
        author.para_for_img(
            "urwotm/2Sam 13v33 כי־אם־אמנון -- MAM Wikisource.png", width_em=21.7
        ),
        author.para_for_img(
            "urwotm/2Sam 15v21 אם־במקום -- MAM Wikisource.png", width_em=24.1
        ),
        author.para(_PARA_082),
        author.para(_PARA_083),
        author.para_for_img(
            "urwotm/2Sam 13v33 כי־אם־אמנון -- long maqaf alternative.png", width_em=21.2
        ),
        author.para(_PARA_085),
        author.para(_PARA_086),
        author.unordered_list(_LIST_087),
        author.para(_PARA_088),
        author.unordered_list(_LIST_089),
    ]
    return author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, cbody)


_PART = 2
_TITLE = urwotm_common.plain_title(_PART)
_FNAME = urwotm_common.FNAMES[_PART]

_URL_TANACH_US_1 = (
    "https://tanach.us/Changes/2020.10.19%20-%20Changes/2020.10.19%20-%"
    "20Changes.xml?2020.09.23-1"
)
_URL_TANACH_US_2 = (
    "https://tanach.us/Changes/2020.10.19%20-%20Changes/2020.10.19%20-%"
    "20Changes.xml?2020.09.23-2"
)
_URL_MANUSCRIPTS_SEFARIA_ORG_1 = (
    "https://manuscripts.sefaria.org/leningrad-color/BIB_LENCDX_F274B.jpg"
)
_URL_BDENCKLA_GITHUB_IO_1 = "https://bdenckla.github.io/MAM-with-doc/"
_URL_BDENCKLA_GITHUB_IO_2 = (
    "https://bdenckla.github.io/MAM-with-doc/foi/foi-kq-simple.html#int"
    "ro-x-velo-y-k-velo-q"
)

_PARA_002 = """This is the second article in a series. The series is about errors in $BHS and/or
$WLC. The other articles in the series are as follows:""".replace(
    "\n", " "
)
_PARA_004 = """In this article I’ll explore two errors in $WLC that are similar to each other. As
in the first article, we will look at editions that share these errors and editions
that lack these errors. Editions that share these errors likely share them causally,
by being derived from $WLC, rather than coincidentally. Editions may lack these
errors because they never had them, or because they have been corrected.""".replace(
    "\n", " "
)
_PARA_005 = """As in the first article, my intent is both specific and general. Specifically, I’m
trying to draw attention to the shortcomings of close-to-$WLC editions. They are not
appropriate for the general purposes for which they are widely pressed into service.
(Indeed, these editions are not even the best for the narrow purpose $WLC was
intended to serve: being a strictly diplomatic edition of ל.)""".replace(
    "\n", " "
)
_PARA_006 = """Generally, I’m trying to shed light on how one makes and improves high quality
editions of the Hebrew Bible. The specifics of the first article gave the reader a
taste of general issues such as the grammar of accents and the use of multiple
manuscripts. Here, the specifics will again give the reader a taste of more general
issues. In this case, our use of specific $masorah notes gives a taste of what those
notes are like, in general.""".replace(
    "\n", " "
)
_PARA_007 = [
    "Now, back to the specifics. $WLC fails to identify two cases in which the",
    " word אם is a $ketiv_velo_qere (henceforth k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    ": kq with the q struck through). As a reminder, a k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    " is a word that finds itself in the following sticky situation:",
]
_PARA_008_r0c0_0 = "According to the writing ($ketiv) tradition, this word …"
_PARA_008_r0c1_0 = [
    author.emphasis("should"),
    " be written (e.g. in unpointed scrolls)",
]
_PARA_008_r1c0_0 = "According to the reading ($qere) tradition, this word …"
_PARA_008_r1c1_0 = [
    author.emphasis("should not"),
    " be “cried out” (chanted or spoken aloud)",
]
_TABLE_008 = [
    [
        author.para(_PARA_008_r0c0_0),
        author.para(_PARA_008_r0c1_0),
    ],
    [
        author.para(_PARA_008_r1c0_0),
        author.para(_PARA_008_r1c1_0),
    ],
]
_PARA_009 = """In these two cases, $WLC correctly transcribes the body text of $BHS, which in turn
correctly transcribes ל. But $WLC fails to identify the letters (and pointing!) of
אם as belonging only to the writing ($ketiv) tradition. These cases are both in 2
Samuel: 13:33 and 15:21. Below we show them in three ways:""".replace(
    "\n", " "
)
_LIST_010 = [
    "As they are in $WLC (converted to Unicode and rendered by a font).",
    [
        "As they would be chanted, according to מ״ק-ל (the $masorah_qetanah note in",
        " ל), which identifies אם as a k",
        mb_html.span("q", {"style": "text-decoration: line-through"}),
        ".",
    ],
    "As they would be written in an unpointed scroll.",
]
_PARA_012 = """Above, we separate out the $qere and $ketiv into their own rows rather than trying
to show them “inline” since:""".replace(
    "\n", " "
)
_LIST_013 = [
    "There are a variety of ways to show $qere and $ketiv inline.",
    "All of those ways may be confusing here, because of issues related to $maqaf.",
]
_PARA_014 = """In $UXLC, which for these purposes can be considered a corrected version of $WLC,
the two cases look like this (as rendered in $UXLC’s canonical edition at
tanach.us):""".replace(
    "\n", " "
)
_TABLE_015 = [
    [
        author.para_for_img("urwotm/2Sam 13v33 כי־אם־אמנון -- UXLC.png", width_em=22.2),
        author.para_for_img("urwotm/2Sam 15v21 אם־במקום -- UXLC.png", width_em=24.9),
    ],
]
_PARA_016 = """The correction involves no change to any letter or pointing. The correction simply
identifies אִם־ as belonging only to the writing ($ketiv) tradition. In the
underlying $UXLC dataset, this means wrapping אִם־ in a <k> rather than <w> XML tag.
(The <k> tag is for $ketiv words and the <w> tag is for normal words.) In the
canonical edition of $UXLC, $ketiv words are shown in a reddish-brown color and
above the normal text’s baseline.""".replace(
    "\n", " "
)
_PARA_017 = [
    "To reiterate: $WLC provides a good representation of how these words appear",
    " in $BHS and ל. In each case, the only way in which $WLC differs from $BHS and",
    " ל is by lacking a $masorah circle. This lack of a $masorah circle is",
    " expected. What is unexpected is that $WLC fails to reflect the ",
    author.emphasis("meaning"),
    " of the $masorah note “called out” by the circle. That $masorah note",
    " identifies אם as a k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    ". (Actually, in 15:21, $BHS has a $masorah circle not only above אם but also",
    " right before & right after it. These circles before and after are not",
    " relevant here, but for completeness we discuss them much further below.)",
]
_PARA_018 = [
    "It is not surprising that these errors in $WLC are shared by Logos LHB and",
    " Accordance HMT-W4. These errors were also shared by $UXLC, but I proposed",
    " corrections and they were accepted (",
    author.anc_h("13:33", _URL_TANACH_US_1),
    ", ",
    author.anc_h("15:21", _URL_TANACH_US_2),
    ").",
]
_PARA_019 = """$WLC’s errors here are not errors in $BHS. They are merely two of those rare cases
in which $WLC did not faithfully transcribe $BHS. $WLC’s failures are understandable
here because of the following:""".replace(
    "\n", " "
)
_LIST_020 = [
    [
        "$WLC does not transcribe the vast majority of $BHS $masorah_qetanah notes",
        " (מ״ק-$BHS). The only ones transcribed are those regarding $ketiv and/or $qere",
        " words, and even those are transcribed only in a stylized way.",
    ],
    [
        "מ״ק-$BHS for k",
        mb_html.span("q", {"style": "text-decoration: line-through"}),
        " are easy to miss since they don’t look like a plain old $ketiv_veqere note.",
    ],
    [
        "K",
        mb_html.span("q", {"style": "text-decoration: line-through"}),
        " words are rare: these two are two of only 8 total.",
    ],
    [
        [
            "These cases are additionally exceptional because they are pointed in $BHS,",
            " correctly reflecting ל! So there is no clue in the body text of $BHS that",
            " these might be k",
            mb_html.span("q", {"style": "text-decoration: line-through"}),
            ". (The other six k",
            mb_html.span("q", {"style": "text-decoration: line-through"}),
            " are unpointed in $BHS). They are pointed in the following two ways:",
        ],
        author.unordered_list(
            [
                "They both have a $xiriq below the $alef.",
                [
                    [
                        "They both have a $maqaf after אם that makes אם look like a plain old atom",
                        " within a $maqaf compound. These compounds are as follows:",
                    ],
                    author.unordered_list(
                        [
                            [
                                "כי־",
                                author.span_color("אם־", "#ff0000"),
                                "אמנון",
                            ],
                            [
                                author.span_color("אם־", "#ff0000"),
                                "במקום",
                            ],
                        ]
                    ),
                ],
            ]
        ),
    ],
]
_PARA_023 = [
    "The factors above give me some sympathy for the difficulty in transcribing",
    " $BHS in these two cases. On the other hand, it is disappointing that the",
    " transcribers failed to take advantage of the classic Masoretic",
    " error-detection mechanism: lists and counts. This mechanism is included in",
    " $BHS in all 8 k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    ", so they should have noticed it in at least one of the 6 k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    " that they did transcribe correctly.",
]
_PARA_024 = [
    "Here’s the מ״ק-$BHS for the 2Sam 15:21 case of k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    ", showing the count of 8 k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    ":",
]
_PARA_026 = """All 8 מ״ק-$BHS take this form, varying only by the $ketiv word in question and the
footnote number. I.e. all 8 מ״ק-$BHS take the following form:""".replace(
    "\n", " "
)
_PARA_027 = [
    urwotm_common.romanized("k"),
    " חד מן ח",
    mb_html.sup(urwotm_common.romanized("n")),
    " כת̇ ולא קר̇",
]
_PARA_028 = "where:"
_LIST_029 = [
    [
        urwotm_common.romanized("k"),
        " is the $ketiv word in question (e.g. אם).",
    ],
    [
        urwotm_common.romanized("n"),
        " is the number of a footnote whose contents is “Mm. 2752,” presumably",
        " referring to the $masorah_gedolah note in ל (henceforth מ״ג-ל) on ",
        author.anc_h("page 274B", _URL_MANUSCRIPTS_SEFARIA_ORG_1),
        ". This note is described in greater detail further below.",
    ],
]
_PARA_030 = (
    "Expanding its footnote and abbreviations, this note can be translated to mean:"
)
_PARA_031 = [
    urwotm_common.romanized("k"),
    " is one of the 8 k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    " listed in Mm. 2752.",
]
_PARA_032 = """I have been careful to call this note a מ״ק-$BHS, not a מ״ק-ל, because this note is
a helpful mix of a מ״ק-ל and a מ״ג-ל. Coloring the מ״ג-ל part green and
square-bracketing it yields:""".replace(
    "\n", " "
)
_PARA_033 = [
    urwotm_common.romanized("k"),
    " ",
    author.span_color("[חד מן ח", "#6aa84f"),
    author.span_color(mb_html.sup("n"), "#6aa84f"),
    author.span_color("]", "#6aa84f"),
    " כת̇ ולא קר̇",
]
_PARA_034 = "I.e. the actual מ״ק-ל merely reads (modulo differences in abbreviation):"
_PARA_035 = [
    urwotm_common.romanized("k"),
    " כת̇ ולא קר̇",
]
_PARA_036 = [
    "For example, for ",
    urwotm_common.romanized("k"),
    " = אם:",
]
_PARA_038 = [
    "Presumably $BHS’s Mm. 2752 is the מ״ג-ל on ",
    author.anc_h("page 274B", _URL_MANUSCRIPTS_SEFARIA_ORG_1),
    " (the page of the Jer. 51:3 ידרך k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    "). In this note, the count of 8 k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    " is given, and those 8 cases are identified in the cryptically concise form",
    " that is typical of $masorah_gedolah notes:",
]
_HBO_040 = "חׄ כותבׄ ולא קרי ‏נא את ידרך חמש דנגב אמנון במקום כאשר גאל"
_PARA_041 = [
    "As fun as they are, we will not delve into the details of this list except to",
    " say that the 8 cases are only identified with sufficient detail to ",
    author.emphasis("check them"),
    " against a fully-detailed list. They are not identified with sufficient detail",
    " to ",
    author.emphasis("constitute"),
    " a fully-detailed list. For more information see Dotan and Reich’s ",
    author.book_title("Masorah Thesaurus"),
    ".",
]
_PARA_042 = [
    "It is disappointing that the $WLC transcribers failed to take advantage of",
    " the error-detection mechanism provided by ל, especially since this mechanism",
    " was helpfully reproduced in all 8 relevant locations by $BHS. Such errors",
    " undo the work of the Masoretes despite the mechanism intended to avoid such",
    " undoing. In other words, the Masoretes (and the $BHS editors!) were well",
    " aware of how easy it would be to miss these k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    ", so they added a mechanism to try to make sure they weren’t missed. This",
    " mechanism failed.",
]
_PARA_043 = "Commendably, the $JPS HET corrects these errors in $WLC:"
_PARA_048 = [
    "BHL and ",
    author.book_title("Keter Yerushalayim"),
    " correctly identify these k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    ". This is not surprising since these editions were overseen by great scholars",
    " of the Masorah. Koren implicitly identifies these k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    " by leaving them unpointed, but to me this is dangerously subtle. I give Koren",
    " “half credit” 😉.",
]
_PARA_049 = [
    "$MAM correctly identifies these k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    ". The “",
    author.anc_h("$MAM with doc", _URL_BDENCKLA_GITHUB_IO_1),
    "” edition also includes ",
    author.anc_h("a list called “x-velo-y-k-velo-q", _URL_BDENCKLA_GITHUB_IO_2),
    "”, which is a version of the Masoretic list of the 8 k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    ". This list is one of many “features of interest” lists that are part of",
    " “$MAM with doc.” Some of these lists mirror lists or counts made by the",
    " Masoretes. The rest of these lists, though not Masoretic in that strict",
    " sense, are certainly Masoretic in spirit.",
]
_PARA_050 = """These lists are generated by a program that runs on $MAM’s sources. Thus they cannot
get out of sync with $MAM’s sources. In this way we avoid the problem the Masoretes
had, where sometimes a $masorah note would contradict the body text of the
manuscript in whose margin it was written.""".replace(
    "\n", " "
)
_PARA_051 = "Did ל get these cases wrong or right?"
_PARA_052 = [
    "My answer is the typical hedge: “yes and no.” The fact that אם is pointed in",
    " ל (i.e. the fact that אם has $xiriq and $maqaf marks) contradicts the",
    " $masorah_qetanah of ל. The pointing is wrong but the מ״ק is right. To be",
    " clear, the pointing is not wrong in the sense that, for example, the $xiriq",
    " should be a $tsere or something like that. The pointing is wrong in the sense",
    " that there should be no pointing at all there. The מ״ק is right not only",
    " according to other manuscripts (not discussed here) but also according to ל",
    " itself, in its $masorah_gedolah note elsewhere (on ",
    author.anc_h("page 274B", _URL_MANUSCRIPTS_SEFARIA_ORG_1),
    ").",
]
_PARA_053 = [
    "The $naqdan of ל (the pointing scribe of ל) made an error by pointing these",
    " two words. These errors did not cause errors in $BHS, but these errors are",
    " probably what caused $WLC to fail to identify these words as k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    ".",
]
_PARA_054 = [
    "This is one of the many pitfalls of $BHS’s fateful decision to build a",
    " critical edition using ל as its base text rather than some eclectic consensus",
    " text. Though Dotan’s BHL is not a critical edition, it provides a useful",
    " contrast to $BHS. BHL meticulously transcribes ל, in fact it transcribes ל",
    " better than $BHS. But, importantly, BHL transcribes ל ",
    author.emphasis("in its notes"),
    " whenever ל’s errors or idiosyncrasies would be inappropriate for a",
    " general-purpose text. In contrast, by using ל as its body text, $BHS",
    " contributed to the misunderstanding that ל somehow ",
    author.emphasis("is"),
    " the consensus Masoretic text.",
]
_PARA_055 = """Some of the fault for this misunderstanding does not lie with $BHS, but rather lies
with the inappropriately general ways in which $BHS’s body text has been pressed
into service. For example, it is one thing for the mention of errors in ל to be
relegated to notes; but it is quite another for those notes to be stripped away, as
in Accordance and Logos, where the $BHS apparatus is only available as a separate
product!""".replace(
    "\n", " "
)
_PARA_056 = "Did $BHS get these cases wrong or right?"
_PARA_057 = [
    "$BHS commits no error by accurately transcribing an error in the body text of",
    " ל, because $BHS is a strictly diplomatic edition of ל. But $BHS can be",
    " faulted if it does not ",
    author.emphasis("note"),
    " the error. $BHS has apparatus notes on both אם but only the note on 15:21",
    " indicates an error in ל. Here are the notes (with some expansion of some",
    " abbreviations) (𝔊=Greek, 𝔏=Latin, 𝔖=Syriac, 𝔙=Vulgate):",
]
_PARA_058 = [
    "13:33 אם: > nonnulli Mss cf 𝔊",
    mb_html.sup("AMs"),
    "𝔏",
    mb_html.sup("115"),
    "𝔖𝔙",
]
_PARA_059 = "15:21 אם: sic L; > pauci Mss cf 𝔊𝔖𝔙; permulti Mss ut Ketib"
_PARA_060 = """Ignoring “ > pauci Mss cf 𝔊𝔖𝔙 ” since non-Hebrew manuscripts are irrelevant for our
purposes, the 15:21 note is reduced to “sic L; permulti Mss ut Ketib,” which I take
to mean:""".replace(
    "\n", " "
)
_LIST_061 = [
    [
        author.emphasis("So"),
        " [in] ",
        author.emphasis("L"),
        " [i.e. the fact that אם is pointed is an error in L, not an error in $BHS];",
    ],
    [
        "[unlike L,] ",
        author.emphasis("very many"),
        " [Hebrew] ",
        author.emphasis("manuscripts"),
        " [have this] ",
        author.emphasis("as"),
        " [a] ",
        author.emphasis("Ketib"),
        " [i.e. have אם unpointed].”",
    ],
]
_PARA_062 = """While we’re scrutinizing $BHS, I will return to something I mentioned in passing far
above: in $BHS, the אם of 15:21 has not only a $masorah circle right above it, but
also has one right before and right after it:""".replace(
    "\n", " "
)
_PARA_064 = """I am confused by this since there is an additional $masorah circle earlier in the
line, bringing the total to four, yet there are only three $masorah notes in the
margin:""".replace(
    "\n", " "
)
_PARA_066 = "The $masorah circle earlier in the line appears on ויאמר, like this:"
_PARA_068 = """I take the first note, צא, to apply to ויאמר, i.e. to apply to the first $masorah
circle on the line. צא represents the number 91 despite its lack of “number dots”
above $tsade and $alef. In similar contexts, the number dots do appear, e.g. in
3:33:""".replace(
    "\n", " "
)
_PARA_070 = [
    "(By the way, this line above also has what seems to be an extra $masorah",
    " circle.) There are actually 121 cases of this special pausal form of ויאמר,",
    " not 91. But only 4 of Job’s 34 are counted, with the remaining 30 only eluded",
    " to in the first of these צא notes (Gen 14:19). See Dotan and Reich’s ",
    author.book_title("Masorah Thesaurus"),
    ".",
]
_PARA_071 = [
    "I take the second note, ב̇",
    mb_html.sup("20"),
    " ($bet with an above-dot and a callout to note 20), to apply to the second",
    " $masorah circle on the line, which is the circle right before אם (or, if you",
    " like, right after כי.). Note 20 says “Cf Jer 22,12 et Mp sub loco.” The first",
    " two words of Jeremiah 22:12 are indeed quite analogous to the $qere of 2",
    " Samuel 15:19:",
]
_PARA_073 = [
    "$BHS’s “Mp sub loco” for Jer. 22:12 is complementary: it is ב̇",
    mb_html.sup("12"),
    " ($bet with an above-dot and a callout to note 12), where note 12 says “Cf 2 S",
    " 15,21 et Mp sub loco.” The $masorah circle corresponding to this note is, as",
    " in 2S 15:21, right after כי (or, if you like, between כי and במקום).",
]
_PARA_074 = [
    "I take the third note, אם חד מן ח",
    mb_html.sup("20"),
    " כת̇ ולא קר̇, to apply to the third $masorah circle on the line, which is the",
    " circle above אם. We have discussed this note above. It is one of 8 notes like",
    " it.",
]
_PARA_075 = """There seems to be no note corresponding to the fourth $masorah circle on the line,
which is the circle just after אם (or if you like, above the $maqaf).""".replace(
    "\n", " "
)
_PARA_076 = [
    "In the Aleppo Codex, our two cases appear unpointed, as one would expect: no ",
    urwotm_common.romanized("hiriq"),
    " under the $alef of אם and no $maqaf after the final $mem of אם. The only",
    " “decoration” on אם is the $masorah circle.",
]
_PARA_079 = (
    "In the Hebrew Wikisource edition of $MAM, our two cases are rendered like this:"
)
_PARA_082 = [
    "This edition of $MAM renders k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    " in gray and in parenthesis. But in 13:33, the spurious $maqaf of the $naqdan",
    " of ל seems to have propagated here, albeit in gray, but outside of the",
    " parenthesis! Is this an error? We don’t think so. Rather, it is this",
    " edition’s way of showing, in an “inline” way, $ketiv words inside $maqaf",
    " compounds. The $maqaf in question is placed outside the parenthesis, to show",
    " that it is not part of the $ketiv proper. But it is still gray, to show that",
    " it is not really part of the $qere either.",
]
_PARA_083 = """The idea behind this gray $maqaf is to prevent the $ketiv from visually breaking up
the $maqaf compound of the $qere: כי־אמנון. One might imagine a variety of other
ways to express this. For example, we might use a very long $maqaf:""".replace(
    "\n", " "
)
_PARA_085 = """All such alternatives I can think of are typographically complex, beyond the scope
of what Wikisource can easily express.""".replace(
    "\n", " "
)
_PARA_086 = [
    "Let’s finish by summarizing. $WLC missed the two instances of k",
    mb_html.span("q", {"style": "text-decoration: line-through"}),
    " ($ketiv_velo_qere) in 2 Samuel.",
]
_LIST_087 = [
    "Logos and Accordance have not corrected these errors.",
    "$UXLC has corrected these errors.",
    [
        "HET and $MAM do not share these errors. Though distantly based on $WLC, these",
        " editions were edited far away from $WLC.",
    ],
    [
        "BHL, ",
        author.book_title("Keter Y"),
        "., and Koren do not share these errors. These editions are not based on $WLC.",
    ],
]
_PARA_088 = """These errors represent a failure of the Masoretic mechanism put in place to try to
avoid such errors.""".replace(
    "\n", " "
)
_LIST_089 = [
    [
        "$BHS not only faithfully reproduced this mechanism but also made it visible",
        " in all 8 relevant cases, to no avail.",
    ],
    "The $naqdan of ל made, in a way, the same errors as $WLC.",
    [
        "The errors of the $naqdan are probably what made the Masoretic",
        " error-detection mechanism fail for $WLC.",
    ],
]
