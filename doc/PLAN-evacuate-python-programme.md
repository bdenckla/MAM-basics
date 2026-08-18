# Evacuating Python from the remaining public repos — the programme

Written 2026-08-02, immediately after `doc/PLAN-evacuate-python-from-wlc-utils.md` finished. That
plan is the model and the precedent; this file is the umbrella over the public repos that still
hold Python — **eight hold it, six are in scope** — and it owns the three things no single repo's
plan can own: the scope, the order, and the work that must happen **before** any repo moves.

## Status

| Repo | Plan | State |
|---|---|---|
| Programme Phase 0 — reconcile the three drifted `check_*`/`fix_*` forks | this file | **not started** |
| UXLC-utils | [PLAN-evacuate-python-from-UXLC-utils.md](PLAN-evacuate-python-from-UXLC-utils.md) | **DONE 2026-08-18 — all seven phases.** Phase 1 2026-08-02: `fe73d07` there, `d5a5052` here; Phase 3 2026-08-02: `662db55` and `f202d21` here, nothing there; Phase 4 2026-08-03: `ad52001` there, `2b5c87c` here; Phase 5 2026-08-03: `d5195e3` in codex-index-leningrad, `748ee2f` there, nothing in this repo's `py/`; Phase 6 2026-08-18: `30cdfd2` here, `9be1431` there; Phase 7 items 2–5 2026-08-18, no commit owed. **UXLC-utils holds zero Python** and its 214 artifacts still regenerate byte-identically from here — 213 of them untouched by Phase 6, the one that moved being `gh-pages/fois/index.html`'s breadcrumb, which now names MAM-basics. **Phase 5 dropped codex-index-leningrad's sparse `py/` half rather than repointing it** — the shared decision with the codex-index trio, written into that plan too. Phase 6 prefixed **50 of 57** bare `#NN` citations with `UXLC-utils#` and left 7 bare, so `CLAUDE.md`'s section is now "Three issue trackers"; Phase 7 item 4 deleted a 33 MB orphaned venv holding **832 `.py`**, the shape wlc-utils' Phase 7 warned of at 789. **Item 6 was done earlier, 2026-08-17, github-misc `549224e`.** This row said "Only Phase 6 remains" until the 2026-08-03 review ([#219](https://github.com/bdenckla/MAM-basics/issues/219), major 4) caught the overstatement; corrected 2026-08-04 |
| holman-ketiv-qere | [PLAN-evacuate-python-from-holman-ketiv-qere.md](PLAN-evacuate-python-from-holman-ketiv-qere.md) | **Phases 1 and 3 DONE 2026-08-18. Phases 4, 6 and 7 remain.** Phase 1: `6b10259` there, preceded by `50b2eaa` there (a nine-day-stale artifact, committed first and alone); nothing owed in this repo's `py/`, `mb_cmn/paths.py` already being vendored there and identical, so Phase 2 genuinely does not recur. Phase 3: `1be01b5` here, 60 new files under `py/` plus a modified `py/tests/test_h_dot_below_nfc.py`, with `9e290ce` and `15824d4` in holman-ketiv-qere either side of it — the ruff and UTF-8 preconditions before, the one artifact the `python_modules`→`hkq_cmn` rename reaches after, both deliberate exceptions to "nothing is committed there". **61 files move and only 60 land**, the NFC guard being a third `_Scope` rather than a copy; that scope also needed `.docx` added to `_BINARY_EXTENSIONS`, which holman's copy listed and this repo's did not, so **diff the binary-extension sets as well as the exclusions at every remaining repo carrying that guard**. Suite 905/5 → **950/5**, up by the 45 the seven copied modules collect; 175 of the 335 artifacts rewritten and 160 untouched, matching Phase 1 exactly; row count still 77. **The source-lint crop was 3, not UXLC-utils' 68** — holman's prose is about ketiv/qere rather than accentuation, so budget that cost by subject matter and expect book-of-job and the trio to behave like UXLC-utils instead. **Three of the seven moving entry points had no `sys.stdout.reconfigure` at all**, so UXLC-utils' "the hazard did not materialize" was a fact about that repo's `CLAUDE.md` rather than about the recipe. **Every baseline had moved** — 99 tracked `.py` not 68, 16,416 lines not 11,159, 300 `gh-pages` not 161, 9 entry points not 6, and the oracle is **335 artifacts, not 163**, of which only 175 are rewritten by a full regeneration. A whole second body of work had arrived: Holman's suggested UXLC corrections, extracted from his emails. **The hand-off from UXLC-utils' Phase 7 item 5 was wider than reported** — `py/uxlc_paths.py` is byte-identical and inventory-invisible as described, but so are the packages `py/uxlc_lci/` (4 files) and `py/uxlc_misc/` (5), all five trees named in that repo's `_VENDORED_PACKAGES`/`_VENDORED_FILES`: the pure deletions are **37, not 26**. Four corrections to the plan's own premises, all in its Phase 1 record: the fault was root **conflation** (six `parents[1]` walks) rather than cwd-relative literals, which is the shape to expect in the remaining repos; holman **has** a tracked `CLAUDE.md`, so Phase 4 edits rather than writes one; `py/tests/test_h_dot_below_nfc.py` collides here and differs, wanting a third `_Scope` rather than a copy; and holman brings **13 ruff findings**, a Phase 3 precondition this plan has no Phase 0 for. Phase 3's GitHub question is answered — `gh --repo` is named outright — and exercising that path found a live decomposed-ḥet label defect, left for Ben |
| book-of-job | [PLAN-evacuate-python-from-book-of-job.md](PLAN-evacuate-python-from-book-of-job.md) | **not started** |
| codex-index-aleppo, -leningrad, -cam1753 | [PLAN-evacuate-python-from-codex-index-trio.md](PLAN-evacuate-python-from-codex-index-trio.md) | **not started** — all three, cam1753 included |
| MAM-simple | Appendix A below — **out of scope, nothing to evacuate** | closed, no work |
| diffable-pointed-hebrew | Appendix B below — **out of scope, left alone** | one loose end, see B |

