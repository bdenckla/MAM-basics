# Wikisource-derived MAM products

## Authorization and status

Ben's decision, 2026-09-10: implement the proposed change from Google-derived MAM
products to Wikisource-derived MAM products. Flesh out the implementation plan
before implementation where needed. Execute the work in fresh, small Codex tasks
that are unlikely to require context compaction. All tasks use the same worktree
and branch, with one writer at a time.

The accepted design is:

1. Wikisource downloads produce MAM-parsed-plain and MAM-parsed-plus.
2. Google Sheet downloads produce MAM-parsed-google, equivalent in contents to
   the current Google-derived MAM-parsed-plain.
3. MAM-parsed-google supplies only the Google input of `diff wsgo`. Ordinary
   MAM product generation does not depend on Google downloads or Sheet synchronization.

Status on 2026-09-10: design review and an in-memory corpus experiment are complete.
No production code or generated product has changed. The next task must finish
the phased plan, establish the baseline, commit the plan, and dispatch the first
implementation task. Implementation is authorized; another approval is not needed.

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

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/inspect_ws_primary_review_20260910.py
```

These scripts are untracked and are available because every successor uses the
same checkout. Remeasure; do not trust copied figures. Promote only useful
verification into maintained code through the repository's entry-point pattern.
The compact difference evidence is committed beside this plan as
`wikisource-derived-mam-products-review-differences.json`. A missing scratch script
does not justify trusting the figures: reconstruct the bounded check from the
method above or its coordinator task before using the figures as acceptance evidence.

## Proposed small implementation phases

The fresh planning task must refine these boundaries and write concrete commands,
dependencies, and acceptance checks before dispatch. Each implementation task
completes only its named phase and commits before creating the next fresh task.
Split a phase further if its scope grows; do not use context compaction as the
intended handoff mechanism.

1. **Independent Wikisource download planning.** Replace the Google-derived
   book/chapter roster and verify unchanged selection/coverage against independent
   committed input. Keep production plain/plus generation unchanged in this phase.
2. **Wikisource-to-product conversion and differential verification.** Build a
   reusable adapter to the existing plain schema, reuse plus generation, and settle
   the measured representation differences. Exercise alternate output paths so
   the current production products remain the comparison reference until cutover.
3. **MAM-parsed-google and comparison input separation.** Add the Google product
   and an explicit reader, rewire `diff wsgo`, and prove that the comparator still
   distinguishes independent Google and Wikisource inputs. Arrange the transition
   so intermediate commits still have coherent writers; the planning task may
   combine a small part of phase 4 here if required.
4. **Production cutover and documentation.** Switch default product generation,
   download/refresh hooks, orchestration, paths and checks; update source claims,
   provenance, runbooks, and both process diagrams. Keep existing downstream
   public paths and schemas unless a separately justified change is necessary.
5. **Downstream verification and completion.** Regenerate the downstream products
   from committed input, account for all differences, rerun affected generation
   for stability where needed, and run the full suite. Record completion and
   remaining archival integration responsibility. Do not create another task if
   all authorized implementation work is complete.

## Baseline and verification requirements for the planning task

The baseline full test count and generated-output synchronization were **not
measured by the design review**. Establish both before implementation and record
the actual commands, source HEAD, results, and any unexplained differences.
The old count quoted in `CLAUDE.md` is not a new measurement.

Set the sibling-input location in the shell used for the suite:

```powershell
$env:REPOS_ROOT="C:/Users/BenDe/GitRepos"
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py
```

Use a real scratch script with an explicit environment and captured UTF-8 log if
the execution tool does not preserve shell environment across calls. No inline
Python, shell here-documents, or PowerShell here-strings. Format changed tracked
Python files with the shared interpreter's `-m black` before committing. New
maintained verification must be differential or mechanical lint, never a global
import-path adjustment or a test that merely repeats the implementation.

Important execution boundary: `py/main_0_mega.py:_run_near_aleppo_census` writes to
`MAM-private/near-aleppo/census/expected` through a subprocess. A worktree mega run
with `REPOS_ROOT` pointing at `GitRepos` would therefore modify the primary private
checkout. Do not do that. The planning task must name the local-product regeneration
commands and either verify the private writer in an isolated scratch copy or
explicitly keep that writer outside the local regeneration run. Report the actual
scope; do not claim a full mega run if a step was omitted. This project does not
authorize development writes in `C:/Users/BenDe/GitRepos/MAM-private`.

During implementation, expected changes are parser/reader/orchestration code, the
new Google parsed product, source/provenance documentation, process diagrams, and
only explained generated differences. Raw downloads, historical releases, external
datasets, credentials, live Wikisource, the live Google Sheet, primary-clone source
files, and unrelated formatting are not expected to change. Perform the migration
against committed downloads; live edits and fresh downloads are unnecessary for
the design and are not part of this authorization.

## Execution log

- 2026-09-10: coordinator prepared this handoff at source `5c0016b0`, verified
  the exact saved worktree project and clean branch, and retained the corpus
  experiment under `.novc`. Fresh planning and implementation tasks are pending.
