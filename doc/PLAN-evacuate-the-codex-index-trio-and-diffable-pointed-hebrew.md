# Total evacuation: the codex-index trio and diffable-pointed-hebrew

State: Phases 0–4 complete — Phase 5 cross-repo bookkeeping remains

This is the third stage Ben authorized on 2026-09-03. It carries the decision
record out of [`PLAN-evacuate-public-repos-programme.md`](PLAN-evacuate-public-repos-programme.md)
§"Third stage — the codex-index trio and diffable-pointed-hebrew, total
evacuation", which is the source of the stage's scope, order and decisions.
The completed second stage is
[`PLAN-evacuate-the-rest-of-three-repos.md`](PLAN-evacuate-the-rest-of-three-repos.md).
Read its sections "Land — Licence — Repoint — Stubs — Empty — Remove" and
"The oracle" before any lane. This plan states only what differs.

## Scope and instruction files

The destination is `C:/Users/BenDe/GitRepos/MAM-basics`; its interpreter is
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`. The sources,
in their required order, are:

1. `C:/Users/BenDe/GitRepos/codex-index-leningrad`
2. `C:/Users/BenDe/GitRepos/codex-index-aleppo`
3. `C:/Users/BenDe/GitRepos/codex-index-cam1753`
4. `C:/Users/BenDe/GitRepos/diffable-pointed-hebrew`

Before every phase, read `C:/Users/BenDe/.claude/CLAUDE.md`,
`C:/Users/BenDe/GitRepos/MAM-basics/CLAUDE.md`, this whole plan, the programme
section above, and the relevant source repository's `CLAUDE.md`. Load the
`hebrew-prose` skill before editing any prose that describes Hebrew
accentuation, a manuscript, or a manuscript transcription. The current phase
does not edit such prose; later lanes will.

Each index lane follows the second-stage sequence — Land, Licence, Repoint,
Stubs where the source has Pages, Empty, Remove — and all four layers under
"The oracle":

1. Blob identity proves every copied file, including images no generator writes.
2. A zero regeneration diff proves each repoint, using the source repository's
   recorded oracle rather than the WLC oracle.
3. Mtime snapshots show which tree a generator actually wrote.
4. The published-URL check distinguishes Ben-controlled links to repoint from
   out-of-reach links that require a frozen redirect manifest.

The Leningrad and Cam1753 source repositories have no Pages site. Their Empty
step leaves one dated breadcrumb `README.md`, pushes it to `origin/main`,
verifies it, and only then archives `bdenckla/codex-index-leningrad` or
`bdenckla/codex-index-cam1753` with `gh repo archive -y`. The Aleppo source
repository remains a redirect host for its three published pages and is not
archived. diffable-pointed-hebrew has no Pages site; whether it is archived
after its breadcrumb is a Ben decision at that lane, not an assumption.

## Status

| Phase | State |
| --- | --- |
| 0 — Preflight: fresh baselines, readiness, and duplicate-data decisions | **DONE 2026-09-03.** The source trees are clean; the fresh MAM-basics suite passed 975 / 5 / 65; the shared `MAM-XML/` disposition is now performed by Phase 2, and Ben's 2026-09-04 Cam1753 decision retains only the 14 spreads. |
| 1 — codex-index-leningrad | **DONE 2026-09-03.** The five-artifact `leningrad/` tree is live; the source is an archived breadcrumb history, and its primary clone remains only as shared Git metadata for its retained review-forest input. |
| 2 — codex-index-aleppo | **DONE 2026-09-04.** The Aleppo tree and pages now live under `aleppo/` and `gh-pages/aleppo/`; the source repository is a deployed redirect host, and its clean primary clone has left `GitRepos`. |
| 3 — codex-index-cam1753 | **DONE 2026-09-04.** `cam1753/` holds the 100 selected source blobs, including the 14 spreads; the 28 page JPEGs are ignored output regenerated from those spreads. The source repository is an archived breadcrumb, and its clean primary clone has left `GitRepos`. |
| 4 — diffable-pointed-hebrew | **DONE 2026-09-04.** The product now lives under `diffable-pointed-hebrew/` and `py/main_diffable_pointed_hebrew.py`; the source is an archived dated breadcrumb, and its verified primary clone has left `GitRepos`. |
| 5 — Cross-repo bookkeeping and stage close | **IN PROGRESS 2026-09-04.** The configuration audit, clone-removal checks, source-state verification, oracles, vendoring regeneration, source-reference classification, and global-instruction update are complete. MAM-private still has functional Aleppo-source paths; its required third-repository edit awaits Ben's direction. |

## Phase 0 — Preflight: fresh baselines, readiness, and duplicate-data decisions

*In `C:/Users/BenDe/GitRepos/MAM-basics` only.* This phase changes only this
plan and the programme Status row. It does not copy, reformat, regenerate, or
delete files in any source repository; a diff outside those two documentation
files is a finding.

### Preconditions and measurement

Re-measure, rather than trusting the decision record, with a temporary
UTF-8 `.novc/` Python script that calls `git -C <repo> ls-files -z` and
`git -C <repo> rev-parse HEAD`. The script must print, for each repository,
the commit, tracked-file count, tracked bytes, tracked `.py` count, published
file and HTML counts, and porcelain status. It must compute the `MAM-XML/`
comparison by relative path and SHA-256, not by a working-tree `cmp`; names in
the published trees include characters that require `-z` handling.

Run the canonical test entry point from the MAM-basics primary checkout:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py
```