**Every number below was measured on 2026-08-02** with the command given beside it; re-measure
before relying on any of them, and treat a mismatch as a finding rather than as noise. UXLC-utils'
Phase 1 has since moved that repo's own figures — 102 tracked `.py`, 17,932 lines, 22 vendored
`mb_cmn/` — and its plan records why.

**That instruction has now paid twice, and the second time it moved every figure for a repo.**
holman-ketiv-qere re-measured on 2026-08-18, at its `637237b`: **99** tracked `.py` against 68,
**16,416** lines against 11,159, **300** tracked `gh-pages` against 161, **9** entry points against
6, and **37** vendored files against 26 — the extra ten being `uxlc_lci/` (4), `uxlc_misc/` (5) and
`uxlc_paths.py`, all byte-identical and all invisible to `doc/vendoring-inventory.md`. A second body
of work had arrived in the sixteen days between: Holman's suggested UXLC corrections, extracted from
his emails. Its plan's re-measured baselines table carries the detail. **Treat the two repos not yet
measured as stale by a comparable margin**, and note that where holman's copies were merely
miscounted, book-of-job's and the trio's have **diverged**, so a copy the inventory cannot see is
lost work there rather than an accounting error.

---

## Why these six, and why public-only

**The destination is a public repo.** MAM-basics is `PUBLIC` (`gh repo list bdenckla --json
name,visibility`). That single fact settles the scope: Python that lives in a private repo cannot
be moved into MAM-basics without publishing it, so the private Python-heavy repos are out of
scope no matter how taxing they are to maintain. That is not a deferral — it is a different
problem with a different answer, and none of these plans should be read as a step toward it.

Out of scope, with the count that would otherwise have qualified each:

| Repo | Tracked `.py` | Why out |
|---|---|---|
| al-hatorah | 268 | private |
| mgketer | 130 | private |
| MAM-for-CCAR | 69 | private, and frozen (`in/repo_maintenance_policy.json`) |
| MAM-for-JPS | 58 | private, and frozen |
| hbofonts | 38 | private |
| MAM-for-Acc | 29 | private, and frozen |
| masorah-books | 19 | private |
| TMC | 17 | private, and frozen |
| CCAR-Psalms | 6 | private, and frozen |

**al-hatorah is the sharpest exclusion and worth stating plainly**: at 268 tracked `.py` it is
larger than book-of-job and larger than wlc-utils was, it is actively developed, and it vendors
28 `mb_cmn` files by copy script. It is excluded solely because it is private. If the tax of
maintaining Python across repos is what motivates this programme, al-hatorah is the biggest
single instance of that tax and this programme does not touch it. Say so when reporting progress,
so "all the Python is consolidated" is never claimed.

**The different answer now exists — `bdenckla/MAM-private`, created 2026-08-07.** Ben's decision
of that date: a new private repo is the destination for the full contents — not Python-only — of
masorah-books, al-hatorah, wlc-utils-private and mgketer, one top-level directory per source
repo. Its plan is `MAM-private/doc/PLAN-evacuate-private-repos.md`, kept there rather than beside
this file because MAM-basics is public and that plan discusses private repos' internals. Nothing
about this programme changes: private Python still does not move into MAM-basics, and the
al-hatorah paragraph above stands — al-hatorah's evacuation is whole-tree, into MAM-private,
under that plan.

