from author_boj_util.job_common import (
    RECORD_1804_CMN_AB,
    BHQ_COMMENT_XELSEWHERE_DUBIOUS,
)
from author_boj_util.all_verses_but_this import reiteration_new_in_bhq

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

_BHQ_COMMENT_1804_B = [
    "$BHQ notes that the דגש on the מ in μL disagrees with μA and μY.",
    " $BHQ misses the געיה in μA.",
    " This געיה is irrelevant to $BHQ’s point here, which is about the דגש.",
    " Still, it would have been nice if $BHQ had transcribed μA’s געיה.",
    " ",
    reiteration_new_in_bhq("18:4"),
]
RECORD_1804_HLM3N5_2_of_2_FTW = {
    **RECORD_1804_CMN_AB,
    "qr-word-id": "HLM3N5_2_of_2_FTW",
    "qr-intermediate": "הֲ֭לְמַעַנְךָ",
    "qr-n_of_m_for_this_word": (2, 2),  # this is record 2 of 2 for this word
    "qr-what-is-weird": "מ has דגש",
    "qr-generic-comment": [
        "The quirk that the פתח on ה",
        " is חטף is discussed in a separate entry of mine.",
    ],
    "qr-ignore-g3yh-diff-in-consensus": True,
    "qr-highlight": 3,
    "qr-bhq-comment": _BHQ_COMMENT_1804_B,
    "qr-noted-by": "nBHQ-nBHL-nDM",
    "qr-ac-loc": {"page": "274v", "column": 2, "line": 3, "word": 4},
}

_BHQ_COMMENT = [
    "$BHQ positions the mark ambiguously.",
    " The mark is a little to the right of center.",
    " So it is not centered, as one would expect a טרחא to be,",
    " but neither is it as far to the right as דחי normally is in $BHQ.",
]
RECORD_1806 = {
    "qr-cv": "18:6",
    "qr-lc-proposed": "א֖וֹר",
    "qr-what-is-weird": "טרחא not דחי",
    "qr-consensus": "א֭וֹר",
    "qr-generic-comment": "The scribe of μL probably intended a דחי but placed it like a טרחא.",
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "402A", "column": 1, "line": -2},
    "qr-ac-loc": {"page": "274v", "column": 2, "line": 5, "word": 6},
    "qr-bhq-comment": _BHQ_COMMENT,
    "qr-noted-by": "tBHQ-nBHL",
}

RECORD_1809 = {
    "qr-cv": "18:9",
    "qr-lc-proposed": "בְּעָּקֵ֣ב",
    "qr-lc-q": "(?)",
    "qr-what-is-weird": "ע has דגש",
    "qr-consensus": "בְּעָקֵ֣ב",
    "qr-generic-comment": [
        "A דגש in a ע doesn’t make sense.",
        " But the dot is convincing,",
        " despite being a little close to the right arm of the ע.",
    ],
    "qr-highlight": 2,
    "qr-lc-loc": {"page": "402A", "column": 2, "line": 2},
    "qr-ac-loc": {"page": "274v", "column": 2, "line": 8, "word": 5},
    "qr-bhq-comment": BHQ_COMMENT_XELSEWHERE_DUBIOUS,
    "qr-noted-by": "nBHQ",
    "qr-uxlc-needs-fix": True,
}
