from author_boj_util import author

_COMMENT = [
    "The mark in question is very heavy,",
    " having a stroke width more typical of a letter-stroke than of a niqqud-stroke.",
    " Its clarity suggests it is part of the re-inking.",
    " Indeed perhaps it is only part of the re-inking,",
    " i.e. perhaps it reflects no mark (or only a much smaller mark) in the original.",
    " The mark in question may be two marks,",
    " a רביע (expected) overlaid with a גרש (unexpected).",
    " Or, it may be only a single mark whose lower end is, for some reason, a blob.",
]
_BHQ_COMMENT = [
    "$BHQ silently supplies the רביע that is the consensus expectation.",
    " It may be interesting to note that $BHS had the רביע on ד.",
    " Like all changes in $BHQ, this change had to be discovered, since",
    " changes from 1997 $BHS to $BHQ are undocumented.",
    " It is a painful “exercise left to the reader” to discover such changes."
    " The lack of documentation is a $DBG tradition carried over from $BHS,"
    " which lacks documentation for both",
    " its 1977 to 1984 changes and",
    " its 1984 to 1997 changes.",
]
RECORD_3902 = {
    "qr-cv": "39:2",
    "qr-lc-proposed": "וְ֝יָדַעְתָּ֜",
    "qr-what-is-weird": "גרש not רביע",
    "qr-consensus": "וְ֝יָדַעְתָּ֗",
    "qr-generic-comment": [author.para(_COMMENT)],
    "qr-highlight": 5,
    "qr-lc-loc": {"page": "408A", "column": 2, "line": -3},
    "qr-ac-loc": {"page": "280v", "column": 1, "line": 16, "word": 1},
    "qr-bhq-comment": [author.para(_BHQ_COMMENT)],
    "qr-noted-by": "nBHL",
    # Perhaps I should have been charitable to BHQ and said tBHQ instead of xBHQ,
    # since BHQ’s transcription of רביע is somewhat reasonable if it were accompanied by a note.
    # But it is not accompanied by a note, and without a note, BHQ needs to make weird things in μL
    # look weird. So רביע is not the right transcription for a diplomatic edition having no note
    # in this location.
}

RECORD_3906 = {
    "qr-cv": "39:6",
    "qr-lc-proposed": "מְלֵֽחָה׃",
    "qr-what-is-weird": "סילוק on ל not ח",
    "qr-consensus": "מְלֵחָֽה׃",
    "qr-highlight-lc-proposed": 2,
    "qr-highlight-consensus": 3,
    "qr-lc-loc": {"page": "408B", "column": 1, "line": 3},
    "qr-ac-loc": {"page": "280v", "column": 1, "line": 20, "word": 6},
    "qr-noted-by": "tBHQ-nBHL-nDM",
}

RECORD_3911 = {
    "qr-cv": "39:11",
    "qr-lc-proposed": "בּ֖וֹ",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "בּ֭וֹ",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "408B", "column": 1, "line": 8},
    "qr-ac-loc": {"page": "280v", "column": 1, "line": 26, "word": 2},
    "qr-noted-by": "tBHQ-zdexiWLC",
}

RECORD_3912 = {
    "qr-cv": "39:12",
    "qr-lc-proposed": "בּ֖וֹ",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "בּ֭וֹ",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "408B", "column": 1, "line": 9},
    "qr-ac-loc": {"page": "280v", "column": 1, "line": 27, "word": 2},
    "qr-noted-by": "tBHQ-zdexiWLC",
}

_COMMENT_3913 = [
    "A more charitable interpretation of the image is that the רביע is present",
    " but is merged with the masorah circle.",
    " (It is fairly clear that a masorah circle is present.)",
    " Note that the vertical line above the ר is a סילוק from the line above.",
]
RECORD_3913 = {
    "qr-cv": "39:13",
    "qr-lc-q": "(?)",
    "qr-lc-proposed": "אֶ֝בְרָה",
    "qr-what-is-weird": "רביע of רביע מוגרש is absent",
    "qr-consensus": "אֶ֝בְרָ֗ה",
    "qr-generic-comment": _COMMENT_3913,
    "qr-highlight": 3,
    "qr-lc-loc": {"page": "408B", "column": 1, "line": 11},
    "qr-ac-loc": {"page": "280v", "column": 1, "line": 28, "word": 5},
    "qr-bhq-comment": [
        "$BHQ seems to split the mark(s) in question",
        " into a רביע on ר and a masorah circle on ב.",
        " This is a reasonable (though somewhat charitable)",
        " interpretation of μL,",
        " but as is so often the case, $BHQ should have noted this quirk.",
    ],
    "qr-noted-by": "nBHL",
}

RECORD_3915 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "39:15",
    "qr-consensus": "תְדוּשֶֽׁהָ׃",
    "qr-lc-proposed": "תְּדוּשֶֽׁהָ׃",
    "qr-what-is-weird": "ת has דגש",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "408B", "column": 1, "line": 14},
    "qr-ac-loc": {"page": "280v", "column": 2, "line": 2, "word": 7},
}

RECORD_3920 = {
    "qr-cv": "39:20",
    "qr-lc-proposed": "הְֽ֭תַרְעִישֶׁנּוּ",
    "qr-what-is-weird": "simple שווא not חטף פתח",
    "qr-consensus": "הֲֽ֭תַרְעִישֶׁנּוּ",
    "qr-generic-comment": "The situation with %המימיך in $link_38_12_HMYMY5 is similar.",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "408B", "column": 1, "line": -10},
    "qr-ac-loc": {"page": "280v", "column": 2, "line": 9, "word": 2},
    "qr-noted-by": "tBHQ-nBHL-nDM",
}

RECORD_3925 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "39:25",
    "qr-consensus": "שָׂ֝רִ֗ים",
    "qr-lc-proposed": "שָׂ֝רִים",
    "qr-what-is-weird": "רביע of רביע מוגרש is absent",
    "qr-highlight": 2,
    "qr-bhq-comment": [
        "Aside: $BHQ’s גרש מוקדם is centered over the ש,",
        " as if it were “normal” (prose-system) גרש.",
    ],
    "qr-lc-loc": {"page": "408B", "column": 1, "line": 26},
    "qr-ac-loc": {"page": "280v", "column": 2, "line": 16, "word": 5},
}
