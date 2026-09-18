# Updates to the plan to remediate the closed 2026-09-14 dual-agent review

State: open, first entry 2026-09-18. Every entry here corrects or supplements
`doc/PLAN-remediate-review-findings-2026-09-14.md`, whose substantive wording is left exactly as
written apart from the mechanically required paragraph join and update pointer.

Ben's decision, 2026-09-11: a finished dated document is left as written, like a pushed commit,
and a correction or later measurement goes in a sibling file named `<stem>-update.md`. This file
is that sibling. The paragraph join and update pointer are the only edits to the document this
file supplements; its substantive wording remains unchanged.

## 2026-09-18: corrections after the September 16 review

The plan's statement that `doc/user-level-config-in-cloud-sessions.md` was already corrected and
needed no further edit was false. The document still needed the three-resource opening and the
two stale two-resource passages corrected by the 2026-09-16 review remediation.

1. The plan's repository remediation reached `71f96ca3` on 2026-09-16. The later GitHub issue
   edit completed the plan's execution after that repository endpoint.
2. In section 1, the remediation task should read
   `C:/Users/BenDe/.agents/skills/codex-worktree-tasks/SKILL.md`, including
   `references/task-lifecycle.md` and `references/worktree-runtime.md`.
3. “39 headed entries” meant 38 level-2 entries plus one level-3 subheading, with 38
   `Recorded by` lines. The finding-10 entry and the subheading had none, while finding 11.5 had
   two.
4. The corrected anchors are `Correcting references before a tracked document is retired`,
   `The live rule in \`leningrad/page-snips/README.md\` therefore remains unchanged`, and
   `That reads \`MAM-simple/\`, so regenerate`.
5. The phrase “four actionable source gaps” was reused for a different set of four. The later
   heading should read `### 7.3 Remaining source corrections`.
6. Throughout the plan, “remediation task” names the task, “remediation task's root agent” names
   its root agent, and “the remediation task's final report” replaces the ambiguous
   self-reference.
7. No new author annotation is owed for the entries in
   `doc/review-findings-2026-09-10-update.md` that were rewritten beneath older `Recorded by`
   lines.
