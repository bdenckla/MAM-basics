"""MAM-simple's books and verses, for checking a Word file against MAM and for the index.

MAM-simple (MAM-simple/json-vtrad-mam/) is the oracle for each book's chapters and
verse numbers, and for which verse each row of a Word file is: its Bible column is
MAM's text, copied from Wikisource. It is also the oracle for the books and chapters
that the base-chapter index links. _projected reads a verse's elements to text by a
closed dispatch, keeping a ketiv and its qere both, for a comparison of letters only.
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
    path = paths.require_mam_simple_vtrad_mam_dir() / book.mam_simple_file
    matches = [item for item in _books(path) if item["osisID"] == book.osis_id]
    if len(matches) != 1:
        raise ValueError(f"{path.name} has {len(matches)} books {book.osis_id!r}")
    for chapter in matches[0]["contents"]:
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
            osis_book, chapter_number, verse_number = verse["osisID"].split(".")
            if osis_book != book.osis_id:
                raise ValueError(f"{verse['osisID']} in book {book.osis_id}")
            yield (int(chapter_number), int(verse_number)), verse


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


# The petuha and setuma breaks, which stand between chapters and verses as well as in them.
_BREAKS = frozenset({"spi-pe2", "spi-pe3", "spi-samekh2", "spi-samekh3"})
_NON_LETTER = re.compile("[^\N{HEBREW LETTER ALEF}-\N{HEBREW LETTER TAV}]")
