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

## Use the home clone's Python environment

The shared `linked-worktrees` skill, “Use the home clone's Python environment”, holds the
interpreter, environment and sibling-path rules.
