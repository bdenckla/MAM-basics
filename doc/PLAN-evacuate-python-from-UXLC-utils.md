# Evacuate all Python from UXLC-utils into MAM-basics

Written 2026-08-02. Governed by [PLAN-evacuate-python-programme.md](PLAN-evacuate-python-programme.md),
which owns the scope, the order and the decisions shared with the other six repos — **read it
first**, and read `doc/PLAN-evacuate-python-from-wlc-utils.md` §"The organizing idea: `repo_root()`
splits into two roots", which is the whole of the hard part here too.

**This is the first repo of the programme, chosen because it is the cleanest**: one `py/` source
root, zero `sys.path` mutations, byte-identical vendored copies, its own `CLAUDE.md` stating the
conventions, and a `main_0_mega.py` that already serves as the regenerate-everything command. If
the recipe does not transfer here it will not transfer anywhere.

## Status

| Phase | State |
|---|---|
| 1 — two roots, no cwd | **not started** |
| 2 — sibling accessor | **not needed** — see below |
| 3 — copy the Python in (dual residency) | **not started** |
| 4 — empty UXLC-utils | **not started** |
| 5 — repoint codex-index-leningrad's sparse copy | **not started** |
| 6 — flip the provenance breadcrumbs and disambiguate issue citations | **not started** |
| 7 — cross-repo bookkeeping | **not started** |

**Phase 2 of the wlc-utils plan does not recur, for this repo or any other in the programme.**
That phase existed to give `mb_cmn/paths.py` an override chain and a sibling accessor; it has
them. `sibling_repo(name)` and `require_sibling(name, path)` at `py/mb_cmn/paths.py:63` and `:75`
are generic over the sibling's name, so `sibling_repo("UXLC-utils")` works today with nothing
added. Confirm by reading those two functions; do not rebuild them.

---

## Baselines — measured 2026-08-02

| Measure | Command (from the repo root) | Value |
|---|---|---|
| tracked `.py` | `git ls-files "*.py" \| wc -l` | **100** |
| lines | `git ls-files "*.py" -z \| xargs -0 wc -l` | **17,651** |
| tracked `gh-pages` | `git ls-files gh-pages \| wc -l` | **184** |
| tracked `out` | `git ls-files out \| wc -l` | **27** |
| tracked `in` | `git ls-files in \| wc -l` | **556** |
| tracked `data` | `git ls-files data \| wc -l` | **2** |
| test modules | `git ls-files "*_test.py"` | **8**, plus `py/main_test.py` |
| entry points | `git ls-files "py/main_*.py"` | **15** |

The **oracle is the 213 tracked artifacts** — 184 under `gh-pages/`, 27 under `out/` — plus
whatever under `in/` a program writes rather than a download. `in/` is 556 files and mostly the
UXLC-39 XML snapshot, but **do not assume all of `in/` is input**: wlc-utils had a tracked
`in/accgram/uxlc_accent_changes.json` that a program wrote, and it was an extra oracle rather than
a violation. Establish which `in/` files this repo's own programs write **before Phase 1**, and
record the answer here; it is the difference between an oracle of 213 files and one of rather more.

**Capture before starting, and re-capture at each phase**, per `agent-planning-principles.md`
§"Write State Back Before Continuing":

```powershell
.venv\Scripts\python.exe py\main_test.py
```

## What moves, and what is a pure deletion

The 100 files break down as:

| Directory | Files | Disposition |
|---|---|---|
| `py/clc/` | 18 | moves as-is — no name collides with MAM-basics' 41 packages |
| `py/uxlc_misc/` | 11 | moves as-is |
| `py/uxlc_fois/` | 8 | moves as-is |
| `py/uxlc_changes/` | 8 | moves as-is |
| `py/uxlc_amb_early_mtg/` | 7 | moves as-is |
| `py/uxlc_lci/` | 5 | moves as-is |
| `py/repo_hygiene/` | 3 | moves, **but see the note below** |
| `py/main_*.py` | 15 | moves, with two renames — below |
| `py/mb_cmn/` | 21 | **pure deletion** |
| `py/mb_diff_mpu/` | 3 | **pure deletion** |
| `tools/repo_maintenance.py` | 1 | retires — below |

