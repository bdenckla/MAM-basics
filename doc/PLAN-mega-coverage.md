# PLAN — make the mega run everything it should, and record why the rest does not

Written by a Claude session on 2026-09-10. Ben's instructions that day were: "An analysis of what
is and isn't part of mega should be made", "Everything that is not part of mega should have a
recorded justification as to why it is not in mega", and "It should be part of repo maintenance
(if it is not already) to check that the only programs not part of mega are those that have
documented justifications for why they are not part of mega." His answers to the six decisions in
`doc/mega-coverage-2026-09-10.md` §1 are recorded there, quoted, and his later decisions of the
same day are quoted in the phases they changed. Everything else here is that session's
reconstruction.

## How this plan is executed

- **One phase per session, never two.** Each phase below is sized so that one session, or one
  sub-agent, can finish it without its context growing large. Ben's instruction, 2026-09-10: the
  sessions are to be "small enough to likely avoid compaction". Stop at the end of the phase and
  report; do not start the next one.
- **The checkout is the worktree `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/mega-coverage`,
  on branch `claude/mega-coverage`. Never create another worktree for this plan, and never edit,
  stage or commit in the primary clone `C:/Users/BenDe/GitRepos/MAM-basics`.** Ben's instruction,
  2026-09-10: "we want to re-use this worktree".
- **Before editing, verify the checkout**, per `~/.claude/CLAUDE.md` §"A successor session verifies
  its exact checkout and commit before editing":
  - `git -C C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/mega-coverage rev-parse --abbrev-ref HEAD`
    prints `claude/mega-coverage`;
  - `git -C … status --porcelain` prints nothing;
  - `git -C … log --oneline -1` is the commit the orchestrating session names in the phase's brief.
  Stop and report on any mismatch.
- **Read before the first edit:** `CLAUDE.md` in the worktree, `~/.claude/CLAUDE.md`, and
  `doc/mega-coverage-2026-09-10.md`, which is the analysis this plan executes and names every
  program by path.
- **The interpreter is the primary clone's venv, by absolute path:**
  `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`, with the worktree as the current
  directory. Since phase 1 (`516a4a1a`) no `REPOS_ROOT` is needed in this worktree.
- **The Glob tool finds nothing inside `.claude/`, where this worktree lives.** Use
  `git -C <worktree> ls-files <path>`, or Grep with an explicit path.
- **Never run the `near-aleppo-census` step.** It rewrites tracked goldens in MAM-private's primary
  clone, and its `gershayim_contexts.py` output will change on the next real mega run because the
  MAM-OSIS clone is gone; Ben has acknowledged that change, and that run is his, not this plan's.
  To exercise mega steps, run their runners from a throwaway script (import `main_0_mega`, pick
  steps from `_STEPS` by `step_id`), never `py/main_0_mega.py` whole, and never `--resume-from` a
  step that the census follows.
- **Do not modify MAM-private at all.**
- **Commit discipline:** black on every changed `.py`
  (`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m black <files>`); the full suite
  (`… py/main_test.py -q -p no:cacheprovider`, from the worktree root) green before committing;
  commit messages in a temp file passed with `git commit -F`; `git commit -- <paths>` naming
  exactly the phase's files; commit on the branch and do not push, do not merge. Throwaway scripts
  and message files go under the worktree's gitignored `.novc/mega-coverage-phase<N>/`. The
  orchestrating session integrates once, at the end, by `~/.claude/CLAUDE.md`'s four-step
  integration.
- **Generated output is the test.** When a new step regenerates a tracked file, the file must come
  out byte-identical, or the diff must be explained before it is committed. An unexplained diff is
  a finding to report, not a thing to commit. A vendored copy's LAST_SYNCED date in
  `out/vendoring_compare_out.txt` is its last commit date, so re-run `py/main_vendoring.py --all`
  AFTER committing a change to a copied support file, not before.
- **Report, at the end of the phase:** the commit hash; the files changed; the suite's result line;
  every regenerated file and whether it was byte-identical; and anything left undecided.

## Phase 1 — find sibling repos beside a worktree's home clone: DONE, `516a4a1a`

`paths.repos_root()` now falls back to the parent of the checkout's home clone, read by
`provenance.home_clone_dir()`. A worktree run finds MAM-private with nothing exported. Suite in
the worktree with nothing exported: 988 passed, 5 skipped.

## Phase 2 — run the post-stress-meteg survey in the mega, skipped in the cloud: DONE, `9657a081`

Ben's decision, 2026-09-10: the survey "should join mega as long as" a worktree run finds
MAM-private next to its home clone (phase 1), and "when it detects it is running in the cloud, it
skips the MAS survey altogether (there is already precedent for this with respect to anything
needing graphviz)".

