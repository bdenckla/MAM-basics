# Total evacuation: the five MAM products

State: Phases 0–2 completed 2026-09-06; Phase 3 Land, Licence, Repoint, and Stubs completed; Empty and Remove await direct approval after automatic approval review rejected source-file removal. MAM-with-doc and MAM-OSIS remain later lanes.

This is the dedicated fourth-stage plan that Ben decided to have on 2026-09-05. The stage moves five public MAM products into C:/Users/BenDe/GitRepos/MAM-basics so MAM-basics no longer writes product data outside MAM-basics. The MAM-private Near Aleppo census is a separate task and remains out of scope.

The programme's “Fourth stage — the five MAM products, total evacuation” section is the decision record. The second-stage plan supplies the common Land — Licence — Repoint — Stubs — Empty — Remove lane and its four oracle layers. The third-stage plan supplies the one-lane-per-session and documentation-only Phase 0 models.

## Scope and required reading

| Role | Absolute path |
| --- | --- |
| Destination | C:/Users/BenDe/GitRepos/MAM-basics |
| Interpreter | C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe |
| Phase 1 source — retired 2026-09-06 | C:/Users/BenDe/GitRepos/MAM-simple (moved to the Windows Recycle Bin after the redirect-host commit) |
| Phase 2 source | C:/Users/BenDe/GitRepos/MAM-for-Sefaria |
| Phase 3 source | C:/Users/BenDe/GitRepos/MAM-parsed |
| Phase 4 source | C:/Users/BenDe/GitRepos/MAM-with-doc |
| Phase 5 source | C:/Users/BenDe/GitRepos/MAM-OSIS |

Before every phase, read the user-level AGENTS.md, the MAM-basics CLAUDE.md, this complete plan, the complete public-repository programme, the second-stage lane and oracle sections, the complete third-stage plan, doc/dual-agent-review.md, doc/review-findings-2026-09-04.md, and the relevant source repository's instruction file. Load hebrew-prose before editing prose that makes a Hebrew accentuation claim.

Each fresh session executes exactly one phase, writes the phase's measured heads, commit identifiers, verification results, and unexpected findings back into this plan and the programme Status table, commits and pushes the finished work, then creates the next task. A product lane never starts in the same session as a later product lane.

## Decisions that govern every lane

Ben made all six decisions on 2026-09-05.

1. MAM-parsed and MAM-simple receive sparse-checkout instructions after landing. The stage creates and maintains no release archive.
2. The four example programs and all 106 tracked example outputs land in MAM-basics. The example outputs remain the independent differential oracle.
3. The stage makes no pre-emptive contact with Sefaria, STEPBible, or CrossWire. An external client that still fetches an old raw-data URL fails loudly once and repoints its data use to MAM-basics.
4. The lane order is MAM-simple, MAM-for-Sefaria, MAM-parsed, MAM-with-doc, then MAM-OSIS. MAM-simple and MAM-for-Sefaria run first because their corpus writes use ../ rather than REPOS_ROOT.
5. The fourth stage runs after the completed third stage. The third stage completed on 2026-09-04, so no third-stage lane may interleave with a fourth-stage lane.
6. This file is the dedicated plan. Phase 0 created this file and did not begin a product lane.

All five source repositories remain live Pages redirect hosts after their lanes. No source repository is archived in this stage. A Pages redirect covers published HTML URLs; a redirect does not preserve a raw data URL, a clone, or an API request.

## Phase 0 — dedicated plan and current baseline — DONE 2026-09-05

In MAM-basics planning documentation only. Phase 0 creates this file and updates the programme's fourth-stage row. Phase 0 does not copy, reformat, regenerate, or delete a product file; does not modify MAM-private; does not delete a planning file; and does not contact an external consumer. A diff outside this file and doc/PLAN-evacuate-public-repos-programme.md is a finding.

The requested base 09d12a0c is an ancestor of the clean current MAM-basics head caedcc938e8e123d330d3bf532c134eec401cad4. Phase 0 preserves the commits after 09d12a0c and plans from the actual current head rather than resetting to the older commit.

Re-measure source facts with a UTF-8 .novc Python script that invokes git -C <path> ls-tree -r -l -z HEAD, parses the NUL-delimited records, and reports committed blob sizes rather than working-tree sizes. The 2026-09-04 review found that CRLF working-tree bytes made previous records disagree with their stated Git instrument. Use git -C <path> status --porcelain separately for clean status.

The canonical suite command is:

~~~powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py
~~~

The fresh 2026-09-05 measurement started from clean trees. The figures below are Git blob facts from git ls-tree -r -l -z HEAD; each lane re-measures rather than copying them.

