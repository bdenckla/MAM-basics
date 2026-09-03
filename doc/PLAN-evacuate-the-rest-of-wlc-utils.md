# Evacuate the rest of wlc-utils into MAM-basics

State: executed 2026-08-17

**This file is the plan. There is no other copy.** It was drafted on 2026-08-03 in
`~/.claude/plans/`, as plan mode requires, and **that copy was deleted once this became the
tracked one** — deliberately, and departing from what
`doc/PLAN-evacuate-python-from-wlc-utils.md` did. That plan left its draft in place under a
`SUPERSEDED — do not edit or work from this copy` banner; five days on, the banner is doing its
job and the file is still 651 lines against the tracked 1228, a near-half-stale document sitting
where a session looking for "the plan" might plausibly find it. Ben, 2026-08-03: *"why not just
delete that stale plan to make it impossible to be confused for 'the real plan'?"* A banner has
to be read; a deleted file cannot be worked from. Nothing was lost — the draft was byte-identical
to this file's first commit apart from its header, so `git show` recovers it.

**So do not re-create one.** If a future session drafts in `~/.claude/plans/` again, fold it in
here and delete it, as `8daef35` did with two such scratch plans.

**ALL ELEVEN PHASES ARE DONE — 0 and 1 on 2026-08-11, 2 through 5 on 2026-08-12, 6 through 8 on
2026-08-13, 9 through 11 on 2026-08-17 — AND THE PLAN IS COMPLETE. Phase 9 was the first deletion
this plan made: wlc-utils went
from 626 tracked files to 497, at `f10f405`, its 154 published pages replaced in place by redirect
stubs, a `404.html` added, and the 130 non-HTML assets removed. Phase 10 finished the emptying the
same day: wlc-utils now tracks 161 files — the 155 stubs plus six root files — at `8250b69`, its
`README.md` and `CLAUDE.md` rewritten as a redirect host's. Phase 11 closed the cross-repo
bookkeeping — every pointer repointed, the freeze on `doc/PLAN-two-accents-on-one-chanted-word.md`
lifted, the three stop-and-ask items answered by Ben — and this plan now records finished work
only.**
Phase 3 **copied** 620 of the original 626 into MAM-basics rather than moving them — that was the
dual-residency window, which Phase 9 closed for `gh-pages/` and Phase 10 closed outright — and the
six loose root files stayed behind. **The site is live and complete**: Ben enabled
Pages on 2026-08-11, `.github/workflows/pages.yml` arrived with the corpus at Phase 3, whose push
fired the first deploy, and Phase 6 added `gh-pages/index.html` on 2026-08-13, so
`https://bdenckla.github.io/MAM-basics/` and everything under `/wlc/` both serve. **Every URL any
other repository cites has been fetched and checked** — Phase 6's execution record has the table,
and Phase 9 re-ran that same list against the old site, where each now serves a stub naming its
MAM-basics equivalent.
Phase 0 is a preflight, Phase 1 edits only `py/mb_cmn/provenance.py` and its test, and Phase
2 edits only MAM-basics' own `.gitattributes`, and Phases 4, 6, 7 and 8 edit only MAM-basics' own
licence, site, generator and source files, so until 2026-08-17 the only thing any phase had changed
in wlc-utils was the freeze notice Phase 0 was asked to land there — see Precondition 1. **Phase 9
ended that**, being both the first phase since Phase 0 to commit inside wlc-utils and the first to
change what the public web serves. **Phase 7 is
the one intentional artifact change in the plan and it has landed**: one `href` on
`gh-pages/wlc/420422/index.html`, in its own commit so that no later phase's zero-diff oracle
carries a real diff inside it. **Phase 8 changed no artifact at all**: the 155 redirect stubs it
builds go to a gitignored scratch directory, and `build --publish` is what Phase 9 used to land
them in wlc-utils. Phase 11 ran on 2026-08-17 and was the last: **the plan is complete**. (This
paragraph read "Nothing has been executed. Every phase below is
unstarted" until Phase 0 ran, and was rewritten at each phase since — "Phase 11 is unstarted" was
the last clause of the original to go. Until Phase 3 it also said
"No file has moved yet" and "no GitHub setting has been touched"; until Phase 6 it said the site
root "404s until Phase 6 adds `gh-pages/index.html`, by design"; and until Phase 9 it opened
"Nothing has been deleted from wlc-utils: it holds the same 626 tracked files it always did". All
four are now false, which is why they are replaced here rather than softened.)

**AS OF PHASE 5, NO PROGRAM WRITES INTO wlc-utils, AND THAT IS THE THING THE WHOLE PLAN WAS FOR.**
`py/wlc_paths.py` is deleted and every generator resolves its corpus under `paths.repo_root()`, so a
MAM-basics worktree now isolates the generated artifacts as well as the source. Measured, not
asserted: a full circuit run left wlc-utils with zero files touched by mtime. What still reached
that repo **in a routine run** was one **read** — `test_h_dot_below_nfc.py`'s wlc-utils NFC scope,
which Phase 5 was told to leave and Phase 10 deleted on 2026-08-17, so a routine run now reaches
wlc-utils not at all. **Phase 8 added a second path, and "routine"
is what keeps this paragraph true**: `py/wlc_redirect/stubs.py`'s `wlc_utils_pages_dir` reaches the
same sibling, but nothing runs it except `main_wlc_redirect_stubs.py check` with no `--dir` and
`build --publish` — no mega step, no test — so a suite run and a circuit run still leave wlc-utils
alone. Phase 8's finding 1 has the full disposition of all three sites that name that sibling.

Written 2026-08-03, on the model of `doc/PLAN-evacuate-python-from-wlc-utils.md`, which is its
precedent in shape and in discipline. Every number below is stated with the command that
re-establishes it, because the tree will have moved on. **Re-measure before relying on a figure,
and treat a mismatch as a finding rather than as noise.**

Repos are `C:/Users/BenDe/GitRepos/wlc-utils` and `C:/Users/BenDe/GitRepos/MAM-basics`. Only
MAM-basics has a `.venv`; wlc-utils' was removed after the Python left (checked 2026-08-03 —
`ls .venv` there finds nothing, so the Python plan's Phase 4 note about a leftover 80 MB venv is
stale).

## Status

| Phase | State |
|---|---|
| 0 — Preflight: baseline, manifest, collision census | **DONE 2026-08-11**, MAM-basics `5344a74` + this write-back, plus three baseline commits in three other repos and one freeze commit in wlc-utils (`c501dc0`). Every census claim re-measured and every one reproduces, the load-bearing zero-self-links figure included. The circuit ran green and **wlc-utils came through it with zero files changed**. **The baseline was NOT clean at first look — 17 files across three repos, from three unrelated causes**, all now committed. Suite is **903 passed / 5 skipped**, not the 913 this plan carried. Three findings this plan did not predict, the sharpest being that **a sibling repo's vendoring drifts this repo's own tracked tree**. Findings under Phase 0 below |
| 1 — The provenance worktree fix | **DONE 2026-08-11.** All three remaining pieces landed: step 2 in MAM-basics `0008eb8`, the tautology-test repairs in the same commit, and the al-hatorah wrapper **retired** in MAM-private `20dfb63` after `c0540e5` pulled the new vendored copy. The re-vendor ripple cost three more commits in three repos — MAM-simple `bae0bff`, MAM-basics `1097530` and `57b83cf` — and MAM-with-doc `d2dc6e5` for a by-design drift the circuit surfaced. Baseline reproduced exactly: **903 passed / 5 skipped**, ruff and black clean at 771 files, wlc-utils' manifest byte-identical and **wlc-utils unmoved at `c501dc0` throughout**. Seven findings, the sharpest being that **this phase's own verification (b) was stale and tested the wrong thing** — `38a3bc7` had already made a worktree run come out right, and the generator the plan names writes no breadcrumb at all. Finding 7 also **settles the long-unverified worktree suite count**: 903 / 5 from a worktree with `REPOS_ROOT` set, identical to the main checkout, zero unreal failures, 919 dead. Findings under Phase 1 below |
| 2 — `.gitattributes` merge | **DONE 2026-08-12**, MAM-basics `30f985b` + this write-back. The four binary declarations landed verbatim, `*.csv text eol=crlf` kept, `* text=auto eol=lf` untouched — and **`git check-attr -a` resolves identically in the two repos** for both paths this phase names, which is the property layer 1 actually needs: agreement between the repos, not any particular attribute value. `GITATTRIBUTES_LF=True`, tree clean, no circuit run and none needed. Three findings, the sharpest being that **this plan's baseline had already moved when the phase began** — MAM-basics was at `e4d7997`, three commits past Phase 1's `9194265`, all three landed the same day. Findings under Phase 2 below |
| 3 — Copy the corpus in (dual residency) | **DONE 2026-08-12**, MAM-basics `f99996f` + this write-back. **620 files land, not the 626 this phase's own verify line claims** — the six loose root files do not travel, exactly as Phase 0's disposition table says — so layer 1 reads **620 of 620 SHA-1 matches**, zero missing, zero mode mismatches, path deltas exactly the 284 `gh-pages/wlc/` prefixes and the one `lci_recs.json` rename. Suite **903 passed / 5 skipped**, ruff clean, black clean at 771 files, all unchanged; **wlc-utils untouched at `c501dc0`**, so Phase 0's manifest stands. **The site is live and the deploy went green**: 8 of 8 HTTP checks as expected, every page byte-identical to what was committed, and the site root 404s by design until Phase 6. Four findings, the sharpest being that **the NFC lint's first failure was a crash on an extensionless GIF, not the offender report this phase predicts**. Findings under Phase 3 below |
| 4 — Licence scoping | **DONE 2026-08-12**, MAM-basics `20bb89e` + this write-back. Thirteen rows added to `DATA-LICENSES.md` and the CC0 1.0 text repeated verbatim at the end of it, beside the MAM statement — **but no CC0 `LICENSE` file was placed in any subtree**, because not one of the three trees this phase names holds only Ben's own work. Coverage checked mechanically rather than by eye: **620 of 620** moved paths are named by a licence statement, **276** are claimed for CC0, and **zero** of those 276 fall in the excluded set. Suite **903 passed / 5 skipped**, no Python touched, no generator or circuit run. Four findings, the sharpest being that **`gh-pages/wlc/` holds 124 scan crops of manuscripts and printed editions** — so this phase's own instruction to place a CC0 file there would have dedicated Koren's and the Leningrad Codex's photography to the public domain. Findings under Phase 4 below |
| 5 — Collapse `wlc_paths.py`; repoint every generator | **DONE 2026-08-12**, MAM-basics `5ed6bb4` + `3edbc5b` + `6fd9a9c` + this write-back, plus one re-vendor commit in holman-ketiv-qere (`637237b`). **The plan's sharpest assertion holds: wlc-utils came through a full circuit run with ZERO files touched**, by mtime and not merely by `git status`, and zero across the whole session. Against wlc-utils as the frozen reference, **614 of the 620 moved paths are byte-identical** — every one of the 284 `gh-pages/wlc/` files included — and the six that differ have two named causes, neither of them a move bug. Suite **903 passed / 5 skipped / 57 subtests**, `ruff` clean, `black` clean at **770** files, one fewer than the baseline 771 because `wlc_paths.py` is gone. **Eight findings, the sharpest being that the plan missed a relative-link computation that would have rewritten the stylesheet href on all 154 pages at once.** Findings under Phase 5 below |
| 6 — Pages live on MAM-basics — ~~**manual gate**~~ **no gate left** | **DONE 2026-08-13**, MAM-basics `c50745a` + this write-back. `gh-pages/index.html` closes the root 404 that had stood since Phase 3, and its deploy went green — run `31710845632`. **The workflow Phase 3 landed is byte-identical to wlc-utils' own**, so the "Copy … verbatim" paragraph reproduces clause for clause with zero differences. **The check list ran 12 of 12 as expected**: 11 URLs at 200 with the served bytes sha256-identical to the committed file, and `/wlc/accgram/` at 404 by design — filed as #230. The stylesheet and the font both resolve and serve at both depths that reference one, and all four fragment anchors are present in the served HTML. Suite **903 passed / 5 skipped**, `ruff` clean, `black` clean at **770** files; no Python touched, no generator and no circuit run. Five findings, the sharpest being that **this phase's own verify list calls `wlc/index.html` a depth-1 page exercising `../style.css`, and it is the one page on the site that references no stylesheet at all**. Findings under Phase 6 below |
| 7 — Repoint the `420422` blob URL | **DONE 2026-08-13**, MAM-basics `a8a9875` + this write-back. The regenerated diff is **exactly what this phase predicts — one source line and one `href`**, in two files and no others. The new blob URL returns **200**, and so does the old one, wlc-utils holding the file until Phase 10; the two are **the same blob, `57439cd` in either repo**, so the destination content does not change, only the repository serving it. `git grep "bdenckla/wlc-utils" -- py gh-pages` is down to three hits and **not one is a link to content**: two commented-out `issues/NN` citations and one prose mention of `bdenckla/wlc-utils-**private**`, a different repository the pattern matches as a prefix. Suite **903 passed / 5 skipped**, `ruff` clean, `black` clean at **770** files. **No circuit run, and the judgement not to run one is recorded below** — the generator is a leaf. Four findings, the sharpest being that **this phase's own instruction to find the constant by the URL string rather than by line number does not work as written**: black split the URL across two adjacent string literals, so the URL the page carries appears nowhere in the source. Findings under Phase 7 below |
| 8 — The redirect-stub generator | **DONE 2026-08-13**, MAM-basics `6a7347d` + `520dc27` + this write-back. `build --out <scratch>` writes **155 files** — 154 page stubs and `404.html` — and `check` over them passes; the three spot-reads at depths 0, 1 and 2 each name their own path's prefix rewrite in all four carriers. **`git status --porcelain` held only the four new source files**, so no tracked artifact moved in either repo and no circuit was run or needed. Suite **905 passed / 5 skipped**, up 2 from 903, and the delta is exactly the new entry point's two parametrized tests in `test_entry_point_subcommands.py`; `ruff` clean, `black` clean at **774** files, up 4 for the four new modules. Phase 6's finding 4 checked rather than assumed: `420422/` and `wlc-a-notes/` get stubs and `accgram/` correctly gets none, all three falling out of the derivation with no special case. Five findings, the sharpest being that **"the last remaining reference to the sibling" describes the state after Phase 10, not this one** — three sites name wlc-utils now and they need three different dispositions. Findings under Phase 8 below |
| 9 — Flip wlc-utils' `gh-pages/` to stubs — ~~**gated on 6**~~ **gate met** | **DONE 2026-08-17**, wlc-utils `f10f405` + this write-back. One commit there, exactly the shape this phase specifies: **154 `M`, 130 `D`, 1 `A`** — the pages modified in place rather than deleted and re-added, `404.html` the only addition, nothing staged outside `gh-pages/`, and no empty directory left behind. wlc-utils goes from 626 tracked files to **497**, of which 155 are the stubs and **zero** are non-HTML. The deploy went green — run `32076961634`, 21 seconds — and **every URL on the Phase 6 list now serves a stub naming its MAM-basics equivalent**, byte-identical to the committed file, with that equivalent itself fetched at 200 so a redirect to a 404 could not pass; the four unstubbed paths tried each answer **404 with the forwarding script**, as designed. Suite **905 passed / 5 skipped**, `ruff` clean, `black` clean at **774** files, MAM-basics otherwise untouched at `2951a01` — **the baseline reproduced with zero drift**, every figure, the re-taken manifest included. Four findings, the sharpest being that **the JavaScript did get executed after all: Phase 8's "there is no `node` on this machine" overlooked `cscript.exe`**, so all four published fragment links were run against the committed bytes rather than read. Findings under Phase 9 below |
| 10 — Empty the rest of wlc-utils | **DONE 2026-08-17**, wlc-utils `cd668e3` + `8250b69`, MAM-basics `aa7f269` + this write-back. The 336 deletions are exactly the five items this phase names, staged as **336 `D` and nothing else**, leaving **161** tracked — the count Phase 9 measured against the verify line's since-corrected 160 — with no untracked residue. **Layer 1 was re-derived one last time in the minutes before the delete**: 335 moved-and-deleted files plus the surviving workflow compared by blob SHA-1, **330 byte-identical, zero missing, and the 6 differing exactly Phase 5's six**; then the frozen reference ended. Both deploys green and **every Phase 9 URL check passes unchanged**; `check` still lints the stubs green. Suite **905 / 5**, `ruff` clean, `black` clean at **774**, and the circuit gave a **zero diff in all ten repos with zero wlc-utils files touched by mtime**. Five findings, the sharpest being that **the "88 issues" this plan and both repos' instruction files repeat is five short, and was on the day it was first written** — the tracker holds 93, #89–#93 filed 2026-07-31. Findings under Phase 10 below |
| 11 — Cross-repo bookkeeping | **DONE 2026-08-17**, MAM-basics `1026778` + this write-back, UXLC-utils `f99610a` (item 9), github-misc `5801305` (items 2 and 3); **wlc-utils untouched at `8250b69`, and the plan is COMPLETE**. All eleven items executed or verified as the no-ops they claim to be, and the freeze on the two-accents plan lifted, dated, in its own notice. Ben answered the three stop-and-ask items the same day: item 2 at the plan's scope — **five** evacuation-stale sites fixed, not the banked four, the six `py/`-path sites stale since 2026-08-01 left flagged; item 3 at full scope — **ten** sites, the plan's six plus two paragraphs Phases 9–10 falsified plus two touch-ups; item 5 decided **no entry**, the freeze register being structural since 2026-08-07 and wrong for a repo still in both workspace files receiving stub-generator commits. Both unsynced pairs verified byte-identical before AND after their edits. Item 4's prediction confirmed by re-running the scan: the NFC findings left wlc-utils' report (`NFC_H_DOT=0; NFC_LATIN=0`) and sit under MAM-basics at Phase 3's exact seven sequences. Suite **905 / 5**, `ruff` clean, `black` clean at **774**, every repo clean and pushed. Five findings, the sharpest being that **both stop-and-ask scopes were undercounts for the same reason: Phase 10's instruction-file rewrite falsified pointer clauses no bank had predicted**. Findings under Phase 11 below |

---

## Context

On 2026-08-03 two MAM-basics sessions ran at once, each in its own git worktree. The worktree
isolated the MAM-basics side perfectly — and bought nothing, because both sessions' generators
read and write `../wlc-utils`, which has no parallel worktree. They collided there: one session
regenerated nine files under `wlc-utils/out/` (four verses flipping clean→error as METHIGAZAQEF
split into QADMA + ZAQEF, and `itm_section` filling in "§256") while the other was mid-commit.
The second session had to inspect mtimes and diffs to work out which dirty files were whose, then
stage a single path by hand rather than trusting `git status`.

One could build parallel worktrees for wlc-utils to match. Ben's judgement is that this is
elaborate for what it buys, and that the better direction is to finish the job the 2026-08-01
Python evacuation started: **evacuate wlc-utils entirely, so that a MAM-basics worktree isolates
the generated artifacts too.**

That is what this plan does, and the collision fix is the reason to prefer it over the tidier
half-measures. **A partial move does not fix it.** Four generators write into wlc-utils' `in/` —
`accgram/ctr_decalogue_fetch.py:91`, `accgram/printed_decalogue_fetch.py:89`,
`main_find_uxlc_accent_changes.py:206` (which rewrites the *tracked*
`in/accgram/uxlc_accent_changes.json`) and `main_wlc_vendor_uxlc.py:31,33` — so leaving `in/`
behind leaves a tracked file a program rewrites outside the worktree boundary. Moving `out/` and
`gh-pages/` alone would fix the incident that happened and leave the class of incident intact.

### Does it actually fix it? Yes, and here is the check

`py/wlc_paths.py`'s accessors are the complete index of what escapes the repo, and there are only
seven of them: `wlc_data_root()`, `out_dir()`, `in_dir()`, `gh_pages_dir()`, `data_dir()`,
`novc_dir()`, `scans_dir()`. Every one resolves under `wlc_data_root()`, and every one is
retargeted here. After Phase 5 the only path in the tree that leaves the checkout is
`WLC_SCANS_DIR` (`accgram/scan_page.py:56`, defaulting to
`C:/Users/BenDe/OneDrive/Documents/ScansOfBooks`) — an absolute, out-of-repo, **read-only** input
that was never in a repo and cannot collide, and the sibling repos MAM-basics already generates
into, which are exactly as unisolated after this plan as before it and are not what the incident
was about.

So: yes. Phase 5's verification is precisely this claim, tested by snapshotting wlc-utils' mtimes
across a full regeneration and requiring **zero files touched**.

---

## Scale — measured 2026-08-03

| | wlc-utils | MAM-basics | after |
|---|---|---|---|
| Tracked files | **626** | **1263** | **~1883** |
| Commits | 940 | 1037 | — |
| `.git` | 99 MB | 64 MB | ~163 MB |
| Working tree | 463 MB | 616 MB | ~800 MB |

`git ls-files | wc -l`, `git rev-list --count HEAD`, `git count-objects -vH`, `du -sh`.

**Re-measured at Phase 0, 2026-08-11**, at wlc-utils `79404fa` and MAM-basics `d100480`. The one
figure this plan actually depends on is unmoved — **626 tracked files in wlc-utils** — and the
rest have drifted, the disk figures downward:

| | wlc-utils | MAM-basics |
|---|---|---|
| Tracked files | **626** (unmoved) | **1286** (was 1263) |
| Commits | **957** (was 940) | **1152** (was 1037) |
| `.git` | **101 MB** (was 99) | **68 MB** (was 64) |
| Whole clone, `.git` included | **316 MB** (was 463) | **429 MB** (was 616) |

**Do not read the shrunken clones as files having gone missing.** Both figures above are `du -sh .`
over the whole clone, which counts untracked scratch — the `.novc/` trees and, in MAM-basics, the
`.venv` — so what shrank is scratch that has since been cleared, not corpus. The tracked-file
counts, which are what layer 1 asserts over, went **up** in MAM-basics and stood still in
wlc-utils. The projected "after" row is therefore a little low and nothing turns on it.

wlc-utils by top-level directory: `gh-pages` 284, `out` 193, `in` 135, `doc` 6, `data` 1,
`.github` 1, plus six loose root files. Disk: `out/` 98 MB, `gh-pages/` 51 MB, `in/` 34 MB,
`data/` 356 KB, `doc/` 156 KB.

**Worktrees get more expensive, and that is a real cost of this fix.** Git shares the object
store, so `.git` is paid once, but each worktree materializes a full working tree: a MAM-basics
worktree goes from ~550 MB to ~735 MB. Three stale ones is 2 GB of duplicated corpus. Clean
before Phase 3 and expect to clean again — `py/main_repo_util.py --clean-worktrees`
(`main_repo_util.py:9`).

### Nothing outside MAM-basics reads these paths

Checked across all 30 clones (`git grep -lI wlc-utils` in each). Every hit is prose, a URL, or an
issue citation — **no sibling repo opens a file under `wlc-utils/{in,out,data,gh-pages}`.** The
closest thing is `UXLC-utils/doc/clc-design.md:238`, which *names* `wlc-utils/out/wlc422-kq-u/`
in a design discussion; that is a citation to repoint in Phase 11, not a dependency.

---

## Decisions settled by Ben, 2026-08-03 — do not relitigate

1. **Everything travels.** All 626 tracked files, for the reason under Context: a partial move
   leaves a tracked file a program rewrites outside the worktree.
2. **wlc-utils stays alive as a redirect host**, emptied to 154 generated per-page stubs plus a
   `404.html` catch-all. Not archived, not deleted. Phase 9 argues why alive beats archived.
3. **The site nests at `gh-pages/wlc/`**, so `bdenckla.github.io/wlc-utils/X` →
   `bdenckla.github.io/MAM-basics/wlc/X` — a pure prefix rewrite, and MAM-basics' own site root
   stays free.
