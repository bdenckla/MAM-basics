# PLAN — repo maintenance across GitRepos, every repo except MAM-basics

State: runbook

Written 2026-08-07 by the session that had just done MAM-basics' own maintenance. Ben's
request, 2026-08-07: *"do repo maintenance across all repos cloned in GitRepos with the
exception of MAM-basics (since we just did MAM-basics in this session)."*

Everything below is written for a session that has none of that conversation. Every figure
carries the command that re-establishes it; re-measure rather than trust, and treat a
mismatch as a finding.

---

## EXECUTED 2026-08-27 — the public half, and the process change the private half forced

The second run of this plan. **Read this section and the 2026-08-07 one below it before acting
on the body**, which is the 2026-08-07 record and is stale on scope in ways this section
corrects again.

Ben's request, 2026-08-27: perform the periodic maintenance over everything it is scoped over,
adjust that scope for the evacuations of public repos into MAM-basics and private repos into
MAM-private, make sure the private half leaks nothing into the public repos, and say which repos
might now be removed as completely evacuated.

**THE PRIVATE HALF IS NOT IN THIS FILE.** MAM-basics is public and three of the repos swept are
not, so the private findings are batched into MAM-private at
`doc/repo-maintenance-2026-08-27.md`, which is where to look for them. This section says nothing
about their content beyond the fact that they exist, and names no path inside a private repo.

### Scope needed no adjustment, which is itself the finding

`all-repos.code-workspace` lists 19 folders and `~/GitRepos` holds 19 clones, and **the two sets
are equal in both directions** — no folder listed but absent, none present but unlisted.
`~/FrozenRepos` holds the same 6. So the evacuations have been keeping the workspace file in
step as they went, and the 30-then-24 figures in the 2026-08-07 record and in §2 below are both
superseded rather than wrong: 30 → 24 when the frozen clones moved out on 2026-08-07, then down
to 19 as al-hatorah, masorah-books, mgketer, breuer-cos and wlc-utils' clones left. §2's advice
to sweep all folders rather than hand-exclude MAM-basics still holds.

Re-establish with `.novc/`-local scripting, or by comparing `Get-ChildItem -Directory` against
the workspace file's `folders` array; `py/repo_util/repo_selection.py`'s `load_workspace_repo_dirs`
raises `FileNotFoundError` on any listed folder not on disk, so a drift in one direction is
already fatal at every action's start.

### What ran, and what it found

All five sweeps over all 19, in the order §3 prescribes, from the main clone.

1. **`--clean-worktrees`** — "nothing to clean" in all 19. Zero linked worktrees and zero
   `claude/*` branches everywhere, MAM-basics included. The one-repo job the 2026-08-07 baseline
   predicted has become a no-repo job.
2. **`--check-repo-standards`** — `GITATTRIBUTES_LF` true in all 19; `SYS_PATH_MUTATIONS`,
   `SYS_PATH_IN_TESTS` and `ROOT_CONFTEST` at zero in all 19. Public-side orphan marks: **zero**.
   Public-side advisory counts, untouched per §8: `HEX_ESCAPES` 79 MAM-basics, 1
   diffable-pointed-hebrew; `NFC_H_DOT` 18 UXLC-utils, 11 MAM-basics, 1 codex-index-leningrad;
   `NFC_LATIN` 22 UXLC-utils, 13 MAM-basics, 1 each in codex-index-leningrad and
   diffable-pointed-hebrew.
3. **`--check-memory-health`** — no repo has an unindexed memory file, a dead pointer or an
   orphaned worktree project directory. `STALE_PATHS`: UXLC-utils 9, MAM-basics 2,
   holman-ketiv-qere 1. UXLC-utils' nine are the residue of its 2026-08-03 evacuation, still
   open from the 2026-08-07 run's "still open, deliberately" list.
4. **`--audit-line-terms`** — `MIXED_FILES=0` and `NO_TERM=0` across all 1,789 tracked `.py`.
5. **`--run-black`** — `BLACK_OK` for all 10 repos with tracked Python, **rewrote no file in any
   repo**, and every tree was still clean afterwards. The other 9 skip as having no tracked
   `.py`, which is not a failure. `BLACK_PROBLEM_COUNT` absent, as H5 predicts.

Suite here: **951 passed, 5 skipped, 59 subtests**, at `-q` (which the count needs — the default
verbosity drops the subtests line).

### The process change: `--visibility`, and a guard that makes the split enforced

Every sweep is RUN from MAM-basics, which is public, and three of the 19 are private. So the path
of least resistance for `--report-txt` is a file this repo tracks, which is the path that
publishes a private repo's internals. Ben's framing, 2026-08-27: a repo's **name** is not
private; its **content** is.

