# Remediate the September 26, 2026 dual-agent review of MAM-basics

State: live; detailed plan drafted 2026-09-28; awaiting approval of concrete wording and execution.

Prepared by Codex on 2026-09-28, New York time. Ben instructed: "Continue the review
process. I think in the narrow sense, the review is done, but next comes remediation, or
whatever is needed to prepare for remediation". Ben approved the complete disposition
package on 2026-09-28 by replying "I approve", and separately authorized review-branch
backup pushes by replying "yes you may push". Those approvals are recorded in
[the September 26 review's live update](dual-agent-review-2026-09-26-turn-01-claude-update.md),
anchor "Ben approved the complete dispositions and branch backup, 2026-09-28".

The dispositions are approved. The concrete editorial replacements and execution in this
plan still require approval under [the periodic-review procedure](periodic-review.md),
anchors "Close-out: from findings to dispositions" and "Separate defects from editorial
proposals" (D7). Preparing or committing this plan does not implement its changes.
An approval of this plan authorizes the stated repairs, including the explicitly identified
pinned change-log correction, but does not select any deferred semantic or policy choice.

## Standalone executor contract

Use the existing development checkout
`C:/Users/BenDe/.Codex/worktrees/dar-2026-09-26/MAM-basics`, branch `dar-2026-09-26`.
The primary integration checkout is `C:/Users/BenDe/GitRepos/MAM-basics`, branch `main`.
The root executor owns final integration. Keep one writer in the development checkout;
sub-agents may investigate and check read-only. Do not create a replacement checkout or
switch the review branch to a new feature branch. The Git worktree lock remains in force
through remediation and integration; cleanup belongs to a separate task after this task ends.

The required preparation baseline is
`8ab079afbac0a6648385f725e51057c2f0fd293f`. It contains the approved package at
`572fa2aba1696c3afc7a6bfc56628fa2c559e168` and the merge of primary `main`
`85cb7acd8df98089614de8e3e30bb67bc5a2c36a` at
`d13270a056ba14424600c1da84ab728f4728f4b2`. Require that baseline, and the commit
containing the approved version of this plan, to be ancestors of the execution HEAD.
The original reviewed endpoint remains `f4d81285` and its start remains `71f96ca3`;
these are historical review anchors, not the development baseline. The later `main`
changes are already part of the baseline and must not be reimplemented.

All relative source and output paths below are relative to the development checkout.
Every Python, generator, formatter and test command below runs with that checkout as cwd,
using the shared interpreter
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`. Never copy or link the
primary virtual environment. Sibling paths resolve through Git common-directory metadata;
no `REPOS_ROOT` override is needed for this managed checkout.

Before editing, load the development checkout's `AGENTS.md` and these live skills and
their task references: `codex-worktree-tasks` (runtime and lifecycle),
`iterative-document-editing`, `mam-repository-topology` (repository maintenance),
`github-issues` (citations, reading/writing, MAM-basics trackers), and `hebrew-prose`
(core rules, MAM-basics, rendered prose). Read `holman/WORKFLOW.md` before its assets or
records; read the applicable `doc/boj-*.md` before book-of-Job code. Never change a live
deployed instruction or skill copy. Canonical copies are under `dot-Codex/` and
`dot-claude/` in the development checkout.

Verify the exact checkout, HEAD, branch and clean status before every edit phase. Use
NUL delimiters for programmatic filename output. The following are separate PowerShell
commands; use the exact per-command `safe.directory` for elevated Git too.

```powershell
git -c safe.directory=C:/Users/BenDe/.Codex/worktrees/dar-2026-09-26/MAM-basics -C C:/Users/BenDe/.Codex/worktrees/dar-2026-09-26/MAM-basics rev-parse --show-toplevel
```

```powershell
git -c safe.directory=C:/Users/BenDe/.Codex/worktrees/dar-2026-09-26/MAM-basics -C C:/Users/BenDe/.Codex/worktrees/dar-2026-09-26/MAM-basics rev-parse HEAD
```

```powershell
git -c safe.directory=C:/Users/BenDe/.Codex/worktrees/dar-2026-09-26/MAM-basics -C C:/Users/BenDe/.Codex/worktrees/dar-2026-09-26/MAM-basics branch --show-current
```

```powershell
git -c safe.directory=C:/Users/BenDe/.Codex/worktrees/dar-2026-09-26/MAM-basics -C C:/Users/BenDe/.Codex/worktrees/dar-2026-09-26/MAM-basics status --porcelain=v1 -z
```

```powershell
git -c safe.directory=C:/Users/BenDe/.Codex/worktrees/dar-2026-09-26/MAM-basics -C C:/Users/BenDe/.Codex/worktrees/dar-2026-09-26/MAM-basics merge-base --is-ancestor 8ab079afbac0a6648385f725e51057c2f0fd293f HEAD
```

Fetch `origin` normally, verify the primary checkout is clean on `main` and agrees with
the fetched default-branch history, and merge primary `main` into the review branch
before a close-out edit task. Stop for unexpected HEAD movement, another writer's files,
missing source material, a non-fast-forward remote update or an unexplained output diff.
Do not amend, rebase, force-push, reset, discard files, retire documents or remove branches.

## Reader-facing documents: concrete approval surface

These replacements correct factual statements or implement the approved dispositions.
The retained post-stress-meteg pages use their deliberate plain "word" terminology.
Caption locators are page identifiers, and none of the changes below adjudicates a new
manuscript reading. Copy pointed Hebrew from the current repository source without
Unicode normalization. Formatting and link changes are identified separately from prose.


| Finding and current source anchor | Current wording or behavior | Proposed wording for approval |
|---|---|---|
| 21, `MAM-simple/doc/reading-mam-simple-xml.md`, "Four marks come first" | Four marks are listed, omitting U+05C9. | "Five code points have priority: shin dot (U+05C1), sin dot (U+05C2), dagesh/mapiq/shuruq dot (U+05BC), dagesh ḥazaq (U+05C9), and rafe (U+05BF). The two dagesh code points have the same priority and retain their relative order. Every other mark keeps its relative order." |
| 21, same guide, "Only those four marks" and "agreement on the four marks" | A four-mark description and unrestricted SBL attribution. | "Only those five code points have a declared priority." Use "agreement on those priorities". Replace the SBL attribution with "The existing combining-class values are attributed to the SBL Hebrew Font recommendation; the repository assigns U+05C9 the same priority as U+05BC." The SBL manual was not inspected for this plan. |
| 22, `aleppo/doc/reading-mam-simple.md` and `cam1753/doc/reading-mam-simple.md`, "The exceptions are these" | The introduction says the exceptions occur in books neither stream covers. | "The reader has the following exceptions to that grouping:" Add "Where a `<kq>` qere ends in a maqaf, the reader keeps the ketiv as a separate entry rather than joining it to the following atom. This occurs in the retained streams at Job 7:1, 9:30 and 41:4." Add "An `<implicit-maqaf/>` contributes no character and does not join the surrounding entries. Whether such pairs should be joined remains deferred." |
| 22, XML guide, "The three cantillations" | "The three cantillations: `<cant-all-three>`"; "giving three cantillations of the same consonantal text"; combined form described as containing the marks of both. | "Dual cantillation: `<cant-all-three>`"; "giving two strands and their combined representation of the same consonantal text"; "Wherever it appears, `<cant-combined>` is a combined representation of the two strands; it need not include every mark of each strand." Keep element names and the existing strand selection. |
| 22, `evr-ii-b-55/README.md`, "the text with the marks of both strands" and "One defect remains" | The combined representation is overstated and the child-reader defect remains recorded as unfixed. | Use "the combined representation of the two strands". Only after the reader differential passes, replace the defect paragraph with "The defect found on 2026-09-26 was fixed on [actual execution date]: `get_verse_words` now reads the child form of `<kq-trivial>` at Psalms 10:5, preserving the second atom and its legarmeh. No current index record reaches Psalms 10, so this fix changes no tracked locator record." Fill the actual date after execution. |
| 24.2, XML guide, "three encodings of each parashah break" | The claim treats within-verse breaks as having start/end attributes too. | "For a break between verses, MAM-simple provides a free-standing element and the adjacent verses' `starts-with-sampe` and `ends-with-sampe` attributes. A break within verse text has its element inside the verse, without corresponding start/end attributes." Correct the existing hazard-audit update to distinguish this guide defect from the valid adjacent-verse rule in the embedded notice. |
| 24.3, `doc/scan-pages.md`, "The Aleppo and Cambridge entry indexes" | Two entry indexes are named and "All three files" becomes misleading after EVR joins the inventory. | "The Aleppo, Cambridge and Evr. II B 55 entry indexes use the same `{header, body}` contract; their format-specific fields are documented in `aleppo/README.md`, `cam1753/README.md` and `evr-ii-b-55/README.md`." Replace "All three files" with "These entry indexes". |
| 24.5, `MAM-parsed/README.md` and `MAM-simple/README.md`, first "spacing around narpas" | The abbreviation precedes its definition. | "spacing around narpas (narrow-sense paseq, ׀)." Remove the repeated later parenthetical definition, retaining the grouping rule. The Aleppo/Cambridge guides already gloss their first use. |
| 25, `py/mb_diff_mpu/mpplus_index.py`, missing old date; `mpplus_subtitle.py`, missing date cells | "Release spanning  to ..." and empty date cells. | Use "Release to {name}" when the old state has no date; leave dated headings intact. Use "Not dated" in missing-date cells, including the Hebrew-date row, without `dir=rtl` on that English cell. Tree identifiers remain undated. |
| 25, `gh-pages/MAM-with-doc/change-log/releases.json`, `_header` | "of commits in the MAM-parsed repo." and `main_diff_mpplus.py`. | "of MAM-parsed states identified by historical MAM-parsed commits or MAM-basics refs." and `py/main_diff.py mpplus`. Old/new/name values remain unchanged. |
| 28, `py/author_misc/he_ws_intro_to_mam_gaya_text.py`, `_TITLE`, `_H1_CONTENTS`; corresponding site/misc labels | "געיה marks in MAM" | "The געיה marks in MAM"; retain the existing formatting substitutions in the H1. Add the same "The " prefix in `py/author_site/site_data.py` and the misc-index label. The three generated pages are the root index, misc index and translation page. |
| 28, translation note, "The heading of the section that contains this one" | A shortened heading is presented as the whole heading. | "The enclosing section's heading includes [the existing excerpt], equating געיה with meteg (U+05BD)." Keep the exact existing Hebrew excerpt and `$gaya`/`$meteg` formatting; identify the excerpt instead of reconstructing a larger quotation. |
| 29, `DATA-LICENSES.md`, landing-page row | "Ben's index of the documents he has written" | "links to editions and datasets of MAM, together with related studies, excerpts, reviews, and technical resources". Preserve the surrounding historical and license statements. |
| 29, `DATA-LICENSES.md`, unpublished crop row | "plus crops from Cambridge Add. 1753 and Codex Sassoon 1053"; "the published Aleppo and Leningrad crops" | "plus crops from the Leningrad Codex, Cambridge Add. 1753 and Codex Sassoon 1053"; "the published post-stress-meteg crops". Keep the existing rights-holder limitation. |
| 30.1, `py/author_site/post_stress_meteg_appendices.py`, paragraph beginning "The maintained meteg-after-silluq register"; `post_stress_meteg.py`, paragraph beginning "The comprehensive meteg-after-silluq page" | Each paragraph promises material its target does not provide. | Delete each entire paragraph node. Do not replace the promises with a new research claim. |
| 30.5, `post_stress_meteg_post_silluq_page.py`, "first table" | Two references become ambiguous after the register precedes the catalogue. | "The abbreviations and codes in the Breuer and Dotan catalogue are decoded below:" and "Further notes on the Breuer and Dotan catalogue:". |
| 30.6, same module, "Early silluq in L & A?" | Manuscript abbreviations enter a heading before being clear. | "Early silluq in Leningrad and Aleppo?" |
| 30.8, same module, "phonetic-hbo #78" | Spaced cross-tracker citation. | "phonetic-hbo#78"; retain its current URL. |

### Formatting, source links and caption locators

For finding 30.7, add `.book-title { font-style: italic; }` to the authored deploy-root
`gh-pages/style.css`. The five existing spans italicize; their text is unchanged.

For finding 30.2, correct both the clickable crop and its caption source link for these
four EVR figures through explicit `source_url` arguments to `_petersburg_crop`.
The retained volume-2 record is
`https://www.nli.org.il/en/manuscripts/NNL_ALEPH990000991240205171/NLI?volumeItem=2`;
its fragment is `#$FL` followed by the file id in this table. These identifiers come
from the retained local image records; the plan performs no new manuscript adjudication.
Keep the existing good 1 Samuel 17:5 and 1 Kings 14:14 source links.

| Figure | Digital image | NLI file id |
|---|---|---|
| Psalms 60:10 | 623 | 48719462 |
| Psalms 70:2 | 632 | 48719471 |
| Psalms 72:15 | 634 | 48719473 |
| Job 4:12 | 714 | 48719553 |

For finding 30.3, make only these locator substitutions in the shared caption source and
corresponding maintained records. The surrounding caption, source URL, rights statement
and interpretation remain unchanged. Ben already selected "digital page" for Cairo.
The explicit `F` in the proposed Leningrad forms is presented here for wording approval;
it is not retroactively attributed to Ben's earlier quotation.

The matching maintained record paths are `doc/meteg-after-silluq-snips/README.md`,
`doc/meteg-after-silluq-psalms-72-15.md` and
`doc/meteg-after-silluq-job-4-12-update.md`. Apply the same substitutions where
those locators occur. Preserve physical folio-count/pair/recto-verso explanations,
catalog quotations, existing data fields and filename spellings. `aleppo/README.md`'s
"270r is leaf 270 recto" explains the physical side and may remain beneath its
already correct page-ID definition. In the snips README, replace "The page is a
leaf in `{leaf_number}{r|v}` form" with "The manuscript page identifier is
`{leaf_number}{r|v}`, as in `270r`." Replace "The page is a folio and side, as in
`430B`" with "The manuscript page identifier combines the folio number and side,
as in `F430B`." In that same Leningrad paragraph, use "every manuscript page
identifier" and "from a page identifier to an image" for the entries in the
mirrored index, preserving its dated count of 982.

The three additional side-lettered EVR identifiers in existing snips source notes
change only their locator label: "folio 303a" → "page 303a", "folio 308b" →
"page 308b", and "folio 348b" → "page 348b". These are recorded identifiers;
do not add any of them to a caption that currently has no locator or reinterpret
the physical folio-pair explanation.

| Figure | Current locator | Proposed locator |
|---|---|---|
| Cairo, 1 Samuel 17:5 | manuscript page 110, digital image 103 | manuscript page 110, digital page 103 |
| Aleppo, 1 Kings 14:14 | leaf 83r | page 83r |
| Leningrad, 1 Kings 14:14 | folio 195B, column 2, line 27 | page F195B, column 2, line 27 |
| Cairo, 1 Kings 14:14 | digital image 204 | digital page 204 |
| EVR, 1 Samuel 17:5 | folio 57a, column 2, line 7 (digital page 120) | page 57a, column 2, line 7 (digital page 120) |
| Aleppo, Psalms 60:10 | leaf 251r | page 251r |
| Leningrad, Psalms 60:10 | folio 377B | page F377B |
| Aleppo, Psalms 70:2 | leaf 253r | page 253r |
| Leningrad, Psalms 70:2 | folio 379B | page F379B |
| Aleppo, Psalms 72:15 | leaf 253v | page 253v |
| Leningrad, Psalms 72:15 | folio 380A, line 3 | page F380A, line 3 |
| Aleppo, Job 4:12 | leaf 271r, column 2, line 5 | page 271r, column 2, line 5 |
| Leningrad, Job 4:12 | folio 398A | page F398A |

Keep the four conforming locators: Cairo 1 Kings 7:37's digital page 186; Leningrad
1 Samuel 17:5's F159A, column 3, line 8; EVR 1 Kings 14:14's digital page 186,
column 1, lines 18–19; Cambridge Job 4:12's page 0073B, column 2, line 13. The
17 manuscript captions without a locator stay without a new locator, including all
seven Sassoon captions. The complete seven-case inventory is 34 manuscript figures
plus the main register's one URJ figure. This dated measurement uses the current
shared crop declarations; recount after regeneration by enumerating those declarations
and the figures in the seven case pages. Shelfmark spelling remains deferred.

### Historical links and retained manuscript labels

Finding 3.1 replaces `in/mam-ws-intro/README.md`'s live path to the retired
mega-coverage plan with: "`git show --stat 985262e2` names every file removed.
Phase 3 of the [retired mega-coverage plan](https://github.com/bdenckla/MAM-basics/blob/f72297084ab94aea6fd1274dc1bc3d7ce6acddd5/doc/PLAN-mega-coverage.md)
records the totals." Use that same complete-family historical commit at the surviving
topology reference, `py/repo_scopes.py` and `py/subcommands/download_wikisource_intro.py`.
The removed `py/ac_paths.py` example is already resolved.

Finding 3.3 corrects the two maintained references in
`doc/meteg-after-silluq-psalms-72-15.md`, anchors line 3 and "The complete run":
replace "is recorded ... `doc/PLAN-meteg-after-silluq-in-uxlc-and-wlc.md`" with
"was recorded in the [retired complete-run plan](https://github.com/bdenckla/MAM-basics/blob/f72297084ab94aea6fd1274dc1bc3d7ce6acddd5/doc/PLAN-meteg-after-silluq-in-uxlc-and-wlc.md)".
Preserve the rest of each passage. This report is maintained by Ben's approved
reclassification; it is not reverted to a receipt.

Finding 18.8 changes `cam1753/doc/cam1753-line-break-task.md`'s heading "Pages
completed" to "Verse labels in the retained line-break files" and inserts:

> The table reports the first and last verse-marker labels in the retained JSON files,
> not independently verified manuscript ranges. "Fragment" means a stored
> verse-fragment-start or verse-fragment-end marker. The stored data is unchanged.

Replace the existing sixteen rows with this finite transcription of the retained labels.
Write "fragment" and "verse-start" in the table rather than the shorthand below.

| Page | First label | Last label |
|---|---|---|
| 0072B | Psalms 149:7, fragment | Job 1:16, fragment |
| 0073A | Job 1:16, fragment | Job 3:5, fragment |
| 0073B | Job 3:5, fragment | Job 5:2, fragment |
| 0074A | Job 5:2, fragment | Job 6:15, fragment |
| 0074B | Job 6:15, fragment | Job 8:6, fragment |
| 0075A | Job 8:6, fragment | Job 9:30, fragment |
| 0075B | Job 9:31, verse-start | Job 11:18, fragment |
| 0076A | Job 11:19, verse-start | Job 13:17, fragment |
| 0076B | Job 13:17, fragment | Job 15:9, fragment |
| 0077A | Job 15:9, fragment | Job 16:16, fragment |
| 0077B | Job 16:16, fragment | Job 19:2, fragment |
| 0078A | Job 19:3, verse-start | Job 20:17, fragment |
| 0078B | Job 20:17, fragment | Job 21:32, fragment |
| 0079A | Job 21:32, fragment | Job 23:14, fragment |
| 0079B | Job 23:14, fragment | Job 26:10, fragment |
| 0080A | Job 26:10, fragment | Job 28:16, fragment |

Add the caveat:

> At 0075A/0075B, 0075B/0076A, 0077B/0078A, and 0080A/0080B, the earlier file
> ends with a fragment-end label and the next file starts with the following verse's
> verse-start label. These stored markers do not provide a consistent description of
> verse continuation across pages. The table displays the labels without resolving
> the manuscript boundary.

The adjacent 0080B starts with Job 28:17; it supplies the caveat, not an extra table row.
Before editing, independently extract the first/last verse markers from the sixteen
`cam1753/cam1753-line-breaks/` JSON files and the first from 0080B. This is a data
comparison, not permission to alter the stored markers or inspect new manuscript material.

In `cam1753/README.md`, "Conventions", add: "Preserve the stored Hebrew data exactly.
Do not normalize it. Repository mark-order and Latin NFC checks include this tree; the
image terms are recorded in `cam1753-spreads-provenance.md`
and `../DATA-LICENSES.md`." Author those two links relative to the
README, using `cam1753-spreads-provenance.md` and `../DATA-LICENSES.md`; these names
are replacement source text rather than plan-relative links. Then remove the redundant `cam1753/CLAUDE.md`
instruction body. Its false claim that no Python reads the tree is not transferred.

Finding 19 changes `aleppo/doc/aleppo-line-breaks.md`, anchor "The check's MAM-simple
sequence comparison ignored meteg and rafe", to: "The check's MAM-simple sequence
comparison omitted U+05BD and U+05BF and no other code points. U+05BD serves as either
meteg or silluq; U+05BF is rafe. `no_marks_comparison_key` was narrowed to those code
points on 2026-09-08, in `c76239a5`." Preserve the following punctuation, format-character
and no-normalization claims. The comparator and consumers were retired at `65f5a1c6`;
this repairs the historical description without restoring their code or regenerating
the frozen comparison.

### Maintained research and index-document corrections

| Finding and current anchor | Current wording | Proposed wording |
|---|---|---|
| 31.2, `doc/meteg-after-silluq-snips/README.md`, opening crop inventory | "thirty-one manuscript crops"; "twenty-seven" fuller notes | "The seven post-silluq case pages publish thirty-four manuscript crops under `gh-pages/img/`; thirty have fuller source notes below. The main post-silluq page publishes the URJ printed-edition crop, which also has source notes here." Distinguish the figure population from all tracked PNGs. |
| 31.7, same README, Cairo/Sassoon 1 Kings 14:14 | "verse-final word" | "verse-final chanted word". This is research prose; retain the plain "word" convention on the rendered post-stress-meteg pages. |
| 31.4, maintained Psalms 72:15 report, summary item 8 | "ch. 8 §46, footnote 81" | "ch. 8 §47, footnote 54 (p. 355 in the Wengrov English translation)". Keep the source claim narrow to the reference already checked in the review. |
| 34.2, `evr-ii-b-55/README.md`, descriptions of line fields | "first"/"second" wording fails to name the fields. | "`de_text_at_line` gives the verse's atoms on one line; `de_text_at_line_ref` names that line and, on a three-column page, its column." |
| 34.2, same README, lead on estimated positions | Attribution conflates the estimating sessions with later recount/reproduction. | "Two sessions estimated page positions; the findings sub-agent recounted the Prophets' rates, and the image-list session reproduced the recount." |
| 34.2, same README, Psalms/Job/Proverbs heading | "Segmentation of these books" | "Segmentation of Psalms, Job and Proverbs". |
| 34.1, `doc/post-stress-meteg-method.md`, two census passages | "each occurrence carrying one meteg"; "135 chanted words carrying two meteg marks" | "Twenty-one of those 143 were one form counted against itself; each occurrence has one meteg. The MBS_O population was therefore ..."; "its tracked output had 135 chanted words that have two meteg marks". Retain the rest of the clauses and historical numbers. |
| 34.5, maintained Psalms 72 report and snips README | "Codex" ambiguously names the agent. | Use "the Codex agent" for the agent; preserve the full manuscript names. Apply the same clear attribution in new updates. |

Finding 31.5 corrects only `in/meteg_after_silluq_koren_readings.json`'s final `about`
sentence: "The tracked post-silluq generator reads this list through
`load_post_silluq_koren_observations` to construct the K masks for 1 Kings 7:37 and
Job 4:12." Values and classifications stay unchanged. This explanatory JSON change
does not change Scripture or manuscript-observation data.

For the dated image-provenance records, put later facts in updates, not the finished
base. The new `doc/post-stress-meteg-image-provenance-update.md` says: "The 1 Kings
14:14 EVR figure now applies a focus-of-attention fade with a luminance mask, four
cutouts and an `rgb(184,184,184)` tint. The tracked PNG remains the byte-identical
source crop; the fade changes presentation only." Its inventory distinguishes six
initial crops from 31 added during the review window; four of the 31 were moved
preexisting crops, 30 appear on the seven case pages, and the URJ crop appears on
the main register. Include the twenty-name mapping below with the actual rename date.

The new `evr-ii-b-55/evr-ii-b-55-images-provenance-update.md` corrects the
directory-wide claim: "No image is tracked in the `evr-ii-b-55` directory. Six crops
of this manuscript are tracked under `gh-pages/img/`." Keep both provenance bases'
original State/header and add only their permitted update pointers.

## Distributed data and published change-log effects

Finding 24.1 removes this exact rule from the canonical parsed-plain notice only:
"A special-letter template's interrupted spelling and uninterrupted atom-form are
two representations of one atom-form; select one text representation rather than
collecting both." Parsed-plus retains that rule. In both notices, move the existing
NARPAS definition before WHITESPACE so the abbreviation is defined before use;
leave both rule strings unchanged. The change is in
`py/mb_cmn/public_data_consumer_notice.py`, `mam_parsed_notice`.
The MAM-simple adjacent-verse rule is already true and stays unchanged. Add the EVR
entry index to canonical notice coverage and lint its existing notice; extend coverage
to the existing UXLC XML derivative. Their present notices are expected to be identical
after regeneration, while parsed-plain and parsed-plus header notice rules change.
Regenerate all 24 current book files in each of `MAM-parsed/plain/` and
`MAM-parsed/plus/` through `py/main_parse.py ws`, then run the hand-run
`py/main_authored.py gen-mam-parsed-docs`. The latter is not a mega step and must
update `gh-pages/MAM-parsed/plain/html/mpplain.html` and
`gh-pages/MAM-parsed/plus/html/mpplus.html` to match the canonical notice.
Other generated documentation, claims and CSS are expected to be unchanged.
Strip only the
notice metadata for an independent before/after payload comparison: every Scripture
body value, index body, and existing schema field must match the baseline. Do not
regenerate removed Google Sheet products or change historical source captures.

Add canonical EVR documentation URL
`https://github.com/bdenckla/MAM-basics/blob/main/evr-ii-b-55/README.md#consumer-guide`
and extend `py/tests/test_public_data_consumer_notices.py` to cover the existing
`evr-ii-b-55/evr-ii-b-55-page-index.json` notice and
`uxlc/out/UXLC-misc/lci_recs.xml`. The existing indexed files are `in/lci_recs.json`,
`aleppo/aleppo-wiki/index-flat-corrected.json`, `aleppo/index-flat-annotated.json`,
and `cam1753/cam1753-page-index.json`. All index bodies and the 35 MAM-simple
JSON plus 35 XML notice-bearing book files are expected to stay byte-identical.

Finding 22 repairs `py/mb_cmn/mam_xml_verses.py`'s omission of a recognized
`<kq-trivial>` child form. Support both current known shapes with explicit shape
validation and named child handling. Preserve the same Scripture/alternative
projection already selected by the reader; reject unknown elements or shapes.
An independent full-corpus XML walk compares the reader's actual atom sequence and
marks with the selected source nodes. The real Psalms 10:5 child content must no
longer disappear. Existing index streams do not reach that verse, so all retained
Aleppo/Cambridge/EVR index and line-break JSON is expected to remain unchanged.
Their stream makers were retired; do not resurrect or run the retired generators.

In that same reader, rename `_CANT_STRANDS` to `_CANT_FORMS` and `_strand_words`
to a matching form name. Replace "all three strands" and both "has the marks of
both" descriptions with two strands and their combined representation, using the
concrete guide wording above. A combined representation need not include every
mark of each strand. Keep Ben's existing combined-form selection exactly.

### Explicit proposed pinned-release remedy for finding 25

The proposed act corrects published report receipts. After the code fix, regenerate
all six named change logs at their existing `old`, `new`, and `name` values, together
with unpinned-latest and the index. This plan's execution approval must explicitly
cover those pinned files. Preserve `2026-09-17` as the release name; the release
naming/date convention in 25.4 remains deferred. No MAM Scripture payload changes.

The affected generated set is
`gh-pages/MAM-with-doc/change-log/{2025-03-19a,2025-03-19b,2026-03-06,2026-03-16,2026-04-14,2026-09-17,unpinned-latest}.{html,json}`
and `index.html`. Detection must distinguish real qere/alternative changes from
the five pointing migrations, unchanged qere wrappers/old-note removal, the already
pointed Ezekiel 40:26 meteg change, and Psalms 71:9's stress-helper difference.
Never promote explanatory or wrapper text to selected Scripture. The selected
Scripture projection remains the existing explicit one.

Fix extractor detection, classifier suppression, JSON serialization and HTML
presentation together, rather than count a generic "template restructured" card as
a useful repair. Keep combining marks anchored to their base character inside a
single highlight span. Add no raw orphan combining literal to tracked code.

The independent oracle compares recognized parameter alternatives across every
registered real release pair, separately from the existing selected-text projection.
It must report missing or extra changes by verse/template/alternative, and fail on
missing input or an empty release population. Use closed dispatch for recognized
templates and parameters; generic recursion into all template parameters is not
an alternative-policy definition. Do not add example-based tests pinning the
selected omitted verses. Regenerated reports supply the published-output differential.

The concrete public schema proposal is an optional `alternative_changes` array on
each affected diff. Preserve the existing selected-text fields. Each entry contains
`template` (the canonical current family name), `occurrence` (one-based within that
recognized family in the verse), `role`, `kind`, `old`, and `new`. Traverse a recognized
`נוסח` only through its Scripture target; exclude its note parameter. Normalize the
recognized historical/current ketiv/qere shape through explicit old/new parameter
roles, excluding source prefixes and metadata. Unknown or malformed shapes raise.
The array is useful alternative data, not a claim that the selected verse text changed.

The initial role inventory is bounded to the already recognized trivial ketiv/qere
qere (historical `קו״כ-אם` and current `מ:קו״כ-אם-2`) and `מ:דחי` parameter 2's
stress-helper alternative. Other recognized templates retain existing comparison,
projection and classifications; do not invent qamats, dual-cantillation or other
alternative roles. The existing structural helper is not itself a semantic role map.
If the independent population check reveals another unresolved role choice, record
that finding for Ben rather than widening this approved remedy.

For the actual `9ce6ee5` to `cb95915` pair, the two substantive entries are:

```json
{"template":"מ:קו״כ-אם-2","occurrence":2,"role":"qere","kind":"content","old":"וְאֵֽלַמָּ֖יו","new":"וְאֵלַמָּ֖יו"}
```

```json
{"template":"מ:דחי","occurrence":1,"role":"stress-helper-alternative","kind":"content","old":"אַֽל־תַּ֭שְׁלִ֭יכֵנִי","new":"אַֽל־תַּ֭שְׁלִיכֵ֭נִי"}
```

The first occurs at Ezekiel 40:26 and the second at Psalms 71:9. The proposed
rendered paragraphs are "Qere alternative changed: [old] → [new]." and "Alternative
with the stress helper changed: [old] → [new]." Put each Hebrew value in its own
`pointed-heb` span with `dir=rtl`. These paragraphs are currently absent.

The five unpointed-to-pointed qere migrations receive the same array shape with
`role: "qere"` and `kind: "pointing-migration"`. Render "Pointing added to the qere
alternative: [old] → [new]." This explicitly discloses migration differences instead
of labeling them ordinary meteg changes. The two unchanged-qere note/wrapper changes
at Deuteronomy 13:16 and Ecclesiastes 10:10 stay suppressed from Scripture change
cards and are disclosed in the remediation update. Suppress a pure rename only after
recognized normalized content equality. Preserve the existing selected-text flattening
policy and classification of unrelated changes; the alternative role/kind supplies the
new distinction. Replace the index's misleading "{count} body text changes" with
"{count} changes" because its cards already include structural changes.

The five migration values in that real pair, all at occurrence 1 of the recognized
trivial ketiv/qere family, are:

| Verse | Old qere alternative | New qere alternative |
|---|---|---|
| Exodus 22:4 | בעירו | בְּעִיר֔וֹ |
| Exodus 22:26 | כסותו | כְסוּתוֹ֙ |
| Exodus 28:28 | מטבעתיו | מִטַּבְּעֹתָ֞יו |
| Leviticus 9:22 | ידיו | יָדָ֛יו |
| Leviticus 16:21 | ידיו | יָדָ֗יו |

These are retained source values, not newly authored Scripture. Exclude the recognized
historical `ל-קרי=` prefix from the serialized old qere value. Do not alter any source
JSON, release boundary, note, or alternative value to obtain the proposed report.

Implement the bounded additions in `mpplus_structure.py`, `mpplus_extract.py`,
`mpplus_expand.py`, `mpplus_json.py`, and `mpplus_html.py`, reusing the explicit
parameter access in `mpplus_template_change_desc.py` where appropriate. Document
the optional array in the serializer contract and report description. The execution
oracle must compare actual old/new alternative values with serialized values; successful
detection alone is insufficient. Leave unchanged qere values and all selected Scripture
fields byte-identical. Record every changed named-report count as a result, not a target.

## Remaining changes: summary and finite execution ledger

The lower-risk work changes maintained Markdown and receipt updates, comments and
docstrings, canonical agent instructions and skills, and bounded code/lints. It
corrects factual records without changing old receipt text beyond the permitted
pointer. The two exceptions needing separate attention are the GitHub issue-body
correction and final user-config deployment, both outward acts already described
below. Finished-record edits and pinned reports are harder to undo independently
of their product reach.

This ledger is cumulative. "Active" means an approved disposition with execution
still pending; it does not claim a fix has been implemented. Every numbered review
finding is covered here or by the explicit deferral ledger. Use the source review's
numbered heading as a searchable anchor for each item; turn 03 and later accepted
corrections control over the first turn's original overstatements.

| Finding | Status and exact scope |
|---|---|
| 1 | Active: correct the September 16 update's credits: 19.4 was falsely called already resolved before its actual migration/prescription/implementation sequence; 13.2 credit is `18aabf8d`; module/CSS credit in finding 14 is `4e30b0f4`, not `18aabf8d`. Keep the separate current matcher defect under finding 16. Add the September 16 plan's single update for the corresponding correction. |
| 2 | Active: replace stale pending/closing clauses in existing September 14/16 review updates and September 16 plan update. Record the historical declaration that Ben approved concrete wording on September 18 as that source declaration, not a newly verified transcript quotation. |
| 3 | Active: repair the surviving retired-plan links in the public wording section and old wlc-utils plan descriptions. Only the old `py/ac_paths.py` example was removed; the module survives. |
| 4 | Active: correct all seven record details: September 14 locators, exact CSS paragraph, first-entry date, seven historical al-hatorah citations plus the test site, duplicated MAM-basics tracker count, Unicode bidi classes, and September 17 approval provenance for endpoint-window review. None authorizes rewriting a finished base. |
| 5 | Active: refresh September 10 live-update references to retired families and current crop/Psalms report descriptions. Historical counts remain identified as dated measurements. |
| 6 | Active: repair current-guidance inbound links to retired families and adopt the exact retirement-reference rule below. Recount current references rather than reuse the review's dated 32/96 populations. |
| 7 | Active: correct the four unauthorized receipt-link edits in the new census update and repair issue 269's family link. No retrospective repinning under 7.3; five Holman evidence-note classifications stay deferred. |
| 8 | Active: add the Ben-authorized reclassification procedure below. Keep Psalms 72:15 maintained; do not reverse its approved transition. |
| 9 | Active: keep all live update files `State: open` while their bases survive. Record effective completion of the September 14 remediation plan as executed 2026-09-16 in its existing update; that date is supported by the issue 278 correction, not inferred from the filename. |
| 10 | Active: repair searchable source-passage locators in the existing update files. Quote the passage's subject or distinctive words so the correction survives line movement. |
| 11 | Active: restore 11.2–11.5's shared safeguards, evidence limits, source-update locators and long-lived backup exception in canonical instructions/skills. All twelve 11.1 legacy clauses stay deferred. |
| 12 | Active: repair surviving current section citations and instructions for future imports. Use current headings "Shell, scripts, and file operations", "Git and commits", "Show local artifacts with file links", and the separate product/act risk axes. Already deleted camguide and book-of-Job Aleppo procedures need no resurrection. |
| 13 | Active: record the existing budget reversal at `51a4120c5d08218798e023ba14b8d3dec34e2e8a`; change no budget. Produce the missing section-level reconciliation of old instructions to current common body, canonical skills/references, approved restoration, or explicit deferral. Retirement of the overtaken plan stays deferred until that mapping exists. |
| 14 | Active: replace the directory-based verification exemption with the change-type rule below, including `py/product_scopes.py`'s matching explanation. Informational lint failures in 14.3 are not a separate code defect. |
| 15 | Active: correct the canonical Wikisource-refresh skill's ordinary worktree sibling resolution, final mandatory mega and conditional full-suite cadence. Keep `REPOS_ROOT` only as an unusual-layout override. Finding 15.3 observations require no additional fix. |
| 16 | Active: fix relocated-path inbound detection using actual per-target retained locations, including absolute, primary-relative, worktree-relative and file-URL spellings with correct token boundaries. Correct the false closure credit. Verification is read-only differential/simulation; perform no real retirement. |
| 17 | Active: broaden the force-flag lint to all relevant cleanup adapters/engine and both `--force`/`-f`; keep legitimate verified cross-volume `.novc` relocation. Remove dead `CleanupReport.errors` or make its reporting contract true; distinguish `show-ref` absence from unexpected diagnostic failure; repair pointers and comments. 17.2 measurement and 17.8 prevention proposals remain deferred. |
| 18 | Active: correct `boj_paths.py`'s CRLF and top-level module claims to LF and twelve modules (eleven runnable entry points plus one library); correct historical editor count/commit credit in the retirement plan's new update; consolidate the Cambridge instruction stub as specified; replace its range table with retained labels. Dead product examples and cam1753 path inventory are already resolved by `65f5a1c6`. |
| 19 | Active: correct the surviving Aleppo comparison description as specified; retired comparator/consumers remain retired. |
| 20 | Active: replace the four added synthetic/mock freshness tests with a real registered-output differential or mechanical coverage lint, and include `style.css` and `filter.js` in freshness comparison. No claim that those assets are currently stale. |
| 21 | Active: reconcile all four-mark descriptions and U+05C9 terminology in the finite source set below; exclude U+05C9 from `clc_dual_cant._VOWEL_POINTS`. Actual MAM mark order and current Scripture stay unchanged. |
| 22 | Active: repair the child reader and guides as above. Implicit-maqaf joining remains deferred. |
| 23 | Active: remove only surviving unused code; correct stale descriptions; extend the real deploy-root geometry scan; fix the Leningrad diagnostic; enforce the already supported finite UXLC child projection. No new ketiv/qere policy. |
| 24 | Active: make the plain notice, guide, audit and notice-coverage changes above. Google JSON inventory gap already resolved by `a41fbcdd`. |
| 25 | Active: apply the explicitly proposed pinned remedy, useful alternative display, undated cells, header description and cluster-safe highlights above. Release naming/date convention stays deferred. |
| 26 | Deferred: source/revision/Holman-message date-label policy. No output or instruction change chooses it. |
| 27 | Deferred: Job 4:12 discrepancy. No new manuscript/Phonetic MAM inspection or semantic survey/text change. |
| 28 | Active: repair title/labels, excerpt attribution and all three cleanup instructions. Keep all current translation caveats and make no human-review claim. |
| 29 | Active: repair license/landing-page facts and internal link/root stylesheet descriptions. Naming, redundant dataset-stub removal and apostrophe policy remain deferred. |
| 30 | Active: make the bounded presentation, source-link and locator changes above. Shelfmark style remains deferred. |
| 31 | Active: correct existing research records, inventories and narrow source citations. Manuscript-observation report coverage and ledger links remain deferred. |
| 32 | Active: rename exactly the twenty new image slugs listed below using the current converter. Preserve bytes and update active references; preserve frozen receipt paths through one update. |
| 33 | Active: correct established figure/attribution/checkout-scope errors. Narrow unsupported Python/locale/Wikisource claims; do not declare an uninspected external source wrong. |
| 34 | Active: name the actual subjects and contributions in current prose and proper updates. Apply turn 03's narrower EVR attribution correction. |
| 35 | Deferred/no-action/already resolved individually as listed below. No new process policy or historical-act reversal. |
| 36 | Active: rename the authored CSS/JavaScript pair to `holman/assets/mam-suggestions-report.css` and `.js`, changing the two `py/py_render/rt_assets.py` source constants. Published asset names and stable HTML URLs stay unchanged; regenerate the report and require byte identity. |

### Bounded code and test work

For finding 21, reconcile the finite current passages identified in
the review: `AGENTS.md`, `doc/mam-normal-mark-order.md`, the XML guide,
`py/mb_diff_mpu/change_ops.py`, `py/check_mark_order.py`,
`py/tests/test_prose_mark_order.py`, `py/tests/test_mam_simple_mark_order.py` and
`py/mb_cmn/uni_denorm.py`, and
`py/author_misc/review_of_artscroll_transliterated_linear_siddur.py`.
Keep source comments ASCII where the user instruction requires `x` for the Hebrew
sound; use ḥ in prose/docstrings. Replace the invalid "mudgash" description of
U+05C9 with dagesh ḥazaq terminology. Do not infer a change to mark priority from the
description correction. Exclude `DAGESH_XAZAQ` from `_VOWEL_POINTS` and compare all
current dual-cantillation outputs before/after; no current corpus difference is expected.

Finding 23 has this finite surviving source set:

- Remove the unused `_hebrew_cell` import and `_case_source_mask_values` helper from
  `py/author_site/post_stress_meteg_post_silluq_page.py`.
- Correct `py/accgram/post_stress_meteg.py`'s pointer to `post_stress_meteg_survey.py`;
  `py/author_site/post_stress_meteg_validation.py`'s focus-set pointer to
  `accgram.post_stress_meteg_sources._FOCUS_VERSES` and the explanatory module to
  `author_site.post_stress_meteg`; `py/mb_cmn/paths.py`'s `_settle` pointer to
  `accgram.post_stress_meteg_sources._settle`.
- Extend `py/tests/test_scan_overlay_viewboxes.py` to collect actual deploy-root HTML
  as well as its existing `wlc/` population. Preserve the real 374×208 source PNG
  and viewBox. This is a tree lint, not a fabricated figure test.
- Replace `gh-pages/wlc/style.css`'s ochre claim with "The caller supplies the
  focus-fade tint; the 1 Kings 14:14 figure uses `rgb(184,184,184)`." Drop the unused
  `overlay_class` argument from `py/py_html/my_html_for_img.py`'s `annotated_img`
  and the unselected `post-silluq-focus-fade-overlay` class in the author module.
  The corresponding generated SVG loses that unused class only.
- Change `py/mb_diff_mpu/grapheme_diff.py`'s dependency description to "Depends on html,
  difflib and the shared Unicode-property fallback." Change the join-key comment in
  `test_final_stress_vs_phonetic_mam.py` to "What is left is letters, points and maqaf."
- Correct `py/redirect_stubs/check.py` to state that a frozen URL target may be maintained
  at its new publisher, such as hbofonts. Do not publish or regenerate redirect hosts.
- Qualify `paths.py`'s old 263,320/122,555 measurement as measured under the
  pre-Unicode-18 annotation relation; the present folding relation was not remeasured
  here. No private repository is inspected to refresh it.
- In `py/uxlc_lci/uxlc_lci_rec_to_xml.py`, change "unsupported JSON value in Leningrad
  header" to "unsupported JSON value in Leningrad index" because the helper reads
  the body too.
- Make `py/author_site/post_stress_meteg_post_silluq_data.py`'s `_uxlc_words` explicitly validate its
  supported `w`/`q` Scripture projection and raise for unsupported children. All five
  current call verses contain `w` only. Do not choose a new ketiv/qere display policy.

For finding 20, a freshness check must compare generated `style.css` and `filter.js`
alongside the registered reports and index. A conditional font absent from the generator's
temporary output is not a stale tracked artifact. Use real release inputs and outputs as
the independent differential; a mechanical source/tree coverage lint is an acceptable
alternative for the removed mock tests. Commit the source and regenerated products before
running `py/main_diff.py mpplus --check`, which checks against committed HEAD.

### Concrete policy wording

For findings 6 and 8, apply this core passage in `py/repo_util/check_repo_standards.py`
("The doc/ directory standard"), `doc/PLAN-repo-maintenance-across-GitRepos.md`
("Receipt immutability and retention are independent"), canonical topology's
`references/repository-maintenance.md` ("Manual document retirement"), and canonical
GitHub issue guidance's `references/reading-and-writing.md` (section 5). Keep the
repository/common instructions and DAR D12 consistent through a short pointer or
matching rule rather than competing definitions:

> Before deleting a receipt family, audit references in tracked files as well as GitHub
> issue bodies and comments. Classify each reference as current guidance or historical
> evidence. A current-guidance reference must reach a maintained successor or block
> deletion. A historical reference must reach the full 40-character SHA of the last
> commit whose tree contains every family member. Verify every target path there and
> link the base and its update so the correction sequence remains visible. Correct
> present-state documents and source comments in place; correct a finished receipt
> through its single live update. Do not bulk-edit finished bases. This audit and the
> retirement decision remain manual.

Preserve existing separate rules for open issue bodies, closed issues, comments,
complete read-back and requiring the archival commit to exist on `origin/main`.
Ordinary whole-family retirement remains distinct from this approved exception:

> Ben may explicitly reclassify a finished receipt family as a maintained document.
> Record Ben's decision and date, identify the original family and an archival commit
> containing every member, and preserve the research provenance and later corrections.
> If the transition consolidates the update into the maintained document, remove the
> update and its pointer in the same commit and repair current-guidance references;
> historical references retain recoverable access to the original family.
> Reclassification is separate from retirement and is never automatic.

This procedure does not authorize reclassifying another family. Ben's September 23
Psalms 72:15 decision remains valid. Use complete-family archive
`f72297084ab94aea6fd1274dc1bc3d7ce6acddd5` for the families retired by
`2a051ba509901228fbd4d62d91b73765b94a39e4`, verifying both paths before writing
each link. Approved 7.3 preserves the older `40395aa3` pins because their family
bytes match; it does not contradict the rule for future retirement links.

For finding 9, clarify the standards/runbook rule:

> While a plan is being executed, keep its State true in place and record a phase
> change in the same commit as the phase work. After the plan becomes a finished
> receipt, a later State correction goes in its update. The latest dated declaration
> of the plan's State in that update is the effective plan State; it is separate from
> the update file's own State. An update remains open while its base is tracked.

Change the symmetric-plan update's own `State: executed` to `State: open, first
entry 2026-09-15.` Its completion entry says: "The plan's effective State is
**executed 2026-09-17**. This update file remains **State: open** while the base is
tracked." The hazard update's own State likewise remains open, first entry September
16. In the September 14 plan update, record effective State **executed 2026-09-16**:
repository remediation reached `71f96ca3`, and the issue 278 body correction/comment
followed that endpoint on September 16. Keep the issue open and the bases unchanged.

For finding 11.2, add these five shared safeguards to canonical
`dot-Codex/user-wide-AGENTS.md`, "Linked-worktree safeguards shared by Claude and Codex":

> A successor continuing work in a named worktree uses that checkout directly. Create
> additional isolation only when Ben asks or concurrent editing requires it, and state
> the reason. A Claude task chip that creates a fresh worktree is the wrong handoff
> vehicle when the work must continue in a named checkout.

> Before diagnosing lost edits, refresh HEAD, task-owned status, recent commits,
> reflogs, and the relevant diffs. Compare the actual provenance before consulting
> stashes or unreachable commits; a matching path alone does not establish lost work.

> When Ben reviews a generated local page, identify and verify the exact page path,
> checkout, and commit. A worktree commit does not establish that the primary clone or
> remote branch contains the page.

> A worktree may have its own freshly created environment when its task requires
> different dependencies. State that reason; never copy or junction the primary environment.

> If the primary clone refuses the final fast-forward, return to the development
> worktree, merge the new main there, and repeat the applicable checks. Do not replace
> the failed fast-forward with a merge in the primary clone.

Make skill routing agent-specific: Codex loads `codex-worktree-tasks`; Claude follows
the shared safeguards and repository integration procedure. Preserve common integration
instructions for both. Source: old common Claude body at
`71f96ca3801863f6fa64c1fd0e75ccfde773439b`, anchors named worktree, lost edits,
exact generated page, different dependencies, and failed fast-forward.

For finding 11.3, restore this always-loaded common section:

> **A transcription is evidence about the transcription.** Attribute a finding from
> WLC, UXLC, MAM, or another transcription to that transcription. A manuscript claim
> requires an actual manuscript reading or a clearly attributed prior reading. Unless
> the image was consulted, report the manuscript as unverified rather than saying the
> manuscript has the transcription's reading. A transcription's silence supplies
> little evidence about a fine mark. When a task needs a manuscript judgment and the
> manuscript cannot be consulted, state that limitation.

Keep the fuller canonical Hebrew-prose `references/sources-and-corpora.md` rules.
Extend the skill's routing to manuscript-versus-transcription prose beyond accentuation.
Qualify current WLC wording in that reference and `core-rules.md`: WLC evidence is
about WLC; a manuscript claim needs manuscript evidence. Preserve the historical
August 7 one-transcription decision. This restoration uses public canonical history,
not a private source inspection.

For finding 11.4, add to common and repository receipt guidance: "Each update entry
identifies the passage it corrects by that passage's own words, not only by a finding
number or line number."

For finding 11.5, restore this common Git paragraph:

> An ordinary secondary worktree commits locally without pushing its branch. A
> long-lived branch whose integration awaits Ben's request is an exception: push the
> worktree branch to origin after every commit as a backup, without pushing main.
> Follow the branch's explicit authorization and integration procedure.

Keep the Codex skill and DAR D11 consistent. DAR is explicitly subject to the exception;
the September 28 backup permission already covers this plan's branch push. The deferred
11.1 thorny-merge and optional-second-suite clauses are not restored by implication.

For finding 14, replace the directory-based exemption in repository `AGENTS.md` with:

> A branch changing only documentation, comments, docstrings, or instruction text needs neither a mega run
> nor the suite. This exemption describes the changed content, not its directory.
> Executable hooks and helpers, tests, schemas, shared data, and execution-changing
> configuration receive the applicable checks even below `doc/`, `dot-claude/`, or
> `dot-Codex/`. Generator or product changes still require their applicable generator checks.

Replace `py/product_scopes.py`'s "What a change owes" description with:

> A documentation-only, comment-only, docstring-only, or instruction-text-only change owes neither the mega nor the
> suite. A change that can reach tier 3 owes a mega run and a reading of every tracked
> diff it leaves. Other executable-source, test, schema, or shared-data changes owe the
> suite. A change to a hand-run generator, or an input it reads, owes every affected
> hand-run generator and inspection of its outputs. AGENTS.md's "Integrating a worktree
> branch here: run the mega unless the branch is exempt" states the final worktree
> integration gate.

Finding 15 applies the same established cadence to canonical Wikisource-refresh
`references/dependent-refresh.md`: normal Git common-directory sibling resolution;
`REPOS_ROOT` for unusual layouts; mandatory final mega on a generator/data branch;
suite after the last test-risky change, with a still-relevant result not rerun merely
for integration. Preserve its authorized intermediate dependency integration procedure.

### Receipt and historical-record repairs

Create exactly these five absent live updates, each with `State: open`, agent/date
attribution and searchable quotations. Add each base's permitted line-4 pointer;
make no other post-completion base edit except a mechanically necessary paragraph join.

| New update | Scope |
|---|---|
| `doc/PLAN-remediate-review-findings-2026-09-16-update.md` | Actual landing credits, historical approval/completion, two incorrect prescribed first-entry dates. |
| `doc/post-stress-meteg-census-2026-09-03-update.md` | Acknowledge four later link edits to its frozen base; do not reverse or further rewrite those links. |
| `doc/PLAN-retire-codex-index-image-work-update.md` | Historical four-editor inventory and implementation/docstring credits. |
| `doc/post-stress-meteg-image-provenance-update.md` | Presentation/inventory corrections and the twenty-name mapping; retain historical base paths. |
| `evr-ii-b-55/evr-ii-b-55-images-provenance-update.md` | Distinguish the image-free directory from six published EVR crops. |

Use existing updates for September 10/14/16 review families, symmetric instructions,
cloud installation, timing, hazards, and post-silluq research. The September 14 plan
update's corrections quote "State: live; written 2026-09-16", "The executing task's
final report names:", "Retiring a finished document", and the relevant skill/reading
passages. Its attribution count is historical: 38 level-2 entries, one level-3 entry,
38 attribution lines; finding 10 lacked one, and finding 11.5 had two. Fix the old
locators and backtick spans without changing those measurements.

Finding 1's credit sequence is `7014cfbb` (moved the drive example), `18ddfbf7`
(prescribed repair), `18aabf8d` (implemented repair). The assertion that it was
already resolved at `d3edadc6` was false. Finding 13.2 diagnostics belong to
`18aabf8d`; finding 14's module/CSS edits belong to `4e30b0f4`. Keep the separate
current relocation-matcher defect in finding 16 visible. Record the earlier plan's
September 18 approval assertion as an assertion in that historical source, not a
newly verified quotation. Attribute September 18 remote-arrival evidence to the
local reflog, never independent GitHub history.

Finding 4.2 restores exactly Ben's already-approved `holman/WORKFLOW.md` paragraph:

> Every authored CSS theme declares `color-scheme: light dark` on `:root`, and every
> theme custom property that stores a color uses a `light-dark(<light>, <dark>)` pair.
> Fixed badge foregrounds and backgrounds remain literal colors. Do not add an
> `@media (prefers-color-scheme: dark)` block.

Correct 4.4 to seven historical accgram al-hatorah citations; the eighth census site
was a test, and three sites literally used the relative sibling path. Preserve Ben's
retained citations. Correct `py/github_issue_edit.py`'s tracker description to
"MAM-private and the five trackers recorded in". Correct the bidi explanation to
"A section sign and a backtick are neutral; an ASCII digit has a weak directional
type. None is a strong character." Date endpoint-window-method approval September
17 via September 16 close-out item 20.

For findings 5, 6 and 10, use the finite passages enumerated in turn 01 and accepted
later turns. Replace live-tree claims with measured-tree/history claims, pin surviving
historical references, and identify corrections by original words. The finite current
reference homes include the standards docstring, mega-coverage test, `dot-Codex/README.md`,
canonical tracker and Hebrew core references, post-silluq data comments, mega provenance,
sigil test, `uxlc/doc/clc-design.md`, and the periodic-review D7 history. Do not turn
24 historical accgram attributions into a new policy census. Preserve the September
23 Psalms 72:15 consolidation and later case-page locations. Rewrap the already
identified overlong canonical reference prose without changing its meaning.

Finding 10's concrete locators are these original source words. In
`doc/meteg-after-silluq-in-uxlc-and-wlc-update.md`, identify the summary passage by
"Section 6 has the links for the other three, 1 Kings 14:14, Psalms 60:10 and
Psalms 70:2." State that "the other three" belongs to the summary, not the section
6 lead. Identify that lead separately by "Built by `py/main_verse_links.py`..."
before supplying its already established correction. In
`doc/meteg-after-silluq-search-in-mam-documentation-update.md`, identify the source
finding by "Ben cites the passage as chapter 8 section 47, page 355, print footnote
54..." and its recapitulation by "Breuer's print page and footnote numbers. Ben's
citation is chapter 8 section 47, page 355, footnote 54..." Preserve the corrected
citation and evidence limitations; do not reopen the source research.

For finding 12, update only surviving current section locators. Fix the future-wrapper
comment in `.claude/hooks/install-user-config.sh` without executable behavior changes,
and record wrapper conversion at `d695966be8daea270f85424cb77d06f3b92a873d` in the
existing cloud update. Do not claim a fresh cloud execution check.

For finding 13, add the missing maintained
`doc/user-wide-instruction-conversion-reconciliation.md`. Inventory every H2/H3 of
`71f96ca3:dot-claude/user-wide-CLAUDE.md`; map exact old headings to current shared
body/skill anchors, retained rules, approved 11.2–11.5 restoration, explicitly deferred
11.1 clauses and source commits. Do not promote the editorial 214-rule segmentation
to a canonical count. Record the September 15 budget reversal; change no current
32,768-byte limit. Replace the overclaim "No genuine policy conflict required a new
decision" with the distinction between preserved/restored and deferred clauses.
Do not execute or retire the overtaken September 9 plan in this task.

For 18.4–18.5, quote "Three editors remain" in the new retirement-plan update and
record that the historical highlight picker made four. Credit `139f631e` for the
reader implementation and `009b6378`/`46e2e524` for docstrings. Finding 34.3's vague
retirement-plan referent is already corrected by `02879b9c`; make no extra base repair.

Finding 34.4 corrects the existing hazard update: hazard 2's audience is generic
external consumers and MAM-internal reproducers. Hazard 3 reaches parsed-plus and
MAM-simple notices, because plain has no special-letter wrapper. Hazard 5/7 and
the closing "Both must require" refer to MAM-parsed and MAM-simple notice families.
Explicitly withdraw the update's "No repository defect was found" for the guide's
universal three-encoding claim, while retaining the genuine between-verse duplicate
counting hazard. The frozen hazard base remains intact.

### Retirement safety fixes and independent checks

Finding 16 changes `py/repo_util/worktree_retirement.py`, particularly
`_reference_matches`, `_citation_references`, `_tracked_relocation_citations` and
their checkout-snapshot callers. Construct references from the actual per-target
`.novc` relocation inventory, not generic relative `.novc/`. Include exact retained
child paths and exact absolute source-directory roots in absolute, checkout-relative,
primary-relative and file-URL spellings. Preserve exact target-root citations while
excluding generic relative `.novc/` references. Include retained child directories/files,
with sentence punctuation and proper boundaries. Unrelated `.novc` citations and
lookalike prefixes must not match. Preserve snapshots, fingerprints, reviewed semantic
notes and fail-closed unreadable-evidence behavior.

Extend the operational `worktree_retirement_simulation_test.py` differential using
actual temporary primary/target/observer Git checkouts and a nonempty relocation tree.
Independently enumerate paths with filesystem APIs, form supported spellings and
negative lookalikes, and compare the detected `(checkout, path, line, source)` set
to that inventory. An observer citation added after the target's recorded HEAD must
be detected. An unreviewed gate must leave registry and file bytes unchanged; an
eligible reviewed simulation must preserve relocated evidence. No real worktree
retirement or new link/junction simulation is part of this plan.

Finding 17 broadens the AST force-operation lint in
`py/tests/test_worktree_retirement_policy.py` across the retirement engine,
compatibility cleanup, owner inspection and both maintenance entry points. Detect
`--force`, `-f`, and forced branch deletion `-D` at every destructive Git
worktree/branch argument position. Reject `git worktree prune` and direct recursive
worktree deletion outside the precise allowances below. Keep ordinary non-forced
Git worktree removal and branch deletion confined to the shared retirement engine.
The finite modules are `worktree_retirement`, `git_worktree_cleanup`,
`codex_worktree_retirement`, `clean_worktrees`, `worktree_owners`, `main_repo_util`
and `main_repo_maintenance`. Preserve
only the existing verified cross-volume `shutil.rmtree(source)` in `_relocate_novc`
and legitimate `.novc` cache cleanup in `main_repo_maintenance._clean_one_novc`;
a global recursive-removal ban would reject those authorized operations.

Remove dead `CleanupReport.errors` and its print loop while retaining actual exception
propagation and sweep failures. Treat unexpected `show-ref` statuses as
`RetirementError`, distinct from an absent reference. Verify selection against actual
temporary Git refs; damaged temporary metadata can exercise failure without a mock
that pins a fabricated error string. Keep the ordinary-token precondition, but do
not claim the constant assertion measures elevation. That method remains deferred.

Correct finite pointers in `in/repo_maintenance_policy.json` and `py/main_repo_util.py`
to the current topology maintenance guidance, and the owner/simulation docstrings.
Use "Flush per-repository progress so captured sweeps remain observable.";
"Compatibility inspection does not use the ended-path argument to authorize
removal."; and "Inspection failures fail the sweep. Safety blockers are reported
as kept worktrees and do not authorize or attempt retirement." Runtime records
supply activity evidence, never removal permission. Active leases and unreadable
installed formats block; a cwd record without a lease does not itself block, and
missing records do not prove task completion. Simulation destruction stays confined
to simulation temporary repositories under the system temporary directory.

### Established timing, source and checkout-scope corrections

Finding 33's public guide replacements are bounded:

- In `doc/windows-long-paths.md`, replace "Python 3.6 and later can use extended
  paths..." with "Python 3.6 and later support the second mechanism above when the
  Windows setting is enabled." Preserve the Spanish-locale official OpenAI URL;
  the review did not prove it broken. Its label may say "official OpenAI worktree
  documentation (Spanish locale)".
- Preserve the original September 19 unset observation, adding "The original record
  did not name the checkout used for this Git setting." Remeasure `core.longpaths`
  independently in primary and development with the explicit commands below. Record
  results, source and actual date; do not reuse the old Claude checkout's setting as
  evidence about this recovered Codex checkout.
- In `doc/sigil-decoding.md`, the ל-א row keeps B 55's identification but replaces
  the asserted distinction with "The mirrored appendix calls B 55 formerly B 247
  at line 78 and describes B 247 as a direct continuation at line 93. The NLI presents
  both shelfmarks together. The corpus also cites B 247 at Job 21:24; this record
  does not resolve that citation's relation to the EVR README's Chronicles-only
  description." Verify the already named local mirror/source anchors; do not
  adjudicate manuscript identity.
- In `doc/scan-pages.md`, "Canonical holdings outside", add "This subsection was
  added by commit `622b48fd` on 2026-09-24; no source here identifies a separately
  dated decision by Ben." Replace "recorded Da'at Miqra disposition" in question 2
  with "Da'at Miqra subsection added on 2026-09-24". This is source attribution,
  not new scan/API work.

In existing timing updates, correct 19,531 to scanner calls: 18,724 verse bodies
plus 807 dual-cantillation rescans; the step writes 18,725 records. Explain the
eight blank Cloud/Ben ratios by two raised steps, five recorded Ben values of 0.0,
and the post-stress-meteg survey skipped in cloud. Preserve the already recorded
step names and original measurements; no private remeasurement is proposed.

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics config --show-origin --get-all core.longpaths
```

```powershell
git -c safe.directory=C:/Users/BenDe/.Codex/worktrees/dar-2026-09-26/MAM-basics -C C:/Users/BenDe/.Codex/worktrees/dar-2026-09-26/MAM-basics config --show-origin --get-all core.longpaths
```

No value with exit 1 means unset for that checkout; any other failure is a diagnostic,
not an unset observation.

### Twenty finite image renames

All paths in this table are under development `gh-pages/img/`. The current converter
is `consensus_to_ascii` in `py/author_boj_util/author.py`. Source forms are the
existing corresponding MAM-simple XML forms, with converter outputs
`גם־עתה → G603FH`, `חושה → XVJH`, `יברכנהו → YBRKNHV`, `מנהו → MNHV`,
`נחשת → NXJF`, and `אעשה → A3JH`. The compound 1 Kings 14:14 form retains maqaf
through the converter; do not substitute an ad hoc transliteration.

| Existing filename | Proposed filename |
|---|---|
| aleppo-083r-1K14v14-atta.png | aleppo-083r-1K14v14-G603FH.png |
| aleppo-253r-Ps70v2-xushah.png | aleppo-253r-Ps70v2-XVJH.png |
| cairo-cotp-image204-1K14v14-atta.png | cairo-cotp-image204-1K14v14-G603FH.png |
| cairo-cotp-p110-image103-1S17v5-nexoshet.png | cairo-cotp-p110-image103-1S17v5-NXJF.png |
| cam1753-0073B-col2-line13-Job4v12-menhu.png | cam1753-0073B-col2-line13-Job4v12-MNHV.png |
| cam1753-unlocated-Ps70v2-xushah.png | cam1753-unlocated-Ps70v2-XVJH.png |
| cam1753-unlocated-Ps72v15-yevarkhenhu.png | cam1753-unlocated-Ps72v15-YBRKNHV.png |
| leningrad-195B-col2-line27-1K14v14-atta.png | leningrad-195B-col2-line27-1K14v14-G603FH.png |
| leningrad-379B-Ps70v2-xushah.png | leningrad-379B-Ps70v2-XVJH.png |
| sassoon-1053-1K14v14-atta.png | sassoon-1053-1K14v14-G603FH.png |
| sassoon-1053-1S17v5-nexoshet.png | sassoon-1053-1S17v5-NXJF.png |
| sassoon-1053-Job4v12-menhu.png | sassoon-1053-Job4v12-MNHV.png |
| sassoon-1053-Ps70v2-xushah.png | sassoon-1053-Ps70v2-XVJH.png |
| sassoon-1053-Ps72v15-yevarkhenhu.png | sassoon-1053-Ps72v15-YBRKNHV.png |
| st-petersburg-evr-ii-b-55-Job4v12-menhu.png | st-petersburg-evr-ii-b-55-Job4v12-MNHV.png |
| st-petersburg-evr-ii-b-55-Ps70v2-xushah.png | st-petersburg-evr-ii-b-55-Ps70v2-XVJH.png |
| st-petersburg-evr-ii-b-55-Ps72v15-yevarkhenhu.png | st-petersburg-evr-ii-b-55-Ps72v15-YBRKNHV.png |
| st-petersburg-evr-ii-b-55-f57a-image120-1S17v5-nexoshet.png | st-petersburg-evr-ii-b-55-f57a-image120-1S17v5-NXJF.png |
| st-petersburg-evr-ii-b-55-image186-1K14v14-atta.png | st-petersburg-evr-ii-b-55-image186-1K14v14-G603FH.png |
| urj-2005-Num23v26-eeseh.png | urj-2005-Num23v26-A3JH.png |

Before moving anything, write an ignored UTF-8 scratch manifest from the actual files
containing old/new path, size, PNG geometry and SHA-256; validate no target exists and
all paths resolve within this exact image directory. Rename with one filesystem API
or PowerShell end to end. Compare every new file with the old manifest. Hash/size/
geometry must match exactly, and the rename diff must show 100% unchanged content.
Do not delete or regenerate a crop to accomplish a rename.

Update `py/author_site/post_stress_meteg_shared.py` and the six affected generated
case/register HTML files through their generator; current snips README, maintained
Psalms 72:15 report and Job 4:12 update receive matching links. Frozen provenance
paths remain in the base, with the mapping in its single update. Preserve the four
pre-window moved slugs, five `HFRV33Y` slugs and two English `final-word` names.
Search both authored and generated current references to all twenty old names, and
classify each surviving historical occurrence instead of blindly replacing it.

### Explicit deferral and no-action ledger

| Item | Approved disposition |
|---|---|
| 7.1 Holman notes | Defer classification/editing of the five dated evidence notes named in the review. |
| 7.3 | No retrospective repinning: the complete-family bytes at the retained pin match the archival endpoint. |
| 11.1 | Defer all twelve legacy clauses: "as unverified", "quite ready", default-branch override, optional second suite, "thorny merge", `total_tokens`, "genuinely ends", "prescribe exactly what", "own words", "Bold lead-ins", "deleting the count", and the three `py/foi/*_explanations.py` modules. Do not mark these intentionally dropped by Ben. |
| 13.2 | Defer retirement of the overtaken instruction-remediation plan until surviving work is reconciled. Change no budget. |
| 17.2 | Defer an ordinary-token measurement method; retain the precondition without treating a constant assertion as evidence. |
| 17.8 | Defer link/junction simulation, wider Git-filename-call lint and Hebrew-presentation-form exclusion from Latin NFC scanning. |
| 18.8 | Defer manuscript adjudication of the four inconsistent stored boundary labels. |
| 22 | Defer joining implicit-maqaf pairs. Preserve current reader grouping. |
| 25.4 | Defer release naming/date convention. Preserve all boundaries and names. |
| 26 | Defer source/revision/message date-label policy. |
| 27 | Defer Job 4:12 adjudication and new evidence work. Preserve current text and survey. |
| 29.5–29.7 | Defer proposal/suggestion naming, redundant dataset-stub removal and apostrophe policy. |
| 30.4 | Defer shelfmark spelling. |
| 31.8 | Defer coverage of existing manuscript observations in maintained reports and ledger report links. Do not silently add an EVR reading to the Psalms 72 report. |
| 35.1 | Defer private-path/filename privacy judgment; inspect no private content. |
| 35.2 | Defer public private-review count/file-kind metadata judgment. |
| 35.3 | Retain quotations as recorded without an invented source. In `doc/periodic-review.md`, replace "file on the pushed branch `dual-agent-review-2026-09-16`" with "`doc/dual-agent-review-2026-09-16-turn-01-claude.md`, now tracked on main". Preserve the historical window claim. |
| 35.4 | No historical-act repair. Defer new process policy. The optional three undated-rule label clarifications are left unimplemented because this plan proposes no finite replacement for them. |
| 35.5 | Defer voice, inspection attribution and raw source-line presentation choices. |
| 35.6 | Defer a general browsing/robots rule; follow the existing HBCE restriction. |
| 35.7 | Already resolved by `a41fbcdd`: Google comparator/output removed. Restore neither. |
| 35.8 | Defer `slhw-desc-0` legarmeh representation policy. |
| 35.9 | Defer PyYAML validator/dependency disposition; remove no dependency. |

## Execution, verification and integration

After Ben approves this concrete plan, freeze the approval scope in the September 26
review's live update with the actual date and approved plan commit. Use coherent
dependency phases: policy/record repairs; reader/notices/alternative-change logic;
bounded safety/lint work; regenerations and final checks. These are dependency phases,
not permission to implement only part of the approved work. The root executor may
choose smaller coherent commits and read-only agents, keeping one writer.

Every commit gets exact HEAD/task-owned status verification, `git diff --check`, Black
at defaults on changed Python only, and directly relevant lints/differentials. Never
run bare pytest or add an import shim. For elevated parent programs launching Git,
append the exact development path through process-local `GIT_CONFIG_*` entries.
Write multiline commit bodies to unique UTF-8 scratch files and use `git commit -F`.
Stage only owned paths. Backup each commit to `origin/dar-2026-09-26`; do not push
`main` or integrate the review branch during intermediate phases.

Use the following actual entrypoints from the development cwd, at the relevant phase.
No generator or full suite is run merely to prepare this plan.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_parse.py ws
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_authored.py gen-mam-parsed-docs
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_authored.py gen-misc
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_authored.py gen-site --trust-surveys
```

The `gen-site` command deliberately renders from the tracked survey for these
presentation-only repairs. Inspect the survey hash beforehand and require it unchanged;
do not rerun private-dependent survey research to adjudicate the deferred Job reading.
The final mandatory mega runs its documented existing survey step normally.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_verify_and_render_table.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py mpplus --all
```

After committing source/products so HEAD is the intended freshness baseline:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py mpplus --check
```

Relevant targeted checks include the real operational simulation (outside the default
suite discovery), retirement policy/freshness, mark order, reader content, notices,
geometry, index links, page conventions and filenames. Add only independent differentials
or mechanical tree/text lints when the approved fix needs new checks.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py py/repo_util/worktree_retirement_simulation_test.py py/tests/test_worktree_retirement_policy.py py/tests/test_diff_mpplus_unpinned_latest.py -q
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py py/tests/test_mam_simple_mark_order.py py/tests/test_prose_mark_order.py py/tests/test_mam_xml_verses.py py/tests/test_public_data_consumer_notices.py py/tests/test_scan_overlay_viewboxes.py py/tests/test_site_index_links.py py/tests/test_post_stress_meteg_plain_word.py py/tests/test_post_stress_meteg_annotations.py py/tests/test_tracked_filenames.py -q
```

Run the existing `py/tests/clc_dual_cant_test.py` through `py/main_test.py` for the
U+05C9 exclusion. Read each tracked output diff after generators. Expected changes
are only the described reader prose/captions/links, notice headers/documentation,
change logs, image-path references and removal of an unused SVG class. Crop bytes,
Scripture body values, stored manuscript markers/geometry, release boundaries/names,
translation caveats, current Job interpretation, surveys and published Holman assets
must stay unchanged. An unexplained diff is a finding and blocks final integration.

After the last executable/test/schema/shared-data change, run the full suite once;
later documentation/comment/record/instruction-text-only commits do not expire that
result. A later material source change requires another relevant suite result.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py
```

### Issue 269: finite approved body correction

Read the entire current issue and all comments immediately before the edit using
`github-issues`. The September 28 read found it open, with no comments/labels/assignees;
that is a dated observation, not a precondition to overwrite later activity.
Replace only its sentence linking the completed mega-coverage plan with the same
base link and its update:

> The completed work is recorded in [`doc/PLAN-mega-coverage.md`](https://github.com/bdenckla/MAM-basics/blob/40395aa3d44608e9f63a75897cd8e42e1b1a7338/doc/PLAN-mega-coverage.md)
> and [its update](https://github.com/bdenckla/MAM-basics/blob/40395aa3d44608e9f63a75897cd8e42e1b1a7338/doc/PLAN-mega-coverage-update.md).

Append a body note dated with the actual execution date: "Edited on [date] by a
Codex session, following Ben's 2026-09-28 approval of the review dispositions, to
link both members of the retired mega-coverage plan family so its Phase 7 correction
remains visible." Keep the `40395aa3` pin; both targets already exist on `origin/main`.
Use the approved editor with a uniquely named scratch body, dry-run, complete outgoing
body review, apply and full read-back. Leave state/title/labels/assignees/comments intact.
No thin review-tracking issue or new issue is part of this plan.

### Final integration and deployed instructions

The final phase verifies both checkouts clean, fetches `origin`, and merges the latest
primary `main` into `dar-2026-09-26` in the development checkout. Resolve conflicts
there and repeat relevant checks if the merge changes their inputs. Run the complete
mandatory mega from the development cwd without `REPOS_ROOT`:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
```

The ordinary mega includes its documented read-only private-dependent survey; this
does not authorize new private research, editing MAM-private, or choosing the deferred
Job policy. A failing step or unexplained tracked diff is failure. Explain and commit
every legitimate generated diff on the review branch. Ensure the separate hand-run
parsed documentation and named-report checks remain current. Record suite/mega
commit IDs and results, not merely elapsed times or a statement that checks were run.

In the primary integration checkout only, verify it is clean on the expected `main`,
then perform the verified fast-forward:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics merge --ff-only dar-2026-09-26
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics push origin main
```

If main moved and the fast-forward refuses, return to the worktree, merge the new
main and verify again. Never substitute a primary merge or force push. This is the
single final integration, which reaches the published Pages tree and distributed
products; it is independently an outward-facing act.

After canonical instruction/skill changes are integrated and `main` is pushed, deploy
from primary `C:/Users/BenDe/GitRepos/MAM-basics` and verify with the complete
read-only check. Do not deploy from the review branch or directly edit live copies.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config --check
```

Put actual implementation dispositions, verification evidence, preserved deferrals
and final integration/deployment evidence in the September 26 review's single live
update. Do not mark remediation complete until the approved active work, issue edit,
generator/suite/mega checks and integration are complete. The numbered review turns
remain frozen. Keep this plan true while executing; once completed it becomes a
receipt, and later correction uses only its single update. Keep the DAR worktree lock
and branch until a separate cleanup task after this task has ended.
