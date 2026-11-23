"""Miqra Mevoar's display pages on Hebrew Wikisource, each a book or a part of one.

A display page, titled DISPLAY_PREFIX and its name, sets each of its verses in MAM's
text beside Rabbi Kokhav's paraphrase from the verse's base chapter, in the form of
Avi's pages for the five megillot. PAGES lists the books and the parts of books, as Avi
divided them, whose base chapters exist: the Torah's five books, three parts each, from
Stage 12 of doc/PLAN-miqra-mevoar.md; Joshua's two parts and five books of the Twelve
from its Stage 10; Micah, Nahum, Habakkuk, Zephaniah, Haggai and Zechariah from its
round 1 of 2026-11-16, and Malachi from its round 2; and Judges' three parts and
Daniel's two from its Stage 11. Their names are those that the main page,
מקרא מבואר, links in revision 3103065, from its section of the Prophets and, for
Daniel's two parts, of the Writings, and, for the Torah's parts, in revision 3103840,
from its section of the Torah, each copied by script, as the comment on PAGES says. A
part's first and last verses are those that its link's label gives, parsed by script,
in revision 3104053 for the first parts of Genesis and of Exodus, whose labels were
corrected by then, as the comment on them says. Obadiah's name has no vav, as Avi's link
and the Word file's title row have it, but its verses name the book as MAM does, with
the vav.
Avi moved Joshua's two parts after Stage 10 created them, and their category lines
still sort them under the names they had then, which PAGES keeps as their sort keys.

Since Stage 13 of the plan, each of the Torah's fifteen parts begins with a block of
title and navigation, in the very same style as the block that Dovi added to Joshua's
first part in revision 3103803: PAGES gives each of them its block_name, the label of
its link in revision 3104053 without the range in parentheses at its end, copied by
script, as the comment on PAGES says, and gives no other page one.

A page's stem names its book: a Word file's stem in books.BOOKS, or an OSIS
abbreviation in base_headings.BOOKS, two sets of keys that must not meet. The places of
its headings come from the tracked JSON, in/miqra-mevoar/, for a book of the first, and
for the Torah, whose base chapters were made before the converter, from base_headings'
records of the headings in those base chapters.

A page with a block_name begins with its block, four lines: the block's line, a
horizontal rule, _BLOCK_RULE, and two blank lines. The block's line is _BLOCK_START, the
block's name and _BLOCK_AFTER_NAME; its topics, joined by _TOPIC_SEPARATOR, each a link,
[[#<chapter> <verse>|<label>]], to a verse of the page that has a heading, in the
page's order, labelled by the very transclusion of the heading that the verse's break
line makes; _BLOCK_AFTER_TOPICS; its chapters, joined by _CHAPTER_SEPARATOR, each a
link, [[#<chapter> <verse>|<chapter>]], to the chapter's first verse on the page, in
the page's order; and _BLOCK_END. Chapters and verses are numerals, and the links reach
the anchors that the verse template and the Decalogue's templates make for their
verses. Those pieces of fixed text are Joshua's, as the comment on them says.

After its block, if it has one, a page has four line shapes and no others: the three of
the megillot's pages, and on the Torah's pages the Decalogue's:

1. A verse: {{מקרא מבואר|<book>|<chapter>|<verse>}}, the book as
   mam_bknas.he_bk39_name names it and the chapter and verse as Hebrew numerals. The
   template sets MAM's verse beside the base chapter's section of the same name, and
   shows the chapter's numeral at its first verse. A page's first verse line, where
   that verse is not its chapter's first, also gives the parameter _CHAPTER_PARAMETER,
   with the chapter's numeral, before its closing braces, as the first verse line of
   Avi's parasha page of Noah does, and the template then shows that numeral at that
   verse. No other line gives the parameter.
2. A verse of the Decalogue: each verse of DECALOGUE, Exodus 20:2 to 20:12 and
   Deuteronomy 5:6 to 5:17, calls instead the template that Avi's page of Yitro or of
   Va'etchanan calls for it, {{<template>|<verse>}} with the verse's numeral, or
   {{<template>}} for the one verse of each Decalogue whose template takes none. Each of
   these templates sets the verse in the strand that MAM-simple calls cant-alef, from
   MAM's page of the Decalogues, where the verse template would set it with both
   strands. No page begins at one of these verses.
3. A break line, before its verse:
   {{פרשה במקרא מבואר|פרשה=<letter>|כותרת={{#קטע:<base chapter>|<section>}}}}.
   The first parameter, pe or samekh, is given where MAM-simple has a petuha or a
   setuma between the verse and the one before it in the same book, and the second
   where the verse has a heading: both, in that order, where both apply, and no line
   where neither does. A petuha that MAM-simple nests in a scribal-difference element,
   with a note on it, has the first parameter that DISPUTED_PETUHOT gives it: pe alone
   before Exodus 34:1, and before Leviticus 7:22 and 7:28 pe with Avi's note on it, as
   his page of Tzav has them. The heading is not copied: the line transcludes it from
   the verse's base chapter, the title that wikitext.page_title gives, by the section
   that wraps it there, wikitext.HEADING_SECTION and the verse's numeral. A break
   inside a verse gets no line, since MAM's verse shows it.
4. The end: a blank line, then the category line, [[קטגוריה:מקרא מבואר|<name>]], whose
   sort key is the page's own name, as each megillah's page has its own, or the sort key
   that PAGES gives it.

page_text generates a page in NFC with no final newline, exactly as a save stores it.
read_page, a closed parser of the block and the four shapes, reads a page back as its
block's name, or None, its verses and its category's sort key, and raises on any other
line; on a block anywhere but a page's first four lines, or in any other shape; on a
block whose topics are not the page's headings, in order, with the same transclusions,
or whose chapters are not the page's chapters at their first verses on the page; on
the chapter parameter anywhere that item 1 does not put it; on a verse line at a verse
to which item 2 gives a Decalogue line, and on a Decalogue line anywhere else; and on a
disputed petuha's first parameter before any verse but its own.
"""

