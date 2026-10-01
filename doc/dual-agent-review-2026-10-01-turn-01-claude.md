# Findings of the 2026-10-01 automated review of MAM-basics' relay implementation window

State: not yet acted on
Updates and later status: [dual-agent-review-2026-10-01-turn-01-claude-update.md](dual-agent-review-2026-10-01-turn-01-claude-update.md).
Next: turn 02, codex

Claude Opus 5.5 (`claude-opus-5-5`), running at `max` effort, wrote this turn as turn 01 of the
automated round recorded in `doc/dual-agent-review-2026-10-01-round.md`, with Claude as Agent 1.
Ben's kickoff instruction, verbatim: "Run the first automated MAM-basics review of the relay
implementation window with Claude as Agent 1." The dispatcher generated this worker's mechanical
prompt at 2026-10-01T11:11:19.881802-04:00, New York time, and launched the worker in
`C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-2026-10-01-claude` on carrier
`dar-2026-10-01` at `ef133e4dc79de069229754ee8dc8d5fc59b3e812`, the round's setup commit. The
worker verified that checkout's root, `HEAD`, carrier and clean status before reading. It wrote
only this file and two scratch files under the ignored `.novc/dar-turn01-scratch/`, and it leaves
staging, the commit and the push to the dispatcher under D13.

**How the turn was checked.** The worker read the whole endpoint diff and the procedure sections
the prompt names. Ten read-only sub-agents then checked the findings in the foreground, and all
ten had finished before this file was written. Eight ran in a first wave: six checked the
findings in groups, one recounted the census and the stream-by-stream claims, and one swept the
two new Python modules for omissions. Two ran in a second wave and checked the three defects the
sweep found, together with a notification defect the registry checker found. Each finding below
names the corrections it adopted. The worker rejected one sweep candidate, that Codex workers
might lose their Git trust entry from the environment, because the runbook,
`doc/dual-agent-review-automation.md`, records in probe P8 two real Codex turns whose native Git
reads succeeded.

**A departure from the usual review shape.** `doc/periodic-review.md`, "What a review file
contains", has the H1 name a periodic window by the previous review's date. This round is instead
a bounded rollout review of the relay that dispatched it: the runbook's post-window entry
"Production readiness recheck, 2026-10-01" records that the periodic series' carried-forward
anchor is unchanged, so this H1 names the window by its subject. The window contains no prior
round's own records. All 15 paths are the relay's protocol text, plan, runbook, configuration,
scripts, code and tests, and this turn reads every one of them as subject. Post-window revisions
of the plan, `doc/PLAN-automate-the-dual-agent-review-relay.md`, and of the runbook are used only
as evidence, and are named as such where used. This worker is itself a product of the reviewed
code, so its prompt and permissions are evidence of that code's behaviour; each finding says when
it relies on them.

**Product reach and dispositions.** No path in the window reaches `gh-pages/`, a `MAM-*` product
directory or a step of `py/main_0_mega.py`. Under Ben's ordering of remediation by public-facing
risk, every finding falls in "All remaining changes — lower risk": agent tooling, code, tests and
internal documents. Every finding is unfixed, because a review turn performs no remediation, and
each concerns content introduced in the window unless its text says otherwise.

## Scope, anchors and census

The window is MAM-basics
`303bf2399c1e1fc1300a75f4fb1ed335d62984d0..1bfceff4d952470618fc7584a6bca4fc5c9b2f5f`, the
endpoints recorded in the round file; the start is an ancestor of the end. The range holds nine
commits, none a merge, all committed on 2026-09-30 between 17:09:20 and 22:27:18, New York time,
under Ben Denckla's Git identity. The plan and the runbook record Codex as the implementing agent.
`1a50d4b6` added the relay. `38f1b573` adopted D13. `05e109cf`, `42cb46a9`, `a92b2ebe` and
`a13f1eab` fixed worker permissions and header parsing. `9988db8e` and `0f745369` recorded
verification, and `1bfceff4` fixed the notification sender and enabled production.

