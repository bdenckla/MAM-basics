# Findings of the 2026-09-11 current-state review of template projection

State: five open findings.

The reviewed state is MAM-basics commit
`73c6b1137777ad1a522949fcea290f8ac1f87a7b`. The review treats the code at that
commit as the subject. It concentrates on template projection, template-shape
validation, and the generated products reached by those paths.

## Product-impact terms

- **Flagship products** are the `MAM-parsed/plus/*.json` dataset, the core
  `MAM-simple` XML and JSON datasets, and the edition pages generated under
  `gh-pages/MAM-with-doc/`.
- **Supplemental published products** are authored analysis or explanatory pages
  and the MAM-with-doc change log.
- **Internal products** are tracked analysis JSON, survey JSON, DOT files, and
  proposed-edit files that are not themselves published editions.

## Finding 1: two qere-selected paths take the pointed ketiv of a trivial-qere template

Finding type: category 2 — behavior was implemented that should not have been
implemented.

`py/hkq_cmn/qere_projection.py:qere_arg_key_for_template` identifies parameter 3
of `מ:קו״כ-אם-2` as the pointed qere. Two other paths describe their result as a
qere projection but take parameter 1:

- `py/hkq_cmn/mam_plus_verse_data.py:_collect_text_fragments`, in the
  `מ:קו״כ-אם-2` arm near line 277;
- `py/versification_and_cantillation/strands.py:_el_text`, in the
  `tmpln.TRIVIAL_QERE` arm near line 89.

The current MAM-parsed-plus corpus has 133 verses containing this template.

### Products reached by finding 1

The `mam_plus_verse_data.py` path reaches these specialized Holman products:

- `holman/docs-not-served/table_data.json` and the published
  `gh-pages/holman/table_data_findings.html` page through
  `verify_table_words_in_mam_plus.py`;
- `holman/docs-not-served/mam_suggestions.json` through
  `verify_mam_suggestions.py`;
- the internal `holman/out/final_hiriq_verse_text_report.json` file.

The `strands.py` path reaches the supplemental published page
`gh-pages/MAM-simple/versification-and-cantillation.html`.

Finding 1 does not feed MAM-parsed-plus generation, the core MAM-simple datasets,
or the MAM-with-doc edition.

### Current product evidence for finding 1

- Sixteen of the 77 Holman table verses are among the 133 affected verses.
- Replacing parameter 1 with parameter 3 only for this measurement changes 15
  Holman rows. Fourteen rows then fail the selected-verse-text check, and 13 rows
  fail the search across all MAM-parsed-plus files.
- None of the 34 MAM-suggestion verses is among the 133 affected verses.
- The final-hiriq search has zero hits under either selection.
- None of the verses used by the current versification-and-cantillation page is
  among the 133 affected verses.

The Holman table result makes the required repair a product-contract question.
The table may need the ketiv, the qere, or both. The code should give that caller
an explicit projection matching the table's question; changing every parameter-1
selection to parameter 3 without settling the table's question would replace one
implicit policy with another.

## Finding 2: qere atom tokenization splits one atom at template-fragment boundaries

Finding type: category 2 — behavior was implemented that should not have been
implemented.

`py/hkq_cmn/qere_projection.py:word_atoms_from_qere_atoms`, near line 220,
tokenizes each projected text fragment independently. A special-letter template
can divide one written atom into adjacent fragments with no whitespace, maqaf,
paseq/legarmeh glyph, or sof pasuq between the fragments. Independent splitting
therefore reports several atoms where the source has one atom. Genesis 1:1, for
example, is split into the fragments `בְּ` and `רֵאשִׁ֖ית` instead of the single
atom `בְּרֵאשִׁ֖ית`.

A traversal of the current corpus finds 48 affected verses and 75 extra fragment
tokens. Tokenization must join adjacent projected text fragments before applying
the delimiter expression, while preserving whatever source information the
ending search needs.

### Products reached by finding 2

The only production caller is
`py/hkq_cmn/qere_ending_search.py`, which is used by
`py/main_search_holam_he_qere.py` to write the internal tracked file
`holman/out/holam_he_qere_report.json`.

Finding 2 does not feed a published HTML page, MAM-parsed-plus, MAM-simple, or
MAM-with-doc. The current holam-he search has 1,369 hits with either tokenization,
so the present report happens not to expose the defect. Another suffix search can
expose it.

## Finding 3: internal documentation links are emitted as page-relative links

Finding type: category 2 — behavior was implemented that should not have been
implemented.

`py/mb_diff_mpu/mpplus_docnote.py:_render_template`, near lines 120–124, handles
`מ:קישור בהערה` and `מ:קישור פנימי בהערה` identically. The documented contract is
different:

- `מ:קישור בהערה` parameter 1 is an external URL used as-is;
- `מ:קישור פנימי בהערה` parameter 1 is a Wikisource-internal target that needs the
  `https://he.wikisource.org/wiki/` base.

