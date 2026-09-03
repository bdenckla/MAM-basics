# Plan: post-stress-meteg page and Holman M23 follow-through

Created 2026-09-03. Execute this plan from
C:/Users/BenDe/GitRepos/MAM-basics. The implementation publishes a generated
survey of MAM metegs after the primary stress, gives Holman suggestion M23 a
neutral link to that survey, and renames the reader-facing Holman archive
label. M23 is accepted already; this plan does not implement that acceptance,
which is item 6 of the programme.

## Where this plan sits in the larger Holman meteg work

This plan is ITEM 1 of a seven-item programme, and it is the only item written
down in a tracked document. The other six — build the Wikisource bot edit for
all 30 meteg suggestions, run it, download the affected chapters, run the wsgo
diff and the standard MAM update pipeline, archive the 30 records, and refresh
the mgketer comparison — are described in
[`PLAN-holman-meteg-rollout-programme.md`](PLAN-holman-meteg-rollout-programme.md).
Read that document first for the ordering and the cross-item dependencies; this
one for the page, the M23 card link, and the terminology rename.

**This plan's phases do not all run at the same point in the programme.**
Corrected 2026-09-03, the programme having said until that day that item 1 "can
be done first or last". Phase 3 MUST run before the programme's item 3, its
verifier needing the thirty mgketer diffs that items 3 through 7 remove; Phases
4, 5 and 6 are indifferent to the pipeline and are cheapest alongside it.
Phases 1 and 2 run AFTER the programme's item 5, because item 5
changes the figures the survey publishes: M23 raises the post-stress count from
231 to 232, and the 29 removals, every one of them a pre-stress meteg, lower
the pre-stress figures. The programme's section "Item 5 changes the survey's
figures, and nothing re-runs the survey by itself" holds the measurement.

Two boundaries between this plan and the programme are worth stating here,
because both are easy to cross by accident. This plan does not edit Wikisource,
does not run the mega pipeline, and does not archive any record — decision 5
below says so, and the programme's items 2 through 6 are where those happen.
And the mgketer refresh is item 7, in MAM-private, which is outside the
MAM-basics pipeline: Phase 3 below READS mgketer's current reports as a
differential oracle and never regenerates them.

## Purpose, decisions, and boundaries

