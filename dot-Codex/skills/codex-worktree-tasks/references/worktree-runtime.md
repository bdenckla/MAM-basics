# Worktree runtime

## Verify or establish the branch

Codex creates the managed worktree before the task starts. Verify the absolute checkout path,
`HEAD`, branch state, and cleanliness before editing.

If `HEAD` is detached in a newly created managed worktree, create and switch to
`codex-worktree-<worktree-id>` at the current `HEAD`. The identifier is the directory directly
under `.codex/worktrees/`: for example, `.../worktrees/a3ff/MAM-basics` uses
`codex-worktree-a3ff`. Preserve an existing checked-out branch unless Ben asks to rename it. If
the proposed name exists, inspect its commit and worktree association before proceeding; never
overwrite it.

## Use Git's local trust exception

Windows can report dubious ownership when the worktree was created under another SID. In an
elevated Windows session, do not wait for that failure. Pass the exact absolute worktree path on
the first Git invocation and every subsequent Git invocation. Never use `safe.directory=*` and
never add the worktree to global Git configuration:

```powershell
git -c "safe.directory=C:/absolute/worktree/repo" -C "C:/absolute/worktree/repo" status --short --branch
```

For a parent program that starts Git, inject the equivalent exact path with
`GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_<n>`/`GIT_CONFIG_VALUE_<n>` into that program's process-local
environment so its Git descendants inherit the trust entry. The ownership warning does not
establish corruption, dirt, or a wrong commit. Trust does not grant filesystem access: if a Git
metadata write crosses a sandbox boundary and is denied, use the normal escalation path.

## Share the primary clone's Python environment

A worktree normally has no `.venv` because the directory is ignored. Use the primary clone's
interpreter by absolute path while keeping the current directory and script path in the
worktree:

```powershell
C:/Users/BenDe/GitRepos/<repo>/.venv/Scripts/python.exe py/main_<x>.py
```

CPython puts the worktree script's directory on `sys.path[0]`, so the primary clone's
interpreter still imports the worktree's `py/` modules. A repository root derived from
`Path(__file__)` also remains the worktree.

Never junction or symlink the primary `.venv` into the worktree: worktree removal can follow the
junction and empty the real environment. Do not copy the environment as a shortcut; Windows
console scripts embed the source interpreter's absolute path. A worktree whose declared purpose
is testing a different dependency set may have a real environment of its own; say why.

Check for sibling paths computed as `repo_root().parent / "<sibling>"` before running a suite.
They resolve under the managed-worktree directory rather than under `GitRepos`. Use the
repository's supported override, such as `REPOS_ROOT`, instead of editing or reading from an
unrecorded primary clone.
