# PLAN — repo maintenance across GitRepos, every repo except MAM-basics

State: runbook

Written 2026-08-07 by the session that had just done MAM-basics' own maintenance. Ben's
request, 2026-08-07: *"do repo maintenance across all repos cloned in GitRepos with the
exception of MAM-basics (since we just did MAM-basics in this session)."*

Everything below is written for a session that has none of that conversation. Every figure
carries the command that re-establishes it; re-measure rather than trust, and treat a
mismatch as a finding.

---

## Current scope and task-artifact retirement — corrected 2026-09-08

This section supersedes the old clone counts and clone descriptions in the dated 2026-08-27
execution record below. The earlier sections remain as records of those runs, not as a current
roster.

The current repository roster is defined by two declarations in
`in/repo_maintenance_policy.json`: `gitrepos_setup_rule` supplies the complete ordered rule, and
`repos_to_keep_absent` names repositories that must not be cloned. Apply every clause, including
the frozen-repository and keep-absent subtractions and the two added gist clones. The workspace
file is the input to a sweep, not a substitute for the setup rule. Do not infer that an extra
clone belongs merely because it exists, and do not infer that a missing unarchived repository
should be restored. The roster-driven files formerly under `misc/linux-sh/` were retired on
2026-09-08 because their twelve-name lists contradicted the canonical declaration.

Correction 2026-09-09: GitRepos setup follows the folders listed in
[all-repos.code-workspace](../all-repos.code-workspace), as specified by
`gitrepos_setup_rule` in [in/repo_maintenance_policy.json](../in/repo_maintenance_policy.json).
Do not enumerate GitHub repositories and subtract exclusion lists, and do not add gist clones.
The earlier scope paragraph's subtraction and gist instructions are superseded.

After the mechanical repository actions, the `doc/` sweep, and the template-projection audit in
step 7, inspect completed task artifacts under `C:/Users/BenDe/Documents/Codex`. Preserve
`C:/Users/BenDe/Documents/Codex/ReviewForests`, even when empty, and preserve every active task
folder. Do not create another maintenance script for this judgment step.

For a directory presented as a reusable worktree forest, read `review-manifest.json` before any
repository command. Preserve a forest whose manifest names a future phase or handoff. A missing
manifest means the directory is not established as a forest: inspect every Git directory instead
of assuming the directory is reusable. A linked worktree has a `.git` pointer file; a `.git`
directory is a standalone clone; a proposal snapshot with neither is not a worktree forest.

Before retiring a standalone task clone, establish all of the following from that exact clone:

1. The working tree is clean.
2. The checked-out commit is preserved in the primary clone or remote.
3. No local branch, unreachable commit, or other object is the only copy of unmerged work.
4. `.git/objects/info/alternates`, when present, is accounted for, and `git count-objects -vH`
   shows whether the task clone itself has unique objects.

Also inspect Claude cache and temporary-data directories outside `Documents/Codex`, without
assuming a fixed cache path. Report each verified cache or temporary directory by exact path and
measured size; a verified disposable directory of at least 1 GiB is a maintenance finding.
Project directories, session transcripts, and `memory/` directories can be durable work, so an
uncertain directory stays in place.

Move every verified retired task folder or cache directory to the Windows Recycle Bin, never to
permanent deletion. State the exact path and why the retirement is safe. Leave an ambiguous task
folder in place and report the question. Recycle Bin contents remain recoverable but continue to
consume disk space until the Recycle Bin is emptied.

### Audit always-loaded AGENTS.md files for trimming opportunities — report only

Inspect the user-wide `~/.codex/AGENTS.md` once and every selected repository's tracked
`AGENTS.md` and `AGENTS.override.md` files as part of the judgment pass. Programmatic Git filename
enumeration still uses `-z`. Measure each file's UTF-8 byte size and look for material that need
not be loaded before every task: dated measurements and historical narratives, long examples,
procedures for a recognizable task type, source-tree-specific detail, and rules duplicated in the
user-wide file, a repository file, a skill, or maintained documentation. A file can merit
trimming while it remains below Codex's byte limit; the cost is repeated context and maintenance
as well as truncation risk.

Report each worthwhile opportunity without implementing it. Name the exact heading or searchable
anchor, the proposed destination, and why a future task would still discover the information.
Prefer a skill only when the task that needs the material has a reliable description-level
trigger; otherwise keep a concise always-loaded rule and point to a focused reference. Do not
assume that a nested `AGENTS.md` will load when tasks normally start at the repository root.

