from author_boj_util.job_common import correctly_ignores

RECORD_1703 = {
    "qr-noted-by": "nDM",
    "qr-cv": "17:3",
    "qr-consensus": "עׇרְבֵ֣נִי",
    "qr-lc-proposed": "עַרְבֵ֣נִי",
    "qr-what-is-weird": "פתח not קמץ (קטן)",
    "qr-highlight": 1,
    "qr-generic-comment": [
        "This case is the opposite of $link_3_4, except there the קמץ is not קטן."
        " Some very faint remains of what might have been a “קמץ dot” can perhaps be seen",
        " under the horizontal line that is transcribed as a פתח.",
    ],
    "qr-lc-loc": {"page": "402A", "column": 1, "line": 4},
    "qr-ac-loc": {"page": "274v", "column": 1, "line": 14, "word": 3},
}

_UXLC_NEEDS_FIX = [
    "$UXLC should do one of the following.",
    "(1) Remove the דגש from מ and note the uncertainty in transcription.",
    "(2) Leave the דגש and note the divergence from consensus as well as",
    " the uncertainty in transcription.",
]

RECORD_1704 = {
    "qr-cv": "17:4",
    "qr-lc-proposed": "מִּשָּׂ֑כֶל",
    "qr-lc-q": "(?)",
    "qr-what-is-weird": "מ has דגש",
    "qr-consensus": "מִשָּׂ֑כֶל",
    "qr-generic-comment": [
        "The color image of μL reveals this דגש to be unlikely.",
        " Surprisingly, $BHL includes this דגש in its body text",
        " rather than noting it in $BHL_A.",
        " In μY, the center of the מ in question is such a blur",
        " that it is impossible to say whether a דגש is there or not.",
    ],
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "402A", "column": 1, "line": 5},
    "qr-ac-loc": {"page": "274v", "column": 1, "line": 15, "word": 4},
    "qr-bhq-comment": correctly_ignores("דגש", "17:4"),
    "qr-noted-by": "nWLC",
    "qr-uxlc-needs-fix": _UXLC_NEEDS_FIX,
    # This is a bracket-p note in WLC.
    # We take it to note a quirk because MAM reveals that WLC is diverging from consensus here.
    # (Normally we only take WLC to note a quirk in the case of bracket-1 notes.)
}

RECORD_1706 = {
    "qr-cv": "17:6",
    "qr-lc-proposed": "וְתֹ֖פֶתּ",
    "qr-what-is-weird": "final ת has דגש",
    "qr-consensus": "וְתֹ֖פֶת",
    "qr-generic-comment": [
        "A דגש in a final ת doesn’t make sense",
        " without a קמץ or a שווא נח below.",
        " But the dot is convincing.",
    ],
    "qr-highlight": 4,
    "qr-lc-loc": {"page": "402A", "column": 1, "line": 7},
    "qr-ac-loc": {"page": "274v", "column": 1, "line": 17, "word": 4},
    "qr-noted-by": "nBHQ",
    "qr-uxlc-needs-fix": True,
}

RECORD_1711 = {
    "qr-cv": "17:11",
    "qr-lc-proposed": "לְבָבִּֽי׃",
    "qr-what-is-weird": "second ב has דגש",
    "qr-consensus": "לְבָבִֽי׃",
    "qr-highlight": 3,
    "qr-lc-loc": {"page": "402A", "column": 1, "line": 13},
    "qr-ac-loc": {"page": "274v", "column": 1, "line": 22, "word": 8},
    "qr-noted-by": "nBHQ",
    "qr-uxlc-needs-fix": True,
}