`accgram-survey-post-stress-meteg` is step 40 of 42, immediately before `gen-site`. In a cloud
session it is recorded as skipped, and the end-of-run banner, renamed `_report_cloud_skips`,
reports skipped steps beside skipped SVG renders. `py/main_0_mega.py --resume-from
accgram-survey-post-stress-meteg` rewrote 16 tracked files: 15 byte-identical, and
`out/vendoring_compare_out.txt`, whose LAST_SYNCED date for the `provenance.py` copy moved because
phase 1 recommitted that copy. Suite: 988 passed, 5 skipped.

## Phase 3 — remove the Wikisource index generators, the plots, and the Sefaria download: DONE, `985262e2`

Ben's decisions, 2026-09-10: the two Wikisource index generators "will never be run again", so
"remove them (and their outputs) from the repo entirely!"; the column-coordinate plots "were
one-time experiments"; and "Let's get rid of in/mam-from-sefaria", with its download command,
since "I'm no longer interested in tracking what sefaria does with what we give them".

64 files deleted and 20 edited, `CLAUDE.md`, `py/ac_paths.py` and `py/repo_scopes.py` among them;
no Leningrad code remains. The pipeline graph was regenerated with Graphviz 16.0.0: its `.dot` lost
exactly the Sefaria node and edge, and Graphviz re-laid out the `.svg` around the gap.
`py/tests/test_h_dot_below_nfc.py`'s "Aleppo data" floor went from 19 to 17, that scope having lost
three files. Suite: 988 passed, 5 skipped.

## Phase 4 — skip the census in the cloud, then fold `py/main_uxlc_mega.py` into the mega: DONE, `bf6316a2` and `f7fb6a62`

Ben's decisions, 2026-09-10: "the near-aleppo census should be skipped if mega detects that mega
is running in the cloud", and folding `py/main_uxlc_mega.py` into the mega: "agreed".

`bf6316a2` skips `near-aleppo-census` in a cloud session the way phase 2 skips the survey. A
simulated cloud run, with `subprocess.run` stubbed to raise, listed both steps in the end-of-run
banner, so a cloud run of the mega now needs no MAM-private. `f7fb6a62` made steps 34–38 of 47 of
`uxlc-check-changes`, `uxlc-fois`, `uxlc-write-page-break-info`, `uxlc-amb-early-mtg` and
`uxlc-word-list`, before `find-uxlc-accent-changes`. It deleted `py/main_uxlc_mega.py`, and made
`py/main_uxlc_download_changes.py` download only. The five steps regenerated 113 tracked files, all
byte-identical to their committed blobs, `in/UXLC-misc/all_changes.json` included. Suite before
each commit: 988 passed, 5 skipped.

## Phase 5a — add the UXLC, Holman, CLC and book-of-job generators

Ben agreed, 2026-09-10, to "add the other offline generators of tracked files". Read each program's
entry point before wiring it; call the function its command line reaches.

1. `py/main_clc.py all`, as a step `clc`.
2. `py/main_estimate_uxlc_locations.py` and then `py/main_render_uxlc_corrections.py`, as two steps
   in that order: the renderer raises on incomplete coverage. Correct both docstrings' stale
   reasons, which say the UXLC XML is not tracked here and name a "sibling UXLC-utils clone".
3. `py/main_verify_and_render_table.py`, as a step. It raises on a verification failure, which is
   wanted.
4. book-of-job's site generator, `py/main_gen_misc_authored_english_documents.py`, as a new step
   `book-of-job-site`; then `py/main_map_changes_to_book_of_job.py` after it, since it reads that
   generator's pages. **Rename the existing step `gen-misc-authored-english-documents` to
   `gen-misc`**, the `main_authored.py` subcommand it actually runs, so that the step and the
   book-of-job file stop sharing a name. The generator ends in a spell check that calls `exit(1)`
   on any finding, so from now on a spelling finding fails the mega. That is intended; say so in
   the step's note.
5. In `doc/PLAN-evacuate-the-rest-of-three-repos.md`, the sentence "book-of-job's oracle is the one
   that is also a mega step" has been false since `3e3b6e0b` (2026-05-06). Add a dated correction
   beside it rather than rewriting the record.
6. Verify as in phase 4: run the new steps from a throwaway script, explain every diff, then the
   full suite.

## Phase 5b — add the MAM-side and remaining generators, the mpplus check, and the warnings fix

1. The doc half of `py/main_mam_simple.py`: a step `mam-simple-docs` after `mam-simple`, running
   what `_write_generated_docs` runs. Give it a public name.
