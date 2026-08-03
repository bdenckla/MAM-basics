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
| 1 — two roots, no cwd | **done** 2026-08-02, commit `fe73d07` in UXLC-utils; plus `d5a5052` here |
| 2 — sibling accessor | **not needed as its own phase**, but not free either — the one piece owed here was done inside Phase 1; see below |
| 3 — copy the Python in (dual residency) | **done** 2026-08-02, commits `662db55` and `f202d21` here; nothing in UXLC-utils, which is what dual residency means |
| 4 — empty UXLC-utils | **not started** |
| 5 — repoint codex-index-leningrad's sparse copy | **not started** |
| 6 — flip the provenance breadcrumbs and disambiguate issue citations | **not started** |
| 7 — cross-repo bookkeeping | **not started** |

**Phase 2 of the wlc-utils plan does not recur, for this repo or any other in the programme.**
That phase existed to give `mb_cmn/paths.py` an override chain and a sibling accessor; it has
them. `sibling_repo(name)` and `require_sibling(name, path)` at `py/mb_cmn/paths.py:63` and `:75`
are generic over the sibling's name, so `sibling_repo("UXLC-utils")` works today with nothing
added. Confirm by reading those two functions; do not rebuild them.

**But "MAM-basics has it" is not the same as "the repo being evacuated can reach it," and Phase 1
found the difference.** UXLC-utils vendored 21 `mb_cmn` files and `paths.py` was not among them,
so the accessor existed nowhere its code could import it. Vendoring it in was the fix (see Phase
1's write-up). **Check each remaining repo's own `py/mb_cmn/` for `paths.py` before assuming this
row costs nothing**; four of the five have `unknown`-mechanism, `DIFFERS` copies, where dropping a
file in is not enough because nothing refreshes them.

---

## Baselines — measured 2026-08-02

| Measure | Command (from the repo root) | Value |
|---|---|---|
| tracked `.py` | `git ls-files "*.py" \| wc -l` | **100** (**102** after Phase 1) |
| lines | `git ls-files "*.py" -z \| xargs -0 wc -l` | **17,651** (**17,932** after Phase 1) |
| tracked `gh-pages` | `git ls-files gh-pages \| wc -l` | **184** |
| tracked `out` | `git ls-files out \| wc -l` | **27** |
| tracked `in` | `git ls-files in \| wc -l` | **556** |
| tracked `data` | `git ls-files data \| wc -l` | **2** |
| test modules | `git ls-files "*_test.py"` | **8**, plus `py/main_test.py` |
| entry points | `git ls-files "py/main_*.py"` | **15** |

**The oracle is 214 tracked artifacts** — not the 213 this table first said, and not the 216
Phase 1 replaced it with. **214 is measured, and it is what the four components below have summed
to all along**; 216 was an arithmetic slip in Phase 1's write-up, corrected in Phase 3. Phase 1
was right about *which* trees count, and wrong twice over about the total:

- **`data/`'s two files are generated and the table above did not count them.**
  `main_write_page_break_info.py` writes `data/lci_augrecs.json` and copies
  `in/UXLC-misc/lci_recs.json` to `data/lci_recs.json`. The name misleads; both are output.
- **Exactly one tracked file under `in/` is written by this repo's own programs from local
  inputs**: `in/UXLC-misc/2026.04.01-map-to-book-of-job.json`, by
  `main_map_changes_to_book_of_job.py`, which reads book-of-job's `out/enriched-quirkrecs.json`
  and `gh-pages/jobn-details/`. It is the exact analogue of wlc-utils'
  `in/accgram/uxlc_accent_changes.json`, and it does regenerate byte-identically.

So `in/` adds **1**, not 555. The other 555 are **downloaded** — `in/UXLC-39` (39) and
`in/UXLC-rest` (7) extracted from tanach.us' `Tanach.xml.zip`, the 19 `in/UXLC-misc/*.xml` change
logs, and `in/UXLC-notes` (477) — or **hand-curated**: `BHL Appendix A Psalms.csv`, the four
Holman JSON/TXT, the four `LC ...csv`, the three `LCIndex.*`, `lci_recs.json`, and the two
`in/UXLC-misc-fixed/` overrides. A download is not a regeneration, so none of them is an oracle:
re-running the downloaders proves the network works, not that the code does.

**Which makes the artifact table above the oracle: 184 `gh-pages/` + 27 `out/` + 2 `data/` +
1 `in/` = 214.**

**But only 127 of the 214 are regenerated at all** — measured in Phase 3 by snapshotting mtimes
across the four trees immediately before a full run. The other **87** are 86 static assets (81
`gh-pages/amb-early-mtg/img/`, 2 `gh-pages/img/`, `gh-pages/index.html`, `gh-pages/style.css`,
`gh-pages/woff2/Taamey_D.woff2`) plus `out/UXLC-misc/map-changes-to-book-of-job.md`, a
hand-authored prose report that happens to live under `out/`. An empty `git status` across all
214 is therefore 127 files proven byte-identical and 87 proven untouched, which is a weaker claim
than "216 regenerated" and the honest one. **The 87 are what Phase 4 must name.**

**Capture before starting, and re-capture at each phase**, per `agent-planning-principles.md`
§"Write State Back Before Continuing":

```powershell
.venv\Scripts\python.exe py\main_test.py
```

## What moves, and what is a pure deletion

**Phase 1 added two files, so the count is 102, not 100** — `py/uxlc_paths.py` and a vendored
`py/mb_cmn/paths.py`. They break down as:

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
| `py/uxlc_paths.py` | 1 | moves; its `uxlc_data_root()` is Phase 3b's one-line retarget |
| `py/mb_cmn/` | 22 | **21 pure deletions, plus one that is not vendored at all — see below** |
| `py/mb_diff_mpu/` | 3 | **pure deletion** |
| `tools/repo_maintenance.py` | 1 | retires — below |

**The vendored files are recorded `identical` in `doc/vendoring-inventory.md`, and that is the
claim to re-confirm rather than trust.** Phase 3 ran `cmp` over `py/mb_cmn` and `py/mb_diff_mpu`
against MAM-basics' own immediately before the copy: **24 identical, and one file with no
counterpart here at all.** Do it again before Phase 4 deletes them — the inventory is
regenerated, not live, and the programme's other five repos show what happens when a copy drifts
unwatched.

**The odd file is `py/mb_cmn/mb_cmn_bib_locales.py`, and it is UXLC-local code wearing a vendored
directory's name.** It is MAM-basics' `bib_locales.py` plus six back-compat aliases for prior
UXLC-local naming; it is absent from the inventory's 21-file `mb_cmn` row; and
`main_update_vendored_files.py` excludes it from the sync by name. Phase 3 did **not** copy it —
its ten importers now use `mb_cmn.bib_locales` directly, with the three aliases that had callers
spelled out. Phase 4 still deletes it, but as UXLC-local code rather than as a vendored copy, and
the inventory row stays at 21.

**76 files move, and 74 land.** The rows above sum to 76 (18+11+8+8+7+5+3+15+1); this line
previously said 77, which counted `tools/repo_maintenance.py` as moving when the same table says
it retires. Two of the 15 entry points then disappear by design (below), so 73 new files landed
in Phase 3, plus one test module that merged into an existing file rather than arriving as its
own.

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

## Phase 1 — two roots, no cwd — DONE 2026-08-02

**Landed as `fe73d07` in UXLC-utils (31 files, +401/−119) and `d5a5052` here.** Every baseline in
the table above was re-measured first and every one matched: 100 tracked `.py` (102 after the
commit adds `py/uxlc_paths.py` and the vendored `py/mb_cmn/paths.py`), 184 `gh-pages/`, 27 `out/`,
556 `in/`, 2 `data/`, 15 entry points, 8 test modules plus the runner. `py/main_test.py` reported
**8/8 modules passed** before and after, from the repo root and from a foreign cwd alike.

**The verification ran as specified and passed.** From `C:\Users\BenDe\GitRepos\MAM-basics` as the
working directory, each entry point by absolute path, individually: `main_uxlc_check_changes`,
`main_fois`, `main_write_page_break_info`, `main_amb_early_mtg`, `main_uxlc_word_list`,
`main_clc`, `main_map_changes_to_book_of_job`, and `main_test`. Afterwards
`git status --porcelain` was **empty in MAM-basics** and, apart from the `.py` files themselves,
**empty in UXLC-utils** — all 216 artifacts came back byte-identical from a foreign cwd, and
their mtimes confirm they were actually rewritten rather than skipped.

Eight things went differently from what is written underneath. The first three bear on later
phases:

- **`main_0_mega.py` does NOT mask cwd bugs here, unlike wlc-utils'.** wlc-utils' mega passed
  `cwd=repo_root` to each child *process*, so its Phase 1 had to bypass it or verify nothing.
  UXLC-utils' imports its five steps as modules and calls `mod.main()` in-process, inheriting
  whatever cwd it was given. Running the steps individually was still the right proof, but the
  reason the wlc plan gives for it does not apply.
- **`main_map_changes_to_book_of_job.py` is a second cross-repo consumer, alongside
  codex-index-leningrad.** It reads book-of-job's `out/enriched-quirkrecs.json` and
  `gh-pages/jobn-details/`, and it writes the one tracked `in/` artifact. It now locates that
  sibling with `require_sibling("book-of-job", ...)` instead of `REPO.parent / "book-of-job"`,
  checked at the top of `main()` rather than at import so the module stays importable without the
  sibling. Phase 7 item 5's grep for `UXLC-utils/py` will not find it; a grep for `book-of-job`
  would have.
- **Phase 6's blast radius is essentially nil, and its stated grep returns zero.**
  `git grep -lI "generated by UXLC-utils" -- out gh-pages in data` matches **0 files** — nothing
  in this repo passes `generator_file` to `mb_cmn.file_io`, so no artifact carries a
  `mb_cmn.provenance` breadcrumb at all. There are exactly two repo-relative strings inside
  artifacts, both left untouched: `gh-pages/fois/index.html`'s prose "generated by
  py/main_fois.py" (unqualified by repo — from `fois_html._write_index`), and
  `main_map_changes_to_book_of_job.py:164`'s `"xml_source": "in/UXLC-misc/2026.04.01 -
  Changes.xml"`, which is written *into* the tracked JSON and which Phase 6's grep would not find
  either. Phase 6 is two edits, not a sweep.
- **Six known offenders was a large undercount: 26 modules needed a path change, spread over five
  shapes the plan's grep would not all have caught.** Plain literals (`"in/UXLC-misc"`,
  `"out/UXLC-misc/sanity_problems.json"`); f-strings (`f"gh-pages/clc/{label}-notes.json"`);
  module constants read by *other* modules (`my_uxlc.UXLC_CANONICAL_DIR`, consumed by
  `clc_attribution` and `main_uxlc_download_changes` as well as by its own `read`);
  `Path("in/UXLC-rest")` and `Path(".novc")` bindings; and `Path(__file__).resolve().parent.parent`
  walks that were cwd-independent already but conflated the two roots
  (`main_verify_notes_zip.py`, `main_map_changes_to_book_of_job.py`, and three test modules).
