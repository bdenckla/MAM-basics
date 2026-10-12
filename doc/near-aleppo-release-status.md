# Near-Aleppo release record

State: executed 2026-10-12; release published and attachments verified

Ben requested on 2026-10-12: "Let's make a Near-Aleppo release" and
"Before we release, I will likely want to edit the release notes". Codex prepared
[release notes](near-aleppo-release-notes-2026-10-12.md) for that editing step.
The [October 7 dry run](near-aleppo-release-notes-2026-10-07-draft.md) remains
the historical draft and packaging proposal.

Ben approved publication on 2026-10-12: "Great, let's make that draft official
and do whatever else is needed to make the release." Codex published
the release through `gh`; no web GUI step remains.

## Cumulative revision ledger

| Requirement | Disposition |
| --- | --- |
| Draft fresh notes from the October 7 sketch and subsequent records | Implemented 2026-10-12; the new draft describes the current dataset and pages |
| Give Ben an opportunity to edit before release | Implemented; Ben accepted the draft and authorized publication on 2026-10-12 |
| Include the current note and carrier contracts and qere-without-ketiv work | Implemented; measured against the current reviewed ledger and build populations |
| Select the release date, tag, final commit, and attachment filenames | Implemented; the annotated tag identifies commit 11740c303f0e74137fc82ed3004caeb65a82e03a |
| Package and publish the dataset release | Implemented 2026-10-12; the published release and both attachments are verified below |

## Approved release scope

Codex selected the descriptive date tag `near-aleppo-2026-10-12` and release
title "Near-Aleppo — 2026-10-12" under Ben's publication authorization.
The attachments are `near-aleppo-2026-10-12.zip` and
`near-aleppo-release-notes-2026-10-12.md`. The annotated tag identifies the
commit finalizing the notes, `11740c303f0e74137fc82ed3004caeb65a82e03a`.
Both attachments were built from that committed tree and verified before
publication.

The approved content is the October 12 draft, with its draft labels removed,
release identity filled in, and attachment references made usable on GitHub.
No dataset, generator, manuscript decision, or licensing policy changed in
this publication phase.

## Draft baseline and evidence

Source, development, and integration checkout:
`C:/Users/BenDe/GitRepos/MAM-basics`, a full clone on `main`. Its clean HEAD
before drafting was `a29f1c08924cb9ab01fe7952257fc8df615ebdbf`. The interpreter
is `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`; commands run
from that checkout's root. Codex performed integration and release publication.

The draft's dataset and pages were checked at that exact commit. Release
execution began at clean `main` commit
`5377432afb7de7cf3ff2ab8429ac1c944b43f8ab`, with `origin/main` at the same commit.
The publication phase changed only the notes and this record; the selected
release commit retains the checked products.

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
The focused check was repeated successfully for publication at preparation HEAD
`5377432afb7de7cf3ff2ab8429ac1c944b43f8ab`. The official notes passed the same
Markdown checks and prose mark-order lint. The full mega and suite were skipped
for these Markdown-only changes, following the nightly cadence in
`doc/review-trial.md`. Archive verification supplied the release-specific checks.

## Published release and attachment verification

The [Near-Aleppo release](https://github.com/bdenckla/MAM-basics/releases/tag/near-aleppo-2026-10-12)
is published as GitHub's latest release, with `draft=false` and `prerelease=false`.
Its release ID is `410891594`. The annotated tag object is
`bdd5ecfc815c6c3533a9d9bba1ffe7f2414041ea`; GitHub's peeled tag resolves to
`11740c303f0e74137fc82ed3004caeb65a82e03a`, the selected source commit.
The GitHub release body exactly matches the committed official notes.

The ZIP has exactly 26 regular files: `README.md`, `LICENSE.md`, and the 24
`plus/*.json` files from the selected commit's `out/near-aleppo/` tree.
It contains no extra files, directories, duplicate members, HTML, crops, fonts,
or review records. CRC validation and JSON parsing passed. Every member was
compared byte for byte with its committed Git blob; a separate read-only agent's
independent audit confirmed the same result. The notes attachment exactly
matches the committed official Markdown file.

Fixed before upload: the initial Git ZIP export changed `LICENSE.md` from
624 bytes with LF line endings to 634 bytes with CRLF line endings. That archive
failed the byte gate and was never uploaded. The final ZIP was built directly
from Git blob bytes, preserving the committed line endings.

Both attachments were uploaded to a temporary draft release, downloaded into
a fresh scratch directory, and reverified before `gh release edit` published
the release. The published API response retained the verified sizes and digests:

| Attachment | Bytes | SHA-256 |
| --- | ---: | --- |
| `near-aleppo-2026-10-12.zip` | 2,032,708 | `e1da8e483e9da462c6d889811be251ff7b993a108b535f62b6097bf5080be74b` |
| `near-aleppo-release-notes-2026-10-12.md` | 8,808 | `998a0f578f02c75f40285f9bc27716367ebc909211f993720b595ef07281859d` |

Tags and GitHub releases are outward-facing acts, authorized by Ben's release
request above. The source edits changed no declared product; the ZIP distributes
`out/near-aleppo/`, which `py/product_scopes.py` declares as distributed data.
Published-asset replacement or tag rewriting would be a separate act.
