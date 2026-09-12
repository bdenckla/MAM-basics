# Updates to the public-repo evacuation programme

State: open, first entry 2026-09-12. Every entry here corrects or supplements
`doc/PLAN-evacuate-public-repos-programme.md`, which declares itself complete and is left exactly
as written.

Ben's decision, 2026-09-11: a finished dated document — a review, a remediation plan, a completed
plan, an execution record — is left as written, like a pushed commit. A correction to one goes in
a sibling file named `<stem>-update.md`, which is what this file is for the programme. Nothing
here edits the document it corrects.

## The licence argument names a `DATA-LICENSES.md` row that does not exist

Recorded by a Claude session on 2026-09-12, for finding 19.2 of
`doc/review-findings-2026-09-10.md` (on branch `dual-agent-review-2026-09-10` until that review
round integrates).

The paragraph beginning "**byte-identical `LICENSE.md`**" lists the CC-BY-SA 4.0 rows that
`DATA-LICENSES.md` already carries as "`in/mam-ws/`, `in/mam-go/`, `in/mam-from-sefaria/` and
`in/mam-ws-bot-edits/`". Measured 2026-09-12, `DATA-LICENSES.md` has no `in/mam-from-sefaria/`
row. The row that exists is `in/mam-from-Sefaria-2021-11-23/`, at line 51, which is a different
directory and still present; the `in/mam-from-sefaria/` that was deleted had no licence row of
its own and has no surviving code reference.

The argument the paragraph makes is unaffected — that the MAM statement and its CC-BY-SA 4.0
regime were already in place before the five products landed, so each lane's licence step adds
rows to a regime rather than establishing one. Only the name of one row is wrong.
