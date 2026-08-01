# Evacuate all Python from wlc-utils into MAM-basics

## Status

| Phase | State |
|---|---|
| 0 — MAM-basics lint and dependency baseline | **done** 2026-08-01, commits `daebad0` and `83766c3` |
| 1 — wlc-utils: two roots, no cwd | **done** 2026-08-01, commits `5ae429d` and `e5be610` (both in wlc-utils) |
| 2 — `mb_cmn/paths.py` absorbs the override chain | **done** 2026-08-01, commit `d01f2c1` |
| 3 — copy the Python in (dual residency) | **done** 2026-08-01, commits `36a6ea8`, `7e8ee0f`, `a647e93`, `646bf2d`; plus `788e06c` in wlc-utils and `0e8c80c` in MAM-with-doc |
| 4 — empty wlc-utils | not started |
| 5 — flip the provenance breadcrumbs | not started |
| 6 — disambiguate issue citations | not started |
| 7 — cross-repo bookkeeping | not started |

This file is the tracked copy and the one to update. It was copied on 2026-08-01 from
`C:\Users\BenDe\.claude\plans\plan-the-evacuation-of-glistening-rocket.md`, which is not
under version control anywhere; that copy now carries a pointer here and should not be
edited.

---

Written 2026-07-31, re-verified against both trees the same day after the maqaf-scans work
landed. Self-contained: every number below is stated with the command that re-establishes it,
because the tree will have moved on. **Re-measure before relying on a figure; treat a mismatch
as a finding, not noise.**

Repos are `C:\Users\BenDe\GitRepos\wlc-utils` and `C:\Users\BenDe\GitRepos\MAM-basics`.
Each has its own `.venv`; the system Python has neither pytest nor PLY. Both repos must be
run from their own root.

## Context

Maintaining Python across multiple repos has become too taxing. This moves **all** of
wlc-utils' Python into MAM-basics, leaving wlc-utils a data-and-docs repo: `in/`, `out/`,
`gh-pages/`, `data/`, `doc/`. The moved code writes back into wlc-utils as a sibling — already
MAM-basics' dominant pattern, since it generates into MAM-parsed, MAM-with-doc, MAM-simple and
MAM-OSIS the same way. `gh-pages/` stays put indefinitely: moving it would break links in the
wild without a forwarding mechanism.

### Scale

- wlc-utils: **267 tracked `.py`, 59,870 lines** (`git ls-files "*.py"`), of which `py/accgram/`
  is 130 and `py/tests/` is 37 (36 `test_*.py` plus the `mc_marks.py` helper).
- Of those, the 26 files in `py/mb_cmn/`, `py/mb_misc/` and `py/mb_diff_mpu/` are vendored from
  MAM-basics and were **byte-identical** to MAM-basics' originals at last check, with no
  wlc-only extras — so they are pure deletions. **Re-confirm with `cmp` over the three
  directories before deleting**; if any file now differs, that difference is a finding to resolve
  first. **241 files actually move.**
- MAM-basics receives them alongside its own 456 `.py` / 68,290 lines and 34 test modules.
- The oracle throughout is **476 tracked artifacts** — 193 under `out/`, 283 under `gh-pages/`
  (`git ls-files out | wc -l`, same for `gh-pages`) — plus tracked
  `in/accgram/uxlc_accent_changes.json`. Regenerating them byte-identically is the test, per
  `wlc-utils/doc/agent-planning-principles.md` §"Generated Outputs Are the Tests".

### Decisions already settled (do not relitigate)

1. **Flat namespacing, minimal renames.** `accgram/`, `py_uxlc/`, `py_wlc/`, `py_html/`,
   `py_wlc_a_notes/`, `py_wlc_diffs_420422/`, `py_wlc_json_and_unicode/` land as-is — none
   collide with MAM-basics' 33 packages, and their intra-package imports need no edit because
   `py/` is already `sys.path[0]` in both repos. Rename only `cmn/`→`wlc_cmn/`,
   `repo_paths.py`→`wlc_paths.py`, `issue_edit.py`→`wlc_issue_edit.py`. Tests fold into
   MAM-basics' `py/tests/`. **Rejected:** an umbrella `py/wlc/` subtree — it would rewrite ~740
   import statements to buy naming tidiness.
2. **Plain copy, no git history graft.** History stays readable in wlc-utils, which is not going
   away. **Rejected:** a `filter-repo` subtree merge to preserve blame.
3. **`py/main_test.py` in MAM-basics flips to a `pytest.main()` wrapper**, matching the one
   wlc-utils adopted on 2026-07-30. All MAM-basics test modules are `unittest.TestCase` and
   pytest collects those natively, so **zero test files are rewritten on either side**, and the
   hand-maintained `TEST_MODULE_SPECS` registry with its silent-drop hazard disappears.
   **Rejected:** porting wlc's ~299 pytest functions to unittest.
4. **ruff comes along and lints the whole merged tree.** Pre-existing findings in MAM-basics' own
   files get their own commit, not folded into the evacuation.
5. **Provenance breadcrumbs flip to MAM-basics**, in a dedicated commit near the end (Phase 5).
6. **GitHub issues unify going forward only.** The 88 existing wlc-utils issues are **not**
   transferred — they keep their numbers and stay put. New issues, including new work on the
   moved code, are filed in MAM-basics. The moved code's bare `#NN` citations get a `wlc-utils#`
   prefix where they name a wlc-utils issue (Phase 6).

### Preconditions

**Both blocking preconditions were satisfied as of 2026-07-31. Re-confirm, don't assume.**

**1. `wlc-utils/doc/PLAN-sys-path-insert.md` is complete** (commits `3083859`, `36d7693`,
2026-07-30). `conftest.py` is deleted and `py/main_test.py` — a `pytest.main()` wrapper — is
tracked. Confirm with `git ls-files py/main_test.py conftest.py` (the first should be listed,
the second not). **Do not confirm with `git log --oneline -N`:** those commits reached `main`
through the merge `7c0a083` and do not appear near the tip. Use
`git merge-base --is-ancestor 3083859 HEAD` instead.

**2. The maqaf-scans plan is finished** —
`C:\Users\BenDe\.claude\plans\in-maqaf-nonfinal-accents-html-include-i-gleaming-eagle.md`,
landed by `e941f1c`, `99808fe`, `5f0fdeb`, `8bb6602`, `cf7c56d`. It went further than it
planned: `99808fe` implemented the viewBox-vs-scan-size lint that plan had filed as out of
scope. **It had to precede this plan and did**, because the two contend for the same oracle —
this one proves itself by regenerating 476 artifacts to a zero diff, that one deliberately
changed two of those pages and added two PNGs. If any comparable page work is in flight when
this plan starts, it must finish or wait: concurrent artifact changes mean this plan cannot tell
a move bug from a page edit.

**3. Clear wlc-utils' orphaned agent worktrees.** From `C:\Users\BenDe\GitRepos\wlc-utils`:

```powershell
.venv\Scripts\python.exe py\main_repo_maintenance.py --skip-black --skip-lint --skip-tests --skip-rebuild
```

### Baselines — captured 2026-08-01

Every phase compares against these, per `agent-planning-principles.md` §"Write State Back
Before Continuing"; later phases cannot be judged without them.

