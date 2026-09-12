# Updates to the Wikisource-derived MAM products programme

State: open, first entries 2026-09-11. Every entry here corrects
`doc/PLAN-wikisource-derived-mam-products.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document — a review, a remediation plan, a completed
plan, an execution record — is left as written, like a pushed commit. A correction to one goes in
a sibling file named `<stem>-update.md`, which is what this file is for that programme. Nothing
here edits the document it corrects.

## The programme's own state: complete

Recorded 2026-09-11. Most plans under `doc/` declare their state in a `State:` line at line 3,
directly under the H1. This one declares it in prose instead, in the sentence beginning "Status
on 2026-09-10: Phases 1 through 5 are complete." Its state in the conventional form is
**complete**.

## "Raw inputs and bot captures are unchanged" stopped being true that same day

Recorded by a Claude session on 2026-09-11, for finding 6 of `doc/review-findings-2026-09-10.md`.

That sentence was true when the programme completed. The production refresh `209b4c05`
(2026-09-10 20:53) then changed 11 books of `in/mam-ws/` and the same 11 books of
`out/mam-ws-bot/proto/`, and with them 21 verses of the Wikisource-derived plain and plus
products. `doc/PLAN-efficient-wikisource-downloads-update.md` §"The production refresh of the 20
chapters, 2026-09-10" records the refresh.