The endpoint diff changes 15 paths, 9 added and 6 modified, with 2,506 insertions and 34
deletions:

| Kind | Added | Modified |
|---|---|---|
| Python | `py/repo_util/dual_agent_review_dispatch.py` (1,066 lines), `py/repo_util/dual_agent_review_round.py` (356), `py/tests/test_dual_agent_review_dispatch.py` (277), `py/tests/test_dual_agent_review_turns.py` (154) | `py/main_repo_util.py`, `py/repo_util/user_config_sync.py` |
| Markdown | `doc/dual-agent-review-automation.md`, `dot-claude/agents/dual-agent-review-turn.md` | `doc/PLAN-automate-the-dual-agent-review-relay.md`, `doc/dual-agent-review.md`, `doc/periodic-review.md`, `dot-claude/README.md` |
| JSON | `in/dual_agent_review_automation.json` | none |
| PowerShell | `misc/dual-agent-review-toast.ps1`, `misc/register-dual-agent-review-task.ps1` | none |

This turn calls `py/repo_util/dual_agent_review_dispatch.py` the dispatcher,
`py/repo_util/dual_agent_review_round.py` the protocol module, the dispatcher's `gate()` the gate,
`in/dual_agent_review_automation.json` the configuration,
`dot-claude/agents/dual-agent-review-turn.md` the agent file, and a round's `inflight.json` the
marker. Bare line numbers cite the dispatcher; other files are named. The dispatcher, the
protocol module, both test modules, `py/repo_util/user_config_sync.py`, the configuration, both
scripts and the agent file are byte-identical at `ef133e4d` and at the window end, and
`py/main_repo_util.py` differs only in its module docstring, so line numbers hold at both.
Documents are cited as of the window end, by section and quoted passage.

## Tree health at `1bfceff4`

1. **The suite, the two relay test modules and Black were not run**, because this worker's
   permissions refuse the interpreter; finding 3 records the evidence.
2. **Whitespace:** `git diff --check` between the two endpoints printed nothing, so the window
   introduces no whitespace error.
3. **Recorded results, not re-run:** the runbook records "The targeted checks passed 4 tests; the
   final full suite passed 1015 tests, with 5 skips and 60 subtests, using `py/main_test.py -q`",
   then the same counts after the notification fix with one warning about pytest's cache. After
   the window, its "Production readiness recheck, 2026-10-01" records "4 passed" for the two relay
   test modules at `61fa3d1d`. The two modules define exactly four test functions, so the counts
   are consistent. The runs themselves rest on untracked receipts that this turn did not read.

## What verifies sound, stream by stream

1. **Protocol parsing against D13.** The protocol module reads only a turn's header block, the
   lines before its first `## ` heading (protocol module 83-117), so a quotation in a body cannot
   change control state. It accepts exactly D13's five forms after the line-3 `State:`, enforces
   D10's State forms, and requires a contiguous sequence from turn 01 with Agent 1's parity. It
   consumes an `Override:` once the named turn exists (protocol module 284-308 and 325-333), and
   applies the caps of 10 turns and 1 reopening so that the first reopening proceeds, a second
   stops dispatch and turn 11 is never dispatched (protocol module 313 and 341-344). The round
   file's example line beginning `Override:` sits below `## Control`, so it cannot act as an
   override. The transition oracle iterates 2 × 10 × 2 × 5 × 4 × 4 = 3,200 combinations, the
   runbook's figure.
2. **Setup.** `start()` refuses unless the named path is a full clone on clean `main` with no
   occupying session, exactly one fetch URL and one push URL, a start commit that is an ancestor
   of the end commit, an end commit contained in `HEAD`, and a Sol model in Codex's configuration.
   It refuses an existing remote branch, carrier, worktree or round control directory before
   creating anything (359-419), checks the remote again before pushing the setup commit, verifies
   the pushed tip, and registers the round only after that verification (460-468).
