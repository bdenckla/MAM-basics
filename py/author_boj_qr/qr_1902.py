from author_boj_util import author
from author_boj_util.uxlc_change import uxlc_change

_GENCOM_PARA_1 = [
    "As $UXLC notes, an erasure under the כ is apparent.",
]
_GENCOM_PARA_2 = [
    "The שווא in question is present in μY.",
    " Relatedly, and importantly, μY has no רפה above its א.",
    " (The ink roughly between the כ and the א is the pair of above-dots",
    " that is μY’s equivalent of a masorah circle.)",
    " Thus, though μY presents a different word than the μL/μA word,",
    " it is still a valid word,",
    " i.e. the word makes sense according to the syllabic grammar of Biblical Hebrew.",
]
_GENCOM_PARA_3 = [
    "In contrast, transcription in $BHQ results in a word that does not make sense,",
    " if it were supplemented with the רפה that is clearly present in μL.",
    " This is one of several cases we’ve seen where רפה,",
    " though generally safe to ignore (and discard),",
    " is not always safe to ignore (and discard).",
    " See also $link_31_7.",
]
RECORD_1902 = {
    "qr-cv": "19:2",
    "qr-lc-proposed": "וּֽתְדַכְּאוּנַ֥נִי",
    "qr-what-is-weird": "כ has שווא",
    "qr-consensus": "וּֽתְדַכּאוּנַ֥נִי",
    "qr-generic-comment": [
        author.para(_GENCOM_PARA_1),
        author.para(_GENCOM_PARA_2),
        author.para(_GENCOM_PARA_3),
    ],
    "qr-highlight": 4,
    "qr-lc-loc": {"page": "402A", "column": 2, "line": 19},
    "qr-ac-loc": {"page": "274v", "column": 2, "line": 24, "word": 5},
    "qr-noted-by": "tBHQ-zUXLC",
    "qr-uxlc-change-url": uxlc_change("2023.10.19", "2023.06.10-19"),
}
