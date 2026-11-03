# Plan: Miqra Mevoar base chapters from Rabbi Kokhav's Word files

State: live, written 2026-11-02; Ben gave his word to execute it the same day. Stages 1 to 6 ran
that evening. Avi answered on 2026-11-03 and had himself created Joshua 1, so Stage 7 waits on
Ben's word alone, and on his choice of what it now saves. The execution ledger below records each
finished stage.

Written 2026-11-02 by Claude (Opus 5.5) in the Phase 1 session that the session "Commander for
Claude's forests" started for Avi's email "Mikra Mevo'ar at Wikisource". The quoted decisions are
Ben's words; everything else is this agent's reconstruction from the Phase 1 study. A fresh
session executes this plan; the session that wrote it does not.

## What this plan does

A hand-run converter in MAM-basics turns each Word file of Rabbi David Kokhav's paraphrase, Miqra
Mevoar, into base-chapter pages for Hebrew Wikisource, and BDencklaBot creates those pages:
Joshua 1 and 2 first, as a pilot for Avi to check, then the rest. The six books now in Avi's
pCloud folder (Joshua, Hosea, Joel, Amos, Obadiah and Jonah) make 56 pages. The converter's
extracted text is tracked in MAM-basics; the Word files and the Wikisource pages are not.

## Decisions ledger

Entries 1 to 3 are Ben's decisions. Entries 5 to 9 were Claude's proposals, approved by Ben's word
in entry 3.

1. **Route: the bot, after a pilot.** Ben, 2026-11-02, answering "Which route should the pages
   take to Wikisource?" with "Bot, after a pilot" rather than "Avi pastes them". Active.
2. **What Git holds.** Ben, 2026-11-02: "Let's try to not duplicate in git what's on pCloud and
   Wikisource (source and target), but we can store intermediate stuff in MAM-basics (okay to be
   public since Wikisource is public); pCloud and Wikisource stuff can of course be cached in
   .novc and non-git tracked places like .novc if that is helpful (I imagine it would be
   helpful)". Active.
3. **Execution gate.** Ben, 2026-11-02, about 20:14 New York time, answering "Ask the commander
   to start Phase 2 now?": "Yes, ask it". Each saving bot run still needs his explicit word for
   that run: the pilot, and then the remaining pages. Creating or editing a Wikisource page is
   outward-facing. Active.
4. **Avi's agreement before the pilot.** The pilot waits for Avi's answer, relayed by Ben, to the
   first question of the draft reply in
   `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar-2026-11-02/reply-to-avi-draft.md`.
   Answered on 2026-11-03 in Avi's email, which Ben relayed. Avi asks that the bot work quietly,
   without cluttering Wikisource's recent changes, and gives its edit summary (entry 9). The
   executor reads this as his agreement; Ben's word for each run settles it.
5. **Where the code lives: MAM-basics.** It follows from entry 1: BDencklaBot, its login check
   and its run conventions are already here. Active.
6. **Mark order.** The tracked JSON keeps each Word file's own mark order, as `AGENTS.md`'s
   mark-order section requires of faithful captures and their intermediates. The pages are NFC,
   the form MediaWiki stores. The paraphrase is not MAM text. Active.
7. **No exception to the hand-run rule.** `extract`, the only subcommand that writes tracked
   output, reads nothing but Word files. MAM-simple is read by `check`, which writes nothing
   tracked, and by the suite test. So a MAM refresh owes the converter no rerun. This replaces
   the exception Phase 1 proposed. Active.
8. **The pCloud link stays out of Git.** Avi shared it with Ben by email. It is kept in
   `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar-2026-11-02/pcloud-link.txt` and given
   to `fetch` by file. Active.
9. **Edit summaries in English,** like the summaries of the 23 edit files in
   `in/mam-ws-bot-edits/`, unless Ben or Avi asks for Hebrew. Each saving run's summary is given
   on its command line and approved with the run. Avi asked on 2026-11-03 for the Hebrew summary
   פרק חדש במקרא מבואר, "a new chapter in Miqra Mevoar", so the exception applies; Ben approves
   the summary with each run.

