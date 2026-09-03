# Running the periodic review with both Claude and Codex

**Nothing in this document has been run.** It records a recommendation Claude made on 2026-09-01,
in a session titled "Claude and Codex complementary workflows", and it was written down on
2026-09-03 because until then the recommendation existed only in that session's transcript and had
to be recovered by searching transcripts. The periodic review is still a Claude-only practice, as
it has been since 2026-07-29.

Read this before adding a second reviewing agent to the review series. It does not describe
anything the repository currently does.

## What the periodic review is today, and what a second agent would join

Every four to eight days one Claude session reads a commit range across the public repositories and
writes `doc/review-findings-<date>.md`. Seven such files exist, from 2026-07-29 to 2026-09-01.

Two properties of the series matter to everything below.

1. **The series is doc-only since 2026-09-01** (`5b89033`). Each file carries a `State:` line at
   line 3 directly under the H1, reading `acted on <date>` plus any clause naming what is not. The
   thin tracking issue every review used to file — wlc-utils#87, then MAM-basics #219, #228, #231,
   #232, #261, #263 — is retired, because every comment on all seven was agent-written from Ben's
   account and only #219 was ever adopted as a citation handle. A review that finds work somebody
   must do still files a real issue with a real body; #233 is that shape.
2. **The series is public-only since 2026-08-26.** It does not read MAM-private. This is load-bearing
   for the Codex scoping rule below, not incidental.

The convention of record for both properties is the "The doc/ directory standard" section of
`py/repo_util/check_repo_standards.py`'s module docstring. Read it there rather than re-deriving it.

## Start with one calibration run, not a standing parallel track

The series runs every four to eight days, so running two agents on every window is a standing cost
against a benefit nobody has measured. Run the dual-agent version **once**, reconcile it, count the
buckets, and only then decide.

1. **If the Codex findings are largely a subset of the Claude findings**, a parallel track is not
   worth its cost. The better shape is to **alternate**: every other review is a Codex review. That
   buys decorrelation across windows at no added cost per window, at the price of never learning
   which agent misses what.
2. **If the two overlap little**, the parallel track is earning its keep and becomes standing
   practice.

Nobody has run either design, so this document has no measurement to report and neither outcome is
predicted here.

## Two designs, and why to try the anchored one first

**Design A, Codex reviews the finished Claude review.** Point Codex at the completed
`doc/review-findings-<date>.md` **plus** the same commit range, and ask two questions: which claims
in this file are false, and which commits in the range does it fail to account for.

**Design B, the parallel blind sweep.** Both agents review the same commit range at the same time,
neither seeing the other's output, each writing its own findings file.

The trade is clean, and neither design subsumes the other. **Design B catches misses**, because the
Codex review looks where the Claude review did not. **Design A catches errors**, because it
re-derives claims that are already written down — but it is anchored to the Claude review and so
will not look anywhere that review did not.

**Design A is the recommended starting point on two grounds.** The record says errors dominate here:
`251b287`'s commit message is "Record the 2026-09-01 review's findings, and fix the record errors it
found", and the series' output is heavily claims in `CLAUDE.md` and `doc/` that turned out to be
wrong. And Design A is roughly a fifth of the work of Design B, so it tests the pairing cheaply.

Design A does not need the blindness rule below, because it is anchored by construction. Everything
from "Keep the two reviews blind" to the end of the reconciliation section applies to Design B only.

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

## Reconcile the two reviews into four buckets — do not merge them into one findings file

Two findings files sitting side by side in `doc/` are worth nothing unless something compares them,
because nobody will do it later. The comparison sorts every finding into one of four buckets.

1. Both reviews found it.
2. Only the Claude review found it.
3. Only the Codex review found it.
4. **The two reviews assert incompatible facts.**

**Bucket 4 is the highest-value output of the whole arrangement.** It means at least one review is
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

Each finding in the reconciliation carries a disposition, written down: fixed, or rejected with the
reason. Without that, an agent silently drops the findings it does not like and reports that it
addressed the review.

## Name the Codex file `doc/codex-review-findings-<date>.md`, and do not rename the Claude series

The Codex counterpart takes the prefixed name `doc/codex-review-findings-<date>.md`. The existing
`doc/review-findings-<date>.md` series keeps its unprefixed name and is **not** renamed to
`claude-review-findings-<date>.md`.

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

### 2. Keep the Codex reviewer read-only

A review agent has no reason to write. Two agents with write access to one working tree stage each
other's half-written work, and that failure is clean and therefore silent — the collision the
worktree rules in `~/.claude/CLAUDE.md` exist to prevent, but with no human turn between the two
agents.

**On Windows this is an honour system rather than a sandbox.** Codex's sandboxing is built around
macOS Seatbelt and Linux Landlock, and its supported Windows path has been WSL; a native Windows run
is unsandboxed. So the read-only property has to be maintained deliberately rather than assumed from
a flag. This has not been tested on this machine — see the closing caveat.

If the Codex reviewer is nevertheless given a working tree, give it its own git worktree rather than
the primary clone, per `~/.claude/CLAUDE.md`'s worktree section, and note that a worktree runs the
primary clone's venv by absolute path.

## A precondition this document does not own: `~/.codex/AGENTS.md`

Codex reads `AGENTS.md`. It will never load `~/.claude/CLAUDE.md` or the `hebrew-prose` skill, which
is where most of the conventions a review checks against actually live — so without an `AGENTS.md`,
a Codex reviewer's findings are noise for reasons that have nothing to do with the review procedure:
it will hand back `python -c` one-liners, bash `&&` chains and `sed -i` edits, all three of which
Ben's global rules ban on measured grounds, and it will report house conventions as errors.

**This is a general prerequisite for using Codex on any of Ben's repositories, not a step of this
procedure, and it is tracked separately** — Ben's decision, 2026-09-03. It is recorded here only so
that a session running a Codex review knows the dependency exists and can check whether it has been
met. The natural home is `github-misc`, which already tracks `dot-claude/CLAUDE.md` and
`dot-claude/skills/`, so a `dot-codex/AGENTS.md` alongside them would fit the existing pattern and
inherit that repository's drift check. As of 2026-09-03 `github-misc` has no `dot-codex/` directory.

## What this document deliberately does not settle

1. **Whether to adopt the parallel track at all.** That is what the calibration run decides.
2. **Whether Codex ever reviews the private side.** Setup item 1 defers this rather than answering it.
3. **How to run Codex on this machine.** No command line is given here, because none has been tested.

## Provenance and caveat

The recommendation recorded here was made by Claude on 2026-09-01 and is written down unrun. Its
claims about Codex — the `AGENTS.md` mechanism, the sandboxing story, the Windows path — come from
Codex's documented behaviour, **not from any test on this machine.** Codex has never been run here.
Treat any specific flag or file-name spelling as the shape of the thing rather than as current
syntax, and verify before relying on it.
