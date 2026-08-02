# Evacuate all Python from book-of-job into MAM-basics

Written 2026-08-02. Governed by [PLAN-evacuate-python-programme.md](PLAN-evacuate-python-programme.md).
**Fourth in the order**, after UXLC-utils, holman-ketiv-qere and the programme's blocking Phase 0.
This is the largest and least regular repo in the programme, and the only one whose plan opens
with a question rather than a phase.

## Status

| Phase | State |
|---|---|
| D — the quirk-record question | **decided 2026-08-02: all 267 move, records included** |
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

## Decision D — the quirk records move with everything else — DECIDED 2026-08-02

`pyauthor_qr/` holds **160 modules, 3,205 lines**, one per quirk record, each a single dict
literal. `pyauthor_qr/qr_0119.py` in full is `RECORD_0119 = {...}` with ten keys: the verse, the
consensus reading, the proposed Leningrad reading, what is odd about it, a comment, and page and
column coordinates in two manuscripts. So 160 of this repo's 267 `.py` are the content of the Job
review expressed in Python syntax rather than tooling.

**They move as they are, along with the other 107. Ben, 2026-08-02.** This plan's first draft
recommended converting them to JSON instead and called moving them "wrong"; both halves of that
were mistaken, and the record of why is worth keeping, because the same reasoning would misfire
again on `author_rocc` or on any future authored corpus.

- **"Converting is the only option that actually empties the repo" was simply false.** The goal is
  a repo with no Python in it. Moving a `.py` to MAM-basics empties book-of-job of it exactly as
  much as rewriting it into JSON does. Both routes end at **0 tracked `.py`** here; they differ
  only in where the content comes to rest, which is a different question and was being smuggled in
  under the first one.
- **"MAM-basics has no reason to hold authored content" is refuted by MAM-basics itself.** It
  already tracks **91 such modules**: `py/author_misc/` (64, including the bilingual
  paseq-and-legarmeh and gray-maqaf essays), `py/author_rocc/` (23) and `py/mb_author/` (4).
  `author_rocc/` is **one module per section of a review** — structurally the same thing as one
  module per quirk record. Editing authored prose in MAM-basics is not an anomaly to be avoided
  here; it is the established practice, at a scale over half again what book-of-job would add.

**Rejected, and why it stays rejected:** converting the 160 to JSON is a real conversion whose
oracle is that all 701 artifacts regenerate byte-identically. It buys nothing this plan needs —
the repo reaches 0 tracked `.py` without it — and it would land as a content rewrite riding along
inside a move, which is the one thing that makes a move's failures ambiguous. If the records
should become data, that is its own change, on its own oracle, at a time of its own choosing.

**One thing follows from the decision.** `pyauthor_qr/` lands beside the modules it now resembles,
as **`author_qr/`**, matching `author_misc/` and `author_rocc/` rather than keeping a `py`-prefixed
name that means nothing in a tree where everything is under `py/`. The same reading applies to
`pyauthor/` (10 files) and `pyauthor_util/` (33), which become `author_boj/` and `author_boj_util/`
or similar — decide the three names together, in Phase 3, so the review's code and its content
stay legible as one thing.

---

## What moves — all 267, of which 16 are a deletion

| Directory | Files | Disposition |
|---|---|---|
| `pyauthor_qr/` | 160 | moves, **renamed `author_qr/`** — Decision D |
| `pyauthor_util/` | 33 | moves, renamed with the other two `pyauthor*` directories |
| repo root | 16 | **6 are a fork family — programme Phase 0**; the rest move |
| `mb_cmn/` | 16 | **diverged — must be reconciled, not deleted** |
| `py_uxlc_loc/` | 10 | **a second fork family — see below** |
| `pyauthor/` | 10 | moves, renamed with the other two `pyauthor*` directories |
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

251 files land, which makes this the largest single phase in the programme — but **160 of them are
one-dict modules that nothing imports except by name**, so the risk is concentrated in the other
91. Do the three `pyauthor*` renames here, together, having decided the three names first.

Otherwise as in the other plans: land the files, retarget the data root to `../book-of-job`, fold
the one test module in, watch `force_utf8_io()` where an entry point becomes a library module, and
finish with the oracle run from MAM-basics writing into `../book-of-job` with
`git status --porcelain` empty in both.

**Must complete in a single session, and stop and ask Ben first.**

## Phase 4 — empty book-of-job

This deletes all 267 tracked `.py`. **Stop and ask Ben first.**

**The conventions live in ten `.github/copilot-instructions*.md` files, not a `CLAUDE.md`**, and
they are the substance of this phase's documentation work. Read all ten before splitting: they
cover image-crop reproducibility, image metadata, three manuscripts' crop conventions,
quirk-record comment style, and how to open generated HTML. **Under Decision D nearly all of them
follow the code to MAM-basics**, the quirk-record comment conventions included, since the records
go there too. What stays is whatever describes the *published site* rather than how it is made.
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
4. Confirm `run_black.py` and `check_repo_standards.py` skip it once it tracks no `.py`.
5. **Delete its `.venv` and any orphaned agent worktrees.**
6. Grep the other repos for `book-of-job/` paths that name Python rather than pages.