**The 24 vendored files are recorded `identical` in `doc/vendoring-inventory.md`, and that is the
claim to re-confirm rather than trust.** Run `cmp` over `py/mb_cmn` and `py/mb_diff_mpu` against
MAM-basics' `py/mb_cmn` and `py/mb_diff_mpu` immediately before deleting. **If any file now
differs, that difference is a finding to resolve first** — the inventory is regenerated, not live,
and the programme's other five repos show what happens when a copy drifts unwatched. With the 24
gone, **76 files actually move.**

Three name questions, all decided here so no phase has to stop for them:

- **`main_0_mega.py` collides with MAM-basics' own.** UXLC-utils' runs five steps
  (`main_uxlc_check_changes`, `main_fois`, `main_write_page_break_info`, `main_amb_early_mtg`,
  `main_uxlc_word_list`) after refreshing UXLC inputs. It lands as **`main_uxlc_mega.py`**, which
  says whose pipeline it is and does not pretend to be the tree-wide one.
- **`main_test.py` and `main_update_vendored_files.py` disappear.** One merged runner serves the
  whole tree, and a repo with no vendored `mb_*` left has nothing to refresh.
- **`repo_hygiene/` overlaps MAM-basics' `repo_util/` in purpose but not in name**, so it lands
  without collision. Do **not** merge the two in this plan: `repo_hygiene/source_hygiene.py`
  enforces the no-orphan-combining-mark rule that UXLC-utils' pre-commit hook runs, and folding it
  into `repo_util/` is a second change riding along on a move. File it as follow-on work.

**`tools/` retires with the Python.** `tools/README.md` states that nothing under `tools/` may
import repo code — both `repo_maintenance.py` and `tools/git-hooks/pre-commit` only shell out to
`py/main_*.py` entry points. Once those entry points are in MAM-basics, both are broken paths, and
they go the way wlc-utils' `.githooks/pre-commit` went in its Phase 4. **The source-hygiene check
they ran must be re-attached on the MAM-basics side in the same phase**, or a rule that has been
enforced on every commit silently stops being enforced.

## The test runners merge, and this is verified rather than assumed

MAM-basics' `py/main_test.py` is a `pytest.main()` wrapper. UXLC-utils' is a hand-maintained
`TEST_MODULE_SPECS` registry that calls each module's `main()` in-process — with a
`check_registry()` that walks `py/` for `*_test.py` on every run and fails if the registry and the
tree disagree, so this repo does **not** have the silent-drop hazard the global `CLAUDE.md`
describes.

The merge is safe because **the test modules already carry `test_*` functions, not only a
`main()`** — checked on 2026-08-02, `py/clc/clc_kq_test.py` has eight of them alongside its
`main()`. pytest's default `python_files` matches `*_test.py` as well as `test_*.py`, so all eight
modules collect natively and **no test file is rewritten on either side**. Re-confirm this by
collection count, not by reading: `pytest --collect-only` over the moved files must report the
same number of tests that `py\main_test.py` reported in UXLC-utils. A module that collects **zero**
is the silent-green failure the testing policy warns about, and it fails the phase.

`check_registry()` and the registry itself go away with the merge — pytest discovers by walking,
which is what `check_registry()` was compensating for.

---

## Phase 1 — two roots, no cwd

The repo's code addresses its own data by cwd-relative literals, which resolve correctly only
while the process runs from this repo's root. Known offenders, found with
`git grep -nI '"gh-pages/\|"out/\|"in/\|"data/' -- '*.py'`:

- `py/clc/clc_render.py:26` — `_OUT_DIR = "gh-pages/clc"`
- `py/clc/clc_long_note.py:78` — `f"gh-pages/clc/{page_label}-long-notes.html"`
- `py/clc/clc_changes.py:27` — `_CHANGES_DIR = "in/UXLC-misc"`
- `py/clc/clc_note_pages.py:42` — `NOTES_DIR = "in/UXLC-notes"`
- `py/main_clc.py:47` — `f"gh-pages/clc/{label}-notes.json"`
- `py/main_fois.py:102` — `f"gh-pages/fois/features_of_interest-{foi_key}.json"`

**Re-run that grep and work from its output, not from this list** — six is what one grep found,
not a proven total, and the `f`-string forms will not all match a naive search for a leading
quote.

Route every one through an accessor that answers "where is UXLC-utils' data", which after the move
is `sibling_repo("UXLC-utils")` and before it is the repo root. **Do this phase entirely inside
UXLC-utils, while the code still runs there**, so the artifacts are the oracle: regenerate all 213
and require a zero diff. That is the whole point of doing it first rather than during the copy —
a path bug found here is one change away from its cause, and a path bug found in Phase 3 is
indistinguishable from a move bug.

**Verify:** `.venv\Scripts\python.exe py\main_0_mega.py` plus `py\main_clc.py`, then
`git status --porcelain` empty; `py\main_test.py` at its captured baseline.

## Phase 3 — copy the Python in (dual residency)

Land the 76 moving files in MAM-basics with both repos holding a working copy, exactly as
wlc-utils' Phase 3 did. **This phase must complete within a single session**: an interrupted
dual-residency window leaves a tree in which neither repo is authoritative and the oracle cannot
tell you which.

- **3a — land the files** under `py/`, with the renames above.
- **3b — retarget the data root** so the moved code writes into `../UXLC-utils`.
- **3c — fold the tests** into `py/tests/`, and check the collection count.
- **3d — `force_utf8_io()`.** Every `py/main_*.py` here reconfigures stdout/stderr to UTF-8 as the
  first lines of `main()`, per this repo's own `CLAUDE.md`. When a former entry point becomes a
  library module called by another entry point, **that reconfiguration silently disappears** —
  the wlc-utils plan lists this as a standing risk and it is live here, because
  `main_uxlc_mega.py` calls five other mains as modules.
- **3e — the oracle run.** From MAM-basics, regenerate all 213 tracked artifacts into
  `../UXLC-utils` and require `git status --porcelain` empty there **and** in MAM-basics.

**Stop and ask Ben before starting Phase 3.** It is the largest phase and the one whose failure is
expensive to unpick.

## Phase 4 — empty UXLC-utils

Pure subtraction, made safe by Phase 3's dual residency: delete all 100 tracked `.py`, `tools/`,
`py/uxlc_misc/requirements.txt`, and the `py/` tree. **Stop and ask Ben first** — it deletes 100
files.

`CLAUDE.md` keeps only what is about this repo and gains what a reader arriving afterwards has no
other way to learn: that there is no Python here, that the code generating `out/` and `gh-pages/`
is `../MAM-basics/py/`, and which entry point writes what. The MAM-reading conventions, the
vendoring rules, the entry-point rules and the source-hygiene rules move to MAM-basics' `CLAUDE.md`
with the code they govern. **`doc/clc-design.md` stays** — it is a design document about the CLC
edition, not about the code.

**Name the tracked artifacts that no program generates**, the way wlc-utils' Phase 4 named its
111, so that deleting them in the belief they will come back stays a mistake nobody makes twice.

## Phase 5 — repoint codex-index-leningrad's sparse copy

**codex-index-leningrad vendors seventeen of this repo's `.py`** into `UXLC-utils-sparse/py/` —
`main_uxlc_estimate_atom_loc.py`, five `uxlc_lci/` modules and eleven `uxlc_misc/` modules —
refreshed by its own root `main_update_vendored_files.py`, which copies "the designated sparse
subset from `../UXLC-utils`". Phase 4 deletes that source.

**This is not in `doc/vendoring-inventory.md`**, which records only `mb_cmn` rows for
codex-index-leningrad, because the scan looks for MAM-basics packages and these are UXLC-utils
ones. Nothing in either repo's tooling would have told you.

