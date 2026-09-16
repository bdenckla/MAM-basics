# What a mega run costs in a cloud container, and how to compare it with Ben's machine

Written by a Claude session in a cloud container on 2026-09-14, carrying out Phase 2 of `doc/PLAN-mega-speedup.md`. Ben's words that day were "Do one or more runs of 'mega' in the cloud and record the results in appropriate files in 'doc'. I think the protocol is to use new files to record timings, albeit of an appropriate name such that they will be found, e.g. doc/mega-timing-cloud-2026-09-14.md." He also put the question §4 answers: "I suppose mega may be faster on cloud because it will (by design) lack MAM-private and graphviz, so some stuff will be skipped. I'm not sure how we should 'normalize' for that to be able to compare with local runs with both MAM-private and graphviz present, but perhaps there isn't much need to normalize if those steps aren't really that time consuming anyway." Everything else here is that session's measurement and analysis.
Updates and later status: [mega-timing-cloud-2026-09-14-update.md](mega-timing-cloud-2026-09-14-update.md).

**Measured against** `main` at `89f10bb4`, which the container's branch
`claude/adoring-shannon-8term6` sat on exactly when the runs were made. MAM-private was absent, as
it is in every cloud container. **Re-measure before relying on a figure.** Every mega run prints
its step times, and §8 gives the commands behind every other figure.

The record this one is read beside is `doc/mega-timing-2026-09-11.md`, which timed the mega on
Ben's machine three days earlier; call it the dated record. Its columns are quoted here as "Ben
pinned, after", the committed code pinned to logical processors 0-11, which is its most repeatable
column.

## Summary: 249 s of steps, one step skipped, and normalizing does matter

1. **A full cloud run takes 249.0 s in its 54 executed steps**, the median of three runs, and
   250.6 to 273.5 s of wall time (§2, §3). All 55 steps of the current mega either ran or were
   skipped for the cloud, no step failed, and each run ended `MEGA RUN IS CLOUD-COMPLETE`.
2. **Normalizing does matter, and Ben's guess that it might not is the one thing here that came
   out the other way.** The single step a cloud run skips,
   `accgram-survey-post-stress-meteg`, is the most expensive step in the whole mega on Ben's
   machine: 40.9 s, which is 16.5% of a comparable run there (§4). Comparing a cloud total with a
   Ben's-machine total understates the cloud by about that much.
3. **No arithmetic normalization is needed all the same, because the fix is to compare step by
   step rather than total to total** — which is what Phase 2 of `doc/PLAN-mega-speedup.md` already
   requires. Over the 52 steps that ran to completion in both places, the cloud takes 235.0 s
   against Ben's pinned 207.6 s, a ratio of **1.13** (§4).
4. **Against Ben's *unpinned* run the cloud is a dead heat**, 235.0 s against 232.5 s, a ratio of
   1.01 (§4). A cloud container is slower than Ben's performance cores and about as fast as his
   machine when Windows is free to use the efficiency cores.
5. **The container is far more repeatable than Ben's machine**, which is the most useful property
   it has for this work. Runs 2 and 3 differ by more than 0.5 s on exactly two steps, and by no
   more than 0.6 s on any step, against the up-to-2.6-times swings the dated record's §1 records
   (§6).
6. **Run 1 is a cold-cache run and should not be pooled with the other two.** It costs 27.9 s more
   than the faster of runs 2 and 3, and 14.4 s of that is `diff-mpplus` alone, which reads git
   objects (§6).
7. **Two tracked outputs change on every cloud run, and neither was committed**, both for the
   shallow-clone reason Phase 2's step 6 predicted. The mechanism is sharper than the one
   `py/subcommands/diff_mpplus.py` anticipates, and §7 records it as a finding rather than fixing
   it, Phase 2 being forbidden to change code.

## 1. The container

| What | Value |
|---|---|
| `CLAUDE_CODE_REMOTE` | `true` |
| `git rev-parse HEAD` | `89f10bb437d60af3279a72c72be9b6aa866c5bf8`, equal to `origin/main` |
| Branch | `claude/adoring-shannon-8term6` |
| `git rev-parse --is-shallow-repository` | `true` |
| Commits in the shallow window | 153 |
| `nproc` | 4 |
| CPU | Intel Xeon @ 2.80GHz, 4 cores, 1 thread per core |
| Memory | 15 GiB, no swap |
| `python3 --version` | 3.11.15 |
| Graphviz `dot` on the path | absent, as expected |
| MAM-private | absent |
| `/proc/loadavg` before runs 1, 2, 3 | 0.45, 0.55, 0.99 |

