# PLAN — MAM mega-pipeline Phase 13, remediation handoff, and forest retirement

State: Phase 13 complete; the first three remediation waves completed 2026-09-02;
the near-Aleppo census gate was added 2026-09-03

Ben's decision, 2026-09-01: the review should have one final Phase 13 for
whole-pipeline integration and closeout. Phase 13 is followed by a separate
remediation program. The pinned review forest remains read-only during a short
handoff overlap, then its worktrees are retired after a separately named
remediation forest has been created and verified. The review forest is not the
remediation workspace.

This file is the canonical, Git-tracked plan. It is written for a fresh session
with none of the conversation that produced it. At this file's creation, no
tracked Phase 13 or remediation plan existed. The only earlier phase plan was in
the archived Codex task `Review main_0_mega.py code`; that task's phase numbering
was superseded as the review chain encountered new natural boundaries.

## The changed phase numbering

The original scoping task proposed phases 0 through 14. In that proposal,
"Phase 13" meant the accgram surveys and HTML generators, while "Phase 14"
combined the near-Aleppo census, vendoring audit, and final reconciliation. The
executed daisy chain subdivided and renumbered that remaining work. The tracked
reports establish the actual ending:

1. Phase 10 reviewed `near-aleppo-census` and is recorded privately in
   `C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01/MAM-private/doc/mega-pipeline-review-phase-10-2026-09-01.md`.
2. Phase 11 reviewed `gen-site` and is recorded publicly in
   `C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01/MAM-basics/doc/mega-pipeline-review-phase-11-2026-09-01.md`.
3. Phase 12 reviewed `vendoring-audit`, the final registered `StepRecord`, and is
   recorded publicly in
   `C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01/MAM-basics/doc/mega-pipeline-review-phase-12-2026-09-01.md`.

Ben's decision above gives the next sequential label a new, unambiguous meaning:
**Phase 13 is whole-pipeline integration and review closeout.** Do not revive the
original Phase 13 or Phase 14 labels.

## Governing instructions and absolute paths

Before the first repository command, read these files completely:

1. `C:/Users/BenDe/.codex/AGENTS.md`;
2. `C:/Users/BenDe/.agents/skills/worktree-forest/SKILL.md`;
3. `C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01/review-manifest.json`;
4. this plan;
5. `C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01/MAM-basics/CLAUDE.md`;
6. `C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01/MAM-basics/doc/agent-planning-principles.md`; and
7. `C:/Users/BenDe/.agents/skills/hebrew-prose/SKILL.md` before evaluating or
   writing any finding, comment, or report prose about Hebrew accentuation.

The review forest is:

`C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01`

The review manifest is:

`C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01/review-manifest.json`

The borrowed interpreters are deliberately outside the forest because virtual
environments are gitignored:

- pipeline and public tests:
  `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`;
- direct private census checks:
  `C:/Users/BenDe/GitRepos/MAM-private/.venv/Scripts/python.exe`.

Use the forest worktree's script paths and current directory with those absolute
interpreters. Do not create, copy, link, or junction a `.venv` inside a worktree.

## Phase 13 starting evidence to re-establish

The following values were measured on 2026-09-01 before this plan was committed.
They are preconditions to re-measure, not values to trust:

| Repository | Expected checkout before the plan commit | Expected head before the plan commit |
|---|---|---|
| MAM-basics | `review/mega-pipeline-2026-09-01` | `2e96662425a739caee459435d563c646c19efe89` |
| MAM-private | `review/mega-pipeline-2026-09-01` | `3aa273676bdad84e7b78f59abf0a06eda94aa6e3` |
| MAM-parsed | detached | `46209cdf17fee718fb893c63fa34a97e8ab0141a` |
| codex-index-aleppo | detached | `1c12a8ed2382ffad1a7e52874bffa5788f26b80a` |
| MAM-with-doc | detached | `999a4371b1d6cf9bec779b873a4ae87aed997dee` |
| MAM-simple | detached | `cd2bef876312187e21386e4c16c3193a5711a59d` |
| MAM-OSIS | detached | `2f783d1d0b1294491e8187c9016eb904a1acff49` |
| MAM-for-Sefaria | detached | `cf193470f6a33d3ed8157b67c4c92efd594d1e11` |

