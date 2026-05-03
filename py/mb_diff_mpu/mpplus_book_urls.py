"""Book URLs and verse-reference formatting for MAM-parsed-plus diff reports.

Exports:
    mam_with_doc_url — build a MAM-with-doc GitHub Pages URL
    wikisource_url   — build a Hebrew Wikisource te'amim URL
    ref_str          — verse reference like "1Samuel 3:4"
"""

from mb_cmn import bib_locales as tbn
from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn.mam_bknas_and_std_bknas import he_bk39_name
from mb_cmn.url_percent import pct_path_component


def mam_with_doc_url(book, chapter, verse):
    """Build a MAM-with-doc GitHub Pages URL for a canonical bk39 id."""
    osdf = tbn.ordered_short_dash_full_39(book)
    return f"https://bdenckla.github.io/MAM-with-doc/{osdf}.html#c{chapter}v{verse}"


def wikisource_url(book, chapter):
    """Build a Hebrew Wikisource te'amim URL for a canonical bk39 id."""
    he_chnu = hvn.INT_TO_STR_DIC[chapter]
    name_he = he_bk39_name(book)
    page_title = pct_path_component(f"{name_he}_{he_chnu}/טעמים", safe="/")
    return f"https://he.wikisource.org/wiki/{page_title}"


def ref_str(diff):
    """Format a verse reference using the canonical bk39 id."""
    return f"{diff['book']} {diff['chapter']}:{diff['verse']}"
