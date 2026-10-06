# Near-Aleppo documentation edit status

State: live

Codex maintains this ledger for [Ben's requested edits](near-aleppo-requested-doc-edits.md).

## A96 — Stored note bodies and HTML presentation

**Status:** implemented by Codex, 2026-10-06.

**Assessment:** The quoted sentence remains true for the JSON dataset, but its scope was unclear.
The HTML edition's reviewed note presentations recast source clauses beside near-Aleppo's form;
the original JSON note bodies remain about MAM's target.

**Authorized scope:** Clarify the passage beginning “Two are MAM's note templates” in
`py/near_aleppo/doc_page.py`, regenerate `gh-pages/near-aleppo/reading-json.html`, and record
A96 here. Ben's request file is unchanged. The JSON dataset and example edition HTML are
expected to remain unchanged. The execution baseline is MAM-basics `617ceb42`.

**Change:** The JSON reference now explicitly scopes unchanged note bodies to the JSON dataset.
A following paragraph explains how the HTML edition recasts reviewed clauses as agreements
with near-Aleppo, places the remaining clauses after MAM's labelled form, and displays the
complete original note when a recast would require uncertain interpretation.

**Evidence:** `py/near_aleppo/phase6_mam_targets.py`, `MamTargets.add_to_e_cell`, rejects changes
to note parameters other than the target. `py/render_wt/render_wikitext_handlers.py`,
`_reviewed_doc_parts`, renders reviewed clauses beside near-Aleppo's form and the remaining
clauses with MAM's labelled form. Genesis 1:1 in `out/near-aleppo/plus/A1-Genesis.json` and
`gh-pages/near-aleppo/edition/A1-Genesis.html` demonstrates the stored and displayed versions.

**Verification:** Run from the MAM-basics repository root:

- `./.venv/Scripts/python.exe -m black py/near_aleppo/doc_page.py` passed.
- `./.venv/Scripts/python.exe py/main_near_aleppo.py --html` passed, including the shared
  renderer's comparison with the pinned tracked MAM-with-doc files. Only `reading-json.html`
  changed among the generated files; the dataset and example edition HTML remained unchanged.
- `./.venv/Scripts/python.exe py/main_near_aleppo.py --check-note-review` passed the fresh
  source enumeration and clause reviews.
- `git diff --check` passed.

The mega and full suite were skipped because the change clarifies rendered prose without
changing data or rendering logic.

## Annotation 1 — Planned template for marks without letters or space

**Status:** implemented by Codex, 2026-10-06; approved by Ben on the same date.

**Authorized scope:** Ben asked Codex to implement its recommendation to retain the original
decision and one concrete explanation under pending work, while removing the planned template
`ניקוד בלי אות ובלי רווח` from instructions for consuming the current dataset. Describe it as
a planned template for an outstanding case. The execution baseline is MAM-basics `a287e556`;
the source, development and integration checkout is `C:/Users/BenDe/GitRepos/MAM-basics`.

**Expected changes:** Update the shared consumer notice and generated JSON headers, the JSON
reference, the decision record, and the pending-work section. Refresh the presentation ledger's
input hashes through the maintained command. Scripture, note bodies, reviewed note dispositions,
sealed pointing inputs and example edition book pages must remain unchanged. Codex owns
verification, the commit and the normal push of `main`.

**Change:** The JSON reference and all 24 book notices now describe the three templates the
dataset uses. The original decision describes the reserved name as a planned template. The
pending-work section explains the intended use at 2 Samuel 18:20: MAM's note records tsere and
merkha without letters or space at the join inside a maqaf compound, while the current edition
still displays the full qere. The build and renderer still await that implementation.

**Verification:** Black passed on the four changed Python files. The dataset rebuild and
HTML regeneration passed, including the shared renderer's comparison against the 62 pinned
MAM-with-doc files. A comparison against `a287e556` verified that all 24 dataset changes are
confined to consumer notices; all 1,548 presentation-ledger entries are unchanged; and only
the ledger's 24 near-Aleppo input hashes changed. The only changed generated pages are
`reading-json.html`, `choices.html` and `coverage-and-status.html`. The planned template has
no mention in the JSON reference or book notices and one mention each in the decision record
and pending-work section. `git diff --check` passed.

The full suite, `./.venv/Scripts/python.exe py/main_test.py -q`, passed: 1,051 tests and
60 subtests passed, with 5 skips and one warning about permission to write pytest's cache.

The mega is skipped because the change is confined to near-Aleppo documentation and consumer
notice strings. The affected generator outputs were regenerated and inspected; build and
rendering algorithms did not change.

## A96 — Superseded by stored reviewed note content, 2026-10-06

**Status:** the earlier A96 implementation is superseded; baked note content is implemented
and verified.

**Authorization:** Ben instructed Codex on 2026-10-06: “Please make a plan to bake the
transformations in and execute it across whatever set of sessions and/or sub-agents it needs.”
The undertaking is recorded in `doc/PLAN-near-aleppo-note-content.md`. Ben's request file
remains unchanged.

**Change:** All 1,548 changed notes now contain the reviewed content in the book JSON.
Parameter 1 remains the near-Aleppo Scripture target. Parameter 2 contains the reviewed
near-Aleppo clause at 1,047 notes; it is an empty array at the 501 notes whose complete
original body remains in MAM context. `מקרא על פי המסורה` preserves the original
structured MAM target. `הערת מקרא על פי המסורה` contains the remaining original
clauses, or the complete original body. Scroll-note parameter 3 and flags retain their roles.
Codex's schema implementation uses `נוסח עם הקשר מקרא על פי המסורה` and
`הערה-2 עם הקשר מקרא על פי המסורה` so that consumers recognize the changed contract.

**Evidence:** `py/near_aleppo/note_content.py`, `NoteContent.apply`, matches each
review's complete source evidence and stores its approved parts. `doc_note_review.py`,
`inventory`, replays the pre-bake build from source inputs, keeping the historical nested
template names solely for the review's evidence identities. Every review is complete and
matches a fresh inventory before dataset writes. The renderer's `_stored_doc_parts` formats
the two stored roles; `edition.render_edition` reads no presentation recipe or review ledger.

**Verification:** Black passed on changed Python files. Dataset and HTML regeneration passed,
and the complete near-Aleppo check passed. All 1,548 ledger rows, including source evidence,
decisions and reasoning, compare exactly with baseline `a9c45ee1`; maintained metadata
removes the 24 published-output hashes and updates only the hash of the clarified pre-bake
MAM-target module. Six targeted differential and source-lint checks passed, including all
book-content invariants, all prior edition book and long-note pages, the 62-file independent
MAM-with-doc oracle, and removal of renderer review dependencies. The only generated HTML
changes explain the new contract in `reading-json.html`, `choices.html` and
`edition/index.html`. Scripture, C and D cells, flags, original MAM targets, sealed pointings and
edition book/long-note HTML remain unchanged. Root Codex independently passed the complete
near-Aleppo check, a three-check migration comparison against the execution baseline, and
the full mega's 60 steps. The full suite passed: 1,054 tests and 60 subtests, with five skips
and one warning about permission to write pytest's cache. Unrelated products remained
unchanged. `doc/PLAN-near-aleppo-note-content.md` is marked executed and records the completed
gates and the documentation-only origin update encountered during integration.

## A97–A101 — Retained-feature list and example, 2026-10-06

**Status:** implemented by Codex, 2026-10-06; authorized by Ben's instruction to process the
request file through A101.
A96 remains implemented by the stored-note-content work recorded above.

**Authorized scope:** Remove A97's tsinnorit/tsinnor list item, A98's assertion that the
holam-haser-for-vav code point records the manuscript's dot placement, A99's deḥi list item,
A100's tipeḥa/tarḥa list item, and A101's corresponding Psalms 40:13 example. Ben's request
file remains verbatim. No new manuscript judgment is needed for these removals.

**Checkout and baseline:** Source, development and integration checkout is
`C:/Users/BenDe/GitRepos2/MAM-basics`, a full clone on `main` at
`e47c7440abb4f28e713cc0a7bf9a38d0c031e5ae` before editing. The only existing modification
is Ben's updated request file. Codex owns the edits, verification, commit and normal push.
Commands run from this checkout's root with its own `.venv/Scripts/python.exe`.

**Expected changes and verification:** Change `py/near_aleppo/doc_registers.py`, remove the
unused example from `py/near_aleppo/doc_policy_examples.py`, and regenerate
`gh-pages/near-aleppo/editorial-policies.html`. Record each request's disposition here and
include Ben's verbatim request-file update in the commit. All datasets, source evidence,
review ledgers, edition book pages and other generated files must remain unchanged.
Format both changed Python files with Black, run `py/main_near_aleppo.py --html`, inspect
the generated diff and removed passages, and run `git diff --check`. The mega and full suite
are skipped because the edits remove documentation content and its unused example helper;
the actual HTML generator checks the affected surface and shared-renderer compatibility.

**Completed dispositions:**

| Request | Status | Change |
| --- | --- | --- |
| A97 | implemented | Removed the tsinnorit/tsinnor list item. |
| A98 | implemented | Removed the claim about the manuscript's dot placement; retained the holam-haser-for-vav item and its figures. |
| A99 | implemented | Removed the deḥi list item. |
| A100 | implemented | Removed the tipeḥa/tarḥa list item. |
| A101 | implemented | Removed the corresponding Psalms 40:13 example and its unused helper and import. |

**Verification:** Black passed on both changed Python files. HTML regeneration passed,
including the shared renderer's comparison with the 62 pinned MAM-with-doc files.
`editorial-policies.html` is the only changed generated file; its diff contains exactly the
requested removals and the joining punctuation in A98's retained item. All datasets, source
evidence, review ledgers, edition book pages and other generated files are unchanged. A search
of the affected source and page found none of the removed passages or the unused helper.
`git diff --check` passed. The mega and full suite were skipped for the documentation-only
scope explained above.

## A102 — Deferred beyond this task's cutoff

**Status:** deferred. Ben added A102 while A97–A101 were being implemented; the current
instruction authorizes processing through A101. A102's requested removal of “The sparseness
of the ketiv/qere” remains for a later instruction. The request-file update is preserved
verbatim, with no agent-written annotations.
