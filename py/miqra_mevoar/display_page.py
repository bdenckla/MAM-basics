"""Miqra Mevoar's display pages on Hebrew Wikisource, each a book or a part of one.

A display page, titled DISPLAY_PREFIX and its name, sets each of its verses in MAM's
text beside Rabbi Kokhav's paraphrase from the verse's base chapter, in the form of
Avi's pages for the five megillot. PAGES lists Joshua's two parts, as Avi divided the
book, and the books of the Twelve whose base chapters exist: the five of Stage 10 of
doc/PLAN-miqra-mevoar.md, and Micah, Nahum, Habakkuk, Zephaniah, Haggai and Zechariah,
added in its round 1 of 2026-11-16. Their names are those that the main page,
מקרא מבואר, links from its section of the Prophets in revision 3101507, each copied by script and
checked against that revision's link. Obadiah's name has no vav, as Avi's link and the
Word file's title row have it, but its verses name the book as MAM does, with the vav.
Avi moved Joshua's two parts after Stage 10 created them, and their category lines
still sort them under the names they had then, which PAGES keeps as their sort keys.

A page has three line shapes and no others, as the megillot's pages have:

1. A verse: {{מקרא מבואר|<book>|<chapter>|<verse>}}, the book as
   mam_bknas.he_bk39_name names it and the chapter and verse as Hebrew numerals. The
   template sets MAM's verse beside the base chapter's section of the same name, and
   shows the chapter's numeral at its first verse. A page begins at a chapter's first
   verse, so no line needs the parameter with which a parasha page numbers a chapter
   that it begins elsewhere.
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
raises on any other line.
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
    """One display page: its key, its name after DISPLAY_PREFIX, its book and chapters,
    and its category line's sort key where that is not its name."""

    key: str
    name: str
    stem: str
    # The first and last chapters of a part of a book, or None for the whole book.
    chapters: tuple[int, int] | None = None
    # The sort key of the page's category line, or None for the page's own name.
    sort_key: str | None = None

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
        verses.append(
            Verse(
                book.bk39_name(),
                hvn.INT_TO_STR_DIC[chapter],
                hvn.INT_TO_STR_DIC[verse],
                None if kind is None else _LETTERS[kind],
                heading,
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
            letter, heading = pending or (None, None)
            verses.append(Verse(*match.groups(), letter, heading))
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


def _page_keys(page, book):
    """The book's (chapter, verse) keys, and those of the page's chapters."""
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
    page_keys = [key for key in keys if first <= key[0] <= last]
    if page_keys[0] != (first, 1):
        raise ValueError(
            f"{page.key} would begin at {page_keys[0]}, not at a chapter's first verse"
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
        lines.append(
            _template_line(_VERSE_TEMPLATE, verse.book, verse.chapter, verse.verse)
        )
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
# The title prefix and the names, as the links of the main page's section of the Prophets
# give them in revision 3101507. Stage 10 copied the prefix and its names by script from
# revision 3101310, except Amos's, MAM's name of the book, and each equals 3101507's link;
# round 1 copied Joshua's new names and the six later names from 3101507 by script.
# Joshua's sort keys are the names under which Stage 10 created its two pages.
DISPLAY_PREFIX = "מקרא מבואר/תצוגה/"
PAGES = {
    page.key: page
    for page in (
        Page("yehoshua-1", "ספר יהושע 1", "yehoshua", (1, 12), sort_key="ספר יהושע א"),
        Page("yehoshua-2", "ספר יהושע 2", "yehoshua", (13, 24), sort_key="ספר יהושע ב"),
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
    )
}
# The templates, their parameters and the section function, copied by script from the
# megillot's display pages as read on 2026-11-04 and checked against the templates' own
# text.
_VERSE_TEMPLATE = "מקרא מבואר"
_BREAK_TEMPLATE = "פרשה במקרא מבואר"
_BREAK_PARAMETER = "פרשה"
_HEADING_PARAMETER = "כותרת"
_SECTION_FUNCTION = "#קטע"
_ARGUMENT = r"([^|{}\[\]=\n]+)"
_VERSE_LINE = re.compile(
    r"\{\{" + re.escape(_VERSE_TEMPLATE) + (r"\|" + _ARGUMENT) * 3 + r"\}\}"
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