3. **Dispatch and the gate.** A carrier moves only by a verified `--ff-only` merge (896-898). The
   gate compares origin URL identity before any outbound query, then checks `HEAD`, the carrier,
   the live remote tip, staged files, status record kinds, the exact path set, a symlinked output,
   the header transition, and turn 01's byte prefix (659-743). Its cross-check that line-ending
   normalization is the only clean-filter change matches `.gitattributes`' `* text=auto eol=lf`.
4. **Handoff.** The dispatcher records the approved tree before committing; verifies the commit's
   parent, tree and subject; pushes only from the expected remote tip, or recognizes a push that
   already landed; verifies the pushed tip; writes a receipt; and removes the marker last
   (746-838). The differential test forces a push failure and recovers the approved commit by a
   manual handoff (`py/tests/test_dual_agent_review_dispatch.py` 137-175).
5. **Repository conventions.** Every Git call in the two modules that returns a list of filenames
   uses `-z` and splits on NUL. All seven clock reads use `datetime.now(NEW_YORK)`, and displayed
   times use `labelled()`. Git trust is the exact-path `safe.directory` from `git_command`, passed
   to workers through `add_windows_safe_directory`. Nothing changes `sys.path`. The new actions
   are a subcommand of the existing entry point, with usage lines in its docstring, and review
   options are refused outside `--dual-agent-review`.
6. **Deployment.** `py/repo_util/user_config_sync.py` archives the agent file, maps it to
   `~/.claude/agents/dual-agent-review-turn.md`, and now requires the source of every mapping that
   is not of kind `absent`; `dot-claude/README.md` documents the new row.
7. **Procedure text.** The window's edits to D9, D11, "Review filenames and State lines" and
   `doc/periodic-review.md` consistently separate manual mechanics from D13's automated ones. D13
   entered `doc/dual-agent-review.md` in `38f1b573`, and the runbook and the plan record Ben's
   "I approve" of 2026-09-30.
8. **The runbook's own descriptions.** Its "4 tests" and "3,200" match the code, and its accounts
   of command-line discovery, `pause` and `resume`, status without fetching, and registry-only
   ticks match the dispatcher.

## Findings

### 1. A turn 02 that stops with `Next: Ben` cannot be handed off without an append to turn 01

**Unfixed.** A defect in new code. It bites only an incomplete turn 02, which in this round is
Codex's.

- For turn 02, the gate's permitted path set is the new turn plus turn 01, and any other set is
  refused (691-700). The protocol module's `validate_turn` and `status()` both accept a turn 02
  that stops for Ben, so only this path-set rule refuses it.
- D13 says the Ben form "stops for a decision or an incomplete turn". The agent file says "If
  blocked, report Next: Ben; with the reason." The prompt offers every turn, turn 02 included,
  "Need a decision or unable to finish: Next: Ben; concrete reason" (529).
- A blocked turn 02 that writes only its own file is refused with "change set must be exactly the
  new turn and, for turn 02, the reconciliation append". That message holds none of the fix-up
  tokens, so the round pauses (926-944 and 956-958), and a manual `handoff` runs the same gate
  and is refused again (768-771).
- The stop can then reach the remote only through an append to turn 01, which D9 reserves for
  Agent 2's reconciliation "once the turn is stable", or through a hand commit outside the
  dispatcher. No window document tells a blocked turn 02 to append anyway, and the dispatch
  test's turn 02 always appends (`py/tests/test_dual_agent_review_dispatch.py` 119-127).
- The omissions sweep found this. A second-wave checker confirmed each step and added that a
  completed turn 02 stopping for a decision would normally carry the append already.

### 2. A failure that recurs after `resume` pauses the round again without notifying Ben

**Unfixed.** A defect in new code.

- `notify()` returns before writing `NEEDS-BEN.md` or showing a toast when
  `last-notification.json` already holds the same reason and cached remote tip (149-157). Only
  `notify()` writes that file, and `resume` removes only `PAUSE` (1025-1035).