Deferred, each until its own decision:

- Display pages for the Prophets, Avi's raw-text pages, and adding Hosea, Joel and Amos to the
  base-chapter index: questions 2, 3 and 4 of the draft reply. Each needs Avi's answer and then a
  revision of this plan. Avi answered on 2026-11-03:
  - **Display pages** come later, as a further step that needs explanation; he and Rabbi Kokhav
    have agreed on how they should look in the Prophets and the Writings.
  - **The raw-text pages** are to go once the work is done; he plans to delete them himself, so
    nothing here touches them.
  - **The base-chapter index** should be finished first, listing every chapter of the Bible, most
    of them as red links. He wrote 972 chapters; MAM-simple has 929, in 39 books, so the count
    needs confirming with him. This is new work for the bot or for a person, and it needs Ben's
    decision and a revision of this plan.
- A book that arrives as one file for two parts, such as Samuel: question 7. The converter raises
  on a second title row; revise this plan when such a file arrives. Avi expects Samuel, Kings and
  Chronicles each as a single file, as the whole Torah once came.
- Revisions after the pages exist: Avi wrote on 2026-11-03 that once the bot has created a book's
  base chapters, Rabbi Kokhav revises them on Wikisource and the Word files no longer matter. So
  the bot's update outcome should not be needed. Until then, Avi keeps revised files in the
  folder, and the copy there is always the current one.

## Execution ledger

Kept by the executing session, a Claude (Opus 5.5) session that the session "Commander for
Claude's forests" started on 2026-11-02 with a brief whose Part A is this plan, frozen at SHA-256
`F8A6FDE51BA13A47FE64417C8E1DA3D254095F95BFB2BD6BBADF2CE404C8516D`. This file began as a
byte-for-byte copy of that frozen plan; this ledger and the State line are the executor's.

- **Development checkout:** `C:/Users/BenDe/GitRepos2/MAM-basics`, assigned by the commander.
  Verified 2026-11-02 at 20:27 New York time: on `main`, clean, fast-forwarded from `6415da3b` to
  origin's `ed66e0af7f77accac633c580ab6c30de97f9a4a1`, of which `6415da3b` is an ancestor. No
  commit since `6415da3b` touches `py/main_ws_bot.py` or `py/subcommands/`.
- **Stage 1:** this file, committed as `147053a8`.
- **Stage 2:** `py/main_miqra_mevoar.py` and `py/miqra_mevoar/`, committed with Stage 3. The
  closed dispatch over Word XML is stricter than the prototype's. It reads the direct children of
  the table, its rows and its cells by name. It accepts a content control outside the table only
  when Word built it as a table of contents, as Joshua's file has after its table. It makes an
  error of every anomaly the prototype only noted: text outside the table, a second title row, a
  heading after a heading, a numbering gap, a heading with no verse after it, and a paraphrase
  cell of two paragraphs. `fetch` uses `py/mb_cmn/polite_download.py` and obeys `robots.txt`;
  pCloud's two API hosts had none on 2026-11-02.
- **Stage 3:** fetched 2026-11-02 into `.novc/miqra-mevoar/pcloud/20261102-203936-209217-0500/`.
  The seven files equal Phase 1's manifest in name, size, file id, modification time and SHA-256,
  so there is no new material from Rabbi Kokhav. `extract` and `check` passed, with the report
  `.novc/miqra-mevoar/checks/20261102-204029-102761-0500.txt`: the measurements below hold, and
  the smallest margin is that of Joshua 12:14 and 12:15, 1.000 against 0.769, in the list of
  kings. All 56 pages that `pages` wrote equal the prototype's byte for byte, and the tracked
  JSON's text equals the prototype's extraction, in the Word files' own mark order.
