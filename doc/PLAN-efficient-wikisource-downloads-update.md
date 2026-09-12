# Updates to the revision-aware Wikisource downloads plan

State: open, first entries 2026-09-11. Every entry here corrects or supplements
`doc/PLAN-efficient-wikisource-downloads.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document — a review, a remediation plan, a completed
plan, an execution record — is left as written, like a pushed commit. A correction to one goes in
a sibling file named `<stem>-update.md`, which is what this file is for the downloads plan.
Nothing here edits the document it corrects.

## The plan's own state: complete

Recorded 2026-09-11. Most plans under `doc/` declare their state in a `State:` line at line 3,
directly under the H1. This one declares it in prose instead, in the paragraph beginning "All
three phases are complete." Its state in the conventional form is **complete**: all three phases
executed, the last of them on 2026-09-10.

## The production refresh of the 20 chapters, 2026-09-10

Recorded by a Claude session on 2026-09-11, for finding 6 of `doc/review-findings-2026-09-10.md`
(on branch `dual-agent-review-2026-09-10` until that review round integrates). Until this
section, the refresh was recorded only in its commit message, "Refresh Wikisource products.
Download current Wikisource data and regenerate the complete pipeline." No document records who
decided to make it, or when.

The refresh is `209b4c05` (2026-09-10 20:53, co-authored by Codex), whose parent is `b2052ab9`,
the Phase 3 seed commit. It reached `main` through the merge `a0a2e3ab` at 21:22. Every figure
below compares `209b4c05` with its parent; re-establish each with the command given, and treat a
mismatch as a finding.

1. **All 20 chapters Phase 3 left unseeded were downloaded**, in 11 books: Genesis 43;
   Deuteronomy 28 and 32; Joshua 19; Judges 10; 1 Samuel 1 and 22; 2 Kings 6 and 17; Isaiah 22,
   24, 42 and 50; Zephaniah 3; Psalms 4, 71 and 84; Daniel 3; 2 Chronicles 26 and 28.
   `in/mam-ws-revisions.json` went from 909 records to 929
   (`git diff --stat 209b4c05^ 209b4c05 -- in/mam-ws/ in/mam-ws-revisions.json`).
2. **The same 11 books changed in the three intermediates written from `in/mam-ws/`**:
   `out/mam-ws-bot/proto/`, `out/mam-ws-bot/proto-fmt-2/` and `out/mam-ws-parsed-fmt-2/`.
3. **21 verses changed in `MAM-parsed/plus/`, and the same 21 in `MAM-parsed/plain/`**, all in
   those chapters:
   1. eleven meteg changes, nine removals (Joshua 19:8, 1 Samuel 1:6 and 22:22, 2 Kings 6:23,
      Isaiah 22:5, 42:24 and 50:7, Zephaniah 3:13, 2 Chronicles 26:15) and two additions
      (Isaiah 24:18, 2 Chronicles 28:19);
   2. ten changes to notes and templates (Genesis 43:28, Deuteronomy 28:30 and 32:18, Judges
      10:11, 2 Kings 17:15, Psalms 4:3, 71:9 and 84:4, Daniel 3:5, 2 Chronicles 28:23).
4. **Only the eleven meteg changes reached `MAM-simple/xml-vtrad-mam/`**
   (`git diff 209b4c05^ 209b4c05 -- MAM-simple/xml-vtrad-mam/`), and `MAM-for-Sefaria/csv/` and
   `MAM-OSIS/MAPM-24/` changed only in the six books holding those eleven verses.
5. **Two downstream outputs were left stale and caught up on 2026-09-11**: the mpplus change log
   under `gh-pages/MAM-with-doc/change-log/`, in `6b45ad0f`, once `f11ecaf8` had fixed the diff
   defect that the Isaiah 24:18 meteg exposed (findings 1 and 2 of the same review); and the
   post-stress-meteg survey, in `aedac688`, which also moved the page's pinned counts.

Those figures were re-measured from `209b4c05` alone, where the review had measured the whole
window. The finding's "21 verses changed in every product" holds for `MAM-parsed/plus/` and
`MAM-parsed/plain/`; `MAM-simple/xml-vtrad-mam/` changed in 11.

## Three passages the refresh made stale

Recorded by a Claude session on 2026-09-11, for the same finding.

1. **The status paragraph** ending "a production refresh remains a separate decision" describes a
   decision that has since been taken and carried out. `209b4c05` downloaded the 20 unequal
   chapters, and `in/mam-ws-revisions.json` has held 929 records, one per chapter, since then.
   The paragraph stays as the record of Phase 3's result.
2. **"A normal all-book run against the committed partial seed would fetch the 20 excluded
   chapters"**: since `209b4c05` the production manifest covers all 929 chapters, so the partial
   seed that sentence describes no longer exists.
   `doc/efficient-wikisource-downloads-phase3-validation.json` still says "20 unequal chapters
   have no seeded record"; it is Phase 3's receipt and stays as written.
3. **"The unresolved production-text decision concerns the 20 excluded chapters"**: that decision
   was taken and carried out on 2026-09-10, in `209b4c05`.