Three of those deserve a sentence.

1. **Python is 3.11.15, not the 3.13.12 Phase 2 expected** from the container measured on
   2026-09-11, and not the 3.13.15 the dated record's machine ran. A cloud container's Python
   version is therefore not stable across containers, and a figure here carries 3.11.15 with it.
2. **The shallow window is 153 commits, not the 221 of the container measured on 2026-09-11.**
   That difference is what makes §7's finding fire here and not there.
3. **Four processors, against the 20 logical processors of the dated record's i5-13500T.** Only
   `foi-features-of-interest` starts a `multiprocessing` pool, and it is one of the steps the
   cloud runs *faster* than Ben's machine, so the processor count did not dominate any figure
   here.

**The packages had to be installed, and the plan's command for it does not work as written.**
`python3 py/main_test.py --collect-only -q` failed on `No module named 'pytest'`, and
`python3 -m pip install -r requirements.txt` then failed with
`Cannot uninstall packaging 24.0, RECORD file not found. Hint: The package was installed by
debian.` The install that worked was
`python3 -m pip install --ignore-installed packaging -r requirements.txt`, which took 23.2 s after
the 20.6 s the failing attempt had already spent. Neither figure is inside any run below. After
it, 993 tests collected, with one collection error in
`py/tests/test_ws_bot_real_diff_links.py` from pywikibot wanting a user-config.

**That collection error belongs to the suite and not to the mega, and no mega run goes near
pywikibot or near a live wiki.** Ben asked on 2026-09-14, seeing the error reported, whether the
mega involved pywikibot and whether what ran was the dry run rather than the live one. It is the
dry run, and three separate facts say so. **`ws-bot-proto` is the only bot step the mega has**, and
`py/subcommands/ws_bot_proto.py`'s docstring describes it as prototyping "the Wikisource bot using
local file I/O instead of live server I/O", exercising the same edit logic but reading and writing
local files "rather than making live Wikisource API calls". **The live path is a different
subcommand that the mega never names**: `py/main_0_mega.py` mentions `ws_bot_proto` at its import
and at its step, and `main_ws_bot` and `ws_bot_real` nowhere. **Exactly one module in the
repository imports pywikibot**, `py/subcommands/ws_bot_real.py`, which is that live path; importing
`main_0_mega` leaves `pywikibot` out of `sys.modules` altogether, and the string does not occur
once in any of the three run logs.

## 2. How the three runs were made

Each run was the plain command of Phase 2's step 4, from the repository root, captured to an
untracked file outside the repository:

```bash
python3 py/main_0_mega.py > <untracked file> 2>&1
```

All three exited 0 and ran all 55 steps. Between runs the four tracked files of §7 were restored,
so each run started from a clean tree.

| Run | Wall (s) | The mega's own step-loop total (s) | Startup (s) |
|---|---:|---:|---:|
| 1 | 273.5 | 271.3 | 2.2 |
| 2 | 250.6 | 248.4 | 2.2 |
| 3 | 251.5 | 249.4 | 2.1 |

Startup is each run's wall time less its step-loop total, and covers starting the interpreter and
importing every step's module. At 2.1 to 2.2 s it sits inside the 1.9 to 3.0 s the dated record
measured on Ben's machine, so a container starts the mega no more slowly than Ben's machine does.

## 3. Where the time goes: all 55 steps

The median of the three runs ranks the steps, and its share and cumulative share are of the
249.0 s that the 54 executed steps take. "Ben pinned, after" is the dated record's §3 column for
the committed code pinned to logical processors 0-11, and "Cloud / Ben" divides this file's median
by it. A blank ratio means the two figures do not compare: `diff-mpplus` and `gen-site` both
*raised* partway through in the dated record, so its figures for them are times until they raised
rather than durations, and both have been fixed since.

