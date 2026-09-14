# The periodic review: one agent, one commit window, one findings file

This document describes the periodic review as a procedure in its own right: what the series is,
what a review file contains, how a review is checked before it is acted on, and how its findings
reach dispositions. It was split out of `doc/dual-agent-review.md` on 2026-09-12 (Ben's
instruction that day), which now covers only the pairing of Claude and Codex on one window. **A
citation written before 2026-09-12 may name `doc/dual-agent-review.md` for material that is now
here**; such citations are left as written, as the stale `../masorah-books/` and `al-hatorah`
paths in `py/accgram/` are.

Read this before starting a periodic review. Read `doc/dual-agent-review.md` as well only when the
window is to be reviewed by two agents; D9 there chooses the procedure for such a window, and does
not require any window to have two.

## What the periodic review is

Every four to eight days one Claude session reads a commit range across the public repositories and
writes `doc/review-findings-<date>.md`. The cadence is observed, not prescribed.

Measured on 2026-09-12, ten files match `doc/review-findings-*.md`, dated 2026-07-29 through
2026-09-08, all of them window reviews. An eleventh file held the name until 2026-09-12, when it
was renamed `doc/blind-dive-into-template-params.md` on Ben's instruction: Codex had written it
(`fa07fd8f`) as a current-state review of template projection at one commit, not a review of a
commit window. Re-establish the census, and read the states rather than inferring them:

```powershell
git ls-files -- "doc/review-findings-*.md"
```

```powershell
git grep -n "^State:" HEAD -- "doc/review-findings-*.md"
```

## Two standing properties of the series

Two properties of the series matter to every review in it.

1. **The series is doc-only since 2026-09-01** (`5b89033`). **"Doc-only" says where a review is
   RECORDED, never what it may READ** — a distinction worth spelling out, because two documents
   written on 2026-09-09 both took it the other way, and either reading would send a session to Ben
   for a scope decision he does not owe. A review reads whatever the window changed in a public
   repository: `doc/review-findings-2026-09-08.md` is headed "review of the public repos" and
   accounts for 99 commits and 513 changed paths across Python, pages and data. What went doc-only
   is the RECORD. Each file carries a `State:` line at
   line 3 directly under the H1. The initial review records remediation state; later turns record
   review completion, under D10 in `doc/dual-agent-review.md`. The
   thin tracking issue every review used to file — wlc-utils#87, then MAM-basics #219, #228, #231,
   #232, #261, #263 — is retired, because every comment on all seven was agent-written from Ben's
   account and only #219 was ever adopted as a citation handle. A review that finds work somebody
   must do still files a real issue with a real body; #233 is that shape.
2. **The series is public-only since 2026-08-26.** It does not read MAM-private. This is load-bearing
   for the Codex scoping rule in `doc/dual-agent-review.md`, not incidental.

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

## What a review file contains

Nothing prescribes a review file's sections. The shape below is what the files share, and it has
travelled by imitation from one dated file to the next, so this section records it rather than
founding it. A review that departs from it should say why in its opening paragraphs.

1. **The H1 names the window**: "Findings of the <date> review of the public repos since <date of
   the previous review>". Through 2026-08-22 it read "of the work since <date>".
2. **Line 3 is the `State:` line**, directly under the H1: `not yet acted on`, or
   `acted on <date>` plus any clause naming what is not. `check_repo_standards.py`'s docstring is
   where that vocabulary is declared.
3. **The opening paragraphs say how the file was written**: which session, which commit it was frozen
   at, and anything that happened to it on the way into the tree.
4. **`## Scope, anchors and census`**: the commit range in each repository, named by commit, and a
   count of what the window changed.
5. **`## Tree health at <commit>`**: the suite's count and the lints, with the commit they ran on
   in the heading.
6. **`## What verifies sound, stream by stream`**: what the review checked and found no defect in,
   so that nobody re-derives it.
7. **`## Findings`**, numbered, with sub-findings numbered under them (4.2, 11.5). **Each finding's
   lead says what happened to it** — unfixed, fixed by a named commit, or raised and not fixed
   because of a stated reason — per `~/.claude/CLAUDE.md`'s prose section on dispositions.
8. **`## Open ends the window itself declares (not findings)`**: work the window's own commits say
   is unfinished, which is not a defect of the window.
