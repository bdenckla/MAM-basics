# Total evacuation: the codex-index trio and diffable-pointed-hebrew

State: Phase 0 complete — the third stage began 2026-09-03

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
| 0 — Preflight: fresh baselines, readiness, and duplicate-data decisions | **DONE 2026-09-03.** The source trees are clean; the fresh MAM-basics suite passed 975 / 5 / 65; the two duplicate-data decisions are recorded for the Aleppo and Cam1753 lanes. |
| 1 — codex-index-leningrad | Not started. Its lane is first and archives the source repository after the verified Empty step. |
| 2 — codex-index-aleppo | Not started. Its lane lands `aleppo/` plus `gh-pages/aleppo/`, freezes the three-page redirect manifest, and leaves the source repository alive. |
| 3 — codex-index-cam1753 | Not started. Its lane lands `cam1753/`, answers the page-image decision recorded below, and archives the source repository after the verified Empty step. |
| 4 — diffable-pointed-hebrew | Not started. Its lane resolves the eight divergent `mb_cmn` copies before moving the root command to `py/main_diffable_pointed_hebrew.py`. |
| 5 — Cross-repo bookkeeping and stage close | Not started. It removes the four workspace entries, performs the final clone-removal checks, records the source-repository dispositions, and closes this stage. |

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

1. `MAM-XML/` occurs in both Aleppo and Cam1753 as the same 24 blobs. The
   Aleppo and Cam1753 readers can share one copy after the repoint. Ben decides
   whether MAM-basics retains one canonical `MAM-XML/` tree or preserves two
   pure-prefix copies.
2. `cam1753-pages/` is derived from the tracked Cam1753 spreads by
   `main_cam1753_split_spreads.py`. Ben decides whether the 48.0 MB page tree
   remains tracked as an oracle or is regenerated from the spreads when needed.

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
The two duplicate-data questions remain Ben's decisions. They do not block the
Leningrad lane, which begins next; they must be answered before an Aleppo or
Cam1753 Land step chooses its `MAM-XML/` or `cam1753-pages/` disposition.

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
forest worktree survives. Remove its workspace folder and visibility-map entry
in the same Empty commit; no `frozen_repos` entry is added.

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
after the full post-removal verification. The `MAM-XML/` disposition must be
Ben's Phase-0 decision, not a fresh local choice.

## Phase 3 — codex-index-cam1753

*The Cam1753 full lane.* Land the source as `cam1753/`, retain or regenerate
`cam1753-pages/` exactly as Ben decided in Phase 0, and add the scoped
non-commercial, attribution-required Ktiv imagery row to `DATA-LICENSES.md`.
Repoint the corpus, image helpers, crop editor and paths module onto the local
tree. Preserve the interactive editor's explicit port 8753 and repoint the
`page-snips/README.md` cross-links.

The lane's 44-of-44 artifact oracle, mtime checks and blob manifest must all
pass before the source is emptied. Then push the dated breadcrumb, archive
`bdenckla/codex-index-cam1753`, remove the workspace and visibility entries,
and remove the clean primary clone only after all worktrees are gone.

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

## Session discipline

One task executes one phase. Every phase re-measures its figures, writes its
execution record and Status update, commits directly to `main`, and pushes.
Run all tests and generators from the MAM-basics primary checkout; a worktree
must use `REPOS_ROOT=C:/Users/BenDe/GitRepos` for read-only sibling data, but
the removal and generation operations themselves belong in the primary clone.
Do not begin the next phase from the task that completed the current one.
