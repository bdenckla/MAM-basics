# Evacuate the rest of wlc-utils into MAM-basics

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

**Phases 0 and 1 are done, both on 2026-08-11. No file has moved yet**, no GitHub setting has been
touched, and wlc-utils holds the same 626 tracked files it always did, still at `c501dc0`. Phase 0
is a preflight and Phase 1 edits only `py/mb_cmn/provenance.py` and its test, so the only thing
either changed in that repo is the freeze notice Phase 0 was asked to land there — see
Precondition 1. Phases 2 through 11 are unstarted. (This paragraph read "Nothing has been
executed. Every phase below is unstarted" until Phase 0 ran, and named Phase 0 alone until Phase 1
ran.)

Written 2026-08-03, on the model of `doc/PLAN-evacuate-python-from-wlc-utils.md`, which is its
precedent in shape and in discipline. Every number below is stated with the command that
re-establishes it, because the tree will have moved on. **Re-measure before relying on a figure,
and treat a mismatch as a finding rather than as noise.**

Repos are `C:\Users\BenDe\GitRepos\wlc-utils` and `C:\Users\BenDe\GitRepos\MAM-basics`. Only
MAM-basics has a `.venv`; wlc-utils' was removed after the Python left (checked 2026-08-03 —
`ls .venv` there finds nothing, so the Python plan's Phase 4 note about a leftover 80 MB venv is
stale).

## Status

| Phase | State |
|---|---|
| 0 — Preflight: baseline, manifest, collision census | **DONE 2026-08-11**, MAM-basics `5344a74` + this write-back, plus three baseline commits in three other repos and one freeze commit in wlc-utils (`c501dc0`). Every census claim re-measured and every one reproduces, the load-bearing zero-self-links figure included. The circuit ran green and **wlc-utils came through it with zero files changed**. **The baseline was NOT clean at first look — 17 files across three repos, from three unrelated causes**, all now committed. Suite is **903 passed / 5 skipped**, not the 913 this plan carried. Three findings this plan did not predict, the sharpest being that **a sibling repo's vendoring drifts this repo's own tracked tree**. Findings under Phase 0 below |
| 1 — The provenance worktree fix | **DONE 2026-08-11.** All three remaining pieces landed: step 2 in MAM-basics `0008eb8`, the tautology-test repairs in the same commit, and the al-hatorah wrapper **retired** in MAM-private `20dfb63` after `c0540e5` pulled the new vendored copy. The re-vendor ripple cost three more commits in three repos — MAM-simple `bae0bff`, MAM-basics `1097530` and `57b83cf` — and MAM-with-doc `d2dc6e5` for a by-design drift the circuit surfaced. Baseline reproduced exactly: **903 passed / 5 skipped**, ruff and black clean at 771 files, wlc-utils' manifest byte-identical and **wlc-utils unmoved at `c501dc0` throughout**. Seven findings, the sharpest being that **this phase's own verification (b) was stale and tested the wrong thing** — `38a3bc7` had already made a worktree run come out right, and the generator the plan names writes no breadcrumb at all. Finding 7 also **settles the long-unverified worktree suite count**: 903 / 5 from a worktree with `REPOS_ROOT` set, identical to the main checkout, zero unreal failures, 919 dead. Findings under Phase 1 below |
| 2 — `.gitattributes` merge | **not started** |
| 3 — Copy the corpus in (dual residency) | **not started** |
| 4 — Licence scoping | **partly landed 2026-08-10, outside this plan**: the root-level structure exists — `DATA-LICENSES.md` (path-by-path map plus the MAM CC-BY-SA statement) and `README.md`'s `## License` section — because MAM-basics' own MAM and chabad.org data had the same ambiguity with no wlc-utils involved. Remaining: add the arriving wlc paths as rows, and place CC0 only where Phase 4's "Where CC0 must NOT go" paragraph allows |
| 5 — Collapse `wlc_paths.py`; repoint every generator | **not started** |
| 6 — Pages live on MAM-basics — ~~**manual gate**~~ **no gate left** | **not started**, and **narrowed 2026-08-11**: its manual gate was Ben enabling Pages, done that day, and its "copy the workflow" step moved to Phase 3, which now publishes the site (Ben: "Let it land"). What remains here is `gh-pages/index.html`, checking the pins against the file Phase 3 landed, and the HTTP list |
| 7 — Repoint the `420422` blob URL | **not started** |
| 8 — The redirect-stub generator | **not started** |
| 9 — Flip wlc-utils' `gh-pages/` to stubs — **gated on 6** | **not started** |
| 10 — Empty the rest of wlc-utils | **not started** |
| 11 — Cross-repo bookkeeping | **not started** |

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
`C:\Users\BenDe\OneDrive\Documents\ScansOfBooks`) — an absolute, out-of-repo, **read-only** input
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
for r in MAM-basics MAM-simple UXLC-utils document-index wlc-utils; do git -C "../$r" grep -hIo "bdenckla\.github\.io/wlc-utils[A-Za-z0-9/._#-]*" -- . ; done | sort | uniq -c | sort -rn
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
`C:\Users\BenDe\GitRepos\MAM-private\doc\PLAN-evacuate-private-repos.md`; its Status table is the
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
page edit. **A plan parked in a `doc\*.md` is already harmless**, and so is an open GitHub issue:
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