| Repository | HEAD | Files | Bytes | .py files | gh-pages files / HTML |
| --- | --- | ---: | ---: | ---: | ---: |
| MAM-basics | caedcc93 | 4,447 | 499,318,034 | 1,163 | 1,509 / 435 |
| MAM-simple | 7a4f21d | 392 | 107,715,529 | 49 | 4 / 2 |
| MAM-for-Sefaria | ce1e04c | 170 | 32,557,099 | 1 | 3 / 1 |
| MAM-parsed | 5108203 | 96 | 29,937,275 | 3 | 36 / 22 |
| MAM-with-doc | 0fe406c | 273 | 47,697,350 | 1 | 267 / 113 |
| MAM-OSIS | 697dc98 | 92 | 29,822,402 | 1 | 30 / 1 |

The product heads remain the 2026-09-04 product heads, and all five product working trees are clean. The example-oracle measurement also still holds: MAM-simple has 47 py-examples files and 105 py-examples-out files, totaling 23,497,110 bytes; MAM-parsed has four py-examples files and one py-examples-out file, totaling 1,522 bytes. The four example entry programs and the 106 outputs total 23,498,632 bytes, or 22.4 MiB.

The canonical suite currently has one baseline failure: py/tests/test_site_index_links.py::test_every_deploy_root_page_is_named_by_an_entry_or_excluded_by_name reports the unlisted root pages post-stress-meteg-cases.html, post-stress-meteg-misc.html, and post-stress-meteg-type-2.html. The complete result is 1 failed, 971 passed, 5 skipped in 101.92 seconds. The failure is not a fourth-stage result and Phase 0 does not change it. Each product lane must preserve this named baseline until a separately authorized task changes the site index; a new failure or a missing expected test is a lane finding.

Run git diff --check before committing. Phase 0 edits Markdown only, so Black does not run. The Phase 0 documentation commit and programme status update are the complete output of Phase 0.

## README audit of completed evacuations — 2026-09-06

The audit reads each historical source README at the revision immediately before its source became a redirect host or was retired, then compares that README with the current MAM-basics destination. A source redirect-host README is not evidence that the former product documentation survived: the source README was deliberately replaced during Empty.

| former repository | historical source README disposition | current MAM-basics disposition after this audit |
| --- | --- | --- |
| MAM-simple | The full source README landed and was adapted as `MAM-simple/README.md`. | Keep the detailed product README; the root README now indexes it. |
| MAM-for-Sefaria | The source README landed byte-identically, then its repository wording and Pages URL were corrected in `598913e5`. | Keep `MAM-for-Sefaria/README.md`; the root README indexes it. |
| codex-index-cam1753 | The source README landed as `cam1753/README.md` and its paths were adapted. | Keep the detailed product README; the root README now indexes it. |
| codex-index-leningrad | Only `page-snips/README.md` landed; the source-root overview became a redirect-host breadcrumb. | Add `leningrad/README.md` for the current index generator and page-snips evidence. |
| codex-index-aleppo | The source-root overview did not land because the redirect-host files stayed at the source. | Add `aleppo/README.md` for the current page-location data, pipeline, and published pages. |
| diffable-pointed-hebrew | The source one-line README landed unchanged. | Revise `diffable-pointed-hebrew/README.md` to name the current MAM-basics command, retained overrides, and historical normalized output. |
| holman-ketiv-qere | The source-root overview became a redirect-host breadcrumb. | Add `holman/README.md` for the three review/correction bodies, reports, and public-data boundary. |
| book-of-job | The source-root overview became a redirect-host breadcrumb. | Add `book-of-job/README.md` for the review site, current data locations, and non-regenerable source data. |
| UXLC-utils | The source-root overview became a redirect-host breadcrumb. | Add `uxlc/README.md` for the UXLC/CLC data split, current generators, and published pages. |

The root README is now the concise map to every landed product README. The detailed product README remains the reader-facing replacement for the former repository README; it is not copied wholesale into the root README.

## Common lane: Land — Licence — Repoint — Stubs — Empty — Remove

Every product lane performs the following six steps in order. The lane-specific sections name differences; a lane does not silently skip a common step.