Do not trim an instruction file, create or restructure a skill, move documentation, or change
`project_doc_max_bytes` during maintenance unless Ben separately asks for implementation. Assess
the limit against the combined instruction chain from the repository root to the relevant working
directory, not against one file in isolation. If every selected repository's relevant chain would
fit under Codex's default 32 KiB project-document limit after a proposed trim, report the raised
limit as a separate configuration opportunity rather than changing it.

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
  **Correction 2026-09-10: this bullet went stale on 2026-09-03 and 2026-09-04,
  when the remaining data of all six moved into MAM-basics**, under `book-of-job/`,
  `uxlc/`, `holman/`, `aleppo/`, `cam1753/` and `leningrad/`. No paths module holds a
  `DATA_REPO_NAME` now, no `sibling_repo("UXLC-utils")` call remains, and none of
  the six is in `all-repos.code-workspace`, so none belongs on a machine.
  `py/lenin_paths.py`, which the bullet names, was deleted on 2026-09-10 by phase 3
  of
  [`doc/PLAN-mega-coverage.md`](https://github.com/bdenckla/MAM-basics/blob/40395aa3d44608e9f63a75897cd8e42e1b1a7338/doc/PLAN-mega-coverage.md).
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
  still ran. **Correction 2026-09-10: that override no longer exists.** It switched the
  activity check off for every worktree in the repo at once; `--session-ended` is its
  per-worktree replacement. See H1.
- MAM-basics: 0 worktrees, 0 `claude/*` branches, `main` at `4afa1e8`.
- Every repo in GitRepos clean and pushed.

1. **Two chip sessions launched 2026-08-07 must have ENDED.** They were:
   - *"Fix #218: 3 prose oddballs block generate-html"* — ran in the MAIN clone
     `C:/Users/BenDe/GitRepos/MAM-basics`, committing to `main`.
   - *"Re-vendor mb_cmn copies stale since the #224 cull"* — ran in worktree
     `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/gallant-meitner-68c79b`, branch
     `claude/gallant-meitner-68c79b`, and edited five sibling repos (al-hatorah, book-of-job,
     codex-index-aleppo, holman-ketiv-qere, mgketer) as shared clones.

   These were prerequisites for the historical run. In a current run, live sessions block
   retirement, and `--run-black` must not reformat files another session is editing.
   The compatibility `--clean-worktrees` action now inspects without removing anything.

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
why the cross-repo inspection exists: repositories without Python can still have linked
worktrees. The historical example was wlc-utils, emptied of Python on 2026-08-01; today's
reachable repository set comes from the workspace and repository-maintenance policy.

Run everything from `C:/Users/BenDe/GitRepos/MAM-basics` with
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`.

Actions are mutually exclusive, one per invocation. Repository sweeps use workspace selection;
`--sync-user-config` and exact-target retirement actions do not:

| Action | Writes? | Notes |
|---|---|---|
| `--inspect-worktrees` | no | selects `--worktree-owner claude`, `codex` or `both`; `--worktree PATH` targets one exact registration |
| `--clean-worktrees` | no | compatibility alias for Claude-only inspection; `--session-ended` validates paths without retiring them |
| `--check-repo-standards` | no | |
| `--check-memory-health` | no | |
| `--audit-line-terms` | no | |
| `--run-black` | **REFORMATS** | its own commit, never riding along |
| `--commit-across-repos` | **COMMITS** | do NOT use — see H3 |
| `--sync-user-config --check` | no live configuration write | fetches `origin` and compares every declared user-level destination with `origin/main` |
| `--sync-user-config` | **DEPLOYS OUTSIDE GIT** | run only from the primary MAM-basics clone after the canonical changes are pushed |
| `--prepare-worktree-retirement PATH` | writes one preflight, not the target | shared audit of one ended target, with optional owner-selection guard |
| `--execute-worktree-retirement PREFLIGHT` | **RELOCATES AND REMOVES** | first runs the mandatory operational simulation and fails closed; only then revalidates the reviewed audit, retains `.novc`, removes one target without force, and uses `branch -d` for its eligible branch |

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

**1. Inspect the requested worktree ownership scope.** For both owners:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_repo_util.py --inspect-worktrees --worktree-owner both --workspace-file C:/Users/BenDe/GitRepos/MAM-basics/all-repos.code-workspace
```

Use `claude` or `codex` to narrow selection. Read every candidate and blocker. Inspection
removes nothing; `WORKTREE_PROBLEM_COUNT` reports repository-audit errors. Follow step 8 for
reviewed per-target preparation and execution, and H8 for runtime limitations.

**2–4. The three read-only checks**, in any order:
```
.venv/Scripts/python.exe py/main_repo_util.py --check-repo-standards --workspace-file all-repos.code-workspace --report-txt <file>
.venv/Scripts/python.exe py/main_repo_util.py --check-memory-health   --workspace-file all-repos.code-workspace --report-txt <file>
.venv/Scripts/python.exe py/main_repo_util.py --audit-line-terms      --workspace-file all-repos.code-workspace --report-txt <file>
```
Use `--report-txt`: the one-line-per-repo stdout summary gives counts, and the text report
gives the actual findings. Write reports into `.novc/`, not into a tracked directory.

**`--check-memory-health` checks a memory directory's mechanics, never whether a memory is still
worth having**, and the judgment half is deliberately not part of maintenance: it belongs to the
on-demand skill `dot-claude/skills/prune-claude-state/`, live at `~/.claude/skills/` and
`~/.agents/skills/`, which Ben invokes as `/prune-claude-state` (the skill carries
`disable-model-invocation: true`, so a session cannot start it). That skill reads a repo's
memories and its slice of `~/.claude/plans/`, cross-checks each against live GitHub issue state
rather than the file's own prose, and deletes nothing without an explicit confirmation. Its own
statement of why it sits outside this runbook is that it is expensive. Do not fold it in, and do
not prune memories by judgment during a maintenance sweep. A worked pass, 2026-09-12 in
MAM-basics: five memories deleted as describing a world that no longer exists or as superseded by
`~/.claude/CLAUDE.md`, five repointed at paths the evacuations had moved, two pairs merged, and
every `MEMORY.md` hook cut to one clause, taking the index that loads each session from 14,766 to
about 7,500 bytes.

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

Receipt immutability and retention are independent. A finished dated document is never edited
while it remains tracked apart from its authorized line-4 update pointer and a mechanically
necessary joining of a prose paragraph that begins on line 3 without changing its text, but
receipt status does not make the document permanent. Treat a base receipt and its optional one
live `<stem>-update.md` as one retirement family: keep or delete the whole family, never only one
member. Never create `<stem>-update-N.md`. A historical numbered sibling found in Git history
remains historical evidence and belongs to the historical family in which it appears; preserving
that file literally does not make numbered siblings current policy.

Before deleting a family, audit GitHub issue bodies and comments owner-wide and classify each
reference. A reference to current guidance is repointed to a current successor or blocks the
deletion. A reference to historical evidence is repointed to the full 40-character SHA of the
last commit whose tree contains every family member. Verify every path there with `git cat-file
-e`; never use `blob/main`, a branch, a tag, a short SHA, or the deletion commit whose tree lacks
the files. Link the base receipt and every update sibling so that the correction sequence remains
visible.

For an open issue, correct a stale body reference with `py/main_github_issue_edit.py`, first with
`--dry-run`, and read the entire outgoing body before applying it. For a closed issue, or a
reference found in any comment, add a dated agent-written correction comment; never edit or delete
an existing comment. Then read back the complete issues, delete the family in one repository
commit, verify, and push. The archival commit must already be on `origin/main` before the issue
links are changed. This audit and the deletion decision remain manual; neither
`py/main_repo_maintenance.py` nor `py/main_repo_util.py` automates them.

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
2026-08-29 the still-paused
[`PLAN-evacuate-the-rest-of-three-repos.md`](https://github.com/bdenckla/MAM-basics/blob/40395aa3d44608e9f63a75897cd8e42e1b1a7338/doc/PLAN-evacuate-the-rest-of-three-repos.md)
cited **seven** of the
nine executed plans, and two of those — `PLAN-evacuate-the-rest-of-wlc-utils.md` and
[`PLAN-evacuate-public-repos-programme.md`](https://github.com/bdenckla/MAM-basics/blob/40395aa3d44608e9f63a75897cd8e42e1b1a7338/doc/PLAN-evacuate-public-repos-programme.md)
— by live markdown link, named as the model it "leans on
rather than restating" and as the source of two sections declared to be its own. Those two were
kept and the other seven deleted (`f6173fe`). The line that held: a plan the surviving work
merely mentions is spent, a plan it tells you to read first is load-bearing.

The rest-of-three plan and the public-repos programme are now completed and retired. Present-state
topology comes from [`all-repos.code-workspace`](../all-repos.code-workspace) and
`gitrepos_setup_rule` in
[`in/repo_maintenance_policy.json`](../in/repo_maintenance_policy.json); the immutable plan links
above are historical evidence.

Report the filenames raised and nothing else — **never a count**, which reads as a defect tally
against repos that have earned their docs. For doc/ files that are *not* plans, the screen stays
the inbound-reference one that same section of `check_repo_standards.py` describes; note that
the screen inverts on plans and must not be used on them.

**7. Audit recursive template and node walkers for undeclared projections — judgment work, not
a `main_repo_util.py` action.** The same recursion syntax serves two opposite purposes: a
template inventory correctly visits every classified branch, while a Scripture survey normally
selects one ketiv/qere, qamats, cantillation, or stress-helper branch. A mechanical rule cannot
decide which purpose a walker serves. Shared helpers also hide the decisive recursion from the
caller's question. Do not add a low-confidence check to `check_repo_standards.py` merely because
`.values()` or `template_param_vals` is easy to find.

Run this search from `C:/Users/BenDe/GitRepos/MAM-basics`; repeat equivalent searches in any repo
that has gained its own MAM/Wikisource consumer since the preceding maintenance run:

```
git -C C:/Users/BenDe/GitRepos/MAM-basics grep -n -E "tmpl_params|template_param_vals|template_param_keys|\.values\(\)|\.items\(\)|flatten|extract|walk|visit|contents|render|text" -- "*.py"
```

The exact anchors are `tmpl_params`, `template_param_vals`, `template_param_keys`, dict
`.values()` and `.items()` loops, recursive `walk`/`_walk`/`visit` functions, and helpers named
`flatten`, `extract`, `render`, `text`, or `contents`. Search names are only the first pass:
follow each shared helper to every caller and inspect the output the caller generates or reports.

Ask these eight classification questions for every reachable recursive walker:

1. What exact survey, transformation, inventory, or rendering question does the caller answer,
   and which tracked or reported output records the answer?
2. Which template and node names can reach the walker, what parameter shape does each name
   require, and does an unknown name raise before recursion begins?
3. Which named parameters are Scripture, documentation, apparatus, formatting, or alternatives?
4. Does the question require ketiv, qere, or both, rather than inheriting an edition-wide choice?
5. Which dual-cantillation, qamats, deḥi, and tsinnor alternative answers the question?
6. If the task is a dataset inventory or structure-preserving transformation, does the module and
   output state explicitly that every classified branch is traversed?
7. Can documentation prose or an unselected alternative satisfy a word, accent, atom, or feature
   search that claims to inspect one Scripture stream?
8. Which canonical generator recreates each affected artifact, and does the regenerated diff
   contain only the changes explained by the corrected projection?

A confirmed blind dive is fixed with named, fail-fast dispatch in the owning semantic consumer.
Raw parser and unparser layers may remain lossless structural recursion when the parser does not
claim that the traversed values are Scripture. Record the files and functions reviewed, including
walkers found valid, so the next maintenance run can distinguish a repeated review from a missed
area.

**8. Retire completed Codex task folders under
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

Linked-worktree retirement has one owner-neutral policy. Load `mam-repository-topology`
and `references/repository-maintenance.md`, section “Completed linked worktrees”; load
`codex-worktree-tasks` and its lifecycle reference when coordinating a Codex task. Claude-only,
Codex-only and both select candidates. An exact path selects one target. All selections share
the same current/primary, active/leased, locked, tracked/untracked, integration, reflog and
object gates, plus citation review and verified `.novc` retention.

Inspect with `--inspect-worktrees --worktree-owner claude|codex|both`, or
`--inspect-worktrees --worktree "C:/absolute/ended-worktree"`. Prepare the selected exact path
with `--prepare-worktree-retirement "C:/absolute/ended-worktree" --task-ended --preflight-file
"C:/absolute/preflight.json"`. Read the JSON and settle every tracked reference to a `.novc`
path that this retirement will relocate; prepare a new file with `--citations-reviewed
--citation-note "disposition"` when necessary. Execute with
`--execute-worktree-retirement "C:/absolute/preflight.json" --task-ended` under the ordinary
user token from a separate checkout. Preparation is nondestructive and does not run the
operational simulation. Every execution and resume attempt runs
`py/repo_util/worktree_retirement_simulation_test.py` first and fails closed before reading the
preflight or mutating the target; only after that pass does the shared executor revalidate and
retire the target. The full absolute PowerShell commands and metadata requirements are in the
shared skill reference.

`--clean-worktrees` now selects Claude candidates for inspection only. Its `--session-ended`
compatibility argument cannot remove anything. Codex-named prepare/execute actions delegate
to the same engine with a Codex selection guard; schema-1 plans must be prepared again.
Neither inspection nor execution prunes registrations or deletes unrelated orphan branches.

Unique ignored `.novc` content does not keep a safe worktree alive. Relocate every `.novc`
outside the target, verify membership, bytes and SHA-256, and keep the JSON provenance.
Unique ignored content outside `.novc` remains a blocker. Retention and disposal are separate:
report each retained path and size, retain by default, and record any later Ben-authorized
Recycle Bin disposal. If Windows unregisters a worktree but leaves ACL residue, record and
measure it, label lower bounds for unreadable entries, and leave it in place. Resume through
the same preflight. Elevation is a separate Ben-chosen residue-disposal stage, never automatic.

**Grandfathered archive recorded 2026-09-15.** The pre-policy archive
`C:/Users/BenDe/.codex/visualizations/2026/09/15/01a0a5e2-b0d2-7e10-a06a-c71acc1ecbac/codex-worktree-retirement-artifacts-2026-09-15.zip`
is retained in place. Its 238 ZIP members preserve paths relative to
`C:/Users/BenDe/.codex/worktrees`, covering `0e63/MAM-private`, `2efd/MAM-basics`,
`36c2/MAM-basics`, `d748/MAM-basics`, `e66d/MAM-basics` and three corresponding orphan-root
entries. Read-only verification on 2026-09-15 found 209 files, 14,999,520 uncompressed bytes, no
bad ZIP member, archive size 6,129,477 bytes, and SHA-256
`21F9A8DA0B974BC9AD8778CBAD352840BA864F76407A0F72EC58029291D7468F`.

Do not extract or repack that verified archive merely to match the new per-`.novc` hierarchy, and
do not pass it to the per-worktree executor: it groups several worktrees and orphan roots and also
contains unique ignored material outside `.novc`. The archive-producing task or Ben should add an
adjacent same-stem JSON record without changing the ZIP. That record names the original path
prefix and source roots above, records each source's `HEAD`, branch and task ID when the source
task can establish them, copies the size/hash/member/ZIP-integrity facts above, dates the creation
and verification with offsets, records each worktree-removal outcome, and sets the current
location and disposition to `retained`. Unknown historical facts are written as unknown rather
than inferred. This maintenance task specifies the registration because the archive's directory
is outside this worktree's writable scope; it does not make that external write.

**The `doc/` sweep was added 2026-08-29, so neither of the two runs recorded above included the
`doc/` sweep** — the 2026-08-07 and 2026-08-27 records describe steps 1–5 only.
**The `Documents/Codex` task-folder step was added 2026-09-04, so neither historic run assessed
those folders either.** **The template-projection audit was added 2026-09-11, so neither historic
run included that audit.**

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
  merged into that repo's default branch before deleting. Re-verify this historical finding;
  current retirement requires the reviewed preflight in step 8 and leaves orphan branches alone.
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

**H1 — Inspection is not retirement authority.** The shared inspector uses Git's
`--no-optional-locks` and never authorizes removal based on index age. Verify the session ended,
prepare a per-target preflight, review it, then execute from a separate checkout. The historical
index-mtime grace could be perturbed by inspection; it is no longer a retirement gate.

**Historical correction, 2026-09-10:** the former `activity_grace_seconds=0` escape was removed
after a live, clean, merged session demonstrated its danger. The replacement `--session-ended`
formerly bypassed age only for named paths. Today that legacy option validates Claude selection
only; it cannot cause deletion. This preserves the incident's lesson without retaining its old
cleanup mechanism.

**H2 — Tracked references to relocated `.novc` paths require review.** Unique ignored content
outside `.novc` blocks retirement. Every selected owner's `.novc` is inventoried, relocated and
verified under step 8, even when small. Every tracked reference to one of those exact relative or
absolute paths requires review; generic `.novc` policy prose does not. Later disposal is a
separate recorded decision. Historical measurement on 2026-08-07 found seven spent ignored files
in two spared MAM-basics worktrees; that observation does not establish that today's contents are
spent.

**H3 — Frozen repos are honored by `--run-black` ONLY (MAM-basics issue #211, open).**
`maintenance_policy.frozen_repos()` is consulted in the `--run-black` branch and nowhere else.
**`--commit-across-repos` can therefore commit to a frozen repo, which is precisely what the
freeze exists to prevent — do not use that action in this sweep.** Frozen repos, verified
2026-08-07 in `in/repo_maintenance_policy.json`, are six: breuer-cos, CCAR-Psalms, MAM-for-Acc,
MAM-for-CCAR, MAM-for-JPS, TMC. Note issue #211's body is itself stale: it says five frozen
repos and "four actions", predating breuer-cos's freeze (2026-07-31) and the
`--check-memory-health` and `--clean-worktrees` actions. Worth a comment on #211 recording
that, rather than a silent fix.

**H4 — Worktree inspection is read-only regardless of repository freeze.** The workspace
roster still bounds discovery. Retirement is separately reviewed and changes local checkout
and eligible branch state; it does not rewrite commits. Never turn a clean inspection into
permission to retire a live worktree.

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

**H8 — Runtime records can block retirement but cannot prove inactivity.** For every owner,
the shared audit reads Claude cwd/session records and desktop leases plus Codex task databases
and writer leases. An unreadable installed format blocks the audit. Missing records still need
an explicit ended-session attestation at preparation and execution. Git locks always block.

1. A runtime can change its private record format or fail to record a session's changed cwd.
   Verify the task ended and keep live worktrees locked; do not substitute index age for proof.
2. Historical observation on 2026-09-10: a Claude session moved from `eloquent-ritchie-0e4c6c`
   to `dual-agent-review-2026-09-10`, while retaining its earlier desktop lease. Both worktrees
   were correctly spared. A stale-looking lease requires investigation, not bypassing.
3. Claude can pool and re-lease a checkout after its original session ends. Codex uses task IDs
   and writer leases instead. These are adapter differences; Git safety and `.novc` handling
   remain identical across selected owners.

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

- **No tracked source file should change except by `--run-black`.** The other cross-repository
  sweeps read only. Shared retirement in step 8 relocates ignored evidence and changes only
  the reviewed target registration and its eligible branch; ownership only selects candidates.
- **`HEX_ESCAPES` findings are advisory and are never auto-fixed** —
  `check_repo_standards.py` says findings are reported, never auto-fixed. Do not start
  converting `\uXXXX` escapes to `\N{...}` across repos as part of a maintenance sweep.
- **A dangling `[[link]]` in a memory file is not an error.** It marks something worth writing
  later. MAM-basics' one dangling link was deliberately left in place on 2026-08-07.
- **A skip in a test suite may be a semantic signal, not a problem.** In MAM-basics' accgram
  tests a skip reports that a page diverges from its strand.

---

## 9. Verification and commit discipline

Re-run each sweep after acting on its findings and confirm the counts moved the way you
expect: `WORKTREE_PROBLEM_COUNT` absent, only the reviewed targets and their eligible branches
retired, no unexpected change outside the selected owners, `WORKTREE_PROJECT_DIRS` at 0 for any repo
whose orphaned session directories you removed, and `MIXED_FILES=0`/`NO_TERM=0` for line terms.
An active or retained worktree of either owner, or a preserved orphan branch, can keep counts nonzero.

For any repo with its own test suite, run it from that repo's root with that repo's own venv
before committing.

Commit directly to `main` in each repo — no feature branches — and push, per Ben's standing
authorization; do not ask, and do not end by handing back an unpushed commit. One commit per
repo. Keep any repo-wide reformat as its own commit (H7). Write multi-line commit messages to
a temp file and use `git commit -F <file>`; no here-strings, no inline `python -c`.
