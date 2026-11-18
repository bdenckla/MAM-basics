# Bounded MAM-basics hourly review, 2026-11-18 (UTC)

State: completed 2026-11-18; review only

Codex reviewed only `efb3bd01cb3ed01f8f37d4e7cd6af59cb146734f` -> `5b6a2ef44c579a08e1f092dbfd6ac4ad681707e8`: four reachable commits / seven paths.
No consequential introduced defect or product repair established. Public review material only;
no sibling input was required. Source and receipt checkouts were detached committed worktrees
using `/workspace/MAM-basics/.venv/bin/python` from the source repository root. Interactive
checkouts were preserved; current local slots/processes were clear before admission. Cross-machine
ownership was not independently verified; the coordinator admitted this sole executor.

Actual independent checks (full commands, exact exits, logs and helpers in the [evidence ZIP](review-hourly-2026-11-18-5b6a2ef4-basics-evidence.zip)):

| Check | Result |
| --- | --- |
| `git diff --check efb3bd01cb3ed01f8f37d4e7cd6af59cb146734f 5b6a2ef44c579a08e1f092dbfd6ac4ad681707e8` | exit 0 |
| Owning Python `-m black --check py/author_site/stress_helper_comparison.py` | 1 file unchanged, exit 0 |
| Owning Python `py/main_authored.py gen-site --trust-surveys` | exit 0, 5.764675 s, exact committed outputs |
| Owning Python `py/main_test.py py/tests/test_prose_conventions.py py/tests/test_prose_mark_order.py py/tests/test_shared_html_styles.py py/tests/test_site_links_relative.py py/tests/test_site_index_links.py -q` | 12 passed, no skips, 32.03 s, exit 0 |
| Independent public data/DOM probe | exit 0; 125 records, 93 rows (37/56), 369 local href/src occurrences and anchors resolve |
| Actual `controls.js` in offline Node DOM harness | exit 0; 8,232 filter/search combinations, 86 menu states, 27,817 assertions |
| Same harness with predecessor `controls.js` | intentional exit 1: stale 93 instead of 37 with Batch 1 selected |

Every maintained stage left clean status and an empty tracked diff. Independent grouping derives
menu populations from the public edition inputs and reconciles every rendered row. Forward and
reverse repeated transitions check each menu against the other menu, disabled zero choices,
forced empty intersections and recovery through All choices. Search changes rows/readout only;
menu labels/counts remain exact throughout. Image toggling and size/reset preserve row filters.
These are offline JavaScript checks, not browser/native-select verification.

Exactly one Koren record (Deut 5:6, appendix p. 39, עליון, batch 2) changes only its two Hebrew
text fields: the same pointed first atom is prepended, with a space on the MAM side and a maqaf
on the printed side. Both prior suffixes and every other record field remain byte-exact, without
normalization. Only those two spans change in one rendered row; all 93 rows keep order and
membership. The added atom occurs in the committed combined-cantillation public verse; no full
single-strand reproduction or original printed-source verification is inferred. The changed
[generator](https://github.com/bdenckla/MAM-basics/blob/5b6a2ef44c579a08e1f092dbfd6ac4ad681707e8/py/author_site/stress_helper_comparison.py),
[data](https://github.com/bdenckla/MAM-basics/blob/5b6a2ef44c579a08e1f092dbfd6ac4ad681707e8/in/stress-helpers/koren.json),
[controls](https://github.com/bdenckla/MAM-basics/blob/5b6a2ef44c579a08e1f092dbfd6ac4ad681707e8/gh-pages/stress-helpers/controls.js),
and [signs document](https://github.com/bdenckla/MAM-basics/blob/5b6a2ef44c579a08e1f092dbfd6ac4ad681707e8/doc/simanim-tanakh-signs.md)
are measured at this source, independently of the older receipt tree.

The first scratch probe incorrectly sought a complete selected-strand string in a combined
MAM page. Its failure, original script and public context are retained; the final check limits
that assertion to the added atom. That initial shell group returned 0 after its subsequent
display commands; the probe's exit was not separately captured. No product was changed.

The signs correction, original scan inspection, dagesh research and author-reported Node/tests/
check_all/Black/reproduction results remain attributed. The discrepancy already awaiting the
owner's decision between the current crop and summer transcription remains with that owner;
neither transcription nor its generated page was repaired or re-adjudicated. No original scans,
census/decision page, live source, browser, native Windows, broad mega/full suite/check_all,
frozen-study/font/baseline/hbofonts, deployment or configuration operation ran. The four
historical orphan crops were not rechecked and remain pending, not passing.

Parent `b8bbbf321fe3a39aeee81a86a46579e57e624cdc` and every earlier status byte/finished receipt remain unchanged.
Overall reviewed-through stays `210affe3ac2931473bead0de839be0de08309e3d`; broad-tested stays the
November 18 nightly source `8c2c3378487c9587659cd0b4a8f3db4690dbcf08`. All older gaps and
source/browser/Windows/Taamey D limits remain distinct. Source and parent have the identical sole
manual-dispatch Pages workflow. Publication is limited to the existing isolated receipt branch;
remote parent/scope/bytes and owned-worktree/slot cleanup are verified at closeout.
