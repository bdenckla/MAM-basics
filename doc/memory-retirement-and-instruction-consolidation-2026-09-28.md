# Memory retirement and instruction consolidation: execution record

State: executed 2026-09-28; the authorized scope is complete through exact deletion-manifest delivery. No memory deletion is approved or performed.
Updates and later status: [memory-retirement-and-instruction-consolidation-2026-09-28-update.md](memory-retirement-and-instruction-consolidation-2026-09-28-update.md).

Codex prepared this sanitized record on 2026-09-28. Ben's instruction was to execute the approved
public proposal and private appendix, complete backup, migration, consolidation, checks,
integration, normal pushes, deployment and disablement, and return the refreshed exact deletion
manifest for separate approval. Ben also said: “Do not delete memories yet.”

## Verified source and development checkouts

| Repository | Source / primary integration | Managed development | Initial verified baseline |
|---|---|---|---|
| MAM-basics | `C:/Users/BenDe/GitRepos/MAM-basics` | `C:/Users/BenDe/.Codex/worktrees/memory-retirement/MAM-basics` | `52f1f6bfce902b1493a6738979aac959841e8f0d` |
| MAM-private | `C:/Users/BenDe/GitRepos/MAM-private` | `C:/Users/BenDe/.Codex/worktrees/3372/MAM-private` | `e781b1accbdf8fb5f94c3a8469b78fd26ab2e86f` |

Origins were fetched before source inspection. Required public commit
`f368a30598e7cb2a6377463d2616b71884a98dda` and required private commit
`e781b1accbdf8fb5f94c3a8469b78fd26ab2e86f` passed the origin/main ancestry gates.
Actual paths, exact HEAD, branch and NUL-delimited clean status were recorded before editing.
The root executor was the sole writer and owned final integration. A read-only sub-agent
checked public proposal coverage and the final public corrections; no private evidence was delegated.

## Implemented scope

The approved public additions P01–P26, N01–N08 and A01–A02 were reconciled against their named
tracked destinations. Covered guidance stayed at its existing authority; obsolete incident and
account observations stayed in the private raw archive. The approved private appendix was
implemented in MAM-private; its content and evidence remain private.

Detailed plan, receipt and non-review State procedures now belong to `iterative-document-editing`;
review naming belongs to `doc/dual-agent-review.md`, “Review filenames and State lines”. Manual
retirement belongs to topology's maintenance reference. Test-shape policy and verification
cadence retain the common body as their authority. Repository exceptions, exact test runner,
product declarations, integration gates and historical rationale remain intact. The standards
checker continues not to validate State shapes; its explanatory routes changed without behavior changes.

`--check-memory-health` and its module were removed. Both pruning skills were rewritten in their
existing canonical directories for plan pruning only, retaining their names and explicit deletion
approval gate. The shared deployment implementation and executable hook behavior were unchanged.
The authored consumer cautions in `MAM-parsed/README.md` were the only product prose edited by this task.

The existing [checkout-kinds plan](PLAN-checkout-kinds-and-portable-knowledge.md), “Workstream B”,
records the approved scope and actual paths. Decisions 4–5 supersede the former account-local
memory exception. Decisions 1–3, 6 and 7, Workstream A, laptop execution and cloud-skill expansion
remain open. No forest, environment-pinning or general future-lessons policy was selected.

## Checks and integration evidence

Black passed on the three changed Python files. Ruff passed with its cache disabled in the managed
checkout. CLI help omits the removed flag; the real entrypoint rejects it before an action runs.
The existing coverage lint passed three tests after the authorized module deletion was staged.
The initial source suite passed 1,021 tests with five declared skips. After merging the concurrent
source updates, the full suite passed 1,011 tests with five declared skips at `b58828c9`.
The later merge changed only an upstream close-out document, so that suite result remains applicable.

The final integration mega passed at `0e6d8a769642a7de239787afca9a7ac8bff01c50`. Git status was clean afterward;
no generated content changed. The only task-owned product delta from the refreshed main was
the planned authored README prose. Concurrent upstream changes were preserved through development
merges. The refused normal public push was retried after merging the new origin/main in development.
A proven unowned empty stale Git lock was retained as private evidence; no work or history was discarded.

Private checks passed `git diff --check`, the retained-archive ignore probe (exit 0), and the
AGENTS non-ignore probe (exit 1). No task-owned private generator, generated output or input changed.
The migrations were fast-forwarded into their primary checkouts and pushed normally:
public `0e6d8a769642a7de239787afca9a7ac8bff01c50` and private `8d72e7070d62d003c87fe63331810804467b98e8`. Ordinary development branches were not pushed.

Canonical instructions and skills were deployed from freshly fetched public origin/main by
`py/main_repo_util.py --sync-user-config`, from public primary with its absolute shared interpreter.
The subsequent `--sync-user-config --check` returned `USER_CONFIG_PROBLEM_COUNT=0`.
Both deployed pruning skills were read and contain plan pruning only. Live instruction files were
not edited by hand.

## Disablement, retained backup and approval boundary

Both original account configurations were verified and retained privately. Unrelated parsed
settings were unchanged. Claude now has `autoMemoryEnabled=false`; Codex has
`features.memories=false`, `memories.generate_memories=false` and `memories.use_memories=false`.
Account, project, managed and launch/environment memory overrides were checked. A fresh Codex
runtime returned all three false values in both primary and development checkouts. A fresh Claude
native control session returned `effective.autoMemoryEnabled=false`, without a memory-key override
or a model call. Its separate authenticated model probe could not run because OAuth had expired;
effective local settings verification succeeded independently.

No Claude memory-writing process was active at final inventory. The existing Codex runtime had no
memory-enabling launch override; fresh pre-change verification had already shown its memory feature
disabled. Fresh verification processes exited before the final backup. The consistent metadata
database backup had zero stage-one outputs and zero memory jobs; that database and its sidecars
are excluded from deletion.

The final snapshot measured 247 files and 617589 bytes across
eight stores, unchanged from the approved inventory. Every source size and SHA-256 matches its
complete private backup. The archive is retained under
`C:/Users/BenDe/GitRepos/MAM-private/memory-retirement-backups/20260928-memory-retirement-a78e/`.
The exact private manifest and backup evidence are recorded in
`C:/Users/BenDe/GitRepos/MAM-private/doc/memory-retirement-2026-09-28.md`, “Exact approval artifact”.
Raw contents, private filenames and private dispositions are not reproduced here.

The executor returns that manifest for Ben's explicit approval. No legacy memory file or index
was rewritten or deleted. Its eight memory directories are separately listed for removal only
when empty after approved file deletion. Changed/new files invalidate the affected approval entry.
Session logs, credentials, account configuration, databases, sidecars, project-key parents and
the retained archive are excluded. Archive disposal requires separate explicit approval.
