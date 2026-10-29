# Later status for the cached audit boundary register

State: open; first entry 2026-10-16

## 2026-10-16 — Ben-authorized main integration and continuation

The base's passages saying that no main integration is authorized and that the
research remains isolated describe its earlier boundary. Ben explicitly authorized
integrating this audit into MAM-basics main and requested a local continuation
runbook on 2026-10-16. [RUNBOOK.md](RUNBOOK.md) is the current guide; the original
source snapshot, proposals and substantive decisions remain preserved.

Subsequent authorized history research is recorded separately in the history
plans, results and literal sources. All 94 applicable cases have dispositions,
including explicitly inconclusive cases. The current completion and follow-up
inventories supersede earlier checkpoint totals, without certifying every reading.

This integration authorizes no source-data edits, deployment or further external
submission. The separate index-label and issue-writing-policy branches are outside
its scope. Open the main checkout's sibling [review.html](review.html) rather than
relying on the original temporary checkout path.

## 2026-10-17 — Wikisource links and submitted proposals

Ben asked that every review entry link to Hebrew Wikisource; each quoted passage
now links to the live page at the heading above it, or at its verse
([RUNBOOK.md](RUNBOOK.md)). He then authorized issues for every approved
proposal: #311 (the appendix's date) and #312 (the Job 9:10 reference), and
#313–#324 for the twelve corrections approved earlier. Each
decision record in [adjudications.json](adjudications.json) holds its issue and
Ben's authorization; no proposal is applied. Proverbs 30:17's ḥataf addition
still awaits Ben's review.

## 2026-10-18 — the Introduction's note templates

Ben asked that every `{{נוסח}}` call in the Introduction take the chapter pages'
form, the note as parameter 2 written `2=`. The Wikisource bot's new `intro` mode
made the six edits on chapters 2, 3 and 4 (`py/ws/ws_bot_edit_history.md`), the
mirror was refreshed, and #323's before and after now show the `2=` form. The
audit's snapshot quotations are unchanged.

## 2026-10-29 — five proposals applied

On 2026-10-19 skadish1 reported five of the submitted proposals done, each with a
link to the Wikisource revision that made it: #311 (revision 3092644), #312
(3092653), #313 (3092656), #314 (3092657) and #315 (3092658). The Introduction
mirror holds the first two from `0cb9332a` and the chapter mirror the other three
from `fd0d1b1d`, both of 2026-10-28; chapter 1's mirrored revision, 3095761, is
later than 3092653 and keeps the change. #313's quotation was applied without the
optional masorah circle. skadish1 closed #314 and #315 on 2026-10-19, and a Claude
session closed #311–#313 on 2026-10-29 at Ben's request. Ben approved recording the
applications here the same day: “Yes, record them”.

Each of those five decisions in [adjudications.json](adjudications.json) now holds
its application, and its case in [review.html](review.html) shows the applied text
after the proposal. The review build checks each applied text against the mirror
commit that holds it. The other nine proposals, #316–#324, are still recorded as
unapplied, and the audit's snapshot quotations are unchanged.

The same Introduction refresh corrected the spelling of Westminster in a heading of
the Westminster page, and the review build stopped there. `RENAMED_HEADINGS` in
`py/intro_doc_audit/human_review.py` now maps the snapshot heading to its current
text for that page's links.
