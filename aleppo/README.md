# Aleppo Codex page-location data in MAM-basics

This product directory holds data and generated artifacts for locating Hebrew words on photographed pages of the Aleppo Codex. The current corpus covers Job, while the pipeline accepts other biblical books when the index data is available.

MAM-basics contains the programs that read and write this product directory. The `main_ac_*` entry points in [`../py/`](../py/) read [`../MAM-simple/xml-vtrad-mam/`](../MAM-simple/xml-vtrad-mam/) as their MAM word-sequence input, write flat streams and annotation editors, and locate annotated words in the page images.

## Data

- `aleppo-pages/` holds the photographed pages; [`aleppo-pages-provenance.md`](aleppo-pages-provenance.md) records their source.
- `ds-flat-stream/` holds generated per-page word streams.
- `line-breaks/` holds line-break data annotated by Ben Denckla.
- `column-coordinates/` holds column geometry annotated by Ben Denckla.
- `aleppo-wiki/` holds J. David Stark's index material and two snapshots of the Wikisource page built by hand from it.
- `doc/` holds procedures for the Aleppo page-location work.

The published scholarly pages are under [`../gh-pages/aleppo/`](../gh-pages/aleppo/) and are served at [bdenckla.github.io/MAM-basics/aleppo/](https://bdenckla.github.io/MAM-basics/aleppo/).

## Consumer guide

`aleppo-wiki/index-flat-corrected.json` is the hand-corrected entry index, and
`index-flat-annotated.json` is its generated form with `de_start_whole` and
`de_end_whole` added. Both have exactly this top-level shape:

```json
{
  "header": {
    "description": "...",
    "consumer_notice": {"summary": "...", "critical_rules": ["..."], "documentation": "https://..."},
    "rows_sans_url": ["..."],
    "rows_with_gap": ["..."],
    "books": ["..."]
  },
  "body": ["...page records only..."]
}
```

The files are locator indexes, not transcriptions of the Aleppo Codex and not Bible
editions. A body record's `de_text_range` can begin or end mid-verse, and `de_gap`
records missing manuscript coverage rather than permission to fill the gap. The range
is locator evidence; it makes no general promise that any text field reproduces the
manuscript's pointing or mark order.

The subordinate `line-breaks/` files align a MAM word stream with manually annotated
page lines, and `column-coordinates/` records image geometry. The line-break stream is
not a diplomatic transcription, and the geometry does not establish textual content.
Neither subordinate format is part of the entry-index schema above.

## Conventions

- A page ID is `{leaf_number}{r|v}`: for example, `270r` is leaf 270 recto.
- Column 1 is the right column, read first in Hebrew; column 2 is the left column.
- Every column has 28 lines.
