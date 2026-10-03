# Updates to the first automated relay review's initial findings

State: open; first entry 2026-10-01.

**Approved remediation and close-out were completed on main on 2026-10-01; the relay was retired on 2026-10-03.**
"Relay retired, 2026-10-03" below records the current disposition. Findings 1 and 11 remain withdrawn.

## Close-out preparation by Codex, 2026-10-01

**Preparation completed; remediation was approved for a fresh executor.** Turn 05's
"No finding has been remediated; every finding that stands remains unfixed" describes the
review's closing disposition before remediation. Turn 04's **Findings after turn 04**, qualified by turn 05's
**Corrections this turn accepts**, **Evidence this turn adds** and **Reading notes on turn 04's
wording**, supplies the agreed review conclusions. Findings 1 and 11 are withdrawn for their
recorded reasons. Agreement between reviewers is no editorial or execution approval.

Codex prepared the single list, six concrete decision proposals and standalone remediation
plan in [PLAN-close-out-review-2026-10-01.md](PLAN-close-out-review-2026-10-01.md). Ben's
decisions and approval snapshot are recorded below; eventual per-finding outcomes belong here;
no numbered review turn or finished comparison is rewritten.

**Manual ownership preparation is complete.** The home clone was clean at the supplied
`38c0116f0d5b49c6ff3734e342ed7e79157e43ae`; the development worktree was clean at the
closed-review commit `aad47955e13e88db020113bacbccfce0ac89c7bb`. Fresh fetch found newer
main `4f4cbb6657e3c7b48a9878308d8cecf6edcc67e1`. After current runtime and process checks
found no worker ownership, the existing round-specific pause action wrote PAUSE before
any merge or tracked edit. D11's clean merge produced pre-edit development HEAD
`ef43a925aa83993400ce4c87cae93dfb47dc2930`. The plan names the exact checkout and
repeatable ownership checks. The scheduler remains enabled; this round stays paused,
and its registry entry and State remain unchanged pending approved lifecycle implementation.

For turn 01's passage "Neither D13 nor the plan says what State a closed round's file should
take", turn 04 and turn 05 retain the already-existing present-state maintenance duty while
leaving the terminal spelling, timing and classification for Ben. Changing State alone does
not resolve the parser/lint and registry lifecycle together.

For turn 01's passage "The dispatcher's commit subject departs from the plan's specified form",
turn 05 clarifies that the mismatch concerns the Claude form; the Codex form already matches.
Turn 04 corrected endpoint ancestry to 2/4/9, and turn 05 corrected turn 03's filtered-subset
wording. These review corrections survive in their own numbered turns; the proposed future
wording is a separate decision.

The separately authorized console fix is already on main as `0c12552b`. The finished comparison
and its original evidence are preserved. Unique comparison additions, general hardening,
performance tuning, private readiness/kickoff and cleanup remain outside execution approval.

**Preparation's effective base State, 2026-10-01:** not yet acted on; close-out plan approved
for fresh-session remediation; every surviving defect remained unfixed at that point.

## Ben's C1 decision, 2026-10-01

**Approved; implementation is assigned to the fresh executor under the complete-scope entry below.** Ben selected "Permit public
checks (Recommended)" in the dialog for **C1. Public checking capability, finding 3**.
The dialog named both workers, relevant public-only checks and scratch probes, the home
interpreter, preservation of tracked inputs/products, scratch in the worker checkout, and
manual handling of private-input checks. It expressly separated capability-policy approval
from the execution approval that follows the remaining choices.

The approved editorial wording is:

> Both workers may run relevant public-only scripts and targeted checks with the named home
> clone's interpreter from their own checkout. Before running a check, verify that its inputs
> stay within the round's evidence scope and that it preserves tracked inputs and products.
> Checks write only ignored scratch; workers do not run generators that rewrite tracked output.
> Scratch probes stay in that checkout's ignored directory. A denied or unavailable required
> check is reported as unchecked. Full-suite checks
> that require private inputs belong to manual remediation, outside a public review turn.

The live plan's C1 passage retains the same wording. The subsequent entries below record
later decisions; implementation/final integration scope is separately recorded there. No
launcher, worker instruction or implementation changed in this decision entry.

## Ben's C2 decision, 2026-10-01

**Approved; implementation is assigned to the fresh executor under the complete-scope entry below.** Ben selected "Approve the
documented trusted-worker boundary (Recommended)" in the dialog for **C2. Worker containment
claim, finding 4**. The dialog described trusted workers with an audited handoff, with no
complete external-file/remote-act containment claim. Ben did not choose the separately
verified hard-containment redesign.