| Rank | Step | Run 1 (s) | Run 2 (s) | Run 3 (s) | Median (s) | Share | Cumulative | Ben pinned, after (s) | Cloud / Ben |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `wlc-json-and-unicode` | 35.4 | 32.8 | 32.8 | 32.8 | 13.2% | 13.2% | 18.4 | 1.78 |
| 2 | `accgram-survey-chanted-word-accents` | 26.5 | 26.2 | 26.8 | 26.5 | 10.6% | 23.8% | 22.0 | 1.20 |
| 3 | `accgram-generate-html` | 18.6 | 20.2 | 19.8 | 19.8 | 8.0% | 31.8% | 12.3 | 1.61 |
| 4 | `diff-wsgo` | 19.2 | 19.9 | 19.5 | 19.5 | 7.8% | 39.6% | 14.6 | 1.34 |
| 5 | `uxlc-fois` | 18.0 | 17.8 | 17.9 | 17.9 | 7.2% | 46.8% | 14.3 | 1.25 |
| 6 | `parse-ws` | 20.0 | 17.6 | 17.4 | 17.6 | 7.1% | 53.9% | 15.2 | 1.16 |
| 7 | `multimark` | 16.9 | 16.6 | 16.8 | 16.8 | 6.7% | 60.6% | 13.7 | 1.23 |
| 8 | `accgram-run-prose` | 12.8 | 13.0 | 13.4 | 13.0 | 5.2% | 65.8% | 8.3 | 1.57 |
| 9 | `mam-simple` | 11.2 | 10.6 | 10.8 | 10.8 | 4.3% | 70.2% | 17.6 | 0.61 |
| 10 | `diff-mpplus` | 21.5 | 7.1 | 7.7 | 7.7 | 3.1% | 73.3% | 8.1 (raised) | -- |
| 11 | `mam-with-doc` | 6.9 | 7.2 | 7.3 | 7.2 | 2.9% | 76.1% | 7.9 | 0.91 |
| 12 | `foi-features-of-interest` | 6.9 | 6.7 | 6.5 | 6.7 | 2.7% | 78.8% | 10.9 | 0.61 |
| 13 | `gen-site` | 6.3 | 6.4 | 6.2 | 6.3 | 2.5% | 81.4% | 0.0 (raised) | -- |
| 14 | `ws-bot-proto` | 5.7 | 5.5 | 5.5 | 5.5 | 2.2% | 83.6% | 4.7 | 1.17 |
| 15 | `accgram-run-poetic` | 3.4 | 3.2 | 3.3 | 3.3 | 1.3% | 84.9% | 2.4 | 1.38 |
| 16 | `accgram-grammaticality` | 3.4 | 3.2 | 3.1 | 3.2 | 1.3% | 86.2% | 2.0 | 1.60 |
| 17 | `book-of-job-site` | 6.0 | 2.7 | 2.9 | 2.9 | 1.2% | 87.3% | 3.9 | 0.74 |
| 18 | `accgram-test-fixes` | 2.7 | 2.4 | 2.6 | 2.6 | 1.0% | 88.4% | 4.8 | 0.54 |
| 19 | `accgram-xcheck-poetic` | 2.4 | 2.3 | 2.4 | 2.4 | 1.0% | 89.4% | 2.6 | 0.92 |
| 20 | `parse-go` | 2.3 | 2.3 | 2.3 | 2.3 | 0.9% | 90.3% | 1.7 | 1.35 |
| 21 | `accgram-servi-xcheck` | 2.1 | 2.0 | 2.2 | 2.1 | 0.8% | 91.1% | 1.6 | 1.31 |
| 22 | `uxlc-amb-early-mtg` | 1.9 | 2.1 | 2.0 | 2.0 | 0.8% | 92.0% | 1.1 | 1.82 |
| 23 | `tmpl-survey` | 1.9 | 1.7 | 1.8 | 1.8 | 0.7% | 92.7% | 8.4 | 0.21 |
| 24 | `estimate-uxlc-locations` | 1.5 | 1.9 | 1.7 | 1.7 | 0.7% | 93.4% | 0.9 | 1.89 |
| 25 | `uxlc-grammar-test` | 1.6 | 1.7 | 1.7 | 1.7 | 0.7% | 94.1% | 1.0 | 1.70 |
| 26 | `wordlist` | 1.7 | 1.5 | 1.5 | 1.5 | 0.6% | 94.7% | 1.0 | 1.50 |
| 27 | `search-holam-he-qere` | 1.4 | 1.4 | 1.4 | 1.4 | 0.6% | 95.2% | 0.9 | 1.56 |
| 28 | `uxlc-word-list` | 1.3 | 1.4 | 1.4 | 1.4 | 0.6% | 95.8% | 0.8 | 1.75 |
| 29 | `uxlc-check-changes` | 1.4 | 1.3 | 1.3 | 1.3 | 0.5% | 96.3% | 1.5 | 0.87 |
| 30 | `wlc-diffs-420422` | 1.3 | 1.4 | 1.3 | 1.3 | 0.5% | 96.8% | 0.7 | 1.86 |
| 31 | `sigil-inventory` | 1.3 | 1.3 | 1.3 | 1.3 | 0.5% | 97.4% | 1.1 | 1.18 |
| 32 | `clc` | 1.1 | 1.3 | 1.2 | 1.2 | 0.5% | 97.8% | 0.9 | 1.33 |
| 33 | `verify-and-render-table` | 1.2 | 1.3 | 1.2 | 1.2 | 0.5% | 98.3% | 0.7 | 1.71 |
| 34 | `uxlc-write-page-break-info` | 0.9 | 0.9 | 0.9 | 0.9 | 0.4% | 98.7% | 0.4 | 2.25 |
| 35 | `gen-misc` | 0.8 | 0.8 | 0.8 | 0.8 | 0.3% | 99.0% | 1.1 | 0.73 |
| 36 | `search-final-hiriq-verse-text` | 0.6 | 0.6 | 0.6 | 0.6 | 0.2% | 99.2% | 0.4 | 1.50 |
| 37 | `explicit-xataf` | 0.5 | 0.5 | 0.5 | 0.5 | 0.2% | 99.4% | 0.4 | 1.25 |
| 38 | `accgram-run-dual-cant` | 0.5 | 0.5 | 0.5 | 0.5 | 0.2% | 99.6% | 0.4 | 1.25 |
| 39 | `accgram-run-printed-decalogue` | 0.3 | 0.3 | 0.3 | 0.3 | 0.1% | 99.7% | 0.3 | 1.00 |
| 40 | `mam-simple-docs` | 0.3 | 0.2 | 0.2 | 0.2 | 0.1% | 99.8% | 0.1 | 2.00 |
| 41 | `diff-ctr-vs-mam` | 0.1 | 0.1 | 0.1 | 0.1 | 0.0% | 99.8% | 0.1 | 1.00 |
| 42 | `decnreub` | 0.1 | 0.1 | 0.1 | 0.1 | 0.0% | 99.9% | 0.1 | 1.00 |
| 43 | `render-uxlc-corrections` | 1.3 | 0.1 | 0.1 | 0.1 | 0.0% | 99.9% | 0.2 | 0.50 |
| 44 | `find-uxlc-accent-changes` | 0.1 | 0.1 | 0.1 | 0.1 | 0.0% | 99.9% | 0.0 | -- |
| 45 | `wlc-a-notes` | 0.1 | 0.1 | 0.1 | 0.1 | 0.0% | 100.0% | 0.2 | 0.50 |
| 46 | `tmpl-survey-toy` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0% | 100.0% | 0.0 | -- |
| 47 | `vendored-tmpl-survey-toy` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0% | 100.0% | 0.1 | 0.00 |
| 48 | `letter-small-job` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0% | 100.0% | 0.0 | -- |
| 49 | `vendored-letter-small-job` | 0.0 | 0.1 | 0.0 | 0.0 | 0.0% | 100.0% | 0.2 | 0.00 |
| 50 | `map-changes-to-book-of-job` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0% | 100.0% | 0.0 | -- |
| 51 | `diffable-pointed-hebrew` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0% | 100.0% | 0.2 | 0.00 |
| 52 | `ac-gen-index-flat-annotated` | 0.1 | 0.0 | 0.0 | 0.0 | 0.0% | 100.0% | 0.0 | -- |
| 53 | `pipeline-graph` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0% | 100.0% | 2.4 | 0.00 |
| 54 | `vendoring-audit` | 0.0 | 0.0 | 0.0 | 0.0 | 0.0% | 100.0% | 3.1 | 0.00 |
| -- | `accgram-survey-post-stress-meteg` (skipped for the cloud) | -- | -- | -- | -- | -- | -- | 40.9 | -- |

