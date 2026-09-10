# Plan: close out the 2026-09-08 review, every step on Codex — turn 5 handed off, Ben's decisions taken, the procedure recorded, the findings remediated, the worktree retired

State: live 2026-09-09; no step started; the starting state was re-measured the same afternoon
after `main` moved, the dated notes below supersede the table where they differ, and the design
was revised that afternoon on Ben's decision to keep the work on the branch until the end, and D9 and
the substance of D11 were decided the same afternoon (step 2).

Status updated 2026-09-09 after step 1: Ben closed the review exchange with the
skill-reading time left unknown. Step 1 is complete; step 2 is active. Ben's exact
decision is recorded below, beside step 1's earlier execution line.

Status updated 2026-09-09 after Ben's D11 naming approval: step 2 is complete.
All D1-D11 decisions are recorded under step 2; no later D-numbered entry exists
in this plan. Step 3 is next, with no decision still pending for its handoff.

Status updated 2026-09-09 after Step 5: steps 1-5 are complete. Ben approved all waves,
P1-P3, E1-E8 and N1-N9 as amended. Step 6, Wave 1, is next in a fresh task. Its V6 setup
and proof precede any remediation edit or back-merge. The technical unchanged-HTML condition
remains in force; the approved E items have a separate editorial phase after the technical
phase passes. See Step 5 and the remediation plan's dated approval record for the current
dispositions; earlier status entries remain historical.

Status updated 2026-09-09 after Wave 1B: Step 6 is active; Waves 1A and 1B are complete.
Wave 1C starts with the bounded evacuation-record and September 4 correction task described
in the remediation plan's Wave 1B execution record. Wave 1 remains incomplete. The V6 stop
and single integration after Wave 4 remain in force, including across intermediate archival.

Status updated 2026-09-09 after Wave 1C1: findings 5.1a/5.2 have dated corrections in the
evacuation records and September 4 review. Wave 1C2 is next for the September 7 historical
records, as bounded in the remediation plan. Wave 1 remains incomplete.

Status updated 2026-09-09 after Wave 1C2: findings 2, 3, 8.1 and 11.1–11.4 now have
dated September 7 record corrections, with their assigned 17f–17g completion qualifications.
Wave 1C3 handles the remaining MAS-plan and standards notes. Wave 1 remains incomplete.

Status updated 2026-09-10 after Wave 1D2: Step 6 remains active; Wave 1 is complete.
The September 8 review now reconciles every Wave 1 crosswalk row and settled decision.
Wave 2 is next and has not started. Waves 2-4 technical work and all E items remain
pending; P2 source/rights-holder identification remains deferred. This update supersedes
the earlier incomplete-Wave-1 status entries, which remain historical records.

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
   **Ordering clarification, 2026-09-09:** the Step-5 approval write-back is plan-only and
   does not back-merge. For Step 6, read the instructions and complete plans, then establish
   and prove the remediation plan's V6 gate before any remediation edit or back-merge.
   Run V6 before and after each merge. Its stop rule supersedes any instruction here to
   resolve, continue, commit completed remediation, or integrate after a real HTML difference.
4. **Never rewrite a dated record.** A correction to any review record or plan record is a dated
   note beside the text it corrects; the five documents of the round keep their text.
5. **Any Hebrew written into a file goes through `has_std_mark_order` before the commit**
   (repository `CLAUDE.md`, first section); Python touched means black on those files
   (`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m black <files>`); no
   `python -c`, no heredocs. A task that touches no Python says so.
6. **Report** the full path of every file written, every commit ID, the branch head, and anything
   unresolved. The report is the next step's input, and the branch head is the next step's
   required commit.

### Ben's phase-handoff instruction, 2026-09-09

Ben extended the instruction to suggest the next phase:

> In fact, not only suggest a next phase, but if it doesn't need my approval, just start the next phase!

After completing a phase, explain the next phase and start it in a fresh task when it is already
authorized and requires no new decision or approval. Step 3 therefore starts step 4 automatically
after committing the procedure update and its execution record. Step 4 writes the concrete
remediation plan and presents it for Ben's step-5 approval; it waits for that approval before
starting dependent step-6 work. Once Ben approves execution, hand off automatically between
authorized remediation waves unless a new decision is required. Carry this dated instruction into
every successor's prompt.