The approved replacement for the relay plan's "The launch flags and the gate enforce this
mechanically" is:

> Workers are instructed to write only their allowed review records and ignored scratch, and
> to leave staging, commits and pushes to the dispatcher. Launch restrictions reduce their
> capabilities. The gate verifies the worker checkout, permitted paths and the named review
> branch before handoff. These checks do not establish containment of every external file,
> shared Git setting or remote act. This design relies on trusted workers following their
> scope; a complete containment guarantee requires a separately verified boundary.

The subsequent entries below record later decisions and execution scope. The same limits
belong in the runbook under the approved plan; an interpreter allow rule is not confinement.

## Ben's C3 decision, 2026-10-01

**Approved; implementation is assigned to the fresh executor under the complete-scope entry below.** Ben selected "Keep present-state
round plus inactive registry (Recommended)" in the dialog for **C3. Registry and round-file
lifecycle, finding 8**. The selection keeps present-state classification; it does not approve
receipt reclassification or branch/worktree deletion.

The approved editorial wording is:

> On acknowledgment closure, the dispatcher marks that round inactive before later ticks can
> fetch or launch it. Manual close-out begins only after a round-specific pause and verification
> that no worker is live. A deactivate action records manual ownership for an already-closed
> round without deleting its registry entry, checkout or evidence. The round file stays live
> while close-out work remains. After approved remediation is verified and main integration
> has actually succeeded, it records State: executed <date>; close-out completed. The parser
> and tracked-round
> lint accept that terminal State, and terminal rounds are never dispatchable.

The approved plan couples parser/lint and inactive-registry changes, keeps cap/decision stops
recoverable, retains PAUSE for this round while old scheduler code runs, and requires the
actual home-registry action only after the new code reaches that home clone. The subsequent
entries below record later decisions and execution scope.

## Ben's C4 decision, 2026-10-01

**Approved; implementation is assigned to the fresh executor under the complete-scope entry below.** Ben selected "Require turn 02
counter-argument before acknowledgment (Recommended)" in the dialog for **C4. Turn-01
acknowledgment, finding 9**. Turn 01 cannot request acknowledgment; the alternative expedited
closure and its reopening consequence were not selected.

The approved D13 qualification is:

> An acknowledgment request is permitted only from turn 02 onward, after a predecessor's
> claims have been assessed under D9. Turn 01 names turn 02 for the counter-argument or stops
> for Ben; turn 02 always supplies its reconciliation append. The earliest owed acknowledgment
> is turn 03. A counter-argument to turn 01 does not consume a reopening.

The subsequent entries below record later decisions and execution scope. The parser, prompt
and independent transition oracle will implement the same semantics only under approved
execution scope.

## Ben's C5 decision, 2026-10-01

**Approved; implementation is assigned to the fresh executor under the complete-scope entry below.** Ben selected "Keep current
nonpossessive Claude form (Recommended)" in the dialog for **C5. Future commit subjects,
finding 12**. Historical pushed subjects remain intact, and no possessive-form change was
selected for future commits.

The approved live-plan wording is:

> Automated handoffs use Record <Claude|Codex> turn <NN> of the <date> dual-agent review.
> Historical subjects remain unchanged. Recovery verifies the subject recorded for the
> original approved attempt rather than silently replacing its expected wording.

The subsequent entries below record later decisions and execution scope. The implementation
currently uses the approved future form; the live plan will be aligned under the remediation
scope.

## Ben's C6 decision, 2026-10-01

**Approved; implementation is assigned to the fresh executor under the complete-scope entry below.** Ben selected "Use the bounded
identity resolver (Recommended)" in the dialog for **C6. Remote identity guard, finding 13**.
This approves supported GitHub HTTPS/SSH identity spellings and actual local Git directories,
with unknown/ambiguous aliases refused before a push. The operator-mapping alternative was
not selected.

The approved runbook wording is:

> Setup records the verified repository identity. Before setup or handoff pushes, and before
> each dispatch, the dispatcher verifies that the home clone's observing destination and
> each worker's effective fetch and push destinations resolve to that identity. Verification
> includes per-worktree configuration and expanded URL rewrite rules. Unknown or ambiguous
> identity stops before a push. Matching branch tips and unchanged URL fingerprints do not
> establish repository identity.