The plan commit advances only MAM-basics. `review-manifest.json` must preserve
`2e96662` as historical evidence while recording the plan commit as MAM-basics'
new expected head. Do not replace an immutable baseline with a later report or
plan head.

At the same checkpoint, all eight worktrees were clean, both review branches
were synchronized with their matching origin branches, and the six dependency
worktrees were detached. Git's Windows SID ownership check required one exact,
command-local `safe.directory` per worktree; no global Git configuration was
changed.

Phase 12 recorded these further baselines:

1. the complete MAM-basics suite: **971 passed and 5 skipped**;
2. the near-Aleppo census: **87 expected files**, aggregate SHA-256
   `e267f49ad6a1f944ecf1ce884f729179d58f88daea9b7899b5d9f29ef96f2435`;
3. the pipeline registry: **42 steps**, with `vendoring-audit` last; and
4. the cumulative review tally: **89 findings: 15 P1, 33 P2, and 41 P3**.

Write a purpose-named ignored script at
`MAM-basics/.novc/phase13_preflight.py` to read the manifest, run labelled Git
checks with exact process-local `safe.directory` entries, re-count the live
registry, re-hash the 87 census files, and fail on every mismatch. Run it from
the MAM-basics review worktree with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/phase13_preflight.py verify
```

The findings tally cannot be accepted merely because the arithmetic in Phase 12
says 89. Phase 13 must reconstruct the ledger from the sources listed below and
confirm that every finding appears exactly once.

## Sources for the 89-finding reconciliation

The early phase findings live in archived Codex tasks rather than tracked phase
reports. That is the persistence gap Phase 13 must close. Read each task by its
exact id, retain its title verbatim, and copy every accepted finding and coverage
statement into the tracked disposition ledger:

| Phase | Codex task id |
|---:|---|
| 0 | `01a058dd-9bee-7cf0-81ab-66f25ca5edc1` |
| 1 | `01a058e9-01d5-7eb1-8dc0-3b4b3aea9267` |
| 2 | `01a058f8-8fc9-7472-b322-6273e1cd375b` |
| 3 | `01a05920-4473-7551-91cd-a14a942f9282` |
| 4 | `01a05a6f-4724-7882-bdb2-f996f6f77fb1` |
| 5 | `01a05ce1-9938-77b2-a665-4fe7a0f17740` |
| 6 | `01a05cf8-a59f-7a13-9019-3ae6c177e5b0` |
| 7 | `01a05d0f-d3e2-76c2-a9e6-65491df01035` |
| 8 | `01a05d4d-02bf-76d3-b9ce-bfdcee7bb4a8` |
| 9 | `01a05db9-428d-7901-9924-f4dc8121102e` |
| 10 | `01a05df3-0b83-7eb3-9df5-f6f2dccd3d7f` |
| 11 | `01a05e33-6693-7bb2-8865-96f8bb3b9e96` |
| 12 | `01a05e78-0e7d-7321-8f57-6ac9172e2871` |

Phases 10 through 12 also have the tracked reports named above. Treat the
tracked reports as the authority where a task summary and a report differ.

The canonical complete disposition ledger belongs in MAM-private because it
necessarily includes Phase 10's private findings. Write it as:

`C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01/MAM-private/doc/mega-pipeline-review-findings-2026-09-01.md`

Write a public companion in MAM-basics containing only public findings, public
coverage, and the aggregate private counts:

`C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01/MAM-basics/doc/mega-pipeline-review-findings-public-2026-09-01.md`

Do not move private paths, controlled inputs, comparison-project details, or
private findings into MAM-basics merely to make the public companion complete.

For each finding, the complete private ledger records one stable id, original
phase and severity, affected repositories and files, concise evidence, current
status, duplicates or dependencies, recommended root-cause group, and one of:
`fix`, `accept`, `already fixed`, `duplicate`, or `needs Ben's decision`. Preserve
the original severity unless Phase 13 gives an explicit evidence-based reason
for changing it.