import dataclasses
import re
import unicodedata

from mb_cmn import hebrew_verse_numerals as hvn
from miqra_mevoar import base_headings
from miqra_mevoar import books
from miqra_mevoar import mam_simple
from miqra_mevoar import tracked
from miqra_mevoar import wikitext


@dataclasses.dataclass(frozen=True)
class Page:
    """One display page: its key, its name after DISPLAY_PREFIX, its book, its chapters
    and the verses in them at which it begins and ends, its category line's sort key
    where that is not its name, and its block's name where it has a block."""

    key: str
    name: str
    # Its book's key: a Word file's stem in books.BOOKS, or an OSIS abbreviation in
    # base_headings.BOOKS.
    stem: str
    # The first and last chapters of a part of a book, or None for the whole book.
    chapters: tuple[int, int] | None = None
    # The sort key of the page's category line, or None for the page's own name.
    sort_key: str | None = None
    # The verse of its first chapter at which the page begins, and the verse of its last
    # chapter at which it ends, or None for that chapter's last verse.
    first_verse: int = 1
    last_verse: int | None = None
    # The part's name in its block of title and navigation, or None for a page without
    # a block.
    block_name: str | None = None

    def title(self) -> str:
        """The page's title on Wikisource."""
        return f"{DISPLAY_PREFIX}{self.name}"

    def category_sort_key(self) -> str:
        """The sort key of the page's category line: sort_key, or else its name."""
        return self.name if self.sort_key is None else self.sort_key


@dataclasses.dataclass(frozen=True)
class Verse:
    """A verse's line on a display page, with what the break line before it gives."""

    book: str
    chapter: str
    verse: str
    # The break line's first parameter, PE or SAMEKH, or a disputed petuha's in
    # DISPUTED_PETUHOT, where a petuha or a setuma comes before the verse, and its
    # heading's transclusion, (target, section), where it has a heading.
    letter: str | None = None
    heading: tuple[str, str] | None = None
    # The chapter's numeral, which a page's first verse line gives as _CHAPTER_PARAMETER
    # where that verse is not its chapter's first, or None.
    chapter_parameter: str | None = None
    # Where the verse's line calls a Decalogue template instead of the verse template,
    # that template and the numeral that it takes, or None, as DECALOGUE gives them.
    decalogue: tuple[str, str | None] | None = None


def page_text(page):
    """A display page's text, exactly as a save stores it."""
    return _text(page.block_name, page_verses(page), page.category_sort_key())


def block_line(name, topics, chapters):
    """A block's line: the part's name; its topics, each ((chapter, verse), label), the
    numerals of the verse before which its heading stands and its link's label; and its
    chapters, each (chapter, verse), the numerals of the chapter and of its first verse
    on the page, each linked by the chapter's numeral. The name, a template's parameter,
    must be plain text, as _BLOCK_NAME and wikitext.wikitext_hazards allow it."""
    if _BLOCK_NAME.fullmatch(name) is None or wikitext.wikitext_hazards(name):
        raise ValueError(f"A block's name is not plain text: {name!r}")
    if not topics or not chapters:
        raise ValueError(f"The block of {name!r} has no topic or no chapter")
    return "".join(
        (
            _BLOCK_START,
            name,
            _BLOCK_AFTER_NAME,
            _TOPIC_SEPARATOR.join(_anchor_link(*topic) for topic in topics),
            _BLOCK_AFTER_TOPICS,
            _CHAPTER_SEPARATOR.join(
                _anchor_link(anchor, anchor[0]) for anchor in chapters
            ),
            _BLOCK_END,
        )
    )


