"""The base-chapter index of Miqra Mevoar on Hebrew Wikisource, linking all 929 chapters.

The index, wikitext.INDEX_TITLE, begins with framing that its editors keep: an
information section, the list of the books already encoded, and the working steps for
editors. One section per book follows, and the category line ends the page. A book's
section is two lines: a heading line, ==<heading>==, and a line of links to the book's
base chapters, *{{ג|'''{{קו תחתי|פרקים:}} <links>'''}}, each link
[[<the chapter's title>|<its numeral>]] and the links joined by " · ". A book of several
parts has one section whose line gives each part as a labelled run, "<label>: <links>;",
the runs joined by a space: the Twelve, as the live page has it, and Samuel, Kings,
Ezra-Nehemiah and Chronicles, as Ben chose on 2026-11-03. A blank line separates two
sections, and the category line follows the last.

page_text completes the index from its live text. The framing, up to the heading of the
first book section, and the text from the category line on keep their bytes. Between
them it generates a section for each of the 24 books, linking every chapter that
MAM-simple has, in its 39 books, to the title that wikitext.page_title gives; most of
those links stay red until their pages exist. read_sections, a closed parser of the two
line shapes, reads the old sections and the new. Each old section must reappear
unchanged, except that a section of labelled runs, such as the Twelve's, need only keep
its old runs unchanged and in order within the new section. Any other line among the old
sections stops the run, and so does a page that is not in NFC, the form MediaWiki stores.

BOOKS lists the 39 books in the order of printed Bibles, which is that of mam_bknas's
BS_ pairs. A section's heading is its book's 24-book name, the first part of the BS_
pair, and a part's label is its 39-book name, with three exceptions copied from the live
page by script: the Twelve's heading lacks "ספר", and Ecclesiastes' heading and
Obadiah's label each have a holam. A book missing from MAM-simple, or a MAM-simple book
missing from BOOKS, is an error.
"""

import dataclasses
import re
import unicodedata

from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn import mam_bknas
from miqra_mevoar import mam_simple
from miqra_mevoar import wikitext


@dataclasses.dataclass(frozen=True)
class Book:
    """One of the 39 books: its BS_ pair, where MAM-simple keeps it, and any exception."""

    mam_book: tuple[str, str | None]
    osis_id: str
    mam_simple_file: str
    # An exception copied from the live page: the heading of a book of one part, or the
    # label of a part of a book.
    display: str | None = None


@dataclasses.dataclass(frozen=True)
class Run:
    """A section's links, or one labelled part's: (target, text) for each link."""

    label: str | None
    links: tuple[tuple[str, str], ...]


@dataclasses.dataclass(frozen=True)
class Section:
    """A book's section of the index: its heading and its runs of links."""

    heading: str
    runs: tuple[Run, ...]


def page_text(old_text):
    """The completed index from its live text, exactly as a save stores it."""
    framing, old_sections, tail = _split(old_text)
    new_sections = sections()
    _require_kept(old_sections, new_sections)
    text = "\n".join(framing + section_lines(new_sections) + tail)
    if not unicodedata.is_normalized("NFC", text):
        raise ValueError("The index's text is not in NFC, the form MediaWiki stores")
    return text


def page_sections(text):
    """The book sections of an index page's text, read by the closed parser."""
    _framing, book_sections, _tail = _split(text)
    return book_sections


def sections():
    """The index's book sections, linking every chapter that MAM-simple has."""
    _require_mam_simple_books()
    out = []
    for book in BOOKS:
        heading = _heading(book)
        run = Run(_label(book), tuple(_chapter_links(book)))
        if out and out[-1].heading == heading:
            out[-1] = Section(heading, out[-1].runs + (run,))
        else:
            out.append(Section(heading, (run,)))
    headings = [section.heading for section in out]
    if len(set(headings)) != len(headings):
        raise ValueError(f"BOOKS gives a heading to two sections: {headings}")
    return out


def section_lines(book_sections):
    """The lines of the sections, with a blank line between two of them."""
    lines = []
    for section in book_sections:
        if lines:
            lines.append("")
        lines.extend([f"=={section.heading}==", _links_line(section.runs)])
    return lines


def read_sections(lines):
    """The sections in lines, as section_lines writes them; raise on any other line."""
    book_sections, at = [], 0
    while True:
        if at + 1 >= len(lines):
            raise ValueError(f"The book sections end inside a section: {lines[at:]!r}")
        book_sections.append(
            Section(_read_heading(lines[at]), _read_runs(lines[at + 1]))
        )
        if at + 2 == len(lines):
            return book_sections
        if lines[at + 2] != "":
            raise ValueError(
                f"{lines[at + 2]!r} follows a book section, where a blank line is due"
            )
        at += 3


