# CLC skeleton — narrow build plan (for a fresh session)

> **Purpose:** a small, self-contained plan to stand up the **CLC walking skeleton** in a fresh
> session, without re-reading the whole design doc. Background and rationale live in
> [doc/clc-design.md](clc-design.md); this file is just the build order. Keep it narrow —
> the point is one end-to-end vertical slice, not the whole edition.

## Status: COMPLETE (as of 2026-06-29)

The skeleton is **built and exceeded** — the definition of done below is met, and several
later-phase features have already landed. (See the design doc's §11 status table for the full
picture.) Built: a `py/main_clc.py` driver writing `gh-pages/clc/<book>.html` (+ `<book>-notes.json`)
for three pilot books — **Genesis, Proverbs, 2 Samuel**.

**Deviations from this plan, as built:**
- **Note prose is the real tanach.us *note page*, not the change-log description.** A *separate*
  offline step (`py/main_clc_download_notes.py`) downloads the note pages into committed
  `in/UXLC-notes/`; the build reads them locally and never touches the network (deterministic). The
  change-log `<correction><description>` is kept **only** for the atom-letter consistency guard; an
  atom whose page is not yet downloaded shows a **`[note not yet downloaded]`** placeholder, never a
  fabricated substitute (issue #19). (Fixes a multi-word/numbered-book URL bug via
  `my_uxlc.book_basename`, e.g. `2Samuel` → `Samuel_2`.)
- **Column order is `text | ref | doc`** (the ref a narrow central spine), not `reference | text | doc`.
- **Three pilot books**, not one.

**Beyond-scope features already pulled in:** Gen 35:22 dual-cantillation strands — near-subtractive
with two loudly-flagged charities (§7.7, `clc_dual_cant`); ketiv/qere boxed-ruby rendering
(`clc_kq`); smart-join of maqaf compounds; the atom/change-log consistency guard; two unit tests
(`clc_dual_cant_test`, `clc_kq_test`).

## Definition of done (skeleton)

A driver `py/main_clc.py` that, for **one pilot book (or chapter)**, reads today's UXLC text and
writes a static page under **`gh-pages/clc/`** in MAM-style **3 columns** (*as built:* `text | ref |
doc`, ref a central spine), where the doc column shows **UXLC's own `<x>` notes** (the under-bar `m`/`d`, plus the transcription-uncertainty `t`) **as always-links**, each carrying the note's prose (*as built:* the tanach.us note
page, downloaded offline — see Status above; the change log is only the consistency guard, and a
not-yet-downloaded page shows a `[note not yet downloaded]` placeholder). **No accent
grammar, no charitable resolution yet** — the skeleton proves the pipeline (read → CLC note schema →
one renderer → `gh-pages/clc/`). Charity layers on later.

## Locked decisions (do not re-litigate)

- **Home:** `py/clc/` (Python) + `gh-pages/clc/` (output). Existing repo modules are importable
  directly (not vendored) — see the design doc §4.
- **Notes policy:** **always link** (uniform; no MAM short-inline / long-link threshold). §7.3.
- **Versification:** primary `vtrad-BHS`. §7.8. (No MAM-boundary coloring in the skeleton.)
- **First note source:** UXLC `<x>` notes, leading with the under-bar-ambiguity codes
  **`m` (prose merkha/meteg/tipexa)** and **`d` (poetic dexi/tarxa/…)**, plus the general transcription-uncertainty catch-all `t` (surfaced, not under-bar). §2, §5, #18.
- **Note schema is defined from requirements (§8), NOT from the `amb_early_mtg` record.**

## Reusable assets (verified on disk)

