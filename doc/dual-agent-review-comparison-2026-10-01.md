# Independent comparison of the first production review's counter-arguments

State: executed 2026-10-01; approved comparison completed; historical review evidence only.

**Both counter-arguments added verified value, and neither covered all the verified material.**
Codex correctly rejected two claimed defects and added two independently reproduced findings.
Blind Claude corrected recovery and evidence-preservation claims that Codex accepted too broadly,
and added further operational and editorial observations. This single comparison of different
agent/model bundles does not establish general model superiority or a standing review policy.

Codex recorded this comparison in `C:/Users/BenDe/GitRepos2/MAM-basics` on `main`, after a fresh
read-only sub-agent's independent assessment and parent verification. Ben approved the proposed
comparison and this filename with "Run the comparison using that filename (Recommended)".
The approved kickoff instruction was:

> Run the first automated MAM-basics review of the relay implementation window with Claude as Agent 1.

## Inputs and independence

The approved endpoint diff is
`303bf2399c1e1fc1300a75f4fb1ed335d62984d0..1bfceff4d952470618fc7584a6bca4fc5c9b2f5f`.
Call the endpoint **E** and the original turn-01 commit
`dd50e9b946609ac8ab7cc8c15d205d93dd5390e9` **B**. Implementation claims below refer to E;
instruction judgments use the instructions at B. Later review turns do not supply comparison
evidence. This record decides neither remediation nor close-out.

| Input | Exact source | SHA-256 |
|---|---|---|
| Original argument | `doc/dual-agent-review-2026-10-01-turn-01-claude.md` at B, before reconciliation | `5b1db09bc9a0bfa7fe44e86d9eeb0414eec819e6c8d4f1820b15d74c832a9aa0` |
| Codex counter-argument | `doc/dual-agent-review-2026-10-01-turn-02-codex.md` at `c9d49a232357140a1d370d454be42b3fd1c8f309` | `0e04f0c087ec4094023eda20640a050a9cd60d5aa0d56b6f22b7eef8fe935adb` |
| Blind Claude counter-argument | `.novc/dual-agent-review-comparison-2026-10-01-claude.md` in the detached comparison checkout | `1489f5b7276d1f8aef1e4a64808d1fcb68a820a845ea139630b4e5d66b121f5d` |

The one-time operator waited for the dispatcher-verified turn-01 handoff, then launched fresh
Claude Opus 5.5/max in
`C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-comparison-2026-10-01-claude`,
detached at B. It did not duplicate a production worker or write the review branch. The blind
worker launched at `2026-10-01T12:03:58.249172-04:00, New York time`, and its completion receipt
was written at `2026-10-01T13:14:39.678789-04:00, New York time`. Its result event reports success.
Its tracked checkout remained clean and its output hash matches the completion receipt.

Parent inspection of the saved stream, including checker calls, found reads within the blind
checkout, earlier Git ancestry, installed Git documentation and the worker's own tool-result
cache. No detected read used Codex turn 02, later review content, another worker's log or private
material. All valid referenced commit hashes were B or its ancestors; the invalid-ref probe and Git's empty
tree object were separately identified. This is an audit of the saved activity, not a claim that
the Git object store made later content physically inaccessible.

The independent assessor, `/root/independent_counterargument_comparison`, was a fresh Codex
sub-agent with no inherited conversation, who authored neither input. It read the original
argument, both counter-arguments, the endpoint diff and baseline instructions, and read no turn
03 or later or private material. It made no writes or Git mutations. The parent checked the
adopted source and instruction claims, recounted the disputed history, and independently read
the retained destination and path-length probes. The parent knew the broader rollout context;
the independent assessor's input boundary supplies the separation for this assessment.

## Original findings

In this table **D** is `py/repo_util/dual_agent_review_dispatch.py`, **P** is
`py/repo_util/dual_agent_review_round.py`, and **TT** is
`py/tests/test_dual_agent_review_turns.py`. Line citations refer to E unless B is named.
Confirmed defects remain historical findings awaiting the separate remediation procedure.

| Finding | Codex | Blind Claude | Verified comparison |
|---|---|---|---|
| 1. Blocked turn 02 and its append | Rejects code defect | Confirms narrower defect and instruction conflict | **Reject the claimed code defect.** The prompt and agent instructions require an append even for a blocked turn; D9 allows unchecked entries. A stable incomplete report can obey both. D:519-529,691-700; B:`doc/dual-agent-review.md`:121-123,321-327. |
| 2. Repeated failure after resume | Confirms | Confirms with precision notes | **Confirmed.** The same reason/tip signature survives resume; varying exit and gate details must also repeat. Existing notice files and stderr still supply evidence. D:139-163,1025-1035. |
| 3. Interpreter checks | Qualifies configured versus effective permissions | Confirms with qualifications and a denial | **Configuration mismatch confirmed; universal inability qualified.** Tracked permissions omit an interpreter despite mandatory reruns of cited scripts. Effective inherited permissions are unknown; descriptive review section shape is not mandatory. E:`in/dual_agent_review_automation.json`:11,17-18; B:`doc/periodic-review.md`:205-207,290-295. |
| 4. Mechanical boundary | Qualifies, without demonstrated escape | Confirms and adds shared hooks/config consequence | **Confirmed limitation; effective escape unverified.** The gate checks limited state, and shared Git metadata matters, but neither input demonstrates a complete permission escape. D:260-266,549-559,659-743,791,819. |
| 5. Whitespace checked after staging | Confirms | Confirms and corrects recovery/fix-up claims | **Confirmed with Claude's substantive corrections.** Unstaging alone repeats the failure unless whitespace changes. A tracked append's whitespace report can echo a classifier token and trigger fix-up, contrary to the original blanket statement. D:740-742,768-778,928-942; P:31-38. |
| 6. Empty refusal reasons | Confirms | Confirms and adds omitted subject diagnostic | **Confirmed.** Git errors retain stderr but discard stdout; the handoff diagnostic mentions tree and parent although it also tests subject. P:31-38; D:794-803. |
| 7. Re-dispatch overwrites records | Confirms without further qualification | Confirms and corrects two preconditions | **Confirmed with Claude's material qualifications.** Re-dispatch requires a clean checkout; fix-up can rewrite refused prose while its marker stands. Codex's unconditional confirmation preserves a false narrowing. D:854-866,894-895,901-942. |
| 8. Notices and retained registry | Confirms mechanisms, qualifies State and one-tick effect | Confirms with exception-placement precision | **Confirmed with bounds.** Closed rounds remain registered. Handled failure pauses one round before ending one tick; notification failures outside those handlers need not pause it. No explicit State transition at exchange closure is established by these inputs. D:466-468,849-885,946-958,1018-1019. |
| 9. Turn-01 acknowledgment | Qualifies as D9/D13 ambiguity | Confirms without qualification | **Policy ambiguity.** Literal D13 permits the transition; D9 assigns turn 02 a counter-argument. The existing text does not settle which interpretation should prevail. P:220-229,313; B:`doc/dual-agent-review.md`:118-145,306-312. |
| 10. Error-text fix-up classifier | Confirms | Confirms and extends consequences | **Confirmed.** Tokens classify errors, and the malformed turn-01 State message contains none of them. The test does not exercise fix-up. D:925-944; P:212-218; E:`py/tests/test_dual_agent_review_dispatch.py`:107-135,210. |
| 11. Selected deployment-name test | Rejects instruction violation | Confirms violation | **Reject the claimed violation.** The test inspects actual source and tree state, an explicitly permitted mechanical lint shape. Narrow coverage alone does not make it an example-based unit test. TT:144-154; B:`dot-Codex/user-wide-AGENTS.md`:337-348. |
| 12. Commit subject and census | Confirms plan mismatch, changes census | Confirms mismatch, corrects ISO-date statement | **Editorial mismatch confirmed; census corrected.** The same prefix selection gives 8/4/13 at setup and 2/4/9 at E. Codex's 2/1/4 requires the extra phrase filter "dual-agent review". Claude correctly identifies `2b36515320bd61a41a051bdb02422866d6ed73e0` as an ISO-date example. D:767,798-799; E:`doc/PLAN-automate-the-dual-agent-review-relay.md`:484-487. |

