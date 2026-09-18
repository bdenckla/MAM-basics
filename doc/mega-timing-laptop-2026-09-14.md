# Mega timing on a Surface Laptop 4, LAPTOP-DBLE8UKA, 2026-09-14

Written by a Claude session on 2026-09-14. Ben's instruction was: "Do a timing run of mega, and record the results (along with this machine's name and any relevant performance information (CPU type, amount of RAM, type of disk, etc.)". Once the first run was under way he added: "I should have said "do as many timing runs as you see fit" so that you could satisfy yourself that the measurement is reasonably consistent". Everything else here is that session's measurement and reconstruction.
Updates and later status: [mega-timing-laptop-2026-09-14-update.md](mega-timing-laptop-2026-09-14-update.md).

**Measured against** `main`: run 1 at `ac24cbd3`, and runs 2 to 4 at `8834ce4b`, whose code is
the same. `8834ce4b` adds only `823be50b`, one regenerated line of `out/vendoring_compare_out.txt`,
and the merge of `460c955f`, which changes documentation and instructions. MAM-private, which the
`accgram-survey-post-stress-meteg` step reads, stood at `8d22f573`. **Re-measure before relying
on a figure**: every mega run prints its step times, and the last section gives the commands.

This is not Phase 1 of `doc/PLAN-mega-speedup.md`. That phase re-measures Ben's Intel Core
i5-13500T desktop, the machine of `doc/mega-timing-2026-09-11.md`; this record times a different
machine.

## Summary: a median of 262.9 s for 55 steps, and consistent from run to run

1. **Four full runs each passed all 55 steps.** The step loop took 269.3, 263.7, 260.5 and 262.0 s,
   a median of 262.9 s and a spread of 3.4%. Each whole invocation took 3.5 to 4.6 s longer, for
   starting Python, importing the steps' modules, the Graphviz check and the closing table.
2. **The steps' times barely moved between runs.** The 15 steps with a median of 5 s or more make
   up 85.6% of the run. Of those 15, 13 varied between their fastest and slowest run by at most 6%.
   The other two, `tmpl-survey` (8.0 to 11.1 s) and `gen-site` (5.6 to 6.3 s), were slowest in
   run 1, and in runs 2 to 4 all 15 stayed within 4%. On the i5-13500T, the 2026-09-11 record's §1
   measured the same step on the same code taking up to 2.6 times as long in one run as in another,
   partly because Windows sometimes ran the mega on an efficiency core. This processor's 16 logical
   processors are all of one kind, which is consistent with the steadier times here but does not
   prove it is the cause.
3. **Run 1 was slower in a few short steps, for no measured reason.** Besides `tmpl-survey` and
   `gen-site`, run 1 took `book-of-job-site` 4.4 s against 2.8 to 3.1 s, `pipeline-graph` 2.6 s
   against 1.1 to 1.9 s, and `render-uxlc-corrections` 1.1 s against 0.1 s. Run 1 was the first
   mega after the full suite and after the call graphs were regenerated. The steps under a second
   show large ratios in the table below mostly because the mega prints step times to 0.1 s.
4. **Nothing else was running.** Total processor load averaged 2.0 to 3.7% in the 60 s before each
   run and 8.8 to 10.2% during it, about one and a half of the 16 logical processors. The mega runs
   one step at a time in one process, except for the `multiprocessing` pool of
   `foi-features-of-interest` and the subprocess steps.
5. **The processor showed no sign of throttling.** Windows' "% Processor Performance" counter, the
   processor's speed against its nominal speed, averaged 190 to 196% during each run, with no
   downward trend from run 1 to run 4. The runs ran from 15:20 to 15:46, with about 90 s of idle sampling
   before each.
6. **A whole run took about as long here as on the i5-13500T, though the two are not strictly
   comparable.** One full run of 59 steps took 285.7 s there on 2026-09-11, on a tree merged with
   `main` at `56132dfd`, as the 2026-09-11 record's §2 notes. Four steps, the Sefaria and OSIS
   steps, have left the mega since, and the code of several of the heaviest remaining steps has
   changed. So this record draws no step-by-step comparison between the two machines.

## The machine

Every figure was read on 2026-09-14 from Windows' own reports: `Win32_Processor`,
`Win32_ComputerSystem`, `Win32_PhysicalMemory`, `Get-PhysicalDisk` and
`powercfg /getactivescheme`.

