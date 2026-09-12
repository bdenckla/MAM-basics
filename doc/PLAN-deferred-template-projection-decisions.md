# Deferred template-projection decisions

Status: Ben Denckla deferred only the semantic decisions under “Deferred
semantic decisions” on 2026-09-12. The decisions under “Decisions already
fixed” and the repairs under “Completed engineering repairs” were completed and
integrated into `main` on 2026-09-12. Do not implement or settle a deferred
semantic decision until Ben resumes the review and makes that decision.

Focused Holman investigation: [MAM-basics #276](https://github.com/bdenckla/MAM-basics/issues/276).

## Repository and review state

The repository is `C:/Users/BenDe/GitRepos/MAM-basics`. The review was conducted
in the linked worktree
`C:/Users/BenDe/.codex/worktrees/36c2/MAM-basics` on branch
`codex-worktree-36c2`.

The proposal state immediately before the completion work was commit
`d9d17aceeb6b8f2b5a304bc755097dc63ffb8c08`. The proposal began from commit
`6982dcf5997b0cf75b32bfe032642c558e7de653`; `main` and `origin/main` were at
`ffc82f60588ddf0b0a7a8cef1b0fea293f15b641` before the completion work. These
commit identifiers describe the historical 2026-09-12 review state. A later
session must inspect current Git state and remeasure affected products rather
than assume that the repository has remained at these commits.

Before continuing the review, read these sources completely:

1. The live user instructions at `C:/Users/BenDe/.Codex/AGENTS.md`.
2. The Hebrew-prose skill at
   `C:/Users/BenDe/.agents/skills/hebrew-prose/SKILL.md`.
3. `doc/review-findings-2026-09-11.md`, which records the five current-state
   findings and their product reach.
4. This document, which records the settled and deferred semantic decisions.

The integrated code implements the decisions already fixed, the completed
engineering repairs, and an explicit `main`-compatible policy for every deferred
consumer. The integrated generated artifacts therefore contain no unapproved
semantic proposal. The remaining consumer-specific decisions below must be made
before an explicit `main`-compatible policy is replaced.

## Decisions already fixed

Do not reopen these decisions while resuming the deferred review:

1. The change-log renderer distinguishes body Scripture from documentation-note
   text. Documentation-note text may quote Scripture, but it remains
   documentation-note text.
2. Documentation-note rendering retains special-letter wrappers and their inline
   content. The retained handling includes `מ:לגרמיה-2`, `מ:פסק`, and link
   templates.
3. The trivial `מ:קו״כ-אם-2` rows in the qere-word-list artifact retain the
   historical parameter-1 pointed ketiv. The review rejected changing those rows
   to parameter 3.
4. `out/mam-qere-words.json` retains its maximal policy for non-ketiv/qere
   alternatives: both parameters of `מ:דחי` and `מ:צינור`; both `ד` and `ס` of
   `מ:קמץ`; and `כפול`, `א`, and `ב` of `מ:כפול`. Nontrivial ketiv/qere templates
   contribute the qere. This qere-word-list decision does not establish policy
   for any other consumer.
5. The sigil prose-token scan retains the new pointed-Hebrew filter.
6. Expression-token splitting discards punctuation-only remnants left after the
   pointed-Hebrew filter. This is behavior 2 from the 2026-09-12 review.
7. The xataf-qamats FOI survey uses parameter 1 only for `מ:דחי` and `מ:צינור`.
8. The xataf-qamats FOI survey continues to exclude the body of `מ:קמץ`. The
   rejected proposal would have changed the artifact from 339 rows on `main` to
   620 rows; the retained exclusion produces 338 rows after the parameter-1-only
   stress-helper decision. Re-establish the current count by running, from the
   selected MAM-basics checkout:

       C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_foi_features_of_interest.py --foi args-foi-qamats-var --single-threaded

9. The 66 poetic stress-helper FOI rows retain the new parameter identifiers in
   their provenance fields. Re-establish the current artifact by running, from
   the selected MAM-basics checkout:

       C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_foi_features_of_interest.py --foi args-foi-poetic-sh --single-threaded

10. The Goerwitz-page glossary remains limited to codes that the page renders.
11. The decnreub proposal selects parameter `ד` only inside `מ:קמץ`. The proposal
    writes 157 rows rather than the 159 rows on `main`. Re-establish the current
    proposal count by running, from the selected MAM-basics checkout:

        C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_decnreub.py

12. The Holman table verifier keeps the parameter-1 pointed-ketiv behavior that
    is on `main` until the row-level investigation in MAM-basics #276 establishes
    the Holman table's required projection. Ben's working hypothesis is that most
    or all affected Holman rows concern ketiv/qere, which makes this decision
    sensitive. The investigation must test the hypothesis row by row.

## Deferred semantic decisions

### 1. Multimark survey population

Consumer and searchable anchor:
`py/multimark/multimark_1.py:get_raw_data_wt` and the handlers for `מ:דחי`,
`מ:צינור`, `מ:קמץ`, and `מ:כפול`. The entry point is `py/main_multimark.py`.

The reviewed proposal used parameter 1 for `מ:דחי` and `מ:צינור`, parameter `ד`
for `מ:קמץ`, and parameter `כפול` for `מ:כפול`. The integrated code instead
preserves the earlier population explicitly: parameters 1 and 2 of the two
stress-helper templates, `ד` and `ס` of `מ:קמץ`, and `כפול`, `א`, and `ב` of
`מ:כפול`.

Ben must decide whether this survey measures one coherent selected Scripture
stream or inventories explicit alternatives. The decision has three independent
parts:

1. For `מ:דחי` and `מ:צינור`, select parameter 1 only, inspect both parameters as
   separate alternatives, or inspect both parameters and deduplicate identical
   survey rows.
2. For `מ:קמץ`, select `ד`, select `ס`, or inspect both as separate alternatives.
3. For `מ:כפול`, select `כפול`, inspect `א` and `ב` separately, or inspect all
   three declared representations.

The 2026-09-12 exploratory measurement found that adding stress-helper parameter
2 adds many duplicate occurrences but only one distinct multimark row; adding
both qamats alternatives added duplicate occurrences and no distinct row; and
using only `א` or only `ב` removed many rows from the combined-cantillation
proposal. Those observations are not a decision and came from an ignored
throwaway measurement script. Recreate the comparison from the current corpus
before Ben decides. After a decision, regenerate all multimark artifacts with:

    C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_multimark.py

Read the diffs in `out/mam-multimarks-raw.json`,
`out/mam-multimarks-full.json`, `out/mam-multimarks-ch.json`, and
`out/mam-multimarks-gch.json` as the differential test.

### 2. Holam-he qere-ending search population

Consumer and searchable anchors:
`py/hkq_cmn/qere_projection.py:project_qere_atoms`,
`py/hkq_cmn/qere_projection.py:qere_arg_key_for_template`, and
`py/hkq_cmn/qere_ending_search.py`. The entry point is
`py/main_search_holam_he_qere.py`.

The reviewed proposal selected parameter 3 of trivial `מ:קו״כ-אם-2`, parameter
1 of `מ:דחי` and `מ:צינור`, parameter `ד` of `מ:קמץ`, and parameter `כפול` of
`מ:כפול`. The integrated code instead preserves the earlier population
explicitly: trivial parameter 1, both parameters of the stress-helper templates,
both qamats alternatives, and all three declared representations of `מ:כפול`.
Documentation parameters remain excluded.

Ben must decide whether the search follows one coherent qere Scripture stream or
searches explicit alternatives as separate forms with a stated deduplication
policy. The maximal qere-word-list decision does not answer this search-specific
question. The completed fragment-tokenization repair joins adjacent projected
fragments before it identifies words and preserves combined source metadata.
After a decision, regenerate `holman/out/holam_he_qere_report.json` with:

    C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_search_holam_he_qere.py

The report regenerated during completion retained the previous hit population;
only its policy notes changed. Review every resulting difference before
committing a later population change.

### 3. Phonetic-MAM stream used by the Breuer word-length survey

Consumer and searchable anchors:
`py/accgram/breuer_word_length.py:_flatten`, `_qamats_branch_labels`, and
`load_phonetic_book`. The entry point is the
`survey-breuer-zaqef-units` subcommand of `py/main_accgram.py`.

The earlier behavior concatenated alternative branches into one form, which is
not a valid representation of one Scripture stream. The reviewed proposal
selected `qamats-dal` and `cant-alef`. The integrated code validates the named
branches and preserves the earlier concatenation explicitly until Ben chooses a
replacement. Rejecting concatenation does not choose its replacement. Ben must
decide:

1. whether Phonetic MAM uses `qamats-dal`, `qamats-sam`, or separate results for
   both qamats alternatives; and
2. whether the survey uses `cant-alef`, `cant-bet`, or separate results for both
   cantillation strands.

After a decision, run the survey from the selected MAM-basics checkout:

    C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_accgram.py survey-breuer-zaqef-units

The survey writes `.novc/breuer-zaqef-units.json`; compare the entire result with
a run from the chosen baseline.

### 4. Hebrew range labels for versification differences

Consumer and searchable anchors:
`py/versification_differences/hebrew.py:_flatten_wtel` and `_HANDLERS`.

The reviewed proposal used the qere of nontrivial ketiv/qere templates;
parameter 1 of trivial `מ:קו״כ-אם-2`; parameter 1 of `מ:דחי` and `מ:צינור`;
parameter `ד` of `מ:קמץ`; and parameter `כפול` of `מ:כפול`. The integrated code
validates every recognized template and explicitly preserves the earlier
all-branch traversal. The range label later retains letters and maqafs.

Ben must decide whether a range label follows one selected Scripture stream or
requires all explicit alternatives to produce the same label. Ketiv/qere
consonants and dual-cantillation maqaf grouping can change a label. Stress-helper
and qamats alternatives may currently disappear during label cleanup, but that
current output equivalence does not establish the semantic contract.

Before implementation, locate every caller of `range_label_for_minirow`,
`range_label_for_minirow_span`, and `range_label_for_wtseq`. Regenerate the
caller-owned products and treat their complete diffs as the test.

### 5. Double-meteg FOI dual-cantillation population

Consumer and searchable anchor: `py/foi/foiz_wt_mtgmtg.py:FOILERS`.

The reviewed proposal used parameter `כפול` of `מ:כפול`. The integrated code
validates the template and explicitly preserves the earlier traversal of all
declared representations. Ben must decide whether the double-meteg survey uses the
combined-cantillation representation, inventories `א` and `ב` separately, or
inventories all declared representations with an explicit deduplication policy.
This FOI decision is independent of the quick-brown FOI decision because the two
surveys ask different questions.

After a decision, regenerate the focused FOI artifacts with:

    C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_foi_features_of_interest.py --foi args-foi-mtgmtg --single-threaded

### 6. Quick-brown FOI dual-cantillation population

Consumer and searchable anchor: `py/foi/foiz_wt_quick_brown.py:FOILERS`.

The reviewed proposal used parameter `כפול` of `מ:כפול`. The integrated code
validates the template and explicitly preserves the earlier traversal of all
declared representations. Ben must decide whether the quick-brown survey uses the
combined-cantillation representation, inventories `א` and `ב` separately, or
inventories all declared representations with an explicit deduplication policy.
Do not copy the double-meteg FOI decision into this consumer without deciding that
the quick-brown survey asks for the same population.

After a decision, regenerate the focused FOI artifacts with:

    C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_foi_features_of_interest.py --foi args-foi-quick-brown --single-threaded

### 7. Versification-and-cantillation page Scripture projection

Consumer and searchable anchors:
`py/versification_and_cantillation/strands.py:_el_text` and
`py/versification_and_cantillation/strands.py:_word_template_text`.

The reviewed proposal described a qere projection but selected parameter 1, the
pointed ketiv, from trivial `מ:קו״כ-אם-2`. The reviewed proposal also selected
parameter 1 from `מ:דחי` and `מ:צינור`, parameter `ד` from `מ:קמץ`, and the
strand selected by the surrounding page logic from `מ:כפול`. The integrated
code validates every recognized template and explicitly preserves the earlier
page behavior until the complete page-specific projection is decided.

No example currently rendered on the page exposes the trivial ketiv/qere
difference. Ben must decide the page's complete projection contract rather than
allow the current examples to decide by absence. The page may need the qere, the
ketiv, or an explicit alternative treatment. The stress-helper and qamats choices
also require approval as parts of the same page-specific contract.

After a decision, regenerate the page through its owning authored-page entry
point and inspect the complete HTML diff. Locate the owning entry point from the
current callers of `build_columns` and `gather_examples`; do not guess a command
from the module path.

### 8. Punctuation in the `foi-kq-simple` `pqere` field

Consumer and searchable anchors:
`py/foi/foiz_wt_kq_1.py:_record_kq_as_foi` and
`py/foi/kq_trivial_types.py:pointed_qere_text`.

The reviewed proposal preserved the paseq/legarmeh glyph from a nested
`מ:לגרמיה-2` in the `pqere` field of the Psalms 10:5 row. The integrated code
explicitly preserves the earlier field value without that glyph. Ben must decide
whether `pqere` means the exact pointed qere including an adjacent separator or
the pointed qere without that separator. The decision must name the broad glyph
as paseq/legarmeh unless the grammatical reading has been established.

After a decision, regenerate the focused FOI artifact with:

    C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_foi_features_of_interest.py --foi args-foi-kq-1 --single-threaded

Inspect `gh-pages/MAM-with-doc/foi/foi-kq-simple.json` and the corresponding HTML
artifact.

### 9. RTMS Scripture projection

Consumer and searchable anchors:
`py/accgram/rtms_token_like.py:text_from_one_token_like` and
`texts_from_token_like_payload`, together with the callers in `py/accgram/rtms_*.py`.

The reviewed proposal included fields classified as `text` or `word` and
excluded fields classified as `note`, `notes`, or `tag="x"`. The integrated code
validates the known structure and explicitly preserves the earlier traversal,
including the text of `tag="x"` records. Output equivalence does not approve the
semantic contract.

Ben must decide which explicitly named RTMS fields are Scripture and which are
documentation. After a decision, retain closed dispatch for the field names and
fail on an unrecognized field rather than recurse through an unknown structure.
Regenerate every RTMS-owned product reached by the callers and inspect the full
diff.

### 10. Internal documentation-link contract

Consumer and searchable anchors:
`py/mb_diff_mpu/mpplus_docnote.py:_render_template` and `_plain_link_target`.

The documented contract says that parameter 1 of `מ:קישור פנימי בהערה` is a
Wikisource-internal target requiring the `https://he.wikisource.org/wiki/` base.
The current corpus has relative Wikisource targets in Proverbs and Job and an
absolute Archive.org URL in a Leviticus call to the internal-link template.
The integrated renderer validates the argument shape, renders parameter 1 as the
link text, and preserves the earlier absence of an `href` until Ben chooses the
contract. External documentation links render as links under the settled
documentation-note decision.

Ben must choose one of these contracts:

1. Enforce the documented strict contract: prefix internal targets with the
   Wikisource base and change the Leviticus call to the external-link template.
2. Define a permissive internal-link contract that prefixes relative targets but
   leaves absolute URLs unchanged, then document that contract explicitly.

After a decision, regenerate the MAM-with-doc change-log artifacts and inspect
every changed `href`. No current change-log report reaches these three calls, so a
zero diff does not remove the need for closed validation of the source calls.

### 11. Holman table projection for trivial ketiv/qere templates

Consumer and searchable anchor:
`py/hkq_cmn/mam_plus_verse_data.py:_collect_text_fragments` in the
`מ:קו״כ-אם-2` arm.

Ben deferred this decision and instructed that the behavior on `main` remain
unchanged. MAM-basics #276 contains the row-level investigation plan. Do not
replace parameter 1 with parameter 3, or add both as separate alternatives,
until the evidence in #276 establishes what the Holman table asks the verifier
to find. Do not generalize the eventual Holman decision to the qere-word list,
the holam-he search, or any FOI survey.

## Completed engineering repairs

The following repairs were completed without selecting a deferred Scripture
stream:

1. `py/hkq_cmn/qere_projection.py:word_atoms_from_qere_atoms` joins adjacent
   projected text fragments before tokenization and preserves combined source
   information. The regenerated holam-he report retained its previous hit set.
   `doc/review-findings-2026-09-11.md`, Finding 2, records the affected examples
   and measured reach.
2. `py/mb_cmn/plain_template_schema.py:validate_current_plain_template`
   validates the exact required and allowed argument identities as well as the
   argument count. Finding 4 records the affected consumers.
3. Existing shape validators now run before parameters are selected, flattened,
   or discarded in `py/mpplus/mpplus_boring_tmpls.py:evaluate`,
   `py/hkq_cmn/mam_plus_verse_data.py:_collect_text_fragments`,
   `py/versification_and_cantillation/strands.py:_el_text`, and the nested
   traversal in `py/decnreub/decnreub_for_one_cant.py`. Finding 5 records the
   product reach.
4. The internal documentation-link handler validates its current shape without
   choosing a target contract. The strict-versus-permissive target decision
   remains deferred under “Internal documentation-link contract.”
5. The affected artifacts were regenerated through their owning entry points,
   and the repository mega run verified the integrated tree. The restored
   `main`-compatible policies kept unresolved proposals out of the generated
   artifacts.

## Expected non-changes

1. Do not change any settled decision listed above while implementing a deferred
   decision for a different consumer.
2. Do not change the parameter-1 Holman table behavior on `main` before the
   investigation in MAM-basics #276 is complete.
3. Do not broaden the maximal qere-word-list policy into another consumer without
   a separate decision for that consumer.
4. The deferred decisions primarily reach supplemental or internal products. No
   decision in this document by itself authorizes a change to MAM-parsed-plus,
   the core MAM-simple XML/JSON datasets, or the MAM-with-doc edition pages.
5. The shape-validator repair in `py/mpplus/mpplus_boring_tmpls.py` has flagship
   blast radius but should be output-neutral for the current valid corpus. Any
   flagship artifact change after that repair is a finding that must be
   explained before integration.

## Procedure when Ben resumes the review

1. Verify the exact checkout with `git rev-parse --show-toplevel`, `git rev-parse
   HEAD`, `git branch --show-current`, and `git status --short`. Start from a
   current checkout of `main` that contains this document; do not resume from the
   historical proposal commit named above.
2. Read current `main`, inspect ancestry, and review intervening changes. Do not
   rebase or rewrite history. Preserve one writer per checkout.
3. Re-establish the current generated baseline before editing. Use the real entry
   points named above and treat any mismatch with tracked artifacts as a finding.
4. Present one consumer decision at a time to Ben, with the current behavior,
   alternatives, affected products, and freshly measured differential effects.
   Do not implement a deferred policy before Ben chooses it.
5. Implement each chosen policy as an explicit, consumer-specific dispatch. Name
   every recognized template and validate the exact shape before selecting or
   discarding parameters.
6. Run Black at its defaults on every changed Python file, using the primary
   clone's interpreter from the worktree:

       C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m black <changed Python files>

7. Run each affected generator, inspect the complete generated diff, and commit
   only explained changes on the worktree branch.
8. Immediately before archival, follow the MAM-basics worktree integration rule:
   merge `main` into the worktree branch, run
   `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py`
   from the worktree, commit every explained generated change, fast-forward the
   primary clone's `main` to the verified worktree branch, and push `main`.
