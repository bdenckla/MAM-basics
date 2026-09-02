# MAM mega-pipeline review, Phase 11: public site generation

Review date: 2026-09-01.

This report reviews only the `gen-site` `StepRecord` immediately after
`near-aleppo-census` in MAM-basics' `py/main_0_mega.py`. The reviewed step writes
MAM-basics' public `gh-pages/index.html` and `gh-pages/unicode-proposals.html`.
Phase 11 did not review or execute the following `vendoring-audit` step, did not
start Phase 12, and did not fix production code or generated output.

The governing forest was
`C:\Users\BenDe\Documents\Codex\ReviewForests\mam-mega-review-2026-09-01`.
The reviewed branch heads were MAM-basics
`6d0aef7b038520a9dea3c12369a614d6eae93115` and MAM-private
`3aa273676bdad84e7b78f59abf0a06eda94aa6e3`, both on
`review/mega-pipeline-2026-09-01`. The six detached dependency worktrees remained
at the commits in `review-manifest.json`: MAM-parsed `46209cdf`,
codex-index-aleppo `1c12a8e`, MAM-with-doc `999a437`, MAM-simple `cd2bef8`,
MAM-OSIS `2f783d1`, and MAM-for-Sefaria `cf19347`. All eight worktrees were clean
at the pre-write checkpoint. The manifest's MAM-private commit is the Phase 10
pre-report head; `3aa2736` is the later Phase 10 report commit and is the actual
Phase 11 baseline.

## Phase 11 outcome and cumulative tally

Phase 11 adds **three genuinely new findings: 0 P1, 1 P2, and 2 P3**. The accepted
tally through Phase 10 was 78 findings: 15 P1, 26 P2, and 37 P3. The cumulative
tally through Phase 11 is therefore **81 findings: 15 P1, 27 P2, and 39 P3**.

The two generated pages are sound at the reviewed commit. The exact registered
runner and the direct `py/main_authored.py gen-site` command each regenerated both
pages byte-identically. The final sizes and SHA-256 values were:

1. `gh-pages/index.html`: 4,484 bytes,
   `4114079d1b1ea63a7e6e3313ceb8cccc64114ed057337e902a7b484a2999edc1`;
2. `gh-pages/unicode-proposals.html`: 2,794 bytes,
   `d2f67e1ee5c9b381787e5c16c4720c34d6349bec9ad7c775cda127c7c68100cb`.

The exact `StepRecord` named `gen-site` was selected from `STEPS`, its runner was
asserted to be the registered `main_authored.gen_site` function, and the runner
was called without executing any neighboring step. The registration's preceding
ID was `near-aleppo-census` and its following ID was `vendoring-audit`. Both page
hashes were unchanged after the exact runner, after a direct generator run, and
after the final regeneration.

## Three new Phase 11 findings

1. **[P2] The two-page generation is not atomic, and its progress output conceals
   the page already replaced before a later writer fails.** `main_authored.py:122`
   constructs a tuple by calling `unicode_proposals.gen_html_file()` and then
   `site_index.gen_html_file()` before the `for` loop begins. Each individual page
   is replaced atomically through `mb_cmn.file_io.with_tmp_openw()` and
   `os.replace()` (`file_io.py:13-19, 38-43`), but no transaction or rollback spans
   both pages. A controlled `.novc` probe redirected the production writers into
   a fresh directory, allowed the real Unicode-proposals writer to finish, and
   made the landing-page writer raise `RuntimeError`. The command failed with the
   Unicode page present and the landing page absent. It also printed no
   `Generated ...` line: tuple evaluation had not reached the loop that reports
   completed paths. The mega-pipeline propagates the exception, but the failed
   step has already changed one of its two tracked outputs and its stdout does not
   identify that partial write.

2. **[P3] `gen-site` has no owned-output cleanup check, so a retired generated page
   can remain in the deployed `gh-pages` tree.** The two writers replace only their
   fixed current filenames. `main_authored.gen_site()` neither declares an owned
   output set nor checks for superseded filenames. A controlled `.novc` probe
   seeded `legacy-generated.html`, ran the real two-page generator successfully,
   and found all three files afterward: the two current pages and the seeded
   legacy page. This repository's Pages workflow deploys the committed
   `gh-pages` directory, so a tracked retired page would remain publicly reachable
   until removed explicitly. No retired root page owned by `gen-site` is present
   at the reviewed commit; the finding is the missing cleanup invariant, not a
   current stray page.

3. **[P3] The scheduling comment's source claim is incomplete even though its
   order-independence conclusion is correct.** `main_0_mega.py:392-397` says
   `gen-site` reads nothing but `py/author_site/site_data.py`'s authored entries.
   The landing page does read its authored entries from `site_data.py`, but the
   Unicode-proposals page also reads its nine proposals, legend, and notes from
   `_PROPOSALS`, `_LEGEND`, and `_NOTES` in
   `py/author_site/unicode_proposals.py:56-137`. The generator remains independent
   of earlier mega-generated artifacts: it completed with `REPOS_ROOT` set to a
   fresh empty directory, and both output hashes remained exact. The comment is
   wrong about which authored source files define the two outputs, not about the
   step's placement after `near-aleppo-census`.

