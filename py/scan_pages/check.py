"""Lint the tracked indexes: mechanical checks over the data, not example tests.

The data model of doc/scan-pages.md makes a page error inexpressible; these checks are
what catch wrong *data* inside that model.  Two of them do real work already at
Phase 0, before a single page has been censused:

  * every stored classification is re-derived from its file name by the parser and
    compared -- a differential check of the whole 5,720-page listing against an
    independent derivation of the same fact;
  * every record's position is looked up in MAM-parsed, so a book, chapter or verse
    that MAM does not have fails here rather than at bring-up time.

MAM-PARSED ABSENT IS A FAILURE, NEVER A SKIP.  No CI runs this, so a check that
quietly passes when it cannot reach its input reports green having verified nothing.
``paths.mam_parsed_path`` fails instead, naming both environment overrides -- which is
the answer a worktree needs, since its ``repo_root().parent`` is inside ``.claude``.

Two checks the Design section lists are not here yet, because both need machinery
Phase 1 builds and neither has any data to run on: re-locating a stored phrase in
MAM's text, and the atoms-per-page band.  They arrive with the census that produces
phrases and stop halves.
"""

from mb_cmn import bib_locales as tbn
from mb_cmn import paths
from mb_cmn import read_books_from_mam_parsed_plus as plus
from scan_pages import classify
from scan_pages import editions
from scan_pages import index_io
from scan_pages import page_kinds as pk


class CheckError(Exception):
    """The tracked index data failed a lint."""


def _check_pages(edition_id, pages, problems):
    """Structure of the page listing, and its classification re-derived."""
    names = [page["file"] for page in pages]
    if names != sorted(names):
        problems.append(f"{edition_id}: pages are not in sorted order")
    if len(set(names)) != len(names):
        problems.append(f"{edition_id}: duplicate file names in pages")
    # Re-derived from the whole listing, not name by name: the divider-leaf pass needs
    # its neighbours, so a per-name re-derivation would disagree with the stored data
    # on every divider and the disagreement would be the checker's fault, not the
    # data's.
    rederived_all = classify.classify_listing(edition_id, names)
    for page, rederived in zip(pages, rederived_all):
        if page["kind"] not in pk.ALL_KINDS:
            problems.append(
                f"{edition_id}: {page['file']}: unknown kind {page['kind']}"
            )
        if rederived is None:
            problems.append(
                f"{edition_id}: {page['file']}: stored, but the parser no longer"
                " classifies it"
            )
        elif rederived != page:
            problems.append(
                f"{edition_id}: {page['file']}: stored classification {page} differs"
                f" from the parser's {rederived}"
            )
    return len(pages)


def _check_recs(edition_id, pages, recs, books, problems):
    """Every record sits on a page that exists, is recordable, and holds its book."""
    by_name = {page["file"]: page for page in pages}
    seen = set()
    for rec in recs:
        page = by_name.get(rec["page"])
        if page is None:
            problems.append(f"{edition_id}: rec on {rec['page']}, which is not a page")
            continue
        if page["kind"] not in pk.RECORDABLE_KINDS:
            problems.append(
                f"{edition_id}: rec on {rec['page']}, whose kind is {page['kind']}"
            )
        if rec["bkid"] not in page.get("bkids", ()):
            problems.append(
                f"{edition_id}: rec on {rec['page']} is for {rec['bkid']}, which that"
                f" page does not carry"
            )
        key = (rec["page"], rec["bkid"], rec["startc"], rec["startv"], rec["startp"])
        if key in seen:
            problems.append(f"{edition_id}: duplicate rec {key}")
        seen.add(key)
        _check_positions(edition_id, rec, books, problems)
    _check_contiguity(edition_id, recs, problems)
    return len(recs)


def _check_positions(edition_id, rec, books, problems):
    """Both ends of a record must name a verse MAM actually has."""
    for end in ("start", "stop"):
        chnu, vrnu = rec[f"{end}c"], rec[f"{end}v"]
        if chnu is None and vrnu is None:
            continue
        if chnu is None or vrnu is None:
            problems.append(f"{edition_id}: {rec['page']}: half-given {end} position")
            continue
        bcvt = tbn.mk_bcvtmam(rec["bkid"], chnu, vrnu)
        if bcvt not in books[rec["bkid"]]["verses_plus"]:
            problems.append(
                f"{edition_id}: {rec['page']}: {rec['bkid']} {chnu}:{vrnu} is not a"
                f" verse MAM has"
            )
        if rec[f"{end}p"] is None or rec[f"{end}p"] < 1:
            problems.append(f"{edition_id}: {rec['page']}: bad {end} atom number")


def _check_contiguity(edition_id, recs, problems):
    """Consecutive complete records of one book must advance and must not overlap.

    Only records with both halves filled take part, so this is quiet at Phase 0 and
    becomes the census's main guardrail the moment stop halves exist.
    """
    complete = [rec for rec in recs if rec["stopc"] is not None]
    by_book = {}
    for rec in complete:
        by_book.setdefault(rec["bkid"], []).append(rec)
    for bkid, book_recs in sorted(by_book.items()):
        for earlier, later in zip(book_recs, book_recs[1:]):
            stop = (earlier["stopc"], earlier["stopv"], earlier["stopp"])
            start = (later["startc"], later["startv"], later["startp"])
            if start <= stop:
                problems.append(
                    f"{edition_id}: {bkid}: {later['page']} starts at {start}, which"
                    f" does not follow {earlier['page']}'s stop at {stop}"
                )
    return len(complete)


def _check_segments(edition_id, pages, segments, problems):
    """Segments, once present, must name real pages and must not overlap.

    A STRAND-TAGGED SEGMENT IS ALLOWED TO SHARE PAGES, and that is not a loophole:
    jc1 prints the תחתון and the עליון side by side on one Decalogue page, so the two
    strands' segments genuinely occupy the same sheet.  Only untagged segments are
    required to be disjoint.
    """
    if not isinstance(segments, list):
        problems.append(f"{edition_id}: segments is not a list")
        return 0
    names = {page["file"] for page in pages}
    claimed = {}
    for segment in segments:
        for name in segment.get("pages", ()):
            if name not in names:
                problems.append(f"{edition_id}: segment names unknown page {name}")
            if segment.get("strand") is None:
                if name in claimed:
                    problems.append(
                        f"{edition_id}: {name} is in two untagged segments"
                        f" ({claimed[name]}, {segment.get('id')})"
                    )
                claimed[name] = segment.get("id")
    return len(segments)


def check_all():
    """Lint every tracked index. Return a counts dict; raise CheckError on any problem."""
    books = plus.read_parsed_plus_bk39s(mam_parsed_path=paths.mam_parsed_path())
    problems = []
    counts = {"pages": 0, "recs": 0, "segments": 0, "editions": 0}
    for edition_id in editions.ALL_EDITION_IDS:
        index = index_io.read_index(edition_id)
        if index["edition"] != edition_id:
            problems.append(f"{edition_id}: index says it is {index['edition']}")
        pages, recs = index["pages"], index["recs"]
        counts["pages"] += _check_pages(edition_id, pages, problems)
        counts["recs"] += _check_recs(edition_id, pages, recs, books, problems)
        counts["segments"] += _check_segments(
            edition_id, pages, index["segments"], problems
        )
        counts["editions"] += 1
    if problems:
        raise CheckError(
            f"{len(problems)} problems in the scan-pages index:\n  "
            + "\n  ".join(problems[:60])
        )
    return counts
