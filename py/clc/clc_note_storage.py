"""Operation-scoped storage for committed UXLC note-page HTML.

Each populated book has one JSON object under ``uxlc/in/UXLC-notes/``.  The
object maps the former HTML filename to the complete HTML string.  A
``NoteStorageOperation`` loads each book at most once; callers create a new
operation when they need to observe changes written by an earlier operation.
"""

import json
from pathlib import Path

from mb_cmn import file_io
import uxlc_paths


def note_filename(book_id, ch, v, position, code):
    """Return the storage key for one note page."""
    return f"{book_id}.{ch}.{v}.{position}-{code}.html"


class NoteStorageOperation:
    """Load and update UXLC note books during one explicit operation."""

    def __init__(self, notes_dir=None):
        self.notes_dir = Path(notes_dir or uxlc_paths.uxlc_notes_dir())
        self._books = {}

    def book_path(self, book_id):
        """Return the JSON path for ``book_id``."""
        return self.notes_dir / f"{book_id}.json"

    def page_text(self, book_id, ch, v, position, code):
        """Return one stored HTML string, or ``None`` when the key is absent."""
        filename = note_filename(book_id, ch, v, position, code)
        return self._book(book_id).get(filename)

    def has_page(self, book_id, ch, v, position, code):
        """Return whether one note-page key is already stored."""
        filename = note_filename(book_id, ch, v, position, code)
        return filename in self._book(book_id)

    def add_page(self, book_id, ch, v, position, code, page_text):
        """Atomically add an absent page without replacing existing entries.

        Return ``True`` when the page was added and ``False`` when the page was
        already present.  The operation's cache changes only after the atomic
        replacement succeeds.
        """
        filename = note_filename(book_id, ch, v, position, code)
        entries = self._book(book_id)
        if filename in entries:
            return False
        updated = dict(entries)
        updated[filename] = page_text
        ordered = {key: updated[key] for key in sorted(updated)}
        file_io.json_dump_to_file_path(ordered, self.book_path(book_id))
        self._books[book_id] = ordered
        return True

    def iter_pages(self):
        """Yield ``(book_id, filename, HTML)`` in deterministic order."""
        if not self.notes_dir.exists():
            return
        for path in sorted(self.notes_dir.iterdir(), key=lambda item: item.name):
            if not path.is_file() or path.suffix != ".json":
                raise ValueError(f"unexpected UXLC note storage entry: {path}")
            book_id = path.stem
            for filename, page_text in self._book(book_id).items():
                yield book_id, filename, page_text

    def _book(self, book_id):
        if book_id not in self._books:
            self._books[book_id] = _read_book(self.book_path(book_id), book_id)
        return self._books[book_id]


def _read_book(path, book_id):
    if not path.exists():
        return {}
    text = path.read_bytes().decode("utf-8")
    entries = json.loads(text, object_pairs_hook=_reject_duplicate_keys)
    if not isinstance(entries, dict):
        raise ValueError(f"UXLC note book must be a JSON object: {path}")
    expected_prefix = f"{book_id}."
    for filename, page_text in entries.items():
        if (
            not isinstance(filename, str)
            or Path(filename).name != filename
            or not filename.startswith(expected_prefix)
            or not filename.endswith(".html")
        ):
            raise ValueError(f"invalid UXLC note filename in {path}: {filename!r}")
        if not isinstance(page_text, str):
            raise ValueError(f"UXLC note page must be a string in {path}: {filename!r}")
    return {key: entries[key] for key in sorted(entries)}


def _reject_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key in UXLC note storage: {key!r}")
        result[key] = value
    return result
