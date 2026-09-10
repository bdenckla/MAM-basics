# Running the periodic review with both Claude and Codex

This document records a recommendation Claude made on 2026-09-01, in a session titled "Claude and
Codex complementary workflows", and first written down on 2026-09-03 because until then the
recommendation existed only in that session's transcript and had to be recovered by searching
transcripts. **The alternating argument, counter-argument and rebuttal round is the standard
dual-agent review, by Ben's decision of 2026-09-09 (D9).** The September 8 review was its worked
case. Design A was the default from 2026-09-07 to 2026-09-09 and was first run on the September 4
window; Design B remains the blind alternative by explicit request.

Read this before starting a dual-agent review. It records the standard round, its shared worktree,
its close-out, and the earlier Design A and Design B procedures.

**Codex already reviews this repository, in a different series.** The staged review of
`py/main_0_mega.py`'s 42 registered steps ran in Codex review forests under
`C:/Users/BenDe/Documents/Codex/ReviewForests/` and produced
`doc/mega-pipeline-review-phase-*-2026-09-01.md`. This document instead pairs Codex with Claude on
the **periodic** review — the `doc/review-findings-<date>.md` series. That series was Claude-only
through 2026-09-01; the 2026-09-04 window is its first paired review. Do not read the earlier
Claude-only history more broadly than that.

## What the periodic review is, and what Codex joined

Every four to eight days one Claude session reads a commit range across the public repositories and
writes `doc/review-findings-<date>.md`. Re-measured on 2026-09-09 at `9ac147cc`, the review
files and their line-3 `State:` entries are:

| Filename pattern | Files at the measured commit | Recorded states |
|---|---|---|
| `doc/review-findings-*.md` | 10 initial Claude reviews, 2026-07-29 through 2026-09-08 | Through September 7: acted on, with dated qualifications. September 8: not yet acted on, with its stated exceptions. |
| `doc/codex-review-findings-*.md` | 7 files: the September 4 counterpart; September 7's standard and `-sol` counterparts; September 8's counter-argument, Claude rebuttal, Codex counter-rebuttal and Claude turn 5 | September 4: acted on 2026-09-07. Both September 7 files: completed 2026-09-08. All September 8 files: completed 2026-09-09. |

The September 4 window was the first paired review; September 7 and September 8 followed it.
The historical Codex prefix therefore does not identify the author of every later turn. The
naming section below records the standard for future files and preserves these historical names
and states. Re-establish the census in the review checkout, and read the states rather than
inferring remediation from a completed review:

```powershell
git ls-files -- "doc/review-findings-*.md" "doc/codex-review-findings-*.md"
```

```powershell
git grep -n "^State:" HEAD -- "doc/review-findings-*.md" "doc/codex-review-findings-*.md"
```

Two properties of the series matter to everything below.

1. **The series is doc-only since 2026-09-01** (`5b89033`). **"Doc-only" says where a review is
   RECORDED, never what it may READ** — a distinction worth spelling out, because two documents
   written on 2026-09-09 both took it the other way, and either reading would send a session to Ben
   for a scope decision he does not owe. A review reads whatever the window changed in a public
   repository: `doc/review-findings-2026-09-08.md` is headed "review of the public repos" and
   accounts for 99 commits and 513 changed paths across Python, pages and data. What went doc-only
   is the RECORD. Each file carries a `State:` line at
   line 3 directly under the H1. The initial review records remediation state; later turns record
   review completion, under D10 in the naming section below. The
   thin tracking issue every review used to file — wlc-utils#87, then MAM-basics #219, #228, #231,
   #232, #261, #263 — is retired, because every comment on all seven was agent-written from Ben's
   account and only #219 was ever adopted as a citation handle. A review that finds work somebody
   must do still files a real issue with a real body; #233 is that shape.
