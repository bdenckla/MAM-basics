"""Read the complete closed display release without accessing a sibling checkout."""

import json

from mb_cmn import bib_locales, paths
from phonetic_mam import display_schema, test_page_display


def data_path(book_id):
    """Return the canonical data filename for one recognized book."""
    display_schema.require(book_id in bib_locales.ALL_BK39_IDS, "unknown book")
    stem = bib_locales.ordered_short_dash_full_39(book_id)
    return paths.phonetic_mam_dir() / "data" / f"{stem}.json"


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        display_schema.require(key not in result, f"duplicate JSON key: {key}")
        result[key] = value
    return result


def read_book(book_id):
    """Read and validate one book; a missing or empty input is an error."""
    path = data_path(book_id)
    book = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object
    )
    # canonical_bytes validates before serialization; do not walk the book twice.
    canonical = display_schema.canonical_bytes(book)
    display_schema.require(book["book"] == book_id, "filename/book identity differs")
    display_schema.require(
        path.read_bytes() == canonical,
        f"noncanonical JSON representation: {path.name}",
    )
    return book


def require_complete_book_set():
    """Require exactly the complete canonical set, with no unreviewed sidecars."""
    directory = paths.phonetic_mam_dir() / "data"
    expected = {data_path(book).name for book in bib_locales.ALL_BK39_IDS}
    display_schema.require(directory.is_dir(), "public Phonetic MAM data is absent")
    actual = {path.name for path in directory.iterdir()}
    display_schema.require(
        actual == expected, "public book set is incomplete or extended"
    )


def iter_books():
    """Yield validated books in canonical order, with book-scoped memory use."""
    require_complete_book_set()
    for book_id in bib_locales.ALL_BK39_IDS:
        yield read_book(book_id)


def validate_complete_release():
    """Check closed shapes, canonical bytes, identities and every required book."""
    root = paths.phonetic_mam_dir()
    expected = {
        root / "README.md",
        root / "schema" / "phonetic-mam-public-v1.schema.json",
        root / "examples" / "display.json",
        *(data_path(book) for book in bib_locales.ALL_BK39_IDS),
    }
    display_schema.require(
        {path for path in root.rglob("*") if path.is_file()} == expected,
        "public release contains missing or unapproved artifacts",
    )
    for _book in iter_books():
        pass
    read_examples()


def read_examples():
    """Read exactly the five public example displays, without source fixtures."""
    directory = paths.phonetic_mam_dir() / "examples"
    display_schema.require(directory.is_dir(), "example display data is absent")
    display_schema.require(
        {path.name for path in directory.iterdir()} == {"display.json"},
        "unknown example release artifact",
    )
    path = directory / "display.json"
    payload = json.loads(
        path.read_text(encoding="utf-8"), object_pairs_hook=_unique_object
    )
    display_schema.require(
        path.read_bytes() == test_page_display.canonical_bytes(payload),
        "noncanonical example display data",
    )
    return payload
