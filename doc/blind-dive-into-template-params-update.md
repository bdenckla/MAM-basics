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
| `py/render_wt/render_wikitext_handlers.py`: `_handle_doc`, now through `split_doc_params`, `_stored_doc_parts`, `_added_clauses`, `_mam_target_clause` (until 2026-10-30 `_added_lines` and `_mam_target_line`), `_handle_marks_without_letter` | Closed renderer handlers with named roles. |
| `py/render_wt/render_wikitext_kq.py`: `_ht_kq_unpack_args`, `_pointing_display_order`, `handle_kq_trivial_ruby`, `_flagged`; `py/render_wt/render_wikitext_added_clauses.py` (until 2026-10-30 `render_wikitext_added_lines.py`); `py/py_misc/near_aleppo_params.py`; `py/py_misc/orphan_marks.py`: `carriers`; `py/py_misc/scrdfftar_to_doc.py`; `py/py_misc/trivial_qere_to_doc.py` | Closed dispatch. |
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

## The 2026-11-11 maintenance audit found one mislabelled projection in new or changed walkers

Recorded by Claude (Opus 5.5) on 2026-11-11, New York time, during repository maintenance, under
step 6 of `doc/PLAN-repo-maintenance-across-GitRepos.md`. A delegated read-only review covered
every Python file added, renamed or changed between `61ab4e3b3f8c9eec5ee4d1f618a34b92c3abb020`,
where the 2026-10-07 audit ended, and `d957048a20f671fbadea37325c91dd9c9bfe4ee9`: 554 files (366
modified, 185 added, 3 renamed) over 856 commits. It screened them with a reference graph over
all tracked Python for direct and mutual recursion across modules, with the runbook's anchors, with
a scan of added lines for calls to walker helpers, and with a screen for explicit-stack loops, then
read every hit in a MAM or Wikisource consumer and followed each shared helper with a new caller to
that caller's output. The recording session re-read C1 and latent items L1, L2 and L6 in the code
and confirmed that `4e9e7b84` is the commit that closed the 2026-10-07 latent item 3. The deferred
decisions in `doc/PLAN-deferred-template-projection-decisions.md` were not re-raised.

One item is confirmed, C1: a mislabel that changes no count. S1 and S2 were suspected; Ben
answered them, with C1, on 2026-11-12. L1 to L6 were latent; on 2026-11-12 `93eb8686` closed
five of them, and `345a0332` closed L4 later that day, as their list below records. The range's largest change for this audit is the template
מ:סילוק לפני געיה (`49b0baf7`, 2026-10-12), whose parameter 1 is a full atom and parameter 2 the
same letters with one HEBREW POINT METEG marking the silluq. Every consumer reviewed that reaches
its two calls, 1 Kings 7:37 and Job 4:12, names the template and reads parameter 1, or reads
through `py/py_misc/wt_qere.py`'s `HANDLERS`, which does.

"(new)" marks a function added in the range. "Seen again" means recursion unchanged since
`61ab4e3b`, the file edited elsewhere.

