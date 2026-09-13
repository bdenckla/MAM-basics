# Updates to the 2026-09-10 public-repository review

State: open, first entry 2026-09-12. Every entry here corrects or supplements
`doc/review-findings-2026-09-10.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document — a review, a remediation plan, a completed
plan, an execution record — is left as written. A correction or later disposition goes in a
sibling file named `<stem>-update.md`, which is what this file is for that review.

## Finding 9: the live plan no longer requires superseded FOI bytes

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 9 is
unfixed and not acted on.

Commit `70d1f581` on branch `dual-agent-review-2026-09-10` fixes criterion 9 in the live
`doc/PLAN-silluq-before-gaya-template.md`. The criterion now compares the regenerated
`gh-pages/MAM-with-doc/foi/foi-mtgmtg.json` with the Git blob measured immediately before
implementation instead of requiring the superseded 718-record bytes.

The 2026-09-12 baseline at `f0795231` is blob
`b6c323992bb1d05e5995b1047449931c8e026464`: 717 records, with group counts 354, 228, 19, 102 and
14. The 1 Kings 7:37 record remains in `1/sopa-y/maq-n` and has two U+05BD marks. A later
starting-blob mismatch remains a finding to remeasure, not a reason to restore old bytes.

Product axis: the repair changes a live plan and this update record; it changes no generator or
product. Act axis: both writes are ordinary repository commits on the unpushed review branch; no
outward-facing act, destructive local act, external configuration write or receipt rewrite
occurred.

## Inherited item 2: update-file State declaration pointers

Recorded by Codex on 2026-09-12. Inherited item 2 under “Three items this round's integration
inherits” is complete.

Implementation commit `d18cbb4b` on branch `dual-agent-review-2026-09-10` adds the owed pointers
from `CLAUDE.md`'s section “A finished dated document is corrected in `<stem>-update.md`, never
edited” and D12 of `doc/dual-agent-review.md` to the declaration in
`py/repo_util/check_repo_standards.py`'s module docstring.

## Finding 11.1: MAM's `סימנים` identifies the Simanim Tanakh

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 11.1
is unfixed and not acted on.

Implementation commit `f13b1a988ebd9871db11f28ea4aec831c48fc0c1` on branch
`dual-agent-review-2026-09-10` adds
`doc/meteg-after-silluq-search-in-mam-documentation-update.md`. The search document is a
finished report, so D12 leaves its two historical references to “the Simanim Tiqqun” intact and
the sibling update says that both references should read “the Simanim Tanakh.”

The correction rests on MAM's mirrored public introduction at
`in/mam-ws-intro/appendices.mediawiki`, which defines `סימנים` in the list of editions based on
the Aleppo Codex as `תנ"ך סימנים (פלדהיים תשס"ח)`. No inference about the Simanim Tiqqun's
haftarot is needed. Finding 11's remaining prose sites are unchanged, and no choice between
`hataf` and `ḥataf` has been made.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; no
outward-facing act, destructive local act, external configuration write or receipt rewrite
occurred.

## Finding 20.2: the three historical referents are named directly

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 20.2
is unfixed and not acted on.

Implementation commit `a65bb60ed66df1cbff72d105abc68c029006a38b` on branch
`dual-agent-review-2026-09-10` completes finding 20.2. The September 8 remediation plan is a
finished document, so D12 leaves both historical phrases unchanged; the plan's existing sibling
update records source commit `0ee34bea8` for the first State and Ben's approval as the event that
made the second State historical. The live September 9 instruction-file remediation plan names
`references/sources-and-corpora.md` directly in place of “the latter.” All three sites were
applicable prose defects rather than protected quotations. No other part of finding 20 changed.

`git diff --check` and the tracked-prose mark-order lint passed. The full suite passed 997 tests,
with 5 skipped and 65 subtests passed. This documentation-only unit does not owe a mega run.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; the finished
September 8 plan remains unchanged, and no outward-facing act, destructive local act, external
configuration write or receipt rewrite occurred.

## Finding 20.3: the three paired referents are named directly

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 20.3
is unfixed and not acted on.

Implementation commit `ded05cd1d24baf32fc415e3d4da881b4527b2d99` on branch
`dual-agent-review-2026-09-10` completes finding 20.3. The mega-coverage plan is finished, so D12
leaves its historical “one flag-selected mode of a program and not another” sentence intact and
`doc/PLAN-mega-coverage-update.md` names the mode that the mega runs and the mode that the mega does
not run. The live `py/tests/test_mega_coverage.py` module docstring makes the same two referents
explicit. The live `py/mb_cmn/graphviz_pin.py` module docstring names `check_installed` as the check
that prevents a wrong Graphviz stamp and `stamp_in_svg_text` as the check of existing SVG stamps.
All three sites were applicable prose defects rather than protected quotations. No other part of
finding 20 changed.

Product axis: the correction changes documentation and Python docstrings only; it changes no
generator behavior or product and does not owe a mega run. Act axis: both commits are ordinary
repository commits on the unpushed review branch; the finished mega-coverage plan remains
unchanged, and no outward-facing act, destructive local act, external configuration write or
receipt rewrite occurred.

## Finding 20.4: the five announced sets are numbered

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 20.4
is unfixed and not acted on.

Implementation commit `5d771295d95f87265cbc7ec169402f5f795c28b0` on branch
`dual-agent-review-2026-09-10` completes finding 20.4. The live instruction-file remediation plan
now numbers its two stale conditions. The live hook comment reconciles “Four further trees” with
the three entries it presents, calls them three entries, and numbers them 1 through 3.

The completed five-products evacuation plan and the completed two-artifact assessment remain
unchanged; their existing sibling update files give the two public findings and the three reasons
as numbered lists. The completed meteg-after-silluq screen report also remains unchanged; the new
`doc/meteg-after-silluq-screen-against-uxlc-and-wlc-update.md` gives its two opening definitions as
a numbered list. All five sites were applicable prose rather than protected quotations. No other
part of finding 20 changed.

Product axis: the correction changes documentation and a code comment only; it changes no
generator behavior or product and does not owe a mega run. Act axis: both commits are ordinary
repository commits on the unpushed review branch; all three finished dated documents remain
unchanged, and no outward-facing act, destructive local act, external configuration write or
receipt rewrite occurred.

## Finding 20.5: the seven finding leads put their dispositions first

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 20.5
is unfixed and not acted on.

Implementation commit `a0ff3b45891e21aa0698b9c7690676f998f68ae6` on branch
`dual-agent-review-2026-09-10` completes finding 20.5. The new
`doc/meteg-after-silluq-psalms-72-15-update.md` gives disposition-first versions of summary items
4, 7 and 8. The existing `doc/meteg-after-silluq-screen-against-uxlc-and-wlc-update.md` now gives
disposition-first versions of findings 1, 5, 6 and 7.

All seven sites were individually confirmed as the reports' analytic prose rather than protected
quotations. Each disposition comes from the same report: an established screen or source result,
Phonetic MAM's exclusion as evidence, or a result not found in Yeivin and Breuer. No substantive
finding changes. Both finished source reports remain unchanged.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; both
finished dated reports remain unchanged, and no outward-facing act, destructive local act,
external configuration write or receipt rewrite occurred.

## Finding 11.4: the nine possession verbs have live “has” corrections

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 11.4
is unfixed and not acted on.

Implementation commit `0e40b5a1d545d13e815e863c759d6b013b40a5ae` on branch
`dual-agent-review-2026-09-10` completes finding 11.4. The new
`doc/meteg-after-silluq-koren-lookup-candidates-update.md` gives the two corrected Koren-candidates
passages, the new `doc/meteg-after-silluq-job-4-12-update.md` gives the five corrected Job 4:12
passages, and the existing `doc/meteg-after-silluq-psalms-72-15-update.md` now gives the two
corrected Psalms 72:15 passages.

All nine sites were individually confirmed as the reports' analytic prose rather than protected
quotations. Each correction replaces only the cited possession verb with “has” and preserves the
passage's claim. The three finished source reports remain unchanged. Finding 11.5's choice between
`hataf` and `ḥataf` remains unmade.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; all three
finished dated reports remain unchanged, and no outward-facing act, destructive local act,
external configuration write or receipt rewrite occurred.

## Finding 11.3: analytic `ga'ya` terms have live `meteg` corrections

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 11.3
is unfixed and not acted on.

