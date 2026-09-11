# What `py/main_0_mega.py` runs, and why everything else does not run there

Written by a Claude session on 2026-09-10. Ben's instructions that day were: "An analysis of what
is and isn't part of mega should be made", "Everything that is not part of mega should have a
recorded justification as to why it is not in mega", and "It should be part of repo maintenance
(if it is not already) to check that the only programs not part of mega are those that have
documented justifications for why they are not part of mega." Of the post-stress-meteg survey he
also said: "If it is not part of mega, it should be!" Everything else here is that session's
analysis.

**Measured against** `main` at `a2e883f1` (2026-09-10 12:04), in the worktree branch
`claude/mega-coverage`. That branch's first commit, `3a1ab7f0`, is the one code change made so far:
the post-stress-meteg page renderer now raises instead of looking a spelling up in MAM-private.
**Re-measure before relying on a row**; the tree moves. Rows for the programs that phase 3 of
`doc/PLAN-mega-coverage.md` removed on 2026-09-10 say so where they stand: the two Wikisource
index generators and the Aleppo column-coordinate plots in §5, and `py/main_download.py
fr-sefaria` in §3 and in §5's third gap.

**§9 is the closing record, 2026-09-10**, of what the mega runs once `doc/PLAN-mega-coverage.md` had
been carried out, and of what became of each recommendation here. The sections before it are the
analysis as it was measured. Dated notes mark, where they stand, the sentences and rows that the
plan's phases made false; where a sentence below has gone stale without one, §9 is the later word.

**Method.** A *program* here is a tracked `.py` with an `if __name__ == "__main__":` block outside
`py/tests/`, plus the four example scripts the mega runs as subprocesses. An entry point's argparse
subcommands are programs of their own, and so is a flag-selected mode when the mega runs one mode
and not another. Six read-only sub-agents read the source of every program (none ran one) and
reported whether a step of `_STEPS` runs it, what it writes (tracked or not, by `git ls-files`),
what it reaches outside the repository, and any reason for leaving it out that is already written
down. The session re-checked the claims that §1's decisions rest on, and corrected one inventory:
`parse-go` calls `main_authored.cmd_gen_mam_parsed_docs(None)`, so the MAM-parsed documents,
`doc/mp-claims.md` and the MAM-parsed claim verification all run in the mega, which that inventory
had reported as not.

**Correction, 2026-09-10: `parse-ws`, not `parse-go`, is the step that runs `gen-mam-parsed-docs`.**
The sentence above was true at `a2e883f1`. `426fa229`, a Codex session's cutover of MAM-parsed to
Wikisource, which phase 7b of `doc/PLAN-mega-coverage.md` merged in `8f5c1c96`, made
`parse_go.almost_main` write only `MAM-parsed/google/`. `parse_ws.almost_main`, which the `parse-ws`
step runs, now calls `main_authored.cmd_gen_mam_parsed_docs(None)` through
`parse_ws_products.generate_production`, so the MAM-parsed documents, `doc/mp-claims.md` and the
claim verification still run on every mega run, in that step. Row 1 of §2's table has the same
correction.

## 1. Decisions for Ben, with recommendations

**Ben answered all six on 2026-09-10**, and `doc/PLAN-mega-coverage.md` carries the answers out:

1. The survey joins the mega, on two conditions: in a worktree it looks for MAM-private "next to the
   worktree's 'home clone'" rather than relying on `REPOS_ROOT`, and in the cloud "it skips the MAS
   survey altogether".
2. Fold `py/main_uxlc_mega.py` into the mega: agreed.
3. Add the other offline generators: agreed. The three gaps after §5's table were not part of the
   answer and stay open.
4. The four judgment calls:
   - (a) The two Wikisource index generators "were one-off programs generating wikitext to get a
     human started, and will never be run again": remove them and their outputs.
   - (b) The column-coordinate plots "were one-time experiments": remove them.
   - (c) The line-break reports stay out of the mega. The fine-grained indexing "served its purpose
     for the book-of-job project".
   - (d) The slide thumbnails stay out of the mega.
5. Delete the dead and redundant programs: agreed. `py/check_ac_word_finding.py`, which the
   recommendation left to Ben, is still open.
6. Build the check: agreed.

The recommendations as they were put to Ben:

1. **Put the post-stress-meteg survey in the mega?** Recommended: yes, as a step before `gen-site`.
   The cost is that the mega would need MAM-private for good, not only until the near-Aleppo census
   leaves it. That is the opposite direction from the vendoring decision of 2026-09-04, recorded in
   `in/vendoring_policy.json`: "The lack of vendoring audit of MAM-private is a cost worth the
   benefit of decoupling MAM-basics from MAM-private." The survey's input lags MAM, because
   al-hatorah's pipeline in MAM-private regenerates it from MAM-parsed, and that lag was accepted on
   2026-09-04 ("I can tolerate that staleness", `doc/PLAN-holman-meteg-rollout-programme.md`). Since
   `3a1ab7f0` the survey build is the only post-stress-meteg code that reads MAM-private, and it
   reads it unconditionally.
2. **Fold `py/main_uxlc_mega.py` into the mega.** Recommended: yes. §5's first row has the reasons
   and the ordering.
3. **Add the other offline generators that §5 marks "add", and close the three gaps listed after
   §5's table.** Recommended: yes, each in the position its row gives.
4. **Four judgment calls from §5**: (a) the two Wikisource index generators, regenerate or freeze;
   (b) the Aleppo column-coordinate plots, frozen like the Cambridge 1753 gutter chart; (c) the two
   line-break reports, the Aleppo one of which currently fails; (d) the slide thumbnails.
5. **Delete the dead and redundant programs in §6.** Recommended: yes, except
   `py/check_ac_word_finding.py`, whose failure was recorded as deliberately unfixed and so is Ben's
   to settle.
6. **Build the check in §7.** Recommended: yes, after 1–5, so that its declaration starts from
   decisions rather than from placeholders.

## 2. What the mega runs: its 41 steps