## Additions and omissions

| Addition | Verified contribution and limit |
|---|---|
| Codex 13: fetch/push destinations | **Confirmed unique addition.** Setup accepts one URL of each kind, observes via fetch and writes via push before verifying. The retained local probe's fetch repository has no refs, while its push repository has setup commit `10378bc4206364a0550d79d45fa7385308fc9f7d`; setup then refuses with no registry entry. Different URL spellings may still denote one repository, so simple string equality is not an established remedy. D:81-87,100-116,371-375,460-469. |
| Codex 14: Windows test-path budget | **Confirmed unique bounded portability failure.** The retained checkout's ordinary `git show` exits 128 with "Filename too long"; per-command `core.longpaths=true` succeeds. The artifact path is 221 characters, or 262 including the revision prefix. The internal cause remains an inference; this establishes a test failure, not production failure. E:`py/tests/test_dual_agent_review_dispatch.py`:21-24. |
| Claude A1: Git children not hidden | **Missing flag confirmed; original visible-window consequence qualified.** Git children lack the hiding flags used for other children. The historical record did not test an active hidden tick. Ben separately requested terminal suppression during this comparison; `0c12552b` adds the Git flag outside the reviewed window. The runbook records that later action and observation bounds. P:31-36; D:176,621,632. |
| Claude A2: fix-up evidence and prompt | **Valid extensions with overlap.** No dedicated refused-version copy or persisted fix-up prompt/error list is written, and the reused prompt requests clean status for a dirty checkout. "No record" is too broad because CLI streams may retain input or earlier content. Its successful-fix-up notice point overlaps finding 10. D:1,502,901,913-945. |
| Claude A3: recovery documentation | **Confirmed extension with unique failed-setup component.** The runbook describes push recovery; failed setup can leave unregistered resources that start refuses to adopt. Other refusal states also need checkout and marker handling the runbook does not describe. D:388-423,460-470,768-778,894-895,1027-1035; E:`doc/dual-agent-review-automation.md`:49-59. |
| Claude A4: pause during worker | **Confirmed unique addition.** Every non-status action takes the lock held through worker and fix-up waits, so pause refuses during that interval. A repository-level PAUSE path is implemented but absent from the window's documentation. D:119-136,625,850-853,936-942,971-982,1018-1035. |
| Claude A5: collision notifications | **Confirmed with deduplication bound.** Lock collision calls notify for every registered round, including paused/closed rounds; deduplication may prevent a fresh visible notice. A missing clone can raise within that exception handler. D:142-157,1058-1065; E:`py/mb_cmn/git_process.py`:10-19. |
| Claude A6: removed clone path | **Confirmed latent code route.** Strict repository resolution fails, then recursive PAUSE-parent creation recreates the former clone path. Actual retirement or recloning was not exercised. D:48-50,849-872; E:`py/mb_cmn/git_process.py`:10-19. |
| Claude A7: private refusal text | **Confirmed conditional code route only.** Missing streams use the helper clone's scheduler log; raw append-whitespace text can enter its refusal and toast. No private material or private production occurrence was consulted, and private readiness P7 remains pending. E:`py/main_repo_util.py`:104,509-516; D:740-742,944,956-957,1065; E:`misc/dual-agent-review-toast.ps1`:15-22. |
| Claude A8: independent-check description | **Confirmed unique editorial addition.** Independent Git checks cover tips, paths, home HEAD and an approved tree; append contents and closure rely on dispatcher logic, and idle relies on fake-worker count. "Every guard" also exceeds the exercised cases. E:`doc/dual-agent-review-automation.md`:98-105; E:`py/tests/test_dual_agent_review_dispatch.py`:158-175,185-212,239-277. |

Claude's additional header-isolation, syntactic-State and forced-push-test qualifications are
supported by the cited source: header input ends only at the first `## ` line, and the forced
push failure raises before Git runs. Those observations do not establish new semantic policy.
Both inputs appropriately leave unproved effective CLI restrictions, scalar event behavior and
other speculative bypasses unresolved. Scheduler power defaults remain unverified here.

Codex missed Claude's material fix-up/recovery corrections and operational additions. Blind
Claude missed Codex's destination and test-path additions, retained unsupported judgments in
findings 1 and 11, and treated finding 9 as settled. Counting findings would obscure overlap,
policy questions and evidence limits. The two bundles supplied complementary value in this case.

## Effort evidence

| Field | Codex counter-argument | Blind Claude counter-argument |
|---|---|---|
| Model / effort | `gpt-6.1-sol` / `xhigh`, confirmed in saved runtime context | `claude-opus-5-5` / `max`, confirmed in launch and initialization |
| Terminal event | `turn.completed` | successful `result` |
| Reported duration | Unavailable | 4,239,453 ms, approximately 70.66 minutes |
| Reported turns | Unavailable | 80 |
| Foreground checkers | Five reported in turn 02; no terminal aggregate | Ten spawned/completed in saved statistics; zero background starts |
| Terminal input accounting | 5,102,054 input; 4,969,344 cached input | 66 input; 461,740 cache creation; 7,168,141 cache read |
| Terminal output accounting | 21,024 output; 4,743 reasoning output | 268,489 output; 210,194 thinking output |

Claude's separate `modelUsage` view reports 712 input, 2,258,714 cache creation, 40,677,135 cache
read, 1,017,575 output and 827,856 thinking tokens, plus list-basis cost USD 41.168565. That is not
an actual account-charge measurement or a field-for-field comparison with Codex. The blind
report's self-count of 73 calls before writing differs in scope from the saved stream's 487 calls
including checkers; both scopes are preserved. Permission denials limited the blind session's
interpreter checks. Neither timing nor token numbers absent from Codex's terminal were invented.

## Evidence retained and verification

The home clone retains all operator inputs, receipts and logs under
`.novc/dual-agent-review-comparison/2026-10-01/`, including `completed.json`,
`operator-independent-audit.json` and `blind-boundary-extract.json`. Production turn evidence is
under `.novc/production-relay-independent-verification-20261001/`, including `turn-02.json` and
the saved Codex runtime-context records. The retained local probes remain in the Codex review
checkout's `.novc/pef16d/s/` and `.novc/t/p6174/`; no evidence or checkout was removed.

Parent reproduction is `.novc/comparison-parent-probe-verification-20261001.json` in the home
clone, and `.novc/verify-comparison-counts-20261001.py` recounts the prefix census. Source and
instruction verification used exact historical commits. The append below mechanically preserves
the complete UTF-8 counter-argument inputs; their extracted bytes and hashes are checked before
commit. Documentation checks do not rerun model workers or expire the relevant suite result.

The production review proceeds separately under the scheduler. Facts-only from turn 03 remains
false. Close-out, review integration, remediation and private rollout retain their separate
decisions and procedures.

## Codex counter-argument, preserved verbatim

````markdown
# Counter-argument to the 2026-10-01 review of the relay implementation window

State: completed 2026-10-01; review only
Next: turn 03, claude

Codex (`gpt-6.1-sol`) wrote turn 02 at `xhigh`, extra high, effort. Ben's kickoff instruction, verbatim: "Run the first automated MAM-basics review of the relay implementation window with Claude as Agent 1."
This turn follows D9 as Agent 2: check Claude's claims, inspect the same endpoint diff
for omissions, and append the reconciliation after the turn is stable.

**The findings remain unfixed.** I confirm findings 2, 5, 6, 7, 10 and the plan mismatch
in 12; qualify findings 3, 4, 8 and 9; and reject the claimed defects in 1 and 11.
Two additional findings, 13 and 14 below, concern destination verification and the
new differential test's Windows path budget. Claude's next turn should assess these
corrections and additions. This turn requests a rebuttal rather than an acknowledgment.

## Provenance, scope and checking