Before creating a successor, finish the phase's writes, commit its write-back locally, and verify
the exact checkout, branch head and clean working tree. Use `list_projects` and
`environment.type = local` for the saved project at
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`; create no additional worktree.
The successor prompt names that verified path, branch `codex-review-2026-09-08`, required source
commit, applicable decisions and phase scope. Verify the actual successor task and its checkout.
Transfer writing responsibility and stop editing after the successor starts.

This instruction supersedes the earlier handoff restriction against creating step 4 without
another request. The integration schedule remains unchanged: no intermediate fast-forward of
`main` or push, including at archival; integrate once after the final step-6 wave, verified in
the worktree first.

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

Executed 2026-09-09: commit `414a20f9`; D11 naming approved, all D1-D11
decisions recorded, and step 2 complete. The dated decisions below supersede
the earlier pending-status records.

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

### Ben's decisions, 2026-09-09: D1 and D2 approved

Ben approved both recommendations in the step-2 task on 2026-09-09:
"I approve of the recommendation for D1, and the recommendation for D2."

1. **D1 — approved replacement wording:**

   > Codex reads AGENTS.md and can load the hebrew-prose skill from ~/.agents/skills/. Codex does not automatically load ~/.claude/CLAUDE.md.

   This approved wording supersedes the longer D1 proposal quoted above. It corrects
   the skill-access claim and distinguishes skill loading from automatic loading of
   an instruction file. Implementation belongs to step 3.
2. **D2 — approved replacement wording:**

   > Plain ‘word’ survives for an ordinary English word, inside quoted or translated source material, and wherever the context already settles which sense is meant (references/terminology.md).

   The skill's opening rule will include the context exception already stated in
   `references/terminology.md`. Implementation and deployment belong to step 6.

Status after these approvals: step 2 remains active. D3–D8, D10, and D11's naming
remain pending; D9 and the substance of D11 retain Ben's earlier decisions. This
update records choices only; no skill or process document has been changed.

### Ben's decisions, 2026-09-09: D3 and D4 approved

Ben approved both recommendations in the step-2 task on 2026-09-09:
"Sure, I approve D3 and D4 as recommended."

1. **D3 — approved:** add a dated addendum to
   `doc/review-findings-2026-09-08.md` recording the corrections accepted in
   the later turns. Preserve the original findings and cite the review turns
   that accepted each correction. Implementation belongs to step 6.
2. **D4 — approved:** add dated notes recording that the Wave 4 command is
   unrecorded, so the cause of the missing subtest line remains unknown; the
   Wave 6 run at 981 tests reported 65 subtests. Also add a dated correction to
   the separate claim that the suite "no longer prints a subtest line."
   Implementation belongs to step 6.

Status after these approvals: step 2 remains active. D5–D8, D10, and D11's
naming remain pending; D9 and the substance of D11 retain Ben's earlier
decisions. This update records choices only; no review record has been changed.

### Ben's decisions, 2026-09-09: D5 and D6 approved

Ben approved D5 and D6 in the step-2 task on 2026-09-09:
"Yeah, I think the assert suffices; no need to record MAS multiplicity in the
JSON and derive the page sentence from the data. I approve D5 and D6 as
recommended."

1. **D5 — leave:** keep the MAS multiplicity assertions and the page sentence
   unchanged. Do not add a MAS multiplicity field to the JSON and do not derive
   the page sentence from such a field. The assertion remains the check that
   stops generation if a future corpus has a MAS chanted word with more than one
   post-stress meteg mark. Finding 13.2 remains a design note rather than a
   remediation item.
2. **D6 — approved clarification:** change `DATA-LICENSES.md`'s
   `aleppo/aleppo-wiki/` row to say "Ben Denckla's hand corrections." The
   clarification identifies whose corrections the row includes. Implementation
   belongs to step 6.

Status after these approvals: step 2 remains active. D7, D8, D10, and D11's
naming remain pending; D9 and the substance of D11 retain Ben's earlier
decisions. This update records choices only; no page, code, or license record
has been changed.

### Ben's decisions, 2026-09-09: D7 broadened and D8 approved

Ben approved D7 and D8 in the step-2 task on 2026-09-09, and broadened D7:
"I approve of D7 and D8 but I don't see why D7's language is limited to the MAS
pages. I would think the MAS pages would be given as an example, not given as
what seem to be the only case needing this protection."

1. **D7 — standing practice, with general scope:** for any remediation
   proposal, separate a reproducible data or code defect from a proposed
   editorial change to terminology, organization, interpretation, or
   attribution. Present each proposed editorial change with concrete wording
   for Ben's approval before applying it. Where Ben has already decided, record
   and follow that decision rather than asking again. Record this standing
   practice in `doc/dual-agent-review.md`. The September 8 MAS-page reversals
   are the worked example, not the scope boundary. Implementation belongs to
   step 3.
2. **D8 — approved:** change the stale descriptive count in
   `py/tests/test_site_index_links.py` from 34 to 35. Leave
   `_MIN_AUTHORED_ANCHORS = 25` unchanged; the edit changes no test behavior.
   Implementation belongs to step 6.

Status after these approvals: step 2 remains active. D10 and D11's naming
remain pending; D9 and the substance of D11 retain Ben's earlier decisions.
This update records choices only; no process document or test has been changed.

### Ben's decision, 2026-09-09: D10 approved

Ben approved D10 in the step-2 task on 2026-09-09: "I approve approve D10 as
recommended."

**D10 — approved:** record these four rules in `doc/dual-agent-review.md`:

1. The standard Codex file has no model suffix. Use a model suffix such as
   `-sol` only for an exceptional additional review whose purpose is to compare
   or repeat the same role with a named model. The existing `-sol` file is the
   worked example.
2. The initial `review-findings-<date>.md` file owns remediation state:
   `not yet acted on` or `acted on <date>`. Every later review turn uses
   `completed <date>; review only`. "Completed" says that the review turn is
   finished; "acted on" says that the findings were remediated.
3. The document standard recognizes the initial Claude files, the Codex
   counter-arguments, and the later dual-agent turns. Existing historical
   `State:` lines and filenames remain unchanged.
4. The first two filenames remain `review-findings-<date>.md` and
   `codex-review-findings-<date>.md`. Later turns use neutral, numbered names:
   `dual-agent-review-<date>-turn-03-claude.md`,
   `dual-agent-review-<date>-turn-04-codex.md`, and the corresponding name for
   each further turn. The neutral stem identifies the shared exchange; the
   number identifies its sequence without an indefinitely lengthening chain of
   rebuttal labels.

Implementation belongs to step 3. Status after this approval: step 2 remains
active, with only D11's naming pending among the D1–D11 entries currently in
this plan. D9 and the substance of D11 retain Ben's earlier decisions. This
update records a choice only; no process document has been changed.

### Ben's decision, 2026-09-09: D11 naming approved; step 2 complete

Ben approved the proposed branch and worktree naming on 2026-09-09:

> I approve of the proposed branch naming scheme and worktree naming scheme, namely dual-agent-review-\<date>.

**D11 — naming approved:** future dual-agent review rounds use branch
`dual-agent-review-<date>` and shared worktree
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-<date>`.
The branch and worktree folder have the same name. Claude creates the shared
worktree and branch at the round's start; every turn of both agents and the
close-out uses that checkout. No task fast-forwards `main` or pushes during the
exchange. The final remediation wave integrates once at the end; the worktree
and branch are retired after the final task ends. This is the D11 substance
Ben had already decided, now with the naming approved. Implementation belongs
to step 3.

