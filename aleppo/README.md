# Aleppo Codex page-location data in MAM-basics

This product directory holds data and generated artifacts for locating Hebrew words on photographed pages of the Aleppo Codex. The current corpus covers Job, while the pipeline accepts other biblical books when the index data is available.

MAM-basics owns the programs that read and write this product directory. The `main_ac_*` entry points in [`../py/`](../py/) read [`../MAM-simple/xml-vtrad-mam/`](../MAM-simple/xml-vtrad-mam/) as their MAM word-sequence input, write flat streams and annotation editors, and locate annotated words in the page images.

## Data

- `aleppo-pages/` holds the photographed pages; [`aleppo-pages-provenance.md`](aleppo-pages-provenance.md) records their source.
- `ds-flat-stream/` holds generated per-page word streams.
- `line-breaks/` holds hand-annotated line-break data.
- `column-coordinates/` holds hand-annotated column geometry.
- `aleppo-wiki/` holds J. David Stark's index material and the Wikisource page derived from it.
- `doc/` holds procedures for the Aleppo page-location work.

The published scholarly pages are under [`../gh-pages/aleppo/`](../gh-pages/aleppo/) and are served at [bdenckla.github.io/MAM-basics/aleppo/](https://bdenckla.github.io/MAM-basics/aleppo/).

## Conventions

- A page ID is `{leaf_number}{r|v}`: for example, `270r` is leaf 270 recto.
- Column 1 is the right column, read first in Hebrew; column 2 is the left column.
- Every column has 28 lines.
