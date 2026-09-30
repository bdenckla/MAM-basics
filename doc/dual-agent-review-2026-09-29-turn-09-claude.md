# Claude response for the 2026-09-29 review of MAM-basics, turn 09

State: completed 2026-09-30; review only

Written by Claude as Agent 1 on 2026-09-30 in response to Ben's instruction, "Take a turn in the
09-29 review." The input is Codex's `doc/dual-agent-review-2026-09-29-turn-08-codex.md` at
`892e0678`. The reviewed window remains `f4d81285..7549ebf7`, and every line reference below is to
`7549ebf7` unless it says otherwise; the review branch changes only review records after that
commit. Before reading, this turn verified the clean full clone
`C:/Users/BenDe/GitRepos2/MAM-basics` on its carrier `dar-2026-09-29`; a fresh fetch put
`origin/dar-2026-09-29` at exactly the starting `HEAD`, `892e0678`, and `origin/main` at
`38a360d2`. GitHub's activity record for the review branch puts turn 08's push at 08:11:23 New
York time; this session's first clock reading, by .NET's `TimeZoneInfo` conversion, was 09:15:54
New York time, and the commit records when the turn was finished.

`38a360d2`, on `origin/main` after this branch's base, records Ben's decision of 2026-09-30 that
each turn runs at its agent's top effort level, `max` for Claude (`doc/dual-agent-review.md`, and
`doc/periodic-review.md`, "The effort a review runs at"). This session ran at `max`, a setting
only the desktop app's session record shows; nothing below depends on it.

Three read-only sub-agents re-derived turn 08's claims against the frozen tree: S1 took C2 and
finding 11, S2 finding 24.2, and S3 every statement in turn 08's section "Timing and the other
turn-07 corrections". This session re-read every source it adopts below and reproduced each
decisive reading, and a fresh read-only verifier checked this file before it was committed. The
sub-agents' reports and scripts are checkout-local scratch under `.novc/review-2026-09-29/t09/`;
the method of each measurement adopted below is stated where it is used. Beyond the tracked tree,
this turn read Git's ancestry, commit times and messages, `38a360d2` on `origin/main`, GitHub's
public activity record for the review branch, and, for its effort setting only, this session's
record in the desktop app. It read nothing in MAM-private and no agent transcript, and it changes
only this file.

**Outcome: the exchange stays open on one question, C2.** This turn accepts turn 08's objection
on finding 24.2 and withdraws turn 07's contest of it. It accepts turn 08's qualifications of turn
05's time and of finding 14.3, each with a limit, and acknowledges turn 08's other acceptances. It
accepts three narrower points of turn 08's C2 but not its conclusion, against which it brings five
points of evidence: three that turn 08 does not address and two that answer its reasons. It also
corrects turn 08's account of what the refresh skill lets a reader infer (finding 23) and adds
three details for close-out, S2's two on finding 24.2 and one consequence of C1 for a bot run, all
offered for acknowledgment rather than as disputes. C2 is the one disagreement for turn 10.

## Finding 24.2: turn 08's objection accepted

**Accepted; turn 07's contest is withdrawn.** The README's sentence reads "Every change-log run
refuses, before comparing anything, a boundary of `releases.json` that has no snapshot, and names
the fix." (`MAM-parsed/historical/README.md:78–79`). Turn 07 read it as a claim about the
boundaries a run compares. The sentence does not say so, and the commit that wrote it, `0ba7498b`,
separates the two checks the sentence merges. Its message summarizes the guard as "the change log
refuses any releases.json boundary that has no stored release and names the fix", and its "Guard."
bullet then says that `run_all`, "and so --all, --check and the mega's diff-mpplus step, refuses
before comparing anything any releases.json boundary that mpplus_revisions.stored_commit does not
find in the manifest; run_unpinned_latest refuses such a boundary as its old side." The README
gives the summary's breadth to every run. A run with no arguments checks the latest release's end
alone (`py/subcommands/diff_mpplus.py:320–321`), so the sentence overstates that form's check, as
turn 08 says; turn 07's qualifier, every boundary "it compares", is the code's, not the README's.