The source and home clone is `C:/Users/BenDe/GitRepos2/MAM-basics`. The development
checkout is `C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-2026-10-01-codex`.
Before reading, I verified that exact root, `HEAD`
`dd50e9b946609ac8ab7cc8c15d205d93dd5390e9`, carrier
`dual-agent-review-2026-10-01-codex`, and clean NUL-delimited status. The status command
also warned that the sandbox could not read the account's Git ignore file; its status
output contained no records. I rechecked the same HEAD and clean status before writing.
The dispatcher's supplied reference is 2026-10-01T12:05:19.524412-04:00, New York time.
The dispatcher owns staging, committing and pushing; Ben's later close-out owns integration.

I read `AGENTS.md`, the required predecessor from that commit, D9, D10, D11, D13,
the review naming section, and the periodic-review effort and checking procedure.
I applied `codex-worktree-tasks` and `iterative-document-editing`. I read all 15 paths
in the endpoint diff
`303bf2399c1e1fc1300a75f4fb1ed335d62984d0..1bfceff4d952470618fc7584a6bca4fc5c9b2f5f`.
The nine-commit count and NUL-delimited file census agree with turn 01; the numstat
totals are 2,506 additions and 34 deletions. The two relay modules, both relay test
files, configuration, scripts and config-sync module are unchanged between the
endpoint and required HEAD. The current procedure supplies
the working instructions; the endpoint versions supply evidence about the implementation.
This window contains no prior round's review records. I read no MAM-private material.

Three foreground read-only checkers verified findings 1–4, 5–8 and 9–12, respectively,
and swept their related implementation surfaces. Two checkers then made separate
read-only passes over the new destination and path findings and the root's scratch
results. Every checker finished before either tracked review file was written.
The root independently read the cited code and ran the probes described below.
All scratch, synthetic repositories and receipts stay under this checkout's `.novc/`.
Every synthetic probe's origin is a local bare repository.

## Tree health and evidence limits

**The window's whitespace check passed.** Its endpoint `git diff --check` printed
nothing. The initial public-only targeted run was:

```powershell
C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe py/main_test.py py/tests/test_dual_agent_review_turns.py py/tests/test_dual_agent_review_dispatch.py -q -p no:cacheprovider
```

It produced **3 passed, 1 failed**, with the new dispatcher differential failing at
the nested scratch worktree's `git show` because Git reported `Filename too long`.
Finding 14 records the bounded consequence. A rerun of those unchanged tests with
process-local `core.longpaths=true` and `core.excludesfile` pointing to this checkout's
`.gitignore` produced **4 passed**. The exclusion setting suppresses the sandbox's
account-ignore warning; its patterns cover neither the asserted unexpected file nor
the turn files. Neither setting was persisted.

**The full suite remains unchecked in this turn**, because the public-only boundary
excludes its private-input tests. No mega or generator is owed by the review files.
Black was not rerun: no tracked Python changed, and the endpoint runbook's Black and
full-suite results remain attributed implementation records rather than repeated results.

Findings below rely on tracked code and reconstructible local probes. The worker-denial
quotations in turn 01, the predecessor's accounts of its own checker activity, and the
implementation's untracked rehearsal receipts were not independently verified here.
The turn-01 denial quotations are not proof of effective CLI permissions for a future
worker. I used no external CLI documentation to establish a permission escape.

## Corrections to turn 01

### Finding 1: the required turn-02 append is documented

**Rejected as a code defect.** The gate does refuse turn 02 without the append, but
D13 explicitly says "Workers write only their new turn and, for turn 02, the
reconciliation append to turn 01." The generated prompt repeats that unconditional
requirement. D9 lets the table record confirmed, qualified, rejected and **unchecked**
claims. A stable report of an incomplete review can therefore append an honest table
without claiming that all work finished.

The finding's sentence "No window document tells a blocked turn 02 to append anyway"
overlooks the universal requirement. A missing append pausing and notifying is the
specified refusal behavior; notification does not require publishing that stop to the
remote branch. An exception permitting a stop without reconciliation would be a new
policy for Ben to choose, rather than a repair established by the existing protocol.

### Findings 3 and 4: configuration is verifiable; effective CLI restrictions are not

**Qualified; the configuration gap and limited gate scope remain unfixed.** The
configuration selects `dontAsk` without an interpreter rule, and `worker_command()`
adds Git rules while denying Bash on Windows. The prompt supplies an interpreter,
and the review-checking procedure calls for rerunning cited scripts. That mismatch
supports asking Ben how automated workers should perform those checks. The files do
not establish every future Claude worker's effective permissions, including inherited
CLI settings. I do not independently adopt the exact transcript denial quotations.

Finding 4 correctly identifies unscoped Edit and Write grants and wildcard suffixes
on Git rules. `gate()` observes the worker checkout and the named round branch,
with ignored scratch excluded. Those checks do not establish a complete boundary
around external files or remote acts. The plan's "The launch flags and the gate
enforce this mechanically" consequently needs a bounded interpretation. The effective
CLI matching and any broader filesystem boundary remain untested; the listed Git
option examples do not establish an observed escape in this review.

### Finding 8: the State constraint is prospective, and the registry failure lasts one tick

**Qualified; duplicate notices and the registry lifecycle gap remain unfixed.** The
source confirms the distinct `round closed` and `round closed: ` reasons, retained
registry entries, fetching after a stop, and renewed notices at changed tips.

`parse_round()` and the tracked-round lint require `State: live`, but no window
instruction requires changing that State when the exchange closes. Retaining live
metadata alongside a final closed turn is currently valid. The finding identifies a
close-out design constraint, rather than an already required State transition that fails.

A deleted remote branch makes the failure tick exit before later registry entries.
That tick also writes `PAUSE`; subsequent ticks skip the failed round and can reach
the later entries. The defect does not establish permanent starvation of those rounds.

### Finding 9: D9 and D13 need a shared policy for turn-01 acknowledgment

**Qualified; a protocol ambiguity remains for Ben.** The validator, prompt and test
oracle permit acknowledgment at turn 01, and a turn-02 objection then consumes a
reopening. D9 assigns turn 02 a counter-argument, while D13's new acknowledgment
form contains no turn-01 exclusion. The implementation matches that literal D13 form.
Changing the permitted form would settle the protocol's meaning; the review cannot
choose that meaning solely from the surprising consequence.

### Finding 11: the deployment test is a permitted source lint

**Rejected as an instruction violation.** The test checks a real repository file,
the archive-path constant and a substring in the mapping's source. The common rule
expressly permits "A mechanical lint over source text or the repository tree."
The prohibition quoted by turn 01 applies to an **example-based unit test**. This
test supplies no synthetic behavioral example. Its narrow coverage is real, but
enumerating every agent file is an optional improvement, not a requirement established
by that rule. The absence of a request for one named test therefore does not prove a violation.

### Finding 12: the plan mismatch holds; the history count is broader than endpoint ancestry

**Confirmed, unfixed, as a low-severity editorial plan mismatch.** The endpoint plan's
tick step 7 specifies `Record <Claude's|Codex> turn`, while `handoff()` computes
`Record Claude turn`. Recovery compares the subject to the computed string, so a
future subject change must account for preserved markers.

The checker's eight possessive Claude, four earlier nonpossessive Claude and thirteen
Codex subjects reproduce using `git log --all`, excluding this round's new commit.
They are not counts of endpoint ancestry alone. That ancestry gives two, one and
four, respectively. The mixed usage conclusion holds; no history rewrite is proposed.

## Confirmed findings and reproduced mechanisms

**Findings 2, 5, 6, 7 and 10 remain confirmed and unfixed.** The checkers' source
readings agree with the root's reading. Findings 7 and 10 need no added qualification
beyond turn 01's existing bounds: redispatch overwrites attempt records after explicit
recovery, and the fix-up classifier relies on error-text tokens.

