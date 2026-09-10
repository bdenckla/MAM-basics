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

## Phase 5a — add the UXLC, Holman, CLC and book-of-job generators: DONE, `e4cf78e6`

Ben agreed, 2026-09-10, to "add the other offline generators of tracked files". Six steps, 39–44 of
53, between `uxlc-word-list` and `find-uxlc-accent-changes`: `clc`, `estimate-uxlc-locations`,
`render-uxlc-corrections`, `verify-and-render-table`, `book-of-job-site` and
`map-changes-to-book-of-job`. The step that ran `main_authored.almost_main` under the name
`gen-misc-authored-english-documents` is now `gen-misc`, so book-of-job's site generator no longer
shares a name with a step that does not run it; `doc/PLAN-evacuate-the-rest-of-three-repos.md` has
a dated correction beside its false sentence. The six steps regenerated 207 tracked files, all
byte-identical to their committed blobs; book-of-job's spell check found nothing. Since this phase,
importing the mega needs `pyspellchecker` and Pillow, which book-of-job's generator imports and
`requirements.txt` names. Suite: 988 passed, 5 skipped.

## Phase 5b — add the MAM-side and remaining generators, the mpplus check, and the warnings fix: DONE except item 2, `2e3a7189`, `c42089e2` and `a153ccb5`

`2e3a7189` makes `write_warnings` write `out/mam-ws-bot/proto-misc/warnings.json` on every proto
run, `[]` when there are no edits: the file went from the six entries of the `52aa7b8c` rehearsal
to `[]`, and the other 79 files under `out/mam-ws-bot/` came out byte-identical. `c42089e2` adds
`check-mpplus` after `parse-go`, raising on any error; on a spoiled scratch copy it named both
injected errors. `a153ccb5` adds `mam-simple-docs`, `search-final-hiriq-verse-text`,
`search-holam-he-qere`, `diffable-pointed-hebrew`, `ac-gen-index-flat-annotated` and
`pipeline-graph`; all 32 tracked files under their outputs are byte-identical. The mega has 60
steps. Suite: 988 passed, 5 skipped.

**Item 2, `py/main_diff.py ctr-vs-mam`, was not added, because it crashes.** The `_HANDLERS` table
in `py/diff_ctr_vs_mam/massage_mpu_verse.py` has no entry for the narrow-sense paseq template
מ:פסק, which Proverbs 8:34 has had in MAM-parsed since 2026-03-16 (`1880cbbd`), in place of the
legarmeh template מ:לגרמיה-2 it had before. The generator has failed on every snapshot since,
which is why its output was never regenerated. Phase 5c item 2 carries it.

The instructions as they were given for phase 5b:

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

## Phase 5c — the check-mpplus position, the ctr-vs-mam step, and argparse for the mega's hand-parsers: DONE, `7509c388`, `9fa80e11` and `577fb455`

`7509c388` moves `check-mpplus` after `foi-features-of-interest`, and changes no output.
`9fa80e11` gives the template מ:פסק a handler, U+05C0 and then a space, gives `py/main_diff.py` an
`almost_main(argv)`, and adds `diff-ctr-vs-mam` after `diff-mpp`. `out/diff_ctr_mam.json` changed
in exactly the five entries item 2 explains, in their `refined` field only, and still has 84
entries. `577fb455` gives the three hand-parsers argparse and an `almost_main(argv)`, and the mega
passes them `["all"]`, `[]` and `[]`; the 14 tracked files the three steps wrote are
byte-identical. The mega has 61 steps. Suite before each commit: 988 passed, 5 skipped.

The phase's report raised four more points, and each is disposed of here:

1. **The new order had a cost, and `18ded998` in phase 6a has fixed it.** A doc-note template with the
   wrong number of arguments now stops the run inside `foi-features-of-interest`, at the bare
   `assert wtp.template_len(tmpl) == 3` in `label_args_of_doc` (`py/foi/foi_wikitext_helpers.py`),
   before `check-mpplus` can name the template. A message on that assert naming the template and
   its argument count means a bad template is still named, while foi's report of malformed
   Unicode still comes first. The orchestrating session chose that over splitting
   `check-mpplus`'s two tests either side of `foi-features-of-interest`, which would add a step
   and no information. Ben, 2026-09-10: "That cost is acceptable to me, i.e. that decision is okay
   by me." Since `18ded998`, a three-argument נוסח template raises
   `doc-note template 'נוסח' has 3 argument(s), not 2:` followed by the template.
2. **`577fb455` changes behaviour on purpose.** Arguments the old code ignored now get argparse's
   usage error and exit status 2: a third positional argument to `py/main_clc.py` or
   `py/main_ac_gen_index_flat_annotated.py`, a chapter after `all` to `py/main_clc.py`, and
   anything but `--audit` to `py/main_find_uxlc_accent_changes.py`. So `main_clc.py all 5`, which
   used to build every pilot page, now exits 2. The documented forms are unchanged.
3. **Two stale docstrings have been fixed on the way.** `py/main_clc.py` named `gh-pages/clc/` for
   pages that are in `gh-pages/uxlc/clc/`, and `py/main_ac_gen_index_flat_annotated.py` gave its
   default paths relative to `aleppo/`. That program's `main()` also sets UTF-8 stdio now, since
   its new `--help` prints em dashes.
4. **§8 item 4 of the analysis had gone stale, and has been corrected** in the commit that records
   this phase: it listed "diff ctr-vs-mam" among the graph's nodes that are not steps.

The instructions as they were given for phase 5c, once Ben had answered both of its open questions
on 2026-09-10:

1. **Move `check-mpplus` after `foi-features-of-interest`.** Phase 5b put it straight after
   `parse-go`, as this plan said. But the mega runs `foi-features-of-interest` early precisely so
   that it reports malformed Unicode before a later step stops the run with an assertion that says
   less, as the comment above that step says, and `check-mpplus` at step 2 pre-empts that report.
2. **The `ctr-vs-mam` step, with a handler for מ:פסק.** Ben approved the fix on 2026-09-10: "Sure go
   ahead with the fix that adds support for מ:פסק." Phase 5b's candidate fix, tried in scratch only,
   maps the template מ:פסק to U+05C0 PASEQ followed by a space, as
   `py/accgram/printed_decalogue_fetch.py` does. With it the run gives 84 entries, as the committed
   file has, and Proverbs 8:34's entry comes out exactly as committed, the committed one having been
   made when that verse had the legarmeh template. The five entries that differ, at Psalms 2:7, 32:4
   and 32:5, differ only in their `refined` field: the committed file has `≁` and `~` where the
   current `py/mb_cmn/uni_heb.py` names U+0598 and U+05AE `(zarshit)` and `(zarnor)`, and those
   names were already in `d86e5779`, so the committed file was stale when it was committed. Add the
   handler to `_HANDLERS` in `py/diff_ctr_vs_mam/massage_mpu_verse.py`, add a `diff-ctr-vs-mam` step
   after `diff-mpp`, and commit the five-entry diff of `out/diff_ctr_mam.json` with that
   explanation. Any other diff is a finding to report, not to commit. The scratch evidence is in the
   worktree's `.novc/mega-coverage-phase5b/ctr/`.
3. **argparse for the three hand-parsers the mega runs.** `py/main_clc.py`,
   `py/main_find_uxlc_accent_changes.py` and `py/main_ac_gen_index_flat_annotated.py` read
   `sys.argv` by hand, and the mega gets their default mode only because it blanks `sys.argv`. Ben,
   2026-09-10, of `main_clc.py`: "It directly parses sys.argv? Gross." Give each argparse and an
   `almost_main(argv)`, and have the mega pass an explicit argument list, as it does for
   `main_accgram.py`'s subcommands. The other 20 hand-parsers, mostly the interactive Aleppo and
   Cambridge 1753 tools, stay as they are. Ben, 2026-09-10: "just leave the other 20 alone, but file
   a MAM-basics GitHub issue regarding their direct use of sys.argv". That issue is #269, which
   lists the 20.
