# Plan: Miqra Mevoar base chapters from Rabbi Kokhav's Word files

State: live, written 2026-11-02; Ben gave his word to execute it the same day. Stages 1 to 6 ran
that evening, and Stages 7 to 9 on 2026-11-03: Avi had himself created Joshua 1, BDencklaBot
created the other 55 base chapters of the six books, and the base-chapter index, which Stage 9
added at Ben's request, links all 929 chapters as revision 3101215. Ben offered Avi the bot for
the display pages (decisions ledger entry 13), and Avi accepted, in an answer that Ben relayed on
2026-11-04 (Deferred, “Display pages”). Stage 10, written that day and executed on Ben's word the
same day, had the bot create the seven of those pages whose base chapters exist, as revisions
3101357 to 3101363, and Ben then sent Avi a reply about them with three questions (execution
ledger, “The reply to Avi”). The State stays live: the display pages of the other seven books of
the Twelve wait for their base chapters (Stage 10, “Left out”, and “Later Word files”), and the
next display work waits on Avi's answer. The execution ledger below records each finished stage.

Written 2026-11-02 by Claude (Opus 5.5) in the Phase 1 session that the session "Commander for
Claude's forests" started for Avi's email "Mikra Mevo'ar at Wikisource". The quoted decisions are
Ben's words; everything else is this agent's reconstruction from the Phase 1 study. A fresh
session executes this plan; the session that wrote it does not.

## What this plan does

A hand-run converter in MAM-basics turns each Word file of Rabbi David Kokhav's paraphrase, Miqra
Mevoar, into base-chapter pages for Hebrew Wikisource, and BDencklaBot creates those pages:
Joshua 1 and 2 first, as a pilot for Avi to check, then the rest. The six books now in Avi's
pCloud folder (Joshua, Hosea, Joel, Amos, Obadiah and Jonah) make 56 pages. The converter's
extracted text is tracked in MAM-basics; the Word files and the Wikisource pages are not. Stage 9,
added on 2026-11-03, has the bot complete the base-chapter index so that it links all 929 of
MAM's chapters. Stage 10, added on 2026-11-04, has it create the display pages that Avi asked for
whose base chapters exist: Joshua's two parts and five books of the Twelve.

## Decisions ledger

Entries 1 to 3 and 10 to 13 are Ben's decisions. Entries 5 to 9 were Claude's proposals,
approved by Ben's word in entry 3.

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
10. **The index by bot.** Ben, 2026-11-03, on the base-chapter index that Avi asked to have
    finished: "I think this is a great task for a bot". Of Avi's count of 972 chapters he said
    "Let's assume he meant 929". Asked "Shall I write the bot's index stage into the plan?", he
    answered "Yes, write it"; Stage 9 is that stage. Active.
11. **The index's books in two parts.** Ben, 2026-11-03, answering "For Samuel, Kings,
    Ezra–Nehemiah and Chronicles: one section per book, or one per part?": "One per book". Each
    such book gets one section with a labelled run per part, as the Twelve has; Stage 9's design
    item 2 follows it. Active.
12. **The index's save does not wait for Avi.** Ben, 2026-11-03, about 11:07 New York time, in
    the Phase 2 session, answering "The email to Avi is ready to send, as in my last message;
    it’s saved at email-to-avi-2026-11-03.md.": "I don't think it is ready to send until we
    complete all Miqra Mevoar work that is not gated on his approval (and report it in that
    email); in particular the 929-chapter index work". So the index's save needs only Ben's word
    for that run, with its summary, and the email reports it. Active.
13. **Display pages: offer Avi the bot.** Ben, 2026-11-03, about 17:55 New York time, in the
    Stage 8 session, answering the recommendation "I recommend offering Avi the bot, once he has
    made his choices for titles and breaks.": "yes offer Avi the bot and draft an email reporting
    on progress and asking questions about next steps". The draft, for Ben to send, is
    `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar/email-to-avi-2026-11-03-six-books.md`.
    It offers a bot-made display page for each of Hosea, Joel, Amos, Obadiah and Jonah, and asks
    Avi's choices of titles, breaks, other content and links. A display stage is written into
    this plan only if he accepts. He accepted, in the answer that Ben relayed on 2026-11-04
    (Deferred, “Display pages”), and Stage 10 is that stage. Active.

Deferred, each until its own decision:

- Display pages for the Prophets, Avi's raw-text pages, and adding Hosea, Joel and Amos to the
  base-chapter index: questions 2, 3 and 4 of the draft reply. Each needs Avi's answer and then a
  revision of this plan. Avi answered on 2026-11-03:
  - **Display pages** come later, as a further step that needs explanation; he and Rabbi Kokhav
    have agreed on how they should look in the Prophets and the Writings.
  - **Display pages, in Avi's later email of 2026-11-03,** which Ben relayed with Stage 8's word:
    the books other than Joshua are "short enough" to be "displayed on a single page, one page per
    book, in a similar fashion to the five megillot", and "For Joshua, I'll need to create an
    example." Ben decided to offer Avi the bot for the five pages (decisions ledger entry 13);
    Joshua's waits on Avi's example. The Stage 8 session's read-only survey of the megillot's
    display pages, and of what the five books would need, is
    `C:/Users/BenDe/AppData/Local/Claude-Data/claude_pzs8sxrjxfjjc/side-session-notes/local_a80ded65-f78e-4280-8493-9dab3b8c5686/miqra-mevoar-display-survey-2026-11-03.md`.
  - **Display pages, in Avi's answer that Ben relayed on 2026-11-04.** Ben pasted the email,
    undated, into the commander session at 09:21 New York time. Avi had set up the main page's
    links "to the actual display pages for public use". He asked the bot to "use the currently red
    links for the Twelve Prophets to create full-book-pages, one per book, in a similar format to
    what already exists for the Five Megillot", the titles being "simply" the books' names. For
    Joshua he described a division into two parts, each named by its chapters: Part One, chapters
    1-12, and Part Two, chapters 13-24. The session that read the answer took it as his acceptance
    of the bot, for Joshua's two parts as well as the Twelve. It read the live pages on 2026-11-04
    at about 09:30 New York time, saving nothing:
    - **The main page** `מקרא מבואר` is at revision 3101310. Four revisions by Dovi, 3101307 to
      3101310, made between 19:22 and 19:32 New York time on 2026-11-03, replaced the Prophets
      section's pointer to the raw text with a numbered list of the Prophets' books, and made the
      Writings' list a numbered list of all its books. Under Joshua it links
      `מקרא מבואר/תצוגה/ספר יהושע א`, named “ספר יהושע, חלק ראשון: כיבוש הארץ (פרקים א-יב)”, and
      `מקרא מבואר/תצוגה/ספר יהושע ב`, named “ספר יהושע, חלק שני: חלוקת הארץ (פרקים יג-כד)”. Under
      the Twelve it links eleven books by their bare names under `מקרא מבואר/תצוגה/`, Obadiah's
      spelled `עבדיה`, without the vav of MAM's name. All 13 links are red, and the other Prophets'
      books have no links yet.
    - **Amos is missing from that list,** though Avi's email gives `עמוס` as an example of
      the titles. Stage 10 creates Amos's page all the same, and the reply drafted for Ben asks
      Avi to add the link.
    - **Seven of the Twelve have no base chapters:** Micah, Nahum, Habakkuk, Zephaniah, Haggai,
      Zechariah and Malachi, whose Word files have not reached Avi's folder. Of the index's links,
      282 lead to existing base chapters: all of the Torah, the five megillot, Joshua, Hosea,
      Joel, Amos, Obadiah and Jonah.
    - **No display page is new:** `מקרא מבואר/תצוגה/` still has 78 pages, none of them a linked
      title.
    - Stage 10 creates the seven pages whose base chapters exist. The other seven wait for their
      base chapters, as the reply drafted for Ben on 2026-11-04 proposes to Avi:
      `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar/email-to-avi-2026-11-04-display-pages.md`.
      Ben sent its v2 (execution ledger, “The reply to Avi”).
  - **The index after the bot.** Avi edited the index eleven times after the bot's revision
    3101215, between 19:00 and 19:52 New York time on 2026-11-03, ending with revision 3101312.
    He removed the information section's list of ready base chapters and its pointer to the raw
    text, which settles the question that Ben's email of 2026-11-03 asked about that list, and he
    gave each part of Samuel, Kings, the Twelve, Ezra–Nehemiah and Chronicles a line of its own.
    The closed parser of `miqra-mevoar-index` reads revision 3101215 but stops at the first of
    those lines, as an offline run showed on 2026-11-04, so that mode cannot edit the index as it
    now is; a bot edit of the index would need a new stage and Ben's word.
  - **The raw-text pages** are to go once the work is done; he plans to delete them himself, so
    nothing here touches them. His answer of 2026-11-04 does not mention them.
  - **The base-chapter index** should be finished first, listing every chapter of the Bible, most
    of them as red links. He wrote 972 chapters; MAM-simple has 929, in 39 books, and Ben
    decided on 2026-11-03: "Let's assume he meant 929". Ben chose the bot (entry 10), and Stage 9
    plans the work.
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
- **Stage 7, 2026-11-03:** Ben's word, answering "On your word here, I'll ask the commander for
  the clone, run a fresh dry run, then the save, and write Stage 7's history entry.": "yes go
  ahead and do that". The commander returned the clone for it. A read-only listing of the folder
  showed `yehoshua.docx` unchanged, and a download of it equalled, by SHA-256, the file the
  tracked JSON came from. The folder also held `.~lock.yehoshua.docx#`, a LibreOffice lock file,
  which stopped `fetch`. This stage's commit makes `fetch` skip and name such lock files. A full
  fetch then found all seven files unchanged, and `check` passed. The dry run at 10:06 New York
  time gave Joshua 1 unchanged and Joshua 2 a create. The saving run at 10:08, with Avi's summary
  פרק חדש במקרא מבואר, created Joshua 2 as revision 3101196. It read the revision back equal to
  the generated text and exited zero, and the edit carries the bot flag. A dry rerun found both
  pages unchanged. `py/ws/ws_bot_edit_history.md` has the entry, with the run directories. Stage 8
  waits on Avi's look at Joshua 2 and on Ben's word.
- **Stage 9's word, 2026-11-03:** Ben, answering "Stage 9, the index of all 929 chapters: only
  your word to execute it. I'll then send the commander a standalone prompt for a fresh session.
  The edit summary gets your approval when its save comes.": "Please do this, and then compose
  an email to Avi describing what we've done and asking for his approval and anything else that
  seems like it should be part of the process he outlines." The commander started a fresh Claude
  (Opus 5.5) session for the stage, with a brief whose Part A is the Phase 2 session's prompt,
  frozen at SHA-256 `561854C99BA606EF96475AA00D922A702549606DB024CFA8FA2A9221D8BD415B`.
- **Stage 9's checkout:** `C:/Users/BenDe/GitRepos2/MAM-basics`, assigned by the commander.
  Verified 2026-11-03 at about 11:14 New York time: on `main`, clean, at `75bb5ef1`, then
  fast-forwarded to origin's `901574086130b4b961b9e1889171f72cfe5f207a`, the varika run's push,
  of which `75bb5ef1` is an ancestor.