Run `git diff --check` before committing. No Python file is edited in this
phase, so Black is not invoked.

Fresh measurement on 2026-09-03 began from clean trees at MAM-basics
`897e8fd`, Leningrad `aa603a9`, Aleppo `8f1fcfd`, Cam1753 `3667b6c`, and
diffable-pointed-hebrew `dd1fdb9`:

| Repository | Tracked files | Tracked bytes | Tracked `.py` | `gh-pages/` files / HTML |
| --- | ---: | ---: | ---: | ---: |
| MAM-basics | 4,151 | 429,462,145 | 1,159 | 1,500 / 428 |
| codex-index-leningrad | 51 | 13,388,571 | 0 | 0 / 0 |
| codex-index-aleppo | 175 | 40,071,030 | 0 | 4 / 3 |
| codex-index-cam1753 | 152 | 84,452,058 | 0 | 0 / 0 |
| diffable-pointed-hebrew | 19 | 1,615,926 | 9 | 0 / 0 |

The workspace has 15 folders and lists all four source repositories. `MAM-XML/`
has 24 files and 7,546,243 bytes in each of Aleppo and Cam1753; the relative
paths and SHA-256 values are identical.

### Decisions prepared for Ben

The later lanes cannot silently choose either form of duplicate data.

1. `MAM-XML/` occurs in both Aleppo and Cam1753 as the same 24 blobs. Ben's
   decision, 2026-09-04, is one canonical temporary pinned `MAM-XML/` tree:
   both readers share it until the later MAM-simple evacuation replaces it.
2. `cam1753-pages/` is derived from the tracked Cam1753 spreads by
   `main_cam1753_split_spreads.py`. Ben's decision, 2026-09-04, is to retain only
   the 14 spreads (25,262,600 bytes) and regenerate the untracked page JPEGs when
   an editor or crop task needs them.

These decisions do not hold up the Leningrad lane. They do hold up the Land
step in the Aleppo and Cam1753 lanes, which must use the chosen paths in their
layer-1 blob manifests.

### Verification and execution record

Record the fresh heads, clean status, test result, workspace count, and
duplicate-data comparison under this heading. Update this plan's Status row
and the third-stage row in the programme in the same MAM-basics commit. The
next task reads the absolute path
`C:/Users/BenDe/GitRepos/MAM-basics/doc/PLAN-evacuate-the-codex-index-trio-and-diffable-pointed-hebrew.md`
and runs Phase 1 only.

