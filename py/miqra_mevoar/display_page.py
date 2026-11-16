"""Miqra Mevoar's display pages on Hebrew Wikisource, each a book or a part of one.

A display page, titled DISPLAY_PREFIX and its name, sets each of its verses in MAM's
text beside Rabbi Kokhav's paraphrase from the verse's base chapter, in the form of
Avi's pages for the five megillot. PAGES lists the books and the parts of books, as Avi
divided them, whose base chapters exist: Joshua's two parts and five books of the Twelve
from Stage 10 of doc/PLAN-miqra-mevoar.md; Micah, Nahum, Habakkuk, Zephaniah, Haggai and
Zechariah from its round 1 of 2026-11-16, and Malachi from its round 2; and Judges' three
parts and Daniel's two from its Stage 11. Their names are those that the main page,
מקרא מבואר, links in revision 3103065, from its section of the Prophets and, for
Daniel's two parts, of the Writings, each copied by script, as the comment on PAGES
says; a part's first and last verses are those that its link's label gives, parsed by
script. Obadiah's name has no vav, as Avi's link and the Word file's title row have it,
but its verses name the book as MAM does, with the vav.
Avi moved Joshua's two parts after Stage 10 created them, and their category lines
still sort them under the names they had then, which PAGES keeps as their sort keys.

A page has three line shapes and no others, as the megillot's pages have:

1. A verse: {{מקרא מבואר|<book>|<chapter>|<verse>}}, the book as
   mam_bknas.he_bk39_name names it and the chapter and verse as Hebrew numerals. The
   template sets MAM's verse beside the base chapter's section of the same name, and
   shows the chapter's numeral at its first verse. A page's first verse line, where
   that verse is not its chapter's first, also gives the parameter _CHAPTER_PARAMETER,
   with the chapter's numeral, before its closing braces, as the first verse line of
   Avi's parasha page of Noah does, and the template then shows that numeral at that
   verse. No other line gives the parameter.
2. A break line, before its verse:
   {{פרשה במקרא מבואר|פרשה=<letter>|כותרת={{#קטע:<base chapter>|<section>}}}}.
   The first parameter, pe or samekh, is given where MAM-simple has a petuha or a
   setuma between the verse and the one before it in the same book, and the second
   where the tracked JSON gives the verse a heading: both, in that order, where both
   apply, and no line where neither does. The heading is not copied: the line
   transcludes it from the verse's base chapter, the title that wikitext.page_title
   gives, by the section that wraps it there, wikitext.HEADING_SECTION and the verse's
   numeral. A break inside a verse gets no line, since MAM's verse shows it.
3. The end: a blank line, then the category line, [[קטגוריה:מקרא מבואר|<name>]], whose
   sort key is the page's own name, as each megillah's page has its own, or the sort key
   that PAGES gives it.

page_text generates a page in NFC with no final newline, exactly as a save stores it.
read_page, a closed parser of the three shapes, reads a page back as its verses and
raises on any other line, and on the chapter parameter anywhere that item 1 does not
put it.
"""

import dataclasses
import re
import unicodedata

from mb_cmn import hebrew_verse_numerals as hvn
from miqra_mevoar import books
from miqra_mevoar import mam_simple
from miqra_mevoar import tracked
from miqra_mevoar import wikitext


@dataclasses.dataclass(frozen=True)
class Page:
    """One display page: its key, its name after DISPLAY_PREFIX, its book, its chapters
    and the verses in them at which it begins and ends, and its category line's sort key
    where that is not its name."""

    key: str
    name: str
    stem: str
    # The first and last chapters of a part of a book, or None for the whole book.
    chapters: tuple[int, int] | None = None
    # The sort key of the page's category line, or None for the page's own name.
    sort_key: str | None = None
    # The verse of its first chapter at which the page begins, and the verse of its last
    # chapter at which it ends, or None for that chapter's last verse.
    first_verse: int = 1
    last_verse: int | None = None

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
    # The break line's letter, PE or SAMEKH, where a petuha or a setuma comes before the
    # verse, and its heading's transclusion, (target, section), where it has a heading.
    letter: str | None = None
    heading: tuple[str, str] | None = None
    # The chapter's numeral, which a page's first verse line gives as _CHAPTER_PARAMETER
    # where that verse is not its chapter's first, or None.
    chapter_parameter: str | None = None


def page_text(page):
    """A display page's text, exactly as a save stores it."""
    return _text(page_verses(page), page.category_sort_key())


