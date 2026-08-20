from author_boj_util.job_common import correctly_ignores

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