The sparse copy also carries data — `UXLC-utils-sparse/in/UXLC-39/*.xml` and
`UXLC-utils-sparse/data/lci_*.json` — and that half is unaffected, since `in/` and `data/` stay in
UXLC-utils. Only the `py/` half needs a new source. Two candidates, and **this is the phase's one
real decision**:

- **Repoint at `../MAM-basics`**, so the script copies the same modules from their new home.
  Keeps codex-index-leningrad working exactly as now, at the cost of a second repo vendoring from
  MAM-basics by a script MAM-basics does not own.
- **Drop the `py/` half entirely** and have codex-index-leningrad call the MAM-basics entry point
  as a sibling. Fewer copies, but it is a change to how that repo runs, and that repo has its own
  plan in this programme.

**Do not decide this inside the codex-index trio's plan and again here.** Whichever phase reaches
it first decides it and writes the answer into both files.

## Phase 6 — breadcrumbs and issue citations

Flip the `generated by UXLC-utils` provenance breadcrumbs to MAM-basics, in a **dedicated commit
near the end**. Establish the blast radius first:

```powershell
git grep -lI "generated by UXLC-utils" -- out gh-pages in data
```

**The provenance override is load-bearing on ordering.** Do not "fix the now-wrong path" mid-move:
doing so destroys the oracle for every artifact carrying a breadcrumb, which is how the regeneration
stops being able to prove anything. The wlc-utils plan restates this as its first standing risk.

Then prefix the moved code's bare `#NN` issue citations with `UXLC-utils#` where they name a
UXLC-utils issue. That tracker keeps its issues and its numbers; `#56`, cited in `py/main_test.py`
and in `CLAUDE.md`, is one of them.

## Phase 7 — cross-repo bookkeeping

1. `in/vendoring_policy.json` — delete the `UXLC-utils` entry; its `pkg_scan_roots` will name
   directories Phase 4 deleted. **`py/main_vendoring.py --all` raises rather than degrading** when
   a configured scan root is missing, and the wlc-utils plan found that this had broken the
   vendoring audit for a full day with nothing noticing, because neither `main_test.py` nor
   `main_0_mega.py` runs it. Regenerate `doc/vendoring-inventory.md` in the same commit.
2. `all-repos.code-workspace` — leave UXLC-utils listed; it keeps hundreds of tracked non-Python
   files. `in/repo_maintenance_policy.json` needs no change, since UXLC-utils is not frozen.
3. `py/repo_util/run_black.py` and `py/repo_util/check_repo_standards.py` — both already gate on
   whether a repo tracks any `.py`, fixed during wlc-utils' Phase 7. **Confirm on the next sweep
   rather than assuming**, and expect `BLACK_ATTEMPTED=False; Skipped: no tracked .py files in
   this repo`.
4. **Delete this repo's `.venv` and any orphaned agent worktrees once its Python is gone.**
   wlc-utils' Phase 7 found `black .` reformatting 789 `.py` tracked in no index anywhere, all of
   them inside a leftover venv and three stale worktrees. `py\main_repo_util.py --clean-worktrees`
   is the tool that now exists for this.
5. **Grep the other repos for `UXLC-utils/py`.** codex-index-leningrad is the known consumer;
   run the grep anyway, because it is what would have revealed that one.
6. **Outside both repos:** check `C:\Users\BenDe\.claude\skills\` and its tracked copy in
   `github-misc/dot-claude/skills/` for citations of UXLC-utils Python. The `hebrew-prose` skill
   names UXLC-utils among the repos it governs and cites `py/clc/clc_dual_cant.py` for the
   silluq-vs-meteg rule. **The live copy and the tracked copy do not sync automatically — edit
   both.** The wlc-utils plan calls its equivalent item the one most likely to be forgotten,
   because neither repo's tooling can see it. **Stop and ask Ben**, as that plan did: it commits
   to a third repo.
