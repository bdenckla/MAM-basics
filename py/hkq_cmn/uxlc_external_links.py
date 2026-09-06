"""External per-verse links for the UXLC-corrections report.

Everything here is derived from a bk39 id through already-vendored ``mb_cmn``
helpers, so all 39 books work; only the tanach.us abbreviations need a table of
their own, and that table is complete rather than scoped to the books the
current emails happen to cover.
"""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import quote

from mb_cmn import bib_locales as tbn

# The book code tanach.us puts in a Tanach.xml query, e.g. Tanach.xml?Ex7:20.
# Copied whole from MAM-basics py/uxlc_fois/fois_mark_grammar_html.py's
# _TANACH_US_BOOK_CODES; that repo also has a py_uxlc table of the same codes,
# but the py_uxlc one is missing Nahum and Habakkuk.
TANACH_US_BOOK_CODES = {
    "Genesis": "Gen",
    "Exodus": "Ex",
    "Levit": "Lev",
    "Numbers": "Num",
    "Deuter": "Deut",
    "Joshua": "Josh",
    "Judges": "Judg",
    "1Samuel": "1Sam",
    "2Samuel": "2Sam",
    "1Kings": "1Kings",
    "2Kings": "2Kings",
    "Isaiah": "Isa",
    "Jeremiah": "Jer",
    "Ezekiel": "Ezek",
    "Hosea": "Hos",
    "Joel": "Joel",
    "Amos": "Am",
    "Obadiah": "Ob",
    "Jonah": "Jon",
    "Micah": "Mic",
    "Nahum": "Nah",
    "Habakkuk": "Hab",
    "Tsefaniah": "Zeph",
    "Haggai": "Hag",
    "Zechariah": "Zech",
    "Malachi": "Mal",
    "Psalms": "Ps",
    "Proverbs": "Prov",
    "Job": "Job",
    "Song of Songs": "Song",
    "Ruth": "Ruth",
    "Lamentations": "Lam",
    "Ecclesiastes": "Eccl",
    "Esther": "Esth",
    "Daniel": "Dan",
    "Ezra": "Ezra",
    "Nehemiah": "Neh",
    "1Chronicles": "1Chr",
    "2Chronicles": "2Chr",
}


@dataclass(frozen=True)
class VerseLink:
    label: str
    href: str
    title: str


def verse_links(book: str, chapter: int, verse: int) -> tuple[VerseLink, ...]:
    """Return the external links shown beside a case's verse reference."""
    if book not in TANACH_US_BOOK_CODES:
        raise ValueError(f"no tanach.us book code for {book!r}")
    osdf = tbn.ordered_short_dash_full_39(book)
    return (
        VerseLink(
            label="UXLC",
            href=(
                "https://tanach.us/Tanach.xml?"
                f"{TANACH_US_BOOK_CODES[book]}{chapter}:{verse}"
            ),
            title="This verse at tanach.us, the UXLC's home",
        ),
        VerseLink(
            label="MwD",
            href=(
                "https://bdenckla.github.io/MAM-basics/MAM-with-doc/"
                f"{quote(f'{osdf}.html')}#c{chapter}v{verse}"
            ),
            title="This verse in MAM-with-doc",
        ),
    )


def book_display_name(book: str) -> str:
    """The bk39 id spelled out for a reader: Levit and Deuter are truncations."""
    return _BOOK_DISPLAY_NAMES.get(book, book)


# bib_locales truncates two Torah book ids; a reader-facing page spells them out.
_BOOK_DISPLAY_NAMES = {
    tbn.BK_LEVIT: "Leviticus",
    tbn.BK_DEUTER: "Deuteronomy",
    tbn.BK_FST_SAM: "1 Samuel",
    tbn.BK_SND_SAM: "2 Samuel",
    tbn.BK_FST_KGS: "1 Kings",
    tbn.BK_SND_KGS: "2 Kings",
    tbn.BK_FST_CHR: "1 Chronicles",
    tbn.BK_SND_CHR: "2 Chronicles",
}