| # | Step | Program it runs |
|---|---|---|
| 1 | `parse-go` | `py/main_parse.py go`, which also regenerates the MAM-parsed documents and `doc/mp-claims.md` and runs the claim verification, through `main_authored.cmd_gen_mam_parsed_docs`. **Stale since `426fa229`; see the correction below this table.** |
| 2 | `foi-features-of-interest` | `py/main_foi_features_of_interest.py` |
| 3 | `mam-with-doc` | `py/main_mam_with_doc.py` |
| 4 | `diff-mpp` | `py/main_diff.py mpp --all` |
| 5 | `tmpl-survey` | `py/main_tmpl_survey.py` |
| 6 | `tmpl-survey-toy` | `py/main_tmpl_survey_toy.py` |
| 7 | `vendored-tmpl-survey-toy` | `MAM-parsed/py-examples/main_tmpl_survey_toy_example.py`, as a subprocess |
| 8 | `mam-simple` | `py/main_mam_simple.py core-only`: the export and the support-file copy, **not** the doc half (§5) |
| 9 | `mam4sef-and-ajf` | `py/main_mam4sef.py --both-sef-and-ajf` |
| 10 | `mam-osis` | `py/main_mam_osis.py` |
| 11 | `letter-small-job` | `py/main_letter_small_job.py` |
| 12 | `vendored-letter-small-job` | `MAM-simple/py-examples/main_letter_small_job_example.py`, as a subprocess |
| 13 | `vendored-mam4sef` | `MAM-simple/py-examples/main_mam4sef_example.py`, as a subprocess |
| 14 | `vendored-mam-osis` | `MAM-simple/py-examples/main_mam_osis_example.py`, as a subprocess |
| 15 | `decnreub` | `py/main_decnreub.py` |
| 16 | `multimark` | `py/main_multimark.py` |
| 17 | `wordlist` | `py/main_wordlist.py` |
| 18 | `explicit-xataf` | `py/main_explicit_xataf.py` |
| 19 | `diff-wsgo` | `py/main_diff.py wsgo` |
| 20 | `parse-ws` | `py/main_parse.py ws` |
| 21 | `ws-bot-proto` | `py/main_ws_bot.py proto`, without `--edits` |
| 22 | `gen-misc-authored-english-documents` | `py/main_authored.py gen-misc`, **not** `py/main_gen_misc_authored_english_documents.py` despite the name (§5) |
| 23 | `wlc-json-and-unicode` | `py/main_wlc_json_and_unicode.py` |
| 24–33 | the ten `accgram-*` steps | `py/main_accgram.py` `run-prose`, `test-fixes`, `run-dual-cant`, `run-poetic`, `xcheck-poetic`, `servi-xcheck`, `grammaticality`, `run-printed-decalogue`, `survey-chanted-word-accents` and `generate-html --trust-survey` |
| 34 | `find-uxlc-accent-changes` | `py/main_find_uxlc_accent_changes.py`, default mode |
| 35 | `uxlc-grammar-test` | `py/main_uxlc_grammar_test.py` |
| 36 | `wlc-diffs-420422` | `py/main_wlc_diffs_420422.py` |
| 37 | `wlc-a-notes` | `py/main_wlc_a_notes.py` |
| 38 | `sigil-inventory` | `py/main_sigil_inventory.py` |
| 39 | `near-aleppo-census` | MAM-private's `near-aleppo/census/run_all.py --write`, as a subprocess |
| 40 | `gen-site` | `py/main_authored.py gen-site --trust-surveys` |
| 41 | `vendoring-audit` | `py/main_vendoring.py --all` |

**Correction, 2026-09-10, to row 1.** Since `426fa229`, a Codex session's cutover of MAM-parsed to
Wikisource, which phase 7b of `doc/PLAN-mega-coverage.md` merged in `8f5c1c96`, `parse-go` writes
only `MAM-parsed/google/`, and it is the `parse-ws` step, row 20 here, that runs
`gen-mam-parsed-docs`, as the correction under the Method paragraph says. The mega now runs
`parse-ws` first; §9 has its steps as they are now.

## 3. Left out of the mega, with the reason already written down