Landed in `6cb65ef` and `b492fd6`:

- `in/repo_maintenance_policy.json` gains a `repo_visibility` map classifying all 19, verified
  against `gh repo view` and, for the ArtScroll gist, `gh api gists/… --jq .public`. Declared
  rather than queried, because the sweeps must work offline and because `gh repo view` cannot
  resolve a gist at all. **Frozen and private are unrelated** and neither list may be derived
  from the other — MAM-private is private and not frozen, mamgo-auto-edits is frozen and public.
- `py/repo_util/report_destination.py` refuses a report covering any private repo whose
  destination is a path a public repo tracks. Three destinations pass: inside a private repo,
  a path git ignores, or no repo at all.
- `--visibility {all,public,private}` splits a sweep so each half is written where it belongs.
  This is the shape a full round of maintenance now takes: two runs of each read-only action.
- `py/tests/test_repo_visibility_declared.py`, 10 tests, keeps the map complete and pins the
  guard's decisions on paths built from it.

**A guard rather than a convention, for the same reason the frozen clones were MOVED out of
GitRepos on 2026-08-07 rather than merely listed**: make the wrong thing unreachable, not merely
discouraged. The convention already existed and was already being followed — the review series
split public-here and private-into-MAM-private on 2026-08-26 — and a convention costs nothing
until the one run that forgets it, by which point the report is written and whatever comes next
commits it.

**One defect the split exposed, now fixed.** `--check-memory-health` is the only sweep that is
not purely per-repo: `_check_cited_paths` calls a citation stale when it resolves in no *swept*
repo, so narrowing the selection narrowed the resolution universe with it. MAM-private read
`STALE_PATHS=14` over all 19 and 19 over the 3 private ones, from the same unchanged files.
`run_check_memory_health_across_repos` now takes `resolution_repo_dirs` separately from the repos
being reported on, and `main_repo_util` passes the whole workspace. Split and unsplit runs agree
again, and every public repo's numbers above are identical either way. **Worth remembering as the
general hazard**: before adding a filter to a cross-repo sweep, ask which of its checks read
across repos rather than within one.

### Whether the write-back had already leaked: audited, and it had not

