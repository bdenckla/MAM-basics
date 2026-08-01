"""HTML coordinator for the "almost errors" page.

Holds the report title, the page-level intro, and ``render_body_contents``,
which threads the two top-level sections together in document order:

  * ``almost_errors_charities`` -- the "Editorial charities" section; and
  * ``almost_errors_oddities`` -- the "Masoretically-blessed oddities" section.

The small shared render helpers live in ``almost_errors_html_shared``; the "real
computing" (parse trees and verdicts) lives in ``almost_errors_trees``.

It shares goerwitz.html's stylesheet + width-limited shell and the shared
error-tree table renderer (``ob_tree_table``), so a later merge with the
prose/poetic reports is mechanical.
"""

from __future__ import annotations

from accgram.almost_errors_charities import (
    charities_intro,
    geresh_muqdam_section,
    ps124_section,
)
from accgram.almost_errors_html_shared import link
from accgram.almost_errors_oddities import (
    double_tsinnor_section,
    ek2031_section,
    oddities_intro,
    telg_section,
)
from accgram.prose_scanner import HasLegarmeh
from py_html import wlc_utils_html as H

REPORT_TITLE = "Almost errors"
_WIDTH_CLASS = "goerwitz-tms-width-limited"


def _intro() -> tuple[object, ...]:
    return (
        H.heading_level_1(REPORT_TITLE),
        H.heading_level_2("Introduction"),
        H.para(
            "This page documents the accent-grammar checker's “almost errors”:"
            " cantillation features that a naïve checker would flag, but that we"
            " do not flag — and, in each case, the reading we chose is a choice,"
            " not a forced move. Two kinds appear here."
        ),
        H.para(
            (
                "First, the ",
                H.bold("editorial charities"),
                ": places where the checker silently normalizes away a genuine quirk"
                " of WLC — sometimes a real Leningrad Codex feature, sometimes an"
                " artifact introduced in BHS or WLC — and reads the text charitably"
                " rather than reporting an error. Here something at least questionable"
                " is being forgiven; the value is transparency about exactly what the"
                " checker quietly fixes, in which direction, and why.",
            )
        ),
        H.para(
            (
                "Second, the ",
                H.bold("masoretically-blessed oddities"),
                ": features that look error-like — two accents crowding"
                " one letter or one chanted word, or one divider written twice in a row — but"
                " that are 100% official masoretic tradition, attested in the standard"
                " manuscripts, ",
                H.bold("not"),
                " leniencies specific to LC, BHS, or WLC. Nothing here is forgiven; the"
                " checker accepts these, and where it must pick how to represent one for"
                " parsing — keep both marks as a sequence, fuse a pair into one token,"
                " carry a single mark, or collapse a repeated divider to one — that choice"
                " is, for the multi-accent cases, among readings that all parse cleanly (the"
                " telisha gedola exhibit below shows the alternatives). The headline case"
                " is Ezekiel 20:31’s mahapakh + qadma (",
                H.code("mahapakh!qadma"),
                "), the only chanted word in Tanakh with two conjunctive accents on"
                " one letter.",
            )
        ),
        H.para(
            (
                "Companion pages: the prose ",
                link("Goerwitz checker run", "goerwitz.html"),
                " and the ",
                link("poetic checker run", "poetic.html"),
                " list the verses the checker actually flags; this page is the"
                " inventory of what it deliberately does not.",
            )
        ),
    )


def render_body_contents(
    index, parser, has_legarmeh: HasLegarmeh
) -> tuple[object, ...]:
    sections: list[object] = [
        *_intro(),
        *charities_intro(),
        *geresh_muqdam_section(),
        *ps124_section(),
        *oddities_intro(),
        *telg_section(index, parser, has_legarmeh),
        *ek2031_section(index, parser, has_legarmeh),
        *double_tsinnor_section(),
    ]
    wrapper = H.div(tuple(sections), {"class": _WIDTH_CLASS})
    return (wrapper,)
