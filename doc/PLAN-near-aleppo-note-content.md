# PLAN: Bake reviewed near-Aleppo note content into the dataset

State: executed 2026-10-06

## Authorization and scope

Ben instructed Codex on 2026-10-06: “Please make a plan to bake the transformations in and
execute it across whatever set of sessions and/or sub-agents it needs.” Codex owns execution,
verification, integration and the normal push of `main`. This plan concerns the public runtime
and dataset only; it does not recreate the historical research plan retained in MAM-private.

Publish notes whose reviewed near-Aleppo clauses and explicit MAM context are already in the
book JSON. Consumers must not load the review ledger or repeat clause recasting to form an
edition. Preserve original source notes and review reasoning in their existing source and
review records. Keep brackets, typography, spacing and page layout as rendering choices.

Ben's requested-edit file remains user-owned. The companion status ledger records the later
outcome superseding A96's description of unchanged note bodies.

## Checkout, baseline and ownership

Source, development and integration checkout: `C:/Users/BenDe/GitRepos/MAM-basics`, a full clone
on `main`, clean at `a9c45ee1ef1c2a4843cb2442840c074fac629d85` before planning. Required baseline:
that commit, which must equal HEAD or be its ancestor. Run commands from this repository root
using `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe` and PowerShell 7.

Follow `AGENTS.md`, the canonical common instructions, and the `iterative-document-editing`
and `hebrew-prose` skills, including their MAM-basics, rendered-prose and verification references.
Recheck exact HEAD, branch and task-owned status before each staging operation. Stop on
unexpected HEAD movement or unowned edits and establish their provenance.

Use one writer in this checkout. Sub-agents may perform bounded design and compatibility
audits read-only; one implementation sub-agent may own all implementation writes while Codex
orchestrates read-only. Root Codex resumes writes only after that writer has stopped. Reusing
this verified full clone avoids concurrent editing and repeats no source discovery. The design
works in a linked worktree too; such a successor loads `codex-worktree-tasks` and uses its home
clone's interpreter, with final integration still owned by root Codex.

## Frozen implementation contract

The approved reviews determine the content; this migration makes no new editorial decisions.
Use explicit changed-note templates `נוסח עם הקשר מקרא על פי המסורה` and
`הערה-2 עם הקשר מקרא על פי המסורה`:

- Parameter `1` is the existing near-Aleppo Scripture target.
- Parameter `2` contains the already reviewed near-Aleppo clause; it is empty when the complete
  original note remains in MAM context.
- `מקרא על פי המסורה` preserves the original structured MAM target.
- `הערת מקרא על פי המסורה` contains the remaining original MAM clauses in their original order,
  or the complete original body when no clause is recast.
- Scroll-note parameter `3` and evidence flags retain their existing distinct roles.

The MAM target and MAM clauses are apparatus, not additional Scripture. Each parser and walker
dispatches explicitly on the recognized template and validates its complete expected shape.
The renderer formats the stored near and MAM roles; it performs no reviewed-clause lookup or
projection. Preserve the existing conversions of scroll notes and trivial ketiv/qere notes,
including explicit context when those notes are nested or merged.

## Implementation sequence

1. Refactor review provenance and source inventory to replay the pre-bake build in memory.
   Remove published-output dependency from review loading. Preserve review rows, source bodies,
   clause dispositions, reasons and evidence identities. Refresh only maintained input metadata
   through the repository command when necessary. Pending, stale, missing, duplicate or unused
   reviews must fail before any dataset writes.
2. Add a final note-content phase after text changes, MAM-target preservation and flags. Apply
   exactly the reviewed parts to each changed note, retaining target, flags, source order and
   scope. Emit the new template contract and consumer notice.
3. Adapt the shared renderer and its conversions to the stored content. Remove recipe injection
   from `near_aleppo/edition.py` and `main_html_pages.py`. Rendering the example edition must
   depend on the book JSON for its note content, with no review-ledger read.
4. Adapt closed template validation, figures, source-note censuses and documentation examples.
   Derive counts about original MAM clauses from original MAM input, rather than mistaking baked
   note content for original source evidence. Update the README, build guide, generated JSON
   reference, edition-index explanation and companion status ledger.
5. Add differential checks against the reviewed ledger and the tracked edition book pages at
   the required baseline. Protect the independent MAM-with-doc oracle already in the renderer.
   Regenerate and inspect every tracked change, then complete the suite and mega gates.

## Evidence and affected surfaces

- `py/near_aleppo/doc_note_review.py`: `input_hashes`, `inventory`, `load`, `recipes`, `check`;
  the current output hashes and unchanged-body assertions establish the dependency loop.
- `in/near-aleppo/doc-note-review.json`: `review.proposed_parts`, `near_clause`, `mam_clauses`;
  these are the reviewed content oracle. Original evidence and decisions must remain intact.
- `py/near_aleppo/main_build.py`: `build`, the final flags/rename/serialization sequence.
- `py/render_wt/render_wikitext_handlers.py`: `_reviewed_doc_parts`, `_mam_target_line`;
  `py/py_misc/scrdfftar_to_doc.py` and `trivial_qere_to_doc.py` own note merging.