For findings 5 and 6, the root created a synthetic home clone and local bare origin,
used the real `start()` and `tick_round()`, and substituted a deterministic worker
that wrote a valid turn header followed by a trailing-space line. Only model selection
and occupancy were stubbed. The gate accepted the untracked file, cached whitespace
checking refused it after staging, the marker had no `approved_tree`, and `PAUSE`
contained only a newline. A repeated `handoff()` refused the staging/status/path breach.
A checker independently read the script and results. This verifies both the staged
but unapproved recovery gap and the stderr-only diagnostic defect. With the sandbox's
account-ignore warning present, the refusal instead carries that unrelated warning;
it still omits the actual whitespace report on stdout.

For finding 2, an isolated `notify()` probe supplied a fixed cached tip and disabled
the toast. The second call with the same reason left the notice untouched. The stronger
evidence is the source's early return and `resume` removing only `PAUSE`; this probe
does not claim an end-to-end resume test or live notification receipt.

## Additional findings

### 13. Setup pushes through a destination it has not verified against the observed round

**Unfixed.** A new operational defect, independently checked with real local Git.
`origin_urls()` permits one fetch URL and one push URL, without establishing that
the initial destinations coordinate the same repository. `remote_tip()` observes
origin's fetch destination. `start()` pushes through origin's push destination and
only afterward verifies through the fetch destination (dispatcher's passages
`setup requires exactly one fetch URL and one push URL`, `HEAD:refs/heads/dar-`,
and `setup push could not be verified`). URL fingerprints detect subsequent changes
but do not establish this initial relationship.

The root created two empty local bare repositories, A and B, and a clean synthetic
home clone on main. Origin's sole fetch URL named A; its sole push URL named B.
The start and end commits both named the synthetic baseline. The normal configuration
was used with rehearsal enabled; only model selection and occupancy were stubbed.
`start()` pushed `refs/heads/dar-2026-10-01` to B, then raised
`setup push could not be verified`. A still had no refs, the registry was absent,
and `setup-inflight.json` remained. The checker independently queried both bare
repositories and checked the pushed setup commit's parent and subject.

The same distinction appears in handoff's pre-push and post-push remote observations;
that path was source-checked, not separately reproduced. Different fetch and push URL
spellings can legitimately address the same repository, so string equality alone is
not an established remedy. The finding concerns an unverified destination relationship,
not the presence of distinct spellings.

Product reach is absent, but the separate act risk matters: verification can refuse
only after a branch has been written to a different destination. The probe exercised
that act solely in local disposable repositories.

### 14. The new dispatcher differential fails within the authorized worktree's path budget

**Unfixed.** A test portability defect in the window, with bounded Windows scope.
`test_local_dispatch_against_git_oracle` nests its synthetic `MAM-basics` home and
two relay worktrees beneath `tmp_path`; the default Windows runner supplies a
worktree-local `.novc/t/<process-id>` base. From this round's authorized checkout,
the test reaches the turn-02 gate and Git reports:

```text
fatal: failed to stat '<commit>:doc/dual-agent-review-2026-09-30-turn-01-claude.md': Filename too long
```

The original command and result are recorded under Tree health above. Effective
`core.longpaths` was unset in this exact checkout, and `LongPathsEnabled` was 0.
The actual scratch turn-01 pathname measures 221 characters. Including the
41-character revision prefix to the corresponding pathname gives 262 characters;
Git's revision/path stat probe causing the failure is an inference from that
measurement and the diagnostic, rather than a claim that the actual artifact path
itself exceeds the legacy limit.

The unchanged targeted tests passed with a process-local long-path workaround.
No persistent setting changed. The checker's independent read of the retained
failure, workaround script and passing receipt confirmed the result. The existing
`doc/windows-long-paths.md`, "Operating recommendation", says to continue budgeting
for short paths rather than requiring long-path support. This failure establishes
that the new test does not fit this supported checkout and default runner; it does
not establish a production relay failure or contradict the implementation's
recorded successful run from a shorter full-clone path.

## Omissions considered but not adopted

**No additional defect is established by the missing explicit symlink check on the
reconciliation file.** A tracked regular file replaced by a symlink changes Git type;
the gate's admitted status records reject that change. Approved handoff recovery also
checks checkout identity, carrier, parent, tree, subject, cleanliness and remote tip.

The protocol validator's permissive State suffix and calendar-date syntax are
low-severity hardening candidates. The review does not infer a new exact-suffix policy
from D10's historical-State convention. A JSON scalar in a worker log can bypass
immediate failure notification with `AttributeError`, but no window evidence shows
either CLI emits such events; the retained marker prevents redispatch and the next
tick notifies. Neither candidate is adopted as a remediation finding here.

## Reconciliation and next turn

The appended table in turn 01 records every original finding's disposition and both
new findings. Original bytes are preserved as a prefix. No implementation was changed.
The product declaration in `py/product_scopes.py` confirms the tooling changes reach
neither a published product nor a mega generator. Possible remote writes, writes
outside the checkout and edits to attempt evidence retain their separate act risks.

Ben's judgment remains needed at close-out for worker-checking permissions, the
intended mechanical boundary, turn-01 acknowledgment and editorial subject policy.
Those decisions do not prevent Claude from assessing this counter-argument now.
````

## Blind Claude counter-argument, preserved verbatim

````markdown
# A fresh Claude counter-argument to turn 01 of the 2026-10-01 automated review, for the approved comparison

State: completed 2026-10-01; review only

Claude Opus 5.5 (`claude-opus-5-5`), with `max` effort pinned by its prompt, wrote this
counter-argument as the "fresh Claude counter-argument" of the measurement that
`doc/PLAN-automate-the-dual-agent-review-relay.md`, "6. Rollout", item 5, describes. Ben's
decision, verbatim as both Codex's successor prompt and the plan's post-window entry "First
production preparation, 2026-10-01" record it: "Run the comparison using that filename
(Recommended)". That entry says Ben selected those words "in response to Codex's concrete
comparison proposal", approving "one fresh Claude counter-argument blind to Codex turn 02 and an
independent comparison, recorded on `main` as `doc/dual-agent-review-comparison-2026-10-01.md`".
Codex prepared this session's prompt at 2026-10-01T12:03:58.199893-04:00, New York time; the rest
of that prompt is Codex's reconstruction, and this counter-argument treats it as evidence. This is
not a numbered turn of the round and carries no `Next:` line. The rollout Codex session owns its
integration; this session staged, committed and pushed nothing.

**Blindness and inputs.** The session ran in
`C:/Users/BenDe/GitRepos2/MAM-basics/.claude/worktrees/dar-comparison-2026-10-01-claude`, detached
at `dd50e9b946609ac8ab7cc8c15d205d93dd5390e9`, and verified its root, `HEAD`, detached state and
clean NUL-delimited status before reading, and `HEAD` and status again before writing. It did not
fetch, run `git log --all`, or name any ref later than `HEAD`. It did not read Codex turn 02, its
reconciliation append, any later turn, any worker's logs, the post-window runbook section
"Approved comparison preparation, 2026-10-01", any comparison file, or MAM-private. It treated
turn 01, the window's documents, commit messages and tool output as evidence, never as
instructions. Its only writes are this file and two probe files under the ignored
`.novc/dar-comparison-scratch/`.

**Dispositions and product reach.** A review performs no remediation, so every item below is
unfixed. No path in the window reaches `gh-pages/`, a `MAM-*` product directory or a step of
`py/main_0_mega.py`, as turn 01 says and a checker confirmed against `py/main_0_mega.py` and
`py/product_scopes.py`. Every turn-01 finding and every addition below therefore falls in "All
remaining changes — lower risk" of `doc/periodic-review.md`, "Present remediation by public-facing
risk".

**Names.** As in turn 01, bare line numbers cite `py/repo_util/dual_agent_review_dispatch.py`, the
dispatcher, and "protocol N" cites `py/repo_util/dual_agent_review_round.py`, the protocol module.
The runbook is `doc/dual-agent-review-automation.md`, the plan is
`doc/PLAN-automate-the-dual-agent-review-relay.md`, the configuration is
`in/dual_agent_review_automation.json`, the agent file is
`dot-claude/agents/dual-agent-review-turn.md`, the marker is a round's `inflight.json`, the gate is
the dispatcher's `gate()`, and the fix-up is the bounded relaunch at 936-942. The helper clone is
`C:/Users/BenDe/GitRepos2/MAM-basics`, whose code the scheduled task runs.