4. **CC0 is scoped to the moved trees**, GPL-3.0 stays at the root for code. Phase 4. (Narrowed
   on a finding of 2026-08-10, not relitigated: CC0 goes only to the moved trees that hold Ben's
   own work, since some of them are vendored tanach.us and chabad.org material he cannot dedicate
   to the public domain. Phase 4's "Where CC0 must NOT go" paragraph names which.)

**What made decision 3 free, and it is the load-bearing fact of the whole `gh-pages/` move:
there is not one absolute self-link anywhere under `gh-pages/`.** Every internal navigation link,
every `src`, every stylesheet reference is relative — `../style.css` from depth-1 pages,
`../../style.css` from depth-2, `img/…` from a section root, `../img/…` from `full-record/` and
`ucp/`, and `woff2/Taamey_D.woff2` resolved against `style.css`'s own location. So **the 284-file
subtree moves wholesale with zero HTML edits, at either layout**, and nesting costs nothing that
landing at the site root would have saved. Measured 2026-08-03, and re-establish it before Phase 3
rather than trusting this paragraph:

```bash
grep -rlI "bdenckla.github.io/wlc-utils" gh-pages | wc -l
```

**0** in wlc-utils. The only absolute `bdenckla.github.io` links the pages carry point *outward*,
193 of them to `MAM-with-doc`, which this plan does not touch. Were that count ever nonzero, every
hit would need rewriting in the same commit as the move, and Phase 3 would stop being a pure copy
with a blob-hash oracle.

### The inbound links — the evidence for decision 2, and Phase 6's verification list

**This is why the repo cannot simply be deleted, and it is the whole case for keeping it alive.**
Swept across all thirty clones on 2026-08-03; re-run before Phase 6 and treat any new citation as
a URL to add to the check list:

```bash
for r in */; do git -C "${r%/}" grep -lI "bdenckla.github.io/wlc-utils" -- . 2>/dev/null; done
```

| Where | What | Editable by Ben? |
|---|---|---|
| `UXLC-utils/in/UXLC-misc/2026.10.19 - Changes.xml` | **5** citations of `…/accgram/goerwitz.html` | **No** — vendored from tanach.us, where Chris Kimball publishes the UXLC change list |
| `UXLC-utils/gh-pages/clc/{Exodus-20,Deuter-5}-long-notes.html` | **4** deep links carrying fragments — `…/accgram/supplied-marks.html#supplied-{dt5v6-bet-atnax,dt5v6-bet-tipexa,dt5v17-alef-tipexa,ex20v3-alef-merkha}` | generated, so repointable — but published |
| `MAM-simple/gh-pages/versification-and-cantillation.html` | `…/accgram/printed-decalogue.html` | generated by `py/versification_and_cantillation/doc.py:63,67` |
| `document-index/README.md` | the site | yes |
| `MAM-basics` `py/clc/clc_render.py`, `py/tests/clc_collect_test.py` | the `supplied-marks.html` corroboration URL, asserted by two CLC tests | yes |

**The four fragment links are the reason the stubs need JavaScript at all** (Phase 8), and the
five tanach.us citations are the reason Phase 6 gates Phase 9. Note the last row: two MAM-basics
tests assert that URL appears in generated CLC HTML, so repointing it is a source change with a
test consequence, not a find-and-replace — deliberately left out of this plan's scope, since the
stubs keep the old URL working.

**Re-swept at Phase 0, 2026-08-11, and the table above undercounts. The sweep to run is a count,
not a file list** — the table was built from `grep -l`, which is why it reads as fewer citations
than exist:

```bash
for r in MAM-basics MAM-simple UXLC-utils document-index wlc-utils; do git -C "../$r" grep -hIo "bdenckla/.github/.io/wlc-utils[A-Za-z0-9/._#-]*" -- . ; done | sort | uniq -c | sort -rn
```

**The Phase 6 check list is 12 distinct URLs**, and three things about them are worth having
before Phase 6 rather than during it:

- **`document-index/README.md` cites four specific deep paths, not "the site"** as the table says:
  `/420422/`, `/420422/full-record/420422-54.html`, `/wlc-a-notes/` and
  `/accgram/goerwitz.html`. Two of those are **directory** URLs, so Phase 8's stub set has to
  cover `index.html` at a directory a citation names without naming the file. All four resolve to
  a file that exists today, checked.
- **UXLC-utils is 7 files, not 3 — but that is one fact counted four times, not new exposure.**
  The tanach.us change list is vendored there four times over (`in/UXLC-misc/`,
  `in/UXLC-misc-fixed/`, `out/UXLC-misc/…txt`, `out/UXLC-misc/all_changes.json`), each copy
  carrying the same 5 `goerwitz.html` citations, and `doc/clc-design.md` adds 1 in prose. The four
  fragment deep links reconcile exactly: `Deuter-5-long-notes.html` has 3 and
  `Exodus-20-long-notes.html` 1.
- **The bare `/accgram/` citation is wlc-utils' `README.md:42`, and needs no external
  coordination**, Phase 10 rewriting that file anyway. Confirmed alongside it:
  `gh-pages/accgram/index.html` does not exist, so Phase 6's "that URL 404s today and that is
  correct" is measured rather than predicted.

**Nothing outside MAM-basics opens a wlc-utils data file — re-established at Phase 0 and it still
holds.** Sweeping every clone for `wlc-utils/{in,out,data,gh-pages}` paths leaves exactly two
hits, both prose in a `doc/` tree: `UXLC-utils/doc/clc-design.md` and the `hebrew-prose` skill's
tracked copy in `github-misc`. **One of them needs more than Phase 11 item 9's one sentence**,
though: `clc-design.md:300` cites `wlc-utils/data/lci_recs.json`, and Phase 3 does not merely move
that file to another repo, it **renames** it to `in/lci_recs.json` — so "every `wlc-utils/…` path
in `doc/` now means `../MAM-basics/…`" is true of `:238` and `:322` and false of `:300`.

Four decisions carried over unchanged from the Python plan: plain copy with no history graft;
regenerating the tracked artifact byte-identically is the test, with no new example-based unit
tests; issues unify going forward only; and one phase per session, written back before the next.

**One decision from the Python plan this deliberately breaks.**
`PLAN-evacuate-python-programme.md`'s carried decision 2 says "**`gh-pages/` stays put
indefinitely** in every repo that has one … Moving it would break links in the wild with no
forwarding mechanism." That was right when there was no forwarding mechanism. Phase 8 builds one.
Five of the six repos still in that programme have a `gh-pages/` and will cite this as precedent,
so Phase 11 records the break in that file explicitly rather than leaving the two documents to
contradict each other.

---

## Preconditions — all four blocking

**State as of 2026-08-11: ALL FOUR ARE MET.** 0, 1 and 3 were met at Phase 0; 2 was met later the
same day, when Ben enabled Pages. **A fifth was added by Ben that day and is the only live gate —
see "Precondition 4" at the end of this section.** Meeting 2 also created a decision this plan did
not previously have: see Phase 3's "STOP" box, since the workflow that publishes the site arrives
at Phase 3 rather than at Phase 6.

**0. The whole MAM-private programme must finish first — every phase of all four repos.**
**MET 2026-08-11.** That programme closed itself — `MAM-private` `b31215a` ("Close the
private-repo evacuation programme: the last row is done") and `5ff6a40` — and its Status table
reads DONE on every row, al-hatorah's R.4 included, which is the row this precondition names.
Checked at MAM-private head `5ff6a40`. Ben's
decision, 2026-08-08: all private work before any public work, and this plan is the first public
work after it. The programme is
`C:/Users/BenDe/GitRepos/MAM-private/doc/PLAN-evacuate-private-repos.md`; its Status table is the
check, and **this precondition is met when al-hatorah's R.4 is written back there**, not when
wlc-utils-private finishes. Numbered 0 rather than 4 so the three below keep the numbers the rest
of this file cites. The reasoning behind it, including what could safely have overlapped and why
that licence goes unused, is under "Interactions with the MAM-private programme".

**1. `wlc-utils/doc/PLAN-two-accents-on-one-chanted-word.md` must land or freeze first.** It was
live — 1209 lines by Phase 0, not the 1134 this plan first measured, §9 the current state and
Phase 4 next — and it generates accgram pages, which are members of the 154-page set this plan
proves itself against by zero diff. This is the same contention the Python plan's Precondition 2
named between itself and the maqaf-scans plan, and it was decisive there: concurrent artifact
changes mean this plan cannot tell a move bug from a page edit.

**MET 2026-08-11: Ben chose freeze**, put to him at Phase 0 with the alternatives measured. The
freeze notice is at the top of that file with a pointer from its §0, wlc-utils `c501dc0`, and it
says the freeze lifts at this plan's Phase 11. **A later session must not land that plan
mid-evacuation.**

**READ THIS BEFORE DOING ANYTHING ABOUT THAT PLAN — it is not a task, and this precondition
generates no work.** What is dangerous is that plan being **executed** while this one runs,
because executing it regenerates accgram pages and this plan cannot then tell a move bug from a
page edit. **A plan parked in a `doc/*.md` is already harmless**, and so is an open GitHub issue:
neither runs by itself. So freezing it, closing it, or simply nobody running it all satisfy this
precondition **identically**, and the freeze is a written record of the choice rather than the
mechanism that makes it safe.

**Do not turn this into an investigation.** On 2026-08-11 a session read "land or freeze" as
licence to work out what that plan still owed, went down through its Phase 4 to MAM-basics#215,
and reported the findings as though something were owed here. Ben, the same day: *"I have no idea
why any of this holds up the evacuation plan as long as it is parked in a `doc/foo.md` and/or
GitHub issue in some repo."* He is right, and this paragraph exists so the next session does not
repeat it. **The only question this precondition ever asks is "is anyone running that plan right
now?" If no, it is met. Move on to the phase.**

**2. Pages enabled on `bdenckla/MAM-basics` — Settings → Pages → Source: GitHub Actions.** Only
Ben can do this; the plan does not attempt it. It is a hard gate on Phase 6.

**MET 2026-08-11, later the same day, by Ben. All four preconditions numbered here are now met**
(the fifth, Precondition 4 below, is the live one). The check is one command and needs no browser:

```bash
gh api repos/bdenckla/MAM-basics/pages
```

It returns `404 Not Found` while Pages is off. It now returns `"build_type": "workflow"`,
`"source": {"branch": "main", "path": "/"}` — **field for field what the same call returns for
`bdenckla/wlc-utils`**, which is the worked example of a met precondition. `"status": null` simply
means no deploy has run yet, which is correct: nothing has been pushed for one to build.

**Ben deliberately did NOT choose a workflow, and that is right — do not add one for him.** When
the Pages UI is set to "GitHub Actions" it offers starter workflows (Static HTML, Jekyll); taking
one would commit a file that **Phase 6 would then have to undo**, since Phase 6 copies wlc-utils'
`pages.yml` verbatim for its specific post-`72ba4ba` action pins. An enabled source with no
workflow file is exactly the state Phase 6 expects to find. Confirmed at Phase 0: MAM-basics has
no `.github` directory at all, tracked or on disk.

**3. Clear MAM-basics' worktrees** (two live on 2026-08-03), for the disk reason above:

```bash
.venv/Scripts/python.exe py/main_repo_util.py --clean-worktrees --workspace-file all-repos.code-workspace
```

**And clear wlc-utils' own, which are easy to forget because this plan is otherwise written from
MAM-basics.** On 2026-08-03 wlc-utils held a live worktree at
`.claude/worktrees/suspicious-nash-51747c` (detached at `61ede49`) plus its
`claude/suspicious-nash-51747c` branch. It carries **no** `.py`, so the hazard that bit
`run_black.py` — reformatting 789 pre-evacuation files inside worktrees nothing tracked — does not
apply here. Two other things do, and both land squarely on this plan:

- It is a **second full checkout of the corpus**, ~460 MB, at a commit predating everything below.
- **Phases 9 and 10 operate inside wlc-utils.** A worktree pinned to a pre-flip commit means the
  repo holds two disagreeing copies of `gh-pages/` while the redirect stubs land, and
  `git worktree remove` on Windows fails outright while any shell sits inside it.

`check_repo_standards.py:25-31` already records that wlc-utils *"goes on accruing worktrees from
agents editing its data"* and deliberately leaves its worktree counts ungated for that reason — so
expect this condition to have recurred by the time a session reads this, rather than assuming the
one named above is still the one present. The same `--clean-worktrees` sweep above reaches it,
wlc-utils being listed in `all-repos.code-workspace`.

**MET 2026-08-11 and it cost nothing: neither repo had a worktree to clear.** `git worktree list`
gave exactly one line in each — `MAM-basics d100480 [main]` and `wlc-utils 79404fa [main]` — so
the recurrence `check_repo_standards.py` predicts had not in fact recurred, and no
`--clean-worktrees` sweep was needed. Re-check rather than assuming this holds; the prediction is
still sound, it simply had not come true on the day.

**4. No other session may hold uncommitted MAM-basics work, and while holman-ketiv-qere's current
work is live, no phase of this plan runs. Ben's decision, 2026-08-11**, taken at Phase 0 on a
measurement rather than a worry — Phase 0 finding 1 below is the mechanism, and it is not the
obvious one. Nothing in holman-ketiv-qere edits MAM-basics; the mega's `vendoring-audit` step
reads **every** sibling repo, so a sibling merely *gaining a vendored file* drifts four tracked
MAM-basics artifacts on the next run. That defeats the "git status shows only this phase's source
edits" assertion Phases 3, 5 and 10 each rest on. Ben was offered the cheaper option — let it run,
and re-audit-and-commit at each phase — and chose the strict serialization the MAM-private
programme used instead: **finish holman-ketiv-qere first.** Check with `git -C
../holman-ketiv-qere status --porcelain` and its recent log before starting any phase.

**Check MAM-basics' own log too — the sibling's is not the whole picture.** Phase 2 found on
2026-08-12 that the holman-ketiv-qere work commits into *this* repo as well, interleaved with that
repo's commits to the minute, and that its latest activity was here rather than there. The two
checks together are the gate; the sibling's log alone read an hour and a half stale. Phase 2's
finding 2 has the timestamps. **Ben answers the question either way** — whether the work is
finished is his to say, not something the logs settle.

**Re-measure wlc-utils' baseline rather than trusting this file's figures.** Its HEAD was
`5783062` when the counts under Scale were taken, `3760b2f` a few hours later, and `79404fa` when
Phase 0 began on 2026-08-11 — so that repo moves under this plan exactly as the Python plan's own
final session found.

---

## Interactions with the MAM-private programme — recorded on both sides

`C:/Users/BenDe/GitRepos/MAM-private/doc/PLAN-evacuate-private-repos.md`, written 2026-08-07,
evacuates masorah-books, al-hatorah, wlc-utils-private and mgketer into `bdenckla/MAM-private`.
It carries a section titled "Interactions with the wlc-rest plan — recorded on both sides"; this
is the corresponding note on this side. First written 2026-08-08 against that plan's original
blanket rule ("never interleaved with the wlc-rest plan's phases"); rewritten later the same
day, after that plan's `57fb4a3` replaced the blanket rule with a traced three-tier one and
corrected a provenance claim this note had copied from its first draft.

**The overlap rule, mirrored from that plan's Sequencing section — three tiers, by which of its
four repos is in play:**

- **wlc-utils-private: never overlap with any phase of this plan.** The tie is
  `py/main_wlc_json_and_unicode.py`, which splits its output between two roots (`:57`, `:65`):
  `_PRIVATE` is wlc-utils-private, `_PUBLIC` is public wlc-utils today — this repo after Phase
  5. That one generator is both wlc-utils-private's layer-2 oracle and the
  `wlc-json-and-unicode` step of this plan's circuit (`main_0_mega.py:253`), so each programme's
  zero-diff and zero-mtime verifications measure trees the other's oracle rewrites. That plan's
  hard tier names Phases 3, 5 and 10 here as the sharpest cases — dual residency's frozen
  reference, the zero-mtime snapshot over wlc-utils, the emptying — but from this side the
  honest statement is broader: Phases 0, 1 and 10 run the circuit too, and Phases 9 and 10 edit
  wlc-utils, which that oracle requires clean as its fourth precondition. Only Phases 2, 4, 7
  and 8 are genuinely inert toward that repo, and scheduling around so fine a distinction buys
  nothing. **Treat it as repo-level: while wlc-utils-private is mid-evacuation there, no phase
  runs here, and vice versa.**
- **al-hatorah: its R.2 must not overlap Phase 5.** Both edit the same block of sibling
  accessors in `py/wlc_paths.py`, and both run this repo's suite and read its pass count.
  Sequence them, either way around.
- **mgketer and masorah-books: free to interleave, under one scheduling rule.** The only
  coupling is that both programmes assert a clean `git status --porcelain` in MAM-basics — and
  mgketer's and al-hatorah's R.3 commit MAM-basics-side vendoring-policy edits — so two sessions
  must not hold uncommitted MAM-basics work at the same time. That is scheduling, not
  correctness: those repos' oracles touch their own trees and read MAM-parsed, never wlc-utils.

**The scheduling question that plan puts to Ben, restated so both plans carry it.**
wlc-utils-private is sequenced first there because it is smallest — and it is also the one repo
that locks this plan out entirely, so "smallest first" and "unblock this plan soonest" pull
opposite ways. Either wlc-utils-private runs R.0–R.4 straight through before this plan advances
past Phase 0, or it moves to last in that programme's order and this plan runs now, with mgketer
and masorah-books free to interleave meanwhile. There is also a case for this plan going first
outright: after Phase 5 the shared generator's `_PUBLIC` half writes into this repo, and after
Phase 10 public wlc-utils holds only stubs — so wlc-utils-private's oracle loses its
fourth-precondition write target and its move gets simpler. **Settled by Ben, 2026-08-08:
wlc-utils-private runs R.0–R.4 straight through, first, by itself — as one unit, with nothing
in parallel, not even a phase of this plan. This plan waits.** (This paragraph first ended
"and resumes at Phase 0 once that repo's R.4 write-back lands"; Ben superseded that the same
day with the whole-programme ordering two paragraphs down — the wait is longer than one
repo.) That plan's `22e7e7f` records the same settlement, scopes the
one-unit run as the single exception to its one-phase-per-session discipline, and closes three
of its gates so the run cannot stall midway. The paragraph above stands as the record of the
alternatives not taken.

**Ben, 2026-08-08, later the same day: the two programmes run strictly serially, as whole
blocks — the interleaving the tiers above license goes deliberately unused.** The coordination
that interleaving would need was judged delicate and error-prone on both sides. The order,
stated by Ben in full: **all private work first — the whole MAM-private programme, all four
repos — before any public work, and the first public work is this plan.** So this plan's Phase
0 waits for al-hatorah's R.4, not for wlc-utils-private's. (This paragraph first read
"wlc-utils-private, then this plan complete, then the remaining three MAM-private repos" — an
inference from the morning's unblock-wlc-rest rationale that Ben corrected the same day:
slotting this plan in mid-programme is itself the interleaving being declined.) No mgketer or
masorah-books phase runs as filler during this plan's manual gates. The three-tier analysis
above stands as the record of what *could* overlap safely — it is reasoning, not schedule.

**Owed to the other side, and not yet paid: MAM-private's plan does not carry this
serialization.** Its file was held by the live wlc-utils-private session when the decision was
made on 2026-08-08, so it still reads as though the tiers govern and as though this plan resumes
after wlc-utils-private. **The first MAM-private session that finds the file free should add
the mirror**: the two programmes run as whole blocks; the whole of that programme precedes any
phase of this one; and the chip its last repo's R.4 spawns is this plan's Phase 0. Until that
lands, the two plans disagree about the order, and **this file is the one Ben stated it to.**

**One consequence for this plan's own verifications, visible from Phase 0 onward:** once that
move lands, `wlc-json-and-unicode` writes its `_PRIVATE` half into
`MAM-private/wlc-utils-private/`, so every "zero diff in both repos" assertion here extends to
a third tree — require MAM-private clean before each circuit run and unchanged after it, except
where a phase's own edits explain the diff.

Two entanglements outlive the contention, and no amount of scheduling removes them:

1. **Phase 5 moves two accessors that plan repoints.** `wlc_utils_private_dir`
   (`py/wlc_paths.py:146`) and `al_hatorah_phonetic_dir` (`:159`, with
   `require_al_hatorah_phonetic_dir` at `:170`) leave `py/wlc_paths.py` for `mb_cmn/paths.py`
   here, and that plan's R.2 for wlc-utils-private and for al-hatorah rewrites exactly those.
   Both sit inside the "14 live sibling accessors" range Phase 5's table moves verbatim —
   verified 2026-08-08, between `mam_simple_dir` at `:109` and `require_uxlc_utils_dir` at
   `:179`, checked because the table elided the fourteen names behind an ellipsis; the table now
   names these two. **Whichever programme executes second finds them in the other file — locate
   them by function name, never by path.**
2. **Phase 11 and that plan's R.4 edit the same two unsynced pairs of files** — the live
   `~/.claude/CLAUDE.md` with its tracked twin at `github-misc/dot-claude/CLAUDE.md`, and the
   live `~/.claude/skills/hebrew-prose/` with its tracked twin at
   `github-misc/dot-claude/skills/hebrew-prose/`. Neither pair syncs, both programmes flag their
   edits stop-and-ask-Ben, and two sessions editing one unsynced pair is precisely how a copy
   goes stale unnoticed. Whichever runs second re-verifies both pairs byte-identical before
   adding to them.

**A third entanglement was recorded here on 2026-08-08 and withdrawn the same day.** This note's
first version claimed that Phase 1's expectation of retiring al-hatorah's `aht_provenance.py`
wrapper is void once al-hatorah nests under MAM-private, "whose origin basename is
`MAM-private`". That plan's `57fb4a3` corrected the claim by reading the code:
`mb_cmn/provenance.py`'s `_display_path` walks a fixed `parents[2]`, so a vendored copy at
`MAM-private/al-hatorah/py/mb_cmn/` lands on a directory still named `al-hatorah`, and the
breadcrumb stays right with no override. Nor does Phase 1's step 2 change that when it lands:
the derivation chain reads `repo_root/.git`, which for a tree nested inside MAM-private does not
exist, so the chain degrades to `repo_root.name` — `al-hatorah`, the right answer. The exposure
would need a derivation that walks *up* to MAM-private's `.git`, which Phase 1's chain
deliberately does not do. What the correctness actually depends on — the vendored copy sitting
exactly two levels below its tree root — is verified at that plan's R.2 rather than assumed.

One thing this plan hands that plan rather than owes it: **`wlc-utils/doc/` moves into
`MAM-basics/doc/` at Phase 3**, and that plan's prose table cites
`wlc-utils/doc/PLAN-two-accents-on-one-chanted-word.md` for its masorah-books path references. It
already says to repoint that file wherever it lives at execution time, so nothing is owed —
recorded here so a Phase 3 session does not read the moved file as breakage.

---

## The organizing idea: the two roots rejoin

The Python evacuation split one `repo_root()` into a CODE root and a DATA root, and
`py/wlc_paths.py`'s module docstring is the statement of that split: *"THIS MODULE IS DELIBERATELY
TWO-ROOTED, and that is the whole point of its existence."*

**This plan rejoins them.** Afterwards `wlc_data_root()` and `paths.repo_root()` name the same
directory, so `py/wlc_paths.py` has no reason to exist, and the only thing left pointing at
wlc-utils is one `sibling_repo("wlc-utils")` call inside the redirect-stub generator.

Everything awkward dissolves rather than moves: the `.novc/` split, `gen_highlight_picker`'s
`../gh-pages/` relative-URL constraint, `main_repo_maintenance.py:110`'s wipe of a foreign scratch
dir, and the seven test modules that reach into a sibling. `mb_cmn/paths.py`'s `REPOS_ROOT` /
`REPO_<NAME>_DIR` override chain stays — it still serves MAM-parsed, MAM-simple, MAM-with-doc,
MAM-OSIS, UXLC-utils and al-hatorah — but it stops being load-bearing for wlc-utils, which is the
sibling a worktree session actually contended over.

**DONE 2026-08-12, and every clause of it held except one.** `py/wlc_paths.py` is deleted, its
docstring's two-rooted statement with it, and the four awkward things above dissolved as predicted.
The exception is the test modules: **eight, not seven** — the list further down under Phase 5 names
eight and this paragraph says seven — and one of them, `test_h_dot_below_nfc.py`'s wlc-utils NFC
scope, still reaches into the sibling by Phase 5's own instruction to leave it for Phase 10. It is a
read, and the assertion this section exists to make was tested directly and held: a full circuit run
touched **zero** files in wlc-utils.

**The one call this section predicts was built on 2026-08-13** — `py/wlc_redirect/stubs.py`'s
`wlc_utils_pages_dir`, which is `paths.require_sibling("wlc-utils", paths.sibling_repo("wlc-utils"))`
plus `/ "gh-pages"`, and is the only place in the tree that resolves the real clone for any purpose
but a test. It is reached by `main_wlc_redirect_stubs.py check` with no `--dir` and by
`build --publish`, and by nothing else, so it does not disturb the zero-files-touched result above.
Phase 8's finding 1 disposes of all three sites naming that sibling, one of which is not a
resolution and must survive Phase 10.

---

## The oracle question: what replaces "copy, don't move"

The Python plan's Phase 3 had an independent oracle because two copies of the code wrote the same
artifacts. **Data cannot be run twice.** Three layers replace it, and each covers exactly what
the others cannot.

**Layer 1 — blob-hash manifest identity, which proves the copy.** `git ls-files -s` in wlc-utils
yields 626 rows of `<mode> <sha1> 0/t<path>`. After the copy the same command in MAM-basics,
restricted to the destination paths, must yield **the identical 626 SHA-1s**, differing only in
path. Git blobs are content-addressed, so this is exact byte-identity — and it is the *only*
evidence covering the 122 PNGs, 2 JPGs, 2 PDFs, the woff2 and the extensionless
`in/Tanach-26.0--UXLC-1.0--2020-04-01/Images/Background`, which no program regenerates and which
layer 2 therefore says nothing about. Exactly two path deltas are expected: the `gh-pages/` →
`gh-pages/wlc/` prefix on 284 files, and `data/lci_recs.json` → `in/lci_recs.json`.

**This is why Phase 2 must precede Phase 3**: `git add` applies `.gitattributes` at add time, and
a differing eol rule changes the blob.

**Layer 2 — zero regeneration diff, which proves the repoint.** After Phase 5, run the full
circuit from `C:/Users/BenDe/GitRepos/MAM-basics`. **THE CIRCUIT IS NOW TWO COMMANDS, NOT ELEVEN
— re-measured at Phase 0, 2026-08-11, and this correction governs Phases 3, 5 and 10, each of
which cites the old list.**

```bash
.venv/Scripts/python.exe py/main_0_mega.py
```

```bash
.venv/Scripts/python.exe py/main_edition_transcription.py build --check
```

The mega's wlc half is the `_STEPS` run from `wlc-vendor-uxlc` through `wlc-a-notes`, and it has
**absorbed all eight of the steps this plan listed as sitting outside it** — the six accgram
subcommands (`accgram-run-dual-cant`, `accgram-xcheck-poetic`, `accgram-servi-xcheck`,
`accgram-grammaticality`, `accgram-run-printed-decalogue`, `accgram-survey-chanted-word-accents`)
plus `find-uxlc-accent-changes` and `uxlc-grammar-test`. wlc-utils `505cbfc`, "Wake two artifacts
the mega now rebuilds, and record the eight new steps", is where that happened.
`main_edition_transcription.py build --check` is the only thing still outside, and
`--resume-from`'s own choices list is the authority — read it rather than this paragraph if the
two ever disagree:

```bash
.venv/Scripts/python.exe py/main_0_mega.py --help
```

**This retires, rather than merely simplifying, the specific staleness this plan warned about.**
Phase 0's text says `main_find_uxlc_accent_changes.py` and `main_uxlc_grammar_test.py` "sit
outside the mega, so nothing rewrites them routinely — which is exactly how
`out/accgram/uxlc_grammar_test.txt` was found two days stale during the Python plan's Phase 1."
Both are mega steps now, so that particular trap is closed.

`git status --porcelain` then shows **only the phase's source edits** — in MAM-basics, wlc-utils,
and the seven other repos the circuit writes.

**Layer 3 — mtime counter-checks, in both directions.** The UXLC-utils Phase 3 record's lesson —
*"count what a run actually rewrites, not what it leaves clean"* — does double duty here.

- *In MAM-basics*: snapshot mtimes before, compare after. Expect roughly **111 files not
  rewritten** — the 73 static assets under `gh-pages/wlc/accgram/` (3 `.js`, 69 `.png`, 1 `.jpg`)
  and the 38 under `out/accgram/goerwitz-stderr/`, captured stderr from the original C checker
  that no Python writes — plus the remaining images. Say which files are proved by layer 2 and
  which only by layer 1; an empty `git status` over files nothing writes is not a claim.
- *In wlc-utils*: snapshot mtimes before, compare after. **Zero files touched.** This is the
  sharpest assertion in the plan and the direct test of the collision fix. An empty `git status`
  there proves nothing — a call site that still points at wlc-utils rewrites a file to *identical*
  bytes, which git cannot see and mtime can.

**And the frozen reference is the original tree — but only the part of it Phase 9 did not
overwrite.** `out/` 193, `in/` 135, `doc/` 6, `data/` 1 and the Pages workflow are files no program
writes any more, so `git diff --no-index` between the trees re-derives layer 1 over those **336** of
the 620 moved files, on demand, until Phase 10 deletes them. **`gh-pages/` stopped being a reference
on 2026-08-17**: Phase 9 replaced all 154 pages there with redirect stubs and deleted the 130
assets, so a `diff --no-index` over that subtree now reports 154 differences which are the flip
rather than move damage. (This paragraph read "wlc-utils holds 626 files no program writes any more,
so `git diff --no-index` between the trees re-derives layer 1 on demand at any point in Phases 3–9"
— right for Phases 3 through 8, and falsified by Phase 9, which is the phase it named last. Phase
9's finding 2.) **Phase 10 spent what remained on 2026-08-17**: layer 1 was re-derived over all 336
comparable files in the minutes before the delete — 330 byte-identical, the 6 differing exactly
Phase 5's six — and then the 335 moved ones among them were deleted, so nothing original is left to
compare against. The Pages workflow is the one comparable file that survives, still byte-identical
to the copy here.

---

## Phase 0 — Preflight: baseline, manifest, collision census — DONE 2026-08-11

*Read-only, plus one commit to this plan file.* No tracked artifact changes.

**That description held for the reading and did not survive the baseline.** Phase 0 turned out to
need **five** commits across five repos, because the circuit it runs to establish a clean baseline
found the baseline dirty. The execution record at the end of this section says which and why.

**Re-measure and record** the table under Scale, plus: `py/main_test.py` — **913 passed, 5
skipped, 57 subtests** on 2026-08-03; `ruff check py`; `black --check py`.

**Capture the 626-row manifest** — `git ls-files -s` in wlc-utils — into `.novc/`, recording its
hash in this file. It is layer 1's before-image and there is no second chance to take it.

**Run the full circuit once from the current state and require a zero diff in both repos.** A
baseline already dirty makes every later phase unjudgeable. Two known ways it goes stale:
`main_find_uxlc_accent_changes.py` and `main_uxlc_grammar_test.py` sit outside the mega, so
nothing rewrites them routinely — which is exactly how `out/accgram/uxlc_grammar_test.txt` was
found two days stale during the Python plan's Phase 1.

**Then the collision census.** Directory-level collisions were checked on 2026-08-03 and there
are none: wlc's `in/` (`Tanach-26.0--UXLC-1.0--2020-04-01`, `UXLC-39`, `UXLC-misc`, `accgram`,
`wlc420`, `wlc422`) and MAM-basics' (`chabad-ctr`, `mam-from-sefaria`,
`mam-from-Sefaria-2021-11-23`, `mam-go`, `mam-ws`, `mam-ws-bot-edits`) are disjoint, as are the
two `out/` sets and the two `doc/` sets. wlc-utils has **no loose files at `in/` top level** and
two at `out/` (`diff_mm_wlc420_wlc422.json`, `diff_mx_wlc420_uxlc.json`), neither colliding. So
**a flat merge works with zero renames**, matching the Python plan's "flat namespacing, minimal
renames". Re-confirm with `comm` over both flat listings rather than trusting this paragraph.

Two census findings already in hand, neither a blocker:

- **`wlc-utils/gh-pages/woff2/Taamey_D.woff2` and `MAM-basics/doc/woff2/Taamey_D.woff2` are
  byte-identical.** Different paths, so no collision, but the repo will hold two copies of one
  font. Out of scope — file an issue, do not fold a deduplication into a move.
- **wlc-utils has no `.csv` files**, so MAM-basics' `*.csv text eol=crlf` rule cannot bite the
  incoming tree. This retires a hazard rather than raising one.

**The six root files cannot simply be copied** — `README.md`, `CLAUDE.md`, `LICENSE`,
`.gitignore`, `.gitattributes` exist in both repos, so "everything travels" means ~620 files, not
626. Disposition:

| File | Disposition |
|---|---|
| `.gitattributes` | merge — Phase 2 |
| `.gitignore` | wlc's only line is `.novc/`, which MAM-basics already ignores. **No edit.** |
| `LICENSE` | **The two differ, and not by drift: wlc-utils is CC0 1.0, MAM-basics is GPL-3.0.** Phase 4. |
| `CLAUDE.md` | wlc's residue is the `agent-planning-principles.md` pointer (Phase 11) and the "there is no `wlc-koren-12th` repo" note (fold into MAM-basics' `CLAUDE.md`). |
| `README.md` | rewritten in place in Phase 10, not copied |
| `wlc-utils.code-workspace` | **the one exception to "everything travels" — delete, don't move.** It is four lines (`{"folders":[{"path":"."}]}`); a `wlc-utils.code-workspace` sitting inside MAM-basics beside `MAM-basics.code-workspace` and `all-repos.code-workspace` is noise, and the workspace it describes still exists in wlc-utils. |

