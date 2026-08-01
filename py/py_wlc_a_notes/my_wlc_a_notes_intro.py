"""Exprots INTRO"""

import py_html.wlc_utils_html as wlc_utils_html

_THIS_PAGE = (
    "This page describes the 39 words having bracket-a notes "
    + "in WLC. Here is how bracket-a notes are defined in "
    + "“A Reference Guide to the Westminster Leningrad Codex” (WLCmanual420.pdf):"
)
_DEFINITION_OF_AN_A_NOTE = (
    "[The a-note marks adaptations] to a Qere "
    + "that ל and BHS, by their design, do not indicate. "
    + "Usually this indicates the addition of a Maqqef to our Qere text "
    + "that is not present in the margin of ל, "
    + "or [...] the addition of a Dagesh or Mappiq to our Qere text "
    + "that is not present in the Ketiv consonants in the main text of ל."
)
_THIS_PAGE_ALSO = (
    "This page also provides links to 37 UXLC change proposals related to these bracket-a notes. "
    + "(There are only 37 not 39 because two of the bracket-a notes "
    + "did not motivate a new change proposal. "
    "One of those two, 1s9:1, already has a pending change proposal "
    "that addresses the issue at hand. "
    "The other, 1k9:9, is a mystery to me: "
    "I can’t figure out what adaptation the bracket-a note is referring to.)"
)
_THIS_PAGE_USES = "This page uses the following abbreviations:"


def _initialisms(no_ucp):
    return wlc_utils_html.unordered_list(
        [
            *([] if no_ucp else ["UCP for “UXLC change proposal”"]),
            "MPK for “manuscript’s pointed ketiv”",
            "AI for “the part of the WLC qere that is at issue”",
            "AIC for “AI category,” i.e. “the type of thing that is at issue in the WLC qere”",
        ]
    )


def intro(no_ucp):
    return [
        wlc_utils_html.para(
            [_THIS_PAGE, wlc_utils_html.blockquote(_DEFINITION_OF_AN_A_NOTE)]
        ),
        *([] if no_ucp else [wlc_utils_html.para([_THIS_PAGE_ALSO])]),
        wlc_utils_html.para([_THIS_PAGE_USES]),
        _initialisms(no_ucp),
    ]
