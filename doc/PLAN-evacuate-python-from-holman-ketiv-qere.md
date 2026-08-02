# Evacuate all Python from holman-ketiv-qere into MAM-basics

Written 2026-08-02. Governed by [PLAN-evacuate-python-programme.md](PLAN-evacuate-python-programme.md).
**Second in the order**, after UXLC-utils: the same shape, smaller, and its job is to confirm the
recipe on a second repo before the expensive ones. Read
[PLAN-evacuate-python-from-UXLC-utils.md](PLAN-evacuate-python-from-UXLC-utils.md) alongside this —
where the two agree, that file carries the reasoning and this one does not repeat it.

## Status

| Phase | State |
|---|---|
| 1 — two roots, no cwd | **not started** |
| 3 — copy the Python in (dual residency) | **not started** |
| 4 — empty holman-ketiv-qere | **not started** |
| 6 — breadcrumbs and issue citations | **not started** |
| 7 — cross-repo bookkeeping | **not started** |

Phase 2 does not recur — `mb_cmn/paths.py` already has `sibling_repo()` and `require_sibling()`.
Phase 5 has no analogue here: nothing vendors this repo's Python.

## Baselines — measured 2026-08-02

| Measure | Value |
|---|---|
| tracked `.py` | **68** |
| lines | **11,159** |
| tracked `gh-pages` | **161** |
| tracked `out` | **2** |
| test modules under `py/tests/` | **8**, plus `py/main_test.py` |
| entry points | **6** `py/main_*.py` |

The oracle is the **163 tracked artifacts**. The README fixes the scope in a way that makes the
oracle unusually sharp: exactly **77 rows** are expected in `docs-not-served/table_data.json`, and
the dataset is not expected to grow. A regeneration that changes the row count is a failure, not a
finding.

The regenerate-everything command is the README's own:

```powershell
.venv\Scripts\python.exe py/main_extract_docx_and_render_table.py
```

## What moves, and what is a pure deletion

| Directory | Files | Disposition |
|---|---|---|
| `py/py_render/` | 14 | moves as-is — no collision with MAM-basics' `render_wt` |
| `py/python_modules/` | 14 | moves, **renamed** — below |
| `py/tests/` | 8 | folds into MAM-basics' `py/tests/` |
| `py/main_*.py` | 6 | moves, less two that disappear |
| `py/mb_cmn/` | 17 | **pure deletion** |
| `py/mb_diff_mpu/` | 9 | **pure deletion** |

The 26 vendored files are recorded `identical` / `copy_script` / **`active`** in
`doc/vendoring-inventory.md` — the only repo in the whole programme whose copies the inventory
calls active rather than stale. **Re-confirm with `cmp` immediately before deleting anyway.** With
them gone, **42 files actually move**.

- **`python_modules/` is a bad name to import into a shared tree** — it says nothing about what is
  inside, and it is a name a second repo already uses (mgketer's `py/python_modules/`, which is
  private and out of scope but will not stay out of the way forever). Land it as **`hkq_cmn/`**,
  matching the `wlc_cmn/` precedent from the wlc-utils move.
- **`main_test.py` and `main_update_vendored_files.py` disappear**, for the reasons UXLC-utils'
  plan gives.
- The other four entry points — `main_extract_docx_and_render_table`, `main_just_render_table`,
  `main_search_final_hiriq_verse_text`, `main_search_holam_he_qere` — collide with nothing and
  move under their own names.

## The test merge is free, and the registry gap is already closed

The 8 test modules are `unittest.TestCase`, which pytest collects natively, so **no test file is
rewritten on either side** — the same reasoning that let MAM-basics' own `main_test.py` become a
`pytest.main()` wrapper.

The global `CLAUDE.md` records that on 2026-07-30 this repo had **2 of 8** test files missing from
its hand-maintained `TEST_MODULE_SPECS`, reporting nothing at all rather than skipping visibly.
**That gap is closed**: checked 2026-08-02, all eight `module_name=` entries match the eight files
under `py/tests/` exactly. So the merge inherits no silently-dead tests — but **re-check before
Phase 3**, because a registry with no automatic cross-check can reopen the gap at any time, and
this one has no `check_registry()` walk of the kind UXLC-utils added.

