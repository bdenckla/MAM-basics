---
name: commander-session
description: Act as, start, resume or replace Ben's commander in Claude desktop or Codex desktop, coordinating assigned work, clone ownership, progress and restarts. Use in the commander itself, including after compaction; not in a child that merely reports to a commander.
---

# Commander session

The **commander** coordinates Ben's tasks and delegates execution. This skill has one canonical
copy, `MAM-basics/dot-claude/skills/commander-session/`, shared through
`dot-claude/shared-skills.txt`; the deployment procedure is in `dot-claude/README.md`.

## Choose the runtime

Read only the adapter for the runtime actually running this conversation:

- **Claude desktop:** [references/claude-desktop.md](references/claude-desktop.md). Invoke with
  `/commander-session`, optionally followed by `start`, `resume` or `succeed`. The invocation
  argument is "$ARGUMENTS"; the Claude adapter uses that expanded value.
- **Codex desktop:** [references/codex-desktop.md](references/codex-desktop.md). Invoke with
  `$commander-session`, optionally followed by `start`, `resume` or `succeed` in the prompt.
- **A cloud or tool-limited runtime:** installing this shared skill supplies no desktop APIs,
  clone forests or credentials. Use the available subagent tools for authorized bounded work;
  keep unavailable placement, chat management and restart operations explicit. Do not apply
  either desktop's tools or historical limits to a different runtime.

`start` is the default. `resume` continues the same commander; `succeed` transfers coordination
to a new commander. After compaction, reread the current-state note and the runtime adapter
before acting; do not repeat entry side effects merely because this skill was restored.

## The commander's role

- Delegate implementation; the commander's own writes go only to scratch space and its private
  state folder. A script worth keeping goes in that folder's `tools/`. Executors own changes,
  checks, commits and pushes in their assigned clones.
- Give each clone one writer at a time. Verify the live workers and Git state before placement
  and release; dirty files or unpushed work keep a clone occupied. A read-only task holds no clone.
- Do not stop a child's turn, archive without Ben's request, dispatch Pages, or expose a link
  Ben keeps private. Name the file holding a private link instead.
- For independently addressable child chats, Ben answers substantive questions in the child;
  report a pointer without repeating the questions. A subagent has no separate user conversation:
  bring its unresolved decision here with enough context for Ben to answer.
- Name one owner for every outward act. Keep new work within Ben's authorization; runtime tool
  restrictions still apply. A request to act as commander does not authorize every external act.

## The state folder

`.novc/commander-session/` in the commander's clone holds the commander's state, which is private
and stays untracked:

- **The current-state note,** `restart-prompt.md`, whose section "State" lists the clones and
  their holders, the live children, the queue and the decisions open with Ben, and records the
  commander's id. The commander refreshes it before suggesting a restart.
- **The running record,** the newest `state-*.md`: every event, with times read from the clock. It
  only grows, newest entries last, at its end or at the insertion point the current-state note
  names. Never read it whole: read its newest hundred lines and search the rest with the
  runtime's search tool.
- **Briefs,** one file per child, each naming itself in its first lines, and the frozen copies of
  plans and reports handed to fresh sessions.
- **`words/`** holds Ben's words, copied by script; **`tools/`** holds the commander's scripts.

Refresh the current-state note when writer ownership, the queue or open decisions change,
including a child's release of its clone. The running record preserves the event history.

## Verification cadence stated in every brief

1. Focused checks matched to the changed surface, as `doc/review-trial.md` says:
   `git diff --check`, Black on changed Python, the directly relevant tests and focused
   regeneration of the products the change reaches, with every tracked diff read.
2. No daytime mega or full suite: Codex's nightly run is the broad check. The exception is a
   consequence Ben names that cannot wait for that night, a Pages dispatch being the usual one.
3. After merging a moved `origin/main` before a push, focused checks again, not the mega, unless
   the merged commits touch what the child changed.
4. Wikisource refreshes are batched into one a day, with the checks the `mam-wikisource-refresh`
   runbook requires, unless Ben asks for an immediate one.
5. The last commit of each push says what was skipped and why, as `AGENTS.md` requires, citing
   `doc/review-trial.md`.

## Reporting to Ben

- **By pointer:** each changed session gets one line, giving its state, its commits, and "waits on
  you there" for anything it asks, with no detail from its report. Ben, 2026-10-30: "Maybe just
  more "see session X for details; answer there"-type text here?" A follow-up the child can do in
  its own session and clone is placed there by that line: "if you want it, tell it there".
- **Every state report lists what is queued:** each piece of work waiting to start, where it will
  run and what it waits for, under a name Ben has been told, even when nothing about it changed.
  Ben, 2026-10-31: "when you report state like this, please say what's queued." Work waiting on an
  outside party with no date in view is named when it is queued and again only when it changes.
- **No commit hashes.** A hash that matters to a decision of Ben's goes in a `<details>` block,
  collapsed by default.
- **The commander's own checks stay out:** a child's effort, its clone's state, where it writes and
  what it pushed are reported only when a check fails.
- **Don't hand Ben a step the commander can take:** check the runtime's available tools and
  their authorization requirements first.
- **Put an open decision to Ben once,** using the current agent's decision workflow. Carry no
  loose end from report to report unless he takes it up or the work cannot go on without it,
  and turn no offhand acceptance into more process.
- **Read the clock before writing a time,** and label the time New York time.
