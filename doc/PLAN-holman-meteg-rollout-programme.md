# Programme: the seven-item Holman meteg rollout

Written 2026-09-03, consolidating into git a plan that until then existed only
in one untracked sketch and in agent-call transcripts. Ben's instruction that
day: *"I want all these consolidated into git and related to each other at this
point, as I fear loosing track of this larger context."*

**STATUS: items 2 through 7 are ALL DONE, items 5, 6 and 7 having finished on
2026-09-04. What remains of this programme is item 1's Phase 1, the post-stress
meteg survey page, and its Phase 2, the M23 card link** — both of which wait on
item 5 by design, and whose figures item 5 has now moved. Item 1's Phases 3
through 6 are done and recorded in that plan.

Every section below is an execution record rather than a sketch. The sketch had
been assembled from three research-agent reports and one Plan-agent validation
pass, synthesized in conversation, and never reviewed against repository state a
second time, and executing it went on finding its figures wrong to the end:
item 2 found four of its own wrong on 2026-09-03, item 4 one of its own the same
day, and item 7 found on 2026-09-04 that its Joshua 10:12 expectation was wrong
in kind rather than in degree. **A figure in a record below is a measurement, so
re-measure rather than trusting it, and treat a mismatch as a finding.**

Execute everything here from `C:/Users/BenDe/GitRepos/MAM-basics`, venv
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`.

## What the programme is for

Holman sent 34 suggestions about MAM, rendered as cards M1–M34 on
`gh-pages/holman/table_data_findings.html`. Thirty of them differ from their
comparison form in metegs alone. This programme applies those thirty to MAM by
Wikisource bot, carries the change through the MAM update pipeline, archives
the thirty records, and refreshes the mgketer comparison.

**All thirty are accepted, and were accepted before any of the research below
was done.** Ben's decision, stated 2026-09-03: he is taking all thirty Holman
meteg suggestions, the 29 removals and M23's one addition alike. **The
post-stress meteg research is background, not a decision input** — in his
words, meteg-after-primary-stress is "an interesting and not-that-common
phenomenon", and the research "was not to determine whether we want to take the
suggestion (we'd already decided that) but to provide background on that
phenomenon." So no item of this programme waits on a disposition, and item 1 is
background material rather than evidence anybody is deciding on. The four
accent-placement records M17, M24, M32 and M34 stand outside this decision as
they stand outside the programme: they keep the dispositions Seth (Avi) Kadish
gave them on 2026-08-28.

**Twenty-nine of the thirty remove a meteg from MAM; one, M23 at Isaiah 23:12,
adds one.** That asymmetry is the single most common way to get this work
wrong, and it recurs in items 2, 3 and 7. Measured 2026-09-03 over
`holman/docs-not-served/mam_suggestions.json`: 29 records where MAM carries the
extra meteg, one where the Aleppo comparison does.

**The letter M is the MAM-suggestion series prefix, not an abbreviation of
meteg.** `py/py_render/rt_mam_suggestion_card.py` renders it as
`M{case_number}`. There are 34 M records; the 30 meteg ones are M1–M16,
M18–M23, M25–M31 and M33 — that is, all of them except M17, M24, M32 and M34,
which are accent-placement records and are NOT part of this programme.

## The seven items

| # | Item | Status |
|---|---|---|
| 1 | Track the notes, publish a gh-pages page, link it from the M23 card, rename the page identity and the archive label | Planned in detail, reviewed — see the plan named below |
| 2 | Build the Wikisource bot edit files for all 30 | **DONE 2026-09-03**, files built and validated offline — see the item 2 section below, which is now an execution record rather than a sketch |
| 3 | Run the bot | **DONE 2026-09-03**, 23 chapters saved on Ben's go-ahead — see the item 3 section below, an execution record now |
| 4 | Download the affected chapters, plus Joshua 10 and Zechariah 2 | **DONE 2026-09-03**, and Zechariah was repair rather than consistency — see the item 4 section below, an execution record now |
| 5 | Run the wsgo diff and the standard MAM update pipeline | **DONE**, steps 1 and 2 on 2026-09-03 and steps 4 through 7 on 2026-09-04, Ben having done step 3 at the keyboard between them — see the item 5 section below, an execution record now |
| 6 | Archive the 30 records | **DONE 2026-09-04**, all 34 M records archived, and the ingest needed two repairs before it would run at all — see the item 6 section below, an execution record now |
| 7 | Refresh the mgketer comparison | **DONE 2026-09-04**, 31 meteg diffs gone and one accent diff arrived — see the item 7 section below, an execution record now |

Items 2 through 7 are ordered by dependency, not by preference: each needs the
one before it.

**Item 1 is NOT independent of them, and it does not move as a unit.** This
paragraph read "Item 1 is independent of all of them and can be done first or
last" until 2026-09-03, and both halves of that sentence are wrong. Item 1's
six phases split around the pipeline:

1. **Before item 3** goes item 1's Phase 3, the mgketer verifier, the one
   phase with a hard deadline: it matches each of the thirty records against a
   live mgketer diff card, and items 3 through 7 are precisely what make those
   thirty diffs disappear — item 7's own expected result below says so in as
   many words. Ben's decision, 2026-09-03: that check runs ONCE, by hand, from
   an entry point of its own, and is not wired into the command that renders
   the Holman pages, which would otherwise stop working when the diffs go.
   Item 1's Phases 4, 5 and 6 are indifferent to the pipeline and can go
   alongside.
2. **After item 5** go item 1's Phase 1, the survey, and its Phase 2, the M23
   card link, which needs Phase 1's page to exist. Item 5 changes the very
   figures the survey publishes; the next section says by how much.

Why that check runs only once, and the two alternatives Ben rejected, are
recorded in that plan's Phase 3.

### Item 5 changes the survey's figures, and nothing re-runs the survey by itself

Item 1's survey counts MAM's metegs by position relative to the primary stress,
so item 5's fresh MAM data moves its numbers in both directions. Measured
2026-09-03 against
[`post-stress-meteg-census-2026-09-03.md`](post-stress-meteg-census-2026-09-03.md),
which is that plan's legacy baseline:

1. **M23 raises the post-stress count from 231 to 232**, adding one meteg of
   exactly the kind the page is about.
2. **All 29 removals are pre-stress metegs, so they move the survey's
   pre-stress figures instead.** Not one of the 29 verses appears anywhere in
   the census's post-stress lists: the six books they touch contribute 46
   entries in all — Judges 5, 1 Samuel 10, 2 Samuel 11, 1 Kings 10, 2 Kings 4,
   2 Chronicles 6 — and every one of the 46 is a different verse. All six are
   prose books, so the prose pre-stress figure of 13,131 falls by about 29.
   "About" because M13 contributes two bot entries against one census
   occurrence, and the exact figure is the tracked generator's to establish
   rather than this document's.

**The trap is that nothing catches it.** Artifact 6 of item 1's plan has the
mega render the page from the tracked `out/accgram/post-stress-meteg.json`
rather than recomputing, so once item 5 lands the published page goes on
printing pre-pipeline figures until somebody re-runs the standalone
computation. So if item 1's Phase 1 has already been done when item 5 runs,
**re-running that computation is a step of item 5**, and its diff against the
tracked JSON is expected to be non-empty in exactly the two ways above.

**IN THE EVENT THE TRAP DID NOT FIRE, because item 5 ran first.** Checked
2026-09-04, immediately after item 5's mega run: `out/accgram/post-stress-meteg.json`
does not exist, item 1's Phase 1 never having been done, so there was no stale
computation to re-run and nothing was published from one. **That makes the
figures above a PREDICTION that Phase 1 will now test rather than a correction it
must apply.** Phase 1 computes against the post-item-5 MAM from the start, so its
first published figures should already be the moved ones: 232 post-stress metegs
rather than 231, and a prose pre-stress figure about 29 below 13,131. Treat a
mismatch with either as a finding.

### Item 1: the notes, the page, the M23 link, the terminology rename

Covered in full by
[`PLAN-post-stress-meteg-page-and-holman-m23.md`](PLAN-post-stress-meteg-page-and-holman-m23.md),
which was reviewed on 2026-09-03 and corrected the same day. That plan
publishes a survey of MAM's 231 post-stress metegs at
`gh-pages/post-stress-meteg.html`, gives the M23 card a neutral link to it, and
makes two reader-facing renames on the Holman pages: the archive label from
"Suppressed" to "Archived", and the page's own title and heading to plainly
**"Holman MAM suggestions"**.

That second rename is Ben's decision of 2026-09-03, and it records something
about this programme rather than only about a page. The page began as a
ketiv/qere review and its title still said so — "Holman's ketiv/qere review and
MAM suggestions". Ketiv/qere is now one kind of suggestion among several, of
which this programme's thirty metegs are the largest, so the compound title
names an old scope. The per-row ketiv/qere vocabulary stays exactly as it is:
it names a category that still exists, and it drives the page's filtering.

It deliberately does NOT archive any record, edit Wikisource, or run the mega
pipeline. Those are items 2 through 6 here.

### Item 2: build the Wikisource bot edit files — DONE 2026-09-03

Executed 2026-09-03 in a worktree of `C:/Users/BenDe/GitRepos/MAM-basics`, on
top of `28564417`. **The bot was not run: `py/main_ws_bot.py real` was not
invoked, with or without `--no-save`.** That is item 3.

The mechanism is `py/ws/ws_bot_edit.py` and `py/main_ws_bot.py`. `edit-kind` is
a FILE-LEVEL key, so one JSON file cannot mix kinds, and two files were built:

1. `in/mam-ws-bot-edits/holman-meteg-removal.json`, `edit-kind: meteg-removal`
   — **29 entries covering 28 records, across 22 chapters of six books** (1
   Kings 7, 11, 12, 15, 17, 18, 22; 1 Samuel 18, 27; 2 Chronicles 6, 18, 24,
   32; 2 Kings 7; 2 Samuel 11, 12, 15, 18; Judges 1, 5, 6, 21). Each entry
   carries `ch`, `old` and a `comment`; `old` occurs exactly once in that
   chapter, and the bot removes the FIRST U+05BD in `old`.
2. `in/mam-ws-bot-edits/holman-meteg-add-isaiah-23-12.json`,
   `edit-kind: explicit-replacement` — one entry, M23 at Isaiah 23:12, the sole
   addition-direction record: `old="ק֣וּמִי"`, `new="ק֣וּמִֽי"`.

Both are built and re-checked by a tracked subcommand rather than by hand:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_ws_bot.py holman-meteg-spec
```

