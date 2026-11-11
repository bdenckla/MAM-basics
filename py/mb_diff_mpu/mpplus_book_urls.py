"""Book URLs and verse-reference formatting for MAM-parsed-plus diff reports.

Exports:
    mam_with_doc_href — build a change log's relative href to a MAM-with-doc verse
    wikisource_url   — build a Hebrew Wikisource te'amim URL
    ref_str          — verse reference like "1Samuel 3:4"
"""

from urllib.parse import quote

from mb_cmn import bib_locales as tbn
from mb_cmn.he_wikisource_url import he_taamim_url
from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn.mam_bknas_and_std_bknas import he_bk39_name
from mb_cmn import site_links

# The change logs' folder below the deploy root, beside MAM-with-doc's book pages: a
# change log's link to another page of the site is relative to it (mb_cmn/site_links.py).
# check_all renders the change logs into a temporary directory, so the folder is named
# here rather than taken from the path a change log is written to.
_CHANGE_LOG_FOLDER = "MAM-with-doc/change-log"


def mam_with_doc_href(book, chapter, verse):
    """A change log's relative href to a verse in MAM-with-doc, for a canonical bk39 id."""
    osdf = tbn.ordered_short_dash_full_39(book)
    # quote matters for exactly one osdf: "E1-Song of Songs" has a space in it.
    page = quote(f"{osdf}.html")
    return site_links.site_href_from_folder(
        _CHANGE_LOG_FOLDER, f"MAM-with-doc/{page}#c{chapter}v{verse}"
    )


def wikisource_url(book, chapter):
    """Build a Hebrew Wikisource te'amim URL for a canonical bk39 id."""
    he_chnu = hvn.INT_TO_STR_DIC[chapter]
    name_he = he_bk39_name(book)
    return he_taamim_url(name_he, he_chnu)


def ref_str(diff):
    """Format a verse reference using the canonical bk39 id."""
    return f"{diff['book']} {diff['chapter']}:{diff['verse']}"
