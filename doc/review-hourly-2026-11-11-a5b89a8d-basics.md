# MAM-basics bounded hourly screen

State: completed 2026-11-11; bounded screen and focused checks only

Screened only `bf302bb9e27ed0de4cbfcfc4c4ff51e6e06741be..a5b89a8df9eb0ce6fd821e91c7b002f0c117c8d2`: five commits / thirteen complete endpoint paths. No consequential introduced defect or product repair established by source and focused execution checks. The CSS bounds, 420422 column order/nowrap classes, shared-style guidance and approved removal of the duplicate index caveat were reviewed. Ben's index-caveat decision is preserved; the complete linked page and its AI caveat are byte-identical to base. Actual responsive rendering remains unverified after the two failed browser harness attempts below.

All three affected maintained generators reproduce committed outputs exactly: `py/main_wlc_diffs_420422.py` (0.690468 s), `py/main_mam_simple.py doc-only` (0.360341 s), and `py/main_authored.py gen-site --trust-surveys` (5.654443 s). Five-file Black passes (0.228969 s). The six-file selected command through `py/main_test.py` passes **16 tests**, no skips/failures, in 30.355975 s wall / 30.16 s pytest. The misc author change is module-docstring-only; its AST is otherwise identical, so no redundant gen-misc run is owed. No broad suite/mega or source refresh was run.

Independent committed-byte checks cover all thirteen paths and preserve every cell's contents/attributes in the **55 + 15 record rows**, after only the declared column reorder and two classes; each list's twelve abbreviation rows differ only by nowrap and serialization whitespace. All link destinations, pointed forms and other content remain. The generated/source MAM-simple CSS copies match exactly. Comment-only WriteCtx code and docstring-only misc author remain AST-identical after removing only the module docstring. Complete class-token census finds **158 centered pages**, **97 with limited-width tables**, including the sixteen multiple-class post-stress pages. The initial exact-body-string census counted only 142/92; the supplemental census preserves that diagnostic and accounts for the omitted class shapes without repeating the successful row comparisons.

Deploy-root and post-stress HTML checks pass. WLC and MAM-simple checks return **1**, with **eleven** and **one** inherited issues respectively: ten unused-image orphans plus the retained XML extension, and the orphan reading-mam-simple-xml page. Every fatal diagnostic line matches the preserved cd0a5d16 run; informational undefined-class counts are explicitly excluded from that comparison. The checker AST is unchanged apart from the intervening, already-reviewed forwarding-stub allowlist. The first census attempt wrongly required whole-file identity across that earlier change and failed; its original code/log are retained, and the corrected scoped comparison passes. These remain failed HTML commands, not clean passes.

Chromium 151.0.7922.173 is installed. The first offline dump-DOM/iframe harness timed out after **60.177417 s**, producing no trustworthy geometry result. After confirming no live first-attempt descendants, a separate bounded CDP harness started Chromium and blocked HTTP(S) before local navigation, but reached **chrome-error://chromewebdata/** instead of the first committed local page; it failed in **0.704890 s**. Logs, both exact harnesses and the CDP command/call record are preserved. The underlying local-file navigation failure is unresolved; no successful table geometry, screenshot, visual, mobile or cross-browser proof is claimed. Only task-created profiles were removed after the attempts ended; no live task browser remained. A safely functioning local browser loading the exact frozen pages is the next trigger for the remaining responsive/rendering check; this task makes no speculative CSS repair.

Receipt lineage continues from `dc737811eb9e6a7f94d3b57a75a1731c7f484a51`, preserving every historical row/receipt. Overall reviewed stays `210affe3ac2931473bead0de839be0de08309e3d`; broad-tested stays `354cc0b7077cb46ba5d7cfc8dd9b453ff68c7bf0`. Earlier pending windows and all source/live/corpus/browser/editorial limits remain distinct. No Private review or repeated checks, original/source acquisition, HP retry, outside-agent contact, font baseline/build/refresh, hbofonts, main/shared integration, deployment/dispatch or schedule work. Local cloud ownership/processes were clear; cross-machine ownership remains unverified. Both source and receipt parent have only the identical manual-dispatch Pages workflow (blob `18ceb19405424710bda47d9a38c470cc2ed9c385`), so this fresh isolated receipt branch cannot trigger deployment. Coordinator observations of empty statuses/no PR workflow are absence of CI evidence, not a CI pass.


Commands ran sequentially in the exact committed owning checkout, with the home interpreter; baseline comparisons are explicitly identified below. Full command arrays, UTC timestamps, durations, failures, output diffs, checker and payload manifest are in the evidence ZIP.

| Stage | Command | Exit | Seconds |
| --- | --- | --- | --- |
| gen-wlc420422 | `py/main_wlc_diffs_420422.py` | 0 | 0.690468 |
| gen-mam-simple-doc | `py/main_mam_simple.py doc-only` | 0 | 0.360341 |
| gen-site | `py/main_authored.py gen-site --trust-surveys` | 0 | 5.654443 |
| black | `-m black --check py/author_misc/he_ws_intro_to_mam_gaya_text.py py/author_site/site_data.py py/py_html/wlc_utils_html.py py/py_wlc_diffs_420422/my_word_diffs_420422_summary.py py/py_wlc_diffs_420422/my_word_diffs_420422_utils.py` | 0 | 0.228969 |
| focused-tests | `py/main_test.py py/tests/test_shared_html_styles.py (full command in evidence)` | 0 | 30.355975 |
| html-root | `py/check_html_syntax_and_sanity.py --deploy-root` | 0 | 0.069797 |
| html-wlc | `py/check_html_syntax_and_sanity.py gh-pages/wlc` | 1 | 1.156125 |
| html-post-stress | `py/check_html_syntax_and_sanity.py gh-pages/post-stress-meteg` | 0 | 1.085157 |
| html-mam-simple | `py/check_html_syntax_and_sanity.py gh-pages/MAM-simple` | 1 | 0.118101 |
| independent | `/workspace/scratch/check_basics_a5b89a8d.py` | 0 | 0.384238 |
| browser | `/workspace/scratch/browser_basics_a5b89a8d.py` | 1 | 60.177417 |
| census | `/workspace/scratch/census_basics_a5b89a8d.py` | 1 | 0.308365 |
| browser-cdp | `/workspace/scratch/browser_cdp_basics_a5b89a8d.py` | 1 | 0.704890 |
| census-corrected | `/workspace/scratch/census_corrected_basics_a5b89a8d.py` | 0 | 0.568897 |

[Evidence](review-hourly-2026-11-11-a5b89a8d-basics-evidence.zip). Receipt parent `dc737811eb9e6a7f94d3b57a75a1731c7f484a51`; source `a5b89a8df9eb0ce6fd821e91c7b002f0c117c8d2`. This commit changes only the receipt, evidence and maintained status. No main/shared integration or deployment.