| Source and searchable function anchors | Classification and disposition |
|---|---|
| `py/mpplus/mpplus_boring_tmpls.py`: `evaluate`, `_preserve_silluq_before_meteg` (new), `_just_take_arg_1`, `_handle_bold`, `_handle_qupo`, `_handle_pseudo_title`, `_handle_word_with_puncta_extraordinaria` | Valid named structural transform (MAM-parsed-plus). The new handler validates the template, evaluates Scripture parameter 1 and keeps parameter 2 as metadata. |
| `py/mb_cmn/template_names.py`: `CURRENT_PLUS_TMPL_NAMES`, `CURRENT_PLUS_PARAM_POLICY`, `validate_current_plus_template`; `py/mb_cmn/silluq_before_meteg.py`: `validate_silluq_before_meteg`, `drop_post_silluq_metegs`; `py/mb_cmn/parser_stage_template_schema.py`; the identical copies in `MAM-parsed/py-examples/mb_cmn/` | Roster and closed schema: the silluq template has exactly parameters 1 and 2 and a validated position. |
| `py/render_wt/render_wikitext_helpers.py`: `render_wtseq`, `_handle_sequence` (new), `render_tmpl_el`, `render_named_param_val`; `py/render_wt/render_wikitext_kq.py`: `handle_qere_with_body` (new), `handle_kq`, `_flagged`, `_ruby` | Closed renderer with named roles. `_handle_sequence` pairs a body template, validated by `orphan_marks.validate_body`, with the following קרי ולא כתיב only when `ro_ketiv_qere_ruby` is set; `handle_qere_with_body` requires the complete qere-only call and renders its parameter 2. |
| `py/render_wt/render_wikitext_handlers.py`: `_handle_doc`, `_stored_doc_parts`, `_added_clauses`, `_mam_target_clause` (until 2026-10-30 `_added_lines`, `_mam_target_line`), `_doc_lemma_subhandler`, `_doc_parts_subhandler`; `py/render_wt/render_wikitext_added_clauses.py`: `flag_clauses` | Closed handlers with named roles; `b992842e` renamed lines to clauses and changed no role. |
| `py/render_wt/render_wikitext_handlers.py`: `_handle_stress_helper_word` (new), `_stress_helper_forms`, `_with_kept_meteg`, `_uninterrupted_word`, `_handle_silluq_before_meteg` (new), `_handle_space_without_marks` (new), `_handle_marks_without_letter` | Closed and validating. The deḥi and tsinnor form is now the caller's `ro_stress_helper` option, which raises on an unknown value: MAM-with-doc states parameter 2 keeping parameter 1's meteg (`mwd_write_book.RENOPTS_MAM_WITH_DOC`, Ben, 2026-10-26 and 2026-10-27), near-Aleppo states parameter 1, an unset option gives parameter 1 (L4, S2). The silluq handler renders parameter 1 and carries parameter 2 only as the `letters-with-silluq` attribute. |
| `py/mb_xml/xml_render.py`: `render_to_xml`, `_RENOPTS_MAM_XML` | MAM-simple's renderer call states cantillation and qamats and leaves the stress-helper form to the default (L4). |
| `py/mb_cmn/mam_simple_json.py` (new; identical copy in `MAM-simple/py-examples/mb_cmn/`): `attributes`, `children`, `find_child`, `structural_children`, `verses`, `read_book_group` | Valid structural readers; `verses` walks only the book24, book39 and chapter hierarchy and raises on a node out of place. |
| `py/mb_cmn/mam_json_verses.py` (ported from XML by `e6a85b43`): `get_verse_words`, `_scribal_difference_target_text`, `_form_words`, `_cant_combined_words`, `_trivial_kq_words`, `_silluq_before_meteg_text` | Not recursive. Closed dispatch whose module docstring declares each element's contribution: a kq's unpointed ketiv, a kq-trivial's displayed pointed form, the combined cantillation, a silluq annotation's text with its scaffold validated and not read. Permissive branches carried over from the XML reader: L3. |
| `py/osis/osis_runner.py`: `_handle`; `py/osis/osis_handlers.py`: `_silluq_before_meteg`, `_ketiv_qere`, `_scrdfftar` | Closed dispatch ported to JSON, now raising explicitly on an unhandled type and class; projection unchanged; the silluq handler emits the text and a note, never the scaffold. |
| `py/mb_sefaria/mam4sef_or_ajf.py`: `_handle` (seen again), `_iter_verses`; `mam4sef_handlers.py`, `mam4ajf_handlers.py`: `_silluq_before_meteg` | Closed dispatch; `_iter_verses` goes through `mam_simple_json.verses` (`4e9e7b84`); the silluq handlers drop only the later meteg marks, as Ben approved on 2026-10-12. |
| `py/mam_morphhb/morphhb_inline.py` (new): `render`, `to_xml`, `verse_children`, `HANDLERS`, `_HANDLERS_INSIDE_NOTE` | Closed dispatch on MAM-simple type and class, raising on any other: combined cantillation (`cant-alef` and `cant-bet` give nothing), ketiv and qere both marked, a scroll-difference note as an OSIS note. Declared in `MAM-morphhb/README.md`, item 5 of "Where MAM-morphhb differs from the 2014 form". `to_xml` is a serializer. |
| `py/mam_morphhb/morphhb_plus.py` (new): `plus_stream`, `_has_line_break`, `_column_c_levels`, `_verse_templates`, `_first_aliyah_name` | `plus_stream` is closed by name and raises on an unknown name; it reads parameter 1 of מ:דחי, מ:צינור and נוסח and ד of מ:קמץ, and takes ketiv/qere, special-letter and silluq templates as opaque tokens. These choices only place line breaks among tokens, and `morphhb_poetry.poetic_lines` checks the tokens against MAM-simple's one for one. It validates no template's shape: L2. `_has_line_break` is a maximal structural guard whose every hit raises. |
| `py/mam_morphhb/morphhb_poetry.py` (new): `_simple_items`, `_tokens`, `poetic_lines` | Closed projection of MAM-simple's children matching `plus_stream`'s, entering only a scroll difference's `sdt-target`; a token mismatch raises. |
| `py/mb_misc/letter_small_job.py` (identical copy in `MAM-simple/py-examples/mb_misc/`): `_small_letters`, `_check_container` | Declared annotation inventory that includes every alternative and note, with closed shape checks; an unknown type raises. |
| `py/mb_diff_mpu/mpplus_structure.py`: `collect_template_names`, `_structure_occurrences`, `_classified_param_items_for_structure` | Fixed in the range: a mapping without `tmpl_name` raises instead of having its values walked (`c2ec0a7a`, 2026-10-21). The silluq template is a parameter-1 role target. `_alternative_text` and `_alternative_instances.visit` seen again. |
| `py/mb_diff_mpu/mpplus_flatten.py`: `_flatten_diff_template_words_only`, `_flatten_diff_element_words_only`, `is_parashah_template`, `_PARAM1_BODY_NAMES` | Closed named dispatch; the silluq template gives parameter 1; a positional-punctuation template now gives a space (`3121f60a`, 2026-10-21); `is_parashah_template` lists its nine names instead of matching a resh followed by digits (`c2ec0a7a`). `flatten_element`, `_flatten_template`, `_flatten_diff_element`, `_flatten_diff_template` and the `_flatten_tracking` pairs seen again. |
| `py/mb_diff_mpu/mpplus_display.py`: `postprocess_kq_html`; `_kq_position_walk`, `_kq_position_walk_template`, `_collect_paseq_types` | Fixed: an unpaired ketiv/qere sentinel raises instead of being stripped (`c2ec0a7a`). The walkers are seen again. |
| `py/hkq_cmn/qere_projection.py`: `project_qere_atoms`, `_project_argument_keys`, `QereProjectionPolicy`, `FOI_KQ_SIMPLE_MAIN_COMPATIBLE_POLICY` | Named caller policies. The silluq template reads parameter 1; narrow-sense paseq and legarmeh have separate policy fields, and foi-kq-simple's pqere keeps its legarmeh (Ben, 2026-11-09, settling deferred item 8). `word_atoms_from_qere_atoms` seen again. |
| `py/hkq_cmn/mam_plus_verse_data.py`: `_collect_text_fragments` | Changed only to read the silluq template's parameter 1; its trivial ketiv/qere arm remains deferred decision 11. `_collect_template_argument_records` and `_render_template_like_text` seen again. |
| `py/foi/foi_wikitext_helpers.py`: `with_attached_marks`, `_with_attached_marks_in_params`, `_add_gray_maqaf`, `_with_mark_moved_back`, `_with_legarmeh`, `_with_mark_after`, `_templates_taking_a_mark_after`, `forms` (all new) | Structure-preserving transformation that validates each template and maps every parameter. It writes a legarmeh's PASEQ code point and the gray-maqaf stand-in onto their forms at every depth, and moves a following sof pasuq or maqaf only into the parameters `_PARAMS_TAKING_A_MARK_AFTER` names (Ben, 2026-11-09): a note's target, never its body. An unnamed template before such a mark raises. |
| `py/foi/foi_wikitext_helpers.py`: `templates_before_sof_pasuq`, `_add_templates_before_sof_pasuq` (new) | Positional structural search at every depth through `template_param_vals`; it checks a template only where a sof pasuq follows it: L1. |
| `py/foi/foi_wikitext_helpers.py`: `all_branch_foilers`, `_foiler_for_silluq_before_meteg` (new), `_foiler_for_all_named_params`, `_find_fois_in_wtel`, the `label_args_of_*` functions | Declared whole-dataset inventory; the silluq scaffold is excluded by name. |
| `py/foi/foiz_wt_dexi_stress_meteg.py` (new): `find_fois_wt`, `_handle_dexi`, `_handle_doc`, `_with_note`, `_mam_with_doc_form`, `_note_html`, `_text`, `_kind` | Declared population: every מ:דחי call in columns C, D and E and in good endings, at any depth. Named parameter roles; the MAM-with-doc column renders with `RENOPTS_MAM_WITH_DOC`. |
| `py/foi/foiz_wt_doc_note_notation.py` (new): `find_fois_wt`, `_find_fois_in_string` | Declared population: the strings of note bodies at any depth (`doc-part-n` in the stack), read by forms. |
| `py/foi/foiz_wt_holam_before_vav.py` (new): `find_fois_wt` | Declared single stream through `project_qere_atoms` with its own policy: qere, a trivial ketiv/qere's pointed ketiv, stress-helper parameter 1, ד, combined cantillation, each named in the module docstring. |
| `py/foi/foiz_wt_kq_1.py`, `foiz_wt_qamats_var.py`, `foiz_wt_slh_word.py`, `foiz_wt_rare_tmpls.py`, `foiz_wt_unicode.py`, `foiz_wt_kq_2.py`, `foiz_wt_pasoleg_2.py`, `foiz_wt_poetic_sh.py`, `foiz_wt_poetic_len.py`, `foiz_wt_rev_mug.py` | Seen again: populations unchanged; the range added the gray sof pasuq, reading by forms and index descriptions. `_html_for_wtseq` in the first three renders with the renderer's default options: S2. |
| `py/foi/foiz_wt_dual_ml_alef.py`: `_find_fois_in_string` | Population code unchanged since before 61ab4e3b; the range changed only its tokenization: S1. |
| `py/foi/foi_gray_marks.py` (new): `_collect_labels`; `py/foi/foi_finals.py`: `_rm_html`, `_rm_html_single`, `_json_value` | Walk rendered HTML, not MAM data; outside this classification. |
| `py/near_aleppo/census/adonai_census.py`, `divine_name_split.py`, `stress_helper_census.py`: `render`; `qamats_params.py`: `render`, `find`; `nusach_aleppo_readings.py`: `each_nusach`, `flatten`, `clauses`; `template_inventory.py`: `main.walk_raw`, `main.walk_settled`; `edition_projection.py`: `_EDITION_KEYS`, `_EDITION_KEYSETS` | Fixed in the range: each walker raises on a mapping that is not a template (`4e9e7b84`, 2026-10-21), closing the 2026-10-07 latent item 3. `clauses` reads note prose through phase 3's `_clauses` (2026-10-08). The silluq template projects to parameter 1, its key set declared from the template's contract. |
| `py/near_aleppo/phase6_flags.py`: `_matching_templates` | Fixed: raises on a template with no phase-2 rule and on a phase-2 action it does not name (`4e9e7b84`). `Flags._walk` seen again. |
| `py/near_aleppo/phase2_templates.py`: `Resolver._template`, `_sequence`, `_kept`, `_RULES`, `selected_keys`, `carriers_text`; `py/py_misc/orphan_marks.py`: `carriers`, `validate_space`, `validate_body` | Closed dispatch: the silluq template dissolves to parameter 1 and joins `TEMPLATES_ABSENT_FROM_DATASET`; the near-Aleppo body templates raise in MAM's text; the carrier validators are closed. `_flatten`, `_contains_mark`, `_assert_no_marks`, `_assert_marks_flattenable`, `_replace_marks` and `assert_templates_absent` seen again. |
| `py/near_aleppo/phase3_policies.py`: `Policies._template`, `Policies._value` | Closed dispatch; the change recognizes one reviewed note at 1 Kings 8:11 by verse and exact text. `_selected_text`, `_holds_template` and `_longest_matchings` seen again. |
| `py/near_aleppo/qere_without_ketiv.py` (new): `BodyEncodings.apply.walk`, `BodyEncodings.apply.expand` | Closed transformation over phase 2's rules: it enters only `phase2.selected_keys` of notes and ketiv/qere templates ("excluding note bodies and apparatus alternatives") and raises on an unknown or unresolved template. |
| `py/near_aleppo/ketiv_checks.py` (new): `check_e_cell`, `_check_value` | Structural lint entering only note targets; `phase2._RULES[name]` raises on an unknown name; a ketiv/qere template is checked where it stands. |
| `py/near_aleppo/doc_figures.py`: `_walk`, `_walk.enter`, `_special_letter_word_1` | Zone-classified walk; the change validates the body-space template and confines it to dataset text. `_rename_back`, `_templates.visit` and `_characters.visit` seen again. |
| `py/near_aleppo/doc_note_review.py`: `inventory`, `check`; `py/near_aleppo/main_build.py`: `build` | A call cycle of build orchestration, not a data walker: `build` calls `check`, whose `inventory` calls `build(bake_notes=False)`. `_data_notes.walk` seen again. |
| `py/near_aleppo/features_of_interest.py` (new): `_verses`, `_rubies`; `foi_spacing.py` (new): `_chunks`, `_atoms`, `resolved_examples`, `counts_by_family`; `foi_qere_without_ketiv.py` (new): `_qere_nodes`, `_text`, `mam_examples`, `_naee_excerpt.projection`, `_naee_excerpt.cut`, `_validate_near_aleppo_encodings` | Walk the shared renderer's output, rendered with the edition mode's options or, in `mam_examples`, with MAM-with-doc's and the stress-helper form stated. Notes are separated by `mam_doc_utils` before any search; `_chunks` and `_naee_excerpt` raise on an unexpected tag or role. `_validate_crop` walks crop records, not templates. |
| `py/near_aleppo/doc_changes.py` | Screen false positive (a parameter named `section`); page assembly. |
| `py/accgram/mam_poetic_accents.py`: `_walk`, `_walk_kq`, `_verse_events`, `_iter_verse_nodes` | Closed event projection of MAM-simple: the qere only, a gray maqaf read as a maqaf (Ben, 2026-10-20), a silluq annotation read with the sof pasuq after it. Closed further on 2026-10-21 (`67237cdb`): an unclassified ketiv/qere child raises, and verses come through `mam_simple_json.verses`. |
| `py/accgram/mam_simple_verse.py`: `_mam_simple_fragments`, `_mam_simple_kq_qere_fragments`, `load_mam_simple_for_refs`, `string_vels` | Named text projection whose strand the caller chooses; a dual-cantillation node with other children and an unclassified ketiv/qere child raise (`67237cdb`); silluq annotations come from the qere and `cant-alef` stream, as the docstring says. `_iter_dict_nodes`: L5. |
| `py/accgram/post_stress_meteg_sources.py`: `_post_silluq_source_annotations`, `_written_stress_helpers` | Declared: annotations from the qere and `cant-alef` projection; `_written_stress_helpers` indexes top-level stress helpers and descends into no template, as before. |
| `py/accgram/breuer_word_length.py`: `tree_leaves.walk`, `zaqef_realms.walk`; `dual_cant_detangle.py`, `prose_run.py`: `_tree_has_error`; `rtms_report.py`: `_leaf_node_name_counts`; `fix_apply.py`: `_collect_unit_setters`; `maqaf_nonfinal_accents.py`: `_mam_simple_gray_maqafs_by_verse.walk`, `uxlc_text`; `rtmsr_sat.py`: `render_sat_value`, `_render_token_like_dict` | Seen again: parse-tree, WLC and UXLC walkers, and the RTMS display, whose population remains deferred decision 9. |
| `py/explicit_xataf/extract.py`: `flatten_text`, `flatten_arg1_strings`; `find_docnote_tmpls`, `join_arg1_strings` | Closed. A separator gives a space (`3dbad806`, 2026-10-21); the silluq template gives parameter 1; `flatten_arg1_strings` passes each template through `join_arg1_strings`, so an unknown one raises (`4e9e7b84`). The two inventories are seen again. |
| `py/verify_mp/corpus.py`: `iter_template_objects`; `py/verify_mp/verifiers_templates.py`: `verify_mp_plus_templates_silluq_before_meteg_cases` (new), `_iter_template_occurrences_with_ancestors` | The structural iterator raises on any node other than a string, a list or a template (`4e9e7b84`); the new verifier is a declared all-column inventory of the template's calls; the ancestor iterator is seen again. |
| `py/versification_and_cantillation/strands.py`: `_el_text`, `_word_template_text` | The silluq template joins the parameter-1 arm; a separator gives a space (`46dfd37f`); the page's projection remains deferred decision 7. |
| `py/versification_differences/hebrew.py`: `_flatten_wtseq`, `_flatten_wtel`, `_recurse_on_keys` and its three callers, `_hnd_return_space`; `py/py_misc/wt_qere.py`: `HANDLERS` | Alternatives are set apart by a space and a narrow-sense paseq gives a space (`46dfd37f`); which alternatives a label reads remains deferred decision 4. The first stage, `wt_qere.HANDLERS`, reads the silluq template's parameter 1. |
| `py/ws/ws_plain.py`: `_element`, `_sequence`, `_is_spacing_template` | Raw parser-stage conversion, lossless structural recursion that claims no Scripture; the change keeps the space after an inverted nun. |
| `py/diff_ctr_vs_mam/massage_mpu_verse.py`: `_massage_mpu_wtseq`, `_massage_mpu_ep_wtel`, `_massage_arg_1` | Seen again; the closed table gained the silluq template's parameter 1. |
| `py/hbce_psalms/compare.py`: `hbce_tokens`, `mam_children_tokens` | Closed readers ported to JSON; a mark with no chanted word before it now raises, on MAM's side and on HBCE's (`a24e81a9` and `ceb9c197`, 2026-10-21). The frozen `hbce-psalms/out/` is not rerun, by Ben's decision of 2026-09-26. |
| `py/py_misc/mam_doc_utils.py`: `_does_not_need_callout`, `_has_pointed_string_within`; `py/py_misc/ren_html_for_renel.py`: `html_for_ren_el` | Render-element processing; the callout check now enters the near-Aleppo ruby box, and `_has_pointed_string_within` tests for a letter directly (`3a1bbe34`). `extract_docs`, `mark_doc_targets` and `_pointed_sum` seen again. |
| `py/mb_misc/hebrew_letter_words.py`: `letters_and_maqafs` | Closed character dispatch (`3a1bbe34`): a gray maqaf is a maqaf, edge punctuation is allowed only at either end, any other character raises. |
| `py/tmpl_survey/nesting_normal_form.py`: `_grammar_edges_and_order`, `RANK_GROUPS_FOR_PLUS_E` | Nesting grammar: two declared edges for the silluq template. |
| `py/intro_doc_audit/census_scope.py` (new): `selected_parts`, `selected_template_paths`; `all_books_hataf.py`: `selected_text`; `poetic_rosters.py`: `selected_leaves`; `structures.py`: `main.walk` | The near-Aleppo edition projection through `edition_parameter_keys_for`, closed by name and measured key set; a separator gives a space (`418e1304`). The labels these outputs give the projection: C1. |
| `py/intro_doc_audit/deuter_hataf_scope.py`: `templates`; `all_books_hataf.py`: `parameter_words` | Validated whole-structure template inventory that records a JSON pointer for each template and reports ketiv and qere apart. In Deuteronomy's column E the nested ketiv/qere templates are four, all in note targets (measured). |
| `py/intro_doc_audit/audit.py`: `inventory_notes`, `object_address` | Note inventory through `find_docnote_tmpls`; target text through `flatten_text`, recording that function's error instead of raising for the 35 notes whose target holds a מ:פסוק. C1. |
| `py/intro_doc_audit/human_review.py`: `strings_in` (in `applied_row`) | Maximal string search in one note object, for a check that raises on any occurrence without a declared context. |
| `py/intro_doc_audit/history_inventory.py`: `dictionaries`; `human_review.py`: `prose`; `history_batch2.py`: `physical_argument`, `note_templates` | The first two walk the audit's own records and prose; the last two are a raw Wikisource parse layer that finds נוסח calls by name in historical revisions. |
| `py/intro_doc_audit/review.py`: `source_node` | Uncalled: L6. |
| `py/miqra_mevoar/mam_simple.py` (new): `_projected`, `_holds_break`, `verse_breaks` | `_projected` is closed (an unknown element raises) and keeps a ketiv and its qere both, for a comparison of letters, as its module docstring says; `_holds_break` is a raising structural guard. |
| `py/author_misc/mam4sef_survey.py` (new): `_nodes`, `_silluq_cases`, `listing_entries` | `_nodes` is an annotation inventory with closed dispatch on the Sefaria handlers' keys; `listing_entries` re-derives the Unicode-name listings, a serializer. |
| `py/tests/test_mam_json_verses.py`: `_selected_parts`; `test_israel_bible_review_mam_forms.py`: `_text`, `_own_text`; `test_sefaria_silluq_documentation.py`: `_inventory`; `test_uni_norm_fragile_harfbuzz.py`: `_strings`; `test_mpplus_alternative_oracle.py`: `_scripture`, `_source_roles.traverse` | An independent oracle of the reader's declared nodes; a closed oracle that states side and strand for each row and raises on a dual cantillation without a strand; a declared annotation inventory; a declared maximal string inventory for a differential test; seen again with the silluq role added. |
| `py/sigils/inventory.py`: `_note_node_to_text`; `py/phonetic_mam/display_schema.py`: `validate_tokens`; `py/phonetic_mam/renderer.py`: `_tokens`; `py/py_misc/mwd_utils.py`: `_length_of_renel`, `_shrink_join`; `py/render_wt/render_wikitext_handlers.py`: `_equal`; `py/render_wt/render_wikitext_kq.py`: `_pointing_display_order`; `py/near_aleppo/phase5_readings.py`: `_walk`; `py/near_aleppo/doc_pages.py`: `_route_links` | Seen again. |

