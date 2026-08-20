from author_boj_util import author
from author_boj_util import cos_urls

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
_FOI_H1 = "https://bdenckla.github.io/MAM-with-doc/foi/"
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
