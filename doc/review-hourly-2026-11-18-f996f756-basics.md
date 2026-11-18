# Bounded MAM-basics hourly review, 2026-11-18 (UTC)

State: completed 2026-11-18; review only

Codex reviewed only `5b6a2ef44c579a08e1f092dbfd6ac4ad681707e8` -> `f996f75630e19241d055215450165bd1da5fed80` (9 endpoint paths).
No consequential introduced defect or repair established. All source execution used the
owning home interpreter from an isolated committed worktree and its declared working root;
interactive homes were preserved. Local slots/processes were clear at admission; checks ran
sequentially, public before Private, with no known competing local owner. Cross-machine
ownership remains unverified. No sibling data input was required.

Full commands, exits, logs, decisive helpers and exact source blobs are in the
[evidence ZIP](review-hourly-2026-11-18-f996f756-basics-evidence.zip). Actual maintained-stage commands:

| Command | Result |
| --- | --- |
| `git diff --check 5b6a2ef44c579a08e1f092dbfd6ac4ad681707e8 f996f75630e19241d055215450165bd1da5fed80` | exit 0, 0.086348 s wall |
| `owning Python -m black --check py/accgram/printed_decalogue_koren_page.py` | exit 0, 0.299875 s wall |
| `owning Python py/main_authored.py gen-site --trust-surveys` | exit 0, 6.302052 s wall |
| `owning Python py/main_authored.py gen-israel-bible-review` | exit 0, 1.374482 s wall |
| `owning Python py/main_accgram.py generate-html-printed-decalogue-koren` | exit 0, 0.707835 s wall |
| `owning Python py/main_test.py (nine relevant modules) -q` | exit 0, 35.013032 s wall |

The selected nine modules were printed_decalogue_koren, printed_decalogue_simanim,
printed_decalogue_page, israel_bible_review_mam_forms, shared_html_styles, prose_conventions,
prose_mark_order, site_links_relative and site_index_links (`test_*.py` under py/tests).
Actual result: **25 passed, no skips, 34.72 s pytest / 35.013032 s wall**. All three affected
generators reproduced committed outputs exactly; every stage left an empty tracked diff.

Independent preservation check exits 0 (1.034198 s), 605 bounded assertions: all 125 edition
records retain their forms and other fields except three appended notes; all 93 stress rows
and their order remain, and the whole prior DOM is recovered after removing those notes.
The new links resolve at the existing Koren/Simanim conclusion IDs. The Israel Bible source
and HTML reconstruct exactly with only the two title reductions, preserving the quotation,
all Hebrew and abbreviation hover titles. The four Koren verdict rows retain their labels,
pages, strands and final two cells (ignoring wrapping), while five columns become three.
Only the one caption and verdict table differ; every other page byte and every Hebrew
sequence remains exact. Shared CSS selects the same cells in all eight Simanim verdict
rows; ruled-rows opts in only the Koren table in the wlc tree. All 413 local href/src
occurrences and applicable anchors resolve. This is technical consistency, not new source
or Decalogue research; editorial/source conclusions remain attributed. The separate Koren
transcription choice remains owner-pending and untouched.

Maintained offline HTML checker: Israel Bible exit 0 (0.122748 s); stress exit 1
(0.867832 s), the same four historical orphan crops; wlc exit 1 (1.300085 s), ten historical
orphan images and one XML file-type issue. All fifteen affected file blobs are unchanged
from base; the checker is unchanged and changed pages only add the three nonimage links.
No new HTML failure established. CSS notices (stress 275, wlc 142) are informational,
not a clean structural pass. Original logs and the corrected wrapping-assumption failure
are retained; no product was restored or repaired. No broad mega/suite/check_all,
browser/native Windows, original scans/source research, live requests, font/baseline or
frozen-study work ran. Author-reported 14/26/31 tests and other checks are attributed,
not added to these 25 independently executed tests. Public evidence is public-only.

Source references: [Koren generator](https://github.com/bdenckla/MAM-basics/blob/f996f75630e19241d055215450165bd1da5fed80/py/accgram/printed_decalogue_koren_page.py),
[shared CSS](https://github.com/bdenckla/MAM-basics/blob/f996f75630e19241d055215450165bd1da5fed80/gh-pages/wlc/style.css),
[Israel Bible source](https://github.com/bdenckla/MAM-basics/blob/f996f75630e19241d055215450165bd1da5fed80/in/israel-bible-review/review.md).

Parent `95e73ae0fd374d665ed22798df93fb16c79902c8` and every earlier status byte/finished receipt are preserved.
Overall reviewed-through remains `210affe3ac2931473bead0de839be0de08309e3d`; broad-tested remains November 18
nightly `8c2c3378487c9587659cd0b4a8f3db4690dbcf08`. All historical gaps and source/native/browser limits remain;
this bounded screen closes no unrelated interval. Only the established isolated receipt
branch is updated, with no main/shared integration, PR, deployment/dispatch or schedule
change. Deployment preflight: identical sole manual-dispatch Pages workflow;
exact-head open-PR search returned none. Remote exact-parent/scope/bytes and owned-worktree/
slot cleanup are verified at closeout.