All six policy choices are approved; the scope/location entry below records subsequent
execution approval. No surviving defect was fixed during decision write-back.

## Ben's complete-scope and fresh-session decision, 2026-10-01

**Approved; implementation and eventual final integration are assigned to a fresh executor.**
Ben selected "Approve; prepare a fresh-session execution prompt (Recommended)" in the dialog
that expressly included all surviving findings, the proposed Next: Ben notice wording,
targeted checks, final suite/mega, final main integration and canonical-agent deployment.
The dialog expressly excluded unique comparison proposals, private rollout and cleanup.

The approved successful-stop notice wording from wave 3 is:

> <repository>, round <date>: Ben's decision required: <worker reason>. Read <turn path>.
> Record the decision in <turn-01 update path>; continue through an authorized Override:
> in <round-file path>.

The live plan's **Frozen approval snapshot, 2026-10-01** binds these choices, expected paths
and unchanged products, verification gates, evidence preservation and final integration
sequence. The fresh session reuses the existing development worktree; it creates no new
isolation without an actual collision. This session commits/pushes the decision write-back
and provides the exact required commit in its standalone successor prompt. The round stays
paused, the Windows scheduler stays enabled, and the existing follow-up stays paused.

No further general execution or main-integration approval is required within this scope.
An unexpected material requirement, unowned edit, unexplained output or ownership collision
still follows the plan's stop/reconciliation procedure. No remediation code was changed in
this planning session.

## Remediation execution by Codex, 2026-10-01

**Implemented; final suite, mega, main integration, deployment and home-registry transition
are pending.** The executor reused the named Claude worktree on local `dar-2026-10-01`.
Required handoff `b7f6f0933d9b57e8b0cfaa96d312ca90bc2011c0` was its clean pre-edit HEAD.
Fresh fetch found that shared review tip unchanged and main at
`4f4cbb6657e3c7b48a9878308d8cecf6edcc67e1`; both D11 merges were already up to date.
Current runtime/process checks found no round worker or dispatcher, no dispatcher lock or
in-flight/setup marker, and PAUSE present. The scheduler stayed enabled, Ready; the existing
follow-up was left paused. The separate console fix remains in the ancestry.

The table resolves the surviving review list by finding number and searchable subject.

| Finding | Implementation and verification |
|---|---|
| 1. Turn 02 stopping without reconciliation | Withdrawn; no new exception. Turn 02's append remains required. |
| 2. Repeated failure suppresses notice | Fixed in `resolve_notice`, `notify` and dispatcher lock handling: recovery ends an episode, new episodes receive distinct notice copies, repeats stay quiet. The recovery-event oracle covers failure, marker and lock episodes, including lock disappearance. |
| 3. Claude interpreter permission | Fixed under C1 in configuration, `worker_command`, prompts and the canonical worker agent. Bounded Claude and Codex probes actually ran the exact home interpreter on a public scratch check and emitted `RELAY_PUBLIC_CHECK_OK é`; tracked diffs stayed unchanged. This observes these launches, not every future CLI launch. |
| 4. Mechanical worker boundary | Fixed under C2 in the live relay plan and runbook with the approved trusted-worker wording. No complete external-file, shared-setting or remote-act containment claim remains. |
| 5. Whitespace checked after staging | Fixed in `proposed_tree` and `handoff`: a disposable index validates all proposed owned bytes before real staging; approval records precede staging. Independent Git index/tree checks cover whitespace settings, reconciliation bytes and preserved legacy staged-unapproved recovery. The runbook explains explicit recovery. |
| 6. Empty or uninformative refusal reason | Fixed in `git_diagnostic` and ancestry/start/end lookup: operation, exit status, available stdout/stderr and explicit empty-output context are retained, with URL credentials redacted. Real Git command results supply the differential oracle. The console-hiding fix is preserved. |
| 7. Attempt records reused | Fixed with exclusively created short attempt directories and separate initial/fix-up prompt, launch, stream and Codex output paths. First refusal diagnostics and owned bytes are saved with `files.json`; redispatch preserves old records. Independent launch and byte observations verify preservation. |
| 8. Stop notices and registry lifecycle | Fixed under C3 in `stop_notice`, `stopped_round`, `deactivate`, parser/lint and CLI. Ben stops name the reason, turn, update and Override route. Closed registrations become inactive; inactive ticks skip clone/remote work. The two-round oracle checks continuation, closure and another eligible round. This actual home registration still awaits the new code's integration. |
| 9. Turn-01 acknowledgment | Fixed under C4 in D9/D13, parser, prompts and worker agent. Turn 02 counter-argument precedes acknowledgment; the earliest owed acknowledgment is turn 03. Both Agent-1 assignments and reachable histories/caps are checked independently. |
| 10. Error-text fix-up classifier | Fixed with typed `GateFailure` categories and `HeaderError`. One fix-up is available only for an all-header refusal; its prompt names the real dirty paths, unchanged HEAD and unstaged index. Refused body/reconciliation bytes are protected. Fault and dirty-byte oracles cover arbitrary token-bearing unsafe errors and header corrections. |
| 11. Deployment test's selected name | Withdrawn; the permitted mechanical deployment lint is retained without optional broadening. |
| 12. Commit subject versus plan | Fixed under C5 by aligning the live plan to `Record <Claude|Codex> turn <NN> of the <date> dual-agent review`. New markers retain their exact subject; recovery retains legacy handling. Historical pushed subjects are unchanged. |
| 13. Remote identity guard | Fixed under C6 in setup, retained registrations/markers, dispatch and pre-push gates. Supported GitHub spellings resolve to host/owner/repository and local destinations to actual Git directories. Independent local A/B, alias/rewrite, retained-baseline and per-worktree destination checks refuse splits without changing either remote. |
| 14. Windows blob-path lookup | Fixed with the explicit `--` blob separator. The focused entry point passed from this exact worktree with process-local `core.longpaths=false`; persistent Git settings stayed unchanged. Short artifact names also repair path-length failures exposed by that run. |
| 15. Verification coverage | Fixed with the approved differential/lint checks in both relay test modules: reachable protocol histories, caps/terminal State, actual Git bytes/refs, refusal categories, recovery, unique artifacts, notice episodes and two-round lifecycle. Missing inputs fail; the existing deployment lint remains. |

