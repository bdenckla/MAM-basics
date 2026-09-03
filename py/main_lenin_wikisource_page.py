"""Build the Wikisource page indexing the Leningrad Codex, from J David Stark's index.

Reads MAM-basics' canonical ``uxlc/data/lci_augrecs.json`` and writes three
artifacts under ``leningrad/lenin-wiki/``: the input rows reshaped
(``index-s0-annotated.json``), those rows collapsed per page and grouped by
book (``index-s2-grouped-by-book.json``), and the wikitext itself
(``index.wiki``). ``lenin_paths`` supplies all four paths.

``index.wiki`` IS A STARTING POINT FOR MANUAL WORK, NOT A PUBLISHABLE PAGE, and it was
never intended to stay in sync with what Wikisource ends up showing.  Ben, 2026-08-31,
on this file's output and its Aleppo counterpart's: they "were only ever intended to be
starting points for manual work on Wikisource."  The page the wiki actually carries at
``ויקיטקסט:מבוא למקרא על פי המסורה/מפתח לכתי"ל`` is that manual work, mirrored here as
``in/mam-ws-intro/index-leningrad.mediawiki``.  The two therefore diverge BY DESIGN --
94 of this generator's 1,135 lines reach the live page, 8% of them -- so a difference
between them is not drift, nothing needs re-syncing in either direction, and no test or
lint should compare them.  Unlike codex-index-aleppo, which keeps
``Wikisource-manual-initial.txt`` and ``Wikisource-manual-final.txt`` beside its
generated file, no snapshot of the Leningrad hand work is tracked; the mirrored page is the
only copy of it outside the wiki.

THE COUNTERPART PIPELINE IS A DIFFERENT TOOL, which is why the two do not share a
name here.  codex-index-aleppo's ``aleppo-wiki/main_make_wikisource_page.py`` reads
a different input format and builds a different page; the trio plan's Phase 0
classified the two as Family 2 and found them to be two tools rather than one with
drift.  This one has run correctly the whole time, which is why that phase could use
it as an oracle and could not use the other -- the aleppo half had been dead since
2026-03-28, a rename having left its four path literals naming a directory that no
longer existed.

This file was ``lenin-wiki/main_make_wikisource_page.py`` in codex-index-leningrad
until Phase 3 of ``doc/PLAN-evacuate-python-from-codex-index-trio.md``, 2026-08-22.
"""

from mb_cmn import file_io
from wlc_cmn.utf8_io import force_utf8_io

import lenin_paths
from lenin_wiki.read_json_file import read_json_file
from lenin_wiki.s1_collapse_rows import s1_collapse_rows
from lenin_wiki.s2_group_by_book import s2_group_by_book
from lenin_wiki.write_wikitext_file import write_wikitext_file


def almost_main() -> None:
    """The body, callable in-process."""
    annotated = read_json_file(lenin_paths.lci_augrecs_path())
    file_io.json_dump_to_file_path(annotated, lenin_paths.index_s0_annotated_path())
    #
    s1_collapsed = s1_collapse_rows(annotated["body"])
    #
    s2_grouped = s2_group_by_book(s1_collapsed)
    file_io.json_dump_to_file_path(s2_grouped, lenin_paths.index_s2_grouped_path())
    #
    write_wikitext_file(s2_grouped, lenin_paths.index_wikitext_path())


if __name__ == "__main__":
    force_utf8_io()
    almost_main()
