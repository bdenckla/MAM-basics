# Review and testing process

State: live; revised 2026-10-16

Ben approved the proposed process on 2026-10-07: "I approve; let's try this new process."
This process controls MAM-basics, MAM-private and occasional hbofonts review and repair work.
It supersedes the older obligatory Ben dispositions, fresh remediation-plan approval, D7's
approval gate for routine internal editorial repairs, blanket finding rechecks, and ordinary
pre-push/full-suite gates. Keep historical evidence, focused regeneration obligations and the
privacy, product, environment and one-writer safeguards. It changes no permissions or releases.

## Agent triage and repairs

One responsible agent reviews each repository's endpoint diff from its adopted/reviewed anchor
to a frozen main commit. Concentrate on consequential, evidenced defects. Reject unsupported
claims with reasons and leave harmless polish alone. No retrospective giant backlog is opened.
An anchor adopted at setup is a starting boundary, not a claim that the old tree was reviewed.

Routine authority covers an objective defect supported by a reproduction or independent check,
with a narrow repair under an existing policy. The agent may perform ordinary private/local
maintenance and integrate and push routine repairs to main with focused verification. Ben's own
direct-to-main workflow continues. This authority excludes new Hebrew interpretation, data
semantics, licensing/publication policy, permissions, destructive operations and new external
publishing actions. Existing main publication can occur before nightly detection.

Check technical uncertainty through targeted investigation or independent review before asking
Ben. A prepared repair that remains uncertain or consequential goes in a draft PR naming the
defect, minimal change, evidence, product effects and exact unresolved question. A genuine policy
choice still needs Ben's decision; a PR does not supply it. Use an issue for a consequential
confirmed defect without a credible repair, following the repository's issue-routing rules.
Do not reopen settled decisions without new evidence or create cleanup work from speculative nits.

## Focused work and nightly checks

Ordinary changes receive focused checks matched to the changed surface, including formatting
and relevant regeneration/comparison. Full mega and suite checks are the nightly default using
each repository's maintained broad-check commands; do not invent a suite where none exists.
Run broad checks immediately only when a specific consequence cannot accept the delay. State
that consequence; touching Python or reaching a product alone does not establish the exception.
Plans and handoffs add no blanket checks or mandatory per-item proof ceremony.

Use the saved portable cloud forest for portable nightly checks when its actual credentials,
committed inputs and environments have been verified; reserve HP for Windows-specific checks.
An offline personal computer must not be a prerequisite for portable testing. An enabled
schedule or saved configuration is not execution evidence: record blockers honestly when no
working runner is available, without advancing unexecuted checks or anchors.

At each nightly run, fetch main and record exact repository and required input commits. Use
isolated checkouts, leaving interactive edits untouched. Since Ben's decision of 2026-10-20
(`doc/clone-forests.md`, “Forest ownership”), such a checkout is in a forest the running agent
owns: by default a full clone that no interactive session is using, with its own environments,
otherwise a linked worktree there with its home clone's environments.
Review only new endpoint diffs; run MAM-basics and MAM-private's broad checks nightly. Check
hbofonts for incoming commits and run its broad checks when its tip changed. Its maintained
command includes its checks. Keep missing checks and unavailable environments explicit.
When a run uses another repository as input, select and record its committed checkout too.

Run generators and checks sequentially within a checkout. A failing check or unexplained output
diff goes through agent triage; do not silently restore evidence or label the run passing.
Do not commit generated changes merely because a generator produced them. Repair only within
routine authority, recheck the decisive evidence, and record any resulting repair commit separately
from the commit originally checked. Expected focused regeneration and its existing exemptions
remain in force. A successful run is quiet; bring Ben only a consequential unresolved question.

Product reach and difficulty of undoing an act are separate considerations. Use declared product
scopes, including generator effects, without turning every edit into a high-risk exception.
Later detection accepts some regressions on main until the nightly run and provides no promise
of pre-publication protection. Private source paths, findings, logs, commit anchors and reports
stay in the private repository; public checks record only allowed results and input commit IDs.