| Component | What Windows reports |
|---|---|
| Computer | `LAPTOP-DBLE8UKA`, a Microsoft Corporation Surface Laptop 4, x64 |
| Processor | "AMD Ryzen 7 Microsoft Surface (R) Edition", AMD64 Family 23 Model 96 Stepping 1 (Zen 2); 8 cores and 16 logical processors, all of one kind; L2 cache 4 MB, L3 cache 8 MB. The Surface Laptop 4's only 8-core AMD processor is the Ryzen 7 4980U, so that is the chip, by inference. |
| Memory | 16 GB: two 8 GB modules of SMBIOS memory type 30 (LPDDR4) at 4266 MT/s, part number H9HCNNNCPMMLXR-NEE; about 7.7 to 8.0 GB was free before each run |
| Disk | Samsung MZ9LQ512HALU-00000, a 512 GB NVMe SSD, holding the NTFS volume C: with 342 GB free |
| Operating system | Windows 11 Home, build 26200 |
| Power | The High performance plan, on mains power |
| Other | Microsoft Defender real-time protection on; the repository is not under OneDrive |
| Python | 3.13.15, in the repository's `.venv` |
| Graphviz | 16.0.0 (20260814.1018), installed by Ben on 2026-09-14 in place of 15.1.1 |

## What had to change before a run could finish on this machine

1. **Graphviz had to be the pinned 16.0.0.** winget listed 15.1.1 as installed, and the first
   attempt stopped at `tmpl-survey`, the eighth step, after 65 s, on the version check in
   `py/mb_cmn/graphviz_pin.py`. Ben installed 16.0.0.
2. **The call graphs named a font this machine lacked, and that has been fixed in the code rather
   than on the machine.** The second attempt stopped at `tmpl-survey` after 79 s, because
   Graphviz could not load SBL Hebrew. It had already written the fallback-font render over
   `gh-pages/MAM-parsed/plain/svg/plain-call-graph-c.svg`, which was restored. Three commits
   followed that day at Ben's request:
   * `6e731b74` renders each SVG through a temporary file.
   * `3d690c2c` draws the call graphs' nodes in Helvetica, which Graphviz draws with Arial.
   * `ac24cbd3` checks Graphviz and its fonts before the mega's first step.

   `py/mb_cmn/graphviz_pin.py`'s docstring records the reasons. Runs 1 to 4 were made on that
   code, and each printed a passing `GRAPHVIZ CHECK` line before its first step.
3. **Stale cached sizes in the git index made rewritten files look modified.** They came from an
   earlier checkout with CRLF line endings. `git status` reported modified files whose contents
   were identical to HEAD: four after the first attempt, and after run 1
   `py-examples-out/letter-small-job.txt` and `py-examples-out/tmpl_survey_toy.json`. `git add` on
   each refreshed the cache and staged nothing. Before the runs, 12 tracked files were still CRLF
   on disk where `.gitattributes` asks for LF.

## The step times: all 55 steps, four runs

The steps are ranked by their median. Share and cumulative share are of the sum of the medians,
262.4 s. A max/min of "-" marks a step that printed 0.0 s in every run.

