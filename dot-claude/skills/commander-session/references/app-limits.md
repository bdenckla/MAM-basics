# Limits of what the app gives

What the Claude desktop app and Claude Code gave the commander, and failed to give it, as observed
from 2026-10-29 to 2026-11-18. A later release may differ: before relying on a limit that matters,
check it again. Ben's words are quoted exactly as the commander's records give them; everything
else records Claude's observations. Codex's 2026-11-17 port updates file references and explains
recovery through the new shared entrypoint and Claude adapter.

## Sessions and tools

- **Locking is cooperative.** Nothing stops a session that Ben starts by hand from writing in a
  clone the commander assigned; the commander can only see that the session exists.
- **The session tools are deferred** and easy to fumble. `claude-desktop.md` gives the one ToolSearch query
  that loads them. If a name no longer resolves, search for it by keyword before concluding that
  the app lacks the tool, and then name the missing tool to Ben.
- **Where a child starts:** the app's guidance for `start_session`'s `cwd` assumes that Ben named
  the place. His standing delegation of Claude's clones, first given when the commander was
  started on 2026-10-29, extended to the D: forests' clones on 2026-11-20 and now in
  `claude-desktop.md`'s ledger, is that naming. The app may show Ben a card the first time a
  session starts in a folder it has not seen.
- **A move into a MAM-private clone failed.** On 2026-11-18 a child in GitRepos/MAM-basics called
  `change_directory` for GitRepos/MAM-private, the clone the commander had granted it. The move
  takes effect when the turn ends; this one failed then and left Ben a dialog, which the child
  quoted as "couldn't move the session to C:\Users\BenDe\GitRepos\MAM-private". The child had worked
  by absolute paths meanwhile. Moves between the MAM-basics clones have worked. By the tool's
  description, Ben approves a folder in auto mode unless it is inside a workspace he trusts; whether
  that explains this failure is not established. So a child never moves into a MAM-private clone
  (`claude-desktop.md`, "Starting, tracking and closing a child").
- **Relayed requests cannot start a session.** On a turn that another session's message or an app
  event started, the app refuses `start_session`. On 2026-11-18 a "user_asked" start succeeded on a
  turn that a child's message had begun, after Ben's own message asking for that session had arrived
  in that turn. A request relayed through a child ("ask the commander to ...") therefore needs Ben's
  own words in the commander, or an "own_initiative" card, which Ben starts. A card takes no `cwd`,
  so it starts in the commander's folder.
- **The effort passed to `start_session` is not necessarily what the child runs at.** Two children
  started with "high", on 2026-10-29 and 2026-10-30, recorded max on every turn of their
  transcripts, and `get_session` reported max for both; why the request was not applied is not
  established. Read what a child runs at from `get_session`, or from the `effort` and
  `perTurnEffort` fields of its transcript.
- **Ben's effort configuration is his,** and the commander leaves it alone. When the commander
  recommended changing one of his settings to agree with another, he said on 2026-10-30: "I've
  messed with this many, many times in the past and I don't trust anything you do or any of your
  ability to introspect. Just leave it how it is."
- **Models:** `start_session` takes only the commander's model or a cheaper one, and the commander
  passes none. Ben may ask for a particular model for a child; `set_session_model` makes the
  switch, which takes effect from the child's next turn.
- **`list_events` shows assistant text and tool-call names, but no tool results.** An answer Ben
  gives in a plan-approval dialog therefore does not appear, and whether a plan session went on to
  execute has to come from Ben or from that session's next report. An interrupted dialog does
  appear, as "[Request interrupted by user for tool use]", and a message queued in that session
  then runs at once.
- **A waiting dialog is Ben's to answer.** The app's side-sessions notice says "do not stop or
  message a waiting session, do not change its mode or settings".
- **`get_usage` reports a session's context as it is now,** after any compaction, and says nothing
  about one. Ben, 2026-10-29, after the commander had cited a compacted child's 17% as a reason to
  keep follow-ups there: "I wouldn't have even asked about a fresh session if that had been the %
  context used before: a compaction happened in the meantime." The figure Ben saw can be much
  higher than the one the commander reads, so the commander says so whenever it cites one. A
  compacted session keeps only a summary of its earlier work and its recent turns; that is its whole
  advantage over a fresh session. By the tool's own description, a session that is idle, starting
  or archived reports its context as unavailable.
- **A message to a busy session waits for that session's turn to end.** On 2026-11-04 a grant sent
  at 14:25 New York time reached its child at about 14:46. A child may read the commander's
  transcript meanwhile, so the commander reports a grant only once it has sent it.
- **A child in another permission mode may hold the commander's message.** By SendMessage's own
  description, a session running in a different permission mode from the sender holds a
  cross-session message for Ben's approval and may let it expire; a child in plan mode is such a
  session.