- **Stage 4:** `git diff --check`, Black, the targeted tests with the tree-wide lints that scan
  new files (89 passed), and the full suite (1,422 passed, 5 skipped, none of them the new
  test's). The mega was skipped, as this plan expects. Pushed as `8680140e`; origin's `main` had
  not moved.
- **Stage 5:** `py/main_ws_bot.py miqra-mevoar`, in `py/subcommands/ws_bot_miqra_mevoar.py`.
  Beyond the plan, a saving run saves with `minor=False` and cosmetic changes off, so that the
  text goes out exactly as generated. It reads each saved revision back through
  `py/ws/ws_revision_api.py`'s `ChapterClient` and tries up to four times over 35 seconds, in case
  a replica has not yet seen the revision. Every run, not only a dry run, writes its pages and
  `misc/outcomes.json`. Read-only trials on 2026-11-02, saving nothing: the pilot's dry run gave two
  creates and a non-zero exit, with pages equal to the prototype's byte for byte (run
  `.novc/mam-ws-bot-miqra-mevoar-runs/20261102-210216-168317-0500/`), and the outcome logic, run
  on the live Genesis 1 base chapter, refused a differing text, listing three revisions by other
  editors, and found the page's own text unchanged. Checks: the targeted tests with the
  tree-wide lints (98 passed) and the full suite (1,422 passed, 5 skipped). Pushed as
  `a0fa8979`; origin's `main` had not moved.
- **Stage 6:** the pilot's dry run, from `a0fa8979`, on 2026-11-02 at 21:19 New York time: two
  creates and a non-zero exit, as expected, saving nothing. Both pages equal the prototype's
  `pages/yehoshua/01.wiki` and `02.wiki` byte for byte. Neither title existed, so there is no
  finding. Run `.novc/mam-ws-bot-miqra-mevoar-runs/20261102-211949-962974-0500/`. Stage 7 waits
  on Avi's answer to the draft reply's first question, which Ben relays, and on Ben's word for the
  save and its summary.
- **Avi's Joshua 1, 2026-11-03:** Avi created the Joshua 1 base chapter himself, from the page
  attached to the reply, before he saw that the bot was to do it: revision 3101153, by Dovi, at
  00:29 New York time, its only revision. He wrote that it looks fine. A dry run from `66f8fae1`
  at 07:37 New York time found Joshua 1 unchanged, equal to the generated text, and Joshua 2 still
  a create (run `.novc/mam-ws-bot-miqra-mevoar-runs/20261103-073724-645077-0500/`). So a saving
  run would leave Joshua 1 alone. BDencklaBot's six latest edits, of 2026-11-02, all carry the bot
  flag, which keeps them out of Wikisource's recent changes by default, as Avi asks.
- **PR 366, 2026-11-03:** Codex's focused review found that an update could save against a
  revision the ownership check never read. Loading a page's history moves pywikibot 11.7.0's
  `latest_revision_id` to the newest revision. If that revision's content is not cached,
  `editpage` fetches the latest revision again while building the request, and that revision's
  timestamp becomes `basetimestamp`. A human edit made after the check would then be overwritten
  with no edit conflict. The window needs a second bot edit between two reads, so it is narrow.
  `66f8fae1` passes `baserevid` and `basetimestamp` of the newest checked revision instead, so that
  such an edit makes MediaWiki detect a conflict. Whether MediaWiki then refuses the save or
  merges it, which no live test has shown, the run fails: a refusal stops it, and a merged text
  fails its read-back check. Ben asked
  through the commander for the PR to be examined and merged if approved. It was approved and
  fast-forwarded into `main`, and GitHub shows it merged at 07:37:40 New York time. A follow-up
  commit relabels its test as one of the ws_bot tests that AGENTS.md excepts from the
  differential-or-lint rule, since the test is example-based, and asserts `baserevid` as well.

## Background for a fresh executor

Read `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar-2026-11-02/README.md` first. It
describes the Phase 1 prototype, which this plan turns into tracked code. Paths below without a
drive are relative to that folder.

