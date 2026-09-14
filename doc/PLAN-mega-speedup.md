# PLAN — make the mega run faster

State: live, no phase started as of 2026-09-14.

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
record's §7 is kept in this plan.** The wording of §7 itself, and the bodies of #272 and #273,
describe 2026-09-11.

Two speedups were made and measured with the dated record, and both are on `main`: `15c09692` gave
the prose scanner a fast path, cutting its time from 75.3 s to 21.1 s over the eight steps that
call it, and `af1c404a` made the JSON writer use `json.dumps`, saving about 15.8 s a run (the dated
record's §5).

## Preconditions

- **Repository**: `C:/Users/BenDe/GitRepos/MAM-basics`, with every command run from its root. The
  interpreter is `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`, spelled
  absolutely in a secondary worktree. Phase 2 uses the cloud container's own `python3`.
- **Instruction files to load first**: `~/.claude/CLAUDE.md` and this repository's `CLAUDE.md`,
  in particular its sections "Integrating a worktree branch here" and "What this repository's
  products are". The `hebrew-prose` skill is not needed for Phases 1 and 2, which write only
  timing records. Load it before editing any docstring or comment under `py/accgram/`, which
  items 3, 4 and 7 would do.
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
- **MAM-simple's tree shrank from 107.7 MB to 37.7 MB on 2026-09-12**, as the session that shrank
  it measured with `du -sb`. `b653e9b9` retired `MAM-simple/misc/Torah-letters-only/`; `d6a6764d`
  removed the example programs' output; `dcd2c1f6` removed the bhs and sef Unicode-names trees;
  `3b1adf45` writes a bhs or sef corpus file only where it differs from the vtrad-mam one, and
  dropped `yeivinID`; `20f18020` then took the choice of which bhs and sef files to write from the
  versification tables. **The `mam-simple` step has not been timed since.** A throwaway script
  that sums the sizes of the files `git ls-files -z -- MAM-simple` names re-establishes the
  tracked tree's size.
- **The code of the heaviest steps has changed**, so the dated record's per-step figures are
  history rather than a baseline. On 2026-09-14 at `bca64824` the command below listed 14 commits
  that are not merges. Two are the dated record's own speedups. The other 12 include the
  MAM-simple commits above and `6dbd27e7`, the template-projection work (`2239cbad`, `5cb06e25`,
  `1b7b97ef`), and two changes to the mpplus diff (`fa517040`, `7fd381db`).

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
   `accgram-survey-chanted-word-accents`, `accgram-generate-html`. #272's body says that three
   `vendored-*` steps run what `mam-simple` rewrites under `MAM-simple/py-examples/`; since
   `d6a6764d` one does, `vendored-letter-small-job`.
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
   `nproc`; the model name from `lscpu`; `free -h`; `python3 --version`, which was 3.13.12 there,
   while the dated record measured the JSON writer's saving on 3.13.15; whether `dot` is on the
   path, which it should not be; and `cat /proc/loadavg` before each run.
3. **Check the packages.** If `python3 py/main_test.py --collect-only -q` fails on a missing
   module, install them with `python3 -m pip install -r requirements.txt`, and record that the
   install happened and how long it took, apart from the runs.
4. **Make three full runs back to back**, from the repository root, each captured to an untracked
   file:

   ```bash
   python3 py/main_0_mega.py > <untracked file> 2>&1
   ```

5. **Compare step by step, never by total**, because a cloud run does less. It skips
   `accgram-survey-post-stress-meteg`, which reads MAM-private and took 40.9 s in the dated
   record's pinned run of the committed code, and it skips the SVG renders of `tmpl-survey`
   (twelve) and `pipeline-graph` (two). The closing banner, `MEGA RUN IS CLOUD-COMPLETE`, lists
   what was skipped.
6. **Check the tree after each run.** A shallow clone can change two outputs with no defect in the
   code, because both read commit dates from a history that a shallow clone truncates.
   `vendoring-audit` dates each vendored copy by its last commit, through `git log -1` in
   `py/vendoring/compare.py`. `diff-mpplus` dates `HEAD` by the last commit to `MAM-parsed/plus`,
   as the docstring in `py/subcommands/diff_mpplus.py` that begins "THE ONE GIT READING LEFT"
   explains. Check a diff in either output against that explanation, and commit neither. Any other
   diff is a failure to report.
7. **Write the record**: a new dated document, `doc/mega-timing-cloud-<date>.md`, with the
   environment, each step's three times, the skips, and Phase 1's medians beside them if Phase 1
   has run. In the same commit, which names both paths, update this plan's Phase 2 status. Push
   the session's own branch, the only branch a cloud session can push to
   (`doc/user-level-config-in-cloud-sessions.md`). A local session then integrates that branch
   under `CLAUDE.md`'s "Integrating a worktree branch here".

What Phase 2 must not change: no code, and no generated output other than the shallow-clone
differences of step 6, which are not committed.

## Implementing items 3 to 9

1. **Every item must be output-neutral**, as both speedups already made were: every tracked output
   stays byte for byte the same. An item that changes an output is a different piece of work.
2. **Attribute a saving by running the old and the new code alternately, call by call, in one
   process**, with the old module loaded from `git show`, as items 4 and 6 of the dated record's
   §8 describe. Whole runs on Ben's machine vary by more than most of these savings.
3. **Then run the mega and read its `git diff`**, which must show nothing but the edited modules.
   That run is also the integration check that `CLAUDE.md` requires.
4. **Run black on each changed Python file, and commit each item on its own, naming its paths**,
   with its measured saving and new status recorded in this plan in the same commit.

## Related plans and issues

- **#278**, "Assert written_this_run == intended == on_disk for single-writer output
  directories", needs the same per-step record of what each step writes that item 1 needs.
- **`doc/PLAN-dispose-mega-pipeline-review-findings.md`** covers the 13 open atomicity findings,
  each about a failure that leaves a set of outputs half-written. Item 1's rule for stopping the
  other steps when one step fails bears on the same failures.

## What this plan does not change

- `doc/mega-timing-2026-09-11.md` stays as written. Anything to add to it goes in
  `doc/mega-timing-2026-09-11-update.md`.
- No issue was edited in writing this plan. The bodies of #272 and #273 still describe
  2026-09-11.