## Phase 13A — complete the forest before running the pipeline

The existing eight-repository forest was sufficient for Phases 10 through 12,
but Phase 12's full test run deliberately borrowed verified-clean primary clones
outside it. That does not prove that the eight repositories cover the
complete pipeline's runtime and write graph.

Derive the complete graph from live registrations, subprocess working
directories, supported `REPO_<NAME>_DIR` lookups, `REPOS_ROOT` lookups, runtime
path construction, and every generated-output destination. Imports and pytest
collection alone are insufficient. Record each repository's role as read-only
input, write target, or tool-only dependency.

For every missing runtime input or write target, add a worktree under the same
forest root and update the manifest before the first complete run. Use detached
worktrees for review-only inputs and outputs. Advance a branch only in
MAM-basics or MAM-private when writing an authorized report or ledger. Every
intentional primary-clone fallback must be read-only, clean, pinned to an exact
commit, and recorded with a reason. A program that bypasses a supported path
override is a finding, not permission to let the primary clone fill the gap.

After expansion, rerun `phase13_preflight.py verify`. If any head, branch,
remote, or cleanliness check differs from the manifest, stop and explain the
difference; do not fetch, pull, rebase, reset, or repair it merely to proceed.

## Phase 13B — run the complete pipeline twice

Write an ignored launcher at `MAM-basics/.novc/phase13_runner.py`. The launcher
must set `REPOS_ROOT` and every supported per-repository override to absolute
forest paths, give child Git processes exact process-local `safe.directory`
entries, snapshot every forest member before and after each command, detect any
write outside the forest, and save UTF-8 stdout and stderr under `.novc` rather
than relying on redirected console encoding.

The launcher must invoke the real entry point, not reproduce the individual
steps. Run the first pass with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/phase13_runner.py run-1
```

The first pass inventories every tracked and untracked change by repository,
records generated-file hashes, and reports every cross-step interaction. An
unexpected diff is a finding until explained. Do not bless or commit generated
output merely because the complete pipeline wrote it.

Only after the first pass succeeds, run the same complete pipeline again without
restoring the first pass's generated outputs:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/phase13_runner.py run-2
```

The second pass must add no further content change. Compare complete hashes, not
only stripped text or mtimes. A nondeterministic or continually changing output
is a Phase 13 finding.

