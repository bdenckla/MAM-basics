---
name: iterative-document-editing
description: Ben's workflow for planning and carrying out multi-turn or multi-session edits to prose, Markdown, generated pages, reports, plans, and other evolving documents. Use when requirements may change across messages, several tasks may inspect the same material, or an approved plan will be handed to a fresh executor. Do not use for a one-turn typo or mechanical formatting correction.
---

# Iterative Document Editing

Keep planning, approval, execution, and handoff explicit while a document's requirements evolve.

## Keep planning read-only

- A planning task remains read-only until Ben explicitly authorizes execution. Leaving Plan Mode
  or entering Default Mode is not execution authorization.
- Treat later suggestions in a planning task as revisions to the plan unless Ben explicitly says
  to implement them.
- Reconcile every visible user message, annotation, and supplied input before declaring the
  specification or plan complete.

## Maintain cumulative state

- Keep one compact cumulative revision ledger. Mark each requirement `active`, `superseded`,
  `implemented`, `deferred`, or `unresolved`.
- When several images, citations, links, or other source materials are involved, maintain an
  input manifest with each item's identity, provenance where relevant, requested use, and
  disposition. Never infer identity from a filename or timestamp. An unresolved in-scope item
  blocks execution.

## Freeze the approved handoff

- Before execution, freeze an approval snapshot containing the current requirements, unresolved
  decisions, expected changed paths or artifacts, and agreed verification scope.
- For substantial work, return a standalone plan that a fresh executor can use by copy and
  paste. Do not leave Plan Mode merely to write a `.novc` plan.
- If Ben explicitly requests a persisted plan and Plan Mode prevents writes, return the complete
  plan for copying or use a separately authorized persistence-only action. Writing the plan does
  not authorize implementing it.

## Execute with one writer

- Keep one writer for a checkout or artifact. Other tasks may investigate read-only. If
  concurrent writing is genuinely required, use separate verified worktrees.
- If new requirements materially change an approved plan during execution, pause implementation
  and reconcile the plan. Do not start a second writer.
- Stop on unexpected `HEAD` movement, unowned modifications, missing source material,
  contradictory requirements, or unexplained generated diffs.
- Respect the agreed verification scope. Do not add a full suite, mega pipeline, or other
  expensive validation merely because it exists.
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
