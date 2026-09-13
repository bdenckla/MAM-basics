# Updates to the 2026-09-11 current-state review of template projection

State: open, first entry 2026-09-13. Every entry here corrects or supplements
`doc/blind-dive-into-template-params.md`, which is left exactly as written.

Ben's decision, 2026-09-11: a finished dated document — a review, a remediation plan, a completed
plan, an execution record — is left as written, like a pushed commit. A correction to one goes in
a sibling file named `<stem>-update.md`, which is what this file is for that review. Nothing here
edits the document it corrects.

The review is Codex-written. It was committed as `doc/review-findings-2026-09-11.md` by `fa07fd8f`
on 2026-09-11 and renamed to `doc/blind-dive-into-template-params.md` by `1856b0a0` on 2026-09-12,
on Ben's instruction, with its content unchanged. MAM-basics #275 tracked the review, and its body
still links to the review under the old name.

## Three of the review's five findings have been fixed, finding 3 partly, and finding 1 is deferred

Recorded by a Claude session on 2026-09-13, at Ben's direction, from reading the code at
`1d2ddc3d`; nothing was re-run for this entry. The review's line `State: five open findings.` is
overtaken. The fixes, like the plan that records the deferrals,
`doc/PLAN-deferred-template-projection-decisions.md`, landed in `1b7b97ef`, a Codex-written commit
of 2026-09-12.

1. **Finding 1 is not fixed; the choices it asks for are deferred.** Both of the paths it names
   still take parameter 1, the pointed ketiv, of `מ:קו״כ-אם-2`. What the Holman verifier's path,
   `py/hkq_cmn/mam_plus_verse_data.py:_collect_text_fragments`, should take is decision 11 of the
   plan, which waits on the row-by-row investigation in MAM-basics #276. What the
   versification-and-cantillation page's path,
   `py/versification_and_cantillation/strands.py:_el_text`, should take is decision 7.
2. **Finding 2 has been fixed.** `py/hkq_cmn/qere_projection.py:word_atoms_from_qere_atoms` now
   gathers each run of adjacent projected text fragments and tokenizes the run as a whole, keeping
   the sources of every fragment that went into an atom, so a special-letter template no longer
   divides one atom into several. The plan's list of completed engineering repairs, item 1, records
   that the regenerated `holman/out/holam_he_qere_report.json` kept its hit set.
3. **Finding 3 has been partly fixed; the rest is deferred.** In
   `py/mb_diff_mpu/mpplus_docnote.py:_render_template`, the internal-link template
   `מ:קישור פנימי בהערה` now has an arm of its own, which requires exactly parameters 1 and 2 and
   renders parameter 1 as plain text, so the page-relative link the finding describes is no longer
   emitted. The external-link template `מ:קישור בהערה` still renders a link. Whether an internal
   target follows the documented strict contract or a permissive one is decision 10 of the plan.
4. **Finding 4 has been fixed.**
   `py/mb_cmn/plain_template_schema.py:validate_current_plain_template` checks every argument's
   identity as well as the argument count: against `_CURRENT_PLAIN_NAMED_ARGUMENT_IDENTITIES` where
   that table has an entry for the template, and against positional identities otherwise.
5. **Finding 5 has been fixed.** Each of the four paths the finding names now validates a
   template's shape before it selects parameters. `py/mpplus/mpplus_boring_tmpls.py:evaluate` calls
   `validate_current_handler_input_template`;
   `py/hkq_cmn/mam_plus_verse_data.py:_collect_text_fragments`,
   `py/versification_and_cantillation/strands.py:_el_text` and
   `py/decnreub/decnreub_for_one_cant.py:_do_one_wtel` call `validate_current_plus_template`.

So what remains of the review is decisions 7, 10 and 11 of
`doc/PLAN-deferred-template-projection-decisions.md`, which MAM-basics #277 tracks, with decision
11 also waiting on MAM-basics #276. The plan's other eight deferred decisions are not dispositions
of this review's findings.
