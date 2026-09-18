# Plan: remediate the closed 2026-09-14 dual-agent review

State: live; written 2026-09-16 after the review exchange closed and Ben approved the complete decision package. Nothing in this plan has been remediated yet.
Updates and later status: [PLAN-remediate-review-findings-2026-09-14-update.md](PLAN-remediate-review-findings-2026-09-14-update.md).

This plan is for a fresh task with no access to the conversation that produced it. The executing
task works in the existing shared checkout
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14` on branch
`dual-agent-review-2026-09-14`. The approved decisions are recorded at source commit
`2e77d2fd7badece46d32eee3db0f90b707b17c35` in
`doc/review-findings-2026-09-14-update.md`, and current `main` at
`0d82b4e6007b462e789381ecaf289842cca0dafa` was merged into the review branch by merge commit
`dab5d091de87daedefe9b055909e7a31ebe7abd8` before this plan was written.

The merge introduced wording that preserves a base receipt together with all update siblings when
the family is retired. Ben clarified on 2026-09-16 that this literal preservation of files active
in that work's context did not reverse his 2026-09-15 decision about the continuing policy. The
continuing policy is one live `<stem>-update.md` per base, with no future numbered
`<stem>-update-N.md` siblings. At this plan's baseline the branch has 25 tracked
`doc/*-update.md` files and no numbered update siblings, so no existing numbered file needs to be
rewritten or deleted.

## 1. Authority, inputs, and checkout preconditions

Before editing, read the live user and repository instructions and load these skills in this
order:

1. `codex-worktree-tasks`, including `references/task-lifecycle.md` and
   `references/worktree-runtime.md`, for the shared-worktree checks, integration boundary, and the
   prohibition on using Codex retirement tooling on a `.claude/worktrees/...` checkout.
2. `hebrew-prose`, including `references/core-rules.md`, `references/terminology.md`,
   `references/mam-basics.md`, and `references/verifying.md`, before changing the two snips
   READMEs, the meteg-after-silluq update, or the `strands.py` docstring.
3. `github-issues`, including `references/reading-and-writing.md`,
   `references/state-changes.md`, `references/citations.md`, and
   `references/mam-basics-trackers.md`, before reading or changing MAM-basics issue #278.

Read all seven review inputs in full before editing:

- `doc/review-findings-2026-09-14.md`;
- `doc/review-findings-2026-09-14-update.md`;
- `doc/codex-review-findings-2026-09-14.md`;
- `doc/dual-agent-review-2026-09-14-turn-03-claude.md`;
- `doc/dual-agent-review-2026-09-14-turn-04-codex.md`;
- `doc/dual-agent-review.md`; and
- `doc/periodic-review.md`.

The root agent is the only writer, stager, and committer in this shared checkout. Read-only
sub-agents may remeasure bounded surfaces, but the root agent verifies every adopted result. Confirm
that no other task is writing this checkout. Before any mutation, verify the exact checkout, HEAD,
branch, required ancestor, and clean tracked state:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14 rev-parse --show-toplevel
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14 rev-parse HEAD
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14 branch --show-current
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14 merge-base --is-ancestor 2e77d2fd7badece46d32eee3db0f90b707b17c35 HEAD
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14 status --short --branch
```

Only after those checks pass, lock the worktree before the first remediation edit. The lock is the
explicit protection approved for finding 10.1:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14 worktree lock --reason "active dual-agent review 2026-09-14" C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14
```

Immediately before editing, merge the then-current local `main` into the review branch. Resolve
conflicts in this worktree, never in the primary checkout. If `main` is still `0d82b4e6`, the merge
is already present through `dab5d091`; a no-op merge is expected. If `main` moved, record the new
baseline and remeasure every drift-prone fact in section 2.

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14 merge main
```

Use the primary clone's interpreter for every Python command while keeping the current directory at
the worktree root:

`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`.

Create substantial throwaway measurement programs as uniquely named UTF-8 files below this
worktree's gitignored `.novc/`; do not use inline multiline interpreters. Record each measurement's
HEAD in its output. An unexpected measurement is a finding, not permission to silently broaden or
narrow this plan.

## 2. Baseline measurements and commands that must be rerun

The figures below were measured at `dab5d091`. They are dated baselines, not constants.

| Surface | Baseline at `dab5d091` | Required response to drift |
| --- | --- | --- |
| Mega and declared generators | 54 `StepRecord` entries and 42 declared entry points; `25bcabf6` removed the earlier 55th/43rd pair | Use these only to diagnose the two live plans; do not put a volatile count back into instructions. |
| `MAM-simple/` | 109 tracked files, 37,647,937 bytes | Explain the new tree before changing the size prose. |
| Receipt updates | 25 `doc/*-update.md`; zero numbered `*-update-N.md` | If a numbered sibling appears, stop and obtain a disposition rather than rewriting a receipt silently. |
| Receipt pointers | All 25 bases lack the approved line-4 pointer | Add the exact pointer in wave 1 and make the lint prove the complete set. |
| September 10 update headings | 39 headed entries; 38 `Recorded by` lines | The missing line belongs to the finding-10 crop-license entry. |
| Ruff | Exactly two F401 findings | A different Ruff result is a separate finding. |
| Hand-run products | Both regeneration commands fail on the missing incremental `Gen` file | After repair both commands must finish and leave their tracked products byte-identical. |
| Finished research reports | Job current blob `eb4dcee4...`, pre-move blob `b8fc419f...`; Psalms current blob `e1b0559a...`, pre-move blob `b7944176...` | Restore the pre-move substantive bytes; the final bases then differ only by the approved line-4 update pointer. Put the relocation only in their live updates. |
| Ignored Cambridge page tree in the primary clone | 28 files, 50,316,747 bytes in the review measurement | Re-measure in the later image-retirement task; do not move it during this remediation. |
| Shared-worktree `.novc/` | 518 files, 59,766,437 bytes during plan writing | Semantically preserve, promote, or explicitly dispose of evidence before retirement. |

Recompute the tracked MAM-simple tree with a scratch program that parses NUL-delimited output from
`git ls-tree -r -l -z HEAD -- MAM-simple`, counts paths, and sums blob sizes. Run it with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/remeasure_review_2026_09_14.py
```

The same program must:

- parse `py/main_0_mega.py` and report both the `StepRecord` inventory and the declared generator
  entry-point inventory, asserting the dated 54/42 baseline and naming `25bcabf6` as the commit that
  removed the prior pair;
- list `doc/*-update.md`, derive every base, and report exact pointer compliance;
- reject `doc/*-update-[0-9]+.md` rather than counting it as an ordinary update;
- count headed entries and `Recorded by` lines in
  `doc/review-findings-2026-09-10-update.md`;
- compare the two report blobs at HEAD with `a8e4790e^`; and
- record the current `main`, HEAD, and merge-base.

Re-run Ruff independently:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m ruff check py
```

Re-establish the exact report rewrite, rather than reconstructing its prose by hand:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14 diff --unified=0 a8e4790e^ a8e4790e -- doc/meteg-after-silluq-job-4-12.md doc/meteg-after-silluq-psalms-72-15.md
```

The volatile tier-3 entry-point count and volatile al-hatorah mention count are intentionally absent
from current instructions. Do not reintroduce or replace either count.

## 3. Complete disposition map

This table is the execution checklist. No finding may disappear merely because a later wave touches
the same file.

| Item | Approved disposition |
| --- | --- |
| Finding 1 | Keep the already-removed volatile count removed; correct the contradictory product-scope description, state the lint boundary, and cover upstream inputs of hand-run generators. |
| Finding 2 | Repair both hand-run generators, correct regeneration and size documentation, regenerate both products, and leave the broader whole-directory guard work with open MAM-basics issue #278. Findings 2.2 and 2.4 are already fixed. |
| Finding 3 | Restore both finished reports byte-for-byte to their pre-move text; record moved paths in live updates; correct the dead Metsudah link through its update; align both crop-naming rules and the two stale September 10 update claims. Finding 3.5 needs no work. |
| Finding 4 | Keep the already-removed count removed; make estimator ambiguity point to the existing `main_verse_links.py --atom N` interface; restore the letters-only note. Do not reverse the intentional lookup policy. |
| Finding 5 | No work: the transient generated-product rewrite was already reversed. |
| Finding 6 | Remove the two unused imports and make Ruff green. |
| Finding 7 | Implement one live update file and the pointer exception; repair live update facts, hashes, attribution, and outcome record; never fabricate the missing historical remediation plan. |
| Finding 8 | Correct the live instructions, hook, procedures, two live retirement plans, Codex-home spelling, closing-message asymmetry, delegation asymmetry, and cloud-session classification. Keep already-resolved 8.5 and no-defect 8.6 closed. Neutral Agent 1/Agent 2 roles are already implemented and remain unchanged. |
| Counter-finding C1 | Correct the image-retirement plan so its later executor moves the primary clone's ignored Cambridge tree only after tracked integration. Do not move it in this remediation. |
| Counter-finding C2 | Put the exact 4 + 24 + 8 title inventory and identity rules into the Google-Sheet retirement plan. The later executor, not this remediation, builds the independent mirror. |
| Finding 9 | Remove the obsolete hand-authored-directory example from open MAM-basics issue #278; do not replace it; preserve issue state and labels. |
| Finding 10 | Add shared-worktree locking, strengthen the Git filename-command lint, correct `_commit_date`'s description to name `--full-history`, and add UTF-8 stream configuration. Findings 10.4–10.6 and 10.8 remain observations. |
| Finding 11 | Apply all remaining prose and usage corrections. The mega-timing update sibling already exists; edit that live sibling rather than creating another. |

## 4. Wave 1: receipt policy, procedures, and the existing receipt set

This wave changes procedure and review records only; it reaches no declared product. The ordinary
commits are easy to undo. The exceptional line-4 insertions rewrite finished bases, which is a
separate record-risk act explicitly approved by Ben on 2026-09-15. Keep those edits mechanical and
in their own commit.

### 4.1 One live update file

Replace the numbered-sibling wording in all current-policy surfaces:

- `AGENTS.md`, anchor `Review filenames and finished dated documents`;
- `dot-Codex/user-wide-AGENTS.md`, anchor `finished dated review`;
- `dot-claude/user-wide-CLAUDE.md`, anchor `A finished dated document is corrected`;
- `doc/dual-agent-review.md`, anchor `Correcting a finished dated document`;
- `py/repo_util/check_repo_standards.py`, anchor ``THE `State:` LINE ON doc/*-update.md``;
- `dot-claude/skills/github-issues/references/reading-and-writing.md`, anchor `Retiring a finished document`;
- `dot-claude/skills/mam-repository-topology/references/repository-maintenance.md`, anchor `Manual document retirement`; and
- `doc/PLAN-repo-maintenance-across-GitRepos.md`, anchor `Receipt immutability and retention are independent`.

Use this core wording, adjusted only for the surrounding subject:

> Each finished document has at most one live sibling, `<stem>-update.md`. Corrections, later
> measurements, later State, and remediation dispositions go in that file. Keep the update file
> true while the base remains tracked, and never create `<stem>-update-N.md`. When the update file
> is created, insert one line directly below line 3 of the base: `Updates and later status:
> [<stem>-update.md](<stem>-update.md).` That pointer, plus a mechanically necessary joining of a
> prose paragraph that begins on line 3 without changing its text, is the only post-completion edit
> to the base.
> A spent base and its optional one update file are one retirement family and may be retired
> together under the manual retirement procedure.

The retirement wording must distinguish literal preservation from future policy: a historical
numbered sibling found in Git history remains historical evidence; the live policy neither creates
another numbered sibling nor uses the historical file as authority for doing so.

Interpret main commit `0d82b4e6` narrowly. Its retirement rules preserve every file that belongs to
an already-existing receipt family, including any numbered sibling that existed when that plan was
written, so retirement work did not have to wait. The commit does not preserve the numbered-sibling
idea as current policy and does not authorize any future `<stem>-update-N.md` file.

### 4.2 Mechanical pointer exception and lint

For each of the 25 tracked `doc/*-update.md` files, derive its base. Some bases have a `State:`
declaration on line 3, some have a provenance paragraph there, and two have a section heading there.
If a prose paragraph begins on physical line 3 and continues on later lines, unwrap only that whole
opening paragraph onto physical line 3 without changing any word, punctuation mark, inline Markdown,
or meaning. If line 3 is already complete or is a heading, leave it untouched. Then insert exactly
this line as physical line 4 of the base:

> `Updates and later status: [<base-stem>-update.md](<base-stem>-update.md).`

The mechanical opening-paragraph join and the pointer are the whole authorized base edit; make no other
change to those 25 bases. Add a new lint-shaped test,
`py/tests/test_receipt_update_links.py`, which:

1. obtains tracked `doc/` filenames with `git ls-files -z` and splits only on NUL;
2. fails if no update input exists;
3. rejects every tracked filename matching `doc/*-update-[0-9]+.md`;
4. requires a base for every `doc/*-update.md`; and
5. requires the exact derived Markdown pointer at line 4, without assuming that line 3 is a
   `State:` declaration.

This is a mechanical tree lint, not an example test. Update the standards docstring to say that an
update file is live: later dated entries are appended and stale present-tense claims are corrected
in place while the base remains tracked.

### 4.3 One canonical close-out list

Keep the generic numbered close-out in `doc/periodic-review.md`, section `Close-out`, with this
substance:

1. Record Ben's decisions on every finding.
2. Write and approve a fresh-task remediation plan with concrete editorial wording.
3. Execute remediation and put later State and every disposition in the review's one live update
   file, leaving the base's historical State untouched apart from its line-4 pointer.
4. Run the required final integration gate.

Replace the duplicate list in `doc/dual-agent-review.md`, anchor `After the exchange closes`, with:

> After the exchange closes, follow `doc/periodic-review.md`'s `Close-out` list. A sequential
> dual-agent round additionally updates this procedure record after Ben's decisions, uses Agent 1's
> turn-01 update file for later dispositions, integrates through the shared-review branch, and
> retires the shared worktree only after the final task ends.

Align D10's State wording in both procedures: the base review's line-3 State records what was true
when the review finished; later remediation State belongs in the single live update file. Remove
`## Dispositions after remediation` from the expected base-review content.

In `doc/periodic-review.md`, replace the overbroad census glob and its dated count with the exact
date-shaped pathspec below, and describe its result without a hard-coded count:

```powershell
git ls-files -- "doc/review-findings-????-??-??.md"
```

The broad `doc/review-findings-*.md` pattern returns 15 files at `dab5d091`, including three update
files; it is not the procedure's review-series census.

Add a searchable `### The September 10 round` passage to `doc/dual-agent-review.md`:

> The September 10 exchange closed, and its remediation outcome is recorded in
> `doc/review-findings-2026-09-10-update.md`. No separate fresh-task remediation plan was written;
> do not fabricate one after the fact.

Neutral Agent 1/Agent 2 roles, odd/even ownership, future numbered turn filenames, and the
historical September 14 filenames at the anchors `The September 14 round also keeps its historical
names` need no edit.

### 4.4 Shared-worktree lock procedure

Under `doc/dual-agent-review.md`'s `The shared worktree` section, add:

> Setup locks the shared worktree with `git worktree lock --reason "active dual-agent review
> <date>" <absolute-worktree-path>` before the first review turn. The lock remains through review
> and remediation. A separate cleanup task unlocks it only after final integration, after the final
> task ends, and immediately before an ordinary non-force worktree removal.

Do not add a session registry and do not weaken the existing no-force rule.

### 4.5 Repair live September 10 records

In `doc/review-findings-2026-09-10-update.md`:

- add `Recorded by Codex on 2026-09-13.` directly below the heading `Finding 10: the moved crop
  directories have dedicated license coverage`;
- replace the nonexistent screen-report blob `09ac3f...` with the accurate statement that its
  substantive content is historical blob `a46dbf0f9b384afa072878584c1dace2328dc179`
  plus only the authorized line-4 update pointer;
- rewrite finding 20.1's live-sounding census as a historical measurement at
  `d34afb44d94a631e08587a49281eec8c3349620d`: retain the searchable word anchors
  `hand-authored` and `hand-maintained`, remove drifting line numbers, and do not claim that the
  measured population is current;
- rewrite finding 20.11's `A fresh live-tree inspection` and canonical/live-copy equality claims as
  a historical measurement at `974395f9f2fabf69eee147c1764886a7c8e28ec0`: retain the recorded
  SHA-256 values as evidence from that checkpoint, remove drifting line numbers, and do not claim
  that the Codex live-copy path or byte equality remains current;
- change the paragraph beginning `The two affected finished dated reports remain unchanged` so
  `doc/user-level-config-in-cloud-sessions.md` is classified as a present-state document kept true
  in place, while `doc/mega-coverage-2026-09-10.md` remains a finished receipt corrected through its
  live update; and
- classify the `.Codex` home references in this live update, including the occurrences near the
  anchors `all nine current destinations`, `Finding 20.11`, and `Item 21.5`, and change every
  present-state home spelling to `.codex` while preserving quoted historical paths as historical.

In `doc/meteg-after-silluq-search-in-mam-documentation-update.md`, use these exact corrected
readings:

> The classification reads “silluq then meteg”; this is analytic prose, not a quotation retaining
> `ga'ya`.

> Finding 11.5's choice was recorded on 2026-09-13 in
> `doc/review-findings-2026-09-10-update.md`: use `ḥataf` in narrative Unicode prose and `xataf` in
> ASCII-oriented contexts.

Commit wave 1 as one procedure/policy commit plus one mechanical base-pointer commit. Before each
commit run the targeted receipt lint and `git diff --check`.

## 5. Wave 2: restore finished reports and correct live research documentation

This wave reaches no declared product and changes no generated output. Its principal act risk is
record integrity, so restore bytes from Git rather than paraphrasing the historical text.

### 5.1 Restore the two receipts and record relocation in their live updates

Restore only the six path/prose changes made by `a8e4790e` in:

- `doc/meteg-after-silluq-job-4-12.md`, whose pre-pointer historical blob is
  `b8fc419f43970d94dd96330074da6c3489eeb839`; and
- `doc/meteg-after-silluq-psalms-72-15.md`, whose pre-pointer historical blob is
  `b7944176b007648166d8c362e06a7927ca84df8d`.

After deleting only the exact line-4 update pointer in memory, each current file must hash to its
listed historical blob. The pointer stays in the tracked file. Do not restore deleted directories.
Append dated entries to
`doc/meteg-after-silluq-job-4-12-update.md` and
`doc/meteg-after-silluq-psalms-72-15-update.md` saying:

> The crop paths named in the finished report are historical. Since commit `a8e4790e`, the live
> crops and their source notes are under `doc/meteg-after-silluq-snips/`; the finished report's
> pre-move wording was restored under the receipt policy.

Use the applicable Psalms path in the Psalms update and the Job path in the Job update. Correct any
old blob assertion to distinguish the historical substantive blob from the current base whose sole
additional line is the authorized pointer.

Only after those restorations, return to `doc/review-findings-2026-09-10-update.md` and:

- replace the claim that all six research reports remained unchanged with the precise outcome:
  the two reports improperly edited during the crop move were restored to their pre-move blobs and
  their relocation was recorded in their live updates;
- replace `the live rule in leningrad/page-snips/README.md remains unchanged` with `The rule
  formerly stated in leningrad/page-snips/README.md is preserved in the two live snips READMEs`;
  and
- make the close-out row for item 20.9 name both live snips READMEs rather than the removed
  Leningrad path.

Audit every one of the 25 live update files for a present-tense assertion that its base `remains
unchanged` at a Git blob. The new line-4 pointer makes such an assertion literally false. Preserve
the historical blob as evidence, but restate the current relation as `the base's substantive bytes
match historical blob <sha>; its only additional line is the authorized update pointer`. Verify
that relation mechanically by removing the exact line-4 pointer in memory and hashing the remaining
UTF-8 bytes; do not rewrite any other base text. Perform this audit after the two report restorations
so every statement records an already-true repository state.

In `doc/metsudah-vs-ctr-update.md`, add a dated correction naming the base passage beginning
`The motivating clue is in`:

> The live destination of the former `doc/ms-snips/README.md` is
> `doc/lam-2-3-akhla-snips/README.md`; the base report keeps its historical link.

Do not edit `doc/metsudah-vs-ctr.md`.

### 5.2 Crop-coordinate rule

Replace the general coordinate sentence in both
`doc/meteg-after-silluq-snips/README.md` and
`doc/lam-2-3-akhla-snips/README.md` with:

> A Leningrad crop may include both column and line when Ben has read the line from the image; the
> section must say when the column comes only from the estimator. For another source, include only
> coordinates established from its image or retained index.

Keep the existing section-specific statement that the Job 4:12 column is estimated and Ben read the
line. Do not recreate `leningrad/page-snips/README.md`.

### 5.3 Remaining live prose corrections

In `doc/lam-2-3-akhla-snips/README.md`:

- replace the UXLC-derived manuscript claim with `UXLC 3.9 has a meteg on בָּֽחֳרִי and another
  on לֶֽהָבָ֔ה, plus silluq on the verse-final סָבִֽיב׃. This records the transcription; it does
  not establish what the Leningrad Codex manuscript has.` Apply the same source discipline to the
  later repeated sentence;
- replace every `Mikraot Gedolot Haketer` with `Mikra'ot Gedolot ha-Keter`;
- replace `shewa` with `sheva`; and
- replace `MAM has no meteg there, as does ...` with `MAM has no meteg there, nor does ...`.

In `doc/meteg-after-silluq-snips/README.md`:

- replace the folder promise with `Each section records the crop's available provenance; the
  Leningrad sections use the image sources named under “The Leningrad Codex.”`; and
- use `verse-final atom` consistently at the five parallel crop descriptions.

In `py/versification_and_cantillation/strands.py`, replace:

> `The Decalogue verses carry the מ:כפול (dual-cantillation) template`

with:

> `The Decalogue verses have the מ:כפול (dual-cantillation) template`.

In the live `doc/mega-timing-2026-09-11-update.md`, add or correct the relevant entry to read
`the WLC 4.22 prose verses`; do not create another update sibling.

In `README.md`, replace `Run tests through the unified harness (on MS-Windows:):` with
`Run tests through the unified harness (on MS-Windows):`.

Format only `py/versification_and_cantillation/strands.py` with Black, run the prose and mark-order
tests that cover the edited files, then commit this wave. No image bytes and no generated page are
expected to change; any such diff is a finding.

## 6. Wave 3: product-scope rule and the two hand-run generators

This wave reaches the distributed `MAM-for-Sefaria/` and `MAM-OSIS/` products and the published
`gh-pages/MAM-OSIS/` documentation. That product reach is independent of act risk: all development
writes are ordinary Git changes, but a later push of `main` publishes them.

### 6.1 Product-scope wording

In `py/product_scopes.py`, replace the contradictory tier-3 sentence with:

> This is the routine route into tiers 1 and 2; declared hand-run generators are the other route.

Replace the final hand-run sentence with:

> A change to a hand-run generator, or to any input it reads, owes rerunning every affected
> generator and inspecting every tracked output it writes; a mega run does not do that for it.

In `AGENTS.md`, replace the current hand-run closing sentence with:

> A hand-run generator can reach a product even though the mega does not run it. A change to a
> hand-run generator, or to any input it reads, requires rerunning every affected hand-run
> generator and inspecting its tracked outputs.

In `py/tests/test_product_scopes.py`, add this exact boundary to the docstring after `WHAT IT
CHECKS`:

> This lint proves that the declared mega entry points and wrappers match `_STEPS`. It does not
> validate prose counts, discover a product left behind by a removed mega step, or infer which
> hand-run generators read a changed upstream input.

### 6.2 One explicit incremental-path resolver

Add a shared MAM-simple book-group path resolver under `py/mb_cmn/`. It must dispatch explicitly on
recognized format (`json`, `xml`) and versification (`mam`, `bhs`, `sef`), try the requested file
first, fall back only from a recognized BHS or Sefaria directory to the parallel MAM directory, and
raise `FileNotFoundError` listing every attempted path. It must never infer a format or tradition
from arbitrary parameter shape.

Use that resolver in all three relevant paths:

- make `py/accgram/mam_simple_verse.py` delegate its existing JSON fallback to the shared resolver;
- make `py/mb_sefaria/mam4sef_or_ajf.py`, anchor `_read_book_group`, resolve each requested JSON
  book group before opening it; and
- change `py/main_mam_osis.py` and `py/osis/osis_runner.py` so OSIS resolves each BHS XML book group
  with the same requested-first, MAM-fallback rule instead of treating `xml-vtrad-bhs` as complete.

Keep `osis_runner`'s general parameterization explicit: its caller supplies the book-group resolver
or both declared input directories; the runner must not probe an undeclared sibling by convention.

### 6.3 Reader-facing regeneration and size wording

In `MAM-simple/README.md`, replace the 39.0 MB sentence with:

> The incremental-folder deletion removed 24.3 MB on 2026-09-12. The same commit removed another
> 1.3 MB by dropping `yeivinID` from the 48 MAM files, taking the product from 63.3 MB to 37.6 MB.

Use the same substance in `MAM-simple/doc/reading-mam-simple.md`.

Replace the final sentence of the retired-example passage in
`MAM-simple/doc/reading-mam-simple.md` with:

> Both editions are still produced by MAM-basics' `py/main_mam4sef.py` and
> `py/main_mam_osis.py`. Both generators follow the incremental-folder rule above: read the
> requested versification file when present and the MAM file otherwise.

In `MAM-for-Sefaria/README.md`, replace `That reads MAM-simple` with:

> That reads the incremental Sefaria and BHS JSON folders with the MAM JSON folder as their base,
> so regenerate MAM-simple first if its source changed.

In `MAM-OSIS/README.md`, use:

> That reads the incremental BHS XML folder with the MAM XML folder as its base, so regenerate
> MAM-simple first if its source changed.

### 6.4 Differential verification of the hand-run products

Immediately before each generator, record a working-tree SHA-256 manifest of that generator's
tracked outputs in `MAM-for-Sefaria/`, `MAM-OSIS/`, and `gh-pages/MAM-OSIS/`. Exclude only the
README files intentionally edited in this wave, name those exclusions in the manifest, and compare
the same path set immediately after the run. Then run:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_mam4sef.py --both-sef-and-ajf
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_mam_osis.py
```

Both commands must succeed. At the `dab5d091` data baseline every tracked output is expected to be
byte-identical. A product diff is not an automatic update: stop, explain which input changed and why,
and treat an unexplained diff as a finding. Do not add an example-based test for one book group; the
real full generator diff is the independent differential check.

Format every changed Python file, run `py/tests/test_product_scopes.py`, the directly affected
MAM-simple/OSIS tests, and Ruff, then commit source, documentation, and any explained generated
change together.

The broader `written_this_run == intended == on_disk` whole-directory guard remains assigned to
open MAM-basics issue #278; do not implement it in this wave.

## 7. Wave 4: atom lookup, Git filename lint, UTF-8 entry point, and lint cleanup

This source wave is not expected to change any repository product. It changes executable code and
tests, so it triggers the final full-suite gate.

### 7.1 Atom ambiguity and letters-only note

In `py/main_uxlc_estimate_atom_loc.py`, catch both no-match and ambiguity failures without adding a
second `--atom` interface. On ambiguity, print the exception, the numbered candidate atoms, and:

> Choose the intended number, then run
> `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_verse_links.py <book>
> <chapter>:<verse> --atom N`.

Verify the parser's exact positional syntax before committing. In `py/main_verse_links.py`, change
the impossible `method == "stripped"` branch to `method == "letters"`, matching
`py/uxlc_misc/my_uxlc_find_atom.py`. The existing note text, `matched by its letters alone`, then
becomes reachable again.

Exercise one current ambiguous query and one letters-only unique query through the real commands;
record exit codes and output in `.novc/`. Do not add a selected-case unit test.

### 7.2 Git filename-command lint

Strengthen `py/tests/test_tracked_filenames.py` so its AST pass resolves simple local Git wrappers:

- detect a wrapper whose body constructs a command beginning with literal `git` and expands its
  positional string arguments;
- inspect call sites that pass `worktree list --porcelain`, `status --porcelain`,
  `ls-tree --name-only`, `ls-files`, or `diff --numstat` through that wrapper; and
- require `-z` at the effective call site.

The broadened pass must cover the wrapper calls currently near
`py/repo_util/git_worktree_cleanup.py`'s `_list_worktrees` and dirty probe, and
`py/mb_diff_mpu/mpplus_revisions.py`'s `filenames`, without pinning the present count of calls.
Keep a nonempty-source assertion. This remains a mechanical source-tree lint.

### 7.3 Remaining four actionable source gaps

In `py/subcommands/diff_mpplus.py`, make `_commit_date`'s historical description name the actual
path-filtered command, ``git log --full-history -1``. Do not change the already-correct resolver.

At the start of `py/main_repo_util.py:main()`, before argument parsing, mirror
`py/main_repo_maintenance.py`:

```python
sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
sys.stderr.reconfigure(encoding="utf-8")
```

Add the needed `sys` import. Remove only these two Ruff findings:

- `from accgram import rtmsr_sat` in `py/accgram/rtmsr_verse.py`; and
- `from mb_cmn import template_names as tmpln` in `py/foi/kq_trivial_types.py`.

Format all changed Python files with Black, then run the filename lint, the receipt lint, affected
atom tests, and the directly affected source checks. Defer final Ruff and the full suite until after
wave 5's last Python edit; section 11 gives those commands.

## 8. Wave 5: live instruction/configuration and cloud-installation corrections

These edits reach no declared MAM product. They become global machine behavior only after the
separate post-push deployment, an outside-Git write with a different act risk.

### 8.1 Durable current wording

In `dot-claude/user-wide-CLAUDE.md`:

- replace `its step 7` with `its task-folder judgment step, “Retire completed Codex task folders
  under ...”` so another inserted step cannot stale the pointer;
- replace the future-tense paragraph ending `until then it is findable only on that round's branch`
  with `MAM-basics' fuller repository statement names that repository's update files; this section
  states the cross-project rule.`; and
- add the general delegation counterpart from `dot-Codex/user-wide-AGENTS.md`, preserving root
  orchestration, one writer per shared checkout, and separate worktrees for concurrent writers.

In `dot-Codex/user-wide-AGENTS.md`, add this compact counterpart to the Claude closing-message rule:

> ## Final messages begin with one H1 report heading
>
> Begin every final message with `# Report: <subject>`, with nothing above it, and use no other H1
> in the turn. Put the direct answer immediately below that heading. The heading names the report's
> subject rather than using a bare `# Report`.

In `doc/dual-agent-review.md`, replace the retired manual write-back/count paragraph with:

> `dot-Codex/user-wide-AGENTS.md` is canonical. After canonical changes integrate and `main` is
> pushed, deploy from the primary clone with `py/main_repo_util.py --sync-user-config`; the command
> fetches and installs only from fresh `origin/main`. Verify afterward with
> `py/main_repo_util.py --sync-user-config --check`.

### 8.2 Lowercase Codex home

Change live `.Codex` home references to `.codex` in:

- `dot-claude/user-wide-CLAUDE.md`;
- `dot-Codex/user-wide-AGENTS.md`;
- `dot-Codex/README.md`;
- `dot-Codex/skills/prune-claude-state/SKILL.md`;
- `py/repo_util/user_config_sync.py`; and
- paused live `doc/PLAN-deferred-template-projection-decisions.md`; and
- present-state references in `doc/review-findings-2026-09-10-update.md`, while preserving any
  occurrence explicitly rewritten as a historical path at a named checkpoint.

Do not change the tracked canonical directory name `dot-Codex/`, and do not rewrite occurrences in
finished receipts. Re-run a case-sensitive `git grep` over current instruction, README, skill,
source, and live-plan surfaces; any remaining live home spelling needs classification.

### 8.3 Cloud hook and cloud-session record

In `.claude/hooks/install-user-config.sh`, replace `Four further entries are tracked beside them`
with:

> Other tracked entries are deliberately not installed here; the relevant cases include:

Keep the current cases and add that `dot-claude/shared-skills.txt` is the local deployment manifest,
not a resource installed by this cloud hook. Do not introduce a count.

`doc/user-level-config-in-cloud-sessions.md` is already corrected and needs no further edit. In its
live update sibling, replace the statement that the source is a finished report with:

> The source document describes the current cloud-session setup and is kept true in place. This
> dated entry records the earlier correction rather than freezing the source document.

Test the hook locally only through its existing redirected-HOME procedure. Report that this does
not exercise an actual cloud container.

Format `py/repo_util/user_config_sync.py` with Black after its final edit. Run the relevant
mega-coverage/configuration checks through `py/tests/test_mega_coverage.py`, then run final Ruff and
the full suite as section 11 requires. The post-integration canonical deployment check remains a
separate read-only check against fetched `origin/main`.

## 9. Wave 6: repair the two live retirement plans, including counter-findings C1 and C2

Editing these live plans reaches no current product and performs neither retirement. The later
Google-Sheet/Wikisource writes are outward-facing and remain manual; the later Cambridge move is a
recoverable but destructive local act. The plans must keep those risks distinct.

### 9.1 Make both plans agent-neutral

In both `doc/PLAN-retire-google-sheet.md` and
`doc/PLAN-retire-codex-index-image-work.md`:

- attribute the decisions to Ben with their recorded dates;
- tell the executor to read the applicable user and repository instructions rather than one
  agent's home file;
- load `codex-worktree-tasks` only when the assigned checkout is Codex-managed;
- preserve an existing branch and use the managing environment's verified detached-worktree rule;
  do not hard-code `codex-worktree-<worktree-id>` for every executor;
- require confirmation that no other task is writing the assigned checkout; and
- attach every drift-prone count to a baseline commit and remeasurement command rather than an
  expected magic number.

For the Google-Sheet plan, say the `hebrew-prose` skill is the installed user skill and the
`spreadsheets` and `computer-use` skills come from the executing environment if available. The
plan must stop if a required skill is unavailable rather than imply those skills are tracked here.

Replace the stale mega-count sentence with:

> Recompute the current `_STEPS` inventory before editing. Removing `parse-go` and `diff-wsgo`
> must reduce that remeasured set by exactly two; do not preserve a dated absolute count.

Record the current fact, pinned to `dab5d091`, that both tracked Sheet-versus-Wikisource diff JSON
files, `out/diff_mamws_mamgo.json` and `out/diff_mamws_mamgo-auto-edits.json`, contain `[]` and this
command reproduces them:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py wsgo
```

Treat a different result as a finding.

### 9.2 C2's exact 36-title inventory

In `doc/PLAN-retire-google-sheet.md`, replace category prose with this exact pinned inventory from
`in/mam-ws-intro/ch2.mediawiki` at `dab5d091`, anchored by `טבלה לדפים של עשרת הדברות` around
lines 361–388 and the song-form table around lines 746–804:

1. Four Decalogue pages: `עשרת הדברות/טעמים`, `Decalogue`,
   `עשרת הדברות בסיס/טעמים`, and `עשרת הדברות/ניקוד`.
2. For each of `שירת הים`, `שירת האזינו`, `מלכי כנען`, `שירת דבורה`, `שירת דוד`,
   `שירת העתים`, `עשרת בני המן`, and `שירת אסף`, the three pages `/טעמים`,
   `/צורת השיר`, and `/צורות נוספות`.
3. Eight chapter pages: `שמות טו/טעמים`, `דברים לב/טעמים`, `יהושע יב/טעמים`,
   `שופטים ה/טעמים`, `שמואל ב כב/טעמים`, `קהלת ג/טעמים`, `אסתר ט/טעמים`, and
   `דברי הימים א טז/טעמים`.

The later executor writes a scratch extractor that parses the two named tables in
`ch2.mediawiki`, asserts that the selected set equals the literal 36-title set above, and records
both requested and redirect-resolved titles. The mirror is independent:

- all 36 requested titles must be unique;
- all resolved identities within `in/mam-ws-special/` must be unique;
- exactly the eight declared chapter identities may overlap the existing book mirror;
- any other cross-mirror overlap, missing page, undeclared redirect convergence, or inventory
  change fails before replacement; and
- the manifest is written last, after all responses validate.

The same scratch extractor must assert the eight Sheet-side `תתת` chapter rows that link to the
eight `/צורות נוספות` pages, pinned to `dab5d091`:

1. `in/mam-go/A-Torah.csv:2078`, `ספר שמות/טו`;
2. `in/mam-go/A-Torah.csv:6173`, `ספר דברים/לב`;
3. `in/mam-go/B-NevRish.csv:327`, `ספר יהושע/יב`;
4. `in/mam-go/B-NevRish.csv:859`, `ספר שופטים/ה`;
5. `in/mam-go/B-NevRish.csv:2912`, `ספר שמואל/שמ"ב כב`;
6. `in/mam-go/E-XamMeg.csv:462`, `מגילת קהלת/ג`;
7. `in/mam-go/E-XamMeg.csv:818`, `מגילת אסתר/ט`; and
8. `in/mam-go/F-KetAx.csv:1756`, `ספר דברי הימים/דה"א טז`.

The executor must rediscover the rows by parsing CSV and matching the `תתת` field and
`/צורות נוספות` target; the pinned line numbers are searchable evidence, not parser input.

The later mirror run expects no changes to MAM-simple corpus data, the MAM-for-Sefaria corpus CSV,
MAM-with-doc book content, or MAM-OSIS corpus content. An unexpected diff is a finding.

### 9.3 C1's primary-checkout Cambridge move

In `doc/PLAN-retire-codex-index-image-work.md`, keep development and the tracked removal in the
assigned checkout. Replace the ignored-tree instruction with:

> During development, inventory
> `C:/Users/BenDe/GitRepos/MAM-basics/cam1753/cam1753-pages/` read-only and record its file count,
> byte count, and a SHA-256 manifest. Do not change that primary-clone tree from a secondary
> checkout. After the retirement branch is fully verified, fast-forwarded into primary `main`, and
> pushed, remeasure the same exact absolute path from a separate primary-checkout step. If the
> measurements still match the reviewed manifest, move the directory to the Windows Recycle Bin
> and verify the original path is absent. Never permanently delete it and never substitute a
> same-relative path in a secondary worktree.

The plan's measurement script, protected-file manifest, and product expectations remain, but every
dated figure must name its baseline commit. No Cambridge tree moves during this remediation.

Commit both live-plan corrections as one coherent planning commit after `git diff --check`.

## 10. Wave 7: MAM-basics issue #278

This wave reaches no declared product. It is an outward-facing GitHub edit and requires the
`github-issues` skill, a dry run, explicit read-back, and agent/date attribution. Ben explicitly
approved this issue edit in the close-out package.

Read the live issue first. It was open, labelled `enhancement`, unassigned, and had no comments at
plan-writing time. Preserve its state, labels, and assignees:

```powershell
gh issue view 278 --repo bdenckla/MAM-basics --json title,state,labels,assignees,body,comments
```

In a uniquely named UTF-8 JSON edits file, replace exactly:

```text
- **"Only these" needs a scope.** Some output directories hold hand-authored companions — `leningrad/page-snips/` has a `README.md` beside the crops — so the `on_disk` half has to mean "only these, among the files this program's naming scheme claims", not "only these, full stop".
```

with:

```text
- **"Only these" needs a scope.** Here, `on_disk` has to mean "only these, among the files this program's naming scheme claims", not "only these, full stop".
```

Do not replace the example with either live snips directory. Append to the outgoing body:

> Edited on `<execution-date>` by a `<Claude|Codex>` session, with Ben's approval, to remove an
> obsolete hand-authored-directory example after the crop directory was retired.

Run the edit command first with `--dry-run`, read the complete generated outgoing body under
`.novc/`, then run the same command without `--dry-run`. Add the required dated comment from its
own uniquely named UTF-8 body file:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_github_issue_edit.py --repo bdenckla/MAM-basics --issue 278 --edits .novc/issue-278-remove-obsolete-example.json --dry-run
```

Read `.novc/issue-bdenckla-MAM-basics-278-outgoing.md` in full. If it is exact, perform the body
edit:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_github_issue_edit.py --repo bdenckla/MAM-basics --issue 278 --edits .novc/issue-278-remove-obsolete-example.json
```

> Written by a `<Claude|Codex>` session on `<execution-date>`, at Ben's request. The obsolete
> `leningrad/page-snips/` example was removed from this open issue's body because that hand-authored
> crop directory was retired. The scope rule and the issue's open guard work are unchanged.

```powershell
gh issue comment 278 --repo bdenckla/MAM-basics --body-file .novc/issue-278-remediation-comment.md
```

Read the issue back with body and comments and verify the exact replacement, dated note, dated
comment, open state, label, and unchanged assignment. Do not close, relabel, or reassign issue #278.

## 11. Verification gates and commit discipline

Keep commits coherent and intended to pass their matched checks:

1. Receipt policy and procedure text.
2. Mechanical line-4 pointers and their tree lint.
3. Restored receipts, live updates, and research prose.
4. Product-scope and generator repair, including regeneration results.
5. Atom, filename-lint, UTF-8, Ruff, and remaining source changes.
6. Canonical user configuration and cloud hook.
7. The two live retirement-plan corrections.

Before each commit:

- confirm HEAD still equals the commit recorded at the start of that wave;
- inspect `git status --short` and the full diff;
- run `git diff --check`;
- run Black at defaults on only changed Python files;
- run the directly relevant targeted tests or lints; and
- stage only that wave's intended paths.

Run the receipt and filename lints together after their last edit:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py py/tests/test_receipt_update_links.py py/tests/test_tracked_filenames.py
```

Run the product-scope lint after the generator wave:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py py/tests/test_product_scopes.py py/tests/test_mega_coverage.py
```

After wave 5's `py/repo_util/user_config_sync.py` edit and Black run, run Ruff:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m ruff check py
```

Run the complete suite once after wave 5, the last test-risky source change:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py
```

Documentation, receipt, and instruction-only commits after that result do not expire it. A later
source or test edit does.

Before the final integration gate, merge then-current `main` into the review branch again. If
`main` moved, resolve in this worktree and rerun every affected targeted check and the full suite.
Then run the mandatory mega from the worktree root:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
```

Read and explain every tracked diff. At the `dab5d091` baseline the mega is expected to add no
tracked diff, and the two hand-run generator products are expected to remain byte-identical. An
unexpected generated diff is a finding. Commit every explained generated change on the review
branch before integration.

## 12. Final integration, deployment, and later cleanup

After all branch commits and the final mega are clean, fast-forward the primary clone's `main`
with `--ff-only` and push `main`. Do not merge by making new work directly in the primary checkout.
A push is outward-facing and deploys `gh-pages/`; verify the branch relationship immediately before
the push. If primary `main` moved, return to this worktree, merge, reverify, and repeat the final
gate.

From the primary clone, first require a clean `main` checkout:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics status --short --branch
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics branch --show-current
```

Verify that primary `main` is still an ancestor of the reviewed branch head:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics merge-base --is-ancestor main dual-agent-review-2026-09-14
```

Fast-forward and verify that both names resolve to the same commit:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics merge --ff-only dual-agent-review-2026-09-14
```

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics rev-parse main dual-agent-review-2026-09-14
```

Push only after those hashes match:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics push origin main
```

Only after the canonical configuration commits are on pushed `origin/main`, deploy from the primary
clone, with the command working directory set to `C:/Users/BenDe/GitRepos/MAM-basics`:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_repo_util.py --sync-user-config
```

Then run the read-only verification:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_repo_util.py --sync-user-config --check
```

The deployment writes outside Git to `~/.claude/`, `~/.agents/`, and `~/.codex/`; report that act
risk separately from its zero MAM-product reach.

Do not retire this shared worktree from the remediation task. Its `.novc/` held unique review,
self-check, and walkthrough evidence during plan writing. A separate setup/cleanup-only Claude task
or Ben must, after the final task ends, remeasure it before assigning every file a preservation,
promotion, or disposal outcome:

```powershell
Get-ChildItem -LiteralPath 'C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14/.novc' -Recurse -Force -File | Measure-Object -Property Length -Sum
```

The cleanup task then:

1. verify the branch is integrated and pushed, the worktree is inactive and clean, and no unique
   untracked or ignored evidence remains without an explicit disposition;
2. distinguish disposable caches from evidence that must be promoted or archived;
3. unlock the worktree;
4. remove it with ordinary `git worktree remove` and no `--force`;
5. verify `git worktree list --porcelain`; and
6. delete the merged branch with ordinary `git branch -d`.

Use these exact checks and actions, one at a time. Confirm the review head is in primary `main`:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics merge-base --is-ancestor dual-agent-review-2026-09-14 main
```

Confirm the target worktree is clean after the task has ended:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14 -C C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14 status --short --branch
```

After the evidence disposition is complete, unlock it:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics worktree unlock C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14
```

Remove it without `--force`:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics worktree remove C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/dual-agent-review-2026-09-14
```

Verify the registry:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics worktree list --porcelain
```

Delete only the integrated branch:

```powershell
git -c safe.directory=C:/Users/BenDe/GitRepos/MAM-basics -C C:/Users/BenDe/GitRepos/MAM-basics branch -d dual-agent-review-2026-09-14
```

The Codex retirement commands must not select this `.claude/worktrees/...` checkout. Worktree and
branch removal are destructive local acts even though product reach is zero.

The image-retirement plan's Cambridge Recycle Bin move and the Google-Sheet plan's external Sheet
and Wikisource edits are later plan-execution steps, not part of this review remediation. Their
corrected plans state their own verification and authority boundaries.

## 13. Completion report

The executing task's final report names:

- every remediation commit and the final integrated `main` commit;
- the full-suite and mega results;
- both hand-run generator commands and whether their products stayed byte-identical;
- the receipt-lint census and confirmation that no numbered update sibling exists;
- the exact issue #278 body edit and dated comment read-back;
- the user-configuration deployment and read-only check results;
- every generated diff and its explanation;
- the separate product-reach and act-risk outcomes; and
- the remaining cleanup task for `.novc/`, the locked shared worktree, and the merged branch.

No implementation choice in this plan remains for approval. If a remeasurement changes the
substantive scope, stop at that finding rather than treating drift as implicit approval.
