"""The places of the headings in the Torah's base chapters on Hebrew Wikisource.

The five books of the Torah reached Avi long ago as a single Word file, which the
converter of py/main_miqra_mevoar.py never read, so in/miqra-mevoar/ holds none of
them. Their 187 base chapters were made on Wikisource before the bot made the other
books', in the form that wikitext.py describes, with a few more line shapes. A display
page of the Torah, py/miqra_mevoar/display_page.py, takes the places of its headings
from these base chapters, as the records here give them: for each chapter, its base
chapter's page id and revision id, and the verses before which it has a heading
section, in order. No text of the base chapters is kept.

BOOKS lists the books of the Torah, keyed by their OSIS abbreviations, each with its
pair of names in mam_bknas and its MAM-simple file. read_record and write_record read
and write a book's record, in/miqra-mevoar-base-headings/<OSIS abbreviation>.json, its
shape checked.

chapter_headings, a closed parser of a base chapter's text, accepts these lines and no
others:

1. the chapter heading, as wikitext.chapter_heading writes it, or with two spaces
   before the numeral, as Genesis 3 and Exodus 4 have it;
2. before the chapter heading, a navigation bar: a call of _NAVIGATION_BAR with the
   index, the book and the numerals of the chapter before the page's own, of its own
   and of the chapter after it, as Numbers 20 has;
3. a heading line, with its leading "*" or without it, as Deuteronomy 22:20 has it,
   standing directly before the verse line of its numeral;
4. a verse line, with or without soft hyphens after it, as Exodus 21:34 has three;
5. a blank line, like those that stand, alone or in pairs, before the heading at the
   start of many a weekly portion;
6. the category line, wikitext.CATEGORY, as the last line.

A tag of another verse's section inside a verse line, as the end tag of verse 1's
section inside the verse line of Leviticus 21:20, is reported rather than refused,
since it moves no heading; any other tag there raises. The verse sections must be
MAM-simple's verses of the chapter, in order, once each.

run is py/main_miqra_mevoar.py's subcommand base-headings. It reads the latest
revision of every base chapter of the Torah, anonymously and uncached, through
ws_revision_api.ChapterClient, at most _BATCH_TITLES titles to a request, since a
request for 50 of these long titles was refused as too long, and parses each. It then
writes the five records, or, with check, writes nothing: it lists each chapter whose
revision changed since its record, and fails if any heading moved, appeared or
vanished, or if a page does not parse.
"""

import dataclasses
import json
import re

from mb_cmn import file_io
from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn import mam_bknas
from mb_cmn import paths
from mb_cmn import polite_download
from miqra_mevoar import mam_simple
from miqra_mevoar import wikitext
from ws import ws_revision_api


@dataclasses.dataclass(frozen=True)
class Book:
    """One book of the Torah: its OSIS abbreviation, and where MAM-simple keeps it."""

    abbreviation: str
    mam_book: tuple[str, str | None]
    mam_simple_file: str
    osis_id: str

    def bk39_name(self) -> str:
        """MAM's name of the book, as the titles of the base chapters give it."""
        return mam_bknas.he_bk39_name(*self.mam_book)


def json_dir():
    """The directory of the records."""
    return paths.in_dir() / "miqra-mevoar-base-headings"


def read_record(book):
    """A book's record, its shape checked."""
    path = _json_path(book)
    record = json.loads(path.read_text(encoding="utf-8"))
    require_shape(record, book, path.name)
    return record


def write_record(book, record):
    """Write a book's record, after checking its shape."""
    path = _json_path(book)
    require_shape(record, book, path.name)
    file_io.json_dump_to_file_path(record, str(path), indent=1)


