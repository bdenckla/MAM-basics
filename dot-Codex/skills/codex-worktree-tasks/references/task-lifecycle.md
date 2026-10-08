# Codex worktree task lifecycle

## Prepare a successor last

Before another task receives writing responsibility, make the current worktree clean and commit
the complete handoff state locally. Create or fork the successor only after that commit exists.
The current task remains responsible for final integration when Ben asks to archive it.

An explicit procedure that names a shared branch on `origin` replaces the local-only handoff: the
handoff is complete only after the promised commit is pushed normally to that exact remote branch.
The successor may use another checkout and verifies the fetched remote tip rather than depending
on the predecessor's worktree or checkout-local branch name.

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

Follow the shared `linked-worktrees` skill's `references/integration.md`.

## Retire a completed worktree through the shared policy

Load `mam-repository-topology` and its `references/repository-maintenance.md`, section
“Completed linked worktrees”. That reference is the common retirement policy for Claude,
Codex, both owners, and an exact named target. `codex` is a candidate selector, not a separate
cleanup system. Follow that reference's retirement eligibility, ownership evidence, approval gates,
verified retention and executor procedure; do not duplicate its removal recipe here.

For Codex provenance, the adapter reads task IDs and cwd values from `state_*.sqlite` under
`CODEX_HOME` (default `$HOME/.codex`) and treats a corresponding `thread-writer-locks/<id>.lock`
as a lease. A present lease blocks even after an ended-task attestation. Claude process records
and desktop leases also block retirement of a Codex-selected worktree if a Claude session
occupies it. Do not remove runtime records to get past a gate.

Absence of a writer lease is not proof that a task ended. Verify that the task ended and repeat
`--task-ended` at preparation and execution, from a separate checkout. The executor also refuses
the current checkout and Git-locked worktrees. A stale runtime record requires investigation;
an unreadable installed runtime database fails closed. Runtime format changes may need adapter
updates, without changing the retirement policy.

## Recover or diagnose a mismatch

The shared `linked-worktrees` skill, “Successors, lost edits and generated pages”, holds the
diagnosis and page-verification rules.
