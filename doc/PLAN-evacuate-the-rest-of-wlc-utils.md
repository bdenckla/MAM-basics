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

**Nothing has been executed.** Every phase below is unstarted: no file has moved, no GitHub
setting has been touched, and wlc-utils is exactly as it was.

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
| 0 — Preflight: baseline, manifest, collision census | **not started** |
| 1 — The provenance worktree fix | **partly landed 2026-08-07, outside this plan**: `38a3bc7` (closing #216) added the worktree `.git`-pointer derivation — steps 1 and 4 of the chain. Remaining: step 2 (the `remote.origin.url` basename, the step that also covers a renamed clone — `grep origin py/mb_cmn/provenance.py` finds nothing), the tautology-test repairs (`test_mb_cmn_provenance.py`'s `_repo_name()` still returns `this_repo_name()`), and the al-hatorah wrapper decision. Re-measure at Phase 0 |
| 2 — `.gitattributes` merge | **not started** |
| 3 — Copy the corpus in (dual residency) | **not started** |
| 4 — Licence scoping | **not started** |
| 5 — Collapse `wlc_paths.py`; repoint every generator | **not started** |
| 6 — Pages live on MAM-basics — **manual gate** | **not started** |
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
4. **CC0 is scoped to the moved trees**, GPL-3.0 stays at the root for code. Phase 4.

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

## Preconditions — all three blocking

**1. `wlc-utils/doc/PLAN-two-accents-on-one-chanted-word.md` must land or freeze first.** It is
live — 1134 lines, §9 is the current state, Phase 4 next — and it generates accgram pages, which
are members of the 154-page set this plan proves itself against by zero diff. This is the same
contention the Python plan's Precondition 2 named between itself and the maqaf-scans plan, and it
was decisive there: concurrent artifact changes mean this plan cannot tell a move bug from a page
edit. **Ben's call, needed before Phase 3.**

**2. Pages enabled on `bdenckla/MAM-basics` — Settings → Pages → Source: GitHub Actions.** Only
Ben can do this; the plan does not attempt it. It is a hard gate on Phase 6.

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

**Re-measure wlc-utils' baseline rather than trusting this file's figures.** Its HEAD was
`5783062` when the counts under Scale were taken and `3760b2f` a few hours later, so that repo
moves under this plan exactly as the Python plan's own final session found.

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
in parallel, not even a phase of this plan. This plan waits, and resumes at Phase 0 once that
repo's R.4 write-back lands.** That plan's `22e7e7f` records the same settlement, scopes the
one-unit run as the single exception to its one-phase-per-session discipline, and closes three
of its gates so the run cannot stall midway. The paragraph above stands as the record of the
alternatives not taken.

**Ben, 2026-08-08, later the same day: the two programmes run strictly serially, as whole
blocks — the interleaving the tiers above license goes deliberately unused.** The coordination
that interleaving would need was judged delicate and error-prone on both sides. The order:
wlc-utils-private (its R.0–R.4 run was already live when this was recorded), then this plan
complete, Phases 0 through 11, then the remaining three MAM-private repos. No mgketer or
masorah-books phase runs as filler during this plan's manual gates. The three-tier analysis
above stands as the record of what *could* overlap safely — it is reasoning, not schedule.
(MAM-private's plan file was held by the live wlc-utils-private session when this was recorded,
so its mirror of this decision goes in at or after that session's write-back, not concurrently.)

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
circuit from `C:\Users\BenDe\GitRepos\MAM-basics`: `py\main_0_mega.py` (whose wlc half is the
`_STEPS` run from `wlc-vendor-uxlc` through `wlc-a-notes`: `wlc-vendor-uxlc`,
`wlc-json-and-unicode`, `accgram-run-prose`, `accgram-test-fixes`, `accgram-run-poetic`,
`accgram-generate-html`, `wlc-diffs-420422`, `wlc-a-notes`), then the six accgram subcommands
outside it (`run-dual-cant`, `run-printed-decalogue`, `survey-chanted-word-accents`,
`xcheck-poetic`, `servi-xcheck`, `grammaticality`), then `main_uxlc_grammar_test.py`,
`main_find_uxlc_accent_changes.py`, and `main_edition_transcription.py build --check`.
`git status --porcelain` then shows **only the phase's source edits**.

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

## Phase 0 — Preflight: baseline, manifest, collision census

*Read-only, plus one commit to this plan file.* No tracked artifact changes.

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

---

## Phase 1 — The provenance worktree fix

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

**wlc-utils is CC0 1.0; MAM-basics is GPL-3.0.** They are the only two of Ben's thirty repos with
a `LICENSE` file at all, and neither README mentions licensing. Moving 626 data files from one to
the other either silently withdraws a published public-domain dedication or leaves the status
ambiguous — and the corpus includes third-party material, `in/Tanach-26.0--UXLC-1.0--2020-04-01/
License.html` being a tracked upstream licence that travels unchanged either way.

Ben's decision: **keep GPL-3.0 at the root for code, and scope CC0 to the moved data.** Place a
verbatim copy of wlc-utils' CC0 `LICENSE` at each arriving tree — `gh-pages/wlc/LICENSE`, and one
covering the wlc portions of `in/` and `out/` — and add a short paragraph to MAM-basics' `README.md`
saying which licence covers what and that the vendored Tanach text carries its own. Prefer the
fewest declarations that unambiguously cover the moved paths over one per directory.

**Verify:** `git status` clean after the commit; a reader landing on any moved path can reach a
licence statement that names it. No artifact changes, so no regeneration is owed.

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

Add `gh-pages/index.html`: a short page pointing at `wlc/`, so `bdenckla.github.io/MAM-basics/` is
not a 404 the day the site goes public.

**Manual gate: Ben sets Settings → Pages → Source: GitHub Actions, then pushes to `main`.** The
workflow triggers on push to main only — a branch push will not deploy, which is a real way to
spend a session believing the phase failed.

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

**Check the MAM-private interlock before scheduling any phase** — "Interactions with the
MAM-private programme" above. The operative rule is Ben's 2026-08-08 serialization decision
recorded there: the two programmes run as whole blocks, never interleaved, so while any
MAM-private phase is live, nothing runs here. The three tiers in that section are the analysis
of what could have overlapped, kept as reasoning only.

Each session reads this file, does exactly **one** phase, verifies it, then writes the result back
into the Status table — state, date, commit shas — and marks that phase's heading `— DONE <date>`,
recording the numbers actually measured and anything the plan did not predict. A phase whose
result is not written back cannot be judged by the next session. Then spawn a task chip for the
next phase quoting this file's absolute path.

**Stop and ask Ben rather than chaining on** at these five points:

- **Precondition 1**, the two-accents plan — land it or freeze it.
- **Phase 3**, the `data/lci_recs.json` → `in/lci_recs.json` rename, if he disagrees.
- **Before Phase 5**, the largest phase, which must complete within one session.
- **Phase 6**, which needs a GitHub settings change only he can make.
- **Before Phase 9**, which changes what the public sees.
- **Phase 11 items 2, 3 and 5** — two untracked-copy edits and one policy decision.

Phases 0, 1, 2, 4, 7, 8 and 10 are safe to chain automatically once their verification passes.

**Run the test suite and every generator from the main checkout, never from a worktree** — until
Phase 1 lands, after which a worktree becomes safe for generators and still gives 12 unreal
failures for the suite.
