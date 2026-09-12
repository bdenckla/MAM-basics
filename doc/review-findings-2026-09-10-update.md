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