| Rank | Step | Run 1 (s) | Run 2 (s) | Run 3 (s) | Run 4 (s) | Median (s) | Min (s) | Max (s) | Max/min | Share | Cumulative |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `accgram-survey-post-stress-meteg` | 48.2 | 48.0 | 47.4 | 48.2 | 48.1 | 47.4 | 48.2 | 1.02 | 18.3% | 18.3% |
| 2 | `accgram-survey-chanted-word-accents` | 22.5 | 22.1 | 21.9 | 21.9 | 22.0 | 21.9 | 22.5 | 1.03 | 8.4% | 26.7% |
| 3 | `wlc-json-and-unicode` | 19.3 | 19.4 | 19.0 | 19.2 | 19.2 | 19.0 | 19.4 | 1.02 | 7.3% | 34.1% |
| 4 | `diff-wsgo` | 17.4 | 17.5 | 17.4 | 17.4 | 17.4 | 17.4 | 17.5 | 1.01 | 6.6% | 40.7% |
| 5 | `multimark` | 15.4 | 16.3 | 15.9 | 16.0 | 15.9 | 15.4 | 16.3 | 1.06 | 6.1% | 46.8% |
| 6 | `uxlc-fois` | 15.3 | 15.8 | 15.4 | 15.6 | 15.5 | 15.3 | 15.8 | 1.03 | 5.9% | 52.7% |
| 7 | `parse-ws` | 15.2 | 15.3 | 15.2 | 15.3 | 15.2 | 15.2 | 15.3 | 1.01 | 5.8% | 58.5% |
| 8 | `accgram-generate-html` | 14.9 | 14.9 | 15.1 | 14.7 | 14.9 | 14.7 | 15.1 | 1.03 | 5.7% | 64.2% |
| 9 | `mam-simple` | 10.5 | 10.8 | 10.7 | 10.7 | 10.7 | 10.5 | 10.8 | 1.03 | 4.1% | 68.2% |
| 10 | `accgram-run-prose` | 9.3 | 9.5 | 9.5 | 9.3 | 9.4 | 9.3 | 9.5 | 1.02 | 3.6% | 71.8% |
| 11 | `tmpl-survey` | 11.1 | 8.2 | 8.0 | 8.0 | 8.1 | 8.0 | 11.1 | 1.39 | 3.1% | 74.9% |
| 12 | `foi-features-of-interest` | 7.6 | 7.7 | 7.7 | 7.6 | 7.7 | 7.6 | 7.7 | 1.01 | 2.9% | 77.8% |
| 13 | `diff-mpplus` | 7.9 | 7.7 | 7.6 | 7.6 | 7.7 | 7.6 | 7.9 | 1.04 | 2.9% | 80.7% |
| 14 | `mam-with-doc` | 6.8 | 6.9 | 6.9 | 6.9 | 6.9 | 6.8 | 6.9 | 1.01 | 2.6% | 83.4% |
| 15 | `gen-site` | 6.3 | 5.8 | 5.6 | 5.7 | 5.8 | 5.6 | 6.3 | 1.12 | 2.2% | 85.6% |
| 16 | `ws-bot-proto` | 4.6 | 4.6 | 4.6 | 4.6 | 4.6 | 4.6 | 4.6 | 1.00 | 1.8% | 87.3% |
| 17 | `book-of-job-site` | 4.4 | 3.1 | 2.8 | 2.8 | 3.0 | 2.8 | 4.4 | 1.57 | 1.1% | 88.4% |
| 18 | `accgram-run-poetic` | 2.8 | 2.9 | 2.9 | 2.8 | 2.8 | 2.8 | 2.9 | 1.04 | 1.1% | 89.5% |
| 19 | `accgram-xcheck-poetic` | 2.1 | 2.2 | 2.2 | 2.2 | 2.2 | 2.1 | 2.2 | 1.05 | 0.8% | 90.4% |
| 20 | `accgram-test-fixes` | 2.3 | 2.1 | 2.0 | 2.0 | 2.0 | 2.0 | 2.3 | 1.15 | 0.8% | 91.1% |
| 21 | `accgram-servi-xcheck` | 2.0 | 2.1 | 2.0 | 2.0 | 2.0 | 2.0 | 2.1 | 1.05 | 0.8% | 91.9% |
| 22 | `accgram-grammaticality` | 1.9 | 1.9 | 1.9 | 1.9 | 1.9 | 1.9 | 1.9 | 1.00 | 0.7% | 92.6% |
| 23 | `parse-go` | 1.6 | 1.6 | 1.6 | 1.6 | 1.6 | 1.6 | 1.6 | 1.00 | 0.6% | 93.2% |
| 24 | `uxlc-amb-early-mtg` | 1.6 | 1.6 | 1.6 | 1.6 | 1.6 | 1.6 | 1.6 | 1.00 | 0.6% | 93.8% |
| 25 | `pipeline-graph` | 2.6 | 1.1 | 1.1 | 1.9 | 1.5 | 1.1 | 2.6 | 2.36 | 0.6% | 94.4% |
| 26 | `search-holam-he-qere` | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 | 1.2 | 1.00 | 0.5% | 94.9% |
| 27 | `estimate-uxlc-locations` | 1.2 | 1.2 | 1.2 | 1.1 | 1.2 | 1.1 | 1.2 | 1.09 | 0.5% | 95.3% |
| 28 | `uxlc-check-changes` | 1.2 | 1.1 | 1.1 | 1.2 | 1.1 | 1.1 | 1.2 | 1.09 | 0.4% | 95.8% |
| 29 | `wordlist` | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.00 | 0.4% | 96.2% |
| 30 | `uxlc-word-list` | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.00 | 0.4% | 96.6% |
| 31 | `uxlc-grammar-test` | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.00 | 0.4% | 97.0% |
| 32 | `sigil-inventory` | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.1 | 1.00 | 0.4% | 97.4% |
| 33 | `clc` | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 | 0.9 | 1.00 | 0.3% | 97.8% |
| 34 | `gen-misc` | 0.9 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.9 | 1.12 | 0.3% | 98.1% |
| 35 | `verify-and-render-table` | 0.8 | 0.7 | 0.8 | 0.8 | 0.8 | 0.7 | 0.8 | 1.14 | 0.3% | 98.4% |
| 36 | `wlc-diffs-420422` | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | 1.00 | 0.3% | 98.7% |
| 37 | `uxlc-write-page-break-info` | 0.6 | 0.6 | 0.6 | 0.6 | 0.6 | 0.6 | 0.6 | 1.00 | 0.2% | 98.9% |
| 38 | `search-final-hiriq-verse-text` | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 1.00 | 0.2% | 99.1% |
| 39 | `explicit-xataf` | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 0.5 | 1.00 | 0.2% | 99.3% |
| 40 | `accgram-run-dual-cant` | 0.4 | 0.4 | 0.4 | 0.4 | 0.4 | 0.4 | 0.4 | 1.00 | 0.2% | 99.5% |
| 41 | `vendored-letter-small-job` | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 1.00 | 0.1% | 99.5% |
| 42 | `accgram-run-printed-decalogue` | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 1.00 | 0.1% | 99.6% |
| 43 | `wlc-a-notes` | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 1.00 | 0.1% | 99.7% |
| 44 | `vendoring-audit` | 0.3 | 0.2 | 0.2 | 0.2 | 0.2 | 0.2 | 0.3 | 1.50 | 0.1% | 99.8% |
| 45 | `diff-ctr-vs-mam` | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 1.00 | 0.0% | 99.8% |
| 46 | `vendored-tmpl-survey-toy` | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 1.00 | 0.0% | 99.8% |
| 47 | `mam-simple-docs` | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 1.00 | 0.0% | 99.9% |
| 48 | `decnreub` | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 1.00 | 0.0% | 99.9% |
| 49 | `render-uxlc-corrections` | 1.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 1.1 | 11.00 | 0.0% | 100.0% |
| 50 | `map-changes-to-book-of-job` | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | 1.00 | 0.0% | 100.0% |
| 51 | `tmpl-survey-toy` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | - | 0.0% | 100.0% |
| 52 | `letter-small-job` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | - | 0.0% | 100.0% |
| 53 | `find-uxlc-accent-changes` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | - | 0.0% | 100.0% |
| 54 | `diffable-pointed-hebrew` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | - | 0.0% | 100.0% |
| 55 | `ac-gen-index-flat-annotated` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | - | 0.0% | 100.0% |
| | **Step loop total** | **269.3** | **263.7** | **260.5** | **262.0** | **262.9** | **260.5** | **269.3** | 1.03 | | |

