---
name: codex-worktree-tasks
description: Ben's rules for creating, verifying, recovering, handing off, or archiving Codex tasks that use Git worktrees, and for ordinary work inside a Codex-managed worktree. Covers exact checkout and commit verification, branch naming, shared virtual environments, local Git trust, one-writer handoffs, and final integration. Do not use for a multi-repository review forest; use worktree-forest.
---

# Codex Worktree Tasks

Keep the task attached to the intended checkout and preserve the Git state that carries its work.
These rules apply to a single-repository Codex task; the `worktree-forest` skill governs a
coordinated multi-repository forest.

## Rules that apply throughout

1. Verify the exact checkout before editing: run `git rev-parse --show-toplevel`,
   `git rev-parse HEAD`, inspect branch or detached-HEAD state, and run
   `git status --porcelain`. A required commit must equal `HEAD` or be an ancestor of it.
2. Treat the primary clone as the integration checkout, not the development workspace. In a
   secondary-worktree task, source edits, generators, formatters, tests, staging, and commits all
   run in the verified worktree.
3. Keep one writer per checkout. Before staging, confirm that `HEAD` still equals the recorded
   pre-work head and that status contains only paths owned by the task.
4. Commit finished work on the worktree's local branch. Do not push the worktree branch or merge
   it into `main` merely as a backup or merely to create a successor task. The no-push exception
   is a long-lived worktree branch whose merge into `main` is not scheduled for when its session
   is archived—for example, because Ben has said it merges only when he asks. Push such a branch
   to `origin` after every commit as a backup and so the work can resume on another machine; this
   still pushes nothing to `main`. A short-lived worktree branch still pushes nothing. Ben's
   reason, 2026-09-15: "Seems like a good idea, as a backup, in case something happens to the
   machine we're working on (and if we wanted to resume that work on another machine, regardless
   of whether data loss happened!)". The first case was MAM-private's branch
   `worktree-near-aleppo`, first pushed 2026-09-15; its own `CLAUDE.md` has carried the rule since
   MAM-private commit `a99d7eb`.

## Load the reference for the selected work

- For ordinary worktree setup, branch state, Python environments, sibling paths, or Windows
  `safe.directory` errors, read [references/worktree-runtime.md](references/worktree-runtime.md).
- Before creating, forking, recovering, handing off, or archiving a Codex task, read
  [references/task-lifecycle.md](references/task-lifecycle.md).

Repository instructions choose the required broad integration check and can add stricter
preconditions.