**The five steps of the dated record that have since left the mega do not appear**, because the
mega no longer has them: `near-aleppo-census`, removed 2026-09-11, and `mam4sef-and-ajf`,
`mam-osis`, `vendored-mam4sef` and `vendored-mam-osis`, removed 2026-09-12, as
`doc/mega-timing-2026-09-11-update.md` records. They were worth 46.1 s between them at Ben's
pinned speed, so the mega has lost roughly that much since the dated record, quite apart from
anything measured here.

## 4. What the cloud does not do, and whether to normalize for it

**The answer to Ben's question is that normalizing does matter, but that comparing step by step
rather than total to total is the whole of the normalization needed.** The
guess in the question — that the skipped work might not be time consuming enough to bother
with — is the one place the measurement disagrees.

**A cloud run omits three things, and one of them is the mega's single most expensive step.**

1. **`accgram-survey-post-stress-meteg` is skipped altogether**, by Ben's decision of
   2026-09-10, because it reads MAM-private's Phonetic MAM. On Ben's machine it is **40.9 s**,
   the largest step in the dated record's pinned column. `gen-site` then renders the nine
   post-stress-meteg pages from the tracked `out/accgram/post-stress-meteg.json` unchanged, which
   is why the pages still come out right.
2. **`tmpl-survey` skips twelve SVG renders**, falling from 8.4 s on Ben's machine to 1.8 s here,
   a ratio of 0.21 against a container that is otherwise slower.
