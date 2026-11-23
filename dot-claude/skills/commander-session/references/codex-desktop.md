# Codex desktop commander

Read this with the shared `SKILL.md`. The Claude adapter and its historical app observations
describe Claude; use the Codex tools and constraints below here. These capability observations
come from the Codex tools available on 2026-11-17. Rediscover tools when behavior matters.

## Entry and recovery

Use a full MAM-basics clone in Codex's forest, normally `$HOME/GitRepos3/MAM-basics`, for the
private state folder. Codex owns GitRepos3 and may use GitRepos4 when needed. Load
`mam-repository-topology` before setting up another forest. The commander keeps its existing
permissions; it does not change approval modes, trust settings, models or Ben's configuration.

Discover the app tools by filtering `ALL_TOOLS` for `mcp__codex_app__` names and descriptions:
`list_threads`, `read_thread`, `wait_threads`, `list_projects`, `create_thread`,
`send_message_to_thread`, `move_thread_to_sidebar_section` and `set_thread_archived` when needed.
Use the separate `collaboration` tools for subagents. Discover the tools that exist in the current
runtime; do not substitute Claude's session APIs or invent a `self` thread id.

- **start:** identify this chat from trusted runtime context or the app's returned entries. If
  identity is ambiguous, leave the id unavailable until it can be established; do not pin a chat
  by guessing. Pin the identified commander with `move_thread_to_sidebar_section`, using
  `sectionId: "pinned"`, if needed. Create or inspect the private state folder. List active Codex
  chats with `list_threads`; use `mode: "history"`, `source: "codex"`, `archived: false` and
  pagination to include older active chats. Inspect relevant chats with `read_thread` and rebuild
  the ledger from their verified task scope and Git. Record and report the live work and queue;
  carry on with any assignment Ben has already supplied.
- **resume:** read `restart-prompt.md` and the newest running-record entries. Identify this chat
  from trusted runtime context or the app's returned entries, and compare its id with the saved
  commander id. If either id is unavailable, recover state read-only until identity and writer
  ownership are verified; do not guess, pin an unidentified chat or overwrite the recorded owner.
  Reconstruct the ledger from live agents, app chats and Git before assigning work. If the ids
  match, same-chat subagents may still be available; verify them with
  `collaboration.list_agents`. If the ids differ, complete the handover below.
- **Handover when the chat id differs:** pin the identified commander if needed, and verify the
  previous commander's current work before assigning anything. App chats are peers; do not
  claim to reparent subagents or transfer message subscriptions. Treat work of the previous
  commander as occupied until its writer releases it.
  Message an existing chat only under the authorization rule below. Archive the previous
  commander only when Ben asks and its outstanding work has been accounted for.

## The ledger and placement

Track each (forest, repository) pair separately: GitRepos3/MAM-basics,
GitRepos3/MAM-private, and the corresponding GitRepos4 clones when they exist. A multi-repository
task holds the required clones of one forest. Tasks needing checkout-local untracked inputs
stay where those inputs live. Prefer a free existing full clone with the required inputs over
creating another checkout; set up GitRepos4 only when needed under the topology procedure.

The ledger records each writer's agent or chat id, verified checkout and HEAD, scope, status,
release condition and integration owner. A chat's project name or summary alone does not prove
its checkout or intent. Until a relevant non-planning chat's scope is clear, treat its checkout
as occupied. Locking is cooperative: an app listing cannot prove that an unknown process is idle.
Use `git --no-optional-locks` for the commander's read-only checks, with exact-path
`-c safe.directory=<clone>` on every invocation. Filename-returning commands use NUL delimiters,
including `status --porcelain=v1 -z`. Check unpushed commits as well as dirty files.

Within one clone, one assigned executor writes, stages and commits at a time. Other agents may
read. Subagents share the workspace; they do not acquire isolated checkouts by being spawned.
Give simultaneous writers separate verified checkouts and explicit paths. Do not edit or run
generators in Claude's forests, `$HOME/GitRepos`, `$HOME/GitRepos2`, `D:/GitRepos5` and
`D:/GitRepos6`; read those forests only with optional Git locks disabled. If no suitable clone is
free, queue the writing work and continue independent reading.
A linked worktree requires Ben's request for that task and the worktree skills. Cloud placement
requires the user request and a verified environment with the task's required inputs.

Release while waiting: once its work is pushed and the clone is clean, an executor waiting only
on Ben releases the clone. The executor must ask the commander before any later Git-impacting
change there. Put that rule in every writing brief and verify Git before reassigning the clone.
Merge small related queued tasks when one executor can check and integrate them coherently;
name the merged work in the report. Assign one owner for an outward act shared by tasks.