## Scale — measured 2026-08-02

`git ls-files "*.py" | wc -l` and `git ls-files "*.py" -z | xargs -0 wc -l` in each repo:

| Repo | Tracked `.py` | Lines | Vendored `mb_*` | Vendored state | Tracked artifacts (the oracle) | Last commit | Pages workflow |
|---|---|---|---|---|---|---|---|
| book-of-job | 267 | 17,060 | 16 `mb_cmn/` | **DIFFERS** | `gh-pages` 694, `out` 7 | 2026-08-02 | `static.yml` |
| UXLC-utils | 100 | 17,651 | 21 `mb_cmn/` + 3 `mb_diff_mpu/` | identical | `gh-pages` 184, `out` 27, `in` 556 | 2026-08-02 | `pages.yml` |
| holman-ketiv-qere | 68 | 11,159 | 17 `mb_cmn/` + 9 `mb_diff_mpu/` | identical | `gh-pages` 161, `out` 2 | 2026-08-02 | `pages.yml` |
| codex-index-aleppo | 44 | 8,223 | 4 `py/mb_cmn/` + 4 in `aleppo-wiki/py/` | **DIFFERS** | `line-breaks` 35, `column-coordinates` 35, `aleppo-wiki` 26, `ds-flat-stream` 8, `gh-pages` 4 | 2026-08-02 | `pages.yml` |
| codex-index-leningrad | 38 | 4,358 | 4 in `lenin-wiki/py/` | **DIFFERS** | `lenin-wiki` 21 | 2026-07-27 | none |
| codex-index-cam1753 | 22 | 5,386 | 3 `mb_cmn/` | 2 identical, `str_defs.py` **DIFFERS** | `cam1753-col-quads` 28, `cam1753-line-breaks` 27 | 2026-04-27 | none |
| **total in scope** | **539** | **63,837** | | | | | |
| diffable-pointed-hebrew — **out of scope**, Appendix B | 9 | 561 | 8 `mb_cmn/` | **DIFFERS** | none tracked | 2026-04-27 | none |

For comparison, wlc-utils was **267 files / 59,870 lines** in one repo. This programme is the same
volume of code again, spread over six repos with six different shapes — which is why it is four
plans and not one. MAM-basics currently tracks **693** `.py`; it would end near **1,180**.

The vendored-state column is read from `doc/vendoring-inventory.md`, regenerated by
`py\main_vendoring.py --all`. **Every repo whose mechanism the inventory records as `unknown` has
a `DIFFERS` copy, and every repo with a copy script is `identical`** — book-of-job, all three
codex-index repos and diffable-pointed-hebrew on one side; UXLC-utils and holman-ketiv-qere on the
other. That correlation is the single best predictor of how hard each repo will be.

## Decisions carried over from the wlc-utils plan

These four hold here unchanged. Do not relitigate them per repo.

1. **Plain copy, no git history graft.** History stays readable in the source repo, which is not
   going away.
2. **`gh-pages/` stays put indefinitely** in every repo that has one, and so does its Pages
   workflow. Moving it would break links in the wild with no forwarding mechanism. The moved code
   writes back into its old repo as a sibling — already MAM-basics' dominant pattern.

   **Broken once since, deliberately — wlc-utils, 2026-08-17, by
   `doc/PLAN-evacuate-the-rest-of-wlc-utils.md`.** That plan moved wlc-utils' whole `gh-pages/`
   into MAM-basics (nested as `gh-pages/wlc/`, a pure prefix rewrite of every URL) after first
   building the forwarding mechanism this decision says did not exist: each of the 154 published
   pages was replaced in place by a redirect stub naming its successor, plus a `404.html`
   catch-all, generated by `py/main_wlc_redirect_stubs.py`, with every externally cited URL
   re-fetched and verified after the flip. The decision's reasoning stands — do not move a
   `gh-pages/` without a forwarding mechanism — but "indefinitely" is no longer literal, and a
   repo in this programme whose `gh-pages/` is ever to move has that plan's Phases 8–10 as the
   worked, verified shape of the exception.
3. **Regenerating the tracked artifacts byte-identically is the test.** No new example-based unit
   tests. Each plan names its own oracle and the one command that re-establishes it.
4. **Issues unify going forward only.** Existing issues keep their numbers and stay in their own
   trackers; a moved file's bare `#NN` gets a `<repo>#` prefix.

## Two decisions that do NOT carry over

The wlc-utils plan settled these; both are **false for this programme**, and assuming otherwise is
the fastest way to lose code silently.