Focused verification passed 15 tests. After the fresh source audit's continuation-handoff and
lock-disappearance repairs, the affected Git/episode checks passed 2 tests with 13 deselected.
Both runs used the required home interpreter from this worktree, `core.longpaths=false`,
`PYTHONUTF8=0` and no `PYTHONIOENCODING`; persistent configuration hashes stayed unchanged.
Black at defaults left all changed Python formatted, and `git diff --check` passed.
Earlier failed focused runs exposed the long artifact paths and an outdated copy-path test
assertion; those failures were corrected without relocating the checkout or changing Windows
settings. Root retained sole writing ownership; delegated audits were read-only and the
bounded test-writing handoff returned ownership before further root edits.

Public verification evidence is retained under this worktree's ignored `.novc/`:
`relay-remediation-focused-7c8322d6f416`, `relay-remediation-focused-862b21ffc0ec`,
`relay-capability-claude-26d30d24db7a`, `relay-capability-claude-ee65fb02ad5e` and
`relay-capability-codex-8f840da99a3c`. Claude's probe used an explicit current packaged
2.1.286 executable after inspecting the historical launch and current installation;
the historical 2.1.284 path was unavailable. This is probe provenance, not a CLI-discovery
redesign. The PowerShell tool result and Codex command result contain the sentinel; the
Claude completed result reports no permission denials. No numbered review or network push
was launched by either probe. Full verification logs remain in MAM-private.

The original 26 home-control evidence files were snapshotted by SHA-256 in
`relay-remediation-snapshot-29ac3e13f38d/original-evidence.json` before implementation.
The five numbered turns, finished comparison/rehearsal evidence, both September 29 reviews,
Ben's separate work and private rollout boundary remain preserved. The single base pointer
already exists and needs no rewrite.

## Final executable verification by Codex, 2026-10-01

**Verified; main integration, deployment and actual home deactivation remain pending.**
Remediation commit `2e120b851d43607bf21b19eadeea27fce114b3b8` was pushed to
`origin/dar-2026-10-01`. Fresh origin/main had advanced to
`5e2fe24295ebd3bce75babc510920f30bf8d8b8c` with independently developed redirect
preparation. The clean home clone fast-forwarded to that tip. The development carrier merged
it without conflict as `4251e8f6e141639cbf07205e480e9277f60715f9`, and that coherent
merge was pushed to the same shared branch. No intermediate remediation reached main.

