from mb_cmn.url_percent import pct_fragment
from author_boj_util import author
from author_boj_util import cos_urls

_COMMENT_PARA1 = [
    "Note that consensus has a rare and hard-to-understand",
    " phenomenon called “secondary מרכא” by Breuer.",
]
_FOI_FRAGMENT = "intro-poetic/(üazll)/(mer)-(üazll)"
_FOI_H2 = f"foi-sec-merk.html#{pct_fragment(_FOI_FRAGMENT)}"
_FOI_H1 = "https://bdenckla.github.io/MAM-basics/MAM-with-doc/foi/"
_FOI_ANC = author.anc_h("here", f"{_FOI_H1}{_FOI_H2}")
_COMMENT_PARA2 = [
    ["This is one of only two strictly analogous cases listed"],
    [" ", _FOI_ANC, ","],
    [" though there are about 30 analogous cases if one includes those"],
    [" where the analogy is allowed to be less strict."],
    [" What makes this case “rare among rare” is that, contrary to most cases,"],
    [" the מקף that is normally implicit is explicit (in the consensus)."],
    [" Interestingly, μL has some sort of disturbance where one would expect the מקף,"],
    [" suggesting that there might have been a מקף here that was erased."],
]
_COS_ENG_ANC = author.anc_h("translation", cos_urls.cos_translation_url())
_COS_HEB_ANC = author.anc_h("original", cos_urls.cos_original_url())
_COMMENT_PARA3 = [
    "See Breuer CoS sections 09.27, 9.37, and 11.06.rn2.",
    " (CoS = The Cantillation of Scripture.)",
    [" (Note that an English ", _COS_ENG_ANC, " of CoS is now available,"],
    " a great boon to students of cantillation who cannot easily read",
    [" the ", _COS_HEB_ANC, " in its modern Hebrew.)"],
]
_COMMENT_PARA4 = [
    "In μY, like μL, there is no מקף.",
]
_BHQ_COMMENT = [
    "The mark under the $vav of %ותהי was changed",
    " from מרכא to געיה in going from $BHS to $BHQ.",
    " This was a regression, in my opinion, since it leaves %ותהי with no accent, only געיה.",
    " This is an uncharitable transcription.",
]
RECORD_0610 = {
    "qr-noted-by": "tBHQ-nDM",
    "qr-cv": "6:10",
    "qr-consensus": "וּ֥תְהִי־ע֨וֹד׀",
    "qr-lc-proposed": "וּֽתְהִי ע֨וֹד׀",
    "qr-what-is-weird": "געיה not מרכא-מקף",
    "qr-highlight-lc-proposed": 1,
    "qr-highlight-consensus": [1, 5],
    "qr-lc-loc": {"page": "398B", "column": 2, "line": 7},
    "qr-ac-loc": {"page": "271v", "column": 2, "line": 5, "word": 1},
    "qr-generic-comment": [
        author.para(_COMMENT_PARA1),
        author.para(_COMMENT_PARA2),
        author.para(_COMMENT_PARA3),
        author.para(_COMMENT_PARA4),
    ],
    "qr-bhq-comment": [
        author.para(_BHQ_COMMENT),
    ],
}