**Excluded, with reasons.** Not MAM or Wikisource consumers: `py/pen_stroke/` and
`py/concrete_transcription/` (glyph geometry and manuscript images); `py/taamey_d/`,
`py/taamey_d_build/` and `Taamey-D/font-m-TaD/` (the font's build, checks and pages;
`qa/corpus_refresh.py` reads the word lists `out/mam-qere-words.json` and
`uxlc/out/uxlc-words.json`, not templates); `py/mb_cmn/polite_download.py` (robots rules and
redirects); `py/repo_util/` and `py/redirect_stubs/`; `py/clc/`, `py/main_clc_ruby_review.py`,
the UXLC and WLC readers (`py/uxlc_*`, `py/py_wlc*`, `py/accgram/uni_to_marks.py`,
`chanted_word_accents_units.py`, `maqaf_nonfinal_accents.py`'s `_wlc_*`, closed on 2026-10-21 by
`ceb9c197`); `py/yeivin_itm/renderer.py` (the ITM adaptation). Not data walkers: HTML authoring
and output (`py/author_site/site_index.py`, `py/mb_misc/mb_html.py`, `py/mb_misc/write_utils.py`,
`py/author_misc/mp_cmn_dedicated_rows.py`, `py/author_misc/mam4sef_common.py`'s lints over the
generated page, `_text_of` in `py/author_boj_util/author.py` and `py/mb_author/author.py`,
`py/miqra_mevoar/docx_table.py`, `py/tests/test_hebrew_letter_spacing.py`), Python-source lints
(`py/tests/test_mega_coverage.py`, `py/tests/test_sibling_reach.py`),
`py/tests/test_uxlc_misc_fixed.py` (UXLC XML), the Wikisource bot's `py/subcommands/ws_bot_*.py`
(loops over its own specification records) and `py/phonetic_mam/compute.py` (`_phrase` reads a
named protocol field).

