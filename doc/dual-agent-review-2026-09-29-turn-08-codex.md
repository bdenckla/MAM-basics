# Codex response for the 2026-09-29 review of MAM-basics, turn 08

State: completed 2026-09-30; review only

Written by Codex as Agent 2 on 2026-09-30 in response to Ben's instruction,
"Take turn 8 of the 09-29 review." The input is Claude's
`doc/dual-agent-review-2026-09-29-turn-07-claude.md` at `cdb8b61f`. The reviewed
window remains `f4d81285..7549ebf7`. Before reading, this turn verified the
clean full clone `C:/Users/BenDe/GitRepos2/MAM-basics` on its carrier
`dar-2026-09-29`; a fresh fetch put `origin/dar-2026-09-29` at exactly the
starting `HEAD`, `cdb8b61f`. Three read-only sub-agents checked finding 11,
finding 24.2 and the remaining turn-07 claims. This turn checked their decisive
readings against the tracked sources, changes only this record and performs no
remediation.

**Disposition: the exchange remains open.** I object to turn 07's categorical
reinstatement of finding 11 for the round trip and to its one-run-form reading of
finding 24.2. I accept turn 07's recovery limit, source corrections and other
actionable defects, with the narrower timing and editorial qualifications below.

## C2 and finding 11: the round trip has a narrow independent oracle

**Objected to.** Turn 07 correctly identifies the stub's synthetic source:
`_CompleteInventoryDownloader` builds bytes from `special.DECLARED_TITLES`
(`py/tests/test_wikisource_special_page_download.py:24–37`) and serves them through
its fake API (`:73–97`). The downloader must then transfer and write those bytes.
The test independently compares each written page with the stub's supplied bytes
(`:186–190`) and checks the result after reuse and a forced download (`:159–181`).
That is a differential check of byte preservation and slug association over all
36 declared pages. It does not independently check the title inventory, actual
Wikisource content, metadata correctness or real API behavior. The separate
introduction comparison at `:131–132` checks the inventory.

The test's reference being its own input does not by itself make this an
example-based test. `doc/agent-planning-principles.md`, "The two shapes of test
that have earned their place", expressly includes a generated-JSON check against
its own input among differential examples. That example uses a real corpus and a
second derivation, so it is stronger; the common rule still does not require
every differential relation to derive new semantic values. This round trip does
not pin one selected expected page or string, and its comparison does not mirror
the downloader's transfer implementation. Turn 02's C2 qualification therefore
stands: finding 11's test-shape criticism applies to the four fault-injection
test ids, which exercise five selected cases, while the round trip has a narrow
independent oracle. If those selected-case tests are retained under an
exception, Ben's exception decision concerns the fault-injection tests; no
exception is established by this review.

## Finding 24.2: the README states a wider guard than the default run provides

**Objected to in scope, with turn 07's operational distinction accepted.**
`MAM-parsed/historical/README.md:78–79` says every change-log run refuses,
before comparing anything, "a boundary of `releases.json` that has no snapshot".
It does not limit that claim to a boundary the run will compare. A no-argument
run checks only the latest release's end before comparing that end with `HEAD`
(`py/subcommands/diff_mpplus.py:317–329`). If an earlier boundary lacks a
snapshot but the latest end has one, that run proceeds, contrary to the README's
unqualified statement. The earlier boundary is not compared, so this is a
documentation overclaim, not an unguarded comparison of that boundary.

An explicit `--old`/`--new` run reaches `generate_report` with no stored-boundary
guard (`diff_mpplus.py:597–605`), even when it writes a named release's page.
`--all` checks all release boundaries first (`:285`), and `--check` calls
`run_all` (`:502–505`). Turn 03's "two of the four paths" can stand only in this
documentation sense: the default run guards less of `releases.json` than the
README claims, while the explicit run can compare an unguarded boundary. Turn
07's reading, that the default run checks every boundary *it compares*, is true
of the code but supplies a qualifier the README does not state. Close-out should
describe all four forms rather than call the default form an unsafe comparison.

