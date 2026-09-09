# Plan: close out the 2026-09-08 review, every step on Codex — turn 5 handed off, Ben's decisions taken, the procedure recorded, the findings remediated, the worktree retired

State: live 2026-09-09; no step started; the starting state was re-measured the same afternoon
after `main` moved, the dated notes below supersede the table where they differ, and the design
was revised that afternoon on Ben's decision to keep the work on the branch until the end, and D9 and
the substance of D11 were decided the same afternoon (step 2).

Status updated 2026-09-09 after step 1: Ben closed the review exchange with the
skill-reading time left unknown. Step 1 is complete; step 2 is active. Ben's exact
decision is recorded below, beside step 1's earlier execution line.

Written 2026-09-09 by the Claude session that wrote turn 5, at Ben's request of that day for "a
concrete plan of steps that includes this handoff of turn 5", assuming, in his words, "arbitrarily,
everything that can be run on Codex is run on Codex". Ben's decision, 2026-09-09: Claude is not used
for any step below; the one Claude act left is the archival of the session that wrote this plan,
which is step 0. Every step names its actor, its input, its output and its commit discipline. A
Codex step is one Codex task, launched by Ben with the prompt given under it, run in the review
worktree on the review branch. **Ben's decision, 2026-09-09, afternoon: the work stays on the
review branch in the review worktree throughout.** No task fast-forwards `main` or pushes, the
archival in step 0 does not integrate, each task merges `main` into the branch before it edits,
and the four-step integration runs once, at the end of step 6, before the worktree is retired.
That replaces this plan's first design of the same day, which integrated at step 0 and at the
end of every task; Ben's question was why the work should not simply continue on the branch,
and there was no reason. Nothing in this plan is remediation: the remediation is planned in
step 4, approved in step 5 and executed in step 6.

## The state this plan starts from

Measured 2026-09-09 about 13:00 in the review worktree, at the commit that adds this plan.
Re-measure before step 1 and treat a mismatch as a finding.

| Item | State |
|---|---|
| Review worktree | `C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`, a linked worktree of `C:/Users/BenDe/GitRepos/MAM-basics` (`git rev-parse --git-common-dir`), branch `codex-review-2026-09-08`, clean (`git status --porcelain`) |
| Branch against `main` | `main` and `origin/main` at `a50da28b`; the branch holds `2b365153` (turn 5), `7c4416cd` (its addendum) and the commit that adds this plan, and nothing else (`git log --format="%h %s" main..codex-review-2026-09-08`). Superseded the same afternoon: see the re-measurement below the five documents |
| Disputes between the reviewers | None. Turn 5 closes the three the rebuttal listed: 1. finding 14.4; 2. C1 / finding 13.2; 3. C2 / finding 17(b)–(e). It also accepts Codex's treatment of finding 6.8 |
| Decisions already taken | `3b0225e0` and `becc6f00` (findings 1, 3 and 5.6, 2026-09-09), and Ben's request that this plan assume Codex for every step |
| Decisions pending | D1–D11 under step 2, all Ben's; D9 and the substance of D11 were decided on 2026-09-09 and are recorded there, and D11's naming is proposed there for Ben's yes or amendment |
| Suite baseline | 983 passed, 5 skipped, 65 subtests passed, Codex's run at `becc6f00` in the review worktree (`doc/codex-review-findings-2026-09-08.md` §"Scope and verification"); turn 5 ran no suite |
| Other sessions | A Claude session may be live in the primary clone; integration touches that clone only by fast-forward. No Codex task is live in the review worktree when step 1 starts, step 0 having ended the Claude session there |
| Turn-5 scripts | `turn5_verify.py`, `turn5_verify2.py`, `turn5_addendum_edit.py` and the two reports, untracked at `C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08/.novc/review-2026-09-08/` and copied to `C:/Users/BenDe/GitRepos/MAM-basics/.novc/review-2026-09-08/`, which survives step 7 |

The round's five documents, each read at the commit named:

1. The Claude argument, `doc/review-findings-2026-09-08.md`, `e56ae06a`, with the reconciliation
   table appended at `5636d38a`.
2. The Codex counter-argument, `doc/codex-review-findings-2026-09-08.md`, `5636d38a`.
3. The Claude rebuttal, `doc/codex-review-findings-2026-09-08-claude-rebuttal.md`, `da4e40a5`.
4. The Codex counter-rebuttal, `doc/codex-review-findings-2026-09-08-codex-counter-rebuttal.md`,
   `ad5d9f43`.
