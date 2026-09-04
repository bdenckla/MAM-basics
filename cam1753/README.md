# Cambridge Ms. Add. 1753 image corpus

This tree holds data for locating Hebrew words on photographed pages of Cambridge
University Library MS Add. 1753. The current work concerns Job, but the procedures
support any biblical book. The programs that read and write this data live in
[`../py/`](../py/).

## Pipeline

1. [`../py/py_ac_loc/mam_xml_verses.py`](../py/py_ac_loc/mam_xml_verses.py) reads
   the shared [`../MAM-XML/`](../MAM-XML/) word-sequence snapshot.
2. [`../py/main_cam1753_gen_flat_stream.py`](../py/main_cam1753_gen_flat_stream.py)
   writes per-page word streams in `cam1753-line-breaks/`.
3. [`../py/main_cam1753_gen_line_break_editor.py`](../py/main_cam1753_gen_line_break_editor.py)
   generates the editor used to annotate line breaks.
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
- [`../MAM-XML/`](../MAM-XML/) is the pinned 24-file snapshot shared with the Aleppo
  lane; [`MAM-simple-provenance.md`](MAM-simple-provenance.md) identifies its source.

The image attribution and non-commercial terms are in
[`cam1753-spreads-provenance.md`](cam1753-spreads-provenance.md) and
[`../DATA-LICENSES.md`](../DATA-LICENSES.md).

## Conventions

- Page IDs are `{spread_number}{A|B}`: `0073A` is the left page of spread 73.
- Column 1 is the right column, read first in Hebrew; column 2 is the left column.
- Every column has 26 lines.

## Documentation

- [`doc/cam1753-line-break-task.md`](doc/cam1753-line-break-task.md) describes the
  manuscript, images, annotation data, and marking task.
- [`doc/reading-mam-simple.md`](doc/reading-mam-simple.md) describes the MAM-XML
  reader and snapshot.
- [`doc/mam-with-doc-urls.md`](doc/mam-with-doc-urls.md) describes MAM-with-doc URLs.
