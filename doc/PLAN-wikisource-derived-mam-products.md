# Wikisource-derived MAM products

## Authorization and status

Ben's decision, 2026-09-10: implement the proposed change from Google-derived MAM
products to Wikisource-derived MAM products. Flesh out the implementation plan
before implementation where needed. Execute the work in fresh, small Codex tasks
that are unlikely to require context compaction. All tasks use the same worktree
and branch, with one writer at a time.

Ben's decision, 2026-09-10, during Phase 2: use `gpt-5.6-sol` for subsequent
implementation tasks. The Codex task-creation tool accepts an explicit `model`
argument, so create Phase 3 and each subsequent implementation successor with
`model = gpt-5.6-sol`; do not rely on inheriting the coordinator's Astra model.
No manual model change in the predecessor is necessary.

The accepted design is:

1. Wikisource downloads produce MAM-parsed-plain and MAM-parsed-plus.
2. Google Sheet downloads produce MAM-parsed-google, equivalent in contents to
   the current Google-derived MAM-parsed-plain.
3. MAM-parsed-google supplies only the Google input of `diff wsgo`. Ordinary
   MAM product generation does not depend on Google downloads or Sheet synchronization.

Status on 2026-09-10: Phases 1 and 2 are complete. Wikisource download planning
is independent of Google, and `parse ws-products --output-dir` generates complete
candidate plain/plus products. Corpus, serialization, rendering and independence
checks passed. Each candidate product differs from production in two explained
fields: Latin composition in 2 Samuel 22:40 and lower-dot order in Psalm 27:13.
Production plain/plus generation remains Google-derived; production artifacts and
raw inputs are unchanged. Phase 3, the Google product and independent comparator
input, is the next writing task. Verification receipts are under "Execution log".
Implementation is authorized; another approval is not needed.

## Exact development location and handoff

- Development checkout: `C:/Users/BenDe/.codex/worktrees/3a6b/MAM-basics`.
- Branch: `codex-worktree-3a6b`.
- Saved project: `ws-direct`, project ID `3f065f8d-6225-4734-b84d-ec5d68aad18e`.
- The task-creation target must use that project with `environment.type = local`.
  The saved path is already a worktree. Do not allocate another worktree or use
  the primary-clone project.
- Coordination task: `01a08bf0-82ce-7960-ae77-48eea708fa61`, titled
  `Create worktree branch name` when the handoff was prepared.
- Reviewed source commit: `5c0016b0fb65d35b6ee30b5e40cc95bf5365168f`.
  Each successor prompt must also name the newer handoff commit that contains
  the preceding phase's completed work.
- Primary clone: `C:/Users/BenDe/GitRepos/MAM-basics`.
- Shared interpreter: `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`.
  Use the interpreter by absolute path; do not create a worktree `.venv`.
- Remaining sibling inputs: `C:/Users/BenDe/GitRepos/MAM-private`.
  Read those inputs with `REPOS_ROOT=C:/Users/BenDe/GitRepos` where required.

Before editing, verify the top-level checkout, HEAD, checked-out branch, clean
status, and required commit ancestry. The reviewed checkout was clean on the
branch at the reviewed source commit. A different HEAD may be legitimate completed
work; inspect commits and file changes before proceeding. Do not discard work.

Load the live user-wide instructions at `C:/Users/BenDe/.codex/AGENTS.md`, this
checkout's `CLAUDE.md` (the repository instruction file), and the `hebrew-prose`
skill at `C:/Users/BenDe/.agents/skills/hebrew-prose/SKILL.md` before relevant prose
edits. Read `doc/agent-planning-principles.md` for verification principles. No
repository `AGENTS.md` existed at the reviewed commit.

Commit finished work locally before creating each successor. Record completed
work, validation, remaining questions, and the next bounded scope in this plan.
Create a successor only after the checkout is clean; verify its actual task ID,
checkout, and starting commit. The predecessor stops editing after the successor
starts. Tasks may remain open, but must not stage or edit concurrently.

Integration remains scheduled for archival under Ben's user-wide instructions.
Do not push the worktree branch or merge into main merely to dispatch a successor.
When Ben requests archival, serialize the shared writer, merge main into the
worktree branch, run the full suite there, fast-forward the primary clone's main,
and push main. If fast-forwarding refuses, repeat the merge and verification in
the worktree. Never resolve integration conflicts in the primary clone. Because
successors share the checkout, coordinate an archival integration with the
successor before touching the index. The coordinator retains responsibility for
its archival integration; subsequent task prompts must carry the same integration
discipline. Do not archive tasks or remove the worktree automatically.

## Review findings to carry into implementation

