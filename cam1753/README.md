# codex-index-cam1753

A digital scholarship tool for locating Hebrew words on photographed pages of
Cambridge University Library MS Add. 1753 (Ketuvim) — μY. The current focus is the
Book of Job, though the infrastructure supports arbitrary biblical books.

**This repo holds data, and no code.** Its Python moved to the sibling repo
MAM-basics on 2026-08-22, under Phases 3 and 4 of that repo's
`doc/PLAN-evacuate-python-from-codex-index-trio.md`; the data stayed here and goes on
being hosted here. Nothing about that is provisional. See [CLAUDE.md](CLAUDE.md) for
which program in MAM-basics writes what here.

A sibling repo, [`codex-index-aleppo`](https://github.com/bdenckla/codex-index-aleppo),
covers the same biblical text in the Aleppo Codex (μA). Both repos use quadrilateral
column geometry.

## Pipeline

Every step runs from `C:/Users/BenDe/GitRepos/MAM-basics` now. The modules kept their
names but dropped a `cam1753` infix that the package name `py_cam1753_loc` already
carries, and each is reached through a `main_cam1753_` wrapper at MAM-basics' `py/`
top level rather than being run directly.

1. **XML parsing** — `../MAM-basics/py/py_ac_loc/mam_xml_verses.py` extracts word lists from `MAM-XML/` (see [Data](#data))
2. **Flat stream** — `../MAM-basics/py/main_cam1753_gen_flat_stream.py` combines explicit verse-range arguments with those word lists into per-page word streams; data in `cam1753-line-breaks/`
3. **Line-break annotation** — human-in-the-loop via `../MAM-basics/py/main_cam1753_gen_line_break_editor.py`; data in `cam1753-line-breaks/`
4. **Column coordinates** — `../MAM-basics/py/main_cam1753_gen_col_quad_editor.py`; data in `cam1753-col-quads/`
5. **Word lookup** — `../MAM-basics/py/main_cam1753_find_word_in_images.py` ties it all together

**Step 1 is codex-index-aleppo's module, and that is not a slip.** This repo's
`py_mam_xml/mam_xml_verses.py` and codex-index-aleppo's `py_ac_loc/mam_xml_verses.py`
were the same reader with 43 lines of drift, and they were reconciled onto one copy
when the code moved. [CLAUDE.md](CLAUDE.md) says what the one behavioural difference
between them was.

## Data

- **`MAM-XML/`** — a flat copy of the **`xml-vtrad-mam`** output of the sibling
  [`MAM-simple`](https://github.com/bdenckla/MAM-simple) repo: the mam vtrad, not `xml-vtrad-bhs`
  or `xml-vtrad-sef`. The directory name is that repo's *former* name, which it was renamed away
  from in its own `0c2ce6b`; `py_cam1753_loc/gen_flat_stream.py` still spells it `MAM_XML_DIR`.
  [`MAM-simple-provenance.md`](MAM-simple-provenance.md) records which commit the copy came
  from, and records the source path as `MAM-simple/out/xml-vtrad-mam` — also pre-rename, since
  MAM-simple's `16b63e3` moved the `xml-vtrad-*` directories to that repo's root and turned
  `out/` into `misc/`.
- **`cam1753-pages/`**, **`cam1753-spreads/`** — page images and the two-page spreads they were
  split from; provenance in `cam1753-spreads-provenance.md`.
- **`cam1753-line-breaks/`**, **`cam1753-col-quads/`** — the generated flat streams with their
  human-annotated line breaks, and the column quadrilaterals.
- **`cam1753-spread-splits-doc/`** — one record per spread of where the gutter was found and what
  each half became, so a split can be audited without re-running the gutter finder.

## Conventions

- **Page IDs:** `{spread_number}{A|B}` — e.g. `0073A` (spread 73, left page), `0073B` (spread 73, right page)
- **Column numbering:** col 1 = right column (read first in RTL), col 2 = left column
- **Lines per column:** 26 — `LINES_PER_COL` in `../MAM-basics/py/py_cam1753_word_image/page.py`

## Docs

- [`doc/cam1753-line-break-task.md`](doc/cam1753-line-break-task.md) — the manuscript, its page images and their provenance, the column-quad data, and the marking task itself
- [`doc/reading-mam-simple.md`](doc/reading-mam-simple.md) — the vendored `MAM-XML/` snapshot and the reader over it; points at MAM-simple for the format itself
- [`doc/mam-with-doc-urls.md`](doc/mam-with-doc-urls.md) — how to build a URL into the MAM-with-doc viewer (book codes, verse fragments)
