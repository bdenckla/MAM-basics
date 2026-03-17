"""
Book URL info and verse-reference formatting for MPP diff reports.

Exports:
    mam_with_doc_url — build a MAM-with-doc GitHub Pages URL
    wikisource_url   — build a Hebrew Wikisource te'amim URL
    ref_str          — short verse reference like "Gen 1:1"
"""

from urllib.parse import quote

from pycmn import hebrew_verse_numerals as hvn

# Keyed by the display names used in diff dicts (from mpp_extract._FILE_STEM_TO_BOOK39S).
# Each value is (OSDF key for MAM-with-doc URLs, Hebrew name for Wikisource URLs).
_BOOK_URL_INFO = {
    "Genesis": ("A1-Genesis", "\u05d1\u05e8\u05d0\u05e9\u05d9\u05ea"),
    "Exodus": ("A2-Exodus", "\u05e9\u05de\u05d5\u05ea"),
    "Leviticus": ("A3-Levit", "\u05d5\u05d9\u05e7\u05e8\u05d0"),
    "Numbers": ("A4-Numbers", "\u05d1\u05de\u05d3\u05d1\u05e8"),
    "Deuteronomy": ("A5-Deuter", "\u05d3\u05d1\u05e8\u05d9\u05dd"),
    "Joshua": ("B1-Joshua", "\u05d9\u05d4\u05d5\u05e9\u05e2"),
    "Judges": ("B2-Judges", "\u05e9\u05d5\u05e4\u05d8\u05d9\u05dd"),
    "1 Samuel": ("BA-1Samuel", "\u05e9\u05de\u05d5\u05d0\u05dc \u05d0"),
    "2 Samuel": ("BB-2Samuel", "\u05e9\u05de\u05d5\u05d0\u05dc \u05d1"),
    "1 Kings": ("BC-1Kings", "\u05de\u05dc\u05db\u05d9\u05dd \u05d0"),
    "2 Kings": ("BD-2Kings", "\u05de\u05dc\u05db\u05d9\u05dd \u05d1"),
    "Isaiah": ("C1-Isaiah", "\u05d9\u05e9\u05e2\u05d9\u05d4\u05d5"),
    "Jeremiah": ("C2-Jeremiah", "\u05d9\u05e8\u05de\u05d9\u05d4\u05d5"),
    "Ezekiel": ("C3-Ezekiel", "\u05d9\u05d7\u05d6\u05e7\u05d0\u05dc"),
    "Hosea": ("CA-Hosea", "\u05d4\u05d5\u05e9\u05e2"),
    "Joel": ("CB-Joel", "\u05d9\u05d5\u05d0\u05dc"),
    "Amos": ("CC-Amos", "\u05e2\u05de\u05d5\u05e1"),
    "Obadiah": ("CD-Obadiah", "\u05e2\u05d5\u05d1\u05d3\u05d9\u05d4"),
    "Jonah": ("CE-Jonah", "\u05d9\u05d5\u05e0\u05d4"),
    "Micah": ("CF-Micah", "\u05de\u05d9\u05db\u05d4"),
    "Nahum": ("CG-Nahum", "\u05e0\u05d7\u05d5\u05dd"),
    "Habakkuk": ("CH-Habakkuk", "\u05d7\u05d1\u05e7\u05d5\u05e7"),
    "Zephaniah": ("CI-Tsefaniah", "\u05e6\u05e4\u05e0\u05d9\u05d4"),
    "Haggai": ("CJ-Haggai", "\u05d7\u05d2\u05d9"),
    "Zechariah": ("CK-Zechariah", "\u05d6\u05db\u05e8\u05d9\u05d4"),
    "Malachi": ("CL-Malachi", "\u05de\u05dc\u05d0\u05db\u05d9"),
    "Psalms": ("D1-Psalms", "\u05ea\u05d4\u05dc\u05d9\u05dd"),
    "Proverbs": ("D2-Proverbs", "\u05de\u05e9\u05dc\u05d9"),
    "Job": ("D3-Job", "\u05d0\u05d9\u05d5\u05d1"),
    "Song of Songs": (
        "E1-Song of Songs",
        "\u05e9\u05d9\u05e8 \u05d4\u05e9\u05d9\u05e8\u05d9\u05dd",
    ),
    "Ruth": ("E2-Ruth", "\u05e8\u05d5\u05ea"),
    "Lamentations": ("E3-Lamentations", "\u05d0\u05d9\u05db\u05d4"),
    "Ecclesiastes": ("E4-Ecclesiastes", "\u05e7\u05d4\u05dc\u05ea"),
    "Esther": ("E5-Esther", "\u05d0\u05e1\u05ea\u05e8"),
    "Daniel": ("F1-Daniel", "\u05d3\u05e0\u05d9\u05d0\u05dc"),
    "Ezra": ("FA-Ezra", "\u05e2\u05d6\u05e8\u05d0"),
    "Nehemiah": ("FB-Nehemiah", "\u05e0\u05d7\u05de\u05d9\u05d4"),
    "1 Chronicles": (
        "FC-1Chronicles",
        "\u05d3\u05d1\u05e8\u05d9 \u05d4\u05d9\u05de\u05d9\u05dd \u05d0",
    ),
    "2 Chronicles": (
        "FD-2Chronicles",
        "\u05d3\u05d1\u05e8\u05d9 \u05d4\u05d9\u05de\u05d9\u05dd \u05d1",
    ),
}

_SHORT_BOOK_NAMES = {
    "Deuteronomy": "Deut",
    "Leviticus": "Lev",
    "1 Samuel": "1Sam",
    "2 Samuel": "2Sam",
    "1 Kings": "1Kgs",
    "2 Kings": "2Kgs",
    "1 Chronicles": "1Chr",
    "2 Chronicles": "2Chr",
    "Song of Songs": "Song",
    "Lamentations": "Lam",
    "Ecclesiastes": "Eccl",
    "Zephaniah": "Zeph",
    "Zechariah": "Zech",
    "Habakkuk": "Hab",
    "Nehemiah": "Neh",
}


def mam_with_doc_url(book, chapter, verse):
    """Build a MAM-with-doc GitHub Pages URL for a verse."""
    osdf = _BOOK_URL_INFO[book][0]
    return f"https://bdenckla.github.io/MAM-with-doc/{osdf}.html#c{chapter}v{verse}"


def wikisource_url(book, chapter):
    """Build a Hebrew Wikisource te'amim URL for a chapter."""
    he_chnu = hvn.INT_TO_STR_DIC[chapter]
    name_he = _BOOK_URL_INFO[book][1]
    page_title = quote(f"{name_he}_{he_chnu}/\u05d8\u05e2\u05de\u05d9\u05dd")
    return f"https://he.wikisource.org/wiki/{page_title}"


def ref_str(diff):
    """Format a verse reference like 'Gen 1:1'."""
    book = diff["book"]
    bk = _SHORT_BOOK_NAMES.get(book, book)
    return f"{bk} {diff['chapter']}:{diff['verse']}"
