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

## Load the reference for the selected work

- For a new Codex-managed worktree's branch, or Windows `safe.directory` errors, read
  [references/worktree-runtime.md](references/worktree-runtime.md).
- Before creating, forking, recovering, handing off, or archiving a Codex task, read
  [references/task-lifecycle.md](references/task-lifecycle.md).

Repository instructions choose the required broad integration check and can add stricter
preconditions.