- `tick_round`'s two failure handlers write `PAUSE` and then call `notify()` (867-872 and
  950-958). Suppose a worker exits non-zero for a usage limit, with the fixed text "worker exited
  N; inspect log for authentication, permission, or usage failure" (642-645). Ben removes the
  marker by hand, as `resume` requires, and resumes. If the same failure recurs at the same tip,
  `PAUSE` is written again but no notice appears, and the round stops silently.
- Every other fixed-text failure behaves the same: a timeout (639-641), a stream without a
  successful terminal event (656), a dirty checkout (895) and a gate refusal (944). A fetch
  failure is suppressed only when Git's error text repeats exactly.
- The plan's "5. Safety and failure handling", written before the window, says "Every failure
  stops the round with a notification". The implementation does so only for the first occurrence
  at a given tip.
- The omissions sweep found this. A second-wave checker confirmed it and widened it from the
  usage-limit case to every fixed-text failure.

### 3. The Claude worker cannot run the interpreter that the review procedure's checks need

**Unfixed; raised for Ben's judgment.** The permission design is new in the window; the procedure
it conflicts with predates the window.

- The configuration sets `claude_permission_mode` to `dontAsk` (line 11). Its
  `claude_allowed_tools` (line 17) holds Read, Grep, Glob, Edit, Write, Agent and Skill plus Git
  read rules, and `worker_command` adds only per-checkout Git read rules built from
  `READ_ONLY_GIT`, then denies Bash on Windows (26-41 and 545-559). No rule names an interpreter,
  a test runner or a script. The plan's "3. The tick" states the consequence: "A headless run
  cannot answer a permission prompt, so a tool call outside the allow rules is denied."
- This worker's one attempt to run the two relay test modules was refused with "Permission to use
  PowerShell has been denied because Claude Code is running in don't ask mode". The command was
  `C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe py/main_test.py py/tests/test_dual_agent_review_turns.py py/tests/test_dual_agent_review_dispatch.py -q`.
  A checker's one attempt at `python.exe --version` met the same refusal, so sub-agents share the
  restriction. Any later Claude worker can repeat either command.
- `doc/periodic-review.md` has the checking sub-agent rerun "the scripts the finding cites"
  ("Reviewing the review, with the same agent and with Ben", item 1), and its "What a review file
  contains", item 5, gives a review "the suite's count and the lints" under a tree-health heading.
  The prompt nevertheless gives every worker an "Interpreter:" line (495). The plan's "3. The
  tick", written before the window, has the prompt name the interpreter and has both worktrees
  use the primary clone's interpreter by absolute path.
- The Codex worker runs under `codex exec -s workspace-write` with network access disabled
  (584-601), a different capability model. No window document says whether it can run the suite,
  and this turn did not check. No window document says that the Claude worker cannot.

### 4. Mechanical limits on the Claude worker cover only its checkout and the round's branch

**Unfixed; a design limitation raised for Ben's judgment.**

- The gate inspects only the worker checkout's index, status, `HEAD` and carrier, the round's
  remote branch, the origin URLs, the turn header and turn 01's prefix (659-743). Ignored paths
  inside the checkout are not inspected, as `.novc/` scratch requires.
- The Claude launch limits shell use to the listed Git subcommands. It limits neither Edit and
  Write paths, which the configuration grants with no path (line 17), nor those subcommands'
  options that write files or run programs. Every generated Git rule ends in a wildcard after the
  subcommand (551), as do the configuration's generic rules, and the comment at 542-543 promises
  only that no middle wildcard grants options before it. Git for Windows' installed documentation
  describes `--output=<file>` for `diff`, `log` and `show`; `-O[<pager>]` for `grep`, which opens
  the matching files in a pager program; `-w` for `hash-object`, which writes an object; and the
  two-argument form of `symbolic-ref`, which updates a ref.
- Outside the checkout lie the home clone's working tree and the round's control directory, from
  which `handoff()` re-reads the marker (747-748). The gate would not see a write there, or a
  push to another branch by a launched program.
- The plan's "5. Safety and failure handling" says "The launch flags and the gate enforce this
  mechanically". That sentence predates the window. The window's list of superseding mechanics
  does not narrow that sentence, and the list calls the rules "ordinary Git reads". D13 claims
  only the checks the gate makes.
