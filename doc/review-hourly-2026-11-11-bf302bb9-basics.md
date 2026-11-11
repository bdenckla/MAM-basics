# MAM-basics bounded hourly screen

State: completed 2026-11-11; bounded screen and focused checks only

Reviewed only `cd0a5d16bbfdfd96acef4ee7a3936fb47d21bf8e..bf302bb9e27ed0de4cbfcfc4c4ff51e6e06741be`: two commits / ten complete endpoint paths. No consequential introduced defect or repair. The new 760-byte forwarding stub is the only change in the published tree; all 3,112 previously published files retain their exact Git blobs. The existing main-page stub, sixteen case/topic pages and their Hebrew/prose are unchanged. Source/title-helper, orchestration, checker/site inventories, license row and routed skill guidance agree on the two stubs. The README records the owner's acceptance of the prior styling; no visual or editorial judgment is reopened.

Actual `py/main_authored.py gen-site --trust-surveys` reproduces all outputs exactly in **5.681041 s**. The selected fourteen-file test command passes **42 tests**, 100.116248 s wall / 98.14 s pytest. Black passes all six changed Python files (0.211807 s); both the deploy-root and post-stress-meteg HTML checks return 0. No broad suite/mega was run.

Independent isolated calls to the actual stub writer reproduce both committed stubs byte for byte. Canonical, refresh, script and visible-link targets agree and exist; the new stub's title agrees with its destination page; a missing-stub probe verifies the checker guard. An independent Node VM runs each exact committed script with six query/fragment combinations: **12 executions pass**, preserving query and fragment bytes. This is script execution with a location mock, not browser rendering or network navigation.

One reviewer setup failure is retained separately: `gen-site` was launched before the owned checkout finished populating. Python exited **2** because the entry point did not yet exist; no generator executed. The original log, status and empty tracked diff are preserved. After the worktree command completed, exact HEAD, entry-point presence and clean status were verified, then the command ran once as `gen-site-ready`. No product repair, blind restoration or completed-check repetition occurred.

Overall reviewed remains `210affe3ac2931473bead0de839be0de08309e3d`; broad-tested remains `354cc0b7077cb46ba5d7cfc8dd9b453ff68c7bf0`. All inherited pending windows, failures and source/live/browser/editorial/corpus limits remain. No new source/image/cache, HP retry, outside-agent contact, font baseline/build, hbofonts, main/shared integration, deployment/dispatch or schedule work. Source and receipt parent have only the identical manual-dispatch Pages workflow. Only the isolated receipt/status/evidence branch is published. Local ownership was clear; cross-machine ownership remains unverified.


Commands ran sequentially in the exact committed owning checkout, with the home interpreter; baseline comparisons are explicitly identified below. Full command arrays, UTC timestamps, durations, failures, output diffs, checker and payload manifest are in the evidence ZIP.

| Stage | Command | Exit | Seconds |
| --- | --- | --- | --- |
| gen-site | `py/main_authored.py gen-site --trust-surveys` | 2 | 0.022190 |
| gen-site-ready | `py/main_authored.py gen-site --trust-surveys` | 0 | 5.681041 |
| black | `-m black --check py/author_site/post_stress_meteg.py py/author_site/site_data.py py/check_html_syntax_and_sanity.py py/main_0_mega.py py/main_authored.py py/tests/test_site_index_links.py` | 0 | 0.211807 |
| focused-tests | `py/main_test.py py/tests/test_site_index_links.py (full command in evidence)` | 0 | 100.116248 |
| html-root | `py/check_html_syntax_and_sanity.py --deploy-root` | 0 | 0.056876 |
| html-post-stress | `py/check_html_syntax_and_sanity.py gh-pages/post-stress-meteg` | 0 | 1.075293 |
| independent | `/workspace/scratch/check_basics_bf302bb9.py` | 0 | 0.295792 |
| redirect-js | `node /workspace/scratch/check_basics_bf302bb9_redirect.js` | 0 | 0.039731 |
| diff-check | `git diff --check` | 0 | 0.009039 |

[Evidence](review-hourly-2026-11-11-bf302bb9-basics-evidence.zip). Receipt parent `be15ab5e9e36d954e5bf395a3c45df06cf1aea79`; source `bf302bb9e27ed0de4cbfcfc4c4ff51e6e06741be`. This commit changes only the receipt, evidence and maintained status. No main/shared integration or deployment.
