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

## CLC box styling correction — 2026-10-08

**Status:** Corrected by Codex after Ben pointed out that borrowing CLC's k/q
presentation included its box. The earlier implementation copied only part of
CLC's presentation; the omitted box and the initial 75% annotation size were
unsupported styling choices. The size was already corrected to 100%.

**Checkout and baseline:** Development and integration remain in the full clone
`C:/Users/BenDe/GitRepos2/MAM-basics`, on main at
`3f476dedeee133d50cee8ea973c434d7ffeae4e6`, clean before editing. Codex owns
the focused verification, commit and normal push using this clone's environment.

**Correction and style comparison:** Each NAEE k/q unit now has the same
inline-block box wrapper as CLC. `py/near_aleppo/edition.css` copies the box rule
from the authoritative `gh-pages/uxlc/style.css`: a 1 px border with the same
light/dark colors, 0.25em corners, 0.15em horizontal padding and 0.05em horizontal
margins. The wrapper encloses both readings. The shared page writer's optional
breaks inside a reading are suppressed within the box so a grouped unit stays
together, as CLC's units do. The renderer's note-callout compatibility unwraps
the box before the existing unread-ketiv decision. The complete edition, its
long-note pages, the FOI guide and the punctuation extract use the box.

NAEE retains the requested pointed ketiv baseline, full-size pointed qere above
it, and vertical gap. Its existing mark-positioning repair is retained. The
source-style comparison also confirms CLC's ruby position, annotation percentage
and small muted missing-reading labels. The new differential check in
`py/tests/test_near_aleppo_clc_style.py` compares these declarations with CLC's
actual stylesheet, rather than pinning copied values.

**Verification and scope:** Black passed on changed Python. HTML and extract
regeneration passed; the HTML read-only comparison passed for all 83 owned
files. Six existing near-Aleppo, note-content and stylesheet checks passed, and
the new CLC-style differential passed in its own run. Both runs had the existing
pytest-cache permission warning. Browser checks visited all 68 edition/index,
FOI-guide and extract pages and checked 1,712 boxes in each of light and dark
modes. Every ruby has one enclosing box containing both readings, equal sizes
where both readings exist, and a positive vertical gap. Box styles match CLC's
computed styles in the effective color scheme; the extract retains its existing
fixed light theme. Light and dark screenshots were inspected.

After removing only box wrappers and serializer whitespace, all 65 book and
long-note pages match the baseline, preserving notes and callouts. The five
FOI verse paragraphs and the extract's source-data JSON are unchanged. The
corpus differential preserved both reading forms and text outside k/q across
69,606 verse fields. The guide's whole-verse differential and desktop, 500 px
and 390 px layout checks passed without overlaps, page overflow or script errors.
MAM-with-doc regenerated byte-identically. CLC, all data, selection files,
external punctuation and the review's plain-text companion remain unchanged.
Generated differences consist of the box wrappers, deployed and embedded CSS,
and the edition-index and FOI introductions describing the box. The README now
describes the corrected display. `git diff --check` passed. The mega and full
suite remain deferred to nightly checks under the approved trial; these focused
regeneration, style, reading-form and generated-output differentials cover the
shared-renderer change.

## Two additional k/q guide entries — 2026-10-08

**Status:** Implemented by Codex. Ben requested Isaiah 26:20, subject to checking
the reference, and the similar case with ketiv בנימן inside a maqaf compound.
The references are confirmed in the stored near-Aleppo data and its rendered
edition: Isaiah 26:20 and 1 Chronicles 9:4.

**Checkout and baseline:** Source, development and integration checkout is the
full clone `C:/Users/BenDe/GitRepos2/MAM-basics`, on main at
`4a43d330de4369d627927698ffbcb42b3b8ec9de`, clean before editing. Codex owns
the focused verification, commit and normal push using this clone's environment.

**Change:** Append the two entries to `py/near_aleppo/features_of_interest.py`.
Isaiah 26:20 highlights the yod in ketiv דלתיך that is absent from qere דלתך;
1 Chronicles 9:4 highlights the single ketiv atom בנימן with its two-atom qere
inside a longer maqaf compound. Both entries show the complete rendered verse
and link the BCV in the heading to NAEE. The first four groups keep their order.

**Verification and scope:** Black passed. HTML regeneration wrote all 83 owned
pages; only `gh-pages/near-aleppo/foi/interesting-ketiv-qere.html` changed.
The HTML read-only comparison passed for all 83 pages and both font copies.
The generated diff consists of the two contents links and two verse sections.
A browser differential matched all seven verse displays to NAEE and checked
all seven heading links. At widths 1400, 500 and 390 px, fonts loaded, reading
sizes agreed, vertical gaps were positive, and there was no annotation overlap,
horizontal overflow or script error. Desktop and narrow screenshots were
inspected. Five focused source-hygiene, mark-literal and stylesheet checks
passed. The dataset, book pages, punctuation review and shared styles remain
unchanged. The full mega and suite remain on the nightly cadence under the
approved trial; focused regeneration and the whole-verse differential cover
this guide-only addition.

## Ruby box vertical clearance — 2026-10-08

**Status:** Corrected by Codex after Ben reported a box with excess space below
the ketiv and asked whether the upper border could collide with qere accents.
The rendered 1 Kings 22:49 and Job 1:10 examples confirm upper marks touching
the old border. This supersedes the earlier inline-block wrapper layout while
retaining CLC's border appearance and horizontal spacing.

**Checkout and baseline:** Development and integration remain in the full clone
`C:/Users/BenDe/GitRepos2/MAM-basics`, on main at
`6d09c8862e1f1aaf9eac43dbec701d8611651b06`, clean before editing. Codex owns
the focused verification, commit and normal push using this clone's environment.

**Cause and correction:** The wrapper inherited its surrounding line height.
In the FOI that left 21 px below the ketiv text rectangle versus 1 px above
the qere rectangle. `py/near_aleppo/edition.css` now gives the wrapper normal
line height, inline-flex layout and 0.15em padding on all sides. Flex layout
includes the annotation within the upper padding; adding padding to the old
inline-block wrapper enlarged only the space below it. The FOI's corresponding
text-rectangle clearances are now 5 px above and 6 px below. CLC's border,
corners, horizontal padding and margins remain; reading sizes, horizontal
widths and the gap between readings are unchanged. The style differential now
compares those borrowed properties while leaving wrapper layout and vertical
padding to NAEE. The README describes this clearance.

**Verification and scope:** HTML and punctuation-review regeneration passed.
An independent comparison with the baseline verified all 85 NAEE assets:
only the deployed ruby stylesheet differs. The review HTML differs only by
the same CSS replacement; its data, rendered content and plain-text companion
remain unchanged. Font copies, edition pages, FOI content, notes, Scripture,
CLC and MAM-with-doc are unchanged.

Browser checks measured 1,714 boxes across 68 edition, FOI and extract pages,
including 880 qere displays whose ink extends above the plain letters. The
loaded font's measured upper ink clearance improved from a minimum of -1 px
to about 2.9 px inside the border; minimum lower clearance is about 6.9 px.
All readings retain their font sizes, widths and positive gap. The seven FOI
verses still match their edition displays and all heading links resolve.
Desktop, 500 px and 390 px checks passed without overlaps, page overflow or
script errors; screenshots of the guide and the two upper-mark cases were
inspected. Three focused CLC-style, stylesheet/font and extract checks passed,
and Black passed on the changed Python test. The mega and full suite remain
on the nightly cadence under the approved trial; focused regeneration,
content comparisons and browser geometry checks cover this CSS correction.

## Qere-without-ketiv manuscript study — 2026-10-08

**Status:** Implemented by Codex as the first draft Ben approved: “what you
propose seems fine, at least as a first draft.” Further discussion continues
alongside implementation.

**Checkout and baseline:** Source, development and integration checkout is
`C:/Users/BenDe/GitRepos/MAM-basics`, a full clone on main at
`5eab49e09093556373054fd2a6b3458dab9b8c8b`, clean before editing.

**Change:** The FOI index and existing ketiv/qere guide now link to
`gh-pages/near-aleppo/foi/qere-without-ketiv.html`. Its nine entries show current
NAEE verses, current MAM qere and attached notes, and generated verse lookup links.
Ben's four dated image readings and supplied crops are displayed inline; the five
entries awaiting image readings are labelled accordingly. The Samuel assessments
identify the notes reviewed on 2026-10-08, with their exact quotations retained in
the reading metadata. Tentative readings and the Judges line-ending hypothesis
remain qualified.

**Maintained home:** `in/near-aleppo/qere-without-ketiv-readings.json` owns the
observations and crop provenance; `in/near-aleppo/img/qere-without-ketiv/` owns the
unchanged PNGs. The shared renderer supplies current Scripture and notes.
`doc/near-aleppo-qere-without-ketiv/README.md` documents maintenance and provenance.
The preserved Downloads bundle's generator README points to this tracked study.
Book datasets, pointing inputs, template policy and Ben's requested-edit file
remain unchanged.

**Verification:** Black passed on both changed Python files. HTML regeneration
and read-only comparison passed for all 88 owned files and both font copies.
An independent artifact differential matched all nine complete NAEE verses and
ruby trees, all nine MAM qere displays and six attached MAM notes. All local links
resolve, and the four supplied, canonical and generated crops have identical
bytes. The six focused test files passed (16 tests); the stylesheet lint passed
again after the final note-font adjustment. A read-only agent review found no
remaining material fidelity issue. The generated page was read, all existing
generated diffs were inspected, and `git diff --check` passed. The mega and full
suite are deferred to nightly checks under the approved trial; focused generation,
the artifact differential and mechanical lints cover this FOI and documentation
change.

**Integration:** Origin advanced to `ba3e0d483c94fa484a54f797d7381fe5db23aa52`
before the push. The normal merge preserves the incoming boxed NAEE rendering,
separate guide additions and all live-ledger entries. The study was regenerated
with that renderer; HTML comparison and the nine-entry artifact differential
passed again. Three focused CLC-style, stylesheet and prose-order checks passed.
Relative to incoming main, the study changes no book dataset or pointing input.

## Final dalet carrier at Isaiah 54:16 — 2026-10-08

**Status:** implemented by Codex, 2026-10-08.

**Authorized scope:** Ben requested all three final-nun marks on an artificial
dalet using the template `ניקוד בלי אות ובלי רווח`, updated documentation,
a font comparison, and an issue in the hbofonts tracker about Taamey D's
detached dagesh. This fresh session executes the supplied Codex handoff.
Source, development and integration checkout is
`C:/Users/BenDe/GitRepos2/MAM-basics`, clean on main at required baseline
`ebaae10fbdfcda32e91f054f0739b2f10d9a4f54`, using its own environment.