The September 8 round keeps branch `codex-review-2026-09-08` and worktree
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`.

Step 2 is complete: D1-D8 and D10 retain the approvals recorded above, D9
retains Ben's standing-process decision, and D11 is approved in substance and
naming. Inspection of this plan on 2026-09-09 found only D1-D11; no D12 or later
entry exists. There are no remaining decision questions for the step-3 handoff.
The step-3 task takes the branch head reported with this decision record as
its required source commit and follows the dated approvals under step 2.
The earlier step-3 input line naming step 1's commit predates these approvals;
the completed step-2 record is the source for the handoff.

This update records decisions only. Earlier dated records are preserved. No
remediation, skill edit, or process-document edit has been performed in step 2.

## Step 3 — Codex brings `doc/dual-agent-review.md` up to date

Executed 2026-09-09: commit `2cddb89347d3cb32baaf4ac92e90c99a61f5b5fd`; step 3 complete.
D1, D7, D9, D10 and D11 are recorded in `doc/dual-agent-review.md`; finding 10 and C5 are
settled there. The review census was re-measured at `9ac147cc`: 10 initial Claude files and
7 Codex-prefixed files, all State lines read. The existing public-tree Hebrew mark-order lint
passed (1 test), `git diff --check` passed, and Design B's blindness rule and both earlier
designs' reconciliation text are unchanged. No tracked Python, generated artifact or review
record changed. The same commit records Ben's phase-handoff instruction above. Step 4 is next
in a fresh task using the same clean worktree and the branch head reported with this execution
record; Ben's step-5 approval is required before dependent remediation. No fast-forward of
`main` or push was performed.

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

Executed 2026-09-09: wrote `doc/PLAN-remediate-review-findings-2026-09-08.md`
after verifying required commit `83b470da1846fc1c739fcca48762d01627fa354e` and
merging `main` into the review branch at `dd86c96fd29c4b345ae37ba7252ffe72944cbef3`.
The plan covers every reconciled finding, retains Ben's settled decisions, and
separates four implementation waves from exact editorial proposals under D7's
general scope. The merged-tree suite passed: 987 passed, 5 skipped, 65 subtests
in 126.54 seconds. Planning changed only the new plan and this dated entry;
no remediation, primary fast-forward, or push occurred. Step 4 is complete and
step 5 awaits Ben's approval. The planning commit is recorded in the follow-up
execution entry after the commit exists.

Execution commit recorded 2026-09-09: `154921c9` contains the remediation plan
and the preceding step-4 entry. Plan links, referenced paths, Markdown tables,
and changed-line whitespace checks passed. The existing prose mark-order lint
passed after staging the planning documents (1 passed, 991 deselected).
No tracked Python file changed. Step 5 is the required next phase: Ben approves
or amends the waves and P1-P3 proposals, with separate dispositions for E1-E8
and N1-N9. No step-6 task has been started.

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

Approval received 2026-09-09, after the remediation plan's update at `961554d4`:
Ben answered the original question, "Do you approve the waves and P1-P3
recommendations, including the exact editorial proposals E1-E8 and N1-N9?",
with "I can now say yes", and requested Step 5 in a fresh task because the
planning task had accumulated too much context. E2 includes Ben's previously
recorded coalesced slash-span amendment. The fresh task records the approval
and prepares execution from the updated plan; the planning task performs no
remediation. Preserve the technical phase's unchanged-HTML condition and V6,
including the mandatory stop and renewed-approval requirement on a difference.
Record the approved HTML editorial work as a separate phase, with its exact
intended differences and output contract addressed before that phase begins.
The approval is not a waiver of the technical stop condition.

**Step 5 completed 2026-09-09:** the fresh task verified clean source commit
`e2693d9a3fbd43981f81c70e21ef6ec66ba41d4c` in the named review worktree and recorded Ben's
approval consistently in `doc/PLAN-remediate-review-findings-2026-09-08.md`, under
"Step-5 approval record and next execution phase". Wave 1, Wave 2, Wave 3, Wave 4,
P1-P3, E1-E8, and N1-N9 are approved as amended. E2 uses a coalesced italic
`meteg/merkha` span, including the slash. No listed proposal needs approval again.

The technical phase keeps the fixed `c2f238f2c253d7b00b2d22dc262fe95c81a82401` HTML baseline
and full V6 stop contract. The remediation plan identifies the exact intended E2/E3/E8
differences and the output-contract preparation required before the separate editorial phase.
The editorial output contract must be resolved and recorded before those HTML edits; a
genuinely unresolved contract revision goes to Ben as a specific decision, without reopening
the item approvals. No decision blocks Wave 1's handoff.

The Step-5 task changes only these plans and commits locally. It performs no remediation,
generator run, V6 implementation, back-merge, integration, or push. After verification and a
clean local commit, start Step 6, Wave 1, automatically under Ben's phase-handoff instruction.
The successor uses the same worktree directly and establishes V6 before touching remediation.
No intermediate archival changes the final-wave integration schedule.

Verification recorded 2026-09-09: only the close-out and remediation plans changed.
`git diff --check` passed. The existing prose mark-order lint passed with
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -B py/main_test.py py/tests/test_prose_mark_order.py -q -p no:cacheprovider`
(1 passed). No tracked Python changed, so black was not required. No full suite or product
generation was run for this planning-only update. The execution commit is recorded below
after the commit exists.

