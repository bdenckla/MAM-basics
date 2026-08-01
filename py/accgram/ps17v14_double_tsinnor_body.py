"""htel element body migrated byte-exactly from the former hand-authored gh-
pages/accgram/ps17v14-double-tsinnor.html. Consumed by
accgram/ps17v14_double_tsinnor.py; edit the generator/this data, not the generated HTML.

Migrated from the former hand-authored JSON sidecar ps17v14_double_tsinnor_body.json (issue #33):
read via import, not a file open.  Edit this module / the generator, not the
generated HTML.

The BYTE-EXACTNESS above is a claim about THIS DATA, not about the page any more.  The
htels here are literal dicts that pin lb1/lb2 on inline tags only, so
h1/p/blockquote/figure/figcaption/img used to take the serializer's old lb1="\\n" default;
since the move to tag-keyed break tables in ``py_html/wlc_utils_html.py`` they take
lb1="", and the page no longer carries a newline straight after those block-level open
tags.  No browser renders the difference, and it is what makes this page break like the
other 151.  See that module's table comment.
"""

TITLE = "Psalms 17:14 — the double tsinnor"

BODY = [
    "\n\n",
    {"_htel_tag": "h1", "contents": ["Psalms 17:14 — the double tsinnor"]},
    "\n\n",
    {
        "_htel_tag": "p",
        "attr": {"class": "lead"},
        "contents": [
            "Psalms 17:14 carries a feature unique in the Three Books: two\n",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["צנור"],
            },
            " (tsinnor) marks in a row. This page records what is\n"
            "known about that doubled mark — its uniqueness, the manuscript evidence, the MAM\n"
            "documentation notes, and Breuer's analysis — and explains how the accent-grammar\n"
            "checker treats it. The material formerly appeared in the Psalms 17:14 section of\n"
            "the ",
            {
                "_htel_tag": "a",
                "attr": {"href": "poetic.html"},
                "lb1": "",
                "lb2": "",
                "contents": ["poetic ungrammatical-verse report"],
            },
            "; once the checker began\n"
            "accepting the verse (see below) that section disappeared, so the discussion is\n"
            "preserved here.",
        ],
    },
    "\n\n",
    {"_htel_tag": "h2", "contents": ["The doubled mark and its uniqueness"]},
    "\n\n",
    {
        "_htel_tag": "p",
        "contents": [
            "A scan of the disjunctive accent stream of every poetic verse finds that these\n"
            "two adjacent tsinnor marks are unique in the Three Books: of the 250 poetic "
            "verses\n"
            "carrying at least one tsinnor, Psalms 17:14 is the only one in which two tsinnor\n"
            "occur consecutively. Both arise from genuine Michigan-Claremont ",
            {"_htel_tag": "code", "lb1": "", "lb2": "", "contents": ["02"]},
            "\n(tsinnor) codes — not a swallowed ",
            {"_htel_tag": "code", "lb1": "", "lb2": "", "contents": ["82"]},
            " (tsinnorit) — on adjacent chanted words:\n",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["בַּחַיִּים"],
            },
            " and the qere ",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["וּצְפוּנְךָ"],
            },
            ".",
        ],
    },
    "\n\n",
    {"_htel_tag": "h2", "contents": ["Manuscript evidence"]},
    "\n\n",
    {"_htel_tag": "p", "contents": ["This verse is not extant in the Aleppo Codex."]},
    "\n\n",
    {
        "_htel_tag": "p",
        "contents": [
            "Though in the Leningrad Codex (L) the first of the two tsinnor marks is a little\n"
            "oddly shaped, S1 (Sassoon 1053) clearly shares these two adjacent tsinnor marks,\n"
            "with no questions of penmanship."
        ],
    },
    "\n\n",
    {
        "_htel_tag": "figure",
        "contents": [
            "\n  ",
            {
                "_htel_tag": "img",
                "attr": {
                    "src": "img/LC-Ps-17v14.png",
                    "alt": "Leningrad Codex, Psalms 17:14",
                },
                "noclose": True,
            },
            "\n  ",
            {"_htel_tag": "figcaption", "contents": ["Leningrad Codex"]},
            "\n",
        ],
    },
    "\n\n",
    {
        "_htel_tag": "figure",
        "contents": [
            "\n  ",
            {
                "_htel_tag": "img",
                "attr": {
                    "src": "img/S1-Ps-17v14.png",
                    "alt": "Sassoon 1053 (S1), Psalms 17:14",
                },
                "noclose": True,
            },
            "\n  ",
            {"_htel_tag": "figcaption", "contents": ["Sassoon 1053 (S1)"]},
            "\n",
        ],
    },
    "\n\n",
    {"_htel_tag": "h2", "contents": ["How the checker treats it"]},
    "\n\n",
    {
        "_htel_tag": "p",
        "contents": [
            "The checker's underlying grammar still cannot parse this sequence directly, and\n"
            "never could: a repeated tsinnor standing before an oleh-weyored that itself "
            "carries\n"
            "a servus is beyond its LALR(1) power (the servus is ambiguous between the second\n"
            "tsinnor and the oleh). That limitation has not changed. What changed is that the\n"
            "verse used to be reported as ",
            {"_htel_tag": "code", "lb1": "", "lb2": "", "contents": ["NO_PARSE"]},
            " and no longer is.",
        ],
    },
    "\n\n",
    {
        "_htel_tag": "p",
        "contents": [
            "The checker now ",
            {"_htel_tag": "em", "lb1": "", "lb2": "", "contents": ["accepts"]},
            " the verse, on a principled basis: a repeated\n"
            "disjunctive is the same divider written twice — Yeivin notes that the zarqa (the\n"
            "prose counterpart of the tsinnor) may be repeated, and Breuer says the same of "
            "the\n"
            "doubled tsinnor — so for grammaticality a repeated divider counts once. Rather "
            "than\n"
            "extend the grammar, the checker adds a step ahead of it: before parsing, it\n"
            "collapses the run of two tsinnor marks to one, and the grammar then parses what\n"
            "remains. The verse's recorded accents — both tsinnor marks — are left untouched, "
            "so\n"
            "the WLC-vs-MAM comparison still sees the doubled mark.",
        ],
    },
    "\n\n",
    {"_htel_tag": "h2", "contents": ["MAM's documentation notes"]},
    "\n\n",
    {
        "_htel_tag": "p",
        "contents": [
            "This verse is heavily commented upon by MAM (see the\n",
            {
                "_htel_tag": "a",
                "attr": {"href": "ps17v14-mam-doc-notes.html"},
                "lb1": "",
                "lb2": "",
                "contents": ["translation of those notes"],
            },
            "), but the\n"
            "comments either do not concern cantillation, or concern cantillation only in ways\n"
            "that would not change the accent-grammar issue. The four notes turn on a "
            "secondary\n"
            "merkha plus ga’ya, a ",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["חטף"],
            },
            " [ḥataf], a missing shva, and\n"
            "the placement of the silluq — none of which alters the disjunctive skeleton, and\n"
            "the conjunctive servus chain the grammar parses is permissive enough that a\n"
            "secondary conjunctive is absorbed harmlessly.",
        ],
    },
    "\n\n",
    {"_htel_tag": "h2", "contents": ["Breuer's analysis"]},
    "\n\n",
    {
        "_htel_tag": "p",
        "contents": [
            "Breuer treats the doubled tsinnor in two places. In ",
            {
                "_htel_tag": "em",
                "lb1": "",
                "lb2": "",
                "contents": ["The Cantillation of\nScripture"],
            },
            ", Ch. 11 (footnote 11, attached to the Psalms 17:14 example\n",
            {
                "_htel_tag": "span",
                "attr": {"lang": "hbo"},
                "lb1": "",
                "lb2": "",
                "contents": ["חֶלְקָם בַּחַיִּים"],
            },
            "), he calls this\n",
            {
                "_htel_tag": "strong",
                "lb1": "",
                "lb2": "",
                "contents": ["“the sole example of two consecutive\n[tsinnor] marks”"],
            },
            " in Scripture. Following Wickes (p. 81 n. 4), he holds\n"
            "that the servant's exceptional cantillation results from the exceptional "
            "(doubled)\n",
            {"_htel_tag": "em", "lb1": "", "lb2": "", "contents": ["mafsik"]},
            ", and he notes a parallel in the Twenty-One Books (Ch. 3 §16 III):\n"
            "there too the servant of the zarqa changes where there are two consecutive zarqa\n"
            "marks.",
        ],
    },
    "\n\n",
    {
        "_htel_tag": "p",
        "contents": [
            "His structural account is in Ch. 10 §9, on the subdividers of the oleh-weyored\n"
            "domain. (Breuer's English translation calls such a subdivider a\n"
            "“viceroy”; its default form is the big revia’ / revia gadol.)\n"
            "Psalms 17:14 is one of very few verses with ",
            {"_htel_tag": "em", "lb1": "", "lb2": "", "contents": ["three"]},
            " such subdividers in the\n"
            "oleh-weyored realm, and its cantillation, he says, is exceptional:",
        ],
    },
    "\n\n",
    {
        "_htel_tag": "blockquote",
        "contents": [
            "“In example II [Psalms 17:14], the final viceroy is [tsinnor],\n"
            "because it is not next to the oleh [weyored]. The penultimate viceroy is "
            "[tsinnor]\n"
            "preceded by a big revia’; but we would expect both these viceroys to be big\n"
            "revia’ marks.”"
        ],
    },
    "\n\n",
    {
        "_htel_tag": "p",
        "contents": [
            "That is: where the rule would place a pair of big revia’ subdividers before\n"
            "the oleh-weyored, Psalms 17:14 substitutes a ",
            {"_htel_tag": "em", "lb1": "", "lb2": "", "contents": ["tsinnor"]},
            " for each — and that\n"
            "substitution, applied to two adjacent subdividers at once, is precisely what "
            "yields\n"
            "the unique run of two consecutive tsinnor marks. It is the same divider (the "
            "tsinnor)\n"
            "appearing twice, which is exactly why the accent-grammar checker can accept the\n"
            "sequence by counting the repeated divider once (above).",
        ],
    },
    "\n\n",
    {
        "_htel_tag": "p",
        "attr": {"class": "src"},
        "contents": [
            "Source: M. Breuer, ",
            {
                "_htel_tag": "em",
                "lb1": "",
                "lb2": "",
                "contents": ["The Cantillation of Scripture"],
            },
            ", Ch. 10 §9\n"
            "and Ch. 11 n. 11 (with Wickes p. 81 n. 4). The Hebrew of the scanned examples is "
            "not\n"
            "reproduced here, as the OCR of the pointed text is unreliable.",
        ],
    },
    "\n\n",
]