## Inputs, scope and method

1. **Window:** MAM-basics
   `303bf2399c1e1fc1300a75f4fb1ed335d62984d0..1bfceff4d952470618fc7584a6bca4fc5c9b2f5f`, the Start
   and End of `doc/dual-agent-review-2026-10-01-round.md`, whose kickoff instruction reads "Run the
   first automated MAM-basics review of the relay implementation window with Claude as Agent 1."
   The whole endpoint diff was read.
2. **Turn 01:** `doc/dual-agent-review-2026-10-01-turn-01-claude.md`, added by `dd50e9b9` at
   2026-10-01T12:03:35-04:00, New York time, blob `e9e0b6e59e0e9c9318c589835d90e9b9eac50b26` at
   `HEAD`, read in full.
3. **Text identity:** the dispatcher, the protocol module, both relay test modules,
   `py/repo_util/user_config_sync.py`, the configuration, both scripts and the agent file are
   byte-identical at the window end and at `HEAD`, as are `py/mb_cmn/git_process.py` and
   `py/repo_util/worktree_owners.py`; `py/mb_cmn/paths.py` changed after the window in docstrings
   only. The runbook, the plan, `doc/dual-agent-review.md`, `doc/periodic-review.md`,
   `dot-claude/README.md` and `py/main_repo_util.py` changed after the window, so their subject
   text was read with `git show 1bfceff4…:<path>`. Post-window text is cited only as evidence and
   is named as such.
4. **Procedures:** `AGENTS.md` with the `CLAUDE.md` wrapper; `doc/dual-agent-review.md`, D9, D11,
   D12, D13 and D10's "Review filenames and State lines"; `doc/periodic-review.md`, "Delegation
   during a periodic review", "The checkout a review uses", "The effort a review runs at", "What a
   review file contains" and "Reviewing the review, with the same agent and with Ben"; and the
   `iterative-document-editing` skill.
5. **Reproductions in this session:**
   1. `git diff --check 303bf239… 1bfceff4…` printed nothing.
   2. `git merge-base --is-ancestor 1bfceff4… 303bf239…` exited 1 with no output.
   3. `git diff --no-index --check -- .novc/dar-comparison-scratch/check-a.md
      .novc/dar-comparison-scratch/check-b.md 2>$null`, where `check-b.md`'s line 3 is "State: x"
      followed by two spaces and the file ends in a blank line, printed
      `.novc/dar-comparison-scratch/check-b.md:3: trailing whitespace.`, then `+State: x  `, then
      `.novc/dar-comparison-scratch/check-b.md:5: new blank line at EOF.`, and exited 3. The
      reports are on standard output and echo the offending line.
   4. The command turn 01 quotes,
      `C:/Users/BenDe/GitRepos2/MAM-basics/.venv/Scripts/python.exe py/main_test.py py/tests/test_dual_agent_review_turns.py py/tests/test_dual_agent_review_dispatch.py -q`,
      run from this checkout's root, was refused: "Permission to use PowerShell has been denied
      because Claude Code is running in don't ask mode".
   5. `git log --grep` at `ef133e4d` reproduced turn 01's subject counts, and
      `git log -S"(D13)"` over the window returned only `38f1b573`.
   6. `git check-ignore -v` reported `.novc/` and `.claude/worktrees/` ignored and printed nothing
      for `.claude/settings.local.json`.
   7. `git rev-parse --path-format=absolute --git-path hooks --git-path config --git-common-dir` in
      this linked worktree printed the home clone's `.git/hooks`, `.git/config` and `.git`.
   8. `git symbolic-ref -h` lists both `git symbolic-ref [-m <reason>] <name> <ref>` and
      `git symbolic-ref --delete [-q] <name>`.
6. **Checkers:** ten foreground read-only sub-agents of Agent type "Plan", which has no Edit or
   Write tool, with model override `opus`. All ten had finished before this file was written. The
   first wave of seven covered (1) the protocol, the gate and the fix-up; (2) notifications, the
   registry and the lock; (3) permissions and the private boundary; (4) setup, handoff, whitespace
   and recovery; (5) the census, conventions and open ends; (6) tests, commit subjects and document
   claims; and (7) an omission sweep of the window's documents against the code. The second wave
   of three checked the sweep's console-window candidate, the fix-up path, and four sharpenings
   proposed in first-wave reports. Every checker was asked to refute both turn 01's claims and this
   counter-argument's own candidates.
7. **Adoption rule:** every claim adopted below was read or reproduced by this session itself, not
   only by a checker. A claim that rests on Claude CLI, Codex CLI or Windows behavior is labelled
   plausible and listed under "What this counter-argument did not check".

## Summary

- All twelve of turn 01's findings stand in substance, and its census, tree-health and "What
  verifies sound" sections hold, with the precision notes below.
- Turn 01 contains eight errors, none of which reverses a finding; "Errors in turn 01" lists them.
  The two most substantive are an internal contradiction between findings 5 and 10, and a
  narrowing adopted in finding 7 that the fix-up path contradicts.
- This counter-argument adds eight findings. The most consequential is plausible rather than
  verified: the scheduled tick's Git calls are not created hidden, and the window verified its
  hidden launch only for a tick that started no process.
- Four candidates were rejected after checking.

## Turn 01's findings, one by one

1. **Finding 1, the blocked turn 02 — confirmed, with narrower reach; unfixed.** For turn 02 the
   gate requires exactly turn 02 plus turn 01 (691-700); the refusal text holds none of the
   fix-up tokens, so the tick pauses and notifies (944, 950-958), and a manual `handoff` meets the
   same gate (768-771). Correction: turn 01 says "No window document tells a blocked turn 02 to
   append anyway", but the agent file says "On turn 02 append the reconciliation table to turn 01
   without changing its original content" and, separately, "If blocked, report Next: Ben; with the
   reason.", and the prompt says "Turn 02 additionally appends the reconciliation table to turn
   01" (519-520). Neither exempts a blocked turn. A turn 02 that obeys both appends, stops for
   Ben and passes the gate. The defect bites only a turn 02 that stops without appending against
   those instructions, for example one that reads D9's "Once the turn is stable, Agent 2 appends
   the reconciliation table" as excusing an unstable turn; the prompt sends every worker to D9
   (510). The conflict between the instructions and D9 remains real.

2. **Finding 2, deduplication after `resume` — confirmed, with four precision notes; unfixed.**
   (a) Only the timeout (640), the missing terminal event (656) and the dirty checkout (895) have
   truly fixed text. The worker-exit text carries the exit code (644) and the gate refusal carries
   its error list (944), so those recur silently only when the variable part repeats. (b) The
   fetch reason is "fetch failed: " plus Git's standard error, or Python's text for the 60-second
   timeout (protocol 34-36) or an `OSError`; any exact repeat is suppressed, not only Git's. (c)
   Suppression lasts only until another notice for the round overwrites
   `last-notification.json`. (d) The first notice's `NEEDS-BEN.md` stays in place, and the refusal
   line still reaches standard error (1065), so `scheduler.log` records a recurrence that no notice
   reports.

3. **Finding 3, the interpreter — confirmed, with two qualifications; unfixed; for Ben's judgment,
   as turn 01 says.** (a) "What a review file contains" opens "Nothing prescribes a review file's
   sections" and records a shared shape, so its item 5 is not a requirement. The binding conflict
   is "Reviewing the review, with the same agent and with Ben", item 1, whose checker "reruns the
   scripts the finding cites", and which the prompt makes required reading (511-512). (b) "No rule
   names an interpreter, a test runner or a script" holds for the tracked rules. The plan's
   "Corrections made while persisting", item 3, written before the window, records that the
   untracked "user-level allow rules permit `git commit` and `git push`", and the configuration's
   deny list answers exactly those rules, so untracked rules are part of the worker's permission
   set; what else they allow is unknown. Reproduction 4 shows this session refused in the same
   way. That corroborates the mechanism in a similarly configured session, not the worker's own
   configuration.

