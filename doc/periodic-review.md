# Periodic review: one repository, one endpoint diff, one responsible reviewer

State: live; revised 2026-11-06

[review-trial.md](review-trial.md) controls current triage, routine repair authority, focused
verification, hourly screening and nightly broad checks. Its compact maintained run notes are
the normal record. This document keeps the ordinary review rules that also apply when Ben asks
for a separate dated review. It creates no schedule or additional approval gate.

## Scope and evidence

A review covers one repository and the single diff between its recorded start and end commits.
Carry forward that repository's reviewed-through anchor, rather than selecting commits by date.
History can help explain the endpoint diff; an intermediate change undone before the endpoint
is not itself a defect in that diff. A separately requested window leaves the ongoing series'
anchor unchanged unless it supplies the missing coverage. Each repository keeps its own anchors.

Use a verified checkout in a forest the running agent owns. Leave interactive work untouched,
keep one writer per checkout and run generators and checks sequentially. A full clone is the
default; a linked worktree uses its home clone's corresponding environment. Follow
`doc/clone-forests.md`, the shared `linked-worktrees` skill and the repository's `AGENTS.md`.

Concentrate on consequential, evidenced defects. Distinguish what the endpoint change introduced
from an older defect. Read the actual source and applicable instructions at the measured commit;
label later evidence as later evidence. Check a technical uncertainty by targeted investigation
or independent checking. Reproduce a disputed claim before adopting it. A passing generator or
preservation check shows consistency with inputs, not editorial correctness.

Name the repository, endpoint commits, checkout, commands actually run, result and material
limitations. Record enough evidence to assess each consequential finding without depending on
ignored scratch, a cache or an agent transcript. A figure names its population and method;
support a recurring defect with its actual affected sites. Report blocked, interrupted or
unexecuted checks honestly. An unexplained generated diff is evidence to investigate, not
something to restore silently. Keep the amount of checking and recording proportionate to
the defect, under the focused and nightly policy in `review-trial.md`.

## Public and private boundaries

MAM-basics' review records cover its public tree and read no private repository as review
material. `in/repo_maintenance_policy.json` declares visibility; private repositories outside
the roster remain private too. A check whose maintained code reads a private sibling may run,
but a public record gives only its allowed result and input commit ID. Private source paths,
findings, logs and other content stay private. The report-destination guard cannot inspect
what an agent later types into prose or a commit message.

MAM-private follows the same ordinary review and testing policy with its own instructions,
commands, environments, anchors and records. Read its `AGENTS.md` before the first check.
A private review may consult public evidence about a private change, but does not thereby
review that public repository's window. Every private review record stays in MAM-private.

## Review filenames and State lines

For a separately requested dated review, keep the established author-based filenames:
`doc/review-findings-<date>.md` for the Claude series and
`doc/codex-review-findings-<date>.md` for a Codex report. Name the author, model, effort level,
scope and endpoint commits in the opening. The requested review effort remains `max` for
Claude and `xhigh` for Codex (Ben, 2026-09-30).

Put `State:` on line 3 under the H1. The initial report records what was true when it finished,
for example `State: not yet acted on`; a report limited to review can use
`State: completed <date>; review only`. Historical names and State declarations stay as written.
Later remediation State and dispositions belong in the report's single live update file.
Use the shared `iterative-document-editing` skill's “Finished receipts and maintained documents”
for corrections, the line-four update pointer and retirement-family treatment. Maintained run
notes under `review-trial.md` stay true in place.

A review gets no thin tracking issue. File a substantive issue for a consequential confirmed
defect without a credible repair, or use an exception PR for a prepared repair that remains
uncertain, as `review-trial.md` directs. Use the shared `github-issues` skill. A review record
does not authorize policy, interpretation, data-semantic, licensing or publication changes.

## Close-out: from findings to dispositions

Triage each consequential finding under `review-trial.md`: repair within routine authority,
reject with reasons, defer explicitly, or name its issue or PR. Call a repair fixed only after
checking the decisive evidence. Routine work needs neither Ben's per-finding decisions nor
a separately approved remediation plan. Do not reopen settled decisions or a dismissed backlog
without new evidence. Explain genuine policy choices and concrete proposed wording to Ben.

### Private follow-up after completed remediation

Keep MAM-private's recorded unfinished work and approved deferrals in its maintained
`doc/review-follow-up.md`. Preserve the substantive disposition, source and searchable passage,
and the decision or condition needed to revisit it. Recording does not authorize implementation
or reopen a settled decision; do not collect unrequested ideas. The contents remain private.

Reuse the register's single thin pointer issue, following `github-issues`; push the register to
main before linking it. Keep that issue open while the register alone holds unresolved work.
Close it only after every entry is resolved, dismissed or moved to named separately tracked work;
reopen that same issue if later close-out adds unresolved work. Subsequent reviews need not
re-triage the unchanged backlog. This rule creates no reminder or automation.

### Present remediation by public-facing risk

When Ben's decision is needed, present reader-facing documents and exact proposed wording
first, then public data and affected values or structure, then a concise summary of other
changes. Classify generator edits by their effect on published documents and data. An ordinary
internal plan or review record does not become reader-facing merely because its Git repository
is public. Product reach and difficulty of undoing an act remain separate considerations.

When Ben requests a walk-through, identify the finding before discussing its disposition and
distinguish correcting the report's wording from repairing the underlying problem. Summarize
wording changes and give detail when useful. Put questions at the end of that presentation;
follow existing authorization and decisions without asking again.
