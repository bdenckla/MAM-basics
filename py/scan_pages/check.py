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

Complete censused books additionally require both source phrases to relocate to
their recorded atoms, complete page coverage and an exact adjacent-atom partition.
The initial body segment names the completed books explicitly; unread seeds do not
count as coverage. The CLI can also report unusually short or long ordinary pages.
"""

from statistics import median

from mb_cmn import bib_locales as tbn
from mb_cmn import paths
from mb_cmn import read_books_from_mam_parsed_plus as plus
from scan_pages import classify
from scan_pages import editions
from scan_pages import index_io
from scan_pages import page_kinds as pk
from scan_pages import census
from scan_pages import decalogue
from scan_pages import text
from scan_pages import tiqqun


class CheckError(Exception):
    """The tracked index data failed a lint."""


def _check_pages(edition_id, pages, problems, occurrence_data=None):
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
    if occurrence_data is not None:
        rederived_all = tiqqun.classify_pages(rederived_all, occurrence_data)
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


def _check_printed_forms(index, problems):
    pages = {page["file"]: page for page in index["pages"]}
    records = {(rec["bkid"], rec["page"]): rec for rec in index["recs"]}
    seen = set()
    for form in index.get("printed-forms", ()):
        bkid, page, owner = form["bkid"], form["page"], form["canonical_page"]
        first, last = tuple(form["first"]), tuple(form["last"])
        lines = form["lines"]
        message = f"{index['edition']} {bkid}: invalid printed form on {page}"
        target = records.get((bkid, owner))
        physical = pages.get(page)
        if (
            target is None
            or physical is None
            or physical["kind"] != pk.BODY
            or bkid not in physical.get("bkids", ())
            or len(first) != 3
            or len(last) != 3
            or first[:2] != last[:2]
            or any(type(pos) is not int or pos < 1 for pos in (*first, *last))
            or first > last
            or not isinstance(lines, list)
            or not lines
            or any(
                not isinstance(line, str) or not text.letters_atoms(line)
                for line in lines
            )
        ):
            problems.append(message)
            continue
        key = (bkid, page, first, last, tuple(lines))
        start = (target["startc"], target["startv"], target["startp"])
        stop = (target["stopc"], target["stopv"], target["stopp"])
        if key in seen or stop[0] is None or not start <= first <= last <= stop:
            problems.append(message)
        if page != owner:
            adjacent = records.get((bkid, page))
            body = census.body_pages(index, bkid)
            if adjacent is None or abs(body.index(page) - body.index(owner)) != 1:
                problems.append(message)
        seen.add(key)


def _density_warnings(edition_id, book, records, pages_by_name, verses):
    """Compare single-book interior pages with their book's typical page."""
    interior = [
        rec for rec in records[1:-1] if pages_by_name[rec["page"]]["bkids"] == [book]
    ]
    if len(interior) < 8:
        return []
    ordinal = {pos: i for i, pos in enumerate(text.positions(verses))}
    sizes = {}
    for rec in interior:
        start = (rec["startc"], rec["startv"], rec["startp"])
        stop = (rec["stopc"], rec["stopv"], rec["stopp"])
        sizes[rec["page"]] = ordinal[stop] - ordinal[start] + 1
    typical = median(sizes.values())
    return [
        f"{edition_id} {book} {name}: {size} atoms (book median {typical:g})"
        for name, size in sizes.items()
        if size < 0.5 * typical or size > 1.5 * typical
    ]


def check_all(*, density_warnings=None):
    """Lint every tracked index. Return a counts dict; raise CheckError on any problem."""
    books = plus.read_parsed_plus_bk39s(mam_parsed_path=paths.mam_parsed_path())
    problems = []
    counts = {"pages": 0, "recs": 0, "segments": 0, "editions": 0}
    for edition_id in editions.ALL_EDITION_IDS:
        index = index_io.read_index(edition_id)
        if index["edition"] != edition_id:
            problems.append(f"{edition_id}: index says it is {index['edition']}")
        pages, recs = index["pages"], index["recs"]
        if "tiqqun" in index:
            if edition_id != editions.SIMANIM_TIQQUN:
                problems.append(f"{edition_id}: unexpected Tiqqun occurrence data")
                continue
            try:
                counts["pages"] += _check_pages(
                    edition_id, pages, problems, index["tiqqun"]
                )
                occurrences, groups = tiqqun.validate(index, books)
            except (ValueError, KeyError, TypeError) as error:
                problems.append(f"{edition_id}: {error}")
            else:
                counts["recs"] += occurrences
                counts["segments"] += groups
            counts["editions"] += 1
            continue
        counts["pages"] += _check_pages(edition_id, pages, problems)
        counts["recs"] += _check_recs(edition_id, pages, recs, books, problems)
        counts["segments"] += _check_segments(
            edition_id, pages, index["segments"], problems
        )
        pages_by_name = {page["file"]: page for page in pages}
        declared = {book for segment in index["segments"] for book in segment["bkids"]}
        completed = {rec["bkid"] for rec in recs if rec["stopc"] is not None}
        if declared != completed:
            problems.append(
                f"{edition_id}: completed books differ from declared coverage"
            )
        for segment in index["segments"]:
            claimed = {
                name
                for book in segment["bkids"]
                for name in census.body_pages(index, book)
            }
            body_order = census.body_order(index)
            expected_pages = [name for name in body_order if name in claimed]
            if segment["pages"] != expected_pages:
                problems.append(
                    f"{edition_id}: coverage pages do not match the declared books"
                )
            if not expected_pages:
                problems.append(f"{edition_id}: empty coverage segment")
            else:
                first = body_order.index(expected_pages[0])
                last = body_order.index(expected_pages[-1])
                if body_order[first : last + 1] != expected_pages:
                    problems.append(f"{edition_id}: noncontiguous body segment")
        for book in sorted(declared):
            try:
                verses = text.book_atoms(book, books)
                records = census.validate_book(index, book, verses)
            except (ValueError, KeyError, TypeError) as error:
                problems.append(f"{edition_id} {book}: {error}")
            else:
                if density_warnings is not None:
                    density_warnings.extend(
                        _density_warnings(
                            edition_id, book, records, pages_by_name, verses
                        )
                    )
        _check_printed_forms(index, problems)
        if "decalogue-ranges" in index:
            try:
                decalogue.validate(index, books)
            except (ValueError, KeyError, TypeError) as error:
                problems.append(f"{edition_id}: {error}")
        counts["editions"] += 1
    if problems:
        raise CheckError(
            f"{len(problems)} problems in the scan-pages index:\n  "
            + "\n  ".join(problems[:60])
        )
    return counts
