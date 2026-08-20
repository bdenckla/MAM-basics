from author_boj_util.job_common import RECORD_1804_CMN_AB

_BHQ_COMMENT_1804_A = [
    "$BHQ silently ignores the possible שווא part of the possible חטף פתח.",
    " It also silently ignores the possible interpretation of that ink as a געיה.",
    " I.e. other than the prepositive דחי accent,",
    " $BHQ supplies only the (full) פתח that is the consensus expectation here.",
    " $BHQ does so silently, i.e. with no note about the pointing of ה.",
]
RECORD_1804_HLM3N5_1_of_2_FTW = {
    **RECORD_1804_CMN_AB,
    "qr-word-id": "HLM3N5_1_of_2_FTW",
    "qr-intermediate": "הַֽ֭לְמַּעַנְךָ",
    "qr-n_of_m_for_this_word": (1, 2),  # this is record 1 of 2 for this word
    "qr-what-is-weird": "פתח on ה is חטף",
    "qr-generic-comment": [
        "The quirk that מ has דגש is discussed in a separate entry of mine.",
    ],
    "qr-ignore-g3yh-diff": True,
    "qr-highlight": 1,
    "qr-bhq-comment": _BHQ_COMMENT_1804_A,
    "qr-noted-by": "nBHL-nDM",
    "qr-ac-loc": {"page": "274v", "column": 2, "line": 3, "word": 4},
}