Confirm the merge by **collection count**, not by reading: a module that collects zero tests is
the silent-green failure the testing policy warns about, and it fails the phase.

## Phase 1 — two roots, no cwd

Known cwd-relative repo-internal literals, from
`git grep -nI '"gh-pages/\|"out/\|"in/\|"docs-not-served/' -- '*.py'`:

- `py/main_just_render_table.py:20` — `default=Path("gh-pages/table_data_findings.html")`
- `py/python_modules/extract_docx_xml_utils.py:22-24` — `"gh-pages/img/row0NN_aleppo_01.png"`
- `py/tests/test_h_dot_below_nfc.py:72-73` — `"out/"`, `"gh-pages/"`

**Re-run the grep and work from its output**, including `docs-not-served/`, which the README shows
is a tracked data directory this repo's own scripts read and write and which the other repos in
the programme have no analogue of.

Route each through an accessor answering "where is holman-ketiv-qere's data" — the repo root
before the move, `sibling_repo("holman-ketiv-qere")` after. **Do this phase inside
holman-ketiv-qere, while the code still runs there**, and prove it by regenerating the 163
artifacts to a zero diff.

## Phase 3 — copy the Python in (dual residency)

The 42 moving files land under `py/`, with `python_modules/` → `hkq_cmn/` and the two
disappearing entry points. Retarget the data root to `../holman-ketiv-qere`; fold the tests;
watch `force_utf8_io()` where a former entry point becomes a library module. **Must complete in a
single session**, and **stop and ask Ben first**.

The oracle run is `main_extract_docx_and_render_table` from MAM-basics, writing into
`../holman-ketiv-qere`, then `git status --porcelain` empty in both repos — and the row count
still 77.

**One thing to check that the other plans do not have:** `py/python_modules/table_row_github_issues.py`
and `refresh_table_row_github_issues.py` reach GitHub. Establish which repo's issue tracker they
name before the move, and whether they authenticate through anything that assumes the process's
working directory. A tool that silently starts reading the wrong tracker is a failure the artifact
oracle cannot see.

## Phase 4 — empty holman-ketiv-qere

Delete all 68 tracked `.py` and the `py/` tree. **Stop and ask Ben first.**

**This repo has no tracked `CLAUDE.md`**, so unlike UXLC-utils there is no conventions file to
split — but that cuts the wrong way: a reader arriving afterwards has *nothing* telling them where
the code went. **Write one in this phase**, saying that there is no Python here, that the code
generating `gh-pages/`, `out/` and `docs-not-served/` is `../MAM-basics/py/`, which entry point
writes what, and that the 77-row expectation is a fixed scope rather than a current count. The
README already carries the workflow commands and must be updated in the same commit, since every
one of them names a path this phase deletes.

## Phase 6 — breadcrumbs and issue citations

```powershell
git grep -lI "generated by holman-ketiv-qere" -- gh-pages out docs-not-served
```

Flip them in a **dedicated commit near the end**, and do not "fix the now-wrong path" mid-move —
that destroys the oracle for every artifact carrying a breadcrumb.

Then prefix the moved code's bare `#NN` with `holman-ketiv-qere#`. Note that this repo's Python
already *renders* issue references into its table, via `rt_issue_tags.py` and
`table_row_github_issues.py`: **those are data about the Holman review, not citations of this
repo's own tracker, and must not be rewritten.** Distinguish the two before touching either.

## Phase 7 — cross-repo bookkeeping

1. `in/vendoring_policy.json` — delete the `holman-ketiv-qere` entry, whose `pkg_scan_roots` names
   `py/mb_cmn` and `py/mb_diff_mpu`; `py/main_vendoring.py --all` **raises** on a missing scan root
   rather than degrading. Regenerate `doc/vendoring-inventory.md` in the same commit. This repo is
   two of the inventory's 19 rows.
2. `all-repos.code-workspace` — leave it listed; it keeps its tracked non-Python files.
3. Confirm `run_black.py` and `check_repo_standards.py` skip it cleanly on the next sweep.
4. **Delete its `.venv` and any orphaned agent worktrees**, per the 789-stray-file finding in the
   wlc-utils plan's Phase 7.
5. Grep the other repos for `holman-ketiv-qere/py`.