**C1. The Introduction audit's outputs call a pointed-ketiv projection "qere".** **Disposition: confirmed; this read-only audit left it unfixed, and `eb52ecd5` fixed it on 2026-11-12, by Ben's option A.** Restating the labels to say what
is selected would choose no new policy; choosing another branch is Ben's decision.

- **Callers.** `py/intro_doc_audit/audit.py`: `inventory_notes` writes each note's
  `target_survey_text` with `explicit_xataf.extract.flatten_text` and the
  `target_projection_notice` "Existing hataf survey projection: qere and primary stress only;
  …". `py/intro_doc_audit/structures.py`: `main` writes the `projection` field "Existing
  edition_projection: qere, primary stress, qamats ד, combined cantillation; …", which
  `catalogues.py` copies. `py/intro_doc_audit/census_scope.py`: `main` gives `two_atom_oleh` the
  predicate "Selected atom has OLE without MERKHA …; qere selected …".
- **Question.** The audit's evidence for the Introduction's claims: the text of each
  documentation note's target, and populations of templates and rare marks in the selected
  stream.
- **Branch included against the label.** For the trivial ketiv/qere template מ:קו״כ-אם-2 all
  three take parameter 1, the pointed ketiv: `flatten_text` through `_RETURN_ARG1_TMPL_NAMES`,
  the edition projection through `_EDITION_KEYS`, and the MAM-simple stream through
  `kq-trivial`, which `render_wikitext_handlers._handle_kq_trivial` fills from parameter 1. For
  כתיב ולא קרי both plus-based projections include the ketiv that is not read
  (`flatten_text` its parameter 2, the edition projection its parameter 1, which holds that
  ketiv in parentheses). The audit's own `doc/intro-doc-audit/METHODS.md` says that its "MAM qere
  labels identify the actual selected source".
