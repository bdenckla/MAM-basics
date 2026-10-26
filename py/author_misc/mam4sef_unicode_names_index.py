"""The Unicode-name listings of MAM for Sefaria: writes ``unicode-names/index.html``.

The page is ``gh-pages/MAM-for-Sefaria/unicode-names/index.html``.  The listings of
``misc/unicode-names/`` were a section of "The encoding of MAM for Sefaria" until Ben gave them
a page of their own on 2026-10-26, to which that page links; ``mam4sef_common.py`` has his
words.  Like that page, this one names no folder of the AJF variant, whose own page no page of
the documentation links to.

``mam4sef_survey`` rebuilds every listing from its CSV file and checks it against the tracked
listing, so what this page says of their format holds for every line, and the example's lines
are read from the tracked listing itself.
"""

from mb_author import author
from mb_cmn import bib_locales as tbn
from mb_cmn import str_defs as sd
from mb_misc import mb_html
from author_misc import mam4sef_common as mc
from author_misc import mam4sef_survey as ms

_INDEX_HREF = "../index.html"
_EX_LISTING = "Genesis 1:5"


def _head(verse) -> str:
    """The line that names ``verse`` in its listing."""
    return f"{verse.bk39id} {verse.chapter}:{verse.verse} in vtrad {tbn.VT_SEF}"


def _intro():
    return [
        author.heading_level_2("Introduction", {"id": "introduction"}),
        mc.p(
            "The folder ",
            mc.code(f"{ms.FOLDER_NAMES}/"),
            " of ",
            mb_html.anchor_h(mc.code("MAM-for-Sefaria"), mc.PRODUCT_URL),
            " lists, by their Unicode names, the code points of the verses of the folder ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            ", whose files the page ",
            mc.title_link(mc.INDEX_TITLE, _INDEX_HREF),
            " describes. This page describes the listings. Every count and example on it is"
            " taken from the files.",
        ),
        *mc.conventions(attention=False),
    ]


def _listings(s):
    verse = s.verse(_EX_LISTING)
    head = _head(verse)
    lines = ms.listing_verse(ms.FOLDER_NAMES, verse.book, head)
    # mb_html wraps a line longer than 100 characters, and refuses two spaces in a row.
    if any(len(line) > 90 or "  " in line for line in lines):
        raise ValueError(
            f"{_EX_LISTING}: a listing line that the page's <pre> would break"
        )
    other = next(v for v in s.verses if v.bk39id != v.book)
    spaced_title = next(book for book in ms.BOOKS if " " in book)
    example = mb_html.table(
        [
            mc.tr(
                [
                    mc.td_he(mc.snippet(verse, 0, len(verse.text))),
                    mc.td_ref(verse.ref),
                ]
            )
        ],
        {"class": "data"},
    )
    return [
        author.heading_level_2("The listings", {"id": "listings"}),
        mc.p(
            "The folder has a listing for each file of ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            ", named as that file is but for its extension, as ",
            mc.code(f"{spaced_title}.txt"),
            " is, and a provenance note, ",
            mc.code(ms.PROVENANCE_NAME),
            ". The listings are text files in UTF-8, with LF line ends. A listing's first"
            " line is ",
            mc.code(f"unicode_names {verse.book}"),
            ", for its book. Then each verse has a line that names it, a line for each run"
            " of its text, and a blank line, but for the last verse.",
        ),
        mc.p(
            "The line that names a verse has the book's identifier in ",
            mc.code("MAM-basics"),
            ", the chapter and verse, and the verse numbering, which is Sefaria's, as ",
            mc.code(head),
            " and ",
            mc.code(_head(other)),
            " do. Each ",
            mc.uname(" "),
            " and ",
            mc.uname(sd.NBSP),
            " has a line of its own, with its name, and so splits the text into runs. A"
            " run's line has its code points, separated by commas, each by the short name"
            " that the table below gives it. Each HTML element has lines of its own: one"
            " with ",
            mc.code("START"),
            " and the element's tag and class before its contents, and one with ",
            mc.code("STOP"),
            " after them, or a single line with ",
            mc.code("START/STOP"),
            " for ",
            mc.code("br"),
            ", which has no contents.",
        ),
        mc.p(
            f"For example, {mc.short_ref(_EX_LISTING)} has this text in ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            ":",
        ),
        mb_html.div([example], {"class": "table-wrap"}),
        mc.p("and these lines in its listing:"),
        mb_html.htel_mk("pre", None, ["\n".join(lines)]),
    ]


def _code_points(s):
    chars = sorted(s.code_points_csv)
    rows = [
        mc.tr(
            [
                mb_html.table_datum(mc.code(f"U+{ord(c):04X}")),
                mb_html.table_datum(mc.uname(c, full=True)),
                mb_html.table_datum(mc.code(ms.short_name_in_listings(c))),
                mc.td_num(s.code_points_csv[c]),
            ]
        )
        for c in chars
    ]
    return [
        author.heading_level_2("The code points", {"id": "code-points"}),
        mc.p(
            f"These are all {len(chars)} code points that the verses of ",
            mc.code(f"{ms.FOLDER_CSV}/"),
            " have, with the short name that each has in the listings, and how many times"
            " the verses have it:",
        ),
        mc.table(["Code point", "Unicode name", "In the listings", "Count"], rows),
    ]


def _pin_claims(s) -> None:
    """Fail the build if the data stops supporting a claim the prose states in words."""
    # "a listing for each file of csv/": every verse of csv/ is listed.
    assert s.listings["csv verses"] == len(s.verses)
    # The page describes no line that a listing has and its verse lacks.
    assert s.listings["csv stripped"] == 0


def gen_html_file():
    """Write the page and its font, and return the page's path."""
    s = ms.survey()
    _pin_claims(s)
    cbody = [
        *mc.page_head(mc.LISTINGS_TITLE),
        *_intro(),
        *_listings(s),
        *_code_points(s),
    ]
    return mc.write_page(__file__, mc.LISTINGS_DIR, mc.LISTINGS_TITLE, cbody, s)