- **`notify_when_idle` did not reach desktop sessions on 2026-10-29.** That day SendMessage
  refused it for all three adopted sessions: "Nothing was subscribed: notify_when_idle is only
  supported for Claude sessions on this machine in this release (not teammates, subagents, Remote
  Control or cloud sessions)." The turn-end notes of nested children are what wake the commander.
- **A cloud session** reaches only MAM-basics, since MAM-private is not attached to its environment,
  and it never reports back to the commander.
- **The shared notes folder** belongs to the commander's app session. The app names it in each
  child's prompt, and children write their handoffs and notes for the commander there.

## Compaction

- **When it happens:** the commander was compacted 31 times from 2026-10-29 to 2026-11-17, twice by
  hand and 29 times automatically, 18 of those before the clears of 2026-11-10 and 11 after. Each of
  the 11 fired with the first message to arrive after 69 to 895 minutes of quiet, two of them with
  Ben's own messages. On 2026-11-17 one fired with the context at 47% of its window, nowhere near
  full.
- **What comes back:** after each compaction Claude Code re-attached the instructions, the date, a
  summary of 16,000 to 20,000 characters, a reference to the running record, a few recently read
  files, and every skill the commander had invoked, whole. It did not re-attach the procedure that
  the commander then kept in a file, and the last three summaries did not name that file. From
  2026-11-10 to 2026-11-17 the commander reread the procedure on five occasions against 11
  compactions. That is why the procedure is now this skill.
- **What the skills documentation promises,** as read on 2026-11-17: after a compaction Claude Code
  puts back each skill's latest invocation, up to that skill's first 5,000 tokens and up to 25,000
  tokens for all skills together, the most recently invoked first, so that an older skill can drop
  out entirely. The original `SKILL.md` therefore stayed under 18,000 characters. The shared
  entrypoint now routes to `claude-desktop.md`; restoration of the entrypoint does not restore a
  reference read earlier, so the commander rereads the adapter after compaction. A commander that
  has invoked many other skills since this one could lose the entrypoint too; Ben's
  `/commander-session resume` brings it back.
- **A change to this skill** goes to its canonical copy, `dot-claude/skills/commander-session/` in
  MAM-basics, through a child holding a MAM-basics clone, once Ben approves the text; the commander
  writes in no clone. The deployed change reaches the commander only at its next invocation, such
  as `/commander-session resume` after a clear, since Claude Code does not reread a skill's file
  during a conversation.
- **The restart practice had not fired by 2026-11-17:** from Ben's choice of a restart by clear
  until that day's compaction the context grew to 47%, and the commander read `get_usage` once,
  after the compaction. Hence `claude-desktop.md`'s rule to read it at the end of each turn that reports to
  Ben.

## Restart mechanics

What the commander found on 2026-11-16 in Claude Code's commands and hooks references and in the
app's tool descriptions, with the correction of 2026-11-17 on `clear_session`:

- **`/clear [name]`,** also spelled `/reset` and `/new`, takes only a name that labels the old
  conversation in the `/resume` picker; it takes no first prompt. After a clear, Ben sends
  `/commander-session resume`.
- **`/compact [instructions]`** takes focus instructions for the summary.
- **`clear_session` with "self"** clears the commander when its turn ends, and it also takes no
  prompt. Its description lists pinned sessions and sessions open on screen among those it refuses,
  but on 2026-11-10 the pinned commander cleared itself this way at Ben's word, and Ben's pointer
  became the cleared conversation's first message. Whether a later release still allows it is
  untested. The commander does not use it on itself (`claude-desktop.md`, "Restarts").
- **A SessionStart hook** with the matcher `clear` or `compact` can add text to a new conversation's
  context. Such a hook runs in every session that reads its settings file, but it can stay silent
  outside the commander: the app sets `CLAUDE_CODE_HOST_SESSION_ID` in each session's process to
  that session's app session id. Whether the variable is still set when the hook runs after a clear
  is untested. Ben has asked for no such hook.

## Ben's words on restarts

At 15:04 New York time on 2026-11-16 Ben asked: "commander should periodically clear or compact
itself with a restart prompt (is there a sort of "argument" to clear and/or compact slash commands
that gives, in the case of clear, a new first prompt and in the case of compact, a sort of set of
hints about what to compact?"

At 15:15 he added the handover to a new session: "another option (a third option beyond
compact and clear) is for the commander to hand off its responsibilities to a new session, though
that would involve moving any nested sessions' ownership to the new session, so that is a tricker
way to go for a commander that is not empty."

At 15:33 he chose the restart by clear, in the words that `claude-desktop.md`, "Restarts", quotes.
