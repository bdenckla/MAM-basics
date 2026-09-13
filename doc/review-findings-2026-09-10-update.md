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
