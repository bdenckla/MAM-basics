# November 12, 2026 nightly MAM-basics checks (UTC)

Maintained mega and complete suite pass at `cfdbb64ef8fc24e777d4d296efb7fe4ac966346d`: **66 completed mega steps; 1,449 tests passed, five intentional controls skipped, zero failed**. Taamey D has 61 PASS results, zero FAIL/SKIP, and its release check passes. Its read-only corpus still reports **REFRESH PENDING** (120,425 -> 120,426 cases: one removed, two added, one relabeled); no refresh, baseline acceptance or font build occurred.

Frozen source: `cfdbb64ef8fc24e777d4d296efb7fe4ac966346d`. Receipt parent: `38a7c53ff0fdd3ab77b8cbb9d788ae461a66c16b`. Exact committed isolated checkouts and owning Python 3.13.15 environments were used; requirements/constraints and pip checks passed. Generators/checks ran sequentially. Home and interactive checkouts were preserved.

| Actual command | Exit | Seconds |
| --- | ---: | ---: |
| `/workspace/MAM-basics/.venv/bin/python -B py/main_0_mega.py` | 0 | 515.701165 |
| `/workspace/MAM-basics/.venv/bin/python -B py/main_test.py` | 0 | 396.842201 |

Full arguments, working directories, UTC start/end times, command logs, input identities and output patches are in the [evidence](review-nightly-2026-11-12-evidence.zip) (SHA-256 `02e463c3e555e8600ba7a531248f08b4b93852fe57b490a1403b808f34fcec26`, 81,166 bytes). Every archived payload size/hash and ZIP CRC was verified. Source tips were unchanged since their completed bounded screens, so those reviews were not duplicated. No source repair or source refresh was made.

Eight SVG output differences were preserved before restoration. XML structure, text, IDs, links, colors and all nongeometric attributes agree; differences are numeric geometry, known Times font alias and three longer existing cubic edge routes. Exact before/after bytes, patch, comparison and routing counts are retained. Only those explained files were restored. The suite left no tracked or untracked differences. There was no failed runtime/setup/check attempt in this run.

The five skips are maintained edition-transcription controls for known divergent Wikisource strands, not missing-input tests or native Windows skips. Actual pytest time was 392.99 s (396.842201 s wall). The mega ran both phonetic export/render steps; they are not described as skipped from a stale docstring.

Overall reviewed-through remains `210affe3ac2931473bead0de839be0de08309e3d`; the latest broad-tested source is the frozen commit above. All earlier pending windows, source/browser/editorial limits and immutable receipts remain. Native Windows behavior is unrun: the Git environment helper's Windows safe.directory branch returns early on Linux. A supported owned HP run is a separate next step; no HP action or denied preflight retry was made. Local slots/processes were clear; cross-machine ownership was not independently verified.

The branch is new and isolated, with no dependent owner/deployment. Source and receipt parent have only the same manual-dispatch Pages workflow. No dispatch, main/shared integration, deployment, hbofonts or schedule change. The coordinator reports the next nightly enabled for November 13, 02:00 America/New_York; this run did not change it. Remote verification and cleanup are recorded in the executor closeout.
