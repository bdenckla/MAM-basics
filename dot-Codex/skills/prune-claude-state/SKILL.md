---
name: prune-Codex-state
description: Review this repository's global .codex/plans draft files against live tracked state and complete relevant issues, and propose stale plans for deletion with explicit confirmation.
when_to_use: Use only when Ben asks to review or prune this repository's draft plan files; routine repository maintenance is separate.
disable-model-invocation: true
---

# Plan pruning

This manual, on-demand procedure addresses only the current repository's drafts in the global
plan directory. These files live outside Git. Preserve ambiguous or unfinished plans.

## Discover this repository's plans

Identify the exact checkout and its origin. The default plan directory is `$HOME/.codex/plans/`;
honor the runtime's configured home when it differs. Read candidate Markdown plans and keep only
files clearly belonging to this repository. A sibling mention alone does not establish ownership.
Read-only delegation may summarize a large inventory; the executor verifies adopted claims.

## Cross-check completion

Compare each candidate with live tracked state, required commits and its named maintained plan.
For relevant issue evidence, load `github-issues` and read the complete issue, including body,
comments, state and labels, with an explicit repository. An issue's closed state alone does not
prove the plan's deferred work is complete. Keep a plan with unfinished or deferred work, an
unresolved discrepancy, or uncertain ownership.

## Present exact lists and obtain approval

Show separate keep and proposed-delete lists with each absolute path and a substantive reason.
Record the proposed files' sizes and SHA-256 values. Ask Ben for explicit approval of that exact
deletion list in ordinary conversation. Approval of a review is not deletion permission.

## Apply only the approved deletions

Re-read the approved files and reject changed or added entries until their refreshed evidence
is approved. Resolve each literal path within the identified plan directory. Delete only the
unchanged approved files with a native filesystem method; do not recursively remove directories
or modify other account state. Report the files actually removed and preserve every unapproved
or ambiguous plan.
