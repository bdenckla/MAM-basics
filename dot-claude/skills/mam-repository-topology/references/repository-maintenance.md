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
