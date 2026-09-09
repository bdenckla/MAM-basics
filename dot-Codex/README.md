# dot-Codex

Tracked copies of Ben's authored, user-level Codex configuration. The live files
sit outside every project repository, so this directory is the durable copy in
`MAM-basics`, alongside `dot-claude`.

| Tracked path | Live location |
| --- | --- |
| `user-wide-AGENTS.md` | `~/.Codex/AGENTS.md` |
| `skills/<name>/` | `~/.agents/skills/<name>/` |

**This directory is storage, and MAM-basics loads none of it.** These trees moved here from
`github-misc` on 2026-09-09; `dot-claude/README.md` gives the reason, which is about Claude's
cloud sessions rather than about Codex, and says why both trees moved together rather than
only the Claude one. The commits stay in `github-misc`'s history, so a `github-misc <sha>`
citation in any of these files is right as written.

`user-wide-AGENTS.md` contains the cross-project instructions Codex loads at session start.
The live file name is plural: `AGENTS.md`, not `AGENT.md`. The tracked copy carries the
`user-wide-` prefix so that no second `AGENTS.md` sits inside MAM-basics to be mistaken for the
repository's own agent instructions.

`skills/` contains user-wide Codex skills. Codex initially sees each skill's name
and description and reads the full `SKILL.md` only when the skill is invoked or
the task matches its description. That makes a skill the right home for a
repeatable, specialized workflow whose details do not belong in every session's
prompt.

Tracked Codex-only skill:

| Skill | Purpose |
| --- | --- |
| `worktree-forest` | Create, verify, reuse, hand off, and retire pinned multi-repository worktree forests, including the Windows SID `safe.directory` workaround. |
| `prune-Codex-state` (`skills/prune-claude-state/`) | Review Codex auto-memory and plan files for the current repository, cross-check them against live issue state, and propose stale files for deletion. |

The general forest procedure is canonical in `skills/worktree-forest/SKILL.md`.
`MAM-basics/doc/review-findings-2026-09-01.md` records the first forest's history,
and each later forest may carry its own `review-manifest.json` and review reports;
those per-run records describe instances rather than replacing the reusable skill.

The cross-agent `hebrew-prose` skill remains canonical under `dot-claude/skills`;
its live Codex-visible copy is under `~/.agents/skills`. The two state-pruning
skills are deliberately separate: Claude's `prune-claude-state` remains canonical
under `dot-claude/skills`, while Codex's `prune-Codex-state` is canonical here at
`dot-Codex/skills/prune-claude-state/` because it addresses Codex memory and plans.

For a shared skill, edit the live Claude copy `~/.claude/skills/<name>/` first, then copy that
complete tree out to the canonical `dot-claude/skills/<name>/` and to `~/.agents/skills/<name>/`.
`dot-claude/README.md`'s "Shared-skill deployment to Claude and Codex" is the four-step procedure
of record, and this paragraph deliberately does not restate it; its two directory comparisons are
required before committing a shared-skill change, and they prove that Claude and Codex will
receive the same instructions. **The order was canonical-first here and in `dot-claude/README.md`
until 2026-09-09**, when Ben settled both documents on the live-first order that sessions were
already using — `dot-claude/README.md` says which commits, and notes that which order is chosen
matters far less than that one is specified.

## Live and tracked copies

Codex loads the live copies; Git protects the tracked copies. Nothing synchronizes
the two automatically. After editing the live `AGENTS.md`, copy it back here and
commit:

```powershell
Copy-Item "$HOME/.Codex/AGENTS.md" "$HOME/GitRepos/MAM-basics/dot-Codex/user-wide-AGENTS.md" -Force
```

After editing the live forest skill, copy its file back here and commit:

```powershell
Copy-Item "$HOME/.agents/skills/worktree-forest/SKILL.md" "$HOME/GitRepos/MAM-basics/dot-Codex/skills/worktree-forest/SKILL.md" -Force
```

After editing the live Codex state-pruning skill, copy its file back here and commit:

```powershell
Copy-Item "$HOME/.agents/skills/prune-claude-state/SKILL.md" "$HOME/GitRepos/MAM-basics/dot-Codex/skills/prune-claude-state/SKILL.md" -Force
```

Compare the live and tracked instruction files with:

```powershell
git diff --no-index -- "$HOME/.Codex/AGENTS.md" "$HOME/GitRepos/MAM-basics/dot-Codex/user-wide-AGENTS.md"
```

Compare the live and tracked forest skills with:

```powershell
git diff --no-index -- "$HOME/.agents/skills/worktree-forest" "$HOME/GitRepos/MAM-basics/dot-Codex/skills/worktree-forest"
```

Compare the live and tracked Codex state-pruning skills with:

```powershell
git diff --no-index -- "$HOME/.agents/skills/prune-claude-state" "$HOME/GitRepos/MAM-basics/dot-Codex/skills/prune-claude-state"
```

The nonzero exit status from `git diff --no-index` means the copies differ; no
output means the copies match.

Deliberately not tracked here: `auth.json`, `config.toml`, `settings*.json`,
plugin caches, session transcripts, databases, logs, machine permission state,
and other generated or secret-bearing Codex state. Add authored configuration
only after checking that it contains no credentials or machine-local authority.
