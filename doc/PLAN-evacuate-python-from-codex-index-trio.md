# Evacuate all Python from codex-index-aleppo, -leningrad and -cam1753 into MAM-basics

Written 2026-08-02. Governed by [PLAN-evacuate-python-programme.md](PLAN-evacuate-python-programme.md).
**Last in the order.** One plan for three repos, because they share a shape, share two fork
families, and share a vendoring problem — doing them separately would answer the same question
three times and risk answering it three different ways.

## Status

| Phase | State |
|---|---|
| **D — is this worth doing for cam1753?** | **awaiting Ben** |
| 0 — reconcile the fork families (programme Phase 0, plus the wiki family below) | **not started** |
| 1 — two roots, no cwd (per repo) | **not started** |
| 3 — copy the Python in (per repo, dual residency) | **not started** |
| 4 — empty each repo | **not started** |
| 6 — breadcrumbs and issue citations | **not started** |
| 7 — cross-repo bookkeeping | **not started** |

## Baselines — measured 2026-08-02

| | codex-index-aleppo | codex-index-leningrad | codex-index-cam1753 |
|---|---|---|---|
| tracked `.py` | 44 | 38 | 22 |
| lines | 8,223 | 4,358 | 5,386 |
| tracked total | 223 | 88 | 172 |
| last commit | **2026-08-02** | 2026-07-27 | **2026-04-27** |
| Pages workflow | `pages.yml` | none | none |
| vendored `mb_cmn` | 4 in `py/mb_cmn/` + 4 in `aleppo-wiki/py/`, **DIFFERS** | 4 in `lenin-wiki/py/`, **DIFFERS** | 3 in `mb_cmn/`, 2 identical + `str_defs.py` **DIFFERS** |
| oracle | `line-breaks` 35, `column-coordinates` 35, `aleppo-wiki` 26, `MAM-XML` 24, `ds-flat-stream` 8, `gh-pages` 4 | `lenin-wiki` 21 | `cam1753-col-quads` 28, `cam1753-line-breaks` 27, `cam1753-spread-splits-doc` 15, `MAM-XML` 24 |

`aleppo-pages` (37), `cam1753-pages` (28) and `cam1753-spreads` (14) are downloaded scans, not
generated artifacts — they are inputs to the oracle, not part of it. Confirm that reading against
each repo's `download_*.py` before relying on it.

---

## Decision D — cam1753, and how much of this is worth doing

codex-index-cam1753 has not been committed to since **2026-04-27**, has no Pages workflow, and
holds 22 `.py` of which 3 are vendored. codex-index-leningrad last moved 2026-07-27 and also has
no Pages workflow. Only codex-index-aleppo is unambiguously live.

The programme exists to reduce the tax of maintaining Python across repos. A dormant repo levies
that tax only when a sweep touches it — which is real (the black sweep, `check_repo_standards.py`
and the vendoring audit all visit it) but small. **Against that, the fork families below are a
genuine liability that does not care whether a repo is dormant**: three drifted copies of one
script are three chances to fix a bug once and leave it broken twice, and the dormant copy is the
one that stays broken.

So the recommendation is: **do Phase 0 for all three regardless — it is the part that pays — and
then decide per repo whether the move itself is worth it.** Reconciling the forks is worth doing
even if not one line ever moves to MAM-basics.

**Stop and ask Ben.** The phases below are written for all three moving.

---

## The fork families

Two families span these three repos and book-of-job. **Programme Phase 0 owns the first and is
blocking; this plan owns the second.**

### Family 1 — the `check_*`/`fix_*` scripts (programme Phase 0)

Six scripts held by book-of-job, codex-index-aleppo and codex-index-cam1753, of which exactly one
pair is still identical. The table is in the programme file; do not re-derive it here.
`py_ac_word_image_helper/` (6 files, book-of-job and codex-index-aleppo, 2 differing) and
`py_cam1753_word_image/` (4 files, book-of-job and codex-index-cam1753, **all 4 differing**) are
part of the same phase.

### Family 2 — the wikisource page generators

`codex-index-aleppo/aleppo-wiki/` and `codex-index-leningrad/lenin-wiki/` are two builds of the
same thing — a Wikisource page for a manuscript index — and share eight module names. Measured
2026-08-02 with `cmp` and `diff`:

| Module | Result |
|---|---|
| `main_make_wikisource_page.py` | differs, 50 lines |
| `py/mam_book_names.py` | differs, 230 lines |
| `py/write_wikitext_file.py` | differs, 139 lines |
| `py/my_open.py` | **identical** |
| `py/hebrew_letters.py` | differs, 2 lines |
| `py/my_utils.py` | differs, 2 lines |
| `py/hebrew_punctuation.py` | **identical** |
| `py/hebrew_verse_numerals.py` | **identical** |

The last four are the diverged `mb_cmn` copies the vendoring inventory already flags — and the
shape of their divergence is informative: **they are nearly identical to each other and both
drifted from MAM-basics**, which reads as one ancestor copied twice while MAM-basics moved on.
That makes them the cheapest reconciliation in the whole programme: diff each against MAM-basics'
current `py/mb_cmn/`, decide whether the 2-line deltas are fixes worth keeping, and then they are
a plain deletion in both repos.

The first three are the real work. `mam_book_names.py` at 230 differing lines is not drift —
Aleppo and Leningrad have genuinely different book divisions and page conventions, and the honest
outcome may be **one parameterized module plus two data tables** rather than one merged file.
Classify before merging, and if the answer is that they are two tools, say so and land them under
two names.