| Program | Why it is left out | Where that is written |
|---|---|---|
| `py/main_accgram.py survey-post-stress-meteg`, and `py/main_authored.py gen-site` without `--trust-surveys`, which rebuilds the same survey | reads MAM-private's Phonetic MAM; the mega renders the pages from the tracked JSON instead | `py/main_0_mega.py`, the comment in `_run_gen_site`; `py/main_authored.py`, the comment above `_SURVEY_READING_PAGES`; commit `deb80472`. **Decision 1**. **Retired on 2026-09-10**: since phase 2 of `doc/PLAN-mega-coverage.md` (`9657a081`), the survey is the mega step `accgram-survey-post-stress-meteg`, which a cloud session skips. `gen-site` without `--trust-surveys` stays out, now because it would rebuild the survey that step has just written (§9) |
| `py/main_accgram.py survey-breuer-zaqef-units` | a measurement written only to `.novc/`; it also reads MAM-private | `py/accgram/breuer_word_length.py` docstring, "WRITES TO .novc/, not to out/" |
| `py/main_accgram.py vendor-printed-decalogue` and `vendor-ctr-decalogue` | network: they refresh vendored snapshots from Wikisource and chabad.org | `py/main_accgram.py` docstring, "NETWORK AUTHOR TOOL, run by hand" |
| `py/main_accgram.py generate-html` without `--trust-survey`, and its fourteen `generate-html-<name>` singles | the `accgram-generate-html` step runs the same batch | `doc/review-findings-2026-08-03.md`, "What is left outside the mega on purpose" |
| `py/main_accgram.py generate-html-wlc-chanted-word-residue` without `--trust-survey` | the same page with its survey rebuilt | `py/accgram/wlc_chanted_word_residue_page.py` docstring |
| `py/main_edition_transcription.py` `scan-page`, `editor`, `zoom-line`, `build` with `--export`, and `highlight-picker` | interactive, and read a personal scan archive outside every repository | the entry point's docstring, "The interactive, machine-local half of the printed-Decalogue work" |
| `py/main_edition_transcription.py` `check` and `build --check` | checks that write nothing | the entry point's docstring; `py/accgram/transcription_build.py`, which names `py/tests/test_edition_transcriptions.py` as the check over every stem |
| `py/main_edition_transcription.py build --derive-only` | re-derives each stem's tracked `.txt` from its tracked JSON, and the suite already fails on any drift between the two | `py/accgram/transcription_build.py` docstring |
| `py/main_verify_meteg_vs_mgketer.py` | a one-time check of Holman's meteg suggestions against MAM-private's mgketer | its docstring, quoting Ben's decision of 2026-09-03: "run it once as a one-time check". Also in §6 |
| `py/main_diff.py mpp --legacy-history` | reads a sibling MAM-parsed clone that belongs on no machine | `py/subcommands/diff_mpp.py` docstring; `CLAUDE.md` |
| `py/main_download.py` `fr-google`, `fr-google --download-only`, `fr-wikisource` and `fr-ws-intro` | network downloads, run when the upstream moves. A fifth, `fr-sefaria`, was removed on 2026-09-10 with the directory it wrote (§5's third gap) | `doc/process-documentation/pipeline.dot`, "External prerequisites (not part of _STEPS)"; the closing comment of `py/main_0_mega.py`; `CLAUDE.md` for `fr-ws-intro` |
| `py/main_ws_bot.py real --no-save` | reads live Wikisource pages through the bot's login | `doc/PLAN-holman-meteg-rollout-programme.md` |
| `py/main_ws_bot.py proto --edits <file>` | a rehearsal of one edit file before a real save | the same plan |
| `py/main_ws_bot.py holman-meteg-spec`, with and without `--write` | a one-shot check designed to stop passing | `py/ws/holman_meteg_edit_spec.py`, "THIS CHECK IS ONE-SHOT, AND IS MEANT TO STOP PASSING". Also in §6 |
| `py/main_slide_generator.py render-slides` | needs Playwright with headless Chromium, and the Windows font directory | `misc/what-is-mam/img/provenance-misc.md`, for the what-is-mam deck only |
| `py/main_uxlc_download_changes.py` | network: downloads UXLC from tanach.us | `py/main_clc_download_notes.py` docstring, which names it as the network half of the UXLC build |
| `py/main_clc.py <BookId> [chapter]` | one book or chapter, for focused work | its docstring |
| `py/main_clc_download_notes.py` | network, and "NOT part of the default build" | its docstring |
| `py/main_ingest_uxlc_emails.py` and `py/main_ingest_mam_suggestions.py` | read Holman's untracked mailboxes under `.novc/`; the reports regenerate from the tracked derivatives | `doc/PLAN-evacuate-the-rest-of-three-repos.md`, "neither is needed to regenerate" |
| `py/main_verify_notes_zip.py` | a verification aid against a downloaded zip outside every repository | its docstring |
| `py/main_ac_find_word_in_images.py`, `main_ac_gen_col_quad_editor.py`, `main_ac_gen_lb_flat_stream.py` and `main_ac_gen_line_break_editor.py` | interactive hand work on the Aleppo page images | `py/ac_paths.py`; `aleppo/README.md`; `aleppo/doc/aleppo-line-breaks.md` |
| `py/main_ac_download_pages.py` and `py/main_cam1753_download_spreads.py` | network downloads of page images from archive.org | their docstrings |
| `py/main_cam1753_find_word_in_images.py`, `main_cam1753_gen_col_quad_editor.py`, `main_cam1753_gen_flat_stream.py`, `main_cam1753_gen_line_break_editor.py`, `main_gen_cam1753_crop_editor.py` and `main_apply_cam1753_crops.py` | interactive hand work on the Cambridge 1753 images | `cam1753/doc/cam1753-line-break-task.md`; `py/cam1753_paths.py`; `doc/boj-cam1753-word-crops.md`; `doc/book-of-job-artifacts.md` |
| `py/main_cam1753_gutter_profile.py` | matplotlib versions make the chart non-reproducible | `cam1753/CLAUDE.md` |
| `py/main_cam1753_split_spreads.py` | regenerates untracked page JPEGs when an editor needs them; its tracked split records do not move | Ben's decision of 2026-09-04, in `doc/PLAN-evacuate-the-codex-index-trio-and-diffable-pointed-hebrew.md` |
| `py/main_list_missing_aleppo_imgs.py` | a console report only | `doc/book-of-job-artifacts.md` |
| `py/check_ac_all.py`, `py/check_cam1753_all.py` and `py/check_cam1753_word_finding.py` | per-manuscript checks | `cam1753/CLAUDE.md`; `doc/PLAN-evacuate-public-repos-programme.md` |
| `py/main_test.py` | the suite, which MAM-basics' maintenance runs just before the mega | `py/main_repo_maintenance.py` docstring |
| `py/main_repo_util.py`, all six actions | cross-repository maintenance; `--commit-across-repos` is barred from the sweep | `doc/PLAN-repo-maintenance-across-GitRepos.md` |
| `py/main_repo_maintenance.py` | MAM-basics' maintenance, whose last step runs the mega | its docstring |
| `py/main_redirect_stubs.py` `build`, `build --publish` and `check` | frozen redirect stubs; publishing needs a temporary clone of a redirect host | `CLAUDE.md`, "Nothing schedules the program" |
| `py/check_mark_order.py` | a source check over file types the suite's lint does not cover | `CLAUDE.md` |
| `py/fix_escape_sequences.py`, as a dry run and with `--apply` | the fixer that `py/check_escape_sequences.py` points to | `py/check_escape_sequences.py`, "Run fix_escape_sequences.py to replace these" |

## 4. Left out, no reason written down, and plainly not mega work

The reasons in this table are Claude-written proposals for Ben to accept or change.
**On 2026-09-10 Ben accepted every one of them that `py/tests/test_mega_coverage.py` took in**;
§9 says which rows were settled another way.

| Program | Proposed reason |
|---|---|
| `py/main_find_uxlc_accent_changes.py --audit` | prints coverage counts and writes nothing |
| `py/main_scan_pages.py survey` | reads the personal scan archive, which is on no other machine, so it is re-run by hand when a scan folder changes |
| `py/main_scan_pages.py check` | writes nothing; `py/tests/test_scan_pages_index.py` runs the same check |
| `py/main_parse.py ws --write-fmt-1` | debugging output to `.novc/`; the tracked half of the run is `parse-ws`'s |
| `py/main_diff.py mpp --old A --new B` | a one-off comparison of two revisions someone picks; `diff-mpp` already rebuilds every named release |
| `py/main_download.py fr-google --skip-download` | `parse-go` plus a read-only `check_mpplus`; but see the second gap after §5's table. **Correction, 2026-09-10**: since `426fa229`, a Codex session's cutover of MAM-parsed to Wikisource, which phase 7b of `doc/PLAN-mega-coverage.md` merged in `8f5c1c96`, this form runs only `parse_go.almost_main`, the parse that the `parse-go` step runs, and `check_mpplus` runs inside the `parse-ws` step instead |
| `py/main_ws_bot.py real` | saves edits to live Hebrew Wikisource under Ben's bot account, so every run is a deliberate act |
| `py/main_ws_bot.py real --identity-run` | exercises the live-wiki plumbing, and needs the network and the bot login |
| `py/main_tmpl_survey.py --write-expanded-stack-grammar-lock` | the locks are what every survey run is checked against, so rewriting them on every run would make that check pass by construction |
| `py/main_tmpl_survey.py --find-stack-path` | a lookup that prints and writes nothing |
| `py/main_foi_features_of_interest.py --foi <name>` and `--single-threaded` | a subset, or a debugging variant, of the step's full run |
| `py/main_vendoring.py --compare`, `--provenance` and `--gen-inventory` | parts of the `--all` audit the step runs |
| `py/main_slide_generator.py make-pptx` | builds an untracked presentation file for giving a talk |
| `py/main_uxlc_estimate_atom_loc.py` | a lookup that prints one estimated folio, column and line |
| `py/main_just_render_table.py --update-issue-metadata` | refreshes a snapshot of the live GitHub tracker through `gh` |
| `py/check_qr_relations.py`, `check_qr_consistency.py`, `check_html_syntax_and_sanity.py`, `check_escape_sequences.py` and `check_function_ordering.py` | checks that write nothing; `py/check_all.py` runs them by hand, and the suite runs the deploy-root mode of `check_html_syntax_and_sanity.py` |
| `py/main_ac_gen_flat_stream.py` | seeds one page from a hand-chosen verse range, and refuses to overwrite |
| `py/main_ac_merge_line_markers.py` | merges line markers from a hand edit, so it has no input until a person edits a page |
| `py/main_source_hygiene.py` | the suite runs the same scan. Also in §6 |
| the `__main__` block of `py/accgram/ctr_decalogue.py` | prints a comparison of two committed files; `py/tests/test_ctr_decalogue.py` pins what it finds. Also in §6 |

## 5. Candidates: tracked output from tracked input, and no reason written down

| Program | Tracked output | Notes | Recommendation |
|---|---|---|---|
| `py/main_uxlc_mega.py` and its five steps: `main_uxlc_check_changes`, `main_fois`, `main_write_page_break_info`, `main_amb_early_mtg` and `main_uxlc_word_list` | `in/UXLC-misc/all_changes.json`; files under `uxlc/out/` and `uxlc/data/`; `gh-pages/uxlc/fois/`; `gh-pages/uxlc/amb-early-mtg/`. Over 30 files | A second orchestrator: UXLC-utils' mega, renamed on arrival. Its docstring's reason for standing apart, "the sibling UXLC-utils'" trees, stopped being true when `uxlc/` landed here. The `find-uxlc-accent-changes` step consumes `all_changes.json`, which nothing in the mega rebuilds. Its only caller is the default mode of `py/main_uxlc_download_changes.py` | Fold the five steps into `_STEPS`, as the wlc half was on 2026-08-01, with `main_uxlc_check_changes` before `find-uxlc-accent-changes`. Make the download program download only, and delete `py/main_uxlc_mega.py`. **Decision 2** |
| `py/main_clc.py all` | 12 files under `gh-pages/uxlc/clc/` | offline and deterministic by design: `uxlc/doc/clc-design.md` says "the build never touches the network" | add |
| `py/main_estimate_uxlc_locations.py`, then `py/main_render_uxlc_corrections.py` | `holman/data/uxlc_atom_locations.json`, `uxlc_standard_atoms.json`; `gh-pages/holman/uxlc_corrections.*`; `holman/docs-not-served/uxlc_corrections.json` | The estimator's docstring gives a stale reason: UXLC XML "this repo does not track", when `in/UXLC-39` is tracked now. The renderer's docstring argues for inclusion: "Reads only what is tracked" | add both, in that order |
| `py/main_verify_and_render_table.py` | the summary in `holman/docs-not-served/table_data.json`; `gh-pages/holman/table_data_findings*` | the documented verifier-renderer, which raises on a verification failure. `py/main_just_render_table.py`'s default mode is its render-only subset and becomes covered by it | add |
| `py/main_map_changes_to_book_of_job.py` | `uxlc/in/UXLC-misc/2026.04.01-map-to-book-of-job.json` | a generated file in an input tree; it reads book-of-job's generated pages | add, after the book-of-job generator |
| `py/main_gen_misc_authored_english_documents.py` | 183 files under `gh-pages/book-of-job/` and `book-of-job/out/` | This is book-of-job's site generator. The mega step named `gen-misc-authored-english-documents` has run `main_authored.almost_main` instead since `3e3b6e0b` (2026-05-06), and book-of-job's generator arrived later under the old name. So the sentence in `doc/PLAN-evacuate-the-rest-of-three-repos.md` "book-of-job's oracle is the one that is also a mega step" is false. The generator ends in a spell check that calls `exit(1)` on any finding | Add it, deciding whether a spelling finding should fail the mega. Rename the step or the file so that the two stop sharing a name |
| `py/main_mam_simple.py doc-only` | `MAM-simple/doc/versification-differences.md`; `gh-pages/MAM-simple/versification-and-cantillation.*`; `gh-pages/MAM-simple/index.html` | the `mam-simple` step calls `almost_main`, which never runs `_write_generated_docs`; these pages have gone stale once | run the doc half in the `mam-simple` step |
| `py/main_diff.py ctr-vs-mam` | `out/diff_ctr_mam.json` | The inventory found the output's only commit is `d86e5779` (2026-03-09), though its generator and its MAM-parsed input have changed since. `py/pipeline_graph/pipeline_graph_spec.py` already draws it as a pipeline step | add, expecting a first-run diff |
| `py/main_search_final_hiriq_verse_text.py` and `py/main_search_holam_he_qere.py` | `holman/out/final_hiriq_verse_text_report.json`, `holam_he_qere_report.json` | Holman reports from the corpus; the second reads the `wordlist` step's output | add, after `wordlist` |
| `py/main_pipeline_graph.py` | `doc/process-documentation/pipeline.dot`, `pipeline.svg`, `MAM-process.dot.svg` | its one tool, Graphviz, is one the mega already needs; its hand-maintained spec has drifted from `_STEPS` (§8) | add |
| `py/main_diffable_pointed_hebrew.py` | the `diffable-pointed-hebrew/*sample-output.json` samples and `misc/zarqa-table-diff/*.dph.txt` | input and output are positional, so a step names four fixed pairs; `diffable-pointed-hebrew/README.md` calls the samples "the differential artifacts for the command" | add, with the four pairs |
| `py/main_ac_gen_index_flat_annotated.py` | `aleppo/index-flat-annotated.json` | a deterministic transform of a tracked, hand-corrected file; it once stayed broken for five months without anyone noticing | add |
| `py/main_lenin_wikisource_page.py` and `py/main_ac_wikisource_page.py` | `leningrad/lenin-wiki/`; `aleppo/aleppo-wiki/index-flat.json`, `index-grouped-by-book.json`, `index.wiki` | Deterministic from tracked input. The recorded sentence, "a starting point for manual work … never intended to stay in sync", is about the live Wikisource page, not about regenerating these files | **Decision 4a**: add both, or record both as frozen. Ben chose neither: **removed on 2026-09-10**, with their outputs, by phase 3 of `doc/PLAN-mega-coverage.md` |
| `py/main_ac_plot_col_coords.py` | `aleppo/plot_col_coords-out/*.png` | matplotlib output; the Cambridge 1753 gutter chart is kept frozen for exactly that reason | **Decision 4b**: record as frozen, like the gutter chart. Ben chose otherwise: **removed on 2026-09-10**, with its PNGs, by phase 3 of `doc/PLAN-mega-coverage.md` |
| `py/main_ac_check_line_breaks.py` and `py/main_cam1753_check_line_breaks.py` | `aleppo/check_line_breaks.html`, `cam1753/check_line_breaks.html` | Reports that check the hand-annotated line breaks against MAM-simple's XML, which the mega rewrites. The Cambridge 1753 report says "All checks passed". The Aleppo report says "91 issue(s) found", and that program exits 1 | **Decision 4c**: add the Cambridge 1753 one; the Aleppo one would fail the mega until its 91 issues are dealt with |
| `py/main_slide_generator.py make-thumbs` | `misc/<deck>/img/thumb-*.png` | thumbnails of slides that `render-slides` makes by hand, with Playwright | **Decision 4d**: record it as left out along with `render-slides` |
| `py/main_accgram.py survey-post-stress-meteg` | `out/accgram/post-stress-meteg.json` | reads MAM-private; §3 has the recorded reason. A fresh run into a scratch file on 2026-09-10 was byte-identical to the tracked JSON | **Decision 1**. Ben chose yes: **added on 2026-09-10**, as the step `accgram-survey-post-stress-meteg` immediately before `gen-site`, by phase 2 of `doc/PLAN-mega-coverage.md` (`9657a081`), once phase 1 (`516a4a1a`) let a worktree run find MAM-private beside its home clone. A cloud session skips it |

Three gaps inside steps the mega already runs:

1. **`ws-bot-proto` never rewrites the tracked `out/mam-ws-bot/proto-misc/warnings.json`.** Without
   `--edits`, the edits context `no_edits()` returns has no `get-warnings` key, so `write_warnings`
   returns early. The inventory found the file was last written by a `proto --edits` rehearsal,
   `52aa7b8c` (2026-08-27).
   **Fixed on 2026-09-10** by `2e3a7189`, in phase 5b of `doc/PLAN-mega-coverage.md`: every proto
   run writes the file, `[]` when there are no edits.
2. **`check_mpplus`, a read-only check of the parsed data, runs only inside
   `py/main_download.py fr-google`**, so only after a Google download.
   **Closed on 2026-09-10**: since `426fa229`, `check_mpplus` runs inside the `parse-ws` step, over
   every plus book it writes, and raises on any error. Phases 5b and 5c of
   `doc/PLAN-mega-coverage.md` had given the check a step of its own, `check-mpplus`; Ben's decision
   of the same day kept it inside `parse-ws`, and phase 7b dropped the step.
3. **Nothing reads `in/mam-from-sefaria/`**, which `py/main_download.py fr-sefaria` wrote.
   **Removed on 2026-09-10**, the directory and the subcommand both, by phase 3 of
   `doc/PLAN-mega-coverage.md`: Ben was "no longer interested in tracking what sefaria does with
   what we give them".

## 6. Dead or redundant programs

| Program | What is wrong | Recommendation |
|---|---|---|
| the `__main__` blocks of fifteen library modules under `py/accgram/`: `telg_doc_notes`, `printed_decalogue_page`, `maqaf_nonfinal_accents_page`, `printed_decalogue`, `wlc_chanted_word_residue_page`, `supplied_marks`, `ps17v14_doc_notes`, `ps17v14_double_tsinnor`, `printed_decalogue_uvinkha_page`, `printed_decalogue_simanim_page`, `printed_decalogue_koren_page`, `dual_under_bars_page`, `dual_cant_run`, `ctr_decalogue` and `almost_errors` | each duplicates a `py/main_accgram.py` subcommand, except `ctr_decalogue`, which only prints (§4). They are second entry points of the kind the one-entry-point rule forbids | delete the blocks |
| the `__main__` blocks of eight modules under `py/py_ac_loc/` and five under `py/py_cam1753_loc/` | each duplicates a `main_ac_*` or `main_cam1753_*` wrapper, and fails on an import when run directly | delete the blocks |
| the `__main__` self-test of `py/ws/ws_tmpl_parser.py` | By reading, it fails on its first case: it expects a `{"tmpl": …}` shape that `mktmpl` has not produced since at least 2026-03-09. Not run | delete the block |
| `py/main_ac_kraken_seg_baselines.py`, with the command line in `py/py_ac_loc/kraken_seg_baselines.py` | Imports a `main` its module does not define. kraken is in no venv on this machine, and the module reads column-coordinate keys that no data file has | delete |
| `py/main_gen_aleppo_crop_editor.py` | raises `TypeError` on every page, because `image_size` is a list; all 160 Aleppo crops exist already | delete, or repair if more crops are wanted |
| `py/check_ac_word_finding.py` | fails 160 of 160, comparing `"1of2"` with `1`; `doc/PLAN-evacuate-public-repos-programme.md` records this as deliberately unfixed | Ben's call: fix the comparison, or delete |
| `py/main_verify_meteg_vs_mgketer.py` | a spent one-time check; by its docstring it now fails for all thirty suggestions | delete |
| `py/main_ws_bot.py holman-meteg-spec` | one-shot, and now raises by design; its module says "Archive the two specs with item 6" | remove the subcommand |
| `py/main_source_hygiene.py` | Its recorded caller, a pre-commit hook, does not exist, and `py/tests/source_hygiene_test.py` runs the same scan | delete, or keep it with a corrected docstring |

Dead code inside live modules: `example_run()` in `py/main_uxlc_estimate_atom_loc.py`, and the
uncalled `add_args` and `run` at the end of `py/author_site/post_stress_meteg.py`.

## 7. The check Ben asked for: a proposed design

- **The declaration.** `py/tests/test_mega_coverage.py` holds `NOT_IN_MEGA`, a dict from program to
  reason. A key is a path plus a subcommand or mode, e.g. `"py/main_download.py fr-wikisource"`.
  Each reason says why the program is left out and where that is recorded. The shape is that of
  `SIBLINGS_REACHED` in `py/tests/test_sibling_reach.py`, whose AST machinery it can share.
- **What counts as a program.** Every tracked `.py` with a `__main__` guard outside `py/tests/`,
  found by AST rather than by file name, because `check_*.py` and `fix_*.py` are programs too. For
  an entry point with argparse subcommands, every `add_parser` name counts, including names built
  from a table, which the lint resolves from the table as the sibling lint resolves
  `REDIRECT_REPOS`.
- **What counts as in the mega.** A `main_*` module that `py/main_0_mega.py` imports and whose
  function a runner calls; the subcommand named in an `almost_main([...])` call; the script path in
  a subprocess argv. A mode chosen by flags cannot be seen this way, so the few programs where the
  mega runs one mode and not another are declared by hand, with the mode spelled out.
- **What fails.**
  1. A program neither run by the mega nor declared.
  2. A declared program that no longer exists: the dead-entry check `test_sibling_reach.py` already
     has.
  3. A declared program that the mega now runs.
- **How it becomes part of maintenance.** MAM-basics' maintenance is `py/main_repo_maintenance.py`.
  Its step 5 runs the suite before its step 6 runs the mega, while the cross-repository runbook
  covers, by its title, every repository except MAM-basics. So a lint in the suite runs during
  maintenance with no new wiring. Name it in `py/main_repo_maintenance.py`'s docstring as well;
  that docstring's list of mega steps is stale (§8).
- **Where the reasons come from.** The §3 rows go in with their citations. The §4 rows go in marked
  as Claude-written proposals until Ben accepts them.

## 8. Incidental findings, raised and not fixed

1. `py/py_ac_loc/merge_line_markers.py` compares Hebrew through `unicodedata.normalize("NFC", …)`,
   which `CLAUDE.md` forbids; it writes the original strings back, not the normalized ones.
2. In `py/check_all.py`, the spell check's `exit(1)` escapes `_run_spellcheck`, so a spelling
   finding skips the other six checks.
3. The mega steps listed in `py/main_repo_maintenance.py`'s docstring include "vendor-uxlc", which
   is not a step, and leave out `sigil-inventory`, `near-aleppo-census` and `gen-site`.
4. `py/pipeline_graph/pipeline_graph_spec.py` has drifted from `_STEPS`. It draws "ws_bot real"
   and "osis_split_mapm", neither of which is a step, and has no node for the wlc and accgram
   steps, `sigil-inventory`, `near-aleppo-census`, `gen-site` or `vendoring-audit`. It also draws
   "diff ctr-vs-mam", which was not a step when this was written, and has been one since phase 5c
   of `doc/PLAN-mega-coverage.md` added `diff-ctr-vs-mam` the same day.
5. Docstrings that still describe the layout from before the evacuations:
   - `py/main_uxlc_mega.py`, "the sibling UXLC-utils'";
   - `py/main_estimate_uxlc_locations.py`, and its NOTE constant, which is written into a tracked
     JSON;
   - `py/main_render_uxlc_corrections.py`;
   - `py/main_search_final_hiriq_verse_text.py` and `py/hkq_cmn/qere_ending_search.py`, which
     still say the output goes through `require_sibling`;
   - `py/main_apply_cam1753_crops.py`;
   - `py/py_cam1753_loc/split_spreads.py`;
   - `py/verify_mp/survey_artifact.py`, which still calls the template survey "intentionally a
     manual step".
6. `py/main_edition_transcription.py`'s docstring says the program writes only disposable
   renderings, but `build` writes tracked files.
7. `py/scan_pages/editions.py`'s `scans_root()` is hard-coded to
   `~/OneDrive/Documents/ScansOfBooks`, and ignores the `WLC_SCANS_DIR` override that
   `py/accgram/scan_page.py` honours.
8. Two documented commands do not work: `py/py_ac_loc/gen_line_break_editor.py` rejects the
   documented `270v 1`, and `py/main_gen_cam1753_crop_editor.py` lacks the documented `--status`
   and `--batch`.
9. **MAM-private's census still lists MAM-OSIS, whose clone is gone.**
   `near-aleppo/census/gershayim_contexts.py` names `"MAM-OSIS"` among the clones it counts, so the
   mega's `near-aleppo-census` step will print `MAM-OSIS: absent` and rewrite a tracked golden in
   MAM-private on its next run. On 2026-09-09 Ben authorized dropping MAM-parsed, MAM-with-doc,
   MAM-simple and MAM-for-Sefaria from that same list, and regenerating the golden.
10. `py/main_accgram.py` defines 28 subcommands, while
    `doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md` says 34.

## 9. Closing record, 2026-09-10: the mega's 60 steps, and the check that keeps the rest declared

Written by the Claude session that executed phase 8 of `doc/PLAN-mega-coverage.md`, the plan that
carried out §1's six decisions. **Measured on** the branch `claude/mega-coverage` at `c9e99dcb`,
before its integration into `main`. `_STEPS` in `py/main_0_mega.py` is the authority on the steps
from then on.

**The mega has 60 steps**, where §2 counted 41. The program each runs is the one that
`py/tests/test_mega_coverage.py` reads from its runner:

| # | Step | Program it runs |
|---|---|---|
| 1 | `parse-ws` | `py/main_parse.py ws`, which also runs what `py/main_authored.py gen-mam-parsed-docs` runs, the MAM-parsed documents, `doc/mp-claims.md` and the claim verification, and checks every plus book it writes with `check_mpplus` |
| 2 | `foi-features-of-interest` | `py/main_foi_features_of_interest.py` |
| 3 | `parse-go` | `py/main_parse.py go`, which writes only `MAM-parsed/google/` |
| 4 | `diff-wsgo` | `py/main_diff.py wsgo` |
| 5 | `mam-with-doc` | `py/main_mam_with_doc.py` |
| 6 | `diff-mpp` | `py/main_diff.py mpp --all` |
| 7 | `diff-ctr-vs-mam` | `py/main_diff.py ctr-vs-mam` |
| 8 | `tmpl-survey` | `py/main_tmpl_survey.py` |
| 9 | `tmpl-survey-toy` | `py/main_tmpl_survey_toy.py` |
| 10 | `vendored-tmpl-survey-toy` | `MAM-parsed/py-examples/main_tmpl_survey_toy_example.py`, as a subprocess |
| 11 | `mam-simple` | `py/main_mam_simple.py core-only`, which ends by running what `copy-support-files` runs |
| 12 | `mam-simple-docs` | `py/main_mam_simple.py doc-only` |
| 13 | `mam4sef-and-ajf` | `py/main_mam4sef.py --both-sef-and-ajf` |
| 14 | `mam-osis` | `py/main_mam_osis.py` |
| 15 | `letter-small-job` | `py/main_letter_small_job.py` |
| 16 | `vendored-letter-small-job` | `MAM-simple/py-examples/main_letter_small_job_example.py`, as a subprocess |
| 17 | `vendored-mam4sef` | `MAM-simple/py-examples/main_mam4sef_example.py`, as a subprocess |
| 18 | `vendored-mam-osis` | `MAM-simple/py-examples/main_mam_osis_example.py`, as a subprocess |
| 19 | `decnreub` | `py/main_decnreub.py` |
| 20 | `multimark` | `py/main_multimark.py` |
| 21 | `wordlist` | `py/main_wordlist.py` |
| 22 | `search-final-hiriq-verse-text` | `py/main_search_final_hiriq_verse_text.py` |
| 23 | `search-holam-he-qere` | `py/main_search_holam_he_qere.py` |
| 24 | `explicit-xataf` | `py/main_explicit_xataf.py` |
| 25 | `ws-bot-proto` | `py/main_ws_bot.py proto`, without `--edits` |
| 26 | `gen-misc` | `py/main_authored.py gen-misc` |
| 27 | `wlc-json-and-unicode` | `py/main_wlc_json_and_unicode.py` |
| 28 | `accgram-run-prose` | `py/main_accgram.py run-prose` |
| 29 | `accgram-test-fixes` | `py/main_accgram.py test-fixes` |
| 30 | `accgram-run-dual-cant` | `py/main_accgram.py run-dual-cant` |
| 31 | `accgram-run-poetic` | `py/main_accgram.py run-poetic` |
| 32 | `accgram-xcheck-poetic` | `py/main_accgram.py xcheck-poetic` |
| 33 | `accgram-servi-xcheck` | `py/main_accgram.py servi-xcheck` |
| 34 | `accgram-grammaticality` | `py/main_accgram.py grammaticality` |
| 35 | `accgram-run-printed-decalogue` | `py/main_accgram.py run-printed-decalogue` |
| 36 | `accgram-survey-chanted-word-accents` | `py/main_accgram.py survey-chanted-word-accents` |
| 37 | `accgram-generate-html` | `py/main_accgram.py generate-html --trust-survey` |
| 38 | `uxlc-check-changes` | `py/main_uxlc_check_changes.py` |
| 39 | `uxlc-fois` | `py/main_fois.py` |
| 40 | `uxlc-write-page-break-info` | `py/main_write_page_break_info.py` |
| 41 | `uxlc-amb-early-mtg` | `py/main_amb_early_mtg.py` |
| 42 | `uxlc-word-list` | `py/main_uxlc_word_list.py` |
| 43 | `clc` | `py/main_clc.py all` |
| 44 | `estimate-uxlc-locations` | `py/main_estimate_uxlc_locations.py` |
| 45 | `render-uxlc-corrections` | `py/main_render_uxlc_corrections.py` |
| 46 | `verify-and-render-table` | `py/main_verify_and_render_table.py` |
| 47 | `book-of-job-site` | `py/main_gen_misc_authored_english_documents.py`, which ends by running `py/check_spelling_in_html.py` |
| 48 | `map-changes-to-book-of-job` | `py/main_map_changes_to_book_of_job.py` |
| 49 | `find-uxlc-accent-changes` | `py/main_find_uxlc_accent_changes.py`, without `--audit` |
| 50 | `uxlc-grammar-test` | `py/main_uxlc_grammar_test.py` |
| 51 | `wlc-diffs-420422` | `py/main_wlc_diffs_420422.py` |
| 52 | `wlc-a-notes` | `py/main_wlc_a_notes.py` |
| 53 | `sigil-inventory` | `py/main_sigil_inventory.py` |
| 54 | `near-aleppo-census` | MAM-private's `near-aleppo/census/run_all.py --write`, as a subprocess; skipped in a cloud session |
| 55 | `accgram-survey-post-stress-meteg` | `py/main_accgram.py survey-post-stress-meteg`; skipped in a cloud session |
| 56 | `gen-site` | `py/main_authored.py gen-site --trust-surveys` |
| 57 | `diffable-pointed-hebrew` | `py/main_diffable_pointed_hebrew.py`, over the four input and output pairs of its `TRACKED_EXPANSIONS` |
| 58 | `ac-gen-index-flat-annotated` | `py/main_ac_gen_index_flat_annotated.py` |
| 59 | `pipeline-graph` | `py/main_pipeline_graph.py` |
| 60 | `vendoring-audit` | `py/main_vendoring.py`, its `--all` audit |

Two steps use MAM-private, and a cloud session skips both, by Ben's decisions of 2026-09-10:
`near-aleppo-census`, which runs in that clone and rewrites its tracked goldens, and
`accgram-survey-post-stress-meteg`, which reads its Phonetic MAM. `parse-go` and `diff-wsgo`, the
Google Sheet's two steps, left the mega in `426fa229` and came back the same day, by Ben's
decision, in phase 7b of the plan.

**Every other program is declared, and a check keeps it so.** `py/tests/test_mega_coverage.py`
finds 141 programs: the tracked `.py` files outside `py/tests/` with a `__main__` block, 91 of
them, a file with argparse subcommands counting once per subcommand. The mega runs 62 of the 141.
`NOT_IN_MEGA` in that file declares the other 79, and 20 modes that the mega does not run of
programs it does run, 99 entries in all, each with the reason the mega leaves it out and where
that reason is recorded. 26 of the reasons are Claude-written proposals, most of them from §4,
and Ben accepted them all on 2026-09-10. The check fails the suite on a program neither run nor
declared, on a declaration whose program, subcommand or flag is gone, and on a declaration of
something the mega now runs. So it keeps true what this section claims, that every program is
run by the mega or declared with a reason. MAM-basics' maintenance runs the suite at step 5 of
`py/main_repo_maintenance.py`, before its step 6 runs the mega. The check does not keep the table
above current, and `_STEPS` is where to look for the steps as they are. To re-count, run the
check and read its `_programs()`, `_scan_mega()` and `NOT_IN_MEGA`.

**What became of the recommendations.** The plan's phase records have the detail and the
commits.

1. Decision 1: phase 1 (`516a4a1a`) lets a worktree run find MAM-private beside its home clone,
   and phase 2 (`9657a081`) made the survey a step. That retires §3's first row and §5's last
   row, each now marked.
2. Decision 2: phase 4 (`f7fb6a62`) folded `py/main_uxlc_mega.py`'s five steps into the mega,
   and deleted it.
3. Decision 3: phases 5a, 5b and 5c added every generator that §5 marks "add", the last of them
   `py/main_diff.py ctr-vs-mam`, once `9fa80e11` gave its template table the narrow-sense paseq
   template. §5's three gaps are closed, each marked where it stands.
4. Decision 4: phase 3 (`985262e2`) removed the two Wikisource index generators, the
   column-coordinate plots and the Sefaria download. The line-break reports and the slide
   thumbnails stay out, declared with Ben's decisions.
5. Decision 5: phases 6a and 6b deleted everything in §6. `py/check_ac_word_finding.py` was
   first fixed and then retired, as Ben chose (`26962cb4`, `7fa58d73`).
6. Decision 6: phase 7 built the check (`3f27b33f`, `d2acfaea`), and phase 8 marked the 26
   accepted reasons (`6fc8ddaa`).

Of §4's rows, two name programs that phase 6a deleted, `py/main_source_hygiene.py` and the
`__main__` block of `py/accgram/ctr_decalogue.py`. Phase 7b dropped the declarations of
`py/main_foi_features_of_interest.py --foi` and `--single-threaded`, since the check counts a
flag that narrows a job or changes how it runs as no mode. Every other reason in §4 is one that
Ben accepted.

**Verified by a full run.** On 2026-09-10 every step except `near-aleppo-census` ran in order, as
the mega runs them, from a throwaway script that imports `py/main_0_mega.py` and picks the steps
from `_STEPS`: all 59 passed, in 377 seconds, and though they wrote 1,611 tracked files, `git status
--porcelain` was empty afterwards, every one of those files having come out byte-identical. The
census was left out because it rewrites tracked goldens in MAM-private, and its next run is Ben's.
The suite then gave 992 passed, 5 skipped.

**Still open, and outside the plan:** §8's findings, except where a phase record of the plan says
that phase fixed one, and the four items of the plan's section "Not in this plan, raised for
Ben".
