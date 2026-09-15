# Codex counter-argument to the 2026-09-14 review of the public repos

State: completed 2026-09-15; review only

This is turn 2 of the D9 alternating round in `doc/dual-agent-review.md`. It checks the Claude
argument in `doc/review-findings-2026-09-14.md`, including Ben's later decisions recorded there,
against the same MAM-basics endpoint diff, `0354b6cc..bca64824`. The argument was first committed
at `d14d2723`; this pass read its corrected form at `fbeb3809`. A later correction to the review
record does not change the endpoint diff under review.

The counter-argument is review only. It changes no source, generated product, issue, remote branch,
or live user-level file. It reads public evidence only and does not read MAM-private. Two read-only
sub-agents separately challenged the counter-findings and the finding-by-finding reconciliation;
the writing session checked their conclusions against the named files before recording them.

## Result

The argument's central diagnoses hold. No numbered finding is rejected. Findings 7, 8, and 10 need
qualification: finding 7.5 overstates the consequence of expected line-number drift; finding 8's
two plan reviews omit one execution-target rule and one reproducible inventory pointer; and finding 10.1's public
code gap is confirmed while the argument's claim that its own session instantiated the gap rests on
machine-local session evidence that this public-only turn did not read.

The two plan omissions are new findings, C1 and C2 below. C3 narrows finding 7.5. The reconciliation
appended to the Claude argument gives one comparison and one remaining-work statement for each of
its numbered findings 1 through 11.

## C1. The image-retirement plan does not resolve its ignored primary-checkout target from a secondary worktree

`doc/PLAN-retire-codex-index-image-work.md` allows implementation in any assigned MAM-basics
checkout. Its measurement script is created and run in that checkout, where it inspects the
relative `cam1753/cam1753-pages/` directory. The removal step likewise says to move that relative
ignored tree to the Recycle Bin, and the final check confirms that the relative path is absent.

That is insufficient for an ignored directory. Git does not populate ignored files in a linked
worktree. On 2026-09-15 the review worktree had no `cam1753/cam1753-pages/`, while the primary clone
at `C:/Users/BenDe/GitRepos/MAM-basics/cam1753/cam1753-pages/` had exactly the plan's planning
snapshot: 28 files and 50,316,747 bytes. The plan's instruction to treat a mismatch as a finding
means a compliant executor must stop on the 28-to-0 mismatch rather than silently claim completion.
The plan never tells that executor where the actual target is or how to resolve an expected
cross-checkout ignored cache, so the executor cannot complete the intended retirement without
inventing a rule.

The plan needs to distinguish the development checkout, where tracked edits and checks run, from
the primary-checkout or all-checkouts inventory of ignored data. It must resolve and verify the
exact existing ignored target before the recoverable Recycle Bin operation. This changes no
product; the hard-to-undo axis is a local destructive act, mitigated by the plan's required
Recycle Bin operation.

Re-establish from the review worktree by comparing `Test-Path` for the two absolute directories and
measuring the primary directory with `Get-ChildItem -File -Recurse` and `Measure-Object Length
-Sum`. The relevant plan anchors are "Work in the exact MAM-basics checkout assigned", "inspect the
ignored `cam1753/cam1753-pages/` directory directly", and "Move the ignored, derived
`cam1753/cam1753-pages/` tree".

## C2. The Google Sheet retirement plan does not cite or pin the 36-page oracle it must preserve

`doc/PLAN-retire-google-sheet.md` tells a fresh executor to declare a 36-page mirror from the
Sheet's `מיוחד special` tab, then delete the Google download and comparison pipeline. The plan
gives categories that add up to 36, but it does not give the 36 exact requested titles, cite a
tracked inventory, name a checkpoint for that inventory, or give a command that reproduces it.

The exact titles are recoverable from public tracked evidence that the argument's plan audit did
not inspect: `in/mam-ws-intro/ch2.mediawiki:361-388` supplies the four Decalogue pages, and
`:738-805` supplies eight groups of three pages plus eight associated chapter pages. The live Sheet
URL is separately recorded in `in/mam-ws-intro/data-sheet-guide.mediawiki:6`. The omission is
therefore not loss of the inventory; it is the plan's failure to name and freeze its available
oracle before removing the old pipeline.

The omission matters because the plan itself calls out a misspelling to correct and a redirect to
follow. A fresh executor should not have to rediscover which tracked table is the oracle or infer
whether later Sheet drift changes the declared set. The plan should cite the tracked exact-title
inventory, pin its checkpoint, and provide a remeasurement command before the old pipeline is
removed, while still letting the new downloader record requested and resolved Wikisource titles
separately.

Re-establish with the section "Add the Wikisource special-page mirror" in the plan, the two tables
in `in/mam-ws-intro/ch2.mediawiki`, and the Sheet link in
`in/mam-ws-intro/data-sheet-guide.mediawiki`.

## C3. Finding 7.5 overstates what line-number drift breaks under D12

