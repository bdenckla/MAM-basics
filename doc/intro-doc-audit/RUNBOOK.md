# Continue the Introduction and doc-note review

State: runbook

Open [review.html](review.html) from the main checkout. It is a standalone local
page; no server or temporary worktree is needed. [METHODS.md](METHODS.md) holds
the detailed evidence and earlier checkpoints. This is the current continuation
guide for a local Codex or Claude session.

## Start here

Read current `AGENTS.md`, the `hebrew-prose` skill and its MAM-basics reference.
Follow `linked-worktrees` for development and integration. Verify the checkout,
branch, HEAD and dirty files before editing; preserve unrelated interactive work.
Use the full clone's environment, or its absolute interpreter from a worktree.
Check active workloads before costly work; use small sequential batches and defer
heavy work to nightly checks.

Ben authorized this audit's integration into main on 2026-10-16. This does not
authorize source edits, manuscript interpretation changes, deployment, external
submission, or merging the separate index-label and issue-writing-policy branches.
Approved corrections remain proposals for Avi, not changes already made to MAM
or Wikisource. Any later application or submission needs its own recorded scope.

## Which files govern what

- `human-review.json` owns case IDs, sections, questions, exact panels,
  translations, reading forms and history summaries. Edit a case here, not in HTML.
- `adjudications.json` owns Ben's substantive decisions and their authority,
  exact proposed edits and application/submission status. Companion adjudication
  notes provide context. Preserve all twelve existing decisions.
- `claims.json`, `notes.json`, the source captures and `source-pin.json` retain
  the original evidence at `89cb865729b0876f1fd32a8a3579eaec80b4fc0c`.
  `snapshot.py` reads raw passages and context from that Git commit. Newer files
  on main do not silently replace the original evidence. Keep this commit
  available locally; rendering fails rather than substituting another version.
- `review.html` and `human-review-coverage.json` are generated. Opening or
  collapsing a case is UI state only; it is neither a decision nor completion.
- Every quoted passage links to the live Wikisource page: an Introduction
  passage at the nearest heading at or above its snapshot line, a doc-note or
  verse at its verse anchor on MAM's chapter page. Ben chose live links on
  2026-10-17, accepting that a link can show text newer than the quotation. A
  heading missing from the current mirror stops the rebuild; cases carry no
  hand-made section links.
- `history-completion.json`, `revision-history-inventory.json` and
  `revision-history-results.json` record history coverage. The final original
  pass has 94/94 dispositions, including explicitly inconclusive cases; this
  does not establish 94 definitive chronologies or resolve every reading.
- [revision-history-followups.json](revision-history-followups.json) groups the
  next evidence or editorial questions. Its seventeen approved/tracked/bounded
  context cases are separate from 77 existing editorial/evidence questions.
  [topic-coverage.json](topic-coverage.json) retains broader evidence boundaries.

The original page has 152 cases and twelve Ben-reviewed proposals. The word
"current" in a frozen quotation means current at its recorded source revision,
not necessarily current on Wikisource today. Neither Introduction nor doc-notes
are automatically authoritative. Bare "in the manuscript" does not name Aleppo.

## Update one case

1. Find its existing ID and read the complete panels, decision, source pointers,
   related adjudication and recorded history. Start with a small group from the
   follow-up inventory; do not repeat completed broad passes.
2. Copy Hebrew from the declared source or immutable revision in code, using
   UTF-8. Do not retype pointed forms or normalize faithful captures. Distinguish
   literal encoding/order, named-source attribution, chronology, quotation scope
   and a supported contradiction. Use repository parsing and sigil decoding.
3. Retain the source IDs and exact quotations. Revise English explanations and
   translations against the whole clause; preserve question marks, source
   qualifiers and ketiv/qere distinctions. Translate explanatory prose, not
   Scripture. New evidence gets a separate source/version record; do not overwrite
   the original snapshots merely to make the old discrepancy disappear.
4. A Ben decision is recorded with its date, authority and exact scope in
   `adjudications.json`, linked by the case's `adjudication` ID. Its `current`,
   `changes` and `proposed_quotation` must agree exactly. Keep the proposal
   unapplied until actual application is separately evidenced. Update its
   companion note and any affected coverage/follow-up record without rewriting
   unrelated decisions. Follow the receipt rules for finished notes.
5. Rebuild the review, read that case visually and inspect the focused diff.
   Literal validation is necessary but does not prove translation accuracy or
   manuscript truth. Preserve the 20–48 px Hebrew slider, default 30; keep English
   at its normal size, and add no copy, print, save or persistent-state controls.

`human_review.reviewed_case_ids` puts a case under **Reviewed** only when its
linked adjudication records Ben's substantive authority and a `by-Ben` status.
Do not move a case by changing its original section, setting a UI flag, closing
its disclosure, or treating an independent check as Ben's approval. The Reviewed
group and its cases start collapsed; they remain available for inspection.

## Commands and scope

From a full Windows checkout's repository root:

```powershell
./.venv/Scripts/python.exe py/main_intro_doc_audit.py review
./.venv/Scripts/python.exe py/main_intro_doc_audit.py history-inventory
git diff --check
```

Linux uses `./.venv/bin/python`; a linked worktree uses its home clone's absolute
interpreter. The entrypoint lowers its own Windows process priority. A prose or
decision edit normally needs only `review`; run `history-inventory` when history
dispositions change. Inspect every changed output. The original reproduction
checks 717 literal passages and twelve proposed quotations; explain any intentional
change rather than treating a changed count as approval. No full mega or suite is
needed for this documentation/research workflow without a specific consequence.

Do not run the entrypoint without a subcommand, broad enumeration commands or
downloads just to refresh the page: they rebuild research inputs from the working
source caches. Repeating the original enumeration requires a separate checkout at
the recorded source commit and the original inputs; changing the source boundary
is a substantive new audit, not presentation maintenance.

History plans/results and selected literal excerpts are tracked in
`history-batch*-{plan,results,sources}.json`; earlier Proverbs and count histories
have their own named files. `history-batch history-batchN` rebuilds a generic
batch, while `history-batch1`, `history-batch2` and `history-batch3` use the earlier
compilers. These optional commands need the separate raw API response cache,
originally `.novc/proverbs-history-api`; rendering and reading the retained
evidence do not. Keep that cache when retiring a worktree. The generic compiler's
`cache_dir` argument can name a retained cache after relocation. Do not invent
missing before/after revisions or fetch another broad batch merely to regenerate.
Retain exact revision IDs, timestamps and parent/diff links; distinguish canonical
chapters from drafts and selected Introduction snapshots from proven insertions.

## Remaining work and eventual submission

Outstanding questions include exact Masorah/edition support, manuscript attribution
and uncertainty, illustration and sentence scope, vowel function/list eligibility,
the counted source population, Dotan's convention, strand allocation and the
adapted Wickes list. Finer origins remain explicitly bounded where unlocated.
Use the specific case and follow-up reason; these are not 77 newly confirmed defects.

Before a Ben-authorized submission for Avi, load the current `github-issues` skill
and operation reference, confirm the destination and exact proposal, and read any
existing issue's full body and comments. Check the already tracked cases and the
receipts for issues 309/310 to avoid duplicates. Keep a submission distinct from a
source correction. Copy the approved Hebrew and authority exactly, include the
required agent/date attribution, and verify the posted text's codepoints by a full
read-back. Record the resulting URL and submitted status separately from Ben's
approval. This runbook does not authorize posting, editing issues, contacting Avi
or modifying Wikisource.