**leningrad's `lenin-wiki/py/` has nine modules aleppo has no counterpart for** —
`vtrad_data.py`, `vtrad_helpers.py`, `masorah_finalis_lines.py`, `image_urls.py`,
`get_cvm_rec_from_bcvt.py`, `my_locales.py`, `read_json_file.py`, `s1_collapse_rows.py`,
`s2_group_by_book.py` — and aleppo has `group_by_book.py`, `book_names.py` and `read_csv_file.py`
against leningrad's `s2_group_by_book.py` and `read_json_file.py`. Those pairs are the same job
against different input formats. They are part of the same classification.

---

## The third UXLC fork, and why this plan does not decide it

`codex-index-leningrad/UXLC-utils-sparse/py/` holds **17 of UXLC-utils' own `.py`** —
`main_uxlc_estimate_atom_loc.py`, five `uxlc_lci/` modules and eleven `uxlc_misc/` modules —
refreshed from `../UXLC-utils` by codex-index-leningrad's root `main_update_vendored_files.py`.
The data half of that sparse copy (`in/UXLC-39/*.xml`, `data/lci_*.json`, 42 files) is unaffected,
since `in/` and `data/` stay in UXLC-utils.

**This is decided in [PLAN-evacuate-python-from-UXLC-utils.md](PLAN-evacuate-python-from-UXLC-utils.md)
Phase 5, which runs first**, and book-of-job's `py_uxlc_loc/` is a third instance of the same
question. Whichever plan reaches it first writes the answer into all three files. Do not decide it
here and discover later that UXLC-utils decided it differently.

---

## Phase 1 — two roots, no cwd

Per repo, and each proved by regenerating that repo's own artifacts to a zero diff before anything
moves.

Known offenders:

- codex-index-aleppo `aleppo-wiki/py/mam_book_names.py:114` — `f"in/mam-ws/{basename}.json"`
- codex-index-aleppo `py/tests/test_h_dot_below_nfc.py:77` — `"gh-pages/"`

**Re-run `git grep -nI '"gh-pages/\|"out/\|"in/\|"MAM-XML/\|"line-breaks/\|"column-coordinates/'`
per repo** — these repos put their artifacts in top-level directories named after the artifact
rather than in an `out/`, so the usual grep misses most of them. That is the single most likely
way to leave a path bug behind in this plan.

**Ignore the `"../aleppo-pages/{page_id}.jpg"` hits** in `py/py_ac_loc/gen_line_break_editor.py:37`
and `py/py_ac_word_image_helper/codex_page.py:34`: those are `src` attributes in generated HTML,
not filesystem paths, and rewriting one breaks the published editor silently.

## Phase 3 — copy the Python in (dual residency)

Per repo, one at a time, each within a single session. Name collisions to settle first:

| Name | Held by | Resolution |
|---|---|---|
| `main_make_wikisource_page.py` | aleppo **and** leningrad | falls out of Family 2's classification |
| `main_update_vendored_files.py` | leningrad (and UXLC-utils, holman-ketiv-qere) | disappears |
| `vendoring_sync.py` | leningrad root — a **vendored `mb_cmn` module** sitting outside `mb_cmn/` | resolve with the rest of that repo's `mb_cmn` |
| `check_*`/`fix_*` × 6 | aleppo and cam1753 | one reconciled copy, from Phase 0 |
| `py_cam1753_word_image/`, `py_ac_word_image_helper/` | shared with book-of-job | one reconciled copy each, from Phase 0 |
| `py_mam_xml/` (cam1753) | — | check against MAM-basics' `mb_xml` before landing |

cam1753's Python is **14 files at the repo root**, so it lands at MAM-basics' `py/` top level and
carries the same two-module-objects hazard book-of-job's `py/` does. Land it as a package.

Retarget each repo's data root to `sibling_repo("codex-index-<x>")`; watch `force_utf8_io()` where
an entry point becomes a library module; finish with the oracle run from MAM-basics and
`git status --porcelain` empty in both repos.

**Stop and ask Ben before the first Phase 3 of the three.**

## Phase 4 — empty each repo

**None of the three has a `CLAUDE.md`** — codex-index-aleppo does, the other two do not.
Whichever the repo, write or update one in this phase saying that there is no Python left, that
the code is `../MAM-basics/py/`, and which entry point writes what. **Name the tracked artifacts
no program generates**, which for these repos includes the downloaded scans.

**Stop and ask Ben before each.**

## Phase 6 — breadcrumbs and issue citations

```powershell
git grep -lI "generated by codex-index" -- .
```

Per repo, in a dedicated commit near the end, and not mid-move.

## Phase 7 — cross-repo bookkeeping

1. `in/vendoring_policy.json` — delete all three entries **and the eight `overrides` rows** naming
   `codex-index-aleppo` and `codex-index-leningrad` paths. Then regenerate
   `doc/vendoring-inventory.md`. `py/main_vendoring.py --all` **raises** on a missing scan root
   rather than degrading, so a half-done edit breaks the audit rather than producing a stale one.
2. The inventory's own comment on `codex-index-leningrad` — that the copy script the provenance
   scan finds there refreshes `UXLC-utils-sparse` from UXLC-utils and never touches `lenin-wiki/py/`
   — becomes obsolete when that script goes. **Delete the comment with the script**, or it will be
   read later as describing something that still exists.
3. `all-repos.code-workspace` — leave all three listed; each keeps its tracked non-Python files.
4. Confirm `run_black.py` and `check_repo_standards.py` skip each once it tracks no `.py`.
5. **Delete each repo's `.venv` and any orphaned agent worktrees.**
6. Grep the other repos for `codex-index-*/py` paths. book-of-job is the known consumer of the two
   word-image helpers; run the grep anyway.
