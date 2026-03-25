# MAM-basics

Python tools for working with [MAM (Miqra according to the Masora)](https://he.wikisource.org/wiki/מקרא_על_פי_המסורה), a scholarly edition of the Hebrew Bible hosted on Hebrew Wikisource, featuring full Masoretic pointing (niqqud) and cantillation marks (te'amim).

## What's here

### Core export pipeline

`main_mam_simple.py` reads from the [MAM-parsed](https://github.com/bdenckla/MAM-parsed) sibling repo and produces XML and JSON exports of MAM.

### Format variants

- `main_mam4sef.py` — Sefaria-compatible MAM variant
- `main_mam4ajf.py` — AJF MAM variant (similar to the Sefaria variant)
- `main_mam_with_doc.py` — HTML with two-column layout and documentation notes
- `main_osis.py` / `main_osis_split_mapm.py` — OSIS (Open Scripture Information Standard) XML

### Downloading

- `main_download_fr_google.py` — from Google Sheets
- `main_download_fr_sefaria.py` — from Sefaria
- `main_download_fr_wikisource.py` — from Hebrew Wikisource

### Parsing

- `main_parse_go.py` — parses downloaded Google Sheets data into structured form
- `main_parse_ws.py` — parses downloaded Wikisource data into structured form

### Diffing and comparison

- `main_diff_wsgo.py` — diffs Wikisource vs. Google Sheets versions
- `main_diff_ctr_vs_mam.py` — compares CTR data against MAM verse data

### Analysis and surveys

- `main_foi_features_of_interest.py` — identifies and catalogs linguistic/textual patterns
- `main_multimark.py` — records letters that carry multiple diacritical marks
- `main_wordlist.py` — generates a JSON list of qere words
- `main_tmpl_survey.py` — surveys Wikisource template usage patterns
- `main_explicit_xataf.py` — extracts explicit-xataf word variants from נוסח notes
- `main_decnreub.py` — writes dual-cantillation (Reuben) info to JSON

### Wikisource bot

- `main_ws_bot.py` — edits Hebrew Wikisource pages via pywikibot
- `main_ws_bot_proto.py` — prototype version using local file I/O

### Utilities

- `main_gen_misc_authored_english_documents.py` — generates miscellaneous HTML documentation
- `main_rename_jpeg_scans.py` — renames JPEG scan files by directory structure
- `main_mam_xml_copy_py_files.py` — copies Python support files to a sibling repo
- `main_0_mega.py` — meta-orchestrator that runs multiple jobs in sequence

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

## Repository layout

```
py/              Python source
  main_*.py      Entry-point scripts
  pycmn/         Common utilities
  pyxml/         XML rendering
  pyrender/      General rendering
  pysefaria/     Sefaria-specific logic
  pyws/          Wikisource-specific logic
  pympp/         MAM parsed-plus helpers
  ...
in/              Input data files
doc/             Documentation and notes
linux-sh/        Shell scripts for Linux setup
```
