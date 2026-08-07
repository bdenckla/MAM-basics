# PLAN — repo maintenance across GitRepos, every repo except MAM-basics

Written 2026-08-07 by the session that had just done MAM-basics' own maintenance. Ben's
request, 2026-08-07: *"do repo maintenance across all repos cloned in GitRepos with the
exception of MAM-basics (since we just did MAM-basics in this session)."*

Everything below is written for a session that has none of that conversation. Every figure
carries the command that re-establishes it; re-measure rather than trust, and treat a
mismatch as a finding.

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
     `C:\Users\BenDe\GitRepos\MAM-basics`, committing to `main`.
   - *"Re-vendor mb_cmn copies stale since the #224 cull"* — ran in worktree
     `C:\Users\BenDe\GitRepos\MAM-basics\.claude\worktrees\gallant-meitner-68c79b`, branch
     `claude/gallant-meitner-68c79b`, and edited five sibling repos (al-hatorah, book-of-job,
     codex-index-aleppo, holman-ketiv-qere, mgketer) as shared clones.

   If either is still live, STOP. `--clean-worktrees` would delete a running session's
   worktree, and `--run-black` would reformat files another session is editing.

2. **The re-vendor branch is merged and its worktree removed.** Check:
   ```
   git -C C:\Users\BenDe\GitRepos\MAM-basics worktree list
   git -C C:\Users\BenDe\GitRepos\MAM-basics branch --list "claude/*"
   ```
   A surviving `claude/gallant-meitner-68c79b` wants merging into `main` first — per Ben's
   standing rule a worktree branch is merged and `main` pushed, rather than the branch pushed.

3. **Every repo is clean and pushed**, so any diff this maintenance produces is attributable:
   ```
   foreach ($d in (Get-ChildItem -Directory C:\Users\BenDe\GitRepos)) { $n = (git -C $d.FullName status --porcelain | Measure-Object).Count; if ($n) { Write-Output "$($d.Name) dirty=$n" } }
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

Run everything from `C:\Users\BenDe\GitRepos\MAM-basics` with
`C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe`.

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
.venv\Scripts\python.exe py\main_repo_util.py --clean-worktrees --workspace-file all-repos.code-workspace
```
Read every `kept ... (reason)` line. A spared worktree is not a failure; it is a question.
`WORKTREE_PROBLEM_COUNT` is the failure signal.

**2–4. The three read-only checks**, in any order:
```
.venv\Scripts\python.exe py\main_repo_util.py --check-repo-standards --workspace-file all-repos.code-workspace --report-txt <file>
.venv\Scripts\python.exe py\main_repo_util.py --check-memory-health   --workspace-file all-repos.code-workspace --report-txt <file>
.venv\Scripts\python.exe py\main_repo_util.py --audit-line-terms      --workspace-file all-repos.code-workspace --report-txt <file>
```
Use `--report-txt`: the one-line-per-repo stdout summary gives counts, and the text report
gives the actual findings. Write reports into `.novc/`, not into a tracked directory.

**5. `--run-black` LAST**, because it is the only one that rewrites source:
```
.venv\Scripts\python.exe py\main_repo_util.py --run-black --workspace-file all-repos.code-workspace
```
Expect `BLACK_PROBLEM_COUNT` absent/zero — see H5 for why, and what a nonzero one means.

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
  `C:\Users\BenDe\.claude\projects\` (`C--Users-BenDe-GitRepos-masorah-books--claude-worktrees-*`).
  Same litter cleaned out of MAM-basics on 2026-08-07 (7 dirs, 50.2 MB). `--check-memory-health`
  reports the count as `WORKTREE_PROJECT_DIRS` but deliberately does not delete them, because
  they hold session transcripts. Check for a `memory/` subdirectory in each before deleting —
  none of MAM-basics' seven had one — and confirm with Ben, who chose deletion for MAM-basics.
- **breuer-cos has 2 orphaned memory files** at
  `C:\Users\BenDe\.claude\projects\C--Users-BenDe-GitRepos-breuer-cos\memory\`. breuer-cos was
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
from the main clone; if a worktree is unavoidable, pass `--repos-root C:\Users\BenDe\GitRepos`
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
$frozen = @('breuer-cos','CCAR-Psalms','MAM-for-Acc','MAM-for-CCAR','MAM-for-JPS','TMC'); $ws = Get-Content "C:\Users\BenDe\GitRepos\MAM-basics\all-repos.code-workspace" -Raw | ConvertFrom-Json; foreach ($f in $ws.folders) { $name = if ($f.path -eq '.') { 'MAM-basics' } else { $f.path -replace '^\.\./','' }; $p = "C:\Users\BenDe\GitRepos\$name"; if (-not (Test-Path $p)) { continue }; $py = (git -C $p ls-files "*.py" | Measure-Object).Count; $wt = ((git -C $p worktree list | Measure-Object).Count - 1); $cb = (git -C $p branch --list "claude/*" | Measure-Object).Count; [PSCustomObject]@{Repo=$name; Frozen=($frozen -contains $name); PyFiles=$py; Venv=(Test-Path "$p\.venv\Scripts\python.exe"); Worktrees=$wt; ClaudeBr=$cb} } | Format-Table -AutoSize
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
  converting `\uXXXX` escapes to `\N{...}` across repos as part of a maintenance sweep.
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
