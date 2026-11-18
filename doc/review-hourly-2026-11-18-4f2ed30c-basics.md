# Bounded MAM-basics stress-helper review, 2026-11-18

State: completed 2026-11-18; review only

Codex reviewed only `8c2c3378487c9587659cd0b4a8f3db4690dbcf08` -> `4f2ed30c5ba8764baa01884637c90248892576f5`: nine commits / 90 paths. No consequential introduced defect or product repair established. Public review material and execution were public-only, from a detached committed checkout using `/workspace/MAM-basics/.venv/bin/python`; these focused commands require no sibling input.

Actual maintained checks, sequentially from the repository root:

| Command | Actual result |
| --- | --- |
| `git diff --check 8c2c3378 4f2ed30c` | exit 0 |
| `-m black --check py/author_site/stress_helper_comparison.py` | one file unchanged; exit 0 |
| `py/main_authored.py gen-site --trust-surveys` | exact committed outputs; exit 0, 5.963938 s wall |
| `py/main_test.py py/tests/test_prose_conventions.py py/tests/test_prose_mark_order.py py/tests/test_shared_html_styles.py -q` | 7 passed, no skips, 33.45 s pytest / 33.702131 s wall; exit 0 |
| `py/check_html_syntax_and_sanity.py gh-pages/stress-helpers` | exit 1: four historical orphan crops, 263 informational CSS references |

Every maintained check leaves empty tracked/untracked status and no generated diff. The four retained orphan crops are pending findings, not a pass or an introduced regression. Exact commands, outputs and exits are in the [evidence](review-hourly-2026-11-18-4f2ed30c-basics-evidence.zip).

Independent committed-data/DOM checks reconcile 51 original edition records into 37 rows and 74 further-result records into 56 rows. All 74 retained MAM words and their identities remain exact; original-page MAM/printed words remain exact. Expected source edition sets independently determine each row's filter suffix and each option's population. All 370 local link/asset occurrences resolve, including local fragments. All 130 PNGs verify, 126 are linked, and all 74 new crops are linked with matching record edition/scan/BCV/atom filename associations. The further-results page has the intended printed words, page/appendix labels, hidden crops and image button. Omitted census/spelling presentation and the single withdrawn comparison follow recorded owner choices; their underlying research judgments were not independently reconstructed.

The actual committed JavaScript passes 4,068 offline filter/search combinations and 4,096 counted option/control checks, including both pages' image toggles and size/reset behavior. This uses a disposable DOM adapter, not browser layout or native rendering. The executor viewed four committed crops and found no obvious mismatch in their visible word portions. Separately, the coordinator viewed the two exact committed Simanim crops named by the sign-height correction and observed the short jagged sign below the circular sign on the same letter. Those bounded observations, immutable blob/hash references and methods are retained without duplicating images. Full-page identity, original scans, census/source evidence, sign classifications, editorial and rights judgments remain unverified or owner-attributed.

One reviewer probe initially failed because it expected a boolean HTML attribute's value to be `hidden`; lxml represents the present attribute with an empty value. Corrected presence checks and the later strengthened data assertions pass; original script/log remain evidence. Initial setup found the receipt remote-tracking ref absent (Git exit 128, setup exit 1); a narrow fetch resolved it before ownership/check execution. Author-reported UTF8-off reproduction, 27/29 focused tests, check_all, later prose/config tests and earlier broad results remain attributed; no duplicate mega/full suite, live source/bot/email, frozen study, font build/baseline, native Windows or browser check ran.

The public archive replaces only the temporary checkout directory prefix with `/PUBLIC_REVIEW_SCRATCH`, because its original name embedded a private identifier. An omission note lists affected files and replacement counts; unmodified original diagnostics and reversible hashes are preserved privately. No command, exit, result or product bytes were changed, and no checks were rerun for this evidence correction.

Receipt parent `6a59cbcc568a55144cbcd19bb4a7932af2de1dfb` and every earlier status byte/finished receipt are preserved. Global reviewed-through stays `210affe3ac2931473bead0de839be0de08309e3d`; last broad-tested stays at the November 18 nightly source `8c2c3378487c9587659cd0b4a8f3db4690dbcf08`. Historical unreviewed windows, crop findings and source/browser/Windows/Taamey D limits remain distinct. Local admission was clear; cross-machine ownership is not independently verified. Only the established isolated receipt branch is extended after checking its exact parent, no dependent open PR, and the unchanged sole manual-dispatch Pages workflow. No main/shared integration, configuration installation, schedule change, dispatch or deployment. Remote scope/byte verification and owned-worktree/slot cleanup follow publication.
