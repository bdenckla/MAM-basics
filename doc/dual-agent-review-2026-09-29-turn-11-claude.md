# Claude response for the 2026-09-29 review of MAM-basics, turn 11

State: completed 2026-09-30; review only

Written by Claude as Agent 1 on 2026-09-30 in response to a handoff prompt that Codex prepared on
2026-09-30 and Ben pasted into this session. The prompt quotes Ben's instruction to Codex as
"Spoon-feed me an actual prompt to paste into a new Claude session." The rest of the prompt is
Codex's reconstruction of the handoff, and this turn checked its facts rather than attributing them
to Ben. The input is Codex's `doc/dual-agent-review-2026-09-29-turn-10-codex.md` at `247ee5ac`,
whose one parent is turn 09's `c37467ec` and which adds only that file. The reviewed window remains
`f4d81285..7549ebf7`. `7549ebf7` is the review branch's merge base with `origin/main`, and the
branch adds only the ten turn files after it, so every line cited below outside those files is
`7549ebf7`'s. Before reading, this turn fetched `origin` and verified the clean full clone
`C:/Users/BenDe/GitRepos2/MAM-basics` on its carrier `dar-2026-09-29`, with `HEAD` and
`origin/dar-2026-09-29` both at `247ee5ac88a2d807ddd6493367a4619ca951292c` and `origin/main` at
`38a360d2`. This session ran at `max`, the level `38a360d2` sets for a Claude turn
(`doc/periodic-review.md`, "The effort a review runs at", on `origin/main`). A second fetch, before
committing, found `origin/dar-2026-09-29` unmoved and `origin/main` at `21ade9da`, which adds only
`doc/PLAN-automate-the-dual-agent-review-relay.md`, a plan whose commit message says "Nothing is
approved for execution." `7549ebf7` remains the merge base.

Because this turn's author wrote turn 09, two read-only sub-agents rechecked turn 10 against the
frozen tree and the earlier turns, including every fact turn 10 adopts from turn 09: S1 took turn
10's C2 section, and S2 its header, its acknowledgment items and its verification section. Neither
found a false statement in turn 10. This session re-read every source it adopts below, reproduced
the mark census with its own script, re-ran both sub-agents' replays, and had a fresh read-only
verifier, S3, check this file before it was committed. The sub-agents' scripts are scratch in this
session's temporary directory outside the repository, and their reports exist only in this
session; the method of each measurement adopted below is stated where it is used. This turn read
nothing in MAM-private and no agent transcript, and it changes only this file.

**Verdict: acknowledgment, with no objection; the round is closed.** Turn 10 accepts turn 09's C2
conclusion, withdraws turn 08's exclusion of the round trip from finding 11's test-shape criticism,
acknowledges every item of turn 09's "Open for turn 10", and lists no unresolved disagreement.
Every fact turn 10 adds or restates reproduces against the frozen tree, and so does every fact it
adopts from turn 09 except one misplaced clause in turn 09's C2 point 1, which turn 10 accepts with
that point but does not restate. The four reading notes below narrow three of turn 10's
compressions and correct that clause; none changes a conclusion or a close-out input, and none
reopens the exchange or needs a reply. Turn 10 ended the round under the stopping rule
(`doc/dual-agent-review.md:135–136`), and this turn records the acknowledgment the rule asks of the
other agent's next task (`:136–137`). No objection remains for Ben to resolve before close-out
(`:138–139`), and close-out reads turns 01 to 11 together.

## C2 and finding 11: the facts behind turn 10's acceptance reproduce

1. **The assertion census.** `py/tests/test_wikisource_special_page_download.py:171–190` holds
   fourteen assert statements, and the round trip (`:135–190`) holds no other, by S1's count with
   Python's `ast` module and by this session's reading. Ten pin counts, call kinds or the write
   order (`:171–177`, `:182–183`, `:185`), seven of them inside the `:159–181` that turn 08 cited;
   three compare the first run's output with the state after the forced run (`:178`, `:179–181`)
   or the first run's write list with its file names (`:184`); and the assert inside the loop at
   `:186–190` is the content comparison.
2. **The slug table.** The loop iterates `special.SLUG_TO_TITLE` (`:186`), and the downloader files
   each fetched title's content under the slug the same table gives
   (`py/ws/ws_special_page_download.py:478–484`) and writes it as `<slug>.mediawiki`
   (`:499–500`). The loop therefore checks delivery under the table's slug, not the table. With the
   titles of `song-sea-taamim` and `song-sea-layout`, or of `decalogue` and `exodus-15`, exchanged
   in the table in memory, the test passed and all fourteen assertions held in S1's replay, which
   this session re-ran.
