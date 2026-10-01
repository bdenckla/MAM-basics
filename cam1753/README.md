# Cambridge Ms. Add. 1753 page-location data

This tree holds data for locating Hebrew words on photographed pages of Cambridge
University Library MS Add. 1753. Its line-break data begins at Psalms 149:7 and continues
through Job into Proverbs, ending with the first three atoms of Proverbs 1:31, and its page
index also covers Lamentations.

No program maintains this data. The page images and every program that worked on them
were retired on 2026-09-26 by
[`../doc/PLAN-retire-codex-index-image-work.md`](../doc/PLAN-retire-codex-index-image-work.md),
so the data below is kept as it stands, and nothing regenerates it.

## Data

- `cam1753-page-index.json` is the low-resolution entry index that the consumer guide
  below describes.
- `cam1753-line-breaks/` and `cam1753-col-quads/` hold the hand-annotated data.
  [`doc/cam1753-line-break-task.md`](doc/cam1753-line-break-task.md) describes both
  formats and what they cover.
- `cam1753-spread-splits-doc/` records where each two-page spread was split into pages,
  so the split can be audited without the images.
- `cam1753-gutter-profiles.png` is the retired gutter finder's chart, kept as a record.
  Matplotlib version changes make it non-reproducible.
- [`check_line_breaks.html`](check_line_breaks.html) is the frozen report of the last
  line-break check; nothing regenerates it.
- `test-data-from-book-of-job.json` holds the 160 Book-of-Job cases that the retired
  word-finding check read. Nothing reads it now.
- [`things-noticed-in-cam1753.md`](things-noticed-in-cam1753.md) records observations
  made while reading the pages.
- [`cam1753-spreads-provenance.md`](cam1753-spreads-provenance.md) records where the
  retired spreads came from and the last commit that holds them.
- [`../MAM-simple/xml-vtrad-mam/`](../MAM-simple/xml-vtrad-mam/) is the MAM word-sequence
  ground truth that the line-break streams follow.

The image attribution and non-commercial terms are in
[`cam1753-spreads-provenance.md`](cam1753-spreads-provenance.md) and
[`../DATA-LICENSES.md`](../DATA-LICENSES.md).

## Consumer guide

`cam1753-page-index.json` is the low-resolution entry index. Its canonical top level
has exactly `header` and `body`:

```json
{
  "header": {
    "description": "...",
    "consumer_notice": {"summary": "...", "critical_rules": ["..."], "documentation": "https://..."}
  },
  "body": ["...page records only..."]
}
```

The header description preserves the index's scope and provenance warning. A body
record identifies a page with `de_leaf`, `de_archive_spread`, and `de_spread_side`, and
can add a column, notes, or text cues with their references. These records are locators,
not transcriptions of Cambridge MS Add. 1753 and not a Bible edition. A text cue can be
letters-only MAM evidence or older pointed locator text, as its accompanying description
states; it must not be cited as a manuscript transcription or treated as a blanket
mark-order guarantee. Mid-verse boundaries and incomplete coverage are meaningful.

The subordinate `cam1753-line-breaks/` files align a MAM word stream with manually
annotated page lines, while `cam1753-col-quads/` records image geometry. Line-break data
is not a diplomatic transcription, and geometry does not establish textual content.
Neither subordinate format is part of the entry-index schema above.

## Conventions

- Page IDs are `{spread_number}{A|B}`: `0073A` is the left page of spread 73.
- Column 1 is the right column, read first in Hebrew; column 2 is the left column.
- Every column has 26 lines.
- Preserve the stored Hebrew data exactly. Do not normalize it. Repository mark-order
  and Latin NFC checks include this tree; the image terms are recorded in
  [cam1753-spreads-provenance.md](cam1753-spreads-provenance.md) and
  [../DATA-LICENSES.md](../DATA-LICENSES.md).

## Documentation

- [`doc/cam1753-line-break-task.md`](doc/cam1753-line-break-task.md) describes the
  manuscript, the retired images, the annotation data, and how it was made.
- [`doc/reading-mam-simple.md`](doc/reading-mam-simple.md) describes the MAM-simple XML
  reader and product path.
- [`doc/mam-with-doc-urls.md`](doc/mam-with-doc-urls.md) describes MAM-with-doc URLs.
