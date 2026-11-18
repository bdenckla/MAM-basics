# Bounded MAM-basics merged stress-helper review, 2026-11-18

State: completed 2026-11-18; review only

Codex reviewed only `4f2ed30c5ba8764baa01884637c90248892576f5` -> `efb3bd01cb3ed01f8f37d4e7cd6af59cb146734f`: two commits / 11 paths. No consequential introduced defect or product repair established. Review and checks used a detached exact committed checkout, public material only and `/workspace/MAM-basics/.venv/bin/python` from the repository root. These focused checks require no sibling input.

Actual sequential maintained checks:

| Command | Result |
| --- | --- |
| `git diff --check 4f2ed30c efb3bd01` | exit 0 |
| `-m black --check py/author_site/stress_helper_comparison.py py/main_authored.py` | two files unchanged; exit 0 |
| `py/main_authored.py gen-site --trust-surveys` | exact committed outputs, exit 0; 5.534423 s wall |
| `py/main_test.py py/tests/test_prose_conventions.py py/tests/test_prose_mark_order.py py/tests/test_shared_html_styles.py py/tests/test_site_links_relative.py py/tests/test_site_index_links.py -q` | 12 passed, no skips; 33.90 s pytest / 34.080028 s wall; exit 0 |
| `py/check_html_syntax_and_sanity.py gh-pages/stress-helpers` | exit 1: the same four historical orphan crops, 273 informational CSS references |

All product stages leave clean status and empty diffs. The four orphan crops remain pending, not passing or newly introduced. [Evidence](review-hourly-2026-11-18-efb3bd01-basics-evidence.zip) preserves exact commands, exits and outputs.

Independent checks reconcile all 125 edition records (51 batch 1 + 74 batch 2), preserving every MAM/printed text pair byte for byte without normalization. The merged 93 rows retain the earlier 37/56 row membership and within-batch order; only the recorded Ezekiel 16:61 category/note changes at the merge. The later citation commit adds one paragraph to six rows, representing seven edition-record citations to six notes, and nothing else in those rows. Source-derived row membership, verse order, edition/category suffixes and option populations reconcile. All 369 local link/asset occurrences and fragments resolve; removed results-page/input references have no executable or generated-page consumer. Existing crop associations remain unchanged; no new pixel or original-scan verification is claimed.

The actual committed controls.js passes 4,116 search/category/batch combinations and 8,260 counted assertions using an offline DOM adapter, including intersecting filters, event listeners, image toggling independent of row visibility, size and reset. Four malformed-input probes refuse missing/unknown batches, missing batch 2 notes and batch overlap. The final disposable differential probe passes 2 tests. Three reviewer-harness errors were corrected with original scripts/logs retained: wrong batch for Ezek, its intended category attribute delta, and a raw-mirror extractor's numeric chapter key. An earlier citation extract included verses but omitted ordinary-page note cells; its incomplete output is retained alongside the strengthened exact public raw-verse and note-context evidence.

Public citations were checked against the committed [MAM-with-doc pages](https://github.com/bdenckla/MAM-basics/tree/efb3bd01cb3ed01f8f37d4e7cd6af59cb146734f/gh-pages/MAM-with-doc) and [raw mirror](https://github.com/bdenckla/MAM-basics/tree/efb3bd01cb3ed01f8f37d4e7cd6af59cb146734f/in/mam-ws). The notes support the attributed statements at their linked targets; no independent printed-source observation, judgment of all 74 note relevance decisions, or new interpretation of “Simanim” is claimed. The [generator](https://github.com/bdenckla/MAM-basics/blob/efb3bd01cb3ed01f8f37d4e7cd6af59cb146734f/py/author_site/stress_helper_comparison.py) and recorded editorial decisions were reviewed without reopening those decisions. Author-reported UTF8-off/twice regeneration, 29 tests and check_all remain attributed. No mega/full suite, browser/native Windows, external request, frozen research or font work ran.

Parent `0be304ef9005650463fdc5f3b71367b9789ebd6b`, every earlier status byte and finished receipt remain. Global reviewed-through stays `210affe3ac2931473bead0de839be0de08309e3d`; last broad-tested stays November 18 nightly source `8c2c3378487c9587659cd0b4a8f3db4690dbcf08`; historical windows, crops and source/browser/Windows/Taamey D limits remain distinct. Local slot/process/worktree admission was clear; cross-machine liveness is unverified. Exact isolated receipt parent and unchanged sole manual-dispatch workflow were checked. A CLI PR read returned Forbidden; no retry or mutation occurred. The coordinator's permitted connected GitHub search at 17:01:57 UTC found no open PR for this exact branch. No main/shared integration, deployment/dispatch, configuration or schedule changes. Remote byte/scope verification and owned-worktree/slot cleanup follow publication.
