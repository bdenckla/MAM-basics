# Updates to the September 8 remediation plan

State: open, first entry 2026-09-11. Every entry here corrects a passage of
`doc/PLAN-remediate-review-findings-2026-09-08.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document — a review, a remediation plan, a completed
plan, an execution record — is left as written, like a pushed commit. A correction to one goes in
a sibling file named `<stem>-update.md`, which is what this file is for the September 8
remediation plan. Nothing here edits the document it corrects.

## The Wave 3 display fallback was retired on 2026-09-10

Recorded by a Claude session on 2026-09-11, for finding 3 of `doc/review-findings-2026-09-10.md`.

Items 1 and 2 of the Wave 3 technical source changes, in the list introduced by "The technical
source changes are:", describe a display fallback that no longer exists. `3a1ab7f0`
(2026-09-10 12:21) removed both `mam_form or chanted_word` sites from
`py/author_site/post_stress_meteg.py`. That module's `_mam_form` now raises `SurveyProblem` for a
displayed survey entry with no `mam_form`, so no render path reaches the snapshot, and item 1's
sentence "An actual display fallback requires the snapshot to be available" no longer applies.
The snapshot lookup is now `_snapshot_unannotated_form`, private to
`py/accgram/post_stress_meteg.py`. Item 1's matching selection, item 2's mark preservation, and
items 3 and 4 are unaffected. `CLAUDE.md`'s section "A code path reads MAM-private every time it
runs, or never" states the rule that retired the fallback.

## Finding 20.2: the State references should name their historical points directly

Recorded by Codex on 2026-09-12, for finding 20.2 of
`doc/review-findings-2026-09-10.md`.

The sentence `The former current State at source 0ee34bea8 is preserved here:` should read
`The State at source commit 0ee34bea8 is preserved here:`. The commit identifies the preserved
State directly.

The sentence `For example, the former line-3 State was:` should read `For example, the line-3
State before Ben's approval was:`. Ben's approval is the event that made the quoted State
historical.
