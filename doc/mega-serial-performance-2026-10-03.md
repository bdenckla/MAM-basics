# Serial mega performance, 2026-10-03

State: executed 2026-10-03. Measured improvements and verification are complete on the isolated branch; main integration is not part of this task.

Written by a Codex session on 2026-10-03 under Ben's delegated instruction to investigate,
implement worthwhile low-complexity improvements on an isolated branch, and push without
merging main. Compact timing evidence is in
[the JSON record](mega-serial-performance-2026-10-03.json).

## Implemented changes

- `phonetic_mam.release.read_book` uses the validation already performed by
  `display_schema.canonical_bytes`, instead of validating immediately before that call too.
  Duplicate-key, book-identity, shape, forbidden-character and canonical-byte checks remain.
  The renderer still validates the entire release before writing anything and keeps its
  book-scoped memory use. No persistent data cache or validation-bypass flag was added.
- `display_schema._text` searches a compiled four-character class instead of constructing
  a set from every string. It changes no character and performs no Unicode normalization.
- `accgram.poetic_scanner` uses the prose scanner's existing safe alternation builder to
  bypass the rule loop only where the final token-free catch-all must win. The longest-match
  loop remains intact elsewhere. A separate one-entry cache keys on a tuple snapshot of the
  current poetic rules; unsupported rule patterns retain the full-loop fallback.

## Repeated measurements

Three fresh-process trials per implementation, executed serially in order old, new, new, old,
old, new. Each process runs the four listed grammar stages and then Phonetic rendering in mega
order. Both wall and process CPU seconds are retained in the JSON; they closely agree. Medians:

| Stage | Before, seconds | After, seconds | Saving, seconds |
| --- | ---: | ---: | ---: |
| Phonetic rendering | 33.105 | 26.910 | 6.195 |
| accgram-run-poetic | 1.593 | 1.179 | 0.414 |
| accgram-xcheck-poetic | 1.148 | 0.697 | 0.451 |
| accgram-servi-xcheck | 1.077 | 0.602 | 0.475 |
| accgram-generate-html | 9.319 | 8.937 | 0.383 |

These are individual stage medians, not a synthetic full-run total. Phonetic rendering's
measured reduction is 18.7%. The four grammar stages establish a repeatable benefit independent
of the much longer survey.