def page_verses(page):
    """The verses of a display page, each with what the break line before it gives."""
    book = book_of_stem(page.stem)
    keys, page_keys = _page_keys(page, book)
    breaks = mam_simple.verse_breaks(book)
    letters = {key: _LETTERS[kind] for key, kind in breaks.items()}
    letters |= _disputed_letters(book, breaks)
    headings = _heading_keys(page.stem, book, keys)
    decalogue = _decalogue(book, keys)
    verses = []
    for chapter, verse in page_keys:
        heading = None
        if (chapter, verse) in headings:
            section = f"{wikitext.HEADING_SECTION}{hvn.INT_TO_STR_DIC[verse]}"
            heading = wikitext.page_title(book.mam_book, chapter), section
        # The page's first verse numbers its chapter where the template would not.
        chapter_parameter = None
        if not verses and verse != 1:
            chapter_parameter = hvn.INT_TO_STR_DIC[chapter]
        if not verses and (chapter, verse) in decalogue:
            raise ValueError(f"{page.key} would begin at a verse of the Decalogue")
        verses.append(
            Verse(
                book.bk39_name(),
                hvn.INT_TO_STR_DIC[chapter],
                hvn.INT_TO_STR_DIC[verse],
                letters.get((chapter, verse)),
                heading,
                chapter_parameter,
                decalogue.get((chapter, verse)),
            )
        )
    return verses


def book_of_stem(stem):
    """The book that a page's stem names: a Word file's stem in books.BOOKS, or an OSIS
    abbreviation in base_headings.BOOKS."""
    if stem in books.BOOKS:
        return books.BOOKS[stem]
    if stem in base_headings.BOOKS:
        return base_headings.BOOKS[stem]
    raise ValueError(f"No display page's book has the stem {stem!r}")


def read_page(text):
    """A page's block's name, or None, its verses and its category's sort key; raise on
    any line of another shape."""
    lines = text.split("\n")
    if len(lines) < 3 or lines[-2] != "":
        raise ValueError("A display page ends in a blank line and its category line")
    category = _CATEGORY_LINE.fullmatch(lines[-1])
    if category is None:
        raise ValueError(f"{lines[-1]!r} is not a display page's category line")
    block, body = _read_block(lines[:-2])
    verses, pending = [], None
    for line in body:
        if match := _BREAK_LINE.fullmatch(line):
            letter, target, section = match.groups()
            if letter is None and target is None:
                raise ValueError(f"{line!r} is a break line with neither parameter")
            if pending is not None:
                raise ValueError(f"{line!r} follows a break line")
            pending = letter, None if target is None else (target, section)
            continue
        if match := _VERSE_LINE.fullmatch(line):
            book, chapter, verse, chapter_parameter = match.groups()
            if (book, chapter, verse) in _DECALOGUE_BY_NAMES:
                raise ValueError(
                    f"{line!r} is a verse line at a verse of the Decalogue"
                )
            if chapter_parameter is not None:
                _check_chapter_parameter(
                    line, verses, chapter, verse, chapter_parameter
                )
            decalogue = None
        elif match := _DECALOGUE_LINE.fullmatch(line):
            decalogue = match.groups()
            book, chapter, verse = _decalogue_verse(line, verses, decalogue)
            chapter_parameter = None
        else:
            raise ValueError(f"{line!r} is none of a display page's line shapes")
        letter, heading = pending or (None, None)
        if letter in _DISPUTED_LETTERS and (
            _DISPUTED_BY_NAMES.get((book, chapter, verse)) != letter
        ):
            raise ValueError(f"{line!r} follows another verse's disputed petuha")
        verses.append(
            Verse(book, chapter, verse, letter, heading, chapter_parameter, decalogue)
        )
        pending = None
    if pending is not None:
        raise ValueError("A display page's last break line has no verse after it")
    if not verses:
        raise ValueError("A display page has no verse")
    block_name = None if block is None else _check_block(block, verses)
    if _text(block_name, verses, category.group(1)) != text:
        raise ValueError("A display page does not read back as itself")
    return block_name, verses, category.group(1)


def _read_block(lines):
    """A page's block, as its name, its topics and its chapters, and the page's lines
    after it; or None and all the lines, where the first line is not a block's line. A
    block is only a page's first four lines: its line, the rule and two blank lines."""
    match = _BLOCK_LINE.fullmatch(lines[0])
    if match is None:
        return None, lines
    if lines[1:4] != [_BLOCK_RULE, "", ""]:
        raise ValueError(
            "A block's line is not followed by its rule and two blank lines"
        )
    name, topics, chapters = match.groups()
    return (
        name,
        _read_links(topics, _TOPIC_SEPARATOR, _TOPIC_LINK),
        _read_links(chapters, _CHAPTER_SEPARATOR, _CHAPTER_LINK),
    ), lines[4:]


def _read_links(text, separator, link):
    """The groups of each link of a block's topics or chapters; raise unless the text is
    those links and the separator between each two of them."""
    found = []
    for item in text.split(separator):
        match = link.fullmatch(item)
        if match is None:
            raise ValueError(f"{item!r} is not a link of a block's line")
        found.append(match.groups())
    return found


