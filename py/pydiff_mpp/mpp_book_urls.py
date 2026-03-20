"""
Book URL info and verse-reference formatting for MPP diff reports.

Exports:
    mam_with_doc_url — build a MAM-with-doc GitHub Pages URL
    wikisource_url   — build a Hebrew Wikisource te'amim URL
    ref_str          — short verse reference like "Gen 1:1"
"""

from urllib.parse import quote

from pycmn import hebrew_verse_numerals as hvn

# Keyed by the display names used in diff dicts (from mpp_extract._CANONICAL_STEM_TO_BOOK39S).
# Each value is (OSDF key for MAM-with-doc URLs, Hebrew name for Wikisource URLs).
_BOOK_URL_INFO = {
    "Genesis": ("A1-Genesis", "בראשית"),
    "Exodus": ("A2-Exodus", "שמות"),
    "Leviticus": ("A3-Levit", "ויקרא"),
    "Numbers": ("A4-Numbers", "במדבר"),
    "Deuteronomy": ("A5-Deuter", "דברים"),
    "Joshua": ("B1-Joshua", "יהושע"),
    "Judges": ("B2-Judges", "שופטים"),
    "1 Samuel": ("BA-1Samuel", "שמואל א"),
    "2 Samuel": ("BB-2Samuel", "שמואל ב"),
    "1 Kings": ("BC-1Kings", "מלכים א"),
    "2 Kings": ("BD-2Kings", "מלכים ב"),
    "Isaiah": ("C1-Isaiah", "ישעיהו"),
    "Jeremiah": ("C2-Jeremiah", "ירמיהו"),
    "Ezekiel": ("C3-Ezekiel", "יחזקאל"),
    "Hosea": ("CA-Hosea", "הושע"),
    "Joel": ("CB-Joel", "יואל"),
    "Amos": ("CC-Amos", "עמוס"),
    "Obadiah": ("CD-Obadiah", "עובדיה"),
    "Jonah": ("CE-Jonah", "יונה"),
    "Micah": ("CF-Micah", "מיכה"),
    "Nahum": ("CG-Nahum", "נחום"),
    "Habakkuk": ("CH-Habakkuk", "חבקוק"),
    "Zephaniah": ("CI-Tsefaniah", "צפניה"),
    "Haggai": ("CJ-Haggai", "חגי"),
    "Zechariah": ("CK-Zechariah", "זכריה"),
    "Malachi": ("CL-Malachi", "מלאכי"),
    "Psalms": ("D1-Psalms", "תהלים"),
    "Proverbs": ("D2-Proverbs", "משלי"),
    "Job": ("D3-Job", "איוב"),
    "Song of Songs": (
        "E1-Song of Songs",
        "שיר השירים",
    ),
    "Ruth": ("E2-Ruth", "רות"),
    "Lamentations": ("E3-Lamentations", "איכה"),
    "Ecclesiastes": ("E4-Ecclesiastes", "קהלת"),
    "Esther": ("E5-Esther", "אסתר"),
    "Daniel": ("F1-Daniel", "דניאל"),
    "Ezra": ("FA-Ezra", "עזרא"),
    "Nehemiah": ("FB-Nehemiah", "נחמיה"),
    "1 Chronicles": (
        "FC-1Chronicles",
        "דברי הימים א",
    ),
    "2 Chronicles": (
        "FD-2Chronicles",
        "דברי הימים ב",
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
    page_title = quote(f"{name_he}_{he_chnu}/טעמים")
    return f"https://he.wikisource.org/wiki/{page_title}"


def ref_str(diff):
    """Format a verse reference like 'Gen 1:1'."""
    book = diff["book"]
    bk = _SHORT_BOOK_NAMES.get(book, book)
    return f"{bk} {diff['chapter']}:{diff['verse']}"
