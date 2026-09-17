# Dependent refresh after MAM Wikisource data changes

Use this procedure only after `SKILL.md`'s download step leaves audited tracked changes in the
verified MAM-basics development checkout. It coordinates existing repository entry points; it
does not authorize a new orchestrator or a push that the surrounding instructions do not allow.

## Preconditions

- Read each repository's instruction file before writing in that repository. Load the applicable
  worktree procedure when any development checkout is a linked worktree.
- Record the absolute top level, branch, `HEAD`, remote relationship, and NUL-delimited status of
  every checkout used. Recheck the recorded `HEAD` and task-owned status before each commit.
- Use the interpreter belonging to each repository's primary clone. Run each command from the
  repository root whose files the command changes.
- Require the primary checkouts at `C:/Users/BenDe/GitRepos/MAM-private` and
  `C:/Users/BenDe/GitRepos/phonetic-hbo` to be on `main`, current enough for the refresh, clean,
  and unambiguously assigned to this workflow before either checkout is written. A clean status
  alone does not establish ownership. A known active task,
  an unexplained worktree association, or the absence of a clear handoff is ambiguous ownership.
- Do not push any repository until all three repositories have completed their local work and
  passed their required gates.

## Refresh sequence

1. **Commit the MAM-basics refresh locally.** In the verified MAM-basics development checkout,
   run the complete product pipeline:

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
   ```

   Read and explain every tracked diff, including generated products. Run `git diff --check`,
   verify that `HEAD` still equals the recorded starting commit, stage only the audited refresh
   paths, inspect the cached diff, run `git diff --cached --check`, and commit locally as
   `Refresh MAM from Wikisource`. Do not push. This commit is required because later change-log
   generation cannot compare against dirty `MAM-parsed/plus` data.

2. **Clear both downstream checkouts before writing either one.** Perform the MAM-private and
   phonetic-hbo preflight in full. If either checkout is dirty, stale in a way that would make
   the inputs ambiguous, or owned by another task, stop before running the MAM-private profile.
   Require a handoff or cleanup; do not borrow, stash, discard, or work around another task's
   state.

3. **Regenerate MAM-private.** From `C:/Users/BenDe/GitRepos/MAM-private`, run its refresh
   profile with its repository interpreter:

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-private/.venv/Scripts/python.exe py/main_0_mega.py --profile mam-refresh
   ```

   Read every MAM-private diff, run the repository's required checks, and commit every explained
   tracked change on `main`. Do not push yet. An unexplained diff or a
   stale MAM-basics input stops the workflow.

4. **Audit phonetic-hbo Pages output.** Inspect the resulting changes in
   `C:/Users/BenDe/GitRepos/phonetic-hbo`, run that repository's required checks, and commit the
   explained Pages changes on `main`. If regeneration legitimately
   produced no phonetic-hbo diff, record the no-op and continue without an empty commit. An
   unexplained diff or evidence that the output did not use the just-committed MAM-private state
   stops the workflow.

5. **Return to MAM-basics and close the dependency loop.** Set the supported sibling-root
   override when the MAM-basics development checkout is a managed worktree:

   ```powershell
   $env:REPOS_ROOT = "C:/Users/BenDe/GitRepos"
   ```

   Rerun the post-stress survey:

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_accgram.py survey-post-stress-meteg
   ```

   Generate the authored pages from that survey:

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_authored.py gen-site --trust-surveys
   ```

   Then run the required complete product pipeline again:

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
   ```

   Audit every diff. Expected survey or page movement is dependent regeneration, not a census
   failure. Commit explained dependent-output changes if any exist; do not create an empty
   commit. A stale MAM-private or phonetic-hbo input, a failed categorical survey claim, or an
   unexplained generated change stops the workflow.

6. **Generate MAM change logs from the final committed MAM-basics state.** The prior MAM-basics
   work must be committed before this command:

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py mpplus --all
   ```

   Read every change-log diff. Changes to reports for named historical releases are unexpected.
   Run the freshness guard:

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py mpplus --check
   ```

   Require current artifacts. If the refresh changed book data but produced no change-log diff,
   treat that as unexpected and stop before pushing; do not create an empty change-log commit.
   Otherwise stage only the audited change-log paths, inspect the cached diff, run
   `git diff --cached --check`, and commit them separately as `Regenerate MAM change logs`. Run
   the freshness guard again.

7. **Run final gates, integrate, and push in dependency order.** If MAM-basics work ran in a
   linked worktree, merge current `main` into the worktree branch according to the repository's
   worktree procedure, rerun every required final gate there, and fast-forward the clean primary
   clone only after the gates pass. MAM-basics requires:

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py
   ```

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
   ```

   Run `git diff --check` through the checkout's required exact-path Git invocation. Require
   clean, explained results in MAM-private and phonetic-hbo under their own instruction files as
   well. Only after all gates pass, push normal fast-forwards in this order:
   MAM-private, phonetic-hbo, MAM-basics. Never force-push. If a push rejects or a remote moves,
   incorporate the new state, rerun the affected generators and gates, and audit every new diff
   before retrying.

8. **Verify the final state.** Fetch the three remotes and require each primary checkout to be
   clean, on `main`, and at the same commit as `origin/main`. A local commit
   left ahead, a remote commit left ahead, or any tracked residue means the workflow is not
   complete.

## Required scenario behavior

1. When no Wikisource data changed, `SKILL.md` stops after the download without downstream
   writes.
2. When relevant data changed and both downstream repositories are available, the workflow
   completes the entire dependency loop before any push.
3. When a downstream checkout is dirty or actively owned, the workflow stops before the first
   downstream write and requires a handoff.
4. When a downstream generator legitimately produces no diff, the workflow continues without an
   empty commit.
