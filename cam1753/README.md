# Cambridge Ms. Add. 1753 image corpus

This tree holds data for locating Hebrew words on photographed pages of Cambridge
University Library MS Add. 1753. The current work concerns Job, but the procedures
support any biblical book. The programs that read and write this data live in
[`../py/`](../py/).

## Pipeline

1. [`../py/py_ac_loc/mam_xml_verses.py`](../py/py_ac_loc/mam_xml_verses.py) reads
   [`../MAM-simple/xml-vtrad-mam/`](../MAM-simple/xml-vtrad-mam/), the MAM word-sequence
   ground truth.
2. [`../py/main_cam1753_gen_flat_stream.py`](../py/main_cam1753_gen_flat_stream.py)
   writes per-page word streams in `cam1753-line-breaks/`.
3. Line breaks were annotated by hand in an editor that
   `py/main_cam1753_gen_line_break_editor.py` generated. It was deleted on 2026-09-26;
   `git show 4ac4f16a:py/py_cam1753_loc/gen_line_break_editor.py` recovers it.
4. [`../py/main_cam1753_gen_col_quad_editor.py`](../py/main_cam1753_gen_col_quad_editor.py)
   generates the editor used to annotate column quadrilaterals.
5. [`../py/main_cam1753_find_word_in_images.py`](../py/main_cam1753_find_word_in_images.py)
   finds annotated words in the page images.

## Data

- `cam1753-spreads/` holds the fourteen tracked two-page source scans.
- `cam1753-pages/` is the gitignored, derived 28-JPEG page tree. Run
  [`../py/main_cam1753_split_spreads.py`](../py/main_cam1753_split_spreads.py) before
  a crop or editor task needs it.
- `cam1753-line-breaks/` and `cam1753-col-quads/` hold the hand-annotated data.
- `cam1753-spread-splits-doc/` records each split so it can be audited without
  rerunning the gutter finder.
- [`../MAM-simple/xml-vtrad-mam/`](../MAM-simple/xml-vtrad-mam/) is the MAM word-sequence
  ground truth shared with the Aleppo lane.

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

## Documentation

- [`doc/cam1753-line-break-task.md`](doc/cam1753-line-break-task.md) describes the
  manuscript, images, annotation data, and marking task.
- [`doc/reading-mam-simple.md`](doc/reading-mam-simple.md) describes the MAM-simple XML
  reader and product path.
- [`doc/mam-with-doc-urls.md`](doc/mam-with-doc-urls.md) describes MAM-with-doc URLs.
