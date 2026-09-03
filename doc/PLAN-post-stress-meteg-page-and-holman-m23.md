# Plan: post-stress-meteg page and Holman M23 follow-through

Created 2026-09-03. Execute this plan from
C:/Users/BenDe/GitRepos/MAM-basics. The implementation publishes a generated
survey of MAM metegs after the primary stress, gives Holman suggestion M23 a
neutral link to that survey, and renames the reader-facing Holman archive
label. The implementation does not decide whether M23 should be accepted.

## Purpose, decisions, and boundaries

The generated HTML page is:

C:/Users/BenDe/GitRepos/MAM-basics/gh-pages/wlc/accgram/post-stress-meteg.html

The generated data companion is:

C:/Users/BenDe/GitRepos/MAM-basics/out/accgram/post-stress-meteg.json

The page describes MAM, a consensus text. The page does not use WLC as the
corpus for a claim about how accentuation works. A clearly attributed
manuscript/transcription comparison may appear only in the separate
post-silluq section.

The following decisions constrain every phase.

1. M23, Isaiah 23:12.11, remains open. The card keeps its present comparison
   and must not gain acceptance, rejection, a suppression entry, or a changed
   source message merely because the new page gives it context.
2. The public page may reproduce an excerpt from Yeivin or Breuer. Each
   excerpt must contain at most 150 words, and every such excerpt together
   must contain at most 300 words. The generator must enforce both limits
   whenever it contains excerpts; paraphrase is not mandatory.
3. U+05BD is silluq only when the stressed syllable is in the verse-final
   chanted word that has sof pasuq. A final input entry with no sof pasuq is
   incomplete input, not a silluq fallback.
4. The category called “meteg sharing a letter with a non-stress-marking
   accent” is an overlapping diagnostic. The page must not present it as a
   fourth mutually exclusive position category.
5. M17 and M32 remain declined. M24 and M34 retain the existing recorded
   dispositions. This plan does not edit Wikisource, run a MAM data download,
   run the mega pipeline, or add an expected-difference suppression for the
   future M24 stress-helper result.
6. C:/Users/BenDe/GitRepos/MAM-basics/py/accgram/meteg_silluq_context.py is
   not changed by this plan. The new survey has a stricter source-data
   completeness check rather than changing the established parser.

## Evidence to re-establish before editing

The five Claude notes below are evidence, not implementation instructions.
Read their claims, then remeasure against current files. The notes described
the MAM-basics commit 3829585; the executor must record the actual MAM-basics,
MAM-private, MAM-parsed, and UXLC-utils revisions in the phase-state note.

1. C:/Users/BenDe/.claude/plans/writing-only-to-a-robust-teapot-M23.md
   gives the M23 question, the initial MAM census, and the 1 Samuel 17:5
   manuscript/transcription observation.
2. C:/Users/BenDe/.claude/plans/writing-only-to-a-robust-teapot-M-vs-mgketer.md
   records the reported agreement of all 30 M (meteg) suggestions with
   mgketer.
3. C:/Users/BenDe/.claude/plans/writing-only-to-a-robust-teapot-census-report.md
   supplies the first census output and exposes the old final-entry
   classification error.
4. C:/Users/BenDe/.claude/plans/writing-only-to-a-robust-teapot-archived-terminology.md
   identifies the five rendered uses of “Suppressed” that should read
   “Archived”.
5. C:/Users/BenDe/.claude/plans/writing-only-to-a-robust-teapot-accent-placement-four.md
   records the status and downstream consequences of M17, M24, M32, and M34.

Before the first edit, load:

1. C:/Users/BenDe/.agents/skills/hebrew-prose/SKILL.md
2. C:/Users/BenDe/GitRepos/MAM-basics/CLAUDE.md
3. C:/Users/BenDe/GitRepos/MAM-basics/doc/agent-planning-principles.md
4. C:/Users/BenDe/GitRepos/MAM-private/masorah-books/README.md
5. C:/Users/BenDe/GitRepos/MAM-private/masorah-books/doc/migration-checklist.md