Implementation commit `2c9b00ca60f077316271af6b5f8ae900cda93566` on branch
`dual-agent-review-2026-09-10` extends
`doc/meteg-after-silluq-search-in-mam-documentation-update.md` with corrected readings for the
analytic category labels in finding 2, the MAM roster statement in finding 4, and the scope note
under “What could not be verified.” Each corrected reading uses “meteg,” as the report's opening
vocabulary note requires.

The finished source report remains unchanged at Git blob
`5c4aaf4c61d8f66f95caf65c48a37a9c1d735fba`. The passages reporting MAM's introduction,
Yeivin's `gaʿya`, or Breuer's `ga'aya` remain unchanged, as do all twelve source-reporting sites
in `doc/foi-mtgmtg-empty-cell.md`. Finding 11.5's separate choice between `hataf` and `ḥataf`
remains unmade.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; the
finished source report remains unchanged, and no outward-facing act, destructive local act,
external configuration write or receipt rewrite occurred.

## Finding 11.2: finding 1's Classification cells name the codices

Recorded by Codex on 2026-09-12. This entry records partial action on finding 11.2: the
Classification-column subunit in finding 1's 31-row table is complete, while finding 11.2's
category label and later prose remain unacted on.

Implementation commit `50f1bf56dc0f311f91641005d4c0f84437059985` on branch
`dual-agent-review-2026-09-10` extends
`doc/meteg-after-silluq-search-in-mam-documentation-update.md` with corrected readings for all
22 applicable Classification cells. The 23 individually checked abbreviations comprise 19 uses
of `L`, corrected to “the LC,” and 4 uses of `A`, corrected to “the Aleppo Codex.” The
Reference, Template, Target and Note columns remain unchanged.

The finished source report remains unchanged at Git blob
`5c4aaf4c61d8f66f95caf65c48a37a9c1d735fba`. The category label corresponding to the original
review's line 60 and the later prose corresponding to its lines 108–146 remain for later tasks;
this entry does not claim that all of finding 11.2 is complete.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; the
finished source report remains unchanged, and no outward-facing act, destructive local act,
external configuration write or receipt rewrite occurred.

## Finding 11.2: finding 2's 23-call category label names the LC

Recorded by Codex on 2026-09-12. This entry records further partial action on finding 11.2. The
finding 2 category label beginning “23: L has a ga'ya to the right of its vowel” is complete;
finding 11.2's later prose remains unacted on.

Implementation commit `b7237bd84f107a8ed7b397871d079ea179087d23` on branch
`dual-agent-review-2026-09-10` extends
`doc/meteg-after-silluq-search-in-mam-documentation-update.md` with the cumulative corrected
reading “23: the LC has a meteg to the right of its vowel (glyph placement).” The category label
was individually checked in finding 2's category list. The correction carries forward finding
11.3's `ga'ya`-to-`meteg` correction and adds only finding 11.2's `L`-to-“the LC” correction.

The finished source report remains unchanged at Git blob
`5c4aaf4c61d8f66f95caf65c48a37a9c1d735fba`. The later prose corresponding to the original
review's lines 108–146 remains for later tasks; this entry does not claim that all of finding
11.2 is complete.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; the
finished source report remains unchanged, and no outward-facing act, destructive local act,
external configuration write or receipt rewrite occurred.

## Finding 11.2: finding 2's parse-failure Judgment cells name the codices

Recorded by Codex on 2026-09-12. This entry records further partial action on finding 11.2. The
Judgment-column subunit in finding 2's 26-row parse-failure table is complete; finding 11.2's
prose after that table remains unacted on.

Implementation commit `9b552fad86ba1cf985d23aff59057b1466d8904a` on branch
`dual-agent-review-2026-09-10` extends
`doc/meteg-after-silluq-search-in-mam-documentation-update.md` with corrected readings for all
seven applicable Judgment cells. The seven individually checked abbreviations comprise six uses
of `L`, corrected to “the LC,” and one use of `A`, corrected to “the Aleppo Codex.” The Reference,
String and Why the parse failed columns remain unchanged.

The finished source report remains unchanged at Git blob
`5c4aaf4c61d8f66f95caf65c48a37a9c1d735fba`. The prose beginning “The 52 NON-verse-final
template calls” and continuing through finding 3's item beginning “Psalms 19:7, where L's one
stroke sits on the first syllable” remains for later tasks; this entry does not claim that all of
finding 11.2 is complete.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; the
finished source report remains unchanged, and no outward-facing act, destructive local act,
external configuration write or receipt rewrite occurred.

## Finding 11.2: the 36 enumerated codex abbreviations are corrected

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 11.2
is unfixed, not acted on or only partly acted on. Finding 11.2 is complete as bounded by the 36
sites that the finding enumerates.

Implementation commit `fa88d68f00e74cc97a714fbead97580da718530f` on branch
`dual-agent-review-2026-09-10` extends
`doc/meteg-after-silluq-search-in-mam-documentation-update.md` with corrected readings for the
five remaining narrative abbreviations. The four individually checked passages begin “The 52
NON-verse-final template calls,” “Psalms 18:46, where L has,” “MAM's editorial rule that where L
has two or more ga'yot,” and “Psalms 19:7, where L's one stroke.” Every `L` in those passages
means the LC.

The earlier entries in the same update file correct 23 abbreviations in finding 1's
Classification cells, one abbreviation in finding 2's category label and seven abbreviations in
finding 2's parse-failure Judgment cells. Those 31 corrections plus the final five narrative
corrections account for all 36 sites named by finding 11.2. The finished source report remains
unchanged at Git blob `5c4aaf4c61d8f66f95caf65c48a37a9c1d735fba`.

Product axis: the correction changes documentation only and reaches no generator or product.
Act axis: both commits are ordinary repository commits on the unpushed review branch; the
finished source report remains unchanged, and no outward-facing act, destructive local act,
external configuration write or receipt rewrite occurred.

## Finding 11.6: the historical filename requires no remediation

Recorded by Codex on 2026-09-12. Finding 11.6 is recorded with no remediation authorized or
required.

The live `doc/PLAN-silluq-before-gaya-template.md` remains `State: live`. Its passage beginning
“The element name deliberately uses `meteg`, not `gaya`” still assigns `meteg` to MAM-simple's
public English vocabulary. Git history shows that commit `772545d5` introduced the plan at its
current path.

The seven in-scope references remain seven path references across four files: one in
`doc/PLAN-meteg-after-silluq-in-uxlc-and-wlc.md`, three in `doc/foi-mtgmtg-empty-cell.md`, one in
`doc/meteg-after-silluq-job-4-12.md`, and two in
`doc/meteg-after-silluq-search-in-mam-documentation.md`. Each reference identifies the existing
plan or uses its path in a command; none states a filename policy. The plan is not renamed, and
this disposition makes no choice among `gaya`, `ga'ya` and `meteg` for filenames.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository commit on the unpushed review branch; no
outward-facing act, destructive local act, external configuration write or receipt rewrite
occurred.

## Finding 18: corrected historical counts require no implementation remediation

Recorded by Codex on 2026-09-12. Finding 18 is disposed of as an evidence-only finding; no
implementation remediation is authorized or required.

A fresh reading of NUL-delimited `git ls-tree -r --name-only -z` output, split only on NUL,
reproduces the corrected historical counts accepted in C6 and turns 3 and 4:

