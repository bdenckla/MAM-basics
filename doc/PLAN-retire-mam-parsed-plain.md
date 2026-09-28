# Deeply retire MAM-parsed plain

State: live; implementation in progress. Ben authorized this plan's persistence
on 2026-09-27 and bounded implementation checkpoints through 2026-09-28. Neither
that authorization nor the checkpoint commits authorize integration, push,
publication, MAM-private edits, or worktree archival.

## Summary

Retire `MAM-parsed/plain/` as a persisted and distributed product, retire its
published documentation and template survey, and remove tests and claim machinery
whose only purpose is to describe or verify those retired artifacts. Keep the
valuable structural validations that operate on the same parser-stage data, but run
them directly on that transient data before it is converted to `MAM-parsed/plus/`
or written. Keep `MAM-parsed/plus/` and its name unchanged.

The first implementation phase writes only MAM-basics. It finishes and commits the
MAM-basics work on `codex-worktree-1a58`, then stops before integration or push.
MAM-private derives its near-Aleppo consumer notice from the exact MAM-parsed-plus
notice and pins that notice's SHA-256, so a separate MAM-private compatibility phase
must be complete and verified before the MAM-basics branch is integrated. The two
repositories are then integrated and pushed as one coordinated close-out.

Ben made the retirement decisions on 2026-09-27. The phrase "deeply retire" means
retiring not only the persisted/distributed plain product, but also the plain
survey, plain documentation, and their self-referential tests. Ben expressly kept
the option, and preference, to run valuable raw-structure validations on the
transient data corresponding to today's persisted plain files.

## Approval snapshot and revision ledger

| Requirement or decision | State | Disposition |
| --- | --- | --- |
| The target is MAM-parsed plain, not MAM-parsed plus. | active | Remove the plain product and its product-only support. |
| Keep `MAM-parsed/plus/` and the word `plus` in its public name and path. | active | Do not rename the surviving product. |
| Remove the persisted/distributed plain JSON. | partially implemented | Commit `4d4385c3cf9ec7ad385e87936739f8687b3cfc7e` stopped every generator from recreating it; delete the tracked `MAM-parsed/plain/` tree next. |
| Remove the plain survey and its generated graphs and data. | active | Delete its outputs and product-facing code; preserve only validations justified independently of the survey. |
| Remove plain documentation and self-referential tests. | active | Delete plain pages, authoring sources, claims, examples, and tests whose subject or oracle is the retired product. |
| Keep valuable raw-structure validation. | implemented | Commits `24b7f23ab80430a1cb413f8e4759d97fb5db3e2d` and `146f6145ad85acf9342b421174e35074480c4301` validate the transient parser-stage structure and raw-to-plus relationship before writes; `4d4385c3cf9ec7ad385e87936739f8687b3cfc7e` moved raw grammar-lock ownership out of the plain survey. |
| Make the plus survey self-contained. | implemented | Commit `146f6145ad85acf9342b421174e35074480c4301` embeds the full plus `mpasuq` result and removes the plus survey's dependency on `plain_result["mpasuq"]`. |
| Make the plus consumer notice self-contained. | active | Remove its comparison with the retired plain product while preserving the substantive plus warnings. |
| Limit the first writing phase to MAM-basics. | active | Audit sibling repositories read-only; make MAM-private changes in a separate task. |
| Stop MAM-basics before integration and push until MAM-private is compatible. | active | The MAM-basics implementation commit is a handoff input, not yet a published result. |
| Ignore unsupported external consumers for this retirement decision. | active | Do not retain plain merely as a compatibility product; Git history remains the reconstruction path. |
| hbofonts and phonetic-hbo need no compatibility edit unless a fresh audit finds a real plain dependency. | active | Treat a newly found dependency as a finding and stop rather than expanding scope silently. |

There are no unresolved policy choices in this snapshot. An implementation finding
that would weaken a retained validation, change plus semantics beyond the consumer
notice, or require another repository's product policy is a new decision and stops
execution for Ben.

## Implementation progress through 2026-09-28

1. The first checkpoint is complete in commit
   `24b7f23ab80430a1cb413f8e4759d97fb5db3e2d`. It introduced the parser-stage
   validation boundary in `py/py_misc/mam_parser_stage.py` and
   `py/verify_mp/parser_stage.py` while deliberately retaining plain writes.
