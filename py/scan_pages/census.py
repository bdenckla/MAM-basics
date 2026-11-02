"""Adopt a whole book's observed page edges, deriving atom numbers from cues."""

from scan_pages import index_io
from scan_pages import text


def body_pages(index, bkid):
    return [
        page["file"]
        for page in index["pages"]
        if page["kind"] == "body" and bkid in page.get("bkids", ())
    ]


def validate_book(index, bkid, verses):
    """Check every page, both cues, and an exact gap-free atom partition."""
    names = body_pages(index, bkid)
    recs = [rec for rec in index["recs"] if rec["bkid"] == bkid]
    if [rec["page"] for rec in recs] != names:
        raise ValueError(
            f"{index['edition']} {bkid}: census must cover every body page in order"
        )
    all_positions = text.positions(verses)
    ordinal = {position: i for i, position in enumerate(all_positions)}
    expected = 0
    for rec in recs:
        start = (rec["startc"], rec["startv"], rec["startp"])
        stop = (rec["stopc"], rec["stopv"], rec["stopp"])
        if start not in ordinal or stop not in ordinal:
            raise ValueError(f"{rec['page']}: invalid atom position")
        if ordinal[start] != expected or ordinal[stop] < ordinal[start]:
            raise ValueError(f"{rec['page']}: gap, overlap or reversed page interval")
        for end, atom_index in (("start", 0), ("stop", 1)):
            span = text.locate_phrase_span(
                verses,
                rec[f"{end}c"],
                rec[f"{end}v"],
                rec[f"{end}_phrase"],
                anchor=end,
            )
            if span[atom_index] != (start if end == "start" else stop):
                raise ValueError(f"{rec['page']}: {end} cue disagrees with stored atom")
            if not start <= span[0] <= span[1] <= stop:
                raise ValueError(f"{rec['page']}: {end} cue extends outside its page")
        if not isinstance(rec["printed_page"], int) or rec["printed_page"] < 1:
            raise ValueError(f"{rec['page']}: missing observed printed page number")
        expected = ordinal[stop] + 1
    if expected != len(all_positions):
        raise ValueError(
            f"{index['edition']} {bkid}: census does not reach the book's last atom"
        )
    return recs


def adopt(index, bkid, edges):
    """Return a checked index; mutate/write nothing if any observation fails."""
    verses = text.book_atoms(bkid)
    records = []
    for edge in edges:
        rec = {
            "page": edge["page"],
            "bkid": bkid,
            "printed_page": edge["printed_page"],
            "note": edge["note"],
        }
        for end, atom_index in (("start", 0), ("stop", 1)):
            c, v, phrase = edge[end]
            rec.update(
                {
                    f"{end}c": c,
                    f"{end}v": v,
                    f"{end}p": text.locate_phrase_span(
                        verses, c, v, phrase, anchor=end
                    )[atom_index][2],
                    f"{end}_phrase": phrase,
                }
            )
        records.append(rec)
    revised = dict(index)
    revised["rec-fields"] = dict(index_io.REC_FIELDS)
    revised["recs"] = [rec for rec in index["recs"] if rec["bkid"] != bkid] + records
    revised["recs"].sort(key=lambda rec: (rec["page"], rec["bkid"]))
    validate_book(revised, bkid, verses)
    segments = index["segments"]
    if segments and (len(segments) != 1 or segments[0]["id"] != "body"):
        raise ValueError("First-phase census supports ordinary body coverage only")
    covered = sorted(set(segments[0]["bkids"] if segments else ()) | {bkid})
    pages = sorted({name for book in covered for name in body_pages(index, book)})
    body_order = [page["file"] for page in index["pages"] if page["kind"] == "body"]
    start, stop = body_order.index(pages[0]), body_order.index(pages[-1])
    if body_order[start : stop + 1] != pages:
        raise ValueError(
            "Extend the current contiguous body census before adopting a distant book"
        )
    revised["segments"] = [{"id": "body", "bkids": covered, "pages": pages}]
    for book in covered:
        validate_book(revised, book, verses if book == bkid else text.book_atoms(book))
    return revised


def run(edition_id, bkid, edges):
    revised = adopt(index_io.read_index(edition_id), bkid, edges)
    index_io.write_index(edition_id, revised)
    return len(edges)