Executed 2026-09-09: commit `10458a3eed434ee8f4556e3f7e3fea3169afdeaa` records the
Step-5 approval and Wave 1 handoff requirements in both plans. The following record commit
adds this hash without amending the approval commit. The successor's required source is
the clean branch head reported after this record commit, containing `10458a3e` as an ancestor.

Actor: Ben. Input: the plan from step 4. Output: an approval for each wave's code and data items,
and for each MAS wording item an approval, a rejection or an amended wording, pasted into the
step-6 prompt for that wave. The step-6 task records them in the plan as dated decisions before it
edits anything else, so the plan carries its approvals.

## Step 6 — Codex executes the remediation plan, one task per wave

Execution-size update, 2026-09-09: Ben asked that remediation tasks be sized to avoid
compaction, and certainly multiple compactions. Wave 1's preparation had already compacted.
The remediation plan's "Smaller execution tasks, recorded 2026-09-09" now divides Wave 1
into bounded tasks and defines scoped source reading. That execution structure supersedes
the one-task-per-wave wording below. Approvals, wave order, the V6 stop, automatic clean
phase handoff, and the single integration after Wave 4 remain in force. Intermediate task
archival does not trigger integration.

Wave 1A completed 2026-09-09: Codex established and proved the V6 gate before remediation,
back-merged `main` at `bd5d9e56fdafb47617c38ce98bc9c98d8337448f`, rechecked V6, and applied
D2's exact shared-skill opening sentence to all three homes. Both whole-directory comparisons
and an independent byte inventory passed. The worktree suite passed with 987 tests, 5 skips,
and 65 subtests in 110.21 seconds; V6 passed again with zero changed HTML locations.
The remediation plan's Wave 1A execution record identifies the scripts, hashes, and evidence.
The remaining Wave 1 work starts with Wave 1B's current documentation and crop inventory.
The implementation and record commit hashes will be recorded after creation. Wave 1 is
not complete; no integration, push, or automatic archival occurred.

