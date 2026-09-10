# Revision-aware Wikisource chapter downloads

## Authorization, status, and development location

Ben's decisions, 2026-09-10: investigate and then implement revision-aware
Wikisource chapter downloads. Commit revision metadata beside downloaded text
so a fresh checkout can reuse unchanged chapters. The completed
[Wikisource-derived-products programme](PLAN-wikisource-derived-mam-products.md)
supplies the settled planner, downloader, parser, and product interfaces.

The programme has three sequential phases:

1. Investigate the current implementation and establish the measured baseline.
2. Implement revision checking, persistence, forced downloads, and bot integration;
   complete offline verification.
3. Verify the complete live corpus, measure the improvement, and seed committed
   metadata only from fetched content equal to the committed raw chapters.

Phase 1 is complete; its execution is recorded below. Phase 2 and Phase 3 remain
to be implemented. Live content differs from the baseline in 20 chapters, so
complete metadata seeding cannot silently refresh those chapters.
Each phase runs in a fresh task, commits its result locally, verifies clean status,
then creates its successor last. Keep one writer in the shared checkout. An open
predecessor task is expected; simultaneous staging or editing is not.

- Development checkout: `C:/Users/BenDe/.codex/worktrees/3a6b/MAM-basics`.
- Existing branch: `codex-worktree-3a6b`.
- Saved project: `ws-direct`, ID `3f065f8d-6225-4734-b84d-ec5d68aad18e`.
- Task creation uses that project with `environment.type = local`. The saved
  directory is already a worktree; do not allocate another worktree.
- Phase 1 task: `01a08d2c-5609-7f20-a3de-7ee5855af4ed`.
- Planning task: `01a08c66-c9fa-7a21-94f4-00934456e344`.
- Phase 1 starting commit: `7d0888b374c51c2c81aa5b461cbeabd15628d17b`.
  HEAD, main, and origin/main all named that commit at preflight.
- Primary clone: `C:/Users/BenDe/GitRepos/MAM-basics`.
- Shared interpreter: `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`.
  No `.venv`, junction, or symlink belongs in the worktree.
- Remaining sibling input: `C:/Users/BenDe/GitRepos/MAM-private`, measured at
  `55252b834d28a6c241e75758aff5d15836621f56`.

Before each phase's first edit, read:

1. `C:/Users/BenDe/.codex/AGENTS.md`.
2. `C:/Users/BenDe/.codex/worktrees/3a6b/MAM-basics/CLAUDE.md`.
3. `C:/Users/BenDe/.codex/worktrees/3a6b/MAM-basics/doc/agent-planning-principles.md`.
4. `C:/Users/BenDe/.agents/skills/hebrew-prose/SKILL.md` before prose about
   Hebrew accentuation.

No repository `AGENTS.md` exists at the baseline. Verify `git rev-parse
--show-toplevel`, `git rev-parse HEAD`, `git branch --show-current`, `git status
--porcelain`, and the required handoff commit's ancestry. Recheck the exact
checkout when analysis becomes implementation. Preserve an unexpected commit or
dirty file and establish its origin before editing. The successor prompt must
name the preceding phase's actual commit; the baseline above is not a substitute.

Every command, source edit, generator, staging operation, and commit runs in the
development checkout. The primary clone supplies only the interpreter until
archival integration. Set `REPOS_ROOT=C:/Users/BenDe/GitRepos` for the suite's
remaining private input. A sandbox ownership error can be handled with an exact,
command-local Git `safe.directory` setting. Do not alter global Git configuration.

## Required behavior

1. Check current chapter revision IDs before fetching reusable chapter text.
   Use `action=query&prop=info` with `redirects=1` and read `lastrevid`.
2. Flatten selected requested titles across book boundaries for metadata checks,
   using at most 50 titles per request. Resolve normalization and redirects on
   every check; preserve requested titles separately from resolved titles.
3. Reuse only when requested title, resolved page identity, current revision ID,
   and the hash of the existing local chapter all agree with valid metadata.
   A stored hash is not proof that the local text still has that hash: recompute it.
