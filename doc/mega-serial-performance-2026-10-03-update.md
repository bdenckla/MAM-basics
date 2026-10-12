# Serial mega performance: later status

State: open; first entry 2026-10-12

## 2026-10-12 — approved main integration

Ben separately authorized integrating the completed serial optimizations from
`perf/serial-mega-20261003` at `f01c4c5585622c2a012926b6b2d669ef163c0f86`.
The original receipt's isolated-branch and pending-integration statements describe its
completed October 3 scope; its measurements and verification are unchanged.

The current implementation retains the poetic scanner's guarded fast path and cache,
the regex membership check, and the single canonical-bytes validation. Reconciliation
preserves all five current forbidden characters, including U+05C5, labelled layout markers,
current example-display imports, and later licence completeness checks. It introduces no
top-level parallel execution. The combined mega completes all 60 steps in 435.123 seconds;
its SVG differences are explained and preserved privately. The original suite failures
and their passing decisive rechecks are described accurately in the
[integration receipt](branch-integration-2026-10-11.md).

The maintained speedup plan now records integration. Issue 273's implementation no longer
exists only on a branch. This task changes no GitHub issue state and makes no new controlled
performance claim; issue 272's parallel-mega proposal remains separate.