- Whether the Claude CLI's own working-directory boundary or command parsing refuses these forms
  was deliberately not tested, and no window document records such a test. The Codex worker's
  sandbox is a separate limit that this turn did not examine.
- A first-wave checker confirmed the documentation by reading it and supplied the narrowed
  wording adopted here.

### 5. A new turn file's whitespace is checked only after the dispatcher stages it

**Unfixed.** A defect in new code.

- The gate's `git diff --check` (740-742) compares the working tree with the index, so it never
  examines the untracked new turn file. `handoff()` first stages the owned paths and only then
  runs `git diff --cached --check`, before it records the approved tree (775-778).
- Git writes `--check` reports to standard output, and the gate itself reads `check.stdout`.
  `protocol.git` builds its error from standard error alone (protocol module 37-38), so this
  refusal's reason is empty. This worker confirmed the stream with a two-file
  `git diff --no-index --check`, one file holding a line with a trailing space and a final blank
  line: with standard error discarded, both reports still printed, and the command exited 3.
- A retried `handoff` finds no approved tree and runs the gate again, which reports "worker staged
  files", "unexpected status entry …" for the added record, and "change set must be exactly …".
  `resume` refuses while the marker exists, so only unstaging by hand recovers. The runbook's
  "The handoff action resumes a dispatcher-approved index or commit idempotently" does not cover
  this staged but unapproved state.
- Git enables `blank-at-eol` and `blank-at-eof` by default, and `.gitattributes` sets no
  whitespace rule for `doc/*.md`, so a Markdown hard line break or a final blank line is enough.
  Under `eol=lf`, CRLF line endings alone are not. No test covers this path.
- The first-wave checker corrected one implication, adopted here. Whitespace errors are not
  eligible for the fix-up, so an earlier check would gain an informative refusal before anything
  is staged, not a fix-up.

### 6. Several refusals carry an empty or uninformative reason

**Unfixed.** A defect in new code.

1. `start()` checks ancestry twice (397-398) and `tick_round` once (896) with
   `git merge-base --is-ancestor`, which exits 1 with no output when the answer is no. This
   worker's `git merge-base --is-ancestor` of the window end against its start showed exactly
   that. `start` then prints "Dual-agent review action refused: " and nothing more (1065). A tick
   writes a `PAUSE` file holding only a newline, and a `NEEDS-BEN.md` and toast whose reason is
   empty (956-957). Under the scheduler's `pythonw.exe`, the refusal line itself goes to
   `.novc/dual-agent-review/scheduler.log`. At line 896, the notice's standing advice to inspect
   the marker and launch records points to files not yet written (913-922).
2. Finding 5's `git diff --cached --check` refusal has the same empty reason. So would `start`'s
   check of the generated round file (436), though that check is unlikely to fail.
3. `rev-parse --verify` (393-396) reports "fatal: Needed a single revision" without saying whether
   the start or the end commit is the bad one.

### 7. Re-dispatching a turn overwrites the earlier attempt's records

**Unfixed.** A defect in new code, against the module docstring's promise to "preserve every
refused turn for inspection".

- A re-dispatch of the same turn and agent rewrites `prompt-turn-NN-<agent>.md` (901) and
  `launch-turn-NN-<agent>.json` (914-922). It truncates `log-turn-NN-<agent>.jsonl` and
  `fixup-turn-NN-<agent>.jsonl`, both of which `launch_worker` opens with mode `"wb"` (613, 923
  and 940). The Codex worker's `-o` target is one `last-message.txt` per round directory
  (598-599), which each Codex launch names as its output, a fix-up and later Codex turns
  included.
- Re-dispatch is an ordinary path: after a failure Ben removes the marker by hand and resumes,
  and the next tick launches the same turn and agent.
- The runbook shows the gap worked around by hand during the rehearsal: "The original marker and
  log are preserved before recovery", and "The timeout files are preserved with
  `-twenty-minute-timeout` names and `timeout-recovery.json`".
