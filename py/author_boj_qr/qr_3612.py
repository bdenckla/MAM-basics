from boj_render import boj_html
from author_boj_util import author
from author_boj_util.job_common import CAM1753_PAGE_URL_BASE

_BHQ_COMMENT = [
    "Here $BHQ has a typo:",
    [" it has ", author.hbo("בִּבְלִ־"), " rather than ", author.hbo("בִּבְלִי־")],
    " in the word it reports for μA and μY.",
    " I.e. it is missing a final $yod before the מקף.",
    " The same typo appears in the $BHQ section “Commentary on the Critical Apparatus.”",
    " In addition to the typo, for some reason $BHQ reports this word as being the קרי",
    [" of μY, i.e. M", boj_html.sup("Y(qere)")],
    [" rather than just M", boj_html.sup("Y"), "."],
    " I see no “Masorah dot pair”",
    " (μY’s equivalent of a masorah circle)",
    " on this word in μY.",
    " Nor do I see any קרי note in the margin.",
]
RECORD_3612 = {
    "qr-cv": "36:12",
    "qr-lc-proposed": "כִּבְלִי־",
    "qr-what-is-weird": "כ not ב",
    "qr-consensus": "בִּבְלִי־",
    "qr-generic-comment": [
        "Although my focus is pointing rather than spelling,",
        " I am interested in a spelling difference like this,",
        " since it is not just a מלא/חסר difference.",
    ],
    "qr-highlight": 1,
    "qr-lc-loc": {"page": "407B", "column": 1, "line": 4},
    "qr-ac-loc": {"page": "279v", "column": 1, "line": 22, "word": 2},
    "qr-bhq-comment": [author.para(_BHQ_COMMENT)],
    "qr-noted-by": "nBHQ-nDM-nWLC",
    "qr-cam1753-page-url": f"{CAM1753_PAGE_URL_BASE}/n87/mode/1up",
    "qr-uxlc-needs-fix": [
        "$UXLC has כ (as it should)",
        " but should note the divergence from consensus",
    ],
}
