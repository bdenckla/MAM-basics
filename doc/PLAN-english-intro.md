# Plan: keep the English Introduction to MAM in parallel on English Wikisource and in gh-pages

State: live; Phases 1 and 2 executed 2026-11-22; Phase 3 next, by Ben's Decision 2

## Origin, and whose words are whose

Written by Claude (Opus 5.5) on 2026-11-22, in a session that the commander session "Commander
for Claude's forests" (`local_a80ded65-f78e-4280-8493-9dab3b8c5686`) started at Ben's word. Ben
typed this in the commander at 09:37 New York time on 2026-11-22, as the commander's brief,
`intro-en-brief-2026-11-22.md`, copies it:

> start a session that will:
>
> 1. (perhaps in a sub-agent, to manage context bloat) download the fragments of an English translation of the Intro to MAM that exist on English Wikisource, downloading them to a git-tracked location that is in some sense (you choose the details of exactly in what sense) parallel to the git-tracked downloads of the Hebrew original Intro to MAM on Hebrew Wikisource.
>
> 2. that session (or a follow-up, or a sub-agent) will also evaluate that translation and suggest tweaks where it seems to fall short.
> 3. that session (or a follow-up, or a sub-agent) will create a thin (short) github issue regarding improving and expanding that translation on english wikisource, including perhaps uploading those few small snippets of translation that we only hold "privately" in mam-basics gh-pages (by "privately" I mean "not on English Wikisource (yet)". As usual this thin github issue will (or at least can, if needed) point to a "thick" plan in the "doc" dir of MAM-basics, usually recorded as one or more markdown files. the overall plan would be to maintain the translation in parallel, both on english wikisource and on mam-basics gh-pages. For one thing, there are some features of presentation that we can do in gh-pages that we can't do on english wikisource (like side-by-side presentation). BTW, does the current side-by-side allow closing/opening "sides" (all 3 modes: Hebrew, English, and bilingual?) […] well obviosly i've mentioned a lot of things here so I'll mention once again, please use sub-agents or separate sessions to handle these things (and perhaps judiciously use parallelism, i.e. where possible use parallelism)

The bracketed omission is one sentence pointing to a private precedent for the modes, which
this public file does not describe. Everything else in this plan is Claude's reconstruction and
design, not Ben's words, until a decision below quotes him. Ben's "Intro to MAM" is the introduction that `in/mam-ws-intro/`
mirrors from Hebrew Wikisource. The decision page,
`https://claude.ai/artifact/6q3B6d6QmYh8QxMeDG8uJB`, puts this plan's open decisions to Ben, with
their recommendations; "Decisions" below records the ones he has answered.

## Where things stand on 2026-11-22

### The Hebrew introduction and its mirror

Hebrew Wikisource's introduction to MAM has thirteen pages, mirrored byte for byte in
`in/mam-ws-intro/` by `py/main_download.py fr-ws-intro`, with `manifest.json` recording each
page's revision. `in/mam-ws-intro/README.md` describes the mirror. Seven of the thirteen pages
end with an interlanguage link to English Wikisource, alone on its line: `root`, `summary`,
`ch1`, `ch2`, `ch3`, `appendices` and `data-sheet-guide`. The other six, `ch4`, `ch5`, the two
manuscript indexes and the two technical guides, have none.

### The English on English Wikisource

The seven linked English pages are subpages of `User:Dovi/Miqra according to the
Masorah/Introduction`, in the user space of Dovi, Avi Kadish's account. This session read
their article views on 2026-11-22, one at a time and at least five seconds apart, and nothing
else of English Wikisource but `robots.txt` and the policy pages below:

| Hebrew slug | English subpage | Revision | Last edited (UTC) | Rough words | What it holds |
|---|---|---|---|---|---|
| `root` | (the root) | 15106504 | 2025-06-01 09:17 | 430 | a contents list, and a note to the reader by the translator |
| `summary` | `/Abstract` | 15903740 | 2026-04-24 19:25 | 2,060 | the edition's English abstract |
| `ch1` | `/Chapter 1` | 14796317 | 2025-01-17 13:24 | 45 | a title only |
| `ch2` | `/Chapter 2` | 14796320 | 2025-01-17 13:24 | 1,450 | two sections, headed 4.6 and 9.1 |
| `ch3` | `/Chapter 3` | 14833310 | 2025-01-30 18:26 | 8,310 | a partial translation |
| `appendices` | `/Appendices` | 14796325 | 2025-01-17 13:26 | 3,190 | a partial translation |
| `data-sheet-guide` | `/Technical Guide to the Spreadsheet` | 14796335 | 2025-01-17 13:29 | 1,690 | the guide to the data sheet |

The word counts are rough counts of Latin-letter words in each rendered page, navigation
included. Chapters 4 and 5 have no English page. The root's note to the reader is signed by
Mitchell Powell. It describes the translation as a student's partial draft, made slowly with
online dictionaries and machine translation, and releases it under CC BY-SA. An eighth page
under the prefix, which the article views did not show, is a redirect: Phase 1's first refresh
found it (item 4 below). Four redirects matter here:

1. `User:Dovi/Miqra according to the Masorah/Information about this Edition`, which the Hebrew
   root's interlanguage link names, leads to the English root.
2. `User:Dovi/Miqra according to the Mesorah`, which the Hebrew root and summary link inline,
   leads to the edition's main English page, `User:Dovi/Miqra according to the Masorah`, outside
   the seven.
3. `User:Dovi/Miqra according to the Mesorah/Technical Guide`, which the Hebrew root links inline,
   leads to the Technical Guide.
4. `User:Dovi/Miqra according to the Masorah/Introduction/Technical Guide`, revision 14796336,
   which the English root's contents list links, leads to `/Technical Guide to the Spreadsheet`.
   Dovi's move of the guide from that title on 2025-01-17 left it behind. It is the one redirect
   under the prefix, and the English mirror holds it, under `technical-guide`, the slug of the
   Hebrew redirect to the Hebrew guide.

### The English held only in gh-pages

These English translations of the introduction are in `gh-pages/`, and none of the seven
English Wikisource pages holds them, as far as their section headings show:

| Page | Writes it | Hebrew source | English, with notes | What the page says of its English |
|---|---|---|---|---|
| `gh-pages/MAM-with-doc/misc/he_ws_intro_to_mam_gray_maqaf_1.html` | `py/author_misc/he_ws_intro_to_mam_gray_maqaf_1.py` | `ch2`, the gray-maqaf section's introduction and its first subsection | about 1,330 words | original to this project |
| `gh-pages/MAM-with-doc/misc/he_ws_intro_to_mam_pasleg.html` | `py/author_misc/he_ws_intro_to_mam_pasleg.py` | `ch2`, the paseq and legarmeh section, all six of its subsections | about 3,570 words | original to this project |
| `gh-pages/MAM-with-doc/misc/he_ws_intro_to_mam_gaya_text.html` | `py/author_misc/he_ws_intro_to_mam_gaya_text.py` | `ch3`, the section on this edition's meteg marks | about 960 words | AI-generated, not yet reviewed by a human |
| `gh-pages/aleppo/missing_sections_torah.html` | hand-edited | `ch3`, one paragraph | about 60 words | prepared separately |
| `gh-pages/aleppo/missing_sections_nakh.html` | hand-edited | `ch4`, one section | about 440 words | prepared separately |

The site index lists all five under "Excerpts from the Introduction to MAM". The gray-maqaf
English was already in this repository's first commit, `d86e5779`, a history-free snapshot of
an earlier repository, so its first author cannot be read here. Both of the first two pages'
English was revised or written in later commits with a Claude co-author trailer, starting with
`e53361e2` and `cad5700f`. No file here says who translated the two Aleppo pages. The unlinked
audit page `gh-pages/intro-doc-audit/index.html` also holds about 190 agent-written translations
of single sentences or fragments, for an audit rather than for reading.

### The side-by-side pages today

The three generated pages are fixed two-column tables, laid out by `he_en_table_wct` in
`py/mb_author/author.py`: Hebrew on the left at 40% and English on the right at 60%, with an
English label row over each section. `py/main_authored.py gen-misc` writes them. They have no
script, no control and no viewport tag, so a reader cannot hide either column, and a phone
shrinks the desktop layout. Every footnote anchor is in the Hebrew column, and the English
footnote links point to it. Some material exists only on the English side: the label rows, the
paseq page's images of the Leningrad Codex, and the gaya page's per-book tables and its notes on
the translation. The two Aleppo pages are fixed tables with the English on the left.

### What English Wikisource's policies say

A reading of ten policy and help pages on 2026-11-22 found the following. Each claim names its
page.

1. Translations made by Wikisource contributors belong in the `Translation:` namespace, under
   `{{Translation header}}`, and need an original on the source language's Wikisource that is
   backed by scans and complete through the translated part, with an interlanguage link to it
   ([Wikisource:Translations](https://en.wikisource.org/wiki/Wikisource:Translations)). The
   Hebrew introduction is a text born on Wikisource, with no scans, so whether it can have a
   `Translation:` work is an open question.
2. That policy allows one English translation per original. It sets no completeness or review
   requirement, but abandoned incomplete works may be nominated for deletion.
3. Wikisource does not generally host extracts or selected sections of a larger work
   ([Wikisource:What Wikisource includes](https://en.wikisource.org/wiki/Wikisource:What_Wikisource_includes)),
   and the same page lists introductions among annotations.
4. User space holds a user's incomplete or experimental subpages
   ([Help:Namespaces](https://en.wikisource.org/wiki/Help:Namespaces)). No page read says how
   long a translation may stay there, how it moves, or how other users should edit it.
5. None of the pages read mentions machine translation or AI-generated text.
6. `{{Bilingual}}` sets facing pages of one scanned bilingual book side by side
   ([Template:Bilingual](https://en.wikisource.org/wiki/Template:Bilingual)), and the guideline
   on multilingual texts is a proposed placeholder
   ([Wikisource:Multilingual texts](https://en.wikisource.org/wiki/Wikisource:Multilingual_texts)).
   Nothing sets a Hebrew Wikisource original beside its English.

### Wikimedia's robots.txt and Robot policy

Wikimedia's `robots.txt`, which `en.wikisource.org` and `he.wikisource.org` both serve,
disallows `/w/` to every user agent; the two copies read on 2026-11-22 differ only in their
sitemap line and in comments. That rule covers the Action API, `/w/api.php`, and
`/w/index.php`. The file's comment welcomes friendly, low-speed bots on article pages, but not on
dynamically generated pages. Wikimedia's
[Robot policy](https://wikitech.wikimedia.org/wiki/Robot_policy), last edited 2026-03-16, asks
every client to honor every directive of `robots.txt`. It also has an Action API section, which
sets the limits for an unauthenticated client: one request at a time, and fewer than five a
second. `fr-ws-intro`, `fr-wikisource` and the introduction bot already read Hebrew Wikisource
through the Action API under the same `robots.txt`, the downloaders with
`obey_robots_txt=False`. No recorded decision of Ben's covers that.

## Decisions

### Answered on the decision page, 2026-11-22

Ben, 2026-11-22, of the decision page's recommendations for the three decisions below: "I concur
with all three off your recommendations on the decision page."

1. **Decision 1: how the English mirror reads English Wikisource. Answered 1A**, the Action API
   as the Hebrew mirror uses it, within the Robot policy's Action API limits. The choices not
   taken were 1B, only URLs that `robots.txt`'s directives allow, that is the article view for
   the revision id and `/wiki/<title>?action=raw&oldid=<revision>` for the wikitext, and 1C,
   asking Wikimedia first, at the address the Robot policy gives. Phase 1 carried it out.
2. **Decision 2: three modes for the side-by-side pages. Answered 2A**, Hebrew, English and
   bilingual modes built once in the shared builder, with the Hebrew left where it is. The
   choices not taken were 2B, the same with the Hebrew on the right, and 2C, not now. Phase 3
   carries it out.
3. **Decision 3: the thin issue's text. Answered 3A**, the draft on the decision page, which
   points to this plan. It is filed as
   [MAM-basics#375](https://github.com/bdenckla/MAM-basics/issues/375), "Improve and extend the
   English translation of MAM's introduction".

### Later, put to Ben when their phase starts

4. **Where the English lives on English Wikisource** (Phases 4 and 5): in Dovi's user space,
   which needs his consent to edits; in a `Translation:` work, if the scan requirement allows
   one; or elsewhere.
5. **Who is consulted before editing** (Phases 4 and 5): Avi Kadish, whose user space holds the
   pages, and Mitchell Powell, who translated them.
6. **Whether AI-assisted English is uploaded, and how it is labeled** (Phase 5).
7. **Which copy of each passage is the text** (Phase 6): the recommendation is below.
8. **The Hebrew downloaders' practice** under Wikimedia's `robots.txt` (Phase 7).

## The design: one English text, two presentations

MAM itself lives on Hebrew Wikisource, and MAM-basics mirrors it and renders it. The
recommendation is to treat the English the same way: English Wikisource holds the English text
of each passage it has, `in/mam-ws-intro-en/` mirrors that text, and `gh-pages/` renders it
beside the Hebrew mirror, with what only `gh-pages/` can do. A passage that is not yet on
English Wikisource keeps its authored English in this repository's generators until it is
uploaded. Once it is uploaded, a differential check compares its generated English with the
mirrored English, which is the oracle, and every difference is a finding to reconcile by hand.
Edits by other people on English Wikisource then reach this repository as mirror diffs, read on
each refresh, rather than being overwritten.

What `gh-pages/` can present that English Wikisource cannot:

1. The Hebrew original from Hebrew Wikisource set beside its English, passage by passage.
2. The reader's choice of Hebrew, English or both (Phase 3).
3. Pointed Hebrew in Taamey D.
4. Notes that open in place, a copy in each column.
5. Links into MAM-with-doc's verses and documentation notes, and into this repository's
   analyses.
6. Generated checks: each passage's staleness against the Hebrew revision it translates, and the
   section map of Phase 6.
7. A boxed caveat on English that no human has reviewed.

What English Wikisource offers that `gh-pages/` cannot: open editing with its history, the
Hebrew pages' interlanguage links, the edition's own English home, and the wiki's readers and
search.

## Phases

Each phase runs in a full clone in a forest that Claude owns, on `main`, as the user-level
instructions say. A fresh session executes each phase and owns its integration.

### Phase 1: the English mirror (executed 2026-11-22)

Ben's item 1. The mirror goes in `in/mam-ws-intro-en/`, beside the Hebrew one, refreshed by a
new `py/main_download.py fr-ws-intro-en`, separate from `fr-ws-intro` for the reason the Hebrew
mirror is separate from `fr-wikisource`: unrelated refresh rhythms.

1. Verify the checkout: `git rev-parse --show-toplevel`, `git rev-parse HEAD`, the branch and
   `git status --porcelain`; then fetch and fast-forward `main`.
2. Write `py/subcommands/download_wikisource_intro_en.py`, modeled on
   `py/subcommands/download_wikisource_intro.py`:
   - `_SLUG_TO_TITLE` declares the eight pages under the prefix, each under its Hebrew
     counterpart's slug, so `in/mam-ws-intro-en/ch3.mediawiki` translates part of
     `in/mam-ws-intro/ch3.mediawiki`: the seven of the table above, and the redirect of
     "The English on English Wikisource", item 4, under `technical-guide`.
   - A live-set check fails if the pages under the prefix gain or lose one. It lists the
     prefix with `list=allpages`, redirects included.
   - A pairing check fails unless each Hebrew page paired with an English page with text has
     exactly one interlanguage link, naming that page or a redirect to it, and every other
     Hebrew page has none. A redirect check fails unless the English redirect and the Hebrew
     redirect of `technical-guide` each lead to their own wiki's page of `data-sheet-guide`.
   - Metadata comes by title and then the exact bytes by revision id, one request at a time,
     at least five seconds apart, with `maxlag=1`. The pairing check resolves the Hebrew
     pages' interlanguage targets through a `ws_revision_api.ChapterClient` of its own, since a
     redirect and its target are one page under two titles, which a `ChapterClient` refuses.
     The declared pages' metadata comes from a query that follows no redirect, so that the
     declared redirect is read as itself, and their bytes from
     `ChapterClient.by_raw_revisions`.
   - It writes each page's wikitext byte for byte, and a `manifest.json` with the Hebrew
     manifest's `title`, `revid`, `timestamp` and `size`, plus `hebrew_title`, taken from the
     Hebrew manifest.
3. Register the subcommand in `py/main_download.py`, in its docstring's list and examples too.
4. Declare it in `NOT_IN_MEGA` of `py/tests/test_mega_coverage.py`, with a reason beginning
   "Claude-written proposal, not yet reviewed by Ben".
5. Write `in/mam-ws-intro-en/README.md`: the sense in which the mirror is parallel, its file
   table, its refresh command, Ben's Decision 1 quoted, its license and staleness, and the
   translator's note. Add a `DATA-LICENSES.md` row: CC-BY-SA 4.0, English Wikisource's terms;
   the translator's note also releases the English under the CC BY-SA license, naming no
   version. Add one sentence to `in/mam-ws-intro/README.md` pointing to the English mirror.
6. Run the refresh twice. The second run must leave a clean tree, which is the mirror's check.
   Read every mirrored file and the manifest, and compare each `size` with the bytes on disk.
7. Run Black on the changed Python, then
   `./.venv/Scripts/python.exe py/main_test.py py/tests/test_mega_coverage.py py/tests/test_tracked_filenames.py`.
8. Commit, naming the paths, with the message in a file. Fetch and merge `origin/main`, then
   push.

**Executed 2026-11-22** in `C:/Users/BenDe/GitRepos2/MAM-basics`, from `2f2a11bd`, in the commit
that records it here. The first refresh failed its live-set check: the listing found an eighth
page under the prefix, `/Technical Guide`, which the article views had not shown. One more
request read it as itself, a 102-byte redirect to `/Technical Guide to the Spreadsheet`. The
Hebrew mirror already holds its own redirect of the same slug "as the redirect it is", in the
words of `py/subcommands/download_wikisource_intro.py`, so the English mirror applies that rule
and holds this one under `technical-guide`, with step 2's redirect check. The seven pages with
text came at the revisions of the table above. The second refresh wrote the same bytes as the
first. Each `size` matched the bytes on disk, and no file holds a carriage return. Every mirrored
file was read in full: each is one complete wiki page, and each fits its row of the table
above. Three steps
beyond the list above follow from the mirror's being a verbatim capture, as the Hebrew one is:

1. `.gitattributes` keeps the line-final blanks of `ch2` (1 line), `ch3` (23) and `appendices`
   (1), as it keeps the Hebrew mirror's.
2. `doc/mam-normal-mark-order.md` records the 339 clusters of `ch3.mediawiki` in the other mark
   order.
3. `py/tests/test_h_dot_below_nfc.py` excludes the English captures by name, as it does the
   Hebrew ones, though none has a decomposed h with dot below today.

The focused tests of step 7, run with `py/tests/test_h_dot_below_nfc.py` and
`py/tests/test_entry_point_subcommands.py`, passed: 50 tests.

### Phase 2: the evaluation (executed 2026-11-22)

Ben's item 2. [intro-en-evaluation-2026-11-22.md](intro-en-evaluation-2026-11-22.md) compares each
English page with the Hebrew mirror and records each shortfall with a suggested tweak. Seven
parallel sub-agents read one slice each, from the article views of the revisions in the table
above. With its update file,
[intro-en-evaluation-2026-11-22-update.md](intro-en-evaluation-2026-11-22-update.md), it records
243 findings, 71 of them substantive, and five problems that run through the pages:

1. drift, since most of the English predates revisions of the Hebrew, including the data sheet's
   freeze on 12 September 2026 and a relabeled roster of sigla;
2. wrong verse references and names, such as Deuteronomy given chapters 40 to 44;
3. terms of art read as ordinary words;
4. an unfinished draft's query marks and garbled sentences;
5. terminology off the house rules.

Its findings are not yet acted on. Later dispositions go in its single update file, as the
`iterative-document-editing` skill says.

### Phase 3: three modes for the side-by-side pages (Decision 2A; next)

Ben's question, "does the current side-by-side allow closing/opening "sides" (all 3 modes:
Hebrew, English, and bilingual?)". The answer on 2026-11-22 is no. Under 2A:

1. In `he_en_table_wct` and `_he_en_table_wci_row_pair` of `py/mb_author/author.py`, mark each
   Hebrew cell, English cell and label row with a class, and wrap the table so that one
   attribute on the page selects the mode.
2. Add a three-button control, Hebrew's own name, "English" and "Both", pinned at the top right
   with room kept for it, hidden until script runs, and with `aria-pressed` on the current
   button. Bilingual is the default and the view without script. The query `?view=he`,
   `?view=en` or `?view=both` names a mode, and nothing is stored. Print follows the mode on
   screen.
3. Give each column its own footnote ids, so that the English footnote links land on English
   copies of the notes. Today every anchor is in the Hebrew column, made by each generator's
   marker functions.
4. Show the material that only the English side has in the English and bilingual modes.
5. Ask `py/mb_misc/mb_html.py` for the viewport tag, which it adds only on request, and stack
   the bilingual columns on a phone, Hebrew above English.
6. Find where the pages' stylesheet, `gh-pages/MAM-with-doc/misc/style.css`, is authored before
   changing it, and keep any new script and style with it.
7. Regenerate with `./.venv/Scripts/python.exe py/main_authored.py gen-misc` and read the diff of
   all three pages. Check each mode at desktop and phone widths in a browser, since the change is
   script behavior.
8. Commit and push. `gh-pages/` is a published product, so the last commit pushed says which
   broad checks it skipped and why, as `AGENTS.md`'s products section requires.

### Phase 4: the evaluation's tweaks on English Wikisource (on Ben's word)

This phase edits English Wikisource, which is outward-facing. It starts only when Ben says so,
after Decisions 4 and 5.

1. Take the findings Ben accepts from the evaluation. Start with the four links of the English
   Appendices to `hcanat.us`, the UXLC's development host (`appendices-8`). Ben, 2026-11-22:
   "we are trying to stamp out all uses of hcanat.us from all MAM-related stuff. It is a dev
   server." `7f43a3c8` removed that host from the Hebrew introduction on 2026-11-06.
2. Write each link to a UXLC verse in tanach.us's HTML view, which `uxlc_verse_url` in
   `py/mb_cmn/uxlc_verse_url.py` builds, as `738dae4e` does for this repository's own pages
   (`ch3b-37`, in the update file). A link to the whole `Tanach.xml` stays XML, as that commit
   keeps XML downloads.
3. Edit the English pages by hand, or through a new `intro-en` mode of `py/main_ws_bot.py`,
   modeled on `intro`: an explicit-replacement edit file, a `--no-save` dry run, and a saving
   run that refreshes the English mirror. The bot account `BDencklaBot` edits Hebrew Wikisource
   today; whether it edits English Wikisource is Ben's choice.
4. Refresh the mirror, read its diff, and record each finding's disposition in
   `doc/intro-en-evaluation-2026-11-22-update.md`.

### Phase 5: the English held only in gh-pages, uploaded (on Ben's word)

Ben's "uploading those few small snippets of translation that we only hold "privately" in
mam-basics gh-pages". It starts only when Ben says so, after Decisions 4, 5 and 6.

1. Before any upload, a human reviews the gaya page's English, which its own caveat calls
   unreviewed AI output. The translator and terms of the two Aleppo pages' English are
   established first.
2. Generate each passage's wikitext from the same generators that write its page, so that the
   upload is regenerable and the passage has one authored copy. Hand-copied wikitext is a
   second copy that drifts.
3. Upload under the placement of Decision 4, then refresh the English mirror and add each new
   page to `_SLUG_TO_TITLE` and to the README's table.
4. Add the differential check of "The design" for each uploaded passage.

### Phase 6: keeping the two in parallel (live)

1. Keep a tracked section map, with each English section and the Hebrew section it translates,
   starting from the evaluation's section maps. A lint fails if a mapped heading is gone from
   either mirror.
2. On each `fr-ws-intro` refresh, list the mapped English sections whose Hebrew changed, from the
   mirror diff, as candidates for the translation to follow.
3. On each `fr-ws-intro-en` refresh, read the diff. For a passage rendered in `gh-pages/`,
   regenerate the page or run the differential check.
4. Render each passage that English Wikisource holds from the English mirror, beside the Hebrew
   mirror, in the Phase 3 layout. That needs a renderer of the English pages' wikitext that
   dispatches explicitly on every template it recognizes and raises on any other, as the
   user-level instructions require.

### Phase 7: the Hebrew downloaders under Wikimedia's robots.txt (on Ben's word)

Decision 1 decides only the English mirror. Whatever Ben decides there, `fr-ws-intro`,
`fr-wikisource`, the special-page download and the bots raise the same question, and this phase
records his answer for them.

## Checkouts, interpreters and skills

- **Checkout:** a full MAM-basics clone in a forest that Claude owns. This plan was written in
  `C:/Users/BenDe/GitRepos2/MAM-basics` at `45a975f7`. Each phase records its own HEAD before
  editing.
- **Interpreter:** that clone's `./.venv/Scripts/python.exe`, from the clone's root.
- **Skills:** `hebrew-prose`, with its `references/mam-basics.md`, for any English rendering of
  the introduction; `iterative-document-editing` for this plan and the evaluation's update;
  `github-issues` for the issue that points here.
- **Unchanged outputs:** Phases 1, 2 and 4 change nothing that the mega writes. Phase 3 changes
  only the three pages that `gen-misc` writes, and Phase 5 only adds wikitext beside them. An
  unexpected diff elsewhere is a finding.
- **Verification:** `doc/review-trial.md` governs: focused checks matched to what changed, Black
  on every changed Python file, and the mega and the suite left to the nightly run unless Ben
  asks.
- **Commits:** on `main`, naming their paths, messages in files; fetch and merge `origin/main`
  before each push; never rewrite history.
- **Privacy:** MAM-basics is public. Nothing from MAM-private goes into it.
- **Publication formats:** print and Kindle editions of the introduction are another session's
  plan, not this one's.