### Execution record — Phase 0, 2026-09-03

Phase 0 began from clean trees at MAM-basics `897e8fd`, Leningrad `aa603a9`,
Aleppo `8f1fcfd`, Cam1753 `3667b6c`, and diffable-pointed-hebrew `dd1fdb9`.
The fresh `git ls-files -z` measurement reproduced 15 workspace folders and
the four-source roster, with no tracked Python in the three index repositories.
It found 24 `MAM-XML/` paths in each of Aleppo and Cam1753, 7,546,243 bytes in
each tree, and SHA-256 equality for every relative path. No source tree was
changed.

The canonical MAM-basics suite passed **975 passed, 5 skipped, 65 subtests**
in 151.12 seconds. `git diff --check` passed before the documentation commit.
The suite's passed count is two higher than the second-stage closeout's 973;
the recorded fresh measurement, not the older figure, is the Phase 1 baseline.
The `MAM-XML/` decision was subsequently made on 2026-09-04: one temporary
canonical pinned tree serves the Aleppo and Cam1753 readers until the MAM-simple
evacuation replaces it. Ben's same-day Cam1753 decision retains only the 14 spreads
and regenerates page JPEGs when an editor or crop task needs them.

## Phase 1 — codex-index-leningrad

*The first full lane, in `C:/Users/BenDe/GitRepos/codex-index-leningrad` and
`C:/Users/BenDe/GitRepos/MAM-basics`.* Re-measure first. Land the non-page
tree under `leningrad/`; preserve the root-relative structure so the migrated
paths module composes from `paths.repo_root() / "leningrad"`. Do not carry the
old `UXLC-utils-sparse/` as an independent source: the second stage already
repointed its vendor to MAM-basics, and this lane retires that copied tree and
the vendor entry point when its reader takes `data/lci_augrecs.json` directly.

Use the three recorded Leningrad oracles and the layer-1 manifest. Repoint the
two relative cross-links in `page-snips/README.md`; do not leave a path from
one evacuated repository pointing at another. Empty the source to its dated
breadcrumb, push and verify it on `origin/main`, archive the GitHub repository,
then remove only a clean primary clone after `git worktree list` proves no
forest worktree needs its shared Git metadata. A retained forest input keeps its
primary clone in place, while the workspace folder and visibility-map entry
still leave in the same Empty commit; no `frozen_repos` entry is added.
in the same Empty commit; no `frozen_repos` entry is added.

### Execution record — Phase 1, 2026-09-03

Phase 1 re-measured clean starting heads at MAM-basics `bc358cd` (4,152 tracked
files, 429,477,537 bytes and 1,159 tracked Python files) and
codex-index-leningrad `aa603a9` (51 tracked files, 13,388,571 bytes and no
tracked Python). The Land manifest retained five artifacts under `leningrad/`:
the three `lenin-wiki/` index files, the hand-maintained crop, and its README.
All five destination blobs matched the source blobs. The 42-file
`UXLC-utils-sparse/` tree and four root control/documentation files did not
land; no source Pages tree or licence-inventory row applied.

MAM-basics commits `84b92fac` (Land) and `079b1e63` (Repoint) moved the files,
retired the sparse vendor and its entry point, and made the index generator
read MAM-basics' canonical UXLC data directly. The generator reproduced all
three index artifacts with zero diff before and after the source removal; the
source mtime comparison after repoint also reported zero changed files. Black
on the edited Python files and `ruff check py` passed.

