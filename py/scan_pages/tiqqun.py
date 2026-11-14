"""Classify, validate and query printed occurrences in the Simanim Tiqqun."""

from collections import defaultdict

from scan_pages import decalogue
from scan_pages import page_kinds as pk
from scan_pages import text

_FULL_BOOK_SECTIONS = {"ordinary_torah", "megillot"}
_SECTIONS = _FULL_BOOK_SECTIONS | {"haftarah", "appendix"}
_NONTEXT = {pk.BLANK, pk.SECTION_TITLE, pk.TOC, pk.APPARATUS}
_RITE_SECTION = "haftarah"


def _claim(roles, page, kind, *, book=None, strand=None):
    entry = roles.setdefault(
        page, {"kind": kind, "books": set(), "strands": set(), "claimed": False}
    )
    if entry["kind"] != kind or (kind in _NONTEXT and entry["claimed"]):
        raise ValueError(f"{page}: conflicting Tiqqun scan roles")
    entry["claimed"] = True
    if book is not None:
        entry["books"].add(book)
    if strand is not None:
        entry["strands"].add(strand)


def classify_pages(pages, data):
    """Assign the observed roles to the filenames in the pointed section."""
    roles = {}
    for entry in data["occurrences"]:
        appendix = entry["section"] == "appendix"
        for leaf in entry["pages"]:
            _claim(
                roles,
                leaf["page"],
                pk.DECALOGUE if appendix else pk.BODY,
                book=entry["bkid"],
                strand=entry.get("strand"),
            )
    for kind, names in data["nontext"].items():
        if kind not in _NONTEXT:
            raise ValueError(f"Unsupported Tiqqun nontext role: {kind}")
        for name in names:
            _claim(roles, name, kind)
    expected = {page["file"] for page in pages if page["kind"] == pk.BODY_UNASSIGNED}
    missing, unassigned = roles.keys() - expected, expected - roles.keys()
    if missing or unassigned:
        raise ValueError(
            f"Tiqqun pointed inventory differs. Missing scans: {sorted(missing)}. "
            f"Unassigned scans: {sorted(unassigned)}."
        )
    return [
        (
            pk.page(
                page["file"],
                role["kind"],
                bkids=sorted(role["books"]),
                strands=sorted(role["strands"]),
            )
            if (role := roles.get(page["file"])) is not None
            else page
        )
        for page in pages
    ]


def _position(value):
    if (
        not isinstance(value, list)
        or len(value) != 3
        or any(type(number) is not int or number < 1 for number in value)
    ):
        raise ValueError(f"Invalid Tiqqun atom position: {value!r}")
    return tuple(value)


def _identity(entry):
    return entry["section"], entry["bkid"], entry["occurrence"]


def validate(index, books=None):
    """Validate the inclusive ranges and every within-occurrence page join."""
    if index["recs"] or index["segments"] or index.get("printed-forms"):
        raise ValueError("Tiqqun occurrence data cannot share an ordinary-body census")
    data = index["tiqqun"]
    required = {"occurrences", "rites", "nontext"}
    if (
        not required <= data.keys() <= required | {"elyon_body"}
        or not data["occurrences"]
    ):
        raise ValueError("Tiqqun catalog needs occurrence, rite and nontext data")
    page_order = {row["file"]: i for i, row in enumerate(index["pages"])}
    projections, entries = {}, {}
    for entry in data["occurrences"]:
        section, book, identity = key = _identity(entry)
        if (
            section not in _SECTIONS
            or not isinstance(identity, str)
            or not identity.strip()
        ):
            raise ValueError(f"Invalid Tiqqun occurrence: {key}")
        expected = {"section", "bkid", "occurrence", "pages"}
        if section == "appendix":
            expected.add("strand")
            if entry.get("strand") != pk.TAXTON:
                raise ValueError(f"Unverified Tiqqun appendix strand: {key}")
        if set(entry) != expected or key in entries or not entry["pages"]:
            raise ValueError(f"Invalid or duplicate Tiqqun occurrence: {key}")
        entries[key] = entry
        if book not in projections:
            verses, protected = text._book_projection(book, books)
            positions = text.positions(verses)
            ordinals = {pos: i for i, pos in enumerate(positions)}
            boundaries = {
                boundary
                for first, last in protected
                for boundary in range(ordinals[first] + 1, ordinals[last] + 1)
            }
            projections[book] = verses, ordinals, boundaries

        verses, ordinals, boundaries = projections[book]
        previous = None
        last_page = -1
        for leaf in entry["pages"]:
            if not {"page", "start", "stop"} <= leaf.keys() <= {
                "page",
                "start",
                "stop",
                "rotation_clockwise",
            } or leaf.get("rotation_clockwise", 0) not in (0, 90):
                raise ValueError(f"Invalid Tiqqun page record: {key} {leaf}")
            start, stop = _position(leaf["start"]), _position(leaf["stop"])
            lo, hi = ordinals[start], ordinals[stop]
            order = page_order[leaf["page"]]
            if (
                lo > hi
                or lo in boundaries
                or hi + 1 in boundaries
                or order <= last_page
            ):
                raise ValueError(f"Invalid Tiqqun interval or page order: {key} {leaf}")
            if previous is None:
                if section in _FULL_BOOK_SECTIONS and lo != 0:
                    raise ValueError(f"Missing opening atoms: {key}")
            elif previous + 1 != lo:
                raise ValueError(f"Gap or overlap in Tiqqun occurrence: {key} {leaf}")
            previous = hi
            last_page = order
        if section in _FULL_BOOK_SECTIONS and previous != len(ordinals) - 1:
            raise ValueError(f"Missing terminal atoms: {key}")
        if section == "appendix":
            decalogue.strand_atoms(
                book,
                verses,
                tuple(entry["pages"][0]["start"][:2]),
                tuple(entry["pages"][-1]["stop"][:2]),
                pk.TAXTON,
            )

    for book, extent in data.get("elyon_body", {}).items():
        if book not in ("Exodus", "Deuter") or set(extent) != {"start", "stop"}:
            raise ValueError(f"Invalid Tiqqun elyon body range: {book}")
        start, stop = (_position(extent[end]) for end in ("start", "stop"))
        entry = entries["ordinary_torah", book, book]
        verses, ordinals, boundaries = projections[book]
        low, high = ordinals[start], ordinals[stop]
        if (
            not ordinals[tuple(entry["pages"][0]["start"])]
            <= low
            <= high
            <= ordinals[tuple(entry["pages"][-1]["stop"])]
            or low in boundaries
            or high + 1 in boundaries
        ):
            raise ValueError(f"Invalid Tiqqun elyon body boundaries: {book}")
        decalogue.strand_atoms(book, verses, start[:2], stop[:2], pk.ELYON)

    for name, rite in data["rites"].items():
        if set(rite) != {"bkid", "occurrence", "start", "stop", "description"}:
            raise ValueError(f"Invalid Tiqqun rite: {name}")
        if not isinstance(rite["description"], str) or not rite["description"].strip():
            raise ValueError(f"Tiqqun rite needs a description: {name}")
        key = _RITE_SECTION, rite["bkid"], rite["occurrence"]
        leaves = entries[key]["pages"]
        _, ordinals, boundaries = projections[rite["bkid"]]
        low, high = (ordinals[_position(rite[end])] for end in ("start", "stop"))
        if (
            not ordinals[tuple(leaves[0]["start"])]
            <= low
            <= high
            <= ordinals[tuple(leaves[-1]["stop"])]
        ):
            raise ValueError(f"Tiqqun rite leaves its occurrence: {name}")
        if low in boundaries or high + 1 in boundaries:
            raise ValueError(f"Tiqqun rite splits a mapped span: {name}")
    return sum(len(entry["pages"]) for entry in entries.values()), len(entries)


