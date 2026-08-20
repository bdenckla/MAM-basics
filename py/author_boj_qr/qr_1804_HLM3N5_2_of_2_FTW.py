from author_boj_util.all_verses_but_this import reiteration_new_in_bhq
from author_boj_util.job_common import RECORD_1804_CMN_AB

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