Then run the canonical suite through the same forest environment:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/phase13_runner.py tests
```

Re-measure rather than copy the Phase 12 baseline of 971 passed and 5 skipped.
Do not add example-based tests. The complete generated output and its second-run
stability are the primary differential check.

Record hashes and diffs, then restore only the exact review-only output paths
changed by the two runs. Confirm that source files, primary clones, immutable
worktree heads, and every path outside the forest remain unchanged. No
production fix belongs in Phase 13.

## Phase 13C — tracked closeout records

Write the public closeout report as:

`C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01/MAM-basics/doc/mega-pipeline-review-phase-13-2026-09-01.md`

Write a private companion only if the integration run or reconciliation needs
private details:

`C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01/MAM-private/doc/mega-pipeline-review-phase-13-2026-09-01.md`

The public report records the complete public runtime/write graph, exact heads,
commands, output inventory, first-run changes, second-run stability, test result,
public findings, final tally, and what did not change. The private companion
records the corresponding private evidence without leaking it into MAM-basics.

Commit only the plan, reports, and disposition ledgers authorized for each
branch. Push both review branches. Do not merge either review branch into `main`
in Phase 13. Update the local manifest with the immutable original baselines,
every added member, and the final expected report-branch heads. Embed the final
manifest's head/role/exception matrix in tracked reports so forest retirement
does not destroy the only reconstructible record.

Phase 13 is complete only when every worktree is clean, both review branches
have zero outgoing commits, all exact heads match the final manifest, and no
review-only output change remains.

## Remediation program — a different forest and a different purpose

After Ben accepts the Phase 13 closeout report, freeze the review forest: no
fix, formatting pass, regeneration, or issue mutation occurs there. Create a
separately named forest under:

`C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-remediation-<YYYY-MM-DD>`

Give the remediation forest its own `review-manifest.json`, purpose, starting
commits, scratch policy, borrowed interpreter paths, runtime/write dependency
graph, and head-advancement rules. Start from the selected current `main` of each
repository, not from the review forest's old detached inputs. Use branch
worktrees only for repositories scheduled to change in the current remediation
wave and detached worktrees for unchanged dependencies.

Organize remediation by shared cause and dependency, not by mechanically walking
findings 1 through 89. The first grouping pass must at least consider:

1. untracked or undeclared runtime inputs and stale-output set boundaries;
2. swallowed subprocess or Git failures and false-success reporting;
3. sibling-path isolation, override bypasses, and containment validation;
4. partial and non-atomic multi-output writes;
5. deterministic generation, owned-output cleanup, and actionable diagnostics;
6. inaccurate comments, registrations, and generated-output documentation.

Within those groups, P1 findings normally precede P2 findings and P2 findings
precede P3 findings, but an enabling fix may move earlier when the ledger states
the dependency. Re-measure every finding against the remediation forest's own
heads; a moved line number is not evidence that a finding disappeared.

Each remediation wave must have one coherent goal and one natural generated-
output or lint-shaped verification point. At the end of every wave, write back
what changed, commands run, output diffs, unresolved risks, commits, pushes, and
the next wave into the complete private ledger and the public companion where
safe. Merge completed worktree branches into each repository's `main` during
the wave and push `main`; do not leave finished fixes only on remediation
branches. Do not change a GitHub issue's state without an accompanying reason,
and identify agent-written issue comments as agent-written.

## Near-Aleppo census remediation before implementation

Ben's decision, 2026-09-03: the private Phase 10 census remediation is a
precondition of near-Aleppo implementation, not cleanup to perform after the
implementation. This adds a dependency to the remediation program: the census
wave need not precede unrelated remediation waves, but it must finish before
near-Aleppo implementation code begins. The private ledger and the two private
near-Aleppo plans hold the findings and evidence at
`C:/Users/BenDe/GitRepos/MAM-private/doc/mega-pipeline-review-findings-2026-09-01.md`,
`C:/Users/BenDe/GitRepos/MAM-private/doc/PLAN-near-aleppo.md`, and
`C:/Users/BenDe/GitRepos/MAM-private/doc/PLAN-near-aleppo-implementation.md`;
this public plan records only the cross-program ordering and acceptance
conditions.

1. Preserve the pre-remediation expected files byte-for-byte, record an
   aggregate hash, and record the exact heads of every repository the census
   reads. Re-measure the live script and expected-file counts. Do not begin by
   rewriting expected files.
2. Remediate the complete private Phase 10 census finding set. A successful run
   after those repairs establishes runner integrity; it does not establish that
   every census algorithm is authoritative.
3. Run the complete census strictly against the preserved expected files and
   capture every changed result before accepting any new expected file. A
   failure is fatal, and no expected file changes unless the complete run
   succeeds.
4. Map every implementation-driving population and factual branch condition to
   one authoritative current census instrument and expected result. A script's
   inclusion in the census runner does not make a superseded or record-only
   script authoritative.
5. Treat every changed result as a finding. A changed population is reconciled
   in both private near-Aleppo plans and becomes a fatal builder assertion. A
   changed factual premise reopens the particular decision that depends on it
   for Ben; it does not silently rewrite the plan or every expected file.
6. Accept a post-remediation implementation baseline before implementation
   begins. Retain the complete census, expected files and private vendored
   dependencies through the first generated dataset's successful comparison
   with that baseline and the public builder's adoption of the enduring fatal
   assertions. Any later narrowing or deletion is a separate decision.

## Review-forest retirement after the short overlap

Keep the completed review forest read-only only until all of these conditions
hold:

1. the Phase 13 reports and ledgers are committed and pushed;
2. the final manifest matrix is preserved in tracked form;
3. the remediation forest has been created, independently verified, and can
   reach every report and ledger it needs;
4. every useful `.novc` result has either been summarized into a tracked report
   or deliberately classified as disposable; and
5. the review worktrees are clean and hold no outgoing commits.

Then retire the review worktrees from a process whose current directory is
outside the forest. Verify every exact absolute target before removal and use
plain `git worktree remove`, never `--force`. A live Windows process can keep a
worktree directory open; wait for that process to end. Worktree retirement does
not decide the disposition of the local or remote review branches. Branch
deletion, history rewriting, force-pushing, and merging remain separate actions.

Git commits and the tracked final manifest matrix are the archive. The worktree
directories are not the archive.

## Remediation wave 1 — change-log failure propagation (completed 2026-09-02)

Ben approved the MP02-02 and MP02-03 remediation wave on 2026-09-02. The wave
used the separately named forest at
`C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-remediation-change-log-fail-closed-2026-09-02`.
The forest manifest records current-main baselines for MAM-basics, MAM-parsed,
MAM-with-doc, and MAM-private. The MAM-basics and MAM-private remediation
branches first merged the retained Phase 13 review records in commits
`8c00c87a0078f7d6ab250596a6a9693e7db385a9` and
`8375f306114a02f6a497b0b435d78d564bcba060`, respectively.

Remeasurement established that MP02-02 was already fixed by MAM-basics commit
`b403e6df00ec7b9349f06f458b921ca44c2c17fb` on 2026-08-31. An ignored adverse
probe confirmed that failures from `ls-tree`, `show`, `log`, and `rev-list` all
raise instead of producing a successful empty report. No additional MP02-02
production change was made.

MAM-basics commit `db4298e8bd1b9b40fcaf800c2d55db6e51b24abb` fixes MP02-03.
`diff_mpp.generate_report()` now captures the full error list returned by
`mpplus_verify.verify_all()` and raises `VerificationError` before reading commit
dates, creating output directories, or writing JSON and HTML. The verifier keeps
its collect-all contract. The ignored adverse probe forced one verification
error and observed zero JSON writes and zero HTML writes.

Verification used
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`. Black left the
edited production file unchanged. The four focused change-log test files passed
with 37 tests. Real `diff-mpp --all` generation reproduced named-release counts
of 76, 557, 19, 139, and 33. The MAM-with-doc detached worktree remained clean,
so all 16 generated artifacts were byte-identical to the committed files. The
MAM-parsed detached worktree also remained clean.

