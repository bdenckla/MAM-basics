# MAM mega-pipeline review: public finding disposition companion

Review closeout date: 2026-09-01.

This is the public companion to the canonical private disposition ledger. It
contains every public finding and public coverage statement, but no private
paths, controlled-input details, comparison-project details, or private finding
text.

## Reconciled public and private counts

The Phase 12 cumulative prose announced 89 findings as 15 P1, 33 P2, and 41 P3.
Reconstruction from the original labels preserves 89 findings but yields 12 P1,
58 P2, and 19 P3. `MP13-03` records and corrects the discrepancy.

Seven findings are private: the six Phase 10 findings and one private Phase 8
finding. Their aggregate is **2 P1, 4 P2, and 1 P3**. The prior public register
therefore contains 82 findings: 10 P1, 54 P2, and 18 P3. Phase 13 adds three
public P2 findings.

| Scope | P1 | P2 | P3 | Total |
|---|---:|---:|---:|---:|
| Public findings through Phase 12 | 10 | 54 | 18 | 82 |
| Private aggregate through Phase 12 | 2 | 4 | 1 | 7 |
| Prior total, reconstructed | 12 | 58 | 19 | 89 |
| Public Phase 13 findings | 0 | 3 | 0 | 3 |
| Final public companion | 10 | 57 | 18 | 85 |
| Final public plus private | 12 | 61 | 19 | 92 |

All findings below retain their original severity. **Open — queued** means the
finding remains present and belongs in a later remediation wave. **Already fixed
before Phase 13** means later remeasurement found a production fix that was
already an ancestor of the pinned Phase 13 baseline. **Fixed in remediation**
means the 2026-09-02 change-log fail-closed wave changed production code and
verified the result. **Fixed in closeout** applies only to the corrected tally in
`MP13-03`; it does not claim a production-code fix.

## Public finding index

### Phase 0 — `Review main_0_mega.py code`

- `MP00-01` **P2** — Five subprocess wrappers bypass repository-specific path
  overrides. Open — queued; repository-path root cause.

### Phase 1 — `Review main_0_mega phase 1`

- `MP01-01` **P1** — Missing books can leave stale MAM-parsed JSON. Open —
  queued; roster root cause.
- `MP01-02` **P2** — Two parse entry points omit `check_mpplus`. Open — queued;
  validation root cause.
- `MP01-03` **P2** — Parse JSON and support-file publication is not batch-atomic.
  Open — queued; atomicity root cause.
- `MP01-04` **P3** — MAM-parsed schema documentation names obsolete keys. Open
  — queued; documentation root cause.
- `MP01-05` **P3** — An accentuation comment speculates about conversion from
  paseq to legarmeh. Open — queued; terminology root cause.

### Phase 2 — `Review main_0_mega Phase 2`

- `MP02-01` **P1** — Diff extraction drops differently keyed and unmatched
  content; a published 0-change result corresponds to 175 normalized matches.
  Open — queued; oracle root cause.
- `MP02-02` **P1** — Git dependency failures formerly could become successful
  empty reports. Already fixed before Phase 13 by MAM-basics commit `b403e6d`
  (2026-08-31); remeasurement confirmed that `ls-tree`, `show`, `log`, and
  `rev-list` failures are fatal.
- `MP02-03` **P2** — Verification errors formerly did not stop JSON and HTML
  publication. Fixed in remediation by MAM-basics commit `db4298e` (2026-09-02);
  the caller raises before reading commit dates, creating output directories, or
  writing JSON and HTML.
- `MP02-04` **P2** — Long-document anchor IDs collide. Open — queued.
- `MP02-05` **P2** — Quick Brown records only the last qualifying category. Open
  — queued.
- `MP02-06` **P2** — Conditional FOI and big-document outputs are not removed
  when empty. Open — queued; stale-roster root cause.
- `MP02-07` **P2** — MAM-with-doc output sets publish incrementally. Open —
  queued; atomicity root cause.
- `MP02-08` **P3** — Reader-facing FOI output spells `legarmeh` as `legarmeih`.
  Open — queued; terminology root cause.

### Phase 3 — `Phase 3 — template-survey review`

- `MP03-01` **P2** — Verbose Wikitext changes positional parameters containing
  `=` into named parameters. Open — queued.
- `MP03-02` **P2** — Missing Graphviz silently preserves stale SVGs. Open —
  queued; external-tool error root cause.
- `MP03-03` **P2** — Obsolete column-versioned graph files are not removed. Open
  — queued; stale-roster root cause.