- **"Flat namespacing, minimal renames — none collide."** That was true of wlc-utils and is
  emphatically not true here. Landing these six repos flat into `py/` would collide on at least
  eleven names, several of them between two source repos rather than against MAM-basics. The
  collisions are enumerated under "Cross-cutting findings" below, and Programme Phase 0 exists to
  resolve the worst family before anything moves.
- **"The vendored copies are pure deletions."** True for UXLC-utils and holman-ketiv-qere, whose
  copies are byte-identical. False for the other five: their `mb_cmn` copies have **diverged**, so
  deleting one destroys whatever local edit it carries. Each affected plan diffs its copies against
  MAM-basics' originals and resolves the differences as a **findings step of its own**, before any
  deletion.

---

## Programme Phase 0 — reconcile the drifted `check_*`/`fix_*` family — BLOCKING

**Three repos carry three forks of the same six scripts, and only one of the six pairs is still
identical.** Measured with `cmp` on 2026-08-02:

| Script | book-of-job | codex-index-aleppo | codex-index-cam1753 | bj vs aleppo | aleppo vs cam1753 |
|---|---|---|---|---|---|
| `check_all.py` | root | `py/` | root | differ | differ |
| `check_mark_order.py` | root | `py/` | root | differ | differ |
| `check_escape_sequences.py` | root | `py/` | root | differ | differ |
| `fix_escape_sequences.py` | root | `py/` | root | differ | differ |
| `fix_mark_order.py` | root | `py/` | root | **identical** | differ |
| `check_word_finding.py` | — | `py/` | root | — | differ |

Two package directories are forked the same way:

- **`py_ac_word_image_helper/`** — 6 files in book-of-job, the same 6 in codex-index-aleppo's
  `py/`. Four are byte-identical (`crop.py`, `flat_index.py`, `hebrew_metrics.py`,
  `linebreak_search.py`); `alef_bet_to_ascii.py` and `codex_page.py` differ.
- **`py_cam1753_word_image/`** — 4 files in book-of-job, the same 4 in codex-index-cam1753. **All
  four differ.**

**Do not move three forks into one repo and sort them out afterwards.** Once they are all under
`py/`, two of the three must be renamed to land at all, the rename hides that they were ever the
same tool, and the divergence becomes permanent. Reconcile first, in the repos where the code
still runs against its own data and a regression is visible.

Phase 0 is therefore its own piece of work, ahead of book-of-job and the codex-index trio:

- **0a — Characterize each divergence.** For all 16 forked files, diff the copies and classify
  each difference as (i) a per-repo constant that belongs in a parameter, (ii) a fix applied to
  one copy and not the others, or (iii) a genuine behavioural difference the repos need. Write the
  classification into this file. **The counts above are the gate**: a re-measure that finds a
  different number of differing files means the tree moved, and the classification is stale.
- **0b — Land one reconciled copy per script, in whichever repo is most active** (book-of-job and
  codex-index-aleppo both had commits on 2026-08-02; codex-index-cam1753 last moved 2026-04-27).
  Each repo's own artifacts are the oracle: regenerate and require a zero diff.
- **0c — Re-run `cmp` and require `identical` across all 16.** Only then is the family one file,
  and only then can it land in MAM-basics once instead of three times.

**Stop and ask Ben if 0a finds category (iii) differences** — genuinely divergent behaviour means
these are not one tool with drift but three tools with a shared ancestor, and the answer is three
differently-named modules rather than one reconciliation. That is a design call, not a step.

## Order

1. **UXLC-utils** — the cleanest, and therefore the one that proves the recipe transfers off
   wlc-utils. Its vendored copies are identical, all its Python is under one `py/`, it has its own
   `CLAUDE.md` stating the conventions, and it already has a `main_0_mega.py` as the oracle
   command. It also has a **downstream consumer** (see finding 2), so doing it first is what
   teaches the trio's plan what a downstream repoint costs.
2. **holman-ketiv-qere** — the same shape, smaller, vendored copies identical. Confirms the recipe
   on a second repo before the expensive one. **Phases 1 and 3 done 2026-08-18; Phases 4, 6 and 7
   remain.** "Smaller" held at planning time and holds less well now: the repo had grown from 68
   tracked `.py` to 99 and from one body of work to two. It still confirmed the recipe, and the
   correction it contributed is the one most worth carrying to steps 4 and 5 — that the thing to
   grep for is a `Path(__file__).resolve().parents[N]` walk conflating the two roots, not a
   cwd-relative string literal.
3. **Programme Phase 0** — must precede both remaining plans.
4. **book-of-job** — the largest, and the one whose Python is not under a `py/` at all.
5. **codex-index trio** — last, and as one plan, because the three share a shape, share the
   reconciled family, and share a vendoring problem.