1. Land. Re-measure the clean source head, make a Git-blob manifest for every source path that the lane lands, and copy the tree as a pure prefix under the source repository's exact name in MAM-basics. Put published files under gh-pages/<source-repository-name>/. Compare the source blobs and staged destination blobs before committing. Static files, fonts, images, and files no program rewrites stay in the manifest.
2. Licence. Add a scoped DATA-LICENSES.md row for each landed directory. Preserve the shared MAM CC BY-SA 4.0 statement. Record MAM-with-doc's documentation material separately when its source facts require it. Retain the unresolved font-terms fact for MAM-simple/gh-pages/woff2/Taamey_D.woff2; do not imply a grant that no source states.
3. Repoint. Change MAM-basics writers, readers, tests, documentation, pipeline graph labels, provenance text, and the four example subprocesses from sibling paths to the landed tree. Run the real product generator after each coherent repoint and compare generated bytes against committed destination blobs. Do not rely on git status --porcelain: a CRLF checkout can report a modified stat cache for a blob-identical file. Format every edited Python file with the canonical interpreter and run applicable source lints.
4. Stubs. Freeze every legacy published HTML path in a dedicated redirect manifest, extend py/main_redirect_stubs.py, generate and test the MAM-basics targets and source stubs, then verify deployment. Add the new target to the generated site index and to its authored description data when the first landed product gives the site a new subtree. The test suite is an invocation-time check, not continuously running CI.
5. Empty. Replace every source data path with a dated breadcrumb README and generated Pages stubs. Repoint source README links to MAM-basics, retain the source Pages workflow, remove the source from all-repos.code-workspace and in/repo_maintenance_policy.json's repo_visibility map in the same commit, and do not add a frozen_repos entry. Push the source breadcrumb and verify that HEAD matches origin/main.
6. Remove. Only after every oracle layer passes, confirm that the source clone is clean, has no unpushed branch or unique object, and has no linked worktree that needs shared Git metadata. A retained linked worktree keeps the primary clone in place until the linked worktree is retired. Do not remove a source clone while a linked worktree remains.

### README disposition — required in every remaining product lane

Treat a source README as product documentation to migrate and rewrite, not as a source-host control file that disappears when the source becomes a redirect host.

1. Before Land, read the complete source `README.md` and classify every substantive section: preserve it in the landed product README, move it to a narrower MAM-basics document or module docstring, or drop it because it governs only the former source repository. Record every disposition in the lane's execution record, including deliberate drops.
2. Include the source README in the Land blob manifest and prove its initial destination copy byte-identical with the rest of the product. Make any needed README adaptation after that proof, so the migration evidence and the current documentation are both explicit.
3. The default landing home is `<product>/README.md`. Rewrite repository-relative prose as product-directory prose; convert source-root paths to their MAM-basics paths; use relative links to other landed product directories; and change operational Pages links to `https://bdenckla.github.io/MAM-basics/<product>/`. Retain an old source URL only when the prose explicitly describes history or the redirect host.
4. Add or update one concise root-README entry that links to the landed product README and says what the product directory contains. The root README is an index, not a duplicate of the product README.
5. In Empty, replace the source README with the dated redirect-host breadcrumb. The source README links to the new product directory and its Pages target, while `<product>/README.md` is the reader-facing documentation that replaces the former repository README.
6. Before committing, read the landed and source README side by side. Verify that operational paths and Pages URLs name MAM-basics, that the root index reaches the landed README, and that no substantive source README section lacks a recorded MAM-basics home or a recorded reason to drop it.

The four oracle layers apply in every lane.

1. Blob identity proves that the landed copy has every selected source blob.
2. Zero regeneration diff proves that the repointed generator writes the destination and preserves the committed product artifact.
3. Mtime snapshots prove which tree the generator wrote. Snapshot both trees before the generator, then record the exact changed path set afterwards.
4. Published URLs prove that every frozen legacy HTML URL redirects to a deployed MAM-basics target. Links controlled by Ben are repointed; external raw data consumers remain outside the redirect contract and follow decision 3.

Run the canonical test suite, git diff --check, redirect-manifest tests, and the affected product oracle before emptying a source and after source removal. Treat the Phase 0 test_site_index_links failure as the only accepted baseline failure. A new test failure, a generator output difference, a changed source mtime, or a manifest mismatch stops the lane.

## Phase 1 — MAM-simple — DONE 2026-09-06

The first product lane. Land the source tree under MAM-simple/ and the published tree under gh-pages/MAM-simple/. Land all 47 files in MAM-simple/py-examples/ and all 105 files in MAM-simple/py-examples-out/. The three MAM-simple example entry programs remain a differential oracle, not an independent product implementation.

Before copying the source tree, repoint the MAM-simple corpus write. Replace py/mb_misc/write_utils.py's ../{mam_for_xxx} construction and py/main_mam_simple.py's variant-mam-for-xxx routing with a destination rooted at MAM-basics. Update py/mb_sefaria/mam4sef_or_ajf.py's input location at the same time. The repoint removes one worktree write that REPOS_ROOT cannot steer. Rewrite the affected docstrings, pipeline graph, tests, and documentation as exact in-repository paths.

