# Updates to the assessment of two stranded artifacts

State: open, first entries 2026-09-12. Every entry here corrects or supplements
`doc/assessment-two-stranded-artifacts-2026-09-09.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document — a review, a remediation plan, a completed
plan, an execution record — is left as written, like a pushed commit. A correction to one goes in
a sibling file named `<stem>-update.md`, which is what this file is for that assessment. Nothing
here edits the document it corrects.

## Every disposition the assessment leaves to Ben was taken the same afternoon

Recorded by a Claude session on 2026-09-12, for finding 14 of `doc/review-findings-2026-09-10.md`
(on branch `dual-agent-review-2026-09-10` until that review round integrates).

The assessment's State line says that "every disposition below is Ben's to choose", and its §8
offers four recommendations and two items under "Left for Ben, because each is a decision rather
than a correction". All six were executed between 13:36 and 14:16 on 2026-09-09, within hours of
the assessment being written. Each of the six commits cites the assessment; the assessment cites
none of them, having been finished before they existed.

| §8 item | Commit | Time | What it did |
|---|---|---|---|
| Recommendation 1, merge `origin/claude/charming-mayer-xknwcw` | `b490988a` | 13:48 | merged the stranded mark-order branch |
| Recommendation 2, move the review plan to `MAM-basics/doc/` | `361b3dab` | 13:36 | moved it from github-misc, repointed |
| Recommendation 3, the report-only widening of `--clean-worktrees` | `5a07e5af` | 14:16 | made a remote-only agent branch visible to the sweep |
| Recommendation 4, repair the four edition transcriptions and widen the lint | `10a5c307` | 13:59 | repaired them, the lint now covering them |
| Left for Ben 1, whether the review joins the public periodic series | `23d33437` | 13:36 | answered it: nothing needs deciding, the public-only property no longer excluding those files |
| Left for Ben 2, whether to close the lint's silent-skip channel | `5300d714` | 14:04 | closed it, under an assertion of its own |

So the State line is overtaken. Nothing in §8 is still Ben's to choose, and a reader arriving at
the assessment on its own would conclude the opposite.

## §9 announces three measurements and numbers four

Recorded 2026-09-12, for the same finding. §9's sentence "The three measurements that needed a
script" is followed by four numbered items. `40c0ade4` of 13:17 that day added the fourth, the
edition-transcription diagnosis of §1, and left the count in the sentence above it at three. The
four items are right; the word "three" is wrong.
