"""MAM-simple's books, verses and breaks, for checking a Word file and for the pages.

MAM-simple (MAM-simple/json-vtrad-mam/) is the oracle for each book's chapters and
verse numbers, and for which verse each row of a Word file is: its Bible column is
MAM's text, copied from Wikisource. It is also the oracle for the books and chapters
that the base-chapter index links, and for the verses and the breaks between them that
a display page shows. _projected reads a verse's elements to text by a closed dispatch,
keeping a ketiv and its qere both, for a comparison of letters only. verse_breaks reads
the petuha and setuma break elements by a closed dispatch of their places.
"""

import json
import re

from mb_cmn import paths


def book_ids():
    """(file name, OSIS id) of every book in MAM-simple, file by file in name order."""
    return [
        (path.name, item["osisID"])
        for path in sorted(paths.require_mam_simple_vtrad_mam_dir().glob("*.json"))
        for item in _books(path)
    ]


def chapter_numbers(book):
    """The numbers of a book's chapters, in MAM-simple's order."""
    return list(dict.fromkeys(chapter for chapter, _verse in verse_keys(book)))


def verse_keys(book):
    """Each (chapter, verse) of a book, in MAM-simple's order."""
    return [key for key, _verse in _verses(book)]


def verse_letters(book):
    """The Hebrew letters of each verse of a book, keyed by (chapter, verse)."""
    return {key: _NON_LETTER.sub("", _projected(verse)) for key, verse in _verses(book)}


def verse_breaks(book):
    """The break, PETUHA or SETUMA, before each verse of a book that has one, by key.

    A break element between two chapters, between two verses or as a verse's last child
    stands before the book's next verse. A break among a verse's children, with a child
    before it and a child after it, is inside the verse, which shows it, so it is left
    out. A break anywhere else raises: first or last among a book's chapters or a
    chapter's verses, a verse's first child, one nested deeper in a verse, and one with
    no verse of the book after it; so does a second break before the same verse. A break
    between two books stands outside both and is not read.
    """
    found, pending = {}, None
    chapters = _book_element(book)["contents"]
    for at, chapter in enumerate(chapters):
        if chapter["type"] in _BREAKS:
            where = f"{book.osis_id}: a break that is not between two chapters"
            pending = _break_kind(
                chapter, pending, _between(chapters, at, "chapter"), where
            )
            continue
        if chapter["type"] != "chapter":
            raise ValueError(
                f"{book.osis_id}: unknown chapter element {chapter['type']}"
            )
        verses = chapter["contents"]
        for verse_at, verse in enumerate(verses):
            if verse["type"] in _BREAKS:
                where = f"{chapter['osisID']}: a break that is not between two verses"
                pending = _break_kind(
                    verse, pending, _between(verses, verse_at, "verse"), where
                )
                continue
            if verse["type"] != "verse":
                raise ValueError(
                    f"{book.osis_id}: unknown verse element {verse['type']}"
                )
            if pending is not None:
                found[_verse_key(book, verse)], pending = pending, None
            children = verse.get("contents", [])
            for child_at, child in enumerate(children):
                if child["type"] not in _BREAKS:
                    if _holds_break(child):
                        raise ValueError(
                            f"{verse['osisID']}: a break nested in a {child['type']}"
                        )
                elif child_at == 0:
                    raise ValueError(f"{verse['osisID']}: a break begins the verse")
                elif child_at == len(children) - 1:
                    pending = _break_kind(child, pending, True, verse["osisID"])
    if pending is not None:
        raise ValueError(f"{book.osis_id}: a break after the book's last verse")
    return found


def _books(path):
    """The book elements of a MAM-simple file, skipping the breaks between two books."""
    data = json.loads(path.read_text(encoding="utf-8"))
    for item in data["contents"]:
        if item["type"] in _BREAKS:
            continue
        if item["type"] != "book39":
            raise ValueError(f"{path.name}: unknown book element {item['type']}")
        yield item


def _verses(book):
    for chapter in _book_element(book)["contents"]:
        if chapter["type"] in _BREAKS:
            continue
        if chapter["type"] != "chapter":
            raise ValueError(
                f"{book.osis_id}: unknown chapter element {chapter['type']}"
            )
        for verse in chapter["contents"]:
            if verse["type"] in _BREAKS:
                continue
            if verse["type"] != "verse":
                raise ValueError(
                    f"{book.osis_id}: unknown verse element {verse['type']}"
                )
            yield _verse_key(book, verse), verse


def _book_element(book):
    path = paths.require_mam_simple_vtrad_mam_dir() / book.mam_simple_file
    matches = [item for item in _books(path) if item["osisID"] == book.osis_id]
    if len(matches) != 1:
        raise ValueError(f"{path.name} has {len(matches)} books {book.osis_id!r}")
    return matches[0]


def _verse_key(book, verse):
    osis_book, chapter_number, verse_number = verse["osisID"].split(".")
    if osis_book != book.osis_id:
        raise ValueError(f"{verse['osisID']} in book {book.osis_id}")
    return int(chapter_number), int(verse_number)


def _between(siblings, at, kind):
    """Whether siblings[at] has an element of this kind on either side of it."""
    return (
        0 < at < len(siblings) - 1
        and siblings[at - 1]["type"] == kind
        and siblings[at + 1]["type"] == kind
    )


def _break_kind(element, pending, placed, where):
    """The kind of a break that stands before the next verse; raise if it cannot."""
    if not placed:
        raise ValueError(where)
    if pending is not None:
        raise ValueError(f"{where}: a second break before one verse")
    return _BREAK_KINDS[element["type"]]


def _holds_break(node):
    """Whether a break element is anywhere among node's descendants."""
    return any(
        child["type"] in _BREAKS or _holds_break(child)
        for child in node.get("contents", ())
    )


def _projected(node):
    kind = node["type"]
    if kind in ("verse", "kq-q"):
        if ("text" in node) == ("contents" in node):
            raise ValueError(f"a {kind} element needs text or contents: {sorted(node)}")
        if "text" in node:
            return node["text"]
        return "".join(_projected(child) for child in node["contents"])
    if kind in ("text", "kq-k", "kq-trivial", "letter-small", "letter-large"):
        return node["text"]
    if kind == "kq":
        return " ".join(_projected(child) for child in node["contents"])
    if kind == "slh-word":
        return "".join(_projected(child) for child in node["contents"])
    if kind in _BREAKS or kind in ("lp-legarmeih", "lp-paseq", "shirah-space"):
        return " "
    if kind == "good-ending":
        return ""
    raise ValueError(f"unknown MAM-simple element {kind}")


PETUHA = "petuha"
SETUMA = "setuma"
# The petuha and setuma breaks, which stand between chapters and verses as well as in
# them. A pe3 is MAM's petuha without a blank line, and a samekh3 its setuma in mid-line.
_BREAK_KINDS = {
    "spi-pe2": PETUHA,
    "spi-pe3": PETUHA,
    "spi-samekh2": SETUMA,
    "spi-samekh3": SETUMA,
}
_BREAKS = frozenset(_BREAK_KINDS)
_NON_LETTER = re.compile("[^\N{HEBREW LETTER ALEF}-\N{HEBREW LETTER TAV}]")