- `py/near_aleppo/doc_figures.py`: `_walk`, `_rename_back`, `_testimony`;
  `doc_page.py` and `doc_policy_examples.py` contain original-body/key-set assertions.
- `py/near_aleppo/consumer_notice.py`, `out/near-aleppo/README.md`,
  `doc/near-aleppo-build.md`, and `doc/near-aleppo-doc-edit-status.md` explain the contract.
- `py/main_0_mega.py`: near-Aleppo census, build and HTML steps; review verification must precede
  dataset writes rather than depend on the later HTML step.

Product reach: `out/near-aleppo/` is distributed data, `gh-pages/` is published, and the build
and renderer are mega generators, as `py/product_scopes.py` declares. Normal commits are
reversible; pushing `main` changes the remote and the later Pages deployment. Updating review
metadata is a separate evidence risk: prove all existing review rows and decisions unchanged.

## Verification and expected changes

Expected changed outputs: the near-Aleppo book JSON note contracts and consumer notices,
the review ledger's maintained input metadata if required, and relevant documentation pages.
Expected unchanged: all Scripture targets/readings, C and D cells, preserved MAM targets,
flag values, original review evidence and decisions, sealed pointing inputs, and every example
edition book and long-note HTML page. Edition-index prose may change. Unrelated products must
remain unchanged. Every unexpected diff is a failure until explained.

Format every changed Python file with this clone's Black. Run the differential note checks,
the complete near-Aleppo check and fresh review check, the full suite and the mega from the root:

```powershell
./.venv/Scripts/python.exe py/main_near_aleppo.py --check
```

```powershell
./.venv/Scripts/python.exe py/main_near_aleppo.py --check-note-review
```

```powershell
./.venv/Scripts/python.exe py/main_test.py -q
```

```powershell
./.venv/Scripts/python.exe py/main_0_mega.py
```

Run `git diff --check` for each commit. Use only the repository test entry point. A generated
output differential and an independent source/review comparison are the test shapes; do not
add selected-case tests that merely mirror the implementation.

Commit coherent stages locally on `main`. Before pushing, fetch `origin`, merge `origin/main`
if it moved, repeat checks owed by the resulting changes, and push normally. Do not rewrite or
discard work. After the final verified change, set this plan to `executed 2026-10-06` in the
same commit as its completed execution record. If another session is needed, leave an exact
standalone handoff naming agent/date, Ben's quoted authorization, required commit, checkout,
remaining scope and root Codex's integration ownership.

## Execution record, 2026-10-06

Root Codex executed the plan in the declared full clone after committing the plan as
`b5abc283f4e0b09e1c1ea6d09f119cb38cbdb669`. Read-only design and compatibility audits
ran alongside one implementation writer. Root resumed write ownership after that writer
finished, inspected the source and generated diffs, and completed the verification gates.

The build now validates reviews against an in-memory pre-bake source replay before writing
the dataset. Its final note-content phase stores the reviewed clauses under the frozen
contract above. The edition renderer reads those roles directly from the book JSON and has
no review-ledger or presentation-recipe dependency. Shared scroll-note and trivial-qere
conversions preserve the explicit MAM context. The README, build guide, JSON reference,
edition index, decision record and companion status ledger describe the resulting contract.

All 1,548 review rows, including source evidence, dispositions and reasoning, are identical
to baseline `a9c45ee1ef1c2a4843cb2442840c074fac629d85`. The dataset contains recast clauses
at 1,047 notes and complete original bodies under MAM context at 501 notes. Maintained ledger
metadata removes the 24 output-file hashes and updates only the hash of the clarified
pre-bake MAM-target module. The original source notes and sealed pointing inputs are unchanged.

Verification completed from the repository root with its own environment:

- Black passed on all 19 changed Python files; `git diff HEAD --check` passed.
- The complete near-Aleppo check passed: five census baselines, all 24 book files, fresh
  review validation, 81 generated files and two font copies. The shared renderer matched
  the 62 independently tracked MAM-with-doc files.
- The full suite passed: 1,054 tests and 60 subtests, with five skips and one warning about
  permission to write pytest's cache.
- The full mega passed all 60 steps. Its generated diffs were confined to the expected
  near-Aleppo outputs; unrelated products remained unchanged.
- A separate three-check migration comparison against the execution baseline passed.
  All 24 books preserve their content outside changed note bodies, template names and
  consumer notices. All prior edition book and long-note HTML pages match byte for byte.
  The only changed generated HTML explains the contract in `reading-json.html`,
  `choices.html` and `edition/index.html`.

After the mega, root corrected one grammar error in the pre-bake module's docstring and
split the README's commands into separate fences. Root refreshed the maintained ledger
hash, then ran the complete near-Aleppo check and full suite on that final state. These
prose-only corrections did not expire the mega result.

Origin advanced during execution to `149d0fe8c2f5300e1d3d24e329a4ac21f9064a3f`.
Root inspected its complete diff: it only appends a separate review record in
`doc/review-findings-2026-10-04-update.md`, without a source or product change. That
non-colliding documentation addition does not expire the verification results.