- **Pages on Wikisource.** A base chapter is titled `מקרא מבואר/פרקי בסיס/ספר <book>/<chapter>`,
  with the book named by `mb_cmn.mam_bknas.he_bk39_name` and the chapter as a Hebrew numeral from
  `mb_cmn.hebrew_verse_numerals`. Its first line is the chapter heading. Each verse is one line,
  wrapped in Labeled Section Transclusion tags named by the verse numeral. A section heading is a
  line of its own before its verse, starting with `*` and wrapped in tags named `כותרת <verse>`.
  The last line is the category. `תבנית:מקרא מבואר` transcludes these sections beside MAM's
  verse. The prototype's pages use these line shapes and no others, as the live pages do: compare
  `pages/yehoshua/01.wiki` with the live capture
  `wikisource-2026-11-02/מקרא_מבואר_פרקי_בסיס_ספר_בראשית_א.wiki`.
- **What MediaWiki stores.** A saved page is NFC, with its trailing whitespace trimmed: the live
  Genesis 1 page ends at its last `]]`. Generate exactly that text, with no final newline, so a
  saved page can be compared with its source byte for byte. The pre-save transform would also
  rewrite signatures (`~~~`), `subst:` and the pipe trick, so the converter rejects them.
- **The Word files.** Each book is one table of four right-to-left columns: the chapter numeral,
  only on a chapter's first verse; the verse numeral; the Bible text, MAM copied from Wikisource;
  and the paraphrase. A heading is a row whose paraphrase cell alone is filled, styled "heading
  3" in Joshua and "heading 4" in the other five books. The title row's Bible cell, styled
  "heading 2", holds the book's pointed name, and Joshua's title row also carries the heading of
  1:1. One heading row in Joel also has a pe, a petuha marker, in its Bible cell, and a row with
  only a pe or a samekh there counts as empty. `scripts/mm_extract.py` has the closed dispatch
  over the XML (`run_text`, `para_text`, `cell_paragraphs` and `read_rows`) and over row kinds
  (`classify` and `build`). Port it, keeping every unknown element or row an error.
- **The pCloud folder.** Its public-link API needs no login.
  `https://api.pcloud.com/showpublink?code=<code>` lists the folder, and
  `https://api.pcloud.com/getpublinkdownload?code=<code>&fileid=<id>` returns hosts and a path,
  giving the download URL `https://<host><path>`. `scripts/pcloud_list.py` and
  `scripts/pcloud_download.py` use it politely.
- **Hebrew in code and prose.** Copy pointed Hebrew by script, never by typing it: the Edit and
  Write tools can reorder marks. The converter's Hebrew constants (the title prefix, the tag
  names, the heading prefix and the category) are unpointed; take them from the prototype or the
  live capture, and Stage 3's byte-for-byte comparison confirms them. Treat the paraphrase as
  Rabbi Kokhav's text and quote it sparingly in documents and commit messages. Load
  `hebrew-prose` before writing about marks or accents.

## Checkouts, baseline and instructions

- **Prototype and caches, read only:**
  `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar-2026-11-02/`, untracked, in that clone
  only.
- **Development and integration checkout:** one full MAM-basics clone in a forest Claude owns,
  assigned by the commander session. Before editing, verify it with `git rev-parse
  --show-toplevel`, `git rev-parse HEAD`, the branch, which must be `main`, and an empty `git
  status --porcelain`, and record its absolute path and exact HEAD in this ledger. Work, commit
  and push from that clone's `main`. Its own `.venv/Scripts/python.exe` runs every command below,
  from the clone's root.
- **Baseline:** fetch `origin` and fast-forward `main`. `git merge-base --is-ancestor 6415da3b
  HEAD` must succeed: at `6415da3b` this plan's study read `py/main_ws_bot.py`,
  `py/subcommands/ws_bot_real.py` and `py/subcommands/ws_bot_intro.py`. If `git log
  6415da3b..HEAD -- py/main_ws_bot.py py/subcommands/` lists commits, read them before Stage 5.
