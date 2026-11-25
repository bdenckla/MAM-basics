"""Differential: each display page shows MAM-simple's verses and breaks and the headings.

py/miqra_mevoar/display_page.py generates Miqra Mevoar's display pages from MAM-simple's
break elements and from the places of the headings. Each page that it generates is read
back by its closed parser, display_page.read_page, which raises on any line outside the
four line shapes, and is compared with oracles that do not share the generator's
reading:

- Its verse lines are MAM-simple's verses from the page's first bound to its last, in
  order, as the verses' osisIDs give them: each names the book as MAM does, and gives
  its chapter and verse as Hebrew numerals. The first of them, and no other, gives the
  chapter parameter, its chapter's numeral, exactly where its verse number is not 1.
- Its petuhot and setumot are those that MAM-simple records in a verse's
  starts-with-sampe field, its own record of a break between the verse and the one
  before it, except at a book's first verse, where the field would record a break
  between two books. The generator reads the break elements instead; a break inside a
  verse has no such field and gets no line. Nor has the verse after a petuha that
  MAM-simple nests in a scribal-difference element: this test's own walk of those
  elements finds each such petuha, before the verse after the one that holds it, and
  the page must give it the first parameter that display_page.DISPUTED_PETUHOT gives
  it. Each one that the walk finds must be in that table, with MAM's note, and each in
  the table must be found.
- Its headings stand where the tracked JSON, in/miqra-mevoar/, gives a verse a heading,
  or, for a book of the Torah, where its file of heading places in
  in/miqra-mevoar-base-headings/, read here by json alone, has one. Each is transcluded
  from the verse's base chapter, the title that py/miqra_mevoar/wikitext.py's
  page_title gives, by the heading's section there.
- A line of the Decalogue stands exactly at each verse of display_page.DECALOGUE, with
  the call that the table gives it, and at no other verse. The table's verses must be
  consecutive verses of MAM-simple's Exodus 20 and Deuteronomy 5, and the numeral of
  each call that has one must be its verse's.
- Its category line sorts it under its own name, or under the sort key that
  display_page.PAGES gives it, as it gives Joshua's two parts the names under which
  Stage 10 created them.
- The pages of a book, such as Joshua's two parts, Judges' three, Daniel's two,
  Genesis' four and each other book of the Torah's three, together show its verses once
  each, in order, across a boundary inside a chapter, as between Judges 2:5 and 2:6 or
  Genesis 25:18 and 25:19, as well as between chapters. A book's verses here are
  MAM-simple's of the chapters that its tracked record holds, which may be only some of
  them: Isaiah's one page shows 40:1 to 66:24.
- Every page begins with a block of title and navigation: its line, a horizontal rule
  and two blank lines. The links of the block's line, found by this test's own reading
  of it, are its topics and then its chapters. Its topics are the verses to which the
  oracle of the headings gives a heading, in order, each anchored by its chapter's and
  its verse's numerals and labelled by the transclusion of its heading's section from
  its base chapter; its chapters are those of the oracle's verses on the page, each
  anchored at its first verse there and labelled by its numeral. read_page gives back
  the block's name, which must be the block_name that display_page.PAGES gives the
  page.
- The block_name of every entry of display_page.PAGES and of
  display_page.BLOCK_ONLY_PAGES holds a Hebrew point, is in NFC, the form MediaWiki
  stores, and has no range in parentheses at its end, and the two tables' keys do not
  meet. The pages of BLOCK_ONLY_PAGES, Avi's pages for the Five Megillot, which the bot
  did not make, have no oracle here: the dry run's reads of their live pages are their
  check.

The oracle finds each book in MAM-simple by its OSIS abbreviation in
py/mb_misc/osis_book_abbrevs.py, not by the converter's tables of books. A missing input
fails rather than skips.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_miqra_mevoar_display.py
"""

import functools
import json
import re
import unicodedata

import pytest

