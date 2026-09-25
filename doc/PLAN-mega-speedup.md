# PLAN — make the mega run faster

State: live. Phase 2 executed 2026-09-14; no other phase started as of that date.

Written by a Claude session on 2026-09-14. Ben's instructions that day, said of the changes to the
mega since 2026-09-11 that the session had just listed for him: "Should other updates you mention
above (for instance removal of Sefaria from mega) be incorporated in the plan? I think so, so
unless you strongly disagree, please incorporate them." And: "Also include in the plan (but do not
do) some re-measurements, particularly on an otherwise-unloaded machine, and some measurements of
mega running in a cloud session". The plan he meant is `doc/mega-timing-2026-09-11.md`, whose §7
proposes the speedups; that file records Ben's reason for the work as "I think the most
interesting direction to go in is to make mega run faster than to keep running mostly useless or
entirely useless test suite entries".

Everything below other than Ben's quoted words is that session's reconstruction. **Re-measure
every figure before relying on it**; each names the record it comes from or the command that
re-establishes it, and a mismatch is a finding to record rather than a number to overwrite.

## The measurement record, and where the status of its proposals is kept

`doc/mega-timing-2026-09-11.md` is the measurement this plan rests on; call it the dated record.
It timed the mega's 60 steps on Ben's machine, at `main` `132f2f3e` plus the four commits of the
branch that added step timing and the first two speedups. It is a finished dated document and
stays as written, under Ben's rule of 2026-09-11, and its sibling
`doc/mega-timing-2026-09-11-update.md` points here. **The status of each proposal in the dated
record's §7 is kept in this plan.** The wording of §7 itself describes 2026-09-11. So did the
bodies of #272 and #273 until 2026-09-14, when a Claude session, with Ben's approval, corrected
their stale statements and commented on each issue with a link to this plan.

`doc/mega-timing-laptop-2026-09-14.md` times the current mega on a second machine, a Surface
Laptop 4 whose AMD Ryzen 7 has 16 logical processors, all of one kind. It records four full runs
of 55 steps at `ac24cbd3` and `8834ce4b`, with a median of 262.9 s in the step loop. It is not
Phase 1, which re-measures Ben's i5-13500T, and its per-step figures are no baseline for that
machine.

**This plan holds more proposals than the dated record's twelve.** Items 13 to 15, added
2026-09-14 at Ben's request, come from reading the post-stress-meteg survey's code rather than from
any measurement, and have their own section below. Item numbers run 1 to 15 across the two
sections, so a reference to an item number needs no further qualification.

