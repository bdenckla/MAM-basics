# Plan: automate the dual-agent review relay, and measure what the second agent adds

State: live. Ben authorized implementation on 2026-09-30; core code and four real automatic
handoffs are verified in GitRepos2. D13 and notification receipt are confirmed;
production is enabled, and scheduler registration and an idle tick are verified
2026-10-01. Ben started the approved first production round on 2026-10-01;
the first three production handoffs are independently verified and turn 04 is running.
The blind measurement is complete. Later production handoffs, stopping behavior
and the approved comparison record remain to be verified.

Planned 2026-09-30 by Claude Fable 5.1 in a Plan Mode session started in
`C:/Users/BenDe/GitRepos/MAM-basics` at `38a360d2`; file and line citations refer to that commit.
Ben declined the session's request to leave Plan Mode, switched the session's model to Claude
Opus 5.5, and asked it to persist the plan here. The Opus session copied the plan the same day
with the changes listed under "Corrections made while persisting". Persisting the plan does not
authorize executing it. Ben's words, verbatim:

1. His opening message:
   > It is inefficient for me to shepherd Claude and Codex through the many turns of a DAR
   > (dual-agent review). I suppose it is worth questioning how much value the dual-agent review
   > process offers over, let's say, an iterative single-agent review process where the agent is
   > basically asked to "try harder" (review the review, review the review of the review, etc.).
   > Another direction to consider is whether the review branch (usually having a name of the
   > form dar-YYYY-MM-DD) could act as a kind of "mailbox" that, through polling or triggering, a
   > single session in Claude and Opus responds to, automatically. One wrinkle there is that
   > although Codex could spawn a fresh session in response, Claude I believe is limited to
   > spawning a sub-agent, but maybe that's not a problem and in fact Codex should use sub-agents
   > to "take a turn" rather than fresh (independent) sessions
2. His reply during the session, beneath the quoted phrase "the Codex app ships a non-interactive
   CLI":
   > Probably will be some sort of authentication nightmare, but sure, why not try, if only in the
   > spirit of confirming that it won't work.
3. His selections in four dialog questions, whose option labels the Fable session wrote: "Yes,
   build the dispatcher (Recommended)"; "Task Scheduler job (Recommended)"; "Opus 5.5 and the
   current Sol (Recommended)"; "Finish both by hand (Recommended)". The section "Decisions Ben
   made on 2026-09-30" gives what each selection means.
4. His request to the Opus session:
   > Please (1) persist this plan as a file in the "doc" folder (2) opine as to whether, though it
   > was planned by Fable, it can be executed by Opus.
5. His question about the Opus session's advice to execute "in a worktree": "why in a
   worktree?" In the dialog that followed he selected "GitRepos2 or GitRepos3 clone
   (Recommended)".
6. His instruction when he ended Plan Mode for that amendment:
   > You are out of plan mode so you can edit the plan, NOT so you can execute it.

Everything else below is the two sessions' reconstruction. Re-verify every observation dated
2026-09-30 before relying on it; the section "Observations of 2026-09-30" gives the commands.

## Execution frame

- **Executor:** a fresh session at its model's top effort, Claude `max` or Codex `xhigh`. Nothing
  in the plan depends on the model that wrote it.
- **Source and baseline:** this file on `main` at or after the commit that last changed it, a
  descendant of `38a360d2`. Check with `git merge-base --is-ancestor 38a360d2 HEAD` in the
  development checkout.
- **Development checkout:** a full MAM-basics clone in a secondary forest,
  `C:/Users/BenDe/GitRepos2/MAM-basics` or `C:/Users/BenDe/GitRepos3/MAM-basics`, whichever no
  other session is writing to; `--forest-status` reports occupancy. Ben chose this on 2026-09-30
  over the linked worktree the first persisted version named. Fetch and fast-forward `main`
  before editing, then record the path and exact `HEAD`. Interpreter: that clone's own
  `./.venv/Scripts/python.exe`, run from the clone's root.
- **Integration owner:** the executing session. It commits on `main` in that clone and pushes
  normally, merging a moved `origin/main` first, as `doc/clone-forests.md`, "Work and
  verification", prescribes.
- **Required reading:** `AGENTS.md`; `doc/dual-agent-review.md` (D9, D10, D11, and "Review
  filenames and State lines"); `doc/periodic-review.md` ("The effort a review runs at" and
  "Reviewing the review, with the same agent and with Ben"); `dot-Codex/user-wide-AGENTS.md`;
  `dot-claude/README.md` ("Main-sourced deployment and check"); the skills
  `iterative-document-editing`, `github-issues` and `mam-repository-topology`.
- **Expected unchanged outputs:** nothing here reaches a mega generator, so no file under
  `gh-pages/` or the `MAM-*` product directories changes. Any such diff is a finding.
- **Checks:** `git diff --check` before each commit; Black on each changed Python file; the new
  test; the full suite once after the last code change,
  `./.venv/Scripts/python.exe py/main_test.py` from the repository root. No mega run.
- **Commit discipline:** coherent commits that name their paths. The procedure text of section 1
  records a decision of Ben's, so it is committed only after he approves its wording.
- **Pointer issue:** none was filed on 2026-09-30, because Ben was deciding whether execution
  would start at once. If the plan waits instead, the `github-issues` skill's rule for a plan
  whose work is still to be done calls for a thin pointer issue.

## Requirement ledger

| Id | Requirement | Status |
|---|---|---|
| R1 | Relieve Ben of relaying each turn | four real automatic handoffs passed in the isolated mirror; first three production handoffs independently verified and turn 04 running; later handoffs and stopping behavior remain pending |
| R2 | Weigh the dual-agent review against one agent iterating on its own review | Ben approved the first-round comparison and `doc/dual-agent-review-comparison-2026-10-01.md` on 2026-10-01; the separate blind Claude process completed at the verified turn-01 commit; fresh independent assessment completed; parent verification and comparison record remain pending |
| R3 | Use the review branch as a mailbox, by polling or trigger | implemented: explicit registry and branch polling, with no adoption of manual rounds |
| R4 | Choose between sub-agents and fresh sessions for taking a turn | both fresh-process workers completed real turns with read-only sub-agents; four handoffs passed |
| R5 | Try the headless CLIs despite the expected authentication trouble | verified 2026-09-30 after Ben renewed Claude login: both headless workers completed two real turns |
| R6 | Dispatch from a Task Scheduler job | implemented: Ben registered the task on 2026-10-01; exact settings verified, scheduled idle tick completed with result 0; notification receipt confirmed |
| R7 | Pin `claude-opus-5-5` at `max` and the kickoff Sol model at `xhigh` | verified in both Claude turns' launch records and both Codex turns' saved runtime contexts |
| R8 | Finish the two rounds in flight by hand | implemented: Ben reported both September 29 reviews completed on 2026-10-01; neither was adopted or modified by the relay |
| R9 | Persist the plan in `doc/` | implemented by the commit that added this file |
| R10 | Execute in a GitRepos2 or GitRepos3 full clone, not a linked worktree | implemented in the verified GitRepos2 full clone |