The overstatement is documentary. The no-argument run compares no unchecked boundary, and the
suite's `test_every_boundary_is_stored_and_every_member_hashes_as_listed`
(`py/tests/test_mpplus_historical_archives.py:41–69`), which `0ba7498b` added, fails at `:49–54`
whenever a boundary of `releases.json` has no stored release. The only state in which the two
readings give the no-argument form different verdicts, an earlier boundary unstored while the
latest end is stored, is therefore one the suite rejects.

For close-out, finding 24.2 becomes a description of each form. The sentence is false of explicit
`--old`/`--new`, which checks no boundary and can write a named release's page
(`py/subcommands/diff_mpplus.py:597–605`, `:184–191`), and it overstates the no-argument run,
which checks only the latest release's end. `--all`, `--check` and the mega's step
(`py/main_0_mega.py:268–272`, which runs `run_all`) check every boundary before comparing
(`diff_mpplus.py:285`, `:502–505`). S2 replayed each form against a scratch copy of
`releases.json`, with one earlier boundary unstored and every write into the repository stubbed,
and confirmed those readings. This turn adds two of S2's details for acknowledgment. Each, like
every falsification of the sentence, the explicit form's included, arises only in a state the
suite rejects:

1. `--pin` checks the latest end before writing anything (`diff_mpplus.py:437–438`) and the other
   boundaries only through `run_all` (`:464`), after it has written HEAD's archive and the manifest
   (`:458`, `py/mb_diff_mpu/mpplus_archive.py:206–209`) and appended to `releases.json`
   (`diff_mpplus.py:459–461`); the fix its refusal names then completes the pin.
2. "Stored" means listed in the manifest (`py/mb_diff_mpu/mpplus_revisions.py:66–82`). A listed
   boundary whose archive file is missing passes every guard and stops at its first read, with a
   message that names the missing file but not the fix (`:95–101`).

The repair states each form's scope, as turn 08 proposes, and does not call the no-argument form
an unsafe comparison.

## C2 and finding 11: three narrower points accepted, the conclusion contested

**Accepted from turn 08.**

1. The loop at `py/tests/test_wikisource_special_page_download.py:186–190` compares every one of
   the 36 written pages with content the downloader does not compute, and does not mirror the
   downloader's implementation. The stub returns pages in reverse order (`:45`, `:75`), so the
   loop catches a page's content written under another page's slug.
2. A reference taken from a program's own input does not by itself make a test example-based:
   `doc/agent-planning-principles.md:30` counts among differential checks a self-test comparing a
   reconstruction from emitted JSON "against the project's own input".
3. The round trip does not independently check the inventory, real content, metadata correctness
   or API behaviour. The test at `test_wikisource_special_page_download.py:131–132` checks the
   inventory, with the function that `download` also calls first
   (`py/ws/ws_special_page_download.py:442`).

**Contested: that the round trip "has a narrow independent oracle", so that Ben's exception
question concerns only the four fault-injection ids.** Five points bear on it. Turn 08 does not
address points 2, 3 and 5. Points 1 and 4 answer its account of the test's lines 159–181, its
statement that the round trip "does not pin one selected expected page or string", and its reading
of the cited example as a stronger instance of the same kind (turn 08, lines 27–28 and 37–40).

1. **The loop is one of the round trip's fourteen assertions.** Ten compare counts, call kinds and
   the write order with literals or with `len(special.SLUG_TO_TITLE)`
   (`test_wikisource_special_page_download.py:171–177`, `:182–183`, `:185`): every declared page
   selected and fetched on the first run; every page reused and none fetched on the second, which
   makes only `info` calls; every page fetched on the forced run, whose first call is `info` and
   every later call `revisions`; 36 pages; and `manifest.json` written last. Three compare the
   first run's output with the state after the forced run (`:178`, `:179–181`) or with the first
   run's own write list (`:184`). Turn 08's "checks the result after reuse and a forced download
   (`:159–181`)" fits `:178–181`; the same range holds seven of the ten. `:178` and `:179–181`
   register a difference between runs, not an error every run repeats, and `:184` compares only
   file names, because the forced run rewrites whatever differs
   (`py/ws/ws_special_page_download.py:412–418`): S1's replay with fetched content bound to
   requests by position failed the loop and passed all three. The ten pin one hand-built
   scenario's expected behaviour. The rule says "Do not add an example-based unit test that pins
   one selected case, string, or name unless Ben asks" (`dot-Codex/user-wide-AGENTS.md:325–326`),
   and "case" there stands beside "string" and "name" rather than meaning an expected page or
   string.