1. **Much of the parsing already exists.** `py/ws/ws_get_bk_in_both_fmts.py`
   produces Wikisource format 2. `py/ws/ws_in2_chap_body.py` separates verse prefix,
   location, and body. `py/subcommands/parse_go.py`, anchor
   `_do_light_books_in_bk24`, constructs the current plain product and calls
   `py/py_misc/mam_parsed_plus.py:add_plus_stuff`. The plus conversion does not
   read Google downloads. Preserve and reuse the plus conversion where possible.
2. **Wikisource downloading currently depends on Google.**
   `py/py_misc/get_wikisource_plan.py`, anchors `_get_zoo_book_plans` and
   `_get_book_plans_for_one_section`, reads the Google CSVs to find chapters.
   Remove that dependency without making a fresh Wikisource download depend on
   already-generated Wikisource products. Inspect existing book/chapter metadata
   before adding a new declaration. Verify coverage independently against the
   committed raw Wikisource corpus, including selectors and partial downloads.
3. **The Google input of the comparator must change explicitly.**
   `py/subcommands/diff_wsgo.py:_do_one_section_of_tanakh` currently reads
   MAM-parsed-plain as Google data and reparses `in/mam-ws` as Wikisource data.
   Leaving that reader unchanged after the source switch would compare Wikisource
   with Wikisource. Preserve the Google search strings and Wikisource replacement
   strings needed by the existing auto-edit process.
4. **Downloads have generation side effects.**
   `py/subcommands/download_google.py:run` calls `parse_go.almost_main` and
   `check_mpplus`. `py/subcommands/download_wikisource.py:run` reparses affected
   books. `py/subcommands/ws_bot_real.py` invokes the Wikisource refresh after
   editing. Reassign product writing and validation deliberately. A Google download
   must not overwrite Wikisource-derived plain or plus. Partial refresh of a
   source book must preserve the other sub-books in the corresponding 24-book file.
5. **Raw input and bot intermediates remain faithful captures.** Keep
   `in/mam-ws`, `in/mam-go`, and the bot's format-2 representation unchanged by
   product normalization. Use `mb_cmn.uni_denorm.give_std_mark_order` at the
   product conversion boundary. Do not apply Unicode normalization to Hebrew.
   Existing comparison conversions in `diff_wsgo/wsgo_ws.py` cover line-break
   notation, spaces, chapter wrappers, and good endings; inspect each conversion
   before sharing it with production code. Avoid making product generation depend
   on the comparison package merely because the scratch experiment reused it.
6. **The orchestrator and documentation need an explicit source switch.**
   `py/main_0_mega.py:_STEPS` currently starts with `parse-go` and runs `parse-ws`
   much later. Plain/plus documentation explicitly names Google as the source.
   `py/pipeline_graph/pipeline_graph_spec.py` generates `pipeline.dot` and
   `pipeline.svg`; `doc/process-documentation/MAM-process.dot` is directly
   authored. Render both SVGs through `py/main_pipeline_graph.py` so the Graphviz
   version pin applies.

## Measured corpus experiment and its limits

Measured against the reviewed source commit, with no downloads or tracked writes:

- Coverage: 39 source books, 929 chapters, 23,202 verses.
- Existing `diff wsgo`: zero difference records and zero auto-edits.
- A trial conversion with MAM mark order matched the parsed JSON structures of
  22 of the 24 plain book files and 22 of the 24 plus book files exactly.
- Both products differed in nine corresponding verse fields across Samuel and
  Psalms. Existing plus validation returned zero errors.
- The trial did not run downstream generators. Parsed JSON equality is not a
  claim of byte-identical serialization or complete migration readiness.

The remaining differences were:

| Location | Difference in trial output versus current output |
| --- | --- |
| 2 Samuel 22:40 | Precomposed versus decomposed accented Latin i in a note |
| Psalm 27:13 | Order of the combining lower dot within the same Hebrew clusters |
| Psalm 107:23-28, 40 | Space versus double underscore after an inverted nun |

The comparison's empty result does not prove exact product preservation. Account
for these differences through existing format/rendering contracts and corpus-wide
checks. The source switch is not authorization to silently change spacing or
rendered text. Do not add verse-specific patches simply to obtain equality with
Google. Establish the general representation rule; document any intentional
output change and obtain Ben's decision if a consequential choice remains.

The scratch experiment reparses committed Wikisource input, uses the existing
Wikisource-side comparison conversions, converts strings to MAM mark order,
round-trips the Wikitext sequence through the existing unparser/parser to get
plain cell structure, groups the source books, and calls the unchanged plus
function. That round trip is an experimental convenience, not a required
production architecture.

The reproducible scratch scripts remain in the exact development checkout:

- `.novc/review_ws_primary_pipeline_20260910.py` reruns the experiment and writes
  `.novc/review_ws_primary_pipeline_20260910_mam_order.json`.
