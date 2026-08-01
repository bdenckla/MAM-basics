"""htel element body migrated byte-exactly from the former hand-authored gh-
pages/accgram/ps17v14-mam-doc-notes.html. Consumed by accgram/ps17v14_doc_notes.py; edit
the generator/this data, not the generated HTML.

Migrated from the former hand-authored JSON sidecar ps17v14_mam_doc_notes_body.json (issue #33):
read via import, not a file open.  Edit this module / the generator, not the
generated HTML.

The BYTE-EXACTNESS above is a claim about THIS DATA, not about the page any more.  The
htels here are literal dicts that pin lb1/lb2 on inline tags only, so h1/p and friends
used to take the serializer's old lb1="\\n" default; since the move to tag-keyed break
tables in ``py_html/wlc_utils_html.py`` they take lb1="", and the page no longer carries
a newline straight after those block-level open tags.  No browser renders the difference,
and it is what makes this page break like the other 151.  See that module's table comment.
"""

TITLE = "MAM documentation notes on Psalms 17:14 — translation"

BODY = [
    "\n\n",
    {
        "_htel_tag": "h1",
        "contents": ["MAM documentation notes on Psalms 17:14 (translated)"],
    },
    "\n\n",
    {
        "_htel_tag": "p",
        "attr": {"class": "note-lead"},
        "contents": [
            "An English rendering of the four MAM נוסח (text-variant) documentation\n"
            "notes on this verse, one per chanted word. Manuscript sigils and the technical\n"
            "accent/mark names are left in Hebrew and explained rather than replaced, and the\n"
            "implicit subject “MAM” is supplied wherever a note begins with\n"
            "“=”. Source:\n",
            {
                "_htel_tag": "a",
                "attr": {
                    "href": "https://bdenckla.github.io/MAM-with-doc/D1-Psalms.html#c17v14"
                },
                "lb1": "",
                "lb2": "",
                "contents": ["MAM-with-doc, Psalms 17:14"],
            },
            ".",
        ],
    },
    "\n\n",
    {
        "_htel_tag": "h2",
        "contents": [
            "Note 1 — on ",
            {
                "_htel_tag": "span",
                "attr": {"class": "lemma", "lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["מִ֥מְתִֽים־יָדְךָ֨\u202f׀"],
            },
        ],
    },
    "\n\n",
    {
        "_htel_tag": "p",
        "contents": [
            {"_htel_tag": "strong", "lb1": "", "lb2": "", "contents": ["MAM = "]},
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["ש1, ק13, ל-א, גסטר1"],
            },
            "\n(with respect to the ",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["מרכא"],
            },
            " [merkha] as a secondary accent\n[",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["טעם משני"],
            },
            "], the ",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["געיה"],
            },
            " [ga’ya]\non the stressed syllable, and the ",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["מקף"],
            },
            " [maqqef]). In these\nmanuscripts (",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["ש1"],
            },
            " = Sassoon 1053,\n",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["ק13"],
            },
            " = Cambridge T-S 13,\n",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["ל-א"],
            },
            " = St. Petersburg EVR-II-B-55,\n",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["גסטר1"],
            },
            " = Gaster 1), and in keeping with the practice of\n"
            "the Keter (Aleppo Codex), there is ",
            {
                "_htel_tag": "em",
                "lb1": "",
                "lb2": "",
                "contents": [
                    "also a ",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["חטף"],
                    },
                    "\n[ḥataf]",
                ],
            },
            ", to indicate the mobilization of the ",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["שווא"],
            },
            "\n[shva] after a merkha functioning as a secondary accent:\n",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["‹מִ֥מֲתִֽים־יָדְךָ֨\u202f׀›"],
            },
            ".",
        ],
    },
    "\n\n",
    {
        "_htel_tag": "ul",
        "contents": [
            "\n",
            {
                "_htel_tag": "li",
                "contents": [
                    "Regarding the merkha and the ga’ya, see ",
                    {
                        "_htel_tag": "strong",
                        "lb1": "",
                        "lb2": "",
                        "contents": [
                            "Breuer,\n",
                            {
                                "_htel_tag": "em",
                                "lb1": "",
                                "lb2": "",
                                "contents": ["Ṭaʿamei ha-Miqra"],
                            },
                            ", §11.3 (pp. 264–265):",
                        ],
                    },
                    " “A special\naccentuation applies before a ",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["לגרמיה"],
                    },
                    " [legarmeh] operating\nwithin the domain of a ",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["פזר"],
                    },
                    " [pazer]: a secondary merkha is\n"
                    "placed at the head of the word before the legarmeh — on condition "
                    "that there\n"
                    "is a separation between the merkha and the vowel that ought to be "
                    "stressed. The\n"
                    "secondary merkha comes with no primary accent, and a ga’ya takes the "
                    "place\n"
                    "of the [primary] accent” (compare the example below at 19:15). The "
                    "accents\n"
                    "appear this way in Breuer and in ",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["מג״ה"],
                    },
                    " (Miqra’ot\nGedolot Ha-Keter), but they omit the maqqef.",
                ],
            },
            "\n\n",
            {
                "_htel_tag": "li",
                "contents": [
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["ל"],
                    },
                    " (Leningrad) =\n",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["‹מִֽמְתִ֥ים־יָדְךָ֨\u202f׀›"],
                    },
                    " (ga’ya, merkha, and\nmaqqef, with no ḥataf) according to ",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["המקליד"],
                    },
                    " (the\ntranscriber) — and likewise in ",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["קורן"],
                    },
                    " (Koren), which\nomits the maqqef — or ",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["‹מִֽמְתִֽים־יָדְךָ֨\u202f׀›"],
                    },
                    "\n(both being ga’yas) according to ",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["דותן"],
                    },
                    " (Dotan) (and\n"
                    "this seems the more likely reading in the Leningrad manuscript "
                    "itself,\n",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["כתי״ל"],
                    },
                    ").",
                ],
            },
            "\n\n",
            {
                "_htel_tag": "li",
                "contents": [
                    "Breuer; Miqra’ot Gedolot Ha-Keter; Simanim; Mechon Mamre."
                ],
            },
            "\n",
        ],
    },
    "\n\n",
    {
        "_htel_tag": "h2",
        "contents": [
            "Note 2 — on ",
            {
                "_htel_tag": "span",
                "attr": {"class": "lemma", "lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["מִֽמְתִ֬ים"],
            },
        ],
    },
    "\n\n",
    {
        "_htel_tag": "p",
        "contents": [
            {"_htel_tag": "strong", "lb1": "", "lb2": "", "contents": ["MAM = "]},
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["ל, ש1, גסטר1"],
            },
            ".",
        ],
    },
    "\n\n",
    {
        "_htel_tag": "ul",
        "contents": [
            "\n",
            {
                "_htel_tag": "li",
                "contents": [
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["ק13"],
                    },
                    ", ",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["פטרבורג-EVR-II-B-55"],
                    },
                    "\n(St. Petersburg EVR-II-B-55), and the practice of Aleppo\n(",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["שיטת-א"],
                    },
                    ") = ",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["מִֽמֲתִ֬ים"],
                    },
                    " (with a\n",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["חטף"],
                    },
                    " [ḥataf]), and so too in ",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["מג״ה"],
                    },
                    ".",
                ],
            },
            "\n",
        ],
    },
    "\n\n",
    {
        "_htel_tag": "h2",
        "contents": [
            "Note 3 — on ",
            {
                "_htel_tag": "span",
                "attr": {"class": "lemma", "lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["יִשְׂבְּע֥וּ"],
            },
        ],
    },
    "\n\n",
    {
        "_htel_tag": "p",
        "contents": [
            {"_htel_tag": "strong", "lb1": "", "lb2": "", "contents": ["MAM = "]},
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["ש1, ק13, גסטר1"],
            },
            " and the printed\neditions (",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["דפוסים"],
            },
            ").",
        ],
    },
    "\n\n",
    {
        "_htel_tag": "ul",
        "contents": [
            "\n",
            {
                "_htel_tag": "li",
                "contents": [
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["ל"],
                    },
                    " (Leningrad) reads\n",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["יִשְׂבּ֥עוּ"],
                    },
                    " (missing the ",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["שווא"],
                    },
                    "\n[shva] under the letter ",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["בי״ת"],
                    },
                    " [bet]), but\n",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["המקליד"],
                    },
                    " (the transcriber) corrected it without noting the\ncorrection.",
                ],
            },
            "\n",
            {"_htel_tag": "li", "contents": ["The notes of Dotan and Breuer."]},
            "\n",
        ],
    },
    "\n\n",
    {
        "_htel_tag": "h2",
        "contents": [
            "Note 4 — on ",
            {
                "_htel_tag": "span",
                "attr": {"class": "lemma", "lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["לְעוֹלְלֵיהֶֽם"],
            },
        ],
    },
    "\n\n",
    {
        "_htel_tag": "p",
        "contents": [
            {"_htel_tag": "strong", "lb1": "", "lb2": "", "contents": ["MAM = "]},
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["ש1"],
            },
            "(?),\n",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["ק-מ"],
            },
            " (Cambridge Add. 1753) — the placement of the\n",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["סילוק"],
            },
            " [silluq].",
        ],
    },
    "\n\n",
    {
        "_htel_tag": "ul",
        "contents": [
            "\n",
            {
                "_htel_tag": "li",
                "contents": [
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["גסטר1"],
                    },
                    " reads ",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["לְעֽוֹלְלֵיהֶֽם"],
                    },
                    "\n(with a ga’ya and a silluq).",
                ],
            },
            "\n",
            {
                "_htel_tag": "li",
                "contents": [
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["ל"],
                    },
                    " (Leningrad) reads\n",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["לְעוֹלְלֵֽיהֶם"],
                    },
                    " (the placement of the silluq), but\n",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["המקליד"],
                    },
                    " (the transcriber) marked the right-side silluq\n"
                    "specifically on the letter ",
                    {
                        "_htel_tag": "span",
                        "attr": {"lang": "hbo"},
                        "lb1": "",
                        "lb2": "",
                        "contents": ["ה״א"],
                    },
                    " [he] (!).",
                ],
            },
            "\n",
            {"_htel_tag": "li", "contents": ["The notes of Breuer and Dotan."]},
            "\n",
        ],
    },
    "\n\n",
]
