# Repository maintenance and local retirement

Read this reference for a maintenance sweep, for Black coverage across repositories, or before
retiring selected linked worktrees, completed Codex task folders, standalone task clones, worktree forests, or disposable
Claude cache data.

## Mechanical repository sweeps

`all-repos.code-workspace` is the complete roster a sweep can reach.
`in/repo_maintenance_policy.json` records frozen repositories and explains why they are absent
from that roster. `in/vendoring_policy.json` declares tracked paths that a sweep leaves alone.
Do not keep a second remembered repository list.

The MAM-basics Black wrapper is:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --run-black --workspace-file all-repos.code-workspace --repos <repo>
```

Omit `--repos` only for a requested full sweep. The action reformats files, so do not run it to
inspect coverage. It derives whether a repository has Python from tracked `*.py` files and fails
when a repository with tracked Python has no Black installation. A vendored file is formatted in
its source repository, not in each destination copy. A repo-wide reformat is a separate commit.

## Manual document retirement

Use MAM-basics' live `doc/PLAN-repo-maintenance-across-GitRepos.md`, section “The `doc/` sweep —
genuinely last”, for the cross-repository procedure. The sweep is judgment work and remains
outside the maintenance scripts. A finished dated document is immutable while tracked apart from
its authorized line-4 update pointer. A spent base receipt and its optional one live
`<stem>-update.md` form one retirement family and may be deleted together. Never create a numbered
update sibling. A historical numbered sibling remains historical evidence and belongs to the
historical family in which it appears; literal preservation does not make that naming current
policy. Before deletion, audit GitHub issue bodies and comments: current-guidance references
must reach a current successor or block deletion, and historical references must reach the
verified full SHA of the last commit containing every family member. Follow the GitHub-issues
skill's open-body versus closed-issue-or-comment procedure for the corrections.

## Completed Codex task folders

Screen `C:/Users/BenDe/Documents/Codex` after the mechanical repository and document sweeps.
Keep `ReviewForests` even when empty, keep every active task folder, and do not remove the parent
directory while either remains.

A directory containing repository names is not automatically a worktree forest. A reusable
forest has `review-manifest.json` at its root and Git worktrees at the paths the manifest
declares. A linked worktree has a `.git` pointer file; a `.git` directory identifies a standalone
clone. A `proposed/` directory containing copies without Git metadata is a proposal snapshot.

Read a forest manifest before running a repository command inside the forest. Preserve a forest
that names a future phase or handoff. When no manifest exists, inspect every Git directory rather
than calling the directory reusable.

For each standalone task clone, establish all of the following:

1. The working tree is clean.
2. The checked-out commit exists in the primary clone or remote.
3. No local branch or object is the only copy of unmerged work.

`.git/objects/info/alternates` can expose objects belonging to the primary clone.
`git count-objects -vH` helps distinguish objects stored by the task clone itself.

## Completed linked worktrees

Claude-only, Codex-only and both are selection scopes. An exact path selects one registered
worktree, including a worktree with no recognized owner. Every selected target uses
`repo_util.worktree_retirement`; `worktree_owners` supplies only discovery, runtime provenance
and branch eligibility. Never maintain separate cleanup policies by owner.

Retirement is a destructive local act independent of product reach. First establish all gates:

1. The task or session has ended. The target is not the primary or executing checkout, is not
   Git-locked, contains no other registered worktree, and has no running session or runtime lease.
2. Tracked and untracked state is clean, with no Git operation in progress. HEAD and the branch
   are integrated into the local default branch. Worktree reflogs, per-worktree refs, recovery
   pseudorefs and administration objects must not be the only protection of recoverable work.
3. Unique ignored content outside `.novc` blocks retirement. Known regenerable tool caches and
   byte-identical primary-checkout copies may be disposable. Linked directories and uncertain
   objects fail closed; never force removal to bypass the audit.
4. Audit tracked citations into `.novc` in both the target and primary checkout, including
   primary receipts added after the target's HEAD. Review every match semantically, promote a durable
   result or record its relocated path, and give a substantive citation note. An unreadable
   citation is a blocker. Generic `.novc` references can be recorded as generic after review.
5. Inventory every `.novc` and relocate it outside the worktree using the shadow layout below.
   Verify membership, bytes and SHA-256 before Git removal. Retain its JSON provenance.

Claude discovery recognizes `.claude/worktrees/` beneath the primary checkout and `claude/*`
branches. Codex discovery recognizes `CODEX_HOME/worktrees/` and `codex/*` or `codex-*` branches.
Conflicting owner evidence blocks retirement. An exact target with a non-agent branch can retire
its checkout while retaining the branch. Only the successfully retired target's unchanged,
integrated branch matching its owner prefix is eligible for `git branch -d`; orphan branches
and branches outside the selected scope remain. Inspection never prunes registrations or
sweeps empty directories.

For every target, read both runtimes. Claude contributes `$HOME/.claude/sessions/*.json` cwd
records and `%APPDATA%/Claude/git-worktrees.json` desktop leases. Codex contributes cwd/task IDs
from `CODEX_HOME/state_*.sqlite` and `thread-writer-locks/<id>.lock` writer leases. Present
records block activity they identify, including cross-owner occupancy. Missing records do not
prove inactivity; unreadable installed formats block the audit. A writer-lock file can outlive
its writer, so its presence conservatively blocks until the runtime record is investigated.
The adapter does not remove or unlock it. The old index-mtime grace is
not an authorization to remove anything. Explicit ended-task attestations are required instead.
An unrecorded session or a runtime that changes its format remains a real limitation: verify the
session ended, honor Git locks, and do not remove or bypass a lease merely to complete cleanup.

### Inspect, prepare and execute

Run from the primary MAM-basics clone with its interpreter. Inspection across the workspace is
read-only and selects only the requested owners:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_repo_util.py --inspect-worktrees --worktree-owner claude --workspace-file C:/Users/BenDe/GitRepos/MAM-basics/all-repos.code-workspace
```

Use `--worktree-owner codex` or `--worktree-owner both` for those scopes. To inspect one target,
use `--inspect-worktrees --worktree "C:/absolute/ended-worktree"` instead of an owner selector.
Inspect each blocker and verify the target's session ended before preparation. Preparation is
per target so a citation review and ended-session attestation cannot spill across candidates:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_repo_util.py --prepare-worktree-retirement "C:/absolute/ended-worktree" --task-ended --preflight-file "C:/absolute/preflight.json"
```

The default durable retention root is `$HOME/worktree-retirements`; override it with
`--retirement-root`. Both the preflight and retention root must be outside the target. Optionally
add `--worktree-owner claude|codex|both` as a preparation selection guard. Record additional known
Codex IDs with `--codex-task-id`; the adapter also discovers IDs. If citations are reported,
settle them and prepare a new file with `--citations-reviewed --citation-note "disposition"`.
The preflight freezes the safety snapshot, owner selection, inventories and destinations.
Preparation remains nondestructive and does not run the operational retirement simulation.

Review the preflight, then execute under the ordinary user token from a separate checkout:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_repo_util.py --execute-worktree-retirement "C:/absolute/preflight.json" --task-ended
```

Every execution and resume attempt first runs
`py/repo_util/worktree_retirement_simulation_test.py` through `py/main_test.py`. The command
fails closed unless the simulation passes, before it reads the preflight or mutates the target.
Only then does execution repeat runtime and Git safety checks, refuse drift, relocate and verify
`.novc`, and use non-forced `git worktree remove` and eligible `git branch -d`. Reuse the same
preflight to resume a recorded removal attempt; the simulation runs again. A registration
removed outside that recorded attempt is a blocker. A failed or ambiguous relocation leaves
evidence in place for inspection; do not improvise a force flag or delete the sidecar.

Compatibility: `--clean-worktrees` now means Claude-only inspection and never removes anything.
Its `--session-ended` paths are checked against that scope, but cannot cause retirement. The
Codex-named prepare and execute actions use the same preparation behavior and mandatory
execution simulation, then route through the shared engine with a Codex selector.
Schema-1 preflights must be prepared again because they omit the shared runtime and object gates.
Repository maintenance uses the same inspection API. Remote-only work is reported from cached
refs, labelled as such; fetch separately when fresh remote evidence is needed.

### Partial Windows removal

Re-read Git's worktree registry after every removal attempt. If Git unregisters the worktree
while Windows ACLs leave files behind, record the unregistered residue and leave it in place.
Report its exact path, readable file count and readable bytes; label both figures as lower
bounds when any entry or subtree is unreadable. Persist the removal result and branch outcome
in the preflight and `.novc` sidecars so resuming is truthful. Runtime and current-path checks
still apply on resume, even when the target is unregistered or held no `.novc`.

Elevation is a separate Ben-chosen residue-disposal stage. Do not request it automatically.
Report the measured residue first; small residue normally remains. If Ben chooses administrator
cleanup, revalidate the exact path, absent registration, retained `.novc` provenance and current
measurement immediately before acting only on that residue. A failed removal that leaves the
registration and alters tracked files needs inspection; the executor never treats missing
tracked files as a clean checkout.

### Retirement hierarchy and metadata

Name an absolute durable retirement root outside the worktree. Below that root, preserve a sparse
shadow of the former absolute parent path:

- `C:\Users\BenDe\...` maps to `drive-C/Users/BenDe/...`.
- `\\server\share\...` maps to `unc/server/share/...`.
- `/...` maps to `root/...`.

At that shadow location, give each retained directory a timestamp-and-random collision-safe name
of the form `.novc--<retirement-id>` and place an adjacent same-stem JSON sidecar. Never overwrite
an existing directory or sidecar. The sidecar records at least the schema version, original
`.novc` and worktree paths, primary repository path, `HEAD`, branch or detached state, discoverable
Codex task IDs and Claude session IDs, selected owners, retirement timestamp with offset, destination, file count, total bytes,
verification manifest and algorithm, relocation method, current disposition, and whether the
worktree and branch were removed.

A same-volume rename is acceptable after a complete pre-move inventory and a post-move
verification. Across volumes, copy first, verify file and directory membership, byte counts and
SHA-256 hashes, and remove the source only after verification succeeds. A verification failure
leaves the source and worktree in place. Report every relocated path and measured size.

The initial disposition is `retained`; retention is not a reason to postpone worktree retirement.
Default to keeping the material, especially when it is small, and do not turn a directory of about
10 KiB into a deletion dilemma. Ask Ben separately whether retained material should be recycled.
When disposal is requested, use the Windows Recycle Bin where repository-maintenance policy
requires recoverability and update the surviving registry or sidecar disposition to `recycled` or
`deleted`. Do not silently discard a sidecar with the directory it describes.

### Grandfather verified pre-policy archives

A pre-policy ZIP or other archive that already preserved worktree evidence need not be extracted
or repacked merely to imitate the per-`.novc` shadow layout. Keep the verified archive bytes and
add an adjacent or retirement-registry JSON record. Record the archive's original source-path
prefix, source worktrees and orphan roots, known `HEAD`, branch and available task/session provenance, archive
byte size and SHA-256, member inventory or its verified manifest, creation and verification facts,
worktree-removal outcome, current location and current disposition. Mark unknown historical facts
as unknown; do not infer them from a filename.

The normal per-worktree executor does not ingest arbitrary legacy archives. Register a legacy
archive with a separate, read-only inventory and sidecar-writing procedure after verifying the
existing bytes. Do not extract, recompress, rename or relocate the archive unless Ben separately
asks. If the archive or registry lies outside the cleanup task's writable scope, prepare the exact
metadata and leave the external sidecar write to the archive-producing task or Ben.

## Claude cache and temporary data

Look for Claude cache and temporary-data directories outside `Documents/Codex` without assuming
a fixed path. Report the exact path and measured size for each verified cache or temporary
directory; a directory of at least 1 GiB is a maintenance finding. Size alone does not prove that
a directory is disposable. Project directories, transcripts, and `memory/` can be durable work,
so leave an uncertain directory in place.

Recycle every verified retirement through the Windows Recycle Bin rather than deleting it
permanently. State the exact path and why it is safe. Leave ambiguous folders in place and report
the unresolved question. Recycled contents remain recoverable but keep consuming disk until the
Recycle Bin is emptied.