Source commit `86f88c0` reduced codex-index-leningrad to its dated README. Its
`HEAD` and `origin/main` were identical at `86f88c0`, no stash or unpushed
branch remained, and GitHub reported `isArchived: true`. `git worktree list`
found a clean detached review-forest input at
`C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01/codex-index-leningrad`,
pinned to manifest commit `2abd7f6`. A linked worktree shares the primary
clone's `.git` directory, so the primary clone must remain until the forest is
retired. An initial deletion attempt removed that shared metadata; the phase
re-cloned the archived `86f88c0` source and recreated the clean detached
`2abd7f6` worktree. The obsolete
`.novc/phase5_sparse_vendor_commit_message.txt` was the sole untracked residue
in the original primary clone and was discarded with that attempted deletion.

With the primary clone absent, the generator left all three index artifacts
unchanged, and the canonical MAM-basics suite passed **975 passed, 5 skipped,
65 subtests passed** in 147.79 seconds. The restored primary clone is not in
the workspace or `repo_visibility`, and remains only for the retained forest;
there is no `frozen_repos` entry. Phase 2 has not started.

## Phase 2 — codex-index-aleppo

*The Aleppo full lane.* Land the source as `aleppo/` and the published tree as
`gh-pages/aleppo/`; add the scoped data-licence row for the Aleppo scans. The
paths accessor changes to `paths.repo_root() / "aleppo"`; merge its
mark-order corpus and NFC source scopes into MAM-basics without reducing the
corpus count. Re-establish the 4-of-4 Aleppo artifact oracle and layer-1
identity before changing the source.

Freeze the three old published paths in
`in/codex-index-aleppo_redirect_pages.json`, add the Aleppo row to the
second-stage redirect table, build and test the generated stubs, and deploy the
MAM-basics target before the source switches. The Aleppo repository remains
alive as the redirect host, but its clean primary clone leaves the workspace
after the full post-removal verification. Ben's 2026-09-04 decision is one
temporary pinned `MAM-XML/` tree shared by this lane and the Cam1753 lane; the
later MAM-simple evacuation replaces it.

### Execution record — Phase 2, 2026-09-04

Phase 2 began from clean MAM-basics `b470675` and codex-index-aleppo
`8f1fcfd`. Land commit `df61173a` copied 170 committed source blobs totalling
39,905,269 bytes: 24 under the shared `MAM-XML/` snapshot, 142 under
`aleppo/`, and four under `gh-pages/aleppo/`. The five source redirect-host
files did not land. The manifest compared the source Git blob for every file,
then compared every staged MAM-basics blob; all 170 matched exactly.

Ben's 2026-09-04 decision retains that one 24-file `MAM-XML/` snapshot as a
temporary pinned input for the Aleppo and Cam1753 readers. The later MAM-simple
evacuation replaces the snapshot and removes `MAM-XML/`; Phase 2 does not begin
that later lane. Commit `a0a2a379` records the snapshot, scans, index, pages,
and remaining Aleppo data in `DATA-LICENSES.md`.

Commit `f5fdd73c` repointed `ac_paths.ac_data_root()` to `aleppo/` and
`ac_paths.mam_xml_dir()` to the shared root. The Aleppo NFC scope now scans the
hand-authored Aleppo data without also scanning it through the MAM-basics root.
The four artifact outputs — `index-flat.json`, `index-grouped-by-book.json`,
`index.wiki`, and `index-flat-annotated.json` — regenerated byte-identically;
all four destination files were rewritten, while the source files retained both
their hashes and mtimes.

Commit `d10fab55` froze the three former pages in
`in/codex_index_aleppo_redirect_pages.json` and registered the source host.
Source commit `ba655df` replaced the three pages with generated stubs and added
`404.html`; `82aa50b` removed every remaining data path and retained only the
redirect host. The target Pages deployment for `f5fdd73c` and the source Pages
deployment for `82aa50b` both succeeded. Each source stub and each MAM-basics
target answered HTTP 200, and each source stub named its corresponding target.