`py/ws/holman_meteg_edit_spec.py` is the module; `--write` rebuilds the two
files, and the default is check-only so that the pre-flight this item's old
sketch asked for can be re-run immediately before item 3's live save without
rewriting its own subject. Its module docstring carries the fuller statement of
everything below.

**Four figures in the sketch this section replaces were wrong**, and each is
worth stating because the arithmetic that produced them is so easy to redo.

1. **`old` CANNOT be `mam_form` verbatim, and this is the big one.**
   `mam_form` is in MAM-normal mark order — shin dot, sin dot, dagesh, rafe,
   then every other mark — and Hebrew Wikisource's wikitext is not: it writes
   the dagesh, shin dot or sin dot AFTER the vowel. Measured 2026-09-03,
   **seventeen of the thirty `mam_form` strings do not occur in their own
   chapter at all**, and **eleven of the seventeen fail for mark order alone**
   (M1, M2, M4, M6, M11, M16, M19, M22, M26, M29, M30). The two orders render
   identically, so nothing looks wrong and only a byte comparison sees it. The
   module therefore searches the chapter in std-order space and slices the
   ORIGINAL text at the index it finds — `give_std_mark_order` reorders marks
   only inside one letter's cluster, so it moves no index. Every `old` is
   the wikitext's own bytes, located by the record rather than copied from it.
   `CLAUDE.md`'s opening section is the rule this instance of the problem
   belongs to.