Ben's separate Claude sessions own the near-Aleppo sealing simplification and the lighter
Wikisource-update process. Follow their resulting maintained update rules. Source refreshes or
mpplus hash movement alone are not defects or approval gates; triage actual failures and
unexplained output changes without automatically rolling back new source data. Preserve
maintained source integrity checks for concrete corruption. Do not preserve or reintroduce
retired hash/sealing/replay gates. Use the resulting maintained commands and proportionate
confidence evidence rather than replacement process machinery. No review relay is introduced.

## Anchors and compact receipts

Keep one small maintained run note per repository; this repository uses
[review-trial-status.md](review-trial-status.md). Record the adopted baseline, reviewed-through
commit, last tested commit/result, and one short outcome per run or repair with evidence links.
Keep commands, failures and limitations only as detailed as needed to assess the result; link
existing receipts instead of copying them or dumping routine logs. Check factual integrity,
not arbitrary receipt-link positions.
Advance reviewed-through only after examining the diff and disposing of consequential findings;
it does not mean every finding is fixed. Advance last tested only for checks actually completed,
recording failures and incomplete runs accurately. A repair is fixed only on decisive evidence,
not merely on a passing preservation check. Commits may carry the detailed evidence.

Routine work needs neither Ben's per-finding decisions nor a separate approved remediation plan.
One concise disposition per repair, rejection, deferral or PR/issue is enough. Existing finished
receipts remain immutable with their single update; change State when the phase changes without
repeating it in every entry. Trial setup/receipt changes are evidence unless they expose a
consequential defect; ordinary code and data repairs remain reviewable window content.

## Trial assessment and scheduling

The approved trial scheduled seven nights, 2026-10-08 through 2026-10-14, around 2 a.m.
America/New_York. At the assessment after six executed nights, there were three test or
documentation upkeep fixes and no newly confirmed product/data defect; Ben-time savings were
not measured. Exact evidence was useful, but passing checks were not editorial proof. Zero
product defects in six nights is not itself a reason to abandon nightly mega/suite testing.
See the [maintained outcomes](review-trial-status.md) and the linked
[run 5](review-trial-run5-2026-10-12.json) and [run 6](review-trial-run6-2026-10-13.json) receipts;
private evidence remains in its owning repository.

The seventh scheduled attempt was blocked before process creation: HP was offline and the
saved runner failed startup twice with a generic ASB error. It ran no checks and advanced no
anchors; only six nights had execution evidence at that assessment. The status notes record
the separately authorized final continuation. Retain nightly testing, consequential new-change review, objective low-risk
autonomous repairs and quiet successes. New-main-only review was already the trial policy.

Ben renewed continuing review and testing on 2026-10-16 because daytime work relies on the
nightly broad checks. The coordinating session confirmed two enabled schedules with no end
date: hourly screening beginning 2026-10-16 at 13:00 America/New_York, and daily broad checks
around 02:00 America/New_York beginning 2026-10-17. The original seven-night schedule and its
execution history remain closed; the October 16 catch-up is a separate run.

Hourly screening freezes new main tips and examines meaningful endpoint changes since each
reviewed-through anchor. Unchanged tips need no repeated review. It uses the existing focused
check and repair policy; broad checks remain nightly unless the already stated consequence
requires an immediate run. Nightly checks run MAM-basics mega and suite and MAM-private
regeneration and audit even when main is unchanged; hbofonts broad checks are due when its
actual source tip changes. Reconcile later isolated receipts before deciding that a tip is new.

Receipt pushes must respect deployment triggers, including documentation-only main pushes.
By Ben's decision of 2026-10-22, hbofonts' Pages deployment runs only when started by hand.
Until that change reaches hbofonts' main, a push there still deploys, so hbofonts receipts stay
on a separate branch; once it has, a receipt push to that main deploys nothing. The scheduler
is managed separately by the coordinating session; this document
records its confirmed arrangement and creates no automation. Further scheduling changes need
Ben's authorization. The renewal changes no substantive repair authority or publication policy.