3. **`pipeline-graph` skips two SVG renders**, falling from 2.4 s to below the 0.05 s the step
   timer rounds away.

Every run printed `MEGA RUN IS CLOUD-COMPLETE: 1 step(s) and 14 SVG render(s) skipped for the
cloud`, and 14 is those twelve plus those two.

**So the skipped step alone is 16.5% of a Ben's-machine run of the same 55-step mega**, taking
that run to be the 207.6 s of comparable steps plus its own 40.9 s. A reader who set the cloud's
249.0 s against a Ben's-machine total would be comparing a run that did less with one that did
more, and would credit the container with a speed it does not have.

**The like-for-like comparison, over the 52 steps that ran to completion in both places:**

| Compared with | Cloud (s) | Ben's machine (s) | Cloud / Ben |
|---|---:|---:|---:|
| Ben pinned to logical processors 0-11, committed code | 235.0 | 207.6 | **1.13** |
| Ben unpinned, run 1 of the dated record | 235.0 | 232.5 | **1.01** |

Those 52 steps are the 54 the cloud executed less `diff-mpplus` and `gen-site`, which raised in
the dated record and so have no duration there to compare against.

**Read the two rows together rather than picking one.** Against Ben's performance cores the
container is 13% slower; against his machine as Windows actually schedules it when unpinned, the
two are level. The dated record's §1 is what makes the second row fair game rather than a
curiosity: on the i5-13500T the same step took up to 2.6 times as long in one run as in another,
depending on which core Windows gave it, so "Ben's machine" is a range and not a number.

**The per-step ratio is a better instrument than either total.** Its median over the 47 steps that
have one is 1.23, and over the 20 steps worth at least 2.0 s on Ben's machine it is 1.16, with an
aggregate of 1.11. The three agree closely enough that **a rough conversion of 1.1 to 1.2 times
Ben's pinned figure will predict a cloud step's cost**, with the exceptions of §5.

## 5. Which steps differ most between the container and Ben's machine

**Both lists below are pointers for later work rather than explanations**, as Phase 2's purpose 2
says. Nothing here was profiled.

**Slower in the container, among steps worth at least 2 s on Ben's machine:**

| Cloud / Ben | Step | Cloud (s) | Ben pinned, after (s) |
|---:|---|---:|---:|
| 1.78 | `wlc-json-and-unicode` | 32.8 | 18.4 |
| 1.61 | `accgram-generate-html` | 19.8 | 12.3 |
| 1.60 | `accgram-grammaticality` | 3.2 | 2.0 |
| 1.57 | `accgram-run-prose` | 13.0 | 8.3 |
| 1.38 | `accgram-run-poetic` | 3.3 | 2.4 |
| 1.34 | `diff-wsgo` | 19.5 | 14.6 |