def _check_block(block, verses):
    """A block's name; raise unless its topics are the page's headings, in order, each
    at its verse and with its break line's transclusion, and its chapters the page's
    chapters, each at its first verse on the page and named by its numeral."""
    name, topics, chapters = block
    headings = [
        (verse.chapter, verse.verse, *verse.heading)
        for verse in verses
        if verse.heading is not None
    ]
    if topics != headings:
        raise ValueError(f"The block of {name!r} has topics other than its headings")
    expected = [(chapter, verse, chapter) for chapter, verse in _first_verses(verses)]
    if chapters != expected:
        raise ValueError(
            f"The block of {name!r} has chapters other than its page's first verses"
        )
    return name


def _check_chapter_parameter(line, verses, chapter, verse, chapter_parameter):
    """Raise unless a verse line gives the chapter parameter where a page may give it:
    on its first verse line, with that line's chapter, at a verse other than alef."""
    if verses:
        raise ValueError(f"{line!r} numbers its chapter but is not the first verse")
    if chapter_parameter != chapter:
        raise ValueError(f"{line!r} numbers a chapter other than its own")
    if verse == hvn.INT_TO_STR_DIC[1]:
        raise ValueError(f"{line!r} numbers its chapter at the chapter's first verse")


def _page_keys(page, book):
    """The book's (chapter, verse) keys, and the page's, from first bound to last."""
    keys = mam_simple.verse_keys(book)
    numbers = list(dict.fromkeys(chapter for chapter, _verse in keys))
    if numbers != list(range(1, len(numbers) + 1)):
        raise ValueError(f"{book.osis_id}: MAM-simple's chapters are {numbers}")
    first, last = page.chapters or (1, len(numbers))
    if not 1 <= first <= last <= len(numbers):
        raise ValueError(
            f"{page.key}: chapters {first} to {last} are not within the book's"
            f" {len(numbers)}"
        )
    last_verses = [verse for chapter, verse in keys if chapter == last]
    start = first, page.first_verse
    end = last, last_verses[-1] if page.last_verse is None else page.last_verse
    for bound in (start, end):
        if bound not in keys:
            raise ValueError(f"{page.key}: {bound} is not a verse of {book.osis_id}")
    page_keys = [key for key in keys if start <= key <= end]
    if not page_keys or page_keys != keys[keys.index(start) : keys.index(end) + 1]:
        raise ValueError(
            f"{page.key} would not run from {start} to {end} in MAM-simple's order"
        )
    return keys, page_keys


def _decalogue_verse(line, verses, call):
    """The book, chapter and verse of a Decalogue line: the verse after that of the line
    before it, which must be the verse to which DECALOGUE gives this call."""
    if not verses:
        raise ValueError(f"{line!r} would begin a page")
    before = verses[-1]
    names = (
        before.book,
        before.chapter,
        hvn.INT_TO_STR_DIC[hvn.STR_TO_INT_DIC[before.verse] + 1],
    )
    if _DECALOGUE_BY_NAMES.get(names) != call:
        raise ValueError(f"{line!r} is not the line of the verse after {before}")
    return names


def _decalogue(book, keys):
    """The Decalogue's call of each verse of the book to which DECALOGUE gives one, by
    key; raise if one of those is not a verse of the book in MAM-simple."""
    found = {
        (chapter, verse): call
        for (osis_id, chapter, verse), call in DECALOGUE.items()
        if osis_id == book.osis_id
    }
    if strays := sorted(set(found) - set(keys)):
        raise ValueError(f"{book.osis_id}: DECALOGUE's {strays} are not MAM's verses")
    return found


def _disputed_letters(book, breaks):
    """The first parameter of the break line before each verse after a petuha that
    MAM-simple nests in a scribal-difference element, by key, as DISPUTED_PETUHOT gives
    it; raise unless the table has exactly those verses of the book, with MAM's notes.
    """
    notes = mam_simple.scribal_difference_breaks(book)
    table = {
        (chapter, verse): entry
        for (osis_id, chapter, verse), entry in DISPUTED_PETUHOT.items()
        if osis_id == book.osis_id
    }
    if set(notes) != set(table):
        raise ValueError(
            f"{book.osis_id}: MAM-simple nests a break before {sorted(notes)},"
            f" DISPUTED_PETUHOT before {sorted(table)}"
        )
    letters = {}
    for key, note in notes.items():
        table_note, letter = table[key]
        if note != table_note or breaks[key] != mam_simple.PETUHA:
            raise ValueError(
                f"{book.osis_id} {key}: MAM-simple's nested break or its note is not"
                " DISPUTED_PETUHOT's"
            )
        letters[key] = letter
    return letters


def _heading_keys(stem, book, keys):
    """The keys of the verses that have a heading: in the tracked JSON for a book of
    books.BOOKS, and in base_headings' record for a book of the Torah."""
    if stem in books.BOOKS:
        return _tracked_heading_keys(book, keys)
    if stem in base_headings.BOOKS:
        return _base_heading_keys(book, keys)
    raise ValueError(f"No display page's book has the stem {stem!r}")


