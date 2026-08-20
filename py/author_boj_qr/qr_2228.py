from author_boj_util import author

_BHQ_COMMENT = [
    "$BHQ places the mark a little left of center.",
    #
    " Though this placement is odd,",
    " this makes it clear that a טרחא was intended by $BHQ rather than a דחי.",
    " Thus $BHQ somewhat-accurately transcribes the quirk in μL,",
    " but should have noted the quirk.",
    #
    " Perhaps even better would have been to (charitably) transcribe this as a דחי,",
    " and note the quirk.",
    " But it is not the editorial policy of $BHQ to make such notes:",
    " although $BHQ is full of charitable transcriptions,",
    " as far as I know it never notes its charity.",
]
RECORD_2228 = {
    "qr-cv": "22:28",
    "qr-lc-proposed": "א֖וֹמֶר",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "אֹ֭מֶר",
    "qr-intermediate": "א֭וֹמֶר",
    "qr-generic-comment": [
        "The scribe of μL probably intended a דחי but placed it like a טרחא.",
        " The מלא/חסר spelling difference is not important to us here.",
    ],
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "403B", "column": 2, "line": 2},
    "qr-ac-loc": {"page": "276r", "column": 1, "line": 17, "word": 5},
    "qr-bhq-comment": [author.para(_BHQ_COMMENT)],
    "qr-noted-by": "tBHQ-nBHL",
}
