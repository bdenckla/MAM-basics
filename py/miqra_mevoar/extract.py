"""Extract a Miqra Mevoar book from its Word file: each verse's heading and paraphrase.

Each book is one table of four right-to-left columns: the chapter numeral, only on a
chapter's first verse; the verse numeral; the Bible text, MAM copied from Wikisource;
and the paraphrase. _classify names each row's kind by a closed dispatch:

  title    the Bible cell alone, styled "heading 2", holds the book's pointed name; the
           paraphrase cell may also hold the heading of the first verse, as Joshua's does
  heading  the paraphrase cell alone, styled "heading 3" or "heading 4", holds the
           heading of the next verse; the Bible cell may hold a pe or a samekh, the
           petuha or setuma marker before it, as one of Joel's does
  verse    the verse numeral, the Bible text and the paraphrase, and the chapter numeral
           on a chapter's first verse
  empty    no text, or only a pe or a samekh in the Bible cell

Any other row is an error, as is a second title row, a heading with no verse after it,
or a chapter or verse number out of sequence. So is a heading or paraphrase that has a
line break, a tab or anything else MediaWiki would interpret or transform. A cell's
text joins its paragraphs, and each run of whitespace in it becomes one space.
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
        record, _bible = extract_book(docx_path, book)
        tracked.write_record(book, record)
        verses = [
            verse for chapter in record["chapters"] for verse in chapter["verses"]
        ]
        headings = sum(verse["heading"] is not None for verse in verses)
        print(
            f"{book.stem}: {len(record['chapters'])} chapters, {len(verses)} verses,"
            f" {headings} headings"
        )


def docx_paths(directory):
    """Every .docx in directory, in name order; exit if there is none."""
    found = sorted(Path(directory).glob("*.docx"))
    if not found:
        raise SystemExit(f"No .docx file in {directory}")
    return found


def extract_book(docx_path, book):
    """A book's record for its tracked JSON, and each verse's Bible cell by (chapter, verse)."""
    data = docx_path.read_bytes()
    title, chapters = _build(docx_table.read_rows(docx_path), docx_path.name)
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
    return record, bible


def _build(rows, name):
    chapters, pending, title = [], None, None
    for index, cells in enumerate(rows):
        where = f"{name} row {index}"
        kind, (c0, c1, c2, c3) = _classify(cells, where)
        if kind == "empty":
            continue
        if kind == "title":
            if title is not None or chapters or pending is not None:
                raise ValueError(
                    f"{where}: a title row after the book's first row of text"
                )
            title, pending = c2, c3 or None
            continue
        if title is None:
            raise ValueError(f"{where}: a {kind} row before the title row")
        if kind == "heading":
            if pending is not None:
                raise ValueError(f"{where}: a heading after the heading {pending!r}")
            pending = c3
            continue
        if c0:
            number = _numeral(c0, f"{where}, chapter cell")
            if number != len(chapters) + 1:
                raise ValueError(f"{where}: chapter {number} after {len(chapters)}")
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
        pending = None
    if title is None:
        raise ValueError(f"{name}: no title row")
    if pending is not None:
        raise ValueError(f"{name}: the heading {pending!r} has no verse after it")
    return title, chapters


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
    if c2 and styles[2] == {_TITLE_STYLE} and not c0 and not c1:
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
    key = _NUMERAL_JUNK.sub("", text)
    if key not in hvn.STR_TO_INT_DIC:
        raise ValueError(f"{where}: not a Hebrew numeral: {text!r}")
    return hvn.STR_TO_INT_DIC[key]


_TITLE_STYLE = "heading 2"
_HEADING_STYLES = frozenset({"heading 3", "heading 4"})
_BREAK_MARKS = frozenset({"\N{HEBREW LETTER PE}", "\N{HEBREW LETTER SAMEKH}"})
_WHITESPACE = re.compile(r"\s+")
_NUMERAL_JUNK = re.compile(
    "[\"'\N{HEBREW PUNCTUATION GERESH}\N{HEBREW PUNCTUATION GERSHAYIM}\\s]"
)