**Verify:** every count recorded; the circuit gives a zero diff in both repos; the census produces
a written collision list.

### Execution record — Phase 0, 2026-08-11

Began at wlc-utils `79404fa`, MAM-basics `d100480`, with all nine repos the circuit touches at
`git status --porcelain` empty. Preconditions 0, 1 and 3 met (see that section); 2 open and
gating Phase 6 only.

**The manifest — layer 1's before-image — was taken twice, and the second one is the live one.**
`.novc/wlc-rest-phase0/wlc-manifest-c501dc0.txt`, **626 rows**, sha256
`28c94cde461849fbffd53ac16de12a6d9f4eb1804a9ce95e1baa212ea51c1ade`. The first was taken at
`79404fa` (sha256 `b4169ae8a82ebb62fa87fd71b98f31fb4f82e231efcc091f89b4d37ab7583ae5`) and was
invalidated within the hour by this phase's **own** freeze commit, `doc/PLAN-two-accents-…md`
being one of the 626. The two differ in **exactly one row**, that file's blob, proved by `diff`
and kept in `.novc/` beside it. **The lesson for a later phase is that "no second chance to take
it" is about the corpus moving, not about the head moving** — while wlc-utils is untouched by any
copy, the manifest can simply be re-taken, and a phase that edits that repo at all must re-take it
rather than reason about the delta.

**The circuit ran green: exit 0, and `main_edition_transcription.py build --check` passes 12/12.**
The assertion this plan cares most about held on the first run — **wlc-utils came through with
zero files changed**.

**But the baseline was NOT clean: 17 files across three repos, from three unrelated causes**, all
committed before this phase was written back. Ben chose "three separate commits" from three
options put to him.

| Repo | Files | Cause | Commit |
|---|---|---|---|
| MAM-parsed | 12 SVGs | **Graphviz 14.1.2 → 15.1.1** | `95f64d7` |
| MAM-basics | 4 | the vendoring audit, finding 1 below | `5344a74` |
| MAM-with-doc | 1 | `unpinned-latest.html`, drifting by design | `518b08d` |

The Graphviz bump is a **real layout change and not just the version stamp** — `plain-call-graph-c`
goes 201pt wide to 215pt, and every polygon and path coordinate moves. It is nonetheless
output-neutral in the sense that matters, proved rather than assumed: all twelve have an
**identical set of `<title>` elements before and after**, so the same nodes and the same edges are
drawn, and every diff is balanced, the same number of lines out as in. `unpinned-latest.html` still
reports "0 changes found"; only its dates moved, 2026-08-02 to 2026-08-09, tracking MAM-parsed's
head rather than the calendar.

#### Findings

**1. A sibling repo's vendoring drifts THIS repo's tracked tree, with no session here touching
anything. This is the finding that changed the plan** — it is why Precondition 4 exists.
holman-ketiv-qere `e2d1f17` vendored `mb_cmn/paths.py` into itself; the mega's **`vendoring-audit`
step reads every sibling repo**, so MAM-basics' `doc/vendoring-inventory.md` and its three
`out/vendoring_*` artifacts went stale, 154 files to 155. **The direction is the counter-intuitive
part**: the danger is not another session writing into MAM-basics, which no
holman-ketiv-qere session does, but this repo's own audit reaching out and noticing. Any phase
asserting "git status shows only my source edits" can be defeated by a sibling repo it never
mentions.

**2. The circuit collapsed from eleven commands to two**, retiring a staleness trap this plan
names. Recorded in full under layer 2 above, since that is where the step list a later phase reads
actually lives.

**3. The suite is 903 passed / 5 skipped, not the 913 / 5 / 57 subtests this plan carried.**
Independently corroborated: MAM-private's programme measured 903 at al-hatorah's R.3 and R.4 and
accounted for the missing test exactly. `ruff check py` clean; `black --check py` clean at 771
files. **903 is the baseline every later phase compares against.**

**Everything the census claimed reproduces, with no exceptions.** The load-bearing figure is
intact — **zero** absolute `bdenckla.github.io/wlc-utils` self-links anywhere under `gh-pages/`,
so the 284-file subtree still moves with no HTML edits at either layout. Also re-confirmed: zero
directory-level collisions across `in/`, `out/` and `doc/`, by `comm` over both flat listings, so
a flat merge still needs zero renames; MAM-basics has neither a `gh-pages/` nor a `.github/`, so
both arrive whole; wlc-utils has no loose file at `in/` top level and exactly the two named at
`out/`; wlc-utils has **0** `.csv`, so MAM-basics' `*.csv text eol=crlf` rule cannot bite; and the
two `Taamey_D.woff2` copies really are byte-identical, sha256 `5cc8df8a…`, so the repo will hold
one font twice — still out of scope, still an issue to file rather than a deduplication to fold
into a move.

**The six root files check out as the disposition table says, with one trivial correction.**
`.gitignore` in wlc-utils is the single line `.novc/`, which MAM-basics already ignores, so no
edit; the two `LICENSE` files differ as stated, wlc-utils' opening "Creative Commons Legal Code"
against MAM-basics' GPL-3.0; wlc-utils' `CLAUDE.md` has five sections, of which the two the table
predicts as residue are present. The correction: **`wlc-utils.code-workspace` is 7 lines, not
4** — the same `{"folders":[{"path":"."}]}` content, pretty-printed. It is still the one file to
delete rather than move.

**Two things banked for Phase 11 while they were cheap to check.** Both unsynced live-plus-tracked
pairs are **byte-identical right now** — `~/.claude/CLAUDE.md` against
`github-misc/dot-claude/CLAUDE.md`, and `~/.claude/skills/hebrew-prose/` against
`github-misc/dot-claude/skills/hebrew-prose/` — which is the state Phase 11 item 3 requires
verifying before it adds to either. And **Phase 11 item 2 understates its own work**: the global
`CLAUDE.md` has **19** wlc-utils references, not the two `agent-planning-principles.md` citations
the item names. Two more go stale from *this* plan — the `file:///…/wlc-utils/gh-pages/accgram/`
link at `:711` and `wlc-utils/doc/edition-transcription-workflow.md` at `:741` — and **six are
already stale today**, naming `wlc-utils/py/...` paths that the 2026-08-01 Python evacuation moved
and nobody has repointed since. Those six are not this plan's to fix and are flagged, not folded
in.

---

## Phase 1 — The provenance worktree fix — DONE 2026-08-11

*In MAM-basics, plus a re-vendor ripple.* Independently valuable, and **a precondition of the
oracle** rather than bookkeeping.

`py/mb_cmn/provenance.py:81` computes `repo_root = Path(__file__).resolve().parents[2]` and `:82`
takes `repo_root.name`, so a run from a worktree stamps `affectionate-robinson-235a9e/py/accgram/…`
into every generated file. Today that is avoided by regenerating from the main clone, and the
docstring at `:73-78` says so: *"regenerating from a worktree writes the worktree's name, exactly
as it always has for every other repo this one generates into."*

**That sentence stops being acceptable here.** Today a worktree run poisons 61 breadcrumbs in a
*sibling* repo. After Phase 3 those 61 artifacts live in this tree, so a worktree run produces a
wrong breadcrumb **and 61 spurious tracked diffs in your own `git status`** — at the exact moment
every phase's verification is "the diff is nothing". If a worktree is to become the normal place
to regenerate, which is the whole point of the plan, this has to be answered rather than
side-stepped.

**The fix is pure file I/O**, every step verified 2026-08-03 on a live worktree. Leave
`_display_path`'s own `parents[2]` walk alone rather than routing it through `paths.repo_root()`:
`provenance.py` is deliberately self-contained because it is vendored, and `CLAUDE.md` names it in
the exception list for exactly that reason. `actual_name` also stays `repo_root.name` — it is
matched against a real filesystem path in the `repos_rel.startswith(prefix)` branch and must keep
naming the directory. **Only `logical_name`'s default changes**, from `actual_name` to a name
derived by this chain, stdlib `pathlib` only, no `subprocess` and no `git` on PATH:

1. **The common git dir.** `repo_root/.git` a directory → itself. A file → read its single
   `gitdir:` line (in this repo's worktree,
   `gitdir: C:/Users/BenDe/GitRepos/MAM-basics/.git/worktrees/<name>`), then apply the `commondir`
   file inside it if present — contents `../..` — to land on `<main clone>/.git`.
2. **`remote.origin.url` basename**, with a trailing `.git` stripped.
3. **The common git dir's parent name**, but only when that dir is literally named `.git`. Covers
   a worktree with no origin. The guard matters: a submodule's `.git` file points into
   `<super>/.git/modules/<name>`, whose parent is `modules`.
4. **`repo_root.name`** — today's behaviour, unchanged.

**Step 2 is the one this plan did not originally have, and it earns its place twice over.** It is
the only step that also fixes a clone whose **directory was renamed**, which Ben raised explicitly;
and it costs no subprocess, because `.git/config` is a plain tab-indented file — `[remote "origin"]`
then `/turl = https://github.com/bdenckla/MAM-basics.git`, confirmed by `cat -A` — so an eight-line
hand-scan beats `configparser`, whose continuation-line handling of tab-indented bodies is a
liability here. **Ben's remotes are inconsistent about the suffix** — MAM-basics, al-hatorah,
MAM-parsed, MAM-with-doc, MAM-OSIS, MAM-for-Sefaria and UXLC-utils carry `.git`; MAM-simple and
wlc-utils do not — so stripping it is required rather than defensive.

**Failure degrades, never raises.** The whole derivation sits under one `except Exception`
returning `repo_root.name`, so a malformed `.git` file, an unreadable config, or a bare or exported
tree with no `.git` at all reproduces exactly today's output rather than exploding several hundred
files into a full regeneration. The existing `ValueError` for a generator path outside both roots
is a *different* contract and stays as is. Memoize on the resolved repo root: a full
`main_0_mega.py` run calls `generated_by_text` thousands of times and should read the config once.

**Keep `repo_name` as an explicit override** on all five public functions and on `_display_path`.
al-hatorah's copy is refreshed by *its own* `py/main_update_vendored_files.py`, on whatever
schedule Ben runs it, so the parameter has to keep working across the window between MAM-basics
changing and al-hatorah pulling; it is also the escape hatch when the derivation is wrong. Rewrite
the `:73-78` paragraph — it becomes false, so it must be replaced, not appended to.

**Why this is output-neutral**, and the check on it: origin basename equals the directory name in
all nine repos checked, and every existing breadcrumb already carries the name the chain derives.
Census by `git grep -h -F "This file was generated by "` per repo, 2026-08-03 — `MAM-basics/` ×457
(MAM-simple 218, MAM-with-doc 104, wlc-utils 62, MAM-parsed 34, MAM-basics 34, MAM-for-Sefaria 4,
MAM-OSIS 1), `MAM-simple/` ×2 (the vendored generator running in place), `al-hatorah/` ×3 (via its
`REPO_NAME` wrapper), plus one `logical-name/` test fixture. Re-measure rather than trusting these.

**`provenance.py` is vendored into exactly two places**, `MAM-simple/py-examples/mb_cmn/` and
`al-hatorah/py/mb_cmn/`, both byte-identical to source on 2026-08-03. This plan said three and
named UXLC-utils, which has no copy. **The two refresh by different mechanisms and cannot land in
one commit.** There is no `MAM-basics/py/main_update_vendored_files.py` — MAM-basics is the source,
and the pull-side scripts live in the destination repos. MAM-simple's copy refreshes *inside the
mega run*, `py/py_misc/mam_simple_copy_py_files.py` listing `mb_cmn/provenance.py` among its
support files and `main_mam_simple` being in `main_0_mega.py`, so it is the one tracked file that
legitimately moves. al-hatorah pulls with its own script, on Ben's schedule, in its own commit —
which is what the surviving `repo_name` override is for.

**The existing provenance tests are tautologies, and repairing them is part of this phase.**
`py/tests/test_mb_cmn_provenance.py`'s `_repo_name()` helper returns `paths.repo_root().name`,
i.e. the same directory name `_display_path` uses — so five of its nine tests compare the function
against its own input and pass green in a worktree while the behaviour is wrong. Pinning the
literal `"MAM-basics"` is what turns them into assertions; that file is never vendored, so the
literal is safe. `test_repo_name_omitted_uses_directory_name` states the very behaviour being
removed and wants renaming with it.

**al-hatorah's wrapper can then retire — a separate repo, a separate commit, and only after that
repo has pulled the new vendored copy.** That repo works around this very bug today:
`py/aht_provenance.py` is three one-line wrappers that pass `repo_paths.REPO_NAME` to the vendored
`provenance` functions, and its two call sites —
`py/override_diff_viewer/generator.py:11` and `py/override_diff_viewer/view_model.py:13` — import
it as `provenance`. Once the derivation lands there, all three swap back to
`from mb_cmn import provenance` and the wrapper file goes. Do **not** delete
`repo_paths.REPO_NAME` in the same breath: `view_model.py:102-105` uses it directly, outside
`provenance`, to format its own paths. That line has the same worktree bug and the same available
fix, but it is al-hatorah's business and a third commit at most; `repo_paths.py:31`'s comment
*"Supplied to mb_cmn.provenance by the aht_provenance wrapper"* goes stale with the wrapper and
needs a line. Verified present in al-hatorah on 2026-08-03; re-check before acting.

**Verify:** (a) the full circuit from the **main checkout** gives a zero artifact diff, proving
the fallback path is untouched — with `git status --short` recorded in all seven repos first,
since they share a data root with no isolation and a concurrent session was seen writing it on
2026-08-03; (b) one breadcrumb-writing generator — `py/main_wlc_a_notes.py` — run from a throwaway
worktree with `REPOS_ROOT` set, and the breadcrumb reads `MAM-basics/py/…`, which is impossible
today. Do **not** attempt the whole suite from a worktree: **13** failures there are not real, and
they are the `../MAM-parsed` half only (MAM-basics#216) — the other four are the doc tests this
phase fixes, and their going green is the sharpest signal that it worked.

**Verification (b) above is stale in both of its halves — see finding 1 below — and its "13
failures there are not real" is measured false: a worktree run gives ZERO failures, see finding
7.** The paragraph is left as written because the execution record has to be readable against what
it was checking. What survives of it is the narrow instruction not to spend this phase's
verification on a worktree suite run, which is sound and is not the same claim as any of the three
just contradicted.

### Execution record — Phase 1, 2026-08-11

Began at MAM-basics `1619de2`, wlc-utils `c501dc0`, with all ten repos the circuit touches at
`git status --porcelain` empty and `git worktree list` one line in each. **Precondition 4, the
only live gate, was clear**: holman-ketiv-qere clean, fully pushed at `278f478`, no worktree, its
last commit `278f478` at 10:08 that morning and nothing since — about nine hours idle when this
phase began at 19:06.

**Every Phase 0 figure reproduced, re-measured rather than trusted.** The suite is **903 passed /
5 skipped** (plus 57 subtests) before and after; `ruff check py` clean; `black --check py` clean
at 771 files; and wlc-utils' manifest re-taken at 626 rows with sha256
`28c94cde461849fbffd53ac16de12a6d9f4eb1804a9ce95e1baa212ea51c1ade`, byte-identical to Phase 0's,
so no re-take was owed. **wlc-utils ends this phase where it began, at `c501dc0`.**

**The circuit ran green from the main checkout**: `main_0_mega.py` exit 0 and
`main_edition_transcription.py build --check` 12/12. **wlc-utils came through with zero files
changed** — checked again after the worktree probe below, which writes into it.

Seven commits across four repos, in this order:

| Repo | Commit | What |
|---|---|---|
| MAM-basics | `0008eb8` | step 2 of the chain, and the tautology-test repairs |
| MAM-private | `c0540e5` | al-hatorah pulls the new vendored `provenance.py` |
| MAM-private | `20dfb63` | `aht_provenance.py` retired, `REPO_NAME` kept |
| MAM-simple | `bae0bff` | takes the copy the mega re-vendored |
| MAM-basics | `1097530` | re-audit vendoring |
| MAM-basics | `57b83cf` | audit tail, after MAM-simple's commit moved a date |
| MAM-with-doc | `d2dc6e5` | `unpinned-latest.html`, drifting by design |

#### Findings

**1. Verification (b) was stale and tested the wrong thing, in both of its halves.** It says the
breadcrumb reading `MAM-basics/py/…` from a worktree is "impossible today". That stopped being
true on 2026-08-07: `38a3bc7`'s `_main_clone_name` walks the `gitdir:` pointer's parents for a
`.git` component and already returned `MAM-basics` for a worktree, so **the worktree probe passes
identically before and after this phase** and demonstrates no regression rather than the new
behaviour. And the generator it names, **`py/main_wlc_a_notes.py`, writes no provenance breadcrumb
at all** — `grep` for "generated by" across `gh-pages/wlc-a-notes/` finds nothing, so there was
never anything there for a worktree name to poison. The probe was re-run with a generator that
does write one: `py/main_accgram.py survey-chanted-word-accents`, whose
`out/accgram/chanted-word-accents.json` carries `MAM-basics/py/accgram/chanted_word_accents.py`.
Run from a worktree named `phase1-probe`, it rewrote that file (mtime moved) and the breadcrumb
was unchanged, wlc-utils staying clean. **All 62 breadcrumbs wlc-utils holds come from
`py/accgram/` generators** — 37 of them from `prose_run` alone — so an accgram subcommand is what
a later phase should reach for, not `main_wlc_a_notes.py`.

**2. So step 2 needed a probe of its own, and what it needs is a checkout whose DIRECTORY NAME
differs from the repo's** — which no checkout on this machine has, since a worktree is covered by
steps 1 and 3. The shapes were built instead, in the throwaway
`.novc/phase1_probe_origin_basename.py`, which copies `provenance.py` into fabricated trees and
asks each one its name. **9 of 9 pass**: a renamed clone with an origin answers `MAM-basics` (step
2, the new behaviour); the same with the `.git` suffix absent, and with an scp-style
`git@github.com:` URL, both answer `MAM-basics`; a renamed clone whose only remote is named
`upstream` answers with its directory (step 3, and the section-header scan does not mistake
`upstream` for `origin`); a junk `.git/config` and a tree with no `.git` at all both degrade to
the directory name without raising; a worktree of a renamed clone answers `MAM-basics` (steps 1
and 2 together); a worktree whose clone has no origin answers with the clone's directory, never
the worktree's; and a submodule-shaped `.git` file answers with the submodule's directory rather
than `modules`.

**3. The origin basename equals the directory name in every clone that matters, and in one it
does not: `ArtScroll`.** Its origin is a **gist**, so the chain would derive
`f04699f2a9c4eccd3220751fdb233722`. Nothing is exposed — it holds two tracked files, no Python and
no breadcrumb, and `provenance.py` is vendored only into MAM-simple and al-hatorah — but the
plan's "origin basename equals the directory name in all nine repos checked" is true of the nine
and not of the twenty. `repo_name` stays the override if a gist clone ever generates anything. The
breadcrumb census otherwise reproduces: `MAM-basics/` ×462, `MAM-simple/` ×2, `al-hatorah/` ×3,
plus the one `logical-name/` test fixture.

**4. The al-hatorah wrapper's retirement rests on the NESTING, not on step 2 — and it had
therefore been redundant since 2026-08-10.** `mb_cmn/provenance.py` walks a fixed `parents[2]`, so
in `MAM-private/al-hatorah/py/mb_cmn/` it lands on a directory named `al-hatorah` **that has no
`.git` of its own**; the chain reaches its last step and answers `al-hatorah`, which is the right
answer. The old code did the same, for the same reason. The same holds inside a MAM-private
worktree, whose copy of that tree is `<worktree>/al-hatorah`, so the worktree hazard the wrapper
existed for cannot arise there at all. This confirms the prediction of the withdrawn third
entanglement under "Interactions with the MAM-private programme" and sharpens it: nesting, not the
derivation, is what makes the name stable. The pull was still owed, to keep the vendored copy in
sync. `repo_paths.REPO_NAME` was **kept**, as this phase says: `view_model.py`'s
`_generated_by_path` still formats an `al-hatorah/...` path itself. Output-neutral, checked rather
than argued — `py/main_3d_make_override_diff_viewer.py` regenerated with **no artifact change at
all** and its breadcrumbs still read `al-hatorah/py/main_3d_make_override_diff_viewer.py`;
al-hatorah's `py/main_test.py` passes 3 tests.

**5. The re-vendor ripple has an ordering, and this session got it wrong and paid one extra
commit.** `vendoring/compare.py` derives `last_synced` from the date of the last commit touching
each file in the **destination** repo, so committing a re-vendored copy anywhere is itself a
change the next audit reports. **Commit the destination repos first, then run the audit, then
commit the audit.** Done the other way round it takes a second audit commit, which is what
`57b83cf` is. It does converge — `doc/vendoring-inventory.md` and `out/vendoring_*` live here and
are vendored nowhere, so nothing reads them back. Two further things the audit showed: the
al-hatorah group briefly split into a 23rd row reading `provenance.py … DIFFERS` while this repo's
source was ahead of the vendored copy, and merged back to 22 rows and 155 files once
MAM-private `c0540e5` landed, its `last_synced` now `mixed` (27 files at 2026-08-10,
`provenance.py` at 2026-08-11); and holman-ketiv-qere's vendored `paths.py` went `no-commits` →
`2026-08-11`, which is **Precondition 4's own mechanism in its benign form** — that repo's
`e2d1f17` committed a file Phase 0 had already seen vendored, so a date cell that had nothing to
name now names a commit.

**6. MAM-with-doc's `unpinned-latest.html` was one head out of date, from Phase 0's own commit
ordering.** Phase 0 regenerated it while MAM-parsed's head was still the 2026-08-09 commit and
landed MAM-parsed's Graphviz commit `95f64d7` afterwards, so the page has read 2026-08-09 since.
It now reads 2026-08-11, still "0 changes found". Nothing is wrong with the page; the lesson is
that a phase committing several repos should regenerate **after** the repo a generated page reads
has been committed, not before.

**7. The worktree suite count is settled: 903 passed / 5 skipped from a worktree, identical to the
main checkout, with `REPOS_ROOT` set.** Taken later the same day, at Ben's instruction, after this
phase's other work was committed — so it is a deliberate measurement outside any phase's
verification, which is what it should always have been. **919 is dead and so are the "unreal
failures"**: there are none. Without `REPOS_ROOT` the same worktree gives **18 collection errors**,
loudly, so there is no silent-green hazard either. The full statement, including what the old
"never from a worktree" instruction now covers and what it no longer covers, is under "How to run
this plan across sessions". (This finding first recorded the measurement as *not* taken, on the
grounds that this phase's verification forbids running the suite from a worktree. That reading was
too broad — the ban is on doing it *inside this phase's verification*, and creating a throwaway
worktree for a separate measurement was available all along.)