5. Claude turn 5, `doc/codex-review-findings-2026-09-08-claude-turn-5.md`, `2b365153`, with its
   addendum at `7c4416cd`.

**Re-measured 2026-09-09 about 13:50, after the table above was written: `main` and
`origin/main` had moved to `63ac5b84`**, by seven commits of 13:03–13:39 authored Ben Denckla from
the primary clone (`847862f9` … `63ac5b84`; `git log --format="%h %ci %s" a50da28b..63ac5b84`),
none of them on this branch, so the branch no longer contains `main`; under rule 3 the step-1 task
merges `main` into the branch before it reads anything else. What they change, and what it means
for the steps:

1. `doc/dual-agent-review.md` gains the paragraph pinning "doc-only" to the record rather than
   the reading, the paragraph declaring the github-misc byte-compare exception spent, and the
   `dot-Codex/user-wide-AGENTS.md` canonical location. Its "will never load" sentence is line
   274 and its "Eight such files" census line 25 at `63ac5b84`, unfixed, so step 3's targets
   stand; step 3 works on the merged file.
2. Two records arrive, `doc/PLAN-remediate-instruction-file-review-findings-2026-09-09.md`
   (`State: live`, nothing acted on) and `doc/assessment-two-stranded-artifacts-2026-09-09.md`.
   The first bears on D1 and D2 as noted under each; it edits neither of step 3's sentences.
3. github-misc leaves `all-repos.code-workspace` and `repo_visibility` (`63ac5b84`), the step its
   message says precedes retiring the clone at Ben's request; the clone was still on disk at
   13:50. Nothing in this plan reads that clone.
4. Three docstrings change (`check_repo_standards.py`, `report_destination.py`,
   `test_prose_conventions.py`), with no change to what any test checks; `63ac5b84`'s message
   records the suite at 983 passed, 5 skipped at that head, so the baseline stands.

## Rules every Codex task in this plan follows

1. **Verify the checkout before reading**: `git rev-parse --show-toplevel`,
   `git rev-parse --abbrev-ref HEAD`, `git rev-parse HEAD` and `git status --porcelain`, all in the
   worktree. The branch is `codex-review-2026-09-08`. The required commit the prompt names must be
   `HEAD` or an ancestor of it (`git merge-base --is-ancestor <required> HEAD`); inspect any
   mismatch before proceeding. The required commit is always the previous step's reported commit,
   which Ben pastes from that step's report.
2. **Read the instructions**: `~/.codex/AGENTS.md`, the repository `CLAUDE.md`, and, for any task
   that writes prose about accentuation, the `hebrew-prose` skill at
   `C:/Users/BenDe/.agents/skills/hebrew-prose/SKILL.md` with its four `references/` files. No
   repository `AGENTS.md` exists.
3. **Merge `main` into the branch first; then commit on the branch only.** After verifying the
   checkout, `git merge --no-edit main` in the worktree, any conflict resolved on the branch, so
   that the task edits files as `main` has them. Commit the files the prompt names and nothing
   else, with the message written to a temp file and passed with `git commit -F`; each task also
   appends one line, "Executed <date>: commit <id>", under its step's heading in this plan, in
   the same commit. No task fast-forwards `main` or pushes: the integration below runs once, at
   the end of the final step-6 wave.
4. **Never rewrite a dated record.** A correction to any review record or plan record is a dated
   note beside the text it corrects; the five documents of the round keep their text.
5. **Any Hebrew written into a file goes through `has_std_mark_order` before the commit**
   (repository `CLAUDE.md`, first section); Python touched means black on those files
   (`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m black <files>`); no
   `python -c`, no heredocs. A task that touches no Python says so.
6. **Report** the full path of every file written, every commit ID, the branch head, and anything
   unresolved. The report is the next step's input, and the branch head is the next step's
   required commit.

## Integration, once, at the end of the final step-6 wave

The four steps of `~/.claude/CLAUDE.md` §"Git & commits", which `~/.codex/AGENTS.md` shares, run
from the review worktree with the primary clone's interpreter, by the task that executes the
remediation plan's final wave and by no other task:

