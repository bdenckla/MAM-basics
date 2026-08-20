from author_boj_util import author
from author_boj_util.job_common import core_ignores

_COM1 = [
    "The possible דגש looks slightly different",
    " than the four nearby dots in the two צירה vowels."
    #
    " This raises the possibility that it is not ink, e.g. a speck on the vellum.",
]
_COM2 = [
    "Note that almost by necessity, if we transcribe the $yod as having a דגש,",
    " then the פתח must be “pulled back” from being a furtive פתח",
    " to being a normal פתח that belongs to the $yod.",
    #
    " This is because, unlike most additions of דגש,",
    " here adding a דגש transforms the letter from being silent (an אם קריאה)",
    " to being (implicitly) doubled (geminated)!",
    #
    " If we give the $yod a דגש but do not pull back the פתח to the $yod,",
    " we are proposing a pointing that goes beyond surprising to nonsensical."
    " To do so would be unreasonably uncharitable.",
]
_COM3 = [
    "Although the position of the פתח (between $yod and ח)"
    " may seem to support the idea that the פתח belongs to the $yod,",
    " this is actually a common position for a furtive פתח.",
    #
    " See, for example, the image we provide of %אלוה in $link_4_9 and $link_11_6."
    #
    " So, the position of the פתח",
    " is actually more consistent with the פתח belonging to the ח."
    #
    " (Or, if you prefer to think of furtive פתח in a different way,",
    " it belongs to the ר (being the second of two vowels belonging to the ר.)",
]
RECORD_1409 = {
    "qr-cv": "14:9",
    "qr-lc-proposed": "מֵרֵ֣יַּח",
    "qr-what-is-weird": "$yod has דגש and pulls back פתח",
    "qr-consensus": "מֵרֵ֣יחַ",
    "qr-highlight": 3,
    "qr-lc-loc": {"page": "401A", "column": 1, "line": -9},
    "qr-ac-loc": {"page": "273v", "column": 2, "line": 11, "word": 4},
    "qr-generic-comment": [
        author.para(_COM1),
        author.para(_COM2),
        author.para(_COM3),
    ],
    "qr-bhq-comment": [
        "$BHQ silently ignores the possible דגש.",
        [" ", *core_ignores(" (or anywhere)")],
    ],
    "qr-noted-by": "nBHL",
}
