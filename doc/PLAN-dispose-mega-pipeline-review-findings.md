# PLAN — give each mega-pipeline review finding a current disposition

State: live, no phase started as of 2026-09-12.

Written by a Claude session on 2026-09-12. Ben's instruction that day, after being shown that 81
of the review's 85 public findings were still recorded as `Open — queued`: "Store this task away
with our usual way: a detailed plan in the 'doc' folder and thin GitHub issue with a pointer to
that plan." The question he had asked, which this plan answers by doing rather than by arguing,
was "whether there were other findings whose remediations were neither done (nor explicitly
recorded to be declined to be done)".

Everything below other than Ben's quoted words is that session's reconstruction. **Re-measure
every figure before relying on it**; each carries the command that re-establishes it, and a
mismatch is a finding to record rather than a number to overwrite.

## Why this exists

`doc/mega-pipeline-review-findings-public-2026-09-01.md` is the public disposition companion to
the 2026-09-01 mega-pipeline review. It is a finished dated document and is left exactly as
written, per Ben's rule of 2026-09-11; `doc/mega-pipeline-review-findings-public-2026-09-01-update.md`
is its live sibling.

Its `Open — queued` label means "open as of 2026-09-01", and by 2026-09-12 that label no longer
sorted the list. Two findings recorded as open had been fixed eight days later by work that never
looked at the list, and three others were still exactly as reported. **A reader cannot tell those
two cases apart without checking each finding against current code, and there are 81 of them.**
That is the whole of the problem, and this plan is the pass that fixes it.

## What is in scope, and what is not

**In scope: the 85 public findings** of the companion named above, the 81 `Open — queued` ones in
particular.

**Not in scope, and deliberately.**

1. **Fixing anything.** This pass reads and records. A finding that turns out to be real and
   trivially fixable is still recorded rather than fixed, because 81 findings times an
   opportunistic fix each is a different and much larger piece of work, and because which of them
   are worth fixing is Ben's call. If a phase turns up something urgent, say so and stop rather
   than widening the pass.
2. **Declining anything.** `declined` is a verdict only Ben can supply. A session executing this
   plan must never write it on its own judgment; the verdict for "this looks not worth doing" is
   `needs Ben`, with the reasoning.
3. **The seven private findings.** The companion's own tally records that seven of the review's 92
   findings are private — the six Phase 10 findings and one Phase 8 finding, aggregating 2 P1, 4
   P2, 1 P3 — and live in MAM-private. They need that clone and a decision from Ben about whether
   the same pass should cover them. Named here so they are not silently forgotten.

## Preconditions

- **Repository**: `C:/Users/BenDe/GitRepos/MAM-basics`. The interpreter is that clone's
  `.venv/Scripts/python.exe`, spelled absolutely if the work runs in a secondary worktree.
- **Instruction files to load before the first edit**: `~/.claude/CLAUDE.md` and this repository's
  `CLAUDE.md`. Load the **`hebrew-prose` skill** before recording a verdict on any
  finding that turns on accentuation prose or terminology. Those include `MP01-05`, `MP02-08`,
  `MP04-07`, `MP04-09`, `MP04-10`, `MP06-07`, `MP07-08`, `MP07-09`, `MP08-03`, `MP08-11`,
  `MP09-05` and `MP09-09`, but that list was assembled from one-line summaries and is not
  exhaustive; the first trap below applies to it too.
- **Another session may be live in this repository.** Work in a worktree if so. A worktree needs no
  `REPOS_ROOT`.
- **Baseline, measured 2026-09-12 at `a9462b61`**: the suite reports **995 passed, 5 skipped, 65
  subtests passed**, and a full mega run passes every step and leaves no diff.

  ```powershell
  C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py
  ```

## The figures this plan rests on, and how to re-establish them

Measured 2026-09-12 at `a9462b61` by parsing the companion's own finding index. A throwaway script
under `.novc/` that matches `^- \`(MP[0-9]+-[0-9]+)\` \*\*(P[0-9])\*\* — ` and classifies each
entry by which disposition phrase its body contains reproduces all of it.

| Figure | Value |
|---|---:|
| Findings in the public companion | 85 |
| `Open — queued` | 81 |
| …of which P1 / P2 / P3 | 8 / 55 / 18 |
| `Fixed in remediation` | 2 |
| `Already fixed before Phase 13` | 1 |
| `Fixed in closeout` | 1 |
| `Open — queued` naming no root cause | 63 |
| Atomicity findings | 13 |

**Three remediation waves ran, all on 2026-09-02, and all three were `MP02-0x` work** — wave 1
`MP02-02` and `MP02-03`, wave 2 `MP02-01`, wave 3 the architectural severing of the dated WLC
private dependency. All three are recorded in
`doc/PLAN-mam-mega-pipeline-phase-13-and-remediation.md`, under headings beginning
`## Remediation wave`. No fourth wave followed: the later `doc/PLAN-remediate-review-findings-*.md`
files belong to the separate periodic review series of 2026-09-07, 2026-09-08 and 2026-09-09.

## The verdict vocabulary is closed

Every finding gets exactly one of these. An unrecognized situation is `needs Ben`, never a new
verdict invented on the spot.