- `.novc/inspect_ws_primary_review_20260910.py` reads that report and writes
  `.novc/review_ws_primary_pipeline_20260910_remaining_differences.json`.

Run from `C:/Users/BenDe/.codex/worktrees/3a6b/MAM-basics`:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/review_ws_primary_pipeline_20260910.py
```

The saved inspector records codepoint differences. Before rerunning that inspector,
remove its `NFC_equal` calculation: the Hebrew-normalization ban covers diagnostics
too. Use direct codepoint/cluster comparisons; the corpus experiment above does not
normalize Hebrew.

These scripts are untracked and are available because every successor uses the
same checkout. Remeasure; do not trust copied figures. Promote only useful
verification into maintained code through the repository's entry-point pattern.
The compact difference evidence is committed beside this plan as
`wikisource-derived-mam-products-review-differences.json`. A missing scratch script
does not justify trusting the figures: reconstruct the bounded check from the
method above or its coordinator task before using the figures as acceptance evidence.

## Implementation phases

Run these phases sequentially. Each task finishes its phase, records results here,
commits locally, verifies clean status, and creates the next fresh task using
`ws-direct` directly. Ben's 2026-09-10 request for fresh tasks supersedes the
context-compaction suggestion in `doc/agent-planning-principles.md`. Keep one
writer per checkout. Split an unexpectedly large phase at a coherent, verified
boundary and record the remaining scope before handing off.

### Phase 1: independent Wikisource download planning

Replace the CSV reads in `py/py_misc/get_wikisource_plan.py`, preserving the return
shape and ordering consumed by `py/ws/ws_download_selector.py` and
`py/subcommands/download_wikisource.py`. Reuse `bib_locales`' book/section roster,
`mam_bknas_and_std_bknas`' names, and `hebrew_verse_numerals`' spelling. The planning
inspection found no complete independent chapter-count declaration in those
modules. Check existing versification metadata before adding a small chapter-count
table, and verify any new declaration against the committed raw corpus. The runtime
planner must need neither CSVs, parsed products, nor previous downloads.

Before editing, capture the old planner's ordered book/chapter/title result in
scratch. Compare the replacement with that result and every chapter key in
`in/mam-ws`. Exercise all books and sections, every single-chapter selection, the
JSON selector's grouping/deduplication/order, and invalid chapters. Use differential
or lint-shaped verification; do not add example tests merely to pin the new table.
Make CSV reads raise during a scratch check to establish independence without
moving inputs. Run the existing downloader checks for batching and partial merging:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py py/tests/test_main_download_fr_wikisource.py
```

Acceptance: unchanged ordered coverage, selectors, titles and partial-download
merging; no raw or generated artifact changes; the corpus check and existing
downloader checks pass. Record the corpus check's exact command, commit, and start
Phase 2. Production plain/plus generation stays Google-derived during Phase 1.

### Phase 2: Wikisource adapter and representation accounting

Build a focused module converting format 2 to the existing plain schema, including
chapter prefix/suffix rows, good endings, templates, verse locations, and complete
39-to-24-book grouping. Extract shared plain-header construction from `parse_go`
where needed; reuse `mam_parsed_plus.add_plus_stuff`. Product conversion must not
import the comparison package. Raw parsing and bot format 2 remain faithful captures.

Expose candidate generation through `py/main_parse.py ws-products --output-dir`,
requiring an explicit output directory during this phase. The directory contains
`plain/` and `plus/`; candidate generation must not rewrite production documentation.
Default `parse ws` still writes format 2 only, and `parse go` stays the production
plain/plus writer until Phase 4.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_parse.py ws-products --output-dir .novc/ws-products-candidate-20260910
```

Compare every candidate JSON structure with production and compare serialization
separately. Run plus validation and MAM mark-order checks over the whole candidate.
Trace each relevant `wsgo_ws` conversion before sharing its meaning: comparison
equivalence is insufficient for a product's spacing contract. Resolve the nine
recorded fields through general rules, never verse-specific patches. Check spacing
after inverted nun through downstream renderers; retain source Latin composition
and distinguish Hebrew mark-order variation from text changes. Do not normalize
Hebrew, even diagnostically. The old scratch inspector's `NFC_equal` field is
historical diagnostic evidence, not an operation to copy into production.

Acceptance: complete corpus/schema coverage, successful validation, zero unexplained
differences, and production outputs unchanged. Record each justified representation
change and its rendering effect. If a consequential choice remains, present concrete
alternatives to Ben before cutover. Commit and start Phase 3.

### Phase 3: Google product and independent comparator input

Add `MAM-parsed/google/` using the current plain schema and filenames. This is
MAM-parsed-google's storage path, following the existing plain/plus naming scheme.
Reuse the CSV parser and preserve today's Google-derived plain contents. Add an
explicit Google accessor and reader, independent of `mam_parsed_path()`'s plus-tree
precondition. Keep the plain reader for ordinary plain-product consumers.

Temporarily let `parse go` write Google alongside existing plain/plus so the
intermediate commit has coherent writers. Rewire only `diff_wsgo`'s Google input;
Wikisource input stays a direct parse of `in/mam-ws`. Update immediate command
documentation to describe the intermediate state; Phase 4 removes the temporary
plain/plus writes.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_parse.py go
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py wsgo
```

