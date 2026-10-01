"""Render the public display corpus as one pronunciation-selectable site.

The renderer has no source-record reader and writes no files. Its caller validates
the complete release and publishes the returned pages and the maintained assets.
"""

from pathlib import Path
from urllib.parse import quote

from mb_cmn import bib_locales
from phonetic_mam import display_schema
from py_html import legacy_html as html
from py_html import legacy_html_lines
from py_html.forbidden_phonetic_marks import refuse_forbidden_phonetic_marks

_YEIVIN_URL = "../yeivin-itm/yeivin_itm.html"
_SOURCE_URL = (
    "https://he.wikisource.org/wiki/"
    "%D7%9E%D7%A7%D7%A8%D7%90_%D7%A2%D7%9C_%D7%A4%D7%99_"
    "%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94"
)
_ASSETS = Path(__file__).with_name("assets")


def source_assets():
    """Return the single maintained CSS and JavaScript sources for publication."""
    return {
        name: (_ASSETS / name).read_bytes()
        for name in ("style.css", "pronunciation.js")
    }


def render_index():
    """Render the unified canonical book index, without loading any source data."""
    sections = []
    for section in bib_locales.ALL_SECIDS:
        links = []
        for book in bib_locales.bk39s_of_sec(section):
            links.extend((_link(book, f"tnkh/{_book_stem(book)}.html"), " "))
        sections.append([f"{section}: ", *links[:-1]])
    contents = [
        html.para(
            [
                "License: ",
                html.anchor(
                    "CC-BY-SA 4.0",
                    {"href": "https://creativecommons.org/licenses/by-sa/4.0/"},
                ),
                ". Source attribution: ",
                html.anchor("Hebrew Wikisource", {"href": _SOURCE_URL}),
                " and ",
                html.anchor(
                    "Al-Hatorah Mikraot Gedolot", {"href": "https://mg.alhatorah.org"}
                ),
                ".",
            ]
        ),
        html.unordered_list(sections),
        html.horizontal_rule(),
        html.para(_link("Phonetic testsuites", "testsuites.html")),
        html.para(html.anchor("Font license and source", {"href": "woff2/SOURCE.txt"})),
        html.para(
            html.anchor(
                [
                    "Excerpts from ",
                    html.span(
                        "Introduction to the Tiberian Masorah", {"class": "book-title"}
                    ),
                    " by Israel Yeivin",
                ],
                {"href": _YEIVIN_URL},
            )
        ),
    ]
    heading = "Phonetic Miqra according to the Masorah (MAM) (מקרא על פי המסורה)"
    return _page("Phonetic MAM: Book Links", heading, contents, "./")


def render_book_pages(book):
    """Return a book's index and chapters, with paths relative to the site root."""
    display_schema.validate_book(book)
    stem = _book_stem(book["book"])
    pages = {f"tnkh/{stem}.html": _book_page(book)}
    for chapter in book["chapters"]:
        filename = _chapter_filename(chapter["number"])
        pages[f"tnkh/{stem}/{filename}"] = _chapter_page(book, chapter)
    return pages


def render_chapter(book, chapter_number):
    """Render one chapter from a validated public book, with no I/O."""
    display_schema.validate_book(book)
    display_schema.require(
        type(chapter_number) is int and 1 <= chapter_number <= len(book["chapters"]),
        "unknown chapter",
    )
    return _chapter_page(book, book["chapters"][chapter_number - 1])


def _book_stem(book_id):
    return bib_locales.ordered_short_dash_full_39(book_id)


def _chapter_filename(number):
    return f"{number:02d}.html"


def _link(label, path, *, rel=None):
    attributes = {
        "href": f"{quote(path, safe='/')}?pronunciation=sephardic",
        "data-pronunciation-link": "",
    }
    if rel is not None:
        attributes["rel"] = rel
    return html.anchor(label, attributes)


def _navigation(links):
    contents = []
    for link in links:
        contents.extend((link, " · "))
    return html.htel_mk(
        "nav", {"aria-label": "Page navigation"}, html.para(contents[:-1])
    )


def _book_page(book):
    book_id = book["book"]
    stem = _book_stem(book_id)
    links = []
    for chapter in book["chapters"]:
        number = chapter["number"]
        path = f"{stem}/{_chapter_filename(number)}"
        links.extend((_link(str(number), path), " "))
    return _page(
        f"{book_id} chapter links",
        book_id,
        [_navigation([_link("Home", "../index.html")]), html.para(links[:-1])],
        "../",
    )


