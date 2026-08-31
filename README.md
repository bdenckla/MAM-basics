# MAM-basics

Python tools for working with [MAM (Miqra according to the Masora)](https://he.wikisource.org/wiki/מקרא_על_פי_המסורה), a scholarly edition of the Hebrew Bible hosted on Hebrew Wikisource, featuring full Masoretic pointing (niqqud) and cantillation marks (te'amim).

## What's here

### Core export pipeline

`main_mam_simple.py` reads from the [MAM-parsed](https://github.com/bdenckla/MAM-parsed) sibling repo, produces XML and JSON exports of MAM, and refreshes the Python support files copied to the MAM-simple sibling repo.

### Format variants

- `main_mam4sef.py` — Sefaria-compatible MAM variant by default, with `--just-ajf` and `--both-sef-and-ajf` for AJF selection
- `main_mam_with_doc.py` — HTML with two-column layout and documentation notes
- `main_mam_osis.py` / `main_osis_split_mapm.py` — OSIS (Open Scripture Information Standard) XML

### Downloading

- `main_download.py fr-google` — from Google Sheets
- `main_download.py fr-sefaria` — from Sefaria
- `main_download.py fr-wikisource` — the MAM books, from Hebrew Wikisource
- `main_download.py fr-ws-intro` — the MAM introduction's thirteen pages, from Hebrew Wikisource, mirrored as verbatim wikitext in `in/mam-ws-intro/`

### Parsing

- `main_parse.py go` — parses downloaded Google Sheets data into structured form
- `main_parse.py ws` — parses downloaded Wikisource data into structured form

### Diffing and comparison

- `main_diff.py wsgo` — diffs Wikisource vs. Google Sheets versions
- `main_diff.py ctr-vs-mam` — compares CTR data against MAM verse data
- `main_diff.py mpp` — compares MAM-parsed plus revisions and writes release diff reports

### Analysis and surveys

- `main_foi_features_of_interest.py` — identifies and catalogs linguistic/textual patterns
- `main_multimark.py` — records letters that carry multiple diacritical marks
- `main_wordlist.py` — generates a JSON list of qere words
- `main_tmpl_survey.py` — surveys Wikisource template usage patterns
- `main_explicit_xataf.py` — extracts explicit-xataf word variants from נוסח notes
- `main_decnreub.py` — writes dual-cantillation (Reuben) info to JSON

### Wikisource bot

- `main_ws_bot.py real` — edits Hebrew Wikisource pages via pywikibot; writes per-chapter run artifacts under `.novc/mam-ws-bot-real-runs/<timestamp>/`; by default, then downloads modified chapters to `in/mam-ws` and reparses affected books (use `--no-post-download` to skip); for process/idempotence checks, use `--identity-run` to avoid saving pages and fail if any chapter would change
- `main_ws_bot.py proto` — prototype version using local file I/O

### Utilities

- `main_authored.py` — generates miscellaneous HTML documentation
- `main_rename_jpeg_scans.py` — renames JPEG scan files by directory structure
- `main_0_mega.py` — meta-orchestrator that runs multiple jobs in sequence
- `main_repo_maintenance.py` — routine repo maintenance: clean `.novc/`, run `main_test.py`, run `main_0_mega.py`

### Cross-repo utility entrypoint

Use `main_repo_util.py` for one-off cross-repo utility operations with one required exclusive action switch:

```bash
.venv/Scripts/python.exe py/main_repo_util.py --run-black --repos MAM-basics
.venv/Scripts/python.exe py/main_repo_util.py --audit-line-terms --repos MAM-basics
.venv/Scripts/python.exe py/main_repo_util.py --commit-across-repos --message-file .novc/commit_msg_shared.txt --dry-run
```

Supported exclusive actions:

- `--run-black`
- `--audit-line-terms`
- `--commit-across-repos`

## Setup

This project requires Python 3 with a virtual environment.

```bash
python -m venv .venv
.venv/Scripts/pip.exe install -r requirements.txt
```

Run scripts from the repo root (not from `py/`):

```bash
.venv/Scripts/python.exe py/main_mam_simple.py
```

Run tests through the unified harness:

```bash
.venv/Scripts/python.exe py/main_test.py
```

Optional: list or run selected test groups:

```bash
.venv/Scripts/python.exe py/main_test.py --list
.venv/Scripts/python.exe py/main_test.py --ws-urls-encoding
```

## Repository layout

```
py/              Python source
  main_*.py      Entry-point scripts
  mb_cmn/         Common utilities
  mb_json/       JSON helpers
  mb_xml/        XML rendering
  render_wt/     General rendering
  mb_sefaria/     Sefaria-specific logic
  ws/            Wikisource-specific logic
  mpplus/        MAM parsed-plus helpers
  ...
in/              Input data files
doc/             Documentation and notes
linux-sh/        Shell scripts for Linux setup
```

Naming note: `mb_` means "from MAM-basics." For currently vendored
packages such as `mb_cmn`, `mb_diff_mpu`, and `mb_author`, the prefix
also signals vendoring origin. For `mb_xml` and `mb_json`, which are
not currently vendored, `mb_` is additionally useful to avoid collisions
with common `xml` and `json` package names.

## License

Two declarations, because this repository holds code and data under different terms.

- **Code: GPL-3.0**, in [`LICENSE`](LICENSE). This covers MAM-basics' own work in code and prose —
  everything under `py/`, `.github/` and `doc/`, and the generated indexes and reports under
  `out/` that carry no corpus text.
- **Data: mapped path by path** in [`DATA-LICENSES.md`](DATA-LICENSES.md). Most corpora keep the
  terms their preparers set: MAM is CC-BY-SA 4.0, attributed to Hebrew Wikisource, and several
  other corpora are reproduced under no grant at all. The accent-grammar material that is this
  repository's own work is CC0 1.0, dedicated in that file. Read it before redistributing
  anything under `in/`, `gh-pages/wlc/` or the derived trees under `out/`.
