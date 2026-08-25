# Evacuate all Python from holman-ketiv-qere into MAM-basics

Written 2026-08-02. Governed by [PLAN-evacuate-python-programme.md](PLAN-evacuate-python-programme.md).
**Second in the order**, after UXLC-utils: the same shape, smaller, and its job is to confirm the
recipe on a second repo before the expensive ones. Read
[PLAN-evacuate-python-from-UXLC-utils.md](PLAN-evacuate-python-from-UXLC-utils.md) alongside this —
where the two agree, that file carries the reasoning and this one does not repeat it.

## Status

| Phase | State |
|---|---|
| 1 — two roots, no cwd | **DONE 2026-08-18** — `6b10259` in holman-ketiv-qere (12 files, +275/−51), preceded by `50b2eaa` there; nothing owed in this repo's `py/` |
| 3 — copy the Python in (dual residency) | **DONE 2026-08-18** — `1be01b5` here (60 new files, 1 modified); in holman-ketiv-qere `9e290ce` before it and `15824d4` after, both deliberate exceptions to dual residency. Suite 905/5 → **950/5**; 175 of 335 artifacts rewritten, 160 untouched, row count 77 |
| 4 — empty holman-ketiv-qere | **DONE 2026-08-18** — `0890cb8` in holman-ketiv-qere (111 files, +121/−16,838) and `b72f785` here. **holman-ketiv-qere holds zero Python.** 107 tracked files deleted, not 104: the 100 `.py`, **five** `_provenance.md`, `py/.gitignore` and `.vscode/settings.json`. Oracle run twice, before and after the deletion, 175/160 both times; row count still 77. Suite 950 → **947**, three tests and not two. **Phase 7 item 1 is done inside this phase**, the scan-root guard having fired the moment the directories went |
| 6 — breadcrumbs and issue citations | **DONE 2026-08-18** — `4e9d809` here (the generator), `ce6dd7d` in holman-ketiv-qere (three artifacts), and a `CLAUDE.md` commit after them. The five stale paths flipped, exactly the five Phase 4 named, in two shapes the artifacts themselves settled. **Not one bare `#NN` needed prefixing**: holman-ketiv-qere's Python never cited its own tracker, so no citation was rewritten in either repo. `CLAUDE.md` is now **"Four issue trackers"** — 81 issues, 1–81, 60 open, the whole range colliding. 175/160 and `row_count` 77 unchanged; suite still 947/5 |
| 7 — cross-repo bookkeeping | **DONE — item 1 2026-08-18** in `b72f785`, with Phase 4; **items 2–5 2026-08-19**. Item 2 and item 3 confirmed, both of item 3's strings verbatim as UXLC-utils returned them. Item 4 deleted a 22 MB venv after a clean junction check, `--clean-worktrees` having run first and found nothing. **Two findings.** Finding 1: `doc/holman-manuscript-citations.md`'s closing line named holman-ketiv-qere's **own** venv, the one tracked site item 4's safety check said would not exist — Phase 4 had rewritten all three `py/…` paths in that same file but a `.venv` path carries no `py/` prefix, so it was invisible to the grep Phases 4 and 6 both swept with. Fixed in `6b0bb63` there, one line, and **the plan's only holman-ketiv-qere commit of this phase**, where UXLC-utils' Phase 7 needed none. Finding 2, **left for Ben**: MAM-private's `mgketer/documentation/mpu-parsing.md` and its generated `out-reports/mpu-parsing.html` carry four live cross-references to `holman-ketiv-qere/py/python_modules/…`, stale twice over. **Finding 3**, about this plan's own bookkeeping: the `59 subtests` figure Phases 3, 4 and 6 all record does **not** reproduce — `pytest-subtests` is not installed, so pytest cannot report it; the two substantive counts match exactly, so **drop the third figure** and record the suite as 947 passed / 5 skipped. 175/335 and `row_count` 77 unchanged; suite still 947/5 |

Phase 2 does not recur — **and confirmed 2026-08-18 for the right reason, which is not the one this
line first gave.** That `mb_cmn/paths.py` has `sibling_repo()` and `require_sibling()` is a fact
about MAM-basics and settles nothing: UXLC-utils' Phase 1 discovered that those functions were not
*reachable* from the source repo, whose vendored `py/mb_cmn/` held 21 files and not that one, so its
Phase 1 had to vendor `paths.py` in first. holman **does** already vendor it, byte-identical, and
its two consumers here import it directly. Check reachability rather than existence in the remaining
plans.

Phase 5 has no analogue here: nothing vendors this repo's Python.

## Baselines — RE-MEASURED 2026-08-18, and every figure had moved

**Do not use the 2026-08-02 column.** Phase 1 re-measured at holman-ketiv-qere `637237b`
(2026-08-12), clean tree, and a whole second body of work had arrived meanwhile: Holman's
suggested UXLC corrections, extracted from his emails and rendered to
`gh-pages/uxlc_corrections.html`. The README describes both halves.

Every 2026-08-18 figure is the state **before** Phase 1, at `637237b`, so that it is a baseline
rather than a result. Phase 1 then added one file, `py/hkq_paths.py`: **Phase 3 and Phase 4 face 100
tracked `.py`, not 99.**

| Measure | 2026-08-02 | 2026-08-18 | |
|---|---|---|---|
| tracked `.py` | 68 | **99** | +31 |
| lines | 11,159 | **16,416** | +5,257 |
| tracked `gh-pages` | 161 | **300** | +139 |
| tracked `out` | 2 | **2** | matches |
| tracked `docs-not-served` | (not counted) | **4** | |
| test modules under `py/tests/` | 8 + `py/main_test.py` | **8** + `py/main_test.py` | matches |
| entry points | 6 `py/main_*.py` | **9** `py/main_*.py` | +3 |
| tracked total | (not counted) | **454** | |

Three packages that did not exist at planning time — `py/uxlc_misc/` (5), `py/uxlc_lci/` (4),
`py/uxlc_comments/` (3) — plus the loose `py/uxlc_paths.py`. Three new entry points:
`main_estimate_uxlc_locations`, `main_ingest_uxlc_emails`, `main_render_uxlc_corrections`.

**The oracle is 335 tracked artifacts, not 163**, across six trees: `gh-pages` 300, `emails` 26,
`docs-not-served` 4, `out` 2, `data` 2, `io` 1. Of those, **175 are actually rewritten** by a full
regeneration and **160 are untouched** — see Phase 1's record for that list, which is what Phase 4
must name. The README still fixes the ketiv/qere scope sharply: exactly **77 rows** are expected in
`docs-not-served/table_data.json`, and a regeneration that changes the row count is a failure, not
a finding. Confirmed at 77 on 2026-08-18.

Regenerating everything is **six commands, not one**. The README's own command covers the
ketiv/qere half only:

```powershell
.venv\Scripts\python.exe py/main_extract_docx_and_render_table.py
.venv\Scripts\python.exe py/main_ingest_uxlc_emails.py
.venv\Scripts\python.exe py/main_estimate_uxlc_locations.py
.venv\Scripts\python.exe py/main_render_uxlc_corrections.py
.venv\Scripts\python.exe py/main_search_holam_he_qere.py
.venv\Scripts\python.exe py/main_search_final_hiriq_verse_text.py
```

`main_ingest_uxlc_emails` needs the untracked mailbox at `.novc/eml/` (13 messages, present
2026-08-18) and `main_estimate_uxlc_locations` needs the sibling UXLC-utils clone;
`main_just_render_table` re-renders a subset of the first command's output and is not needed for a
full pass.

**This repo's venv has black but NO pytest**, checked 2026-08-18 — `py/main_test.py` is a
`unittest` loader, so nothing there needs it. That makes a fourth repo in that shape, alongside
mgketer, book-of-job and codex-index-aleppo. Its ruff comes from **this** repo's venv, holman
having none.

## What moves, and what is a pure deletion

**Re-counted 2026-08-18 by Phase 1.** Every row below had grown, and the pure deletions were
undercounted by ten because the inventory cannot see three of the five vendored trees.