## Execution authorization and checkout, 2026-09-30

Codex records Ben's instruction: "Implement the recent plan to try to make auto-handoffs
in dual-agent review. I'm not sure what the plan is called." Ben then instructed:
"don't interfere with either of the ongoing dual-agent reviews (a MAM-basics and a MAM-private)".
The actual development checkout is `C:/Users/BenDe/GitRepos2/MAM-basics`, clean `main`
at `303bf2399c1e1fc1300a75f4fb1ed335d62984d0` before editing; `38a360d2` is an ancestor.
That clone's own `.venv/Scripts/python.exe` runs all checks. Codex owns the main push.
`doc/dual-agent-review-automation.md` holds the implementation details, D13 approval
record, local verification results, and remaining operational prerequisites.
Ben subsequently selected the D13 approval passage in Codex's implementation
report and replied "I approve" on 2026-09-30. The approved wording is now in
`doc/dual-agent-review.md`, "Automated relay and the `Next:` line" (D13).
The ongoing reviews and the occupied primary clone remain outside execution scope.

## Implementation status and choices, updated 2026-10-01

Ben approved the runbook's proposed D13 wording on 2026-09-30, satisfying this
plan's requirement for approval before adoption as the review procedure. D13 is
now adopted in `doc/dual-agent-review.md`. Production is enabled after Ben
confirmed the corrected notification; Ben registered the scheduler on 2026-10-01. The manual
procedure continues to govern the ongoing rounds. The runbook records the final suite result
(1015 passed, 5 skipped, 60 subtests), the local Git differential check, and probes
P1 through P8. Ben renewed Claude login and the headless Opus 5.5 probe succeeded.
The isolated public-source capability check exposed denied native PowerShell Git
reads; the launcher now names the exact checkout and read commands in its allow
rules. Both full capability checks subsequently passed, including native Git,
foreground sub-agents and ignored JSON writes. The local-mirror round completed
four automatic handoffs, stopped before turn 05 at its four-turn cap, and then
remained idle. The real round requested an acknowledgment; it did not close.
Independent Git evidence confirms only the permitted turn paths changed, turn 02
preserved turn 01's byte prefix, and metadata stayed unchanged. Closure and idle
after closure passed separately in the differential check. A future production
window needed Ben's approval at this rehearsal stage; the production-kickoff entry
below records his later start. This plan's full definition of done has not been met.
The real-worker collision probe also passed: a same-tree child commit advanced
only the local mirror's synthetic `dar-2026-10-02` branch while Claude ran. The
dispatcher rejected the moved remote, preserved its pause, marker and logs, and
invoked the hidden toast without recording an error. Ben has been asked to check
Windows notifications with Win+N. Ben reported no matching notification and
provided a screenshot showing ChatGPT notifications. The helper's assumed sender
`Microsoft.Windows.PowerShell` was absent from the installed app list. The
corrected helper resolves the installed Windows PowerShell sender, checks its
notification setting and records whether the submitted toast reached history.
Both its hidden launch and the dispatcher path reached history. Ben replied
"Yes, I see the corrected test" and supplied a screenshot showing Windows
PowerShell, **Dual-agent review** and the corrected test message. This satisfies
P6's receipt check and clears the production flag. The runbook records the fix,
preserved screenshot manifest and completed registration command.

Ben subsequently ran the supplied registration command and reported
**Dual-agent review relay**, **Ready**. Codex independently verified its exact
helper-clone action, three-minute repetition, interactive limited privilege and
**IgnoreNew** setting. A scheduled tick completed with result `0`; the registry
is absent and there are zero registered rounds. The receipt is
`.novc/relay-scheduler-registration-20261001.json` in the implementation clone.
No production round was started at scheduler registration. Ben subsequently ran
the approved kickoff, as recorded below. The two September 29 manual rounds stay excluded.

## First production preparation, 2026-10-01

Codex continued in the intended full clone at clean `main`
`61fa3d1d06311ae6567be12093809aa446e1ff52`, equal to the handoff baseline and
the live `origin/main`. The four focused relay tests passed at that commit.
The historical 1,015-test result below validates its stated implementation
revision, not every change subsequently merged into this baseline.
The scheduler's exact hidden action, three-minute interval, interactive limited
privilege and IgnoreNew setting still match the registered configuration;
its latest completed tick returned `0`. Production is enabled, the registry
is absent, and no production round has been started.

The proposed first window is the endpoint diff
`303bf2399c1e1fc1300a75f4fb1ed335d62984d0..1bfceff4d952470618fc7584a6bca4fc5c9b2f5f`:
nine relay implementation commits and 15 changed paths, with no product changes
or September 29 review records. This bounded rollout review is a proposed
selection, not a replacement for the periodic series' carried-forward anchor.
Claude was recommended as Agent 1. Before kickoff, the proposed remote branch,
local carriers, worktree paths and round control directory were checked absent.
Ben subsequently ran the supplied start command after the preparing conversation
yielded, approving the date, window, Agent 1 and exact kickoff instruction through
that action. The production-kickoff entry records the verified result.

Ben selected "Run the comparison using that filename (Recommended)" in response
to Codex's concrete comparison proposal. That approves one fresh Claude
counter-argument blind to Codex turn 02 and an independent comparison, recorded
on `main` as `doc/dual-agent-review-comparison-2026-10-01.md`. The runbook's
"Approved comparison preparation, 2026-10-01" records the prompt frames and
the exact turn-01 commit that must be filled before the blind worker starts.
Facts-only from turn 03 remains false; Ben has not approved adopting that rule.
Private readiness P7 remains unverified.

## Rollout handoff authorization, 2026-10-01

Ben reported completion of both manual reviews and authorized proceeding:

> Both 09-29 reviews (MAM-private and MAM-basics) are completed. I am doing some follow-up items suggested by the MAM-basics 09-29 review but that work is not part of the review proper. So I think you can proceed, though you are approaching compaction, so perhaps give me a prompt for a new session that will proceed.

This is Ben's completion report, not an independent audit of review integration
or branch retirement. The review-completion wait is cleared. His follow-up work
remains outside this task's write ownership, and neither completed manual round
is adopted. A fresh Codex session continues in
`C:/Users/BenDe/GitRepos2/MAM-basics`, using its own environment and owning any
further authorized main integration. The first-production-preparation and
production-kickoff entries record the later comparison approval and kickoff.
The facts-only rule remains unapproved.
Private readiness P7 remains unverified.

## First production kickoff, 2026-10-01

Ben ran the supplied start command and returned its status. Independent Git reads
verified setup commit `ef133e4dc79de069229754ee8dc8d5fc59b3e812` on
`origin/dar-2026-10-01`, based on the clean home clone's `main` at
`870ce133048aff218484683f5ef3f569150e086b`. The recorded approved endpoints are
`303bf2399c1e1fc1300a75f4fb1ed335d62984d0..1bfceff4d952470618fc7584a6bca4fc5c9b2f5f`,
Claude is Agent 1, the caps are 10 and 1, and facts-only remains false.
The exact kickoff instruction is:

> Run the first automated MAM-basics review of the relay implementation window with Claude as Agent 1.

The existing scheduler launched turn 01 at
`2026-10-01T11:11:14.568068-04:00, New York time`. The task was Running, with
its dispatcher lock, in-flight marker, prompt and launch record present.
The launch pins Claude Opus 5.5/max; its startup hook succeeded. One compound
PowerShell Git read was denied by the allow rules, and subsequent native Git
reads succeeded. No handoff or halt was established by this initial observation.

Under Ben's comparison approval, Codex queued the separate fresh headless Claude
measurement with `.novc/run-approved-relay-comparison-20261001.py` in the home
clone. It waits for the dispatcher's verified `handoff-turn-01.json`, then creates
a separate locked checkout detached at that exact commit, fills the prepared
prompt, and launches Claude at the round's pinned Opus 5.5/max. It neither launches
nor commits a review turn. Its wait is bounded to three hours and its worker to
the configured 120 minutes. The measurement's records are under
`.novc/dual-agent-review-comparison/2026-10-01/`; failure preserves the venue and
records for inspection. Production verification and the independent comparison
remain unfinished. Neither completed September 29 round is adopted.

Ben then selected "Approve this follow-up (Recommended)" for a 15-minute
follow-up in the preparing chat: verify this production round, finish the
already approved comparison, commit and push completed documentation, then stop.
Automatic approval review had rejected creating that recurring automation without
explicit authorization. After Ben's approval, Codex created the active chat
follow-up `verify-first-production-dual-agent-review`. It stays quiet during
ordinary progress, reports a halt, required decision, measurement failure or
completion, and pauses after the round ends or halts and the comparison is
recorded, or when a halt prevents that comparison. It does not dispatch review
turns, override a halt or authorize close-out or remediation.

Core commit `1a50d4b6d132a66dcb9d54d9b9275cd62fc2d580` is on `origin/main`.
The complete main-sourced configuration deployment installed only the new Claude
agent file, and its follow-up check reported zero problems. Existing instructions,
hooks and skills were already clean and were not replaced.

The implemented mechanics supersede the planned mechanics below where they differ:

- The helper clone is GitRepos2. It runs without updating the occupied primary clone;
  round worktrees belong to the exact full clone named at kickoff.
- Only rounds explicitly registered by `start` are polled. Existing manual branches
  are never adopted. Private logs and notifications stay in the private repository.
- Toasts use the installed Windows PowerShell sender returned by `Get-StartApps`,
  rather than an assumed identifier. A blocked setting raises an error; successful
  submissions record sender, setting, tag and history evidence in `toast-result.json`.
- Carriers update through verified `--ff-only` merges. No reset or `checkout -B` is
  used; unexpected commits and occupancy stop dispatch.
- Default caps allow one reopening and turns 01 through 10. The first reopening is
  permitted; a second stops. Facts-only from turn 03 remains false pending Ben's
  separate decision. Other proposed defaults are recorded in tracked configuration.
- `dontAsk` and explicit tool allow rules include native PowerShell and ordinary
  Git reads, plus exact per-checkout trust options before the read subcommand.
  Authentication, native Git permissions and headless sub-agents passed both live
  capability checks and four real turns. Worker-local configuration disables
  background checkers, and prompts require waiting for every foreground checker.
- Codex starts a fresh `exec` process without `--ephemeral`: the first capability
  check's child could not load its parent transcript under that flag. The dispatcher
  never resumes a prior turn. Claude's exact native PowerShell Git read passed
  independently after the permission fix; the full capability checks also passed.
- The header-only `Next:` parser ignores quotations in the body. The independent
  transition oracle covers both header cardinality and raw, fenced and blockquoted
  forms, so review prose cannot change dispatcher control state.
- Manual mechanics in D9, D11 and `doc/periodic-review.md` explicitly point to D13's
  automated caps, worktrees and dispatcher-owned Git operations. The approved D13
  wording is unchanged. The planned fallback to adopting a manual round is not
  implemented; both headless sub-agent checks passed and existing manual rounds
  remain excluded.
- Atomic in-flight markers record an approved tree before commit. Manual handoff can
  recover that commit or an already successful push idempotently after a failure.
- Rehearsal setup checks every fetch and push URL before any remote query, requiring
  one local filesystem destination of each kind. URL identity changes refuse a
  worker result before outbound contact; launch records do not store credentials.
- `pythonw.exe` supplies the hidden scheduler launch. A hidden Windows PowerShell
  WinRT helper supplies the toast; agent shell commands use PowerShell 7.
- The three-turn local check uses deterministic fake workers and does not establish
  real-model review behavior. Four real turns and the real collision guard passed
  separately, and the scheduler is registered with a verified idle tick. Private
  SSH probing, measurement and first production adoption remain rollout work.

## Continuation checkpoint and successor prompt, 2026-10-01

Codex prepared this checkpoint in the GitRepos2 home clone at clean `main`
`7d0426b2e79f2c673c7e2f127de797b5ff68389c`, pushed normally to `origin/main`.
That commit merges Ben's separate dispatch-test cleanup and its record,
`954dacf5` and `f3760d1c`, with the rollout documentation. The merged tree passed
`py/main_test.py -q`: 1,016 passed, 5 skipped and 60 subtests passed in 137.44
seconds. Black's check left the changed dispatch test unchanged, and
`git diff --check` passed. This new full-suite result belongs to the merged tree;
the earlier 1,015-test result remains historical.

At `2026-10-01T11:42:36.499333-04:00, New York time`, the production branch
still held setup commit `ef133e4dc79de069229754ee8dc8d5fc59b3e812`, with Claude
turn 01 live, no handoff receipt and no pause. The blind measurement operator
was still waiting for the verified turn-01 handoff. These are dated observations,
not assumptions for a successor: recheck the control records and current processes.

The preparing chat and its approved follow-up remain the verification and
comparison owner. Compaction does not transfer that ownership. A fresh chat may
inspect read-only, but must establish an explicit handover and disable or transfer
the existing follow-up before becoming the writer. Never leave two follow-ups
writing the same home clone. The Windows dispatcher continues independently and
retains sole ownership of every numbered review turn.

**Backup successor prompt:**

