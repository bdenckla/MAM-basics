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
| 3 — copy the Python in (dual residency) | **not started** |
| 4 — empty book-of-job | **not started** |
| 6 — breadcrumbs and issue citations | **not started** |
| 7 — cross-repo bookkeeping | **not started** |

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