The current MAM-parsed-plus corpus has three `מ:קישור פנימי בהערה` calls. The
Proverbs and Job calls have Wikisource-relative targets, so the current renderer
would produce broken page-relative links. The Leviticus call has an absolute
Archive.org URL despite using the internal-link template; the current renderer
happens to leave that URL usable, while the data does not satisfy the documented
template contract.

### Products reached by finding 3

The renderer is used only by the published MAM-with-doc change-log subsystem:

- `gh-pages/MAM-with-doc/change-log/*.html`;
- the corresponding change-log JSON files.

Finding 3 does not affect the MAM-with-doc edition pages or MAM-parsed-plus data.
No currently generated change-log report contains an internal-link call, so the
bad link is latent until a reported difference includes one of these notes.

## Finding 4: the plain-template validator checks argument count but not argument identity

Finding type: category 1 — required validation was not implemented.

`py/mb_cmn/plain_template_schema.py:validate_current_plain_template`, near lines
153–167, checks the template name and number of arguments. Several plain
templates use named arguments encoded inside those argument sequences. An
unexpected named argument can replace a required named argument without changing
the argument count, and the validator accepts that malformed shape.

Examples include the named branches of `מ:כפול`, the named qamats alternatives of
`מ:קמץ`, and the metadata arguments of `מ:קו״כ-אם-2`. The closed schema should
declare and validate required and allowed argument identities, not only the
number of arguments.

### Products and operations reached by finding 4

- `py/tmpl_survey/survey_plain.py` writes
  `out/tmpl-survey-plain/plain.json`, DOT files, and the published plain-template
  call-graph SVGs under `gh-pages/MAM-parsed/plain/svg/`.
- `py/main_authored.py verify-mp` reads the plain survey while checking claims in
  the authored MAM-parsed documentation.
- `py/subcommands/diff_wsgo.py` writes
  `out/diff_mamws_mamgo.json` and
  `out/diff_mamws_mamgo-auto-edits.json`; the second file contains proposed
  changes for the Google Sheet.

Finding 4 does not generate MAM-parsed-plain or MAM-parsed-plus. Its direct risks
are an inaccurate survey, a false-green documentation check, or a malformed
proposed spreadsheet edit. The current corpus passes the weaker validation; this
review did not identify a malformed current named-argument shape.

## Finding 5: several closed shape validators are not called on paths that discard parameters

Finding type: category 1 — required validation calls were not implemented.

The code defines closed required/allowed-parameter policies, but several
consumers dispatch on a recognized name and immediately select, flatten, or drop
parameters without applying the corresponding shape validator.

The highest-impact path is
`py/mpplus/mpplus_boring_tmpls.py:evaluate`, near lines 11–35. The module defines
`validate_current_handler_input_template` near line 167, but `evaluate` does not
call it before a handler returns a replacement string or selects a parameter. An
unexpected parameter can therefore be silently discarded by the flagship
MAM-parsed-plus generation path.

Additional paths with the same class of omission are:

- `py/hkq_cmn/mam_plus_verse_data.py:_collect_text_fragments`, which selects one
  parameter from recognized plus templates without calling
  `template_names.validate_current_plus_template`;
- `py/versification_and_cantillation/strands.py:_el_text`, which performs the same
  kind of selection for the supplemental versification-and-cantillation page;
- the nested-template traversal in
  `py/decnreub/decnreub_for_one_cant.py`; the outer decnreub traversal validates
  each top-level template, but this inner traversal dispatches on nested template
  names without validating each nested template's shape.

### Products reached by finding 5

- **Flagship products:** `mpplus_boring_tmpls.evaluate` is called by
  `py/py_misc/mam_parsed_plus.py` while generating `MAM-parsed/plus/*.json`.
  MAM-parsed-plus then feeds the core MAM-simple XML/JSON products and the
  MAM-with-doc edition.
- **Specialized and supplemental products:** `mam_plus_verse_data.py` feeds the
  Holman products listed under finding 1, and `strands.py` feeds
  `gh-pages/MAM-simple/versification-and-cantillation.html`.
- **Internal product:** the decnreub path writes `out/mam-decnreub.json`.

The current corpus has the expected shapes, and this review found no current
flagship output corrupted by finding 5. The missing validation nevertheless has
flagship blast radius: a future recognized template shape change can be silently
lost during MAM-parsed-plus generation instead of stopping at the closed dispatch
boundary.

## Product-priority summary

Finding 5 is the only open finding with direct flagship-product blast radius.
Finding 1 affects specialized Holman products and one supplemental authored page.
Finding 3 affects the supplemental MAM-with-doc change log. Finding 4 affects
surveys, documentation verification, and proposed spreadsheet edits. Finding 2
affects one internal analysis JSON file and does not change that file's current
hit set.

No finding in this document establishes that a current flagship artifact has
wrong content. Finding 5 establishes that a future recognized template-shape
change can reach flagship artifacts without the intended fail-fast validation.