Acceptance: every Google file equals the baseline plain file, plain/plus stay
unchanged, and comparator artifacts match the empty baseline. Use scratch or
in-memory inputs to show a Google-only change produces a difference and a
production-plain change does not affect the comparator. Verify Google search
strings and Wikisource replacement strings without writing to the Sheet. Audit
production Google-reader consumers: only `diff wsgo` may consume this product.
Commit and start Phase 4.

### Phase 4: production cutover and source documentation

Make `parse ws` produce format 2 and Wikisource-derived plain/plus. A selected
source book must rebuild its complete 24-book group from committed WS input so
sibling sub-books remain present. Make `parse go` and Google downloads write
Google only. Move plain/plus validation, generated docs and support copying to
WS product generation. Check the WS download hook and `ws_bot_real` refresh.

Start ordinary `main_0_mega` generation with WS parsing and remove its Google
parse/comparison dependency. Google parsing and `diff wsgo` remain explicit commands;
ordinary product generation must not depend on Sheet synchronization. Avoid parsing
WS twice in one run. Update source claims in authored plain/plus docs, command help,
support provenance, current runbooks and product READMEs. Update the pipeline spec
and authored `MAM-process.dot`; render both diagrams with `py/main_pipeline_graph.py`.
Leave historical release explanations and captures unchanged.

Acceptance: ordinary generation works with Google input access made to fail in a
scratch harness; Google generation leaves plain/plus untouched; selected WS refresh
preserves complete grouped books; raw and bot captures are unchanged; generated
differences match Phase 2's accounting and the source documentation. Run the local
commands below plus affected downloader, bot, path and documentation checks. Commit
and start Phase 5. No private generator runs in the primary clone.

### Phase 5: downstream verification and completion

Regenerate all local downstream steps, including examples, surveys, release reports
and accgram output. Use a scratch driver over maintained `main_0_mega._STEPS`, run
every local step in order, and omit only `near-aleppo-census`. Record the actual
step list and failures. Run doc/diagram CLIs separately where the mega invokes only
a core generator. A subset run is not a full mega run; no additional permanent
pipeline entry point is needed for this migration.

Compare artifacts against the baseline commit and Phase 2's report. Explain text
and spacing changes individually; identify routine provenance/timestamp changes
separately. Run Google parsing and `diff wsgo` explicitly, verify source independence,
and repeat affected generators for stability. Run the full suite with the environment
below; record its count and skip reasons. A baseline count never excuses a new failure.

The private census writer may stay outside local completion, with that limitation
stated. If private-effect verification is needed, read the private instructions and
create a disposable standalone clone of the committed private tree inside this
worktree's `.novc/`. Use a real Git clone because `run_all.py:tracked_scripts` uses
`git ls-files`. Pin and record its commit. Run from the disposable clone with
`REPO_MAM_PARSED_DIR` set to this worktree's `MAM-parsed` and `REPOS_ROOT` set to
`C:/Users/BenDe/GitRepos` for remaining read-only inputs. `census_paths.py` anchors
private writes to the clone containing the script. Verify resolved paths first.
Compare with private goldens before any `--write`; write goldens only in the clone.
Private primary-checkout files are not migration outputs to integrate here.

Acceptance: local generation and full suite pass; no unexplained generated changes;
Google/WS provenance is independent; raw inputs, historical releases and primary
source files stay unchanged. Record completion and archival integration responsibility,
commit cleanly, and stop creating successors when authorized implementation is complete.
Do not archive automatically.

## Baseline commands and scope

Measured HEAD: `67cb3ecc17931732d2cd1f9bbafee1976a322a2e` on
`codex-worktree-3a6b`. The checkout was clean before generation. The read-only
private input checkout was at `55252b834d28a6c241e75758aff5d15836621f56`.
Recheck both commits when repeating a measurement and record changed inputs.