## Load and wall time, run by run

The load figures are means of one sample a second. "Before" is the 60 s idle sample taken just
before the mega started.

| Run | Started | Load before | Load during | Processor performance before | Processor performance during | Step loop (s) | Invocation (s) |
|---:|---|---:|---:|---:|---:|---:|---:|
| 1 | 15:20:52 | 3.7% | 10.2% | 151% | 195% | 269.3 | 273.9 |
| 2 | 15:29:35 | 3.4% | 9.3% | 150% | 190% | 263.7 | 267.6 |
| 3 | 15:35:40 | 2.1% | 8.8% | 130% | 196% | 260.5 | 264.0 |
| 4 | 15:41:41 | 2.0% | 9.2% | 131% | 196% | 262.0 | 265.6 |

## What was checked, and what did not change

1. **Runs 2, 3 and 4 each left `git status --porcelain` printing nothing**, so every tracked output
   the mega regenerates came out identical to what `8834ce4b` commits.
2. **Run 1 left one content change, which is explained and committed as `823be50b`.** It is the
   last-synced date of the `file_io.py` copy in `out/vendoring_compare_out.txt`, which `6e731b74`
   moved. It also left the two stale-cache entries of the section above, whose contents were
   unchanged.
3. **MAM-private stayed clean**: `git status --porcelain` there printed nothing after run 1 and
   after run 4.
4. **No step was skipped.** This is not a cloud session, and the Graphviz check passed before every
   run.
5. **The runs were not pinned to particular processors**, since every logical processor here is of
   one kind. The 2026-09-11 record pinned its runs to take the i5-13500T's efficiency cores out of
   a comparison.

## How the runs were made

1. **The mega, from the repository root**, with its standard output and standard error captured
   to a file outside the repository. Its `STEP TIME:` lines and closing table are the step times
   above:

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
   ```

2. **The load samples.** A throwaway script ran `typeperf` for 60 s before each run, and again
   once a second for the length of the run, on three counters: `\Processor(_Total)\% Processor
   Time`, `\Processor Information(_Total)\% Processor Performance` and
   `\Memory\Available MBytes`. It also timed the whole mega invocation. The command for the idle
   sample alone:

   ```powershell
   typeperf "\Processor(_Total)\% Processor Time" -si 1 -sc 60
   ```

3. **The sequence.** A throwaway driver started each run only once a 30 s sample of total load
   averaged under 8%, which it did at the first try every time. It killed any mega that ran past
   900 s, which none did. After each run it recorded `git status --porcelain` and would have
   stopped at any change. Runs 2 to 4 ran back to back.
4. **The medians, minimums and maximums** were taken by a throwaway script from the four runs'
   `STEP TIME:` lines.