def _base_heading_keys(book, keys):
    """The keys of the verses that base_headings' record of the book gives a heading."""
    record = base_headings.read_record(book)
    numbers = list(dict.fromkeys(chapter for chapter, _verse in keys))
    if [chapter["chapter"] for chapter in record["chapters"]] != numbers:
        raise ValueError(f"{book.abbreviation}: the record's chapters are not MAM's")
    found = {
        (chapter["chapter"], verse)
        for chapter in record["chapters"]
        for verse in chapter["headings"]
    }
    if strays := sorted(found - set(keys)):
        raise ValueError(f"{book.abbreviation}: headings before {strays}, not verses")
    return found


def _tracked_heading_keys(book, keys):
    """The keys of the verses that the tracked JSON gives a heading."""
    record = tracked.read_record(book)
    tracked_keys = [
        (chapter["chapter"], verse["verse"])
        for chapter in record["chapters"]
        for verse in chapter["verses"]
    ]
    if tracked_keys != keys:
        raise ValueError(f"{book.stem}: the tracked JSON's verses are not MAM-simple's")
    return {
        (chapter["chapter"], verse["verse"])
        for chapter in record["chapters"]
        for verse in chapter["verses"]
        if verse["heading"] is not None
    }


def _text(block_name, verses, sort_key):
    lines = [] if block_name is None else _block(block_name, verses)
    for verse in verses:
        if verse.letter is not None or verse.heading is not None:
            lines.append(_break_line(verse.letter, verse.heading))
        if verse.decalogue is not None:
            if verse.chapter_parameter is not None:
                raise ValueError(f"{verse} numbers its chapter on a Decalogue line")
            template, numeral = verse.decalogue
            lines.append(
                _template_line(template, *([] if numeral is None else [numeral]))
            )
            continue
        parameters = [verse.book, verse.chapter, verse.verse]
        if verse.chapter_parameter is not None:
            parameters.append(f"{_CHAPTER_PARAMETER}={verse.chapter_parameter}")
        lines.append(_template_line(_VERSE_TEMPLATE, *parameters))
    lines.extend(["", _category_line(sort_key)])
    text = "\n".join(lines)
    if not unicodedata.is_normalized("NFC", text):
        raise ValueError(
            "A display page's text is not in NFC, the form MediaWiki stores"
        )
    return text


def _block(name, verses):
    """A page's block, its four lines: its line, the rule and two blank lines. Its topics
    are the page's verses that have a heading, each labelled by its break line's
    transclusion of it, and its chapters the page's, each at its first verse there."""
    topics = [
        ((verse.chapter, verse.verse), _transclusion(*verse.heading))
        for verse in verses
        if verse.heading is not None
    ]
    return [block_line(name, topics, _first_verses(verses)), _BLOCK_RULE, "", ""]


def _first_verses(verses):
    """The (chapter, verse) numerals of each chapter's first verse among verses, in
    order."""
    firsts = {}
    for verse in verses:
        firsts.setdefault(verse.chapter, verse.verse)
    return list(firsts.items())


def _anchor_link(anchor, label):
    """A link to the anchor that the verse template makes at a verse, by its chapter's
    and its verse's numerals."""
    chapter, verse = anchor
    return f"[[#{chapter} {verse}|{label}]]"


def _break_line(letter, heading):
    parameters = []
    if letter is not None:
        parameters.append(f"{_BREAK_PARAMETER}={letter}")
    if heading is not None:
        parameters.append(f"{_HEADING_PARAMETER}={_transclusion(*heading)}")
    return _template_line(_BREAK_TEMPLATE, *parameters)


def _transclusion(target, section):
    """The transclusion of a heading's section from its base chapter."""
    return "{{" + _SECTION_FUNCTION + ":" + target + "|" + section + "}}"


def _template_line(name, *parameters):
    return "{{" + "|".join((name, *parameters)) + "}}"


def _category_line(name):
    """The category line of the base chapters, wikitext.CATEGORY, with a sort key."""
    if not (wikitext.CATEGORY.startswith("[[") and wikitext.CATEGORY.endswith("]]")):
        raise ValueError(f"{wikitext.CATEGORY!r} is not a category link")
    return f"{wikitext.CATEGORY[:-2]}|{name}]]"


def _verse_names(key):
    """A verse of the Torah, (OSIS id, chapter, verse), as a page's lines name it: by
    MAM's name of its book and the numerals of its chapter and verse."""
    osis_id, chapter, verse = key
    (book,) = [book for book in base_headings.BOOKS.values() if book.osis_id == osis_id]
    return book.bk39_name(), hvn.INT_TO_STR_DIC[chapter], hvn.INT_TO_STR_DIC[verse]


PE = "\N{HEBREW LETTER PE}"
SAMEKH = "\N{HEBREW LETTER SAMEKH}"
_LETTERS = {mam_simple.PETUHA: PE, mam_simple.SETUMA: SAMEKH}
# A page's stem names a book of one of these tables, never of both.
if not set(books.BOOKS).isdisjoint(base_headings.BOOKS):
    raise ValueError("books.BOOKS and base_headings.BOOKS share a key")