2. **The series is public-only since 2026-08-26.** It does not read MAM-private. This is load-bearing
   for the Codex scoping rule below, not incidental.

   **Its one standing exception — the byte-compare of github-misc's instruction-file plumbing, which
   the review files record as row 22 and finding 5.6 — is SPENT as of 2026-09-09, and no future
   review should apply it.** The twelve files it reached became canonical in this public repository
   that day, at `dot-claude/` and `dot-Codex/`, so the ordinary sweep reads them like any other
   tracked file; and github-misc's clone was retired the same day, so performing the byte-compare
   would now mean re-cloning a private remote to compare a file against itself. It is recorded as
   spent rather than deleted so that a reader of finding 5.6 can still see why it existed. Nothing
   replaces it: **no scope widening and no new exception is owed for `dot-claude/` or `dot-Codex/`**,
   which point 1 above is what settles.

The convention of record for both properties is the "The doc/ directory standard" section of
`py/repo_util/check_repo_standards.py`'s module docstring. Read it there rather than re-deriving it.

## Calibrate before adopting a standing parallel track

The series runs every four to eight days, so running a blind Design B review on every window is a
standing cost against a benefit to measure before adopting that cadence. Under Design B, reconcile
one blind dual-agent run, count the four buckets, and only then decide on a standing blind track.

1. **If the Codex findings are largely a subset of the Claude findings**, a parallel track is not
   worth its cost. The better shape is to **alternate**: every other review is a Codex review. That
   buys decorrelation across windows at no added cost per window, at the price of never learning
   which agent misses what.
2. **If the two overlap little**, the parallel track is earning its keep and becomes standing
   practice.

The 2026-09-04 Design A run confirmed four Claude subfindings it checked, rejected none of the
checked claims, and found one record error the Claude review omitted. Because Design A is anchored
to the Claude review, that result measures error-checking value but not independent overlap; it does
not fill the four Design B buckets.

The September 7 window added `doc/codex-review-findings-2026-09-07.md` (Terra) and the requested
additional `doc/codex-review-findings-2026-09-07-sol.md`. Re-read at `9ac147cc` on 2026-09-09,
Terra confirmed its selected claims and found no omission; Sol checked a largely separate set,
corrected the qamats-variant unit and count and the trailer-spelling count, and found omitted
artifact whitespace errors. Sol's independence caveat records that it saw Terra's reconciliation
before returning to the frozen Claude report. These were Design A checks, not a blind Design B
comparison.

The September 8 window added the counter-argument and the alternating turns recorded below.
Corrections were accepted by both reviewers. Ben judged the turn-taking process successful and
made it standard on 2026-09-09 (D9). The exchange measures the value of checking and correcting
review claims; it does not supply Design B's independent-overlap buckets.

The undecided blind-review cadence is separate from the design choice. Whenever a periodic review is
run as a dual-agent review, use the standard alternating round unless Ben explicitly requests
Design B's blind, independent sweep. D9 chooses the dual-agent procedure; it does not require
every periodic review window to use two agents or establish a blind parallel-track cadence.

## The standard alternating round — Ben's decision, 2026-09-09 (D9)

The round takes turns in this order:

1. **Claude argument:** the initial review of the named public commit ranges, committed as
   `doc/review-findings-<date>.md`.
2. **Codex counter-argument:** check the Claude claims and the same ranges for omissions,
   committed as `doc/codex-review-findings-<date>.md`. Once stable, append the reconciliation
   table to the argument under `## Reconciliation with the Codex review`, recording confirmed,
   qualified, rejected and unchecked claims and identifying unfixed work.
3. **Claude rebuttal:** accept, qualify or contest the counter-argument and its characterization
   of the argument. A rebuttal need not defend the initial findings.
4. **Codex counter-rebuttal:** assess the rebuttal against the cited evidence and record any
   corrections Codex accepts.
5. **Further alternating turns as needed:** Claude, then Codex, until the stopping rule applies.

Each turn is a tracked file. Ben supplies the next task with that file's path and commit; the
next task reads the committed file instead of depending on pasted chat or remembered conclusions.
Verify the exact shared checkout, branch, required commit and clean working tree before reading.
A newer starting commit must contain the required commit as an ancestor. The naming section gives
the numbered filenames for turns after the counter-argument.

**The stopping rule:** a turn that accepts everything and lists no unresolved disagreement ends
the round. The other agent's next task reads that turn and records an acknowledgment or an
objection. An objection identifies the disputed claim and the evidence needed to settle it; it
does not silently become a remediation instruction. Ben resolves any objection that needs his
decision before close-out proceeds. Step 1 of
`doc/PLAN-close-out-review-2026-09-08.md` is the worked acknowledgment and closure decision.