**One repo at a time, and one phase at a time within it.** Each plan's verification asserts that
MAM-basics' `git status --porcelain` is empty, which a concurrent plan would pollute — the same
reason the wlc-utils plan forbade running its Phases 0 and 1 together.

---

## Cross-cutting findings

**1. Entry-point names collide at MAM-basics' `py/` top level.** MAM-basics already tracks 34
`main_*.py` there. Colliding names among the repos in scope:

| Name | Held by |
|---|---|
| `main_0_mega.py` | MAM-basics **and** UXLC-utils |
| `main_test.py` | MAM-basics, UXLC-utils **and** holman-ketiv-qere |
| `main_update_vendored_files.py` | UXLC-utils, holman-ketiv-qere **and** codex-index-leningrad |
| `main_make_wikisource_page.py` | codex-index-aleppo **and** codex-index-leningrad |
| `main_find_word_in_*_images.py` | codex-index-aleppo, codex-index-cam1753 (differing stems, same job) |

`main_test.py` and `main_update_vendored_files.py` resolve by disappearing: one merged test runner
serves the whole tree, and a repo with no vendored `mb_*` left needs no refresh script.
`main_0_mega.py` and `main_make_wikisource_page.py` need real names, decided in their own plans.

**2. codex-index-leningrad vendors seventeen of UXLC-utils' own `.py`.** Its
`UXLC-utils-sparse/py/` holds `main_uxlc_estimate_atom_loc.py`, five `uxlc_lci/` modules and
eleven `uxlc_misc/` modules, refreshed by codex-index-leningrad's own
`main_update_vendored_files.py` from the sibling `../UXLC-utils`. **The vendoring inventory does
not record this**: it lists only `mb_cmn` rows for that repo, because the scan looks for
MAM-basics packages. Evacuating UXLC-utils' Python breaks that script's source. Handled in
UXLC-utils' plan; flagged here because the inventory alone will not reveal it, and because it is
evidence that a second such relation may exist somewhere the scan cannot see.

**That last clause came true twice, and the blind spot is bigger than "a loose file at the top of
`py/`."** UXLC-utils' Phase 7 item 5 found holman-ketiv-qere's `py/uxlc_paths.py` byte-identical to
this repo's and absent from the inventory, and reported it as the loose-file case: a scan looking for
`mb_*` packages cannot see a single file. holman's Phase 1 then found, 2026-08-18, that **two whole
packages are invisible on the same tracker for the same reason** — `py/uxlc_lci/` (4 files) and
`py/uxlc_misc/` (5), both named in that repo's `_VENDORED_PACKAGES` and both synced from
`../MAM-basics`. So the mechanism is not "loose files escape" but **`in/vendoring_policy.json`'s
`pkg_scan_roots` is a hand-maintained list with no cross-check against what the destination repo's
own sync script names**, exactly the failure mode a hand-maintained test registry has. **The check
worth running per repo before its Phase 4 is to read that repo's `main_update_vendored_files.py` and
compare its `_VENDORED_PACKAGES` and `_VENDORED_FILES` against the inventory's rows** — not to trust
the inventory, and not to grep for `mb_*`. For holman it cost only an undercount, 26 against 37, all
37 identical; in book-of-job and the trio the copies have **diverged**, so there the same blind spot
would destroy a local edit.

**Resolved 2026-08-03 in UXLC-utils' Phase 5: the `py/` half was dropped, not repointed**
(`d5195e3` in codex-index-leningrad, `748ee2f` in UXLC-utils). What settled it is worth carrying:
**nothing in the consumer imported the seventeen**, and their one entry point could not run there
anyway — the sparse copy never carried `mb_cmn`, so it raised `ModuleNotFoundError` long before
Phase 4. Three findings that will recur at the next downstream consumer:

- **A vendored copy can be dead without anyone noticing, and "it works today" is worth
  checking rather than assuming.** Both plans described this one as working, on the strength of a
  sync script that refreshed it. Run the consumer's entry point before deciding what its copy is
  worth.
- **The broken script failed loudly but partially.** `copy_by_intersection(strict=True)` raises on
  the first missing source file, and it iterates in sorted order — so `data/` and `in/` were
  copied and `provenance.md` was never written. Expect a half-sync, not a no-op.
- **The consumer's prose named the moved code in four files, none of which imported it** —
  `README.md`, `.github/copilot-instructions.md`, `.vscode/launch.json` and a test module's scope
  docstring. **Grep a consumer for the vendored directory's name**, not for the module names.

