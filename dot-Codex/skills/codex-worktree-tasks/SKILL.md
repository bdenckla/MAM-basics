---
name: codex-worktree-tasks
description: Ben's Codex-only rules for creating, forking, handing off, recovering, or archiving Codex tasks that use Git worktrees, and for a new Codex-managed worktree's branch name and Windows Git trust. Load the shared linked-worktrees skill as well for the agent-neutral worktree rules.
---

# Codex Worktree Tasks

Keep the task attached to the intended checkout and preserve the Git state that carries its work.
The agent-neutral rules for any linked worktree, including branch pushing, the home clone's
environment, successors, lost-edit diagnosis and integration, live in the shared
`linked-worktrees` skill; load it with this one. This skill adds what is specific to Codex's
managed worktrees and tasks.

## A full clone is the default checkout

By Ben's decision of 2026-10-20, Codex works by default in full clones in the forests it owns,
`$HOME/GitRepos3` and, when it needs another place, `$HOME/GitRepos4`, rather than in new
worktrees; the common instruction body's “Clone forests and portable work” gives the ownership
rule. A Codex-managed worktree remains permitted when a task needs one. Create it only from a
saved project whose clone is in a Codex forest: integration fast-forwards the home clone's
`main`, and `$HOME/GitRepos` and `$HOME/GitRepos2` belong to Claude.

## Load the reference for the selected work

- For a new Codex-managed worktree's branch, or Windows `safe.directory` errors, read
  [references/worktree-runtime.md](references/worktree-runtime.md).
- Before creating, forking, recovering, handing off, or archiving a Codex task, read
  [references/task-lifecycle.md](references/task-lifecycle.md).

Repository instructions choose the required broad integration check and can add stricter
preconditions.