**`wlc-json-and-unicode` is the one to look at first.** It is the slowest step of a cloud run at
32.8 s and 13.2% of it, where on Ben's machine it ranks sixth; its 1.78 is the worst ratio of any
large step. Four of the other five above are accgram steps, which suggests the accgram scanners
suit the i5-13500T better than this Xeon, though nothing here establishes why.

**Faster in the container, same threshold:**

| Cloud / Ben | Step | Cloud (s) | Ben pinned, after (s) |
|---:|---|---:|---:|
| 0.00 | `pipeline-graph` | 0.0 | 2.4 |
| 0.00 | `vendoring-audit` | 0.0 | 3.1 |
| 0.21 | `tmpl-survey` | 1.8 | 8.4 |
| 0.54 | `accgram-test-fixes` | 2.6 | 4.8 |
| 0.61 | `mam-simple` | 10.8 | 17.6 |
| 0.61 | `foi-features-of-interest` | 6.7 | 10.9 |

**Two of those six are the Graphviz skips of §4 and mean nothing about the hardware**:
`pipeline-graph` and `tmpl-survey`. **`vendoring-audit` is the interesting one**, falling from
3.1 s to below rounding. It spends its time in `git log -1` per vendored file through
`py/vendoring/compare.py`, so it is dominated by process spawning, which Linux does far more
cheaply than Windows. `accgram-test-fixes`, `mam-simple` and `foi-features-of-interest` are
genuinely faster here and unexplained; `foi-features-of-interest` is the one step that starts a
`multiprocessing` pool, and it is faster on 4 processors than on 20, which is worth somebody's
curiosity but not a claim.

## 6. Run 1 is a cold-cache run, and runs 2 and 3 are the repeatable pair

**Run 1 costs 27.9 s more than the faster of runs 2 and 3**, summed over the steps where it is
slower, and the excess is concentrated rather than spread:

| Step | Run 1 (s) | Run 2 (s) | Run 3 (s) | Run 1 excess (s) |
|---|---:|---:|---:|---:|
| `diff-mpplus` | 21.5 | 7.1 | 7.7 | +14.4 |
| `book-of-job-site` | 6.0 | 2.7 | 2.9 | +3.3 |
| `parse-ws` | 20.0 | 17.6 | 17.4 | +2.6 |
| `wlc-json-and-unicode` | 35.4 | 32.8 | 32.8 | +2.6 |
| `render-uxlc-corrections` | 1.3 | 0.1 | 0.1 | +1.2 |

**`diff-mpplus` is over half of it**, and it is the step that reads git objects, which is what a
first run has to fault in from disk. Nothing changed in the repository between the runs, so the
page cache is the only candidate on offer here, and no experiment was run to confirm it.

**Runs 2 and 3 agree to within 0.6 s on every step**, and differ by more than 0.5 s on only two:
`accgram-survey-chanted-word-accents`, 26.2 against 26.8, and `diff-mpplus`, 7.1 against 7.7. Set
that against the dated record's §1, where two unpinned runs on Ben's machine put
`near-aleppo-census` at 17.6 and 43.4 s and `mam4sef-and-ajf` at 4.2 and 11.0 s with nothing
changed. **A container is the better place to measure a speedup**, which is worth knowing for the
items of `doc/PLAN-mega-speedup.md` that still need attributing — with the caveat that the
container cannot measure the one step it skips.

**So the medians of §3 are medians of three, but a future run should discard its first.** The
251 s of runs 2 and 3 is the figure to quote for a warm container, and the 273 s of run 1 the
figure for a fresh one.

## 7. What the runs changed in the tree, why none of it was committed, and one finding

**Every run left exactly the same four tracked files modified, and all four were restored rather
than committed**, as Phase 2 requires:

```
 M doc/vendoring-inventory.md
 M gh-pages/MAM-with-doc/change-log/unpinned-latest.html
 M gh-pages/MAM-with-doc/change-log/unpinned-latest.json
 M out/vendoring_compare_out.txt
```

**Both are the shallow-clone effects Phase 2's step 6 names, and neither is a defect in the
code.** No other file changed, and **no `.dot` file changed**, so the hazard the cloud banner
warns about — a rewritten `.dot` committed without the `.svg` a container cannot render — did not
arise.

**The finding, which is raised here and not fixed:** the mechanism is not quite the one
`py/subcommands/diff_mpplus.py` anticipates, and it is worth recording because it makes the wrong
date easier to hit than that docstring suggests.