This lane also replaces the temporary root MAM-XML/ snapshot retained for the Aleppo and Cambridge 1753 readers. Re-measure matching committed XML blobs, repoint both readers to MAM-simple/, and remove MAM-XML/ only after the Aleppo and Cambridge 1753 readers reproduce their documented artifacts. Do not begin a Cambridge 1753 product change or modify MAM-private.

Generate the three MAM-simple documents and corpus with the production command, then run the three example programs against MAM-simple/py-examples/ and compare the 105 outputs with MAM-OSIS, MAM-for-Sefaria, and MAM-basics' expected files. Freeze the two source Pages paths, extend the redirect table, deploy the source stubs and MAM-basics targets, and verify every legacy HTML URL. Add sparse-checkout instructions for MAM-simple/ to the MAM-basics documentation; do not create a release archive.

### Phase 1 execution record — 2026-09-06

The phase began with MAM-basics at `25edd2f31e7f344182f754123ca8a8d0e0061967` and MAM-simple at `7a4f21d0f7882e5c90ae46a5689d016d24528416`, both clean. MAM-basics commit `cf7c7a3509632d87a6432ce0a67cfd39ad0733e4` landed the product. MAM-simple commit `9a350be55f44029cb0349df50fc1246b4e796b38` retained the source repository as its Pages redirect host. Both commits are pushed to `main`.

1. Blob identity: all 389 selected source blobs landed as staged MAM-basics blobs with no difference. The 24 temporary `MAM-XML/` blobs became the MAM-native MAM-simple XML files, and the temporary root tree was removed.
2. Regeneration: the MAM-simple corpus and three documents regenerated into MAM-basics. The 216 core corpus artifacts, 105 example outputs, 24 MAM-OSIS example artifacts, 39 MAM-for-Sefaria CSV artifacts, 39 MAM-for-Sefaria Unicode-name artifacts, and 43 vendored source files all compared byte-identically with their respective oracles.
3. Mtime evidence: regeneration changed 407 expected MAM-basics paths and no MAM-simple source path.
4. Published URLs: MAM-basics Pages deployment `34037896289` and MAM-simple Pages deployment `34038057050` both succeeded. The deployed legacy `index.html` and `versification-and-cantillation.html` stubs contain the expected immediate redirects to the MAM-basics MAM-simple Pages targets.

Cambridge 1753's seven affected line-break JSON files were updated, under Ben's authorization, for the ten diacritic-only differences introduced by current MAM-simple. `py/check_cam1753_all.py` passed all four checks after the update.

The focused Phase 1 test set passed 47 tests. The post-removal full suite passed 973 tests, skipped 5 tests, and passed 65 subtests in 78.22 seconds. `git diff --check` passed before both commits.

Two findings were non-regressions. `py/check_ac_all.py` still reports Aleppo's pre-existing word-finding and line-break JSON-consistency failures with the landed MAM-simple reader; this lane did not change Aleppo's data. The full suite's desktop command bridge discarded its direct exit summary, so the verified result above comes from an ignored UTF-8 recorder that preserved the subprocess exit code and output.

After the source redirect Pages deployment and its live HTML verification, the source clone was clean, its `HEAD` matched `origin/main`, it had one worktree and no unpreserved branch or object, and it was moved to the Windows Recycle Bin. Its contents remain recoverable there.

## Phase 2 — MAM-for-Sefaria

The second product lane. Land the source tree under MAM-for-Sefaria/ and its published tree under gh-pages/MAM-for-Sefaria/. Repoint the Sefaria writer to the landed MAM-simple corpus and to MAM-for-Sefaria/. The lane removes the second cwd-relative corpus write that REPOS_ROOT cannot steer. Confirm that the MAM-simple example's 39 CSV blobs match the MAM-for-Sefaria CSV blobs and that the remaining _provenance.md difference names the example generator by design.

Freeze the one source Pages path, create and deploy its redirect stub, and retain the source as a Pages redirect host. Do not contact Sefaria. The source README may say that the product is suitable for Sefaria import, but no source evidence proves that a Sefaria client automatically fetches the old repository.

### Phase 2 execution record — 2026-09-06

The phase began with MAM-basics at `ca457e0b` and MAM-for-Sefaria at
`ce1e04c7ce39fc318465450eca004126c4c6128b`, both clean. MAM-basics commit
`4195440e` landed the product. MAM-for-Sefaria commit `cf23b47` retained the
source repository as its Pages redirect host. Both commits are pushed to `main`.

1. Blob identity: all 168 selected source blobs — every source path other than
   the source Pages workflow and a source-only scratch commit message — were
   staged byte-identically under `MAM-for-Sefaria/` or
   `gh-pages/MAM-for-Sefaria/`. The landed source-hygiene test then received
   the necessary product-prefix adaptation, and the static index lost its stale
   machine-specific validation comment.
