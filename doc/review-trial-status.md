# MAM-basics review and testing trial status

State: live; prepared 2026-10-07

Policy: [review-trial.md](review-trial.md). One confirmed automation, `Review MAM changes`,
schedules seven daily runs on 2026-10-08 through 2026-10-14, around 2 a.m. America/New_York.

| Anchor | Commit/result |
| --- | --- |
| Adopted baseline | `d66a3faf1403e945a0f41e5d25c86c3ac72b871f` |
| Reviewed through | `d66a3faf1403e945a0f41e5d25c86c3ac72b871f`; adopted without retrospective review |
| Last tested | None; trial checks have not run |

Run from an isolated repository root with its home clone's interpreter: `py/main_0_mega.py`,
then `py/main_test.py`. Use each required private sibling's recorded committed checkout;
do not copy private evidence into this note. Explain tracked generator diffs and record
failures/incomplete checks before updating the anchors. Detailed repair evidence may live in
the repair commit; a passing suite or no-diff mega is not proof of the underlying interpretation.

| Run/repair | Frozen commit and allowed input IDs | Result, disposition and evidence |
| --- | --- | --- |
| Setup, 2026-10-07 | Adopted baseline above | No retrospective review or broad-check run; procedure integrated and seven-night schedule confirmed |
| Run 1, 2026-10-08 | `275ed4683a6b71b4cba33f99c0ed57740e92c292`; no runtime sibling inputs selected | Blocked before execution: shell setup returned `helper_unknown_error: setup refresh had errors` twice, including a minimal clock read. HP process inventory, isolated checkout and home-environment verification were unavailable; mega and suite were not started, so there are no test durations or results. GitHub endpoint inventory found 61 incoming commits; full code/data review remains incomplete. Reviewed-through and last-tested anchors stay unchanged. |

After night seven, record the compact assessment of Ben's time, meaningful defects,
unnecessary changes and adequacy of evidence here.