- A second-wave checker narrowed the claim, and this turn adopts the narrowing. The refused turn
  file and its marker are never overwritten while the marker stands. A later re-dispatch replaces
  the attempt record: the prompt, launch record, worker log and fix-up log.

### 8. Notices after a stop are duplicated and outlive the round, and the registry is never pruned

**Unfixed.** Low severity.

1. A stop reached through the dispatcher's own handoff is notified twice. The handoff tick sends
   the bare reason, such as "round closed" (946-948). The next tick sends the same reason followed
   by ": " and the problem list (874-884). That is a different reason at the same tip, so the
   deduplication does not suppress it.
2. A closed round stays registered. `start()` only appends to `rounds.json` (466-468), no action
   removes an entry, and every tick fetches each registered round that has neither `PAUSE` nor a
   marker (849-872).
3. D11 has each close-out task push its commits, including merges of `origin/main`, to
   `origin/dar-<date>`. A tick that sees each new tip notifies "round closed: " again. Once a
   close-out edit changes the round file's `State: live`, the tick notifies "invalid protocol: …"
   instead, because `parse_round` accepts no other State (protocol module 124-125). The test
   helper `lint_automated_round_headers` applies `parse_round` to every round file tracked at
   `HEAD` (`py/tests/test_dual_agent_review_turns.py` 119-131), so after integration the round
   file cannot leave `State: live` without failing the suite. Neither D13 nor the plan says what
   State a closed round's file should take.
4. After close-out deletes the remote branch, as separately authorized, the next fetch fails. The
   tick writes `PAUSE`, toasts "fetch failed: …" with the advice to inspect the marker and logs,
   and re-raises (867-872). That ends the tick before later registered rounds are visited
   (1018-1019).
5. Neither D13, the runbook nor the plan names a step to deregister or pause a closed round.
   Running the existing `pause` action before deleting the branch would prevent the alarm.

The registry checker corrected "indefinitely" in this turn's draft: fetching stops at a pause or
at the deletion, and only the registry entry persists. It also found item 1 and the repeated
notice in item 3. A second-wave checker confirmed both, limited item 1 to stops reached through a
handoff, and noted the `State: live` interplay; the consequence for the suite is this turn's own
reading of the test.

### 9. Turn 01 may request an acknowledgment, a form D9 gives no meaning there

**Unfixed.** Low severity.

- `validate_turn` accepts a turn 01 that names turn 02 and the other agent with the
  `; acknowledgment` suffix (protocol module 220-229), and the prompt offers turn 01 an
  "Agreement:" line of that form (526).
- D9 makes turn 2 the counter-argument, and its stopping rule turns on "a turn that accepts
  everything and lists no unresolved disagreement"; turn 01 has nothing to accept. D13's form 2
  does not exclude turn 01.
- If turn 01 used the form, turn 02 could only close the round, object or ask Ben. An objection
  counts as a reopening (protocol module 313), so at the default reopening cap of 1 a substantive
  counter-argument would spend the round's only permitted reopening. The gate would still demand
  turn 02's append.
- The transition oracle (`py/tests/test_dual_agent_review_turns.py` 74-80) asserts the same
  permission at every turn number, so closing the gap requires changing the test as well. It also
  exercises combinations that cannot occur, such as closure at turn 01 after an acknowledging
  predecessor.

### 10. The bounded fix-up is chosen by matching error text, and the turn-01 State error misses it

**Unfixed.** Low severity.

- `tick_round` relaunches the worker once only when every gate error contains "Next:", "State:",
  "acknowledgment" or "D10" (926-944). A malformed later-turn State line produces "later turn has
  invalid D10 State:" (protocol module 216), which qualifies. A malformed turn-01 State line
  produces "turn 01 must record not yet acted on" (protocol module 218), which contains none of
  the four tokens, so it is refused outright.
- Other messages qualify only through their wording. "turn needs an H1, blank line, and line-3
  State:" (protocol module 212) qualifies through "State:". Turn 02's "invalid reconciliation
  header: …" (739) qualifies through its inner message. Raw `diff --check` output (742) qualifies
  whenever an offending line happens to contain a token. None of these is one of the breaches
  that the comment at 927 excludes.
