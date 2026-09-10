# Total evacuation: the five MAM products

State: live

This is the dedicated fourth-stage plan that Ben decided to have on 2026-09-05. The stage moves five public MAM products into C:/Users/BenDe/GitRepos/MAM-basics so MAM-basics no longer writes product data outside MAM-basics. The MAM-private Near Aleppo census is a separate task and remains out of scope.

The programme's “Fourth stage — the five MAM products, total evacuation” section is the decision record. The second-stage plan supplies the common Land — Licence — Repoint — Stubs — Empty — Remove lane and its four oracle layers. The third-stage plan supplies the one-lane-per-session and documentation-only Phase 0 models.

## Scope and required reading

| Role | Absolute path |
| --- | --- |
| Destination | C:/Users/BenDe/GitRepos/MAM-basics |
| Interpreter | C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe |
| Phase 1 source — retired 2026-09-06 | C:/Users/BenDe/GitRepos/MAM-simple (moved to the Windows Recycle Bin after the redirect-host commit) |
| Phase 2 source — retired 2026-09-08 | C:/Users/BenDe/GitRepos/MAM-for-Sefaria (moved to the Windows Recycle Bin after the separate safety report and Ben's approval) |
| Phase 3 source — retired 2026-09-06 | C:/Users/BenDe/GitRepos/MAM-parsed (moved to the Windows Recycle Bin after Phase 3) |
| Phase 4 source — retired 2026-09-06 | C:/Users/BenDe/GitRepos/MAM-with-doc (moved to the Windows Recycle Bin after Phase 4) |
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

The product heads remain the 2026-09-04 product heads, and all five product working trees are clean. A later Git-blob recount corrected the example totals: MAM-simple has 47 `py-examples` files and 105 `py-examples-out` files totaling 23,675,571 bytes; MAM-parsed has four example programs plus one output, and the four entry programs plus all 106 outputs total 23,500,226 bytes. Re-establish these figures from `git ls-tree -r -l HEAD` rather than working-tree sizes.

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

1. Blob identity: all 389 selected source blobs first landed as staged MAM-basics blobs with no difference. Seven selected files were then deliberately adapted before the landing commit; the execution record's original sentence omitted that post-staging qualification. The 24 temporary `MAM-XML/` blobs became the MAM-native MAM-simple XML files, and the temporary root tree was removed.
2. Regeneration: the MAM-simple corpus and three documents regenerated into MAM-basics. The 216 core corpus artifacts, 105 example outputs, 24 MAM-OSIS example artifacts, 39 MAM-for-Sefaria CSV artifacts, 39 MAM-for-Sefaria Unicode-name artifacts, and 43 vendored source files all compared byte-identically with their respective oracles.

   **Correction, 2026-09-08:** the landed Phase 1 product has 44 vendored source files, not 43.
   `MAM-simple/py-examples/mb_cmn/paths.py` was added by the Phase 1 landing commit
   `cf7c7a35` but omitted from the count above.
3. Mtime evidence: regeneration changed 407 expected MAM-basics paths and no MAM-simple source path.
4. Published URLs: MAM-basics Pages deployment `34037896289` and MAM-simple Pages deployment `34038057050` both succeeded. The deployed legacy `index.html` and `versification-and-cantillation.html` stubs contain the expected immediate redirects to the MAM-basics MAM-simple Pages targets.

Cambridge 1753's seven affected line-break JSON files were updated, under Ben's authorization, for the ten diacritic-only differences introduced by current MAM-simple. `py/check_cam1753_all.py` passed all four checks after the update.

The focused Phase 1 test set passed 47 tests. The post-removal full suite passed 973 tests, skipped 5 tests, and passed 65 subtests in 78.22 seconds. `git diff --check` passed before both commits.

Two findings were non-regressions. `py/check_ac_all.py` still reports Aleppo's pre-existing word-finding and line-break JSON-consistency failures with the landed MAM-simple reader; this lane did not change Aleppo's data. The full suite's desktop command bridge discarded its direct exit summary, so the verified result above comes from an ignored UTF-8 recorder that preserved the subprocess exit code and output.

After the source redirect Pages deployment and its live HTML verification, the source clone was clean, its `HEAD` matched `origin/main`, it had one worktree and no unpreserved branch or object, and it was moved to the Windows Recycle Bin. Its contents remain recoverable there.

**Breadcrumb correction, 2026-09-08.** Redirect-host commit `376912a` dates the README's move:
“On 2026-09-06, MAM-simple became a product tree in MAM-basics.” The temporary shallow clone
used for that correction was clean after the push and was moved to the Windows Recycle Bin.

## Phase 2 — MAM-for-Sefaria — DONE 2026-09-06

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

**Remove completion, 2026-09-08.** Ben accepted the separate clone-safety recommendation.
Immediately before retirement, the clone was clean on `main`; `HEAD`, local `main`, and
`origin/main` all equalled `cf23b478f801ca586d227693db9133da54d87f30`; one worktree, no
stash, only local `main`, and the three remote tags were present. `git fsck --unreachable
--no-reflogs` found one unreachable commit, `34c94a8`, whose patch-id equals reachable
ancestor `746d6d2`. The exact clone path `C:/Users/BenDe/GitRepos/MAM-for-Sefaria` was moved
to the Windows Recycle Bin and remains recoverable until the Recycle Bin is emptied.

## Phase 3 — MAM-parsed — DONE 2026-09-06

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

### Phase 3 Repoint, Stubs, and approval pause — 2026-09-06

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
The site-index failure required correction before claiming a green final
canonical suite; the earlier 975-pass result did not describe the later
tree. The correction and successful reruns are recorded below.

At the approval pause, Empty and Remove had **not** run. The source was clean
at `6dfc8db9`, matching remote `main`, with its product files still tracked.
Its workspace roster and `repo_visibility` entries remained in place. Automatic approval
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

The pause required direct approval, Empty and Remove, a canonical-suite and
product/history rerun with the actual sibling clone absent, and final source
deployment verification before completion. The execution record below records
that continuation. No later product lane began during the pause.

### Phase 3 Empty and Remove — approved and executed 2026-09-06

Ben's direct approval, 2026-09-06: “I approve of this deletion,” referring to
the proposed removal of the 56 duplicate product files. Automatic approval
review accepted the approved operation. Source commit
`c9e04c496920b1c423069dfbc4b31078efa0b0a0` removed exactly those paths and
installed the reviewed dated README. The source retains 27 tracked files:
the README, `.gitattributes`, `.gitignore`, its Pages workflow, 22 redirect
stubs, and `404.html`. The source commit was pushed to `main`; source Pages
deployment `34055284061` succeeded at that commit, and all 22 source/target
URL pairs again passed live HTTPS checks.

The post-stress-meteg site-index failure was resolved separately in
MAM-basics commit `d3d7e321446d7a73dfeb31dc7ef4d3247c1e78cc`. The rendered
main page already linked both new child pages; the source lint's list of
deliberately unlisted child pages lacked their names. Adding those names
beside the existing child-page entries changed no generated page. The focused
site-index tests, Black, and Ruff passed. The full pre-removal suite then
passed **975 tests and skipped 5 in 98.25 seconds**.

MAM-basics commit `9a61e7b58ccf8a9f7478f19bcb81e5485651e688` removed
MAM-parsed from `all-repos.code-workspace` and `repo_visibility` together and
was pushed. A final workspace sweep also found the MAM-parsed entry in
`MAM-basics.code-workspace`; that entry and a stale MAM-simple entry left
after Phase 1 were removed. The smaller workspace now names MAM-basics,
MAM-with-doc, and MAM-OSIS. No frozen or keep-absent entry was added.

The final source safety report at `c9e04c4` confirmed a clean tree, matching
remote copies of every local branch and tag, one primary worktree, no stash,
and no alternates. Its unreachable objects remained exactly the superseded
snapshots classified above. The only ignored file was generated Python
bytecode. The measured clone contained 3,423 files and 253,508,049 bytes.
The resolved target was checked as exactly
`C:/Users/BenDe/GitRepos/MAM-parsed`, with no reparse point, and its HEAD,
clean state, remote, and worktree count were rechecked immediately before
the Windows Recycle Bin operation. The operation succeeded; the original
path is absent and the clone remains recoverable in the Recycle Bin.

With the actual sibling clone absent and no path override, the production
parse, template-survey, pipeline-graph, site, and example commands passed.
Parse verification reported **79 passed, 0 failed, 1 pending**, retaining
the pre-existing `mp.plain.docs.book39-skeleton.common` pending check.
Regeneration changed 111 tracked destination mtimes and produced zero Git
content differences; the source path remained absent. All original corpus,
static-asset, and example blobs still match the Land manifest apart from the
previously recorded README, provenance, source-lint, and index-link changes.

The post-removal historical run reproduced every named-release and unpinned
oracle HTML/JSON byte. Current MAM-basics `HEAD` comparisons matched the
immutable migration-source comparison. Explicit legacy history raised the
required missing-clone error, and no command recreated the sibling path.
The default unpinned-latest operation also selected release `9ce6ee5` and
generated its report against MAM-basics `HEAD`, with output directed to
scratch so the later MAM-with-doc lane remained untouched.
The frozen redirect manifest passed against regenerated scratch stubs after
source removal. Logs are `post-removal-products.log`,
`post-removal-history.log`, and `after-removal-mtimes.json` under the ignored
Phase 3 evidence directory named above.

The final post-removal canonical suite passed **975 tests and skipped 5 in
93.67 seconds**, with no failure. Its command remains the canonical
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py`
from the MAM-basics root; the UTF-8 log is
`approved-post-removal-suite.log`. `git diff --check` passed, and the final
configuration/source audit confirmed the absent source path, its 27 remote
redirect-host blobs totaling 21,201 bytes, and no MAM-parsed entry in either
workspace or the maintenance-policy maps. The source Git-tree measurement
can be re-established without restoring the clone:

```powershell
gh api 'repos/bdenckla/MAM-parsed/git/trees/c9e04c496920b1c423069dfbc4b31078efa0b0a0?recursive=1'
```

All four oracle layers are complete. The MAM-basics head before the final
completion-record/workspace commit was
`9a61e7b58ccf8a9f7478f19bcb81e5485651e688`; the final source head is
`c9e04c496920b1c423069dfbc4b31078efa0b0a0`. The source remains unarchived.
Phases 5 and later remain unstarted, and MAM-private was not modified.

## Phase 4 — MAM-with-doc — DONE 2026-09-06

The fourth product lane. Land the source tree under MAM-with-doc/ and its published tree under gh-pages/MAM-with-doc/. Repoint py/main_mam_with_doc.py, py/subcommands/diff_mpp.py, MAM-parsed inputs, tests, documentation, and pipeline-graph labels. The current graph label ending in MAM-with-doc/docs/ is stale: the source has gh-pages/ and no docs/ directory. Correct the label as part of the repoint and treat the rendered graph diff as evidence.

Freeze and verify all 113 legacy HTML paths. The MAM-with-doc Pages citations in the local Wikisource introduction are Ben-controlled documentation references and must be repointed to MAM-basics; do not contact Avi Kadish or edit the mirrored Wikisource source as part of this lane.

### Phase 4 execution record — 2026-09-06

1. **Land and licence.** The frozen source at `0fe406c44c1b51e7c540574475830d6169256e73` contained 273 files totaling 47,697,350 bytes. Land commit `5a28bc0e` copied 272 selected blobs without mismatch into `MAM-with-doc/` and `gh-pages/MAM-with-doc/`; the source Pages workflow remained in the redirect host. `DATA-LICENSES.md` records the product’s CC BY-SA terms, the generated page tree, the scans’ separate rights holders, and the two Taamey font copies’ unknown terms without granting rights. The output inventory has 267 published files.

2. **Repoint and permanent inputs.** Target commit `3c8c9750` moved every Phase 4 writer and reader to the landed tree, corrected the pipeline label to `gh-pages/MAM-with-doc/`, and repointed the controlled MAM-with-doc URLs. Commit `19df42f3` removed the retired repository from the workspace and visibility configuration. `in/mam_with_doc_redirect_pages.json` records all 113 legacy HTML paths. MAM-parsed’s permanent historical inputs and the explicit `--legacy-history` sibling remained unchanged. The byte-verbatim `in/mam-ws-intro/` source mirror was not edited.

3. **Generation and checks.** The Phase 4 regenerators changed zero source files and 145 target files. A second FOI, MAM-with-doc, MAM-parsed-plus, authored-page, and pipeline-graph generation pass changed zero target output bytes. `py/main_diff.py mpp --all` reports 180 raw changes; the stored latest JSON has `diff_count` 56 and the published page has 58 cards. The frozen redirect manifest built and checked 113 stubs plus `404.html`. The source h-dot-below checker passed its 6 tests. The first full canonical suite exposed a stale generated MAM-simple versification page that still named the retired MAM-with-doc URL. `py/main_mam_simple.py doc-only` changed only that page; its targeted canonical test passed 7 tests and 27 subtests. The target and redirect host passed the HTTPS check, including a legacy page and the custom 404 page; GitHub Pages runs `34061866037` (target) and `34062108606` (redirect host) both succeeded. The final canonical suite passed 976 tests with 5 skipped and 65 subtests in 90.70 seconds.

   **Oracle qualification, recorded 2026-09-08.** Thirteen landed published files differ from
   their source blobs: ten because controlled URLs were repointed, and three generated
   change-log files because `change-log/unpinned-latest.json` moved from 24 to 56 records when
   the source's stale report was regenerated. The Phase 4 generation check established the
   current product output; it did not preserve all committed source artifacts byte-for-byte.

4. **Empty and remove.** Source commit `904c9fa` retained the dated README, Pages workflow, 113 redirect stubs, and `404.html`, and removed the former product source. Before retirement, the source clone was clean on `main`, `HEAD` equaled `origin/main` at `904c9fa178265dce6fec5704f5c0424fc94f6719`, it had one worktree, and `remediation/mp02-01-extraction-2026-09-02` was an ancestor of `main`. `C:/Users/BenDe/GitRepos/MAM-with-doc` then moved to the Windows Recycle Bin.

**Correction, 2026-09-09 (September 8 review, finding 5.2):** the retained-host list
in item 4 omits `.gitattributes` and `.gitignore`. MAM-with-doc's historical tree at
`904c9fa178265dce6fec5704f5c0424fc94f6719` retains both dotfiles alongside the README,
Pages workflow, redirect stubs, and `404.html` already listed. This corrects the
historical file inventory; the recorded retirement is unchanged.

## Phase 5 — MAM-OSIS

The fifth product lane. Land the source tree under MAM-OSIS/ and its published tree under gh-pages/MAM-OSIS/. Repoint py/main_mam_osis.py, its MAM-simple XML input, output directory, header, combined OSIS file, index page, documentation, and pipeline-graph labels to the two landed product directories. Generate the 24 OSIS book files and compare the result to the MAM-simple example's 24 OSIS blobs.

Freeze and verify the one legacy HTML path. Retain the MAM-OSIS source as a Pages redirect host. Do not contact STEPBible or CrossWire; an external client that uses an old raw MAM-OSIS URL follows the decision for a loud one-time failure.

### Phase 5 session boundaries — Ben's decision, 2026-09-10

Ben requested “bite-sized” chained tasks to avoid or minimize context compaction.
Phase 5 therefore spans the following bounded tasks. The original instruction to
complete Phase 5 end to end describes their combined result, not one task's scope.

1. **5A — checkout verification and preflight record: DONE 2026-09-10.** Record
   the exact starting trees, source inventory, committed example oracle, canonical
   suite, README disposition, and findings for the implementation tasks.
2. **5B — Land and Licence: DONE 2026-09-10.** Freeze a tracked source-to-destination Git-blob
   manifest, copy the selected source blobs, prove staged identity, and commit Land
   before adapting any copied text. Commit the scoped licence rows separately.
   Verify the deployed target page and its assets. Keep source files, writers,
   redirect configuration, and roster entries unchanged. The next task is 5C.
3. **5C — Repoint and product verification: DONE 2026-09-10.** Repoint writers, readers,
   documentation, product URLs, and pipeline labels. Merge the source hygiene
   check's scope into the canonical checker, rather than retaining an independently
   runnable duplicate. Regenerate the real product and its independent example,
   preserve and compare the frozen source artifacts, record exact source and
   destination mtime changes, and explain every changed byte. Run the canonical
   suite and affected lints. The next task is 5D.
4. **5D — Stubs and published URLs: DONE 2026-09-10.** Freeze every actual legacy HTML path,
   register the redirect host, add the authored site-index entry, generate and
   test the stubs, and deploy the destination before flipping the source pages.
   Verify every legacy/target URL pair, query/fragment preservation, and custom
   404 behavior. Keep the remaining source product files until 5E. The next task
   is 5E.
5. **5E — Empty.** After checking all preceding oracle evidence, replace the
   source product with its dated redirect-host README and retained host files.
   Remove MAM-OSIS from both workspace files and `repo_visibility` together.
   Push and verify the source deployment and clean remote-aligned heads. Keep
   the local source clone until 5F. The next task is 5F.
6. **5F — Remove and Phase 5 completion.** Re-measure source branches, tags,
   objects, stashes, ignored/untracked files, and worktrees; recycle only the
   verified safe exact source clone. Run the product/example oracle, redirect
   checks, and canonical suite with the actual sibling absent. Record exact
   commits, deployments, and results in this plan and Programme Status, then
   push and verify the final clean states. Do not begin or create Phase 6.

Each task reads the current user-wide instructions and MAM-basics `CLAUDE.md`,
this plan's common lane and README-disposition rules, the complete Phase 5 section,
and the source files and review sections relevant to its bounded work. The
programme's fourth-stage decision section and the second-stage “The oracle” and
“The per-repo lane” sections remain the authorities; consult their relevant
sections rather than repeatedly loading every completed stage's full history.
This changes repeated reading and task boundaries, not the migration's obligations.
Load `hebrew-prose` before changing accentuation prose. Ordinary URL/path
adaptations and the licence scoping already authorized by the lane do not authorize
unrelated editorial changes from the reviews.

Before creating a successor, write back the completed chunk and remaining work,
commit and push the finished changes, verify both primary checkouts, and leave
no pending edits for the successor to inherit. Create only the next bounded task,
using the saved `GitRepos` project directly (`environment.type = local`, actual
path `C:/Users/BenDe/GitRepos`); that is the available saved project containing
the required primary checkouts. Put the verified MAM-basics commit and unchanged
or deliberately advanced source commit in the successor prompt. The successor
must verify the exact repo roots, heads, branches, status, and remote ancestry
before editing. Do not substitute the saved September 8 review worktree.

### Phase 5A preflight record — 2026-09-10

Task `01a08ba3-f988-7e52-bae1-36f17b21875f`, titled “Execute Phase 5 — MAM-OSIS”,
ran from `C:/Users/BenDe/GitRepos`. Both required primary checkouts were clean
on `main`; `git rev-parse --show-toplevel`, `git rev-parse HEAD`,
`git branch --show-current`, `git status --porcelain`, `git rev-parse origin/main`,
and live `git ls-remote origin refs/heads/main` verified the exact paths and heads:

| Repository | Starting commit | Tracked files | Git-blob bytes | Python files | Published files / HTML |
| --- | --- | ---: | ---: | ---: | ---: |
| MAM-basics | `9d1de07404bd9257c3e4cafc0acc1c46b87264c9` | 5,547 | 798,180,091 | 1,221 | 1,829 / 578 |
| MAM-OSIS | `697dc98a904a52ed81bb105772f002d3efb360e3` | 92 | 29,822,402 | 1 | 30 / 1 |

Re-establish the inventory from `git -C <absolute-repo-path> ls-tree -r -l -z
<starting-commit>`, parsing the NUL-delimited records and summing committed blob
sizes. The destination has advanced since Phase 0 through the earlier landings
and subsequent work; its old figures are not the Phase 5 baseline. Every source
inventory figure still matches Phase 0 because the source commit is unchanged.

| Source tree or file | Files | Git-blob bytes |
| --- | ---: | ---: |
| `MAPM-24/` | 24 | 6,673,778 |
| `MAPM-orig-24/` | 24 | 7,853,592 |
| `MAPM-orig/` | 3 | 7,692,615 |
| `gh-pages/` | 30 | 782,189 |
| `mapm.osis.xml` | 1 | 6,800,731 |
| `header.xml` | 1 | 1,503 |
| `mapm.conf` | 1 | 2,825 |
| `osis2mod example command.txt` | 1 | 291 |
| `README.md` | 1 | 266 |
| `LICENSE.md` | 1 | 1,964 |
| `py/tests/test_h_dot_below_nfc.py` | 1 | 11,643 |
| `.gitattributes`, `.gitignore`, Pages workflow, tracked scratch message | 4 | 1,005 |

The complete source HTML set is `gh-pages/index.html`. The workflow is
`.github/workflows/pages.yml`, publishes only `gh-pages/`, and already has
`github-pages` concurrency with cancellation. Existing successful deployments
are MAM-basics run `34484135686` at `9d1de074` and MAM-OSIS run `33867262435`
at `697dc98`. These are pre-migration deployments, not proof of the future
destination or redirects. Re-establish with `gh run list --repo bdenckla/<repo>
--workflow pages.yml --limit 1 --json databaseId,headSha,status,conclusion,url`.

The canonical baseline command, run from the primary MAM-basics root with
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py`,
passed **988 tests and skipped 5 in 99.30 seconds**. The log prints no subtest
total. The old Phase 0 site-index failure is absent; a new failure must be
investigated, not accepted under that historical exception. All 24 committed
`MAM-simple/py-examples-out/osis/*.xml` blobs equal the corresponding source
`MAPM-24/*.xml` blobs by filename and Git object ID. This is a committed-input
comparison; no production or example generator was run in 5A. The real
regeneration and mtime oracles belong to 5C.

The source has no `AGENTS.md` or `CLAUDE.md`; MAM-basics' sole repository
instruction file is `CLAUDE.md`. The complete source README has three substantive
paragraphs: the OSIS extract, its SWORD/STEPBible/CrossWire purpose, and its
documentation URL. Preserve all three in `MAM-OSIS/README.md`, adapting repository
wording and the Pages URL after Land identity is proved. No substantive README
paragraph is to be dropped. Add the concise root-README link in 5C.

The remaining implementation findings are:

1. The source tracks `.novc/commit_msg_regen.txt` (113 bytes), an obsolete commit
   message, not product data. Record its exclusion from Land; it remains in
   source Git history. Retain the source workflow at the host.
2. `MAPM-orig/readme.txt` states CC BY-SA **3.0** for the historical external
   snapshot; `MAPM-orig/provenance.txt` names openscriptures/morphhb. Preserve
   that historical attribution and its separate terms. The current root
   `LICENSE.md` is byte-identical to landed `MAM-simple/LICENSE.md` and states
   CC BY-SA **4.0**. Do not apply one undifferentiated licence row to both trees.
3. The source hygiene test finds its root through Git, so a copied runnable test
   would scan MAM-basics with source-relative exclusions. Carry its generated
   and historical-data exclusions into the canonical checker in 5C; explicitly
   record the duplicate test's disposition rather than claiming it remains.
4. `py/main_mam_osis.py` already reads local `MAM-simple/xml-vtrad-bhs/`, but its
   book output, header, combined output, and page output still resolve the sibling.
   Repoint those paths. `mapm.conf` contains both an old Pages URL and an old
   GitHub data-source URL; the SWORD example command contains the old absolute
   combined-file path. The pipeline specification has two `../MAM-OSIS/` labels;
   remove the corresponding obsolete sibling-lint suppression when repointing.
5. `all-repos.code-workspace` has 6 folders and `MAM-basics.code-workspace` has
   2; both name `../MAM-OSIS`. `repo_visibility` has 7 entries, including public
   MAM-OSIS. MAM-OSIS is in neither `frozen_repos` nor `repos_to_keep_absent`.
   Re-measure these values in 5E, then remove the source from both workspaces
   and `repo_visibility` together. No replacement freeze or keep-absent entry
   is owed.

Ignored local evidence is under `C:/Users/BenDe/GitRepos/MAM-basics/.novc/phase5-mam-osis/`:
the two baseline blob inventories, the two grouped inventory reports, and
`baseline-suite.log`. The UTF-8 measurement runner is
`C:/Users/BenDe/GitRepos/MAM-basics/.novc/phase5_mam_osis_run.py`; its `inventory`
command rebuilds the inventories, and its `run <log-name> <command>...` command
saves a command's log. These are convenience evidence, not permanent oracles;
5B must commit the Land manifest. Source-retirement safety and live redirect
verification remain unperformed. No product file or MAM-private file changed.

### Phase 5B Land and Licence record — 2026-09-10

Task `01a08bae-f414-76d1-a070-66b97c7eab16` used the primary checkouts directly:
`C:/Users/BenDe/GitRepos/MAM-basics` at
`dc0e60edf6aab7fec6cc45b42002ce7541b12498` and
`C:/Users/BenDe/GitRepos/MAM-OSIS` at
`697dc98a904a52ed81bb105772f002d3efb360e3`. Root, HEAD, branch, clean status,
`origin/main`, and live remote `main` were independently verified before Land.
Both branches were `main`; no worktree was allocated.

Land commit **`1c817b5307ca535a5fc04ede8cd98add4a79a6f6`** contains the pure
prefix copies and the permanent tracked manifest
[`in/mam_osis_land_manifest.json`](../in/mam_osis_land_manifest.json).
Licence commit **`c39b6dd69e91eacd7f2ab878fe771db89972e214`** changes only
`DATA-LICENSES.md`. Both commits were pushed to primary `main` before the target
deployment check. No source commit was made.

The source was re-measured with `git -C C:/Users/BenDe/GitRepos/MAM-OSIS ls-tree
-r -l -z 697dc98a904a52ed81bb105772f002d3efb360e3`: **92 blobs / 29,822,402
bytes**. The manifest records every selected and excluded source path, source
Git blob, mode, size, SHA-256, destination, and disposition. All source modes are
`100644`; no source `AGENTS.md` or `CLAUDE.md` exists.

| Disposition | Files | Source Git-blob bytes |
| --- | ---: | ---: |
| Current product, metadata, README, license, attributes and ignore rules, under `MAM-OSIS/` | 32 | 13,481,564 |
| Historical `MAPM-orig/` and `MAPM-orig-24/`, under `MAM-OSIS/` | 27 | 15,546,207 |
| Original source-hygiene checker, under `MAM-OSIS/py/tests/`, pending 5C | 1 | 11,643 |
| Complete published tree, under `gh-pages/MAM-OSIS/` | 30 | 782,189 |
| **Selected total** | **90** | **29,821,603** |
| `.github/workflows/pages.yml`, retained at the source host | 1 | 686 |
| `.novc/commit_msg_regen.txt`, obsolete commit message excluded from Land | 1 | 113 |
| **Source total** | **92** | **29,822,402** |

The complete source README landed unchanged. Its OSIS-extract paragraph,
SWORD/STEPBible/CrossWire purpose paragraph, and documentation-URL paragraph all
remain in `MAM-OSIS/README.md`; no paragraph was dropped. Repository wording,
the operational URL, and the root README index entry remain 5C work. Both source
dotfiles were selected; the source workflow was not copied into the product.
The excluded scratch message remains in source history.

Every selected destination index entry was compared with the immutable source
using `git ls-files --stage -z`, then `git cat-file blob` verified the byte count
and SHA-256. The complete destination path set equaled the selected manifest
set. All **90** copies, including the README, matched. The same comparison
passed against Land commit `1c817b53` using `git ls-tree -r -l -z`. All **24**
`MAM-OSIS/MAPM-24/*.xml` blobs also matched the committed
`MAM-simple/py-examples-out/osis/*.xml` oracle by filename and Git object ID.
No production or example regeneration ran; regeneration and both-tree mtime
checks remain 5C work.

**Inherited whitespace:** full Land `git diff --cached --check` reported 42
diagnostics in 21 files under `MAM-OSIS/MAPM-orig-24/`. Each affected file ends
with a line containing two tabs, producing trailing-whitespace and blank-at-EOF
diagnostics. Every affected line was verified in the immutable source blob and
preserved. The manifest's `inherited_whitespace.findings` records all paths,
line numbers, diagnostics, and source blobs. The staged check passed after
excluding exactly those 21 proven source-identical paths. No whitespace rule
or historical file was changed. Licence and execution-record diffs pass the
ordinary `git diff --check` without exclusions.

The copied `MAM-OSIS/py/tests/test_h_dot_below_nfc.py` remains the original
11,643-byte blob. Its Git-root discovery would scan MAM-basics from the new
location; 5B does **not** claim that it runs with product scope. The canonical
runner collects `py/tests/`, not that copied test. Landing expands the canonical
root scan, so verification ran through
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`, from the primary
MAM-basics root:

1. `py/main_test.py py/tests/test_h_dot_below_nfc.py -q`: **6 passed in 22.48
   seconds**. No narrow canonical scope adjustment was required in 5B.
2. `py/main_test.py`: **988 passed, 5 skipped in 129.93 seconds**. No subtest
   total was printed; the 5A test inventory is unchanged.
3. `-m black MAM-OSIS/py/tests/test_h_dot_below_nfc.py`: file left unchanged,
   preserving Land blob identity.

Licence scopes are separate: current product and published files use MAM's
CC BY-SA 4.0 statement, whose source blob was verified byte-identical to
`MAM-simple/LICENSE.md`. `MAM-OSIS/MAPM-orig/` and `MAM-OSIS/MAPM-orig-24/`
retain the CC BY-SA **3.0 Unported** notice in `MAPM-orig/readme.txt`, dated
2014-02-19, with openscriptures/morphhb provenance from
`MAPM-orig/provenance.txt`. The shared quoted statement and historical notices
were not edited. The current licence inventory describes the retained source
checker; **5C must update that description when removing the duplicate**.

Target Pages run [`34489367085`](https://github.com/bdenckla/MAM-basics/actions/runs/34489367085)
succeeded at `c39b6dd6`. HTTPS verification fetched every selected published path
at `https://bdenckla.github.io/MAM-basics/MAM-OSIS/`: **30 files / 782,189
bytes**, each HTTP 200 with the expected content type and the source SHA-256.
The copied HTML references all 28 PNGs and its stylesheet by relative path;
every PNG header and dimension was valid. Percent-encoded image filenames were
checked too. The deployed
[index page](https://bdenckla.github.io/MAM-basics/MAM-OSIS/index.html) and all
assets therefore match the frozen source. This is destination deployment
evidence; legacy redirects are still 5D work.

Convenience logs and reports are under `.novc/phase5-mam-osis/`, including
`phase5b-land-suite.log`, `phase5b-land-hygiene.log`,
`phase5b-inherited-whitespace.json`, and `phase5b-deployed-assets.json`.
The permanent oracle is the tracked manifest and Land commit, not these ignored
files. `.novc/phase5b_land.py verify 1c817b5307ca535a5fc04ede8cd98add4a79a6f6`
repeats the committed copy and 24-book checks from the target Git objects.

**Next task: 5C only.** Repoint the output/header/combined/page paths, preserve
and adapt the README paragraphs, fix `mapm.conf` and the SWORD command URLs and
paths, and update the pipeline labels. Merge the source checker's generated and
historical exclusions and binary-extension coverage into the canonical checker,
then explicitly dispose of the copied checker and update its licence-inventory
description. Run real production and example regeneration, both-tree mtime
snapshots, frozen-blob comparisons, affected lints, and the canonical suite.
Keep the source product, workflow, redirect configuration, workspace roster,
and source README until their assigned 5D/5E tasks. Create 5D only after 5C's
write-back is committed and pushed and both primary trees are clean and
remote-aligned. No MAM-private change, full mega run, or Phase 6 work is authorized.

### Phase 5C Repoint and product verification record — 2026-09-10

Task `01a08bc0-2276-7052-a792-11c049d7ded9`, titled “MAM-OSIS 5C — Repoint
and product verification”, ran from `C:/Users/BenDe/GitRepos` in the saved
GitRepos project's Local mode. The primary checkouts were independently verified
with `rev-parse --show-toplevel`, `rev-parse HEAD`, `branch --show-current`,
`status --porcelain`, `rev-parse origin/main`, and live
`ls-remote origin refs/heads/main`. Both were clean on `main`, with matching
local, tracking, and live remote heads:

| Repository | Starting commit |
| --- | --- |
| `C:/Users/BenDe/GitRepos/MAM-basics` | `b7684e5500a6546611b5f442f28a1ec18c708b32` |
| `C:/Users/BenDe/GitRepos/MAM-OSIS` | `697dc98a904a52ed81bb105772f002d3efb360e3` |

Repoint commit **`ef570b8c745c40e28f8594bdceac6bdea5d3f818`** contains the
implementation and permanent
[`in/mam_osis_repoint_verification.json`](../in/mam_osis_repoint_verification.json).
The frozen Land manifest is unchanged. No source commit was made.

The file dispositions are:

1. `py/main_mam_osis.py` resolves the book directory, header, and combined file
   under `paths.repo_root() / "MAM-OSIS"`, and the page directory under
   `paths.repo_root() / "gh-pages" / "MAM-OSIS"`. Its MAM-simple input was
   already local. The existing OSIS conversion and local-schema validation code
   needed no change.
2. `MAM-OSIS/README.md` keeps all three source paragraphs: the OSIS extract,
   SWORD/STEPBible/CrossWire purpose, and documentation URL. The source and landed
   README were read side by side. The first paragraph now says product directory;
   the documentation paragraph links to the MAM-basics Pages target. The purpose
   paragraph is unchanged. Root `README.md` adds the concise product README link.
   No substantive paragraph was dropped.
3. `MAM-OSIS/mapm.conf` changes only its operational Pages URL and GitHub
   `TextSource` URL. `MAM-OSIS/osis2mod example command.txt` adds `MAM-basics/`
   to the absolute combined-file path. Historical dates, source notices, snapshots,
   and pre-existing accentuation claims are unchanged; `hebrew-prose` was loaded.
4. `py/tests/test_h_dot_below_nfc.py` gains the MAM-OSIS scope and excludes the
   product from its general root scope. The new scope retains `MAPM-24/`,
   `MAPM-orig/`, `MAPM-orig-24/`, and `mapm.osis.xml` exclusions. Published
   output is already excluded under the canonical root's `gh-pages/` prefix.
   The scope measures seven files with a floor of six: `.gitattributes`,
   `.gitignore`, `LICENSE.md`, `README.md`, `header.xml`, `mapm.conf`, and
   `osis2mod example command.txt`. The source's 16 binary extensions are a subset
   of the canonical 21; the canonical-only entries are `.docx`, `.man`,
   `.md5sum`, `.wts`, and `.xlsx`. No extension was lost. The copied
   `MAM-OSIS/py/tests/test_h_dot_below_nfc.py` was explicitly removed, and
   `DATA-LICENSES.md` no longer inventories that duplicate.
5. `py/pipeline_graph/pipeline_graph_spec.py` changes both `../MAM-OSIS/`
   display labels to `MAM-OSIS/`. `py/tests/test_sibling_reach.py` removes the
   obsolete label suppression and the production-writer sibling declaration.
   Task 5D must add a declaration for the newly registered redirect host; no
   MAM-OSIS redirect registration exists in 5C.
6. `CLAUDE.md`, `py/main_0_mega.py`, and `py/mb_cmn/paths.py` now describe the
   local OSIS product. The shared path-helper docstring was copied into
   `MAM-simple/py-examples/mb_cmn/paths.py`. All 44 declared support files were
   compared with their canonical sources, allowing only checkout CRLF/LF
   conversion; all matched. The OSIS example entry point and the mega's example
   subprocess already use the landed MAM-simple cwd. The mega was inspected but
   not run. Dated execution records were preserved.

The real commands below used
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`. Run from
`C:/Users/BenDe/GitRepos/MAM-basics`, except the example command, which requires
`C:/Users/BenDe/GitRepos/MAM-basics/MAM-simple`:

| Command after the interpreter | Result and exact write scope |
| --- | --- |
| `py/main_mam_osis.py` | 24 `MAM-OSIS/MAPM-24/*.xml` files, `MAM-OSIS/mapm.osis.xml`, `gh-pages/MAM-OSIS/index.html`, and `gh-pages/MAM-OSIS/two_col_style.css`: 27 changed destination mtimes, all bytes identical to the frozen Land blobs. Combined XML passed OSIS XSD validation with the local XML namespace schema. |
| `py-examples/main_mam_osis_example.py` | 24 changed mtimes under `MAM-simple/py-examples-out/osis/`; every file equals its committed example and the frozen Land book blob byte for byte. |
| `py/main_pipeline_graph.py` | Rewrites `doc/process-documentation/pipeline.dot`, `pipeline.svg`, and `MAM-process.dot.svg`. The last file remains byte-identical. The final DOT diff is only the shortened OSIS label; the SVG diff is that label, its narrower cylinder, and the paths and arrowheads of its two incoming edges. |

**Graph newline finding and fix:** the first graph run emitted CRLF from
`pipeline_graph.write_dot_file`, whose `open()` omitted `newline`. The writer
now passes `newline=""`; Black ran, and the canonical graph command was rerun.
The final DOT uses LF. The verification report preserves both graph runs rather
than replacing the first run's evidence. Each graph run changed the same three
mtimes, with no source write. No historical XML whitespace was normalized.

Before and after each command, snapshots covered all tracked files plus recursively
enumerated working files, including ignored outputs. Traversal omitted Git metadata,
venvs, scratch, and interpreter/lint caches; tracked files inside omitted directories
remained included. Each snapshot covered **16,748 destination files and 92 source
files**. Every source comparison returned **zero changed mtimes**. The tracked
verification report records every changed destination path, nanosecond mtime before
and after, byte count, Git blob hash, SHA-256, and comparison result. Its four
command records include the first graph run and its corrected rerun. The header,
historical snapshots, and PNG assets were not rewritten.

All 90 Land destinations were rechecked against their frozen blob hashes, sizes,
and SHA-256 values. Of those destinations, **86 remain byte-identical**, three
have the documented README/URL/path adaptations, and the duplicate checker is
removed. The 27 historical files, all 30 published files, current book and combined
exports, header, license, and product dotfiles are preserved. Independently,
`.novc/phase5b_land.py verify 1c817b5307ca535a5fc04ede8cd98add4a79a6f6`
passed for all 90 committed Land files and all 24 committed example blobs. No
generated OSIS blob difference needs an exception; none occurred.

Validation, through the canonical interpreter from the primary MAM-basics root:

1. `py/main_test.py`: **988 passed, 5 skipped in 91.35 seconds**; no subtest
   total was printed.
2. `py/main_test.py py/tests/test_h_dot_below_nfc.py py/tests/test_sibling_reach.py
   py/tests/test_vendoring_policy_paths.py py/tests/test_graphviz_version_pin.py
   py/tests/test_prose_mark_order.py -q`: **24 passed in 17.02 seconds**.
3. Black and Ruff passed for all eight changed tracked Python files; ordinary
   `git diff --check` and `git diff --cached --check` passed without exclusions.
4. After adding the permanent report and plan write-back,
   `py/main_test.py py/tests/test_h_dot_below_nfc.py
   py/tests/test_prose_mark_order.py -q`: **7 passed in 11.99 seconds**.

The OSIS published subtree is byte-identical to the deployed 5B tree. 5B's target
deployment evidence remains applicable; legacy redirects, query/fragment behavior,
and custom 404 checks remain 5D work. Ignored convenience snapshots and command logs
are in `.novc/phase5-mam-osis/`; the tracked Land manifest and Repoint report are
the permanent evidence.

**Next task: 5D only.** Freeze the source's actual legacy HTML set, register the
MAM-OSIS redirect host and its manifest tests, add the authored site-index entry,
generate and deploy targets before flipping the source Pages tree, and verify
every legacy/target URL pair plus query, fragment, and custom 404 behavior. Keep
the remaining source product, README, workflow, both workspace rosters, and
`repo_visibility` until their assigned 5E work. 5F owns source retirement and
the actual-absent-source oracle. Commit/push and verify both primary trees before
creating each successor, using the saved GitRepos project directly in Local mode.
MAM-private, the full mega, and Phase 6 remain outside this task chain's scope.


### Phase 5D Stubs and published URLs record — 2026-09-10

Task `01a08bd3-7610-7ac1-9c22-fc7c95898562`, titled “MAM-OSIS 5D — Stubs
and published URLs”, used the saved GitRepos project directly in Local mode.
`read_thread` verified its actual cwd as `C:/Users/BenDe/GitRepos`. Before editing,
the exact primary roots, HEAD, branch, clean status, `origin/main`, and live
remote `main` were verified independently:

| Primary checkout | Starting commit, equal to tracking and live remote `main` |
| --- | --- |
| `C:/Users/BenDe/GitRepos/MAM-basics` | `2d82bcbb7bd8a0967093d2b6ef09fbccf8a87dfa` |
| `C:/Users/BenDe/GitRepos/MAM-OSIS` | `697dc98a904a52ed81bb105772f002d3efb360e3` |

Target preparation **`d61c3472981f927d69a5a7452690d5130078a1c5`** and source
Pages flip **`26a7e85f8cb211043c33ef2badfddb4ac69d5ee9`** were committed and
pushed directly to primary `main`, in that order. The permanent evidence is
[`in/mam_osis_stubs_verification.json`](../in/mam_osis_stubs_verification.json).
The original Land manifest remains unchanged.

The legacy set was re-measured from `git -C C:/Users/BenDe/GitRepos/MAM-OSIS
ls-tree -r -l -z 697dc98a904a52ed81bb105772f002d3efb360e3` and independently
compared with every actual file under the source `gh-pages/`. Both sets contain
**30 files / 782,189 bytes: one HTML page, 28 PNGs, and one stylesheet**. The
only legacy HTML path is `index.html`.
[`in/mam_osis_redirect_pages.json`](../in/mam_osis_redirect_pages.json) freezes
that complete set, the source commit, date, and the lane's reason for retaining
the host. Do not rebuild this historical set from current destination files.

The implementation and source dispositions are:

1. `py/redirect_stubs/stubs.py` gains the MAM-OSIS row, preserving the existing
   pure prefix rewrite, query/fragment JavaScript, canonical link, meta refresh,
   visible fallback, and custom 404. `py/tests/test_sibling_reach.py` gains the
   corresponding redirect-only declaration. The canonical manifest test already
   parametrizes directly over `REDIRECT_REPOS`; the new row therefore adds its
   test case without a duplicate registration or test-file edit.
2. `py/author_site/site_data.py` adds MAM-OSIS under “Editions of MAM”. After
   inspecting `py/main_authored.py` and `author_site/site_index.py`, the scratch
   command `.novc/phase5d_evidence.py site-index` called the actual
   `author_site.site_index.gen_html_file()` function. Its before/after tracked-file
   mtime check records exactly one write, `gh-pages/index.html`, and zero source
   writes. The complete generated diff is one added link. No unrelated root page
   was regenerated.
3. The real CLI built and checked a preview, then `build --repo MAM-OSIS
   --publish` modified the source `gh-pages/index.html` in place and added
   `404.html`. After target deployment and HTTP verification, `git rm` removed
   exactly the 29 source published assets preserved at the destination. The
   source commit changes only `gh-pages/` and now has **64 tracked files**.
   All **62 non-published source blobs**, including the README, workflow,
   historical XML, current product, and tracked scratch message, are unchanged.
4. Both workspace files, `repo_visibility`, and the whole maintenance policy are
   unchanged. Both destination OSIS subtrees are also byte-identical to their
   5C commits. Empty and source-clone retirement remain assigned to 5E and 5F.

Deployment and URL evidence:

1. The preceding target run
   [`34492296511`](https://github.com/bdenckla/MAM-basics/actions/runs/34492296511)
   succeeded at `2d82bcbb`. Target preparation run
   [`34493549562`](https://github.com/bdenckla/MAM-basics/actions/runs/34493549562)
   succeeded at `d61c3472` **before the source flip**. Every target file returned
   HTTP 200, the expected content type, and the frozen source SHA-256: all
   **30 files / 782,189 bytes**, including percent-encoded PNG names. The live
   site index matched the generated file and linked the target.
2. Source run
   [`34493924015`](https://github.com/bdenckla/MAM-OSIS/actions/runs/34493924015)
   succeeded at `26a7e85`. The **33 HTTP checks** cover the root URL, the explicit
   index with an encoded query, `404.html`, a missing nested path, and every
   removed asset. The root and index return the exact generated stub with HTTP
   200; the explicit `404.html` returns 200; the missing path and removed assets
   return HTTP 404 with the exact generated custom-404 body.
3. Live browser navigation verified the index and root redirects with exact
   query/fragment preservation, and the custom 404 with a missing nested path
   and all three percent-encoded PNG names. The target document loaded all 28
   images. The PNG navigations reached loaded target images with their encoded
   paths, queries, and fragments intact. The missing path remained a missing
   target, as expected. Exact input/output URLs are in the permanent report.
4. The source page has no authored anchor IDs or named anchors, so the fragment
   check proves URL preservation rather than scrolling to a nonexistent anchor.
   The query surviving proves execution of the page stub's JavaScript: the meta
   refresh uses a fixed URL. An optional direct stylesheet browser navigation
   timed out with the custom-404 document still selected and is not counted as
   browser proof; the independent HTTP checks verify the source response and
   exact target CSS bytes. The temporary browser tab was closed.

The legacy Pages URL sweep ran before and after the changes with `git grep -n
-I -F bdenckla.github.io/MAM-OSIS` in every primary Git clone under
`C:/Users/BenDe/GitRepos`, including a read-only scan of MAM-private. No additional
operational citation needs repointing. MAM-basics has the dated programme source
URL record and, after preparation, the deliberate redirect-manifest description.
MAM-OSIS retains its README and `mapm.conf` links for 5E. The remaining clones
have zero hits. These editable links are not the reason for retaining the host.

Validation used `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`
from `C:/Users/BenDe/GitRepos/MAM-basics`:

1. `py/main_test.py`: **989 passed, 5 skipped in 93.90 seconds**. No subtest
   total was printed. The increase from 988 is the new MAM-OSIS manifest case.
2. `py/main_test.py py/tests/test_redirect_manifest.py
   py/tests/test_site_index_links.py py/tests/test_sibling_reach.py -q`:
   **15 passed in 3.45 seconds**.
3. `py/main_redirect_stubs.py check --repo MAM-OSIS` passed against the source
   tree; `check --repo MAM-OSIS --dir .novc/phase5-mam-osis/phase5d-stubs`
   passed against the preview. Both report one stub and `404.html`, all correct.
4. Black left all three changed tracked Python files unchanged; Ruff passed
   those files. Both repositories passed the ordinary staged and unstaged
   whitespace checks.
5. After staging the permanent report and plan write-back,
   `py/main_test.py py/tests/test_h_dot_below_nfc.py
   py/tests/test_prose_mark_order.py -q`: **7 passed in 12.02 seconds**.

Convenience evidence and command logs are under `.novc/phase5-mam-osis/`.
Inspect `.novc/phase5d_evidence.py` before reuse: `freeze` is a one-time capture,
`target-http <run-id>` and `source-http <run-id>` require that run's head to equal
the current checkout, and `verify-source-scope` intentionally stops applying
after 5E. The tracked manifests and verification reports are the permanent
evidence; none depends on keeping the ignored scratch files.

**Next task: 5E only.** Verify the preceding oracle evidence, replace the source
product with the dated redirect-host README and retained host files, and remove
MAM-OSIS from both workspace files and `repo_visibility` together. Preserve the
generated stubs and source workflow, push and verify deployment, and keep the
local source clone for 5F. Create 5F only after 5E's write-back is committed and
pushed and both primary trees are clean and remote-aligned. The saved GitRepos
project's absolute path remains `C:/Users/BenDe/GitRepos`, selected in Local
mode. No MAM-private modification, full mega, 5F execution, or Phase 6 work
occurred in 5D. Do not begin or create Phase 6.

## Phase 6 — cross-repository bookkeeping and fourth-stage close

After all five product lanes. Do not begin Phase 6 until every source is a pushed, deployed redirect host and every lane records all four oracle layers. Re-run the canonical suite, every MAM product generator, all four examples, all redirect-manifest tests, the vendoring regeneration, git diff --check, and the source-reference sweep. Re-measure the MAM-basics Git-blob count and bytes, the workspace folder count, repo_visibility, and the five source repositories' breadcrumb state. The expected structural result is five landed top-level product directories, five landed published subtrees, five source redirect hosts, and no MAM-basics product write outside MAM-basics.

Update the programme Status table and this plan with actual heads, manifest totals, deployment checks, and the exact suite result. Keep doc/PLAN-evacuate-public-repos-programme.md, doc/PLAN-evacuate-the-rest-of-three-repos.md, and doc/PLAN-evacuate-the-codex-index-trio-and-diffable-pointed-hebrew.md. The earlier planning documents are execution records and this plan cites the second-stage lane and Decision F.

Commit each finished MAM-basics change directly to main in the primary clone, or merge a completed worktree branch into the primary clone's main during the same session. Commit and push every finished source breadcrumb and MAM-basics commit. Do not push a routine worktree branch; merge it into main and push main. Ask before a force-push, a rebase, an amend, a reset, branch deletion, or any source-clone deletion whose clean and linked-worktree checks do not settle its safety.
