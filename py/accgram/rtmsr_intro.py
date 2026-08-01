from __future__ import annotations

from accgram import rtmsr_bracket_notes
from py_html import wlc_utils_html

_GC_AUTHOR = "Goerwitz, Richard"
_GC_TITLE = (
    "A New Masoretic “Spell Checker” or A Fast, Practical Method For Checking "
    "the Accentual Structure and Integrity Of Tiberian-Pointed Biblical Texts"
)
_GC_BOOK_TITLE = (
    "Studies in Semitic and Afroasiatic Linguistics Presented to Gene B. Gragg"
)
_GC_SERIES = "Studies in Ancient Oriental Civilization 60"
_GC_PAGES = "111-122"
_GC_YEAR = "2007"
_GC_ISBN = "978-1-885923-41-7"
_GC_BOOK_URL = (
    "https://isac.uchicago.edu/research/publications/saoc/"
    "saoc-60-studies-semitic-and-afroasiatic-linguistics-presented-gene-b"
)


def build_intro_contents(
    ungrammatical_count: int,
) -> tuple[object, ...]:
    intro_text = (
        f"This page lists the {ungrammatical_count} WLC 4.22 verses that are considered ungrammatical"
        " by the Python port of the Goerwitz accent checker."
    )
    ungrammatical_text = (
        "These verses are considered ungrammatical because they parse into a tree"
        " containing the string \u201cERROR\u201d; each section below includes one such"
        " tree. Potential causes of \u201cERROR\u201d include"
        " WLC issues,"
        " BHS issues,"
        " LC issues, and"
        " checker issues."
        " (Issues include errors but also mere quirks.)"
    )
    msp_text = "The issues can be filtered by their category:"
    msp_categories = (
        "“Missing sof pasuq.”",
        "“Missing silluq,” where a sof pasuq is present but the verse-final chanted word has no accent.",
        "“Zarqa whim,” where WLC turns a scribal zarqa whim into an error.",
        "“Other,” for everything else.",
    )
    source_text = (
        "The issues can also be filtered based on the source of the issue:"
        " WLC, BHS/BHQ, the LC, or unclear/TBD."
        "This \u201cSource\u201d filter is ANDed with the category filter."
    )
    and_text = (
        "There are two further filters, each ANDed with the filters above:"
        " whether the issue has an associated UXLC change, and"
        " whether the word in question has a bracket-note in WLC."
        " Each toggle is three-state: has, doesn’t have, or don’t care"
        " (the default)."
    )
    bracket_notes_text = (
        "We define the bracket-note codes in the ",
        wlc_utils_html.anchor(
            rtmsr_bracket_notes.WLC_BRACKET_NOTES_HEADING,
            {"href": f"#{rtmsr_bracket_notes.WLC_BRACKET_NOTES_ANCHOR_ID}"},
        ),
        " section at the end of this page, but you can also hover over"
        " their use in any verse to see these definitions.",
    )
    almost_errors_text = (
        "For a discussion of quirks that the checker silently accepts, see the ",
        wlc_utils_html.anchor("Almost errors", {"href": "almost-errors.html"}),
        " page.",
    )
    printed_decalogue_text = (
        "Aside: this page runs the checker on WLC (after ",
        wlc_utils_html.anchor(
            "supplying certain marks", {"href": "supplied-marks.html"}
        ),
        "); whether the accents in the"
        " Decalogues of the printed tradition are grammatical is examined in ",
        wlc_utils_html.anchor(
            "In the printed tradition, are the accents of the Decalogue grammatical?",
            {"href": "printed-decalogue.html"},
        ),
        ".",
    )

    return (
        wlc_utils_html.heading_level_2("Introduction"),
        wlc_utils_html.para(intro_text),
        wlc_utils_html.para(ungrammatical_text),
        wlc_utils_html.para(msp_text),
        wlc_utils_html.unordered_list(msp_categories),
        wlc_utils_html.para(source_text),
        wlc_utils_html.para(and_text),
        wlc_utils_html.para(bracket_notes_text),
        wlc_utils_html.para(almost_errors_text),
        wlc_utils_html.para(printed_decalogue_text),
    )


def checker_article_citation_contents() -> tuple[object, ...]:
    citation_text = (
        f"{_GC_AUTHOR}. ‹{_GC_TITLE}.›" f" In {_GC_BOOK_TITLE} (pp. {_GC_PAGES}). (",
        wlc_utils_html.anchor(_GC_SERIES, {"href": _GC_BOOK_URL}),
        f"). The Oriental Institute, Chicago, {_GC_YEAR}. ISBN {_GC_ISBN}.",
    )
    return (
        wlc_utils_html.para(
            "The Goerwitz accent grammar checker is described in the following article:"
        ),
        wlc_utils_html.para(citation_text),
    )