- **`PurePosixPath(...).name` was a live bug waiting for absolute paths.** All three FOI HTML
  modules derived a JSON catalog's link text and `href` that way. On Windows a `PurePosixPath`
  sees no separator in a backslashed absolute path and returns the whole string as the "name", so
  the pages would have shipped an absolute local path in an `href` — a wrong artifact, not a
  crash. Changed to `Path(...).name`. **Expect the same idiom in the other five repos.**
- **Three test modules were already compensating, and all three are retired.**
  `clc_attribution_test.main()` did `os.chdir(_REPO_ROOT)` before calling the library;
  `clc_kq_test` and `clc_dual_cant_test` each walked `__file__` up to the repo root to build
  `in/UXLC-39` paths. All now use `uxlc_paths.uxlc_39_dir()`, and the suite passes from a foreign
  cwd.
- **`WriteCtx.path` needed no signature change but did need its annotation corrected.** It is
  typed and flows through `mb_cmn.file_io.with_tmp_openw` to `open()`, so a `Path` works
  throughout (`_openw`'s `os.path.dirname` and `_tmp_path`'s `pathlib` both accept one). The one
  place a `str` is still passed deliberately is `polite_download.CacheConfig(dir_path=...)`, whose
  field is declared `str` in a vendored module this repo must not edit.