2. `py/main_diff.py ctr-vs-mam`, as a step after `parse-go`. Its output `out/diff_ctr_mam.json` has
   not been committed since 2026-03-09, so expect a first-run diff. Explain it, from the generator's
   and the inputs' history, before committing; if it cannot be explained, stop and report.
3. `py/main_search_final_hiriq_verse_text.py` and `py/main_search_holam_he_qere.py`, as steps
   after `wordlist`, whose output the second one reads. Correct their comments that say the output
   goes through `require_sibling`.
4. `py/main_pipeline_graph.py`, as a step before `vendoring-audit`. Graphviz is already required by
   `tmpl-survey`, and `survey_dot.render_svg` already skips a render in the cloud.
5. `py/main_diffable_pointed_hebrew.py`, as one step covering its four fixed input and output
   pairs; `diffable-pointed-hebrew/README.md` and `misc/zarqa-table-diff/make-dph-files.ps1` name
   them.
6. `py/main_ac_gen_index_flat_annotated.py`, as a step.
7. **`check_mpplus`** (`py/py_misc/check_mpplus.py`), as a step `check-mpplus` immediately after
   `parse-go`, failing the mega on any error, as `py/subcommands/download_google.py`'s `run` does;
   that download path keeps its own call. Today the check runs only there, inside
   `py/main_download.py fr-google`, while the mega's `parse-go` step runs the same parse and skips
   the check that follows it on the download path. Ben, 2026-09-10: running it in the mega "checks
   the check", making sure the check itself still works. It also covers the other way the plus
   JSON changes: `parse-go` regenerates it from the tracked CSVs on every mega run, so a change to
   the parser, or to the check's own rules, reaches the data with no download at all.
8. **Fix `ws-bot-proto`'s `warnings.json`.** Warnings are collected only for an edit file. The
   mega's run has none: `no_edits()` in `py/ws/ws_bot_edit.py` returns a context with no
   `get-warnings` key, so `write_warnings` returns without writing, and the tracked
   `out/mam-ws-bot/proto-misc/warnings.json` keeps whatever the last `proto --edits` rehearsal
   wrote while the proto files beside it are overwritten without edits. Ben, 2026-09-10: "that
   seems bad, let's fix that." Make every proto run write the file, in its empty form when there
   are no edits, so that it always belongs to the same run as its neighbours. The `ws_bot` tests
   pin edit payloads on purpose (`CLAUDE.md`), so read them before changing the edits context.
9. Verify as in phase 4.

## Phase 6 — delete the dead and redundant programs, and retire `check_ac_word_finding.py`

Ben agreed, 2026-09-10. The analysis's §6 has each with its evidence.

1. The `__main__` blocks of the fifteen `py/accgram/` library modules §6 lists. Where a function
   exists only for its `__main__` block, it goes too; check `py/tests/` first.
2. The `__main__` blocks of the eight `py/py_ac_loc/` and five `py/py_cam1753_loc/` modules. Keep
   each `main()` that a `main_ac_*` or `main_cam1753_*` wrapper calls. (Phase 3 already deleted
   `py/py_ac_loc/plot_col_coords.py`, one of the eight.)
3. `py/ws/ws_tmpl_parser.py`'s `__main__` block, with `_do_quick_test` and the test-case tables only
   it uses.
4. `py/main_ac_kraken_seg_baselines.py` and `py/py_ac_loc/kraken_seg_baselines.py`, and their entry
   in `ac_paths.AC_TOP_LEVEL_MODULES`; add a dated note to `aleppo/doc/ocr-with-kraken.md`.
5. `py/main_gen_aleppo_crop_editor.py`, with any path-list entry naming it and a dated note in
   `doc/boj-aleppo-word-crops.md`.
6. `py/main_verify_meteg_vs_mgketer.py`.
7. The `holman-meteg-spec` subcommand of `py/main_ws_bot.py`, and `py/ws/holman_meteg_edit_spec.py`
   if nothing else uses it. The two spec files in `in/mam-ws-bot-edits/` stay as records.
8. `py/main_source_hygiene.py`; `py/tests/source_hygiene_test.py` runs the same scan.
9. The dead code in live modules: `example_run()` in `py/main_uxlc_estimate_atom_loc.py`, and the
   uncalled `add_args` and `run` at the end of `py/author_site/post_stress_meteg.py`.
