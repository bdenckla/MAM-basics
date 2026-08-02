# Evacuate all Python from book-of-job into MAM-basics

Written 2026-08-02. Governed by [PLAN-evacuate-python-programme.md](PLAN-evacuate-python-programme.md).
**Fourth in the order**, after UXLC-utils, holman-ketiv-qere and the programme's blocking Phase 0.
This is the largest and least regular repo in the programme, and the only one whose plan opens
with a question rather than a phase.

## Status

| Phase | State |
|---|---|
| **D — the quirk-record decision** | **awaiting Ben — blocks everything below** |
| 0 — reconcile the three fork families | **not started** |
| 1 — two roots, no cwd | **not started** |
| 3 — copy the Python in (dual residency) | **not started** |
| 4 — empty book-of-job | **not started** |
| 6 — breadcrumbs and issue citations | **not started** |
| 7 — cross-repo bookkeeping | **not started** |

## Baselines — measured 2026-08-02

| Measure | Value |
|---|---|
| tracked `.py` | **267** |
| lines | **17,060** |
| tracked `gh-pages` | **694** (`jobn` 531, `jobn-details` 160, plus `index.html`, `style.css`, `woff2`) |
| tracked `out` | **7** JSON |
| test modules | **1** (`test_h_dot_below_nfc.py`, at the repo root) |
| entry points | **5** `main_*.py`, all at the repo root |
| conventions docs | **10** `.github/copilot-instructions*.md` — there is **no** `CLAUDE.md` |

The oracle is the **701 tracked artifacts**. `check_all.py` runs seven checks over them and is the
nearest thing this repo has to a gate; `main_gen_misc_authored_english_documents.py` is the nearest
thing to a regenerate-everything command. **Establish before Phase 1 which of the five entry
points must run, in what order, to rewrite all 701** — that command is the oracle, and this repo
does not currently name it anywhere.

---

## Decision D — 160 of the 267 files are content, not code

`pyauthor_qr/` holds **160 modules, 3,205 lines**, one per quirk record, each a single dict
literal. `pyauthor_qr/qr_0119.py` in full is `RECORD_0119 = {...}` with ten keys: the verse, the
consensus reading, the proposed Leningrad reading, what is odd about it, a comment, and page and
column coordinates in two manuscripts.

**That is the content of the Job review, expressed in Python syntax.** It is not tooling, it is
not shared with anything, and moving it to MAM-basics would move the substance of one project's
scholarship into a repo about a different thing. So "evacuate all Python from book-of-job" cannot
mean what it meant for wlc-utils, and the plan has to say which of three things it means:

- **D1 — convert the 160 to data and leave them here.** Each module is already a JSON-shaped dict,
  and the repo already emits `out/enriched-quirkrecs.json`, so the target format is one this repo
  understands. The code moves to MAM-basics and reads the records from `../book-of-job` as data.
  Outcome: book-of-job becomes a data-and-docs repo like wlc-utils, with **0** tracked `.py`.
  Cost: a real conversion, whose oracle is that all 701 artifacts regenerate byte-identically.
  **This is the recommendation** — it is the only option under which the programme's stated
  outcome is actually reached for this repo.
- **D2 — move all 267, records included.** Literal, cheapest, and wrong: MAM-basics acquires 160
  files it has no reason to hold, and every future edit to a quirk record — an ordinary act of
  authorship — becomes a commit in the tooling repo.
- **D3 — move the 107 code files and leave the 160 records as Python.** Honest about what they
  are, and cheapest to execute correctly. But book-of-job keeps 160 tracked `.py`, so the black
  sweep, `check_repo_standards.py` and the vendoring audit all keep treating it as a Python repo,
  and the maintenance tax this programme exists to reduce is not reduced here.

**Stop and ask Ben. Nothing below can be scoped until this is answered**, because D changes the
file count, the oracle, and whether Phase 4 empties the repo or merely thins it. The phases below
are written for **D1**; under D3, drop the conversion step from Phase 3 and read Phase 4 as
deleting 107 files rather than 267.

---

## What moves — the 107 non-record files