Commit `a21dd5e7` removed the primary clone from `all-repos.code-workspace` and
`repo_visibility`. Before deleting the direct clone, its only worktree was the
clean primary worktree, `git stash list` was empty, and its `HEAD` equalled
`origin/main` at `82aa50b`; `C:/Users/BenDe/GitRepos/codex-index-aleppo` is now
absent. Black and `ruff check py` passed. The final canonical suite passed
**974 passed, 5 skipped, 65 subtests passed** in 89.80 seconds.

## Phase 3 — codex-index-cam1753

*The Cam1753 full lane.* Land the source as `cam1753/`, retain the 14 spreads, and
regenerate the untracked `cam1753-pages/` JPEGs when needed. Add the scoped
non-commercial, attribution-required Ktiv imagery row to `DATA-LICENSES.md`.
Repoint the corpus, image helpers, crop editor and paths module onto the local
tree. Preserve the interactive editor's explicit port 8753 and repoint the
`page-snips/README.md` cross-links.

The lane's 44-of-44 artifact oracle, mtime checks and blob manifest must all
pass before the source is emptied. Then push the dated breadcrumb, archive
`bdenckla/codex-index-cam1753`, remove the workspace and visibility entries,
and remove the clean primary clone only after all worktrees are gone.

### Execution record — Phase 3, 2026-09-04

The lane began with MAM-basics at `b925d60` and codex-index-cam1753 at
`3667b6c`, both clean. The 24 source `MAM-XML/` blobs already matched the
canonical root snapshot. Land commit `e110ada3` copied the other 100 source
blobs into `cam1753/`; the staged Git-blob manifest matched all 100. It retains
the 14 spreads (25,262,600 bytes), excludes both the shared XML tree and the
derived page tree, and preserves the non-reproducible gutter chart without
rerendering it. `cdfcab56` recorded the Ktiv attribution-required,
educational-and-research, non-commercial image terms separately.

`d0222fed` repointed the corpus, crop, editor, and validation paths to
`cam1753/`, made `MAM-XML/` the shared root snapshot, and made
`cam1753-pages/` ignored output. The splitter regenerated all 28 page JPEGs
from the 14 retained spreads. The destination mtime check changed exactly the
15 split records and `check_line_breaks.html`; the generated artifacts had zero
Git content diff. `check_cam1753_all.py` passed all four checks, including
160/160 word findings, before and after the primary source clone was removed.
The sibling-reach and NFC scopes passed, as did `ruff check py`, Black on the
five edited Python files, `git diff --check`, and the final canonical suite:
974 passed and 5 skipped.

Source commit `aab417b` left exactly `.gitattributes`, `.gitignore`,
`README.md`, and `CLAUDE.md`; its `HEAD` equalled `origin/main`, the stash was
empty, and `git worktree list` reported only the clean primary worktree. GitHub
reported `isArchived: true`. MAM-basics commit `b71dbdae` removed the source
from `all-repos.code-workspace` and `repo_visibility`, updated the live crop and
snip procedures, and recorded the local `cam1753/` location. The verified
primary clone at `C:/Users/BenDe/GitRepos/codex-index-cam1753` was then removed.

## Phase 4 — diffable-pointed-hebrew

*The last source lane.* Before moving anything, diff its eight `mb_cmn/` files
against `C:/Users/BenDe/GitRepos/MAM-basics/py/mb_cmn/` and classify each
difference: upstream fix, local adaptation to retain under the
`diffable-pointed-hebrew/` data prefix, or drift to drop. A source copy is not
deleted before that classification has an execution record.

Move the root program to `py/main_diffable_pointed_hebrew.py`, with a docstring
that says it is the repository's former product command and accepts a source
file and an output file. Its samples land under `diffable-pointed-hebrew/`.
Delete the vendoring-policy entry in the deleting phase, regenerate
`doc/vendoring-inventory.md` and its dependent reports, and expect the
vendoring-policy test parametrization to lose one case. Retire the source to a
dated breadcrumb after verification; ask Ben whether this source repository is
also archived before taking that GitHub action.

