from author_boj_util import (
    author,
    cos_urls,
)
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

_COMMENT_1413_PARA1 = [
    "I find $WLC’s transcription far-fetched.",
    #
    " Note that the consensus has a rare and hard-to-understand",
    " phenomenon called “secondary מהפך” by Breuer."
    #
    " It may seem weird that in the consensus, געיה",
    " immediately follows the מהפך,",
    " but this is actually expected (or at least “allowed”)",
    " if the מהפך is secondary, as it is here, according to Breuer.",
]
_FOI_H2 = "foi-sec-star-breuer-cos.html#intro-11.66.rn1"
_FOI_H1 = "https://bdenckla.github.io/MAM-basics/MAM-with-doc/foi/"
_FOI_ANC = author.anc_h("here", f"{_FOI_H1}{_FOI_H2}")
_MAM_ANC = author.anc_h("$MAM", "https://purl.org/mam/hebrew-wikisource")
_COMMENT_1413_PARA2 = [
    ["The consensus word ", author.hbo("תָּ֤שִֽׁית"), " may be easier to understand"],
    " if one considers it",
    [" and ", author.hbo("לִ֖י"), " (the next word)"],
    " to form a compound word whose מקף is, somewhat inexplicably, left implicit.",
    " If the מקף were made explicit, the compound would be written as",
    [" ", author.hbo("תָּ֤שִֽׁית־לִ֖י")],
    " and indeed that is the way that word is written (albeit with the מקף colored gray)",
    [" in some editions of ", _MAM_ANC, " (מקרא על פי המסורה)."],
    #
    " This and a handful of analogous cases are listed",
    [" ", _FOI_ANC, ", with the implicit מקף represented as a tilde (~)."],
]
_COS_ENG_ANC = author.anc_h("translation", cos_urls.cos_translation_url())
_COS_HEB_ANC = author.anc_h("original", cos_urls.cos_original_url())
_COMMENT_1413_PARA3 = [
    "See Breuer CoS sections 11.66.rn1 and 11.79.",
    " (CoS = The Cantillation of Scripture; rn = Roman numeral.)",
    [" (Note that an English ", _COS_ENG_ANC, " of CoS is now available,"],
    " a great boon to students of cantillation who cannot easily read",
    [" the ", _COS_HEB_ANC, " in its modern Hebrew.)"],
]
RECORD_1413 = {
    "qr-cv": "14:13",
    "qr-lc-proposed": "תָּ֤שִׁ֥ית",
    "qr-lc-q": "(?)",
    "qr-what-is-weird": "מרכא not געיה",
    "qr-consensus": "תָּ֤שִֽׁית",
    "qr-generic-comment": [
        author.para(_COMMENT_1413_PARA1),
        author.para(_COMMENT_1413_PARA2),
        author.para(_COMMENT_1413_PARA3),
    ],
    "qr-highlight": 2,
    "qr-lc-loc": {"page": "401A", "column": 1, "line": -3},
    "qr-ac-loc": {"page": "273v", "column": 2, "line": 17, "word": 5},
    "qr-bhq-comment": [
        "In my opinion, $BHQ benefits from ignoring $WLC here,",
        " though $BHQ likely ignored $WLC as a whole",
        " rather than considering and rejecting",
        " this particular change in $WLC relative to $BHS.",
    ],
    "qr-noted-by": "nWLC",
}