The first full suite passed 1,054 tests and 60 subtests, with 5 skips. Because incoming main
changed executable source/tests, the full suite was repeated after the merge with the same
options: 1,056 tests and 60 subtests passed, with the same 5 skips. The required mega then
passed all 57 steps at that exact merged commit. The post-mega NUL-delimited status and
tracked diff were empty: there is no generated diff to explain or commit. Both final gates
used `core.longpaths=false`, UTF-8 mode disabled and no `PYTHONIOENCODING`; persistent Git
configuration stayed unchanged. Full logs and result JSON are retained privately in
`MAM-private/.novc/relay-remediation-suite-81b160adf334`,
`MAM-private/.novc/relay-remediation-suite-c06c3890051f` and
`MAM-private/.novc/relay-remediation-mega-137e3a59bc57`.

The fresh implementation/coverage audits found no remaining material in-scope gap after the
two final repairs. Fake workers/local notices verify dispatcher behavior; they do not
establish live Windows notification receipt. Automatic Claude discovery was unavailable in
this installation, so the capability probe used the already-supported explicit CLI setting;
CLI-discovery redesign remains outside this approved package.

The actual home registry is still the retained legacy active entry at this point, PAUSE is
present, no marker/lock or runtime blocker exists, and all original 26 evidence hashes match.
The Windows task is Ready, enabled, with IgnoreNew. Only after the verified tree is pushed
to main will canonical deployment and the home entry point's deactivate action run.

**Effective base State, 2026-10-01:** acted on; every surviving approved finding is remediated
and verified under its recorded qualification; findings 1 and 11 remain withdrawn. Integration
and lifecycle completion are pending, so the maintained round still records State: live.

## Completed close-out by Codex, 2026-10-01

**Completed on main; every surviving approved finding is fixed under its recorded
qualification.** Findings 1 and 11 remain withdrawn. The clean home main fast-forwarded to
verified `5a5d80b853ba07ef24ff0bdbb3f8382e1604518d` and the normal push succeeded.
Fresh origin/main then supplied canonical deployment: `USER_CONFIG_DEPLOYED_COUNT=1`,
followed by `USER_CONFIG_PROBLEM_COUNT=0`. The revised canonical
`dot-claude/agents/dual-agent-review-turn.md` was deployed; live instruction files were not
edited directly. "Relay retired, 2026-10-03" below records the deployed copy's later
disposition.

The revised home entry point ran `--dual-agent-review deactivate` for this exact round.
Its actual registry retained the entry with `state: inactive`, `ownership: manual`,
`closed_tip: 5a5d80b853ba07ef24ff0bdbb3f8382e1604518d` and stored timestamp
`2026-10-01T18:04:47.728712-04:00`. The transition evidence was retained at
`C:/Users/BenDe/GitRepos2/MAM-basics/.novc/dual-agent-review/2026-10-01/deactivation-1359b6e8192044f792c878b27a16802c.json`.
PAUSE remained present; no in-flight/setup marker or dispatcher lock was removed to clear a
gate. When this entry was written, both worktrees, the branch and all original control evidence
remained recoverable; "Relay retired, 2026-10-03" below records what became of them.

The instrumented tick imported the home module, asserted its actual CONTROL path and inactive
manual registration, and forbade fetch/launch/notify/round visits. It returned zero with every
counter zero and unchanged registry/round-control bytes. The Windows task's inspected action
used the home `.venv/Scripts/pythonw.exe`, home `py/main_repo_util.py`,
`--dual-agent-review tick` and home working directory, with no alternate configuration. It
remained Ready, enabled, with IgnoreNew when this entry was written. This proves inactive
dispatch handling for the scheduler's source and registry; it does not claim a new worker
exchange or notification receipt. The existing follow-up was left paused and received no
automation update.

The final ownership/evidence audit found clean home/development checkouts, no runtime
blockers and all original 26 SHA-256 hashes unchanged. The round now records
`State: executed 2026-10-01; close-out completed`; the relay's parser and lint then admitted
this terminal state, and the round could not dispatch. This final documentation commit records
those actual outcomes. The executable and generated-product trees remain the verified `4251e8f6`
tree, so the 1,056-pass/60-subtest suite and 57-step mega results remain applicable.
The existing census and deployment lints passed on the final terminal round (2 passed,
13 deselected) with `core.longpaths=false` and explicit-encoding checks; the final tracked
whitespace check passed. Their public evidence is retained in
`.novc/relay-remediation-focused-4cc8444380f7` in the development worktree.