| need | use |
|---|---|
| read UXLC text | `uxlc_misc/my_uxlc.read(book_id)` → chapters→verses→words; or `my_uxlc.read_all_books(handlers)`. Examples: [py/main_uxlc_word_list.py](../py/main_uxlc_word_list.py), [py/main_fois.py](../py/main_fois.py) |
| extract `<x>` note codes per atom | the FOIs reader pattern — [`_handle_wc_x`](../py/main_fois.py#L54-L59) builds `atom[2]["types"]` |
| note **prose** (the apparatus text) | **as built:** the tanach.us *note page*, downloaded offline by [py/main_clc_download_notes.py](../py/main_clc_download_notes.py) into committed `in/UXLC-notes/` and read by [py/clc/clc_note_pages.py](../py/clc/clc_note_pages.py). The change-log `<correction><description>` ([py/uxlc_changes/](../py/uxlc_changes/), joinable by citation `ch:v.atom`) is now only the **consistency guard**, not the prose. |
| book ids / order / cant-system | `mb_cmn.mb_cmn_bib_locales` (`ALL_BOOK_IDS`), `mb_cmn.cantsys` (prose/poetic), `_is_prose_section_of_job` |
| JSON / file output | `mb_cmn.file_io.json_dump_to_file_path` |
| 3-column presentation model | MAM-with-doc: `MAM-basics/py/mwd/mwd_write_book.py`, `mam_doc_utils.mark_doc_targets`, `mwd_utils.html_for_ver_ndd` (design doc §5). Output examples in `MAM-with-doc/gh-pages/*.html` |
| fonts / css | reuse `gh-pages/woff2/Taamey_D.woff2` + `gh-pages/style.css`; borrow `mam-doc-*` CSS or define `clc-doc-*` |

## Build order

1. **`py/clc/` package + `py/main_clc.py` driver** that reads one pilot book and writes
   `gh-pages/clc/<book>.html`. Get an empty 3-column page rendering first.
2. **CLC note schema** (one dict/dataclass): `book, ch, v, atom, word, note_code, note_text,
   source, diff_type, is_uxlc_departure, uxlc_reading, clc_reading`. Plain data (JSON-serializable)
   so the same records can later feed the §7.9 difference index. (Schema fields per design doc §8.)
3. **Note source = `<x>` notes joined to note prose.** Collect per-atom `<x>` codes
   (`clc_collect.iter_noted_atoms`); for each, read the downloaded tanach.us note page
   (`clc_note_pages.local_note_prose`) to fill `note_text` — *as built*, replacing the original
   change-log-description plan; the change log now only backs the consistency guard, and a not-yet-
   downloaded page shows a `[note not yet downloaded]` placeholder (issue #19), never a fabricated
   substitute. Emit CLC notes for the pilot — the under-bar **`m`/`d`** first, then the transcription-uncertainty **`t`** (surfaced but not under-bar; §2, #18).
   (Skeleton: `is_uxlc_departure=False`, `diff_type='under-bar'` (m/d) or `'transcription-uncertainty'` (t), `clc_reading` = UXLC reading — we
   are only *surfacing* the ambiguity, not yet resolving it.)
4. **Always-link 3-column renderer.** Text column = running verse text; each noted word links to its
   note (anchor / per-note entry). Reference column = book ch:v(.atom).
5. **Pilot scope:** pick a slice that contains at least one `m` and one `d` note so both under-bar
   paths render (e.g. a Psalms chapter for `d` + a Torah chapter for `m`); a whole short book is also
   fine. Leave exact choice to the session.

## Explicitly OUT of scope for the skeleton (later phases)

Accent-grammar integration & actual charitable resolution (§2a/§3/§9 #1); the `q`-dagesh restoration
(§7.15); bracket notes (§7.2); change-records-as-notes beyond the join above (§7.4); images / Sefaria
links (§7.6); MAM-boundary versification color (§7.8); the differences-from-UXLC index (§7.9); the
intro essay (§7.10); BHL Appendix A (§7.11); meteg-position normalization (§7.13); control-char
stripping (§7.14). Each is "a new note source feeding the one renderer" once the skeleton exists.

*(Since pulled in early — no longer out of scope; see Status above: the detangled dual-cant display
for Gen 35:22 (§7.7), and ketiv/qere display, part of FOIs-as-notes (§7.5).)*

## Still-open inputs the session may need to decide

*(All resolved, as built:)*
- ~~Exact pilot book/chapter.~~ → Genesis, Proverbs, 2 Samuel.
- ~~Whether doc links target per-note anchors on a single big-doc page (MAM-style) or a notes page.~~
  → per-note anchors **inline in the same verse row's doc column** (anchor id `clc-{ch}-{v}-{pos}`).
- ~~Final schema field names.~~ → `book, ch, v, atom_index, atom_text, note_code, note_text, source,
  diff_type, is_uxlc_departure, uxlc_reading, clc_reading` (`clc_note.ClcNote`).