2. Regeneration: `py/main_mam4sef.py` regenerated the landed output with zero
   Git content diff. All 39 standard CSV blobs match MAM-simple's example
   output; the two `_provenance.md` files differ only in the generator path by
   design.
3. Mtime evidence: the repointed generator changed zero tracked source paths.
   The product writes only inside MAM-basics.
4. Published URLs: MAM-basics Pages deployment `34048786608` and
   MAM-for-Sefaria Pages deployment `34049004202` both succeeded. Live HTTPS
   checks returned 200 for the landed target and the legacy source URL; the
   legacy page contains its immediate redirect to the target.

Ruff passed. The landed source-hygiene test passed 6 tests, and the focused
machine-path, redirect-manifest, and sibling-reach set passed 11 tests. The
canonical suite passed 974 tests and skipped 5 tests in 106.42 seconds. The
source's byte-preserved CSV, Unicode-name, and static-page blobs carry
pre-existing trailing whitespace and final blank lines, so `git diff --check`
reports them when the files enter MAM-basics; the check passed for every
Phase 2-authored change.

## Phase 3 — MAM-parsed

The third product lane. Land the source tree under MAM-parsed/ and its published tree under gh-pages/MAM-parsed/. Repoint parse-go, the MAM-parsed readers, the authored-document output, the test fixtures, and every path in the pipeline graph to MAM-parsed/plus/ or MAM-parsed/plain/ within MAM-basics. Land the MAM-parsed example program and py-examples-out/tmpl_survey_toy.json. Keep vendored-tmpl-survey-toy running against the landed example and verify its one-file differential result.

Freeze and verify all 22 legacy HTML paths. Add sparse-checkout instructions for MAM-parsed/ to the MAM-basics documentation; do not create a release archive. The source README and source Pages stubs point to the new MAM-basics paths.

### Phase 3 preflight — 2026-09-06 — paused before Land

The preflight used the primary checkout at
`C:/Users/BenDe/GitRepos/MAM-basics`, initially clean on `main` at
`bf8969e11d5827aa24e23155d4682426c4cf22ff`. The source at
`C:/Users/BenDe/GitRepos/MAM-parsed` is clean on `main` at
`51082036e5907991d0d322cb6dfcc6404802099f`. Its measured inventory remains
96 tracked files, 29,937,275 Git-blob bytes, 3 Python files, and 36 published
files including 22 HTML paths. Its only worktree is the primary clone. No
source instruction file exists among its tracked files or root files.

Re-establish the source inventory from the path, blob-size, and object columns
of this command; count HTML under `gh-pages/` separately from all published files:

```powershell
git -C C:/Users/BenDe/GitRepos/MAM-parsed ls-tree -r -l HEAD
```

