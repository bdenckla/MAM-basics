# PLAN — make repository- and user-level CLAUDE.md and AGENTS.md symmetric via @ imports

State: live.
Updates and later status: [PLAN-symmetric-CLAUDE-and-AGENTS-instructions-update.md](PLAN-symmetric-CLAUDE-and-AGENTS-instructions-update.md).

*Agent-written. A Claude session filed the original report on 2026-09-11 at Ben's request. Ben decided on 2026-09-12 to expand the work from repository-level symmetry to user-level symmetry and to use Claude Code's `@` import syntax at both levels. Implementation is in progress: the Claude cloud hook's prepositioning of the future user-level import target, the MAM-basics repository-level conversion, and the Codex project-instruction startup and maintenance checks reached `main` in commits `8065daec`, `f3c7b05e`, and `52b91ac0` by 2026-09-15. The user-level wrapper conversion, the MAM-private repository-level conversion, and the fresh-session and real Claude-cloud verification remain.*

## Decision: `AGENTS.md` is the common file at both levels

Use one common `AGENTS.md` body at each level. Codex loads each `AGENTS.md` natively; Claude Code loads the same body through a minimal `CLAUDE.md` wrapper.

```text
Repository level
  MAM-basics/CLAUDE.md  -> @AGENTS.md
  MAM-basics/AGENTS.md  -> common repository instructions

User level
  ~/.claude/CLAUDE.md   -> @~/.codex/AGENTS.md
  ~/.codex/AGENTS.md    -> common user instructions
```

The tracked user-level copies remain deliberately prefixed so MAM-basics does not auto-load them merely because they are stored in the repository:

```text
dot-claude/user-wide-CLAUDE.md  -> tracked copy of the Claude wrapper
dot-Codex/user-wide-AGENTS.md   -> tracked copy of the common user instructions
```

MAM-private should use the repository-level pattern too: its `CLAUDE.md` becomes `@AGENTS.md`, and its new `AGENTS.md` holds its common repository instructions.

Small Claude-specific or Codex-specific sections may remain in a common `AGENTS.md`. Give each section an exact heading such as `Claude Code only: cloud SessionStart installation` or `Codex only: worktree handoff`, so the agent that does not use the section can identify it as inapplicable. Keeping these rare, short sections in the common file is preferable to turning either `CLAUDE.md` wrapper into a second instruction body. If agent-specific content later becomes substantial, move the substantial content to that agent's native skill or other explicitly named mechanism; do not grow two parallel copies of the shared rules.

## Why the change is needed

The asymmetry measured on 2026-09-11 was real:

1. At user level, `~/.claude/CLAUDE.md` and `~/.codex/AGENTS.md` both existed, but their content was not symmetric. The then-live Codex file lacked four Claude sections and parts of nine more; the remediation plan recorded this as D3.
2. At repository level, MAM-basics and MAM-private had `CLAUDE.md` files and no `AGENTS.md` files. An ordinary Codex session therefore missed most repository-specific instructions unless its prompt explicitly told it to read `CLAUDE.md`.
3. MAM-basics' repository instructions exceeded Codex's default combined project-instruction budget of 32 KiB. Moving the body to `AGENTS.md` without raising the budget would load only part of the intended file.

Those measurements are historical evidence, not implementation inputs. Before editing, remeasure the current live files, tracked copies, repository files, exact checkout paths, and commits. In particular, compare both live user files with both tracked copies before copying in either direction; never overwrite a newer live rule with an older tracked copy.

## Implementation plan

### 1. Establish the exact inputs before merging instruction bodies

Work from verified checkouts of:

- `C:/Users/BenDe/GitRepos/MAM-basics`, or the exact MAM-basics worktree assigned to the implementing task.
- `C:/Users/BenDe/GitRepos/MAM-private`, or the exact MAM-private worktree assigned to the implementing task.
- `C:/Users/BenDe/.claude/CLAUDE.md`.
- `C:/Users/BenDe/.codex/AGENTS.md`.

Record each repository's HEAD, branch or detached-HEAD state, and `git status --porcelain`. Recheck immediately before the first edit. Re-measure byte counts and list headings rather than relying on the 2026-09-11 figures. Compare each live user file against its tracked copy in MAM-basics.

