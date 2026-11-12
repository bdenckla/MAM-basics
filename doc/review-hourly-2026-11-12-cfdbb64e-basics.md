# MAM-basics bounded hourly screen

State: completed 2026-11-12; bounded screen and focused checks only

Frozen endpoint `9f8901a92f8f040060841b1e5ba19524b97bbba3` -> `cfdbb64ef8fc24e777d4d296efb7fe4ac966346d`: one commit / two public paths. No consequential introduced defect established; no product repair. Review and execution use public material only.

The public policy adds three declared record-folder exclusions. The parser requires the record section/list, exact entry keys, string folder entries and trailing slashes, and merges those folders with existing file exclusions. The regex escapes metacharacters, retains file end anchors, and treats a trailing-slash entry as a whole subtree. All other configuration apart from the explanatory comment and new section is unchanged; all five unaffected function ASTs match the base. The unchanged maintained caller still adds exclusions only for repositories other than the source repository.

Changed-source Black passes (0.151923 s); all four existing prose-convention tests pass through `py/main_test.py` (16.145645 s wall / 15.93 s pytest). Independent checks pass (0.431051 s): 15 malformed policy cases rejected; valid empty and repeated-repository sections handled; 12 generic file/folder/package/metacharacter regex cases and nine declared-policy cases pass. The maintained `run_black_across_repos` is exercised against two disposable public Git fixtures with actual owning-environment Black. Four excluded files retain exact bad-format bytes, four nearby live files are formatted, and both source-repository originals are formatted without exclusions. Only the unchanged Windows executable-discovery helper is adapted to the owning Linux interpreter; this is not full CLI or native Windows evidence. No actual repository sweep or private inventory was run.

The regex is a leading-slash path-component search, not a start-of-string anchor; a nested occurrence of the same folder suffix also matches. The probes record this behavior explicitly and do not claim root-only matching. No consequential incorrect exclusion is established by this public-only bounded screen. There were no failed command/check attempts and no tracked or untracked source differences. The real maintenance CLI and roster were inspected without dispatching the mutating sweep. No product generation, broad mega/suite, private input inspection, source refresh or visual/font check was warranted or run.

Lineage continues from `6187492ddea354efca7b80909e7f62a27f62447e`, keeping every historical row, pending window and finished receipt. Overall reviewed remains `210affe3ac2931473bead0de839be0de08309e3d`; broad-tested remains `354cc0b7077cb46ba5d7cfc8dd9b453ff68c7bf0`. Prior browser/source/editorial/HP and frozen-font limits remain separate. Local process/slot ownership was clear; cross-machine ownership remains unverified. The maintenance owner retains real sweep/decision work, and the next broad owner retains broad coverage.

Source and receipt parent share the same sole manual-dispatch Pages workflow, verified before the fresh isolated receipt push. No workflow dispatch, main/shared integration or deployment occurs. Exact remote commit/scope/evidence verification and task-worktree/slot cleanup are recorded at closeout; home and unrelated work are preserved.


Commands ran sequentially in the exact committed owning checkout, with the home interpreter; baseline comparisons are explicitly identified below. Full command arrays, UTC timestamps, durations, failures, output diffs, checker and payload manifest are in the evidence ZIP.

| Stage | Command | Exit | Seconds |
| --- | --- | --- | --- |
| black | `-m black --check py/repo_util/maintenance_policy.py` | 0 | 0.151923 |
| prose-tests | `py/main_test.py py/tests/test_prose_conventions.py` | 0 | 16.145645 |
| independent | `/workspace/scratch/check_basics_cfdbb64e.py` | 0 | 0.431051 |

[Evidence](review-hourly-2026-11-12-cfdbb64e-basics-evidence.zip). Receipt parent `6187492ddea354efca7b80909e7f62a27f62447e`; source `cfdbb64ef8fc24e777d4d296efb7fe4ac966346d`. This commit changes only the receipt, evidence and maintained status. No main/shared integration or deployment.