| Directory | 2026-08-02 | 2026-08-18 | Disposition |
|---|---|---|---|
| `py/py_render/` | 14 | **19** | moves as-is — name confirmed free in this repo's `py/` |
| `py/python_modules/` | 14 | **23** | moves, **renamed** to `hkq_cmn/` — below |
| `py/uxlc_comments/` | (did not exist) | **3** | moves as-is — name confirmed free |
| `py/tests/` | 8 | **8** | folds in, but **one of the eight collides and differs** — below |
| `py/main_*.py` | 6 | **9** | moves, less two that disappear |
| `py/hkq_paths.py` | (did not exist) | **1** | moves — Phase 1 wrote it; one line changes at the move |
| `py/mb_cmn/` | 17 | **18** | **pure deletion** |
| `py/mb_diff_mpu/` | 9 | **9** | **pure deletion** |
| `py/uxlc_lci/` | (not listed) | **4** | **pure deletion** |
| `py/uxlc_misc/` | (not listed) | **5** | **pure deletion** |
| `py/uxlc_paths.py` | (not listed) | **1** | **pure deletion** |

**The pure deletions are 37, not 26, and all 37 are byte-identical** to this repo's originals by
`cmp`, checked 2026-08-18. `doc/vendoring-inventory.md` records only two of the five trees —
`mb_cmn` (18 files) and `mb_diff_mpu` (9) — because `in/vendoring_policy.json`'s `pkg_scan_roots`
for this repo declares only those two. `uxlc_lci`, `uxlc_misc` and `uxlc_paths.py` appear **nowhere**
in the inventory, though holman's own `py/main_update_vendored_files.py` names all five: the first
four in `_VENDORED_PACKAGES` and `uxlc_paths.py` in `_VENDORED_FILES`, synced from `../MAM-basics`.
This is the programme's cross-cutting finding 2 recurring, and it is wider than the hand-off from
UXLC-utils' Phase 7 item 5 described — that hand-off named the one loose file, and the two packages
are invisible for the same reason. **Re-confirm with `cmp` immediately before deleting anyway.**

The arithmetic, against the 100 tracked `.py` holman has after Phase 1 added `hkq_paths.py`: 37 are
pure deletions, leaving 63; `main_test.py` and `main_update_vendored_files.py` disappear, for the
reasons UXLC-utils' plan gives; so **61 files land here**. Eight of those 61 are tests folding into
this repo's existing `py/tests/`, and one of the eight needs a decision rather than a copy — below.

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

## Phase 1 — two roots, no cwd — DONE 2026-08-18

**Landed as `6b10259` in holman-ketiv-qere (12 files, +275/−51). Nothing was owed in this repo's
`py/`** — unlike UXLC-utils' Phase 1, which had to vendor `mb_cmn/paths.py` in first. It is already
there in holman and byte-identical, so the Phase-2-does-not-recur conclusion **does** hold for this
repo. Check it per repo in the remaining plans regardless; UXLC-utils' Phase 1 record says why.

**One commit came first, deliberately alone: `50b2eaa`, regenerating
`out/holam_he_qere_report.json`.** That tracked artifact was nine days stale. `27294af` (2026-08-09)
re-vendored `py/mb_cmn/template_names.py` from this repo, where the ketiv/qere template names had
been respelled with U+05F4 HEBREW PUNCTUATION GERSHAYIM in place of an ASCII double quote, and
nothing regenerated the report afterwards; it was last written 2026-04-27. The whole diff is that
one substitution in two names, `כו״ק` and `מ:קו״כ-אם-2`, 62 lines each way, with every hit count and
every vowel-only form identical. Committing it before touching a path is what gave Phase 1 a clean
oracle — the same move UXLC-utils' Phase 3 made with `662db55`.

**The verification passed as specified.** From `C:\Users\BenDe\GitRepos\MAM-basics` as the working
directory, each entry point by absolute path on holman's own interpreter: all six generators, then
`main_just_render_table`, then `main_test`. Afterwards holman held nothing but the twelve `.py`
files, and **MAM-basics, UXLC-utils and MAM-parsed were all clean** — so the 335 artifacts came back
byte-identical from a foreign cwd and nothing was written into the wrong tree. Suite **51 tests,
OK**, unchanged from the pre-change baseline. `black` clean on all twelve files.

Nine things went differently from what is written underneath. The first four bear on later phases:

- **The fault was root CONFLATION, not cwd-relativity, and the plan's grep could not have found
  most of it.** `main_just_render_table`'s two argparse defaults were the only genuinely
  cwd-relative literals in the repo. What actually broke the move was that each of the six
  generators had its own `Path(__file__).resolve().parents[1]`, spelled `REPO_ROOT`, and composed
  **both** data paths (`REPO_ROOT / "gh-pages"`) and sibling-repo paths (`REPO_ROOT.parent /
  "MAM-parsed"`) off that one value. Those are cwd-independent already — which is exactly why a
  grep for a leading quote misses them — and after the move the data ones resolve silently into
  MAM-basics' tree. Two library modules had the same shape at `parents[2]`
  (`python_modules/qere_ending_search.py`, `python_modules/table_row_github_issues.py`) and a third
  at `parents[2] / "assets"` (`py_render/rt_assets.py`). **Expect this shape rather than string
  literals in book-of-job and the codex-index trio**, and grep for `parents[` as well.
- **`py/tests/test_h_dot_below_nfc.py` collides with this repo's file of the same name and the two
  DIFFER** — 304 lines there against 433 here. Do not merge them and do not copy holman's over.
  This repo's version already scans **two repos** through a `_scopes()` function, one `_Scope` per
  tree with its own exclusions and floor, and the UXLC-utils scope is rooted at
  `uxlc_paths.uxlc_data_root()`. **Phase 3's move is therefore to add a third `_Scope` rooted at
  `hkq_paths.hkq_data_root()`, and delete holman's copy** — which is what UXLC-utils' Phase 3 did
  with its own near-copy, `py/repo_hygiene/nfc_h_dot_below_test.py`. Simply dropping holman's copy
  without adding the scope would silently end NFC linting over that repo's hand-authored
  non-Python files: `doc/` (2), `README.md`, `CLAUDE.md`, `docs-not-served/table_data_fields.md`
  and the 26 files under `emails/`. Pick the floor the way the UXLC-utils scope's comment explains.
- **Phase 4's premise is wrong: holman-ketiv-qere HAS a tracked `CLAUDE.md`.** It has five
  sections, and one of them is load-bearing — the public-repo boundary that keeps every email
  address out of a tracked file, `.eml` files living untracked in `.novc/eml/` while
  `main_ingest_uxlc_emails.py` writes an address-free derivative under `emails/`. Phase 4 does not
  write that file from nothing; it **edits** it, and the address boundary and the `light-dark()`
  CSS convention must survive intact. Its "Vendor whole files" section is the one that goes.
- **The oracle is 335 artifacts and only 175 of them are regenerated at all.** An mtime snapshot
  immediately around a full six-command run, taken from both working directories with the same
  result, shows **175 rewritten and 160 untouched**. The 160 are the list Phase 4 must name: **154
  `gh-pages/img/`**, `gh-pages/index.html`, the two `gh-pages/JC3 ...` pages,
  `gh-pages/woff2/Taamey_D.woff2`, `docs-not-served/table_data_fields.md` and
  `io/table_row_github_issues.json`. The 154 are untouched **by design** —
  `extract_docx_xml_utils.export_images` is write-once and raises rather than overwrite an image
  whose bytes differ, with three Aleppo crops named in `PRESERVED_EXTRACTED_IMAGE_PATHS` exempted
  as manual replacements. So for that tree the oracle's proof is indirect and stronger than a diff:
  a wrong root produces 154 files where nothing tracks them, and MAM-basics' working tree stayed
  empty.
- **Phase 3's GitHub question is answered, positively.**
  `python_modules/refresh_table_row_github_issues.py` passes `--repo bdenckla/holman-ketiv-qere` to
  `gh issue list` from constants in `table_row_github_issues.py`, so the tracker is named outright
  and no working directory picks it. Nothing authenticates through anything cwd-dependent. **A tool
  silently reading the wrong tracker is not a risk here**, and the constants stay as they are after
  the move, the issues being about the review holman holds.
