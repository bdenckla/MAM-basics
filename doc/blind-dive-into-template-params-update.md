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
   `py/mb_cmn/plain_template_schema.py:validate_current_plain_template` checks every argument's
   identity as well as the argument count: against `_CURRENT_PLAIN_NAMED_ARGUMENT_IDENTITIES` where
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
pipeline was removed during the execution of `doc/PLAN-retire-google-sheet.md`. The survey and
documentation-verification paths named beside them remain current.

## The maintenance audit also found missing validation in dataset inventories

Fixed by Codex during the maintenance pass of 2026-09-28: the topmost-documentation-note
finder and the plain/plus stack-path lookup now validate recognized templates before recording
a result or recursing. This supplements the base review's passage “several closed shape
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
structural template predicate. Both walkers now validate names and shapes before matching or
recursing. The plain walker also validates the recognized custom-tag leaves. Stack discovery
retains every classified branch and the existing occurrence order, limits and verbose payloads.
The existing occurrence fixture was corrected to use a valid parameterless separator template.
Normal and verbose CLI results for `E/נוסח` match before and after in each dataset, and a
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