**Every turn is review only and uses public evidence only.** It performs no remediation and
does not rewrite an earlier turn. A correction belongs in the turn that accepts the correction.
Turn 2's initial reconciliation is the specified append to the argument, not permission to edit
the original findings; subsequent corrections to that table are recorded in subsequent turns.
The close-out reads the table together with those corrections and Ben's decisions.

After the exchange closes, close-out proceeds in this order, as worked in
`doc/PLAN-close-out-review-2026-09-08.md`:

1. Record Ben's decisions on the choices the review leaves to him.
2. Update the procedure record with the round's outcome and the approved process changes.
3. Write a remediation plan for a fresh task, including concrete editorial wording for Ben's
   approval; obtain the required approvals before execution.
4. Execute the approved remediation, recording each finding's disposition under a dated
   `## Dispositions after remediation` section in the initial review. Preserve earlier records;
   add dated corrections beside any record that needs correction.
5. Integrate once after the final remediation wave, using the worktree procedure below.
6. Retire the shared worktree and branch after the final task ends.

### The shared worktree — Ben's decision, 2026-09-09 (D11)

For future rounds, the Claude session that writes the argument creates branch
`dual-agent-review-<date>` and worktree
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-<date>` at the round's
start. The branch and worktree folder have the same name. Every turn of both agents and every
close-out task uses that checkout directly, with writing responsibility passed between tasks.
Do not create another worktree for a successor. The primary clone supplies its venv by absolute
path; development commands, edits, staging and commits use the verified shared worktree.

Each close-out task merges `main` into the review branch before editing and resolves conflicts
there. No intermediate task fast-forwards `main` or pushes, including when an intermediate task
is archived. The final remediation task integrates once: merge `main` into the review branch,
run the repository suite in the worktree with `REPOS_ROOT=C:/Users/BenDe/GitRepos` and
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`, then fast-forward the primary
clone's `main` with `--ff-only` and push `main`. If the fast-forward refuses because `main`
moved, merge and verify again in the worktree. Retire the worktree and its merged branch only
after the final task has ended.