Finding 7.5 says that line numbers in two live update entries have drifted. The same finding says
both entries name the text they locate. D12 in `doc/dual-agent-review.md` states that every update
entry names the corrected passage by that passage's own words "since line numbers drift". Under
that rule, later line-number drift is expected and the word anchors remain valid locators. The
argument therefore should not present the changed numbers as broken location evidence.

D12 also says that an update file is live and kept true, so a present-tense assertion that text is
at a particular live line can still be refreshed or given an explicit checkpoint. The
qualification is about consequence, not a categorical rejection of the argument's low-severity
maintenance finding.

The second half of finding 7.5 remains sound. The entry for finding 20.11 records SHA-256 values
without naming the commit or other checkpoint at which they were measured; later file changes make
the values impossible to interpret from the entry alone. That reproducibility gap remains part of
finding 7's unfixed work.

## Assessment of the eleven Claude findings

"Confirmed" means the bounded diagnosis and its own stated disposition reproduce; it does not
convert a design note into a defect or approve a remedy. "Qualified" records a narrower evidence
claim or additional work. None of these comparisons marks unfixed work fixed.

| Claude finding | Codex comparison |
|---:|---|
| 1 | **Confirmed.** The live instruction still says 47 entry points and 59 steps while the endpoint has 43 declared and resolved entry points across 55 steps. The upstream-change gap, lint boundary, and contradictory tier-3 docstring also remain. |
| 2 | **Confirmed.** Both hand-run product generators read tradition directories whose first required book-group files no longer exist under incremental storage. The 39.0 MB statement omits the same commit's `yeivinID` reduction. Parts 2.2 and 2.4 were repaired within the window. |
| 3 | **Confirmed.** The report blobs named by the live update files are stale, the moved `metsudah-vs-ctr` link has no sibling correction, and the retained crop-naming rule lost its single declared home. The rest of the crop move remains sound as the argument says. |
| 4 | **Confirmed.** The stale al-hatorah count and the missing letters-only-match note reproduce. The changed lookup itself is correctly labelled not a defect; ambiguous failure remains a usability observation rather than a data error. |
| 5 | **Confirmed.** The two endpoint trees are equal and the transient side-branch rewrite was restored before the endpoint. The argument correctly places it outside the diff and records no remaining work. |
| 6 | **Confirmed.** Ruff reports only the two named F401 imports. |
| 7 | **Qualified by C3.** The nonexistent blob, procedure departures, conflicting update-file rules, missing `Recorded by` line, checkpoint-less measurements, and two internal inconsistencies reproduce. Drifted line numbers do not break the durable word anchors D12 requires, though uncheckpointed present-tense line claims may still be refreshed. |
| 8 | **Qualified and extended by C1 and C2.** The stated instruction and plan defects reproduce or are correctly labelled design questions. The plan audit is incomplete without a rule for resolving the ignored primary-checkout target and a pinned pointer to the tracked 36-page oracle. |
| 9 | **Confirmed.** The open issue's body still names the removed `leningrad/page-snips/` example and has no comment correcting it. No issue change was made. |
| 10 | **Qualified by the public-evidence boundary.** The source establishes the session-protection gap, incomplete NUL-delimiter lint, stale `_commit_date` docstring, and missing UTF-8 stdio setup. Parts 10.4 through 10.6 and 10.8 remain observations, not defects. The machine-local example used by 10.1 was not independently read. |
| 11 | **Confirmed.** The six prose defects reproduce against the loaded `hebrew-prose` rules and the files' live-versus-finished classifications. No manuscript reading was adjudicated. |

## Scope and verification

The checkout began clean on branch `dual-agent-review-2026-09-14` at `fbeb3809`, which contains
the required `1887188f`. `git diff --check 0354b6cc bca64824` was clean. Black 26.8.0 reported all
1,044 Python files unchanged. Ruff 0.16.5 reported exactly the two F401 errors in finding 6.

The existing public review checks for product scopes, live update-file blobs, and MAM-simple sizes
were rerun where they did not depend on nested Git accepting this linked worktree. Direct source and
tree checks supplied the generator-path, plan, link, and endpoint-tree evidence. Helper reruns that
nested Git rejected as an unsafe repository were not used as evidence. The earlier full-suite and
mega results were not repeated: this turn changed only review records and the reviewed source tree
has not changed since the argument's endpoint.

The public GitHub histories of the fifteen quiet repositories were checked for the bounded window.
No commit appeared in MAM-simple, MAM-parsed, MAM-with-doc, MAM-for-Sefaria, MAM-OSIS,
codex-index-aleppo, codex-index-cam1753, codex-index-leningrad, diffable-pointed-hebrew,
book-of-job, holman-ketiv-qere, UXLC-utils, wlc-utils, Taamey_D, or phonetic-hbo. MAM-basics issue
#278 was read without modification. No private repository, live Sheet, live Wikisource page,
manuscript image, user session record, remote branch, or issue state was changed or adjudicated.
