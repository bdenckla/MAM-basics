"""Extract a Miqra Mevoar book from its Word file: each verse's heading and paraphrase.

Each book is one table of four right-to-left columns, or several tables read as one
(docx_table.py): the chapter numeral, only on a chapter's first verse; the verse
numeral; the Bible text, MAM copied from Wikisource; and the paraphrase. _classify
names each row's kind by a closed dispatch:

  title    the Bible cell alone, styled as heading 2, holds the book's pointed name; the
           paraphrase cell may also hold the heading of the first verse, as Joshua's does
  heading  the paraphrase cell alone, styled as heading 3 or heading 4, holds the
           heading of the next verse; the Bible cell may hold a pe or a samekh, the
           petuha or setuma marker before it, as one of Joel's does
  verse    the verse numeral, the Bible text and the paraphrase, and the chapter numeral
           on a chapter's first verse
  empty    no text, or only a pe or a samekh in the Bible cell

Any other row is an error, as is a second title row, a heading with no verse after it,
or a chapter or verse number out of sequence. So is a heading or paraphrase that has a
line break, a tab or anything else MediaWiki would interpret or transform. A cell's
text joins its paragraphs, and each run of whitespace in it becomes one space.

Where a book's entry in books.BOOKS declares its chapters, (first, last), as Isaiah's
declares 40 to 66, the rows after the title row and before the verse row that opens
the first chapter are read past before _classify sees them, since a row of an
unfinished chapter, such as a verse with no paraphrase yet, would be refused. That
verse row is the first whose chapter cell is first's numeral and whose verse cell is
alef, and only those two cells of a row are read to find it. The last row with text
before it, past any empty row, gives the verse its heading if it is a heading row; a
row with a chapter or verse number gives none, and any other row is an error. The title
row is still required as the first row of text, and may not hold a heading, which
would be 1:1's. The chapters are then numbered from first, and the last must be last.
Each row read past is named as such where a picture in it is named, and extract and
check say how many rows they read past.

A style is known by its name in the file's styles.xml. _TITLE_STYLES and _HEADING_STYLES
name only styles that Rabbi Kokhav's files have used: the files of the thirteen books
first tracked name them "heading 2", "heading 3" and "heading 4", and Avi's corrected
files of Judges and Malachi, saved again on 2026-11-16, name two of them "Heading 2" and
"Heading 4". Those two files also give every other paragraph the style "Normal", where
the other files give it none; a style that is no heading's makes no row a title or a
heading.

A picture that holds no text, in a cell, is read past (docx_table.py), and each one is
named by its file, its row, the row's place in the book and its cell, so that nobody
loses track of a picture that the pages leave out.
"""

import hashlib
import re
import unicodedata
from pathlib import Path

from mb_cmn import hebrew_verse_numerals as hvn
from miqra_mevoar import books
from miqra_mevoar import docx_table
from miqra_mevoar import tracked
from miqra_mevoar import wikitext


def run(directory):
    """Write in/miqra-mevoar/<stem>.json for every .docx in directory."""
    for docx_path in docx_paths(directory):
        book = books.book_of_stem(docx_path.stem)
        record, _bible, notes = extract_book(docx_path, book)
        tracked.write_record(book, record)
        verses = [
            verse for chapter in record["chapters"] for verse in chapter["verses"]
        ]
        headings = sum(verse["heading"] is not None for verse in verses)
        print(
            f"{book.stem}: {len(record['chapters'])} chapters, {len(verses)} verses,"
            f" {headings} headings"
        )
        for line in notes:
            print(f"  {line}")


def docx_paths(directory):
    """Every .docx in directory, in name order; exit if there is none."""
    found = sorted(Path(directory).glob("*.docx"))
    if not found:
        raise SystemExit(f"No .docx file in {directory}")
    return found