**Re-measure wlc-utils' baseline rather than trusting this file's figures.** Its HEAD was
`5783062` when the counts under Scale were taken, `3760b2f` a few hours later, and `79404fa` when
Phase 0 began on 2026-08-11 — so that repo moves under this plan exactly as the Python plan's own
final session found.

---

## Interactions with the MAM-private programme — recorded on both sides

`C:\Users\BenDe\GitRepos\MAM-private\doc\PLAN-evacuate-private-repos.md`, written 2026-08-07,
evacuates masorah-books, al-hatorah, wlc-utils-private and mgketer into `bdenckla/MAM-private`.
It carries a section titled "Interactions with the wlc-rest plan — recorded on both sides"; this
is the corresponding note on this side. First written 2026-08-08 against that plan's original
blanket rule ("never interleaved with the wlc-rest plan's phases"); rewritten later the same
day, after that plan's `57fb4a3` replaced the blanket rule with a traced three-tier one and
corrected a provenance claim this note had copied from its first draft.

**The overlap rule, mirrored from that plan's Sequencing section — three tiers, by which of its
four repos is in play:**

- **wlc-utils-private: never overlap with any phase of this plan.** The tie is
  `py\main_wlc_json_and_unicode.py`, which splits its output between two roots (`:57`, `:65`):
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
  accessors in `py\wlc_paths.py`, and both run this repo's suite and read its pass count.
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
`MAM-private\wlc-utils-private\`, so every "zero diff in both repos" assertion here extends to
a third tree — require MAM-private clean before each circuit run and unchanged after it, except
where a phase's own edits explain the diff.

Two entanglements outlive the contention, and no amount of scheduling removes them:

1. **Phase 5 moves two accessors that plan repoints.** `wlc_utils_private_dir`
   (`py\wlc_paths.py:146`) and `al_hatorah_phonetic_dir` (`:159`, with
   `require_al_hatorah_phonetic_dir` at `:170`) leave `py\wlc_paths.py` for `mb_cmn\paths.py`
   here, and that plan's R.2 for wlc-utils-private and for al-hatorah rewrites exactly those.
   Both sit inside the "14 live sibling accessors" range Phase 5's table moves verbatim —
   verified 2026-08-08, between `mam_simple_dir` at `:109` and `require_uxlc_utils_dir` at
   `:179`, checked because the table elided the fourteen names behind an ellipsis; the table now
   names these two. **Whichever programme executes second finds them in the other file — locate
   them by function name, never by path.**
2. **Phase 11 and that plan's R.4 edit the same two unsynced pairs of files** — the live
   `~\.claude\CLAUDE.md` with its tracked twin at `github-misc\dot-claude\CLAUDE.md`, and the
   live `~\.claude\skills\hebrew-prose\` with its tracked twin at
   `github-misc\dot-claude\skills\hebrew-prose\`. Neither pair syncs, both programmes flag their
   edits stop-and-ask-Ben, and two sessions editing one unsynced pair is precisely how a copy
   goes stale unnoticed. Whichever runs second re-verifies both pairs byte-identical before
   adding to them.

**A third entanglement was recorded here on 2026-08-08 and withdrawn the same day.** This note's
first version claimed that Phase 1's expectation of retiring al-hatorah's `aht_provenance.py`
wrapper is void once al-hatorah nests under MAM-private, "whose origin basename is
`MAM-private`". That plan's `57fb4a3` corrected the claim by reading the code:
`mb_cmn\provenance.py`'s `_display_path` walks a fixed `parents[2]`, so a vendored copy at
`MAM-private\al-hatorah\py\mb_cmn\` lands on a directory still named `al-hatorah`, and the
breadcrumb stays right with no override. Nor does Phase 1's step 2 change that when it lands:
the derivation chain reads `repo_root/.git`, which for a tree nested inside MAM-private does not
exist, so the chain degrades to `repo_root.name` — `al-hatorah`, the right answer. The exposure
would need a derivation that walks *up* to MAM-private's `.git`, which Phase 1's chain
deliberately does not do. What the correctness actually depends on — the vendored copy sitting
exactly two levels below its tree root — is verified at that plan's R.2 rather than assumed.

One thing this plan hands that plan rather than owes it: **`wlc-utils\doc\` moves into
`MAM-basics\doc\` at Phase 3**, and that plan's prose table cites
`wlc-utils\doc\PLAN-two-accents-on-one-chanted-word.md` for its masorah-books path references. It
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

---

## The oracle question: what replaces "copy, don't move"

The Python plan's Phase 3 had an independent oracle because two copies of the code wrote the same
artifacts. **Data cannot be run twice.** Three layers replace it, and each covers exactly what
the others cannot.

**Layer 1 — blob-hash manifest identity, which proves the copy.** `git ls-files -s` in wlc-utils
yields 626 rows of `<mode> <sha1> 0\t<path>`. After the copy the same command in MAM-basics,
restricted to the destination paths, must yield **the identical 626 SHA-1s**, differing only in
path. Git blobs are content-addressed, so this is exact byte-identity — and it is the *only*
evidence covering the 122 PNGs, 2 JPGs, 2 PDFs, the woff2 and the extensionless
`in/Tanach-26.0--UXLC-1.0--2020-04-01/Images/Background`, which no program regenerates and which
layer 2 therefore says nothing about. Exactly two path deltas are expected: the `gh-pages/` →
`gh-pages/wlc/` prefix on 284 files, and `data/lci_recs.json` → `in/lci_recs.json`.

**This is why Phase 2 must precede Phase 3**: `git add` applies `.gitattributes` at add time, and
a differing eol rule changes the blob.

**Layer 2 — zero regeneration diff, which proves the repoint.** After Phase 5, run the full
circuit from `C:\Users\BenDe\GitRepos\MAM-basics`. **THE CIRCUIT IS NOW TWO COMMANDS, NOT ELEVEN
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

**And the frozen reference is the original tree.** Until Phase 10 deletes it, wlc-utils holds 626
files no program writes any more, so `git diff --no-index` between the trees re-derives layer 1
on demand at any point in Phases 3–9.

---

## Phase 0 — Preflight: baseline, manifest, collision census — DONE 2026-08-11

*Read-only, plus one commit to this plan file.* No tracked artifact changes.

**That description held for the reading and did not survive the baseline.** Phase 0 turned out to
need **five** commits across five repos, because the circuit it runs to establish a clean baseline
found the baseline dirty. The execution record at the end of this section says which and why.

**Re-measure and record** the table under Scale, plus: `py\main_test.py` — **913 passed, 5
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
`.novc\wlc-rest-phase0\wlc-manifest-c501dc0.txt`, **626 rows**, sha256
`28c94cde461849fbffd53ac16de12a6d9f4eb1804a9ce95e1baa212ea51c1ade`. The first was taken at
`79404fa` (sha256 `b4169ae8a82ebb62fa87fd71b98f31fb4f82e231efcc091f89b4d37ab7583ae5`) and was
invalidated within the hour by this phase's **own** freeze commit, `doc/PLAN-two-accents-…md`
being one of the 626. The two differ in **exactly one row**, that file's blob, proved by `diff`
and kept in `.novc\` beside it. **The lesson for a later phase is that "no second chance to take
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
step reads every sibling repo**, so MAM-basics' `doc\vendoring-inventory.md` and its three
`out\vendoring_*` artifacts went stale, 154 files to 155. **The direction is the counter-intuitive
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
pairs are **byte-identical right now** — `~\.claude\CLAUDE.md` against
`github-misc\dot-claude\CLAUDE.md`, and `~\.claude\skills\hebrew-prose\` against
`github-misc\dot-claude\skills\hebrew-prose\` — which is the state Phase 11 item 3 requires
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
then `\turl = https://github.com/bdenckla/MAM-basics.git`, confirmed by `cat -A` — so an eight-line
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
2026-08-03; (b) one breadcrumb-writing generator — `py\main_wlc_a_notes.py` — run from a throwaway
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
behaviour. And the generator it names, **`py\main_wlc_a_notes.py`, writes no provenance breadcrumb
at all** — `grep` for "generated by" across `gh-pages/wlc-a-notes/` finds nothing, so there was
never anything there for a worktree name to poison. The probe was re-run with a generator that
does write one: `py\main_accgram.py survey-chanted-word-accents`, whose
`out/accgram/chanted-word-accents.json` carries `MAM-basics/py/accgram/chanted_word_accents.py`.
Run from a worktree named `phase1-probe`, it rewrote that file (mtime moved) and the breadcrumb
was unchanged, wlc-utils staying clean. **All 62 breadcrumbs wlc-utils holds come from
`py/accgram/` generators** — 37 of them from `prose_run` alone — so an accgram subcommand is what
a later phase should reach for, not `main_wlc_a_notes.py`.

