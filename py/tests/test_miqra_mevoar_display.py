"""Differential: each display page shows MAM-simple's verses and breaks and the headings.

py/miqra_mevoar/display_page.py generates Miqra Mevoar's display pages from MAM-simple's
break elements and from the tracked JSON. Each page that it generates is read back by
its closed parser, display_page.read_page, which raises on any line outside the three
line shapes, and is compared with oracles that do not share the generator's reading:

- Its verse lines are MAM-simple's verses of the page's chapters, in order, as the
  verses' osisIDs give them: each names the book as MAM does, and gives its chapter and
  verse as Hebrew numerals.
- Its petuhot and setumot are those that MAM-simple records in a verse's
  starts-with-sampe field, its own record of a break between the verse and the one
  before it, except at a book's first verse, where the field would record a break
  between two books. The generator reads the break elements instead; a break inside a
  verse has no such field and gets no line.
- Its headings stand where the tracked JSON, in/miqra-mevoar/, gives a verse a heading,
  each transcluded from the verse's base chapter, the title that
  py/miqra_mevoar/wikitext.py's page_title gives, by the heading's section there.
- Its category line sorts it under its own name.
- The pages of a book, such as Joshua's two parts, together show its verses once each,
  in order.

The oracle finds each book in MAM-simple by its OSIS abbreviation in
py/mb_misc/osis_book_abbrevs.py, not by the converter's table of books. A missing input
fails rather than skips.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_miqra_mevoar_display.py
"""

import functools
import json

import pytest

from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn import mam_bknas_and_std_bknas
from mb_cmn import paths
from mb_misc import osis_book_abbrevs
from miqra_mevoar import books
from miqra_mevoar import display_page
from miqra_mevoar import tracked
from miqra_mevoar import wikitext

_KEYS = list(display_page.PAGES)


def test_the_table_lists_pages():
    """Fail, rather than parametrize nothing, when no page is listed."""
    assert _KEYS, "display_page.PAGES lists no page"


@pytest.mark.parametrize("key", _KEYS)
def test_a_page_shows_mam_simple_and_the_tracked_headings(key):
    page = display_page.PAGES[key]
    book = books.book_of_stem(page.stem)
    verses, name = display_page.read_page(display_page.page_text(page))
    assert name == page.name
    assert verses == _expected_verses(page, book)


def test_the_pages_of_a_book_show_it_once():
    shown = {}
    for page in display_page.PAGES.values():
        verses, _name = display_page.read_page(display_page.page_text(page))
        shown.setdefault(page.stem, []).extend(
            (verse.chapter, verse.verse) for verse in verses
        )
    for stem, numerals in shown.items():
        expected = [
            (hvn.INT_TO_STR_DIC[chapter], hvn.INT_TO_STR_DIC[verse])
            for (chapter, verse), _sampe in _mam_simple_verses(
                books.book_of_stem(stem).mam_book
            )
        ]
        assert numerals == expected, stem


def _expected_verses(page, book):
    """The page's verses as the oracles give them, in display_page.Verse's form."""
    verses = _mam_simple_verses(book.mam_book)
    first, last = page.chapters or (1, verses[-1][0][0])
    bk39id = mam_bknas_and_std_bknas.MAM_HBNP_TO_BK39ID[book.mam_book]
    headings = _tracked_headings(book)
    expected = []
    for at, ((chapter, verse), sampe) in enumerate(verses):
        if not first <= chapter <= last:
            continue
        heading = None
        if (chapter, verse) in headings:
            heading = (
                wikitext.page_title(book.mam_book, chapter),
                f"{wikitext.HEADING_SECTION}{hvn.INT_TO_STR_DIC[verse]}",
            )
        expected.append(
            display_page.Verse(
                mam_bknas_and_std_bknas.he_bk39_name(bk39id),
                hvn.INT_TO_STR_DIC[chapter],
                hvn.INT_TO_STR_DIC[verse],
                None if at == 0 or sampe is None else _SAMPE_LETTERS[sampe],
                heading,
            )
        )
    return expected


@functools.cache
def _mam_simple_verses(mam_book):
    """Each verse of a book in MAM-simple: its (chapter, verse) and starts-with-sampe."""
    bk39id = mam_bknas_and_std_bknas.MAM_HBNP_TO_BK39ID[mam_book]
    osis_id = osis_book_abbrevs.BOOK_ABBREVS[bk39id]
    found = [
        item
        for path in sorted(paths.require_mam_simple_vtrad_mam_dir().glob("*.json"))
        for item in json.loads(path.read_text(encoding="utf-8"))["contents"]
        if item["type"] == "book39" and item["osisID"] == osis_id
    ]
    assert len(found) == 1, f"MAM-simple has {len(found)} books {osis_id}"
    verses = []
    for chapter in found[0]["contents"]:
        if chapter["type"] in _BREAKS:
            continue
        assert chapter["type"] == "chapter", f"{osis_id}: {chapter['type']}"
        for verse in chapter["contents"]:
            if verse["type"] in _BREAKS:
                continue
            assert verse["type"] == "verse", f"{chapter['osisID']}: {verse['type']}"
            book_id, chapter_number, verse_number = verse["osisID"].split(".")
            assert book_id == osis_id, verse["osisID"]
            verses.append(
                (
                    (int(chapter_number), int(verse_number)),
                    verse.get("starts-with-sampe"),
                )
            )
    assert verses, f"MAM-simple's {osis_id} has no verses"
    return tuple(verses)


def _tracked_headings(book):
    """The (chapter, verse) of each verse that the tracked JSON gives a heading."""
    return {
        (chapter["chapter"], verse["verse"])
        for chapter in tracked.read_record(book)["chapters"]
        for verse in chapter["verses"]
        if verse["heading"] is not None
    }


# The petuha and setuma breaks, which stand between books and chapters too.
_BREAKS = frozenset({"spi-pe2", "spi-pe3", "spi-samekh2", "spi-samekh3"})
# starts-with-sampe takes a break's bare name, and a page gives it as its letter.
_SAMPE_LETTERS = {
    "pe2": "\N{HEBREW LETTER PE}",
    "pe3": "\N{HEBREW LETTER PE}",
    "samekh2": "\N{HEBREW LETTER SAMEKH}",
    "samekh3": "\N{HEBREW LETTER SAMEKH}",
}
