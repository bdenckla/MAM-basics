"""The tracked text of Miqra Mevoar, in/miqra-mevoar/<stem>.json, read and written.

Each file holds one book: its name, its Word file's name, size and SHA-256, and its
chapters, each verse with the heading before it, or null, and its paraphrase, in the
Word file's own mark order. The Bible column is not kept: it is MAM's text, which
Wikisource and MAM-simple already hold. Every read checks the record's whole shape.
"""

import json

from mb_cmn import file_io
from mb_cmn import paths
from miqra_mevoar import books


def json_dir():
    """The directory of the tracked JSON."""
    return paths.in_dir() / "miqra-mevoar"


def tracked_books():
    """The books that have tracked JSON, in stem order; raise if there are none."""
    stems = sorted(path.stem for path in json_dir().glob("*.json"))
    if not stems:
        raise ValueError(f"No Miqra Mevoar JSON in {json_dir()}")
    return [books.book_of_stem(stem) for stem in stems]


def read_record(book):
    """A book's tracked record, its shape checked."""
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
    """Raise unless record has exactly the keys and numbering of a book's record."""
    _require_keys(record, {"book", "source", "chapters"}, where)
    if record["book"] != book.bk39_name():
        raise ValueError(f"{where}: book {record['book']!r}, not {book.bk39_name()!r}")
    _require_keys(record["source"], {"file", "size", "sha256"}, f"{where} source")
    for number, chapter in enumerate(record["chapters"], start=1):
        _require_keys(chapter, {"chapter", "verses"}, f"{where} chapter {number}")
        if chapter["chapter"] != number:
            raise ValueError(
                f"{where}: chapter {chapter['chapter']} where {number} is due"
            )
        for verse_number, verse in enumerate(chapter["verses"], start=1):
            at = f"{where} {number}:{verse_number}"
            _require_keys(verse, {"verse", "heading", "paraphrase"}, at)
            if verse["verse"] != verse_number:
                raise ValueError(
                    f"{at}: verse {verse['verse']} where {verse_number} is due"
                )
        if not chapter["verses"]:
            raise ValueError(f"{where}: chapter {number} has no verses")
    if not record["chapters"]:
        raise ValueError(f"{where}: no chapters")


def _require_keys(mapping, keys, where):
    if not isinstance(mapping, dict) or set(mapping) != keys:
        shown = sorted(mapping) if isinstance(mapping, dict) else type(mapping).__name__
        raise ValueError(f"{where}: keys {shown}, not {sorted(keys)}")


def _json_path(book):
    return json_dir() / f"{book.stem}.json"
