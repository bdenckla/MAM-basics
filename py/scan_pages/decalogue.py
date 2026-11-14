"""Resolve named Decalogue ranges in ordinary catalogs."""

from accgram import mam_simple_verse
from mb_cmn import mam_simple_json
from mb_cmn import paths
from mb_misc import osis_book_abbrevs
from scan_pages import census
from scan_pages import page_kinds as pk
from scan_pages import text


def _uses_body(extent):
    return "appendix" not in extent or extent.get("body", False)


def strand_atoms(book, verses, first_cv, last_cv, strand):
    """Require the named strand's atoms to match the canonical coordinates."""
    key = {pk.TAXTON: "vels_cant_alef", pk.ELYON: "vels_cant_bet"}[strand]
    source = mam_simple_verse.mam_simple_json_path(
        paths.mam_simple_dir().with_name("json-vtrad-mam"), book
    )
    prefix = osis_book_abbrevs.BOOK_ABBREVS[book]
    expected = {cv: atoms for cv, atoms in verses.items() if first_cv <= cv <= last_cv}
    strand_atoms = {}
    for node in mam_simple_json.verses(mam_simple_json.read_book_group(source)):
        osis, c, v = node["osisID"].split(".")
        cv = int(c), int(v)
        if osis == prefix and cv in expected:
            normalized = mam_simple_verse._normalize_mam_simple_verse(
                node, include_strands=True
            )
            words = mam_simple_verse.string_vels(normalized[key], node["osisID"])
            strand_atoms[cv] = text.letters_atoms(" ".join(words))
    if not expected or strand_atoms != expected:
        raise ValueError(f"Decalogue coordinates disagree with {key} in {book}")
    return strand_atoms


def validate(index, books=None):
    """Verify named ranges, appendix roles and the canonical projections."""
    pages = {page["file"]: page for page in index["pages"]}
    for book, readings in index["decalogue-ranges"].items():
        if book not in ("Exodus", "Deuter") or not readings.keys() <= set(
            pk.ALL_STRANDS
        ):
            raise ValueError(f"Invalid named Decalogue book or strand: {book}")
        verses = text.book_atoms(book, books)
        positions = set(text.positions(verses))
        for strand, extent in readings.items():
            start, stop = (tuple(extent[key]) for key in ("start", "stop"))
            if start not in positions or stop not in positions or stop < start:
                raise ValueError(f"Invalid named Decalogue range: {book} {strand}")
            fields = extent.keys() - {"start", "stop"}
            if fields not in (set(), {"appendix"}, {"appendix", "body"}) or (
                "body" in fields and extent["body"] is not True
            ):
                raise ValueError(f"Invalid named Decalogue fields: {book} {strand}")
            if _uses_body(extent):
                census.validate_book(index, book, verses)
            if "appendix" in fields:
                appendix = extent["appendix"]
                page = pages[appendix]
                if (
                    page["kind"] != pk.DECALOGUE
                    or book not in page["bkids"]
                    or strand not in page["strands"]
                ):
                    raise ValueError(f"Invalid named Decalogue appendix: {appendix}")
            strand_atoms(book, verses, start[:2], stop[:2], strand)


def resolve(index, book, chapter, verse, phrase, strand):
    """Intersect the verified named range with the selected page records."""
    extent = index["decalogue-ranges"].get(book, {}).get(strand)
    if extent is None:
        return []
    start, stop = (tuple(extent[key]) for key in ("start", "stop"))
    cv = chapter, verse
    if not start[:2] <= cv <= stop[:2]:
        return []
    verses = text.book_atoms(book)
    named = strand_atoms(book, verses, start[:2], stop[:2], strand)
    first, last = (*cv, 1), (*cv, len(named[cv]))
    if phrase is not None:
        first, _ = text.locate_phrase_span(named, *cv, phrase)
        last = first
    use_body = _uses_body(extent)
    if use_body:
        rows = census.validate_book(index, book, verses)
    else:
        rows = [{"page": extent["appendix"], "bkid": book}]
    hits = []
    for row in rows:
        low, high = start, stop
        if use_body:
            low = max(start, tuple(row["start" + key] for key in "cvp"))
            high = min(stop, tuple(row["stop" + key] for key in "cvp"))
        if low <= high and low <= last and first <= high:
            hits.append(
                {
                    "page": row["page"],
                    "bkid": book,
                    "strand": strand,
                    **{
                        "start" + key: value
                        for key, value in zip("cvp", low, strict=True)
                    },
                    **{
                        "stop" + key: value
                        for key, value in zip("cvp", high, strict=True)
                    },
                }
            )
    return hits
