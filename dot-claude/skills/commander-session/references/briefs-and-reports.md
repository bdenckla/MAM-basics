# Briefs and reports

The Claude-specific detail behind `claude-desktop.md`'s "Starting, tracking and closing a
child" and the shared `SKILL.md`'s "Reporting to Ben". Ben's words are quoted exactly as the
commander's records give them, with their dates; everything else is Claude's wording except the
Codex-authored reference routing added for the shared skill.

## What a brief carries

A brief is a file in the state folder, named `<task>-brief-<date>.md`. It follows the user-level
section "Task prompts and handoffs" and carries, in this order:

1. **Its origin:** "Written by Claude (<model>) on <date> in the commander session", with the
   commander's title and id, and the brief's own file name, so that the child can find the file.
2. **Ben's words,** quoted exactly as a block, with the time he typed them in UTC and New York
   time, followed by "Everything else in this brief is Claude's reconstruction, not Ben's words."
3. **Pointers to check, not findings:** what the placement research turned up, for the child to
   verify.
4. **The task,** as a numbered list, with what done looks like. Choices for Ben go on the child's
   own decision page, with each choice's consequences and a recommendation. Ben's further requests
   in that session are its task too, within the scope the brief states.
5. **Placement:** the clone, its state when the commander checked it (clean or not, its commit
   against origin's `main`) and the time of that check, and that the commander assigns the clone to
   this child alone until it reports done. A child holding no clone writes nothing in any clone and
   asks the commander for one by SendMessage before its first Git-impacting change.
6. **The guard, for a child that starts in the commander's folder and moves:** check with
   `list_sessions` that no other session works in the target clone; move there with
   `mcp__ccd_directory__change_directory`, a deferred tool loaded with ToolSearch; verify the clone
   with `git rev-parse --show-toplevel`, `git rev-parse HEAD`, the branch and
   `git status --porcelain`; then fetch and fast-forward `main`. If any check fails, write nothing
   and tell the commander in one line by SendMessage.
7. **Integration, owned by the child:** commit on `main`, naming its paths in `git add` and
   `git commit`, with messages written to files that quote Ben's words; fetch and merge
   `origin/main` before each push; push `main` normally; on a merge conflict, stop and tell the
   commander. Every Git call gets `-c safe.directory=<that clone's exact path>`, and every command
   uses that clone's own `.venv` interpreter, run from the clone's root.
8. **Checks:** the verification cadence in `SKILL.md`, and the products section of `AGENTS.md` on
   what the last commit of a push says about the checks it skipped. Every tracked diff is read.
9. **Rules:**
   - **Questions:** the commander relays none. The child asks Ben on its decision page and in its
     final message, by number and question, and Ben can talk to it directly. The child asks Ben
     itself about a follow-up it could do in its own clone, and sends the commander by SendMessage
     anything it wants scheduled, not only in its report.
   - **An open decision** is put to Ben once, not carried from report to report.
   - **Release while waiting,** allocation rule 7 in `claude-desktop.md`, in full.
   - **Context:** past about 30% of its context with much left, the child carries on through
     subagents, one bounded slice each, with one writer in the clone at a time; past about 70% with
     work left, it writes a standalone handoff into the shared notes folder the app names in each
     child's prompt, stops, and sends the handoff to the commander by SendMessage.
   - **Credentials:** Git and `gh` get no chance to ask for them: `GIT_TERMINAL_PROMPT=0`,
     `GCM_INTERACTIVE=never`, `GIT_SSH_COMMAND=ssh -o BatchMode=yes` and `GH_PROMPT_DISABLED=1`.
   - **Standing rules:** no history rewrite, no force-push, no amend; PowerShell 7, with no `sed`
     or `awk`; scripts and commit messages in files, never `python -c` for anything substantial;
     anything likely to take over two minutes in the background; no Claude auto memory; read the
     clock before writing a time.
   - **Privacy:** MAM-basics is public on GitHub, so anything moved from `.novc/` into a tracked
     file is checked for private details first, and a link Ben keeps private is never printed or
     written; only the path of the file that holds it is named.
   - **Codex's forests,** if the child may read them: `git --no-optional-locks status`, or files
     only.
   - **The commander's id,** for SendMessage.
10. **The report:** it begins with `# Report: <subject>`, puts first what Ben must see, such as the
    decision page's link and the commits pushed, then what waits on Ben, and says whether the child
    holds a clone. A report of done releases it.

## Briefs of particular kinds

- **An issue-only session** loads `github-issues`, files only after Ben approves the text in that
  session, and begins its report with the issue's URL.
- **A Wikisource-edit issue** is done when its saved revision does what the issue asks. A brief
  never judges such an issue by origin's `main`, which takes the edit only at the next Wikisource
  refresh, routine work of its own. Ben, 2026-11-02, of four such issues closed while the mirror
  still lagged: "closing these issues is not (and should not be, for similar cases in the future)
  gated by this refresh."
- **A planning brief** tells the child to end its turn with its report and not to call
  ExitPlanMode.
- **An outward act that two children could take** gets one owner; the other child's brief tells it,
  in so many words, to leave the act alone.
- **A fresh session continuing a child's work** gets a frozen copy of the child's report or plan,
  made by script into the state folder, and the clones the child releases to it.

## Ben's words reach a brief only by script

- **Copy, never retype.** The commander's scripts in `tools/` find a phrase in a transcript, copy
  Ben's whole message into `words/`, and fill a brief template from it; a pasted multi-line message
  needs a fill script of its own. Transcripts are under `$HOME/.claude/projects/`, in the project
  folder named after the session's clone. A child that moved with `change_directory` keeps its
  transcript in the project folder of the clone it moved to.
- **Mid-turn messages** from Ben are stored as `queue-operation` entries and as an `attachment`
  entry's `prompt`, not as `user` entries, so a script that finds or copies his words reads both.
- **The start tool's prompt is a hand copy,** typed by Claude, so an invisible character in Ben's
  words can change on the way: on 2026-11-05 a narrow no-break space in a pasted time became a
  plain space. Before a start, list the words file's invisible characters by script, and name the
  brief file as the exact copy.
- **Pointed Hebrew is worse:** the same day a hand copy put a pointed word of Ben's message into
  Unicode's mark order. When Ben's words hold pointed Hebrew, the prompt quotes them without it, or
  points to the brief file for them, and says so. Hebrew in a frozen report is copied out of the
  transcript by script, never with Write or Edit.
- **After the start,** a script checks every non-empty line of the brief, and Ben's words, against
  the child's first prompt in its transcript.
- **A relayed quote of Ben** is checked before the commander acts on it. The quote finder in
  `tools/` reads the last day's transcripts in the project folders of Claude's four clones and
  prints Ben's turns that contain a phrase. Another session's quoting of Ben also appears in the
  commander's own transcript, so the finder skips that transcript, and it marks a turn that is a
  cross-session message as the sending session's text.

## Grounds of the rules for starting and placing a child

- **Effort max.** Ben, 2026-10-30: "I think you are launching sessions with only "high" effort but
  I prefer "max"?" The same day, of a report line saying that a session had started at max effort:
  "I consider that self-talk. Great that you took my instructions to heart, but you don't have to
  reassure me."
- **No cheaper model.** Ben, 2026-10-30: "for someone with a subscription model (as opposed to API
  pricing) I don't see why one would ever use Haiku."