- **The accessor is deliberately more than five root functions.** `py/uxlc_paths.py` also has
  `uxlc_39_dir`, `uxlc_rest_dir`, `uxlc_misc_dir`, `uxlc_misc_fixed_dir`, `uxlc_notes_dir`,
  `out_uxlc_misc_dir`, `clc_pages_dir`, `fois_pages_dir`, `amb_early_mtg_pages_dir` and
  `tanach_us_http_cache_dir`, because `in/UXLC-misc` alone appeared in six modules and
  `out/UXLC-misc` in three. The point of the phase is that each such string appears once.

### The accessor, and how `mb_cmn/paths.py` got here

**This repo did not vendor `mb_cmn/paths.py`, and now does.** The plan above says Phase 2 does not
recur because `sibling_repo`/`require_sibling` already exist — true of MAM-basics, but they were
not *reachable* from UXLC-utils, whose `py/mb_cmn/` held 21 files and not that one. **Check this
per repo in the remaining plans rather than inheriting the Phase-2-not-needed conclusion.**

The fix is the sanctioned one and it is durable: `main_update_vendored_files.py` syncs by
`vendoring_sync.copy_by_intersection`, which iterates the files **already present in the
destination**, so dropping `paths.py` into `py/mb_cmn/` once enrolls it permanently — the next
refresh copies it rather than dropping it. Confirmed by re-running the script (it reported 21
copied files, up from 20) and again with `--force-provenance` to record it in
`py/mb_cmn/_provenance.md`. `doc/vendoring-inventory.md` here was regenerated in the same breath
(`d5a5052`): the UXLC-utils `mb_cmn` row goes 20 → 21 files, still `identical` / `copy_script`,
tree total 177 → 178.

