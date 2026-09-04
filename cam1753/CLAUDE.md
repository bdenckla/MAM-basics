# CLAUDE.md

What this repo is, its pipeline and its page/column conventions are in [README.md](README.md);
the longer references are in [`doc/`](doc/). Only what an assistant gets wrong without being
told is below.

## There is no Python here — the code is `../MAM-basics/py/`

Every `.py` this repo tracked left on 2026-08-22, under Phase 4 of
`../MAM-basics/doc/PLAN-evacuate-python-from-codex-index-trio.md`. **Twenty-three files: do not
put one back.** Fifteen of them sat loose at this repo's root, beside the data they read.

**Twelve of the twenty-three did not move — they were deleted as duplicates**, MAM-basics
already holding the same text:

- `py_cam1753_word_image/` (4) — one committed blob with MAM-basics' copy, which arrived there
  with book-of-job's own evacuation on 2026-08-19.
- `mb_cmn/` (3) — vendored from MAM-basics, all three byte-identical.
- `check_mark_order.py`, `check_escape_sequences.py`, `fix_mark_order.py` and
  `fix_escape_sequences.py` — MAM-basics holds all four. What they needed was this repo's code
  and corpus IN their scope, not a second copy of the script.
- `py_mam_xml/mam_xml_verses.py` — see the section below, which is the one deletion that took a
  decision rather than a comparison.

**The eleven that moved kept their names and dropped a `cam1753` infix** that the package name
`py_cam1753_loc` now carries: `gen_cam1753_flat_stream.py` is `py_cam1753_loc/gen_flat_stream.py`
there. Each is reached through a wrapper at MAM-basics' `py/` top level, named `main_cam1753_`
plus the module's own stem — so `main_cam1753_gen_flat_stream.py`. The two checks became
`check_cam1753_all.py` and `check_cam1753_word_finding.py`.

**Four of the eight now share a module name with codex-index-aleppo's exactly** —
`check_line_breaks`, `gen_flat_stream`, `gen_line_break_editor` and `gen_col_quad_editor`, in
`py_cam1753_loc/` and `py_ac_loc/` respectively. The two manuscripts' answers to one problem sit
under one set of names in two packages, and their entry points differ only in `main_cam1753_`
against `main_ac_`.

**`requirements.txt` and `codex-index-cam1753.code-workspace` went with the Python**, on Ben's
decisions of 2026-08-22. The first named black, matplotlib and pyspellchecker and nothing here
imports any of them now; the second declared a three-folder view opening this repo beside
book-of-job and codex-index-aleppo, and both of those repos' workspace files were deleted the
same way, so nothing opens the three together any more.

## The MAM-XML reader is codex-index-aleppo's now, and one tag is why

`py_mam_xml/mam_xml_verses.py` here and `py_ac_loc/mam_xml_verses.py` in codex-index-aleppo were
**the same tool with 43 lines of drift**, most of it docstring. A census of every tag in the
three books both read — Ps, Job and Prov, whose `MAM-XML/` snapshots are byte-identical across
the two repos — found **exactly one treated differently**:

- **`spi-invnun`**, 7 occurrences, all in `Ps.xml`, first at `Ps.107.23`. Those are the inverted
  nuns (nun hafukha) of Psalm 107.
- codex-index-aleppo's copy **raised** on it, having grown a fail-fast `else: raise` for unknown
  tags without ever being given a clause for that one. This repo's copy **silently skipped** it,
  having no `else` at all.

The shared copy was given the missing clause — the mark carries no text, so it is skipped exactly
as `implicit-maqaf` and `shirah-space` already were — and this repo's copy was deleted.
**Verified by loading both readers side by side over whole-book ranges of all three books: 4512
verses, 30322 words, 0 mismatches.** So nothing this repo generates changed.

## What MAM-basics writes here

Run either from anywhere; each addresses this repo by absolute path, through
`MAM-basics/py/cam1753_paths.py`.

**28 page images and 15 split records**, from the 14 downloaded spreads:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_cam1753_split_spreads.py
```

**`check_line_breaks.html`**, rewritten by every run of the check register:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/check_cam1753_all.py
```

**Those 44 files are the oracle**: run both and all 44 come back byte-identical unless something
real has changed, which is what MAM-basics' Phase 3 used to prove the move. `check_cam1753_all.py`
reports **4 of 4**, and its word-finding check passes **160 of 160** where codex-index-aleppo's
structurally identical one fails 160 of 160 — that manuscript's line-break JSON migrated to an
N-of-M column identifier in 2026-03 and this one keeps `"col": 1`.