1. Commits `38a606e2`, `c2f238f2`, `f1166057`, `931d6762`, `c36f5baa` and `9d1de074` each have
   1,074 tracked HTML files overall, 1,829 tracked files under `gh-pages/` and 578 tracked HTML
   files under `gh-pages/`.
2. Commit `0354b6cc` has 598 tracked HTML files overall, 1,859 tracked files under `gh-pages/`
   and 579 tracked HTML files under `gh-pages/`.

The NUL-delimited filenames also confirm the two tracked Holman HTML paths named in C6. Ordinary
line splitting treated Git's quoted forms of those paths as filenames whose final character was
a quotation mark, so the original suffix test returned 1,072 rather than 1,074. The same quoted
forms explain the historical `gh-pages/` undercounts. Finding 18.2's inference that two untracked
HTML files accounted for 1,074 is therefore withdrawn in the completed review exchange.

Finding 18.1 remains unverified. The live public tree does not establish the archived run's exact
inputs, and identical bytes in two archived log files do not establish that either log file was
copied. This disposition makes no attribution for how the archived log files arose.

Finding 18 concerns the interpretation of historical evidence, not generator behavior or a
product defect. The numerical correction is already recorded in the completed review exchange,
and finding 18.1 supplies no evidence that selects an implementation change. No historical
finished report is edited.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository commit on the unpushed review branch; no
outward-facing act, destructive local act, external configuration write or receipt rewrite
occurred.

## Finding 8: applicable State defects have declarations

Recorded by Codex on 2026-09-12. This entry supersedes the review's statements that finding 8 is
unfixed or not acted on. It excludes the historical review State lines that D10 of
`doc/dual-agent-review.md` protects and does not add the mechanical check that finding 8 presents
as a separate proposal.

A fresh NUL-delimited `git ls-files -z` census at starting commit `eb79e618` found 25 direct
`doc/PLAN-*.md` files after excluding sibling update files. Nine plans needed effective State
declarations:

1. `doc/PLAN-close-out-review-2026-09-08.md`: `State: executed 2026-09-10` in its new sibling
   update.
2. `doc/PLAN-efficient-wikisource-downloads.md`: `State: executed 2026-09-10` in its existing
   sibling update.
3. `doc/PLAN-evacuate-five-MAM-products.md`: `State: executed 2026-09-10` in its existing sibling
   update.
4. `doc/PLAN-evacuate-public-repos-programme.md`: `State: executed 2026-09-10` in its existing
   sibling update.
5. `doc/PLAN-wikisource-derived-mam-products.md`: `State: executed 2026-09-10` in its existing
   sibling update.
6. `doc/PLAN-worktree-file-consolidation.md`: `State: executed 2026-09-10` in its new sibling
   update.
7. `doc/PLAN-deferred-template-projection-decisions.md`: `State: paused 2026-09-12` at line 3.
8. `doc/PLAN-retire-codex-index-image-work.md`: `State: live` at line 3.
9. `doc/PLAN-retire-google-sheet.md`: `State: live` at line 3.

The first six plans are finished execution records, so D12 leaves all six plans unchanged and
their sibling update files supply the effective declarations. The last three plans describe work
that is paused or live, so the three State lines are kept true in the plans themselves. The
fourth plan added after the review anchor, `doc/PLAN-dispose-mega-pipeline-review-findings.md`,
already begins with `State: live` and needs no correction.

The same census found 21 review files in D10's families. Sixteen historical State lines remain
unchanged under D10's preservation rule. The four files in the 2026-09-10 round use the applicable
initial-argument or later-turn State phrase. The remaining line is
`doc/review-findings-2026-09-08.md`'s `State: remediated 2026-09-10`, last written by `9d1de074`
on 2026-09-10 after `2cddb893` recorded D10 on 2026-09-09. The review's existing sibling update
now supplies the corrected reading `State: acted on 2026-09-10` with the original qualifications.

Implementation commit `d3ab7cf16949c44d5c1d5fe01c53f311d38afadf` makes only those bounded
corrections. `git diff --cached --check` and the tracked-prose mark-order lint passed. The full
suite passed 997 tests, with 5 skipped, in 117.26 seconds. This documentation-only unit does not
owe a mega run.

Product axis: the corrections change documentation only and reach no generator or product. Act
axis: both commits are ordinary repository commits on the unpushed review branch; every finished
plan and review remains unchanged, and no outward-facing act, destructive local act, external
configuration write or receipt rewrite occurred.

## Finding 20.6: backslash paths require no receipt rewrite

Recorded by Codex on 2026-09-12. Finding 20.6 is disposed of as an evidence-only census; no
remediation is authorized or required.

A fresh census read NUL-delimited `git ls-files -z` output, split filenames only on NUL, decoded
each filename as UTF-8 and parsed every tracked direct `in/*.json` file from an explicit UTF-8
read. The census reproduces the finding's exact population: 45 JSON string values, each on a
distinct source line, contain a Windows absolute backslash path such as `C:\...`. A captured log
value containing more than one such path counts once, matching the review's string-line census.
The ten files and their counts are:

1. `in/mam_osis_empty_verification.json`: 2.
2. `in/mam_osis_remove_verification.json`: 9.
3. `in/mam_osis_repoint_verification.json`: 8.
4. `in/mam_osis_stubs_verification.json`: 4.
5. `in/mam_products_phase6a_verification.json`: 2.
6. `in/mam_products_phase6b_verification.json`: 5.
7. `in/mam_products_phase6c_verification.json`: 3.
8. `in/mam_products_phase6d_verification.json`: 2.
9. `in/mam_products_phase6e_verification.json`: 9.
10. `in/mam_products_phase6f_verification.json`: 1.

All 45 values are immutable evidence-receipt data: 39 are structured path or command values and
six are captured `log_text` values. None is reader-facing prose. The same NUL-safe tracked-file
scan found no Python reference to any of the ten receipt filenames, and the tracked Python tree
has no shared consumer for the two filename families. References outside the ten receipts are
finished plan and review records, evidence inventories, and a validation record; no live code
consumes the recorded path values. Converting their separators would rewrite the receipts rather
than correct live input.

`git diff --check` and the tracked-prose mark-order lint passed. The full suite passed 997 tests,
with 5 skipped and 65 subtests passed. This documentation-only disposition does not owe a mega
run.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository commit on the unpushed review branch; no
outward-facing act, destructive local act, external configuration write or receipt rewrite
occurred.

## Finding 20.8: immutable commit messages require no history rewrite

Recorded by Codex on 2026-09-12. Finding 20.8 is disposed of as an immutable-history census; no
remediation is authorized or required.

A fresh check of the cited commits and their Git trees reproduces the four observations:

1. Commit `5e7f0d6b` says that `CLAUDE.md` “holds Hebrew on 126 lines.” The committed
   `5e7f0d6b:CLAUDE.md` blob has 16 lines containing a Hebrew-block codepoint.
2. Commit `74d883d2` says that its twelve configuration files have “13 Hebrew clusters, 0 in
   Unicode-normal order.” The twelve committed files have 13 Hebrew letter clusters with at
   least one combining mark and zero clusters with two or more combining marks. None of the 13
   clusters can distinguish Unicode-normal order from MAM-normal order. Section 3 of the
   finished `doc/assessment-two-stranded-artifacts-2026-09-09.md` correctly says that the files
   are in the prose lint’s scope and are not offenders, but its clean result supplies no
   discriminating mark-order evidence for those files.
3. Commit `5a07e5af` reports 983 passed tests, while commit `7af937fa` reports 984 and calls 983
   “one low.” The commits are on different lines after merge base `63ac5b84`: `5a07e5af` is one
   commit from the merge base, and `7af937fa` is eight commits from the merge base. The parent of
   `7af937fa`, `c65e103d`, contains the newly added
   `test_hand_authored_prose_is_in_mam_mark_order` test. The finished assessment already states
   the historical relationship accurately: 983 passed at `a50da28b`, and 984 were expected on
   the merged tree because the prose lint added one test.