**3. Every repo in scope uses cwd-relative repo-internal paths**, which is the same problem
wlc-utils' Phase 1 solved. Representative hits: UXLC-utils `py/clc/clc_render.py:26`
`_OUT_DIR = "gh-pages/clc"` and `py/clc/clc_changes.py:27` `_CHANGES_DIR = "in/UXLC-misc"`;
book-of-job `pyauthor/job1_full_list_details.py:15` `out_dir = f"gh-pages/{D1D_DIR}"`;
holman-ketiv-qere `py/main_just_render_table.py:20` `Path("gh-pages/table_data_findings.html")`;
codex-index-aleppo `aleppo-wiki/py/mam_book_names.py:114` `f"in/mam-ws/{basename}.json"`. Each is
a path that resolves correctly only while the process runs from that repo's root, which is exactly
what stops being true. **`repo_root()` splitting into a CODE root and a DATA root is the organizing
idea of every plan here, as it was of the wlc-utils one** — read that plan's section of that name
before starting any of these.

Three things UXLC-utils' Phase 1 learned about this, all likely to recur:

- **A grep for leading `"in/` and friends undercounts badly.** Six known offenders there turned
  out to be 26 modules, because the same path also arrives as an f-string, as a module constant
  another module imports, as a `Path("...")` binding, and as a
  `Path(__file__).resolve().parent.parent` walk that is cwd-independent already but still
  conflates the two roots. Grep for the directory *names* anywhere in the line, not for a leading
  quote.
- **`PurePosixPath(...).name` breaks the moment a path goes absolute on Windows** — it sees no
  separator in a backslashed path and returns the whole string. Three modules used it to derive a
  link's `href` from an output path, so the failure is a wrong artifact rather than a crash.
  `git grep -n PurePosixPath` in each repo before starting.
- **`mb_cmn/paths.py` may not be in the destination repo's vendored subset**, in which case the
  accessor Phase 2 is said to have already provided is not reachable from the code that needs it.
  Finding 3 above assumes it is; check.

Five more from UXLC-utils' **Phase 3**, all of which will recur:

- **A file inside a vendored `mb_*/` directory need not be a vendored copy.** UXLC-utils'
  `py/mb_cmn/mb_cmn_bib_locales.py` is MAM-basics' `bib_locales.py` plus six local aliases,
  absent from the inventory's row for that repo and excluded from its own sync script by name.
  Copied in as-is it would have put a 636-line near-duplicate of a native module inside
  `py/mb_cmn/` — the two-module-objects failure the global `CLAUDE.md` describes, reached without
  any `sys.path` line. **`cmp` every file in a vendored directory against MAM-basics' own and
  treat "no counterpart here" as a finding, not as a new file to copy.**
- **Grep for cross-references to a renamed entry point by MODULE NAME, not by path.**
  UXLC-utils' `main_uxlc_download_changes.py` ended with `import main_0_mega; main_0_mega.main()`,
  a name that exists in both repos — so after the move it silently ran MAM-basics' tree-wide
  pipeline instead of the UXLC one. It succeeds; nothing fails. Any repo whose mega gets renamed
  has this.
- **A repo's copy of `nfc_h_dot_below_test.py` must merge, not move.** It finds its repo root by
  `git rev-parse` from its own file's location, so under MAM-basics' `py/tests/` it scans
  MAM-basics — a second, weaker pass over this tree, and a failing one. Add a `_Scope` to
  `py/tests/test_h_dot_below_nfc.py` instead; it now carries three.
- **Budget for this repo's lints scanning the arrived code.** UXLC-utils' 77 files produced 68
  genuine findings — 15 prose-convention and 53 transliteration — of which roughly half were our
  own wording to fix and half external vocabulary needing a `# translit-ok` pragma. Plus two
  ruff findings, in a repo that runs no linter. This was the largest single piece of Phase 3's
  work, larger than the copy itself. **And the traffic runs both ways**: UXLC-utils' arriving
  `source_hygiene` checker found eight orphan combining marks in *MAM-basics'* own tree.
- **Count what a run actually rewrites, not what it leaves clean.** An empty `git status` across
  an artifact tree proves nothing about files no program writes. Snapshot mtimes before the run:
  of UXLC-utils' 214 tracked artifacts only **127** were rewritten, the other 87 being static
  assets and one hand-authored report filed under `out/`. Phase 1's write-up had claimed all of
  them regenerated.

**3a. Live downloads are untestable and that is deferred, not owed.** tanach.us' `robots.txt`
disallows both paths UXLC-utils' two downloaders need, so Phase 3 there could not run either;
`polite_download` is configured `obey_robots_txt=True` and that was not worked around. **Ben's
decision, 2026-08-02: testing anything that requires a live download is deferred, and does not
block completion of this programme.** The loop closes at MAM-basics **#214**, which waits on a
separate task drafting an email to Chris Kimball, tanach.us' maintainer. The account is in
UXLC-utils' plan, Phase 3.