9. **`## What this review did not check`**.
10. **`## Dispositions after remediation`**, added later, when somebody acts on the findings: one
    row per finding or sub-finding, each naming the commit that fixed it or the decision that
    closed it.

Items 4, 5, 6 and 9 first appear together in `doc/review-findings-2026-09-04.md`. From 2026-08-03
to 2026-09-01 a review usually fixed some findings during the review itself and said so under
`## How the review was acted on (<date>)`, and `doc/review-findings-2026-07-29.md` groups its
findings under `## Major` and `## Minor — <area>` headings. A review in a two-agent window also
carries `## Inputs for the reconciliation with the Codex review` and, after turn 2,
`## Reconciliation with the Codex review`; `doc/dual-agent-review.md` owns both.

## Reviewing the review, with the same agent and with Ben

**A review file can be reviewed again by the same agent before it is acted on, and the one time
that was done it found real defects each time.** This is worth trying, not established: it rests on
one review, `doc/review-findings-2026-09-10.md`, reviewed twice by Claude on 2026-09-12. Ben asked
for both passes, and for this section, on that day.

1. **Pass 1, `99ac89a7` (10:30).** It read the commits that had edited the file since it was first
   committed as `301d0fcc`, and corrected six passages: the `State:` line's shape; a lead saying
   "Nothing was fixed" that the dispositions table contradicted; finding 11.4 announcing 8 sites
   and enumerating 9; finding 11.5's count including the review file's own occurrence; a word in
   finding 20's lead that a terminology commit had missed; and a dispositions preamble naming the
   wrong branch. No finding's substance changed.
2. **Pass 2, `c8de6abc` (14:06).** It audited the whole document rather than the edits, and
   corrected four passages: finding 4 item 2 announced 7,247 clusters in 152 files and enumerated
   7,243 in 151; finding 7 item 3 said six earlier files carry `.novc` pointers where 41 do; a row
   of the dispositions table used a construction the review itself reports in three other files and
   carried a clause that had gone stale; and line 3 said the dispositions table "has a row per fix",
   which was wrong three ways. It reported two further items without an edit.

**The two passes found different things because they read different things.** Pass 1 read the edits
and checked them against each other. Pass 2 read the whole file and checked its arithmetic, and
that is what found the two census errors, both present since `301d0fcc` and so available to pass 1,
which never read those passages. Pass 2 also caught two defects in text written after the
original: the construction in the dispositions row, which `b5d5d8b1` wrote and pass 1 read without
catching, and the "row per fix" clause on line 3, which pass 1 itself wrote. **Every one of the ten
corrections is the kind of defect that survives the writing pass because the writer knows what was
meant**: a count that does not match its own list, a census that understates, a clause true when
written.

**Ben's part was a fact about the environment, not a judgment about the content.** During pass 2,
at 13:58, Ben wrote: "I fear that the the 2026-09-10 review file may have been updated during your
review. Look at any commits since your review and see if that influences your plan for edits to the
review file." Three commits had landed during the pass — `575114dc` and `39cdd0e3` on `main` and
`5f336b75` on the review branch — and between them they settled one of the items pass 2 had
planned to edit, and made line 3 wrong in a third way. The session had no reason to look. **A long
review pass does not see its tree move**, and a one-line prompt from a person who can see it is
enough. The standing safeguard is the
non-collision check `~/.claude/CLAUDE.md` already requires before a commit — `HEAD` at the start
equals `HEAD` immediately before committing — applied to the whole reading window of a review pass
and not only to its commit.

**Being wrong in a review of a review is cheap.** Pass 2 recommended replacing `State: open` with
`live` in the update files, and withdrew the recommendation on reading `39cdd0e3`, which had
declared `open` better. Nothing had been edited on the strength of the recommendation.

### How Ben walks through a review's findings

Ben's rules for an interactive walk through a review's findings, given on 2026-09-11 while the
2026-09-10 review was walked through and on 2026-09-14 while the 2026-09-14 review was. They are
what make his part of a review of a review work.

**What the walk-through is for.** Ben, 2026-09-14: it is mainly about Ben identifying what the
review findings are, to see whether he wants to weigh in on them, for example by suggesting a
different remediation or questioning a finding, and about the agent fixing up the findings' language
or, in extreme cases, weighing in as Ben does, for example by suggesting a remediation different
from those already present or questioning the finding itself. In his words: "Notably, this process
is unlikely to be about me fixing up review finding language, nor is it likely to be about me
questioning your proposed fix-ups to review finding language."