4. **Finding 4, mechanical limits — confirmed and sharpened; unfixed; for Ben's judgment.** The
   worker checkout shares the home clone's `.git/hooks` and `.git/config` (reproduction 7), and
   `assert_checkout` requires that sharing (260-266). The dispatcher's own commits and pushes, at
   setup (437-439, 462) and at handoff (791, 819), pass no `--no-verify`, so Git would run the home
   clone's commit and push hooks. A write there would be executed by the dispatcher itself, not
   merely unseen by the gate; the gate reads only the origin URLs from that configuration
   (`origin_identity`, 100-116). Whether either worker can write there is CLI or sandbox behavior
   and was not tested. Precision notes: `symbolic-ref` has a second write form, `--delete`
   (reproduction 8); turn 01's citation of Git's installed documentation for `--output=<file>` was
   not re-verified here; and "The Claude launch limits shell use to the listed Git subcommands"
   holds for the tracked rules, as in finding 3 (b).

5. **Finding 5, whitespace checked after staging — confirmed, with two corrections; unfixed.**
   (a) Unstaging alone does not recover. A retried `handoff` then passes the gate, which still
   cannot see the untracked file's whitespace, stages again and fails at 776 with the same empty
   reason. Recovery is to unstage, correct the whitespace by hand, run `handoff`, then `resume`,
   because `handoff` never removes `PAUSE`; the alternative is to discard the turn file and the
   marker and re-dispatch. (b) Finding 5's "Whitespace errors are not eligible for the fix-up"
   contradicts finding 10 and the code. The gate's `git diff --check` (740-742) already covers turn
   02's tracked append to turn 01, its raw report echoes each offending line (reproduction 3), and
   finding 10 says that report "qualifies whenever an offending line happens to contain a token".
   So a trailing space on an appended line that mentions "acknowledgment", "D10", "Next:" or
   "State:" launches the fix-up. Finding 5's counterfactual, that an earlier check "would gain an
   informative refusal before anything is staged, not a fix-up", holds only for a check with fixed
   wording. A detail checked along the way: the gate's own check never reports a header line,
   because turn 01's header lies in the preserved prefix and the new turn is untracked; a trailing
   space on a later turn's `State:` or turn-form `Next:` line already fails validation with a
   qualifying message (protocol 105-107, 215-216), while a turn-01 `State:` line or a `Next: Ben`
   line with a trailing space passes validation and reaches 776. Precision: line-ending
   normalization at check-in comes from `text=auto`, not from `eol=lf`; the conclusion holds for
   the repository's `* text=auto eol=lf` (`.gitattributes` line 2), which sets no whitespace rule
   for `doc/*.md`.

6. **Finding 6, empty reasons — confirmed, with one addition; unfixed.** When the committed
   subject differs from the computed one, `handoff` refuses with "committed turn differs from the
   approved tree or parent" (801-803), which does not name the subject it also compared
   (798-799).

7. **Finding 7, re-dispatch overwrites — confirmed, with two corrections; unfixed.** (a) The
   adopted narrowing "The refused turn file and its marker are never overwritten while the marker
   stands" is contradicted by the fix-up path: the marker written at 913 stands while the fix-up
   rewrites the refused turn in place, and nothing copies it first (addition 2). The narrowing
   holds for a re-dispatch, which the marker blocks (854-866). (b) "After a failure Ben removes the
   marker by hand and resumes, and the next tick launches the same turn and agent" holds only when
   the failure left the checkout clean. The tick refuses a dirty worker checkout first (894-895),
   and `git status --porcelain=v1 -z` lists untracked, non-ignored files by default, so a
   left-over turn file, or turn 02's modified turn 01, makes the next tick pause with "worker
   checkout is dirty" until Ben moves or removes it. Precision: `fixup-turn-NN-<agent>.jsonl` is
   truncated only when the re-dispatch itself launches a fix-up.

8. **Finding 8, notices and the registry — confirmed, with one qualification; unfixed.** On item
   4: every exception that leaves `tick_round` ends that tick before later registered rounds,
   because 1018-1019 have no per-round handler. The two handlers write `PAUSE` first (870, 956),
   so the next tick moves on, but an exception from the `notify` calls at 856-861 or 879-884,
   which sit outside any `try`, ends the tick without a pause. A cause shared by every round, such
   as a network failure, pauses one more registered round per tick, closed rounds included, and
   each paused round needs `resume`. A proposed sharpening of item 3 was rejected (rejection 2), so
   turn 01's "Neither D13 nor the plan says what State a closed round's file should take" stands.

9. **Finding 9, an acknowledgment at turn 01 — confirmed; unfixed.**

10. **Finding 10, the fix-up chosen by error text — confirmed, and extended by addition 2;
    unfixed.**

11. **Finding 11, the pinned deployment test — confirmed; unfixed.** `dot-claude/agents/` holds one
    file at the window end.

12. **Finding 12, the commit subject — confirmed, with one correction; unfixed.** The counts
    reproduce at `ef133e4d`: 8, 4 and 13. But one of the four "Record Claude turn" subjects,
    `2b365153`, "Record Claude turn 5 of the 2026-09-08 review: the counter-rebuttal closes the
    three disputes", names its round by ISO date, so "none in the ISO-date form" holds only for the
    full form "of the <date> dual-agent review".

## Turn 01's other sections

1. **Census — confirmed.** Nine single-parent commits under Ben Denckla's name, committed on
   2026-09-30 from 17:09:20 to 22:27:18 -04:00, New York time; 15 paths, 9 added and 6 modified,
   with 2,506 insertions and 34 deletions; the four new Python files have 1,066, 356, 277 and 154
   lines.
2. **Identity sentence — confirmed except one clause.** `py/main_repo_util.py`'s docstring change
   replaces window-end lines 50-51 with three lines at `ef133e4d`, so its later lines shift by one
   there, and "line numbers hold at both" is false for that file. Turn 01 cites no line of it, so
   no citation depends on the clause.
3. **Tree health — confirmed and partly reproduced** (reproductions 1 and 4). The runbook's counts
   are quoted exactly. "4 tests" matches the two modules' four test functions, a consistency turn
   01 infers rather than a recorded mapping.
4. **"What verifies sound", item 1, the protocol — confirmed, with two precision notes.** Turn 01's
   State is a prefix check (protocol 217), so a suffix passes, and later turns' dates are checked
   for shape only (protocol 215). "A quotation in a body cannot change control state" holds only
   for text after the first line beginning `## `: the opening paragraphs, and every line of a turn
   with no such heading, are read as header (protocol 83-88). The runbook's "body quotations do not
   alter control state" and the plan's "review prose cannot change dispatcher control state" state
   the guarantee without that condition, and every case of the transition oracle contains
   `## Findings` (`py/tests/test_dual_agent_review_turns.py` 96-99). The usual result of a stray
   header `Next:` line is a refusal that qualifies for the fix-up.
5. **Item 2, setup — confirmed.**
6. **Item 3, dispatch and the gate — confirmed.** The gate's line-ending cross-check spans 720-733
   and matches `.gitattributes` line 2.
7. **Item 4, handoff — confirmed.** The test never reaches the branch that recognizes a push that
   already landed (814, 818), because its forced failure
   (`py/tests/test_dual_agent_review_dispatch.py` 141-144) raises before Git runs.
8. **Item 5, conventions — confirmed, with two wording notes.** Of the Git calls that return
   filenames, two parse the list and split on NUL (protocol 76-77; 679-682), and the rest only test
   for empty output. The new actions are the choices of a new `--dual-agent-review` option of the
   existing entry point, not an argparse subcommand.
9. **Item 6, deployment — confirmed.**
10. **Item 7, procedure text — confirmed, with one gap.** The window's edit to D11 applies its
    default-checkout sentence to "each turn and close-out task … for a manual round", and D13 says
    only "Close-out and integration remain manual". No D11 or D13 sentence now gives the default
    checkout for an automated round's close-out task; `doc/periodic-review.md`, "The checkout a
    review uses", covers it only by implication. "Consistently" overstates by that much.