In the September 8 round, Codex created
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08` on branch
`codex-review-2026-09-08` in turn 2 without instruction. The shared checkout worked: later turns
of both agents and the close-out used it. Ben's judgment on 2026-09-09 was that creating the
worktree had been a good idea, but its path and branch read as Codex's. The approved naming makes
the shared purpose explicit. The September 8 worktree and branch keep their existing names.

### Separate defects from editorial proposals — Ben's decision, 2026-09-09 (D7)

For every remediation proposal, separate reproducible data or code defects from proposed
editorial changes to terminology, organization, interpretation or attribution. Present concrete
wording for each editorial change for Ben's approval before applying it. Follow already-recorded
decisions without asking again. Agreement between reviewers does not approve an editorial change.

The September 8 MAS-page reversals are the worked example, not the scope boundary. The broad
instructions at `47edbee6` made editorial rewrites executable without identifying approved
wording; `1095f029` and `a9edd4f9` record Ben's reversal of unrequested rewrites. Those decisions
require dated corrections to the earlier remediation records, not reinstatement of the reversed
prose. The counter-argument's "MAS decisions and the scope of future remediation" section and
the close-out plan's D7 decision record the evidence and Ben's generalization of the rule.

### Present remediation by public-facing risk — Ben's decision, 2026-09-09

For future remediations (actions based on review findings), Ben wants proposed changes
presented in the following order and at the following level of detail. The categories
express the risk Ben assigns to changing what readers see or consumers receive.

1. **Public-facing documents — high risk.** Present changes to rendered HTML and to
   Markdown intended for readers, such as README and license pages. Show the current and
   proposed wording; identify formatting changes separately. Ordinary plans and review
   records under `doc/` do not enter this category merely because the repository is public.
2. **Public-facing data — high risk.** Present changes to published corpus data, such as
   MAM-parsed-plus JSON, with the affected text, values, or structure. Trace generated
   effects: an analysis JSON change and a Phonetic MAM JSON change that produces no change
   in Phonetic MAM HTML belong with the lower-risk changes in Ben's distinction. Say when
   no public-facing data change is proposed, and distinguish an unchanged regenerated
   file from a proposed content change.
3. **All remaining changes — lower risk.** Start with a summary by type, at the granularity
   of "wording changes to Markdown files in doc directories", "Python comments and
   docstrings", "agent instructions", "code and tests", or "vendoring reports". Ben will
   ask for finer detail where he wants it; do not begin by requiring him to inspect every
   internal wording replacement.

Classify a change by its effect on the published document or data, including effects of
edits in a generator. A Python filename does not make a change lower risk if the change
alters published HTML or corpus JSON. A public Git repository does not make every file
public-facing in the sense Ben means here.

Use these categories for the approval presentation even when the written plan also has
finding-number references, separate editorial and technical items, and implementation waves
ordered by dependencies. Keep that execution detail available in the plan. The presentation
preference does not itself approve a proposed change or alter a decision already recorded.

The worked case is Ben's September 9 inspection of the September 8 remediation plan: he
first requested the HTML and reader-facing Markdown changes, then the public JSON changes,
then a summary of the remaining change types. The earlier presentation grouped editorial
proposals by MAS versus non-MAS subject matter and led with implementation waves, mixing
reader-facing wording with internal documentation. Future presentations use Ben's risk
categories first.

## Earlier designs — Design A was the default, 2026-09-07 to 2026-09-09; Design B is the blind alternative

**Design A, Codex reviews the finished Claude review.** Point Codex at the completed
`doc/review-findings-<date>.md` **plus** the same commit range, and ask two questions: which claims
in this file are false, and which commits in the range does it fail to account for.

**Design B, the parallel blind sweep.** Both agents review the same commit range at the same time,
neither seeing the other's output, each writing its own findings file.

The trade is clean, and neither design subsumes the other. **Design B catches misses**, because the
Codex review looks where the Claude review did not. **Design A catches errors**, because it
re-derives claims that are already written down — but it is anchored to the Claude review and so
will not look anywhere that review did not.

**Design A was chosen as the default on 2026-09-07 on two grounds.** The record says errors dominate here:
`251b287`'s commit message is "Record the 2026-09-01 review's findings, and fix the record errors it
found", and the series' output is heavily claims in `CLAUDE.md` and `doc/` that turned out to be
wrong. And Design A is roughly a fifth of the work of Design B. Use Design B only when the second
review must search independently for omissions rather than checking and extending the first review.

Design A does not need the blindness rule below, because it is anchored by construction. The
blindness section applies to Design B only. **Both designs require reconciliation**, but the
reconciliation section below assigns that work differently for Design A and Design B.

## Experimental Claude rebuttal round (2026-09-09)

Ben proposed trying an additional round for the 2026-09-08 review, with this terminology:

1. **Claude argument:** Claude's initial review.
2. **Codex counter-argument:** Codex's assessment of Claude's review.
3. **Claude rebuttal:** Claude's response to Codex's counter-argument. A rebuttal can accept,
   qualify, or contest Codex's criticisms; it need not defend every original finding.

The periodic reviews already provide some delayed feedback: the next Claude review can examine
the preceding Codex findings and remediations. The experiment brings an explicit Claude rebuttal
into the same review window, before disputed findings become remediation instructions.

For this experiment, Claude writes the rebuttal to
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08/doc/codex-review-findings-2026-09-08-claude-rebuttal.md`.
The original Claude review and Codex findings remain intact. Ben gives the next Codex task the
file path and, if committed, the commit ID; Ben need not paste the rebuttal into chat. The next
Codex task reads the rebuttal from that file.

**Outcome recorded 2026-09-09:** the experiment completed with corrections accepted by both
reviewers. Ben made the alternating round the standard dual-agent review on 2026-09-09 (D9),
replacing Design A as the default. The five documents of the exchange are:

1. Claude argument: `doc/review-findings-2026-09-08.md`, `e56ae06a`, with its reconciliation
   table appended at `5636d38a`.
2. Codex counter-argument: `doc/codex-review-findings-2026-09-08.md`, `5636d38a`.
3. Claude rebuttal: `doc/codex-review-findings-2026-09-08-claude-rebuttal.md`, `da4e40a5`.
4. Codex counter-rebuttal:
   `doc/codex-review-findings-2026-09-08-codex-counter-rebuttal.md`, `ad5d9f43`.
