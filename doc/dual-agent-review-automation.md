# Automated dual-agent review operations

State: live; four real automatic handoffs verified 2026-09-30; D13 and notification receipt confirmed; production enabled; scheduler registration pending.

Ben authorized `doc/PLAN-automate-the-dual-agent-review-relay.md` on 2026-09-30 and
excluded both ongoing September 29 reviews. The sole development checkout is
`C:/Users/BenDe/GitRepos2/MAM-basics`, starting on clean `main` at
`303bf2399c1e1fc1300a75f4fb1ed335d62984d0`. Its own environment runs all commands.
Codex owns implementation, verification, and pushing `main`.

## Approved D13 protocol

Ben approved the proposed D13 wording on 2026-09-30 by selecting the approval
passage in Codex's implementation report and replying "I approve". The approved
wording now lives in `doc/dual-agent-review.md`, "Automated relay and the `Next:`
line — Ben's decision, 2026-09-30 (D13)". The approval covers that protocol;
the facts-only rule, measurement and future review window
retain their recorded prerequisites.

## Configuration and operation

`in/dual_agent_review_automation.json` sets launch rules, caps, timeouts, and CLI
discovery; `--automation-config <absolute-path>` selects an explicit alternative.
`production_enabled` is true after the real-worker rehearsal, collision probe
and Ben's confirmation of corrected notification receipt. D13 is approved.
Claude discovery checks PATH, `.local/bin`, the ordinary app-bundled CLI, and its
packaged-app LocalCache layout. Codex
checks an explicit path, `CODEX_CLI_PATH` in its configuration, then the newest app
binary. Existing CLI authentication is used; tokens are never written to tracked
configuration or launch records. Launch JSON records the model, effort and arguments.

The scheduler may run this secondary clone's code without changing the occupied
primary clone. The registry and process lock stay under its
`.novc/dual-agent-review/`. Each round's logs, markers and notification file stay
under the round's own repository. Private findings and logs remain in MAM-private.

Status reads the last fetched branch without fetching:

```powershell
C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos2/MAM-basics/py/main_repo_util.py --dual-agent-review status --repo C:/Users/BenDe/GitRepos2/MAM-basics --round 2026-09-29
```

An idle tick only visits rounds registered by `start`; an empty registry does nothing:

```powershell
C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos2/MAM-basics/py/main_repo_util.py --dual-agent-review tick
```

Kickoff requires a new date, Agent 1, endpoints, and Ben's verbatim instruction.
The helper creates two locked worktrees under the named home clone's
`.claude/worktrees/`, using that clone's interpreter. Carriers update only through
verified fast-forward merges. `pause` writes `PAUSE`; `resume` removes it only with
no in-flight marker. `handoff` gates a preserved result before committing and pushing.
Stale locks and in-flight markers are never automatically deleted. After a push
failure, inspect the committed tip, remote tip and marker; preserve the turn's commit.
The handoff action resumes a dispatcher-approved index or commit idempotently,
verifying its tree and parent, and recognizes a push that already reached the remote.
Then resume the round to clear its failure pause. A commit made by a worker has no
dispatcher approval record and remains a breach.

The toast helper uses Windows PowerShell's .NET Framework WinRT support in a hidden
process: the required WinRT types are unavailable in this machine's PowerShell 7.
Agent shell commands and the registration command still run in PowerShell 7.
The sender is the installed **Windows PowerShell** identity returned by
`Get-StartApps`, so notifications appear under Windows PowerShell with the title
**Dual-agent review**. A disabled notification setting produces `toast-error.txt`;
a successful submission produces `toast-result.json` with its sender, setting,
tag, group and immediate notification-history result. API acceptance and history
evidence do not independently establish that Ben saw a notification.

## Scheduler registration

The registration script creates a task every 3 minutes, only while Ben is logged on,
with limited privilege and `IgnoreNew` instance handling. `pythonw.exe` starts the
tick without a console window. Registration remains Ben's action after live worker
verification. This implementation does not enable an unattended task.

The worker rehearsal, collision probe and notification receipt have passed.
Ben confirmed the corrected **Dual-agent review** toast under **Windows PowerShell**
and supplied a screenshot. Production is enabled and this command is ready for
Ben to run in PowerShell 7 without elevation. The task serves only explicitly
registered rounds; the current empty registry makes its tick idle. A production
round still requires Ben's approved future window, Agent 1 and kickoff instruction.

```powershell
& C:/Users/BenDe/GitRepos2/MAM-basics/misc/register-dual-agent-review-task.ps1 -Repository C:/Users/BenDe/GitRepos2/MAM-basics
```

## Verification and remaining rollout