| Measure | Captured | Planned-at value |
|---|---|---|
| MAM-basics `py\main_test.py` | **320 tests, OK** (unittest registry) | — |
| wlc-utils `py\main_test.py` | **504 passed, 5 skipped** | 487/5, before maqaf-scans |
| wlc-utils `git ls-files "*.py"` | **267** | 267 |
| wlc-utils `git ls-files out` | **193** | 193 |
| wlc-utils `git ls-files gh-pages` | **283** | 283 |
| wlc-utils `git grep -lI "generated by wlc-utils" -- out gh-pages in` | **61** | 61 — the Phase 5 blast radius |

All four file counts matched the planned values exactly. The commands that re-establish
them, from each repo's own root:

```powershell
.venv\Scripts\python.exe py\main_test.py
```

Two facts worth carrying forward, both bearing on later phases:

- **black is at 26.5.1 in both venvs**, so the "black version skew" risk below is not live
  as of 2026-08-01. Re-check before Phase 3 rather than trusting this line.
- **MAM-basics' 320 tests still pass, and `main_0_mega.py` still regenerates every
  artifact with no diff, after Phase 0's lint fixes.** That is the Phase 0 half of the
  Phase 3 oracle.

---

## How to run this plan across sessions

**This file is the orchestrator. No live session needs to stay open**, and no session needs to
remember anything from the one before it.

Each session: read this file, do exactly one phase, verify it, then **write the result back into
the Status table at the top** — state, date, and the commit shas — and mark that phase's own
heading `— DONE <date>`, recording under it the numbers actually measured and anything found
that the plan did not predict. A phase whose result is not written back cannot be judged by the
next session, which is the whole point of `agent-planning-principles.md` §"Write State Back
Before Continuing". Then spawn a task chip for the next phase, quoting this file's absolute path.

Phase 0 is the worked example of that shape — copy it.

Phases are strictly sequential — **do not run two in parallel, including Phases 0 and 1.** They
touch different repos and look independent, but Phase 1's verification asserts that MAM-basics'
`git status --porcelain` is empty, which a concurrent Phase 0 would pollute.

**Stop and ask Ben rather than chaining on** at these four points:

- **Phase 0 Step E**, if MAM-basics' own ruff findings turn out to be project-sized rather than a
  step. Report a categorized count.
- **Before Phase 3.** It is the largest phase, it must complete within a single session (the
  dual-residency window leaves an ambiguous tree if interrupted), and it is the one whose failure
  is expensive to unpick.
- **Before Phase 4**, which deletes 267 files. Worth an explicit look.
- **Phase 7 item 8**, which commits to a third repo (`github-misc`) that neither repo's tooling
  can see.

Phases 1, 2, 5 and 6 are safe to chain automatically once their verification passes.

---

## The organizing idea: `repo_root()` splits into two roots

Everything hard here reduces to one fact. Today `wlc-utils/py/repo_paths.py`'s `repo_root()`
answers two different questions with one value:

- **CODE root** — where the Python lives: `py/`, `py/tests/`, the checkout `gh` and
  `git worktree` act on, the tree the source lints scan.
- **DATA root** — where the corpus lives: `in/`, `out/`, `gh-pages/`, `data/`, and (per Phase 3b)
  `.novc/`.

After the move these diverge. `py/main_0_mega.py:28` (`repo_root / "py"`) is a code use;
`py/accgram/chanted_word_accents.py:1107` (`repo_root / "out" / ...`) is a data use.
`py/tests/test_prose_conventions.py` is both in one function — line 181 code, lines 193-194 data.

The sequencing follows directly: **every change expressible as "stop conflating the two roots"
belongs in wlc-utils first, because there it is provable by byte-identical regeneration.**
Everything else can only happen after.

Scope is smaller than it looks. Of the ~41 `repo_paths.repo_root()` call sites, most are
vestigial `add_args(parser, repo_root=...)` threading, and most `default_*(repo_root)` helpers
ignore the parameter and call `out_dir()`/`gh_pages_dir()` instead (`supplied_marks.py:100-101`,
`mam_simple_verse.py:26-31`, `fix_tester.py:692-697`). Only five sites actually compose off it.

---

## Phase 0 — MAM-basics lint and dependency baseline — DONE 2026-08-01

*In MAM-basics.* So the first ruff failure after the move is unambiguously about moved code.

**Landed as `daebad0` (steps 1-3) and `83766c3` (step 4).** All three verification commands
below pass. Three things went differently from what is written underneath, and the first
of them changes how Phase 3 must be verified:

- **Ruff 0.16 widened its default rule set, so "the default rules" is no longer a stable
  thing to configure.** A fresh install gave MAM-basics ruff 0.16.1 while wlc-utils has
  0.15.21. With the *same* `ruff.toml`, 0.15.21 reports **0** findings on wlc-utils' `py/`
  and 0.16.1 reports **776** on that same unchanged tree; on MAM-basics the two report 53
  and 996. The default went from four rule families to roughly forty. MAM-basics'
  `ruff.toml` therefore writes the rule set out as an explicit
  `select = ["E4", "E7", "E9", "F"]` instead of inheriting it, and both ruff versions now
  agree at 53 here. **wlc-utils' own `ruff.toml` still inherits the default**, so a
  `pip install -U ruff` there — at any point before Phase 4 deletes the file — would
  manufacture 776 findings out of nothing. Phase 3's "`ruff check py` exit 0" step is only
  meaningful with the explicit `select` in place.
- **`black` was already in MAM-basics' `requirements.txt`**, contrary to step 1 below; only
  `ply` and `ruff` were actually missing. Both are installed and `import ply` succeeds.
- **Step 4 found 53 findings, not a project's worth.** 24 were ruff's own safe fixes (19
  F401 unused imports, 3 F541, 2 F811 — none serving as a re-export, checked against the
  sibling repos that vendor the files). The 29 hand fixes: 18 E402 all caused by
  `_REPOS = paths.repos_root()` sitting between two import blocks in `main_0_mega.py`; 4
  F841 (`_flag_non_inferrable()` in `main_explicit_xataf.py` mutates its argument, so the
  call stayed and only the binding went); 3 E741 `l`→`ltr` in `mb_diff_mpu`; one F601
  duplicate dictionary key in `foi/foiz_wt_oleh_yored.py`, where both entries mapped to the
  same value and so were dead duplication rather than a silently dropped mapping; one E711,
  one E731, and an F821 `noqa` for `usernames` in `ws/pywikibot-user-config.py`, which
  pywikibot pre-populates in the namespace it execs that file in.

Two of the files step 4 touched, `mb_cmn/read_books_from_mam_parsed_plus.py` and
`mb_cmn/ws_tmpl2.py`, are vendored into sibling repos. `main_0_mega.py`'s vendoring step
resyncs MAM-simple's copy of `ws_tmpl2.py` on its own, so no manual re-vendor is owed; but
the same mega run also resynced three MAM-simple files and one MAM-with-doc change-log page
that were **already** stale before Phase 0 touched anything. Expect those in the working
tree, and do not read them as move damage during Phase 3.

1. Add `ply` and `ruff` to `requirements.txt` and install them. (At planning time MAM-basics' venv
   had neither — check with `.venv\Scripts\python.exe -c "import ply, ruff"`.) Also add `black`,
   which wlc-utils' maintenance script runs but its `requirements.txt` never listed.