Whether the same exposure recurs was checked on 2026-08-03, by grepping the other four repos in
scope for `polite_download`, `robots`, `requests`, `urlopen` and `urllib`. **It does not — the
robots block is specific to `polite_download` against tanach.us, and `polite_download` is used
only in MAM-basics and UXLC-utils.** What the other repos do have, so nobody re-checks:

| Repo | Downloader | Shape |
|---|---|---|
| book-of-job | **none for source data** | its one network path is `check_html_syntax_and_sanity.py --w3c`, which POSTs generated HTML to `validator.w3.org/nu` behind an opt-in flag. `mb_cmn/uxlc_change_url.py` composes a tanach.us href for a link and downloads nothing. |
| codex-index-aleppo | `py/download_aleppo_pages.py` | page images from archive.org by raw `urlopen`; run by hand, and three modules only print "Run download_aleppo_pages.py" when the images are absent |
| codex-index-cam1753 | `download_cam1753_spreads.py` | the same shape against archive.org, and **nothing in that repo calls it** |
| codex-index-leningrad | **none** | `lenin-wiki/py/image_urls.py` composes sefaria and archive.org hrefs for links |
| holman-ketiv-qere | **none** | |

So the two archive.org downloaders cannot raise `RobotsDisallowedError` — they consult no
`robots.txt` at all. **They are nevertheless as unexercised as the tanach.us pair**, and the
finding that matters transfers unchanged: a downloader writing into the wrong repo's `in/` is the
failure the two-roots work exists to prevent, and composing the right path is not the same as
writing to it. Each affected plan should say plainly which of its downloaders it has and has not
run, rather than letting an empty `git status` stand in for the claim.

Four more from UXLC-utils' **Phase 4**, all of which will recur:

- **The `in/vendoring_policy.json` edit belongs to the DELETING phase, not to bookkeeping.** Every
  plan here files it under its own Phase 7, on the wlc-utils precedent — but wlc-utils' Phase 7
  also added `py/tests/test_vendoring_policy_paths.py`, whose whole job is to fire the moment a
  configured `pkg_scan_roots` directory vanishes. It duly failed inside UXLC-utils' Phase 4
  verification run, the first red suite of the programme, and the entry had to come out before the
  phase could pass. **Move the item into each remaining plan's deleting phase**, and regenerate
  `doc/vendoring-inventory.md` and the three `out/vendoring_*` artifacts in the same commit.
  Expect the suite's pass count to drop by exactly the number of parametrize cases that repo's
  entry contributed — three for UXLC-utils, so 916 → 913.
- **The tracked deletion is bigger than the `.py` count, and the surplus is repo-specific.**
  UXLC-utils' 102 `.py` came to 110 tracked files: plus `requirements.txt`, the two
  `_provenance.md` vendoring breadcrumbs sitting *inside* the vendored packages, `.vscode/`
  (debugpy launches and a venv auto-approve), and `.github/copilot-instructions.md`, the Copilot
  twin of `CLAUDE.md` and ~95% Python conventions. **Inventory each repo's non-`.py` Python
  scaffolding before quoting a deletion count to Ben.** And `git rm` leaves the untracked half
  behind — 217 `__pycache__`/`.pytest_cache` files here — so delete the source root outright
  afterwards, or the repo still looks like it has Python.
- **A repo's own `doc/` links at its own `py/`, and those links go dangling.** `doc/clc-design.md`
  stays in UXLC-utils by design, and 35 of its markdown links name 19 `py/…` paths this phase
  deleted. Ben's call was one sentence in `CLAUDE.md` — every `py/…` path in `doc/` now means
  `../MAM-basics/py/…` — rather than 35 edits riding along on a deletion commit, with the one file
  that did *not* move called out by name. **Grep each repo's `doc/` for `](py/` before the
  deleting phase**, decide which way, and say so in the plan rather than discovering it mid-commit.
- **Do not move a convention into MAM-basics' `CLAUDE.md` that MAM-basics already practices.**
  Each plan says the evacuated repo's conventions "move to MAM-basics' `CLAUDE.md` with the code
  they govern". For UXLC-utils that was true of none of them: the MAM-reading rule is already how
  thirteen modules here read MAM, the vendoring rules have no meaning in the vendoring *source*,
  and the entry-point and `sys.path` rules are already in this repo's `CLAUDE.md`. **Check what is
  already there and already practised before copying prose across**; a wholesale restoration is
  the failure mode Ben's standing note on this file's minimality warns about.

