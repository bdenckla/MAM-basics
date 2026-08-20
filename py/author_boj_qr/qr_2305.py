from author_boj_util import author

_COM_PART_1 = [
    "As is often the case, there is some question as to",
    " whether μA has מרכא or געיה, because either are valid in this context.",
    #
    " I have shown μA with געיה because that is what $DM does and I am primarily reporting $DM here.",
]
_COM_PART_2 = [
    "In an appendix, the כתר ירושלים (Jerusalem Crown) edition disagrees,",
    " giving μA a מרכא.",
    #
    " This may mean that Breuer changed his mind on this issue over the years."
    #
    " As usual with the כתר ירושלים,",
    " it is not clear whether this מרכא reading in the appendix is",
    " directly from Breuer or from Ofer.",
]
RECORD_2305 = {
    "qr-noted-by-mam": True,
    "qr-noted-by": "aDM",
    "qr-cv": "23:5",
    "qr-ac-proposed": "מַה־יֹּֽאמַר־לִֽי׃",
    "qr-consensus": "מַה־יֹּ֥אמַר לִֽי׃",
    "qr-ac-loc": {"page": "276r", "column": 1, "line": 25, "word": 5},
    "qr-what-is-weird": "געיה-מקף not מרכא",
    "qr-highlight-ac-proposed": 8,
    "qr-generic-comment": [
        author.para(_COM_PART_1),
        author.para(_COM_PART_2),
    ],
    "qr-bhq-comment": [
        "$BHQ transcribes μL as in the consensus shown above,",
        " i.e. with %יאמר having a מרכא and no מקף.",
        #
        " Note that a מרכא only exists in μL if we charitably assume",
        " that it is attached to the bottom of the $yod.",
        #
        " A less charitable transcription would not have this מרכא.",
        #
        " Instead, it would interpret those ink (remains) as a long $yod",
        " or perhaps even a $vav.",
    ],
    "qr-lc-loc": {"page": "403B", "column": 2, "line": 11},
}
