# Updates to the symmetric CLAUDE.md and AGENTS.md instructions plan

State: open, first entry 2026-09-15.

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