1. `git merge --no-edit main` in the worktree; resolve any conflict on the branch.
2. The suite on the merged tree, after `$env:REPOS_ROOT="C:/Users/BenDe/GitRepos"`:
   `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q`. Expect 983
   passed, 5 skipped unless the task added tests; any other result is fixed by a further commit on
   the branch, never on `main`.
3. `git -C C:/Users/BenDe/GitRepos/MAM-basics merge --ff-only codex-review-2026-09-08`. If it
   refuses, `main` moved: return to 1.
4. `git -C C:/Users/BenDe/GitRepos/MAM-basics push`.

## Step 0 — Ben archives the Claude session that wrote this plan, without integration

Actor: Ben, then that session. Ben asks the session to archive. By Ben's decision of 2026-09-09 it
does not run the integration procedure — the worktree rule's archival clause is set aside for this
branch, which continues under Codex — and it reports the branch head, which is step 1's required
commit. Output: the branch clean at that head, `main` untouched, no Claude session live in the
worktree.

## Step 1 — Codex reads turn 5 and records its acknowledgment: the handoff

Executed 2026-09-09: commit `8c49cdd2666382fe838d50affdff432e381c2694`; objection recorded; step 1 stops for Ben's decision.

**Ben's decision closing the review exchange, 2026-09-09:**

> Leave Claude’s skill-reading time unknown. The uncertainty does not affect the review’s conclusions. Close the review exchange and proceed to step 2.

The timing objection no longer blocks close-out. Step 1 is complete and the review
exchange is closed. The original review conclusions stand; the earlier acknowledgment
remains a dated record of the objection Ben has now disposed of.

Actor: Codex, one task. Input: the required commit from step 0. Output: a dated section appended to
the Codex counter-rebuttal, committed on the branch. If that section records an
objection, the plan stops here: Ben decides how the objection is handled before step 2.

Prompt to paste, with the required commit filled in:

```
Acknowledge turn 5 of the experimental September 8 dual-agent review.

Use this existing worktree directly:
C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08

Before reading, verify the checkout path, branch, HEAD, and working-tree status. The branch is codex-review-2026-09-08. The required commit is <required commit>. A newer HEAD must contain that commit as an ancestor. Inspect any mismatch before proceeding. Then merge main into the branch with git merge --no-edit main, resolving any conflict on the branch, before reading further.

Read applicable global instructions, repository CLAUDE.md, and the hebrew-prose skill with its references. No repository AGENTS.md exists. Read doc/PLAN-close-out-review-2026-09-08.md; this task is its step 1 and follows its rules.

Read doc/codex-review-findings-2026-09-08-claude-turn-5.md, including its addendum. It is Claude's closure check on your counter-rebuttal: it accepts every concession, closes the three disputes the rebuttal listed, withdraws the rebuttal's "in the skill nowhere" on your evidence, and dates that paragraph to github-misc 9ea78d2. Check each claim it makes about your documents or about a commit against the commit objects.

Append one dated section to doc/codex-review-findings-2026-09-08-codex-counter-rebuttal.md, headed with its outcome: "Turn 5 read 2026-09-DD: no objection", or "Turn 5 read 2026-09-DD: objection", quoting each disputed claim exactly and naming the decisive evidence. Change nothing else in that file and nothing in any other record.

Public evidence only. Review only: no remediation, no process changes, no edits to earlier records. Commit only that edited document and this plan's execution line on codex-review-2026-09-08. Do not fast-forward main and do not push. Reply with the full file path, the commit ID, the branch head, and anything still unresolved.
```

## Step 2 — Ben decides D1–D11

Started 2026-09-09 on Ben's instruction above. D9 and the substance of D11 remain
decided. D1–D8, D10, and D11's naming await Ben's choices; the review-closure
decision settles the timing objection rather than those separate choices.

Actor: Ben. Input: the rebuttal's "Choices requiring Ben's judgment", finding 10, the Codex
reconciliation, and Ben's two decisions of 2026-09-09 recorded under D9 and D11. Output: eleven
decisions, pasted into the prompts of steps 3 and 4 with the template below. Where the two
reviewers converge the convergence is stated; apart from D9 and D11, nothing here is a decision.