> Codex prepared this handoff on 2026-10-01. Ben's latest instruction, verbatim:
> "Oh, the second of two things is this session will soon be compacted; should
> anything be done to make a more orderly management of context, e.g. start a new
> session (or give me a prompt for a new session that I will start)?"
> The remaining prompt is Codex's reconstruction. Codex recommended retaining
> the preparing chat as owner through compaction; this is a backup prompt for a
> deliberate later handover, not evidence that Ben approved transferring ownership.
>
> Source, intended development and main integration checkout:
> `C:/Users/BenDe/GitRepos2/MAM-basics`. Required source commit:
> `7d0426b2e79f2c673c7e2f127de797b5ff68389c`. The successor, once ownership is
> transferred, owns authorized documentation integration in this full clone.
> Use `C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe` from that
> repository root. Verify root, HEAD, branch and NUL-delimited status; a newer
> HEAD must contain the required commit. Preserve newer commits and unowned work.
>
> Read `AGENTS.md`, `doc/PLAN-automate-the-dual-agent-review-relay.md`,
> `doc/dual-agent-review-automation.md`,
> `doc/dual-agent-review.md` and `doc/periodic-review.md`. Load
> iterative-document-editing, codex-worktree-tasks and mam-repository-topology.
> Check the existing follow-up `verify-first-production-dual-agent-review` before
> writing. If it remains active in the preparing chat, inspect read-only and
> report the state; obtain Ben's explicit handover instruction before changing
> its ownership. Establish one writer before any main edit or commit.
>
> Continue verification of production round `2026-10-01`, shared remote branch
> `dar-2026-10-01`, Agent 1 Claude. Approved window:
> `303bf2399c1e1fc1300a75f4fb1ed335d62984d0..1bfceff4d952470618fc7584a6bca4fc5c9b2f5f`.
> Setup commit: `ef133e4dc79de069229754ee8dc8d5fc59b3e812`. The pinned workers
> are Claude Opus 5.5/max and Codex `gpt-6.1-sol`/xhigh; caps are 10 turns and
> one reopening, and facts-only remains false. The scheduler is already
> registered. Let the dispatcher launch, commit and push every review turn;
> never restart the round, relay manually, remove a marker or bypass a halt.
> Verify handoff ancestry, permitted paths, unchanged round metadata,
> reconciliation prefixes, model and effort evidence, and stopping behavior
> under the approved procedure. Distinguish a live in-flight marker from a
> stalled worker; a planned next turn alone does not authorize launching it.
>
> Ben approved one blind Claude counter-argument and the independent comparison
> in `doc/dual-agent-review-comparison-2026-10-01.md`. The one-time operator
> `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/run-approved-relay-comparison-20261001.py`
> already exists and was launched; execution session 57831 was still running
> at handoff. Inspect its waiting, in-flight, completion and failure receipts
> under `.novc/dual-agent-review-comparison/2026-10-01/`, and verify process
> state before any recovery. Never duplicate the operator or blind worker.
> The operator creates a separate locked checkout detached at the exact pushed
> turn-01 commit. Verify the saved log's blind input boundary before accepting
> the output. After both the blind output and pushed Codex turn 02 exist, use
> a fresh read-only comparison sub-agent with no inherited conversation that
> authored neither counter-argument. Verify its claims, preserve both
> counter-arguments and measured effort in the approved record, then commit
> and push finished documentation on main normally. Do not infer missing
> timing or token figures or turn this single measurement into standing policy.
>
> A compact read-only inspector is
> `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/inspect-production-relay-20261001.py`.
> Protect Ben's separate follow-up work, both completed September 29 reviews,
> and all rehearsal venues, unique commits, logs, markers and screenshot evidence.
> Private readiness P7 remains unverified; private automation is outside this
> round. Close-out and remediation retain their separate procedures. Notify
> only on a meaningful halt, decision, measurement failure or completion.
> Pause the verification follow-up after the round ends or halts and the
> comparison is recorded, or report and stop if the halt prevents comparison.

## First production handoff verified, 2026-10-01

The dispatcher pushed Claude turn 01 as
`dd50e9b946609ac8ab7cc8c15d205d93dd5390e9`, a direct child of the setup commit.
The independent verifier checked the receipt, exact changed path, unchanged
round bytes, quoted kickoff instruction, valid `Next: turn 02, codex`, pinned
launch model and effort, and successful Claude terminal event. A live remote
read corroborated the pushed commit. The saved evidence is
`.novc/production-relay-independent-verification-20261001/turn-01.json`; the
repeatable scratch verifier is `.novc/verify-production-handoffs-20261001.py`.
The worker's terminal log reports 3,125,198 ms and 66 turns; these are recorded
worker measurements rather than a reconstruction from commit times.

The scheduler launched Codex turn 02 at
`2026-10-01T12:05:19.992312-04:00, New York time`. The already-running comparison
operator launched the separate blind Claude worker at
`2026-10-01T12:03:58.249172-04:00, New York time`. Independent Git reads found
its dedicated checkout detached at the exact turn-01 commit with clean
NUL-delimited status. At this observation both processes were live, neither
turn 02 nor the blind output was complete, and the verification follow-up was active.

## Second production handoff verified, 2026-10-01

The dispatcher pushed Codex turn 02 as
`c9d49a232357140a1d370d454be42b3fd1c8f309`, a direct child of the verified
turn-01 commit. Independent verification checked the exact two changed paths,
unchanged round bytes, original turn-01 bytes preserved as a prefix, quoted
kickoff instruction, valid `Next: turn 03, claude`, pinned launch arguments and
successful Codex terminal event. A live remote read corroborated the push.
The worker's saved runtime context independently confirms `gpt-6.1-sol`,
`xhigh`, and the dedicated Codex checkout. Evidence is preserved in
`.novc/production-relay-independent-verification-20261001/turn-02.json` and
`codex-context-123822-698840.json` in that same directory.

The scheduler launched Claude turn 03 at
`2026-10-01T12:26:19.948592-04:00, New York time`. The separate blind Claude
measurement was still running at that observation. The independent comparison
then awaited that measurement's verified completion; Codex turn 02 was available.
No production halt was observed, and the verification follow-up remained active.

## Third handoff and terminal suppression, 2026-10-01

The third production handoff is `58597c3b622e37839e97f49c86df63a9eadc3fde`,
independently verified against its receipt, exact Git parent and changed path,
unchanged round metadata and successful Opus 5.5/max terminal result. Codex
turn 04 is live in its dedicated worktree. The separate blind measurement
completed successfully, and the fresh read-only comparison agent completed its
assessment; parent verification and the finished comparison record remain.

Ben asked to suppress distracting terminal windows. The Windows Git child
launches now use `CREATE_NO_WINDOW`; workers remain running and later scheduled
controllers load the change. The complete suite passed 1,016 tests with 5 skips
in 154.11 seconds. The runbook's "Suppressing dispatcher Git consoles" passage
records the exact scope and the limit of the visible-window observation.

## Context: what the relay costs

- MAM-basics `origin/dar-2026-09-29` held eight turns when planning began. Its pushes, New York
  time: 14:08, 15:13, 16:03, 16:10, 16:13, 16:20 and 17:24 on 09-29, then 08:11 on 09-30.
  Turn 09, Claude's, was pushed at 10:09 on 09-30 while this plan was being persisted.
- A MAM-private round of the same date ran in parallel, relayed the same way.
- An agent's turn takes minutes. Every longer gap is Ben's relay: a fresh session or thread per
  turn and a one-line instruction such as "take turn 4 of the 09-29 review".
- MAM-basics round lengths: 09-08 five turns plus an appended acknowledgment, 09-10 four, 09-14
  four, 09-16 six, 09-26 six, and 09-29 at least nine. No round in either repository closed
  before turn 4: every turn 02 raised something, and the stopping rule owes an acknowledgment
  turn.

## Assessment: what the second agent has added

