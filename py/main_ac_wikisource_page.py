"""Build the Wikisource page indexing the Aleppo Codex, from J David Stark's index.

Reads the hand-made CSV in the sibling codex-index-aleppo's ``aleppo-wiki/`` and
writes three artifacts back beside it: the CSV's rows as JSON (``index-flat.json``),
those rows grouped by book (``index-grouped-by-book.json``), and the wikitext itself
(``index.wiki``).  All four paths come from ``ac_paths``.

WHY THE FOUR PATHS WERE DEAD FOR FIVE MONTHS, which is worth keeping in front of a
reader of this file.  They were the cwd-relative literals ``"aleppo/..."`` until
2026-08-22, naming the directory this tree had before ``9025037`` (2026-03-28)
renamed ``codex-index/aleppo`` to ``codex-index-aleppo/aleppo-wiki`` -- see
``provenance.md`` beside the data.  The rename did not repoint them, so from that day
this generator raised ``FileNotFoundError`` from every working directory and its
three outputs had no producer at all.  Phase 1 of
``doc/PLAN-evacuate-python-from-codex-index-trio.md`` repointed them first, before
any other path work in that repo, precisely so that the rest of the phase had an
oracle to prove itself against.

THE COUNTERPART PIPELINE IS A DIFFERENT TOOL, which is why the two do not share a
name here.  codex-index-leningrad's is ``main_lenin_wikisource_page.py``; it reads a
different input format and builds a different page, and the trio plan's Phase 0
classified the two as Family 2 and found them to be two tools rather than one with
drift.

This file was ``aleppo-wiki/main_make_wikisource_page.py`` in codex-index-aleppo
until Phase 3 of the same plan, 2026-08-22.
"""

from wlc_cmn.utf8_io import force_utf8_io

import ac_paths
from ac_wiki.group_by_book import group_by_book
from ac_wiki.read_csv_file import read_csv_file
from ac_wiki.write_wikitext_file import write_wikitext_file


def almost_main() -> None:
    """The body, callable in-process."""
    data_entries = read_csv_file(
        ac_paths.wiki_index_csv_path(), ac_paths.wiki_index_flat_path()
    )
    grouped = group_by_book(data_entries, ac_paths.wiki_index_grouped_path())
    write_wikitext_file(grouped, ac_paths.wiki_index_wikitext_path())


if __name__ == "__main__":
    force_utf8_io()
    almost_main()