from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn import mam_bknas_and_std_bknas
from mb_cmn import paths
from mb_misc import osis_book_abbrevs
from miqra_mevoar import base_headings
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
    text = display_page.page_text(page)
    block_name, verses, sort_key = display_page.read_page(text)
    assert sort_key == (page.name if page.sort_key is None else page.sort_key)
    expected = _expected_verses(page)
    assert verses == expected
    assert block_name == page.block_name
    assert block_name is not None, key
    lines = text.split("\n")
    assert lines[1:4] == [_RULE, "", ""]
    assert _BLOCK_LINK.findall(lines[0]) == _expected_block_links(expected)


def test_each_block_name_is_pointed_nfc_and_without_a_range():
    entries = [
        (key, page.block_name)
        for table in (display_page.PAGES, display_page.BLOCK_ONLY_PAGES)
        for key, page in table.items()
    ]
    assert display_page.BLOCK_ONLY_PAGES, "display_page.BLOCK_ONLY_PAGES lists no page"
    for key, name in entries:
        assert name is not None, key
        assert any(
            unicodedata.name(char, "").startswith("HEBREW POINT") for char in name
        ), key
        assert unicodedata.is_normalized("NFC", name), key
        assert _RANGE_AT_END.search(name) is None, key


def test_the_tables_keys_do_not_meet():
    assert set(display_page.PAGES).isdisjoint(display_page.BLOCK_ONLY_PAGES)


def test_the_pages_of_a_book_show_it_once():
    shown = {}
    for page in display_page.PAGES.values():
        _block_name, verses, _sort_key = display_page.read_page(
            display_page.page_text(page)
        )
        shown.setdefault(page.stem, []).extend(
            (verse.chapter, verse.verse) for verse in verses
        )
    for stem, numerals in shown.items():
        book = _book(stem)
        _osis_id, verses = _mam_simple_verses(book.mam_book)
        held = _record_chapters(stem, book)
        expected = [
            (hvn.INT_TO_STR_DIC[chapter], hvn.INT_TO_STR_DIC[verse])
            for (chapter, verse), _sampe in verses
            if held is None or chapter in held
        ]
        assert numerals == expected, stem


def test_the_disputed_petuhot_are_the_nested_breaks_of_mam_simple():
    found = {}
    for stem in sorted({page.stem for page in display_page.PAGES.values()}):
        osis_id, nested = _nested_breaks(_book(stem).mam_book)
        found |= {(osis_id, *key): note for key, note in nested.items()}
    assert found, "the walk of the pages' books finds no nested break"
    assert found == {
        key: note for key, (note, _letter) in display_page.DISPUTED_PETUHOT.items()
    }


def test_the_decalogue_is_consecutive_verses_of_exodus_20_and_deuteronomy_5():
    by_book = {}
    for (osis_id, chapter, verse), call in display_page.DECALOGUE.items():
        by_book.setdefault(osis_id, []).append((chapter, verse))
        _template, numeral = call
        assert numeral in (None, hvn.INT_TO_STR_DIC[verse]), (osis_id, chapter, verse)
    chapters = {
        osis_id: {chapter for chapter, _verse in keys}
        for osis_id, keys in by_book.items()
    }
    assert chapters == {"Exod": {20}, "Deut": {5}}
    for osis_id, keys in by_book.items():
        verses = [key for key, _sampe in _mam_simple_verses_of(osis_id)]
        start = verses.index(min(keys))
        assert sorted(keys) == verses[start : start + len(keys)], osis_id