| Verdict | Means | Evidence required |
|---|---|---|
| `fixed` | Production code no longer has the defect | The commit that fixed it, found with `git log -S` or `git log --format=... -1 -- <path>`, and what in the current code shows it |
| `still real` | The defect is present today | A command and its output — a count, a path, a grep — that a reader can re-run |
| `obsolete` | The code, product or repository the finding names no longer exists | What removed it, and when |
| `needs Ben` | Cannot be settled without a decision of his | The question, stated so he can answer it in one line |
| `declined` | Ben decided not to act | His words and the date. **Never written without them.** |

## Two traps, both met on 2026-09-12

1. **The `atomicity root cause` tag is not an index of its subject.** Thirteen findings are about
   atomicity; only four carry the tag — `MP01-03`, `MP02-07`, `MP03-04`, `MP06-02`. Worse,
   `MP12-05` ("Four vendoring outputs can be mixed or truncated after failure") states the problem
   without using the words *atomic*, *transaction* or *incremental*, so a text search for those
   misses it. The same will be true of other root-cause tags. **Read each finding; do not group
   them by grep.** The session that wrote this plan first reported eleven atomicity findings and
   had to correct the count to thirteen.
2. **Never take a verdict from the companion's own status line.** That is the defect this pass
   exists to repair. Every verdict comes from current code.

## Worked examples, so a fresh session knows what a filled-in row looks like

Five findings were checked on 2026-09-12 and their verdicts are settled. They go into the output
as-is, and they show the shape.

- **`MP13-01`** (unpinned Graphviz version drift rewrites all 12 generated call-graph SVGs) —
  **`fixed`** by `7b3bed38` of 2026-09-09, "Pin Graphviz at 16.0.0, and make a missing dot fail
  instead of skip". `py/mb_cmn/graphviz_pin.py` pins the full version stamp bidirectionally and
  `py/tests/test_graphviz_version_pin.py` holds it.
- **`MP03-02`** (missing Graphviz silently preserves stale SVGs) — **`fixed`** by the same commit,
  whose title says so.
- **`MP02-08`, `MP04-09`, `MP06-07`** (reader-facing prose spells `legarmeh` as `legarmeih`) —
  **`still real`**. `gh-pages/MAM-OSIS/index.html` shows the spelling in visible prose, a heading
  among the hits ("Paseq marks (as distinct from legarmeih marks)"), and
  `gh-pages/MAM-for-Sefaria/index.html` shows it in a romanized table cell. **Do not use a raw
  grep count as the evidence.** `git grep -lI 'legarmeih' -- gh-pages/ out/` names 17 files on
  2026-09-12, but only 8 are HTML, and even there some hits may be class names; 4 are CSS and
  5 JSON, where the string is likely an identifier or data. MAM-simple's XML element for
  legarmeh is itself named `lp-legarmeih`, which is part of a published schema: a verdict on
  these findings concerns reader-facing prose only, and renaming a schema identifier would be
  a separate decision, and Ben's. The session that wrote this plan first cited the 17 as the
  evidence and had to correct it.

## Output

**A new file, `doc/mega-pipeline-review-dispositions-<date>.md`**, dated for the day the pass
finishes, with one row per finding: id, severity, the companion's one-line summary, the verdict,
and the evidence. It is a dated document, so once finished it is not edited; a later correction
goes in its own `-update.md`.

**One entry added to `doc/mega-pipeline-review-findings-public-2026-09-01-update.md`**, which is
live, pointing at that file and giving the resulting tally. Nothing in this plan edits the
2026-09-01 companion itself.

## Phases

Thirteen phases, one per `MP` phase group that has public findings: `MP00` through `MP13` less
`MP10`, whose six findings are all private and out of scope above. Each phase reads every
finding in its group against current code, writes its rows, and is committed on its own.
Open findings per group, measured 2026-09-12: MP00 1, MP01 5, MP02 5, MP03 6, MP04 10, MP05 6,
MP06 7, MP07 9, MP08 10, MP09 9, MP11 3, MP12 8, MP13 2 — 81 in all, and uneven by design, the
grouping keeping each phase's findings about one area of the pipeline, which is what makes
them cheap to check together.

Per phase:

1. Read every finding in the group in the companion, and its fuller write-up in
   `doc/mega-pipeline-review-phase-11-2026-09-01.md`, `…-phase-12-…` or `…-phase-13-…` where one
   exists.
2. Check each against current code and record a verdict with its evidence.
3. Commit that phase's rows, with the phase's verdict tally in the message.

Nothing in a phase depends on an earlier phase, so the pass can be split across sessions or task
chips; each is self-contained given this plan.

## What is NOT expected to change

**No production code, no generated artifact, no GitHub issue state.** The only files this pass
writes are the new dispositions file and one entry in the existing update file. So:

- The suite must still report **995 passed, 5 skipped, 65 subtests passed** — re-measure, since
  the count grows as tests are added, and treat a change with an unexplained cause as a finding.
- A mega run must still pass every step and leave no diff. Running it is optional per phase and
  worth doing once at the end.
- `git status --porcelain` must name only `doc/` files at every commit.

If a phase finds it cannot record a verdict without changing code, that is a `needs Ben`.

## Effort

81 findings, most settleable in a few minutes by reading the finding and grepping the code, some
needing a real judgment. The terminology findings need the `hebrew-prose` skill loaded and are the
slowest. Expect the pass to be worth splitting across several sessions, which the phase structure
allows.