The changed Python passed Black. The targeted checks passed 4 tests; the final full
suite passed 1015 tests, with 5 skips and 60 subtests, using `py/main_test.py -q`.
The latest notification-fix run passed the same counts with one warning that
pytest could not write its local cache; no test failed. Both PowerShell
scripts passed syntax parsing. No mega generator is reached; `gh-pages/` and all
`MAM-*` products stayed unchanged.

The local Git differential check dispatched three turns with deterministic fake
workers against a temporary bare repository. Independent Git observations confirmed
the new turn paths, reconciliation append, pushed tips, closure and subsequent idle
tick. The check exercised foreign writes, staging, a worker commit and push, changed
push URLs, and refusal of network rehearsal destinations before any remote query.
A forced push failure paused and notified; manual handoff recovered the approved
commit without rerunning the worker or rewriting history. This verifies the
dispatcher; it is not the plan's three-turn real-worker rehearsal.

| Probe | Verified result and remaining work |
|---|---|
| P1: Claude effort and sub-agents | Passed the renewed-login and full capability checks, then real turns 01 and 03 at Opus 5.5/max with one and three completed foreground checkers, no background checker, and automatic handoff. Turn 01's two denied Git grep calls were replaced by allowed reads; the final grep rule separately passed with zero denials. Turn 03's denied rev-list read led to the final rule, which passed the real collision probe with zero denials. |
| P2: Codex model and effort | Passed the full capability check after removing `--ephemeral`, then real turns 02 and 04 with three read-only checkers each and automatic handoff. Both saved runtime contexts confirm `gpt-6.1-sol`, `xhigh`, workspace-write and network disabled. |
| P3: foreign-file gate | Passed against independent Git status evidence in the local check. |
| P4: movement and failures | Passed with a real Claude worker: the local mirror advanced mid-process, the gate rejected remote movement, the checkout stayed clean at its original tip, and pause, marker, logs and notification were preserved. Independent bare-repository reads confirmed the dummy commit. The differential worker-push refusal and forced dispatcher push-failure recovery also passed. |
| P5: closure and cap | The differential three-turn check requested acknowledgment, closed, and did not launch a fourth worker. The real four-turn rehearsal requested turn 05 acknowledgment, stopped at cap 4, and stayed idle with no further commit. The real round did not close. |
| P6: notifications and hidden launch | Passed after correcting the sender identity. The hidden helper and dispatcher test both reached Windows notification history. Ben replied "Yes, I see the corrected test" and supplied a screenshot. The hidden `pythonw.exe` idle tick exited 0 with an empty registry. The scheduled task has not been registered. |
| P7: private SSH | Deferred until both ongoing reviews finish and Ben approves private rollout. No private fetch or push was attempted. |
| P8: Codex worktree and instructions | Passed in both real Codex turns: the runtime CWD is the dedicated Codex worktree, native PowerShell verified root/HEAD/carrier/NUL status, and repository and required skill instructions were loaded. All three turn-02 checker reports arrived before the final revisions and dispatcher commit; completion before its first draft write is not established. |

Original failed authentication logs are preserved in this implementation clone's
`.novc/dual-agent-review-probe-20260930/`; the successful renewed-login probe is in
`.novc/dual-agent-review-renewed-login-20260930/`. The isolated rehearsal home is
`C:/Users/BenDe/GitRepos-rehearsal/dual-agent-review-20260930/MAM-basics`, a clean
public-source clone with its own environment and a local bare origin. Its initial
baseline is `38f1b57313267908ad70a70cbfa15f4b6919fe0d`; initial capability logs stay
in its `.novc/dual-agent-review-preflight/`. No worker reads MAM-private. The
separate `.novc/dual-agent-review-native-git-20260930/` probe in the implementation
clone confirmed the new Claude permission rule: the exact native PowerShell Git
read returned that baseline with zero permission denials. Fresh Codex processes
now retain their ordinary CLI transcripts to support sub-agents; the dispatcher
never resumes an earlier turn's session.
The successful full capability logs and JSON records are in the rehearsal home's
`.novc/dual-agent-review-preflight-02/`. Its main baseline is
`05e109cf579d97404ff596a1f8ff78394d077c20`. The isolated round started at local
mirror tip `491168dd13a831be3bf5b1ef1d70beafbdbcd4db`, reviewing the D13 adoption
window `9988db8e..38f1b573`, with Claude as Agent 1, a four-turn cap and a twenty-minute
worker deadline. Logs and markers stay in that home's
`.novc/dual-agent-review/2026-09-30/`. Codex stopped the first worker after denied
batched PowerShell reads led it to use Git Bash. Only the verified rehearsal driver
PID 35672 and its own descendants were terminated; the checkout stayed clean and
no review turn was committed. The original marker and log are preserved before
recovery. The launcher now denies Bash on Windows, covers exact quoted trust
prefixes, and supplies separate Git command forms in the prompt. Optional shell
and clock queries are unnecessary because the native tool declares PowerShell 7+
and the dispatcher supplies an explicit New York timestamp.
The isolated quoted-prefix worktree probe then returned the expected tip with
zero permission denials. Its launch command is 13,754 characters, independently
checked below the Windows 32,767-character limit; records are in the implementation
clone's `.novc/dual-agent-review-native-worktree-20260930/`.
The retry completed all five foreground checker reports but exceeded the rehearsal's
shortened twenty-minute deadline before writing a turn. The dispatcher preserved
the in-flight marker, logs, pause and notification; its worker checkout and local
remote stayed at `491168dd13a831be3bf5b1ef1d70beafbdbcd4db` with no turn file.
The worker's dead-process session record was cleared by Claude's own normal startup,
after its PID was independently verified absent; Codex did not edit the runtime
registry. The timeout files are preserved with `-twenty-minute-timeout` names and
`timeout-recovery.json`. The five completed checker reports remain in
`completed-checker-evidence-from-timeout.md` under the same round directory.
The initial argument resumed under the normal 120-minute deadline, using those
reports as evidence and at most one fresh foreground checker.