- **Tracked outputs.** `doc/intro-doc-audit/notes.json`: 15 of its 3,905 records have a target
  holding a trivial ketiv/qere, so their `target_survey_text` is a pointed ketiv under a notice
  that says qere, for example line 4683, Genesis 13:3's ketiv with final he where the qere has
  vav; 2 more hold the unpointed ketiv of a כתיב ולא קרי. Both counts are the same at HEAD and at
  the audit's pinned source `89cb865729b0876f1fd32a8a3579eaec80b4fc0c`
  (`doc/intro-doc-audit/source-pin.json`). The `projection` field of
  `structural-populations.json`, `rare-mark-populations.json` and `catalogue-comparison.json`,
  and the `two_atom_oleh` predicate of `next-pass-census.json`.
- **Effect: none measured beyond the labels.** None of the 15 targets' ḥataf vowels differs
  between parameters 1 and 3. At all 149 trivial ketiv/qere templates in the edition
  projection's column-E stream, parameters 1 and 3 carry the same numbers of deḥi, ole, merkha,
  shalshelet, merkha kefula, qarney para, yerah ben yomo, telisha gedola, geresh and gershayim.
  All 8 כתיב ולא קרי calls in that stream, and both in note targets, are unpointed.
- **Reproduction.** Read `doc/intro-doc-audit/notes.json` line 4683 beside Genesis 13:3's מ:קו״כ-אם-2 call in
  `MAM-parsed/plus/A1-Genesis.json`.
- **Relation to earlier findings.** The same class as finding 1 of
  `doc/blind-dive-into-template-params.md`, in a consumer added after it; deferred decisions 7
  and 11 name other consumers and are not re-raised.
- **Put to Ben** on 2026-11-11, with S1 and S2.

