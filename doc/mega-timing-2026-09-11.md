# Where a mega run spends its time, and what makes it faster

Written by a Claude session on 2026-09-11, from a task chip that another Claude session wrote the
same day. Ben's words behind the chip were "I think the most interesting direction to go in is to
make mega run faster than to keep running mostly useless or entirely useless test suite entries"
and "Please bring up a task chip for this mega speedup investigation." Everything else here is the
measurement and analysis of the session that wrote this file.

**Measured against** `main` at `132f2f3e` (2026-09-11) plus the commits of branch
`claude/quirky-keller-b4fa8b`: `93550605` (step timing), `15c09692` (the prose scanner),
`af1c404a` (the JSON writer) and `55eaacac` (one regenerated line that `af1c404a` causes, §6).
MAM-private stood at `3d6f25b`. The machine is Ben's: an Intel Core
i5-13500T with 6 performance cores and 8 efficiency cores (20 logical processors), Windows 11 on
the Balanced power plan, Python 3.13.15. **Re-measure before relying on a figure.** Every mega run
now prints its step times, and §8 gives the commands behind every other figure.

## Summary: 327 s of steps, two speedups made, and two failing steps

1. **A full run spends 327 s in its 60 steps, and 15 steps account for 86% of that** (§3, run
   1). The two accgram surveys alone take 105 s, 32% of the run. 45 steps take under 5 s each.
   Since these runs, `main` has deleted one of the 60, `near-aleppo-census` (`d32a17b8`), which
   takes about 18 s more off a run (§7, item 2).
2. **Two output-neutral speedups have been made on the branch** (§5), each measured inside one
   process with the old code and the new running alternately, call by call. The prose scanner now
   skips its rule loop wherever only its catch-all rule can match, which cuts its time by 72%,
   from 75.3 s to 21.1 s over the eight steps that call it. The JSON writer now uses Python's C
   encoder, which cuts JSON writing by three quarters, from 20.86 s to 5.05 s a run. Whole runs
   are too noisy here to confirm the sum: the eight scanner steps took 25 to 50 s less, but whole
   runs only 15 to 24 s less, because the other 52 steps varied by 30 s between runs with no
   change to their code.
3. **Two steps fail on `main`, so a full run takes three invocations** (§2). The failure of the
   `diff-mpp` step, the mpplus diff, is known. The failure of `gen-site` is new, and is raised
   here and not fixed, because fixing it changes figures in the post-stress-meteg pages' prose.
4. **Running independent steps at the same time is the largest remaining saving, and the largest
   change** (§7, item 1). The longest chain of steps that must follow one another took about 78 s
   in the pinned run, against 303 s for all the steps one after another.
5. **On this machine the same step on the same code can take up to 2.6 times as long in one run
   as in another** (§1), partly because Windows sometimes runs the mega on an efficiency core. A
   single run is therefore a poor measure of any change smaller than that.

## 1. How the runs were measured, and why a single run misleads

Since `93550605`, `py/main_0_mega.py` prints `STEP TIME: <step>: <seconds> s` after every step and,
at the end, every step it ran, slowest first, with its share of the run. Both are printed when a
step raises, the table coming before the traceback.

A full run on `main` at `132f2f3e` is three invocations, because two steps raise (§2). Run 1, the
source of §3's table, was those three invocations from 09:32 to 09:39 on 2026-09-11, with no
change to anything a step runs. Starting the interpreter and importing every step's module took
1.9 to 3.0 s per invocation, measured as each invocation's wall time less the step loop's time.

**A single run misleads on this machine: the same step, on the same code, took up to 2.6 times as
long in one run as in another.** One cause is measured. The i5-13500T mixes fast and slow cores,
and a single-threaded Python step runs at very different speeds depending on which one Windows
gives it. The step `uxlc-fois`, run on the same code each time, took 13.72 and 11.56 s pinned to
logical processors 0-11, and 22.96 and 23.56 s pinned to logical processors 12-19. Unpinned, it
took 13.6 s in run 1 and 22.2 s in run 2, and neither change moves it by more than a few
hundredths of a second (it writes 0.1 M characters of JSON). Between those two runs
`near-aleppo-census` went from 17.6 to 43.4 s and `mam4sef-and-ajf` from 4.2 to 11.0 s, though no
change touched either. Opting the process out of Windows power throttling did not help: three
such runs of `uxlc-fois` took 10.95, 13.83 and 15.48 s, against 10.72, 10.99 and 12.05 s for
three plain runs interleaved with them.

**Pinning to logical processors 0-11 removed the slow-core cases but not all the variation**, and
the rest has no measured cause. In the two pinned runs of §3, `near-aleppo-census` took 19.4 and
34.9 s, and `mam-simple`, pinned, took 18.1 s against 11.8 s unpinned in run 1. So §5 attributes
savings from measurements taken inside one process, where the old code and the new code run
alternately, call by call, on the same inputs, and gives the whole-run totals with the variation
of the untouched steps beside them. One more hazard is another session: a second mega run started
from another worktree at 10:07 slowed a baseline run so much (`parse-ws` 40.4 s against 12.8 to
15.2 s otherwise) that the baseline was discarded. Two sessions integrating at once will each see
a slower mega.

