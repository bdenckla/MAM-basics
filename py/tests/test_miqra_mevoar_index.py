"""Differential: the base-chapter index links exactly MAM-simple's chapters, in order.

py/miqra_mevoar/index_page.py generates the book sections of Miqra Mevoar's base-chapter
index from its own table of the 39 books and from MAM-simple. Read back by the index's
closed parser, those sections must link exactly the chapters of MAM-simple
(MAM-simple/json-vtrad-mam/), book by book in the order of py/mb_cmn/bib_locales.py's
ALL_BK39_IDS, each to the title that py/miqra_mevoar/wikitext.py's page_title gives,
with the chapter's numeral as the link's text. The oracle finds each book in MAM-simple
by its OSIS abbreviation in py/mb_misc/osis_book_abbrevs.py, and each chapter by its
chapter element's osisID, independently of the index's table. A MAM-simple book outside
the 39, and a MAM-simple with no books, fail rather than skip.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_miqra_mevoar_index.py
"""

import json

from mb_cmn import bib_locales
from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn import mam_bknas_and_std_bknas
from mb_cmn import paths
from mb_misc import osis_book_abbrevs
from miqra_mevoar import index_page
from miqra_mevoar import wikitext


def test_the_index_links_every_chapter_of_mam_simple():
    chapters = _mam_simple_chapters()
    assert chapters, f"no books in {paths.require_mam_simple_vtrad_mam_dir()}"
    expected = []
    for bk39id in bib_locales.ALL_BK39_IDS:
        mam_book = mam_bknas_and_std_bknas.BK39ID_TO_MAM_HBNP[bk39id]
        for number in chapters.pop(osis_book_abbrevs.BOOK_ABBREVS[bk39id]):
            expected.append(
                (wikitext.page_title(mam_book, number), hvn.INT_TO_STR_DIC[number])
            )
    assert not chapters, f"MAM-simple books outside the 39: {sorted(chapters)}"
    book_sections = index_page.read_sections(
        index_page.section_lines(index_page.sections())
    )
    linked = [
        link for section in book_sections for run in section.runs for link in run.links
    ]
    assert linked == expected


def _mam_simple_chapters():
    """Each MAM-simple book's chapter numbers, in its order, keyed by its osisID."""
    chapters = {}
    for path in sorted(paths.require_mam_simple_vtrad_mam_dir().glob("*.json")):
        for item in json.loads(path.read_text(encoding="utf-8"))["contents"]:
            if item["type"] in _BREAKS:
                continue
            assert item["type"] == "book39", f"{path.name}: {item['type']}"
            assert item["osisID"] not in chapters, f"{item['osisID']} twice"
            numbers = []
            for chapter in item["contents"]:
                if chapter["type"] in _BREAKS:
                    continue
                assert chapter["type"] == "chapter", f"{path.name}: {chapter['type']}"
                book, number = chapter["osisID"].split(".")
                assert book == item["osisID"], chapter["osisID"]
                numbers.append(int(number))
            chapters[item["osisID"]] = numbers
    return chapters


# The petuha and setuma breaks, which stand between books and chapters too.
_BREAKS = frozenset({"spi-pe2", "spi-pe3", "spi-samekh2", "spi-samekh3"})
