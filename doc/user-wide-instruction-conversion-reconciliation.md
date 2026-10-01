# User-wide instruction conversion reconciliation

This maintained document maps the full user-level Claude instruction body before its compact
common-body conversion. Recorded by ChatGPT-Codex on 2026-09-28, New York time, under Ben's
approved September 26 remediation plan. It records section-level coverage, not a canonical
“214-rule” count. The approved restorations and deferred decisions are distinct.

The old Claude body is
[`dot-claude/user-wide-CLAUDE.md` at `71f96ca3801863f6fa64c1fd0e75ccfde773439b`](https://github.com/bdenckla/MAM-basics/blob/71f96ca3801863f6fa64c1fd0e75ccfde773439b/dot-claude/user-wide-CLAUDE.md).
The conversion is `d695966be8daea270f85424cb77d06f3b92a873d`; the approved remediation snapshot is
`1a92af88c82aecec0e637eddf23942c2c7c52377`, and its execution handoff is
`93fe8704a61cdc7fb7b60d2391a6f4e54ab73ed4`. “Shared body” below means
[`dot-Codex/user-wide-AGENTS.md`](../dot-Codex/user-wide-AGENTS.md). Shared skill paths are
canonical paths beneath `dot-claude/skills/`; the worktree skill is canonical under
`dot-Codex/skills/codex-worktree-tasks/`. Live copies are deployed destinations.

## Section-level coverage

The old Claude body has 35 level-2 headings and one level-3 heading. Every heading appears once
in this table. The approved restoration references identify September 26 review findings, whose
full wording and deferrals remain in the approved remediation plan.

| Old heading at `71f96ca3` | Current home or exact anchor | Disposition |
|---|---|---|
| Two axes of risk: does the change reach a product, and is the act hard to undo | Shared body: `Risk has two independent axes` | Retained; the unverified-result clause remains deferred (11.1). |
| Git & commits — commit at will; integrate worktrees at archival | Shared body: `Git and commits`; worktree skill: `references/task-lifecycle.md` | Retained and relocated; approved named-checkout and failed-fast-forward safeguards restored (11.2); long-lived-branch backup exception restored (11.5). Four legacy clauses remain deferred (11.1). |
| Verification cadence for multi-session work: cheap checks per commit, broad checks at risk and integration gates | Shared body: `Verification cadence for multi-session work` | Retained. |
| Delegate bounded work when it helps | Shared body: `Delegate bounded work when it helps` | Retained. |
| all-repos.code-workspace is the roster: clone only what it lists | Topology skill: `Sources of truth` | Relocated to the canonical topology skill. |
| Periodic repository maintenance also retires completed Codex task folders | Topology skill: `references/repository-maintenance.md`, `Completed Codex task folders`, `Completed linked worktrees`, and `Claude cache and temporary data` | Relocated to the canonical topology skill. |
| Never change an issue's state without a comment saying why | Shared body: `Load task-specific skills`; GitHub issue skill: `references/state-changes.md` | Retained as routing; detailed procedure relocated. |
| No GitHub issue for an idea, and no offer to file one | Shared body: `Load task-specific skills`; GitHub issue skill: `references/reading-and-writing.md`, `Filing an issue` | Retained and relocated. |
| Handing off to a task chip: be archivable BEFORE you spawn it | Shared body: `Claude Code only: task-chip handoffs`; worktree skill: `references/task-lifecycle.md`, `Prepare a successor last` | Retained and relocated; session-budget and genuinely-ending clauses remain deferred (11.1). |
| Prompt authorship: sign the chips you write, never assume I wrote the one you got | Shared body: `Task prompts and handoffs` | Retained. |
| A successor session verifies its exact checkout and commit before editing | Shared body: `Linked-worktree safeguards shared by Claude and Codex`; worktree skill: `references/task-lifecycle.md` | Retained and relocated; named-checkout and lost-edit/page-recovery safeguards restored (11.2). |
| A worktree runs the primary clone's venv, by absolute path | Shared body: `Linked-worktree safeguards shared by Claude and Codex`; worktree skill: `references/worktree-runtime.md` | Retained and relocated; different-dependency environment rule restored (11.2). |
| Running scripts — no inline one-liners | Shared body: `Shell, scripts, and file operations` | Retained; exact-command harness override remains deferred (11.1). |
| Prefer the built-in tools to shell, and a Python script to assembled shell | Shared body: `Shell, scripts, and file operations` | Retained. |
| Throwaway scripts: the lowest bar of software | Shared body: `Shell, scripts, and file operations`, passage `A throwaway scratch script` | Retained. |
| No `sys.path` surgery — one entry point per repo, subcommands under it | Shared body: `Python entry points and imports` | Retained. |
| Authored paths use forward slashes | Shared body: `Authored paths use forward slashes` | Retained. |
| Commands you hand *me* to run: PowerShell, one per block | Shared body: `Commands written for Ben` | Retained. |
| Plans are written for a FRESH session to execute | Shared body: `Plans and finished dated records` | Retained. |
| A finished dated document is corrected in `<stem>-update.md`, never edited | Shared body: `Plans and finished dated records`; editing skill: finished-record and retirement rules | Retained with permitted pointer/paragraph join; source-word citation rule restored (11.4). Retirement-family links follow findings 6 and 8. |
| Format Python with black | Shared body: `Format changed Python with Black` | Retained. |
| Template dispatch is closed — no defaults, guesses, or blind dives | Shared body: `Template dispatch is closed` | Retained. |
| Tests: differential and lint-shaped only | Shared body: `Tests are differential or lint-shaped` | Retained. |
| Prose: name the referent, don't leave me to reconstruct it | Shared body: `Prose names its subject` | Retained; report-end full-statement clause remains deferred (11.1). |
| Prose: if you announce a count, NUMBER the items — `1.`, `2.`, `3.` | Shared body: `Prose names its subject` | Retained; do-not-delete-the-count and bold-lead-ins clauses remain deferred (11.1). |
| Prose: a heading NAMES ITS SUBJECT — no cute or coy titles | Shared body: `Prose names its subject` | Retained. |
| Prose: a reported finding says what HAPPENED to it — "has been fixed", up front | Shared body: `Prose names its subject` | Retained. |
| Prose: the closing message opens with an H1 HEADING that names the report | Shared body: `Final messages begin with one H1 report heading` | Retained. |
| Unicode in source code — no orphan combining marks | Shared body: `Unicode in source and at runtime` | Retained. |
| Terminology: paseq vs. legarmeh (Hebrew accentuation) | Hebrew prose skill: `references/terminology.md`, `Paseq vs legarmeh` | Relocated. |
| Terminology: silluq vs. meteg (Hebrew accentuation) | Hebrew prose skill: `references/terminology.md`, `Meteg vs silluq; meteg not ga'ya` | Relocated; the three-module file-location pointer remains deferred (11.1). |
| Maqaf sits on the accents' own scale, at the bottom of it | Hebrew prose skill: `references/core-rules.md`, `Maqaf is the last rung of ONE scale` | Relocated. |
| A transcription is evidence about the transcription, never about the manuscript | Shared body: `A transcription is evidence about the transcription`; Hebrew prose skill: `references/sources-and-corpora.md`, `The corpora, and which one a claim takes` | General evidence rule restored (11.3); Hebrew-specific corpus guidance retained in the skill. |
| Unicode at runtime — UTF-8 stdio on Windows; prefer files for non-ASCII output | Shared body: `Unicode in source and at runtime` | Retained. |
| Showing me a local file: hand me a `file:///` link, don't open anything | Shared body: `Show local artifacts with file links`; Hebrew prose skill: `references/rendered-prose.md`, `Handing a page to Ben` | Retained and relocated. |
| If a task genuinely needs the pane's introspection (H3) | Shared body: `Show local artifacts with file links`, passage `genuinely needs live DOM` | Retained. |


## Twelve deferred legacy clauses

Every clause below remains deferred under finding 11.1. No clause has an “intentionally dropped”
disposition from Ben. The line locators refer to the pinned old Claude body; the source words are
the searchable anchors.

1. Lines 99–101, `report it as unverified rather than as working`: explicit reporting of an
   unverified code path.
2. Lines 142–144, `it wasn't quite ready when you asked, but now it is`: readiness-answer wording.
3. Lines 164–165, `default branch`: harness override for the default-branch instruction.
4. Lines 189–190, `suite`: optional second suite run during integration.
5. Lines 206–208, `thorny merge`: temporary worktree-branch backup during a difficult merge,
   followed by removal after integration.
6. Lines 378–381, `<total_tokens>`: session budget rather than a gauge of context consumed.
7. Lines 456–459, `genuinely ends`: ending unfinished work without a successor.
8. Lines 595–601, `Expect the harness to prescribe exactly what these bullets ban`: override
   harness instructions that recommend banned script forms.
9. Lines 1079–1081, `repeat that statement, or refer to it in its own words`: full explanation
   in the final report.
10. Lines 1109–1113, `Bold lead-ins`: bold lead-ins do not replace a subject-naming heading.
11. Lines 1118–1120, `count`: preserving an announced count rather than deleting it.
12. Lines 1342–1345, `py/foi/`: the location of three meteg data modules.

## The instruction budget changed later

The earlier 131,072-byte budget was reversed by
`51a4120c5d08218798e023ba14b8d3dec34e2e8a` on September 15, which restored the 32,768-byte default.
The symmetric-instructions plan's update records this later result. This reconciliation changes
no configuration and does not execute or retire the separate September 9 instruction-pruning
plan.

## Reproduce the old heading inventory

Run this read-only command from any PowerShell 7 working directory, with `<clone>` replaced by the
absolute path, in forward slashes, of any full MAM-basics clone. It reads only that repository at
the pinned commit; it does not require the obsolete full live Claude body.

```powershell
(git -c safe.directory=<clone> -C <clone> show 71f96ca3801863f6fa64c1fd0e75ccfde773439b:dot-claude/user-wide-CLAUDE.md).Where({ $_ -match '^#{2,3} ' })
```
