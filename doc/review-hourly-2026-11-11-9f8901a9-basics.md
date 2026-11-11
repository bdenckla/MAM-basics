# MAM-basics bounded hourly screen

State: completed 2026-11-11; bounded screen and focused checks only

Frozen endpoint `d957048a20f671fbadea37325c91dd9c9bfe4ee9` -> `9f8901a92f8f040060841b1e5ba19524b97bbba3`: four commits / 28 paths. No consequential introduced defect established; no product repair.

The FOI index conversion preserves all 26 destinations, order, labels, descriptions and inline markup after serializer whitespace folding. Hebrew codepoints are unchanged. The complete maintained FOI generator reproduces committed outputs exactly; all 53 other FOI outputs have identical endpoint blobs. The source change uses the existing anchor/description producers and coverage guard, with two-column table styling and viewport metadata.

Twenty focused maintained tests pass: shared styles (2), receipt links (1), source hygiene (9), prose conventions (4), and tracked Phonetic MAM release (4). Changed-source Black passes for all three Python paths. FOI HTML validation reports no output issues, with 1,160 informational undefined CSS-class references retained; this is not an assertion that every CSS reference has been resolved. Every executed stage leaves zero tracked or untracked product differences. There were no failed execution stages or diagnostic retries in this window.

The other two Python deltas are docstring/comment-only by AST comparison. Three Phonetic MAM approval-string changes add archival URL prefixes, preserving all other configuration. All 16 retired documents match their base blobs at full archival commit `462984bb567a6498fd4f2d7ef00e3186fcd00f02`; 33 distinct immutable file targets in changed surviving prose/configuration resolve locally. Recorded retirement approval and external issue-body audit remain attributed; no external audit was repeated. The appended maintenance report was read, but its historical C1/S1/S2 and latent findings belong to the existing Claude maintenance session and Ben. This screen neither reopens those decisions nor claims to have independently rerun that audit.

Overall reviewed-through remains `210affe3ac2931473bead0de839be0de08309e3d`; broad-tested remains `354cc0b7077cb46ba5d7cfc8dd9b453ff68c7bf0`. All inherited rows, pending windows and immutable receipts are carried forward. No broad suite/mega, live-source/editorial/manuscript check or browser/font verification ran. The earlier responsive-browser failures and gap remain open; no failed browser harness was repeated. Local slot/process ownership was clear at admission; cross-machine ownership remains unverified. Existing maintenance owners resolve their findings; the next scheduled broad owner handles broad coverage. A corrected supported browser setup is the trigger for future visual checks.

Only this task's isolated receipt branch is published. Its source and receipt-parent workflows are the same manual-dispatch-only Pages workflow; no dispatch, integration or deployment is performed. Home and unrelated checkouts are preserved. Exact remote SHA/scope/evidence verification and task-worktree cleanup are reported at closeout.


Commands ran sequentially in the exact committed owning checkout, with the home interpreter; baseline comparisons are explicitly identified below. Full command arrays, UTC timestamps, durations, failures, output diffs, checker and payload manifest are in the evidence ZIP.

| Stage | Command | Exit | Seconds |
| --- | --- | --- | --- |
| foi | `py/main_foi_features_of_interest.py --single-threaded` | 0 | 16.890839 |
| black | `-m black --check py/foi/foi_finals.py py/author_misc/mam4sef_index.py py/main_0_mega.py` | 0 | 0.412297 |
| focused-tests | `py/main_test.py py/tests/test_shared_html_styles.py py/tests/test_receipt_update_links.py py/tests/source_hygiene_test.py py/tests/test_prose_conventions.py py/tests/test_phonetic_display_release.py` | 0 | 81.888729 |
| html-foi | `py/check_html_syntax_and_sanity.py gh-pages/MAM-with-doc/foi` | 0 | 1.403997 |
| independent | `/workspace/scratch/check_basics_9f8901a9.py` | 0 | 0.327847 |

[Evidence](review-hourly-2026-11-11-9f8901a9-basics-evidence.zip). Receipt parent `605d4951cbf457e2a024c185a915d3b9fef87369`; source `9f8901a92f8f040060841b1e5ba19524b97bbba3`. This commit changes only the receipt, evidence and maintained status. No main/shared integration or deployment.