4. Commit `209b4c05` changes 24 rows of `out/vendoring_compare_out.txt` from `eol-only` to
   `identical` and merges the corresponding eight rows of `doc/vendoring-inventory.md` into four,
   while its message names only the Wikisource refresh and pipeline regeneration. Its immediate
   history contains the completed efficiency programme at `b2052ab9`; that programme’s finished
   plan explicitly says that the same generated report changes were preserved in scratch and
   restored rather than included in the programme commits. The live vendoring inventory now
   reports its current three-file population accurately as two `identical` rows.

The four inaccurate or incomplete statements are commit-message history. The assessment and the
efficiency plan are finished dated reports and remain unchanged under D12. The live `CLAUDE.md`,
the prose mark-order lint and the generated vendoring reports require no correction. Rewriting the
commit messages would require a history rewrite, which is neither authorized nor warranted.

`git diff --check` and the tracked-prose mark-order lint passed. The full suite passed 997 tests,
with 5 skipped and 65 subtests passed, in 111.21 seconds. This documentation-only disposition
does not owe a mega run.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository commit on the unpushed review branch; no history
rewrite, outward-facing act, destructive local act, external configuration write or receipt
rewrite occurred.

## Finding 20.1: term-of-art uses remain and the Ben attribution is explicit

Recorded by Codex on 2026-09-12. Finding 20.1 is complete.

Ben's 2026-09-04 commit `b4706759` says that `script-regenerable` supersedes an authorship claim
when a script reproduces an artifact, while `Ben-written` and `Claude-written` remain useful for
artifacts that no script reproduces. The same message expressly says that this refinement is not a
rename: “hand-authored” remains an unambiguous lint-scope term meaning “not emitted by a script,”
and no repository-wide sweep is proposed. The review's phrase “against the 2026-09-04 vocabulary”
therefore does not supply a mechanical replacement rule.

A fresh live-tree census gives these dispositions:

1. Commit `3134f32b` already corrected the three source descriptions cited in the finding.
   `py/main_pipeline_graph.py` now calls `MAM-process.dot` Ben-written, and
   `py/main_0_mega.py` describes the structured specification without an authorship claim and
   calls `MAM-process.dot` Ben-written. The three cited spellings are absent from both modules.
2. The finding's two `CLAUDE.md` anchors now occur at lines 24 and 49. Both use “hand-authored” as
   the mark-order lint's term of art. The live instruction file has two additional occurrences of
   the same term at lines 69 and 166; both make the same generated-or-captured distinction. All
   four remain. The historical “hand-maintained” test-registry description at line 992 states the
   maintenance method rather than an unknown authorship and also remains.
3. `py/tests/test_prose_mark_order.py` still has exactly five occurrences of “hand-authored,” at
   lines 1, 6, 41, 45 and 176. Line 1 names the lint's scope; line 6 quotes the instruction that
   motivated the lint; line 41 distinguishes captured note HTML from prose; line 45 distinguishes
   external input from prose; and line 176 states the lint failure. All five retain the term of
   art. The adjacent line 56 called the edition-transcription headers “hand-written” and
   immediately identified their contents as Ben's notes. Commit `c8ba9f00` changes that live
   docstring to “Ben-written.”
4. The finished `doc/PLAN-wikisource-derived-mam-products.md` and frozen
   `doc/mam-products-phase6-command-map.md` each have one “hand-authored” occurrence, both
   distinguishing source from generated output. The finished
   `doc/assessment-two-stranded-artifacts-2026-09-09.md` has ten literal “hand-authored”
   occurrences and one “hand-written” occurrence, rather than a literal population of nine. The
   occurrences at lines 66, 68 and 175 quote earlier instruction text. Lines 89, 93, 117, 176,
   233, 234 and 553 use the generated-or-captured classification. The “hand-written” occurrence
   at line 116 describes Ben's notes in a header that is never regenerated, so
   `doc/assessment-two-stranded-artifacts-2026-09-09-update.md` records that the phrase should be
   read as “Ben-written header.” D12 leaves all three finished documents unchanged.

Black left the edited Python file unchanged. `git diff --check` and the tracked-prose mark-order
lint passed; the lint passed 1 test. The full suite passed 997 tests, with 5 skipped, in 114.05
seconds. The source change is a docstring correction and reaches no generator or generated
product, so this unit does not owe a mega run.

Product axis: the correction changes a code docstring and documentation only; it reaches no
generator or product. Act axis: the commits are ordinary repository commits on the unpushed
review branch; all finished dated documents remain unchanged, and no outward-facing act,
destructive local act, external configuration write or receipt rewrite occurred.

## Finding 20.11: inline-code link examples require no remediation

Recorded by Codex on 2026-09-12. Finding 20.11 is complete as an evidence-only disposition.

A fresh live-tree inspection gives these dispositions:

1. The tracked canonical `dot-claude/user-wide-CLAUDE.md` has the cited text at line 1416, and
   the live `C:/Users/BenDe/.claude/CLAUDE.md` has the same text at line 1416. The two files are
   byte-identical at SHA-256
   `F32191A794596500297D4B566DAE98BEDCB126D00821B2BDCD880FFB438D0D18`.
2. The tracked canonical `dot-Codex/user-wide-AGENTS.md` has the cited text at line 1197, and
   the live `C:/Users/BenDe/.Codex/AGENTS.md` has the same text at line 1197. The two files are
   byte-identical at SHA-256
   `577320F67CB32E2910D1DA269899814B5E44771D2D78E4E46D43321BAA3AECFC`.

Both occurrences of `[page](gh-pages/accgram/page.html)` are enclosed by backticks, so CommonMark
parses each occurrence as an inline-code example rather than as a link. The surrounding sentence
explicitly calls the repo-relative spelling “the wrong thing here.” The nonexistent target is
therefore part of the negative example. Replacing the target with an existing page would make the
example contradict the instruction it illustrates.

The positive `file:///C:/Users/BenDe/GitRepos/MAM-basics/gh-pages/wlc/accgram/maqaf-nonfinal-accents.html`
example occurs in a fenced code block in each instruction file, and the named file exists in both
the primary clone and the review worktree. No tracked Markdown-link checker exists in the live
tree; the review-only `md_links_check.py` named by the finding treated inline code as links. No
checker weakening, exclusion or mechanical gate is warranted.

The same review census separately identifies
`misc/what-is-mam/img/provenance-misc.md:6` as a dead link. That occurrence is an ordinary
reader-facing Markdown link, its target
`.github/prompts/capture-what-is-mam-slides.prompt.md` is absent, and commit `84a801f4` deleted the
target. The dead provenance link is pre-existing and is not one of finding 20.11's two instruction
examples, so this narrow unit leaves the dead provenance link unchanged.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped and 65 subtests passed, in 113.28 seconds. No Python file
changed, and this documentation-only disposition does not owe a mega run.

Product axis: this disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository change on the unpushed review branch; the tracked
canonical instruction files, the live user-level copies, every finished dated document and the
dead provenance link remain unchanged. No outward-facing act, destructive local act, external
configuration write or receipt rewrite occurred.

## Finding 11.5: `hataf` versus `ḥataf` still needs Ben's decision

Recorded by Codex on 2026-09-12. Finding 11.5 is re-established and remains decision-pending; no
prose spelling has been selected.

At checkpoint `974395f9f2fabf69eee147c1764886a7c8e28ec0`, after current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was confirmed already merged, a fresh census used
NUL-delimited `git ls-files -z` for the tracked-Markdown population. Each table entry gives
literal sites followed by lines containing a site:

| Finished report | `xataf` | `hataf` | `ḥataf` |
|---|---:|---:|---:|
| `doc/meteg-after-silluq-screen-against-uxlc-and-wlc.md` | 7 / 4 | 0 / 0 | 0 / 0 |
| `doc/meteg-after-silluq-search-in-mam-documentation.md` | 6 / 5 | 3 / 3 | 0 / 0 |
| `doc/meteg-after-silluq-koren-lookup-candidates.md` | 1 / 1 | 10 / 5 | 0 / 0 |
| `doc/meteg-after-silluq-in-uxlc-and-wlc.md` | 0 / 0 | 2 / 2 | 0 / 0 |
| `doc/meteg-after-silluq-job-4-12.md` | 0 / 0 | 3 / 3 | 0 / 0 |
| `doc/meteg-after-silluq-psalms-72-15.md` | 0 / 0 | 6 / 2 | 0 / 0 |

The six reports therefore have 24 plain-`hataf` sites on 15 lines. They also have 14 `xataf`
sites on 10 lines: 13 sites on 9 lines are prose in the screen and search reports, while the
remaining site is the identifier path `py/explicit_xataf/extract.py` in the Koren-candidates
report. None of the six reports has `ḥataf`.

Outside the six reports and the remediation records that merely discuss finding 11.5, the
`ḥataf` population remains seven sites on six lines:

1. `doc/mega-pipeline-review-findings-public-2026-09-01.md:126, :128, :130` has three
   `explicit-ḥataf` sites.
2. `doc/mega-pipeline-review-phase-13-2026-09-01.md:148` has one `explicit-ḥataf` site.
3. `doc/metsudah-vs-ctr.md:237` has one `ḥataf qamats` site.
4. `misc/mam-is-a-dataset/script.md:19` has `ḥataf` and `ḥataf pataḥ` on the same line.

Before this entry, five further `ḥataf` sites merely discussed the unresolved choice:
`doc/review-findings-2026-09-10.md:626`,
`doc/meteg-after-silluq-search-in-mam-documentation-update.md:93`, and
`doc/review-findings-2026-09-10-update.md:55, :163, :185`. The pre-entry tracked-Markdown total at
the checkpoint was consequently 12 literal sites on 11 lines; only the seven sites on six lines
listed above use `ḥataf` as the prose term rather than as the subject of this review.

The authority check does not select between the two prose alternatives:

1. Commit `9e3aed3424b2cbe00cb2334360125f4ae0243666` of 2026-03-25 is the only matching commit
   message that explicitly maps `hataf` to `ḥataf` in prose and `xataf` in identifiers. The
   commit has a Claude coauthor trailer and does not attribute that editorial choice to Ben.
   Later report commits introduced the plain spelling without declaring a reversal. The
   historical commit is evidence for `ḥataf`, not an explicit Ben decision.
2. The current `py/tests/test_transliterations.py` docstring describes het-as-plain-`h` forms as
   retired, but the live denylist has no `hataf` pattern and scans Python rather than Markdown.
   The current user-level Claude and Codex instructions, `CLAUDE.md`,
   `doc/dual-agent-review.md`, and the live `hebrew-prose` skill have no `hataf`, `ḥataf` or
   `xataf` occurrence that selects the prose spelling.
3. `py/accgram/printed_decalogue_strands.py` single-sources its rendered names and has
   `ROM_PATAX = "pataḥ"`, but it has no `ROM_HATAF`. Its `SCOPE` paragraph makes the `ROM_*`
   convention specific to the printed-Decalogue pages. Extending either the dotted consonant or
   the single-sourcing table to `hataf` would be a new editorial choice.

Ben still needs to choose `hataf` or `ḥataf` for prose. The 13 historical prose sites with
`xataf` are not a third candidate; after Ben selects the prose spelling, sibling update files can
give the corrected readings for the six finished reports. D12 leaves all six reports unchanged,
and no sibling correction file is created before the replacement is approved.

`git diff --check` and the tracked-prose mark-order lint passed. The full suite passed 997 tests,
with 5 skipped and 65 subtests passed. This documentation-only disposition reaches no generator
or product and does not owe a mega run.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository change on the unpushed review branch; all six
finished reports remain unchanged, and no outward-facing act, destructive local act, external
configuration write or receipt rewrite occurred.

## Finding 20.9: crop-coordinate filename policy still needs Ben's decision

Recorded by Codex on 2026-09-12. Finding 20.9 is re-established and remains decision-pending; no
image has been adjudicated, no coordinate has been newly confirmed, no crop has been renamed and
the live naming rule has not been tightened.

At checkpoint `bea962688e6153bac935995d4fd0e490916bd640`, after current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was confirmed already merged, the live evidence is:

1. `leningrad/page-snips/README.md` still permits the
   `<folio><side>-col<N>-line<N>-<ref>-<slug>.png` form “when the line has been read off the image”
   and uses the coordinate-free form when the line has not been read. The rule conditions the
   coordinate-bearing name on the line; the rule does not say that every encoded coordinate must
   have been independently confirmed.
2. The tracked Psalms crop remains
   `leningrad/page-snips/380A-col2-line3-Ps72v15-yevarkhenhu.png`. Its README entry says that Ben
   read line 3 from the image and that column 2 is the estimator's, not an independently confirmed
   column. Commit `b97a2100af5d63671203dcf0d110eb741b2f0375`, which introduced the crop, states
   both facts and calls the same arrangement the Lamentations 2:3 precedent.
3. The tracked Lamentations crop remains
   `leningrad/page-snips/430B-col2-line10-Lam2v3-akhla.png`. Its README entry says that Ben read
   line 10 from the image and that column 2 is still the estimator's. A rule requiring independent
   confirmation of every coordinate would therefore affect the Lamentations crop as well as the
   Psalms crop.
4. Commit `9eff3d0044ad097d2c050bd1a4d9f9e75bc46ae0` is still the latest commit that changed
   `leningrad/page-snips/README.md`. Its subject says “a name has a line only if read,” and it
   removed the coordinates from the Job 4:12 crop because neither the column nor the line had been
   read from the image. It did not remove either crop whose line had been read.
5. A search of the post-`9eff3d00` repository history and the current repository, Codex and Claude
   instruction files found no later explicit Ben decision requiring independent confirmation of
   every coordinate. The later matching entries are the dual-agent review records themselves:
   C4 and turn 3 both call the stronger rule Ben's choice, and the reconciliation table calls the
   stronger rule undecided.

Ben still needs to choose between two policies:

1. **Keep the live rule.** Reading the line authorizes the coordinate-bearing filename. An
   estimator-supplied column may remain in the filename when the README discloses that the column
   is unconfirmed. Both current coordinate-bearing filenames comply and require no remediation.
2. **Require independent confirmation of every encoded coordinate.** An estimator-supplied column
   may not remain in a filename merely because the line was read. The Psalms and Lamentations
   crops would then need a later, explicit disposition: independently confirm each column or adopt
   and apply a filename form that does not assert the unconfirmed column.

Until Ben selects a policy, the live README, the three crop filenames and all finished dated
documents remain unchanged. This documentation-only disposition reaches no generator or product
and does not owe a mega run.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository change on the unpushed review branch; no
outward-facing act, destructive local act, external configuration write or receipt rewrite
occurred.

## Finding 7.1, Phase 6 map, September 8 review and close-out plan: no missing `.novc` dependency remains

Recorded by Codex on 2026-09-12. This entry classifies only the live `.novc` references in
`doc/mam-products-phase6-command-map.md`, `doc/review-findings-2026-09-08.md` and
`doc/PLAN-close-out-review-2026-09-08.md`. It does not establish a rule for the rest of finding
7's census.