`py/uxlc_paths.py` is then the UXLC analogue of `py/wlc_paths.py` here, and deliberately the same
shape. `uxlc_data_root()` is `paths.repo_root()` today; **after the move it becomes
`paths.require_sibling("UXLC-utils", paths.sibling_repo("UXLC-utils"))` and that is the whole of
Phase 3b** — one line, because nothing else composes a data path off anything but that function.

### Not exercised, and why

Three entry points' path edits are inspection-only. `main_uxlc_download_changes.py` and
`main_clc_download_notes.py` hit tanach.us and would rewrite `in/`; `main_verify_notes_zip.py`
needs a `Notes.zip` in `~/Downloads`. **Phase 3e should run at least one of the downloaders once
from MAM-basics**, since a downloader writing into the wrong repo's `in/` is precisely the failure
this phase exists to prevent and is the one class of it still unproven.

**Phase 3 could not do that, and it is now deferred rather than owed.** tanach.us' `robots.txt`
disallows both paths, and Ben decided on 2026-08-02 that live-download testing does not block the
programme; see Phase 3's record for the block and the three indirect checks done instead, and
MAM-basics **#214** for what stays untested. **No later phase of this plan owes a downloader run.**

---

The rest of this section is the plan as written before the phase ran; the six offenders it names
were the starting point, not the total.

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

## Phase 3 — copy the Python in (dual residency) — DONE 2026-08-02

