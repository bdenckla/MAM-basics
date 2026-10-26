# Plan: rewrite the MAM-for-Sefaria encoding page to document what MAM-for-Sefaria contains

State: executed 2026-10-26; see "Execution record" at the end.
Updates and later status: [PLAN-rewrite-MAM-for-Sefaria-encoding-page-update.md](PLAN-rewrite-MAM-for-Sefaria-encoding-page-update.md).

Ben approved this plan on 2026-10-26 through plan-mode approval, without revising it. This is
its tracked copy: the plan as approved, less its private evidence and its private follow-ups,
which belong to a private repository.

## Context

Written by Claude (Opus 5.5) on 2026-10-24, in a plan-mode session.

MAM-basics' hand-authored page `gh-pages/MAM-for-Sefaria/index.html` ("The encoding of MAM for
Sefaria") documented MAM-for-Sefaria only as differences from Sefaria's former Tanakh (old
Sefaria). In the QUPO table of its "Robust Unicode" section (searchable passage: "Below is a
table showing the two unique"), old Sefaria's Exodus 20:4 atom מתחת has PATAH, QAMATS, DAGESH,
ETNAHTA, GERESH on its tav, with no CGJ, while MAM's atom beside it has QAMATS, DAGESH, ETNAHTA,
GERESH, CGJ, PATAH. The page's `styles.css` sets `*[lang="hbo"] { font-family: "Taamey D"; }`
and neither it nor `gh-pages/document.css` has an `@font-face`, so each reader sees whatever
Taamey D is installed, or a fallback font, and how old Sefaria's atom looks depends on which
font that is.

Ben's decision, 2026-10-24, verbatim: "The entire documentation needs to be rewritten from fresh
perspective of just documenting what MAM for Sefaria contains rather than documenting MAM for
Sefaria as it differs from "old Sefaria" (tanach.us for sefaria). When this rewrite is done, this
problem should go away."

The page is also stale apart from that atom. Its figures are those of Sefaria's 2021 copy of
MAM, saved at MAM-basics `in/mam-from-Sefaria-2021-11-23/`, not of the files MAM-basics now
writes. Counted read-only on 2026-10-24 across the 39 files of each:

| Markup | Page says | 2021 copy | `MAM-for-Sefaria/csv/` today |
| --- | --- | --- | --- |
| `mam-implicit-maqaf` spans | 63 | 63 | 116 |
| `mam-kq-trivial` spans | 116 | 116 | 149 |
| notes, `<sup>*</sup>` with `<i class="footnote">` | 29 | 29 | 0 |
| `k-velo-q-maq` spans | not mentioned | 0 | 2 |

The page's Version Source, an English Wikisource URL, is also the 2021 copy's; today's files have
the Hebrew Wikisource page. And it never mentions three of the five header rows, the run of eight
no-break spaces that the handlers write for each shirah space (`_shirah_space` in
`py/mb_sefaria/mam4sef_handlers.py`), the `csv-ajf/` variant or the Unicode-name listings.

Intended outcome: a page that describes MAM-for-Sefaria's files and their encoding directly, as
they are now, with no old Sefaria text, and so no Hebrew whose appearance depends on which
Taamey D a reader has.

## Checkouts, baselines and ownership

- **Source and development checkout:** a full MAM-basics clone in a Claude-owned forest that no
  other session is writing in. Every command runs from that clone's root with its own
  interpreter, `./.venv/Scripts/python.exe`.
- **Baseline:** MAM-basics `27f263cb` or a descendant (`git merge-base --is-ancestor 27f263cb
  HEAD`). Before editing, record `git rev-parse --show-toplevel`, `git rev-parse HEAD`, the branch
  and `git status --porcelain`; the clone must be clean on `main`.
- **Skills:** `hebrew-prose` (with the references listed under "Writing rules"),
  `iterative-document-editing`.
- **Executor and integrator:** a fresh session started from this plan (decision 3). The executor
  owns integration into MAM-basics `main` and the push. Starting `.github/workflows/pages.yml`
  publishes the site and needs Ben's separate go-ahead.

## Public-safety rule

MAM-basics is public. Ben's rule of 2026-08-27, in MAM-basics' `in/repo_maintenance_policy.json`
("repo_visibility"), lets a public file name a private repository but not carry paths inside
them, file names of theirs, and findings about them. So nothing about a private repository's
commits, builds or measurements goes into the page, the generator, a commit message or this
tracked copy.

## Decisions

**Made.** Ben, 2026-10-24: rewrite the whole page to document what MAM-for-Sefaria contains, with
no comparison to old Sefaria (verbatim under "Context"). This plan takes the content consequences
in "What the new page documents" as following from that decision.

**Approved with the plan, 2026-10-26.** Each was put to Ben with its alternatives; he approved the
plan as written for the recommended choice.

1. **How the page is produced: (a), a generator.** `hebrew-prose` rules that pointed Hebrew is
   never retyped but lifted from data with an exactly-one-match assertion (`core-rules.md`, "Never
   retype an accent"), and that every count is read from the artifact that wrote it
   (`verifying.md`). A generator writes the page from the tracked CSV files: every example comes
   from a lookup that must match exactly once, every count is computed, and the list of tags and
   classes comes from parsing every file with closed dispatch, so the page cannot omit one. The
   page is regenerated whenever the CSV files change. The alternative, (b), hand-authoring the
   page with examples copied once by script, would leave every example and count a claim no check
   defends.
2. **Which Taamey D the page uses: (a), MAM-basics' copy.** Add
   `gh-pages/MAM-for-Sefaria/woff2/Taamey_D.woff2`, byte-identical to the copies the other product
   pages serve (all 16 copies had SHA-256 `5CC8DF8A…2C474` on 2026-10-24), and an `@font-face`
   rule in `styles.css`. In `DATA-LICENSES.md`, the `gh-pages/MAM-for-Sefaria/` row gains "except
   `woff2/Taamey_D.woff2`", and the font row's "sixteen tracked, byte-identical copies" becomes
   seventeen, re-verified. Drop the page's list of fonts "expected to be available on the
   system". Every reader then sees the same font with nothing installed, and the page moves with
   MAM-basics when it adopts a new Taamey D release. The alternative, (b), keeping the installed
   font, would leave a reader without Taamey D seeing a fallback font.
3. **Who executes and integrates:** a fresh session started from this plan, in a Claude-owned
   MAM-basics full clone that no other session is writing in.

## What the new page documents

One section per feature of the files, each saying what MAM-for-Sefaria has, with an example
lifted from the CSV files and its count. Following Ben's decision, there is no old Sefaria, UXLC or
WLC row, comparison or history. The outline, in the current page's order where that still fits:

1. **Introduction.** What MAM is; that MAM-for-Sefaria is the extract that Sefaria imports and
   shows as its default Tanakh; where the files are (MAM-basics' `MAM-for-Sefaria/` directory) and
   how current they are, by a link to its `README.md` rather than a restatement; the page's
   typographic conventions (hover text, the attention color, Unicode names in small capitals).
2. **The files.** All four folders of 39 files each:
   - `csv/`: Sefaria's versification; five header rows (Index Title, Version Title, Language,
     Version Source, and Version Notes, which has HTML of its own) and then one row per verse,
     reference then verse HTML.
   - `csv-ajf/`: the AJF variant. BHS versification, no header, and four columns: reference, the
     combined text, then alef and bet, which are empty except in the dual-cantillation verses. Its
     text is plain, with its own spellings of samekh, pe, legarmeh and paseq, and ketiv always
     first. Never expand "AJF": Ben removed a guessed expansion in `c0d12c94` (2026-03-09). If the
     page should say what it stands for or who uses it, Ben supplies the words.
   - `misc/unicode-names/` and `misc/unicode-names-ajf/`: the code-point-name listings, and their
     line format.
   - The verse numbering, including Joshua 21:36–37, which hold only an em dash because Sefaria's
     numbering has those verses and MAM has no text for them.
3. **Markup.** The closed set the handlers of `py/mb_sefaria/mam4sef_handlers.py` emit, confirmed
   by the generator's dispatch over the files:
   - the elements `span`, `b`, `small`, `big`, `sup` and `br`;
   - the classes `mam-spi-samekh`, `mam-spi-pe`, `mam-spi-invnun`, `mam-implicit-maqaf`,
     `mam-kq`, `mam-kq-k`, `mam-kq-q`, `mam-kq-trivial` and `k-velo-q-maq`;
   - legarmeh as THIN SPACE, then PASEQ in `<b>`; paseq as THIN SPACE, then PASEQ in `<small>`,
     then THIN SPACE;
   - the runs of one or eight no-break spaces, and the entities `&nbsp;` and `&thinsp;`, which the
     files use in place of the raw characters;
   - the ketiv and qere types and their order, ketiv velo qere and qere velo ketiv, and trivial
     pairs.
4. **Characters.**
   - The code points whose mark depends on context, as MAM-for-Sefaria uses them: ZARQA, ZINOR,
     PASEQ, YERAH BEN YOMO, ATNAH HAFUKH, GERESH, and GERESH MUQDAM, whose verses the generator
     classifies as prose or poetic.
   - QAMATS QATAN, HOLAM HASER FOR VAV, RAFE, UPPER DOT and LOWER DOT.
   - Geresh or gershayim with telisha gedolah; the zarqa's stress helper; the postpositive zarqa
     on an atom's last letter.
   - Meteg after silluq: the existing table, see "Tests the page must keep passing".
   - Mark order: MAM's, never Unicode-normalized, as `py/mb_cmn/uni_denorm.py` defines it.
5. **What the files leave out**, as the handlers decide it: MAM's notes; the good-ending markers;
   and, in `csv/`, the separate dual-cantillation strands.
6. **Robust Unicode.** Where MAM-for-Sefaria has a CGJ (the words for Jerusalem by type, the
   Decalogue QUPO and UM atoms, and any other place the data shows) and what it keeps in place.
   Explain each kind by listing its code points by name in order, with MAM-for-Sefaria's atom
   rendered beside them. **Never render a form without its CGJ**: that is the kind of string old
   Sefaria's Exodus 20:4 atom is, and the page would bring back the problem the rewrite removes.

Dropped as outside "what MAM for Sefaria contains", unless Ben says otherwise:
- the qamats qatan tables in Taamey Frank CLM, SBL Hebrew and Ezra SIL, and the remark that a
  ḥataf qamats glyph should match QAMATS QATAN;
- the Michigan-Claremont `82L` history and the recommendation to Groves;
- the UXLC proposals and reports;
- the section on notes, since the files have none;
- the PDF and `features-of-interest.pdf` references. No PDF of the page is built in MAM-basics,
  and MAM's features-of-interest pages, at `gh-pages/MAM-with-doc/foi/`, survey MAM-parsed rather
  than these files.

## How the page is produced (decision 1(a))

Facts from 2026-10-24, at MAM-basics `27f263cb`:
- Nothing in MAM-basics reads the MAM-for-Sefaria CSV files back in. The only writer is
  `py/mb_sefaria/write_utils_sef_or_ajf.py`, which `py/main_mam4sef.py` runs by hand.
- The CSV files lag MAM-simple: the last commit to them is `accced5d` (2026-10-12), and
  MAM-simple's JSON last changed in `80c1b4ec` (2026-10-20). So the page must read the CSV files
  themselves, never MAM-simple, or it would document text the product does not ship.
- Changing `py/main_mam4sef.py` would oblige rerunning it and inspecting every CSV it writes
  (`AGENTS.md`, "What this repository's products are, and which check a change owes"). The page
  generator therefore lives outside it and writes nothing under `MAM-for-Sefaria/`.

The design:
1. **Entry point.** A new subcommand of `py/main_authored.py`, writing only
   `gh-pages/MAM-for-Sefaria/index.html` and its `woff2/` copy. Add it to the subcommand list in
   that docstring.
2. **Module.** A new module beside the other authored pages, using `py/mb_author/author.py`
   (`help_gen_html_file`, `hbo`, the `$` substitutions) and `py/mb_misc/mb_html.py`. Mind
   `author.py`'s stem rule: an output named `index` needs a module stem that ends in "index" and
   is not "index". The generated banner comes from `py/mb_cmn/provenance.py`'s
   `generated_html_comment`, replacing the "Hand-authored static page" comment. Keep the current
   head's viewport meta, which `mb_html.html_el2` does not emit by itself; if keeping it needs a
   writer change, make the smallest one.
3. **Reading.** List the files with `git ls-files -z`, read them with the `csv` module (they are
   CRLF), and check their shape: a `csv/` file has five key/value header rows
   (`py/mb_sefaria/sef_header.py`) and then rows of reference and verse HTML; a `csv-ajf/` file has
   no header and three text columns after the reference; a listing follows the line format of
   `py/mb_misc/write_utils.py`.
4. **Closed dispatch.** Parse every cell's HTML and dispatch on every recognized element and class;
   raise on anything else. That table is the page's list of markup, so the list is complete by
   construction. Do the same for the string-level features the page names (CGJ kinds, PASEQ
   contexts, the em-dash verses).
5. **Examples and counts.** Lift each example with a lookup that must find exactly one match,
   collected in a list, never a set, following `_find_span()` in
   `py/accgram/maqaf_nonfinal_accents_page.py` and `_source_focus_word()` in
   `py/author_site/post_stress_meteg_post_silluq_data.py`. Compute every count. Pin each sentence
   whose truth depends on the data, in the manner of `maqaf_nonfinal_accents_page.pin_claims`,
   raising rather than warning.
6. **Two-vowel guard.** Raise if any rendered Hebrew has two vowels on one letter, except in the CGJ
   kinds the page names and the dispatch recognizes.
7. **Mega.** Add a `StepRecord` to `_STEPS` in `py/main_0_mega.py`, and update
   `py/product_scopes.py` as `py/tests/test_product_scopes.py` and `py/tests/test_mega_coverage.py`
   require. The step reads only tracked files, so the page then follows any later rerun of
   `py/main_mam4sef.py`.
8. **Font (decision 2(a)).** Copy the font with `py/mb_misc/report_stylesheet.py`'s
   `copy_report_font`, which copies `doc/woff2/` into a page's `woff2/`, and declare it in the
   hand-authored `styles.css` under the family name "Taamey D WOFF2", as the other product sheets
   do, so that a locally installed Taamey D cannot take its place. Also style whatever element the
   `$MAM`-style abbreviations emit (`<abbr class="small-caps">`), which the old sheet does not.
9. **Revision line.** Keep "Author: Ben Denckla" and a "Revision:" date as typed constants, as
   `py/author_misc/notes_on_aliyot.py` does; a revision date takes no time-zone label.

## Tests the page must keep passing

- `py/tests/test_sefaria_silluq_documentation.py` parses the page. Keep exactly one
  `table#meteg-after-silluq-cases` with `th[data-osis-id][scope=col]` column headers,
  `tr[data-version=sefaria]` and `tr[data-version=other-mam]` rows labelled "Sefaria" and "other
  versions of MAM", and `td` cells with `lang="hbo" dir="rtl"`. It checks the table against
  MAM-simple's annotations and both exporters' handlers, a derivation independent of the CSV files
  the generator reads, so it stays as the page's differential check. On 2026-10-24 the CSV files
  agree: in `csv/I Kings.csv` at 7:37, the verse-final atom לכלהנה has its silluq on the second
  lamed and no meteg after it. Should the CSV files ever lag MAM-simple here, the test fails, and
  that is a finding for Ben rather than something to paper over.
- `py/tests/test_shared_html_styles.py`: the page links `../document.css` before `styles.css`, and
  every `url()` in a linked sheet resolves to a file inside `gh-pages/`.
- `py/tests/test_redirect_manifest.py`: the page stays at `gh-pages/MAM-for-Sefaria/index.html`,
  where the old `bdenckla.github.io/MAM-for-Sefaria/` redirect points.
- The rendered-prose lints that cover every `gh-pages` page: `py/tests/test_prose_conventions.py`
  (Hebrew-name plurals), `py/tests/test_transliterations.py` (rendered transliterations),
  `py/tests/test_no_machine_paths_in_artifacts.py` and `py/tests/test_tracked_filenames.py`.
- For the new Python: `py/tests/test_h_dot_below_nfc.py`, `py/tests/test_transliterations.py`'s
  source checks, `py/tests/test_explicit_time_zones.py`, `py/tests/test_product_scopes.py` and
  `py/tests/test_mega_coverage.py`.
- No repository lint checks `lang` and `dir` on this page's Hebrew, so check those by reading.

## Writing rules for the page

Load `hebrew-prose` and its references `core-rules.md`, `terminology.md`, `rendered-prose.md`,
`verifying.md` and `mam-basics.md` before writing. The points this page will meet most:

- Use the house names: atnaḥ (ETNAHTA only as a Unicode name), legarmeh, pataḥ, qamats, munaḥ,
  merkha, tipeḥa in prose verses and tarḥa in poetic verses, qere, rafeh. Name accent and mark
  plurals with the default nouns of `terminology.md` ("two qamats vowels", "two meteg marks").
- Say "prose verses" and "poetic verses", never "the 21 books" or "Jb, Pr, & Ps": Job's frame is
  prose. Decide a verse's system with `py/mb_diff_mpu/describe_diff.py`'s `is_poetic`, or with a
  more central helper if the generator work finds one.
- Atom and chanted word as `core-rules.md` defines them; "has" for possession; no "witness".
- Pointed Hebrew keeps its vowels here: this page documents the encoding of every mark, the
  exception that `core-rules.md` allows where the vowel is the point. Say so in the generator's
  comment.
- Rendered-page mechanics: a real em dash; never an English sentence opening on a Hebrew word;
  `dir="rtl"` on every Hebrew table cell; pointed Hebrew immediately left of its BCV; compared
  words one above the other in one cell; romanized accent names in `<span class="romanized">`
  from shared constants rather than retyped.
- Mark names in Unicode-name small capitals where the page means a code point, as now.

## Steps

1. **Verify the checkout** as "Checkouts, baselines and ownership" says, and stop on anything
   unexpected.
2. **Track this plan** as `doc/PLAN-rewrite-MAM-for-Sefaria-encoding-page.md`, with `State: live`
   on line 3.
3. **Build the reader and the dispatch** (design items 3–4). Run them over all 78 CSV files and
   the 78 listings and settle the inventory of elements, classes and string features before
   writing prose. Any recognized feature that the outline lacks is added to the outline; anything
   unrecognized is a finding to bring to Ben, not to dispatch on by guesswork.
4. **Write the generator and the prose**, section by section in the outline's order, with the
   lookups, counts, pins and two-vowel guard of design items 5–6.
5. **Stylesheet and license rows.** In `styles.css`, remove the `prince-tooltip` declaration and
   the `span.mam-letter-small`, `-large` and `-hung` rules, which nothing emits. Style what the
   generator emits. In `DATA-LICENSES.md`, the `gh-pages/MAM-for-Sefaria/` row's "generated index
   and stylesheets" becomes true of the index; make it "stylesheet", the one there is. Add the
   font copy, the `@font-face` rule and the two license-row changes of decision 2(a).
6. **Wire the entry point and the mega step** (design items 1 and 7).
7. **Regenerate and read** the whole new page from the file, then give Ben its `file:///` link to
   view, opening nothing.
8. **Verify** as below, **commit**, and **integrate** as below. Set this plan's State to
   `executed <date>` in the last commit.

## Verification

Focused checks matched to the changed surface, per MAM-basics `doc/review-trial.md`, "Focused work
and nightly checks". The mega and the suite stay with the nightly run unless a specific consequence
cannot wait; the last pushed commit message says so, per `AGENTS.md`.

1. `./.venv/Scripts/python.exe py/main_authored.py <new subcommand>` twice; the second run
   changes nothing.
2. `./.venv/Scripts/python.exe -m black <each changed .py file>` and `git diff --check`.
3. `./.venv/Scripts/python.exe py/main_test.py py/tests/test_sefaria_silluq_documentation.py
   py/tests/test_shared_html_styles.py py/tests/test_redirect_manifest.py
   py/tests/test_prose_conventions.py py/tests/test_transliterations.py
   py/tests/test_no_machine_paths_in_artifacts.py py/tests/test_tracked_filenames.py
   py/tests/test_h_dot_below_nfc.py py/tests/test_explicit_time_zones.py
   py/tests/test_product_scopes.py py/tests/test_mega_coverage.py`, all passing.
4. `py/main_0_mega.py` has no single-step option (only `--resume-from`), so item 1 stands in for
   the new step, and the nightly mega exercises the step itself.
5. **Content checks on the rendered page:** no "old Sef", "UXLC", "WLC", "tanach.us",
   "Michigan", "PDF" or "Prince"; every Hebrew `td` has `dir="rtl"`; each count in the prose
   matches the generator's computed value, by reading the page.

## Expected changed and unchanged paths

- **Changed:** the new module, `py/main_authored.py`, `py/main_0_mega.py`, `py/product_scopes.py`,
  `gh-pages/MAM-for-Sefaria/index.html` and `styles.css`, `gh-pages/MAM-for-Sefaria/woff2/Taamey_D.woff2`,
  `DATA-LICENSES.md`, and this plan.
- **Unchanged:** everything under `MAM-for-Sefaria/` (the CSV files and listings), every other
  `gh-pages` page, and every other generator's output. Any other diff is a finding to explain
  before going on.

## Integration

1. Commit coherent steps on `main`, each message ending with the session's attribution trailer.
2. Fetch `origin`; if `origin/main` moved, merge it, rerun the affected checks, then push `main`
   normally.
3. Do not start `.github/workflows/pages.yml`. The page reaches the site at the next manual
   dispatch, which needs Ben's go-ahead.

## Ledger

| Id | Requirement | Status |
| --- | --- | --- |
| R1 | Ben, 2026-10-24: rewrite the page to document what MAM-for-Sefaria contains | implemented |
| R2 | No old Sefaria text, comparison or history on the page (follows from R1) | implemented |
| R3 | Old Sefaria's Exodus 20:4 atom, whose look depends on the installed font | superseded by R1 |
| R4 | The page covers all four folders, `csv-ajf/` and the listings included (follows from R1) | implemented |
| R5 | "AJF" stays unexpanded unless Ben supplies its meaning | implemented |
| R6 | The page's figures come from today's files, not the 2021 copy (follows from R1) | implemented |
| Q1 | Decision 1 above, how the page is produced | (a), approved with the plan, 2026-10-26 |
| Q2 | Decision 2 above, which Taamey D the page uses | (a), approved with the plan, 2026-10-26 |
| Q3 | Decision 3 above, who executes and integrates | a fresh session, approved with the plan, 2026-10-26 |

## Execution record

Executed by Claude (Opus 5.5) on 2026-10-26, in a full MAM-basics clone in a Claude-owned forest,
from `926a6e78`, a descendant of `27f263cb`, clean on `main`.

- **The generator.** `py/author_misc/mam4sef_survey.py` reads the 156 tracked files of
  `MAM-for-Sefaria/` with closed dispatch and counts what the page states;
  `py/author_misc/mam4sef_index.py` writes the page from that survey, with the lookups, pins and
  two-vowel guard of design items 5–6. `py/main_authored.py gen-mam-for-sefaria-doc` runs it,
  and so does the mega's last step, `mam-for-sefaria-doc`.
- **What the inventory added to the outline:** each listing is re-derived from its CSV file and
  must match it line for line, but for the trailing spaces that the CSV writer strips from a
  row's last field; `csv-ajf/`'s spellings are checked against the counts of `csv/`; the
  ketiv/qere shapes include a pair of three words each and two pairs separated by a maqaf,
  besides the five types the old page named; a table of all 92 code points, with the listings'
  short names; the contexts of each run of NO-BREAK SPACE, and the breaks inside verses; and,
  for the Decalogue's CGJ letters, the two strands from `csv-ajf/`, which show that the marks on
  either side of each CGJ are the two strands'.
- **Departures from "Expected changed and unchanged paths":**
  1. `py/product_scopes.py` is unchanged. The step's runner is
     `main_authored.gen_mam_for_sefaria_doc`, a function of `py/main_authored.py`, which
     `_GENERATOR_ENTRY_POINTS` already declares, so no wrapper needs declaring.
  2. `py/tests/test_mega_coverage.py` has a new `_RUNNER_CALLS` entry naming the subcommand that
     function runs, which the scan needs for a function of a program with subcommands.
  3. `py/mb_misc/mb_html.py` has the smallest writer changes the page needed: an optional
     viewport meta, `WriteCtx.viewport`, off by default, and a line-break entry for `<i>`, which
     the `Version Notes` header has. `py/mb_author/author.py` passes the viewport through
     `help_gen_html_file` and has three new romanized keys, `$gershayim`, `$telisha_gedolah` and
     `$qere_velo_ketiv`. Regenerating with `py/main_authored.py gen-misc` and
     `gen-site --trust-surveys` changed no tracked page.
  4. The meteg-after-silluq table's case list and its "other versions of MAM" row come from the
     silluq-before-meteg annotations of `MAM-simple/json-vtrad-mam/`, which no CSV file has. Its
     Sefaria row, and every other example, come from the CSV files.
  5. The romanized names come from `author.py`'s `$` keys, the single source of this family of
     pages, rather than the `ROM_*` constants of `py/accgram/printed_decalogue_strands.py`, which
     serve the printed-Decalogue pages and import the accgram grammar.
  6. The mega step is the last of `_STEPS`, rather than beside `gen-misc`: the page raises when
     its files no longer bear out a claim, as when `MAM-for-Sefaria/` lags a MAM-simple change
     the page describes, and last, that failure stops no other step.
- **Verification:** the subcommand twice, with identical output; Black on every changed Python
  file; `git diff --check`; the eleven test files of "Verification" item 3, 47 tests passing; and
  the content checks of item 5, which found none of the dropped terms and `lang="hbo"
  dir="rtl"` on every `td` that holds Hebrew. The mega and the suite are left to the nightly run,
  per `doc/review-trial.md`.