def _split(text):
    """The framing's lines, the book sections, and the lines from the category line on."""
    lines = text.split("\n")
    first = next(
        (
            at
            for at in range(len(lines) - 1)
            if _HEADING.fullmatch(lines[at]) and lines[at + 1].startswith(_LINKS_START)
        ),
        None,
    )
    if first is None:
        raise ValueError("The index has no book section")
    if wikitext.CATEGORY not in lines[first:]:
        raise ValueError("The index has no category line after its book sections")
    end = lines.index(wikitext.CATEGORY, first)
    framing, tail = lines[:first], lines[end:]
    if not framing or not framing[0].startswith(_INFORMATION_HEADING):
        raise ValueError(f"The index begins {lines[0]!r}, not its information section")
    if strays := [line for line in tail if line.startswith(_LINKS_START)]:
        raise ValueError(f"The index has links after its category line: {strays!r}")
    return framing, read_sections(lines[first:end]), tail


def _read_heading(line):
    match = _HEADING.fullmatch(line)
    if match is None:
        raise ValueError(f"{line!r} is not a book section's heading")
    return match.group(1)


def _read_runs(line):
    if not (line.startswith(_LINKS_START) and line.endswith(_LINKS_END)):
        raise ValueError(f"{line!r} is not a book section's line of links")
    body = line[len(_LINKS_START) : -len(_LINKS_END)]
    if _LINKS.fullmatch(body):
        runs = (Run(None, _read_links(body)),)
    elif _LABELLED_RUNS.fullmatch(body):
        runs = tuple(
            Run(match.group(1), _read_links(match.group(2)))
            for match in _LABELLED_RUN.finditer(body)
        )
    else:
        raise ValueError(f"{line!r} is neither one run of links nor labelled runs")
    if _links_line(runs) != line:
        raise ValueError(f"{line!r} does not read back as itself")
    return runs


def _read_links(text):
    return tuple((match.group(1), match.group(2)) for match in _LINK.finditer(text))


def _links_line(runs):
    if len(runs) == 1 and runs[0].label is None:
        body = _joined(runs[0].links)
    elif runs and all(run.label is not None for run in runs):
        body = " ".join(f"{run.label}: {_joined(run.links)};" for run in runs)
    else:
        raise ValueError(f"Runs neither one unlabelled run nor all labelled: {runs!r}")
    return f"{_LINKS_START}{body}{_LINKS_END}"


def _joined(links):
    return _SEPARATOR.join(f"[[{target}|{text}]]" for target, text in links)


def _require_kept(old_sections, new_sections):
    """Raise unless each old section reappears, or, if labelled, each of its old runs."""
    new_by_heading = {section.heading: section for section in new_sections}
    old_headings = [section.heading for section in old_sections]
    problems = []
    if len(set(old_headings)) != len(old_headings):
        problems.append(f"the old index repeats a heading: {old_headings}")
    for old in old_sections:
        new = new_by_heading.get(old.heading)
        if new is None:
            problems.append(f"no new section is headed {old.heading!r}")
        elif _labelled(old) and _labelled(new):
            remaining = iter(new.runs)
            if not all(run in remaining for run in old.runs):
                problems.append(
                    f"the old runs of {old.heading!r} are not kept in order"
                )
        elif old != new:
            problems.append(f"the section {old.heading!r} changes")
    kept = [
        section.heading for section in new_sections if section.heading in old_headings
    ]
    if kept != old_headings:
        problems.append(f"the old sections' order {old_headings} changes")
    if problems:
        raise ValueError(
            "The new index drops what the old one has: " + "; ".join(problems)
        )


def _labelled(section):
    return all(run.label is not None for run in section.runs)


def _heading(book):
    bk24_name, part = book.mam_book
    if part is None:
        return book.display or bk24_name
    return _PART_HEADINGS.get(bk24_name, bk24_name)


def _label(book):
    if book.mam_book[1] is None:
        return None
    return book.display or mam_bknas.he_bk39_name(*book.mam_book)


def _chapter_links(book):
    numbers = mam_simple.chapter_numbers(book)
    if numbers != list(range(1, len(numbers) + 1)):
        raise ValueError(f"{book.osis_id}: MAM-simple's chapters are {numbers}")
    for number in numbers:
        yield wikitext.page_title(book.mam_book, number), hvn.INT_TO_STR_DIC[number]


def _require_mam_simple_books():
    found = mam_simple.book_ids()
    table = [(book.mam_simple_file, book.osis_id) for book in BOOKS]
    for name, ids in (("MAM-simple", found), ("BOOKS", table)):
        if len(set(ids)) != len(ids):
            raise ValueError(f"{name} has a book twice: {sorted(ids)}")
    if missing := sorted(set(found) - set(table)):
        raise ValueError(f"MAM-simple has books that BOOKS lacks: {missing}")
    if missing := sorted(set(table) - set(found)):
        raise ValueError(f"BOOKS has books that MAM-simple lacks: {missing}")


