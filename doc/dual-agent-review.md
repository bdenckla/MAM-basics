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

**The periodic review itself is described in `doc/periodic-review.md`**, split out of this
document on 2026-09-12: the series, its two standing properties, what a review file contains,
and the remediation rules D7 and the risk ordering. A citation written before that date may
name this document for material that is now there.

## What Codex joined

Re-measured on 2026-09-09 at `9ac147cc`, the review files and their line-3 `State:` entries are:

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

Both properties that make the series safe to pair, doc-only since 2026-09-01 and public-only
since 2026-08-26, are stated in `doc/periodic-review.md`. The Codex scoping rule below depends on
the second.

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

**Each named turn may itself be an orchestrated multi-agent task — Ben's decision, 2026-09-15.**
The turn's root reviewer and any sub-agent may delegate bounded, independently checkable work to
another sub-agent, either in parallel or as a sequential handoff. The root reviewer remains
responsible for the turn: the root reviewer sets the scope, reconciles the reports, verifies the
claims it adopts, and owns the tracked file and commit. Because the agents share the D11 checkout,
only one agent writes, stages or commits at a time; other sub-agents report without editing unless
writing responsibility is explicitly handed to one sub-agent. Use delegation when it can save
time, protect the root reviewer's context or improve confidence, not merely to create another
task.

Before the round starts, assign the two roles. **Agent 1 reviews first and owns every odd-numbered
turn; Agent 2 reviews second and owns every even-numbered turn. Either Claude or Codex may be Agent
1, and the other is Agent 2.** The role names describe sequence, not which agent fills the role.
There is no maximum number of turns; the stopping rule below ends the exchange.

The round takes turns in this order:

1. **Agent 1 argument:** review the named commit ranges after sub-agents have checked each finding,
   with no walk-through of the findings before Agent 2's turn, as `doc/periodic-review.md`'s section
   "Reviewing the review, with the same agent and with Ben" sets out (Ben's decision, 2026-09-15).
2. **Agent 2 counter-argument:** check Agent 1's claims and the same ranges for omissions. Once the
   turn is stable, Agent 2 appends the reconciliation table to Agent 1's argument, recording
   confirmed, qualified, rejected and unchecked claims and identifying unfixed work.
3. **Agent 1 rebuttal:** accept, qualify or contest the counter-argument and its characterization
   of the argument. A rebuttal need not defend the initial findings.
4. **Agent 2 counter-rebuttal:** assess the rebuttal against the cited evidence and record any
   corrections Agent 2 accepts.
5. **Further alternating turns as needed:** Agent 1 owns odd turns and Agent 2 owns even turns until
   the stopping rule applies.

Each turn is a tracked file named
`doc/dual-agent-review-<date>-turn-<NN>-<claude|codex>.md`: the two-digit number records sequence and
the final component records the agent that actually wrote the turn. Ben supplies the next task with
that file's path and commit; the next task reads the committed file instead of depending on pasted
chat or remembered conclusions. Verify the exact shared checkout, branch, required commit and clean
working tree before reading. A newer starting commit must contain the required commit as an
ancestor. The naming section distinguishes this standard round from single-agent and blind-review
filenames.

**The stopping rule:** a turn that accepts everything and lists no unresolved disagreement ends
the round. The other agent's next task reads that turn and records an acknowledgment or an
objection. An objection identifies the disputed claim and the evidence needed to settle it; it
does not silently become a remediation instruction. Ben resolves any objection that needs his
decision before close-out proceeds. Step 1 of
`doc/PLAN-close-out-review-2026-09-08.md` is the worked acknowledgment and closure decision.

**Every turn is review only and, in this repository's series, uses public evidence only.** It
performs no remediation and does not rewrite an earlier turn. A correction belongs in the turn that
accepts the correction.
Turn 2's initial reconciliation is the specified append to the argument, not permission to edit
the original findings; subsequent corrections to that table are recorded in subsequent turns.
The close-out reads the table together with those corrections and Ben's decisions.

After the exchange closes, follow `doc/periodic-review.md`'s `Close-out` list. A sequential
dual-agent round additionally updates this procedure record after Ben's decisions, uses Agent 1's
turn-01 update file for later dispositions, integrates through the shared-review branch, and
retires the shared worktree only after the final task ends.

### Correcting a finished dated document — Ben's decision, 2026-09-11 (D12)

A finished dated document — a review, a remediation plan, a completed plan, an execution record —
is left as written, like a pushed commit under a "never amend pushed commits" discipline. Ben's
reason, 2026-09-11: keeping such documents current is maintenance without end, and it also makes
them more confusing rather than less, since a reader cannot tell how the writer could have known
at the time what the document now says.

Each finished document has at most one live sibling, `<stem>-update.md`. Corrections, later
measurements, later State, and remediation dispositions go in that file. Keep the update file true
while the base remains tracked: append later dated entries and correct stale present-tense claims
in place. Never create `<stem>-update-N.md`.

When the update file is created, insert one line directly below line 3 of the base: `Updates and
later status: [<stem>-update.md](<stem>-update.md).` That pointer, plus a mechanically necessary
joining of a prose paragraph that begins on line 3 without changing its text, is the only
post-completion edit to the base. Each update entry names the passage it corrects by that passage's
own words, since line numbers drift. A spent base and its optional one update file are one
retirement family and may be retired together under the repository's manual retirement procedure.
A historical numbered sibling in Git history remains historical evidence; the live policy neither
creates another numbered sibling nor uses the historical file as authority for doing so.

The `State:`-line declaration for update files is in `py/repo_util/check_repo_standards.py`'s
module docstring, under “THE `State:` LINE ON doc/*-update.md”.

A document that describes the present is the opposite case and is kept true in place: `CLAUDE.md`,
the READMEs, the docstrings, this file, and a plan still being executed.

### The shared worktree — Ben's decision, 2026-09-09 (D11)

For future rounds, prefer a setup-only Claude session to create branch `dual-agent-review-<date>`
and worktree
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-<date>` at the round's start,
even when Codex is Agent 1. Setup creates the checkout and performs no review turn. If that setup
session is unavailable, Agent 1 may create the same branch and worktree. The branch and worktree
folder have the same name. Every turn of both agents and every close-out task uses that checkout
directly, with writing responsibility passed between tasks. Do not create another worktree for a
successor. The primary clone supplies its venv by absolute path; development commands, edits,
staging and commits use the verified shared worktree.

Setup locks the shared worktree with `git worktree lock --reason "active dual-agent review
<date>" <absolute-worktree-path>` before the first review turn. The lock remains through review
and remediation. A separate cleanup task unlocks it only after final integration, after the final
task ends, and immediately before an ordinary non-force worktree removal.

Each close-out task merges `main` into the review branch before editing and resolves conflicts
there. No intermediate task fast-forwards `main` or pushes, including when an intermediate task
is archived. Intermediate remediation tasks follow `doc/periodic-review.md`'s “Verification
cadence during remediation”: every coherent commit gets the cheap checks matched to its changed
surface, while the full suite runs after the last test-risky change rather than after every
low-test-risk commit or handoff. A later documentation, comment, review-record or instruction-only
commit does not expire that full-suite result. The final remediation task integrates once: merge
`main` into the review branch,
run `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py` from the
worktree with no `REPOS_ROOT`, read its Git diff, and commit every explained generated change on
the branch. An unexplained generated change or a failing mega step is a failure. Then fast-forward
the primary clone's `main` with `--ff-only` and push `main`. If the fast-forward refuses because
`main` moved, merge and verify again in the worktree. Retire the worktree and its merged branch
only after the final task has ended.

A round of the private series, which `doc/periodic-review.md` describes, works the same way in
MAM-private: its shared worktree is
`C:/Users/BenDe/GitRepos/MAM-private/.claude/worktrees/dual-agent-review-<date>`, and its final
integration verifies with what MAM-private's `CLAUDE.md` requires in place of this repository's
mega.

In the September 8 round, Codex created
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08` on branch
`codex-review-2026-09-08` in turn 2 without instruction. The shared checkout worked: later turns
of both agents and the close-out used it. Ben's judgment on 2026-09-09 was that creating the
worktree had been a good idea, but its path and branch read as Codex's. The approved naming makes
the shared purpose explicit. The September 8 worktree and branch keep their existing names.

### The September 10 round

The September 10 exchange closed, and its remediation outcome is recorded in
`doc/review-findings-2026-09-10-update.md`. No separate fresh-task remediation plan was written;
do not fabricate one after the fact.

The September 14 round also keeps its historical names and author-specific role descriptions. It
began before Ben's 2026-09-16 Agent 1 and Agent 2 decision, used the shared worktree named
`dual-agent-review-2026-09-14`, and closed without a remaining disagreement after four turns. Ben's
approved close-out choices are recorded in `doc/review-findings-2026-09-14-update.md`. The neutral
roles and turn-01/turn-02 filenames above govern future rounds; they do not rename or rewrite that
finished exchange, and approval of its choices does not claim its remediation is complete.

### Remediation approvals: D7 and the risk ordering

Close-out step 3's approvals follow D7, "Separate defects from editorial proposals", and Ben's
ordering of remediation by public-facing risk. Both moved to `doc/periodic-review.md` on
2026-09-12, since they apply to every review and not only to a two-agent window.

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

## Review filenames and State lines — Ben's decisions, 2026-09-09 (D10) and 2026-09-16

The existing `doc/review-findings-<date>.md` series keeps its unprefixed name and is **not** renamed
to `claude-review-findings-<date>.md`. A Codex counterpart in the blind Design B procedure takes the
prefixed name `doc/codex-review-findings-<date>.md`. Those author-based names remain the single-agent
and blind-review convention; the standard sequential alternating round uses neutral numbered turn
files.

For future reviews, the filenames and states follow these rules:

1. **Number every turn of a standard alternating round:**
   `doc/dual-agent-review-<date>-turn-01-<claude|codex>.md`, then turn 02 and every later turn. The
   stem identifies the shared exchange, the number identifies its sequence, and the final component
   records the actual author. Agent 1 owns odd turns and Agent 2 owns even turns.
2. **Keep author-based names for single-agent reviews and blind Design B:**
   `doc/review-findings-<date>.md` remains the Claude series, and
   `doc/codex-review-findings-<date>.md` remains the Codex Design B counterpart. Reserve a suffix
   such as `-sol` for an exceptional additional review comparing or repeating the same blind role
   with a named model; September 7's `-sol` file is the worked example.
3. **Keep the historical finish state in the argument:** turn 01 of a standard alternating round,
   or the unprefixed file of a single-agent or blind review, records at line 3 what was true when
   that review finished. Every later alternating turn and every blind counterpart uses
   `State: completed <date>; review only`. Later remediation State and every disposition belong in
   the first argument's single live update file, not in a new section of the finished base review.
4. **Recognize all review files in the document standard:** the initial single-agent files, blind
   counterparts and exceptional additional reviews, and every numbered dual-agent turn. The older
   `doc/review-findings-*.md` glob in the standard's history names only the unprefixed series.
   Preserve historical filenames and `State:` lines, including September 4's Codex "acted on",
   September 8's turns under a Codex-prefixed stem, and September 14's mixed old and numbered
   naming.

For the single-agent and blind conventions, the asymmetry reads correctly: the unprefixed name is
the incumbent, and the prefixed name announces its difference. Repository instructions say that an
unprefixed name means the Claude series, so a reader meeting that convention is not left to infer
it. The standard alternating convention has no such filename asymmetry.

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

### 1. Scope Codex to its window's series, explicitly

A Codex agent that reads MAM-private and then writes any review turn into MAM-basics publishes
private material permanently, and no mechanism prevents it.
`py/repo_util/report_destination.py`'s guard makes it mechanically impossible for
`main_repo_util.py` to write a private-covering report into a public tree, but that guard's
docstring names what it deliberately does not cover: "what a human or an agent later types into a
`doc/` file". A Codex reviewer writing into `doc/` is exactly that uncovered case.

The public-only scope this repository's series has run under since 2026-08-26 removes this
structurally. Keep the Codex reviewer of a window of this repository's series inside that scope.

**A window of the private series has the opposite boundary: its records stay in MAM-private.** Ben,
2026-09-14: "I would like the MAM-private review process to be potentially dual-agent", and, on
where the Codex file goes, "wouldn't it be in MAM-private/doc/codex-review-findings-YYYY-MM-DD.md
or whatever the analogy with MAM-basics would dictate?" That quotation predates the neutral
numbered convention. A private window's Codex reviewer reads the private clones in its window and
writes only into MAM-private's `doc/`, using numbered turns for a standard alternating round and
the author-based name for blind Design B. As item 4 of `doc/periodic-review.md`'s section "The
private series, recorded in MAM-private" says, the Codex task reads MAM-private's `CLAUDE.md`
before its first check, since Codex does not load that file.

### 2. Limit the Codex reviewer to review records

A Codex reviewer writes only the numbered turn that belongs to Codex and, when Codex is Agent 2,
the specified reconciliation append to Agent 1's argument. A Codex reviewer does not modify source
files, generated products, or earlier findings. Two agents with write
access to one working tree can stage each other's half-written work, and that failure is clean and
therefore silent — the collision the worktree rules in `~/.claude/CLAUDE.md` exist to prevent, but
with no human turn between the two agents.

The record-only scope has to be maintained deliberately rather than inferred from a sandbox flag.
This document does not prescribe or assess current Codex sandbox syntax.

For the standard alternating round, give the Codex reviewer the shared worktree created under D11
above. Every successor uses that same checkout directly. A worktree runs the primary clone's venv
by absolute path.

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

`dot-Codex/user-wide-AGENTS.md` is canonical. After canonical changes integrate and `main` is
pushed, deploy from the primary clone with `py/main_repo_util.py --sync-user-config`; the command
fetches and installs only from fresh `origin/main`. Verify afterward with
`py/main_repo_util.py --sync-user-config --check`.

## What this document deliberately does not settle

1. **Whether every periodic window should have a blind parallel review.** Design B's calibration
   addresses that cadence; D9 already settles the standard dual-agent procedure.
2. **How to run Codex on this machine.** No command line is given here. Codex demonstrably runs
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
