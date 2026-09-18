# Updates to the Metsudah-versus-CTR comparison

State: open, first entry 2026-09-12. Every entry here corrects or supplements
`doc/metsudah-vs-ctr.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document — a review, a remediation plan, a completed
plan, an execution record — is left as written, like a pushed commit. A correction to one goes in
a sibling file named `<stem>-update.md`, which is what this file is for that comparison. Nothing
here edits the document it corrects.

## The module named beside the Sefaria download endpoint is gone

Recorded by a Claude session on 2026-09-12, for finding 19.1 of
`doc/review-findings-2026-09-10.md` (on branch `dual-agent-review-2026-09-10` until that review
round integrates).

The sources section describes the Metsudah CSV as fetched from
`https://www.sefaria.org/download/version/<book> - he - <versionTitle>.csv`, and adds "(the same
endpoint `py/subcommands/download_sefaria.py` uses for MAM)". That module is not in this
repository: `985262e2` of 2026-09-10, "Remove the Wikisource index generators, the column plots
and fr-sefaria", deleted it with the `fr-sefaria` subcommand it served. Measured 2026-09-12, no
file of that name is tracked.

The comparison itself is unaffected. Its fetch happened on 2026-08-04, the CSV it produced is
what the findings rest on, and nothing in this repository re-fetches from that endpoint now.

## 2026-09-16: the crop README moved after the finished report

The base passage beginning “The motivating clue is in” names the historical destination. The live
destination of the former `doc/ms-snips/README.md` is
`doc/lam-2-3-akhla-snips/README.md`; the base report keeps its historical link.

## 2026-09-18: the prose system is a property of verses, not books

The base's phrase `prose-book tipḥas` should read `tipḥas in prose verses`; the prose and poetic
systems classify verses, not books.