### Execution record — Phase 4 classification, 2026-09-04

Before Land, committed blobs at MAM-basics `4f3d26fb` and
diffable-pointed-hebrew `dd1fdb9e` were compared for every source `mb_cmn/`
copy. No source copy is deleted before this record. The classifications are:

| source copy | classification and disposition |
| --- | --- |
| `cantsys.py` | Byte-identical to MAM-basics. Use MAM-basics' copy; no source copy lands. |
| `file_io.py` | MAM-basics has the upstream LF-default, provenance, type, and configurable-indent improvements. The source copy is drift to drop; its Windows default writes CRLF, so each source sample re-run differed from its LF tracked blob only in line endings. |
| `hebrew_accents.py` | Drift to drop. The source copy lacks maintained constants and keeps superseded non-Unicode codes; the product command does not use that surface. |
| `hebrew_letters.py` | Drift to drop: only older docstring spacing differs. |
| `hebrew_points.py` | Drift to drop. The source copy lacks maintained regular-expression constants; the product command does not use them. |
| `hebrew_punctuation.py` | Drift to drop. The source copy lacks maintained punctuation constants; the product command does not use them. |
| `str_defs.py` | Drift to drop. The source copy lacks two maintained quotation-mark constants; the product command does not use them. |
| `uni_heb.py` | Retain its local adaptation only: nine short Unicode-name assignments differ from `mb_cmn.uni_heb.shunna()` and are required by all three committed product samples. `diffable-pointed-hebrew/short_unicode_name_overrides.json` holds those nine assignments. The source copy's unused legacy utility surface is drift to drop. |

The former product command calls only `uni_heb.shunna()`. A temporary
MAM-basics candidate using the nine retained assignments and current
`mb_cmn` utilities regenerated `sample-output.json`, `tiny-sample-output.json`,
and `tiny-sample-output-normalized.json` byte-identically from their committed
source blobs. The source command's three Windows re-runs have the source
`file_io.py` CRLF output, so none is byte-identical to its LF tracked blob.

### Execution record — Phase 4 completion, 2026-09-04

Land copied seven source blobs into `diffable-pointed-hebrew/` and stored the
nine retained assignments in `short_unicode_name_overrides.json`; the staged
blobs matched the source blobs. Licence recorded the source MIT grant in
`DATA-LICENSES.md`. Repoint added `py/main_diffable_pointed_hebrew.py`, which
uses maintained `mb_cmn` utilities and accepts a source file and an output
file. Its standard and tiny samples regenerated byte-identically, and the
source clone had zero tracked-file modification-time changes during that
verification.

The source command's `--normalize` option was not moved. MAM-basics does not
normalize Hebrew, so `tiny-sample-output-normalized.json` remains preserved
historical product data rather than output of the new command. The no-Pages
source needs no redirect stubs. `misc/zarqa-table-diff/make-dph-files.ps1` now
calls the new command without normalization; one of its tracked outputs changed
at three entries where the old normalization had reordered Hebrew marks.

Empty removed the source from `all-repos.code-workspace`, `repo_visibility`,
the vendoring policy, the sibling-reach declaration, and the former vendoring
prose. Vendoring regeneration wrote 43 rows across seven destination
repositories. The source's pushed breadcrumb commit `97d95e1` retains only
`.gitattributes`, `.gitignore`, and `README.md`; `HEAD` equalled `origin/main`,
the working tree and stash were empty, and `git worktree list` named only its
primary worktree before the primary clone was moved to the Windows Recycle Bin.
The MAM-basics suite collected 977 tests with the five established skips, Ruff
passed, and Black left the edited Python files unchanged. Ben archived
`bdenckla/diffable-pointed-hebrew` on 2026-09-04; `gh repo view --json
isArchived,url` confirmed its archive state.

## Phase 5 — Cross-repo bookkeeping and stage close

