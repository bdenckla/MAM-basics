# MAM-basics

This repository contains files related to [MAM (Miqra according to the Masorah)](https://he.wikisource.org/wiki/מקרא_על_פי_המסורה), a scholarly (and practical!) edition of the Hebrew Bible hosted on Hebrew Wikisource. MAM features full Masoretic pointing (niqqud) including cantillation marks (te'amim). This repository's files include Python tools and the products they generate, among them a published website.

## What's here

### Core pipeline

1. **Download.** `main_download.py fr-wikisource` downloads MAM's books from Hebrew Wikisource into `in/mam-ws/` and maintains a 36-page special-page mirror under `in/mam-ws-special/`.
2. **Parse.** `main_parse.py ws` parses the downloaded Wikisource MAM into [MAM-parsed-plus](MAM-parsed/README.md) under `MAM-parsed/plus/`.
3. **Make MAM-simple.** `main_mam_simple.py` reads `MAM-parsed/plus/` and produces XML and JSON exports of MAM under [`MAM-simple/`](MAM-simple/).
4. **Make MAM-for-Sefaria and MAM-OSIS.** MAM-simple is used to make two more products: `main_mam4sef.py` writes [`MAM-for-Sefaria/`](MAM-for-Sefaria/), and `main_mam_osis.py` writes [`MAM-OSIS/`](MAM-OSIS/README.md).

Another product that, like MAM-simple, has `MAM-parsed/plus/` as its source is the "MAM with doc" edition: `main_mam_with_doc.py` writes its HTML pages, in a two-column layout with documentation notes, under `gh-pages/MAM-with-doc/`.

Two diagrams show this pipeline:

1. [`doc/process-documentation/pipeline.svg`](doc/process-documentation/pipeline.svg) draws the programs named above and the Wikisource bot, with Hebrew Wikisource and the directories they read and write. A solid box is a program that `py/main_0_mega.py` runs, labelled with its step ids; a dashed box is a program run by hand.
2. [`doc/process-documentation/MAM-process.dot.svg`](doc/process-documentation/MAM-process.dot.svg)

### Product and corpus directories

Several of the directories below have a README of their own, beside the files it describes.

- [`MAM-parsed/`](MAM-parsed/README.md) — MAM-parsed-plus JSON, historical release inputs, documentation, and a toy example
- [`MAM-simple/`](MAM-simple/) — XML and JSON MAM exports in three versifications
- [`MAM-for-Sefaria/`](MAM-for-Sefaria/) — CSV MAM export suitable for Sefaria import; its [encoding documentation](https://bdenckla.github.io/MAM-basics/MAM-for-Sefaria/) is published with this site
- [`MAM-with-doc/`](MAM-with-doc/README.md) — an HTML edition of MAM with documentation notes; its [published edition](https://bdenckla.github.io/MAM-basics/MAM-with-doc/) is in the site tree
- [`MAM-OSIS/`](MAM-OSIS/README.md) — OSIS MAM exports for conversion to SWORD format, with configuration and documentation
- [`Phonetic-MAM/`](Phonetic-MAM/README.md) — the Phonetic MAM display as JSON: MAM's displayed Hebrew with its Sephardic and Ashkenazic transcriptions; `main_phonetic_mam.py` exports it and renders its [published pages](https://bdenckla.github.io/MAM-basics/phonetic-mam/) in the site tree
- [`Yeivin-ITM/`](Yeivin-ITM/README.md) — the exact fractions behind the meteg claims Ben Denckla added to his adaptation of selected excerpts from Israel Yeivin's *Introduction to the Tiberian Masorah*; `main_yeivin_itm.py` writes them and renders the [published excerpts](https://bdenckla.github.io/MAM-basics/yeivin-itm/yeivin_itm.html) in the site tree
- [`aleppo/`](aleppo/) — Aleppo Codex page-location data
- [`cam1753/`](cam1753/) — Cambridge MS Add. 1753 page-location data
- [`evr-ii-b-55/`](evr-ii-b-55/) — St. Petersburg Evr. II B 55 page-location data
- [`in/lci_recs.json`](in/lci_recs.json) — Leningrad Codex page-location data
- [`book-of-job/`](book-of-job/) — files related to the BHQ Job review
- [`holman/`](holman/) — files related to Daniel Holman's change proposals
- [`uxlc/`](uxlc/) — files related to UXLC

### Downloading

- `main_download.py fr-ws-intro` — the MAM introduction's thirteen pages, from Hebrew Wikisource, mirrored as verbatim wikitext in `in/mam-ws-intro/`

### Diffing and comparison

- `main_diff.py mpplus` — compares MAM-parsed plus revisions and writes release diff reports

### Analysis and surveys

- `main_foi_features_of_interest.py` — identifies and catalogs linguistic/textual patterns
- `main_multimark.py` — records letters that carry multiple diacritical marks
- `main_wordlist.py` — generates a JSON list of qere words
- `main_tmpl_survey.py` — surveys Wikisource template usage patterns
- `main_explicit_xataf.py` — extracts explicit-xataf word variants from נוסח notes
- `main_decnreub.py` — writes dual-cantillation (Reuben) info to JSON

### Wikisource bot

- `main_ws_bot.py real` — edits Hebrew Wikisource pages via pywikibot
- `main_ws_bot.py proto` — prototype version using local file I/O

### Utilities

- `main_authored.py` — generates miscellaneous HTML documentation
- `main_0_mega.py` — orchestrator that runs multiple jobs in sequence
- `main_repo_maintenance.py` — routine repo maintenance, e.g. clean `.novc/`


## Setup

This project requires Python 3 with a virtual environment. On MS-Windows:

```bash
python -m venv .venv
.venv/Scripts/pip.exe install -r requirements.txt -c constraints.txt
```

Run scripts from the repo root, not from `py/`. On MS-Windows:

```bash
.venv/Scripts/python.exe py/main_mam_simple.py
```

Run tests through the unified harness (on MS-Windows):

```bash
.venv/Scripts/python.exe py/main_test.py
```

## Repository layout

Hebrew Wikisource is the maintained textual source. The former MAM Google Sheet has
been a frozen historical archive since September 12, 2026; its download, comparison,
and auto-edit pipeline is no longer part of this repository.

```
py/              Python source
  main_*.py      Entry-point scripts
  mb_cmn/        Common utilities
  mb_json/       JSON helpers
  mb_xml/        XML rendering
  render_wt/     General rendering
  mb_sefaria/    Sefaria-specific logic
  ws/            Wikisource-specific logic
  mpplus/        MAM parsed-plus helpers
  ...
in/              Input data files
doc/             Documentation and notes
misc/linux-sh/   Standalone Linux bootstrap script for cloning MAM-basics
```

## License

Two declarations, because this repository holds code and data under different terms:

1. **Code: GPL-3.0**, in [`LICENSE`](LICENSE). This covers MAM-basics' work in code and prose —
   everything under `py/`, `.github/` and `doc/` except the adapted excerpts and their remarks under
   `py/yeivin_itm/content/`, the third-party font under `doc/woff2/`, and the page crops in
   `doc/*-snips/` and the Hebrew Wikisource Village Pump discussion captured and translated in
   `doc/wikisource-dagesh-discussion-*`, and the generated indexes and reports under `out/` that
   carry no corpus text. Six rendering-helper modules beside the excerpts are GPL-3.0 code;
   [`DATA-LICENSES.md`](DATA-LICENSES.md) names them.
   The excerpts' path-specific permission terms are in [`Yeivin-ITM/README.md`](Yeivin-ITM/README.md)
   and [`DATA-LICENSES.md`](DATA-LICENSES.md); no GPL sublicense over them is asserted.
2. **Data: mapped path by path** in [`DATA-LICENSES.md`](DATA-LICENSES.md). Most corpora keep the
  terms their preparers set: MAM is CC-BY-SA 4.0, attributed to Hebrew Wikisource, and several
  other corpora are reproduced under no grant at all. The accent-grammar material that is this
  repository's own work is CC0 1.0, dedicated in that file. Read it before redistributing
  anything under `in/`, `gh-pages/wlc/` or the derived trees under `out/`.
