# MAM-basics bounded hourly screen

State: completed 2026-11-11; bounded screen and focused checks only

Reviewed only `cba3b401666aa0a49147fdc54294086ff343de81..cd0a5d16bbfdfd96acef4ee7a3936fb47d21bf8e`: six commits and **402 complete checkout paths**, rather than the connector's capped 300. Complete inventory/patch retained. No consequential introduced defect established; no repair. Later main `f962a43a` was observed but is outside this screen.

Fifteen affected maintained generator/check commands reproduce exactly, including authored site/misc/Israel Bible/MP docs, accgram HTML, WLC/UXLC comparisons, CLC, Holman, Book of Job and its mapping consumer, near-Aleppo HTML check, Taamey D documentation only, MAM-simple documentation and change-log freshness. No frozen font generation, QA, corpus refresh or baseline acceptance. The selected 16-file repository test command passes **84 tests**, 94.306648 s wall / 93.99 s pytest; all 54 changed Python files pass Black.

Independent comparison of all **341 changed HTML pages** preserves every node/attribute and non-whitespace text after exactly 2,239 same-site link conversions and Israel Bible's one added shared stylesheet, 112 form-class substitutions and three inline-class removals. Hebrew codepoint sequences remain exact. The entire enriched Job JSON differs only by four link conversions. Fifteen helper probes and four fragment/cache probes pass; query/fragment suffixes, directory landing pages, percent-encoded targets and invalid paths are covered. Whitespace folding is explicit; no Unicode normalization was used. Source review confirms the Numbers remap remains and chat/data-notice builders keep absolute URLs; the narrowed Holman link builder's maintained non-page callers select only its unchanged UXLC link.

HTML checks pass for deploy root, MAM-with-doc, book-of-job, CLC, Israel Bible, near-Aleppo and post-stress-meteg. Six other affected scopes remain **exit 1**, with preserved baseline reports: MAM-parsed 10 issues, MAM-simple 1, Holman 5, Taamey D 8, UXLC 2 and WLC 11. The UXLC base had nine: exactly the seven declared legacy CLC stub orphans disappear. Other five issue lists remain unchanged; informational CSS references remain separately reported. None is called a clean checker pass.

Licensing changes follow the recorded owner decisions: Ben answered GPL-3.0 for the Israel Bible prose/input; quoted forms retain source terms and the crop has no new grant. CLC's no-grant rows retain the evacuated source's terms. Israel Bible typography/readability and owner source judgments are not independently adjudicated by regeneration. The removed final-message instruction is prose-only; it restores the earlier body without altering executable policy.

Overall reviewed remains `210affe3ac2931473bead0de839be0de08309e3d`; broad-tested remains `354cc0b7077cb46ba5d7cfc8dd9b453ff68c7bf0`. All inherited pending windows, historical failures and source/live/manuscript/browser/editorial/corpus limits remain. No broad mega/full suite, fresh source/cache, HP, hbofonts, external validation, deployment/dispatch, main/shared integration or schedule work. Local ownership was clear; cross-machine HP ownership remains unverified. Sole Pages workflow at source/receipt parent is manual dispatch. Only the isolated receipt branch is published.


Commands ran sequentially in the exact committed owning checkout, with the home interpreter; baseline comparisons are explicitly identified below. Full command arrays, UTC timestamps, durations, failures, output diffs, checker and payload manifest are in the evidence ZIP.

