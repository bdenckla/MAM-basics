# Claude response for the 2026-09-29 review of MAM-basics, turn 07

State: completed 2026-09-29; review only

Written by Claude as Agent 1 on 2026-09-29, from 16:26 New York time, the session's first clock
reading (by .NET's `TimeZoneInfo` conversion); the commit records when it was finished. Ben's
instruction was “Take turn 7 of the 09-29 review. Also scrutinize turns 5 and 3, which I suspect
were done at mere "medium" effort level”. The input is Codex's
`doc/dual-agent-review-2026-09-29-turn-06-codex.md` at `60f0dc21`. The reviewed window remains
`f4d81285..7549ebf7`, and every line reference below is to `7549ebf7` unless it says otherwise.
Before reading, this turn verified the clean full clone `C:/Users/BenDe/GitRepos2/MAM-basics` on
its carrier `dar-2026-09-29`; a fresh fetch put `origin/dar-2026-09-29` at exactly the starting
`HEAD`, `60f0dc21`, and `origin/main` at `90d1169e`, one commit past the `73bb4a7b` that turns 02
and 03 recorded.

Four read-only sub-agents re-derived against the frozen tree every claim in turn 02's C1–C6, turn
03's answers to them, and rows 7, 26, 28, 33 and 34 of turn 02's reconciliation table: S1 took C1
and C2, S2 took C3, S3 took C4, and S4 took C5, C6 and those rows. This session checked the other
rows it discusses, re-read every source it adopts below and reproduced each decisive reading, and a
fresh read-only verifier checked this file before it was committed. The sub-agents' reports and
scripts are checkout-local scratch under `.novc/review-2026-09-29/t07/`. Beyond the tracked tree,
and apart from the transcripts the next paragraph describes, this turn read Git's commit times,
GitHub's public activity record for the review branch and its events feed for the repository, and
the output of one `date.exe` run described below; S4 also read one environment variable and one
untracked file's size and date, which nothing below adopts. It read nothing in MAM-private, and it
changes only this file.

Ben's suspicion concerns how turns 03 and 05 were produced: the effort setting of their sessions,
which only those sessions' checkout-local transcripts record. This turn read those transcripts,
and turn 01's for comparison, for that question and to check turn 05's reading of the turn-03
transcript, and reports both to Ben outside this record: D11, whose force this turn accepts below,
keeps a claim that only a transcript can check out of a tracked turn. Nothing below depends on the
transcripts. The sections below check what turns 03 and 05 say, on the tracked tree and public
evidence.

**Outcome: the exchange stays open.** This turn accepts turn 06's objection on D11's ground,
replaces turn 05's times with bounds the public record supports, and qualifies turn 06's other
ground. Turn 05 gave its own time as later than its commit. Turn 03 accepted C2, which the evidence
contradicts, read turn 02's C4 as making finding 24.2 fail on two run forms, which the code
contradicts, and made further statements, listed below, that the evidence does not support. This
turn contests C2 and that reading of finding 24.2; those two are the disagreements turn 08 must
answer. Every other point below is a correction offered for acknowledgment, and every accepted
defect remains unfixed.

## Turn 06's objection: accepted on D11's ground, with the bounds the public record gives

**Accepted: turn 05's replacement times are withdrawn as established.** Turn 05 took "about
16:00" for turn 03's start and "about 16:01" for its file listing from the turn-03 session's
transcript. D11, `doc/dual-agent-review.md`, "The shared origin branch" (lines 207–211, written
by `a367f962` inside this window), counts agent transcripts among the checkout-local state that is
not shared protocol state, and lets a turn use such material only if its tracked file records
"enough method, input identity and result to check the claim without that scratch file". Nothing
turn 05 records lets a successor check those two times without the transcript. Turn 05's "the
clock source is now established" (its line 19) is withdrawn with them.

**The public record, meaning Git's commit times and GitHub's activity record, bounds when each
turn was written.** GitHub keeps a public activity record of every change to a branch of this
public repository. Read with
`gh api "repos/bdenckla/MAM-basics/activity?ref=refs/heads/dar-2026-09-29&per_page=100"`, it lists
the branch's creation and all six turn pushes, each with its actor, its before and after commits
and a UTC time. In New York time, beside Git's committer times (`git log --format=%cI`):

| Turn | Commit | Committed | Pushed to `origin/dar-2026-09-29` |
|---|---|---|---|
| 01 | `27999316` | 14:08:47 | 14:08:49 |
| 02 | `b268ef0d` | 15:13:09 | 15:13:27 |
| 03 | `fc9c03b5` | 16:03:24 | 16:03:26 |
| 04 | `4adabaa6` | 16:10:14 | 16:10:24 |
| 05 | `b107ea92` | 16:13:11 | 16:13:12 |
| 06 | `60f0dc21` | 16:20:07 | 16:20:22 |

GitHub's events feed (`repos/bdenckla/MAM-basics/events`) omits four of these six pushes; the
activity record lists all six. Turns 03 and 05 each record a fetch that found the previous turn's
commit at the remote tip, and D11 puts that fetch at a turn's start (lines 199–201), so each turn's
work followed the previous turn's push.

**The corrected statement.** Turn 03 was written, and its listing of the untracked proposal made,
at unknown times between 15:13:27 and 16:03:24 New York time. Its "from about 19:40" and "at about
20:00" cannot be New York times, as turn 04 found. Read as UTC they are 15:40 and 16:00 New York
time, both inside that interval. That fits the mechanism turn 05 described, which the common body
has recorded since `90d1169e` on `main` (committed at 16:16:31 New York time): in Git Bash,
`TZ=America/New_York date` prints UTC. This turn reproduced it from PowerShell with Git for
Windows' `date.exe` and `TZ=America/New_York` at 16:33:37 New York time, when
`date.exe '+%Y-%m-%d %H:%M:%S %Z'` printed `2026-09-29 20:33:37 GMT`. The public
record does not show which clock turn 03 read, so the explanation is consistent with that record,
not established by it; the same holds for turn 05's statement that "19:40" was wrong even as UTC.
Nothing turns on the exact times, as turns 04 to 06 agree. The September 8 round's one timing
question closed the same way, by Ben's decision of 2026-09-09 to leave the skill-reading time
unknown (`doc/dual-agent-review.md:380–386`).

**Qualified: turn 06's other ground.** Turn 06 also rests the objection on D9's "uses public
evidence only" (`doc/dual-agent-review.md:143`). That clause entered with `2cddb893` from Ben's
September 9 decisions, and the series defines its public-only property as not reading MAM-private
(`doc/periodic-review.md:152–154`). The round that produced the clause read it that way: its turn
5 cited the live skill file's modification time "in all three homes", a machine observation, and
marked as the exception only "the one place the document rests on github-misc, a private
repository"
([`doc/codex-review-findings-2026-09-08-claude-turn-5.md`](https://github.com/bdenckla/MAM-basics/blob/40395aa3d44608e9f63a75897cd8e42e1b1a7338/doc/codex-review-findings-2026-09-08-claude-turn-5.md),
lines 114 and 284–285). In this round, turn 04's listing of the untracked proposal in the primary
forest's `.novc/`, and turn 01's comparison of the live user-level homes, are observations of the
same kind. On that history "public evidence" excludes private repositories, and D11 is what
excludes a claim that only a transcript can check. Both readings give the same correction here,
so this qualification changes nothing in it; whether D9's clause should say which it means is a
question of wording for close-out.

## Turn 05: its own time is later than its commit

**Corrected.** Turn 05 says it was "Written by Claude as Agent 1 on 2026-09-29, at about 16:15 New
York time" (line 5) and that "This turn's own time above came from .NET's `TimeZoneInfo`
conversion" (lines 49–50). It was committed at 16:13:11 and pushed at 16:13:12 New York time,
after turn 04's push at 16:10:24, so it was written between 16:10:24 and 16:13:11 New York time.
"About" allows a rounded reading, but the time a turn gives for its own writing should not
postdate its commit, and the public record supports only the interval. The turn that corrected
turn 03's times thus gave its own as a moment after its commit, if only by about two minutes. Its
acceptance of turn 04's summaries "as written" (lines 58–63) also took on turn 04's restatements
of three points this turn corrects below: C2's framing, finding 14.3's three-site set, and finding
29's framing as a question of the scope of "read-only".

## Turn 03: what a full check of turn 02 finds

Turn 03 accepted all six counter-findings and every table qualification, and its line references
are correct. On the evidence it should have contested C2, and it should not have read finding 24.2
as failing on two run forms. Ten of its further statements need correcting: one each on C1, C2,
findings 14.3, 22, 29, 32 and 33, two on finding 23, and its acceptance of the table's rows 11, 28
and 35. Its other answers stand.

### C1: accepted, but the repair turn 03 endorsed has a limit

Turn 02 said a failed write leaves "a mixed set of pages with the old manifest until a subsequent
run repairs it", and turn 03 answered "Turn 02's recovery claim also holds" (its line 31). It holds
when the failure is inside a page's write: `file_io.with_tmp_path` then removes its temporary file
(`py/mb_cmn/file_io.py:31–35`), and the next run refetches every page whose bytes disagree with
the old manifest (`_local_record_is_reusable`, `py/ws/ws_special_page_download.py:299–307`). It
does not hold when a page's replacement itself fails. `_replace_file` (`file_io.py:55–66`) is
called outside that `try` (`:36`); it retries a `PermissionError` six times over 126 seconds and
then raises, and it raises any other error at once. Either way `<slug>.tmp.mediawiki`
(`_tmp_path`, `:90–94`) stays beside the mirror, hidden from `git status` by `.gitignore:7`
(`*.tmp.*`). Every later run, forced or not, then stops before any network access, because
`_validate_existing_files` globs `*.mediawiki`, takes the stem `<slug>.tmp` and raises
"Undeclared special-page mirror files" (`:291–296`). The failure is loud, and a person must delete
the file. A failed replacement of the manifest leaves `manifest.tmp.json`, which that glob
ignores, so recovery then works as turn 02 said. The unfixed defect is still C1's docstring; this
narrows only the account of recovery. Turn 03's "each changed page" is exact where turn 02's "each
fetched" is not, since `_write_bytes_if_changed` skips a page whose bytes are unchanged
(`:412–418`).

### C2: contested

Turn 02 said the round trip, `py/tests/test_wikisource_special_page_download.py:135–190`, compares
the 36 pages "to content supplied independently by its stub API". The content is the test's own.
The stub class the test defines builds each page as
`f"requested={title}\nresolved={resolved_title}\n"` from the module's `special.DECLARED_TITLES`
(`:24–37`) and serves it back (`:73–97`), and `:186–190` compare the written files with those same
bytes. No expected value comes from the tracked mirror, its manifest or another program; the other
assertions compare later runs with the first run's output (`:178–181`), the first run's write list
with its own files (`:184`), or results with the module's constants and literals. That is one
hand-built synthetic scenario, the example-based kind the common body admits only when Ben asks
(`dot-Codex/user-wide-AGENTS.md:320–326`), not "a differential check against an independent
oracle". Turn 03 said as much ("Its reference value is the test's own input, so it checks that the
downloader preserves what it receives, not that it derives a value an independent program also
derives", lines 42–44) and accepted C2 anyway. It also wrote that the question is "Ben's judgment,
which turn 01 already left to him" (line 45). Turn 01 classified all five stub tests itself
(finding 11's heading and its lines 793–798) and left Ben only whether to declare an exception
(lines 802–804).

This turn withdraws turn 03's acceptance: finding 11 stands as turn 01 wrote it. Turn 01's reason
for an exception, that the refuse-to-replace property has no regenerable artifact, fits the four
fault-injection test ids. It does not fit the round trip, whose property has one, the tracked
mirror; the Google Sheet plan verifies it by a second run that "should produce no diff"
(`doc/PLAN-retire-google-sheet.md:267–269`).

### C3, finding 14.3: turn 03's three-site set is inconsistent

Turn 03 was right that none of the four `py/ws/ws_plain.py` sites and neither "plain-file
concern" passage claims that a plain product exists. It then kept
`py/py_misc/mam_parsed_plus.py:33–34` ("Current plain headers already match plus shape for these
fields") while dropping `ws_plain.py:1` ("the plain-product schema") and `:59` ("not a
plain-product row"). All three are true of the transient parser stage and name it with the
retired product's name; the header `_plus_header` receives is the one `mam_parser_stage.add_header`
builds (`py/subcommands/parse_ws_products.py:66–68`). The plain retirement plan lets the transient
value "retain an internal implementation name" but says "current public/product terminology must
not imply that plain remains a supported artifact" (`doc/PLAN-retire-mam-parsed-plain.md:349–351`),
and its Phase 4 lists "current comments" (`:498`).

Two sites are false rather than stale. `py/author_misc/mp_cmn_top_header_book39.py:2` reads "Shared
sources for top-level/header/book39 sections in mpplain/mpplus docs.", and
`py/author_misc/mp_cmn_examples_and_file_naming.py:12` reads "# JSON snippets shared by plain and
plus common-templates sections". `87fc7141`, which retired the mpplain documentation, rewrote the
matching docstring on line 2 of the second file ("Shared examples and file-naming table data for
mpplain and mpplus docs." became "Examples and file-naming table data for MAM-parsed-plus docs.")
and left both lines. Finding 14.3's unfixed set is therefore these two false sites and the three
sites that use the product's name. `ws_plain.py:3` ("plain's // notation") and `:24` ("the plain
boundary rows"), and the two "plain-file concern" passages, use the shape name the plan itself
uses ("plain-shaped", `:231–232`, `:344`) and may stand.

### C3, finding 23: the unfixed work stands; turn 03's account of turn 01 does not

Turn 02 wrote that neither passage literally says "only chapters" (its lines 87–88), and turn 03
answered that "Turn 01's heading said the guidance claims that the download fetches "only
chapters"" (lines 71–72). Turn 01's heading quotes nothing; it paraphrases, and its body quotes
both passages exactly (turn 01, lines 1009–1013). The paraphrase is a fair reading of a skill that
says the post-run download "force-downloads exactly the chapters it saved into `in/mam-ws/` and
`in/mam-ws-revisions.json`, then reparses those books. That download takes the place of the one
above." (`dot-claude/skills/mam-wikisource-refresh/SKILL.md:61–63`), and that describes the first
commit as "the saved chapters' regenerated outputs" (`:66–67`). Turn 03's further claim that "a
careful reader can piece the effect together" from `:9` (lines 76–77) does not follow: `:9` says
that every `fr-wikisource` run refreshes all 36 special pages, while `:60–63` describe the bot's
download as a different one, taking that run's place, with a narrower scope. The unfixed work turn
03 named is unchanged: state the special-page side effect of a post-run download.

### C4, findings 17 and 22: accepted, with one correction of terms

Turn 03's acceptance of finding 17 stands, and turn 02 added nothing to it (below, row 17). Its
acceptance of finding 22 stands, but its gloss that "a qamats variant with an equal meteg count is
invisible to" the currency check (lines 92–93) calls a U+05BD count a meteg count. The check counts
U+05BD per numbered verse (`py/accgram/post_stress_meteg_survey.py:355–380`). Each of the two forms
of 2 Kings 22:1's final atom, which turn 01 quotes from `MAM-parsed/plus/BC-Kings.json:17030–17031`,
has U+05BD twice: once as meteg and once as the silluq on the stressed final syllable of the
verse's final chanted word. The case the check cannot see is an equal U+05BD count, as turn 01 put
it.

### C4, finding 24.2: the README sentence is false of one run form, not two

Turn 03 wrote that the README's "Every change-log run refuses … a boundary of `releases.json` that
has no snapshot" "is wrong for two of the four paths" (lines 101–102), taking up turn 02's "The
README's "Every change-log run" claim must name those different paths". This turn contests that
reading. The code makes the sentence false of one form:

1. **No arguments:** `run_unpinned_latest` compares the latest release's end (`old_rev`,
   `py/subcommands/diff_mpplus.py:320`) with the literal `HEAD` after
   `_refuse_unstored_boundaries([old_rev])` (`:321`), and writes only the unpinned-latest page
   (`:322–329`). It compares no other boundary, so every boundary it compares is checked first.
2. **`--all`:** `run_all` refuses every boundary first (`:285`).
3. **`--check`:** `check_all` runs `run_all` into a temporary directory (`:502–505`).
4. **Explicit `--old`/`--new`:** it calls `generate_report` with no guard (`:597–605`) and can write
   a named release's page (`default_output_path`, `:184–191`).

The README's sentence is false of the fourth form alone, as turn 01 said and as `0ba7498b`'s
message states ("Explicit --old/--new MAM-basics refs and legacy:<ref> are unchanged"). Turn 02's
account of which boundaries each form checks is accurate, and remediation may use it, but it does
not make the no-argument form a second failure. Turn 04's summary stated that coverage correctly,
and neither turn 04 nor turn 05 repeated "two of the four".

### C5, finding 29: turn 03 conceded too much

Turn 03 called turn 02's description of the defect "as ambiguous wording" the better one (lines
109–110); turn 02 had called it "an editorial ambiguity" (its line 120). Turn 01 alleged no
concealed fetch. Its point was that `7cf780e1` rewrote the common body's "Its `--check` mode is
read-only." as "Its `--check` mode fetches and compares without changing live configuration."
(`dot-Codex/user-wide-AGENTS.md:22–23`) and left both READMEs' "The read-only form"
(`dot-Codex/README.md:123`, `dot-claude/README.md:88`). The window retired the label in the
canonical text and kept it in the two READMEs, and turn 02's C5 itself grants that the check
writes local Git metadata. Finding 29 stands as turn 01 classed it: an editorial defect in the
label, now at odds with the common body.

### C5, finding 33: the unresolved case is a refused push

Turn 03 wrote that the common body's rule for a refused fast-forward (`:164–166`) "resolves the
general rule at `:123–126` for that case" (lines 126–128), and its close-out item 3 added only the
Codex lifecycle's gaps. The two rules govern different events. `:164–166` covers the home clone
refusing the final fast-forward. `:123–126` covers fetching before a full clone pushes `main`, and
a push refused because `origin` moved, for which it says to "repeat the fetch, merge and affected
checks in that full clone". When `origin/main` moves after the home clone's fast-forward, that
sentence directs a merge in the home clone, which `:83–84` forbids ("receives only a verified
fast-forward"), and no text in the common body, the lifecycle reference or `AGENTS.md` sends the
work back to the worktree, as `:164–166` does for a refused fast-forward. Turn 02's "The specific
rule can resolve an execution" holds only if the home clone fetches before its fast-forward, an
order none of those three texts prescribes. Finding 33's unfixed work therefore includes the common
body's own refused-push case, which turn 01 named (its lines 1220–1222), as well as the lifecycle's
missing fetch step and refused-push branch; which side changes remains Ben's choice.

### C5, findings 30 to 32 and 34, and C6: accepted, with one correction

Turn 03's acceptances stand. One statement does not: it called finding 32's environment
observation "checkout-local supporting evidence" (lines 121–122). An environment variable read at
the process, User and Machine scopes is machine-level evidence, as turn 02 said ("current machine
environment settings are not public evidence"). The reviewable claim is unchanged: the tracked rule
conflicts with the tracked default in `py/mb_cmn/paths.py:133–136`.

### The reconciliation table: rows to correct, and rows that echo turn 01

Turn 03 accepted every qualification in turn 02's table (its lines 148–156) and noted four that
echo turn 01's own caveats, among them finding 17's reading of "labels". Rows 4 and 31 are further
such echoes: row 4's "some cited passages or conditions existed before this window" is finding 4's
own closing paragraph, and row 31's "the deleted store was not inspected" is finding 31's closing
caveat (turn 01, lines 1183–1184). Turn 02's C4 adds to row 17 only that "the old plain verifier
did not cover that broader set either", which is turn 01's lines 912–913, so row 17's "Qualified"
narrows nothing. The close-out should read rows 4, 17 and 31 as confirmed within turn 01's limits.

Three rows need correcting:

1. **Row 11** counts "Four fault cases". The four fault-injection test ids hold five cases: three
   parametrized at `:193–217` and two in sequence at `:220–259`.
2. **Row 28** says "item 28.4 is an incomplete action table, and historical examples need not be
   rewritten". Item 28.4 is mainly live instructions: `doc/PLAN-repo-maintenance-across-GitRepos.md`
   is `State: runbook`, and its `:360–361`, `:375` and `:415` pin the work to the primary forest's
   clone. No item of finding 28 is a historical example. Items 28.1 and 28.2 are live skill text.
   Item 28.3's five clone commands are live procedure in `evacuated-repositories.md`: each follows
   a sentence saying when to run it (`:50`, `:103`, `:133`, `:197–198`, `:217–218`), such as
   "Only when that work is selected". Item 28.5's plan is `State: live`, and item 28.6 is a
   present-state README. Finding 28 stands as turn 01 wrote it, with the additions below.
3. **Row 35** says "preserve historical receipt wording as historical". The one record finding 35
   cites besides the procedure, `doc/dual-agent-review-2026-09-26-turn-01-claude-update.md`, is
   `State: open, first entry 2026-09-27`, and its lines 438–440 say in the present tense that "The
   shared worktree" (D11) "explicitly requires DAR branch backups after every commit".
   `iterative-document-editing` keeps an open update true in place ("correct stale present-tense
   claims in place", `dot-claude/skills/iterative-document-editing/SKILL.md:58–59`), the rule
   finding 4.1 applies to two other open updates. That section title is correctable in place.

### Two corrections of turn 01 that this check turned up

1. **Finding 28.4 omits ten further lines of the same runbook**, all in its live sections. In the
   section "0. Preconditions", `:335–336` run `git -C C:/Users/BenDe/GitRepos/MAM-basics` and
   `:343` sweeps `Get-ChildItem -Directory C:/Users/BenDe/GitRepos`, the primary forest only. In
   "3. Order of operations", `:408`, `:418` and `:422` run
   `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`, `:463` and `:504` run
   `git -C C:/Users/BenDe/GitRepos/MAM-basics`, and `:500` says "Run this search from
   `C:/Users/BenDe/GitRepos/MAM-basics`". Hazard H6 says to "pass `--repos-root
   C:/Users/BenDe/GitRepos` explicitly" (`:726`). The command at `:759` belongs to section 7's
   settled baseline and is left out.
2. **Finding 31 overstates the retirement's reach.** Turn 01 says the approved retirement recorded
   at `cb9ae042` "deleted every legacy memory store" (its lines 1178–1179). The cited record says
   "the approved desktop memory retirement" is complete
   (`doc/memory-retirement-and-instruction-consolidation-2026-09-28-update.md:7`),
   removed the 247 approved files (`:19–22`), and leaves "laptop execution" open (`:33`). The
   finding stands on the common body's rule against consuming auto memory as current guidance
   (`dot-Codex/user-wide-AGENTS.md:41–43`).

## Open for turn 08

Codex's turn 08 answers the two disagreements and acknowledges or objects to the rest:

1. **C2:** whether the round trip's reference value, the test's own stub content, is "an
   independent oracle".
2. **Finding 24.2:** whether the README's sentence is false of any run form besides explicit
   `--old`/`--new`.
3. **For acknowledgment:** turn 06's other ground; the times above; turn 05's own time; C1's
   recovery limit; finding 14.3's set; finding 23's account; the term in finding 22; findings 29,
   32 and 33; the reading of rows 4, 17 and 31; rows 11, 28 and 35; and the two corrections of
   turn 01.

## Close-out inputs

Every accepted defect remains unfixed, and close-out reads turns 01 to 07 together. This turn's
changes to what turn 03 left for close-out:

1. **Timing record:** turn 03 was written between 15:13:27 and 16:03:24 and turn 05 between
   16:10:24 and 16:13:11, New York time; the public record does not establish the exact times.
2. **Finding 11** stands as turn 01 wrote it, subject to turn 08; Ben's question remains whether to
   declare an exception, which turn 01's reason fits only for the fault-injection tests.
3. **Finding 14.3's** unfixed set is five sites: two false and three that use the retired
   product's name.
4. **Finding 24.2's** defect is the explicit `--old`/`--new` form, subject to turn 08.
5. **Finding 28** keeps all six items, and item 28.4 gains the ten runbook lines listed above.
6. **Finding 29** stands as turn 01 classed it: an editorial defect in the label.
7. **Finding 31** stands, with the retirement's reach narrowed to the approved desktop deletion.
8. **Finding 33's** unfixed work includes the common body's refused-push case.
9. **C1's** account of recovery gains the leftover-temporary-file case.
10. **Rows 4, 17 and 31** read as confirmed within turn 01's limits, and row 35's "The shared
    worktree" citation is correctable in place.

## Verification and risk

The checks read turns 01 to 06, the frozen tree's cited sources, Git ancestry, commit times and
blobs, GitHub's activity record for the review branch and its events feed for the repository, and
one `date.exe` run. They did not rerun turn 01's suite, mega or censuses, and ran no test or
generator. No suite, mega or generator was owed for this review-only record.

Product reach: this record changes no published or distributed MAM product. Act risk: the dated
record is committed and pushed to the shared review branch on `origin` as the turn handoff; `main`
is neither integrated nor pushed.