def _expected_verses(page):
    """The page's verses as the oracles give them, in display_page.Verse's form."""
    book = _book(page.stem)
    osis_id, verses = _mam_simple_verses(book.mam_book)
    _osis_id, nested = _nested_breaks(book.mam_book)
    bk39id = mam_bknas_and_std_bknas.MAM_HBNP_TO_BK39ID[book.mam_book]
    headings = _headings(page.stem, book)
    expected = []
    for at, ((chapter, verse), sampe) in enumerate(verses):
        if not _on_page(page, (chapter, verse), verses[-1][0][0]):
            continue
        letter = None if at == 0 or sampe is None else _SAMPE_LETTERS[sampe]
        if (chapter, verse) in nested:
            assert (
                letter is None
            ), f"{osis_id} {chapter}:{verse}: two records of a break"
            _note, letter = display_page.DISPUTED_PETUHOT[(osis_id, chapter, verse)]
        heading = None
        if (chapter, verse) in headings:
            heading = (
                wikitext.page_title(book.mam_book, chapter),
                f"{wikitext.HEADING_SECTION}{hvn.INT_TO_STR_DIC[verse]}",
            )
        chapter_parameter = None
        if not expected and verse != 1:
            chapter_parameter = hvn.INT_TO_STR_DIC[chapter]
        expected.append(
            display_page.Verse(
                mam_bknas_and_std_bknas.he_bk39_name(bk39id),
                hvn.INT_TO_STR_DIC[chapter],
                hvn.INT_TO_STR_DIC[verse],
                letter,
                heading,
                chapter_parameter,
                decalogue=display_page.DECALOGUE.get((osis_id, chapter, verse)),
            )
        )
    return expected


def _expected_block_links(expected):
    """The links of a block's line, (anchor, label), as the oracles give them: a topic
    for each verse that has a heading, in order, anchored at its chapter and verse and
    labelled by the transclusion of its heading's section from its base chapter; then
    each chapter of the page, anchored at its first verse there and labelled by its
    numeral."""
    topics = [
        (f"{verse.chapter} {verse.verse}", _transclusion(*verse.heading))
        for verse in expected
        if verse.heading is not None
    ]
    firsts = {}
    for verse in expected:
        firsts.setdefault(verse.chapter, verse.verse)
    chapters = [(f"{chapter} {verse}", chapter) for chapter, verse in firsts.items()]
    return topics + chapters


def _transclusion(target, section):
    """The parser function's call that transcludes the section of the target page."""
    return "{{" + _SECTION_FUNCTION + ":" + target + "|" + section + "}}"


def _on_page(page, key, last_chapter):
    """Whether a verse's (chapter, verse), from its osisID, is on the page: from its first
    chapter's first_verse to its last chapter's last_verse, or that chapter's end."""
    first, last = page.chapters or (1, last_chapter)
    chapter, verse = key
    if key < (first, page.first_verse) or chapter > last:
        return False
    return chapter < last or page.last_verse is None or verse <= page.last_verse


def _book(stem):
    """A page's book, by its stem: a Word file's stem in books.BOOKS, or an OSIS
    abbreviation in base_headings.BOOKS."""
    if stem in books.BOOKS:
        return books.BOOKS[stem]
    return base_headings.BOOKS[stem]


def _record_chapters(stem, book):
    """The numbers of the chapters that a book's tracked record holds, for a book of
    books.BOOKS, whose record may hold only some, as Isaiah's holds 40 to 66; or None,
    for a book of the Torah, whose pages show the whole book."""
    if stem not in books.BOOKS:
        return None
    return {chapter["chapter"] for chapter in tracked.read_record(book)["chapters"]}


def _headings(stem, book):
    """The (chapter, verse) of each verse that has a heading: by the tracked JSON for a
    book of books.BOOKS, and by the book's file of heading places, read by json alone,
    for a book of the Torah."""
    if stem in books.BOOKS:
        return {
            (chapter["chapter"], verse["verse"])
            for chapter in tracked.read_record(book)["chapters"]
            for verse in chapter["verses"]
            if verse["heading"] is not None
        }
    path = paths.in_dir() / "miqra-mevoar-base-headings" / f"{stem}.json"
    record = json.loads(path.read_text(encoding="utf-8"))
    return {
        (chapter["chapter"], verse)
        for chapter in record["chapters"]
        for verse in chapter["headings"]
    }


def _mam_simple_verses(mam_book):
    """A book's OSIS abbreviation, and each of its verses in MAM-simple: its (chapter,
    verse) and starts-with-sampe."""
    bk39id = mam_bknas_and_std_bknas.MAM_HBNP_TO_BK39ID[mam_book]
    osis_id = osis_book_abbrevs.BOOK_ABBREVS[bk39id]
    return osis_id, _mam_simple_verses_of(osis_id)


