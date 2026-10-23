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
| Reviewed through | `27f263cb6a158566ec290a67123364f6b690106b`; connector endpoint review from `d6d96d936d2556bfc6ded87efd62876af5e88d35` (one commit/one documentation path), following the [prior isolated receipt](https://github.com/bdenckla/MAM-basics/blob/54bfe0d699e68d5e7cbe07b36107886b5a325316/doc/review-trial-status.md). Conditional deployment safeguards remain intact; no new consequential defect confirmed. Prior checker repair `062da1e80a1e725b1dd176a9b9d3e9c18a1b6076` remains isolated, pending Ben's main-integration approval. |
| Last tested | `27f263cb6a158566ec290a67123364f6b690106b`; October 23 mega exit 0, 60 steps/no skips in 793.101 s; full suite exit 0 in 476.176 s: 1099 passed, 5 existing skips, 82 subtests passed; eight freshly explained SVG differences preserved |
| Last focused checked | Source `75de03e816162c6e5f7005eb85b36a5024c09cce`: 51 maintained tests pass; repair `062da1e80a1e725b1dd176a9b9d3e9c18a1b6076`: 32 independent/regression checks pass. No broad-test advance |

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
| Nightly, 2026-10-23 | `27f263cb6a158566ec290a67123364f6b690106b`; allowed committed inputs `b58ea672854a0ee563c9fdbd64afe93859ec2cc9`, `56f4ba837f70c9a6a7a3ad4692c49e5d09c98eec` | New nightly run: mega exit 0, all 60 steps/no skips (793.101 s); full suite exit 0 (476.176 s): 1099 passed, 5 existing edition-transcription skips, 82 subtests passed. Eight SVG geometry/Times-alias differences freshly verified and preserved privately; all other content reproduces. Suite ran on the clean frozen tree after verified reverse apply. Latest isolated receipt reconciled; no repeated review window, repair integration or main advance. [Compact receipt](review-nightly-2026-10-23.json). Isolated branch only; no deployment or schedule operation. |

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