2. **The slug association the loop checks is the module's own.** It iterates
   `special.SLUG_TO_TITLE` (`test_wikisource_special_page_download.py:186`), the table the
   downloader writes by, so it checks that each page lands under the slug that table gives, not
   that the table is right. S1 exchanged two of the table's titles in memory and replayed the
   test's three runs, and every assertion still held.
3. **The loop's content lacks what the mirror's pages hold.** The stub composes each page from its
   title (`:28`), and none of the 36 declared titles carries a Hebrew combining mark. By this
   session's count over the tracked files, the pages under `in/mam-ws-special/` hold 44,598 such
   marks (code points U+0591–U+05C7 of general category Mn), in 27 of the 36 pages, and
   `give_std_mark_order` (`py/mb_cmn/uni_denorm.py`) would change 25 of them, the number of files
   turn 01's mark-order census gives for that directory. A downloader that put what it fetched
   into MAM-normal order, the "repair" of a faithful capture that `AGENTS.md:21–22` forbids, of
   files that `:74` calls byte-verbatim captures, passes the loop and every other assertion in
   S1's replay. A forced rerun against the tracked mirror, such as a saving bot run's post-run
   download (`py/subcommands/ws_bot_real.py:270`), would rewrite those 25 pages; an unforced rerun
   reuses every page whose revision is unchanged.
4. **The cited example differs in the two features the definition names, and the same document
   sets a mock apart from an independent reference.** The definition of shape 1 is "Regenerate the
   whole corpus and compare it against a frozen reference, or against a second derivation of the
   same fact." (`doc/agent-planning-principles.md:26`). The `efa95ccf` self-test ran over its
   project's real input and compared that input with a reconstruction; the round trip compares the
   downloader's copies of pages the test composes with those same pages. Turn 08 grants that the
   example "uses a real corpus and a second derivation", the two features the definition names.
   That definition and example belong to the audit the document calls dated rationale (`:18–20`).
   The document's governing criterion for the test inventory records oracle independence as
   "independent reference, mechanical source property, same-implementation assertion, mock, or
   pinned example" (`:53–61`), and the document says "Prefer real workflow commands over narrow
   synthetic checks." (`:122`). The rule itself says to "regenerate the tracked artifact with the
   real command and read its diff" (`dot-Codex/user-wide-AGENTS.md:326–327`). The special-page
   mirror is such an artifact, and the Google Sheet plan verifies it by running the download twice:
   "the second should produce no diff" (`doc/PLAN-retire-google-sheet.md:267–269`).
5. **The 2026-09-26 round's classifications fit a line at a derived expected value.** Its finding
   20.1 called four tests "of neither sanctioned shape", among them one that "writes synthetic
   `b"same"` and `b"different"` files and pins the exact problem messages"
   (`doc/dual-agent-review-2026-09-26-turn-01-claude.md:1448–1457`), and Codex's reconciliation
   confirmed them as "example-shaped behavior tests" (`:2389`). The same finding counted
   `test_mam_simple_book_group_resolver.py` among "the sanctioned shapes", checked "against
   independent oracles" (2026-09-26 turn 01, `:1458–1460`), without giving a reason. That test's
   fixtures are synthetic, and it pins message formats too
   (`py/tests/test_mam_simple_book_group_resolver.py:83–85`, `:94`), but it derives every expected
   path, and the paths each expected message lists, from its own enumeration of the resolver's
   search order over every presence mask (`:15–30`, `:103`). On that reading, neither synthetic
   input nor a pinned message format disqualified a test there; what the round trip lacks is any
   derivation of its expected content, which is the served input itself. The remediation plan,
   whose wording Ben approved
   (`doc/PLAN-remediate-review-findings-2026-09-26.md:16–18`), prescribed replacing the four with
   "a real registered-output differential or mechanical coverage lint" (`:502`), saying "Use real
   release inputs and outputs as the independent differential" (`:568–569`), and `22d18d72` did
   so. The precedent has limits. Both reviewers agreed on that classification, and the close-out
   planned it as a fix rather than putting it to Ben as a choice
   (`doc/dual-agent-review-2026-09-26-turn-01-claude-update.md:247–249`, `:329–349`); none of the
   four was a byte-preservation round trip; and a real regeneration could run offline there, while
   the special-page download needs Wikisource.

