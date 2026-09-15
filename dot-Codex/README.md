# dot-Codex

Tracked copies of Ben's authored, user-level Codex configuration. The live files
sit outside every project repository, so this directory is the durable copy in
`MAM-basics`, alongside `dot-claude`.

| Tracked path | Live location |
| --- | --- |
| `user-wide-AGENTS.md` | `~/.Codex/AGENTS.md` |
| `hooks.json` | `~/.Codex/hooks.json` |
| `hooks/check_project_doc_budget.py` | `~/.Codex/hooks/check_project_doc_budget.py` |
| `skills/<name>/` | `~/.agents/skills/<name>/` |

Deployment also creates
`~/.Codex/hooks/expected-user-wide-AGENTS.sha256` from the `origin/main` copy of
`user-wide-AGENTS.md`; the generated fingerprint is not a separately authored tracked file.

**This directory is storage, and project instruction discovery loads none of it.** Repo
maintenance deliberately runs the tracked hook script as a check. These trees moved here from
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

Tracked Codex-only skills:

| Skill | Purpose |
| --- | --- |
| `worktree-forest` | Create, verify, reuse, hand off, and retire pinned multi-repository worktree forests, including the Windows SID `safe.directory` workaround. |
| `prune-Codex-state` (`skills/prune-claude-state/`) | Review Codex auto-memory and plan files for the current repository, cross-check them against live issue state, and propose stale files for deletion. |

The general forest procedure is canonical in `skills/worktree-forest/SKILL.md`.
`MAM-basics/doc/review-findings-2026-09-01.md` records the first forest's history,
and each later forest may carry its own `review-manifest.json` and review reports;
those per-run records describe instances rather than replacing the reusable skill.

The cross-agent `github-issues`, `hebrew-prose` and `verse-links` skills remain canonical under
`dot-claude/skills`; `dot-claude/shared-skills.txt` declares their live Codex destinations under
`~/.agents/skills`. The two state-pruning
skills are deliberately separate: Claude's `prune-claude-state` remains canonical
under `dot-claude/skills`, while Codex's `prune-Codex-state` is canonical here at
`dot-Codex/skills/prune-claude-state/` because it addresses Codex memory and plans.

## Machine-local project-instruction budget

Each machine's `~/.codex/config.toml` must set:

```toml
project_doc_max_bytes = 131072
```

MAM-basics' common repository `AGENTS.md` body exceeds Codex's default 32 KiB project-instruction
budget. The larger limit is shared by the project files selected from the project root down to
the session's working directory, not applied separately to each file. The user-wide
`~/.Codex/AGENTS.md` is loaded outside that project budget and must not be added to the project
total. `config.toml` remains machine-local and untracked; the deployment procedure below does not
install or change it.

The user-level `SessionStart` hook reads the effective working directory from Codex's hook input
and reads `project_doc_max_bytes`, `project_doc_fallback_filenames` and `project_root_markers`
from the machine's `config.toml`. It reproduces the root-to-working-directory file selection and
warns when those selected project files exceed the configured threshold. The hook also compares
the live user-wide `AGENTS.md` with the origin-derived fingerprint installed by the last
successful deployment. It does not query a model, launch a nested Codex process, read the
session transcript or search for Codex's internal truncation-log wording. The normal clean path
only parses one small TOML file, reads the selected instruction files and hashes the user-wide
file, so it remains network-free and normally completes in a small fraction of a second.

This is an estimate of Codex's active project total because hook input supplies the working
directory but not Codex's already-computed byte count or every effective configuration layer.
In particular, a command-line `-c` override or an additional selected environment is not exposed
to the hook. Ordinary local sessions using `config.toml` have the same inputs as the check.

For every instruction file and skill, edit the tracked canonical copy in a MAM-basics development
checkout. Integrate and push the commit before deploying it. `dot-claude/README.md`'s
“Main-sourced deployment and check” is the procedure of record for Claude, Codex, shared and
agent-specific configuration together.

## Main-sourced deployment and check

Codex loads the live copies; Git protects the tracked canonical copies. Ben's decision,
2026-09-13: **do not edit a live copy.** After the canonical change is committed, integrated into
`main` and pushed, run this from `C:/Users/BenDe/GitRepos/MAM-basics`, the primary clone:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config
```

The command fetches `origin`, fails before any live write if the fetch or source validation fails,
and deploys both instruction files, the Codex hook configuration and script, the generated
user-wide-instruction fingerprint, and all tracked skills only from the freshly updated
`refs/remotes/origin/main`. It stages complete replacements and rolls earlier replacements back
if a later replacement fails. The former manual, live-first copy commands are retired.

The read-only form reports `clean`, `drift`, or `not installed` for every Claude and Codex
destination:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config --check
```

Ordinary `py/main_repo_maintenance.py` runs that installation check automatically and then runs
the tracked Codex hook script in maintenance mode. The second check reports the selected project
files and sizes against the threshold from live `config.toml`, and verifies the live user-wide
file against the installed fingerprint. The fetched comparison establishes whether the installed
hook and fingerprint still match current `origin/main`; the startup hook itself intentionally
does no fetch.

Codex treats this user hook as non-managed configuration. After its first installation, or after
its definition changes, use `/hooks` to review and trust the new exact definition; a file-content
check cannot establish Codex's separate trust state.

The Claude cloud-session hook is the declared exception: it sources the cloud session's
checked-out branch, which is `main` only when `main` is that branch. The hook prepositions
`dot-Codex/user-wide-AGENTS.md` as `~/.codex/AGENTS.md`, the import target selected by issue 274's
symmetric-instructions design. It does not install this README, a Codex-only skill, `config.toml`,
or any other Codex state.

Deliberately not tracked here: `auth.json`, `config.toml`, `settings*.json`,
plugin caches, session transcripts, databases, logs, machine permission state,
and other generated or secret-bearing Codex state. Add authored configuration
only after checking that it contains no credentials or machine-local authority.