@functools.cache
def _mam_simple_verses_of(osis_id):
    return tuple(
        (key, verse.get("starts-with-sampe")) for key, verse in _verse_elements(osis_id)
    )


def _nested_breaks(mam_book):
    """A book's OSIS abbreviation, and the note of each break in a scribal-difference
    element of the book, keyed by the (chapter, verse) of the verse after the verse that
    holds it."""
    bk39id = mam_bknas_and_std_bknas.MAM_HBNP_TO_BK39ID[mam_book]
    osis_id = osis_book_abbrevs.BOOK_ABBREVS[bk39id]
    return osis_id, _nested_breaks_of(osis_id)


@functools.cache
def _nested_breaks_of(osis_id):
    elements = _verse_elements(osis_id)
    found = {}
    for at, (key, verse) in enumerate(elements):
        for node in _descendants(verse):
            if node["type"] != "scrdfftar" or not any(
                inner["type"] in _BREAKS for inner in _descendants(node)
            ):
                continue
            notes = [
                part["text"] for part in node["contents"] if part["type"] == "sdt-note"
            ]
            assert len(notes) == 1, f"{osis_id} {key}: {len(notes)} notes"
            assert at + 1 < len(elements), f"{osis_id} {key}: a break after the book"
            after = elements[at + 1][0]
            assert after not in found, f"{osis_id} {after}: two nested breaks"
            found[after] = notes[0]
    return found


def _descendants(node):
    for child in node.get("contents", ()):
        yield child
        yield from _descendants(child)


@functools.cache
def _verse_elements(osis_id):
    """Each verse element of a book in MAM-simple, with its (chapter, verse)."""
    book = _mam_simple_books()[osis_id]
    verses = []
    for chapter in book["contents"]:
        if chapter["type"] in _BREAKS:
            continue
        assert chapter["type"] == "chapter", f"{osis_id}: {chapter['type']}"
        for verse in chapter["contents"]:
            if verse["type"] in _BREAKS:
                continue
            assert verse["type"] == "verse", f"{chapter['osisID']}: {verse['type']}"
            book_id, chapter_number, verse_number = verse["osisID"].split(".")
            assert book_id == osis_id, verse["osisID"]
            verses.append(((int(chapter_number), int(verse_number)), verse))
    assert verses, f"MAM-simple's {osis_id} has no verses"
    return tuple(verses)


@functools.cache
def _mam_simple_books():
    """Every book39 element of MAM-simple, by its osisID."""
    found = {}
    paths_found = sorted(paths.require_mam_simple_vtrad_mam_dir().glob("*.json"))
    assert paths_found, "MAM-simple has no JSON"
    for path in paths_found:
        for item in json.loads(path.read_text(encoding="utf-8"))["contents"]:
            if item["type"] == "book39":
                assert item["osisID"] not in found, item["osisID"]
                found[item["osisID"]] = item
    return found


# The petuha and setuma breaks, which stand between books and chapters too.
_BREAKS = frozenset({"spi-pe2", "spi-pe3", "spi-samekh2", "spi-samekh3"})
# starts-with-sampe takes a break's bare name, and a page gives it as its letter.
_SAMPE_LETTERS = {
    "pe2": "\N{HEBREW LETTER PE}",
    "pe3": "\N{HEBREW LETTER PE}",
    "samekh2": "\N{HEBREW LETTER SAMEKH}",
    "samekh3": "\N{HEBREW LETTER SAMEKH}",
}
# A block's horizontal rule, as on Joshua's first part, the block's model.
_RULE = "-----"
# The parser function by which a page transcludes a section of another page, the
# Labeled Section Transclusion extension's Hebrew name for it.
_SECTION_FUNCTION = "#\N{HEBREW LETTER QOF}\N{HEBREW LETTER TET}\N{HEBREW LETTER AYIN}"
# A link of a block's line, [[#<anchor>|<label>]].
_BLOCK_LINK = re.compile(r"\[\[#([^|\]]+)\|(.+?)\]\]")
# A range in parentheses at the end of a link's label on the main page.
_RANGE_AT_END = re.compile(r"\([^()]*\)\s*$")