2. Copy `wlc-utils/ruff.toml` to `MAM-basics/ruff.toml` (default rules, `line-length = 100`,
   `target-version = "py311"`), fixing the header's repo name.
3. Add a `run_lint()` step to `MAM-basics/py/main_repo_maintenance.py`, mirroring wlc-utils'
   `py/main_repo_maintenance.py:119-123` (`subprocess.run([sys.executable, "-m", "ruff", "check",
   "py"], cwd=_REPO)`), plus a `--skip-lint` flag, wired in after `run_black()`. Update the
   docstring's step count.
4. **Separate commit:** fix whatever `ruff check py` reports across MAM-basics' existing files.

**Verify.** From `C:\Users\BenDe\GitRepos\MAM-basics`:

```powershell
.venv\Scripts\python.exe -m ruff check py
```

```powershell
.venv\Scripts\python.exe py\main_repo_maintenance.py --skip-novc --skip-tests --skip-rebuild
```

---

## Phase 1 — wlc-utils: two roots, no cwd — DONE 2026-08-01

*In wlc-utils.* The preparatory decoupling, provable in place.

**Landed as `5ae429d` (the code) and `e5be610` (one stale artifact, kept separate).** Every
baseline was re-measured first and every one matched: 267 tracked `.py`, 193 under `out/`,
283 under `gh-pages/`, 61 breadcrumb files, and 504 passed / 5 skipped both before and
after. ruff (0.15.21, unchanged — deliberately not upgraded) and black (26.5.1) are clean.

**The verification ran as specified and passed.** From `C:\Users\BenDe\GitRepos\MAM-basics`
as the working directory, each entry point by absolute path, individually — never through
`main_0_mega.py`, whose `cwd=repo_root` would have masked all of it:
`main_update_vendored_files`, `main_wlc_json_and_unicode`, `main_accgram` × 6 subcommands
(run-prose, run-poetic, run-dual-cant, run-printed-decalogue, survey-chanted-word-accents,
generate-html), `main_wlc_diffs_420422`, `main_wlc_a_notes`, `main_find_uxlc_accent_changes`,
`main_uxlc_grammar_test`, `main_edition_transcription build --check`, and the new
`highlight-picker`. Afterwards `git status --porcelain` was **empty in MAM-basics** and, apart
from the one artifact below, **empty in wlc-utils**. 475 of the 476 artifacts, plus tracked
`in/accgram/uxlc_accent_changes.json`, came back byte-identical from a foreign cwd.

Six things went differently from what is written underneath. The first bears on Phase 3:

- **`out/accgram/uxlc_grammar_test.txt` was stale in the tree, and Phase 3e step 6 will hit
  it again if this is forgotten.** It was last regenerated by `b8488ac` (2026-06-27);
  `995133d` (2026-06-29) retired "oddball" for "ungrammatical" in the source that writes its
  closing paragraph and never re-ran the generator. One line, one word. Regenerating from
  wlc-utils' **own** root gives the identical diff, which is how it was shown to be staleness
  rather than a cwd effect, and it is committed as `e5be610`. The cause is structural:
  `main_uxlc_grammar_test.py` is not one of `main_0_mega.py`'s seven steps, so it is the one
  tracked artifact nothing rewrites routinely. **Expect the same class of thing from
  `main_find_uxlc_accent_changes.py`, also outside the mega** — it happened to be current.
- **`uxlc.read`'s `books_dir="in/UXLC"` default named a directory this repo has never had.**
  `in/` holds `UXLC-39`, `UXLC-misc` and `Tanach-26.0--UXLC-1.0--2020-04-01`, so that default
  could not have resolved against *any* cwd. Its sole caller passes the directory explicitly,
  so it became a required argument rather than an absolute default.
- **`my_uxlc.UXLC_CANONICAL_DIR` already had a workaround, at a site the table below does not
  list.** `main_uxlc_grammar_test.py` overwrote the module constant at import time to make the
  module usable away from the repo root. Fixing the constant retires the monkeypatch, so the
  edit is two files, not one.
- **`chanted_word_accents.py` already had `default_json_out_path()` fifteen lines above the
  `add_args` that ignored it**, so the `--json-out` default (`repo_root / "out" / ...`) and
  `run`'s fallback (`repo_paths.out_dir() / ...`) were two spellings that could drift apart.
  `add_args` now calls the helper and `del repo_root`s the parameter, matching `scan_page`.
- **The optional half of 1b was taken: `gen_highlight_picker` is now a `highlight-picker`
  subcommand of `main_edition_transcription.py`**, with `add_args`/`run` like its five
  neighbours, its hand-rolled `sys.argv` scanning, `main()`, `__main__` guard and inline
  `stdout.reconfigure` all gone. `test_entry_point_subcommands.py` covers the wiring; the
  subcommand was also exercised end-to-end from the foreign cwd.
- **Two Phase 3/4 preconditions were confirmed early and cost nothing.** All 26 files in
  `py/mb_cmn/`, `py/mb_misc/` and `py/mb_diff_mpu/` are still byte-identical to MAM-basics'
  originals, so §Scale's "pure deletions" holds. And `main_update_vendored_files.py` is
  already fully `repo_paths`-anchored and **never touches MAM-simple** — so MAM-simple's four
  dirty `py-examples/` files are unrelated pre-existing drift, not something a wlc run
  produces. Do not read them as move damage in Phase 3.

**The proof must use MAM-basics as the foreign cwd, not an empty scratch dir.** MAM-basics has
its own `in/` and `out/`, so `_PUBLIC = "."` would *silently* write `MAM-basics/out/wlc420.json`
rather than crash. Only the real post-move cwd reproduces the silent-wrong-repo case.

### 1a — Kill the 12 cwd-relative offenders

Line numbers were accurate when planned; locate by content if they have drifted. Re-derive the
list with a grep for `"in/`, `"out/`, `"gh-pages/`, `"data/`, `"./` and `= "."` under `py/`,
discarding CSS hex colours and help text.

| Site | Literal | |
|---|---|---|
| `py/py_wlc_a_notes/my_wlc_a_notes_{full,native,summary,xml}.py` | `f"gh-pages/wlc-a-notes/{path}"` | write |
| `py/py_wlc_diffs_420422/my_word_diffs_420422_{full,summary}.py` | `f"gh-pages/420422/{path}"` | write |
| `py/main_wlc_json_and_unicode.py:53` | `_PUBLIC = "."` | write |
| `py/main_find_uxlc_accent_changes.py:203-204` | `in/UXLC-misc/all_changes.json`, `in/accgram/uxlc_accent_changes.json` | read + **write of a tracked file** |
| `py/py_uxlc/my_uxlc.py:7` | `UXLC_CANONICAL_DIR = "in/UXLC-39"` | read |
| `py/py_uxlc/my_uxlc_page_break_info.py:61` | `"data/lci_recs.json"` | read |
| `py/py_wlc_diffs_420422/my_word_diffs_420422_add_fields.py:65` | `in/UXLC-misc/all_changes.json` | read |
| `py/py_wlc_json_and_unicode/uxlc.py:8,12` | `books_dir="in/UXLC"` default arg | read |