def require_shape(record, book, where):
    """Raise unless record has the keys, numbering and values of a book's record."""
    _require_keys(record, {"book", "chapters"}, where)
    if record["book"] != book.bk39_name():
        raise ValueError(f"{where}: book {record['book']!r}, not {book.bk39_name()!r}")
    chapters = record["chapters"]
    if not isinstance(chapters, list) or not chapters:
        raise ValueError(f"{where}: no chapters")
    for number, chapter in enumerate(chapters, start=1):
        at = f"{where} chapter {number}"
        _require_keys(chapter, {"chapter", "page_id", "revision_id", "headings"}, at)
        if chapter["chapter"] != number:
            raise ValueError(
                f"{at}: chapter {chapter['chapter']!r} where {number} is due"
            )
        for key in ("page_id", "revision_id"):
            if not _positive(chapter[key]):
                raise ValueError(
                    f"{at}: {key} {chapter[key]!r} is not a positive integer"
                )
        headings = chapter["headings"]
        if not (
            isinstance(headings, list)
            and all(_positive(verse) for verse in headings)
            and headings == sorted(set(headings))
        ):
            raise ValueError(f"{at}: headings {headings!r} are not verses in order")
    for key in ("page_id", "revision_id"):
        values = [chapter[key] for chapter in chapters]
        if len(set(values)) != len(values):
            raise ValueError(f"{where}: two chapters have the same {key}")


def chapter_headings(text, book, chapter, verses):
    """The verses before which a base chapter has a heading, in order, and a report of
    each tag of another verse's section in its verse lines; raise on a line of any other
    shape.

    text is the base chapter's text, and verses are the numbers of the chapter's verses
    in MAM-simple, in order.
    """
    where = wikitext.page_title(book.mam_book, chapter)
    lines = text.split("\n")
    start = 1 if lines[0] == _navigation_bar(book, chapter) else 0
    if len(lines) < start + 2:
        raise ValueError(f"{where}: {len(lines)} lines")
    if lines[start] not in _chapter_headings(chapter):
        raise ValueError(
            f"{where}: line {start + 1} is not the chapter heading: {lines[start]!r}"
        )
    if lines[-1] != wikitext.CATEGORY:
        raise ValueError(f"{where}: the last line is not the category line")
    headings, found, strays, pending = [], [], [], None
    for number, line in enumerate(lines[start + 1 : -1], start=start + 2):
        at = f"{where} line {number}"
        if line == "":
            if pending is not None:
                raise ValueError(f"{at}: a blank line after the heading of {pending}")
            continue
        if match := _HEADING_LINE.fullmatch(line):
            if pending is not None:
                raise ValueError(f"{at}: a heading after the heading of {pending}")
            pending = _verse_number(match.group(1), at)
            continue
        match = _VERSE_LINE.fullmatch(line)
        if match is None:
            raise ValueError(f"{at}: none of a base chapter's line shapes: {line!r}")
        name, body = match.groups()
        verse = _verse_number(name, at)
        strays.extend(_strays(body, verse, at))
        if pending is not None:
            if pending != verse:
                raise ValueError(f"{at}: the heading of {pending} is before {verse}")
            headings.append(verse)
            pending = None
        found.append(verse)
    if pending is not None:
        raise ValueError(
            f"{where}: the heading of {pending} has no verse line after it"
        )
    if found != list(verses):
        raise ValueError(
            f"{where}: its verse sections are {found}, not MAM-simple's {list(verses)}"
        )
    return headings, strays


def run(check=False):
    """Read every base chapter of the Torah and write the records or, with check,
    compare them with the records, writing nothing; return 1 on any failure, else 0."""
    chapters = _chapters()
    texts = _latest_revisions([title for _book, _chapter, title, _verses in chapters])
    live, failures = {}, []
    for book, chapter, title, verses in chapters:
        identity, text = texts[title]
        try:
            headings, strays = chapter_headings(text, book, chapter, verses)
        except ValueError as error:
            failures.append(f"does not parse: {error}")
            continue
        for stray in strays:
            print(f"reported: {stray}")
        live[book.abbreviation, chapter] = {
            "chapter": chapter,
            "page_id": identity["page_id"],
            "revision_id": identity["revision_id"],
            "headings": headings,
        }
    for book in BOOKS.values():
        entries = [
            entry for (key, _n), entry in live.items() if key == book.abbreviation
        ]
        count = sum(len(entry["headings"]) for entry in entries)
        print(f"{book.abbreviation}: {len(entries)} chapters, {count} headings")
    print(
        f"{len(live)} of {len(chapters)} chapters parsed,"
        f" {sum(len(entry['headings']) for entry in live.values())} headings"
    )
    if check:
        failures.extend(_differences(live))
    elif not failures:
        for book in BOOKS.values():
            record = {
                "book": book.bk39_name(),
                "chapters": [
                    entry
                    for (key, _n), entry in live.items()
                    if key == book.abbreviation
                ],
            }
            write_record(book, record)
            print(f"wrote {_json_path(book)}")
    for failure in failures:
        print(f"FAIL {failure}")
    print(f"failures: {len(failures)}")
    return 1 if failures else 0


