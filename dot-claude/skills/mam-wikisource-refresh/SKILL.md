---
name: mam-wikisource-refresh
description: Refresh MAM book data from Hebrew Wikisource and regenerate, audit, commit, and publish the dependent products and MAM change logs. Use when Ben asks to download, update, or refresh Hebrew Wikisource book data. Do not use for the separately mirrored MAM introduction, Wikisource bot edits, or Google Sheets refreshes.
---

# Refresh MAM from Hebrew Wikisource

Use this workflow for MAM book-data downloads from Hebrew Wikisource. The workflow has two
local commits because the change-log generator compares the latest release with committed
`HEAD`; dirty `MAM-parsed/plus` data is invisible to that comparison.

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

## Commit the refresh and generated products

When tracked data changed:

1. Run the complete product pipeline:

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
   ```

2. Read and explain every tracked diff, including every generated product diff. An unexplained
   generated change is a failure, not a reason to continue.
3. Run `git diff --check`.
4. Immediately before staging, require `HEAD` to equal the recorded starting `HEAD`. Require
   NUL-delimited status to contain only the downloaded data and audited outputs owned by this
   refresh.
5. Stage only those audited paths, inspect the cached diff, run `git diff --cached --check`, and
   commit locally as `Refresh MAM from Wikisource`. Do not push yet.

The local commit is a functional prerequisite for the next phase: `diff_mpplus` reads committed
`HEAD`, not dirty `MAM-parsed/plus`.

## Regenerate and commit the change logs

Against the new refresh commit, run:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py mpplus --all
```

Read every change-log diff. Changes to reports for named historical releases are unexpected and
must be explained or fixed before continuing. Normally only `unpinned-latest.html`,
`unpinned-latest.json`, and `index.html` change.

Run the read-only freshness guard:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py mpplus --check
```

Require it to report that the artifacts are current. If regeneration produced no tracked
change-log diff, treat that as an unexpected result and stop before pushing; do not create an
empty second commit. Otherwise record the refresh commit's `HEAD`, and immediately before
staging require `HEAD` still to equal that commit and status to contain only the audited
change-log paths. Stage only those paths, inspect the cached diff, run
`git diff --cached --check`, and commit them locally as `Regenerate MAM change logs`.

Run the guard again and require a clean worktree:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py mpplus --check
```

Follow the surrounding checkout's integration procedure. Once the authorized target is ready,
push the two commits together in one normal push; never force-push. Verify that local `HEAD` and
`origin/main` identify the same integration commit. If the push rejects because `main` moved,
incorporate the new `main`, repeat the required generator and guard checks, and read every new
tracked diff. Audit and commit any explained task-owned generated change before retrying the
normal push; an unexplained change blocks integration.

## Separate workflows

- The separately mirrored MAM introduction is not this workflow. Read
  `in/mam-ws-intro/README.md` completely and follow its independent refresh procedure; do not
  treat the bare `py/main_download.py fr-ws-intro` command as the whole procedure.
- Wikisource bot edits are outward-facing edits with their own workflow.
- Google Sheets refreshes are a separate data source and workflow.

This skill's canonical copy is `MAM-basics/dot-claude/skills/mam-wikisource-refresh/`. It is
shared with Codex through `dot-claude/shared-skills.txt` and reaches both live skill homes only
through the deployment procedure in `MAM-basics/dot-claude/README.md`.
