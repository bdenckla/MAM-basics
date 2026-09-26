# Aleppo Codex page-location data in MAM-basics

This directory holds data for locating Hebrew words on photographed pages of the Aleppo Codex. It is intentionally uneven: much of the codex is indexed at page level, while Job and a run of Deuteronomy pages also have line and column data.

One program maintains this directory: [`../py/main_ac_gen_index_flat_annotated.py`](../py/main_ac_gen_index_flat_annotated.py) writes `index-flat-annotated.json` from the hand-corrected index, and the mega runs it. The page scans and the programs that worked on them were retired on 2026-09-26 by [`../doc/PLAN-retire-codex-index-image-work.md`](../doc/PLAN-retire-codex-index-image-work.md), so the line, column and flat-stream data below are kept as they stand, and nothing regenerates them.

## Data

- `line-breaks/` holds line-break data annotated by Ben Denckla.
- `column-coordinates/` holds column geometry annotated by Ben Denckla.
- `ds-flat-stream/` holds per-page word streams without line markers, as the retired generator wrote them.
- [`check_line_breaks.html`](check_line_breaks.html) is the frozen report of the last line-break check; nothing regenerates it.
- [`aleppo-pages-provenance.md`](aleppo-pages-provenance.md) records where the retired page scans came from and the last commit that holds them.
- `aleppo-wiki/` holds J. David Stark's index material and two snapshots of the Wikisource page built by hand from it.
- `doc/` holds notes on the retained line-break data, on reading MAM-simple, on MAM-with-doc URLs, and on OCR of Aleppo Codex images with Kraken.

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