Make a section-level table for the two user files. Classify every difference as shared, Claude Code only, Codex only, stale, or contradictory. Use Ben's latest dated decision where two passages conflict; stop for Ben's decision where the repository does not already settle the conflict. The resulting common user file must be the resolved union, not today's Codex file copied over today's Claude file.

### 2. Build and deploy the common user-level file

Put the resolved union in `C:/Users/BenDe/.codex/AGENTS.md`. Make agent-specific applicability explicit in the relevant headings or first sentences. Update the common file's opening deployment instructions so they describe one common body and one Claude wrapper rather than two independent instruction bodies.

Copy the common body to `MAM-basics/dot-Codex/user-wide-AGENTS.md`. Replace both `C:/Users/BenDe/.claude/CLAUDE.md` and `MAM-basics/dot-claude/user-wide-CLAUDE.md` with the minimal wrapper:

```text
@~/.codex/AGENTS.md
```

Update `dot-claude/README.md`, `dot-Codex/README.md`, and the common file's own preamble so the edit, copy, comparison, and drift-check procedure has one content source. The procedure must still compare the live common file with its tracked copy and the live wrapper with its tracked copy. `C:/Users/BenDe/.codex/config.toml` remains machine-local and untracked.

This step writes outside a repository and changes what future Claude and Codex sessions load. Treat the live deployment as a separate verification target, not as a side effect of editing the tracked copies.

### 3. Make Claude cloud sessions install the user-level import target

The wrapper's import target does not exist in a fresh Claude cloud container merely because `dot-Codex/user-wide-AGENTS.md` is present in the checkout. Update `.claude/hooks/install-user-config.sh` so its remote-only path independently installs:

```text
dot-Codex/user-wide-AGENTS.md          -> ~/.codex/AGENTS.md
dot-claude/user-wide-CLAUDE.md         -> ~/.claude/CLAUDE.md
dot-claude/skills/hebrew-prose/        -> ~/.claude/skills/hebrew-prose/
```

Create `~/.codex/AGENTS.md` before installing or reporting the Claude wrapper. The presence checks must treat the wrapper and its import target independently: an existing `~/.claude/CLAUDE.md` does not make a missing `~/.codex/AGENTS.md` acceptable. Update every success, already-present, missing-source, and partial-install banner to name all three installed resources accurately.

Update `doc/user-level-config-in-cloud-sessions.md` to describe the new three-resource installation. Preserve the local `CLAUDE_CODE_REMOTE` guard and the rule that the hook never overwrites an existing live file.

The cloud hook is a code path that cannot be fully exercised on this Windows machine. Run its existing fake-home cases locally, add the new common-file and partial-install cases, and run `bash -n`; then label the result locally verified but cloud-unverified until a real Claude cloud session confirms it.

### 4. Convert MAM-basics repository instructions

Create `MAM-basics/AGENTS.md` from the current repository `CLAUDE.md`, then replace `MAM-basics/CLAUDE.md` with:

```text
@AGENTS.md
```

Do not copy the body blindly. Rewrite loader-specific statements and paths so both agents receive accurate directions. Examples include the separate live paths for the shared `hebrew-prose` skill (`~/.claude/skills/hebrew-prose/` for Claude and `~/.agents/skills/hebrew-prose/` for Codex), Claude's cloud hook, and Codex worktree operations. Use explicit agent-specific headings where a common formulation would be false.

Add a short compatibility note near the top of the common repository file: historical prose that cites “`CLAUDE.md`'s section X” now means section X in the common `AGENTS.md` imported by `CLAUDE.md`. Do not mechanically rewrite every historical citation. In particular, do not edit a finished dated document; if a finished dated document genuinely needs correction, follow the `<stem>-update.md` rule.

Set `project_doc_max_bytes = 131072` in `C:/Users/BenDe/.codex/config.toml` before treating the Codex side as working. Document the required machine-local setting in `dot-Codex/README.md`. Re-measure the final combined project instruction size and stop if 128 KiB no longer leaves room for the actual discovery chain; do not assume the 2026-09-11 file size remains current.

