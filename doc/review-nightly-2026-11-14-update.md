# November 14 nightly checks: later Windows coverage

State: open; first entry 2026-11-14

## November 14: coordinator-verified HP supplement

The passage “Current-source native Windows checks remain unrun.” is supplemented by
coordinator-verified HP results at exact source
`46ed8dc5ac41fe556b131b7911726c215ab64140`, after the cloud slots were released.
This cloud task publishes the coordinator's summary; it did not execute the HP checks
or independently inspect their raw logs. The base remains completed, with this bounded
Windows coverage and all other scope limits retained.

The detached checkout `C:/Users/BenDe/GitRepos3/nightly-windows-20261114`
ran from its root using the owning home interpreter:

```powershell
C:/Users/BenDe/GitRepos3/MAM-basics/.venv/Scripts/python.exe py/main_test.py py/tests/test_worker_budget.py py/tests/test_git_process.py py/tests/test_mb_cmn_provenance.py py/tests/test_worktree_retirement_citations.py -q
```

Result: **41 passed in 3.90 seconds, exit 0**. These four modules need no sibling
inputs; the portable run's recorded input pins remain unchanged.

From the checkout's `py` directory, a probe imported `mb_cmn.worker_budget` and
asserted `os.name == 'nt'`, `_windows_available_memory()>0`,
`_cpu_times() is not None`, `resource_limits()[0]>0`, and
`1<=choose_workers(39)<=4`. **Exit 0**: memory `2630119424` bytes,
CPU counters `[51668864218750, 53719692968750]`, limits `[20, 2630115328]`,
workers `3`. Separate memory samples are observations, not lasting machine capacities.

The coordinator retained `tests.txt` and `probe.txt` in HP home's
`.novc/nightly-windows-20261114/`; these logs were not transferred to this cloud task.
`Get-CimInstance` found no Python/pytest processes before or after. HP home stayed
clean at `7c5b8f28d5a61091001b8d16426b3d14a860c8e4`. The worktree had no tracked
diffs; `git worktree remove` completed, existence was false, and only home remained
listed. No UI control, HP main change, push or deployment occurred.

No further checks ran for this publication. This supplement claims no native Windows
mega/full suite, renderer, browser, font or Private coverage. The four historical
orphan-crop HTML findings, Taamey D corpus/baseline limits, overall reviewed anchor
`210affe3ac2931473bead0de839be0de08309e3d`, other gaps and prior receipts remain.
Only the established isolated Basics receipt branch is updated.