**S1. The dual-mater FOI reads a scroll-difference note's prose.** **Disposition: settled on 2026-11-12 by Ben's option B, which keeps the row, in `d6a93d9c`; pre-existing**, unchanged in this range except for its
tokenization. `py/foi/foiz_wt_dual_ml_alef.py`: `_find_fois_in_string` drops a string only when
the stack's last label is `doc-part-n`, so its all-branch population also searches the note of
a targeted scroll difference (parameter 2 of מ:הערה-2, labelled `scrdfftar-note`) and the
strings of a template inside a documentation note's body. Its page explanations in
`py/foi/dml_an_explanations.py` state no population. Tracked evidence:
`gh-pages/MAM-with-doc/foi/foi-alef-dual-ml-alef-second.json` has one such row, Genesis 4:13 with
`stack_str` "scrdfftar-note", a form quoted in the note; it was already there at 61ab4e3b. The
other labelled row, Lamentations 1:12's special-letter word, is in a note's target. The label,
and `_NOTE_STACK_PARTS`'s naming of scroll-difference note parts, suggest the inclusion is
deliberate. **What would settle it:** Ben stating whether the two dual-mater pages survey
Scripture strings only or also forms quoted in scroll-difference notes; if only Scripture,
`py/main_foi_features_of_interest.py` regenerates the pages for the diff.

**S2. FOI fragments show deḥi and tsinnor by the renderer's default.** **Disposition: settled on 2026-11-12 by Ben's option A, MAM-with-doc's form in both cells, in `345a0332`; a display question that the range introduced.**
`py/foi/foiz_wt_kq_1.py`, `foiz_wt_slh_word.py` and `foiz_wt_rare_tmpls.py` render in
`_html_for_wtseq` with `handlers.default_hctx()`. A מ:דחי or מ:צינור inside such a fragment
therefore shows parameter 1, while MAM-with-doc's verse column has shown parameter 2 keeping
parameter 1's meteg since Ben's decisions of 2026-10-26 and 2026-10-27. Measured: 15
stress-helper templates in MAM-parsed-plus sit inside ketiv/qere templates (7 in כו״ק, 8 in
מ:קו״כ-אם-2), and none inside a special-letter word or a targeted scroll difference, so up to
15 rows of foi-kq-simple, whose first cell is "MAM's rendering of the template", differ from
MAM-with-doc's column. `foiz_wt_dexi_stress_meteg.py` states `RENOPTS_MAM_WITH_DOC` instead.
**What would settle it:** Ben deciding whether FOI renderings under `gh-pages/MAM-with-doc/foi/`
follow MAM-with-doc's stress-helper form; either way the three callers can state
`ro_stress_helper`, and `py/main_foi_features_of_interest.py --foi args-foi-kq-1
--single-threaded` would show the rows that change.

Latent items, recorded so that a later change cannot make them live unnoticed. Each describes
the code as the audit found it at `d957048a`, as the table above does. On 2026-11-12
`93eb8686` closed L1, L2, L3, L5 and L6, under Ben's instruction of 2026-10-21 quoted below,
without changing a tracked output; `345a0332` closed L4 later that day, after Ben's answers to S2 and L4:

1. **L1, closed: `py/foi/foi_wikitext_helpers.py`: `_add_templates_before_sof_pasuq`** recursed
   through `template_param_vals` into every parameter of every template and checked a template's
   name only where a sof pasuq followed it, so an unknown template elsewhere was entered without
   raising, which Ben's closed-dispatch rule asks a shared helper not to do. Nothing escaped:
   each of its four callers (`foiz_wt_kq_1`, `foiz_wt_qamats_var`, `foiz_wt_slh_word`,
   `foiz_wt_rare_tmpls`) then walks the same cell through `all_branch_foilers`, whose
   `_find_fois_in_wtel` validates every template. It now validates each template with
   `validate_current_plus_template` before entering its parameters, as `with_attached_marks`
   does.
2. **L2, closed: `py/mam_morphhb/morphhb_plus.py`: `plus_stream`** was closed by name but
   called no shape validator (`node.get("tmpl_params") or {}`); an added parameter of מ:דחי,
   מ:צינור, נוסח or מ:קמץ would have been discarded silently in MAM-morphhb, a distributed
   product. It now takes each template's parameters from `validate_current_plus_template`,
   which other readers of the same files call.
3. **L3, closed; carried over from `mam_xml_verses.py` at 61ab4e3b:
   `py/mb_cmn/mam_json_verses.py`: `get_verse_words`** passed over a `kq` with no `kq-k`, a
   `scrdfftar` with no `sdt-target`, a `text` child with empty text, an `slh-word` with an empty
   `slhw-desc-0` and a paseq-family child with no word before it. No current verse reached
   these branches: `py/tests/test_mam_json_verses.py`'s full-corpus differential
   `test_reader_atom_content_matches_selected_source_nodes_over_the_full_corpus` asserts each
   missing child and the word before a paseq-family mark. Each of those cases now raises, and
   every other child's shape is checked. Two cases give no word and are named: a `text` child
   holding only whitespace, of which there are 28, and a scroll-difference target that is empty,
   at Exodus 26:6 and Deuteronomy 27:19, or holds only a parashah break, at three sites.
4. **L4, closed on 2026-11-12 by `345a0332`: the stress-helper default.** `py/render_wt/render_wikitext_handlers.py`:
   `_STRESS_HELPER_FORMS` gives parameter 1 to a caller that sets no `ro_stress_helper`, and the
   comment above it declares that default as the renderer's behavior before the option existed.
   `py/mb_xml/xml_render.py`: `_RENOPTS_MAM_XML`, MAM-simple's call and through it MAM-OSIS's,
   MAM-for-Sefaria's and MAM-morphhb's, states cantillation (`rv-cant-all-three`) and qamats
   (`rv-dalet`) but not the stress-helper form, and MAM-simple's README and guides mention
   neither stress helpers nor the qamats choice (searched `MAM-simple/` outside its JSON and
   `gh-pages/MAM-simple/`). Output is unchanged by the range. Ben's rule asks each caller to
   state its stress-helper alternative. The S2 callers rely on the default;
   `py/tests/test_mpplus_latest_note_schema.py` renders no stress-helper template, so it needs
   no form. `93eb8686` removed the default and had MAM-simple's call and the three S2 callers
   state the form they showed; before it was pushed, the commit that records this put all six
   files it had changed for L4 back as they were. Stating any form in the three S2 callers
   would answer S2, which is Ben's question, and no recorded decision covers MAM-simple's form,
   so Ben was asked for it on 2026-11-12. L4 can close once both are answered.
5. **L5, closed; its recursion was unchanged until then: `py/accgram/mam_simple_verse.py`:
   `_iter_dict_nodes`** yielded every dictionary of a MAM-simple file wherever it stood, and
   its callers `load_mam_simple_for_refs` and `mam_simple_refs` passed over a verse whose
   osisID was not a string. The matching locator in `mam_poetic_accents.py`,
   `_iter_verse_nodes`, was closed on 2026-10-21 (`67237cdb`) through
   `mam_simple_json.verses`. It selected no text, so it could not project; it could only leave
   a malformed verse unread. Both callers now locate verses through
   `mam_simple_json.read_book_group` and `mam_simple_json.verses`, which raise on a node out of
   place, and they raise on a verse without an osisID.
