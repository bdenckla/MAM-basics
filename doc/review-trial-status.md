# MAM-basics review and testing trial status

State: live; prepared 2026-10-07

Policy: [review-trial.md](review-trial.md). One confirmed automation, `Review MAM changes`,
schedules seven daily runs on 2026-10-08 through 2026-10-14, around 2 a.m. America/New_York.

| Anchor | Commit/result |
| --- | --- |
| Adopted baseline | `d66a3faf1403e945a0f41e5d25c86c3ac72b871f` |
| Reviewed through | `52f73420395ce9416b9928a957cde9287c273843`; run 6 endpoint through `d921ed3565fb3e6cba8b9d46104e92a488b8df12` and narrow JSON test-caller repair reviewed |
| Last tested | `d921ed3565fb3e6cba8b9d46104e92a488b8df12`; 60-step mega passes with zero tracked output diffs; suite 1079 passed, 5 documented skips, 1 stale XML test-caller failure; repair `52f73420395ce9416b9928a957cde9287c273843` passes all 3 focused module tests; no all-green full rerun |

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