- **Research before a start stops at placement.** Ben, 2026-11-07, of the research done before one
  start: "to me that is a bit beyond your brief, but I guess is okay." He approved the rule the
  same day: "Yes, add it".
- **Ben answers children; the commander relays nothing.** Ben, 2026-10-30, after the commander's
  question box had twice repeated a child's questions: "Why are you asking me about D1 to D3? First
  of all that's the job of the session in question (these are not session-management questions,
  which would be your job), and second of all I've answered it there." Asked the same day whether a
  question about starting further fixes also asked where they would be made, he said: "your call,
  but that session's context is 53% full ...".
- **Adopted sessions.** Ben, 2026-10-29: "Can you sort of take responsibility for the 3
  non-archived sessions that currently exist, even though they 'predated' you?"
- **Archive questions come to the commander.** Ben, 2026-10-30, after asking a child itself: "maybe
  I should be asking you such things because that is sort of a session-management question?" That
  day a child said that another session could be archived, unaware that the other session still
  had a follow-up to plan; a child vouches only for its own state.
- **Place every plan.** Ben, 2026-10-30: "there is a plan proposed there, as usual with
  possibly-bad-idea in-planning-session execution proposed. That's something you need to decide on"
- **A child past about half its context.** Ben, three times on 2026-10-30:
  - "My answer is, yes, go ahead, but not necessarily in this (>50% context full) session";
  - "Yes, but I advise a fresh session for this and any other follow-up work";
  - "as usual, I'd like like to discuss that (I don't have an answer yet), and do the resulting
    work in a fresh session".