---

## Phase 2 — `.gitattributes` merge — DONE 2026-08-12

*In MAM-basics. Its own commit, touching nothing else, before any file arrives.*

Append wlc-utils' four binary declarations — `*.png`, `*.jpg`, `*.pdf`, `*.woff2` (wlc-utils#50) —
to MAM-basics' `.gitattributes`. Keep MAM-basics' `*.csv text eol=crlf`. Both repos already carry
an identical `* text=auto eol=lf`, so that line does not move.

Content-based auto-detection would very likely handle the 124 images and the extensionless
`Images/Background` anyway. **Do not retest that theory during a 620-file `git add`** — wlc-utils
wrote the rules down deliberately, and a mangled blob discovered at layer 1 is a phase to unpick.

**Verify:** `git check-attr -a` against paths that do not yet exist (it accepts arbitrary paths) —
`gh-pages/wlc/accgram/img/x.png` and `in/Tanach-26.0--UXLC-1.0--2020-04-01/Images/Background`.
Then `check_repo_standards.py` still reports `GITATTRIBUTES_LF=True`, and `git status --porcelain`
is empty.

### Execution record — Phase 2, 2026-08-12

Began at MAM-basics `e4d7997` — **not** the `9194265` Phase 1 left behind, see finding 1 — with
wlc-utils unmoved at `c501dc0` and clean, MAM-basics clean and pushed, and neither repo holding a
worktree. Landed as `30f985b` and pushed fast-forward, no force. **No generator, no mega and no
circuit ran, and none was needed**: this phase changes no Python and no data, so `git check-attr` is
its whole oracle. wlc-utils was not touched at all, so **Phase 0's manifest stands unchanged** —
`.novc/wlc-rest-phase0/wlc-manifest-c501dc0.txt`, 626 rows, sha256 `28c94cde…` — and did not need
re-taking.

The commit is the four declarations copied verbatim from wlc-utils plus a comment saying why they
arrive before the files they govern, and nothing else.

**All three verifications pass, and the first one passes in the form that matters.** `git check-attr
-a` resolves **identically in the two repos** for both paths — which is the real property, since
layer 1 needs the two repos to agree rather than needing any particular attribute value:

| Path | Resolves to | wlc-utils at its own spelling |
|---|---|---|
| a `.png` (`gh-pages/wlc/accgram/img/x.png` here, `gh-pages/accgram/img/x.png` there) | `binary: set`; `diff`, `merge`, `text` all `unset`; `eol: lf` | identical |
| `in/Tanach-26.0--UXLC-1.0--2020-04-01/Images/Background` | `text: auto`, `eol: lf` | identical |

**The extensionless `Images/Background` matches none of the four globs, and that is right rather
than an omission a later phase should fix.** wlc-utils does not cover it either, so both repos hand
it to the same `* text=auto eol=lf` rule and git decides by content at `git add` time — the same
decision from the same rule in both repos, which is the whole of what byte-identity needs. **Phase 3
must not add a glob for it.** `check_repo_standards.py` then reports `GITATTRIBUTES_LF=True`, along
with `LINKED_WORKTREES=0`, `AGENT_BRANCHES=0` and `SYS_PATH_MUTATIONS=0`; and `git status
--porcelain` is empty after the commit.

#### Findings

**1. The baseline had already moved when this phase began — MAM-basics `9194265` → `e4d7997` — but
the suite count had not.** Three commits landed on 2026-08-12 at 11:25, 12:04 and 13:35, touching
five Python files: `py/main_clc_download_notes.py`, `py/main_uxlc_download_changes.py`,
`py/mb_cmn/uxlc_change_url.py`, `py/uxlc_changes/uxlc_authors.py` and `py/uxlc_misc/my_uxlc.py`.
That is UXLC download work, unrelated to this plan. Nothing in Phase 2 depends on the suite, so this
phase is unaffected — **Phase 3 is not**, since it asserts `py/main_test.py` "at its Phase 0 count"
and would read any change those three commits caused as a move bug. Re-measured here to spare Phase
3 the ambiguity: **903 passed, 5 skipped, 57 subtests** at `e4d7997`, which is Phase 0's and Phase
1's figure exactly. **903 still stands as the number Phase 3 compares against.**

**2. Precondition 4's gate check should read MAM-basics' OWN log, not only holman-ketiv-qere's.**
The precondition names `git -C ../holman-ketiv-qere status --porcelain` and that repo's recent log
as the check, and on 2026-08-12 both looked reassuring — clean, fully pushed, no worktree, last
commit some hours back. Both missed the sharper fact: **the holman-ketiv-qere work was committing
into MAM-basics itself**, interleaved with that repo's commits to the minute. MAM-basics `aa5322c`
(12:04:54) sits between holman-ketiv-qere `a0a722a` (11:38:08) and `11ff82a` (12:05:34), and the
last activity of the whole undertaking was MAM-basics `e4d7997` at 13:35 — later than anything in
holman-ketiv-qere. A session checking only the sibling repo would have judged the gate on evidence
an hour and a half staler than what its own repo's log held. **Ben settled it the same day: that
work is finished, run Phase 2.** A later phase re-checking this gate should look at both logs.

Worth recording alongside it: **the mechanism Precondition 4 actually names had not fired.** None of
holman-ketiv-qere's seven commits that day touched `py/mb_cmn/` — they are `gh-pages/uxlc_img/`
PNGs, `py/py_render/` and `py/python_modules/` — and its `paths.py` was last vendored at `e2d1f17`
(2026-08-11 09:45), which is the very commit Phase 0's finding 1 named and which MAM-basics
`5344a74` already absorbed. So the vendoring drift was quiet; what was not quiet was the work.

**3. The new declarations shift no existing blob, and two of the four globs match nothing in this
repo today.** 54 tracked MAM-basics files match the four globs: 53 `.png` and one `.woff2`,
`doc/woff2/Taamey_D.woff2` — the copy Phase 0 found byte-identical to wlc-utils'. **Zero `.jpg` and
zero `.pdf`**, so those two globs are purely forward-looking, governing files that do not arrive
until Phase 3. All 54 report `git ls-files --eol` as `i/-text w/-text attr/-text`: index, worktree
and attribute agree that no text conversion applies, so every one of them was binary by
auto-detection before this commit and is binary by declaration after it. Nothing renormalized, which
is why this commit's diff really is ten lines of `.gitattributes` and nothing more.

---

## Phase 3 — Copy the corpus in (dual residency) — DONE 2026-08-12

*In MAM-basics. wlc-utils is not touched at all.* Nothing here reads the new files yet; the
generators still write into the sibling. **That is the dual-residency window and it is safe** —
wlc-utils stays authoritative and frozen, so the copy is provable and revertible.

Land: `out/` 193, `in/` 135, `doc/` 6, `.github/` (MAM-basics has none, so it arrives whole),
`gh-pages/` 284 **under `gh-pages/wlc/`**. `data/lci_recs.json` → **`in/lci_recs.json`**.

### THIS PHASE PUBLISHES THE SITE — settled 2026-08-11, Ben: **"Let it land."**

**Decided, not open. Do not defer the workflow file and do not re-propose deferring it.** The
question arose hours after Phase 0, when Ben enabled Pages and met Precondition 2, and he answered
it the same day. What follows is the mechanism, then what the decision costs and buys, then the
alternative he turned down.

wlc-utils' `.github/` is **exactly one file**, `.github/workflows/pages.yml`, and it triggers on
`push: branches: [main]`. So "`.github/` arrives whole" means this phase's **own landing commit is
a push to main that fires a Pages deploy** — and with Precondition 2 now met, that deploy is live
rather than inert. **The site therefore goes public at Phase 3**, not at the Phase 6 the plan
designates as its manual gate and calls "the one place in this plan where a mistake makes
something public."

**The publication itself would be benign, and that is exactly why this is easy to miss.** By the
time this phase commits, `gh-pages/wlc/` holds the real 284 files, so
`bdenckla.github.io/MAM-basics/wlc/…` would serve correctly on the first deploy. Only
`gh-pages/index.html` would be absent, Phase 6 being what adds it, so the site **root** would 404
for as long as the two phases are apart. Nothing breaks; the manual gate just stops existing,
silently.

**So this phase carries four obligations the plan did not originally give it:**

1. **Land `gh-pages/wlc/` and `.github/` in ONE commit, or `gh-pages/` strictly first.** The deploy
   publishes whatever the tree holds when the workflow first runs. A commit that lands the workflow
   ahead of the pages would deploy an empty or partial site — briefly, but publicly, and the
   `concurrency` block means only the *last* run survives, so a bad first deploy is not
   self-correcting until something else is pushed.
2. **Re-read `path: gh-pages` in the workflow before committing.** It is already right for the
   nested layout, and it is the one line that decides what becomes public. **This instruction used
   to live in Phase 6 and belongs here now**, because the first deploy is this phase's.
3. **Verify the deploy, not just the diff.** Layer 1 says the bytes arrived; it says nothing about
   whether GitHub built them. After pushing, check the run succeeded — `gh run list --workflow
   pages.yml --limit 1` — and fetch one page at each nesting depth from
   `https://bdenckla.github.io/MAM-basics/wlc/`. A red first deploy discovered at Phase 6 is a
   diagnosis three phases from its cause.
4. **Expect `https://bdenckla.github.io/MAM-basics/` itself to 404, and do not treat it as
   damage.** `gh-pages/index.html` is Phase 6's to add, so the site **root** stays a 404 for as
   long as the two phases are apart. Everything under `/wlc/` serves correctly meanwhile. Say so
   in this phase's write-back so the next session does not chase it.

**What the decision buys**, and why it is the cheaper of the two: decision 1's "everything travels"
holds without an exception, and **layer 1 stays whole at 626 of 626 in a single phase** rather than
splitting 625-plus-1 across two, which would have made this plan's sharpest assertion the one thing
in it needing a footnote.

**Those two figures are wrong and the argument they serve is not — the real pair is 620-of-620
against 619-plus-1.** Six of the 626 are loose root files that do not travel, per Phase 0's
disposition table, so this phase lands 620. Measured at execution, 2026-08-12; finding 1 below.
Nothing about the decision changes, only its arithmetic.

**The alternative Ben turned down, recorded so it is not re-proposed:** defer
`.github/workflows/pages.yml` to Phase 6, landing 625 files here. It would have kept Phase 6 as the
moment of publication and kept that phase's manual gate real. It was rejected because splitting
layer 1 costs more than the gate is worth here — the gate guards against publishing something
wrong, and by the time this phase commits there is nothing wrong to publish.

**On `data/` — the one rename in the plan, and it is Ben's to veto.** It is a single
hand-maintained lookup table with a single reader (`py_uxlc/my_uxlc_page_break_info.py:62`).
Creating a top-level `data/` in MAM-basics for one file inverts this repo's own convention that
committed input lives in `in/` — and UXLC-utils' `data/` is *generated* despite the name, a
confusion `test_h_dot_below_nfc.py:124` already had to encode. As `in/lci_recs.json` it stays
correctly inside the NFC lint's scope as hand-authored material, and `data_dir()` dies in Phase 5.

**In the same commit, the NFC-lint scoping edit** — otherwise the suite is red on arrival.
`test_h_dot_below_nfc.py:107` excludes `out/` wholesale but only six *named* `in/` subdirectories,
and has no `gh-pages/` exclusion (MAM-basics has no such tree today). Measured 2026-08-03 across
all 626 incoming files: **exactly 7 offending sequences, and every one is vendored external text
that must not be normalized** —

| File | Hits |
|---|---|
| `in/UXLC-39/Psalms.xml` | 1 — "tarḥa" decomposed, inside Moshe Greenberg's change description |
| `in/UXLC-misc/all_changes.json` | 4 — two "tarḥa", two "qibbuṣ" as `s` + `\N{COMBINING DOT BELOW}` |
| `in/accgram/uxlc_accent_changes.json` | 2 — derived from `all_changes.json`, so it inherits them |

`out/`, `gh-pages/` and `data/` are clean. These are Chris Kimball's and Moshe Greenberg's words,
copied verbatim from tanach.us by `main_wlc_vendor_uxlc.py`; normalizing them would break
byte-identity with upstream and be undone on the next vendor run. **They are exclusions, not
fixes.**

Add to `_EXCLUDE_DIR_PREFIXES` (`:107-114`): `"in/UXLC-39/"`, `"in/UXLC-misc/"`,
`"in/Tanach-26.0--UXLC-1.0--2020-04-01/"`, `"in/wlc420/"`, `"in/wlc422/"`, and `"gh-pages/"`; and
add `in/accgram/uxlc_accent_changes.json` to `_EXCLUDE_FILES`. **Exclude that one file, not
`in/accgram/` wholesale** — the 24 hand-authored edition transcriptions under
`in/accgram/edition_transcriptions/` are Ben's own prose and belong in scope. Comment the new
entries with what they are: external Tanach/UXLC snapshots kept verbatim for fidelity to source.
`gh-pages/` goes in on the principle `out/` is already on — generated, not hand-authored. `out/`
itself needs no change, being a prefix exclusion already, which is why the incoming 193 are
covered for free.

**Do not touch the wlc-utils `_Scope` at `:157-167` yet**; it still points at a full repo. Phase
10 deletes it.

**Verify — layer 1.** `git ls-files -s` for the landed paths against Phase 0's manifest: **626 of
626 SHA-1 matches**, path deltas exactly the `gh-pages/wlc/` prefix and the one `lci_recs.json`
rename. Then `py/main_test.py` at its Phase 0 count; `git status --porcelain` empty in wlc-utils
(nothing was touched) and clean here after the commit.

**The count in that paragraph is 620, not 626, for the reason two paragraphs above** — the six loose
root files do not travel. Everything else in it was run as written and passed. The wrong figure is
left standing so the execution record below reads against what it was checking.

### Execution record — Phase 3, 2026-08-12

Began at MAM-basics `93b9b90`, wlc-utils `c501dc0`, both clean, both pushed, neither holding a
worktree. Landed as `f99996f`, one commit, pushed fast-forward with no force. **wlc-utils ends this
phase exactly where it began** — `c501dc0`, `git status --porcelain` empty — so Phase 0's manifest
stands unchanged and needed no re-take.

**Precondition 4 was checked on both logs, as Phase 2's finding 2 requires, and it was clear.**
holman-ketiv-qere clean, no worktree, its last commit `69b13f0` at 12:06:32; MAM-basics' own log
holds nothing from that undertaking after `e4d7997` at 13:35:11, everything later being Phase 2's
own `30f985b` and `93b9b90` at 15:59 and 16:02. This phase began at 16:06. Ben's statement of
2026-08-12 that the work is finished therefore held, on the evidence of both logs rather than one —
which is the check Phase 2 asked for, run.

**No generator, no mega and no circuit ran, and none was needed.** Nothing here reads the new files
and no generator was repointed, so there is no artifact to regenerate; a circuit run could only have
introduced drift into the frozen reference this phase's whole method depends on. Layer 2 arrives at
Phase 5, as the plan says.

**The baseline reproduced before anything was copied.** Suite **903 passed / 5 skipped**, the figure
Phases 0, 1 and 2 all measured. The manifest `.novc/wlc-rest-phase0/wlc-manifest-c501dc0.txt`
re-hashed to sha256 `28c94cde461849fbffd53ac16de12a6d9f4eb1804a9ce95e1baa212ea51c1ade` at 626 rows,
byte-identical to Phase 0's. After the one Python edit, `ruff check py` clean and `black --check py`
clean at 771 files — Phase 1's figure exactly.

**Layer 1 passed on the first run: 620 of 620 SHA-1 matches**, zero missing, zero SHA-1 mismatches,
zero mode mismatches, and the path deltas exactly the 285 the plan predicts — 284 `gh-pages/wlc/`
prefixes plus `data/lci_recs.json` → `in/lci_recs.json`. Staged additions by top-level directory:
`gh-pages` 284, `out` 193, `in` 136 (135 plus the renamed `lci_recs.json`), `doc` 6, `.github` 1.
**No Python arrived**, wlc-utils having had none since the 2026-08-01 evacuation, which is why `ruff`
and `black` are unmoved. The scripts are in `.novc/wlc-rest-phase3/`.

**The site is live and the deploy went green.** Run `31636754716` on `f99996f`, conclusion `success`
— the first Pages run this repo has ever had, its only prior workflow run being a 2026-05-14 Copilot
agent. **8 of 8 HTTP checks came out as expected, and each served page is byte-identical to the
committed file**, sha256-compared rather than eyeballed: `/wlc/index.html` and `/wlc/style.css` at
depth 1, `/wlc/accgram/almost-errors.html` at depth 2, `/wlc/420422/` resolving to its `index.html`,
`/wlc/420422/full-record/420422-01.html` at depth 3, the 296 KB
`/wlc/accgram/goerwitz.html` that tanach.us cites five times, and the `woff2` as a binary case.
**`https://bdenckla.github.io/MAM-basics/` itself returns 404, which is obligation 4 satisfied
rather than damage** — `gh-pages/index.html` is Phase 6's to add, and until it does, the site root
404s while everything under `/wlc/` serves. Do not chase it.

#### Findings

**1. Layer 1's figure is 620, not 626 — this phase contradicted Phase 0, and Phase 0 is the side
that is right.** Phase 3's verify line asks for "626 of 626 SHA-1 matches" and its publish box argues
from "626 of 626 ... rather than splitting 625-plus-1". Phase 0's disposition table says the
opposite in as many words: `.gitattributes`, `.gitignore`, `CLAUDE.md`, `LICENSE`, `README.md` and
`wlc-utils.code-workspace` do not travel, "so 'everything travels' means ~620 files, not 626". 620
is what landed. **The publish box's argument survives with its arithmetic corrected** — landing
`.github/workflows/pages.yml` here keeps layer 1 whole at 620 of 620 rather than splitting it
619-plus-1 across two phases — so nothing about Ben's "Let it land" decision is disturbed. Both
figures are corrected in place above, at the box and at the verify line.

**2. The NFC lint's first failure was a CRASH on an extensionless GIF, not the offender report this
phase predicts — and it is the very file Phase 2 told Phase 3 not to add a glob for.** With the
corpus staged and the scoping edit not yet made, both scanning tests died with `UnicodeDecodeError:
'utf-8' codec can't decode byte 0xb3 in position 10` on
`in/Tanach-26.0--UXLC-1.0--2020-04-01/Images/Background`, whose first bytes are `GIF89a`.
`_is_binary` tests the file *extension* and that file has none, so `read_text` raises before a single
offender is reached; it is the one file in the whole MAM-basics scope that git calls binary
(`i/-text`) while the lint calls it text. **The exclusion this phase prescribes for a different
reason — external tanach.us snapshot — is what keeps it out**, so the prescribed edit was sufficient
as written and needed no widening. But a session that had trimmed the exclusion list to just the
three files carrying the seven sequences would have left the crash in place. **Phase 2 remains right
that no `.gitattributes` glob is wanted for that file**: that is git's content detection, this is the
lint's scope, and they are different mechanisms with different answers.

**3. The seven offending sequences reproduce exactly, and the scoping edit lands where it was aimed.**
One at `in/UXLC-39/Psalms.xml:758`, four at `in/UXLC-misc/all_changes.json:21749,21757,33951,33982`,
two at `in/accgram/uxlc_accent_changes.json:8489,8497` — the same three files and the same
distribution the phase names, measured rather than assumed. After the edit, incoming files inside the
MAM-basics NFC scope fall from **294 to 34**, and the 34 are the right ones: **24 of them are the
edition transcriptions under `in/accgram/edition_transcriptions/`**, the exact count this phase
insists must stay in scope, plus the six `doc/` files, three other hand-authored `in/accgram/` JSONs,
`.github/workflows/pages.yml`, and `in/lci_recs.json` — whose staying in scope is part of what the
rename out of `data/` was for. Zero undecodable files and zero cluster hits remain.

**4. One file drew a CRLF warning at `git add` time and it is not a defect — it is layer 1 earning
its keep.** `in/accgram/edition_transcriptions/koren_dt_elyon.txt` warned that "CRLF will be replaced
by LF the next time Git touches it". Both repos report `i/lf w/crlf attr/text=auto eol=lf` for it:
the working-tree copy carries 129 CRs and the index blob is LF, and that was already true in
wlc-utils. The on-disk bytes are identical in the two repos (8392 each) and the blob matched, because
`text=auto` normalized on add exactly as it had in wlc-utils. **The lesson for Phases 9 and 10 is
that the working tree and the blob can legitimately disagree, so a copy must be verified at the blob
level** — comparing working-tree bytes would have been the wrong instrument here even though it
happens to agree.

---

## Phase 4 — Licence scoping — DONE 2026-08-12

*In MAM-basics.* Small, and best done while the arriving trees are still obviously separable.

**Half of this phase already landed, on 2026-08-10; Phase 4 is now the other half.** The
root-level structure was built then, because the same ambiguity already existed in MAM-basics
without wlc-utils: MAM-basics tracks MAM text in `in/mam-ws/`, `in/mam-go/`,
`in/mam-from-sefaria/`, `in/mam-from-Sefaria-2021-11-23/` and `in/mam-ws-bot-edits/`, text derived
from those in `out/mam-ws-parsed-fmt-2/`, `out/mam-ws-bot/`, `out/tmpl-survey-plain/` and
`out/tmpl-survey-plus/`, and third-party material in `in/chabad-ctr/` — all of it covered by
nothing but the root GPL-3.0 and silence. Two files now exist in
`C:/Users/BenDe/GitRepos/MAM-basics`: **`DATA-LICENSES.md`**, a path-by-path table followed by the
MAM CC-BY-SA 4.0 statement copied verbatim from
`C:/Users/BenDe/GitRepos/MAM-parsed/LICENSE.md`; and a **`## License` section at the end of
`README.md`** naming the two declarations. **So this phase extends an existing map rather than
starting one — add rows to `DATA-LICENSES.md`; do not write a second document, and do not restate
the map in `README.md`.**

**wlc-utils is CC0 1.0; MAM-basics is GPL-3.0.** Moving 626 data files from one to the other
either silently withdraws a published public-domain dedication or leaves the status ambiguous.
(This paragraph read "They are the only two of Ben's thirty repos with a `LICENSE` file at all,
and neither README mentions licensing" until 2026-08-10. Both halves were wrong:
`diffable-pointed-hebrew` carries an MIT `LICENSE`, and six repos — MAM-parsed, MAM-simple,
MAM-with-doc, MAM-OSIS, MAM-for-Sefaria and phonetic-hbo — carry a `LICENSE.md` holding the MAM
CC-BY-SA statement. Re-establish with `ls C:/Users/BenDe/GitRepos/*/LICENSE*`.)

Ben's decision, 2026-08-03: **keep GPL-3.0 at the root for code, and scope CC0 to the moved data.**
Place a verbatim copy of wlc-utils' CC0 `LICENSE` at each arriving tree that holds only Ben's own
work — `gh-pages/wlc/LICENSE`, and one covering the wlc portions of `in/` and `out/`. Prefer the
fewest declarations that unambiguously cover the moved paths over one per directory.

**No such tree exists, so no CC0 file was placed anywhere — measured at execution, 2026-08-12,
finding 1 below.** `gh-pages/wlc/` fails the test as squarely as `in/` does: 124 of its 284 files
are crops of manuscript and printed-edition photography. Ben's decision is unchanged and was
executed; what is dropped is the prediction that the CC0-able material would fall on directory
boundaries a `LICENSE` file could sit at. The dedication is made in `DATA-LICENSES.md`'s table
instead, path by path, with the CC0 text repeated verbatim at the end of that file beside the MAM
statement — which is the "fewest declarations that unambiguously cover the moved paths" this
paragraph asks for, since the CC0 boundary is not a directory in any of the three trees.

**Where CC0 must NOT go — checked 2026-08-10, and it narrows the decision above rather than
reversing it.** Kimball's `in/Tanach-26.0--UXLC-1.0--2020-04-01/License.html` grants two different
things: the biblical Hebrew text "may be viewed or copied without restriction", but "All other
files and the look-and-feel of the site are copyrighted by the publisher and require written
permission for any purpose." Two arriving trees are mostly those other files — `in/wlc420/` and
`in/wlc422/` hold `WLCmanual420.pdf`, `WLC_Manual422.pdf` and five release-notes HTML pages
between them, no biblical text among them. A CC0 file placed over the arriving `in/` wholesale
would dedicate Kimball's copyrighted manual to the public domain, which is not Ben's to do.

**"No biblical text among them" is wrong, and the error runs the safe way — measured 2026-08-12,
finding 2 below.** Those two trees hold sixteen files, and `wlc420_ps.txt` and `wlc422_ps.txt` are
3.46 MB each of the Westminster Leningrad Codex in Michigan-Claremont transliteration, each opening
with the J. Alan Groves Center's own header: "This file may be redistributed only with permission."
So the trees carry the **strictest** terms in the repository rather than merely Kimball's reserved
files, and this paragraph's conclusion is strengthened, not disturbed. The header reaches the 102
files of `out/wlc420*/`, `out/wlc422*/` and the two loose `out/diff_*.json` as well, that being the
same text restructured.