The records show a real but modest contribution per round. Most correction volume comes from
same-model checks in fresh context. The records cannot show the one thing only a second model can
supply: misses that Claude's model would never notice. No blind round was ever run, and Claude
was Agent 1 in every round, so "Codex", "the second agent" and "going second" cannot be told
apart. The evidence supports Ben's suspicion without settling it. This plan therefore removes the
relay cost first and runs one measurement, rather than dropping Codex on present evidence.

The evidence comes from a sub-agent's reading of all eleven rounds in both repositories, which
cited a passage for every count. Private-series detail stays in MAM-private and appears here only
in aggregate.

- Codex's turn 02 rejected no finding outright in six of eight alternating rounds. It added zero
  to four items per round. Additions that mattered on their own appeared in about half the
  rounds. Two public examples: the 09-10 round's 3,590 lookups that succeed at the wrong atom,
  and the 09-14 round's two gaps that would have stopped its remediation plan.
- Corrections flowed both ways. Claude caught factual errors in Codex's turns in at least seven
  rounds, and several of Codex's qualifications "answer claims the argument did not make", in the
  words of the 09-26 turn 03.
- Same-model checking in fresh context already does most of the correcting. The double re-review
  in `doc/periodic-review.md`, "The evidence from 2026-09-12", found real defects on both passes.
  The 09-26 turn 03 self-check made "13 corrections of substance and 4 of wording". The 09-29
  turn 07, re-checking with four sub-agents, corrected ten statements of its own turn 03.
- Rounds lengthen for reasons other than substance: disputes over characterization and locator
  labels (09-16, 09-26), a scope objection only Ben could settle, the owed acknowledgment turn,
  and errors from low-effort turns. The MAM-basics 09-29 round spent turns 04 to 06 on turn 03's
  clock times and provenance.
- No per-turn time or token record exists, so cost cannot be compared.

## Decisions Ben made on 2026-09-30

1. Build the dispatcher. For automated rounds it supersedes the step "Ben supplies the next task
   with that file's path and pushed commit" in `doc/dual-agent-review.md`.
2. Dispatch from a Windows Task Scheduler job running a Python tick every few minutes, with
   headless `claude -p` and `codex exec` workers. The dispatcher commits and pushes.
3. Pin the worker models: `claude-opus-5-5` at `max`; for Codex, the Sol model that
   `C:/Users/BenDe/.codex/config.toml` names at kickoff, pinned for the round at `xhigh`.
4. Finish the two rounds in flight by hand. The dispatcher starts with the first round created by
   the new setup action.
5. The executor works in a GitRepos2 or GitRepos3 full clone, not a linked worktree.

## Observations of 2026-09-30

Claude, on this machine:

- Only the desktop app is installed. Its bundled Claude Code CLI is
  `C:/Users/BenDe/AppData/Roaming/Claude/claude-code/2.1.284/claude.exe`; the version segment
  changes on update. Its help lists `-p`, `--agent`, `--agents`, `--effort`, `--model`,
  `--permission-mode`, `--allowedTools`, `--disallowedTools`, `--output-format`, and a
  `setup-token` command: "Set up a long-lived authentication token (requires Claude
  subscription)". A headless probe failed with "OAuth session expired and could not be
  refreshed". Print mode refuses `stream-json` output without `--verbose`: "When using --print,
  --output-format=stream-json requires --verbose". The `claude.exe` under
  `C:/Program Files/WindowsApps/` is the Electron app, not the CLI.
- A custom agent file supports frontmatter `model`, `effort` (including `max`), `permissionMode`,
  `tools`, `disallowedTools`, `maxTurns` and `omitClaudeMd`, per the Claude Code sub-agent
  documentation. Sub-agents start with fresh context.
- `C:/Users/BenDe/.claude/settings.json` sets `"model": "sonnet"` and `"effortLevel": "xhigh"`, so
  model and effort must be pinned per launch. Its allow list includes `Bash(git -C:*)`,
  `Bash(git commit:*)` and `Bash(git push:*)`, so a headless worker may commit and push unless the
  launch denies it.
- Desktop scheduled tasks, `Monitor`, `CronCreate` and cloud routines exist and were evaluated.
  The chosen design uses none of them.

Codex, on this machine:

- The Codex desktop app bundles the CLI. Its directory changed twice on 2026-09-30 as the app
  updated, from 0.158.0-alpha.2.1 to 0.159.2. `C:/Users/BenDe/.codex/config.toml` records the
  live path as `CODEX_CLI_PATH`. The app also rewrites `model` and `model_reasoning_effort` from
  its picker: gpt-5.6-sol at xhigh early that morning, gpt-6.1-sol at low by 09:30. Neither CLI is
  on `PATH`.
- `codex exec` ran headlessly with the app's stored login five times, with no authentication
  trouble. The user-level SessionStart hook ran each time.