Two speedups were made and measured with the dated record, and both are on `main`: `15c09692` gave
the prose scanner a fast path, cutting its time from 75.3 s to 21.1 s over the eight steps that
call it, and `af1c404a` made the JSON writer use `json.dumps`, saving about 15.8 s a run (the dated
record's §5).

## Preconditions

- **Baseline suite at `bca64824`:** the repository suite passed 997 tests with 5 skipped.
  Re-run the suite at the execution baseline and record the new counts before relying on that
  baseline.
- **Repository**: `C:/Users/BenDe/GitRepos/MAM-basics`, with every command run from its root. The
  interpreter is `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`, spelled
  absolutely in a secondary worktree. Phase 2 uses the cloud container's own `python3`.
- **Instruction files to load first**: `~/.claude/CLAUDE.md` and this repository's `CLAUDE.md`,
  in particular its sections "Integrating a worktree branch here" and "What this repository's
  products are". The `hebrew-prose` skill is not needed for Phases 1 and 2, which write only
  timing records. Load it before editing any docstring or comment under `py/accgram/`, which
  items 3, 4, 7 and 13 to 15 would do.
- **Another session may be live in this repository.** Code work goes in a worktree. Timing work
  cannot share the machine at all: the dated record's §1 discarded a baseline run because a mega
  started from another worktree slowed it, `parse-ws` taking 40.4 s against 12.8 to 15.2 s.
- **Phases 1 and 2 do not depend on each other or on any item**, and no item depends on either
  phase. Running Phase 1 before implementing an item gives that item a current baseline.
- **The step list**: 55 steps at `bca64824`, against the 60 the dated record timed. `--help`
  prints every step's name among the choices of `--resume-from`:

  ```powershell
  C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py --help
  ```

## What has changed since the dated record's runs

- **A full run is one invocation again.** The two steps that raised in the dated record's runs
  were both fixed on 2026-09-11, `diff-mpplus` by `f11ecaf8` and `gen-site` by `aedac688`. One
  full run on a tree merged with `main` at `56132dfd` then passed all 59 steps in 285.7 s, as the
  note in the dated record's §2 says.
- **`diff-mpp` has been called `diff-mpplus` since `8b2386b0`** (2026-09-11). The dated record
  keeps the old name.
- **Four Sefaria and OSIS steps left the mega on 2026-09-12**: `mam4sef-and-ajf`, `mam-osis`,
  `vendored-mam4sef` and `vendored-mam-osis`. They left for a product reason, not for speed. Ben:
  "I know of no reason to be supplying constantly-updated versions of these", quoted in full in
  `bf4a6c5e` and in `py/main_0_mega.py` where two of the steps stood. `d6a6764d` retired the two
  example programs and their `vendored-*` steps; `bf4a6c5e` removed the other two steps and
  declared their programs in `py/tests/test_mega_coverage.py`'s `NOT_IN_MEGA`. Together the four
  took 8.2, 20.7, 11.2 and 15.7 s in the dated record's four runs, summing its §3 rows. A session
  estimated on 2026-09-12, from those runs alone, that removing them saves about 5% of a run,
  roughly 11 to 14 s of 285.7 s. **No run has measured that saving**; step 7 of Phase 1 can. All
  four hang off `mam-simple` and lie on neither of item 1's long chains, so under item 1 their
  removal would save almost nothing.
- **MAM-simple's tree was recorded as shrinking from 107.7 MB to 37.7 MB on 2026-09-12, but the
  post-shrink figure is not reproducible from the preserved evidence.** The session attributed the
  figures to `du -sb` but preserved neither its raw output nor the exact working-tree state. At
  `bca64824`, the tracked files total 37,647,285 bytes, or 37.6 MB. Treat 37.7 MB as an unverified
  historical filesystem measurement unless preserved evidence re-establishes it. `b653e9b9`
  retired `MAM-simple/misc/Torah-letters-only/`; `d6a6764d` removed the example programs' output;
  `dcd2c1f6` removed the bhs and sef Unicode-names trees; `3b1adf45` writes a bhs or sef corpus file
  only where it differs from the vtrad-mam one, and dropped `yeivinID`; `20f18020` then took the
  choice of which bhs and sef files to write from the versification tables. **The `mam-simple`
  step has not been timed on Ben's machine since.** On
  the Surface Laptop 4 of `doc/mega-timing-laptop-2026-09-14.md` it took a median of 10.7 s on
  2026-09-14, a figure from a different machine and so not comparable with the dated record's
  11.3 to 18.1 s. A throwaway script
  that sums the sizes of the files `git ls-files -z -- MAM-simple` names re-establishes the
  tracked tree's size.
- **The code of the heaviest steps has changed**, so the dated record's per-step figures are
  history rather than a baseline. On 2026-09-14 at `bca64824` the command below listed 14 commits
  that are not merges. Two are the dated record's speedups, `af1c404a` and `15c09692`. The other
  twelve are four MAM-simple commits (`d6a6764d`, `dcd2c1f6`, `3b1adf45`, `20f18020`),
  `6dbd27e7`, the three template-projection commits (`2239cbad`, `5cb06e25`, `1b7b97ef`), and four
  mpplus commits (`fa517040`, `8b2386b0`, `cde921bf`, `7fd381db`).

  ```powershell
  git -C C:/Users/BenDe/GitRepos/MAM-basics log --no-merges --format="%h %ad %s" --date=short 132f2f3e..HEAD -- py/main_mam_simple.py py/main_tmpl_survey.py py/tmpl_survey py/subcommands py/accgram py/main_accgram.py py/mb_cmn/file_io.py py/main_wlc_json_and_unicode.py py/main_fois.py py/main_mam_with_doc.py py/main_multimark.py
  ```

- **`doc/PLAN-retire-google-sheet.md`, which is live, would remove two more steps**, `parse-go`
  and `diff-wsgo`, which took 1.1 to 3.5 s and 12.4 to 16.1 s in the dated record's runs. If that
  plan runs first, Phase 1 times two fewer steps, and item 6 shrinks to the one repeated parse
  left, in `ws-bot-proto`.

## The dated record's twelve §7 items, and what has become of each

Each estimate is the dated record's, made on Ben's machine before the changes above. Statuses are
as of 2026-09-14. Before starting an item, check its issue, where it has one, with
`gh issue view <number> --repo bdenckla/MAM-basics --json state,comments`, and the recent history
of the code the item names.

1. **Run independent steps at the same time.** Estimated saving: more than half of a run. The 60
   steps took 302.7 s one after another in the dated record's pinned run of the committed code,
   and the longer of its two chains of dependent steps took 77.8 s, so a run might take 90 to
   120 s. Risk: high. **Filed as #272, open, not started.** Both chains are unchanged at
   `bca64824`: `parse-ws`, `mam-simple`, `accgram-survey-post-stress-meteg`, `gen-site`; and
   `wlc-json-and-unicode` with `mam-simple`, then `accgram-run-prose`,
   `accgram-survey-chanted-word-accents`, `accgram-generate-html`. Since `d6a6764d` one
   `vendored-*` step runs what `mam-simple` rewrites under `MAM-simple/py-examples/`,
   `vendored-letter-small-job`; #272's body said three until it was corrected on 2026-09-14.
   Item 1 needs a declared list of what each step reads and writes, as #272's body and the dated
   record's §7 both say, and #278 could use the same list; see "Related plans and issues" below.
2. **Take `near-aleppo-census` out of the mega.** Saving: 17.6 s in run 1, 19.4 s pinned. **Done
   in `d32a17b8`** on 2026-09-11, so that the mega writes nothing outside this repository.
3. **Give the poetic scanner the prose scanner's fast path.** Estimated saving: about 5 s of the
   7.54 s the poetic scanner took over five steps. Risk: low. **Filed as #273, open, not started.**
4. **Scan the chanted-word survey's three corpora at the same time, in three processes.**
   Estimated saving: about 5 s. Risk: medium. Not started, not filed.
5. **Render `tmpl-survey`'s twelve SVGs at the same time, on a pool of threads.** Estimated
   saving: about 5 s of the 7.5 s its `dot` subprocesses took under cProfile. Risk: low to medium.
   Not started, not filed.
6. **Parse the Wikisource input once per run.** `diff-wsgo` and `ws-bot-proto` each repeat the
   parse that `parse-ws` has just made, which took 1.87 s. Estimated saving: about 4 s. Risk:
   medium. Not started, not filed. The Google Sheet retirement above would leave one repeat.
7. **Load MAM-simple once in the post-stress-meteg survey**, where `load_mam_simple_for_refs` runs
   four times. Estimated saving: about 2 to 3 s. Risk: low if the four calls ask for the same
   references, which nobody has checked. Not started, not filed. The MAM-simple changes above may
   have moved this figure.
8. **Read MAM-parsed's `plus/` tree once per run**, not once in each of the seven steps that read
   it whole. Estimated saving: about 1.5 s. Risk: medium. Not started, not filed.
9. **Split each atom into clusters once in `uxlc-fois`.** Estimated saving: about 1 s. Risk: low to
   medium. Not started, not filed.
10. **Pin the mega to the performance cores.** Not proposed by the dated record: the pinned runs'
    totals came within 2% of the unpinned ones, and the affinity mask names this CPU's cores.
    Pinning stays useful for comparisons, as in Phase 1.
11. **Skip steps whose inputs have not changed.** Not proposed for the integration check: the mega
    is the test because it recomputes every golden, so a skipped step tests nothing, and an input
    missing from a declared list turns a failure into a pass. At most an opt-in for runs during
    development.
12. **Run the subprocess steps in-process.** Not proposed: interpreter start-up is worth well under
    a second in all. The dated record counted four `vendored-*` subprocess steps; two remain,
    `vendored-tmpl-survey-toy` and `vendored-letter-small-job`.

## Three further proposals for the post-stress-meteg survey, from reading its code on 2026-09-14

**None of these three is measured, and no figure below is a measurement of a change.** They come
from reading `py/accgram/post_stress_meteg.py` in a cloud container on 2026-09-14, where
`accgram-survey-post-stress-meteg` is the one step that does not run, so the session that proposed
them could time nothing. Ben asked that day for them to be added here. **Treat each as a hypothesis
to verify before believing it**; the shares quoted are the dated record's profile of the existing
code. They are numbered 13 to 15 so that a reference to an item number stays unambiguous: items 1
to 12 above are the dated record's, and these three are not.

**Why this step repays the attention.** It was the dated record's largest step, 58.5 s unpinned and
40.9 s pinned, and that record's §4 item 1 puts 132.9 of its 150.9 s under cProfile in **four
passes of `_scan`**. All three items below are about those four passes. Item 7 above, which loads
MAM-simple once, is about the same step and is independent of these three. `build_survey` makes the
four calls, which are two cantillation strands times two modes:

```python
found              = _scan(phon_dir, CANT_ALEF)
found_bet          = _scan(phon_dir, CANT_BET)
template_found     = _scan(phon_dir, CANT_ALEF, dual_templates_only=True)
template_found_bet = _scan(phon_dir, CANT_BET, dual_templates_only=True)
```

13. **Decode the Phonetic MAM files once a run, not four times.** `_scan` has
    `data = json.loads(path.read_text(encoding="utf-8"))` inside its loop over
    `sorted(phon_dir.glob("*.json"))`, so each of the four passes reads and decodes every file of
    the standard set. Hoisting the read and the decode above the four calls, and passing the
    decoded data in, cuts that work to a quarter. **Expected saving: not estimated.** The dated
    record's profile does not separate decoding from scanning, so measure it first, by Phase 1 or
    by a profile run of the one step. **Risk: low**, provided the scan treats the decoded data as
    read-only, which is to be checked before the four passes share one copy.

14. **Stop the two `dual_templates_only` passes paying for the verses they skip.** Those two passes
    open with `if dual_templates_only and not dual: continue`, so they visit only the
    dual-cantillation verses, which `_has_dual_cantillation`'s docstring puts at the two Decalogues
    plus Genesis 35:22 — a handful out of the whole standard set. Each pass nevertheless decodes
    every file and runs `_has_dual_cantillation` on every verse to reach that `continue`.
    **Item 13 removes most of this by itself**, since the only per-verse cost then left in the two
    passes is the dual test; computing the dual set once would remove the rest. The three
    assertions immediately after the four calls already establish that all four passes agree on
    `dual_cant_verses`. **Expected saving: whatever item 13 does not already take. Risk: low.**

15. **Scan a verse that has no dual cantillation once, rather than once per strand.** This is the
    largest of the three and the only one that is not plainly safe.
    `_select_cantillation_strand` branches only where a payload begins `[_DUALCANT_MARKER]`, that
    marker being `"cb-dualcant"`; everywhere else it rebuilds a structurally identical result. So
    for every verse without a dual-cantillation node the `CANT_ALEF` and `CANT_BET` passes select
    equal text and then scan it identically, and the verses that do have such a node are the
    handful item 14 names. **Expected saving: up to one of the two full passes**, which would be
    the largest single saving proposed anywhere in this plan. **Risk: medium to high**, for a
    reason easy to miss: `_scan` makes one `prose_scanner.HasLegarmeh()` per file and keeps it
    across that file's verses, so each pass builds stateful per-file scanner state in verse order,
    and skipping the non-dual verses of the second strand would change that state. The `found` dict
    accumulates `Counter`s and lists across a whole pass besides. **Any implementation must leave
    `out/accgram/post-stress-meteg.json` byte for byte the same**, which is the differential check
    this repository relies on, and that file's figures reach the nine post-stress-meteg pages that
    read it.

## Phase 1: re-measure on Ben's machine with nothing else running

Ben asked for this phase to be planned and not yet done. Start it only when he says to.

Its three purposes:

1. A per-step baseline of the current mega, from which each item's estimate is re-derived.
2. Whether the run-to-run variation the dated record measured, up to 2.6 times for one step on
   unchanged code, persists when nothing else is running.
3. Optionally, the real cost of the four Sefaria and OSIS steps removed on 2026-09-12.

Steps:

1. **Make sure the machine is otherwise unloaded.** Ask Ben to confirm that no other Claude Code
   session, Codex thread or terminal job is running a mega, a suite, a generator or a build, and
   to close whatever else he judges heavy. `git worktree list` names the checkouts where such work
   could be running, but cannot say whether any is.
2. **Verify the checkout**: `git rev-parse --show-toplevel`, `git rev-parse HEAD`, and
   `git status --porcelain`, which must print nothing.
3. **Record the environment**: the commit; the interpreter's `--version`; the power plan, from
   `powercfg /getactivescheme`; and that the machine is still the dated record's, an Intel Core
   i5-13500T with 6 performance cores, 8 efficiency cores and 20 logical processors.
4. **Sample the idle load for 60 s before each run**, and keep the output:

   ```powershell
   typeperf "\Processor(_Total)\% Processor Time" -si 1 -sc 60
   ```

   One busy logical processor out of 20 is 5% of the total, and the mega runs one step at a time
   in one process, apart from the `multiprocessing` pool of `foi-features-of-interest` and the
   subprocess steps. So an idle mean above a few percent, or a mean well above 5% while a run is
   under way, means something else is using the processor; find it before trusting the run. A
   second `typeperf`, writing to a file with `-o` for the length of a run, gives the second
   figure.
5. **Make six full runs, alternating unpinned and pinned**, starting unpinned. A full run took
   285.7 s with 59 steps on 2026-09-11, so the six take about half an hour with their samples.
   Unpinned:

   ```powershell
   C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
   ```

   Pinned to logical processors 0 to 11, the performance cores of this CPU: set the launching
   PowerShell's affinity, then start the mega from that same PowerShell process, whose mask the
   mega inherits. Where each command starts a fresh shell, join the two with `;` in one
   invocation.

   ```powershell
   [System.Diagnostics.Process]::GetCurrentProcess().ProcessorAffinity = [IntPtr]0xFFF
   ```

   Capture each run's standard output and standard error to an untracked file. The `STEP TIME:`
   lines and the closing table, headed `MEGA STEP TIMES: <n> step(s) in <seconds> s`, are ASCII,
   so any capture keeps them intact.
6. **Check the tree after each run.** `git status --porcelain` must print nothing. A run that
   leaves a diff is an integration failure under `CLAUDE.md`'s "Integrating a worktree branch
   here", not a timing: stop and report it.
7. **Optionally, time the four removed steps directly.** Add a detached worktree at `d6a6764d^`,
   the last commit that still has all four. There, a throwaway script imports `main_0_mega`, finds
   each of the four steps' `StepRecord` in `_STEPS`, blanks `sys.argv` as `main()` does, and times
   each runner three times, pinned. Their inputs are MAM-simple's tracked files at that commit, so
   no earlier step has to run first. Afterwards, if `git status --porcelain` in that worktree
   prints nothing, remove the worktree with a plain `git worktree remove`; if it prints anything,
   ask Ben.
8. **If the spread across runs stays large**, a throwaway script that runs the steps in one process
   and records each step's `time.process_time()` beside its wall time tells computing apart from
   waiting. That script needs an `if __name__ == "__main__":` guard, because
   `foi-features-of-interest` starts a `multiprocessing` pool whose children re-import the main
   script.
9. **Write the record**: a new dated document, `doc/mega-timing-<date>.md`, with the environment,
   the load samples, and for each step the median, minimum and maximum of the three unpinned runs
   and of the three pinned runs, the step loop's totals, and step 7's figures if it ran. Set a
   step beside the dated record's §3 only where the `git log` command above shows its code
   unchanged since. In the same commit, update this plan's items with the new figures and its
   State line with the phase.

What Phase 1 must not change: no code and no generated output. Its commit names only the new
record and this plan.

## Phase 2: measure the mega in a cloud session

**Executed 2026-09-14, and its record is `doc/mega-timing-cloud-2026-09-14.md`, corrected the same
day by `doc/mega-timing-cloud-2026-09-14-update.md`.** A Claude cloud session on
`bdenckla/MAM-basics`, on branch `claude/adoring-shannon-8term6` at `main` `89f10bb4`, made three
full runs on Python 3.11 and, after the cloud update found out why that was the wrong interpreter,
two more on 3.13. All 55 steps ran or were skipped for the cloud in every run and no step failed.
This phase calls `doc/mega-timing-cloud-2026-09-14.md` the cloud record and
`doc/mega-timing-cloud-2026-09-14-update.md` the cloud update. The 2026-09-11 dated record is
`doc/mega-timing-2026-09-11.md`.

**The figures to quote are the cloud update's**, the cloud record's being 3.11 measurements: a
3.13 run takes **229.7 s**, the median of the two printed 3.13 step-loop totals, against 248.9 s on
3.11. The steps below are left as written; what each produced is in those two files. Five things
are worth carrying here:

1. **Normalizing for the cloud's skips does matter**, against the guess in Ben's instruction that
   it might not: the one step a cloud run skips, `accgram-survey-post-stress-meteg`, is the
   mega's most expensive on Ben's machine at 40.9 s, or 16.5% of a comparable run there. Step 5's
   "compare step by step, never by total" is the whole of the normalization needed.
2. **Like for like the container is 1.04 times Ben's pinned machine** over the 52 steps that
   completed in both, and **0.93 times** his unpinned run, so a container is within a few percent
   of his performance cores and ahead of his machine unpinned. (On 3.11 those ratios read 1.13 and
   1.01, which is what the cloud record states.)
3. **A container is markedly more repeatable than Ben's machine**, each pair of warm runs agreeing
   to within 0.6 s on every step, so it is the better place to attribute a speedup — for every
   step but the one it skips. A first run in a fresh container is a cold-cache run and should be
   discarded.
4. **One finding, raised in this phase and not fixed in it, has been fixed since by `b5dd2ffb`.**
   Git treats each commit a shallow clone lists in `.git/shallow` as having no parents, so every
   file in it looks added, and the path-filtered walk that dated unpinned-latest returned such a
   commit rather than finding nothing. The cloud record's §7 has the finding, which reproduced
   identically on 3.13, but blames a missing parent object, which the cloud update corrects. Since
   `b5dd2ffb`, `diff-mpplus` labels unpinned-latest by the tree id of `MAM-parsed/plus` and gives
   it no date, so a shallow clone no longer changes that report; no cloud run has confirmed it yet.
5. **The environment's setup script failed until Ben fixed it on 2026-09-14; steps 3 and 4 below
   survive it either way.** It failed with exit code 2, having built a 3.13 virtual environment
   and then looked for `requirements.txt` in `/home/user`, the parent of the clone rather than the
   clone. A session that does not notice falls back to the system `python3`, which is 3.11 and
   whose dpkg-managed `site-packages` then blocks a `pip install` — which is exactly what happened
   on 2026-09-14, and why the cloud record's figures are 3.11 ones. Inside the 3.13 environment the
   install takes 3.0 s and no conflict arises. **The fix is Ben's report and is not verified in
   this repository**, the container that found the fault having been built before it; the next
   cloud session confirms it by finding a populated 3.13 environment at step 3, and needs no
   workaround if it does. The cloud update entry has the evidence.

Ben asked for this phase to be planned and not yet done. It cannot run on Ben's machine: Ben
starts a Claude Code cloud session on `bdenckla/MAM-basics` at `main`, and that session carries it
out.

Its three purposes:

1. How long a full run takes in a cloud container. `doc/` records no cloud mega timing, and the
   only cloud timing the session writing this plan came across is the suite's, 106 s, in the
   message of `fa517040`.
2. Which steps' times differ most between a container and Ben's machine, as a pointer for later
   work rather than an explanation.
3. How many processors a container offers, which bears on item 1.

Steps:

1. **Confirm that it is a cloud session**: `CLAUDE_CODE_REMOTE` must be `true`. That is the
   variable `in_cloud_session` in `py/mb_cmn/graphviz_pin.py` reads, and every cloud skip in the
   mega depends on it.
2. **Record the environment**: `git rev-parse HEAD`; `git rev-parse --is-shallow-repository`,
   since the container that `fa517040` measured on 2026-09-11 held a shallow clone of 221 commits;
   `nproc`; the model name from `lscpu`; `free -h`; **the version of the interpreter the runs will
   actually use, which is the virtual environment's and not `python3`'s** — record both, since on
   2026-09-14 they were 3.13.12 and 3.11.15 and only the first is the one to measure on, while the
   dated record measured the JSON writer's saving on 3.13.15; whether `dot` is on the path, which
   it should not be; and `cat /proc/loadavg` before each run.
3. **Check the interpreter first, then the packages.** Amended 2026-09-14, after the run recorded
   in `doc/mega-timing-cloud-2026-09-14.md` followed the earlier wording of this step and measured
   the wrong Python throughout. **Do not reach for `python3`**: in a cloud container that is the
   system interpreter, 3.11, and its `site-packages` is managed by dpkg, so a `pip install` into
   it fails on a package pip cannot uninstall. Use the virtual environment the environment's setup
   script builds, which is 3.13 and is what Ben's machine runs. Find it before anything else —
   `.venv` at the repository root, or at `/home/user/.venv` while the setup script's working
   directory is still the parent of the clone — and check its version with
   `<venv>/bin/python --version`. **If the setup script failed and there is no usable 3.13
   environment, say so and stop rather than falling back to `python3`**, since a fallback silently
   changes what is being measured. Install into that environment with
   `uv pip install --python <venv>/bin/python -r requirements.txt`, which took 3.0 s on
   2026-09-14, and record the install apart from the runs. Then confirm the packages with
   `<venv>/bin/python py/main_test.py --collect-only -q`; a pywikibot user-config collection error
   in `py/tests/test_ws_bot_real_diff_links.py` is a suite matter that no mega step touches.
4. **Make three full runs back to back**, from the repository root, each captured to an untracked
   file, using the 3.13 environment of step 3 and never a bare `python3`. Discard the first run's
   figures: a fresh container runs it cold, which cost 27.9 s on 2026-09-14, over half of that in
   `diff-mpplus` alone. Between runs, check the tree as step 6 says, so that each run starts clean.

   ```bash
   <venv>/bin/python py/main_0_mega.py > <untracked file> 2>&1
   ```

5. **Compare step by step, never by total**, because a cloud run does less. It skips
   `accgram-survey-post-stress-meteg`, which reads MAM-private and took 40.9 s in the dated
   record's pinned run of the committed code, and it skips the SVG renders of `tmpl-survey`
   (twelve) and `pipeline-graph` (two). The closing banner, `MEGA RUN IS CLOUD-COMPLETE`, lists
   what was skipped.
6. **Check the tree after each run.** A run should change no tracked file, and any diff is a
   failure to report. Until 2026-09-14 this step expected a shallow clone to change the outputs of
   two steps with no defect in their diffs, because both read commit dates from a history that a
   shallow clone truncates: `vendoring-audit`, which dated each vendored copy by its last commit
   and was removed from the mega that day, and `diff-mpplus`, which dated unpinned-latest by the
   last commit to `MAM-parsed/plus` until `b5dd2ffb` labelled that report by the tree's id
   instead. No cloud run has confirmed the clean tree yet.
7. **Write the record**: a new dated document, `doc/mega-timing-cloud-<date>.md`, with the
   environment, each step's three times, the skips, and Phase 1's medians beside them if Phase 1
   has run. In the same commit, which names both paths, update this plan's Phase 2 status. Push
   the session's own branch, the only branch a cloud session can push to
   (`doc/user-level-config-in-cloud-sessions.md`). A local session then integrates that branch
   under `CLAUDE.md`'s "Integrating a worktree branch here".

What Phase 2 must not change: no code and no generated output. A difference that step 6 finds is
reported, not committed.

## Implementing items 3 to 9 and 13 to 15

1. **Every item must be output-neutral**, as both speedups already made were: every tracked output
   stays byte for byte the same. An item that changes an output is a different piece of work.
2. **Attribute a saving by running the old and the new code alternately, call by call, in one
   process**, with the old module loaded from `git show`, as items 4 and 6 of the dated record's
   §8 describe. Whole runs on Ben's machine vary by more than most of these savings.
3. **Then run the mega and read its `git diff`**, which must show nothing but the edited modules.
   That run is also the integration check that `CLAUDE.md` requires.
4. **Run black on each changed Python file, and commit each item on its own, naming its paths**,
   with its measured saving and new status recorded in this plan in the same commit.

Run `git diff --check` and the full suite before committing each completed executable item. Run
the repository's final mega integration gate after the last executable change and explain every
tracked generated diff.

## Related plans and issues

- **[#278](https://github.com/bdenckla/MAM-basics/issues/278)**, "Assert written_this_run ==
  intended == on_disk for single-writer output directories". The declared list of what each
  step reads and writes, which item 1 needs, would also record two things #278 needs: which
  step owns each output directory, which #278 says is recorded nowhere in this repository, and
  which files each step claims, the scope #278 says its `on_disk` set needs. The list would not
  supply `written_this_run`, which has to be recorded as files are written. Ben raised the
  connection on 2026-09-14, and #278's body links back to this plan.
- **`doc/PLAN-dispose-mega-pipeline-review-findings.md`** covers the 13 open atomicity findings,
  each about a failure that leaves a set of outputs half-written. Item 1's rule for stopping the
  other steps when one step fails bears on the same failures.

## What this plan does not change

- `doc/mega-timing-2026-09-11.md` stays as written. Anything to add to it goes in
  `doc/mega-timing-2026-09-11-update.md`.
- No issue was edited in writing this plan. A later session corrected the bodies of #272 and
  #273 on 2026-09-14, and linked each issue to this plan in a comment.