# The three exceptions, copied by script from the live page's revision 3084327 as
# captured on 2026-11-02, each holam spelled by its name.
_TWELVE_HEADING = "תרי עשר"
_OBADIAH_LABEL = "ע\N{HEBREW POINT HOLAM}בדיה"
_QOHELET_HEADING = "מגילת ק\N{HEBREW POINT HOLAM}הלת"
# The heading of a book of several parts, where it is not the book's 24-book name.
_PART_HEADINGS = {mam_bknas.BS_HOSEA[0]: _TWELVE_HEADING}
BOOKS = (
    Book(mam_bknas.BS_GENESIS, "Gen", "Gen.json"),
    Book(mam_bknas.BS_EXODUS, "Exod", "Exod.json"),
    Book(mam_bknas.BS_LEVIT, "Lev", "Lev.json"),
    Book(mam_bknas.BS_NUMBERS, "Num", "Num.json"),
    Book(mam_bknas.BS_DEUTER, "Deut", "Deut.json"),
    Book(mam_bknas.BS_JOSHUA, "Josh", "Josh.json"),
    Book(mam_bknas.BS_JUDGES, "Judg", "Judg.json"),
    Book(mam_bknas.BS_FST_SAM, "1Sam", "1Sam-2Sam.json"),
    Book(mam_bknas.BS_SND_SAM, "2Sam", "1Sam-2Sam.json"),
    Book(mam_bknas.BS_FST_KGS, "1Kgs", "1Kgs-2Kgs.json"),
    Book(mam_bknas.BS_SND_KGS, "2Kgs", "1Kgs-2Kgs.json"),
    Book(mam_bknas.BS_ISAIAH, "Isa", "Isa.json"),
    Book(mam_bknas.BS_JEREM, "Jer", "Jer.json"),
    Book(mam_bknas.BS_EZEKIEL, "Ezek", "Ezek.json"),
    Book(mam_bknas.BS_HOSEA, "Hos", "Hos-Mal.json"),
    Book(mam_bknas.BS_JOEL, "Joel", "Hos-Mal.json"),
    Book(mam_bknas.BS_AMOS, "Amos", "Hos-Mal.json"),
    Book(mam_bknas.BS_OBADIAH, "Obad", "Hos-Mal.json", _OBADIAH_LABEL),
    Book(mam_bknas.BS_JONAH, "Jonah", "Hos-Mal.json"),
    Book(mam_bknas.BS_MICAH, "Mic", "Hos-Mal.json"),
    Book(mam_bknas.BS_NAXUM, "Nah", "Hos-Mal.json"),
    Book(mam_bknas.BS_XABA, "Hab", "Hos-Mal.json"),
    Book(mam_bknas.BS_TSEF, "Zeph", "Hos-Mal.json"),
    Book(mam_bknas.BS_XAGGAI, "Hag", "Hos-Mal.json"),
    Book(mam_bknas.BS_ZEKHAR, "Zech", "Hos-Mal.json"),
    Book(mam_bknas.BS_MALAKHI, "Mal", "Hos-Mal.json"),
    Book(mam_bknas.BS_PSALMS, "Ps", "Ps.json"),
    Book(mam_bknas.BS_PROV, "Prov", "Prov.json"),
    Book(mam_bknas.BS_JOB, "Job", "Job.json"),
    Book(mam_bknas.BS_SONG, "Song", "Song.json"),
    Book(mam_bknas.BS_RUTH, "Ruth", "Ruth.json"),
    Book(mam_bknas.BS_LAMENT, "Lam", "Lam.json"),
    Book(mam_bknas.BS_QOHELET, "Eccl", "Eccl.json", _QOHELET_HEADING),
    Book(mam_bknas.BS_ESTHER, "Esth", "Esth.json"),
    Book(mam_bknas.BS_DANIEL, "Dan", "Dan.json"),
    Book(mam_bknas.BS_EZRA, "Ezra", "Ezra-Neh.json"),
    Book(mam_bknas.BS_NEXEM, "Neh", "Ezra-Neh.json"),
    Book(mam_bknas.BS_FST_CHR, "1Chr", "1Chr-2Chr.json"),
    Book(mam_bknas.BS_SND_CHR, "2Chr", "1Chr-2Chr.json"),
)
_INFORMATION_HEADING = "==מידע על פרקי הבסיס"
_LINKS_START = "*{{ג|'''{{קו תחתי|פרקים:}} "
_LINKS_END = "'''}}"
_SEPARATOR = " \N{MIDDLE DOT} "
_HEADING = re.compile("==([^=]+)==")
_LINK_PATTERN = r"\[\[([^\[\]|]+)\|([^\[\]|]+)\]\]"
_LINKS_PATTERN = rf"{_LINK_PATTERN}(?:{_SEPARATOR}{_LINK_PATTERN})*"
_RUN_PATTERN = rf"([^\s:;\[\]][^:;\[\]]*): ({_LINKS_PATTERN});"
_LINK = re.compile(_LINK_PATTERN)
_LINKS = re.compile(_LINKS_PATTERN)
_LABELLED_RUN = re.compile(_RUN_PATTERN)
_LABELLED_RUNS = re.compile(rf"{_RUN_PATTERN}(?: {_RUN_PATTERN})*")