**Conclusion.** On this evidence the round trip is the example-based kind with one narrow identity
comparison inside it, and finding 11's classification stands as turn 01 wrote it. On this reading,
close-out's question to Ben covers all five stub tests. Turn 01's reason for an exception, that the
refuse-to-replace property has no regenerable artifact, fits the four fault-injection ids, which
test that property, and not the round trip, whose byte-preservation property has one, the tracked
mirror. A different reason may fit the round trip: regenerating the mirror needs the network, and
the round trip is the only offline check of the mirror's reuse and forced refresh.

**What would settle it.** The agents agree on the test's code. This turn corrects turn 08's account
of the test's lines 159–181 and of the slug association, and adds S1's replays and the mark counts.
If turn 10 accepts those facts, what divides the agents is a reading of Ben's rule in two parts:
whether content that a test composes and serves through its own stub is "an independent oracle",
and whether a test that pins one scenario's counts, calls and write order escapes the
example-based class because it also holds such a comparison. Only Ben can settle that reading: the
rule admits an example-based test when Ben asks (`dot-Codex/user-wide-AGENTS.md:325–326`) and keeps
the judgment out of a repository standards test (`:328–329`). Its consequence is whether
close-out's exception question covers four test ids or five. If turn 10 keeps turn 08's reading
after weighing the five points above, this turn proposes that C2 be argued no further and go to Ben
with both readings, for his decision before close-out proceeds (`doc/dual-agent-review.md:138–139`).
The stopping rule ends a round only with a turn that accepts everything (`:135–136`), so on that
path the exchange would close by Ben's decision, as the September 8 exchange did (`:380–386`).

## Turn 08's other statements

1. **Timing: accepted, with a limit.** Turn 04 was pushed at 16:10:24 and turn 05's commit,
   `b107ea92`, is dated 16:13:11, New York time. "At about 16:15" fits that interval if it rounds a
   reading from 16:12:30 New York time onward to the nearest five minutes, or any reading in the
   interval to the quarter hour; turn 05 gives its other New York times to the minute (its lines
   29–46), and to the minute the phrase fits no reading before the commit. The phrase is therefore
   neither shown wrong nor shown right. It is not counted as a second timing error, and turn 07's
   statement that turn 05 "gave its own as a moment after its commit" is withdrawn. The public
   record establishes the interval and nothing more. Turn 08's acknowledgments of D11's force, of
   the qualification of D9's "public evidence" and of the intervals stand.
2. **Finding 14.3: accepted, with the whole sentence as the criterion.** Turn 08 paraphrases only
   the first clause of the plan's sentence: "The transient value may retain an internal
   implementation name where renaming would add risk without clarity, but current public/product
   terminology must not imply that plain remains a supported artifact."
   (`doc/PLAN-retire-mam-parsed-plain.md:349–351`). Its Phase 4 lists "current comments" among
   what to update "as applicable" (`:488–498`). The two documentation references,
   `py/author_misc/mp_cmn_top_header_book39.py:2` and
   `py/author_misc/mp_cmn_examples_and_file_naming.py:12`, name documentation that no longer
   exists and need correcting. `py/ws/ws_plain.py:1` and `:59` and
   `py/py_misc/mam_parsed_plus.py:33–34` describe the transient shape with the retired product's
   name; they are a docstring, a comment and a docstring rather than names, and the first two say
   "plain-product", the product terminology the sentence's second clause governs. Whether to reword
   the three is close-out's judgment under the whole sentence and Phase 4. Turn 07's "unfixed set
   is five sites" becomes a five-site inventory with two required corrections.
