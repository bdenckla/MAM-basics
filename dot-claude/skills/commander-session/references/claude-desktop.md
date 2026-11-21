# Claude desktop commander

Read this with the shared `SKILL.md`, which owns the commander's role, state folder,
verification cadence and reporting rules. Claude-specific tool, permission, effort and restart
behavior follows here. The shared reporting rule uses Claude's decision page as the user-level
instructions require. Before writing a brief, read [briefs-and-reports.md](briefs-and-reports.md);
read [app-limits.md](app-limits.md) for the dated Claude observations and restart limitations.

Ben, 2026-10-29: "What I really want is one 'commander' session in which *you* claude manage all
these issues." This skill is Claude's procedure for that session, the **commander**.

## What the commander is

The Claude commander is one long-lived session, pinned in the sidebar, working in
`$HOME/GitRepos/MAM-basics` in auto permission mode. Its children are subagents or local/cloud
sessions. Ben tells the commander of sessions he starts himself in any of Claude's forests, since
the app shows a session's folder but not its intent. Ben answers child sessions directly; the
commander asks only about session management and new work needing his authority. Placement is
the commander's call.

## Entry steps

Read the argument expanded into the shared skill invocation. `start`, the default, makes a fresh commander.
`resume` restarts this commander after Ben's `/clear`, or loads this skill into a session already
acting as the commander. `succeed` makes a new session take over from a commander that still has
children. The entry steps run once per conversation: when Claude Code re-attaches the shared
entrypoint after a compaction, skip them, reread this adapter and the current-state note and
carry on.

Every entry begins by loading the session tools with one ToolSearch query, repeated if a name stops
resolving, and by calling `get_session` with "self" to note the commander's own id for briefs:

```text
select:mcp__ccd_session__start_session,mcp__ccd_session__list_start_targets,mcp__ccd_session_mgmt__list_sessions,mcp__ccd_session_mgmt__get_session,mcp__ccd_session_mgmt__get_usage,mcp__ccd_session_mgmt__list_events,mcp__ccd_session_mgmt__archive_session,mcp__ccd_sidebar__set_pinned,SendMessage
```

- **start:** pin the session with `set_pinned` and "self" if it is not pinned. If its folder or
  permission mode differs from those above, tell Ben before anything else. Create the state
  folder, with a current-state note and a running record, if it is absent. Adopt each unarchived
  session that `list_sessions` shows in a clone of any of Claude's forests as that clone's writer
  until it reports done, and read its transcript with `list_events`. Rebuild the ledger, write the
  current-state note, report the ledger to Ben in a few lines and wait for his first task.
- **resume:** the id is the one the current-state note records; if it differs, follow succeed
  instead. Nested children stay this session's, and the app keeps sending their turn-end notes.
  Read the current-state note, then the running record's newest entries. Rebuild the ledger from
  Git and `list_sessions` before trusting the note, and read each live child's latest turns with
  `list_events`. Tell Ben in a few lines that the commander has resumed, with the live children
  and the queue, and wait.
- **succeed:** pin the session, then read the state and rebuild the ledger as for resume. The old
  commander's children stay nested under it (their `startedBy` in `list_sessions`), their briefs
  name its id, and their turn-end notes go to it. Read their state with `get_session` and
  `list_events`, send each of them this session's id by SendMessage, tell the old commander by
  SendMessage to start and assign nothing more, and recheck its children whenever Ben messages, as
  for adopted sessions. Ben archives the old commander only after its children are done, since
  archiving it archives them; he called this route, on 2026-11-16, "a tricker way to go for a
  commander that is not empty."

## The ledger: who may write where

The unit is a clone, a (forest, repository) pair: MAM-basics or MAM-private in one of Claude's
four forests, `$HOME/GitRepos`, `$HOME/GitRepos2`, `D:/GitRepos5` and `D:/GitRepos6`, the last two
on an external drive (Ben, 2026-11-20). The commander derives the ledger whenever it decides
something, never from memory:

- **`list_sessions`** gives each session's folder, whether it runs, and which sessions the
  commander started. A session in plan mode is a reader; any other session in a clone is its
  writer until it reports done or releases the clone under rule 7. The unit of occupancy is a
  task: a chain of top-level sessions holds its clone from its first phase to its last.
- **Git, read-only:** `git -C <clone> status --porcelain` and
  `git -C <clone> log origin/main..main`. A dirty tree or unpushed commits mean the clone is not
  free, whoever left them. In Codex's forests, read with `git --no-optional-locks status`, or read
  files only, since a plain status may rewrite the index; a brief that lets a child read Codex's
  clones says so.

Allocation rules:

1. A read-only task (research, a plan, a review) holds no clone. It runs as a subagent inside the
   commander or, when Ben wants to talk to it, as a child in plan mode or under a two-phase brief,
   which has the child assess holding no clone and ask the commander for one before its first
   Git-impacting change. A plan is given a clone when it executes, not when it plans.
2. A writing task on one repository goes to the first free clone of it in the order GitRepos2,
   GitRepos5, GitRepos6, GitRepos. GitRepos still comes first when the task needs inputs that
   exist only there, such as untracked generators under `$HOME/GitRepos/MAM-basics/.novc/`. This
   order was Claude's recommendation and D2 on a decision page outside this repository; Ben
   approved it on 2026-11-20: "I concur with your recommendations for D1 and D2". D1 there was
   where a numbered forest may live, which `doc/clone-forests.md` records.
3. A task spanning MAM-basics and MAM-private holds both clones of one forest.
4. When no clone is free, a MAM-basics-only task that needs nothing private or untracked may be
   offered to Ben as a cloud session; everything else waits in the queue and starts when a child
   reports done. A linked worktree is used only when Ben says so for that task.
