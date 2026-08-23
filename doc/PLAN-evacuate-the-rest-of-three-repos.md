# Total evacuation: book-of-job, holman-ketiv-qere and UXLC-utils

Written 2026-08-22, the day
[`PLAN-evacuate-python-programme.md`](PLAN-evacuate-python-programme.md) closed — its last row,
the codex-index trio, finished that morning and all six public repos in that programme hold zero
tracked `.py`. This plan is the second stage Ben decided the same day: the three repos named in
the heading give up **everything else** as well, and stay alive as redirect hosts.

**Read [`PLAN-evacuate-the-rest-of-wlc-utils.md`](PLAN-evacuate-the-rest-of-wlc-utils.md) before
executing any phase here.** That plan did this once, for one repo, and finished 2026-08-17. It is
the model, and this file leans on it rather than restating it: where a question was settled there,
this file cites the section by name and says only what differs. The two files are not
interchangeable — that one is a completed execution record, this one is unexecuted work.

**The destination repo is `C:\Users\BenDe\GitRepos\MAM-basics`**, whose venv is
`C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe`. The three source repos are
`C:\Users\BenDe\GitRepos\book-of-job`, `C:\Users\BenDe\GitRepos\holman-ketiv-qere` and
`C:\Users\BenDe\GitRepos\UXLC-utils`. None of the three has a venv it needs any more, their Python
having gone.

**No skill is needed for this plan.** It touches no prose about accentuation, so the
`hebrew-prose` skill does not fire; the instruction files that do govern it are
`C:\Users\BenDe\.claude\CLAUDE.md` (global) and `C:\Users\BenDe\GitRepos\MAM-basics\CLAUDE.md`
(this repo). Read both before the first edit. One phase writes prose *about* the Holman review and
the Job manuscripts into `DATA-LICENSES.md`; that is licensing prose, not accentuation prose.

## Status

**PAUSED — Ben, 2026-08-23, after Phase 0 closed at `1410b5d`**: *"I want to pause the evacuation
work for a while."* The Phase 1 chip was cancelled rather than launched. Nothing is in flight: no
tree has landed, no repo but MAM-basics has been written to, and the dual-residency window has not
opened, so this is the first of the safe stopping places under "How to run this plan across
sessions" and can last indefinitely. **To resume**: re-check the four heads against the ones
Phase 0's record names, re-run the preconditions, re-measure per the Scale section's standing
instruction, and then run Phase 1 — which is verification only, per its Status row below.

| Phase | State |
|---|---|
| 0 — Preflight: baselines, collision census, and the five decisions | **DONE 2026-08-23** — seven commits to this file, `0decb3f` through the one recording Decision E. Every Scale figure reproduced but the "outside `gh-pages/`" column (48 / 596 / 734, not 50 / 597 / 737); the census reproduced with one refinement (`sanity_problems.json` moves, 40 duplicates drop, not 41); the layer-4 sweep returned the list the plan has; baseline 941 passed / 5 skipped / 59 subtests, ruff and black clean. All five decisions answered, one at a time: A `book-of-job` / `holman` / `uxlc`; B no `LICENSE`, and the docx does not move — the cord to it is cut; C same relative path, `data/` at `data/`; D `py_ac_loc/` dropped; E two files deleted, the meteg-marks pair lands at `out/`. Two questions parked for Phases 3 and 5, written where those phases will find them |
| 1 — `.gitattributes` merge in MAM-basics | not started — **verification only since 2026-08-23**: its one owed edit, `*.docx binary`, went with Decision B's sub-question, so it proves its two no-ops on one file each and commits nothing but its record |
| 2 — Generalize the redirect-stub generator to a table of four | not started |
| 3 — holman-ketiv-qere, the pilot lane; plus the generated landing page | not started |
| 4 — book-of-job | not started |
| 5 — UXLC-utils | not started |
| 6 — Cross-repo bookkeeping, and close the second stage | not started |

---

## Context — what this plan does, and the two programme decisions it executes

Two sections of [`PLAN-evacuate-python-programme.md`](PLAN-evacuate-python-programme.md) are this
plan's charter. Both are Ben's decisions of 2026-08-22, both are recorded there rather than here,
and **neither is reopened by this plan**:

1. **"Decision — total evacuation for three repos, Python-only for the codex-index trio"**, with
   its subsection **"Everything moves; only stubs stay"**. Search either heading. The whole
   `gh-pages/` tree of each of the three repos moves into MAM-basics; each published page is
   replaced in place by a forwarding stub; a `404.html` catch-all covers everything else; the
   `README.md` of each emptied repo points a GitHub browser at the new location. **The
   codex-index trio is excluded and keeps its data.**
2. **"Decision — the site's landing page becomes generated"**. `gh-pages/index.html` in
   MAM-basics is hand-written today and says so in an HTML comment. It becomes generated, with
   one entry per `gh-pages/<subtree>/index.html`, in the phase that lands the first arriving
   subtree — which is Phase 3 here.

**The reversal recorded in "Everything moves; only stubs stay" is the one thing most likely to be
re-proposed by a fresh session, so read it before economizing.** An earlier decision the same day
was to leave the images behind and move only the HTML, on the ground that the images never change.
The premise was measured and is true; the conclusion was dropped anyway, because every image
reference in these pages is relative, so moving the whole subtree keeps every one of them valid
and moving only the HTML would mean repointing each reference **in the generators**. Do not
reinstate the split.

**What this plan is not.** It does not reopen any of the four completed Python-evacuation plans,
and it does not touch codex-index-aleppo, codex-index-leningrad or codex-index-cam1753 except as
readers (see Phase 5 and Phase 6). `PLAN-evacuate-the-rest-of-wlc-utils.md` was a new plan rather
than a reopening of `PLAN-evacuate-python-from-wlc-utils.md`, and the programme says explicitly
that the same holds here: **one new plan covering all three repos**, which is this file.

---

## Scale — measured 2026-08-22

**Re-measure every figure below before relying on it, and treat a mismatch as a finding rather
than as noise.** That instruction has already paid twice in the Python programme, once moving
every figure for a repo.

Heads at measurement: MAM-basics `edebdac`, book-of-job `3f096b9`, holman-ketiv-qere `5f419ef`,
UXLC-utils `292e7a7`.

**Re-measured later on 2026-08-22, by the review that corrected this file**: MAM-basics `59142cf`,
2,282 tracked files / 271.4 MB, `gh-pages/` unchanged at 285 / 50.0 / 155; book-of-job and
holman-ketiv-qere at the same heads with the same figures; UXLC-utils at **`b7b4eb9`**, one commit
past `292e7a7` — the repoint of its CLC deep links off wlc-utils, 3 files under `gh-pages/clc/`
and no change to any count in the table.

### The three sources

| Repo | tracked | MB | `gh-pages/` files | `gh-pages/` MB | HTML pages | outside `gh-pages/` | MB outside |
|---|---|---|---|---|---|---|---|
| book-of-job | 784 | 73.4 | 694 | 65.2 | **175** | 90 | 8.1 |
| holman-ketiv-qere | 348 | 58.1 | 300 | 35.5 | **6** | 48 | 22.6 |
| UXLC-utils | 780 | 43.1 | 184 | 18.4 | **91** | 596 | 24.7 |
| **total** | **1,912** | **174.6** | **1,178** | **119.1** | **272** | **734** | **55.4** |

**Phase 0's re-measure, 2026-08-23, at MAM-basics `d095871`, book-of-job `3f096b9`,
holman-ketiv-qere `5f419ef`, UXLC-utils `b7b4eb9`: every figure in the first six columns
reproduces exactly, and the last two columns did NOT.** The table read holman-ketiv-qere **50** /
22.6, UXLC-utils **597** / **24.9** and a total of **737** / **55.6** until that day. The cause is
the trap the paragraph below this one warns about, sprung on the column it does not mention: the
"outside `gh-pages/`" counts had been taken with a naive `git ls-files | grep -v '^gh-pages/'`,
and `git ls-files` quotes a path holding a non-ASCII byte, so the two JC3 pages in
holman-ketiv-qere and the one Hebrew-named JPG under UXLC-utils' `gh-pages/amb-early-mtg/img/`
begin with `"` rather than `gh-pages/`, escaped the exclusion, and were counted as outside —
2 files in holman-ketiv-qere, 1 file and 0.14 MB in UXLC-utils. The corrected figures are
`tracked − gh-pages files` and `MB − gh-pages MB`, which the first six columns had supplied all
along, and they are what the per-repo tables in Phases 3 and 5 sum to: holman-ketiv-qere's
itemized 43 plus its five housekeeping files (`.gitattributes`, `.github/workflows/pages.yml`,
`.gitignore`, `CLAUDE.md`, `README.md`) is 48, and UXLC-utils' 591 plus the same five is 596.
Re-establish with the null-delimited form, which is the only safe one for this column:

```bash
git -C ../holman-ketiv-qere ls-files -z | tr '\0' '\n' | grep -vc '^gh-pages/'
```

The same miscount had been copied into Decision C, Phase 3 and Phase 5, each corrected in place
the same day with its old figure noted beside it.

```bash
git -C ../book-of-job ls-files | wc -l
```

```bash
git -C ../book-of-job ls-tree -r -l HEAD gh-pages | awk '{s+=$4; c++} END {print c, s/1048576}'
```

```bash
git -C ../book-of-job ls-files -z gh-pages | tr '\0' '\n' | grep -ci '\.html\?$'
```

**Use the `-z` form for the page count.** holman-ketiv-qere has two `gh-pages` paths that
`git ls-files` quotes, and a naive `grep '\.html$'` drops them.

**The `gh-pages/` figures match the programme's table exactly** — 694/65.2/175, 300/35.5/6,
184/18.4/91 — so nothing drifted in that half between the programme's measurement and this one.

**Three counts matter and they size three different jobs**, which is why they are kept apart: the
**1,178** is the size of the `gh-pages/` move, the **272** is the size of the stub set left behind
(one stub per HTML page), and the **734** is a third job the programme's tables do not cover at
all — the data, inputs and prose outside `gh-pages/` that "total evacuation" also carries. (This
figure, and the 596 two sentences on, read 737 and 597 until Phase 0's re-measure of 2026-08-23 —
see the note under the table.)

**holman-ketiv-qere is the lopsided one**: 300 files moved and **6** stubs written, its published
site being almost entirely images. **UXLC-utils is lopsided the other way**: 184 files under
`gh-pages/` and **596** outside it.

### The destination

MAM-basics at `edebdac`: **2,279** tracked files, **271.3 MB**, of which `gh-pages/` is **285
files / 50.0 MB / 155 HTML pages** — essentially all of it wlc-utils'.

**The programme's figures for MAM-basics are already stale and this is the re-measure.** It
records 2,220 files / 270.7 MB, measured earlier on 2026-08-22; the tree has since grown by 59
files and 0.6 MB. Nothing follows from the drift except the instruction that produced it: measure
again at Phase 0. **Phase 0 did, 2026-08-23, at `d095871`: 2,282 files / 271.4 MB, `gh-pages/`
285 / 50.0 / 155** — the 2026-08-22 review's figures exactly, the three commits since `59142cf`
having touched only this file.

After all three lanes: roughly **1,463 files / 169 MB** under `gh-pages/`, and about **4,100 files
/ 430 MB** for the repo. Git stores these as ordinary blobs and nothing here is near a size limit.
(This sentence said "about 3,900 files / 380 MB" until Phase 0, 2026-08-23, and neither figure
follows from the table: 2,282 + 1,912 is 4,194, less the 15 housekeeping files that collide by
path and do not travel, the 40 duplicate blobs Phase 5 drops rather than moves (12.2 MB — see
Phase 0's census record) and `UXLC-utils.code-workspace`, is 4,138 files; 271.4 + 174.6 less the
same 12.2 MB is 433.8 MB. Decision D's `py_ac_loc/`, 76 files / 7.8 MB, and Decision B's docx,
20.6 MB, come off those figures only if Ben drops them. The conclusion the figures served — that
nothing is near a size limit — is unchanged either way.)

**For scale against the precedent:** wlc-utils' move carried 284 files / 50.0 MB and left 154
stubs plus `404.html`. This is about four times its file count in the `gh-pages/` half alone, and
the 734 files outside `gh-pages/` have no counterpart in it at all — wlc-utils' `out/` 193, `in/`
135, `doc/` 6 and `data/` 1 came to 335, which is less than half of what these three repos hold
outside their published trees.

---

## Decisions carried in — do not relitigate

These were settled elsewhere and are named here so that a fresh session does not re-put them.

1. **Everything moves; only stubs stay.** Ben, 2026-08-22, reversing an earlier decision the same
   day. See the programme's "Everything moves; only stubs stay".
2. **`mb_cmn/provenance.py`'s `_repo_root()` stays `parents[2]`.** Ben, 2026-08-22. The programme
   has a whole section on it, recording that the alternative costs three commits across three
   repos and that al-hatorah's three tracked breadcrumbs would be rewritten to name the wrong
   tree. **Do not re-propose the `.git` walk.** It had been carried as open by six phases across
   two plans before it was decided.
3. **Alive beats archived.** `PLAN-evacuate-the-rest-of-wlc-utils.md` §"Why alive beats archived":
   an archived repo cannot be edited, so its pages become frozen duplicates with no canonical tag
   and no signal which copy is current. A stub says "this moved"; an archive says nothing.
4. **Pages must be live on the destination before any repo is flipped to stubs.**
   `PLAN-evacuate-the-rest-of-wlc-utils.md` §"Why Pages must be live first". **All three repos
   already satisfy this** — MAM-basics' Pages deploy has been live since 2026-08-13, and the
   generators for all three repos moved here on 2026-08-19 (book-of-job), 2026-08-18
   (holman-ketiv-qere) and 2026-08-02 (UXLC-utils).
5. **The stub generator is generalized, not copied.** The programme says so directly:
   `py/main_wlc_redirect_stubs.py` "is the template to generalize rather than to adapt".
6. **Each evacuated repo's clone comes off the local disk when its lane finishes.** Ben's
   decision, 2026-08-22. **The repo itself stays alive on GitHub** — this removes a directory under
   `C:\Users\BenDe\GitRepos`, and nothing else. **wlc-utils is doing the same thing on the same
   day**, by Ben's instruction in a concurrent session — *"Freeze the manifest, then delete the
   clone and workspace entry"* — so this is not a departure from that precedent but a continuation
   of it, and al-hatorah's clone came off on 2026-08-11 the same way. The lane's Step 6 is where it
   happens, in what order, and why it is worth doing.
7. **A manifest entry stays a bare path; it does not gain an optional explicit redirect target.**
   Ben's decision, 2026-08-22, put to him by the session that froze wlc-utils' set. **Considered
   and declined, not pending** — do not re-propose it as an improvement. It would have made a
   renamed page's stub repointable at the content's new home; without it the two repairs are
   republish-at-the-old-path or drop-the-URL-and-its-stub. The reasoning, and the reason the
   decision is cheap to revisit if it ever bites, is under Phase 2's "Renaming a frozen page".
   **Decision 8 below does NOT weaken this, and a draft of this file that said it did was wrong on
   a point of attribution** — recorded because the mistake is the kind a later reader would make
   again from the same materials. That draft had Ben deciding on the premise "the known citations
   are few, so dropping a stub costs nothing real", and then had decision 8's unknowable cited set
   undercutting him. **That premise was the sessions' rendering of his decision, never his
   reasoning.** Ben, 2026-08-22, on being shown the supposed tension: *"I stand by that decision.
   It was made in your ignorance of how widespread the need for stubs is; I was perfectly aware of
   how widespread the need for stubs is when I made that decision."* So the two decisions were
   taken by someone holding both facts at once, and there is no tension between them to resolve.
   **What makes the deferral safe is unchanged and never depended on a citation count**: a rename
   fails the suite by name, and adding the branch **then** is the same one-line change as adding it
   now, so nothing is foreclosed by waiting.
8. **Assume every one of these repos' old URLs is cited where Ben cannot reach it.** Ben,
   2026-08-22, answering the question Phase 0 was going to put to him: *"Assume URLs to all three
   are cited in places I cannot reach (Twitter posts, emails sent, etc.)"* **Non-empty and
   unknowable — there is no list and there will not be one.** This is what keeps three redirect
   hosts alive, and what forbids pruning any manifest to the citations that can be found. Layer 4
   under "The oracle" has the three consequences.

---

## Decisions this plan needs from Ben — five, all at Phase 0 — ALL FIVE DECIDED 2026-08-23

**Every decision below is answered, one at a time, at Phase 0 on 2026-08-23; each answer is the
first paragraph of its section**, dated and in his words where he gave any, with the text that was
put to him kept beneath it as the record of what he was choosing between. Phase 0's execution
record has the five in one place.

**Put these to Ben one at a time, in plain prose, before Phase 1.** Each is a genuine choice with
a cost on both sides; each carries a recommendation so the question is answerable rather than
open-ended. **Record the answer and its date in this section**, not in a phase's execution record,
so the answers stay together.

### Decision A — what each arriving subtree is called under `gh-pages/`

**DECIDED — Ben, 2026-08-23, at Phase 0: `gh-pages/book-of-job/`, `gh-pages/holman/` and
`gh-pages/uxlc/`.** Neither of the two forms put to him, but one of each plus a third spelling:

| Repo | subtree | published prefix after the move |
|---|---|---|
| book-of-job | `book-of-job` | `bdenckla.github.io/MAM-basics/book-of-job/` |
| holman-ketiv-qere | `holman` | `bdenckla.github.io/MAM-basics/holman/` |
| UXLC-utils | `uxlc` | `bdenckla.github.io/MAM-basics/uxlc/` |

His reasons, as given: book-of-job keeps its full name because the short `job` "is sometimes
confusing (particularly when lowercase) because of the English word 'job'"; UXLC-utils becomes
`uxlc`, which names the edition rather than abbreviating the repo, exactly as `wlc` does; and
holman-ketiv-qere becomes `holman`, the reviewer's name. **So the redirect is a prefix rewrite
for all three and a prefix insertion for only the first** — which costs nothing, since Phase 2's
table row carries the old prefix and the new one per repo in any case, and is what the wlc row
already does (`bdenckla.github.io/wlc-utils/` → `…/MAM-basics/wlc/`). Nothing else in this
section is changed by the answer; it stands as the record of what was put to him.

The published URL becomes `bdenckla.github.io/MAM-basics/<subtree>/<path>`, and `<subtree>` is a
free choice. wlc-utils' tree landed at `gh-pages/wlc/`.

**Recommendation: the repo names verbatim** — `gh-pages/book-of-job/`,
`gh-pages/holman-ketiv-qere/`, `gh-pages/UXLC-utils/`. Three reasons:

- **It coins no alias.** `~/.claude/CLAUDE.md`'s prose section is explicit that a thing gets one
  name and that a coinage has to be defined where it is introduced. `boj` and `hkq` would be new
  names for things that already have names.
- **It makes each redirect a pure prefix *insertion* rather than a rewrite.** The old URL
  `bdenckla.github.io/book-of-job/x` becomes `bdenckla.github.io/MAM-basics/book-of-job/x`, so the
  mapping needs no table and no reader has to learn it.
- **It survives being read cold**, in a citation, years later.

**The alternative is the short form** — `job/`, `hkq/`, `uxlc/` — matching `wlc/` and matching the
`boj_paths.py` / `hkq_paths.py` / `uxlc_paths.py` module names already in `py/`. **`wlc` is not
quite a precedent for it**: `wlc` names the Westminster Leningrad Codex, a real thing with that
name, rather than abbreviating `wlc-utils`. By the same test `uxlc` is a real name too, `job` is
arguable, and `hkq` is a coinage. So the short form is not uniform even on its own terms.

**Whichever is chosen, choose all three at once and write them into this section**, because Phase
2's generalized generator takes them as a table and Phase 3 is the first to consume it.

**Two riders travelled with this decision, both from Phase 2's "Naming" paragraphs, and both are
DECIDED — Ben, 2026-08-23, taking the recommendation on each.** They were put alongside Decision A
because all three bear on what the tool is called; Decision A itself is still open.

- **Rename `py/main_wlc_redirect_stubs.py` and `py/wlc_redirect/` to `py/main_redirect_stubs.py`
  and `py/redirect_stubs/`.** Decided 2026-08-23. Phase 2 says when in its sequence the rename
  happens — after the byte-identity check, never before.
- **Republish wlc-utils' 155 committed stubs once after the rename**, so their `GENERATED by`
  comment names the generator that exists, rather than leaving them naming a retired file.
  Decided 2026-08-23. One commit in wlc-utils, from the shallow clone Phase 2 makes for the
  byte-identity check; the expected diff is exactly one comment line in each of 155 files, and
  anything beyond that is a finding.

### Decision B — the licence position for the arriving trees

**DECIDED — Ben, 2026-08-23, at Phase 0: leave each of the three emptied repos without a
`LICENSE`, as it is today.** Taking the recommendation: an emptied repo holds nothing but generated
stubs and a `404.html`, so there is nothing of substance left in it to license, and adding one
would be a new statement with no need behind it. Each lane's Step 2 still adds the arriving tree's
rows to `DATA-LICENSES.md`, the crops and Holman's images getting a row of their own modelled on
the `gh-pages/wlc/*/img/` row. Re-checked the same day: still no `LICENSE` in any of the three
(book-of-job `3f096b9`, holman-ketiv-qere `5f419ef`, UXLC-utils `b7b4eb9`). **The docx
sub-question below was put to him separately**; its answer is recorded beside it.

**None of the three repos has a `LICENSE` file.** Checked 2026-08-22: `ls ../book-of-job | grep -i
licen` and the same in the other two return nothing, where wlc-utils has a CC0 `LICENSE` at its
root. That is what made wlc-utils' Phase 4 tractable and it does not transfer.

MAM-basics is GPL-3.0 with `DATA-LICENSES.md` carving out per-path terms. The arriving trees
include material that is plainly not MAM-basics' to grant — book-of-job's `gh-pages/jobn/img/`
holds crops from photographic facsimiles of the Aleppo, Leningrad and Cambridge 1753 manuscripts,
holman-ketiv-qere's `gh-pages/img/` holds 154 images extracted from Holman's own review document,
and UXLC-utils' `in/` is tanach.us's under the terms `DATA-LICENSES.md` already states for
`in/UXLC-39/` and `in/UXLC-misc/`.

**Recommendation:** add a row set per arriving tree to `DATA-LICENSES.md`, modelled on the one row
that already covers the three `gh-pages/wlc/*/img/` directories together and says *"each rights
holder's; no grant is made or implied here"* (one row, not three — corrected by the 2026-08-22
review); leave each emptied repo without a `LICENSE`, as it is today. **The question for Ben is the
second half** — whether an emptied repo holding nothing but generated stubs should acquire a
`LICENSE` it never had. wlc-utils kept the CC0 it already had, which is not the same as adding one.