**Nor is `in/accgram/` uniformly Ben's**, which is the trap inside the trap: 25 of its 27 files
are his — `printed_decalogue_teamim.json` and the 24 hand transcriptions under
`edition_transcriptions/` — but `ctr_decalogue.json` is derived from chabad.org's Complete Tanach
with Rashi, and `uxlc_accent_changes.json` is derived from Kimball's `in/UXLC-misc/all_changes.json`
and carries Kimball's and Moshe Greenberg's own change descriptions. Those are the same two files
Phase 3 already treats as external for the NFC lint, so the two phases should agree about them.

So: scope CC0 to what is Ben's own work, and give every vendored tree a `DATA-LICENSES.md` row
naming its real terms instead. `License.html` travels unchanged either way.

**Verify:** `git status` clean after the commit; a reader landing on any moved path can reach a
licence statement that names it, and no path is claimed for CC0 that the paragraphs above exclude.
No artifact changes, so no regeneration is owed.

### Execution record — Phase 4, 2026-08-12

Began at MAM-basics `e6c3141`, wlc-utils `c501dc0`, both clean, both pushed, neither holding a
worktree — Phase 3's closing baseline, reproduced exactly, with MAM-basics at **1906** tracked
files and wlc-utils at **626**. Landed as `20bb89e`, one commit. **wlc-utils was read for its
`LICENSE` and its file list and for nothing else, and ends this phase at `c501dc0` with
`git status --porcelain` empty.**

**Precondition 4 was checked on both logs, as Phase 2's finding 2 requires, and it was clear.**
holman-ketiv-qere clean, no worktree, its last commit `69b13f0` at 12:06:32; MAM-basics' own log
holds nothing from that undertaking after `e4d7997` at 13:35:11, everything later being Phases 2
and 3 from 15:59 to 16:19. Ben's statement of 2026-08-12 that the work is finished held on the
evidence of both logs rather than one.

**No generator, no mega, no circuit and no regeneration — as this phase says, and none was
wanted.** Two files changed, `DATA-LICENSES.md` and `README.md`, neither of them Python, so `ruff`
and `black` had nothing to run over. The suite was run anyway, because the NFC lint scans
hand-authored files and this phase wrote 190 lines of them: **903 passed / 5 skipped**, the figure
Phases 0 through 3 all measured.

**What landed.** Thirteen rows in `DATA-LICENSES.md`, covering every arriving tree; the GPL-3.0
paragraph widened to name `.github/` and the prose under `doc/`, with `doc/woff2/` excepted; a
third "shape of these declarations" item recording why no CC0 file sits in a subtree; and the CC0
1.0 text repeated verbatim in a fenced block at the end of the file, mirroring how the MAM
CC-BY-SA statement is already carried there. In `README.md`, two clauses of the `## License`
section that the arriving corpus had made false — "each corpus keeps the terms its preparers set"
and "one corpus is reproduced under no grant at all". **No second document was written and the map
is not restated in `README.md`.**

**Verification was mechanical rather than by eye.** `.novc/wlc-rest-phase4/check_coverage.py`
derives the 620 moved paths from wlc-utils' own `git ls-files` minus Phase 0's six stay-behind root
files, applies the two path deltas, and assigns each path to exactly one licence statement:

| | |
|---|---|
| moved paths, all present in MAM-basics | **620** |
| named by a licence statement | **620** — none uncovered |
| claimed for CC0 | **276** |
| CC0 claims the exclusions forbid | **0** |

The 276 are the 159 generated pages, scripts and stylesheet under `gh-pages/wlc/`, the 91 files of
`out/accgram/`, the 25 hand-authored files of `in/accgram/`, and `in/lci_recs.json`.

#### Findings

**1. `gh-pages/wlc/` does not hold only Ben's own work, so no CC0 file was placed there — and this
is the correction Ben already made on 2026-08-10 for Kimball's manual, applied to a tree this phase
had not measured.** 124 of its 284 files are image crops, and they are photography of manuscripts
and printed editions: the filenames name the Aleppo Codex (`AC-1K-20v25.png`), the Leningrad Codex
(`LC-043A-Exod-20v13-lo.png`), Koren (`Koren-p-113-Ex-Dec-p-trad-taxton.png`), Ginsburg,
Heidenheim, Hahn, Da'at Miqra and a Venice edition. Two were opened and looked at rather than
inferred from their names. With the font that is **125 of 284**. The instruction "Place a verbatim
copy of wlc-utils' CC0 `LICENSE` at ... `gh-pages/wlc/LICENSE`" would have dedicated all of it to
the public domain, which is not Ben's to do — word for word the reasoning the "Where CC0 must NOT
go" paragraph already applies to `in/`. What was executed is that paragraph's governing sentence,
"scope CC0 to what is Ben's own work, and give every vendored tree a `DATA-LICENSES.md` row naming
its real terms instead". **The boundary is not a directory, which is why no file could express
it**: all 124 crops sit under three `img/` directories, but the 159 CC0 files sit beside those
directories at every level, so "everything under `gh-pages/wlc/` except the three `img/`
directories and `woff2/`" can be a row in a table and nothing else. Recorded in
`DATA-LICENSES.md`'s own shape paragraph as well as here, so it does not get reinstated by someone
reading only the plan.

**2. `in/wlc420/` and `in/wlc422/` DO hold biblical text, and it carries the strictest terms in the
repository — so this phase's conclusion is right and its stated reason understates itself.**
Corrected in place above. The two `_ps.txt` files are the Westminster Leningrad Codex, 3.46 MB
each, headed "This file may be redistributed only with permission" by the J. Alan Groves Center.
Also present, and also not Kimball's: `michigan.man`, H. Van Dyke Parunak's 1982 code manual for
the Michigan Old Testament, and `supplmt.wts`, the Groves Center's supplement to it. **This reaches
`out/` as well** — the 102 files of `out/wlc420*/`, `out/wlc422*/` and the two loose `diff_*.json`
are that same text restructured, so they are not claimed for CC0 either, and their row says why.

**3. The Taamey D font's terms are recorded nowhere, and the file cannot supply them.**
`gh-pages/wlc/woff2/Taamey_D.woff2` arrived byte-identical to the `doc/woff2/Taamey_D.woff2` that
has stood here since `d86e577`, 2026-03-09 — the pair Phase 0's census noticed and left as an issue
to file. No repository of Ben's names the font's licence: swept across seven clones for "Culmus",
"OFL" and "Taamey ... licen", the only hits are inside PNG binaries. The woff2 itself reports
`metaLen` 0, so it carries no metadata block to read either. Its row names both copies, says the
terms are not recorded, and makes no grant. **A pre-existing gap this phase surfaced rather than
created**, and it is Ben's to settle — establishing the font's terms would let that row say
something.

**4. `DATA-LICENSES.md` carried a sentence Phase 3 had already made false.** "Scans of printed
editions are **not** in this repository, and the indexes under `in/scan-pages/` are not a
substitute for them" was written on 2026-08-10 and was true then; the 124 crops landed on
2026-08-12. It now says that **whole** scans are still absent and names the crops as the exception,
with the change and its date recorded in the paragraph itself. **The lesson for Phases 5 through
11: a claim this repo makes about itself can be falsified by a phase that edits no prose at all,
and nothing in this plan's verification list would have caught it.**

**Two things left alone deliberately, flagged rather than folded in.** `DATA-LICENSES.md`'s
pre-existing row for `in/Psalms 120-134 -- wlcubs420.txt` calls that WLC sample copyable "without
restriction" on tanach.us's authority, and it now sits eight rows above a statement quoting the
Groves Center's "only with permission" over the same corpus. Both statements are in the repository
and the tension is real; reconciling them is Ben's call, and that file is not a moved path this
phase may edit. Second, the map still names no terms for `misc/`, `py-examples-out/`, `.vscode/`,
`.claude-disabled/` or the three loose root scripts — the root GPL-3.0 is the default that covers
them, and widening the map to trees this plan never touched is scope this phase does not have.

---

## Phase 5 — Collapse `wlc_paths.py`; repoint every generator — DONE 2026-08-12

*In MAM-basics.* The large phase. **Keep it to one session** — an interrupted repoint leaves half
the generators writing to the sibling and half writing home, which is worse than either.

`py/wlc_paths.py` disappears. Its contents split three ways:

| Today | Becomes | Sites |
|---|---|---|
| `wlc_data_root()` | `paths.repo_root()` | 28 / 27 modules |
| `out_dir()`, `in_dir()` | `paths.out_dir()`, `paths.in_dir()` — **new in `mb_cmn/paths.py`**, layout accessors this repo wants anyway | 26/15, 16/12 |
| `gh_pages_dir()` | `paths.wlc_pages_dir()` = `paths.gh_pages_dir() / "wlc"` | 26 / 26 |
| `data_dir()` | dies; its one caller reads `paths.in_dir() / "lci_recs.json"` | 1 |
| `novc_dir()`, `scans_dir()` | `paths.novc_dir()`, `paths.scans_dir()` — **one** scratch dir now, not two | 2, 1 |
| `siblings_root`, `sibling`, `require_sibling` | delete — pure delegation to `mb_cmn.paths` since the Python plan's Phase 2 | — |
| `mam_basics_dir`, `require_mam_basics_dir` | delete — already dead | — |
| the 14 live sibling accessors (`mam_simple_dir` … `require_uxlc_utils_dir` — among them `wlc_utils_private_dir` and `al_hatorah_phonetic_dir`, which the MAM-private programme repoints; see "Interactions with the MAM-private programme") | move verbatim into `mb_cmn/paths.py`, which already owns `sibling_repo` | names unchanged |

**Two accessors for the pages tree, not one.** `gh_pages_dir()` means the deploy root;
`wlc_pages_dir()` means `gh-pages/wlc/`. All 26 wlc call sites take the second, which leaves
MAM-basics free to publish something of its own later without every wlc page landing at the site
root.

**Churn control.** The rewrite is two mechanical substitutions per module — `import wlc_paths` →
`from mb_cmn import paths`, and `wlc_paths.X()` → `paths.X()` with `wlc_data_root` → `repo_root`
and `gh_pages_dir` → `wlc_pages_dir`. The whole diff should be import lines and qualified names.
**Use `open(..., newline="")` on both read and write**: the Python plan's Phase 5 lost a pass to
`Path.write_text` silently converting 20 files to CRLF.

Adding four layout accessors to `mb_cmn/paths.py` has nil blast radius: `paths.py` exists only in
MAM-basics, and `copy_by_intersection` copies only files already present in a destination, so
nothing propagates until a repo opts in.

Also in this phase — all of it the `.novc` constraint dissolving, and worth reading against
`wlc_paths.py`'s docstring, which exists to explain why it could not dissolve before:

- `accgram/gen_highlight_picker.py:130` — `img_url = f"../gh-pages/accgram/img/{img_name}"`
  becomes `f"../gh-pages/wlc/accgram/img/{img_name}"`. Still relative to the picker page's own
  `.novc/` location, now MAM-basics'. The old constraint held because `.novc/` and `gh-pages/`
  were siblings one level under `wlc_data_root()`; they are siblings one level under
  `repo_root()` now, so the geometry survives the move and only the nesting segment is added.
- `gen_highlight_picker.py:152-158` — `--serve` served from `wlc_data_root()`; becomes
  `paths.repo_root()`.
- `accgram/scan_page.py:59` — `OUT = paths.scans_dir()`. `WLC_SCANS_DIR` is absolute and
  out-of-repo; unaffected.
- `main_repo_maintenance.py:102-110` — drop the wlc-utils `.novc/` wipe and the paragraph
  explaining why a foreign wipe was needed. There is one `.novc/` now. **Keep** the docstring's
  warning about `.novc` having once destroyed a durable result — that is the version that learned
  the lesson.

**The eight test modules that resolve wlc paths**, all falling out of the same substitution:
`test_prose_conventions.py:196-201` (asserts non-empty, so it fails loudly — which is what you
want), `test_almost_errors.py:107` (binds at **module** level, so a miss is an import-time
collection error rather than a test failure — fix it first), `test_scan_overlay_viewboxes.py`,
`test_maqaf_nonfinal_accents_page.py`, `test_printed_decalogue_koren.py`,
`test_printed_decalogue_simanim.py`, `test_dual_cant_detangle.py`, and
`test_h_dot_below_nfc.py:50,159` (the import and the wlc scope's root — leave the scope itself for
Phase 10).

**Verify — layers 2 and 3, and this is the plan's centre of gravity.**

1. Full circuit from `C:/Users/BenDe/GitRepos/MAM-basics`. `git status --porcelain` here shows
   **only the source edits**; none of the 620 landed files changed.
2. **Snapshot wlc-utils' mtimes before and compare after: zero files touched.** This is the direct
   test of the collision fix, and an empty `git status` there is not sufficient — a stale call
   site rewrites a file to identical bytes.
3. Snapshot MAM-basics' mtimes too and record how many of the 620 were rewritten. Expect roughly
   509. Report the ~111 static files as proved by layer 1 only.
4. `py/main_test.py` at its Phase 0 count; `ruff check py` and `black --check py` clean.
5. `py/main_edition_transcription.py build --check` — 12/12 committed `.txt` bodies re-derived.
6. **The claim under Context, tested directly:** `git grep -n "wlc_paths\|wlc-utils" -- py` finds
   no path construction, only prose and issue citations.

**Verification 6 cannot be literally true until Phase 10, and it is this phase's own instructions
that make it so — see finding 6 below.** Leaving `test_h_dot_below_nfc.py`'s wlc-utils NFC scope for
Phase 10, which the paragraph on the eight test modules requires, means leaving a scope that must
resolve a root. The claim it was reaching for does hold in the form that matters: **no generator
constructs a wlc-utils path, and nothing writes there.**

### Execution record — Phase 5, 2026-08-12

Began at MAM-basics `2250c1c`, wlc-utils `c501dc0`, both clean, both pushed, neither holding a
worktree — Phase 4's closing baseline, reproduced exactly, with MAM-basics at **1906** tracked files
and wlc-utils at **626**. Run from the **main checkout**, not a worktree, so this phase's zero-mtime
assertion is measured where the generators actually run. Four commits here — `5ed6bb4` the repoint,
`3edbc5b` the UXLC refresh, `6fd9a9c` the vendoring re-audit, and this write-back — plus one in
holman-ketiv-qere, `637237b`. All pushed fast-forward, no force; three Pages deploys, all green
(runs `31662766682`, `31662795524`, `31662898211`).

**Precondition 4 was checked on both logs, as Phase 2's finding 2 requires, and it was clear.**
holman-ketiv-qere clean, no worktree, its last commit `69b13f0` at 12:06:32; MAM-basics' own log
holds nothing from that undertaking after `e4d7997` at 13:35:11, everything later being Phases 2, 3
and 4 from 15:59 to 16:43. Ben's statement of 2026-08-12 that the work is finished held on the
evidence of both logs. **That gate is about the WORK being live, and it was not — but the work had
left two loose ends this phase then had to walk into anyway; see findings 5 and 8.**

**This phase's own scale reproduces**: `py/wlc_paths.py` **203 lines, 23 `def`s**, and **72 files
under `py/` mentioning `wlc_paths`** — of which **64** carried `import wlc_paths` and 8 named it in
prose only.

**wlc-utils ends this phase exactly where it began** — `c501dc0`, `git status --porcelain` empty —
so Phase 0's manifest stands unchanged and needed no re-take.

**Layer 3, and it is the whole point of the plan: ZERO files touched in wlc-utils.** Snapshotted by
`st_mtime_ns` over all 627 files on disk there (626 tracked plus one under the ignored `.claude/`),
three times: at session start, after every source edit, and after the full circuit. Zero mtime
changes, zero size changes, zero added, zero removed, at every comparison. **The circuit is the two
commands Phase 0's finding 2 named** — `main_0_mega.py` exit 0, then `main_edition_transcription.py
build --check` 12/12 — and eleven was never tried.

**Layer 2, cross-checked against the frozen reference rather than only against `git status`.**
wlc-utils still holds 620 files no program writes any more, so a byte comparison re-derives layer 1
on demand, which is what the plan offers for exactly this moment:

| | |
|---|---|
| moved paths compared | **620** |
| byte-identical to wlc-utils' copy | **614** |
| missing here | **0** |
| differing | **6** |

**All 284 `gh-pages/wlc/` files are in the 614** — every one of the 154 pages, the stylesheet, the
scripts and the images — which is the sharpest single piece of evidence that the repoint is
content-neutral, and the thing finding 1 nearly broke. The six that differ have two causes and
neither is a move bug: `out/accgram/chanted-word-accents.json` and `out/accgram/research-oddballs.json`
are this phase working (findings 2 and 7), and `in/UXLC-misc/_provenance.md`,
`in/UXLC-misc/all_changes.json`, `in/accgram/uxlc_accent_changes.json` and
`out/accgram/uxlc_grammar_test.txt` are the UXLC refresh (finding 5).

**Every other verification passed as written.** Suite **903 passed / 5 skipped / 57 subtests** —
measured before the edits, again after them and before the circuit, and again at the end, the same
figure all three times and the figure Phases 0 through 4 all measured. `ruff check py` clean.
`black --check py` clean at **770** files, one fewer than the standing 771 because `wlc_paths.py` is
gone. The tree is clean and nothing is unpushed.

**What the rewrite actually was.** `mb_cmn/paths.py` gains six layout accessors (`in_dir`, `out_dir`,
`gh_pages_dir`, `wlc_pages_dir`, `novc_dir`, `scans_dir`) and the eleven live sibling accessors,
moved by name; `data_dir`, `siblings_root`, `sibling`, the `require_sibling` re-export and the two
dead `mam_basics_dir` names are deleted with the module. 72 files took the two mechanical
substitutions; 49 further prose occurrences naming a wlc site path gained the `wlc/` segment, gated
on the named directory existing under `gh-pages/wlc/` so that `py/clc/`'s references to UXLC-utils'
pages and `py/versification_and_cantillation/`'s to MAM-simple's were left alone. Two call sites
that composed `repo_root() / ".novc"` by hand now ask `novc_dir()`, so that string appears once.

**Phase 7's `420422` blob URL was deliberately left alone**, that phase's own instruction being that
folding it in would put a real diff inside a zero-diff oracle.

#### Findings

**1. The plan missed a relative-link computation, and it would have rewritten the stylesheet href on
all 154 pages at once. This is the finding of the phase.**
`rtms_report._path_to_gh_pages_style`, which 13 page modules call for their `path_to_style`, derives
each page's `../` prefix by finding a path part named `gh-pages` and counting the depth below it.
**`style.css` sits at the WLC SITE ROOT, `gh-pages/wlc/`, one level below the deploy root** — so
counting from `gh-pages` emits `../../style.css` where every published page says `../style.css`. It
now anchors on `gh-pages/wlc` when that segment is present and falls back to `gh-pages` when it is
not, so a `--html-out` pointing at a bare `gh-pages/` behaves as before;
`_derive_html_out_from_out_path` needed the same segment. **The plan's "Churn control" paragraph is
what obscured it**: "two mechanical substitutions per module … the whole diff should be import lines
and qualified names" is true of 72 files and false of this one, because this computation never
mentions `wlc_paths` and so appears in no census of it. **The lesson for Phase 8, which builds the
redirect stubs by prefix rewrite: a path computed from a path PART is invisible to a search for the
accessor that produced it.** Verified live afterwards, not merely by diff —
`https://bdenckla.github.io/MAM-basics/wlc/accgram/goerwitz.html` serves `href="../style.css"`.

**2. `out/accgram/chanted-word-accents.json` changed, and a generated artifact carrying a path in its
PROSE is why.** `chanted_word_accents.py:1210` writes an `already_documented_elsewhere` sentence that
cites `gh-pages/accgram/almost-errors.html` by name, and that sentence is emitted into the JSON. So
the prose sweep moved a tracked artifact. Nothing in this plan's verification list distinguishes
"the artifact changed because the code moved" from "the artifact changed because a docstring did";
the frozen-reference comparison is what made it cheap to tell.

**3. The plan's accessor arithmetic is wrong in both directions, and neither error costs anything.**
Its table says "the 14 live sibling accessors (`mam_simple_dir` … `require_uxlc_utils_dir`)". Between
those two names there are **13**, of which the same table separately deletes two as already dead
(`mam_basics_dir`, `require_mam_basics_dir`), so **11 moved**. The same table calls the layout
additions "four layout accessors" while listing six. Measured 2026-08-12. Both figures are
descriptions of work the table also spells out by name, and the names were followed.

**4. All nine `wlc_paths.require_sibling` "call sites" are prose.** Not one is a call: they are
docstring and comment citations, eight of them in `py/tests/` explaining why a missing sibling FAILS
rather than skips. The per-accessor counts in this plan's table come from a text search, so they
count sentences alongside code — worth knowing before a later phase sizes work from one.

**5. The circuit pulled five weeks of UXLC change log, and that is Phase 0's finding 1 from the
other direction.** `wlc-vendor-uxlc` copies UXLC-utils' `out/UXLC-misc/all_changes.json` in, and the
copy that arrived at Phase 3 had been vendored at UXLC-utils `52de493` on **2026-07-06**. That repo's
`3435fc8` — "Refresh the change logs from hcanat.us, and override its four defects" — landed at
**12:05 on 2026-08-12**, and no circuit had run here since Phase 1 on 2026-08-11, so the first
circuit run after it pulled the lot: `all_changes.json` +996 lines, `uxlc_accent_changes.json` +444,
and `out/accgram/uxlc_grammar_test.txt` moving from 201 prose-corpus verses to 211. **The report's
directional-asymmetry claim now has two counterexamples**, Ex 38:12.6 and Judg 11:24.7, both crossing
WLC-ungram → UXLC-gram where the OUT set had none; the report checks the claim rather than asserting
it, so it says so itself. Committed apart from the repoint, as `3edbc5b`. **Phase 0's finding 1 was a
SIBLING gaining a vendored file and drifting artifacts here; this is this repo's own vendored INPUT
going stale against a sibling that moved. Phase 10 should expect the class, not the instance.**

**6. Verification 6 is unsatisfiable as written, and this phase's own instructions are why.** It asks
that `git grep -n "wlc_paths\|wlc-utils" -- py` find "no path construction". Two survive.
`test_h_dot_below_nfc.py:190` is the wlc-utils NFC scope's root, now
`paths.require_sibling("wlc-utils", paths.sibling_repo("wlc-utils"))` — a **read**, and the plan's own
list of the eight test modules says to leave that scope for Phase 10, which cannot be done without
leaving it a root to resolve. `test_mb_cmn_paths.py:106` passes the string `"wlc-utils"` to
`sibling_repo` under a mocked environment as test DATA, asserting the name-mapping function, and
touches no filesystem. The claim that does hold, and is what the Context section actually argues, is
that **no generator constructs a wlc-utils path**. Phase 8 will add one more read —
the redirect-stub generator's own — which that phase already calls "the last remaining reference to
the sibling in the whole tree"; after Phase 10 removes the NFC scope, it will be.

**7. `out/accgram/research-oddballs.json` is the phase's own receipt, and it is the one artifact that
prints where the generators read from.** Its header records the absolute directories of its inputs,
which went from `C:/Users/BenDe/GitRepos/wlc-utils/out/accgram/prose/_oddballs.json`,
`.../wlc-utils/out/wlc422-kq-u` and `.../wlc-utils/in/UXLC-39` to the MAM-basics spellings of all
three. **Note for Phase 10 and for anyone reading that file: it commits a machine-specific absolute
path into a tracked artifact.** That predates this plan and is not this phase's to change, but it is
now this repo's own path rather than a sibling's, which makes it more visible rather than less.

