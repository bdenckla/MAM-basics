# Updates to the plan to remediate the closed 2026-09-14 dual-agent review

State: open, first entry 2026-09-18. Every entry here corrects or supplements
`doc/PLAN-remediate-review-findings-2026-09-14.md`, whose substantive wording is left exactly as
written apart from the mechanically required paragraph join and update pointer.

Ben's decision, 2026-09-11: a finished dated document is left as written, like a pushed commit,
and a correction or later measurement goes in a sibling file named `<stem>-update.md`. This file
is that sibling. The paragraph join and update pointer are the only edits to the document this
file supplements; its substantive wording remains unchanged.

## 2026-09-18: corrections after the September 16 review

The plan's sentence “`doc/user-level-config-in-cloud-sessions.md` is already corrected and needs
no further edit” was false. The document still needed the three-resource opening and the
two stale two-resource passages corrected by the 2026-09-16 review remediation.

1. The declaration beginning “State: live; written 2026-09-16” is superseded. The plan's
   effective State is **executed 2026-09-16**: repository remediation reached `71f96ca3`,
   followed on September 16 by the issue 278 body correction and comment. This update remains
   **State: open** while the base is tracked.
2. The reading passage beginning “Before editing, read the live user and repository
   instructions and load these skills in this order” omitted the cross-agent skill location.
   The remediation task should read
   `C:/Users/BenDe/.agents/skills/codex-worktree-tasks/SKILL.md`, including
   `references/task-lifecycle.md` and `references/worktree-runtime.md`.
3. The table label “39 headed entries” meant 38 level-2 entries plus one level-3 subheading,
   with 38 `Recorded by` lines. Finding 10 lacked an attribution line; finding 11.5 had two,
   including the attribution beneath its level-3 subheading.
4. Replace the anchor `Retiring a finished document` with
   `Correcting references before a tracked document is retired`; replace the original words
   `the live rule in leningrad/page-snips/README.md remains unchanged` with the searchable
   anchor ``The live rule in `leningrad/page-snips/README.md` therefore remains unchanged``;
   and replace the original words `That reads MAM-simple` with the searchable anchor
   ``That reads `MAM-simple/`, so regenerate``.
5. The phrase “four actionable source gaps” was reused for a different set of four. The later
   heading should read `### 7.3 Remaining source corrections`.
6. The completion passage “The executing task's final report names:” has an ambiguous
   self-reference. Throughout the plan, “remediation task” names the task, “remediation task's
   root agent” names its root agent, and “the remediation task's final report” names its report.
7. No new author annotation is owed for the entries in
   `doc/review-findings-2026-09-10-update.md` that were rewritten beneath older `Recorded by`
   lines.

## 2026-09-27: counter-finding C2 implementation status

Counter-finding C2's repository work was implemented through
`doc/PLAN-retire-google-sheet.md`: the independent 36-page special-page mirror and its
identity checks now belong to every `fr-wikisource` run, and the Google download,
parse, comparison, and auto-edit pipeline has been removed. The overall retirement
remains incomplete until Ben applies and reports the manual frozen-Sheet and Hebrew
Wikisource documentation edits and both live results are verified as that plan requires.
