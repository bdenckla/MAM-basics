# MAM mega-pipeline review, Phase 12: vendoring audit integration

Review date: 2026-09-01.

This report reviews only the final `vendoring-audit` `StepRecord` immediately
after `gen-site` in MAM-basics' `py/main_0_mega.py`. The reviewed step writes the
vendoring comparison, provenance, and inventory artifacts. Phase 12 did not fix
production code or generated output and did not begin another review phase.

The governing forest was
`C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01`.
The reviewed branch heads were MAM-basics
`a617dc1d8abbe27b644197a3edb251853cac8efa` and MAM-private
`3aa273676bdad84e7b78f59abf0a06eda94aa6e3`, both on
`review/mega-pipeline-2026-09-01`. The six detached dependency worktrees remained
at the commits in `review-manifest.json`: MAM-parsed `46209cdf`,
codex-index-aleppo `1c12a8e`, MAM-with-doc `999a437`, MAM-simple `cd2bef8`,
MAM-OSIS `2f783d1`, and MAM-for-Sefaria `cf19347`. All eight worktrees were clean
at the pre-write checkpoint. The manifest's MAM-basics commit is the Phase 11
pre-report head; `a617dc1` is the later Phase 11 report commit and is the actual
Phase 12 baseline.

## Phase 12 outcome and cumulative tally

Phase 12 adds **eight genuinely new findings: 0 P1, 6 P2, and 2 P3**. The accepted
tally through Phase 11 was 81 findings: 15 P1, 27 P2, and 39 P3. The cumulative
tally through Phase 12 is therefore **89 findings: 15 P1, 33 P2, and 41 P3**.

The exact `StepRecord` named `vendoring-audit` was selected from `_STEPS`, its
runner was asserted to be the registered `main_vendoring.almost_main` function,
and the runner was called without executing either neighboring step. The live
registration was index 41 of 42, immediately after `gen-site`, and was the final
registered step.

The policy currently derives 97 relationships: 43 for MAM-simple, 8 for
diffable-pointed-hebrew, and 46 for MAM-private. By source package, the same 97
relationships divide into 71 `mb_cmn`, 14 `mb_misc`, 7 `mb_sefaria`, 4 `osis`,
and 1 `mb_diff_mpu` copy. Successful generation writes **four** tracked files:

1. `doc/vendoring-inventory.md`;
2. `out/vendoring_compare_out.txt`;
3. `out/vendoring_provenance_out.json`; and
4. `out/vendoring_provenance_out.txt`.

The exact run wrote 97 comparison rows and an inventory of 12 aggregate rows,
97 files, and zero ignored files. The exact run changed only the inventory and
comparison artifacts. The post-run SHA-256 values were:

1. `doc/vendoring-inventory.md`:
   `1069c0ec473eb7e1b735a62fc610fdb6d7c628706de0dc5ceb2db025e296bde9`;
2. `out/vendoring_compare_out.txt`:
   `92c7af95b4b39e9efca3e459ecc2a8af6ba7a3f7d854938bbb2db82238487703`;
3. `out/vendoring_provenance_out.json`:
   `c046559e5478e3359c7762873f98e7eef1e7cb3110976c14cd87a0c9910d39a0`;
   and
4. `out/vendoring_provenance_out.txt`:
   `944e4c83c868bcfbbe8c9a8240d8dfbce850cae8bfdc5e8f020ba274823ccea3`.

The two reported content differences do not add two copy-drift findings.
MAM-private's stale `al-hatorah/py/mb_cmn/provenance.py` and the previously stale
comparison row were already accepted as finding 5 in
`doc/review-findings-2026-09-01.md`. MAM-simple's stale
`py-examples/osis/osis_runner.py` is replaced by the earlier registered
`mam-simple` step during a complete mega run; that difference is evidence for
finding 7 below. A direct `py/main_vendoring.py --all` rerun after the exact step
returned zero, emitted no stderr, and reproduced all four post-run files
byte-for-byte. Phase 12 restored the two changed generated artifacts to the
reviewed commit before adding this report.

## Eight new Phase 12 findings

1. **[P2] The vendoring audit bypasses the documented per-repository path
   overrides, so an otherwise valid review forest can fail or read the wrong
   checkout.** `mb_cmn/paths.py:131-140` defines sibling lookup precedence as
   `REPO_<NAME>_DIR`, then `REPOS_ROOT/name`, then the checkout's parent. The
   vendoring modules instead capture `paths.repos_root()` in module-level `_REPOS`
   values (`discover.py:14`, `compare.py:46`, and `provenance.py:19`) and construct
   every destination as `_REPOS / repo_name` (`discover.py:87`, `compare.py:100,
   103`, and `provenance.py:113`). The focused vendoring path lint passes because
   the lint uses `paths.sibling_repo()`, but the production audit uses a different
   path model. A controlled production `--compare` run pointed `REPOS_ROOT` at the
   eight-repository forest and supplied the clean primary diffable-pointed-hebrew
   clone through `REPO_DIFFABLE_POINTED_HEBREW_DIR`. The audit ignored the
   per-repository override and failed with `ValueError: Missing destination repo:
   diffable-pointed-hebrew` before writing an output.

