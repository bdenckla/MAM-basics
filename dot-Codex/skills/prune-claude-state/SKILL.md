---
name: prune-Codex-state
description: Review this repo's Codex auto-memory files and this repo's entries among the global ~/.Codex/plans/ plan files, cross-check each against live GitHub issue state, and propose stale ones for deletion (with explicit confirmation before deleting anything).
when_to_use: Use when the user asks to clean up / prune / review Codex's memory or plan files for the current repo, or asks "what memory/plan files are stale" — not for routine repo maintenance (tests, rebuilds, .novc), which is a separate script.
disable-model-invocation: true
---

Manual, on-demand hygiene pass over Codex's *own* persisted state for the
current repo: the auto-memory directory and this repo's slice of the global
plan-file directory. Both live outside git (no undo), so nothing is ever
deleted without an explicit user confirmation. This is expensive (multiple
`gh issue view` lookups, possibly a research agent) — that's why it's a
separate on-demand skill rather than something bundled into routine repo
maintenance.

## Step 1 — Read this repo's memory

The system prompt at the start of this session already states this repo's
memory directory path (look for "You have a persistent, file-based memory
system at ..."). Read `MEMORY.md` in that directory, then read every memory
file it links to.

## Step 2 — Find this repo's plan files

Plan files live in `~/.Codex/plans/*.md` and are **global, not per-repo** —
most belong to other repos. Identify the current repo (name, GitHub
`owner/repo` slug from `git remote -v`, and any sibling-repo names it
interacts with). If there are more than ~15 plan files, delegate the read to
an Explore (or general-purpose) agent rather than reading all of them
yourself, since most content is irrelevant and shouldn't bloat this session's
context — ask the agent to report back only: filename, does it mention this
repo (yes/no), referenced GitHub issue number(s) if any, and one line on
whether the plan's own text claims the work is done.

Keep only the files that clearly reference the current repo.

## Step 3 — Cross-check against live state, not the file's own text

A file's own prose is not a reliable "is this done" signal — this kind of
review has previously misjudged an issue as still-open hours after it was
actually closed, and separately missed that an issue can be *deliberately*
left open (a deferred follow-up) even though the plan's main content is fully
committed. So for every GitHub issue number found in a candidate memory or
plan file:

- Run `gh issue view <n> --json state,title,closedAt` (or `gh issue list
  --state all` once, up front, and match against it) to get the live state.
- If the file claims specific commits landed, spot-check with `git log --grep`
  or `git log --oneline -- <path>` rather than trusting the claim.

A memory or plan file is a delete candidate only when the live issue state
(closed, no deferred follow-up mentioned) *and* the file's own content agree
the described work is finished. If the issue is open, or is closed but the
file/issue mentions deferred/follow-up work, keep it.

## Step 4 — Build and show the proposed lists

Produce two lists with a one-line reason each: **proposed delete** and
**keep** (memory files and plan files together, clearly labeled). Print the
full lists as text — do not try to cram a large list into `AskUserQuestion`
options (that tool caps at 4 options per question, so it can't hold a
per-file checklist).

## Step 5 — Confirm before deleting

Ask exactly one `AskUserQuestion` question: whether to proceed with the
proposed deletions. Offer options roughly like "Delete all N (Recommended)",
"I'll tell you which to keep/skip" (then continue in normal conversation —
the user will name exceptions in free text), and "Cancel, delete nothing".
Never delete anything the user hasn't confirmed, and never batch this
confirmation with unrelated deletions from a different run.

## Step 6 — Apply confirmed deletions

- Delete the confirmed memory `.md` files, then remove their corresponding
  index lines from `MEMORY.md` (do not touch entries that weren't confirmed
  for deletion).
- Delete the confirmed plan `.md` files under `~/.Codex/plans/`.
- Report what was actually removed.

Leave everything not explicitly confirmed untouched, including plan files
belonging to other repos (Step 2 should have already excluded most of those,
but don't second-guess ambiguous cases into the delete list — when in doubt,
keep).