At checkpoint `a94ee16e703c768838b4b58c4d239c68623c1632`, after current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was confirmed already merged, each assigned document
has 4 lines containing `.novc`. Their Git blobs are
`741485b0672a6985712ec9a7025d6528547b5cd0`,
`3df541234f0952f17efce6c5b897af7ff7451f11` and
`baccee1bdf429519314ea7a5252ea495e0bf98f9`, respectively. The command map has no sibling update.
The existing `doc/review-findings-2026-09-08-update.md` and
`doc/PLAN-close-out-review-2026-09-08-update.md`, at Git blobs
`d38316952314a11182beaab2ce8b2004740aea77` and
`69b989ec30fe319b13a27cc13eb04ada439b7b23`, correct unrelated State and display-fallback
passages and supply no scratch artifact.

The 12 lines have these classifications:

| Finished document and searchable anchor | Lines in the live tree | Classification |
|---|---:|---|
| `mam-products-phase6-command-map.md`: “The directories are” | 130–132 | Reproducible commands and disposable outputs. The tracked `in/mam_products_phase6_baseline.json` preserves the full `build` and `check` argument arrays, exact redirect-manifest inputs and every `scratch_stub_paths` member for all five directories. The live `py/main_redirect_stubs.py` and `py/redirect_stubs/stubs.py` implement those commands. Each `.novc` directory is regenerated output, not an input. |
| `mam-products-phase6-command-map.md`: “Use a uniquely named `.novc/` Python file” | 177 | Reproducible method and temporary implementation choice. The plan gives the exact NUL-delimited `git ls-tree` command above this line and the byte-count, SHA-256 and Git-object checks below it; the tracked baseline preserves the sets and file records being checked. No particular scratch filename or unrecorded predicate is required. |
| `review-findings-2026-09-08.md`: “and `give_std_mark_order` put them back” | 71 | Historical provenance and reproducible method. The finished review already contains the corrected bytes. The tracked `give_std_mark_order` and `has_std_mark_order` implementation remains in `py/mb_cmn/uni_denorm.py`, and `py/tests/test_prose_mark_order.py` now checks the finished review. The primary clone still has `fix_findings_marks.py`, but that writer is not an input to the document or the lint. |
| `review-findings-2026-09-08.md`: “Every script and output is untracked under” | 145 | Historical evidence-location and naming record. The line identifies the completed review's four stream prefixes and main-session bundle. The review's tracked scope, findings, reconciliation and dispositions preserve the conclusions; no current Python path invokes this directory. The primary clone still has the evidence bundle, but no tracked result or current method takes the bundle as input. |
| `review-findings-2026-09-08.md`: “`9e6e9e17`'s ‘415 files’” | 558 | Historical evidence-inventory result. The primary clone's `review-2026-09-07` directory still has exactly 416 files, including `commit_msg_review_findings_2026_09_07.txt`; commit `9e6e9e173d179aa3ddea2b2217f5798e6f1a3e94` preserves the earlier 415-file statement. The corrected count describes that completed bundle and is not an input to a live operation. |
| `review-findings-2026-09-08.md`: “or `.novc/review-2026-09-08/` script that re-establishes it” | 756 | Reproducible-method index and historical evidence pointer. The review states the fixed Git ranges, each finding's population and measurement, and the plain Git commands where a command suffices. The named throwaway scans implement those stated checks; every specifically named re-establish artifact checked for this classification remains in the primary copy. The tracked reconciliation and dated dispositions preserve the accepted conclusions, and no unrecorded semantic partition comparable to finding 7.2's first-match predicates was found. |
| `PLAN-close-out-review-2026-09-08.md`: “Turn-5 scripts” | 108 | Historical evidence pointer. The old worktree is gone, but all three named scripts and both reports remain in the primary clone's copied review directory. The tracked turn-5 document gives the Git commands and findings those files checked; finding 7's earlier singleton classification records that the verdicts depend on tracked files and Git history rather than on the verification scripts. |
| `PLAN-close-out-review-2026-09-08.md`: “integration-receipt.json” and “ignored `.novc/review-remediation-2026-09-08/` evidence” | 1177 and 1208 | Historical receipt pointer and preservation instruction. The source directory disappeared with the retired worktree, as planned, but its 6,208 files survive in the verified external evidence archive and manifest named at lines 1211–1213. The archive's current SHA-256 is `33495ad7b7d0b040719ded27ff5544a75efb2f19c0c971c4d333a790dbb523ce`, equal to the manifest, and the manifest inventories `wave4-01a08b71/integration-receipt.json`. The receipt is preserved evidence, not a missing dependency. |
| `PLAN-close-out-review-2026-09-08.md`: “the ignored `.novc/review-2026-09-08/` does not count” | 1232 | Historical retirement instruction and evidence-location note. The statement explains Git's worktree-removal behavior and points back to the primary copy of the turn-5 files, which still exists. The worktree and branch named by the completed instruction are gone; no current operation depends on the old ignored directory. |

No `.novc` artifact named or described by these lines is an indispensable missing dependency of a
tracked result or method. The close-out evidence remains deliberately external and verified; it
must remain unchanged as a receipt. No further Ben decision arises from this unit, and D12 leaves
all three finished documents and both existing sibling updates unchanged.

This evidence-only disposition reaches no generator or product and does not owe a mega run.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped and 65 subtests passed, in 81.12 seconds.

Product axis: this classification changes only the review's live sibling update and reaches no
generated MAM product. Act axis: the write is an ordinary repository change on the unpushed review
branch; no outward-facing act, destructive local act, external configuration write or receipt
rewrite occurred.

## Finding 7.2: the two finished reports have one missing exact-replay dependency

Recorded by Codex on 2026-09-12. This entry classifies only the `.novc` references in
`doc/meteg-after-silluq-screen-against-uxlc-and-wlc.md` and
`doc/meteg-after-silluq-search-in-mam-documentation.md`. It does not establish a rule for the
rest of finding 7's census.