That docstring, under "THE ONE GIT READING LEFT", expects the failure to be a walk that finds
*nothing*: "If no commit inside the window touched `MAM-parsed/plus`, that walk finds nothing and
the date falls back to HEAD's own." What happens in this container instead is that the walk finds
a commit that never touched `MAM-parsed/plus` at all. **A shallow clone's graft boundaries have no
parent object, so git shows every file in such a commit as added**, and a path-filtered walk
therefore stops at one. This container's `.git/shallow` names three commits, of which `d3ab7cf`
(2026-09-12) is the newest, and `git log -1 -- MAM-parsed/plus` returns `d3ab7cf` although its
subject is "Correct finding 8 State declarations" and its real change is documentation.

The consequence is exactly the class of wrongness the docstring predicts — a wrong date in a
published report rather than a wrong diff — and the diff is demonstrably intact:

| Field of `unpinned-latest.json` | Committed | This container |
|---|---|---|
| `new_rev` | `73c6b1137777ad1a522949fcea290f8ac1f87a7b` | `d3ab7cf16949c44d5c1d5fe01c53f311d38afadf` |
| report date | 2026-09-11 | 2026-09-12 |
| `diff_count` | 69 | 69 |

**`vendoring-audit` fails the same way and shows it more plainly.** It dates each vendored copy by
that copy's last commit, and all three copies collapse onto the graft boundary's date at once:
`file_io.py` from 2026-09-11 to 2026-09-12, `provenance.py` from 2026-09-10 to 2026-09-12, and
`letter_small_job.py` from 2026-09-08 to 2026-09-12. Three different true dates becoming one
shared wrong date is the graft boundary's signature.

**Why this is not fixed here**: Phase 2 of `doc/PLAN-mega-speedup.md` says in terms that it must
change no code. The 2026-09-11 container did not see this because 3 commits inside its 221-commit
window genuinely touched `MAM-parsed/plus`, so its walk stopped at a real one before reaching a
graft boundary. Whether to guard it is a decision for Ben, and the docstring's own reason for
recording rather than guarding — that guarding means raising, which 2026-09-11's work removed —
still applies.

## 8. Commands behind the figures

1. **Step times.** Every mega run prints them: a `STEP TIME:` line after each step, and a closing
   table, which also marks a step skipped for the cloud. The three runs are the three plain
   invocations of §2. The per-step figures here were parsed from those lines and checked against
   each run's own closing table, which agreed to the 0.1 s the table rounds to.
2. **Wall time and startup.** Each run was wrapped by reading `date +%s.%N` before and after, and
   startup is that wall time less the step-loop total the mega prints.
3. **The environment table of §1.** `git rev-parse HEAD`, `git rev-parse
   --is-shallow-repository`, `git rev-list --count HEAD`, `nproc`, `lscpu`, `free -h`,
   `python3 --version`, `command -v dot` and `cat /proc/loadavg`.
4. **The graft-boundary finding of §7.** `cat .git/shallow` lists the boundaries;
   `git log -1 -- MAM-parsed/plus` shows which commit the path-filtered walk stops at; and
   `git cat-file -p d3ab7cf` shows that its parent `eb79e61` is named but absent, which is what
   makes git treat every file in it as added.
5. **The like-for-like totals of §4.** The dated record's §3 table was parsed for its "Pinned,
   after" column, `diff-mpp` was mapped to its current name `diff-mpplus`, and that step and
   `gen-site` were excluded as having raised there. The throwaway scripts that did the parsing
   were not kept; they read only the three captured run logs and
   `doc/mega-timing-2026-09-11.md`, both of which are still here, so any figure above can be
   re-derived from them.
6. **The tree checks of §7.** `git status --porcelain` after each run, `git diff` on each of the
   four files, and `git restore` on the same four before the next run.
7. **That the mega never reaches pywikibot or a live wiki (§1).**
   `grep -rnE "^\s*(import|from)\s+pywikibot" py/ --include=*.py` returns the single line
   `py/subcommands/ws_bot_real.py:18`; `grep -n "ws_bot" py/main_0_mega.py` returns only the
   `ws_bot_proto` import and step; and a throwaway script that imports `main_0_mega` and then
   tests `"pywikibot" in sys.modules` prints `False`.