def extract_book(docx_path, book):
    """A book's record for its tracked JSON, each verse's Bible cell by (chapter, verse),
    and lines of notes: where the book's entry declares its chapters, one that says how
    many rows were read past before them, and then one naming each picture read past in
    the file."""
    data = docx_path.read_bytes()
    table = docx_table.read_table(docx_path)
    title, chapters, places, read_past = _build(
        table.rows, docx_path.name, book.chapters
    )
    unmarked = "".join(char for char in title if unicodedata.category(char) != "Mn")
    if unmarked != book.title:
        raise ValueError(f"{docx_path.name}: title {unmarked!r}, not {book.title!r}")
    record = {
        "book": book.bk39_name(),
        "source": {
            "file": docx_path.name,
            "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
        },
        "chapters": [
            {
                "chapter": chapter["chapter"],
                "verses": [
                    {key: verse[key] for key in ("verse", "heading", "paraphrase")}
                    for verse in chapter["verses"]
                ],
            }
            for chapter in chapters
        ],
    }
    bible = {
        (chapter["chapter"], verse["verse"]): verse["bible"]
        for chapter in chapters
        for verse in chapter["verses"]
    }
    notes = []
    if book.chapters is not None:
        first, last = book.chapters
        notes.append(
            f"{docx_path.name}: {read_past} rows read past, before {first}:1, since the"
            f" book's entry declares chapters {first} to {last}"
        )
    notes.extend(
        f"{docx_path.name} row {picture.row} ({places[picture.row]}),"
        f" cell {picture.cell}: a picture that holds no text, read past"
        for picture in table.pictures
    )
    return record, bible, notes


def _build(rows, name, declared=None):
    """The book's title, its chapters, each row's place, its verse or its kind, and how
    many rows were read past. Where declared gives the book's first and last chapters,
    the rows before the first chapter's first verse are read past, as the module
    docstring says."""
    first, last = declared or (1, None)
    chapters, pending, title = [], None, None
    places, heading_row = {}, None
    resume, read_past = 0, 0
    for index, cells in enumerate(rows):
        if index < resume:
            continue
        where = f"{name} row {index}"
        kind, (c0, c1, c2, c3) = _classify(cells, where)
        if kind == "empty":
            places[index] = "an empty row"
            continue
        if kind == "title":
            if title is not None or chapters or pending is not None:
                raise ValueError(
                    f"{where}: a title row after the book's first row of text"
                )
            title, pending = c2, c3 or None
            places[index] = "the title row"
            if declared is not None:
                if pending is not None:
                    raise ValueError(
                        f"{where}: the title row holds a heading, which would be 1:1's,"
                        f" but the book's chapters begin at {first}"
                    )
                resume, heading = _first_verse_row(rows, index, first, name)
                for skipped in range(index + 1, resume):
                    places[skipped] = f"a row read past, before {first}:1"
                read_past = resume - index - 1
                if heading is not None:
                    heading_row, pending = heading
                    read_past -= 1
            continue
        if title is None:
            raise ValueError(f"{where}: a {kind} row before the title row")
        if kind == "heading":
            if pending is not None:
                raise ValueError(f"{where}: a heading after the heading {pending!r}")
            pending, heading_row = c3, index
            continue
        if c0:
            number = _numeral(c0, f"{where}, chapter cell")
            due = first + len(chapters)
            if number != due:
                raise ValueError(f"{where}: chapter {number} after {due - 1}")
            chapters.append({"chapter": number, "verses": []})
        if not chapters:
            raise ValueError(f"{where}: a verse before any chapter")
        verses = chapters[-1]["verses"]
        number = _numeral(c1, f"{where}, verse cell")
        if number != len(verses) + 1:
            raise ValueError(
                f"{where}: chapter {chapters[-1]['chapter']} verse {number}"
                f" after {len(verses)}"
            )
        verses.append(
            {"verse": number, "heading": pending, "paraphrase": c3, "bible": c2}
        )
        places[index] = f"{chapters[-1]['chapter']}:{number}"
        if heading_row is not None:
            places[heading_row] = f"the heading of {places[index]}"
        pending, heading_row = None, None
    if title is None:
        raise ValueError(f"{name}: no title row")
    if pending is not None:
        raise ValueError(f"{name}: the heading {pending!r} has no verse after it")
    if last is not None and (not chapters or chapters[-1]["chapter"] != last):
        ended = chapters[-1]["chapter"] if chapters else None
        raise ValueError(f"{name}: the chapters end at {ended}, not {last}")
    return title, chapters, places, read_past


