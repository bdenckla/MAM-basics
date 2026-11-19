# Bounded Sheet credit-port and contributors review

State: completed 2026-11-19; review only

Codex (GPT-6, xhigh), November 19 19:00 UTC screen. Frozen `5ed853e2670bac7a7158553848cb66fad375fb53` -> `45c6f6a85cb5f144447f678781b75eb2b4b331a8` (2 commits / 21 paths). **No consequential introduced defect or product repair established.** Current guidance and the complete endpoint were inspected; recorded owner decisions remain attributed and are preserved.

**41 maintained tests pass (29.02s), with no skips. Ten distinct independent probes pass after correcting one census assumption**: the first invocation had 8 passed/1 failed; only the failed case was rerun (1 pass), then one association/order probe passed. The failed assertion counted shared UI IDs across documents as credit IDs. Its original helper/log and corrected result are preserved; no product changed.

The port has 62 records / 8 contributors:61 Sheet credits from 28 distinct frozen rows, plus the existing credit. Report matches are 39/4/1/17/1 in 2025-03-19a,2026-03-06,2026-03-16,2026-09-17 and unpinned-latest. Row 142's owner-selected verse, the joint 9/240 evidence, row 104's two credits and excluded 249/264/273 are consistent with the local data/record. The capture remains 189,511 bytes / 1,084 CSV records, with manifest SHA-256 030cb757… unchanged. This checks bounded accounting, not the owner's entire overlap survey or its editorial conclusions.

All 62 credit IDs independently match their selector digests and remain stable under metadata/record-order changes; suffix behavior is checked. All 125 local navigation links resolve, and every contributor grouping, change order, evidence association and rendered form matches its linked card. Ruby markup is preserved on the one affected credited card. Absent/duplicate cards, wrong verse line, missing credit line and absent forms refuse; names/template fallback escape safely. Existing report JSON differs only by credits; HTML only by credit lines and IDs. Unrelated report data/forms, stylesheet, filter and release inventory stay exact; index adds only its declared link. Contributors output is registered for regeneration/currentness/pinning. Actual `mpplus --all` and `--check` reproduce every committed product. Scoped HTML exits 0, with 100 informational CSS references; this is not broader site/browser proof.

Actual sequential commands from the owned source checkout `/workspace/scratch/hourly-20261119-port/basics-source`, using its home interpreter (Python 3.13.15; the corresponding subtree cwd where recorded):

| Stage | Command | Exit | Wall seconds |
| --- | --- | ---: | ---: |
| diff-check | `git diff --check 5ed853e2670bac7a7158553848cb66fad375fb53 45c6f6a85cb5f144447f678781b75eb2b4b331a8` | 0 | 0.030513 |
| black | `/workspace/MAM-basics/.venv/bin/python -m black --check py/mb_diff_mpu/mpplus_contributors.py py/mb_diff_mpu/mpplus_credits.py py/mb_diff_mpu/mpplus_html.py py/mb_diff_mpu/mpplus_index.py py/subcommands/diff_mpplus.py py/tests/test_diff_mpplus_unpinned_latest.py` | 0 | 0.305140 |
| mpplus-all | `/workspace/MAM-basics/.venv/bin/python py/main_diff.py mpplus --all` | 0 | 6.196326 |
| mpplus-check | `/workspace/MAM-basics/.venv/bin/python py/main_diff.py mpplus --check` | 0 | 6.601955 |
| focused-tests | `/workspace/MAM-basics/.venv/bin/python py/main_test.py py/tests/test_diff_mpplus_unpinned_latest.py py/tests/test_mpplus_extract.py py/tests/test_mpplus_historical_archives.py py/tests/test_mpplus_alternative_oracle.py py/tests/test_shared_html_styles.py -q -ra` | 0 | 29.615764 |
| change-log-html | `/workspace/MAM-basics/.venv/bin/python py/check_html_syntax_and_sanity.py gh-pages/MAM-with-doc/change-log` | 0 | 1.239155 |
| port-probe | `/workspace/MAM-basics/.venv/bin/python py/main_test.py /workspace/scratch/hourly-20261119-port/public-artifacts/test_port_review.py -q -ra` | 1 | 0.488958 |
| port-probe-corrected | `/workspace/MAM-basics/.venv/bin/python py/main_test.py /workspace/scratch/hourly-20261119-port/public-artifacts/test_port_review.py::test_ids_forms_links_and_output_preservation -q -ra` | 0 | 0.929603 |
| association-order-probe | `/workspace/MAM-basics/.venv/bin/python py/main_test.py /workspace/scratch/hourly-20261119-port/public-artifacts/test_port_review.py::test_contributor_associations_and_order -q -ra` | 0 | 0.408041 |

Owner credit identities, selection decisions, complete Sheet research and external source/rights claims remain attributed. No live Sheet/Wikisource request, new attribution, contributor contact, plan continuation, issue action or broad rerun. No source/rights/editorial decision is supplied by synthetic checks. No archived/BHSA or frozen font/hbofonts operation, baseline acceptance, PR/issue, configuration/schedule, deployment/dispatch or main/shared integration. Expected refusal cases are successful checks; scratch failures are explicitly distinguished from repository failures.

Local admission at `2026-11-19T19:21:29.216524+00:00` verified clean homes, released prior slots, no running check process and only this visible task. Source and receipt use detached committed worktrees with the owning home environment; no sibling runtime input was required. Cross-machine owner activity remains unverified; no owner visual/editorial checkout was used or task duplicated.

Only isolated branch `review/hourly-20261117-3691d51b` advances from sole receipt parent `e024116922a6138fe5d9a5824028f80820d7a9bf`. All previous status bytes, immutable receipts, nightly/HP records and historical limits remain. Overall reviewed-through stays `210affe3ac2931473bead0de839be0de08309e3d`; independent broad-tested stays November 19 nightly `54aaab9300e1559c891275a547dd516a84207354`. Earlier gaps remain; this bounded result supplies no older missing coverage. Fresh connected PR searches were empty; source/parent retain the verified non-deploying workflow state. Remote bytes, three-path scope, ancestry and owned cleanup are verified at publication/closeout.

[Evidence](review-hourly-2026-11-19-45c6f6a8-basics-evidence.zip): **66415 bytes**, SHA-256 `749f62464499464f41ca1ac1e37df55e5bb38db4da30b233108335dd4bbc1529`, **40** safe regular payloads plus self-excluding `manifest.json`. CRCs and all payload hashes/sizes verified. Includes complete endpoint patch, immutable source/blob manifest, actual commands/logs, original failed scratch helper and corrected evidence, and status-preservation proof.