2. **M18, 2 Kings 21:12, is ALREADY APPLIED on Wikisource and is excluded from
   the file.** The fresh download of 2026-09-03 has no meteg on the resh of
   ירושלם there, nor on the vav of ויהודה, which is mgketer's
   `2K21:12#0ebb56b0` and which no Holman record covers. So somebody edited
   that verse for both metegs. An entry for M18 would abort the whole run,
   `ws_bot_edit.edit_page_text` asserting its `old` occurs exactly once, so
   `_ALREADY_APPLIED` excludes it by name and the check fails loudly if the
   meteg ever comes back. **This is why the removal file holds 29 entries and
   not 30**: 28 records at one entry each, plus M13's second.
3. **Four more records sit inside a template, not one.** M3, M20, M21 and M25
   all name ירושלם, which the wikitext writes across a `{{מ:ירושלם|…|…}}` call
   — `יְרֽוּשָׁל{{מ:ירושלם|ָ|ֽ}}ם׃` — with the meteg in the plain-text part
   before it. Their `old` is the whole word as written, template call included.
   Note that in M3, M20 and M21 that call's second parameter is **itself a
   U+05BD**, the silluq of a verse-final word, so `old` holds two of them and
   the bot's remove-the-first rule is what keeps the silluq. The module asserts
   per entry that the first U+05BD in `old` is the located target.
   M18 was a fifth such case before it was applied.
4. **M13 is two entries, exactly as
   [`holman-meteg-m13-qamats-template.md`](holman-meteg-m13-qamats-template.md)
   found**: `old="הׇֽחֳלֵֽיתִי"` for the ד parameter of its
   `{{מ:קמץ|ד=…|ס=…}}` call and `old="הָֽחֳלֵֽיתִי"` for the ס parameter.
   Removing the meteg from ד alone would leave the two forms differing in
   something other than the qamats, which is the only thing that template
   exists to vary. That note's own cross-check passes: after the edit,
   2 Chronicles 18:33's call is byte-identical to the one in 1 Kings 22:34.

**So the "not yet checked" question this section used to end on is answered:
five of the thirty records sit inside a template, not one.** Four are ירושלם
and one is קמץ, and M18 was a sixth until it was applied.

What the checks report, all of them re-runnable:

1. **The arithmetic gate passes 30 of 30.** Stripping the first U+05BD from
   `mam_form` reproduces `comparison_form` for the 29 removals, and stripping
   it from `comparison_form` reproduces `mam_form` for M23.
2. **Uniqueness passes for all 30 entries**, checked in both texts a bot may be
   handed: the raw wikitext `real` edits, and the format-2 round trip `proto`
   edits. M23's `old` is worth its own mention — `ק֣וּמִי` occurs twice in the
   whole corpus, once in Isaiah 23 and once in Lamentations, against 21
   similarly-spelled קומי atoms, so the chapter scoping is what makes it safe.
3. **Both `proto` runs applied cleanly**, and every one of the 23 touched
   chapters differs from its input by exactly the metegs its own entries name
   and by nothing else — 22 chapters losing between one and three metegs, and
   Isaiah 23 gaining one.

Re-downloading the target chapters first, so the `old` strings are built
against current text, is what surfaced finding 2 above. One command does it,
`--book-chapters-json` being far cheaper than 24 `--chapter` runs:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_download.py fr-wikisource --book-chapters-json .novc/holman-meteg-removal-chapters.json
```

`holman-meteg-spec --selector-dir .novc` writes that selector, one file per
spec, naming exactly that spec's chapters.

### Item 3: run the bot — DONE 2026-09-03

Executed 2026-09-03 in a worktree of `C:/Users/BenDe/GitRepos/MAM-basics`, on
top of `0d1ad458`, and committed as `031b4306`. **Ben gave the go-ahead in
words that day**, in answer to a report of exactly what would change; the
sketch below is what the run followed, and every one of its instructions held.

Three commands ran, in this order.

1. **The pre-flight, check-only**, `py/main_ws_bot.py holman-meteg-spec`. It
   reproduced every figure on record: 30 records (29 removal, 1 addition),
   arithmetic gate 30 of 30, M18 excluded as already applied, removal spec 28
   records to 29 entries across 6 books, uniqueness 30 of 30 in both texts,
   coverage 29 records and 30 entries. `--selector-dir .novc` then wrote the
   two selectors, 22 book/chapter pairs for the removal spec and 1 for the
   addition.
2. **`real --no-save` over the full target set**, one run per spec. Each
   fetched the live text, ran the identical uniqueness assertions against it,
   and exited naming the chapters that would change: all 22 removal chapters,
   and Isaiah 23. Nothing outside either spec.
3. **`real` for the save, in seven book-sized slices**, each over a per-book
   cut of the removal selector written by a throwaway splitter, plus the
   addition spec's one-chapter selector:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_ws_bot.py real --edits in/mam-ws-bot-edits/holman-meteg-removal.json --book-chapters-json .novc/holman-meteg-removal-1Kings.json -dir:C:/Users/BenDe/.pywikibot
```

**Twenty-three chapters saved**, and the counts are chapters per slice rather
than chapter numbers: seven of 1 Kings, four each of Judges, 2 Chronicles and
2 Samuel, two of 1 Samuel, one of 2 Kings, and Isaiah 23 alone.
`modified-chapters.json` was read after each slice and named exactly that
slice's chapters.

