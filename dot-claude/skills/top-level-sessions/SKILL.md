---
name: top-level-sessions
description: Start a Claude Code session that is top-level rather than nested under this session, when Ben asks to start, spawn or launch a session, a fresh session, a peer session, or a top-level or non-child session, including one to execute a plan; also move a session this one started, or this session itself, to top level. Claude desktop app only.
when_to_use: Use whenever Ben asks for work to run in another session. Subagents, which the Agent tool runs inside this session, need no skill.
---

# Top-level sessions

The Claude desktop app can always give Ben a top-level session. `start_session` starts a new
session nested under this session, and `detach_session` then moves the new session to top
level. Do both without first telling Ben that you may be unable to. A nested session is archived
with the session that started it, so Ben could not archive this session without losing the new
one.

## Load the tools in one search

The session tools are deferred. Load all five with one ToolSearch query:

```text
select:mcp__ccd_session__start_session,mcp__ccd_session_mgmt__detach_session,mcp__ccd_session_mgmt__get_session,mcp__ccd_session__list_start_targets,mcp__ccd_session_mgmt__set_session_permission_mode
```

If a name no longer resolves, search for "start session" and "detach" before concluding that the
app lacks the tool, and then name the missing tool to Ben.

## Prepare the start

- **Initiation:** Ben's request is an instruction to start the session now. Pass
  `initiation: "user_asked"`, never an `"offer"` card.
- **Context:** pass `context: "fresh"` with a `background` of at least 80 characters, unless Ben
  asks for this conversation to carry over.
- **Checkout:** by default the new session works in this session's full clone, with
  `use_worktree: false`, and this session stops writing there. Pass another folder as `cwd`,
  spelled as `list_start_targets` reports it, when Ben names that folder or when this session
  must keep writing here; the common body's “Clone forests and portable work” chooses the forest.
  From a worktree session, give the new session its own checkout: the app refuses to detach a
  session that shares another session's worktree. Check the target checkout's branch, `HEAD` and
  status before starting.
- **Brief:** follow the common body's “Task prompts and handoffs”: the agent and date, Ben's
  instruction quoted, the rest marked as reconstruction, the checkout, the required commit and the
  integration owner. The new session owns its own commits and pushes, because this session stops
  hearing about its turns once it is detached. Put bulky evidence in a gitignored folder with a
  `README.md` and give the folder's absolute path.
- **Permission mode:** the new session starts at or below this session's mode, in the order plan,
  default, acceptEdits, auto, bypassPermissions. Pass `permission_mode: "plan"` for planning or
  research that Ben has not told it to execute. If this session is in plan mode and the new
  session must execute, start the new session in plan mode and raise it with
  `set_session_permission_mode`, which shows Ben an approval card.

## Start, detach and verify

1. Call `start_session`.
2. Call `detach_session` at once with the session id that `start_session` returned.
3. Call `get_session` on that id and confirm `detached: true` and the expected `cwd`.

If the detach is refused, quote the refusal and tell Ben that the sidebar's “Detach to top level”
does the same. When Ben asks to move this session itself to top level, pass `"self"` to
`detach_session`; that works only when another session's Claude started this one.

## Report

Link the new session as `[its title](#local_<id>)`. Say where it works, at which commit, what its
brief quotes and what it owns. Say that its reports will appear only in that session, and whether
this session can now be archived without affecting it.
