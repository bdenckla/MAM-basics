# Repository maintenance and local retirement

Read this reference for a maintenance sweep, for Black coverage across repositories, or before
retiring completed Codex task folders, standalone task clones, worktree forests, or disposable
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

## Completed Codex linked worktrees

The cross-repository `--clean-worktrees` sweep is Claude-owned. It may remove a worktree below a
main checkout's `.claude/worktrees/` directory or on a `claude/*` branch; it reports and leaves a
Codex worktree for the owner-specific retirement flow. A Codex cleanup in turn must refuse every
Claude worktree and `claude/*` branch.

Load `codex-worktree-tasks` and its `references/task-lifecycle.md` before retiring a Codex linked
worktree. The task must have ended; the worktree must be inactive, unlocked and safe in tracked,
untracked, ref, reflog and object state; and the branch and `HEAD` must be integrated or otherwise
durably preserved. Unique uncommitted or unmerged work remains a blocker.

Unique ignored `.novc` content alone is not a reason to keep an otherwise removable worktree.
Audit tracked citations into the old `.novc` path, relocate every `.novc` directory to the sparse
absolute-path shadow and JSON-sidecar representation specified by the Codex lifecycle reference,
and verify the relocation before allowing worktree removal. Never overwrite a retirement
destination. A cross-volume relocation copies and verifies membership, byte counts and strong
hashes before removing the source. A failed verification leaves the source and worktree in place.
Known disposable caches retain their existing disposition.

Retention is a separate decision. Report each retained path and size and default to keeping it,
especially when small; ask Ben separately before disposal. Requested disposal uses the Windows
Recycle Bin when recoverability is required, and the surviving registry or sidecar records whether
the material is retained, recycled or deleted.

On Windows, Codex performs the read-only audit, prepares the JSON preflight, and makes the best
safe cleanup attempt under the ordinary user token when cleanup is in scope. An absolute
PowerShell 7 handoff to Ben may invoke the same checked
`py/main_repo_util.py --execute-codex-worktree-retirement` action. The action revalidates the
recorded gates immediately before mutation, refuses drift, avoids force, and uses `git branch -d`.
If Git unregisters the worktree but ownership or ACLs leave a directory, measure its exact path,
readable file count and readable byte total, label lower bounds when anything is unreadable, and
leave the verified residue in place. Do not escalate automatically. Report the residue first;
administrator cleanup is a separate Ben-chosen stage, normally unnecessary for small residue, and
must revalidate and target only that measured unregistered path.

A verified archive created before this representation is grandfathered. Do not extract or repack
it solely for conformity and do not feed arbitrary legacy ZIPs to the per-worktree executor. Add
an adjacent or registry JSON record for the original path prefix, sources and known task/Git
provenance, archive size, SHA-256, member inventory, verification, removal outcome, location and
disposition. Unknown facts remain explicit. If that sidecar is outside the current task's writable
scope, prepare the registration and leave the external write to the archive-producing task or Ben.

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
