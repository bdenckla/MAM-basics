# Updates to the symmetric CLAUDE.md and AGENTS.md instructions plan

State: executed, first entry 2026-09-15.

This file is the dynamic home for later progress, State, scope changes, measurements, and dispositions for [the frozen base plan](PLAN-symmetric-CLAUDE-and-AGENTS-instructions.md). Append later dated entries here and correct stale present-tense claims here while the base remains tracked.

## Integrated MAM-basics progress — 2026-09-15

Written by a Codex session on 2026-09-15, at Ben's request.

Progress is integrated into `main` through [`52b91ac0`](https://github.com/bdenckla/MAM-basics/commit/52b91ac00bfe4bea99a2b94805f9a3ed48e0a15e):

1. [`8065daec`](https://github.com/bdenckla/MAM-basics/commit/8065daec) updated the Claude cloud SessionStart hook to install `~/.codex/AGENTS.md` independently beside the current Claude user file and shared `hebrew-prose` skill. Its syntax and fake-home cases passed locally; a real Claude cloud container has not verified it yet.
2. [`f3c7b05e`](https://github.com/bdenckla/MAM-basics/commit/f3c7b05e) created MAM-basics' common repository `AGENTS.md` and reduced its `CLAUDE.md` to the `@AGENTS.md` wrapper.
3. [`52b91ac0`](https://github.com/bdenckla/MAM-basics/commit/52b91ac00bfe4bea99a2b94805f9a3ed48e0a15e) added the Codex SessionStart check and repository-maintenance checks for the combined root-to-working-directory `AGENTS.md` byte count, the live `project_doc_max_bytes` value from `config.toml`, the installed hook files, and the user-wide `AGENTS.md` fingerprint derived from `origin/main`.

Verification at integration:

- The canonical test suite passed with 988 tests passed and 5 semantic skips before integration.
- The required MAM-basics mega gate completed all 54 steps in 247.1 seconds and left no tracked generated diff.
- The primary checkout and `origin/main` both reached `52b91ac00bfe4bea99a2b94805f9a3ed48e0a15e` by fast-forward.
- The `origin/main`-sourced user-config deployment completed, and its read-only follow-up reported `USER_CONFIG_PROBLEM_COUNT=0`.
- The live maintenance check measured 80,412 combined project-instruction bytes against the configured 131,072-byte limit, matched the user-wide `AGENTS.md` to its origin-derived fingerprint, and reported `CODEX_INSTRUCTION_PROBLEM_COUNT=0`.
- The mega gate produced no declared MAM-basics product change.

The issue remains open. The user-level `CLAUDE.md` wrapper conversion, the MAM-private repository conversion, the fresh Claude and Codex session checks, and a real Claude cloud-session check remain. The new non-managed Codex hook must also be trusted through `/hooks` before Codex will run it automatically; that trust state cannot be verified from the deployed files.

## MAM-private implementation spin-off — 2026-09-16

Recorded by a Codex session on 2026-09-16 at Ben's request.

The MAM-private implementation has been spun off to
[MAM-private#26](https://github.com/bdenckla/MAM-private/issues/26) and its detailed
[`doc/PLAN-consolidate-agent-instructions.md`](https://github.com/bdenckla/MAM-private/blob/main/doc/PLAN-consolidate-agent-instructions.md),
established by MAM-private commit
[`8a3e7eb5272bb5301fdf7993994b1ddf48ab074e`](https://github.com/bdenckla/MAM-private/commit/8a3e7eb5272bb5301fdf7993994b1ddf48ab074e).
The MAM-private implementation is no longer owned by the MAM-basics issue 274 plan family.

The MAM-private plan gates its execution on completion and deployment of the user-level
conversion. The implementing MAM-private session must then re-inspect the final live and
canonical user-level files before deciding what MAM-private can remove.

The remaining MAM-basics scope is the user-level `CLAUDE.md` wrapper conversion, fresh local
Claude Code and Codex verification, and real Claude cloud verification.

## User-level common-body conversion and deployment — 2026-09-16

Recorded by a Codex session on 2026-09-16 at Ben's request.

The user-level conversion is implemented and deployed. Before editing, the session remeasured the
2026-09-16 baseline at MAM-basics commit
`a7cb3e979e809e32fd27d3d11a3d336ea36f48ab`: the canonical common file was 16,252 bytes, the
canonical Claude file was 121,892 bytes, and each canonical file remained byte-identical to its
live destination. Current `main` and `origin/main` were still at that baseline.

The old Claude body was reconciled section by section against the compact Codex body and the
canonical skills. No genuine policy conflict required a new decision. The resolved common body
preserves the unique live rules for authored forward-slash paths, successor-prompt authorship,
finding dispositions, and shared checkout and virtual-environment safeguards. The Claude task-chip
and cloud-installation material remains under explicit `Claude Code only` headings. Detailed
GitHub-issue, Hebrew-prose, repository-topology, and Codex-worktree procedures remain routed to
their canonical skills instead of being copied back into the always-loaded body.

Commit
[`d695966be8daea270f85424cb77d06f3b92a873d`](https://github.com/bdenckla/MAM-basics/commit/d695966be8daea270f85424cb77d06f3b92a873d)
made `dot-Codex/user-wide-AGENTS.md` the single canonical user-level instruction body and reduced
`dot-claude/user-wide-CLAUDE.md` to exactly `@~/.codex/AGENTS.md` followed by one LF. The commit
also corrected the deployment READMEs, current GitHub-issue skill references, and two explanatory
Python docstrings. Inspection confirmed that `py/repo_util/user_config_sync.py` and
`.claude/hooks/install-user-config.sh` already deploy, compare, and bootstrap the common body and
wrapper independently, so no executable behavior changed. Black left both docstring-only Python
files unchanged. Per Ben's documentation and instruction verification policy, no mega run, suite,
targeted document lint, or other repository lint was run; the complete diff was reviewed manually,
and `git diff --check` passed.

The worktree branch was merged with current `main`, the primary clone was confirmed clean at the
expected baseline, and the primary clone fast-forwarded and pushed `main` to `d695966b`. The
authorized deployment then ran from `C:/Users/BenDe/GitRepos/MAM-basics` and reported
`USER_CONFIG_DEPLOYED_COUNT=5`, sourcing
`refs/remotes/origin/main@d695966be8daea270f85424cb77d06f3b92a873d`. Its immediate read-only
follow-up reported every destination clean and `USER_CONFIG_PROBLEM_COUNT=0`.

Independent read-back recorded these final canonical and live measurements:

| File | Bytes | SHA-256 | Result |
| --- | ---: | --- | --- |
| common `AGENTS.md` | 19,856 | `92e929ed58527634de2c04087208f4f2b4597a5276e3d4df4ec7180d09db1443` | canonical and live files byte-identical |
| Claude wrapper | 20 | `38a1085f3a53b4027ff2e96fad50daa2c372c17f5fcf0f973298316435e2ead1` | canonical and live files byte-identical; bytes end in one LF |

The MAM-private issue 26 dependency on the deployed user-level conversion is now satisfied, but
MAM-private remains outside this plan family's scope. This update file remains **State: open**.
MAM-basics issue 274 now has exactly three remaining checks:

1. A fresh local Claude Code session check.
2. A fresh local Codex session check.
3. A real Claude cloud-session check.

The implementing session did not perform or claim any fresh-session check because its startup
context predates the deployment.

## Fresh local Codex startup verification — 2026-09-16

Recorded by a Codex session on 2026-09-16 at Ben's request.

Ben supplied the response from a newly started local Codex task. Before using tools, that task
correctly named and summarized the final user-level H2, `Show local artifacts with file links`,
and the final MAM-basics H2, `This is the only repository instruction body`. It also correctly
identified `dot-Codex/user-wide-AGENTS.md` as the canonical tracked user-level common body,
explained that Claude Code receives that body through the minimal tracked
`dot-claude/user-wide-CLAUDE.md` wrapper, distinguished the live deployed Claude file from its
canonical source, and identified the MAM-basics `SessionStart` hook as the Claude cloud-session
installer.

The fresh local Codex startup check therefore passed. This update file remains **State: open**.
MAM-basics issue 274 now has exactly two remaining checks:

1. A fresh local Claude Code session check.
2. A real Claude cloud-session check.

No fresh local Claude Code or Claude cloud-session verification has occurred.

## Fresh local Claude Code startup verification — 2026-09-17

Recorded by a Codex session on 2026-09-17, at Ben's request.

The development checkout was the primary clone at
`C:/Users/BenDe/GitRepos/MAM-basics`, on clean `main` at
`a4968fd7b8eac92caf4df6736b128b5a1e1e1b13`. The required deployment comparison
reported
`USER_CONFIG_SOURCE=C:/Users/BenDe/GitRepos/MAM-basics refs/remotes/origin/main@a4968fd7b8eac92caf4df6736b128b5a1e1e1b13`
and `USER_CONFIG_PROBLEM_COUNT=0`.

The Codex implementing session started a brand-new, non-persistent local Claude
Code process from that checkout, using the installed Claude Code 2.1.274 binary
with tools disabled and the prescribed prompt unchanged. Ben did not supply a
separate response. The process produced no instruction-content response and did
not reach model inference. Its complete result reported:

> Failed to authenticate: OAuth session expired and could not be refreshed

The fresh local Claude Code startup check therefore did not pass. Because no
model response was produced, none of the content acceptance criteria could be
evaluated: the process did not name or summarize either final H2, identify the
canonical common body or tracked wrapper, explain the two live deployed files,
identify the Claude cloud-session installer, or report whether startup produced
an import, truncation, or instruction-loading warning. The exact failed
criterion was the prerequisite that the fresh Claude Code session produce a
startup-only response from its loaded instructions.

This update file remains **State: open**. MAM-basics issue 274 still has exactly
two remaining checks:

1. A successful fresh local Claude Code session check after local Claude Code
   authentication is restored.
2. A real Claude cloud-session check.

The issue body remains current and was not edited.

## Successful fresh local Claude Code startup verification — 2026-09-17

Recorded by a Codex session on 2026-09-17, at Ben's request.

Ben supplied the complete response unchanged from a newly started interactive
local Claude Code session rooted at `C:/Users/BenDe/GitRepos/MAM-basics`. Before
using a tool or reading a file, that session correctly named and summarized the
final user-level H2, `Show local artifacts with file links`, and the final
MAM-basics H2, `This is the only repository instruction body`. It identified
`dot-Codex/user-wide-AGENTS.md` as the tracked canonical common body and
`dot-claude/user-wide-CLAUDE.md` as the tracked wrapper, distinguished both from
the live `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md` files, and explained that
the live Claude wrapper imports the live common body. It also identified
`.claude/hooks/install-user-config.sh` as the Claude cloud-session installer.
The response reported no import, truncation, or instruction-loading warning.

The tool-free verification response did not query its instantaneous Git HEAD
while other work was advancing the primary checkout. The earlier preflight had
verified the relevant deployed configuration at
`a4968fd7b8eac92caf4df6736b128b5a1e1e1b13` with
`USER_CONFIG_PROBLEM_COUNT=0`. Before recording this successful response, Git
history confirmed that none of `AGENTS.md`, `CLAUDE.md`, the two tracked
user-level instruction files, the cloud hook, or its settings registration
changed between that commit and the recording baseline
`163ca7827d111b1a7c1ff66da534c0a3f8ce887d`. The exact instantaneous commit is
therefore not claimed, but the instruction content under test is pinned to both
verified endpoints.

The fresh local Claude Code startup check passed. The earlier failed command-line
attempt remains above as historical evidence and is superseded by this successful
interactive check.

## Real Claude cloud-session verification — 2026-09-17

Recorded by a Codex session on 2026-09-17, at Ben's request.

Ben supplied two complete responses unchanged from a fresh Claude Code cloud
session. The first response used no tool and read no file. Its startup context
contained the full-success `SessionStart` banner for installing the common body,
Claude wrapper, and `hebrew-prose` skill. It correctly reported both imported
instruction bodies through their final H2 sections, found `hebrew-prose` in the
available-skills list, and reported no import, truncation, or instruction-loading
warning.

The second response used read-only tools and recorded Claude Code 2.1.274 in
container hostname `vm`, with `HOME=/root`, `CLAUDE_CODE_REMOTE=true`, and the
repository at `/home/user/MAM-basics`. The checked-out branch was
`claude/optimistic-ramanujan-84xvh7` at
`92f73fa321f17c5d65950c304a6c632401315e24`; the user-level conversion commit
`d695966be8daea270f85424cb77d06f3b92a873d` was an ancestor.

The cloud filesystem evidence reported:

- `dot-Codex/user-wide-AGENTS.md` and `/root/.codex/AGENTS.md` were both 21,291
  bytes with SHA-256
  `e3db8fb6e2a7484cb0d1589b9e4a2cec2aca1308126052437329fce4e5453360`.
- `dot-claude/user-wide-CLAUDE.md` and `/root/.claude/CLAUDE.md` were both 20
  bytes with SHA-256
  `38a1085f3a53b4027ff2e96fad50daa2c372c17f5fcf0f973298316435e2ead1`.
- The tracked and installed `hebrew-prose` trees contained the same seven files
  and 105,784 bytes; every corresponding file hash matched.
- Both `cmp` checks and the recursive skill-tree `diff` produced no output. The
  user wrapper contained exactly `@~/.codex/AGENTS.md` plus one LF, and the
  repository wrapper contained exactly `@AGENTS.md` plus one LF.
- `.claude/settings.json` registered the cloud installer for `SessionStart`.
  Repository status was clean before and after verification, and HEAD did not
  move.

The real Claude cloud-session check passed. The successful local Codex, local
Claude Code, and Claude cloud checks now complete every remaining verification
owned by this plan family.

## Completion disposition — 2026-09-17

Recorded by a Codex session on 2026-09-17, at Ben's request.

This update file is now **State: executed**. The common user-level instruction
body, both Claude wrappers, the MAM-basics common repository body, the local
deployment procedure, and the cloud bootstrap have all been implemented and
verified through fresh local Codex, fresh local Claude Code, and real Claude
cloud sessions. MAM-private remains separately tracked by
[MAM-private issue 26](https://github.com/bdenckla/MAM-private/issues/26).
MAM-basics issue 274 has no remaining work and may be closed.