- **Instructions:** this repository's `AGENTS.md` and `doc/review-trial.md`;
  `py/ws/pywikibot-setup.md`; and, in `py/ws/ws_bot_edit_history.md`, the entry "Introduction
  note templates: every `נוסח` call given `2=`, 2026-10-18", which added the last new bot mode.
  The common instruction body's "Template dispatch is closed" and "Tests are differential or
  lint-shaped" govern the code and its test.
- **Integration owner:** the executing session.

## Stage 1. Track this plan

Copy this file to `doc/PLAN-miqra-mevoar.md`, record the development clone's path and HEAD in its
ledger, and commit. Keep it true as the stages finish: each stage's commit updates the ledger,
and the last one sets the State line.

## Stage 2. The converter: `py/main_miqra_mevoar.py` and `py/miqra_mevoar/`

A hand-run entry point with four subcommands, its code in the package.

1. **`fetch --link-file <path>`** reads the public link from the file, lists the folder, and
   downloads every file into a new directory, `.novc/miqra-mevoar/pcloud/<timestamp>/`, never
   into an existing one. It writes `manifest.json` there with each file's name, pCloud file id,
   size, modification time and SHA-256. It sends one request at a time, at least two seconds
   apart, with a User-Agent naming MAM-basics; checks each download's size against the listing;
   and rejects a `.docx` that is not a sound zip or whose expanded size is out of proportion to
   its own. It writes the link nowhere.
2. **`extract <directory>`** reads every `.docx` in the directory and nothing else. It maps each
   file's stem to its book through an explicit table (`yehoshua`, `hoshea`, `yoel`, `amos`,
   `ovadya` and `yona` today) and raises on an unknown stem. It requires the title row's text,
   its marks stripped, to equal the table's entry for that stem, copied from the files by script;
   Obadiah's title has no vav, unlike MAM's book name. It requires chapters and verses numbered
   1, 2, 3 and on without a gap. It rejects a paraphrase or heading that contains a line break or
   anything MediaWiki would interpret or transform: `[[`, `]]`, `{{`, `}}`, `<`, `>`, `~~~`, `''`,
   `__`, `&` or `subst:`. It writes `in/miqra-mevoar/<stem>.json`: the book; the source file's
   name, size and SHA-256; and the chapters, each verse with its heading or null and its
   paraphrase, in the Word file's own mark order. It does not write the Bible column, which is
   MAM's text and is already held by Wikisource and MAM-simple.
3. **`check <directory>`** extracts the same Word files again and requires the result to equal
   the tracked JSON. It requires each book's chapters, and each chapter's verse numbers, to equal
   MAM-simple's (`MAM-simple/json-vtrad-mam/`). It requires each row's Bible column, letters
   only, to match MAM-simple's same-numbered verse better than either neighbouring verse, with a
   ratio of at least 0.6 (`difflib.SequenceMatcher` without autojunk), projecting MAM-simple's
   elements through a closed dispatch as the prototype's `mam_project` does. Phase 1's floor of
   0.9 flagged two short verses with a ketiv and a qere, Joshua 15:53 at 0.78 and Hosea 10:10 at
   0.88, whose closer neighbours scored 0.34; 0.6 still separates a right row from a wrong one.
   It writes a report under `.novc/miqra-mevoar/checks/`, listing each book's five smallest
   margins, writes nothing tracked, and exits non-zero on any failure.
4. **`pages --out <new directory>`** writes each chapter's page from the tracked JSON, NFC and
   without a final newline, as `<stem>/<two-digit chapter>.wiki`, with `titles.tsv` mapping each
   file to its title.

Throughout: closed dispatch over Word XML and MAM-simple elements; no `sys.path` changes; Black on
every changed Python file; and the timestamp in New York time through
`py/mb_cmn/new_york_time.py`.