**`git status --porcelain` is a usable instrument in this repo**, unlike codex-index-aleppo's,
where two thirds of the tracked files are CRLF on disk against an LF blob. Only 1 of this repo's
176 files was, and the seven missing `newline=""` writes that used to dirty the tree on every
check run were all closed on 2026-08-22.

**`cam1753-gutter-profiles.png` is NOT part of the oracle.** `py_cam1753_loc/gutter_profile.py`
re-renders it byte-identically run-to-run under one matplotlib version, but 1,541 bytes larger
than the tracked copy under a newer one — so its bytes track the matplotlib version rather than
the code, and a re-render is a deliberate act rather than a verification.

## What no program writes

**97 of this repo's 142 tracked artifacts are written by no program**, and will not come back if
they are lost:

| Tree | Files | Where it comes from |
|---|---|---|
| `cam1753-col-quads/` | 28 | human-annotated, through the editor |
| `cam1753-line-breaks/` | 27 | human-annotated, through the editor |
| `MAM-XML/` | 24 | vendored snapshot of MAM-simple's `xml-vtrad-mam` |
| `cam1753-spreads/` | 14 | downloaded scans from archive.org |
| `page-snips/` | 2 | one hand-made crop and the README recording what it settles |
| `cam1753-page-index.json` | 1 | hand-made, and read by no program at all |
| `test-data-from-book-of-job.json` | 1 | extracted from book-of-job's quirk records |

**The other 45 artifacts are generated, but only 44 of them reproducibly.** The 44 are
`check_line_breaks.html`, the 28 under `cam1753-pages/` and the 15 under
`cam1753-spread-splits-doc/`; the forty-fifth is `cam1753-gutter-profiles.png`, for the reason
the section above gives.

**The remaining 10 of this repo's 152 tracked files are its own paperwork**, and are artifacts of
nothing: the three under `doc/`, `README.md`, this file, `MAM-simple-provenance.md`,
`cam1753-spreads-provenance.md`, `things-noticed-in-cam1753.md`, `.gitattributes` and
`.gitignore`. 97 + 45 + 10 = 152.

## The interactive editors need a local HTTP server, started separately

They will not work from a `file://` URL, and none of them starts a server for itself — each
expects one to be running already, at a port it hardcodes. Start the server **from this repo's
root**, even though the code is now in MAM-basics:

| Editor | Server to start first |
|---|---|
| `main_cam1753_gen_col_quad_editor.py`, `main_cam1753_gen_line_break_editor.py` | `python -m http.server 8119` from this repo's root (they load `http://localhost:8119/cam1753-pages/...`) |
| `main_cam1753_find_word_in_images.py` | `python -m http.server 8753 -d .novc` (`SERVER_PORT` in that script) |

`file://` fails for two separate reasons, so neither is fixable by adjusting the page: the
image loads cross-origin, and `navigator.clipboard` / `canvas.toBlob()` need a secure context.
Plain `http://localhost` counts as a secure context in every major browser, so no TLS is needed.
A static, read-only HTML file that does none of that opens fine as a file.

## Hebrew combining marks are in this project's own order, not Unicode's

Never run `unicodedata.normalize` (NFC, NFD, or any other form) over Hebrew text here. NFC
reorders combining marks and destroys the order this project deliberately keeps. The order, and
the authoritative implementation, are `give_std_mark_order` in
`../MAM-basics/py/mb_cmn/uni_denorm.py`, which is where it is maintained and which this repo's
own `mb_cmn/` was a byte-identical copy of until the move.
`../MAM-basics/py/check_mark_order.py` checks a tree against it and is wired into
`check_cam1753_all.py`. When two Hebrew strings that should be equal do not match, put both
through `give_std_mark_order` rather than normalizing.

## MAM-basics still lints this repo, and now scans it for NFC

Deleting the code here did not end the checks that ran over this repo's data, and added one that
never ran here at all.

- **`check_mark_order.py` and `check_escape_sequences.py` in MAM-basics take a union of per-repo
  scope lists**, and `cam1753_paths.code_paths()` plus this repo's data root are two entries in
  it. So the moved code is still linted, and so are this repo's 72 tracked JSON.
- **`py/tests/test_h_dot_below_nfc.py` in MAM-basics carries a `codex-index-cam1753` scope**,
  added when the code moved. **This repo never had a copy of that test**, so unlike the other
  five evacuated repos this is a new check rather than a preserved one. It was added because
  otherwise nothing anywhere would read this repo's hand-authored Hebrew, and it passed on the
  first run. **14 files are in scope**, the six artifact trees being excluded.
