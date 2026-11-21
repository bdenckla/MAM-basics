"""Build links to the UXLC HTML verse view."""

import re


# A few older WLC and Job pages use full book names instead of the site codes.
_BOOK_CODES = {
    "1Samuel": "1Sam",
    "2Samuel": "2Sam",
    "Isaiah": "Isa",
    "Lamentations": "Lam",
}


def uxlc_verse_url(bcv: str) -> str:
    """Return the HTML view for one verse, e.g. Judg21:20-21:20."""
    match = re.fullmatch(r"([1-3]?[A-Za-z]+)([0-9]+:[0-9]+)", bcv)
    if match is None:
        raise ValueError(f"expected a UXLC book, chapter and verse: {bcv!r}")
    book, cv = match.groups()
    return f"https://tanach.us/Tanach.html?{_BOOK_CODES.get(book, book)}{cv}-{cv}"