| Directory | Files | Disposition |
|---|---|---|
| `pyauthor_util/` | 33 | moves as-is |
| repo root | 16 | **6 are a fork family — programme Phase 0**; the rest move |
| `mb_cmn/` | 16 | **diverged — must be reconciled, not deleted** |
| `py_uxlc_loc/` | 10 | **a second fork family — see below** |
| `pyauthor/` | 10 | moves as-is |
| `py/` | 7 | moves, **but two names are traps** — see below |
| `py_ac_word_image_helper/` | 6 | **a third fork family — programme Phase 0** |
| `pydiff_mm/` | 5 | moves as-is; distinct from MAM-basics' `mb_diff_mpu` |
| `py_cam1753_word_image/` | 4 | **a fourth fork family — programme Phase 0** |

**Two directory names are traps for anyone reading `git ls-files` by prefix.** `py_ac_loc/` holds
**76 tracked files and zero `.py`** — it is MAM-XML data, despite the `py_` prefix. `py_uxlc_loc/`
holds 40 UXLC XML files *and* 10 `.py`. Do not infer a directory's contents from its name in this
repo.

### The `mb_cmn` copy has diverged

`doc/vendoring-inventory.md` records book-of-job's 16 `mb_cmn` files as **`DIFFERS`**, with
mechanism `unknown` — no copy script has ever refreshed them. **Deleting them the way wlc-utils'
26 were deleted would destroy whatever those differences are.** Diff all 16 against MAM-basics'
originals and classify each difference before Phase 3: a fix that belongs upstream, a local
adaptation that belongs in the moving code, or drift that can simply be dropped. **Write the
classification into this file.** Only after that are they a deletion.

### `py_uxlc_loc/` is a diverged fork of UXLC-utils' Python

Ten modules whose names map one-to-one onto UXLC-utils' `py/uxlc_misc/` and `py/uxlc_lci/`. All
eight with a direct counterpart differ, measured 2026-08-02 with `cmp` and `diff`:

| book-of-job | UXLC-utils counterpart | Differing lines |
|---|---|---|
| `my_uxlc_location.py` | `uxlc_misc/my_uxlc_location.py` | 372 |
| `my_uxlc_lci_rec.py` | `uxlc_lci/uxlc_lci_rec.py` | 308 |
| `my_uxlc_lci_augrec.py` | `uxlc_lci/uxlc_lci_augrec.py` | 302 |
| `my_uxlc.py` | `uxlc_misc/my_uxlc.py` | 240 |
| `my_uxlc_bibdist.py` | `uxlc_misc/my_uxlc_bibdist.py` | 185 |
| `my_uxlc_page_break_info.py` | `uxlc_misc/my_uxlc_page_break_info.py` | 162 |
| `my_uxlc_cvp.py` | `uxlc_misc/my_uxlc_cvp.py` | 116 |
| `my_uxlc_verlen.py` | `uxlc_lci/uxlc_lci_verlen.py` | 14 |

**None of this is in `doc/vendoring-inventory.md`**, which records only `mb_cmn` rows for
book-of-job — the scan looks for MAM-basics packages, and these are UXLC-utils ones. It is the
same blind spot that hides codex-index-leningrad's `UXLC-utils-sparse/py/`, and it means **the
UXLC location code exists in three public repos**: UXLC-utils, codex-index-leningrad and here.

**Do not assume these are stale copies of UXLC-utils' files.** At 372 differing lines the more
likely reading is independent evolution on both sides, in which case they are two tools with a
common ancestor and both belong in MAM-basics under distinct names. Classify before deciding, and
**decide it in coordination with UXLC-utils' Phase 5**, which faces the same question for
codex-index-leningrad's copy. Whichever plan reaches the question first answers it and writes the
answer into both files.

### Two names in `py/` collide by meaning, not by path

`py/hebrew_letter_words.py` and `py/uni_heb_char_classes.py` would land as **top-level** modules in
MAM-basics' `py/`, where `mb_misc/hebrew_letter_words.py` already exists. A top-level
`hebrew_letter_words` alongside `mb_misc.hebrew_letter_words` is two module objects for one name —
two copies of every module-level constant, and a class from one failing `isinstance` against the
other. The global `CLAUDE.md` describes this as the cost of a `sys.path` insert; here it is reached
with no `sys.path` line at all, purely by landing a root-level module.

**Land the seven `py/` files as a package**, `boj_render/` or similar, matching the `wlc_cmn/` and
`hkq_cmn/` precedents. Four of the seven already carry a `boj_` prefix, so the package name is the
one the repo was already reaching for.

---

