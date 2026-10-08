---
name: linked-worktrees
description: Ben's rules, for Claude and Codex alike, for working in a linked Git worktree of any clone forest — its branch and when to push it, its home clone's Python environment, one-writer handoffs and successors, diagnosing apparently lost edits, verifying a generated page, and integrating the branch into main by fast-forward. Use for any work in, handoff from, or integration of a linked worktree.
---

# Linked worktrees

These rules apply to linked worktrees in any clone forest, whichever agent works in them. The
common instruction body keeps the rules every session needs: verify the exact checkout before
editing, use the home clone's interpreter by absolute path, and never junction, symlink or copy
the home clone's environment. A multi-repository review procedure may add its own manifest and
stricter ownership rules. ChatGPT-Codex also loads `codex-worktree-tasks` for creating, forking
and archiving Codex tasks and for a Codex-managed worktree's branch name.

## Rules that apply throughout

1. **The worktree is the development checkout; its home clone is the integration checkout.**
   Source edits, scripts, generators, formatters, tests, staging and commits all run in the
   verified worktree. An explicit repository procedure may instead assign a full checkout to a
   named shared branch on `origin`; that procedure then owns the development and integration
   roles for its workflow.
2. **One writer per checkout.** Before staging, confirm that `HEAD` still equals the recorded
   pre-work head and that status contains only paths the task owns.
3. **Use the worktree's existing local branch and do not push it.** Commit there. Do not push
   the worktree branch or merge it into `main` merely as a backup or merely to create a
   successor task.
4. **A long-lived branch is pushed after every commit.** The exception to rule 3 is a worktree
   branch whose merge into `main` is not scheduled for when its session is archived, for
   example because Ben has said it merges only when he asks. Push such a branch to `origin`
   after every commit as a backup and so the work can resume on another machine; this still
   pushes nothing to `main`. Ben's reason, 2026-09-15: "Seems like a good idea, as a backup, in
   case something happens to the machine we're working on (and if we wanted to resume that work
   on another machine, regardless of whether data loss happened!)". The first case was
   MAM-private's branch `worktree-near-aleppo`, first pushed 2026-09-15; its own `CLAUDE.md` has
   carried the rule since MAM-private commit `a99d7eb`.
5. **A shared branch on `origin` replaces the local branch as the boundary.** When an explicit
   procedure names one shared branch on `origin`, every authorized checkout may use its own local
   carrier branch, and each completed handoff commit is pushed to that exact remote branch. The
   local branch name and checkout path are not shared state; do not publish the carrier name as
   another remote branch. Follow the branch's explicit authorization and integration procedure.
6. **Integrate immediately before the task is archived**, or earlier only when Ben asks or a
   concrete dependency requires it, by following the repository's integration check and
   [references/integration.md](references/integration.md).

## Use the home clone's Python environment

A worktree normally has no `.venv` because the directory is ignored. Keep the current directory
and script path in the worktree while naming the home clone's interpreter:

```powershell
C:/absolute/home-clone/.venv/Scripts/python.exe py/main_<x>.py
```

CPython puts the worktree script's directory on `sys.path[0]`, so the home clone's interpreter
still imports the worktree's `py/` modules, and a repository root derived from `Path(__file__)`
remains the worktree. Junction or symlink removal can follow the link and empty the real
environment, and a copied environment fails because Windows console scripts embed the source
interpreter's absolute path. A worktree whose task requires different dependencies may have a
freshly created environment of its own; state that reason.

Before running a suite, follow the repository's test-entrypoint and sibling-path instructions,
using a repository-supported sibling-path override when the worktree layout requires one.
MAM-basics resolves a linked worktree's siblings through Git's common-directory metadata; its
`AGENTS.md`, “Running tests”, is the authority. `REPOS_ROOT` remains an override for an unusual
layout, not a normal worktree prerequisite.

## Successors, lost edits and generated pages

A successor continuing work in a named worktree uses that checkout directly. Create additional
isolation only when Ben asks or concurrent editing requires it, and state the reason. A Claude
task chip that creates a fresh worktree is the wrong handoff vehicle when the work must continue
in a named checkout.

Before diagnosing lost edits, refresh `HEAD`, task-owned status, recent commits, reflogs and the
relevant diffs. A checkout that was dirty earlier can now be clean because another task committed
the work. Compare the actual provenance before consulting stashes or unreachable commits; a
matching path or an unreachable snapshot alone does not establish lost work.

When Ben reviews a generated local page, identify and verify the exact page path, checkout and
commit. A worktree commit does not update another checkout, the home clone's `main` or a remote
branch. State the checkout and commit containing the result, and include any required
integration in completion.

## Claude cloud applicability

A Claude cloud session's own checkout is normally a full clone with its own environment, so
these rules apply there only when the session creates or works in a linked worktree. The
Windows commands above are examples for Ben's machines; a Linux checkout names
`.venv/bin/python` instead. Installing this skill supplies rules, not credentials, sibling
clones or permissions.

## Canonical copy

This skill is canonical at `MAM-basics/dot-claude/skills/linked-worktrees/` and is shared with
Codex through `dot-claude/shared-skills.txt`. Ben's decision of 2026-10-08, "pursue all of
those trims", moved these rules here from the common instruction body and from
`codex-worktree-tasks`. Change the canonical copy first, then use the deployment procedure in
`dot-claude/README.md`.
