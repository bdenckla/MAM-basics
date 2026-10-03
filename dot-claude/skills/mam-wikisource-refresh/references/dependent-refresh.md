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
   If the mega stops at `yeivin-itm-survey-meteg-claims`, follow "Gates that a text change can
   trip", item 1, before committing. Use `Refresh MAM from Wikisource`, or the saving bot run's own record as `SKILL.md` specifies.
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
   unexplained output changes stop the workflow; "Gates that a text change can trip" says how
   the Yeivin claim pins and the legacy display projection are resolved.

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

## Gates that a text change can trip

Two checks compare current output with records that no generator rewrites. A refresh that
changes MAM's text can trip both. Approval of the refresh does not approve either record, and no
agent approves the Yeivin pins.

1. **The Yeivin claim pins.** `py/yeivin_itm/claim_schema.py` pins the 20 fractions that Ben
   approved and a SHA-256 of the claim population, which is every record in the ordinary
   population of `out/accgram/meteg-before-stress.json` whose pattern is FR1, FR2, FR3, AFR1,
   AFR4 or XAFR1. When a pinned fraction or a claim-population record changes, the mega stops
   at `yeivin-itm-survey-meteg-claims`, and `py/main_yeivin_itm.py survey-meteg-claims` and
   `check` raise without writing.
   1. Leave `py/yeivin_itm/claim_schema.py`, `Yeivin-ITM/meteg-claims.json` and
      `gh-pages/yeivin-itm/` unchanged.
   2. Run `./.venv/Scripts/python.exe py/main_yeivin_itm.py review-claims`, which writes
      nothing, and give Ben its report: each changed fraction with its approved and new
      values, and each page line whose text would change, before and after. Add the
      claim-population records that `git diff -- out/accgram/meteg-before-stress.json` shows
      added, removed or changed.
   3. Stop until Ben approves the new pins in his own message. Without that approval the
      refresh ends before any push.
   4. With his approval, change only the pins he approved and run
      `./.venv/Scripts/python.exe py/main_0_mega.py --resume-from yeivin-itm-survey-meteg-claims`.
      Audit the regenerated claim file and pages. Commit step 1's refresh paths first, then the
      pins, the claim file and the changed pages in a commit of their own whose message quotes
      Ben's approval.
2. **The legacy display projection.** `test_complete_release_and_unified_projection` compares a
   rendered Phonetic MAM chapter with its frozen hashes in
   `in/phonetic_mam_legacy_projection_sha256.json` only while the chapter's MAM-parsed input
   matches its fingerprint in `in/phonetic_mam_legacy_projection_inputs.json`.
   `./.venv/Scripts/python.exe py/main_phonetic_mam.py check` lists the chapters that have left
   the comparison. Require each listed chapter to be one whose data a committed refresh changed,
   and audit each newly listed chapter's rendered diff in both pronunciations. A mismatch in a
   chapter whose input is unchanged is a regression: stop and resolve it. Never regenerate
   either file; no source exists for the old pages' display of new text.

## Required scenario behavior

1. Unchanged Wikisource data stops after the download, without downstream writes.
2. Changed chapter data requires the complete two-repository loop before any push.
3. A dirty or actively owned private checkout stops before the first public mega reads it.
4. A legitimate generator no-op continues without an empty commit.
5. A one-repository cloud checkout still lacks the private adapter and regeneration inputs;
   cloud-skipped mega steps do not establish completion of a changed-data refresh.
6. A changed claim-population record or Yeivin fraction stops the refresh until Ben approves
   new pins.