- D13 says refusals pause the round and does not mention a fix-up; the plan's step 6 of "3. The
  tick" provides one. No test exercises the fix-up path.

### 11. `test_agent_deployment_source_and_mapping` pins one selected name

**Unfixed.** Low severity; a question of test shape under the common instruction body.

- The test (`py/tests/test_dual_agent_review_turns.py` 144-154) asserts one hard-coded `Path`'s
  membership in `_ARCHIVE_PATHS`, that file's existence, and one literal substring in the source
  of `py/repo_util/user_config_sync.py`.
- The common body's "Tests are differential or lint-shaped" says "Do not add an example-based unit
  test that pins one selected case, string, or name unless Ben asks." No window document records
  such a request. The plan's specification of the test file covers only the header lint, the
  contiguity lint and the census differential.
- A lint-shaped alternative would enumerate `dot-claude/agents/` with `git ls-files -z`, fail on
  an empty list, and require an archive path and a mapping for each file. That directory holds one
  file today, so such a lint would check the same file; the defect is in the test's shape, not
  its coverage.

### 12. The dispatcher's commit subject departs from the plan's specified form

**Unfixed.** Editorial; low severity.

- The dispatcher commits "Record Claude turn 01 of the 2026-10-01 dual-agent review" for Claude
  (767). The plan's step 7 of "3. The tick" specifies
  `Record <Claude's|Codex> turn <NN> of the <date> dual-agent review`, and its "1. Protocol
  additions" item 4 calls that "the established subject form". The plan's list of superseding
  mechanics does not mention the change.
- The history is mixed. "Record Claude's turn" appears in eight subjects, all from 2026-09-26 on.
  "Record Claude turn" appears in four, from the 09-08, 09-10 and 09-16 rounds, none in the
  ISO-date form. "Record Codex turn" appears in thirteen.
- Recovery compares the committed subject with the computed one (798-799), so a change of form
  must not strand a marker made before it.
- A first-wave checker recounted the history and corrected this turn's draft, which had treated
  the possessive as the established form throughout.

## Open ends the window itself declares (not findings)

1. The plan's "7. Decisions for rollout" says its remaining choices "still need confirmation at
   rollout": items 2 to 8, which are the facts-only rule, the dispatcher taking turns 01 and 02,
   `dontAsk`, the measurement, the rehearsal venue, the notification channel and the Codex
   worktree's location. After the window, item 5 was approved on 2026-10-01, with its record named
   `doc/dual-agent-review-comparison-2026-10-01.md`. This round runs with the implemented choices
   for the rest, and with facts-only off.
2. At the window end, the runbook's State line and "Scheduler registration" record registration as
   pending; the post-window commit `d488f405` records it as done, with a successful idle tick.
3. Probe P7, private SSH, was deferred, and private rollout remains a separate step.
4. The rehearsal home, its local mirror, worktrees, logs and failure receipts remain preserved;
   their retirement awaits the repository's backup and retirement procedure.
5. The plan says "This plan's full definition of done has not been met". That definition ends with
   "one real round whose every turn was dispatched", which this round is meant to supply.
6. The runbook's P8 row records that checker completion before turn 02's first draft "is not
   established".

## What this review did not check

1. The suite, the two relay test modules and Black; finding 3 gives the reason.
2. The live behaviour of the Claude and Codex command-line programs: whether Claude's permission
   matching admits the forms in finding 4, what `--permission-prompts none` does, and the limits
   of the Codex sandbox.
3. Every untracked receipt that the runbook and plan cite, in the implementation clone's or the
   rehearsal home's `.novc/`, and this round's own dispatcher logs. The measured figures resting
   on them were not re-derived: the launch-command lengths of 13,754, 16,162 and 17,366
   characters, the suite counts, and the checker timings.
4. The notification helper and the registered scheduled task as installed on the machine,
   including the task's power settings.