**The measured result is 29 metegs off and one on, a net of 28**, counting
U+05BD in `in/mam-ws` before and after: Judges 1202 → 1194, 1 Samuel 1482 →
1480, 2 Samuel 1142 → 1138, 1 Kings 1338 → 1330, 2 Kings 1265 → 1264, 2
Chronicles 1462 → 1456, Isaiah 2034 → 2035. **Twenty-nine verses changed and
nothing else in the 23 chapters did** — one verse per entry except at 2
Chronicles 18:33, where M13's two entries are the two parameters of one
`{{מ:קמץ}}` call and so land in a single verse.

**The pre-flight now raises rather than passing, and that is the designed end
state.** Re-run immediately after the save, `holman-meteg-spec` raises
`SpecProblem` on M1: no prefix of its MAM form reaching past the meteg occurs
in 1 Kings 7 any more, because the meteg is gone. `holman_meteg_edit_spec.py`'s
module docstring says this is what to expect and that the specs are to be
archived with item 6 rather than kept green.

The run is recorded in
[`ws_bot_edit_history.md`](../py/ws/ws_bot_edit_history.md) as a new era, and
that file's "current" marker has moved off the sigil ב2 entry onto it.

**What the sketch below said, kept as written because the run followed it.**

`proto --edits <file>` validates against local `in/mam-ws/` text. That is
necessary and not sufficient: it does not prove the strings are still unique on
the live wiki. `real --no-save` fetches live text, runs the identical
assertion, and skips only the final `page.save()`. **Run `--no-save` across the
full target set immediately before the real save.** A report of every chapter
that would change is the expected outcome, not a failure to fix.

**The bot has no crash recovery** — no try/except anywhere in the apply loop.
A failure partway through leaves whatever was already saved standing on live
Wikisource with none of the run's bookkeeping written. Mitigation: run `real`
in book-sized slices rather than one 29-entry sweep, checking
`modified-chapters.json` after each slice, so a failure's blast radius is one
book.

**A bare `--book39` slice will NOT work, and the correction matters because
this paragraph asked for one until 2026-09-03.** `--book39 1Kings` selects all
22 chapters of the book, and `ws_bot_edit.assert_book_plans_within_target_set`
then refuses every chapter the spec does not name, exiting before a single
page is fetched. Slice with `--book-chapters-json` instead, over a per-book cut
of the selector that `holman-meteg-spec --selector-dir .novc` writes. **Every
`proto` or `real` run of either Holman spec needs that selector**, for the same
reason: with no selector at all the run selects all 39 books.

**Add the run to [`ws_bot_edit_history.md`](../py/ws/ws_bot_edit_history.md)
when it happens, and move that file's "current" marker off the sigil ב2 entry.**
Item 2 deliberately did not, the history recording bots that have run.

This item needs Ben's own `~/.pywikibot/password.py`, a bot password under the
account `BDencklaBot`. Verify it exists before starting. **A session must never
see, create or handle that credential**, and editing a live wiki is an
irreversible outward-facing action: it is Ben's to authorize each time.

**A SESSION RUNS THIS ITEM ITSELF, and the paragraph above is about permission
rather than ability — do not read it as saying otherwise.** Sessions have run
this bot. The credential is never read by the session: `-dir:` points pywikibot
at `~/.pywikibot/`, pywikibot reads `password.py`, and
`ws_bot_real._assert_pywikibot_auth_files_present` does no more than test that
the file is there. So what item 3 waits on is Ben's go-ahead, which is a
sentence from him, and not a step he has to carry out at the keyboard.
`py/ws/pywikibot-setup.md` is the operating manual, `-dir:` mechanism and all.
Written 2026-09-03, after a session recommended item 1's Phase 3 over item 3 on
the ground that "a session can't do it: it needs your pywikibot credential" —
Ben: *"A session can do it, and absolutely has done it."* The ordering that
session recommended was right for a different and better reason, the deadline
below; the credential was never the obstacle.

### Item 4: download the affected chapters, plus Joshua 10 and Zechariah 2 — DONE 2026-09-03

The affected-chapter half needed no command of its own: `--no-post-download`
was not passed, so each of item 3's seven `real` runs downloaded and reparsed
its own slice's chapters as it finished. That is where the seven changed
`in/mam-ws/*.json` and `out/mam-ws-parsed-fmt-2/*.json` of `031b4306` come
from.