MAM-private commit `87d8972287961671420c2792459c59cca954d52e` updates the canonical
ledger without changing either finding's severity. The public companion records
the same dispositions. MP02-01 remains open, the empty unpinned report remains
unendorsed, and MP02-07 batch atomicity remains outside the wave. Both forests
remain present pending Ben's next remediation or retirement decision.

## Remediation wave 2 — MP02-01 normalized extraction (completed 2026-09-02)

Ben approved the MP02-01 implementation wave on 2026-09-02. The wave used the
separately named forest at
`C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-remediation-mp02-01-2026-09-02`.
Its current-main baselines were MAM-basics
`e2b5208560e348a06c69d240f38b9f3a20889209`, MAM-parsed
`54ba7e0b2b9db37be6ef1b9f36072cc4eeda9908`, MAM-with-doc
`7834b2d0df0dc8104fd339fb81ae13a9ed0dfcab`, and MAM-private
`1463bc96872b2cd4a57a0c6e690dd91aece6ec1f`. The MAM-private worktree was
created only after unrelated near-Aleppo work left its primary clone clean and
pushed at that final baseline.

MAM-basics commit `9d1c6840f97b32891dd2d0b81ef5d2176f74bd42` fixes MP02-01.
Each revision now supplies its own checked chapter-and-verse normalization map.
Extraction traverses the union of canonical book files, chapters, and verses,
so an old-only or new-only structure is compared against an empty side instead
of disappearing. Duplicate normalized keys, duplicate canonical files,
unmapped keys, unsupported key types, and malformed book-structure counts are
fatal.

