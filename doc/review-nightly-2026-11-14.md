# November 14 continuing nightly broad checks

State: completed 2026-11-14; known HTML findings and scope limits retained
Updates and later status: [review-nightly-2026-11-14-update.md](review-nightly-2026-11-14-update.md).

Portable source `46ed8dc5ac41fe556b131b7911726c215ab64140`; committed read-only sibling input `3cfacbc28ad75e2939613ab796a90d40a40181c5`. Latest hourly receipt `a6a08c8bb482f800725bf6a087403dfc7aaf92a3` already covers through this source, so no hourly window review or focused matrix was repeated. Overall reviewed-through remains `210affe3ac2931473bead0de839be0de08309e3d`; all historical gaps and finished receipts remain.

The owning CPython 3.13.15 environment matches current requirements/constraints, has no system-site packages, and passes `pip check`. Saved runtime activation selected pinned native tools. Checks ran sequentially from an isolated committed source checkout using `/workspace/MAM-basics/.venv/bin/python`:

| Command arguments after the owning interpreter | Exit | Result | Wall seconds |
| --- | --- | --- | --- |
| `-B py/main_0_mega.py` | 0 | 66 completed steps; no cloud skips | 494.977895 |
| `-B py/main_test.py` | 0 | 1449 passed / 5 declared control skips | 363.317166 |
| `-B py/check_html_syntax_and_sanity.py gh-pages/stress-helpers` | 1 | Four historical orphan crops; 111 informational CSS references | 0.646315 |

Mega ran 2026-11-14T07:33:36.767236+00:00 through 2026-11-14T07:41:51.745336+00:00; suite ran 2026-11-14T07:42:04.690870+00:00 through 2026-11-14T07:48:08.008283+00:00. The maintained cloud exclusion depends strictly on `CLAUDE_CODE_REMOTE=true`; that flag is unset here, so all 66 steps actually ran, including the allowed read-only exporter. Public records retain its result and input ID; original diagnostics remain private.

Taamey D's mega steps report **61 PASS / 0 FAIL / 0 SKIP**, unchanged QA reports, and successful verification of nine published release files. The read-only corpus check remains **REFRESH PENDING**; no corpus refresh, font build or baseline acceptance occurred. These steps were not repeated separately. The suite's five declared divergent-edition control skips are `koren_ex_elyon, simtan_dt_taxton, simtiq_dt_taxton, simtiq_ex_elyon, simtiq_ex_taxton`; their control requires an agreeing page and the separate grammaticality test covers these stems. No missing-input skip was introduced. Pytest time: 359.84 seconds.

Eight SVG differences were preserved in full, with binary Git diff, NUL-delimited status/untracked inventories and every before/after byte. Independent XML comparison retains exact elements, child counts, IDs, labels, links, colors, meaningful text and nongeometric attributes; only numeric geometry, valid cubic-edge routing and the known Times alias differ. All eight before/after hashes also match November 13 evidence exactly. After evidence verification these explained platform differences were restored; suite and scoped HTML check leave no tracked or untracked product changes. No generated change was accepted or committed.

The HTML check is **not a pass**: its complete four-orphan report is byte-identical to the latest hourly result at this same source. These are retained historical crops, not a newly introduced finding; no crop was removed or copied into evidence. Broad execution succeeds after explained SVG triage while these HTML findings remain explicitly pending. Passing consistency checks make no new source, manuscript, editorial or visual claim.

Current-source native Windows checks remain unrun. On HP, after checking availability and non-overlap, use the same source and owning environment for `py/main_test.py py/tests/test_worker_budget.py py/tests/test_git_process.py py/tests/test_mb_cmn_provenance.py py/tests/test_worktree_retirement_citations.py -q -ra`, plus the actual Windows memory/CPU API probe. The previous 41-test/resource-API supplement is evidence only at `9ed47c6e8999ecaf56031e9b3f524bee6e01507a`; no current native Windows result is inferred. No HP job was started.

Only the existing isolated receipt branch `review-hourly-20261113-7173440e-basics-receipts` is extended from exact parent `a6a08c8bb482f800725bf6a087403dfc7aaf92a3`. Both source and parent contain only the identical manual-dispatch Pages workflow (blob `18ceb19405424710bda47d9a38c470cc2ed9c385`). No main integration, deployment/dispatch, external acquisition, live bot, frozen-font or schedule work occurs. Local ownership/process checks were clear; cross-machine ownership remains unverified. Publication and task-owned clean-worktree removal are verified separately at closeout.

[Evidence](review-nightly-2026-11-14-evidence.zip): `76093f90cc29c27263f2b68d8f873f1ac6a4d4b9c04a129190bd1b7c708e1c10` (168317 bytes; 31 hashed payloads). Original private-dependent diagnostics are retained privately; the public mega log omits that diagnostic interval. Archive CRC and every manifest hash pass before publication.