Wave 1A implementation commit recorded 2026-09-09: `d5616b8f`. The subsequent record-only
commit provides the clean required source for the automatically created Wave 1B task.
The successor uses the same saved worktree directly. The original task stops editing after
handoff and remains available for Ben to archive; that archival does not trigger integration.

Wave 1B completed 2026-09-09 by Codex task `01a0892f-1dac-7811-9662-8554324cbafc` in
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`, branch
`codex-review-2026-09-08`, starting clean at `85dcf63dc1a0aef83cca8cedbacc95365743f6f9`.
The required back-merge reported `Already up to date.` V6 passed before and immediately after
the merge, then after the suite: nine checkout and nine fresh-render pages, zero changed
locations, unchanged pinned survey JSON. The existing gate and baseline were inspected and
preserved. The remediation plan's Wave 1B record gives the evidence paths and exact commands.

Wave 1B applied the approved current-documentation fragments, eleven/nine page counts,
35-anchor comment with floor 25 unchanged, corrected MAM-with-doc inventory, Ben Denckla
attribution, and dated maintenance-scope correction. P2 now has an individual six-crop
inventory linked from DATA-LICENSES; source and rights-holder identification remains deferred,
and no grant changed. Black left all six touched Python files unchanged; the canonical suite
passed **987 tests, 5 skips, and 65 subtests in 108.36 seconds**. Only completed Wave 1B
findings received disposition rows. No generated artifact, test behavior, or sibling checkout
changed; no integration, push, or archival occurred.

Wave 1 is not complete. The next task is Wave 1C1 on the same saved project with
`environment.type = local`, for findings 5.1a/5.2 in the evacuation records and September 4
review. The remaining historical corrections stay for subsequent Wave 1C work; Wave 1D owns
the accepted-corrections append and complete reconciliation. The implementation hash and
final checkpoint verification are recorded in a following local record commit. Creation of
the successor waits for that clean checkpoint; the predecessor stops editing after dispatch.

Executed 2026-09-09: Wave 1B implementation commit
`42520d05ad004e99c0fff68bcf634a763ad22b15`. The worktree was clean after that commit. Final
scope and prose-lint checks passed; V6 passed before the implementation commit and again at
`42520d05` before the record-only checkpoint, with zero changed locations. The remediation
plan records the evidence directories. The record-only commit supplies the clean required
source for Wave 1C1's automatic handoff; no integration or push is due at this checkpoint.

Wave 1C1 completed 2026-09-09 by Codex task `01a08940-ef16-7b02-b00b-a99f8e9048c7`,
using the saved project directly at
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`, branch
`codex-review-2026-09-08`. The verified source was clean at
`d4dacdbaea8f57cd23012840fa9a0a30e378a950`; the back-merge reported `Already up to date.`
The unchanged V6 gate passed before and immediately after the merge. Its fixed HTML and
survey baseline remains `c2f238f2`; no real approval stop occurred.

The approved dated notes now cover D4's no-subtest-line correction, the historical
directory observation, six numbered branch names and tips from the retained September 7
deletion-output record, `4195440e`'s removed constant, the landed sparse instructions,
`19df42f3`'s workspace/visibility removal, `9cf48863`'s recorded clone retirement, and both
omitted MAM-with-doc host dotfiles. No original historical line was rewritten, no tracked
Python changed, and no cleanup, evacuation, generated-artifact edit, or sibling write ran.
The remediation plan's Wave 1C1 record gives the historical evidence and verification paths.
Only completed 5.1a/5.2 work received September 8 disposition rows.

