---
name: mam-wikisource-refresh
description: Refresh MAM book data from Hebrew Wikisource and regenerate, audit, commit, and publish the dependent products and MAM change logs. Use when Ben asks to download, update, or refresh Hebrew Wikisource book data. Do not use for the separately mirrored MAM introduction, Wikisource bot edits, or Google Sheets refreshes.
---

# Refresh MAM from Hebrew Wikisource

Use this workflow for MAM book-data downloads from Hebrew Wikisource. Coordinate the repositories'
existing entry points; do not create a new orchestration program. A changed refresh is committed
before dependent regeneration, and MAM change logs are committed only after the dependency loop
returns to its final MAM-basics state. The change-log generator compares the latest release with
committed `HEAD`; dirty `MAM-parsed/plus` data is invisible to that comparison.

The commands below run from the verified MAM-basics development checkout. Use
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe` as the interpreter, even when the
development checkout is a linked worktree. Keep network approval, integration, and push
authority within the surrounding user and repository instructions; this skill does not grant
them.

## Verify the checkout

Before downloading anything:

1. Record the absolute top level, current `HEAD`, and branch. Require a branch or establish the
   worktree branch through the applicable worktree procedure.
2. Require clean `git status --porcelain=v1 -z` output, and record the starting `HEAD` for the
   collision check before the first commit.
3. When a required source commit was supplied, require that commit to equal `HEAD` or be an
   ancestor. Refresh `origin/main` when the surrounding instructions require a current remote
   baseline.
4. Confirm that the primary interpreter above exists. Never copy, junction, or symlink the
   primary `.venv` into a worktree.
5. On Windows when repository ownership differs, pass the development checkout's exact absolute
   path through `git -c "safe.directory=<DEV>" -C "<DEV>"` on every Git invocation. Never add a
   global trust exception.

Keep one writer in the checkout. If the starting state is dirty or the checkout identity is not
the expected one, stop before the download.

## Download and decide whether work exists

Run the book-data download without `--force-download`:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_download.py fr-wikisource
```

Use `--force-download` only when Ben explicitly requests a forced download. After the command,
inspect NUL-delimited Git status before running a generator. Require every changed or untracked
path to be an expected output of the book-data download; an unexpected path blocks the workflow.
If status is completely clean, report that the Wikisource data is already current and stop: do
not run mega, commit, or push. If no tracked file changed but expected untracked output remains,
report that unexpected residue and stop for cleanup or direction; do not run mega, commit, or
push.

## Complete the dependent refresh

When tracked Wikisource data changed, read and follow
[references/dependent-refresh.md](references/dependent-refresh.md) before running a generator.
That reference governs the complete MAM-basics → MAM-private → phonetic-hbo → MAM-basics
dependency loop, the separate change-log commit, final gates, push order, and clean remote-state
check.

The downstream preflight happens before any downstream write. A clean checkout is necessary but
does not prove that the checkout is unowned: if MAM-private or phonetic-hbo is dirty, is attached
to another active task, or cannot be assigned unambiguously to this refresh, stop and require a
handoff. Expected dependent regeneration is regeneration, not a failed census. A dependent
generator that legitimately produces no diff needs no commit; never create an empty commit.

Any unexplained diff, failed gate, stale input, changed recorded `HEAD`, or ambiguous ownership
stops the workflow before pushing. The surrounding user and repository instructions govern
integration and push authority; this skill does not grant them.

## Separate workflows

- The separately mirrored MAM introduction is not this workflow. Read
  `in/mam-ws-intro/README.md` completely and follow its independent refresh procedure; do not
  treat the bare `py/main_download.py fr-ws-intro` command as the whole procedure.
- Wikisource bot edits are outward-facing edits with their own workflow.
- Google Sheets refreshes are a separate data source and workflow.

This skill's canonical copy is `MAM-basics/dot-claude/skills/mam-wikisource-refresh/`. It is
shared with Codex through `dot-claude/shared-skills.txt` and reaches both live skill homes only
through the deployment procedure in `MAM-basics/dot-claude/README.md`.
