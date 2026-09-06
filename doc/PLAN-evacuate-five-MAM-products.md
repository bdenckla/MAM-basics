# Total evacuation: the five MAM products

State: Phase 0 completed 2026-09-05; no product lane has started

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

## Common lane: Land — Licence — Repoint — Stubs — Empty — Remove

Every product lane performs the following six steps in order. The lane-specific sections name differences; a lane does not silently skip a common step.

1. Land. Re-measure the clean source head, make a Git-blob manifest for every source path that the lane lands, and copy the tree as a pure prefix under the source repository's exact name in MAM-basics. Put published files under gh-pages/<source-repository-name>/. Compare the source blobs and staged destination blobs before committing. Static files, fonts, images, and files no program rewrites stay in the manifest.
2. Licence. Add a scoped DATA-LICENSES.md row for each landed directory. Preserve the shared MAM CC BY-SA 4.0 statement. Record MAM-with-doc's documentation material separately when its source facts require it. Retain the unresolved font-terms fact for MAM-simple/gh-pages/woff2/Taamey_D.woff2; do not imply a grant that no source states.
3. Repoint. Change MAM-basics writers, readers, tests, documentation, pipeline graph labels, provenance text, and the four example subprocesses from sibling paths to the landed tree. Run the real product generator after each coherent repoint and compare generated bytes against committed destination blobs. Do not rely on git status --porcelain: a CRLF checkout can report a modified stat cache for a blob-identical file. Format every edited Python file with the canonical interpreter and run applicable source lints.
4. Stubs. Freeze every legacy published HTML path in a dedicated redirect manifest, extend py/main_redirect_stubs.py, generate and test the MAM-basics targets and source stubs, then verify deployment. Add the new target to the generated site index and to its authored description data when the first landed product gives the site a new subtree. The test suite is an invocation-time check, not continuously running CI.
5. Empty. Replace every source data path with a dated breadcrumb README and generated Pages stubs. Repoint source README links to MAM-basics, retain the source Pages workflow, remove the source from all-repos.code-workspace and in/repo_maintenance_policy.json's repo_visibility map in the same commit, and do not add a frozen_repos entry. Push the source breadcrumb and verify that HEAD matches origin/main.
6. Remove. Only after every oracle layer passes, confirm that the source clone is clean, has no unpushed branch or unique object, and has no linked worktree that needs shared Git metadata. A retained linked worktree keeps the primary clone in place until the linked worktree is retired. Do not remove a source clone while a linked worktree remains.

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

## Phase 3 — MAM-parsed

The third product lane. Land the source tree under MAM-parsed/ and its published tree under gh-pages/MAM-parsed/. Repoint parse-go, the MAM-parsed readers, the authored-document output, the test fixtures, and every path in the pipeline graph to MAM-parsed/plus/ or MAM-parsed/plain/ within MAM-basics. Land the MAM-parsed example program and py-examples-out/tmpl_survey_toy.json. Keep vendored-tmpl-survey-toy running against the landed example and verify its one-file differential result.

Freeze and verify all 22 legacy HTML paths. Add sparse-checkout instructions for MAM-parsed/ to the MAM-basics documentation; do not create a release archive. The source README and source Pages stubs point to the new MAM-basics paths.

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
