# Plan: Miqra Mevoar base chapters from Rabbi Kokhav's Word files

State: live, written 2026-11-02; Ben gave his word to execute it the same day. Stages 1 to 6 ran
that evening, and Stages 7 to 9 on 2026-11-03: Avi had himself created Joshua 1, BDencklaBot
created the other 55 base chapters of the six books, and the base-chapter index, which Stage 9
added at Ben's request, links all 929 chapters as revision 3101215. Ben offered Avi the bot for
the display pages (decisions ledger entry 13), and Avi accepted, in an answer that Ben relayed on
2026-11-04 (Deferred, “Display pages”). Stage 10, written that day and executed on Ben's word the
same day, had the bot create the seven of those pages whose base chapters exist, as revisions
3101357 to 3101363, and Ben then sent Avi a reply about them with three questions (execution
ledger, “The reply to Avi”). Avi answered on 2026-11-05: he had added Amos's link to the main
page and renamed Joshua's two display pages, and he is building a model for the parts of large
books (execution ledger, “Avi's answer to the reply”). The State stays live: the model waits on
Avi and then on Ben's decision (Deferred, “The parts of large books”), and Word files of further books
take the course of “Later Word files”. With its change of 2026-11-16 the display mode's table
took Joshua's live titles and kept Stage 10's names as their sort keys (decisions ledger entries
14 and 15). On 2026-11-16 Avi's folder held nine new
books and none of the first six: the text of Micah, Nahum, Habakkuk, Haggai and Zechariah is now
tracked (execution ledger, “Later Word files, 2026-11-16”). Ben's decisions of that day
(decisions ledger entry 15) gave round 1 to a fresh session: the bot created those five books'
29 base chapters the same day, the converter now reads Zephaniah and Daniel, whose text is
tracked, and on Ben's word the bot then created Zephaniah's 3 base chapters and the display
pages of those five books and of Zephaniah (execution ledger, “Round 1 of Ben's decisions of
2026-11-16”). Avi answered Ben's email that afternoon (Deferred, “Avi's answers to Ben's email
of 2026-11-16”), and in round 2, another fresh session, the bot created Daniel's 12 base
chapters on Ben's word of round 1 (execution ledger, “Round 2, after Avi's answers”). The
converter now reads Avi's corrected files of Judges and Malachi, saved again with other style
names, and on Ben's word of round 2 the bot created their 24 base chapters and the display page
of Malachi, the last of the Twelve's. Avi's main page now also links display pages of Judges,
in three parts, and of Daniel, in two, which Stage 11, written in round 2, plans; Ben gave his
word to execute it, in a fresh session that the commander starts. That session gave the
generator the change that Stage 11 designs and the display table its five pages, and on Ben's
word for each run, given on its decision page, the bot created all five, so Stage 11 is
executed (execution ledger, “Stage 11, the display pages of Judges and Daniel”). On
2026-11-22 Avi asked for the display pages of the five books of the Torah, which his main page
now links in parts, and Ben gave his word to plan and execute them in one session (decisions
ledger entry 16). Stage 12, written that day, plans them, and its code and its dry run are
done. On Ben's word of the same day the stage paused, and its four open choices went to Avi
in an email that Ben sent the same day (decisions ledger entry 17). Avi answered that
evening, and Ben relayed the answers with his word to act on them (entry 18): Avi corrected
the two labels that decision 1 questioned and chose 2a, 3a and 4b, the bot's block of title
and navigation. A fresh session resumed Stage 12, found his fixes on the live pages, and
wrote Stage 13, which plans the block (execution ledger, “Stage 12 resumed”). On 2026-11-23
Ben chose the three recommendations of the stage's decision page (decisions ledger entry 19),
among them the 15 pages' creation with their blocks, in one saving run; another fresh session
took his answers and executes Stage 13, and each saving run waits on his word.
The execution ledger below records each finished stage.

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
whose base chapters exist: Joshua's two parts and five books of the Twelve. Stage 11, added on
2026-11-16, plans the display pages of Judges, in three parts, and of Daniel, in two, which Avi
linked from his main page that day. Stage 12, added on 2026-11-22, plans the display pages of
the five books of the Torah, three parts to a book, which the main page links in its revision
3103840 of 2026-11-21. Stage 13, added on 2026-11-22, plans the block of title and navigation
that Avi asked for on each of those 15 parts, in the style of Joshua's first part.

## Decisions ledger

Entries 1 to 3 and 10 to 18 are Ben's decisions. Entries 5 to 9 were Claude's proposals,
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
14. **Joshua's titles in the display mode's table: later.** Ben, 2026-11-05, answering "Should
    the display table take Joshua's new titles now, or with its next change?" with "Later, as
    recommended". The recommendation was to leave `display_page.PAGES` with Stage 10's titles of
    Joshua's two pages, now redirects (execution ledger, “Avi's answer to the reply”), since no
    run is due and a change now would change nothing on Wikisource, and to make any change with
    the table's next change, when the later books of the Twelve are added. That change also
    settles whether part two keeps Stage 10's name as its category sort key. Settled by entry
    15, item 5.
