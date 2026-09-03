# MAM mega-pipeline review, Phase 13: whole-pipeline integration and closeout

Review date: 2026-09-01.

Phase 13 completes the staged review of the 42 registered steps beneath
`py/main_0_mega.py`. It expands the review forest to every runtime and canonical
test dependency, runs the complete real entry point twice, runs the full test
suite, reconstructs the finding ledger from the exact Phase 0–12 sources, and
records the review-only output changes before restoring them. Phase 13 does not
fix production code, merge either review branch, create a remediation forest, or
retire the review forest.

The governing forest is
`C:/Users/BenDe/Documents/Codex/ReviewForests/mam-mega-review-2026-09-01`.
The `worktree-forest` skill governed forest expansion and baseline preservation.
The `hebrew-prose` skill governed every finding and report statement involving
Hebrew accentuation.

## Outcome

The integration run succeeds and is deterministic after its first refresh:

1. the live registry has 42 unique steps and `vendoring-audit` is last;
2. the first complete run returned 0 and changed 45 tracked working-byte states
   in four repositories;
3. the second complete run returned 0 and its complete watched-content post-state
   exactly equals the first run's post-state;
4. the final suite reported **971 passed and 5 skipped in 144.39 seconds** and
   changed no nonignored forest content; and
5. every review-only output was restored through a closed 45-path allowlist, and
   no detached dependency HEAD changed.

The first-run changes are not all harmless. Phase 13 adds three P2 findings:

1. `MP13-01`: the installed Graphviz 16.0.0 rewrites 12 SVGs committed from
   Graphviz 15.1.1, while the external-tool version is neither pinned nor
   recorded as a generated-output input;
2. `MP13-02`: 29 tracked text artifacts are rewritten only at the working-byte
   and line-ending level on the first run from a clean checkout; and
3. `MP13-03`: the published `15 P1 / 33 P2 / 41 P3` severity split cannot be
   reproduced from the 89 original finding labels.

Reconstruction preserves the original labels. The prior 89 findings are **12 P1,
58 P2, and 19 P3**. With the three Phase 13 P2 findings, the final cumulative
total is **92 findings: 12 P1, 61 P2, and 19 P3**. The public companion contains
85 findings; seven private findings are represented publicly only by their
aggregate `2 P1 / 4 P2 / 1 P3` count.

## Forest completion and dependency derivation

Phase 13 re-derived the dependency graph from the live registry, path APIs,
subprocess working directories, imports, vendoring policy, and canonical-suite
inputs. The deliberately eight-member Phase 10–12 forest lacked ten clean
dependencies. Phase 13 verified each primary clone on `main`, clean, synchronized
with `origin/main`, and at the exact recorded commit before adding a detached
worktree. No primary-clone fallback remains.

The complete 18-member matrix at the pre-report checkpoint is below. The two
review branches may advance only by the authorized Phase 13 reports and ledgers;
their immutable historical baselines remain recorded in `review-manifest.json`.
For MAM-basics, `HEAD` after the report commit means the commit containing this
report; the local manifest records its exact hash after commit. Detached heads
remain literal and immutable.

| Repository | Phase 13 pre-report head | Checkout | Role | Expected origin |
|---|---|---|---|---|
| MAM-basics | `b98f64011b07dc512d8e9a8723a844e9dd42c15c` | `review/mega-pipeline-2026-09-01` | entry point, public plan, report, and public ledger | `https://github.com/bdenckla/MAM-basics.git` |
| MAM-private | `3aa273676bdad84e7b78f59abf0a06eda94aa6e3` | `review/mega-pipeline-2026-09-01` | private runner/input, private report, and canonical ledger | private origin; exact URL remains in the local manifest |
| MAM-parsed | `46209cdf17fee718fb893c63fa34a97e8ab0141a` | detached | pipeline output and downstream input | `https://github.com/bdenckla/MAM-parsed.git` |
| codex-index-aleppo | `1c12a8ed2382ffad1a7e52874bffa5788f26b80a` | detached | read-only census input | expected origin recorded locally |
| MAM-with-doc | `999a4371b1d6cf9bec779b873a4ae87aed997dee` | detached | pipeline output and link/census input | `https://github.com/bdenckla/MAM-with-doc.git` |
| MAM-simple | `cd2bef876312187e21386e4c16c3193a5711a59d` | detached | pipeline output, later accgram input, vendoring destination | `https://github.com/bdenckla/MAM-simple.git` |
| MAM-OSIS | `2f783d1d0b1294491e8187c9016eb904a1acff49` | detached | pipeline output and census input | `https://github.com/bdenckla/MAM-OSIS.git` |
| MAM-for-Sefaria | `cf193470f6a33d3ed8157b67c4c92efd594d1e11` | detached | pipeline output and census input | `https://github.com/bdenckla/MAM-for-Sefaria.git` |
| UXLC-utils | `b7b4eb9706b1db1ae87410cb79319ad321d38eb7` | detached | pipeline and test input | `https://github.com/bdenckla/UXLC-utils.git` |
| diffable-pointed-hebrew | `dd1fdb9e56490f83793bfc72b9b2d3a91389319c` | detached | vendoring and test input | `https://github.com/bdenckla/diffable-pointed-hebrew.git` |
| book-of-job | `d09b966e5293605fdac843259da5eb258a5ee967` | detached | canonical-suite data input | `https://github.com/bdenckla/book-of-job.git` |
| codex-index-cam1753 | `73098821c9d5c96241f9e246d8974258c32a9f13` | detached | canonical-suite data input | `https://github.com/bdenckla/codex-index-cam1753.git` |
| codex-index-leningrad | `2abd7f6d4b6ebfbad5c39545fc830b9b3f1e8165` | detached | canonical-suite data input | `https://github.com/bdenckla/codex-index-leningrad.git` |
| github-misc | `f8898a95ee4ca04f631006644c80ad3646f9c911` | detached | canonical-suite policy input | expected origin recorded locally |
| hbofonts | `96bd8ae2baf473278a62d461915eef475d5a373b` | detached | canonical-suite policy input | `https://github.com/bdenckla/hbofonts.git` |
| holman-ketiv-qere | `94cab4af489a8ebb463988d9c46ddef4c838b701` | detached | canonical-suite data input | `https://github.com/bdenckla/holman-ketiv-qere.git` |
| phonetic-hbo | `593549731a2f9e1629b3614ea090112a0c8ce527` | detached | canonical-suite policy input | `https://github.com/bdenckla/phonetic-hbo.git` |
| Taamey_D | `4a3c8369c4bea391d5d9ea4e2858335f503197b6` | detached | canonical-suite policy input | expected origin recorded locally |

