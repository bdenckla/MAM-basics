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

## The scan archive's location has one definition, overridden by `BOOK_SCANS_ROOT`

Recorded by Claude on 2026-09-28. This entry disposes of item 7 in section 8,
“`py/scan_pages/editions.py`'s `scans_root()` is hard-coded to
`~/OneDrive/Documents/ScansOfBooks`, and ignores the `WLC_SCANS_DIR` override that
`py/accgram/scan_page.py` honours.” The source analysis is a finished dated report and remains
unchanged.

Fixed on 2026-09-28. `book_scans_root()` in `py/mb_cmn/paths.py` is now the one definition of the
scan archive's location. Both readers use it: `SCANS` in `py/accgram/scan_page.py`, which
`py/accgram/transcription_editor.py` imports, and `edition_dir()` in `py/scan_pages/editions.py`,
whose `scans_root()` was removed. So `py/main_scan_pages.py survey` now honours the override too.
Ben chose the single definition and the override's new name, `BOOK_SCANS_ROOT`, the same day. The
old name, `WLC_SCANS_DIR`, carried a prefix left over from wlc-utils; it is no longer read, even
as a fallback. With the variable unset, both readers resolve `~/OneDrive/Documents/ScansOfBooks`,
as before.

The change reaches no product. No mega step imports either reader, and the one hand-run generator
that reads the archive, `py/main_scan_pages.py survey`, resolves the same edition folders as
before when the variable is unset.