def page_verses(page):
    """The verses of a display page, each with what the break line before it gives."""
    book = books.book_of_stem(page.stem)
    keys, page_keys = _page_keys(page, book)
    breaks = mam_simple.verse_breaks(book)
    headings = _heading_keys(book, keys)
    verses = []
    for chapter, verse in page_keys:
        kind = breaks.get((chapter, verse))
        heading = None
        if (chapter, verse) in headings:
            section = f"{wikitext.HEADING_SECTION}{hvn.INT_TO_STR_DIC[verse]}"
            heading = wikitext.page_title(book.mam_book, chapter), section
        # The page's first verse numbers its chapter where the template would not.
        chapter_parameter = None
        if not verses and verse != 1:
            chapter_parameter = hvn.INT_TO_STR_DIC[chapter]
        verses.append(
            Verse(
                book.bk39_name(),
                hvn.INT_TO_STR_DIC[chapter],
                hvn.INT_TO_STR_DIC[verse],
                None if kind is None else _LETTERS[kind],
                heading,
                chapter_parameter,
            )
        )
    return verses


def read_page(text):
    """A page's verses and its category's sort key; raise on any line of another shape."""
    lines = text.split("\n")
    if len(lines) < 3 or lines[-2] != "":
        raise ValueError("A display page ends in a blank line and its category line")
    category = _CATEGORY_LINE.fullmatch(lines[-1])
    if category is None:
        raise ValueError(f"{lines[-1]!r} is not a display page's category line")
    verses, pending = [], None
    for line in lines[:-2]:
        if match := _VERSE_LINE.fullmatch(line):
            book, chapter, verse, chapter_parameter = match.groups()
            if chapter_parameter is not None:
                _check_chapter_parameter(
                    line, verses, chapter, verse, chapter_parameter
                )
            letter, heading = pending or (None, None)
            verses.append(
                Verse(book, chapter, verse, letter, heading, chapter_parameter)
            )
            pending = None
        elif match := _BREAK_LINE.fullmatch(line):
            letter, target, section = match.groups()
            if letter is None and target is None:
                raise ValueError(f"{line!r} is a break line with neither parameter")
            if pending is not None:
                raise ValueError(f"{line!r} follows a break line")
            pending = letter, None if target is None else (target, section)
        else:
            raise ValueError(f"{line!r} is none of a display page's line shapes")
    if pending is not None:
        raise ValueError("A display page's last break line has no verse after it")
    if not verses:
        raise ValueError("A display page has no verse")
    if _text(verses, category.group(1)) != text:
        raise ValueError("A display page does not read back as itself")
    return verses, category.group(1)


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


def _heading_keys(book, keys):
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


def _text(verses, name):
    lines = []
    for verse in verses:
        if verse.letter is not None or verse.heading is not None:
            lines.append(_break_line(verse.letter, verse.heading))
        parameters = [verse.book, verse.chapter, verse.verse]
        if verse.chapter_parameter is not None:
            parameters.append(f"{_CHAPTER_PARAMETER}={verse.chapter_parameter}")
        lines.append(_template_line(_VERSE_TEMPLATE, *parameters))
    lines.extend(["", _category_line(name)])
    text = "\n".join(lines)
    if not unicodedata.is_normalized("NFC", text):
        raise ValueError(
            "A display page's text is not in NFC, the form MediaWiki stores"
        )
    return text


def _break_line(letter, heading):
    parameters = []
    if letter is not None:
        parameters.append(f"{_BREAK_PARAMETER}={letter}")
    if heading is not None:
        target, section = heading
        transclusion = "{{" + _SECTION_FUNCTION + ":" + target + "|" + section + "}}"
        parameters.append(f"{_HEADING_PARAMETER}={transclusion}")
    return _template_line(_BREAK_TEMPLATE, *parameters)


def _template_line(name, *parameters):
    return "{{" + "|".join((name, *parameters)) + "}}"


def _category_line(name):
    """The category line of the base chapters, wikitext.CATEGORY, with a sort key."""
    if not (wikitext.CATEGORY.startswith("[[") and wikitext.CATEGORY.endswith("]]")):
        raise ValueError(f"{wikitext.CATEGORY!r} is not a category link")
    return f"{wikitext.CATEGORY[:-2]}|{name}]]"


PE = "\N{HEBREW LETTER PE}"
SAMEKH = "\N{HEBREW LETTER SAMEKH}"
_LETTERS = {mam_simple.PETUHA: PE, mam_simple.SETUMA: SAMEKH}
# The title prefix and the names, as the links of the main page give them in revision
# 3103065, in its section of the Prophets and, for Daniel's, of the Writings. Stage 10
# copied the prefix and its names by script from revision 3101310, except Amos's, MAM's
# name of the book, and each equals 3101507's link; round 1 copied Joshua's new names and
# the six later names from 3101507 by script, and round 2 Malachi's from 3103065. Stage
# 11 copied the names of Judges' three parts and Daniel's two from 3103065 by script,
# and parsed each part's first and last verses from its link's label.
# Joshua's sort keys are the names under which Stage 10 created its two pages.
DISPLAY_PREFIX = "מקרא מבואר/תצוגה/"
PAGES = {
    page.key: page
    for page in (
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
_BREAK_LINE = re.compile(
    r"\{\{"
    + re.escape(_BREAK_TEMPLATE)
    + r"(?:\|"
    + re.escape(_BREAK_PARAMETER)
    + f"=({PE}|{SAMEKH}))?"
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