The three SSH origin URLs omitted from the public table are retained exactly in
the local manifest. There are zero primary-clone exceptions.

## Preflight evidence

The preflight used command-local `safe.directory` configuration for each
repository and process-local Git configuration for child processes. It did not
change global Git configuration. It verified:

1. all 18 worktree paths, origin URLs, expected HEADs, checkout modes, and clean
   states;
2. both review branches at zero ahead and zero behind their upstreams before
   Phase 13 report writes;
3. 42 unique live `StepRecord` IDs with `vendoring-audit` last;
4. the primary MAM-basics interpreter at
   `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe` and no `.venv`
   inside any worktree; and
5. the Phase 10 census baseline: 87 tracked expected files with aggregate
   SHA-256 `e267f49ad6a1f944ecf1ce884f729179d58f88daea9b7899b5d9f29ef96f2435`.

## Runtime, write, and test graph

The real pipeline ran from the MAM-basics worktree with `REPOS_ROOT` set to the
forest root and all 18 `REPO_<NAME>_DIR` variables set to their forest worktrees.
MAM-basics, MAM-parsed, MAM-with-doc, MAM-simple, MAM-OSIS,
MAM-for-Sefaria, and MAM-private are pipeline write targets. UXLC-utils,
diffable-pointed-hebrew, codex-index-aleppo, and the writer repositories also act
as runtime inputs. The remaining repositories are read-only canonical-suite
inputs.

The recorded cross-step interactions are:

1. `parse-go` writes MAM-parsed; later MAM-parsed readers consume that regenerated
   tree.
2. `mam-with-doc` and `diff-mpp` write MAM-with-doc after `parse-go` supplies their
   MAM-parsed input.
3. `mam-simple` writes MAM-simple; Sefaria/AJF, OSIS, letter-small-job, and accgram
   read the regenerated MAM-simple tree.
4. `wlc-vendor-uxlc` reads UXLC-utils and refreshes inputs consumed by later WLC
   and accgram steps.
5. `wlc-json-and-unicode` refreshes outputs used by later accgram steps.
6. prose and poetic accgram runs write grammar outputs consumed by grammaticality
   and HTML generation.
7. the chanted-word accent survey writes the survey trusted by accgram HTML
   generation.
8. the UXLC accent-change filter writes the JSON consumed by the UXLC grammar
   test.
9. sigil inventory and the private census read the MAM-parsed tree regenerated by
   `parse-go`.
10. the private census writes its tracked expected outputs.
11. vendoring reads MAM-simple after its support copies are refreshed and also
    reads its other policy-defined repositories.

## Two complete runs and exact changed-output inventory

