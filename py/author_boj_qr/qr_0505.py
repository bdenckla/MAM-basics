from author_boj_util.golinets import golinets_citation
import author_boj_util.author as author

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