1. **Say which of two things is meant: the wording of finding N, or the problem finding N
   describes.** Never write a bare "fix finding N". Fixing the wording is the agent's part of a
   walk-through; fixing the problem is a separate decision Ben makes per finding.
2. **Say what a finding is before saying anything about it.** Ben, 2026-09-11: "You need to not
   just say something like 'I fixed finding 6.' that requires me to have in my head what finding 6
   is."
3. **Change nothing beyond what Ben asks.** Presenting a finding is not authorization to fix it,
   and a fix he does ask for lands off the review branch.
4. **Use one word for one thing.** The case: "record" was naming both a post-stress-meteg survey
   entry and a document's written account, until `3f962e62`.
5. **Summarize a finding's wording changes and offer the detail, rather than presenting each
   change.** Say what the finding is about and that there are wording changes to it, and offer to
   detail them. Ben, 2026-09-14, after finding 3 of the 2026-09-14 review was presented with
   eighteen wording corrections, each quoted as it stood and as proposed: "For the record it would
   have been sufficient for you to summarize what finding 3 was about and say you had various
   wording changes to it, and *offered* to detail them to me, which I would have likely declined yet
   still told you to go ahead and implement." Where the agent also weighs in, with a different
   remediation or a doubt about the finding itself, it says so plainly, since weighing in is what
   the walk-through is for.

## Close-out: from findings to dispositions

After a review is written, and after any review of it:

1. Record Ben's decisions on the choices the review leaves to him.
2. Write a remediation plan for a fresh task, including concrete wording for each editorial change,
   and obtain Ben's approval before execution. The two rules below govern how.
3. Execute the approved remediation, recording each finding's disposition under a
   `## Dispositions after remediation` section at the end of the review file. The rest of the file
   is left as written; a correction to it goes in `<stem>-update.md`, under `~/.claude/CLAUDE.md`'s
   section "A finished dated document is corrected in `<stem>-update.md`, never edited".
4. Integrate by the worktree procedure in `~/.claude/CLAUDE.md`, with step 2 a mega run, as
   `CLAUDE.md`'s section "Integrating a worktree branch here" requires.

### Verification cadence during remediation — Ben's decision, 2026-09-13

Remediation uses three verification gates, chosen by test-breakage risk rather than by the number
of commits or handoffs:

1. Every commit gets `git diff --check`, formatting for each changed source file, and directly
   relevant targeted tests or lints.
2. The full suite runs after the last change with a meaningful likelihood of breaking it:
   executable source, tests or test infrastructure, schemas, shared data, cross-repository path
   behavior, or another surface the repository identifies. Documentation, comments, review
   records and instruction-only commits are batched; none of those commits or handoffs by itself
   requires another full-suite run or expires the last relevant result. If no later test-risky
   change follows, that result remains the verification result for final close-out.
3. A targeted generator runs during development when useful for a product-affecting change. A
   repository-wide generation or regeneration pipeline runs earlier only when a generator,
   orchestration or product change makes a differential checkpoint materially useful, and always
   at the final integration gate where repository instructions require it. MAM-basics' complete
   mega is not a per-unit check.

Deferred broad verification still requires small, coherent commits, each intended to be valid.
A final failure may be isolated by bisect, but the cadence does not license a knowingly broken
intermediate commit. A repository-specific or user-explicit requirement for more verification
wins. Test-breakage risk remains separate from the public/product risk and hard-to-undo-act axes.

The 2026-09-10 remediation is the case that produced the rule. At the time of Ben's decision, the
live update summarized 18 successful full-suite runs; the known actual lower bound was 20 because
an earlier finding-10 run had been replaced in the live section and the finding-10
final-disposition task ran the suite twice. No remediation-chain mega had run, and one mega
remained reserved for final integration. Those figures are historical evidence that the per-unit
full-suite cadence was disproportionate, not a count a future close-out must re-measure.

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

## What this document deliberately does not settle

1. **The cadence.** "Every four to eight days" describes the series; nothing requires it.
2. **Whether a window has one reviewer or two.** D9 in `doc/dual-agent-review.md` settles the
   procedure for a two-agent window and leaves the choice open.
3. **Whether a review is reviewed again before it is acted on.** The section "Reviewing the review,
   with the same agent and with Ben" records one case and recommends trying it; it does not require
   it.