Confirm all four source repositories are absent from
`all-repos.code-workspace`, `repo_visibility`, and the vendoring policy, with
no `frozen_repos` entries. Extend the MAM-basics location sections in
`CLAUDE.md` rather than duplicating them. Update `DATA-LICENSES.md`, source
README dispositions, source issue-tracker wording, and any global or
github-misc instruction copy that names an evacuated path. Search the source
repository names across the live roster and classify every hit; a third-repo
edit still stops for Ben's direction.

Re-run the canonical suite, each affected oracle, the redirect-manifest tests,
the vendoring regeneration, Black on edited Python, Ruff, and `git diff
--check`. Confirm each removal's source `origin/main` state and every
`git worktree list` result before deleting a clean primary clone. Record the
final commits and deployed redirects, update the programme Status table, then
delete the spent programme and second-stage plan only after confirming this
plan contains their remaining live decisions.

### Execution record — Phase 5 preliminary checks, 2026-09-04

The workspace has eleven folders and names none of the four evacuated source
repositories. `repo_visibility`, `in/vendoring_policy.json`, and
`frozen_repos` name none of them either. `DATA-LICENSES.md` already has the
Aleppo, Cambridge 1753, and diffable-pointed-hebrew rows the source lanes
added, so the Phase 5 audit found no licence-row change to make.

GitHub confirms that codex-index-leningrad, codex-index-cam1753, and
diffable-pointed-hebrew are archived, while codex-index-aleppo remains the
redirect host. All four source trackers have no open issue. The source
READMEs state their destination and disposition except for
diffable-pointed-hebrew's last sentence, which still says that Ben decides
whether to archive it. That sentence predates Ben's archive action. An
archived repository rejects a push, so correcting the source README would
require Ben to direct an unarchive-and-rearchive operation.

codex-index-aleppo, codex-index-cam1753, and diffable-pointed-hebrew were
already absent from `C:/Users/BenDe/GitRepos`. The Leningrad primary clone was
clean; its `HEAD` and `origin/main` were both `86f88c0`, and `git worktree
list` named only the primary checkout. The review forest named in the Phase 1
record was no longer present, so the clean primary clone was moved to the
Windows Recycle Bin. The four source clone paths are now absent.

The live-roster reference sweep classified current MAM-basics paths and prose
as destination references, redirect-host configuration, or historical records.
MAM-basics now names the local Aleppo paths in the affected command docstrings,
the Wikisource-mirror subcommand, and `doc/scan-pages.md`. The tracked
github-misc instruction copies and the live Codex instruction file now say
that codex-index-aleppo is a redirect host; github-misc commit `f2b7a9a` is
pushed. Ben authorized MAM-private's functional Aleppo-source repoint, and the
result is pushed. No functional Aleppo-source path remains in MAM-private.
Phase 5 still cannot close because correcting diffable-pointed-hebrew's stale
README requires the directed unarchive-and-rearchive operation described
above. Historical plans and dated review findings remain as execution records.

The Leningrad and Aleppo generators regenerated with zero Git diff. The
Cambridge 1753 oracle passed all four checks, including all 160 word findings.
The standard and tiny diffable-pointed-hebrew samples regenerated
byte-identically; the normalized historical sample remains data rather than
output. The redirect-manifest test passed its five tests, vendoring regeneration
reported seven rows and 43 files, Ruff passed, Black left the five edited
Python files unchanged, and the canonical suite passed 972, skipped 5, and
reported 65 subtests.

## Session discipline

One task executes one phase. Every phase re-measures its figures, writes its
execution record and Status update, commits directly to `main`, and pushes.
Run all tests and generators from the MAM-basics primary checkout; a worktree
must use `REPOS_ROOT=C:/Users/BenDe/GitRepos` for read-only sibling data, but
the removal and generation operations themselves belong in the primary clone.
Do not begin the next phase from the task that completed the current one.