1. **D1 — the "will never load" sentence in `doc/dual-agent-review.md`** (line 258 at `49609331`;
   finding 10 with C5). The rebuttal's proposed wording: "Codex reads `AGENTS.md`, not
   `~/.claude/CLAUDE.md`, and loads the `hebrew-prose` skill only from its copy under
   `~/.agents/skills/` — which is why that copy exists, and why finding 5.6 of the 2026-09-08
   review compares it byte for byte." Approve it or give other wording. Since `74d883d2` the
   skill's canonical copy is `dot-claude/skills/hebrew-prose/` in MAM-basics, which the wording
   may name. Executed in step 3. Noted 2026-09-09: the instruction-file plan's D3 cites this
   sentence's `CLAUDE.md` half — Codex does not load `~/.claude/CLAUDE.md` — as the fact deciding
   its structural question; that half is true and the rebuttal's wording keeps it, so the two
   plans do not collide.
2. **D2 — `SKILL.md:19–20`'s "only"**, against `references/terminology.md:26` (finding 14.4). The
   rebuttal's proposed sentence: "Plain 'word' survives for an ordinary English word, inside quoted
   or translated source material, and wherever the context already settles which sense is meant
   (`references/terminology.md`)." Approve, amend or leave. A yes is a MAM-basics change now: edit
   the live `~/.claude/skills/hebrew-prose/SKILL.md`, copy it to `dot-claude/skills/hebrew-prose/`
   and to `~/.agents/skills/hebrew-prose/`, and run `dot-claude/README.md`'s two comparisons. It
   bears on #265's registry proposal. Executed in step 6. Noted 2026-09-09: the instruction-file
   plan's D6 also edits `SKILL.md`, its frontmatter description; the two edits touch different
   lines, and whichever executes second re-runs the comparisons.
3. **D3 — where the rebuttal's accepted corrections are recorded**: a dated addendum under
   `doc/review-findings-2026-09-08.md`, or the rebuttal file alone. The corrections: 13.2's filing,
   13.5, 13.7, 14.1, 16's eight withdrawn sites, 17's heading and 17(e)'s count, 11.1's clause,
   finding 10's omission of C5, the `47edbee6` process finding, and turn 5's withdrawal of "in the
   skill nowhere". Executed in step 6 if an addendum.
4. **D4 — the Wave 4 record and finding 5.1**: a dated note at
   `doc/PLAN-remediate-review-findings-2026-09-07.md:523` (at `38a606e2`) that the run's command is
   unrecorded and that Wave 6 at 981 tests printed 65 subtests; and a dated correction of
   `doc/PLAN-evacuate-the-rest-of-three-repos.md:1853`'s "no longer prints a subtest line". Both
   reviews want both. Yes or no. Executed in step 6.
5. **D5 — finding 13.2's design note**: leave the assertion-plus-literal as it is, which both
   reviewers recommend, or report MAS multiplicity as a JSON count the way MBS multiplicity is, with
   a Methods-page sentence whose wording comes to Ben in step 5. Executed in step 6 if the count.
6. **D6 — `DATA-LICENSES.md:88`**: whether "hand corrections" says whose. Executed in step 6.
7. **D7 — Codex's process rule for future remediation**: separate a reproducible data or code
   defect from a proposed change to the MAS pages' terminology, organization, interpretation or
   attribution, and present concrete wording for approval before applying it. Adopt as standing,
   and where to record it, or apply it to this remediation only; step 4 applies it either way.
   Recorded in step 3 when its home is `doc/dual-agent-review.md`, and as a step-6 item otherwise.
8. **D8 — `py/tests/test_site_index_links.py:84`**: "34" to "35", one word. Yes or no. Executed in
   step 6.
9. **D9 — the rebuttal round's status. DECIDED, Ben, 2026-09-09, afternoon: the turn-taking
   round is the standard dual-agent review.** His words: "let's make this iterative (taking
   turns, argument, counter-argument, rebuttal, etc.) process the standard dual agent review
   process; I think it has worked well". `doc/dual-agent-review.md` still says adoption is
   undecided and names Design A as the default; step 3 rewrites it so that the standard review is
   the round this window ran — Claude argument; Codex counter-argument, with the reconciliation
   table appended to the argument; Claude rebuttal; Codex counter-rebuttal; further turns
   alternating as needed — each turn a tracked file the next task reads from its path and commit,
   which Ben supplies, ending when a turn accepts everything and lists no unresolved
   disagreement, which the other agent's next task reads and acknowledges (step 1 of this plan is
   the worked case). Every turn is review only, on public evidence, with no remediation and no
   edit to an earlier turn; a correction lives in the turn that accepts it. Design A becomes the
   default that held from 2026-09-07 to 2026-09-09 and Design B stays the blind alternative, both
   kept as descriptions. Recorded in step 3.
