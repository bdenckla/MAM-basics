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
