"""Shared identity of the four "Undoing and redoing the work of the Masoretes"
pages.

The series is *mutually* cross-linked -- Part 2 links back to Part 1 as well
as forward -- so the four page modules must not import each other. They import
this instead, and nothing here imports them.

Two spellings of every title are needed, and mixing them up is the easy
mistake. Anything that reaches ``author.dollar_sub`` (headings, link text)
must carry ``$`` keys, since ``dollar_sub_g._check_no_undollared`` raises on a
bare "qadma". Anything that does not (the HTML ``<title>``, the
``misc/index.html`` entry, which go through ``mb_html`` directly) must be
plain text, since an unsubstituted ``$qadma`` would reach the reader verbatim.
"""

from mb_author import author
from mb_misc import mb_html

SERIES = "Undoing and redoing the work of the Masoretes"

# One h1 per page rather than the source's single shared title, so that each
# page's top-level heading is unique. The subtitle becomes the h2.
SUBTITLES = {
    1: "The tale of the $qadma",
    2: "Saying the quiet part out loud",
    3: "Extra verses",
    4: "Atnaḥ hafukh",
}
SUBTITLES_PLAIN = {
    1: "The tale of the qadma",
    2: "Saying the quiet part out loud",
    3: "Extra verses",
    4: "Atnaḥ hafukh",
}
FNAMES = {
    1: "urwotm_1_tale_of_the_qadma.html",
    2: "urwotm_2_saying_the_quiet_part_out_loud.html",
    3: "urwotm_3_extra_verses.html",
    4: "urwotm_4_atnax_hafukh.html",
}

PARTS = (1, 2, 3, 4)


def heading_1(part: int) -> str:
    """This page's own h1. No ``$`` key occurs in it, but see heading_2."""
    return f"{SERIES} – Part {part}"


def heading_2(part: int) -> str:
    """This page's h2: the source's subtitle, dollared."""
    return SUBTITLES[part]


def plain_title(part: int) -> str:
    """The two halves rejoined, for ``<title>`` and ``misc/index.html``."""
    return f"{heading_1(part)}: {SUBTITLES_PLAIN[part]}"


def link_text(part: int) -> str:
    """The same string for contexts that do run through ``dollar_sub``."""
    return f"{heading_1(part)}: {SUBTITLES[part]}"


def link_to_part(part: int):
    """One entry of the series list that opens each of the four pages."""
    return author.anc_h(link_text(part), f"./{FNAMES[part]}")


def other_parts(part: int):
    """The other three parts, in order -- the series list of one page."""
    return [link_to_part(other) for other in PARTS if other != part]


def anchor_part(part: int):
    """A reference to one part from outside the series."""
    anchor = author.anchor_h("document", f"./{FNAMES[part]}")
    return author.std_anchor(anchor, link_text(part))


def romanized(text: str):
    """An italic term with no ``$`` key of its own.

    Ben's decision (Phase 2 review): a Latin phrase such as *mater lectionis*
    reuses the ``romanized`` class rather than earning a ``foreign`` class of
    its own. The class is styled ``font-style: italic`` and already carries
    any italicized term; giving Latin its own class would mean touching the
    stylesheet every misc page shares, for no visible difference.
    """
    return mb_html.span_c(text, "romanized")
