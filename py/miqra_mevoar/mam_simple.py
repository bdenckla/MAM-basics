"""MAM-simple's books, verses and breaks, for checking a Word file and for the pages.

MAM-simple (MAM-simple/json-vtrad-mam/) is the oracle for each book's chapters and
verse numbers, and for which verse each row of a Word file is: its Bible column is
MAM's text, copied from Wikisource. It is also the oracle for the books and chapters
that the base-chapter index links, and for the verses and the breaks between them that
a display page shows. _projected reads a verse's elements to text by a closed dispatch,
keeping a ketiv and its qere both, for a comparison of letters only: so it reads a hung
letter, such as the nun of Judges 18:30, as its letter, and keeps a word that is read
but not written, such as the one of Judges 20:13, as it keeps a qere. verse_breaks reads
the petuha and setuma break elements by a closed dispatch of their places, and
scribal_difference_breaks gives the note of each break that a scribal-difference element
holds.
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


def record_verse_keys(book):
    """Each (chapter, verse) that a book's tracked record holds, in MAM-simple's order:
    the verses of the chapters that the book's entry in books.BOOKS declares, or of every
    chapter; raise if the declared chapters are not within the book's."""
    keys = verse_keys(book)
    if book.chapters is None:
        return keys
    first, last = book.chapters
    numbers = list(dict.fromkeys(chapter for chapter, _verse in keys))
    if not (first <= last and first in numbers and last in numbers):
        raise ValueError(
            f"{book.osis_id}: chapters {first} to {last} are not within MAM-simple's"
            f" {numbers[0]} to {numbers[-1]}"
        )
    return [key for key in keys if first <= key[0] <= last]


def verse_letters(book):
    """The Hebrew letters of each verse of a book, keyed by (chapter, verse)."""
    return {key: _NON_LETTER.sub("", _projected(verse)) for key, verse in _verses(book)}


def verse_breaks(book):
    """The break, PETUHA or SETUMA, before each verse of a book that has one, by key.

    A break element between two chapters, between two verses or as a verse's last child
    stands before the book's next verse. So does the break of a scribal-difference
    element that is a verse's last child and whose target holds that break and nothing
    else, as at the ends of Exodus 33:23 and of Leviticus 7:21 and 7:27, where MAM's
    note says which tradition lacks the petuha or doubts it. A break among a verse's
    children, with a child before it and a child after it, is inside the verse, which
    shows it, so it is left out. A break anywhere else raises: first or last among a
    book's chapters or a chapter's verses, a verse's first child, one nested deeper in a
    verse in any other way, and one with no verse of the book after it; so does a
    second break before the same verse. A break between two books stands outside both
    and is not read.
    """
    return {key: kind for key, (kind, _note) in _breaks(book).items()}


def scribal_difference_breaks(book):
    """The note of each break that verse_breaks reads from a scribal-difference element,
    keyed by the verse before which the break stands."""
    return {key: note for key, (_kind, note) in _breaks(book).items() if note}


def _breaks(book):
    """(kind, note) of the break before each verse of a book that has one, by key, as
    verse_breaks describes; the note is a scribal-difference element's, or None."""
    found, pending = {}, None
    chapters = _book_element(book)["contents"]
    for at, chapter in enumerate(chapters):
        if chapter["type"] in _BREAKS:
            where = f"{book.osis_id}: a break that is not between two chapters"
            pending = _break_kind(
                chapter, None, pending, _between(chapters, at, "chapter"), where
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
                    verse, None, pending, _between(verses, verse_at, "verse"), where
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
                last = child_at == len(children) - 1
                if child["type"] not in _BREAKS:
                    if not _holds_break(child):
                        continue
                    if child["type"] != "scrdfftar" or not last:
                        raise ValueError(
                            f"{verse['osisID']}: a break nested in a {child['type']}"
                        )
                    held, note = _scribal_difference_break(child, verse["osisID"])
                    pending = _break_kind(held, note, pending, True, verse["osisID"])
                elif child_at == 0:
                    raise ValueError(f"{verse['osisID']}: a break begins the verse")
                elif last:
                    pending = _break_kind(child, None, pending, True, verse["osisID"])
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


def _break_kind(element, note, pending, placed, where):
    """The kind of a break that stands before the next verse, and its note; raise if it
    cannot stand there."""
    if not placed:
        raise ValueError(where)
    if pending is not None:
        raise ValueError(f"{where}: a second break before one verse")
    return _BREAK_KINDS[element["type"]], note


def _scribal_difference_break(element, where):
    """The break that a scribal-difference element's target holds, and the element's
    note; raise unless the element has a target that holds one break and nothing else,
    and then a note."""
    keys = {"type", "sdt-starpos", "contents"}
    if set(element) != keys or element["sdt-starpos"] not in _STAR_POSITIONS:
        raise ValueError(f"{where}: a scribal-difference element of an unknown shape")
    parts = element["contents"]
    if [part["type"] for part in parts] != ["sdt-target", "sdt-note"]:
        raise ValueError(f"{where}: a scribal-difference element of other parts")
    target, note = parts
    held = target.get("contents", [])
    if set(target) != {"type", "contents"} or len(held) != 1:
        raise ValueError(f"{where}: a scribal-difference target with more than a break")
    if held[0]["type"] not in _BREAKS:
        raise ValueError(f"{where}: a scribal-difference target with a break nested")
    text = note.get("text")
    if set(note) != {"type", "text"} or not isinstance(text, str) or not text:
        raise ValueError(f"{where}: a scribal-difference note of an unknown shape")
    return held[0], text


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
    if kind in (
        "text",
        "kq-k",
        "kq-trivial",
        "kq-q-velo-k",
        "letter-small",
        "letter-large",
        "letter-hung",
    ):
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
# The sides of its target on which a scribal-difference element's note belongs.
_STAR_POSITIONS = frozenset({"before-word", "after-word"})
_NON_LETTER = re.compile("[^\N{HEBREW LETTER ALEF}-\N{HEBREW LETTER TAV}]")
