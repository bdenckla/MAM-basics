# MAM-basics bounded hourly screen

State: completed 2026-11-11; bounded screen and focused checks only

Screened only `9bce144ecc823856cbb0fe417b87dbc8ef474447..d957048a20f671fbadea37325c91dd9c9bfe4ee9`: one commit / three paths. The complete utility and both page diffs plus the commit's recorded decision were inspected under the current Hebrew-prose procedures. No consequential introduced defect or repair established. Typed example records now supply either a plain tooltip definition or HTML contents. Ben's decision that compared pointed/bare forms use the same font is preserved; punctuation-only pairs retain the surrounding font. This is no new editorial interpretation or font assessment.

Actual `py/main_wlc_diffs_420422.py` reproduces all tracked outputs exactly in **0.710301 s**. Changed-source Black passes (0.178913 s). `py/main_test.py py/tests/test_shared_html_styles.py py/tests/test_prose_conventions.py` passes **six tests**, no failures/skips, in **32.558368 s** wall. The changed `gh-pages/wlc/420422` HTML scope returns 0 in 0.672933 s, retaining 692 informational undefined-class references and no fatal issues. No broader HTML scopes, mega/full suite, font build/baseline or source refresh was repeated.

Independent preservation passes in **0.076809 s**. Each abbreviation table has exactly **14 new lang="hbo" spans around seven example pairs**; +psq and +mqf have none, and the three plain definitions remain unchanged. Removing only those declared wrappers reconstructs the base table after folding serialization whitespace. Everything outside the abbreviation tables is byte-identical, including all 55 + 15 record rows. All **70 tooltip attributes**, Hebrew-run codepoints/order, links, IDs, images, scripts and styles remain exact. The shared WLC stylesheet itself is unchanged. No normalization is applied.

Lineage continues from `55f43c8684893454004f94710901e3f300c4a6f5`, retaining every historical row and finished receipt. Overall reviewed remains `210affe3ac2931473bead0de839be0de08309e3d`; broad-tested remains `354cc0b7077cb46ba5d7cfc8dd9b453ff68c7bf0`. The earlier a5b89a8d responsive-browser attempts/gap remain explicit and were not repeated; no visual browser, font-QA, source/manuscript/editorial or broad-suite pass is claimed. Private is unchanged and was not rechecked. No HP retry, source acquisition, outside-agent contact, hbofonts, main/shared integration, deployment/dispatch or schedule work. Local cloud ownership was clear; cross-machine ownership remains unverified. Source and receipt parent retain only the same manual-dispatch Pages workflow, verified before the fresh isolated receipt publication.


Commands ran sequentially in the exact committed owning checkout, with the home interpreter; baseline comparisons are explicitly identified below. Full command arrays, UTC timestamps, durations, failures, output diffs, checker and payload manifest are in the evidence ZIP.

| Stage | Command | Exit | Seconds |
| --- | --- | --- | --- |
| regenerate | `py/main_wlc_diffs_420422.py` | 0 | 0.710301 |
| black | `-m black --check py/py_wlc_diffs_420422/my_word_diffs_420422_utils.py` | 0 | 0.178913 |
| focused-tests | `py/main_test.py py/tests/test_shared_html_styles.py py/tests/test_prose_conventions.py` | 0 | 32.558368 |
| html-420422 | `py/check_html_syntax_and_sanity.py gh-pages/wlc/420422` | 0 | 0.672933 |
| independent | `/workspace/scratch/check_basics_d957048a.py` | 0 | 0.076809 |

[Evidence](review-hourly-2026-11-11-d957048a-basics-evidence.zip). Receipt parent `55f43c8684893454004f94710901e3f300c4a6f5`; source `d957048a20f671fbadea37325c91dd9c9bfe4ee9`. This commit changes only the receipt, evidence and maintained status. No main/shared integration or deployment.