If C:/Users/BenDe/GitRepos/MAM-private/masorah-books/AGENTS.md is present,
load it before editing. If it is absent, record the absence in the phase-state
note rather than treating an unavailable instruction file as hidden context.

Use the full Yeivin OCR, not the partial adaptation:

C:/Users/BenDe/GitRepos/MAM-private/masorah-books/books/itm/md-export-of-docx/

Use the Breuer Markdown export, not the docx files:

C:/Users/BenDe/GitRepos/MAM-private/masorah-books/books/cos/md-export-of-docx/

The historical snapshot reported 233,715 prose-verse U+05BD occurrences and
43,711 poetic-verse U+05BD occurrences. The historical snapshot reported 231
post-stress metegs, including 140 in prose verses and 91 in poetic verses.
Those figures are a remeasurement target, not text for the new page. A
different result is a finding that must be explained before the page is
committed.

## Preconditions and collision checks

Another session may be live in MAM-basics or a sibling repository. Record the
MAM-basics HEAD, inspect status, and record the intended-path list before
editing. Unrelated dirty paths do not block this plan; never stage them. Just
before committing, recheck that HEAD has not changed and that only the
intended paths are staged.

The expected source-data precondition is that the Phonetic MAM standard-set
JSON remains available under:

C:/Users/BenDe/GitRepos/MAM-private/al-hatorah/io/a01-phonetic-std-set/

Run the existing stress-oracle differential check before writing the survey:

~~~powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_test.py C:/Users/BenDe/GitRepos/MAM-basics/py/tests/test_final_stress_vs_phonetic_mam.py
~~~

If that check fails, stop. The new page must not create a second interpretation
of the Phonetic MAM stress notation.

## Phase 1: build the survey data and generated page

Add these focused modules:

1. C:/Users/BenDe/GitRepos/MAM-basics/py/accgram/post_stress_meteg.py
2. C:/Users/BenDe/GitRepos/MAM-basics/py/accgram/post_stress_meteg_page.py

Register a new generate-html-post-stress-meteg subcommand in:

C:/Users/BenDe/GitRepos/MAM-basics/py/main_accgram.py

Follow the existing maqaf-nonfinal-accents architecture: the page module owns
the command-line arguments and writes both the JSON and the HTML in one run.
The default output paths are the two paths named in the Purpose section.
Accept explicit output-path arguments for focused verification.

### Survey data rules

Read every Phonetic MAM standard-set file through the existing final_stress
interface. Preserve the MAM form and source reference exactly as supplied.
Do not normalize Hebrew text. Treat the stress marker in the JTA field as the
stress oracle; do not infer primary stress from a U+05BD position.

For every U+05BD, record enough structured data to regenerate every displayed
table and count:

1. book, chapter, verse, and atom/chanted-word location;
2. whether the containing verse is prose or poetic;
3. the complete pointed chanted word and the JTA stress representation;
4. the U+05BD position relative to the stressed syllable;
5. whether the chanted word has sof pasuq; and
6. the mechanical diagnostic flags used by the page.

Classify a U+05BD as silluq only if all three conditions hold:

1. the mark is in the stressed syllable;
2. the chanted word is verse-final; and
3. the chanted word has sof pasuq.

If a final parsed entry lacks sof pasuq, raise a data-completeness error that
names the reference. Do not classify the mark and do not silently continue.
The page may describe a U+05BD elsewhere as a meteg only after this check has
made the silluq boundary explicit.

Keep relative-position groups mutually exclusive: pre-stress, stressed, and
post-stress. Store “shares a letter with a non-stress-marking accent” in a
separate diagnostic list or boolean. Render that diagnostic as an overlap,
with an explicit explanation that a record can also be post-stress.

Derive every count shown in prose, a table heading, or a figure caption from
the JSON. Add a pin_claims-style assertion that rederives the claimed groups
and raises on drift. Do not duplicate a numeric total in a docstring.

### Public-page content

The page needs these named sections:

1. “Meteg after the primary stress in MAM” defines the survey and states the
   exact silluq boundary.
2. “MAM census by verse system” presents prose-verses and poetic-verses
   counts, then links every displayed figure to the generated JSON.
