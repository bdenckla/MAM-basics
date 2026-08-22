# Evacuate all Python from book-of-job into MAM-basics

Written 2026-08-02. Governed by [PLAN-evacuate-python-programme.md](PLAN-evacuate-python-programme.md).
**Fourth in the order**, after UXLC-utils, holman-ketiv-qere and the programme's blocking Phase 0.
This is the largest and least regular repo in the programme, and the only one whose plan opens
with a question rather than a phase.

## Status

| Phase | State |
|---|---|
| D — the quirk-record question | **decided 2026-08-02: all 267 move, records included** |
| 0 — reconcile the fork families | **DONE 2026-08-19, all five families.** Three were closed by the programme's blocking Phase 0 (`33b3ee2` here, `98021de` in codex-index-aleppo, `f56831c` in codex-index-cam1753). The two this repo owed were classified the same day, and `py_uxlc_loc/` hit the gate; **Ben's decisions, 2026-08-19, were to move book-of-job from UXLC 2.1 to 2.5, put its finer LC index records for pages 397A and 406A upstream and into BOTH copies of `lci_recs.json`, and target MAM-basics' `uxlc_misc`/`uxlc_lci` lineage rather than its `py_uxlc/` one.** Landed as `4d1ad89` in UXLC-utils and `2979507` here (the records), `6fb8c06` in book-of-job (`mb_cmn/`, seven files) and `7ca99f7` in book-of-job (the UXLC move, 44 files). **All 701 artifacts are byte-identical after every step, and the final run is silent** — no `fline mismatch`, which the coarse records had produced. See "Phase 0 — the execution record" below |
| 1 — two roots, no cwd | **DONE 2026-08-19.** Landed as `45f8853` in book-of-job (18 files, +305/−100), adding `boj_paths.py`; nothing owed in MAM-basics. The oracle now runs from a foreign working directory with all **701 artifacts byte-identical** and MAM-basics' tree untouched, `check_all.py` 7 of 7, the NFC suite 6 tests OK. Tracked `.py` is now **268** and lines **17,064**. **This repo does not vendor `mb_cmn/paths.py` and must not** — `parents[2]` is wrong at a root-level `mb_cmn/` — so `code_root()` walks to `.git` instead. **The prescribed grep undercounted by six and two of its seven hits are false positives.** Two root walks were left alone on purpose, `py_ac_word_image_helper/flat_index.py` and `py_cam1753_word_image/page.py`, both being blobs shared with a codex-index repo. **One question is open and is Ben's: `mb_cmn/provenance.py`'s `parents[2]`.** See "Phase 1 — two roots, no cwd" below |
| 3 — copy the Python in (dual residency) | **DONE 2026-08-19.** Landed as `ef8e384` in MAM-basics (243 files: 241 `.py` under the four names Ben settled that day — `author_boj_qr/`, `author_boj_util/`, `author_boj/`, `boj_render/` — plus `quirks-BHQ.txt` and the spelling dictionary); nothing owed in book-of-job, whose HEAD is `45f8853` before and after. `a585cb6` precedes it and is not the move: it regenerates `doc/vendoring-inventory.md`, which Phase 0 left stale. **The oracle passed on the first run from MAM-basics and on every run since** — silent, all **701 artifacts byte-identical**, from this repo's root, from `GitRepos`, and from book-of-job's own copy. Suite unchanged at 947 passed, 5 skipped; `check_all.py` 7 of 7 from both repos. **The `path_to_uxlc` parameter Phase 1 demanded is not needed**: all 39 UXLC XML are one blob across the three repos and `lci_recs.json` differs from UXLC-utils' in one header line, so `prep()` takes no arguments and `uxlc_misc`/`uxlc_lci` were not touched. **The one fork the move forced is four source lints**, which scanned a repo root that now holds all of MAM-basics; `fix_mark_order.py` would have rewritten this repo on sight. Two of this repo's own lints fired on the arriving code and both were right. See "Phase 3 — copy the Python in (dual residency)" below |
| 4 — empty book-of-job | **DONE 2026-08-21.** Landed as `a846585` in book-of-job (320 files: 317 deletions, 3 modified) and `cff95f7` here (14 files). **book-of-job holds zero Python**: 268 `.py` deleted, plus `quirks-BHQ.txt`, the spelling dictionary, the **40 UXLC data files Ben chose to delete** rather than keep, and 7 of the 9 procedure docs, which followed the code here as `doc/boj-*.md`. Tracked files 1103 → 786. Nine directories went whole. **All 701 artifacts byte-identical after the deletion and the oracle silent**, run three times; `check_all.py` 7 of 7. **Phase 7 item 1 fired inside this phase for the third repo running** and costs **two** tests, not holman's predicted three — one case per `pkg_scan_root` plus one, and book-of-job had one scan root where holman had two. Suite 947 → **945 passed, 5 skipped, 59 subtests**. **Two forecasts came out one short each, both for the same reason**: mark order scans **298** files rather than 299 (Ben's delete decision took `lci_recs.json` as well as the spelling dictionary) and the NFC scope holds **35** rather than 42 (the seven moved docs). **The `59 subtests` figure DOES reproduce and Phase 1's reason for saying otherwise was wrong** — six modules use `unittest`'s native `self.subTest`, which pytest counts without the absent `pytest-subtests`. `CLAUDE.md` there was edited and the README replaced; both name the **518 artifacts no program writes**. **Two root-level files orphaned by the deletion, `book-of-job.code-workspace` and `requirements.txt`, were Ben's decision the same day and he chose to delete both** — a second commit each side, `aa20c61` there and the commit carrying this record here, taking that repo to **784** tracked files and a root of four. `mb_cmn/provenance.py`'s `parents[2]` is **moot for book-of-job now**, that tree being gone. See "Phase 4 — empty book-of-job" below |
| 6 — breadcrumbs and issue citations | **DONE 2026-08-22.** Landed as `8293ce8` here and **nothing in book-of-job** — the first of the programme's three Phase 6 runs to owe its data repo nothing. Both halves of the prescription were nil, as Phase 4 predicted: **both breadcrumb greps return 0** (no code here ever passed `generator_file`, so no artifact carries an `mb_cmn.provenance` breadcrumb), and **not one of the 29 `#NN` sites in the 268 pre-move `.py` needed a prefix** — 24 lines of CSS hex colours, 4 Yeivin *ITM* section numbers in the deleted `mb_cmn/hebrew_accents.py`, and one already written out as `bdenckla/wlc-utils#43`. **holman-ketiv-qere's rule has its second confirming case at four times the size**: 241 modules moved and owed one clause. What the phase did owe, and neither plan wrote down: **`CLAUDE.md`'s section is now "Five issue trackers"** — book-of-job keeps **61 issues, 1–61, 19 open**, and **four of the six four-way collisions become five-way** (#19, #29, #48, #52), #69 and #75 staying four-way. **book-of-job needs no `doc/` exception and goes further than holman-ketiv-qere**: `#NN` appears nowhere in any of its 784 tracked files. **The two wider sweeps found nothing stale either** — its 17 `py/…` paths are correct under the working directory Phase 4 declared once at the top (a **third** breadcrumb shape), and no tracked file names its own `.venv`, so **Phase 7 item 5 can delete that 153 MB venv with no documentation edit**. Oracle silent, 700/1/0, suite 945/5/59, `check_all.py` 7 of 7. See "Phase 6 — breadcrumbs and issue citations" below |
| 7 — cross-repo bookkeeping | **DONE 2026-08-22, items 2–6; item 1 had landed inside Phase 4** (2026-08-21: the `book-of-job` entry deleted from `in/vendoring_policy.json` and `doc/vendoring-inventory.md` regenerated, 20 rows/129 files → 18/112). **Landed as one commit here and nothing in book-of-job** — the second of the four Phase 7 runs to owe its data repo no commit. **Item 2's string survives and the plan's attribution of it was what was stale**: `main_map_changes_to_book_of_job.py` has been this repo's since 2026-08-03, its `html_base` is a label `write_mapping()` puts in the output dict rather than a path anything opens, the real route to that sibling is `uxlc_paths.require_book_of_job_dir()`, and the label reaches a tracked artifact in UXLC-utils. **Item 3 confirmed verbatim for the third repo running**; book-of-job is not in `frozen_repos` and needs not be. **Item 4's zero-`.py` case was decided in advance by a fix made for exactly this shape** — `run_black.py` asks `_has_tracked_py_files` *before* looking for black, an ordering changed 2026-08-02 because wlc-utils' leftover venv had just been reformatted — and book-of-job was that shape at more than double the size: **1,722 untracked `.py` inside the venv**, against wlc-utils' 789 and UXLC-utils' 832, every one skipped. Both sweep strings came back verbatim. **Item 5 deleted a 153 MB venv** after `--clean-worktrees` reported nothing to clean across all 20 repos, the three safety greps came back as Phase 6 measured them, and a junction check reported a plain `Directory` with its own `pyvenv.cfg`. **book-of-job's `CLAUDE.md` sentence needed no edit for the opposite reason from the other two repos'**: theirs describe a venv now gone, while line 19's "there is no `.venv` here to run it with" was *false about the disk* and this phase makes it true. **Item 6 found five stale citations, and the grep shape the two earlier plans prescribe would have found one of them** — book-of-job's Python sat at the repo root, so `book-of-job/py` matches almost nothing that moved, and three of the five name a bare module filename with the repo left to the surrounding prose. **Grep for the repo's NAME and classify by hand.** Three are in MAM-private and are reported, not fixed: `mgketer/documentation/periodic-maintenance.md` lines 137–152, a "Checks ported from book-of-job (TBD)" section naming `check_all.py` and five `check_*.py` that are all this repo's now — **holman-ketiv-qere's finding 2 recurring in the same shape in the same tree**; `masorah-books/doc/migration-checklist.md:152`'s `../book-of-job/pyauthor_qr/qr_1413.py`, whose point survives and only whose path is wrong; and mgketer's diverged copy of `alef_bet_to_ascii.py`. **The fourth is one blob across two public repos** — `py/py_ac_word_image_helper/alef_bet_to_ascii.py:5` here and codex-index-aleppo's byte-identical copy, both citing "book-of-job `author.py`" — so it is **handed to the trio plan** rather than forked by an edit to one side; this repo's copy misattributes to a sibling a file this repo holds. The fifth is `UXLC-utils/doc/clc-design.md:824`'s "many check scripts", a third repo again. **github-misc and the skills are nil**, book-of-job's one mention in each copy being `hebrew-prose/SKILL.md`'s repo list, still correct. Oracle silent, 700/1/0 before and after the deletion, suite 945/5/59 with the `59 subtests` reproducing a fourth time, `check_all.py` 7 of 7. See "Phase 7 — cross-repo bookkeeping" below |

## Baselines — measured 2026-08-02

