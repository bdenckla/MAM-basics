# Near-Aleppo documentation edit status

State: live

Codex maintains this ledger for [Ben's requested edits](near-aleppo-requested-doc-edits.md).

## A96 — Stored note bodies and HTML presentation

**Status:** implemented by Codex, 2026-10-06.

**Assessment:** The quoted sentence remains true for the JSON dataset, but its scope was unclear.
The HTML edition's reviewed note presentations recast source clauses beside near-Aleppo's form;
the original JSON note bodies remain about MAM's target.

**Authorized scope:** Clarify the passage beginning “Two are MAM's note templates” in
`py/near_aleppo/doc_page.py`, regenerate `gh-pages/near-aleppo/reading-json.html`, and record
A96 here. Ben's request file is unchanged. The JSON dataset and example edition HTML are
expected to remain unchanged. The execution baseline is MAM-basics `617ceb42`.

**Change:** The JSON reference now explicitly scopes unchanged note bodies to the JSON dataset.
A following paragraph explains how the HTML edition recasts reviewed clauses as agreements
with near-Aleppo, places the remaining clauses after MAM's labelled form, and displays the
complete original note when a recast would require uncertain interpretation.

**Evidence:** `py/near_aleppo/phase6_mam_targets.py`, `MamTargets.add_to_e_cell`, rejects changes
to note parameters other than the target. `py/render_wt/render_wikitext_handlers.py`,
`_reviewed_doc_parts`, renders reviewed clauses beside near-Aleppo's form and the remaining
clauses with MAM's labelled form. Genesis 1:1 in `out/near-aleppo/plus/A1-Genesis.json` and
`gh-pages/near-aleppo/edition/A1-Genesis.html` demonstrates the stored and displayed versions.

**Verification:** Run from the MAM-basics repository root:

- `./.venv/Scripts/python.exe -m black py/near_aleppo/doc_page.py` passed.
- `./.venv/Scripts/python.exe py/main_near_aleppo.py --html` passed, including the shared
  renderer's comparison with the pinned tracked MAM-with-doc files. Only `reading-json.html`
  changed among the generated files; the dataset and example edition HTML remained unchanged.
- `./.venv/Scripts/python.exe py/main_near_aleppo.py --check-note-review` passed the fresh
  source enumeration and clause reviews.
- `git diff --check` passed.

The mega and full suite were skipped because the change clarifies rendered prose without
changing data or rendering logic.

## Annotation 1 — Planned template for marks without letters or space

**Status:** implemented by Codex, 2026-10-06; approved by Ben on the same date.

**Authorized scope:** Ben asked Codex to implement its recommendation to retain the original
decision and one concrete explanation under pending work, while removing the planned template
`ניקוד בלי אות ובלי רווח` from instructions for consuming the current dataset. Describe it as
a planned template for an outstanding case. The execution baseline is MAM-basics `a287e556`;
the source, development and integration checkout is `C:/Users/BenDe/GitRepos/MAM-basics`.

**Expected changes:** Update the shared consumer notice and generated JSON headers, the JSON
reference, the decision record, and the pending-work section. Refresh the presentation ledger's
input hashes through the maintained command. Scripture, note bodies, reviewed note dispositions,
sealed pointing inputs and example edition book pages must remain unchanged. Codex owns
verification, the commit and the normal push of `main`.

**Change:** The JSON reference and all 24 book notices now describe the three templates the
dataset uses. The original decision describes the reserved name as a planned template. The
pending-work section explains the intended use at 2 Samuel 18:20: MAM's note records tsere and
merkha without letters or space at the join inside a maqaf compound, while the current edition
still displays the full qere. The build and renderer still await that implementation.

**Verification:** Black passed on the four changed Python files. The dataset rebuild and
HTML regeneration passed, including the shared renderer's comparison against the 62 pinned
MAM-with-doc files. A comparison against `a287e556` verified that all 24 dataset changes are
confined to consumer notices; all 1,548 presentation-ledger entries are unchanged; and only
the ledger's 24 near-Aleppo input hashes changed. The only changed generated pages are
`reading-json.html`, `choices.html` and `coverage-and-status.html`. The planned template has
no mention in the JSON reference or book notices and one mention each in the decision record
and pending-work section. `git diff --check` passed.

The full suite, `./.venv/Scripts/python.exe py/main_test.py -q`, passed: 1,051 tests and
60 subtests passed, with 5 skips and one warning about permission to write pytest's cache.

The mega is skipped because the change is confined to near-Aleppo documentation and consumer
notice strings. The affected generator outputs were regenerated and inspected; build and
rendering algorithms did not change.

## A96 — Superseded by stored reviewed note content, 2026-10-06

**Status:** the earlier A96 implementation is superseded; baked note content is implemented
and verified.

**Authorization:** Ben instructed Codex on 2026-10-06: “Please make a plan to bake the
transformations in and execute it across whatever set of sessions and/or sub-agents it needs.”
The undertaking is recorded in `doc/PLAN-near-aleppo-note-content.md`. Ben's request file
remains unchanged.

**Change:** All 1,548 changed notes now contain the reviewed content in the book JSON.
Parameter 1 remains the near-Aleppo Scripture target. Parameter 2 contains the reviewed
near-Aleppo clause at 1,047 notes; it is an empty array at the 501 notes whose complete
original body remains in MAM context. `מקרא על פי המסורה` preserves the original
structured MAM target. `הערת מקרא על פי המסורה` contains the remaining original
clauses, or the complete original body. Scroll-note parameter 3 and flags retain their roles.
Codex's schema implementation uses `נוסח עם הקשר מקרא על פי המסורה` and
`הערה-2 עם הקשר מקרא על פי המסורה` so that consumers recognize the changed contract.

**Evidence:** `py/near_aleppo/note_content.py`, `NoteContent.apply`, matches each
review's complete source evidence and stores its approved parts. `doc_note_review.py`,
`inventory`, replays the pre-bake build from source inputs, keeping the historical nested
template names solely for the review's evidence identities. Every review is complete and
matches a fresh inventory before dataset writes. The renderer's `_stored_doc_parts` formats
the two stored roles; `edition.render_edition` reads no presentation recipe or review ledger.

**Verification:** Black passed on changed Python files. Dataset and HTML regeneration passed,
and the complete near-Aleppo check passed. All 1,548 ledger rows, including source evidence,
decisions and reasoning, compare exactly with baseline `a9c45ee1`; maintained metadata
removes the 24 published-output hashes and updates only the hash of the clarified pre-bake
MAM-target module. Six targeted differential and source-lint checks passed, including all
book-content invariants, all prior edition book and long-note pages, the 62-file independent
MAM-with-doc oracle, and removal of renderer review dependencies. The only generated HTML
changes explain the new contract in `reading-json.html`, `choices.html` and
`edition/index.html`. Scripture, C and D cells, flags, original MAM targets, sealed pointings and
edition book/long-note HTML remain unchanged. Root Codex independently passed the complete
near-Aleppo check, a three-check migration comparison against the execution baseline, and
the full mega's 60 steps. The full suite passed: 1,054 tests and 60 subtests, with five skips
and one warning about permission to write pytest's cache. Unrelated products remained
unchanged. `doc/PLAN-near-aleppo-note-content.md` is marked executed and records the completed
gates and the documentation-only origin update encountered during integration.

## A97–A101 — Retained-feature list and example, 2026-10-06

**Status:** implemented by Codex, 2026-10-06; authorized by Ben's instruction to process the
request file through A101.
A96 remains implemented by the stored-note-content work recorded above.

**Authorized scope:** Remove A97's tsinnorit/tsinnor list item, A98's assertion that the
holam-haser-for-vav code point records the manuscript's dot placement, A99's deḥi list item,
A100's tipeḥa/tarḥa list item, and A101's corresponding Psalms 40:13 example. Ben's request
file remains verbatim. No new manuscript judgment is needed for these removals.

**Checkout and baseline:** Source, development and integration checkout is
`C:/Users/BenDe/GitRepos2/MAM-basics`, a full clone on `main` at
`e47c7440abb4f28e713cc0a7bf9a38d0c031e5ae` before editing. The only existing modification
is Ben's updated request file. Codex owns the edits, verification, commit and normal push.
Commands run from this checkout's root with its own `.venv/Scripts/python.exe`.

**Expected changes and verification:** Change `py/near_aleppo/doc_registers.py`, remove the
unused example from `py/near_aleppo/doc_policy_examples.py`, and regenerate
`gh-pages/near-aleppo/editorial-policies.html`. Record each request's disposition here and
include Ben's verbatim request-file update in the commit. All datasets, source evidence,
review ledgers, edition book pages and other generated files must remain unchanged.
Format both changed Python files with Black, run `py/main_near_aleppo.py --html`, inspect
the generated diff and removed passages, and run `git diff --check`. The mega and full suite
are skipped because the edits remove documentation content and its unused example helper;
the actual HTML generator checks the affected surface and shared-renderer compatibility.

**Completed dispositions:**

| Request | Status | Change |
| --- | --- | --- |
| A97 | implemented | Removed the tsinnorit/tsinnor list item. |
| A98 | implemented | Removed the claim about the manuscript's dot placement; retained the holam-haser-for-vav item and its figures. |
| A99 | implemented | Removed the deḥi list item. |
| A100 | implemented | Removed the tipeḥa/tarḥa list item. |
| A101 | implemented | Removed the corresponding Psalms 40:13 example and its unused helper and import. |

**Verification:** Black passed on both changed Python files. HTML regeneration passed,
including the shared renderer's comparison with the 62 pinned MAM-with-doc files.
`editorial-policies.html` is the only changed generated file; its diff contains exactly the
requested removals and the joining punctuation in A98's retained item. All datasets, source
evidence, review ledgers, edition book pages and other generated files are unchanged. A search
of the affected source and page found none of the removed passages or the unused helper.
`git diff --check` passed. The mega and full suite were skipped for the documentation-only
scope explained above.

## A102 — Deferred beyond this task's cutoff

**Status:** deferred. Ben added A102 while A97–A101 were being implemented; the current
instruction authorizes processing through A101. A102's requested removal of “The sparseness
of the ketiv/qere” remains for a later instruction. The request-file update is preserved
verbatim, with no agent-written annotations.

## Review order and ketiv display — 2026-10-07

**Status:** implemented by Codex, 2026-10-07; authorized by Ben's review feedback
in this chat.

**Decisions:** Sort the maqaf section and the pasoleg section independently by book,
chapter and verse. Display ketiv as the primary text, with pointed qere above it using
HTML ruby. Ben chose ruby as the first display to try; synthesized notes or added note
clauses remain a deferred alternative if the ruby display proves unsuitable.

**Checkout and baseline:** Development is in `C:/Users/BenDe/GitRepos2/MAM-basics`,
on `codex/near-aleppo-ketiv-final-maqaf-20261007` at
`21385a303c30acca9163c59e810a3b923be484dc`, with no local edits before work.
Codex owns the edits, verification, commit and branch push. Main integration is deferred.
Commands run from this checkout's root with its own `.venv/Scripts/python.exe`.

**Expected changes and verification:** Adapt the shared renderer through a near-Aleppo
option, preserving MAM-with-doc's existing display. Regenerate the edition, its render-tag
report and both review files. Keep the dataset, selection, source notes, pointing inputs,
external punctuation and review dispositions unchanged. Use Black, focused near-Aleppo
checks, a differential comparison of both reading forms, browser layout checks and
`git diff --check`. The review trial leaves the mega and full suite to nightly checks.

**Change:** Both review sections now follow MAM's book order and numeric chapter and
verse, with change status retained as a label. The initial display at `37606647` showed
ketiv on the baseline and pointed qere above it at 75% of the baseline size; the later
size decision below supersedes that percentage. Trivial templates
use their pointed ketiv and pointed qere arguments; their source metadata is retained
on the annotation's hover. One-sided templates use CLC's editorial placeholders in
the missing reading's position. Existing unread-ketiv callouts and external punctuation
retain their behavior. No qere-note fallback was implemented; it remains Ben's deferred
alternative. The edition index and dataset README explain the display.

**Verification:** Six focused tests passed, with the existing pytest-cache permission
warning. HTML and review regeneration passed. A corpus differential against the serial
renderer preserved all ketiv forms, ordinary qere forms and literal text outside the
displays; trivial qere forms matched their stored arguments. All 65 serial book and
long-note pages reproduced the baseline exactly, and all 66 current edition pages matched
fresh rendering. MAM-with-doc regenerated byte-identically. The dataset, selection,
pointing inputs, note-review ledger and other near-Aleppo pages stayed unchanged.
Edge Chromium checks passed for section order, ketiv baselines, smaller qere above them,
embedded fonts, all extract text panels, slider sizes, narrow layout and print controls,
with no network requests or script errors. Desktop, narrow-layout and edition-row
screenshots were inspected. Black and `git diff --check` passed. The mega and full suite
were deferred under the approved review trial; these focused checks cover the changed
rendering surface. Main integration remains deferred.

## Ruby size and qamats investigation — 2026-10-07

**Status:** Size change implemented; the difference in Ben's screenshots is deferred
under the integration instruction below.

**Decision:** Ben requested 100% ruby text, matching CLC's `ruby.clc-kq rt` rule in
`gh-pages/uxlc/style.css`. The execution baseline is `37606647d246b588cbe71e9855db382124cff59e`
in `C:/Users/BenDe/GitRepos2/MAM-basics` on the existing review branch. The checkout was
clean before editing. Main integration remains deferred.

**Change and verification:** The edition's annotation is now the same size as its
baseline. The edition index and dataset README explain the equal size. HTML and review
regeneration changed only the edition index, its ruby stylesheet and the review HTML;
book pages, the plain-text companion and data stayed unchanged. Browser checks confirmed
equal sizes at the default and slider endpoints, above-baseline placement, narrow layout
and print behavior. The corpus differential continued to preserve reading forms and text
outside the displays. Actual edition browser checks passed for Numbers, 1 Chronicles,
Daniel and Ruth. Black and `git diff --check` passed. Broad checks remain deferred under
the approved review trial for this CSS and explanatory-prose change.

**Qamats disposition:** No font position was changed. The MAM-with-doc and near-Aleppo
font files in this clone, and MAM-with-doc's font in the primary forest, have identical
SHA-256 hashes. Controlled Edge Chromium comparisons of the same form at the same size
did not show a change in mark placement when square brackets were added or removed,
or when ruby alignment and kerning were varied. The vendored font source explicitly
offsets qof's below-mark anchor 120 font units to the right of its advance midpoint
(`sources/main_fill_in_template.py`, `A4_qof`, in the font's source archive under
`in/font-support/taamey-d-0.921/`). That is relevant font evidence, but it does not by
itself explain the apparent difference between Ben's screenshots. The early claim about
ordinary text is not a settled diagnosis of his browser's display. Genesis 3:11 was
provided as a reference with an ordinary final tav carrying qamats for Ben's comparison.

## Vertical ruby gap and main integration — 2026-10-07

**Status:** Implemented, integrated and pushed to main, 2026-10-07; authorized by
Ben's instruction to apply the package without waiting for the qamats investigation,
and to add vertical space between qere and ketiv.
This instruction supersedes the earlier deferments of main integration.

**Checkout and baseline:** Source, development and integration checkout is
`C:/Users/BenDe/GitRepos2/MAM-basics`, a full clone using its own environment.
The review branch began this phase at `726d906a559073ccc81d10734b4fb28b616b89a8`,
with a clean checkout. Current main, `0cf3f380a5f8d5dbbcbf7db2a2cd230c2c5ff46d`,
merged cleanly into the review branch as `8ba308a86a541d31c30da15347f88b09a94066ae`.
Codex owns the focused checks, commit, normal branch push, fast-forward of main and
normal push of main. The qamats diagnosis and trailing-space hypothesis are deferred.

**Gap decision and scope:** A CSS prototype in the extract confirmed that 0.2em of
padding below the ruby annotation leaves a visible gap while keeping the two readings
at equal size. The same source stylesheet serves the edition and extract. Regenerate
the stylesheet, index explanation and review HTML. Reading forms, external punctuation,
the selection, pointing data, book pages and plain-text companion remain unchanged
by this gap change. The complete integration includes the earlier final-punctuation
additions, the special separator correction, ketiv on the baseline, full-size qere above
it, and the sorted review extract with context and notes.

**Verification and integration sequence:** Use Black on changed Python, the maintained
HTML and extract generators, focused near-Aleppo and shared-HTML checks, the corpus
differential, browser checks and `git diff --check`. The review trial leaves the mega
and full suite to nightly checks. Immediately before integration, fetch origin again;
merge any moved main into the review branch and repeat affected checks. Then fast-forward
this clone's main to origin/main and the verified review branch, and push normally.

**Completed verification:** Six focused tests passed on the combined branch, with the
existing pytest-cache permission warning. An independent comparison against current
origin/main found exactly 36 added final maqafs and five added final pasolegs, with no
other frozen-record changes and an unchanged reviewed-pointing file. The corpus
differential preserved ketiv forms, ordinary qere forms and text outside the displays;
trivial qere forms matched their stored arguments. HTML generation and the extract's
read-only comparison passed. Gap measurements across all 98 extract ruby units were
4 px at size 20, 6 px at size 30, and approximately 9.6 px at size 48, with equal
baseline and annotation sizes. Browser checks passed for sorting, embedded fonts,
source text, sliders, narrow layout and print controls, with no extract network
requests or script errors. Actual edition checks passed for Numbers, 1 Chronicles,
Daniel and Ruth. Screenshots were inspected. MAM-with-doc regenerated without any
tracked change. The gap's generated differences are only its stylesheet, index
explanation and review HTML; book pages, data and the plain-text companion are unchanged.
Black and `git diff --check` passed. The mega and full suite remain deferred under
the approved trial; these focused checks cover the package and the combined branch.

**Integration result:** The verified review branch's `2f3013113b3c2abfa23a7cea30bb10b4eb5c441d`
was pushed as its backup. Fresh origin/main remained `0cf3f380`; this clone's main
fast-forwarded first to origin/main and then to `2f301311`. The normal push succeeded,
and both local HEAD and origin/main were verified at `2f301311` with a clean checkout.
The complete package is on origin/main. The qamats diagnosis and trailing-space
experiment remain deferred; no font positioning or speculative spacing workaround
was included. This completion entry is a documentation-only follow-up on main.

## NAEE final-mark investigation and ruby correction — 2026-10-07

**Status:** The broader final-mark displacement is reproduced and fixed in the
near-Aleppo example edition (NAEE) and punctuation extract. This investigation
supersedes the earlier qamats deferment.

**Authorization and baseline:** Ben asked to examine qere with other final marks
below and above once ruby was used throughout NAEE. The narrow CSS repair follows
the existing display policy and routine-repair authority in `doc/review-trial.md`.
Source, development and integration checkout is `C:/Users/BenDe/GitRepos2/MAM-basics`,
a full clone on main at `c9a589d84f3bc0ad563e0ba7f5c44b80024137e5`, clean before
editing. Codex owns verification, the commit and normal push of main.

**Survey and finding:** The 39 main book pages contain 1,185 Scripture qere
annotations, excluding note lemmas. Of these, 309 have marks below or above their
final Hebrew letter, representing 19 distinct Unicode code points. For multi-atom
qere, this survey examines the final atom; trailing punctuation and stored mark
order are preserved. In controlled Edge comparisons against the same qere HTML
outside ruby, 101 of these 309 annotations differ beyond one pixel of raster
rounding at both the normal edition size, 26.133333 px, and an enlarged size of
48 px. Representative differences include tevir and merkha below, and pashta and
zaqef qatan above. The effect therefore extends beyond qamats.

**Correction:** `py/near_aleppo/edition.css`, at the selector
`ruby.near-aleppo-kq > rt > span`, makes the annotation's span an inline block
with normal line height. Changing only this layout rule removes every detected
discrepancy in the 309 annotations at both sizes. The earlier font-anchor evidence
does not explain the ruby-versus-ordinary-text difference; the early ordinary-text
claim was too broad. The controlled comparison supports a ruby-layout diagnosis;
the browser engine's internal cause remains unverified. Forcing mark features or
adding a trailing space inside the qere span did not repair the representative
cases. No font file or Hebrew text was changed.

**Verification and product scope:** HTML and extract regeneration passed. Their
only tracked generated changes are the deployed NAEE stylesheet and the extract's
embedded copy of that stylesheet. Book pages, datasets, selection data,
MAM-with-doc, external punctuation and the plain-text companion remain unchanged.
The corpus differential again preserved reading forms and text outside the ruby
displays across 69,606 verse fields. Extract checks preserved section order, source
panels, embedded fonts, slider sizes, narrow layout and print controls, with no
script errors. Actual edition checks passed for Numbers, 1 Chronicles, Daniel
and Ruth. All 98 extract ruby units retain equal reading sizes and gaps of 4 px
at size 20, 6 px at size 30, and approximately 9.6 px at size 48.

A local comparison page shows original ruby, corrected ruby and ordinary qere
for 31 representative cases covering all 19 mark types. Its corrected cases
match ordinary controls within one pixel, with identical text and size, loaded
fonts and no script errors or network requests. The page's screenshot was
inspected. The decisive comparison registers each whole glyph raster before
comparing the positions of marks relative to letters. `git diff --check` passed.
The mega and full suite are deferred to nightly checks under the approved trial;
the change is confined to CSS and the focused differential and browser checks
cover its effects.

## Features of interest and verse links — 2026-10-08

**Status:** Implemented by Codex, authorized by Ben's request for a near-Aleppo
features-of-interest document whose first entry is interesting ketiv/qere,
starting with the four entries from the preceding reply.

**Checkout and baseline:** Source, development and integration checkout is
`C:/Users/BenDe/GitRepos2/MAM-basics`, a full clone on main at
`f9d817b1d292babf1ed742cba32b6cd183f6d4c7`, clean before editing. Codex owns
the generation, focused checks, commit and normal push. The clone's own
`.venv/Scripts/python.exe` runs each command from the repository root.

**Change:** `gh-pages/near-aleppo/foi/index.html` starts with a link to
`interesting-ketiv-qere.html`. The guide begins with 2 Samuel 8:3, Isaiah 54:16,
Genesis 30:11 and a qere-without-ketiv entry containing Ruth 3:5 and Judges 20:13.
The initial guide showed each current NAEE ruby in a table, with relative verse
links and separate published links from the shared verse-link builder. The
full-verse layout revision below supersedes that presentation. The dataset
overview and edition index link to the FOI index.

**Maintained source and reproduction:** `py/near_aleppo/features_of_interest.py`
owns the ordered selection and explanations. It uses Scripture rendered with
the existing NAEE policy, excluding note lemmas; no copied Hebrew forms or new
template interpretations are introduced. The ordinary
`./.venv/Scripts/python.exe py/main_near_aleppo.py --html` command regenerates
both pages. The README records that command. `py/main_verse_links.py` now accepts
`--near-aleppo` to print a verse's local file URL for the calling checkout and
its published URL, without changing the default link output.

**Verification and scope:** Black passed on the six changed Python files. HTML
generation and its read-only comparison passed for all 83 owned output files.
The only changed existing generated pages are the dataset overview and edition
index, each adding FOI navigation. All book pages, datasets, review files and
MAM-with-doc remain unchanged. A differential browser check matched all five
guide examples to their main Scripture displays in the actual edition. Every
verse link landed on its unique anchor; the shared NAEE builders also matched
all 39 edition filenames and first-verse anchors, including the filename with
spaces. The optional CLI links matched the guide, and the default CLI output
matched the committed source's output. The requested entry order, equal reading
sizes, vertical gap, fonts and narrow layout passed, with no script errors.
Desktop and narrow screenshots were inspected. Ten existing stylesheet/font
and source-hygiene checks passed, with the existing pytest-cache permission
warning. `git diff --check` passed. The mega and full suite are deferred to
nightly checks under the approved trial; focused regeneration, the edition
differential and the mechanical checks cover this navigation and guide change.

## Notes for applications — 2026-10-08

**Status:** Implemented by Codex, authorized by Ben's correction that this section
is for "quick mentions of the most common pitfalls, with a link to more extensive
documentation" rather than detailed template specifications.

**Checkout and baseline:** Source, development and integration checkout is
`C:/Users/BenDe/GitRepos/MAM-basics`, a full clone on main at
`c0fa37c0f80af9b1b2098df83a34b326898cca15`, clean before editing.

**Change:** Shortened the shared notice's first two bullets to the closed-dispatch
and Scripture-versus-metadata pitfalls. The added marks template gets only a
passing mention. The section introduction links to the template definitions,
GAV notation and display, and added-parameter roles. Those detailed sections
already contained the specifications and remain unchanged. The release-notes
draft now links directly to the detailed template and parameter sections.

**Verification:** Black and the focused unused-import check passed on both changed
Python files. Dataset and HTML regeneration passed. An independent comparison of
all 24 book files found changes only to the first two consumer-notice rules;
all other headers, Scripture and note content are unchanged. The generated
`reading-json.html` changes only under "Notes for applications", with all three
links targeting existing sections. No other generated page, pointing input,
population file or note-review ledger changed. The three existing prose lints
passed, and `git diff --check` passed. The mega and full suite are deferred under
the approved trial; focused regeneration and differential checks cover this
documentation and dataset-header change.

## Full verses and linked headings in the k/q guide — 2026-10-08

**Status:** Implemented by Codex. Ben requested entire verses for the four
existing groups, removal of the published URLs and tables, and a verse link on
the BCV portion of each heading. This supersedes the initial table presentation.

**Checkout and baseline:** Development and integration remain in the full clone
`C:/Users/BenDe/GitRepos2/MAM-basics`, on main at
`c0fa37c0f80af9b1b2098df83a34b326898cca15`, clean before editing. Codex owns
the focused checks, commit and normal push using this clone's environment.

**Change:** The guide now shows the complete rendered Scripture verse in an RTL
paragraph for each reference. The BCVs in the first three headings are links;
Ruth 3:5 and Judges 20:13 have separate linked subheadings within the fourth
group. The heading links open the corresponding NAEE verses with surrounding
text and notes. Tables and separate published URLs are removed. The selection
and group order are unchanged. Guide-specific line spacing leaves room for
full-size qere annotations when verses wrap. The README describes the current
layout; its existing HTML command regenerates the guide.

**Verification and scope:** Black passed. HTML regeneration and read-only
comparison passed for all 83 owned files. The only changed generated page is
`gh-pages/near-aleppo/foi/interesting-ketiv-qere.html`. Its text was read, and
desktop and narrow screenshots were inspected. A browser differential matched
all five complete verse displays to the corresponding Scripture cells in the
actual NAEE book pages. Every linked heading landed on its unique verse anchor.
At widths 1400, 500 and 390 px, annotations had a positive vertical gap, equal
reading sizes where both readings exist, no overlap with adjacent wrapped lines,
and no horizontal page overflow. Fonts loaded and no script errors occurred.
The guide has no tables or external published links. Book pages, datasets,
the FOI index, the two navigation indexes, review files and shared styles remain
unchanged. `git diff --check` passed. The mega and full suite remain deferred
to nightly checks under the approved trial; regeneration and the full-verse
and layout differential cover this guide-only change.