5. Claude turn 5: `doc/codex-review-findings-2026-09-08-claude-turn-5.md`, `2b365153`, with
   its addendum at `7c4416cd`.

Turn 5 accepted Codex's concessions and closed the three disputes the rebuttal had listed:

1. **Finding 14.4:** Codex withdrew the claim that the repository's attribution of the context
   permission for plain "word" to the skill was inaccurate. The permission is in
   `references/terminology.md`; the remaining inconsistency is the opening `SKILL.md` sentence's
   "only". Claude withdrew "in the skill nowhere" as a claim about the page exception in the
   inspected skill.
2. **C1 / finding 13.2:** Codex withdrew "without checking it" and "manufacture agreement" as
   paraphrases of Claude's finding, and any implication that Claude proposed removing the guards.
   Claude reclassified 13.2 as a design note; both reviewers agreed that no present MAS output
   defect had been established.
3. **C2 / finding 17(b)–(e):** Claude accepted that the heading misclassified accurate historical
   commit messages as errors. Codex accepted that the individual items described subsequent
   changes rather than claiming that the messages were false when written.

The rebuttal's further accepted corrections were confirmed in the counter-rebuttal and turn 5:

| Finding | Correction Claude accepted |
|---|---|
| 13.7 | The conjunctive-accent claim is checked by a per-record raise. |
| 17(e) | The sentence count needed correction. |
| 16 | Withdraw the eight sites based on generalized verb or authorship restrictions. |
| 11.1 | The Wave 4 command is unrecorded, so the cause of its missing subtest line is unknown. |
| 10 / C5 | The procedure's "will never load" premise is false and was omitted from finding 10. |
| 14.1 | The defect concerns an earlier use of "word", not the definition's expository paragraph number. |
| 13.5 | `build_survey` raises; `_problems` returns the problems. |
| MAS-remediation process | The argument omitted the broad editorial instructions at `47edbee6`. |

Codex also conceded that finding 6.8 had already called the historical anchor count "true then";
Claude corrected finding 6's heading because item 6.8 became stale before the merge named there.

The step-1 acknowledgment, appended to the counter-rebuttal at
`8c49cdd2666382fe838d50affdff432e381c2694`, accepted the substantive closure and recorded an
objection to the inferred time of Claude's skill reading. **Ben closed the review exchange on
2026-09-09:** leave the skill-reading time unknown; the uncertainty does not affect the review's
conclusions. The objection is disposed of by that decision, as recorded beside step 1 in
`doc/PLAN-close-out-review-2026-09-08.md`; it is not an unresolved dispute. The exchange's
closure and D9's adoption of the procedure do not claim that outstanding remediation is done.

## Keep the two reviews blind to each other

Under Design B the two reviews are run **against the same anchors, concurrently, with neither seeing
the other's output.** This is the condition that makes the parallel track worth anything at all.

The reason is error decorrelation, and it is fragile. A Codex review run after reading
`doc/review-findings-2026-09-01.md` anchors on those conclusions and confirms them, so the second
review reports agreement and you have paid twice for one review's worth of independence. The same
rule governs what either agent is handed in the first place: give the reviewer the diff, never the
authoring session's transcript and never the commit message's justification, because a reviewer
shown the rationale reports agreement with it.

"Same anchors" means the same commit range in the same repositories, named explicitly, and the same
starting commit for each repository the range covers.

## Reconcile both designs; use four buckets only for Design B

Two findings files sitting side by side in `doc/` are worth nothing unless something compares them,
because nobody will do it later. Both designs therefore end with an explicit reconciliation, but
the design decides who writes it and what the comparison can honestly claim.

**Under Design A, the Codex reviewer writes the reconciliation before ending the Codex review.**
Codex has read the Claude findings by design, and its two assigned questions already are the
comparison: which Claude claims are false, and which commits the Claude review fails to account for.
Once the Codex findings are stable, the same Codex session appends a short reconciliation recording
the Claude claims it confirmed, the Claude claims it rejected, the omissions it found, and the
Claude claims it did not independently check. A fresh session would add no independence to an
anchored review and would discard the comparison context the Codex reviewer already has.