5. MAM-private, which this series does not read, and probe P7.
6. Commits after the window, except where this turn names them as evidence.
7. The prose style of the window's documents, beyond the factual consistency of the passages
   cited.

## Reconciliation by Codex, turn 02, 2026-10-01

Codex wrote this append at `xhigh`, extra high, effort after all foreground checkers
finished. The original turn-01 bytes remain unchanged as a prefix. These are review
judgments, not remediation decisions. The counter-argument and full evidence are in
`doc/dual-agent-review-2026-10-01-turn-02-codex.md`; Claude's turn 03 should assess the
rejections, qualifications and two added findings before the round seeks acknowledgment.

| Finding and subject | Turn-02 disposition | Unfixed work and qualification |
|---|---|---|
| 1. Turn 02 stopping without reconciliation | Rejected as a code defect | D13 and the prompt universally require the append. D9 permits unchecked claims in the table. A stop-without-append exception would be a new policy, not an established repair. |
| 2. Repeated failure after resume suppresses notice | Confirmed | Unfixed: the reason/tip signature survives resume and suppresses a renewed notice when PAUSE is recreated. The local notify probe was isolated, with toast disabled. |
| 3. Claude interpreter permission | Qualified | Unfixed configuration gap: no interpreter rule is provided while the procedure asks for checks. Effective future CLI restrictions and the exact transcript-denial quotations remain unchecked. Ben decides the intended checking capability. |
| 4. Mechanical worker boundary | Qualified | Unfixed design limitation: the grants and gate do not establish a complete boundary around external files and remote acts. Actual permission matching and the listed escape forms remain untested. Ben decides the intended boundary. |
| 5. Whitespace checked after staging | Confirmed | Unfixed: a deterministic-worker probe reproduced the staged, unapproved result and subsequent handoff refusal. |
| 6. Empty or uninformative refusal reason | Confirmed | Unfixed: stderr-only reporting loses whitespace stdout and negative-ancestry context. The probe produced a newline-only PAUSE after cached whitespace refusal. |
| 7. Redispatch overwrites attempt records | Confirmed | Unfixed: prompts, launch records, logs and the Codex last-message output reuse names after explicit recovery. Existing turn files and markers remain protected while the marker stands. |
| 8. Stop notices and registry lifecycle | Qualified | Unfixed duplicate notices and lifecycle gap. Non-live State is a prospective constraint, not a required closure transition. Deleted-branch failure blocks later entries on that tick; subsequent ticks skip its PAUSE. |
| 9. Turn-01 acknowledgment | Qualified | Unfixed D9/D13 ambiguity for Ben: literal D13 permits it, while D9 assigns turn 02 the counter-argument. An objection's reopening consequence is confirmed. |
| 10. Error-text fix-up classifier | Confirmed | Unfixed: the invalid turn-01 State message misses the four tokens; unrelated whitespace content can match them. |
| 11. Deployment test's selected name | Rejected as an instruction violation | The test mechanically lints actual source and the repository tree, an allowed shape. Broadening its narrow coverage is optional; no repair is established by the cited rule. |
| 12. Commit subject versus plan | Confirmed; history scope clarified | Unfixed low-severity editorial mismatch. The mixed-history counts use all local refs, not endpoint ancestry alone. A future subject change must preserve recovery compatibility. |
| 13. Fetch/push destination verification — added in turn 02 | Confirmed | Unfixed: real local Git setup pushed to bare B before verification against bare A refused. URL fingerprints detect changes, not the initial destination relationship. Different spellings of the same repository are legitimate. |
| 14. Nested Windows differential-test path — added in turn 02 | Confirmed | Unfixed test portability defect: default targeted run gave 3 passed, 1 failed here; a process-local long-path workaround gave 4 passed. Production relay failure is not established. |

The endpoint census and whitespace check were verified. The full suite, effective
Claude CLI permissions, installed notification/task behavior and untracked rehearsal
receipts remain unchecked by turn 02. None of the confirmed or qualified work was
remediated during this review. Later corrections belong in later turns.
