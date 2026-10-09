# MAM-basics review and testing trial status

State: live; prepared 2026-10-07

Policy: [review-trial.md](review-trial.md). One confirmed automation, `Review MAM changes`,
schedules seven daily runs on 2026-10-08 through 2026-10-14, around 2 a.m. America/New_York.

| Anchor | Commit/result |
| --- | --- |
| Adopted baseline | `d66a3faf1403e945a0f41e5d25c86c3ac72b871f` |
| Reviewed through | `2265bf9cde517502571b6f848c950c3c0394feaa`; run 2 endpoint review, no new consequential defect confirmed |
| Last tested | `2265bf9cde517502571b6f848c950c3c0394feaa`; all 60 mega steps completed; suite passed with five documented semantic skips; eight SVG layout/Times-alias diffs explained and preserved |

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

After night seven, record the compact assessment of Ben's time, meaningful defects,
unnecessary changes and adequacy of evidence here.