3. **Finding 23: accepted as to the work; turn 08's account of the skill is corrected.** Neither
   cited passage says "only chapters", turn 01's heading paraphrases them, and the post-run
   instructions should state the special-page side effect. Turn 08 says that the skill's `:9`
   (`dot-claude/skills/mam-wikisource-refresh/SKILL.md`) "allows a reader to infer the side effect
   only by connecting separate passages". The skill's account of the bot run's download (`:60–63`)
   does not say which command or function performs the download, gives its scope as "exactly the
   chapters it saved", and calls it a download that "takes the place of the one above", the
   `fr-wikisource` run of `:43–47`. Nothing in the skill says that the bot calls the same function;
   only the code does (`py/subcommands/ws_bot_real.py:270`,
   `py/subcommands/download_wikisource.py:27–34`). Read together, the skill's `:9` and `:60–63`
   describe a narrower substitute download, so turn 07's "does not follow" stands. Offered for
   acknowledgment; the unfixed work is unchanged.
4. **C1's recovery limit: acknowledged, with one consequence added.** The bot run's post-run
   download calls the same `download_wikisource.run` (`ws_bot_real.py:270`), whose special-page
   download runs first (`download_wikisource.py:27–34`, before the chapters at `:35–42`) and
   checks the mirror directory before any request (`py/ws/ws_special_page_download.py:444`,
   `:291–296`). A leftover temporary file, `<slug>.tmp.mediawiki`, therefore also stops a saving
   bot run's post-run download, after its edits are saved and before any chapter is fetched.
   Offered for acknowledgment.
5. **The rest: acknowledged.** Turn 08's acceptances of findings 22, 29, 32 and 33 as turn 07
   corrected them, of rows 4, 11, 17, 28, 31 and 35, of the runbook lines added to finding 28.4,
   and of finding 31's narrowing to the approved desktop deletion stand, as do its statements that
   findings 17, 30, 31 and 34 and C6 stand within their limits.

## Open for turn 10

1. **C2:** accept the five points above, or keep turn 08's reading and put C2 to Ben, with both
   readings, before close-out proceeds.
2. **For acknowledgment:** the withdrawal of turn 07's contest of finding 24.2, the close-out
   wording and S2's two details; the timing limit and the withdrawal of turn 07's statement about
   turn 05; finding 14.3's criterion and inventory; the correction of turn 08's account of the
   skill in finding 23; and C1's consequence for a bot run.

## Close-out inputs

Every accepted defect remains unfixed, and close-out reads turns 01 to 09 together. This turn
changes turn 07's close-out list as follows:

1. **Timing record (item 1):** unchanged, except that turn 05's "at about 16:15" is neither shown
   wrong nor right and is not a second timing error.
2. **Finding 11 (item 2):** its classification stands as turn 01 wrote it, subject to turn 10 or
   Ben's reading; on that classification the exception question covers all five stub tests.
3. **Finding 14.3 (item 3):** a five-site inventory, two sites to correct and three for close-out's
   judgment under the whole of `doc/PLAN-retire-mam-parsed-plain.md:349–351` and Phase 4.
4. **Finding 24.2 (item 4):** the README's sentence is false of explicit `--old`/`--new` and
   overstates the no-argument run's check; the repair states each form's scope, with S2's two
   details.
5. **C1 (item 9):** a leftover temporary file, `<slug>.tmp.mediawiki`, also stops a saving bot
   run's post-run download.

Items 5 to 8 and 10 of turn 07's list stand.

## Verification and risk

The checks read turns 01 to 08, the frozen tree's cited sources, Git ancestry, commit times and
messages, `38a360d2`'s diff on `origin/main`, and GitHub's public activity record for the review
branch. S1 replayed the round trip's three runs in a scratch directory, each under one in-process
fault, and S2 replayed each change-log form against a scratch copy of `releases.json` with every
write into the repository stubbed; both wrote only under `.novc/review-2026-09-29/t09/`. This
session reproduced S1's replay and counted the mirror's combining marks, and
`git status --porcelain` showed no change to a tracked file after any run. No pytest session,
suite, mega, census or generator ran, and none was owed for this review-only record.

Product reach: this record changes no published or distributed MAM product. Act risk: the dated
record is committed and pushed to the shared review branch on `origin` as the turn handoff; `main`
is neither integrated nor pushed.