Ben's decision, 2026-09-03, settling what the evidence note
doc/holman-meteg-m23-isaiah-23-12.md left open ("Which repo hosts the page,
and its name, are not decided"): the page is published at MAM-basics' own
deploy root, beside gh-pages/unicode-proposals.html, as one of this
repository's own authored pages. Six artifacts, all in MAM-basics:

1. The computation module is
   C:/Users/BenDe/GitRepos/MAM-basics/py/accgram/post_stress_meteg.py.
2. The data companion is
   C:/Users/BenDe/GitRepos/MAM-basics/out/accgram/post-stress-meteg.json. It is
   a drift-guard read by the page's pin_claims assertion, NOT a reader-facing
   artifact: no .json is published under gh-pages anywhere in this repository,
   and the accgram pages link to none.
3. The page module is
   C:/Users/BenDe/GitRepos/MAM-basics/py/author_site/post_stress_meteg.py,
   rendering with accgram's helpers. Per py/author_site/entries.py's stated
   rule, it describes itself in that module's declarative types rather than
   writing URLs straight into anchor_h calls, or the link lint cannot see them.
4. The published HTML is
   C:/Users/BenDe/GitRepos/MAM-basics/gh-pages/post-stress-meteg.html. Hyphens,
   matching unicode-proposals.html, the page it sits beside.
5. Its title and filename constants go in
   C:/Users/BenDe/GitRepos/MAM-basics/py/author_site/site_data.py beside
   UNICODE_PROPOSALS_FNAME and UNICODE_PROPOSALS_TITLE, with an authored entry
   so gh-pages/index.html links it. The M23 card's link is then the relative
   ../post-stress-meteg.html#m23-isaiah-23-12.
6. main_authored.py's gen_site gains a flag that renders the page from the
   tracked JSON instead of recomputing, so the mega pipeline never requires
   MAM-private.

WHY THE DEPLOY ROOT AND NOT MAM-with-doc/gh-pages/misc/, which is where the
authored Tanakh-topic documents otherwise live. Ben's requirement, 2026-09-03:
this plan must be executable in a MAM-basics worktree. Three consequences
follow, and each favours the deploy root.

1. A worktree isolates MAM-basics only. Every write named above lands inside
   the worktree, and the merge back to main is a single-repository merge; a
   write to MAM-with-doc would escape the isolation entirely.
2. main_authored.py's almost_main, which gen-misc calls, is all-or-nothing: it
   regenerates all eighteen miscellaneous documents plus that shelf's
   index.html and style.css. gen_site regenerates two pages, both here.
3. py/tests/test_site_index_links.py checks that every index link pointing into
   this repository's gh-pages/ names a file that exists. Its docstring says why
   the MAM-with-doc half is deliberately unchecked: that would need a sibling
   clone, and the missing-input rule forbids skipping. So a page at the deploy
   root is inside the half a lint can reach, and a page on the miscellaneous
   shelf is permanently outside it.

Why accgram's render helpers rather than mb_author's: the page needs
accents_and_letters, the verse-reference formatters ref_abbrev / ref_display /
ref_short / verse_links, the itm() and cos() source-title helpers, and
H.table_row_of_data's per-cell attribute splicing, which is how the dir="rtl"
rule is satisfied. py/mb_author/ and py/author_misc/ have none of those,
because the authored documents hand-type their rows rather than compute them.

Why not gh-pages/wlc/accgram/, which was this plan's location until
2026-09-03: the wlc/ prefix exists so wlc-utils' 154 frozen redirect stubs can
rewrite a prefix onto MAM-basics/wlc/<path>, a page published here after the
2026-08-17 move earns no stub, and the page's own Purpose says it does not take
WLC as its corpus.

The page describes MAM, a consensus text. The page does not use WLC as the
corpus for a claim about how accentuation works. A clearly attributed
manuscript/transcription comparison may appear only in the separate
post-silluq section.

The following decisions constrain every phase.

1. M23, Isaiah 23:12.11, IS ACCEPTED, along with the other 29 meteg
   suggestions. Ben's decision, stated 2026-09-03: he is taking all thirty, and
   the post-stress meteg research was never an input to that — the acceptance
   preceded it, and the research provides background on a phenomenon he finds
   interesting and not that common. This decision read "M23, Isaiah 23:12.11,
   remains open" until that day. What still holds is the scope guard, and it is
   why this decision keeps its place: THIS PLAN does not implement the
   acceptance. The card keeps its present comparison forms and source message,
   and must not gain an archived disposition as a side effect of the new page
   giving it context. Item 6 of the programme records the acceptance, for M23
   and the other 29 together.
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

All five moved into this repository's doc/ on 2026-09-03, out of
C:/Users/BenDe/.claude/plans/, where this plan cited them until that day. Three
of them gained a dated correction in the move, each marked
“Correction, 2026-09-03” and placed beside the claim it corrects. Their sixth
sibling, doc/holman-meteg-m13-qamats-template.md, holds the M13 template
finding and is not evidence this plan needs.

1. doc/holman-meteg-m23-isaiah-23-12.md
   gives the M23 question, the initial MAM census, and the 1 Samuel 17:5
   manuscript/transcription observation. Its corrections settle the page
   location this plan decides, and demote its census figures to a legacy
   baseline.
2. doc/holman-meteg-vs-mgketer.md
   records the reported agreement of all 30 M (meteg) suggestions with
   mgketer.
3. doc/post-stress-meteg-census-2026-09-03.md
   supplies the first census output and exposes the old final-entry
   classification error.
4. doc/holman-suggestions-archived-terminology.md
   identifies the five rendered uses of “Suppressed” that should read
   “Archived”. Its correction records that the note's own total of six is
   wrong, the measured count being five, as this plan and the programme both
   say.
5. doc/holman-accent-placement-four.md
   records the status and downstream consequences of M17, M24, M32, and M34.

Before the first edit, load:

1. The hebrew-prose skill, INVOKED BY NAME rather than read as a file, so its
   four references/ files come with it. references/rendered-prose.md is where
   the dir="rtl" rule this plan depends on is stated in full, and reading only
   SKILL.md misses it. The live copy is
   C:/Users/BenDe/.claude/skills/hebrew-prose/, tracked in github-misc at
   dot-claude/skills/. DO NOT read C:/Users/BenDe/.agents/skills/hebrew-prose/:
   that copy is a stale mechanical rename of the live one, differing in
   SKILL.md and in three of the four references/ files, and it says
   "~/.Codex/AGENTS.md" and "MAM-basics/AGENTS.md" where the live copy says
   "~/.claude/CLAUDE.md" and "MAM-basics/CLAUDE.md".
2. C:/Users/BenDe/GitRepos/MAM-basics/CLAUDE.md
3. C:/Users/BenDe/GitRepos/MAM-basics/doc/agent-planning-principles.md
4. C:/Users/BenDe/GitRepos/MAM-private/masorah-books/CLAUDE.md
5. C:/Users/BenDe/GitRepos/MAM-private/masorah-books/README.md
6. C:/Users/BenDe/GitRepos/MAM-private/masorah-books/doc/migration-checklist.md

There is no masorah-books/AGENTS.md and there never has been. This plan asked
for one until 2026-09-03, having inherited the name from the stale skill copy
above; the file the live skill actually says to read first is that tree's
CLAUDE.md, item 4 in the list.

Use the full Yeivin OCR, not the partial adaptation:

C:/Users/BenDe/GitRepos/MAM-private/masorah-books/books/itm/md-export-of-docx/

Use the Breuer Markdown export, not the docx files:

C:/Users/BenDe/GitRepos/MAM-private/masorah-books/books/cos/md-export-of-docx/

The historical figures below are the 2026-09-03 output of the throwaway census
script C:/Users/BenDe/.claude/plans/writing-only-to-a-robust-teapot-census.py,
which stays untracked there because its line 49 is a sys.path.insert. Its
report is tracked, at doc/post-stress-meteg-census-2026-09-03.md.
Use the figures as a legacy comparison baseline only. Do not run or edit that
script during this work: it overwrites the evidence report, and its
verse-final test treats a final parsed entry as verse-final even when that
entry lacks sof pasuq. The strict tracked generator in Phase 1 replaces it as
the remeasurement authority.

| system | chanted words checked | pre-stress meteg | post-stress meteg | silluq |
|---|---|---|---|---|
| prose | 233,715 | 13,131 | 177 | 18,779 |
| poetic | 29,605 | 1,814 | 54 | 4,486 |

So the survey's headline count is 231 post-stress metegs, 177 in prose verses
and 54 in poetic verses, over 263,320 chanted words. The run reported zero
syllable-count mismatches, zero same-letter failures, and zero entries lacking
jta or fva; a nonzero count in any of those three is itself a finding. The
overlapping diagnostic of decision 4 stood at 27 in prose verses and 119 in
poetic verses, counted inside the pre-stress and post-stress groups rather
than beside them.

Those figures are not text for the new page. The new generator must compare
its result with the legacy baseline and record each difference. A changed
silluq or stressed-syllable count caused by the corrected sof-pasuq boundary
is an expected correction; it still needs a separate audit listing the
affected references. Any other difference is a finding that must be explained
before the page is committed. Note that 233,715 counts chanted words checked,
not U+05BD occurrences; the legacy run classified 32,087 U+05BD occurrences in
prose verses and 6,354 in poetic verses.

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

1. C:/Users/BenDe/GitRepos/MAM-basics/py/accgram/post_stress_meteg.py, the
   survey computation over the Phonetic MAM standard set.
2. C:/Users/BenDe/GitRepos/MAM-basics/py/author_site/post_stress_meteg.py, the
   page. Same basename in a different package, as accgram's own
   maqaf_nonfinal_accents / maqaf_nonfinal_accents_page pair splits computation
   from rendering. py/author_site/unicode_proposals.py is the model to follow.

Register the page in C:/Users/BenDe/GitRepos/MAM-basics/py/main_authored.py's
gen_site, whose loop currently runs unicode_proposals.gen_html_file() and
site_index.gen_html_file(); the new page joins it, and site_index must run
last so the index sees the entry.

DO NOT add the page to py/main_accgram.py's _HTML_GENERATORS table. That table
was this plan's route until 2026-09-03, and it is wrong twice over: its own
comment ties each entry's name to a gh-pages/wlc/accgram/<name>.html
destination, and py/main_0_mega.py runs the whole batch, so a member reading
MAM-private would make the mega require a private clone for the first time.

The mega runs main_authored.gen_site too, so the deploy root already carries
the staleness protection batch membership would have bought. That step is the
reason for artifact 6 in the Purpose section: add a flag to main_authored.py
that renders the page from the tracked out/accgram/post-stress-meteg.json
rather than recomputing, pass it from the mega, and recompute from MAM-private
only on an explicit run. The model is py/main_accgram.py's --trust-survey,
which only the mega passes and which fails loudly when the JSON it was told to
trust is absent; that flag is routed to one report through the scalar
_SURVEY_READING_REPORT, and the main_authored equivalent should be written for
a named set from the start.

The survey computation owns the command-line arguments for a standalone run and
writes the JSON; the page module writes the HTML. Both accept explicit output
paths for focused verification. The default paths are those named in the
Purpose section.

### Survey data rules

Read every Phonetic MAM standard-set file directly, as
C:/Users/BenDe/GitRepos/MAM-basics/py/tests/test_final_stress_vs_phonetic_mam.py
does. There is no standard-set reading interface in
C:/Users/BenDe/GitRepos/MAM-basics/py/accgram/final_stress.py to reuse: that
module is a predicate over a pointed word, whose public surface is
ends_in_furtive_patax, last_syllable_onset, and is_final_stress, and
is_final_stress answers only whether the stress is final rather than which
syllable carries it. Reuse its nucleus-finding conventions where they fit, and
reach the stressed syllable itself from the JTA field. Preserve the MAM form
and source reference exactly as supplied. Do not normalize Hebrew text. Treat
the stress marker in the JTA field as the stress oracle; do not infer primary
stress from a U+05BD position.

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

If a final parsed entry lacks sof pasuq, collect its reference and continue
scanning, then fail at the end of the run with the complete list. Do not
classify any such mark and do not silently continue past the run. Collecting
before failing is what makes the audit below possible: a run that raises on the
first offending reference can never enumerate the rest, and the plan asks for
an enumeration. Phase 3's verifier is written the same way, failing with a list
rather than on first sight. The page may describe a U+05BD elsewhere as a meteg
only after this check has made the silluq boundary explicit.

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
   counts, every one of them derived from the generated JSON. It does NOT link
   to that JSON: no .json is published under gh-pages anywhere in this
   repository, and maqaf-nonfinal-accents.html, the model page, links to none.
   The JSON is the pin_claims oracle, not a reader-facing artifact.
3. “Post-stress metegs by structural type” separates mechanical results from
   the interpretation attributed to Yeivin and Breuer. A record that does not
   meet a displayed type remains visible as unclassified; do not force it into
   a source-derived category.
4. “The M23 comparison at Isaiah 23:12” gives context for the suggestion.
   Give this section the stable HTML identifier m23-isaiah-23-12. The page uses
   complete chanted-word forms lifted from the source data, never hand-typed
   accents. Because this phase runs after the programme's item 5, MAM has the
   meteg by then and Holman's recorded comparison forms do not: his `mam_form`
   is what he was sent, frozen at the date of his message. Say that, rather
   than presenting a difference that no longer exists. The suggestion was
   taken, and the section's subject is what kind of meteg it is and how common
   that kind is in MAM, not an open disagreement.
5. “The post-silluq case at 1 Samuel 17:5” says explicitly that MAM has only
   its silluq at that place, and attributes every other reading to the source
   that actually carries it. Name WLC 4.22 and UXLC 3.9 as the transcriptions
   they are — “UXLC 3.9 records two U+05BD”, never “Leningrad has two” — and
   cite the Leningrad Codex only from the manuscript image, folio F159A column
   3 line 8, which the M23 evidence note links. Do not write “LC/WLC”: that
   slash-pair collapses a manuscript into a transcription of it, which is the
   distinction this section exists to make.
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

Use Yeivin sections 308, 332, 338, 354, and 357 and Breuer Chapter 8 sections
2–10, 46, and 47 as search anchors, then cite only claims the current OCR
supports. Yeivin section 308 feeds the closed-final-syllable ṣere case in
section 338; Breuer sections 5–8 describe the broader big-vowel-in-a-closed-
syllable type. Keep those scopes distinct in the rendered prose.

Each of the three post-stress types must be anchored in BOTH sources, because
the page's section 3 attributes its interpretation to Yeivin and Breuer
together, and an unbalanced anchor list sources the rarest type best and the
commonest worst. The pairing, from the M23 evidence note:

| Type | Yeivin | Breuer Ch. 8 | Marked |
|---|---|---|---|
| Closed syllable with ṣere | 338, fed by 308 | 5–8 | obligatory, in manuscripts and printed texts |
| Guttural at word end | 354 | 9–10 | obligatory |
| Open syllable, the קוּמִי rule | 332 | 46–47 | optional, rarely marked, not in printed texts |

Breuer sections 9–10 were absent from this list until 2026-09-03, leaving
Yeivin section 354 as the one type cited from a single source; Breuer section 3
is the ten-type taxonomy the three rows above are drawn from, and section 2 is
its statement that optional ga'ayot follow no set tradition.

Yeivin section 325, ga'ya before paseq, is deliberately NOT an anchor: Yeivin
calls it marked only in early manuscripts and rare even there. If the census
turns up post-stress metegs before a paseq, that is a finding, and the decision
to add section 325 is Ben's rather than the executor's.

Do not turn a source observation into a claim that MAM follows a Breuer
edition: MAM is a consensus text.

Generate the focused artifacts:

~~~powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_authored.py gen-site
~~~

This command is the authoritative remeasurement.

THE AUDIT IS A SECTION OF THE JSON, NOT A THIRD FILE. Earlier drafts of this
plan required "a separate audit" while also saying the expected additions were
only two files, and never gave the audit a path; and an audit printed to stdout
would put Hebrew references on a stream that is cp1252 on this machine when
redirected. So the generator writes a named section inside
out/accgram/post-stress-meteg.json holding the comparison against the legacy
baseline: each differing count, and the references whose classification the
corrected sof-pasuq boundary moved. Read that section as part of reading the
JSON. Nothing is printed to stdout but ASCII progress.

Expected changes, all in MAM-basics:

1. out/accgram/post-stress-meteg.json — new.
2. gh-pages/post-stress-meteg.html — new.
3. gh-pages/index.html — one added entry, from the site_data authored entry.
4. gh-pages/unicode-proposals.html — regenerated by gen_site and expected
   BYTE-IDENTICAL. A diff here is a finding, not noise.

An unexplained change outside those four is a failure.

## Phase 2: give M23 a controlled contextual link

Add a small Holman-context metadata module keyed by the stable source reference
Isa 23:12.11, not by the transient M23 ordinal. Confirmed 2026-09-03: that
record's ref field in holman/docs-not-served/mam_suggestions.json is exactly
"Isa 23:12.11", and rt_mam_suggestion_card.py already keys a frozenset by the
same kind of reference — EXTRA_LETTER_SPACING_REFS, whose members are
"Judg 10:11.1" and "Zech 2:4.11". Note that the card resolves ref_as_sent
before ref, so the new lookup must read the same field the card does.

The module stores the label “Meteg after the primary stress in MAM” and the
generated relative destination, which is a sibling-directory hop now that the
page publishes at the deploy root rather than under gh-pages/wlc/accgram/:

../post-stress-meteg.html#m23-isaiah-23-12

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

Add a mechanical differential verifier for every meteg suggestion record. The
historical roster contains 30: M1–M16, M18–M23, M25–M31, and M33. A changed
roster is a finding; the verifier must report it rather than silently applying
the historical count.

THE LETTER M DOES NOT MEAN METEG. It is the MAM-suggestion series prefix, which
py/py_render/rt_mam_suggestion_card.py renders as M{case_number}. Measured
2026-09-03 over holman/docs-not-served/mam_suggestions.json: there are 34 M
records, of which 30 differ from their comparison form in metegs alone. The
other four are M17, M24, M32 and M34 — precisely the accent-placement records
Phase 5 guards — so Phase 3 and Phase 5 partition one set of 34 exhaustively,
and neither phase's roster may be derived by assuming M1–M30.

Keep the verifier in a focused Holman module behind its OWN entry point, run
by hand, ONCE, before the programme's item 3. Do NOT wire it into
C:/Users/BenDe/GitRepos/MAM-basics/py/main_verify_and_render_table.py. Ben's
decision, 2026-09-03, settling the question this phase raised earlier the same
day, in his words: "run it once as a one-time check and don't wire it into the
renderer." The section below gives the reason and what was rejected. On the
entry point that does have it, --mgketer-root stays REQUIRED rather than
optional with a skip: a missing input must fail rather than report green having
verified nothing. The one-time run reads the current mgketer reports under:

C:/Users/BenDe/GitRepos/MAM-private/mgketer/

For each M record, the verifier must find one mgketer diff card for the same
reference and atom, verify both sides against Holman's MAM and Aleppo forms,
and derive the meteg direction from those two forms. The 2026-09-03 baseline
has 29 “MAM adds meteg” records and one “mgketer adds meteg” record: M23,
Isaiah 23:12.11. M23 therefore passes only when mgketer, rather than MAM, has
the meteg at the designated atom.

Match the complete atom and its accentuation, not consonants alone. M22 has
two look-alike compounds in one verse whose accentuation and atom location
distinguish the Holman record from the unrelated mgketer record. Permit a
display-artifact normalization only from a named, record-specific allowlist
that the verifier reports; do not normalize forms broadly enough to hide a
different reading.

The verifier must fail with a list of missing, ambiguous, or mismatched stable
references; it must not merely print a warning. Record a compact source
revision and result summary in the existing verification data only when the
current data format already has a verification field. Do not copy private
report prose into a public artifact.

This is a differential check against an independent report, not a hand-picked
example test. It is the only new test-shaped mechanism this plan needs.

### Ben's decision, 2026-09-03: the check runs once and stays out of the renderer

This section was an OPEN QUESTION when it was written earlier the same day. Ben
settled it that day, in his words: “run it once as a one-time check and don't
wire it into the renderer.”

THE PROBLEM IT SETTLES. Phase 3 requires one live mgketer diff card per M
record, and the programme's items 3 through 7 remove exactly those thirty
differences from MAM. The programme's item 7 states the expected outcome
itself: “MAM adds meteg” drops by the extant removals and “mgketer adds
meteg” drops to 4, M23 leaving that category. So after the programme has run,
the check finds no card for any of the thirty and fails for all thirty. Had it
been wired into the rendering command as a required argument, that failure
would have left the public Holman pages unrenderable rather than merely
unverified. Ordering Phase 3 before item 3 gets the check run while it can
still run; only leaving it out of the renderer stops the command breaking
afterwards.

WHAT THE EXECUTOR DOES:

1. Give the check its own entry point and run it by hand, once, before the
   programme's item 3, at the MAM-basics and MAM-private revisions current
   then. Record its result in this plan's phase-state section: the run is not
   repeatable after the programme, so the phase-state is the only place the
   result will survive.
2. Let nothing in a pipeline, a test or a rendering command depend on it.
   py/main_0_mega.py reaches neither Holman rendering command, so there is
   nothing to keep out of the mega either.
3. Leave py/main_verify_and_render_table.py's arguments alone. Its existing
   verification of the table's words against MAM-parsed and its notes against
   UXLC is unaffected by this phase and stays exactly as it is.

TWO ALTERNATIVES WERE REJECTED, recorded so they are not re-proposed. A
snapshot of the mgketer reports, tracked in this repository, would keep the
check recurring, at the cost of a tracked copy of private-repository output
needing its own licence scoping. Checking only records carrying no archived
disposition would, after item 6, check none of the thirty and so report green
having verified nothing, which this repository's missing-input rule forbids.

## Phase 4: rename the Holman page identity and archive label

Two reader-facing renames, both in
C:/Users/BenDe/GitRepos/MAM-basics/py/py_render/rt_html.py, done together
because SUPPRESSED_PAGE_TITLE is touched by both and would otherwise be
rewritten twice through an intermediate value nobody wants.

### Rename A: drop the ketiv/qere framing from the page's identity

Ben's decision, 2026-09-03: the page's title and heading should read simply
**“Holman MAM suggestions”**. His reason, in his own words: *“The ketiv/qere
review that this all started with was just a specific type of MAM suggestion
that now is not the only type of suggestion covered by this document.”*

Three constants carry the old framing. Measured 2026-09-03 at rt_html.py lines
54 to 56:

1. `MAIN_PAGE_TITLE = "Holman k/q + MAM suggestions"` becomes
   `"Holman MAM suggestions"`.
2. `MAIN_PAGE_HEADING = "Holman's ketiv/qere review and MAM suggestions"`
   becomes `"Holman MAM suggestions"`.
3. `SUPPRESSED_PAGE_TITLE = "Holman k/q - Suppressed"` becomes
   `"Holman MAM suggestions - Archived"`, which is rename A and rename B in one
   string.

The comment above those constants states the justification this decision
overturns — that the page “carries two bodies of Holman's work since
2026-09-02, so its title and heading name both.” Replace it rather than leaving
it to contradict the code, keeping its still-true second half: the FILENAME
table_data_findings.html is deliberately unchanged, being the URL index.html
links and the one Ben has already sent to correspondents.

**Change nothing else that says ketiv/qere.** The rest of that vocabulary names
a category of finding that still exists as one kind among several, which is
precisely Ben's point, and it is load-bearing: the `kind-ketiv-qere` filter ids
and `cat-kind-ketiv-qere` CSS classes that drive the page's filtering, the
`ketiv/qere` finding badges and the legend swatch, the `UXLC ketiv` and
`HaKeter ketiv` comparison-column names, and every
github.com/bdenckla/holman-ketiv-qere issue URL. Touching any of those breaks
filtering or link resolution rather than renaming a page.

### Rename B: “Suppressed” becomes “Archived”

Change the four reader-facing values that use “Suppressed” to “Archived”:

1. the main-page navigation label;
2. the archive page title (the same constant as rename A's item 3);
3. the archive page heading; and
4. the archive records heading.

Update nearby reader-facing comments to name the Archived page where doing so
removes a contradiction. Keep internal identifiers such as SUPPRESSED_*,
archive predicates, JSON keys, and generated filenames unchanged unless a
specific technical reason requires a separate rename.

The rendering run is the verifier-renderer, unchanged and with no new
argument. Phase 3's mgketer check is a separate one-time entry point and is
deliberately not part of this command; py/main_just_render_table.py, the
render-only command, is not the one to use either, since the existing
MAM-parsed and UXLC verification should run alongside the rename:

~~~powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_verify_and_render_table.py
~~~

Read these two rendered files after that command:

1. C:/Users/BenDe/GitRepos/MAM-basics/gh-pages/holman/table_data_findings.html
2. C:/Users/BenDe/GitRepos/MAM-basics/gh-pages/holman/table_data_findings_suppressed.html

There are five reader-visible “Suppressed” occurrences before the rename:
one in the main page and four in the archive page. Confirm that those five
reader-visible labels read “Archived” afterward. Do not count a sixth
occurrence that does not exist. The generated archive filename remains
table_data_findings_suppressed.html.

For rename A there are three reader-visible occurrences, measured 2026-09-03:
the main page's `<title>` and `<h1>`, and the archive page's `<title>`. The
archive page has no `<h1>` carrying the old framing — its heading is the bare
“Suppressed”, which rename B handles. Afterwards the main page's `<title>` and
`<h1>` both read “Holman MAM suggestions” and the archive page's `<title>`
reads “Holman MAM suggestions - Archived”.

Both pages will still hold many occurrences of “ketiv/qere” after this phase,
in the filter ids, CSS class names, finding badges, legend, comparison-column
names and issue URLs listed above. That is the expected result, not a missed
rename.

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

## Phase 6: close the published-but-unlinked gap in the site index

Ben's request, 2026-09-03, occasioned by this plan adding the deploy root's
second authored page. Extend
C:/Users/BenDe/GitRepos/MAM-basics/py/tests/test_site_index_links.py with the
direction it does not yet cover.

What it checks today is entry to file: test_every_in_site_link_names_a_tracked_page
asserts that every index link pointing into this repository's gh-pages/ names a
file that exists. The reverse is unchecked, so a page generated at the deploy
root with no site_data entry is published and unreachable from the index, and
nothing says so.

Add a test asserting the reverse: every tracked gh-pages/*.html at the deploy
root is either named by an authored entry or listed in a NAMED exclusion tuple
in the test. Naming the exclusions is what makes the check work — a deliberate
omission must not be indistinguishable from an accident. index.html itself is
the obvious first member, being the index rather than an entry in it.

Keep it at the deploy root; do not walk the whole gh-pages/ tree. The
subtree pages under gh-pages/wlc/, gh-pages/holman/ and gh-pages/book-of-job/
are reached through their own subtree indexes rather than through authored
entries, so including them would fail immediately and for the wrong reason.

Follow the file's existing convention that a green run which verified nothing
is a failure: assert the input is the size it should be before asserting
anything about it, as both current tests do.

This is one commit of its own, separate from the page. It changes a shared
lint that the whole repository's site depends on, and it should be reviewable
without the page's diff around it.

## Final verification, commit, and phase state

Format only the Python files changed by this plan:

~~~powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m black C:/Users/BenDe/GitRepos/MAM-basics/py/accgram/post_stress_meteg.py C:/Users/BenDe/GitRepos/MAM-basics/py/author_site/post_stress_meteg.py C:/Users/BenDe/GitRepos/MAM-basics/py/author_site/site_data.py C:/Users/BenDe/GitRepos/MAM-basics/py/main_authored.py C:/Users/BenDe/GitRepos/MAM-basics/py/py_render/rt_html.py C:/Users/BenDe/GitRepos/MAM-basics/py/py_render/rt_mam_suggestion_card.py C:/Users/BenDe/GitRepos/MAM-basics/py/tests/test_site_index_links.py
~~~

Add the Phase 3 verifier module and its entry point to that command when their
filenames are settled. py/main_accgram.py is deliberately absent: this plan no
longer touches it. py/main_verify_and_render_table.py left the list on
2026-09-03, when Ben's decision kept Phase 3's check out of that command; no
phase of this plan edits that file now.

Run the stress-oracle check, the focused page generator, and the
verifier-renderer after formatting. Read the generated JSON and both generated
HTML pages; inspect the complete diff. Run the relevant existing Holman
verification tests if main_verify_and_render_table.py names them as
preconditions.

The expected tracked changes are:

1. py/accgram/post_stress_meteg.py and py/author_site/post_stress_meteg.py,
   with their site_data.py constants and authored entry;
2. out/accgram/post-stress-meteg.json and gh-pages/post-stress-meteg.html, both
   new, plus gh-pages/index.html gaining one entry;
3. main_authored.py's render-from-JSON flag and the mega's use of it;
4. the renderer context metadata and the M23 contextual link;
5. the Phase 3 verifier module and the OWN entry point it runs from, never
   wired into main_verify_and_render_table.py; the two regenerated Holman HTML
   files; and any verification summary the verifier owns;
6. Phase 4's two renames: the three page-identity strings that become
   “Holman MAM suggestions” and the four reader-facing “Archived” labels; and
7. py/tests/test_site_index_links.py's new reverse-direction test, as its own
   commit.

The expected non-changes are:

1. MAM source data, Wikisource data, and MAM-parsed data;
2. M23's source message, comparison forms, and disposition;
3. the M17, M24, M32, and M34 dispositions;
4. meteg_silluq_context.py;
5. py/main_accgram.py and every accgram page, none of which this plan touches;
6. gh-pages/unicode-proposals.html, regenerated by gen_site and expected
   byte-identical; and
7. private-source text outside the bounded public excerpts.

After each completed phase, add a dated phase-state section to this plan. The
phase-state section records input revisions, the exact commands run, measured
figures, changed paths, and any explained mismatch with the historical
snapshot. After final verification, commit only the intended paths on main and
push main. Do not stage unrelated changes that were already present.