2. The second checkpoint is complete in commit
   `146f6145ad85acf9342b421174e35074480c4301`. It completed the planned structural,
   closed-template, recursive-grammar, normal-form, expanded-stack, special
   ketiv/qere, paragraph-argument, D-column, and raw-to-plus validations. It also
   made the plus survey's `mpasuq` data self-contained. Do not rediscover or
   reimplement those completed checks unless a concrete regression is found.
3. The second checkpoint passed Black, 14 targeted tests, the full suite with
   1,014 passed and five skipped, the 52-step mega, all 79 non-pending
   MAM-parsed verifiers, and all-books candidate generation. The candidate's 24
   plain and 24 plus JSON files matched the tracked products byte-for-byte; plain
   writing remained enabled by design. `git diff --check` passed and the worktree
   was clean after the commit.
4. The third checkpoint is complete in commit
   `4d4385c3cf9ec7ad385e87936739f8687b3cfc7e`. It moved the unchanged raw
   expanded-stack lock to the parser-stage validator, made the survey lock updater
   plus-only, stopped production and candidate generation from writing or returning
   plain paths, and deleted the callerless plain wrapper. The affected command
   wording, callers, and mega-coverage declarations now describe plus-only output.
5. The third checkpoint passed Black, 51 targeted tests, the full suite with 1,014
   passed and five skipped, and the full 52-step mega. Its candidate contained
   exactly 24 plus JSON files, no plain directory, and bytes identical to the 24
   tracked plus files. The raw lock was a 100% rename with unchanged bytes. The
   plus-only lock updater removed four stale direct-nesting edges left behind when
   `73c6b1137777ad1a522949fcea290f8ac1f87a7b` wrapped those special-letter
   templates; no other generated artifact changed. `git diff --check` passed and
   the worktree was clean after the commit.
6. The next bounded checkpoint completes the remaining MAM-basics retirement across
   Phases 3 through 6 and commits it locally. The tracked plain trees are still live
   inputs to current authoring, survey, verifier, and test code, so deleting a tree
   without retiring those consumers would not be a coherent checkpoint. Complete
   those coupled removals together, regenerate and verify MAM-basics, and stop at
   the separate MAM-private compatibility gate. Do not edit MAM-private, integrate,
   push, publish Pages, or archive the worktree in that checkpoint.

## Inputs and dated baseline