**8. Phase 10's instruction to delete `test_h_dot_below_nfc.py`'s `import wlc_paths` at `:50` is
stale, and one more re-vendor was owed than this phase expected.** That import is already gone —
this phase changed it, as its own list of the eight test modules says. What Phase 10 will find there
is the `_Scope` and `_WLC_EXCLUDE_DIR_PREFIXES`, and a `from mb_cmn import paths` that must stay
because the MAM-basics and UXLC-utils scopes use it. Separately, `mb_cmn/paths.py` is vendored into
holman-ketiv-qere, so editing it drifted this repo's own audit — Precondition 4's mechanism firing
even though the work it names is finished. Phase 1's finding 5 ordering was applied rather than
rediscovered and cost the predicted one commit each side: destination first (`637237b`, whose pull
also carried `uxlc_misc/my_uxlc.py` forward from `e4d7997`, a second thing nothing had re-vendored
since 13:35 that day; holman-ketiv-qere's own suite passes, 51 tests), then the audit, then the audit
commit. **What is left differing is NOT this phase's and was recorded rather than fixed**:
`mb_cmn/uxlc_change_url.py` against mgketer and book-of-job, both stale since `e4d7997`. book-of-job's
copies have mechanism `unknown` and category `stale`, so nothing syncs that repo by script; mgketer's
are an active `copy_script` destination, but whether mgketer wants the hcanat.us default is a question
for whoever made that change.

**One prediction of this plan's that came out exactly wrong, and it is worth a line because a later
phase may reuse the reasoning.** Verify step 3 expects "roughly 509" of the 620 rewritten and "~111"
not. Measured: **351 rewritten, 269 not.** The two groups the plan names reproduce to the file — 73
static assets under `gh-pages/wlc/accgram/` and 38 under `out/accgram/goerwitz-stderr/`, 111 exactly
— but the estimate counted only those, and **forgot that the whole of `in/` is committed INPUT that
nothing regenerates**: 94 files there, plus 54 images under `gh-pages/wlc/wlc-a-notes/img/` and
`gh-pages/wlc/420422/img/`, plus `doc/` 6 and `.github/` 1. The plan's own instruction is the right
one and was followed — say which files are proved by layer 2 and which only by layer 1 — but the
number attached to it was built from the output trees alone.

---

## Phase 6 — Pages live on MAM-basics — DONE 2026-08-13

*In MAM-basics, plus one manual action only Ben can take.*

**THE WORKFLOW IS ALREADY HERE, AND THE SITE IS ALREADY PUBLIC — settled 2026-08-11, Ben: "Let it
land."** Phase 3 lands `.github/` whole, which is that one file, and the deploy it fires is live.
See Phase 3's decision box. **So this phase copies nothing and gates nothing**; both halves of its
original description are spent. Precondition 2, the settings change only Ben could make, was done
on 2026-08-11.

**What is left here is real work, and it is the whole of the verification below:** add
`gh-pages/index.html`, closing the root 404 that has stood since Phase 3; confirm the pins are
what the paragraph below says; and run the HTTP list, which no earlier phase does in full. **Read
the "Copy … verbatim" paragraph as a description of the file you should find**, and treat any
difference from it as a finding — Phase 3 landed a copy of wlc-utils' file, so it should match.

Copy wlc-utils' `.github/workflows/pages.yml` **verbatim**: `on: push branches:[main]` plus
`workflow_dispatch`; `permissions: contents:read / pages:write / id-token:write`;
`concurrency: {group: github-pages, cancel-in-progress: true}`; `actions/checkout@v7`,
`configure-pages@v6`, `upload-pages-artifact@v5` with `path: gh-pages`, `deploy-pages@v5`. Those
pins are post-`72ba4ba` ("Bump the pinned Pages actions off the deprecated Node 20"); do not
re-derive them. `path: gh-pages` is already right for the nested layout. No `CNAME`, no
`.nojekyll`, no `_config.yml` — matching what works today.

The concurrency block is the reason Ben's standing commit-and-push-at-will rule is safe: a
rapid-fire series of pushes produces one deploy, the last one. All twelve of his Pages repos
declare it; **do not add a sleep, a cron, or a "have I deployed recently" check.**

Add `gh-pages/index.html`: a short page pointing at `wlc/`. **The root has been a 404 since Phase
3**, that phase publishing the site without it, so this closes a gap rather than pre-empting one.
(This paragraph read "so `bdenckla.github.io/MAM-basics/` is not a 404 the day the site goes
public" — true when this phase was the day the site went public, which the 2026-08-11 decision
changed.)

~~**Manual gate: Ben sets Settings → Pages → Source: GitHub Actions, then pushes to `main`.**~~
**Done 2026-08-11 — there is no manual gate left in this phase.** Ben enabled Pages that day and
correctly chose no starter workflow. What survives from that bullet is the operational fact, and
it still bites: **the workflow triggers on push to `main` only**, so a branch push will not deploy
— a real way to spend a session believing the phase failed.

**Verify by HTTP, not by diff.** This is the one phase with no artifact oracle.

- The five URLs tanach.us cites: `.../MAM-basics/wlc/accgram/goerwitz.html` → 200.
- The four UXLC-utils fragment deep links, e.g.
  `.../wlc/accgram/supplied-marks.html#supplied-dt5v6-bet-atnax` → 200 **and the anchor resolves**.
- MAM-simple's link target, `.../wlc/accgram/printed-decalogue.html` → 200.
- **One page at each nesting depth**, because `style.css` is referenced as `../style.css` from
  depth-1 pages and `../../style.css` from depth-2, and `woff2/Taamey_D.woff2` from inside the CSS:
  `wlc/index.html`, `wlc/420422/index.html`, `wlc/420422/full-record/<any>.html`,
  `wlc/wlc-a-notes/ucp/<any>.html`. Confirm the stylesheet **and the font** both load — browser
  network panel, not merely a 200 on the HTML.
- One `img/` PNG.
- **`.../wlc/accgram/` 404s, and that is correct.** `gh-pages/accgram/` has no `index.html` today
  either, though wlc-utils' README advertises the section, so it serves nothing before and nothing
  after. **Record this explicitly**, because after Phase 9 a redirect landing on a 404 looks
  exactly like evacuation damage. File it as its own issue; fixing it is page work, and page work
  contends with this plan's oracle.

### Execution record — Phase 6, 2026-08-13

Began at MAM-basics `89b9b1d`, wlc-utils `c501dc0`, both clean, both pushed, neither holding a
worktree — `git worktree list` gave exactly one line in each. MAM-basics holds **1905** tracked
files, wlc-utils its unchanged **626**. Landed as `c50745a`, one commit, two files, pushed
fast-forward with no force. **wlc-utils was not touched at all**, so Phase 0's manifest still
stands.

**Precondition 4 was checked on both logs and was clear.** holman-ketiv-qere clean, no worktree,
its last commit `637237b` at 2026-08-12 23:05:35 — which is Phase 5's own re-vendor commit in that
repo, not that undertaking's work. MAM-basics' own log holds nothing from it either: its last four
commits are Phase 5's `5ed6bb4`, `3edbc5b`, `6fd9a9c` and `89b9b1d`, at 23:04 through 23:11 the
same evening. So Ben's statement of 2026-08-12 that the work is finished held for a fourth phase
running, on the evidence of both logs rather than one.

**No generator, no mega and no circuit ran, and none was needed** — this phase adds a hand-written
page and changes no generator, so there is no artifact to regenerate. `git status --porcelain`
showed only `gh-pages/index.html` and `DATA-LICENSES.md` before the commit, and nothing after it.
The baseline reproduced unchanged: suite **903 passed / 5 skipped**, the figure every phase from 0
onward has measured; `ruff check py` clean; `black --check py` clean at **770** files, Phase 5's
figure exactly. No Python was touched, so black had nothing to format.

**The workflow reproduces the "Copy … verbatim" paragraph clause for clause, with zero
differences.** `diff .github/workflows/pages.yml ../wlc-utils/.github/workflows/pages.yml` is
empty — the file Phase 3 landed is byte-identical to the file this phase describes. Every clause
checks out individually too: `on: push branches: [main]` plus `workflow_dispatch`; `contents:
read` / `pages: write` / `id-token: write`; `concurrency: {group: github-pages,
cancel-in-progress: true}`; `actions/checkout@v7`, `actions/configure-pages@v6`,
`actions/upload-pages-artifact@v5` with `path: gh-pages`, `actions/deploy-pages@v5`. And no
`CNAME`, `.nojekyll` or `_config.yml` exists anywhere in the tree, tracked — `git ls-files` finds
none of the three.

**`gh-pages/index.html` is hand-written, and it says so in a comment.** The three sibling repos
whose `gh-pages/index.html` is generated — MAM-parsed, MAM-with-doc, MAM-OSIS — all open with a
"Do not edit by hand" comment naming their generator in `MAM-basics/py/`, so an index page here
carrying no marker either way would read as one whose generator had gone missing. It references no
stylesheet, matching the two hand-written index pages in these repos: wlc-utils' own, which is
`gh-pages/wlc/index.html` here, and UXLC-utils'.

**The deploy went green: run `31710845632` on `c50745a`, conclusion `success`, 5 seconds of
queue.** The four runs before it — `31663135208` on `89b9b1d` and the three Phase 5 commits before
that — were all green too, so no red deploy has ever been left behind for a later phase to
diagnose.

**The check list ran 12 of 12 as expected, and every 200 was byte-checked rather than counted.**
The script is `.novc/wlc-rest-phase6/phase6_http_check.py`; for each URL mapping to a committed
file it sha256-compares the served bytes against that file, so a stub answering 200 would fail.

| URL, under `https://bdenckla.github.io/MAM-basics/` | Result |
|---|---|
| `wlc/accgram/goerwitz.html` — the five tanach.us citations, all of this one URL | 200, bytes match |
| `wlc/accgram/supplied-marks.html` — the two MAM-basics CLC tests' corroboration URL | 200, bytes match |
| the same page with each of the four `#supplied-…` fragments UXLC-utils cites | 200, bytes match, and all four anchor targets present |
| `wlc/accgram/printed-decalogue.html` — MAM-simple's link target | 200, bytes match |
| `wlc/420422/`, `wlc/420422/full-record/420422-54.html`, `wlc/wlc-a-notes/` — three of `document-index`'s four deep paths | 200, bytes match; both directory URLs resolve to their `index.html` |
| `wlc/accgram/` — `document-index`'s fourth, and wlc-utils' `README.md:42` | **404, and that is correct** — see finding 4 |
| `wlc/` and the site root `/` | 200, bytes match; **the root is what this phase adds** |

**The stylesheet and the font both load — the two things a 200 on the HTML does not prove.** Each
page's `href` was resolved the way a browser resolves it, then fetched; then the stylesheet's own
`@font-face` `src: url("woff2/Taamey_D.woff2")` was resolved against the stylesheet's location and
fetched, and its first four bytes checked to be `wOF2`. Both two-deep pages tried
(`wlc/420422/index.html`, `wlc/accgram/supplied-marks.html`) emit `../style.css`, both three-deep
pages (`wlc/420422/full-record/420422-54.html`, `wlc/wlc-a-notes/ucp/uxlc_change_proposal_01.html`)
emit `../../style.css`, and all four resolve to the single
`…/MAM-basics/wlc/style.css`, which serves 200, whose font resolves to `…/MAM-basics/wlc/woff2/Taamey_D.woff2`,
which serves 200 as a real woff2. **So Phase 5's finding 1 is confirmed live at both depths**: the
relative-link computation it repaired is emitting the right prefix on the deployed site, not merely
in the tree. One `img/` PNG was fetched as the binary case —
`wlc/420422/img/1Kings17v15.png`, 433,717 bytes, PNG magic intact, sha256 matching the committed
file.

**The inbound sweep was re-run across every clone and the distinct URL set is unchanged at 12.**
Raw occurrence counts have grown since Phase 0 and none of the growth is a new citation: MAM-basics
now contributes 18 hits of its own, 9 of them its dual-resident copies of
`in/UXLC-misc/all_changes.json` and `in/accgram/uxlc_accent_changes.json` and 5 of them this plan
file's own prose. There are **20 clones now, not the thirty this plan swept on 2026-08-03**, the
MAM-private programme having consolidated four of them. Six repos cite the old site: MAM-basics 18,
UXLC-utils 25, wlc-utils 13, document-index 4, MAM-simple 1, and **holman-ketiv-qere 1, which
Phase 0's five-repo sweep would not have reached** — see finding 5.

**`https://bdenckla.github.io/MAM-basics/wlc/accgram/` 404s, and it is recorded rather than
fixed**, as this phase requires: [#230](https://github.com/bdenckla/MAM-basics/issues/230), filed
in MAM-basics per this repo's "Two issue trackers" section. That issue states outright that the
404 is not evacuation damage, so that a Phase 9 redirect landing on it is not read as breakage.

#### Findings

**1. This phase's own verify list calls `wlc/index.html` a depth-1 page exercising `../style.css`,
and it is the one page on the site that references no stylesheet at all.** The list says "`style.css`
is referenced as `../style.css` from depth-1 pages and `../../style.css` from depth-2" and then
names four pages. Measured 2026-08-13: `gh-pages/wlc/index.html` sits *beside* `gh-pages/wlc/style.css`
and carries no `<link>` element whatever — it is a bare `<ul>` of seven links; the `../style.css`
pages are one directory below that, and the `../../style.css` pages two. So the four named pages
exercise three behaviours rather than two, and the unstyled one is the site's own wlc index.
**Nothing is broken, and that is exactly the risk**: a session reading the verify list would expect
a `../style.css` on `wlc/index.html`, and could read its absence as a Phase 5 regression in the very
computation Phase 5's finding 1 repaired. The check was run on both remaining depths instead, two
pages each, which is what the list was reaching for.

**2. The workflow needed no correction, so the "treat any difference as a finding" instruction
found nothing — and the byte comparison is what makes that worth saying.** Reading the six clauses
off the file and ticking them against the paragraph would have proved only that the clauses named
are right. `diff` against wlc-utils' copy proves there is nothing in the file the paragraph fails
to name, which is the stronger claim and the cheaper check.

**3. The licence map did not cover the new page, and the gap was between two statements rather
than inside either.** `DATA-LICENSES.md`'s GPL-3.0 paragraph enumerates `py/`, the Pages workflow
under `.github/`, `doc/` and `out/`; its table's three `gh-pages` rows are all under
`gh-pages/wlc/`. A file at `gh-pages/index.html` falls between the two and was named by neither.
It went in as a **table row** rather than a clause in the paragraph, so that a path lookup finds it
beside the other `gh-pages` rows, and the row says outright that it is not one of the pages the row
below dedicates to CC0 — the distinction Phase 4 was careful about, kept careful. It is GPL-3.0 as
MAM-basics' own work: written here, holding no corpus text, and never in `bdenckla/wlc-utils`.

**4. `/wlc/accgram/` 404s and always did, in both repos — measured on both sides, not inferred
from one.** `gh-pages/wlc/accgram/` holds 14 HTML pages and no `index.html`, and
`git -C ../wlc-utils ls-files gh-pages/accgram/index.html` returns nothing at `c501dc0`, so the
section served nothing before the copy and serves nothing after it. `wlc-utils/README.md:42`
advertises the directory regardless, which is what makes the 404 reachable. #230 carries the
detail, including that `gh-pages/wlc/index.html` links only 5 of the 14 pages individually, so the
other 9 are reachable only from inside the section or by citation.

**5. The sweep this plan prescribes reads five named repos, and a sixth now has a hit — which is
Phase 0's finding 1 surfacing in a new place.** holman-ketiv-qere's `py/mb_cmn/paths.py:83` carries
`bdenckla.github.io/wlc-utils/X`, this plan's own prefix-rewrite placeholder, because that file is
a **vendored copy** of MAM-basics' `py/mb_cmn/paths.py` — the very vendoring that Precondition 4
exists for. So it is not a URL to add: it is prose, and `X` is not a path. **The lesson for Phase
11's re-sweep is that the repo list must be derived rather than typed** — the five-repo command
this plan carries would have missed it, and a vendored copy of a file citing a real URL would have
been missed the same way.

---

## Phase 7 — Repoint the `420422` blob URL — DONE 2026-08-13

*In MAM-basics. Two lines.* Must land **before** Phase 10.

`gh-pages/wlc/420422/index.html` links
`https://github.com/bdenckla/wlc-utils/blob/main/out/diff_mm_wlc420_wlc422.json`, emitted by
`py/main_wlc_diffs_420422.py:11`. **This is a second URL surface, and it is easy to miss.** `out/`
is never deployed to Pages — `upload-pages-artifact` takes `path: gh-pages` only — so this is a
github.com blob link, untouched by the Pages redirect and killed outright when Phase 10 empties
`out/`.

Change the constant to `bdenckla/MAM-basics/blob/main/out/diff_mm_wlc420_wlc422.json`. **Its own
commit** — this is the single intentional artifact change in the whole plan, and folding it into
Phase 5 would put a real diff inside a zero-diff oracle.

**Verify:** regenerate; the diff is one source line and one `href`. Fetch the new blob URL: 200.
Then `git grep -n "bdenckla/wlc-utils" -- py gh-pages` finds nothing that is a link to *content*
rather than a citation of the repo.

### Execution record — Phase 7, 2026-08-13

Began at MAM-basics `56ac9f4`, wlc-utils `c501dc0`, holman-ketiv-qere `637237b`, with **the whole
Phase 6 baseline reproducing exactly** — MAM-parsed `95f64d7`, MAM-simple `bae0bff`, MAM-with-doc
`d2dc6e5`, MAM-OSIS `a037a76`, MAM-for-Sefaria `5f41c16`, UXLC-utils `4d70cf4`, MAM-private
`20dfb63`, every one of the ten clean, and `git worktree list` one line in each of MAM-basics and
wlc-utils. Precondition 4 checked on both logs as instructed: holman-ketiv-qere clean and last
committed 2026-08-12 23:05, and MAM-basics' own log showing nothing since but this plan's Phases 5
and 6. No mismatch anywhere, so this record has no baseline drift to report — the first phase of
which that is true.

**The change is one line, and the regeneration is exactly what the phase predicts.**
`_NOTE_DIFFS_JSON_URL` in `py/main_wlc_diffs_420422.py` now names `bdenckla/MAM-basics`;
`.venv/Scripts/python.exe py/main_wlc_diffs_420422.py` rewrote the page, and `git status` held
**two files and no others** — the source and `gh-pages/wlc/420422/index.html`, one insertion and
one deletion in each. Committed as `a8a9875`, alone, per this phase's own instruction. Suite **903
passed / 5 skipped**, unchanged from Phase 0's baseline; `ruff check py` clean; `black --check py`
clean at **770** files. Pages deploy run `31727592763`, green in 29 seconds, and the change was
verified **on the deployed site** to the standard Phase 6 set: `https://bdenckla.github.io/MAM-basics/wlc/420422/index.html`
serves the `bdenckla/MAM-basics` URL and its served bytes are sha256-identical
(`1d4e76f7edc78688…`) to the committed file.

The verification the phase asks for, in its own order: the diff is one source line and one `href`;
the new blob URL returns **200**; and `git grep -n "bdenckla/wlc-utils" -- py gh-pages` leaves
three hits, **none of them a link to content** — `printed_decalogue_simanim_page.py:140` and `:141`
are commented-out `issues/52` and `issues/56` citations, which belong in `bdenckla/wlc-utils`
because that tracker keeps its own 88 issues, and `mb_cmn/paths.py:246` is prose naming
`bdenckla/wlc-utils-private`, a **different repository** that the pattern catches as a prefix.
Zero hits under `gh-pages`.

#### Findings

**1. This phase's instruction to find the constant by the URL string rather than by line number
does not work as written, and the line number was right all along.** The plan says "`:11` — line
numbers drift, so find it by the URL string" — sound advice that fails here, because **the URL the
page carries appears nowhere in the source.** black split it across two adjacent string literals to
fit 88 columns:
`"https://github.com/bdenckla/wlc-utils/blob/main/out/" "diff_mm_wlc420_wlc422.json"`. So grepping
for the URL as the page spells it finds the page and not the generator that emits it. What does
find it is a distinctive *fragment* — `diff_mm_wlc420_wlc422.json`, or the constant name
`_NOTE_DIFFS_JSON_URL`. **The general lesson for the remaining phases is that a searchable anchor
has to survive the formatter**, and black's implicit concatenation is a formatter that silently
breaks long string literals in the middle. Prefer the identifier.

**2. The one-source-line diff was contingent on the destination name's length, with one character
to spare.** `MAM-basics` is one character longer than `wlc-utils`, so that line went from 87
columns to **exactly 88** — black's default limit, and black leaves it alone at 88. One more
character in the repository name and black would have re-wrapped the constant, making the diff two
or three source lines and quietly falsifying this phase's own "one source line" criterion. Nothing
was at risk here, because the criterion is a description of the change rather than a gate on it,
but a phase elsewhere that asserted a line count over a formatted file would have been.

**3. No circuit run, and that is the judgement this phase called for rather than an omission.**
`main_wlc_diffs_420422.py` is a **leaf**: it reads `py_wlc_diffs_420422/my_word_diffs_420422.py`, a
Python data module, and writes only under `gh-pages/wlc/420422/`; nothing downstream reads what it
writes. It is a mega step (`wlc-diffs-420422`, `main_0_mega.py:337`), so a full circuit would have
run it too — and would have rewritten the rest of the corpus around it, burying a two-line diff in
whatever else moved. **Running the one generator is not the cheap substitute for the circuit here,
it is the better evidence**, because the assertion this phase makes is about which files change and
a narrower run makes that assertion narrower. Phases 8 through 11 should ask the same question
before reaching for the two-command circuit: the circuit is the right tool when the claim is
"nothing else moved", and the wrong one when the claim is "exactly this moved".

**4. The repoint is unobservable from the response, and the page carries a second anchor to the
same file that nothing checks.** Both URLs return 200 today, and the two blobs are **the same
object** — `57439cd1843001b2381d3329b21c51783065ce8e` in MAM-basics and in wlc-utils alike — so
fetching either one cannot tell you which repository served it. **A later phase must therefore
verify this repoint by reading the URL string in the page, never by fetching it**; the fetch stops
being a distinguishing test only at Phase 10, when the wlc-utils copy goes and the old URL starts
404ing, which is the whole reason this phase comes first. The second anchor is the sentence the
link sits in: it states "196 note (bracket-note) changes", and the comment above it
(`main_wlc_diffs_420422.py`, in `_path_and_title_and_intro_for_main`) says the number is taken from
that JSON's "notes differences" array by hand and must be updated if the file is regenerated.
Checked while here, since the link and the number make one claim between them: the array holds
**196** entries, so page and file agree today. Nothing enforces it, and this phase deliberately did
not add a test for it — a count pinned in a test is the example-based shape `CLAUDE.md` rules out,
and the honest fix if it ever matters is to derive the number rather than assert it.

(A "Next is Phase 8" paragraph stood here until Phase 8 ran on 2026-08-13, and was deleted rather
than left, by the convention it stated: **one forward pointer per file, at the end of the latest
execution record.** It replaced a "Next is Phase 7" pointer at the end of Phase 6's record for the
same reason — a forward pointer is not a record of what the phase did, and two of them naming
different phases is precisely what misleads the fresh session this plan is written for. The live
one is at the end of Phase 8's record below.)

---

## Phase 8 — The redirect-stub generator — DONE 2026-08-13

*In MAM-basics only.* Nothing is published; it writes to a scratch directory.

New entry point `py/main_wlc_redirect_stubs.py` with `build` and `check` subcommands, a
`build_parser()` extracted out of `main()`, and a `Subcommands:` docstring block with name and
description on **separate** lines — `test_entry_point_subcommands.py` enforces both, and the
one-line form reads to its `fullmatch` as an empty block. Logic in `py/wlc_redirect/`.

**The listing is the site itself, not a file.** Derive the URL set from `git ls-files gh-pages/wlc`
filtered to `*.html` (154 today), strip the `gh-pages/wlc/` prefix, and that string is *both* the
old wlc-utils path and the new MAM-basics suffix. The stub set therefore cannot drift from the
site: a page added later gets a stub on the next run, one removed loses its stub.

Each stub, written to wlc-utils' `gh-pages/<path>`:

- `<link rel="canonical" href="https://bdenckla.github.io/MAM-basics/wlc/<path>">`
- `<meta http-equiv="refresh" content="0; url=https://bdenckla.github.io/MAM-basics/wlc/<path>">`
- a `<script>` doing `location.replace(target + location.search + location.hash)`
- a visible one-line human fallback link

**The JS is not belt-and-braces — it is the only thing that carries a fragment.** A meta-refresh
takes a fixed URL, and the incoming `#supplied-dt5v6-bet-atnax` is arbitrary; only JS can read and
re-append it. So with JS disabled the four UXLC-utils deep links land on the right page at the top
rather than at the anchor. **State that degradation in the generator's docstring** rather than
leaving it to be discovered.

Plus `gh-pages/404.html`: JS reads `location.pathname`, strips the leading `/wlc-utils/`, prepends
`/MAM-basics/wlc/`, re-appends search and hash, `location.replace`. GitHub Pages serves it with an
HTTP **404** status for any unmatched path — expected, and precisely why the 154 real stubs exist,
so that every URL anyone actually cites returns 200.

`check` asserts stub-set ↔ page-set correspondence and that each stub's target is the prefix
rewrite of its own path. That is a mechanical lint over generated text — the second of the two
allowed test shapes — not an example-based unit test.

**Verify:** `build --out <scratch>` produces 155 files; `check` passes; spot-read three stubs at
three depths; and confirm the generator resolves wlc-utils through
`paths.require_sibling("wlc-utils", paths.sibling_repo("wlc-utils"))` — **the last remaining
reference to the sibling in the whole tree.**

### Execution record — Phase 8, 2026-08-13

Began at MAM-basics `104d5db`, wlc-utils `c501dc0`, holman-ketiv-qere `637237b`, with **the whole
Phase 7 baseline reproducing exactly** — MAM-parsed `95f64d7`, MAM-simple `bae0bff`, MAM-with-doc
`d2dc6e5`, MAM-OSIS `a037a76`, MAM-for-Sefaria `5f41c16`, UXLC-utils `4d70cf4`, MAM-private
`20dfb63`, every one of the ten clean, `git worktree list` one line in each of MAM-basics and
wlc-utils, and the tracked counts at **1906** here and **626** there. Precondition 4 checked on
both logs as instructed: holman-ketiv-qere clean and last committed 2026-08-12 23:05, and
MAM-basics' own log showing nothing since but this plan's Phases 5 through 7. No mismatch anywhere,
so this record, like Phase 7's, has no baseline drift to report.

**Landed as two commits.** `6a7347d` is the generator and nothing else — `py/main_wlc_redirect_stubs.py`
plus `py/wlc_redirect/{stubs,build,check}.py`, 517 lines across four new files. `520dc27` is a
comment this phase made false, kept separate so the first commit's diff stays exactly the new
source files, which is this phase's verification (finding 1).

**The verification the phase asks for, in its own order.** `build --out .novc/wlc-rest-phase8/stubs`
writes **155 files** — 154 page stubs and `404.html` — and `check --dir` over them passes with exit
0. Three stubs read at three depths, and each names its own path's prefix rewrite in all four
carriers: `index.html` at depth 0, `accgram/supplied-marks.html` at depth 1 (the page UXLC-utils'
four fragment links point into), and `420422/full-record/420422-54.html` at depth 2 (one of
`document-index/README.md`'s four cited paths). The sibling resolution is
`py/wlc_redirect/stubs.py`'s `wlc_utils_pages_dir`, one call, spelled exactly as the phase
requires — but "the last remaining reference in the whole tree" is not true today and finding 1
says what is.

**`git status --porcelain` held only the four new source files, so no tracked artifact moved in
either repo**, which is this phase's whole claim and is why no circuit ran — Phase 7's finding 3
applied as written. wlc-utils came through at `c501dc0` with an empty status even after `check`
read all 154 of its pages; the eight other sibling repos were clean before and after.

**Phase 6's finding 4 checked rather than assumed, and the derivation gets all three cases right on
its own.** `420422/` and `wlc-a-notes/` — the two directory URLs `document-index/README.md` cites
without naming a file — each hold an `index.html`, so each gets a stub that a bare directory URL
reaches. `accgram/` holds none, so it gets none and falls to the `404.html` catch-all, which is
faithful: that URL 404s today and always did (#230). Nothing in the generator special-cases a
directory; the three outcomes fall out of filtering the page listing to `*.html`.

Suite **905 passed / 5 skipped / 57 subtests**, up 2 from the 903 that had held since Phase 0, and
**the delta is fully accounted for**: `test_entry_point_subcommands.py` discovers entry points by
scanning `py/main_*.py` for `add_subparsers(`, that count went 10 to 11, and it has two
parametrized tests, so the new entry point brings exactly two. No new test file was added, for the
reason under finding 3. `ruff check py` clean; `black --check py` clean at **774** files, up 4 from
Phase 7's 770 — the four new modules, one each.

#### Findings

**1. "The last remaining reference to the sibling in the whole tree" describes the state after
Phase 10, not the state this phase leaves.** Three sites in `py/` name wlc-utils as a sibling once
this phase lands, and they need three different dispositions, so Phase 10 should not read the
phrase as "delete the one that is left":

- `py/wlc_redirect/stubs.py`'s `wlc_utils_pages_dir` — the new one, and the one that stays. It is
  what Phase 9 writes through and what Phase 9's own verification lints with.
- `py/tests/test_h_dot_below_nfc.py:190` — the NFC scope. **This plan's own head paragraph already
  says Phase 10 deletes it**, and Phase 10's text names the lines, so the two statements were
  already in tension before this phase; the count was one because that head paragraph is about
  *routine* runs and this phase's verify line is about the tree.
- `py/tests/test_mb_cmn_paths.py:106` — **not a resolution at all, and it must stay.** It is the
  unit test proving `REPO_WLC_UTILS_DIR` and `REPO_WLC_UTILS_PRIVATE_DIR` are distinct environment
  variables rather than one shadowing the other; it resolves a fake `/pub` under a mocked
  environment and never looks at a clone. A Phase 10 sweep for the string `sibling_repo("wlc-utils")`
  would catch it, and deleting it would delete a test of the override chain that has nothing to do
  with wlc-utils existing.

The NFC scope's comment additionally read *"THE ONE PATH IN py/ THAT STILL LEAVES THIS CHECKOUT"*,
which this phase falsified. `520dc27` qualifies it to "in a routine run" and names the other one,
rather than bumping a count: the generator's path is **asked for** — nothing reaches it but
`check` with no `--dir`, and `build --publish` — so no mega step and no test reaches wlc-utils, and
a suite run and a circuit run still leave that repo alone, which is the property Phase 5 measured.

**2. A lint that has only ever passed is not known to work, and proving `check` can fail meant
pointing it at the real pages.** At Phase 8 there is no committed stub tree anywhere, so `check`'s
default target — wlc-utils' own `gh-pages/` — still holds the 154 real pages. That is the negative
test, and it is a good one: **654 problems, exit 1**, each page reported for naming the target in
no canonical link, no meta refresh and no script, and `404.html` reported absent. Three more
failure modes were exercised by hand on a copy of the scratch tree: a deleted stub (reported as a
published page with no stub), an added one (a stub standing in for no page), a target edited to
the wrong path (reported with both URLs it names), and a `--dir` that does not exist (reported as
a problem, **not** a skip, per `CLAUDE.md`'s missing-input rule). All four messages name the fix.

**3. The JavaScript is the one part this phase cannot execute, and Phase 9 is where it gets
exercised — do not let that slip.** The stubs sit in a scratch directory that nothing serves, and
there is no `node` on this machine, so the fragment-carrying `location.replace` and `404.html`'s
prefix strip are verified **by reading, not by running**. Phase 9 already names the right test —
*"The four fragment links are the acceptance test for the JS half specifically — check in a
browser that it lands on the anchor, not merely on the page"* — and this finding is here so that
line is read as load-bearing rather than as belt-and-braces. No pytest module was added for the
same reason it would have been circular: until Phase 9 lands there is no committed stub tree to
lint, and a test that built one to a temp directory first would be checking the generator against
itself. `check` is the lint, run by hand, which is what this phase's own text asks for.

**4. Where `build` writes by default was left open, and the answer is a safety decision Phase 9
needs to know about.** The phase says "writes them to a scratch directory and publishes nothing",
which describes this phase's run rather than the program's default. So `--out` defaults to the
gitignored `.novc/wlc-redirect-stubs/` and **`--publish` is what targets wlc-utils** — the safe
destination is the one you get by saying nothing, and writing into another repository takes saying
so. **Phase 9 runs `build --publish`**, and does not have to spell a sibling path. The two are a
mutually exclusive group, so neither can be given twice over. `build` deletes nothing: Phase 9's
removal of the 130 non-HTML assets is a `git rm` that phase does, and a stub whose page has since
gone is reported by `check` rather than silently cleaned up.

**5. `404.html` carries three of the four things a page stub carries, and the missing two are
missing for a reason.** It has no `<link rel="canonical">`, because it answers many paths and each
has its own current copy, and no `<meta http-equiv="refresh">`, because a meta refresh takes a
fixed URL and the URL here is derived from the path that was asked for. So it is the one file in
the tree with **no fixed target to compare**, and `check` gives it its own three requirements —
the script, the visible link, and the `/wlc-utils/` prefix it strips — rather than exempting it
from checking. Worth stating because the obvious implementation checks every `.html` the same way
and then either fails on `404.html` forever or skips it entirely.

(A "Next is Phase 9" paragraph stood here until Phase 9 ran on 2026-08-17, and was deleted rather
than left, by the convention Phase 7's record states: one forward pointer per file, at the end of
the latest execution record. The live one is at the end of Phase 9's record below.)

---

## Phase 9 — Flip wlc-utils' `gh-pages/` to stubs — DONE 2026-08-17

*In wlc-utils.* **Hard-gated on Phase 6 being deployed and HTTP-verified.**

One commit: 154 HTML files **modified in place** (a stub at the same path is a modification, not a
delete-plus-add, which keeps the diff readable), `404.html` added, and the 130 non-HTML assets
deleted (122 png, 3 js, 2 jpg, 1 xml, 1 woff2, 1 css). Nothing else changes.

### Why Pages must be live first

1. **A redirect to a 404 is worse than no redirect.** It turns a working URL into a confidently
   wrong one — and the five tanach.us citations and four UXLC-utils deep links are published where
   Ben cannot edit them, so nobody will report the breakage.
2. **Reversibility.** While wlc-utils still serves the real pages, every step is a `git revert`
   plus a redeploy. Once emptied, the public surface depends on a MAM-basics deploy nobody has
   observed succeeding, gated on a repo-settings change outside this plan's control. Emptying
   first gambles the only live copy on an action the plan cannot perform.
3. **The dual-live window costs nothing.** Two sites serving identical content harms nobody, and
   the `<link rel="canonical">` resolves the duplicate the moment the stubs land.

### Why alive beats archived

Archiving would be less work and would keep *both* surfaces — an archived repo is read-only but
its Pages site keeps serving, and its `blob/main/...` URLs keep resolving. It is rejected because
the pages would then be **frozen duplicates**: every page would exist twice on the web with no
signal which is current, Ben could not add a canonical tag afterwards (an archived repo cannot be
edited), and a reader arriving from tanach.us in 2029 would get the 2026 text with no hint that a
maintained version exists. A stub says "this moved"; an archive says nothing.

**Verify:** re-run the entire Phase 6 URL list against `bdenckla.github.io/wlc-utils/…` and
confirm each redirects to its MAM-basics equivalent. **The four fragment links are the acceptance
test for the JS half specifically — check in a browser that it lands on the anchor, not merely on
the page.** Then a path with no stub (`/wlc-utils/out/anything`) exercises `404.html`. Then
`main_wlc_redirect_stubs.py check` passes against the committed tree.

### Execution record — Phase 9, 2026-08-17

Began at MAM-basics `2951a01`, wlc-utils `c501dc0`, holman-ketiv-qere `637237b`, and **the whole
Phase 8 baseline reproduced with zero drift** — MAM-parsed `95f64d7`, MAM-simple `bae0bff`,
MAM-with-doc `d2dc6e5`, MAM-OSIS `a037a76`, MAM-for-Sefaria `5f41c16`, UXLC-utils `4d70cf4`,
MAM-private `20dfb63`, every one of the ten clean and pushed, `git worktree list` one line in each.
MAM-basics held **1910** tracked files and wlc-utils its unchanged **626**, of which `gh-pages/` was
**284**: 154 `.html` and 130 non-HTML, breaking down as 122 png, 3 js, 2 jpg, 1 xml, 1 woff2 and 1
css, exactly as this phase's brief states. Suite **905 passed / 5 skipped**, `ruff` clean, `black`
clean at **774** files. The manifest was re-taken before wlc-utils was touched, per Phase 0's
lesson, and is **byte-identical to Phase 0's** — 626 rows, sha256 `28c94cde4618…`.

**Precondition 4 was checked on both logs and was clear.** holman-ketiv-qere clean, no worktree,
last committed 2026-08-12 23:05 — still Phase 5's own re-vendor commit there rather than that
undertaking's work. MAM-basics' own log holds nothing from it either: everything since is this
plan's Phases 5 through 8. So Ben's statement of 2026-08-12 that the work is finished held for a
sixth phase running, on the evidence of both logs rather than one.

**Landed as one commit in wlc-utils, `f10f405`, in exactly the shape this phase specifies.**
`git status` before staging read **154 `M`, 130 `D` and one `??`**, and the staged diff **1 `A`,
130 `D`, 154 `M`**, with nothing outside `gh-pages/`. The 154 modifications in place are what keeps
the diff readable, and they were established rather than hoped for: the two page-path sets were
compared first and are identical, 154 for 154, so every stub landed on an existing page at its own
path. `404.html` is the one addition, wlc-utils having had none. The repo now tracks **497** files
— 626 − 130 + 1 — of which `gh-pages/` holds **155**, and **not one non-HTML file is left there**.

**`build --publish` wrote all 155 and deleted nothing, as Phase 8's finding 4 says it would.** The
130 removals are the `git rm` this phase does by hand: the list was derived from `git ls-files
gh-pages` filtered to non-`.html`, screened for odd characters and for stray `.html` rows before
use, and passed to `git rm --pathspec-from-file`. It left **no empty directories** — the three
`img/` trees and `woff2/` are gone from disk, and the seven directories remaining under `gh-pages/`
all hold HTML.

**The verification, in this phase's own order.**

1. **The deploy went green** — run `32076961634` on `f10f405`, conclusion `success`, 21 seconds.
   That workflow triggers on push to `main` only, and the push was a fast-forward with no force.
2. **The whole Phase 6 URL list was re-run against `bdenckla.github.io/wlc-utils/…`, and each
   serves a stub naming its MAM-basics equivalent.** The script is
   `.novc/wlc-rest-phase9/phase9_http_check.py`, and for each old URL it checks three things rather
   than one: HTTP 200; the served bytes sha256-identical to the committed stub, so a stale deploy
   fails; and the target the stub names, **which it then fetches and requires 200 of**, so a
   redirect to a 404 could not pass. Nothing is followed — **the redirect is client-side and never
   an HTTP 3xx** — so what is read is the served text.

| Old URL, under `https://bdenckla.github.io/wlc-utils/` | Result |
|---|---|
| `accgram/goerwitz.html` — the five tanach.us citations | 200, bytes match, names `…/MAM-basics/wlc/accgram/goerwitz.html`, which serves 200 |
| `accgram/supplied-marks.html` — the two MAM-basics CLC tests' corroboration URL, and the page the four deep links point into | 200, bytes match, target serves 200 |
| `accgram/printed-decalogue.html` — MAM-simple's link target | 200, bytes match, target serves 200 |
| `420422/`, `420422/full-record/420422-54.html`, `wlc-a-notes/` — three of `document-index`'s four deep paths | 200, bytes match, targets serve 200; both directory URLs resolve to their own stub |
| the old site root, `/wlc-utils/` | 200, bytes match, names `…/wlc/index.html`, which serves 200 |
| `accgram/` — `document-index`'s fourth, and wlc-utils' `README.md:42` | **404 carrying the forwarding script** — #230 behaving as designed, and it 404ed before this phase too |
| `out/anything`, `style.css`, `420422/img/1Kings17v15.png` — a path nobody ever published, and two assets this phase deleted | **404 carrying the forwarding script**, all three |

3. **The four fragment links were executed rather than read** — finding 1. A browser check is still
   owed, and it is Ben's to make; the four links went to him with this write-back.
4. **A path with no stub answers 404 *and* redirects**, which is what item 4 of the brief asks for:
   `/wlc-utils/out/anything` returns HTTP 404 and serves `404.html`, whose script forwards to
   `…/MAM-basics/wlc/out/anything`. GitHub Pages sets that status whatever the file then does.
5. **`check` with no `--dir` passes against the committed tree** — "154 stubs and 404.html, all
   correct", exit 0, with the working tree equal to `HEAD`. **And it is not the evidence that the
   assets went**: it globs `*.html`, so it would print that same line with all 130 still in place.
   The separate count is what proves that half — `git ls-files gh-pages | grep -vc '\.html$'` is
   **0**.

**MAM-basics was left alone, which this phase asserts rather than assumes.** Its suite is **905
passed / 5 skipped**, the Phase 8 figure exactly, and that is the cheapest evidence that a phase
operating in another repo touched nothing here; `ruff` clean; `black` clean at **774** files. No
Python was written, so black had nothing to format, and nothing under `gh-pages/` was regenerated.
At the end MAM-basics is at `2951a01` plus this write-back, and the other eight repos are each at
the commit they began at, all clean and all pushed.

#### Findings

**1. The JavaScript did get executed, and Phase 8's "there is no `node` on this machine" was true
without being the whole story: `cscript.exe` is a JavaScript engine, and every Windows install has
one.** Phase 8's finding 3 records the fragment-carrying `location.replace` and `404.html`'s prefix
strip as verified by reading rather than by running, and names this phase as where they would first
run — meaning in a browser, which only Ben can drive. They ran here first instead. Windows Script
Host's JScript (`C:/Windows/System32/cscript.exe`) executes the stubs' ES3-simple code verbatim, so
`.novc/wlc-rest-phase9/run_stub_js.js` reads the committed bytes out of wlc-utils' tree, extracts
each `<script>` body, `eval`s it against a fake `location` that records the URL instead of
navigating, and compares against the expected target. **Eleven cases, all correct.** All four
published deep links land on `…/wlc/accgram/supplied-marks.html#supplied-…` with the fragment
intact. `404.html`'s prefix strip — an `indexOf`/`slice` pair, and the only real logic anywhere in
the stubs — is right on a deleted asset, a deep deleted image, the `accgram/` directory, a
query-plus-fragment, and the else branch a path outside `/wlc-utils/` takes, which sends the reader
to the new site root rather than concatenating nonsense.

**What it proves and what it does not.** It proves the string arithmetic, which is the part that
could have been wrong and the part nothing had ever run. It does not prove that a browser honors
`location.replace`, nor that a browser scrolls to the anchor on arrival — those are properties of
the browser rather than of this code, so the browser check stays owed. **What has changed is that
the browser check now confirms a mechanism instead of discovering one**, which is a materially
different risk to be carrying into Phase 10. The general lesson is that "there is no JavaScript
runtime on this machine" is worth one command to re-check rather than inheriting from an earlier
phase: the runtime that is always present on Windows is the one nobody lists.

**2. The frozen reference described under "The oracle question" dies at this phase — one phase
earlier than the sentence saying so.** That section ended: *"Until Phase 10 deletes it, wlc-utils
holds 626 files no program writes any more, so `git diff --no-index` between the trees re-derives
layer 1 on demand at any point in Phases 3–9."* Phase 9 is the last phase it names and is the phase
that falsifies it. For `gh-pages/` the reference is gone: all 154 pages were overwritten and the 130
assets deleted, so 284 of the 620 moved files have no original left to compare against — **and 154
of those 284 still exist at the same path holding entirely different bytes**, which is worse than
their being absent, because a `diff --no-index` run in ignorance reports 154 differences that look
like catastrophic move damage. What survives is worth naming precisely: **336 of the 620** — `out/`
193, `in/` 135, `doc/` 6, `data/` 1 and the Pages workflow — are untouched and stay comparable until
Phase 10. The sentence was corrected in place rather than left to mislead, this file being the
authority a fresh session works from.

**3. A `grep -P` that fails on this machine's locale reads exactly like a check that found
nothing.** While the removal list was being built, its paths were screened for spaces and non-ASCII
with `grep -nP '[^\x21-\x7e]' || echo "(none)"`. Git Bash here answers **`grep: -P supports only
unibyte and UTF-8 locales`** and exits non-zero, so the `||` fired and printed the reassuring
"(none: all plain ASCII, no spaces)" **having examined nothing**. The screen was redone with a POSIX
class under `LC_ALL=C` and did then pass — 130 plain-ASCII paths, no spaces — so nothing was at
risk. The shape is what is worth recording: a check whose failure is indistinguishable from its
success, which is the silent-green failure this repo's `CLAUDE.md` rules against in tests, arriving
in a shell command instead. **An `|| echo "(none)"` fallback converts any error into a pass.** A
`git rm` of 130 files is precisely where a silently-skipped path screen would have cost something.

**4. A directory URL's stub sends the reader to the explicit `index.html` rather than to the
directory, and that is correct — recorded so it is not later read as a defect.**
`document-index/README.md` cites `/420422/` and `/wlc-a-notes/` without naming a file, and GitHub
Pages serves each from that directory's `index.html`; the stub lives in that file, so the target it
names, and its `<link rel="canonical">`, are `…/wlc/420422/index.html` rather than `…/wlc/420422/`.
Both forms serve the page at the new site — the target was fetched at 200 — so nothing is broken,
and naming one of two equivalent URLs is exactly what a canonical link is for. It falls out of
Phase 8's derivation, where a stub's target is the prefix rewrite of its own **path**; no special
case for directories could be added without the generator learning which paths a server resolves to
an index, which is the server's fact rather than the tree's.

(A "Next is Phase 10" paragraph and its three hand-off bullets stood here until Phase 10 ran on
2026-08-17, and were deleted rather than left, by the convention Phase 7's record states: one
forward pointer per file, at the end of the latest execution record. All three hand-offs were
taken — the 161, the last use of the frozen reference, the three dispositions — and Phase 10's
record accounts for each. The live pointer is at the end of that record below.)

---

## Phase 10 — Empty the rest of wlc-utils — DONE 2026-08-17

*In wlc-utils, plus one commit here.* Pure subtraction with no published effect. Worth an explicit
look before running, as the Python plan's Phase 4 was.

Delete `out/` 193, `in/` 135, `doc/` 6, `data/` 1, `wlc-utils.code-workspace`. Keep `LICENSE`
(CC0, and now correct for a repo holding nothing but generated HTML), `.gitignore`,
`.gitattributes`, `.github/workflows/pages.yml`, and `gh-pages/` (155 files).

**`README.md`** becomes one screen: this repo is a redirect host; the site is at
`https://bdenckla.github.io/MAM-basics/wlc/`; the mapping is a pure prefix rewrite; it moved on
`<date>`; **the repo still exists because 154 published URLs are cited from places Ben cannot
edit** — tanach.us' UXLC change list, UXLC-utils' CLC pages, MAM-simple, document-index; its 88
issues are still live and read here; the data and code are in `../MAM-basics`; the pre-evacuation
history is intact here.

**`CLAUDE.md`** shrinks to those facts plus the two only an agent needs, which are the most
valuable lines in the phase: **`gh-pages/` is generated — do not hand-edit it; regenerate with
`MAM-basics/py/main_wlc_redirect_stubs.py`**, and **there is no Python and no data here; `doc/`
moved to `MAM-basics/doc/`**. Keep the "a bare `#NN` here means a wlc-utils issue" note. Drop the
`doc/agent-planning-principles.md` pointer, which now names a file in another repo — Phase 11
repoints its readers.

**In MAM-basics, same session:** delete the wlc-utils `_Scope` at `test_h_dot_below_nfc.py:157-167`,
`_WLC_EXCLUDE_DIR_PREFIXES` at `:118`, and the `import wlc_paths` at `:50`. **Two of those three
anchors have moved or gone — locate them by name, per Phase 7's finding 1.** Checked 2026-08-13:
`_WLC_EXCLUDE_DIR_PREFIXES` is at `:142` and the `_Scope` around `:180-210`, both found by
identifier; and **there is no `import wlc_paths` left to delete**, Phase 5 having deleted that
module outright on 2026-08-12, so that third item is already done rather than pending.

**And do not sweep for the string `sibling_repo("wlc-utils")` — one of its three sites must
survive.** `py/wlc_redirect/stubs.py`'s `wlc_utils_pages_dir` is the redirect generator's own
resolution and is what keeps working after this phase; `py/tests/test_mb_cmn_paths.py:106` is not a
resolution at all but the unit test proving `REPO_WLC_UTILS_DIR` and `REPO_WLC_UTILS_PRIVATE_DIR`
are distinct environment variables, resolving a fake `/pub` under a mocked environment. Only the
NFC scope above goes. Phase 8's finding 1 has the reasoning. What survives in
wlc-utils is a README, a CLAUDE.md and 155 generated stubs; the scope's own comment says its floor
of 10 exists *"to catch an exclusion filter that swallowed EVERYTHING, not to assert a tree
size"*, and scanning 154 generated files is not what it was written for. Deleting a `_Scope`
changes no test count — the four scanning tests simply cover fewer files. Update the module
docstring's "THREE REPOS ARE SCANNED" at `:8`.

**Verify:** `git ls-files` in wlc-utils prints **161** paths and nothing else (this line said 160
until Phase 10 ran — one too low, exactly as Phase 9's record predicted: 497 − 336 = 161, the 155
stubs plus the six root files this phase's own prose keeps); the Phase 9 URL checks
still pass after the deploy; `py/main_test.py` here unchanged; the full circuit here still gives a
zero diff. Check for untracked residue — `git rm` leaves it behind — though wlc-utils has no
`.venv` as of 2026-08-03.

### Execution record — Phase 10, 2026-08-17

Began at MAM-basics `69931be`, wlc-utils `f10f405`, holman-ketiv-qere `637237b`, and **the whole
Phase 9 baseline reproduced with zero drift** — MAM-parsed `95f64d7`, MAM-simple `bae0bff`,
MAM-with-doc `d2dc6e5`, MAM-OSIS `a037a76`, MAM-for-Sefaria `5f41c16`, UXLC-utils `4d70cf4`,
MAM-private `20dfb63`, every one of the ten clean and pushed, `git worktree list` one line in each.
MAM-basics held **1910** tracked files and wlc-utils its post-flip **497** — `gh-pages` 155, `out`
193, `in` 135, `doc` 6, `data` 1, `.github` 1, six loose root files. Suite **905 passed / 5
skipped**, `ruff` clean, `black` clean at **774** files.

**Precondition 4 was checked on both logs and was clear** for a seventh phase running:
holman-ketiv-qere clean at `637237b`, last committed 2026-08-12 23:05 — still Phase 5's own
re-vendor commit — and MAM-basics' own log holding nothing but this plan's Phases 5 through 9.

**The explicit look happened before the delete, as this phase's own text asks.** The list was
derived by `git ls-files out in doc data wlc-utils.code-workspace` — **336 rows** — then screened
for spaces and non-ASCII under `LC_ALL=C` with a POSIX class and **no `|| echo` fallback**, Phase
9's finding 3 applied as written (all 336 plain ASCII, screen exit 1 = no matches); then read in
full. Zero `gh-pages/` paths in it; the nine `.html` it does hold are `in/` WLC release notes and
UXLC licence pages, deletable; nothing outside the five named items.

**Layer 1 was re-derived one final time immediately before the delete, because afterwards there is
no original left to compare.** The 335 moved files being deleted plus the surviving Pages workflow,
compared by blob SHA-1 against this repo's copies: **330 byte-identical, zero missing, zero mode
mismatches, and the 6 differing exactly the six Phase 5's record names** — the two survey JSONs
Phase 5 itself was working, and the four files of the UXLC refresh. `wlc-utils.code-workspace` is
the 336th deletion and was never copied, by Phase 0's disposition.

**Landed as wlc-utils `cd668e3`**: staged exactly **336 `D` plus 2 `M`** — the two rewritten
instruction files — and nothing else. `README.md` is one screen saying the repo is a redirect
host, why it stays alive, and that its issues and history stay; `CLAUDE.md` holds the two agent
facts this phase calls its most valuable lines, plus the `#NN` convention. The repo now tracks
**161** files — the count Phase 9 measured, against this phase's own since-corrected 160 — and
`git status --porcelain --ignored` shows **no untracked residue**: only the pre-existing ignored
`.claude/` and `.novc/`, and no `.venv`, as expected since 2026-08-03. The four deleted trees are
gone from disk with no empty directories left. **A second commit `8250b69` followed within the
hour** — finding 3 — and the koren note moved here rather than dying (finding 3 again). Both
deploys went green: runs `32079069852` and `32079886541`.

**In MAM-basics, `aa7f269`.** The wlc-utils `_Scope` and `_WLC_EXCLUDE_DIR_PREFIXES` are deleted —
located by identifier, per Phase 7's finding 1 — and there was indeed **no `import wlc_paths` to
delete**, exactly as the 2026-08-13 check predicted. The module docstring's "THREE REPOS ARE
SCANNED" reads TWO, and the floor-guard rationale the deleted scope's comment carried ("to catch an
exclusion filter that swallowed EVERYTHING, not to assert a tree size") moved into the UXLC-utils
scope's comment, which had leaned on it by reference ("for the same reason wlc-utils' is").
`sibling_repo("wlc-utils")` is down to **exactly the two sites Phase 8's finding 1 says survive**:
the redirect generator's own resolution, and `test_mb_cmn_paths.py`'s override unit test. No sweep
was run; the two survivors were checked by name. `CLAUDE.md` received the koren note per Phase 0's
disposition and the 93-issue correction (finding 1), and one docstring
(`wlc_chanted_word_residue_page.py`) had its live forward reference to the two-accents plan
repointed at this repo's `doc/` copy, the wlc-utils path it cited having been deleted this phase.

**The verification, in this phase's own order.**

1. **`git ls-files` in wlc-utils prints 161 paths and nothing else** — 155 under `gh-pages/`, six
   at the root — re-measured at `8250b69` after both commits.
2. **Every Phase 9 URL check passes unchanged after the deploy** — `phase9_http_check.py` re-run in
   full: seven stubbed paths at 200 with served bytes sha256-identical to the committed stubs and
   every named target itself fetched at 200; the served stub re-appends `location.hash` and all
   four fragment anchors are present at their destinations; all four catch-all paths 404 carrying
   the forwarding script. **Nothing this phase deleted was served, and the checks confirm it.**
3. **Suite 905 passed / 5 skipped**, the Phase 8 figure exactly — deleting a scope changes no test
   count, the four scanning tests just cover fewer files. `ruff` clean; `black --check` clean at
   **774** files, unchanged, no file having been added or removed.
4. **The full circuit gives a zero diff in all ten repos.** `main_0_mega.py` exit 0,
   `main_edition_transcription.py build --check` 12/12; afterwards nine repos read `git status
   --porcelain` empty and MAM-basics held exactly this phase's three source edits. The vendoring
   audit rewrote its four artifacts to identical bytes — finding 5 predicted it would, wlc-utils
   having held no Python since 2026-08-01 and no policy entry. And layer 3 directly: an mtime
   snapshot over wlc-utils' whole working tree before the mega, compared after — **zero touched,
   zero appeared, zero vanished** across 165 files. `check` with no `--dir` still lints the
   committed stub tree green.

#### Findings

**1. The "88 issues" the plan and both repos' instruction files repeat is five short, and was on
the day it was first written.** The tracker holds **93** issues (27 open, measured 2026-08-17), and
#89–#93 were filed **2026-07-31** — before the 2026-08-01 Python move that every statement of "88"
is dated to. So the figure was never a count that later drifted; it was five short from the start,
and it propagated from file to file unre-measured for seventeen days. The rewritten `README.md` and
`CLAUDE.md` in wlc-utils say 93 with the measurement date; this repo's `CLAUDE.md` sentence was
corrected in `aa7f269`; the plan's own historical "88"s above stand as history. The general lesson
is the plan's own re-measure rule applied to a figure nobody thought of as a measurement: an issue
count is one.

**2. The scope's floor guard made the edit order inside this phase mandatory, which "deleting a
`_Scope` changes no test count" is true of only at the end state.** With wlc-utils emptied, the
wlc scope's in-scope set is the six root files minus nothing — **6 files, under its floor of 10**
— so a suite run between the `git rm` and the scope deletion errors `setUpClass` for all four
scanning tests. That is the floor doing precisely what its comment says it is for: an emptied tree
is indistinguishable from an exclusion filter that swallowed everything, and it refuses to pass
over a hollow scan. The suite was accordingly run only after the scope deletion, and the guardrail
sentence now lives in the UXLC scope's comment with this episode cited.

**3. The rewrite of wlc-utils' instruction files needed a correcting commit within the hour, and
all three corrected sentences were inherited from the file being replaced.** `8250b69` fixed:
the claim that `main_repo_maintenance.py` wipes wlc-utils' `.novc/` — it stopped on 2026-08-12,
when Phase 5 repointed the writers, so the old `CLAUDE.md` had itself been stale for five days and
the rewrite copied the staleness forward; the claim that no mega step reaches the repo — the
closing vendoring audit *reads* every sibling on disk, so the true claim is about writes and is
now stated as such; and a "generates all of it" whose antecedent covered `doc/`, which no program
generates. The koren note also moved to this repo's `CLAUDE.md` in the same pair of commits,
executing the disposition Phase 0's table recorded rather than quietly keeping the note where the
shrink instruction would have deleted it. The lesson: a rewrite-from-scratch re-asserts every
sentence it keeps, so each inherited sentence needs re-verifying against today, not against the
file it came from.

**4. Two different sets in this plan are both called "336", and they differ by one file each
way.** The five deletions total 336 — the 335 moved files plus `wlc-utils.code-workspace`, which
never moved. The comparable remainder of the frozen reference was also 336 — the same 335 plus
`.github/workflows/pages.yml`, which survives this phase and was never deleted. They overlap in
335. Nothing was miscounted anywhere; the coincidence is just primed to read as an off-by-one to
anyone re-deriving one figure from the other, so the pre-delete comparison above names its set
explicitly.

**5. `in/vendoring_policy.json` has no wlc-utils entry, so Phase 11 item 6's justification is
stale while its conclusion holds.** The item says "no change; the wlc-utils entry went in
`ea9f199`" — but the policy today names repos only for vendored *Python package* copies, and
wlc-utils has held no Python since 2026-08-01; whatever `ea9f199` added is gone. "No change" is
still the right answer, on the simpler ground that there is nothing there to change. Two more
hand-offs for Phase 11's item 1 while it edits this repo's `CLAUDE.md`: the "Two issue trackers"
section's closing paragraph still says a bare `#NN` read in wlc-utils' `doc/` and `in/` means a
wlc-utils issue — directories this phase deleted, whose byte-identical copies now sit in *this*
repo's `doc/` and `in/` still carrying those bare wlc-utils citations, which deserves the saying;
and the section's opening can now cite 93 rather than nothing, `aa7f269` having already made that
correction.

(A "Next is Phase 11" paragraph and its three hand-offs stood here until Phase 11 ran on
2026-08-17, and were deleted rather than left, by the convention Phase 7's record states: one
forward pointer per file, at the end of the latest execution record. All three hand-offs were
taken — item 6's stale-but-right justification, the two additions to item 1's `CLAUDE.md` edit,
and the 93-with-a-date for item 10's commit message — and Phase 11's record accounts for each.
Phase 11 was the last phase, so no live pointer replaces this one anywhere: the plan is complete.)

---

## Phase 11 — Cross-repo bookkeeping — DONE 2026-08-17

*In MAM-basics, plus two places neither repo's tooling can see.* One commit here.

1. **`MAM-basics/CLAUDE.md`** — *"The fullest statement of this rule, with the evidence behind it,
   is in the sibling repo: `wlc-utils/doc/agent-planning-principles.md`"*. Now local:
   `doc/agent-planning-principles.md`, and "in the sibling repo" must go. A genuine improvement —
   the rule's fullest statement comes home to the repo that practises it.
2. **`~/.claude/CLAUDE.md`** (global, tracked in `github-misc` at `dot-claude/CLAUDE.md`, which
   does **not** auto-sync) cites `wlc-utils/doc/agent-planning-principles.md` twice. Edit the live
   copy, then copy it back to the repo and commit — the drift is silent otherwise.
3. **The `hebrew-prose` skill**, live at `~/.claude/skills/hebrew-prose/` and tracked at
   `github-misc/dot-claude/skills/`, two copies that do not sync. **Six of its wlc-utils
   references become wrong**: `doc/agent-planning-principles.md`, `doc/review-findings-2026-07-29.md`
   and `doc/edition-transcription-workflow.md` (all three now under `MAM-basics/doc/`); the
   `file:///…/wlc-utils/gh-pages/accgram/maqaf-nonfinal-accents.html` link in
   `references/rendered-prose.md:147` (now `MAM-basics/gh-pages/wlc/accgram/`); and
   `out/accgram/maqaf-nonfinal-accents.json` in `references/sources-and-corpora.md:189`. What
   stands: the `wlc-utils#NN` citations, that tracker keeping its 88 issues. Edit **both** copies
   and verify byte-identical after.
4. **`py/repo_util/check_repo_standards.py`** discusses wlc-utils in prose at `:25-31`, `:39`,
   `:45-48`, `:456-462`. Follow the convention already used there: append to the dated blame-crawl
   paragraphs, rewrite only what is false as written. Its `has_tracked_py` gate already handles a
   Python-less wlc-utils correctly. **Predict this**, so it is not read as a new finding: the NFC
   findings in `in/UXLC-39/Psalms.xml`, `in/UXLC-misc/all_changes.json` and
   `in/accgram/uxlc_accent_changes.json` **disappear from the wlc-utils report and reappear under
   MAM-basics**, where Phase 3's exclusions cover them.
5. **`in/repo_maintenance_policy.json`** — wlc-utils is not in `frozen_repos` today. After Phase
   10 it genuinely is: nothing there is hand-edited and its one tracked tree is regenerated from
   here. Adding it is a real decision, not a formality — **put it to Ben.**
6. **`in/vendoring_policy.json`** — no change; the wlc-utils entry went in `ea9f199`, so
   `test_vendoring_policy_paths.py` does not fire here as it did in UXLC-utils' Phase 4.
7. **`all-repos.code-workspace:88` and `MAM-basics.code-workspace:25`** — leave `../wlc-utils` in
   both. The repo still exists and still receives commits from the stub generator.
8. **`py/repo_util/run_black.py`** — no change; it already records *"Skipped: no tracked .py files
   in this repo"*. Confirm on the next sweep.
9. **`UXLC-utils/doc/clc-design.md`** names `wlc-utils/out/wlc422-kq-u/`, `wlc-utils/py/accgram/`
   and others across ~20 lines. The Python plan's Phase 4 record settled the cheap answer for
   exactly this shape: **one sentence in that repo's `CLAUDE.md`** saying every `wlc-utils/…` path
   in `doc/` now means `../MAM-basics/…`, rather than twenty edits.
10. **wlc-utils' 88 issues stay in `bdenckla/wlc-utils`, and this plan does not change that.**
    `CLAUDE.md`'s "Two issue trackers" section holds unaltered: a bare `#NN` in MAM-basics means
    MAM-basics, a wlc-utils issue is written `wlc-utils#NN`, and `wlc_issue_edit.py` keeps its
    required `repo` argument and its deliberately bare `#69` example. **Say so in the commit
    message**, so nobody reads a fully-evacuated wlc-utils as licence to "tidy" the split.
11. **Update both PLAN files' Status tables**, and add a paragraph to
    `PLAN-evacuate-python-programme.md` recording that its carried decision 2 — "`gh-pages/` stays
    put indefinitely" — **has now been broken once, deliberately, and how**. Five of the six repos
    still in that programme have a `gh-pages/`, and they will cite this as precedent.

### Execution record — Phase 11, 2026-08-17

Began at MAM-basics `2658c02`, wlc-utils `8250b69`, holman-ketiv-qere `637237b`, and **the whole
Phase 10 baseline reproduced with zero drift** — MAM-parsed `95f64d7`, MAM-simple `bae0bff`,
MAM-with-doc `d2dc6e5`, MAM-OSIS `a037a76`, MAM-for-Sefaria `5f41c16`, UXLC-utils `4d70cf4`,
MAM-private `20dfb63`, github-misc `81fdcec`, every one of the eleven clean and pushed,
`git worktree list` one line in each of MAM-basics and wlc-utils, tracked counts **1910** here and
**161** there. Suite **905 passed / 5 skipped / 57 subtests**, `ruff` clean, `black` clean at
**774** files — measured before the phase and again after it, unchanged both times.

**Precondition 4 was checked on both logs and was clear** for an eighth phase running:
holman-ketiv-qere clean at `637237b`, last committed 2026-08-12 23:05 — still Phase 5's own
re-vendor commit there — and MAM-basics' own log holding nothing but this plan's Phases 5
through 10.

**Landed as four commits across three repos, wlc-utils touched by none of them**: MAM-basics
`1026778` (items 1 and 4, the freeze lift, and item 11's paragraph, with item 10 said in its
message) plus this write-back; UXLC-utils `f99610a` (item 9); github-misc `5801305` (items 2 and
3). All pushed fast-forward, no force. The one Pages deploy the MAM-basics push fired went green
(run `32082549902`, 28 s) and republished identical content, nothing under `gh-pages/` having
changed.

**The items, in order.**

1. **`CLAUDE.md`** — the tests-rule sentence reads "in this repo: `doc/agent-planning-principles.md`"
   now, dated; and the "Two issue trackers" closing paragraph carries what Phase 10's finding 5
   handed this item: the six `doc/` files that arrived 2026-08-12 are named one by one, and they
   and the wlc trees under `in/` still carry bare `#NN` citations that mean wlc-utils issues —
   the one standing exception to "a bare `#NN` here means MAM-basics". The 93 was already in
   place from `aa7f269` and needed nothing.
2. **`~/.claude/CLAUDE.md` + `github-misc/dot-claude/CLAUDE.md`** — asked first, per the plan,
   and Ben chose the plan's scope. **Five sites fixed, not the banked four** (finding 1): the
   `agent-planning-principles.md` and `edition-transcription-workflow.md` citations, the
   `file:///` example link (now `MAM-basics/gh-pages/wlc/accgram/`), and the two "short pointer
   in wlc-utils' `CLAUDE.md`" clauses — Tests section and maqaf section — which Phase 10's
   rewrite had orphaned and which now name MAM-basics' `CLAUDE.md`. The six `wlc-utils/py/...`
   sites stale since 2026-08-01 stay flagged, per the plan and per Ben. Pair byte-identical
   before and after.
3. **The `hebrew-prose` skill, both copies** — Ben chose the widest offered scope, **ten sites**
   (finding 2): the plan's six (`agent-planning-principles.md` in `SKILL.md` and `verifying.md`,
   `review-findings-2026-07-29.md` in `SKILL.md`, `edition-transcription-workflow.md` and the
   `file:///` link in `rendered-prose.md`, the survey's JSON-and-page pair in
   `sources-and-corpora.md`, with `gh-pages/` nesting as `gh-pages/wlc/`); the two paragraphs
   Phases 9–10 falsified — `SKILL.md`'s closer, which called wlc-utils "a data-and-docs repo"
   with "88 issues" and now says redirect host and 93 measured 2026-08-17, and `verifying.md`'s
   "writes into wlc-utils' `out/` and `gh-pages/` as a sibling — the corpus did not [move]",
   which now names MAM-basics' own trees; and two touch-ups — `terminology.md`'s "venv was left
   on disk" (removed by 2026-08-03) and `SKILL.md`'s description line, which no longer lists
   wlc-utils as a place prose gets written. Pair byte-identical before and after.
4. **`check_repo_standards.py`** — two dated appends in the file's own convention: the
   `has_tracked_py` gate's wlc-utils example records the 2026-08-17 emptying, and the
   doc/-standard paragraph says its six surviving doc files are this repo's now. **The scan was
   re-run rather than assumed, and the prediction confirmed exactly** (finding 4): wlc-utils'
   report reads `NFC_H_DOT=0; NFC_LATIN=0`, and MAM-basics' carries Phase 3's seven sequences at
   the very same line numbers, beside two pre-existing MAM-basics-native findings.
5. **`frozen_repos` — Ben decided NO ENTRY** (finding 3), with the mechanics in front of him:
   the freeze has been structural since 2026-08-07, the register documents paused client
   projects with a thaw procedure that cannot even be stated for wlc-utils, wlc-utils stays in
   both workspace files receiving stub-generator commits — and `run_black.py:140` still consults
   the register, so an entry would have made it load-bearing again for exactly this one repo.
6. **`in/vendoring_policy.json`** — verified: no wlc-utils key anywhere in the file (its `repos`
   object names eight repos), so "no change" holds on Phase 10 finding 5's simpler ground.
7. **Both workspace files keep `../wlc-utils`** — verified at `all-repos.code-workspace:61` (the
   plan's `:88` drifted) and `MAM-basics.code-workspace:25`. **Reversed for one of the two files
   by Ben's decision, 2026-08-22, `7ddd6da`** ("rm UXLC-utils & wlc-utils from workspace"): that
   commit removed `../wlc-utils` and `../UXLC-utils` from `MAM-basics.code-workspace`, taking it
   from 8 folders to 6, and touched nothing else. `all-repos.code-workspace` still lists both
   (`:58` and `:61`), so the black sweep's reach is unchanged. Recorded here on 2026-08-22 by the
   follow-up to `doc/review-findings-2026-08-22.md`'s finding 5, which found the decision in no
   plan.
8. **`run_black.py`** — confirmed on a sweep scoped to wlc-utils: `REPO=wlc-utils;
   BLACK_ATTEMPTED=False; BLACK_OK=False; Skipped: no tracked .py files in this repo`.
9. **UXLC-utils' `CLAUDE.md`** — one paragraph beside its existing `py/`-paths substitution
   rule: every `wlc-utils/...` path in `doc/` means `../MAM-basics/...`, except
   `wlc-utils/data/lci_recs.json` (cited in `clc-design.md` §6), which the move also renamed to
   `in/lci_recs.json` — the carve-out this plan's inbound-links section requires.
10. **Said in `1026778`'s commit message**: the issue split stands, `wlc_issue_edit.py` keeps its
    required `repo` argument and its deliberately bare `#69` example, and both repos' instruction
    files now say 93 with a measurement date.
11. **This plan's Status table row and this record are the write-back**; the programme plan got
    the decision-2 break paragraph, placed inside decision 2 itself. **Its Status table holds no
    row about this plan, so "both PLAN files' Status tables" resolves to one table plus that
    paragraph** (finding 5).

**The freeze lift is executed, not just noted**: `doc/PLAN-two-accents-on-one-chanted-word.md`'s
notice now opens "FROZEN 2026-08-11 … and the freeze LIFTED 2026-08-17, at
`MAM-basics/doc/PLAN-evacuate-the-rest-of-wlc-utils.md`'s Phase 11, exactly where its own terms
said it would", and the one clause the freeze had left false-in-waiting ("they simply do not run
yet") is gone. That plan is parked, not resumed: lifting the freeze starts nothing.

#### Findings

**1. Item 2's banked scope was an undercount and its own "twice" an overcount — the same file
measured differently at three dates.** The item (2026-08-03) says the global `CLAUDE.md` cites
`agent-planning-principles.md` twice; today it cites it **once**, the file having moved on since.
Phase 0 (2026-08-11) banked 19 wlc-utils references with **four** to fix; today `grep` matches 21
lines with **five** to fix, because **Phase 10's rewrite of wlc-utils' `CLAUDE.md` falsified the
two "short pointer in wlc-utils' `CLAUDE.md`" clauses** — a consequence no bank predicted, since
Phase 0's sweep ran six days before the shrink was executed. The general lesson is the plan's
own re-measure rule applied to its own banks: a banked measurement of a live file is a
prediction, and the re-measure is the deliverable.

**2. Item 3 grew the same way and for the same reason.** The six named sites reproduce — at
drifted line numbers (`rendered-prose.md:147`→`:192`, `sources-and-corpora.md:189`→`:223`) — and
two whole paragraphs had been falsified since the item was written: `SKILL.md`'s closer and
`verifying.md`'s Commands intro, both describing the pre-evacuation division of labour between
the two repos, both carrying the "88 issues" figure Phase 10's finding 1 corrected. Ben took all
ten fixes, the two touch-ups included.

**3. Item 5's premise aged out from under it, and the answer followed the mechanics rather than
the premise.** The item (2026-08-03) predates the 2026-08-07 structural freeze; by execution day
the register was documentation of clones moved out of `GitRepos`, with a thaw procedure that
cannot be stated for wlc-utils. The live wrinkle put to Ben: `run_black.py:140` still consults
the register, so an entry for a repo still in the workspace would flip its sweep note to
"Skipped: frozen" — the register becoming load-bearing again for exactly one repo, against the
policy file's own "it is documentation" sentence. Ben chose no entry.

**4. Item 4's NFC prediction confirmed to the line number, which is more than it promised.** The
seven moved sequences appear in MAM-basics' report at **exactly** Phase 3's positions —
`Psalms.xml:758`, `all_changes.json:21749,21757,33951,33982`, `uxlc_accent_changes.json:8489,8497`
— despite Phase 5's UXLC refresh having added 996 lines to `all_changes.json`, all of them
evidently past `:33982`. The report also holds two findings that did NOT move in — the
`#`-comment hit at `py/py_wlc_a_notes/my_wlc_a_notes.py:360` and `in/mam-go/B-NevRish.csv:2900`,
both MAM-basics-native and pre-existing — named here so nobody reads them as evacuation residue.

**5. Item 11's "both PLAN files' Status tables" names a second table with nothing to update.**
`PLAN-evacuate-python-programme.md`'s Status table tracks that programme's own six repos and
never carried a row about this plan, so the item resolves to: this plan's table, plus the
decision-2 break paragraph that file did get. Recorded so nobody re-derives a missing obligation
from the word "both".

---

## Risks, and what could go wrong irreversibly

- **Emptying a published site while uneditable citations point at it is the only genuinely one-way
  step.** Not because bytes are lost — they are in wlc-utils' 99 MB `.git` forever — but because a
  silently-wrong redirect generates no complaint. tanach.us' five citations are the sharpest case.
  This is what the Phase 6 → Phase 9 gate exists for; do not collapse those phases even if both
  look ready in one session.
- **Fragments survive only via JavaScript.** Four published deep links depend on it. A stub whose
  script has a typo still redirects (the meta-refresh fires) and still looks fine to a status
  check — it just silently drops the anchor. Test a fragment link in a real browser, not `curl`.
- **A stale `wlc_paths` call site is invisible to `git status`**, because it rewrites a file to
  identical bytes. Phase 5's mtime snapshot is the only thing that catches it, and if Phase 10
  lands before it is caught the generator starts failing on a directory that no longer exists —
  loud, but a phase late. **Retired 2026-08-12: the snapshot was taken and found zero touched
  files, so there is no stale call site to find. A DIFFERENT invisibility bit this phase instead,
  and Phase 8 should carry it forward — a path computed from a path PART rather than from an
  accessor is invisible to any search for the accessor. Phase 5's finding 1.**
- **Concurrent page work destroys the oracle.** `PLAN-two-accents-on-one-chanted-word.md` is live
  and generates accgram pages. Precondition 1, and Ben's call.
- **Enabling Pages publishes `gh-pages/` and only `gh-pages/`** on a repo that has published
  nothing until now. Re-read `path: gh-pages` before the first deploy: it is the one place in this
  plan where a mistake makes something public.
- **Files change under you mid-session.** wlc-utils moved under the Python plan's own final
  session. Re-check `git status` and `git log` in both repos before staging, and commit by hunk.

---

## How to run this plan across sessions

**This file is the orchestrator; no live session needs to stay open**, and no session needs to
remember anything from the one before it.

**The MAM-private interlock is SPENT — that programme completed on 2026-08-11, and there is
nothing left there to schedule around.** What "Interactions with the MAM-private programme" above
still holds is history plus two live entanglements, which no completion removes: Phase 5 moving
the two accessors that programme repointed (find them **by function name**, since that programme
ran second and they are in `mb_cmn/paths.py` now, not `py/wlc_paths.py`), and Phase 11 sharing two
unsynced live-plus-tracked file pairs with that programme's R.4. The paragraph this replaces told
a scheduler to check whether a MAM-private phase was live; none can be.

**The scheduling constraint that replaced it is Precondition 4** — holman-ketiv-qere, Ben's
decision of 2026-08-11. Check that before scheduling any phase.

Each session reads this file, does exactly **one** phase, verifies it, then writes the result back
into the Status table — state, date, commit shas — and marks that phase's heading `— DONE <date>`,
recording the numbers actually measured and anything the plan did not predict. A phase whose
result is not written back cannot be judged by the next session. Then spawn a task chip for the
next phase quoting this file's absolute path.

**Stop and ask Ben rather than chaining on** at these five points:

- ~~**Precondition 1**, the two-accents plan — land it or freeze it.~~ **Asked and answered
  2026-08-11: Ben chose freeze.** Struck rather than deleted so a later session does not re-ask a
  settled question. See Precondition 1.
- **Phase 3**, the `data/lci_recs.json` → `in/lci_recs.json` rename, if he disagrees.
- ~~**Before Phase 3**: whether `.github/workflows/pages.yml` lands with the rest of `.github/` and
  publishes the site at Phase 3, or is deferred to Phase 6.~~ **Asked and answered 2026-08-11: Ben
  said "Let it land."** Phase 3 publishes. Struck rather than deleted so it is not re-asked; that
  phase's decision box carries the four obligations it puts on Phase 3.
- **Before Phase 5**, the largest phase, which must complete within one session.
- ~~**Phase 6**, which needs a GitHub settings change only he can make.~~ **Done 2026-08-11: Ben
  enabled Pages**, and correctly chose no starter workflow. Phase 6 still has manual verification
  in it — the HTTP list, checked in a browser and not by `curl` — but no longer waits on a setting.
- **Before Phase 9**, which changes what the public sees.
- ~~**Phase 11 items 2, 3 and 5** — two untracked-copy edits and one policy decision.~~ **Asked
  and answered 2026-08-17**: items 2 and 3 executed at the scopes Ben chose, item 5 decided as
  no entry. Phase 11's record has all three.

Phases 0, 1, 2, 4, 7, 8 and 10 are safe to chain automatically once their verification passes.

**SETTLED 2026-08-11, by measurement, at MAM-basics `73f8ea3`: a worktree run of the suite is
IDENTICAL to a main-checkout run — 903 passed, 5 skipped, 57 subtests, zero failures — provided
`REPOS_ROOT=C:/Users/BenDe/GitRepos` is set.** Taken in a throwaway `git worktree add --detach`
created for the purpose, on the main clone's venv by absolute path, and removed after; it dirtied
nothing in any of the ten repos. **919 is dead**, and so is the "12 unreal failures" / "13 unreal
failures" the two paragraphs this replaces argued over: there are no unreal failures any more,
because `38a3bc7` repointed seventeen callers of `read_books_from_mam_parsed_plus` off their
cwd-relative `"../MAM-parsed"` default on 2026-08-07, and Phase 1's `0008eb8` fixed the provenance
half on 2026-08-11. Re-measure rather than trusting this paragraph, but expect the main-checkout
count, whatever that has become.

**`REPOS_ROOT` is load-bearing, and it fails loudly rather than silently** — measured in the same
worktree without it: **18 collection errors**, every one a `FileNotFoundError: sibling repo <name>
not found` naming both environment overrides, so pytest stops at collection and reports nothing as
passing. That is `require_sibling` working as designed, and it is the reason no session has ever
been misled into a green worktree run that verified nothing.

**So the old instruction — "run the test suite and every generator from the main checkout, never
from a worktree" — is withdrawn for the SUITE and stands for the GENERATORS.** The suite reads
sibling repos and writes none, so a worktree run of it is now a first-class way to run it. The
generators are a different matter and the ban on them is untouched: this plan's verifications are
zero-diff and zero-mtime assertions over wlc-utils, MAM-private and the other siblings, none of
which any MAM-basics worktree isolates — which is the whole reason the evacuation exists. Phase
1's own verification still says not to run the suite from a worktree *as part of that phase's
checking*, and that is a narrower and still-sound instruction: it is about not spending a
verification budget on a second variable.

(A fourth paragraph stood here until 2026-08-11, saying the instruction stands regardless of the
number, on the ground that this plan's verifications are zero-diff and zero-mtime assertions over
siblings a worktree does not isolate. That ground is right and is now the third paragraph above,
where it says what it actually governs — the generators. It was deleted rather than left, because
after the split it would have read as re-banning the suite runs the first paragraph just
permitted.)
