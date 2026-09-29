---
name: iterative-document-editing
description: Ben's workflow for planning and carrying out multi-turn or multi-session edits to prose, Markdown, generated pages, reports, plans, and other evolving documents. Use when requirements may change across messages, several tasks may inspect the same material, or an approved plan will be handed to a fresh executor. Do not use for a one-turn typo or mechanical formatting correction.
---

# Iterative Document Editing

Keep planning, approval, execution, and handoff explicit while a document's requirements evolve.

## Keep planning read-only

- Follow the common instruction body's “Planning remains planning until explicit execution”
  section for the authorization gate.
- Reconcile every visible user message, annotation, and supplied input before declaring the
  specification or plan complete.

## Maintain cumulative state

- Keep one compact cumulative revision ledger. Mark each requirement `active`, `superseded`,
  `implemented`, `deferred`, or `unresolved`.
- When several images, citations, links, or other source materials are involved, maintain an
  input manifest with each item's identity, provenance where relevant, requested use, and
  disposition. Never infer identity from a filename or timestamp. An unresolved in-scope item
  blocks execution.

- Ask one independent decision at a time with the facts needed to answer it.
- Maintain one tracked plan per undertaking. Revise that plan as requirements change, and
  identify each deferred decision's file, searchable section and responsible stage.

## Executable plans

Every executable plan is a handoff artifact for a fresh executor with no access to the
surrounding conversation. Keep the plan proportional: a short task can have a short standalone
plan. A repository execution plan is worktree-compatible by default; an exception states why
the task cannot run in a worktree and names the alternative checkout.

Each plan identifies:

1. Absolute source, development and primary integration checkout paths, and the checkout where
   each command runs. Record the actual development path and exact HEAD before editing.
2. Required baseline commits and ancestry checks, the shared interpreter, required skills and
   instruction files, and the executor who owns final integration.
3. Dated and attributed decisions. Figures that must stay current have baseline commits and
   re-measurement commands; a passing-question measurement may remain a dated observation
   without a maintained reproduction path when the plan says so.
4. Expected unchanged outputs, with any unexpected diff treated as a finding.
5. The actual file and a searchable passage as well as any line number for evidence or decisions.
6. Preconditions, exact verification commands, commit discipline and the integration sequence.

After substantial planning or investigation, prefer execution in a fresh worktree session.
Use same-session execution when the work is small and repeating discovery would cost more.

## Finished receipts and maintained documents

A finished dated review, remediation plan, completed plan, or execution record is a receipt.
Leave the finished base immutable while tracked. Each receipt has at most one live sibling,
`<stem>-update.md`; corrections, later measurements, later State and remediation dispositions
go there. Keep the update true while its base remains tracked: append later dated entries and
correct stale present-tense claims in place. Never create `<stem>-update-N.md`.

When creating the update, insert exactly one line directly below line 3 of the base:
`Updates and later status: [<stem>-update.md](<stem>-update.md).` That pointer, plus a mechanically
necessary joining of a prose paragraph beginning on line 3 without changing its text, is the
only post-completion edit to the base. Each update entry identifies the corrected passage by
that passage's own words, rather than only a finding number or line number.

The latest dated State declaration in the update is the effective State of its base; the update's
own State remains open while the base is tracked. A base and its optional one update form one
retirement family. A numbered sibling in Git history is historical evidence and does not
authorize another numbered sibling. Load `mam-repository-topology`, “Manual document retirement”,
for retirement references and Ben-authorized reclassification.

Present-state documents, instructions, README files, comments, docstrings and plans still being
executed stay true in place. Do not relabel a completed receipt as live to avoid these rules.

## MAM-basics and MAM-private State conventions

Write `State:` on line 3, directly under the H1. Non-review plans use `executed <date>`,
`paused <date>`, `live`, `runbook`, or `pointer`, with explanatory clauses when needed.
Sporadic intended work is live; paused identifies work stopped on a named day (Ben, 2026-08-29).
Whoever moves a phase updates its State in the same commit as the phase work. The delayed
phase record at `c0d9e21` prompted that requirement on 2026-08-27.

An update file uses `State: open` with its first-entry date; “first entry” and “first entries”
are the recorded forms (declared 2026-09-12). Its own State has no terminal form while its base
is tracked. Later base-State changes follow “Finished receipts and maintained documents”.

Review filenames, author and turn ownership, and review State exceptions are maintained only in
MAM-basics' `doc/dual-agent-review.md`, “Review filenames and State lines”. Private review scope
remains private. `py/repo_util/check_repo_standards.py` does not mechanically validate State
shapes or decide document retirement.

## Freeze the approved handoff

- Before execution, freeze an approval snapshot containing the current requirements, unresolved
  decisions, expected changed paths or artifacts, and agreed verification scope.
- For substantial work, return a standalone plan that a fresh executor can use by copy and
  paste. Do not leave Plan Mode merely to write a `.novc` plan.
- If Ben explicitly requests a persisted plan and Plan Mode prevents writes, return the complete
  plan for copying or use a separately authorized persistence-only action. Writing the plan does
  not authorize implementing it.

- Before declaring archival or handoff readiness, compare useful findings and decisions with
  the durable artifact. Close small obvious gaps under the common readiness rule.

## Execute with one writer

- Keep one writer for a checkout or artifact. Other tasks may investigate read-only. If
  concurrent writing is genuinely required, use separate verified worktrees.
- If new requirements materially change an approved plan during execution, pause implementation
  and reconcile the plan. Do not start a second writer.
- Stop on unexpected `HEAD` movement, unowned modifications, missing source material,
  contradictory requirements, or unexplained generated diffs.
- Respect the agreed verification scope. Do not add a full suite, mega pipeline, or other
  expensive validation merely because it exists.
- Bound long background work, give an estimate when evidence supports it, observe progress,
  and fail when a required measurement cannot be read.
- Defer Git checkout, branch, integration, and retirement mechanics to the applicable worktree
  instructions.

At completion, reconcile every ledger entry as `implemented`, `superseded`, `deferred`, or
`unresolved`.

The canonical copy of this shared skill is
`dot-claude/skills/iterative-document-editing/SKILL.md` in MAM-basics, and
`dot-claude/shared-skills.txt` declares its Codex destination. Never edit the live copies. Commit,
integrate, and push the canonical change to `main`, then deploy both live copies with
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config`
from the primary MAM-basics clone.