- **Exercising that refresh found a live defect, and it is the one write the artifact oracle never
  covers — RESOLVED 2026-08-18, no commit owed here.** `main_just_render_table --update-issue-metadata`
  was broken by a Unicode form mismatch: the GitHub label spelled its ḥet **decomposed**,
  `U+0068 U+0323`, where `ISSUE_LABEL_TO_TAG` has the precomposed `U+1E25` that this repo's NFC
  convention requires, so the lookup missed and the refresh dropped the `holam-he` tag from 7 of the
  77 rows (rows 21, 22, 34, 36, 49, 75, 76 — issues 40, 27, 41, 42, 63, 71, 72). (This read "8 of
  the 77 rows", as `6b10259`'s message does, until the 2026-08-22 review's follow-up, while listing
  these same seven issues; `grep -c holam-he io/table_row_github_issues.json` is 7. The tracker's
  `ḥolam he` label is on eight issues, the eighth being #81, which maps to no row.) Nothing wrong shipped: `py_render/rt_html.py`'s
  `_validate_issue_tag_definitions` then raised. The tracked `io/table_row_github_issues.json` was
  correct throughout — only a refresh corrupted it on disk, and that run was reverted rather than
  committed. A second label, `ḥolam vav`, is spelled **precomposed** on the same tracker and has no
  `ISSUE_LABEL_TO_TAG` entry — its two issues' rows have empty tags in the tracked JSON, so that part
  was always consistent and never a defect. **Left unfixed on purpose, spawned as a task chip
  2026-08-18**: the chip's session put three fixes to Ben — normalize on read, rename the live label,
  or accept both spellings as keys — and he chose the rename, over normalizing (which would have
  added a `unicodedata.normalize` call to a repo family with a strong "never NFC over Hebrew"
  convention) and over accepting both spellings (which would have left the inconsistency permanently
  documented rather than removed). `gh label edit` renamed the live label from decomposed to
  precomposed; the label ID (`LA_kwDOR5Dbpc8AAAACekXYaQ`) matched on issues 40 and 72 before and
  after, confirming a true rename rather than a delete-and-recreate. That alone fixed the lookup —
  `ISSUE_LABEL_TO_TAG`'s key was already precomposed, so **no `py/` file changed**. Re-running
  `--update-issue-metadata` then produced an empty `git diff` on `io/table_row_github_issues.json`
  and completed without raising; suite still 51 tests, OK. holman-ketiv-qere's tree stayed clean at
  `6b10259` — nothing to commit or push. Ben declined to also file a holman-ketiv-qere issue for it.
- **13 ruff findings under this repo's `ruff.toml`, and holman has never been linted.** That repo
  has no ruff in its venv and no rule set of its own, so the findings were measured by running this
  repo's ruff against its `py/`. **None of the 13 is in a file Phase 1 touched.** Nine are in
  `main_search_holam_he_qere.py`, whose module docstring sits *after* `from __future__ import
  annotations`, making every later import an E402; the rest are two F841 unused bindings
  (`rt_html.py`, `verify_table_words_in_mam_plus.py` — the `verify_table_words_in_mam_plus.py`
  one checked and merely dead, not a wrong-variable bug) and two F401 unused imports in `rt_record_card.py`. **This is a Phase 3
  precondition**, that phase requiring `ruff check py` to exit 0 here; it is the analogue of the
  wlc-utils plan's Phase 0 step 4, which this plan has no counterpart to.
- **The test registry gap is still closed.** All eight `module_name=` entries in
  `TEST_MODULE_SPECS` match the eight files under `py/tests/` exactly, re-checked 2026-08-18. The
  merge still inherits no silently-dead tests. `py/main_test.py` remains a `unittest` loader with a
  hand-maintained tuple and no `check_registry()` walk, so re-check again before Phase 3.
- **Two parameters were renamed to say what they already were.** `export_images`' and the docx
  pipeline's `repo_root` parameter is now `data_root`, that being the root each extracted image
  path is measured against by `relative_to` — a data-root use throughout, and one that raises
  loudly rather than silently misfiling if the wrong root reaches it.
  `PRESERVED_EXTRACTED_IMAGE_PATHS`' comment now says the paths are spelled relative to the data
  root, and says "three" crops where it had said "two" of three since 2026-04.

### The accessor

`py/hkq_paths.py`, deliberately the same shape as `py/uxlc_paths.py`. `hkq_data_root()` is
`paths.repo_root()` today and becomes
`paths.require_sibling("holman-ketiv-qere", paths.sibling_repo("holman-ketiv-qere"))` after the
move; **that body is the whole of the Phase 3 retarget**, because nothing else composes a data path
off anything but that function. Twelve accessors, one per tree or file that appeared in more than
one module: `gh_pages_dir`, `email_img_dir`, `out_dir`, `docs_not_served_dir`, `emails_dir`,
`data_dir`, `io_dir`, `assets_dir`, `novc_dir`, `eml_dir`, plus named paths for the review docx, the
77-row table, the findings HTML, the corrections HTML and JSON, and the row-issues JSON.

Two things about it worth carrying forward:

- **`assets/` is DATA, not code**, though it is authored CSS and JS rather than generated output. It
  is input to a generator whose published copies sit under `gh-pages/`, and it stays with the site.
  A reader who classifies it by "is it hand-written source?" gets it backwards.
- **`mam_qere_words_path()` is the one path whose KIND flips at the move.** It names this repo's
  `out/mam-qere-words.json`, the sanity check the holam-he search compares its hit set against.
  Today that is `paths.sibling_repo("MAM-basics") / "out" / ...`; after the move it is
  `paths.out_dir()` — the CODE root's tree, where every other accessor in the module wants the DATA
  root's. It has an accessor of its own so that the flip is one line and is documented where it
  happens.

Sibling lookups now go through `mb_cmn.paths` — `sibling_repo("MAM-parsed")`,
`mam_parsed_plus_dir()`, `uxlc_utils_dir()` — which brings the `REPO_<NAME>_DIR` / `REPOS_ROOT`
override chain with them, so they also stop resolving wrongly in a worktree.

---

The rest of this section is the plan as written before the phase ran. Its three named sites were the
starting point and not the total, and its framing — cwd-relative string literals — was the wrong
diagnosis, as the first bullet above records.

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

## Phase 3 — copy the Python in (dual residency) — DONE 2026-08-18

**Landed as `1be01b5` in this repo — 60 new files under `py/` plus one modified,
`py/tests/test_h_dot_below_nfc.py`.** Two commits bracket it in holman-ketiv-qere, both
deliberate exceptions to "nothing is committed there": `9e290ce` before, clearing the 13 ruff
findings and the missing UTF-8 stdio, and `15824d4` after, regenerating the single artifact whose
bytes the package rename reaches. Ben's decision, 2026-08-18, put the preconditions in holman
rather than in a commit here straight after the copy, so that neither could make the copy look
like its cause.

**Every baseline was re-measured first and every one matched**, except two that are Phase 1's own
effect rather than drift: 455 tracked files against the table's 454 and 16,640 lines against
16,416, both being `py/hkq_paths.py` and Phase 1's net `+275/−51` measured at `637237b`, before
Phase 1. 100 tracked `.py`, 335 artifacts across the six trees, 8 test modules plus the runner, 9
entry points, suite 51 OK, `table.row_count` 77, 13 ruff findings in the same four files, and all
37 vendored `.py` byte-identical by `cmp`. This repo: 905 passed / 5 skipped / 57 subtests, ruff
clean, black clean, `source_hygiene` OK.

**The oracle ran as specified and passed.** All six generators from
`C:\Users\BenDe\GitRepos\MAM-basics` as the working directory, on this repo's interpreter. An
mtime snapshot around the run shows **175 rewritten and 160 untouched**, the same split and the
same list Phase 1 measured. `git status --porcelain` held nothing outside `py/` here, UXLC-utils
and MAM-parsed stayed clean, and `row_count` is still 77.

Seven things went differently from what is written underneath. The first four bear on later phases:

- **61 files move but only 60 LAND.** `py/tests/test_h_dot_below_nfc.py` becomes a scope edit to
  an existing file rather than a copy, so it is not among the new files. UXLC-utils' Phase 3
  recorded the same shape as "76 move and 74 land". State the two numbers apart in book-of-job's
  and the trio's plans, or a copy commit's file count reads as a shortfall.
- **The third `_Scope` needed one thing beyond the scope itself: `.docx` in
  `_BINARY_EXTENSIONS`.** holman's own copy of the test listed it and this repo's did not, so the
  merged scope read that repo's tracked review docx as text and died decoding a zip —
  `UnicodeDecodeError` in two of the six tests. **Diff the two files' binary-extension sets, not
  only their exclusions and floors, at every remaining repo that carries a copy of this guard.**
  The floor needed nothing: 40, the one holman's copy carried, still fits, with 154 files in scope
  today and about 48 surviving Phase 4.
- **The source-lint crop was 3, not the 68 UXLC-utils' Phase 3 called its largest piece of work.**
  holman's prose is about ketiv/qere rather than accentuation, which is the whole of the
  difference. One transliteration, `mahpakh` for the house `mahapakh` in
  `hkq_cmn/uxlc_change_records`; and one agentive "reads" that takes a `# prose-ok` pragma rather
  than a rewording, because it sits inside `"Job 14.19 where UXLC reads as Merekha.png"`, which is
  Holman's filename on disk. **Budget by subject matter rather than by file count** — book-of-job
  and the codex-index trio are accentuation repos and should be expected to behave like
  UXLC-utils, not like this one. The pragma goes on the dict entry itself: the scan exempts a line
  only via that line or the one after it, so a pragma on the line above leaves the entry flagged.
- **The rename reaches a tracked artifact, and that is not the breadcrumb flip Phase 6 defers.**
  `data/uxlc_standard_atoms.json`'s `note` field embeds the package name, so
  `python_modules/uxlc_standard_atoms` became `hkq_cmn/uxlc_standard_atoms` there. Committed in
  holman as `15824d4` rather than held back: holding it would put that repo's tracked copy
  permanently at odds with the code that writes it, and every later regeneration would show the
  file dirty — which is the oracle damage Phase 6's rule exists to prevent, not an instance of it.
  **Phase 6 still owes two paths their repo name**, neither touched here: that note's
  `hkq_cmn/uxlc_standard_atoms`, and `docs-not-served/table_data_fields.md` line 35, which is
  hand-authored and still says `py/python_modules/verify_table_words_in_mam_plus.py`. Phase 6's
  own grep, `git grep -lI "generated by holman-ketiv-qere" -- gh-pages out docs-not-served`,
  matches **nothing** in this repo — so that grep is not the one that finds this work.

- **Three of the seven moving entry points had no `sys.stdout.reconfigure` at all** —
  `main_extract_docx_and_render_table`, `main_just_render_table`, `main_search_holam_he_qere` —
  and `main_search_final_hiriq_verse_text` reconfigured stdout but not stderr. Two of the three
  print `json.dumps(..., ensure_ascii=False)`, so non-ASCII can reach a stdout that Windows
  encodes cp1252 whenever it is redirected. Nothing had crashed because those summaries happen to
  hold no non-ASCII. UXLC-utils' Phase 3 recorded this hazard as one that "did not materialize",
  every entry point there having reconfigured; **that was a fact about UXLC-utils' `CLAUDE.md`,
  not about the recipe**, so check it per repo. Fixed in `9e290ce`, all four now reconfiguring
  both streams as the first lines of `main()`.
- **The rename touched 77 occurrences in 34 of the 60 files, and two of them were
  `unittest.mock.patch` target strings.** `"python_modules.verify_table_words_in_mam_plus.EXPECTED_ROW_COUNT"`
  resolves by name at run time, so a missed one fails as a patch that finds nothing rather than as
  an import error. `py/repo_util/maintenance_policy.py` says `python_modules` too and was left
  alone, naming mgketer's package; **check every match against what it actually names before a
  bulk rewrite.**
- **A number in `15824d4`'s commit message is wrong.** It says "all 396 entries of standard_atoms
  are byte-identical"; the real count is **124**, read out of the regenerated file afterwards. The
  substance holds — the whole diff is the one `note` sentence — but 396 was written without being
  read, which is what `doc/agent-planning-principles.md` forbids. Recorded here rather than
  amended, a push having already landed.

---

The rest of this section is the plan as written before the phase ran.

**61 moving files** land under `py/` (not 42 — see the re-counted disposition table), with
`python_modules/` → `hkq_cmn/` and the two disappearing entry points. Retarget the data root to
`../holman-ketiv-qere`; fold the tests; watch `force_utf8_io()` where a former entry point becomes a
library module. **Must complete in a single session**, and **stop and ask Ben first**.

**The retarget is one line**, the body of `hkq_paths.hkq_data_root()` — Phase 1 built the accessor
for exactly this, and its record says what the new body is.

The oracle run is **six commands, not one**, listed under the re-measured baselines above, all from
MAM-basics writing into `../holman-ketiv-qere`, then `git status --porcelain` empty in both repos —
and the row count still 77. Expect **175 of the 335 artifacts to be rewritten**; the other 160 are
named in Phase 1's record, and a wrong root shows up there as untracked files appearing in
MAM-basics rather than as a diff, so check for those too.

**Two preconditions Phase 1 established, neither of which this section originally anticipated:**

- **`ruff check py` must exit 0 here afterwards, and holman brings 13 findings with it**, in files
  Phase 1 did not touch. Fix them — in holman, before the copy, or here in a commit of their own
  immediately after — but do not let them ride along in the copy commit, or the copy looks like it
  caused them. Phase 1's record enumerates them.
- **`py/tests/test_h_dot_below_nfc.py` must NOT be copied.** It collides with this repo's file of
  the same name, the two differ, and the right move is a third `_Scope` in this repo's `_scopes()`
  rooted at `hkq_paths.hkq_data_root()`, then deleting holman's copy. Phase 1's record has the
  reasoning and the trap in getting it wrong.

**One thing to check that the other plans do not have — ANSWERED 2026-08-18, no work owed.**
`py/python_modules/table_row_github_issues.py` and `refresh_table_row_github_issues.py` reach
GitHub, and they name `bdenckla/holman-ketiv-qere` outright, as `REPO_OWNER`/`REPO_NAME` constants
passed to `gh issue list --repo`. No working directory picks the tracker and nothing authenticates
cwd-dependently, so a tool silently reading the wrong tracker is not a risk here and the constants
stay as they are. What that path *does* have is a live Unicode-form defect, unrelated to the move
and recorded in Phase 1's findings.

## Phase 4 — empty holman-ketiv-qere — DONE 2026-08-18

**Landed as `0890cb8` in holman-ketiv-qere (111 files changed, 121 insertions, 16,838 deletions)
and `b72f785` here.** Ben was asked first, as this section and the prompt both require, and
approved three things: the deletion, `.vscode/settings.json` as an extra beyond the plan's list,
and rewriting every `py/…` path in the README rather than stating one substitution.

**Every baseline was re-measured first and every one matched but one**, which is Phase 3's own
effect rather than drift. 100 tracked `.py`, 455 tracked files, 335 artifacts across the six trees,
8 test modules plus the runner, 9 entry points, suite 51 OK, `table.row_count` 77, all 37 vendored
`.py` byte-identical by `cmp`, the 13-message mailbox present and the UXLC-utils sibling present.
Here: 950 passed / 5 skipped / 59 subtests, ruff clean, black clean at 834 files,
`source_hygiene` OK.

**The one mismatch: 16,637 lines, not 16,640.** Measured across the three commits —
`6b10259` 16,640, `9e290ce` **16,637**, `15824d4` 16,637 — so the figure in Phase 3's record was
taken before Phase 3's own precondition commit `9e290ce`, which cleared the 13 ruff findings and
added the UTF-8 reconfigures at +12/−15. The same shape as the two Phase 3 itself recorded, one
phase further on: **a plan's freshest figure is still the previous phase's, and the previous
phase's own commits move it.**

**The oracle ran twice, once before the deletion and once after**, both times all six generators
from `C:\Users\BenDe\GitRepos\MAM-basics` on this repo's interpreter, with an mtime snapshot
around each. Both runs: **175 rewritten, 160 untouched**, the same split and the same list Phase 1
and Phase 3 measured. Both times `git status --porcelain` in holman held nothing but this phase's
own edits, MAM-basics' tree stayed clean, and `row_count` was still 77. The pre-deletion run is
worth keeping in the recipe — it proves the generators reach the sibling correctly at the current
HEAD, so anything that breaks afterwards is the deletion's doing and not a pre-existing fault.

**The 160, named here as the section below asks:** **154 `gh-pages/img/`**, `gh-pages/index.html`,
the two `gh-pages/JC3 The Biblical Text in the JC Edition #19-ז` pages,
`gh-pages/woff2/Taamey_D.woff2`, `docs-not-served/table_data_fields.md` and
`io/table_row_github_issues.json`. They are named in holman's `CLAUDE.md` too, where a reader of
that repo will meet them, as UXLC-utils' Phase 4 put its 87 in that repo's `CLAUDE.md`. The
reusable script is `.novc/hkq_oracle_mtimes.py` (`snapshot` / `compare`), a holman twin of
`.novc/oracle_mtimes.py`, which is hardwired to UXLC-utils and its four trees.

Six things went differently from what is written underneath. The first four bear on later phases:

- **The tracked deletion is 107 files, not the 104 this section implies.** Beyond the 100 `.py`
  there are **five** `_provenance.md`, not four: the four package breadcrumbs plus
  **`py/_provenance.md`**, which is the breadcrumb for the loose vendored `py/uxlc_paths.py` and is
  invisible to `doc/vendoring-inventory.md` for exactly the reason Phase 7 item 1 gives about
  `uxlc_paths.py` itself. Also **`py/.gitignore`** (one line, `novc_*.py`) and, by Ben's decision,
  **`.vscode/settings.json`**, whose nineteen auto-approve rules name that repo's interpreter
  (four spellings of `.venv/Scripts/python.exe`) and its `py/` scripts (six rules, one of them
  `py/extract_docx.py`, already gone before this phase) — and also nine that name none of that:
  seven `git` rules (`--version`, `config --get remote.origin.url`, `rev-parse`, `remote`, `add`,
  `commit`, `push`), `where.exe` and `.vscode/settings.json` itself. (This read "fifteen
  auto-approve rules name nothing but that repo's interpreter and its `py/` scripts", as
  `0890cb8`'s message does, until the 2026-08-22 review's follow-up; the count and the nine are
  by `git -C ..\holman-ketiv-qere show 15824d4:.vscode/settings.json`. The decision is
  unaffected: nothing in the file was worth keeping once the interpreter and scripts left.)
  Neither `py/` nor `.vscode/` had other tracked contents, so both went whole. **Count the
  non-`.py` tracked files under `py/` in book-of-job and the codex-index trio before quoting a
  deletion size**: `git ls-files py | grep -v '\.py$'` is the command, and here it found six.
- **Phase 7 item 1 is Phase 4's, exactly as UXLC-utils' Phase 4 predicted it would be in every
  remaining plan.** Deleting `py/mb_cmn/` and `py/mb_diff_mpu/` turned both of holman's
  `pkg_scan_roots` into missing directories, and
  `py/tests/test_vendoring_policy_paths.py::test_every_pkg_scan_root_exists` failed twice in this
  phase's own verification run, once per scan root. Removing the entry and regenerating with
  `py/main_vendoring.py --all` is in `b72f785`. The inventory diff is **only** the two
  holman-ketiv-qere rows, 23 rows / 155 files → **21 rows / 128 files**, the 27 being the 18
  `mb_cmn` plus 9 `mb_diff_mpu` that `cmp` had confirmed identical minutes earlier; no pre-existing
  drift came with it. **Phase 7's remaining items are untouched.**
- **The suite's baseline moves 950 → 947, three tests and not the two that failed.** The third is
  a dest-repo case: `test_vendoring_policy_paths.py` derives *every* parametrize list in it from
  the policy, so the entry was contributing one of those besides its two scan-root cases. 28
  collected in that file before, 25 after — the identical arithmetic to UXLC-utils' 916 → 913 and
  32 → 29. **Predict three per repo, not two**, in book-of-job and the trio.
- **The README's commands were nine, not six.** The extra three are `py/main_test.py`, at lines
  303, 312 and 316, and that runner is one of the two entry points that **disappears** rather than
  moving — so the "## Tests" section could not be repointed by substituting a prefix. It now names
  MAM-basics' runner and a `-k` selection, this repo's `--verify-table-words-in-mam-plus` and
  `--h-dot-below-nfc` having no counterpart here; the replacement command was run before being
  written down (16 passed, 939 deselected). **A README's command count is not its
  generator count** — count `main_test` and any other disappearing entry point separately.
- **The NFC floor holds at 47, one below the 48 the scope's comment predicted**, the difference
  being `.vscode/settings.json`, which was not in the prediction because Ben added it to the
  deletion. 154 files were in scope before and 47 after, against a floor of 40 tested strictly, and
  the guard runs green. Two of the 47 are the `gh-pages/JC3 …` pages, which reach the count only
  because `git ls-files` quotes their non-ASCII names and the leading quote carries them past the
  `gh-pages/` prefix filter — the test uses `git ls-files` without `-z`, so this replicates exactly.
  The comment now states the measured figure instead of the prediction (`b72f785`).
  **Corrected by the 2026-08-22 review's follow-up: 152 → 45, not 154 → 47.** The two quoted
  `JC3 …` names pass the prefix filter but are not paths, so the test's own `is_file()` check,
  three lines further down `_tracked_files_in_scope`, drops both; calling that function on the
  holman scope returns 45 (re-measured 2026-08-22), and the same two come off the "before"
  figure. The arithmetic above kept them; the test never did. The floor of 40 is unaffected, and
  `py/tests/test_h_dot_below_nfc.py`'s holman-scope comment now says 152 and 45.
- **The `doc/` question this section does not raise: holman's `doc/` had four `py/…` paths**, in
  its two files, the same shape as the README's. Rewritten with it, on Ben's "rewrite every one".
  UXLC-utils' Phase 4 met a much larger version of this — 35 links in `doc/clc-design.md` — and Ben
  chose to leave those and state the substitution once. **The two answers are not in conflict**: a
  stated substitution works where only the repo prefix changed, and here `python_modules` →
  `hkq_cmn` changed as well, while `py/uxlc_lci/` and `py/uxlc_misc/` were pure deletions rather
  than moves, so no single stated rule covers all three cases. **Ask per repo, and let the size of
  the rewrite and whether a package was renamed decide it.**

**Two things this phase deliberately did not do, both Phase 6's.**
`docs-not-served/table_data_fields.md` has **two** wrong paths, not the one Phase 3's record names:
line 35's `py/python_modules/verify_table_words_in_mam_plus.py` and **line 3's
`py/main_extract_docx.py`**, which is stale twice over — the entry point is
`main_extract_docx_and_render_table.py` and has been for longer than the move. That file is
hand-authored and one of the 160, so editing it damages no oracle; it was left alone only because
Phase 3 assigned it to Phase 6. And `data/uxlc_atom_locations.json` **also** carries
`py/main_estimate_uxlc_locations.py` in its `note`, as does `data/uxlc_standard_atoms.json`
alongside the `hkq_cmn/uxlc_standard_atoms` Phase 3 named — so that file owes **two**
qualifications in one sentence. Those two `note` fields are generated, which is precisely what
Phase 6's do-not-fix-mid-move rule protects. **Phase 6's inventory is at least five sites, not
two**, and `git grep -nIo 'py/[A-Za-z_./]*' -- data docs-not-served io` is what finds them.

---

The rest of this section is the plan as written before the phase ran.

Delete all **100** tracked `.py` (not 68 — see the re-measured baselines) and the `py/` tree.
**Stop and ask Ben first.**

**CORRECTED 2026-08-18 by Phase 1: this repo DOES have a tracked `CLAUDE.md`.** The sentence below
saying it does not was wrong, and acting on it would have overwritten a live conventions file. It
has five sections, and two must survive this phase intact:

- **the public-repo address boundary**, which is the important one. A `.eml` file's headers have
  Holman's address, Chris Kimball's and Ben's; those files are untracked in `.novc/eml/`, and
  `main_ingest_uxlc_emails.py` writes an address-free derivative under `emails/` that everything
  downstream reads, with `uxlc_email_extract.redact_addresses` running over each body and
  `_sender_display_name` raising rather than passing a bare From header through. Nothing about the
  Python moving changes that boundary, and the section must not be casualty to a rewrite.
- **the `light-dark()` CSS convention**, which governs `assets/` — a tree that stays here.

What that file needs *added* is what the retired sentence wanted written: that there is no Python
here any more, that the code generating `gh-pages/`, `out/`, `docs-not-served/`, `emails/`, `data/`
and `io/` is `../MAM-basics/py/`, which entry point writes what, and that the 77-row expectation is
a fixed scope rather than a current count. Its "Vendor whole files" section is the one that goes,
`py/main_update_vendored_files.py` being deleted. Its two sections on locating a word in the
manuscripts already point at sibling repos and need no change. The README carries the workflow
commands and must be updated in the same commit, since every one of them names a path this phase
deletes — and there are **six** such commands, not the one the README leads with.

**Name the 160 artifacts a full regeneration does NOT rewrite**, the way wlc-utils' Phase 4 named
its 111 and UXLC-utils' Phase 3 its 87. Phase 1's record lists them.

## Phase 6 — breadcrumbs and issue citations — DONE 2026-08-18

**Landed as `4e9d809` here (the generator), `ce6dd7d` in holman-ketiv-qere (three artifacts), and
a `CLAUDE.md` commit after them.** The breadcrumb flip is its own commit in each repo, as this
section asks.

**Every baseline was re-measured first and, for the first time in this plan, every one matched.**
holman-ketiv-qere at `0890cb8`, clean, **0 tracked `.py`**, 348 tracked files, 335 artifacts across
the six trees (`gh-pages` 300, `emails` 26, `docs-not-served` 4, `out` 2, `data` 2, `io` 1),
`table.row_count` 77, the 13-message mailbox present, the UXLC-utils sibling present. MAM-basics at
`e823a79`, clean, suite **947 passed / 5 skipped / 59 subtests**, ruff clean, `source_hygiene` OK.
Phases 1, 3 and 4 each found a figure that had moved; this phase found none, and the reason is
worth keeping: **Phase 4 measured them all hours earlier and nothing ran in between.** Freshness,
not luck — the re-measure is still what establishes that.

**Part 1 — the five stale paths, exactly the five Phase 4 named.** The grep below is the one that
finds them, and it found four `py/…` hits; the fifth, `hkq_cmn/uxlc_standard_atoms`, carries no
`py/` prefix and so is invisible to it. **Read the matched sentences, not only the matched paths.**

The two generated `note` fields were fixed at the generator here —
`main_estimate_uxlc_locations.py`'s `NOTE` and `STANDARD_ATOMS_NOTE` module constants — and the
artifacts regenerated, never edited. `docs-not-served/table_data_fields.md` was edited directly,
being hand-authored and one of the 160 no run rewrites.

**Two shapes, not one, and the artifacts themselves settled which goes where.** The generated
notes take a bare `MAM-basics/py/…`, matching UXLC-utils' Phase 6 and — decisively —
`data/uxlc_atom_locations.json`'s own first sentence, which has said `MAM-basics'` with no `../`
since before the move; a grep of all 335 artifacts for the repo name returns that one site, so
there was exactly one precedent and it is in the very file being edited. The hand-authored
markdown takes `../MAM-basics/py/…`, matching this repo's README.md and CLAUDE.md, which Phase 4
rewrote that way on Ben's "rewrite every one". `hkq_cmn/uxlc_standard_atoms` also gained the `.py`
it lacked, so that it reads as a file rather than a directory; holman's README.md already spelled
that module `../MAM-basics/py/hkq_cmn/uxlc_standard_atoms.py`. Both note paragraphs were re-wrapped
to hold every line inside black's 88 with the word sequence preserved.

Afterwards `git grep -nIoE '(^|[^-a-zA-Z0-9/])py/[A-Za-z_./]*' -- data docs-not-served io` returns
**nothing**: no unqualified `py/` path survives anywhere in holman-ketiv-qere's data or prose.

**Part 2 — there was nothing to prefix, and that is this phase's real finding.** Not one bare
`#NN` in the moved code names a holman-ketiv-qere issue, so no citation was rewritten in either
repo. The full inventory, measured rather than assumed:

- **In the 60 files Phase 3 moved:** 20 `#`-plus-digit sites, all disposed of. **19 are CSS hex
  colours** in `py/py_render/rt_assets.py`; the twentieth is the **`#2026.08.05-6` UXLC change
  anchor** in `py/hkq_cmn/uxlc_change_records.py`, which is not an issue and correctly stays bare.
- **In the rest of holman-ketiv-qere's pre-move `py/`:** eight more sites, at `6b10259`. Six sat
  in `py/mb_cmn/`, a pure deletion — four lines of `hebrew_accents.py` citing Yeivin *ITM* as
  `#194`, `#358` and `#361`, and two of `paths.py`, a `#75` naming **MAM-basics'** paths convention
  and an already-prefixed `wlc-utils#48`. The other two are both `#187`, naming **MAM-basics'** NFC
  convention: one in `main_test.py`, which disappeared at the move, one in
  `test_h_dot_below_nfc.py`, which collided with this repo's copy.

So **every `#NN` holman-ketiv-qere's Python ever carried was either not an issue at all or an
issue of MAM-basics' own**, and the repo whose name would have been the prefix was cited by its
Python not once. `rt_issue_tags.py` and `table_row_github_issues.py` were checked and left alone as
this section requires, their `REPO_OWNER`/`REPO_NAME` constants included.

**The `22` in the task prompt has no source in either plan.** `git grep` finds no such figure in
this file or in `PLAN-evacuate-python-programme.md`; this section, as written below, names no count
at all. Treated as the mismatch this plan says to treat it as, and recorded here so the next
session does not go looking for 22 citations that were never measured.

**`CLAUDE.md`'s section is now "Four issue trackers".** holman-ketiv-qere keeps **81 issues,
numbered 1–81, 60 of them open**, measured 2026-08-18 with
`gh issue list --repo bdenckla/holman-ketiv-qere`. The whole numbered range collides with
MAM-basics', all 81 — sharper even than UXLC-utils' 1–56 — and three worked collisions are given
(#4, #48, #75). **Six numbers the section already used as wlc-utils or UXLC-utils collisions are
now four-way**: #19, #29, #48, #52, #69, #75. A third bullet joins "two things a blind sweep gets
wrong", for the two modules that render issue references as data. The rename strands one more
pointer, `PLAN-evacuate-python-from-UXLC-utils.md`'s Phase 6 record calling the section "Three
issue trackers"; it is left as written, the answer that plan chose for its own four strandings.

**holman-ketiv-qere needs no `doc/` exception, the one way it differs from wlc-utils and
UXLC-utils.** Its `doc/` has two files and neither carries a bare `#NN`. The only `#NN` in any of
its tracked prose is the `#19` its `CLAUDE.md` quotes once, in the one backtick span
`gh-pages/JC3 The Biblical Text in the JC Edition #19-ז` that names the two pages sharing that
stem (this said "quotes twice from the filenames" until the 2026-08-22 review's follow-up;
`git grep -c '#19' -- CLAUDE.md` there is 1) — a JC Edition article number, not an
issue, and so an instance of the trap rather than an exception to the rule.

**Verification.** The full six-command regeneration ran from
`C:\Users\BenDe\GitRepos\MAM-basics` on this repo's interpreter, with an mtime snapshot around it
via `.novc/hkq_oracle_mtimes.py`: **175 of 335 rewritten, 160 untouched**, the same split and the
same list Phases 1, 3 and 4 measured, and `table.row_count` still **77**. holman-ketiv-qere's
`git status --porcelain` held exactly the three intended files and nothing else —
`docs-not-served/table_data_fields.md` and `io/table_row_github_issues.json`, both among the 160,
stayed byte-identical apart from this phase's own edit to the first. MAM-basics' tree held only
`py/main_estimate_uxlc_locations.py`, then only `CLAUDE.md`; `gh-pages/`, `out/` and `in/`
untouched. Suite **947 passed / 5 skipped / 59 subtests**, unchanged; `ruff check py` clean; black
left the one touched file unchanged; `source_hygiene` OK.

---

The rest of this section is the plan as written before the phase ran.

```powershell
git grep -lI "generated by holman-ketiv-qere" -- gh-pages out docs-not-served
```

**That grep matches nothing, in either repo — it is not what finds this phase's work.** Phase 3
established that and Phase 4 re-confirmed it. Use this instead, from
`C:\Users\BenDe\GitRepos\holman-ketiv-qere`:

```powershell
git grep -nIo "py/[A-Za-z_./]*" -- data docs-not-served io
```

**Phase 4 measured five sites, not the two Phase 3's record names.** Two are generated `note`
fields, which is exactly what the do-not-fix-mid-move rule below protects, so they want a
generator edit here plus a regeneration rather than an edit to the artifact:

- `data/uxlc_standard_atoms.json`'s `note` — **two** qualifications in one sentence, not one:
  `hkq_cmn/uxlc_standard_atoms`, which Phase 3 named, and `py/main_estimate_uxlc_locations.py`,
  which it did not.
- `data/uxlc_atom_locations.json`'s `note` — `py/main_estimate_uxlc_locations.py`, the same
  "Written by" sentence.
- `docs-not-served/table_data_fields.md` — **two** wrong paths, not the one Phase 3 named: line
  35's `py/python_modules/verify_table_words_in_mam_plus.py`, and line 3's
  `py/main_extract_docx.py`, which is stale twice over, the entry point having been
  `main_extract_docx_and_render_table.py` since well before the move. This file is hand-authored
  and one of the 160 no run rewrites, so editing it damages no oracle; Phase 4 left it alone only
  because Phase 3 had assigned it here.

Flip them in a **dedicated commit near the end**, and do not "fix the now-wrong path" mid-move —
that destroys the oracle for every artifact carrying a breadcrumb.

Then prefix the moved code's bare `#NN` with `holman-ketiv-qere#`. Note that this repo's Python
already *renders* issue references into its table, via `rt_issue_tags.py` and
`table_row_github_issues.py`: **those are data about the Holman review, not citations of this
repo's own tracker, and must not be rewritten.** Distinguish the two before touching either.

## Phase 7 — cross-repo bookkeeping — DONE 2026-08-19 (items 2–5; item 1 landed inside Phase 4)

**Items 2, 3 and 5 were run rather than assumed. Item 4 deleted a 22 MB venv and found no
orphaned worktrees. Three findings came out of it, and the second is left for Ben.** Unlike
UXLC-utils' Phase 7, which needed no commit in either repo, this one needed a one-line commit in
holman-ketiv-qere — `6b0bb63` there, see finding 1.

**Every baseline was re-measured first and every one matched**, as Phase 6's did and for the same
reason: Phase 6 measured them the day before and nothing ran in between. holman-ketiv-qere at
`ce6dd7d`, clean, **0 tracked `.py`**, 348 tracked files, 335 artifacts across the six trees
(`gh-pages` 300, `emails` 26, `docs-not-served` 4, `out` 2, `data` 2, `io` 1), `table.row_count`
77, one 22 MB `.venv`, and `git worktree list` showing only the main checkout. MAM-basics at
`35903bc`, clean, suite **947 passed / 5 skipped**, ruff clean, `source_hygiene` OK.

**Item 2 — confirmed, no change.** `all-repos.code-workspace` lists `../holman-ketiv-qere` at
line 31 and it stays: that repo still tracks 348 non-Python files.
`in/repo_maintenance_policy.json`'s `frozen_repos` names six repos — CCAR-Psalms, MAM-for-Acc,
MAM-for-CCAR, MAM-for-JPS, mamgo-auto-edits and TMC — and holman-ketiv-qere is not among them and
does not need to be. That register is for paused client projects whose last-changed dates are the
point; holman-ketiv-qere is live work whose generators simply live elsewhere now.

**Item 3 — confirmed, and both predicted strings came back verbatim.** The three subcommand names
were checked against `py/main_repo_util.py` before running, as the task required, and all three
are spelled as the task gave them. `--run-black --workspace-file all-repos.code-workspace --repos
holman-ketiv-qere` reports `REPO=holman-ketiv-qere; BLACK_ATTEMPTED=False; BLACK_OK=False;
Skipped: no tracked .py files in this repo`, the same string UXLC-utils returned.
`--check-repo-standards` on the same repo degrades just as gracefully:
`MAINTENANCE_SCRIPT=n/a; WORKTREE_STEP=n/a; PATH_UTILITY=n/a`, with `LINKED_WORKTREES=0`,
`AGENT_BRANCHES=0`, `SYS_PATH_MUTATIONS=0` and `GITATTRIBUTES_LF=True`. Both runs were scoped with
`--repos`, since dropping it **reformats every repo in the workspace**.

**Item 4 — a 22 MB venv deleted, no orphaned worktrees.** Smaller than the shapes wlc-utils (789
`.py`) and UXLC-utils (832 `.py`, 33 MB) found, holman's venv having held black and no pytest.
Done in the order this plan requires:

- **`--clean-worktrees` ran first**, before anything else touched a worktree, and reported
  `worktrees: nothing to clean`, agreeing with the `git worktree list` baseline. Hand-running
  `git status` inside a worktree refreshes the index mtime that
  `repo_util/git_worktree_cleanup.py` reads as recent activity, and the sweep then spares the
  worktree, so the sweep goes before the poking and not after.
- **Then the checks the deletion was conditional on** — and this is where finding 1 came out. Zero
  tracked files under `.venv`, which is self-ignoring via the `.venv/.gitignore` that
  `python -m venv` writes.
- **And the junction check, which a sibling rule makes mandatory**, because a junction here would
  have taken MAM-basics' venv with it: `Get-Item -Force` reported `Attributes: Directory`, no
  `ReparsePoint`, empty `LinkType` and empty `Target`, and holman's own `pyvenv.cfg` naming
  `C:\Users\BenDe\GitRepos\holman-ketiv-qere\.venv` as what `python -m venv` was pointed at,
  distinct from MAM-basics' `pyvenv.cfg` naming its own. A real directory, so
  `Remove-Item -Recurse -Force` was safe. Afterwards
  `C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe` was confirmed present **and
  confirmed to run**, reporting 3.13.14, and the full oracle was re-run clean.

**Finding 1 — the safety check failed on one tracked site, and Phase 4's own sweep is why.** Item
4's check predicted that every remaining `.venv` mention in holman-ketiv-qere's tracked files
names **MAM-basics'** venv by absolute path. One did not:
`doc/holman-manuscript-citations.md`'s closing line named **holman-ketiv-qere's own** venv by
absolute path — "Run anything written for this from the repo root with
`C:\Users\BenDe\GitRepos\holman-ketiv-qere\.venv\Scripts\python.exe`" — an actionable instruction
pointing at the very directory this phase deletes. **Phase 4 (`0890cb8`) rewrote all three `py/…`
module paths inside that same file** to `../MAM-basics/py/hkq_cmn/…` and
`../MAM-basics/py/py_render/…`, so the file was in that phase's hands and the interpreter line
was missed rather than spared. The reason it was missed is the blind spot Phase 6 already
recorded: **a `.venv` path carries no `py/` prefix**, so it is invisible to the
`py/[A-Za-z_./]*` grep both Phase 4 and Phase 6 swept with — exactly how
`hkq_cmn/uxlc_standard_atoms` escaped Phase 6's own grep. **Grep for the interpreter as well as
for the code paths at every remaining repo**, since the two sweeps miss the same shape.

The fix is one line: the interpreter now reads
`C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe`. **"from the repo root" was left
alone and is still correct** — holman-ketiv-qere's root is where `emails/`, `data/` and
`gh-pages/` live, which is what the re-establishment steps above that line read, and the
interpreter's location decides nothing about the working directory.

Two further `.venv` mentions were examined and **deliberately left**, both in
holman-ketiv-qere's `CLAUDE.md`, both descriptive rather than actionable: line 17's "the `.venv`
left here has nothing to run" and lines 91–92's "the Aleppo one needs Pillow, which this repo's
venv lacks". Each describes a venv this phase has now removed. **UXLC-utils' `CLAUDE.md` carries
the identical sentence and its own Phase 7 left it**, quoting it as evidence the deletion was
safe without revisiting it afterwards, so the two repos are consistent as they stand. Whether
both repos' sentences should be trued up is one question for Ben rather than two, and it changes
no behaviour either way. A third mention, `CLAUDE.md` line 104's relative
`.venv/Scripts/python.exe`, **is not a mismatch**: it follows a `cd` to
`C:\Users\BenDe\GitRepos\codex-index-aleppo` and names that repo's venv, which is what the
surrounding prose tells the reader to do.

**Item 5 — the grep run across all nineteen sibling repos, and it found a live consumer.** In
MAM-basics itself the only hits are two lines of the plan files describing the grep, one in this
file and one in `PLAN-evacuate-python-from-UXLC-utils.md`. The known loose end needed no chasing
and is recorded as moot: UXLC-utils' Phase 7 item 5 handed this plan the finding that
holman-ketiv-qere vendored a loose `py/uxlc_paths.py` invisible to `doc/vendoring-inventory.md`,
and Phase 4 deleted all of holman-ketiv-qere's Python, so nothing was owed.

**Finding 2 — four stale citations in a third repo, left for Ben.** `MAM-private` carries live
cross-references to holman-ketiv-qere's Python:

- a MAM-private `mpu-parsing.md`, lines 9–10 (private annex §5)
- its generated rendering, lines 21–22

They cite `holman-ketiv-qere/py/python_modules/mam_plus_verse_data.py` (`_collect_text_fragments`)
and `holman-ketiv-qere/py/python_modules/qere_projection.py` (`project_qere_atoms`) under a
"**Cross-references:** … When updating rules here, check for matching logic to propagate" heading,
so they are pointers meant to be followed rather than history. They are **stale twice over**:
holman-ketiv-qere has held zero Python since Phase 4, and `python_modules/` was renamed to
`hkq_cmn/` in Phase 3. The correct targets are `MAM-basics/py/hkq_cmn/mam_plus_verse_data.py` and
`MAM-basics/py/hkq_cmn/qere_projection.py`, both confirmed present here. **Not fixed** (as of
this record, `2ce3efb`, 2026-08-19 09:44; **fixed fifteen minutes later by MAM-private `e8fd4ae`**,
2026-08-19 09:59, "mgketer doc: repoint two cross-references to MAM-basics/py/hkq_cmn/", which
edited exactly the two files named above, 4 lines each way — noted here 2026-08-22 by the
follow-up to `doc/review-findings-2026-08-22.md`'s finding 5, until which only the book-of-job
plan cited `e8fd4ae`), on
UXLC-utils' Phase 7 item 6 precedent that a commit to a third repo stops and asks: MAM-private is
neither of this plan's two repos, `mgketer` is a directory inside it rather than a repo of its own
(`git -C mgketer rev-parse --git-common-dir` answers `../.git`), MAM-private was clean at
`a1b489e`, and the `.html` is generated, so the fix is an edit to the markdown plus whatever
regenerates the report. **This is the programme's cross-cutting finding 2 in a new shape**: not a
vendored copy the inventory cannot see, but a *documentation* cross-reference no repo's tooling
can see, and it was found only because item 5 greps the siblings. **Run item 5's grep against
MAM-private at book-of-job and the codex-index trio**, which the earlier plans had no reason to.

**Verification.** The full six-command regeneration ran from `C:\Users\BenDe\GitRepos\MAM-basics`
on this repo's interpreter, after the venv deletion, with an mtime snapshot around it via
`.novc/hkq_oracle_mtimes.py`: **175 of 335 rewritten, 160 untouched**, the same split Phases 1, 3,
4 and 6 measured, and `table.row_count` still **77**. All six generators exited 0; the mailbox
held its 13 messages and the UXLC-utils sibling was present at `9be1431`.
holman-ketiv-qere's `git status --porcelain` then held exactly one file, the
`doc/holman-manuscript-citations.md` of finding 1, and its tracked total was still 348.
MAM-basics' tree was **clean** — `gh-pages/`, `out/` and `in/` untouched, as this phase expected,
since none of its own artifacts depend on holman-ketiv-qere. Suite **947 passed / 5 skipped**,
unchanged; `ruff check py` exit 0; `source_hygiene` OK. No Python was edited in either repo, so
black had nothing to run on.

**Finding 3, small and about the plan's own bookkeeping rather than about either repo: the
`59 subtests` figure does not reproduce.** Phases 3, 4 and 6 each record the suite as
"947 passed / 5 skipped / 59 subtests" (Phase 3's as 950/5/59), and the task prompt for this phase
repeated it. Measured 2026-08-19, the suite's summary line reads `947 passed, 5 skipped` and
nothing more, and the word "subtest" appears **zero** times in the full output.
`pytest-subtests` is **not installed** in `.venv` — `pip list` shows `pytest 9.1.0` and no
subtests plugin — so pytest has no way to report the figure, and a third count cannot be produced
on demand. **The two substantive counts match exactly**, so nothing about the suite has changed
and this costs the verification nothing; what it costs is the third figure, which should be
dropped from the triple rather than carried forward. Record the suite as **947 passed / 5
skipped** in the remaining plans, and re-measure rather than copying a figure whose instrument is
not in the venv.

**Correction, 2026-08-22 (the 2026-08-22 review, `doc/review-findings-2026-08-22.md` finding 6):
Finding 3 above is wrong — the `59 subtests` figure does reproduce.** pytest 9.1.0 reports
`unittest` subtests natively, with no `pytest-subtests` plugin: the review's full run at `b37bdb4`
printed `945 passed, 5 skipped, 59 subtests passed`, and `py/main_test.py -q` over the six
`subTest` modules alone prints `90 passed, 59 subtests passed`. The book-of-job plan's Phase 4
record had already said so ("that is wrong … measured twice"); this paragraph re-points the plan
that made the claim. Why the 2026-08-19 measurement above saw no subtests line is not explained by
anything in the record, and the review did not reproduce it. Keep recording the triple.

---

The rest of this section is the plan as written before the phase ran.

1. **DONE 2026-08-18, inside Phase 4, as `b72f785`.** Deleting `py/mb_cmn/` and `py/mb_diff_mpu/`
   turned both scan roots into missing directories and
   `test_every_pkg_scan_root_exists[holman-ketiv-qere-…]` failed twice in Phase 4's own
   verification run — which is what UXLC-utils' Phase 4 said to expect in every remaining plan.
   The inventory went 23 rows / 155 files → 21 rows / 128 files, the diff being only the two
   holman-ketiv-qere rows. The original instruction, which said this repo is "two of the
   inventory's 19 rows" and was measured before the wlc-utils and UXLC-utils entries came out:
   delete the `holman-ketiv-qere` entry, whose `pkg_scan_roots` names `py/mb_cmn` and
   `py/mb_diff_mpu`; `py/main_vendoring.py --all` **raises** on a missing scan root rather than
   degrading. Regenerate `doc/vendoring-inventory.md` in the same commit.

   **Note what those two rows do NOT cover, measured 2026-08-18: `py/uxlc_lci/` (4 files),
   `py/uxlc_misc/` (5) and `py/uxlc_paths.py` are vendored from this repo too — named in holman's
   `_VENDORED_PACKAGES` and `_VENDORED_FILES` — and appear nowhere in the inventory,** the scan
   roots declaring only the two `mb_*` packages. Deleting the entry disposes of the undercount
   along with the rest, so **no fix is owed here**; it is recorded because Phase 4's pure-deletion
   accounting depends on it (37 files, not 26) and because the same blind spot may hide copies in
   book-of-job and the codex-index trio, where the copies have **diverged** and a missed one is
   lost work rather than a miscount. This is the programme's cross-cutting finding 2, wider than
   the UXLC-utils hand-off that named only the one loose file.
2. `all-repos.code-workspace` — leave it listed; it keeps its tracked non-Python files.
3. Confirm `run_black.py` and `check_repo_standards.py` skip it cleanly on the next sweep.
4. **Delete its `.venv` and any orphaned agent worktrees**, per the 789-stray-file finding in the
   wlc-utils plan's Phase 7.
5. Grep the other repos for `holman-ketiv-qere/py`.
