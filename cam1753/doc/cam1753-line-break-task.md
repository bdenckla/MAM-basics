# cam1753 Line-Break Data

This note describes the retained line-break and column data for Cambridge University
Library MS Add. 1753: what it covers, what its files hold, and how it was made. The
marking is finished. The programs and page images it used were retired on 2026-09-26 by
[`../../doc/PLAN-retire-codex-index-image-work.md`](../../doc/PLAN-retire-codex-index-image-work.md),
so nothing regenerates this data. Until then this file was the marking procedure;
`git show f4d81285:cam1753/doc/cam1753-line-break-task.md` recovers that version, and
`git show f4d81285:<path>` recovers each retired program.

## Manuscript

Cambridge University Library, MS Add. 1753 (Ketuvim). Images downloaded from archive.org (item `ketuvim-cambridge-ms-add-1753-images`, zip `Ketuvim_Cambridge_MS_Add_1753_jp2.zip`, scale=2, server `ia800901.us.archive.org`).

## Page images

- **28 individual pages**, `0072B` through `0086A`, approx 2200x3040 px
- Split from fourteen two-page spreads (archive pages 77-90)
- Naming: archive page N → left=recto(A) of leaf N-4, right=verso(B) of leaf N-5
- `../cam1753-spread-splits-doc/` records each split
- Provenance, and the last commit that holds the spreads, are documented in
  `../cam1753-spreads-provenance.md`

## Coverage

- Line breaks: 27 pages, `0072B` through `0085B`, from Ps 149:7 through the end of Job.
  Page `0086A` is past Job and has no line-break file.
- Column quadrilaterals: all 28 pages.
- All 27 line-break files carry line markers. The frozen report
  [`../check_line_breaks.html`](../check_line_breaks.html) says all checks passed for the
  27 pages, as a check on 2026-09-26 found.

### Verse labels in the retained line-break files

The table reports the first and last verse-marker labels in the retained JSON files,
not independently verified manuscript ranges. "Fragment" means a stored
verse-fragment-start or verse-fragment-end marker. The stored data is unchanged.

| Page | First label | Last label |
|---|---|---|
| 0072B | Psalms 149:7, fragment | Job 1:16, fragment |
| 0073A | Job 1:16, fragment | Job 3:5, fragment |
| 0073B | Job 3:5, fragment | Job 5:2, fragment |
| 0074A | Job 5:2, fragment | Job 6:15, fragment |
| 0074B | Job 6:15, fragment | Job 8:6, fragment |
| 0075A | Job 8:6, fragment | Job 9:30, fragment |
| 0075B | Job 9:31, verse-start | Job 11:18, fragment |
| 0076A | Job 11:19, verse-start | Job 13:17, fragment |
| 0076B | Job 13:17, fragment | Job 15:9, fragment |
| 0077A | Job 15:9, fragment | Job 16:16, fragment |
| 0077B | Job 16:16, fragment | Job 19:2, fragment |
| 0078A | Job 19:3, verse-start | Job 20:17, fragment |
| 0078B | Job 20:17, fragment | Job 21:32, fragment |
| 0079A | Job 21:32, fragment | Job 23:14, fragment |
| 0079B | Job 23:14, fragment | Job 26:10, fragment |
| 0080A | Job 26:10, fragment | Job 28:16, fragment |

At 0075A/0075B, 0075B/0076A, 0077B/0078A, and 0080A/0080B, the earlier file
ends with a fragment-end label and the next file starts with the following verse's
verse-start label. These stored markers do not provide a consistent description of
verse continuation across pages. The table displays the labels without resolving
the manuscript boundary.

The table stops at 0080A; `cam1753-line-breaks/` holds all 27 pages.

## Line-break files

Each `../cam1753-line-breaks/<page>.json` is a flat JSON array (a "flat stream") of MAM's
atoms, as plain Hebrew strings split after every maqaf, and one-key markers:

- **Structural markers:** `{"page-start": "0072B"}`, `{"page-end": "0072B"}`
- **Verse markers:** `{"verse-start": "Job 1:16"}`, `{"verse-end": "Job 1:16"}`, and
  `verse-fragment-start` and `verse-fragment-end` where a page begins or ends mid-verse
- **Parashah markers:** `{"parashah": "spi-pe2"}`
- **Line markers:** `{"line-start": {"col": 1, "line-num": 1}}` and
  `{"line-end": {"col": 1, "line-num": 1}}`
- **Blank lines:** `{"blank-line": {"col": 1, "line-num": 13}}`

Col 1 = the right column (read first), Col 2 = the left column, and each column's lines
count from 1 to 26. A “blank line” is a line without verse content (masorah notes,
decorations between books, etc.), not necessarily visually empty.

The streams were generated from `../../MAM-simple/xml-vtrad-mam/` with the segmentation
that `get_verse_atoms` in `../../py/mb_cmn/mam_xml_verses.py` now gives, and the line
markers were then added by hand in an interactive editor, one page at a time.
[`reading-mam-simple.md`](reading-mam-simple.md) describes the reader's choices.

## Column quad data

- **28 JSON files** in `../cam1753-col-quads/` — manually defined bounding quadrilaterals
- Col1 = RIGHT column (read first in RTL), Col2 = LEFT column
- Each has `rel` (0-1 normalized) and `px` coordinates for corners tl/tr/bl/br
- 26 weighted line-boxes per column: top box 1.5x (ascenders), bottom box 1.25x (descenders), 24 normal
- Made in an interactive HTML editor, which was retired with the rest

## Key Files

| File | Purpose |
|------|---------|
| `../cam1753-line-breaks/*.json` | Line-break data per page (flat stream + markers) |
| `../cam1753-col-quads/*.json` | Column bounding quad data |
| `../cam1753-spread-splits-doc/*.json` | Where each spread was split into pages |
| `../check_line_breaks.html` | The frozen report of the last line-break check |
| `../../py/mb_cmn/mam_xml_verses.py` | MAM-simple verse and atom extraction |
| `../../MAM-simple/xml-vtrad-mam/*.xml` | Hebrew Bible text source |