## 2. Two steps fail on `main` at `132f2f3e`, so a full run takes three invocations

1. **`diff-mpp`, the mpplus diff, raises `VerificationError`, as already known.** It writes the
   five named releases' reports, then fails on the unpinned-latest report at Isaiah 24:18. This is
   finding 1 of `doc/review-findings-2026-09-10.md`, which is on branch
   `dual-agent-review-2026-09-10`, and `CLAUDE.md`'s integration section records it; the
   remediation of that review owns the fix. A branch under way on 2026-09-11 renames the step
   `diff-mpplus`.
2. **`gen-site` raises `AssertionError`, which is new, and is raised here and not fixed.**
   `pin_claims` in `py/author_site/post_stress_meteg.py`, at the assertion beginning
   `assert census_chanted_word_summary["by_system"] == {`, pins the prose `mbs_only` count at
   12,849; the survey step just before `gen-site` now writes 12,842. The survey's committed
   output, `out/accgram/post-stress-meteg.json`, was last regenerated at `ad44dba7` (2026-09-09),
   and both of the survey's inputs moved on the evening of 2026-09-10: `209b4c05` refreshed
   MAM-simple from Wikisource, and MAM-private `65ee486` refreshed the Phonetic MAM books the
   survey reads (`al-hatorah/io/a01-phonetic-std-set/` and `al-hatorah/io/a01-phonetic-jta/`) in
   the seven books of that refresh. The regenerated JSON differs in 63 lines. "Meteg before the
   stressed syllable" falls by 7, from 14,767 to 14,760 under `cant-alef` and from 14,768 to
   14,761 under `cant-bet`. "Meteg sharing a letter with a non-stress-marking accent" rises from
   27 to 28, with a new record at Isaiah 24:18, the meteg that refresh added. The count
   `metegs_in_the_surveyed_snapshot` falls from 38,161 to 38,154. **It is not fixed here**
   because the fix changes figures that the nine post-stress-meteg pages state in prose, which is
   an editorial decision rather than a timing one; the regenerated JSON is not committed either.
   Another session found the same failure the same morning while checking the integration of
   `claude/loving-ptolemy-1i4seh`, which reached `main` as `478bdae6` all the same.