Each becomes an absolute path off a `repo_paths` accessor. `WriteCtx.path`
(`py/py_html/wlc_utils_html.py:18`) is typed `str` but flows through
`mb_cmn.file_io.with_tmp_openw` to `open()`, so absolute works with no signature change. Fixing
`_PUBLIC` fixes `_UXLC_BOOKS_DIR` and all five path builders at once. The `out/accgram/...`
strings in `main_accgram.py` and `accgram/classify.py` are argparse help text, not paths —
leave them.

### 1b — Add the missing accessors and route the five live compositions through them

New in `py/repo_paths.py`: `data_dir()`, `novc_dir()`, `scans_dir()`. Then retarget
`accgram/chanted_word_accents.py:1107`, `accgram/scan_page.py:59`, `issue_edit.py:45-46`,
`main_repo_maintenance.py:63`, and `accgram/gen_highlight_picker.py:46-48` — the last being the
**only** module that bypasses `repo_paths` entirely (`Path(__file__).resolve().parents[2]`).

While there: `gen_highlight_picker.py` is a sixth independently-runnable module of the kind
`doc/PLAN-sys-path-insert.md` retired — hand-rolled `sys.argv` scanning (~lines 561-590), its own
`main()` and `if __name__ == "__main__"`, and an inline `stdout.reconfigure`. It escaped that
plan only because it has no `sys.path.insert`. Folding it into `main_edition_transcription.py`
as a `highlight-picker` subcommand is the same change as the other five and is cheapest here.
Optional, but it is the last one.

Leave `main_0_mega.py:28` and `py/tests/test_prose_conventions.py:181` alone — code-root uses,
handled in Phase 3.

### 1c — Verify

**`main_0_mega.py:94` passes `cwd=repo_root` to every child, which masks all of this.** Run the
steps **individually**, or neutralize that `cwd=` for the proof. Otherwise Phase 1 verifies
nothing.

From `C:\Users\BenDe\GitRepos\MAM-basics` as the working directory, run each wlc entry point by
absolute path, e.g.:

```powershell
C:\Users\BenDe\GitRepos\wlc-utils\.venv\Scripts\python.exe C:\Users\BenDe\GitRepos\wlc-utils\py\main_wlc_a_notes.py
```

Repeat for `main_wlc_diffs_420422.py`, `main_wlc_json_and_unicode.py`,
`main_find_uxlc_accent_changes.py`, and `main_accgram.py generate-html`. Then `git status
--porcelain` must be **empty in both repos** — empty in MAM-basics proves nothing leaked in,
empty in wlc-utils proves the artifacts regenerated byte-identically.

---

## Phase 2 — `mb_cmn/paths.py` absorbs the override chain — DONE 2026-08-01

*In MAM-basics.* **Absorb rather than let `wlc_paths.py` keep a private copy.**

**Landed as `d01f2c1`.** The predicted breakage was real and was reproduced before the
change: from `.claude/worktrees/focused-bhabha-25d9de`, `sibling_repo("MAM-parsed")`
answered `C:\Users\BenDe\GitRepos\MAM-basics\.claude\worktrees\MAM-parsed`, `exists: False`.
After the change, verified on a throwaway worktree cut from the Phase 2 commit and then
removed: with nothing exported it still resolves there but now **raises**, naming the path,
`REPO_MAM_PARSED_DIR`, `REPOS_ROOT` and the siblings root searched; with
`REPOS_ROOT=C:\Users\BenDe\GitRepos` it resolves to the real clone and passes
`require_sibling`. `main_test.py` and `main_0_mega.py` are unchanged from the main
worktree — the mega regenerated every artifact with `git status --porcelain` empty in
both MAM-basics and wlc-utils.

Three notes:

- **Only `repos_root()` and `sibling_repo()` exist, not additional `siblings_root()`/
  `sibling()` aliases.** The instruction below asks for `sibling_repo` as an alias for
  `sibling`, but its stated goal is leaving the 63 existing call sites untouched, and one
  name per function achieves that with less. Phase 3b already has `wlc_paths` delegating
  wlc's spelling to this module, so nothing needs two names for one function. **Phase 3b's
  delegation targets are therefore `paths.repos_root` and `paths.sibling_repo`.**
- **Tests: 320 → 333.** `py/tests/test_mb_cmn_paths.py`, ported from wlc-utils'
  `test_repo_paths.py`, with two cases that are new rather than ported: that `wlc-utils` and
  `wlc-utils-private` map to distinct env variables rather than one shadowing the other, and
  that `REPOS_ROOT` makes a checkout whose parent holds no clones find the real ones. It is
  registered in `TEST_MODULE_SPECS`, and the registry was compared against
  `py/tests/test_*.py` afterwards — 35 files, 35 registered, no silent drop. **That check
  disappears at Phase 3d**, which deletes the registry.
- **`Get-ChildItem env:` found no `REPOS_ROOT`, no `REPO_*_DIR` and no `WLC_*`**, so the
  rename carries no compatibility cost, as predicted.

This is not hypothetical. `MAM-basics/py/mb_cmn/paths.py` computes `repos_root()` as
`repo_root().parent`; in a worktree under `.claude/worktrees/` that is the worktrees directory,
so `sibling_repo("MAM-parsed")` resolves to a path that does not exist. **MAM-basics is already
broken in its own worktrees** — check with `git worktree list`, then from any listed worktree:

```powershell
..\..\..\.venv\Scripts\python.exe -c "from mb_cmn import paths; print(paths.sibling_repo('MAM-parsed'))"
```

wlc-utils' `repo_paths.py` was written to fix exactly this, with a three-level override chain
(`WLC_<NAME>_DIR` → `WLC_SIBLINGS_ROOT` → `repo_root().parent`) and a `require_sibling()` that
fails with a message naming both overrides rather than skipping. Keeping two copies would leave
the fix in a file named `wlc_paths.py` while the module everything imports stays broken.

Blast radius is nil: `mb_cmn` is vendored into six repos, but `paths.py` exists only in
MAM-basics, and `vendoring_sync.copy_by_intersection` copies only files already present in the
destination — so nothing propagates until a repo opts in.

Port `repo_paths.py:59-114` (`siblings_root`, `_env_name`, `sibling`, `require_sibling`) and its
module docstring into `py/mb_cmn/paths.py`, keeping `sibling_repo(name)` as an alias for
`sibling(name)` so existing call sites are untouched. Rename the env prefix from `WLC_` to
repo-agnostic (`REPOS_ROOT`, `REPO_<NAME>_DIR`) — nothing in the environment set any `WLC_*` var
when this was planned (`Get-ChildItem env:WLC_*`), so there is no compatibility cost.

Rewrite `wlc-utils/py/tests/test_repo_paths.py` (~33 tests) as a test of `mb_cmn.paths`. It is
the oracle proving the override chain moved intact — treat it as a deliverable, not collateral.

**Verify:** the worktree command above now resolves to the real clone with `REPOS_ROOT` set;
`py/main_test.py` and `py/main_0_mega.py` unchanged from the main worktree.

---

## Phase 3 — Copy the Python into MAM-basics (dual residency) — DONE 2026-08-01

