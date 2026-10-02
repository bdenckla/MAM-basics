# Dependent refresh after MAM Wikisource data changes

Use this procedure only after `SKILL.md`'s download step, or the post-run download of a live
Wikisource bot run, leaves audited tracked changes in the verified MAM-basics development
checkout. Coordinate the existing entry points under the surrounding authorization.

## Preconditions

- Read the instructions of MAM-basics and MAM-private and the applicable worktree procedure.
- Record every selected checkout's absolute path, branch, HEAD, remote relationship and
  NUL-delimited status. Recheck HEAD and task-owned status before each commit.
- Use each full clone's own environment, or the development worktree's home-clone environment.
  Run each command from the root whose files it changes.
- Assign a clean, current MAM-private development checkout before the first public mega,
  which reads its adapter, and recheck that assignment before every private write.
  A known active writer or ambiguous ownership requires a handoff. A linked private worktree
  is supported: all retained private generators write within MAM-private.
- Select the public input checkout through `REPO_MAM_BASICS_DIR` for private commands.
  The public exporter selects the corresponding private checkout through
  `REPO_MAM_PRIVATE_DIR`. Required sources and owning interpreters must exist.
- Do not push either repository until the local dependency loop and its gates pass.
  phonetic-hbo is a frozen redirect and historical issue host; this refresh never reads,
  preflights, writes or restores its clone.

## Refresh sequence

1. **Commit the public refresh locally.** In the MAM-basics development checkout, run:

   ```powershell
   ./.venv/Scripts/python.exe py/main_0_mega.py
   ```

   The public mega exports `Phonetic-MAM/` through the retained read-only private source
   adapter, then renders and analyzes the tracked public release. Audit every generated diff,
   run whitespace checks, verify the recorded HEAD and commit only the audited refresh paths.
   Use `Refresh MAM from Wikisource`, or the saving bot run's own record as `SKILL.md` specifies.
   This local commit precedes change-log generation, which compares committed data.

2. **Recheck private ownership and inputs before writing.** Require the selected private
   checkout clean and assigned to this workflow. `REPO_MAM_BASICS_DIR` must name the just
   committed public checkout. Stop on stale input or an unrelated writer; do not borrow,
   stash or discard another task's state.

3. **Regenerate retained private products.** From the MAM-private development root, run:

   ```powershell
   ./.venv/Scripts/python.exe py/main_0_mega.py --profile mam-refresh
   ```

   Use the private home-clone interpreter by absolute path in a worktree. This updates private
   source diagnostics, comparisons, research and census products. Audit every diff and run
   the repository's required checks. Commit explained changes locally; a legitimate no-op
   needs no empty commit. The profile has no publication ownership in phonetic-hbo.

4. **Close the public dependency loop.** From the MAM-basics development root, run its mega
   again with `REPO_MAM_PRIVATE_DIR` selecting the verified private development checkout:

   ```powershell
   ./.venv/Scripts/python.exe py/main_0_mega.py
   ```

   The exporter is the routine public pipeline's only private dependency. Phonetic rendering,
   both meteg surveys, the Breuer survey and the Yeivin claims/rendering consume public data.
   Audit every diff and commit explained dependent changes. Failed gates, stale inputs and
   unexplained output changes stop the workflow.

5. **Generate change logs from final committed public data.** Run:

   ```powershell
   ./.venv/Scripts/python.exe py/main_diff.py mpplus --all
   ```

   Audit every change-log diff; named historical-release reports must remain unchanged.
   Then run:

   ```powershell
   ./.venv/Scripts/python.exe py/main_diff.py mpplus --check
   ```

   If book data changed but no change-log diff results, stop and resolve the discrepancy.
   Otherwise commit audited logs separately as `Regenerate MAM change logs` and repeat the
   freshness guard. Do not create an empty commit.

6. **Run final gates, integrate and push.** Follow both repositories' current integration
   rules. Merge moved origin/main in the development worktree, repeat affected checks and
   fast-forward its clean home clone only after gates pass. Run the full suite after the last
   change likely to break it; later documentation does not expire that result. Generator/data
   branches still owe the final mega after current main is incorporated. Require clean,
   explained results in both repositories. Push normal fast-forwards in dependency order:
   MAM-private, then MAM-basics. If a push rejects, incorporate the moved origin in development,
   repeat affected generators and checks, and audit new diffs before retrying.

7. **Verify completion.** Fetch both origins. Require each home clone clean on main and equal
   to origin/main. Any ahead/behind commit or tracked residue means the refresh is incomplete.

## Required scenario behavior

1. Unchanged Wikisource data stops after the download, without downstream writes.
2. Changed chapter data requires the complete two-repository loop before any push.
3. A dirty or actively owned private checkout stops before the first public mega reads it.
4. A legitimate generator no-op continues without an empty commit.
5. A one-repository cloud checkout still lacks the private adapter and regeneration inputs;
   cloud-skipped mega steps do not establish completion of a changed-data refresh.