The canonical worktree suite, with `REPOS_ROOT=C:/Users/BenDe/GitRepos`, passed
**987 tests, 5 skips, and 65 subtests in 106.01 seconds**. V6 passed immediately afterward
for all nine checkout and nine freshly rendered pages, with zero changed locations and
unchanged survey JSON. The full output and gate evidence are recorded in the remediation
plan. No tracked Python changed, so no black invocation was needed.

Wave 1C2 next handles the September 7 historical records for findings 2, 3, 8.1, and
11.1–11.4, including the Sol review's count correction and the related 17f–17g completion
qualifications. MAS-plan notes, N8, the standards census, and remaining record-only
dispositions stay for later Wave 1 work; Wave 1D still owns the complete accepted-corrections
append and reconciliation. The next task is authorized after the clean committed checkpoint,
using the same saved project with `environment.type = local`. The predecessor stops editing
after dispatch. Integration and push still occur only after final Wave 4.

Executed 2026-09-09: Wave 1C1 implementation commit
`9241107ba5c3438a8b51c3032bfdce0bd7b4d070`. The worktree was clean after the commit.
Final scope verification passed, and V6 passed before implementation and again at that
commit before this record-only checkpoint, always with zero changed locations. The
remediation plan gives the exact evidence paths. The following record commit supplies
the required clean source for Wave 1C2; no integration or push is due.

Wave 1C2 executed 2026-09-09 by Codex task `01a08953-8231-70f1-859c-663cb8c29a72`
directly in `C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`, branch
`codex-review-2026-09-08`, from clean source
`8d6c4df8bac66367aa4519b633cf450a558b27c8`. The back-merge was already up to date.
The inspected V6 gate passed before and immediately after the merge against the fixed
`c2f238f2` baseline; no real approval stop occurred.

Dated notes in the September 7 review, remediation plan, and Sol review now distinguish
the continuing 210 whitespace findings in 193 files, retained model fixes, Ben's
editorial reversals, accepted local glosses, settled BHS/edition questions, ordinary
368/370 versus combined 370/372 scope, the unrecorded Wave 4 invocation and unknown
missing-line cause, completed implementations behind unchecked boxes, 25 formatted
sources plus one copied Python file, and the spell check's tracked frequency outputs.
Only the corresponding 17f–17g completion qualifications and completed September 8
disposition rows were added. Original records and checkboxes remain intact.

The remediation plan's Wave 1C2 record names the bounded measurement reports and exact
public Phonetic MAM source commit. No tracked Python, generated artifact, license grant,
behavior, or sibling checkout changed; no spell checker, survey, maintenance, or cleanup
ran. Suite, final V6, and local commit evidence follow after verification.

Verification completed 2026-09-09: the canonical worktree suite, with
`REPOS_ROOT=C:/Users/BenDe/GitRepos`, reported **987 passed, 5 skipped, and 65 subtests
passed in 107.46 seconds**. V6 passed immediately afterward for all nine checkout
pages and all nine fresh-render pages, with zero changed locations and unchanged
survey JSON. The scope check confirms all original lines are preserved in the six
authorized Markdown files, valid Hebrew mark order and diff whitespace, and identical
frozen/current whitespace finding sets. No tracked Python changed, so black was not
needed. The remediation plan names the exact evidence files; local commit evidence follows.

Wave 1C3 next handles the named MAS plans, merge-plan State/N8 notes, and standards
docstring census under the remediation plan's precise boundary. Wave 1D still owns
remaining record-only dispositions, the accepted-corrections append and full
reconciliation. The successor starts automatically after the clean committed checkpoint,
using the same saved project directly with `environment.type = local`; writing
responsibility transfers at dispatch. Integration and push occur once after final Wave 4.

Executed 2026-09-09: Wave 1C2 implementation commit
`4cc94bef9251b4677c7ea918875c913e17ca5c31`. The worktree was clean afterward.
All original lines in the six authorized Markdown files passed preservation checks;
V6 passed before implementation and at that commit before this record-only checkpoint.
The remediation plan names all five passing V6 runs and the final scope report.
The following record commit supplies the clean source for Wave 1C3's automatic handoff
on the same saved project. No integration or push is due at this checkpoint.

Wave 1C3 executed 2026-09-09 by Codex task `01a08967-0bc1-7f01-b9e0-2776b5403ef2`
directly in `C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08`, branch
`codex-review-2026-09-08`, from clean source `1b86afa85af9566032eb839d941bac057121da99`.
The required back-merge was already up to date. The inspected V6 gate passed before
and immediately after the merge against the fixed `c2f238f2` baseline, with zero
changed locations and unchanged survey JSON. No real approval stop occurred.