4. Fetch changed chapters by the exact revision IDs returned by the check, using
   `prop=revisions`, `revids`, `rvprop=ids|content`, and `rvslots=main`. Verify the
   returned revision and page identity. Never pair later title-fetched text with
   an earlier `lastrevid`.
5. When trustworthy metadata is absent, fetch selected content directly by title
   with `rvprop=ids|content` and `redirects=1`. Avoid a preliminary full metadata
   pass over uncached chapters. Use the revision ID returned with the text.
6. Preserve serial requests, compression, throttling, timeouts, retries, the
   existing 20-chapter content batch size, selectors, complete-book prerequisites
   for partial downloads, and post-download hooks. Metadata batching may cross
   books; content batching remains bounded by the established limit.
7. Store one tracked file, `in/mam-ws-revisions.json`, outside `in/mam-ws/`.
   Include schema version and endpoint. Index records by existing book39 ID and
   Hebrew chapter ID. Each record contains requested title, resolved title,
   page ID, revision ID, and SHA-256 of the local chapter line array serialized
   as `json.dumps(lines, ensure_ascii=False, separators=(",", ":"))` encoded as
   UTF-8. Do not normalize, strip, or change strings. Hashing includes line order
   and empty lines, with no trailing serialization newline.
8. Store no routine check timestamps. Repeated unchanged runs must have no
   tracked diff. Avoid rewriting a book whose contents are unchanged.
9. Missing, malformed, unsupported, or mismatched metadata cannot authorize
   reuse. Report the condition and fetch selected content. Validate types and
   schema, including positive page/revision IDs and a valid digest. Do not let
   Python booleans pass as integer IDs.
10. Validate a complete book, atomically write the book, then atomically update
    metadata for that book. An interruption must leave matching metadata or a
    detectable mismatch that forces fetching next time. Never commit metadata
    ahead of its content. Preserve unselected chapter content and valid metadata
    records; do not use a partial selection to erase unrelated records.
11. Add `--force-download` to `main_download.py fr-wikisource` and a corresponding
    keyword argument to `download_wikisource.run`. Forced downloads bypass reuse
    and refresh metadata from returned content revisions.
12. Make `ws_bot_real._download_modified_chapters` force-download the chapters
    modified by the bot. Preserve the empty-modification early return and bot
    modes that suppress post-download work.
13. Always run the existing parsing/product hook for selected affected books,
    including a run that reuses every selected chapter. The settled hook writes
    format 2, complete affected 24-book plain/plus groups, support files, and
    documentation, and validates plus products.
14. Pass `allow_cache=False` for chapter metadata and content requests. Leave
    the generic `mb_cmn.polite_download` cache implementation unchanged.
15. Report selected, reused, and fetched chapter counts, metadata/content/total
    request counts, and elapsed download time, separately from parsing. Make
    API errors, missing pages, duplicate identities, incomplete responses, and
    inaccessible revision content fail visibly. Count actual attempts when
    reporting transport requests; do not label planned batches as attempts.
16. Seed metadata only when the fetched revision and locally written content
    agree. During migration, commit metadata only for live fetched content that
    exactly equals the committed chapter. Report upstream differences; do not
    silently refresh production data to make seeding possible.

The freshness claim covers downloaded raw chapter wikitext. Template edits may
change rendered pages without changing chapter revisions, and chapter checks do
not establish one simultaneous whole-corpus snapshot. Every selected chapter
gets a live revision check or a direct content retrieval on every run. Do not
add age-based freshness, recent-changes checkpoints, concurrency, or unrelated
HTTP-cache repairs. Keep introduction downloads, Google behavior, published
URLs, product schemas, raw file format, ordering, and Hebrew bytes unchanged.

## Current implementation and API findings

The following anchors were inspected at the Phase 1 starting commit:

| File / anchor | Contract to preserve or extend |
| --- | --- |
| `py/py_misc/get_wikisource_plan.py:get_book_plans`, `get_chapter_plans` | Plans come from book metadata and `ws_chapter_counts`, without reading Google or prior downloads. Titles contain underscores. |
| `py/ws/ws_download_selector.py:selected_book_plans` | All books, book39, section6, one chapter, or JSON book/chapter pairs. JSON grouping deduplicates chapters and preserves book encounter order; chapter order follows the full plan. |
| `py/subcommands/download_wikisource.py:_chapter_plan_batches` | Content is fetched in groups of at most 20, restarted for each book. |
| `download_wikisource.py:_chapter_lines_from_response_json`, `_alias_to_requested_title` | Resolves normalized/redirected titles, rejects missing/duplicate/incomplete title results, and uses `content.splitlines()` unchanged. Extend validation to revision and page IDs. |
| `download_wikisource.py:_merge_book_contents` | A partial selection requires an existing complete book. Reconstructs canonical full-book chapter order. Validate before committing new content. |
| `download_wikisource.py:_write_book` | Already uses `file_io.json_dump_to_file_path`, which writes a temporary file then calls `os.replace` with Windows permission retries. Add equality avoidance and metadata sequencing around the existing atomic mechanism. |
| `download_wikisource.py:run`, `run_from_args` | One downloader session, then `parse_ws.almost_main(wsds.affected_bkids(book_plans))`. No force argument or revision persistence exists. |
| `py/subcommands/parse_ws.py:almost_main` | Writes selected format-2 books and calls `parse_ws_products.generate_production`. |
| `py/subcommands/parse_ws_products.py:generate`, `generate_production` | Reloads all source sub-books in each affected book24 group, writes plain/plus, validates plus, copies support files, and generates documentation. |
| `py/subcommands/ws_bot_real.py:_download_modified_chapters` | Calls `download_wikisource.run(modified_book_plans)` after successful edits. Add the force keyword here. |
| `py/mb_cmn/polite_download.py:get_json`, `_request` | `allow_cache=False` already bypasses generic cache reads and writes. Conditional requests require returned ETag or Last-Modified. Cache presence alone never skips the network. |

The downloader's existing configuration is a 30-second timeout, four maximum
attempts, retry statuses 408/429/500/502/503/504, exponential backoff starting at
one second and capped at 30 seconds, `maxlag=1`, and a per-host request-start
delay with a 1.5-second minimum and 3-second mean. Preserve its informative
`Denckla-Dowload-MAM-Bot/1.1` User-Agent and contact URL. API-level errors inside
HTTP 200 responses currently fail assertions rather than receiving HTTP retries;
do not mistake the HTTP retry policy for retrying every API error.