4. Verify: the affected steps' outputs byte-identical, the ctr-vs-mam diff excepted as explained;
   the full suite.

## Phase 6 — delete the dead and redundant programs, and retire `check_ac_word_finding.py`: DONE, in sessions 6a and 6b

Ben agreed, 2026-09-10. The analysis's §6 has each with its evidence. **Run it as two sessions**,
for size. **6a** is items 1–9, the deletions of dead and redundant code, plus finding 1 of phase
5c's record. **6b** is items 10–17: the retirement of the word-finding check, the Stark CSV, the
runbook, the stale wording, the redundant PowerShell script, the second copy of
`lci_augrecs.json`, and two points from 6a's report. Each session ends with item 18's
verification, run over its own items.

**6a: DONE, `5295fdea`, `5f35dea3`, `625a00ef` and `18ded998`.** `5295fdea` deletes the
`__main__` blocks of items 1–3: those of the fifteen `py/accgram/` modules, of six `py/py_ac_loc/`
and five `py/py_cam1753_loc/` modules, and `ws_tmpl_parser`'s self-test. The seventh `py_ac_loc`
module, `kraken_seg_baselines.py`, went whole under item 4. `5f35dea3` deletes the five dead
programs of items 4–8, and four pieces of library code that had no caller once those programs were
gone: `py/hkq_cmn/verify_meteg_suggestions_vs_mgketer.py`; `py/hkq_cmn/mam_meteg_suggestions.py`,
a roster derived from the tracked MAM-suggestions JSON, which stays, as do the two Holman edit
specs in `in/mam-ws-bot-edits/`; `repo_hygiene.source_hygiene.run`; and
`codex_page.find_page_for_verse`. `625a00ef` deletes item 9's dead code. `18ded998` gives foi's
doc-note assert its message, finding 1 of phase 5c's record, and corrects the comment above the
`check-mpplus` step. The `foi-features-of-interest` step, rerun alone, left every tracked file
byte-identical, and the suite gave 988 passed, 5 skipped before each commit. The reference sweep
left only dated execution records: plans under `doc/`, among them
`doc/PLAN-holman-meteg-rollout-programme.md` and `doc/PLAN-post-stress-meteg-page-and-holman-m23.md`,
both of which say "State: executed 2026-09-04"; two review-findings files; and `CLAUDE.md`'s history
of the book-of-job move. The phase's report raised two more points, which items 16 and 17 carry
into 6b.

**6b: DONE, `26962cb4`, `7fa58d73`, `8fd9fb18`, `e820ca4e` and `15822344`.** `26962cb4` fixes
`py/check_ac_word_finding.py`'s column comparison, taking it from `PASS: 0`, `FAIL: 160` to
`PASS: 160`, and `7fa58d73` retires it, with its fixture and J David Stark's CSV. The "Aleppo
data" scope of `py/tests/test_h_dot_below_nfc.py` went from 18 files to 16, and its floor from 17
to 15. `8fd9fb18` corrects the runbook's `lenin_paths` bullet, with a dated correction beside the
2026-08-27 record, and the stale "sibling UXLC-utils" wording: the plan's four places, and three
more that the sweep found in `py/hkq_cmn/uxlc_atom_locations.py`'s module docstring and in
`py/hkq_cmn/uxlc_standard_atoms.py`. Of the files that the two rerun Holman steps wrote, only the
`note` lines of the two `holman/data/` JSON files changed. `e820ca4e` deletes `make-dph-files.ps1`
and the `uxlc/out/UXLC-misc/` copy of `lci_augrecs.json`, which `py/main_write_page_break_info.py`
no longer writes; the rerun step's three outputs were byte-identical, and the deleted copy did not
come back. `15822344` corrects `aleppo/doc/aleppo-line-breaks.md` to `270v 1of2`, and deletes all
nine unused names, none of which turned out to be used. The suite gave 988 passed, 5 skipped
before each commit. One more stale sentence came to light, and phase 8's item 1 carries it.

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
13. **The stale "sibling UXLC-utils" wording that phase 5a left in four places.** The `NOTE` and
    `STANDARD_ATOMS_NOTE` constants in `py/main_estimate_uxlc_locations.py` still say the UXLC XML
    is in "the sibling UXLC-utils", and both are written into the tracked
    `holman/data/uxlc_atom_locations.json` and `uxlc_standard_atoms.json`. Two error messages in
    `py/hkq_cmn/uxlc_atom_locations.py` still say the estimator needs the sibling clone, and so
    does `data_dir()`'s docstring in `py/hkq_paths.py`. Correct all four, then rerun the
    `estimate-uxlc-locations` and `render-uxlc-corrections` steps. The only diffs allowed are those
    note strings, in the two JSON files and anywhere the renderer carries them on.