The assigned MAS plans now have dated notes for the chosen post-silluq interpretation,
the ninth-page arrival, matching lines versus occurrences, original proposal attribution,
and historical suite baselines. The merge plan has the approved executed State and exact
N8 notes. Existing census, State, dated-decision, and 32-hunk/13-file corrections were
retained; the merge-message discrepancy is recorded without amendment. The standards
docstring has the dated historical census correction and D10 procedure pointer, with
behavior unchanged. Only completed findings received disposition rows. Black left the
sole touched Python file unchanged. The remediation plan records bounded measurements;
suite, final V6 and commit evidence follow after verification.

Wave 1D next owns the remaining record-only dispositions, complete September 8
accepted-corrections append, and full Wave 1 reconciliation. Its exact boundary is in
the remediation plan's Wave 1C3 record. Wave 1 is incomplete; Wave 2 and the E items
remain pending. After the clean committed checkpoint, the authorized successor uses
the same saved project directly with `environment.type = local`; writing responsibility
transfers at dispatch. Integration and push occur once after final Wave 4.

Wave 1C3 verification completed 2026-09-09: the canonical worktree suite, with
`REPOS_ROOT=C:/Users/BenDe/GitRepos`, reported **987 passed, 5 skipped, and 65
subtests passed in 103.43 seconds**. V6 passed immediately afterward with zero
changed locations for the nine checkout and nine fresh-render pages and unchanged
survey JSON. The seven-file scope check confirms preservation of original dated
records, unchanged standards behavior, sixteen line-3 State entries, valid Hebrew
mark order, clean diff whitespace, and both skill comparisons empty. No new test,
generated artifact, or sibling file changed. The remediation plan names the exact
scripts and reports; local commit evidence follows.

Executed 2026-09-09: Wave 1C3 implementation commit
`26cf55dd354ae2afdeaa8ef352a94278d2372eab`. The worktree was clean afterward.
The remediation plan names the final scope report and passing pre-commit V6 evidence.
V6 passed again at `26cf55dd` before the record commit. All five actual Wave 1C3
gate runs passed with zero changed locations; the remediation plan gives the paths.
The following record-only checkpoint supplies the required clean source for Wave 1D,
on the same saved project. No integration or push is due at this checkpoint.

Wave 1D1 execution, 2026-09-10: Codex task `01a08977-c847-7f41-887f-7b1891162ef1`
verified the exact review worktree and `codex-review-2026-09-08`, clean at required source
`0ee34bea8ac36f058543d7f757c97f66e6b562cd`. The required back-merge was already up to date.
The inspected V6 gate passed before and immediately after the merge against fixed baseline
`c2f238f2`, with zero changed locations and unchanged pinned survey JSON. No real stop occurred.

The approved split into Wave 1D1/1D2 keeps each task bounded. Wave 1D1 writes the complete
accepted-corrections append under D3, preserves the original dated text and disposition rows,
and adds the review's current State above its historical State. The append includes the exact
eight finding-16 withdrawals and D3's three-sentence/two-table correction. D6 and N8 remain
completed individual corrections, with the blanket cleanup rejected. Only the September 8
review and both plans change. No tracked Python or generated artifact changes.

Wave 1D2 next owns the remaining record-only dispositions and full crosswalk reconciliation,
as precisely bounded in the remediation plan's Wave 1D1 record. Wave 1 remains incomplete.
Waves 2-4 technical findings and all E items remain pending; P2's source/rights-holder
identification remains deferred. After the verified clean local checkpoint, create the
authorized successor on the same saved project with `environment.type = local`, verify
its actual ID and checkout, and stop editing at dispatch. Integration and push occur once,
after final Wave 4. Verification and local commit evidence follow.

Wave 1D1 verification completed 2026-09-10: the canonical suite with
`REPOS_ROOT=C:/Users/BenDe/GitRepos` reported **987 passed, 5 skipped, and 65 subtests
passed in 108.80 seconds**. V6 passed immediately afterward with zero changed locations,
unchanged page membership and pinned survey JSON. The scope check confirms only the
three authorized record paths changed, the original historical lines remain, the eight
withdrawals match the rebuttal verbatim, Hebrew mark order and diff whitespace pass,
and both whole-skill comparisons are empty. No tracked Python changed; no new tests were
added. The remediation plan records the exact script, command and evidence paths.

