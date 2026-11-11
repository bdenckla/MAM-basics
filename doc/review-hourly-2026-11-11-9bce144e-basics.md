# MAM-basics bounded hourly screen

State: completed 2026-11-11; bounded screen and focused checks only

Screened only `a5b89a8df9eb0ce6fd821e91c7b002f0c117c8d2..9bce144ecc823856cbb0fe417b87dbc8ef474447`: two commits / **50 complete endpoint paths** (the connector summary said 49). The actual inventory is 22 Python modules, 27 HTML pages and the shared-style guide. No consequential introduced defect or repair established. New prose supplies readable descriptions for the 26 FOI index entries; the index and existing pages now use the already-maintained arrow-link stylesheet/helper. The complete source delta, descriptions and guidance were inspected under the Hebrew-prose rules. No new source/manuscript/editorial judgment is claimed.

Actual `py/main_foi_features_of_interest.py --single-threaded` reproduces all tracked output exactly in **16.022099 s**. All 22 changed Python files pass Black (0.353825 s). The selected four-file `py/main_test.py` command passes **31 tests**, no failures/skips, in **30.106449 s** wall / 29.86 s pytest. The FOI HTML checker returns 0 (1.258206 s), with 1,159 informational undefined-class references and no fatal issues. No full suite/mega or source refresh ran.

Independent comparison passes in **0.889971 s**: all **26 JSON blobs** remain exact; all **26 non-index DOMs** equal base after excluding only the added shared stylesheet/data-na-link attributes and folding serializer whitespace. All 27 pages retain their Hebrew-run sequences, href sequences, IDs, exact script/style/image bytes. All **3,219 local link occurrences**, including file and HTML-fragment targets, resolve in the frozen tree. The 26 index entries each have a readable description and the complete key set agrees with the generated pages. The actual coverage-guard function, extracted from the frozen AST without importing product modules, accepts the complete key set and rejects missing and extra keys. The writer still skips index generation for a selected-FOI run.

Outside foi_finals, all 21 changed modules are AST-identical after excluding only the new INDEX_DESCRIPTION assignments and the two descriptor-only imports. The changed final writer applies the existing pure link decorator before its existing temporary-file writer; JSON and finder semantics remain unchanged. Existing link presentation and CSS sources were not changed, so their unrelated consumers need no redundant regeneration in this window. Passing consistency checks do not independently establish source or editorial correctness.

Lineage continues from `5619790b090590f4e5f43f69c5ad57816ad2463d`; prior finished receipts and every historical status row remain. Overall reviewed stays `210affe3ac2931473bead0de839be0de08309e3d`; broad-tested stays `354cc0b7077cb46ba5d7cfc8dd9b453ff68c7bf0`. In particular, the preceding a5b89a8d responsive-browser gap remains unverified and its failed attempts are not repeated. All older source/live/editorial/corpus and checker limitations remain distinct. No Private content was used as review material. No HP retry, source acquisition, font build/baseline/refresh, hbofonts, outside-agent contact, main/shared integration, deployment/dispatch or schedule work. Local cloud ownership was clear; cross-machine ownership remains unverified. The source and receipt parent retain only the same manual-dispatch Pages workflow, verified before this isolated receipt publication.


Commands ran sequentially in the exact committed owning checkout, with the home interpreter; baseline comparisons are explicitly identified below. Full command arrays, UTC timestamps, durations, failures, output diffs, checker and payload manifest are in the evidence ZIP.

| Stage | Command | Exit | Seconds |
| --- | --- | --- | --- |
| foi | `py/main_foi_features_of_interest.py --single-threaded` | 0 | 16.022099 |
| black | `-m black (full command in evidence)` | 0 | 0.353825 |
| focused-tests | `py/main_test.py py/tests/test_foi_kq_trivial_types.py py/tests/test_shared_html_styles.py py/tests/test_prose_conventions.py py/tests/test_prose_mark_order.py` | 0 | 30.106449 |
| html-foi | `py/check_html_syntax_and_sanity.py gh-pages/MAM-with-doc/foi` | 0 | 1.258206 |
| independent | `/workspace/scratch/check_basics_9bce144e.py` | 0 | 0.889971 |

[Evidence](review-hourly-2026-11-11-9bce144e-basics-evidence.zip). Receipt parent `5619790b090590f4e5f43f69c5ad57816ad2463d`; source `9bce144ecc823856cbb0fe417b87dbc8ef474447`. This commit changes only the receipt, evidence and maintained status. No main/shared integration or deployment.