def _chapters():
    """(book, chapter, base chapter's title, MAM-simple's verses) of every chapter."""
    found = []
    for book in BOOKS.values():
        keys = mam_simple.verse_keys(book)
        for chapter in dict.fromkeys(number for number, _verse in keys):
            verses = [verse for number, verse in keys if number == chapter]
            title = wikitext.page_title(book.mam_book, chapter)
            found.append((book, chapter, title, verses))
    return found


def _latest_revisions(titles):
    """Each title's identity and its latest revision's text, read uncached."""
    found = {}
    with polite_download.PoliteDownloader(_CONFIG) as downloader:
        client = ws_revision_api.ChapterClient(downloader, _API_PHP)
        for batch in ws_revision_api.batches(titles, _BATCH_TITLES):
            identities = []
            for title, (identity, _lines) in client.by_titles(
                batch, content=False
            ).items():
                if identity["resolved_title"] != title:
                    raise ValueError(
                        f"{title} resolves to {identity['resolved_title']}"
                    )
                identities.append(identity)
            for title, (identity, revision) in client.by_raw_revisions(
                identities
            ).items():
                found[title] = identity, revision["content"].decode("utf-8")
            print(f"read {len(found)} of {len(titles)} base chapters")
    return found


def _differences(live):
    """Print each chapter whose revision changed since its record, and return a failure
    for each chapter whose headings differ from its record's."""
    failures, changed = [], 0
    for book in BOOKS.values():
        record = read_record(book)
        keys = mam_simple.verse_keys(book)
        numbers = list(dict.fromkeys(number for number, _verse in keys))
        if [chapter["chapter"] for chapter in record["chapters"]] != numbers:
            failures.append(f"{book.abbreviation}: the record's chapters are not MAM's")
            continue
        for recorded in record["chapters"]:
            entry = live.get((book.abbreviation, recorded["chapter"]))
            if entry is None:
                # Its page does not parse, which is a failure already.
                continue
            title = wikitext.page_title(book.mam_book, recorded["chapter"])
            if (entry["page_id"], entry["revision_id"]) != (
                recorded["page_id"],
                recorded["revision_id"],
            ):
                changed += 1
                print(
                    f"changed: {title}: page {recorded['page_id']} revision"
                    f" {recorded['revision_id']} to page {entry['page_id']} revision"
                    f" {entry['revision_id']}"
                )
            if entry["headings"] != recorded["headings"]:
                failures.append(
                    f"headings differ: {title}: the record has"
                    f" {recorded['headings']}, the page {entry['headings']}"
                )
    print(f"{changed} chapters have another revision than their records'")
    return failures


def _chapter_headings(chapter):
    """The chapter heading as wikitext writes it, and the same with two spaces before
    its numeral."""
    if not wikitext.CHAPTER_HEADING_START.endswith(" "):
        raise ValueError("wikitext's chapter heading has no space before its numeral")
    numeral = hvn.INT_TO_STR_DIC[chapter]
    return {
        wikitext.chapter_heading(chapter),
        f"{wikitext.CHAPTER_HEADING_START} {numeral}{wikitext.CHAPTER_HEADING_END}",
    }