All commands run from `C:/Users/BenDe/.codex/worktrees/3a6b/MAM-basics` using
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`. For the full suite:

```powershell
$env:REPOS_ROOT="C:/Users/BenDe/GitRepos"
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -rs
```

Use `.novc/ws_products_baseline_20260910.py` when the execution tool does not preserve
shell environment. It sets cwd/environment and captures UTF-8 logs. Successful runs
used approved elevated execution because the restricted sandbox could not launch
the shared interpreter. Sandbox Git reads used a command-local `safe.directory`
exception for the exact worktree; the wrapper passes that exception to child Git
processes through environment. No global Git configuration changed.

The driver `.novc/ws_products_regenerate_local_20260910.py` ran eight commands in
order, each prefixed by the absolute shared interpreter above:

1. `py/main_parse.py go` — plain/plus, documentation, claims and support copying.
2. `py/main_parse.py ws` — all format-2 books.
3. `py/main_diff.py wsgo` — comparison and auto-edit JSON.
4. `py/main_mam_with_doc.py` — all text-with-documentation pages.
5. `py/main_mam_simple.py` — all variants, support copies and documentation.
6. `py/main_mam4sef.py --both-sef-and-ajf` — both export variants.
7. `py/main_mam_osis.py` — OSIS export and validation.
8. `py/main_pipeline_graph.py` — pipeline DOT/SVG and authored-process SVG.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_products_regenerate_local_20260910.py
```

All eight returned zero. After regeneration, `git diff --stat` showed only the
manually escaped review-evidence field; no generated file changed. Both
`out/diff_mamws_mamgo.json` and `out/diff_mamws_mamgo-auto-edits.json` stayed empty
arrays. Documentation verification reported 79 passed, 0 failed and 1 pending
(`mp.plain.docs.book39-skeleton.common`), a baseline pending claim rather than a
skipped product build.

Logs and JSON command receipts are in `.novc/ws-products-baseline-20260910/`:
`suite.json` is the initial run, `suite-after-evidence-escape.json` the corrected
run, and `experiment.json` the corpus experiment. These files persist for successors
in the shared checkout; the commands and results here are the durable record.

The baseline excluded the private census writer entirely and created no private
clone. It did not run the remaining mega steps, including accgram regeneration,
release comparisons and vendoring audit. The baseline establishes synchronization
for the eight commands above, not the whole mega pipeline. In particular,
`main_0_mega.py:_run_near_aleppo_census` with `REPOS_ROOT=GitRepos` would write into
the private primary clone and must not be invoked that way.

Format changed tracked Python files with the shared interpreter's `-m black`
before committing. No inline scripts, shell here-documents or PowerShell here-strings.
Maintained verification must be differential or lint-shaped, without import-path
configuration. Raw downloads, historical releases, external datasets, credentials,
live Wikisource, the live Sheet, primary-clone source files and unrelated formatting
are not expected to change. Fresh downloads and live edits are outside this task.

## Execution log

- 2026-09-10: coordinator prepared the handoff at source `5c0016b0`, verified the
  saved project and clean branch, and retained the scratch corpus experiment.
- 2026-09-10: planning task `01a08c1d-40bc-7140-99a8-a060900b109f` verified the exact
  checkout, branch, clean status and required source `67cb3ecc`. `list_projects`
  confirmed `ws-direct`'s path; `CODEX_THREAD_ID` and `read_thread` confirmed the
  planning task's ID and checkout.
- 2026-09-10: the initial full suite returned **1 failed, 988 passed, 5 skipped**
  in 138.23 seconds. `TestHDotBelowNfc.test_no_decomposed_latin_diacritic_cluster`
  named the review-evidence JSON's decomposed Latin specimen. The specimen now uses
  the JSON escape `i\u0301`, preserving its decoded value and codepoint evidence.
- 2026-09-10: the full-corpus experiment rerun at `67cb3ecc` found 39 source books,
  929 chapters and 23,202 verses; 22 equal plain books and 22 equal plus books out
  of 24 each; nine changed fields in each product; zero plus validation errors;
  zero comparator records and zero auto-edits. No production candidate was written.
- 2026-09-10: all eight local regeneration commands passed with no generated
  differences. The corrected full suite (`py/main_test.py -rs`) passed:
  **989 passed, 5 skipped in 126.03 seconds**. All skips came from
  `test_edition_transcriptions.py:1168`: those controls require a page agreeing
  with its Wikisource strand. The JSON escape was checked against the committed
  evidence with `json.loads`; all decoded values are identical. No production
  Python changed, so no tracked Python required formatting.
- 2026-09-10: Phase 1 is ready for dispatch after this plan and the evidence fix
  are committed locally. The planning task stops writing when Phase 1 starts.
  Integration remains scheduled for archival, serialized with the successor.

### Phase 1 completion, 2026-09-10

