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
Ben's authorization; no proposal was then applied. Proverbs 30:17's ḥataf addition
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
commit that holds it. The other nine proposals, #316–#324, were then still recorded
as unapplied, and the audit's snapshot quotations are unchanged.

The same Introduction refresh corrected the spelling of Westminster in a heading of
the Westminster page, and the review build stopped there. `RENAMED_HEADINGS` in
`py/intro_doc_audit/human_review.py` now maps the snapshot heading to its current
text for that page's links.

## 2026-10-29 — four more proposals applied

Later that day skadish1 reported four more of the submitted proposals done, each
with a link to the Wikisource revision that made it: #321 (chapter 3, revision
3098995), #322 (chapter 2, 3098993), #323 (3098992) and #324 (3098991). A Claude
session checked each revision against its issue and closed the four issues at
Ben's request. The Introduction mirror holds chapter 2 at revision 3099100 and
chapter 3 at the later revision 3099123 from `f82138dd`. Ben approved recording
the applications the same day, answering a plan that recommended it: “Yes, as
recommended”.

#321, #322 and #324 were applied exactly as proposed. #323 went further: the
layout example's whole verse now copies MAM's Proverbs 30:19, whose note gives the
printed editions' word pair with a space, and a footnote in section עולה ויורד had
the maqaf form at the audit's snapshot. Its application record declares the
context of each occurrence of the old and the new word pair, and the review build
checks that every occurrence lies in one of them. Nine proposals are now recorded
as applied, #311–#315 and #321–#324.

#316–#320 are still recorded as unapplied. The same refresh took chapter 3's
revision 3099123 and chapter 5's revision 3099114, which add Genesis 30:27 and
2 Samuel 8:10 to their ḥataf lists as #320 and #318 propose; skadish1 reported
both done later on 2026-10-29, and the last 2026-10-31 entry below records their
applications.

## 2026-10-31 — the page served from gh-pages

Ben asked for an overall issue to track the possible issues this audit raised, pointing
to its overall document, and asked that the document, being HTML, be served from
gh-pages: “it doesn't need to be "official" in particular it doesn't need a link-path
to it from gh-pages/index.html, i.e. it should be an "orphan" that you need to know its
URL and that is the only way to get to it”. The `review` subcommand now also writes
`gh-pages/intro-doc-audit/index.html`, served at
<https://bdenckla.github.io/MAM-basics/intro-doc-audit/>. It differs from
[review.html](review.html) only in its font path and in linking this directory's notes
on GitHub, and no other page links to it. For this one page, this supersedes the base's
exclusion of gh-pages edits; the site changes only when Ben dispatches the Pages
workflow. #346, filed the same day with Ben's approval, is the overall issue for the
page's open discrepancies and questions.

## 2026-10-31 — two more proposals applied

A Claude session checked Avi's revisions against #318 and #320 and closed both at
Ben's request. Revision 3099114 of chapter 5 adds 2 Samuel 8:10 to the Samuel list,
and revision 3099123 of chapter 3 adds Genesis 30:27 to the Genesis list, each after
the entry its proposal names and with its heading's count raised by one, exactly as
proposed. Ben then asked that the applications be recorded: “File + record 318/320”.
Each decision in [adjudications.json](adjudications.json) now holds its application,
checked against `f82138dd`, the mirror commit that holds both revisions. Because an
added entry lands away from the heading shown with it, these two records set
`mirror_check` to `full-list`: the build requires the mirror to hold each decision's
whole proposed list once and its snapshot list nowhere. Eleven proposals are now
recorded as applied: #311–#315, #318 and #320–#324.

The same reports answer the other two additions: “Song of Songs 1:6 does not belong,
the hataph is not in AC” (#317) and “Numbers 10:9 is not relevant” (#319). Both
issues remain open, and #316, #317 and #319 are still recorded as unapplied.