**2. So step 2 needed a probe of its own, and what it needs is a checkout whose DIRECTORY NAME
differs from the repo's** — which no checkout on this machine has, since a worktree is covered by
steps 1 and 3. The shapes were built instead, in the throwaway
`.novc\phase1_probe_origin_basename.py`, which copies `provenance.py` into fabricated trees and
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
therefore been redundant since 2026-08-10.** `mb_cmn\provenance.py` walks a fixed `parents[2]`, so
in `MAM-private\al-hatorah\py\mb_cmn\` it lands on a directory named `al-hatorah` **that has no
`.git` of its own**; the chain reaches its last step and answers `al-hatorah`, which is the right
answer. The old code did the same, for the same reason. The same holds inside a MAM-private
worktree, whose copy of that tree is `<worktree>\al-hatorah`, so the worktree hazard the wrapper
existed for cannot arise there at all. This confirms the prediction of the withdrawn third
entanglement under "Interactions with the MAM-private programme" and sharpens it: nesting, not the
derivation, is what makes the name stable. The pull was still owed, to keep the vendored copy in
sync. `repo_paths.REPO_NAME` was **kept**, as this phase says: `view_model.py`'s
`_generated_by_path` still formats an `al-hatorah/...` path itself. Output-neutral, checked rather
than argued — `py\main_3d_make_override_diff_viewer.py` regenerated with **no artifact change at
all** and its breadcrumbs still read `al-hatorah/py/main_3d_make_override_diff_viewer.py`;
al-hatorah's `py\main_test.py` passes 3 tests.

**5. The re-vendor ripple has an ordering, and this session got it wrong and paid one extra
commit.** `vendoring/compare.py` derives `last_synced` from the date of the last commit touching
each file in the **destination** repo, so committing a re-vendored copy anywhere is itself a
change the next audit reports. **Commit the destination repos first, then run the audit, then
commit the audit.** Done the other way round it takes a second audit commit, which is what
`57b83cf` is. It does converge — `doc\vendoring-inventory.md` and `out\vendoring_*` live here and
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

## Phase 2 — `.gitattributes` merge

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

---

## Phase 3 — Copy the corpus in (dual residency)

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
rename. Then `py\main_test.py` at its Phase 0 count; `git status --porcelain` empty in wlc-utils
(nothing was touched) and clean here after the commit.

---

## Phase 4 — Licence scoping

*In MAM-basics.* Small, and best done while the arriving trees are still obviously separable.

**Half of this phase already landed, on 2026-08-10; Phase 4 is now the other half.** The
root-level structure was built then, because the same ambiguity already existed in MAM-basics
without wlc-utils: MAM-basics tracks MAM text in `in/mam-ws/`, `in/mam-go/`,
`in/mam-from-sefaria/`, `in/mam-from-Sefaria-2021-11-23/` and `in/mam-ws-bot-edits/`, text derived
from those in `out/mam-ws-parsed-fmt-2/`, `out/mam-ws-bot/`, `out/tmpl-survey-plain/` and
`out/tmpl-survey-plus/`, and third-party material in `in/chabad-ctr/` — all of it covered by
nothing but the root GPL-3.0 and silence. Two files now exist in
`C:\Users\BenDe\GitRepos\MAM-basics`: **`DATA-LICENSES.md`**, a path-by-path table followed by the
MAM CC-BY-SA 4.0 statement copied verbatim from
`C:\Users\BenDe\GitRepos\MAM-parsed\LICENSE.md`; and a **`## License` section at the end of
`README.md`** naming the two declarations. **So this phase extends an existing map rather than
starting one — add rows to `DATA-LICENSES.md`; do not write a second document, and do not restate
the map in `README.md`.**