## Stage 3. The tracked intermediate, its README and its test

1. Fetch:

   ```powershell
   ./.venv/Scripts/python.exe py/main_miqra_mevoar.py fetch --link-file C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar-2026-11-02/pcloud-link.txt
   ```

   Compare the new manifest's SHA-256 values with
   `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar-2026-11-02/pcloud-2026-11-02-manifest.json`.
   A changed or new file is new material from Rabbi Kokhav: name it in the report and expect its
   differences in the steps below.
2. Run `extract` and `check` on the new directory, then `pages`. For an unchanged Word file,
   every page must equal the prototype's byte for byte, for example:

   ```powershell
   git diff --no-index --exit-code C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar-2026-11-02/pages/yehoshua .novc/miqra-mevoar/pages/<stamp>/yehoshua
   ```

   Run that for each of the six books. Any difference is a finding to explain before going on.
3. Write `in/miqra-mevoar/README.md`. It says that the files hold Rabbi David Kokhav's Miqra
   Mevoar, extracted from the Word files that reach Avi, for publication on Hebrew Wikisource
   under the license the project's main page gives, Creative Commons Attribution-ShareAlike 3.0
   Unported, whose attribution, that page says, is a direct link to it. It says that the Word
   files are not tracked and their folder is not linked; that the JSON keeps each Word file's mark
   order deliberately; and how to regenerate, with this stage's commands. It holds no pointed
   Hebrew, since `py/tests/test_prose_mark_order.py` reads every tracked `.md`.
4. Add `py/tests/test_miqra_mevoar_versification.py`, a differential test. For every
   `in/miqra-mevoar/*.json`, the book's chapters, and each chapter's verse numbers, equal
   MAM-simple's. It also lints the tracked text for the line breaks and wikitext of Stage 2's
   `extract`. It fails, never skips, when the directory is empty or a book is missing from
   MAM-simple. Add no example-based tests.
5. Declare each new subcommand in `NOT_IN_MEGA` in `py/tests/test_mega_coverage.py`, following
   the entry for `py/main_ws_bot.py intro`: `fetch` downloads from a third-party host; `extract`
   and `check` read Word files that exist only where `fetch` ran; and `pages` writes untracked
   previews only.

## Stage 4. Verify and push the converter

Run `git diff --check` and Black on the changed Python files, then the targeted tests:

```powershell
./.venv/Scripts/python.exe py/main_test.py py/tests/test_miqra_mevoar_versification.py py/tests/test_mega_coverage.py py/tests/test_product_scopes.py py/tests/test_prose_mark_order.py py/tests/test_tracked_filenames.py
```

then the full suite:

```powershell
./.venv/Scripts/python.exe py/main_test.py
```

The mega reads none of the new files and runs none of the new code, so skipping it is expected;
say so in the message of the last commit pushed, as `AGENTS.md` requires. Expected unchanged:
every product directory that `py/product_scopes.py` declares, `in/mam-ws/` and
`in/mam-ws-bot-edits/`. Commit, fetch, merge `origin/main` if it moved and rerun the affected
checks, and push `main`.

## Stage 5. The bot mode: `py/main_ws_bot.py miqra-mevoar`

Add the subcommand in `py/subcommands/ws_bot_miqra_mevoar.py`, modelled on `ws_bot_intro.py`.

1. Its arguments are `--book <stem>`, repeatable; `--chapters <first>-<last>`, with one book
   only; `--no-save`; `--summary <text>`, required unless `--no-save`; and pywikibot's `-dir:`.
   It reuses `ws_bot_real.assert_pywikibot_dir_configured`.