def _chapter_page(book, chapter):
    book_id, number = book["book"], chapter["number"]
    links = [
        _link("Home", "../../index.html"),
        _link(f"{book_id} chapters", f"../{_book_stem(book_id)}.html"),
    ]
    if number > 1:
        links.append(_link("Previous", _chapter_filename(number - 1), rel="prev"))
    if number < len(book["chapters"]):
        links.append(_link("Next", _chapter_filename(number + 1), rel="next"))
    content = [_navigation(links)]
    for verse in chapter["verses"]:
        number = verse["number"]
        content.append(
            html.heading_level_2(
                str(number), {"class": "verse-number", "id": f"v{number}"}
            )
        )
        content.append(html.table([_row(row, verse) for row in verse["rows"]]))
    title = f"{book_id} {chapter['number']}"
    return _page(title, title, content, "../../")


def _row(row, verse):
    cells = [
        html.table_datum(
            _tokens(tokens) if tokens is not None else None,
            {"dir": "rtl", "lang": "hbo"} if tokens is not None else None,
        )
        for tokens in row["hebrew"]
    ]
    counts = verse["transcription_columns"]
    for column in range(max(counts.values())):
        alternatives = []
        present = []
        for pronunciation in display_schema.PRONUNCIATIONS:
            if column >= counts[pronunciation]:
                continue
            present.append(pronunciation)
            tokens = row["transcriptions"][pronunciation][column]
            alternatives.append(
                html.span(
                    _tokens(tokens) if tokens is not None else None,
                    {"class": f"pronunciation-{pronunciation}"},
                )
            )
        attributes = None
        if len(present) == 1:
            attributes = {"class": f"column-{present[0]}-only"}
        cells.append(html.table_datum(alternatives, attributes))
    return html.table_row(cells)


def _tokens(tokens):
    elements = []
    for token in tokens:
        if isinstance(token, str):
            elements.append(token)
        elif token["kind"] == "implicit-maqaf":
            elements.append(
                html.span(
                    "\N{HEBREW PUNCTUATION MAQAF}", {"class": "mam-implicit-maqaf"}
                )
            )
        elif token["kind"] == "superscript-e":
            elements.append(html.sup("e"))
        elif token["kind"] == "stressed":
            elements.append(
                html.span(_tokens(token["content"]), {"class": "jt-stressed"})
            )
        elif token["kind"] == "reading":
            elements.append(
                html.span(_tokens(token["content"]), {"title": token["label"]})
            )
        else:
            raise display_schema.PublicReleaseError("unknown rendered token")
    return elements


def _controls():
    choices = [html.htel_mk("legend", flex_contents="Pronunciation")]
    for pronunciation in display_schema.PRONUNCIATIONS:
        identifier = f"pronunciation-{pronunciation}"
        attributes = {
            "type": "radio",
            "name": "pronunciation",
            "id": identifier,
            "value": pronunciation,
        }
        if pronunciation == "sephardic":
            attributes["checked"] = ""
        choices.extend(
            [
                html.htel_mk("input", attributes),
                html.htel_mk("label", {"for": identifier}, pronunciation.capitalize()),
            ]
        )
    return html.htel_mk("fieldset", {"class": "pronunciation-controls"}, choices)


def _page(title, heading, contents, asset_prefix):
    head = html.htel_mk(
        "head",
        flex_contents=[
            html.htel_mk("meta", {"charset": "utf-8"}),
            html.htel_mk(
                "meta",
                {"name": "viewport", "content": "width=device-width, initial-scale=1"},
            ),
            html.htel_mk("title", flex_contents=title),
            html.htel_mk(
                "link", {"rel": "stylesheet", "href": f"{asset_prefix}style.css"}
            ),
            html.htel_mk(
                "link", {"rel": "icon", "href": f"{asset_prefix}../favicon.svg"}
            ),
            html.htel_mk(
                "script", {"src": f"{asset_prefix}pronunciation.js", "defer": ""}
            ),
        ],
    )
    body = html.htel_mk(
        "body",
        flex_contents=[
            html.heading_level_1(heading),
            _controls(),
            html.htel_mk(
                "noscript",
                flex_contents=html.para(
                    "Without JavaScript, pronunciation controls affect this page only. "
                    "Links open with Sephardic pronunciation; URL selection and "
                    "Ashkenazic navigation persistence require JavaScript."
                ),
            ),
            html.htel_mk("main", flex_contents=contents),
        ],
    )
    tree = html.htel_mk("html", {"lang": "en"}, [head, body])
    text = "<!doctype html>\n" + "\n".join(
        legacy_html_lines.get_lines_from_html_el(False, tree)
    )
    refuse_forbidden_phonetic_marks(text, title)
    return text
