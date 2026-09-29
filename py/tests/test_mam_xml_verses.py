"""MAM-simple through ``mb_cmn.mam_xml_verses``: a lint over the tree and a differential.

``py/mb_cmn/mam_xml_verses.py`` reads MAM-simple/xml-vtrad-mam/ for locating text in
manuscripts, and no program the mega runs calls it: the Evr. II B 55 page index uses it
by hand. So without these checks a new MAM-simple element, such as the planned
silluq-before-meteg, would surface only at the next hand use. Ben chose on 2026-09-26 to
add both checks:

1. THE LINT: every <verse> of every tracked MAM-simple/xml-vtrad-mam/*.xml passes
   ``get_verse_atoms``, and none of its atoms is empty. ``get_verse_atoms`` splits each
   entry of ``get_verse_words`` after every maqaf, so an entry ending in a maqaf would
   give an empty atom. Until the split moved into the reader on 2026-09-26, this lint
   checked the entries for a final maqaf instead.
2. THE DIFFERENTIAL: for every <book39> of every file, ``get_verses_in_range`` over the
   whole book returns exactly the verses that an independent scan of that <book39> finds,
   in document order. The scan reads each verse's chapter and verse from its osisID and
   shares no code with the reader. Until 2026-09-26 the reader took each file's first
   <book39> whatever book it was asked for, so 15 books were unreachable.

A tracked file missing from disk fails rather than skips, and the file, book and verse
counts are asserted non-zero, so an empty scan cannot pass.
"""

import subprocess
import re
import xml.etree.ElementTree as ET

from mb_cmn import paths
from mb_cmn.mam_xml_verses import get_verse_atoms, get_verses_in_range

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


def test_every_verse_passes_get_verse_atoms_with_no_empty_atom():
    verse_count = 0
    refused = []
    offenders = []
    for path in _tracked_xml_files():
        for verse in ET.parse(path).getroot().iter("verse"):
            verse_count += 1
            try:
                atoms = get_verse_atoms(verse)
            except ValueError as error:
                refused.append(str(error))
                continue
            if "" in atoms:
                offenders.append(f"{verse.attrib['osisID']}: {atoms}")
    assert verse_count > 0, "No <verse> was found in MAM-simple/xml-vtrad-mam/"
    assert not refused, f"{len(refused)} verses refused: {refused}"
    assert not offenders, f"Verses with an empty atom: {offenders}"


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


def _selected_parts(node):
    """Independently walk only the reader's declared Scripture nodes."""
    if node.tag in {"verse", "cant-combined", "kq-trivial", "sdt-target"}:
        if "text" in node.attrib:
            yield node.attrib["text"]
        else:
            for child in node:
                yield from _selected_parts(child)
    elif node.tag in {"text", "kq-k-velo-q"}:
        yield node.attrib["text"]
    elif node.tag == "slh-word":
        yield node.attrib["slhw-desc-0"]
    elif node.tag in {"lp-legarmeih", "lp-paseq"}:
        yield "\N{HEBREW PUNCTUATION PASEQ}"
    elif node.tag == "kq":
        ketiv = node.find("kq-k")
        assert ketiv is not None
        if "text" in ketiv.attrib:
            yield ketiv.attrib["text"]
        else:
            special = ketiv.find("slh-word")
            assert special is not None
            yield special.attrib["slhw-desc-0"]
    elif node.tag == "scrdfftar":
        target = node.find("sdt-target")
        assert target is not None
        yield from _selected_parts(target)
    elif node.tag == "cant-all-three":
        combined = node.find("cant-combined")
        assert combined is not None
        yield from _selected_parts(combined)
    elif node.tag in {
        "implicit-maqaf",
        "shirah-space",
        "spi-invnun",
        "spi-pe1",
        "spi-samekh1",
        "spi-pe2",
        "spi-samekh2",
        "spi-pe3",
        "spi-samekh3",
        "kq-q-velo-k",
        "kq-k-velo-q-maq",
        "good-ending",
    }:
        return
    else:
        raise ValueError(f"Unknown selected-source node <{node.tag}>")


def test_reader_atom_content_matches_selected_source_nodes_over_the_full_corpus():
    """Compare marks as well as letters, independently of the reader's word joining."""
    count = 0
    mismatches = []
    attached = {"\N{HEBREW PUNCTUATION PASEQ}", "\N{HEBREW PUNCTUATION SOF PASUQ}"}
    maqaf = "\N{HEBREW PUNCTUATION MAQAF}"
    for path in _tracked_xml_files():
        for verse in ET.parse(path).getroot().iter("verse"):
            expected = []
            for part in _selected_parts(verse):
                for atom in re.findall(rf"[^\s{maqaf}]+{maqaf}?", part):
                    if atom in attached:
                        assert expected, verse.attrib["osisID"]
                        expected[-1] += atom
                    else:
                        expected.append(atom)
            actual = get_verse_atoms(verse)
            count += 1
            if actual != expected:
                mismatches.append((verse.attrib["osisID"], actual, expected))
    assert count > 0
    assert not mismatches, f"Selected atom-content mismatches: {mismatches}"