**Effective base State, 2026-10-01:** acted on; approved remediation, main integration,
canonical deployment and manual inactive lifecycle completed. The five numbered turns,
comparison/rehearsal evidence, both September 29 reviews, console fix and Ben's separate
follow-up work are preserved. Private readiness/kickoff, excluded comparison proposals,
general hardening, performance tuning and cleanup remain outside this completed scope.

## Update-State correction by Codex, 2026-10-02

**Corrected the update's own State; remediation remains complete.** The former
`State: closed; first entry and remediation completion 2026-10-01` confused the update's State
with its base review's effective State. The update stays open while its base is tracked, as
`iterative-document-editing` requires. The completed effective base State recorded above stands.

## Relay retired, 2026-10-03

Recorded by Claude Opus 5.5 on 2026-10-03, New York time, executing items R1 to R7 of
`doc/PLAN-remediate-review-findings-2026-10-02.md` in `C:/Users/BenDe/GitRepos2/MAM-basics` on the
machine `LAPTOP-DBLE8UKA`.

**Retired: the relay that this round reviewed and remediated was removed from the tree on
2026-10-03; this round's records stay unchanged.** Ben's selection on 2026-10-03, verbatim, was
"Retire the relay now" (`doc/review-findings-2026-10-02-update.md`, "Ben's close-out decisions,
2026-10-03", item 3). Commit `4573b0070be6eab2d31257a1cdf766b60ae766af`, which added this entry,
removed the relay's ten files, among them `py/repo_util/dual_agent_review_dispatch.py`,
`py/repo_util/dual_agent_review_round.py`, their two test modules,
`doc/dual-agent-review-automation.md` and `doc/PLAN-automate-the-dual-agent-review-relay.md`,
together with the `--dual-agent-review` action of `py/main_repo_util.py` and the agent file's
deployment in `py/repo_util/user_config_sync.py` and `dot-claude/README.md`. Its parent,
[`cbd405b11ef990040031ccf19699db54a69a489d`](https://github.com/bdenckla/MAM-basics/tree/cbd405b11ef990040031ccf19699db54a69a489d),
is the last commit whose tree holds every removed file; each path and line that this round's
records cite in those files resolves there. D13 in `doc/dual-agent-review.md` is now a dated
retirement note.

The round file, the five numbered turns, `doc/PLAN-close-out-review-2026-10-01.md` and
`doc/dual-agent-review-comparison-2026-10-01.md` are unchanged. In the round file, "This
present-state file identifies an automated round" and "PAUSE, worktrees, branch and evidence are
retained" describe the round as of 2026-10-01; no dispatcher reads the file now. The same
commit corrected five present-tense passages above in place:

1. The bold lead under the State line read "Approved remediation and close-out are completed on
   main; deployment and home deactivation are verified." and was followed by "The execution entry
   below records the current disposition." They now read "Approved remediation and close-out were
   completed on main on 2026-10-01; the relay was retired on 2026-10-03." and ""Relay retired,
   2026-10-03" below records the current disposition."
2. In "Completed close-out by Codex, 2026-10-01", "The revised canonical
   `dot-claude/agents/dual-agent-review-turn.md` is deployed; live instruction files were not
   edited directly." now reads "… was deployed; live instruction files were not edited directly.
   "Relay retired, 2026-10-03" below records the deployed copy's later disposition."
3. In the same entry, the passage from "Its actual registry retains the entry" to "all original
   control evidence remain recoverable." is now in the past tense: "retains" became "retained",
   "The transition evidence is retained at" became "… was retained at", "PAUSE remains present"
   became "PAUSE remained present", and "Both worktrees, the branch and all original control
   evidence remain recoverable." became "When this entry was written, both worktrees, the branch
   and all original control evidence remained recoverable; "Relay retired, 2026-10-03" below
   records what became of them."
4. In the same entry, "The Windows task's inspected action uses" became "… used", and "It remains
   Ready, enabled, with IgnoreNew." became "It remained Ready, enabled, with IgnoreNew when this
   entry was written."
5. In the same entry, "its parser/lint already admits this terminal state and it cannot dispatch"
   became "the relay's parser and lint then admitted this terminal state, and the round could not
   dispatch".

Ben authorized in advance, on 2026-10-03, the acts outside the repository that the remediation
plan lists under "Acts outside the repository"; later dated entries here record each one's
outcome as it is done, and `origin/dar-2026-10-01` stays by his choice.

**Effective base State, 2026-10-03:** acted on; the approved remediation completed on 2026-10-01
stands as recorded above, and the relay it remediated was retired on 2026-10-03.