**A sub-question that is Ben's alone: holman-ketiv-qere's `Review of Qere and Kethib readings in
the Aleppo and Leningrad.docx`**, 20.6 MB and 90% of that repo's non-`gh-pages` bytes. It is
Holman's own document, and moving it into MAM-basics moves it under a different repository's
licence statement. It has a reader — `hkq_paths.review_docx_path()`, called by
`main_extract_docx_and_render_table.py`, which is that repo's oracle — so it cannot simply be
dropped.

**DECIDED — Ben, 2026-08-23, at Phase 0: the docx does NOT move to MAM-basics, and it is
removed from holman-ketiv-qere; the extracted data becomes the source data.** His words: *"I'm
confident in the extractor; let's remove the docx file from the holman-ketiv-qere repo and not
evacuate it to MAM-basics. Also accordingly of course we need to 'cut the cord' to it, treating
the data we extract from it as the source data (although of course keeping documented that it
originally came from a docx)."* Put to him with three options — move it with a
`DATA-LICENSES.md` row of its own (the recommendation), move it outside `gh-pages/` (the same
thing), or leave it behind as the one non-stub file the emptied repo keeps — and he chose a fourth.
**"Cannot simply be dropped" above was true only while the extractor had to run; the decision is
that it no longer has to.** What follows, each at the phase that owns it:

- **Phase 1 loses its one owed edit.** The `*.docx binary` rule was wanted only ahead of this
  file arriving, and it is the only `.docx` tracked in any of the three repos (checked 2026-08-23
  with `git ls-files '*.docx'` in each). MAM-basics' `.gitattributes` already covers everything
  that still arrives, so Phase 1 is verification only — its two prove-it-on-one-file checks — and
  commits nothing unless a check fails.
- **Phase 3's Step 3 cuts the cord, which is the lane's largest change for this repo.**
  `docs-not-served/table_data.json`, `docs-not-served/introduction.md` and the 154 images under
  `gh-pages/img/` stop being regenerated and become tracked source data. The `extract()` half of
  `main_extract_docx_and_render_table.py` — `hkq_cmn/extract_docx_pipeline.py`'s
  `parse_docx_archive` and `write_extract_files`, `hkq_cmn/extract_docx_xml_utils.py`,
  `hkq_paths.review_docx_path()` and `REVIEW_DOCX_NAME` — retires; the two verifications
  (`verify_table_words_in_mam_plus`, `verify_table_notes_in_uxlc`) and
  `render_table_data_findings_html` stay, reading the now-source JSON, and the script is renamed
  for what it still does. **`hkq_cmn/extract_docx_notes.py` stays whatever its name says**: the
  two verifiers and `py_render/rt_mam_uxlc_diff_descriptions.py` import `standard_book_name`,
  `INVISIBLE_MARK_PATTERN` and `parse_verse_reference` from it. The images were write-once
  already — `export_images` raises rather than overwrite a differing image, per
  `hkq_paths.gh_pages_dir`'s docstring — so for them the cord was cut in practice long ago.
- **One design point for that Step 3, to be put to Ben at Phase 3 if the session cannot settle
  it from the code: `persist_verify_summary` writes the two verification summaries back INTO
  `table_data.json`.** While the file was generated that was enrichment of an artifact; once it
  is source data, it is a program rewriting a tracked source file in place with derived fields
  (`mam_plus_verify`, `uxlc_verify` and three row lists). Either the in-place rewrite stays, as
  an idempotent enrichment that `git status` proves clean, or the derived fields move out into a
  file of their own that the findings page reads alongside the source. The plan does not decide
  this; Phase 3's record says which was chosen and why.
- **The provenance stays written down, per the decision's last clause.** `table_data.json`'s
  own `source_document` field already names the docx and stays as it is;
  `docs-not-served/table_data_fields.md`, the hand-authored description of the JSON, is rewritten
  to say the table was extracted once rather than is extracted; and a `_provenance.md` beside the
  data — the convention `in/UXLC-39/_provenance.md` and `in/UXLC-misc/_provenance.md` already
  use here — records the document's name, that it is Holman's, the holman-ketiv-qere commit it was
  extracted from and the extractor's commit, and that **the document itself remains in
  `bdenckla/holman-ketiv-qere`'s history**, since Step 5 removes it from the tree and not from the
  repo, which stays alive. Step 2's `DATA-LICENSES.md` row says the same in licence terms: the
  images and the table text are Holman's, reproduced as the data the review pages derive from,
  no grant made or implied.
- **Phase 3's Step 5 deletes the docx alongside everything the earlier steps moved** — the one
  file in any lane that is deleted without having been copied first — and holman-ketiv-qere's
  own `*.docx binary` rule may stay in the `.gitattributes` Step 5 keeps.
- **The figures shrink accordingly**: what Phase 3 moves outside `gh-pages/` is 47 files /
  2.0 MB rather than 48 / 22.6, and layer 1 no longer has a docx to cover. The Scale table
  measures what the repos hold and is left as measured.

### Decision C — where each repo's non-`gh-pages` tree lands

**734 files, and the programme's decision sections do not cover them** (737 until Phase 0's
re-measure of 2026-08-23 — see the note under the Scale table). wlc-utils' precedent
merged at the same relative path (`out/`→`out/`, `in/`→`in/`, `doc/`→`doc/`) with one file
relocated (`data/lci_recs.json`→`in/lci_recs.json`).

**The path-collision census says merging is safe** — measured 2026-08-22, the only tracked paths
identical between MAM-basics and any of the three are housekeeping files plus
`gh-pages/index.html`, and, for UXLC-utils, 39 files under `in/UXLC-39/`:

```bash
git ls-files | sort > .novc/_mb.txt && git -C ../UXLC-utils ls-files | sort > .novc/_r.txt && comm -12 .novc/_mb.txt .novc/_r.txt
```

**Recommendation:** merge at the same relative path, per precedent, with the four exceptions in
Decisions D and E below.

**DECIDED — Ben, 2026-08-23, at Phase 0: the same relative path**, taking the recommendation —
*"I concur with your recommendation to use the same relative path."* Three particulars were put
to him with it and go with the answer:

- **Five new top-level directories appear in MAM-basics, all holman-ketiv-qere's**: `emails/`
  (26 files), `docs-not-served/` (4), `assets/` (4), `io/` (1) and `data/` (2, joined by
  UXLC-utils' 2 — `uxlc_atom_locations.json` and `uxlc_standard_atoms.json` beside
  `lci_augrecs.json` and `lci_recs.json`, no name shared). book-of-job and UXLC-utils add nothing
  at top level that MAM-basics lacks, `doc/`, `out/` and `in/` all existing; `py_ac_loc/` is
  Decision D. The six arriving `doc/` files clash with none of MAM-basics' 45.
- **`data/` lands at `data/`, NOT at `in/` as wlc-utils' one relocation did.** MAM-basics
  already holds `in/lci_recs.json`, wlc-utils' copy, and UXLC-utils' `data/lci_recs.json` (one
  blob with its own `in/UXLC-misc/lci_recs.json`) differs from it by exactly one header comment
  line — `"(see mb_cmn_bib_locales.py)"` against `"(see my_tanakh_book_names.py)"`, the `body`
  identical, as `py/boj_paths.py`'s docstring already records. Two parallel readers keep the two
  copies apart: `py/py_uxlc/my_uxlc_page_break_info.py` reads `paths.in_dir() / "lci_recs.json"`
  and `py/uxlc_misc/my_uxlc_page_break_info.py` reads `uxlc_paths.data_dir() / "lci_recs.json"`,
  and `py/main_write_page_break_info.py` writes the `data/` pair. The same-path census could not
  see this, since it compares equal paths and the precedent's relocation makes two unequal paths
  equal. **Landing at `data/` collides nothing and defers the collapse of the two copies — and
  of the two reader lineages — to Phase 5's trap 3**, which already owes Ben the "two copies of
  the same data" question for `in/UXLC-39/` and `in/UXLC-misc/`; `lci_recs.json` joins that
  question rather than getting one of its own.
- **`.claude/commands/halve.md` lands under `.claude-disabled/commands/`**, beside the two
  retired commands MAM-basics keeps there, rather than becoming a live slash command at
  `.claude/commands/`. Same relative path for the file, one directory over for the mechanism.

### Decision D — book-of-job's `py_ac_loc/`, which nothing reads

**DECIDED — Ben, 2026-08-23, at Phase 0: drop it.** Taking the recommendation as it stood after
Phase 0's blob comparison below — *"I concur with your recommendation to drop it."* So Phase 4
never copies `py_ac_loc/`; its Step 5 deletes it with the rest, and the 2026-02-19 snapshot of the
Job pages stays where it already is twice over, in `bdenckla/book-of-job`'s history and in
codex-index-aleppo's. Three consequences for Phase 4, each named below and repeated here so the
lane sees them together: the mark-order check goes from 509 files to 460 and that is the expected
change; `doc/reading-mam-simple.md` is reworded where it links to
`py_ac_loc/MAM-simple-provenance.md` and describes `py_ac_loc/MAM-XML/`; and what Phase 4 moves
outside `gh-pages/` is 9 files — `out/` 7 and `doc/` 2 — rather than 85.

**76 files, 7.8 MB, 96% of book-of-job's non-`gh-pages` bytes, and it has no accessor in
`py/boj_paths.py` and no reader anywhere in MAM-basics' `py/`.** Despite the `py_` prefix it holds
no Python: `MAM-XML/` (24 book XML, a vendored MAM-simple snapshot), `column-coordinates/` (24),
`line-breaks/` (24, hand-made), a `codex-index/` and two provenance files.

**It partly duplicates codex-index-aleppo, and only partly**, which is what makes this a decision
rather than a sweep: `MAM-XML` is one blob with codex-index-aleppo's, but `column-coordinates` and
`line-breaks` **differ** between the two repos. And MAM-basics already has a `py/py_ac_loc/`, which
is a **package of codex-index-aleppo's code** — the same name for a different thing, so a naive
move at the same relative path collides with a package.

Three options: move it into MAM-basics under a name that does not collide; merge it into
codex-index-aleppo, which is the repo whose data it duplicates; or drop it. **Recommendation: put
it to Ben with the three options and the blob comparison**, exactly as book-of-job's Phase 4 put
the 40 orphaned UXLC data files to him and he chose delete. Do not decide it inside a phase.

**Phase 0's blob comparison, 2026-08-23, book-of-job `3f096b9` against codex-index-aleppo
`1da6b23` — and it narrows the question.** "Differ" above was true and understated: **every one
of the 76 files is in codex-index-aleppo's history, and none carries an edit codex-index-aleppo
lacks.**

- **26 are one blob with codex-index-aleppo today**: the 24 `MAM-XML/*.xml` at the same paths,
  and `codex-index/index-flat.json`, which is codex-index-aleppo's `aleppo-wiki/index-flat.json`.
- **48 — the 24 `column-coordinates/` and 24 `line-breaks/`, all Job pages `270r`–`281v` — are
  one blob with codex-index-aleppo at its `0be4d38` (2026-02-19) and `295829e` (2026-02-24), 48
  of 48.** book-of-job's own last edit to them is `fa897f4`, 2026-02-19, the same ketiv-word fix
  made in both repos the same day. After `295829e` codex-index-aleppo alone moved on —
  `eb4bcaf` (2026-03-14) migrated the column IDs to its NofM format and the Deuteronomy pages
  `001r`–`006r` followed, which is why it holds 35 of each today against book-of-job's 24. So
  book-of-job's copy is a **strict older snapshot**, not a divergent one: a one-page diff is
  68+/33− in `column-coordinates/270r.json` and 112+/112− in `line-breaks/270r.json`, all of it
  codex-index-aleppo's later work. Re-establish by taking any of the 48 blobs from
  `git -C ../book-of-job ls-files -s py_ac_loc/line-breaks` and running
  `git -C ../codex-index-aleppo log --oneline --find-object=<blob>`.