Observed denials also identified two missing read commands: `git check-ignore` and
`git grep`. Both exact native PowerShell rules subsequently passed isolated probes
with zero denials; records stay in this implementation clone's
`.novc/dual-agent-review-check-ignore-20260930/` and
`.novc/dual-agent-review-git-grep-20260930/`. The expanded launch remains below the
Windows command limit at 16,162 characters. The `Next:` parser now counts only
header fields; body quotations do not alter control state. Its independent model
checks 3,200 transition, header and body combinations. D9, D11 and periodic-review
cross-references now distinguish manual mechanics from the approved D13 mechanics.
The approved D13 wording is unchanged.
The parser's header scope follows the plan's `Next:` specification: exactly one
line beginning `Next:` "in its header block". Rehearsal review
opinions do not replace that implementation requirement.

The four real turns passed automatic handoff at
`16956671abac29445bf7a7b2c824bd10ee2a51c8` and
`2e0a969a9306426d65cc321c1d0e807d5ad42200`, then
`c2c5c064d91ebcd33c9438baca3f520f1c8e5a5d` and
`aeeb021fc1b539c1449f1e8fd860fdd1f3439664`. Turn 02 preserved turn 01's byte prefix
and appended reconciliation. Turn 04 requested turn 05 acknowledgment; cap 4
stopped dispatch and a subsequent tick made no further commit. The independent
receipt is `.novc/relay-real-worker-verification-20260930.json` in the implementation
clone. The four-turn controller was `42cb46a9eefefda2d18ece69301ec5da252795f9`;
the final parser and read-rule fixes are verified separately at
`a13f1eab39d96c9512c501937a22d2c31f9c3bc8`. Both Codex runtime contexts confirm
the pinned model and effort. Their startup warnings concern plugin icon paths
and unsupported shell snapshots; neither prevented successful terminal events or handoff.

Turn 02's third checker report arrived 23 milliseconds after its initial draft
write completed. Delivery time does not establish the checker's physical completion
time. All reports arrived before the two final revisions and dispatcher commit;
the handed-off artifact incorporates the checker results. The evidence does not
establish that every checker finished before the first draft.

Turn 03's attempted `git rev-list` count exposed another missing read permission;
the rule is included in the final launcher. With all three added read commands the
launch is 17,366 characters, independently checked below the Windows limit.

The first synthetic collision probe, round `2026-10-01`, used a shortened
ten-minute deadline and timed out after its two native Git reads and checker.
Its logs, moved local remote, clean worker tip, pause, marker and timeout alert
remain preserved in the rehearsal home. The worker PID was verified absent;
Claude's normal startup cleared its own dead-process record, with before-and-after
evidence in the implementation clone's
`.novc/dual-agent-review-owned-stale-session-final-20260930/`.