The two extra chapters were downloaded separately, before the bot ran, and
committed as `0d1ad458`:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_download.py fr-wikisource --book-chapters-json .novc/holman-extra-chapters.json
```

**Zechariah 2:4 was repair, not consistency, and the paragraph this replaces
said otherwise.** That paragraph read: "Zechariah 2:4's local copy already had
the corrected form, so downloading it is consistency rather than repair."
Measured 2026-09-03, immediately before this download,
`in/mam-ws/CK-Zechariah.json` held אֲשֶׁר־זֵ֣רוּ, the munaḥ on the zayin, and
`MAM-parsed/plain/CA-The-12-Minor-Prophets.json` still does; the download
replaced it with אֲשֶׁר־זֵר֣וּ, the munaḥ on the resh, which is M34 and has
been live on Hebrew Wikisource since 2026-08-28. So **both** extra chapters
were stale locally, on the same footing, and item 5's wsgo diff carries two
accent-placement corrections to the Google Sheet rather than Joshua's alone.
`holman-accent-placement-four.md`'s stage table says the same wrong thing and
now carries a correction beside it. Joshua 10:12 was stale as stated, with one
pashta יְהוֹשֻׁעַ֙ before the download and two יְהוֹשֻׁ֙עַ֙ after it.

**Joshua 10:12 is not expected to go quiet downstream**, and this is the
programme's other standing trap. The mark added there is a stress helper, a MAM
notational convention the source manuscripts are not expected to have, so
mgketer showing a diff at that atom afterward is correct. It needs no
suppression entry.

### Item 5: the wsgo diff and the standard update pipeline — DONE 2026-09-03 and 2026-09-04

**Steps 1 and 2 ran on 2026-09-03 and are committed as `e43cb5fd`, pushed to
`main` the same day. Ben did step 3 at the keyboard that day, and steps 4
through 7 ran on 2026-09-04.** The step list below carries what each one did.

Both tracked outputs were empty before the run, so all **35** rows
`py/main_diff.py wsgo` wrote are new, and all 35 are accounted for:

1. **28 rows, the removal verses of item 3's bot run.** Twenty-nine entries,
   but M13's two are the two parameters of one `{{מ:קמץ}}` call at 2 Chronicles
   18:33 and so land in one verse.
2. **1 row, Isaiah 23:12** — M23, the one addition-direction record.
3. **1 row, Joshua 10:12** — M24's stress helper, from item 4's separate
   download.
4. **1 row, Zechariah 2:4** — M34, the munaḥ on the resh where the Sheet has it
   on the zayin, from the same download.
5. **2 rows, 2 Kings 21:12** — M18's resh meteg of ירושלם, gone from Hebrew
   Wikisource before item 2 built the edit files, and the vav meteg of ויהודה
   that no Holman record covers. Item 2's finding 2 predicted both. They reach
   `in/mam-ws` by item 2's fresh download, not by any entry of item 3's bot, so
   this is where M18 finally propagates.
6. **2 rows, 2 Samuel 18:20, and these are outside the programme altogether.**
   They are documentation notes, tagged `נוסח:2`, whose wording was edited on
   Hebrew Wikisource independently of anything here and arrived with item 2's
   download of 2 Samuel 18. The Sheet has the older wording, so the pipeline
   carries the newer one to it, which is what the pipeline is for. **Expect
   them among the auto-edits and do not treat them as a defect**, but read them
   before applying, since nothing in this programme vouches for them.

The suite was green in the worktree with `REPOS_ROOT` set: **975 passed, 5
skipped**.

**What these 35 rows do NOT carry is eleven further Holman meteg edits made on
Wikisource on 2026-08-30 and 2026-08-31**, deliberately left for later — see
the section between this item and item 6.

In order:

1. `py/main_diff.py wsgo` — compares `in/mam-ws/` against `MAM-parsed/plain/`,
   writing `out/diff_mamws_mamgo.json` and `out/diff_mamws_mamgo-auto-edits.json`.
   **Done 2026-09-03.**
2. Commit and push the auto-edits JSON, because the next step fetches it over
   HTTP from GitHub. **Done 2026-09-03**, in `e43cb5fd`, merged to `main` and
   pushed as `25bfb0b1`.
3. **Ben, manually, in the MAM Google Sheet**: "Import auto-edits from GitHub",
   then "Apply imported auto-edits", both Apps Scripts under
   `misc/Google Sheet Apps Scripts/`. No session can automate this step.
4. `py/main_download.py fr-google` — downloads and reparses, producing fresh
   `MAM-parsed/plus/` and `plain/`. **Done 2026-09-04.** Three section CSVs
   moved, by **33** lines in all — `B-NevRish` 26, `C-NevAx` 2, `F-KetAx` 5 —
   and those 33 lines are the 33 distinct verses behind the 35 rows, the two
   rows at 2 Kings 21:12 and the two at 2 Samuel 18:20 each landing in a single
   verse. Seven books moved in `MAM-parsed`: Joshua, Judges, Samuel, Kings,
   Isaiah, The-12-Minor-Prophets and Chronicles.
5. Re-run `py/main_diff.py wsgo` and confirm it is empty for the touched verses.
   **Done 2026-09-04, and it is empty EVERYWHERE rather than only at the touched
   verses**: both `out/diff_mamws_mamgo.json` and
   `out/diff_mamws_mamgo-auto-edits.json` are `[]`, and
   `out/mam-ws-bot/proto-misc/modified-chapters.json` is `[]` with them. The
   eleven edits whose download is deferred stay invisible, both sides lacking
   them equally, as the section below this item predicts.
6. `py/main_0_mega.py` from the repository root, from scratch. Regenerates
   MAM-parsed, MAM-simple, MAM-with-doc, MAM-for-Sefaria, MAM-OSIS, and this
   repository's own `out/` and `gh-pages/`. **Done 2026-09-04, and see the
   worktree warning below before running it that way.**
7. Commit and push every touched sibling repository. Each has its own
   `gh-pages/` Pages-deploy workflow firing on push to `main`. **Done
   2026-09-04**, six of them: MAM-parsed `5108203`, MAM-simple `7a4f21d`,
   MAM-with-doc `0fe406c`, MAM-for-Sefaria `ce1e04c`, MAM-OSIS `697dc98` and
   MAM-private `d40e0c8`, that last for the near-aleppo census goldens
   `py/main_0_mega.py` regenerates as a step.

**A MEGA RUN FROM A WORKTREE MISDIRECTS TWO OF ITS STEPS, SILENTLY, AND THE
MEGA'S OWN DOCSTRING SAYS OTHERWISE.** That docstring claims the mega "no longer
writes outside the checkout it runs in, which is what makes a worktree run of it
isolated". That is true of the wlc steps it is written about and false of the
pipeline as a whole. `mb_misc/write_utils.py` builds its destination as the
CWD-RELATIVE `f"../{mam_for_xxx}"`, and it is one of the handful of files
`CLAUDE.md` says are deliberately cwd-relative so that they stay portable when
vendored. Run from `.claude/worktrees/<name>`, that resolves to
`.claude/worktrees/MAM-simple` and `.claude/worktrees/MAM-for-Sefaria`, which the
run CREATES rather than failing on. `REPOS_ROOT` does not help, those modules
never calling `paths`.

Measured 2026-09-04: **216 MAM-simple files and 160 MAM-for-Sefaria files** went
to those phantom siblings, and because `mam-osis` and the accgram steps read the
REAL MAM-simple, which was still stale, MAM-OSIS came out unchanged when it
should have moved. **The failure is silent in both directions** — exit status 0,
and a sibling that looks merely untouched.

What repaired it, and what to do instead: the misdirected output is CORRECT
CONTENT IN THE WRONG DIRECTORY, so it was copied into the real siblings and the
mega re-run as `--resume-from mam-osis`, which rebuilds everything downstream
from the corrected MAM-simple. Convergence was then proved twice over — a third
full mega run left every one of the six siblings' diff sets byte-identical, and
the strays it re-created compared equal to the real repositories at 0 content
differences. **Prefer running the mega from the primary clone.** If it must run
from a worktree, check `.claude/worktrees/` for stray sibling directories
afterwards, every time.

### Eleven other Holman meteg edits are live on Wikisource and absent from this snapshot — their DOWNLOAD deferred 2026-09-03

**Ben's decision, 2026-09-03: leave their download for later.** They are
recorded here so the gap is not lost. Nothing in items 5 through 7 waits on
them: both sides of the wsgo comparison lack the eleven equally, so the pipeline
stays consistent without them.

**SAY WHAT WAS DEFERRED, BECAUSE IT IS NOT THE EDITS.** Ben's correction,
2026-09-04, of a report that had called these "the eleven deferred Wikisource
edits": that phrasing *"was alarming and misleading. The edits to Wikisource
were not deferred, it is their incorporation into MAM-basics (and propagation
elsewhere from there) that was deferred."* All eleven edits are **live and
finished on Hebrew Wikisource**, made between 2026-08-30 and 2026-08-31.
Deferred is their download into `in/mam-ws/` and their propagation onward from
there. A short label that attaches "deferred" to the edits reads as though the
edits themselves were still owing on the wiki, which would be a different and
much worse state of affairs.

Between 2026-08-30 and 2026-08-31 Seth (Avi) Kadish made **twelve** meteg edits
to MAM on Hebrew Wikisource, each credited in the MAM change log to Daniel
Holman. **Exactly one of the twelve is a record of this programme**: 2 Kings
21:12, which is M18. Its log row reads "Removed 2 metegs
from עַל־יְרוּשָׁלַ֖͏ִם וִיהוּדָ֑ה following AC", which is what item 2's finding 2
met as an already-applied suggestion, second meteg and all.

**The other eleven are a different Holman batch and are in no ingest here.**
Checked 2026-09-03 against all 34 records of
`holman/docs-not-served/mam_suggestions.json`, whose three source messages are
Holman's workbooks of 2026-08-21 and 2026-08-27, four cases each, and his prose
list of 2026-08-31, thirty cases, titled "Fw: 30 More Corrections for MAM".
**That title is the tell**: the eleven reached MAM through an earlier
communication than any message this repository has ingested, so no M number
names them and no disposition of item 6 covers them.

**They are absent from `in/mam-ws/` because their chapters have not been
downloaded since 2026-08-26**, commit `77383ac4`, four days before the edits
were made. Every download since has been chapter-targeted — item 2's 22 removal
chapters plus 2 Kings 21, item 4's Joshua 10 and Zechariah 2, and item 3's 23
modified chapters — and **2 Kings 21 is the only one of the twelve on that
list, which is exactly why M18 was the only one this programme met.**

Measured 2026-09-03 in `in/mam-ws/`, all eleven still have the pre-edit form.
**Nine still have the meteg the edit removed** — Joshua 19:8, 1 Samuel 1:6, 1
Samuel 22:22, 2 Kings 6:23, 2 Chronicles 26:15, Isaiah 22:5, Isaiah 42:24,
Isaiah 50:7 and Zephaniah 3:13 — and **two still lack the meteg the edit
added**, 2 Chronicles 28:19 and Isaiah 24:18.

**Nothing is inconsistent, and that is what makes the gap cheap to defer.**
Both sides of the wsgo comparison lack the eleven equally, so item 5 step 5
reads empty for them whether or not they are picked up. MAM simply keeps the
pre-edit form at those eleven verses until a download reaches them, and item 5
step 6's mega run propagates that pre-edit form to every generated repository.

**What closes it**, whenever it is taken up: a chapter-targeted download naming
those eleven chapters — Joshua 19, 1 Samuel 1 and 22, 2 Kings 6, 2 Chronicles
26 and 28, Isaiah 22, 24, 42 and 50, Zephaniah 3 — then `py/main_diff.py wsgo`,
then a Google Sheet import-and-apply round of its own, then the mega run. A
full `py/main_download.py fr-wikisource` closes it too, and closes the whole
2026-08-26 gap with it, at the price of bringing down a week of edits nobody
here has reviewed.

### Item 6: archive the 30 records — DONE 2026-09-04

**All thirty are archived, and with the four accent-placement records already
there that makes all 34.** Committed as `e97bcc79`. Each of M1–M16, M18–M23,
M25–M31 and M33 has a `Disposition` entry in `DISPOSITION_BY_REF` in
`py/hkq_cmn/mam_suggestion_dispositions.py`, outcome "Suggestion taken",
`decided_by` "Ben Denckla". The entries were generated from
`holman/docs-not-served/mam_suggestions.json` rather than typed, each summary
naming the letter and the direction from that record's own `description`.

`decided_on` is **2026-09-03, not the execution date this item originally
named.** That is the day Ben took all thirty as a batch and the day the bot ran,
and the field records who decided rather than who typed; the four entries beside
them likewise carry the date Seth (Avi) Kadish decided, 2026-08-28.

**THE INGEST WOULD NOT RUN AT ALL, AND TWO REPAIRS WERE NEEDED BEFORE THIS ITEM
COULD BE DONE.** Both are consequences of item 5 landing rather than defects it
exposed by chance, and neither was foreseen here. `verify_mam_suggestions`'
`check_case` derives the atom a case is about by locating Holman's quoted MAM
form in the verse and asking which atom differs from his comparison form. **A
suggestion that has been taken leaves MAM without the form he quoted**, so once
item 5 landed all thirty quoted MAM forms occurred zero times and the first case
raised.

1. **The comparison form now anchors the derivation when the MAM form is
   absent**, that being what MAM has in such a case. The answer is unchanged
   either way, both runs having the same length and differing at one offset, and
   the evidence that it is unchanged is that `stated_atom_agrees` is still 34 of
   34. It still raises when NEITHER form occurs exactly once.
2. **The corrected quoted forms now reach `check_case`**, which
   `mam_suggestion_corrections`' docstring had already recorded as "a limitation
   rather than a choice". Joshua 10:12 needs it: MAM never had the U+05A8 qadma
   spelling Holman typed and no longer has the single-pashta form either, so only
   the corrected comparison form, the doubled pashta, is findable. The payload is
   unaffected, `apply_corrections` still rewriting it afterwards.

**The extract's own numbers corroborate the archiving rather than merely
reporting it.** `suppressed_case_count` goes 4 to 34 and
`comparison_form_already_present` goes 0 to 32, and the two cases where MAM does
not have the comparison form are exactly M17 and M32 — the two records whose
outcome is "Suggestion not taken". All 34 cards render on the Archived page and
none remains on the findings page.

**The mailbox is untracked and a worktree has none**, so the ingest was run as
`py/main_ingest_mam_suggestions.py --eml-dir C:/Users/BenDe/GitRepos/MAM-basics/.novc/eml-mam`,
pointing at the primary clone's copy. It reads only messages Holman sent and
skips the rest by sender, which it reports.

**Look up each record's actual `ref` field from the suggestions JSON by
`case_number`; do not construct it from the displayed "BookName ch:v.atom"
form.** `book_abbrev`, which `ref` uses (for example "2Ch"), differs from
`std_book_name`, which the display string uses (for example "2Chronicles"), so
a guessed ref fails to match silently.

The reader-facing rename of that page's label from "Suppressed" to "Archived"
is item 1's Phase 4, and was already done when this item ran.

### Item 7: refresh the mgketer comparison — DONE 2026-09-04

mgketer lives in `C:/Users/BenDe/GitRepos/MAM-private/mgketer` and is **outside
the MAM-basics pipeline**: `py/main_0_mega.py` does not reach it, and this
repository only ever reads its reports. Precondition:
`MAM-parsed/plus/<Book>.json` current for the seven affected books, from item
5's mega run.

```powershell
C:/Users/BenDe/GitRepos/MAM-private/mgketer/.venv/Scripts/python.exe py/main_diff.py --all
```

No re-scrape is needed, since mgketer's scraped data does not change when MAM
does, and no suppression entry is needed, since a diff simply disappears when
the texts agree.

**DONE 2026-09-04**, committed as MAM-private `5bb03b0` and `7ab3495` and
pushed. The by-type table moved as follows, counted as diff cards on the pages
themselves rather than read off the summary alone:

1. **"MAM adds meteg" falls from 67 to 37** — thirty cards leave and none
   arrives.
2. **"mgketer adds meteg" falls from 5 to 4**, the departing card being Isaiah
   23:12, M23 being the one record of the thirty that adds a meteg.
3. **"Meteg moved" stays at 5.**
4. **A new "Accent" page arrives with one card**, Zechariah 2:4. That is M34,
   whose munaḥ item 5 carried to the resh of זֵר֣וּ where mgketer has it on the
   zayin; the card is marked "AC lost", the Aleppo Codex not being extant there.
   Its page had to be added to git or `index.html` would link to nothing.

The non-common total therefore falls from **281 to 251**, which reconciles
exactly: minus 30, minus 1, plus 1.

**THIRTY CARDS LEAVE "MAM adds meteg" WHERE TWENTY-NINE RECORDS ASKED FOR IT**,
and this item's original guess that the drop would be "however many of the 28
non-M13 removals are extant" was wrong on both counts. All 29 removal records
dropped their card, and the thirtieth departure is a SECOND card at 2 Kings
21:12: one is M18's meteg on the resh of ירושלם, the other the meteg on the vav
of ויהודה, which no Holman record covers and which item 2's finding 2 predicted
would travel with it.

**JOSHUA 10:12 SHOWS NO DIFF HERE, AND THIS ITEM'S EXPECTATION OF ONE WAS
WRONG.** It said a new diff was expected because M24 gives MAM a pashta with its
stress helper where the Aleppo Codex transcription has the pashta alone. No such
card exists, before the refresh or after it — mgketer's Joshua report has the
same four cards either way and 10:12 is not among them. **mgketer strips stress
helpers by design**: its `py/python_modules/strip_stress_helpers.py` says
outright that "MAM includes these helpers; mgketer omits them. We strip them so
they don't produce false diffs", and pashta is one of the four postpositives it
handles. The massaged Joshua 10 token records the stripping, its `orig_text`
holding MAM's doubled pashta and its `text` the single pashta the comparison
sees. So the conclusion that the case needs no suppression entry stands, for the
opposite reason to the one given: there is no diff to suppress.

## The evidence notes, and where they live

Six of the seven files that are the evidence base for this programme are
tracked `doc/` files of this repository as of 2026-09-03, moved there from
`C:/Users/BenDe/.claude/plans/`, where they had been written while concurrent
work in git-tracked areas was unconcluded. Each opens by naming this document.
The seventh, the census script, stays untracked.

| Tracked note | What it holds |
|---|---|
| [`holman-meteg-m23-isaiah-23-12.md`](holman-meteg-m23-isaiah-23-12.md) | The M23 question, the Yeivin and Breuer sections for each post-stress type, the census summary, and the 1 Samuel 17:5 post-silluq case |
| [`holman-meteg-vs-mgketer.md`](holman-meteg-vs-mgketer.md) | The 30-row table of verses and forms, and the M13 and M22 special cases |
| [`holman-meteg-m13-qamats-template.md`](holman-meteg-m13-qamats-template.md) | M13's `{{מ:קמץ}}` template finding, which item 2 turns into two bot entries |
| [`holman-accent-placement-four.md`](holman-accent-placement-four.md) | M17, M24, M32 and M34 — the four records this programme excludes — and why Joshua 10:12 stays noisy |
| [`holman-suggestions-archived-terminology.md`](holman-suggestions-archived-terminology.md) | The five rendered uses of "Suppressed" that item 1 renames |
| [`post-stress-meteg-census-2026-09-03.md`](post-stress-meteg-census-2026-09-03.md) | The 2026-09-03 census output, the legacy baseline item 1's Phase 1 measures against |

**Three of the six carry a dated correction, and there are six corrections
among the three**, each marked `Correction, 2026-09-03` and placed beside the
claim it corrects rather than replacing it. Counted 2026-09-03: the M23 note
has three, the accent-placement note two, the terminology note one, and the
other three notes none. This paragraph enumerated three of them until that day,
omitting the accent-placement note's first correction entirely, and said five
until item 4's execution added the sixth. The six:

1. The M23 note's page location and name, left open when it was written, are
   settled by item 1's plan.
2. That same note's census figures are demoted to a legacy comparison baseline,
   the census script's verse-final test being defective.
3. That same note's closing section, "What this leaves for Ben to decide about
   M23", is demoted to background: nothing was left to decide, the acceptance
   of all thirty having preceded the research.
4. The accent-placement note leaves two "2026-09-05" dates as written, both
   postdating that note's capture and unexplained, on the ground that a date in
   an evidence note is itself evidence.
5. The terminology note's count of rendered "Suppressed" occurrences reads six
   where the measured count, and that note's own enumeration, is five.
6. The accent-placement note's propagation table puts the M34 fix in
   `in/mam-ws/` and in `MAM-parsed/plain/` when neither had it, and names the
   form זֵ֣רוּ as the fix, when זֵ֣רוּ is what the fix replaced. Measured while
   item 4 ran; item 4's section above carries the same measurement.

The census script that produced the census report stays at
`C:/Users/BenDe/.claude/plans/writing-only-to-a-robust-teapot-census.py` and
**cannot be tracked as it stands**: line 49 is a `sys.path.insert`, which
`~/.claude/CLAUDE.md` bans in tracked source at a count of zero per
repository. Its job is taken over by item 1's Phase 1 generator, so the report
is worth tracking and the script is not.

`although-the-forest-of-peppy-lampson.md`, in the same directory, belongs to
the **evacuation** programme rather than this one — see
[`PLAN-evacuate-the-rest-of-three-repos.md`](PLAN-evacuate-the-rest-of-three-repos.md).

## Preconditions common to every item

Another session may be live in MAM-basics or a sibling repository. Record HEAD,
inspect status, and record the intended-path list before editing; never stage a
path this programme did not touch. Items 4 through 7 reach MAM-parsed,
MAM-simple, MAM-with-doc, MAM-for-Sefaria, MAM-OSIS and MAM-private, none of
whose revisions were recorded when this programme was sketched — re-check all
of them before starting.

In a worktree, sibling repositories do not resolve by default:
`paths.repos_root()` returns `repo_root().parent`, which is the worktree's
parent rather than `GitRepos`. Set `REPOS_ROOT=C:/Users/BenDe/GitRepos`, or a
per-repository `REPO_<NAME>_DIR`, and the failure is loud rather than silent
either way.

**Item 2 needed neither, and the reason generalizes to item 3.** Nothing in
`py/main_download.py fr-wikisource`, `py/main_ws_bot.py`, `py/ws/` or
`py/subcommands/parse_ws.py` calls `sibling_repo` or `repos_root` — the one
sibling-reaching module in `py/ws/`, `ws_foi_kq_trivial_scope.py`, is imported
only by `ws_bot_edit_kq_triv_add_type.py`, which `ws_bot_edit.py` does not
import. Items 4 through 7 are a different matter, reaching MAM-parsed and the
rest.

**The test suite, though, wants the override even when the change under test
does not — set it and the suite is fully green in a worktree.** Measured
2026-09-03 in a worktree, with item 2's own changes in the tree:

```powershell
$env:REPOS_ROOT="C:/Users/BenDe/GitRepos"; C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q
```

gives **973 passed, 5 skipped, 0 failed**, and writes into no sibling
repository — all eight were clean before and after. The same run with no
override gives **904 passed, 34 failed, 35 errors** across eleven files, every
one of them reaching a sibling that resolves to `.claude/worktrees/<name>`.
904 + 34 + 35 = 973, so the override accounts for the whole difference and
nothing else is hiding in it. **Do not read an un-overridden total as a
baseline, and do not conclude from one that the suite cannot be run here**:
it can, and a full green total is the figure to measure against.

**That total moves as tests are added, so re-measure rather than reusing it.**
The 973 above was measured with item 2's changes in the tree; the same command
with item 3's, later on 2026-09-03, gives **975 passed, 5 skipped, 0 failed**.
The un-overridden figures are left as measured that morning and have not been
re-run, so the arithmetic above pins the 973 rather than the 975.