- **`image-sources.md` was codex-index-aleppo's too, and was removed there on purpose** —
  `3a50ec1`, "Remove redundant image-sources.md (superseded by aleppo-pages-provenance.md)"; its
  Internet Archive API and leaf-to-page formula are in that repo's `aleppo-pages-provenance.md`
  and `doc/aleppo-line-breaks.md`.
- **The remaining two are provenance breadcrumbs about the copies themselves** —
  `MAM-simple-provenance.md` (284 bytes; the same path in codex-index-aleppo is a different blob,
  being that repo's own breadcrumb) and `codex-index/codex-index-provenance.md` (430 bytes, naming
  the old `codex-index` repo at `88553fe`). Neither says anything a dropped copy would still need.

**So the three options weigh differently than the paragraph above suggests.** "Merge into
codex-index-aleppo" would add nothing — that repo already holds every byte, 26 of them live and
48 in history — and "move into MAM-basics" would bring in a snapshot of another repo's data that
is superseded in the other repo. **That leaves drop as the natural answer, and the
recommendation becomes: drop it, unless Ben wants the Job-page snapshot of 2026-02-19 kept
somewhere for its own sake.**

**Two qualifications to "no reader", found the same day.** The claim that nothing in MAM-basics'
`py/` reads it is true of consumers and false of one lint: `py/check_mark_order.py` scans every
`.json` under `boj_paths.boj_data_root()` through `repo_scopes.corpus_roots()`, and its own
docstring names "24 line-break files under book-of-job's `py_ac_loc/`" as the reason it reads the
data root at all. It reported **509 files** on 2026-08-23; 49 of those are `py_ac_loc/`'s JSON
(24 + 24 + `index-flat.json`), so dropping the directory takes the check to **460**, and Phase 4's
"a change in what the lints cover is a finding" should expect exactly that change and no other.
No coverage is lost by it — the same pages' later versions are scanned under codex-index-aleppo's
own root, which is also in `corpus_roots()`. And book-of-job's `doc/reading-mam-simple.md`, which
Phase 4 moves, links to `py_ac_loc/MAM-simple-provenance.md` and describes `py_ac_loc/MAM-XML/`;
if the directory is dropped, Phase 4 rewrites those sentences rather than moving a dangling link.

### Decision E — the four loose UXLC-utils files, and one live instruction among them

**DECIDED — Ben, 2026-08-23, at Phase 0, taking each recommendation** — *"I concur with your
recommendation to delete."* The four dispositions, for Phase 5 to carry out:

| file | disposition |
|---|---|
| `UXLC-utils.code-workspace` | **delete** at Step 5, never copied — 107 bytes naming `.` and `../codex-index-leningrad`, matching the deletion of book-of-job's equivalent |
| `Possible false early meteg marks.code-search`, `Possible false early meteg marks.csv` | **move, landing at `out/`**, at Step 1 — a saved VS Code search (66 hits in 21 files over the old `in/UXLC` directory name, which the `# Including:` line still carries and which stays as written) and its result as data. `doc/clc-design.md:203` calls the CSV its seed list through a relative link into `doc/` that has never resolved; fix that link to `../out/…` as the doc moves, and say so in Phase 5's record |
| `shared-with-codex-index-leningrad.md` | **delete** at Step 5, never copied. Its claim — UXLC-utils is the canonical source for `codex-index-leningrad/UXLC-utils-sparse/` — becomes false with the move; its one live fact, the refresh command, already names and is documented in `py/main_lenin_vendor_uxlc.py`; its history note on `main_update_vendored_files.py` is already in `py/lenin_paths.py`'s docstring. Phase 5's Step 3 makes `main_lenin_vendor_uxlc.py`'s docstring say the source is now MAM-basics' own `in/UXLC-39/` and `data/`, and Step 5's owed codex-index-leningrad commit corrects that repo's `CLAUDE.md`, `README.md` and `UXLC-utils-sparse/provenance.md` the same way — the three homes that remain, where a fourth statement would go stale |

**Parked for Phase 5, noted to Ben and not put to him: whether the sparse copy should exist at
all afterwards.** Measured 2026-08-23: its only reader is MAM-basics' own
`py/main_lenin_wikisource_page.py`, through `lenin_paths.lci_augrecs_path()`, and nothing in
codex-index-leningrad (which has no Python) reads it. So after this plan it is a copy of MAM-basics'
own `data/lci_augrecs.json` read back through a sibling. Phase 5's trap 4 assumes it survives
with its refresh repointed; the alternative — read `data/lci_augrecs.json` directly, retire
`main_lenin_vendor_uxlc.py` and the 41-file `UXLC-utils-sparse/` tree in codex-index-leningrad —
is Phase 5's to put to Ben, at its Step 3, before the repoint is written either way.

`UXLC-utils.code-workspace` is orphaned by the evacuation, and
`PLAN-evacuate-python-from-book-of-job.md` records Ben deleting the equivalent file in that repo —
so **recommendation: delete it**, matching that precedent.
`Possible false early meteg marks.code-search` and `Possible false early meteg marks.csv` are a
saved VS Code search and its result as data, with no reader; **recommendation: move them with
`out/`**, since discarding a finding is a different act from tidying a workspace file.

**`shared-with-codex-index-leningrad.md` is the one that needs Ben.** It declares UXLC-utils
canonical for `codex-index-leningrad/UXLC-utils-sparse/` and gives the refresh command. **That
claim becomes false the moment UXLC-utils is evacuated**, and codex-index-leningrad's `CLAUDE.md`
and `README.md` depend on it — see Phase 5, which is where the coupling is worked out.

---

## The organizing idea: three more roots rejoin

The Python evacuation split one `repo_root()` into a CODE root and a DATA root, three times over.
`py/boj_paths.py`, `py/hkq_paths.py` and `py/uxlc_paths.py` are the three statements of that split,
each resolving a sibling clone through `paths.require_sibling(...)`.

**This plan rejoins them, and each of the three modules loses its reason to exist.** Afterwards the
data root and `paths.repo_root()` name the same directory, and the only thing left pointing at each
sibling is one resolution inside the redirect-stub generator — which is exactly what
`py/wlc_redirect/stubs.py`'s `wlc_utils_pages_dir` is today, and which its docstring calls "THE
LAST REFERENCE TO THAT SIBLING IN THIS TREE".

**The three modules are spelled inconsistently, and a repoint has to know that before it starts**
— surveyed 2026-08-22:

| module | data-root constant | how the root is resolved |
|---|---|---|
| `py/hkq_paths.py` | `DATA_REPO_NAME = "holman-ketiv-qere"`, **used** by `hkq_data_root()` | through the constant |
| `py/boj_paths.py` | `DATA_REPO_NAME = "book-of-job"`, **declared and never referenced**, including inside the module | `boj_data_root()` hardcodes the literal |
| `py/uxlc_paths.py` | **no such constant at all** | `uxlc_data_root()` hardcodes the literal |

**And `py/uxlc_paths.py` resolves a SECOND sibling, book-of-job** — `book_of_job_dir()` and
`require_book_of_job_dir()`, read by `py/main_map_changes_to_book_of_job.py` for
`book-of-job/out/enriched-quirkrecs.json` and `book-of-job/gh-pages/jobn-details/`. That script is
one of UXLC-utils' three oracle commands, but the clone it resolves is book-of-job's, so the
repoint is **Phase 4's**, not Phase 5's — see Phase 4's trap on it. A Phase 4 that follows
`boj_paths.py` alone leaves it pointing at the sibling. (Added by the 2026-08-22 review; the survey
above had recorded `uxlc_paths.py` as resolving UXLC-utils only.)

**And UXLC-utils has a second, independent resolution path that `uxlc_paths.py` does not go
through.** `py/mb_cmn/paths.py` defines `uxlc_utils_dir()` and `require_uxlc_utils_dir()` — find
them by name, not by line number — with four call sites in
`py/main_extract_docx_and_render_table.py`, `py/main_lenin_vendor_uxlc.py` and
`py/main_wlc_vendor_uxlc.py` (twice). A repoint that follows `uxlc_paths.py` alone misses all
four. **`py/tests/test_verify_table_notes_in_uxlc.py` spells `"UXLC-utils"` ten more times, and
none of the ten is a resolution**: each builds a fixture under `tmp_dir / "UXLC-utils" / "in" /
"UXLC-39"` and passes it as `uxlc_utils_path=`, so the test reaches no sibling and needs no
repoint. (This paragraph counted "eight literal-string sites" and "all twelve" until the 2026-08-22
review; the fixture spellings had been lumped in with the four resolutions.)

**Two accessors must NOT be swept along with the rest, and both are easy to sweep:**

- **`hkq_paths.mam_qere_words_path()`** returns `paths.out_dir() / "mam-qere-words.json"` — the
  **code** root's `out/`, MAM-basics' own, not the data root. It already points where the others
  are being moved to.
- **`py/hkq_cmn/table_row_github_issues.py`'s `REPO_NAME`** is `"holman-ketiv-qere"` as a
  **GitHub tracker name**, passed to `gh issue list --repo`. It is not a filesystem path, and
  MAM-basics' `CLAUDE.md` §"Five issue trackers" names this exact module as the trap to check for
  first. A blanket rename breaks the rendered issue links on the report pages.

**What dissolves rather than moves.** As wlc-utils' `.novc/` split and
`gen_highlight_picker`'s relative-URL constraint dissolved:

- **`py/main_wlc_vendor_uxlc.py` becomes a self-copy and should be deleted, along with its mega
  step.** Read its docstring: it copies `UXLC-utils/in/UXLC-39`'s XML and `UXLC-utils/out/UXLC-misc`'s
  JSON into MAM-basics' own `in/`. Once UXLC-utils' `in/` and `out/` are here, source and
  destination are the same tree. **This is measurable today and explains the collision census**:
  41 of UXLC-utils' non-`gh-pages` blobs are already in MAM-basics, being those 39 XML plus
  `all_changes.json` — and one 3-byte `[]`, `sanity_problems.json`, that nothing vendors and that
  is a coincidence rather than a copy (Phase 0's item 2, 2026-08-23).
  The mega's `wlc-vendor-uxlc` step goes with it, and the `find-uxlc-accent-changes` step's "must
  come after wlc-vendor-uxlc" note has to be rewritten. **This is Phase 5's largest single
  simplification and its largest single risk** — see that phase.
- **`all-repos.code-workspace`'s three entries.** Both the UXLC-utils plan and the book-of-job
  plan recorded a decision to leave `../book-of-job`, `../holman-ketiv-qere` and `../UXLC-utils`
  listed, on the ground that each still held hundreds of tracked non-Python files. **That reason
  expires here.** Phase 6 disposes of it. **`../wlc-utils` is already out**: it left the file on
  2026-08-22 with its clone (MAM-basics' `CLAUDE.md` §"There is no local `wlc-utils` clone
  either, and its stub set is frozen"), and the file listed 19 folders when the review of this
  plan checked later that day. (This sentence read "Note that wlc-utils is still listed,
  deliberately" until that review.)

---

## The oracle: what replaces "copy, don't move"

Data cannot be run twice, so the three layers of
`PLAN-evacuate-the-rest-of-wlc-utils.md` §"The oracle question: what replaces 'copy, don't move'"
apply unchanged in shape. What differs is layer 2, and the difference is large enough to state
first.

**Layer 1 — blob-hash manifest identity, which proves the copy.** `git ls-files -s` in the source
repo yields `<mode> <sha1> 0\t<path>` per file. After the copy, the same command in MAM-basics,
restricted to the destination paths, must yield the **identical SHA-1s**, differing only in path.
Git blobs are content-addressed, so this is exact byte-identity — and it is the **only** evidence
covering the 884 PNGs, 3 JPGs and the 4 woff2 across the three repos, which no program
regenerates and which layer 2 therefore says nothing about. (The 20.6 MB docx was in this list
until 2026-08-23; Decision B's sub-question took it out of the move. **And once Phase 3's Step 3
cuts the cord, layer 1 becomes the only evidence for holman-ketiv-qere's `table_data.json`,
`introduction.md` and the 154 images under `gh-pages/img/` as well**, those having stopped being
regenerated.)

**This is why Phase 1 must precede every copy**: `git add` applies `.gitattributes` at add time, so
a differing eol rule changes the blob.

**Layer 2 — zero regeneration diff, which proves the repoint. THE WLC-UTILS ORACLE DOES NOT COVER
THESE THREE REPOS, and assuming it does is the most expensive mistake available here.** Measured
2026-08-22: `py/main_0_mega.py`'s `_STEPS` holds **39** steps, and **exactly one of them is a
generator of any of these three repos' artifacts** — `gen-misc-authored-english-documents`,
book-of-job's oracle, covered two paragraphs down; none is a holman-ketiv-qere or UXLC-utils
generator. (This sentence said "34 steps and not one of them is a book-of-job, holman-ketiv-qere
or UXLC-utils generator" until the 2026-08-22 review: the count was wrong — `_STEPS` has not
changed since `5ed6bb4` on 2026-08-12 — and the claim contradicted the paragraph below it.)
Re-establish with

```bash
.venv/Scripts/python.exe py/main_0_mega.py --help
```

Each repo brings its own oracle, taken from its own completed Python plan's execution record. All
ten entry points named below were confirmed present in `py/` on 2026-08-22.

| Repo | Oracle | Artifacts | Source |
|---|---|---|---|
| book-of-job | `py/main_gen_misc_authored_english_documents.py`, alone | **183 of 701** rewritten; **518 written by no program**, being essentially the 515 PNGs | `PLAN-evacuate-python-from-book-of-job.md` §"The oracle: `main_gen_misc_authored_english_documents.py`, alone" |
| holman-ketiv-qere | **six commands, not one**: `main_extract_docx_and_render_table.py`, `main_ingest_uxlc_emails.py`, `main_estimate_uxlc_locations.py`, `main_render_uxlc_corrections.py`, `main_search_holam_he_qere.py`, `main_search_final_hiriq_verse_text.py` | 335 artifacts, 175 rewritten and 160 untouched at that plan's Phase 3 | `PLAN-evacuate-python-from-holman-ketiv-qere.md`, its "Regenerating everything is six commands, not one" block |
| UXLC-utils | `py/main_uxlc_mega.py`, `py/main_clc.py`, `py/main_map_changes_to_book_of_job.py` | **214**; at that plan's Phase 6, **127 rewritten and 87 not** | `PLAN-evacuate-python-from-UXLC-utils.md` §"The oracle ran as specified and passed" |

**holman-ketiv-qere's first command changes shape at Phase 3's Step 3**, by Decision B's
sub-question (Ben, 2026-08-23): the docx does not move, so `main_extract_docx_and_render_table.py`
loses its extraction half and is renamed for the verifying and rendering it still does, and
`table_data.json`, `introduction.md` and the 154 images under `gh-pages/img/` pass from "artifacts
the oracle rewrites" to "source data layer 1 proves". The six commands are still six; one of them
just writes less. Phase 3's record names the renamed command.

**book-of-job's oracle is the one that is also a mega step** — `gen-misc-authored-english-documents`
— so a mega run covers book-of-job's 183 and nothing else of these three repos'. Do not read a
clean mega as a clean move.

**Two of holman-ketiv-qere's six commands need something a fresh clone does not have**, and both
are named in that repo's plan: `main_ingest_uxlc_emails` needs the untracked mailbox at
`holman-ketiv-qere/.novc/eml/` (13 messages, present 2026-08-18), and `main_estimate_uxlc_locations`
needs the UXLC-utils clone. **The mailbox is a Phase 3 item** — it is untracked, so no commit moves
it, and the accessor `hkq_paths.eml_dir()` will point at a directory inside an emptied repo unless
the files are moved by hand and the accessor repointed.

**Layer 3 — mtime counter-checks, in both directions.** Snapshot mtimes before a regeneration and
compare after. In MAM-basics, expect a large not-rewritten set and **say which files are proved by
layer 1 and which by layer 2** — an empty `git status` over files nothing writes is not a claim.
In the source repo, expect **zero files touched**; an empty `git status` there proves nothing,
because a call site still pointing at the sibling rewrites a file to identical bytes, which git
cannot see and mtime can. UXLC-utils' Phase 6 record names the reusable script it used,
`.novc/oracle_mtimes.py` with `snapshot` and `compare` subcommands; rebuild it if it is gone, since
`.novc/` is not tracked.

**Layer 4 — the published-URL check, and a citation is one of TWO things, never one.** wlc-utils'
Phase 6 built a URL list, and the list conflated two kinds of citation until Ben separated them on
2026-08-22. **`py/wlc_redirect/stubs.py`'s docstring, corrected in `f762d2b`, is the statement of
record — read it before writing any prose here about what a stub is for.** Ben, 2026-08-22:
*"The stubs are for things out of my control... like references on tanach.us or URLs in emails I've
already sent. For the two that are under my control, why wouldn't I just update the URL rather than
rely on the stub."*

- **A citation Ben cannot reach is the REASON a stub exists.** tanach.us's published change list is
  the one enumerable example for wlc-utils, citing `accgram/goerwitz.html` five times in change
  proposals Ben submitted and that site publishes. **The copies vendored back under
  `UXLC-utils/in/UXLC-misc/` are snapshots of what tanach.us publishes, so editing one would
  falsify the snapshot and change nothing about the citation** — that is the trap this distinction
  is most likely to spring. Beyond that: emails already sent, other people's pages, bookmarks,
  search indexes, none of them enumerable.
- **A citation Ben CAN edit is a URL to update, and is not a reason for anything.** It belongs in
  that repo's lane as work, not in the argument for keeping a redirect host alive. **Updating beats
  redirecting**, and for a reason that outlives the preference: a stale link in Ben's own tree is
  checked by nothing, where a frozen manifest entry is checked by the per-repo manifest test on
  every suite run.

**Every inbound link this plan's sweep found is of the second kind, and that is a fact about the
instrument.** Measured 2026-08-22 across every clone under `C:\Users\BenDe\GitRepos` and
`C:\Users\BenDe\GitRepos\MAM-private` — all of them Ben's:

- `bdenckla.github.io/book-of-job/jobn-details/*.html` — seven sites in
  `MAM-private/mgketer/py/python_modules/diff_crops.py` and seven in that repo's
  `out-reports/by-book/D3-Job/suppressed.html`
- `bdenckla.github.io/book-of-job/jobn/job2_main_article.html` — `document-index/README.md`
- `bdenckla.github.io/UXLC-utils/wlc-a-notes/` — **one generator constant, `_WLCAU` in
  `py/author_boj/job5_orphan_qere_points.py`, emitted twice into book-of-job's
  `gh-pages/jobn/job5_orphan_qere_points.html`. It is already dead, and has been since at least
  2026-04-10 (book-of-job `ba0d97a`)**: UXLC-utils never published a `wlc-a-notes/` — that tree is
  wlc-utils', now `gh-pages/wlc/wlc-a-notes/` here — so the URL 404s today and wants
  `https://bdenckla.github.io/MAM-basics/wlc/wlc-a-notes/` whatever this plan does. It is Phase
  4's, being book-of-job's generator, and it is the "prefer the generator" case. No stub would
  ever have rescued it: after Phase 5 the UXLC-utils `404.html` would forward it to
  `MAM-basics/uxlc/wlc-a-notes/`, which does not exist. (Found by the 2026-08-22 review; the
  sweep recorded above had missed it. The forwarded path read `MAM-basics/UXLC-utils/…` until
  Decision A was answered on 2026-08-23.)

The sweep also returns the three `py/*_paths.py` docstrings, which name each repo's URL and go
with the modules at Step 3, and book-of-job's and UXLC-utils' own `README.md`, which name their own
sites and are rewritten at Step 5. Nothing else. **A bullet here read "UXLC-utils' published CLC
pages carry deep links, per `wlc-utils/README.md`" until the 2026-08-22 review**: those are links
*from* UXLC-utils' pages *to* wlc-utils, repointed in UXLC-utils `b7b4eb9` that day, and not a
citation of any of these three repos' URLs at all.

**`git grep` across Ben's clones finds exactly the citations that are work items and, by
construction, none of the citations that justify stubs.** So the list above is this plan's repoint
backlog, not its evidence. **An earlier draft of this section presented it as the evidence**, which
inverted the argument for all three repos at once.

**The question no sweep of this disk could answer — is any URL of these three repos cited anywhere
Ben cannot reach? — is ANSWERED, and the answer is yes for all three.** Ben, 2026-08-22:
**"Assume URLs to all three are cited in places I cannot reach (Twitter posts, emails sent, etc.)"**
So this is settled and **Phase 0 must not re-put it**; it is carried-in decision 8.

**The answer's shape matters as much as its content, and it is not the shape wlc-utils' was.**
wlc-utils had an enumerable citation — tanach.us's five, nameable and checkable. Here there is no
list and there will not be one: the cited set is **non-empty and unknowable**. Three consequences
follow, and they run in different directions, which is why they are stated separately:

- **The justification for keeping three redirect hosts alive is settled**, and needs no enumeration
  to stand on. It is the strongest possible answer for that purpose.
- **No emptied `README.md` may name a citation list**, because there is none to name. Say that the
  old URLs are cited in places Ben cannot reach — posts and sent email among them — and stop.
  **Naming the repointed in-tree citations there would be worse than saying nothing**, per Step 5.
- **Every published page is potentially cited**, so no page may be dropped from a manifest on the
  ground that nothing cites it. That was already the rule below; it now rests on something Ben has
  stated rather than on caution.

**And it does NOT license pruning the manifest.** Freeze each repo's whole published set at its
flip, exactly as Phase 2 says. The citations that matter most are the ones nobody can enumerate, so
the published set is the only available proxy for "what might be cited out there". **Do not reduce
the frozen set to the citations you can find** — this correction is about the argument for the
stubs and about repointing what Ben owns, and about neither the size of the frozen set nor whether
to have one.

**What the same sweep found NOTHING in, which is what turns an unexpected diff later into a finding
rather than noise.** Run 2026-08-22 as `git grep -n -I -E "book-of-job|holman-ketiv-qere|UXLC-utils"`
in every clone under `C:\Users\BenDe\GitRepos` and in `C:\Users\BenDe\GitRepos\MAM-private`,
ignoring `.venv` and `node_modules`:

- **Zero hits of any kind**, so no dependency and no prose to correct: **MAM-parsed, MAM-with-doc,
  MAM-OSIS, MAM-for-Sefaria, phonetic-hbo, ArtScroll, diffable-pointed-hebrew, hbofonts.** Eight
  clones, and the four MAM-\* data repos among them are the ones a reader would most expect to be
  coupled.
- **Prose or historical mentions only, with no path dependency and nothing to edit**:
  codex-index-aleppo's and codex-index-cam1753's `CLAUDE.md` and `MAM-simple-provenance.md`,
  MAM-simple's `py/main_test.py`, `MAM-private/al-hatorah/py/main_test.py`,
  `MAM-private/doc/PLAN-evacuate-private-repos.md`, and — added by Phase 0's re-sweep,
  2026-08-23, which found them where the 2026-08-22 sweep had not listed them — three more in
  `MAM-private/mgketer/`: `documentation/periodic-maintenance.md` (book-of-job "has held zero
  tracked `.py` since 2026-08-21", which stays true), `py/py_ac_word_image_helper/alef_bet_to_ascii.py`
  ("which was book-of-job's") and `py/python_modules/hebrew_word_id.py` ("the same scheme as
  *book-of-job*"). **codex-index-aleppo and codex-index-cam1753
  are named here deliberately**: the codex-index trio is excluded from this plan, and these two of
  the three turn out to have no dependency on any evacuated repo either, so nothing about the trio
  is contingent on this work. **codex-index-leningrad is the exception and is the one trio member
  this plan does owe a commit** — see Phase 5's trap 4.

So the repos this plan touches at all are: the three being evacuated, MAM-basics,
codex-index-leningrad, `MAM-private` (two prose files), `document-index`, and `github-misc` (the
two files that do not auto-sync). **Anything else showing a diff is a finding.**

---

## The per-repo lane — the six steps, stated once

Phases 3, 4 and 5 each run this lane for one repo. The lane is stated here so the three phases
record only what is specific to their repo and their execution, rather than triplicating it.

**Land — Licence — Repoint — Stubs — Empty — Remove.** One commit per step, minimum; more where a
step is large. The sixth step is not a commit at all.

**Step 1 — Land the tree (dual residency).** *In MAM-basics only; the source repo is not touched.*
Copy `gh-pages/` in under `gh-pages/<subtree>/` per Decision A, and the non-`gh-pages` tree per
Decision C. Nothing here reads the new files yet — the generators still write into the sibling.
**That is the dual-residency window and it is what makes the copy provable and revertible**, the
source staying authoritative until Step 3.

**THIS STEP PUBLISHES.** MAM-basics' `.github/workflows/pages.yml` triggers on `push: branches:
[main]` and uploads `path: gh-pages`, and MAM-basics' Pages has been live since 2026-08-13. So the
landing commit's push deploys the arriving subtree to
`bdenckla.github.io/MAM-basics/<subtree>/…` immediately. This is not a hazard — by the time the
commit exists the subtree holds the real files, so the pages serve correctly on the first deploy —
but it means **the manual gate wlc-utils' Phase 6 provided does not exist here**, and it is the
reason Step 1 verifies the deploy rather than only the diff.

Verify: layer 1 over every file; `gh run list --workflow pages.yml --limit 1` shows success; fetch
one page at each nesting depth from `bdenckla.github.io/MAM-basics/<subtree>/…` and confirm 200
plus correct rendering, images included.

**Step 2 — Licence scoping.** *In MAM-basics.* Add the arriving tree's rows to `DATA-LICENSES.md`
per Decision B. Model them on the existing `gh-pages/wlc/` rows, which are the register to match —
including the pattern that manuscript crops get a row of their own, apart from the pages, saying
no grant is made or implied (one row covers all three `gh-pages/wlc/*/img/` directories today).
**Do this before Step 3**, so the statement lands with the files rather than after
something reads them.

**Step 3 — Repoint every generator, and collapse the path module.** *In MAM-basics.* Every
accessor that composed a path off the data root now composes it off `paths.repo_root()`. When the
module has nothing left that names the sibling, delete it. **Check the two exceptions named in
"The organizing idea" above before sweeping**: `hkq_paths.mam_qere_words_path()` already points at
MAM-basics, and `hkq_cmn/table_row_github_issues.py`'s `REPO_NAME` is a tracker name.

Verify: run this repo's oracle from `C:\Users\BenDe\GitRepos\MAM-basics`; **zero tracked artifacts
come back modified** in either repo; mtime snapshots in both directions per layer 3, with **zero
files touched in the source repo**; `py/main_test.py` still green; `ruff check py` and
`black --check py` clean.

**Step 4 — Flip `gh-pages/` to stubs.** *In the source repo.* **Hard-gated on Step 1's deploy
having been HTTP-verified.** One commit: every HTML page **modified in place** — a stub at the same
path is a modification, not a delete-plus-add, which keeps the diff readable — `404.html` added,
and every non-HTML asset deleted. Nothing else changes.

**Capture the frozen manifest in this same step, as the commit immediately BEFORE the flip** — the
flip being the last moment the old published URL set is knowable. It cannot be the same commit:
the manifest is a MAM-basics file (`in/<repo>_redirect_pages.json`, under Phase 2's table) and
the flip is a commit in the source repo, and `build --publish` reads the manifest, so the
MAM-basics commit comes first. **The repo's row joins Phase 2's table, and the manifest test's
parametrize list, in that same MAM-basics commit** — not at Phase 2, where the manifest does not
exist yet and a missing one fails rather than skips. (This paragraph said "in this same commit"
until the 2026-08-22 review.)

**And split the citations two ways rather than listing them once**, per layer 4 above. An earlier
draft of this step said to capture "the list of places those old URLs are cited from" as one list,
which is the conflation Ben corrected on 2026-08-22:

- **Citations Ben controls are WORK, done in this same phase.** Repoint each at its new MAM-basics
  URL. Find them per repo with `git grep -n 'bdenckla.github.io/<repo>'` across every clone under
  `C:\Users\BenDe\GitRepos` and `C:\Users\BenDe\GitRepos\MAM-private` — the instrument that found
  wlc-utils' **ten**, repointed in `d70e14c`. **Prefer the generator to the artifact**: wlc-utils'
  four CLC deep links were one constant, `py/clc/clc_render.py`'s `_LC_CORROBORATED_LINK`, plus a
  regeneration. **Expect this to be real work in each of the three lanes rather than a footnote** —
  these repos cross-cite each other and MAM-basics far more than wlc-utils did.

  **Then re-run the sweep and record that it comes back clean, which is the half most likely to be
  skipped.** `stubs.py`'s docstring is the model, added in `abf32c2`: after the repoint, a
  `git grep bdenckla.github.io/wlc-utils` over every clone returns only prose *describing* the
  redirect and the tanach.us snapshots — **so a hit found later is a new citation of a dead site
  rather than one the sweep missed**, which is a claim the repoint cannot make without the second
  sweep. **The snapshots must stay as they are**: five citations each in `UXLC-utils/in/UXLC-misc/`
  and `in/UXLC-misc-fixed/`, their derived `out/UXLC-misc/` copies, and this repo's vendored
  `in/UXLC-misc/all_changes.json` and `in/accgram/uxlc_accent_changes.json`. Editing one falsifies
  the snapshot and changes nothing about the citation.
- **Citations Ben cannot reach are the REASON the stubs exist, and for these three repos there is
  no list of them to record.** wlc-utils had one enumerable citation of that kind, tanach.us's
  five, and `stubs.py`'s docstring names it. **These three have none**: the tanach.us snapshots
  under `UXLC-utils/in/UXLC-misc/` cite no URL of book-of-job, holman-ketiv-qere or UXLC-utils
  (the sweep under layer 4, 2026-08-22), and decision 8 is the whole of what is known — the URLs
  are cited in posts and sent email and there is no list. So the manifest's `comment` field
  records **decision 8 and its date**, names an enumerable out-of-reach citation only if one has
  turned up by then, and stops. **Only that belongs in the argument for keeping the redirect host
  alive**, and only that belongs in the emptied repo's `README.md`. (Until the 2026-08-22 review
  this bullet said the citations Ben cannot reach "go in the manifest's own `comment` field", and
  the paragraph below it called them "the second list" — a list decision 8 says does not exist.)

**So the "drop the URL and its stub" repair is never informed by a record here.** For wlc-utils
the repair can consult a named citation; for these three it is always dropping a URL that decision
8 says to assume is cited, and nothing captured at Step 4 can make that cheaper. Carried-in
decision 7 is why the repair matters; Phase 2's "Renaming a frozen page" says what this does to
the choice between the two repairs.

Verify: the layer-4 URL list against the old host, each redirecting to its MAM-basics equivalent;
a path with no stub exercises `404.html`; the generalized `check` subcommand passes against the
committed tree. **Check a fragment-carrying deep link in a browser** — it must land on the anchor,
not merely on the page, which is the acceptance test for the JavaScript half specifically. **And
check a stub whose own path needs percent-encoding**, where the repo has one: in holman-ketiv-qere
the two JC3 pages, whose names carry `#`, spaces and ז — their old URLs resolve only with `%23`,
and Phase 2's encoding requirement exists for them. Fetch the stub at the encoded old URL, confirm
200, and confirm the redirect lands on the page rather than on a fragment.

**Step 5 — Empty the rest.** *In the source repo, plus one commit in MAM-basics.* Pure subtraction
with no published effect, and worth an explicit look before running. Delete everything the earlier
steps moved. Keep `.gitignore`, `.gitattributes`, `.github/workflows/`, `gh-pages/` and the two
files below. Check for untracked residue: `git rm` leaves it behind.

**`README.md`** becomes one screen: this repo is a redirect host; the site is at
`https://bdenckla.github.io/MAM-basics/<subtree>/`; the mapping is a pure prefix rewrite; it moved
on `<date>`; **the repo still exists because its old URLs are cited in places Ben cannot reach —
posts and sent email among them — and there is no list of them, so do not write one**; its issues
are still live and read here; the data and code are in `../MAM-basics`; the pre-evacuation history
is intact here. **Do not justify it by a citation in one of Ben's own repos**: those were repointed
in this lane's Step 4, so citing one here would be claiming a reason the lane itself removed. **And
do not hedge it into "may be cited"** — carried-in decision 8 settles that they are.

**`CLAUDE.md`** shrinks to those facts plus the two only an agent needs — **`gh-pages/` is
generated, do not hand-edit it, regenerate with MAM-basics' stub generator**, and **there is no
Python and no data here**. Keep that repo's "a bare `#NN` here means a `<repo>` issue" note where
it has one.

**Step 6 — Remove the clone from `C:\Users\BenDe\GitRepos`.** *No commit anywhere.* **Ben's
decision, 2026-08-22**, given while this plan was being written, and **the wlc-utils precedent is
the same**: that clone came off the disk the same day, by the concurrent session, per carried-in
decision 6 and MAM-basics' `CLAUDE.md` §"There is no local `wlc-utils` clone either, and its stub
set is frozen". (This paragraph said the removal was "departing from the wlc-utils precedent,
whose clone is still on the disk" until the 2026-08-22 review, which found
`C:\Users\BenDe\GitRepos\wlc-utils` gone.)

**The repo stays alive on GitHub. Only the local clone goes.** Everything the redirect host is for
— the stubs, the `404.html`, the Pages deploy, the issue tracker, the pre-evacuation history —
lives at `github.com/bdenckla/<repo>` and is untouched by deleting a directory here. **This is not
archiving and not deletion**, and it must not be described as either: decision 3 above rejects
archiving, and it stays rejected. The precedent for the removal itself is al-hatorah, whose clone
came off the disk on 2026-08-11 after its tree moved into MAM-private.

**Removal is the lane's final proof rather than its tidy-up, and that is the reason to want it.**
Every reader of the sibling resolves it through `paths.require_sibling(...)`, which **fails loudly**
when the directory is absent. So after the clone is gone:

```bash
.venv/Scripts/python.exe py/main_test.py
```

plus this repo's oracle from the table under "Layer 2", and `ruff check py`. **Anything that now
fails names a reader Step 3 missed** — which is precisely the class of bug an empty `git status` in
the sibling could not have detected, because a call site still pointing there rewrites a file to
identical bytes. Run the **other two repos'** oracles as well, because two of them read a clone
that another lane removes: `holman-ketiv-qere`'s `main_estimate_uxlc_locations` reads the
UXLC-utils clone, so it would break at Phase 5's Step 6 rather than at its own phase; and
UXLC-utils' `main_map_changes_to_book_of_job` reads the book-of-job clone through
`uxlc_paths.book_of_job_dir()`, so it breaks at **Phase 4's** Step 6 unless Phase 4's Step 3
repointed it — which that phase's trap says it must.

**Before deleting, prove nothing is lost — four checks, all of which wlc-utils passed on
2026-08-22:** `HEAD` equals `origin/main`; `git status --porcelain` empty; `git stash list` empty;
`git worktree list` showing the one working tree only. Then, separately, **account for everything
untracked**, because that is the only content the GitHub copy does not hold:

```bash
git -C ../<repo> status --porcelain --ignored
```

**The known case is holman-ketiv-qere's `.novc/eml/`** — 13 raw messages that its oracle needs and
that no commit ever moved. Phase 3's Step 3 moves them; **Step 6 is where forgetting to would
become irreversible.** Check for a `.venv`, a `.novc/`, and any unpushed branch (`git -C ../<repo>
log --branches --not --remotes --oneline`) before removing.

**The removal is three acts, not one, and the order is forced.** The procedure has a name and two
precedents — al-hatorah's clone on 2026-08-11, and the frozen repos' move into `FrozenRepos`:

1. **Drop the repo's entry from `all-repos.code-workspace` FIRST, in the same commit as Step 5.**
   Not housekeeping: `repo_selection.load_workspace_repo_dirs` **raises `FileNotFoundError` on any
   workspace folder missing from disk, and it runs before every action**, so a clone deleted while
   its entry stands breaks `--run-black`, `--clean-worktrees` and the standards checks outright —
   all of them, not just the part that touched the removed repo. **Entry first, clone second, and
   never the other way round.**
2. **Delete the clone.**
3. **Record it in `MAM-basics/CLAUDE.md`, by EXTENDING the section that will already be there.**
   **The note goes here, not in the emptied repo's own `CLAUDE.md`** — that file is unreachable
   once the clone is gone, which is the whole point. This repo already carries the pattern in its
   §"There is no `wlc-koren-12th` repo", written because repeated sessions burned a turn on a
   directory that was not what it looked like; the concurrent session of 2026-08-22 added a second,
   §"There is no local `wlc-utils` clone either, and its stub set is frozen", beside it. **Extend
   that one or sit beside it — do not duplicate it, and state the workspace-entry mechanism in item
   1 only once**, wherever it already stands. Give the re-clone command per repo, and note that
   **`git clone --depth 1` is well under a megabyte and is all a stub publish needs** — neither
   `build --publish` nor `check` reads history.

**Regenerating the stubs needs that re-clone**, `build --publish` and the argument-less `check`
both resolving the sibling. **The occasion is far rarer than it looks, and knowing why is what
makes removal cheap**: a page created here *after* the move never had an old URL, so it earns no
stub and the set never grows. The one genuine occasion left is a page that existed at the flip
being renamed or deleted here.

**A repo in neither `GitRepos` nor `FrozenRepos` cannot be reached by any sweep** — a sweep
iterates the repos a workspace file lists and resolves them under `--repos-root`. So removal *is*
the freeze, structurally, exactly as the move into `FrozenRepos` is for the six repos already
there. Phase 6's item 6 should be answered in that light.

**Windows will not delete a directory a running process holds open**, so no shell may be `cd`'d
inside the clone when it goes. If the removal fails for that reason, it is a held handle rather
than a permissions problem.

---

## Preconditions

**1. The Python-evacuation programme must be complete.** **MET 2026-08-22** — all six repos hold
zero tracked `.py` and `PLAN-evacuate-python-programme.md`'s Status table reads DONE on every row.
Re-check that table rather than trusting this line.

**2. MAM-basics' Pages must be live.** **MET since 2026-08-13.** Check with
`gh run list --workflow pages.yml --limit 1 --repo bdenckla/MAM-basics` and by fetching
`bdenckla.github.io/MAM-basics/wlc/index.html`.

**3. No plan that regenerates any of the 1,178 arriving artifacts may be executed while this plan
runs.** This is the same contention wlc-utils' Precondition 1 named, and its own warning applies
verbatim: **a plan parked in a `doc/*.md` file is already harmless, and so is an open GitHub
issue — neither runs by itself.** So this precondition generates no work. **Do not turn it into an
investigation**; wlc-utils' Phase 0 records a session that read the equivalent clause as licence to
work out what a parked plan still owed and went three levels deep. What is dangerous is a
concurrent *execution*, because then a move bug and a page edit are indistinguishable.

Nothing currently parked touches these artifacts, checked 2026-08-22: `doc/scan-pages.md` is at
Phase 0 and concerns printed-edition page indexes, and
`doc/PLAN-two-accents-on-one-chanted-word.md` regenerates accgram pages under `gh-pages/wlc/`,
which is not an arriving subtree.

**4. MAM-private's melody-compiler work may run concurrently, and this is recorded so nobody
serializes on it needlessly.** Checked 2026-08-22 against
`MAM-private/al-hatorah/doc/PLAN-melody-compiler.md` at MAM-private `35b6cce`, and **re-checked
later the same day at `3d2ecf1`, after that work reached Phase 3 planning: still no import of any
MAM-basics module and no path reaching outside MAM-private.** That work writes
only `MAM-private/al-hatorah/py/melc/`, `py/main_melc.py`, `out/melc-*` and its own plan file; it
imports nothing from MAM-basics (`main_melc.py` and `py/melc/*` import only `aht`, `aht_phon`,
`mb_cmn` and `melc`); it runs on al-hatorah's own venv; and it publishes nothing, the tunes it
vendors being unlicensed and forbidden to reach a public repo. **No file, git index, venv or Pages
deploy is shared with this plan.** Two soft touchpoints, neither blocking: its Phase 3 may *read*
MAM-basics' `py/accgram/` for a `TROPE_GROUP` parse, which this plan does not edit; and its Phase 4
answers MAM-basics #3 and #4, which is tracker traffic rather than file contention.

**5. Another session may be live in MAM-basics, and that is not a precondition failure.** The
check that matters is not "was another session open" but "did another session's work interleave
with mine", and it is provable directly: `HEAD` at the start equals `HEAD` immediately before
committing; `git status --porcelain` empty at the start and holding only this phase's paths before
staging; and the push landing fast-forward with no `--force`.

---

## Phase 0 — Preflight: baselines, collision census, and the five decisions — DONE 2026-08-23

*No commit in any repo except this file.* Nothing is copied and nothing is deleted.

1. **Re-measure the Scale table**, every row, with the commands given beside it. Record the four
   repo heads. **A mismatch is a finding**: write it into the Scale section rather than silently
   updating the number.
2. **Re-run the collision census**, per Decision C, for all three repos. Expect: housekeeping files
   plus `gh-pages/index.html` for each; plus 39 `in/UXLC-39/*.xml` for UXLC-utils. **Confirm the 39
   are byte-identical** —

   ```bash
   git ls-files -s in/UXLC-39 | awk '{print $2, $4}' | sort > .novc/_a.txt
   ```

   and the same command with `git -C ../UXLC-utils`, then `diff`. Measured 2026-08-22: all 39
   identical, MAM-basics holding one extra file (`in/UXLC-39/_provenance.md`). **So those 39 are a
   duplicate to drop rather than a file to move**, and the same holds for ONE of the 2 under
   `out/UXLC-misc/` — `all_changes.json`, vendored here as `in/UXLC-misc/all_changes.json`. **Not
   for the other: `out/UXLC-misc/sanity_problems.json` is the 3-byte `[]`, and its blob match is
   a content coincidence with four unrelated empty-list files here** (`out/diff_mamws_mamgo*.json`
   and two under `out/mam-ws-bot/proto-misc/`) and with UXLC-utils' own
   `gh-pages/clc/Exodus-20-notes.json`. Nothing vendors it: `main_wlc_vendor_uxlc.py`'s `_sync`
   goes through `vendoring_sync.copy_by_intersection`, which copies only files already present in
   the destination, and `in/UXLC-misc/` holds `all_changes.json` alone. **So Phase 5 moves
   `sanity_problems.json` with the rest of `out/`, and the duplicates to drop are 40, not 41**
   — 39 XML at 10.8 MB plus `all_changes.json` at 1.4 MB, 12.2 MB in all. (This sentence said
   "the same holds for the 2" until Phase 0 ran, 2026-08-23.) Re-derive the blob-level census too,
   which is what found them:

   ```bash
   git ls-files -s | awk '{print $2}' | sort -u > .novc/_mbblobs.txt
   ```

   then intersect with the source repo's non-`gh-pages` blobs. Measured 2026-08-22: book-of-job 1
   (its Pages workflow), holman-ketiv-qere 0, UXLC-utils 41.
3. **Build the layer-4 URL list, in TWO parts.** Sweep every clone under
   `C:\Users\BenDe\GitRepos` and `C:\Users\BenDe\GitRepos\MAM-private` for
   `bdenckla.github.io/<repo>/`. **Everything that sweep returns is a citation Ben controls, and so
   is a repoint work item for that repo's lane, not evidence for a stub** — the sites known as of
   2026-08-22 are under "Layer 4" above, and the sweep is what makes the list current.
   **The part no sweep can answer is already answered — do not re-ask it.** Ben, 2026-08-22:
   assume URLs to all three are cited in places he cannot reach, posts and sent email among them.
   Carried-in decision 8, and layer 4 above has what follows from it.
4. **Record the baseline test count and lint state**: `py/main_test.py`'s summary line,
   `ruff check py`, `black --check py`. **The figure has moved twice in four days** — UXLC-utils'
   Phase 6 recorded 913 passed / 5 skipped on 2026-08-18, and the concurrent session measured
   **941 passed, 5 skipped, 59 subtests** on 2026-08-22 after adding
   `py/tests/test_wlc_redirect_manifest.py`. Re-measure; the point of the baseline is that Phase 2
   and each lane's Step 3 can say what they changed.
5. **Put the five decisions to Ben**, one at a time, in plain prose — not as a batch and not
   through a multiple-choice picker. Write each answer and its date into the Decisions section
   above.

**What is NOT expected to change in this phase:** any file in any of the four repos except this
plan file. If `git status` shows anything else, that is a finding.

### Execution record — Phase 0, 2026-08-23

Began at MAM-basics `d095871`, book-of-job `3f096b9`, holman-ketiv-qere `5f419ef`, UXLC-utils
`b7b4eb9` — the heads the chip named — with all four at `git status --porcelain` empty, all four
on `main` with nothing unpushed, and MAM-basics confirmed the main clone rather than a worktree
(`git rev-parse --git-common-dir` is `.git`). **Nothing was copied, nothing was deleted, and no
repo but MAM-basics was written to**; every command below is read-only outside `.novc/`. The
working files are in `.novc\three-repos-phase0\` (gitignored), the flat listings and blob sets the
census was taken from.

**Items 1 to 4 were done in one sitting and written back first (`0decb3f`); item 5, the five
decisions, was put to Ben one at a time afterwards**, each answer recorded under "Decisions this
plan needs from Ben" and committed as it arrived: A in `09498cd`, B in `c2d8fb1` and its docx
sub-question in `5421e49`, C in `3f9eff4`, D in `0a1ccb5`, E in the commit that closed the phase.
Seven commits in all, every one to this file alone; `HEAD` before each equalled the previous
commit, `git status` held this file only, and every push was a fast-forward.

**Item 5 — the five answers, in one place.** Subtrees `gh-pages/book-of-job/`, `gh-pages/holman/`
and `gh-pages/uxlc/` (A). No `LICENSE` for the emptied repos (B); and Holman's docx does not move
— it is deleted from holman-ketiv-qere at Phase 3's Step 5 and the extracted data becomes source
data with its origin documented, which retires the extraction half of that repo's first oracle
command and takes away Phase 1's one owed `.gitattributes` edit (B's sub-question). Same relative
path for the non-`gh-pages` trees, with `data/` at `data/` and `halve.md` under
`.claude-disabled/` (C). `py_ac_loc/` dropped, never copied (D). `UXLC-utils.code-workspace` and
`shared-with-codex-index-leningrad.md` deleted, the two meteg-marks files landing at `out/` (E).
**Two of the five answers were not among the options put** — A's mixed spelling and B's
sub-question's fourth option — which is the case for putting a decision rather than recommending
one and proceeding. **Two questions were parked for later phases rather than asked**, each written
where its phase will find it: `persist_verify_summary`'s in-place rewrite of `table_data.json` once
that file is source data (Phase 3's Step 3, under Decision B's sub-question), and whether
codex-index-leningrad's sparse copy survives at all (Phase 5's Step 3, under Decision E and trap
4).

**What the next phase now knows that this file did not say on 2026-08-22.** Phase 1 owes no
edit: it proves its two no-ops on one file each, and commits only its record. Phase 3 moves 47
files outside `gh-pages/`, not 48, deletes one file it never copied, and rewrites rather than
regenerates its table. Phase 4 moves 9 files outside `gh-pages/`, not 85, and expects the
mark-order check to drop from 509 files to 460. Phase 5 moves `sanity_problems.json` with `out/`,
lands `data/` at `data/`, and carries a third pair into its trap-3 collapse question.

**Item 1 — the Scale table reproduces in its first six columns and not in its last two.** Every
tracked-file count, total size, `gh-pages/` count, `gh-pages/` size and HTML-page count came back
exactly as written, for all three sources and for MAM-basics. The "outside `gh-pages/`" column
was wrong by 2 files for holman-ketiv-qere, and by 1 file and 0.2 MB for UXLC-utils — the three
quoted, Hebrew-named `gh-pages/` paths, leaked past a naive `grep -v '^gh-pages/'` into the
outside count. The corrected table, the cause, and the null-delimited command are under "Scale";
the same figures were corrected in place in Decision C, Phase 3 and Phase 5. **The after-all-lanes
projection was also off** — "about 3,900 files / 380 MB" does not follow from the table's own
figures, which give about 4,100 / 430 before anything is dropped; corrected in place, with the
derivation. Neither correction changes any decision.

**Item 2 — the collision census reproduces exactly, with one refinement that changes what Phase
5 does to one file.** Path collisions: book-of-job `.gitattributes`, `.gitignore`, `CLAUDE.md`,
`README.md` and `gh-pages/index.html`; holman-ketiv-qere and UXLC-utils those plus
`.github/workflows/pages.yml`; and for UXLC-utils the 39 `in/UXLC-39/*.xml`. **book-of-job's
workflow does not collide by path because it is `.github/workflows/static.yml`**, a different
name for the same 687-byte blob as MAM-basics' `pages.yml` — which is why it is the one
book-of-job blob in the blob census and is absent from the path census. The 39 XML are 39 of 39
byte-identical, MAM-basics holding `in/UXLC-39/_provenance.md` besides. The blob census: book-of-job
1, holman-ketiv-qere 0, UXLC-utils 41. **The refinement: the 41st is `out/UXLC-misc/sanity_problems.json`,
a 3-byte `[]` whose match with MAM-basics is a content coincidence, not a vendored copy** —
`main_wlc_vendor_uxlc.py` copies by intersection with what `in/UXLC-misc/` already holds, which is
`all_changes.json` alone. So 40 blobs are duplicates to drop (12.2 MB) and that one file moves
with `out/`. Written into item 2 above, into "The organizing idea", and into Phase 5's trap 3.

**Item 3 — the layer-4 sweep returns the list the section already has, and nothing of a new
kind.** Citations of `bdenckla.github.io/{book-of-job,holman-ketiv-qere,UXLC-utils}` across the
19 clones (MAM-private counted once; its three subtrees are not clones): mgketer's seven in
`py/python_modules/diff_crops.py` and seven in `out-reports/by-book/D3-Job/suppressed.html`,
`document-index/README.md`'s one, `_WLCAU` at `py/author_boj/job5_orphan_qere_points.py:81` and
its two emitted copies in book-of-job's `gh-pages/jobn/job5_orphan_qere_points.html`, the three
`py/*_paths.py` docstrings, book-of-job's `README.md` (one line, two URLs) and UXLC-utils'
`README.md` (four URLs, lines 54–57) — plus this plan and
`doc/PLAN-evacuate-python-from-book-of-job.md`, which describe the URLs. **holman-ketiv-qere's
URL is cited nowhere but its own path module's docstring.** Over HTTP the same day: the `_WLCAU`
URL answers 404 and `bdenckla.github.io/MAM-basics/wlc/wlc-a-notes/` answers 200, as layer 4 says;
all three old sites still answer 200 at their roots. The name sweep confirmed the eight zero-hit
clones as listed, codex-index-leningrad's four files (Phase 5's trap 4) and github-misc's three
(Phase 6's items 3 and 4: `SKILL.md`'s description line names book-of-job and UXLC-utils,
`terminology.md` names UXLC-utils at `:123` and `:144`), and added three prose-only mgketer files to
the list under layer 4. The second part of this item was not put to Ben — decision 8 stands.

**Item 4 — the baseline is exactly the figure carried.** `py/main_test.py`: **941 passed, 5
skipped, 59 subtests passed** in 158 s. `ruff check py`: clean. `black --check py`: clean, **1,134
files**, black 26.5.1. And one figure the plan did not carry, added because Decision D moves it:
`py/check_mark_order.py` reports **509 files**, 49 of them book-of-job's `py_ac_loc/*.json`.

**Preconditions, re-checked.** 1: the programme's Status table reads DONE on all five rows and
WRITTEN on this plan's. 2: `gh run list --workflow pages.yml --limit 1 --repo bdenckla/MAM-basics`
shows success for the `d095871` push, and `bdenckla.github.io/MAM-basics/wlc/index.html` answers
200. 5: `HEAD` at start `d095871`, equal to `HEAD` before each commit below.

**Banked for later phases, while cheap.** Both unsynced live-plus-tracked pairs are byte-identical
today — `~\.claude\CLAUDE.md` against `github-misc\dot-claude\CLAUDE.md`, and the
`hebrew-prose` skill against its tracked copy — the state Phase 6's items 3 and 4 need before they
add to either. `all-repos.code-workspace` lists **19** folders, the three repos among them and
`../wlc-utils` not, so Phase 6's item 7 starts from 19 and ends at 16 as written.
`in/repo_maintenance_policy.json`'s `frozen_repos` holds six entries, none of them wlc-utils or any
of the three (item 6's premise). `in/vendoring_policy.json` has no entry for any of the three, but
**its top-level `comment` says `main_lenin_vendor_uxlc.py` refreshes codex-index-leningrad "from the
sibling UXLC-utils"** — a clause Phase 5's repoint falsifies, so Phase 6's item 5 owes that
sentence an edit even though no entry changes.

#### Findings

**1. The "outside `gh-pages/`" column had sprung the plan's own quoted-path trap.** The plan warns
about it for the HTML-page count and had used the naive form for the column beside it. Three
files, 0.14 MB — nothing turns on it, except that a Phase 5 session counting 596 against a plan
saying 597 would otherwise have spent a turn on the difference. The `-z` form is now given for
that column too.

**2. One of the 41 "duplicates" is a file that must move.** `sanity_problems.json` is the
currently-empty output of a UXLC-utils oracle step; dropping it on the strength of a 3-byte blob
coincidence would have deleted an artifact. A blob census finds content identity and says nothing
about provenance; the vendoring script's `copy_by_intersection` is what settled which of the 41
are copies.

**3. Decision D is narrower than written.** book-of-job's `py_ac_loc/` is, to the byte, a
snapshot of codex-index-aleppo at 2026-02-19 plus two breadcrumbs: 26 files one blob with that
repo today, 48 one blob with its `0be4d38`/`295829e`, and `image-sources.md` deliberately retired
there. "Partly duplicates" was the right description of the trees and the wrong description of the
history. The recommendation under Decision D changed from "put the three options" to "drop,
unless Ben wants the snapshot kept", and the one lint that reads it — `check_mark_order.py`, 509
files → 460 — is named so Phase 4 expects the change.

---

## Phase 1 — `.gitattributes` merge in MAM-basics

*In MAM-basics only.* One commit. **Blocking on every Land step**, for the reason layer 1 gives:
`git add` applies `.gitattributes` at add time, so a rule that differs between source and
destination changes the incoming blob and destroys the byte-identity evidence.

The four files as of 2026-08-22 — re-read each rather than trusting this table:

| Repo | rules beyond `* text=auto eol=lf` |
|---|---|
| MAM-basics | `*.csv text eol=crlf`; `*.png`, `*.jpg`, `*.pdf`, `*.woff2` binary |
| book-of-job | `*.png`, `*.woff2` binary — a subset of MAM-basics' |
| holman-ketiv-qere | `*.docx`, `*.png`, `*.woff2` binary — **`*.docx` is not in MAM-basics'** |
| UXLC-utils | none at all |

**The one edit this phase owed was `*.docx binary` in MAM-basics**, ahead of holman-ketiv-qere's
20.6 MB review document arriving — **and it is no longer owed: Decision B's sub-question was
answered on 2026-08-23, the docx does not move, and it is the only `.docx` in any of the three
repos.** So this phase makes no edit at all unless one of the two checks below fails; it is a
verification phase, and its commit, if any, is this file's record. (Until that day this
paragraph said to copy the comment convention already in MAM-basics' `.gitattributes`, which
explains why the binary rules were copied from wlc-utils ahead of that corpus — still the
convention to follow if a rule ever does turn out to be needed.)

**Two interactions to check rather than assume, and both are expected to be no-ops:**

- **UXLC-utils declares no binary rules**, yet holds 80 PNGs and 3 JPGs. `text=auto` auto-detects
  binary content, so those blobs should be stored unconverted in both repos and the explicit
  `binary` rule should change nothing. **Prove it on one file** before the copy rather than after.
- **MAM-basics' `*.csv text eol=crlf` meets UXLC-utils' 6 tracked CSVs.** `text eol=crlf`
  normalizes to LF *in storage* and checks out CRLF, and UXLC-utils stores LF, so the blob should
  be unchanged and only the working-tree copy differs. **Prove it on one file**, and note the
  consequence for anyone reading the CSV afterwards.

**Verify:** `git ls-files --eol` over a sample of each incoming type; `py/main_test.py` unchanged;
nothing in `git status` but `.gitattributes`.

---

## Phase 2 — Generalize the redirect-stub generator to a table of four

*In MAM-basics only.* Nothing is published; the build writes to a gitignored scratch directory by
default. **This phase can run before any tree has landed**, and doing so front-loads the risk: the
wlc-utils stub set is a live regression oracle for the generalization, and a generalized generator
whose wlc rows still produce the committed 155 files is proven before it is trusted with anything
new.

**What exists today**, re-measured by the 2026-08-22 review at `59142cf`, after the freeze and the
docstring corrections had landed: `py/main_wlc_redirect_stubs.py` (117 lines) plus
`py/wlc_redirect/` — `stubs.py` (391), `build.py` (53), `check.py` (54), 615 lines in total, and
`py/tests/test_wlc_redirect_manifest.py` (53). The wlc-specific facts are **six module-level
constants in `stubs.py`** — `NEW_SITE`, `OLD_PATH_PREFIX`, `_CLONE_URL`, `_MANIFEST_PATH`,
`_PAGES_PREFIX` and the repo name inside `wlc_utils_pages_dir` — plus `default_out_dir`'s
`"wlc-redirect-stubs"`, the `wlcPrefix`/`wlcPath`/`wlcRest` identifiers in `_NOT_FOUND_TEMPLATE`,
the `GENERATED by py/main_wlc_redirect_stubs.py` comment in both templates, the phrase "frozen
wlc-utils URL" in two of `check_problems`' messages, and the prose in the docstrings and the two
`add_args` help strings. Find them by name, not by line number. (This paragraph listed 517 lines
and four constants until the review; `_CLONE_URL` and `_MANIFEST_PATH` arrived with the freeze in
`e761cef`.)

**The generalization is a record per evacuated repo — one row at this phase, four by the end of
Phase 5**: the source repo name, the `gh-pages/` subtree name under MAM-basics (Decision A), the
old URL prefix, the manifest path, and **the clone URL** — the last because a resolver that fails
once the clone is gone should carry its own fix, per Step 6. **Only the wlc row exists at this
phase.** A row needs its frozen manifest, and a missing manifest fails rather than skips (by
design — see the test's docstring), so each of the other three rows is added in its own lane's
Step 4, in the MAM-basics commit that captures its manifest. A table that named all four at Phase
2 would fail the suite on three of them from the day it landed.

### The page set is FROZEN, not derived — and this paragraph corrects the rest of this plan

**READ THE COMMITTED `py/wlc_redirect/` BEFORE GENERALIZING ANYTHING. Do not trust this file's
description of it.** An earlier draft of this phase, written 2026-08-22, said the set was derived
from the live `git ls-files gh-pages/<subtree>` and called that derivation "the design's whole
point", which "must survive". **That was wrong, and generalizing it would have propagated a defect
to four repos.**

**Ben settled it on 2026-08-22**, the same day this plan was written and while it was being
written: a session working concurrently in this repo replaced the derivation with a frozen manifest
at `in/wlc_redirect_pages.json`, holding the 154 paths wlc-utils published, captured at the
2026-08-17 flip. That file's own `comment` field is the statement of record — read it first — and
what it says is:

**A stub answers an OLD URL. The set can only shrink, never grow.** A page published under
`gh-pages/wlc/` *after* the move never had a `bdenckla.github.io/wlc-utils/` URL, so it must not
get a stub; a live derivation gives it one. The defect the derivation actually caused was the
mirror image and is what surfaced it: **every new page here looked like a missing stub.**

**Four consequences for this plan, which supersede what its other sections say:**

1. **Each repo needs its own frozen manifest, captured at its Step 4** — from the source repo's
   `gh-pages/` tree as it stands at the flip, which is the last moment the old published set is
   knowable. Capture it in the same commit as the flip. **After that the manifest is append-never**;
   removing an entry is the only edit it can take, and only when the page it names stops being
   published here.
2. **`check`'s failure modes change shape**, and the concurrent session's rewrite is the model: a
   frozen URL with no stub (a cited URL that would 404), a stub answering no frozen URL (it stands
   in for nothing), and a frozen URL whose page is no longer published under the subtree (its stub
   redirects to a page that is not there). **The third has no counterpart in the derived design**
   and is the one worth having. A fourth correspondence — a page published here that no stub names
   — is **deliberately not checked**, that being the never-event this whole section is about;
   `check_problems`' docstring states all four, including the one it does not enforce.

   **The one function became two, and the generalization should keep both names**:
   `redirected_pages(repo_root)` reads the frozen manifest, and `published_pages(repo_root)` is the
   live `git ls-files gh-pages/<subtree>`, used **only** for that third failure mode.

3. **Each repo needs the third failure mode hoisted into the test suite**, as
   `py/tests/test_wlc_redirect_manifest.py` now does for wlc-utils — or, better here, as one
   generalized test parametrized over the table's rows, **which means one row at this phase and a
   row added per lane at Step 4**, for the reason given above: a row without a committed manifest
   fails, and three of the four manifests do not exist until their flips. **The reason is Step
   6**: that check is the
   only part of the lint needing no stub tree, and therefore **the only part that still runs once
   the clone is gone.** Everything else in `check` goes dark at Step 6, so without this the frozen
   manifest silently stops being verified at the exact moment nobody can look.
4. **What is still derived is the *destination*, not the set.** The path below the manifest entry
   remains both the old path and the new suffix, so the rewrite stays a pure prefix rewrite and
   still needs no mapping table. **That much of the old paragraph was right** and is why the four
   rows above are still the whole of the per-repo configuration.

**The concurrent work landed** — `e761cef` (the freeze), `f762d2b` (what a stub is for),
`d70e14c` (the repoint) and `abf32c2` (the sweep's negative result), confirmed by the 2026-08-22
review with `git log --oneline -- py/wlc_redirect in/wlc_redirect_pages.json`. Re-run that command
anyway; do not generalize the derived design in any case.

### Renaming a frozen page: DETECTED by the freeze, and repairable two ways of three

**An earlier draft of this section was wrong and the correction is the point of it.** It said a
rename "silently sends its old URL to a MAM-basics 404". **That was true of the derived design and
is false as of the freeze**, and the difference is exactly what freezing bought. In the derived
design the expected set moved with the site, so a rename changed both sides together and nothing
here could notice; only `check` against a clone could, which nothing scheduled and which no clone
now exists for. **Frozen, the manifest does not move**, so a rename is a **detected event on every
ordinary suite run, needing no clone anywhere.**

Verified 2026-08-22 by reading `py/tests/test_wlc_redirect_manifest.py`: it compares
`stubs.redirected_pages` against `set(stubs.published_pages)`, both resolved from
`paths.repo_root()`, and resolves no sibling at all. The concurrent session demonstrated it with a
real `git mv` of `gh-pages/wlc/accgram/goerwitz.html`, which fails the suite naming the page, and
renamed it back.

**What survives is about repair, not detection**, and it is narrow. `target_url` is a pure prefix
rewrite of the stub's own path, so once the test fires there are exactly two ways out:

1. **Republish the page at its old path** — rename it back.
2. **Drop the URL from the manifest and delete its stub**, letting the old citation fall to the
   `404.html` catch-all.

**There is no third way — no way to say "the old URL X now lives at Y"** — and an optional explicit
target in the manifest is the whole of what would add it.

**Ben's decision, 2026-08-22: skip it. Recorded as considered and declined, not pending, and it is
carried-in decision 7 above.** **It holds for this plan's 272 frozen URLs (175 + 6 + 91) as it does
for wlc-utils' 154, and it was made knowing the cited set is unenumerable** — Ben, 2026-08-22: *"I
was perfectly aware of how widespread the need for stubs is when I made that decision."* **So do not
reopen it on the strength of decision 8**, which states that same fact and was not new information
to him.

**What makes the deferral safe**: if a cited page is ever renamed, the failing test names it, and
adding the branch **then** is the same one-line change it is now. Nothing is foreclosed by waiting,
and that holds however many citations exist.

**Do not restate this decision as resting on the citations being few.** Two sessions summarized it
that way on 2026-08-22 and neither had it from Ben; the enumerable list — for wlc-utils, five
citations of `accgram/goerwitz.html` in tanach.us's published change list, named in
`py/wlc_redirect/stubs.py`'s docstring — is the part of the cited set that can be *written down*,
not an estimate of its size.

**That list is shorter than an earlier draft of this paragraph said**, which also counted four CLC
deep links and four `document-index/README.md` paths. Those are Ben's own and were repointed rather
than redirected on 2026-08-22; see layer 4. **Only the citations he cannot reach bear on this
decision**, because a citation he can edit is not answered by a stub either way.

**One consequence for the lane, and it runs the other way from how this paragraph first put it:
option 2 is never cheap here.** For wlc-utils, "drop the URL" can consult the one named citation
in `stubs.py`'s docstring. For these three repos there is nothing to consult — decision 8 says the
URLs are cited and that there is no list, and Step 4 records exactly that and nothing more. So when
the manifest test fires, option 2 is always dropping a URL assumed cited, which weighs the choice
toward option 1, republishing at the old path. (Until the 2026-08-22 review this paragraph said
Step 4's record "is what makes option 2 cheap later" — a record that, for these repos, cannot
exist.)

**What `404.html` does and does not lower.** With JavaScript on, it strips the old prefix and
prepends the new site, so **an old path with no stub of its own still forwards** — to a browser.
That is the whole of it. It carries no meta refresh, because its target is computed from the path,
so **with JavaScript off a path with no stub forwards nowhere**; and GitHub Pages serves it with
HTTP 404 whatever it then does, so to anything that reads the status — a search engine, a link
checker, tanach.us's readers' tooling — an un-stubbed path is a dead URL. The per-page stub is the
only thing that answers 200, and the only thing that forwards a no-JavaScript reader at all. (This
paragraph called the stubs "belt and braces over a catch-all that already works" until the
2026-08-22 review; the Requirements bullet below it had said the opposite all along.)

**Requirements the existing design imposes, none of which this phase may quietly drop:**

- **Each stub carries its target three times and the three are not redundant.** The
  `<link rel="canonical">` names the current copy for a search engine; the
  `<meta http-equiv="refresh">` is the no-JavaScript path and takes a fixed URL; only the
  `<script>` can re-append `location.search` and `location.hash`, because a fragment is never sent
  to the server. **State the JavaScript-off degradation in the docstring** — a deep link lands on
  the right page at its top rather than at its anchor — rather than leaving it to be discovered.
- **`404.html` per repo**, reading `location.pathname`, stripping the old prefix, prepending the
  new site, re-appending search and hash. GitHub Pages serves it with an HTTP 404 status whatever
  it then does, which is precisely why the per-page stubs exist: a cited URL has to answer 200.
- **A directory URL is covered only where the directory holds an `index.html`**, which is correct
  rather than accidental — and is why `gh-pages/wlc/accgram/` gets no stub today (issue #230).
- **`check` is a mechanical lint over generated text**, the second of the two test shapes
  MAM-basics' `CLAUDE.md` allows. Keep it that shape; do not add example-based assertions.
- **`test_entry_point_subcommands.py` enforces the docstring's `Subcommands:` block**, with name
  and description on **separate** lines — the one-line form reads to its `fullmatch` as an empty
  block.

**And one requirement the existing design never met, because wlc-utils' 154 names never needed
it: `target_url` must percent-encode the path.** Found by the 2026-08-22 review. `target_url` is
`NEW_SITE + page_path`, raw. holman-ketiv-qere's two JC3 pages carry `#`, spaces and ז in their
names, and a raw `#` in the meta refresh URL or in `location.replace(...)` starts a fragment, so
the stub would send the reader to a path truncated at the `#` — a 404. Verified over HTTP that
day: the old URL with `%2319-%D7%96` answers 200, the same URL with a raw `#` answers 404.
`check`'s `_TARGET_RE` also stops at whitespace, so a raw space would make `check` mis-read the
stub's own target. **`urllib.parse.quote(page_path, safe="/")` inside `target_url` fixes both at
once**, since `check` compares against `target_url`. The `<title>` may keep the raw path; it is
text, not a URL. book-of-job's 175 and UXLC-utils' 91 page names are plain ASCII, so the pilot
lane's two pages are the whole of this — which is one more reason the pilot is the right first
lane, and Step 4's verify fetches one of them.

**Naming.** `py/main_wlc_redirect_stubs.py` and `py/wlc_redirect/` are now misnamed for a
four-repo tool. **Renaming them is the honest move and it is not free**: the entry point is cited
by name in wlc-utils' `CLAUDE.md`, in `PLAN-evacuate-the-rest-of-wlc-utils.md`'s Phases 8 to 11,
and in `py/wlc_redirect/stubs.py`'s own docstring. **DECIDED — Ben, 2026-08-23: rename to
`py/main_redirect_stubs.py` and `py/redirect_stubs/`**, and repoint wlc-utils' `CLAUDE.md` in the
same commit; leave the completed plan's execution records as written, since they describe what was
true when they ran. The decision is recorded under Decision A, where it was put to him; it is not
a Phase 0 question any more.

**The rename and the byte-identity check below cannot both hold at once, so the order is forced:
generalize first, prove byte-identity, THEN rename.** Every one of wlc-utils' 155 committed files
carries `<!-- GENERATED by py/main_wlc_redirect_stubs.py -- do not edit; run that program again. -->`,
and `404.html` also carries the `wlcPrefix`/`wlcPath`/`wlcRest` identifiers. A generalization
that renames the entry point, or those identifiers, or reworks the "frozen wlc-utils URL" message
text, changes the rendered output, and the byte-identity check is then measuring the rename
rather than the generalization. So: generalize with the template text unchanged, run the check,
and only then rename. (Added by the 2026-08-22 review; this phase had listed both as if they were
independent.)

**The rename then leaves the 155 committed stubs naming a retired file, and that is DECIDED too —
Ben, 2026-08-23: republish them once.** After the rename, every committed file in wlc-utils names
a generator that no longer exists at that path, under a comment that tells the reader to run it.
The alternative, leaving them — the stubs work, the comment misdirects — was considered and
declined. So this phase ends with `build --publish` into the clone it has on disk anyway, and one
commit in wlc-utils **whose diff is exactly one comment line in each of 155 files; anything beyond
that is a finding**, which is also a second proof that the generalization changed nothing else.
The plan's "publishing is a never-event" is about needing to, and a one-line diff over files
already proven identical is the cheapest publish there will ever be. The decision is recorded
under Decision A.

**Verify — and there is no `../wlc-utils` to verify against, so the first step is a clone.** The
wlc-utils clone came off the disk on 2026-08-22 (MAM-basics' `CLAUDE.md` §"There is no local
`wlc-utils` clone either, and its stub set is frozen"). So:

```powershell
git clone --depth 1 https://github.com/bdenckla/wlc-utils.git C:\Users\BenDe\GitRepos\wlc-utils
```

**Do not re-add `../wlc-utils` to `all-repos.code-workspace`** — the entry stays out, only the
directory comes and goes — **and remove the clone again when this phase closes**, per Step 6's
checks (nothing unpushed, nothing untracked). **The phase's order in that clone is: byte-identity
check, then the rename, then the one-time republish decided above — `build --publish`, one commit,
pushed — then the removal.** Then: `build --out <scratch>` for the wlc row
produces exactly the 155 files committed in wlc-utils, byte-identical — `git diff --no-index`
between the scratch tree and `C:\Users\BenDe\GitRepos\wlc-utils\gh-pages` is the check, and it is
expected to be empty **before the rename**; `check` passes against that committed tree; a row
whose manifest is not committed makes `build` and `check` **raise on the missing file rather than
run empty** — that is the frozen design's behavior, and it is what to verify, by pointing the tool
at such a row; `py/main_test.py` green; `black` and `ruff` clean on the files touched. (This
paragraph said "`build` for a repo whose tree has not landed produces an empty set and `check`
says so rather than passing vacuously" until the 2026-08-22 review — a leftover of the derived
design, under which an un-landed tree yielded an empty `git ls-files`.)

---

## Phase 3 — holman-ketiv-qere, the pilot lane; plus the generated landing page

*The per-repo lane, run for `C:\Users\BenDe\GitRepos\holman-ketiv-qere`.*

**Why this repo goes first.** It has the **smallest stub set of the three by a wide margin — 6
pages** — and the smallest non-`gh-pages` tail at 48 files, while still being a real move at 300
files and 35.5 MB. So it exercises every step of the lane at the lowest cost, which is the same
reasoning the Python programme used in putting UXLC-utils and then holman-ketiv-qere ahead of
book-of-job.

**What this repo holds outside `gh-pages/`**, surveyed 2026-08-22 — 48 files, 22.6 MB, being the
43 itemized below plus `.gitattributes`, `.github/workflows/pages.yml`, `.gitignore`, `CLAUDE.md`
and `README.md` (the heading said 50 until Phase 0's re-measure of 2026-08-23 — see the note under
the Scale table; the two JC3 pages had been counted as outside):

| path | files | MB | what it holds |
|---|---|---|---|
| `Review of Qere and Kethib readings in the Aleppo and Leningrad.docx` | 1 | **20.6** | Holman's review — the source of the 77-row table and of the 154 images under `gh-pages/img/`. **90% of the bytes.** **DOES NOT MOVE — Decision B's sub-question, answered 2026-08-23: deleted at Step 5, never copied; the extracted data becomes the source at Step 3.** |
| `emails/` | 26 | 0.056 | An address-free derivative of Holman's 13 correction emails, a `.txt` body and `.json` metadata per message. The ingest redacts as it reads, because the repo is public; the raw `.eml` stay in the gitignored `.novc/eml/`. |
| `docs-not-served/` | 4 | 0.272 | `introduction.md`, `table_data.json` (77 rows) and `uxlc_corrections.json`, all generated; `table_data_fields.md` is hand-authored and documents the third. |
| `out/` | 2 | 1.611 | The two phenomenon searches. |
| `doc/` | 2 | 0.021 | Findings prose. **No accessor and no reader in MAM-basics.** |
| `data/` | 2 | 0.018 | Written by `main_estimate_uxlc_locations` from the UXLC-utils clone; tracked so a fresh clone can render without ~11 MB of UXLC XML. |
| `assets/` | 4 | 0.016 | Authored CSS and JavaScript the render steps copy into `gh-pages/`. **Input to a generator, not output** — do not treat as an artifact. |
| `io/` | 1 | 0.007 | `table_row_github_issues.json`, the per-row issue state and labels. |
| `.claude/` | 1 | 0.0004 | `.claude/commands/halve.md`, a one-off slash command. **A dot-directory, so a glob that skips the six housekeeping files still misses it.** |

**Three traps specific to this repo:**

1. **The docx has spaces in its name and `git ls-files` does NOT quote it**, being pure ASCII. The
   two paths this repo *does* get quoted are both under `gh-pages/` and are quoted for a Hebrew ז
   rather than for their spaces — `"gh-pages/JC3 The Biblical Text in the JC Edition #19-\327\226.html"`
   and its ` - English` sibling. **So a census written from `git ls-files | grep '"'` finds the two
   pages and misses the 20.6 MB document.** Use `-z`. **Those same two pages are also the only
   pages in any of the three repos whose stub target needs percent-encoding** — the `#` in their
   names starts a fragment in a raw URL — which is Phase 2's encoding requirement and Step 4's
   extra verify; nothing links to them from the rest of the site, so the stub is the only way a
   reader of the old URL reaches them.
2. **`hkq_paths.mam_qere_words_path()` must not be repointed** — it already returns MAM-basics'
   own `out/`. Named again here because Step 3 is where it would be swept.
3. **`py/hkq_cmn/table_row_github_issues.py`'s `REPO_NAME` is a tracker name, not a path.**
   MAM-basics' `CLAUDE.md` §"Five issue trackers" names this module and `py/py_render/rt_issue_tags.py`
   as the pair that renders issue references as *data* about the review, and says prefixing or
   renaming them corrupts the rendered table.

**The docx is this phase's one deletion without a copy, and cutting the cord to it is this
phase's largest Step 3 change.** Decision B's sub-question, answered by Ben on 2026-08-23, lists
what that entails — the extraction half of `main_extract_docx_and_render_table.py` retires and
the script is renamed, `table_data.json`, `introduction.md` and `gh-pages/img/` become source data
with a `_provenance.md` beside them, `persist_verify_summary`'s in-place rewrite of the JSON is a
design point to settle, and Step 5 deletes the document from the tree while
`bdenckla/holman-ketiv-qere`'s history keeps it. Read that list before starting Step 3; it is kept
there rather than here so that the decision and its consequences stay together.

**The mailbox is this phase's one untracked move.** `main_ingest_uxlc_emails` reads
`holman-ketiv-qere/.novc/eml/` through `hkq_paths.eml_dir()`. No commit moves an untracked
directory, so Step 3 must move those 13 messages by hand into MAM-basics' `.novc/` and repoint the
accessor, or the oracle stops running the moment Step 5 empties the repo. **Verify the ingest
reproduces the 26 tracked files in `emails/` byte-identically after the move**, which is what
proves the redaction ran the same way. **Step 6 is where forgetting this becomes irreversible** —
the mailbox is untracked, so the GitHub copy does not hold it and removing the clone destroys the
only copy. Account for it explicitly with `git -C ../holman-ketiv-qere status --porcelain
--ignored` before removing anything.

### The generated landing page rides with this phase's Land step

**Ben's decision, 2026-08-22**, recorded in the programme under "Decision — the site's landing
page becomes generated". It belongs here because a generator emitting a fixed one-item list is dead
weight, and the shape of the thing is decidable only once there is more than one subtree to list.

`gh-pages/index.html` today opens with `Hand-written, unlike the pages below wlc/, which are
generated. No program writes this file.` — read it with `head -2 gh-pages/index.html`. That comment
is what the generator replaces, with the `Do not edit by hand.` breadcrumb from
`mb_cmn/provenance.py`'s `generated_html_comment` that every other generated page here carries.

- **A subcommand under an existing `py/main_*.py`, never a new entry point**, and no `sys.path`
  prelude. `main_authored.py` already hosts `gen-mam-parsed-docs`, which writes a sibling's
  `index.html`, so it is the obvious host; the session writing the generator picks.
- **Derive the subtree list from the site**, one entry per `gh-pages/<subtree>/index.html`, the way
  the stub generator derives its stub set. **The descriptions cannot be derived and stay authored**
  — the present page's wlc entry is the register to match, and a subtree with no description is a
  gap to fill rather than a link to emit bare.
- **Reproduce the current page's shape otherwise**: no stylesheet, the same `<ul>` of one-line
  entries, the same closing pointer at the `README`. **So the first regeneration's diff should be
  the breadcrumb comment and the added entry and nothing else**; anything further is a finding, not
  a tidy-up.
- **`gh-pages/wlc/index.html` stays hand-written and is not in scope.** It arrived verbatim from
  `bdenckla/wlc-utils` as that repo's own landing page.
- **`DATA-LICENSES.md`'s `gh-pages/index.html` row expires.** It describes the page as "a
  hand-written list of one item, pointing at `wlc/`", and both halves stop being true. The licence
  itself does not change. Fix it in this phase's Licence step.
- **The page joins the artifact oracle.** Once generated, "regenerating the tracked artifacts
  byte-identically is the test" reaches it, and this phase must name the command that does so.

---

## Phase 4 — book-of-job

*The per-repo lane, run for `C:\Users\BenDe\GitRepos\book-of-job`.*

**The largest move of the three** — 694 files and 65.2 MB under `gh-pages/`, 175 stubs — and the
simplest data tail once Decision D is answered.

**What it holds outside `gh-pages/`**, surveyed 2026-08-22 — 90 files, 8.1 MB:

| path | files | MB | what it holds |
|---|---|---|---|
| `py_ac_loc/` | 76 | **7.8** | Aleppo Codex data despite the `py_` prefix — **no Python in it**. **Decision D: DROPPED, Ben, 2026-08-23 — deleted at Step 5, never copied.** |
| `out/` | 7 | 0.329 | Generated JSON; six regenerate with the site, and `cam1753-crops.json` is hand-made crop coordinates. |
| `doc/` | 2 | 0.003 | `opening-html-files.md` and `reading-mam-simple.md` — procedures about *reading* what is here. The seven about how it is made already moved, and MAM-basics' `CLAUDE.md` has a section on them. |

**515 of the 694 `gh-pages/` files are PNGs, and 518 of that repo's 701 artifacts are written by no
program.** So **layer 1 is the only evidence for the great majority of this move**, and layer 2
reaches 183 files. Say which is which in the execution record; an empty `git status` over files
nothing writes is not a claim.

**`boj_paths.py`'s `DATA_REPO_NAME` is declared and never referenced**, `boj_data_root()`
hardcoding the literal instead. So Step 3 deletes a dead constant here as well as collapsing the
accessor, and a grep for the constant will not find the resolution.

**Only three subtrees compose off `boj_data_root()`** — `gh-pages`, `out` and `.novc` — which is
why `py_ac_loc/` and `doc/` have no accessor at all. Re-establish with

```bash
grep -rn "boj_data_root() /" py/
```

**`py/repo_scopes.py` calls `boj_paths.code_paths()`, `boj_paths.boj_data_root()` and
`boj_paths.code_dir()`** — the union the source lints scan. Step 3 has to keep those lints scanning
the same files under the new spelling, and a change in what they cover is a finding.

**Trap — a SECOND module resolves this repo's clone, and it is not `boj_paths.py`.** Found by the
2026-08-22 review. `py/uxlc_paths.py`'s `book_of_job_dir()` and `require_book_of_job_dir()` are
read by `py/main_map_changes_to_book_of_job.py` — `BOOK_OF_JOB_REPO / "out" /
"enriched-quirkrecs.json"` and `BOOK_OF_JOB_REPO / "gh-pages" / "jobn-details"`, whose
`walk_html_chain` parses `<title>` and `<td>` cells out of the pages. That script is one of
UXLC-utils' three oracle commands, but what it resolves is **this** repo's clone, so **the repoint
is this phase's Step 3**, not Phase 5's. Left alone: after this phase's Step 4 it walks **stubs**
— the walker reports "FILE NOT FOUND" only for an absent file, and a stub is present, with a
`<title>` and no `<td>` — and rewrites `in/UXLC-misc/2026.04.01-map-to-book-of-job.json` from
garbage without raising; at this phase's Step 6 `require_book_of_job_dir` fails loudly. Run
UXLC-utils' oracle after this phase's Step 3 as well as book-of-job's own, which is not what the
lane's Step 3 says by default.

**A repoint work item for this phase's Step 3, and it predates this plan.** `_WLCAU` in
`py/author_boj/job5_orphan_qere_points.py` emits `https://bdenckla.github.io/UXLC-utils/wlc-a-notes/`
twice into `gh-pages/jobn/job5_orphan_qere_points.html`, and that URL has 404'd since at least
2026-04-10 — UXLC-utils never had a `wlc-a-notes/`; wlc-utils did, and it is now
`gh-pages/wlc/wlc-a-notes/` here. Set it to
`https://bdenckla.github.io/MAM-basics/wlc/wlc-a-notes/` and regenerate; the page is one of the
183 the oracle rewrites. Layer 4 has the finding in full.

**Decision D is answered before Step 1, not during it — and it IS answered: drop, Ben,
2026-08-23.** `py_ac_loc/` is 96% of this repo's non-`gh-pages` bytes, has no consumer, collides
by name with MAM-basics' `py/py_ac_loc/` package, and is a byte-exact 2026-02-19 snapshot of
codex-index-aleppo's data (Phase 0's blob comparison under Decision D). So Step 1 copies `out/`
and `doc/` only, 9 files; Step 5 deletes `py_ac_loc/` with the rest; the mark-order check's 509
files become 460; and `doc/reading-mam-simple.md` is reworded where it names the directory.
Landing it "for now" under a made-up name was the outcome to avoid, and it is avoided.

---

## Phase 5 — UXLC-utils

*The per-repo lane, run for `C:\Users\BenDe\GitRepos\UXLC-utils`.*

**Last, because it is the entangled one.** Its published tree is the middle of the three at 184
files, but it carries **596 files outside `gh-pages/`**, a second resolution path in
`mb_cmn/paths.py`, 52 space-containing tracked paths, a downstream sparse copy in another repo, and
the one mega step this plan dissolves.

**What it holds outside `gh-pages/`**, surveyed 2026-08-22 — 596 files, 24.7 MB, being the 591
itemized below plus `.gitattributes`, `.github/workflows/pages.yml`, `.gitignore`, `CLAUDE.md` and
`README.md` (this heading and the sentence above said 597 and 24.9 until Phase 0's re-measure of
2026-08-23 — see the note under the Scale table; the Hebrew-named JPG under
`gh-pages/amb-early-mtg/img/` had been counted as outside):

| path | files | MB | what it holds |
|---|---|---|---|
| `in/` | 556 | 18.5 | `UXLC-39` 39 / 10.8 MB (canonical UXLC book XML), `UXLC-notes` 477 / 0.88 MB (downloaded tanach.us note pages), `UXLC-misc` 31 / 3.88 MB (dated change logs, `LCIndex.*`, Holman change tables, `lci_recs.json`), `UXLC-rest` 7 / 2.85 MB, `UXLC-misc-fixed` 2 / 0.09 MB (hand-corrected overrides that shadow `UXLC-misc`) |
| `out/` | 27 | 5.46 | `out/UXLC-misc/` 25 / 2.71 MB including the **hand-authored** `map-changes-to-book-of-job.md`; `uxlc-words.json` 2.74 MB; `uxlc-words-fragile.json` |
| `data/` | 2 | 0.671 | `lci_augrecs.json`, `lci_recs.json` — generated lookup tables **other repos consume** |
| `doc/` | 2 | 0.096 | `clc-design.md` and `clc-skeleton-plan.md`. **Live prose**, cited from `github-misc/dot-claude/CLAUDE.md` |
| four loose files | 4 | 0.008 | **Decision E** |

**Trap 1 — the space hazard is here, not in holman-ketiv-qere.** **52 tracked paths outside
`gh-pages/` contain a space**, none of them quoted by `git ls-files` because all are ASCII: 26 in
`in/UXLC-misc/`, 18 in `out/UXLC-misc/`, 4 in `in/UXLC-notes/`, 2 in `in/UXLC-misc-fixed/`, 2 at
top level. Re-establish with

```bash
git -C ../UXLC-utils ls-files | grep -v '^"\?gh-pages' | grep -c ' '
```

**Use `-z` and null-delimited iteration throughout this phase**, in the copy and in every
verification. One file *is* quoted and it is under `gh-pages/`, for a Hebrew word in its name.

**Trap 2 — the second resolution path.** `py/mb_cmn/paths.py`'s `uxlc_utils_dir()` and
`require_uxlc_utils_dir()` bypass `uxlc_paths.py` entirely, with four call sites in
`py/main_extract_docx_and_render_table.py`, `py/main_lenin_vendor_uxlc.py` and
`py/main_wlc_vendor_uxlc.py`. A repoint following `uxlc_paths.py` alone misses those four.
`py/tests/test_verify_table_notes_in_uxlc.py` spells `"UXLC-utils"` ten times more, all of them
fixture paths under `tmp_dir` passed as `uxlc_utils_path=`, none a resolution and none needing a
repoint — see "The organizing idea". **`uxlc_paths.py` also has no `DATA_REPO_NAME` to grep for.**

**Trap 3 — `py/main_wlc_vendor_uxlc.py` becomes a self-copy, and deleting it is the phase's
largest change.** It copies `UXLC-utils/in/UXLC-39`'s XML and `UXLC-utils/out/UXLC-misc`'s JSON
into MAM-basics' `in/UXLC-39` and `in/UXLC-misc`; once the source tree is here, both sides are the
same repo. **This is what 40 of the 41 duplicate blobs of Phase 0's census are** — the 41st,
`out/UXLC-misc/sanity_problems.json`, is a 3-byte `[]` that nothing vendors and that moves with
`out/`; Phase 0's item 2 has it. Deleting the entry point
means also removing the mega's `wlc-vendor-uxlc` step and rewriting the `find-uxlc-accent-changes`
step's "must come after wlc-vendor-uxlc" note and the `accgram-survey-chanted-word-accents` step's
ordering comment, both of which name it. **Decide deliberately whether MAM-basics keeps two copies
of the same data** — `in/UXLC-39/` alongside the arriving `in/UXLC-39/`, and `in/UXLC-misc/`
alongside the arriving `out/UXLC-misc/` — **or collapses to one**, and put the collapse to Ben,
since it changes what several accgram steps read. **`lci_recs.json` is a third pair in that same
question** (Decision C, 2026-08-23): MAM-basics' `in/lci_recs.json` and the arriving
`data/lci_recs.json` differ by one header comment line and are read by two parallel modules,
`py/py_uxlc/my_uxlc_page_break_info.py` and `py/uxlc_misc/my_uxlc_page_break_info.py`; put all
three pairs to him at once rather than one per session.

**Trap 4 — codex-index-leningrad holds a sparse vendored copy, and it is already stale.**
`codex-index-leningrad/UXLC-utils-sparse/` is refreshed by MAM-basics'
`py/main_lenin_vendor_uxlc.py`, and that repo's `CLAUDE.md` says *"`../UXLC-utils` is the source of
truth — never edit `UXLC-utils-sparse/` directly"*, names `../MAM-basics/py/main_uxlc_mega.py`, and
records at a line found by searching for the date that **as of 2026-08-22 the vendored copy is
behind**, taken at UXLC-utils `748ee2f`. Its `README.md` names the same paths, as does
`UXLC-utils-sparse/provenance.md` and `page-snips/README.md`. **Step 3 repoints
`main_lenin_vendor_uxlc.py` at MAM-basics' own tree and Step 5 owes codex-index-leningrad a commit**
correcting those statements. This is the strongest external coupling any of the three repos has;
the three MAM-* data repos, phonetic-hbo and diffable-pointed-hebrew have none. **Before Step 3
writes the repoint, put Decision E's parked question to Ben**: the sparse copy's only reader is
MAM-basics' own `main_lenin_wikisource_page.py`, so the repoint keeps alive a copy of this repo's
own `data/lci_augrecs.json` read through a sibling, and retiring the copy, the vendoring script and
`lenin_paths.uxlc_sparse_dir` instead is the alternative. Whichever he chooses, Step 5's
codex-index-leningrad commit says which.

**Trap 5 — `shared-with-codex-index-leningrad.md` is a live instruction whose claim expires**, per
Decision E.

**Trap 6 — this repo's Step 6 breaks other things, so run the other two repos' oracles after it.**
(It is one of two such Step 6s, not the only one: Phase 4's removal of the book-of-job clone
breaks this repo's own `main_map_changes_to_book_of_job` unless Phase 4's Step 3 repointed
`uxlc_paths.book_of_job_dir()` — see Phase 4's trap.) Removing the UXLC-utils clone takes away a
directory that
`holman-ketiv-qere`'s `main_estimate_uxlc_locations` reads and that
`main_lenin_vendor_uxlc.py` copies from into `codex-index-leningrad/UXLC-utils-sparse/`. **Both
must already be repointed at MAM-basics' own tree by this phase's Step 3**, and Step 6 is what
proves it: `require_sibling` fails loudly on a missing directory, so a survivor announces itself
rather than silently reading a stale copy. Run `py/main_test.py`, all three repos' oracles, and
`main_lenin_vendor_uxlc.py` after the removal, not before.

**One thing that does NOT change:** MAM-basics' `CLAUDE.md` §"Five issue trackers" records
UXLC-utils' `doc/` as a standing exception, where a bare `#NN` still means a UXLC-utils issue. That
`doc/` is now moving into MAM-basics, where a bare `#NN` means a MAM-basics issue. **So the
exception stops being about a sibling repo's directory and becomes about two files inside this one**
— which is exactly the shape wlc-utils' `doc/` took when it arrived. Phase 6 rewrites the section;
**do not prefix the citations inside `clc-design.md`**, since qualifying them would imply they were
ambiguous, and that repo's plan settled the same question the same way.

---

## Phase 6 — Cross-repo bookkeeping, and close the second stage

*In MAM-basics, plus three places no repo's tooling can see.* Modelled on
`PLAN-evacuate-the-rest-of-wlc-utils.md`'s Phase 11, which is the checklist to re-read.

1. **`MAM-basics/CLAUDE.md` §"Five issue trackers"** — rewrite the standing-exception paragraphs.
   Before this plan, the exceptions are wlc-utils' `doc/` and `in/` copies living here plus
   UXLC-utils' own live `doc/`; afterwards UXLC-utils' two `doc/` files live here too. **The three
   trackers keep their issues and their numbers, and the `<repo>#NN` citation convention is
   unchanged** — say so in the commit message, so nobody reads a fully-evacuated repo as licence to
   "tidy" the split. Check whether the section's "holman-ketiv-qere needs no such exception" and
   "book-of-job needs no such exception either" paragraphs survive the arrival of those repos'
   `doc/` files.
2. **`MAM-basics/CLAUDE.md` §"`doc/boj-*.md` are book-of-job's procedures"** — it ends by saying
   book-of-job keeps two procedures of its own, `doc/opening-html-files.md` and
   `doc/reading-mam-simple.md`. Phase 4 moves both. Rewrite that sentence.
3. **`C:\Users\BenDe\.claude\CLAUDE.md`** — the global file, tracked in `github-misc` at
   `dot-claude/CLAUDE.md`, which does **not** auto-sync. It names all three repos across roughly a
   dozen lines. Edit the live copy, then copy it back and commit, or the tracked copy silently goes
   stale:

   ```powershell
   Copy-Item "$HOME\.claude\CLAUDE.md" "$HOME\GitRepos\github-misc\dot-claude\CLAUDE.md" -Force
   ```

4. **The `hebrew-prose` skill**, live at `C:\Users\BenDe\.claude\skills\hebrew-prose\` and tracked
   at `github-misc/dot-claude/skills/`, two copies that do not sync. Its
   `references/terminology.md` names UXLC-utils twice and book-of-job not at all; book-of-job and
   UXLC-utils are both named in `SKILL.md`'s frontmatter `description` line, which is what decides
   when the skill fires. (This item said `terminology.md` "names book-of-job and UXLC-utils" until
   the 2026-08-22 review.) **Edit both copies of each file and verify byte-identical after.**
5. **`in/vendoring_policy.json`** — no entry remains for any of the three; each was deleted as its
   Python plan finished. Confirm rather than assume, and re-run `py/main_vendoring.py --all` if
   anything changes, since `test_vendoring_policy_paths.py` derives its parametrize lists from that
   file and UXLC-utils' Phase 4 lost three tests that way.
6. **`in/repo_maintenance_policy.json`** — the register of what is frozen and why. **Removing the
   clones settles this rather than raising it**: `frozen_repos` no longer skips anything at run
   time, the freeze having been structural since 2026-08-07, and a sweep cannot reach a repo that
   is in neither `GitRepos` nor `FrozenRepos`. So the three are unreachable whether or not they are
   registered. **The remaining question is documentary — should the register record why they left?
   — and it is Ben's.** Note the precedent both ways: **wlc-utils is not in `frozen_repos` today**,
   checked 2026-08-22, though the same question was put at its Phase 11; and every repo that *is*
   registered is a paused client project whose last-changed date is the point, which is not what
   these three are.
7. **`all-repos.code-workspace` — the three entries must GO, and Step 6 is what forces it.**
   `../book-of-job`, `../holman-ketiv-qere` and `../UXLC-utils` at three lines. Both the UXLC-utils
   plan and the book-of-job plan recorded a decision to leave them listed *because each still held
   hundreds of tracked non-Python files*; that reason expired when the trees moved, and the clone
   removal ends the matter — a workspace folder naming a directory that does not exist is not
   merely stale but **fatal to every sweep**, per Step 6's ordering rule.
   **Remove each entry in its own repo's lane, in the same commit as that repo's Step 5**, so the
   workspace file never names a directory that has just gone; **this item is then a confirmation
   here rather than an edit.** **The arithmetic, measured 2026-08-22 rather than taken from either of
   the two conflicting figures in circulation that day**: the file listed **20** folders, and **19**
   once wlc-utils came out, which is where it stood mid-flight when this was checked with
   `grep -c '"path":' all-repos.code-workspace`. **So this plan takes it to 16.** Re-run that
   command rather than assuming the starting point.

   **`../wlc-utils` is already gone, and this plan did not own that** — Ben's instruction in the
   concurrent session of 2026-08-22 was *"Freeze the manifest, then delete the clone and workspace
   entry"*, and the 2026-08-22 review found it done: 19 folders listed, no `../wlc-utils`, no
   clone. **So do not expect `../wlc-utils` to be present as a control**, which an earlier draft
   of this file wrongly said it would be, giving as the reason that its clone "still receives
   commits from the stub generator" — the frozen manifest is exactly what establishes that it
   almost never does. Phase 2's one-off re-clone for its byte-identity check does **not** put the
   entry back. Confirm what the file lists rather than assuming either way.
8. **`py/repo_util/check_repo_standards.py`** discusses these repos in prose. Follow the convention
   already used there: append to the dated blame-crawl paragraphs, rewrite only what is false as
   written.
9. **`MAM-private/masorah-books/doc/migration-checklist.md`** names two book-of-job paths that
   Phase 4 makes stale — `../book-of-job/gh-pages/jobn-details/1413.html` and
   `../book-of-job/out/enriched-quirkrecs.json` — and warns that they are deep-linked. One commit
   in MAM-private. (This item said a third path, `../book-of-job/pyauthor_qr/qr_1413.py`, was
   "already stale" until the 2026-08-22 review; that line already reads
   `../MAM-basics/py/author_boj_qr/qr_1413.py`, with a dated note of the move.)
10. **`MAM-private/mgketer/CLAUDE.md`** says *"It reads `../UXLC-utils` from MAM-basics now"* and
    instructs relative `../repo-name` addressing including `book-of-job`. Same commit.
11. **Update this file's Status table and the programme's.** Add a paragraph to
    `PLAN-evacuate-python-programme.md` recording that its second stage is complete, and that its
    carried decision 2 — "`gh-pages/` stays put indefinitely" — is now broken four times rather
    than once.

---

## Risks, and what could go wrong irreversibly

- **A stub pointing at a page that is not there.** A redirect to a 404 turns a working URL into a
  confidently wrong one, and a citation Ben cannot reach is one nobody will report — **not the
  citations in mgketer, `document-index` and `py/author_boj/`, which are his own and which this plan
  repoints rather than redirects** (layer 4; an earlier draft of this bullet had them the wrong way
  round, and named UXLC-utils' CLC deep links here, which are outbound and not citations of these
  repos at all). **Mitigated twice over**: the
  lane's hard gate, Step 4 not running until Step 1's deploy has been HTTP-verified; and, for the
  case that arises *later* — a frozen page renamed or dropped here — the per-repo manifest test of
  Phase 2's consequence 3, which fails the ordinary suite naming the page and needs no clone.
  **"Nobody will report it" is therefore true of the world and false of the suite**, which is the
  whole reason that test is worth having per repo.
- **Deleting a source tree before every reader is repointed.** Step 5 is the only irreversible
  step in the lane, and it is separated from Step 3 by a full oracle run for exactly that reason.
  UXLC-utils is the sharp case, because `codex-index-leningrad` reads it through a vendoring
  script and `holman-ketiv-qere`'s own oracle reads it too.
- **A blob that differs because `.gitattributes` differed.** Silent, and it destroys the only
  evidence covering 884 PNGs, 3 JPGs and 4 woff2 (and, until 2026-08-23, the 20.6 MB docx, which
  no longer moves). **Mitigated by Phase 1 preceding every Land step**, and detected by layer 1
  if it happens anyway.
- **A naive glob dropping a file with a space or a non-ASCII byte in its name.** 52 such paths in
  UXLC-utils, 1 in holman-ketiv-qere plus 2 quoted ones, and the largest single file in the whole
  move is one of them. **Mitigated by `-z` everywhere.**
- **A stub whose target carries a raw `#`**, redirecting holman-ketiv-qere's two JC3 pages to a
  path truncated at the `#`. Silent — the stub is well-formed and `check` would pass it if the
  expected target is built the same raw way. **Mitigated by percent-encoding in `target_url`**
  (Phase 2) and by Step 4's fetch of one of the two at its encoded old URL.
- **A concurrent execution of a plan that regenerates an arriving artifact**, which makes a move
  bug and a page edit indistinguishable. Precondition 3.
- **Untracked content destroyed with the clone at Step 6.** The GitHub copy holds only what was
  committed, so a `.novc/`, a `.venv` or an unpushed branch goes for good. **The known case is
  holman-ketiv-qere's `.novc/eml/`, 13 messages its own oracle needs**, and it is known only
  because that repo's Python plan wrote it down. Mitigated by Step 6's
  `git status --porcelain --ignored` and unpushed-branch check, which is the one part of that step
  that has to happen *before* the delete rather than after.
- **`py_ac_loc/` landing under an invented name because Decision D was deferred into a phase.**
  Not dangerous, but it is how a 7.8 MB directory nobody reads becomes permanent.

---

## How to run this plan across sessions

**A fresh session should be able to pick this file up and execute the next phase without reading
this one's conversation**, which is the standard `~/.claude/CLAUDE.md` sets. What that requires of
each session:

1. **Read this whole file first**, then the phase you are running, then the sections it cites in
   `PLAN-evacuate-the-rest-of-wlc-utils.md` by name.
2. **Re-measure before trusting any figure**, using the command given beside it, and **treat a
   mismatch as a finding** — write it into the section, do not silently update the number.
3. **Write an execution record under the phase**, in the style the four completed plans use:
   what landed, in which commit of which repo, what differed from what was written, and what the
   next phase now knows that this file did not say. **Record the commits.**
4. **Commit and push per `~/.claude/CLAUDE.md`'s Git section** — directly to `main`, at will,
   without asking. Run black on any Python touched, from
   `C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe -m black`, before committing.
5. **Update the Status table in the same commit** as the work it describes.
6. **Do not start a lane you cannot finish through Step 3.** Steps 1 and 2 leave the tree in dual
   residency, which is safe and revertible and can sit indefinitely. Stopping between Step 3 and
   Step 4 is also safe — the source repo still serves its own pages. **Stopping between Step 4 and
   Step 5 is the one bad place to stop**: the pages are stubs and the data is still there, so the
   repo is neither a working site nor an emptied one. Stopping between Step 5 and Step 6 is safe
   and can sit indefinitely — an emptied clone on the disk costs nothing but the space, and Step 6
   is a verification as much as a cleanup, so it is worth running deliberately rather than
   tacked onto a tired session.