MediaWiki documents the 50-title limit in
[API:Query](https://www.mediawiki.org/wiki/API:Query), `lastrevid` in
[API:Info](https://www.mediawiki.org/wiki/API:Info)
and exact revision retrieval plus `rvprop=ids` in
[API:Revisions](https://www.mediawiki.org/wiki/API:Revisions). Its
[API etiquette](https://www.mediawiki.org/wiki/API:Etiquette) calls for serial,
batched, compressed requests with a descriptive User-Agent and `maxlag` for
noninteractive work. Live checks and their limits are recorded below; documentation
alone does not establish the local baseline.

## Phase 1 measurements and verification

Measured on 2026-09-10 at the starting commit and private input commit above.
The compact durable receipt is
[efficient-wikisource-downloads-phase1-validation.json](efficient-wikisource-downloads-phase1-validation.json).
Every figure below can be re-established with the scratch commands and methods
in this section; remeasure against the executor's actual commits and treat any
mismatch as a finding.

The planner and committed raw book keys agree in order across 39 books and 929
chapters. The raw book files total 10,312,149 bytes. Per-book 20-title content
batching requires 70 requests; flattening metadata into batches of 50 requires
19 requests. Per-book coverage and hashes are in the receipt.

The successful live measurement ended at `2026-09-10T21:28:55Z`:

| Operation | HTTP requests | Compressed body bytes | Decoded body bytes | Wall seconds |
| --- | ---: | ---: | ---: | ---: |
| Current full-content downloader, scratch destination | 70 | 2,051,127 | 10,330,082 | 204.20 |
| Repeat the first 20-title content batch with a populated cache | 1 | 46,094 | 242,128 | 2.49 |
| All chapter metadata, 50 titles per request across books | 19 | 24,940 | 299,641 | 53.81 |
| Exact content revisions for a 20-chapter subset | 1 | 46,177 | 240,937 | 4.09 |

All successful responses above were HTTP 200 and gzip-compressed. They supplied
`Cache-Control: private, must-revalidate, max-age=0`, no ETag, and no Last-Modified.
The warm-cache request sent no conditional validator and downloaded the whole
body again. The metadata check used 72.9% fewer requests and 98.8% fewer compressed
body bytes than the measured full-content request set. These are measurements
of API operations, not a completed incremental implementation or a promised
production speedup. Phase 3 must measure the implemented unchanged and forced
paths independently.

The measuring session read raw response-body bytes before decompression; byte
counts exclude HTTP headers, TLS, and chunk framing. It kept the existing
User-Agent, timeout, random throttle, retries, and `maxlag=1`, with serial
`Accept-Encoding: gzip, deflate` requests. The content run called the unchanged
`_download_book` into scratch, with an initially empty generic HTTP cache.
Timing includes throttling, JSON handling, scratch recording, book writing, and
comparison overhead, and excludes parsing/products. Request groups shared a
downloader, so a group's wall time can include its initial inter-request delay.
The separately run production parse in the local mega took 17.08 seconds,
including process/import overhead.

The first measurement attempt failed visibly on request 63, for Esther, after
62 successful content requests. Wikisource returned HTTP 200 with API error
`maxlag` and reported lag `1.000879` seconds. The existing downloader asserted
because the response had no query object. Evidence remains in the original
scratch directory; the full repetition used the same policy and a fresh scratch
cache. Do not count the interrupted attempt as a successful full download or
quietly change `maxlag` to avoid recording the failure.

The live metadata checks returned all 929 distinct page identities and positive
revision IDs. Every requested underscore title had a normalization mapping;
none of the corpus titles redirected. No continuation, warning, missing page,
or duplicate identity appeared in the successful corpus checks. Separate probes
confirmed the behaviors absent from that corpus result:

1. A direct 20-title `rvprop=ids|content` response paired IDs with content, and all
   20 returned chapter arrays matched committed data.
2. An exact-revision 20-chapter response matched the checked page/revision IDs
   and previously fetched chapter arrays.
3. A historical exact-revision request for page ID `235906` returned requested
   revision `2907537`, while the preceding latest-content response named
   `2987209`. The request retrieved the historical revision, not the latest one.
4. A bounded redirect discovery followed by `prop=info&redirects=1` returned
   six real redirect mappings, six title normalizations, six resolved pages,
   and no missing pages. Those pages are outside the selected MAM corpus.

The full-content comparison found 909 equal chapter arrays and 20 different
chapter arrays. Twenty-eight raw book files are byte-identical to their live
scratch downloads. The differing chapters are:

| No. | Book39 | Chapter | Changed raw line numbers, one-based |
| ---: | --- | ---: | --- |
| 1 | Genesis | 43 | 32 |
| 2 | Deuter | 28 | 36 |
| 3 | Deuter | 32 | 48 |
| 4 | Joshua | 19 | 13 |
| 5 | Judges | 10 | 19 |
| 6 | 1Samuel | 1 | 10 |
| 7 | 1Samuel | 22 | 27 |
| 8 | 2Kings | 6 | 28 |
| 9 | 2Kings | 17 | 21 |
| 10 | Isaiah | 22 | 9 |
| 11 | Isaiah | 24 | 23 |
| 12 | Isaiah | 42 | 32 |
| 13 | Isaiah | 50 | 12 |
| 14 | Tsefaniah | 3 | 18 |
| 15 | Psalms | 4 | 8 |
| 16 | Psalms | 71 | 14 |
| 17 | Psalms | 84 | 9 |
| 18 | Daniel | 3 | 10 |
| 19 | 2Chronicles | 26 | 20 |
| 20 | 2Chronicles | 28 | 25, 29 |

The receipt stores exact inserted/deleted characters as JSON escapes, local and
live chapter hashes, and line locations. Full contexts remain in scratch
`upstream-differences.json`; source strings were never normalized. Phase 1
makes no editorial judgment about those changes. The fetched books and later
info response are separate observations: the baseline content request used
`rvprop=content` without IDs, so those later info IDs must not seed metadata
for the earlier content. Phase 3 must retrieve paired revision IDs/content and
recheck equality before committing any metadata. Leave unequal chapters out
of any claimed complete seed until a separate production-update decision or
a fresh equal retrieval resolves the mismatch.

The required full suite returned zero: **990 passed, 5 skipped, and 65 subtests
passed in 108.33 seconds** (109.49 seconds including the wrapper). The five skips
remain the existing semantic controls in `py/tests/test_edition_transcriptions.py`,
anchor `test_the_synthesized_mark_body_reproduces_the_scanner_on_an_agreeing_page`:
`koren_ex_elyon`,
`simtan_dt_taxton`, `simtiq_dt_taxton`, `simtiq_ex_elyon`, and `simtiq_ex_taxton`.
No missing-input skip was accepted.

Every maintained local mega step ran in order: 38 completed successfully, with
only the private writer `near-aleppo-census` omitted. The driver took 295.68
seconds. The durable receipt contains the actual ordered steps, return codes,
timings, and protected-tree hashes. The separate documentation, diagrams,
Google parse, and WS/Google comparison commands also returned zero. Documentation
verification reported 79 passed, zero failed, and the existing pending claim
`mp.plain.docs.book39-skeleton.common`. Both comparator outputs remain empty arrays.

Generated artifacts were synchronized except for these measured, preserved
vendoring-report differences:

1. `out/vendoring_compare_out.txt`: 24 `eol-only` entries became `identical`;
   all 44 support copies are byte-identical to source in the measured checkout.
2. `doc/vendoring-inventory.md`: the same classification changes merged the
   inventory's eight grouped rows into four. No source-content difference appeared.

Those reports describe on-disk line endings. The generated versions were saved
under `.novc/ws-efficiency-phase1-20260910/preserved-generated/`, hash-verified,
then their committed versions restored. The programme does not repair the
unrelated vendoring audit or include report churn in Phase 1. Future local
mega runs may reproduce the same report differences; identify them explicitly.
All other tracked generation output stayed unchanged. Raw Google, raw
Wikisource, bot captures, and historical input tree hashes stayed unchanged.
Production downloader source, raw chapters, metadata storage, and primary-clone
files were not changed by Phase 1.

### Reproducing Phase 1

All commands below run from the exact development checkout. The measurement
driver sets `REPOS_ROOT`, the exact Git safe-directory exception for subprocesses,
UTF-8 logging, and the working directory. The shared interpreter required approved
elevated execution because the sandbox could not launch it. No global configuration
was changed.

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_efficiency_phase1_20260910.py inventory
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_efficiency_phase1_20260910.py run baseline-suite py/main_test.py -q -p no:cacheprovider
```

The interrupted attempt used the default scratch directory:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_efficiency_phase1_20260910.py live
```

The successful attempt used a fresh scratch directory:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_efficiency_phase1_20260910.py run live-retry .novc/ws_efficiency_phase1_20260910.py live ws-efficiency-phase1-20260910-retry
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_efficiency_phase1_20260910.py run api-probes .novc/ws_efficiency_api_probes_20260910.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_efficiency_phase1_20260910.py run local-mega .novc/ws_products_phase5_mega_20260910.py --run-label ws-efficiency-phase1-mega
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_efficiency_extras_20260910.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_efficiency_upstream_diff_20260910.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_efficiency_receipt_20260910.py
```

Raw responses, request headers/parameters, full logs, captured books, and detailed
diffs are gitignored under `.novc/ws-efficiency-phase1-20260910/` and
`.novc/ws-efficiency-phase1-20260910-retry/`. The local mega's detailed logs are
under `.novc/ws-products-baseline-20260910/ws-efficiency-phase1-mega/`.
Scratch source hashes are in the receipt. The live scripts intentionally refuse
to overwrite a request capture; choose a fresh task-specific output name when
repeating and adjust the probe/receipt paths. Do not erase the baseline evidence.
The one-use `ws_efficiency_preserve_reports_20260910.py` verifies baseline HEAD
and generated hashes before preserving/restoring its two paths; reconstruct
that narrow check for a newer baseline rather than weakening its assertions.

If scratch tools are absent, reconstruct the same bounded measurement: enumerate
current ordered plans against committed raw keys; call the current downloader
into a separate directory through one measured polite session; capture compressed
bodies before decoding; repeat a populated-cache request; check all titles in
50-title metadata batches; retrieve the measured exact-revision subset and a
historical revision; compare all raw arrays without normalization; run the
maintained local generators and full suite. Do not infer new measurements from
the old receipt.

Phase 1 wrote no tracked Python and added no tests. Black formatted the six new
scratch scripts. The staged plan and receipt passed the prose/Unicode lints:
7 passed in 20.27 seconds. `git diff --cached --check` also passed. The exact
lint command is recorded in the receipt. After the plan and receipt are committed locally,
the next task owns Phase 2 only. The unresolved live-text differences constrain
Phase 3 seeding; they do not prevent offline Phase 2 implementation.

## Phase 2: implement and verify offline

Implement the required behavior above using focused modules for metadata and
revision retrieval where useful; keep the existing downloader's orchestration
small. Decide serialization field names once and document the versioned schema.
Materialize selected plans before reusing them for downloads and post-download
hooks. Flattening metadata requests must not key chapters solely by Hebrew
chapter ID: chapter IDs repeat in different books.

Response validation must account for normalization chains, redirect chains, and
multiple requested titles converging on one identity. Do not silently overwrite
entries in a dictionary. Bind exact-revision responses by revision ID and page
ID, since API page order is independent of requested chapter order. If a page
is moved or a revision becomes unavailable after checking, fail or explicitly
recheck before accepting content; never invent a successful match.

Use corpus-wide offline differential checks against frozen live response bodies
or a second independent derivation, plus scratch fault injection. Phase 1's
content responses lack revision IDs; do not fabricate IDs for committed metadata
from those responses or combine them with later info responses. Synthetic IDs
are acceptable only inside clearly labelled offline fault-injection fixtures.

Verify this complete matrix and record actual results:

| Condition | Required result |
| --- | --- |
| Unchanged remote revisions | Every selected chapter reused after a live check; no content fetch or tracked diff; normal hook runs. |
| Changed remote revisions | Only changed selected chapters fetched, by checked IDs; exact content and metadata agree. |
| Locally modified chapter or mismatched hash/title/page/revision | No reuse of the affected chapter. |
| Missing, malformed, unsupported, wrong-endpoint metadata | Visible report and direct fetching; no metadata-only pass over an entirely uncached selection. |
| First download without books or metadata | Full selection succeeds directly from title content responses carrying IDs. |
| Fresh-checkout reuse | Committed books and metadata suffice; generic HTTP cache absent. |
| Forced download | Every selected chapter fetched directly and metadata refreshed; no reuse. |
| Partial selectors | All selector forms preserve ordering, complete-book prerequisites, unselected content/metadata, and complete affected product groups. |
| Normalized and redirected titles | Requested/resolved titles and identities tracked separately and checked again. |
| Missing pages, duplicate identities, API errors, incomplete responses | Visible failure before accepting an invalid book/metadata pair. |
| Interruption after book replacement and before metadata replacement | Next run detects mismatch and fetches; no stale metadata authorizes changed local content. |
| Exact-revision race | A later title revision cannot be paired with an earlier checked revision. |
| Bot refresh | Modified chapters receive force mode; existing no-save/identity/no-post-download behavior remains. |

Do not add hand-picked example tests. Existing downloader tests may require
minimal interface/fixture updates for required revision IDs and the force keyword;
do not retain an obsolete production API solely to satisfy a mock. Existing bot
payload checks remain permitted under repository instructions. Missing corpus
inputs must fail. Never add `sys.path` manipulation to tracked code or tests.

Run Black at defaults on only changed Python files, regenerate affected tracked
products through the real commands below, inspect all diffs, and run the full
suite. Write results and remaining Phase 3 work into this plan, commit locally,
verify clean status, then create Phase 3 in `ws-direct` with a local environment
and the actual handoff commit. Stop editing after dispatch.

## Phase 3: complete-corpus equality and performance

Freeze current revision IDs for every selected chapter through live checks or
direct content responses. Compare incremental retrieval with an independent full
content retrieval of those same exact revision IDs across the entire corpus.
Independence means a separate full retrieval/derivation, not rereading the
incremental result under another name. Compare chapter line arrays, raw book
serialization, and all regenerated products; unexplained differences fail.

Measure an unchanged repeat separately from parsing, and compare against a
forced full download. Record request attempts and logical batches separately if
retries occur. Count compressed response-body bytes before decompression; do not
label decoded `response.content` bytes as network bytes. Report request reduction,
bandwidth reduction, and elapsed-time change separately. Preserve the normal
random throttle and report each run's scope and conditions; Phase 1 timings are
single-run observations, not a promised fixed speedup.

Seed `in/mam-ws-revisions.json` only after every relevant live fetched chapter
exactly equals its committed raw chapter. Do not copy Phase 1's later info IDs
onto earlier content. If upstream text differs, retain the fetched text in
scratch and report the book/chapter and exact difference; production updates
need a separate decision. The implementation can still finish without pretending
unequal data has trustworthy metadata.

Run the complete local regeneration scope below, inspect all generated diffs,
run the full suite, Black changed Python, finish this execution record, and
commit. Phase 3 creates no successor. Integrate only under the archival procedure.

## Regeneration, suite, and handoff commands

Run from `C:/Users/BenDe/.codex/worktrees/3a6b/MAM-basics`:

```powershell
$env:REPOS_ROOT="C:/Users/BenDe/GitRepos"
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider
```

The direct production hook's real command is:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_parse.py ws
```

An independent candidate writes outside production:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_parse.py ws-products --output-dir .novc/ws-efficiency-candidate
```

For complete local regeneration, reuse the existing scratch driver over maintained
`main_0_mega._STEPS`, with a new run label for each phase:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_products_phase5_mega_20260910.py --run-label ws-efficiency-phase3-mega
```

The driver runs every local step in order and omits only `near-aleppo-census`.
That omitted step writes into the private primary clone and is outside this
programme. If the scratch driver is missing, reconstruct its narrow operation
from `main_0_mega._STEPS`, recording the actual step list, return codes, and
before/after hashes. Do not run the unfiltered mega in a secondary worktree.
The standalone export commands are `py/main_mam_with_doc.py`,
`py/main_mam_simple.py`, `py/main_mam4sef.py --both-sef-and-ajf`, and
`py/main_mam_osis.py`; the local mega includes those generators.

Run separately where the mega invokes only a core generator or omits an explicit
comparison workflow:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_mam_simple.py doc-only
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_authored.py gen-mam-parsed-docs
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_pipeline_graph.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_parse.py go
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py wsgo
```

These Google commands parse committed input and compare locally; no Sheet writes
or downloads are required. Google product files must remain unchanged.

Before each commit, verify HEAD has not moved since the phase started and status
contains only that phase's paths. Stage explicit paths, run `git diff --cached
--check`, and commit with a task-specific message file and Codex attribution.
Recheck clean status. Do not push the worktree branch or merge merely to hand off.

Create the next task last, after verification and the local commit. Inspect
`list_projects`, use the verified `ws-direct` project with `environment.type =
local`, and pass the absolute checkout, branch, actual required commit, phase
scope, this plan, and archival responsibility. Verify the returned actual task
ID with `read_thread`; a provisional `clientThreadId` is pending setup, not a
substitute task ID. Wait for startup verification, then leave writing to the
successor. Use the user's configured default model unless Ben specifies a model
for this programme.

When Ben requests archival, serialize the writer with any active successor.
Once both trees are clean: merge main into the worktree branch, run the full
suite on the merged tree in the worktree, fast-forward primary main to the
verified branch, then push main. If main advances and `--ff-only` refuses,
repeat the worktree merge and verification. Never resolve conflicts or edit
source in the primary clone. Do not archive tasks, remove worktrees, delete
branches, rewrite history, or discard work automatically.
