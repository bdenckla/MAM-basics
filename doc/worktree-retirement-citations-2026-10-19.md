# Worktree citation optimization evaluation

State: executed 2026-10-19; optional optimization closed by narrow integration

Ben conditionally authorized integrating this optimization if its speed benefit justified
it without losing safety, and explicitly excluded the slow retirement simulation.
Only the seven added lines from
`b85e1885bec90123f3fe8a5f91327619c96fcbbd` were transplanted onto
`c9c0af54feaa49f96bc48ec8296f08e67c796ca1`; the research branch was not merged.

Every candidate must contain `.novc` before the filter is enabled. The line receives the
same `normcase` and slash replacement as the existing matcher. A discarded line therefore
cannot contain any candidate. Mixed reference sets retain the original loop. Citation
membership, ordering, text, line numbers, byte counts and hashes remain equal; deletion,
retention, runtime and execution-simulation gates are unchanged.

Focused verification from an isolated sparse checkout, using the home clone's Python
3.13.15 environment:

```text
/workspace/MAM-basics/.venv/bin/python py/main_test.py py/tests/test_worktree_retirement_citations.py py/tests/test_worktree_retirement_policy.py -q -ra
```

Result: **13 passed in 0.14 s**. Black and `git diff --check` also pass. The maintained
tests use an explicit expected-output oracle and synthetic tracked-file reads, with no
retirement preparation or execution. They cover empty, all-`.novc`, mixed, plain-only and
uppercase reference sets under `posixpath.normcase` and `ntpath.normcase`; forward and
backslashes; case variants; absolute paths and file URLs; missing paths and boundary
lookalikes; file locators `:3`, `:3-5`, `:3–5`, `#L3`, `#l3` and trailing punctuation;
directory boundaries; repeated references and distinct sources; NUL-separated filenames
with spaces/tabs; 500-character clipping; line numbers, byte counts and SHA-256; and
unreadable-file failures.

A throwaway differential harness also loaded the actual baseline collector's function
from the exact main commit above. All ten curated old/new complete-output comparisons,
four unreadable-file checks and four benchmark-dataset output comparisons agree.

The bounded synthetic benchmark calls that collector with 1,000 references and 1,000
lines in one UTF-8 file. References are `.novc/file-NNNN.txt`; relevant lines cite one
such path with `:3-5`, while other lines contain no candidate fragment. Git filename
discovery and reference generation are supplied in memory; file reads and SHA-256 are
still performed. Five timed samples per variant alternate old/new order after one
untimed equality check. Median elapsed seconds on this Linux runner:

| Normalizer | Relevant lines | Baseline | Optimized | Ratio |
| --- | ---: | ---: | ---: | ---: |
| POSIX | 10 / 1,000 | 0.585412 | 0.008593 | 68.1× faster |
| Windows | 10 / 1,000 | 0.735884 | 0.007523 | 97.8× faster |
| POSIX | 1,000 / 1,000 | 0.525800 | 0.511396 | 2.7% less elapsed time |
| Windows | 1,000 / 1,000 | 0.703153 | 0.707448 | 0.6% more elapsed time |

Median process CPU seconds were respectively 0.585359 → 0.008595,
0.735876 → 0.007524, 0.525799 → 0.511397 and 0.703149 → 0.707432.
The sparse-case benefit warrants integration; the small all-relevant variation does not
change the safety argument. These are CPU-matching results, not end-to-end retirement
timings or evidence of faster Git, hashing or retention I/O. Native Windows filesystem
behavior was not exercised. No broad suite, mega or retirement simulation was run;
focused checks match the changed internal function and the controlling review trial.

Before pushing, the sole tracked workflow, `.github/workflows/pages.yml`, was inspected:
it deploys only on schedule or manual dispatch, with no push trigger. No product files
or workflows changed. The user-directed lightweight cleanup applies only to this
session's newly created temporary checkout; user worktrees and HP diagnostics are
outside this task.