**Under Design B, a fresh session sorts every finding into four buckets.**

1. Both reviews found it.
2. Only the Claude review found it.
3. Only the Codex review found it.
4. **The two reviews assert incompatible facts.**

**Bucket 4 is the highest-value output of Design B.** It means at least one review is
wrong about a re-derived figure, and it names exactly which figure to check by hand. A single
merged set of findings dissolves bucket 4, because a merge has to pick a winner and does it
silently. So the reconciliation tabulates the two reviews; it does not wrangle them into one.

**Where the reconciliation goes: a section in the Claude review's own file.** The 2026-09-01
recommendation said to put it in a comment on the review window's thin tracking issue, reusing
machinery that then existed. That machinery was retired eight minutes later the same day, in
`5b89033`, so **an issue comment is no longer available and that half of the recommendation is
void.** The doc-only replacement is to add a `## Reconciliation with the Codex review` section to
`doc/review-findings-<date>.md`, which is the file a reader is already in — the same reasoning that
put the `State:` line there.

Each finding in the reconciliation ultimately carries a disposition, written down: fixed, or
rejected with the reason. The initial comparison marks unresolved work as unfixed; the later pass
replaces that state with the earned disposition. Without that record, an agent silently drops the
findings it does not like and reports that it addressed the review.

**The comparison is known at reconciliation; the dispositions are not, so expect two writes.** The
Design A comparison can be written when the Codex findings are stable; the Design B buckets can be
written when both blind findings files are frozen. Whether a finding was *fixed* is knowable only
once somebody has acted on it, which is normally a later pass — the same split the `State:` line
already makes between a review and its `acted on <date>`. So the Design A comparison or Design B
four-bucket table lands when the comparison runs, and each finding's disposition lands when the
work is done. Do not hold the comparison back waiting for the dispositions, and do not write a
disposition the work has not yet earned.

**Under Design B, run the reconciliation as a fresh, post-review task.** Start the task only after
both the Claude and Codex findings files are complete and frozen. The task may read both files and
append the four-bucket table and, on the later pass above, the dispositions to the Claude file, but
it does not rewrite either agent's original findings. The reconciliation is comparison work, not a
third review or a silent revision of either independent result.

For Design B, **"fresh" means a session that wrote neither findings file** — not merely a new task
inside one of the two reviewing sessions. The agent whose findings are under comparison must not be
the one adjudicating bucket 4, which exists precisely because at least one of the two reviews is
wrong there; an agent grading its own paper there will resolve it in its own favour without ever
intending to. A session that watched either review being written is anchored to it and is not a
reconciler either, for the same reason the two reviews are kept blind in the first place.

## Review filenames and State lines — Ben's decision, 2026-09-09 (D10)

The Codex counterpart takes the prefixed name `doc/codex-review-findings-<date>.md`. The existing
`doc/review-findings-<date>.md` series keeps its unprefixed name and is **not** renamed to
`claude-review-findings-<date>.md`.

For future rounds, the filenames and states follow these rules:

1. **Keep the first two filenames:** `doc/review-findings-<date>.md` for the Claude argument and
   `doc/codex-review-findings-<date>.md` for the Codex counter-argument. The standard Codex file
   has no model suffix. Reserve a suffix such as `-sol` for an exceptional additional review
   comparing or repeating the same role with a named model; September 7's `-sol` file is the
   worked example.
2. **Number later turns:** `doc/dual-agent-review-<date>-turn-03-claude.md`,
   `doc/dual-agent-review-<date>-turn-04-codex.md`, and the corresponding numbered name for each
   further alternating turn. The stem identifies the shared exchange and the number identifies
   its sequence.
3. **Keep remediation state in the initial argument:** `review-findings-<date>.md` uses
   `State: not yet acted on` or `State: acted on <date>`, with any qualifications. Every later
   review turn uses `State: completed <date>; review only`. Completion means the review turn
   is finished; "acted on" means findings were remediated. Keep the state at line 3, directly
   under the H1.