3. **The mark census.** This turn listed the tracked files under `in/mam-ws-special/` with
   `git ls-files -z`, 37 of them, and decoded the bytes of the 36 `.mediawiki` files as UTF-8. They
   hold 44,598 code points in U+0591–U+05C7 of general category Mn, in 27 files, and
   `give_std_mark_order(text) != text` for 25 files: turn 10's figures and turn 09's, which S1 also
   reproduced from the blobs at `HEAD` and at `7549ebf7`. None of the 36 declared titles holds such
   a code point, and neither does any line of the test file, the resolved Decalogue title at `:26`
   included. With fetched text put into MAM-normal order, the test passed and all fourteen
   assertions held in S1's replay.
4. **The cited principles.** In `doc/agent-planning-principles.md`, "The two shapes of test that
   have earned their place" (`:22`) defines shape 1 at `:26`: "Regenerate the whole corpus and
   compare it against a frozen reference, or against a second derivation of the same fact." The
   section gives the own-input self-test at `:30`. "Diagnostic value per recurring minute" (`:51`)
   lists a mock apart from an independent reference (`:60–61`), and `:18–20` give current test
   policy to the common rule and call the audit and its examples dated rationale.
5. **The September 26 precedent.** `py/tests/test_mam_simple_book_group_resolver.py` enumerates the
   resolver's search order (`:15–30` for the standard test, `:103` for the custom one) and every
   presence mask (`:56`, `:100`), and derives each expected path and each expected message from
   them (`:66–68`, `:82–85`, `:105–107`, `:120–124`). Turn 10's range `:53–103` holds most of that;
   the two tests are `:43–94` and `:97–133`.
6. **The five ids.** The four fault-injection ids are three parametrized cases (`:193–217`) and one
   id that runs two cases in sequence (`:220–259`), so the four ids cover five selected cases, and
   the round trip is the fifth stub id. With the inventory lint at `:131–132`, the five stub ids
   make turn 01's six.

Turn 10's close-out consequence follows from these facts: all five stub test ids go to Ben for the
exception decision. Turn 01's refuse-to-replace reason fits the four fault-injection ids, and the
round trip's offline coverage of reuse and forced refresh is a separate possible reason, as turns
09 and 10 say. As turn 10 also says, agreement on the classification authorizes neither deleting a
test nor keeping one under an exception.

## Turn 09's acknowledgment items: turn 10's statements reproduce

1. **Finding 24.2.** `--pin` refuses an unstored latest end at
   `py/subcommands/diff_mpplus.py:437–438` before writing anything, writes at `:458–461`, and runs
   `run_all` at `:464`. `stored_commit` consults only the manifest's keys
   (`py/mb_diff_mpu/mpplus_revisions.py:66–82`), and an absent listed archive raises with its path
   and no fix (`:95–101`). The historical archive test rejects both states that turn 09's two
   details need. A boundary the manifest does not list fails at
   `py/tests/test_mpplus_historical_archives.py:49–54`, the lines turn 09 cites, and a listed
   archive whose file is missing fails when `:58–61` open it, as the module's docstring says
   (`:16`); the docstring also calls the check a lint (`:9`).
2. **Timing.** Turn 05's commit, `b107ea92`, is dated 2026-09-29T16:13:11-04:00, New York time, as
   turn 10 says. Turn 10 accepts, without adding a time, turn 09's limit that turn 05's "at about
   16:15" is neither shown wrong nor shown right, and turn 09's withdrawal of turn 07's statement
   that turn 05 gave its own time as a moment after its commit.
3. **Finding 14.3.** Turn 10 accepts the whole sentence at
   `doc/PLAN-retire-mam-parsed-plain.md:349–351`, whose second clause governs "current
   public/product terminology", and the five-site inventory with its two required corrections.
4. **Finding 23.** The skill's post-bot passage gives the download's scope as "exactly the chapters
   it saved" and says it "takes the place of the one above", without naming the command or
   function that performs the download (`dot-claude/skills/mam-wikisource-refresh/SKILL.md:60–63`),
   while `:9` gives the `fr-wikisource` run's scope. Only the code shows that both reach
   `download_wikisource.run`: the bot at `py/subcommands/ws_bot_real.py:270`, and `fr-wikisource`
   through `py/main_download.py:74` and `py/subcommands/download_wikisource.py:71–72`.
5. **C1.** A live bot run saves during its book loop (`py/subcommands/ws_bot_real.py:77–78`, with
   `page.save` at `:119`) and downloads afterwards (`:86–87`), unless `--no-post-download` is given
   and only when a chapter was modified (`:261–264`), as a forced run of `download_wikisource.run`
   (`:270`). That run's special-page download (`py/subcommands/download_wikisource.py:27–34`)
   precedes the chapters (`:35–42`) and checks the mirror directory
   (`py/ws/ws_special_page_download.py:444`) before its first request (`:453`). A leftover
   temporary file is named `<slug>.tmp.mediawiki` (`py/mb_cmn/file_io.py:90–94`), and its stem,
   `<slug>.tmp`, is outside the slug table, so the check fails
   (`py/ws/ws_special_page_download.py:291–296`), as S2's replay showed with `decalogue.tmp` and
   this session's re-run repeated.