## Registration, ordering, and dependency results

`main_0_mega.py:398-402` registers `gen-site` immediately after
`near-aleppo-census`, with `main_authored.gen_site` as its callable and a note
naming both output files. The exact-run probe confirmed all three facts from the
live `StepRecord`, rather than reproducing the call from the note.

The step has no sibling-repository input. Both writers use MAM-basics' own
`author_site` modules, `mb_cmn` HTML/provenance helpers, and the MAM-basics
`gh-pages` output directory. Setting `REPOS_ROOT` to a fresh empty directory did
not change path resolution, output bytes, stdout, stderr, or the zero exit status.
The pinned sibling worktrees therefore matter to link verification but not to
generation. No primary-clone content entered either page.

There is no internal concurrency: the Unicode-proposals writer completes before
the landing-page writer begins. That fixed sequence is deterministic on success,
but finding 1 is the consequence of the same sequence on failure. The current
placement after the census is safe because `gen-site` reads no census output and
the census reads neither site page. Finding 3 is the only scheduling-comment defect
found.

## Source-to-output and link-integrity results

The landing page carries all 28 authored entry anchors from `site_data.py`, in the
same section and entry order, with no missing or extra authored entry. The rendered
page has one additional deliberate anchor to this repository's README. The focused
`test_site_index_links.py` lint passed both tests: every landing-page link into
MAM-basics' own site names a tracked deployed file, and the two Misc titles still
match the `_TITLE` values in their generating modules.

Twelve landing-page links point into MAM-with-doc. Each of the twelve mapped target
files exists in the pinned MAM-with-doc worktree at `999a437`; no target was
resolved against a moving primary clone. The remaining authored external links
were compared with their source constants and spot-opened where the review browser
could retrieve them. The Unicode proposal PDFs, repository/release pages, and
published project pages that were retrievable led to the intended subjects.
Google Docs, OneDrive, and several direct GitHub Pages URLs could not all be given
a reliable HTTP verdict by that browser because of safe-navigation or cache
restrictions, so Phase 11 does not claim a complete network-status oracle for
authored external destinations.

The Unicode-proposals page carries all nine proposal entries and the exact 14
source-document anchors from `_PROPOSALS`, in source order. Its two internal note
links point to the exact IDs emitted from `_NOTES`; no fragment target is missing
and no ID is duplicated. Both pages have a doctype, `html lang="en"`, UTF-8 meta,
the shared `style.css` link, and no duplicate ID. The shared stylesheet exists and
is tracked.

The repository-wide HTML syntax-and-sanity checker still reports 202 issues, the
same known backlog measured by the earlier 2026-09-01 public review. None of those
202 diagnostics names `gh-pages/index.html` or
`gh-pages/unicode-proposals.html`; the orphan diagnostic remains the separately
settled `wlc/index.html`. Phase 11 therefore treats the two reviewed pages as clear
without describing the whole `gh-pages` tree as checker-clean.

## Output cleanup, reproducibility, and failure-boundary results

Successful regeneration is reproducible. The pre-write snapshot, exact registered
run, direct command, empty-`REPOS_ROOT` run, and final command all produced the same
two sizes and hashes. Git reported no diff in either generated page after every
production write. The controlled failure and cleanup probes wrote only under the
review forest's ignored `.novc`; the probes did not touch the tracked `gh-pages`
files.

Each individual output uses a temporary sibling and `os.replace()`, so a failure
during one page's own serialization does not leave that page half-written.
Finding 1 is the missing two-page transaction. Finding 2 is the absence of an
owned-output cleanup invariant. No concurrent writer, nondeterministic ordering,
sibling-path leak, current stale output, or unexplained generated diff was found.

## Reproduction commands and verification record

From the MAM-basics review worktree, the exact registered step was exercised by the
ignored Phase 11 probe with:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe .novc\phase11_probe.py registered exact_step
```

The prescribed direct generator was exercised with:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe py\main_authored.py gen-site
```

The focused landing-page lint was exercised with:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe .novc\phase11_probe.py tests py\tests\test_site_index_links.py -q
```

The complete MAM-basics suite was exercised with the review-forest dependencies
pinned where the forest contains them and clean primary clones supplied only for
the ten dependencies absent from the deliberately eight-repository forest:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe .novc\phase11_probe.py tests
```

The result was **971 passed and 5 skipped in 100.54 seconds**. The focused file had
already reported **2 passed**. The HTML checker was exercised with:

```powershell
C:\Users\BenDe\GitRepos\MAM-basics\.venv\Scripts\python.exe py\check_html_syntax_and_sanity.py gh-pages
```

The ignored probe also captured source/output inventories, the empty-`REPOS_ROOT`
run, the partial-failure boundary, and the cleanup boundary as JSON under
MAM-basics `.novc`. The final cross-phase checkpoint found every review worktree
clean before this report, retained Phase 10's 87 expected census files, and retained
their aggregate SHA-256
`e267f49ad6a1f944ecf1ce884f729179d58f88daea9b7899b5d9f29ef96f2435`.
The only tracked Phase 11 change is this public report. No production fix, fetch,
update, rebase, merge, worktree removal, or Phase 12 work occurred.