10. **`py/check_ac_word_finding.py`: fix it, then retire it, in two commits.** Ben, 2026-09-10:
    "why not fix it and then delete it, i.e. retire it in good working form."
    - **The fix, committed first.** codex-index-aleppo's `eb4bcaf` (2026-03-14, "Add Deut support
      and migrate column IDs to NofM format") changed every `line-breaks/*.json` from `"col": 1` to
      `"col": "1of2"`, so the finder has returned `"NofM"` strings since, while the expected values
      in `aleppo/test-data-from-book-of-job.json` keep the bare column number. Compare the number
      only, and show the check passing: `PASS: 160`.
    - **The retirement, committed second.** Delete the check; its fixture
      `aleppo/test-data-from-book-of-job.json`, which nothing else reads; and
      `ac_paths.word_finding_test_data_path()`. Remove its import, list entry and docstring line
      from `py/check_ac_all.py`, and its entry from `ac_paths.AC_TOP_LEVEL_MODULES`.
      `py/check_cam1753_all.py`'s docstring compares its own check with this one, so update that
      sentence. Deleting the fixture shrinks `py/tests/test_h_dot_below_nfc.py`'s "Aleppo data"
      scope again, so lower its floor again, by the file's own convention of one below the count.
11. **J David Stark's `aleppo/aleppo-wiki/J David Stark Aleppo Codex Index.csv`.** Ben,
    2026-09-10: "That Stark CSV file can be removed." Nothing has read it since phase 3 removed the
    Aleppo index generator. Keep `LICENSE.txt`, which still covers `index-flat-corrected.json`, a
    hand-corrected form of the same index, and keep `precursors/`, which Ben's answer did not name.
    Update what describes the CSV: `aleppo/aleppo-wiki/provenance.md`, `DATA-LICENSES.md`,
    `ac_paths.wiki_dir()`'s docstring, and the comment in `py/tests/test_h_dot_below_nfc.py` that
    explains why `aleppo-wiki/` is in its scope. That deletion shrinks the "Aleppo data" scope too,
    so set its floor once, after both deletions.
12. `doc/PLAN-repo-maintenance-across-GitRepos.md`, a live runbook, still names `py/lenin_paths.py`,
    which phase 3 deleted, in a bullet that was already stale before then. Correct it.
13. Verify: the reference sweep for every deleted name, the full suite.

## Phase 7 — build the check

Ben agreed, 2026-09-10. Build `py/tests/test_mega_coverage.py` to the design in
`doc/mega-coverage-2026-09-10.md` §7, reusing `py/tests/test_sibling_reach.py`'s AST approach and
its dead-entry check.

1. **Programs:** every tracked `.py` with a `__main__` guard outside `py/tests/`, including the
   `py-examples` scripts, found by AST. For an argparse entry point, every subcommand name,
   including names built from a table.
2. **In the mega:** what `py/main_0_mega.py`'s runners call: imported entry modules whose functions
   a runner calls, subcommands named in `almost_main([...])` calls, and script paths in subprocess
   argv.
3. **`NOT_IN_MEGA`:** a dict from program key to reason, each reason citing where it is recorded.
   Take the rows of the analysis's §3 with their citations, and §4's rows marked as Claude-written
   proposals not yet reviewed by Ben. Add Ben's 2026-09-10 decisions: the slide thumbnails ("don't
   include these thumbnail-generator-programs in mega") and the line-break reports ("it served its
   purpose for the book-of-job project"). Add whatever phases 2–6 leave out. Where the mega runs
   one flag-selected mode of a program and not another, declare the other mode by hand.
4. **Failures:** a program neither run nor declared; a declaration whose program is gone; a
   declaration whose program the mega now runs.
5. Name the check in `py/main_repo_maintenance.py`'s docstring, whose step 5 runs the suite before
   step 6 runs the mega, and correct that docstring's stale list of mega steps. Also correct
   `py/mb_cmn/graphviz_pin.py`'s docstring, which says `tmpl-survey` is "step 5 of 41": the mega
   had 47 steps after phase 4, and phases 5a and 5b add more. Grep for any other stated step count.
6. Verify: the full suite green; then, uncommitted, delete one declaration and see the check fail
   naming that program, and restore it.

## Phase 8 — full verification

1. From a throwaway script, run every step of `_STEPS` except `near-aleppo-census`, in order, with
   nothing exported.
2. `git status` must be clean. Any diff is explained and committed on its own, or reported.
3. Run the full suite.
4. Update `doc/mega-coverage-2026-09-10.md` with a closing record of what the mega now runs, which
   also retires its §3 and §5 rows for the post-stress-meteg survey, and report the branch head for
   the orchestrating session to integrate.

## Not in this plan, raised for Ben

1. **`uxlc/data/lci_augrecs.json` has had no reader since phase 3** removed the Leningrad index
   generator, its only reader. `py/main_write_page_break_info.py` still writes it, beside an
   identical `uxlc/out/UXLC-misc/lci_augrecs.json`, and becomes a mega step in phase 4.
   `py/uxlc_paths.py`'s `data_dir()` docstring still calls that directory data "other repos
   consume".
2. The incidental findings of the analysis's §8, except those a phase above fixes on its way past.
