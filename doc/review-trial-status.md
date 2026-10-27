# MAM-basics review and testing trial status

State: live; continuing review/testing renewed 2026-10-16

Policy: [review-trial.md](review-trial.md). One confirmed automation, `Review MAM changes`,
scheduled seven daily runs on 2026-10-08 through 2026-10-14, around 2 a.m. America/New_York.
That closed trial remains historical. Ben renewed the work on 2026-10-16; the coordinating
session confirmed enabled hourly new-main screening from October 16 at 13:00 and daily broad
checks around 02:00 from October 17, America/New_York, with no end date. Scheduling remains
with that session; this run created no automation.

| Anchor | Commit/result |
| --- | --- |
| Adopted baseline | `d66a3faf1403e945a0f41e5d25c86c3ac72b871f` |
| Reviewed through | `9302ad04b347aa2db3ee0004962cd66202031cce`; stress-helper parameter selection and near-Aleppo isolation reviewed from `629218d2f44c006f36eeb0dcb16e8eacdd052a41`; no consequential implementation defect or repair. |
| Last tested | `9302ad04b347aa2db3ee0004962cd66202031cce`; October 27 cloud nightly: mega exit 0 in 495.494 s, all 61 steps/no skips; full suite exit 0 in 333.300 s: 1100 passed, 5 skipped, 82 subtests passed in 329.93s (0:05:29); eight explained SVG differences preserved and reversed. [Compact receipt](review-nightly-2026-10-27.json) |
| Last focused checked | `9302ad04b347aa2db3ee0004962cd66202031cce`; 4 independent checks and the parent oracle pass, zero skips; three-book MAM-with-doc regeneration and all 106 near-Aleppo files reproduce. Corrected scratch HTML assumption and stopped diagnostic are retained. [Receipt](review-hourly-2026-10-27-stress-helper.json). Broad-tested anchor unchanged. |
| Pending focused review | `9302ad04b347aa2db3ee0004962cd66202031cce` through `46f80ecc8b29fdd7f5fdf30c40bc2b3382bbb352`; source inspection, independent raw census/row pairs, archive provenance hashes and formatting pass. Generators/shared-renderer checks not started under the parent HP overlap restriction. [Partial receipt](review-hourly-2026-10-27-dehi-font-partial.json). |

Run from an isolated repository root with its home clone's interpreter: `py/main_0_mega.py`,
then `py/main_test.py`. Use each required private sibling's recorded committed checkout;
do not copy private evidence into this note. Explain tracked generator diffs and record
failures/incomplete checks before updating the anchors. Detailed repair evidence may live in
the repair commit; a passing suite or no-diff mega is not proof of the underlying interpretation.