| Stage | Command | Exit | Seconds |
| --- | --- | --- | --- |
| gen-site | `py/main_authored.py gen-site --trust-surveys` | 0 | 5.665713 |
| gen-misc | `py/main_authored.py gen-misc` | 0 | 1.886659 |
| gen-israel | `py/main_authored.py gen-israel-bible-review` | 0 | 1.337163 |
| gen-mp-docs | `py/main_authored.py gen-mam-parsed-docs` | 0 | 3.925540 |
| accgram-html | `py/main_accgram.py generate-html --trust-survey` | 0 | 10.562287 |
| wlc-420422 | `py/main_wlc_diffs_420422.py` | 0 | 0.498719 |
| amb-early | `py/main_amb_early_mtg.py` | 0 | 0.964602 |
| clc | `py/main_clc.py all` | 0 | 0.810758 |
| holman-render | `py/main_verify_and_render_table.py` | 0 | 1.039928 |
| job-site | `py/main_gen_misc_authored_english_documents.py` | 0 | 1.571848 |
| job-map-changes | `py/main_map_changes_to_book_of_job.py` | 0 | 0.049536 |
| near-aleppo-html | `py/main_near_aleppo.py --html --check` | 0 | 26.990719 |
| taamey-doc | `py/main_taamey_d.py doc` | 0 | 0.046398 |
| mam-simple-doc | `py/main_mam_simple.py doc-only` | 0 | 0.205783 |
| change-log-check | `py/main_diff.py mpplus --check` | 0 | 7.020515 |
| black | `-m black --check` (54 changed Python files; full command in evidence) | 0 | 1.235100 |
| focused-tests | `py/main_test.py` (16 explicit test files; full command in evidence) | 0 | 94.306648 |
| html-root | `py/check_html_syntax_and_sanity.py --deploy-root` | 0 | 0.071405 |
| html-MAM-parsed | `py/check_html_syntax_and_sanity.py gh-pages/MAM-parsed` | 1 | 0.109109 |
| html-MAM-simple | `py/check_html_syntax_and_sanity.py gh-pages/MAM-simple` | 1 | 0.135142 |
| html-MAM-with-doc | `py/check_html_syntax_and_sanity.py gh-pages/MAM-with-doc` | 0 | 1.471624 |
| html-book-of-job | `py/check_html_syntax_and_sanity.py gh-pages/book-of-job` | 0 | 0.379022 |
| html-clc | `py/check_html_syntax_and_sanity.py gh-pages/clc` | 0 | 0.319052 |
| html-holman | `py/check_html_syntax_and_sanity.py gh-pages/holman` | 1 | 0.965709 |
| html-israel-bible-review | `py/check_html_syntax_and_sanity.py gh-pages/israel-bible-review` | 0 | 0.089587 |
| html-near-aleppo | `py/check_html_syntax_and_sanity.py gh-pages/near-aleppo` | 0 | 1.617853 |
| html-post-stress-meteg | `py/check_html_syntax_and_sanity.py gh-pages/post-stress-meteg` | 0 | 1.155973 |
| html-taamey-d | `py/check_html_syntax_and_sanity.py gh-pages/taamey-d` | 1 | 0.084150 |
| html-uxlc | `py/check_html_syntax_and_sanity.py gh-pages/uxlc` | 1 | 0.845316 |
| html-wlc | `py/check_html_syntax_and_sanity.py gh-pages/wlc` | 1 | 1.203268 |
| independent | `/workspace/scratch/check_basics_cd0a5d16.py` | 0 | 2.531323 |
| html-base-MAM-parsed | `py/check_html_syntax_and_sanity.py gh-pages/MAM-parsed` | 1 | 0.069823 |
| html-base-MAM-simple | `py/check_html_syntax_and_sanity.py gh-pages/MAM-simple` | 1 | 0.071035 |
| html-base-holman | `py/check_html_syntax_and_sanity.py gh-pages/holman` | 1 | 0.185335 |
| html-base-taamey-d | `py/check_html_syntax_and_sanity.py gh-pages/taamey-d` | 1 | 0.097127 |
| html-base-uxlc | `py/check_html_syntax_and_sanity.py gh-pages/uxlc` | 1 | 0.146958 |
| html-base-wlc | `py/check_html_syntax_and_sanity.py gh-pages/wlc` | 1 | 0.365367 |
| diff-check | `git diff --check` | 0 | 0.011485 |

[Evidence](review-hourly-2026-11-11-cd0a5d16-basics-evidence.zip). Receipt parent `0fe766ec95082e00f178793cd9e71a7d8e0b5d1d`; source `cd0a5d16bbfdfd96acef4ee7a3936fb47d21bf8e`. This commit changes only the receipt, evidence and maintained status. No main/shared integration or deployment.