**4. book-of-job has no `py/`, so its modules land at MAM-basics' `py/` top level.** Sixteen
scripts sit at its repo root and seven more in a `py/` that is a package of page-rendering helpers
rather than a source root. Two of those seven are `hebrew_letter_words.py` and
`uni_heb_char_classes.py`; MAM-basics already has `mb_misc/hebrew_letter_words.py`. Landing
book-of-job's copy as a **top-level** `hebrew_letter_words` alongside `mb_misc.hebrew_letter_words`
produces two module objects for one name — the failure mode the global `CLAUDE.md` describes under
the `sys.path` ban, reached here without any `sys.path` line at all.

**5. Four of the six in scope were committed to on 2026-08-02, and one has not moved since
2026-04-27.** book-of-job, UXLC-utils, holman-ketiv-qere and codex-index-aleppo are live;
codex-index-leningrad last moved 2026-07-27 and codex-index-cam1753 is dormant. **Dormancy is not
a reason to treat a repo differently** — see the codex-index trio's plan, where cam1753 is in on
exactly the same terms as the other two. **Files change under you mid-session** — Ben edits in
parallel, and wlc-utils moved under the wlc-utils plan's own final session. Re-check `git status`
and `git log` before staging, and commit by hunk.

---

## Appendix A — MAM-simple: nothing to evacuate

MAM-simple tracks 47 `.py`, which would put it fifth in the scale table. **43 of them are already
generated by MAM-basics** — `py-examples/mb_cmn` (18), `py-examples/mb_misc` (14),
`py-examples/mb_sefaria` (7) and `py-examples/osis` (4), all recorded `identical` /
`copy_script` / `generated` in `doc/vendoring-inventory.md`. They are the published artifact of
that repo, not code maintained there, and evacuating them would delete the product.

The other four are `py/tests/test_h_dot_below_nfc.py` and the three
`py-examples/main_*_example.py`, which the inventory's "Intentionally non-vendored" table already
declares are maintained in MAM-simple on purpose. **This repo is closed for this programme.** Its
`.py` count should not be read as Python awaiting evacuation, and a future audit that reads it that
way should be pointed here.

## Appendix B — diffable-pointed-hebrew: left alone, with one loose end

Nine tracked `.py`, of which **eight are a vendored `mb_cmn`** and one is the repo's entire reason
to exist, `diffable-pointed-hebrew.py` at the root. Nineteen tracked files in total, no `out/`, no
`gh-pages/`, no Pages workflow, dormant since 2026-04-27.

**Out of scope, on the same principle as MAM-simple. Ben, 2026-08-02:** a thin script — or a
handful of them — that exists only in a non-MAM-basics repo, combined with vendored files, is a
repo to leave alone, *"as long as its vendoring is all nicely set up like vendoring in other
repos"*. That is the criterion, and it is a better one than the draft's "is this worth the
trouble", because it names the property that makes a small Python repo cheap rather than guessing
at effort.

**This repo does not currently meet that criterion, and that is the loose end.** Its eight
`mb_cmn` files are recorded **`DIFFERS`** in `doc/vendoring-inventory.md`, with mechanism
`unknown` — meaning no copy script has ever refreshed them and nobody has looked at how far they
have drifted. Compare holman-ketiv-qere, whose copies are `identical` and `copy_script`: that is
what "nicely set up" looks like.

So the work here is not an evacuation but a **vendoring repair**, and it is small:

1. Diff the eight against MAM-basics' current `py/mb_cmn/` and classify each difference — a fix
   that belongs upstream, a local adaptation, or drift to drop.
2. Give the repo a `main_update_vendored_files.py` copying by intersection, matching the four
   repos that already have one.
3. Update `in/vendoring_policy.json` to declare the mechanism, and regenerate the inventory. The
   row should then read `identical` / `copy_script`.

Worth doing on its own account whichever way the scope question had gone: a divergence nobody has
looked at is a bug of unknown size. It is not blocked by anything in this programme and does not
block anything in it.

---

## How to run this programme

Same discipline as the wlc-utils plan, and for the same reason: **no live session stays open, and
no session needs to remember anything from the one before it.**

Each session reads the relevant plan, does exactly **one** phase, verifies it, and writes the
result back into that plan's Status table — state, date, commit shas — and marks the phase heading
`— DONE <date>`, recording the numbers actually measured and anything the plan did not predict.
Then it updates this file's Status table, and spawns a task chip for the next phase quoting the
plan's absolute path. A phase whose result is not written back cannot be judged by the next
session.

**Run the test suite and every generator from each repo's own main checkout, never from a
worktree.** The wlc-utils plan's Phase 7 cost a full pass to this: from
`.claude/worktrees/<name>`, MAM-basics' suite gives 12 failures that are not real, and generators
are worse than broken — they succeed and write the worktree's directory name into the provenance
breadcrumbs.
