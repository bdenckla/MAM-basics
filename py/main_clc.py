"""Exports main: build the CLC walking skeleton for one pilot book, or all of them.

Usage (run from the repo root, like the other py/main_*.py drivers):

    python py/main_clc.py                      # default: all pilot pages (_ALL_JOBS)
    python py/main_clc.py all                   # same, explicit
    python py/main_clc.py [BookId] [chapter]     # just one page

Pass any bk39 id (e.g. "Psalms", "Job", "Genesis") to retarget. Pass an
optional 1-based chapter number to limit output to that chapter (e.g.
``python py/main_clc.py Exodus 20`` for the Decalogue) — handy for focusing on a
dual-cant chapter without the rest of the book.

Writes (``<label>`` is ``<book>`` for a whole book, ``<book>-<chapter>`` if limited):
    gh-pages/clc/<label>.html             the 3-column always-link page
    gh-pages/clc/<label>-notes.json       the CLC notes as plain data (feeds §7.9 later)
    gh-pages/clc/<label>-long-notes.html  this job's long notes (§7.3), only if it has any
"""

import sys

import mb_cmn.file_io as my_open
import mb_cmn.bib_locales as tbn
import clc.clc_collect as clc_collect
import clc.clc_long_note as clc_long_note
import clc.clc_render as clc_render
import uxlc_paths

# The pilot pages currently checked into gh-pages/clc/: three whole pilot books
# (Genesis is a single poetic book carrying both ``m`` and ``d`` under-bar notes, so
# both seed paths render — build-order step 5; Proverbs and 2Samuel are the other two
# pilots) plus the two Decalogue dual-cant demo chapters.
_ALL_JOBS = [
    (tbn.BK_GENESIS, None),
    (tbn.BK_PROV, None),
    (tbn.BK_SND_SAM, None),
    (tbn.BK_DEUTER, {5}),
    (tbn.BK_EXODUS, {20}),
]


def _build_one(book_id, chapters):
    assert book_id in tbn.ALL_BK39_IDS, f"unknown book id: {book_id!r}"
    book, notes = clc_collect.collect_for_book(book_id, chapters=chapters)
    html_path = clc_render.write_book(book_id, book, notes, chapters=chapters)
    label = clc_render.out_label(book_id, chapters)
    disp = clc_render.disp_label(book_id, chapters)
    notes_path = uxlc_paths.clc_pages_dir() / f"{label}-notes.json"
    my_open.json_dump_to_file_path([note.as_dict() for note in notes], notes_path)
    print(f"CLC skeleton: {len(notes)} notes for {label}")
    print(f"  wrote {html_path}")
    print(f"  wrote {notes_path}")
    long_notes = clc_render.build_long_notes(book_id, book, notes, chapters=chapters)
    if long_notes:
        long_notes_path = clc_long_note.write_page(
            label, disp, long_notes, main_page_href=f"{label}.html"
        )
        print(f"  wrote {long_notes_path} ({len(long_notes)} long note(s))")


def main():
    """Build the CLC skeleton page(s) + notes JSON, then each job's own long-notes
    page (design doc §7.3) for whatever long notes it opted into."""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    if len(sys.argv) <= 1 or sys.argv[1] == "all":
        for book_id, chapters in _ALL_JOBS:
            _build_one(book_id, chapters)
    else:
        book_id = sys.argv[1]
        chapters = {int(sys.argv[2])} if len(sys.argv) > 2 else None
        _build_one(book_id, chapters)


if __name__ == "__main__":
    main()