4. **Recognize all the review files in the document standard:** the initial Claude files, the
   Codex counter-arguments and exceptional additional reviews, and the later numbered dual-agent
   turns. The older `doc/review-findings-*.md` glob in the standard's history names only the
   initial series. The naming and state rules here cover the additional files too. Preserve
   historical filenames and `State:` lines, including September 4's Codex "acted on" and
   September 8's later turns under a Codex-prefixed stem.

The asymmetry reads correctly: the unprefixed name is the incumbent, and the prefixed name announces
its difference. `CLAUDE.md` carries one sentence saying that an unprefixed name means the Claude
series, so a reader meeting the asymmetry is not left to infer it.

The rename was measured and rejected on 2026-09-01, when `review-findings` appeared on 41 lines
across 18 files, 39 of them naming a dated file, 25 citing `doc/review-findings-2026-07-29.md`
alone, and none of the 41 executable — every one a docstring, a comment, or markdown. Re-measured
2026-09-03 at `dc24164b`, before this document was added: **50 occurrences across 23 files**, of
which **29 across 11 files** name `doc/review-findings-2026-07-29.md`. The figure grew with the
`State:` line work and the mega-pipeline review docs, and this document itself adds further
citations, so re-measure rather than trusting either figure:

```powershell
git -C C:/Users/BenDe/GitRepos/MAM-basics grep -cI "review-findings"
```

Four reasons the rename was rejected, none of which the growing count changes.

1. **Ben has twice chosen a one-sentence fix over a mass edit and recorded the choice.** The eight
   `../masorah-books/` paths and the seven `al-hatorah` paths in `py/accgram/` are each stale by
   exactly one directory, and `CLAUDE.md` says so in prose rather than editing the fifteen sites.
2. **The most-cited file is the one a rename would hurt most.** `check_repo_standards.py` singles
   `doc/review-findings-2026-07-29.md` out as the model case of a doc earning its place, precisely
   because a dozen code comments cite it by item number. Churning those citations to add an agent's
   name to the path is a poor trade.
3. **`doc/review-findings-2026-07-29.md` is not natively this repository's file.** It arrived
   byte-identical from wlc-utils, and `CLAUDE.md` asserts that identity. Renaming it would
   retroactively label as a Claude review a file that predates the distinction.
4. **There is precedent for keeping a name and explaining it.** `CLAUDE.md`'s "Five issue trackers"
   section kept its name after five more trackers were consolidated into it, with an explicit note
   recorded so a rename is not re-proposed.

## Two things to set up before the first Codex review

### 1. Scope Codex to the public repositories, explicitly

A Codex agent that reads MAM-private and then writes `doc/codex-review-findings-<date>.md` into
MAM-basics publishes private material permanently, and no mechanism prevents it.
`py/repo_util/report_destination.py`'s guard makes it mechanically impossible for
`main_repo_util.py` to write a private-covering report into a public tree, but that guard's own
docstring names what it deliberately does not cover: "what a human or an agent later types into a
`doc/` file". A Codex reviewer writing into `doc/` is exactly that uncovered case.

The public-only scope the review series has run under since 2026-08-26 removes this structurally.
Keep Codex inside that scope, and do not give it a private-side lane until the question of where
that lane's output lives has been settled.

### 2. Limit the Codex reviewer to review records

A Codex reviewer writes only the named findings and reconciliation records, including the specified
reconciliation append to the Claude argument. A Codex reviewer does not modify source files,
generated products, or earlier findings. Two agents with write
access to one working tree can stage each other's half-written work, and that failure is clean and
therefore silent — the collision the worktree rules in `~/.claude/CLAUDE.md` exist to prevent, but
with no human turn between the two agents.

The record-only scope has to be maintained deliberately rather than inferred from a sandbox flag.
This document does not prescribe or assess current Codex sandbox syntax.

For the standard alternating round, give the Codex reviewer the shared worktree created by
Claude, under D11 above. Every successor uses that same checkout directly. A worktree runs the
primary clone's venv by absolute path.

## A precondition this document does not own: `~/.codex/AGENTS.md`

**Ben's approved replacement, 2026-09-09 (D1):**

> Codex reads AGENTS.md and can load the hebrew-prose skill from ~/.agents/skills/. Codex does not automatically load ~/.claude/CLAUDE.md.

