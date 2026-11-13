# November 13 nightly checks: later Windows coverage

State: open; first entry 2026-11-13

## November 13: focused native Windows supplement

The base receipt's native-Windows limitation is supplemented at the same source,
`9ed47c6e8999ecaf56031e9b3f524bee6e01507a`. On Bens-HP-mini, an isolated
committed worktree in the Codex-owned GitRepos3 forest used its home clone's
CPython 3.13.15 environment. Requirements and constraints matched the source;
`pip check` passed. Process inventory found no Python or FontForge jobs before
execution. Cloud phases had completed and released their slots.

The maintained entry point ran these platform-sensitive modules sequentially in
one focused invocation, with `-q -ra`:

- `py/tests/test_worker_budget.py`
- `py/tests/test_git_process.py`
- `py/tests/test_mb_cmn_provenance.py`
- `py/tests/test_worktree_retirement_citations.py`

Result: **41 passed in 3.71 seconds**, exit 0. This covers Windows-specific Git
and filename behavior as well as maintained resource-policy fault injection.
An additional read-only probe executed the actual Windows memory and CPU API
paths: available memory 2768482304 bytes, CPU counters 35271738593750 /
36733255937500, detected CPU limit 20, and three workers selected for 39 tasks.
Positive memory, ordered nonnegative counters, and the one-to-four worker bound
were asserted successfully. These sampled resource values are not lasting limits.

No broad cloud phase was repeated. No generated tracked differences, repair,
font generation, baseline acceptance, main integration or deployment occurred.
No private runtime input was used by these focused modules. Historical review
anchors and pending gaps remain unchanged. The interactive home checkout was
preserved. This supplement does not claim native Windows execution of every
portable test or change any private input-blocked result.
