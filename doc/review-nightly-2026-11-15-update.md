# November 15 nightly checks: later Windows coverage

State: open; first entry 2026-11-15

## November 15: HP worker-verified supplement

The passage “Native Windows checks at this source remain unrun here.” now has later
HP worker-verified evidence at exact source
`647ef21ca9d09b1b50264b000cd6a31fd376e572`, after portable checks and slot release.
This cloud publisher records the supplied worker report; it had no HP environment
access or tool control and did not connect to HP, execute these checks or inspect
their raw logs. The base remains completed, with this bounded later coverage and
all other portable limits retained.

The worker used detached checkout
`C:/Users/BenDe/GitRepos3/nightly-windows-20261115`, running from its root with the
owning home interpreter:

```powershell
C:/Users/BenDe/GitRepos3/MAM-basics/.venv/Scripts/python.exe py/main_test.py py/tests/test_worker_budget.py py/tests/test_git_process.py py/tests/test_mb_cmn_provenance.py py/tests/test_worktree_retirement_citations.py -q
```

Worker-reported result: **41 passed in 4.04 seconds, exit 0**. These four modules
require no sibling inputs; the portable run's exact input pins remain unchanged.

From the checkout's `py` directory, the native probe imported
`mb_cmn.worker_budget` and asserted Windows, positive available memory, available
CPU counters, a positive CPU limit, and `1 <= choose_workers(39) <= 4`.
**Exit 0**: memory `2921029632` bytes, CPU counters
`[68683818906250, 71316853906250]`, limits `[20, 2921025536]`, workers `4`.
Separate memory samples are observations, not lasting machine capacities.

The worker reports retained HP home-checkout logs
`.novc/nightly-windows-20261115/tests.txt` (**101 bytes**) and
`.novc/nightly-windows-20261115/probe.txt` (**119 bytes**). Their bytes were not
copied or inspected here; this supplement adds no log archive. The existing
[portable evidence](review-nightly-2026-11-15-evidence.zip) remains unchanged.

The worker reports no Python/pytest/fontforge processes before or after. The
worktree was clean; removal exited 0, its path was absent and only home remained
listed. HP home stayed clean at
`7c5b8f28d5a61091001b8d16426b3d14a860c8e4`. No UI control, main change, HP push,
deployment, font operation, generator, broad duplication or Private Windows check
occurred.

This publication runs no further product or native checks. The supplement does
not establish Windows mega/full suite, renderer, browser, font or Private coverage.
Native scan, OneDrive attributes, scan-root/URI and native-viewer behavior remain
unverified by this four-module/resource-API subset. The four historical orphan-crop
HTML findings, Taamey D corpus/baseline limits, earlier source/browser gaps,
pending windows and all prior receipts remain distinct. Overall reviewed-through
stays `210affe3ac2931473bead0de839be0de08309e3d`; broad-tested stays at the actual
portable source `647ef21ca9d09b1b50264b000cd6a31fd376e572`. No anchor advances
from this supplement. Only the established isolated Basics receipt branch is
updated, directly atop `88ff59f12261e056a1511e4105d117d51a5ceccb`.