## Phase 1 — two roots, no cwd

This repo's Python runs with the **repo root** as `sys.path[0]`, not a `py/`, and addresses its
data by cwd-relative literals. Known offenders from
`git grep -nI '"gh-pages/\|"out/\|f"gh-pages/' -- '*.py'`:

- `main_gen_misc_authored_english_documents.py:28,31,34,49` — `"gh-pages/jobn"`,
  `f"gh-pages/{D1D_DIR}"`, `"gh-pages/index.html"`
- `pyauthor/job1_full_list_details.py:15` — `out_dir = f"gh-pages/{D1D_DIR}"`
- `test_h_dot_below_nfc.py:78` — `"out/"`

**Re-run the grep.** Several files use `Path(__file__)` already (`check_escape_sequences.py`,
`check_mark_order.py`, `check_spelling_in_html.py`, `fix_escape_sequences.py`,
`fix_mark_order.py`), so the repo is not uniformly cwd-bound and the fix is not uniform either.

**Ignore the `"../"` hits.** `git grep '\.\./'` returns a dozen matches in this repo that are all
**HTML hrefs** — `f"../jobn-details/{sid}.html"`, `"../jobn/style.css"` — relative links inside
generated pages, not filesystem paths. Rewriting one as a filesystem path breaks the published
site silently, since the artifacts still regenerate and only a browser notices.

Do this phase inside book-of-job, and prove it by regenerating all 701 artifacts to a zero diff.

## Phase 3 — copy the Python in (dual residency)

Under **D1** this phase carries the record conversion, which makes it the largest single phase in
the programme. Consider splitting it: **3-record** (convert `pyauthor_qr/` to data and prove the
701 artifacts unchanged, entirely inside book-of-job) then **3-code** (the move proper). Two
provable steps beat one step whose failure has two candidate causes.

Otherwise as in the other plans: land the files, retarget the data root to `../book-of-job`, fold
the one test module in, watch `force_utf8_io()` where an entry point becomes a library module, and
finish with the oracle run from MAM-basics writing into `../book-of-job` with
`git status --porcelain` empty in both.

**Must complete in a single session, and stop and ask Ben first.**

## Phase 4 — empty book-of-job

Under D1 this deletes 267 tracked `.py`. **Stop and ask Ben first.**

**The conventions live in ten `.github/copilot-instructions*.md` files, not a `CLAUDE.md`**, and
they are the substance of this phase's documentation work. Read all ten before splitting: they
cover image-crop reproducibility, image metadata, three manuscripts' crop conventions,
quirk-record comment style, and how to open generated HTML. Roughly, the crop and image ones
follow the code to MAM-basics; the quirk-record ones stay, because under D1 the records stay.
**Write a `CLAUDE.md` here in the same phase**, stating that there is no Python left, that the code
generating `gh-pages/` and `out/` is `../MAM-basics/py/`, and which entry point writes what. The
README is two lines and needs replacing outright.

**Name the tracked artifacts that no program generates**, as wlc-utils' Phase 4 named its 111.
With 694 files under `gh-pages/` this is not optional bookkeeping: it is the only thing standing
between a future session and deleting hand-made pages in the belief they will come back.

## Phase 6 — breadcrumbs and issue citations

```powershell
git grep -lI "generated by book-of-job" -- gh-pages out
```

Flip in a dedicated commit near the end; do not fix the now-wrong path mid-move.

## Phase 7 — cross-repo bookkeeping

1. `in/vendoring_policy.json` — delete the `book-of-job` entry, then regenerate
   `doc/vendoring-inventory.md`. `py/main_vendoring.py --all` **raises** on a missing scan root.
2. **UXLC-utils names this repo in its own code**: `py/main_map_changes_to_book_of_job.py:165`
   carries `"html_base": "../book-of-job/gh-pages/jobn-details/"`. That is a published-URL base
   rather than a source path, so it survives the move — **but it survives only if the site keeps
   its shape**, which is a reason not to reorganize `gh-pages/` in the same programme.
3. `all-repos.code-workspace` — leave book-of-job listed.
4. Confirm `run_black.py` and `check_repo_standards.py` skip it once it tracks no `.py` — under
   D3 they will not, and should not.
5. **Delete its `.venv` and any orphaned agent worktrees.**
6. Grep the other repos for `book-of-job/` paths that name Python rather than pages.