**Expected changes:** One reviewed pointed-ketiv value, explicit dalet validation
and closed dispatch, consumer notices, carrier and edition explanations,
editorial decisions, and their generated consequences. Ketiv letters, qere,
GA/GV payloads and validation, all other Scripture forms, and MAM-with-doc
remain unchanged. The artificial dalet carries dagesh, tsere and mahapakh
immediately after the final nun with no space. The marks remain associated
with the final nun; this font accommodation supplies no ownerless-mark
manuscript claim. The planned use at 2 Samuel 18:20 remains pending.

**Verification scope:** Focused build and HTML regeneration, affected extract
regeneration, shared-renderer comparison, corpus differential, mechanical
source checks, Black on changed Python, and actual-font browser inspection.
Full mega and suite remain on the approved nightly cadence.


**Implemented encoding:** Reviewed record `C1-Isaiah:54:16:0` now stores
`["הִן", {"tmpl_name":"ניקוד בלי אות ובלי רווח",
"tmpl_params":{"1":"דֵּ֤","carrier":"final-nun-dalet"}}]`.
The new template has an explicit `_CARRIERS` build dispatch and shared renderer
dispatch. The central guard accepts exactly this GD discriminator and mark
shape; GA/GV guards are unchanged. The existing k/q display-order helper already
uses that central guard. The edition renders `הִן«דֵּ֤»` with no space, under the
unchanged qere `הִנֵּ֤ה`. Carrier documentation, consumer rules, decisions,
edition explanation, build guide and README now describe GD. The `gav-display`
anchor remains. The pending 2 Samuel 18:20 use requires its own future variant.

