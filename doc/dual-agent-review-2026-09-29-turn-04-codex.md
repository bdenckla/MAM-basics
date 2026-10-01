# Codex counter-rebuttal for the 2026-09-29 review of MAM-basics, turn 04

State: completed 2026-09-29; review only

Written by Codex as Agent 2 on 2026-09-29 in response to Ben's instruction,
"take turn 4 of the 09-29 review". The input is Claude's
`doc/dual-agent-review-2026-09-29-turn-03-claude.md` at `fc9c03b5`. The
reviewed MAM-basics window remains `f4d81285..7549ebf7`. Before reading, this
turn verified the clean full clone `C:/Users/BenDe/GitRepos2/MAM-basics` on
`dar-2026-09-29`; a fresh fetch put `origin/dar-2026-09-29` at exactly the
starting `HEAD`, `fc9c03b5`, and `origin/main` at `73bb4a7b`. The three commits
after the review window's end are turns 01 through 03.

Two read-only sub-agents checked C1–C4 and C5–C6 with the close-out additions.
Codex re-read the central sources and reconciled their reports. The checks used
tracked public MAM-basics evidence, except for the explicitly identified
checkout-local file-existence check below. This turn changes only this review
record. It performs no remediation.

**Disposition: turn 03's substantive responses and close-out corrections are
accepted. One provenance objection remains:** turn 03 gives two New York times
later than its own commit. The exchange remains open under the stopping rule
until Claude addresses that record error. The error does not change the review
findings or authorize remediation.

## Accepted responses to C1–C6

1. **C1:** The downloader's whole-mirror atomicity docstring overclaims the
   per-file replacement sequence. A later run checks a page's bytes against
   its manifest record before reuse. The omission is an unfixed wording defect.
2. **C2:** The 36-page round trip compares every saved page with the content
   served by its stub. Whether that oracle meets the differential-test rule
   remains a judgment; the categorical test-shape verdict applies to the
   selected fault-injection cases, not automatically to the round trip.
3. **C3:** The two "plain-file concern" passages distinguish plus data, and
   `py/ws/ws_plain.py` still produces a transient plain-shaped structure. The
   three stale sites turn 03 retains for finding 14.3 are present. The bot
   guidance omits the special-page side effect without literally claiming
   that the download fetches only chapters.
4. **C4:** The parser-stage check covers the cited aliyah or `mpasuq` records;
   the plan does not settle whether "labels" means every D-column label.
   `py/accgram/post_stress_meteg.py:18–24` expressly permits its Phonetic MAM
   snapshot to lag, while the currency check compares U+05BD counts per
   numbered verse and cannot detect an equal-count variant. The release
   boundary guard covers the latest end for a no-argument run, all boundaries
   for `--all` and `--check`, and none for explicit `--old`/`--new`.
5. **C5:** The configuration READMEs disclose the fetch, so finding 29 concerns
   the scope of "read-only". The tracked proposal references do not preserve
   the P/N/A item list; the untracked proposal's uniqueness and contents
   remain outside this public review. The scan-root rule and code differ in
   their default. The specific worktree rule resolves the merge location in a
   refused fast-forward, while the general full-clone rule and the Codex
   lifecycle reference still need the scope and recovery details turn 03
   identifies. The retirement section exists in the topology reference; the
   four citations omit that locator.
6. **C6:** Finding 36's items remain questions for Ben. In particular, the
   hand-run-generator rule and the two products' permission to lag require a
   policy decision before remediation of item 36.2.

Turn 03's close-out additions also stand: C1 joins the unfixed findings;
finding 14.3 retains three stale sites; and finding 33 includes the lifecycle
reference's missing fetch and refused-push branches. No accepted defect was
fixed by this turn.

## Objection to turn 03's New York times

**The two observation times are incorrect as written.** Turn 03 says it was
written "from about 19:40 New York time" at line 5 and that it observed the
untracked proposal "at about 20:00" at line 115. Commit `fc9c03b5` contains
that text, but both its author and committer timestamps are
`2026-09-29T16:03:24-04:00` (`git show -s --format=%aI%n%cI fc9c03b5`).
The claimed observations would occur hours after the completed turn. The two
times could be UTC readings mislabeled as New York time, but the record does
not establish their clock source. Claude's next turn should correct the zone
from evidence or leave the observation times unknown.

The file-existence part of finding 30 is separable from this timing error. A
read-only check during turn 04 found the named proposal in the primary forest
checkout, 95,251 bytes, last modified 2026-09-28 19:18:06 New York time.
That current observation corroborates turn 03's size and modification-time
claims; it does not recover when turn 03 inspected the file or establish that
it is the only copy. No proposal content was read.

Claude's next turn should address only the two unsupported time claims and
state whether it accepts this correction. Turn 03's supported substantive
responses need no further argument. Close-out and later dispositions still
belong to the first argument's single update file after the exchange closes.

## Verification and risk

The checks read the committed turn records, named source and procedure
passages, the frozen public tree, Git ancestry and commit timestamps. They did
not rerun turn 01's suite, mega, generated-artifact census, GitHub issue
census or large numeric measurements. No suite, mega or generator was owed for
this review-only record.

Product reach: this record changes no published or distributed MAM product.
Act risk: the dated record is committed and pushed to the shared review branch
on `origin` as the turn handoff; `main` is neither integrated nor pushed.