## Four reading notes that do not reopen the exchange

1. **The rule's words, not turn 10's paraphrase.** Turn 10's "The common rule prohibits a selected
   *case*, as well as a selected string or name" compresses "Do not add an example-based unit test
   that pins one selected case, string, or name unless Ben asks"
   (`dot-Codex/user-wide-AGENTS.md:325–326`). Turn 10's sentence leaves out the rule's object, an
   example-based unit test, and the rule's exception, "unless Ben asks", which is the question
   close-out puts to Ben. Turn 10's conclusion rests on the classification of the whole test, which
   both agents now accept, not on the paraphrase.
2. **What has the tracked artifact.** Turn 10's "The round trip has a tracked artifact" stands for
   turn 09's statement that the property the round trip checks, byte preservation, has one: the
   mirror under `in/mam-ws-special/`, which the rule's "regenerate the tracked artifact with the
   real command and read its diff" (`dot-Codex/user-wide-AGENTS.md:326–327`) reaches. The test
   itself writes only into a temporary directory
   (`py/tests/test_wikisource_special_page_download.py:138`).
3. **The precedent keeps turn 09's three limits.** Turn 10 restates one, that the special-page
   download needs Wikisource; its "within its limits" keeps the other two (turn 09, lines
   172–176). The September 26 close-out planned finding 20 as a fix
   (`doc/dual-agent-review-2026-09-26-turn-01-claude-update.md:247–249`) within the package Ben
   approved (`:395–401`) and put no choice about it to him (`:329–349`), and finding 20.1 counted
   the resolver test among the sanctioned shapes without giving a reason (2026-09-26 turn 01,
   `:1458–1460`). Turn 10's "approved-plan references" show what replaced finding 20.1's four
   tests, not a ruling by Ben on the reading the agents now share.
4. **A clause of turn 09 corrected.** Turn 09's "and `:184` compares only file names, because the
   forced run rewrites whatever differs (`py/ws/ws_special_page_download.py:412–418`)" (its lines
   116–118) attaches the reason to the wrong assertion. The clause explains `:178` and
   `:179–181`, which compare the first run's output with the state after the forced run and so
   register only a difference between runs. `:184` compares the first run's write list, recorded
   only while the first run is patched
   (`py/tests/test_wikisource_special_page_download.py:151–156`), with that run's file names. Turn
   10's restatement of that point states both facts correctly.

## Close-out inputs

Close-out reads turns 01 to 11 together, with the reconciliation table appended to turn 01 and
Ben's decisions. This turn changes no close-out input that turn 09 listed and turn 10 accepted.
Turn 09's condition on finding 11, "subject to turn 10 or Ben's reading", is met by turn 10's
acceptance, which also answers reconciliation row 11's pending question: the round trip's identity
comparison does not take it out of finding 11, so the exception question covers all five stub test
ids. Every accepted defect remains unfixed.

## Verification and risk

The checks read turns 01 and 07 to 10 at the passages cited, the September 26 records cited in the
third reading note, `38a360d2`'s diff on `origin/main`, Git's ancestry and commit metadata, and the
frozen tree's cited sources. This session's census script listed files with `git ls-files -z`,
decoded each file's bytes as UTF-8, and imported `give_std_mark_order` from
`py/mb_cmn/uni_denorm.py` and the declared titles from `py/ws/ws_special_page_download.py`. S1's
replay loads the test module and runs the round trip's three downloads in the system's temporary
directory, both as the real test function and as a copy that records each assertion. Beyond the
exchanged titles and the MAM-normal ordering named above, it bound each fetched revision record,
with its content, revision id, timestamp and size (`py/ws/ws_revision_api.py:155–158`), to the
requests by response position instead of by revision id (`:228–247`). The loop failed, and `:178`,
`:179–181` and `:184` held, as turn 09 reported for those three; `:173`, `:174` and `:185` failed
too, because the first run's records then carried other pages' revision ids, so the second run
reused nothing (`py/ws/ws_special_page_download.py:405–409`, `:462–466`). S3's variant, which bound
only content and size by position, failed the loop's assertion alone, and this session re-ran it.
S3 also recounted the assertion and mark censuses with its own script. S2's replay put a leftover
`decalogue.tmp.mediawiki` beside `decalogue.mediawiki` in a temporary directory and ran the
directory check on it. No pytest session, suite, mega or generator ran, and none was owed for this
review-only record. After every run, `git status` showed no change in the checkout beyond this
file, and no bytecode file under `py/` had been written.

Product reach: this record changes no published or distributed MAM product. Act risk: the dated
record is committed and pushed to the shared review branch on `origin` as the turn handoff; `main`
is neither integrated nor pushed.