def _result(entry, leaf, first, last):
    row = {
        "page": leaf["page"],
        "bkid": entry["bkid"],
        "section": entry["section"],
        "occurrence": entry["occurrence"],
        "start": list(first),
        "stop": list(last),
        "rotation_clockwise": leaf.get("rotation_clockwise", 0),
    }
    if "strand" in entry:
        row["strand"] = entry["strand"]
    return row


def resolve(data, book, chapter, verse, phrase=None, *, strand=None, rite=None):
    """Return each matching printed occurrence, ordered by scan filename."""
    selection = None
    if rite is not None:
        selection = data["rites"].get(rite)
        if selection is None:
            raise ValueError(f"Unknown approved Tiqqun rite: {rite}")
        if selection["bkid"] != book:
            return []
    body_range = data.get("elyon_body", {}).get(book) if strand == pk.ELYON else None
    if strand == pk.ELYON and body_range is None:
        return []
    cv = chapter, verse
    candidates = []
    for entry in data["occurrences"]:
        if entry["bkid"] != book:
            continue
        if body_range is not None:
            if entry["section"] != "ordinary_torah":
                continue
            entry = {**entry, "strand": pk.ELYON}
        elif entry.get("strand") != strand:
            continue
        if selection is not None and (
            entry["section"] != _RITE_SECTION
            or entry["occurrence"] != selection["occurrence"]
        ):
            continue
        limit = body_range if body_range is not None else selection
        for leaf in entry["pages"]:
            first, last = tuple(leaf["start"]), tuple(leaf["stop"])
            if limit is not None:
                first = max(first, tuple(limit["start"]))
                last = min(last, tuple(limit["stop"]))
            if first <= last and first[:2] <= cv <= last[:2]:
                candidates.append((entry, leaf, first, last))
    if not candidates:
        return []
    verses = text.book_atoms(book)
    if strand == pk.TAXTON:
        first_cv = min(
            tuple(entry["pages"][0]["start"][:2]) for entry, *_ in candidates
        )
        last_cv = max(tuple(entry["pages"][-1]["stop"][:2]) for entry, *_ in candidates)
        verses = decalogue.strand_atoms(book, verses, first_cv, last_cv, strand)
    elif body_range is not None:
        first_cv = tuple(body_range["start"][:2])
        last_cv = tuple(body_range["stop"][:2])
        verses = decalogue.strand_atoms(book, verses, first_cv, last_cv, strand)
    first, last = 1, len(verses[cv])
    if phrase is not None:
        start, _ = text.locate_phrase_span(verses, chapter, verse, phrase)
        first = last = start[2]
    low, high = (*cv, first), (*cv, last)
    return sorted(
        (
            _result(entry, leaf, first, last)
            for entry, leaf, first, last in candidates
            if first <= high and low <= last
        ),
        key=lambda row: row["page"],
    )
