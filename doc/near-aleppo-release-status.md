# Near-Aleppo release preparation

State: live; notes approved and release publication in progress

Ben requested on 2026-10-12: "Let's make a Near-Aleppo release" and
"Before we release, I will likely want to edit the release notes". Codex prepared
[release notes](near-aleppo-release-notes-2026-10-12.md) for that editing step.
The [October 7 dry run](near-aleppo-release-notes-2026-10-07-draft.md) remains
the historical draft and packaging proposal.

Ben approved publication on 2026-10-12: "Great, let's make that draft official
and do whatever else is needed to make the release." Codex is carrying out
the release through `gh`; Ben need not create it in the web GUI.

## Cumulative revision ledger

| Requirement | Disposition |
| --- | --- |
| Draft fresh notes from the October 7 sketch and subsequent records | Implemented 2026-10-12; the new draft describes the current dataset and pages |
| Give Ben an opportunity to edit before release | Implemented; Ben accepted the draft and authorized publication on 2026-10-12 |
| Include the current note and carrier contracts and qere-without-ketiv work | Implemented; measured against the current reviewed ledger and build populations |
| Select the release date, tag, final commit, and attachment filenames | Implemented; use the date and names below, and tag the commit finalizing these notes |
| Package and publish the dataset release | Active; create and verify the dataset-only ZIP, then publish through gh |

## Approved release scope

Codex selected the descriptive date tag `near-aleppo-2026-10-12` and release
title "Near-Aleppo — 2026-10-12" under Ben's publication authorization.
The attachments are `near-aleppo-2026-10-12.zip` and
`near-aleppo-release-notes-2026-10-12.md`. The annotated tag will identify the
commit finalizing the notes. Package files from that committed tree, never from
uncommitted working files. Upload and verify both attachments before publication.

The approved content is the October 12 draft, with its draft labels removed,
release identity filled in, and attachment references made usable on GitHub.
No dataset, generator, manuscript decision, or licensing policy changes are
part of this publication phase.

## Draft baseline and evidence

Source, development, and integration checkout:
`C:/Users/BenDe/GitRepos/MAM-basics`, a full clone on `main`. Its clean HEAD
before drafting was `a29f1c08924cb9ab01fe7952257fc8df615ebdbf`. The interpreter
is `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`; commands run
from that checkout's root. Codex owns this draft's integration.

The current candidate's dataset and pages were checked at that exact commit.
It is a content baseline, not a selected final release commit: release-notes
edits and any later product changes must be reconciled before tagging.

Before this release, GitHub's release and tag-ref APIs returned no releases or
tags, verified again on 2026-10-12. The first announcements were made on 2026-10-06,
so comparisons use the reconstructed anchors recorded in the October 7 draft:

| Comparison | Commit |
| --- | --- |
| Dataset and documentation first announced at 9:06 a.m., New York time | `a287e556b2626533ed8710108e546da7a60b3fcf` |
| NAEE first announced at 4:35 p.m., New York time | `429e452e8d4b72bf702c0cf996f641bdeaa89f87` |
| October 7 dry-run candidate | `2f3013113b3c2abfa23a7cea30bb10b4eb5c441d` |

These boundaries do not establish the exact Pages deployment served to the
announcement recipients. The note-content migration was already in the
afternoon anchor, so the new notes compare the dataset with the morning anchor.

The maintained [build guide](near-aleppo-build.md),
[dataset README](../out/near-aleppo/README.md), and
[documentation edit status](near-aleppo-doc-edit-status.md) explain the current
implementation. The generated JSON reference's searchable passage
"The parameters near-Aleppo adds" reports 1,552 changed notes. A fresh read of
`in/near-aleppo/doc-note-review.json`, fields `review.proposed_parts.near_clause`
and `review.presentation`, gives 1,047 notes with an NA-adjusted clause and
505 notes retaining complete MAM context. The `qere_without_ketiv_counts` and
`qere_without_ketiv_sites` fields of `in/near-aleppo/build-populations.json`
give three marks-with-space sites, one marks-without-space site, and five
space-without-marks sites; the draft names all nine.

Endpoint inspection from the October 7 candidate covered the book JSON changes,
including carrier-template renames, parameter removal, explicit pointed-ketiv
structures, qere-without-ketiv additions, 2 Kings 14:7, and 1 Kings 8:11.
Manuscript images were not independently reread for this draft. Its manuscript
discussion attributes the existing recorded readings and MAM notes.

## Verification for the draft

On 2026-10-12 the focused command passed:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_near_aleppo.py --check
```

It confirmed all five census files, all 1,552 changed-note reviews, the 24 book
files, `build-populations.json`, and the generated pages and font copies were
current. It wrote no products, and the checkout remained clean before drafting.
The new Markdown received a read-only factual review. Its UTF-8 encoding,
LF endings, State lines, relative links, and published-page link targets and
anchors passed local checks. The existing prose mark-order lint passed
(`py/main_test.py py/tests/test_prose_mark_order.py -q`: one test passed).
The full mega and suite are deferred to the nightly cadence in
`doc/review-trial.md`; this phase changes Markdown only.

## Publication sequence

Keep `AGENTS.md`, `doc/review-trial.md`, `doc/near-aleppo-build.md`, and the
iterative-document-editing and Hebrew-prose skills as the controlling instructions.
Read the Near-Aleppo privacy criteria before any public prose draws on private
evidence. No new manuscript interpretation or data policy is part of this release.

Reverify the checkout and reconcile the draft with the chosen candidate. Repeat
the focused command above at the final content commit if products or their inputs
move. Treat any failing check or unexplained product diff as unfinished work.
Commit release preparation on `main`; fetch and merge `origin/main` before a
normal push, with focused checks for any incoming changes.

The dataset-only ZIP scope comes from the October 7 draft's "Release contents
and remaining work": `README.md`, `LICENSE.md`, and exactly the 24 `plus/*.json`
files from `out/near-aleppo/` at the selected commit. Verify its member list and
file contents against that commit before attaching it. Keep notes as a separate
release attachment. HTML, crops, fonts, and review records stay outside the ZIP.
No maintained packaging command exists yet; prepare the archive from the chosen
commit after its name and tag are settled.

Publish only after Ben's release-notes editing is complete. Record the selected
commit and tag, attachment names, archive verification, and GitHub release URL
here in the same phase commit. Tags and GitHub releases are outward-facing acts;
replacing published assets would be a separate act. The current Markdown-only
draft changes no declared product; the eventual ZIP distributes
`out/near-aleppo/`, which `py/product_scopes.py` declares as distributed data.