10. **D10 — the review files' naming and `State:` vocabulary** (finding 10): whether the `-sol`
    suffix is a convention to record; whether Codex files keep "completed <date>" beside the
    Claude files' "not yet acted on" and "acted on <date>"; whether the doc standard's glob
    `doc/review-findings-*.md` should match the Codex names; and, now that turns beyond the second
    are standard (D9), how turn files are named — this round put `-claude-rebuttal`,
    `-codex-counter-rebuttal` and `-claude-turn-5` after the Codex file's stem. Codex's
    reconciliation calls these policy questions. Recorded in step 3.
11. **D11 — a shared worktree for the whole round. DECIDED in substance, Ben, 2026-09-09,
    afternoon; the naming is proposed here for his yes or amendment.** This round's worktree,
    `C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08` on `codex-review-2026-09-08`,
    was created by Codex in turn 2 without instruction — Ben's recollection, borne out by the
    branch's reflog, which starts "Created from becc6f00" with the counter-argument `5636d38a`
    as its first commit — and every later turn of both agents and this close-out ran in it. Ben's
    judgment: "it turns out to have been a good idea, so let's record that as part of the
    standard dual-agent review plan", named so that "it is clear from path and/or branch alone
    that this is a *shared* worktree, not a worktree belonging to whatever agent created it",
    and created by Claude, "since, somewhat arbitrarily, the dual-agent review process starts
    with Claude". So the standard is: the Claude session that writes the argument creates the
    worktree and its branch at the round's start; every turn of both agents and the close-out
    use it directly; no task fast-forwards `main` or pushes; one integration at the end; then the
    worktree and branch are retired. Proposed naming, for D11's line in the template: branch
    `dual-agent-review-<date>` and worktree
    `C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-<date>` — the parent
    is where a Claude-made worktree goes, and the leaf and the branch say what it is. This
    round's worktree keeps its name; renaming a live worktree mid-round is churn for nothing.
    Recorded in step 3.

Template for the prompts of steps 3 and 4. Fill every line; "as proposed", "yes", "no" and
"leave" are answers:

```
D1:
D2:
D3:
D4:
D5:
D6:
D7:
D8:
D9: standing, decided 2026-09-09
D10:
D11: naming as proposed, or the branch and path to use
```

## Step 3 — Codex brings `doc/dual-agent-review.md` up to date

Actor: Codex, one task. Input: step 1's reported commit; D1, D7, D9, D10 and D11. Output:
`doc/dual-agent-review.md` edited and committed on the branch. This is the close-out's one
process-record change, kept apart from the remediation so that step 4's plan lists finding 10 and
C5 as done here rather than scheduling them twice.

Prompt to paste, with the required commit and the decisions filled in:

```
Bring doc/dual-agent-review.md up to date with the experimental rebuttal round's outcome and Ben's decisions.

Use this existing worktree directly:
C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08

Before reading, verify the checkout path, branch, HEAD, and working-tree status. The branch is codex-review-2026-09-08. The required commit is <required commit>. A newer HEAD must contain that commit as an ancestor. Inspect any mismatch before proceeding. Then merge main into the branch with git merge --no-edit main, resolving any conflict on the branch, before reading further.

Read applicable global instructions, repository CLAUDE.md, and the hebrew-prose skill with its references. Read doc/PLAN-close-out-review-2026-09-08.md; this task is its step 3 and follows its rules.

Ben's decisions, 2026-09-DD:
D1: <...>
D7: <...>
D9: standing, decided 2026-09-09 (the plan's step 2 has Ben's words and what the standard consists of)
D10: <...>
D11: <naming>

Do six things in doc/dual-agent-review.md, and nothing else:
1. Under "Experimental Claude rebuttal round (2026-09-09)", add a dated outcome paragraph: the five documents with their commits (the plan's state section lists them), the step-1 acknowledgment with its commit, the three disputes closed, the corrections each side accepted, and Ben's D9 decision stated as a decision with its date.
2. Replace the sentence saying Codex "will never load" the hebrew-prose skill with Ben's D1 wording, dated.
3. Correct the stale statements finding 10 of doc/review-findings-2026-09-08.md lists — the review census ("Eight such files exist ... the 2026-09-04 file has the first Codex counterpart"), the calibration section's coverage, and the backslash path — re-measuring each before writing: count doc/review-findings-*.md and doc/codex-review-findings-*.md at HEAD and read their State lines.
4. Record Ben's D10 decisions in the naming section, and Ben's D7 decision if its home is this file.
5. Make the turn-taking round the standard review, per D9: state it as the default where the document now names Design A as the default; describe the turns (Claude argument; Codex counter-argument, with the reconciliation table appended to the argument; Claude rebuttal; Codex counter-rebuttal; further alternating turns as needed), each turn a tracked file the next task reads from its path and commit, which Ben supplies; the stopping rule (a turn that accepts everything and lists no unresolved disagreement ends the round, and the other agent's next task reads it and records an acknowledgment or an objection); what a turn may do (review only, public evidence only, no remediation, no edit to an earlier turn, corrections in the accepting turn); and the close-out that follows (decisions, procedure record, remediation plan, remediation, one integration, retirement), citing this plan as the worked case. Keep Design A as the default that held from 2026-09-07 to 2026-09-09 and Design B as the blind alternative, both as descriptions, dated.
6. Record D11 as standing practice, with Ben's naming: the Claude session that writes the argument creates the shared worktree and branch at the round's start; every turn of both agents and the close-out use it directly; no task fast-forwards main or pushes; one integration at the end; then it is retired. Say that this round's worktree was created by Codex in turn 2 without instruction, that it worked, and that its path and branch read as Codex's, which the naming fixes.

What is not expected to change: the descriptions of Design A and Design B beyond their status, the blindness rule within Design B, the reconciliation rules of the two earlier designs, and any review record.

Commit only doc/dual-agent-review.md and this plan's execution line on codex-review-2026-09-08. Do not fast-forward main and do not push. Reply with the full file path, the commit ID, the branch head, and anything still unresolved.
```

## Step 4 — Codex writes the remediation plan for a fresh session

Actor: Codex, one task. Input: step 3's reported commit; D2–D8. Output:
`doc/PLAN-remediate-review-findings-2026-09-08.md`, committed on the branch. No page, code or
record changes in this task.

Prompt to paste, with the required commit and the decisions filled in:

```
Write doc/PLAN-remediate-review-findings-2026-09-08.md, the remediation plan for the 2026-09-08 review, for a fresh session to execute.

Use this existing worktree directly:
C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08

Before reading, verify the checkout path, branch, HEAD, and working-tree status. The branch is codex-review-2026-09-08. The required commit is <required commit>. A newer HEAD must contain that commit as an ancestor. Inspect any mismatch before proceeding. Then merge main into the branch with git merge --no-edit main, resolving any conflict on the branch, before reading further.

Read applicable global instructions, repository CLAUDE.md, and the hebrew-prose skill with its references. Read doc/PLAN-close-out-review-2026-09-08.md; this task is its step 4 and follows its rules. Read doc/PLAN-remediate-review-findings-2026-09-07.md for the shape to take: a State line at line 3, decision gates, waves, a per-wave execution record, the verification commands, and the commit discipline.

Ben's decisions, 2026-09-DD:
D2: <...>
D3: <...>
D4: <...>
D5: <...>
D6: <...>
D7: <...>
D8: <...>

Sources, in order of authority: the reconciliation table appended to doc/review-findings-2026-09-08.md at 5636d38a; the rebuttal (da4e40a5), the counter-rebuttal (ad5d9f43) and turn 5 (7c4416cd), which amend the table's dispositions; the step-1 acknowledgment; Ben's decisions above and at 3b0225e0 and becc6f00.

Every finding the table marks unfixed becomes a plan item with its finding number, the file and a searchable anchor, the line as measured at 38a606e2, the command that re-establishes it, the wave it belongs to, and what is not expected to change. Every finding already settled is listed as settled with the commit or decision that settled it: 1, 3 and 5.6 (3b0225e0, becc6f00); 10 and C5 (step 3's commit); 13.2 as a design note (D5), 13.5, 13.7, 14.1, 16's eight withdrawn sites and 17(b)-(e) (accepted in the rebuttal); and whatever D2-D8 close.

Apply Codex's process rule from doc/codex-review-findings-2026-09-08.md, "MAS decisions and the scope of future remediation", whatever D7 says about recording it: reproducible data and code defects go in waves that Ben's approval of the plan authorizes; every proposed change to the MAS pages' terminology, organization, interpretation or attribution is a separate item carrying its concrete wording, before and after, executed only after Ben approves that item in step 5. Rows 13 and 21 of doc/review-findings-2026-09-07.md and that plan's Wave 2 result want dated corrections, not reinstated prose; say so.

State each wave's regeneration commands (the real CLI commands), the suite baseline of 983 passed, 5 skipped, 65 subtests at becc6f00 with the instruction to re-measure, and each wave's preconditions: which files are expected to change and which are not.

Write no page, no code and no record change. Commit only the new plan and this plan's execution line on codex-review-2026-09-08. Do not fast-forward main and do not push. Reply with the full file path, the commit ID, the branch head, and anything still unresolved.
```