# The title prefix and the names, as the links of the main page give them in revision
# 3103065, in its section of the Prophets and, for Daniel's, of the Writings, and in
# revision 3103840, for the Torah's, in its section of the Torah. Stage 10 copied the
# prefix and its names by script from revision 3101310, except Amos's, MAM's name of the
# book, and each equals 3101507's link; round 1 copied Joshua's new names and the six
# later names from 3101507 by script, and round 2 Malachi's from 3103065. Stage 11
# copied the names of Judges' three parts and Daniel's two from 3103065 by script, and
# parsed each part's first and last verses from its link's label. Stage 12 copied the
# names of the Torah's fifteen parts from 3103840 by script, and parsed each part's
# first and last verses from its link's label, but for the first parts of Genesis and
# of Exodus, as the comment on them says; the labels of revision 3104053, parsed by
# script, give all fifteen parts their ranges here.
# Joshua's sort keys are the names under which Stage 10 created its two pages.
# Stage 13 copied by script each of the Torah's fifteen parts' block_name, its link's
# label in revision 3104053 without the range in parentheses at the label's end; each
# is pointed and in NFC, as MediaWiki stores it. No other entry has a block_name.
DISPLAY_PREFIX = "מקרא מבואר/תצוגה/"
PAGES = {
    page.key: page
    for page in (
        # By decision 1a of Stage 12, the first parts of Genesis and of Exodus end
        # where their second parts begin, though the labels of revision 3103840
        # ended them at chapters 12 and 11, so that every verse is on a page; the
        # two labels have given these ranges since revision 3104053.
        Page(
            "gen-1",
            "ספר בראשית 1",
            "Gen",
            (1, 11),
            block_name="סֵפֶר בְּרֵאשִׁית, חֵלֶק רִאשׁוֹן: רֵאשִׁית הָאָדָם",
        ),
        Page(
            "gen-2",
            "ספר בראשית 2",
            "Gen",
            (12, 36),
            block_name="סֵפֶר בְּרֵאשִׁית, חֵלֶק שֵׁנִי: אֲבוֹת יִשְׂרָאֵל",
        ),
        Page(
            "gen-3",
            "ספר בראשית 3",
            "Gen",
            (37, 50),
            block_name="סֵפֶר בְּרֵאשִׁית, חֵלֶק שְׁלִישִׁי: בְּנֵי יִשְׂרָאֵל",
        ),
        # Exodus' first part, by decision 1a, as gen-1's comment says.
        Page(
            "exod-1",
            "ספר שמות 1",
            "Exod",
            (1, 17),
            block_name="סֵפֶר שְׁמוֹת, חֵלֶק רִאשׁוֹן: מִשִּׁעְבּוּד לִגְאֻלָּה",
        ),
        Page(
            "exod-2",
            "ספר שמות 2",
            "Exod",
            (18, 24),
            block_name="סֵפֶר שְׁמוֹת, חֵלֶק שֵׁנִי: מַעֲמַד הַר סִינַי",
        ),
        Page(
            "exod-3",
            "ספר שמות 3",
            "Exod",
            (25, 40),
            block_name="סֵפֶר שְׁמוֹת, חֵלֶק שְׁלִישִׁי: מְלֶאכֶת הַמִּשְׁכָּן",
        ),
        Page(
            "lev-1",
            "ספר ויקרא 1",
            "Lev",
            (1, 10),
            block_name="סֵפֶר וַיִּקְרָא, חֵלֶק רִאשׁוֹן: עֲבוֹדַת ה'",
        ),
        Page(
            "lev-2",
            "ספר ויקרא 2",
            "Lev",
            (11, 18),
            block_name="סֵפֶר וַיִּקְרָא, חֵלֶק שֵׁנִי: טֻמְאָה וְטָהֳרָה",
        ),
        Page(
            "lev-3",
            "ספר ויקרא 3",
            "Lev",
            (19, 27),
            block_name="סֵפֶר וַיִּקְרָא, חֵלֶק שְׁלִישִׁי: קְדֻשָּׁה",
        ),
        Page(
            "num-1",
            "ספר במדבר 1",
            "Num",
            (1, 10),
            block_name="סֵפֶר בְּמִדְבַּר, חֵלֶק רִאשׁוֹן: \"עַל פִּי ה' יַחֲנוּ וְעַל פִּי ה' יִסָּעוּ\"",
        ),
        Page(
            "num-2",
            "ספר במדבר 2",
            "Num",
            (11, 22),
            last_verse=1,
            block_name='סֵפֶר בְּמִדְבַּר, חֵלֶק שֵׁנִי: "וַיָּרֶב הָעָם"',
        ),
        Page(
            "num-3",
            "ספר במדבר 3",
            "Num",
            (22, 36),
            first_verse=2,
            block_name='סֵפֶר בְּמִדְבַּר, חֵלֶק שְׁלִישִׁי: "בְּעַרְבֹת מוֹאָב עַל יַרְדֵּן יְרֵחוֹ"',
        ),
        Page(
            "deut-1",
            "ספר דברים 1",
            "Deut",
            (1, 11),
            last_verse=25,
            block_name='סֵפֶר דְּבָרִים, חֵלֶק רִאשׁוֹן: "שְׁמַע יִשְׂרָאֵל"',
        ),
        Page(
            "deut-2",
            "ספר דברים 2",
            "Deut",
            (11, 26),
            first_verse=26,
            block_name="סֵפֶר דְּבָרִים, חֵלֶק שֵׁנִי: הַחֻקִּים וְהַמִּשְׁפָּטִים",
        ),
        Page(
            "deut-3",
            "ספר דברים 3",
            "Deut",
            (27, 34),
            block_name="סֵפֶר דְּבָרִים, חֵלֶק שְׁלִישִׁי: דִּבְרֵי מֹשֶׁה הָאַחֲרוֹנִים",
        ),
        Page("yehoshua-1", "ספר יהושע 1", "yehoshua", (1, 12), sort_key="ספר יהושע א"),
        Page("yehoshua-2", "ספר יהושע 2", "yehoshua", (13, 24), sort_key="ספר יהושע ב"),
        Page("sephershoftim-1", "ספר שופטים 1", "sephershoftim", (1, 2), last_verse=5),
        Page(
            "sephershoftim-2", "ספר שופטים 2", "sephershoftim", (2, 16), first_verse=6
        ),
        Page("sephershoftim-3", "ספר שופטים 3", "sephershoftim", (17, 21)),
        Page("hoshea", "הושע", "hoshea"),
        Page("yoel", "יואל", "yoel"),
        Page("amos", "עמוס", "amos"),
        Page("ovadya", "עבדיה", "ovadya"),
        Page("yona", "יונה", "yona"),
        Page("mikha", "מיכה", "mikha"),
        Page("nahum", "נחום", "nahum"),
        Page("havaquq", "חבקוק", "havaquq"),
        Page("tzefanya", "צפניה", "tzefanya"),
        Page("hagay", "חגי", "hagay"),
        Page("zekharya", "זכריה", "zekharya"),
        Page("malakhi", "מלאכי", "malakhi"),
        Page("daniyel-1", "ספר דניאל 1", "daniyel", (1, 6)),
        Page("daniyel-2", "ספר דניאל 2", "daniyel", (7, 12)),
    )
}
# The templates, their parameters and the section function, copied by script from the
# megillot's display pages as read on 2026-11-04 and checked against the templates' own
# text, except the verse template's chapter parameter, which Stage 11 copied by script
# from the first verse line of the parasha page of Noah, revision 964086, and checked
# against the template's text in revision 2852518.
_VERSE_TEMPLATE = "מקרא מבואר"
_CHAPTER_PARAMETER = "פרק"
_BREAK_TEMPLATE = "פרשה במקרא מבואר"
_BREAK_PARAMETER = "פרשה"
_HEADING_PARAMETER = "כותרת"
_SECTION_FUNCTION = "#קטע"
# The fixed text of a block's line, copied by script from the first line of Joshua's
# first part in revision 3103803, the block that Dovi added there, and divided as Stage
# 13 of the plan divides it; it is in NFC, as MediaWiki stores it. Before the part's
# name: a template's call, two templates' openings and the opening of bold. After it:
# the close of the bold and of the inner template, a template's call, and bold opened
# again on the word for topics, a colon and a space. Between two topics. After the
# topics: the close of the bold, the same template's call, and a parenthesis opened on
# the word for chapters, a colon and a space. Between two chapters. After the chapters:
# the close of the parenthesis and of the outer template, and one more template's call.
_BLOCK_START = "{{מ:טעמי המקרא|15}}{{מרכז|{{ג|'''"
_BLOCK_AFTER_NAME = "'''}}{{ש}}'''נוֹשְׂאִים: "
_TOPIC_SEPARATOR = " · "
_BLOCK_AFTER_TOPICS = "'''{{ש}}(פרקים: "
_CHAPTER_SEPARATOR = ", "
_BLOCK_END = ")}}{{מ:טעמי המקרא-סוף}}"
# The block's second line, a horizontal rule, before its two blank lines.
_BLOCK_RULE = "-----"
# The Decalogue's templates, copied by script from Avi's pages of Yitro, revision
# 962744, and of Va'etchanan, revision 962961: on each page, the template that its
# verses of the Decalogue call with their numerals, and the one that Exodus 20:12, or
# Deuteronomy 5:16, calls with none.
_YITRO = "מקרא מבואר/עשרת הדברות יתרו"
_YITRO_12 = "מקרא מבואר/עשרת הדברות יתרו יב"
_VAETCHANAN = "מקרא מבואר/עשרת הדברות ואתחנן"
_VAETCHANAN_16 = "מקרא מבואר/עשרת הדברות ואתחנן טז"
# The verses of the Decalogue, by (OSIS id, chapter, verse), each with the template that
# its line calls and the numeral that the template takes, or None, as Avi's pages of
# Yitro and Va'etchanan give them.
DECALOGUE = {
    **{
        ("Exod", 20, verse): (_YITRO, hvn.INT_TO_STR_DIC[verse])
        for verse in range(2, 12)
    },
    ("Exod", 20, 12): (_YITRO_12, None),
    **{
        ("Deut", 5, verse): (_VAETCHANAN, hvn.INT_TO_STR_DIC[verse])
        for verse in (*range(6, 16), 17)
    },
    ("Deut", 5, 16): (_VAETCHANAN_16, None),
}
# The petuhot that MAM-simple nests in a scribal-difference element, by the (OSIS id,
# chapter, verse) of the verse after each, with MAM's note on it, copied by script from
# MAM-simple, and the first parameter of its break line, as Avi's pages have it: the
# petuha alone before Exodus 34:1, as on his page of Ki Tisa, revision 966044, and
# before Leviticus 7:22 and 7:28 the petuha with his note on it, copied by script from
# his page of Tzav, revision 966718.
DISPUTED_PETUHOT = {
    ("Exod", 34, 1): ("ספק פרשה סתומה בכתר ארם צובה", PE),
    ("Lev", 7, 22): ("אין פרשה בספרי ספרד ואשכנז", "פ (בספרי תימן)"),
    ("Lev", 7, 28): ("אין פרשה בספרי תימן", "פ (בספרי ספרד ואשכנז)"),
}
# The first parameters of a break line that stand for a petuha.
PETUHA_LETTERS = frozenset(
    {PE, *(letter for _note, letter in DISPUTED_PETUHOT.values())}
)
# DECALOGUE's verses and DISPUTED_PETUHOT's, as a page's lines name them.
_DECALOGUE_BY_NAMES = {_verse_names(key): call for key, call in DECALOGUE.items()}
_DISPUTED_BY_NAMES = {
    _verse_names(key): letter for key, (_note, letter) in DISPUTED_PETUHOT.items()
}
# The first parameters of a break line that only a disputed petuha's verse may have.
_DISPUTED_LETTERS = frozenset(_DISPUTED_BY_NAMES.values()) - {PE, SAMEKH}
_BREAK_LETTERS = sorted(
    {PE, SAMEKH, *_DISPUTED_LETTERS}, key=lambda letter: (-len(letter), letter)
)
_DECALOGUE_TEMPLATES = sorted(
    {template for template, _numeral in DECALOGUE.values()},
    key=lambda template: (-len(template), template),
)
_ARGUMENT = r"([^|{}\[\]=\n]+)"
_VERSE_LINE = re.compile(
    r"\{\{"
    + re.escape(_VERSE_TEMPLATE)
    + (r"\|" + _ARGUMENT) * 3
    + r"(?:\|"
    + re.escape(_CHAPTER_PARAMETER)
    + "="
    + _ARGUMENT
    + r")?\}\}"
)
_DECALOGUE_LINE = re.compile(
    r"\{\{("
    + "|".join(re.escape(template) for template in _DECALOGUE_TEMPLATES)
    + r")(?:\|"
    + _ARGUMENT
    + r")?\}\}"
)
_BREAK_LINE = re.compile(
    r"\{\{"
    + re.escape(_BREAK_TEMPLATE)
    + r"(?:\|"
    + re.escape(_BREAK_PARAMETER)
    + "=("
    + "|".join(re.escape(letter) for letter in _BREAK_LETTERS)
    + "))?"
    + r"(?:\|"
    + re.escape(_HEADING_PARAMETER)
    + r"=\{\{"
    + re.escape(_SECTION_FUNCTION)
    + ":"
    + _ARGUMENT
    + r"\|"
    + _ARGUMENT
    + r"\}\})?\}\}"
)
_CATEGORY_LINE = re.compile(
    re.escape(wikitext.CATEGORY[:-2]) + r"\|" + _ARGUMENT + r"\]\]"
)
# A block's name, which holds no bracket, brace, pipe, tag, equals sign or line break,
# and a block's line: its name, and the text of its topics and of its chapters, which
# _read_links reads.
_BLOCK_NAME = re.compile(r"[^\[\]{}|<>=\n]+")
_BLOCK_LINE = re.compile(
    re.escape(_BLOCK_START)
    + "("
    + _BLOCK_NAME.pattern
    + ")"
    + re.escape(_BLOCK_AFTER_NAME)
    + "(.+?)"
    + re.escape(_BLOCK_AFTER_TOPICS)
    + "(.+?)"
    + re.escape(_BLOCK_END)
)
# A chapter's or a verse's numeral in a block's anchor, and a block's links: a topic's,
# labelled by its heading's transclusion, and a chapter's, labelled by its numeral.
_NUMERAL = r"([^\s|{}\[\]=#]+)"
_ANCHOR = r"\[\[#" + _NUMERAL + " " + _NUMERAL + r"\|"
_TOPIC_LINK = re.compile(
    _ANCHOR
    + r"\{\{"
    + re.escape(_SECTION_FUNCTION)
    + ":"
    + _ARGUMENT
    + r"\|"
    + _ARGUMENT
    + r"\}\}\]\]"
)
_CHAPTER_LINK = re.compile(_ANCHOR + _NUMERAL + r"\]\]")