- **One owner for each outward act.** Ben, 2026-10-31, after one child offered to file an issue
  that another child had already drafted: "I'm concerned that we have some cross-session
  responsibility, which could result in double-issue filing or zero-issue filing"
- **Release while waiting.** The commander proposed the rule after Ben asked whether another
  forest, a long-lived worktree or cloud sessions would help; he approved it on 2026-10-31: "Yes,
  fine, please implement."
- **Issue-only sessions.** `github-issues`, "Issue-only sessions", quotes Ben's words of
  2026-10-30.

## Reporting rules and their grounds

1. **Report by pointer.** Each changed session gets one line: its state, its commits, and "waits on
   you there" for anything it asks, with no detail from the child's report. The fault this
   corrected was copying a child's figures and examples into the commander's own decision lists.
   Ben, 2026-10-30: "I don't think we're striking the right balance in this session; maybe it is an
   impossible balance to strike because session-management questions cannot be separated from
   internal-to-the-session details. The result is I'm being asked detailed questions in this
   session that I think are repeated inside other sessions. I'm not sure what the answer is, short
   of doing all communication here, which I don't want to try (at least not yet). Maybe just more
   "see session X for details; answer there"-type text here?"
2. **What is asked in the commander:** only an archive, a start of new work, or a follow-up needing
   another session or clone, each in one line that names the session whose report has the details.
   A follow-up the child can do in its own session and clone is placed there by its line: "if you
   want it, tell it there".
3. **Every state report lists what is queued,** even when nothing about it changed, under a name
   Ben has been told. Ben, 2026-10-31: "when you report state like this, please say what's queued."
   He had had to ask what a plan named in earlier reports was, and whether a task was queued.
4. **Work waiting on an outside party with no date in view** is named when it is queued and again
   only when it changes. Ben, 2026-11-04, of a line repeating that a pull request would be posted
   once an outside project's maintainers accepted another: "You don't have to keep telling me this.
   For one thing, for all we know it will be months, if ever, that this happens, so it is not like
   we're expecting feedback today or tomorrow."
5. **The commander's own checks stay out of the report** unless one fails. Ben, 2026-10-30, of a
   line saying that a session held no clone and wrote nothing in one of Codex's forests: "I also
   didn't need to know those details. It is certainly a big help that you handled those details,
   but the cherry on top would be to not only not have to handle them but also not have to hear
   about them."
6. **No commit hashes.** Ben, 2026-10-30: "I really don't care about hashes. If you need this for
   your own records in this transcript, can you hide them behind some sort of "details" collapsing
   display, that is collapsed by default?" The commander's records come from Git and the state
   folder, so its reports name no hashes; a hash that matters to a decision of Ben's goes in a
   `<details>` block.
7. **Don't hand Ben a step the commander can take.** Ben, 2026-10-30, of a line telling him that he
   had to start and pin a new session: "why would I have to do that? I mean, it is no big deal, but
   sometimes I feel like you paint yourself as more helpless than you are."
8. **Anything for the commander goes by SendMessage,** since a turn-end note quotes only the first
   400 characters of a report. Ben, 2026-10-31, of a recommendation that had reached the commander
   only as a line deep in a report: "Do you feel like the commander knows about this?"
9. **Put an open decision to Ben once,** and turn no offhand acceptance into more process. Ben,
   2026-11-04, of a name he had accepted: "... because you were repeatedly mentioning it as a loose
   end in another session and I was finding it annoying." Briefs have said so since that day.
10. **Read the clock before writing a time.** On 2026-11-04 the commander twice wrote estimated
    times that lay in the future.
11. **Report a grant only once it is sent.** A message to a busy session waits for that session's
    turn to end, and a child may read the commander's transcript meanwhile.