15. **The update of 2026-11-16: every recommendation.** Ben, 2026-11-16, before 11:14 New York
    time, in the session that carried out the update, answering the six decisions of its
    decision page: "ask the commander for a fresh session that will follow all your
    recommendations BUT FIRST compose an email to Avi asking any questions he needs to answer,
    since even if his answers don't block making some progress, in terms of time zones we need
    to ask them as soon as possible so they don't block the second round of progress, i.e. the
    round that does depend on his answers". The recommendations, as that page gave them
    (execution ledger, “Later Word files, 2026-11-16”):
    1. **The five books' save.** One saving run creates the 29 base chapters of Micah, Nahum,
       Habakkuk, Haggai and Zechariah, with Avi's summary of entry 9. This is Ben's word for
       that run and its summary (entries 3 and 9).
    2. **Pictures.** The converter reads past a picture that holds no text, still refusing any
       drawing that holds text, and names each picture it reads past in its output. Ben tells
       Avi which verses had pictures.
    3. **Daniel's table of contents.** The converter also reads past a table of contents that
       Word built as a field after the table: empty paragraphs, and paragraphs styled "toc"
       with a level, within one field whose instruction is TOC, and nothing else.
    4. **Two slips.** Avi is asked to correct Malachi 2:16's chapter cell and Judges 6:23's
       verse cell in the files. Judges and Malachi wait for the corrected files.
    5. **Joshua's display entries.** When the display mode's table takes the new books,
       Joshua's two entries take their live titles, and Stage 10's names stay their category
       sort keys, in a field of their own.
    6. **No test** of whether the pCloud link reaches a file outside its folder.

    The page also said, needing no answer unless Ben objected, that the projection that
    `check` uses would read the hung letter of Judges 18:30 as its letter and keep the word of
    20:13 that is read but not written, as it keeps a ketiv and its qere both. Every other
    saving run, the display pages' included, still needs Ben's word for that run. Active:
    round 1 carried out items 1, 2, 3 and 5 and the projection (execution ledger, “Round 1 of
    Ben's decisions of 2026-11-16”), and for item 4 round 2 tracked the text of Avi's
    corrected files and, on Ben's word, created their base chapters (execution ledger,
    “Round 2, after Avi's answers”).
16. **The Torah's display pages.** Ben, 2026-11-22, at 09:01 New York time, in the commander
    session, asking it for a session in one of the clones on the D: drive, exactly:

    > Please create a session using one of the clones on the new D drive (to test it further) that will respond to Avi's email below (respond in the sense of doing the work requested, as well as respond in the sense of generating a draft email response when that work is done):
    >
    > email from Avi subject: Miqra Mevo'ar on the Torah
    > email from Avi body:
    > I made [section links for the five books of the Torah](https://he.wikisource.org/wiki/%D7%9E%D7%A7%D7%A8%D7%90_%D7%9E%D7%91%D7%95%D7%90%D7%A8#%D7%A1%D7%A4%D7%A8%D7%99_%D7%94%D7%AA%D7%95%D7%A8%D7%94) (similar to what was done for Joshua and Judges).
    > Would it be possible to create those pages? The purpose is to make the text usable for those who do not follow the weekly portions, including students in Israeli schools.

    This is his word to plan Stage 12 and to execute it, the work that Avi's email asks for,
    and then to draft the reply for Ben to send. Each saving run still needs his word for that
    run (entry 3), and the stage's four open choices wait on his answers on its decision page.
    Active.
17. **Stage 12 paused, its questions to Avi.** Ben, 2026-11-22, before 10:45 New York time, in
    the session executing Stage 12, after its dry run, exactly:

    > Save your work so far in git in a way that will be easily resumable, i.e. save it in a way that will require little or no redundant work required when we resume.
    >
    > Then compose an email asking all these questions of Avi, except perhaps the "save run A and save run B" ones, which aren't really his call. I don't understand what they are, but my vague sense is that the decision should be clear given my "save your work so far ..." instructions above.

    and then, about the email:

    > In the email, apologize that I'm not making some or all of these decisions myself, but admit that I cannot because I am not following any of the details or looking at the pages; I am basically acting as a relay of his emails to Claude.

    So Stage 12's decisions 1 to 4 go to Avi, in an email that the session drafted for Ben to
    send. The session reads the rest of his words as holding the saving runs, decisions 5 and
    6, until the work resumes after Avi answers; each saving run still needs Ben's word for
    that run (entry 3). Settled by entry 18.
18. **Avi's answers to Stage 12's questions.** Ben, 2026-11-22, at 20:14 New York time, in
    the commander session, relaying Avi's answers to the email of entry 17, exactly:

    > regarding the miqra mevoar project, avi writes in an email:
    >
    > 1. Fixed.
    > 2. Use the same special templates as in the parashah pages (טעם תחתון).
    > 3. Do the same as in the parashah pages.
    > 4. If the bot can create that kind of title and navigation in the very same style as Joshua 1, that would be great!
    >
    > All of the typos listed in the parashah pages, listed at the end, are now fixed.
    >
    > please act upon the decisions 1 thru 4 he provides. or I guess check that 1 is indeed fixed and act on decisions 2, 3, and 4. you might also check that indeed "All of the typos listed in the parashah pages, listed at the end [of the email in 5 bullet points], are now fixed.
    >
    > do you have record of the email this references (e.g. the numbers 1 thru 4) or should I provide that for context?

    Avi's four numbered answers are to the email's four questions, which are Stage 12's
    decisions 1 to 4, and the slips that he calls fixed are the five that the email listed
    at its end. So decision 1 rests on his corrected labels, which give Genesis' first part
    chapters 1 to 11 and Exodus' first part chapters 1 to 17, the ranges of 1a; decisions 2
    and 3 take 2a and 3a; and decision 4 takes 4b, a block of title and navigation that the
    bot builds on each of the Torah's 15 parts in the very same style as Joshua's first
    part, which needs a stage of its own and which Stage 13 plans. The
    session that resumed the stage reads Ben's words as his word to act on the four answers
    and to check Avi's fixes, and, for 4b, to plan that stage, which a fresh session
    executes; each saving run still needs his word for that run (entry 3). Active.
19. **Stage 13's decisions 7 to 9.** Ben, 2026-11-23, at 04:27 New York time, in the session
    that the commander started to take his answers and execute Stage 13, exactly:

    > I concur with all of your recommendations on the decision page. Please either proceed here or ask the commander for a fresh session in which you will proceed.

    The page recommended (a) for each of the three (Stage 13, “Choices”): 7a, the 15 pages
    created once, with their blocks, in one saving run by the stage's executor; 8a, each
    topic's label transcluding its heading from its base chapter; and 9a, no block now for the
    six parts made without one, the reply to Avi asking whether he wants them. The session,
    which did not write the stage, executes it, as his words allow; each saving run still
    needs his word for that run (entry 3). Active.

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
  - **Display pages, in Avi's answer of 2026-11-05 to that reply,** which Ben relayed that day
    (execution ledger, “Avi's answer to the reply”). Avi wrote "All of this looks great". He had
    renamed Joshua's two parts with the digits 1 and 2 in place of the letters alef and bet, "in
    order to avoid confusion", and he is building, in the first part, "a model for title and
    navigation in parts of large books" (“The parts of large books”, below).
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
- **The parts of large books.** Avi wrote on 2026-11-05 that in Joshua's first part he is
  "building a model for title and navigation in parts of large books, based on the contents of
  the page", which "presumably will become a template" and "in the future could presumably be
  built by AI". He expects that the model "will presumably be implemented for the five books of
  the Torah, too, in addition to the currently existing pages for the weekly portions". Until
  2026-11-22 nothing here built the model, which waited on Avi's model and then on a decision
  whether the bot has a part in it; Stage 13 now plans it for the Torah's 15 parts, on Avi's
  answer of that day (decisions ledger entry 18). As read at revision 3101512 (execution ledger,
  “Avi's answer to the reply”), the model is a centred block of three lines above the bot's
  text, which it leaves unchanged, with a horizontal rule after it:
  1. the part's name, pointed, as the main page labels its link, without the label's chapter
     range;
  2. its topics: Rabbi Kokhav's 18 headings in the part, in the page's order, each equal after
     NFC to the tracked JSON's heading and linked within the page to its verse;
  3. its chapters, each numeral linked within the page to the chapter's first verse.
  - **Its sources.** Everything but the part's name comes from the page's contents, and from
    data that the display generator already reads: the headings and their places from the
    tracked JSON, and the chapters from MAM-simple.
  - **The topics are copies,** not transclusions, so a heading that Rabbi Kokhav revises on its
    base chapter changes on the page's break line but not among its topics.
  - **Part two** has no such block yet.
  - **As read on 2026-11-22,** part one carries the block as Dovi reworked it on 2026-11-21, in
    revision 3103803: one centred line of templates that gives the part's name, its topics and
    its chapters, and then a horizontal rule. Judges' second part, which Dovi edited the same
    day, carries two pictures at its end and no block. Stage 12's decision 4 asked whether the
    bot makes the block for the Torah's 15 parts; Avi asked for it, in the very same style as
    Joshua's first part (decisions ledger entry 18), and Stage 13 plans it, from that block as
    revision 3103803 has it.
- **Avi's answers to Ben's email of 2026-11-16,** drafted in the update's session for Ben to
  send: `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar-2026-11-16/email-to-avi-2026-11-16.md`,
  with its copyable page beside it. Ben sent it before 11:39 New York time that day, writing in
  the update's session, as that session relayed his words: "Email sent to Avi." (execution
  ledger, “Round 1 of Ben's decisions of 2026-11-16”). Its five questions: whether Avi will clear Malachi 2:16's
  chapter cell; whether he will correct Judges 6:23's verse cell; whether Daniel's file,
  changed on 2026-11-16 after the others, is final; whether he wants display pages for Judges
  and Daniel, and how each would be divided and titled; and whether Micah's same heading
  before 1:1 and 2:1 is intended. Judges and Malachi wait on the first two. The third bears on
  Daniel's save: Ben's word "Do the saves recommended in 1a and 2a" took the decision page's
  1a, "Save Zephaniah's 3 now, and Daniel's 12 once Avi says his file is final", so Daniel's
  save needs no further word if Avi says so and the file is unchanged. A display page for Judges or Daniel waits on the fourth and then on a stage
  of this plan that Ben approves. Avi answered on 2026-11-16, in a reply that Ben pasted into
  the commander session at 15:16 New York time and that the execution ledger quotes (“Round 2,
  after Avi's answers”): he made both corrections in the files, Daniel's file is final, he
  linked display pages for Judges and Daniel from the main page, and the pictures may be
  ignored. Stage 11 is the stage that the fourth answer called for.

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
- **Avi's answer to the reply, 2026-11-05:** Ben pasted it, undated, into the commander session
  at 10:29 New York time, under his own first line: "spawn a session to reflect (perhaps in
  whatever miqra mevoar plan exists) this feedback from Avi (perhaps looking at his changes to
  make sure we know what he's talking about)". He did not say what it answers; the commander
  took it, as this entry does, for Avi's answer to the reply of 2026-11-04, whose pages it
  discusses (Deferred, “Display pages”). The commander started a fresh Claude (Opus 5.5)
  session, with a brief saved as
  `C:/Users/BenDe/GitRepos/MAM-basics/.novc/commander-session/miqra-mevoar-avi-feedback-brief-2026-11-05.md`,
  SHA-256 `B657391CB0799391308A9F86005568CF0BDA1B9E12A06FFF9B5F7DB9974AC855`. Its checkout,
  `C:/Users/BenDe/GitRepos2/MAM-basics`, was verified at 10:36 New York time: on `main`, clean,
  at `5a6ce47752d01af360b0489e10184c500f378949`. The session ran no BDencklaBot command and
  edited nothing on Wikisource.
  - **The read.** On Ben's words, the session read anonymously at 10:41 New York time, in 18
    requests through `polite_download.PoliteDownloader`: the seven pages and their histories,
    the old titles and their move logs, the main page's revisions from 3101310, and the log
    events and contributions since 2026-11-04 at 11:00 New York time of Dovi, Avi's account.
    The responses are kept byte for byte, with a README, in
    `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar-avi-feedback-2026-11-05/`.
  - **The rename.** Dovi moved Joshua's two parts, which keep their page ids and histories.
    Each move left a redirect at the old title, and the main page links the new titles from its
    revision 3101502. Part two's text is still the bot's byte for byte, and each part's category
    line still sorts it under Stage 10's name. The moves:
    1. part one, page 1756989, at 06:03 New York time: from `מקרא מבואר/תצוגה/ספר יהושע א`
       to `מקרא מבואר/תצוגה/ספר יהושע 1`, the redirect being revision 3101499;
    2. part two, page 1756990, at 06:04: from `מקרא מבואר/תצוגה/ספר יהושע ב`
       to `מקרא מבואר/תצוגה/ספר יהושע 2`, the redirect being revision 3101501.
  - **Part one** has six edits by Dovi after the move, from 06:11 to 07:21 New York time, ending
    at revision 3101512. They add Avi's model above the bot's text, which stays byte for byte as
    the bot made it (Deferred, “The parts of large books”). At 05:58, before the move, he had
    also marked the bot's revision of part one as reviewed, in Wikisource's review log.
  - **The main page** is at revision 3101507, after six revisions by Dovi from 05:56 to 06:25
    New York time. Its lists of the Prophets and the Writings are no longer numbered; the
    Twelve's links stand on one line, with Amos's between Joel's and Obadiah's from revision
    3101494; and revision 3101507 adds vowel points to Joshua's name and to its parts' labels.
    The API's parse of that revision finds all seven display pages linked and existing, and the
    links of Micah to Malachi still red.
  - **Nothing else changed.** The other five pages have only the bot's revision. Dovi's
    contributions since 2026-11-04 at 11:00 New York time are those twelve edits and the four
    revisions that the moves made, and his log events are the two moves and the review.
  - **The reply's three questions.** The live main page answers the first, since it links
    Amos. The email does not answer the second, on the display pages of Micah to Malachi, but
    it asks for none of them now, and it begins "All of this looks great"; so each is still made
    after its base chapters, as Stage 10, “Left out”, provides. On the third, the pages' form,
    Avi asks no change to the seven pages, and adds his model to Joshua's part one.
  - **The tracked code keeps Stage 10's titles.** `py/miqra_mevoar/display_page.py`'s `PAGES`
    keeps Joshua's two old names, which its docstring and a comment say were copied from the
    main page's revision 3101310. The keys `yehoshua-1` and `yehoshua-2` are unchanged, so
    `py/main_ws_bot.py`'s help and `py/ws/pywikibot-setup.md` stay true. A run of
    `miqra-mevoar-display`, dry or saving, given no `--page` or either Joshua key, meets the
    old titles. pywikibot 11.7.0's `Page.exists()` is true of a redirect, and `Page.text` gives
    the redirect's own text, so the mode refuses both pages, lists each redirect's revision by
    Dovi, saves nothing for them and exits non-zero; the other five pages are unchanged. While
    the redirects stand, no run can create a page at an old title. Giving the table the new
    names would not make Joshua's pages unchanged: part one now carries Avi's model, and the
    generator takes each page's category sort key from the table's name, so part two would be
    unchanged only if Stage 10's name stayed its sort key. Whether the table takes the new
    titles now, or with its next change, waits on Ben's decision.
  - **Ben's decision on the titles,** the same day: "Later, as recommended" (decisions ledger
    entry 14).
- **Later Word files, 2026-11-16:** Ben typed in the commander session at 09:42 New York time:
  “Launch a session that will update Miqra Mevoar based on new files found at the "pCloud" link.
  BTW verify that the "pCloud" link is either not git-tracked at all, or only-git-tracked in
  MAM-private (NOT MAM-basics).” The commander's brief reports that it found the link's code in
  no tracked file and no commit, on any ref, of GitRepos and GitRepos2's clones of MAM-basics and
  MAM-private, and that Git ignores the link file. The commander started a fresh Claude (Opus
  5.5) session with that brief, saved as
  `C:/Users/BenDe/GitRepos/MAM-basics/.novc/commander-session/miqra-mevoar-update-brief-2026-11-16.md`,
  SHA-256 `A3E12FC0A1EF47FB91B1CE727557EAF0D43A0764726631FB1E4FCB4FB720C523`. Its checkout,
  `C:/Users/BenDe/GitRepos2/MAM-basics`, was verified at about 09:55 New York time: on `main`,
  clean, at `2a108647c4b17e587a00549eb9fa8de8958e0e3e`, then fast-forwarded to origin's
  `babc6ba7756e43eb7696af332625af7918437753`, whose two new commits touch nothing of this plan's.
  - **The fetch,** at 09:56 New York time into
    `.novc/miqra-mevoar/pcloud/20261116-095654-155958-0500/`, brought nine Word files, all new:
    `sephershoftim.docx` (Judges), 364,865 bytes; `mikha.docx`, 113,269; `nahum.docx`, 83,586;
    `havaquq.docx`, 87,618; `tzefanya.docx`, 106,002; `hagay.docx`, 78,314; `zekharya.docx`,
    163,867; `malakhi.docx`, 91,420; and `daniyel.docx`, 253,304. pCloud dates each of them
    2026-11-15, except Daniel's, 2026-11-16. The folder no longer holds the six earlier books'
    Word files or Joshua's PDF. The newest earlier fetch, `20261103-145602-860752-0500`, holds
    them, and its six Word files equal by SHA-256 the sources that the tracked JSON records. The
    folder still holds `.~lock.yehoshua.docx#`, which `fetch` skipped.
  - **Four of the files stop the converter,** as its closed dispatch requires. A read-only
    diagnosis by the scripts in `.novc/miqra-mevoar-2026-11-16/scripts/`, with their reports
    beside them, set each stop aside in memory to find the next, and then ran `check`'s
    comparisons with MAM-simple on the result:
    1. **Judges,** `sephershoftim.docx`: two small pictures, about a centimetre across, in the
       paraphrase cells of 8:7 and 9:14, which the XML reader does not name; and the verse cell
       of 6:23, whose letters are bet and gimel, not the numeral kaf gimel. MAM-simple's Judges
       also has two elements that the projection in `py/miqra_mevoar/mam_simple.py` does not
       name: `letter-hung`, the hung nun of 18:30, and `kq-q-velo-k`, the word of 20:13 that is
       read but not written.
    2. **Zephaniah,** `tzefanya.docx`: two small pictures in the verse-number cells of 2:13 and
       2:14, whose descriptions name image files on daf-yomi.com, `strix1.jpg` and `bubo.jpg`,
       the Latin names of two kinds of owl.
    3. **Malachi,** `malakhi.docx`: an equals sign and a semicolon in the chapter cell of 2:16,
       which begins no chapter.
    4. **Daniel,** `daniyel.docx`: after its table, a table of contents of the book's name and
       its 14 headings, with page numbers, which Word built as a TOC field in 15 paragraphs
       styled "toc 2" and "toc 4", outside any content control, unlike Joshua's.

    With those set aside, and with the projection reading the hung nun as its letter and keeping
    the word read but not written, the four read as Judges, 21 chapters, 618 verses and 51
    headings; Zephaniah, 3, 53 and 3; Malachi, 3, 55 and 7; and Daniel, 12, 357 and 14. `check`'s
    comparisons find no failure in any of them. Judges' title row, like Obadiah's, has no vav.
    What becomes of each file waits on Ben's decisions.
  - **The other five books** joined `books.BOOKS`, each title copied by script from its file's
    title row: `mikha`, `nahum`, `havaquq`, `hagay` and `zekharya`. Since `check` requires a
    directory's Word files to be exactly the tracked books, `extract`, `check` and `pages` ran on
    `.novc/miqra-mevoar/combined/20261116-100316-381543-0500/`, which joins those five files with
    the six earlier books' files from the fetch of 2026-11-03. Each file equals its fetch's
    manifest by SHA-256, and the directory's `sources.json` names each file's fetch.
    `in/miqra-mevoar/README.md` now describes such a directory.
  - **The results.** `extract` wrote the five new files and rewrote the six earlier ones byte for
    byte: Micah, 7 chapters, 105 verses and 12 headings; Nahum, 3, 47 and 3; Habakkuk, 3, 56 and
    3; Haggai, 2, 38 and 4; and Zechariah, 14, 211 and 21; in all 29 chapters, 457 verses and 43
    headings. `check` passed for all eleven books, with the report
    `.novc/miqra-mevoar/checks/20261116-100324-636850-0500.txt`. Among the five, the smallest
    margin is that of Zechariah 6:2 and 6:3, 1.000 against 0.695, and the lowest ratio that of
    Zechariah 14:6, which has a ketiv and a qere, 0.842 against 0.427. `pages` wrote 85 pages into
    `.novc/miqra-mevoar/pages/20261116-100336-311211-0500/`, and those of the six earlier books
    equal the prototype's byte for byte.
  - **The reading of the JSON's diff,** aided by the survey
    `.novc/miqra-mevoar-2026-11-16/survey-new-json-20261116.txt`: the five files have no
    character that the six earlier books lack, only Hebrew letters and marks, the space and
    ordinary punctuation. Micah's headings before 1:1 and 2:1 are the same text, a prophecy of
    Samaria's destruction. Zechariah repeats two paraphrases, at 4:4 and 6:4 and at 7:4 and 8:18;
    MAM-simple's letters of 7:4 and 8:18 are the same, and those of 4:4 and 6:4 match with a
    ratio of 0.938.
  - **The dry run,** at 10:09 New York time, from the tree that this entry's commit records,
    after a check that no other BDencklaBot run was in progress: `miqra-mevoar --no-save` over
    the five books gave 29 creates, no title existing, and exited non-zero, as a dry run before a
    save does. Its 29 pages equal those of `pages` byte for byte. Run
    `.novc/mam-ws-bot-miqra-mevoar-runs/20261116-100925-652046-0500/`. The save waits on Ben's
    word for that run, with its summary.
  - **Checks:** `git diff --check`, Black on `py/miqra_mevoar/books.py`, and Stage 10's
    verification command with `py/tests/test_miqra_mevoar_save_receipts.py` added (113 passed);
    then, with the new files staged so that the tree-wide lints read them, those lints and the
    versification test again (50 passed). The full suite and the mega were skipped: the change
    adds five table entries and five data files that only the Miqra Mevoar converter, its bot
    modes and their tests read, and the mega reads none of them.
  - **Pushed** as `b3eab6bc`. The decision page, an artifact,
    https://claude.ai/artifact/KANC5eqKCUMX9Hdu8aiUvR, put six decisions to Ben.
  - **The pCloud link's reach,** which Ben asked about the same morning: "my concern is if you
    can use it to navigate "up" in a directory hierarchy". The link is a pCloud shared link,
    `u.pcloud.link/publink/show` with an opaque code, to the folder that holds the Word files,
    with the rights to read and download only. pCloud's listing of it, as fetched on
    2026-11-02, holds no id or path of any folder above that one, and the public-link methods
    take only the link's code and, for a download, a file's id. So no way up is exposed.
    pCloud's warning about parent folders concerns its Public Folder's direct links, whose
    address is a path, another kind of link. Not tested, by Ben's decision (decisions ledger
    entry 15, item 6): whether a download through the link refuses the id of a file outside
    the folder.
  - **The link's copies,** by a search for its code that printed only paths: the link file of
    decisions ledger entry 8, which Git ignores; Claude Code's backup of it under
    `~/.claude/file-history/`; and two Claude Code transcripts, the Phase 1 session's and the
    commander's of October 29 to November 10. The code is in no other file of the eight clones
    of the four forests, and in no commit or commit message of GitRepos2's two clones, origin's
    branches included.
  - **Ben's decisions and the email to Avi:** decisions ledger entry 15, and Deferred, “Avi's
    answers to Ben's email of 2026-11-16”. The rest of the work goes to a fresh session that
    the commander starts, with the brief
    `C:/Users/BenDe/AppData/Local/Claude-Data/claude_pzs8sxrjxfjjc/side-session-notes/local_a80ded65-f78e-4280-8493-9dab3b8c5686/miqra-mevoar-round-1-brief-2026-11-16.md`.
- **Round 1 of Ben's decisions of 2026-11-16:** the commander adapted that draft and started a
  fresh Claude (Opus 5.5) session with it, saved as
  `C:/Users/BenDe/GitRepos/MAM-basics/.novc/commander-session/miqra-mevoar-round-1-brief-2026-11-16.md`,
  SHA-256 `E2C65BC586FCA6F0599964253CB666A82AE41A7B5F72739BD91005AD029290E6`. Its checkout,
  `C:/Users/BenDe/GitRepos2/MAM-basics`, was verified before a fetch at 11:37 New York time: on
  `main`, clean, at `1884cf59c47d85d8cb74ec3f2a2a26015444e431`, level with origin, with no
  other session working in it.
  - **The email to Avi** went out: the update's session reported in the shared notes folder at
    11:39 New York time that Ben had sent it (Deferred, “Avi's answers to Ben's email of
    2026-11-16”).
  - **The fetch,** at 11:37 New York time into
    `.novc/miqra-mevoar/pcloud/20261116-113743-667491-0500/`: its manifest is byte-identical to
    that of the morning's fetch, so no Word file had changed, and the slips of Malachi and
    Judges are still in their files.
  - **The save** of decisions ledger entry 15, item 1. Before the dry run, and again before the
    save, no `main_ws_bot.py` process was running on the machine and no session of the
    commander's family was busy. The dry run at 11:40 New York time gave 29 creates, and its
    pages equal those of the dry run of 10:09 byte for byte. The saving run, from 11:42 to
    11:47 with Avi's summary of entry 9, copied from this plan by script, created the 29 pages
    as revisions 3102993 to 3103022, all but 3102999, read each back equal to the generated
    text, and exited zero. A read after the run, without the bot's login, found each page with
    one revision, BDencklaBot's, not minor, with that summary, and each creation and its
    category entry with the bot flag. A dry rerun found all 29 unchanged and exited zero.
    `py/ws/ws_bot_edit_history.md` has the entry, with the run directories.
  - **The converter,** decisions ledger entry 15, items 2 and 3, and the projection that the
    decision page announced:
    1. `py/miqra_mevoar/docx_table.py` reads past a drawing only in a table cell, and only
       when it is one frame, inline or anchored, whose graphic data is one picture and which
       holds no text: no WordprocessingML element, and no text, text box or text body of
       DrawingML. `read_table` gives each picture's row and cell, and `extract`'s output and
       `check`'s report name it by file, row, the row's place and cell. Any other drawing,
       and a picture outside a cell, still raise.
    2. After the table, the same module reads past empty paragraphs and one field whose
       instruction is TOC, its text only in its result and only in paragraphs styled "toc"
       with a level, with PAGEREF fields nested in its result and none nested in them. A
       field character or instruction anywhere else still raises. Joshua's content control
       is read as before.
    3. `py/miqra_mevoar/mam_simple.py`'s projection reads `letter-hung` as its letter and
       keeps `kq-q-velo-k`, as it keeps a ketiv and its qere both.
    4. `py/miqra_mevoar/books.py` gains `tzefanya` and `daniyel`, each title copied by script
       from its file's title row through the new reader; each equals MAM's name of the book.
  - **The results,** on `.novc/miqra-mevoar/combined/20261116-115425-523981-0500/`, which joins
    the six earlier books' files from the fetch of 2026-11-03 with the seven others from that
    of 11:37. `extract` wrote Zephaniah, 3 chapters, 53 verses and 3 headings, naming its two
    pictures, in the verse cells of 2:13 and 2:14, and Daniel, 12, 357 and 14, its table of
    contents read past; it rewrote the other eleven books' JSON byte for byte. `check` passed
    for all thirteen, with the report `.novc/miqra-mevoar/checks/20261116-115439-327550-0500.txt`.
    Zephaniah's and Daniel's margins and ratios equal those of the update's diagnosis with its
    problems set aside in memory: Daniel's smallest margin is that of 3:2, 0.897 against 0.667,
    and its lowest ratio that of 5:30, 0.750 against 0.174. `pages` wrote 100 pages into
    `.novc/miqra-mevoar/pages/20261116-115451-round-1/`, and the eleven books' 85 equal those
    of 10:03 byte for byte. With the new reader, Judges gets past its pictures and stops at its
    verse cell of 6:23, and Malachi at its chapter cell of 2:16, as round 2 expects. The
    reading of the new JSON, aided by a survey script in
    `.novc/miqra-mevoar-round-1-2026-11-16/scripts/`: neither file has a character that the
    eleven earlier books lack, only Hebrew letters and marks, the space and ordinary
    punctuation, and neither repeats a paraphrase or a heading.
  - **The dry run of Zephaniah's and Daniel's base chapters,** at 11:56 New York time: 15
    creates, and the run's pages equal those of `pages` byte for byte (run
    `.novc/mam-ws-bot-miqra-mevoar-runs/20261116-115613-777573-0500/`). Their save needs Ben's
    word; Avi's answer to the email's third question, whether Daniel's file is final, bears on
    Daniel's.
  - **Checks:** `git diff --check`; Black on the five changed modules; Stage 10's verification
    command with `py/tests/test_miqra_mevoar_save_receipts.py` added, after staging the two
    new JSON files so that the tree-wide lints read them (119 passed). The mega and the full
    suite were skipped: the mega runs none of this code, and the converter is imported only by
    its entry point, its three bot modes and five tests, all in that run.
  - **Pushed** as `2a82085e`.
  - **The display mode's table,** decisions ledger entry 15, item 5. `Page` in
    `py/miqra_mevoar/display_page.py` gains `sort_key`, its category line's sort key where that
    is not the page's name. `PAGES` gives Joshua's two parts the titles to which Avi moved them
    and keeps Stage 10's names as their sort keys, and it adds Micah, Nahum, Habakkuk, Haggai
    and Zechariah. Every new name was copied by script from the main page's latest revision,
    3101507, read again just before; the other five names equal that revision's links.
    `py/tests/test_miqra_mevoar_display.py` takes a page's expected sort key from the table.
  - **The display dry runs,** at 12:03 New York time, after a `miqra-mevoar --no-save` run over
    the five books found all 29 base chapters unchanged (run
    `.novc/mam-ws-bot-miqra-mevoar-runs/20261116-120237-571476-0500/`) and the main page was
    still at revision 3101507:
    1. **The five new pages:** five creates, and the parse check found no missing link or
       transcluded page (run `.novc/mam-ws-bot-miqra-mevoar-display-runs/20261116-120302-349946-0500/`).
       In the columns of Stage 10's table, verse lines; petuhot and setumot; headings; and
       break lines with a break only, a heading only and both: Micah 105; 12 and 4; 12; 5, 1
       and 11. Nahum 47; 2 and 1; 3; 1, 1 and 2. Habakkuk 56; 4 and 4; 3; 6, 1 and 2. Haggai
       38; 7 and 0; 4; 5, 2 and 2. Zechariah 211; 25 and 9; 21; 16, 3 and 18. In all: 457 verse
       lines, 68 breaks, 43 headings and 76 break lines.
    2. **Joshua's two keys:** part one refused, listing Dovi's seven revisions from 3101498 to
       3101512 after the bot's 3101357, and part two unchanged. Both parts' generated pages
       equal those of Stage 10's dry run byte for byte (run
       `.novc/mam-ws-bot-miqra-mevoar-display-runs/20261116-120307-948003-0500/`). The mode
       only creates, so no run saves anything for Joshua.

    The save of the five pages needs Ben's word, with its summary; the session offers Stage
    10's.
  - **Pushed** as `4136d08c`. The decision page, an artifact,
    https://claude.ai/artifact/JxV9X7eRsyPm8DxQRmZD8a, built by script from the dry runs and
    this plan, puts two decisions to Ben: the save of Zephaniah's and Daniel's 15 base
    chapters, recommending Zephaniah's now and Daniel's once Avi says his file is final; and
    the save of the five display pages with Stage 10's summary, recommended.
  - **Ben's word,** in the round 1 session before 12:20 New York time, answering the decision
    page: "Do the saves recommended in 1a and 2a". So Zephaniah's base chapters were saved and
    Daniel's wait for Avi's word that his file is final (1a), and the five display pages were
    saved with Stage 10's summary (2a).
  - **Zephaniah's save.** A fetch at 12:19 New York time into
    `.novc/miqra-mevoar/pcloud/20261116-121956-152507-0500/` gave a manifest byte-identical to
    that of 11:37. No `main_ws_bot.py` process was running before either bot run of this save.
    The dry run at 12:20 gave 3 creates, with pages equal to those of 11:56 byte for byte. The
    saving run at 12:21, with Avi's summary copied from this plan by script, created Zephaniah
    1 to 3 as revisions 3103032 to 3103034, read each back equal to the generated text, and
    exited zero. A read after the run, without the bot's login, found each page with one
    revision, BDencklaBot's, not minor, with that summary and the bot flag. A dry rerun found
    all 3 unchanged and exited zero.
  - **The display pages' save.** Before it, a `miqra-mevoar --no-save` run over the five books
    found all 29 base chapters unchanged (run
    `.novc/mam-ws-bot-miqra-mevoar-runs/20261116-122231-819251-0500/`), and the main page was
    still at revision 3101507. The saving run at 12:23 New York time, with Stage 10's summary
    copied from this plan by script, created the pages of Micah, Nahum, Habakkuk, Haggai and
    Zechariah as revisions 3103035 to 3103039, read each back equal to the generated text, one
    of them after a `maxlag` wait, and exited zero; its pages equal those of the dry run at
    12:03 byte for byte. A read after the run found each page with one revision, BDencklaBot's,
    not minor, with that summary, and each creation and its category entry with the bot flag.
    A dry rerun found all five unchanged, with no missing link or transcluded page, and exited
    zero. `py/ws/ws_bot_edit_history.md` has an entry for each of the two saves, with the run
    directories, and the decision page marks both decisions answered and carried out.
  - **Zephaniah's display page.** The brief put it in round 2, beside Malachi's, though it waits
    on nothing of Avi's: only on its base chapters, which existed from 12:21. Ben asked, after
    the session's report of 12:28: "Why wasn't this Zephaniah work part of what you already
    did?" The session added Zephaniah to the display mode's table, its name copied by script
    from the main page's revision 3101507, read again at 12:39 New York time. A `miqra-mevoar
    --no-save` run found Zephaniah's 3 base chapters unchanged (run
    `.novc/mam-ws-bot-miqra-mevoar-runs/20261116-123944-251638-0500/`), and the display dry run
    at 12:39 gave one create, with no missing link or transcluded page: 53 verse lines; 3
    petuhot and 3 setumot; 3 headings; and break lines with a break only, a heading only and
    both, 4, 1 and 2 (run `.novc/mam-ws-bot-miqra-mevoar-display-runs/20261116-123948-889773-0500/`).
    Its save needs Ben's word; the decision page asks for it as decision 3.
  - **Zephaniah's display page saved,** on Ben's word, answering decision 3: "Do the save
    recommended in 3a". Before the save, Zephaniah's 3 base chapters were again unchanged (run
    `.novc/mam-ws-bot-miqra-mevoar-runs/20261116-124654-178558-0500/`) and the main page still
    at revision 3101507. The saving run at 12:47 New York time, with Stage 10's summary copied
    from this plan by script, created the page as revision 3103041, read it back equal to the
    generated text, and exited zero; its page equals the dry run's byte for byte. A read after
    the run, without the bot's login, found the page with one revision, BDencklaBot's, not
    minor, with that summary, and the creation and its category entry with the bot flag. A dry
    rerun found it unchanged, with no missing link or transcluded page, and exited zero.
    `py/ws/ws_bot_edit_history.md` has the entry, with the run directories, and the decision
    page marks decision 3 answered and carried out.
  - **The report to Avi.** At Ben's request the session drafted an email reporting round 1's
    saves:
    `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar-round-1-2026-11-16/email-to-avi-2026-11-16-saved.md`,
    with its copyable page beside it, built by `scripts/build_email_saved.py` there, which
    requires every link to name a page that round 1 saved. It tells Avi that Daniel's 12 base
    chapters are ready and that the bot will create them once he says the file is final, and
    that Judges and Malachi follow his corrections. Ben, before 13:00 New York time: "I sent
    the email to Avi."
  - **Round 2** waits on Avi's answers (Deferred, “Avi's answers to Ben's email of
    2026-11-16”). Its standalone prompt, written for the commander when this session ended, is
    `C:/Users/BenDe/AppData/Local/Claude-Data/claude_pzs8sxrjxfjjc/side-session-notes/local_a80ded65-f78e-4280-8493-9dab3b8c5686/miqra-mevoar-round-2-prompt-2026-11-16.md`.
- **Round 2, after Avi's answers, 2026-11-16:** Ben pasted Avi's reply to his email of that day
  into the commander session at 15:16 New York time, with the instruction "launch a session to
  act on avi's reply email related to the Miqra Mevoar project". Avi's reply, as Ben pasted it,
  with the link on "main page" left out:

  > I made the two small corrections in the files (#1-#2).
  > Yes, Daniel is good to go (#3). I guess he just finished it.
  > I put in links on the main page for Judges and Daniel (4).
  > You can ignore the pictures. If he wants, he can deal with them himself in terms of
  > licenses and everything. I'll let him know about the repeated title, and he can fix that
  > too.

  The commander started a fresh Claude (Opus 5.5) session with a brief that adapts round 1's
  prompt, saved as
  `C:/Users/BenDe/GitRepos/MAM-basics/.novc/commander-session/miqra-mevoar-round-2-brief-2026-11-16.md`,
  SHA-256 `750C3AC2DC03C086AE989620751C70905BE20E11D66CFB86D7ACD71041FAD425`. Its checkout,
  `C:/Users/BenDe/GitRepos2/MAM-basics`, was verified at 15:22 New York time: on `main`, clean,
  at `b41f31668958bdaade9a9846fbbf07aa75f76fac`, level with origin, with no other session
  working in it.
  - **The fetch,** at 15:24 New York time into
    `.novc/miqra-mevoar/pcloud/20261116-152406-317227-0500/`: Daniel's file and the six other
    files of round 1 are byte-identical to those of the fetch at 12:19, and Daniel's equals by
    SHA-256 the source that `in/miqra-mevoar/daniyel.json` records. Judges' and Malachi's files
    are new: pCloud dates them 2026-11-16 at 19:44 and 19:43 UTC, and they have 160,983 and
    27,650 bytes, against 364,865 and 91,420 before.
  - **Daniel's save,** on Ben's word of round 1 (“Round 1 of Ben's decisions of 2026-11-16”,
    “Ben's word”) and Avi's answer. Before the dry run, and again before the save, no
    `main_ws_bot.py` process was running on the machine and no other session of the
    commander's family was doing bot work. The dry run at 15:25 New York time gave 12 creates,
    and its pages equal those of the dry run of 11:56 byte for byte (run
    `.novc/mam-ws-bot-miqra-mevoar-runs/20261116-152525-435088-0500/`). The saving run, from
    15:26 to 15:28 with Avi's summary of entry 9, copied from this plan by script, created
    Daniel 1 to 12 as revisions 3103073 to 3103086, all but 3103077 and 3103083, read each back
    equal to the generated text, and exited zero. A read after the run, without the bot's
    login, found each page with one revision, BDencklaBot's, not minor, with that summary, and
    each creation and its category entry with the bot flag. A dry rerun found all 12 unchanged
    and exited zero. `py/ws/ws_bot_edit_history.md` has the entry, with the run directories. A
    first launch of the save, at 15:25, ran nothing: the folder of its log did not exist, so
    PowerShell refused the redirection before it started the launcher, and no run directory
    was made.
  - **Judges' and Malachi's corrected files** hold Avi's two corrections: Judges 6:23's verse
    cell has the numeral kaf gimel, and Malachi 2:16's chapter cell is empty. A comparison
    with round 1's copies through the converter's table reader found every other cell's text
    the same, but for whitespace gone from the ends of five Bible cells, a paraphrase cell
    and a heading, which the converter trims in any case
    (`.novc/miqra-mevoar-round-2-2026-11-16/survey-texts-and-styles.txt`). Judges' pictures
    are still in the paraphrase cells of 8:7 and 9:14. But the files were saved again with
    other style names: the styles named "heading 2" and "heading 4", with the ids "2" and
    "4", are now named "Heading 2" and "Heading 4", with the ids "Heading2" and "Heading4",
    and every paragraph that had no style has the style "Normal". So the converter's closed
    dispatch stopped at each file's title row.
  - **The converter,** in `py/miqra_mevoar/extract.py`, now names "Heading 2" beside "heading
    2" as the title's style, and "Heading 4" beside "heading 3" and "heading 4" as a
    heading's, and its docstring says which files use which. A census of the styles of the
    table paragraphs of all fifteen files found no others: no style, "heading 2", "heading
    3" and "heading 4" in the thirteen earlier files, and "Normal", "Heading 2" and "Heading
    4" in the two corrected ones. "Normal", like no style, makes no row a title or a
    heading. `books.BOOKS` gains `sephershoftim` and `malakhi`, each title copied by script
    from its file's title row through the reader: Malachi's equals MAM's name of the book,
    and Judges', like Obadiah's, lacks the vav of MAM's name.
  - **The results,** on `.novc/miqra-mevoar/combined/20261116-153615-763470-0500/`, which joins
    the six earlier books' files from the fetch of 2026-11-03 with the nine others from that
    of 15:24. `extract` wrote Judges, 21 chapters, 618 verses and 51 headings, naming its two
    pictures, and Malachi, 3, 55 and 7, as the update's diagnosis had found them; it rewrote
    the other thirteen books' JSON byte for byte. `check` passed for all fifteen, with the
    report `.novc/miqra-mevoar/checks/20261116-153628-775184-0500.txt`: Judges' smallest
    margin is that of 16:7 and 16:8, 1.000 against 0.614, and its lowest ratio that of 7:21,
    0.962 against 0.322; Malachi's are those of 3:11, 1.000 against 0.472, and of 3:12, 0.989
    against 0.411. `pages` wrote 124 pages into
    `.novc/miqra-mevoar/pages/20261116-153645-round-2/`, and the thirteen books' 100 equal
    those of round 1 byte for byte. The reading of the new JSON, aided by a survey script in
    `.novc/miqra-mevoar-round-2-2026-11-16/scripts/`: neither file has a character that the
    thirteen earlier books lack, only Hebrew letters and marks, the space and ordinary
    punctuation; Malachi repeats no paraphrase or heading, and Judges repeats one heading,
    Samson's revenge, before 15:1 and before 16:23.
  - **Checks:** `git diff --check`; Black on the two changed modules; Stage 10's verification
    command with `py/tests/test_miqra_mevoar_save_receipts.py` added, after staging the two
    new JSON files so that the tree-wide lints read them (129 passed). The mega and the full
    suite were skipped: the mega runs none of this code, and the converter is imported only
    by its entry point, its three bot modes and five tests, all in that run.
  - **Pushed** as `9b2d8909`.
  - **The dry run of Judges' and Malachi's base chapters,** at 15:43 New York time, from that
    commit, after a check that no `main_ws_bot.py` process was running and no other session
    of the commander's family was doing bot work: 24 creates, no title existing, and the
    run's pages equal those of `pages` byte for byte (run
    `.novc/mam-ws-bot-miqra-mevoar-runs/20261116-154317-514447-0500/`). The save needs Ben's
    word for that run, with its summary.
  - **The main page,** read again at 15:38 New York time, is at revision 3103065, Dovi's of
    14:54. Since revision 3101507 it has gained only links to display pages of Judges and
    Daniel, in parts: Judges' first part from 1:1 to 2:5, its second from 2:6 to the end of
    chapter 16 and its third chapters 17 to 21, and Daniel's first part chapters 1 to 6 and
    its second chapters 7 to 12. The Twelve's line is unchanged.
  - **Malachi's display page.** Malachi joins the display mode's table, its name copied by
    script from the twelfth link of the Twelve's line in revision 3103065, which equals MAM's
    name of the book. A preview dry run at 15:43 New York time gave one create: 55 verse
    lines; 6 petuhot and 1 setuma; 7 headings; and break lines with a break only, a heading
    only and both, 1, 1 and 6. Its parse check found red links to exactly Malachi's three
    base chapters, which do not exist yet (run
    `.novc/mam-ws-bot-miqra-mevoar-display-runs/20261116-154353-296615-0500/`). Its save
    needs Ben's word, and then the base chapters' save and a fresh dry run that finds no
    missing link.
  - **Checks** of the table's change: `git diff --check`; Black on `display_page.py`; Stage
    10's verification command with `py/tests/test_miqra_mevoar_save_receipts.py` added (130
    passed). Pushed as `a5df0ffc`.
  - **Stage 11,** the display pages of Judges and Daniel, written into this plan as planning
    only. A forked sub-agent of the round 2 session, writing nothing but its own folder,
    `.novc/miqra-mevoar-round-2-2026-11-16/stage-11/`, read the parasha page of Noah and the
    verse template, measured the counts by a walk that shares no code with the generator,
    and drafted the stage; the session checked its counts, its quotations of the Noah page
    and its five names against the kept responses, and placed it by script, with two changes
    of wording.
  - **The decision page,** an artifact, https://claude.ai/artifact/QVrERyj3zqyDacRCCr81YD,
    built by script from the dry runs, the kept responses and this plan, puts three
    decisions to Ben: 1, the save of Judges' and Malachi's 24 base chapters with Avi's
    summary, recommended now; 2, the save of Malachi's display page with Stage 10's summary
    right after it, on the conditions above, recommended; and 3, his word to execute Stage
    11 in a fresh session, recommended, with Daniel's two pages free to go first.
  - **Ben's word,** in the round 2 session before 16:01 New York time, answering the decision
    page: "Do 1a, 2a and 3a". So Judges' and Malachi's 24 base chapters are saved now, after
    a fresh fetch finds both files unchanged and a fresh dry run gives the pages put to him
    (1a); Malachi's display page right after them, if a fresh run finds its base chapters
    unchanged, the main page still links its title and a fresh dry run finds no missing link
    (2a); and Stage 11 is executed in a fresh session that the commander starts, each of its
    saves on Ben's word for that run (3a).
  - **The base chapters' save.** A fetch at 16:01 New York time into
    `.novc/miqra-mevoar/pcloud/20261116-160109-118981-0500/` gave a manifest byte-identical
    to that of 15:24. No `main_ws_bot.py` process was running before the dry run or before
    the save; of the commander's family, only the session on the morphhb page was busy, on a
    page generator in the GitRepos clone, not on bot work. The dry run at 16:02 gave 24
    creates, with pages equal to those of 15:43 byte for byte (run
    `.novc/mam-ws-bot-miqra-mevoar-runs/20261116-160214-376731-0500/`). The saving run, from
    16:02 to 16:07 with Avi's summary of entry 9, copied from this plan by script, created
    Judges 1 to 21 and Malachi 1 to 3 as revisions 3103109 to 3103133, all but 3103128, read
    each back equal to the generated text, and exited zero. A read after the run, without the
    bot's login, found each page with one revision, BDencklaBot's, not minor, with that
    summary, and each creation and its category entry with the bot flag. A dry rerun found
    all 24 unchanged and exited zero. `py/ws/ws_bot_edit_history.md` has the entry, with the
    run directories.
  - **Malachi's display page's save.** The dry rerun above found Malachi's base chapters
    unchanged, and the main page, read again at 16:04 and at 16:08 New York time, was still
    at revision 3103065. The display dry run at 16:08 gave one create, with no missing link
    or transcluded page, and its page equals the preview's byte for byte (run
    `.novc/mam-ws-bot-miqra-mevoar-display-runs/20261116-160805-558860-0500/`). The saving
    run at 16:08, with Stage 10's summary copied from this plan by script, created the page
    as revision 3103136, read it back equal to the generated text, and exited zero. A read
    after the run, without the bot's login, found the page with one revision, BDencklaBot's,
    not minor, with that summary, and the creation and its category entry with the bot flag.
    A dry rerun found it unchanged, with no missing link or transcluded page, and exited zero.
    `py/ws/ws_bot_edit_history.md` has the entry, with the run directories, and the decision
    page marks decisions 1 and 2 answered and carried out. Each of the Twelve now has its
    display page.
  - **Stage 11's word.** Ben's 3a is his word to execute Stage 11. By his rule a fresh session
    executes it, not the round 2 session that wrote it: its standalone prompt, written for
    the commander, is
    `C:/Users/BenDe/AppData/Local/Claude-Data/claude_pzs8sxrjxfjjc/side-session-notes/local_a80ded65-f78e-4280-8493-9dab3b8c5686/miqra-mevoar-stage-11-prompt-2026-11-16.md`,
    and the decision page marks decision 3 answered.
- **Stage 11, the display pages of Judges and Daniel, 2026-11-16:** the commander started a
  fresh Claude (Opus 5.5) session with a brief that carries Stage 11's prompt, saved as
  `C:/Users/BenDe/GitRepos/MAM-basics/.novc/commander-session/miqra-mevoar-stage-11-brief-2026-11-16.md`,
  SHA-256 `9B78EC922D9FB129FB69DDAF4B772270B318794CA90BB6C277796E5C3092C5EA`. Its checkout,
  `C:/Users/BenDe/GitRepos2/MAM-basics`, was verified at 16:56 New York time: on `main`, clean,
  at `8cc22b46348651dd6e2f04c6a013e77157026ded`, level with origin, with no other session
  working in it. The session's scripts and evidence are in
  `.novc/miqra-mevoar-stage-11-2026-11-16/`.
  - **The main page,** read again by script at 16:59 New York time, was still at revision
    3103065, its text equal to round 2's kept copy, and linked exactly the five names.
  - **The generator,** `py/miqra_mevoar/display_page.py`, as the stage's design gives it:
    `Page` gained `first_verse` and `last_verse`; `_page_keys` takes a page's verses from its
    first bound to its last, and raises if either bound is not a verse of the book or if the
    verses between them are not in MAM-simple's order; `Verse` gained `chapter_parameter`,
    which `page_verses` sets on a page's first verse alone, where its verse number is not 1;
    `_text` writes the parameter; and `read_page` accepts it only on a page's first verse
    line, with that line's own chapter numeral, at a verse other than alef. A script,
    `scripts/apply_stage_11.py` in that folder, copied the parameter's name from the Noah
    page's revision 964086, checked it against the verse template's text in revision 2852518,
    copied the five names from revision 3103065 and parsed each link's label into its part's
    range: Judges 1:1 to 2:5, 2:6 to 16:31 and 17 to 21, and Daniel 1 to 6 and 7 to 12. The
    same parser gives Joshua's two links the table's ranges. Judges' three entries follow
    Joshua's, and Daniel's two follow Malachi's. The module docstring and the table's comment
    say so, and now also name Malachi, which round 2 added to the table.
  - **The test,** `py/tests/test_miqra_mevoar_display.py`: `_expected_verses` takes a page's
    verses from its first bound to its last, as their osisIDs give them, and gives the first
    of them the chapter parameter exactly where its verse number is not 1. The test of a
    book's pages now covers Judges' three and Daniel's two.
  - **Unchanged:** the generated text of each of the 14 pages already in the table, byte for
    byte, written by a script before and after the change. Daniel's two pages and Judges'
    third equal byte for byte those that Stage 10's generator made offline in round 2.
  - **Checks:** `git diff --check`; Black on the two changed Python files; Stage 11's
    verification command (135 passed). The mega and the full suite were skipped: the mega
    runs none of this code, and the generator is imported only by its bot mode and two
    tests, all in that command.
  - **Pushed** as `4c0d5efc`.
  - **The dry runs,** from that commit, after a check that no `main_ws_bot.py` process was
    running and no other session of the commander's family was doing bot work. The main
    page, read again at 17:09 New York time, was still at revision 3103065 and linked the
    five names. A `miqra-mevoar --no-save` run over `sephershoftim` and `daniyel` found all
    33 base chapters unchanged (run
    `.novc/mam-ws-bot-miqra-mevoar-runs/20261116-170926-478759-0500/`).
    1. **Daniel's two pages,** at 17:09: two creates, with no missing link or transcluded
       page (run `.novc/mam-ws-bot-miqra-mevoar-display-runs/20261116-170945-588565-0500/`).
    2. **Judges' three pages,** at 17:10: three creates, with no missing link or
       transcluded page (run
       `.novc/mam-ws-bot-miqra-mevoar-display-runs/20261116-171004-529582-0500/`).

    Each of the five pages has the counts of Stage 11's table and equals byte for byte the
    page that the generator wrote for the comparison after the change; Daniel's two and
    Judges' third also equal round 2's offline pages. Judges' second part opens with the two
    lines that Stage 11 quotes, its first part ends at 2:5, and no other line of the three
    gives the chapter parameter.
  - **The decision page,** an artifact, https://claude.ai/artifact/WfkABxxnxSCqKmtGsu1PUS,
    built by script from the dry runs, the kept main page and this plan, puts two decisions
    to Ben: 1, the save of Daniel's two pages, and 2, the save of Judges' three, each in one
    run with Stage 10's summary, recommended now, after a fresh check of the preconditions
    and a fresh dry run that gives the same pages.
  - **Pushed** as `ec211fa8`.
  - **Ben's word,** in this session before 17:25 New York time, answering the decision page:
    "Do 1a and 2a". So Daniel's two pages and then Judges' three were saved, each in one run
    with Stage 10's summary, after a fresh check of the preconditions and a fresh dry run.
  - **Daniel's save.** Before it, no `main_ws_bot.py` process was running, and of the
    commander's family only the session looking for a process that hogs the machine's
    resources and the session on the morphhb page were working, neither on bot work. The
    main page, read again at 17:25 New York time, was still at revision 3103065 and linked
    the five names, and a `miqra-mevoar --no-save` run found the 33 base chapters of Judges
    and Daniel unchanged (run
    `.novc/mam-ws-bot-miqra-mevoar-runs/20261116-172530-530303-0500/`). The dry run at 17:25
    gave two creates, with no missing link or transcluded page, and pages equal to those of
    17:09 byte for byte (run
    `.novc/mam-ws-bot-miqra-mevoar-display-runs/20261116-172556-318807-0500/`). The saving
    run at 17:26, with Stage 10's summary copied from this plan by script, created Daniel 1
    to 6 and 7 to 12 as revisions 3103153 and 3103154, read each back equal to the generated
    text, and exited zero; its pages equal the dry run's byte for byte. A read after the
    run, without the bot's login, found each page with one revision, BDencklaBot's, not
    minor, with that summary, and each creation and its category entry with the bot flag. A
    dry rerun found both unchanged, with no missing link or transcluded page, and exited
    zero.
  - **Judges' save.** Before it, the main page, read again at 17:27, was still at revision
    3103065; a `miqra-mevoar --no-save` run found Judges' 21 base chapters unchanged (run
    `.novc/mam-ws-bot-miqra-mevoar-runs/20261116-172722-680784-0500/`); and the dry run at
    17:27 gave three creates, with no missing link or transcluded page, and pages equal to
    those of 17:10 byte for byte (run
    `.novc/mam-ws-bot-miqra-mevoar-display-runs/20261116-172733-004691-0500/`). No
    `main_ws_bot.py` process was running, and the same two sessions of the family were
    working, neither on bot work. The saving run, from 17:27 to 17:28 with Stage 10's
    summary copied from this plan by script, created Judges 1:1 to 2:5, 2:6 to 16:31 and 17
    to 21 as revisions 3103155 to 3103157, read each back equal to the generated text, and
    exited zero; its pages equal the dry run's byte for byte. A read after the run, without
    the bot's login, found each page with one revision, BDencklaBot's, not minor, with that
    summary, and each creation and its category entry with the bot flag. A dry rerun found
    all three unchanged, with no missing link or transcluded page, and exited zero.
    `py/ws/ws_bot_edit_history.md` has an entry for each of the two saves, with the run
    directories, and the decision page marks both decisions answered and carried out.
  - **The email to Avi,** which Ben asked this session for on 2026-11-17, before 09:05 New
    York time, is drafted for him to send. It reports round 2's saves and this stage's; that
    Judges' second part numbers its chapter on its first verse, as the Noah page does; that
    the parts of Judges and Daniel have no title and navigation block; that the pictures are
    left out; that the converter reads the corrected files' new style names; and that Judges
    repeats a heading before 15:1 and 16:23, which Avi may mention to Rabbi Kokhav with
    Micah's. It asks Avi nothing. The draft is
    `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/miqra-mevoar-stage-11-2026-11-16/email-to-avi-2026-11-17.md`,
    with its copyable page beside it, both built by `scripts/build_email_to_avi.py` in that
    folder, which takes each page's title from the verified saves of round 1, round 2 and this
    stage and the repeated heading from the tracked JSON.
- **Stage 12, the display pages of the Torah, 2026-11-22:** Ben's request (decisions ledger
  entry 16) reached a fresh Claude (Opus 5.5) session that the commander started with a brief
  saved as
  `C:/Users/BenDe/GitRepos/MAM-basics/.novc/commander-session/miqra-mevoar-torah-brief-2026-11-22.md`.
  Its checkout, `D:/GitRepos5/MAM-basics`, on the D: drive as Ben asked, was verified before
  this stage's first edit: on `main`, clean, at `3bc9510ef68507f156a9ce98afa370feb475a1d1`,
  level with origin after a fetch, with no other session working in it. The session's scripts
  and evidence are in that clone's `.novc/miqra-mevoar-torah-2026-11-22/`.
  - **The reads,** anonymous, saving nothing: the main page's latest revision, 3103840,
    Dovi's of 2026-11-21 at 16:32 New York time, which links 15 part pages from its section of
    the Torah, all of them red, beside Avi's 54 pages of the weekly portions; and, at 09:18 New
    York time on 2026-11-22, those 15 titles, the 54 pages, the Torah's 187 base chapters and
    the 19 pages of the display table (`wikisource/torah-read-20261122T141807Z/`). Two pages of
    the table are no longer the bot's text alone: Joshua's first part, whose block Dovi
    reworked on 2026-11-21 (revision 3103803), and Judges' second, to which Dovi added two
    pictures the same day (revision 3103757).
  - **The weekly-portion pages,** compared with MAM-simple and the base chapters by
    `scripts/analyze_torah_read.py` (`survey/torah-read-analysis.txt`): besides the three line
    shapes, each has a title template, the aliyot's headings, blank lines and a category of
    its portion. Beyond those, they set the Decalogue through Avi's templates, give two
    petuhot of Tzav a note, and carry three headings of Numbers in the verse template. Their
    breaks and headings differ from MAM-simple's and the base chapters' at a few places, five
    of them heading lines that transclude from another book's or another chapter's base
    chapter. Stage 12 follows MAM-simple and the base chapters, as Stage 10's choice 1 does.
  - **Stage 12,** written into this plan as planning, with its four open choices, and pushed
    as `45a975f7`.
  - **The code,** made by a subagent of this session from the stage's text, as its design items
    1 to 3 and 5 give it, with recommendations 1a, 2a and 3a: `f910d8b3`, the heading places and
    the subcommand `py/main_miqra_mevoar.py base-headings`, whose one run, ending at 10:04 New
    York time, parsed all 187 base chapters and recorded 443 headings, equal to an independent
    reading of the pages kept at 09:18; and `a65a91d1`, the generator, the display table's 15
    entries, the bot mode's counts and the test. The 19 pages already in the table generate
    byte for byte as before, and the 124 base chapters that `pages` writes are unchanged.
    Checks: `git diff --check`; Black on the changed Python files; Stage 11's verification
    command with `py/tests/test_product_scopes.py` added (159 passed). Pushed as `a65a91d1`.
  - **The dry run,** at 10:36 New York time, after a check that no `main_ws_bot.py` process was
    running and that no session of the commander's family was doing bot work. Before it,
    `base-headings --check` found every heading where the records have it, with no revision
    changed, and the main page, read again, was still at revision 3103840, with the same 15
    links and labels. `miqra-mevoar-display --no-save` over the 15 pages gave 15 creates, each
    with the stage's counts and with no missing link or transcluded page, and each equal byte
    for byte to the subagent's offline page (run
    `.novc/mam-ws-bot-miqra-mevoar-display-runs/20261122-103600-150955-0500/`).
  - **The decision page,** an artifact, https://claude.ai/artifact/XYchLEVJdwMQh5FM3wDJHN,
    puts to Ben decisions 1 to 4 and two saving runs, each recommended now, after a fresh
    check of the preconditions and a fresh dry run that gives the same pages: decision 5, run
    A, the nine pages that no decision changes, and decision 6, run B, the four that decisions
    2 and 3 shape. Run C, Genesis' and Exodus' first parts, waits on decision 1.
  - **Paused,** on Ben's word before 10:45 New York time (decisions ledger entry 17): the
    stage's decisions 1 to 4 go to Avi in an email drafted for Ben to send, and its saving runs
    wait until the work resumes (Stage 12, “Resuming Stage 12”).
  - **The email to Avi** went out: Ben, in this session at about 11:26 New York time: “I have
    sent the email to Avi.” It is the draft
    `.novc/miqra-mevoar-torah-2026-11-22/email-2026-11-22/email-to-avi-2026-11-22.md` of
    `D:/GitRepos5/MAM-basics`, built with its copyable page by `scripts/build_email.py` in that
    folder. It apologizes, as Ben asked (decisions ledger entry 17), that he relays these
    questions instead of deciding them himself; asks Avi the stage's four questions, each with
    the choice that the pages follow unless he prefers another; and lists the slips found on
    his weekly-portion pages. Stage 12 then waited on his answers.
- **Stage 12 resumed, 2026-11-22:** Ben's message of decisions ledger entry 18 reached a fresh
  Claude (Opus 5.5) session that the commander started with a brief saved as
  `C:/Users/BenDe/GitRepos/MAM-basics/.novc/commander-session/miqra-mevoar-torah-resume-brief-2026-11-22.md`.
  Its checkout, `D:/GitRepos5/MAM-basics`, was verified before its first edit: on `main`,
  clean, at `d541ec755ad1c5aa9bd053a87532e8c60816ff55`, with no other session working in it,
  and fast-forwarded to origin's `aeec88eab432487ed0f6ada4cf614c3a47e958c3`. Its scripts and
  evidence are in that clone's `.novc/miqra-mevoar-torah-2026-11-22/resume/`.
  - **The reads,** anonymous, saving nothing: the main page's latest revision, 3104053,
    Dovi's of 16:08 New York time; and, at 20:24, the Torah's 15 part titles, its 54
    weekly-portion pages, its 187 base chapters and the 34 pages of the display table
    (`resume/wikisource/torah-read-20261123T012439Z/`). None of the 15 part pages exists, and
    no page of the table has changed since the reads of 2026-11-22 at 09:18.
  - **Decision 1.** The labels of revision 3104053, parsed by Stage 12's parser, give Genesis'
    first part chapters 1 to 11 and Exodus' first part chapters 1 to 17, the ranges that
    `display_page.PAGES` already gives them; the other 13 labels are those of revision
    3103840, and each of the 15 gives its page's range in the table
    (`resume/survey/labels-3104053.txt`). The table is unchanged, and its comments no longer
    call the two ranges pending.
  - **The five slips,** each fixed on its live page, by Dovi, between 16:13 and 16:24 New York
    time (`resume/survey/slips.txt`): Naso's heading before Numbers 5:1 now transcludes from
    the base chapter of chapter 5 (revision 3104057); Devarim's before Deuteronomy 2:2, 2:9 and
    2:17 from that of Deuteronomy 2 (3104059); Shoftim's before 19:1 from that of chapter 19,
    with the heading of 18:9 now before 18:9 and no break line before 18:19 (3104063); Ki
    Tetze's heading before 22:6 stands inside its template (3104067); and the verse line of
    Leviticus 21:20 in its base chapter holds no tag but its own (3104069). The analysis of
    2026-11-22, rerun on the new read, no longer finds the first four
    (`resume/survey/analysis-diff.txt`).
  - **Decisions 2 and 3.** Avi's pages of Yitro, Va'etchanan, Ki Tisa and Tzav are still at
    revisions 962744, 962961, 966044 and 966718, from which the code copied the Decalogue's
    templates and the disputed petuhot's first parameters, so 2a and 3a need no change.
  - **A comparison newly possible.** The rerun analysis now reads the breaks of Exodus and
    Leviticus, since Stage 12's `mam_simple.verse_breaks` reads the nested petuhot instead of
    raising on them, so it compares those books' weekly-portion pages too. Besides the
    disputed petuhot, which Tzav shows as decision 3a has them, it finds four breaks where
    Avi's pages differ from MAM-simple, of the kind that it found in the other three books on
    2026-11-22 and that the email did not list: a petuha before Exodus 34:11, where MAM-simple
    has no break; petuhot before Leviticus 13:38 and 13:40, where it has setumot; and a
    petuha before Leviticus 23:5, where it has one before 23:4
    (`resume/survey/new-breaks.txt`). The display pages follow MAM-simple there, as
    everywhere (Stage 10's choice 1).
  - **The heading places.** `base-headings --check`, ending at 20:37 New York time, parsed all
    187 base chapters and found every heading where the records have it. Only Leviticus 21's
    revision had changed, and the check reported no stray tag, where on 2026-11-22 it
    reported verse 1's end tag inside verse 20's line. Since that base chapter is an input of
    the hand-run `base-headings`, the session ran it again, ending at 20:39: its one change to
    the records is Leviticus 21's revision id, 3009315 to 3104069.
  - **Pushed** as `23e17b23`, with a merge of origin's `aca80dd5`, as `40cf4d7a`.
  - **Stage 13,** written into this plan as planning, with its three open choices, decisions 7
    to 9 of the decision page, from read-only measurements of the same reads: Joshua's first
    part is Dovi's block before the bot's text, byte for byte, and its block is its name, its
    18 headings and its 12 chapters (`resume/survey/joshua-1-block-check.txt`); 441 of the
    Torah's 443 headings begin with the same word (`resume/survey/first-words.txt`); and of the
    six parts made without a block, all but Judges' second still hold the bot's text alone
    (`resume/scripts/compare_table_pages.py`). Pushed as `a6632256`.
  - **The dry run,** from that commit, at 20:55 New York time, after a check that no
    `main_ws_bot.py` process was running and that no session of the commander's family was
    doing bot work. Before it, the main page, read again at 20:54, was still at revision
    3104053, with the same 15 links and labels (`resume/scripts/check_main_page.py`), and
    `base-headings --check`, ending at 20:55, found every heading where the records have it,
    with no revision changed. `miqra-mevoar-display --no-save` over the 15 pages gave 15
    creates, each with Stage 12's counts and with no missing link or transcluded page, and
    each equal byte for byte to the page of the dry run of 10:36 and to Stage 12's offline page
    (run `.novc/mam-ws-bot-miqra-mevoar-display-runs/20261122-205552-105959-0500/`).
  - **The decision page,** https://claude.ai/artifact/XYchLEVJdwMQh5FM3wDJHN, rebuilt by
    `resume/decision-page/build_page.py`, reports the checks above and puts Stage 13's decisions
    7 to 9 to Ben, each recommending (a); under 7b it puts to him one saving run of the 15
    pages without blocks, with Stage 10's summary. Nothing is saved on Wikisource.
  - **Stage 13's executor's prompt** is
    `C:/Users/BenDe/AppData/Local/Claude-Data/claude_pzs8sxrjxfjjc/side-session-notes/local_a80ded65-f78e-4280-8493-9dab3b8c5686/miqra-mevoar-stage-13-prompt-2026-11-22.md`,
    sent to the commander, to start once this ledger records Ben's answers to decisions 7 to 9.

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

## Stage 11. The display pages of Judges and Daniel, on Ben's word

The round 2 session wrote this stage on 2026-11-16 (execution ledger, “Round 2, after Avi's
answers”), after Avi answered the fourth question of Ben's email of that day by linking display
pages for Judges and Daniel from the main page (Deferred, “Avi's answers to Ben's email of
2026-11-16”). By Ben's rule a fresh session executes it, not the session that wrote it, and it
stays planning only until he gives his word to execute it; each saving run needs his word too.
The design is that session's proposal: Ben's word to execute approves it, and he may change any
of it first, the scope included.

**What it does.** BDencklaBot creates the five display pages that the main page `מקרא מבואר` links
for Judges and Daniel, in the form of Stage 10's pages: Judges in three parts and Daniel in two,
as Avi divided them. It only creates pages; it never edits one. One part begins inside a chapter,
which Stage 10's generator refuses, so the stage first gives the generator the parameter with
which Avi's parasha pages number the chapter that a page begins inside.

**The pages,** keyed as the bot mode names them, with the names that the main page links in
revision 3103065, Dovi's of 2026-11-16 at 14:54 New York time, copied from that revision by script, and
the ranges that each link's label gives, parsed by script:

1. `sephershoftim-1`: `מקרא מבואר/תצוגה/ספר שופטים 1`, Judges 1:1 to 2:5.
2. `sephershoftim-2`: `מקרא מבואר/תצוגה/ספר שופטים 2`, Judges 2:6 to 16:31.
3. `sephershoftim-3`: `מקרא מבואר/תצוגה/ספר שופטים 3`, Judges 17 to 21.
4. `daniyel-1`: `מקרא מבואר/תצוגה/ספר דניאל 1`, Daniel 1 to 6.
5. `daniyel-2`: `מקרא מבואר/תצוגה/ספר דניאל 2`, Daniel 7 to 12.

Judges' links stand in the main page's section `==ספרי הנביאים==` and Daniel's in `==ספרי הכתובים==`. The
revision changed nothing else since 3101507, which round 1 read
(`.novc/miqra-mevoar-round-2-2026-11-16/wikisource/diff-3101507-3103065.txt`). The keys follow
Joshua's: the Word file's stem and the part's number. The parser of the labels gives Joshua's
two links the table's ranges, 1 to 12 and 13 to 24.

**A page that begins inside a chapter.** Avi's parasha pages begin where a parasha does. The page
of parashat Noah, `מקרא מבואר/תצוגה/ספר בראשית/פרשת נח`, read at revision 964086, begins its text at Genesis 6:9, after a
title template and the heading of its first section, with these two lines:

- a break line with both parameters: `{{פרשה במקרא מבואר|פרשה=פ|כותרת={{#קטע:מקרא מבואר/פרקי בסיס/ספר בראשית/ו|כותרת ט}}}}`;
- its first verse line: `{{מקרא מבואר|בראשית|ו|ט|פרק=ו}}`.

Its first verse line, and only that one of its 153 verse lines, gives the parameter `פרק=`,
whose value is the chapter's numeral; its later sections, some of which begin inside a chapter,
as its third does at 7:17, do not. The verse template, read at revision 2852518, shows the
parameter's value as the chapter's numeral where it is given, and otherwise shows the chapter's
numeral only at a verse numbered alef. So `sephershoftim-2` opens with these two lines:

- a break line with both parameters: `{{פרשה במקרא מבואר|פרשה=פ|כותרת={{#קטע:מקרא מבואר/פרקי בסיס/ספר שופטים/ב|כותרת ו}}}}`;
- its first verse line: `{{מקרא מבואר|שופטים|ב|ו|פרק=ב}}`.

**Choices,** each a proposal that Ben's word approves:

1. **The ranges and names follow the main page's links,** copied and parsed by script.
2. **The parameter `פרק=` stands on a page's first verse line only, and only where that verse
   is not its chapter's first,** with the chapter's numeral, as on the Noah page. No other line
   takes it.
3. **A break before a page's first verse is shown,** as Stage 10's choice 2 has it. MAM-simple has
   a petuha before Judges 2:6, before Judges 17:1 and before Daniel 7:1, and the tracked JSON
   gives each of those verses a heading, so each later part opens with a break line that has
   both parameters, as Joshua's second part does. `sephershoftim-1` ends at 2:5, before that
   petuha.
4. **A break inside a verse gets no line,** as Stage 10's choice 3 has it. MAM-simple's Judges has
   one, a petuha inside 2:1, on `sephershoftim-1`; Daniel has none.
5. **Sort keys** are the pages' own names, as Stage 10's choice 4 has it.
6. **No title and navigation block.** The bot's pages carry the three line shapes and nothing
   else, as Joshua's two parts did when the bot created them. Avi's model for the parts of large
   books (Deferred, “The parts of large books”) is his to add, as he did on Joshua's first part,
   unless Ben decides that the bot should make it: an open question for Ben, which this stage
   does not settle.

**Counts,** measured on 2026-11-16 from MAM-simple and `in/miqra-mevoar/` at `9b2d8909`, by a
scratch walk of MAM-simple and the tracked JSON, `in/miqra-mevoar/sephershoftim.json` and
`in/miqra-mevoar/daniyel.json`, that shares no code
with the generator (`.novc/miqra-mevoar-round-2-2026-11-16/stage-11/walk-counts.txt`). The walk
gives Stage 10's counts for Jonah and round 1's for Zephaniah, and agrees with the
starts-with-sampe field of every verse but each book's first in Joshua, Judges, Daniel, Jonah
and Zephaniah. Stage 10's generator, run
offline on the three parts that begin at a chapter, gives the same counts and raises on nothing
in either book (`.novc/miqra-mevoar-round-2-2026-11-16/stage-11/gen-offline.txt`). The dry run's
pages must have them:

| Page | Verse lines | Petuhot, setumot | Headings | Break lines: break only, heading only, both |
|---|---|---|---|---|
| Judges 1:1 to 2:5 | 41 | 5, 4 | 6 | 4, 1, 5 |
| Judges 2:6 to 16:31 | 430 | 51, 8 | 37 | 22, 0, 37 |
| Judges 17 to 21 | 147 | 17, 2 | 8 | 11, 0, 8 |
| Daniel 1 to 6 | 196 | 10, 11 | 7 | 15, 1, 6 |
| Daniel 7 to 12 | 161 | 7, 1 | 7 | 1, 0, 7 |

In all: 975 verse lines, 116 breaks, 65 headings and 118 break lines. Judges' three pages hold
its 618 verses and 51 headings, and Daniel's two its 357 verses and 14 headings.

**The design.**

1. **Generator,** `py/miqra_mevoar/display_page.py`:
   - `Page` gains `first_verse: int = 1`, the verse of its first chapter at which the page
     begins, and `last_verse: int | None = None`, the verse of its last chapter at which it
     ends, or None for that chapter's last. Every entry already in `PAGES` stays as it is.
     `sephershoftim-1` has the chapters (1, 2) and `last_verse=5`; `sephershoftim-2` has the
     chapters (2, 16) and `first_verse=6`.
   - `_page_keys` takes the book's verses from its first bound to its last, raises if either
     bound is not a verse of the book, as it now raises on a chapter outside the book, and
     requires the page to begin at its first bound, as it now requires a chapter's first verse.
   - `Verse` gains `chapter_parameter: str | None = None`, the chapter's numeral, which
     `page_verses` sets on a page's first verse alone, and only where that verse is not its
     chapter's first.
   - `_text` writes `|פרק=` and that numeral before a verse line's closing braces where the
     verse has it.
   - `read_page`, the closed parser, accepts the parameter only on a page's first verse line,
     only with that line's own chapter numeral and only where its verse is not alef, and raises
     on it anywhere else; every other line is still one of the three shapes.
   - The parameter's name is a constant beside the template's, copied by script from the Noah
     page's revision 964086 and checked against the template's text in revision 2852518.
   - `PAGES` gains the five entries, their names copied by script from revision 3103065. The
     module docstring and the table's comment say so, and the docstring's sentence that no line
     needs the parameter gives way to choice 2.
2. **Bot mode,** `py/main_ws_bot.py miqra-mevoar-display`: unchanged. Each run names its pages
   with `--page`, since a run over the whole table refuses Joshua's part one, which carries
   Avi's model (“Later Word files”).
3. **Test,** `py/tests/test_miqra_mevoar_display.py`, differential:
   - `_expected_verses` takes the page's verses from its first bound to its last, as
     MAM-simple's osisIDs give them, rather than its chapters, and gives the first of them the
     chapter parameter exactly where its verse number, from its osisID, is not 1.
   - `test_the_pages_of_a_book_show_it_once` then checks that Judges' three pages and Daniel's
     two show each book's verses once each, in order, the boundary between 2:5 and 2:6 included.
   - The generated pages, read back through `read_page`, are the test of the parser's new
     acceptance; no example test is added.

**Preconditions,** before the dry run and again before the save:

- The base chapters exist: Judges' 21, created by their own saving run on Ben's word, and
  Daniel's 12, created on 2026-11-16 as revisions 3103073 to 3103086. While Judges' do not
  exist, the dry run's parse check finds its pages' links to them missing. Daniel's two pages
  need not wait for Judges': a run may name only them.
- A `miqra-mevoar --no-save` run over `sephershoftim` and `daniyel` finds all 33 base chapters
  unchanged, since the places of the headings come from the tracked JSON. If one differs, stop
  and report it to Ben.
- The main page's latest revision, read again by script, still links the five names. If it
  does not, stop and report it.
- No `main_ws_bot.py` process runs, and no other session of the commander's family does bot
  work.

**Verification,** focused, under `doc/review-trial.md`: `git diff --check`; Black on the changed
Python files; and Stage 10's targeted tests with `py/tests/test_miqra_mevoar_save_receipts.py`
added:

```powershell
./.venv/Scripts/python.exe py/main_test.py py/tests/test_miqra_mevoar_display.py py/tests/test_miqra_mevoar_versification.py py/tests/test_miqra_mevoar_index.py py/tests/test_miqra_mevoar_bot_revision_guard.py py/tests/test_mega_coverage.py py/tests/test_entry_point_subcommands.py py/tests/source_hygiene_test.py py/tests/test_prose_conventions.py py/tests/test_transliterations.py py/tests/test_explicit_time_zones.py py/tests/test_stderr_error_handler.py py/tests/test_h_dot_below_nfc.py py/tests/test_prose_mark_order.py py/tests/test_tracked_filenames.py py/tests/test_miqra_mevoar_save_receipts.py
```

Expected unchanged: the generated text of every page already in `PAGES`, byte for byte,
compared by a scratch script before and after the change; every product directory that
`py/product_scopes.py` declares, `in/miqra-mevoar/`, `in/mam-ws/` and `in/mam-ws-bot-edits/`. The
mega runs none of this code; the last pushed commit's message says what was skipped and why.

**The dry run and the save.** Run `--no-save` with `--page` naming the five pages, or Daniel's two
alone while Judges' base chapters do not exist. Compare each page with the counts above, and read
its first two lines and its last. `daniyel-1`, `daniyel-2` and `sephershoftim-3` must equal byte
for byte the pages that Stage 10's generator made offline,
`.novc/miqra-mevoar-round-2-2026-11-16/stage-11/generated/`. Report the creates, the counts, the
parse check and the run directory to Ben; then stop. Each save needs his explicit word for that
run, with Stage 10's summary, copied from the plan by script through round 1's launcher,
`.novc/miqra-mevoar-round-1-2026-11-16/scripts/run_bot_with_plan_summary.py display`. After it,
a read after the run, and a dry rerun that finds every page unchanged; then an entry in
`py/ws/ws_bot_edit_history.md`, the execution ledger and the State. Commit, fetch, merge
`origin/main` if it moved, and push.

**Checkout and coordination,** as for Stage 10: a full MAM-basics clone that the commander
assigns, verified clean on `main` at the commit that added this stage or a descendant, with
`git merge-base --is-ancestor`; its own `.venv/Scripts/python.exe`, run from its root; and
`-c safe.directory=<clone>` on every Git call. The stage reads MAM-simple, the tracked JSON and
the live pages; its untracked inputs, the kept responses and the offline pages under
`.novc/miqra-mevoar-round-2-2026-11-16/`, are in `C:/Users/BenDe/GitRepos2/MAM-basics` alone.

## Stage 12. The display pages of the Torah, on Ben's word

This session wrote this stage on 2026-11-22 (execution ledger, “Stage 12, the display pages
of the Torah”), after Avi asked, in an email that Ben pasted into the commander session, for
the display pages of the five books of the Torah that his main page now links in parts
(decisions ledger entry 16). Ben's request is his word to plan the stage and to execute it in
this one session, which he asked to do the work and then to draft the reply; a subagent of
this session, given this stage's text as a fresh executor, makes the code change. Each saving
run still needs Ben's word for that run (decisions ledger entry 3). The design is this
session's proposal. The four choices that neither the plan nor Ben's words settled went to
Avi (decisions ledger entry 17), and his answers, which Ben relayed the same evening, settle
them (entry 18): decisions 1 to 3 as the code has them, and 4b, which Stage 13 plans.

**What it does.** BDencklaBot creates the 15 display pages that the main page `מקרא מבואר` links
from its section `==ספרי התורה==` in revision 3103840, Dovi's of 2026-11-21 at 16:32 New York
time, in the form of Stage 10's and Stage 11's pages: each book in three parts, as Avi divided
it. It only creates pages; it never edits one. Avi's 54 pages of the weekly portions, which the
same section links, stay as they are: no page of this stage has one of their titles.

**The pages,** keyed as the bot mode names them, by the book's OSIS abbreviation in lower case
and the part's number, with the names that the main page links, copied from that revision by
script, and the ranges that each link's label gives, parsed by script, as revision 3104053
gives them for `gen-1` and `exod-1`, whose labels Avi corrected there (decision 1):

1. `gen-1`: `מקרא מבואר/תצוגה/ספר בראשית 1`, Genesis 1 to 11, as its label has given since revision 3104053 (decision 1).
2. `gen-2`: `מקרא מבואר/תצוגה/ספר בראשית 2`, Genesis 12 to 36.
3. `gen-3`: `מקרא מבואר/תצוגה/ספר בראשית 3`, Genesis 37 to 50.
4. `exod-1`: `מקרא מבואר/תצוגה/ספר שמות 1`, Exodus 1 to 17, as its label has given since revision 3104053 (decision 1).
5. `exod-2`: `מקרא מבואר/תצוגה/ספר שמות 2`, Exodus 18 to 24.
6. `exod-3`: `מקרא מבואר/תצוגה/ספר שמות 3`, Exodus 25 to 40.
7. `lev-1`: `מקרא מבואר/תצוגה/ספר ויקרא 1`, Leviticus 1 to 10.
8. `lev-2`: `מקרא מבואר/תצוגה/ספר ויקרא 2`, Leviticus 11 to 18.
9. `lev-3`: `מקרא מבואר/תצוגה/ספר ויקרא 3`, Leviticus 19 to 27.
10. `num-1`: `מקרא מבואר/תצוגה/ספר במדבר 1`, Numbers 1 to 10.
11. `num-2`: `מקרא מבואר/תצוגה/ספר במדבר 2`, Numbers 11:1 to 22:1.
12. `num-3`: `מקרא מבואר/תצוגה/ספר במדבר 3`, Numbers 22:2 to 36:13.
13. `deut-1`: `מקרא מבואר/תצוגה/ספר דברים 1`, Deuteronomy 1:1 to 11:25.
14. `deut-2`: `מקרא מבואר/תצוגה/ספר דברים 2`, Deuteronomy 11:26 to 26:19.
15. `deut-3`: `מקרא מבואר/תצוגה/ספר דברים 3`, Deuteronomy 27 to 34.

The keys follow no Word file, since the Torah reached Avi long ago as a single file that this
plan's converter never read; MAM-simple's OSIS abbreviations name the books without a new
transliteration. The parser of the labels is Stage 11's, which gives Joshua's, Judges' and
Daniel's links the table's ranges. Numbers 22:2 and Deuteronomy 11:26 begin inside a chapter,
so the first verse lines of `num-3` and `deut-2` give the chapter parameter, as Stage 11
provides.

**What the Torah brings that the other books did not,** measured on 2026-11-22 from MAM-simple
at `3bc9510e` and from the live pages, read anonymously at 09:18 New York time, saving nothing
(execution ledger, “Stage 12, the display pages of the Torah”):

1. **No tracked text.** `in/miqra-mevoar/` holds no book of the Torah. The Torah's 187 base
   chapters exist, made on Wikisource before this plan, and their latest revisions are
   ShalomOrobot's, 169 of them, and those of the account David Kochav, 18. So the places of
   the headings must come from the base chapters themselves: 443 heading sections, Genesis 92,
   Exodus 105, Leviticus 70, Numbers 72 and Deuteronomy 104.
2. **Line shapes that the bot's base chapters lack,** by a census of all 187
   (`survey/base-line-census.txt`): 41 blank lines, alone or in pairs, before the heading at
   the start of a weekly portion; a navigation-bar line, `{{סרגל ניווט|...}}`, before the chapter
   heading of Numbers 20; two spaces before the numeral in the chapter headings of Genesis 3
   and Exodus 4; a heading line without its leading `*`, before Deuteronomy 22:20; three soft
   hyphens after the end tag of the verse line of Exodus 21:34; and, inside the verse line of
   Leviticus 21:20, a stray end tag of verse 1's section, which changes neither verse's
   paraphrase, as an anonymous parse showed on 2026-11-22 (`survey/parse-lev-21.txt`). Each
   chapter has one verse section for each of MAM-simple's verses, in order, and each of its
   heading sections stands before the verse line of its own numeral.
3. **The Decalogue.** Avi's pages of Yitro and Va'etchanan set Exodus 20:2 to 20:12 and
   Deuteronomy 5:6 to 5:17, verse by verse, through templates that ShalomOrobot made for them
   in 2022: `{{מקרא מבואר/עשרת הדברות יתרו|...}}`
   and `{{מקרא מבואר/עשרת הדברות ואתחנן|...}}` with the verse's numeral, and, for Exodus 20:12 and Deuteronomy
   5:16, `{{מקרא מבואר/עשרת הדברות יתרו יב}}` and `{{מקרא מבואר/עשרת הדברות ואתחנן טז}}`. Each sets MAM's lower cantillation, the
   strand that the templates call תחתון, from MAM's page `עשרת הדברות בסיס/טעמים`, beside the
   base chapter's paraphrase. The verse template, given the same verses, sets MAM's text with
   both cantillations on one line, as MAM's chapter pages have it. An anonymous parse of both,
   on 2026-11-22, showed each (`survey/parse-decalogue.txt`). Decision 2.
4. **Three disputed petuhot.** MAM-simple nests a petuha in a scribal-difference element, with
   a note, at the end of Exodus 33:23 (ספק פרשה סתומה בכתר ארם צובה), of Leviticus 7:21
   (אין פרשה בספרי ספרד ואשכנז) and of Leviticus 7:27 (אין פרשה בספרי תימן). `mam_simple.verse_breaks` raises
   on each, as its closed dispatch requires; Stage 10's code found them. Avi's pages show a
   petuha alone before Exodus 34:1, and before Leviticus 7:22 and 7:28 a petuha with a note in
   parentheses: `פ (בספרי תימן)` and `פ (בספרי ספרד ואשכנז)`. Decision 3.
5. **Two labels that disagree with their neighbours.** By the labels, Genesis' first part,
   chapters 1 to 12, and its second, 12 to 36, both show chapter 12's 20 verses; and Exodus'
   first part, 1 to 11, and its second, 18 to 24, leave out chapters 12 to 17, 183 verses. Each
   second part begins where its book's weekly portions and its title begin a new subject.
   Decision 1. Avi corrected both first parts' labels on 2026-11-22, to chapters 1 to 11 and
   1 to 17, in the main page's revision 3104053 (decisions ledger entry 18).

**Choices.** Decisions 1 to 4 were Ben's, on the stage's decision page, until he passed them to
Avi on 2026-11-22 (decisions ledger entry 17). Avi's answers, which Ben relayed that evening
(entry 18), settle them: 1a, with the two labels corrected; 2a; 3a; and 4b, which Stage 13
plans. The code follows (a) for decisions 1 to 3:

1. **The first parts of Genesis and Exodus.** (a) The table gives `gen-1` chapters 1 to 11 and
   `exod-1` chapters 1 to 17, the chapters up to each second part's label, so that the dry run
   and the test cover every verse; they are saved only once Avi confirms those ranges, and the
   reply asks him to, and to correct the two labels. (b) Save them now with those ranges. (c)
   Follow the labels, showing chapter 12 of Genesis twice and Exodus 12 to 17 nowhere.
2. **The Decalogue.** (a) Avi's templates, as on his pages of Yitro and Va'etchanan: each verse
   by the template that his page gives it, with the break lines as MAM-simple gives them. (b)
   The verse template, which sets MAM's text with both cantillations.
3. **The three disputed petuhot.** (a) As Avi's pages show them: the petuha alone before Exodus
   34:1, and before Leviticus 7:22 and 7:28 the petuha with his note, copied by script from his
   page of Tzav. (b) The petuha alone at all three, as MAM's text has it. (c) No break line at
   any of them, as MAM-simple's starts-with-sampe fields have it.
4. **Avi's title and navigation block** (Deferred, “The parts of large books”). (a) None,
   as on Stage 11's pages; Avi adds it where he wants it, as he did on Joshua's first part. (b)
   The bot builds it from the page's headings and chapters.
5. **As on the earlier pages:** a break before a page's first verse is shown, a break inside a
   verse gets no line, and each page's sort key is its own name (Stage 10's choices 2 to 4); the
   chapter parameter stands on a page's first verse line alone, where that verse is not its
   chapter's first (Stage 11's choice 2).

**Counts,** measured on 2026-11-22 from MAM-simple at `3bc9510e` and the live base chapters by
a scratch walk that shares no code with the generator (`scripts/walk_torah.py`, whose output
is `survey/walk-torah.txt`), with decisions 1a and 3a; the Decalogue's lines are verse lines.
The dry run's pages must have them:

| Page | Verse lines | Petuhot, setumot | Headings | Break lines: break only, heading only, both |
|---|---|---|---|---|
| Genesis 1 to 11 | 299 | 14, 26 | 17 | 29, 6, 11 |
| Genesis 12 to 36 | 785 | 17, 13 | 49 | 1, 20, 29 |
| Genesis 37 to 50 | 449 | 11, 9 | 26 | 10, 16, 10 |
| Exodus 1 to 17 | 467 | 30, 20 | 37 | 15, 2, 35 |
| Exodus 18 to 24 | 192 | 10, 34 | 14 | 31, 1, 13 |
| Exodus 25 to 40 | 550 | 29, 37 | 54 | 14, 2, 52 |
| Leviticus 1 to 10 | 252 | 22, 10 | 24 | 10, 2, 22 |
| Leviticus 11 to 18 | 284 | 13, 21 | 23 | 15, 4, 19 |
| Leviticus 19 to 27 | 323 | 18, 15 | 23 | 12, 2, 21 |
| Numbers 1 to 10 | 420 | 46, 19 | 24 | 43, 2, 22 |
| Numbers 11:1 to 22:1 | 352 | 25, 14 | 28 | 14, 3, 25 |
| Numbers 22:2 to 36:13 | 516 | 20, 33 | 20 | 35, 2, 18 |
| Deuteronomy 1:1 to 11:25 | 337 | 11, 19 | 24 | 11, 5, 19 |
| Deuteronomy 11:26 to 26:19 | 352 | 11, 74 | 65 | 22, 2, 63 |
| Deuteronomy 27 to 34 | 266 | 12, 26 | 15 | 24, 1, 14 |

In all: 5,844 verse lines, among them 23 of the Decalogue; 659 breaks; 443 headings; and 729
break lines.

**The design.**

1. **The heading places,** `in/miqra-mevoar-base-headings/<OSIS abbreviation>.json`, one file
   for each book of the Torah, with a `README.md` beside them: for each chapter, its number,
   its base chapter's page id and revision id, and the verses before which it has a heading
   section, in order. No text of the base chapters is kept (decisions ledger entry 2). The
   module is `py/miqra_mevoar/base_headings.py`. It lists the books of the Torah, keyed by
   their OSIS abbreviations, each with its pair of names in `mam_bknas` and its MAM-simple
   file, and reads and writes a book's record, its shape checked.
2. **The subcommand,** `py/main_miqra_mevoar.py base-headings`, a hand-run generator like the
   others of that entry point: it reads the latest revision of each of the Torah's base
   chapters, anonymously, through `ws_revision_api.ChapterClient` and a
   `polite_download.PoliteDownloader`, a dozen titles to a request, since a request for 50 of
   these titles was refused as too long; it parses each by a closed parser and writes the
   records. The parser accepts, line by line, the chapter heading, as
   `wikitext.chapter_wikitext` writes it or with two spaces before the numeral; before it, the
   navigation-bar line, whose template's name is copied by script from Numbers 20; a heading
   line, with or without its leading `*`; a verse line, with or without trailing soft
   hyphens; a blank line; the category line, `wikitext.CATEGORY`; and no other line. Another
   section's tag inside a verse line, as on Leviticus 21:20, is reported rather than refused,
   since it moves no heading. The verse sections must be MAM-simple's verses of the chapter,
   in order, once each, and each heading line must stand directly before the verse line of
   its numeral, as every one of the 443 does. `base-headings --check`
   reads the same pages and writes nothing: it lists each chapter whose revision changed, and
   exits non-zero if any heading moved, appeared or vanished or if a page does not parse.
3. **Generator,** `py/miqra_mevoar/display_page.py`:
   - A `Page`'s `stem` names a book of `books.BOOKS`, by its Word file's stem, or of
     `base_headings`'s books, by its OSIS abbreviation; the two sets of keys are disjoint,
     which the module checks. A page's headings come from the tracked JSON for the first and
     from the heading places for the second.
   - `PAGES` gains the 15 entries, their names copied by script from revision 3103840 and their
     ranges parsed by script from its labels, except `gen-1` and `exod-1`, as decision 1 gives
     them. The module docstring and the table's comment say so.
   - **The Decalogue,** by decision 2a: a closed table, copied by script from Avi's pages of
     Yitro, revision 962744, and Va'etchanan, revision 962961, gives each of Exodus 20:2 to
     20:12 and Deuteronomy 5:6 to 5:17 its template and, where the template takes one, its
     numeral. That verse's line calls its template instead of the verse template; its break
     line, if any, is as for any verse. The generator raises if a page would begin at one of
     these verses, and the closed parser accepts such a call only at its verse.
   - **The disputed petuhot,** by decision 3a: `mam_simple.verse_breaks` reads a
     scribal-difference element that is a verse's last child and whose target holds one break
     and nothing else as that break, standing before the next verse; its closed dispatch still
     raises on any other nesting. A closed table, keyed by the three verses after them and
     checked against MAM's notes, gives each break line its first parameter: the petuha alone
     before Exodus 34:1, and Avi's two texts, copied by script from his page of Tzav, revision
     966718, before Leviticus 7:22 and 7:28. The parser accepts those texts only at those
     verses, and the bot mode's counts count them as petuhot.
   - Every entry already in `PAGES` keeps its text byte for byte: no book of theirs has a
     Decalogue or a scribal-difference element.
4. **Bot mode,** `py/main_ws_bot.py miqra-mevoar-display`: unchanged. Each run names its pages
   with `--page`, since a run over the whole table refuses Joshua's first part and Judges'
   second, which Dovi has edited.
5. **Test,** `py/tests/test_miqra_mevoar_display.py`, differential:
   - The oracle of a Torah page's headings is its book's file of heading places, read by the
     test's own reading of the JSON; for the other books it stays the tracked JSON.
   - The oracle of its breaks stays MAM-simple's starts-with-sampe field, with the disputed
     petuhot found by the test's own walk of MAM-simple's scribal-difference elements; each
     one it finds must be in the generator's table, and each in the table must be found.
   - A Decalogue line stands exactly at each verse of the generator's table, and the table's
     verses must be consecutive verses of MAM-simple's Exodus 20 and Deuteronomy 5.
   - The pages of each book of the Torah show its verses once each, in order, as the other
     books' pages do.
   - A missing input fails rather than skips.

**Preconditions,** before the dry run and again before each save:

- `py/main_miqra_mevoar.py base-headings --check` finds every heading of the pages' base
  chapters where the heading places have it. If one differs, stop and report it to Ben.
- The main page's latest revision, read again by script, still links the 15 names with the same
  labels. If it does not, stop and report it.
- No `main_ws_bot.py` process runs, and no other session of the commander's family does bot
  work.

**Verification,** focused, under `doc/review-trial.md`: `git diff --check`; Black on the changed
Python files; Stage 11's verification command, with any test that the new subcommand calls for
added; and one run of `py/main_miqra_mevoar.py base-headings`, whose tracked output is read.
Expected unchanged: the generated text of every page already in `PAGES`, byte for byte,
compared by a scratch script before and after the change; every product directory that
`py/product_scopes.py` declares; `in/miqra-mevoar/`, `in/mam-ws/` and `in/mam-ws-bot-edits/`.
The mega runs none of this code; the last pushed commit's message says what was skipped and why.

**The dry run and the saves.** Run `--no-save` with `--page` naming the 15 pages. Compare each
page with the counts above, and read its first two lines and its last. Report the creates, the
counts, the parse check and the run directory to Ben on the decision page; then stop. Three
saving runs, each on Ben's word for that run, with Stage 10's summary copied from this plan by
script through round 1's launcher, copied into this session's folder:

1. **Run A:** the nine pages that no decision changes, if decision 4 takes its
   recommendation: `gen-2`, `gen-3`, `lev-2`, `lev-3`, `num-1`, `num-2`,
   `num-3`, `deut-2` and `deut-3`.
2. **Run B:** `exod-2` and `deut-1`, which hold the Decalogue, and `exod-3` and `lev-1`, which
   hold the disputed petuhot, as decisions 2 and 3 have them.
3. **Run C:** `gen-1` and `exod-1`, once Avi confirms their ranges, or as Ben decides.

Avi has since confirmed the ranges and chosen 4b (decisions ledger entry 18), so these three
runs give way to Stage 13's decision 7: under 7a, Stage 13's executor creates the 15 pages with
their blocks, in one run; under 7b, the session that resumed this stage saves the 15 now,
without blocks, in one run with Stage 10's summary, on Ben's word for that run.

After each save, a read after the run, without the bot's login, and a dry rerun that finds every
saved page unchanged; then an entry in `py/ws/ws_bot_edit_history.md`, the execution ledger and
the State. Commit, fetch, merge `origin/main` if it moved, and push.

**The reply to Avi,** drafted for Ben once the pages that he approves are saved: it reports the
pages, asks Avi to confirm the ranges of Genesis' and Exodus' first parts and to correct their
labels, and says how the pages set the Decalogue and the disputed petuhot.

**Checkout and coordination:** `D:/GitRepos5/MAM-basics`, which the commander assigned to this
session, verified clean on `main` at `3bc9510e`, level with origin; its own
`.venv/Scripts/python.exe`, run from its root; and `-c safe.directory=D:/GitRepos5/MAM-basics`
on every Git call. The session releases the clone while it waits on Ben. Its untracked inputs
and evidence, the kept responses among them, are in `.novc/miqra-mevoar-torah-2026-11-22/` of
that clone alone.

**Resuming Stage 12.** On 2026-11-22 Ben paused the stage after its dry run (decisions ledger
entry 17). Done: the stage, pushed as `45a975f7`; its code, `f910d8b3` and `a65a91d1`; its dry
run; and the record of them, `c5a09ec0` (execution ledger, “Stage 12, the display pages of
the Torah”). Nothing is saved on Wikisource. Avi answered the four questions of the email that
the session drafted and Ben sent on 2026-11-22,
`D:/GitRepos5/MAM-basics/.novc/miqra-mevoar-torah-2026-11-22/email-2026-11-22/email-to-avi-2026-11-22.md`,
with its copyable page beside it, the same evening (decisions ledger entry 18), and a fresh
session resumed the stage (execution ledger, “Stage 12 resumed”); each saving run waits on
Ben's word for that run. The session that resumes:

1. Records Avi's answers, as Ben relays them, in the decisions ledger.
2. Changes the code only where an answer is not the recommendation, and keeps every other
   page of `display_page.PAGES` byte for byte, compared by a scratch script before and after:
   decision 1 is the ranges of `gen-1` and `exod-1` in `PAGES`, with their rows of the Counts
   table measured again; 2b removes `DECALOGUE` and its line shape; 3b or 3c changes
   `DISPUTED_PETUHOT` and the parser's acceptance of its texts; 4b needs a stage of its own,
   which is Stage 13.
   Then the focused checks of “Verification” above, a commit and a push.
3. Checks the preconditions and runs a fresh dry run, as “The dry run and the saves” says.
4. Puts each saving run to Ben with its pages, their count, its summary and a page to look
   at, on the stage's decision page, https://claude.ai/artifact/XYchLEVJdwMQh5FM3wDJHN, and
   saves only on his word for that run: run A, the nine pages that no decision changes; run
   B, `exod-2`, `exod-3`, `lev-1` and `deut-1`; and run C, `gen-1` and `exod-1`, once their
   ranges are settled. Since Avi chose 4b, these runs give way to Stage 13's decision 7, as
   “The dry run and the saves” now says.
5. After each save, does what “The dry run and the saves” says, and tells the commander
   the pages saved and their revisions.
6. Drafts the reply to Avi on the saves, as “The reply to Avi” says.

The session's helpers are untracked, in
`D:/GitRepos5/MAM-basics/.novc/miqra-mevoar-torah-2026-11-22/`. In `scripts/`:
`check_main_page.py`, the main page's precondition; `summarize_display_run.py`, which compares
a dry run's counts with the Counts table, and whose copy of the table a change of decision 1's
ranges updates; the launcher `run_bot_with_plan_summary.py`, which copies Stage 10's summary
from this plan; and `read_after_save.py`, the read after a save. In `decision-page/`: the
decision page's builder, `build_page.py`. In `wikisource/`: the responses kept on 2026-11-22.
A session in another clone reads them there by absolute path and copies what it runs into its
own `.novc/`, as this session copied round 1's. The kept responses are evidence of 2026-11-22;
the preconditions read the live pages again.

## Stage 13. The block of title and navigation on the Torah's parts, on Ben's word

The session that resumed Stage 12 wrote this stage on 2026-11-22 (execution ledger, “Stage 12
resumed”), on Avi's answer to Stage 12's decision 4, which Ben relayed: “If the bot can create
that kind of title and navigation in the very same style as Joshua 1, that would be great!”
(decisions ledger entry 18). A fresh session executes it, never the session that wrote it;
Ben's word to act on Avi's answers covers its execution, and each saving run still needs his
word for that run (entry 3). The design is that session's proposal. Three choices that neither the plan nor
Avi's words settled, decisions 7 to 9 of the stage's decision page, took Ben's answers on
2026-11-23: he chose each one's recommendation, marked (a), as decisions ledger entry 19
records.

**What it does.** BDencklaBot creates the Torah's 15 part pages of Stage 12, `gen-1` to
`deut-3`, each with a block of title and navigation at its top (decision 7a), in the very same
style as the block that Dovi added to Joshua's first part in revision 3103803 (Deferred, “The
parts of large books”). A block's topics are its page's headings and its chapters are its page's chapters,
each linked to its place on the page. Below the block, each page is exactly as Stage 12 makes
it. The 19 other pages of `display_page.PAGES` keep their text byte for byte, and Joshua's first
part keeps Dovi's block.

**The model,** measured on 2026-11-22 from Joshua's first part in revision 3103803 and from the
main page's revision 3104053, both read anonymously at 20:24 New York time, by
`resume/scripts/check_joshua_block.py` (`resume/survey/joshua-1-block-check.txt`), in
`D:/GitRepos5/MAM-basics/.novc/miqra-mevoar-torah-2026-11-22/`:

1. The page is four lines and then the bot's text of `yehoshua-1`, as `display_page.page_text`
   gives it, byte for byte: the block's line, a horizontal rule, `-----`, and two blank lines.
   Dovi added those four lines and changed nothing else.
2. The block's line is six pieces of fixed text around the part's own three, in this order:
   fixed text, a template's call, two templates' openings and the opening of bold; the part's
   name, which is its link's label on the main page without the range in parentheses at its
   end; fixed text, which closes the bold and the inner template, calls a template and opens
   bold again with the word for topics, a colon and a space; the topics, each a link
   `[[#<chapter> <verse>|<label>]]` to the verse before which its heading stands, joined by the
   fixed text ` · `, a space, a middle dot and a space; fixed text, which closes the bold, calls
   the same template and opens a parenthesis with the word for chapters, a colon and a space;
   the chapters, each a link `[[#<chapter> <first verse>|<chapter>]]`, joined by the fixed text
   `, `; and fixed text, which closes the parenthesis and the outer template and calls one more
   template. Chapters and verses are numerals throughout.
3. Joshua's topics are the 18 headings of its chapters 1 to 12 in the tracked JSON, in order,
   after NFC, each labelled by its heading's text, and its chapters are 1 to 12, each linked to
   its first verse. Rebuilt from these pieces, the line equals revision 3103803's line byte for
   byte.
4. The links reach the anchors that the verse template makes, `<chapter> <verse>` in numerals,
   as the Decalogue templates do for their verses: the templates' text that Stage 12 kept,
   `wikisource/templates-20261122T142511Z.json` in the same folder.

**What the Torah's parts bring that Joshua's first part did not,** measured on 2026-11-22 from
the same reads by `resume/scripts/survey_heading_texts.py` and `survey_block_inputs.py`
(`resume/survey/heading-texts.txt` and `block-inputs.txt`):

1. **Headings that live in the base chapters.** No book of the Torah is in `in/miqra-mevoar/`:
   Stage 12's heading places give the verses of its 443 headings, and their text is only in the
   base chapters, of which Git keeps no text (decisions ledger entry 2). All 443 are pointed, in
   NFC, and hold no markup, and 441 of them begin with the word פָּרָשַׁת, which none of
   Joshua's does; the other two are the headings before Exodus 20:1 and Deuteronomy 22:20
   (`resume/survey/first-words.txt`). Decision 8.
2. **Chapters split between two parts.** Numbers' second part ends at 22:1 and its third
   begins at 22:2; Deuteronomy's first ends at 11:25 and its second begins at 11:26. Joshua's
   parts hold whole chapters. A block lists each chapter that has a verse on its page, linked
   to its first verse there: on `num-3` chapter 22's link reaches 22:2, and on `deut-2` chapter
   11's reaches 11:26.
3. **Names with quotation marks and apostrophes.** Four names hold words in double quotation
   marks. Two hold a he and an apostrophe, the abbreviation of the divine name, and
   the name of `lev-1` ends with it, so that its apostrophe meets the three apostrophes that
   close the name's bold; MediaWiki reads four in a row as an apostrophe and the end of bold.
4. Every page's first verse has a heading, and no heading stands at a verse of the Decalogue.
   The 15 blocks have 17, 49, 26, 37, 14, 54, 24, 23, 23, 24, 28, 20, 24, 65 and 15 topics, in
   the order of the pages, the headings of Stage 12's Counts table.

**Choices,** decisions 7 to 9 of the stage's decision page,
https://claude.ai/artifact/XYchLEVJdwMQh5FM3wDJHN, numbered after Stage 12's 1 to 6. Ben
chose 7a, 8a and 9a on 2026-11-23 (decisions ledger entry 19):

7. **When the 15 pages are saved.** (a) With their blocks: this stage's executor creates each
   page once, in one saving run of the 15. (b) Now, without blocks: the session that resumed
   Stage 12 saves the 15 in one run from Stage 12's code, and this stage adds each block by
   the update outcome below, which edits a page only while it holds the bot's text alone.
8. **The topics' labels.** (a) Each label transcludes its heading from its base chapter, by the
   very call that the verse's break line makes, so that a heading that Rabbi Kokhav revises
   changes in the block too; each label shows the heading whole, its first word included.
   (b) Each label is a copy of its heading's text, as Joshua's are: the bot reads the texts from
   the base chapters when it builds a page, and a revised heading leaves its copy behind.
   (c) A copy without its first word where that word is פָּרָשַׁת, as in 441 of the 443,
   which makes the topics shorter, like Joshua's, but changes Rabbi Kokhav's wording, which
   nobody has asked for.
9. **The parts made without a block:** Joshua's second part, Judges' three and Daniel's two.
   (a) None now: the reply to Avi asks whether he wants the bot to give each of them a block.
   (b) This stage gives them blocks too, by the update outcome, from the names of their links'
   labels in revision 3104053, which are pointed, and from their headings in the tracked JSON:
   the five whose text is still the bot's, all but Judges' second part, which holds Dovi's two
   pictures and is left to Avi or Dovi. (c) None, and nothing asked.

**The design,** for decisions 7a, 8a and 9a:

1. **Generator,** `py/miqra_mevoar/display_page.py`:
   - `Page` gains `block_name`, the part's name for its block, or None for a page without one.
     The Torah's 15 entries of `PAGES` take their names, copied by script, from their links'
     labels in revision 3104053, without the range in parentheses at the end of each; no other
     entry has one. The module docstring and the table's comment say so.
   - The six pieces of fixed text, copied by script from the first line of Joshua's first part
     in revision 3103803, as item 2 of the model divides it, are constants, with a comment that
     says so.
   - `page_text` puts a block before the text of each page that has a `block_name`: the block's
     line, the horizontal rule and two blank lines, then the page's text as now. A function
     builds the block's line from a name, the anchors and labels of its topics and the anchors
     of its chapters. The topics are the page's verses that have a heading, in order, each
     anchored at its chapter and verse and labelled by decision 8a's transclusion, the same
     call as its break line's; the chapters are those of the page's verses, in order, each
     anchored at its first verse on the page.
   - `read_page`, the closed parser, accepts a block only as a page's first four lines, and its
     line only in the shape above, with decision 8a's labels. It checks the block against the
     page's own lines, and raises unless its topics are the page's headings, in order, with the
     same transclusions, and its chapters the page's chapters at their first verses. It returns
     the block's name, or None, with the page's verses and sort key, and raises on any other
     line, as now. The bot mode's and the test's calls change with it, as do those of the
     helpers that the executor runs.
   - Every page without a `block_name` keeps its text byte for byte.
2. **Bot mode,** `py/main_ws_bot.py miqra-mevoar-display`: unchanged but for its call of
   `read_page`. Its dry run's parse, which requires that no link or transcluded page be
   missing, now covers the block's templates too.
3. **Test,** `py/tests/test_miqra_mevoar_display.py`, differential, with its own oracles:
   - On a page with a `block_name`, the block's topics are the verses to which the test's oracle
     gives a heading, in order, each with its chapter's and verse's numerals as its anchor and
     the transclusion of its heading's section from its base chapter as its label; its chapters
     are those of the oracle's verses on the page, each anchored at its first verse there.
   - Every page of the Torah has a block, and no other page has one.
   - Each `block_name` holds a Hebrew point, is in NFC and has no range in parentheses at its
     end.
   - A missing input fails rather than skips.

**If Ben had answered otherwise,** which he did not (decisions ledger entry 19):

- **Decision 7b or 9b** adds an **update** outcome to the bot mode, for a page that exists and
  whose live text equals, byte for byte, the text that the generator gives it without its
  block: a saving run replaces it with the text with the block, as an edit that may not create
  a page, with an edit summary that Ben approves with the run, and reads it back as a creation
  is read back. Any other page that exists is refused, as now. Under 9b, `block_name` is given
  to `yehoshua-2`, `sephershoftim-1`, `sephershoftim-3`, `daniyel-1` and `daniyel-2` from their
  labels in revision 3104053, copied by script, and their headings come from the tracked JSON,
  as their break lines' do; the test's oracle of their topics stays the tracked JSON.
- **Decision 8b or 8c** makes each label a copy of its heading's text, read from the base
  chapters when the bot builds a page, which then depends on the live pages: the bot mode reads
  them, the generator takes them as an argument, and the test checks the block's anchors and
  shape only. Under 8c a copy loses its first word where that word is פָּרָשַׁת.

**Preconditions,** before the dry run and again before each save:

- `py/main_miqra_mevoar.py base-headings --check` finds every heading of the pages' base
  chapters where the heading places have it. If one differs, stop and report it to Ben.
- The main page's latest revision, read again by script, still links the 15 names with the
  labels of revision 3104053, from which the blocks' names come. If it does not, stop and
  report it.
- Joshua's first part is still at revision 3103803. If Dovi has changed its block again, stop
  and report it to Ben: “the very same style” is the block as it then stands.
- None of the 15 pages exists, under decision 7a.
- No `main_ws_bot.py` process runs, and no other session of the commander's family does bot
  work.

**Verification,** focused, under `doc/review-trial.md`: `git diff --check`; Black on the changed
Python files; and this command, Stage 11's with `py/tests/test_product_scopes.py` and
`py/tests/test_sibling_reach.py` added (161 passed on 2026-11-22, before this stage's change):

```powershell
./.venv/Scripts/python.exe py/main_test.py py/tests/test_miqra_mevoar_display.py py/tests/test_miqra_mevoar_versification.py py/tests/test_miqra_mevoar_index.py py/tests/test_miqra_mevoar_bot_revision_guard.py py/tests/test_mega_coverage.py py/tests/test_entry_point_subcommands.py py/tests/source_hygiene_test.py py/tests/test_prose_conventions.py py/tests/test_transliterations.py py/tests/test_explicit_time_zones.py py/tests/test_stderr_error_handler.py py/tests/test_h_dot_below_nfc.py py/tests/test_prose_mark_order.py py/tests/test_tracked_filenames.py py/tests/test_miqra_mevoar_save_receipts.py py/tests/test_product_scopes.py py/tests/test_sibling_reach.py
```

Compared by a scratch script before and after the change, as `resume/scripts/write_pages.py`
and `compare_dirs.py` compared Stage 12's resumed pages: the generated text of the 19 pages
without a block, byte for byte; and, of each Torah page, the text after its block's four lines,
which must equal Stage 12's page byte for byte (`resume/generated-after-comments/`). A scratch
script also gives the generator's function that builds a block's line the name of Joshua's
first part, the anchors and texts of its 18 headings and its 12 chapters, and requires revision
3103803's line byte for byte. Expected unchanged: every product directory that
`py/product_scopes.py` declares, and `in/`. The mega runs none of this code; the last pushed
commit's message says what was skipped and why.

**The dry run and the save.** Run `--no-save` with `--page` naming the 15 pages. Each page must
have Stage 12's counts, which `scripts/summarize_display_run.py` compares; read each page's
first five lines and its last. Render the blocks of `lev-1` and `num-1` through the API's parse
action, which saves nothing, and check that each name shows whole in bold. Report the creates,
the counts, the parse check and the run directory to Ben on the decision page; then stop. One
saving run of the 15, on Ben's word for that run, with Stage 10's summary, copied from this plan
by script through the launcher `scripts/run_bot_with_plan_summary.py display`. After it, a read
after the run, without the bot's login, by `scripts/read_after_save.py`, and a dry rerun that
finds every saved page unchanged; then an entry in `py/ws/ws_bot_edit_history.md`, the execution
ledger and the State. Commit, fetch, merge `origin/main` if it moved, and push.

**The reply to Avi,** drafted for Ben once the pages are saved, as Stage 12's “The reply to Avi”
and the user-level section “Emails written for Ben to send” say: it reports the 15 pages, says
that their blocks follow Joshua's first part, with each topic transcluded from its base chapter
and a split chapter linked to its first verse on the page, and, under decision 9a, asks whether
Avi wants the bot to give a block to Joshua's second part, Judges' three parts and Daniel's two.
Nothing is sent: Ben sends it himself.

**Checkout and coordination:** `D:/GitRepos5/MAM-basics`, whose
`.novc/miqra-mevoar-torah-2026-11-22/` holds the helpers named here and the kept responses, or
another full clone in one of Claude's forests that the commander assigns, which then reads those
by absolute path and copies what it runs into its own `.novc/`. Before the first edit: verify the
clone with `git rev-parse --show-toplevel`, `git rev-parse HEAD`, its branch and `git status
--porcelain`; fetch, and require `main`, clean, at the commit that added this stage or a
descendant, with `git merge-base --is-ancestor`. Its own `.venv/Scripts/python.exe`, run from its
root, and `-c safe.directory=<clone>` on every Git call. Load `iterative-document-editing` before
editing this plan, and `hebrew-prose`, with its `references/mam-basics.md`, before prose about
the Hebrew text. The executor owns its commits' integration: it commits on `main`, naming its
paths, fetches and merges `origin/main` before each push, and pushes `main`. The kept responses
are evidence of 2026-11-22; the preconditions read the live pages again.

## Later Word files

A new or revised book repeats Stage 3's fetch, extract and check, and a reading of the tracked
JSON's diff, and then Stages 6 to 8 for its pages, each saving run again on Ben's word. An update
goes through only for pages that nobody but BDencklaBot has edited. A book of the Twelve whose
base chapters arrive this way then gets its display page through Stage 10's mode, added to that
mode's table, again on Ben's word for each saving run. Such a run names its pages with `--page`:
a run over the whole table refuses Joshua's part one, which carries Avi's model (execution
ledger, “Avi's answer to the reply”), and Judges' part two, to which Dovi added two pictures
on 2026-11-21 (execution ledger, “Stage 12, the display pages of the Torah”). Since round 1
of 2026-11-16 the table gives Joshua's two
entries the titles to which Avi moved them, and keeps Stage 10's names as their sort keys
(decisions ledger entry 15, item 5).

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
