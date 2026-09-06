from author_boj_util import author
from author_boj_util import cos_urls

_COMMENT_PARA1 = [
    "Note that consensus has a rare and hard-to-understand",
    " phenomenon called “secondary מרכא” by Breuer."
    #
    " It may seem rather extraordinary to have two מרכא marks on the same word,",
    " but this is actually expected (or at least “allowed”).",
]
_FOI_H2 = "foi-sec-merk.html#intro-poetic/(mer)/(mer),(mer)"
_FOI_H1 = "https://bdenckla.github.io/MAM-basics/MAM-with-doc/foi/"
_FOI_ANC = author.anc_h("here", f"{_FOI_H1}{_FOI_H2}")
_COMMENT_PARA2 = [
    "This is one of about a dozen analogous cases listed",
    [" ", _FOI_ANC, "."],
]
_COS_ENG_ANC = author.anc_h("translation", cos_urls.cos_translation_url())
_COS_HEB_ANC = author.anc_h("original", cos_urls.cos_original_url())
_COMMENT_PARA3 = [
    "See Breuer CoS sections 9.23, 9.24, and 11.20.",
    " (CoS = The Cantillation of Scripture.)",
    [" (Note that an English ", _COS_ENG_ANC, " of CoS is now available,"],
    " a great boon to students of cantillation who cannot easily read",
    [" the ", _COS_HEB_ANC, " in its modern Hebrew.)"],
]
RECORD_3410 = {
    "qr-cv": "34:10",
    "qr-lc-proposed": "אַֽנֲשֵׁ֥י",
    "qr-what-is-weird": "געיה not מרכא (on א)",
    "qr-consensus": "אַ֥נֲשֵׁ֥י",
    "qr-generic-comment": [
        author.para(_COMMENT_PARA1),
        author.para(_COMMENT_PARA2),
        author.para(_COMMENT_PARA3),
        "In μY, the mark in question is absent: the א just has פתח.",
    ],
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "406B", "column": 2, "line": 14},
    "qr-ac-loc": {"page": "279r", "column": 1, "line": 10, "word": 5},
    "qr-noted-by": "tBHQ-zmiscWLC",
}
