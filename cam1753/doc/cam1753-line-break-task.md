# cam1753 Line-Break Marking Task

## Manuscript

Cambridge University Library, MS Add. 1753 (Ketuvim). Images downloaded from archive.org (item `ketuvim-cambridge-ms-add-1753-images`, zip `Ketuvim_Cambridge_MS_Add_1753_jp2.zip`, scale=2, server `ia800901.us.archive.org`).

## Page Images

- **28 individual pages** in `cam1753-pages/` (0072B.jpg through 0086A.jpg, approx 2200x3040 px)
- Split from two-page spreads in `cam1753-spreads/` (archive pages 77-90)
- Naming: archive page N → left=recto(A) of leaf N-4, right=verso(B) of leaf N-5
- Provenance documented in `cam1753-spreads-provenance.md`

## Column Quad Data

- **28 JSON files** in `cam1753-col-quads/` — manually defined bounding quadrilaterals
- Col1 = RIGHT column (read first in RTL), Col2 = LEFT column
- Each has `rel` (0-1 normalized) and `px` coordinates for corners tl/tr/bl/br
- 26 weighted line-boxes per column: top box 1.5x (ascenders), bottom box 1.25x (descenders), 24 normal
- Generated via `../../py/main_cam1753_gen_col_quad_editor.py` (interactive HTML editor, serves images via localhost:8119)

## Local HTTP Server

HTML editors that load page images need `http://localhost:8119/` serving
`C:/Users/BenDe/GitRepos/MAM-basics/cam1753`. Start there with:
```
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m http.server 8119
```
Run in background. Required because browsers block `file://` cross-origin image loads in SVG/canvas.

## Status

- [x] Download and split page images (28 pages)
- [x] Column quad data for all 28 pages
- [x] Identify text on pages: Ps 149:7 through end of Job (page 0085B). Page 0086A is past Job — ignore it. 27 pages total: 0072B through 0085B.
- [x] Build flat stream generator (`../../py/main_cam1753_gen_flat_stream.py`)
- [x] Build line-break editor (`../../py/main_cam1753_gen_line_break_editor.py`) with blank-line feature
- [ ] Mark line breaks for all 27 pages (0072B through 0085B)

### Pages completed

| Page   | Start verse       | End verse (fragment) |
|--------|-------------------|----------------------|
| 0072B  | Ps 149:7          | Job 1:16 (mid)       |
| 0073A  | Job 1:16 (mid)    | Job 3:19 (mid)       |
| 0073B  | Job 3:19 (mid)    | Job 5:16 (mid)       |
| 0074A  | Job 5:16 (mid)    | Job 6:29 (mid)       |
| 0074B  | Job 6:29 (mid)    | Job 8:6 (mid)        |
| 0075A  | Job 8:6 (mid)     | Job 9:31 (mid)       |
| 0075B  | Job 9:31 (mid)    | Job 11:19 (mid)      |
| 0076A  | Job 11:19 (mid)   | Job 13:18 (mid)      |
| 0076B  | Job 13:18 (mid)   | Job 15:10 (mid)      |
| 0077A  | Job 15:10 (mid)   | Job 16:16 (mid)      |
| 0077B  | Job 16:16 (mid)   | Job 19:3 (mid)       |
| 0078A  | Job 19:3 (mid)    | Job 20:18 (mid)      |
| 0078B  | Job 20:18 (mid)   | Job 21:32 (mid)      |
| 0079A  | Job 21:32 (mid)   | Job 23:14 (mid)      |
| 0079B  | Job 23:14 (mid)   | Job 25:6 (mid)       |
| 0080A  | Job 26:10 (mid)   | Job 28:17 (mid)      |

## Procedure: Marking Line Breaks Page by Page

### First page (bootstrapping)

1. User identifies the starting verse (e.g. `Ps 149:7`) and a generous ending verse.
2. Generate the flat stream:
   ```
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_cam1753_gen_flat_stream.py 0072B Ps 149:7 Job 2:10
   ```
3. Generate and open the editor (always start with col 1):
   ```
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_cam1753_gen_line_break_editor.py 0072B 1
   ```
   The script writes the HTML and opens it in the browser automatically.
4. In the editor: right-click the actual first word on the page to set page-start (if the flat stream includes earlier words from the same verse). Click the last word of each line to mark line-ends. Click line numbers to add blank lines (for masorah notes, inter-book gaps, etc. — any line without verse content). Use the col toggle to switch between columns.
5. Click **Export** → paste directly into `cam1753-line-breaks/<page_id>.json`.
6. **Do NOT** paste the exported JSON into the chat window — that causes Unicode NFC normalization of Hebrew text.

### Subsequent pages (chaining)

1. Generate the flat stream with `--chain`, which reads the previous page\u2019s JSON and starts at the next word:
   ```
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_cam1753_gen_flat_stream.py 0073A --chain 0072B Job 4:10
   ```
   This auto-detects whether the previous page ended mid-verse (generates a `verse-fragment-start`) or at a verse boundary (starts at next full verse). The end verse (`Job 4:10`) should be generous — extra verses at the end are harmless.
2. Generate and open the editor:
   ```
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_cam1753_gen_line_break_editor.py 0073A 1
   ```
3. Mark line breaks, export, paste into file (same as bootstrapping steps 4-6).

### Important notes

- **The flat stream generator refuses to overwrite** existing files. Use `--force` to overwrite deliberately.
- **Minimum word count**: The generator requires at least 300 words. If it rejects, use a later end verse.
- **Always use MAM-basics' interpreter by absolute path** — never bare `python`. The
  active interpreter is `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`.
- **Never use `python -c "..."`** one-liners — always create a script in `.novc/`, per the user-level `CLAUDE.md`'s "Running scripts — no inline one-liners" section, whose temp-file-location bullet names a repo's gitignored scratch dir first.
- The editor loads images from `http://localhost:8119/cam1753-pages/` — the local HTTP server must be running.
- Col 1 = right column (read first), Col 2 = left column. The editor has a toggle button to switch.
- “Blank lines” are lines without verse content (masorah notes, decorations between books, etc.), not necessarily visually empty.

### Editor features

- **Sync mode** (on by default, toggle with `s` key): highlights the next line to mark in the image panel using a reverse-highlight fade, and scrolls both image and words panels to track progress.
- **Auto-switch**: when col 1 reaches 26 line-ends, automatically switches to col 2.
- **Flat-order line numbering**: line numbers are assigned from a single flat counter across both columns (1–26 = col 1, 27–52 = col 2). Inserting or removing a line-end in col 1 correctly shifts col 2 numbering.
- **Crop toggle**: switch between column-cropped and full-page image view.
- **Resizable divider**: drag the divider between words and image panels.

## Key Files

| File | Purpose |
|------|---------|
| `../../py/main_cam1753_gen_flat_stream.py` | Generate flat-stream JSON for a page (manual or `--chain` mode) |
| `../../py/main_cam1753_gen_line_break_editor.py` | Generate interactive HTML editor for marking line breaks |
| `cam1753-line-breaks/*.json` | Line-break data per page (flat stream + markers) |
| `cam1753-col-quads/*.json` | Column bounding quad data (used by editor for image cropping) |
| `cam1753-pages/*.jpg` | Individual page images |
| `../../py/py_ac_loc/mam_xml_verses.py` | MAM-simple verse extraction |
| `../../MAM-simple/xml-vtrad-mam/*.xml` | Hebrew Bible text source |
