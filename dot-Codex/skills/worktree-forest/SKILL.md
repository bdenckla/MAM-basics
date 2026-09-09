---
name: worktree-forest
description: Create, verify, reuse, hand off, or retire a pinned multi-repository Git worktree forest for cross-repository reviews and reproducible pipeline runs. Use when a task mentions a review forest, worktree forest, ReviewForests path, review-manifest.json, or reusing the same pinned repository set across sessions. Do not use for an ordinary single-repository Codex worktree.
---

# Worktree Forests

A worktree forest is Ben's local convention for a coordinated set of Git
worktrees, one per participating repository, under a single root. It is not a
Codex or Git feature with its own metadata. The forest's purpose is to give a
multi-repository review or regeneration one pinned, isolated input set that can
be reused by later sessions.

Treat a forest as an execution environment, not as a loose collection of nearby
checkouts. A command belongs in the forest only when every repository input it
can reach resolves to the intended forest worktree or to an exception recorded
in the manifest.

## Read the forest before using it

1. Read `review-manifest.json` at the forest root before running a repository
   command. If no manifest exists, reconstruct and write one before treating the
   directory as reusable.
2. Record the forest root, purpose, scratch policy, interpreter paths, repository
   membership, immutable baseline commits, checkout modes, and each repository's
   role. Record every deliberate primary-clone fallback.
3. Distinguish an immutable input worktree from a report branch that may advance.
   If a report branch advances, preserve the original baseline and record the new
   expected head; do not silently reinterpret the baseline commit as the current
   head.
4. Verify every worktree's `HEAD`, branch or detached state, cleanliness, and
   configured remote against the manifest. Do not fetch, pull, rebase, reset, or
   repair a mismatch merely to make the check pass.
5. Derive membership from the full runtime dependency graph, not only imports or
   test collection. Runtime path lookups can reveal repositories absent from a
   static list; a missing member is a forest-design finding.

## Handle Windows SID ownership checks locally

Git can reject a valid forest worktree as having dubious ownership when Codex
created or opened the worktree under a different Windows SID. This can happen on
the same machine even though the human-facing Windows account is unchanged.

Do not respond by adding forest paths to the machine's global Git configuration.
Global `safe.directory` entries persist after the forest is retired and silently
widen trust for every later Git process.

Pass the exact worktree path as command-local Git configuration on every Git
invocation instead. Use forward slashes in the `safe.directory` value:

```powershell
git -c "safe.directory=C:/absolute/forest/repo" -C "C:/absolute/forest/repo" status --short --branch
```

For a Python probe or production command that starts Git internally, give only
that child process the equivalent `GIT_CONFIG_COUNT`, `GIT_CONFIG_KEY_<n>`, and
`GIT_CONFIG_VALUE_<n>` environment entries. Prefer one exact `safe.directory`
entry per repository the child can inspect. A process-local wildcard is a last
resort for a controlled probe that must inspect a manifest-defined set; never
write the wildcard to global or repository configuration.

The ownership rejection is not evidence that the worktree is corrupt, dirty, or
at the wrong commit. Re-run the same read-only check with command-local trust,
then evaluate the Git result normally.

## Create a forest

1. Choose a root outside every participating repository. On this Windows machine,
   the normal location is
   `C:/Users/BenDe/Documents/Codex/ReviewForests/<forest-name>` unless Ben names
   another location.
2. Verify each primary clone is clean and record its starting `HEAD` before
   creating a worktree. Existing user changes remain outside the forest and are
   not copied, staged, or normalized.
3. Create a branch worktree only for a repository expected to receive review
   records or other authorized commits. Use a detached worktree for an immutable
   dependency. A forest branch is an isolation mechanism, not a pull-request
   workflow.
4. Pin each worktree to an exact commit and write the manifest immediately. The
   forest is not reusable until the manifest and a complete clean/head report
   exist.
5. Put disposable probes only in a gitignored scratch directory inside the
   relevant forest worktree. Do not use or modify a primary clone's scratch
   directory.

The manifest schema may follow the task, but it must name at least:

- the forest root, purpose, creation date, and scratch policy;
- each repository's name, primary clone, forest worktree, baseline commit,
  checkout mode, role, and head-advancement policy;
- every interpreter or tool intentionally borrowed from a primary clone; and
- every repository input intentionally left outside the forest, with its verified
  commit and reason.

## Run work inside a forest

- Use absolute forest paths for repository inputs and outputs. Set `REPOS_ROOT`
  and supported `REPO_<NAME>_DIR` overrides explicitly when the program resolves
  sibling repositories.
- Use a primary clone's venv by absolute path, because venvs are gitignored and
  must not be copied, linked, or junctioned into worktrees. The script path and
  current directory still point into the forest worktree.
- Treat a program that bypasses a supported per-repository override as a finding;
  do not hide the bypass by broadening the forest or changing a primary clone.
- Do not allow an unrecorded primary clone to fill a missing forest member. If a
  primary clone is an intentional fallback, verify that clone is clean and record
  the exact commit before the run.
- Before staging, confirm that the repository `HEAD` still equals the recorded
  pre-work head and that status contains only paths owned by the current task.
- Keep generated-output probes reversible. Record hashes and diffs, then restore
  only the exact outputs the probe changed when the task is review-only.

## Reuse or hand off a forest

A later session does not inherit the earlier session's verification. The handoff
must name the absolute forest root and manifest, the exact phase or scope, current
heads, permitted branch advancement, known dirty state, interpreter paths, and
any allowed primary-clone exceptions. The new session repeats the manifest,
ownership, head, and cleanliness checks before work.

Do not describe a forest merely as “the same forest as before.” Forest identity
comes from its absolute root plus its manifest and verified heads.

## Finish or retire a forest

1. Restore review-only probe changes and commit only the authorized report or
   production paths.
2. Push every authorized forest-branch commit according to the repository's Git
   instructions. Do not merge a review branch when the task says to leave the
   branch unmerged.
3. Verify every member's final `HEAD`, branch state, cleanliness, and outgoing
   commits. State recorded exceptions by repository name.
4. Preserve the manifest and review reports for as long as another session may
   reuse the forest.
5. Remove worktrees or branches only when Ben asks or the governing workflow
   explicitly includes retirement. Verify exact paths before removal. A live
   Windows process whose current directory is inside a worktree can prevent
   removal; wait for that process to end rather than forcing deletion.