The ignored independent check ran as:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/mp02_01_verify.py
```

The check independently read all 218 revisions from `9ce6ee5` through
`54ba7e0b2b9db37be6ef1b9f36072cc4eeda9908`. Both endpoints had 24 files, 929
chapters, and 23,202 verses. The old endpoint had 24,131 Hebrew-string chapter
and verse keys; the new endpoint had 24,131 numeric-string keys. Independent
normalization and production extraction each found 175 changed locations, with
zero disagreements and zero verification errors. Adverse cases established
zero differences for equal content under unlike keys, one difference for
changed content under unlike keys, explicit old-only and new-only file,
chapter, and verse results, and fatal duplicate, unmapped, and malformed input.

Black ran on the two edited Python files through the primary MAM-basics venv.
The focused repository command passed 37 tests:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q py/tests/test_diff_mpp_unpinned_latest.py py/tests/test_mpplus_extract.py py/tests/test_mpplus_file_matching.py py/tests/test_mpplus_latest_note_schema.py
```

The full regeneration command was:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py mpp --all
```

The named-release raw counts remained 76, 557, 19, 139, and 33. The unpinned
comparison reported 175 raw changes; its JSON has 51 records and its HTML has
57 reader-facing change cards. Only `gh-pages/change-log/index.html`,
`gh-pages/change-log/unpinned-latest.json`, and
`gh-pages/change-log/unpinned-latest.html` changed; the other 13 regenerated
change-log artifacts were byte-identical. MAM-with-doc commit
`4397daa6f915f643241290c7b9748dcea61bdd24` records those three artifacts.

MAM-private commit `bd38622ce43fb50ce80022d1559abcb1816d4fcf` updates the canonical
disposition ledger, and the public companion records the same disposition.
MP02-07 batch atomicity remains outside this wave. No GitHub issue state changed.
The investigation and implementation forests remain present pending a later
retirement decision.

## Remediation wave 3 — sever the dated WLC private dependency (completed 2026-09-02)

Ben directed this architectural wave on 2026-09-02 after asking whether the
mega pipeline's dated-WLC generation was the only MAM-basics reach into
`MAM-private/wlc-utils-private`. The approved trade was explicit: the preserved
2025-03-21 outputs may become stale, and severing the runtime dependency is
worth that cost.

MAM-basics commit `d152ec8d7a8757f9ee679900490fa6f48a148c3e` removes the
dependency. `py/main_wlc_json_and_unicode.py` now generates only the public
`wlc420` and `wlc422` families and their public comparisons. The dated release
descriptors and `mb_cmn.paths.wlc_utils_private_dir()` are gone. Follow-up
commit `688bc05a8f7465e013ffb55230193abdf2978267` restores the original
`wlc-utils`/`wlc-utils-private` pair in two generic env-name mapping tests after
Ben clarified on 2026-09-02 that a textual reference is not a dependency. The
tests use repo names and dummy env values only as inert input; the tests perform
no directory existence check or filesystem access. No dated release support or
private path accessor returned.

MAM-private commit `40a7db9ff6ae1235d9f2d45bf44fbac9ffac93be` records the
decision at the private tree's README, at the governing evacuation plan, and in
the canonical disposition ledger. The existing private Phase 8 finding remains
open: severing regeneration does not repair the preserved output and is not
reported as though it did. The accepted disposition here is the risk that those
outputs may become stale.

Verification used
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`. Black
formatted the four edited Python files. The focused path suite passed 14 tests.
The real `py/main_wlc_json_and_unicode.py` entry point exited 0; every public
tracked output was byte-identical, and `MAM-private/wlc-utils-private/in` and
`out` had zero diff. The full MAM-basics suite passed 971 tests and 65 subtests,
with 5 pre-existing skips.

MAM-basics `HEAD` advanced during verification from `a9422f9` to `757aa68` in
concurrent HKQ work. The intervening commit touched four HKQ/render paths and
none of this wave's four paths. The full suite ran on the newer head, staging
named only this wave's paths, and the push was a fast-forward. No GitHub issue
state changed.