The intended MAM-basics development checkout is
`C:/Users/BenDe/.codex/worktrees/1a58/MAM-basics`. The required source commit for
the next checkpoint is `4d4385c3cf9ec7ad385e87936739f8687b3cfc7e`. The original
implementation baseline, `85cb7acd8df98089614de8e3e30bb67bc5a2c36a`, must remain
an ancestor. The primary integration checkout is
`C:/Users/BenDe/GitRepos/MAM-basics`. The shared interpreter is
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`.

At the original implementation baseline, immediately before the first checkpoint,
and after the third checkpoint, the dated removal inventory was:

1. 25 files under `MAM-parsed/plain/`: 24 JSON books and `provenance.md`.
2. 14 files under `gh-pages/MAM-parsed/plain/`: eight HTML pages and six SVGs.
3. Seven files under `out/tmpl-survey-plain/`: one JSON survey and six DOT files.

Remeasure those figures before implementation; they are a drift detector, not a
substitute for discovering all current references.

```powershell
@(rg --files MAM-parsed/plain).Count
```

```powershell
@(rg --files gh-pages/MAM-parsed/plain).Count
```

```powershell
@(rg --files out/tmpl-survey-plain).Count
```

The implementation is based on these current anchors rather than on line numbers:

- `py/subcommands/parse_ws_products.py`, `def generate`, validates a transient
  plain-shaped value, converts and validates it against plus, and currently writes
  both values.
- `py/py_misc/mam_parsed_plain.py`, `def add_header`, constructs the shared
  top-level wrapper and currently adds the public plain consumer notice.
- `py/py_misc/mam_parsed_plus.py`, `def add_plus_stuff`, consumes the transient
  plain-shaped value.
- `py/main_tmpl_survey.py`, `def almost_main`, currently produces both surveys and
  owns both expanded-stack lock update paths. The plus survey is already
  self-contained; the raw lock still belongs to the old plain-survey path.
- `py/tmpl_survey/survey_plain.py`, `def survey`, contains a mixture of product
  survey reporting and reusable observations about the parser-stage structure.
- `py/verify_mp/verifiers_plain.py` contains both raw-structure checks worth
  preserving and documentation/product checks to retire.
- `py/verify_mp/verifiers_both.py` contains claims that currently join the plain and
  plus surveys and must become plus-only or retire.
- `py/mb_cmn/public_data_consumer_notice.py`, `def mam_parsed_notice`, currently
  dispatches between plain and plus and makes the plus notice comparative.
- `py/main_authored.py`, `cmd_gen_mam_parsed_docs`, currently loads both corpora and
  surveys and writes both documentation families.
- `py/pipeline_graph/pipeline_graph_spec.py`, the `ds_parsed_plain` and `mpu_plain`
  records, declares the public plain product and its survey edge.
- `doc/mp-claims.md` is generated evidence about the current authoring claims, not
  an independently edited source of truth.

The earlier four-repository audit found no internal plain consumer in MAM-private,
hbofonts, or phonetic-hbo. MAM-private consumes `MAM-parsed/plus/`; the compatibility
issue is its deliberate notice pin in
`near-aleppo/py/consumer_notice.py`, searchable by `_MAM_NOTICE_SHA256`. Recheck all
four repositories before deleting, because that audit is dated evidence rather
than a permanent invariant.

## Execution setup and ownership

1. Read the current user instructions and the assigned checkout's `AGENTS.md`.
2. Load `iterative-document-editing` and `codex-worktree-tasks`. Load
   `hebrew-prose` before editing consumer notices or documentation that discusses
   Hebrew accentuation or cantillation. Load `mam-repository-topology` before the
   sibling-repository audit and coordinated integration phase.
3. Verify the exact worktree before editing:

   ```powershell
   git -c "safe.directory=C:/Users/BenDe/.codex/worktrees/1a58/MAM-basics" -C "C:/Users/BenDe/.codex/worktrees/1a58/MAM-basics" rev-parse --show-toplevel
   ```

   ```powershell
   git -c "safe.directory=C:/Users/BenDe/.codex/worktrees/1a58/MAM-basics" -C "C:/Users/BenDe/.codex/worktrees/1a58/MAM-basics" rev-parse HEAD
   ```

   ```powershell
   git -c "safe.directory=C:/Users/BenDe/.codex/worktrees/1a58/MAM-basics" -C "C:/Users/BenDe/.codex/worktrees/1a58/MAM-basics" branch --show-current
   ```

   ```powershell
   git -c "safe.directory=C:/Users/BenDe/.codex/worktrees/1a58/MAM-basics" -C "C:/Users/BenDe/.codex/worktrees/1a58/MAM-basics" status --porcelain=v1 -uall
   ```

4. Require the recorded `HEAD` to equal the required baseline or contain it as an
   ancestor. Require a clean checkout. Stop on unexpected `HEAD` movement,
   unowned changes, missing inputs, or a second writer.
5. Keep one writer in the MAM-basics worktree. Read-only sub-agents may inventory,
   review, or independently check the final diff. A sub-agent must not edit,
   stage, or commit in the shared checkout.
6. Use the primary clone's interpreter by absolute path, but run every script,
   formatter, test, generator, Git operation, and commit from the verified
   worktree.
7. Record the remeasured inventory and any drift in this plan's execution findings
   when the plan is completed. Do not create a second plan or numbered update.

## Phase 1: establish a complete current-use inventory

Status through `4d4385c3cf9ec7ad385e87936739f8687b3cfc7e`: complete for the
current checkpoint boundary. The searches and read-only sibling audit found no
live plain consumer outside MAM-basics. Repeat only focused drift checks for paths
affected by a new checkpoint; do not redo the full discovery without evidence of
drift.

Search all tracked current code, tests, product declarations, documentation, and
generated artifacts for the retired product and survey. Search for at least:

- `MAM-parsed/plain`, `MAM-parsed-plain`, and public plain URLs;
- `tmpl-survey-plain`, `survey_plain`, `load_plain`, and `corpus_plain`;
- `mam_parsed_notice("plain")` and `MAM_PARSED_PLAIN_DOCUMENTATION`;
- `mp.plain.`, `mp.both.`, `plain-only`, `diff-from-plain`, and prose that defines
  plus only by comparison with plain;
- `expanded_stack_grammar_plain.lock.json`, `plain_raw_sc`, and
  `plain_mpasuq`;
- `plain/ and plus/`, `production plain/plus`, and help text or launch settings
  that promise both outputs.

Classify every hit before editing:

1. Current product, generator, test, documentation, or configuration: remove or
   rewrite it.
2. Valuable validation of the transient parser representation: move or retain it
   in the parser-stage validation path.
3. Finished dated receipt or historical artifact: preserve it under the historical
   rules below.
4. Another repository's active dependency: stop and report it unless it is the
   already-approved MAM-private compatibility work.

Run a fresh read-only search in MAM-private, hbofonts, and phonetic-hbo. The expected
finding is that all live consumers use plus or plus-derived data. Do not edit those
repositories in Phase 1.

## Phase 2: make the parser-stage value transient and validated

Status through `4d4385c3cf9ec7ad385e87936739f8687b3cfc7e`: complete. The
in-memory parser-stage boundary, raw-to-plus validation, raw-lock ownership,
plus-only product writes and return values, and deletion of the callerless public
plain wrapper are implemented. The semantic checks listed below are completed
invariants, not work to recreate.

Refactor `parse_ws_products.generate` so the plain-shaped structure exists only in
memory between Wikisource parsing and `add_plus_stuff`. The production and candidate
generators write only `plus/<book>.json`. Update command descriptions, return values,
coverage declarations, and callers so no interface promises a plain output.

The transient value may retain an internal implementation name where renaming would
add risk without clarity, but current public/product terminology must not imply that
plain remains a supported artifact. Remove the public plain consumer notice from the
transient header. Do not add a new persisted debug, cache, snapshot, or survey file
as a replacement.

Create a parser-stage validation boundary that receives the transient value directly.
Run it for every affected book group before `add_plus_stuff` and before any product
write. Run the raw-to-plus relationship checks while both values are still in
memory, also before writing. A validation failure must abort the parse; missing data
must fail rather than skip.

Preserve the following semantic checks, refactoring survey or verifier helpers into
purpose-named validation modules where necessary:

- top-level, header, book39, chapter, pseudo-verse, verse-tuple, and column
  structure, including chapter boundary records;
- the C-, D-, and E-column structural rules, with the D-column labels,
  coordinates, aliyah records, and their raw-to-plus correspondence checked
  directly;
- the closed recognized-template and custom-tag roster and the expected argument
  shape of each recognized template;
- recursive node grammar and allowed node kinds, including the distinction among
  Scripture-bearing, documentation, apparatus, formatting, and alternative
  children;
- the special ketiv/qere template's semantic shape;
- the paragraph-template argument constraint;
- nesting normal form and the expanded stack grammar that protect the parser
  representation.

The former plain expanded-stack lock represents a valuable raw-stage invariant,
not a reason to keep the survey. Commit `4d4385c3cf9ec7ad385e87936739f8687b3cfc7e`
moved it unchanged to
`py/verify_mp/expanded_stack_grammar_parser_stage.lock.json` and made
`py/verify_mp/parser_stage.py` own its read and comparison. The survey command now
updates only the plus lock, which remains with the plus survey. Never update either
lock merely to make a failure green.

Commit `4d4385c3cf9ec7ad385e87936739f8687b3cfc7e` also changed
`parse_ws_products.generate` and its callers to write and return only plus product
paths, updated the affected wording and coverage, and deleted
`py/py_misc/mam_parsed_plain.py` after verifying that it had no remaining caller.
The all-books candidate contained exactly 24 plus JSON files and no plain directory,
and every candidate plus file was byte-for-byte equal to the tracked plus file.

Delete checks that only count, rank, graph, document, exemplify, or prove the
existence of the retired plain product. Do not preserve the entire plain survey as
an internal survey in disguise. If a retained validation currently depends on a
survey accumulator, extract the smallest validation-oriented collector and give it
a non-survey interface.

Do not add example-based unit tests for individual templates or strings. The real
parse and generated plus artifact are the differential test; source-tree lints and
closed-roster checks may remain mechanical tests.

## Phase 3: retire the plain product and survey

Status through `4d4385c3cf9ec7ad385e87936739f8687b3cfc7e`: the plus survey is
self-contained, including full `mpasuq` data, and production and candidate
generation no longer writes plain JSON. All tracked plain product, documentation,
and survey trees and their remaining product-facing consumers still remain. The
next checkpoint deletes those trees and retires their coupled consumers across
Phases 3 through 5 before running Phase 6 verification.

Delete these generated trees completely:

- `MAM-parsed/plain/`;
- `gh-pages/MAM-parsed/plain/`;
- `out/tmpl-survey-plain/`.

Delete product-only implementation after its retained validation logic has moved,
including `py/tmpl_survey/survey_plain.py` and the plain product header helper if it
no longer has a legitimate transient role. Remove the plain survey's rendering,
normalization note, graph configuration, output paths, CLI wording, and lock-update
behavior from `py/main_tmpl_survey.py` and its helpers.

The surviving plus survey is already self-contained: it does not accept
`plain_mpasuq`, emit `"same as plain"`, load a plain artifact, or require a plain
survey to explain its result. Preserve that invariant, the plus survey outputs,
and plus-only normal-form validation. Move genuinely generic stack helpers out of
`survey_plain.py` before deleting that module.

Update `py/main_0_mega.py` and `py/tests/test_mega_coverage.py` so the mega still
runs the plus survey and the parse step, while nothing expects the deleted outputs.
An ordinary parse, authored-documentation run, survey run, test run, or mega run
must be unable to recreate any retired plain path.

Update `py/product_scopes.py` and its test to describe the surviving
`MAM-parsed/plus/` distribution accurately. `MAM-parsed/` remains a distributed-data
tree; do not rename the plus product or falsely remove the whole tree from product
scope.

## Phase 4: make plus documentation and notices independent

Status through `4d4385c3cf9ec7ad385e87936739f8687b3cfc7e`: not yet implemented.
The next bounded checkpoint owns this work together with the coupled Phase 3 and
Phase 5 removals.

Rewrite the canonical MAM-parsed-plus consumer notice so it is true and complete
without referring readers to the retired plain product. Prefer a plus-specific
function or otherwise close dispatch explicitly on the one surviving MAM-parsed
variant; do not retain a dead `plain` branch.

In particular, replace the comparative rule that says plus omits plain's
pseudo-verses with a direct statement of which source boundary records are absent
from plus and what consumers must still handle. Preserve every other substantive
consumer warning unless an independent finding proves it stale. Remove the plain
documentation URL constant and plain target checks.

Regenerate all 24 `MAM-parsed/plus/*.json` files. Their
`header.consumer_notice` objects are expected to change. Outside that notice, the
plus JSON payloads must remain semantically and byte-for-byte unchanged; any other
plus change is a finding that must be explained and, if it changes policy or data,
approved before proceeding.

Remove the plain documentation authoring family and its snippets. Expected
product-specific candidates include `py/author_misc/mpplain*.py`,
`py/author_misc/mp_cmn_plain_only.py`, plain JSON snippets, plus-versus-plain pages,
and plain-only-template pages. Inspect shared authoring modules before deleting
them: keep and simplify code that still authors plus documentation.

Make the plus documentation self-contained. Remove navigation, examples, claims,
and explanatory prose whose subject is plain or whose only function is comparing
plus with plain. Keep descriptions of plus structure and consumer responsibilities
that remain true in their own right.

Update current repository documentation and generated pages, including as
applicable:

- `README.md`, `MAM-parsed/README.md`, and `DATA-LICENSES.md`;
- `doc/mam-normal-mark-order.md` and other current guidance that enumerates public
  data trees;
- `doc/process-documentation/pipeline.dot` and
  `py/pipeline_graph/pipeline_graph_spec.py`, followed by graph regeneration;
- `doc/mp-claims.md`, by changing its authoring inputs and regenerating it rather
  than hand-editing the generated table;
- current comments, help text, provenance, support-file copies, launch settings,
  and repository-standard lints.

`doc/PLAN-silluq-before-gaya-template.md` is a live plan and must remain true in
place if it still mentions plain. `doc/blind-dive-into-template-params.md` is a
finished receipt; record any necessary retirement disposition in its existing
`doc/blind-dive-into-template-params-update.md`, not in the base. Apply the same
receipt rule to every other finished dated plan, review, or report.

Preserve historical evidence, including `MAM-parsed/historical/`, the
`in/mam_products_phase6*.json` records, completed dated reviews and plans, historical
timing or validation reports, and old change logs. A historical mention of plain is
not a current dependency. Do not rewrite history merely to make a repository-wide
text search empty.

## Phase 5: retire self-referential claims and tests

Status through `4d4385c3cf9ec7ad385e87936739f8687b3cfc7e`: not yet implemented.
The next bounded checkpoint must retire these consumers in the same coherent commit
that deletes their plain product and survey inputs.

Remove `mp.plain.*` documentation claims and their payload examples. Rewrite or
remove `mp.both.*` claims according to their actual surviving subject:

- a fact about plus becomes an explicitly plus claim and plus verifier;
- a raw-parser invariant moves to the parser-stage validator and is no longer
  justified by a public documentation claim;
- a comparison, example, or census meaningful only because both artifacts existed
  retires.

Simplify `py/verify_mp/corpus.py`, `survey_artifact.py`, `driver.py`,
`verifiers_plain.py`, `verifiers_both.py`, `verifiers_plus.py`, and
`payload_examples.py` as their live responsibilities require. Delete a module when
no live responsibility remains. Do not leave a `PlainCorpus`, `survey_plain`,
plain artifact loader, or dead verifier registry behind.

Update or remove tests whose oracle is the retired JSON, survey, documentation, or
examples. This includes the plain branches of
`test_public_data_consumer_notices.py`, the plain survey normal-form and invariant
tests, plain documentation payload checks, and retired-path lists in
`test_no_machine_paths_in_artifacts.py`.

Retain tests only when they are differential against an independent oracle or are
mechanical lints over live source. The main parse must itself exercise every
retained raw validator. Add no selected-case tests merely to replace deleted
self-referential coverage.

## Phase 6: regenerate and verify MAM-basics

The last completed full verification checkpoint is
`4d4385c3cf9ec7ad385e87936739f8687b3cfc7e`, with the results recorded in
“Implementation progress through 2026-09-28.” A later code checkpoint expires that
result only for surfaces the later checkpoint can affect and must run the cheap,
targeted, suite, generator, and final integration gates required by the current
repository instructions.

Run Black at defaults on every changed Python file, using the primary clone's
interpreter from the MAM-basics worktree. Run targeted tests while refactoring, then
run the real generators at the end.

Exercise candidate plus generation without writing the production tree:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_parse.py ws-products --output-dir .novc/retire-mam-parsed-plain-candidate
```

The candidate directory must contain only the surviving plus product and must pass
the transient raw validation and existing plus validation. Then regenerate the
tracked products through the normal pipeline.

Run the full suite from the worktree root:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py --basetemp .novc/pytest-retire-mam-parsed-plain -p no:cacheprovider
```

Run the full mega from the worktree root:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
```

Read the complete tracked diff. The expected changes are:

1. deletion of the plain JSON, pages, survey artifacts, authoring sources, claims,
   examples, and product-only tests;
2. parser-stage validation code and any purpose-led rename of the raw grammar lock;
3. plus JSON consumer-notice changes only, with all other plus data unchanged;
4. a self-contained plus survey and plus documentation;
5. regenerated MAM-parsed documentation, process graphs, claim inventory, and
   directly affected provenance or support files; and
6. current README, license, scope, help, and lint updates.

`MAM-simple/`, the MAM-for-Sefaria corpus CSV, MAM-with-doc book content,
`MAM-OSIS/` corpus content, Wikisource inputs, and unrelated published pages are
expected not to change. A full mega can expose an independent newer-input change;
record and explain such a diff separately, and stop if it is not understood.

Confirm mechanically that no live generator, current documentation target, test,
or product declaration requires `MAM-parsed/plain/` or
`out/tmpl-survey-plain/`, and that ordinary commands do not recreate either path.
Historical receipts may still contain the names.

Before staging, recheck `HEAD` against the recorded starting commit and require
status to contain only task-owned paths. Run `git diff --check`. Commit coherent,
verified MAM-basics work on `codex-worktree-1a58`. Do not push the worktree branch,
fast-forward primary `main`, or publish Pages. Report the exact implementation
commit and stop at the MAM-private compatibility gate.

## Phase 7: update MAM-private in a separate task

The MAM-private task begins only after the MAM-basics implementation commit exists
and its worktree is clean. Its prompt must identify:

- this plan and the exact MAM-basics implementation commit;
- `C:/Users/BenDe/.codex/worktrees/1a58/MAM-basics` as the source of the candidate
  `MAM-parsed/plus/` tree;
- the assigned MAM-private development checkout and its required starting commit;
- the fact that the MAM-basics task retains final integration responsibility.

The MAM-private executor must read its current instructions and plans, load
`codex-worktree-tasks` when applicable, load `mam-repository-topology`, and load
`hebrew-prose` before revising the notice. It must verify its own checkout before
editing and use one writer.

At minimum, audit and update:

- `near-aleppo/py/consumer_notice.py`, including `_MAM_NOTICE_SHA256` and the
  near-Aleppo notice's comparative reference to MAM-parsed plain;
- `near-aleppo/in/build-populations.json` and census provenance, if the changed plus
  tree identity requires their normal refresh procedure;
- generated near-Aleppo book notices and current HTML documentation;
- current comments, documentation, and checks that mention MAM-parsed plain; and
- vendored support such as `template_names.py` only if the MAM-basics implementation
  changed the source that MAM-private intentionally vendors.

Re-derive the near-Aleppo notice deliberately from the new self-contained MAM
notice. Preserve its dataset-specific changes; do not copy the MAM notice over it.
Point the MAM-private run at the exact unintegrated MAM-basics worktree through the
repository-supported `REPOS_ROOT` and `REPO_MAM_PARSED_DIR` mechanism, so the bytes
read are the bytes identified by the candidate MAM-basics commit. Follow
MAM-private's own census, generator, test, formatter, and integration rules rather
than inventing commands here.

Commit the complete, verified MAM-private compatibility change. Do not declare the
gate satisfied merely because the SHA constant was edited: the normal near-Aleppo
build, documentation generation, tracked outputs, and repository checks must pass
against the exact candidate plus tree.

## Phase 8: coordinated integration and close-out

Do not start close-out until both implementation commits are clean and verified.
Then:

1. Return to the MAM-basics worktree, merge current MAM-basics `main` into
   `codex-worktree-1a58`, and resolve all work on the worktree branch.
2. Run the required full MAM-basics mega after the merge. Read every tracked diff
   and commit every explained generated change. The suite is optional at this final
   integration gate unless the merge or fix changed executable behavior after the
   last full-suite result.
3. If the final plus notice or `MAM-parsed/plus/` tree identity differs from the one
   used by the MAM-private compatibility commit, the gate has reopened: update and
   reverify MAM-private before either repository is pushed.
4. With both repositories ready, fast-forward the primary MAM-basics checkout from
   the verified worktree branch and push MAM-basics `main` normally. Then integrate
   and push the prepared MAM-private compatibility commit under MAM-private's own
   rules in the same coordinated close-out. Never force-push either repository.
5. Verify local `main`, remote `origin/main`, and the intended implementation commits
   agree in both repositories. Verify both primary checkouts and development
   worktrees are clean.
6. Update this plan in place to `State: executed <date>` with concise execution
   findings: baseline and final commits, remeasured inventories, retained raw
   validations, test and mega results, explained generated diffs, MAM-private
   compatibility commit, integration order, and remote-ref verification. A
   documentation-only execution-record update does not expire the successful mega.
7. Archive or retire the worktree only when Ben asks or the normal task lifecycle
   reaches that point. Final integration remains the responsibility of the task
   that owns this plan.

## Stop conditions

Stop and report rather than improvising if any of these occurs:

- the required MAM-basics commit is not `HEAD` or an ancestor, the worktree is
  dirty for an unknown reason, or `HEAD` moves unexpectedly;
- a live internal consumer of persisted plain data is found outside the already
  approved MAM-private notice compatibility work;
- preserving a raw validation appears to require preserving the public survey or a
  persisted substitute;
- an existing raw validation conflicts with current parser behavior and updating
  the expectation would choose semantic policy;
- plus changes anywhere other than the approved notice and self-contained
  documentation/survey surfaces without a separately understood cause;
- the suite, mega, candidate generation, or MAM-private compatibility build fails;
- a generated diff is unexplained; or
- final MAM-basics merging changes the plus notice or tree after MAM-private was
  verified.

## Risk and reversibility

The product reach is high. This work deletes a distributed data product and
published documentation, changes all MAM-parsed-plus headers, changes generator and
validation code, and eventually publishes the result through `main`. The required
full suite, mega, diff review, and MAM-private gate follow from that reach.

The repository deletions are recoverable from Git history. Integration and pushes
are outward-facing and harder to undo, which is why the MAM-basics implementation is
committed but held before integration until MAM-private is ready. This plan does not
authorize force-push, history rewriting, discarding unrelated work, editing external
services, or preserving an unsupported compatibility product for hypothetical
external consumers.