def _navigation_bar(book, chapter):
    """The navigation bar that may stand before a chapter's heading, or None for a
    book's first chapter, which has no chapter before it."""
    if chapter == 1:
        return None
    numerals = [
        hvn.INT_TO_STR_DIC[number] for number in (chapter - 1, chapter, chapter + 1)
    ]
    parameters = (_NAVIGATION_BAR, wikitext.INDEX_TITLE, book.mam_book[0], *numerals)
    return "{{" + "|".join(parameters) + "}}"


def _verse_number(name, at):
    """The number of the verse that a section's name numbers; raise on another name."""
    number = hvn.STR_TO_INT_DIC.get(name)
    if number is None or hvn.INT_TO_STR_DIC[number] != name:
        raise ValueError(f"{at}: the section name {name!r} is not a verse's numeral")
    return number


def _strays(body, verse, at):
    """A report of each tag of another verse's section inside a verse line's body; raise
    on any other tag, or any other angle bracket, there."""
    reports = []
    for match in _TAG.finditer(body):
        kind, name = match.groups()
        other = _verse_number(name, at)
        if other == verse:
            raise ValueError(f"{at}: a tag of verse {verse}'s section inside its own")
        reports.append(
            f"{at}: the {_TAG_KINDS[kind]} tag of verse {other}'s section inside the"
            f" verse line of {verse}"
        )
    if _ANGLE.search(_TAG.sub("", body)):
        raise ValueError(f"{at}: an angle bracket inside the verse line of {verse}")
    return reports


def _positive(value):
    return type(value) is int and value > 0


def _require_keys(mapping, keys, where):
    if not isinstance(mapping, dict) or set(mapping) != keys:
        shown = sorted(mapping) if isinstance(mapping, dict) else type(mapping).__name__
        raise ValueError(f"{where}: keys {shown}, not {sorted(keys)}")


def _json_path(book):
    return json_dir() / f"{book.abbreviation}.json"


BOOKS = {
    book.abbreviation: book
    for book in (
        Book("Gen", mam_bknas.BS_GENESIS, "Gen.json", "Gen"),
        Book("Exod", mam_bknas.BS_EXODUS, "Exod.json", "Exod"),
        Book("Lev", mam_bknas.BS_LEVIT, "Lev.json", "Lev"),
        Book("Num", mam_bknas.BS_NUMBERS, "Num.json", "Num"),
        Book("Deut", mam_bknas.BS_DEUTER, "Deut.json", "Deut"),
    )
}
# The navigation bar's template, copied by script from the first line of the base
# chapter of Numbers 20, revision 1453389, as read on 2026-11-22.
_NAVIGATION_BAR = "סרגל ניווט"
_NAME = "([^<>/]+)"
_HEADING_LINE = re.compile(
    r"\*?<"
    + re.escape(wikitext.SECTION_START + wikitext.HEADING_SECTION)
    + _NAME
    + "/>[^<>]*<"
    + re.escape(wikitext.SECTION_END + wikitext.HEADING_SECTION)
    + r"\1/>"
)
_VERSE_LINE = re.compile(
    "<"
    + re.escape(wikitext.SECTION_START)
    + _NAME
    + "/>(.*)<"
    + re.escape(wikitext.SECTION_END)
    + r"\1/>"
    + "\N{SOFT HYPHEN}*"
)
_TAG = re.compile(
    "<("
    + re.escape(wikitext.SECTION_START)
    + "|"
    + re.escape(wikitext.SECTION_END)
    + ")"
    + _NAME
    + "/>"
)
_TAG_KINDS = {wikitext.SECTION_START: "begin", wikitext.SECTION_END: "end"}
_ANGLE = re.compile("[<>]")
_BATCH_TITLES = 12
_API_PHP = "https://he.wikisource.org/w/api.php"
_CONFIG = polite_download.PoliteDownloadConfig(
    user_agent=(
        "MAM-basics Miqra Mevoar base headings (https://github.com/bdenckla/MAM-basics)"
    ),
    throttle=polite_download.ThrottleConfig(min_delay_s=1.5),
)