A separate all-call differential ran the five stages requested by
[MAM-basics issue 273](https://github.com/bdenckla/MAM-basics/issues/273), including the
post-stress survey. All **26,804** old/new token sequences matched, including token text and
positions. Timed call totals were **4.557 seconds old, 1.589 seconds new**. These include
per-call timing instrumentation; they are not whole-stage benchmark times.

On the **1,539,529 actual display strings** in a complete corpus validation, three alternating
predicate trials gave median 0.580 seconds for set construction/intersection, 0.363 for
`isdisjoint`, 0.228 for compiled regex search, and 0.571 for four containment tests. Regex was
selected only after measuring this hotspot. The differential test also compares the predicate
with set membership over every Python Unicode code point, including controls and surrogates.

## Profile findings and scope decisions

The initial full serial mega completed all 57 stages in 402.7 seconds (403.166 including the
harness overhead). Its largest newly migrated costs were post-stress survey 140.8 seconds,
Phonetic export 60.7, pre-stress analysis 40.9, and Phonetic rendering 37.7. Yeivin rendering
took 0.5 seconds and claim projection rounded to 0.0 seconds; neither justified added machinery.

Separate cProfile runs attributed 43.1 of 90.4 instrumented rendering seconds to 195
`validate_book` calls: five validations per book. The pre-stress analysis made 117 such calls
(26.9 instrumented seconds); the post-stress survey made 468 (108.8 instrumented seconds).
The duplicate-read change removes two validations per book during rendering and one per book
read during analysis. These profile times include large profiler overhead and are diagnostic,
not savings estimates. The post-stress survey still reads the corpus in four passes; changing
its pass structure or cache lifetime is deferred, preserving its stateful scanning behavior.

The current checkout was inspected before using the historical research. The old private
standard-set interface is no longer the public analysis source. The already completed melody
optimization was not repeated. No private code, migration, data model or release field changed.
No C++/Rust build dependency, worker pool, CPU affinity policy, or fine-grained parallelism was
introduced. There was no need for a native rewrite to obtain the measured wins.

Issue 273 is worthwhile at its newly measured saving and remains open pending integration.
[Issue 272](https://github.com/bdenckla/MAM-basics/issues/272) remains open: parallel mega
execution was not implemented or benchmarked under this serial scope. No issue was closed as
not planned on an unmeasured estimate. Both issues and their comments were reviewed through
the GitHub connector; this environment's `gh` GraphQL and REST API requests were forbidden.

## Reproduction and limits

Baseline: `d8b6e1d7ace2baaeabfd03c6cc16366db7374286`, checkout `/workspace/MAM-basics`,
branch `perf/serial-mega-20261003`. Python 3.13.15 on Linux, cgroup quota
`400000 100000` (four CPUs). Source `/workspace/.cloud-setup/activate.sh` before shell work;
use the checkout's `.venv/bin/python` and repository root as cwd. Both owning environments
passed `pip check`. The private adapter was available, so export ran; no cloud-skip environment
override was introduced. The adapter's required pipe processes remain part of the workload.

For serial mega measurements, the scratch harness imports `main_0_mega`, replaces only the
`foi-features-of-interest` StepRecord runner with
`lambda: main_foi_features_of_interest.almost_main(single_threaded=True)`, then calls
`main_0_mega.main()` with no CLI arguments. All other runners and order are unchanged. It saves
`_STEP_TIMES` and total `perf_counter` duration. The focused harness selects the named
StepRecords in their existing order. Old trials replace the three changed functions' code
objects with their baseline definitions before execution, retaining the same globals and
callers. Each trial is a new process; no benchmark or test was run concurrently with another.
Existing OS caches and generated files were retained; host-wide cache dropping was not used.

Scratch harnesses, old-function snapshots, logs, profiles and output hashes are retained in
the checkout's ignored `.novc/serial-performance-20261003/`. The JSON record preserves all
individual repeated timings, both complete runs, and the differential totals. Full-run totals
are one observation per implementation, not repeated medians; use the paired stage trials for
the stronger causal estimate. These Linux measurements do not establish Windows performance.

## Final verification

The after-run completed all 57 serial stages in **374.6 seconds**, versus **402.7 seconds**
before: a 28.1-second observed reduction (7.0%). Timed calls to main, including preflight but
excluding imports, were 374.656 versus 403.166
seconds. This is one full run per version, so it is supporting evidence rather than a repeated
whole-run estimate. Export remained 60.7 seconds; rendering took 30.4, pre-stress analysis
39.0, and post-stress survey 123.5 seconds (140.8 before). The repeated focused rendering
results above are stronger evidence for its causal saving than these single full-run numbers.

SHA-256 manifests of 4,538 tracked files outside the source/documentation directories match
exactly before and after. All tracked generated differences from the starting commit were
already present in the unmodified baseline: eight Graphviz SVGs. XML comparison explains them
as geometry changes plus the `Times New Roman,serif` to `Times,serif` host alias; all other
attributes, labels and links match. The exact eight-file Git patch reproduced after the
optimized mega. These host-specific SVG changes are excluded from the implementation commit.

The repository entrypoint `.venv/bin/python py/main_test.py -q -ra` passed **1,058 tests and
60 subtests**, with the five existing edition-transcription divergence skips, in 211.58 seconds.
The two new tests are differential: full-Unicode forbidden-character membership and the
complete tracked poetic corpus against the full rule loop. Black at defaults and
`git diff --check` passed. Only the three source modules, the differential test, this record
and its JSON, and the maintained speedup plan are included. No generated product changed.

The branch is `perf/serial-mega-20261003`; the task's final response identifies its remotely
verified commit. Main integration, deployment, and the separately handed-off migration work
are outside this task. Issue 273 remains open for that integration, rather than being marked
complete while its implementation exists only on this branch.
