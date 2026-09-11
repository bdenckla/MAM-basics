from author_boj_util.golinets import golinets_citation
import author_boj_util.author as author
from author_boj_util.thin_spaced_paren import wrap_with_thin_spaced_paren

_COMPAR1 = [
    "There is little or no evidence of a דגש in the צ in μL.",
    " The consensus has this דגש.",
]
_COMPAR2 = [
    "It is said (from direct inspection of μL in Russia) that there is",
    " “a pale yellow dot in the [צ]",
    " which could be the trace of a worn-off [דגש]”",
    [" in ", golinets_citation("242")],
]
_COMPAR3 = [
    "This is interesting to know, since this pale yellow dot is not visible in the color image.",
    " All that is present in the color image is a slight smudge between the צ and the נ.",
    " This smudge closely resembles other nearby smudges.",
]
_COMPAR4 = [
    "Though interesting, this report of a pale yellow dot still falls well under the “little”",
    " of my assessment that there is little or no evidence of a דגש here.",
]

RECORD_0505 = {
    "qr-cv": "5:5",
    "qr-lc-proposed": "מִצִנִּ֥ים",
    "qr-what-is-weird": "צ lacks דגש",
    "qr-consensus": "מִצִּנִּ֥ים",
    "qr-highlight": 2,
    "qr-generic-comment": [
        author.para(_COMPAR1),
        author.para(_COMPAR2),
        author.para(_COMPAR3),
        author.para(_COMPAR4),
    ],
    "qr-lc-loc": {"page": "398A", "column": 2, "line": 22},
    "qr-ac-loc": {"page": "271r", "column": 2, "line": 23, "word": 2},
    "qr-bhq-comment": [
        "As is often the case, here $BHQ has the consensus",
        " rather than the best guess as to the actual contents of μL.",
    ],
    "qr-noted-by": "nDM",
}

RECORD_0520 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "5:20",
    "qr-consensus": "בְּֽ֭רָעָב",
    "qr-lc-proposed": "בְּ֭רָעָב",
    "qr-what-is-weird": "ב lacks געיה",
    "qr-highlight": 1,
    "qr-generic-comment": "Note that μY, like μL, lacks the געיה in question.",
    "qr-lc-loc": {"page": "398B", "column": 1, "line": 13},
    "qr-ac-loc": {"page": "271v", "column": 1, "line": 12, "word": 6},
}

RECORD_0523 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "5:23",
    "qr-consensus": "הׇשְׁלְמָה־לָּֽךְ׃",
    "qr-lc-proposed": "הׇשְׁלְמָה־לָֽךְ׃",
    "qr-lc-q": "(?)",
    "qr-what-is-weird": "ל lacks דגש",
    "qr-highlight": 7,
    "qr-generic-comment": [
        "There is some kind of a dot way over next to the",
        " final $khaf " + wrap_with_thin_spaced_paren("ך"),
        " but it could easily be either not ink, or not intentional ink.",
        " Aside: the קמץ under ה is קטן.",
    ],
    "qr-lc-loc": {"page": "398B", "column": 1, "line": 17, "line2": 18},
    "qr-ac-loc": {"page": "271v", "column": 1, "line": 17, "word": 1},
}

RECORD_0524 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "5:24",
    "qr-consensus": "נָ֝וְךָ֗",
    "qr-lc-proposed": "נָ֝וְךָ",
    "qr-what-is-weird": "רביע of רביע מוגרש is absent",
    "qr-highlight": 3,
    "qr-generic-comment": [
        "The dot above the",
        " final $khaf " + wrap_with_thin_spaced_paren("ך"),
        " might at first glance appear to be a candidate",
        " for the possibly-expected רביע, but it is almost certainly",
        " the קמץ dot belonging to the word-part %השלמה־ above,",
        " which, coincidentally, is part of our entry for $link_5_23.",
    ],
    "qr-lc-loc": {"page": "398B", "column": 1, "line": 19},
    "qr-ac-loc": {"page": "271v", "column": 1, "line": 18, "word": 2},
}