**Landed as four MAM-basics commits — `36a6ea8` (the `main_test.py` flip, deliberately
first and alone), `7e8ee0f` (the copy), `a647e93` (MAM-basics' own newly-linted prose) and
`646bf2d` (one generator ordering fix) — plus `788e06c` in wlc-utils and `0e8c80c` in
MAM-with-doc.** Every baseline was re-measured first and every one matched: 267 tracked
`.py` in wlc-utils, 193 under `out/`, 283 under `gh-pages/`, 61 breadcrumb files, 504
passed / 5 skipped, and 333 tests in MAM-basics. black is 26.5.1 in both venvs, so the
black-skew risk was still not live.

**The oracle ran as specified and passed.** From `C:\Users\BenDe\GitRepos\MAM-basics` as
the working directory: wlc's own mega first for a clean baseline, then `out/accgram/` and
`gh-pages/accgram/` deleted, then MAM-basics' merged `py\main_0_mega.py`, then the seven
accgram subcommands the mega does not run (run-dual-cant, run-printed-decalogue,
survey-chanted-word-accents, xcheck-poetic, servi-xcheck, test-fixes, grammaticality),
`main_uxlc_grammar_test.py`, `main_find_uxlc_accent_changes.py`, and
`main_edition_transcription.py build --check` (12/12 committed `.txt` bodies re-derived).
**Not one artifact came back modified.** After restoring the 111 files nothing
regenerates (73 static assets under `gh-pages/accgram` — three `.js` and seventy
`.png`/`.jpg` — and 38 under `out/accgram/goerwitz-stderr/`, captured stderr from the
original C checker that no Python here writes), `git status --porcelain` was empty in
wlc-utils, MAM-basics, and all five MAM siblings.

Final measurements: **824 passed, 5 skipped** in MAM-basics (**69 test modules**, exactly
as predicted); **504 passed, 5 skipped** still in wlc-utils; **693** tracked `.py` in
MAM-basics (457 + 236); `ruff check py` and `black --check py` (692 files) both clean.

The test arithmetic closes exactly: 333 + 504 = 837, less 16 for `test_repo_paths.py`
(Phase 2 had already ported it to `test_mb_cmn_paths.py`, so it was not copied) and 6 for
the collapsed `test_h_dot_below_nfc.py`, plus 1 new `wlc_issue_edit` test and 8 new
entry-point-exemption tests = 824.

Seven things went differently from what is written underneath. The first three bear on
Phase 4 and beyond:

- **`generate-html` could not run against a deleted `out/accgram`, and this is
  pre-existing.** `printed_decalogue_koren_page` reads
  `out/accgram/maqaf-nonfinal-accents.json` — the only place one HTML generator consumes
  another's output — but sat three entries ahead of its writer in `_HTML_GENERATORS`. It
  never surfaced because the file was always left over from a previous run; step 2's
  perturbation is precisely what exposes it. **Confirmed pre-existing before anything was
  touched, by running wlc-utils' own unmodified `py/main_accgram.py generate-html`
  against the same deleted tree: identical traceback, identical missing path.** Fixed in
  MAM-basics only (`646bf2d`), since wlc's copy is the oracle and Phase 4 deletes it.
- **Two source lints now scan MAM-basics' own tree and found 13 things there.**
  `test_transliterations` (8, in 4 files) and `test_prose_conventions` (5, in 3 files) —
  more than the 6-in-3 the plan predicted, because `repo_util/check_memory_health.py` did
  not exist when it was written. All were genuine; `a647e93` resolves them per decision 4,
  in its own commit rather than folded into the move. Of the eight transliteration hits
  only one took a `# translit-ok` pragma; `uni_heb.py`'s three became "Note on ZINOR",
  matching what that note's own body already said, and two were plain uses fixed outright
  (`mehuppak`→`mahapakh`, `etnachta`→`atnax`). **The copy commit `7e8ee0f` is therefore
  red on three tests; the tree is green from `a647e93`.**
- **`test_entry_point_subcommands` newly discovers MAM-basics' mains, and eight of them
  fail its convention.** They register subcommands with the parser still inside `main()`,
  so it cannot be read without running the program; two (`main_mam_simple`,
  `main_slide_generator`) also have no `Subcommands:` docstring block at all. Extracting
  eight `build_parser()`s and authoring two docstring blocks is its own commit, so they
  sit in an explicit `_PARSER_NOT_YET_EXTRACTED` list. **That list is not a silent skip:**
  a new test asserts each name is still discovered and still genuinely unconverted, so
  converting one without deleting its line fails, and so does a stale line. A stem not on
  the list that lacks `build_parser()` fails exactly as before.
- **wlc-utils' own vendoring step re-synced the three `mb_cmn` files `a647e93` touched**,
  which is the dual-residency window working as designed rather than a surprise. Committed
  in wlc-utils as `788e06c` so the oracle's "empty `git status`" stayed meaningful.
  Comments only; no artifact changed.
- **`wlc_issue_edit`'s byproduct path had to change too, not just its `gh` invocation.**
  Making the repo an explicit argument fixes the `gh` call, but one
  `issue-69-outgoing.md` for two trackers reintroduces the same ambiguity in the scratch
  directory, so the path carries the repo. It also moved to MAM-basics' `.novc/`: what it
  is a byproduct of is an issue edit, not the wlc-utils corpus.
- **`main_accgram` needed `almost_main(argv)`, not a bare `almost_main()`**, since three
  mega steps come from it and the mega blanks `sys.argv` before running its steps.
- **MAM-simple's four dirty `py-examples/` files were not dirty.** The plan and the
  Phase 0 record both warn not to read them as move damage; in the event all five MAM
  siblings were clean throughout, so there was nothing to misread.

Also worth carrying forward: `mb_cmn/`, `mb_misc/` and `mb_diff_mpu/` were re-confirmed
byte-identical before the copy — 26 `.py` identical, 0 differing, the only wlc-only files
being the three `_provenance.md` breadcrumbs. §3a's "pure deletions" holds for Phase 4.

---

**The key structural decision: copy, do not move.** Get MAM-basics fully green while wlc-utils
stays untouched. Both copies then write into the *same* `out/` and `gh-pages/`, which makes the
old code an **independent oracle** for the new — shape 1 of `agent-planning-principles.md`.
Deletion is Phase 4, a pure subtraction verified separately. A single move commit would have no
oracle at all.

### 3a — Land the files

Copy as-is: `accgram/` (~130 files), `py_uxlc/`, `py_wlc/`, `py_html/`, `py_wlc_a_notes/`,
`py_wlc_diffs_420422/`, `py_wlc_json_and_unicode/` — **0 import edits**.
Rename: `cmn/`→`wlc_cmn/`, `repo_paths.py`→`wlc_paths.py`, `issue_edit.py`→`wlc_issue_edit.py`
(roughly 48, 55 and 1 import sites respectively).
Do **not** copy `mb_cmn/`, `mb_misc/`, `mb_diff_mpu/` — verify byte-identity, then leave them for
Phase 4 to delete.

One deviation worth taking: `cmn/git_worktree_cleanup.py` lands in **`repo_util/`**, not
`wlc_cmn/`. `MAM-basics/py/repo_util/check_repo_standards.py:38` already calls it "the reference
implementation" for the cross-repo `worktree_hygiene` standard; filing it under a
`wlc_`-prefixed package makes it look repo-specific when the point is that it is not. Cost: one
import and one comment.

### 3b — Retarget `wlc_paths.py`

```
repo_root()      → rename to wlc_data_root(); body becomes
                   paths.require_sibling("wlc-utils", paths.sibling_repo("wlc-utils"))
out_dir / in_dir / gh_pages_dir / data_dir  → bodies unchanged, now off the data root
novc_dir()       → wlc_data_root() / ".novc"    (stays in wlc-utils -- see below)
scans_dir()      → novc_dir() / "scans"
siblings_root / sibling / require_sibling   → delegate to mb_cmn.paths
mam_simple_dir(), mam_parsed_plus_dir(), etc.  → unchanged (already sibling lookups)
```

**Rename `repo_root()` to `wlc_data_root()` rather than keeping an alias.** In a repo whose
actual root is elsewhere the old name is actively misleading, and renaming forces every call
site to be *looked at* — which is the point. A silent rename leaves them all resolving
plausibly to the wrong thing.

**`.novc/` stays in wlc-utils**, and MAM-basics keeps its own — two scratch dirs, each in the
repo whose data it concerns. The tempting alternative (scratch follows the code, so `.novc`
becomes MAM-basics') breaks `gen_highlight_picker.py`: its `_build_html` sets
`img_url = f"../gh-pages/accgram/img/{img_name}"`, a path **relative to the picker page's own
`.novc/` location**. Move `.novc/` to MAM-basics and that resolves to `MAM-basics/gh-pages/...`,
which does not exist — and it breaks the ordinary `file://` open, not just the opt-in `--serve`
mode, since both consume the same relative `src`. Keeping `.novc` under the data root leaves the
picker, `scan_page.py`'s `.novc/scans`, and wlc-utils' `.gitignore` line all working with no
edit at all. Say in the module docstring that `wlc_paths` is deliberately two-rooted.

Consequence: nothing wipes wlc-utils' `.novc/` once Phase 4 deletes its maintenance script, so
MAM-basics' `main_repo_maintenance.py` step 1 must wipe **both** — it already resolves wlc-utils
via `wlc_paths`.

`WLC_SCANS_DIR` (`accgram/scan_page.py:56`, defaulting to
`C:\Users\BenDe\OneDrive\Documents\ScansOfBooks`) is unaffected: absolute and out-of-repo
already. Its output follows `novc_dir()`.

**One hazard the `.novc` decision does not dissolve — `wlc_issue_edit.py`.** Its own docstring
states the trap: *"`gh` resolves which repo 'issue &lt;number&gt;' names from the git checkout it
runs in, so an unanchored call made from another repo's directory would edit THAT repo's
same-numbered issue."* It passes `cwd=_REPO_ROOT` (~lines 79 and 115). With the trackers
deliberately split (decision 6), *neither* root is a safe default — wlc-utils holds issues 1-88,
MAM-basics holds everything new. So **make the repo an explicit required parameter**: pass
`--repo bdenckla/<name>` through to `gh`. An explicit argument cannot silently edit the wrong
tracker; an inherited cwd can.

### 3c — Entry-point names

wlc-utils has **11** `main_*.py` (`git ls-files "py/main_*.py"`). Seven move unchanged, no
collision: `main_accgram.py`, `main_edition_transcription.py`, `main_wlc_json_and_unicode.py`,
`main_wlc_a_notes.py`, `main_wlc_diffs_420422.py`, `main_find_uxlc_accent_changes.py`,
`main_uxlc_grammar_test.py` (keeping this last name keeps `check_repo_standards.py`'s special
case for it true).

The remaining four need work — and **three of them are name collisions with MAM-basics' own
mains**: `main_0_mega.py`, `main_repo_maintenance.py`, and `main_test.py`. The last is resolved
by Phase 3d, which replaces MAM-basics' unittest-registry runner with wlc's `pytest.main()`
wrapper, so one file survives rather than two. The other two are absorbed:

- **`main_update_vendored_files.py` → `main_wlc_vendor_uxlc.py`, gutted.** Its `mb_cmn`/
  `mb_misc`/`mb_diff_mpu` half (~lines 17-22, 59-61, 70-99) syncs into destinations Phase 4
  deletes — dead code. Only the UXLC data half survives (~lines 25-29, 62-65, 100-119):
  `in/UXLC-39` `.xml` and `in/UXLC-misc` `.json` from UXLC-utils with their two `_provenance.md`,
  which feeds `main_find_uxlc_accent_changes.py`. The rename also stops it shadowing MAM-basics'
  own `main_vendoring.py`.
- **`main_0_mega.py` → absorbed into MAM-basics' `main_0_mega.py` `_STEPS` list.** (Name
  collision: both repos have one.) Phase 1 licenses this — the `cwd=repo_root` at line 94 is a
  workaround for the very offenders Phase 1 removes, so once no step depends on cwd the steps can
  run in-process as `StepRecord`s, matching MAM-basics' convention. It also fixes a currently
  invisible bug: accgram reads `MAM-simple/json-vtrad-bhs`, which `main_mam_simple` regenerates,
  and today the two separate megas let accgram silently consume a stale MAM-simple. Append the
  seven wlc steps after `mam-simple`, in their existing order. Each of the five rebuild mains
  gains an `almost_main()`.
- **`main_repo_maintenance.py` → absorbed.** (Also a name collision.) MAM-basics' version gains
  the worktree-cleanup step — bringing the reference implementation home to the repo that
  measures every other repo against it, and which cleans none of its own worktrees today — plus
  Phase 0's ruff step, plus the wlc-utils `.novc` wipe from 3b. Preserve wlc's docstring warning
  about `.novc` having once destroyed a durable result; MAM-basics' equivalent is the complacent
  version ("never a durable result") and wlc's is the one that learned the lesson.

**`force_utf8_io()` is the easy-to-miss break.** Five wlc mains call it only from
`if __name__ == "__main__"`, which stops running once absorbed, and MAM-basics' `main_0_mega.py`
reconfigures nothing (only its `main_repo_maintenance.py` does, in the parent process).
Hebrew-emitting steps will then raise `UnicodeEncodeError` on cp1252 whenever the mega is run
directly. Add `wlc_cmn.utf8_io.force_utf8_io()` at the top of MAM-basics' `main_0_mega.main()`.
Note the two repos use different idioms for this — wlc has the `force_utf8_io` helper, MAM-basics
inlines `sys.stdout.reconfigure` in each main. Consolidating them is reasonable follow-on work,
not part of this effort.

### 3d — Tests

Flip `MAM-basics/py/main_test.py` to a `pytest.main()` wrapper, copying wlc-utils'
`py/main_test.py` — including its docstring explaining why a bare `pytest` fails to collect and
must not be "fixed" with a `conftest.py`, `pytest.ini` `pythonpath`, `.pth` or `PYTHONPATH`.
Delete `TEST_MODULE_SPECS`. Drop wlc's 36 `test_*.py` modules into `py/tests/` alongside
MAM-basics' 34, giving **69 test modules** after the one merge below, plus wlc's
`py/tests/mc_marks.py` helper, which matches no discovery pattern and needs no registration.
Zero test files rewritten. Rewrite MAM-basics' `CLAUDE.md` registry section accordingly.

**Do the flip as its own commit before the copy** — cheap and decisive. From
`C:\Users\BenDe\GitRepos\MAM-basics`, compare the recorded baseline against:

```powershell
.venv\Scripts\python.exe -c "import pytest,sys; sys.exit(pytest.main(['py/tests']))"
```

Counts must match; any divergence is a real finding. One thing to watch: `py/tests/` has no
`__init__.py`, so unittest imports modules as `tests.test_x` while pytest imports them top-level
as `test_x`. Both work given unique basenames — guaranteed once the one collision below is merged.

**Merge the two `test_h_dot_below_nfc.py`** — the only filename collision between the two
`py/tests/` directories (confirm with `comm` over both file lists). Keep wlc's detector: it uses
`tokenize` COMMENT tokens where MAM-basics' uses a naive `line.find("#")`, which false-positives
on `#` inside string literals. Make the merged module scan **both** trees — `paths.repo_root()`
and `wlc_paths.wlc_data_root()` — since wlc-utils' `doc/` and `CLAUDE.md` still carry
hand-authored transliterations after the evacuation. Its `assert len(in_scope) > 100` floor
breaks for a wlc-utils whose in-scope count drops to roughly 18; make the floor per-repo.

**`test_transliterations.py`** newly scans MAM-basics' whole `py/` tree instead of wlc's. A
denylist run over MAM-basics at planning time found **6 hits in 3 files**, all legitimate —
`mb_cmn/hebrew_accents.py`, `mb_cmn/uni_heb.py` (three), `versification_and_cantillation/
strands.py` (two). Re-run rather than trusting that count; each genuine hit gets a
`# translit-ok` pragma per wlc-utils issue #26. Delete the module's
`_VENDORED = {"mb_cmn", "mb_misc", "mb_diff_mpu"}` exclusion — those packages are native in
MAM-basics, not "not ours to normalize", and half the hits hide behind it.

### 3e — Verify (the oracle run)

1. From wlc-utils, run `py\main_0_mega.py`; `git status --porcelain` empty (baseline).
2. **Perturb** — delete `out/accgram/` and `gh-pages/accgram/`. Not optional: without it a mega
   that silently no-ops passes.
3. From `C:\Users\BenDe\GitRepos\MAM-basics` as the working directory:

   ```powershell
   .venv\Scripts\python.exe py\main_0_mega.py
   ```

   then `py\main_find_uxlc_accent_changes.py` and `py\main_wlc_vendor_uxlc.py`.
4. **The oracle:** `git status --porcelain` empty in wlc-utils; in MAM-basics only the new `.py`
   files. Byte-identity across 476 artifacts, produced by code in a different repo from a
   different cwd, is as strong as verification gets here.
5. `py\main_test.py` (expect MAM-basics' recorded baseline plus wlc's, minus whatever the
   h-dot-below merge collapses); `ruff check py` exit 0; `black --check py`.
6. Individually, what the mega does not cover: `py\main_accgram.py generate-html`,
   `py\main_edition_transcription.py build --check` (all committed `.txt` bodies re-derived —
   the check that carried Phase 4 of the sys.path plan), `py\main_uxlc_grammar_test.py`.

Keep this phase to one session, and end it at a clean `git status` in both repos or a
`git checkout -- out gh-pages` in wlc-utils — an interrupted dual-residency window leaves a tree
that may have been written by either copy.

---

## Phase 4 — Empty wlc-utils

*In wlc-utils.* Zero tracked `.py` afterward.

**Delete:** all 267 tracked `.py` and the `py/` tree; `requirements.txt`; `ruff.toml`;
`.githooks/pre-commit` (it runs two test files that have moved — **tell Ben to run
`git config --unset core.hooksPath`** if he ever enabled it, or every commit fails on a missing
script); `.vscode/launch.json` (both configs are debugpy Python launches).

**Rewrite:**

- `.gitignore` — drop `__pycache__/`, `novc_*.py` and `.venv/`; **keep `.novc/`**, which per 3b
  still receives picker pages and `scan_page.py`'s renderings.
- `wlc-utils.code-workspace` — delete the whole `chat.tools.terminal.autoApprove` block; all ~10
  regexes are Python commands, and several already name flags and files that do not exist. Move
  the `../wlc-utils-private` folder entry to `MAM-basics.code-workspace`, which should also gain
  `../wlc-utils`.
- `CLAUDE.md` — most of it is about *code* and moves to `MAM-basics/CLAUDE.md`: the
  `hebrew-prose` skill pointer, the `printed_decalogue_strands.py` rendered-prose pointer, the
  `dir="rtl"` table rule with its `maqaf_nonfinal_accents_page._HEBREW_CELL` reference, "Never a
  loose word", "Maqaf is the last rung" with its `MAQAF_IS_THE_LAST_RUNG` and
  `edition_transcription` citations, and both test sections (reconciling against MAM-basics'
  existing "differential and lint-shaped only" section). What stays in wlc-utils: the
  `doc/agent-planning-principles.md` pointer, the "there is no `wlc-koren-12th` repo" note, and
  **a new opening paragraph stating that this repo contains no Python and that the code
  generating `out/` and `gh-pages/` lives in `../MAM-basics/py/`, naming the entry points.** That
  paragraph is the single most valuable line in the whole evacuation — without it, the next agent
  to open wlc-utils has no way to find its generators.
- `README.md` — currently a Python package tour, and already stale (it advertises a `py/py_hebrew/`
  that does not exist). Replace with: what the data is, which sibling repo generates it, and the
  exact regeneration command.
- `doc/PLAN-sys-path-insert.md` — its Coordination section lists eleven "do not touch, in any
  branch or worktree" files, every one of which has now left the repo. Append a closing note
  recording that the plan completed and its subject files moved, so a future session does not go
  looking for them.

**Not affected:** `.github/workflows/pages.yml` — checkout, configure-pages, upload `gh-pages/`,
deploy. No Python, no `setup-python`, no pip; it works identically before and after. Also
`.gitattributes`, `LICENSE`, `data/`, and all of `doc/`.

**Verify:** `git ls-files "*.py"` prints nothing; then from MAM-basics run the mega and confirm
wlc-utils' `git status --porcelain` is still empty — the tree still regenerates.

---

## Phase 5 — Flip the provenance breadcrumbs

*Deliberately late, and deliberately its own commit.*

`MAM-basics/py/mb_cmn/provenance.py` derives the breadcrumb prefix from
`Path(__file__).resolve().parents[2]` — the repo containing `provenance.py`. After the move that
is MAM-basics, so the breadcrumb would read `MAM-basics/py/accgram/prose_run.py` — except that
`wlc_provenance.py` supplies `REPO_NAME = "wlc-utils"` as a `logical_name` override that rewrites
it back. **Leaving that override alone through Phases 3-4 is precisely what makes byte-identity
the oracle**; flipping it early would bury the move's real diff under ~61 changed files.

From the moment Phase 4 lands, though, the override asserts something false:
`wlc-utils/py/accgram/prose_run.py` no longer exists. The breadcrumb's job is to answer "what
regenerates this file", so it must flip.

Delete `wlc_provenance.py` and revert its ~30 call sites to plain `from mb_cmn import
provenance`, and drop `REPO_NAME` from `wlc_paths.py`. With no override, `_display_path` yields
the MAM-basics path automatically — correct, with no new code.
`py/tests/test_wlc_provenance.py` asserts the exact generated string and is the guard that fires
if this is wrong; update it to the code root.

**Verify:** regenerate, then in wlc-utils `git diff --stat` shows ~61 files at one changed line
each, and the diff body contains nothing but `generated by` lines. Anything else is a bug.

---

## Phase 6 — Disambiguate issue citations

*In MAM-basics only.* **The 88 wlc-utils issues are not transferred** — they keep their numbers
and stay where they are. The trackers unify *going forward*: new issues, including new work on
the moved code, are filed in MAM-basics.

That leaves one thing to fix. The moved code holds roughly **338 bare `#NN` citations**, and once
it sits in MAM-basics a bare `#69` naturally reads as MAM-basics #69 — a different issue. Rule
after the move: in MAM-basics, a bare `#NN` means MAM-basics; anything naming a wlc-utils issue
is written `wlc-utils#NN`.

Not a blind sweep, because both repos have issues in the 1-88 range and the moved code already
cites some genuine MAM-basics numbers (`#187`, `#194`, `#198`, `#201`, `#208`, `#221`, `#246`).
But it is far smaller than 338 sites suggests: the citations cluster hard on a few numbers —
when planned, `#52`×38, `#69`×37, `#36`×31, `#9`×24, `#74`×22, `#81`×19, `#65`×17, `#82`×16,
`#86`×14 — so **resolve each distinct number once**, comparing both repos' issue titles
(`gh issue view <n> --repo bdenckla/<repo>`) against the surrounding comment, then apply
per-number. Roughly 40 judgment calls, then mechanical.

`doc/`, `in/` and `CLAUDE.md` stay in wlc-utils, where a bare `#NN` remains correct — **leave
those ~91 references alone.** Qualifying them would be churn, and would imply they were
ambiguous.

Record the policy in both `CLAUDE.md`s: new issues go to MAM-basics; wlc-utils' 1-88 remain as
they are and are cited with the `wlc-utils#` prefix.

**Verify:** the commit's whole diff is issue-reference text. Spot-check that each distinct
number's resolved target title actually matches what the surrounding comment is about — a wrong
call here produces a plausible-looking lie, which is the only failure mode that matters.

---

## Phase 7 — Cross-repo bookkeeping

*In MAM-basics, plus one repo outside both.* All stale references that would otherwise mislead a
future session; one commit.

1. `in/vendoring_policy.json` — delete the `wlc-utils` entry; its `pkg_scan_roots` names a
   directory Phase 4 deleted.
2. `doc/vendoring-inventory.md` — regenerate with `py\main_vendoring.py --all`; verify the diff
   removes only wlc-utils rows.
3. `py/repo_util/repo_selection.py` — its "the same principle as wlc-utils'
   `repo_paths.require_sibling`" comment is no longer a cross-repo citation; after Phase 2 it is
   `mb_cmn.paths.require_sibling`, one directory away. Rewrite as an internal reference.
4. `py/repo_util/check_repo_standards.py` — retarget the "see wlc-utils' `repo_paths` docstring"
   comment to `mb_cmn/paths.py` and the `worktree_hygiene` reference implementation to
   `repo_util/git_worktree_cleanup.py`. Its dated blame-crawl paragraph and the `_is_test_file`
   docstring both name wlc-utils mains that now live locally — these are dated records, so append
   notes rather than rewriting, per the convention already used for
   `wlc-utils/doc/review-findings-2026-07-29.md`. **And gate the `path_utility`,
   `maintenance_script` and `worktree_hygiene` checks on `_has_tracked_py_files()`** — otherwise
   an emptied wlc-utils reports three false findings permanently. `run_black.py` already models
   this gate.
5. `py/repo_util/run_black.py` — no code change needed; its `_has_tracked_py_files()` already
   makes wlc-utils a legitimate "no tracked .py files" skip. Confirm on the next sweep rather
   than assuming.
6. **Worktree cleanup for wlc-utils becomes homeless.** It will keep accruing worktrees — agents
   still edit `doc/` and `gh-pages/` there — but Phase 4 deleted its maintenance script. Add a
   `--clean-worktrees` action to `py/main_repo_util.py`, alongside `--run-black` and
   `--check-repo-standards`, running `git_worktree_cleanup` across every repo in
   `all-repos.code-workspace`.
7. `all-repos.code-workspace` — leave wlc-utils listed; it still has hundreds of tracked
   non-Python files. `in/repo_maintenance_policy.json` needs no change (wlc-utils is not frozen).
8. **Outside both repos:** the `hebrew-prose` skill at `C:\Users\BenDe\.claude\skills\hebrew-prose\`,
   tracked in the `github-misc` repo at `dot-claude/skills/`. Its description names wlc-utils
   first among the repos it governs, and its file citations —
   `printed_decalogue_strands.py`, `maqaf_nonfinal_accents_page.py`, `MAQAF_IS_THE_LAST_RUNG`,
   `edition_transcription` — all become `MAM-basics/py/accgram/`. A third repo must be committed
   to. **This is the item most likely to be forgotten, because neither repo's tooling can see
   it.** Note the skill's live copy and its tracked copy in `github-misc` do not sync
   automatically; update both.

---

## Risks worth restating

- **The provenance override is load-bearing on ordering** (Phase 5). Do not "fix the now-wrong
  path" mid-move — it destroys the oracle for all ~61 artifacts.
- **`main_0_mega.py:94`'s `cwd=repo_root` masks Phase 1's entire verification.** Exercise the
  steps directly.
- **`force_utf8_io()` silently disappears** when subprocess steps become in-process steps (3c).
- **`in/accgram/uxlc_accent_changes.json` is a tracked file that a program writes**, breaking the
  usual "`in/` is input, `out/` is output" reading, and easy to mistake for hand-authored. It is
  an extra oracle — use it in Phases 1, 3 and 4.
- **MAM-basics' venv may lack `ply`.** Without Phase 0, `import accgram.prose_ply_grammar` fails
  at collection and will look like a move bug rather than a missing dependency. (Both grammars
  build with `write_tables=False`, so no `parser.out`/`parsetab.py` is ever written — nothing to
  gitignore.) **Settled by Phase 0** — `ply` is installed and listed.
- **Ruff version skew reads exactly like a lint regression in the moved code.** Ruff 0.16
  widened its default rule set from four families to roughly forty, which turns an
  unchanged, previously clean tree into hundreds of findings. MAM-basics' `ruff.toml` now
  pins the rule set explicitly (Phase 0); wlc-utils' does not. If Phase 3's `ruff check py`
  suddenly reports in the hundreds, check `ruff --version` and the `select` before reading
  a single finding as a move bug.
- **black version skew.** The two repos' venvs may be on different black versions, and
  wlc-utils' `requirements.txt` never pinned black at all. Run `black --check py` in wlc-utils
  using *MAM-basics'* black before Phase 3; if nonzero, land that reformat in wlc-utils first so
  the move diff stays a pure copy — the same discipline decision 4 applies to ruff.
- **Files change under you mid-session.** Ben edits in parallel; the sys.path plan's last two
  commits landed while this plan was being written. Re-check `git status` and `git log` before
  staging, and commit by hunk rather than sweeping up whatever is in the tree.
