# Automated dual-agent review operations

State: live; core implemented and verified 2026-09-30; D13 approved 2026-09-30; live rollout pending.

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
the facts-only rule, measurement, real-worker rehearsal and future review window
retain their recorded prerequisites.

## Configuration and operation

`in/dual_agent_review_automation.json` sets launch rules, caps, timeouts, and CLI
discovery; `--automation-config <absolute-path>` selects an explicit alternative.
`production_enabled` remains false until the real-worker rehearsal passes;
both production kickoff and scheduler registration refuse. D13 is approved.
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

## Scheduler registration

The registration script creates a task every 3 minutes, only while Ben is logged on,
with limited privilege and `IgnoreNew` instance handling. `pythonw.exe` starts the
tick without a console window. Registration remains Ben's action after live worker
verification. This implementation does not enable an unattended task.

```powershell
& C:/Users/BenDe/GitRepos2/MAM-basics/misc/register-dual-agent-review-task.ps1 -Repository C:/Users/BenDe/GitRepos2/MAM-basics
```

## Verification and remaining rollout

The changed Python passed Black. The targeted checks passed 4 tests; the final full
suite passed 1015 tests, with 5 skips and 60 subtests, using `py/main_test.py -q`.
Pytest reported one cache-write permission warning; no test failed. Both PowerShell
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
| P1: Claude effort and sub-agents | Passed the renewed-login and full capability checks. Opus 5.5 at max verified root, HEAD, branch and NUL status, completed one foreground Explore checker, and wrote the ignored capability JSON. Terminal statistics confirm one completed checker, zero background checkers and no nested child. The native PowerShell Git rules passed; an optional shell-version expression was denied and its ineffective allow rule was removed. Real turns are in progress. |
| P2: Codex model and effort | Passed the full capability check after removing `--ephemeral`: native Git reads, one completed checker and native JSON write succeeded. The saved `turn_context` confirms `gpt-6.1-sol`, `xhigh`, workspace-write and network disabled. Its thread is `01a0f49c-77ad-7841-9f6d-b1de819b4f5a`. Real-turn verification remains. |
| P3: foreign-file gate | Passed against independent Git status evidence in the local check. |
| P4: movement and failures | The gate rejected a worker push observed independently on the bare remote. Forced dispatcher push-failure notification and commit recovery passed. A real-worker remote-movement rehearsal remains. |
| P5: closure | The local three-turn check requested acknowledgment, closed, and did not launch a fourth worker. |
| P6: notifications and hidden launch | Both hidden WinRT notification tests returned 0; visual receipt is unconfirmed. Ben was asked whether he saw the notification titled Dual-agent review with Relay rehearsal notification test. The hidden `pythonw.exe` idle tick exited 0 with an empty registry. The scheduled task has not been registered. |
| P7: private SSH | Deferred until both ongoing reviews finish and Ben approves private rollout. No private fetch or push was attempted. |
| P8: Codex worktree and instructions | Passed instructions, clean HEAD and branch, and foreground checker verification in the full rehearsal clone. Worktree verification awaits its real turn. |

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
The source implementation registry is absent;
no production round was started. The primary clone was not fast-forwarded. Production remains
disabled until the real-worker checks pass; Ben has approved D13. Core commit
`1a50d4b6d132a66dcb9d54d9b9275cd62fc2d580` was pushed to `main`. Main-sourced
configuration deployment installed only the new Claude agent file; every existing
instruction, hook and skill was already clean. The subsequent
`--sync-user-config --check` returned zero problems.
Worker fix commit `05e109cf579d97404ff596a1f8ff78394d077c20` is on `origin/main`;
its complete deployment installed only the changed Claude agent definition and
the follow-up check again returned zero problems. The latest full suite passed
1015 tests, 5 skips and 60 subtests without a warning.

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

No live review or measurement begins in this implementation task.