6. **L6, closed: uncalled walker code.** `py/intro_doc_audit/review.py`: `source_node` had no
   caller (its only references were its own recursion); it serialized every parameter of any
   template without checking its name. It is deleted.
   `py/near_aleppo/census/nusach_aleppo_readings.py`: `collect` remains uncalled, kept as
   declared population code by Ben's decision of 2026-10-09; not re-raised.

**The 2026-10-07 latent item 3 is no longer present as described.** `4e9e7b84` ("Close the census,
phase-6, verify_mp, explicit_xataf and mam4sef walkers", 2026-10-21) made the four census `render`
functions, `qamats_params.find`, `nusach_aleppo_readings.each_nusach` and `flatten`, and
`template_inventory`'s `walk_raw` and `walk_settled` raise on a mapping that is not a template,
and made `phase6_flags._matching_templates` raise on a template without a phase-2 rule and on an
action it does not name, on Ben's instruction that day: "Close them all. Even if they are getting
away with it, they set a bad precedent."

Verification for this audit: none was owed beyond reading, since it changed nothing; the clone was
clean on `main` at `d957048a` before and after the review.

## Archived receipt references, 2026-11-11

Recorded by Claude (Opus 5.5) on 2026-11-11, New York time, after Ben approved the retirement that
day. The entry "The census reads note prose with phase 3's reader, 2026-10-08" says that
"`doc/PLAN-maintenance-follow-up-2026-10-08.md`, workstream A, carried it out", and the entry
"Archived receipt references, 2026-10-09" was recorded "in the cloud session that executed
workstream C of `doc/PLAN-maintenance-follow-up-2026-10-08.md`". The maintenance follow-up
plan has been retired from the tracked tree with its update. Both remain at
`462984bb567a6498fd4f2d7ef00e3186fcd00f02`: the archived
[maintenance follow-up plan](https://github.com/bdenckla/MAM-basics/blob/462984bb567a6498fd4f2d7ef00e3186fcd00f02/doc/PLAN-maintenance-follow-up-2026-10-08.md)
and its [update](https://github.com/bdenckla/MAM-basics/blob/462984bb567a6498fd4f2d7ef00e3186fcd00f02/doc/PLAN-maintenance-follow-up-2026-10-08-update.md).

## C1, S1, S2 and L4 were settled and carried out, 2026-11-12

Recorded by Claude (Opus 5.5) on 2026-11-12, New York time, during repository maintenance, by a
sub-agent of the session that owns its integration. The entry "The 2026-11-11 maintenance audit
found one mislabelled projection in new or changed walkers" put C1, S1 and S2 to Ben, and its
latent item 4 says that he was asked for MAM-simple's stress-helper form. He answered on
2026-11-12:

1. At 14:26 New York time he answered "Take my recommendations for decisions 3 to 6?" with "Yes,
   all four". Decisions 3, 4 and 5 were C1's option A, S1's option B and S2's option A.
2. At 14:23 New York time, in another session, he answered "Your answers to F1, L4 and L8: A or B
   each?" with "A for all three". Of the three, L4 is this record's: its option A is that
   MAM-simple states parameter 1, the form without the stress helper, which every MAM-simple
   release has shipped.

**C1, fixed by `eb52ecd5`.** Option A, "Correct the labels": "rewords the notes' notice, the
populations' projection field and the census predicate to say what is read: the qere, except a
trivial ketiv/qere's pointed ketiv and the unread ketiv of כתיב ולא קרי. Then regenerates.
Only label text changes." Each label now says what its own projection reads, taking the template
names from `py/mb_cmn/template_names.py` through two constants in `py/intro_doc_audit/audit.py`:

- `audit.py`, the `target_projection_notice` of `doc/intro-doc-audit/notes.json`:
  "Existing hataf survey projection: qere, except that a trivial ketiv/qere (מ:קו״כ-אם-2) gives its pointed ketiv and כתיב ולא קרי gives its unread ketiv; primary stress only; structural marks may be omitted, but every separator between two atoms, the gray maqaf included, gives a space. Use target_node for evidence."
- `structures.py`, the `projection` field of `structural-populations.json`, which
  `rare-mark-populations.json` and `catalogue-comparison.json` copy: "Existing edition_projection: qere, except that a trivial ketiv/qere (מ:קו״כ-אם-2) gives its pointed ketiv and כתיב ולא קרי gives its unread ketiv in parentheses; primary stress, qamats ד, combined cantillation; note target only. Structure counted before selecting its child. No note-body recursion and no all-parameters fallback."
- `census_scope.py`, the `two_atom_oleh` predicate of `next-pass-census.json`:
  "Selected atom has OLE without MERKHA, and the immediately following atom has MERKHA; qere selected, except that a trivial ketiv/qere (מ:קו״כ-אם-2, MAM-simple's kq-trivial) gives its pointed ketiv and כתיב ולא קרי (kq-k-velo-q) gives no atom; fragments reassembled, paseq tokens excluded from atom adjacency. This is a current MAM predicate, not a physical-manuscript count." The census's atoms come from MAM-simple through accgram's
  `mam_simple_verse`, which reads a `kq-trivial`'s text, the pointed ketiv, and gives a
  `kq-k-velo-q` a boundary and no text, so this label says that כתיב ולא קרי gives no
  atom.

The outputs keep the evidence pinned at `89cb865729b0876f1fd32a8a3579eaec80b4fc0c`, so the
generator ran in a scratch worktree of `df516a00` in which these inputs had their `89cb8657`
content: the five that `doc/intro-doc-audit/source-pin.json` pins, every blob checked against it,
and the three MAM-simple files that `census-scope` reads, whose blobs equal those of `fb566021`,
the commit that `next-pass-census.json` records for them. With the old code,
`py/main_intro_doc_audit.py`, run with no subcommand and with `structures`, `catalogues` and
`census-scope`, rewrote byte for byte all nine files those runs write. With the change, only the
labels changed: each of the 3,905 notices in `notes.json`, among them those of the 15 records
whose target holds a trivial ketiv/qere and of the 2 whose target holds a כתיב ולא קרי,
at 2 Kings 5:18 and Ruth 3:12; the `projection` field of the three population files; and the
census predicate. No count changed, and `py/main_intro_doc_audit.py review` rewrote its outputs
unchanged.

**S1, settled by `d6a93d9c`.** Option B, "Keep them, and say so": "keeps the row, and states
on both pages that spellings quoted in scroll-difference notes are included and labelled. It also
makes the documentation-note exclusion whole, so that the text inside a template in a note's body
is skipped too. No row changes." `py/foi/foiz_wt_dual_ml_alef.py`: `_find_fois_in_string` skips a
string wherever `doc-part-n` stands in its stack. `py/foi/dml_an_explanations.py`: the overall
explanation of both dual-mater pages gains the paragraph "Besides MAM's running text, including
the targets of documentation notes, this search reads scroll-difference notes, so a spelling
quoted in one is included, with scrdfftar-note in the last column of its row. The bodies of
documentation notes are not searched." Measured: the two pages gained that paragraph and nothing
else; their JSON is unchanged, 110 rows in `foi-alef-dual-ml-alef-first.json` and 684 in
`foi-alef-dual-ml-alef-second.json`, whose row 2 is still Genesis 4:13 with `stack_str`
"scrdfftar-note".

**S2, settled by `345a0332`.** Option A, "Follow MAM-with-doc in both cells": "the three
generators state MAM-with-doc's stress-helper option, the pqere policy takes the same form, and
the FOI pages are regenerated. 11 rows gain the stress helper, 4 of them in both cells."
`py/foi/foiz_wt_kq_1.py`, `foiz_wt_slh_word.py` and `foiz_wt_rare_tmpls.py` render their
fragments with the value of `ro_stress_helper` that `mwd_write_book.RENOPTS_MAM_WITH_DOC` states,
parameter 2 keeping parameter 1's meteg. In `py/hkq_cmn/qere_projection.py` a policy names the
forms of a stress-helper template that it reads in a validated field, `stress_helper_forms`,
which replaces `stress_helper_argument_keys` and raises on a name it does not know.
`FOI_KQ_SIMPLE_MAIN_COMPATIBLE_POLICY`, which gives foi-kq-simple's pqere cell, names parameter 2
keeping parameter 1's meteg and keeps its legarmeh setting; the other policies name the
parameters they read before. The renderer's code that checks the two parameters and derives that
third form moved to `py/mb_cmn/stress_helper_forms.py`, which the renderer and the policies share.
Measured by one run of `py/main_foi_features_of_interest.py` for S1 and S2 together:
`foi-kq-simple.json` keeps its 1,213 rows, and 11 of them gain a deḥi stress helper, in 15 cells:
the first cell, MAM's rendering of the template, of the seven כו״ק rows at Psalms 49:15, 74:6
and 77:20, Proverbs 24:17 and Job 16:16, 33:28 and 42:2, and both that cell and the pqere cell of
the four מ:קו״כ-אם-2 rows at Proverbs 6:13 and 26:24 and Job 27:15 and 38:41. These are all 15
stress-helper templates inside ketiv/qere templates in MAM-parsed-plus, each a מ:דחי, and in
none does parameter 2 lack a meteg that parameter 1 has, so no meteg is kept. No other FOI file
changed: no stress-helper template stands in a fragment of foi-slh-word or foi-rare-tmpls.

**L4, closed by `345a0332`.** `py/render_wt/render_wikitext_handlers.py`:
`_STRESS_HELPER_FORMS` has no default, so a caller that meets מ:דחי or מ:צינור without
stating `ro_stress_helper` raises. `py/mb_xml/xml_render.py`: `_RENOPTS_MAM_XML`, MAM-simple's
call, states "rv-without-stress-helper", Ben's L4 answer, and `MAM-simple/README.md` says that
MAM-simple gives the form without the stress helper. The renderer's other callers state their
forms already: MAM-with-doc, near-Aleppo's edition mode, `py/near_aleppo/foi_qere_without_ketiv.py`
and `py/foi/foiz_wt_dexi_stress_meteg.py`; `py/tests/test_mpplus_latest_note_schema.py` renders no
stress-helper template. Measured: in the mega that followed, the generators of MAM-simple, MAM-with-doc and
near-Aleppo changed no tracked file.

Checks: each of the three commits above had Black, `git diff --check` and a mark-order
check of every added line, and `py/main_test.py` over the files its message names: 5 passed for C1, and 69 passed
with 8 subtests for S1 and S2 together, the lints over published pages among them; Ruff passed
on the changed modules. After the last code change `py/main_0_mega.py` exited 0, 66 steps in
886 seconds, with no tracked change beyond these commits'; its `taamey-d-corpus` step reported
the refresh pending that needs Ben's baseline acceptance and that these changes do not cause.
`py/main_test.py` then gave 1449 passed, 5 skipped. The one hand-run generator rerun was
`py/main_intro_doc_audit.py`, as C1 above describes. MAM-OSIS, MAM-for-Sefaria and MAM-morphhb
read MAM-simple, which did not change, so their generators were not rerun; `hbce-psalms/out/`
stays frozen, and the Taamey D corpus was not refreshed.

This entry corrected seven passages of the entry "The 2026-11-11 maintenance audit found one
mislabelled projection in new or changed walkers" in place:

1. "S1 and S2 are suspected and need Ben's answers." now reads "S1 and S2 were suspected; Ben
   answered them, with C1, on 2026-11-12."
2. "on 2026-11-12 `93eb8686` closed five of them, and L4 stays open, as their list below
   records." now reads "on 2026-11-12 `93eb8686` closed five of them, and `345a0332` closed L4
   later that day, as their list below records."
3. C1's "**Disposition: confirmed, unfixed** (this audit is read-only)." now reads
   "**Disposition: confirmed; this read-only audit left it unfixed, and `eb52ecd5` fixed it on
   2026-11-12, by Ben's option A.**"
4. S1's "**Disposition: suspected, unconfirmed; pre-existing**" now reads "**Disposition:
   settled on 2026-11-12 by Ben's option B, which keeps the row, in `d6a93d9c`;
   pre-existing**".
5. S2's "**Disposition: suspected, unconfirmed; a display question that the range
   introduced.**" now reads "**Disposition: settled on 2026-11-12 by Ben's option A, MAM-with-doc's
   form in both cells, in `345a0332`; a display question that the range introduced.**"
6. The latent items' "without changing a tracked output; L4 stays open:" now reads "without
   changing a tracked output; `345a0332` closed L4 later that day, after Ben's answers to S2 and
   L4:".
7. Latent item 4's "**L4, open: the stress-helper default.**" now reads "**L4, closed on
   2026-11-12 by `345a0332`: the stress-helper default.**"
