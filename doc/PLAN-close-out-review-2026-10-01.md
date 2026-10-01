# Plan: close out and remediate the first automated relay review

State: live; decision package prepared 2026-10-01; remediation execution awaits Ben's approval.

Codex prepared this plan on 2026-10-01 from the supplied successor prompt. The predecessor
quoted Ben's latest instruction as: "Please give a prompt for a session that will do (or at
least start) what remains to be done. Remediation and/or close-out?" The successor prompt's
remaining text was the predecessor's reconstruction. This plan proposes remediation; no
reviewer agreement or planning commit is execution approval.

## Execution frame and verified preparation

- Source and full integration clone: `C:/Users/BenDe/GitRepos2/MAM-basics`.
- Development checkout: `C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-2026-10-01-claude`.
  Local carrier: `dar-2026-10-01`; shared coordination branch: `origin/dar-2026-10-01`.
- Required source commit: `38c0116f0d5b49c6ff3734e342ed7e79157e43ae`.
  Required closed-review commit: `aad47955e13e88db020113bacbccfce0ac89c7bb`.
  Initial inspection found clean home `main` at the source commit and clean development
  carrier at the review commit. Fresh fetch found `origin/main` at
  `4f4cbb6657e3c7b48a9878308d8cecf6edcc67e1` and the review branch at the review commit.
- Before any tracked edit, D11 preparation merged that fresh main into the development
  carrier. Actual pre-edit HEAD: `ef43a925aa83993400ce4c87cae93dfb47dc2930`.
  Its parents are the required review commit and the fetched main commit; both required
  commits are ancestors. Relative to fetched main, it adds only the round and five turns.
- Interpreter: `C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe`.
  All development scripts, checks, generators, staging and commits run from the development
  checkout. The home clone supplies its environment and receives only final fast-forwards.
- Integration owner: the executing Codex session, or an explicitly named successor accepting
  this plan and its approval snapshot. Intermediate tasks push only the shared review branch.
- Read the latest home and development `AGENTS.md`, canonical common body, the
  `iterative-document-editing`, `codex-worktree-tasks` (runtime and lifecycle references),
  and `mam-repository-topology` skills. Read `doc/dual-agent-review.md` D9/D10/D11/D12/D13
  and review filenames; `doc/periodic-review.md` close-out, D7 and verification cadence;
  the relay plan and runbook; all five numbered turns and the round file. The comparison is
  finished historical evidence, read for the scope boundary below and never rerun.

**Manual ownership preparation completed.** The current runtime audit read both agents'
session databases and leases and found no blockers in either review worktree. A live Windows
process query found no matching round worker or dispatcher. The dispatcher lock and round
in-flight/setup markers were absent. The existing round-specific `pause` action then wrote
`C:/Users/BenDe/GitRepos2/MAM-basics/.novc/dual-agent-review/2026-10-01/PAUSE` before the merge
or any review-branch edit. Reinspection at `2026-10-01T15:54:53.549564-04:00, New York time`
confirmed PAUSE present and no marker, lock or runtime blocker. The scheduler remained
enabled, Ready, with IgnoreNew. The existing paused follow-up must remain paused.
The close-out executor now owns this carrier; no automated worker owns a numbered turn.
The registry entry and round's `State: live` stay as they are pending lifecycle approval.
Do not resume this closed exchange, disable the global scheduler, or erase ownership records.