**Filed:** [hbofonts issue 123](https://github.com/bdenckla/hbofonts/issues/123)
requests direct Taamey D support. The issue records agent authorship, the supplied
handoff's quotation of Ben's instruction, exact codepoints and a rendering
reproduction. Full reads of hbofonts issues 99 and 33 found no duplicate of
this case; the issue was read back after filing. The frozen 0.921 source explicitly
omits final-nun+dagesh composition by design, while its GPOS has an attachment
anchor. The issue distinguishes composition from all attachment support.

**Font comparison:** The local artifact is
`.novc/isaiah54-16-font-comparison-20261008.html`, with companion
`.novc/isaiah54-16-font-evidence-20261008.json` and five screenshots.
The sheet compares source original, actual regenerated carrier markup and
ordinary-nun qere, in ordinary text and actual NAEE ruby markup/CSS, at 32,
48 and 72 px and CSS weight 400, with synthetic bold disabled. Font files,
name-table versions and SHA-256 hashes appear in the sheet and evidence JSON.

The tested installed versions are Taamey D 0.921 (its sole face is named Medium,
used at CSS weight 400), SBL Hebrew 1.56a Build 016, Ezra SIL 2.51 (2007),
Times New Roman 7.12 and Arial 7.06. Headless Edge 154.0.4258.62 on
Windows 11 Pro 10.0.26200 x64 rendered at viewport 1280 × 1000 CSS pixels,
DPR 1. CDP actual-font evidence checked 27 reading spans per font and the
edition's frozen 0.921 webfont separately. Every Hebrew span used the requested
font. Taamey D lacks guillemets; their explicit Arial fallback is identified.
No requested font was missing. The newer sibling hbofonts build 0.931 was not
substituted. All six screenshots were inspected: the original's dagesh is
detached in every tested font, while GD places the dot with dalet in ordinary
text and ruby. These findings describe the tested environment and versions.

**Verification:** Black passed on all eleven changed Python files; focused tests
passed, 19 tests with the existing pytest-cache permission warning. Build,
HTML and punctuation-extract regeneration passed. MAM-with-doc regenerated
byte-identically. The corpus differential against the baseline found exactly
24 changed consumer notices and one pointed-ketiv value; all ketiv consonants,
whole qeres, notes and other Scripture text are unchanged. The Isaiah edition HTML differs only in the one ketiv display. The FOI
guide additionally updates that case's title and explanation: the artificial
dalet and guillemets make the old “wider qere” description false. Actual
rendered widths were 56.875 CSS pixels for the ketiv display and 35.171875 for
the qere. The guide now explains the additional qere he and final carrier. The four changed
generated documentation pages contain only the documented GD consequences.
Build populations, note-review ledger, punctuation extract and render-tag
reports remain unchanged. Validation differentials agree with the baseline
over all 64 stored GA/GV templates, retaining their dagesh prohibition.
A mechanical check rejects 106 altered GD payloads or parameter shapes.
No earlier stored carrier is final. Read-only product comparison and
`git diff --check` passed. Full mega and suite remain on the nightly cadence
under `doc/review-trial.md`; no consequence requires immediate broad checks.


**Integration:** The carrier implementation was committed as `b9c4dd09`.
Fetched origin/main advanced to `7c82b5df6deeee66568830bf63b7ba0a2cee1350`.
The normal full-clone merge preserves the incoming 2 Kings 14:7 pointing,
qere-without-ketiv study, Ezekiel decision record and both live-ledger entries.
Only the ledger's concurrent append needed manual resolution. The combined
build and all 88 HTML products regenerated without additional differences.
The corpus and GA/GV/GD differentials passed again against incoming main,
isolating exactly this task's notices and Isaiah payload. The combined tree's
19 focused tests passed again with the existing cache-permission warning;
the HTML read-only comparison passed for 88 files and both font copies.
The carrier implementation files and reviewed Isaiah payload are unchanged
from `b9c4dd09`. Mega and full suite remain on the approved nightly cadence.


**Final incoming main:** Origin advanced again to `df5519d4`, adding instruction
updates and the census note-reader refactor. The normal merge was clean.
The complete maintained `py/main_near_aleppo.py --check` passed: all five
census baselines, 24 dataset files and their population metadata, 1,548 source
note reviews, 88 HTML files and both font copies agree. The task differential
passed again against `df5519d4`; the final carrier implementation is unchanged.
The directly relevant dataset and note-content tests passed after this merge.
No additional generated differences arose. The full mega and suite remain
on the approved nightly cadence, as the final commit message records.

## Isaiah 26:20 guide correction — 2026-10-11

**Status:** Corrected by Codex after Ben questioned the reference and identified
the intended case as ketiv/qere in the middle of a three-atom maqaf compound.
The BCV was correct. The earlier entry's passage “Isaiah 26:20 highlights the
yod in ketiv דלתיך” selected the verse's separate, ordinary pair rather than
the intended MAM ketiv יעבור and qere יַעֲבׇר.

**Checkout and baseline:** Source, development and integration checkout is the
full clone `C:/Users/BenDe/GitRepos2/MAM-basics`, clean on main at
`2265bf9cde517502571b6f848c950c3c0394feaa` before editing.

**Correction:** The guide's Isaiah entry now identifies MAM's compound
עַד־יַעֲבׇר־זָֽעַם and links to its MAM-with-doc display. It explains NAEE's
existing display עַד־יַעֲבָור־זָֽעַם without qere above the middle atom:
MAM's note reports the ketiv and no qere note in the Aleppo Codex. In forming
the near-Aleppo dataset, we inferred the ketiv's pointing from the qere. This
correction attributes the manuscript report to MAM's note; no manuscript image was
consulted. The initial description distinguished the earlier boxed דלתיך / דלתך pair;
the later excerpt change below omits that pair and removes its explanation.

**Verification and scope:** Black passed. HTML regeneration changed only the
guide among the 88 generated files. An independent comparison confirmed that
all seven guide verse paragraphs are byte-identical to the baseline, all guide
links and anchors resolve against the local published products, and the MAM
and NAEE datasets support the corrected description. The 12 focused source
hygiene, accent-mark literal and prose mark-order checks passed, with the
existing pytest-cache permission warning. Scripture, pointing inputs, edition
book pages and shared styles are unchanged. The full mega and suite remain
on the approved nightly cadence; focused regeneration and the artifact
comparison cover this guide correction.

**Wording correction, 2026-10-11:** Corrected by Codex at Ben's request.
The guide now says “In forming the near-Aleppo dataset, we inferred the ketiv's
pointing from the qere” rather than attributing the inference to NAEE.
Black and HTML regeneration passed; the generated diff changes only that
sentence and its line wrapping. The live ledger's description is corrected
in place. Data and verse displays are unchanged.

**Excerpt and ink correction, 2026-10-11:** Implemented by Codex at Ben's
request. The Isaiah display now replaces the first half, through the
atom בַּעֲדֶ֑ךָ, with an ellipsis. The displayed second half comes from
the existing rendered verse, and the entire final three-atom compound uses
the existing teal `example-difference` ink color in light and dark mode.
The ordinary ketiv/qere is no longer displayed; its explanatory sentence
is removed. The edition book page and dataset are unchanged.

Black and HTML regeneration passed; only the guide changed among the 88
generated files. An independent artifact comparison confirmed that the six
other guide verse displays are byte-identical and that the excerpt matches
the complete second half in NAEE's book page. Headless Edge checks passed
at 1100 and 390 px in light and dark mode: the whole compound inherits the
contrasting ink, Hebrew fonts load, direction is RTL, and no page overflow
or script error occurs. All four screenshots were inspected, and the three
focused accent-literal and prose mark-order checks passed. Broad checks
remain on the approved nightly cadence; the focused artifact differential
and visual checks cover this presentation change.

## Link presentation trial on the manuscript study — 2026-10-11

**Status:** Implemented by Codex, authorized by Ben's request to research
Wikisource, other approaches and MAM-basics precedents, then implement an
experiment in `qere-without-ketiv.html`. Ben's subsequent approval and the broader
rollout are recorded under “Shared arrow links across near-Aleppo pages” below.
Development and integration use the full clone `C:/Users/BenDe/GitRepos/MAM-basics`
on main at `79c923957188007a2ffd70dd6ece60103cbeec97`, clean before editing.

**Change:** The page uses un-underlined clickable labels with trailing link
markers, a hover background and a keyboard-focus outline. Same-page jumps,
other MAM-basics pages and external providers have distinct arrow shapes.
The locally authored CSS and inline SVG masks are embedded by the page's own
generator. Shared styles, other pages and link-opening behavior are unchanged.
`doc/near-aleppo-qere-without-ketiv/README.md`, “Link presentation trial”, records
the research sources, current repository precedents and the bounded design.

**Verification:** Black, HTML regeneration and read-only comparison passed for
all 88 owned files and both font copies. The exact body differential matches
the baseline after removing only the new body and external-link class attributes;
Hebrew order, RTL markup, labels, URLs, observations and image references are
unchanged. All three SVG masks parse as self-contained SVG; declared normal and
visited colors have at least 6.02:1 contrast against the normal and hover
backgrounds. The existing stylesheet test passed, and `git diff --check` passed.
Only the study page changed among existing generated artifacts. Book datasets,
pointing inputs, observations and crops are unchanged.

**Unverified visual checks:** Browser security policy blocked the local preview
because `file:` URLs are disallowed. Visual layout and keyboard behavior await
Ben's local review; no passing browser check is claimed. Mega and full suite
remain on the approved nightly cadence. Focused generation and offline
content/style checks cover this reversible page-specific experiment.

## Shared arrow links across near-Aleppo pages — 2026-10-11

**Status:** Implemented by Codex after Ben approved the study's arrow links and
requested the presentation across near-Aleppo-related pages. Ben also asked
whether a same-page link to an earlier anchor would use an up arrow.

**Checkout and baseline:** Source, development and integration checkout is the
full clone `C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`97cb7825cd6b3b1991e9300a7bf5913690e504a7` before editing. Codex owns the
implementation, verification, commit and normal push. A read-only agent
inventoried the affected pages and reviewed the integration.

**Change:** All 77 HTML pages under `gh-pages/near-aleppo/` and the maintained
standalone final-punctuation extract use the approved link presentation.
`py/near_aleppo/link_presentation.py` inserts presentation attributes into the
original rendered HTML and assigns up/down arrows by comparing each same-page
link with its target in document order. Other MAM-basics pages retain a right
arrow; destinations outside MAM-basics retain a boxed outward arrow. The shared
authored stylesheet is `py/near_aleppo/link_presentation.css`; publication uses
one generated copy, and the offline extract embeds it. The extract permits data
images in its content security policy for the self-contained SVG masks. The
study's private CSS now owns only its layout.

**Verification:** Black passed on all four changed Python files. The actual
HTML and extract generators and their read-only comparisons passed: 89 owned
HTML-build files, both font copies and both extract files are current. Three
focused renderer, CLC-style and shared-stylesheet tests passed. An independent
artifact differential confirmed all 78 page bodies are byte-identical to the
baseline after removing only presentation attributes. All 2,533 links retain
their labels and destinations; every local fragment resolves and its arrow
matches document order. The three upward links occur under “Notes for
applications” in `reading-json.html`. All three SVG masks parse without remote
dependencies. Hebrew order, RTL markup, source-data scripts, book datasets,
pointing inputs, observations, crops and the plain-text extract are unchanged.
The read-only agent review found no material integration issue, and
`git diff --check` passed.

**Verification limits:** Ben reviewed and approved the original presentation.
Automated visual and keyboard checks retain the earlier browser-policy block
on local `file:` previews; no automated browser pass is claimed. The full mega
and suite remain on the approved nightly cadence. Focused generation, complete
artifact comparisons and mechanical link checks cover this presentation rollout;
no consequence requires immediate broad checks.

## Arrow links on the top-level index — 2026-10-11

**Status:** Implemented by Codex at Ben's request to apply the arrow
link convention to `gh-pages/index.html`.

**Checkout and baseline:** Source, development and integration checkout is the
full clone `C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`b8a4e72256950749bd5554f2cc7bbba6f651eb27` before editing. Codex owns the
implementation, focused verification, commit and normal push.

**Change and scope:** `py/author_site/site_index.py` applies the existing shared
helper and loads `near-aleppo/link-presentation.css`. The helper now accepts an
explicit page directory so the top-level index is located at the website root;
near-Aleppo callers retain their default. The index has no same-page anchors;
its 28 links to MAM-basics pages use right arrows and its 15 links to external
destinations use boxed outward arrows.

**Verification:** Black passed on both changed Python files, and the maintained
`py/main_authored.py gen-site` completed. An independent comparison confirmed
the complete index is byte-identical to the baseline after removing only
presentation attributes and the shared stylesheet reference; all 43 link cues
match their destinations. The existing index and shared-stylesheet lints passed,
four tests. Near-Aleppo HTML and standalone-extract read-only comparisons passed
without generated differences. All other root pages, Hebrew and RTL markup,
datasets and study inputs are unchanged. `git diff --check` passed.

**Verification limits:** The unchanged styles use Ben's approved presentation;
automated visual and keyboard checks retain the previously documented local
preview restriction. Mega and full suite remain on the approved nightly cadence.
The real generators, complete-page differential and focused lints cover this
extension; no consequence requires immediate broad checks.

## Retirement of the completed punctuation extract — 2026-10-11

**Status:** Retired by Codex after Ben proposed removing the page and asked
whether it reviewed the completed legarmeh/maqaf additions.

**Checkout and baseline:** Source, development and integration checkout is the
full clone `C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`dc57597b8b797d7f1ac9a7747cbee5c8af1b6859` before editing. Codex owns the
retirement, focused verification, commit and normal push.

**Completion evidence:** “Vertical ruby gap and main integration” above records
the completed 2026-10-07 package at `2f301311`: 36 added final maqafs and five
added final U+05C0 signs in stored pointed ketivs. The extract also displayed
already-present punctuation, for 42 maqaf and 12 paseq/legarmeh cases in total.
Its read-only comparison passed against the current dataset immediately before
retirement. The earlier qamats question was superseded by the final-mark ruby
correction recorded below the integration entry; it does not require this page.

**Retired scope:** Removed the HTML extract, its plain-text companion, its
dedicated generator, and its selection JSON. Removed the `--punctuation-review`
CLI branch and the differential check that existed solely for these outputs.
Updated current README and styling instructions, and marked the extract as
retired in the study's source note and the live release-notes draft. The draft's
commit-specific link still preserves the historical site list. Git history keeps
all four removed files; historical verification entries remain as dated evidence.
The actual frozen and reviewed pointing inputs, edition renderer, book datasets,
population metadata, note reviews and published HTML remain unchanged.

**Verification:** The extract's read-only check passed before removal. Black
passed on the changed entry point and test file. Both remaining near-Aleppo
differential tests passed, covering the census, dataset/population baselines and
source-note review inventory. The HTML read-only comparison passed for all 89
owned files and both font copies. The CLI help no longer offers the retired
command; a search found no extract dependencies in current Python or published
products. A complete changed-path audit and direct Git comparison confirm that
the production pointing inputs, datasets and published pages are unchanged.
`git diff --check` passed. Mega and full suite remain on the approved nightly
cadence; this retirement has focused checks and changes no production reading.

## Prominent qere-without-ketiv encoding — 2026-10-11

**Status:** Implemented by Codex after Ben explicitly requested implementation
of the document-only plan. Ben chose readable encoding summaries followed by
curly-brace notation, with dataset implementation left for separate work.

**Checkout and baseline:** Source, development and integration checkout is the
full clone `C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`17b79fd70c6e0173b192193b5d67868a2aa5298f` before editing. The planning baseline
`6e793c906e2275d0df51e0631849b0c38ba95b94` is its ancestor. The intervening link
presentation rollout and removal of the obsolete display-space paragraph are
preserved. Codex owns implementation, focused verification, commit and push.

**Change:** The study explains the two near-Aleppo-specific marks templates and
the artificial carrier convention. Each entry puts “Near-Aleppo encoding” before
its full verse. Current encodings are labelled implemented; intended encodings
are labelled pending or assessment open. The generator reads complete current
source fragments from the dataset through the existing closed Scripture walk,
excluding note bodies and copied MAM lemmas, validates both literal parameters
and the whole qere, and lets the HTML writer escape the notation as text.

The study's v2 metadata records four intended assessments: the template with
space above the marks at Judges 20:13 and 2 Kings 19:31, empty body text at
2 Samuel 16:23, and the template without space above the marks at 2 Samuel 18:20.
The five entries awaiting image readings keep their encoding assessments open.
The 2 Kings holam reading remains tentative; the 2 Samuel 18:20 use still awaits
its own variant and implementation. No pending payload is fabricated. All nine
current source fragments still use `קרי ולא כתיב`; neither marks template is
applied at these sites.

**Verification:** Black passed on the changed Python file. Real HTML generation
and its read-only comparison passed for all 89 owned files and both font copies.
An independent check read the dataset JSON and matched all nine displayed source
fragments, confirmed that encoding precedes every verse, and checked the pending
labels and RTL source isolation. After removing only the added encoding sections,
the original page body is byte-identical to the baseline. Existing manuscript
metadata is unchanged after removing the new intended-encoding field. Only the
study page changed among generated products; datasets, edition pages, crop bytes
and existing link presentation are unchanged. The generated HTML was read,
the read-only agent review found no material defect, and `git diff --check` passed.

**Verification limits:** Automated browser inspection retains the local-preview
restriction recorded in the study README; no browser pass is claimed. Mega and
full suite remain on the approved nightly cadence. Focused generation and the
complete source and artifact comparisons cover this document-only revision.

## 2 Kings 19:37 manuscript reading — 2026-10-11

**Status:** Recorded by Codex from Ben's supplied crop and direct observation:
“marks without letters (qamats, qamats, pashta) with space above.” Ben described
a large horizontal space, presumably left intentionally by the letter-scribe;
that intention remains an attributed hypothesis.

**Checkout and baseline:** Source, development and integration checkout is the
full clone `C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`ec505454b0677ad6dc231d6f87440099d56acbbe` before editing. Codex owns the update,
focused verification, commit and normal push.

**Change:** The maintained reading record now records the two qamats marks and
pashta of בָּנָיו֙, without letters and with space above. The existing intended
encoding assessment uses `marks-with-space`; implementation remains pending.
Codex inspected `Screenshot 2026-10-11 120243.png` and copied its unchanged bytes
to `in/near-aleppo/img/qere-without-ketiv/aleppo-2K19-37.png`. The HTML build
copies that crop for inline display. The source note records provenance and
the reading; four selected cases still await image readings.

**Verification:** HTML regeneration and read-only comparison passed for all
90 owned files and both font copies. An independent baseline differential
confirmed that all eight other case records and HTML sections are unchanged,
along with the target's Scripture, MAM qere, current source notation and links.
All five canonical/generated crop pairs have identical bytes; the new crop
also matches the supplied screenshot. The generated HTML diff was read.
The prose mark-order check passed (one test), and `git diff --check` passed.
Production datasets are unchanged. Mega and full suite remain on the approved
nightly cadence; focused generation, the artifact differential and the prose
check cover this observation and crop update.

## Jeremiah 31:37 manuscript reading — 2026-10-11

**Status:** Recorded by Codex from Ben's supplied body-text and marginal-note
crops. Ben read a rather generous horizontal space with no niqqud and a masorah
circle in the space. The marginal qere note is partly obscured by damage, so some
of its letters are inferred.

**Checkout and baseline:** Source, development and integration checkout is the
full clone `C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`a7d936b3db3514c5138a14b71275292926d7fb76` before editing. Codex owns the update,
focused verification, commit and normal push.

**Change:** The reading record preserves the body-text observation for בָּאִ֖ים
and the qualification about the damaged marginal qere note. Its intended body
encoding assessment is `empty-body`, pending implementation. Codex inspected
`Screenshot 2026-10-11 121352.png` and `Screenshot 2026-10-11 121420.png` and
copied their unchanged bytes to `aleppo-Je31-37.png` and
`aleppo-Je31-37-marginal-qere.png` under the study's canonical image directory.
The primary crop record now supports one explicitly named, optional
`marginal_qere_note` crop. Both shapes are validated, and both images receive
distinct captions and alt text. Three selected cases still await image readings.

**Verification:** Black passed on the changed generator. HTML regeneration and
read-only comparison passed for all 92 owned files and both font copies. An
independent baseline differential confirmed that all eight other case records
and HTML sections are unchanged, along with the target's Scripture, MAM qere
and notes, current source notation and links. All seven canonical/generated
crop pairs have identical bytes, and both new crops match the supplied
screenshots. The generated HTML diff was read. The prose mark-order and Python
accent-mark lints passed (three tests); `git diff --check` passed. Production
datasets are unchanged. Mega and full suite remain on the approved nightly
cadence; focused generation, the artifact differential and the lints cover
this observation and the paired crop display.

## Jeremiah 31:37 marginal-note damage and layout — 2026-10-11

**Status:** Clarified by Codex from Ben's further image reading. The damage looks
as if opaque tape had been laid parallel to the right margin, obscuring
approximately the first letter of each inferred word on its own line. Ben does
not know the cause. The tape comparison describes how the damage looks; it does
not propose a mechanism.

**Checkout and baseline:** Source, development and integration checkout is the
full clone `C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`cd4c7140ea8cb72f62987b062a14905274cf4ece` before editing. Codex owns the update,
focused verification, commit and normal push.

**Change:** The reading record now describes obscured letters and unknown cause.
Its `marginal_qere_note.inferred_lines` preserves Ben's four supplied words in
their exact order, including the third line as supplied. The study and source
note show the inferred vertical layout in an RTL block with one word per line.
The generator validates a nonempty list of nonempty, single-line strings.

**Verification:** Black passed on the changed generator. HTML regeneration and
read-only comparison passed for all 92 owned files and both font copies. An
independent baseline differential confirmed the exact inferred words, order and
RTL markup. All eight other cases, the target's body reading and both encoding
assessments, Scripture, MAM qere and notes, source notation, links and crop
markup are unchanged. All seven crop pairs retain identical bytes. The generated
HTML diff was read; the focused prose/Python mark lints passed (three tests),
and `git diff --check` passed. Mega and full suite remain on the approved nightly
cadence; focused generation, the artifact differential and the lints cover
this clarification and vertical-layout display.

## Jeremiah 50:29 manuscript reading — 2026-10-11

**Status:** Recorded by Codex from Ben's supplied crop and direct observation:
generous horizontal space without niqqud, containing a masorah circle, with the
preceding maqaf extending into the space.

**Checkout and baseline:** Source, development and integration checkout is the
full clone `C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`a78b684874d9448fc162f6cb3e0238022b5f27ad` before editing. Codex owns the update,
focused verification, commit and normal push.

**Change:** The reading record now records the space, absent qere letters and
niqqud, masorah circle, and maqaf extending into the space at לָהּ֙. Its intended
body encoding assessment is `empty-body`, pending implementation. Codex inspected
`Screenshot 2026-10-11 122253.png` and copied its unchanged bytes to
`in/near-aleppo/img/qere-without-ketiv/aleppo-Je50-29.png`; the HTML build copies
the crop for inline display. Ruth 3:5 and Ruth 3:17 still await image readings.

**Verification:** HTML regeneration and read-only comparison passed for all
93 owned files and both font copies. An independent baseline differential
confirmed that all eight other case records and HTML sections are unchanged,
along with the target's Scripture, MAM qere and notes, current source notation
and links. All eight canonical/generated crop pairs have identical bytes; the
new crop also matches the supplied screenshot. The generated HTML diff was
read. The prose mark-order lint passed (one test), and `git diff --check` passed.
Production datasets are unchanged. Mega and full suite remain on the approved
nightly cadence; focused generation, the artifact differential and the prose
lint cover this observation and crop update.

## Ruth 3:5 manuscript reading — 2026-10-11

**Status:** Recorded by Codex from Ben's supplied crop and direct observation:
generous horizontal space without niqqud, containing only a masorah circle.

**Checkout and baseline:** Source, development and integration checkout is the
full clone `C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`f2ae390cbeacc4a77dbb2411d14b2893cfc41070` before editing. Codex owns the update,
focused verification, commit and normal push.

**Change:** The reading record now records the generous space without qere
letters or niqqud at אֵלַ֖י and the masorah circle within the space. Its intended
body encoding assessment is `empty-body`, pending implementation. Codex inspected
`Screenshot 2026-10-11 122537.png` and copied its unchanged bytes to
`in/near-aleppo/img/qere-without-ketiv/aleppo-R3-5.png`; the HTML build copies
the crop for inline display. At that revision, Ruth 3:17 was the final selected
case awaiting an image reading.

**Verification:** HTML regeneration and read-only comparison passed for all
94 owned files and both font copies. An independent baseline differential
confirmed that all eight other case records and HTML sections are unchanged,
along with the target's Scripture, MAM qere and notes, current source notation
and links. All nine canonical/generated crop pairs have identical bytes; the
new crop also matches the supplied screenshot. The generated HTML diff was
read. The prose mark-order lint passed (one test), and `git diff --check` passed.
Production datasets are unchanged. Mega and full suite remain on the approved
nightly cadence; focused generation, the artifact differential and the prose
lint cover this observation and crop update.

## Ruth 3:17 manuscript reading — 2026-10-11

**Status:** Recorded by Codex from Ben's supplied crop and direct observation:
generous space at the end of a manuscript line without niqqud, containing only
a masorah circle. The possibility that the line ending accounts for the generous
space accidentally remains Ben's hypothesis. All nine selected cases now have
dated image readings and crops; dataset implementation remains pending.

**Checkout and baseline:** Source, development and integration checkout is the
full clone `C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`a5a0e976af55940f2aed9f2c68523a3dfdda935f` before editing. Codex owns the update,
focused verification, commit and normal push.

**Change:** The reading record now records the generous end-of-line space
without qere letters or niqqud at אֵלַ֔י and the masorah circle within the space.
The spacing hypothesis is separately attributed to Ben. Its intended body
encoding assessment is `empty-body`, pending implementation. Codex inspected
`Screenshot 2026-10-11 122806.png` and copied its unchanged bytes to
`in/near-aleppo/img/qere-without-ketiv/aleppo-R3-17.png`; the HTML build copies
the crop for inline display. The source note now covers all nine selected cases.

**Verification:** HTML regeneration and read-only comparison passed for all
95 owned files and both font copies. An independent baseline differential
confirmed that all eight other case records and HTML sections are unchanged,
along with the target's Scripture, MAM qere and notes, current source notation
and links. All ten canonical/generated crop pairs have identical bytes; the
new crop also matches the supplied screenshot. The generated HTML diff was
read. The prose mark-order lint passed (one test), and `git diff --check` passed.
Production datasets are unchanged. Mega and full suite remain on the approved
nightly cadence; focused generation, the artifact differential and the prose
lint cover this observation and crop update.

## Marginal-note words — 2026-10-11

**Status:** Corrected by Codex at Ben's request: “these are words, just call them
words!” These are words in a marginal note.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`2ec93ab625a180c200f2584b61400a6edd677f23` before editing. Codex owns the correction,
focused verification, commit and normal push.

**Change:** The study now says “one word per line” and “each inferred word”. The
generator, reading metadata, source note and maintained descriptions use the same
wording. The inferred Hebrew words, their order, and their qualifications are
unchanged.

**Verification:** Black passed on the changed generator. HTML regeneration and
read-only comparison passed for all 95 owned files and both font copies. An
exact baseline comparison confirmed only the requested English replacements in
the generator, metadata, source note and generated page. The generated diff was
read, and `git diff --check` passed. Mega and full suite remain on the approved
nightly cadence; regeneration and the exact wording comparison cover this
terminology correction.

## Tape comparison describes appearance — 2026-10-11

**Status:** Amplified by Codex at Ben's request. The cause of the damage remains
unknown. The tape comparison describes how the damage looks; it does not propose
a mechanism.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`1a76228b225d8ee5e4c4129db09030d6466387e4` before editing. Codex owns the update,
focused verification, commit and normal push.

**Change and verification:** Added the qualification to the reading metadata,
source note and generated study. HTML regeneration and read-only comparison
passed for all 95 owned files and both font copies. An exact baseline comparison
confirmed that only this qualification changed in the records and page. The
generated diff was read, and `git diff --check` passed. Mega and full suite remain
on the approved nightly cadence; regeneration and the exact comparison cover
this prose clarification.

## MAM note translations and comparisons — 2026-10-11

**Status:** Implemented by Codex at Ben's request for English translations of
MAM doc-notes and discrepancies between his descriptions and MAM's.

**Checkout and baseline:** Source, development and integration use the full
clone `C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`9a8b64fd600764bb702b69393de7551dcaae8ee5` before this work. Codex owns the
document revision, focused verification, commit and normal push.

**Change:** The maintained English-note input supplies six complete translations
and nine comparisons. The generator reconciles each translation with its whole
current MAM lemma and note parts, and each comparison with the observation and
documentation text it assesses. Hebrew examples remain in RTL blocks. Source
sigla and the Simanim Tanakh title were checked against the local mirrored MAM
introduction. A discrepancy summary appears near the top of the study.

**Discrepancy:** At 2 Samuel 16:23, MAM describes only a narrow space; Ben
describes a fairly generous space even after the maqaf, insufficient for letters
but ample for below-marks. Both descriptions say that pointing is absent. The
other attached notes agree where the descriptions overlap; additional surrounding
text, marginal-note quotations and spacing hypotheses are identified as additions.
Judges 20:13, 2 Kings 19:31 and 2 Kings 19:37 have no attached MAM note to compare.

## Supplemental encoding and body-text definition — 2026-10-11

**Status:** Corrected by Codex at Ben's request. Every existing `קרי ולא כתיב`
call and its qere are to be retained and supplemented by one body-text template.
The earlier presentation suggesting replacement, including “empty body text”,
is superseded. Dataset implementation remains deferred while the document evolves.

**Change:** Pending supplements distinguish niqqud with horizontal space,
niqqud without horizontal space above the marks, and horizontal space without
niqqud. Existing marks templates are candidates; supplemental names, parameter
shapes and call placement remain to be designed. The study now qualifies its
opening definition: qere letters are absent from the body text and written in a
marginal note. Shared masorah-circle presence is noted once at the top, while
complete MAM notes and translations retain their source references. Circle
positions remain in reading metadata; authored per-case repetitions are removed.

**Verification for both revisions:** Black passed on the changed generator.
HTML regeneration and read-only comparison passed for 95 files and both font
copies. An independent baseline differential verified all six translations,
nine comparisons, the one discrepancy and nine unchanged current source calls.
Scripture, Hebrew notes, manuscript readings, inferred marginal words, crops,
links and production datasets are preserved. A read-only reviewer found no
material translation or document defects. The three focused prose and mark
lints passed, the generated diff was read, and `git diff --check` passed.
Mega and full suite remain on the approved nightly cadence; focused regeneration,
source reconciliation, the artifact differential and lints cover these revisions.

## Body-text wording — 2026-10-11

**Status:** Implemented by Codex at Ben's request. The introductory sentence now
reads “The space and marks in the body text of the manuscript can nevertheless
differ.” This replaces the vague “at the manuscript site”.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`b711ceaaf73c865ff3c89ab61340c6fe8112c0d5` before editing. Codex owns the wording
change, focused verification, commit and normal push.

**Verification:** Black passed on the changed generator. HTML regeneration and
read-only comparison passed for all 95 files and both font copies. The generated
diff contains only the requested sentence replacement and paragraph wrapping.
`git diff --check` passed. Mega and full suite remain on the approved nightly
cadence; regeneration and the inspected diff cover this prose-only correction.

## Introductory list of case contents — 2026-10-11

**Status:** Implemented by Codex at Ben's request. “Have their own labels” meant
the HTML document's headings, but the phrase was vague. The introduction now
lists the current NAEE contents, any MAM notes, and the Aleppo images for each
case using Ben's proposed wording. The image-reading attribution remains.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`8f7aa4f0ff5084ee0337a4f50cc9d270ce23d9fb` before editing. Codex owns the revision,
focused verification, commit and normal push.

**Verification:** Black passed on the generator. HTML regeneration and read-only
comparison passed for all 95 files and both font copies. The generated diff was
read and contains only this introduction revision. `git diff --check` passed.
Mega and full suite remain on the approved nightly cadence; regeneration and
the inspected diff cover this prose-only revision.

## Horizontal space and line position — 2026-10-11

**Status:** Implemented by Codex at Ben's request. “Encoding conventions” now
defines “space above the marks” as horizontal space in the line of letters,
between words or at the end of a manuscript line. End-of-line space may have
been left on purpose or may be accidental. Judges 20:13 and Ruth 3:17 are the
two end-of-line cases; none of the cases in this study is at the start of a line.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`7253552845aa6a9687992b28d6a5f1210afe84fc` before editing. Codex owns the revision,
focused verification, commit and normal push.

**Verification:** Codex consulted the recorded observations and all nine
body-text crops for the line-position statement. Black passed on the generator.
HTML regeneration and read-only comparison passed for all 95 files and both
font copies. The generated diff was read and adds only the requested paragraph.
`git diff --check` passed. Mega and full suite remain on the approved nightly
cadence; image inspection, regeneration and the inspected diff cover this
prose-only clarification.

## Remove displayed recording and review dates — 2026-10-11

**Status:** Implemented by Codex at Ben's request. All nine “Aleppo manuscript
reading” headings now omit their recording dates. The two Samuel descriptions
also omit the date on which MAM's note was reviewed. No dates remain in the
rendered study; source provenance dates remain in the reading metadata.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`120ecb4abcac7fe6f1a3667e92547b1937f8484d` before editing. Codex owns the revision,
focused verification, commit and normal push.

**Verification:** Black passed on the generator. HTML regeneration and read-only
comparison passed for all 95 files and both font copies. The generated diff was
read and contains only the nine heading changes and two date removals in prose.
The date search found no remaining dates in the page. `git diff --check` passed.
Mega and full suite remain on the approved nightly cadence; regeneration and
the inspected diff cover this prose-only revision.

## Consolidated sentence-prose batch — 2026-10-11

**Status:** Implemented. Ben's chat messages are the request source; Codex records
the consolidated batch in this existing tracked ledger. Earlier document requests
are implemented in the entries above. This batch combines Ben's requests to:

1. Use sentences in place of “No dagesh.” and throughout the document's English
   prose: “Please let's use sentences here and throughout the document.”
2. Qualify the absence of dagesh with “as expected, since dagesh marks are never
   included in cases of qere without ketiv”, with the body-text scope explicit.

The prose pass revised English descriptions, list items, encoding summaries,
translation fragments and captions. Hebrew source quotations, qere readings,
template notation and structural headings retain their existing contents.
Codex uses this ledger to consolidate chat requests before implementation and
record each batch's implemented, deferred or unresolved dispositions at completion.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`648efbaf72485ab5a1b4b1965ef8e6625dd79de5` before editing. Codex owns the revision,
focused verification, commit and normal push.

**Verification:** Black passed on the generator. HTML regeneration and read-only
comparison passed for all 95 files and both font copies. The full generated diff
was read; Scripture, Hebrew sources, current source calls, readings, inferred
marginal words, links and crops are preserved. Dates remain hidden, and the
previous spacing, circle and damage qualifications remain intact. A read-only
reviewer found no material prose or translation defects. The three focused prose
and mark lints passed, and `git diff --check` passed. Mega and full suite remain
on the approved nightly cadence; focused regeneration, source reconciliation,
inspection, review and lints cover this consolidated prose batch.

## Center manuscript images — 2026-10-11

**Status:** Implemented. Ben requested “Center images.” All ten manuscript crops,
including the marginal-note crop, and their captions are centered in the
study through its shared CSS rules.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`212e9c0ccf5598aa868265ac599994c76dc97792` before editing. Codex owns the layout
change, focused verification, commit and normal push.

**Verification:** HTML regeneration and read-only comparison passed for all
95 files and both font copies. All ten image elements use the shared centering
rule. The generated diff was read and changes only the two CSS rules; the page
body and images are unchanged. `git diff --check` passed. Mega and full suite
remain on the approved nightly cadence; regeneration and stylesheet inspection
cover this layout-only change.

## Center short Hebrew displays — 2026-10-11

**Status:** Implemented. Ben requested centering short displayed Hebrew, specifically
the MAM qere and current source-notation values. This batch centers those values
and the Hebrew quotations in English translations. The inferred marginal-note
block is centered as a whole while preserving its RTL layout and one word per line.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`a1296f9faf50d49711965355d9c84a02eb093c33` before editing. Codex owns the layout
change, focused verification, commit and normal push.

**Verification:** Black passed on the generator. HTML regeneration and read-only
comparison passed for all 95 files and both font copies. The generated diff was
read and contains only centering rules and display-class assignments. The nine
qere values, nine source-notation values, four translated Hebrew quotations and
one inferred marginal-note block use the centering rules. Text, marks, RTL
attributes, word order, images and manuscript observations are preserved.
`git diff --check` passed. Mega and full suite remain on the approved nightly
cadence; regeneration and stylesheet/markup inspection cover this layout-only change.

## Color MAM note targets — 2026-10-11

**Status:** Implemented. Ben requested coloring the ink of the targets in “Current
MAM doc-note” entries, following MAM-with-doc and near-Aleppo. The target markup
is already present; the study now uses the matching blue/light-blue color rules
for note lemmas and target passages in the displayed verses.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`427e4e89ea13097a7b938f466e1131784556ee4c` before editing. Codex owns the styling
change, focused verification, commit and normal push.

**Verification:** The color matches `py/mb_misc/styles_mam_with_doc.css`, which
supplies MAM-with-doc and near-Aleppo's edition styling. All six attached note
lemmas use the target class. HTML regeneration and read-only comparison passed
for all 95 files and both font copies. The generated diff was read and adds
only the target-ink rule and its source comment; markup, text and images are
unchanged. `git diff --check` passed. Mega and full suite remain on the approved
nightly cadence; regeneration and the checked stylesheet precedent cover this
styling-only change.

## Contrast spacing with absent pointing — 2026-10-11

**Status:** Implemented. Ben requested “yet” in the 2 Samuel 16:23 description:
“The space is fairly generous even after the maqaf, yet there is no pointing
for אִ֖ישׁ.” The comparison's subject text is reconciled with that wording.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`72c9078cc35c92e561cf81ec46c0fb46f3b72104` before editing. Codex owns the wording
change, focused verification, commit and normal push.

**Verification:** HTML regeneration and read-only comparison passed for all
95 files and both font copies. The generated diff was read and changes only
“with no” to “yet there is no” in the requested sentence. `git diff --check`
passed. Mega and full suite remain on the approved nightly cadence; regeneration
and the inspected diff cover this prose-only correction.

## Anonymous voice and the meaning of narrow — 2026-10-11

**Status:** Implemented. Ben requested an unnamed authorial voice throughout the study
and a more substantive discussion of MAM's “narrow” at 2 Samuel 16:23. The possible
interpretation is narrow relative to the room required for letters, rather than
for points alone. Named-contributor references are removed from the rendered
prose, and the summary and comparison describe an apparent discrepancy with
this possible reconciliation. Source provenance remains in the maintained metadata.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`cdb7b0b9f8a4b175561b40266aeca04f486a016b` before editing. Codex owns the prose
revision, focused verification, commit and normal push.

**Verification:** Black passed on the generator. HTML regeneration and read-only
comparison passed for all 95 files and both font copies. The generated and input
diffs were read; MAM notes and translations, qere glyphs, inferred words, styles,
images and source provenance are preserved. The source-note assessment now records
the possible interpretation of “narrow”. The rendered page has no contributor-name
references or dates. A read-only reviewer found no material voice or interpretation
defects and confirmed the hypotheses and damage qualifications are preserved.
The three focused prose and mark lints passed, and `git diff --check` passed.
Mega and full suite remain on the approved nightly cadence; focused regeneration,
source reconciliation, inspection, review and lints cover this prose revision.

## Remove generic qere display explanation — 2026-10-11

**Status:** Implemented. Ben requested removal of the generic explanation that the
dataset retains the pointed qere and NAEE displays it above the editorial
“no ketiv” label. The shared generator included that explanation in all nine
case entries; there is no case-specific reason to retain it at 2 Samuel 18:20.
The current template identification and the intended supplemental encoding
remain intact.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`82a248cdbedfadafc0b07035e8c0286efa166327` before editing. Codex owns the removal,
focused regeneration, commit and normal push.

**Verification:** Black passed on the generator. HTML regeneration and read-only
comparison passed for all 95 files and both font copies. The generated diff was
read and removes only the generic explanation in all nine case entries.
`git diff --check` passed. Mega and full suite remain on the approved nightly
cadence; focused regeneration and the inspected diff cover this prose-only change.

## Explain agreement with an implied qere — 2026-10-11

**Status:** Implemented. Ben requested “the qere implied by the Leningrad Codex”
in place of “the Leningrad Codex's qere” and comparable clarification elsewhere.
The English versions translate and expand MAM's abbreviated notes. Their
statements of agreement must preserve the uncertainty about whether the agreement
concerns letters in the margin, niqqud in the body text, or both.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`ed4fb323756452bc6ef6321499a7acb94549e445` before editing. Codex owns the explanatory
prose, regeneration, focused verification, commit and normal push.

**Change:** Both Ruth translations now use the requested implied-qere wording.
Jeremiah 31:37 likewise attributes the reported agreement to the readings implied
by the manuscripts. The six English-section headings identify translation and
explanation, and one introductory paragraph records the unresolved scope of the
brief agreement statements. The maintained source note describes this treatment.

**Verification:** Black passed on the generator. HTML regeneration and read-only
comparison passed for all 95 files and both font copies. The source and generated
diffs were read; only the requested explanatory prose and headings change.
Original MAM notes, Hebrew text, comparisons, manuscript readings and encodings
are preserved. `git diff --check` passed. Mega and full suite remain on the
approved nightly cadence; focused regeneration, note-source reconciliation and
diff inspection cover this prose-only clarification.

## Describe absent pointing neutrally — 2026-10-11

**Status:** Implemented. Ben questioned “missing” in the Ruth translations and
suggested “not written” or “not present”. The Hebrew חסרים supports “missing”
or “absent”, but does not establish a cause for the absence. Use “not present”
in both Ruth notes and the comparable Jeremiah 31:37 translation of חסר.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`99d018732732930d74bb8a158002a1b304289cb9` before editing. Codex owns the wording,
regeneration, focused verification, commit and normal push.

**Verification:** HTML regeneration and read-only comparison passed for all
95 files and both font copies. The source and generated diffs were read and
change only these three English descriptions of absent pointing. Original Hebrew
notes and Scripture are preserved. `git diff --check` passed. Mega and full
suite remain on the approved nightly cadence; focused regeneration and diff
inspection cover this wording-only change.

## Use one name for the additional template — 2026-10-11

**Status:** Implemented. Ben requested consistent reference to the “additional
template”, rather than rotating between that phrase and “supplement”. Use
“additional template” throughout the study's introduction, encoding labels,
case explanations and maintained source note. Preserve the distinction between
the existing qere call and the proposed additional template.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`93a6727e5774334e4332db5d5cbb82396c16fe7b` before editing. Codex owns the consistent
wording, regeneration, focused verification, commit and normal push.

**Verification:** Black passed on the generator. HTML regeneration and read-only
comparison passed for all 95 files and both font copies. The source and generated
diffs were read. “Supplement” and “supplemental” no longer name the additional
template in the study or its maintained description; all references to the
renamed private generator constant were reconciled. Recorded readings, template
classifications, Hebrew text, notes and current dataset calls are preserved.
`git diff --check` passed. Mega and full suite remain on the approved nightly
cadence; focused regeneration, terminology searches and diff inspection cover
this wording change and matching private identifier rename.

## Qualify whether niqqud are present — 2026-10-11

**Status:** Implemented. Ben requested “if any” in the encoding-conventions sentence.
Use “The additional template records which niqqud, if any, are present” to
state explicitly that the body text may have no niqqud.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`18936e5b27461d28f9b1dd6c0e5b508a1856c094` before editing. Codex owns the wording,
regeneration, focused verification, commit and normal push.

**Verification:** Black passed on the generator. HTML regeneration and read-only
comparison passed for all 95 files and both font copies. The generated diff was
read and changes only the requested qualification and resulting line wrapping.
`git diff --check` passed. Mega and full suite remain on the approved nightly
cadence; focused regeneration and diff inspection cover this wording-only change.

## Name the existing niqqud templates — 2026-10-11

**Status:** Implemented. Ben requested “The existing niqqud templates” in place of
“The existing marks templates” to avoid the possible English-verb reading of
“marks”.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`a9513424352c44ea8bca662164f237f7aaf2658a` before editing. Codex owns the wording,
regeneration, focused verification, commit and normal push.

**Verification:** Black passed on the generator. HTML regeneration and read-only
comparison passed for all 95 files and both font copies. The generated diff was
read and changes only “marks” to “niqqud” in the requested phrase.
`git diff --check` passed. Mega and full suite remain on the approved nightly
cadence; focused regeneration and diff inspection cover this wording-only change.

## Describe the current carrier convention — 2026-10-11

**Status:** Implemented. Ben requested the current carrier choices instead of the
historical statement “The original convention uses alef carriers.” State that
the carrier can be alef, vav, or, rarely, dalet.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`bef8252784d2f667d62185dea711dc7ffac2cdf3` before editing. Codex owns the wording,
regeneration, focused verification, commit and normal push.

**Verification:** Black passed on the generator. HTML regeneration and read-only
comparison passed for all 95 files and both font copies. The current validator
recognizes alef, vav and dalet carriers. The generated diff was read and replaces
only the historical sentence with the current carrier choices.
`git diff --check` passed. Mega and full suite remain on the approved nightly
cadence; focused regeneration and diff inspection cover this wording-only change.

## Name the unsettled carrier payload — 2026-10-11

**Status:** Implemented. Ben requested the verse instead of “an unsettled case”.
Name 2 Kings 19:31 and explain that its tentative ḥolam male reading leaves
the carrier payload unsettled, as the maintained reading already records.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`02db015b258686eb94bea305e38083d9323fc03c` before editing. Codex owns the wording,
regeneration, focused verification, commit and normal push.

**Verification:** Black passed on the generator. HTML regeneration and read-only
comparison passed for all 95 files and both font copies. The generated diff was
read and names 2 Kings 19:31 and the tentative ḥolam male reading, with the
existing romanization styling. The maintained reading supports that explanation.
`git diff --check` passed. Mega and full suite remain on the approved nightly
cadence; focused regeneration and diff inspection cover this prose clarification.

## State that the existing qere calls will remain — 2026-10-11

**Status:** Implemented. Ben reaffirmed that every existing `קרי ולא כתיב` call
will remain. Replace “still uses” with “uses … and will continue to do so”
and remove the parenthetical English gloss in that sentence. The additional
template supplements the existing call.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`53e7aa829b0b213cff2e7a854c03cbf2c29b131d` before editing. Codex owns the wording,
regeneration, focused verification, commit and normal push.

**Verification:** Black passed on the generator. HTML regeneration and read-only
comparison passed for all 95 files and both font copies. The generated diff was
read and changes only the requested wording and resulting line wrapping; every
existing qere call and all pending additional-template assessments are preserved.
`git diff --check` passed. Mega and full suite remain on the approved nightly
cadence; focused regeneration and diff inspection cover this wording-only change.

## Summarize the cases in a compact table — 2026-10-11

**Status:** Implemented. Ben requested a table instead of the numbered verse list,
with narrow columns and defined abbreviations. At minimum the table must record
niqqud presence and horizontal-space presence, independently of whether niqqud
occupy or lie beneath that space. Use N and H with +/− values, and a position
column with BW for between written words and EOL for the end of a manuscript line.
Preserve the verse links to the full case discussions and the shared statement
about masorah circles. The table summarizes manuscript readings, not current
dataset encodings.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`a833ad895408061c30d4a40562175d80f2c6ec66` before editing. Codex owns implementation,
regeneration, focused verification, commit and normal push. A read-only reviewer
owns independent reconciliation of the nine readings and body-text crops.

**Verification:** Black passed on the generator. The initial render rejected the
unsupported caption element; the table now uses a supported section heading,
explicit table label and linked legend, with no shared HTML-writer changes.
HTML regeneration and read-only comparison passed for all 95 files and both font
copies. The source and generated diffs were read. The table's nine values and
positions agree with the image readings; an independent reviewer inspected all
nine body-text crops and found no mismatches or consequential implementation
defects. Codex also inspected the seven crops used for the newly explicit BW
positions. The existing verse links, Scripture, MAM notes, translations, images,
current dataset calls and tentative ḥolam male qualification are preserved.
The three focused prose and mark lints passed, and `git diff --check` passed.
Mega and full suite remain on the approved nightly cadence; focused regeneration,
image reconciliation, review and lints cover this study-table change.

## Show chanted-word context instead of whole verses — 2026-10-11

**Status:** Implemented. Ben requested one chanted word before the QVLK and one
after it, with two on the available side for a verse-final or verse-initial
QVLK, and ellipses for omitted text. Preserve the complete chanted word containing
the QVLK when the QVLK is in a maqaf compound, then retain the neighboring
chanted words. Rename the display heading to “Current NAEE excerpt” and center
these short Hebrew displays. Keep the qere, its box, marks and target ink intact.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`c020675419d3c31d83239d1926bbb66929568f96` before editing. Codex owns implementation,
regeneration, focused verification, commit and normal push. A read-only reviewer
independently checks the nine context selections and ellipsis placement.

**Verification:** Black passed on the generator. HTML regeneration and read-only
comparison passed for all 95 files and both font copies. The source and generated
diffs were read. All nine excerpts retain the independently checked neighboring
chanted words and intact maqaf compounds. Every excerpt has a leading ellipsis;
seven have a trailing ellipsis. The other two, 2 Kings 19:31 and Ruth 3:5, reach
the verse ending and retain sof pasuq. No current QVLK is verse-initial or
verse-final; the renderer's explicit endpoint branches retain two neighbors on
the available side. The independent final review found no material defects in
the selections, original-node preservation or endpoint logic. The headings,
centering and dataset README now describe excerpts. All MAM notes, translations,
table entries, qere glyphs, target ink, images and dataset calls are preserved.
The three focused prose and mark lints passed, and `git diff --check` passed.
Mega and full suite remain on the approved nightly cadence; focused regeneration,
independent context review, source inspection and lints cover this excerpt change.

## Keep only discrepancies and additional manuscript remarks — 2026-10-11

**Status:** Implemented. Ben requested that comparisons with MAM record only
discrepancies, excluding agreements and summaries of facts supplied by only one
description. Trim the displayed manuscript remarks to facts beyond MAM's note.
Keep the qualified interpretation of “narrow” at 2 Samuel 16:23 in those remarks,
without a separate discrepancy entry: the comparison depends on whether the
space is assessed relative to the letters or the niqqud.

**Checkout and baseline:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, clean on main at
`b6a38a3f37fbed2024236a2086631142af27204e` before editing. Codex owns the
source edits, regeneration, focused verification, commit and normal push.
A read-only reviewer checks the trimming against all six MAM notes.

**Execution scope:** Preserve full structured image readings, provenance, all
Hebrew notes and translations, images, summary-table values, NAEE excerpts and
dataset calls. Allow no separate remarks where everything duplicates MAM, and
no comparison block where no discrepancy remains. Update the maintained source
README. Run Black on the changed generator, the real HTML build and comparison,
the focused prose/mark lints and diff checks. Mega and full suite remain on the
approved nightly cadence.

**Verification:** Black passed on the generator. The real HTML build and
read-only comparison passed for all 95 files and both font copies. The generated
diff removes the discrepancy summary and all nine comparison blocks; the
qualified “narrow” discussion appears once in the additional remarks. Separate
remarks at 2 Samuel 18:20 and Ruth 3:5 are omitted because they duplicate MAM.
The other remarks retain only the additional details, and the three cases
without attached notes retain their full remarks. Nullable displayed remarks
and comparisons are explicit in the revised source formats and renderer.
An independent reviewer found no material defects in the trimming or renderer.
A differential comparison with the baseline confirmed that full structured
readings, all six Hebrew notes and English translations, nine excerpts and qere
displays, source notation, table, images and inferred marginal-note layout are
preserved. The three focused prose and mark lints passed. The source and rendered
diffs were read, and `git diff --check` passed. This revision supersedes the
earlier agreement comparisons and duplicated manuscript prose. Mega and full
suite remain on the approved nightly cadence; focused regeneration, preservation
comparison, independent review and lints cover this presentation change.

## Clarify the opening definition — 2026-10-11

**Status:** Implemented. Ben requested a less awkward opening and an unambiguous
relationship between the qere letters and the body text. Use: “In each case of
qere without ketiv, the body text contains no letters for the qere; those letters
are written in a marginal note.” Apply the same wording to the source README.

**Checkout and verification scope:** The full clone
`C:/Users/BenDe/GitRepos/MAM-basics` is clean on main at
`f5c43013038b14a85add49aaa040d838cf947c2d` before editing. Codex owns the wording,
regeneration, diff inspection, commit and normal push. Run Black on the changed
generator and the real HTML build/comparison. Mega and full suite remain on the
approved nightly cadence for this wording-only change.

**Verification:** Black passed. The real HTML build and read-only comparison
passed for all 95 files and both font copies. The source and generated diffs
were read; the rendered change is confined to the opening sentence and its
line wrapping. The source README uses the same definition. `git diff --check`
passed. Mega and full suite remain on the approved nightly cadence because
this edit changes only explanatory wording.

## Rework the opening around shared and varying features — 2026-10-11

**Status:** Implemented. Ben requested a full paragraph rewrite: first state the
features shared by every case, then name the features that vary. State that
each case discussed here has qere letters in a marginal note and a masorah
circle in the body text, where the qere letters are absent. Then state that
niqqud presence and horizontal-space presence differ from case to case. Fold
the later circle-presence paragraph into this opening so the common feature
is stated once. This supersedes the preceding opening-sentence revision.

**Checkout and verification scope:** The full clone
`C:/Users/BenDe/GitRepos/MAM-basics` is clean on main at
`a33521dd1f0aba6642b62ee86daff2d940a9faa5` before editing. Codex owns the prose,
source README, regeneration, diff inspection, commit and normal push. Run Black
on the changed generator and the real HTML build/comparison. Mega and full
suite remain on the approved nightly cadence for this prose-only revision.

**Verification:** Black passed. The real HTML build and read-only comparison
passed for all 95 files and both font copies. The source and generated diffs
were read: the opening paragraph is replaced, and the later circle paragraph
is removed. The source README now states the same common and varying features.
All case discussions, notes, images, table entries and dataset calls are
unchanged. `git diff --check` passed. Mega and full suite remain on the approved
nightly cadence because this change affects only introductory prose.

## Rewrite the per-case lead-in and bullets; continue in a new chat — 2026-10-11

**Status:** Implemented in the successor chat. Ben requested that the lead-in and
bullets describe each case's section, rather than the page as a whole. The
prior lead-in, “The verses below show:”, introduced three bullets beginning
“The page shows” or “The page includes”. Ben called both the lead-in and the
repeated bullet openings awkward. Ben suggested a lead-in along the lines of
“For each case of qere without ketiv, below we show the following”. The intended
list contents remain the current NAEE excerpt, any relevant MAM notes, and the
Aleppo Codex images. The revision uses natural complete sentences, without
“The page” as the subject of each bullet. Codex selected the precise wording
under the existing authorization; no additional decision from Ben was needed.

Ben also wrote: “Please record all queued request and start a new session.”
Codex recorded the queue here and transferred execution after committing and
pushing the handoff record. The rendered lead-in and bullets were unchanged
by the handoff commit.

**Queue reconciliation:** All earlier qere-study edit requests in this run
are implemented or superseded by later requests. The latest opening paragraph
at `a1661834d4a2186bef4a04640ddd251b23f08dc0` states the shared marginal note
and masorah circle first, then the varying niqqud and horizontal space.
The possible “narrow” discrepancy appears once within the additional manuscript
remarks; separate comparisons now contain only discrepancies and have no
entries. Manuscript remarks add only facts beyond MAM's notes. The confirmed
omission of נְאֻם־ in MAM's Jeremiah 31:37 illustration is an observation about
MAM's description, not a discrepancy with Ben's remarks; the original quoted
note and its translation remain unchanged. The historical A102 request remains
deferred under the earlier cutoff: its “The sparseness of the ketiv/qere” row
is still present in `py/near_aleppo/doc_registers.py` and
`gh-pages/near-aleppo/coverage-and-status.html`. Preserve that separate deferred
request; this handoff does not extend the qere-study task to A102.

**Deferred dataset decisions:** Every existing `קרי ולא כתיב` call will remain.
The planned additional template describes niqqud and horizontal space. Dataset
implementation is separate from this prose task. Names, syntax and call placement
remain to be designed; `רווח בלי ניקוד` was a chat suggestion, not an approved
design. The no-space variant for 2 Samuel 18:20 and the tentative ḥolam male
carrier payload for 2 Kings 19:31 remain open. The official dataset README
already links to the study. Do not implement dataset changes through this handoff.

**Verified source and intended development checkout:**
`C:/Users/BenDe/GitRepos/MAM-basics`, full clone on main, clean at
`a1661834d4a2186bef4a04640ddd251b23f08dc0` before this ledger-only commit.
The successor continues locally in this exact checkout from the pushed handoff
commit supplied in its opening prompt. Codex in the successor chat owns the
prose edit, focused verification, commit and normal push of main. This chat
stops writing after dispatch, so there is one writer. No worktree is requested.

**Files and retained requirements:** Edit
`py/near_aleppo/foi_qere_without_ketiv.py` and regenerate
`gh-pages/near-aleppo/foi/qere-without-ketiv.html`. Update this ledger in place;
Ben owns `doc/near-aleppo-requested-doc-edits.md`, which remains read-only.
The source README is `doc/near-aleppo-qere-without-ketiv/README.md`; the study
inputs are `in/near-aleppo/qere-without-ketiv-readings.json` and
`in/near-aleppo/qere-without-ketiv-mam-notes-en.json`. Preserve all nine cases,
six complete Hebrew MAM notes and English translations, centered images and
short Hebrew displays, colored note targets, inferred marginal-note layout,
summary-table values, excerpts, qere letters and marks, provenance and uncertainty.
Keep the unnamed authorial voice, consistent terminology, complete sentences
and absence of recording dates in the rendered study.

**Successor checks and completion:** Read `AGENTS.md`, `doc/review-trial.md`,
the Hebrew prose skill and its MAM-basics/rendered-prose references, and the
iterative document editing skill. Verify exact root, HEAD, branch and status
before edits and before staging. Use PowerShell 7 and this clone's interpreter
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe` from its root.
Run Black on the changed generator, then `py/main_near_aleppo.py --html` and
`py/main_near_aleppo.py --html --check`. Inspect all generated diffs and run
`git diff --check`. The expected product diff is only the study's lead-in and
three bullets. Mega and full suite remain on the approved nightly cadence for
this prose-only change. Commit finished work on main, fetch origin, merge if
needed under the full-clone rules, and push normally. Record check scope in the
commit message. Do not open a browser or launch an app preview; verify generated
content by reading it and give an absolute file link.

**Handoff verification:** The only edit in this chat is this ledger entry.
The source and pending passages were read, and the queue was reconciled with
the maintained ledger and request file. `git diff --check` is required before
commit. No generator, mega or suite run is owed by this record-only change.

**Successor implementation and verification:** The exact development and
integration checkout was verified as `C:/Users/BenDe/GitRepos/MAM-basics`,
clean on main at `4a0fd45c8bc671a91abb3fd4fa4ec640ee1dd551` before editing.
The lead-in now reads: “For each case of qere without ketiv, we present the
following in a separate section below:”. The three complete-sentence bullets
describe the current NAEE excerpt in context, relevant MAM notes with English
translations and explanations, and Aleppo Codex images of the case.
Black passed on the changed generator. The real HTML build and read-only
comparison passed for all 95 files and both font copies. The source and
generated diffs were read, and the generated introduction was read back.
The only product change is the lead-in and three bullets; the opening
paragraph and all case content remain unchanged. The request file and
deferred dataset and A102 work remain unchanged. `git diff --check` passed.
Mega and full suite remain on the approved nightly cadence because this
revision changes only introductory prose.

## Correct masorah-circle presence at 2 Kings 19:31 — 2026-10-11

**Status:** Implemented; Ben approved the push on 2026-10-11. Ben corrected the image reading: “No masorah circle is
present in 2 Kings 19:31.” Replace the universal circle-presence statement with
“A masorah circle is present in every case except 2 Kings 19:31.” Record the
absence and its provenance in the 2 Kings 19:31 source reading. The presence of
niqqud and horizontal space and the tentative ḥolam male reading are unchanged.
The opening paragraph and source README must state the exception consistently.

**Checkout and one-writer resumption:** The successor chat finished its lead-in
and bullet edit and is idle. Its local commit is
`1f4f5b2e3850d86a658a8b999b47b30e5b307789`; the full clone
`C:/Users/BenDe/GitRepos/MAM-basics` is clean on main at that commit before
this correction. Codex in this chat resumes as sole writer for Ben's new
correction. The supplied `aleppo-2K19-31.png` crop was consulted. Ben's earlier
objection to “Image readings are attributed to Ben Denckla.” needs no edit:
the current source and rendered study already omit that sentence and contributor
names. The unnamed rendered voice remains in force; provenance remains in source
records.

**Earlier push rejection:** The successor's push of `1f4f5b2e` to `origin/main` was rejected
by automatic approval review because main can publish the site and the handoff
was not accepted as authorization for that push. At the start of this correction,
origin/main was at `4a0fd45c8bc671a91abb3fd4fa4ec640ee1dd551`. The correction
was completed and verified locally before asking Ben to approve pushing both
local commits. The rejected push was not retried before approval. The changed product is the
published study page; the change can be revised through a later commit, while
the push is an outward-facing publication step.

**Verification scope:** Use this clone's environment for Black on the changed
generator, the real HTML build/comparison and focused prose/mark lints. Read all
source and generated diffs and run `git diff --check`. The expected product diff
against `1f4f5b2e` is only the opening paragraph. Preserve the successor's lead-in
and bullets, all cases, notes, translations, excerpts, table and crops. Mega and
full suite remain on the approved nightly cadence.

**Verification:** Black passed. The real HTML build and read-only comparison
passed for all 95 files and both font copies. The three focused prose and
Hebrew-mark lints passed. The source and generated diffs were read: the only
product change against the successor's commit is the opening paragraph.
The input change explicitly records absent circle presence and Ben's correction
as its basis; no other reading data or encoding assessment changed. The source
README states the exception in its opening and reading record. The successor's
lead-in and bullets and all notes, translations, excerpts, table values and crops
are preserved. `git diff --check` passed. Mega and full suite remain on the
approved nightly cadence for this study-specific correction.

**Standalone push handoff (approval granted):** Codex prepared this instruction on
2026-10-11. Ben's authorized content change was: “No masorah circle is present
in 2 Kings 19:31.” The remaining instruction is Codex's reconstruction of the
pending publication step. After Ben explicitly approves the push, continue in
the source, development and integration checkout
`C:/Users/BenDe/GitRepos/MAM-basics`, using its own environment. Verify clean
main and that required baseline `1f4f5b2e3850d86a658a8b999b47b30e5b307789`
is an ancestor of HEAD and the final local commit is “Correct the masorah-circle
exception in the qere study”. The executor owns final integration and push.
Fetch origin; if origin/main moved, merge normally in this full clone and repeat
the checks owed by the resulting changes. The ledger records the completed
focused checks and the nightly broad-check exception. Push main normally,
including both the successor's lead-in rewrite and this correction; never
force-push or rewrite history. Verify HEAD against origin/main and clean status,
then report the pushed commit. Until Ben approves, retain both local commits
and do not repeat the rejected push.

**Approval and readiness, 2026-10-11:** Ben wrote: “Yes, push the circle
correction and the lead-in rewrite to origin/main.” The approval condition in
the preceding handoff is fulfilled. The exact full clone was verified clean
on main at `e2864dfcb873d808310db7aa680a061657309d35`. A fresh fetch confirmed
origin/main remains at `4a0fd45c8bc671a91abb3fd4fa4ec640ee1dd551` and is an
ancestor of HEAD, so no merge or new product checks are required. This approval
record changes only the maintained ledger; the prior focused verification
remains applicable. Record-only diff checks are owed before the normal push.

## Define absent letters and list the varying body-text features — 2026-10-11

**Status:** Implemented. Ben supplied replacement opening prose using קרי ולא כתיב,
stating that neither qere nor ketiv letters are present in the body text, and
retaining the masorah-circle exception at 2 Kings 19:31. The opening now introduces
two varying features as bullets: whether "orphan" (letterless) niqqud are present
and whether horizontal space is present. The revision uses Ben's supplied wording
and the sentence-completing bullets. This supersedes the preceding opening prose;
the per-case lead-in and contents list remain unchanged.

**Checkout and execution scope:** Source, development and integration use the
full clone `C:/Users/BenDe/GitRepos/MAM-basics`, verified clean on main at
`f73c7f799daab18f8f0ae980166ee476a1250da7` before editing; origin/main matches.
Codex owns the generator edit, matching source README, HTML regeneration,
focused verification, commit and normal push. Edit
`py/near_aleppo/foi_qere_without_ketiv.py`,
`doc/near-aleppo-qere-without-ketiv/README.md`, this ledger and the generated
`gh-pages/near-aleppo/foi/qere-without-ketiv.html`. Preserve all case content,
notes, translations, readings, excerpts, table values, images and dataset calls.
The request file remains read-only; dataset implementation and A102 remain deferred.

**Verification scope:** Use this clone's interpreter from the repository root
for Black on the changed generator, `py/main_near_aleppo.py --html` and
`py/main_near_aleppo.py --html --check`. Read every generated diff and the
generated opening; the expected product change is only the opening paragraph
and its new two-item feature list. Run `git diff --check`. Mega and full suite
remain on the approved nightly cadence for this introductory-prose change.

**Verification:** Black passed on the changed generator. The real HTML build
and read-only comparison passed for all 95 files and both font copies. The
source and generated diffs were read, and the generated opening was read back:
Ben's supplied wording and two bullets appear, with the Hebrew phrase isolated
for direction. The only product change is the opening paragraph and feature
list. The matching source README and this ledger are updated; all case content
and deferred work remain unchanged. `git diff --check` passed. Mega and full
suite remain on the approved nightly cadence for this prose-only change.

## Simplify the per-case contents list — 2026-10-11

**Status:** Implemented. Ben supplied the lead-in “For each case of קרי ולא כתיב,
we show the following:” and three replacement bullets about the NAEE display,
MAM notes and Aleppo images. The revision uses that wording exactly, with the
Hebrew phrase isolated for direction. This supersedes the earlier per-case wording.

**Checkout and scope:** Source, development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, verified clean on main at
`5fbc7b48d413600f31aab1ac1bef5d8b1dbab6b5` before editing. Codex owns the
generator edit, regeneration, focused verification, commit and normal push.
Only `py/near_aleppo/foi_qere_without_ketiv.py`,
`gh-pages/near-aleppo/foi/qere-without-ketiv.html` and this ledger change.
Preserve the opening, all case content and deferred work.
Ben's request file remains read-only. Run Black, the real HTML build and
read-only comparison, inspect the generated diff and content, and run
`git diff --check`. Mega and full suite remain on the approved nightly cadence
for this introductory-prose change.

**Verification:** Black passed. The real HTML build and read-only comparison
passed for all 95 files and both font copies. The source and generated diffs
were read, and the generated lead-in and bullets were read back. The only
product change is the requested lead-in and three bullets; all other study
content remains unchanged. `git diff --check` passed. Mega and full suite
remain on the approved nightly cadence for this prose-only revision.

## Explain agreement wording in MAM note translations — 2026-10-11

**Status:** Implemented. Ben supplied a replacement translation paragraph explaining
the presentation of Hebrew notes and English translations, expanded abbreviated
wording, and the ambiguity of the example note "=ל-קרי". The paragraph quotes
the current “agrees” translation and describes “is consistent with” as more
conservative, relating the implied qere to body niqqud, if any, and marginal
qere letters. The revision uses the supplied wording, adds the missing opening
quotation mark before the final suggested translation, and isolates the Hebrew
note for direction. This supersedes the previous introductory translation paragraph;
the case translations themselves remain unchanged.

**Checkout and scope:** Source, development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, verified clean on main at
`d55532b2d18404e7599aa490236a083517d9ada0` before editing. Codex owns the
generator edit, regeneration, focused verification, commit and normal push.
Only `py/near_aleppo/foi_qere_without_ketiv.py`,
`gh-pages/near-aleppo/foi/qere-without-ketiv.html` and this ledger change.
All other study content and deferred work remain unchanged; Ben's request file
remains read-only. Run Black, the real HTML build and read-only comparison,
inspect the generated paragraph and all diffs, and run `git diff --check`.
Mega and full suite remain on the approved nightly cadence for this prose change.

**Verification:** Black passed. The real HTML build and read-only comparison
passed for all 95 files and both font copies. The source and generated diffs
were read, and the generated paragraph was read back. The only product change
is the requested introductory paragraph, with the quotation mark correction
described above; all case translations and other study content are unchanged.
`git diff --check` passed. Mega and full suite remain on the approved nightly
cadence for this prose-only revision.

## Name the existing qere template explicitly — 2026-10-11

**Status:** Implemented. Ben requested “every site below uses the קרי ולא כתיב
template and will continue to do so”. The generator and study now use that
wording. All other study content and deferred work remain unchanged.

**Checkout and verification:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, verified clean on main at
`54bc4297756f072d080341f24b13caf76958ff76` before editing. Black passed on the
generator. The real HTML build and read-only comparison passed for all 95 files
and both font copies. The source and generated diffs and generated sentence
were read; the only product change is the requested wording and line wrapping.
`git diff --check` passed. Mega and full suite remain on the approved nightly
cadence for this wording-only change. Codex owns commit and normal push.

## Name the summary-table columns in the legend — 2026-10-11

**Status:** Implemented. Ben requested the explicit subjects “The "N" column”,
“The "H" column” and “The "Pos." column” before “records” in the summary
legend. The generator and study now use that wording. Definitions, table values
and all other study content remain unchanged.

**Checkout and verification:** Development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, verified clean on main at
`16f8bb323c0fb419ffb87a23b40fe90e5f3cdf88` before editing. Black passed on the
generator. The real HTML build and read-only comparison passed for all 95 files
and both font copies. The source and generated diffs and generated legend were
read; the only product change is the requested wording and line wrapping.
`git diff --check` passed. Mega and full suite remain on the approved nightly
cadence for this wording-only change. Codex owns commit and normal push.

## List and count all three varying body-text features — 2026-10-11

**Status:** Implemented. Ben supplied a three-item replacement feature list:
niqqud are present in four of nine cases; horizontal space is absent only at
2 Samuel 18:20; a masorah circle is absent only at 2 Kings 19:31. The revision
moves the circle exception from the opening paragraph into this list and follows
the list with Ben's parenthetical definition of present niqqud as “orphan”, or
letterless, niqqud. It uses the supplied wording and numerals. This supersedes
the two-item feature list.

**Checkout and scope:** Source, development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, verified clean on main at
`df31de3702c21e6cc53cd0abbc23bc89370fb91d` before editing. Codex owns the
generator edit, matching source README, regeneration, verification, commit
and normal push. All case records, translations, excerpts, summary table values,
crops and deferred work remain unchanged; Ben's request file remains read-only.

**Verification:** Black passed on the generator. The real HTML build and
read-only comparison passed for all 95 files and both font copies. The source
and generated diffs were read, and the regenerated introduction and table were
read back. The table confirms four niqqud-present rows among nine and only
2 Samuel 18:20 without horizontal space. The source reading records the circle
absence at 2 Kings 19:31. The only product change is the requested opening
feature passage and parenthetical explanation. The source README matches.
`git diff --check` passed. Mega and full suite remain on the approved nightly
cadence for this prose-only change.

## Remove repeated source notation and standalone qere brackets — 2026-10-11

**Status:** Implemented. Ben authorized removing every “Current source notation”
subsection if the notation adds nothing beyond the MAM qere display, and requested
removal of square brackets from those displays. The nine current calls each have
the bracketed qere as their first parameter and the same qere as their second
parameter; the introduction already identifies the template. Codex agrees that
these source blocks add no independent case information. The revision removes
the blocks and their unused display plumbing and styles, while retaining source
validation. Each standalone MAM qere appears without brackets; quoted MAM notes
retain their original text and brackets. The source README and stale notation
wording are updated.
This supersedes the earlier source-notation presentation requirement.

**Checkout and scope:** Source, development and integration use the full clone
`C:/Users/BenDe/GitRepos/MAM-basics`, verified clean on main at
`4c81f0d7ddd283627f2694b26aaf97ab417299a0` before editing. Codex owns the generator,
study CSS, matching source README, regeneration, verification, commit and normal
push. All qere letters and marks, current and pending encoding summaries,
excerpts, notes, translations, readings, table values, crops and deferred work
are preserved. Ben's request file remains read-only. Run Black, the real HTML
build and read-only comparison, compare the page with the baseline after only
the authorized presentation changes, inspect all diffs and run `git diff --check`.
Mega and full suite remain on the approved nightly cadence for this presentation change.

**Verification:** Black passed on the generator. The real HTML build and
read-only comparison passed for all 95 files and both font copies. A differential
comparison with the baseline, normalizing HTML line wrapping, confirmed all nine
source blocks duplicate their MAM qere and all nine standalone displays lose only
their brackets. Every other page element and its content are preserved, apart
from the unused source styles and the guide's stale notation wording. This
includes all qere letters and marks, quoted MAM notes and their brackets, English
translations, encoding summaries, excerpts, table values and images. The source
validation still checks one correctly shaped source call per case and agreement
of its whole qere with MAM. All source and generated diffs and the regenerated
displays were read. `git diff --check` passed. Mega and full suite remain on the
approved nightly cadence for this presentation change.
