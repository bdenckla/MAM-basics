"""Differential: each tracked Miqra Mevoar book has MAM-simple's chapters and verses.

For every in/miqra-mevoar/*.json, the book's chapters, and each chapter's verse numbers,
must equal those of MAM-simple (MAM-simple/json-vtrad-mam/), the oracle against which
`py/main_miqra_mevoar.py check` also measures the Word files. The tracked headings and
paraphrases are also linted for what py/miqra_mevoar/wikitext.py refuses: a line break
or another control character, a space at either end, and wikitext. An empty directory,
or a book that MAM-simple lacks, fails rather than skips.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_miqra_mevoar_versification.py
"""

import pytest

from miqra_mevoar import books
from miqra_mevoar import mam_simple
from miqra_mevoar import tracked
from miqra_mevoar import wikitext

_STEMS = sorted(path.stem for path in tracked.json_dir().glob("*.json"))


def test_the_directory_holds_json():
    """Fail, rather than parametrize nothing, when no book is tracked."""
    assert _STEMS, f"no JSON in {tracked.json_dir()}"


@pytest.mark.parametrize("stem", _STEMS)
def test_versification_equals_mam_simple(stem):
    book = books.book_of_stem(stem)
    record = tracked.read_record(book)
    keys = [
        (chapter["chapter"], verse["verse"])
        for chapter in record["chapters"]
        for verse in chapter["verses"]
    ]
    assert keys == mam_simple.verse_keys(book)


@pytest.mark.parametrize("stem", _STEMS)
def test_text_has_nothing_mediawiki_would_change(stem):
    problems = []
    for chapter in tracked.read_record(books.book_of_stem(stem))["chapters"]:
        for verse in chapter["verses"]:
            where = f"{stem} {chapter['chapter']}:{verse['verse']}"
            for field in ("heading", "paraphrase"):
                text = verse[field]
                if text is None and field == "heading":
                    continue
                if not isinstance(text, str) or not text:
                    problems.append(f"{where} {field}: {text!r}")
                elif hazards := wikitext.wikitext_hazards(text):
                    problems.append(f"{where} {field}: {hazards}")
    assert not problems, "\n".join(problems)