Task `01a08c2c-001e-7c51-bd21-abc6c7e036f9` verified the development checkout
`C:/Users/BenDe/.codex/worktrees/3a6b/MAM-basics`, branch `codex-worktree-3a6b`,
clean status and starting HEAD `491cb6b84639a8235941e7ad63dd1d8127b82c67` before
editing. The required commit was HEAD. The checkout receipt is
`.novc/ws-products-phase1-checkout-20260910.json`; `read_thread` confirmed the
task ID and checkout, and `list_projects` confirmed the saved `ws-direct` path.

`py/py_misc/get_wikisource_plan.py` now constructs book plans from the existing
`bib_locales` roster and sections, existing MAM book names and existing Hebrew
numerals. The new `py/ws/ws_chapter_counts.py:BOOK39_CHAPTER_COUNTS` supplies
chapter counts. Inspection of `py/py_misc/vtrad_data.py` and
`py/clc/clc_versification.py` found verse mappings rather than complete chapter
counts; `bib_locales` supplies book metadata and a limited chapter-width grouping.
The new declaration is checked independently against every raw Wikisource book
by `py/tests/test_wikisource_plan_corpus.py`. The selector and downloader modules
are unchanged.

All commands below ran from the exact development checkout with the absolute
shared interpreter and approved elevated execution. Before editing the planner,
the following command captured its ordered book/chapter/title results, all book
and section selections, every single-chapter selection, and JSON selector results:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_products_phase1_20260910.py capture
```

The capture is `.novc/ws-products-phase1-old-planner-20260910.json`, tied to
starting commit `491cb6b84639a8235941e7ad63dd1d8127b82c67`. The capture command
refuses to overwrite that file. Do not recapture a replacement planner as the old
baseline. Verification of the replacement used:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_products_phase1_20260910.py check
```

The comparison returned zero and wrote
`.novc/ws-products-phase1-verification-20260910.json`. Its results were:

1. All 39 ordered book plans, 6 section selections, 929 single-chapter selections,
   and page titles equal the pre-edit results. All raw chapter keys equal the
   planned chapter keys in order, and the planned raw paths cover every raw file.
2. All 156 invalid-chapter cases and 237 JSON selector cases equal the pre-edit
   results. The JSON cases include reversed corpus order, duplicated chapter pairs,
   interleaved book pairs, empty input and invalid chapter values. Book order follows
   first appearance; chapter order follows the complete book plan.
3. All 70 request batches retain chapter order and the existing maximum of 20
   titles. All full-book plans are recognized as full; single-chapter plans are
   recognized as partial exactly when the book has additional chapters. All 77
   in-memory first/last-chapter merges retain every unselected chapter and the
   complete book order. No merged data was written to raw input.
4. The complete planner/selector comparison passes while Google CSV reads raise.
   A fresh planner import and full planning also pass with file opens blocked.
   Planning needs no CSV, parsed product or previous download.

Formatting ran successfully on every changed tracked Python file:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m black py/py_misc/get_wikisource_plan.py py/ws/ws_chapter_counts.py py/tests/test_wikisource_plan_corpus.py
```

The existing downloader checks and new corpus comparison ran through the baseline
wrapper, which sets explicit cwd, `REPOS_ROOT` and command-local Git configuration:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_products_baseline_20260910.py phase1-downloader py/main_test.py py/tests/test_main_download_fr_wikisource.py py/tests/test_wikisource_plan_corpus.py
```

Result: **15 passed in 0.39 seconds**, comprising 14 existing downloader checks
and the corpus comparison. The log and command receipt are
`.novc/ws-products-baseline-20260910/phase1-downloader.log` and
`.novc/ws-products-baseline-20260910/phase1-downloader.json`. The suite has automatic
discovery; the new test requires no registry entry. The full suite was not repeated
in Phase 1; the last full result remains the baseline above.

The Phase 1 diff contains only the planner, chapter-count module, corpus comparison
and this plan. Raw downloads, format 2, plain/plus, bot intermediates, historical
releases and generated documentation are unchanged. Phase 1 ran no downloads or
product generators and wrote no primary-clone source files. No unresolved Phase 1
finding remains.

The next task owns Phase 2 only: implement candidate `ws-products --output-dir`
generation, account for all representation differences and validate the complete
candidate corpus while leaving production outputs unchanged. After its verified
local commit, Phase 2 must start Phase 3 as a fresh task in `ws-direct` using
`environment.type = local`, and pass the same sequential handoff rule forward.
The Phase 1 task stops writing before Phase 2 starts. Integration remains scheduled
for archival and must be serialized with the successor writer.

### Phase 2 completion, 2026-09-10

