from author_boj_util.author import yyy_dash_nothing
from author_boj_util import author

_GENCOM_PARA_2 = [
    "The two dots above the מ in the μY image are",
    " the pair of above-dots that is μY’s equivalent of a masorah circle.",
    " See $link_19_16_BMV0PY for another example of this two-dot callout notation.",
]
_BHQCOM_PART_1 = [
    "$BHQ reflects neither μL nor the consensus expectation here.",
    " It reflects μL except it places the סילוק under the א instead of the $vav.",
    #
    " This not only contradicts μL,",
    " but also makes no sense given the רפה on the א.",
    #
    " (Admittedly, the actual location in μL, under the $vav, doesn’t make any sense either.)",
    #
]
_BHQCOM_PART_2 = [
    "I would also argue that this particular רפה should have been shown,",
    " despite the general policy of $BHQ to ignore רפה marks in μL.",
    " In such a confusing word, the reader needs all the detail and context possible,",
    " such as this רפה mark.",
    " See also $link_19_2 for another case where רפה is important.",
]
_BHQCOM_PART_3 = [
    "$BHQ notes that here μL disagrees with μA and μY.",
    #
    " But $BHQ gives the מ in μA and μY a מרכא rather than a סילוק,",
    " which seems more likely a typo than a deliberate choice.",
]
RECORD_3107 = {
    "qr-cv": "31:7",
    "qr-lc-proposed": "מֻאֿוּֽם׃",
    "qr-what-is-weird": ["קובוץ-סילוק not ", yyy_dash_nothing("סילוק")],
    "qr-consensus": "מֽאֿוּם׃",
    "qr-highlight": [1, 3],
    "qr-lc-loc": {"page": "405B", "column": 1, "line": -6, "including-blank-lines": 1},
    "qr-ac-loc": {"page": "278r", "column": 1, "line": 2, "word": 5},
    "qr-generic-comment": [
        "The consensus has סילוק under מ and nothing (אפס (zero)) under $vav.",
        author.para(_GENCOM_PARA_2),
    ],
    "qr-bhq-comment": [
        author.para(_BHQCOM_PART_1),
        author.para(_BHQCOM_PART_2),
        author.para(_BHQCOM_PART_3),
    ],
    "qr-bhq": "מֻאֽוּם׃",
    "qr-noted-by": "nBHL-nDM-nWLC",
    # Above we consider this xBHQ because:
    #    Though it attempts to transcribe the quirk, it does so inaccurately.
    #    Though it notes the quirk, it does so inaccurately.
}
