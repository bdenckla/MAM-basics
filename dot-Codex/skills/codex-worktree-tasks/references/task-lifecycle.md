# Codex worktree task lifecycle

## Prepare a successor last

Before another task receives writing responsibility, make the current worktree clean and commit
the complete handoff state locally. Create or fork the successor only after that commit exists.
The current task remains responsible for final integration when Ben asks to archive it.

Identify all three before creating a successor:

1. The source task and its actual checkout.
2. The saved project's absolute path.
3. The required source commit containing the work.

A fresh task continuing a named worktree uses that saved project directly with a local
environment. A `working-tree` starting state means the selected project's checkout, not
automatically the caller's checkout. Put the verified source path, required commit, intended
development location, and final-integration responsibility in the successor prompt.

Creation can return a provisional client task ID while setup continues. Do not pass that value to
tools requiring a task ID, substitute a similarly titled task, or repeat creation because a task
listing omits pending or running work. Record the returned IDs and inspect the exact task.

Require the successor to verify `git rev-parse --show-toplevel`, `git rev-parse HEAD`, branch or
detached state, and `git status --porcelain` before editing. A deliberately newer starting point
must contain the required commit as an ancestor.

## Treat handoff routing as configuration

Inspect the available handoff operation and establish its exact destination before invoking it.
A path written in a follow-up prompt does not configure routing. Do not use handoff to discover
where a task will move. Preserve stale-checkout work and inspect commit ancestry before choosing
an integration; commit distance alone does not predict conflicts.

A co-present task is normally the handoff partner, not a precondition failure. Do not watch
transcript byte counts. Prove non-collision directly: the recorded starting `HEAD` still matches
before commit, status before staging contains only the current task's paths, and the eventual
push is a normal fast-forward with no force.

## Integrate immediately before archival

Once the worktree and primary checkout are clean:

1. In the worktree, merge `main` into the worktree branch. Resolve conflicts and make any fixes
   on that branch.
2. Run the repository's required broad check on the merged branch. Commit every explained
   generated change there; an unexplained change is a failure.
3. In the primary clone, fast-forward `main` with
   `git -C <primary-clone> merge --ff-only <worktree-branch>`. If `main` moved, return to step 1
   instead of creating a second merge in the primary clone.
4. Push `main` normally.

The primary clone receives only the verified fast-forward. Removing the worktree and deleting its
branch wait until the task has ended on Windows; never force removal around a live process.

## Retire a completed Codex worktree without losing `.novc`

Worktree retirement is a destructive local act, separate from product reach and separate from
retention of the worktree's ignored material. A completed task is not enough by itself. Before
retirement, establish every ordinary gate:

1. The Codex task has ended, the worktree is inactive and unlocked, and the cleanup command is not
   running from that worktree.
2. The tracked and untracked working state is safe. Unique uncommitted or unmerged work remains a
   blocker.
3. The worktree's `HEAD` and branch are fully integrated into the primary branch or are otherwise
   durably preserved. No commit, reflog entry, object, or other recoverable work may exist only in
   the worktree administration directory.
4. The target is explicitly Codex-owned. A Codex retirement never selects or mutates a worktree
   under `.claude/worktrees/` or a `claude/*` branch.
5. Tracked documentation, receipts and commands have been searched for citations into each old
   `.novc` path. Promote a durable result to a tracked or stable location, or record the relocated
   path, before removing the worktree. A human reviews the matches; a grep count is not a semantic
   disposition.

Known disposable tool caches can still be discarded under repository maintenance policy. Any
other unique ignored content outside `.novc` blocks retirement. Unique ignored content under one
or more `.novc` directories does not keep an otherwise safe worktree alive: relocate every
`.novc` directory, verify the retained copy, and only then remove the worktree and an eligible
merged Codex branch.

Use `py/main_repo_util.py --prepare-codex-worktree-retirement` from the primary MAM-basics clone to
write a new JSON preflight outside the target. Record every discoverable Codex task ID. If the
preflight reports tracked `.novc` citations, inspect and settle them, then prepare a new preflight
with `--citations-reviewed` and a substantive `--citation-note`. A ready preflight freezes the
worktree path, primary repository, `HEAD`, branch or detached state, integration and reflog checks,
ignored-content classification, citation audit, `.novc` inventories and collision-free
destinations. It does not mutate the target.

After the task has ended, run `py/main_repo_util.py --execute-codex-worktree-retirement` under the
ordinary user token from a separate checkout or cleanup task, using the primary MAM-basics
interpreter, the absolute preflight path and `--task-ended`. A valid PowerShell 7 handoff to Ben is
also useful when Ben will run the command. The executor repeats the safety audit and refuses drift
before mutation. It never passes force to `git worktree remove`, deletes only the target's merged
Codex branch with `git branch -d`, and never reaches a Claude worktree or branch. Codex makes the
best safe ordinary-token cleanup attempt when cleanup is in scope; a task still cannot remove the
worktree it is running in.

Windows can let Git unregister the worktree while ownership or ACLs leave files behind. Re-read
Git's worktree registry after every removal attempt. If the target is unregistered, classify the
remaining directory as verified residue rather than treating elevation as the default next step.
Measure and report its exact path, readable file count and readable byte total; if any entry or
subtree is unreadable, label both figures as lower bounds and report the unreadable count. Leave
the residue in place. The preflight and `.novc` sidecars record whether the worktree remains
registered, the removal message, the residue measurement and the completed branch action so the
ordinary-token command can resume truthfully after a partial Git removal.

Elevation is a separate, user-chosen residue-disposal stage. Do not request elevation
automatically. First report the measured residue and narrower risk, then let Ben decide whether it
is large or troublesome enough to justify administrator access. Small residue normally remains.
Only after Ben chooses that stage, provide or run an administrator-requiring command that targets
the one measured, Git-unregistered residue path and revalidates the path, absent worktree
registration, retained `.novc` provenance and current measurement immediately before deletion.

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
Codex task IDs, retirement timestamp with offset, destination, file count, total bytes,
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
prefix, source worktrees and orphan roots, known `HEAD`, branch and Codex task provenance, archive
byte size and SHA-256, member inventory or its verified manifest, creation and verification facts,
worktree-removal outcome, current location and current disposition. Mark unknown historical facts
as unknown; do not infer them from a filename.

The normal per-worktree executor does not ingest arbitrary legacy archives. Register a legacy
archive with a separate, read-only inventory and sidecar-writing procedure after verifying the
existing bytes. Do not extract, recompress, rename or relocate the archive unless Ben separately
asks. If the archive or registry lies outside the cleanup task's writable scope, prepare the exact
metadata and leave the external sidecar write to the archive-producing task or Ben.

## Recover or diagnose a mismatch

Before searching stashes or unreachable objects, refresh `HEAD`, status, recent commits, reflog,
and the relevant file diffs. A checkout that was dirty earlier can now be clean because another
task committed the work. An unreachable snapshot is not evidence of loss without provenance and
a comparison with committed work.

Verify the exact generated page or artifact path Ben will review. A commit in one worktree does
not update another checkout, `main`, or the remote. State the checkout and commit containing the
result, and include any required integration in completion.