14. **`misc/zarqa-table-diff/make-dph-files.ps1`.** It runs `py/main_diffable_pointed_hebrew.py`
    over the two zarqa tables beside it, and those two pairs are among the four in that module's
    `TRACKED_EXPANSIONS`, which the mega's `diffable-pointed-hebrew` step has regenerated since
    phase 5b. Delete the script, and reword the comment above `TRACKED_EXPANSIONS`, the only live
    text that names it. `doc/PLAN-evacuate-the-codex-index-trio-and-diffable-pointed-hebrew.md`
    names it in an execution record, which stays as written, as does this plan's phase 5b record.
15. **Keep one copy of `lci_augrecs.json`, the one in `uxlc/data/`.** Ben, 2026-09-10: "just
    choose one and delete the other. I think the idea is some external client might want to use it
    in a way unlike the estimator program (or programs) work, i.e. instead of forming augrecs on
    the fly they might want them pre-formed." `py/main_write_page_break_info.py`, which the mega
    runs as `uxlc-write-page-break-info`, writes the same flattened records to
    `uxlc/out/UXLC-misc/lci_augrecs.json` and to `uxlc/data/lci_augrecs.json`, and nothing in the
    repository reads either: `py/main_estimate_uxlc_locations.py` and
    `py/main_uxlc_estimate_atom_loc.py` build the augmented records in memory from
    `in/lci_recs.json` and `in/UXLC-39/`. The `uxlc/data/` copy stays, because it is the copy that
    `uxlc/doc/clc-design.md`, `doc/scan-pages.md`, `DATA-LICENSES.md` and a comment in
    `in/vendoring_policy.json` name, while the other is named only by its writer and by the step's
    note. Of the other path Ben said, the same day, that it "seems a little worse to me because
    this is nobody's output (not any more at least) yet there is 'out' in the path". So:
    - stop writing the `uxlc/out/UXLC-misc/` copy, and `git rm` it;
    - correct the `uxlc-write-page-break-info` step's note in `py/main_0_mega.py`;
    - reword `uxlc_paths.data_dir()`'s docstring, which says "Generated UXLC data other repos
      consume", to give the purpose Ben gave: the augmented records pre-formed, for a client that
      wants them that way rather than built on the fly as the two estimators build them.

    Rerun the step: `uxlc/data/lci_augrecs.json`, `uxlc/out/UXLC-misc/page_counts.json` and
    `uxlc/out/UXLC-misc/lci_recs.xml` must come out byte-identical, and the deleted copy must not
    come back: `git status --porcelain` must not list `uxlc/out/UXLC-misc/lci_augrecs.json` as
    untracked.
16. **`aleppo/doc/aleppo-line-breaks.md` still documents `270v 1`**, which `main()` in
    `py/py_ac_loc/gen_line_break_editor.py` rejects. `5295fdea` corrected that module's docstring
    to the NofM form, `270v 1of2`, which is half of the analysis's §8 finding 8. Correct the doc the
    same way. The other half, the `--status` and `--batch` that
    `py/main_gen_cam1753_crop_editor.py` documents and lacks, is recorded in #269 and stays out of
    this plan.