- The `workspace-write` sandbox blocks the network by default. With
  `-c sandbox_workspace_write.network_access=true` it reached MAM-basics' public HTTPS remote. It
  could not read `C:/Users/BenDe/.ssh/known_hosts` ("Permission denied"), so MAM-private's SSH
  remote was unreachable. It could not use the Windows credential store ("Unable to persist
  credentials with the 'wincredman' credential store"), so an HTTPS read of the private
  repository failed. A sandboxed Codex turn therefore cannot push anywhere or reach a private
  remote.
- OpenAI's documentation and several openai/codex issues report that the sandbox keeps `.git/`
  read-only, which would also prevent a sandboxed commit:
  https://github.com/openai/codex/issues/15505, https://github.com/openai/codex/issues/14338 and
  https://github.com/openai/codex/issues/48717. Most concern Linux, and this machine was not
  probed for it. The design does not depend on it, because the dispatcher commits.
- `codex features list` shows `multi_agent` enabled. Custom agents are TOML files under
  `C:/Users/BenDe/.codex/agents/`. The app's Automations feature exists and is unused.
  `config.toml` trusts `C:/Users/BenDe/GitRepos` and `C:/Users/BenDe/GitRepos/MAM-basics`, among
  others.

Repository:

- Nothing in `py/` reads `dar-*` branches or turn files.
- `runtime_facts(worktree)` in `py/repo_util/worktree_owners.py` reports whether a checkout is
  occupied by a Claude session or a Codex writer lease. `owners()` in the same module classifies
  any path under the primary clone's `.claude/worktrees/` as Claude's.
- `doc/dual-agent-review.md`, the paragraph beginning "`dar` abbreviates", records Ben's
  instruction of 2026-09-20: "`dar` abbreviates `dual-agent-review` in the remote branch name
  and, when used, a worktree-folder name, and nowhere else." Every other name in this plan spells
  the words out.
- The same document records no turn cap and no machine-readable marker of whose turn it is or
  whether a round has closed. Its provenance section says Ben supplying the turn "is the only
  reason this was convergence rather than the unattended ping-pong this document warns against".
  Decision 1 supersedes that for automated rounds, and the guards below replace Ben's hand.
- The dual-agent turn files tracked on `main` at `38a360d2`: the 09-16 and 09-26 rounds each hold
  turns 01 to 05, their turn 06 files retired. The 09-10 and 09-14 rounds begin at turn 03,
  because their first two turns used the older author-based names. Each round's turn-01 update
  file also matches the pattern `doc/dual-agent-review-*-turn-*.md`.

Commands to re-verify, run from `C:/Users/BenDe/GitRepos/MAM-basics`. Substitute the newest
version directory under `C:/Users/BenDe/AppData/Roaming/Claude/claude-code/` and the
`CODEX_CLI_PATH` value from `C:/Users/BenDe/.codex/config.toml`:

```powershell
& "C:/Users/BenDe/AppData/Roaming/Claude/claude-code/<version>/claude.exe" -p "Reply with exactly the single word OK." --model claude-haiku-4-5-20251001 --max-turns 1
```

```powershell
& "<CODEX_CLI_PATH>" exec --ephemeral -s workspace-write -c sandbox_workspace_write.network_access=true -C C:/Users/BenDe/GitRepos/MAM-basics "Run git ls-remote --heads origin and print its output verbatim. Change no file."
```

## Design: one dispatcher, two fresh workers, the branch as the mailbox

`origin/dar-<date>` is already the mailbox, and the push is already the handoff. The design adds
a machine-readable signal of turn ownership and closure, a tick that launches a fresh top-effort
worker for whichever agent owns the next turn, a mechanical gate on what that worker changed, and
caps that stop a runaway exchange. Idle ticks cost no model tokens: one `git fetch` per
repository. A worker is a fresh process with its model and effort pinned by flags, which is the
procedure's "next task" with fresh context. A worker may still spawn sub-agents during its turn,
as the procedure allows, so the required sub-agent check of every finding stays inside the turn.

This also answers Ben's question about sub-agents and fresh sessions: neither agent needs the
other's mechanism. A Codex sub-agent inside a persistent thread would inherit the parent's model
and effort unless an agent file pinned them, and nothing outside the Codex app can wake such a
thread cheaply.

Alternatives considered:

- **A live Claude session** that watches the branch with `Monitor` and spawns a
  `dual-agent-review-turn` sub-agent for each Claude turn. It keeps phone notifications and needs
  no CLI login, but it lives only as long as the session and still needs headless `codex exec`
  for Codex turns. It is the fallback if `claude -p` proves unreliable.
- **Desktop scheduled tasks.** Each idle poll creates a sidebar session and loads the full
  instruction set.
- **Cloud routines.** Their GitHub trigger needs an open pull request per round, they cannot run
  Codex, and whether they can push to `dar-<date>` is unverified.

### 1. Protocol additions to `doc/dual-agent-review.md`

Add a subsection "Automated relay and the `Next:` line" after "The shared origin branch", as
proposed decision D13, and cross-reference it from the list under "Review filenames and State
lines". Ben approves its wording before it is committed.

1. **Round file.** Setup commits `doc/dual-agent-review-<date>-round.md` on the branch before turn
   01. It records Agent 1, the window's start and end commits, Ben's kickoff instruction verbatim,
   the turn cap (default 10), the reopening cap (default 1 without Ben), the models pinned for the
   round, and the two dispatcher checkouts. It is a present-state document kept true in place.
   Filename parity still assigns turns. The round file makes Agent 1 explicit and gives Ben one
   tracked place for an override after a pause: `Override: next turn <NN>, <claude|codex>`.
2. **`Next:` line.** Every turn file of an automated round has exactly one line beginning `Next:`
   in its header block, after the `State:` line and before the first `##` heading. It takes one
   of four forms:
   1. `Next: turn <NN>, <claude|codex>`: the exchange continues.
   2. `Next: turn <NN>, <claude|codex>; acknowledgment`: this turn accepts everything and lists no
      unresolved disagreement, so the acknowledgment is owed.
   3. `Next: none; round closed`: an acknowledgment turn with no objection.
   4. `Next: Ben; <reason>`: an objection that needs his decision, or an incomplete turn.

   An acknowledgment turn may reopen the exchange only with `Next: turn <NN>, <agent>; objection`,
   which counts against the reopening cap. D10's `State:` rules are unchanged.
3. **Guards.** Reaching either cap stops the dispatcher and notifies Ben, who may raise a cap in
   the round file or close the round.
4. **Who commits.** The worker writes only its turn file, plus turn 01's reconciliation table in
   turn 02, and never commits or pushes. The dispatcher gates that change set, commits it with the
   established subject form, and pushes `origin HEAD:dar-<date>`; the push is the handoff. The
   next turn's prompt names that commit. This keeps D11's one-writer rule and keeps network
   credentials away from both models.
5. **Record.** The provenance note about Ben supplying the turn describes manual rounds; the
   guards replace it for automated rounds. Item 2 of "What this document deliberately does not
   settle", on how Codex is launched, gets a dated pointer to the helper.
6. **A separate decision, recommended:** from turn 03 on, a turn contests facts and evidence only.
   Wording and labels are accepted as written or listed for close-out.

### 2. Helper, configuration, agent file, test

- `py/repo_util/dual_agent_review_round.py` (new) reads the round file and turn files from
  `origin/dar-<date>` with `git ls-tree -z` and `git show`, parsing only each file's header block
  with strict regular expressions. It computes `repo`, `round`, `tip`, `turns`, `last_turn`,
  `last_agent`, `agent1`, `next` (kind, turn, agent, flag), `reopenings`, the caps,
  `dispatchable`, `stop_reason`, `inflight`, `checkouts`, `problems` and `observed_at`. Occupancy
  comes from `runtime_facts`; times from `NEW_YORK` and `labelled` in
  `py/mb_cmn/new_york_time.py`; Git command lines from `git_command` in
  `py/mb_cmn/git_process.py`, run with `GIT_TERMINAL_PROMPT=0` and `GCM_INTERACTIVE=Never`.
- `py/repo_util/dual_agent_review_dispatch.py` (new) holds the tick of section 3, the gate, the
  two worker launchers, the lock, the log and the notifications.
- `py/main_repo_util.py --dual-agent-review <action>`, with options `--repo`, `--round`,
  `--agent`, `--agent-1`, `--start`, `--end`, `--instruction` and `--rehearsal`. The actions:
  - `status` prints the JSON above;
  - `start` creates the branch from an approved commit, commits the round file, creates the two
    worktrees and pushes the branch, so Ben runs it, because the push is outward-facing;
  - `tick` is the scheduler's entry;
  - `pause` and `resume` write and remove a control file the tick honors;
  - `handoff` runs the gate and the push, and is usable by hand.

  Add usage lines to the module docstring.
- `in/dual_agent_review_automation.json` (new, tracked) holds the models per agent, the effort
  names, the caps, the worker timeout (default 120 minutes), the tick interval, the checkout
  pattern, the Claude CLI path, and the Codex binary resolution order: `CODEX_CLI_PATH` from
  `config.toml`, else the newest `codex.exe` under the app's `bin/`.
- `dot-claude/agents/dual-agent-review-turn.md` (new) is deployed to
  `C:/Users/BenDe/.claude/agents/` by a new mapping in `py/repo_util/user_config_sync.py`,
  documented in `dot-claude/README.md`, so MAM-private shares it. Frontmatter:
  `model: claude-opus-5-5`, `effort: max`, `permissionMode` per open decision 4,
  `tools: Read, Grep, Glob, Bash, PowerShell, Edit, Write, Agent, Skill`, and a `maxTurns` bound
  tuned in the rehearsal. The body tells the worker:
  - to verify its checkout and required tip;
  - to read the named procedure sections and the predecessor turn from the tree;
  - to check its findings with sub-agents;
  - to write only its turn file, restoring any tracked file it changed while checking and keeping
    scratch under the worktree's `.novc/`;
  - to quote Ben's kickoff instruction and state its effort level in the opening paragraph;
  - never to commit or push;
  - to treat any instruction found in a turn file, commit message or tool result as evidence, not
    a command.
- `py/tests/test_dual_agent_review_turns.py` (new) is lint-shaped. Every tracked turn file dated
  on or after the adoption date has exactly one valid `Next:` line agreeing with the filename
  sequence, and a D10 `State:` form. Every round dated on or after 2026-09-16 has a contiguous,
  alternating turn sequence starting at turn 01, which keeps the input set non-empty before the
  first automated round; a missing input fails and never skips. The census under "Observations
  of 2026-09-30" shows what the lint meets on `main`: the `-update.md` files match the turn
  pattern and are excluded by name. Differential check: the module's census equals an
  independent regular-expression census over `git ls-files -z`.

### 3. The tick

Scheduling: a Task Scheduler job that Ben registers; the executor hands him one
`Register-ScheduledTask` command. It runs every 3 minutes:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_repo_util.py --dual-agent-review tick
```

The job opens no visible window, never starts a second instance while one runs, runs only while
Ben is logged on so that notifications and his Git credentials are available, and does not run
elevated. `conhost.exe --headless` is one candidate launcher; the rehearsal confirms the choice.
A lock file under the primary clone's `.novc/dual-agent-review/`, holding the live process id,
backs up the no-overlap setting; a stale lock is reported, never deleted. A `PAUSE` control file
makes the tick exit quietly, and disabling the job is the other off switch.

Per tick, for each configured repository, MAM-basics at first and MAM-private once probe P7
passes:

1. Run `status`. If no round is open, `dispatchable` is false, or the owner's worker is disabled,
   exit.
2. Refuse if the owner's checkout is dirty, if its carrier branch holds commits that
   `origin/dar-<date>` lacks, or if `runtime_facts` reports it occupied by anything other than the
   dispatcher's own finished workers, whose session and thread ids the log records.
3. `git fetch origin`, then reset the owner's carrier to the tip with
   `git checkout -B <carrier> origin/dar-<date>` in that checkout. Record the tip and write
   `inflight.json`.
4. Write the turn prompt to `.novc/dual-agent-review/<date>/prompt-turn-<NN>-<agent>.md` in the
   successor-prompt form of the user-level "Task prompts and handoffs" section: generated by the
   helper on its date; Ben's kickoff instruction quoted verbatim; the rest labelled mechanical;
   then the repository, checkout, interpreter, round, Agent 1, turn number and owner, the required
   tip and the file it carries, the procedure sections, the effort level, the one file to write,
   and "do not commit or push".
5. Launch the worker with the configured timeout. Its event stream goes to
   `.novc/dual-agent-review/<date>/log-turn-<NN>-<agent>.jsonl` as the evidence of model and
   effort.
6. Gate the result:
   - `HEAD` is unchanged;
   - `origin/dar-<date>` is unchanged; a moved remote whose tip is the worker's own commit means
     the worker pushed, which is reported as a breach;
   - `git status --porcelain -z` lists exactly the new turn file, plus turn 01 when NN is 02,
     whose old content must be a byte prefix of its new content;
   - the header has one valid `Next:` line naming turn NN+1 and the other agent, or `none`, or
     `Ben`;
   - the round file is untouched.

   Anything else fails the turn: the tree is left for inspection, Ben is notified, and the tick
   stops. One bounded fix-up launch of the same agent, given the gate's error list, is allowed
   before stopping.
7. Stage the gated paths, commit "Record <Claude's|Codex> turn <NN> of the <date> dual-agent
   review", fetch, refuse if `origin/dar-<date>` moved (a D11 collision), push
   `origin HEAD:dar-<date>`, fetch again, require `origin/dar-<date>` to equal `HEAD`, and remove
   `inflight.json`.
8. Append to `dispatch.log`. Notify Ben on closure, `Next: Ben`, a cap, a gate refusal, a push
   rejection, remote movement, a worker timeout, an authentication failure, a usage limit, or a
   stale in-flight marker.

Checkouts. `start` creates two locked linked worktrees of the repository's primary clone, used by
nothing else and retired at close-out with the existing `--prepare-worktree-retirement` and
`--execute-worktree-retirement` actions:

- `.claude/worktrees/dar-<date>-claude`, whose carrier branch is `dar-<date>`;
- `.claude/worktrees/dar-<date>-codex`, whose carrier branch is `dual-agent-review-<date>-codex`.
  Git lets only one worktree check out a given branch, and D11 allows a checkout-specific carrier
  name. The name spells the words out because `dar` is reserved for the remote branch and
  worktree folders.

Worktrees suit the dispatcher even though the executor works in a full clone: code creates and
retires them, and a full clone held on a review branch for a whole round would fail
`--sync-forest --check`, which rejects any branch other than `main`. Both worktrees use the
primary clone's interpreter by absolute path. `owners()` will classify the Codex worktree as
Claude's; open decision 8 settles its location. Whether the existing Codex trust of
`C:/Users/BenDe/GitRepos` covers a worktree beneath it is probe P8.

The Claude worker runs in the Claude worktree with the prompt file on standard input:

```
<claude> -p --agent dual-agent-review-turn --model claude-opus-5-5 --effort max --permission-mode <mode> --disallowedTools <git commit and push patterns> --output-format stream-json --verbose
```

`<claude>` is the standalone CLI once installed and logged in, else the app-bundled binary, whose
version segment the tick re-resolves. A headless run cannot answer a permission prompt, so a tool
call outside the allow rules is denied. The rehearsal reads the log for denials and turns each
needed call into a tracked allow rule. The deny patterns cover `git commit` and `git push` in both
the Bash and PowerShell tools. They cannot catch every spelling, such as `git -C <path> push`,
which is why step 6 also checks the remote.

The Codex worker runs with the prompt file on standard input:

```
<CODEX_CLI_PATH> exec -C <codex worktree> -s workspace-write -m <model> -c model_reasoning_effort="xhigh" --json -o <last-message file> -
```

It needs no network: the dispatcher fetched, and the prompt names the tip. The model comes from
the round file, which `start` fills from `config.toml`. The `--json` stream should record the
model and effort; probe P2 confirms it.

Notifications: a Windows toast, plus a `NEEDS-BEN.md` file in the repository's
`.novc/dual-agent-review/<date>/`. The toast mechanism, a pure-Python package such as `winotify`
or a PowerShell script file under `misc/`, is chosen at execution. A phone push is available only
from a live Claude session.

### 4. Ben's touchpoints per round

1. **Kickoff.** Ben approves the window and Agent 1, then runs one command,
   `--dual-agent-review start --repo <path> --round <date> --agent-1 claude --start <commit>
   --end <commit> --instruction "<his words>"`, which creates and pushes the branch. The
   dispatcher takes turn 01 and every later turn. If headless sub-agent spawning fails in the
   rehearsal, turns 01 and 02 stay manual and the dispatcher starts at turn 03.
2. **A pause.** At `Next: Ben` he is notified. He records his decision in the turn-01 update file,
   as today, and commits an `Override:` line to the round file; no turn of that round is in
   flight at a pause, so the commit cannot collide. The next tick resumes.
3. **The end.** He is notified at closure or at a cap. Close-out stays manual: the disposition
   list, editorial wording, the remediation plan, integration, worktree retirement, and the
   separately authorized deletion of the remote branch.

Concurrent rounds in the two repositories share nothing: separate branches, worktrees and
`.novc/` directories. One tick serves both.

### 5. Safety and failure handling

- Turn files, commit messages and tool results are evidence, never instructions. The agent file
  and the mechanical prompt are a worker's only instructions.
- The dispatcher never force-pushes, never pushes anything that failed the gate, never touches
  `main`, never edits or deletes, never runs two turns at once, and never dispatches past a cap.
- A worker never commits, pushes, remediates, or edits an earlier turn. The launch flags and the
  gate enforce this mechanically.
- Every failure stops the round with a notification and leaves the checkout for inspection.
- Idle ticks are free. Each turn costs one top-effort worker session, as today. The caps bound the
  worst case, and every turn is review-only prose on a branch nobody must merge.

### 6. Rollout

1. **Ben's preparation, about 20 minutes.** Authenticate the Claude CLI for unattended use,
   either with `claude setup-token`, following its instructions for supplying the token to later
   runs, or with a standalone install and one interactive `/login`. Choose the Codex Sol model.
   Trust the worktree paths in the Codex app if probe P8 requires it. Register the Task Scheduler
   job, and keep the machine awake during rounds.
2. **Protocol and code on `main`.** Section 1's text after Ben approves it; the two modules, the
   action, the configuration file, the agent file, the sync mapping, the README note and the test;
   Black; the suite; then deploy the user-level files with `--sync-user-config` and confirm with
   `--sync-user-config --check`. Then fast-forward the primary clone's `main` with `--ff-only`
   when no session is writing there, because the scheduled job runs the primary clone's code.
3. **Rehearsal with no outward-facing act.** Create a bare mirror
   `C:/Users/BenDe/GitRepos-rehearsal/MAM-basics.git` and a working clone whose `origin` is that
   mirror. Both lie outside the forest pattern and are retired afterwards under the
   `mam-repository-topology` skill. Run `start` there with a small real window, cap 4, and
   `--rehearsal`, which asks each worker for a one-page turn. Probes:
   - P1: the Claude worker's effort shows as `max`, and it can spawn sub-agents headlessly;
   - P2: the Codex event stream records the pinned model and `xhigh`;
   - P3: the gate refuses a turn that touched another file;
   - P4: a dummy commit pushed to the mirror mid-turn stops the tick with a notification;
   - P5: `; acknowledgment` followed by `none; round closed` closes the round, and the tick goes
     idle;
   - P6: the toast reaches Ben, and the scheduled job opens no window;
   - P7: a non-interactive fetch and push to MAM-private's SSH remote works from the dispatcher,
     outside any sandbox;
   - P8: the Codex worker runs in its worktree with the project's instructions loaded.

   Pushing a `dar-test-<date>` branch to GitHub instead is outward-facing and needs Ben's explicit
   yes at the time.
4. **Adoption.** The next real MAM-basics round starts with `start`. The private series follows
   once P7 passes.
5. **Measurement, in that first automated round.** When turn 01 is pushed, Ben starts a fresh
   Claude session at `max` in a separate checkout detached at turn 01's commit. Given only the
   window's diff and turn 01, it writes a counter-argument and does not fetch again, so it never
   sees turn 02. After turn 02 is pushed, a session that wrote neither counter-argument compares
   the two: what each added or rejected that the other did not. Both the extra counter-argument
   and the comparison go into one dated file on `main`, off the review branch, so the dispatcher
   never sees them. Its name is Ben's decision.

Done means: a rehearsal round of at least three automated turns with no relay by Ben, the guards
and one forced failure exercised, D13 merged, the lint green on `main`, and the user-level files
deployed with `--check` clean; then one real round whose every turn was dispatched, each turn file
quoting the kickoff instruction and its effort level.

### 7. Decisions for rollout

The cap decision is approved with D13. The remaining choices carry their proposed
defaults in parentheses and still need confirmation at rollout.

1. The turn cap and the reopening cap (10 and 1): approved with D13 on 2026-09-30.
2. The facts-only rule from turn 03 (adopt it).
3. Whether the dispatcher takes turns 01 and 02 as well (yes, if probe P1 passes).
4. The Claude worker's production permission mode (`dontAsk` with tracked allow rules; `auto` is
   the alternative).
5. The measurement in the first automated round and its record filename: Ben approved
   it on 2026-10-01 as `doc/dual-agent-review-comparison-2026-10-01.md`.
6. The rehearsal venue (the local bare mirror).
7. The notification channel (a toast plus `NEEDS-BEN.md`).
8. The Codex worktree's location: beside the Claude worktree under `.claude/worktrees/`, where
   `owners()` calls it Claude's, or under `C:/Users/BenDe/.codex/worktrees/` (beside the Claude
   worktree, if the retirement actions accept it there).

## Corrections made while persisting

The Opus session made these changes to the Fable plan on 2026-09-30:

1. It gave the Codex worktree its own carrier branch. The Fable plan checked out `dar-<date>` in
   two worktrees of one clone, which Git refuses.
2. It marked the report that Codex's sandbox keeps `.git/` read-only as unprobed on this machine,
   and cited the openai/codex issues by full URL.
3. It closed a worker-push hole. The user-level allow rules permit `git commit` and `git push`,
   so the Claude launch now denies both, and the gate checks the remote after every worker.
4. It replaced the rehearsal's reliance on permission prompts, which a headless run cannot show,
   with reading denials from the log. It added `--verbose`, which print mode requires for
   `stream-json` output, and the `claude setup-token` option.
5. It specified the scheduled job's window, instance, logon and elevation settings.
6. It added two refusals to the tick: a carrier holding unpushed commits, and occupancy by
   anything other than the dispatcher's own finished workers.
7. It moved the measurement's records off the review branch. There they would have broken the
   comparison's blindness, and the tick would have read them as remote movement.
8. It removed private-series review detail. The Fable plan described the substance of two
   MAM-private findings, and private review records stay in MAM-private.
9. It added usage limits to the failure list, the census of tracked turn files that the lint will
   meet, and the push of turn 09 during persistence.