Until both are fixed, a full run is three invocations, the second resuming after `diff-mpp`. The
runs measured here resumed the third time after `gen-site`, skipping it:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py --resume-from diff-ctr-vs-mam
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py --resume-from diffable-pointed-hebrew
```

A better third invocation for an integration check, which the other session used, puts the
committed survey JSON back and resumes *from* `gen-site`, so that `gen-site` and the four steps
after it are checked too:

```powershell
git restore out/accgram/post-stress-meteg.json
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py --resume-from gen-site
```

`gen-site`'s time does not appear in the runs measured here. Run alone on the committed survey
JSON, it took 4.1 s.

## 3. Where the time goes: all 60 steps

Run 1 ranks the steps: it is the unchanged code, unpinned, and its three columns give each
step's seconds, its share of the 326.9 s and the running total of the shares. The other three
columns are for comparison, and show how far one step moves between runs. "Pinned, before" is the
unchanged code pinned to logical processors 0-11 (321.8 s in all); "Pinned, after" is the
committed code of §5 pinned the same way (302.7 s); "Run 2, after" is the committed code
unpinned (307.1 s). A step that raised is marked, and its figure is the time until it raised.

| Rank | Step | Run 1 (s) | Share | Cumulative | Pinned, before (s) | Pinned, after (s) | Run 2, after (s) |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | `accgram-survey-post-stress-meteg` | 58.5 | 17.9% | 17.9% | 48.3 | 40.9 | 40.0 |
| 2 | `accgram-survey-chanted-word-accents` | 46.7 | 14.3% | 32.2% | 34.2 | 22.0 | 22.8 |
| 3 | `accgram-generate-html` | 19.3 | 5.9% | 38.1% | 11.3 | 12.3 | 18.6 |
| 4 | `near-aleppo-census` | 17.6 | 5.4% | 43.5% | 19.4 | 34.9 | 43.4 |
| 5 | `diff-wsgo` | 16.1 | 4.9% | 48.4% | 13.9 | 14.6 | 12.4 |
| 6 | `wlc-json-and-unicode` | 16.0 | 4.9% | 53.3% | 20.0 | 18.4 | 19.8 |
| 7 | `accgram-run-prose` | 14.4 | 4.4% | 57.7% | 16.9 | 8.3 | 8.4 |
| 8 | `parse-ws` | 14.0 | 4.3% | 62.0% | 15.1 | 15.2 | 12.8 |
| 9 | `uxlc-fois` | 13.6 | 4.2% | 66.1% | 12.7 | 14.3 | 22.2 |
| 10 | `tmpl-survey` | 12.6 | 3.9% | 70.0% | 10.4 | 8.4 | 8.3 |
| 11 | `mam-with-doc` | 12.2 | 3.7% | 73.7% | 6.2 | 7.9 | 5.0 |
| 12 | `mam-simple` | 11.8 | 3.6% | 77.3% | 18.1 | 17.6 | 11.3 |
| 13 | `multimark` | 10.7 | 3.3% | 80.6% | 17.1 | 13.7 | 11.8 |
| 14 | `diff-mpp` (raised VerificationError) | 10.1 | 3.1% | 83.7% | 7.2 (raised) | 8.1 (raised) | 6.1 (raised) |
| 15 | `foi-features-of-interest` | 8.7 | 2.7% | 86.4% | 10.4 | 10.9 | 7.2 |
| 16 | `mam4sef-and-ajf` | 4.2 | 1.3% | 87.6% | 10.0 | 5.3 | 11.0 |
| 17 | `ws-bot-proto` | 4.1 | 1.3% | 88.9% | 5.2 | 4.7 | 4.2 |
| 18 | `parse-go` | 3.5 | 1.1% | 90.0% | 1.9 | 1.7 | 1.1 |
| 19 | `book-of-job-site` | 2.9 | 0.9% | 90.9% | 3.7 | 3.9 | 4.1 |
| 20 | `vendored-mam4sef` | 2.5 | 0.8% | 91.6% | 6.6 | 3.6 | 2.5 |
| 21 | `accgram-run-poetic` | 2.0 | 0.6% | 92.2% | 2.3 | 2.4 | 2.3 |
| 22 | `vendoring-audit` | 1.9 | 0.6% | 92.8% | 3.2 | 3.1 | 3.9 |
| 23 | `pipeline-graph` | 1.5 | 0.5% | 93.3% | 2.1 | 2.4 | 3.3 |
| 24 | `accgram-xcheck-poetic` | 1.4 | 0.4% | 93.7% | 1.8 | 2.6 | 1.9 |
| 25 | `accgram-servi-xcheck` | 1.4 | 0.4% | 94.1% | 1.4 | 1.6 | 1.5 |
| 26 | `accgram-grammaticality` | 1.4 | 0.4% | 94.6% | 1.5 | 2.0 | 1.5 |
| 27 | `estimate-uxlc-locations` | 1.4 | 0.4% | 95.0% | 1.0 | 0.9 | 0.9 |
| 28 | `accgram-test-fixes` | 1.3 | 0.4% | 95.4% | 2.4 | 4.8 | 1.5 |
| 29 | `uxlc-amb-early-mtg` | 1.3 | 0.4% | 95.8% | 0.9 | 1.1 | 1.9 |
| 30 | `uxlc-grammar-test` | 1.3 | 0.4% | 96.2% | 1.3 | 1.0 | 0.8 |
| 31 | `uxlc-check-changes` | 1.2 | 0.4% | 96.5% | 1.1 | 1.5 | 2.1 |
| 32 | `clc` | 1.1 | 0.3% | 96.9% | 0.9 | 0.9 | 0.8 |
| 33 | `uxlc-word-list` | 1.0 | 0.3% | 97.2% | 0.8 | 0.8 | 0.8 |
| 34 | `sigil-inventory` | 0.9 | 0.3% | 97.5% | 0.8 | 1.1 | 0.8 |
| 35 | `mam-osis` | 0.8 | 0.2% | 97.7% | 2.4 | 1.2 | 1.4 |
| 36 | `search-holam-he-qere` | 0.8 | 0.2% | 98.0% | 0.9 | 0.9 | 0.8 |
| 37 | `gen-misc` | 0.8 | 0.2% | 98.2% | 1.0 | 1.1 | 1.2 |
| 38 | `vendored-mam-osis` | 0.7 | 0.2% | 98.4% | 1.7 | 1.1 | 0.8 |
| 39 | `wordlist` | 0.7 | 0.2% | 98.6% | 0.8 | 1.0 | 1.1 |
| 40 | `verify-and-render-table` | 0.7 | 0.2% | 98.8% | 0.8 | 0.7 | 1.1 |
| 41 | `uxlc-write-page-break-info` | 0.6 | 0.2% | 99.0% | 0.5 | 0.4 | 0.8 |
| 42 | `render-uxlc-corrections` | 0.5 | 0.2% | 99.2% | 0.2 | 0.2 | 0.2 |
| 43 | `wlc-diffs-420422` | 0.5 | 0.2% | 99.3% | 0.5 | 0.7 | 0.5 |
| 44 | `search-final-hiriq-verse-text` | 0.3 | 0.1% | 99.4% | 0.4 | 0.4 | 0.4 |
| 45 | `explicit-xataf` | 0.3 | 0.1% | 99.5% | 0.5 | 0.4 | 0.4 |
| 46 | `accgram-run-dual-cant` | 0.3 | 0.1% | 99.6% | 0.4 | 0.4 | 0.3 |
| 47 | `vendored-letter-small-job` | 0.2 | 0.1% | 99.7% | 0.4 | 0.2 | 0.2 |
| 48 | `accgram-run-printed-decalogue` | 0.2 | 0.1% | 99.7% | 0.3 | 0.3 | 0.1 |
| 49 | `wlc-a-notes` | 0.2 | 0.1% | 99.8% | 0.2 | 0.2 | 0.2 |
| 50 | `diffable-pointed-hebrew` | 0.2 | 0.1% | 99.8% | 0.2 | 0.2 | 0.2 |
| 51 | `diff-ctr-vs-mam` | 0.1 | 0.0% | 99.9% | 0.1 | 0.1 | 0.1 |
| 52 | `vendored-tmpl-survey-toy` | 0.1 | 0.0% | 99.9% | 0.1 | 0.1 | 0.1 |
| 53 | `mam-simple-docs` | 0.1 | 0.0% | 99.9% | 0.2 | 0.1 | 0.1 |
| 54 | `decnreub` | 0.1 | 0.0% | 100.0% | 0.1 | 0.1 | 0.0 |
| 55 | `map-changes-to-book-of-job` | 0.1 | 0.0% | 100.0% | 0.0 | 0.0 | 0.1 |
| 56 | `tmpl-survey-toy` | 0.0 | 0.0% | 100.0% | 0.0 | 0.0 | 0.0 |
| 57 | `letter-small-job` | 0.0 | 0.0% | 100.0% | 0.0 | 0.0 | 0.0 |
| 58 | `find-uxlc-accent-changes` | 0.0 | 0.0% | 100.0% | 0.0 | 0.0 | 0.0 |
| 59 | `gen-site` (raised AssertionError) | 0.0 | 0.0% | 100.0% | 0.0 (raised) | 0.0 (raised) | 0.0 (raised) |
| 60 | `ac-gen-index-flat-annotated` | 0.0 | 0.0% | 100.0% | 0.0 | 0.0 | 0.0 |

## 4. What the largest steps do

Every step runs inside the mega's Python process unless this list says otherwise. The
seconds are run 1's. "Under cProfile" figures come from running the one step under Python's
profiler, which inflates small Python calls, so they give shares rather than times.

1. **`accgram-survey-post-stress-meteg`, 58.5 s.** Reads MAM-private's Phonetic MAM and
   MAM-simple's `xml-vtrad-mam`, and writes `out/accgram/post-stress-meteg.json`; skipped in a
   cloud session. Under cProfile, 132.9 of its 150.9 s are four passes of `_scan`, which call
   the prose scanner on 37,510 verse bodies (54.1 s, 36%) and the poetic scanner on 8,930
   (6.7 s). MAM-simple is loaded four times, by four calls of `load_mam_simple_for_refs`
   (11.1 s).
2. **`accgram-survey-chanted-word-accents`, 46.7 s.** Reads WLC 4.22 (`out/wlc422-kq-u`, which
   `wlc-json-and-unicode` writes), UXLC (`in/UXLC-39`) and MAM-simple, and scans the prose
   verses of all three: 56,172 verse bodies. Under cProfile the prose scanner is 78.8 of its
   113 s (70%), in 179 million `re.Pattern.match` calls. Writes
   `out/accgram/chanted-word-accents.json`.
3. **`accgram-generate-html`, 19.3 s.** Runs the fourteen HTML generators of `_HTML_GENERATORS`
   in `py/main_accgram.py` one after another, writing under `gh-pages/wlc/accgram/`. The residue
   page reads the chanted-word survey's JSON instead of recomputing it (`--trust-survey`). The
   poetic scanner is 1.5 s of it (§7, item 3). Not profiled.
4. **`near-aleppo-census`, 17.6 s.** The one step that runs outside this repository: a
   subprocess, `near-aleppo/census/run_all.py --write` in MAM-private, which runs 102 census
   scripts as child processes through a pool of 6 threads and rewrites their goldens under
   `near-aleppo/census/expected/`. Reads MAM-parsed's `plus/` tree through
   `REPO_MAM_PARSED_DIR`, and this repository's `aleppo/`. Skipped in a cloud session. Deleted
   from the mega by `d32a17b8`, after these runs.
5. **`diff-wsgo`, 16.1 s.** Parses all 39 books of the Wikisource input `in/mam-ws/` again (the
   parse that `parse-ws` has just done), reads `MAM-parsed/google/`, and compares the two,
   writing `out/diff_mamws_mamgo.json` and `out/diff_mamws_mamgo-auto-edits.json`. The parse is
   about 2 s of it (§7, item 6), so most of the step is the comparison. Not profiled.
6. **`wlc-json-and-unicode`, 16.0 s.** Converts WLC 4.20 and 4.22 into JSON and Unicode under
   `out/`, and compares 4.20 with the UXLC books. Every accgram step reads its
   `out/wlc422-kq-u`. Not profiled.
7. **`accgram-run-prose`, 14.4 s.** Scans and parses the WLC 4.22 prose books, 19,531 verse
   bodies, with the prose scanner and the PLY grammar, and writes `out/accgram/prose/`. Under
   cProfile the scanner is 24.0 of its 52.9 s (45%), and writing JSON through `json.dump` is
   13.2 s (25%), 4.9 million separate writes.
8. **`parse-ws`, 14.0 s.** Parses the 39 Wikisource books of `in/mam-ws/`, writes
   `out/mam-ws-parsed-fmt-2/` and MAM-parsed's `plain/` and `plus/`, checks every plus book with
   `check_mpplus`, copies MAM-parsed's support files and regenerates its documentation. Not
   profiled.
9. **`uxlc-fois`, 13.6 s.** Reads `in/UXLC-39` and the UXLC change log, and writes
   `gh-pages/uxlc/fois/`. Under cProfile it is 108 million small Python calls: two mark-grammar
   passes each split every atom into letter clusters (611,934 splits, one per atom per pass) and
   test 1.2 million clusters against a series of patterns.
10. **`tmpl-survey`, 12.6 s.** Surveys the templates of MAM-parsed's `plain/` and `plus/` trees
    and renders 12 call graphs with the pinned Graphviz, one after another. Under cProfile 7.5 of
    its 11.5 s are 24 `dot` subprocesses: the 12 renders, and a `dot -V` version check before
    each.
11. **`mam-with-doc`, 12.2 s.** Reads MAM-parsed's `plus/` tree and writes MAM-with-doc's 39
    books, two HTML files each, under `gh-pages/MAM-with-doc/`. Not profiled.
12. **`mam-simple`, 11.8 s.** Reads MAM-parsed's `plus/` tree and writes MAM-simple in XML and
    JSON for three versification traditions (the `MAM-simple/` tree is 107.9 MB), then copies
    MAM-simple's example-support files. Not profiled.
13. **`multimark`, 10.7 s.** Reads MAM-parsed's `plus/` tree, records every letter with more than
    one mark in `out/mam-multimarks-raw.json`, and summarizes it. Not profiled.
14. **`diff-mpp`, 10.1 s until it raised.** The mpplus diff: reads the named releases from the
    tracked archives under `MAM-parsed/historical/` (84.6 MB of zip files) and, for the
    unpinned-latest report, the plus tree of HEAD through `git show`, one subprocess per book.
    Not profiled.
15. **`foi-features-of-interest`, 8.7 s.** Reads MAM-parsed's `plus/` tree and reports its
    features of interest. Not profiled.

Three kinds of repeated work recur, and §7 prices each:

1. Seven steps read the whole of MAM-parsed's `plus/` tree afresh through
   `read_parsed_plus_bk39s`: `foi-features-of-interest`, `mam-with-doc`, `mam-simple`,
   `multimark`, `wordlist`, `explicit-xataf` and `sigil-inventory` (§7, item 8).
2. Three steps parse the whole Wikisource input: `parse-ws`, `diff-wsgo` and `ws-bot-proto`
   (§7, item 6).
3. Four accgram steps scan the same poetic verses with the poetic scanner, each for itself
   (§7, item 3).

## 5. Two speedups made on the branch, both output-neutral

1. **The prose scanner now skips its rule loop where only the catch-all rule can match**, in
   `15c09692` (`py/accgram/prose_scanner.py`). `scan_accents` mirrors flex: at each position of a
   verse body it tries all 38 rules of `_GG_RULES` and keeps the longest match, rule order
   breaking ties. At most positions (a letter placeholder, a space, a maqaf) nothing but the last
   rule, the catch-all `.`, can match. Every rule but the catch-all is now also compiled into one
   alternation, which matches at a position if and only if one of those rules does. Where it does
   not, the scanner takes the catch-all's one-character match, which emits no token, without
   running the loop; where it does, the loop runs exactly as before. The alternation is built
   from the rule list the scanner is about to read, and rebuilt when that list changes, because
   `almost_errors_trees._no_mahapakh_qadma_fuse` rebinds `_GG_RULES` for the Ezekiel 20:31
   exhibit. A first check whose harness compiled the alternation once, from the original list,
   disagreed on that exhibit and on nothing else, which is how the rebinding was found; the
   committed code compares the list with the one it last built from on every call.

   Measured inside one process, the old function (loaded from `93550605`, the commit before the
   change) and the new one ran alternately on every call of eight mega steps:

   | Step | Scanner calls | Old (s) | New (s) |
   |---|---:|---:|---:|
   | `accgram-survey-chanted-word-accents` | 56,172 | 39.39 | 10.63 |
   | `accgram-survey-post-stress-meteg` | 37,510 | 21.12 | 6.40 |
   | `accgram-run-prose` | 19,531 | 13.16 | 3.61 |
   | `accgram-generate-html` | 2,282 | 0.58 | 0.19 |
   | `uxlc-grammar-test` | 1,488 | 0.63 | 0.17 |
   | `accgram-test-fixes` | 190 | 0.27 | 0.07 |
   | `accgram-run-printed-decalogue` | 220 | 0.11 | 0.04 |
   | `accgram-run-dual-cant` | 807 | 0.07 | 0.02 |
   | **All eight** | **118,200** | **75.33** | **21.12** |

   The 54.2 s saved is 72% of the scanner's time. No call differed in any token's type, leaf or
   start position, nor in the state of the `HasLegarmeh` counter after the call. The check ran
   unpinned, so its seconds are those of whichever cores it got; what it measures is the ratio
   between the two columns, since the two functions ran one right after the other, call by
   call, on the same core.
2. **The JSON writer now uses Python's C encoder**, in `af1c404a` (`py/mb_cmn/file_io.py`, and
   `MAM-simple/py-examples/mb_cmn/file_io.py`, the verbatim copy that the `mam-simple` step
   makes). `json_dump_to_file_path`, which 53 modules call, wrote through `json.dump`, which never
   uses the C encoder: it always encodes in pure Python, and writes the text in pieces, 4.9
   million of them in `accgram-run-prose` alone. On the Python 3.13.15 this repository runs,
   `json.dumps` hands an indented encoding to the C encoder, so the writer now makes one
   `json.dumps` and one write. Written both ways at indents 0, 1 and 2, the twelve largest
   tracked JSON files gave identical bytes every time and took 4.47 s under `json.dump` against
   1.38 s under `json.dumps`. Over a whole run, measured inside one process with every payload
   written both ways, call by call, the old way to a scratch file and the new way to the real
   output:

   | Step | Files written | Characters (M) | `json.dump` (s) | `json.dumps` (s) |
   |---|---:|---:|---:|---:|
   | `wlc-json-and-unicode` | 102 | 58.9 | 5.93 | 1.54 |
   | `parse-ws` | 87 | 34.3 | 5.62 | 1.07 |
   | `accgram-run-prose` | 37 | 23.2 | 3.01 | 0.58 |
   | `mam-simple` | 72 | 24.1 | 2.21 | 0.68 |
   | `parse-go` | 24 | 13.3 | 1.14 | 0.30 |
   | `ws-bot-proto` | 80 | 17.0 | 0.99 | 0.33 |
   | `accgram-run-poetic` | 3 | 3.0 | 0.69 | 0.16 |
   | `uxlc-check-changes` | 123 | 1.7 | 0.25 | 0.04 |
   | `foi-features-of-interest` | 23 | 2.0 | 0.19 | 0.05 |
   | `wordlist` | 1 | 1.8 | 0.15 | 0.06 |
   | `sigil-inventory` | 1 | 3.4 | 0.15 | 0.06 |
   | `uxlc-word-list` | 2 | 1.8 | 0.10 | 0.05 |
   | 17 other steps | 40 | 6.5 | 0.43 | 0.11 |
   | **All 29 steps that write through it** | **595** | **191.0** | **20.86** | **5.05** |

   So the change takes about 15.8 s off every run, three quarters of its JSON writing, most of
   it in the five steps that write the most: `wlc-json-and-unicode`, `parse-ws`,
   `accgram-run-prose`, `mam-simple` and `parse-go`. This measurement is the one to trust for
   the JSON change; the whole-run comparison below cannot see it.

**In whole runs, the eight scanner steps took 25 to 50 s less after the changes, and the whole
run 15 to 24 s less; the noise of §1 allows no closer figure.** Over the four runs of §3's
table:

| Steps | Run 1, before (s) | Pinned, before (s) | Pinned, after (s) | Run 2, after (s) |
|---|---:|---:|---:|---:|
| The eight that call the prose scanner | 142.0 | 115.1 | 90.0 | 92.5 |
| The other 52 | 184.9 | 206.7 | 212.7 | 214.6 |
| All 60 | 326.9 | 321.8 | 302.7 | 307.1 |

The other 52 steps, whose code the scanner change does not touch and the JSON change can only
make faster, took from 185 to 215 s, with no pattern between the runs before and the runs after.
That 30 s spread is the noise. It hides the JSON writer's saving entirely, and in the whole-run
totals it ate part of the scanner's.

## 6. What was checked, and what is not expected to change

**Nothing a step writes is expected to change except the one line of item 2**; only how long the
steps take. The steps, their order and their arguments are as they were. The `STEP TIME` lines
and the closing table are new lines on standard output, and nothing else in the output is new.

1. **Every tracked output the mega regenerates came out byte for byte the same** with both
   changes. After a full run (run 2, the three invocations of §2), `git status --porcelain`
   listed only the two edited modules, the copy of `file_io.py`, and
   `out/accgram/post-stress-meteg.json`, whose regenerated bytes (blob `e15cad57`) are the bytes
   that run 1 wrote without either change (§2, item 2). That covers MAM-parsed's `plain/` and
   `plus/`, all of MAM-simple and every accgram corpus, all written through the new JSON writer,
   and every accgram output that depends on the scanner.
2. **One tracked output does change, as a consequence of committing `af1c404a`, and the change
   has been committed** (`55eaacac`). `out/vendoring_compare_out.txt`, which `vendoring-audit`
   writes, records the date of each vendored copy's last commit, and `af1c404a` moved the
   `file_io.py` copy's from 2026-09-06 to 2026-09-11. The pinned run of the committed code wrote
   exactly that one-line change.
3. **`gen-site` reproduced its eleven pages** when run alone with both changes on the committed
   survey JSON, since in a full run it raises before rendering anything.
4. **Two outputs are regenerated by no run on `main`**, before these changes or after them: the
   unpinned-latest report of the mpplus diff and the change-log index (§2, item 1).
5. **MAM-private stayed clean**: `git status --porcelain` there printed nothing after any run.
6. **The scanner change also passed the differential check of §5**: 118,200 calls with no
   difference.
7. **The suite was not run.** `CLAUDE.md`'s integration section makes it optional, and the
   mega's reproduction of the goldens is the check it relies on.

## 7. Speedups proposed for Ben, largest first

None of these is made on the branch; item 2 has since been made on `main`. Each saving is an
estimate from the measurements named with it, after the two changes of §5.

1. **Run independent steps at the same time**, filed as #272. The mega runs one step at a time,
   in one process, on one of 20 logical processors. Most steps read only committed inputs or the
   output of one or two earlier steps, and most of the notes in `_STEPS` say which. Two chains
   are long: the MAM
   chain, `parse-ws`, then `mam-simple`, then `accgram-survey-post-stress-meteg`, then
   `gen-site`; and the WLC chain, `wlc-json-and-unicode` (with `mam-simple`), then
   `accgram-run-prose`, then `accgram-survey-chanted-word-accents`, then `accgram-generate-html`.
   In the pinned run of the committed code, the MAM chain took 77.8 s (15.2 + 17.6 + 40.9, and
   4.1 for `gen-site` run alone), and the WLC chain 75.4 s (the 32.8 s until both
   `wlc-json-and-unicode` and `mam-simple` had finished, then 8.3 + 22.0 + 12.3), while all 60
   steps one after another took 302.7 s. Everything off those two chains could run beside them
   on the other cores. So a run bounded by its longest chain might take something like 90 to
   120 s, allowing for the slower efficiency cores and for steps competing for the disk.
   **Expected saving: more than half of a run. Risk: high, and the largest change here.** The
   steps share one process (`main()` blanks `sys.argv` for all of them, and
   `almost_errors_trees` rebinds `prose_scanner._GG_RULES` while it runs), their reads and writes
   are declared nowhere but in prose, and some steps write what others read (`mam-simple`
   deletes and rewrites `MAM-simple/py-examples/`, which three `vendored-*` steps run and
   `vendoring-audit` reads). It needs a declared read and write list per step, one process per
   running step, and a rule for stopping the other steps when one fails.
2. **Take `near-aleppo-census` out of the mega: this has been done on `main`**, in `d32a17b8`
   (2026-09-11 10:19, after the runs measured here), for the other reason Ben wanted it, the
   write into MAM-private. **Saving: the step's 17.6 s in run 1, 19.4 s pinned.** MAM-private's
   census goldens now need a trigger of their own.
3. **Give the poetic scanner change 1's fast path**, filed as #273.
   `poetic_scanner.scan_accent_tokens` runs the same loop over its 35 rules, ending in the same
   catch-all, and five steps call it, four of
   them on the same 4,465 or so poetic verse bodies: 1.32 s in `accgram-run-poetic`, 1.15 s in
   `accgram-xcheck-poetic`, 1.41 s in `accgram-servi-xcheck`, 1.52 s in `accgram-generate-html`
   and 2.14 s in `accgram-survey-post-stress-meteg`, 7.54 s in all. **Expected saving: about
   5 s**, if the fast path skips as large a share of positions there as in the prose scanner.
   **Risk: low**, with the same differential check as change 1.
4. **Scan the chanted-word survey's three corpora at the same time**, in three processes. The
   three `scan_corpus` calls in `build_survey` are independent, and after change 1 their scanning
   took 10.6 s in §5's unpinned check, less on a performance core, of a step that took 22.0 s
   pinned. **Expected saving: about 5 s. Risk: medium**: starting a Python process on Windows
   costs about a second, module-level caches are rebuilt in each, and the results must be put
   back together in the fixed corpus order.
5. **Render `tmpl-survey`'s twelve SVGs at the same time**, on a pool of threads, since each is a
   separate `dot` subprocess writing a different file. **Expected saving: about 5 s** of the
   7.5 s the renders took under cProfile. **Risk: low to medium**: a cloud session records its
   skipped renders in a list whose order would have to be kept.
6. **Parse the Wikisource input once per run.** `diff-wsgo` and `ws-bot-proto` each repeat the
   parse of the 39 books that `parse-ws` has just made, and one parse took 1.87 s (2.56 s the
   first time in a process). **Expected saving: about 4 s. Risk: medium**: a shared parse has to
   be keyed on the input files' contents, and no consumer may change it.
7. **Load MAM-simple once in the post-stress-meteg survey.** `load_mam_simple_for_refs` runs four
   times (11.1 of 150.9 s under cProfile, 7%). **Expected saving: about 2 to 3 s. Risk: low** if
   the four calls ask for the same references, which is still to be checked; otherwise a cache
   keyed by the references.
8. **Read MAM-parsed's `plus/` tree once per run**, not once in each of the seven steps that read
   it whole. One read took 0.24 s (0.92 s the first time in a process). **Expected saving: about
   1.5 s. Risk: medium**: the shared structure must not be changed by any step, and `parse-ws`
   rewrites the tree before the first reader.
9. **Split each atom into clusters once in `uxlc-fois`.** Its two mark-grammar passes each split
   every atom (611,934 splits in all; 7.3 of 45.2 s under cProfile, 16%), so sharing the split
   saves half of that. **Expected saving: about 1 s. Risk: low to medium.**
10. **Pinning the mega to the performance cores is not proposed as a speedup.** It removes the
    slow-core cases that cost run 2 8.6 s on `uxlc-fois` and 25.8 s on `near-aleppo-census`
    against run 1, but the pinned runs' totals came within 2% of the unpinned ones (321.8 against
    326.9 s before the changes, 302.7 against 307.1 s after), and pinned steps still varied
    (§1). Its mask also names this CPU's cores, so on another machine it could select the slow
    ones. It stays useful for taking the efficiency cores out of a comparison (§8, item 2).
11. **Skipping steps whose inputs have not changed is not proposed for the integration check.**
    The mega is the test because it recomputes every golden. A step skipped on the strength of a
    declared input list tests nothing, and a list that misses one input turns a failure into a
    pass. At most it could be an opt-in for runs during development.
12. **Running the subprocess steps in-process is not proposed.** Apart from
    `near-aleppo-census` (item 2), the mega starts four Python subprocesses, the `vendored-*`
    steps, which took 3.5 s together in run 1; the smallest took 0.1 s including the start of
    its interpreter, so start-up is worth well under a second in all. Running MAM-simple's and
    MAM-parsed's example scripts as separate programs, on the copies of the support modules
    beside them, is also what those steps are for.

The hand estimates in `py/main_0_mega.py`'s comments predate the timing, and four of them are
now far out: "~40s" for `diff-mpp` (10.1 s until it raised), "~15s" for `vendoring-audit`
(1.9 s), "~12 s for all eight together" for the steps added on 2026-08-04 (8.0 s), and "~3s"
for `accgram-test-fixes` (1.3 s). They are raised here and not changed, being history in a
comment; the table each run now prints supersedes them.

## 8. Commands behind the figures

1. **Step times.** Every mega run prints them: a `STEP TIME:` line after each step, and the
   closing table. A full run on `main` at `132f2f3e` is the three invocations of §2.
2. **A run pinned to the performance cores of Ben's machine.** Set the PowerShell process's
   affinity, then start the mega from the same PowerShell session, whose children inherit the
   mask:

   ```powershell
   [System.Diagnostics.Process]::GetCurrentProcess().ProcessorAffinity = [IntPtr]0xFFF
   ```

   `0xFFF` selects logical processors 0-11, which on the i5-13500T are the six performance cores
   and their second threads, as the `uxlc-fois` timings of §1 show. On another CPU the mask means
   something else. The setting lasts as long as that PowerShell session; a new one starts
   unpinned.
3. **One step alone, and under cProfile.** A throwaway script, run from the repository root,
   imported `main_0_mega`, found the step's `StepRecord` in `_STEPS` by its id, blanked
   `sys.argv` as `main()` does, and called the step's runner, timed, either plainly or inside a
   `cProfile.Profile`.
4. **The scanner's differential check.** A throwaway script loaded `py/accgram/prose_scanner.py`
   as it stood at `93550605` (from `git show`) as a separate module, replaced
   `accgram.prose_scanner.scan_accents` with a wrapper before anything imported it, and ran eight
   mega steps in one process. On each call the wrapper pointed the old module at the current
   `_GG_RULES`, ran the old function on a copy of the `HasLegarmeh` object and the new function
   on the original, compared every token's type, leaf and start, compared the two objects'
   state, and timed both.
5. **The JSON writers' comparison on the largest files.** A throwaway script loaded each of the
   twelve largest tracked `.json` files, wrote it with `json.dump` and again with `json.dumps`
   and one write, each at indents 0, 1 and 2, opening the files as `mb_cmn/file_io.py` does
   (`encoding="utf-8"`, `newline=""`), compared the bytes and timed both.
6. **The JSON writers' comparison over a whole run.** A throwaway script replaced
   `mb_cmn.file_io._json_dump_to_file_pointer` with a wrapper that wrote every payload twice,
   the old way to a scratch file and the new way to the real output, timing both, and then ran
   every mega step in order in one process except `diff-mpp` and `gen-site`, which raise, and
   `near-aleppo-census`, which never calls this module. It needs an `if __name__ == "__main__":`
   guard, because `foi-features-of-interest` starts a `multiprocessing` pool whose children
   re-import the main script.
7. **The repeated work of §7, items 3, 6 and 8.** A throwaway script timed one parse of the 39
   Wikisource books through `ws.ws_get_bk_in_both_fmts.get_bk_in_both_fmts`, one whole read of
   MAM-parsed's `plus/` tree through `read_parsed_plus_bk39s`, and, through a timing wrapper
   patched in before anything imported it, every call of `poetic_scanner.scan_accent_tokens`
   made by `accgram-run-poetic`, `accgram-xcheck-poetic`, `accgram-servi-xcheck`,
   `accgram-grammaticality`, `accgram-generate-html` and `accgram-survey-post-stress-meteg`.
