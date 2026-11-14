"""Resolve exact censused page records; never open a viewer or guess a page."""

from scan_pages import census
from scan_pages import decalogue
from scan_pages import editions
from scan_pages import page_kinds as pk
from scan_pages import text
from scan_pages import tiqqun


class UncensusedError(ValueError):
    """The requested source range has not been completely censused."""


def resolve(index, bkid, chapter, verse, phrase=None, strand=None, *, rite=None):
    """Return page records or Tiqqun occurrences containing the requested atoms."""
    if rite is not None and strand is not None:
        raise ValueError("Choose a Tiqqun rite or a Decalogue strand")
    data = index.get("tiqqun") if index["edition"] == editions.SIMANIM_TIQQUN else None
    if data is not None:
        if strand == "e" and "elyon_body" not in data:
            raise UncensusedError(
                "Simanim Tiqqun: named elyon body lookup is unverified"
            )
        strand_by_suffix = {None: None, "t": pk.TAXTON, "e": pk.ELYON}
        if strand not in strand_by_suffix:
            raise ValueError(f"Unknown Decalogue strand: {strand}")
        return tiqqun.resolve(
            data,
            bkid,
            chapter,
            verse,
            phrase,
            strand=strand_by_suffix[strand],
            rite=rite,
        )
    if rite is not None:
        raise UncensusedError(f"{index['edition']}: Tiqqun rite lookup is unavailable")
    if strand is not None and "decalogue-ranges" in index:
        named = {"t": pk.TAXTON, "e": pk.ELYON}
        if strand not in named:
            raise ValueError(f"Unknown Decalogue strand: {strand}")
        reading = named[strand]
        if reading in index["decalogue-ranges"].get(bkid, {}):
            return decalogue.resolve(index, bkid, chapter, verse, phrase, reading)
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
        start, _ = text.locate_phrase_span(verses, chapter, verse, phrase)
        first = start[2]
        last = first
    low, high = (chapter, verse, first), (chapter, verse, last)
    return [
        rec
        for rec in recs
        if (rec["startc"], rec["startv"], rec["startp"]) <= high
        and (rec["stopc"], rec["stopv"], rec["stopp"]) >= low
    ]


def resolve_printed_forms(index, bkid, chapter, verse, phrase):
    """Return every recorded exact printed form at a verse, including counterparts."""
    atoms = text.letters_atoms(phrase)
    if not atoms:
        raise ValueError("Printed-form lookup requires a nonempty phrase")
    matches = [
        form
        for form in index.get("printed-forms", ())
        if form["bkid"] == bkid
        and tuple(form["first"][:2]) == (chapter, verse)
        and text.letters_atoms(" ".join(form["lines"])) == atoms
    ]
    if not matches:
        raise UncensusedError(
            f"{index['edition']}: no recorded printed form at {bkid} {chapter}:{verse}"
        )
    return matches
