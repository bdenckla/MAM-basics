# Bounded MAM-basics screen: 7542d563

State: completed 2026-11-11; focused offline review and execution only

Codex reviewed `9006ea5ca465642faa60aaf13fdd9391780b57ef..7542d5636edeec99e7493249130df7a298b1144a`: 12 reachable commits and 83 rename-aware changed paths. Receipt parent: `d9effa2afaff1fbf52c14288844c91832071ca78`. No consequential introduced defect or product repair was established. The source head, committed inputs and owning Python 3.13.15 environment were isolated; no sibling input was needed.

## Findings and disposition

- The three-book refresh changes notes at 2 Samuel 21:19, Jeremiah 39:13 and 2 Chronicles 35:9. Selected Scripture fields and all other plus content are unchanged after omitting documentation bodies only. Raw, parsed and prototype deltas are retained; live revision authenticity and manuscript claims remain attributed.
- Near-Aleppo keeps all 1,558 ledger rows, with only two changed reviews: the same targets now have 1,052 recast / 506 framed presentations. All other 1,556 rows remain identical. The maintained fresh-enumeration, build and HTML checks pass; no new interpretation or stored pointing was introduced by this screen.
- All 36 unused images are retained byte-identically at their new non-deployment paths. The unused CSV and misc index are removed as requested. All 20 page-generation calls are preserved. Every page on the earlier 19 root-reachability routes remains byte-identical. Existing human-review caveats remain.
- The special-page manifest's 36 retained captures match its existing sizes/hashes; the two refreshed special pages are inspected as captures, without normalization or source acquisition. The change log differs only in its current plus-tree identity; the listed changes are unchanged. Four sigil prose-token count deltas agree with the note edits and maintained regeneration.
- Morphology's Python edit is docstring-only. Upstream PR/merge statements remain owner-attributed. The optional export had already completed before the coordinator clarified the exemption; it reproduces exactly and was not repeated.

## Checks actually executed

Every command below uses `/workspace/MAM-basics/.venv/bin/python` from the frozen source worktree. All 16 maintained commands leave zero tracked or untracked differences. Full commands, paths, output and timings are in the evidence archive.

| Maintained command | Result | Wall seconds |
| --- | --- | --- |
| `py/main_authored.py gen-misc` | 0; no differences | 1.820866 |
| `py/main_mam_morphhb.py` | 0; no differences | 1.126308 |
| `py/main_parse.py ws --book39 2Samuel` | 0; no differences | 3.783229 |
| `py/main_parse.py ws --book39 Jeremiah` | 0; no differences | 3.898745 |
| `py/main_parse.py ws --book39 2Chronicles` | 0; no differences | 3.813353 |
| `py/main_mam_with_doc.py --book39 2Samuel` | 0; no differences | 0.251483 |
| `py/main_mam_with_doc.py --book39 Jeremiah` | 0; no differences | 0.371337 |
| `py/main_mam_with_doc.py --book39 2Chronicles` | 0; no differences | 0.241078 |
| `py/main_sigil_inventory.py` | 0; no differences | 0.589777 |
| `py/main_near_aleppo.py --check-note-review` | 0; no differences | 13.463147 |
| `py/main_near_aleppo.py --build --check` | 0; no differences | 19.266327 |
| `py/main_near_aleppo.py --html --check` | 0; no differences | 24.637718 |
| `py/main_diff.py mpplus --check` | 0; no differences | 6.327237 |
| `py/check_html_syntax_and_sanity.py gh-pages/MAM-with-doc` | 0; no differences | 1.416308 |
| `py/main_test.py` with the targets below | 26 passed; 0 failed/skipped (22.87 s pytest) | 23.054164 |
| `-m black --check` on all eight changed Python files | all unchanged | 0.319662 |

The test selection is `test_site_index_links.py`, `test_deploy_root_html.py`, `test_redirect_manifest.py`, `test_prose_conventions.py`, `test_prose_mark_order.py`, `test_near_aleppo_note_content.py`, plus the special-page independent-inventory test and the change-log declared-artifact test. All run through `py/main_test.py -q`; the exact node IDs are retained in `execution-summary.json`.

Twelve additional probes exercise the actual HTML-checker functions: relative/published paths, fragments, percent-decoding, queries, directory indexes, foreign-site exclusion, root-index orphan accounting, the explicit outside-link exception and its missing-file guard, recursive scope, JSON/Markdown allowance, retained empty-file/extension diagnostics and deploy-relative boundaries. The complete independent endpoint/probe check passes in 1.249544 s.

## HTML report accounting and diagnostics

The checker immediately before its repair, at `7a0ea7a3bfa9c1ef0e3e6d6f35fb5d1ea20e2a51`, returns **exit 1 with 80 issues** in 1.437232 s. The final checker returns **exit 0 with zero fatal issues**. Its exact accounting is 36 orphan-image reports plus two GIF-type reports for the same moved image set; 34 JSON and one Markdown report covered by explicit permitted extensions; one unused CSV deleted; and six HTML orphan reports covered by five top-index links plus one explicit outside-linked stub.

Both reports still contain **16,966 informational undefined CSS class references**. They are not independently validated definitions or a warning-free result. No W3C upload occurred.

Two scratch-review assumptions were corrected with originals preserved: an ID assertion omitted the ledger's Hebrew sub-book label; a report summarizer omitted the two GIF-type reports. Only the corrected scratch checker reran. The report correction reads saved logs only; no maintained test, generator or CLI checker was repeated for either correction. No product changed.

## Coverage limits and publication

Overall reviewed-through remains `210affe3ac2931473bead0de839be0de08309e3d`; broad-tested remains `73fbf0406b8cf843b2aabcbb8ef0b558d0fa7148`. Prior receipts and every inherited Stage 10/PR369/source/live/browser/editorial limitation, including read-only Taamey D corpus REFRESH PENDING, remain unchanged. No full suite/mega or source-refresh dependency-loop rerun is claimed. Upstream PR status, live sources, manuscripts, browser/font rendering and informational CSS ownership are not independently closed by these checks.

The receipt continues only the isolated receipt lineage; it imports no source main changes. Source head and receipt parent both have only manual-dispatch Pages workflow `18ceb19405424710bda47d9a38c470cc2ed9c385`. Publication to `review-hourly-20261111-7542d563-basics-receipts` cannot trigger that workflow. No main/shared integration, deployment/dispatch, bot save, external validation upload, font/hbofonts or schedule operation occurred. No remote CI result is inferred.

[Independent checker](review-hourly-2026-11-11-7542d563-basics-check.py) and [verified evidence](review-hourly-2026-11-11-7542d563-basics-evidence.zip): 80,563 bytes; SHA-256 `c5f6d6b7cea95d0b2095625b5e710d3aaaf1df71a602cf6f503b802c5c4ad6d7`. All 88 unique members, CRCs and manifest sizes/hashes verified. Earlier results remain at the [immutable prior receipt](https://github.com/bdenckla/MAM-basics/blob/d9effa2afaff1fbf52c14288844c91832071ca78/doc/review-hourly-2026-11-11-9006ea5c-basics.json).