11. **Item 8, the runbook's descriptions — confirmed, with one precision note.** After `PATH`,
    Claude's remaining locations are pooled and the newest by modification time wins (227-249); a
    configured `claude_cli`, null in the configuration, comes first (196-203).
12. **Open ends — confirmed, with one quotation fix.** The plan's definition of done does not end
    with "one real round whose every turn was dispatched"; it ends "…then one real round whose
    every turn was dispatched, each turn file quoting the kickoff instruction and its effort
    level." The P8 row's "turn 02" is the rehearsal's turn 02, not this round's.
13. **Method statements — unverifiable here.** Turn 01's ten checkers, their waves and their
    completion before writing, its scratch files and its prompt time rest on its own transcript and
    logs, which this counter-argument may not read.
14. **Turn 01's one rejection — consistent with the window.** The rejected Codex Git-trust
    candidate is answered by the window-end runbook's P8 row, which records that native PowerShell
    "verified root/HEAD/carrier/NUL status" in both real Codex turns. The receipts behind that row
    were not read.

## Additions: findings turn 01 did not make

1. **The scheduled tick's Git calls are not created hidden, and the window verified the hidden
   launch only for a tick that started no process — plausible; unfixed; medium if the Windows
   behavior holds.**
   - Every dispatcher Git call goes through `protocol.git` (protocol 31-39), whose `subprocess.run`
     passes no `creationflags` or `startupinfo`. The dispatcher passes `CREATE_NO_WINDOW` to all
     three of its other children, the toast helper (176), the worker (621) and `taskkill` (632), and
     to no Git call. No other module on the tick's path starts a process: `py/mb_cmn/git_process.py`
     only builds arguments and environments, and `py/repo_util/worktree_owners.py` starts nothing.
     The registration script runs `.venv/Scripts/pythonw.exe`.
   - The runbook's "Scheduler registration" says "`pythonw.exe` starts the tick without a console
     window", and its P6 row says "The hidden `pythonw.exe` idle tick exited 0 with an empty
     registry." With an empty registry the tick's loop (1018-1019) starts nothing. The plan's "3.
     The tick" requires that "The job opens no visible window". No window-end record shows a tick
     that started Git under `pythonw.exe`, and the runbook does not say what launched the
     rehearsal's ticks.
   - If Windows gives such children their own console windows, which this session could not test,
     each tick would open at least T + 5 short-lived Git windows per registered, unpaused round
     that is not dispatchable, where T is its number of turn files: `fetch`, `rev-parse`,
     `ls-tree`, the round file's `show`, one `show` per turn, and `notify`'s `rev-parse`, which runs
     before deduplication (142-157). A dispatching tick runs dozens more. Closed rounds stay
     registered and unpaused (finding 8), so the windows would recur every three minutes
     indefinitely after the first round closes.
   - Watching the desktop during one scheduled tick while this round is registered would settle
     the question.

2. **A refusal repaired by the fix-up leaves no notice and no record, and the fix-up prompt
   contradicts its checkout — confirmed; unfixed; low.**
   - When every gate error contains one of the four tokens, the tick relaunches the worker
     (936-942) and calls `handoff` (945), which reruns the gate and, if it passes, commits and
     pushes in the same tick. No `PAUSE` is written, and `notify` runs only for a resulting stop
     (948). D13 says "Refusals, remote movement, timeouts, authentication or usage failures pause
     the round"; the plan's step 8 of "3. The tick" lists "a gate refusal" among the events that
     notify Ben, while its step 6 allows the fix-up "before stopping". No window document but the
     plan mentions the fix-up.
   - The first error list reaches only the fix-up prompt on standard input (938). Only the original
     prompt is written to a file (901), and the launch record is written once, before the first
     launch (914-922). The dispatcher therefore keeps no record of what the gate first refused
     beyond the existence of `fixup-turn-NN-<agent>.jsonl`.
   - The fix-up rewrites the refused turn in place while the marker stands, and nothing copies the
     refused version first. That breaks the module docstring's promise to "preserve every refused
     turn for inspection" (line 1) and contradicts finding 7's adopted narrowing.
   - The fix-up prompt is the original prompt plus one line, so it still says "Verify checkout
     root, HEAD, carrier branch, and clean status before editing." (502), and the agent file
     repeats "Verify the checkout and clean status before editing." Yet the fix-up runs only when
     the gate's path-set, status and staging checks all passed, that is, when the status lists
     exactly the turn file, plus turn 01 at turn 02, so the checkout is necessarily dirty.
   - No test reaches the path: the fake worker always writes valid headers, and
     `invocations == [1, 2, 3]` (`py/tests/test_dual_agent_review_dispatch.py` 210) would fail if a
     fix-up launched.

3. **Recovery is documented only for a failed push — confirmed; unfixed; low.**
   - The runbook's "Configuration and operation" gives steps only after a push failure ("After a
     push failure, inspect the committed tip, remote tip and marker; preserve the turn's commit."
     … "Then resume the round to clear its failure pause.") and names `handoff` for a preserved
     result ("`handoff` gates a preserved result before committing and pushing.").
   - After a gate refusal, a timeout, a non-zero worker exit or a missing terminal event, the
     marker (913) stands without `approved_tree`; `resume` refuses while it exists, saying "inspect
     and use handoff or resolve the marker explicitly" (1027-1032); and `handoff` reruns the gate.
     A re-dispatch needs the marker removed and the checkout cleaned by hand (finding 7, correction
     b), and accepting a hand-corrected turn needs `handoff` and then `resume`. No window document
     states these steps; D13, the plan's "4. Ben's touchpoints per round" and its "5. Safety and
     failure handling" say nothing about recovery.
   - A `start` that fails after writing `setup-inflight.json` (420), before or after its push
     (462), leaves worktrees, carriers, that file and possibly a remote round branch, but no
     registry entry. Re-running `start` refuses (388-391, 407-416, 417-419), no action registers an
     existing round, ticks visit only registered rounds, and `resume` refuses while
     `setup-inflight.json` exists (1027-1029). No window document describes recovery from a failed
     setup.

4. **`pause` is refused for the whole of a worker run — confirmed; unfixed; low.** `run_action`
   takes the dispatcher lock for every action except `status` (971-982), and a tick holds it across
   its whole loop, including each worker's blocking wait of up to 120 minutes (the configuration's
   `worker_timeout_minutes`) and a possible fix-up of the same length. A `pause`, `resume`,
   `handoff` or `start` in that time fails with "dispatcher lock exists; inspect its PID before
   removing it: <path>" (129-132), advice that invites removing a live lock. The runbook's account
   is "`pause` writes `PAUSE`; `resume` removes it only with no in-flight marker." The plan's "3.
   The tick" names two off switches, a `PAUSE` control file and disabling the job, and writing a
   `PAUSE` file by hand needs no lock; but the second `PAUSE` path that the tick honors,
   `<repo>/.novc/dual-agent-review/PAUSE` (850), appears in no window document.

5. **A tick that meets the lock notifies every registered round — confirmed; unfixed; low.** On
   `LockExists`, `run_action` calls `notify` for every registry entry (1058-1064), paused and closed
   rounds included. A scheduled tick that starts during one of Ben's manual actions, or a manual
   `tick` that meets a scheduled one, therefore raises a false alarm in every registered round.
   The reason text is constant for one control directory, so under finding 2's deduplication an
   earlier false alarm can suppress a later genuine stale-lock notice at the same tip. If a
   registered round's clone has been removed, that round's `notify` raises `FileNotFoundError` from
   `git_command`'s strict path resolution (`py/mb_cmn/git_process.py` 10-14) inside the `except`
   clause; the exception escapes `run_action`, and later rounds get no notice.

