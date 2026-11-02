"""Resolve exact censused page records; never open a viewer or guess a page."""

from scan_pages import census
from scan_pages import text


class UncensusedError(ValueError):
    """The requested source range has not been completely censused."""


def resolve(index, bkid, chapter, verse, phrase=None, strand=None):
    """Return records for a verse, or the first atom of a unique phrase."""
    covered = sorted(
        {book for segment in index["segments"] for book in segment["bkids"]}
    )
    if strand is not None or bkid not in covered:
        available = ", ".join(covered) or "none"
        raise UncensusedError(
            f"{index['edition']}: requested range/strand is not censused; "
            f"censused ordinary-body books: {available}"
        )
    verses = text.book_atoms(bkid)
    recs = census.validate_book(index, bkid, verses)
    atoms = verses[chapter, verse]
    first, last = 1, len(atoms)
    if phrase is not None:
        first, _ = text.locate_phrase(verses, chapter, verse, phrase)
        last = first
    low, high = (chapter, verse, first), (chapter, verse, last)
    return [
        rec
        for rec in recs
        if (rec["startc"], rec["startv"], rec["startp"]) <= high
        and (rec["stopc"], rec["stopv"], rec["stopp"]) >= low
    ]