3. “Post-stress metegs by structural type” separates mechanical results from
   the interpretation attributed to Yeivin and Breuer. A record that does not
   meet a displayed type remains visible as unclassified; do not force it into
   a source-derived category.
4. “The M23 comparison at Isaiah 23:12” gives neutral context for the
   suggestion without deciding its disposition. Give this section the stable
   HTML identifier m23-isaiah-23-12. The page uses complete
   chanted-word forms lifted from the source data, never hand-typed accents.
5. “The post-silluq case at 1 Samuel 17:5” attributes the separate
   manuscript/transcription observation to the LC/WLC or UXLC as applicable
   and says explicitly that MAM has only its silluq at that place.
6. “Sources and limits” cites the relevant Yeivin and Breuer sections and
   records the page's quotation accounting when the page contains excerpts.

Use a table rather than running prose wherever the page compares forms. Every
Hebrew-form cell has dir="rtl". Render forms with the existing
accents_and_letters helper, without vowels unless a vowel is the point of that
specific comparison. Search for forms by complete chanted-word patterns and
raise unless each intended location resolves exactly once.

If the page includes an excerpt, put its source identifier and text in one
structured private-source-excerpts sequence in the page module. Count
whitespace-delimited words in the same helper that renders the excerpt. Assert
that every excerpt is at most 150 words and that the sum is at most 300 words. If
the page uses no excerpts, the helper asserts that the excerpt list is empty.

Use Yeivin sections 332, 354, and 357 and Breuer Chapter 8 sections 2, 3,
46, and 47 as search anchors, then cite only claims the current OCR supports.
Do not turn a source observation into a claim that MAM follows a Breuer
edition: MAM is a consensus text.

Generate the focused artifacts:

~~~powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_accgram.py generate-html-post-stress-meteg
~~~

Read both regenerated artifacts. An unexplained change outside the new JSON
and new HTML is a failure. The expected generated additions are only:

1. C:/Users/BenDe/GitRepos/MAM-basics/out/accgram/post-stress-meteg.json
2. C:/Users/BenDe/GitRepos/MAM-basics/gh-pages/wlc/accgram/post-stress-meteg.html

## Phase 2: give M23 a controlled contextual link

Add a small Holman-context metadata module keyed by the stable source reference
Isa 23:12.11, not by the transient M23 ordinal. The module stores the label
“Meteg after the primary stress in MAM” and the generated relative destination:

../wlc/accgram/post-stress-meteg.html#m23-isaiah-23-12

Thread that data through:

1. C:/Users/BenDe/GitRepos/MAM-basics/py/py_render/rt_html.py
2. C:/Users/BenDe/GitRepos/MAM-basics/py/py_render/rt_mam_suggestion_card.py

The renderer emits the controlled contextual link after the M23 card content.
It does not reinterpret Markdown from a source message and it escapes the
label and href. No other card gains a link unless its reference is added to
the same explicit metadata table.

Do not place the link in:

C:/Users/BenDe/GitRepos/MAM-basics/holman/docs-not-served/mam_suggestions.json

That JSON is derived from the suggestion source. A renderer-owned context map
keeps the extracted comparison data separate from a later public explanation.

The M23 card must keep its existing title, forms, source message, disposition,
and comparison status. The only intended M23 rendered difference is the new
neutral contextual link.

## Phase 3: re-establish the M-versus-mgketer evidence

Add a mechanical differential verifier for the 30 M (meteg) suggestion
records. Keep the verifier in a focused Holman module and invoke it from
C:/Users/BenDe/GitRepos/MAM-basics/py/main_verify_and_render_table.py through
an explicit --mgketer-root argument. The command reads the current mgketer
reports under:

C:/Users/BenDe/GitRepos/MAM-private/mgketer/

For each M record, the verifier must establish that the mgketer report records
the suggested extra meteg in the corresponding MAM reading. It must fail with
a list of missing or mismatched stable references; it must not merely print a
warning. Record a compact source revision and result summary in the existing
verification data only when the current data format already has a verification
field. Do not copy private report prose into a public artifact.