**Landed as two MAM-basics commits — `662db55` (this repo's own eight orphan combining marks,
deliberately first and alone so no commit is red) and `f202d21` (the copy, 74 files). Nothing
was committed in UXLC-utils, which is what dual residency means.** Every baseline was
re-measured first and every one matched: 102 tracked `.py` there, 184 `gh-pages/`, 27 `out/`,
556 `in/`, 2 `data/`, 15 entry points, 8 test modules plus the runner, and `py/main_test.py`
reporting **8/8 modules passed**. This repo went 693 → 766 tracked `.py`.

**The oracle ran as specified and passed.** From `C:\Users\BenDe\GitRepos\MAM-basics` as the
working directory, main checkout: `main_uxlc_mega.py`, then `main_clc.py`, then
`main_map_changes_to_book_of_job.py`. Afterwards `git status --porcelain` was **empty in
UXLC-utils** and held nothing outside `py/` here. Run twice, before and after the lint fixes
below, with the same result both times.

Final measurements: **916 passed / 5 skipped** here, up from **862 / 5** by exactly the 54 the
moved tests collect; `ruff check py` and `black --check py` (765 files) both clean;
`py/main_source_hygiene.py` clean over this tree.

Nine things went differently from what is written underneath. The first four bear on Phase 4:

- **The oracle is 214 artifacts, not 216, and only 127 of them are regenerated at all.** The
  count is the plan's own arithmetic slip: its four components are 184 `gh-pages/` + 27 `out/` +
  2 `data/` + 1 `in/`, which sum to **214**, re-measured and confirmed. Worse, an mtime snapshot
  taken immediately before the run shows **127 rewritten and 87 untouched** — 86 static assets
  (81 `gh-pages/amb-early-mtg/img/`, 2 `gh-pages/img/`, `gh-pages/index.html`,
  `gh-pages/style.css`, `gh-pages/woff2/Taamey_D.woff2`) plus **`out/UXLC-misc/map-changes-to-book-of-job.md`,
  a hand-authored prose report sitting in a generated tree** (`e4edbc5` "Move mapping report out
  of gh-pages"; nothing in `py/` writes that path). **Phase 1's write-up is wrong on this point**
  — it claims "all 216 artifacts came back byte-identical … their mtimes confirm they were
  actually rewritten rather than skipped," which cannot have been true of the 87. **These 87 are
  the list Phase 4 must name**, the way wlc-utils' Phase 4 named its 111.
- **76 files move and 74 land, not 77 and 76.** The disposition table's own rows sum to 76 moving
  (18+11+8+8+7+5+3+15+1); the headline 77 additionally counts `tools/repo_maintenance.py`, which
  the same table says *retires*. Of the 76, `main_test.py` and `main_update_vendored_files.py`
  disappear by design, so **73 new files landed** plus one merged away (below) = 74.
- **`py/mb_cmn/mb_cmn_bib_locales.py` is NOT a vendored copy, so the pure deletions are 24, not
  25.** `cmp` against this repo's originals found 24 identical and one with no counterpart at
  all: that file is MAM-basics' `bib_locales.py` plus a tail of six back-compat aliases for prior
  UXLC-local naming, it is absent from `doc/vendoring-inventory.md`'s 21-file row, and
  `main_update_vendored_files.py` excludes it from the sync **by name** (`_PYCMN_EXCLUDE`).
  Landing a 636-line near-duplicate inside this repo's native `py/mb_cmn/` is precisely the
  two-module-objects hazard the global `CLAUDE.md` describes, so instead its **ten importers now
  use `mb_cmn.bib_locales`** and the three aliases with callers are spelled out at the call site:
  `ALL_BOOK_IDS`→`ALL_BK39_IDS` (8 sites), `ordered_short_dash_full`→`_39` (1), `section`→
  `get_secid` (1). The other three aliases had no callers. **Phase 4 still deletes the file** —
  but as UXLC-local code, not as a vendored copy, and the inventory row stays at 21.
- **The downloader run could not be completed, and not for any reason this move introduced:
  tanach.us' `robots.txt` now disallows both paths.** `main_uxlc_download_changes.py` raises
  `RobotsDisallowedError` on `https://tanach.us/Books/Tanach.xml.zip`, and
  `main_clc_download_notes.py` raises it on `https://tanach.us/Notes/...`;
  `polite_download` is configured `obey_robots_txt=True` and that was **not** worked around.
  What the check exists to prove is nevertheless established, from three directions: the live
  `main_uxlc_download_changes.py` run printed its target as
  `C:\Users\BenDe\GitRepos\UXLC-utils\.novc\Tanach.xml.zip` *before* the refusal; a live
  `main_clc_download_notes.py Obadiah` from this repo found and skipped UXLC-utils' committed
  copy of that note page, so it reads the right tree; and every write target composed offline
  (`in/UXLC-39`, `in/UXLC-rest`, `in/UXLC-misc/<date> - Changes.xml`, `in/UXLC-notes/...`, the
  HTTP cache) resolves under `C:\Users\BenDe\GitRepos\UXLC-utils`. `git status` was empty in
  **both** repos afterwards. **A downloader actually writing has still never been observed from
  here**, and cannot be until tanach.us' robots.txt changes or Ben decides otherwise.
  **Ben's decision, 2026-08-02: testing anything that requires a live download is deferred, and
  does not block completion of this plan or of the programme.** This is settled, not an open loose
  end — the loop closes at MAM-basics **#214**, which names what stays untested and notes that the
  thing it waits on is a separate task drafting an email to Chris Kimball, tanach.us' maintainer,
  about the robots.txt policy and about an authenticated mode of access.
- **3d's live risk did not materialize, and this repo's convention is why.** All 13 moved entry
  points call `sys.stdout.reconfigure` as the **first lines of `main()`**, not from
  `if __name__ == "__main__"`, so a step invoked as a module by `main_uxlc_mega` reconfigures
  exactly as it would standalone. The wlc-utils hazard was five mains that reconfigured only in
  the `__main__` guard; UXLC-utils' own `CLAUDE.md` requires the `main()` placement, and that
  rule is what made this a non-event.
- **There WAS one move bug, of exactly the class this exercise targets — it succeeds rather than
  crashing.** `main_uxlc_download_changes.py` ended with `import main_0_mega` /
  `main_0_mega.main()`. In UXLC-utils that named the UXLC pipeline; here it names **this repo's
  tree-wide mega**, so a routine input refresh would have rebuilt all of MAM-basics instead.
  Fixed to `main_uxlc_mega`. **Grep each remaining repo for cross-references to a renamed entry
  point by module name** — an `import` of a name that exists in both repos is invisible to a
  grep for paths.
- **`nfc_h_dot_below_test.py` merged instead of moving, and copying it would have been wrong
  rather than merely redundant.** It located its repo root by `git rev-parse` **from its own
  file's directory**, so under `py/tests/` here it would have scanned MAM-basics — a second,
  weaker pass over this tree (naive `line.find("#")` comment detection where this repo's
  `test_h_dot_below_nfc.py` uses `tokenize`, and none of this repo's exclusions), and it would
  have failed. Its scope is now a **third `_Scope`** in `test_h_dot_below_nfc.py`, beside
  MAM-basics and wlc-utils, so UXLC-utils' `doc/`, `CLAUDE.md` and `README.md` stay covered after
  Phase 4. The plan did not anticipate this; **expect the same collision in every remaining repo
  that carries a copy of this guard.**
- **This repo's two source lints found 68 things in the arrived code, all genuine**, plus the 8
  in this repo's own tree that the *arriving* lint found (commit `662db55`). `test_prose_conventions`:
  15 — agentive verbs (`UXLC reads`, `UXLC writes`, `the LC wrote`, `the atom carries`,
  `MAM shows`) become `has`; three `word-division` become `punctuation`; three `MAM reads
  through` become `runs through`, which leaves the established `reads on` / `reads through`
  idiom alone where its subject is a strand rather than a corpus. `test_transliterations`: 53 —
  **30 were our own identifiers and comments** and take the house spellings (`etnahta`→`etnaxta`,
  `tipeha`→`tipexa`, `atnach`→`atnax`, including a local variable in three test functions),
  while **23 legitimately quote an external vocabulary** and take a `# translit-ok` pragma naming
  which: UXLC's own `refuni` names, verbatim tanach.us note prose, book-of-job's mark names, and
  anchor-id slugs frozen in the tracked artifacts. Two of the pragmas had to be re-placed after
  black split the lines they had lengthened. **Budget for this in the remaining plans** — it was
  the single largest piece of Phase 3's work.
- **Ruff, which UXLC-utils does not run, found two:** an ambiguous `l` comprehension variable
  (`E741`) and an unused import (`F401`). Neither is a move consequence; both are what a repo
  with no linter accumulates. Expect a similar small crop per repo.

Also worth carrying forward: `check_registry()` and `TEST_MODULE_SPECS` went away with
`main_test.py`, as planned — but so did each moved test module's **`main()`**, which was a
hand-maintained list of that module's own test functions and had nothing calling it once the
registry runner stopped moving. Leaving eight of those in `py/tests/` would have re-imported, at
module scale, the drift hazard `fd2241a` removed at tree scale. The seven collect **54** tests
(16, 9, 9, 6, 6, 6, 2 — none zero), and 54 + the 6 merged into `test_h_dot_below_nfc.py` = **60**,
which is exactly what UXLC-utils' eight modules run there.

---

The rest of this section is the plan as written before the phase ran.

Land the 76 moving files in MAM-basics with both repos holding a working copy, exactly as
wlc-utils' Phase 3 did. **This phase must complete within a single session**: an interrupted
dual-residency window leaves a tree in which neither repo is authoritative and the oracle cannot
tell you which.

- **3a — land the files** under `py/`, with the renames above. `py/uxlc_paths.py` lands beside
  `py/wlc_paths.py`, which it is modelled on; the names do not collide.
- **3b — retarget the data root** so the moved code writes into `../UXLC-utils`. Phase 1 reduced
  this to **one line**: `uxlc_paths.uxlc_data_root()` becomes
  `paths.require_sibling("UXLC-utils", paths.sibling_repo("UXLC-utils"))`, and its module
  docstring says so. Delete the vendored `py/mb_cmn/paths.py` with the rest of `py/mb_cmn/`; the
  moved `uxlc_paths` then imports MAM-basics' own.
- **3c — fold the tests** into `py/tests/`, and check the collection count.
- **3d — `force_utf8_io()`.** Every `py/main_*.py` here reconfigures stdout/stderr to UTF-8 as the
  first lines of `main()`, per this repo's own `CLAUDE.md`. When a former entry point becomes a
  library module called by another entry point, **that reconfiguration silently disappears** —
  the wlc-utils plan lists this as a standing risk and it is live here, because
  `main_uxlc_mega.py` calls five other mains as modules.
- **3e — the oracle run.** From MAM-basics, regenerate all 216 tracked artifacts into
  `../UXLC-utils` and require `git status --porcelain` empty there **and** in MAM-basics. Phase 1
  already did exactly this run with the code still in UXLC-utils, so a diff here is a move bug and
  nothing else. Add one downloader run, which Phase 1 could not do.

**Stop and ask Ben before starting Phase 3.** It is the largest phase and the one whose failure is
expensive to unpick.

## Phase 4 — empty UXLC-utils

Pure subtraction, made safe by Phase 3's dual residency: delete all **102** tracked `.py` (100
before Phase 1 added two), `tools/`, `py/uxlc_misc/requirements.txt`, and the `py/` tree. **Stop
and ask Ben first** — it deletes over a hundred files.

**Two of those 102 are the downloaders, and no run of them is owed before deleting them.**
`main_uxlc_download_changes.py` and `main_clc_download_notes.py` both raise
`RobotsDisallowedError` against tanach.us as of 2026-08-02, and Ben deferred live-download testing
that day (Phase 3's record; MAM-basics **#214**). Delete them with the rest.

`CLAUDE.md` keeps only what is about this repo and gains what a reader arriving afterwards has no
other way to learn: that there is no Python here, that the code generating `out/` and `gh-pages/`
is `../MAM-basics/py/`, and which entry point writes what. The MAM-reading conventions, the
vendoring rules, the entry-point rules and the source-hygiene rules move to MAM-basics' `CLAUDE.md`
with the code they govern. **`doc/clc-design.md` stays** — it is a design document about the CLC
edition, not about the code.

**Name the tracked artifacts that no program generates**, the way wlc-utils' Phase 4 named its
111, so that deleting them in the belief they will come back stays a mistake nobody makes twice.
**Phase 3 measured them: 87 of the 214** — 81 `gh-pages/amb-early-mtg/img/`, 2 `gh-pages/img/`,
`gh-pages/index.html`, `gh-pages/style.css`, `gh-pages/woff2/Taamey_D.woff2`, and
`out/UXLC-misc/map-changes-to-book-of-job.md`, the last being a hand-authored prose report living
under a generated tree. Re-derive the list rather than copying it (snapshot mtimes across the
four trees, run every generator, and list what did not move), but expect these.

**Re-attaching source hygiene needs no work beyond deleting `tools/`.** Phase 3 landed
`py/repo_hygiene/source_hygiene.py` and `py/main_source_hygiene.py` here, where the CLI scans
*this* repo's tree and `py/tests/source_hygiene_test.py` is the guard; both are clean. What is
lost with `tools/git-hooks/pre-commit` is the per-commit enforcement in UXLC-utils, which after
Phase 4 has no Python to enforce it over. If Ben wants the check running per commit on
**MAM-basics**, that is a new hook in this repo and a decision to put to him, not a
re-attachment.

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

**Phase 1 established the blast radius, and it is two strings in two files, not a sweep.** The
grep this section prescribed —

```powershell
git grep -lI "generated by UXLC-utils" -- out gh-pages in data
```

— matches **zero** files: nothing in this repo passes `generator_file` to `mb_cmn.file_io`, so no
artifact carries an `mb_cmn.provenance` breadcrumb at all. What does exist is two repo-relative
strings that a grep for the breadcrumb phrasing misses:

1. `gh-pages/fois/index.html` — the prose "This is an HTML view of the FOI catalog generated by
   py/main_fois.py", written by `fois_html._write_index`. Unqualified by repo, so it needs the
   repo name added rather than one name swapped for another.
2. `in/UXLC-misc/2026.04.01-map-to-book-of-job.json` — its `"xml_source"` field, the literal
   `"in/UXLC-misc/2026.04.01 - Changes.xml"` at `main_map_changes_to_book_of_job.py:164`. A
   repo-relative path *inside* an artifact, and it stays correct as long as it is read as relative
   to UXLC-utils, which is where the file lives.

**The ordering rule still holds even at this size.** Do not "fix the now-wrong path" mid-move:
touching either of these before the move destroys the oracle for the artifact carrying it. The
wlc-utils plan restates this as its first standing risk. Phase 1 left both alone.

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
   run the grep anyway, because it is what would have revealed that one. **Grep for
   `book-of-job` too**: Phase 1 found that `main_map_changes_to_book_of_job.py` reads that
   sibling's `out/` and `gh-pages/`, a cross-repo dependency running in the other direction that
   a `UXLC-utils/py` grep cannot see. It now goes through `require_sibling`, so a missing
   book-of-job fails naming both environment overrides instead of composing a path into nothing.
6. **Outside both repos:** check `C:\Users\BenDe\.claude\skills\` and its tracked copy in
   `github-misc/dot-claude/skills/` for citations of UXLC-utils Python. The `hebrew-prose` skill
   names UXLC-utils among the repos it governs and cites `py/clc/clc_dual_cant.py` for the
   silluq-vs-meteg rule. **The live copy and the tracked copy do not sync automatically — edit
   both.** The wlc-utils plan calls its equivalent item the one most likely to be forgotten,
   because neither repo's tooling can see it. **Stop and ask Ben**, as that plan did: it commits
   to a third repo.