## Step 5 — Ben approves the remediation plan

Actor: Ben. Input: the plan from step 4. Output: an approval for each wave's code and data items,
and for each MAS wording item an approval, a rejection or an amended wording, pasted into the
step-6 prompt for that wave. The step-6 task records them in the plan as dated decisions before it
edits anything else, so the plan carries its approvals.

## Step 6 — Codex executes the remediation plan, one task per wave

Actor: Codex, one task per wave, in the plan's order. Input: the previous task's reported commit;
Ben's step-5 approvals for the wave. Output: the wave's commits, the wave's execution record in the
remediation plan, a dated row per settled finding under `## Dispositions after remediation` in
`doc/review-findings-2026-09-08.md` (the section `doc/dual-agent-review.md` prescribes); the final
wave's task also runs the integration procedure above, once for the whole close-out.

Prompt to paste, once per wave:

```
Execute wave <N> of doc/PLAN-remediate-review-findings-2026-09-08.md.

Use this existing worktree directly:
C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08

Before reading, verify the checkout path, branch, HEAD, and working-tree status. The branch is codex-review-2026-09-08. The required commit is <required commit>. A newer HEAD must contain that commit as an ancestor. Inspect any mismatch before proceeding. Then merge main into the branch with git merge --no-edit main, resolving any conflict on the branch, before reading further.

Read applicable global instructions, repository CLAUDE.md, and the hebrew-prose skill with its references. Read doc/PLAN-close-out-review-2026-09-08.md; this task is its step 6 for wave <N> and follows its rules. Read the remediation plan in full before editing.

Ben's approvals, 2026-09-DD: wave <N> approved. MAS items: <item: approved wording / rejected / amended to "...">.

Record the approvals in the remediation plan as dated decisions before editing anything else. Execute the wave's items in order. Regenerate tracked artifacts with the real commands and read the diff; an unexplained diff is a failure. Do not touch an item of another wave, an unapproved MAS item, or the text of any dated record except by a dated note beside it. After the wave: write its execution record in the remediation plan; add a dated row per settled finding under "## Dispositions after remediation" in doc/review-findings-2026-09-08.md; run black on any Python touched; run the suite. Commit as the remediation plan says. If this is the remediation plan's final wave, run the close-out plan's Integration section after the commit; otherwise do not fast-forward main and do not push. Reply with every file path, every commit ID, the branch head, main's head after the fast-forward if this was the final wave, and anything still unresolved.
```

## Step 7 — Ben retires the worktree and its branch

After the final step-6 task has integrated and ended, since a task cannot remove the worktree it
runs in:

```powershell
git -C C:/Users/BenDe/GitRepos/MAM-basics worktree remove C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08
```

```powershell
git -C C:/Users/BenDe/GitRepos/MAM-basics branch -d codex-review-2026-09-08
```

`branch -d`, never `-D`: it succeeds only when every commit is on `main`, which is the record that
nothing was lost. `worktree remove` refuses a worktree with untracked or modified files; the ignored
`.novc/review-2026-09-08/` does not count, and its turn-5 scripts have their copy under the primary
clone. If it refuses anyway, read `git -C <worktree> status --porcelain` before reaching for
`--force`.

## What this plan does not do

1. It decides nothing: D1–D11 and the step-5 approvals are Ben's; D9 and the substance of D11 are
   his decisions of 2026-09-09, recorded under step 2.
2. It remediates nothing: no page, code or record changes before step 6.
3. It uses Claude for nothing after step 0.
4. It touches `main` once, at the end of step 6; until then every commit is on the branch.