This is a differential check against an independent report, not a hand-picked
example test. It is the only new test-shaped mechanism this plan needs.

## Phase 4: rename the Holman reader-facing archive label

In C:/Users/BenDe/GitRepos/MAM-basics/py/py_render/rt_html.py, change the
four reader-facing values that use “Suppressed” to “Archived”:

1. the main-page navigation label;
2. the archive page title;
3. the archive page heading; and
4. the archive records heading.

Update nearby reader-facing comments to name the Archived page where doing so
removes a contradiction. Keep internal identifiers such as SUPPRESSED_*,
archive predicates, JSON keys, and generated filenames unchanged unless a
specific technical reason requires a separate rename.

The required rendering run is the verifier-renderer, not the render-only
command:

~~~powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_verify_and_render_table.py --mgketer-root C:/Users/BenDe/GitRepos/MAM-private/mgketer
~~~

Read these two rendered files after that command:

1. C:/Users/BenDe/GitRepos/MAM-basics/gh-pages/holman/table_data_findings.html
2. C:/Users/BenDe/GitRepos/MAM-basics/gh-pages/holman/table_data_findings_suppressed.html

There are five reader-visible “Suppressed” occurrences before the rename:
one in the main page and four in the archive page. Confirm that those five
reader-visible labels read “Archived” afterward. Do not count a sixth
occurrence that does not exist. The generated archive filename remains
table_data_findings_suppressed.html.

## Phase 5: verify the M17, M24, M32, and M34 boundary

Read:

C:/Users/BenDe/GitRepos/MAM-basics/py/hkq_cmn/mam_suggestion_dispositions.py

Confirm that the existing disposition map still records:

1. M17, 2 Kings 17:15.15, declined;
2. M24, Joshua 10:12.3, taken;
3. M32, Judges 10:11.1, declined; and
4. M34, Zechariah 2:4.11, taken.

This check is a scope guard. It does not edit MAM source data. When a later
authorized MAM pipeline refresh takes M24 through the Wikisource and MAM
stages, MAM is expected to have the doubled pashta stress helper while mgketer
has one pashta. That future intentional difference is not a reason to add a
suppression entry. The later pipeline executor must remeasure M24 and M34 at
the actual source revisions rather than trust the date or snapshot in the
evidence note.

## Final verification, commit, and phase state

Format only the Python files changed by this plan:

~~~powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m black C:/Users/BenDe/GitRepos/MAM-basics/py/accgram/post_stress_meteg.py C:/Users/BenDe/GitRepos/MAM-basics/py/accgram/post_stress_meteg_page.py C:/Users/BenDe/GitRepos/MAM-basics/py/main_accgram.py C:/Users/BenDe/GitRepos/MAM-basics/py/py_render/rt_html.py C:/Users/BenDe/GitRepos/MAM-basics/py/py_render/rt_mam_suggestion_card.py
~~~

Run the stress-oracle check, the focused page generator, and the
verifier-renderer after formatting. Read the generated JSON and both generated
HTML pages; inspect the complete diff. Run the relevant existing Holman
verification tests if main_verify_and_render_table.py names them as
preconditions.

The expected tracked changes are:

1. this plan's implementation modules and the main_accgram registration;
2. the new JSON and accgram HTML page;
3. the renderer context metadata and the M23 contextual link;
4. the two regenerated Holman HTML files and any established verification
   summary that the verifier owns; and
5. the four reader-facing “Archived” labels.

The expected non-changes are:

1. MAM source data, Wikisource data, and MAM-parsed data;
2. M23's source message, comparison forms, and disposition;
3. the M17, M24, M32, and M34 dispositions;
4. meteg_silluq_context.py;
5. every existing accgram page except the deliberate new page; and
6. private-source text outside the bounded public excerpts.

After each completed phase, add a dated phase-state section to this plan. The
phase-state section records input revisions, the exact commands run, measured
figures, changed paths, and any explained mismatch with the historical
snapshot. After final verification, commit only the intended paths on main and
push main. Do not stage unrelated changes that were already present.
