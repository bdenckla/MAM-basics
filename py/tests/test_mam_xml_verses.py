"""MAM-simple through ``py_ac_loc.mam_xml_verses``: a lint over the tree and a differential.

``py/py_ac_loc/mam_xml_verses.py`` reads MAM-simple/xml-vtrad-mam/ for locating text in
manuscripts, and everything that calls it is hand-run, outside the mega. So without these
checks a new MAM-simple element, such as the planned silluq-before-meteg, would surface
only at the next hand run. Ben chose on 2026-09-26 to add both checks:

1. THE LINT: every <verse> of every tracked MAM-simple/xml-vtrad-mam/*.xml passes
   ``get_verse_words``, and no entry of its ``words`` ends in a maqaf. Both flat-stream
   generators split each entry after every maqaf, so such an entry would give an empty
   atom.
2. THE DIFFERENTIAL: for every <book39> of every file, ``get_verses_in_range`` over the
   whole book returns exactly the verses that an independent scan of that <book39> finds,
   in document order. The scan reads each verse's chapter and verse from its osisID and
   shares no code with the reader. Until 2026-09-26 the reader took each file's first
   <book39> whatever book it was asked for, so 15 books were unreachable.

A tracked file missing from disk fails rather than skips, and the file, book and verse
counts are asserted non-zero, so an empty scan cannot pass.
"""

import subprocess
import xml.etree.ElementTree as ET

from mb_cmn import paths
from py_ac_loc.mam_xml_verses import get_verse_words, get_verses_in_range

_MAQAF = "\N{HEBREW PUNCTUATION MAQAF}"
_WHOLE_BOOK = ((1, 1), (999, 999))


def _tracked_xml_files():
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", "MAM-simple/xml-vtrad-mam/*.xml"],
        cwd=paths.repo_root(),
        capture_output=True,
        encoding="utf-8",
        check=True,
    )
    rels = [name for name in result.stdout.split("\0") if name]
    assert rels, "No tracked MAM-simple/xml-vtrad-mam/*.xml file was found"
    return [paths.repo_root() / rel for rel in rels]


def test_every_verse_passes_get_verse_words_with_no_entry_ending_in_a_maqaf():
    verse_count = 0
    refused = []
    offenders = []
    for path in _tracked_xml_files():
        for verse in ET.parse(path).getroot().iter("verse"):
            verse_count += 1
            try:
                words = get_verse_words(verse)["words"]
            except ValueError as error:
                refused.append(str(error))
                continue
            for entry in words:
                if entry.endswith(_MAQAF):
                    offenders.append(f"{verse.attrib['osisID']}: {entry}")
    assert verse_count > 0, "No <verse> was found in MAM-simple/xml-vtrad-mam/"
    assert not refused, f"{len(refused)} verses refused: {refused}"
    assert not offenders, f"Entries ending in a maqaf: {offenders}"


def _scanned_cvs(book39):
    """The chapter:verse label of every <verse> under book39, from its osisID alone."""
    cvs = []
    for verse in book39.iter("verse"):
        book, chapter, verse_number = verse.attrib["osisID"].split(".")
        assert book == book39.attrib["osisID"], verse.attrib["osisID"]
        cvs.append(f"{chapter}:{verse_number}")
    return cvs


def test_get_verses_in_range_returns_every_verse_of_every_book():
    book_count = 0
    verse_count = 0
    mismatches = []
    for path in _tracked_xml_files():
        for book39 in ET.parse(path).getroot().iter("book39"):
            book_count += 1
            book = book39.attrib["osisID"]
            expected = _scanned_cvs(book39)
            got = [v["cv"] for v in get_verses_in_range(path, book, *_WHOLE_BOOK)]
            verse_count += len(got)
            if got != expected:
                mismatches.append(f"{path.name} {book}: {len(got)} of {len(expected)}")
    assert book_count > 0, "No <book39> was found in MAM-simple/xml-vtrad-mam/"
    assert verse_count > 0, "get_verses_in_range returned no verse at all"
    assert not mismatches, f"Books whose verses differ from the scan: {mismatches}"
