# Codex review of the 2026-09-08 Claude review

State: completed 2026-09-09; Design A comparison and reconciliation recorded. No remediation
was performed. The September 9 decisions already recorded by Claude remain in force.

This is the Codex second side of `doc/dual-agent-review.md`, Design A. It checks the claims in
`doc/review-findings-2026-09-08.md` against the same public commit ranges. It also checks whether
the review leaves material changes or consequences unaccounted for. It is an anchored review,
not a blind second census of defects.

The main record findings reproduce, including the untouched whitespace defects and the
maintenance runbook's contradiction of its policy. Some conclusions need correction before
the review becomes a remediation checklist: successful assertions were described as if they
did not check claims, later edits were treated as errors in earlier commit messages, and
prose rules were extended beyond their stated scope. The MAS wording reversals require a
record of Ben's decisions, not automatic reinstatement of the reversed edits.

## Scope and verification

| Item | Verified scope |
|---|---|
| MAM-basics review range | `8bf586a3c4b2d955bc2ca1b0233e504594945d48..38a606e2a2f8d4b34d972f4634be40f13ec132d8` |
| MAM-simple review range | `9a350be5..376912a758443bb0c015bd77dfca5bef3e97f9c9`, read through the GitHub comparison API |
| Review checkout | `C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08` |
| Review branch and starting commit | `codex-review-2026-09-08`, `becc6f0014e1646d47c3b63239945e3b7838d17e` |
| Later material included deliberately | `e56ae06a` records Claude's findings; `3b0225e0` records Ben's decisions on findings 1 and 3; `becc6f00` records resolution of the skill-copy discrepancy |
| Instructions | Global Codex instructions; repository `CLAUDE.md` (the repository has no `AGENTS.md`); the dual-agent procedure; `hebrew-prose` and its rendered-prose reference |
| Division of work | Fresh agents checked MAS claims and remediation records. The coordinator checked the census, public repository coverage, decisive evidence, and this reconciliation |

The Git census reproduces **98 MAM-basics commits, 92 non-merge commits, 81 first-parent
commits, 43 without a co-author trailer, and 42 with only a subject**. The exact trailer
spellings and their counts reproduce. The endpoint diff has 19 additions, 14 deletions and
480 modifications: 513 paths. MAM-simple has exactly one commit, changing only the date in
its README breadcrumb. The fourteen public repositories Claude calls quiet return no commits
for the bounded interval `2026-09-07T14:35:00Z` through `2026-09-09T01:49:57Z`.

All MAM-basics hashes and changed paths were catalogued. A hash absent from the narrative is
not, by itself, an omitted change: many page commits are covered by the review's grouped
descriptions. No additional substantive commit family was found missing from those
descriptions. The corrections below concern the conclusions drawn from the evidence.