The baseline canonical suite passed **974 tests and skipped 5 tests in 91.12
seconds**, using the command below. The formerly accepted site-index failure
did not recur. The UTF-8 subprocess log and initial blob inventories are in
the ignored `C:/Users/BenDe/GitRepos/MAM-basics/.novc/phase3-mam-parsed/`
directory; these are local evidence, not inputs required by a fresh checkout.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe C:/Users/BenDe/GitRepos/MAM-basics/py/main_test.py
```

During the read-only preflight, MAM-basics advanced to
`ae450bd04f3fed6d22c07a48d92deec9329adbc3` through an unrelated
post-stress-meteg merge. The merge changed no Phase 3 instruction or
change-log reader file. Before the execution-record edit, both primary
checkouts were clean and their heads matched `git ls-remote origin
refs/heads/main`. The source head remained unchanged.

**The unresolved dependency is historical MAM-parsed revisions.**
`py/mb_diff_mpu/mpplus_extract.py` (`MAM_PARSED_DIR`, `_git_show`, and
`_list_plus_files`) reads `plus/` through Git, rather than reading only the
current filesystem. `py/subcommands/diff_mpp.py` also reads commit dates,
selects the latest release by distance to source `HEAD`, and compares that
release against source `HEAD`. The release definitions read during preflight
are in `C:/Users/BenDe/GitRepos/MAM-with-doc/gh-pages/change-log/releases.json`
at MAM-with-doc `0fe406c44c1b51e7c540574475830d6169256e73`.

1. Every boundary in those release definitions resolves in MAM-parsed and
   fails with exit 128 in MAM-basics: `b5e8f94`, `3d5ecfd`, `049e636`,
   `cc43fe0`, `1880cbb`, and `9ce6ee5`. Repointing the current data directory
   does not supply these commits. An in-memory path-only repoint reproduced
   `_list_plus_files("9ce6ee5")` raising `Not a valid object name 9ce6ee5`;
   no tracked Python or product file was edited for that check.
2. Empty would remove `plus/` from the source's new `HEAD`, so retaining the
   direct clone would not preserve default comparisons. Remove would then
   remove the local repository in which the historical reads run. The
   existing canonical tests do not establish that these historical reads
   survive evacuation; the unpinned-latest tests mock the Git-dependent work.
3. The programme's carried-over decision says **“Plain copy, no git history
   graft.”** The present plan does not define how one comparison spans the
   source history and MAM-basics history, including dates and latest-release
   selection. Moving MAM-with-doc's output in Phase 4 cannot repair the input
   dependency after Phase 3 has emptied MAM-parsed.

Reproduce the missing-boundary check with these commands, then repeat for
each boundary named by the current release definitions:

```powershell
git -C C:/Users/BenDe/GitRepos/MAM-parsed rev-parse --verify '9ce6ee5^{commit}'
```

```powershell
git -C C:/Users/BenDe/GitRepos/MAM-basics rev-parse --verify '9ce6ee5^{commit}'
```

**Superseded proposal, not implemented:** preserve access to the
source's pre-evacuation Git history through an ignored bare history cache
under MAM-basics, fetched from the source remote when needed. Read legacy
revisions from that cache and current/new revisions from MAM-basics, with
explicit repository identity for each revision and a recorded migration
boundary. The cache is disposable and recreatable; first use requires
network access. This preserves arbitrary historical comparisons without
grafting histories or maintaining release archives. Implement and verify
the revision, date, and latest-release handling before resuming the lane;
keep MAM-with-doc output relocation in Phase 4. Obtain differential results
for every named release and for the latest release against the immutable
source head above before changing the reader, then compare the revised
reader's results against those results.

The complete source README was read. Its planned disposition is to preserve
every substantive section in `MAM-parsed/README.md`: product identity and
data source, JSON/parse-tree explanation, plain/plus differences, detailed
structure links, toy program and output, format-stability warning,
alternative formats, and maintainer contact. After initial blob identity,
adapt repository wording, Pages URLs, and links to landed alternatives;
correct the broken toy-program link to
`py-examples/main_tmpl_survey_toy_example.py`, and verify the stated
`good_ending` header key against the current schema. No section has a
planned deliberate drop. Initial README blob identity and final side-by-side
README verification remain unperformed because Land has not begun.

No Land, Licence, Repoint, Stubs, Empty, or Remove step was performed. All
four lane oracles remain outstanding. No product file, source README,
redirect configuration, workspace roster, or maintenance policy changed;
no source clone was removed. Phases 4 and later remain unstarted. Resume
Phase 3 only after the history strategy is decided, re-reading the required
instructions and re-measuring current heads and the canonical suite.

### Phase 3 history decision and resumed execution — 2026-09-06

Ben's decision, 2026-09-06: preserve the historical versions required by the
common change-log runs as explicit, tracked product inputs in MAM-basics.
Preserve arbitrary historical comparisons through read access to a sibling
MAM-parsed clone, required only for that rare mode. The rejected cache
proposal is not implemented. No command automatically creates or fetches
the optional clone, and its historical reads do not write to the clone.

The resumed primary checkout was clean at
`06a21a3acf3fc042a53c5faec32f8e802e625544`. The MAM-parsed source remained
clean at `51082036e5907991d0d322cb6dfcc6404802099f`.

1. Land commit `63cf6c98` copied every source blob except its Pages workflow:
   95 files and 29,936,589 bytes under `MAM-parsed/` and
   `gh-pages/MAM-parsed/`. Every staged blob matched the source, including
   the complete README and all static assets.
2. Licence and historical-input commit `8176e91d` retained the scoped MAM
   licence and unresolved font terms. The historical tree stores the
   named-release boundary inputs: 144 JSON blobs totaling 84,572,003 bytes.
   Every staged historical JSON blob matched its recorded source commit.
   Both commits were pushed to `main`.
3. Before changing the reader, every named-release report and the latest
   release against source `51082036` was generated into ignored scratch
   files. The revised reader reproduced every HTML and JSON byte with
   `REPO_MAM_PARSED_DIR` pointing at a nonexistent path. Explicit legacy
   mode matched the stored-input comparison and failed when that clone was
   absent. `--legacy-history` selects sibling refs; normal `HEAD` selects
   the committed landed product. The migration metadata preserves the
   initial source date and the release ordering across the move.
4. The first repointed `py/main_parse.py go` run passed 79 checks with
   1 pending documentation check. It changed 74 tracked destination mtimes
   and zero tracked source mtimes. All original landed blobs remained
   content-identical. Subsequent README, index-URL, and example-provenance
   adaptations are required path/documentation changes, recorded separately
   from that initial zero-difference regeneration.

The historical source-only README link and `good_ending` key were corrected
in the preserved product README; every original substantive section remains,
with no deliberate drop.

### Phase 3 Repoint and Stubs record; Empty approval pending — 2026-09-06

Repoint commit `8e5735fb722a368c0c19a20ef815fded8dea567a` moved the production
writers, MAM-basics readers, authored documentation, graph labels, and example
execution to the landed product. Commit
`2a50fd15a2c8e4b73b91fa486b79eee508360ca9` added the frozen redirect manifest,
redirect-host configuration, site-index entry, and an example-support copy
fix that preserves LF bytes even when the canonical Python checkout uses
CRLF. Both commits were pushed. An unrelated post-stress-meteg merge then
advanced clean MAM-basics to `718f48b5fd4381b13a2f4360589fefce9046459b`;
that merge changed no Phase 3 path.

1. Regeneration and mtimes: the final product check ran `py/main_parse.py go`,
   `py/main_tmpl_survey.py`, `py/main_pipeline_graph.py`,
   `py/main_authored.py gen-site`, and the real mega-pipeline
   `vendored-tmpl-survey-toy` runner with the MAM-parsed sibling override
   pointing at a nonexistent directory. It changed 109 tracked destination
   mtimes and zero tracked source mtimes. Core JSON, all 12 call-graph SVGs,
   and the example output match the original source blobs. The only landed
   blob differences are the adapted product README, example provenance,
   example source-hygiene test, and published index README link.
2. Historical oracle: all five named releases and the unpinned comparison
   against immutable source `51082036` reproduced the original HTML and JSON
   bytes. Their raw-change counts are respectively 76, 557, 19, 139, 33, and
   180. The stored-input comparison against MAM-basics `HEAD` also matched
   the read-only sibling comparison. Missing legacy history fails rather
   than creating or fetching a clone. The real `--legacy-history` CLI was
   exercised with explicit refs and scratch output. Change-log output remains
   in MAM-with-doc pending Phase 4; no published change-log regeneration was
   performed as part of Phase 3.
3. Published URLs: MAM-basics Pages deployment `34054337177` succeeded at
   `2a50fd15`. MAM-parsed source commit
   `6dfc8db93f967b2335b9a7b59c62296b4780902f` replaced the 22 original HTML
   pages with generated stubs, added `404.html`, and removed the 14 superseded
   site assets. Its Pages deployment `34054626554` succeeded. Live HTTPS
   checks returned 200 for all 22 targets and all 22 legacy HTML URLs; every
   source page carries the expected immediate redirect and query/fragment
   preservation script. Local redirect lint also passed for all 22 stubs and
   the catch-all.
4. Verification findings: the canonical suite passed 975 tests and skipped 5
   in 107.51 seconds after the repoint. Initial lint failures identified
   historical/generated JSON wrongly included in the source NFC check and
   obsolete sibling-path exemptions; the corrected scopes preserve the source
   JSON bytes. The landed source-hygiene suite passed 6 tests. Black, Ruff,
   and `git diff --check` passed for the authored changes. Adding the new
   redirect row initially changed the default command choice; the row order
   was corrected to preserve the existing default.

The final pre-Empty rerun at MAM-basics `718f48b5` reported **1 failed,
974 passed, and 5 skipped in 101.63 seconds**. The failure is
`test_site_index_links.py::test_every_deploy_root_page_is_named_by_an_entry_or_excluded_by_name`,
which names `post-stress-meteg-type-1-lacks-mas.html` and
`post-stress-meteg-type-2-lacks-mas.html` as unlisted deploy-root pages.
Those pages belong to the separately active post-stress-meteg work; Phase 3
did not edit those pages or their site-index entries. The MAM-parsed tests
passed. The last historical-oracle rerun also passed all byte comparisons,
legacy parity, and the required failure when the legacy clone is absent.
Record and resolve the site-index failure before claiming a green final
canonical suite; the earlier 975-pass result does not describe the later
tree.

Empty and Remove have **not** run. The source remains clean at `6dfc8db9`,
matching remote `main`, with its product files still tracked. Its workspace
roster and `repo_visibility` entries remain in place. Automatic approval
review rejected the attempted Empty command before execution, then rejected
a retry supported by the recovered Phase 3 launch instructions: the review
requires direct user authorization for deleting the 56 source product files
and does not accept the agent-created delegation as authorization for that
scope. No workaround or further deletion attempt was made.

The prepared Empty step removes only the 56 product paths already preserved
in pushed Land commit `63cf6c98`, replaces the source README with the dated
redirect-host breadcrumb, and retains `.gitattributes`, `.gitignore`, the
Pages workflow, all 22 stubs, and `404.html`. Remove then retires only
`C:/Users/BenDe/GitRepos/MAM-parsed` through the Windows Recycle Bin, after
rechecking the source commit, working tree, refs, objects, and worktrees.
The workspace and visibility-map entries must leave together when Empty
completes. No history rewrite is required.

The source safety check found one primary worktree, no stash, matching
remote copies of every local branch and tag, and only generated Python
bytecode among ignored files. The unreachable commit `c7d7ba69` has the
identical full tree as remote-preserved ancestor `6766d3d9`. The unreachable
commit `53eed580` differs from remote-preserved ancestor `cc43fe04` only by
a superseded documentation-link sentence; its implementation and data are
preserved. Both reachable counterparts and the original source `51082036`
were verified as ancestors of `origin/main`. These findings do not identify
unmerged implementation work; the Recycle Bin would retain the local
objects as well. Re-measure rather than treating the safety report as valid
indefinitely.

Local evidence and the exact product-path removal list are under
`C:/Users/BenDe/GitRepos/MAM-basics/.novc/phase3-mam-parsed/`, including
`retirement-proof.json`, `source-safety-before-empty.json`,
`live-source-pages.json`, and the product/history oracle logs. The proposed
source README is
`C:/Users/BenDe/GitRepos/MAM-basics/.novc/phase3_mam_parsed_source_readme.md`.
These ignored files are review evidence; the committed product, historical
manifest, and redirect manifest are the durable inputs.

After approval, complete Empty and Remove, rerun the canonical suite and
product/history oracles with the actual sibling clone absent, verify the
final source deployment, and record the final source and destination commits.
Do not begin Phase 4 or create a successor while Phase 3 remains unfinished.

## Phase 4 — MAM-with-doc

The fourth product lane. Land the source tree under MAM-with-doc/ and its published tree under gh-pages/MAM-with-doc/. Repoint py/main_mam_with_doc.py, py/subcommands/diff_mpp.py, MAM-parsed inputs, tests, documentation, and pipeline-graph labels. The current graph label ending in MAM-with-doc/docs/ is stale: the source has gh-pages/ and no docs/ directory. Correct the label as part of the repoint and treat the rendered graph diff as evidence.

Freeze and verify all 113 legacy HTML paths. The MAM-with-doc Pages citations in the local Wikisource introduction are Ben-controlled documentation references and must be repointed to MAM-basics; do not contact Avi Kadish or edit the mirrored Wikisource source as part of this lane.

## Phase 5 — MAM-OSIS

The fifth product lane. Land the source tree under MAM-OSIS/ and its published tree under gh-pages/MAM-OSIS/. Repoint py/main_mam_osis.py, its MAM-simple XML input, output directory, header, combined OSIS file, index page, documentation, and pipeline-graph labels to the two landed product directories. Generate the 24 OSIS book files and compare the result to the MAM-simple example's 24 OSIS blobs.

Freeze and verify the one legacy HTML path. Retain the MAM-OSIS source as a Pages redirect host. Do not contact STEPBible or CrossWire; an external client that uses an old raw MAM-OSIS URL follows the decision for a loud one-time failure.

## Phase 6 — cross-repository bookkeeping and fourth-stage close

After all five product lanes. Do not begin Phase 6 until every source is a pushed, deployed redirect host and every lane records all four oracle layers. Re-run the canonical suite, every MAM product generator, all four examples, all redirect-manifest tests, the vendoring regeneration, git diff --check, and the source-reference sweep. Re-measure the MAM-basics Git-blob count and bytes, the workspace folder count, repo_visibility, and the five source repositories' breadcrumb state. The expected structural result is five landed top-level product directories, five landed published subtrees, five source redirect hosts, and no MAM-basics product write outside MAM-basics.

Update the programme Status table and this plan with actual heads, manifest totals, deployment checks, and the exact suite result. Keep doc/PLAN-evacuate-public-repos-programme.md, doc/PLAN-evacuate-the-rest-of-three-repos.md, and doc/PLAN-evacuate-the-codex-index-trio-and-diffable-pointed-hebrew.md. The earlier planning documents are execution records and this plan cites the second-stage lane and Decision F.

Commit each finished MAM-basics change directly to main in the primary clone, or merge a completed worktree branch into the primary clone's main during the same session. Commit and push every finished source breadcrumb and MAM-basics commit. Do not push a routine worktree branch; merge it into main and push main. Ask before a force-push, a rebase, an amend, a reset, branch deletion, or any source-clone deletion whose clean and linked-worktree checks do not settle its safety.