Task `01a08c34-8c06-75d1-9623-cfad5aac6b5a`, `Build Wikisource product adapter`,
verified the exact development checkout, branch `codex-worktree-3a6b`, clean
status and starting HEAD `ee7ee2a05502e944162e34711da8210b50e2604f`. The
checkout receipt is `.novc/ws-products-phase2-checkout-20260910.json`.
`read_thread` confirmed the task ID and checkout; `list_projects` confirmed that
`ws-direct` still resolves to the development worktree.

The implementation adds `py/ws/ws_plain.py:convert_book`, a recursive format-2
adapter with no comparison-package import and no unparse/reparse round trip.
`py/py_misc/mam_parsed_plain.py:add_header` now supplies the shared header;
`parse_go` uses that function with unchanged output. The command module
`py/subcommands/parse_ws_products.py` groups every source book into complete
24-book files, reuses `mam_parsed_plus.add_plus_stuff`, writes the candidate
`plain/` and `plus/` directories and validates plus output. `py/main_parse.py`
exposes `ws-products` with required `--output-dir`. A production-tree destination
is rejected. Candidate generation writes no documentation or support copies.
`parse go` remains the production plain/plus writer; `parse ws` remains the
format-2 writer.

#### Representation rules and complete accounting

The adapter was checked against the meaning and consumers of each relevant
conversion in `py/diff_wsgo/wsgo_ws.py`:

1. Format-2 `¶` represents a source line boundary (`ws_get_bk_in_fmt_2` appends
   it after each input line). The plain spelling is `//`. Coalesce adjacent
   strings recursively, and use the existing template constructor for plain's
   `stmpl`/`tmpl` forms. An isolated `//` in a verse prefix becomes `__` only
   when the prefix lacks a spacing template; a documented spacing target counts
   as spacing. The explicit prefix template table fails on an unknown name.
2. A standalone `&#32;` becomes `__` in prefix context and a space in generic
   context. The inverted-nun template's argument has a separate established
   contract: its trailing space becomes `__`. This rule uses the template's
   name and argument, never a verse location. `render_wikitext_handlers.py`,
   anchor `_handle_inverted_nun`, requires the `__` spelling; the trial's plain
   space would fail its assertion. All seven Psalm 107 fields now equal
   production, and the two Numbers templates retain their lack of trailing space.
3. Apply `give_std_mark_order` to product strings. Preserve the existing
   adjacent-pair spelling `ha.GER_M + ha.REV`. The committed format-2 corpus
   contains 236 occurrences of the opposite adjacent order. Omitting the pair
   conversion produced 232 additional changed fields per product across Psalms,
   Proverbs and Job. The consumer `foiz_wt_rev_mug.py:_get_features` explicitly
   recognizes `GER_M` followed by `REV`, so the conversion preserves behavior
   beyond the comparison package. All those additional fields equal production
   after the general pair rule. No Unicode normalization is used in the adapter.
4. Reconstruct the noinclude wrappers in chapter rows `0` and `תתת`, and place
   each good ending with its `////` and section wrappers before the footer.
   Preserve verse prefixes, location templates and bodies. The category remains
   source-page metadata and is not a product row. All chapter boundary rows,
   locations, headers, book grouping and the four good endings equal production.

The final candidate and production files have the same serialization convention:
UTF-8, two-space JSON indentation, insertion order and a final LF. Comparing
parsed structures and comparing bytes independently both give 22 identical files
out of 24 per product. There are two changed verse fields and four changed string
leaves per product, completely accounted for below.

| Field | Candidate behavior | Rendering effect |
| --- | --- | --- |
| 2 Samuel 22:40, E | Preserve source `í` (U+00ED) in the note instead of Google's `i` plus U+0301. | The documented renderer retains this composition difference in the note. MAM-simple omits the note, so its output has no corresponding difference. |
| Psalm 27:13, E | Preserve source lower-dot order outside MAM's declared mark priorities; three string leaves differ. | The documented renderer retains the order difference in the text, lemma and note; MAM-simple retains the order difference in the verse text. Direct cluster comparison confirms identical base characters and identical mark multisets, with no spacing or character-content change. |

There is no unresolved product representation choice. The compact durable receipt
is `doc/wikisource-derived-mam-products-phase2-validation.json`, including exact
codepoint differences, renderer differences, counts and all inverted-nun results.
Its JSON escapes preserve the diagnostic strings without introducing decomposed
Latin specimens into hand-authored source. The old inspector's `NFC_equal`
calculation was removed before its `walk` helper was reused. No Hebrew
normalization was added to, or called by, the candidate comparison or renderer
checks.

#### Phase 2 verification commands