def _first_verse_row(rows, title_row, first, name):
    """The index of the verse row that opens chapter first, after the title row, and that
    verse's heading, (its row, its text), or None, as the module docstring says."""
    for start in range(title_row + 1, len(rows)):
        cells = rows[start]
        if (
            len(cells) >= 2
            and _numeral_or_none(_cell_text(cells[0])) == first
            and _numeral_or_none(_cell_text(cells[1])) == 1
        ):
            break
    else:
        raise ValueError(f"{name}: no verse row opens chapter {first}")
    for index in range(start - 1, title_row, -1):
        cells = rows[index]
        if len(cells) >= 2 and (_cell_text(cells[0]) or _cell_text(cells[1])):
            # A row of the chapters before, such as an unfinished verse: no heading.
            return start, None
        where = f"{name} row {index}"
        kind, (_c0, _c1, _c2, c3) = _classify(cells, where)
        if kind == "heading":
            return start, (index, c3)
        if kind != "empty":
            raise ValueError(f"{where}: a {kind} row before {first}:1")
    return start, None


def _classify(cells, where):
    if len(cells) != 4:
        raise ValueError(f"{where}: {len(cells)} cells")
    c0, c1, c2 = (_cell_text(paragraphs) for paragraphs in cells[:3])
    c3 = _paraphrase_cell_text(cells[3], where)
    styles = [
        {style for style, text in paragraphs if _clean(text)} for paragraphs in cells
    ]
    if not (c0 or c1 or c2 or c3):
        return "empty", (c0, c1, c2, c3)
    if c2 and len(styles[2]) == 1 and styles[2] <= _TITLE_STYLES and not c0 and not c1:
        if c3 and not styles[3] <= _HEADING_STYLES:
            raise ValueError(
                f"{where}: a title row whose paraphrase cell is not a heading"
            )
        return "title", (c0, c1, c2, c3)
    if not c0 and not c1 and (not c2 or c2 in _BREAK_MARKS) and c3:
        if not styles[3] or not styles[3] <= _HEADING_STYLES:
            raise ValueError(
                f"{where}: a lone paraphrase cell styled {styles[3]}: {c3!r}"
            )
        return "heading", (c0, c1, c2, c3)
    if not c0 and not c1 and c2 in _BREAK_MARKS and not c3:
        return "empty", (c0, c1, c2, c3)
    if c1 and c2 and c3:
        if styles[3] & _HEADING_STYLES:
            raise ValueError(f"{where}: a verse row styled as a heading")
        return "verse", (c0, c1, c2, c3)
    raise ValueError(f"{where}: unclassifiable row {[c0, c1, c2, c3]!r}")


def _paraphrase_cell_text(paragraphs, where):
    """The paraphrase cell's text: one paragraph at most, with nothing to interpret."""
    filled = [text for _style, text in paragraphs if _clean(text)]
    if len(filled) > 1:
        raise ValueError(f"{where}: the paraphrase cell has {len(filled)} paragraphs")
    if not filled:
        return ""
    text = _clean(filled[0])
    # Spaces at the ends are dropped; a line break or a tab anywhere is refused.
    if hazards := wikitext.wikitext_hazards(filled[0].strip(" ")):
        raise ValueError(f"{where}: the paraphrase cell has {hazards}: {text!r}")
    return text


def _cell_text(paragraphs):
    return _clean(" ".join(text for _style, text in paragraphs))


def _clean(text):
    """Make each whitespace run one space, and strip both ends."""
    return _WHITESPACE.sub(" ", text).strip()


def _numeral(text, where):
    number = _numeral_or_none(text)
    if number is None:
        raise ValueError(f"{where}: not a Hebrew numeral: {text!r}")
    return number


def _numeral_or_none(text):
    """The number of a cell's Hebrew numeral, or None if the cell holds none."""
    return hvn.STR_TO_INT_DIC.get(_NUMERAL_JUNK.sub("", text))


# The names of the title's style and of the headings' styles: the module docstring says
# which files use which.
_TITLE_STYLES = frozenset({"heading 2", "Heading 2"})
_HEADING_STYLES = frozenset({"heading 3", "heading 4", "Heading 4"})
_BREAK_MARKS = frozenset({"\N{HEBREW LETTER PE}", "\N{HEBREW LETTER SAMEKH}"})
_WHITESPACE = re.compile(r"\s+")
_NUMERAL_JUNK = re.compile(
    "[\"'\N{HEBREW PUNCTUATION GERESH}\N{HEBREW PUNCTUATION GERSHAYIM}\\s]"
)