**wlc-utils is CC0 1.0; MAM-basics is GPL-3.0.** Moving 626 data files from one to the other
either silently withdraws a published public-domain dedication or leaves the status ambiguous.
(This paragraph read "They are the only two of Ben's thirty repos with a `LICENSE` file at all,
and neither README mentions licensing" until 2026-08-10. Both halves were wrong:
`diffable-pointed-hebrew` carries an MIT `LICENSE`, and six repos — MAM-parsed, MAM-simple,
MAM-with-doc, MAM-OSIS, MAM-for-Sefaria and phonetic-hbo — carry a `LICENSE.md` holding the MAM
CC-BY-SA statement. Re-establish with `ls C:\Users\BenDe\GitRepos\*\LICENSE*`.)

Ben's decision, 2026-08-03: **keep GPL-3.0 at the root for code, and scope CC0 to the moved data.**
Place a verbatim copy of wlc-utils' CC0 `LICENSE` at each arriving tree that holds only Ben's own
work — `gh-pages/wlc/LICENSE`, and one covering the wlc portions of `in/` and `out/`. Prefer the
fewest declarations that unambiguously cover the moved paths over one per directory.

**Where CC0 must NOT go — checked 2026-08-10, and it narrows the decision above rather than
reversing it.** Kimball's `in/Tanach-26.0--UXLC-1.0--2020-04-01/License.html` grants two different
things: the biblical Hebrew text "may be viewed or copied without restriction", but "All other
files and the look-and-feel of the site are copyrighted by the publisher and require written
permission for any purpose." Two arriving trees are mostly those other files — `in/wlc420/` and
`in/wlc422/` hold `WLCmanual420.pdf`, `WLC_Manual422.pdf` and five release-notes HTML pages
between them, no biblical text among them. A CC0 file placed over the arriving `in/` wholesale
would dedicate Kimball's copyrighted manual to the public domain, which is not Ben's to do.

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