Every command ran from `C:/Users/BenDe/.codex/worktrees/3a6b/MAM-basics` with the
absolute shared interpreter and approved elevated execution. The baseline wrapper
supplied the already-documented cwd, `REPOS_ROOT` and command-local Git settings.
The candidate generation command is the Phase 2 command above. Complete structure,
key-order, row-length, coverage, mark-order and serialization comparison used:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_products_phase2_verify_20260910.py
```

Result: 39 source books, 929 chapters, 23,202 verses, 24 files per product, zero
plus validation errors and zero candidate files outside MAM mark order. All
metadata and collection shapes match production; only the fields in the table
differ. Detailed receipt: `.novc/ws-products-phase2-verification-20260910.json`.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_products_baseline_20260910.py phase2-render .novc/ws_products_phase2_render_20260910.py
```

Result: all 39 books and 23,202 verses rendered with the MAM-with-doc options and
the MAM-simple XML renderer. The documented rendering differs only at the two
locations in the table; the simple rendering differs only at Psalm 27:13.
All nine inverted-nun elements match production. Their actual simple elements
were also passed through the Sefaria, AJF and OSIS handlers: the seven trailing
spaces remain NBSP in Sefaria/OSIS and ordinary space in AJF; Numbers retains no
added space. Detailed receipt: `.novc/ws-products-phase2-rendering-20260910.json`.
Initial scratch harness attempts omitted the documented-renderer options and
used the wrong AJF dispatch level; both harness errors were corrected before the
successful whole-corpus run. No renderer implementation changed.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_products_baseline_20260910.py phase2-independence .novc/ws_products_phase2_independence_20260910.py
```

Result: the real candidate CLI succeeds while every open under `in/mam-go` and
production `MAM-parsed` raises, comparison-package imports raise, and file writes
are confined to the scratch candidate directory. All 39 reparsed format-2 books
equal the committed format-2 artifacts and remain unmodified after conversion.
All 48 candidate files equal the first candidate byte for byte. The input census
records four good endings, 62,499 templates, 33,555 line boundaries, nine standalone
space entities and the 236 adjacent pairs described above. Detailed receipt:
`.novc/ws-products-phase2-independence-20260910.json`.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_products_phase2_receipt_20260910.py
```

Result: the CLI rejects a missing destination and a production destination before
generation. The script also writes the compact durable receipt from the measured
scratch reports; it does not generate products.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_products_baseline_20260910.py phase2-google-regeneration py/main_parse.py go
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_products_baseline_20260910.py phase2-format2-regeneration py/main_parse.py ws
```

Both returned zero with no generated changes. Google regeneration's documentation
checks reported 79 passed, zero failed and the same one pending claim. Default WS
parsing wrote only unchanged format-2 artifacts. Comparator code and its existing
empty output artifacts were unchanged; Phase 2 did not rerun `diff wsgo`.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m black py/main_parse.py py/subcommands/parse_go.py py/subcommands/parse_ws_products.py py/py_misc/mam_parsed_plain.py py/ws/ws_plain.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_products_baseline_20260910.py phase2-suite py/main_test.py -rs
```

Formatting passed. The full suite passed **990 tests, with 5 semantic skips in
107.19 seconds**. The skips are the same transcription controls at
`test_edition_transcriptions.py:1168` as the baseline. Phase 2 added no tests.
Logs and command receipts use the labels above under
`.novc/ws-products-baseline-20260910/`.

After staging the new source and receipt, the wrapper label `phase2-source-lints`
ran `py/main_test.py py/tests/test_prose_mark_order.py
py/tests/test_h_dot_below_nfc.py py/tests/test_entry_point_subcommands.py`:
**29 passed in 20.07 seconds**. This check includes the new files in scans based
on Git's tracked-file list. `git diff --cached --check` also passed.

#### Phase 3 handoff boundary

The next task owns Phase 3 only: add the Google product and explicit reader,
temporarily retain coherent Google/plain/plus writing, rewire the comparator's
Google input, and verify source independence and search/replacement payloads.
Production cutover remains Phase 4. One existing comparator implementation detail
requires attention before Phase 3 runs the comparator: `wsgo_go.py:_massage_wtel`
still calls `unicodedata.normalize("NFC", wtel)` on strings that include Hebrew.
The candidate code does not share that helper. Honor the Hebrew-normalization ban
when verifying the comparator, while preserving its comparison equivalences and
original source strings for search/replacement. A direct cluster comparison is
available in the Phase 2 scratch rendering check.

Raw downloads, production plain/plus, format 2, bot intermediates, historical
releases, generated documentation and primary-clone source files are unchanged.
Phase 2 ran no downloads, live edits or private generators. After the verified
local commit, create Phase 3 as a fresh task using `ws-direct` with
`environment.type = local`, and pass the sequential handoff rule forward through
Phase 5. The Phase 2 task stops writing before Phase 3 starts. Integration remains
scheduled for archival, serialized with the successor writer; no worktree-branch
push or immediate integration is part of this handoff.