17. **Nine pieces of code that phase 6a found unused, all of them unused before it began:**
    `gen_html_file`, `_post_stress` and `_book_name` in `py/author_site/post_stress_meteg.py`;
    `image_relpath` and `_leaf_to_page_n` in `py/py_ac_word_image_helper/codex_page.py`;
    `_KOREN_PAGE` in `py/accgram/printed_decalogue_page.py`; `_occurrence` in
    `py/accgram/maqaf_nonfinal_accents_page.py`; `write_stream` in `py/py_ac_loc/gen_flat_stream.py`;
    and `IMG_DIR` in `py/py_cam1753_loc/gen_line_break_editor.py`. Delete each after confirming, as
    item 9 did, that nothing calls or reads it. Keep any that turns out to be used, and report it.
18. Verify: the reference sweep for every deleted name, the full suite.

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
   `py/main_clc.py` is one: the mega runs its `all` mode, so its per-book mode is declared by hand.
4. **Failures:** a program neither run nor declared; a declaration whose program is gone; a
   declaration whose program the mega now runs.
5. Name the check in `py/main_repo_maintenance.py`'s docstring, whose step 5 runs the suite before
   step 6 runs the mega, and correct that docstring's stale list of mega steps. Also correct the
   two docstrings that give `tmpl-survey`'s position among the mega's steps:
   `py/mb_cmn/graphviz_pin.py`'s says "step 5 of 41", and `py/tmpl_survey/survey_dot.py`'s says
   "step 5 of its 41" and "the remaining 36 steps". Every phase since phase 2 has added steps, and
   `check-mpplus` now runs before `tmpl-survey`, so neither figure is right any more. Name the step
   by its id and state no position or count, since any figure goes stale with the next step added.
   Grep for any other stated step position or count.
6. Verify: the full suite green; then, uncommitted, delete one declaration and see the check fail
   naming that program, and restore it.

## Phase 8 — full verification

1. **Correct the last "sibling UXLC-utils" sentence, which phase 6b found.**
   `py/hkq_cmn/uxlc_change_records.py`'s module docstring says that Gen 14:17.9, Ex 5:22.11 and
   2Sam 3:30.10 "are the instances in the change files on disk in the sibling UXLC-utils". Find
   where those change files are now, confirm that the same three instances are the ones there, or
   report the difference, and name the path in the sentence. Commit this before item 2's run, so
   that the run verifies the finished tree.
2. From a throwaway script, run every step of `_STEPS` except `near-aleppo-census`, in order, with
   nothing exported.
3. `git status` must be clean. Any diff is explained and committed on its own, or reported.
4. Run the full suite.
5. Update `doc/mega-coverage-2026-09-10.md` with a closing record of what the mega now runs, which
   also retires its §3 and §5 rows for the post-stress-meteg survey, and report the branch head for
   the orchestrating session to integrate.

## Not in this plan, raised for Ben

1. The incidental findings of the analysis's §8, except those a phase above fixes on its way past.
2. **Two UXLC library packages hold near-copies of the same modules**, found on 2026-09-10 while
   tracing `lci_augrecs.json`. `py/py_uxlc/my_uxlc_page_break_info.py` and
   `py/uxlc_misc/my_uxlc_page_break_info.py` differ in 4 lines of each file, `my_uxlc_location.py`
   in those two packages in 6, and `py/py_uxlc/my_uxlc_lci_augrec.py` and
   `py/uxlc_lci/uxlc_lci_augrec.py` in 4, by `git diff --no-index --stat`. Seventeen files import
   `py_uxlc`, and `py/main_write_page_break_info.py` imports `uxlc_misc` and `uxlc_lci`. They are
   library modules rather than programs, so they are outside this plan's scope. Nobody has yet
   checked which set should remain.