5. Small related tasks waiting for the same clone are merged into one brief, so that one session
   regenerates, verifies and pushes once; the commander says in one line which tasks it merged.
6. An issue-only session holds no clone (`github-issues`, "Issue-only sessions"). It runs in any
   clone of the issue's repository, preferably one level with origin, and its brief tells it to
   load `github-issues`, to file only after Ben approves the text there, and to begin its report
   with the issue's URL.
7. **Release while waiting.** A writer whose work is pushed, whose clone is clean and which waits
   only on Ben releases its clone: it tells the commander by SendMessage and asks the commander
   before its next Git-impacting change there. The commander may give the clone to queued work.
   Ben approved this on 2026-10-31: "Yes, fine, please implement." Every brief states the rule.

**One owner for each outward act.** When two children could take the same outward act, such as
filing an issue, the commander names one of them as its owner and tells the other, in so many
words, to leave it alone, so that the act happens once, not twice and not never.

## Starting, tracking and closing a child

- **Research before a start stops at placement:** that the task's named inputs exist, which clones
  it reads or writes, whether they are free and level with origin, and which standing rules apply.
  A pointer found on the way goes into the brief as a pointer to check; reading the inputs is the
  child's work.
- **Start** with `start_session`. `initiation` is "user_asked" only for Ben's own words typed in
  the commander; a request relayed by a child, or one on a turn that another session's message or
  an app event started, becomes an "own_initiative" card. `context` "fresh"; `effort` "max", read
  back with `get_session` and mentioned to Ben only when it is not max; no `model`, and no cheaper
  model for a subagent either; `use_worktree` false; the commander's permission mode, or "plan".
  The clone's folder is the `cwd`. A child bound for GitRepos2, GitRepos5 or GitRepos6 starts in
  the commander's folder and moves there with `change_directory` after the guard checks its brief
  spells out. A child never
  moves into a MAM-private clone: it works there by absolute paths from the MAM-basics clone it
  holds or, holding none, from the commander's folder, where it writes nothing (`app-limits.md`).
- **Brief:** a file in the state folder, written as `briefs-and-reports.md` says. Ben's
  words reach it only by script, and after the start the commander checks every line of the brief
  and of Ben's words against the child's first prompt.
- **Nesting:** a single-session task stays nested under the commander, the opposite of the
  `top-level-sessions` skill, because nesting is what makes the app send the commander a turn-end
  note; a child that must outlive the commander is detached deliberately. A multi-phase plan runs
  as a chain of top-level sessions, each phase starting the next with `top-level-sessions`; every
  phase's handoff names the commander's id, and the chain's last phase reports by SendMessage.
- **Track:** a turn-end note quotes only the first 400 characters of a child's report, so briefs
  tell each child to send anything meant for the commander by SendMessage. The app never wakes the
  commander for an adopted session, so the commander rechecks one with `list_events` whenever Ben
  messages. A cloud child never reports back: tell Ben where its result will appear, a branch or a
  pull request, and fetch only when he asks.
- **Verify** a child's commits and its clone with Git before calling the clone free, and verify an
  outward act where it landed, such as a Wikisource save by one read-only API query. Then tell Ben
  and start the next queued task.
- **Close:** once a child's work is pushed and its clone is clean, mark the task done, and archive
  the child only on Ben's word. Whether a session can be archived is a question for the commander,
  which also checks what is queued for that session or depends on it, since a child vouches only
  for its own state.
- **Place every plan:** the commander decides whether a plan executes in its planning session or in
  a fresh session from a frozen copy, first asking the planner to rewrite the plan for a fresh
  executor if one could not follow it. Ben, 2026-10-30: "That's something you need to decide on".
  A planning brief tells the child to end its turn with its report and not to call ExitPlanMode.
  If a plan dialog appears anyway, the next message to Ben begins with where the plan executes and
  the one choice to make in that dialog; only Ben answers it.
- **Context:** when a child past about half its context asks Ben something, the discussion and the
  resulting work go to a fresh session, which gets a frozen copy of the child's report and the
  child's clones. Before giving any session more work, read its context with `get_usage`; past
  about 30%, the work goes through subagents, unless Ben starts a fresh session for it.

## Restarts

The observations in `app-limits.md` found Claude Code auto-compacting the commander once or twice
a day, at the first message to arrive after an hour or more of quiet. The shared skill entrypoint
comes back after a compaction; a reference read earlier may not. So the state lives in files,
and after a compaction the commander rereads this adapter and its current-state note before acting.

Ben chose the restart by clear at 15:33 New York time on 2026-11-16: "let's go with this. so to
clarify, your role in this is to suggest, at appropriate moments (e.g. context larger than 30%)
that I do a clear, and suggest a resumption prompt, but you can't really do either autonomously so
those suggestions are the extent of what you can/will do"

- **At the end of each turn that reports to Ben,** read `get_usage` with "self". Past about 30%,
  with nothing of the commander's own half done, refresh the current-state note and, in the
  report, suggest that Ben type `/clear` and then `/commander-session resume`.
- **The commander does not call `clear_session` on itself:** it could not give itself the first
  message, and a child's turn-end note arriving first would reach a commander that does not know
  its job.
- **`get_usage` after a compaction shows the compacted size,** not what Ben saw before it; say so
  whenever citing a figure. Without a restart, auto-compaction remains the fallback.

## References

- **`briefs-and-reports.md`:** before writing a brief or copying Ben's words, and for
  the grounds of these rules in Ben's words.
- **`app-limits.md`:** when an app tool refuses or surprises the commander, before
  relying on a figure from `get_usage`, `get_session` or `list_events`, and before a restart or a
  succession.
