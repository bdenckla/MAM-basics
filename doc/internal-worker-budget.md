# Internal worker budget

State: runbook; current policy and its verification evidence.

`py/mb_cmn/worker_budget.py` chooses a budget when an existing internal pool starts.
The mega runner still executes its steps sequentially. The FOI pool uses this helper;
`--single-threaded` continues to bypass the pool and resource sampling entirely.

The default ceiling is four workers, further limited by the number of tasks, available
logical CPUs, current idle CPU capacity, and estimated memory capacity. Set
`MAM_MAX_WORKERS` to a positive integer to change the ceiling. It does not override the
resource limits. `MAM_WORKER_MIB` changes the estimated memory per worker, normally
512 MiB. Invalid settings fail explicitly when a pool is requested.

CPU capacity is sampled over 200 ms at pool creation. Linux uses `/proc/stat` for the
process's affinity set and also accounts for CPU consumed under visible finite cgroup-v2
quotas. Windows uses `GetSystemTimes`. The idle fraction scales the usable logical CPU
count, and the result is rounded down, with a minimum of one worker. This can choose
three workers on an otherwise lightly loaded four-CPU allocation.

Linux memory detection uses `MemAvailable`, capped by remaining memory under visible
cgroup-v2 limits, including ancestors. Windows uses available physical memory from
`GlobalMemoryStatusEx`. The policy reserves the larger of 512 MiB or one quarter of
currently available memory before dividing by the per-worker estimate. Missing CPU,
load, or memory information imposes a fallback ceiling of two. At least one worker is
allowed for nonempty work; this is not an out-of-memory guarantee.

These are launch-time estimates, not reservations. Concurrent sessions can observe the
same free resources; pools do not resize after launch. The ceiling and headroom reduce
oversubscription but cannot eliminate that race. Windows Job Object limits and Linux
cgroup-v1 limits are not detected. Windows CPU utilization is system-wide rather than
specific to a restricted affinity set. Native Windows execution remains to be checked;
the Windows API success/failure paths have been exercised with mocks on Linux.

The focused policy checks run through the normal entrypoint:

```sh
.venv/bin/python py/main_test.py py/tests/test_worker_budget.py -q
```

No text conversion or Unicode normalization is introduced.

## Measurements on 2026-10-03

Three alternating before/after pairs used Python 3.13.15 on Linux, with five affinity
CPUs and a four-CPU cgroup quota. The policy selected three workers in every FOI run.
The old pool used eight. Median elapsed time increased from 3.885 to 4.379 seconds
(0.495 seconds); median sampled aggregate peak RSS decreased from 438 to 215 MiB.
This is a conservative resource cap, not a single-run speedup. Memory was not the
binding limit in these measurements; available memory after the comparisons was
about 15.3 GiB.

[Raw measurements](internal-worker-budget-measurements.json) include all six runs.
Invocations were sequential, with no other task-owned benchmark or mega running.
The legacy variant substituted the previous fixed count for `choose_workers` while
running the same generator source and inputs; the budget variant used the real helper.
RSS was sampled every 50 ms across the invocation's process session and sums shared
pages more than once. Both timing and RSS therefore include harness limitations.
The commands correspond to `py/main_foi_features_of_interest.py` at base commit
`644a6c9c3203e12e5fe7bdad75b165c16bb9aab5` and this branch's implementation.

FOI's tracked outputs remained byte-identical after the comparisons, a Linux spawn-mode
run, and a real `--single-threaded` run with an intentionally invalid worker-budget
setting (confirming the serial path bypasses configuration and sampling).

The full suite passed: 1,074 passed, five skipped. After making the mocked cgroup path
lookup portable to Windows, all eighteen focused cases passed again. The full public
mega passed in 401.9 seconds, including Phonetic MAM export/render and Yeivin ITM.
Eight SVGs reproduced the previously measured Linux geometry/Times-font-alias
differences: both process-documentation SVGs and the six MAM-parsed call-graph SVGs.
Their XML content agreed after excluding geometry and the font alias, and their bytes
exactly matched the saved Linux baseline. Those platform-only differences were restored
to HEAD; the 4,538-file manifest then matched, with no generated product change retained.
Black and `git diff --check` passed. Native Windows verification is not yet claimed.

## Lightweight native Windows verification

From a checkout of this branch, use its owning environment. The first command covers
the policy and mocked failure cases. The second exercises the actual operating-system
APIs; both memory and CPU counters should be available, and the selected count should
be between one and four with default settings. The final two commands exercise Windows
process spawning and check FOI output equivalence.

```powershell
.\.venv\Scripts\python.exe py/main_test.py py/tests/test_worker_budget.py -q
.\.venv\Scripts\python.exe -c "import runpy; m=runpy.run_path('py/mb_cmn/worker_budget.py'); print('memory:', m['_windows_available_memory']()); print('CPU counters:', m['_cpu_times']()); print('limits:', m['resource_limits']()); print('workers:', m['choose_workers'](39))"
.\.venv\Scripts\python.exe py/main_foi_features_of_interest.py
git diff --exit-code -- gh-pages/MAM-with-doc/foi
```

Record the actual outputs and machine context before calling this native verification
complete. Linux tests that mock Windows calls do not establish it.