The final collision probe, synthetic round `2026-10-02`, ran under the normal
120-minute deadline with the current controller
`a13f1eab39d96c9512c501937a22d2c31f9c3bc8`. Its real Claude worker completed
exactly two native Git reads with zero permission denials and a successful
terminal event. While that process ran, the local bare branch advanced from
`be6c6bc424a2d72dd65a0cd13ef123aad1f49f72` to same-tree child
`9fb2b071e2a9ff8e312a1409955ac3361aaff851`. The worker checkout stayed clean at
its initial tip. The dispatcher reported **remote moved during the turn**,
paused, and preserved its marker and notification. This capability probe wrote
no review turn. Its independent receipt is
`.novc/relay-live-movement-verification-20260930.json` in the implementation clone;
the controller's injection and result receipts remain in the rehearsal home's
`.novc/dual-agent-review/2026-10-02/`. These synthetic failure rounds are
intentionally paused and require no action to resume them.

The source implementation registry is absent;
no production round was started. The primary clone was not fast-forwarded. Production is
enabled after Ben's notification confirmation; Ben has approved D13. Core commit
`1a50d4b6d132a66dcb9d54d9b9275cd62fc2d580` was pushed to `main`. Main-sourced
configuration deployment installed only the new Claude agent file; every existing
instruction, hook and skill was already clean. The subsequent
`--sync-user-config --check` returned zero problems.
Worker fix commit `05e109cf579d97404ff596a1f8ff78394d077c20` is on `origin/main`;
its complete deployment installed only the changed Claude agent definition and
the follow-up check again returned zero problems. That implementation suite passed
1015 tests, 5 skips and 60 subtests without a warning.

## Notification correction and user receipt, 2026-09-30

Fixed: the original helper submitted to `Microsoft.Windows.PowerShell`, an identity
absent from this machine's installed app list. That notifier reported **Enabled**
and returned without error, but Ben saw no relay notification. The corrected
helper resolves the installed sender with `Get-StartApps` and verifies its setting.
Windows requires a desktop notifier to use the identity of an installed shortcut;
[Microsoft's desktop notification documentation](https://learn.microsoft.com/en-us/windows/win32/shell/enable-desktop-toast-with-appusermodelid)
describes that requirement. The corrected hidden helper and dispatcher test
both recorded their own tags in notification history.

Ben replied "Yes, I see the corrected test" and then supplied a screenshot
"For the record:". The screenshot shows the sender **Windows PowerShell**, the
title **Dual-agent review**, and **Relay notification test: corrected Windows**.
The initial missing-notification screenshot and corrected screenshot are preserved
with verified SHA-256 copies and dispositions in this implementation clone's
`.novc/dual-agent-review-toast-evidence-20260930/manifest.json`. The originals were
`codex-clipboard-419e1d93-24ce-43f7-8930-1f352fc1e7ac.png` and
`codex-clipboard-e1db891f-8261-4e5e-90bd-bc66f0f6cfb4.png` in Ben's temporary directory.
The initial identity diagnostic is `.novc/relay-toast-identity-probe-20260930.json`;
the corrected hidden and dispatcher receipts are in
`.novc/dual-agent-review-toast-fixed-20260930/`. The unregistered synthetic
notification folder `.novc/dual-agent-review/2026-10-03/` contains the dispatcher's
`NEEDS-BEN.md` and `toast-result.json`; it is no review round and changes no Git ref.
Production is enabled; scheduler registration and the first approved window remain
Ben's next actions. The occupied primary clone and both ongoing reviews remain excluded.
Black left the changed Python file clean. Both PowerShell scripts parsed without
errors. The final suite after the helper and production-flag changes passed
1015 tests, 5 skips and 60 subtests using `py/main_test.py -q`; its one warning was
an inability to write pytest's local cache. The scheduler task was independently
checked absent. No generator or product is reached by this fix.

## Future review and measurement

The first real automated round requires Ben's future window approval. The comparison
measurement also needs his decision and record filename. These two prompts are
prepared for that kickoff; their placeholders must be filled from the approved round
and their successor provenance must name the preparing agent, date, source checkout,
required commit, development checkout and integration owner.

1. **Fresh Claude counter-argument:** run at max in a separate checkout detached at
   the verified turn-01 commit. Quote Ben's measurement instruction verbatim. Read
   only the approved window's diff, applicable instructions and turn 01; do not fetch
   or read turn 02. Check findings with read-only sub-agents. Write the counter-argument
   to that checkout's `.novc/` and report input commits and method without pushing.
2. **Independent comparison:** after turn 02 is pushed, an author of neither
   counter-argument reads both counter-arguments and verifies each claimed addition
   or rejection against the same window. Record shared and unique findings, errors,
   evidence, and measured effort. Preserve both counter-arguments in the dated file
   Ben names on `main`, outside the review branch. The executing session owns that
   integration; the dispatcher never reads or writes the comparison.

No production review or measurement begins in this implementation task. The local
mirror, its unique commits, worktrees, logs and failure receipts remain preserved;
retirement requires the repository's verified backup and retirement procedure.