The canonical suite was run once in the review checkout at `becc6f00`, using the primary
clone's interpreter and `REPOS_ROOT=C:/Users/BenDe/GitRepos`: **983 passed, 5 skipped,
65 subtests passed in 124.74 seconds**. The tracked working tree was clean before and after.
This is a new run at the review checkout's starting commit; it is not a claim to have rerun
the suite at every historical commit. The invocation was:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider
```

Run that command from the review checkout after setting the sibling root:

```powershell
$env:REPOS_ROOT="C:/Users/BenDe/GitRepos"
```

Targeted independent checks included the full original whitespace finding set, the Holman
table cells, pinned commit contents, the MAS JSON partitions, and adverse probes of the
assertions described below. No source file, generated page, global instruction, issue, or
existing finding was changed. Only this file and the appended reconciliation were written
as tracked review records.

## Corrections to Claude's findings

### C1. The MAS assertions detect counterexamples

**Reject the implication in finding 13.2 that the multiplicity assertions make the Methods
claim true without checking it.** `_census_chanted_word_summary` at `38a606e2`, lines
1630–1635, raises if a MAS chanted word has multiple post-stress records, or if a MAS chanted
word with a pre-stress meteg has multiple pre-stress records. An adverse duplicate-record
probe raises `AssertionError` in each case. The assertions stop generation; they neither
discard the counterexample nor emit a falsely reassuring result. The existing data has
232 distinct MAS keys, each with exactly one post-stress record.

The broad category definition using "one or more" and the narrower observed multiplicity
are compatible. A future corpus counterexample would require a decision about the published
claim and the implementation. That possible future work does not make a present guard a
defect, and does not justify removing the guard now.

**Reject finding 13.7's claim that conjunctive stress is pinned only by counts derived from
the same rule.** `stress_accent_classification`, lines 1155–1200, reparses each MAS record's
stress-letter accent and raises `SurveyProblem` when the accent is not a regular conjunctive.
Changing that accent in an adverse probe triggers the exception. This is an explicit check,
not merely a constant zero in a returned count. The scope remains the MAS records recognized
by the survey; the check does not independently adjudicate the exceptional verse-final
interpretation in finding 1.

Disposition: the assertions remain unchanged. Correct the assessment in the reconciliation;
do not turn findings 13.2 and 13.7 into instructions to weaken validation.

### C2. Later changes do not falsify earlier commit messages

**Reject items 17(b), 17(c), 17(d), and 17(e) as immutable-message errors.** Each claim holds
in the commit whose message states it:

1. `fe4e602f` has the census 263,191 / 14,752 / 232 in its HTML. The merged census changed later.
2. `bdcdc5e2` defines the fit types as 2A and 2B. `97a1b46f` later refines their names to 2Af
   and 2Bf.
3. `24f1e4a3` adds `gh-pages/post-stress-meteg-type-1.html`. The later consolidation removes it.
4. `95c457c2` has the explanatory paragraph its message describes, in that commit's HTML at
   lines 425–435. Later page revisions do not invalidate the message.

These are accurate records of earlier states. Preserve the messages. Distinguish those cases
from item 17(a), where the merge message's 36 hunks disagrees with the reproduced 32 hunks.
The later prose reversals in item 17(f) likewise establish a subsequent change, not a false
description of what `e91d7358` initially did. Incomplete remediation in item 17(g) is supported
by the still-unfixed findings, especially Sol-1; it does not follow merely from later reverts.

Disposition: reject the error classification for 17(b)–(e). Retain historical changes as
history and record any current unfinished work separately.

### C3. Finding 16 extends prose rules beyond their stated scope

Finding 16 extends the "has" rule from a corpus, manuscript, edition, atom or chanted word
having a mark to any file or directory having text. The inspected rule does not establish
that extension. Its examples involving files that "carry" text are not established
violations of that rule.

The treatment of "hand transcriptions" and "hand corrections" also needs narrowing.
`b4706759` explicitly declines a sweep and distinguishes cases where context identifies the
author from vague claims about how text was produced. `DATA-LICENSES.md` identifies the
contributors in the relevant passages. The commit does not establish a blanket ban on those
phrases or an instruction to replace them everywhere.

The specific numbered-list and unclear-referent observations can be considered on their
merits. They do not authorize a general rewrite of the window's records or Ben's page prose.

Disposition: reject those generalized rule violations; leave the text unchanged.

### C4. A different suite run does not explain a missing output line

Finding 11.1 correctly observes that the current suite prints a subtest line. It does not
establish that the Wave 4 run's missing line "was a reporting artifact." The Wave 4 record
expressly reports what that particular run printed and declines to infer a count. A later
run, including this review's run, cannot establish the omitted line's cause in an earlier run.

The separate undated/current claim that the suite "no longer prints a subtest line" is
contradicted by the present run and still needs a dated correction. Keep that current claim
separate from the historical observation about the Wave 4 run.

Disposition: qualify finding 11.1; do not invent an explanation for the historical output.

### C5. The procedure incorrectly says Codex cannot load the Hebrew prose skill

The prerequisite section of `doc/dual-agent-review.md` says Codex "will never load" the
`hebrew-prose` skill. The same document's provenance section records that the skill governed
the earlier Codex pipeline review. The Codex reviewer can also load the supplied skill in
the present review. The absolute inability claim is false; automatic loading from
Claude-specific locations and the ability to load a supplied skill are different questions.

Finding 10 notices the procedure's stale review census and naming policy but omits this
premise. The September 8 change updates the neighbouring prerequisite paragraph without
resolving the contradiction.

Disposition: unfixed procedure-record error. Correcting that premise is separate from
changing any MAS prose or instruction policy.

## MAS decisions and the scope of future remediation

The public records establish that the September 8 prose reversals were deliberate. The
messages of `1095f029` and `a9edd4f9` identify unrequested rewrites and Ben's instruction to
revert them; `825cef66` restores the declared plain "word" vocabulary. A reconciliation
should update the earlier "fixed" rows to describe those decisions. It should not label
every reversed editorial change unfinished work awaiting reinstatement.

The plan already contains broad editorial instructions that made those changes executable:
`doc/PLAN-remediate-review-findings-2026-09-07.md`, at `47edbee6`, directs the executor to
decide the type-3 rule, replace the BHS attribution, and "Apply every prose correction,"
including loose "word". The checklist does not identify which concrete MAS rewrites Ben
has approved. A general instruction to execute that checklist is not evidence of separate
approval of every editorial choice embedded in it. This is a process omission beyond merely
noticing that disposition rows became stale.

For any later remediation proposal, separate a reproducible data or code defect from a
proposed change to the document's terminology, organization, scholarly interpretation or
source attribution. Present the concrete MAS wording changes for Ben's approval before
applying them. Where Ben has already decided, record and follow that decision instead of
asking again or treating the review as contrary authorization.

The September 9 dispositions are therefore carried forward:

1. **Finding 1:** `3b0225e0` defines "ignore" as the deliberate interpretation Ben selected.
   The survey classification remains unchanged. No classifier correction follows from the
   earlier ambiguity alone.
2. **Finding 3:** Ben's direct BHS reading is recorded in the source docstring and the prior
   review's disposition note. The BHS wording stands; the objection to calling WLC and UXLC
   editions was withdrawn. Replacing those labels again would contradict the settled decision.
3. **Finding 5.6:** the named `sources-and-corpora.md` copies in `.agents`, `.claude`, and the
   tracked instruction-copy location are byte-identical on September 9: 18,785 bytes each,
   SHA-256 `9f0d5dfd15794496642f1067d98fda6e9148fb6a286e4a7d7247e7e29a8507a0`.
   This identity check is the procedure's existing, narrow instruction-plumbing exception.

Finding 14.4 also needs a precise description of the missing skill exception. The skill's
opening does not contain the quoted permission "wherever the context already settles which
sense is meant"; that wording is in the repository instructions and is attributed back to
the skill. Ben's explicit repository exception remains valid. The inaccurate attribution is
a refinement of finding 14.4 and issue #265, not a reason to qualify "word" again on the pages.

The paragraph count in finding 14.1 needs the same care: the definition is the second
expository paragraph and the third HTML `p` because the spacing control uses a `p`. The claim
that no earlier sentence uses "word" is false; the choice to call the definition the second
paragraph is defensible. The manually enumerated page tuple still cannot detect a newly
added page automatically, as finding 14.2 says.

## Reconciliation by Claude finding

The comparison table is appended to `doc/review-findings-2026-09-08.md`. Confirmed means the
specified observation was independently checked; it does not mean that a particular remedy
has been approved. Qualified and rejected refer to review conclusions, not silent edits of
Claude's original text. Unfixed findings remain unfixed unless a dated disposition already
records Ben's decision or completed work.

## Limits

This review did not read the private scholarly sources, adjudicate manuscript crops or
printed-edition readings, rerun the private-input survey or the mega pipeline, or regenerate
the tracked product trees. The complete independent phonetic corpus comparison, all source
attributions, and every claim in Claude's stream summaries were not repeated. The comparison
does not claim that an unchecked statement has been confirmed.

No historical test run was reconstructed. Pages workflow and issue-timeline claims were not
independently audited. Filesystem housekeeping and the Recycle Bin were not reviewed or
changed. The separate question about the previous remediation task's context and compaction
was investigated outside the public review records; no transcript content is published here.

The review records are committed only on the local review branch. Integration into `main`
remains scheduled immediately before this task is archived, under the global worktree rule.