2. **[P2] A failed Git history query becomes the valid-looking value
   `no-commits`, and the audit succeeds without the dependency failure.**
   `compare._git_log_date()` runs `git log` at `compare.py:75-84`, but lines 85-88
   inspect only stdout and never test `returncode` or stderr. A controlled Git
   result with return code 128, empty stdout, and a unique stderr sentinel produced
   `no-commits`. The comparison writer would serialize that value as the copy's
   last-sync state and continue. An empty successful history and a failed Git
   command are therefore indistinguishable in the tracked report.

3. **[P2] Untracked Python files are production audit inputs even though the
   provenance module says tracked state is the question.** Source discovery reads
   every on-disk `*.py` through `iterdir()` at `discover.py:60-72`; destination
   discovery reads every matching on-disk file through `iterdir()` at
   `discover.py:83-114`; and copy-script discovery searches the working tree with
   `rglob()` at `provenance.py:99-109`. The explanatory comment at
   `provenance.py:45-57` expressly says that what the repository tracks is the
   question, but the exclusion list can name only anticipated ignored directory
   names. In a policy-shaped directory under `.novc`, an untracked source
   `probe.py` and untracked destination `probe.py` became a real relationship,
   while an untracked `scratch/copy_probe.py` became a reported copy script. A
   developer's unrelated work in a non-excluded directory can therefore change
   all three generated report families.

4. **[P2] Policy paths are called relative but are not checked for containment, so
   a policy typo can move an audit input outside the pinned repository.**
   `_expect_rel_path()` at `repo_policy.py:93-100` rejects backslashes and leading
   or trailing slashes, but accepts parent traversal and Windows drive-qualified
   paths. The controlled validator accepted `../escape`,
   `nested/../../escape`, and `C:/absolute/escape`. Those values flow into source
   package directories, destination scan roots, explicit destination paths, and
   provenance scan roots. On Windows, joining a drive-qualified path discards the
   intended base; joining either parent-traversal value can escape the intended
   checkout after path resolution. The policy is tracked and trusted rather than
   hostile, but the missing containment check allows a spelling error to defeat
   the pinned-forest boundary silently.

5. **[P2] The four-output regeneration is neither file-atomic nor set-atomic, so a
   failed audit can leave a mixed and even truncated tracked report set.**
   `main_vendoring.almost_main()` calls comparison, provenance, and inventory in
   sequence at `main_vendoring.py:37-45`. The comparison writer opens its tracked
   file directly in write mode (`compare.py:117-129`); the provenance writer then
   opens the text file directly and the JSON file directly
   (`provenance.py:139-170`); the inventory writer finally calls `write_text()` on
   its tracked file (`gen_inventory.py:354`). There is no temporary-file replace,
   transaction, or rollback. A controlled failure after the provenance JSON
   writer emitted `{"repos": [` left the JSON file truncated and left the text
   report fully replaced. In a real run, the comparison output would already have
   been replaced and the inventory would still be old. The exception propagates,
   but the failed step does not preserve the pre-run output set.

6. **[P2] A vendored copy whose source module disappears drops out of the audit
   instead of being reported as `MISSING-SRC`.** `_source_file_names()` collects
   only source filenames that currently exist (`discover.py:60-72`), and
   `_scanned_dest_paths()` discards every destination whose basename is not in
   that current source set (`discover.py:83-107`). An override cannot preserve the
   relationship: `discover_relationships()` rejects an override whose source
   basename is absent (`discover.py:174-178`). Although `MISSING-SRC` appears in
   `IDENTITY_VALUES` at `discover.py:22`, `_identity()` returns `DIFFERS` for a
   missing source at `compare.py:62-65`, and production discovery prevents that
   row from reaching `_identity()`. A controlled policy-shaped probe produced one
   row while source and destination existed; after removing only the source, the
   destination still existed and the relationship list was empty. Regenerating a
   previously tracked inventory can expose a removed row once, but a freshly
   accepted baseline no longer names or audits the stale destination copy.