Executed 2026-09-10: Wave 1D1 implementation commit
`b829a6aaf45d3b92e594da462f0012241c5aece6`; the worktree was clean afterward.
The remediation plan records the final scope report and passing pre-commit V6 evidence.
The following record-only commit supplies Wave 1D2's clean source in the verified saved
project. Wave 1 remains incomplete; full reconciliation is Wave 1D2's responsibility.
No integration, push, or automatic archival occurred.

V6 passed again at `b829a6aa` before the record commit; the remediation plan records
the exact evidence path. Every actual Wave 1D1 V6 run passed with zero changed locations
and unchanged survey JSON. No real stop occurred.

Wave 1D2 reconciliation completed 2026-09-10 by Codex task
`01a08987-8ee2-7372-9104-7cfb7f224d5a`, directly in
`C:/Users/BenDe/.codex/worktrees/MAM-basics-review-2026-09-08` on
`codex-review-2026-09-08`, clean at required source
`f60aa4260c24cfff726c590613abd72b88fdfd4d`, containing `b829a6aa`.
The required back-merge was already up to date. V6 passed before and immediately after
the merge against fixed baseline `c2f238f2`, with zero changed locations and unchanged
survey JSON. The original gate hash and failure-propagation proof remain valid.

The remaining record-only dispositions and complete crosswalk reconciliation are in
`doc/review-findings-2026-09-08.md`. Wave 1D1's complete accepted-corrections section and
all earlier disposition rows remain unchanged. The complete named XML target check
reproduces valid empty outputs and confirms unchanged inputs; it does not establish
independent language/edition claims or the reviewer's 415/416 scratch count. The
remediation plan names the bounded evidence and every completed/remaining boundary.
Only the September 8 review and these two plans change; no tracked Python or generated
artifact changes. No new test is added.

Wave 1 is complete. The next authorized fresh task is Wave 2 for whitespace outputs,
Holman RTL and existing MAS lint membership coverage, under its V2/V3/V6 output
contract. Wave 2 has not started. Its source is the verified clean local checkpoint
reported at handoff, using saved project `51e16ebd-373a-41f7-833e-9def3ef72b81` with
`environment.type = local`. Verify the actual successor ID and exact checkout; stop
editing when writing responsibility transfers. All E items remain for the separate
editorial phase after Wave 3 technical verification. P2 source/rights-holder
identification stays deferred. No integration, push or automatic archival occurs here;
the single integration remains scheduled after final Wave 4.

Wave 1D2 verification completed 2026-09-10: the canonical suite with
`REPOS_ROOT=C:/Users/BenDe/GitRepos` passed **987 tests, 5 skips, and 65 subtests in
102.78 seconds**. V6 passed immediately afterward with zero changed locations and
unchanged survey JSON. The independent Wave 1D2 scope check matches all 52 crosswalk
rows, preserves the historical records and entire accepted-corrections section, and
passes Hebrew mark order, diff whitespace and both whole-skill comparisons. Only the
three authorized Markdown files changed. The remediation plan records the exact
commands and evidence paths; local commit evidence follows after creation.

Executed 2026-09-10: Wave 1D2 implementation commit
`f7360667f2cd00ea5453757c81921b31b4b2d859`; the worktree was clean afterward.
The remediation plan gives the final implementation scope and passing pre-commit V6
evidence. The following record-only commit supplies Wave 2's clean required source in
the verified saved project. Wave 1 is complete. The exact handoff head and actual successor
ID are reported at dispatch; no integration, push or automatic archival occurred.

V6 passed again at `f7360667` before the record commit. The remediation plan names
that evidence and the passing record-scope report. Every actual Wave 1D2 V6 check
passed with zero changed locations and unchanged survey JSON; no real stop occurred.

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

Before reading, verify the checkout path, branch, HEAD, and working-tree status. The branch is codex-review-2026-09-08. The required commit is <required commit>. A newer HEAD must contain that commit as an ancestor. Inspect any mismatch before proceeding.

Read applicable global instructions, repository CLAUDE.md, and the hebrew-prose skill with its references. Read doc/PLAN-close-out-review-2026-09-08.md; this task is its step 6 for wave <N> and follows its rules. Read the remediation plan in full before editing. Establish and prove its V6 gate before any remediation edit or back-merge, then run V6 before and after git merge --no-edit main in the worktree. A real MAS HTML difference stops the entire process for Ben's renewed explicit decision; read-only diagnosis is allowed, but do not fix forward or continue another wave. Failed or incomplete checks also block progress.

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