- `MP03-04` **P2** — Template-survey output publishes incrementally across two
  repositories. Open — queued; atomicity root cause.
- `MP03-05` **P3** — The toy survey omits Column D. Open — queued.
- `MP03-06` **P3** — Two survey return-value docstrings describe the wrong tuple.
  Open — queued.

### Phase 4 — `Phase 4 — MAM-simple output review`

- `MP04-01` **P1** — Relative output roots ignore repository overrides and can
  split one export across checkouts. Open — queued; path root cause.
- `MP04-02` **P2** — The mega omits five MAM-simple documentation/font artifacts.
  Open — queued; roster root cause.
- `MP04-03` **P2** — MAM-simple, support-copy, Sefaria/AJF, and OSIS publication
  is not batch-atomic. Open — queued.
- `MP04-04` **P2** — Phase 4 output rosters are not reconciled. Open — queued.
- `MP04-05` **P2** — Malformed Job XML destroys the prior small-letter report.
  Open — queued.
- `MP04-06` **P2** — The OSIS page publishes two stale counts. Open — queued.
- `MP04-07` **P2** — Sefaria/AJF prose calls stress helpers an extra accent. Open
  — queued; terminology root cause.
- `MP04-08` **P3** — The MAM-simple XML guide excludes an emitted empty element
  shape. Open — queued.
- `MP04-09` **P3** — Phase 4 reader-facing prose uses `legarmeih`. Open — queued.
- `MP04-10` **P3** — OSIS prose mischaracterizes MAM and the Aleppo Codex. Open —
  queued.

### Phase 5 — `Review main_0_mega.py Phase 5`

- `MP05-01` **P1** — Sigil inventory treats ordinary Hebrew letters as sigla.
  Open — queued.
- `MP05-02` **P2** — Five generators accept incomplete book coverage. Open —
  queued; roster root cause.
- `MP05-03` **P2** — Multimark publication is not batch-atomic. Open — queued.
- `MP05-04` **P2** — Explicit-ḥataf publication is not batch-atomic. Open —
  queued.
- `MP05-05` **P2** — Explicit-ḥataf annotations are not reconciled. Open —
  queued.
- `MP05-06` **P3** — The explicit-ḥataf numerical claim says 664 instead of 670.
  Open — queued.

### Phase 6 — `MAM-basics Phase 6 review`

- `MP06-01` **P1** — Correlated inputs can hide a missing Wikisource chapter.
  Open — queued; oracle root cause.
- `MP06-02` **P1** — A live bot failure can leave partial remote publication and
  stale local state. Open — queued; atomicity root cause.
- `MP06-03` **P2** — HTTP cache metadata and bodies update separately. Open —
  queued.
- `MP06-04` **P2** — Four Wikisource output families are neither batch-atomic nor
  roster-reconciled. Open — queued.
- `MP06-05` **P2** — The bot prototype retains stale warnings. Open — queued.
- `MP06-06` **P2** — Bot documentation describes the wrong validation mode. Open
  — queued.
- `MP06-07` **P3** — Generated Wikisource diff prose uses `legarmeih`. Open —
  queued.

### Phase 7 — `MAM-basics Phase 7 review`

- `MP07-01` **P2** — MAM-simple documentation cannot bootstrap an empty target.
  Open — queued.
- `MP07-02` **P2** — `gen-misc` neither owns nor validates required assets. Open
  — queued.
- `MP07-03` **P2** — The HTML validator crashes while reporting Hebrew paths on
  Windows. Open — queued.
- `MP07-04` **P2** — Phase 7 publication is incremental rather than batch-atomic.
  Open — queued.
- `MP07-05` **P2** — Retired HTML and orphan images lack an ownership manifest.
  Open — queued.
- `MP07-06` **P2** — The MAM-simple page's mid-verse petuḥah count is stale. Open
  — queued.
- `MP07-07` **P2** — `notes_on_aliyot.html` requests an undefined font class.
  Open — queued.
- `MP07-08` **P3** — Visible Decalogue strand names use romanized and positional
  labels. Open — queued.
- `MP07-09` **P3** — Four authored sources say poetic books instead of poetic
  verses. Open — queued.

### Phase 8 — `MAM-basics Phase 8 review`

- `MP08-01` **P1** — Maqaf changes are not applied to the grammar-test body. Open
  — queued.
- `MP08-02` **P1** — NFC hides eight current WLC/UXLC mark-order differences.
  Open — queued.
- `MP08-03` **P1** — The accent-change filter uses Unicode names instead of prose
  grammatical roles. Open — queued.
- `MP08-04` **P2** — Unsupported UXLC tokens silently become filler letters. Open
  — queued.