At checkpoint `c141f54105e12042150b16b81cf521685071d7be`, after current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was confirmed already merged, each finished report
has 23 lines containing `.novc`. The current worktree has none of the named `mas_a_*` or
`mas_b_*` files. The screen report's named worktree,
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/zen-babbage-2d6583`, no longer exists. The
screen report remains unchanged at Git blob `09ac3f23175aacb1ffb10c39894b3c2d2fe78912`.
The documentation-search report remains unchanged at Git blob
`5c4aaf4c61d8f66f95caf65c48a37a9c1d735fba`.

The 23 screen-report lines have these classifications:

| Searchable anchors in the finished screen report | Lines in the live tree | Classification |
|---|---:|---|
| “Written by `.novc/mas_b_write_doc.py`” | 3 | Historical provenance. The sentence identifies the writer that lifted the Hebrew forms and made the finished report; D12 gives no current process a reason to regenerate that report. |
| `mas_b_syllables.py`, `mas_b_screen.py`, `mas_b_mgketer.py`, `mas_b_nuclei.py`, `mas_b_write_doc.py`, `mas_b_verify_members.py` and `mas_b_peek_no_sopa.py` in the analytic sections | 22, 31–32, 59, 65, 85, 96, 101, 251, 268 and 313 | Reproducible methods. Sections 1, 3 and 11 state the inputs, loader rules, verse-final-chanted-word rule, alignment, position comparison, classes, calibration and syllable criterion. The missing filenames identify the implementations used in 2026; the methods do not require those implementations. |
| “listed in `.novc/mas_b_mgketer_report.txt`” | 276 | Filename inventory. The missing intermediate report held the 17-item skip list; the screen report states the count and the reason for the skips, and the list can be re-derived by section 11's method. |
| “All are gitignored under `.novc/`” and the nine `.novc/mas_b_*.py` command lines | 318, 329, 333, 337, 341, 345, 349, 353, 357 and 361 | Historical command record. The commands name the order and environment of the completed run. The old worktree is gone, so the commands are not runnable instructions in the live tree. Lines 364–381 preserve what each command did and which intermediate files it made. |

The screen method has a concrete tracked replacement for the unavailable scripts. Commit
`6ca009a583805283c4dd695adf465fff8056f774` changed the live
`doc/PLAN-meteg-after-silluq-in-uxlc-and-wlc.md` to call the screen report's section 11 “the
method of record for loading and aligning all three.” The MAM-simple, UXLC 3.9, WLC 4.22 and WLC
4.20 inputs and the named `accgram` helpers all exist at the report's pinned MAM-basics commit
`30fb7681`. Phonetic MAM exists at the pinned MAM-private commit
`3f53991ca85d0b53b0e9291d670299f4f4b5c6db`. Git history identifies
`3025e8221d05a624071dccba0eecd10bbd4c3d1c` as the last MAM-private commit affecting
`mgketer/out/` before the report was committed. No `.novc` file is indispensable to repeating
the screen as a new measurement from those tracked inputs.

The 23 documentation-search-report lines have these classifications:

| Searchable anchors in the finished documentation-search report | Lines in the live tree | Classification |
|---|---:|---|
| `mas_a_compare_a06_ws_report.txt`, `(c')` in `mas_a_ws_docnotes_report.txt` and `mas_a_intro_grep_report.txt` | 16, 135 and 139 | Filename inventory. These are missing intermediate views of the completed run. The report states the compared sets, the 52-call disposition, the eight introduction-search terms and the four filtered views. |
| `mas_a_stress_after_census.py` and `mas_a_stress_classify.py` in the analytic sections | 72 and 87 | Reproducible methods. The report states Ben's syllable definition, the census population and classifications, and the candidate rule; the classification uses the tracked `py/accgram/post_stress_meteg.py` parser. The historical Phonetic MAM input remains available at `3f53991ca85d0b53b0e9291d670299f4f4b5c6db`. |
| “the test for each is in `.novc/mas_a_write_doc.py`” | 56 | Indispensable missing dependency for exact replay of the ten first-match category counts. The report lists category names and totals, but no tracked file preserves the predicates or the precedence behavior when one call matches several predicates. Reimplementation without those decisions could produce a different partition while preserving the same 166-call population. |
| “All scripts are gitignored under `.novc/`” and the eight `.novc/mas_a_*.py` command lines | 241, 250, 256, 262, 268, 274, 280, 286 and 292 | Historical command record. The commands identify the completed run's environment and order; no live operation invokes them. |
| The eight numbered `.novc/mas_a_*.py` descriptions | 247, 253, 259, 265, 271, 277, 283 and 289 | Method and filename inventory. The entries say what was scanned, cross-checked, classified or looked up and name the intermediate files. The tracked inputs exist at MAM-basics commit `30fb7681` and MAM-private commit `3f53991ca85d0b53b0e9291d670299f4f4b5c6db`; the live tree also has the tracked Wikitext parser and the post-stress-meteg parser. The writer reference is historical provenance except for the missing first-match predicates identified above. |

Neither finished report has a statement that no `.novc` dependency remains. Finding 7's example
of that category is `doc/meteg-after-silluq-in-uxlc-and-wlc.md`, outside this classification.
The later sibling update files correct terminology and presentation but preserve no `mas_a_*` or
`mas_b_*` implementation, so they do not close the exact-replay gap.

Ben still needs to choose the disposition for the missing first-match predicates:

1. **Restore exact remeasurement.** Reconstruct the predicates from the original task evidence,
   review every semantic choice, and preserve the approved implementation in tracked source
   behind a repository entry point.
2. **Keep the counts as historical results.** Add a later correction to
   `doc/meteg-after-silluq-search-in-mam-documentation-update.md` saying that the ten category
   counts cannot now satisfy the finished report's “Re-measure rather than trust” instruction.

Until Ben chooses, no predicate has been reconstructed, no script has been added, and neither
finished report nor either sibling update file has been changed. This evidence-only disposition
reaches no generator or product and does not owe a mega run.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped, in 76.12 seconds.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository change on the unpushed review branch; both finished
reports remain unchanged, and no outward-facing act, destructive local act, external
configuration write or receipt rewrite occurred.

## Finding 7.1, mega-coverage pair: no missing `.novc` dependency remains

Recorded by Codex on 2026-09-12. This entry classifies only the `.novc` references in
`doc/PLAN-mega-coverage.md` and `doc/mega-coverage-2026-09-10.md`. It does not establish a rule
for the rest of finding 7's census.

At checkpoint `8e2db58f6fd3b7fd30bd3c71951167871637f294`, after current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was confirmed already merged, the finished plan has
2 lines containing `.novc` and the finished report has 3. The plan's named worktree,
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/mega-coverage`, no longer exists. The plan
remains unchanged at Git blob `dee11fb218d56f77ab780a7e1a7528322daa464b`; the report remains
unchanged at Git blob `9b0a26f459fc340c4e046403cd41340dd9220fd4`. The existing
`doc/PLAN-mega-coverage-update.md` changes only Phase 7's run-mode sentence and supplies no
missing scratch artifact.

The five lines have these classifications:

| Searchable anchor in the finished plan or report | Lines in the live tree | Classification |
|---|---:|---|
| Plan: “Throwaway scripts and message files go under” | 51 | Historical method. The sentence records where each completed phase put temporary working files; it points to no particular file and preserves no input or result. |
| Plan: “The scratch evidence is in the worktree's `.novc/mega-coverage-phase5b/ctr/`” | 226 | Historical evidence pointer. The directory and its worktree are gone, but no indispensable dependency is missing. The plan's Phase 5c item 2 records the accepted narrow-sense paseq-template mapping, the 84-entry result and the five changed records; Phase 5c's completion record names commit `9fa80e1162c8dc9a0c3f9a93dd1507ca755d92f3`. That commit preserves the handler, mega step and exact `out/diff_ctr_mam.json` diff, and the handler and step remain in the live tree. |
| Report: “a measurement written only to `.novc/`” | 137 | Reproducible method and output policy. The tracked `survey-breuer-zaqef-units` entry point regenerates `.novc/breuer-zaqef-units.json`; `.novc` is the destination, not an input. The separately stated Phonetic MAM dependency remains explicit and is not a missing `.novc` dependency. |
| Report: “read Holman's untracked mailboxes under `.novc/`; the reports regenerate from the tracked derivatives” | 154 | Statement that no report-regeneration dependency remains. The mailboxes are intentionally per-machine inputs needed only to ingest a new message. Existing reports regenerate from `holman/emails/` and `holman/docs-not-served/mam_suggestions.json`, as `CLAUDE.md`, the two tracked path accessors and the cited evacuation plan state. |
| Report: “debugging output to `.novc/`; the tracked half of the run is `parse-ws`'s” | 181 | Reproducible method and disposable output. The tracked `py/main_parse.py ws --write-fmt-1` path writes `.novc/mam-ws-parsed-fmt-1/`; the normal parse path writes the tracked format-2 and production outputs. The format-1 directory is re-created output, not an input or evidence dependency. |

No line in this pair is a filename inventory, and no `.novc` artifact is indispensable to a
tracked result or method asserted by this pair. Holman's mailboxes remain indispensable only for
future ingestion of the messages they contain; that intentional per-machine input boundary is
already tracked and requires no new decision. No correction to either finished document and no
addition to its sibling update is warranted.

This evidence-only disposition reaches no generator or product and does not owe a mega run.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped, in 77.58 seconds.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository change on the unpushed review branch; both finished
documents and the plan's sibling update remain unchanged, and no outward-facing act, destructive
local act, external configuration write or receipt rewrite occurred.

## Finding 7.1, five singleton documents: no missing `.novc` dependency remains

Recorded by Codex on 2026-09-12. This entry classifies only the single live `.novc` line in each
of `doc/assessment-two-stranded-artifacts-2026-09-09.md`,
`doc/codex-review-findings-2026-09-08-claude-turn-5.md`, `doc/foi-mtgmtg-empty-cell.md`,
`doc/user-level-config-in-cloud-sessions.md` and
`doc/meteg-after-silluq-in-uxlc-and-wlc.md`. It does not establish a rule for the rest of finding
7's census.

At checkpoint `e13ebba2e71e3f81fa54e04d209f9f1804ed37c1`, current `main` was already merged. The five
documents have Git blobs `f6fdd5591aeabd0a18894968eb1e493e754045ae`,
`211802245bf15d6a21b1670c450f410c9f0ad98b`, `591e14fcaa1cf734c0776887020573fdadcc48f2`,
`d7bde24203e46f12a748f365f398d4308f0f9a54` and
`fad8f1836286e3fbb76ce0da39918f23cdb9e4b9`, respectively. None has a sibling update file.

| Finished document and searchable anchor | Live line | Classification |
|---|---:|---|
| `assessment-two-stranded-artifacts-2026-09-09.md`: “the three measurements that needed a script” | 568 | Reproducible method and historical execution record. Section 9 names the interpreter, import, predicates, revisions, pathspecs and outputs, then explicitly tells a fresh session to rewrite the throwaway scripts because the preceding sections contain the whole method. Commit `847862f9ef0f6276e827b86a59ef5b6bc7d7cebb` records the same four evidence groups and their results. |
| `codex-review-findings-2026-09-08-claude-turn-5.md`: “The scripts are untracked at” | 52 | Historical evidence pointer. The unavailable filenames say where the completed review read its figures; the following sentence states that every citation also gives the plain Git command that re-establishes the figure. The verdicts depend on the cited tracked files and Git history, not on either verification script. |
| `foi-mtgmtg-empty-cell.md`: “The census scripts are gitignored” | 107 | Filename inventory and reproducible quantitative method. The section names each script's population, the tracked `wt_qere` handlers and the report role. Its numbered clauses state the counts, partitions, formulas, reduced-vowel control, consonantal-skeleton and stem comparisons, and verse-position comparison. The tracked `py/foi/foiz_wt_mtgmtg.py` handler and `gh-pages/MAM-with-doc/foi/foi-mtgmtg.json` preserve the survey population and partition; the document's regeneration command re-derives them. Commit `d99f2cf4134ac7691c3e10a58053ceb2d575180e` also records that the three evidence strands are re-derivable from the file. `verify_doc_claims.py` was a completed-run check, not an unrecorded semantic policy. |
| `user-level-config-in-cloud-sessions.md`: “The harness was a throwaway under `.novc/`” | 209 | Reproducible method and historical test record. Lines 206–210 enumerate all six fake-home cases, and the tracked `.claude/hooks/install-user-config.sh` remains the subject under test. The separately recorded real-cloud and live-home exercises are historical environment measurements, not outputs whose only evidence is the scratch harness. |
| `meteg-after-silluq-in-uxlc-and-wlc.md`: “checked that nothing in the file points into a `.novc` directory” | 118 | Statement that no dependency remains. The occurrence denies a `.novc` pointer and describes a completed writer check. Sections 9 and 10 preserve the data sources, method, calibration and tracked verse-link command. |

No `.novc` file named or described by these five lines is indispensable to a tracked result or
method. No further Ben decision arises from this five-document unit, and D12 leaves all five
finished documents unchanged.

This evidence-only disposition reaches no generator or product and does not owe a mega run.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped and 65 subtests passed, in 77.21 seconds.

Product axis: this classification changes only the review's live sibling update and reaches no
generated MAM product. Act axis: the write is an ordinary repository change on the unpushed review
branch; no outward-facing act, destructive local act, external configuration write or receipt
rewrite occurred.

## Finding 10: Aleppo crop license-notice wording still needs Ben's decision

Recorded by Codex on 2026-09-12. Finding 10 is re-established and remains decision-pending; no
license wording, image license or crop has been changed.

At checkpoint `217fd9086eddc03af6e480e1895a03eefe3f25fe`, after current `main` at
`f079523148ae4892bec3b313dd43b3b627c1a2a9` was confirmed already merged, the live evidence is:

1. `DATA-LICENSES.md:92` still has the path cell “`aleppo/`, except `aleppo/aleppo-pages/` and
   `aleppo/aleppo-wiki/`.” Its content cell names “line and column data annotated by Ben
   Denckla, derived reports, procedures, and provenance records”; its terms cell names “Ben
   Denckla's compilation and analysis.” The path cell does not exclude `aleppo/page-snips/`, and
   neither descriptive cell names photographic crops.
2. `DATA-LICENSES.md` still has no row specific to `aleppo/page-snips/`.
   `DATA-LICENSES.md:95` separately covers `leningrad/page-snips/` as “crops that Ben Denckla
   made from Leningrad Codex photographs,” under “each rights holder's; no grant is made or
   implied here,” and says that the crops are reproduced as evidence for the manuscript readings
   documented beside them.
3. `aleppo/page-snips/` currently contains two PNG crops and its README. The README records Ben's
   2026-09-10 judgment that tiny crops like these are kept as fair use, says that each section
   identifies the crop's author and source image, and says that Ben's crops come from mgketer.org
   unless he says otherwise. Both crop sections identify Ben and an mgketer.org image.
4. `ca0b4d02064280c19907d47b788fb9b83f82e70d` introduced the directory and the first crop at
   20:26 on 2026-09-10; `7d40fa06c776e5e74e6034799508b3c57d23ba81` added the second at 20:55.
   The latest commit to `DATA-LICENSES.md` is still
   `7fa58d7345eafa5a9903a5e7be7bf23aadb8bb99` at 18:10 that day, before either crop arrived.
5. The reconciliation confirms a notice-coverage mismatch and leaves reader-facing license
   wording as an editorial proposal. Ben's later wording approval in
   `ad73ec3a750cc85f7beb77276b14f946ae132d20` changes the finding's lead to “Licence coverage
   gap,” names the Leningrad row as the row a remedy would copy, and says that Ben had not asked
   for remediation. A search of later repository history and the current repository, Codex and
   Claude instructions found no later explicit Ben decision selecting the table wording.

Ben still needs to choose between two concrete table treatments:

1. **Add a dedicated Aleppo-crops row.** Change the catch-all path cell to the following text,
   then add the proposed row beside the other Aleppo rows:

   ```markdown
   `aleppo/`, except `aleppo/aleppo-pages/`, `aleppo/aleppo-wiki/` and `aleppo/page-snips/`
   ```

   ```markdown
   | `aleppo/page-snips/` | crops that Ben Denckla made from Aleppo Codex photographs shown by mgketer.org | **each rights holder's; no grant is made or implied here.** The crops are reproduced as evidence for the manuscript readings documented beside them |
   ```

2. **Use one row for both codices' crop directories.** Make the same change to the Aleppo
   catch-all path cell, then replace the existing Leningrad row with this shared row:

   ```markdown
   | `aleppo/page-snips/`, `leningrad/page-snips/` | crops that Ben Denckla made from Aleppo and Leningrad Codex photographs | **each rights holder's; no grant is made or implied here.** The crops are reproduced as evidence for the manuscript readings documented beside them |
   ```

Neither alternative repeats the Aleppo README's fair-use statement in `DATA-LICENSES.md`.
Repeating that statement in the root license notice would be a separate reader-facing wording
decision. Until Ben selects the table treatment, `DATA-LICENSES.md`, both crop directories, all
images and all finished dated documents remain unchanged. This documentation-only disposition
reaches no generator or product and does not owe a mega run.

`git diff --check` and the tracked-prose mark-order lint passed; the lint passed 1 test. The full
suite passed 997 tests, with 5 skipped and 65 subtests passed, in 76.82 seconds.

Product axis: the disposition changes a review update only and reaches no generator or product.
Act axis: the write is an ordinary repository change on the unpushed review branch; no
outward-facing act, destructive local act, external configuration write or receipt rewrite
occurred.
