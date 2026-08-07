"""Walk the five scan folders, classify every file, and write the tracked indexes.

No image is read here and none is copied: the index records file names and the facts
derivable from them, which are uncopyrightable and belong in a public repo.

THIS STEP REFUSES RATHER THAN SHRINKS.  An unrecognized file name, a file OneDrive has
left as a cloud-only placeholder, an unexpected extension -- each raises, naming every
offender.  The alternative is an index that is silently short, and a page missing from
the index is a page no lookup can ever return, with nothing downstream to notice.
"""

import os
import stat

from scan_pages import classify
from scan_pages import editions
from scan_pages import index_io
from scan_pages import page_kinds as pk

# OneDrive marks a file whose bytes are not on this machine.  Reading one would either
# stall on a network fetch or fail outright, and indexing it unread would record a page
# nobody can open.
_CLOUD_ONLY_ATTRS = (
    getattr(stat, "FILE_ATTRIBUTE_OFFLINE", 0x1000)
    | getattr(stat, "FILE_ATTRIBUTE_RECALL_ON_OPEN", 0x00040000)
    | getattr(stat, "FILE_ATTRIBUTE_RECALL_ON_DATA_ACCESS", 0x00400000)
)


class SurveyError(Exception):
    """A scan folder held something the survey will not silently drop."""


def _listing(edition_id):
    """Return an edition's sorted file names, refusing anything unreadable."""
    folder = editions.edition_dir(edition_id)
    if not folder.is_dir():
        raise SurveyError(f"{edition_id}: no scan folder at {folder}")
    names, not_jpg, cloud_only = [], [], []
    for entry in sorted(folder.iterdir(), key=lambda path: path.name):
        if entry.is_dir():
            not_jpg.append(entry.name + "/")
            continue
        if entry.suffix.lower() != ".jpg":
            not_jpg.append(entry.name)
            continue
        if _is_cloud_only(entry):
            cloud_only.append(entry.name)
        names.append(entry.name)
    if not_jpg:
        raise SurveyError(
            f"{edition_id}: {len(not_jpg)} non-JPG entries in {folder}: "
            + ", ".join(not_jpg[:20])
        )
    if cloud_only:
        raise SurveyError(
            f"{edition_id}: {len(cloud_only)} files are OneDrive cloud-only"
            f" placeholders and were not indexed. Make the folder available offline,"
            f" then re-run. First few: " + ", ".join(cloud_only[:20])
        )
    return names


def _is_cloud_only(path):
    attributes = getattr(os.stat(path), "st_file_attributes", 0)
    return bool(attributes & _CLOUD_ONLY_ATTRS)


def _classified(edition_id, names):
    """Classify every name, or raise naming all the names that did not classify."""
    pages, unclassified = [], []
    for name, page in zip(names, classify.classify_listing(edition_id, names)):
        if page is None:
            unclassified.append(name)
        else:
            pages.append(page)
    if unclassified:
        raise SurveyError(
            f"{edition_id}: {len(unclassified)} file names did not classify. Extend"
            f" py/scan_pages/classify.py -- reading the page image if the name does not"
            f" say what it is. Names: " + ", ".join(unclassified[:40])
        )
    return pages


def _seeded_recs(pages):
    """Return one start-half record per book, on the first page carrying that book.

    Free from the file names alone: a book's text begins at its chapter 1, verse 1,
    atom 1, and that is on the first page the book appears on.  Everything else --
    both phrases and the whole stop half -- waits for the census, which reads pages.
    """
    recs, seen = [], set()
    for page in pages:
        if page["kind"] not in pk.RECORDABLE_KINDS:
            continue
        for bkid in page.get("bkids", ()):
            if bkid in seen or page["kind"] != pk.BODY:
                continue
            seen.add(bkid)
            recs.append(
                {
                    "page": page["file"],
                    "bkid": bkid,
                    "startc": 1,
                    "startv": 1,
                    "startp": 1,
                    "stopc": None,
                    "stopv": None,
                    "stopp": None,
                    "start_phrase": None,
                    "stop_phrase": None,
                    "note": "seeded by survey: a book starts at 1:1 atom 1",
                }
            )
    return recs


def _anomalies(edition_id, pages):
    """Return the notes worth a human's attention, without failing the run."""
    out = []
    body_books = {}
    for index, page in enumerate(pages):
        if page["kind"] != pk.BODY:
            continue
        for bkid in page["bkids"]:
            body_books.setdefault(bkid, []).append(index)
    for bkid, indices in sorted(body_books.items()):
        span = pages[indices[0] : indices[-1] + 1]
        strayed = [
            page["file"]
            for page in span
            if page["kind"] == pk.BODY and bkid not in page["bkids"]
        ]
        if strayed:
            out.append(
                f"{bkid}: body pages of other books lie inside its run"
                f" ({len(strayed)}), first {strayed[0]}"
            )
        if len(indices) == 1:
            out.append(f"{bkid}: only one body page, {pages[indices[0]]['file']}")
    if edition_id == editions.BHL:
        out.extend(_bhl_bare_number_anomalies(pages))
    unadjudicated = classify.unadjudicated_book_openings(edition_id, pages)
    if unadjudicated:
        out.append(
            f"{len(unadjudicated)} books show no divider leaf, so their opening page is"
            f" recorded as text unconfirmed; the census reads these first: "
            + ", ".join(unadjudicated)
        )
    return out


def _bhl_bare_number_anomalies(pages):
    """bhl's bare-numbered pages are appendix continuations, so they must follow one."""
    first_appendix = next(
        (i for i, page in enumerate(pages) if "Appendix" in page["file"]), None
    )
    if first_appendix is None:
        return ["bhl: no Appendix page found, so bare-numbered pages are unexplained"]
    early = [
        page["file"]
        for i, page in enumerate(pages)
        if i < first_appendix and page["file"][: -len(".jpg")].isdigit()
    ]
    if early:
        return [
            "bhl: bare-numbered pages before the first Appendix page: "
            + ", ".join(early)
        ]
    return []


def survey_edition(edition_id):
    """Classify one edition's folder and write its index. Return a report dict."""
    names = _listing(edition_id)
    pages = _classified(edition_id, names)
    recs = _seeded_recs(pages)
    # Segments -- the runs of pages over which the text advances contiguously -- are
    # filled by the phases that read pages.  An empty list is this edition's honest
    # state now, not a missing input; check() verifies whatever is here.
    index_io.write_index(edition_id, index_io.make_index(edition_id, pages, recs, []))
    kinds = {}
    for page in pages:
        kinds[page["kind"]] = kinds.get(page["kind"], 0) + 1
    body_pages = {}
    for page in pages:
        if page["kind"] == pk.BODY:
            for bkid in page["bkids"]:
                body_pages[bkid] = body_pages.get(bkid, 0) + 1
    return {
        "edition": edition_id,
        "files": len(names),
        "kinds": kinds,
        "body_pages_per_book": body_pages,
        "recs": len(recs),
        "rec_pages": len({rec["page"] for rec in recs}),
        "anomalies": _anomalies(edition_id, pages),
    }


def survey_all():
    """Survey every edition. Return one report per edition, in the canonical order."""
    return [survey_edition(edition_id) for edition_id in editions.ALL_EDITION_IDS]
