"""Exports main"""

from py_misc import my_html
from pyauthor_util import author


def anchor():
    return author.std_anchor(_ANCHOR, _H1_CONTENTS)


def gen_html_file(tdm_ch):
    cbody = [
        author.heading_level_1(_H1_CONTENTS),
        author.para(_INTRO_PARA),
        author.heading_level_2("Endnotes"),
        author.para(_ENDNOTE_1),
    ]
    return author.help_gen_html_file(__file__, tdm_ch, _FNAME, _TITLE, cbody)


def _endnote_callout(num):
    """Baseline (non-superscript) endnote callout: [N] where N is a link."""
    return ["[", my_html.anchor_h(str(num), f"#en{num}"), "]"]


def _endnote_body(num, contents):
    """Endnote entry: [N] text, with an id anchor for the callout to target."""
    marker = my_html.anchor(str(num), {"id": f"en{num}"})
    return ["[", marker, "] ", contents]


def _nbsp(text):
    """Return text with regular spaces replaced by non-breaking spaces."""
    return text.replace(" ", "\N{NO-BREAK SPACE}")


_TITLE = "The Next 700 Bibles"
_H1_CONTENTS = "The Next 700 Bibles"
_FNAME = "the_next_700_bibles.html"
_ANCHOR = my_html.anchor_h("document", f"./{_FNAME}")

_URL_LANDIN_PDF = "https://www.cs.cmu.edu/~crary/819-f09/Landin66.pdf"
_ANC_LANDIN = my_html.anchor_h("(PDF)", _URL_LANDIN_PDF)

_INTRO_PARA = [
    "This document's title is inspired by the title"
    " (and some of the spirit) of an influential 1966 paper by "
    + _nbsp("P. J. Landin."),
    " ",
    _endnote_callout(1),
]

_ENDNOTE_1 = _endnote_body(
    1,
    [
        _nbsp("P. J. Landin,")
        + " "
        + author.dquote("The Next 700 Programming Languages,")
        + " ",
        author.emphasis("Communications of the ACM"),
        ", "
        + _nbsp("vol. 9")
        + ", "
        + _nbsp("no. 3")
        + ", March 1966, "
        + _nbsp("pp. 157–166")
        + ". ",
        _ANC_LANDIN,
    ],
)
