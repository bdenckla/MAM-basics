"""Cross-book helper constants/functions shared by the ob_notes_* modules."""

from __future__ import annotations

from py_html import wlc_utils_html

# Transliteration term constants.  Several accent/term names contain het, which
# the repo writes precomposed (U+1E25).  Defining each term once here lets
# the ob_notes_* modules interpolate the glyph (e.g. f"...{TIPEXA}...") instead
# of embedding it inline.  The X in each name is the repo's ASCII stand-in for
# het (TIPEXA -> "tipeXa" -> "tipe" + het + "a").  Issue #36 review follow-up.
_XET = "ḥ"
TAXTON = "ta" + _XET + "ton"
TIPEXA = "tipe" + _XET + "a"
MUNAX = "muna" + _XET
DEXI = "de" + _XET + "i"
ATNAX = "atna" + _XET
ETNAXTA = "etna" + _XET + "ta"
PETUXAH = "petu" + _XET + "ah"
MINXAT = "Min" + _XET + "at"


def ambiguous_mark_context_comment(marked_word: str) -> str:
    return (
        f"In the LC, inclination does not reliably identify a mark as a merkha, a {TIPEXA}, or a meteg."
        " Yet, from context, we can usually determine the most likely intended meaning,"
        f" and that is the case here with {marked_word}."
    )


TIP_LIKE_INCL = f"The slightly northwest-to-southeast ({TIPEXA}-like) inclination of the mark in question is, while not irrelevant, hardly definitive."


MISSING_SOF_PASUQ_SUMMARY = (
    "A sof pasuq is missing somewhere in the LC-BHS-WLC pipeline."
)


MISSING_SOF_PASUQ_COMMENT = (
    "Likely the sof pasuq is missing from the start of the pipeline, i.e. from the LC."
)


SOMEWHERE = "Somewhere in the LC-BHS-WLC pipeline, $wlc_focus_desc appears rather than $diff_wlc_mam_desc."


BHS_TRANSCRIBES = "BHS transcribes a $diff_wlc_mam_desc as a $wlc_focus_desc."


ZARQA_WHIM_SUMMARY = "WLC turns a scribal zarqa whim into an outright error."


# In-page link to the nu 20:19 ungrammatical section. The href must match that
# section's anchor id (see ob_report.ungrammatical_anchor_id: "ob" + bcv with ":"->"v").
ZARQA_WHIM = {
    "st-summary": ZARQA_WHIM_SUMMARY,
    "comment": (
        [
            "This is one of twelve items of this type. See ",
            wlc_utils_html.anchor("nu 20:19", {"href": "#obnu20v19"}),
            " for more discussion of items like this.",
        ],
    ),
}