| Run/repair | Frozen commit and allowed input IDs | Result, disposition and evidence |
| --- | --- | --- |
| Setup, 2026-10-07 | Adopted baseline above | No retrospective review or broad-check run; procedure integrated and seven-night schedule confirmed |
| Run 1, 2026-10-08 | `275ed4683a6b71b4cba33f99c0ed57740e92c292`; no runtime sibling inputs selected | Blocked before execution: shell setup returned `helper_unknown_error: setup refresh had errors` twice, including a minimal clock read. HP process inventory, isolated checkout and home-environment verification were unavailable; mega and suite were not started, so there are no test durations or results. GitHub endpoint inventory found 61 incoming commits; full code/data review remains incomplete. Reviewed-through and last-tested anchors stay unchanged. |
| Run 1 cloud continuation, 2026-10-08 | `f9d817b1d292babf1ed742cba32b6cd183f6d4c7`; committed input `dc4bcd276938a40b72d8a7694466358c4f89c0a4` | Reviewed the new endpoint from the adopted baseline, including the 61 incoming commits and the HP receipt. No consequential defect confirmed; retired seals and source-hash movement were not treated as defects. Mega exit 0 in 489.001 s; suite exit 0 in 296.792 s: 1,047 passed, five documented edition-transcription skips, 82 subtests passed. Data, HTML and font outputs reproduced. Eight SVGs differ only in Graphviz font metrics/layout and the Times font-family alias; their titles, labels and links agree. These diffs are retained in the isolated checkout, without committing regenerated products. Receipt stays on an isolated branch; no main push or deployment. |
| Run 2, 2026-10-09 | `2265bf9cde517502571b6f848c950c3c0394feaa`; committed input `e9d0f95e1b16603efb6d4f18b164766bcf3d2ece` | Reviewed 24 incoming commits from `f9d817b1d292babf1ed742cba32b6cd183f6d4c7`. Mega exit 0 in 473.746 s; suite exit 0 in 290.058 s: 1048 passed, 5 skipped, 82 subtests passed in 287.42s (0:04:47). Data and HTML reproduce; eight SVGs differ only in coordinates/dimensions and the Times alias, with every other XML element, attribute, title, label and link equal. No consequential defect confirmed or repair made. Run 1's completed cloud anchors were reconciled from its isolated receipt branch; this receipt stays isolated too. |
| Run 3, 2026-10-10 | `3982871623dab43c84f163f5090d1d24a894d4ff`; committed input `0825f8041dbf1b87afdbd4fb26642f49722a627c` | Reviewed eight new main commits from `2265bf9cde517502571b6f848c950c3c0394feaa`. Mega exit 0 in 468.431 s; suite exit 0 in 296.897 s: 1048 passed, 5 skipped, 82 subtests passed in 294.45s (0:04:54). All 60 steps ran. Data and HTML reproduce; eight SVG differences were freshly verified as geometry/Times-alias only, with all other XML equal, and retained unstaged. No new consequential defect or repair. Run-2 anchors recovered from isolated receipt `2cb41b92ec0cc0b8d4aa67ac9ffff5a38ac3676a` without merging it; this receipt stays isolated. |
| Run 4, 2026-10-11 | `6d50cea430aa44d059ac45e12d778af1ba5d0a60`; committed input `0825f8041dbf1b87afdbd4fb26642f49722a627c` | Reviewed the one new main commit from `3982871623dab43c84f163f5090d1d24a894d4ff`: the maintained plan correctly retains item 36.8 as MAM-basics #303; the complete issue and comments were read through the GitHub connector. Mega exit 0 in 780.234 s, all 60 steps; suite exit 0 in 442.783 s: 1048 passed, 5 skipped, 82 subtests passed in 440.26s (0:07:20). Data and HTML reproduce. Eight SVG diffs are freshly verified as geometry/Times-alias only, with every other XML element, attribute, text and link equal; preserved unstaged. No defect, repair, decision PR or new issue. Run-3 anchors reconciled from isolated receipt `aa6c90a49f28dfef2a3f56d1a8c85e1ca68b1abd`; this receipt stays isolated. |
| Run 5, 2026-10-12 | `6168259fa913cfc74358972c16ecc7fdb97350f1`; committed allowed inputs `8b8b6af548a1d0016baa7d1ad991801707d66c23` and `853682c32f69dc5dfd90091fd6743f8f3bc00e56` | Reviewed the endpoint from `6d50cea430aa44d059ac45e12d778af1ba5d0a60` (110 reachable incoming commits, 215 changed paths). Independent 24-book comparison agrees with approved changes and current qere/body records. Windows mega exit 0 in 466.070 s, all 60 steps and zero tracked output diffs, including the former eight SVGs. Suite exit 1 in 276.356 s: 1072 passed, 5 documented skips, one missing canonical receipt-pointer failure. Fixed in `3a46a5b138be5b0535c3de99384a9ccce08966c5` under existing policy; decisive lint exit 0 in 0.518 s (1 passed). No new all-green full rerun claimed. [Compact receipt](review-trial-run5-2026-10-12.json). |
| Run 6, 2026-10-13 | `d921ed3565fb3e6cba8b9d46104e92a488b8df12`; allowed committed input IDs `b65627f15d1fc70f755783b6bcd4ae8b97be74a1` and `384682ab4ef5c64106735af5789a86573c5c0e51` (font receipt checkout; source main remains `853682c32f69dc5dfd90091fd6743f8f3bc00e56`) | Reviewed 72 reachable commits / 347 paths from `3a46a5b138be5b0535c3de99384a9ccce08966c5`. Windows mega exit 0 in 560.244 s, all 60 steps, zero tracked output diffs. Suite exit 1 in 340.588 s: 1079 passed, 5 documented skips, one differential test still passing XML to the JSON-only OSIS caller. Test-only repair `52f73420395ce9416b9928a957cde9287c273843` retains the independent assertions; focused module exit 0 in 0.475 s, 3 passed. No all-green full rerun claimed. [Compact receipt](review-trial-run6-2026-10-13.json). |
| Run 7 scheduled attempt and final continuation, 2026-10-14 | Frozen source `f3e4fdf824bc8ac45f21f4460e94d1bf25ce942c`; allowed committed input IDs `3d45d8a396b0eadc062116403f143adc0cb5adbf` and `4159205f3765a10ba8df7ec75a1d25dbca82ac54` (font receipt checkout; source main `853682c32f69dc5dfd90091fd6743f8f3bc00e56`) | Scheduled attempt blocked before child creation (HP offline; saved runner startup failed twice with generic ASB error), advancing no checks or anchors. Later authorized HP continuation reviewed `52f73420395ce9416b9928a957cde9287c273843` → `f3e4fdf824bc8ac45f21f4460e94d1bf25ce942c` (64 commits/300 paths). Maintained mega exit 0 in 549.692 s, all 60 steps and zero generated differences; suite exit 0 in 383.274 s: 1086 passed, 5 skipped in 381.44s (0:06:21). No new consequential defect or nightly repair. Owner changes retain their attribution. |
| Continuing catch-up, 2026-10-16 | Frozen source `8bc42598e67b5a525d08b78eedea54b5b10ab119`; allowed committed inputs `6fe3502687f1e8c60931575c31905956f4dafb24` and `853682c32f69dc5dfd90091fd6743f8f3bc00e56` | Saved cloud mega exit 0 in 490.925 s; all 60 steps and SVG renders ran. Eight SVGs differ only in geometry/known Times alias, all other XML content equal. Suite exit 1 in 344.051 s: 1085 passed, 2 lint failures, 5 established skips, 82 subtests passed. Repair `acbb568b23c32708073d7ec7b9fd42e5350d80fe` records the existing manual-research exclusion, removes redundant package guards, and preserves literal quotation order within the prose lint; five decisive lint checks pass in 1.31 s, six NFC checks in 25.30 s. A corrupted duplicate citation block was removed without changing the proposal. Review/history-inventory CLI outputs reproduce. [Compact receipt](review-continuing-2026-10-16.json). |
| Nightly, 2026-10-17 | `b82fe2374923e86b857a6d6ff0ca560d74789045`; allowed committed inputs `2507cdca31640043f7063392725d1491acf80f8b` and `853682c32f69dc5dfd90091fd6743f8f3bc00e56` | Mega exit 0 in 468.032 s, all 60 steps; full suite exit 0 in 312.451 s: 1087 passed, 5 established skips, 82 subtests passed. Prior repair `acbb568b23c32708073d7ec7b9fd42e5350d80fe` is included; the earlier lint failures no longer reproduce. Eight SVG geometry/Times-alias differences and two change-log tree-ID-only differences freshly verified; complete patches preserved privately. No new defect or repair. [Compact receipt](https://github.com/bdenckla/MAM-basics/blob/1e2bbaf8eccadae4ce9f3cdee695c7f92d225535/doc/review-nightly-2026-10-17.json). Isolated receipt branch only; no main integration or deployment. |
| Nightly, 2026-10-18 | `80dd9f04e56ae705981749ba9fbafb7fb243c3de`; allowed committed inputs `3c7a60e9cfd7f670a35b3ea4dbfc2179367ef4aa` and `853682c32f69dc5dfd90091fd6743f8f3bc00e56` | Mega exit 0 in 459.423 s, 60 steps; full suite exit 0 in 300.922 s: 1087 passed, 5 established skips, 82 subtests passed. Eight SVG layout differences and two change-log provenance differences verified and preserved privately. Focused review reproduces 152 cases / 718 literal passages / 14 proposed quotations. Four stale history-inventory context fields synchronized with two existing Ben decisions in `339dbb3b95b690bf42f915360b57f9393791448d`; focused rebuild reproduces, no history routing or source-data change. Reconciled prior receipt `1e2bbaf8eccadae4ce9f3cdee695c7f92d225535`; pending hourly receipt work remains accounted for by this endpoint review. [Compact receipt](https://github.com/bdenckla/MAM-basics/blob/6480c7c452071f4847b5b1b29741d06f09ef803a/doc/review-nightly-2026-10-18.json). Isolated branch only; no main push or deployment. |
| Nightly, 2026-10-19 | `2716f6333613cd680b7c9054f2307e88cb0eff23`; allowed committed inputs `3c7a60e9cfd7f670a35b3ea4dbfc2179367ef4aa` and `853682c32f69dc5dfd90091fd6743f8f3bc00e56` | Mega exit 0 in 492.840 s, all 60 steps; full suite exit 0 in 325.203 s: 1087 passed, 5 established skips, 82 subtests passed. Eight SVG layout and two change-log provenance differences verified and preserved privately. Offline reconstruction confirms six template replacements and all 13 mirror page sizes; focused research review reproduces. No new defect or repair; the October 18 inventory-context repair remains separate and unmerged. [Compact receipt](https://github.com/bdenckla/MAM-basics/blob/c27501150f4ce9bc3fb6d8e7ca18e0a79f1b77b3/doc/review-nightly-2026-10-19.json). Isolated branch only; no main push or deployment. |
| Nightly, 2026-10-20 | `040dbfb3dfb0dcb37ce2e439b9402207fdc8a9c5`; allowed committed inputs `91d800de422d71deaa6ef28f05b4193223ca9e61`, `853682c32f69dc5dfd90091fd6743f8f3bc00e56` | Mega exit 0 in 479.191 s, 60 steps; suite exit 0 in 332.349 s: 1099 passed, 5 skipped, 82 subtests passed in 329.42s (0:05:29). Eight SVG layout/Times-alias and two provenance-only differences independently verified and preserved privately. Reviewed ten commits / 11 paths; offline downloader/report probes pass. No new consequential defect or repair. [Compact receipt](https://github.com/bdenckla/MAM-basics/blob/2560261b137a357189718fb8301e1d745a5b8763/doc/review-nightly-2026-10-20.json). Isolated branch only; no main integration or deployment. |
| Nightly, 2026-10-21 | `eecb2e8abf54fd9aee90d8455073a8f69b93f0bc` | Reconciled the completed isolated nightly: mega 60 steps; suite 1099 passed, 5 skipped, 82 subtests passed. [Exact execution receipt](https://github.com/bdenckla/MAM-basics/blob/aa79651c8e5beda011e6c834fad346f4aa8b6e3f/doc/review-nightly-2026-10-21.json). No duplicate broad run. |
| Hourly review, 2026-10-21 | `eecb2e8abf54fd9aee90d8455073a8f69b93f0bc` → `75de03e816162c6e5f7005eb85b36a5024c09cce` | Reviewed 16 commits/100 paths. Reproduced placeholder/inline-ketiv ownership errors in numbered_atoms and repaired them in isolated `062da1e80a1e725b1dd176a9b9d3e9c18a1b6076` with differential role/guard coverage. Maintained source checks: 51 pass; repaired probes/regression: 32 pass. All 59 corpus JSON changes are notice-only. No current change record targets corrected metadata; no report-total or manuscript correction asserted. [Compact receipt](https://github.com/bdenckla/MAM-basics/blob/8b51464f1139b09e24327e56f708ca008310e516/doc/review-hourly-2026-10-21-75de03e8.json). No main integration or deployment. |
| Focused review and portability repair, 2026-10-20 | Reviewed `d27594238139e75d507b2b2a921de1707946c3d1` from `a9db1ad3b30a5d8da411457b9d93457554b2384c`; repair `44a457c513795920b5d350ef27074fc1acca919a` | Owner receipt `a14f499d3ddd6ca7f660fdd7180eb8c2895d255b` reports mega pass on `b643e9796e326e553a5d0aa7af3f50bfe462d6c0`, with suite 1089 passed, ten Windows-invalid-filename failures and five skips. Linux source control: 12 citation tests pass; repaired focused modules: 36 passed. Actual filename-selection checks retain POSIX tab coverage and select Windows-safe names; no native Windows rerun is claimed. Algorithmic generated deltas are explained with source text unchanged; the 2 Kings 5:18 joining convention stays provisional. No broad rerun or main integration. [Compact receipt](review-citation-portability-2026-10-20.json). |
| Hourly connector review, 2026-10-21 19:09 UTC | `75de03e816162c6e5f7005eb85b36a5024c09cce` → `69fcfc87a8aa348dd1382e8d73baccfaf3e315a5` | Reviewed the [17-commit/47-path endpoint](https://github.com/bdenckla/MAM-basics/compare/75de03e816162c6e5f7005eb85b36a5024c09cce...69fcfc87a8aa348dd1382e8d73baccfaf3e315a5): separator preservation, closed readers, positional gray-maqaf operations and poetic pairing. Independent JSON comparison preserves all 3,905 note records and source/evidence fields; only their projection notices and 362 space-only target projections change. Other generated deltas are 11 explicit-xataf mappings, two prose-fragment spaces and token counts 53157/807 → 53156/808. No new consequential defect. This review ran no tests or generators; broad-tested and focused-checked anchors remain unchanged. The owner's [separate receipt](https://github.com/bdenckla/MAM-basics/commit/69fcfc87a8aa348dd1382e8d73baccfaf3e315a5) reports all 60 mega steps, no tracked changes and 1099 passed/5 skipped on `ceb9c1977343fecd74eee0d8fb0202ad45b36f92`; both commits were verified to share tree `0f3dc6af53c66b376c0394f82418494750525803`, but these checks were not rerun here. Prior repair remains pending and its code is not included. Isolated receipt only; no main integration or deployment. |
| Hourly connector review, 2026-10-21 16:45, New York time (20:45 UTC) | `69fcfc87a8aa348dd1382e8d73baccfaf3e315a5` → `838b1d6b49f33ac988b677227793896c9af5337c` | Reviewed the [three-commit/one-path endpoint](https://github.com/bdenckla/MAM-basics/compare/69fcfc87a8aa348dd1382e8d73baccfaf3e315a5...838b1d6b49f33ac988b677227793896c9af5337c): approved canonical Hebrew prose terminology guidance only, with quotation and technical-identifier exceptions preserved. No executable, source-data or generated-product change and no new consequential defect. Reconciled the preceding isolated receipt without repeating its review. No tests, generators or installed-skill synchronization ran in this screening; broad-tested and focused-checked anchors stay unchanged. The only workflow has scheduled/manual triggers, not push triggers. Isolated receipt only; no main integration, deployment or checker-repair integration. |
| Nightly, 2026-10-22 | `838b1d6b49f33ac988b677227793896c9af5337c`; allowed committed inputs `b58ea672854a0ee563c9fdbd64afe93859ec2cc9`, `853682c32f69dc5dfd90091fd6743f8f3bc00e56` | Mega exit 0 in 820.510 s, all 60 steps and no skips; suite exit 0 in 534.653 s: 1099 passed, 5 skipped, 82 subtests passed in 531.73s (0:08:51). Eight SVG geometry/Times-alias differences freshly verified and preserved privately; all other generated content reproduces. Reconciled the latest isolated review receipt without duplicating its review. Prior checker repair remains pending. [Compact receipt](https://github.com/bdenckla/MAM-basics/blob/75d973ed36cbac0e6df81f33b5a5a960a2814fe7/doc/review-nightly-2026-10-22.json). Isolated branch only; no main integration or deployment. |
| Hourly connector review, 2026-10-22 12:26, New York time (16:26 UTC) | `838b1d6b49f33ac988b677227793896c9af5337c` → `d6d96d936d2556bfc6ded87efd62876af5e88d35` | Reviewed the [one-commit/four-path endpoint](https://github.com/bdenckla/MAM-basics/compare/838b1d6b49f33ac988b677227793896c9af5337c...d6d96d936d2556bfc6ded87efd62876af5e88d35): the daily Pages schedule is removed, with only manual `workflow_dispatch` retained. Matching instruction prose, docstrings and an assertion message change; no executable Python, source input or generated product changes. No new consequential defect. The [owner commit](https://github.com/bdenckla/MAM-basics/commit/d6d96d936d2556bfc6ded87efd62876af5e88d35) reports Black, whitespace checks and 18 focused tests; those checks were not rerun here. This connector review ran no tests or generators, and broad-tested and focused-checked anchors remain unchanged. Reconciled the completed October 22 nightly without repeating it. Prior checker repair remains isolated. Receipt branch only; no main integration, workflow dispatch or deployment. |
| Hourly connector review, 2026-10-22 13:32, New York time (17:32 UTC) | `d6d96d936d2556bfc6ded87efd62876af5e88d35` → `27f263cb6a158566ec290a67123364f6b690106b` | Reviewed the [one-commit/one-path endpoint](https://github.com/bdenckla/MAM-basics/compare/d6d96d936d2556bfc6ded87efd62876af5e88d35...27f263cb6a158566ec290a67123364f6b690106b): procedure wording preserves hbofonts receipt isolation until its manual-only deployment change reaches main. No code, workflow, input or generated-product change and no new consequential defect. The [owner commit](https://github.com/bdenckla/MAM-basics/commit/27f263cb6a158566ec290a67123364f6b690106b) reports 16 focused tests; not rerun here. This connector screen ran no tests or generators. Broad-tested and focused-checked anchors and the prior pending repair remain unchanged. Isolated receipt only; no main integration, dispatch or deployment. |
| Nightly, 2026-10-23 | `27f263cb6a158566ec290a67123364f6b690106b`; allowed committed inputs `b58ea672854a0ee563c9fdbd64afe93859ec2cc9`, `56f4ba837f70c9a6a7a3ad4692c49e5d09c98eec` | New nightly run: mega exit 0, all 60 steps/no skips (793.101 s); full suite exit 0 (476.176 s): 1099 passed, 5 existing edition-transcription skips, 82 subtests passed. Eight SVG geometry/Times-alias differences freshly verified and preserved privately; all other content reproduces. Suite ran on the clean frozen tree after verified reverse apply. Latest isolated receipt reconciled; no repeated review window, repair integration or main advance. [Compact receipt](https://github.com/bdenckla/MAM-basics/blob/180806349a53ed865cc598a3bbea532e11e65274/doc/review-nightly-2026-10-23.json). Isolated branch only; no deployment or schedule operation. |
| Hourly connector review, 2026-10-23 22:19 UTC | `27f263cb6a158566ec290a67123364f6b690106b` → `cda80a1cb5b49f709c13f3ad332eca68992e02ef` | Reconciled [October 23 nightly receipt](https://github.com/bdenckla/MAM-basics/blob/180806349a53ed865cc598a3bbea532e11e65274/doc/review-trial-status.md). Two reachable commits, including a merge, change only the same quoted article from “the trace” to “a trace” in `py/author_boj_qr/qr_05.py`, `book-of-job/out/enriched-quirkrecs.json` and `gh-pages/book-of-job/jobn-details/0505.html`. Source wording and all three endpoint patches agree; no Hebrew, interpretation, executable logic, workflow or policy change. Owner-reported focused generation is attributed evidence, not rerun here. No executor or tests ran: this bounded prose correction and matching generated copies need no deeper review. Reviewed-through advances; broad/focused-tested anchors and prior repair disposition stay unchanged. Isolated receipt branch only; no main integration, workflow dispatch or deployment. |

Run 1's cloud commands ran sequentially from
`/workspace/review-trial-run1-20261008/MAM-basics`, with its home interpreter:

```text
/workspace/MAM-basics/.venv/bin/python py/main_0_mega.py
/workspace/MAM-basics/.venv/bin/python py/main_test.py -q -ra
```

The maintained suite checked the near-Aleppo dataset, note review and punctuation extract;
no additional replay or sealing check was introduced. Graphviz was the pinned
`16.0.0 (20260814.1018)`. Browser verification of ruby alignment was not performed.

Run 2 used the existing clean saved cloud checkout `/workspace/MAM-basics` on the isolated
`review-trial-run2-20261009` branch and its own `.venv/bin/python`, with the two maintained
commands above run sequentially (`py/main_test.py -q -ra`). All 60 mega steps ran; no cloud
step or SVG render was skipped. A transient transport disconnect left the original mega
running; its recorder confirmed completion, so no expensive check was restarted. The eight
SVG diffs remain unstaged, with private supporting evidence. Current browser appearance
was not verified. Run 2 does not integrate either pending basics branch or change scheduling.
Run 1's original cloud receipt is preserved at
[its exact commit](https://github.com/bdenckla/MAM-basics/blob/f12dbaca5e09d4d0eccc2dfacfec02cfb8d2f3ed/doc/review-trial-status.md).

Run 3 used the saved clean isolated checkout `/workspace/MAM-basics` at the commit above,
with its own Python 3.13.15 environment. Sequential commands were `.venv/bin/python
py/main_0_mega.py` and `.venv/bin/python py/main_test.py -q -ra`. No mega step or SVG render
was skipped. Graphviz matched `16.0.0 (20260814.1018)`. Generated SVGs remain local and
unstaged; no generated products were committed. The suite checked maintained near-Aleppo
acceptance without restoring retired seals. No pending branch was integrated or schedule
extended. Browser appearance was not verified.

Run 4 used the saved clean `/workspace/MAM-basics` checkout on the isolated
`review-trial-run4-20261011` branch and its own Python 3.13.15 environment. Commands ran
sequentially: `.venv/bin/python py/main_0_mega.py`, then `.venv/bin/python py/main_test.py
-q -ra`. The required sibling stayed committed at the input above throughout both commands.
HP had already failed before process creation and was not retried; cloud job inventory
found no expensive ongoing work. No step or SVG render was skipped. Graphviz matched its
full pin. Generated SVGs remain local and unstaged, with private comparison evidence.
Browser appearance was not verified. No pending branch was integrated, main pushed or
schedule extended.

## Evidence integration, 2026-10-12

Ben's separate authorization consolidated the latest authoritative status on main.
Earlier isolation and no-main-push statements describe each nightly execution stage.
Historical failures and the actual reviewed/tested run-4 anchors remain unchanged.
The [integration receipt](branch-integration-2026-10-11.md) records standalone implementation
verification; it is not a fifth nightly run and does not alter the seven-night schedule.

After night seven, record the compact assessment of Ben's time, meaningful defects,
unnecessary changes and adequacy of evidence here.

Run 5's single HP shell preflight succeeded. Existing constrained Python 3.13.15 environments and pinned Graphviz 16.0.0 were verified; expensive commands ran sequentially in isolated committed checkouts. The canonical worker helper's normal native Windows memory/CPU API path and bounded counts now pass a direct probe; forced shortage, affinity and API-failure cases remain untested. Ordinary repair/record consolidation starts no deployment workflow, and the home working checkouts stay unchanged. No new manuscript interpretation, browser appearance proof, product publication or trial extension is claimed.

Run 6 preserves the deliberate JSON-only MAM-simple representation and XML OSIS output. The repaired test uses the current JSON caller without changing production projections or the independent oracle. Original suite failure remains recorded. HBCE has owner token/tag evidence but no full comparison/output regeneration in this run. No browser, manuscript or pronunciation judgment, private evidence disclosure, deployment or schedule extension; night seven remains 2026-10-14.

Final continuation completes the previously unfinished check after the seventh scheduled attempt failed; it does not make that scheduled attempt successful. The assessment after six executed nights remains dated evidence: three test/documentation upkeep fixes, no newly confirmed product/data defect and no measured Ben-time savings. The final review adds no trial-origin repair. Owner reconciliation and manuscript-index repairs are owner work; reproducibility and passing checks remain limited evidence of editorial correctness. Existing receipts above retain the original failures and decisive rechecks. Ben approved main integration of the process update and final receipts on 2026-10-14; the [existing process document](review-trial.md) states the intended workflow. No schedule renewed or extended, private evidence disclosed, browser/manuscript/pronunciation adjudication, or deployment performed by this continuation.

Post-freeze inventory: main advanced during execution to `aa505ff7f14ed3a6d5028a9dfa1c3c6ea1fe9490`, four further owner commits covering expanded typography/family counts and approved plural defaults. Those changes and their owner-focused evidence are outside the completed frozen review/test window above. The checked source remains `f3e4fdf824bc8ac45f21f4460e94d1bf25ce942c`; no result or anchor is advanced by that later remote observation.

Approved integration, 2026-10-14: process documentation and this status note are merged over owner main `6fdb1ee044b9671bb0fb4d7c606d119c07b1eb16`. The integration changes only these two documentation files relative to that owner tip. Reviewed/tested source remains `f3e4fdf824bc8ac45f21f4460e94d1bf25ce942c`; later owner commits were not broadly retested. Focused prose/Unicode checks and link/anchor checks validate the documentation integration. The active owner checkout is preserved. No renewed schedule or deployment is authorized by this merge; hbofonts remains branch-only.

Continuing execution, 2026-10-16: the saved cloud forest and owning constrained Python
3.13.15 environment were verified before the sequential mega/suite commands. Graphviz
matched its full pin; no cloud step or SVG render was skipped. Isolated committed input
checkouts excluded regenerated files. No personal computer was needed. Generated differences
are retained as complete patches in their owning private evidence; no product was accepted.
The failed full suite remains the original result; decisive focused checks establish the
verification repair. No manuscript, translation or browser judgment is inferred.

Post-freeze inventory, 2026-10-16: main reached
`ef2113632c82c5546ae8f4e07a190f7ec235d381` while this run executed. Its three additional
commits include the separately authorized index-label and issue-policy branches. Those
changes were not broadly tested by this run; the pending window starts after
`8bc42598e67b5a525d08b78eedea54b5b10ab119`. Receipt integration does not advance that
frozen review/test boundary. The October 16 renewal preserves all original trial history
and substantive repair authority; this run created no duplicate schedule or deployment.

Receipt integration, 2026-10-16: reconciled the already integrated owner main
`ef2113632c82c5546ae8f4e07a190f7ec235d381` in
`007fe0de0f4a38f60983cf845bb0dde3068bbe2d`, without integrating either owner branch a
second time. The combined coverage/prose mark-order checks pass after reconciliation
(five tests in 1.10 s). Documentation and source changes remain separate from the
frozen broad results; no all-green full-suite rerun or later tested anchor is claimed.
The receipt push uses the existing main workflow, with no direct deployment or dispatch.

Hourly screening, 2026-10-16 13:24, New York time: read-only endpoint review from
`8bc42598e67b5a525d08b78eedea54b5b10ab119` through
`3b8b2aea66e72cdf14bca18f809b9e5c38e57605` covers seven commits and 13 paths.
The already authorized homepage labels preserve their destinations and match the generated
page; the issue policy, focused verification repair and catch-up records are consistent with
their maintained authorities. Removed package guards retain the canonical dispatcher; literal
quotation exemptions match the research runbook. No new consequential defect or repair.
No checks ran during this screening; last-tested and all prior failures/results stay unchanged.
Broad checks remain nightly; this text-only receipt does not advance review to its own commit.

Hourly screening, 2026-10-16 14:49, New York time: reconciled the preceding receipt and
reviewed seven new owner commits (21 paths) from
`74a2e907a65d00b82d66f4efe84e281a9f8320e6` through
`049e3aabd558ec776bef009fef8ccefc72656021`. Yeivin source spacing changes match their
rendered differences; the mirror whitespace exemption is limited to verbatim MediaWiki files,
and the skill landing-page correction matches the existing location. The settled decision
record and crop provenance change documentation/comments, with no near-Aleppo dataset or
reading-table change. Owner-focused regeneration/check evidence remains attributed to those
commits; this screening ran no tests and did not independently adjudicate the manuscript image.
No new consequential defect or repair. Last-tested stays unchanged; broad checks remain nightly.

Hourly screening, 2026-10-16 18:29, New York time: reconciled the preceding receipt and
reviewed `39a1146d4cb02cfd9648f9ef7c054a92f8efbdc8` through
`740daaa2af3472441437005769d67cbf21250141`. The two notice generators and three HTML
notices reflect Ben's approved ketiv/qere display policy. All 83 JSON patches contain only
notice-text changes, in three identical groups of 24, 35 and 24 files; Scripture payloads
are unchanged. The focused regeneration, 59 claim checks and 16 tests are owner-reported
commit evidence, not rerun by this screening. No new consequential defect or repair;
last-tested stays unchanged and broad checks remain nightly.

Compact receipt integration, 2026-10-20: Ben approved updating this maintained note where
a main push has no deployment trigger. The October 17–20 rows retain their original isolated
execution-stage publication statements; their dated structured receipts remain unchanged at
the immutable commits linked above. Only this maintained note is integrated here. Tested and
reviewed source anchors, sibling inputs, failures and skips remain those actually recorded;
this documentation commit advances none of them. No mega or full suite is repeated for this
integration; focused receipt, anchor and link checks apply. No workflow is dispatched.

Citation portability verification and approved integration, 2026-10-20: the coordinating
session verified native Windows results for exact commit
`c9bde2e515aca8efbf288c6725489100e06e1970`: all 12 citation tests passed, including
the ten previously failing parametrizations, with CPython 3.13.15, pytest 9.1.1 and Windows 11
build 26300. The [single structured receipt update](review-citation-portability-2026-10-20-update.json)
records the later result; the base receipt retains its original Linux-only state and now
links that update. Ben approved integrating the narrow test repair and its receipt into main.
No full suite or mega is repeated, no broad-tested anchor is advanced, and the owner
receipt's ten full-suite failures and five skips remain historical results. The integration
adds no FOI or other branch, production change, generated output or workflow change. Pages
has no push trigger; no workflow is dispatched.

Nightly attempt, 2026-10-24: reconciled isolated receipt `23e370cc2e9af2463f34a088ea52e05c62f71220` and the
preceding nightly receipt `180806349a53ed865cc598a3bbea532e11e65274`. Current main remains
`cda80a1cb5b49f709c13f3ad332eca68992e02ef`, already reviewed. The selected saved runner never became usable;
both minimal shell attempts returned "No usable execution environment is available."
All 2 prescribed broad stages are unstarted, with no exit code, duration, fresh output
comparison or tested-anchor advance. [Compact blocked receipt](review-nightly-2026-10-24.json).
No test process or temporary checkout was created; existing live-process inventory was unavailable.
Main integration, interactive HP work, baseline acceptance, frozen-font work and deployment did not occur.

HP recovery, 2026-10-24: mega exit 0, 60 steps/no skips in 870.820 s, zero tracked output differences; suite exit 0 in 590.685 s: 1099 passed, 5 skipped, 82 subtests passed in 588.06s (0:09:48). The original blocked startup entry and JSON remain unchanged. Exact current main and committed sibling inputs are recorded in the [HP recovery receipt](review-nightly-2026-10-24-hp-recovery.json). Generated differences were preserved and independently inspected; no product or baseline was accepted. No new repair, main integration or deployment.

Hourly connector screening, 2026-10-24 20:09, New York time (2026-10-25 00:09 UTC):
reconciled completed HP receipt [`c8b6ce67`](https://github.com/bdenckla/MAM-basics/commit/c8b6ce6719de119fd430a6b9d98e36e7477a27c1)
without repeating its checks or earlier windows. Reviewed the [one-commit/three-path endpoint](https://github.com/bdenckla/MAM-basics/compare/cda80a1cb5b49f709c13f3ad332eca68992e02ef...0f66512aa92d32f7de463b9aad82b8c2edec9462).
The two Python changes isolate SLH prose in a `lang=he`, RTL cell, keeping compact text
in its `lang=hbo` cell; the generated SLH page reflects that split. The description producer
supplies the singleton string and terminal parenthesized explanation required by the splitter.
The JSON serialization path, non-SLH table construction, qualifiers and render attributes are
unchanged. No consequential defect or repair; classification is reviewed/screened, not broadly tested.
The [owner commit](https://github.com/bdenckla/MAM-basics/commit/0f66512aa92d32f7de463b9aad82b8c2edec9462)
records Black/whitespace checks, focused regeneration, five style/prose tests, unchanged generic
FOI output, all 159 displayed rows/parsed-page comparison and computed-style/render inspection.
Those executed checks were not rerun here. This screening ran no tests or generators; the
broad-tested anchor remains `cda80a1cb5b49f709c13f3ad332eca68992e02ef`, with the original blocked
attempt and later HP result preserved. This receipt branches from the latest isolated receipt,
not from the reviewed source: its checkout is evidence, not a new tested source. No main/shared
branch change, deployment, editorial change, baseline acceptance or frozen-font regeneration.

Hourly connector screening, 2026-10-24 23:48, New York time (2026-10-25 03:48 UTC):
reconciled isolated receipt [`5eeec102`](https://github.com/bdenckla/MAM-basics/commit/5eeec102d856bf87b0ad1a03cbac64fa702b72ce)
and its completed October 24 HP recovery without repeating checks or earlier review windows.
Reviewed the [one-commit/one-path endpoint](https://github.com/bdenckla/MAM-basics/compare/0f66512aa92d32f7de463b9aad82b8c2edec9462...926a6e785be4236673ac4a5c8c34afe63ed417f4):
only `dot-claude/skills/github-issues/references/reading-and-writing.md` changes.
The added prose records the owner's observed loss of combining marks in an issue body and
advises describing a heavily marked atom in words from the start. The existing requirement
to compare filed code points remains intact. This is transport guidance, not a change to
Hebrew data, interpretation, executable code, workflows or generated products.
No consequential defect or repair was identified. The historical transport observation was
not independently reproduced; this connector-only screen ran no tests or generators.
Reviewed-through advances to the frozen endpoint; broad-tested and focused-checked anchors,
the original startup failure and the later HP results remain unchanged. This update preserves
the prior maintained history on the isolated receipt branch only; no main/shared-branch
integration, deployment, editorial change, baseline acceptance or frozen-font regeneration.

Nightly broad checks, 2026-10-25: reconciled isolated receipt `5a7fcf0f9372bc0035341ebde2b40199ffb5734f`; the frozen source was already screened, so no review window was repeated. Completed the maintained broad checks with zero tracked output differences. The [compact receipt](review-nightly-2026-10-25.json) records exact source/input commits, commands, durations, actual skips and limitations. Earlier blocked attempts, failures, focused results and pending isolated repairs keep their original scope. This branch preserves the previous receipt history; its code tree is not the tested source. No source repair, main integration, deployment, baseline acceptance, frozen-font regeneration or schedule change.

Nightly broad checks, 2026-10-26: reconciled isolated receipt `f0162355445de9a6dbf34df3fd58e1fd693b5d15`; frozen main equals the reviewed-through anchor, so no review window was repeated. mega exit 0 in 475.487 s, all 60 steps/no skips; full suite exit 0 in 321.367 s: 1099 passed, 5 established skips, 82 subtests passed; eight explained SVG geometry/Times-alias differences preserved and reversed. The [compact receipt](review-nightly-2026-10-26.json) records exact commands, committed inputs, results, skips, generated differences and limits. Evidence was preserved before restoring generated artifacts; none was accepted into source or baseline. This branch continues the prior receipt history; its code tree is not the tested source. Earlier failures, owner attribution and pending isolated repairs retain their original scopes. No main integration, deployment, publication or schedule change.

Hourly focused review, 2026-10-26: reconciled nightly receipt `c6a28fc5388f84017064e7d48e75234426b8e912` without repeating its broad checks. Closed only `926a6e785be4236673ac4a5c8c34afe63ed417f4` through `3c6b216c13c3ffa043501a485ea5481a6ab31e93`: independent extraction from all 24 committed raw plus JSON books agrees form-for-form, with eight plus rows and no double-guillemet row. Full FOI-only regeneration reproduces all 51 root files, including the new page and retained empty section; selected-note and other-FOI runs preserve the expected products. Six scratch checks passed initially; one scratch assertion mistook HTML line wrapping for missing text, then passed alone after whitespace-aware correction (six deselected). No production defect or repair. [Compact receipt](review-hourly-2026-10-26-doc-notes.json) retains commands, counts, output comparisons and limits; previous focused evidence remains below. Broad-tested source/result and prior failures/isolated repairs retain their original scopes. The new isolated receipt branch continues the nightly history; its code tree is not the tested source. No Private write, HP action, main push, deployment, font generation or baseline acceptance.

Previous focused-check result (historical scope): source
`75de03e816162c6e5f7005eb85b36a5024c09cce`: 51 maintained tests pass; repair
`062da1e80a1e725b1dd176a9b9d3e9c18a1b6076`: 32 independent/regression checks pass.
No broad-test advance.

Hourly focused review, 2026-10-26: reconciled `556df8b0dcc46be5998a1850f4b85c33e143775e` and reviewed only `3c6b216c13c3ffa043501a485ea5481a6ab31e93` through `ee700b4713ea242e5d27f18bdff3093756df97d7` (three commits / 12 paths). New guide generation and existing miscellaneous/trusted-survey site generation reproduce without tracked output differences. The 22 existing focused tests pass; two separate raw-CSV/HTML census checks pass, independently matching 23,206 CSV and 23,213 AJF rows, 92 code-point counts, all 14 element/class counts, local links, marked Hebrew cells and CGJ preservation. All 17 canonical font copies have the existing 0.921 hash; the license diff inventories that existing asset/exception and establishes no new terms. No consequential defect or repair; author/plan claims were not adopted as new authority. [Compact receipt](review-hourly-2026-10-26-sefaria.json) preserves exact commands, committed inputs, zero skips and the incidental pytest/gen-misc overlap. Prior FOI evidence, its scratch assertion failure/correction, the broad-tested anchor and pending isolated repairs remain historical results with their original limits. The new receipt branch continues the existing history; its code tree is not the tested source. No Private/Fonts/HP action, main integration, deployment, baseline acceptance or font generation.

Hourly focused review, 2026-10-26: continued `86c1afedd4b8fd693d709b168143e82ee7bf3444` and closed only `ee700b4713ea242e5d27f18bdff3093756df97d7` through `c6701099fd146832cb74a523d549a0e4c09c97b1` (one commit / 13 paths). All three regenerated pages reproduce with no tracked diff; 25 maintained checks pass, zero skips. Independent raw-file checks match the 92 CSV/90 AJF code-point inventories and every count, all 14 markup counts, navigation, local links/fragments, stylesheet/font targets and CGJs. The first scratch run had two passes and one false trailing-space assertion; after distinguishing spaces retained in the CSV from stripping of the last field, only that check reran and passed, confirming nine documented exceptions and 3,482 retained trailing spaces. [Compact receipt](review-hourly-2026-10-26-sefaria-split.json) records the failure, focused follow-up and verified sequential process timestamps. No consequential defect or repair. Data/font inputs and license terms are unchanged; editorial choices and previous receipt history, including its overlap record, are preserved. Broad-tested source/result remains unchanged. New isolated receipt branch only; no broad rerun, main integration, deployment, permission/license change, font build, baseline acceptance or Fonts/Private/HP action.

Hourly focused review, 2026-10-26: reconciled `505af0986bf7a1dff8e5fcc3cebe2c75a664b306` and closed only `c6701099fd146832cb74a523d549a0e4c09c97b1` through `fab8bd0a886d623c4fd6b2a324594f8aee19af87`. Three pages reproduce with no tracked difference; all 53 lifted example cells retain their ordered text and one-font markup. Initial focused run: three passed/one scratch adapter failure, zero skips; only the corrected guard check reran and passed, including 11 prose-fragment mutations and inline/break boundaries. [Compact receipt](review-hourly-2026-10-26-prose-font.json) retains actual commands/failure and evidence. Processes were sequential; prior anchors and receipt history are preserved. No consequential product defect or repair; no broad rerun, main/shared integration, deployment, Private/HP action, font build or baseline acceptance.

Previous focused scope (historical): Source `c6701099fd146832cb74a523d549a0e4c09c97b1`; three-page regeneration reproduces; 25 maintained tests pass, zero skips. Two independent checks pass initially; corrected trailing-space oracle passes alone on follow-up. [Focused receipt](review-hourly-2026-10-26-sefaria-split.json) preserves exact scope/failure/commands. Prior focused evidence and overlap record unchanged; no broad-test advance.


Hourly connector screening, 2026-10-26 20:25 UTC: examined the one-commit endpoint
`fab8bd0a886d623c4fd6b2a324594f8aee19af87` through
`4490e668dc168b598010dd2250878defc88830c1`. Only the plan's completion record
changed: it attributes Ben's review and leaves Pages dispatch separate. The current
Pages workflow was read and is manual-only; no dispatch or publication is authorized
or performed by this record. No executable, generated output, data or policy change,
so no deeper investigation, executor, regeneration or test run was needed. Owner-reported
checks are not claimed as ours. Prior focused and broad-tested anchors remain unchanged.

Hourly focused review, 2026-10-26: continued `0f7314624d37086b307072baaad3217045b7242c` and closed only `4490e668dc168b598010dd2250878defc88830c1` through `629218d2f44c006f36eeb0dcb16e8eacdd052a41` (two commits / 83 paths). Shared asset resolution, unchanged 0.921 bytes, source-link reachability, standalone packaging and focused Phonetic/Yeivin/Sefaria/near-Aleppo/versification comparisons pass. The scratch near-Aleppo comparison initially omitted the existing link-presentation stage; its diagnostic failure and corrected one-check pass are retained. No consequential defect or repair; license wording was assessed only against existing declarations and moved bytes. [Compact receipt](review-hourly-2026-10-26-shared-font.json) records actual commands, failures, zero skips, output comparisons and limits. All stages across both repositories were awaited sequentially. Broad-tested anchor, prior failures and receipt history remain unchanged. This new isolated receipt branch contains no integration, deployment, font generation or baseline acceptance; its code tree is not the tested source.

Hourly focused review, 2026-10-27: continued `b3ac70cdb47de783ed3cd0404df60059709df8f9` and closed only `629218d2f44c006f36eeb0dcb16e8eacdd052a41` through `9302ad04b347aa2db3ee0004962cd66202031cce` (one commit / 13 paths). Selected MAM-with-doc generation and all 106 near-Aleppo outputs reproduce. Exact-parent differential rendering agrees for all 4,512 verses in three modes, including nested qamats and documentation; 7,119 raw helper/option comparisons, malformed-input checks and actual FOI option-isolation calls pass. Default and near-Aleppo retain parameter 1; MAM-with-doc uses parameter 2. The scratch endpoint oracle initially missed meteg replacements already present in the raw selected parameters; its failures, stopped slow diagnostic and corrected raw-derived comparison are preserved. All processes were awaited sequentially; no skips or production failure. [Compact receipt](review-hourly-2026-10-27-stress-helper.json) records exact commands, counts, output comparisons and limitations. No consequential implementation defect or repair; the editorial decision is preserved. Broad-tested and historical receipt anchors retain their scopes. Isolated receipt branch only; no broad rerun, main/shared integration, deployment, Private change, font regeneration or baseline acceptance.

Nightly broad checks, 2026-10-27: continued isolated receipt `d227e2b7d2153a7fb69a6345e11e0cdb2febd04c` and preserved the preceding nightly history. Actual main equals reviewed-through; no endpoint window was repeated. mega exit 0 in 495.494 s, all 61 steps/no skips; full suite exit 0 in 333.300 s: 1100 passed, 5 skipped, 82 subtests passed in 329.93s (0:05:29); eight explained SVG differences preserved and reversed. The [compact receipt](review-nightly-2026-10-27.json) records exact inputs, commands, actual skips/failures, fresh output triage and limits. Generated evidence was preserved before restoration; none was accepted into source or baseline. No source repair, main/shared integration, deployment, publication or scheduling action. This isolated receipt tree is not the broadly tested source; prior focused evidence, failures and pending repairs retain their scopes.

Hourly partial review, 2026-10-27: continued nightly receipt `ab2b85d7c75cc927d930b1d17b112d301d42dae1`, preserving the reconciled `9302ad04b347aa2db3ee0004962cd66202031cce` reviewed/broad-tested anchors and all earlier history. Inspected only the new endpoint through `46f80ecc8b29fdd7f5fdf30c40bc2b3382bbb352`. Lightweight raw-JSON inspection independently matches all five census counts and nine published parameter pairs; the 1.0 font/archive bytes and all nine source members match the declared release/source commit, support mappings and same-host links agree, and spacing executable code is unchanged. Eight-file formatting and endpoint whitespace checks pass. No confirmed defect or repair. [Partial receipt](review-hourly-2026-10-27-dehi-font-partial.json) records exact inputs, commands and omissions. The parent restriction for the active HP reader task prevents expensive generators/large tests; none started, and no release has arrived. FOI regeneration, actual note/count/empty/isolation behavior and shared-renderer product comparisons remain pending, so neither reviewed-through nor tested anchors advance. Clean isolated checkouts and evidence are retained for continuation. No Private write, font engineering/build, baseline acceptance, main/shared push or deployment.