7. **[P3] The final-step comment incorrectly says no earlier mega step feeds the
   audit.** `main_0_mega.py:403-409` begins, “Last, and not because anything above
   it feeds it.” The earlier `mam-simple` registration calls
   `main_mam_simple.almost_main` at `main_0_mega.py:200-203`;
   `main_mam_simple.almost_main()` calls `copy_support_files()` at
   `main_mam_simple.py:158`; and the support-file list includes
   `osis/osis_runner.py` at `mam_simple_copy_py_files.py:90`. The controlled copy
   run wrote 43 Python files and made the copied `osis_runner.py` byte-identical
   to its MAM-basics source, SHA-256 `5e2c1355bf86aebffa34e7713f6873e17e7176ed06b50900bd1cf5d1f0a98d55`.
   The exact isolated audit found that pinned MAM-simple copy stale because Phase
   12 did not run the earlier `mam-simple` step. The final placement is correct:
   the audit belongs after the writer that refreshes a destination being audited.
   The comment's independence rationale is wrong.

8. **[P3] The registration and module prose misstate both the audit scope and its
   output count.** The live `StepRecord` note at `main_0_mega.py:410-413` says the
   step “scans every sibling repo on disk,” but the policy names exactly three
   repositories and the implementation visits those policy repositories. The
   adjacent comment and the module docstring say the step writes three artifacts
   (`main_0_mega.py:408` and `main_vendoring.py:21-25`), but Git and the live
   writers identify the four tracked files listed above. The glob-shaped note
   mentions both provenance formats indirectly, while the prose's count remains
   wrong. The audit scope is policy-defined, not a census of every on-disk sibling,
   and the generated-output test has four members, not three.

## Registration, dependency, and deterministic-output results

The exact runner confirmed the required registration boundary: `vendoring-audit`
is the last of 42 steps, immediately after `gen-site`, and calls
`main_vendoring.almost_main`. The callable writes comparison first, provenance
second, and inventory last. Inventory deliberately reads the two reports just
written by passing `refresh_live_inputs=False`.

The current order after `mam-simple` is required for the generated MAM-simple
copy identified in finding 7. No dependency on `gen-site` was found; adjacency to
`gen-site` follows only because both steps close the current mega pipeline. The
audit also reads MAM-private and diffable-pointed-hebrew. Production regeneration
used the pinned MAM-simple and MAM-private worktrees plus the separately verified
clean diffable-pointed-hebrew primary clone at `dd1fdb9` because that repository
is outside the deliberately eight-repository review forest. No other primary
clone supplied a production audit input.

There is no internal concurrency. Relationship, repository, path, and report
ordering is explicit or sorted, and a direct successful rerun reproduced all four
post-run files byte-for-byte. Finding 5 concerns the sequential writer's failure
boundary, not a successful-run race. No nondeterministic output was found.

## Inventory, stale-copy, and diagnostics results

The 97 current relationships agree between discovery, comparison, and inventory,
and the package and destination counts reconcile to 97. Current regeneration
correctly surfaced both known on-disk differences and changed no provenance
artifact. The two existing differences are explained above; Phase 12 found no
third current copy difference.

Finding 6 is the stale-copy cleanup failure: a destination left behind after its
source is retired falls outside discovery. Finding 3 is the opposite set-boundary
failure: a new untracked source and matching destination enter discovery. Together
the two findings show that the production relationship set follows the mutable
working directory rather than a tracked declaration or tracked-set equality.

Missing configured repositories and missing configured scan roots raise clear
`ValueError` exceptions. Identity differences remain report rows rather than
process failures, which is appropriate for an audit whose tracked diff is the
test. The two diagnostic failures are narrower: finding 1 rejects a documented
path configuration, and finding 2 converts a failed Git dependency into ordinary
report data. The mega runner propagates exceptions raised by the vendoring code.

## Reproduction commands and verification record

From the MAM-basics review worktree, the exact registered step was exercised by
the ignored Phase 12 probe with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/phase12_probe.py registered exact_step
```

The direct successful rerun was exercised with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/phase12_probe.py direct direct_after_exact
```

The focused policy-path lint was exercised with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/phase12_probe.py tests py/tests/test_vendoring_policy_paths.py -q
```

The focused lint reported **18 passed in 0.10 seconds**. The complete MAM-basics
suite was exercised with the review-forest dependencies pinned where the forest
contains them and verified-clean primary clones supplied only for the ten
dependencies absent from the deliberately eight-repository forest:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/phase12_probe.py tests
```

The complete suite reported **971 passed and 5 skipped in 93.40 seconds**. The
ignored probe captured output hashes, relationship counts, registration identity,
the deterministic rerun, the scheduling dependency, and all controlled failure
and set-boundary results as JSON under MAM-basics `.novc`.

The final cross-phase checkpoint retained Phase 10's 87 expected census files and
their aggregate SHA-256
`e267f49ad6a1f944ecf1ce884f729179d58f88daea9b7899b5d9f29ef96f2435`.
The only tracked Phase 12 change is this report. No production fix, generated
artifact, fetch, update, rebase, merge, worktree removal, or later-phase work is
included.