Both runs invoked the real entry point:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
```

The final evidence runs returned 0 in 243.26 seconds and 396.33 seconds. Each run
reported 79 MAM-parsed claims passed, 0 failed, and 1 pending; 670 explicit-ḥataf
mappings with 0 failures; and 4,450 of 4,465 clean poetic parses, with 13
missing-silluq error records and 2 verses without a parse.

The first run changed 45 tracked working-byte states. The aggregate hashes below
hash each changed path, size, and file SHA-256 in sorted path order.

| Repository | Changed paths | Before aggregate | After aggregate |
|---|---:|---|---|
| MAM-basics | 17 | `a3734ffb926dd68a0761d6449c2e893b2d54ec84d1e291ff2e095df50f93b3c0` | `08133189e71789600a44c268427dd1ba49daebd3a91523e30d50869a39a08bb2` |
| MAM-parsed | 13 | `6610187cd49f6d95ec744ae98add58ece26d8c89ba7a14d9c884ad9712198c24` | `45d69bdbaffede989bc50ab9c74cd19f50c2db5ffab2d46eebfc1ececa381369` |
| MAM-with-doc | 13 | `f96dcaa9d5631dda49cf8909a6cf5789300c4699ad34c47b6fc258657bfdeb80` | `b82252130346a9eb962db56425936be011684c12fbae632ae9345b7e555c3784` |
| MAM-simple | 2 | `6ae7d71ba1fc67abfb03c3d402c04a507e44551211516dd1802ed31bdb72b1b7` | `096ee8cfe10cbd33c71afb8d0b75034c1ebddb4a8d6edb93914f85ab6703a172` |

Sixteen paths had normalized-content differences:

1. MAM-basics `doc/vendoring-inventory.md` and
   `out/vendoring_compare_out.txt`;
2. all 12 MAM-parsed call-graph SVGs;
3. MAM-with-doc `gh-pages/change-log/unpinned-latest.html`; and
4. MAM-simple `py-examples/osis/osis_runner.py`.

The 12 SVGs record Graphviz 15.1.1 in the committed header and Graphviz 16.0.0 in
the regenerated header; geometry and dimensions change as well. That is new
finding `MP13-01`.

The other normalized changes are duplicate or superseded evidence rather than
new findings. The vendoring changes reproduce a known stale vendored copy and the
required scheduling relationship already recorded by Phase 12. The MAM-simple
support copy is refreshed by the earlier `mam-simple` step, exactly as Phase 12
finding `MP12-07` describes. The old change-log date accompanies the invalid
empty unpinned report already recorded by `MP02-01`.

The remaining 29 paths differ only in working bytes and line endings: 15 in
MAM-basics, one in MAM-parsed, 12 in MAM-with-doc, and one in MAM-simple. Git's
normalized diff does not enumerate them, but the exact SHA-256 snapshots do. That
is new finding `MP13-02`.

The second run changed no repository. Its post-state is exactly equal to the first
run's post-state for every fixed HEAD tree, every allowlisted output hash, every
unexpected status path, and every nonignored untracked path. No nondeterminism was
found after the first refresh.

## Full-suite verification

The final suite invoked the real top-level test entry point with the same 18
forest overrides:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py
```

Result: **971 passed, 5 skipped in 144.39 seconds**. The runner's full pre/post
content state is equal, and the outside-primary guard found no concurrent change
during the final suite.

## Finding-ledger reconstruction

Phase 13 read the exact archived task IDs for Phases 0–12, retained each task's
title verbatim, and treated the tracked Phase 10–12 reports as authoritative where
a task summary could differ. The reconstructed per-phase counts are:

| Phase | P1 | P2 | P3 | Total |
|---:|---:|---:|---:|---:|
| 0–9 | 10 | 48 | 14 | 72 |
| 10, private | 2 | 3 | 1 | 6 |
| 11 | 0 | 1 | 2 | 3 |
| 12 | 0 | 6 | 2 | 8 |
| Prior reconstructed total | 12 | 58 | 19 | 89 |
| 13 | 0 | 3 | 0 | 3 |
| Final total | 12 | 61 | 19 | 92 |

The source rows themselves prove the corrected split. No report records a
severity change that could produce the previously announced 15/33/41 split. The
public disposition companion assigns stable IDs to all 85 public findings and
states the aggregate count of the seven private findings. The canonical private
ledger contains all 92 findings, current status, disposition, dependencies, and
duplicate/root-cause relationships.

## Restoration, concurrency boundary, and acceptance state

All 45 exact changed paths were restored through a closed allowlist. The restore
refused dynamic dirty-path cleanup and would stop on any non-allowlisted path.
Ignored Phase 13 evidence remains under MAM-basics `.novc`; every useful result is
summarized in this report or the ledgers.

An independent session changed the primary MAM-private clone during both complete
pipeline runs. The Phase 13 runner detected the outside change, while the pinned
MAM-private forest head and every forest content hash remained fixed. No private
path or controlled-input detail is reproduced here; the private Phase 13 companion
records the audit evidence. The final suite observed no outside-primary change.

The review forest remains available read-only for acceptance and later handoff.
No review branch is merged, no remediation forest exists, and the forest is not
retired. After report commits, the local manifest is the authority for the exact
final report-branch heads; detached heads remain the literal hashes in the matrix
above.

The final private report-branch head is
`13a691f968c9782886e29094fac6611b95db8989`, pushed to
`origin/review/mega-pipeline-2026-09-01`. The final MAM-basics report-branch head
is the commit containing this report; its exact hash is recorded in the local
manifest after this report is committed.