---

## Phase 5 — Collapse `wlc_paths.py`; repoint every generator

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

1. Full circuit from `C:\Users\BenDe\GitRepos\MAM-basics`. `git status --porcelain` here shows
   **only the source edits**; none of the 620 landed files changed.
2. **Snapshot wlc-utils' mtimes before and compare after: zero files touched.** This is the direct
   test of the collision fix, and an empty `git status` there is not sufficient — a stale call
   site rewrites a file to identical bytes.
3. Snapshot MAM-basics' mtimes too and record how many of the 620 were rewritten. Expect roughly
   509. Report the ~111 static files as proved by layer 1 only.
4. `py\main_test.py` at its Phase 0 count; `ruff check py` and `black --check py` clean.
5. `py\main_edition_transcription.py build --check` — 12/12 committed `.txt` bodies re-derived.
6. **The claim under Context, tested directly:** `git grep -n "wlc_paths\|wlc-utils" -- py` finds
   no path construction, only prose and issue citations.

---

## Phase 6 — Pages live on MAM-basics

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

---

## Phase 7 — Repoint the `420422` blob URL

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

---

## Phase 8 — The redirect-stub generator

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

---

## Phase 9 — Flip wlc-utils' `gh-pages/` to stubs

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

---

## Phase 10 — Empty the rest of wlc-utils

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
`_WLC_EXCLUDE_DIR_PREFIXES` at `:118`, and the `import wlc_paths` at `:50`. What survives in
wlc-utils is a README, a CLAUDE.md and 155 generated stubs; the scope's own comment says its floor
of 10 exists *"to catch an exclusion filter that swallowed EVERYTHING, not to assert a tree
size"*, and scanning 154 generated files is not what it was written for. Deleting a `_Scope`
changes no test count — the four scanning tests simply cover fewer files. Update the module
docstring's "THREE REPOS ARE SCANNED" at `:8`.

**Verify:** `git ls-files` in wlc-utils prints 160 paths and nothing else; the Phase 9 URL checks
still pass after the deploy; `py\main_test.py` here unchanged; the full circuit here still gives a
zero diff. Check for untracked residue — `git rm` leaves it behind — though wlc-utils has no
`.venv` as of 2026-08-03.

---

## Phase 11 — Cross-repo bookkeeping

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
  loud, but a phase late.
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
ran second and they are in `mb_cmn\paths.py` now, not `py\wlc_paths.py`), and Phase 11 sharing two
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
- **Phase 11 items 2, 3 and 5** — two untracked-copy edits and one policy decision.

Phases 0, 1, 2, 4, 7, 8 and 10 are safe to chain automatically once their verification passes.

**SETTLED 2026-08-11, by measurement, at MAM-basics `73f8ea3`: a worktree run of the suite is
IDENTICAL to a main-checkout run — 903 passed, 5 skipped, 57 subtests, zero failures — provided
`REPOS_ROOT=C:\Users\BenDe\GitRepos` is set.** Taken in a throwaway `git worktree add --detach`
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