### 5. Convert MAM-private repository instructions

Apply the same repository pattern in the verified MAM-private checkout: move the common body into `AGENTS.md`, reduce `CLAUDE.md` to `@AGENTS.md`, and rewrite any agent-specific wording precisely. MAM-private's body measured about 13 KiB on 2026-09-11 and fit the default budget, but verify its current size and its combined discovery-chain size anyway.

Keep the repositories' own instructions separate. “Common” means common to Claude and Codex within one scope; it does not mean combining MAM-basics-specific and MAM-private-specific rules into one cross-repository file.

### 6. Verify content equality and fresh-session behavior

Static comparisons are necessary but not sufficient:

1. Confirm that each `CLAUDE.md` wrapper contains only its intended `@` import plus a final newline.
2. Confirm that the live user common file and tracked common file are byte-identical, and that the live Claude wrapper and tracked wrapper are byte-identical.
3. Confirm that the common files do not import their wrappers, which would create a cycle.
4. Search current, non-historical documentation for deployment directions that still describe two independent user instruction bodies. Update those live descriptions; leave finished dated documents unchanged.
5. Start fresh Claude Code and Codex sessions in MAM-basics and MAM-private. Ask each session for a rule from near the end of both the user-level and repository-level common files. Checking a tail rule detects truncation and proves more than checking only that a filename was discovered.
6. In a real fresh Claude cloud session, confirm that the hook creates `~/.codex/AGENTS.md` and `~/.claude/CLAUDE.md`, that Claude follows the user-level import, that Claude follows the repository-level import, and that `hebrew-prose` remains available. Record the container, checkout commit, file hashes or byte counts, and the exact tail rules observed.

Claude Code's official documentation recommends `@AGENTS.md` as the Windows-friendly way for `CLAUDE.md` to follow `AGENTS.md`, and documents `@` imports from a user's home directory. The same documentation says Cowork desktop skips user-scope imports outside its working directory. This plan targets Claude Code local and cloud sessions. Record Cowork desktop as unsupported by the user-level import unless Ben separately expands the scope; do not restore a second full instruction copy as an unrequested Cowork workaround.

### 7. Run repository checks, commit, and integrate

For the MAM-basics hook, run the dedicated fake-home harness and syntax check before the repository-wide gate. Because the branch changes executable hook code as well as instruction files, follow MAM-basics' worktree integration rule: merge `main` into the worktree branch, run `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py` from the worktree root, inspect the complete generated diff, and treat every unexplained change as a failure. Commit explained changes before fast-forwarding the primary clone and pushing `main` at archival.

Commit MAM-private separately after its own applicable checks. Do not use one repository's clean status or commit as evidence for the other repository. Do not rewrite history to roll back: restore the prior full `CLAUDE.md` bodies in new commits if rollback is needed.

## Expected product and action risk

The expected repository changes alter agent instructions and cloud-session setup; they are not expected to change MAM-parsed, MAM-with-doc, MAM-simple, gh-pages, or another declared MAM-basics product. Reconfirm that expectation against the then-current `py/product_scopes.py` and treat any product diff as a finding.

The actions still touch the separate hard-to-undo axis: live writes under `~/.claude/` and `~/.codex/` affect every future session, and the Claude cloud hook cannot be fully verified locally. Keep the tracked copies, hashes, fresh-session checks, and cloud verification as receipts. Updating this issue is also outward-facing; the issue should remain open until the implementation and both agents' fresh-session checks are complete.

## Sources

- [Custom instructions with AGENTS.md (OpenAI)](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [How Claude remembers your project (Anthropic)](https://code.claude.com/docs/en/memory)
- [openai/codex `codex-rs/core/src/agents_md.rs`](https://github.com/openai/codex/blob/main/codex-rs/core/src/agents_md.rs)
- [openai/codex `codex-rs/config/defaults.toml`](https://github.com/openai/codex/blob/main/codex-rs/config/defaults.toml)

Edited on 2026-09-15 by a Codex session, with Ben's approval, to replace the stale claim that no implementation had begun with the current completed and remaining scope.