A sweep for private-repo path markers across all 16 public clones returns hits in MAM-basics only,
and every one falls into a category that is deliberate rather than accidental: `CLAUDE.md`'s
pointers to where the primary sources live (Ben's decisions of 2026-08-10 and 2026-08-11),
machinery that must name a destination to work (`in/vendoring_policy.json`, `py/mb_cmn/paths.py`,
`py/main_0_mega.py`), generated vendoring artifacts, and the execution records in `doc/PLAN-*.md`.
**No maintenance report has ever been written into a tracked file here** — the 2026-08-07 run
wrote its reports to `.novc/`, as §3 instructs, and so did this one.

**The criteria that actually govern this are narrower than "private paths must not travel", and
are stated in MAM-private at `doc/near-aleppo-privacy.md`.** Read that before writing public prose
about any private tree; its §4 gives a mechanical backstop grep and, more usefully, the two ways
that grep misleads. It was run over every line this session added here, in both spellings of the
abbreviation it looks for, with zero hits.

### Which repos might now be removed: mgketer already is, and no other clone qualifies

- **mgketer, the repo Ben named, is done on both counts already.** There is no
  `~/GitRepos/mgketer` — its tree lives under MAM-private — and `bdenckla/mgketer` was
  **archived on GitHub on 2026-08-27T00:28:51Z** (= 2026-08-26 20:28 EDT; GraphQL `archivedAt`, checked 2026-09-01 — this bullet said 2026-08-10 until then, the private-evacuation date standing in for the archive date). Nothing left to do.
- **None of the six public repos whose Python was evacuated is a removal candidate**, because
  none was completely evacuated: only their Python left. Tracked-file counts today are
  book-of-job 784, UXLC-utils 780, holman-ketiv-qere 347, codex-index-aleppo 175,
  codex-index-cam1753 152, codex-index-leningrad 51 — corpora, `in/` trees and `gh-pages/`.
  **Four publish a live Pages site** (book-of-job, UXLC-utils, holman-ketiv-qere,
  codex-index-aleppo), and **all six are resolved by this repo's own code**: five as
  `DATA_REPO_NAME` in `py/ac_paths.py`, `py/boj_paths.py`, `py/cam1753_paths.py`,
  `py/hkq_paths.py` and `py/lenin_paths.py`, and UXLC-utils through `sibling_repo("UXLC-utils")`
  at four sites. Removing any of those clones would break a generator.
- **No GitHub repo is an archiving candidate either**, and the reason is uniform: archiving makes
  a tracker read-only, and every candidate still has open issues — UXLC-utils 27,
  holman-ketiv-qere 60, book-of-job 19, wlc-utils 21, and on the private side the four counted in
  the private record. The three codex-index trackers are at zero open, but their repos hold live
  data this repo reads, so archiving them would freeze corpora still in use.
- **The already-removed clones are the pattern to read this against.** wlc-utils went 2026-08-22,
  al-hatorah 2026-08-11, masorah-books and mgketer with the private evacuation. In every case the
  clone went when **nothing on disk resolved it any more** — not when its issues closed and not
  when its remote was archived. That is the test to apply next time, and none of the 19 passes it
  today.

### Recommendation Ben should decide on

The private record ends with one, because it is a private-side question: the tracker
consolidation that mirrors the public transfer of 2026-08-26 has not happened. It is stated there
with its counts, and is deliberately not acted on.

---

## EXECUTED 2026-08-07 — the outcome, and which predictions failed

Carried out in full the same day it was written. **Read this section before acting on
anything below: the body is kept as the record of what was planned, and several of its
figures — and two of its instructions — are now wrong.**

**What changed, by repo.** holman-ketiv-qere: leftover worktree and `claude/*` branch
removed as predicted, plus two orphan combining marks escaped (`dd082a7`). UXLC-utils and
masorah-books: an empty worktree husk removed from each. MAM-basics: `check_memory_health.py`
corrected (`81ee45c`, `519be83`). The other 26 repos: nothing. `--run-black` rewrote no file
anywhere.

**Predictions that FAILED.**

- *"Leftover worktrees exist in exactly ONE repo."* True of REGISTERED worktrees only. The
  section 7 baseline used `git worktree list`, which cannot see a leftover DIRECTORY.
  UXLC-utils held a flat-empty husk, and masorah-books one wrapping an empty `py/cos/`. The
  second was neither removed nor reported, because `_sweep_empty_dirs` tested
  `any(child.iterdir())` — fixed in `8cdb22f`, which now treats "no file at any depth" as
  empty and age-gates the widened case.
- *"breuer-cos has 2 orphaned memory files that want carrying over into masorah-books."*
  Wrong on both counts, and obeying it would have done harm. It held ONE memory file, about
  wlc-utils rather than about Breuer, already superseded by wlc-utils' own
  `no-wlc-koren-12th-repo.md`. Carrying it over would have planted a superseded memory in a
  repo it was never about. `check_memory_health.py`'s docstring now carries the lesson.
- *Section 5's masorah-books item was incomplete.* Five orphaned session directories was
  right for that repo; there were 22 across four repos, wlc-utils holding 15.

**Decisions Ben took on the questions this plan raised, all 2026-08-07.** All 22 orphaned
session directories deleted (47 MB), plus the orphaned project directories for breuer-cos and
yeivin-itm (7.1 MB); none held a `memory/` subdirectory. NO repo gains its own
`py/main_repo_maintenance.py` — al-hatorah was considered and declined (`e66754e`), so
`MAINTENANCE_SCRIPT=False` is the settled answer rather than a gap. `* text=auto eol=lf`
added to the six non-frozen repos lacking it, sparing three upstream Calendrica files in
github-misc. The breuer-cos CLONE deleted and the repo dropped from the workspace
(`79df1e9`), its GitHub repository staying unarchived until all five of its issues resolve.

**Sections 1 and 2 are stale on scope.** The frozen clones left GitRepos for the sibling
`C:/Users/BenDe/FrozenRepos` and left `all-repos.code-workspace` (`bcf88ae`), so the freeze is
structural: the workspace lists 24 folders, not 30, and no sweep can reach a frozen repo at
all. `--include-frozen`, named in section 1's table area and in H3, was removed (`9113cb3`).

**Hazards, as they played out.** H1 was avoided by running `--clean-worktrees` first. H3's
warning against `--commit-across-repos` was honoured — every repo was committed by hand. H5
held: `--run-black` reported no problems, and since the five py-without-venv repos were all
frozen and have now MOVED, every repo left in GitRepos with tracked Python has a venv, which
retires issue #212's cited cases.

**Still open, deliberately.** `HEX_ESCAPES` and the `NFC_*` counts are advisory and were not
touched. The one substantial finding this sweep raised and did not act on: wlc-utils' and
UXLC-utils' memory files carry stale path citations left by the 2026-08-01 evacuation of
their Python into MAM-basics — `--check-memory-health` reports 5 and 8 citations resolving
nowhere, plus dozens now resolving in MAM-basics instead.

---

## 0. Preconditions — check all four before doing anything

**All four were verified satisfied at 2026-08-07 13:05**, immediately before this plan was
committed. They are kept as checks because a session picking this up later cannot assume the
tree stayed still. What was verified then:

- Both chip sessions ended, and both succeeded. MAM-basics issue #218 is CLOSED, unblocked by
  `673cb05` ("Research the three prose oddballs the METHIGAZAQEF change made, and unblock
  generate-html"). The vendoring drift 46621c7 recorded was resolved by `bbf600b` ("Resolve
  the vendoring drift 46621c7 recorded, in all five sibling repos"), followed by `4afa1e8`
  ("Fix the category vocabulary of the vendoring inventory"). All five sibling repos were
  confirmed by hand to no longer carry `pct_query`, `pct_decode` or `he_ascii_identifier`.
- The re-vendor branch `claude/gallant-meitner-68c79b` was merged and deleted, and its
  worktree removed. Removing it needed the `activity_grace_seconds=0` override of H1: the
  session had ended 15 minutes earlier, inside the sweep's one-hour grace, so the sweep spared
  it as "may be in use". Only the activity heuristic was overridden; every other condition
  still ran.
- MAM-basics: 0 worktrees, 0 `claude/*` branches, `main` at `4afa1e8`.
- Every repo in GitRepos clean and pushed.

1. **Two chip sessions launched 2026-08-07 must have ENDED.** They were:
   - *"Fix #218: 3 prose oddballs block generate-html"* — ran in the MAIN clone
     `C:/Users/BenDe/GitRepos/MAM-basics`, committing to `main`.
   - *"Re-vendor mb_cmn copies stale since the #224 cull"* — ran in worktree
     `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/gallant-meitner-68c79b`, branch
     `claude/gallant-meitner-68c79b`, and edited five sibling repos (al-hatorah, book-of-job,
     codex-index-aleppo, holman-ketiv-qere, mgketer) as shared clones.

   If either is still live, STOP. `--clean-worktrees` would delete a running session's
   worktree, and `--run-black` would reformat files another session is editing.

2. **The re-vendor branch is merged and its worktree removed.** Check:
   ```
   git -C C:/Users/BenDe/GitRepos/MAM-basics worktree list
   git -C C:/Users/BenDe/GitRepos/MAM-basics branch --list "claude/*"
   ```
   A surviving `claude/gallant-meitner-68c79b` wants merging into `main` first — per Ben's
   standing rule a worktree branch is merged and `main` pushed, rather than the branch pushed.

3. **Every repo is clean and pushed**, so any diff this maintenance produces is attributable:
   ```
   foreach ($d in (Get-ChildItem -Directory C:/Users/BenDe/GitRepos)) { $n = (git -C $d.FullName status --porcelain | Measure-Object).Count; if ($n) { Write-Output "$($d.Name) dirty=$n" } }
   ```

4. **Run from the MAIN MAM-basics clone, never from a worktree.** See hazard H6 — this is the
   one that silently produces wrong answers rather than an error.

---

## 1. What the tooling is

**MAM-basics is the only repo in GitRepos with its own `py/main_repo_maintenance.py`**
(verified 2026-08-07 by scanning every directory for that path). Every other repo's
maintenance comes from MAM-basics' cross-repo entry point, `py/main_repo_util.py`. That is
the whole reason the cross-repo sweep exists: `repo_util/clean_worktrees.py`'s docstring says
plenty of repos have no Python and so can have no maintenance script of their own —
wlc-utils above all, which was emptied of Python on 2026-08-01 while agents go on editing its
`doc/` and `gh-pages/`.

Run everything from `C:/Users/BenDe/GitRepos/MAM-basics` with
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`.

Six actions, mutually exclusive, one per invocation:

| Action | Writes? | Notes |
|---|---|---|
| `--clean-worktrees` | yes | removes finished worktrees + merged `claude/*` branches |
| `--check-repo-standards` | no | |
| `--check-memory-health` | no | |
| `--audit-line-terms` | no | |
| `--run-black` | **REFORMATS** | its own commit, never riding along |
| `--commit-across-repos` | **COMMITS** | do NOT use — see H3 |

**`--workspace-file all-repos.code-workspace` is not optional.** The default
`MAM-basics.code-workspace` lists only the handful of repos MAM-basics generates into, and
anything outside it dies with "Requested repo was not found in workspace folders".

---

## 2. Scope, and a recommendation about excluding MAM-basics

`all-repos.code-workspace` lists 30 folders: 29 siblings plus MAM-basics itself as `"."`.

**Recommendation: do NOT hand-exclude MAM-basics — sweep all 30.** Three reasons, and Ben
should overrule this if he disagrees:

- `--repos` with 29 hand-typed names is error-prone, and a typo silently narrows the sweep.
- MAM-basics will have moved since its 2026-08-07 maintenance: the two chip sessions above
  add commits and may leave a worktree behind. Re-checking it is a feature, not redundancy.
- Every action is cheap or idempotent on an already-clean repo. `--run-black` on MAM-basics
  was verified clean at 770 files on 2026-08-07, so it is a no-op there.

If MAM-basics must genuinely be excluded, `--repos` takes an explicit list — build it from
the workspace file rather than typing it.

---

## 3. Order of operations

**1. `--clean-worktrees` FIRST, before any hand-inspection of any worktree.** See H1.
```
.venv/Scripts/python.exe py/main_repo_util.py --clean-worktrees --workspace-file all-repos.code-workspace
```
Read every `kept ... (reason)` line. A spared worktree is not a failure; it is a question.
`WORKTREE_PROBLEM_COUNT` is the failure signal.

**2–4. The three read-only checks**, in any order:
```
.venv/Scripts/python.exe py/main_repo_util.py --check-repo-standards --workspace-file all-repos.code-workspace --report-txt <file>
.venv/Scripts/python.exe py/main_repo_util.py --check-memory-health   --workspace-file all-repos.code-workspace --report-txt <file>
.venv/Scripts/python.exe py/main_repo_util.py --audit-line-terms      --workspace-file all-repos.code-workspace --report-txt <file>
```
Use `--report-txt`: the one-line-per-repo stdout summary gives counts, and the text report
gives the actual findings. Write reports into `.novc/`, not into a tracked directory.

**5. `--run-black`**, last of the mechanical steps and the only one that rewrites source:
```
.venv/Scripts/python.exe py/main_repo_util.py --run-black --workspace-file all-repos.code-workspace
```
Expect `BLACK_PROBLEM_COUNT` absent/zero — see H5 for why, and what a nonzero one means.

**6. The `doc/` sweep — genuinely last, and the only step that is not mechanical.** It deletes
tracked files and needs a judgment `main_repo_util.py` deliberately does not make, so it runs
after everything else, where a wrong call is plainest in the diff. The standard it applies is
the "The doc/ directory standard" section of `py/repo_util/check_repo_standards.py`: a doc file
that only records finished work is deleted, not archived; git history keeps it.

**Only two folders under `GitRepos` have plans — MAM-basics 6 and MAM-private 4**, and that
second figure read 3 until 2026-08-29, when running this step against MAM-private turned up a
fourth: `al-hatorah/doc/PLAN-melody-compiler.md`, live work sitting in one of the evacuated trees
rather than at that repo's own `doc/`. The measurement that said 3 was a glob of `doc/PLAN-*.md`
at each repo root, which cannot see a tree's own `doc/`, **so the screen has to cross
directories** — a git pathspec written without `:(glob)` lets `*` match `/`, and running it
through git rather than over the filesystem also keeps a leftover agent worktree's copies of the
same plans out of the count. Raise the candidates:

```
git -C C:/Users/BenDe/GitRepos/MAM-basics grep -l "^State: executed" -- "*PLAN-*.md"
```

All ten carry the `State:` line as of 2026-08-29 — MAM-basics' six from the day it was
introduced, and MAM-private's four the same day, in that repo's `6a60e8b` and `0bdde52`.

Then ask the second question of each **by hand**, because the `State:` line does not answer it:
**does surviving work lean on this plan, and how hard?** *Executed is not the same as spent.* On
2026-08-29 the still-paused `PLAN-evacuate-the-rest-of-three-repos.md` cited **seven** of the
nine executed plans, and two of those — `PLAN-evacuate-the-rest-of-wlc-utils.md` and
`PLAN-evacuate-public-repos-programme.md` — by live markdown link, named as the model it "leans on
rather than restating" and as the source of two sections declared to be its own. Those two were
kept and the other seven deleted (`f6173fe`). The line that held: a plan the surviving work
merely mentions is spent, a plan it tells you to read first is load-bearing.

Report the filenames raised and nothing else — **never a count**, which reads as a defect tally
against repos that have earned their docs. For doc/ files that are *not* plans, the screen stays
the inbound-reference one that same section of `check_repo_standards.py` describes; note that
the screen inverts on plans and must not be used on them.

**7. Retire completed Codex task folders under
`C:/Users/BenDe/Documents/Codex` — judgment work outside the Python CLI.** This is normal
repository maintenance even though the folder is outside `GitRepos`, but it deliberately is **not**
a new `main_repo_util.py` action: an automatic process cannot determine whether a task is active,
whether an apparently obsolete clone carries unique unmerged work, or whether a multi-repository
folder is a forest intended for a later handoff.

Keep the `ReviewForests` root, whether it is empty or populated, and keep each active task folder.
For a dated task folder that appears complete, distinguish these cases before retiring it:

1. A reusable worktree forest has `review-manifest.json` at the forest root and Git worktrees at
   the paths declared in that manifest. Read the manifest before running Git in any forest member.
   A directory merely containing repository-named copies is not a forest.
2. A linked worktree has a `.git` pointer file. A `.git` directory is a standalone clone, so check
   its cleanliness, branch/ref state, and whether the checked-out commit is already preserved in
   the primary clone or remote. A clone using `objects/info/alternates` can show dangling objects
   that actually belong to the primary clone; verify its own object store before calling the clone
   disposable.
3. A Git-less `proposed/` copy set is a task artifact, not a forest. Once its changes are committed
   and pushed, retain the commits and generated reports in their proper repositories rather than
   retaining the copies.
4. Claude cache and temporary-data directories can live outside `Documents/Codex`, and their paths
   can change. Report each identified Claude cache or temporary directory with its exact path and
   measured size; a directory of 1 GiB or more is a maintenance finding. Do not classify a directory as
   cache only because it is large: Claude project directories, session transcripts, and `memory/`
   directories can contain durable work. Verify that a directory is disposable cache data before
   retiring it, and preserve an uncertain directory.

Move only verified completed task folders to the Windows Recycle Bin, record the exact paths and
the evidence, and leave an ambiguous task folder in place. The Recycle Bin makes a mistake
recoverable, but it does not free disk space until emptied. Do not delete the `Documents/Codex`
root while an active task folder or the `ReviewForests` root remains.

**The `doc/` sweep was added 2026-08-29, so neither of the two runs recorded above included the
`doc/` sweep** — the 2026-08-07 and 2026-08-27 records describe steps 1–5 only. **The
`Documents/Codex` task-folder step was added 2026-09-04, so neither historic run assessed those
folders either.**

---

## 4. Parallelism — what to fan out, and what not to

Ben asked whether sub-agents could run the repos in parallel. Split the question:

**Do NOT fan out the sweeps themselves.** All five sweep actions are ALREADY cross-repo: each
loops over every repo inside one process. Handing them to sub-agents would duplicate that
loop, and two agents running `--run-black` against the same repo would race on the same
files. The sweeps are also not the slow part — the black sweep is the longest and is minutes,
not hours.

**DO fan out the follow-up.** What the sweeps produce is a list of findings per repo, and
acting on a finding is judgment work: is this spared worktree's gitignored file recorded
anywhere else, is this hex escape worth converting, does this repo want its own maintenance
script. That work is repo-local, so one sub-agent per repo-with-findings is genuinely
parallel and collision-free — different repos are different working trees.

Three constraints on that fan-out:

- **At most one agent per repo.** Two agents in one repo stage into one index and can commit
  each other's half-written work, which fails cleanly and therefore silently.
- **No sub-agent runs a cross-repo sweep.** The parent session owns those; a sub-agent
  reports on and fixes its one repo.
- **Do not give the sub-agents worktrees.** The work is in OTHER repos, so a MAM-basics
  worktree buys no isolation, and running the sweep from a worktree is actively wrong (H6).

---

## 5. Concrete pending items, found 2026-08-07 — re-verify each

- **holman-ketiv-qere has a leftover worktree and branch.**
  `.claude/worktrees/festive-shamir-dad9ec` (detached at `ca1beea`) and branch
  `claude/festive-shamir-dad9ec`, "Register two unrun test modules in main_test.py". Confirm
  merged into that repo's default branch before deleting; `--clean-worktrees` checks this
  itself and refuses an unmerged branch, so let it decide rather than pre-empting it.
- **masorah-books has 5 orphaned worktree project directories** under
  `C:/Users/BenDe/.claude/projects/` (`C--Users-BenDe-GitRepos-masorah-books--claude-worktrees-*`).
  Same litter cleaned out of MAM-basics on 2026-08-07 (7 dirs, 50.2 MB). `--check-memory-health`
  reports the count as `WORKTREE_PROJECT_DIRS` but deliberately does not delete them, because
  they hold session transcripts. Check for a `memory/` subdirectory in each before deleting —
  none of MAM-basics' seven had one — and confirm with Ben, who chose deletion for MAM-basics.
- **breuer-cos has 2 orphaned memory files** at
  `C:/Users/BenDe/.claude/projects/C--Users-BenDe-GitRepos-breuer-cos/memory/`. breuer-cos was
  superseded on 2026-07-31 when Breuer's *Cantillation of Scripture* was merged into
  masorah-books. Per `check_memory_health.py`'s docstring these are memories worth keeping, so
  they want **carrying over into masorah-books' memory directory, not deleting.**
  That docstring also cites `yeivin-itm` as having four such files; verified 2026-08-07 that
  `C--Users-BenDe-GitRepos-yeivin-itm` now has NO memory directory, so that half of its
  example is already resolved and **the docstring is stale on it** — worth correcting while
  you are there.
- **Only MAM-basics has `py/main_repo_maintenance.py`.** `--check-repo-standards` reports
  `MAINTENANCE_SCRIPT` per repo. Whether any other repo should gain one is a real question,
  not an obvious yes — raise it with Ben rather than writing scripts unasked.

---

## 6. Hazards

**H1 — Hand-inspecting a worktree makes the sweep skip it.** `git_worktree_cleanup` decides
"may be in use" from the mtime of the per-worktree `index` file, which ANY git command in
that worktree rewrites, `git status` included; the grace is one hour. On 2026-08-07 this
session probed four MAM-basics worktrees with `git status --ignored` and the sweep then
spared two of them, reporting activity 5 and 12 minutes ago when the real last activity was
over an hour earlier. **Run the sweep first; investigate only what it spares.** The module
restores the index mtime around its OWN probe; a probe you run from the shell gets no such
restore. If you have already poisoned the stamps, do not reach for a force flag — the module
documents that a `--force` reaches none of its conditions, since all are decided in Python
before git runs. Confirm the real times from the index mtimes, then call
`git_worktree_cleanup.clean_worktrees(repo, activity_grace_seconds=0)` from a throwaway
`.novc/` script, which is the documented parameter rather than an override of its judgement.

**H2 — A spared worktree holding gitignored content is a review task, not a bug.** The sweep
spares a worktree whose gitignored files exist nowhere else, naming them. Check each is
recorded somewhere durable — a filed issue, a commit — before deleting anything. On
2026-08-07 two MAM-basics worktrees were spared this way and all seven files turned out to be
spent: a draft issue body byte-identical to the filed issue, and five throwaway scripts whose
findings were already written up in an issue comment.

**H3 — Frozen repos are honored by `--run-black` ONLY (MAM-basics issue #211, open).**
`maintenance_policy.frozen_repos()` is consulted in the `--run-black` branch and nowhere else.
**`--commit-across-repos` can therefore commit to a frozen repo, which is precisely what the
freeze exists to prevent — do not use that action in this sweep.** Frozen repos, verified
2026-08-07 in `in/repo_maintenance_policy.json`, are six: breuer-cos, CCAR-Psalms, MAM-for-Acc,
MAM-for-CCAR, MAM-for-JPS, TMC. Note issue #211's body is itself stale: it says five frozen
repos and "four actions", predating breuer-cos's freeze (2026-07-31) and the
`--check-memory-health` and `--clean-worktrees` actions. Worth a comment on #211 recording
that, rather than a silent fix.

**H4 — `--clean-worktrees` does not consult the frozen list either, and that is defensible.**
Removing a worktree, or deleting an already-merged `claude/*` branch, changes no commit and no
last-changed date, which is what a freeze protects. State this deliberately rather than
leaving it as an unexamined gap; if Ben disagrees it belongs in #211.

**H5 — black runs from each repo's OWN venv.** `run_black.py` prefers
`<repo>/.venv/Scripts/black.exe`, falls back to `<repo>/.venv/Scripts/python.exe -m black`,
and FAILS the run for a repo with tracked `.py` and neither (there is no black on PATH on this
machine). Measured 2026-08-07: every repo with tracked `.py` and no `.venv` is frozen
(CCAR-Psalms, MAM-for-Acc, MAM-for-CCAR, MAM-for-JPS, TMC), and `--run-black` skips frozen
repos — **so the sweep should report no black problems.** A nonzero `BLACK_PROBLEM_COUNT` means
a non-frozen repo lost its venv, which is MAM-basics issue #212's territory (create missing
venvs; treat a hydrated venv as a repo standard). A missing venv is an un-hydrated clone, not
a documentation bug: create it, or say it is missing and stop.

**H6 — Never run the sweep from a worktree.** `main_repo_util.py` defaults `repos_root` to
`workspace_file.parent`. Run from a worktree with a relative `--workspace-file`, that resolves
to the worktree's own copy, so every sibling lookup becomes
`.claude/worktrees/<sibling>` and finds nothing. This is the general hazard Ben's user-level
CLAUDE.md records as "a repo path that reaches a sibling clone can break in a worktree". Run
from the main clone; if a worktree is unavoidable, pass `--repos-root C:/Users/BenDe/GitRepos`
explicitly.

**H7 — Repo-wide reformatting is its own commit.** If black touches files unrelated to any
other change, that is pre-existing drift (usually a black version bump) and must not ride
along and make a small change look like a formatting commit.

---

## 7. Baseline measured 2026-08-07, 13:05 — settled

Taken after both chip sessions had ended and MAM-basics' leftover worktree was removed, so
nothing was moving. An earlier measurement at ~12:30 was taken while both sessions were live
and is not reproduced here: it showed `holman-ketiv-qere` with 4 dirty files at one moment and
0 a minute later, because the re-vendor session was committing in it. Re-measure anyway if
time has passed.

Re-establish with:
```
$frozen = @('breuer-cos','CCAR-Psalms','MAM-for-Acc','MAM-for-CCAR','MAM-for-JPS','TMC'); $ws = Get-Content "C:/Users/BenDe/GitRepos/MAM-basics/all-repos.code-workspace" -Raw | ConvertFrom-Json; foreach ($f in $ws.folders) { $name = if ($f.path -eq '.') { 'MAM-basics' } else { $f.path -replace '^\.\./','' }; $p = "C:/Users/BenDe/GitRepos/$name"; if (-not (Test-Path $p)) { continue }; $py = (git -C $p ls-files "*.py" | Measure-Object).Count; $wt = ((git -C $p worktree list | Measure-Object).Count - 1); $cb = (git -C $p branch --list "claude/*" | Measure-Object).Count; [PSCustomObject]@{Repo=$name; Frozen=($frozen -contains $name); PyFiles=$py; Venv=(Test-Path "$p/.venv/Scripts/python.exe"); Worktrees=$wt; ClaudeBr=$cb} } | Format-Table -AutoSize
```

Findings from that run, worth carrying forward:

- **Leftover worktrees/branches exist in exactly one repo: holman-ketiv-qere (1 and 1).**
  Every other repo in the workspace, MAM-basics included, is 0 and 0. So the worktree half of
  this sweep is expected to be a one-repo job — if `--clean-worktrees` reports leftovers
  anywhere else, something has changed since 2026-08-07 and is worth reading before acting.
- **Repos with tracked `.py` but no `.venv`**: CCAR-Psalms (6 files), MAM-for-Acc (29),
  MAM-for-CCAR (69), MAM-for-JPS (58), TMC (17) — all five frozen.
- **Repos with no tracked `.py` at all**: ArtScroll, document-index, github-misc,
  mamgo-auto-edits, UXLC-utils, wlc-utils. A repo with no Python is not a black failure.
- **MAM-basics' own 2026-08-07 result, for comparison**: black clean at 770 files, ruff clean,
  902 tests passed / 5 skipped, line terms clean at 771 files, `SYS_PATH_MUTATIONS=0`,
  `ORPHAN_MARKS=0`, `HEX_ESCAPES=67`.

---

## 8. What is NOT expected to change

- **No tracked source file should change except by `--run-black`.** The four other sweeps read
  only; `--clean-worktrees` touches worktrees, branches and `.claude/worktrees/` directories,
  never a tracked file.
- **`HEX_ESCAPES` findings are advisory and are never auto-fixed** —
  `check_repo_standards.py` says findings are reported, never auto-fixed. Do not start
  converting `/uXXXX` escapes to `\N{...}` across repos as part of a maintenance sweep.
- **A dangling `[[link]]` in a memory file is not an error.** It marks something worth writing
  later. MAM-basics' one dangling link was deliberately left in place on 2026-08-07.
- **A skip in a test suite may be a semantic signal, not a problem.** In MAM-basics' accgram
  tests a skip reports that a page diverges from its strand.

---

## 9. Verification and commit discipline

Re-run each sweep after acting on its findings and confirm the counts moved the way you
expect: `WORKTREE_PROBLEM_COUNT` absent, `LINKED_WORKTREES`/`AGENT_BRANCHES` at 0 for every
repo you cleaned, `WORKTREE_PROJECT_DIRS` at 0 for any repo whose orphaned session directories
you removed, `MIXED_FILES=0`/`NO_TERM=0` for line terms.

For any repo with its own test suite, run it from that repo's root with that repo's own venv
before committing.

Commit directly to `main` in each repo — no feature branches — and push, per Ben's standing
authorization; do not ask, and do not end by handing back an unpushed commit. One commit per
repo. Keep any repo-wide reformat as its own commit (H7). Write multi-line commit messages to
a temp file and use `git commit -F <file>`; no here-strings, no inline `python -c`.