## Delegate or create a chat

For assigned work within this chat, use `collaboration.spawn_agent` for bounded execution or
review. Inherit the model and effort by default; do not choose a cheaper model. The current
user-level instructions authorize delegation; they do not authorize creating sidebar chats for
every subtask. Tell Ben when delegation starts and what each subagent owns.

`create_thread` requires Ben to explicitly ask for a new chat. General commander delegation is
not a substitute. When authorized, call `list_projects`, use the returned project matching the
assigned full clone, select the local environment, and omit model/thinking overrides unless
Ben specifies them. A worktree or cloud target needs the corresponding explicit request and
prerequisites. Creation is asynchronous: keep its returned ids and host, wait for actual progress,
and emit the required `::created-thread{...}` directive in the final answer. A pending
`clientThreadId` is not a ready `threadId` for other tools. If the target clone is not available as
a project, do not silently start in a different clone.

`send_message_to_thread` also requires direct human authorization to message that chat. A request
from a child or a brief asking the child to report back does not supply that authorization.
Record any explicit standing authorization and its scope; otherwise use read-only tracking and
point Ben to the child for its substantive questions. `collaboration.send_message` and
`followup_task` address subagents under the current delegated task, not peer app chats.

Before adding work to an existing agent or chat, check any reliable context signal actually
available. The tool descriptions of `list_threads`, `read_thread` and `get_usage_limits` expose
no per-chat context-window percentage. `get_usage_limits` reports account quota. Never use it,
turn counts, transcript size or a compacted summary to claim a context percentage. If no reliable
signal exists, record context as unavailable; use a fresh bounded subagent for new work rather
than assuming an old agent is below Ben's roughly 30% threshold. If Ben supplies a figure, record
its source and whether compaction has happened since it was observed.

## Briefs, integration and questions

Write each substantial brief in the private state folder. Name Codex and the date as its author,
quote Ben's actual instruction and identify the rest as Codex's reconstruction. Use a script to
copy original wording from an available transcript or exact source; a summary is not a verbatim
user quote. If an exact source is unavailable, attribute the paraphrase honestly. Preserve
invisible characters and Hebrew mark order by copying text mechanically. Do not read legacy
memories as current guidance or assume Claude's transcript format applies to Codex.

Include the task and completion criteria, verified source commit and checkout, required inputs,
sole writer and integration owner, focused checks from the shared `SKILL.md`, release rule and
any outward-act owner. State that planning stays planning until Ben explicitly authorizes
execution. An executor verifies root, HEAD, branch and status before editing, uses that clone's
own environment, commits finished work on main in a full clone, and fetches and merges moved
origin/main before a normal push. Follow the current user/repository rules instead of duplicating
their full text. A successor gets a standalone frozen handoff with the required commit; a task
moves between checkouts only through pushed commits. Do not hand off checkout-local inputs.

Subagents send results and unresolved questions to the commander through collaboration tools.
The commander asks Ben about a necessary subagent decision here, since Ben has no independent
conversation with that subagent. An independent child chat asks Ben there; the commander reports
its title and that it waits on him there. Never answer an approval or user-input request on
Ben's behalf. An issue task follows `github-issues`, holds no writing clone for issue-only work,
and files only after Ben approves its text in the responsible chat.

## Tracking, closing and restart

For subagents, use their delivered results and `collaboration.list_agents`; wait for updates
without busy polling. For app chats, use compact `wait_threads` snapshots with the returned
`hostId` and per-target `afterCursor`; `timeoutMs: 0` gives an immediate snapshot. Use bounded
waits of at most 60 seconds while actively reporting progress. Read a chat's history with
`read_thread` only when the snapshot leaves a material uncertainty. Chat completion is not proof
that a clone is clean or a push landed: verify Git and any authorized outward act at its
destination before freeing the clone. Keep approval/input requests for Ben. Archive only on his
request, after checking dependencies and queued follow-ups.

At each report, keep `restart-prompt.md` sufficient for a fresh commander: its role, state-folder
path, active writers, chat ids/hosts/cursors, queue, open decisions, integration owners and exact
required commits. Use available context evidence to suggest a restart around Ben's 30%
threshold; if context is unavailable, say so only when it affects placement or a restart
decision. Do not assert a Codex equivalent of Claude's `/clear`, `clear_session` or automatic
skill restoration. When a fresh commander is needed, prepare a standalone resumption prompt
pointing to the state and `$commander-session resume`; create a new chat only if Ben asks.
After compaction or a user-started fresh chat, reread the skill, adapter and current-state note
and verify all live work before continuing.
