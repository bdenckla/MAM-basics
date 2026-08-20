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