- `MP08-05` **P2** — The vendored destination tree is an undocumented file
  manifest. Open — queued.
- `MP08-06` **P2** — Phase 8 publication is not transactional. Open — queued.
- `MP08-07` **P2** — The WLC/UXLC comparison silently caps its report. Open —
  queued.
- `MP08-09` **P2** — The 4.20/4.22 pages are an unchecked manual mirror. Open —
  queued.
- `MP08-10` **P2** — WLC a-note 16 displays munax while naming merkha. Open —
  queued.
- `MP08-11` **P3** — Reader-facing WLC prose violates accentuation terminology
  rules. Open — queued.

One additional Phase 8 finding is private and appears only in the aggregate.

### Phase 9 — `Review MAM-basics Phase 9`

- `MP09-01` **P2** — Unknown PCFG productions receive implausibly high
  probability. Open — queued.
- `MP09-02` **P2** — Missing MAM-simple silently removes one dual-cantillation
  fold. Open — queued.
- `MP09-03` **P2** — Accgram output families retain stale files and lack a
  set-level transaction. Open — queued.
- `MP09-04` **P2** — Poetic comparison coverage shrinks silently. Open — queued.
- `MP09-05` **P2** — The servant cross-check counts ambiguous vertical-line
  patterns as legarmeh. Open — queued.
- `MP09-06` **P2** — Printed-Decalogue generation accepts incomplete committed
  input rosters. Open — queued.
- `MP09-07` **P2** — The printed-Decalogue baseline claim is not checked by the
  step. Open — queued.
- `MP09-08` **P2** — Redirected HTML generation reads two hard-coded default JSON
  paths. Open — queued.
- `MP09-09` **P3** — Accgram prose misstates source standing and terminology.
  Open — queued.

### Phase 10 — private near-Aleppo review

Six findings are private and appear only in the aggregate: 2 P1, 3 P2, and 1 P3.

### Phase 11 — public site generation review

- `MP11-01` **P2** — Two-page `gen-site` publication is not atomic and progress
  output hides the partial write. Open — queued.
- `MP11-02` **P3** — `gen-site` has no owned-output cleanup check. Open — queued.
- `MP11-03` **P3** — The scheduling comment omits an authored source module. Open
  — queued.

### Phase 12 — vendoring audit review

- `MP12-01` **P2** — Production vendoring bypasses repository-specific path
  overrides. Open — queued.
- `MP12-02` **P2** — Failed Git history becomes `no-commits` and audit success.
  Open — queued.
- `MP12-03` **P2** — Untracked Python files become production audit inputs. Open
  — queued.
- `MP12-04` **P2** — Relative policy paths are not checked for containment. Open
  — queued.
- `MP12-05` **P2** — Four vendoring outputs can be mixed or truncated after
  failure. Open — queued.
- `MP12-06` **P2** — A destination whose source disappeared drops out instead of
  becoming `MISSING-SRC`. Open — queued.
- `MP12-07` **P3** — The final-step comment incorrectly says no earlier step feeds
  the audit. Open — queued.
- `MP12-08` **P3** — Vendoring prose misstates both scope and output count. Open
  — queued.

### Phase 13 — whole-pipeline integration and closeout

- `MP13-01` **P2** — Unpinned Graphviz version drift rewrites all 12 generated
  call-graph SVGs. Open — queued; related to but distinct from missing-Graphviz
  finding `MP03-02`.
- `MP13-02` **P2** — A clean checkout's first mega run rewrites 29 tracked text
  artifacts only at the working-byte/line-ending level. Open — queued.
- `MP13-03` **P2** — The published cumulative severity split does not match the 89
  original labels. Fixed in closeout by this companion and the canonical ledger.

## Public coverage through Phase 13

The reconstructed public coverage includes orchestration and path resolution;
MAM-parsed generation; FOI and MAM-with-doc; template surveys; MAM-simple,
Sefaria/AJF, OSIS, and examples; Phase 5 inventories; Wikisource tooling;
authored-document generation; public WLC/UXLC ingestion and reports; the accgram
prose, poetic, dual-cantillation, printed-Decalogue, survey, and HTML families;
public site generation; vendoring; and the complete 42-step integration run.

Phase 13 expanded the forest to every runtime and test dependency, ran all 42
registered steps twice, compared generated bytes and immutable HEAD trees, ran
the full suite, and restored every review-only output. The second run changed no
watched byte. The full suite reported 971 passed and 5 skipped. The private
near-Aleppo implementation and private comparison finding are represented here
only by aggregate counts.