- **Stage 9's code:** `py/miqra_mevoar/index_page.py`, the mode `py/main_ws_bot.py
  miqra-mevoar-index` in `py/subcommands/ws_bot_miqra_mevoar_index.py`, and
  `py/tests/test_miqra_mevoar_index.py`. Beyond the design:
  - `wikitext.page_title` takes a book's `BS_` pair, so that it titles any of MAM's chapters, and
    `wikitext.INDEX_TITLE` and `wikitext.CATEGORY` are new public names. `pages` then wrote all 56
    pages and `titles.tsv` equal byte for byte to Stage 3's output.
  - `mam_simple.py` reads MAM-simple's book level by a closed dispatch. The files of Samuel,
    Ezra–Nehemiah and Chronicles have a petuha break between their two books, on which the old
    reading would have failed. `spi-samekh3`, a setuma break found in eight books outside the
    six, joins the breaks.
  - The test's oracle is independent of the index's table: it orders the books by
    `bib_locales.ALL_BK39_IDS`, finds each in MAM-simple by its OSIS abbreviation in
    `osis_book_abbrevs`, and takes each chapter from its chapter element's osisID.
  - The parser requires each line of links to read back as itself, and the index to begin with
    its information section. A run also writes its diff as `index.diff` and its facts as
    `misc/index-run.json`.
  - Offline, on Phase 1's capture of revision 3084327, the generator kept all 13 old sections and
    wrote 24, with 929 links where there were 267. The framing and the category line kept their
    bytes, and the page grew from 22,242 bytes to 71,895. The unified diff adds 34 lines and
    removes one, the Twelve's line, whose two old runs reappear unchanged in the new one. A
    second pass over the new text changes nothing.
  - Checks: `git diff --check`, Black, and the targeted tests with the tree-wide lints (91
    passed); the full suite (1,426 passed, 5 skipped, none of them the new test's). The mega was
    skipped, as in Stage 4.
- **Stage 9's dry run, 2026-11-03 at 11:39 New York time,** from the tree that this stage's
  commit records, after the commander confirmed that no other BDencklaBot run was in progress.
  `miqra-mevoar --no-save` for Joshua 1 and 2 found both pages unchanged and exited zero (run
  `.novc/mam-ws-bot-miqra-mevoar-runs/20261103-113923-412155-0500/`), so generalizing the title
  function changed no title. `miqra-mevoar-index --no-save` read the index's latest revision,
  3084327, Dovi's of 2026-09-23 at 07:21:02 UTC, on page id 375628; its bytes equal Phase 1's
  capture, and the new text equals the offline result. Every old section reappears, the Twelve's
  two old runs within its new section. The run exited non-zero, as a dry run before a save does
  (run `.novc/mam-ws-bot-miqra-mevoar-index-runs/20261103-113936-837559-0500/`). The save waits
  on Ben's word for that run, with `--base-revid 3084327` and its summary (decisions ledger
  entry 12).
- **Stage 9's save, 2026-11-03:** Ben's word, answering "Save the index with --base-revid 3084327
  and the proposed Hebrew summary?": "Yes, save it". The commander confirmed that no other
  BDencklaBot run was in progress and returned the clone, which was fast-forwarded from
  `96d13d1c` to origin's `5eab0965`, the varika refresh's six commits, which touch neither
  MAM-simple nor this plan's code. A fresh dry run at 12:52 New York time gave the reviewed dry
  run's old text, new text and diff byte for byte. The saving run at 12:53, with the summary
  השלמת רשימת פרקי הבסיס לכל ספרי המקרא, saved revision 3101215 over 3084327, read it back equal
  to the generated text, and exited zero. A read after the run found 3101215 the latest
  revision, BDencklaBot's, not minor, with the summary and the bot flag, and found that
  regenerating from it changes nothing. `py/ws/ws_bot_edit_history.md` has the entry, with the
  run directories.
- **Stage 8's word, 2026-11-03:** Ben relayed Avi's answer to the commander session at 14:52 New
  York time, under his own first line: "Launch a session that will act upon the following email
  from Avi (notably, I think this unblocks some Miqra Mevoar work):". Avi wrote that Joshua 2
  "looks fine" and "let's finish the available chapters" of Miqra Mevoar as base chapters; the
  commander read that as Avi's confirmation that the Word files in the folder are final. The
  commander started a fresh Claude (Opus 5.5) session for the stage, with a brief whose Part A is
  the Phase 2 session's prompt, frozen at SHA-256
  `25511F3E24190CED119B7A61C9D68FB82DCD0EE0D105A236CCE9F828809FEF24`.
- **Stage 8's checkout:** `C:/Users/BenDe/GitRepos2/MAM-basics`, assigned by the commander.
  Verified 2026-11-03, before a fetch at 14:56 New York time: on `main`, clean, at origin's
  `23b7e24f00ce78ab45c475df94f9f57cd8dcaead`, of which `75bb5ef1` is an ancestor.
- **Stage 8, 2026-11-03:** the fetch's manifest was byte-identical to Stage 7's, so no Word file
  had changed, and `check` passed. The commander confirmed before the dry run, and again before
  the save, that no other BDencklaBot run was in progress. The dry run at 14:57 New York time gave
  54 creates and Joshua 1 and 2 unchanged, with no refusal, and its 56 pages equal the prototype's
  byte for byte. The saving run, from 15:00 to 15:09 with Avi's summary, created the 54 pages as
  revisions 3101229 to 3101282, read each back equal to the generated text, and exited zero; its
  pages equal the dry run's. Every creation carries the bot flag. A dry rerun found all 56 pages
  unchanged and exited zero. `py/ws/ws_bot_edit_history.md` has the entry, with the run
  directories. Stage 8 sets this plan's State to executed once Stage 9 is done, as it is, but the
  State stays live: the commander's brief adds a stage to this plan for the display pages if Ben
  gives them to the bot, and an executed plan is not reopened.
- **Avi's answer on the display pages, 2026-11-04:** Ben relayed it to the commander session at
  09:21 New York time, asking for "a session to respond to this email from Avi". The commander
  started a fresh Claude (Opus 5.5) session, with a brief whose Part A is the Stage 8 session's
  prompt, frozen at SHA-256 `4199F2106DC56CFFA045AFFB49BDD088B766D0687183CC536BD96A6B3AEC4977`.
  Its checkout, `C:/Users/BenDe/GitRepos2/MAM-basics`, was verified at about 09:25 New York time:
  on `main`, clean, at `dc41e480`, then fast-forwarded to origin's
  `76583ffa727636a20f4c6496370aa94038fb6535`, whose four new commits add MAM-morphhb and touch
  nothing of this plan's. The session read the live pages, saving nothing (Deferred, “Display
  pages”), wrote Stage 10 and drafted Ben's reply to Avi. It ran no BDencklaBot command.
- **Stage 10's word, 2026-11-04:** Ben, answering "Do you give your word to execute Stage 10 as
  written, in a fresh session?" in the session that wrote the stage: "Yes, execute it", at 09:59
  New York time. He then answered "Yes, start it" in the commander session, to its question about
  starting the executing session. The commander started a fresh Claude (Opus 5.5) session for the
  stage, with a brief whose Part A is the writing session's prompt, frozen at SHA-256
  `F441BB0AE0A5430C99F992DB4AA360BBFFE89211A99BF3CA8CB46FC6D8415712`.
- **Stage 10's checkout:** `C:/Users/BenDe/GitRepos2/MAM-basics`, assigned by the commander.
  Verified 2026-11-04, before the stage's first edit: on `main`, clean, at origin's
  `210affe3ac2931473bead0de839be0de08309e3d`, the push of this stage, of which `f0d2f2e6`, the
  commit that added it, is an ancestor.
- **Stage 10's code:** `py/miqra_mevoar/display_page.py`; `verse_breaks` in
  `py/miqra_mevoar/mam_simple.py`; the mode `py/main_ws_bot.py miqra-mevoar-display`, in
  `py/subcommands/ws_bot_miqra_mevoar_display.py`; and `py/tests/test_miqra_mevoar_display.py`.
  Beyond the design:
  - The main page's latest revision, read just before the code was written, was still 3101310,
    and its bytes equal the writing session's capture. The table's names and the line shapes'
    templates and parameters were copied from that revision and from the megillot's pages by
    script, each checked against a second source, such as a template's own parameter names.
  - The test's oracle for the breaks is MAM-simple's `starts-with-sampe` field, its own record of
    the break before a verse, so it does not share the generator's reading of the break elements.
    Across all of MAM-simple, every break element between two books, chapters or verses has that
    field on the verse after it and `ends-with-sampe` on the verse before it, except three
    elements nested in an `sdt-target`, before Exodus 34:1 and Leviticus 7:22 and 7:28, outside
    these books, whose neighbours have neither field; and no break element is a verse's first or
    last child.
  - The closed parser, `display_page.read_page`, lives in the generator's module, as the index's
    does, and requires a page to read back as itself. The mode also counts each page's lines with
    it in `misc/outcomes.json`, in the columns of the table above.
  - The parse check of `--no-save` asks for the transcluded pages as well as the links, and fails
    on a missing one of either.
  - The mode generates every selected page before it reads any live one, so that a page that the
    generator refuses stops the run before anything is saved. It saves with the bot flag given
    explicitly.
  - Offline, the seven pages have exactly the table's counts, and Joshua's second part opens with
    the one break line that has both parameters. The same rendering, given Ruth, Song of Songs and
    Esther from MAM-simple with no headings, gives Avi's live pages of 2026-11-04 for Ruth and Song
    of Songs byte for byte, and Esther's apart from its note at the top and its notes section.
  - An offline exercise with stand-ins for pywikibot, which no tracked test keeps, ran the mode's
    dry run, its save and its refusal, and checked that a save is not minor, has cosmetic changes
    off and the bot flag, and is `createonly`.
  - Checks: `git diff --check`, Black, and the verification command above (93 passed). The full
    suite and the mega were skipped, as this stage expects. Pushed as `48d811f1`; origin's `main`
    had not moved.
- **Stage 10's dry run, 2026-11-04 at 11:20 New York time,** from `48d811f1`, after the commander
  confirmed that no other BDencklaBot run was in progress. The main page's latest revision was
  still 3101310, before the run and again after it, so no title had changed and Amos still had no
  link. The precondition, `miqra-mevoar --no-save` over the six books at 11:19, found all 56 base
  chapters unchanged and exited zero (run
  `.novc/mam-ws-bot-miqra-mevoar-runs/20261104-111943-509759-0500/`). `miqra-mevoar-display
  --no-save` gave seven creates and exited non-zero, as a dry run before a save does. Each page has
  exactly the table's counts and equals a fresh generation byte for byte, and Joshua's second part
  opens with the one break line that carries both the petuha before 13:1 and the heading of 13:1.
  The parse check found no missing link or transcluded page on any page. A read-only parse after
  the run, without the bot's login, found that the check had pages to check: 52 links and 21
  transcluded pages on Jonah's page and 365 and 44 on Joshua's second part, all of them existing.
  Run `.novc/mam-ws-bot-miqra-mevoar-display-runs/20261104-112021-866392-0500/`. The save waits on
  Ben's word for that run, with its summary.
- **Stage 10's save, 2026-11-04:** Ben's word, answering "Save the seven display pages with the
  proposed Hebrew summary?": "Yes, save them". The commander confirmed that no other BDencklaBot
  run was in progress and returned the clone, still at `b391b856`. The precondition again found
  all 56 base chapters unchanged (run
  `.novc/mam-ws-bot-miqra-mevoar-runs/20261104-112830-348954-0500/`). The saving run, at 11:29 and
  11:30 New York time with the summary דף תצוגה חדש במקרא מבואר, "a new display page in Miqra Mevoar", created
  the seven pages as revisions 3101357 to 3101363, read each back equal to the generated text, and
  exited zero; its pages equal the dry run's. A read after the run found each page with one
  revision, BDencklaBot's, not minor, with that summary, and each creation and its category entry
  with the bot flag. A dry rerun found all seven pages unchanged, with no missing link or
  transcluded page, and exited zero. `py/ws/ws_bot_edit_history.md` has the entry, with the run
  directories. The State stays live, as Stage 10 provides while display work that Ben has given
  to the bot remains: the pages of Micah to Malachi, which Stage 10 leaves for after their base
  chapters.
- **Codex's review of Stage 10, 2026-11-04:** Codex found a defect in the bot's records, and its
  reads of the seven saved revisions were refused with a 403 by its cloud tunnel. Claude answered
  the review in a session that the commander started, and Ben relayed the answer.
  - **The defect.** Each bot mode of this plan read its saved revisions back before it wrote
    `misc/saved-pages.json`, and caught only `ChapterResponseError`. So when a read-back raised, as
    it does on a network failure, no record of the revisions already saved was written. Stage 10's
    run did not take that path: its record holds all seven pages, each verified. Codex's repair,
    PR 368, began as a draft for the display mode. Claude reproduced the defect and found the same
    order in the base-chapter and index modes. Codex extended the repair to all three modes, with
    the ws_bot test `py/tests/test_miqra_mevoar_save_receipts.py`, and merged it as `f6585c7f`, on
    Ben's authorization, as the merge commit records. Each mode now writes its record before the
    read-back and again after it. After the merge, Claude ran that test from a scratch copy: it
    fails its four cases of a raising read-back against the modes as they were before PR 368, and
    passes all eight of its cases against the merged ones.
  - **A narrower window remains,** which both agents left out of scope: after a creation,
    pywikibot 11.7.0's `BasePage._save` reads the page's info over the network, so a failure there
    ends the save with an error for a page that exists, and leaves no record. A rerun would find
    such a page unchanged.
  - **The seven revisions.** On Ben's word, Claude read revisions 3101357 to 3101363 anonymously
    at 14:12 New York time and kept each response byte for byte, with SHA-256 hashes, in
    `.novc/codex-stage-10-review-2026-11-04/read-20261104-141253-0500/` of
    `C:/Users/BenDe/GitRepos2/MAM-basics`; that folder's `README.md` says how to check them. Each
    revision's content equals the generated page of all three Stage 10 runs byte for byte, and
    MediaWiki's SHA-1 of it matches. Each revision is BDencklaBot's, is not minor, is its page's
    first revision, and carries Stage 10's summary.
- **The reply to Avi, 2026-11-04:** Ben, at about 17:20 New York time: "I've sent
  email-to-avi-2026-11-04-display-pages-v2.html to Avi via email." That is v2 of the reply drafted
  with Stage 10, made by script in the session that answered Codex's review, from the draft in
  `.novc/miqra-mevoar/`, which stays unchanged. Its source is
  `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/codex-stage-10-review-2026-11-04/email-to-avi-2026-11-04-display-pages-v2.md`.
  - **What v2 adds to the draft:** it asks for Amos's link only if the list still skips Amos.
    It also adds a paragraph, “Your look at the pages”, which asks Avi to look the seven pages
    over before the bot makes the later books' pages in the same form. That paragraph tells him
    that each heading's words are transcluded from its base chapter, but that each heading line's
    place was fixed when the bot made the page. So a heading that Rabbi Kokhav adds at another
    verse, or moves, does not appear on the display page until someone adds its line.
  - **Its three questions to Avi:** Amos's link; the display pages of Micah to Malachi now, or
    after their base chapters, as the reply proposes; and any change to the pages' form. The next
    display work waits on his answer.

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
State set to executed, if Stage 9 is done too; commit and push.

## Stage 9. The base-chapter index, on Ben's word

The executing session wrote this stage on 2026-11-03. Ben had decided "I think this is a great
task for a bot" (ledger entry 10), and asked for the stage with "Yes, write it", answering "Shall
I write the bot's index stage into the plan?". It may run before or after Stage 8. By Ben's rule a
fresh session executes it, not the session that wrote it, and it stays planning only until he
gives his word to execute it. The session that hears his word then sends the commander session a
standalone prompt for that fresh session.

**What it does.** BDencklaBot completes the base-chapter index, the page `מקרא מבואר/פרקי בסיס`, so
that it links every one of MAM's 929 chapters, as Avi asked in his email of 2026-11-03 (ledger
entry 4). Most of the links stay red until their pages exist. The bot rewrites only the page's
book sections; the framing above them and the category line below them keep their bytes.

**The page as read on 2026-11-03.** Page id 375628. Its latest revision, 3084327, is Dovi's of
2026-09-23 at 07:21 UTC: 22,242 bytes, equal to Phase 1's capture
`C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar-2026-11-02/wikisource-2026-11-02/מקרא_מבואר_פרקי_בסיס.wiki`.
Its eight latest revisions are seven by Dovi, of 2026-09-06 to 2026-09-23, and one by
ShalomOrobot, of 2022. Its layout:

- **The framing:** an information section, whose heading begins `==מידע על פרקי הבסיס`; a list of
  the books already encoded; and numbered working steps for editors. Avi keeps that list, so the
  bot leaves the framing alone.
- **One section per book:** a heading line, `==<heading>==`; one line
  `*{{ג|'''{{קו תחתי|פרקים:}} <links>'''}}`; and a blank line. Each link is
  `[[מקרא מבואר/פרקי בסיס/ספר <MAM's bk39 name>/<numeral>|<numeral>]]`, and the links are joined
  by ` · `.
- **The Twelve** share one section, headed `==תרי עשר==`. Its line gives each prophet as
  `<label>: <links>;`, and the runs are joined by a space.
- **The last line** is `[[קטגוריה:מקרא מבואר]]`.
- **The sections present** are Genesis to Deuteronomy, Joshua, the Twelve (Obadiah and Jonah
  only), Song of Songs, Ruth, Lamentations, Ecclesiastes, Esther and Daniel. They follow the order
  of printed Bibles, which is also the order of the `BS_` pairs in `py/mb_cmn/mam_bknas.py`.
- **Display names:** the headings are MAM's 24-book names, the first parts of `mam_bknas`'s `BS_`
  pairs, with two exceptions. The Twelve's heading lacks "ספר", and Ecclesiastes' heading,
  `מגילת קֹהלת`, has a holam. The Twelve's labels are MAM's sub-book names, except Obadiah's,
  `עֹבדיה`, which also has a holam. The link targets use MAM's bk39 names (`he_bk39_name`), so
  Obadiah's target has a vav.

**The design.** These are the executing session's proposals. Ben's word to execute this stage
approves them, and he may change any of them first.

1. **Generator,** `py/miqra_mevoar/index_page.py`. Its book table lists all 39 books in
   `mam_bknas`'s order, each with its `BS_` pair, OSIS id, MAM-simple file, and display heading
   or label. The three exceptions above are explicit entries, their Hebrew copied from the live
   page by script, never typed. Chapters come from MAM-simple through `mam_simple.py`'s closed
   dispatch. A MAM-simple book missing from the table raises, and so does a table book missing
   from MAM-simple. Link targets come from the converter's own title function, generalized from
   the six-book table to every book; the six books' titles must not change.
2. **The one new layout, as Ben chose it (ledger entry 11):** a book of two parts other than the
   Twelve (Samuel, Kings, Ezra and Nehemiah, and Chronicles) gets one section under its 24-book
   heading. That section has a labelled run for each part, as the Twelve has, and the labels are
   the bk39 names, such as `שמואל א`. Ben chose this over a section for each part.
3. **The page's text:** the live revision's text up to the heading of its first book section,
   unchanged; then the generated sections; then the live revision's text from its category line
   on, unchanged. It is generated in NFC with no final newline, as the base chapters are. A
   closed parser of the two line shapes above reads the old page's sections and the new. Each old
   section must reappear unchanged, except the Twelve's, whose old runs must reappear unchanged
   within it. Any other line in the old sections stops the run.
4. **Bot mode,** `py/main_ws_bot.py miqra-mevoar-index`, in
   `py/subcommands/ws_bot_miqra_mevoar_index.py`, with the chapter mode's login check:
   - `--no-save` reads the live page and writes `old.wiki`, `new.wiki` and a unified diff into
     `.novc/mam-ws-bot-miqra-mevoar-index-runs/<timestamp>/`. It prints the base revision id and
     the number of links, 929, and exits non-zero if the page would change.
   - A saving run requires `--base-revid`, the revision whose diff Ben reviewed, and `--summary`.
     It refuses unless that revision is still the page's latest. It then regenerates the text and
     saves it with `nocreate`, `baserevid` and that revision's `basetimestamp`. It reads the
     saved revision back through `ws_revision_api.ChapterClient`, requires its bytes to equal the
     generated text, and writes `misc/saved-pages.json`.
   - The mode is declared in `NOT_IN_MEGA`, as `miqra-mevoar` is, and documented in
     `py/main_ws_bot.py`'s docstring and in `py/ws/pywikibot-setup.md`.
5. **Test,** `py/tests/test_miqra_mevoar_index.py`, differential. The generated sections, read
   back by the closed parser, must link exactly MAM-simple's 929 chapters, in order, each to the
   title that the converter's function gives.

**Verification,** as in Stages 4 and 5: `git diff --check`; Black; the targeted tests
(`test_miqra_mevoar_index.py`, `test_miqra_mevoar_versification.py`,
`test_miqra_mevoar_bot_revision_guard.py`, `test_mega_coverage.py`,
`test_entry_point_subcommands.py`, and the tree-wide lints `source_hygiene_test.py`,
`test_prose_conventions.py`, `test_transliterations.py`, `test_explicit_time_zones.py`,
`test_stderr_error_handler.py` and `test_h_dot_below_nfc.py`); then the full suite. The mega is
skipped, as in Stage 4. Finally, a `miqra-mevoar --no-save` run for Joshua 1 and 2 must find both
pages unchanged, which shows that generalizing the title function changed no title.

**The dry run and the save.** Run `--no-save` and read its diff. Report to Ben the base revision,
the diff's size, and that every section of the old page reappears in the new; then stop. The save
needs Ben's explicit word for that run, with its `--base-revid` and its summary. Avi's summary for
new chapters does not fit an edit of the index, so ask Ben for one, offering a Hebrew one in Avi's
manner. After the save, add an entry to `py/ws/ws_bot_edit_history.md` and record the stage in the
execution ledger. Then commit, fetch, merge `origin/main` if it moved, and push.

**Checkout and coordination,** as for the plan's other stages: a full MAM-basics clone that the
commander session assigns, verified clean on `main`, and its own `.venv/Scripts/python.exe`, run
from its root. Every Git call gets `-c safe.directory=<clone>`. Ask the commander before any
Git-impacting change, and release the clone while waiting on Ben. The stage needs no untracked
input, since it reads the live page itself.

## Stage 10. The display pages, on Ben's word

The session that read Avi's answer wrote this stage on 2026-11-04 (Deferred, “Display pages”),
following Ben's decision to offer Avi the bot (ledger entry 13). By Ben's rule a fresh session
executes it, not the session that wrote it, and it stays planning only until he gives his word to
execute it; each saving run needs his word too. The design is that session's proposal: Ben's word
to execute approves it, and he may change any of it first, the scope included.

**What it does.** BDencklaBot creates seven of the display pages that Avi's main page links, each
setting MAM's verses beside Rabbi Kokhav's paraphrase in the form of Avi's megillot pages: the two
parts of Joshua and the five books of the Twelve whose base chapters exist. It only creates pages;
it never edits one.

**The pages,** keyed as the bot mode names them, with the titles that the main page `מקרא מבואר`
links from its section `==ספרי הנביאים==` in revision 3101310, copied from that revision by script:

1. `yehoshua-1`: `מקרא מבואר/תצוגה/ספר יהושע א`, Joshua 1 to 12.
2. `yehoshua-2`: `מקרא מבואר/תצוגה/ספר יהושע ב`, Joshua 13 to 24.
3. `hoshea`: `מקרא מבואר/תצוגה/הושע`, all of Hosea.
4. `yoel`: `מקרא מבואר/תצוגה/יואל`, all of Joel.
5. `amos`: `מקרא מבואר/תצוגה/עמוס`, all of Amos.
6. `ovadya`: `מקרא מבואר/תצוגה/עבדיה`, all of Obadiah.
7. `yona`: `מקרא מבואר/תצוגה/יונה`, all of Jonah.

- **Amos** has no link on the main page, but Avi's email gives `עמוס` as an example of the
  titles, so its title is built as the others are, from the prefix and MAM's name of the book.
  Ben's reply asks Avi to add the link.
- **Obadiah's** title has no vav, like Avi's link and the Word file's title row. The template's
  book name is MAM's, `עובדיה`, as in the base chapters' titles and MAM's chapter page.
- **Left out:** Micah, Nahum, Habakkuk, Zephaniah, Haggai, Zechariah and Malachi, which the main
  page also links, have no base chapters. A display page for one of them now would show, beside
  every verse, a red link titled with its missing base chapter, as a read-only preview of Micah
  1:1 showed on 2026-11-04. It would also lack Rabbi Kokhav's headings, whose places come from
  the Word files. Each is made after its base chapters, under “Later Word files”, unless Ben
  decides otherwise on Avi's answer to the reply.

**The page text.** Three line shapes, as on the megillot's pages and the Torah's parasha pages,
and no others:

1. **A verse:** `{{מקרא מבואר|<book>|<chapter>|<verse>}}`, with the book as `mam_bknas.he_bk39_name`
   names it and the chapter and verse as Hebrew numerals. The template sets MAM's verse beside the
   base chapter's section of the same name and shows the chapter numeral at a chapter's first verse.
   Every page here begins at a chapter's first verse, so no line needs the parameter `פרק=` with
   which a parasha page numbers a chapter that it begins elsewhere; the generator raises if a page
   would begin at another verse.
2. **A break or a heading,** on a line before its verse:
   `{{פרשה במקרא מבואר|פרשה=<פ or ס>|כותרת={{#קטע:מקרא מבואר/פרקי בסיס/ספר <book>/<chapter>|כותרת <verse>}}}}`.
   `פרשה=` is given only where MAM-simple has a petuha or a setuma between the verse and
   the one before it in the same book, and `כותרת=` only where the tracked JSON gives the
   verse a heading: both, in that order, where both apply, as on the Lamentations page, and no
   line where neither does. The heading's text is not copied; the line transcludes it from the
   base chapter.
3. **The end:** a blank line, then `[[קטגוריה:מקרא מבואר|<name>]]`, whose sort key is the page's own
   name after `מקרא מבואר/תצוגה/`, as each megillah's page has its own.

Nothing else is on a page: no note at the top and no notes section, since Avi asked for none. The
text is NFC, with no final newline, as the base chapters' is.

**Choices,** each a proposal that Ben's word approves:

1. **The breaks follow MAM exactly,** as on the Song of Songs, Ruth and Esther pages. Avi asked
   for "a similar format" to the megillot's; the Lamentations page's note and the two setumot
   missing from the Ecclesiastes page are departures, not the format.
2. **A break before a page's first verse is shown,** as on Avi's parasha pages: those of Noah,
   Lekh Lekha and Va'era each open with a break line that has both parameters. Here only Joshua's
   second part has one: MAM's petuha before 13:1, on one line with the heading of 13:1.
3. **A break inside a verse gets no line,** since MAM's verse shows it: a read-only preview of
   Hosea 1:2 on 2026-11-04 showed the transcluded verse breaking at its petuha. Joshua 4:1 has
   the only other such break in these books.
4. **Sort keys** are the pages' own names, as the megillot's are.

**Counts,** measured on 2026-11-04 from MAM-simple and `in/miqra-mevoar/` at `76583ffa`; the dry
run's pages must have them:

| Page | Verse lines | Petuhot, setumot | Headings | Break lines: break only, heading only, both |
|---|---|---|---|---|
| Joshua 1 to 12 | 303 | 22, 18 | 18 | 24, 2, 16 |
| Joshua 13 to 24 | 353 | 33, 31 | 25 | 39, 0, 25 |
| Hosea | 197 | 10, 6 | 13 | 5, 2, 11 |
| Joel | 73 | 3, 3 | 3 | 4, 1, 2 |
| Amos | 146 | 22, 6 | 21 | 8, 1, 20 |
| Obadiah | 21 | 0, 0 | 1 | 0, 1, 0 |
| Jonah | 48 | 2, 1 | 4 | 1, 2, 2 |

In all: 1,141 verse lines, 157 breaks, 85 headings and 166 break lines.

**The design.**

1. **Generator,** `py/miqra_mevoar/display_page.py`. Its table lists the seven pages, each with its
   key, its name after the prefix, its book from `books.BOOKS` and its chapters. The names are
   copied by script from revision 3101310, never typed; Amos's is MAM's name. Verses and breaks
   come from MAM-simple through `mam_simple.py`, extended by a closed dispatch for breaks. A break
   element between two chapters, between two verses or as a verse's last child stands before the
   next verse. A break among a verse's children, with a child before it and a child after it, is
   inside the verse and gets no line. A break anywhere else, such as a verse's first child, one
   nested deeper or one after a book's last verse, raises. Headings come from the tracked JSON
   through `tracked.py`. Each transclusion's target is the title that `wikitext.page_title`
   gives, and the heading section's name is the base chapters' own, made public in `wikitext.py`.
2. **Bot mode,** `py/main_ws_bot.py miqra-mevoar-display`, in
   `py/subcommands/ws_bot_miqra_mevoar_display.py`, modelled on the chapter mode in
   `ws_bot_miqra_mevoar.py`, with its login check:
   - Its arguments are `--page <key>`, repeatable, all seven when none is given; `--no-save`;
     `--summary`, required unless `--no-save`; and pywikibot's `-dir:`.
   - It gives each page one of three outcomes. **Create:** the page does not exist; it is saved
     with `createonly`, not minor, with cosmetic changes off and the bot flag, as the chapter mode
     saves. **Unchanged:** the live text equals the generated text. **Refuse:** the page exists
     with another text; nothing is saved for it, the editors of its revisions are listed, and the
     run exits non-zero. There is no update.
   - Every run writes its pages and `misc/outcomes.json` under
     `.novc/mam-ws-bot-miqra-mevoar-display-runs/<timestamp>/`. `--no-save` also renders each
     generated page through the API's `parse` action, which saves nothing, and requires that no
     link on it be red, as a misspelled book name or a missing base chapter would make one. It
     saves nothing and exits non-zero if any page would be created.
   - A saving run reads each saved revision back through `ws_revision_api.ChapterClient`,
     requires its bytes to equal the generated text, writes `misc/saved-pages.json`, and exits
     non-zero on any mismatch.
   - The mode is declared in `NOT_IN_MEGA`, as `miqra-mevoar` is, and documented in
     `py/main_ws_bot.py`'s docstring and in `py/ws/pywikibot-setup.md`.
3. **Test,** `py/tests/test_miqra_mevoar_display.py`, differential. A closed parser of the three
   line shapes reads each generated page back, raising on any other line. A page's verse lines
   must equal MAM-simple's verses of its chapters, in order, as their osisIDs give them; its
   petuhot and setumot must equal those that the test's own walk of MAM-simple finds between
   verses; the places of its headings must equal the tracked JSON's; each transclusion's target
   must be the base chapter's title; and Joshua's two pages together must cover its 24 chapters
   once each. The test fails, never skips, when an input is missing.

**Preconditions,** before the dry run and again before the save:

- The places of the headings come from the tracked JSON, which matches the base chapters only
  while nobody has revised them on Wikisource. A `miqra-mevoar --no-save` run over the six books
  must find all 56 base chapters unchanged. If one differs, stop and report it to Ben.
- The commander confirms that no other BDencklaBot run is in progress, as for Stages 8 and 9.

**Verification,** focused, under `doc/review-trial.md`: `git diff --check`; Black on the changed
Python files; and the targeted tests, with the tree-wide lints that scan new files:

```powershell
./.venv/Scripts/python.exe py/main_test.py py/tests/test_miqra_mevoar_display.py py/tests/test_miqra_mevoar_versification.py py/tests/test_miqra_mevoar_index.py py/tests/test_miqra_mevoar_bot_revision_guard.py py/tests/test_mega_coverage.py py/tests/test_entry_point_subcommands.py py/tests/source_hygiene_test.py py/tests/test_prose_conventions.py py/tests/test_transliterations.py py/tests/test_explicit_time_zones.py py/tests/test_stderr_error_handler.py py/tests/test_h_dot_below_nfc.py py/tests/test_prose_mark_order.py py/tests/test_tracked_filenames.py
```

The full suite and the mega are the nightly default, and the mega runs none of this code; the
last pushed commit's message says what was skipped and why. Expected unchanged: every product
directory that `py/product_scopes.py` declares, `in/miqra-mevoar/`, `in/mam-ws/` and
`in/mam-ws-bot-edits/`.

**The dry run and the save.** Run `--no-save` for all seven pages, compare each page with the
counts above, and read its first and last lines. Report to Ben the seven creates, the counts, the
parse check and the run directory; then stop. The save needs Ben's explicit word for that run,
with its summary. Avi's summary for the base chapters names a chapter, so ask Ben for one,
offering a Hebrew one in Avi's manner. After the save, a dry rerun must find all seven pages
unchanged. Then add an entry to `py/ws/ws_bot_edit_history.md`, record the stage in the execution
ledger, and set this plan's State to executed, unless display work that Ben has given to the bot
remains. Commit, fetch, merge `origin/main` if it moved, and push.

**The reply to Avi** was drafted on 2026-11-04 to be sent once the pages exist, as Ben wanted of
the emails of 2026-11-03 (ledger entry 12):
`C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar/email-to-avi-2026-11-04-display-pages.md`.
Its copyable page is the `.html` beside it, built by
`C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar/render_email_2026_11_04.py`. After the
save, correct any claim of the draft that the run did not bear out, build the page again, and give
Ben its `file:///` link. Send nothing.

**Checkout and coordination,** as for the plan's other stages: a full MAM-basics clone that the
commander session assigns, verified clean on `main` at the commit that added this stage or a
descendant, with `git merge-base --is-ancestor`; its own `.venv/Scripts/python.exe`, run from its
root; and `-c safe.directory=<clone>` on every Git call. Ask the commander before any BDencklaBot
run, dry runs included, and release the clone while waiting on Ben. The stage reads MAM-simple,
the tracked JSON and the live pages; its only untracked input is the draft reply, which is in
`C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar/` alone.

## Later Word files

A new or revised book repeats Stage 3's fetch, extract and check, and a reading of the tracked
JSON's diff, and then Stages 6 to 8 for its pages, each saving run again on Ben's word. An update
goes through only for pages that nobody but BDencklaBot has edited. A book of the Twelve whose
base chapters arrive this way then gets its display page through Stage 10's mode, added to that
mode's table, again on Ben's word for each saving run.

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
