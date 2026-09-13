# Updates to the 2026-09-10 mega-coverage analysis

State: open, first entry 2026-09-13.

## User-configuration synchronization adds one utility action and one maintenance step

Recorded by Codex on 2026-09-13. This entry corrects the table row
“`py/main_repo_util.py`, all six actions” and both passages stating that MAM-basics maintenance
runs the suite at step 5 and the mega at step 6. The source analysis is a finished dated report
and remains unchanged.

`py/main_repo_util.py` now has seven mutually exclusive actions. Six serve the cross-repository
maintenance sweep; `--sync-user-config` checks or deploys MAM-basics' tracked user-level agent
configuration and does not traverse the workspace roster. The program remains outside the mega
for the maintenance reason the source analysis records.

`py/main_repo_maintenance.py` now checks user-level configuration drift at step 3. The check
fetches `origin` and compares every declared live destination with the freshly updated
`origin/main` without changing live configuration. Consequently the maintenance suite is step 6
and the mega is step 7. The suite's `test_mega_coverage.py` remains the mechanical coverage check
that runs immediately before the mega.

These changes reach neither a MAM generator nor a product. The maintenance check performs no live
configuration write; its fetch updates local remote-tracking Git metadata but performs no
outward-facing write.
