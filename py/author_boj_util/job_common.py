from boj_render import boj_html
from author_boj_util import author


def suffix(contents):
    new_cont = "\N{EN DASH}\N{HAIR SPACE}" + contents
    inner = author.span_unpointed_tanakh(new_cont, {"dir": "rtl"})
    return boj_html.span(inner, {"style": "white-space:nowrap"})


def correctly_ignores(what, cv, adjective=""):
    return [
        _corr_ig_cmn(what, adjective),
        *[author.para(c) for c in _CORRECTLY_IGNORES_CONTENTS[cv]],
    ]


def core_ignores(option):
    return [
        f"Since $BHQ does not note any uncertainty in its transcription here{option},",
        " it is hard to distinguish whether $BHQ has ignored the mark in question",
        " on purpose or by accident.",
    ]


CAM1753_PAGE_URL_BASE = (
    "https://archive.org/details/ketuvim-cambridge-ms-add-1753-images/page"
)


def _corr_ig_cmn(what, adjective):
    adj = f" {adjective}" if adjective else ""
    contents = [
        f"$BHQ has no {what} here.",
        " I happen to think that this is the best transcription of μL here,",
        " but I don’t know whether $BHQ arrived at this transcription",
        " on purpose or by accident.",
        " Did the editors of $BHQ consider, but ultimately decide against,",
        f" the faint possible{adj} {what}?",
        " Or did they simply ignore μL entirely, supplying the consensus pointing,",
        f" which has no {what}?",
    ]
    return author.para(contents)


_SEE_3419_CONTENTS = [
    "See my entry on ",
    author.span_unpointed_tanakh("נכר"),
    " in $link_34_19 for further discussion.",
]
_MORE_BROADLY = [
    "More broadly, $BHQ Job never notes",
    " any uncertainty in its transcription of μL.",
    " This may mislead many readers.",
    " Despite the fact that",
    " high-resolution, color images of μL are now widely available,",
    " many readers will not engage with those images enough to understand how often",
    " there is great uncertainty in transcribing μL.",
    " And, even if the reader understands that such uncertainty exists in general,",
    " $BHQ should, in my opinion, indicate to the reader the specific cases",
    " where its transcription is particularly uncertain.",
]
_CORRECTLY_IGNORES_3419_CONTENTS = [
    core_ignores(""),
    _MORE_BROADLY,
]
_CORRECTLY_IGNORES_CONTENTS = {
    "34:19": _CORRECTLY_IGNORES_3419_CONTENTS,
    "36:29": [_SEE_3419_CONTENTS],
    "17:4": [_SEE_3419_CONTENTS],
}


BHQ_COMMENT_XELSEWHERE_DUBIOUS = [
    "$BHQ notes this possibility,",
    " whereas this is not noted in the other editions under consideration.",
    " It could be the editors of those other editions did not catch this,",
    " or it could be that they caught it",
    " but considered it to be too slight a possibility to note it.",
]
BHQ_COMMENT_CMN_0409_AND_SIMILAR = [
    "This is one of seven similar cases in Job in μL.",
    " All are correctly transcribed in $BHQ, i.e. transcribed without a מפיק.",
    " Although all are correctly transcribed in $BHQ,",
    " they are noted to different extents in $BHQ.",
]
BHQ_COMMENT_LIKE_0409 = [
    *BHQ_COMMENT_CMN_0409_AND_SIMILAR,
    " $link_4_9 discusses the matter at greater length.",
]


BHQ_COMMENT_0914_AND_0930 = [
    "$BHQ silently supplies the סילוק that is the consensus expectation,",
    " despite little or no evidence for it in μL.",
]
RECORD_1804_CMN_AB = {
    "qr-cv": "18:4",
    "qr-lc-proposed": "הֲ֭לְמַּעַנְךָ",
    "qr-consensus": "הַֽ֭לְמַעַנְךָ",
    "qr-bhq": "הַ֭לְמַּעַנְךָ",
    "qr-lc-loc": {"page": "402A", "column": 1, "line": -4},
}
RECORD_2221_CMN_AB = {
    "qr-cv": "22:21",
    "qr-lc-loc": {"page": "403B", "column": 1, "line": -6},
}
BHQ_COMMENT_2808_AND_2911 = [
    "$BHQ silently supplies the חיריק that is the consensus expectation,",
    " despite no evidence for it in μL.",
]
BHQ_COMMENT_CMN_3105_3206 = [
    "$BHQ silently supplies the marks in the vowel-then-accent order that is",
    " the consensus expectation, in clear contradiction of μL here.",
]