| Measure | Value |
|---|---|
| tracked `.py` | **268** after Phase 1, which added `boj_paths.py`. It was **267** through Phase 0 — `mb_cmn/provenance.py` arrived and `py_uxlc_loc/my_tanakh_book_names.py` went, so `mb_cmn/` is **17** and `py_uxlc_loc/` **9**. **Phases 3 and 4 face 268** |
| lines | **17,064** after Phase 1, whose net +205 is `boj_paths.py`. It was **16,859** after Phase 0, re-measured 2026-08-19 (17,105 before it, 17,060 before the programme's Phase 0); that phase's net −246 is `my_tanakh_book_names.py`'s 566 out against `provenance.py`'s 223 and the six re-vendored `mb_cmn` files' growth in |
| tracked `gh-pages` | **694** (`jobn` 531, `jobn-details` 160, plus `index.html`, `style.css`, `woff2`) |
| tracked `out` | **7** JSON |
| test modules | **1** (`test_h_dot_below_nfc.py`, at the repo root) |
| entry points | **5** `main_*.py`, all at the repo root |
| conventions docs | **1** `CLAUDE.md`, re-measured 2026-08-19. The row said **10** `.github/copilot-instructions*.md` and **no** `CLAUDE.md`; `69162e4` deleted the Copilot file and `991a1c4` moved the nine procedure docs out of `.github/` and added a `CLAUDE.md`, both on 2026-08-03, the day after this plan was written. **Phase 4 edits a `CLAUDE.md` here rather than writing one**, as it did at holman-ketiv-qere |

The oracle is the **701 tracked artifacts**, re-counted 2026-08-19 with
`git -C book-of-job ls-files 'gh-pages/*' 'out/*' | wc -l`. `check_all.py` runs seven checks over
them and is the nearest thing this repo has to a gate.

**The oracle command is `main_gen_misc_authored_english_documents.py`, alone, run from the repo
root** — settled 2026-08-19 by Phase 0, which the row above asked it to settle. There is no order
to establish, because the other four entry points write no tracked artifact between them, and it
rewrites **183** of the 701, not all of them:

```powershell
C:\Users\BenDe\GitRepos\book-of-job\.venv\Scripts\python.exe main_gen_misc_authored_english_documents.py
```

The Phase 0 record below carries what that cost to establish: the venv held one of the five
packages `requirements.txt` names, and `git status --porcelain` is the **wrong instrument** for
reading the result here.

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
| `mb_cmn/` | 16 → **17** | **reconciled by Phase 0, and now a plain deletion.** All 17 are one blob with MAM-basics' `py/mb_cmn/`; the 17th is `provenance.py`, which `file_io.py` drags in |
| `py_uxlc_loc/` | 10 → **9** | **reconciled by Phase 0**, and a plain deletion too: Ben chose MAM-basics' `uxlc_misc`/`uxlc_lci`, which already holds this code. `my_tanakh_book_names.py` is gone, it having been a second copy of `mb_cmn/bib_locales.py` |
| `pyauthor/` | 10 | moves, renamed with the other two `pyauthor*` directories |
| `py/` | 7 | moves, **but two names are traps** — see below |
| `py_ac_word_image_helper/` | 6 | **a third fork family — programme Phase 0** |
| `pydiff_mm/` | 5 | moves as-is; distinct from MAM-basics' `mb_diff_mpu` |
| `py_cam1753_word_image/` | 4 | **a fourth fork family — programme Phase 0** |

**Two directory names are traps for anyone reading `git ls-files` by prefix.** `py_ac_loc/` holds
**76 tracked files and zero `.py`** — it is MAM-XML data, despite the `py_` prefix. `py_uxlc_loc/`
holds 40 data files *and* 10 `.py`. Do not infer a directory's contents from its name in this
repo. (The 40 read **39** XML under `py_uxlc_loc/UXLC/` plus **one** JSON,
`py_uxlc_loc/UXLC-misc/lci_recs.json`, re-measured 2026-08-19; this row said "40 UXLC XML files",
which loses the JSON — and the JSON is the file Phase 0 found is hand-indexed for Job and held
nowhere else.)

### The `mb_cmn` copy has diverged — **6 files, not 16, re-measured 2026-08-19**

**This subsection is the prescription, left as written. The classification it asks for is in
"Phase 0 — the execution record" below, under "Family 1"** — all six differences are droppable
drift, and the family reconciles. Two claims below did not survive that run: the sentence about
`doc/vendoring-inventory.md` is itself the stale record, and the six files drag a seventeenth,
`provenance.py`, along with them.

`doc/vendoring-inventory.md` records book-of-job's 16 `mb_cmn` files as **`DIFFERS`**, with
mechanism `unknown` — no copy script has ever refreshed them. **That is now stale**: compared as
committed blobs against MAM-basics' `py/mb_cmn/`, **10 of the 16 are identical and 6 differ** —
`bib_locales.py`, `file_io.py`, `hebrew_accents.py`, `hebrew_punctuation.py`, `uni_heb.py` and
`uxlc_change_url.py`. Two re-vendoring commits closed most of the gap after this plan was written,
`8bc2602` (2026-08-04, `str_defs.py`) and `60db958` (2026-08-07, `url_percent.py`), and others had
converged earlier. Re-establish with
`git -C book-of-job rev-parse HEAD:mb_cmn/<f>` against `git -C MAM-basics rev-parse HEAD:py/mb_cmn/<f>`,
**never `cmp` on the working trees** — see the note under `py_uxlc_loc/` for what that instrument
does here.

**Deleting the 6 the way wlc-utils' 26 were deleted would destroy whatever those differences
are.** Diff those 6 against MAM-basics' originals and classify each difference before Phase 3: a
fix that belongs upstream, a local adaptation that belongs in the moving code, or drift that can
simply be dropped. **Write the classification into this file.** Only after that are they a
deletion. The other 10 are a plain deletion, being byte-identical to what MAM-basics already has.

### `py_uxlc_loc/` is a diverged fork of the UXLC location code

**This subsection is the prescription, left as written. The classification it asks for is in
"Phase 0 — the execution record" below, under "Family 2"**, and it **hits the gate**. Its eight
line counts all reproduce; three of its other claims do not. Only **one** module lacks a
counterpart, not two — `my_uxlc_lci_rec_flatten.py` has `py/uxlc_lci/uxlc_lci_rec_flatten.py`, and
`my_tanakh_book_names.py` is an older copy of `mb_cmn/bib_locales.py`. And MAM-basics holds **two**
forks of this code rather than one, so "MAM-basics is what to diff against" names two different
files per module.

Ten modules whose names map one-to-one onto what is now MAM-basics' `py/uxlc_misc/` and
`py/uxlc_lci/`; eight have a direct counterpart and two do not. **The counterpart moved after this
plan was written**: UXLC-utils' Python was evacuated into MAM-basics on 2026-08-03, so
`../UXLC-utils/py/` names nothing and MAM-basics is what to diff against.

**The 2026-08-02 figures were a line-ending artifact.** They read 372, 308, 302, 240, 185, 162, 116
and 14 differing lines, and **seven of those eight are exactly twice the file's total line count** —
`my_uxlc_lci_rec.py` is 154 lines and was reported at 308, `my_uxlc_lci_augrec.py` 151 and 302,
`my_uxlc_page_break_info.py` 81 and 162, `my_uxlc_verlen.py` 7 and 14. That is what a diff reports
when *every* line differs, each counted once as removed and once as added. book-of-job's working
tree holds 258 of its 267 tracked `.py` as CRLF while its index holds LF, so a working-tree `diff`
against an LF checkout reports the whole file every time. The programme plan's Phase 0 record
carries the full account of that instrument; there it cost a quarter of its own table's verdicts.

Re-measured 2026-08-19 against committed blobs:

| book-of-job `py_uxlc_loc/` | MAM-basics counterpart | Differing lines | Was reported |
|---|---|---|---|
| `my_uxlc.py` | `uxlc_misc/my_uxlc.py` | **97** | 240 |
| `my_uxlc_page_break_info.py` | `uxlc_misc/my_uxlc_page_break_info.py` | **41** | 162 |
| `my_uxlc_location.py` | `uxlc_misc/my_uxlc_location.py` | **30** | 372 |
| `my_uxlc_bibdist.py` | `uxlc_misc/my_uxlc_bibdist.py` | **23** | 185 |
| `my_uxlc_lci_augrec.py` | `uxlc_lci/uxlc_lci_augrec.py` | **8** | 302 |
| `my_uxlc_cvp.py` | `uxlc_misc/my_uxlc_cvp.py` | **4** | 116 |
| `my_uxlc_lci_rec.py` | `uxlc_lci/uxlc_lci_rec.py` | **2** | 308 |
| `my_uxlc_verlen.py` | `uxlc_lci/uxlc_lci_verlen.py` | **2** | 14 |

Re-establish a row with `diff` of `git -C book-of-job show HEAD:py_uxlc_loc/<f>` against
`git -C MAM-basics show HEAD:py/<counterpart>`, counting lines matching `^[<>]`.

**None of this is in `doc/vendoring-inventory.md`**, which records only `mb_cmn` rows for
book-of-job — the scan looks for MAM-basics packages, and these are UXLC-utils ones. It is the
same blind spot that hides codex-index-leningrad's `UXLC-utils-sparse/py/`, and it means **the
UXLC location code exists in three public repos**: UXLC-utils, codex-index-leningrad and here.

**The conclusion this section drew does not survive the re-measure.** It read: "At 372 differing
lines the more likely reading is independent evolution on both sides, in which case they are two
tools with a common ancestor and both belong in MAM-basics under distinct names." At 2 to 97 lines
**that reading is no longer the likely one — ordinary drift is**, and what these eight probably
want is reconciliation onto MAM-basics' copies rather than a second set of names in the same repo.
`my_uxlc.py` at 97 and `my_uxlc_page_break_info.py` at 41 are the only two big enough to hide a
real behavioural difference, so look there first; the four at 8 lines or fewer are almost certainly
drift. **Classify before deciding either way** — the point of the correction is that the design
call is now open rather than settled against reconciliation.

**Decide it in coordination with UXLC-utils' Phase 5**, which faced the same question for
codex-index-leningrad's copy and **dropped that repo's sparse `py/` half rather than repointing
it** (2026-08-03, `d5195e3` in codex-index-leningrad) — a precedent for dropping a diverged fork
rather than renaming it, and one that reads very differently now the divergence here is measured in
tens of lines. Whichever plan reaches the question first answers it and writes the answer into both
files.

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

## Phase 0 — the execution record — **DONE 2026-08-19, both families reconciled**

Classified 2026-08-19 at book-of-job `33b3ee2` and MAM-basics `ebc9669`, both content-clean, after
the programme's blocking Phase 0 had closed the other three fork families. `mb_cmn/` reconciled
outright; `py_uxlc_loc/` hit the gate, **Ben answered the same day**, and both were then
reconciled. The prescription this record answers is the two `###` subsections above, left as
written. **What Ben decided, and what landed, is in the closing section "The gate, and how it was
answered".**

**Every figure here was taken on committed blobs** — `git -C <repo> rev-parse HEAD:<path>`, and
`diff` of `git show HEAD:<a>` against `git show HEAD:<b>` — never `cmp` or `diff` on a checked-out
file. The re-measure moved one figure the instrument note itself rests on: book-of-job now holds
**249** of its 267 tracked `.py` as CRLF in the working tree and 18 as LF, where the note above
says 258 and 9. Nine files moved, and they are exactly the nine the programme's Phase 0 touched
here — the five `33b3ee2` rewrote and the four `py_cam1753_word_image/` checkouts 0c refreshed. Not
drift, then, but that phase's own effect, and the moral is unchanged: **re-measure the instrument
as well as the thing.**

### The oracle: `main_gen_misc_authored_english_documents.py`, alone — and 518 artifacts no program writes

The Baselines section asked which of the five entry points must run, in what order, to rewrite all
701. The answer is **one entry point, no order, and it does not rewrite all 701.** Read off the
five entry points and confirmed by running them:

| Entry point | What it writes |
|---|---|
| `main_gen_misc_authored_english_documents.py` | **175 HTML + 2 CSS + 6 `out/*.json` = 183 tracked artifacts** |
| `main_apply_cam1753_crops.py` | PNGs under `gh-pages/jobn/img/cam1753/`, and appends `out/cam1753-crops.json` — but only for the crops in a hand-made editor export it takes as its argument, so it is a manual ingest step rather than a regenerator |
| `main_gen_aleppo_crop_editor.py` | `.novc/` only — gitignored (`.gitignore:4`) |
| `main_gen_cam1753_crop_editor.py` | `.novc/` only |
| `main_list_missing_aleppo_imgs.py` | nothing; it prints |

The other three read `out/enriched-quirkrecs.json` **at module import time**, so they all depend on
the oracle having run first. That, and not an ordering among them, is the only sequencing there is.

**So 518 of the 701 tracked artifacts are written by no program in this repo**: 515 PNG, 2 woff2
and `out/cam1753-crops.json`. Of the 515 PNG, only the 160 under `gh-pages/jobn/img/cam1753/` have
even a manual producer here; the 160 under `Aleppo/`, the 160 under `Lenin/`, the 30 under
`gh-pages/jobn/img-orphans/` and 5 loose files in `img/` have none. **This is most of Phase 4's
"name the tracked artifacts that no program generates" already done** — and it is a larger share
than wlc-utils' 111 of its own corpus, so Phase 4 should start from this table rather than
re-deriving it.

Re-establish with `git -C book-of-job ls-files 'gh-pages/*' | sed 's/.*\.//' | sort | uniq -c`
(515 png, 175 html, 2 woff2, 2 css) and
`git -C book-of-job ls-files 'gh-pages/jobn/img/*' | sed 's|.*/img/||; s|-.*||' | sort | uniq -c`.

### The venv held one of the five packages its own `requirements.txt` names

The oracle would not start: `main_gen_misc_authored_english_documents.py` imports
`check_spelling_in_html` at module level, which imports `spellchecker`, and book-of-job's `.venv`
had **black and nothing else**. The repo tracks a `requirements.txt` naming **black, matplotlib,
numpy, Pillow, pyspellchecker**, so the venv was under-hydrated against this repo's own
declaration rather than the declaration being wrong. Fixed by installing it, which is a change to a
gitignored venv and nothing else:

```powershell
C:\Users\BenDe\GitRepos\book-of-job\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

**This widens a programme Phase 0 finding rather than repeating it.** That phase recorded that no
repo's `check_all.py` runs in its own venv — book-of-job on `pyspellchecker`, the two codex-index
repos on `Pillow` — and called it pre-existing. It is: the same missing package also stops the
**oracle**, which is a good deal worse than stopping an aggregate check, and neither the programme
plan nor this one had noticed. **At the codex-index trio, install each repo's `requirements.txt`
before concluding anything about what its entry points do.** Note also that **MAM-basics' own venv
has Pillow and pytest but no `pyspellchecker`**, so Phase 3 must add it there when
`check_spelling_in_html.py` lands.

### `git status --porcelain` is the wrong instrument in book-of-job, and this is the third table it would have corrupted

A clean regeneration at HEAD, changing nothing, leaves `git status --porcelain` reporting **183
modified files**. They are not modified. `git diff --exit-code` passes, `git diff-files` reports
no change, and `git hash-object` on each file returns the blob already in the index. What differs
is git's cached **stat** data: `git ls-files --debug gh-pages/index.html` records `size: 777` where
the file and the blob are **757** bytes. The 777 is the CRLF checkout the working tree held before
the run; the generator writes LF (`mb_cmn/file_io.py`'s `_openw` defaults `newline=""`), so the run
converts those 183 files from CRLF to LF — a real change on disk that `text=auto eol=lf` makes
invisible to a content comparison. `git update-index --refresh` does not clear it, in or out of a
sandbox, and the index is not rewritten.

**The verification convention every plan in this programme uses — "`git status --porcelain` empty"
— therefore cannot be used in book-of-job.** Use a byte comparison against the HEAD blobs instead,
which needs no index at all: read each tracked artifact with `git cat-file blob HEAD:<path>` and
compare it to the file on disk, reporting byte-identical, line-ending-only, and genuinely different
as three separate verdicts, the way `py/vendoring/compare.py` already does for vendored copies.
Measured that way, the baseline run gives **700 byte-identical, 1 line-ending-only, 0 content
differences** — the one being `out/cam1753-crops.json`, which the oracle does not write and whose
checkout is still CRLF.

**This is the same instrument that has now cost this programme four tables** — the programme plan's
`py_cam1753_word_image/` verdicts, this plan's `py_uxlc_loc/` line counts, this plan's `mb_cmn`
"all 16 DIFFERS", and now the oracle's own pass/fail. **Carry the byte-comparison recipe to the
codex-index trio**, where the same `.gitattributes` and the same stale checkouts exist.

### `doc/vendoring-inventory.md` was right, and this plan was the stale record

The prescription says the inventory "still records all 16 as `DIFFERS`, with mechanism `unknown`",
and calls correcting it in scope. **It records no such thing.** Read 2026-08-19, it carries three
rows for book-of-job's `mb_cmn`, and they agree with this phase exactly: the **six** named files as
`DIFFERS`, nine as `eol-only`, and `str_defs.py` as `identical`. `py/vendoring/compare.py` grew
that three-verdict identity column on 2026-08-04, after the 2026-08-03 review ([#219](https://github.com/bdenckla/MAM-basics/issues/219),
minor 14) found the two-verdict version reporting CRLF as drift — and its docstring names
book-of-job as one of the repos that got the correction. **So the inventory had already made the
instrument correction that this programme kept re-learning by hand**, and nothing there needs
fixing. `unknown` and `stale` are both still true and both still right: no copy script has ever
refreshed these files.

The thing to fix is the habit. **Read the artifact before calling it stale** — this claim cost
nothing to check and had been carried in the plan for seventeen days.

### One correction owed to a neighbouring plan: the `59 subtests` figure does reproduce

**SUPERSEDED 2026-08-19 by Phase 1, which re-measured and found no subtests line at all — see
"The `59 subtests` figure does not reproduce" in that phase's record below.** This subsection is
left as Phase 0 wrote it, being that phase's record, but **do not act on it**: the instruction it
issues is the wrong one, and holman-ketiv-qere's Finding 3 was right after all.

MAM-basics' suite, run as this phase's verification at `ebc9669`, reports **947 passed, 5 skipped,
59 subtests passed** in 114s. The programme plan's holman-ketiv-qere row carries a "Finding 3"
saying that third figure does **not** reproduce, that `pytest-subtests` is not installed so pytest
cannot report it, and that the figure should be dropped. **The package is indeed absent** —
`pip show pytest-subtests` says "Package(s) not found" — **and the figure appears anyway**, because
pytest 9.1.0 counts `unittest` subtests natively and needs no plugin for it. So the finding's
number was right and its explanation wrong, and the instruction it issued would delete a figure
that measures something. **Do not drop it**; re-measure it like any other.

### Family 1 — `mb_cmn/`: six differences, all droppable drift, and the family reconciles

Confirmed on blobs: **10 of the 16 identical, 6 differing**, exactly the six the prescription
names. Categories are this plan's own: **(i)** a fix belonging upstream in MAM-basics, **(ii)** a
local adaptation belonging in the moving book-of-job code, **(iii)** drift that can simply be
dropped.

| File | bj / mb lines | The difference | Category |
|---|---|---|---|
| `bib_locales.py` | 640 / 640 | book-of-job's `parse_short_bcv` matches `[A-z0-9][A-z]?`; MAM-basics matches `[A-Za-z0-9][A-Za-z]?`. `[A-z]` is the classic over-wide class, admitting `[`, `\`, `]`, `^`, `_` and backtick between `Z` and `a` | **(iii)** — MAM-basics has the fix |
| `hebrew_accents.py` | 155 / 155 | one comment on the conjunctives list: book-of-job's `# (but mehuppak legarmeih is disjunctive)` against MAM-basics' `mahapakh` | **(iii)** — MAM-basics has the spelling the rest of these repos use |
| `uni_heb.py` | 209 / 264 | MAM-basics adds `he_to_ascii_direct`, `he_ascii_slug` and their three module-level tables, and capitalizes `zinor` to `ZINOR` in three comment lines. Every changed line is an addition on the MAM-basics side or one of those three comments: **MAM-basics is a strict superset** | **(iii)** |
| `uxlc_change_url.py` | 25 / 32 | MAM-basics gives `uxlc_release_xml_url` a `host` parameter defaulting to `tanach.us`, which is what book-of-job's copy hardcodes, so every existing call behaves identically | **(iii)** |
| `hebrew_punctuation.py` | 33 / 17 | book-of-job has `import re` and two functions MAM-basics lacks, `split_at_bog_maq` and `atoms_and_bog_maqs`, which split a phrase at a black **or gray** maqaf | **(iii)** — see below |
| `file_io.py` | 69 / 87 | MAM-basics gives `json_dump_to_file_path` three defaulted parameters, `generator_file=None`, `newline=""` and `indent=2` | **(iii)** — see below |

**No difference in this family is category (i) or (ii).** In five of the six, MAM-basics' copy is
simply the later text and book-of-job's the older; in `hebrew_punctuation.py` the direction is the
other way and the answer is still to drop book-of-job's.

**`hebrew_punctuation.py` — the two extra functions are dead, and MAM-basics never had them.**
`split_at_bog_maq` and `atoms_and_bog_maqs` have no caller anywhere in book-of-job: the only three
hits for either name are the two `def` lines and the one line where the first calls the second
(`git -C book-of-job grep -n 'split_at_bog_maq\|atoms_and_bog_maqs' -- '*.py'`). They arrived on
2026-02-06 in `d6485a3`, "some updates from al-hatorah", and have never been called since. A search
of MAM-basics' whole history for either name returns nothing, so this is not something MAM-basics
deleted — it never had it. MAM-basics does use `NU_GMAQ` in nine modules and splits at a gray maqaf
some other way. Dropping book-of-job's copy therefore loses dead code and nothing else.

**`file_io.py` — behaviour-preserving, but it drags a seventeenth file with it.** All three added
parameters default to what book-of-job's copy already does: `generator_file=None` skips the
provenance injection entirely, `indent=2` is what book-of-job hardcodes, and `newline=""` is what
`_openw` — **byte-identical in the two copies** — already defaults to. book-of-job's two callers
(`pyauthor_util/qr_make_json_outputs.py`, four calls, and `py/boj_html.py`, one) pass two arguments
and would be unaffected. But MAM-basics' copy opens with `from mb_cmn import provenance` at module
level, and **book-of-job has no `provenance.py`**, so re-vendoring `file_io.py` means vendoring
`provenance.py` as well.

**And `provenance.py` does not fit book-of-job's depth.** Its `_repo_root()` is
`Path(__file__).resolve().parents[2]`, which is right at al-hatorah's `py/mb_cmn/` and lands on
`C:\Users\BenDe\GitRepos` from book-of-job's root-level `mb_cmn/`. It would never fire — the whole
chain runs lazily and book-of-job passes no `generator_file` — but it is a wrong root sitting in a
file, and it is **holman-ketiv-qere's Phase 1 finding in a fourth guise**: a `parents[N]` walk that
means one thing under a `py/` and another without one. That is Phase 1's subject here, so the two
decisions are the same decision.

**Family 1's disposition, then:** re-vendor MAM-basics' six over book-of-job's, carry
`provenance.py` in as a seventeenth file, and prove it with the oracle. Nothing is lost, and the
run is worth having for its own sake — it is the evidence Phase 3 needs that MAM-basics' `mb_cmn`
serves book-of-job's code. **Not done in this phase**, per the hard stop below.

### Family 2 — `py_uxlc_loc/`: one tool with drift, whose reconciliation is a design call

**The eight re-measured line counts all reproduce exactly** — `my_uxlc.py` 97,
`my_uxlc_page_break_info.py` 41, `my_uxlc_location.py` 30, `my_uxlc_bibdist.py` 23,
`my_uxlc_lci_augrec.py` 8, `my_uxlc_cvp.py` 4, `my_uxlc_lci_rec.py` 2, `my_uxlc_verlen.py` 2. Three
things the prescription says about this family are nevertheless wrong, and each was cheap to check.

**Correction 1: only ONE module has no counterpart, not two.**
`py_uxlc_loc/my_uxlc_lci_rec_flatten.py` has one — `py/uxlc_lci/uxlc_lci_rec_flatten.py`, differing
by **8** lines, under the same `my_` -stripping rename the other `uxlc_lci/` files took. It was
missed because the prescription's table stops at the eight it lists.

**Correction 2: the remaining one has a counterpart too, under another name.**
`py_uxlc_loc/my_tanakh_book_names.py` (566 lines) is an older copy of what MAM-basics carries as
`mb_cmn/bib_locales.py` (640 lines) — same module, past a rename of its public names:
`ALL_BOOK_IDS` → `ALL_BK39_IDS`, `section()` → `get_secid()`, `book_is_of_sec` → `bk39_is_of_sec`,
with `BK_JOB = "Job"` unchanged in both. MAM-basics' `py/py_uxlc/my_uxlc.py` states the equivalence
in code, having swapped `import py_uxlc_loc.my_tanakh_book_names as tbn` for
`import mb_cmn.bib_locales as tbn`. **So book-of-job carries two copies of that module** —
`mb_cmn/bib_locales.py`, four lines from MAM-basics', and `py_uxlc_loc/my_tanakh_book_names.py`,
its ancestor — and both are live, `job_ov_and_de.py` importing the second while `mb_cmn` supplies
the first. That is the **fifth copy axis inside one repo** the programme's Phase 0 warned about,
met a second time.

**Correction 3, and the big one: MAM-basics has TWO forks of this code, not one, and they differ
from each other.** `py/py_uxlc/` (11 modules) came in from **wlc-utils** on 2026-08-01 (`7e8ee0f`);
`py/uxlc_misc/` and `py/uxlc_lci/` came in from **UXLC-utils** on 2026-08-03. Nine of book-of-job's
ten modules have a counterpart in each. Measured three ways:

| book-of-job `py_uxlc_loc/` | vs `py/py_uxlc/` | vs `uxlc_misc/`, `uxlc_lci/` | the two MAM-basics forks, vs each other |
|---|---|---|---|
| `my_uxlc.py` | **33** | 97 | 78 |
| `my_uxlc_page_break_info.py` | 41 | 41 | 8 |
| `my_uxlc_location.py` | 30 | 30 | 12 |
| `my_uxlc_bibdist.py` | 23 | 23 | 2 |
| `my_uxlc_lci_augrec.py` | 8 | 8 | 8 |
| `my_uxlc_lci_rec_flatten.py` | 8 | 8 | 4 |
| `my_uxlc_cvp.py` | 4 | 4 | **0** |
| `my_uxlc_lci_rec.py` | 2 | 2 | 2 |
| `my_uxlc_verlen.py` | 2 | 2 | 2 |

book-of-job's names match `py/py_uxlc/`'s exactly, and `my_uxlc.py` is three times closer to it, so
**`py/py_uxlc/` is the nearer relative** — but "reconcile onto MAM-basics' copy" names two different
files for every module in the table, and the two are not the same file.

**What the differences actually are.** In **six** of the nine — `my_uxlc_bibdist.py`,
`my_uxlc_lci_augrec.py`, `my_uxlc_lci_rec_flatten.py`, `my_uxlc_cvp.py`, `my_uxlc_lci_rec.py`,
`my_uxlc_verlen.py` — there is **no behavioural difference whatever**: the import prefix
`py_uxlc_loc.` against `py_uxlc.`, and a docstring style where book-of-job has a one-line summary
plus an `__all__` list and MAM-basics folded the names into the docstring and dropped `__all__`.
In the other three the content difference is **one thing, three times**: book-of-job's fork **takes
its data root as a parameter** (`path_to_uxlc`, `path_to_lci_recs`, a `paths_dict`), and
MAM-basics' **hardcodes it** to `paths.in_dir()`. Three smaller items ride along: MAM-basics adds a
`_stripped_text` None-guard and a `CANONICAL_XML_FILE_NAMES` frozenset, and **book-of-job has one
fix MAM-basics lacks** — `get_book_order`'s docstring reads "In particular, the two books of
Chronicles are in" against MAM-basics' "I particular, … are  in", so that one is **category (i)**,
a fix belonging upstream, and the only one in either family.

### What trips the gate: two data snapshots, not two spellings of one

book-of-job's code reads `py_uxlc_loc/UXLC/` (39 XML) and `py_uxlc_loc/UXLC-misc/lci_recs.json`.
MAM-basics' code reads `in/UXLC-39/` (39 XML plus a `_provenance.md`) and `in/lci_recs.json`. **All
39 XML differ as blobs, and the difference is not cosmetic:**

- **The releases are two years apart.** book-of-job's header says `UXLC 2.1`, `1 Apr 2024`, build
  `27.2`; MAM-basics' says `UXLC 2.5`, `1 Apr 2026`, build `27.6`.
- **The text of Job differs.** Ignoring the `<x>` transcription markers 2.5 adds to 48 words,
  `difflib` over the two `<w>` sequences gives **30 edit runs**, and Job's word count moves from
  **8283 to 8288**. Among them: `לֹֽא־` in 2.1 against `לֹֽא` in 2.5, a **maqaf where the newer
  release has none**, so what is one chanted word in the older is two in the newer; three atoms
  exchange a deḥi for a tipeḥa; one exchanges a revia for a geresh; and at Job 6:10, 2.1 has
  וּ֥תְהִי with a merkha where 2.5 has וּֽתְהִי with a meteg (mid-verse, so a meteg and never a
  silluq).
- **The word count is what the estimator runs on.** `my_uxlc_bibdist.py` is "biblical distance
  (word count)", and `my_uxlc_location.py` turns that into a page, column and line estimate in the
  Leningrad Codex. Five more words in Job is an input change, not a presentation change.
- **book-of-job's `lci_recs.json` is RICHER for Job than MAM-basics', not older.** 61 differing
  lines, and they run one way: where book-of-job's records for Leningrad pages **397A** and
  **406A** carry `startco`, `startli`, `stopco` and `stopli`, MAM-basics' carry `null`, and
  book-of-job splits 406A into several ranges MAM-basics keeps as one. That is hand-indexing done
  for this review and held nowhere else.

**Measured, not argued.** Three runs of the oracle, book-of-job's code unchanged except where
stated:

| Data | Reader | Result |
|---|---|---|
| book-of-job's own | unchanged | exit 0, **silent**, 701 artifacts byte-identical |
| MAM-basics' `in/` | unchanged | **crashes** — `AttributeError: 'NoneType' object has no attribute 'strip'` at `my_uxlc.py:53`, on a `<w>` whose tail is `None` because 2.5 put an `<x>` marker inside the word |
| MAM-basics' `in/` | MAM-basics' `_stripped_text` guard applied | exit 0, 701 artifacts byte-identical, **but two new warnings**: `row-0119 fline mismatch` and `row-3210 fline mismatch` |

Three things follow, and the middle one is the surprise.

**MAM-basics' `_stripped_text` is not cosmetic — it is the fix that makes the reader survive UXLC
2.5.** book-of-job's copy lacks it and does not need it, because it reads 2.1. Code and data are
matched to each other on both sides.

**The 701 artifacts do not move.** That was worth measuring rather than assuming, and it is a fact
about what the estimate is *used for*, not about the two datasets being equivalent: `_pg_diff` in
`pyauthor_util/job_ov_and_de.py:85` compares the estimate against the location recorded in the
quirk record and prints a line when they disagree by more than two, and that line goes to stdout
and into no artifact. The two rows that then warn — 0119 and 3210, that is Job 1:19 and Job 32:10 —
sit on pages **397A** and **406A**, which are precisely the two whose column and line coordinates
MAM-basics' `lci_recs.json` has as `null`. So the degradation is exact and traceable: swapping the
data silently turns off the check that validates this review's recorded Leningrad locations.

**So the answer for family 2 is neither of the two the prescription offers.** These are not "two
tools with a common ancestor" needing distinct names — six of the nine differ in nothing but an
import prefix and a docstring, and the other three in one parameter. Nor is plain reconciliation
onto MAM-basics' copies available, because that would silently swap a two-years-newer corpus and a
**coarser** Job index into a published review. It is **one tool with drift whose reconciliation
requires three decisions that are Ben's**, listed at the gate below.

### The gate, and how it was answered

The prescription's gate: stop if 0a finds a genuine behavioural difference the repos need. It did,
in family 2 — MAM-basics' hardcoded data root **cannot be pointed at book-of-job's data at all**
(`read_lci_recs_dot_json()` takes no argument and has no override hook), and the two datasets
differ in the text of Job. Three questions went to Ben, and **all three were answered 2026-08-19**:

1. **Does book-of-job's UXLC snapshot stay at 2.1, or move to 2.5?** — **Move to 2.5.**
2. **What happens to its finer `lci_recs.json` records for Leningrad pages 397A and 406A, which
   exist nowhere else?** — **Upstream, and into BOTH copies of the file.**
3. **Which of MAM-basics' two forks is the target?** — **`py/uxlc_misc/` plus `py/uxlc_lci/`.**

**One fact narrowed question 1 before it was asked.** `MAM-basics/in/UXLC-39/Job.xml` and
`UXLC-utils/in/UXLC-39/Job.xml` are the **same blob**, `c710a1c4`, both UXLC 2.5 — so the snapshot
choice never depended on the fork choice.

### What landed

Four commits, in three repos.

| Commit | Repo | What |
|---|---|---|
| `4d1ad89` | UXLC-utils | the five records into `in/UXLC-misc/lci_recs.json`, plus the four derivatives `main_uxlc_mega.py` rewrites |
| `2979507` | MAM-basics | the same five records into `in/lci_recs.json` |
| `6fb8c06` | book-of-job | `mb_cmn/`: the six re-vendored, plus `provenance.py` |
| `7ca99f7` | book-of-job | UXLC 2.1 → 2.5 across 39 XML, four code edits, and `my_tanakh_book_names.py` deleted |

**The records merge lost nothing, and `page_counts.json` is the independent check that says so.**
397A keeps its span and gains coordinates 1,1 → 3,27. 406A's single null-coordinate record
(31:35p8 → 33:11p2) becomes book-of-job's four, which subdivide **exactly** that span — same
start, same end — so the page length does not move and that file does not change. 979 records
become 982 in both copies, and each merged body is now equal, list for list, to book-of-job's.

**Only the header still differs between the two copies**, in one string of
`column-dictionary.bkid`: UXLC-utils' names `mb_cmn_bib_locales.py` where MAM-basics' and
book-of-job's still name `my_tanakh_book_names.py`. Left alone — it is the evidence of which
lineage each file belongs to.

**Family 1 needed no further decision.** All six took MAM-basics' text verbatim, `provenance.py`
came in as the seventeenth file, and the sixteen shared names are now one blob with
`py/mb_cmn/`. The `parents[2]` in the vendored `provenance.py` still lands on `GitRepos` rather
than on book-of-job; it never fires, and editing a vendored copy would be the drift this phase
exists to end, so it stands as a Phase 1 item.

**Family 2 was reconciled semantically rather than textually.** book-of-job's copies are a pure
deletion in Phase 4 — MAM-basics already holds the code Ben chose — so what Phase 0 owed was proof
that MAM-basics' modules produce book-of-job's artifacts, not a byte-for-byte merge. The four code
edits are each a difference MAM-basics' copies already carry: the `_stripped_text` None-guard,
`mb_cmn.bib_locales` as `tbn` in place of `my_tanakh_book_names`, `ALL_BOOK_IDS` → `ALL_BK39_IDS`,
`section` → `get_secid`, and `ordered_short_dash_full` → `ordered_short_dash_full_39`. The
docstring-and-`__all__` style in which six of the nine modules are MAM-basics' **only** difference
was deliberately left, being cosmetic churn in files about to be deleted.

**`my_tanakh_book_names.py` is gone, and with it book-of-job's second live copy of
`bib_locales`.** The swap was checked rather than assumed: all 39 `BK_*` constants agree in value,
`ALL_BOOK_IDS` equals `ALL_BK39_IDS`, `SEC_SIF_EM` is unchanged, and `ordered_short_dash_full`
agrees with `ordered_short_dash_full_39` on all 39 books. `section` and `get_secid` **disagree on
25 of the 39** — but only in the transliteration of the section-id strings, `NevAḥ` against
`NevAx`, `ḤamMeg` against `XamMeg`, `KetAḥ` against `KetAx` — and the one predicate book-of-job
asks, `section(bkid) == SEC_SIF_EM`, agrees on all 39. **Check the predicate a caller uses, not
the function's whole range**: 25 of 39 disagreeing looks fatal and is not.

**The one difference that belonged upstream went upstream.** `get_book_order`'s docstring reads
"In particular, the two books of Chronicles are in" in book-of-job and read "I particular, … are
in" in **both** MAM-basics forks; book-of-job's is now in both.

### What the oracle says, at each step

Every run is `main_gen_misc_authored_english_documents.py`, compared by reading each HEAD blob
with `git cat-file` rather than by `git status`:

| After | Artifacts | Generator output |
|---|---|---|
| nothing (baseline at `33b3ee2`) | 700 identical, 1 line-ending-only, **0 content differences** | silent |
| `mb_cmn/` re-vendored | same | silent |
| UXLC 2.5 and the four code edits | same | **silent** |

**That the last run is silent is the result worth having.** The same code on MAM-basics' *coarse*
`lci_recs.json` prints two `fline mismatch` lines, at rows 0119 and 3210 — the two quirk records
sitting on pages 397A and 406A. book-of-job's copy already held those coordinates, which is why it
is the copy that went upstream, and with it the location cross-check is as quiet on UXLC 2.5 as it
was on 2.1. **The corpus moved two years and the review's 160 recorded Leningrad locations still
check out.**

`check_all.py` passes all 7 checks after each step — the first time it has run in book-of-job at
all, the venv having held one of the five packages `requirements.txt` names. black leaves every
edited file unchanged. MAM-basics' suite stays at 947 passed, 5 skipped, 59 subtests passed.

**Two findings for the codex-index trio.** `main_write_page_break_info.main()` reads
`data/lci_recs.json` and only **then** copies `in/UXLC-misc/lci_recs.json` over it, so a change to
the hand-maintained source needs **two runs** to reach the derivatives; the first run here left
`lci_augrecs.json` at 979 while `lci_recs.json` had already become 982. And
`out/UXLC-misc/all_changes_loc_checks.json` moved: 9 of its 1399 entries changed, 5 better and 4
worse, total absolute `fline_diff` over those 9 falling **33.03 → 12.38**. The win is the worst
case, 397A column 3 line 21 going from **23.69 lines out to 1.47**. The 4 that worsen are all on
406A column 1 and all by about 2.3 lines, which is systematic rather than random: the subdivision
leaves lines 11 and 20 of that column blank, and `fline` arithmetic assumes 27 contiguous lines
per column, so the recorded line and the estimate now count differently. **Left as it stands** —
it is a question about what the UXLC change data's line numbers count, and it is Ben's.

---

## Phase 1 — two roots, no cwd — **DONE 2026-08-19**

**Landed as `45f8853` in book-of-job (18 files, +305/−100), which adds `boj_paths.py`. Nothing
was owed in MAM-basics.** The prescription this record answers is the section below it, left as
written.

**Every baseline was re-measured first and every one matched**: 267 tracked `.py` (`mb_cmn/` 17,
`py_uxlc_loc/` 9), 16,859 lines, 701 tracked artifacts, all at `7ca99f7`. After the commit,
**268** and **17,064** — both of them `boj_paths.py` and the net of the edits. **Phase 3 and
Phase 4 therefore face 268 files, not 267.**

**The verification ran from `C:\Users\BenDe\GitRepos\MAM-basics` as the working directory**, on
book-of-job's own interpreter by absolute path, and passed: the oracle **silent**, all **701
artifacts byte-identical** against their HEAD blobs, **MAM-basics' tree untouched** before and
after, `check_all.py` **7 of 7**, the NFC suite **6 tests, OK**, and every one of the five entry
points importing and resolving each of its roots into book-of-job. black clean on all 18 files.
The two checks that count files report **326** for mark order and **268** `.py` for escapes,
against Phase 0's 325 and 267 — one more file each, which is `boj_paths.py` and nothing else.

### The `59 subtests` figure does not reproduce, and Phase 0's correction of it was wrong

MAM-basics' suite, run as this phase's verification at `7bf4e00`, reports **947 passed, 5 skipped**
in 90.5s — **no subtests line at all**. Run twice, identically. 952 collected, which is 947 + 5.

Phase 0's record says that figure "does reproduce", reports **947 passed, 5 skipped, 59 subtests
passed**, and instructs later phases not to drop it, on the explanation that "pytest 9.1.0 counts
`unittest` subtests natively and needs no plugin for it". **It does not.** Measured here:
`self.subTest` is used in **25** of this repo's test files, `pytest-subtests` is absent
(`pip show` → "Package(s) not found", the same answer Phase 0 got), pytest is 9.1.0, `main_test.py`
passes no plugin flags and the repo has no pytest config — and the summary line carries no subtests
count. The subtests still *run*, inside each `TestCase` through unittest's own machinery; what
requires the plugin is **counting them in the summary**.

**So holman-ketiv-qere's "Finding 3" was right on the substance** — the figure does not reproduce,
and a baseline that carries it will not be matched — **and it was Phase 0's correction that was
wrong, not the finding.** Phase 0 was right that the reason given for dropping it ("pytest cannot
report it") deserved checking, and right to say "re-measure it like any other"; re-measuring is
what produced this. **The standing baseline for MAM-basics' suite in this programme is
`947 passed, 5 skipped`**, and the third figure should be dropped after all — from this plan, from
the programme plan, and from the codex-index trio's, none of which should now go looking for it.

### `boj_paths.py`, and why it does NOT vendor `mb_cmn/paths.py`

**This repo does not vendor `mb_cmn/paths.py` and must not start.** UXLC-utils' Phase 1 hit the
same absence and answered it by vendoring the file in; that answer is wrong here, and the reason
is the shape of this repo rather than a preference. `paths.repo_root()` is
`Path(__file__).resolve().parents[2]` — correct for a `py/mb_cmn/` two levels down, and wrong
here, where `mb_cmn/` sits at the **repo root** and that walk lands on `GitRepos`. Vendoring it
verbatim would import a broken root; editing the vendored copy is the drift Phase 0 exists to
end. So `boj_paths.code_root()` walks up to the nearest ancestor holding `.git` instead — the
identical idiom the programme's Phase 0 put into `check_escape_sequences.py`, `check_mark_order.py`,
`fix_mark_order.py` and `py_ac_word_image_helper/codex_page.py` in this same repo, and
depth-independent for exactly the reason that phase gives.

**So the Phase-2-does-not-recur conclusion holds here, but by a different route than at
holman-ketiv-qere**, which had `paths.py` already and byte-identical. Three repos, three answers:
holman inherited it, UXLC-utils vendored it, book-of-job cannot and does not. **Check it per repo
at the codex-index trio, and check the depth of `mb_cmn/` as well as its presence** — that is what
decides which of the three answers applies.

At the move, **two lines change**: `boj_data_root()` becomes
`paths.require_sibling("book-of-job", paths.sibling_repo("book-of-job"))`, and `code_root()` may
become `paths.repo_root()` or stay as it is, the `.git` walk resolving to MAM-basics' root once
the code lives there. Nothing else composes a data path off anything but `boj_data_root()`.

### The prescribed grep undercounted by six, and two of the seven it found are false positives

Re-run at `7ca99f7`, `git grep -nI '"gh-pages/\|"out/\|f"gh-pages/' -- '*.py'` returns the seven
sites the section below names. **Six more needed changing that it cannot see**, and one of them is
the one that actually broke a foreign-cwd run:

- **`pyauthor_util/job_ov_and_de.py:35,36`** — `paths_dict`'s `"py_uxlc_loc/UXLC"` and
  `"py_uxlc_loc/UXLC-misc/lci_recs.json"`. **The grep never looked for that prefix.** These are
  the first paths the oracle touches after the CSS files, so a run from MAM-basics dies here with
  `FileNotFoundError: 'py_uxlc_loc/UXLC/Genesis.xml'` — which is also the proof that the phase
  had something real to fix. Note what the directory name hides: `py_uxlc_loc/` is **data** as
  well as code, the trap the "Two directory names are traps" subsection above already names.
- **`pyauthor_util/author.py:134`** — `_Path("gh-pages") / "jobn" / img_prefix / img_path`, inside
  `para_for_img`. No slash inside the quotes, so no leading-quote search finds it.
- **`check_html_syntax_and_sanity.py:48`** — an argparse `default="gh-pages"`, which `check_all.py`
  always took, having passed no `pages_dir`. The same shape as holman's `main_just_render_table`
  defaults, and the same reason a grep misses it.
- **`check_spelling_in_html.py:308`** — `out_dir = project_root / "out"`, a **third** site in a
  file the prescription gave two of.
- **`check_qr_consistency.py:121`** — `Path("pyauthor_qr")`, and **`check_function_ordering.py:67`**
  — `Path(".")`. Both cwd-relative scans of **source**, so they take `code_root()` rather than the
  data root. Neither is in the shared `check_*`/`fix_*` family: book-of-job alone has these two
  files, checked against both codex-index repos.

**And `test_h_dot_below_nfc.py:78,79` are not path construction at all.** `"out/"` and
`"gh-pages/"` there are entries of `_EXCLUDE_DIR_PREFIXES`, repo-relative prefixes matched against
each scanned file's path — nothing builds a path from them, and rewriting either would be a bug.
Left alone, with a docstring note added so nobody "fixes" them later. That module's `_repo_root()`
shells out to `git rev-parse --show-toplevel` and is already cwd-independent, so it does not take
`code_root()` either. **Two of seven grep hits wrong in the same direction is worth carrying to
the trio**: read what a hit *does* before counting it an offender.

### The fault named in one sentence, and the one file where both roots met

Holman-ketiv-qere's Phase 1 concluded that the fault is root **conflation** rather than
cwd-relativity, and the programme's Order item 2 promoted that to the thing to grep for. **Here it
is both, in roughly equal measure**, and `check_spelling_in_html.main()` is the miniature of the
whole phase: one `Path(__file__).parent`, bound once as `project_root`, composed the `gh-pages`
tree it reads — DATA, which stays in book-of-job — *and* the custom dictionary that sits beside
its own module — CODE, which follows the Python. **One expression standing for two roots**, which
no grep for a string literal can find and which a move silently resolves into the wrong tree. The
two now say which root they mean, and the dictionary keeps `Path(__file__).parent` deliberately,
that being right at whatever depth the module comes to rest.

### The foreign-cwd verification convention would have clobbered a tracked MAM-basics file

UXLC-utils' and holman-ketiv-qere's Phase 1 records both verify by running from
`C:\Users\BenDe\GitRepos\MAM-basics`. **Run that way *before* the fix, book-of-job's oracle writes
`gh-pages/index.html` and `gh-pages/style.css` cwd-relatively, and MAM-basics has a tracked
`gh-pages/index.html` of its own.** It would not have failed; it would have overwritten that file
and reported success. Neither of the other two repos had the collision — neither writes a bare
`gh-pages/index.html` — so the convention had never been tested against a repo that did.

The failure was demonstrated instead from an empty scratch directory, where it dies loudly on
`FileNotFoundError: 'gh-pages/style.css'` for want of a `gh-pages/` to write into. **That loudness
is an accident of the empty directory, not a property of the bug.** At the codex-index trio, check
what the entry points write to a bare relative path before running one from MAM-basics; two of the
three write a `gh-pages/` tree.

### Two root walks left deliberately untouched, both because Phase 0 made them shared blobs

The programme's Order item 4 hands this phase `py_ac_word_image_helper/flat_index.py:7`, whose
`Path(__file__).resolve().parent.parent.parent` resolves to `C:\Users\BenDe\GitRepos` because the
package sits at this repo's root. **It is wrong, and it is not this phase's to fix.** Verified
2026-08-19 on committed blobs: all six files of `py_ac_word_image_helper/` are **one blob** with
codex-index-aleppo's `py/py_ac_word_image_helper/`, and all four of `py_cam1753_word_image/` are
one blob with codex-index-cam1753's — `flat_index.py` at `af610508` and `page.py` at `73b3d80d`
in both repos of each pair. Editing either in book-of-job alone re-forks the family that Phase 0
had just reconciled, for a module nothing runs.

**How the wrongness got past Phase 0 is the transferable part.** That phase reviewed *sixteen
files that had diverged*, and replaced the `parents[N]` walk with the `.git` walk in the four of
them that carried one — `codex_page.py` among them, its `ROOT` depth being the whole of its diff.
`flat_index.py` was **already byte-identical** and so never entered the review. It is identical
and therefore wrong in one of the two repos: `parent.parent.parent` is the repo root in
codex-index-aleppo, where the package sits under a `py/`, and `GitRepos` in book-of-job, where it
does not. **A file being one blob across two repos is not evidence that the blob is right in
both** — it is evidence that a depth-counting walk in it is right in at most one. Step 5 should
sweep the reconciled packages for `parents[`/`.parent.parent` outright rather than only the files
that differed.

Two facts bound how much this costs. **Nothing imports `flat_index.py`** — not the four modules
`main_gen_aleppo_crop_editor` pulls from its package, not anything in either repo; and
`index-flat-annotated.json`, the file it names, exists in codex-index-aleppo and at **neither**
`GitRepos\index-flat-annotated.json` nor book-of-job's root, so both the wrong root and the right
one raise. It is unreachable code inside a package the programme's Phase 0 already established is
dead here, book-of-job having none of the six data directories the two word-image packages need.

**`py_cam1753_word_image/page.py:10` is a different case and needs saying separately**, because
the Order item groups the two. Its `Path(__file__).resolve().parent.parent` is the repo root in
book-of-job **and** in codex-index-cam1753, both of which hold that package at the root — so it is
**correct in both today** and is not a defect at all. It becomes wrong only when book-of-job's copy
lands under MAM-basics' `py/`, which makes it **a Phase 3 item**, and one that has to be settled
in both repos at once or not at all.

### `mb_cmn/provenance.py`'s `parents[2]` — the facts, and the question that is Ben's

Phase 0's record left this as a Phase 1 item and the Order item repeats it. **Phase 1 did not pick,
and the question stands.** What is now established:

- **Four copies exist**, swept across `GitRepos` and `MAM-private` on 2026-08-19: MAM-basics
  `py/mb_cmn/`, MAM-private `al-hatorah/py/mb_cmn/`, MAM-simple `py-examples/mb_cmn/`, and
  book-of-job `mb_cmn/`. **`_repo_root()`'s `parents[2]` is right in three of the four** — each of
  those sits two levels below its repo root — and wrong only in book-of-job, whose `mb_cmn/` is one
  level below. So "re-vendor everywhere" is really "re-vendor into one repo"; the other two need no
  new bytes whatever is decided.
- **The wrongness is latent, and stays latent.** Nothing in book-of-job passes `generator_file` to
  `mb_cmn.file_io`, so `this_repo_name()` and `_display_path()` never run and no artifact here
  carries a breadcrumb. `git grep -lI "generated by book-of-job" -- gh-pages out` returns **0**,
  which also means **Phase 6's blast radius in this repo is nil**, the same finding UXLC-utils'
  Phase 1 recorded for its own. Were it to fire, the breadcrumb would read
  `GitRepos/book-of-job/...`: `_common_git_dir(GitRepos)` finds no `.git`, so the chain degrades to
  step 4 and names the directory `GitRepos`.
- **Phase 4 deletes book-of-job's `mb_cmn/` outright**, all 17 files, so the wrong walk disappears
  without anyone touching it.
- **The file already contains the machinery for the depth-independent answer.** `_common_git_dir`
  reads git's own files and handles a worktree's `.git` file; a `_repo_root()` that walked to `.git`
  would be self-consistent with it and correct at every depth.

**The question for Ben: leave it, with these facts recorded, or change MAM-basics'
`py/mb_cmn/provenance.py` to walk to `.git` and re-vendor into book-of-job?** The first costs
nothing and expires at Phase 4. The second is a cross-repo change to a file four repos share, for a
defect that never fires — but it is also the one that stops the next repo hitting it. Put to him
2026-08-19; **do not let a later phase pick this silently.**

### Five things Phase 3 now owes, three of them new

- **MAM-basics' `py/uxlc_misc/my_uxlc.py` has no `path_to_uxlc` parameter.** Its `read()` calls a
  hardcoded `canonical_xml_path(book_id)` where book-of-job's takes the path as an argument — the
  hardcoded data root Phase 0's gate found, still hardcoded. book-of-job's nine `py_uxlc_loc/`
  modules are a pure deletion, so **Phase 3 must give MAM-basics' copy the parameter, or point
  book-of-job's data at `in/UXLC-39/`**, and that is a real code change rather than a repoint.
  Phase 1 needed no edit there: `job_ov_and_de.py` now hands `prep()` a `Path`, and every module
  under `py_uxlc_loc/` takes it as an argument and passes it to `open()` or
  `ElementTree.parse()`, both of which accept one. **Not one file under `py_uxlc_loc/` was
  touched**, which is what keeps that deletion clean.
- **`py_cam1753_word_image/page.py`'s depth**, above — settle it in book-of-job and
  codex-index-cam1753 together.
- **`test_h_dot_below_nfc.py` folds into this repo's file of the same name**, as holman's did:
  add a `_Scope` rooted at book-of-job's data root and delete book-of-job's copy. Its
  `_EXCLUDE_DIR_PREFIXES` are repo-relative and will need re-rooting with it.
- **MAM-basics' venv has no `pyspellchecker`** and `check_spelling_in_html.py` imports it at module
  level — carried forward from Phase 0's record, still true, still Phase 3's to fix.
- **`py/boj_html.py`'s `WriteCtx.path` is now annotated `Path`**, not `str`. It flows to the
  vendored `mb_cmn.file_io.with_tmp_openw`, whose `os.path.dirname` and `pathlib` arithmetic both
  take one, so **the vendored file needed no change** — the same finding UXLC-utils' Phase 1
  recorded for its own `WriteCtx`.

One behavioural change worth naming because it is invisible in the diff: `_delete_files` in the
oracle went from `glob.glob(f"{directory}/{pattern}")` to `directory.glob(pattern)`, and
`Path.glob` matches leading-dot names where `glob.glob` does not. There are no dotfiles under
`gh-pages/jobn/` or `gh-pages/jobn-details/`, so the two agree; the artifact comparison would have
shown it either way, as a missing file or an untracked one, and showed neither.

---

The rest of this section is the plan as written 2026-08-02, before the phase ran. The seven
offenders it names were the starting point, not the total — see the undercount above.

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

## Phase 3 — copy the Python in (dual residency) — **DONE 2026-08-19**

**Landed as `ef8e384` in MAM-basics (243 files added, 1 modified). Nothing was owed in
book-of-job, whose HEAD is `45f8853` before and after and whose tree is content-clean.**
A second commit, `a585cb6`, precedes it and is not part of the move — see "One tracked
artifact was stale, and Phase 0 is what made it so" below. The prescription this record
answers is the section below it, left as written.

**Every baseline was re-measured first and every one matched**: 268 tracked `.py` in
book-of-job (`mb_cmn/` 17, `py_uxlc_loc/` 9), 17,064 lines, 701 tracked artifacts, all at
`45f8853`; MAM-basics clean at `634e5b6` with **947 passed, 5 skipped**. The baseline
oracle run was silent and gave 700 byte-identical, 1 line-ending-only, 0 content
differences, and `check_all.py` 7 of 7 over 326 files and 268 `.py`. **No figure this
phase inherited was wrong**, which is worth saying because the two phases before it each
found several that were.

### The oracle passed on the first run from MAM-basics, and on every run since

Silent, exit 0, and all **701 tracked artifacts byte-identical** to their HEAD blobs.
Measured by reading each blob with `git cat-file --batch` and comparing bytes, never by
`git status --porcelain`, which cannot be used in book-of-job — Phase 0's instrument note
holds, and the 183 files a clean run rewrites still report as modified there.

| Run | Artifacts | Generator output |
|---|---|---|
| baseline, book-of-job's copy from its own root | 700 identical, 1 line-ending-only, **0 content differences** | silent |
| MAM-basics' copy, cwd = MAM-basics | same | silent |
| MAM-basics' copy, cwd = `C:\Users\BenDe\GitRepos` | same | silent |
| book-of-job's copy again, after the move | same | silent |

The one line-ending-only file is `out/cam1753-crops.json`, which the oracle does not
write and whose checkout is still CRLF — the same one Phase 0 and Phase 1 each found.
**No `fline mismatch` line in any run**, so the location cross-check still has the 397A
and 406A coordinates Phase 0 sent upstream. `check_all.py` passes 7 of 7 from MAM-basics
and, unchanged, 7 of 7 from book-of-job. MAM-basics' suite is **947 passed, 5 skipped**,
the baseline exactly.

**Both residencies produce the same bytes**, which is what "dual residency" has to mean
and was cheap to check: book-of-job's own interpreter running book-of-job's own copy, and
MAM-basics' interpreter running MAM-basics' copy, give the same 701.

### The four names, and why the fourth was not optional

Ben settled all four together, 2026-08-19, on the recommendation that the quirk records
carry the `boj` marker rather than the bare `author_qr/` Decision D had proposed:

| book-of-job | MAM-basics | Files |
|---|---|---|
| `pyauthor_qr/` | `py/author_boj_qr/` | 160 |
| `pyauthor_util/` | `py/author_boj_util/` | 33 `.py` + `quirks-BHQ.txt` |
| `pyauthor/` | `py/author_boj/` | 10 |
| `py/` | `py/boj_render/` | 7 |

`pydiff_mm/` (5), `py_ac_word_image_helper/` (6) and `py_cam1753_word_image/` (4) kept
their names, and the sixteen runnable modules plus `boj_paths.py` landed at the top of
`py/`. **363 import rewrites across 105 files.** The fourth rename is the one that had to
happen whatever it was called: `py/hebrew_letter_words.py` would otherwise have landed as
a top-level module beside `mb_misc/hebrew_letter_words.py` — two module objects for one
name, reached with no `sys.path` line at all.

**243 files landed, not the 251 the prescription names.** That figure was 267 minus the
16 `mb_cmn` files, and three things have moved since: `mb_cmn/` became 17,
`py_uxlc_loc/` became 9 and is also a deletion, `boj_paths.py` was added by Phase 1, and
`test_h_dot_below_nfc.py` folds into this repo's file rather than landing. 268 − 17 − 9 −
1 = **241 `.py`**, plus `quirks-BHQ.txt` and the spelling dictionary, which is CODE and
travels beside its module.

### The UXLC parameter the plan demanded is not needed, and that was measured

Item 1 of Phase 1's handover says MAM-basics' `uxlc_misc/my_uxlc.py` has no
`path_to_uxlc` parameter where book-of-job's fork takes the path as an argument, and that
Phase 3 must **either** give MAM-basics' copy the parameter **or** point book-of-job's
data at `in/UXLC-39/`. Neither, as it turns out, and the reason is that Phase 0 already
did the work:

- **All 39 UXLC XML are one blob** across book-of-job's `py_uxlc_loc/UXLC/`, MAM-basics'
  `in/UXLC-39/` and UXLC-utils' `in/UXLC-39/`. Verified on committed blobs, 39 of 39 both
  ways.
- **`lci_recs.json` differs in one line.** book-of-job's copy and MAM-basics'
  `in/lci_recs.json` are the *same blob*, `a34c1075`; UXLC-utils' `data/lci_recs.json` and
  `in/UXLC-misc/lci_recs.json` are `ed3f4d1d`, and `diff` between the two gives exactly
  one line — the header column dictionary's gloss naming `mb_cmn_bib_locales.py` against
  `my_tanakh_book_names.py`, which Phase 0 recorded and deliberately left. The `body`,
  which is all `lci_rec.unflatten_many` reads, is identical.

So `job_ov_and_de.make_ov_and_de` now calls `my_uxlc_location.prep()` with no arguments,
`boj_paths.uxlc_dir()` and `lci_recs_path()` are deleted, and **nothing was added to
`uxlc_misc` or `uxlc_lci`**. Declining to add the parameter is the point: those three
modules' only content difference from book-of-job's fork *was* that parameter, so putting
it back would have re-imported the drift Phase 0's reconciliation dropped.

**What that costs, stated plainly:** regenerating book-of-job's site now needs UXLC-utils
checked out as well as MAM-basics and book-of-job. `paths.require_sibling` makes a missing
sibling a loud failure rather than a silent wrong answer, which is why this is a
dependency and not a hazard. It also leaves book-of-job's 39 XML and its
`lci_recs.json` read by nobody — **40 orphaned data files, and a Phase 4 question**, not
one this phase should answer while the deletion of that repo's Python is still pending.

### Four source lints had to be told what they lint — the one fork the move forced

In book-of-job, `check_function_ordering`, `check_mark_order`, `check_escape_sequences`
and the two `fix_*` scripts scanned the repo root, which held nothing but this code. Here
that same root holds all of MAM-basics, and **none of the three checks has a repo-wide
meaning**. Measured 2026-08-19, before anything was changed:

| Check | Over MAM-basics' `py/` | Over the book-of-job packages |
|---|---|---|
| function ordering | **1172 violations** | 0 |
| mark order | violations in `py/ws/ws_bot_edit_old_joshua_meteg.py` | 0 |
| unnecessary `\uXXXX` escapes | violations in `py/wlc_cmn/wlc_bracket_note_definitions.py` | 0 |

All five now take their scope from `boj_paths.code_paths()`, which returns the seven
packages, the sixteen modules and the one data file by name. **`check_escape_sequences.py`,
`check_mark_order.py`, `fix_escape_sequences.py` and `fix_mark_order.py` were one blob
with codex-index-cam1753's copies and no longer are.** That is the same trap the plan
names for `page.py`, and here it could not be avoided: a `.git` walk finds a repo root and
**cannot find a subtree**, so the shared file's one assumption is false in its new home.
codex-index-cam1753's copies are untouched, and the trio's own plan will meet this wall
when its Python moves.

**`fix_mark_order.py` is the one that mattered most.** It has no `main()`, no dry-run and
no `--apply`: it rewrites every file under the root it finds, at import. Left alone it
would have reformatted MAM-basics on sight, including the `py/ws/` file the mark-order
check reports above.

**The price of the scope list, stated where the list lives:** `BOJ_PACKAGES` and
`BOJ_TOP_LEVEL_MODULES` are hand-maintained, so a book-of-job module added to `py/` and
not listed goes unlinted. `code_paths()` raises on an entry that no longer exists, so a
rename or a deletion fails loudly and only an unlisted addition is silent — and
book-of-job's Python is being evacuated rather than developed.

### Mark order reads BOTH roots, and scoping it to the code alone was a silent loss

Caught by watching the count rather than the verdict. `check_all.py` reported **7 of 7**
with mark order over **241** files where book-of-job's run reports **326**, and 326 − 241
is not the 27 files that were deleted or folded: it is those 27 plus **58 `.json` that
never left book-of-job**. This check reads `.json` as well as `.py`, and the corpus keeps
24 hand-made line-break files under `py_ac_loc/`, `out/`'s seven, and the rest.

So `_scoped_files()` yields the code paths **and** the `.json` under
`boj_paths.boj_data_root()`, and the check now scans **300** files — 241 `.py`, the moved
spelling dictionary, and 58 in the corpus, which becomes 299 when Phase 4 deletes
book-of-job's copy of that dictionary. Spanning two roots also broke `path.relative_to`,
which raises on every file under the root it was not given; `_display_path` tries both.

**The transferable part:** a lint that loses its inputs goes on printing OK. Nothing
failed, no artifact moved, and the only symptom was a number in a success message. When a
check changes scope, **read what it counted, not whether it passed.**

### Two lints in this repo fired on the arriving code, and both were worth having

**`test_transliterations.py` (wlc-utils#26) failed the suite**, on
`author_boj_util/author.py:468 tipeha -> tipeḥa (U+1E25)`. The value was already the
precomposed `tipeḥa`; what the lint saw is the ASCII substitution **key**, `$tipeha`,
which spells ḥet with `h` where its fifteen neighbours in the same table spell it with `x`
— `$tarxa`, `$dexi`, `$munax`, `$patax`, `$xataf`. Renamed to `$tipexa`. **Safe to the
byte, because the key has no user**: that table row is its only occurrence in all 241
files, so no quirk record ever substituted it and no artifact could move. The `# translit-ok`
pragma was the wrong answer here — that mechanism is for external vocabularies and
verbatim citations, and this token is book-of-job's.

**`check_function_ordering` failed on a function this phase wrote**, `display_path`,
public and placed after a private. Renamed `_display_path`. The check earning its keep on
the first new code it saw is the argument for keeping it scoped rather than dropping it.

### The NFC test gains a fourth scope

`py/tests/test_h_dot_below_nfc.py` now scans **four** repos, book-of-job joining
MAM-basics, UXLC-utils and holman-ketiv-qere, and that repo's own 331-line copy is
superseded — it locates its root by `git rev-parse` from its own directory, so copied here
it would have scanned MAM-basics, which is exactly what the UXLC-utils and
holman-ketiv-qere scopes were added to prevent.

- **`_BINARY_EXTENSIONS` were diffed, as the plan asks**, that being how holman's phase
  found a missing `.docx`. **book-of-job's sixteen extensions are a strict subset of this
  file's**, so nothing was owed. Recording the negative result because the instruction to
  check will be given again at the codex-index trio.
- **Seven exclusion prefixes came over re-rooted**, `out/`, `gh-pages/`,
  `py_uxlc_loc/UXLC/`, `py_uxlc_loc/UXLC-misc/` and three under `py_ac_loc/`. Two of them
  name a directory whose `py_` prefix promises Python and delivers data, which is why they
  are spelled to the subdirectory: `py_ac_loc/line-breaks/` is hand-made JSON and stays in
  scope.
- **The floor is 30**, against book-of-job's own 200. 312 files are in scope today and
  **42** after Phase 4, since two of the 44 non-`.py` in scope came here with the code.

### The venv needed more than the plan's item 4 said

Item 4 names `pyspellchecker`, and it is right that `check_spelling_in_html.py` imports it
at module level. **`numpy` was missing too**, and without it neither crop editor imports:
`py_ac_word_image_helper/crop.py` and `py_cam1753_word_image/crop.py` both use it. Both
packages are installed here now.

**`matplotlib` is not**, and that is a finding about book-of-job rather than about this
repo: its `requirements.txt` names black, matplotlib, numpy, Pillow and pyspellchecker,
and `git grep matplotlib -- '*.py'` in that repo returns **nothing**. Phase 0 installed
that file wholesale to get the oracle running and had no reason to notice. **At the
codex-index trio, read what the code imports, not only what `requirements.txt` declares.**

### The two word-image packages: one root walk repaired, one broken, neither touched

Phase 1 left `py_ac_word_image_helper/flat_index.py` and `py_cam1753_word_image/page.py`
alone because each is one blob with a codex-index repo's copy, and handed `page.py` to
this phase. **Both are still untouched, and both blobs are still shared.** The move
settles them in opposite directions, which is the part worth recording:

- **`flat_index.py`'s `parent.parent.parent` becomes RIGHT.** It lands on MAM-basics'
  root, exactly as it does in codex-index-aleppo, where that package also sits under a
  `py/`. The move repairs it for free — the wrongness Phase 1 recorded was book-of-job's
  root-level placement, and that placement is what ended.
- **`page.py`'s `parent.parent` becomes wrong**, naming `py/` where it named a repo root
  in both book-of-job and codex-index-cam1753.

**It is inert either way, which is why leaving it is not negligence.** The three
directories it names — `cam1753-line-breaks`, `cam1753-col-quads`, `cam1753-pages` — are
**absent from book-of-job**, checked 2026-08-19, and absent from MAM-basics; so the walk
resolved to a real root and named nothing, and now resolves to a wrong root and names
nothing. The plan's own instruction is to settle it in both repos at once or not at all,
and "not at all" is what this phase took.

### One tracked artifact was stale, and Phase 0 is what made it so

`doc/vendoring-inventory.md` still reported book-of-job's six `mb_cmn` files as `DIFFERS`.
They have not differed since `6fb8c06`, which re-vendored them and brought `provenance.py`
in as a seventeenth; nothing regenerated the inventory afterwards. `py/main_vendoring.py
--all` now reports them `identical`, and the book-of-job rows collapse from three to two —
21 rows over 128 files become 20 over 129. Committed separately as **`a585cb6`**, before
the move, so the move's own diff carries nothing that is not the move. Re-run after the
move: **unchanged**, the 243 new files sitting under no scan root
`in/vendoring_policy.json` declares. Phase 7 regenerates it again after deleting that
repo's entry.

**This is the other half of Phase 0's own lesson.** That phase spent a subsection under
the heading "Read the artifact before calling it stale" on having wrongly called this
exact file stale — and it was right about the file as it stood that morning, then made it
stale by evening. So: **re-read the artifact after changing what it measures, not only
before.**

### Four corrections to the prescription below

- **"251 files land"** — 243 do, as counted above.
- **"Do the three `pyauthor*` renames"** — there are **four** renames, the fourth being
  book-of-job's own `py/` to `boj_render/`, which the plan's "Two names in `py/` collide by
  meaning" subsection already argues for without counting it among the renames.
- **"watch `force_utf8_io()` where an entry point becomes a library module"** — there is
  nothing to watch. **book-of-job has no stdio reconfiguration anywhere**, in any of its
  268 `.py`: `grep -rn 'reconfigure\|force_utf8\|PYTHONUTF8'` over the moved code returns
  nothing. No entry point became a library module either; all five stayed entry points.
  The concern is real in the abstract — the oracle's stdout must stay silent, and does —
  but it names a mechanism this repo never adopted.
- **"`git status --porcelain` empty in both"** — empty in MAM-basics, and it is the
  assertion there. In book-of-job it is the wrong instrument, as Phase 0 established at
  length in this same document; the byte comparison against HEAD blobs is what this phase
  used, and `git diff --stat HEAD` empty is the cheap confirmation beside it.

### What Phase 4 now owes, beyond what it already knew

- **40 orphaned data files.** `py_uxlc_loc/UXLC/` (39 XML) and
  `py_uxlc_loc/UXLC-misc/lci_recs.json` are read by nothing once book-of-job's Python
  goes, the moved code reading UXLC-utils' copies instead. All 39 XML are one blob with
  UXLC-utils' and MAM-basics' copies; `lci_recs.json` is one blob with MAM-basics'
  `in/lci_recs.json`. **Nothing is lost by deleting them and nothing breaks by keeping
  them**, so it is a question for Ben rather than a mechanical step.
- **`pyauthor_util/quirks-BHQ.txt` and `check_spelling_in_html.custom-dict.json` are
  already here**, so Phase 4 deletes them there as well as the `.py`. Otherwise
  `pyauthor_util/` survives as a one-file directory in a repo declared to have no Python.
- **The NFC scope's floor of 30 assumes 42 files remain.** If Phase 4 deletes more of the
  corpus than the `.py` plus those two, re-check it.
- **`check_all.py` and the four lints run from MAM-basics now**, so book-of-job's
  `CLAUDE.md` should say so rather than naming its own root-level scripts.
- **The mark-order count becomes 299** when book-of-job's copy of the spelling dictionary
  goes, from 300 today.

---

The rest of this section is the plan as written 2026-08-02, before the phase ran.


251 files land, which makes this the largest single phase in the programme — but **160 of them are
one-dict modules that nothing imports except by name**, so the risk is concentrated in the other
91. Do the three `pyauthor*` renames here, together, having decided the three names first.

Otherwise as in the other plans: land the files, retarget the data root to `../book-of-job`, fold
the one test module in, watch `force_utf8_io()` where an entry point becomes a library module, and
finish with the oracle run from MAM-basics writing into `../book-of-job` with
`git status --porcelain` empty in both.

**Must complete in a single session, and stop and ask Ben first.**

## Phase 4 — empty book-of-job — **DONE 2026-08-21**

**Landed as `a846585` in book-of-job (320 files: 317 deletions, 3 modified) and `cff95f7`
here (14 files).** Ben was asked first, as this section and the task prompt both require,
and answered one question: **delete book-of-job's 40 orphaned UXLC data files** rather than
keep them. The prescription this record answers is the section below it, left as written.

**Every baseline was re-measured first and every one matched.** book-of-job at `45f8853`,
clean, 268 tracked `.py` (`mb_cmn/` 17, `py_uxlc_loc/` 9), 17,064 lines, 701 tracked
artifacts, 1103 tracked files; MAM-basics clean at `f9b6245` with 241 copies of the moved
code; UXLC-utils clean at `4d1ad89`. The baseline oracle run was silent and gave 700
byte-identical, 1 line-ending-only, 0 content differences; `check_all.py` 7 of 7 with mark
order over 300 files and escapes over 241 `.py`. **No figure this phase inherited was
wrong, and that is now true of Phases 3 and 4 both.**

### Ben's decision: delete the 40, and what that costs

Phase 3 pointed the moved code at UXLC-utils' copies after proving the data equivalent, so
`py_uxlc_loc/UXLC/` (39 XML) and `py_uxlc_loc/UXLC-misc/lci_recs.json` were read by
nothing. Confirmed again before asking: in MAM-basics' copy of the code the only two
mentions of `py_uxlc_loc` are a docstring line in `py/boj_paths.py` and two **exclusion**
prefixes in `py/tests/test_h_dot_below_nfc.py`; the three real reads were all in
book-of-job's own `.py`, which this phase deletes.

**Ben, 2026-08-21: delete.** The cost is stated where a reader of that repo will meet it,
in its `README.md` and `CLAUDE.md`: book-of-job no longer holds the UXLC snapshot its
published review was built on, the bytes surviving in UXLC-utils and here.

### The deletion is 317 files, and nine directories went whole

268 `.py` + `pyauthor_util/quirks-BHQ.txt` + `check_spelling_in_html.custom-dict.json` +
the 40 UXLC data files = **310**, plus the **7** procedure docs that moved here. Tracked
files **1103 → 786**, tracked `.py` **0**.

holman's phase asks for `git ls-files py | grep -v '\.py$'` before quoting a deletion size.
The equivalent here is per-directory, this repo's code having had no `py/` over it, and it
is what proved every directory could go whole rather than survive as a one-file stub:

| Directory | Tracked | `.py` | Non-`.py` |
|---|---|---|---|
| `pyauthor_qr/` | 160 | 160 | — |
| `pyauthor_util/` | 34 | 33 | `quirks-BHQ.txt` |
| `pyauthor/` | 10 | 10 | — |
| `py/` | 7 | 7 | — |
| `pydiff_mm/` | 5 | 5 | — |
| `py_ac_word_image_helper/` | 6 | 6 | — |
| `py_cam1753_word_image/` | 4 | 4 | — |
| `mb_cmn/` | 17 | 17 | — |
| `py_uxlc_loc/` | 49 | 9 | 39 XML + `lci_recs.json` |

The only tracked non-`.py` inside the code was `quirks-BHQ.txt` and the UXLC data. The
spelling dictionary sat at the repo root beside its module. **There was no `.vscode/`**, so
holman's extra did not recur; what recurred instead is a `book-of-job.code-workspace` and a
`requirements.txt` at the root, both orphaned by the deletion and neither one an obvious
whole-file delete — see "Two root-level files the deletion orphaned" below.

### Nothing moved: the oracle, before and after

Run from `C:\Users\BenDe\GitRepos\MAM-basics` on this repo's interpreter, MAM-basics'
copy of the code, three times — before the deletion, after it, and after all the prose
edits. **Silent, exit 0, every time**, and all **701 tracked artifacts** compared against
their HEAD blobs by `git cat-file --batch` as **700 byte-identical and 1 line-ending-only,
0 content differences**. The one is `out/cam1753-crops.json`, whose checkout is still CRLF
— the same file Phases 0, 1 and 3 each found. **No `fline mismatch` line in any run**, so
the location cross-check still has the 397A and 406A coordinates Phase 0 sent upstream.
`check_all.py` 7 of 7 after the deletion as before it.

### Two figures the plan forecast, and both are off by the same cause

- **Mark order scans 298 files, not 299.** The forecast assumed only the spelling
  dictionary would leave book-of-job's corpus. `check_mark_order._corpus_json_files()`
  yields *every* `.json` under `boj_data_root()`, and
  `py_uxlc_loc/UXLC-misc/lci_recs.json` is one, so Ben's delete decision took it too.
  300 − 2 = 298.
- **The NFC scope holds 35 files, not 42.** The seven procedure docs that moved here are
  the entire difference: the comment's prediction counted `doc/` at nine and it is two
  now. The floor of 30 still clears it, and the comment states the measured figure with
  its accounting. Measured by calling `_scopes()` and `_tracked_files_in_scope()`
  directly rather than by trusting the guard, which only asserts the floor.

**Both are the same lesson in two places: a forecast made before a decision is a forecast
about a different phase.** Neither is a defect, and each was a finding only because the
count was read rather than the verdict — which is the transferable half of Phase 3's
"a lint that loses its inputs goes on printing OK."

### Phase 7 item 1 fired again, and holman's "three per repo" is one too many here

`test_vendoring_policy_paths.py::test_every_pkg_scan_root_exists[book-of-job-mb_cmn-mb_cmn]`
failed in this phase's own verification run, exactly as UXLC-utils' Phase 4 predicted it
would in every remaining plan. The entry is deleted and `py/main_vendoring.py --all`
regenerated `doc/vendoring-inventory.md`: **20 rows over 129 files → 18 over 112**, the 17
being book-of-job's `mb_cmn` copies. The three `out/vendoring_*` artifacts are **55 lines
of pure deletion with no additions**, so no pre-existing drift rode along.

**The suite loses two tests, not three.** That file collected **25** cases before and
**23** after. holman's record predicts three per repo from its own arithmetic — but holman
had **two** `pkg_scan_roots` and book-of-job has one. **The rule is one case per scan root
plus one dest-repo case for the entry**, so the trio's plans should count scan roots rather
than repeat the number three. Suite **947 → 945 passed, 5 skipped, 59 subtests**.

### The `59 subtests` figure DOES reproduce, and Phase 1's reason for saying otherwise was wrong

Phase 0 of this plan corrected holman's Finding 3, which had dropped the figure; Phase 1
re-measured, could not reproduce it, and concluded that "Finding 3 was right on the
substance and Phase 0's correction of it was wrong," setting the standing baseline at
`947 passed, 5 skipped` with **no third figure**. That is wrong. Measured twice this phase
with `.venv/Scripts/python.exe py/main_test.py -q` from the repo root, the summary line
reads **`945 passed, 5 skipped, 59 subtests passed`**.

Phase 1's stated mechanism does not hold either. `pytest-subtests` is indeed absent — `pip
show` reports "Package(s) not found" — but the figure never came from that plugin. **Six
modules under `py/tests/` use `unittest`'s native `self.subTest`**, which pytest counts on
its own: `test_explicit_claims.py`, `test_foi_kq_trivial_types.py`,
`test_verify_table_words_in_mam_plus.py`, `test_versification_and_cantillation_doc.py`,
`test_ws_bot_kq_triv_add_type.py` and `test_ws_bot_kuk_special_callsite_migration.py`.
**The standing baseline is `947 passed, 5 skipped, 59 subtests`** at `f9b6245`, and
`945 passed, 5 skipped, 59 subtests` after this phase.

**Three phases across two plans have now argued this figure back and forth without anyone
naming the mechanism.** The transferable rule is the one that would have ended it at the
first exchange: **when a figure will not reproduce, find what produces it before concluding
it is spurious** — `grep -rl subTest py/tests` is the whole investigation.

### The nine procedure docs split 7–2, and the criterion is not the plan's

The plan says "nearly all of them follow the code to MAM-basics… What stays is whatever
describes the *published site* rather than how it is made." That criterion does not decide
`viewing-image-metadata.md` (reading a PNG's metadata is neither) or `reading-mam-simple.md`
(which describes a vendored data tree). The one used instead, and the one to reuse at the
trio: **a doc moves if following it means touching the code or the pipeline the code
drives; it stays if following it means looking at something the emptied repo holds.**

| Doc | Disposition |
|---|---|
| `aleppo-word-crops.md` | → `doc/boj-aleppo-word-crops.md` |
| `cam1753-word-crops.md` | → `doc/boj-cam1753-word-crops.md` |
| `leningrad-word-crops.md` | → `doc/boj-leningrad-word-crops.md` |
| `leningrad-image-scaling.md` | → `doc/boj-leningrad-image-scaling.md` |
| `image-crop-reproducibility.md` | → `doc/boj-image-crop-reproducibility.md` |
| `viewing-image-metadata.md` | → `doc/boj-viewing-image-metadata.md` |
| `quirkrec-comments.md` | → `doc/boj-quirkrec-comments.md` — Decision D names this one explicitly |
| `opening-html-files.md` | **stays** — it opens `gh-pages/`, which stayed |
| `reading-mam-simple.md` | **stays** — it describes `py_ac_loc/MAM-XML/`, which stayed |

The `boj-` prefix matches the `author_boj_*` / `boj_render` marker Ben settled in Phase 3;
MAM-basics' `doc/` is flat, so a prefix rather than a subdirectory. `CLAUDE.md` here gains
a short section for the seven, since nothing in the code points at them.

**Every path in the seven was repointed and then checked to exist** — all 17 real paths
resolve, the only unresolved two being the `qr_XXXX.py` placeholders. That check is worth
running rather than trusting the substitution list, because it caught a double `py/py/`
prefix in two files. Four things a path rewrite alone would not have caught:

- **Two of the seven told a reader to verify a regeneration with `git status --porcelain`**
  on book-of-job's `gh-pages/`. That is the instrument this plan spends a Phase 0
  subsection warning against, and once the file moved it was also **unrunnable**, `git
  status` refusing a path outside the repo it runs in. Both now use
  `git -C ../book-of-job diff --stat HEAD`, with the reason inline so it is not reverted
  as a stylistic preference.
- **The apply-script template's root walk broke.** `boj-aleppo-word-crops.md` carried a
  `.novc/` throwaway template computing `ROOT = Path(__file__).resolve().parent.parent`
  and importing `py_ac_word_image_helper` from it. The script now lives in **this** repo's
  `.novc/`, reaches `py/` from there, and takes its destination from
  `boj_paths.aleppo_img_dir()`. The `sys.path` insert is kept and labelled — a gitignored
  throwaway is the one place the ban does not apply.
- **`cam1753-word-crops.md` calls the manuscript μC.** The generated site and the code both
  call it **μY**, 3 and 5 times respectively, and μC appears nowhere else in either repo.
  Corrected. **A doc that has not been read in two years disagrees with the artifacts
  about more than paths.**
- **That same file spells its commands with backslashes**, so a forward-slash substitution
  pass missed all eleven. **Substitute on both separators, or check afterwards.**

`reading-mam-simple.md` stayed but needed one edit: "the two files that name the directory"
is one now, and it names `../MAM-basics/py/tests/test_h_dot_below_nfc.py`; the other was a
gitignored throwaway rather than a tracked file.

### The 518 artifacts, named where a reader of that repo will meet them

Phase 0's table was re-measured before being copied, and every figure matched: 515 PNG,
175 HTML, 2 CSS, 2 woff2 under `gh-pages/`, 7 JSON under `out/`; 160 each under
`jobn/img/Aleppo/`, `jobn/img/Lenin/` and `jobn/img/cam1753/`, 30 under `jobn/img-orphans/`
and 5 loose in `jobn/img/`. The five loose ones are named individually in book-of-job's
`CLAUDE.md`, since a five-file residue is exactly what a sweep rounds off.

They go in that repo's `CLAUDE.md` as a table, as UXLC-utils' Phase 4 put its 87 in that
repo's `CLAUDE.md` and holman's its 160. **The README says it too**, in one sentence with
the number in it, because the README is what a reader meets first.

### `CLAUDE.md` edited, README replaced

Phase 1 corrected this section's "write a `CLAUDE.md` here": the file exists (`991a1c4`,
2026-08-03) and this was an edit. What survived from the old text is the quirkrec reading
advice — read `out/enriched-quirkrecs.json`, edit the Python, name the loop variable `eqr`
— repointed at `py/author_boj_qr/` here. What is new is the no-Python-here statement, the
five-entry-point table, the 518-artifact table, the lints-run-from-MAM-basics section, and
the instruction to read a regeneration with `git diff` rather than `git status --porcelain`.

The README was two lines and is replaced outright. It now says what the review argues, what
the 160 detail pages are, and that each has word-level crops from all three of μA, μL and
μY — **verified rather than asserted**: the three crop sets are each exactly 1:1 with the
160 detail-page filenames, checked by `diff` over the sorted SID lists.

### `mb_cmn/provenance.py`'s `parents[2]` is moot for book-of-job now

Phases 1 and 3 both put this to Ben and neither picked. **This phase's deletion of
book-of-job's `mb_cmn/` has ended it there**: the wrong copy no longer exists, so the
question is now only whether MAM-basics' copy should walk to `.git` and be re-vendored for
the *other* repos that hold it. It was not decided silently, and it is not this phase's to
decide. `git grep -lI "generated by book-of-job" -- gh-pages out` still returns 0, so
Phase 6's blast radius in that repo remains nil.

### Two root-level files the deletion orphaned — **Ben, 2026-08-21: delete both**

Neither is a `.py` and neither came here with the code, so neither is in this section's
prescription — and both are now about Python that does not exist:

- **`book-of-job.code-workspace`.** Five of its six launch configurations name deleted
  scripts, its settings block is `python.analysis` severity overrides plus terminal
  auto-approve rules for a `.venv` Phase 7 item 5 deletes. This is holman's
  `.vscode/settings.json` case, which Ben approved deleting. What is *not* about Python is
  its folder list, which opens book-of-job beside `codex-index-aleppo` and
  `codex-index-cam1753` — a view that survives either way, MAM-basics'
  `all-repos.code-workspace` listing all four folders.
- **`requirements.txt`.** Five packages — black, matplotlib, numpy, Pillow, pyspellchecker
  — for code that is gone, hydrating a `.venv` Phase 7 item 5 deletes. Phase 3 also found
  `matplotlib` is imported by nothing in that repo. Neither UXLC-utils nor
  holman-ketiv-qere has a `requirements.txt`, so there is no precedent either way.

**Ben chose to delete both, 2026-08-21**, in a second commit each side — `aa20c61` there
and the commit carrying this record here. Nothing in either repo's code referenced them,
checked by `git grep` first; MAM-basics' `all-repos.code-workspace` still lists book-of-job among
its folders, which is where the three-repo view survives and which Phase 7 item 3 leaves
alone. book-of-job's tracked files are **784** and its root holds four files: `.gitattributes`,
`.gitignore`, `CLAUDE.md`, `README.md`. The NFC scope went **35 → 33**, exactly the
prediction, still clear of the floor of 30.

**At the trio, sweep the repo root for files whose subject is the interpreter rather than
the code** — a workspace file, a `requirements.txt`, a `.vscode/`, an `.editorconfig` —
before quoting a deletion size, the way holman's phase says to sweep for non-`.py` under
`py/`. **The workspace file is the one to look at rather than assume**: this one was
mostly launch configurations and `python.analysis` settings, but it also declared the
three-folder view opening book-of-job beside `codex-index-aleppo` and `codex-index-cam1753`,
which is not about Python at all and is why it was a question rather than a step.

---

The rest of this section is the plan as written 2026-08-02, before the phase ran.


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

## Phase 6 — breadcrumbs and issue citations — **DONE 2026-08-22**

**Landed as `8293ce8` here — `CLAUDE.md`, this record and the two Status rows — and nothing at all
in book-of-job.** Both halves of the prescription below were
nil when Phase 4 measured them on 2026-08-21, and re-measuring on 2026-08-22 confirmed both: no
breadcrumb to flip, no citation to prefix. **This is the first of the programme's three Phase 6
runs to owe its data repo no commit at all** — UXLC-utils' moved one artifact
(`gh-pages/fois/index.html`) and holman-ketiv-qere's moved three. What this phase did owe is a
`CLAUDE.md` section, which neither this plan nor the programme plan wrote down: book-of-job has an
issue tracker of its own, so **"Four issue trackers" is now "Five issue trackers"**.

**Every baseline was re-measured first and every one matched.** book-of-job at `aa20c61`, clean,
**784 tracked files, 0 tracked `.py`, 701 tracked artifacts**; MAM-basics at `e6447e2`, clean;
UXLC-utils at `4d1ad89`, clean. Suite **945 passed, 5 skipped, 59 subtests**; the oracle silent
with **700 byte-identical, 1 line-ending-only (`out/cam1753-crops.json`), 0 content differences**;
`check_all.py` 7 of 7, mark order over 298 files, escapes over 241 `.py`. **Phases 4 and 6 have
now both found every inherited figure right**, for the reason holman-ketiv-qere's Phase 6 record
gives: the phase before measured them and nothing ran in between.

### Part 1 — nothing to flip, and three checks rather than one say so

Both greps this section prescribes return **0**, run from
`C:\Users\BenDe\GitRepos\book-of-job`: `git grep -lI "generated by book-of-job" -- gh-pages out`,
and the bare `git grep -lI "book-of-job" -- gh-pages out` besides. **The structural reason is the
one UXLC-utils' Phase 1 found in that repo**: no code here ever passed `generator_file` to
`mb_cmn.file_io`, so no artifact carries an `mb_cmn.provenance` breadcrumb to be wrong. That is
also why `mb_cmn/provenance.py`'s wrong `parents[2]` was latent here rather than damaging.

**But a zero from the prescribed grep is not the whole answer, and holman-ketiv-qere's Phase 6 is
the reason to say so** — there the breadcrumb grep matched nothing while five stale `py/…` paths
sat in the data and the prose. Both of that phase's wider sweeps were run here, plus the
interpreter sweep the programme's Phase 7 finding 1 added:

- **`git grep -nIoE '(^|[^-a-zA-Z0-9/])py/[A-Za-z_./]*' -- .` returns 17 hits in 2 files** —
  16 in `CLAUDE.md`, 1 in `README.md` — **and every one of the 17 is correct, not stale.** Phase 4
  rewrote both files with the working directory declared once at the top — search that `CLAUDE.md`
  for "Everything below runs from", line 18 as of 2026-08-22 — so a bare `py/main_…` underneath
  it resolves correctly. **That is a third breadcrumb shape**, alongside the two holman-ketiv-qere's
  Phase 6 recorded: not a bare `MAM-basics/py/…` and not a `../MAM-basics/py/…`, but a bare `py/…`
  licensed by a stated root. The lesson holman's phase drew — ask which neighbourhood a path sits
  in rather than picking one shape per repo — holds, with the neighbourhood here being a whole
  document rather than a sentence.
- **`git grep -nI "\.venv" -- .` returns 4 hits and not one names book-of-job's own venv.**
  `.gitignore:2` is the ignore rule; `CLAUDE.md:19` says outright that there is no `.venv` here to
  run anything with; the other two are `.venv/Scripts/python.exe py/…` command lines under the
  same declared MAM-basics root. A search for an absolute path to this repo's interpreter
  (`GitRepos.book-of-job.*venv` and both separator spellings) returns nothing. **So the trap that
  bit holman-ketiv-qere's Phase 7 item 4 does not recur**: that repo's `doc/` named its own venv
  by absolute path, an instruction pointing at the directory Phase 7 was about to delete. Phase 7
  item 5 can delete book-of-job's `.venv` — **153 MB on disk, the largest of the four**, against
  UXLC-utils' 33 MB and holman-ketiv-qere's 22 MB — with no documentation edit owed.

### Part 2 — nothing to prefix, and the citation count did not track the file count

**29 `#`-plus-digit sites across the 268 `.py` book-of-job tracked before the move, and every one
is disposed of without a prefix.** Measured at `45f8853`, that repo's HEAD before Phase 4's
deletion, so the count covers the code that moved *and* the code that was deleted:

| Where | Sites | Disposition |
|---|---|---|
| `main_gen_aleppo_crop_editor.py` | 12 lines | CSS hex colours — moved, stay bare |
| `main_gen_cam1753_crop_editor.py` | 12 lines | CSS hex colours — moved, stay bare |
| `mb_cmn/hebrew_accents.py` | 4 lines | Yeivin *ITM* `#194`, `#358`, `#361` — deleted with `mb_cmn/` |
| `pyauthor_util/qr_relations.py:75` | 1 | already written out in full as `bdenckla/wlc-utils#43` |

The 24 CSS lines carry **46 hex-colour tokens** between them; the table counts lines, because that
is what a `git grep -n` sweep hands a reader. Restricted to the **241 modules Phase 3 moved**, the
count is **25** — the 24 CSS lines plus `py/author_boj_util/qr_relations.py:75` — which is
**holman-ketiv-qere's result almost exactly**, that repo's 60 moved files having yielded 19 CSS
colours plus one UXLC change anchor.

**book-of-job owes even less than holman-ketiv-qere did, in two places.** Its `mb_cmn/` copy held
**no `paths.py`** — Phase 1 established that this repo deliberately does not vendor it — so the
`#75` naming MAM-basics' paths convention and the already-prefixed `wlc-utils#48` that
holman-ketiv-qere's deletion disposed of have no counterpart here. And its root-level
`test_h_dot_below_nfc.py` cites nothing at all, where holman-ketiv-qere's carried a `#187` naming
MAM-basics' NFC convention. **Neither absence is luck**: both are consequences of decisions this
plan's Phase 1 recorded.

**The second trap the `CLAUDE.md` section names does not recur here, and that was checked rather
than assumed.** Grepping the 241 moved modules for `REPO_OWNER`, `REPO_NAME`, `gh issue` and
`github` finds no issue-rendering machinery: the `github` hits are `bdenckla.github.io` published
URLs, three "Initially generated by GitHub Copilot" provenance comments, and
`py/boj_paths.py:127`'s `DATA_REPO_NAME = "book-of-job"`, which names a sibling repo to build
paths from exactly as `py/hkq_paths.py:43` does and has nothing to do with `gh`.
`py/py_render/rt_issue_tags.py` and `py/hkq_cmn/table_row_github_issues.py` were left untouched,
their `REPO_OWNER`/`REPO_NAME` constants included.

**So the transferable rule from holman-ketiv-qere's Phase 6 now has its second confirming case,
at four times the size**: 241 modules moved and owed one clause, where 60 modules owed one clause.
**How many citations a move owes is a function of what its code talks about, never of how many
files it is.** book-of-job's Python is a review of one biblical book and its manuscript images; it
had no reason to cite a tracker, and it did not.

### What Phase 6 actually owed: `CLAUDE.md`'s section becomes five

**book-of-job keeps 61 issues, numbered 1–61 with no gaps, 19 of them open**, measured 2026-08-22
with `gh issue list --repo bdenckla/book-of-job --state all`. They were not transferred when that
repo's Python moved here on 2026-08-19, exactly as wlc-utils', UXLC-utils' and holman-ketiv-qere's
were not. So a citation of one is written **`book-of-job#NN`**.

**All four of the other trackers were re-measured too, and all four matched what the section
already claimed**: wlc-utils 93 (1–93, 21 open), UXLC-utils 56 (1–56, 27 open),
holman-ketiv-qere 81 (1–81, 60 open). MAM-basics itself holds 230 issues numbered 1–231, the one
gap being #129. **The re-measure was worth running rather than trusting**: this section's own
wlc-utils count stood five short for weeks before anyone checked it.

Eight edits landed in `CLAUDE.md`. Items 3, 4 and 7 below are **corrections** — claims a fifth
tracker falsifies — rather than extensions of the section:

1. The heading, "Four issue trackers" → **"Five issue trackers"**.
2. A book-of-job paragraph after holman-ketiv-qere's, with the counts, two fresh low-number
   collisions (book-of-job#1 studies UXLC changes in Job where MAM-basics #1 syllabifies pointed
   Hebrew; book-of-job#7 shows only the first five of each group where MAM-basics #7 adds
   `main_diff_mpp.py`), and the shape of the tracker.
3. **The collision arithmetic.** Four of the six numbers the section called four-way collisions
   are now **five-way** — #19, #29, #48 and #52, whose book-of-job titles are "Add Aleppo Codex
   image for 34:5", "supplement μA images with manuscript locations", "details is getting too big"
   and "30:18: add prefix; expand Lenin crop". **#69 and #75 stay four-way**, book-of-job's
   numbering stopping at 61. holman-ketiv-qere's sentence was moved to the past tense ("became
   four-way collisions when holman-ketiv-qere's tracker was added") so that the promotion of four
   of them reads as a sequence rather than a contradiction.
4. **"Unlike the other three moves, this one had nothing to prefix"** was a uniqueness claim that
   book-of-job falsifies, and it opened with a bare "this one" besides. It now reads "Unlike the
   two moves that had citations to prefix — wlc-utils' 326 and UXLC-utils' 50 —
   holman-ketiv-qere's move had nothing to prefix", which names both sides and stays true.
5. A book-of-job nothing-to-prefix paragraph carrying the 29-site inventory above.
6. The history sentence, which had recorded two of the section's names. It now records all four
   — "Two issue trackers" until 2026-08-18, "Three issue trackers" for part of that same day,
   "Four issue trackers" from later that day until 2026-08-22, "Five issue trackers" since — and
   counts the **ten** sentences across four plans that still cite it under a retired name, listed
   by plan and by which name each uses. Counted 2026-08-22 with `git grep -cI "<name>" -- doc`.
   All ten are left as written, being execution records of the section as it stood.
7. The `doc/`-exception paragraphs. holman-ketiv-qere's "the one place it differs from the other
   three" became "the first of the four evacuated repos to need none", a book-of-job paragraph
   follows it stating that those four now split two and two, and the wlc-utils paragraph's "the
   one standing exception" became "one of the two standing exceptions" — a claim the UXLC-utils
   paragraph right below it had already contradicted.
8. The "Not every `#NN` is an issue" bullet's bare "CSS carries hex colours" now names the two
   crop-editor generators and the 46 colours they hold between them, so that the largest single
   block of non-issue `#NN` in this repo is findable from the bullet that warns about it.

**book-of-job needs no `doc/` exception, and it goes further than holman-ketiv-qere does.**
`git grep -nIE '#[0-9]+'` over its **whole tracked tree** returns nothing at all, measured
2026-08-22 — not in `CLAUDE.md`, `README.md`, the two `doc/` files or the three `.md` under
`py_ac_loc/`, and not in any of the 701 artifacts under `gh-pages/` and `out/` either. **All 784
tracked files are free of `#NN` in every shape**, issue numbers and hex colours alike. **So the
four evacuated repos split two and two**: wlc-utils' `doc/` and `in/` copies now living here and
UXLC-utils' own live `doc/` are the two standing exceptions, and holman-ketiv-qere and book-of-job
need none. Stating this
is worth the sentence because the arithmetic that predicts otherwise is easy to do — the emptied
repo is the one whose tracker was just added.

### Verification — confirmation rather than verification, and run anyway

Phase 6 touched no code, so nothing it did could move any of these; running them establishes that
nothing else did either.

- **The oracle**, `py/main_gen_misc_authored_english_documents.py` from
  `C:\Users\BenDe\GitRepos\MAM-basics` on this repo's interpreter: **silent, exit 0**, and no
  `fline mismatch` line, so the location cross-check still holds the 397A and 406A coordinates
  Phase 0 sent upstream.
- **All 701 artifacts compared against their HEAD blobs** by `git cat-file --batch`, before the
  oracle run and after it, with the same verdict both times: **700 byte-identical, 1
  line-ending-only, 0 genuinely different.** The one is `out/cam1753-crops.json`, whose checkout
  is still CRLF — the same file Phases 0, 1, 3 and 4 each found. `git status --porcelain` was not
  used in book-of-job, per this plan's Phase 0 subsection.
- **Suite 945 passed, 5 skipped, 59 subtests**, unchanged, via
  `.venv/Scripts/python.exe py/main_test.py -q` from the repo root.
- **`check_all.py` 7 of 7**, mark order over 298 files, escapes over 241 `.py`.
- **`git status --porcelain` empty in book-of-job and in UXLC-utils** at the end; in MAM-basics it
  held only this phase's own three prose files.
- The NFC guard was re-run on its own after the `CLAUDE.md` edit, **6 passed** — that file being
  in its scope.

### The open question is still open, and this phase did not touch it

`mb_cmn/provenance.py`'s `_repo_root()` is `parents[2]`. Phase 4's deletion of book-of-job's
`mb_cmn/` ended the question **for book-of-job**, and Part 1 above records why it was latent even
before that: nothing here passed `generator_file`, so no breadcrumb was ever written. **What
remains open is only whether MAM-basics' copy should walk to `.git` and be re-vendored for the
other repos that still hold it** — the two codex-index repos and diffable-pointed-hebrew. Phases
1, 3 and 4 each put it to Ben and none picked; this phase did not pick either.

---

The rest of this section is the plan as written 2026-08-02, before the phase ran.


```powershell
git grep -lI "generated by book-of-job" -- gh-pages out
```

Flip in a dedicated commit near the end; do not fix the now-wrong path mid-move.

## Phase 7 — cross-repo bookkeeping — **DONE 2026-08-22 (items 2–6; item 1 landed inside Phase 4)**

**Items 2, 3, 4 and 6 were run rather than assumed. Item 5 deleted a 153 MB venv holding 1,722
untracked `.py` files, after `--clean-worktrees` found nothing to clean.** Nothing here needed a
commit in book-of-job: every item was a confirmation, a grep, or the deletion of an untracked
directory. **That makes two of the four Phase 7 runs that owed their data repo no commit** —
UXLC-utils' owed none either, and holman-ketiv-qere's owed a one-liner. **This phase completes the
plan**, book-of-job being the fourth of the programme's five steps.

**Every baseline was re-measured first and every one matched**, for the reason Phases 4 and 6
already gave: the phase before measured them and nothing ran in between. MAM-basics at `151dbf8`,
clean, nothing unpushed; book-of-job at `aa20c61`, clean, **784 tracked files, 0 tracked `.py`,
701 tracked artifacts** (694 `gh-pages`, of which 531 `jobn` and 160 `jobn-details`, plus 7 `out`
JSON); UXLC-utils at `4d1ad89`, clean. Suite **945 passed, 5 skipped, 59 subtests**; the oracle
silent; `check_all.py` 7 of 7, mark order over 298 files, escapes over 241 `.py`.

**Item 1 — confirmed, not redone.** `git grep -cI "book-of-job" -- in/vendoring_policy.json
doc/vendoring-inventory.md` returns nothing, as Phase 4 left it on 2026-08-21.

### Item 2 — the string survives, and the plan's attribution of it was the stale part

The prescription below says "UXLC-utils names this repo in its own code" and cites
`py/main_map_changes_to_book_of_job.py:165`. **That module has not been UXLC-utils' since
2026-08-03**, when that repo's Python was evacuated; the live site is
`C:\Users\BenDe\GitRepos\MAM-basics\py\main_map_changes_to_book_of_job.py:165`, where the line
number happens not to have drifted. It is the only `book-of-job/gh-pages` string under `py/`.

**The reading was confirmed rather than assumed, and it holds for a sharper reason than "it is a
URL".** The string is never used to open anything: `write_mapping()` puts
`"html_base": "../book-of-job/gh-pages/jobn-details/"` into the output dict as a **label**,
beside the matched entries' bare `html` filenames, so that a reader of the JSON can compose the
link. The module reaches book-of-job's real files by a different route entirely —
`BOOK_OF_JOB_REPO = uxlc_paths.book_of_job_dir()` at line 38, guarded by
`uxlc_paths.require_book_of_job_dir()` at line 399, which is `paths.require_sibling`, so a
missing clone fails naming its overrides instead of composing a path into nothing. That is the
arrangement UXLC-utils' own Phase 7 item 5 recorded, still standing.

**And the label reaches a tracked artifact in a third repo**, which is what makes it worth a
check rather than a shrug: `UXLC-utils/in/UXLC-misc/2026.04.01-map-to-book-of-job.json:3` carries
the same string verbatim, the generator living here and writing there. **What keeps it correct is
that `gh-pages/jobn-details/` is still 160 tracked files in book-of-job** — the reason the
prescription gives for not reorganizing `gh-pages/` in the same programme, which no phase has.

### Item 3 — confirmed, and the string came back verbatim for the third repo running

`all-repos.code-workspace:7` reads `"path": "../book-of-job"`, one of the 20 folders that file
lists, and it stays: that repo still tracks 784 non-Python files.
`in/repo_maintenance_policy.json`'s `frozen_repos` names six repos — CCAR-Psalms, MAM-for-Acc,
MAM-for-CCAR, MAM-for-JPS, mamgo-auto-edits and TMC — and book-of-job is not among them and does
not need to be, that register being for paused client projects whose last-changed dates are the
point. Both UXLC-utils' and holman-ketiv-qere's Phase 7 records predicted their equivalents would
come back verbatim and both did; this is the third.

### Item 4 — the zero-`.py` case was decided in advance, by a fix made for exactly this shape

**`run_black.py` cannot reach the "tracked `.py` but no black" failure from a repo tracking
none.** `_has_tracked_py_files` is consulted **before** black is even looked for: with
`has_tracked_py` False the sweep sets `command = None` and the note
`Skipped: no tracked .py files in this repo`, and the `problem` branch that names a missing black
is reachable only when the repo does track Python. **That ordering is itself the record of this
exact situation.** Its docstring says the sweep asked the question only *after* failing to find a
black to run until 2026-08-02, so "a Python-less repo that still had a `.venv` lying around got
the full `black .` treatment over whatever untracked Python happened to be on disk" — and names
wlc-utils, emptied of Python on 2026-08-01, whose leftover venv and three orphaned worktrees held
the 789 `.py` the sweep then reformatted, tracked in no index anywhere.

**book-of-job was that shape at more than double the size, and running the sweep before deleting
the venv is what turns the docstring's claim into a measurement.** Its `.venv` held **1,722
untracked `.py`**, against wlc-utils' 789 and UXLC-utils' 832. The sweep skipped every one of
them. Both runs were scoped with `--repos`, since dropping it reformats every repo in the
workspace, and both used `--workspace-file all-repos.code-workspace`, the default file listing
only the repos this one generates into:

- `--run-black` reports `REPO=book-of-job; BLACK_ATTEMPTED=False; BLACK_OK=False; Skipped: no
  tracked .py files in this repo`, the same string UXLC-utils and holman-ketiv-qere returned.
- `--check-repo-standards` degrades just as gracefully: `MAINTENANCE_SCRIPT=n/a;
  WORKTREE_STEP=n/a; PATH_UTILITY=n/a`, with `LINKED_WORKTREES=0`, `AGENT_BRANCHES=0`,
  `SYS_PATH_MUTATIONS=0`, `SYS_PATH_IN_TESTS=0`, `HEX_ESCAPES=0`, `ORPHAN_MARKS=0`,
  `NFC_H_DOT=0`, `NFC_LATIN=0` and `GITATTRIBUTES_LF=True`. Its own docstring states the
  gate — a repo with no tracked `.py` is not measured on the Python standards, because
  `maintenance_script`, `path_utility` and the `script_covers` half of `worktree_hygiene` each
  ask for a Python file — and names wlc-utils as the case that made the gate necessary. The two
  worktree **counts** are deliberately not gated, since such a repo goes on accruing worktrees
  from agents editing its data.

### Item 5 — 153 MB deleted, no worktrees, and one documentation sentence made true

Done in the order this plan requires:

- **`--clean-worktrees` ran first**, before anything else touched a worktree, and reported
  `worktrees: nothing to clean` for all 20 repos in the workspace, book-of-job among them —
  agreeing with the `git worktree list` baseline, which shows only the main checkout, and with
  the absence of any `.claude/worktrees` directory. Hand-running `git status` inside a worktree
  refreshes the index mtime that `repo_util/git_worktree_cleanup.py` reads as recent activity,
  and the sweep then spares that worktree, so the sweep goes before the poking.
- **Then the checks the deletion was conditional on**, all three re-verified rather than taken
  from Phase 6. `git grep -nI "\.venv" -- .` returns 4 hits and not one names book-of-job's own
  venv: `.gitignore:2` is the ignore rule, and `CLAUDE.md:19`, `:27` and `:94` are covered below.
  A search for an absolute path to this repo's interpreter
  (`GitRepos[\\/]book-of-job[\\/.]*venv`, both separator spellings) returns nothing, which is the
  interpreter sweep the programme's Phase 7 finding 1 added. Zero tracked files under `.venv`,
  which is self-ignoring via the `.venv/.gitignore` that `python -m venv` writes.
- **And the junction check, which a sibling rule makes mandatory**, because a junction here would
  have taken MAM-basics' venv with it: `Get-Item -Force` reported `Attributes: Directory`, no
  `ReparsePoint`, empty `LinkType` and empty `Target`, and book-of-job's own `pyvenv.cfg` naming
  `C:\Users\BenDe\GitRepos\book-of-job\.venv` as what `python -m venv` was pointed at, distinct
  from MAM-basics' `pyvenv.cfg` naming its own. A real directory, so `Remove-Item -Recurse
  -Force` was safe. Afterwards `C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe` was
  confirmed present **and confirmed to run**, reporting 3.13.14, and the oracle was re-run clean.

book-of-job's root now holds four directories and four files with no `.venv` among them, and the
repo is unchanged at 784 tracked files.

**The `CLAUDE.md` sentence here needed no edit for the opposite reason from the other two repos',
and that difference is worth stating.** holman-ketiv-qere's and UXLC-utils' each say some version
of "whatever `.venv` is left here has nothing to run" — descriptive of a venv their Phase 7
removed, and each left as written, the two repos being consistent as they stand. book-of-job's
`CLAUDE.md:19` says something else: **"Nothing runs from here, and there is no `.venv` here to run
it with."** That was an assertion about the disk, and it was **false** while a 153 MB venv sat
there; this phase makes it true. Phase 4 wrote it ahead of the deletion. The other two `.venv`
mentions, `CLAUDE.md:27` and `:94`, are the `.venv/Scripts/python.exe py/…` command lines that
line 18's "Everything below runs from **MAM-basics' repo root**" licenses — Phase 6's third
breadcrumb shape, and correct as they stand.

**So the trap that bit holman-ketiv-qere's Phase 7 did not recur, and re-verifying cost little.**
There, `doc/holman-manuscript-citations.md` named that repo's own venv by absolute path — an
actionable instruction pointing at the directory the phase was about to delete — and needed a
commit. Here nothing did.

### Item 6 — five stale citations, and the grep shape the earlier plans prescribe would have found one

The grep ran over **26 clones**: the 20 under `C:\Users\BenDe\GitRepos` and the 6 under
`C:\Users\BenDe\FrozenRepos`, which the workspace file no longer reaches.

**The prescribed shape does not transfer to this repo, and the reason is structural rather than
bad luck.** UXLC-utils' Phase 7 grepped `UXLC-utils/py` and holman-ketiv-qere's grepped
`holman-ketiv-qere/py`, which sufficed because all the Python of each sat under one `py/`.
**book-of-job's sat at the repo root** — `pyauthor_qr/`, `pyauthor_util/`, `pyauthor/`,
`mb_cmn/`, `py_uxlc_loc/`, `pydiff_mm/` and sixteen root-level modules — so `book-of-job/py`
matches almost none of what moved. Worse, **three of the five stale citations carry no path at
all**: they name a bare module filename and leave the repo to the surrounding prose ("book-of-job
`author.py`", "The sibling repo `book-of-job` has a `check_all.py` harness"). No path-shaped grep
can see those in any repo. **Grep for the repo's NAME and classify the hits by hand**, which is
what was done here and what the codex-index trio should do.

**Three stale citations in MAM-private, reported and not fixed.** That repo is neither of this
plan's two, so the precedent set by UXLC-utils' item 6 and followed by holman-ketiv-qere's finding
2 applies: a commit to a third repo stops and asks. MAM-private was not written to.

1. **`mgketer/documentation/periodic-maintenance.md`, lines 137–152** — a section headed
   "## 7. Checks ported from book-of-job (TBD)", opening "The sibling repo `book-of-job` has a
   `check_all.py` harness running several checks that may be worth porting or adapting for this
   repo", with a five-row table naming `check_escape_sequences.py`, `check_mark_order.py`,
   `check_function_ordering.py`, `check_html_syntax_and_sanity.py` and `check_spelling_in_html.py`
   with a port priority each, and a closing line telling the reader to start with the first.
   **All six are this repo's now** — `py/check_all.py` and the five `py/check_*.py` — and
   book-of-job holds none of them. This is **holman-ketiv-qere's finding 2 recurring in the same
   shape at the same repo**: a pointer written to be followed, under a heading about propagating
   work, in a place no tooling of the evacuated repo can see.
2. **`masorah-books/doc/migration-checklist.md:152`** — `../book-of-job/pyauthor_qr/qr_1413.py`,
   listed under "**Do not touch (7).**" among files carrying a published link into
   `MAM-with-doc`'s Breuer FOI page. The live path is
   `MAM-basics/py/author_boj_qr/qr_1413.py`. **The item's point survives and only its path is
   wrong** — the link must still not be renamed — and its two neighbours in that list,
   `../book-of-job/gh-pages/jobn-details/1413.html` and `../book-of-job/out/enriched-quirkrecs.json`,
   are both still correct, those trees having stayed.
3. **`mgketer/py/py_ac_word_image_helper/alef_bet_to_ascii.py:6`** — "Same scheme as mgketer
   ``hebrew_word_id.py`` and book-of-job ``author.py``". The live target is
   `MAM-basics/py/author_boj_util/author.py`.

**One stale citation in two public repos, and it is a single blob, so it is handed to the trio
plan rather than fixed here.** `py/py_ac_word_image_helper/alef_bet_to_ascii.py:5` **in this
repo** and `codex-index-aleppo/py/py_ac_word_image_helper/alef_bet_to_ascii.py:5` carry that same
sentence, and the two files are **byte-identical** (md5 `5a25fbe8734f08553d0bc1c31521904c`) — the
family the programme's Phase 0 reconciled. **Editing this repo's copy alone would fork what that
phase spent a step unifying**, so this plan's own "both repos at once or not at all" applies, and
the moment both public copies come under one hand is the trio plan, codex-index-aleppo's Python
moving here. mgketer's third copy is **already diverged** (md5 `c7d2c780664875449d98a55c2c567fbc`:
a "Initially generated by GitHub Copilot" line, `\uXXXX` escapes where the reconciled pair carries
literal Hebrew, and two double-spaces after a period), so it is no part of that blob and needs its
own edit whatever happens to the other two. **This repo's copy has the sharper edge of the
three**: it says "book-of-job `author.py`" while sitting in the repo that now holds `author.py`,
so it attributes a file to a sibling that has it not.

**One stale citation in UXLC-utils, reported and not fixed, that repo being a third one too.**
`doc/clc-design.md:824` describes book-of-job as "(sibling repo; self-contained, with its own
`gh-pages` + many check scripts)", proposing it as a harvesting target for CLC notes. The
`gh-pages` half holds; "many check scripts" and "self-contained" do not. It sits in UXLC-utils'
own live `doc/`, which `CLAUDE.md`'s issue-tracker section names as one of the two standing
exceptions.

**Checked and correct, listed so nobody re-derives them:**

- `codex-index-aleppo/py/check_word_finding.py:5–6` and `py/check_all.py:6,44` name "book-of-job
  quirkrecs" and "the book-of-job repo's enriched-quirkrecs.json". **Data, and still there**:
  `out/enriched-quirkrecs.json` is one of book-of-job's seven tracked `out/` JSON.
  `check_word_finding.py:18`'s `TEST_DATA = ROOT / "test-data-from-book-of-job.json"` is a local
  file of codex-index-aleppo's named after the repo, not a path into it.
  `codex-index-cam1753`'s root-level `check_all.py` and `check_word_finding.py` carry the same
  four mentions and are correct for the same reason.
- `codex-index-aleppo.code-workspace:7` and `codex-index-cam1753.code-workspace:7` are
  `"path": "../book-of-job"`, the same folder entry item 3 confirms here.
- `MAM-simple-provenance.md:8` in both codex-index repos names the git tag
  `2026-02-14-book-of-job-py-ac-loc`. A tag name, and `py_ac_loc/` is data despite its prefix.
- `document-index/README.md:18`, the seven `quirkrec-link` anchors in
  `mgketer/out-reports/by-book/D3-Job/suppressed.html` and the seven `quirkrec_url` values in
  `mgketer/py/python_modules/diff_crops.py` are published `bdenckla.github.io/book-of-job/…`
  URLs. The site is intact, so all fifteen resolve.
- `UXLC-utils/CLAUDE.md:39–41` names `main_map_changes_to_book_of_job.py` and says it reads the
  sibling's `out/enriched-quirkrecs.json` and `gh-pages/jobn-details/`. Both data paths hold, and
  the module being this repo's is licensed by that file's own opening section, which declares the
  working root — the third breadcrumb shape again, in the repo Phase 6 did not check it in.
- In this repo, two mentions were examined and **deliberately left**, both being records of the
  past rather than pointers to follow. `py/vendoring/compare.py:21` names book-of-job as holding
  the latent-CRLF condition, but dates the claim to the first three-verdict run on 2026-08-04,
  when that repo did hold vendored copies. `py/repo_util/check_repo_standards.py:197` and `:565`
  say the file-scan checks match "book-of-job's `check_escape_sequences.py`" and that
  `_raw_string_spans` is "Adapted from" it — an attribution of origin, which a move does not
  falsify. The 12 `book-of-job/.novc` paths across `doc/boj-aleppo-word-crops.md`,
  `doc/boj-cam1753-word-crops.md` and `doc/boj-leningrad-word-crops.md` are scratch-directory
  paths in that repo and are correct as Phase 4 repointed them.

**github-misc and the skills are nil here, and the reason differs from UXLC-utils'.** That plan's
item 6 needed a one-line edit (github-misc `549224e`) because `references/terminology.md` cited
"UXLC-utils `clc_dual_cant._accent_name`" by repo. book-of-job is mentioned **once** in each copy
of the skill tree and it is the same line in both: `hebrew-prose/SKILL.md`'s `description:`
frontmatter listing book-of-job among the repos the skill governs. **That is still correct** —
book-of-job holds 694 files of rendered `gh-pages/` prose — and it is the mention UXLC-utils'
Phase 7 also left, for that same reason. Grepping both copies for `quirkrec`, `pyauthor`,
`check_all` and `jobn` returns nothing, so no module of book-of-job's was ever cited there.
**Both copies were checked**, the live `C:\Users\BenDe\.claude\skills\` and the tracked
`github-misc/dot-claude/skills/`, since neither syncs to the other. Nothing owed, and no commit
to github-misc.

### Verification

- **The oracle**, `py/main_gen_misc_authored_english_documents.py` run from
  `C:\Users\BenDe\GitRepos\MAM-basics` on this repo's interpreter **after the venv deletion**, as
  UXLC-utils' Phase 7 did: **silent, exit 0, zero bytes of stdout**, and no `fline mismatch` line,
  so the location cross-check still holds the 397A and 406A coordinates Phase 0 sent upstream.
- **All 701 artifacts compared against their HEAD blobs** with `git cat-file --batch`, once before
  the deletion and once after the deletion and the oracle run, **with the same verdict both
  times: 700 byte-identical, 1 line-ending-only, 0 genuinely different.** The one is
  `out/cam1753-crops.json`, whose checkout is still CRLF — **the same file Phases 0, 1, 3, 4 and 6
  each found, six phases running.** `git status --porcelain` was not used in book-of-job, per this
  plan's Phase 0 subsection.
- **Suite 945 passed, 5 skipped, 59 subtests**, unchanged, via
  `.venv/Scripts/python.exe py/main_test.py -q` from the repo root. **The `59 subtests` figure
  reproduced again**, which is the fourth measurement confirming Phase 4's correction of
  holman-ketiv-qere's finding 3: the figure comes from `unittest`'s native `self.subTest` in six
  modules under `py/tests/`, not from the absent `pytest-subtests`.
- **`check_all.py` 7 of 7**, mark order over 298 files, escapes over 241 `.py`.
- **`git status --porcelain` empty in UXLC-utils**, still at `4d1ad89`; in MAM-basics it held only
  this phase's own two prose files. **No Python was edited in either repo, so black had nothing to
  run on.**

### What this phase hands the codex-index trio, beyond what the programme plan already carries

1. **The `alef_bet_to_ascii.py` citation, two public copies and one blob.** Fix this repo's and
   codex-index-aleppo's together when that repo's Python moves, and note that mgketer's third copy
   is diverged and sits in MAM-private, so it is Ben's either way.
2. **Grep for the repo's NAME, not for `<repo>/py`.** The trio's Python is under `py/` in
   codex-index-aleppo and at the root in codex-index-cam1753, so the two halves of the trio would
   need different path greps — and a name grep needs neither.
3. **Run the grep against MAM-private**, which is the programme's Phase 7 finding 2 and which paid
   again here: three of the five stale citations are in that repo, and one of the three is the
   same "check for matching logic to propagate" shape holman-ketiv-qere's Phase 7 found in the
   same `mgketer/documentation/` tree.

### The open question is still open, and this phase did not touch it

`mb_cmn/provenance.py`'s `_repo_root()` is `parents[2]`. Phase 4's deletion of book-of-job's
`mb_cmn/` ended the question **for book-of-job**, and Phase 6 recorded why it was latent even
before that: nothing there passed `generator_file`, so no breadcrumb was ever written. **What
remains open is only whether this repo's copy should walk to `.git` and be re-vendored for the
other repos that still hold it** — the two codex-index repos and diffable-pointed-hebrew. Phases
1, 3, 4 and 6 each put it to Ben and none picked; this phase did not pick either.

---

**The original prescription follows.**

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
