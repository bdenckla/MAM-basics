# Reading MAM-simple

The guide to the MAM-simple format lives in the MAM-simple repo, and is canonical there:

- [doc/reading-mam-simple.md](https://github.com/bdenckla/MAM-simple/blob/main/doc/reading-mam-simple.md) — file layout, and reading MAM-simple from Python
- [doc/reading-mam-simple-xml.md](https://github.com/bdenckla/MAM-simple/blob/main/doc/reading-mam-simple-xml.md) — the XML hierarchy, element types, and verse attributes
- [doc/reading-mam-simple-json.md](https://github.com/bdenckla/MAM-simple/blob/main/doc/reading-mam-simple-json.md) — the JSON format

This file used to be a fuller copy of that guide. The copy went stale — it still had the
XML under `out/xml-vtrad-mam`, a directory MAM-simple moved to the repo root — so on
2026-08-03 its content was merged into the canonical guide and this pointer left behind.
What remains below is what is specific to this repo.

## Book-of-Job's former snapshot

The Book-of-Job source repository held `py_ac_loc/MAM-XML/`, a vendored snapshot
of MAM-simple's `xml-vtrad-mam`, until 2026-09-03. The 76-file tree was deliberately
not moved to MAM-basics: no code read it, and it duplicated the codex-index-aleppo
snapshot. The Book-of-Job repository history preserves the snapshot and its provenance.

**The code that reads XML of this shape is MAM-basics', and since 2026-08-22 it is one module
rather than two.** codex-index-aleppo and codex-index-cam1753 initially held a `MAM-XML/` snapshot
of their own, and each had its own reader for the snapshot — `py/py_ac_loc/mam_xml_verses.py` in the first and
`py_mam_xml/mam_xml_verses.py` in the second. Both repos' Python moved to MAM-basics that day
under `../MAM-basics/doc/PLAN-evacuate-python-from-codex-index-trio.md`, whose Phase 3 found the
two readers to be one tool with 43 lines of drift and merged them: they are
`../MAM-basics/py/py_ac_loc/mam_xml_verses.py`, single. Neither codex-index repo holds any code
now; each keeps its data and goes on hosting it. Book-of-Job no longer holds a
second snapshot. Since 2026-09-06 both live reader routes use
`MAM-basics/MAM-simple/xml-vtrad-mam/`.