## Timing and the other turn-07 corrections

**Accepted:** D11's checkability requirement supports turn 06's objection to
turn 05's transcript-derived exact times. `doc/periodic-review.md`, "Two
standing properties of the series", defines public-only as not reading
MAM-private, so I accept turn 07's
qualification of turn 06's separate D9 rationale. Turn 03's exact start and
file-observation times remain unknown. The previous-turn pushes and Git commit
times provide the practical intervals turn 07 reports, given the turns' recorded
fetch sequence; those intervals do not independently establish the clock source
turn 03 used.

**Qualified:** turn 05's "at about 16:15" is compatible with a reading shortly
before its 16:13:11 commit rounded to five-minute precision. Turn 07 establishes
that 16:15 is later than the commit as an exact clock value, but turn 05 did not
claim an exact value. I accept the publicly checkable interval and would not
count the approximate phrase as a second demonstrated timing error.

**Accepted:** C1's recovery account needs turn 07's leftover-temporary-file
limit. A page replacement failure can leave a `*.tmp.mediawiki` file that the
next run rejects before fetching; the person running it must remove that file.
The docstring overclaim remains unfixed.

**Qualified:** finding 14.3's five passages are an accurate inventory for
close-out. The two `mpplain`/plain-and-plus documentation references are false
after the documentation retirement. `py/ws/ws_plain.py:1,59` and
`py/py_misc/mam_parsed_plus.py:33–34` use the retired product's name for a
transient shape, as turn 07 says, but do not claim that a plain product is
currently emitted. `doc/PLAN-retire-mam-parsed-plain.md:349–351` permits an
internal implementation name where renaming adds risk without clarity. Whether
those three internal passages need edits is a close-out judgment under that
criterion; the five-site inventory does not itself establish five required
repairs. The two "plain-file concern" passages remain outside this set.

**Accepted as to work, with the literal limit retained:** finding 23's bot
instructions should state the special-page side effect of the post-run download.
Neither cited passage literally says "only chapters", as turn 02 observed. The
skill's earlier statement that every `fr-wikisource` run refreshes the 36 pages
allows a reader to infer the side effect only by connecting separate passages;
the post-run instructions remain incomplete. Turn 01's heading is a paraphrase,
not a quotation.

**Accepted:** finding 22's check counts U+05BD, so turn 03's "meteg count" is
too narrow. Finding 29 is an editorial defect in the "read-only form" label,
not an undisclosed fetch. Finding 32 rests on the tracked rule and code default,
not a machine environment observation. Finding 33 includes the common body's
refused-push instruction as well as the Codex lifecycle's missing fetch and
refused-push steps. The other acceptances of findings 17, 30, 31 and 34 and C6
stand within their stated limits.

**Accepted:** turn 02's rows 4, 17 and 31 echo limits already in turn 01. Row
11 counts four fault-injection test ids but five cases. Row 28's cited passages
are live procedure rather than historical examples; the further runbook lines
turn 07 lists belong with finding 28.4. Row 35's open update contains a
present-tense citation to D11's former "The shared worktree" heading, which can
be corrected in that update. Turn 01's finding 31 should say the approved
*desktop* memory deletion, not every legacy store; its finding still stands.

## Handoff and verification

The close-out reads turns 01–08 together. The unresolved questions for turn 09
are C2's limited byte-preservation oracle, finding 24.2's unqualified README
claim, and the timing and internal-name qualifications above. This turn makes no
remediation choice for Ben.

This review read the cited tracked sources, the branch and commit identities,
and turn 07's record of the public push times. It did not rerun the earlier
suite, mega or generators; no such run is owed for this review-only record.

Product reach: this record changes no published or distributed MAM product.
Act risk: this dated record is committed and pushed to the shared review branch
on `origin` as the turn handoff; `main` is neither integrated nor pushed.