The reviewer needs the applicable global instructions and the skill with its references before
checking house conventions. The earlier inability claim was the procedure error identified by C5;
it confused automatic loading of Claude's instruction file with Codex's ability to load the skill.

**This is a general prerequisite for using Codex on any of Ben's repositories, not a step of this
procedure, and it is tracked separately** — Ben's decision, 2026-09-03. It is recorded here only so
that a session running a Codex review knows the dependency exists and can check whether it has been
met.

**It has been met.** `~/.codex/AGENTS.md` exists and is 1,106 lines, re-measured on 2026-09-09
(the September 8 measurement was 1,077). It is a port of `~/.claude/CLAUDE.md`,
carrying the same opening convention — its canonical copy is **this repository's**
`dot-Codex/user-wide-AGENTS.md` since 2026-09-09, alongside the `dot-claude/` copies, with the same
manual write-back and the same drift check. It was `github-misc`'s `dot-Codex/AGENTS.md` until that
day; the tracked `user-wide-` name distinguishes the stored copy from repository instructions.
Re-establish with `(Get-Content C:/Users/BenDe/.codex/AGENTS.md).Count`. Note the capital C
in `dot-Codex`, which a case-sensitive glob for `dot-codex` misses.

## What this document deliberately does not settle

1. **Whether every periodic window should have a blind parallel review.** Design B's calibration
   addresses that cadence; D9 already settles the standard dual-agent procedure.
2. **Whether Codex ever reviews the private side.** Setup item 1 defers this rather than answering it.
3. **How to run Codex on this machine.** No command line is given here. Codex demonstrably runs
   here — see the provenance section — but this document has not examined how it is invoked, and
   guessing a spelling would be worse than the omission.

## Provenance and caveat

The recommendation recorded here was made by Claude on 2026-09-01. Design A was first run on
2026-09-04, in `doc/review-findings-2026-09-04.md` and
`doc/codex-review-findings-2026-09-04.md`. Ben made Design A the default dual-agent design on
2026-09-07. Design A remained the default until Ben adopted the alternating round on 2026-09-09;
Design B remains unrun and optional by explicit request.

**Its claim that Codex had never been run on this machine was false, and is corrected here.** The
2026-09-01 session said so, this document repeated it on 2026-09-03, and a `git worktree list` that
same day disproved it: four Codex review forests then existed under
`C:/Users/BenDe/Documents/Codex/ReviewForests/`. Those forests were retired by 2026-09-04;
`~/.codex/sessions` holds Codex session history, and
`~/.codex/AGENTS.md` was 1,077 lines as measured on 2026-09-08; the prerequisite section above
records the September 9 measurement. Codex ran the staged mega-pipeline review of `py/main_0_mega.py`'s
42 steps, whose output is this repository's `doc/mega-pipeline-review-phase-*-2026-09-01.md` — that
review names its governing forest and records that the `worktree-forest` and `hebrew-prose` skills
governed it.

The lesson is the one `CLAUDE.md` already states about transcriptions, applied to a session
transcript: **a transcript is evidence about that session, never about the machine.** The 2026-09-01
caveat was accurate about what that session had done and wrong as a claim about this machine, and
repeating it without checking is how it propagated. Check the machine.

This document does not assess Codex's current sandboxing behaviour on Windows. The procedural rule
is independent of that implementation detail: the reviewer writes only the named review records.

**This document is itself a small worked example of the pairing, and converged in two rounds.**
Claude drafted it on 2026-09-03. Codex then added the "Run the reconciliation as a fresh,
post-review task" paragraph (`706395bf`), which closed a real gap: the draft said what the
reconciliation produces and where it goes but never who runs it or when, so the default reading left
a reviewing agent adjudicating its own bucket 4. Claude then added the two-writes paragraph and the
"fresh means a session that wrote neither findings file" paragraph. **Ben supplied the turn between
each round, which is the only reason this was convergence rather than the unattended ping-pong this
document warns against** — neither agent ever answered the other directly. Ben's decision,
2026-09-04: that fresh-session safeguard belongs to Design B, where bucket 4 compares independent
reviews. Under Design A, the Codex review is the comparison, so the Codex reviewer writes the short
reconciliation while the comparison context is still present.
