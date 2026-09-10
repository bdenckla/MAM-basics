# MAM-basics

Python tools for working with [MAM (Miqra according to the Masora)](https://he.wikisource.org/wiki/מקרא_על_פי_המסורה), a scholarly edition of the Hebrew Bible hosted on Hebrew Wikisource, featuring full Masoretic pointing (niqqud) and cantillation marks (te'amim).

## What's here

### Core export pipeline

`main_mam_simple.py` reads from the [MAM-parsed](MAM-parsed/README.md) product directory, produces XML and JSON exports of MAM under [`MAM-simple/`](MAM-simple/), and refreshes its example-program support files there.

### Landed product and corpus directories

Each landed product keeps its detailed README beside the files it describes. This root index names the product directories that formerly had repositories of their own.

- [`MAM-parsed/`](MAM-parsed/README.md) — plain and plus parsed MAM JSON, historical release inputs, documentation, and a toy example
- [`MAM-simple/`](MAM-simple/) — XML and JSON MAM exports in three versifications
- [`MAM-for-Sefaria/`](MAM-for-Sefaria/) — CSV MAM export suitable for Sefaria import; its [encoding documentation](https://bdenckla.github.io/MAM-basics/MAM-for-Sefaria/) is published with this site
- [`MAM-with-doc/`](MAM-with-doc/README.md) — MAM's HTML edition with documentation notes; its [published edition](https://bdenckla.github.io/MAM-basics/MAM-with-doc/) is in the site tree
- [`MAM-OSIS/`](MAM-OSIS/README.md) — OSIS MAM exports for conversion to SWORD format, with configuration and documentation
- [`aleppo/`](aleppo/) — Aleppo Codex page-location data and photographed-page records
- [`cam1753/`](cam1753/) — Cambridge MS Add. 1753 page-location data and source scans
- [`leningrad/`](leningrad/) — Leningrad Codex index data and page-image evidence
- [`book-of-job/`](book-of-job/) — data and reading procedures for the BHQ Job review
- [`holman/`](holman/) — data and rendered reports from Daniel Holman's three review/correction bodies
- [`uxlc/`](uxlc/) — UXLC data and documentation for the planned CLC edition
- [`diffable-pointed-hebrew/`](diffable-pointed-hebrew/) — samples and product-specific short Unicode-name overrides

### Format variants

- `main_mam4sef.py` — Sefaria-compatible MAM variant by default, with `--just-ajf` and `--both-sef-and-ajf` for AJF selection
- `main_mam_with_doc.py` — HTML with two-column layout and documentation notes
- `main_mam_osis.py` — OSIS (Open Scripture Information Standard) XML

### Downloading

- `main_download.py fr-google` — from Google Sheets
- `main_download.py fr-sefaria` — from Sefaria
- `main_download.py fr-wikisource` — the MAM books, from Hebrew Wikisource
- `main_download.py fr-ws-intro` — the MAM introduction's thirteen pages, from Hebrew Wikisource, mirrored as verbatim wikitext in `in/mam-ws-intro/`

### Parsing

- `main_parse.py go` — parses downloaded Google Sheets data into the independent comparison product
- `main_parse.py ws` — parses downloaded Wikisource data into format 2 and the production plain/plus products

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

- `main_authored.py` — generates miscellaneous HTML documentation; its `gen-site` subcommand writes the eleven deploy-root pages: `gh-pages/index.html`, `gh-pages/unicode-proposals.html`, and the nine `gh-pages/post-stress-meteg*.html` pages
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
misc/linux-sh/   Standalone Linux bootstrap script for cloning MAM-basics
```

Naming note: `mb_` means "from MAM-basics." The MAM-simple examples currently
receive copies from `mb_cmn`, `mb_misc`, `mb_sefaria`, and `osis`. For
`mb_xml`, `mb_json`, and other packages that are not currently copied, the
`mb_` prefix is additionally useful to avoid collisions with common package
names.

## License

Two declarations, because this repository holds code and data under different terms:

1. **Code: GPL-3.0**, in [`LICENSE`](LICENSE). This covers MAM-basics' work in code and prose —
   everything under `py/`, `.github/` and `doc/` except the third-party font under `doc/woff2/`,
   and the generated indexes and reports under `out/` that carry no corpus text.
2. **Data: mapped path by path** in [`DATA-LICENSES.md`](DATA-LICENSES.md). Most corpora keep the
  terms their preparers set: MAM is CC-BY-SA 4.0, attributed to Hebrew Wikisource, and several
  other corpora are reproduced under no grant at all. The accent-grammar material that is this
  repository's own work is CC0 1.0, dedicated in that file. Read it before redistributing
  anything under `in/`, `gh-pages/wlc/` or the derived trees under `out/`.