2. For each selected chapter it generates the page with the converter's own function from the
   tracked JSON, reads the live page, and gives the chapter one of four outcomes:
   1. **create:** the page does not exist. Save with `createonly=True`, so that a page someone
      else made in the meantime is not overwritten.
   2. **unchanged:** the live text equals the generated text. Nothing to do.
   3. **update:** the texts differ and every revision of the page is BDencklaBot's. Save with
      `nocreate=True`.
   4. **refuse:** the texts differ and someone else has edited the page. Save nothing for it,
      list the page with the other editors' revisions, and exit non-zero when the run ends. People,
      not the bot, reconcile a revision from Rabbi Kokhav with an edit made on Wikisource.
3. With `--no-save` it writes every generated page into the run directory, lists each chapter's
   outcome, saves nothing, and exits non-zero if any page would be created or updated, as the
   other modes' dry runs do.
4. A saving run then reads each saved page again from the API, uncached, and requires its text
   to equal the generated text byte for byte. It records each page's old and new revision ids
   and diff links in `misc/saved-pages.json` and exits non-zero on any mismatch. There is no MAM
   post-run download, since no MAM page changes.
5. Its run artifacts go to `.novc/mam-ws-bot-miqra-mevoar-runs/<timestamp>/`.
6. Update `py/main_ws_bot.py`'s docstring examples and `py/ws/pywikibot-setup.md`, and declare
   the mode in `NOT_IN_MEGA` as the `intro` mode is declared: it saves to live Hebrew Wikisource
   under Ben's bot account, so every run is a deliberate act.

Verify as in Stage 4, then push.

## Stage 6. The pilot's dry run

Reading through the bot's login saves nothing, so this needs no further word from Ben:

```powershell
./.venv/Scripts/python.exe py/main_ws_bot.py miqra-mevoar --book yehoshua --chapters 1-2 --no-save -dir:$env:USERPROFILE/.pywikibot
```

Expected: two creates and a non-zero exit, with the run's two pages equal byte for byte to the
prototype's `pages/yehoshua/01.wiki` and `02.wiki`. On 2026-11-02 none of the 56 titles existed
(`wikisource-2026-11-02/target-status.json`), so an existing page now is a finding. Report to Ben
and stop.

## Stage 7. The pilot's save, on Ben's word

Preconditions: Avi's agreement (ledger entry 4) and Ben's explicit word for this run, including
its summary. Run Stage 6's command without `--no-save` and with `--summary`. The run's own
byte-for-byte check must pass. Then add an entry to `py/ws/ws_bot_edit_history.md` in that file's
form: purpose, authorization quoting Ben, the new mode, each page's new revision id, the safety
rule, and the run's and the dry run's artifact directories. Update this plan's ledger, commit and
push, and report the two pages' links to Ben for Avi.

## Stage 8. The other 54 pages, on Ben's word

After Avi has looked at the pilot and Ben gives his word: a dry run over all six books, expecting
54 creates and 2 unchanged pages; the saving run and its check; a history entry; this plan's
State set to executed; commit and push.

## Later Word files

A new or revised book repeats Stage 3's fetch, extract and check, and a reading of the tracked
JSON's diff, and then Stages 6 to 8 for its pages, each saving run again on Ben's word. An update
goes through only for pages that nobody but BDencklaBot has edited.

## Measurements of 2026-11-02

Dated observations from the prototype, which `check` measures again:

- Six books, 56 chapters and 1,141 verses: Joshua 656, Hosea 197, Joel 73, Amos 146, Obadiah 21
  and Jonah 48. Every chapter's verse count equals MAM-simple's.
- 85 headings: Joshua 43, Hosea 13, Joel 3, Amos 21, Obadiah 1 and Jonah 4.
- No paraphrase or heading has a control character, a line break, a space at either end, or
  wikitext.
- Avi's raw-text drafts on Wikisource equal the generated text, after NFC, for all of Obadiah and
  Jonah and 655 of Joshua's 656 verses. The exception is the heading before Joshua 12:9, which
  the draft runs onto 12:8 and the Word file gives its own row.
- BDencklaBot is in the `bot`, `user` and `autoconfirmed` groups, has the `createpage` and
  `noratelimit` rights, and had 1,960 edits. None of the 56 titles existed.