Repeat the checkout verification before editing; these commands run from any PowerShell 7
directory and name the exact development checkout:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-2026-10-01-claude -C C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-2026-10-01-claude rev-parse --show-toplevel HEAD
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-2026-10-01-claude -C C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-2026-10-01-claude branch --show-current
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-2026-10-01-claude -C C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-2026-10-01-claude status --porcelain=v1 -z
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-2026-10-01-claude -C C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-2026-10-01-claude merge-base --is-ancestor 38c0116f0d5b49c6ff3734e342ed7e79157e43ae HEAD
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-2026-10-01-claude -C C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-2026-10-01-claude merge-base --is-ancestor aad47955e13e88db020113bacbccfce0ac89c7bb HEAD
```

Each ancestry command must exit zero; a different HEAD is acceptable only with explained
ancestry and ownership. Read `runtime_facts` for both exact review checkouts and inspect
current processes, lock and markers again. The planning inspector is the home clone's
ignored `.novc/closeout-20261001-occupancy.py`; its absence does not block repeating those
documented API and control-file checks from a fresh scratch script.

Read-only ownership inspection commands run with the home clone as the working directory:

```powershell
C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --inspect-worktrees --worktree C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-2026-10-01-claude
```

```powershell
C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --inspect-worktrees --worktree C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-2026-10-01-codex
```

These inspections also report retirement gates; an expected lifecycle Git lock does not
authorize its removal. For current writing ownership use the returned runtime facts, current
processes and Git state, rather than inferring that a completed worker record is current.
The Windows process query below emits only identities and matching flags:

```powershell
Get-CimInstance Win32_Process -Filter "Name = 'python.exe' OR Name = 'pythonw.exe' OR Name = 'claude.exe' OR Name = 'codex.exe'" | Select-Object ProcessId, ParentProcessId, Name, @{Name='TargetsThisRound'; Expression={ $_.CommandLine -like '*dar-2026-10-01*' }}, @{Name='RelayDispatcher'; Expression={ $_.CommandLine -like '*--dual-agent-review*tick*' }}
```

Inspect `C:/Users/BenDe/GitRepos2/MAM-basics/.novc/dual-agent-review/dispatcher.lock`
and this round's `inflight.json`, `setup-inflight.json` and `PAUSE` beneath
`C:/Users/BenDe/GitRepos2/MAM-basics/.novc/dual-agent-review/2026-10-01/`.
An unreadable runtime/process audit blocks ownership transfer; a missing lock alone does not
establish inactivity. If a scheduler tick momentarily owns its lock, do no branch mutation
until a fresh audit establishes the paused round has no live worker.

## Single close-out list

The authoritative dispositions are turn 04's **Findings after turn 04**, qualified by turn 05's
**Corrections this turn accepts**, **Evidence this turn adds**, and **Reading notes on turn 04's
wording**. Every surviving fix defaults to later in the remediation phase. No pressing
product failure calls for an immediate main fix.

| Finding | Disposition and proposed remediation |
|---|---|
| 1. Turn 02 stopping without reconciliation | Withdrawn: D13 and both worker instructions require the append even for a blocked turn; D9 permits unchecked claims, so no stop-without-append exception is proposed. |
| 2. Repeated failure suppresses notice | Unfixed; renew notices for a new failure or stale-marker/lock episode after recovery while suppressing repeats of the same unresolved episode. |
| 3. Claude interpreter permission | Qualified and unfixed; align both workers' public checking capability with the procedure, subject to decision C1. Particular Claude denials do not prove every future launch's permissions. |
| 4. Mechanical worker boundary | Qualified and unfixed; state and verify the actual gate limits, subject to C2. The scratch diff-output admission establishes no external escape or complete containment. |
| 5. Whitespace checked after staging | Unfixed; validate all proposed owned bytes before touching the real index, and document recovery of a preserved staged but unapproved attempt. Unstaging alone repeats the whitespace failure. |
| 6. Empty or uninformative refusal reason | Unfixed; include relevant Git stdout, stderr, operation and exit status, with explicit start/end and ancestry context. Retain the completed console-hiding fix. |
| 7. Attempt records reused | Unfixed; use unique attempt and fix-up artifacts, including Codex output, saved fix-up input and refused prose, without rewriting existing evidence. |
| 8. Stop notices and registry lifecycle | Qualified and unfixed; use one stop notice format and retire dispatch eligibility, subject to C3. The present-state maintenance duty already exists, but exchange closure does not itself require a terminal State. A deleted-branch failure blocks later entries for its failure tick only. |
| 9. Turn-01 acknowledgment | Qualified and unfixed; settle D9/D13 semantics through C4, then align parser, prompt and independent transition oracle. |
| 10. Error-text fix-up classifier | Unfixed; classify gate failures structurally, permit one header-only correction including turn-01 State, and give the fix-up the actual owned dirty state. Arbitrary text containing a token must not trigger correction. |
| 11. Deployment test's selected name | Withdrawn as an instruction violation: it is a permitted mechanical source/tree lint; broader agent-file coverage is optional and outside this package. |
| 12. Commit subject versus plan | Unfixed editorial mismatch in the Claude form only; settle C5 and preserve existing subjects and recovery. Correct endpoint ancestry counts are 2 possessive Claude, 4 nonpossessive Claude and 9 Codex. |
| 13. Fetch/push destination verification | Unfixed; verify a retained repository identity before setup and handoff pushes, including home and worker configuration, under C6. Matching tips or URL hashes alone are insufficient. |
| 14. Nested Windows test path | Unfixed test portability defect; add the revision/path separator to the gate's blob read and verify from this long worktree with process-local longpaths disabled. No production relay failure was established. |
| 15. Next: Ben notice content | Unfixed, low severity; carry the worker's reason and current turn path, and describe the decision/Override route rather than directing Ben to an absent in-flight marker. The protocol still retains the reason. |

**Risk and expected outputs.** All proposed changes concern relay code/tests, agent configuration,
instructions and internal documents. No public-facing document or corpus-data change is proposed.
`py/product_scopes.py` declares no product or mega entry reached by the relay. Every declared
published/distributed product must remain unchanged, including `gh-pages/`, `MAM-*`,
`Phonetic-MAM/`, and `Yeivin-ITM/`. Unexpected generated diffs block completion.
Independently, shared-branch and final-main pushes are outward-facing; a changed remote guard
and worker permissions affect acts outside the checkout; attempt-evidence changes require
preservation. No branch deletion, worktree removal, history rewrite or evidence retirement is
part of this approval.

## Decisions and concrete editorial wording

Each recommendation below remains a proposal until Ben answers it. C1 was approved on
2026-10-01 by selecting "Permit public checks (Recommended)"; its quoted wording below is
approved. C2 through C6 and execution scope remain pending. Record answers with their
date and exact approved wording in the single turn-01 update, then freeze the approval snapshot
here before implementation. Ask for execution scope after the decisions are settled; an answer
about a policy alone does not imply execution or main integration.

### C1. Public checking capability, finding 3

Recommend permitting both workers to run relevant public-only scripts and targeted checks with
the exact home interpreter, including scratch probes in their own ignored directory. Preserve
Claude's unattended permission mode; do not switch to auto merely to make a command run.
The alternative is a deliberate restricted-checking protocol whose worker reports missing
execution evidence and sends required reruns to the manual executor; that requires an explicit
exception to the current checking procedure, not a claim that denied checks were performed.

Proposed addition to D13 and the worker instructions:

> Both workers may run relevant public-only scripts and targeted checks with the named home
> clone's interpreter from their own checkout. Before running a check, verify that its inputs
> stay within the round's evidence scope and that it preserves tracked inputs and products.
> Checks write only ignored scratch; workers do not run generators that rewrite tracked output.
> Scratch probes stay in that checkout's ignored directory. A denied or unavailable required
> check is reported as unchecked. Full-suite checks
> that require private inputs belong to manual remediation, outside a public review turn.

The launcher supplies exact-interpreter rules for Claude; a fresh bounded capability probe
checks actual admission and records denials. Do not grant an unrelated interpreter or make
full-suite execution a duty of every numbered turn.

### C2. Worker containment claim, finding 4

Recommend describing the present system as trusted workers with an audited handoff, and making
its observed boundary explicit. This accepts the bounded design; it does not establish a
complete filesystem/remote barrier. The alternative is a separately planned hard-containment
design, which must prove its boundary before adoption and may change C1's implementation.

Replace the relay plan's **Safety and failure handling** sentence "The launch flags and the
gate enforce this mechanically" with:

> Workers are instructed to write only their allowed review records and ignored scratch, and
> to leave staging, commits and pushes to the dispatcher. Launch restrictions reduce their
> capabilities. The gate verifies the worker checkout, permitted paths and the named review
> branch before handoff. These checks do not establish containment of every external file,
> shared Git setting or remote act. This design relies on trusted workers following their
> scope; a complete containment guarantee requires a separately verified boundary.

Add the same limits to the runbook without treating an interpreter allow rule as confinement.
Preserve the distinction between configured grants and observed effective CLI behavior.

### C3. Registry and round-file lifecycle, finding 8

Recommend retaining the round file as a maintained present-state document and adding an
inactive/manual registry state. Closure transitions only that round out of dispatch eligibility;
a new explicit deactivate action handles older already-closed registrations after current
process/marker checks. Retain the entry, control records and transition evidence. Tick skips
inactive entries before resolving the clone or fetching. Cap and decision stops remain paused
but recoverable; a cap does not automatically declare review closure or remediation completion.

Proposed addition to D13 and the runbook:

> On acknowledgment closure, the dispatcher marks that round inactive before later ticks can
> fetch or launch it. Manual close-out begins only after a round-specific pause and verification
> that no worker is live. A deactivate action records manual ownership for an already-closed
> round without deleting its registry entry, checkout or evidence. The round file stays live
> while close-out work remains. After approved remediation is verified and main integration
> has actually succeeded, it records State: executed <date>; close-out completed. The parser
> and tracked-round
> lint accept that terminal State, and terminal rounds are never dispatchable.

Implement the parser/lint and registry transition together; changing State alone is no remedy.
For this round keep PAUSE throughout, then deactivate through the verified new action. The
alternative is Ben-authorized receipt reclassification with a single round update family; that
alternative still needs inactive dispatch state and a recorded archival baseline. Neither
route authorizes deleting a registry entry, branch or worktree.

### C4. Turn-01 acknowledgment, finding 9

Recommend excluding acknowledgment requests at turn 01. Proposed D13 form-2 qualification:

> An acknowledgment request is permitted only from turn 02 onward, after a predecessor's
> claims have been assessed under D9. Turn 01 names turn 02 for the counter-argument or stops
> for Ben; turn 02 always supplies its reconciliation append. The earliest owed acknowledgment
> is turn 03. A counter-argument to turn 01 does not consume a reopening.

The alternative expressly permits an expedited turn-01 request and turn-02 closure, and accepts
that a turn-02 objection consumes a reopening. Record whichever semantics Ben selects in D9,
D13, prompt and oracle; do not infer a choice from the existing validator.

### C5. Future commit subjects, finding 12

Recommend the currently implemented nonpossessive Claude form, aligning the live relay plan's
**Protocol additions** item 4 and **The tick** step 7 with the runbook and code:

> Automated handoffs use Record <Claude|Codex> turn <NN> of the <date> dual-agent review.
> Historical subjects remain unchanged. Recovery verifies the subject recorded for the
> original approved attempt rather than silently replacing its expected wording.

The alternative adopts the plan's possessive Claude form for future commits. If selected,
preserved markers without a subject field still recover under their original form; a new
field records the exact approved subject. No pushed historical subject is amended.

### C6. Remote identity guard, finding 13

Recommend a bounded identity resolver: supported GitHub HTTPS/SSH spellings resolve to an
approved host/owner/repository identity; local rehearsal destinations resolve to the actual
Git directory. Reject unsupported transports or ambiguous aliases before writes. This supports
equivalent known spellings while refusing separate A/B destinations; it makes no universal
remote-ID claim. The alternative uses explicit operator-verified fetch/push identity mappings,
which need their own maintained account configuration and provenance.

Proposed runbook wording:

> Setup records the verified repository identity. Before setup or handoff pushes, and before
> each dispatch, the dispatcher verifies that the home clone's observing destination and
> each worker's effective fetch and push destinations resolve to that identity. Verification
> includes per-worktree configuration and expanded URL rewrite rules. Unknown or ambiguous
> identity stops before a push. Matching branch tips and unchanged URL fingerprints do not
> establish repository identity.

Never print credential-bearing URLs. Revalidate immediately before outbound writes and retain
the setup-to-dispatch baseline. Probe per-worktree config independently from the home clone.

## Implementation waves after approval

1. **Freeze approval and preserve recovery.** Record every answer and approved execution scope
   in `doc/dual-agent-review-2026-10-01-turn-01-claude-update.md`; revise this live plan.
   Snapshot existing attempt metadata/evidence without rewriting originals. Recheck pause,
   ownership, exact HEAD, clean status, fetched tips and baseline ancestry. Merge fresh main
   in this worktree as D11 requires before subsequent edits. Do not copy the home environment.
2. **Repair handoff, diagnostics and portability (5, 6, 13, 14).** Change the two relay modules
   and extend the local Git differential. Whitespace validation uses a disposable index built
   from the baseline and exactly the admitted paths, so Git's own attributes/whitespace rules
   are the oracle and the real index remains untouched on refusal. A late staged-but-unapproved
   state is preserved for explicit recovery. Git diagnostics carry operation/exit/stdout/stderr;
   start/end lookup and false ancestry have meaningful context. Add `--` to the gate's blob
   read. Implement C6 with pre-write checks and retained identity rather than tip equality.
3. **Repair attempts, fix-up and notices (2, 7, 10, 15 and notice portion of 8).** Create unique
   attempt directories with exclusive creation; each initial/fix-up launch has its own prompt,
   command, streams and Codex last message. Persist first gate diagnostics and refused owned
   bytes before the bounded correction. Typed failures distinguish header errors from path,
   Git, whitespace or ownership failures. A dedicated fix-up prompt states the expected dirty
   paths, unchanged HEAD and no-staging condition. New failure episodes get a fresh notice;
   repeats within an unresolved episode stay quiet. Use one structured stop formatter on
   handoff and idle paths; a successful Ben stop names its reason, turn and Override route.

   Proposed successful-stop notice wording, also subject to the editorial approval:

   > <repository>, round <date>: Ben's decision required: <worker reason>. Read <turn path>.
   > Record the decision in <turn-01 update path>; continue through an authorized Override:
   > in <round-file path>.
4. **Apply approved policies (3, 4, 8, 9, 12).** Align configuration, worker agent, parser,
   registry actions, CLI choices, oracle and maintained docs. Add backward-compatible reads
   for existing registries/markers; unknown states fail loudly. Deactivate this paused round
   through the verified action only after it is available in the scheduler's source checkout.
   Do not run the worktree entry point as though its CONTROL were the home registry.
5. **Verify, reconcile and integrate.** Resolve every list item in the one update, recording
   changed paths, checks, commits and any approved deferral by searchable passage. Add a concise
   October 1 closure/remediation entry to `doc/dual-agent-review.md`. Update the live relay plan
   and runbook in place; leave the five numbered turns and comparison untouched except the
   sole turn-01 pointer. Run the final gates and integration sequence below. Record verified
   remediation with integration pending before the push; declare completed close-out only
   after actual successful integration and the home-registry/deployment checks below.

Expected changed paths: this plan, the single turn-01 update and its base pointer;
`py/repo_util/dual_agent_review_dispatch.py`, `py/repo_util/dual_agent_review_round.py`,
both `py/tests/test_dual_agent_review_*.py` files, `py/main_repo_util.py` for the action,
`in/dual_agent_review_automation.json`, `dot-claude/agents/dual-agent-review-turn.md`,
the live relay plan/runbook/procedure, and the round file's approved terminal State.
Do not broaden the deployment lint for withdrawn finding 11.

## Verification and commit discipline

Run commands from the development checkout unless a different checkout is named. On Windows
use PowerShell 7, exact-path per-command Git trust, and the home interpreter. Shell commands
below use one command per block; set process-local exact Git trust for script children where
needed. All filename-producing Git commands use NUL delimiters.

Before each coherent commit, recheck HEAD and task-owned status against the recorded pre-edit
HEAD, run `git diff --check`, Black every changed Python file at defaults, and the directly
relevant checks. Stage only named owned paths and commit, then push `origin HEAD:dar-2026-10-01`
normally. A changed remote review tip or rejected push stops for collision investigation;
no force, reset, rebase, amend or discard is authorized.

The protocol oracle covers both Agent-1 assignments, the admitted lifecycle states, each
control form and cap, and C4's reachable transitions. The real local-Git differential covers
repeated failures/recovery, whitespace before staging, preserved legacy recovery, unique
initial/fix-up evidence, every typed refusal category, and Ben stop contents. Independent Git
reads establish actual index/tree/remote bytes and unchanged main. Use separate local A/B
repositories for setup, between-turn and per-worktree splits; both remain unchanged on
refusal. Compare canonical local aliases and supported GitHub URL forms against independent
identity expectations. A two-round oracle verifies that inactive closed registrations neither
fetch nor notify and do not stop another round. Missing inputs fail rather than skip.
No example-based test merely pins a chosen string or name.

Focused command:

```powershell
C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe py/main_test.py py/tests/test_dual_agent_review_turns.py py/tests/test_dual_agent_review_dispatch.py -q -p no:cacheprovider
```

For finding 14, a scratch wrapper in this worktree invokes that same entry point with
process-local `core.longpaths=false` and records the effective setting and unchanged Git
configuration. Do not relocate the test into a short checkout or change machine settings to
make it pass. Check explicit encodings with PYTHONUTF8=0 and PYTHONIOENCODING cleared.
A new bounded local capability probe, if C1 is approved, launches no numbered review and
pushes to no network remote. Preserve its logs; distinguish source permission rules from
observed worker behavior. A live notification-receipt test is separate if needed to establish
actual receipt, rather than claiming fake-worker checks prove what Ben saw.

After the last test-risky change, run the full suite once, then repeat only when new changes,
failures or unresolved concerns justify it. This manual remediation may use the private
inputs the suite requires, but private findings/logs remain in MAM-private. Prior rollout
results are historical and do not validate new implementation.

```powershell
C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q
```

Reserve the mega for final integration after merging fresh main. It runs here despite absent
relay product reach because this approved branch then includes executable remediation.

```powershell
C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
```

Every step must pass and every tracked generated diff must be read and explained; commit
explained output in this worktree. Expect no generated output changes from relay remediation.
Do not hydrate or synchronize a missing/occupied sibling merely to bypass a failure; follow
the topology procedure and existing authorization.

## Final integration and deployment

After all approvals and remediation are complete, fetch origin in the home clone. Fast-forward
its clean main to fresh origin/main only when no other writer occupies it. Merge fresh main
into the development carrier; apply the owed checks above there. Push the verified review
commit to the one shared branch. Fetch again immediately before final integration. If fresh
origin/main is not an ancestor, return to the worktree, merge and repeat affected gates.
Fast-forward the clean home main to the verified review branch and push main normally.
A refused fast-forward or moved-origin push returns to the worktree; never substitute a merge
in the home clone. Recheck both roots, commits, status and live tips.

Only after main is pushed, deploy changed canonical agent instructions from the full home
clone using its own environment; the deployment fetches and installs from fresh origin/main.

```powershell
C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config
```

```powershell
C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe py/main_repo_util.py --sync-user-config --check
```

Then use the approved lifecycle action from that home clone for its actual registry. Keep the
existing PAUSE while the scheduler source remains old. Verify the enabled scheduler skips this
round without fetching or launching, and the registry/control evidence remains recoverable.
Do not unpause the follow-up, start another round or perform private rollout.

After successful main push, deployment and registry checks, finish the actual-result receipt,
round's terminal State and this plan's executed State in one documentation commit in the
development worktree. Push it to the shared branch and fast-forward/push the clean home main
under the same fresh-origin safeguards. The verified executable tree and generated outputs
are unchanged by this receipt, so cheap documentation checks suffice and the still-relevant
suite/mega results do not expire. If incoming main introduces test or product risk, merge and
repeat the affected gates in the worktree before that final fast-forward.

## Scope boundary and deferred proposals

The comparison's **Additions and omissions** is not remediation authorization. Its A1 console
fix is already completed by separately requested `0c12552b`. Its A2 first-error persistence,
refused-copy and dirty fix-up prompt overlap surviving findings 7/10 and are included only to
that extent. Its A3 general failed-setup/recovery runbook, A4 pause while a worker holds the
lock, A5 lock-collision notices, A6 removed-clone recreation, A7 private refusal-text handling
and A8 independent-check description remain separate proposals. No new work on those unique
additions, header/date/scalar/config hardening, deployment-lint broadening or acknowledgment
prompt performance tuning is approved here. Do not rerun the blind comparison.

The original review's **Open ends the window itself declares** remain distinguished from
defects: the comparison, scheduler registration and first production exchange are now recorded
complete; facts-only remains false and unapproved; private readiness P7 and a private kickoff
remain separate; rehearsal/evidence retirement remains unauthorized; checker completion before
the rehearsal's first draft remains bounded historical evidence. Reconcile stale present-tense
rollout claims only to verified outcomes, without attributing the implementation's choices to
new decisions by Ben. Preserve the two completed September 29 reviews and Ben's follow-up work.

## Cumulative ledger and approval snapshot

| Requirement | Status |
|---|---|
| One complete list, including withdrawn claims and final qualifications | implemented in planning; execution dispositions still pending |
| Exact checkout/ancestry, current worker occupancy and round-specific pause | implemented in preparation; repeat ownership checks before every write phase |
| C1 public checking capability and quoted wording | implemented decision: approved by Ben 2026-10-01; execution remains pending |
| C2 through C6 concrete choices and editorial wording | unresolved; Ben's answers required |
| Defect fixes and approved policy implementation | deferred to approved remediation |
| Sole turn-01 update and exact base pointer | implemented for planning; append approved decisions and later results here |
| Suite after final test-risky change and final mega/integration | deferred; no new remediation validated yet |
| Preserved turns, finished comparison, console fix, manual reviews and private boundary | active throughout |

Approval snapshot: C1 approved 2026-10-01; remaining decisions and execution not yet approved.
Record dated decisions, approved alternatives, expected
changed paths, any deferrals and explicit execution/final-integration scope before wave 1.
Planning validation at `ef43a925aa83993400ce4c87cae93dfb47dc2930`: the protocol/census/deployment
lint module passed 3 tests and the tracked whitespace check passed. No Python implementation
changed in preparation, so no Black, full suite or mega is owed by this planning commit.
These results do not validate any future remediation.
If work ends before completion, commit/push finished authorized work and provide a standalone
successor prompt naming source/development/integration paths, exact required commit, pause
and ownership state, approvals still missing, verification owed and integration owner.