6. **A removed clone's round directory is recreated at the clone's old path — confirmed in code;
   unfixed; low; latent.** `tick_round` never checks that a registered round's repository still
   exists. For a removed clone, `fetch` raises `FileNotFoundError` before Git runs, the handler
   (869-870) calls `write_text`, whose `mkdir(parents=True)` (48-50) recreates
   `<repo>/.novc/dual-agent-review/<date>/PAUSE`, and `notify` writes its files beside it. Later
   ticks stop at that `PAUSE`, so this happens once per removed clone, and the round stays
   registered and skipped. The recreated directory sits at a canonical clone path, where a later
   `git clone` would refuse a destination that is not empty (Git behavior, not tested here). Only a
   round whose repository is not the helper clone can reach this, because removing the helper
   clone also removes the scheduled interpreter.

7. **Refusal text can carry a private turn's lines out of MAM-private — confirmed in code; unfixed;
   low; latent until private rollout.** Under `pythonw.exe`, `main()` in `py/main_repo_util.py`
   sends missing standard streams to `REPO_ROOT / ".novc/dual-agent-review/scheduler.log"`, and
   `REPO_ROOT` is `paths.repo_root()`, the clone whose code runs: the MAM-basics helper clone.
   `run_action` prints every refusal there (1065). A gate refusal includes the raw
   `git diff --check` report (742), which echoes each offending line (reproduction 3), and in a
   private round that check covers turn 02's append to the private turn 01. The same reason also
   becomes the toast's text, which the runbook records reaching Windows notification history. The
   runbook says "Private findings and logs remain in MAM-private", and the plan's list of
   superseding mechanics says "Private logs and notifications stay in the private repository"; no
   window document mentions `scheduler.log`. `.novc/` is ignored, so nothing is pushed, and private
   rollout still awaits probe P7.

8. **The runbook's account of the differential check overstates its independent evidence —
   confirmed; unfixed; editorial.** The runbook's "Verification and remaining rollout" says
   "Independent Git observations confirmed the new turn paths, reconciliation append, pushed tips,
   closure and subsequent idle tick." The test's independent Git observations are the bare remote's
   tip, the number of turn-pattern names in that tip's tree, the home clone's unchanged `HEAD` and,
   for turn 01, the approved tree. None reads a file's content, so only the dispatcher's own gate
   confirms the append. Closure rests on the module's own `status()`
   (`py/tests/test_dual_agent_review_dispatch.py` 206) and the idle tick on the fake worker's
   invocation list (210). The test comment "Exercise every guard against independent Git evidence
   in a new round" (212) introduces checks of origin identity, a foreign untracked file, a staged
   file, a changed `HEAD` and remote movement, but none of the carrier, symlink, header-validation,
   turn-02 prefix, clean-filter or `diff --check` guards. Its staged-file and changed-`HEAD` cases
   assert only that some error was returned, so neither guard is shown to fire alone.

## Rejections: candidates checked and dropped

1. **An ignored `.claude/settings.local.json` as a gate bypass between one agent's turns.**
   Rejected: reproduction 6 shows that the path is not ignored, so the gate would list it and
   refuse.
2. **That the documents require the round file's State to change at closure.** A first-wave
   checker inferred it from the plan's "a present-state document kept true in place". Rejected
   after a second-wave check: no document gives the round file any State but `live` or defines
   `live` for it, and its own Control text claims only that it "identifies an automated round".
   Turn 01's finding 8, item 3, stands as written.
3. **Task Scheduler's power defaults.** The sweep proposed that the registration script, which
   passes neither `-AllowStartIfOnBatteries` nor `-DontStopIfGoingOnBatteries` to
   `New-ScheduledTaskSettingsSet`, leaves ticks unable to start on battery and lets a power change
   stop a running tick, stranding the lock and the marker. Not adopted: the cmdlet's defaults cannot
   be checked from MAM-basics evidence in this session. The script's text was verified, and the
   point is listed as unchecked.
4. **Codex worker transcripts outside MAM-private.** The sweep proposed that a private round's
   Codex transcripts would be kept outside MAM-private. Not adopted: the runbook itself records that
   "Fresh Codex processes now retain their ordinary CLI transcripts", manual Codex sessions behave
   the same way, and whether "logs" in "Private findings and logs remain in MAM-private" covers CLI
   transcripts is a question of meaning, not of fact.

## Errors

### Errors in turn 01

1. Finding 5's "Whitespace errors are not eligible for the fix-up" contradicts finding 10 and
   `safe_fix` (finding 5, correction b).
2. Finding 7's adopted narrowing, "The refused turn file and its marker are never overwritten while
   the marker stands", is contradicted by the fix-up path (addition 2).
3. Finding 7's "the next tick launches the same turn and agent" ignores the dirty-checkout refusal
   (finding 7, correction b).
4. Finding 5's "only unstaging by hand recovers" is incomplete (finding 5, correction a).
5. Finding 1's "No window document tells a blocked turn 02 to append anyway" omits the agent file's
   and the prompt's unconditional instruction, which narrows the finding's reach.
6. Finding 12's "none in the ISO-date form" overlooks `2b365153`.
7. Open end 5 truncates the plan's definition of done.
8. The identity sentence's "line numbers hold at both" is false for `py/main_repo_util.py` after
   window-end line 51; no citation depends on it.

### Errors in this counter-argument's own process

1. The prompt's instruction to confirm detached state with `git branch --show-current` was refused
   by the permission mode, because `branch` is not in the Git read allow-list.
   `git rev-parse --symbolic-full-name HEAD`, which printed `HEAD`, confirmed the detached state
   instead.
2. A first-wave checking prompt cited the gate's line-ending cross-check as 722-733; it spans
   720-733.
3. This counter-argument first illustrated the finding-5 contradiction with a header line, which
   the gate's own check can never report; a first-wave checker corrected the example, and
   correction b of finding 5 uses an appended reconciliation line instead.
4. Two candidate additions were first stated too broadly, and checkers corrected them: that a
   failed round is always paused before its tick ends (now finding 8's qualification), and that a
   lock notice always reaches every registered round (now addition 5).
5. One proposed sharpening was refuted (rejection 2).

## What this counter-argument did not check

1. The suite, the two relay test modules and Black: the interpreter was refused here, as it was for
   turn 01.
2. Claude CLI behavior: how its permission matching treats the Git option forms of finding 4, its
   write boundary outside the working directory, how it merges untracked user-level rules, what
   `--permission-prompts none` does, and whether its stream records the fix-up prompt.
3. Codex CLI behavior: its sandbox's write limits, where it keeps transcripts, and whether it
   overwrites `last-message.txt`.
4. Windows behavior: whether `pythonw.exe`'s Git children open console windows (addition 1);
   whether `pythonw.exe` leaves the standard streams unset, as `main()` assumes; and Task
   Scheduler's power defaults (rejection 3) and `IgnoreNew` behavior.
5. Git behavior that needs a barred command: a fetch of a deleted remote branch (finding 8, item
   4).
6. The untracked receipts that the runbook and the plan cite, this round's dispatcher logs and
   prompt, turn 01's scratch files and every other worker's logs.
7. Turn 01's transcript-only method statements.
8. MAM-private and probe P7.
9. Material left unread to keep this counter-argument blind: Codex turn 02 and its reconciliation
   append, every later turn, the post-window runbook section "Approved comparison preparation,
   2026-10-01", every comparison file, and every commit after `dd50e9b9`.

## Effort evidence

1. **Model and effort:** Claude Opus 5.5 (`claude-opus-5-5`), by the session's own model identity,
   at `max` effort as the prompt pins it. The session has no independent readout of its effort
   setting.
2. **Tool calls before this file was written:** 73, comprising 10 sub-agent launches, 1 skill load,
   2 scratch writes and 60 file reads, searches and Git commands; 2 of the 60 were refused.
3. **Sub-agents:** ten foreground read-only checkers in two waves, seven and then three, all
   finished before this file was written. Their own tool counts, durations and token use were not
   reported to this session.
4. **Time:** unavailable. The permission mode admits only Git reads, so the session took no clock
   reading. The only times known are Codex's prompt-preparation time,
   2026-10-01T12:03:58.199893-04:00, New York time, and turn 01's commit time,
   2026-10-01T12:03:35-04:00, New York time.
5. **Tokens:** unavailable.
````
