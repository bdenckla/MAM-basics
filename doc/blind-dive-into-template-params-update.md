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
   `py/mb_cmn/parser_stage_template_schema.py:validate_parser_stage_template` checks every argument's
   identity as well as the argument count: against `_PARSER_STAGE_NAMED_ARGUMENT_IDENTITIES` where
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

## The Google comparison product named in finding 4 was retired

Recorded by Codex on 2026-09-27. The base review's description of finding 4 names
`py/subcommands/diff_wsgo.py`, the two `out/diff_mamws_mamgo*.json` files, and proposed
Google Sheet edits as products reached by the weaker validator. Those paths were historical
evidence at the reviewed commit, but the Google download, parse, comparison, and auto-edit
pipeline was removed during the execution of the archived [Google Sheet retirement plan](https://github.com/bdenckla/MAM-basics/blob/eea4c583f12ee90f75003dd4c75be5d6d52f7c85/doc/PLAN-retire-google-sheet.md). The survey and
documentation-verification paths named beside them remained current at that checkpoint.

## The maintenance audit also found missing validation in dataset inventories

Fixed by Codex during the maintenance pass of 2026-09-28: the topmost-documentation-note
finder and the plain/plus stack-path lookup were made to validate recognized templates before
recording a result or recursing. This supplements the base review's passage “several closed shape
validators are not called on paths that discard parameters”; the inventory paths below were
outside that passage's original list. The pass reviewed MAM-basics at
`8c2fa6c3442997a1cdf4c08504974c5db8fbd38d`, prioritizing consumers changed after the earlier
repairs in `1b7b97ef` and following their shared helpers.

`py/explicit_xataf/extract.py:find_docnote_tmpls` previously accepted a documentation-note
template before validating its required parameters and silently ignored a mapping that did
not have a recognized template representation. Every encountered mapping now goes through
`validate_current_plus_template`. The inventory still records topmost notes and visits every
classified branch outside those note bodies. Its routine callers are the explicit-xataf
generator and the sigil inventory. The HBCE Psalms census also calls it; the current census
matches all 620 rows of the frozen `hbce-psalms/out/mam_psalms_docnotes.tsv` byte for byte, and
the frozen output was preserved.

`py/tmpl_survey/stack_path_lookup.py:_walk_wtel_plain` and `_walk_wtel_plus` previously
accepted template names without the current schemas and skipped mappings that failed the
structural template predicate. Both walkers then validated names and shapes before matching or
recursing, and the plain walker also validated the recognized custom-tag leaves; the merge
`ebbfa90f`, which integrated the plain retirement on 2026-09-28, removed that walker, and
`_walk_wtel_plus` keeps the validation. Stack discovery
retains every classified branch and the existing occurrence order, limits and verbose payloads.
The existing occurrence fixture was corrected to use a valid parameterless separator template.
Normal and verbose CLI results for `E/נוסח` matched before and after in each dataset, and a
lookup with no matching path traversed the complete plain and plus corpora successfully.

Remains deferred: the semantic choices in
`doc/PLAN-deferred-template-projection-decisions.md`. This audit applied the existing shape
policies and chose no new ketiv/qere, strand, vowel, stress-helper, feature-population or link
policy.

The public reviewed-functions record follows. “Structural” means representation-preserving
traversal or a mechanical representation check; “inventory” means the declared classified
dataset population; “selected text” and “note prose” identify the consumer's named child roles.

| Source and searchable function anchors | Classification and disposition |
|---|---|
| `py/mb_cmn/ws_tmpl2.py`: `use_tmpl2`, `mktmpl_mp`, `map_params`, parameter accessors | Valid structural helpers. |
| `py/mb_cmn/mpplus_schema_guard.py`: `_walk` | Valid structural lint. |
| `py/mpplus/mpplus_boring_tmpls.py`: `evaluate` | Valid named structural transform; the inventory consumer now supplies its additional validation. |
| `py/mpplus/mpplus_slh_words.py`: `_recurse_down_into_tmpls` | Valid closed structural transform. |
| `py/mpplus/mpplus_scrdfftar.py`: `add`, `_make_edin_for_scrdff_pbd_yes` | Valid named scroll-note conversion. |
| `py/mb_misc/tmpl_survey_toy.py`: `_record` | Valid closed inventory. |
| `py/tmpl_survey/survey_plus.py`: `_record_wtel`, `_record_tmpl` | Valid closed whole-structure inventory. |
| `py/tmpl_survey/survey_plain.py`: `_wtel_type_and_subtype`, `_record_tmpl` | Valid closed template/custom-tag inventory. |
| `py/tmpl_survey/stack_path_lookup.py`: `_walk_wtel_plain`, `_walk_wtel_plus` | Fixed missing inventory validation. |
| `py/tmpl_survey/stack_path_verbose_payload.py`: `wtel_to_wikitext_plus`, `_wtseq_to_wikitext_plus` | Valid structural unparser. |
| `py/verify_mp/corpus.py`: `iter_plain_col_objects`, `iter_template_objects`, `iter_all_template_objects` | Valid structural corpus iterators. |
| `py/explicit_xataf/extract.py`: `find_docnote_tmpls`, `join_arg1_strings`, `flatten_text` | Fixed note inventory; closed note prose and named target projection retain existing choices. |
| `py/sigils/inventory.py`: `_note_node_to_text` | Valid closed note-prose scan. |
| `py/hbce_psalms/mam_docnotes.py`: `_psalms_chapters`, `docnote_rows` | Whole-minirow note inventory using the repaired finder. |
| `py/mb_diff_mpu/mpplus_extract.py`: `_canonicalize_template_names`, `_targeted_scrdff_note_values`, `_drop_redundant_non_targeted_scrdff_notes` | Valid structural historical normalization. |
| `py/mb_diff_mpu/mpplus_normalize.py`: `_normalize_element` | Valid structural historical normalization. |
| `py/mb_diff_mpu/mpplus_structure.py`: `collect_template_names`, `_structure_occurrences`, `_alternative_role_params`, `_alternative_text`, `_alternative_instances` and its `visit` | Valid classified structure inventory and approved alternative comparison. |
| `py/mb_diff_mpu/mpplus_docnote.py`: `_to_raw_html`, `_render_template` | Closed note-prose renderer; the recorded internal-link choice remains deferred. |
| `py/hkq_cmn/qere_projection.py`: `project_qere_atoms`, `_project_argument_keys`, `word_atoms_from_qere_atoms` | Valid named caller policies and adjacent-fragment tokenization. |
| `py/py_misc/wt_qere.py`: `_do_one_wtel`, `hnd_recurse_on_all_declared_alternatives` and named handlers | Closed first-stage qere projection with declared alternatives retained. |
| `py/multimark/multimark_1.py`: `_do_one_wtel`, `_recurse_on_keys` | Declared maximal population; its policy remains deferred. |
| `py/versification_differences/hebrew.py`: `_flatten_wtseq`, `_flatten_wtel`, `_recurse_on_keys` | Declared range-label projection; its policy remains deferred. |
| `py/accgram/rtms_token_like.py`: `texts_from_token_like_payload` | Closed record fields; its population choice remains deferred. |
| `py/accgram/breuer_word_length.py`: `_flatten`, `_qamats_branch_labels` | Named phonetic-record dispatch; its alternative choice remains deferred. |
| `py/accgram/mam_simple_verse.py`: `_iter_dict_nodes`, `_mam_simple_fragments`, `_mam_simple_kq_qere_fragments`, `_normalize_mam_simple_verse`, `_normalize_mam_simple_node` | Structural verse location and named text projection. |
| `py/accgram/mam_poetic_accents.py`: `_iter_verse_nodes`, `_walk`, `_walk_kq` | Structural verse location and named event projection. |
| `py/render_wt/render_wikitext_helpers.py`: `_handle_wikitext_element` and traced handlers | Closed renderer with named Scripture and apparatus roles. |

Verification passed: Black and Ruff, the full suite (1,019 passed, five skipped), and all
52 mega steps. The rebuilt tracked artifacts were unchanged. The CLI comparisons and full
dataset traversal described above also passed; the frozen Psalms note census was checked
through its read-only row builder.

## The persisted plain product and survey have been retired

Recorded by Codex on 2026-09-28 during execution of
`doc/PLAN-retire-mam-parsed-plain.md`. The base review's descriptions of
`MAM-parsed/plain/`, `py/tmpl_survey/survey_plain.py`,
`out/tmpl-survey-plain/`, and the published plain-template call graphs are now
historical evidence about the reviewed commit. The maintenance-audit table's
plain-survey row, the plain half of its stack-path-lookup row, and its plain-corpus
iterator names are likewise historical evidence about that audit's commit.
MAM-basics no longer persists or distributes the plain representation or its
survey. The raw template-shape and expanded-stack checks remain live at the
transient parser-stage validation boundary in `py/verify_mp/parser_stage.py`.

## Corrections made in the 2026-09-29 review's remediation, 2026-09-30

Recorded by Claude on 2026-09-30, New York time, under the approved remediation plan for the
2026-09-29 dual-agent review. The merge `ebbfa90f`, which integrated the plain retirement
`87fc7141` on 2026-09-28, left five passages above false. The first two now have `87fc7141`'s own
wording, which that merge dropped (the review's finding 1.3); the other three are of the same
kind (the plan's flagged site 1).

1. In "Three of the review's five findings have been fixed, finding 3 partly, and finding 1 is
   deferred", item 4:
   "`py/mb_cmn/plain_template_schema.py:validate_current_plain_template` checks every argument's
   identity … against `_CURRENT_PLAIN_NAMED_ARGUMENT_IDENTITIES`" now reads
   "`py/mb_cmn/parser_stage_template_schema.py:validate_parser_stage_template` checks every
   argument's identity … against `_PARSER_STAGE_NAMED_ARGUMENT_IDENTITIES`".
2. In "The Google comparison product named in finding 4 was retired": "The survey and
   documentation-verification paths named beside them remain current." now reads "… remained
   current at that checkpoint."
3. In "The maintenance audit also found missing validation in dataset inventories": "the
   plain/plus stack-path lookup now validate recognized templates before recording a result or
   recursing" now reads "… were made to validate recognized templates …".
4. In the same entry: "Both walkers now validate names and shapes before matching or recursing.
   The plain walker also validates the recognized custom-tag leaves." now reads "Both walkers then
   validated names and shapes before matching or recursing, and the plain walker also validated
   the recognized custom-tag leaves; the merge `ebbfa90f`, which integrated the plain retirement
   on 2026-09-28, removed that walker, and `_walk_wtel_plus` keeps the validation."
5. In the same entry: "Normal and verbose CLI results for `E/נוסח` match before and after" now
   reads "… matched before and after …".

## The 2026-10-07 maintenance audit found no undeclared projection in new or changed walkers

Recorded by Claude on 2026-10-07, New York time, during repository maintenance, under step 6 of
`doc/PLAN-repo-maintenance-across-GitRepos.md`. A delegated read-only review covered every Python
file added, renamed or changed between the previous audit's commit
`e5f5045d34bf1cede1f8b25c2a75e000645b0056` and `61ab4e3b3f8c9eec5ee4d1f618a34b92c3abb020`, 474
files over 410 commits. It screened them with an AST scan for recursion and the runbook's anchors
and a scan of added lines for new calls to shared walker helpers, then read every hit. The
recording session re-read the three latent items below in the code and re-measured the first one's
counts at `72c698939af4b89dd2025a761cb4a85f21e5af56`. No confirmed undeclared projection was found,
and the deferred decisions in `doc/PLAN-deferred-template-projection-decisions.md` were not
re-raised.

| Source and searchable function anchors | Classification and disposition |
|---|---|
| `py/near_aleppo/phase2_templates.py`: `Resolver._sequence`, `_template`, `_kept`, `_special_letter_word`, `selected_keys`, `_flatten`, `_assert_marks_flattenable` | Closed dispatch on `_RULES` with measured key sets; the docstring declares the selected parameters. |
| `py/near_aleppo/phase2_templates.py`: `assert_templates_absent`, `_contains_mark`, `_assert_no_marks`, `_replace_marks` | Valid structural checks and transforms. |
| `py/near_aleppo/phase3_policies.py`: `Policies._value`, `_template`, `_selected_text`, `_clauses`, `_ketiv_qere_apparatus` | Closed dispatch; `_clauses` is the closed note-prose reader and raises on an unrecognized template. |
| `py/near_aleppo/phase5_readings.py`: `_walk`, `notes`, `_side_keys`, `_direct_ketiv_qere_target`, `Readings._apply` | Closed dispatch. |
| `py/near_aleppo/phase6_mam_targets.py`: `_walk`; `phase6_rename.py`: `Renames._walk`; `phase6_flags.py`: `Flags._walk` | Closed dispatch. |
| `py/near_aleppo/frozen_ketiv.py`: `sites`; `editorial_ketiv.py`; `reviewed_ketiv.py`; `note_content.py`; `doc_note_review.py`: `_data_notes`; `doc_template_examples.py`: `_wikitext`; `doc_policy_examples.py`; `doc_page.py`; `doc_he_transfer.py` | Closed dispatch or named selections. |
| `py/near_aleppo/census/edition_projection.py` and the `render`, `find` and `each_nusach` walkers of `qamats_params.py`, `stress_helper_census.py`, `adonai_census.py`, `divine_name_split.py` and `nusach_aleppo_readings.py` | Declared single-stream projection table that fails fast; latent items 1 and 3 below. |
| `py/near_aleppo/census/template_inventory.py`: `walk_raw`, `walk_settled` | Declared raw inventory and declared population; `walk_settled` checks names, and the build's phase 2 checks key sets. |
| `py/near_aleppo/doc_figures.py`: `_walk`, `_templates`, `_characters`, `_new_characters`, `_selected_text`, `_mam_selected_text` | Zone-classified full inventory; `_new_characters` declares its population, which includes alternatives and the ketiv/qere apparatus parameters; the two selected-text readers are closed. |
| `py/render_wt/render_wikitext_handlers.py`: `_handle_doc`, now through `split_doc_params`, `_stored_doc_parts`, `_added_lines`, `_mam_target_line`, `_handle_marks_without_letter` | Closed renderer handlers with named roles. |
| `py/render_wt/render_wikitext_kq.py`: `_ht_kq_unpack_args`, `_pointing_display_order`, `handle_kq_trivial_ruby`, `_flagged`; `py/render_wt/render_wikitext_added_lines.py`; `py/py_misc/near_aleppo_params.py`; `py/py_misc/orphan_marks.py`: `carriers`; `py/py_misc/scrdfftar_to_doc.py`; `py/py_misc/trivial_qere_to_doc.py` | Closed dispatch. |
| `py/verify_mp/parser_stage.py`: `_validate_node`, `_validate_no_parser_stage_encoding`; `py/verify_mp/kq_qere_first_contexts.py`: `_scan`; `py/verify_mp/corpus.py`: `template_names_called` | Structural validation; `_scan` is a maximal structural search that fails on a target in a non-text parameter. |
| `py/phonetic_mam/strand_layouts.py`: `_strand`, `_dual_count`; `py/phonetic_mam/core/dualcant_templates.py`: `validate_template`; `py/phonetic_mam/core/dualcant_arguments.py`: `_get_dcargs_for_wtel`; `py/phonetic_mam/core/dualcant_prepare.py`: `prepare`; `py/phonetic_mam/display_projection.py`: `_row`, `_verse` | Closed dispatch and structural counts; qamats alternatives stay an explicit pair, and display branches stay labelled. |
| `py/phonetic_mam/display_schema.py`: `validate_tokens`; `py/phonetic_mam/core/distinguished.py`: `reject_legacy_annotations` | Valid structural validation. |
| `py/phonetic_mam/analysis_reader.py`: `Verse.readings`, `Verse.events`, `select` | Every branch unless the caller selects. Its callers declare their choice: `py/accgram/meteg_before_stress.py`: `analyze_books` records the projection in its output; `py/accgram/post_stress_meteg_survey.py`: `_scan` names its selectors in the survey's scope field; `py/tests/test_final_stress_vs_phonetic_mam.py`: `_book` is a declared all-branch oracle; `py/accgram/breuer_word_length.py`: `load_phonetic_book` is deferred decision 3. |
| `py/accgram/post_stress_meteg_sources.py`: `_written_stress_helpers`; `py/accgram/breuer_word_length.py`: `_written_forms_by_reading`; `py/accgram/decalogue_m_trad.py`: `_flatten_template`; `py/accgram/printed_decalogue_fetch.py`: `_resolve_templates` | Closed dispatch; `_written_forms_by_reading` names the `cant-alef` strand, and `_resolve_templates` raises on any template left over. |
| `py/accgram/maqaf_nonfinal_accents.py`: `_mam_simple_gray_maqafs_by_verse` | Structural count of every implicit-maqaf node, held equal to the hits along `flatten_ep_for_diff`'s selected stream, so a divergence raises. |
| Recursion unchanged since the previous audit: `py/tmpl_survey/stack_path_lookup.py`: `_walk_wtel_plus`; `py/tmpl_survey/stack_path_verbose_payload.py`; `py/tmpl_survey/survey_plus.py`; `py/tmpl_survey/nesting_normal_form.py`; `py/mb_diff_mpu/mpplus_structure.py`; `py/mpplus/mpplus_boring_tmpls.py`; `py/verify_mp/verifiers_templates.py`: `_iter_template_occurrences_with_ancestors` | Seen again; only the plain retirement and docstrings changed them. |

The audit left three latent items unfixed. The 2026-10-08 and 2026-10-09 entries below fix item
1 and dispose of item 2; item 3 remains unfixed. None changed a tracked output on the audit's
day; each is recorded so that a later change cannot make it live unnoticed. The census and
phase-6 code they concern were under active near-Aleppo development on the audit's day, so
maintenance changed none of them.

1. **The stress-helper census reads note prose through the Scripture projection.** In
   `py/near_aleppo/census/nusach_aleppo_readings.py`, `clauses`, which
   `py/near_aleppo/census/stress_helper_census.py` calls, flattens each non-separator template
   with `flatten(..., projected=True)`. The census therefore drops the display text of the link
   templates `מ:קישור בהערה` and `מ:קישור פנימי בהערה`, since their edition keys in
   `py/near_aleppo/census/edition_projection.py` are empty. The legarmeh template `מ:לגרמיה-2` and
   the narrow-sense paseq template `מ:פסק` become spaces, since that table lists them as
   separators. The build's note-prose reader, `py/near_aleppo/phase3_policies.py`: `_clauses`,
   keeps the link text, writes Unicode PASEQ (U+05C0) for both of the latter templates, and raises
   on any template it does not name. At `72c69893`, the note bodies that the census's `each_nusach`
   walk reaches hold 32 and 2 of the two link templates, 31 of `מ:לגרמיה-2` and 9 of `מ:פסק`. None
   of them is in any of the 18 clauses that `in/near-aleppo/census/stress_helper_census.txt`
   reports, so the census does not depend on the difference today. Whether the census should read
   note prose as phase 3 does was a choice for Ben; he chose on 2026-10-08 that it should, and the
   entry below records the change.
2. **Uncalled code in the same module.** In `py/near_aleppo/census/nusach_aleppo_readings.py`,
   `collect` and `keys_for` have no callers, `text_of` is called only by `collect`, and no caller
   passes `projected=False` to `flatten`, whose `False` branch walks every parameter of every
   template without validation. It would become a blind dive only if something called it again.
   The 2026-10-08 entry below deletes `keys_for` and the `False` branch, and the 2026-10-09
   entry records Ben's decision to keep `collect`.
3. **Silent fallbacks with no input that reaches them.** The `render` functions of
   `qamats_params.py`, `stress_helper_census.py`, `adonai_census.py` and `divine_name_split.py`,
   under `py/near_aleppo/census/`, return an empty string for a mapping that is not a template, and
   `each_nusach`, `walk_raw` and `walk_settled` skip one. `py/near_aleppo/phase6_flags.py`:
   `_matching_templates` returns without recursing for a template that `phase2._RULES` does not
   name, and does nothing for a rule action other than the three it handles. The review's scan
   found no non-template mapping in any plus cell at `61ab4e3b`, and `_matching_templates` sees
   only note targets that phase 3's closed walk has accepted, with its result held to an exact
   count. Closed dispatch would raise in each case.

Verification for this audit: the full suite (1,047 passed, five skipped) and all 60 mega steps,
with no tracked diff, ran at `61ab4e3b`; `py/main_near_aleppo.py --check` reported the five census
baselines, the dataset and the pages current at `72c69893`.

## The census reads note prose with phase 3's reader, 2026-10-08

Ben's decision on latent item 1 of the 2026-10-07 entry above, given on 2026-10-08 in reply to
that maintenance's report: "sure, let's do that". `doc/PLAN-maintenance-follow-up-2026-10-08.md`,
workstream A, carried it out from `ba3e0d483c94fa484a54f797d7381fe5db23aa52` in a Claude cloud
session.

1. **Item 1 is fixed.** `py/near_aleppo/census/nusach_aleppo_readings.py`: `clauses` now takes a
   verse reference and reads the note body with `py/near_aleppo/phase3_policies.py`: `_clauses`,
   keeping its own rule of dropping empty clauses. Link templates now contribute their display
   text, `מ:לגרמיה-2` and `מ:פסק` contribute HEBREW PUNCTUATION PASEQ as phase 3 writes them,
   and any template that reader does not name raises with the census's verse reference.
   `py/near_aleppo/census/stress_helper_census.py`: `main` passes `nar.ref(bcvt)`.
2. **Item 2 is partly fixed.** `keys_for` is deleted, and so is `flatten`'s `projected` keyword
   with its unvalidated branch that walked every parameter; `flatten` now has only the edition
   projection, which `text_of` uses for a note's Scripture target. `collect` and `text_of` are
   kept, unfixed, for a reason the plan did not foresee. `collect` is the only user of `text_of`
   and `flatten`, of six siglum helpers (`split_outside_brackets`, `normalize`, `expand`,
   `classify`, `head_is_prose` and `prose_head_last_siglum`), and of `CODEX_TEXT`,
   `CODEX_TESTIMONY`, `NOT_THE_TEXT` and `PAREN_LIST`. Comments in
   `py/near_aleppo/phase6_flags.py` and at `py/near_aleppo/phase3_policies.py`'s `_head_sigla` and
   `_TESTIMONY_LIST` name this module as the census's authority for how sigla are read. Deleting
   `collect` therefore means deleting or rehoming that authority and correcting those three
   comments, in code another session edits most days. That was put to Ben; the 2026-10-09 entry
   below records his decision. The same measurement found that `reading_head`, the `BRACKETED`
   pattern it uses, and the `HEBREW` and `POINTED` patterns had no user at all; the 2026-10-09
   entry deletes them.
3. **Outputs.** `py/main_near_aleppo.py --check` reported all five census baselines byte for
   byte, the dataset, `build-populations.json` and the pages current after the change. A scratch
   run of `collect` over the whole corpus, which also feeds every reachable note body through
   phase 3's reader, raised nothing and gave the same summary counts before and after: 3,595
   notes, 6,879 clauses, of which 2,140 agree, 3,487 differ and 1,252 have no equals sign.
4. **Checks.** `py/main_test.py py/tests/test_near_aleppo.py
   py/tests/test_near_aleppo_note_content.py` passed five tests; Black left both changed files
   unchanged; `python -m ruff check py` passed.

## `collect` is kept as the census's declared population code, 2026-10-09

Ben's decision on 2026-10-09, accepting the recommendation of the session that executed
workstream A: keep `collect`, since comments at `py/near_aleppo/phase3_policies.py`'s
`_head_sigla` and `_TESTIMONY_LIST` and in `py/near_aleppo/phase6_flags.py` name
`py/near_aleppo/census/nusach_aleppo_readings.py` as the census's authority for how sigla are
read. `collect`'s docstring now declares it that module's population code for the qualified
clauses and records the decision. With `text_of` and `flatten`, which only `collect` uses, it is
no longer unfixed but declared. `reading_head`, `BRACKETED`, `HEBREW` and `POINTED`, which nothing
used, are deleted. Latent item 2 is thereby disposed of. `py/main_near_aleppo.py --check`
reported the five census baselines, the dataset and the pages current afterwards; Black and
`python -m ruff check py` passed.

## Archived receipt references, 2026-10-09

Recorded by Claude on 2026-10-09, New York time, in the cloud session that executed
workstream C of `doc/PLAN-maintenance-follow-up-2026-10-08.md`, after Ben approved its
deletion list and corrections that day. The entry "The persisted plain product and survey have been retired" says it was
"Recorded by Codex on 2026-09-28 during execution of `doc/PLAN-retire-mam-parsed-plain.md`".
That completed receipt has been retired from the tracked tree and remains at
[MAM-parsed plain retirement plan](https://github.com/bdenckla/MAM-basics/blob/38a8db9ae851b83d43b5c5ad42c007943b54d724/doc/PLAN-retire-mam-parsed-plain.md).
