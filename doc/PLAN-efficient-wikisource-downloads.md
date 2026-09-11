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

All three phases are complete. Phase 3 verified all 929 chapter arrays,
all 39 raw serializations, and 628 regenerated product files against an
independent retrieval of the same exact revisions. Metadata is seeded for
909 chapters. The 20 unequal chapters retain their committed raw text and
have no seeded record; a production refresh remains a separate decision.
Each phase runs in a fresh task, commits its result locally, and verifies clean
status. Phases 1 and 2 create their successors last; Phase 3 creates none.
Keep one writer in the shared checkout. An open
predecessor task is expected; simultaneous staging or editing is not.

Correction recorded by a Claude session on 2026-09-11, for finding 6 of the 2026-09-10 review:
the production refresh that the paragraph above calls a separate decision has been made and
carried out. `209b4c05` (2026-09-10 20:53) downloaded the 20 unequal chapters, and
`in/mam-ws-revisions.json` has held 929 records, one per chapter, since then. The section
"Production refresh of the 20 chapters, 2026-09-10" below records what the refresh changed. The
paragraph above stays as the record of Phase 3's result.

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

### Phase 2 execution record (2026-09-10)

The implementation ran in task `01a08d41-612e-7aa3-9312-2eecd9e9b881`, in the
verified checkout and branch above, starting from Phase 1 commit
`0beade0bac7794437dd35e5d54d95802f08c874e`. The private input remained at
`55252b834d28a6c241e75758aff5d15836621f56`.

The implementation has these module boundaries:

1. `py/ws/ws_revision_metadata.py` validates and persists schema version 1.
   Its top-level fields are `schema_version`, `endpoint`, and `books`.
   `books[book39][chapter]` contains `requested_title`, `resolved_title`,
   `page_id`, `revision_id`, and `sha256`. Digests follow Required behavior 7.
   Duplicate JSON keys invalidate the manifest; invalid individual records
   cannot authorize reuse, while valid unselected records survive.
2. `py/ws/ws_revision_api.py` validates title normalization and redirect chains,
   unique page/revision identities within and across batches, complete responses,
   and accessible exact revision content. `CountingSession.request` counts
   actual transport attempts; `ChapterClient` counts logical batches separately.
   Every chapter request passes `allow_cache=False`.
3. `py/ws/ws_chapter_download.py` checks reusable titles across books in batches
   of 50, retrieves direct or checked-revision content in per-book batches of
   20, validates complete books, and writes changed books before metadata.
   Equality avoids book replacement; metadata serialization has no timestamps.
4. `py/subcommands/download_wikisource.py:run` materializes selections, reports
   download counts/time before parsing, and always invokes the affected-book
   production hook. `main_download.py fr-wikisource --force-download` and
   `run(..., force_download=True)` bypass reuse. The bot's modified-chapter
   refresh passes that keyword; its suppression modes remain unchanged.

`in/mam-ws-revisions.json` is tracked with the version and endpoint but an empty
`books` object. No production chapter was downloaded or seeded in Phase 2.
An empty manifest makes the first actual download use direct content retrieval;
fresh-checkout reuse becomes available for records seeded in Phase 3 or written
by a later download. No synthetic identity appears in tracked metadata.
The generic HTTP downloader, introduction downloads, raw chapter arrays,
selectors, product schemas, and published URLs have no implementation changes.

Offline verification is recorded in
`doc/efficient-wikisource-downloads-phase2-validation.json`. The main matrix ran
51 checks across all 39 books and 929 chapters. Synthetic IDs were attached only
inside explicitly labelled offline response fixtures; frozen Phase 1 text and
the independent Phase 1 book files supplied the content/serialization oracle.
Real captured paired-content responses, exact-revision responses, and redirects
were also replayed without adding IDs to them.

| Verified condition | Observed result |
| --- | --- |
| Initial corpus retrieval | 929 fetched, 70 content attempts, no metadata pass; all 39 serialized books byte-identical to independently downloaded Phase 1 books. |
| Unchanged repeat and fresh-checkout fixture | 929 reused, 19 metadata attempts, zero content attempts; bytes and modification times unchanged. Metadata batches crossed book boundaries. |
| Forced corpus | 929 fetched in 70 content attempts, no metadata pass; unchanged books and manifest were not rewritten. |
| Changed remote revisions | Every 37th corpus chapter was changed: 26 fetched by checked IDs, 903 reused. Independent content and manifest comparison passed. |
| Local modifications and record corruption | Full-corpus sweeps of local edits, hashes, requested/resolved titles, page/revision IDs, invalid digests, and boolean IDs prevented incorrect reuse. |
| Unusable manifest | Missing, malformed, unsupported, wrong-endpoint, and boolean-version manifests caused direct retrieval with no metadata pass. |
| Selectors and preservation | All-book, book39, section6, chapter, and JSON selectors passed reuse and force paths; full corpus content/metadata survived partial selection. Missing/incomplete/invalid partial books failed before network access. |
| Title resolution | Reversed normalization and redirect chains worked across the entire corpus; converging titles and duplicate identities across batches failed visibly. |
| Response failures | Missing pages, duplicate pages, incomplete responses, HTTP-200 maxlag errors, warnings, continuation, invalid IDs, cyclic aliases, moved pages, wrong exact revisions, and unavailable content failed without accepting the affected book. |
| Interruption | A fault after book replacement and before metadata replacement left old metadata. The next run detected the local hash mismatch and fetched directly. |
| Revision race | Changed chapters used `revids`; a later title value could not satisfy the earlier checked revision. |
| Attempts versus batches | An injected timeout and HTTP 503 retry produced 21 metadata attempts for 19 logical batches. The transport policy was unchanged; only sleeps were suppressed for offline replay. |
| Bot and CLI | Force-mode forwarding, empty modified lists, no-save, identity mode, no-post-download, and CLI wiring passed without wiki writes. |

The additional verification script passed 9 checks. A mixed Genesis selection
reused 48 chapters, fetched one directly after rejecting its invalid record, and
fetched one by checked revision ID, preserving every unselected book. Direct
response faults also covered hidden-content flags, multiple revisions, boolean
revision IDs, duplicate page IDs, and `badrevids`.

The real production hook ran after an entirely reused partial selection in
`2Samuel`, `Joel`, `Ezra`, and `2Chronicles`. It regenerated and validated the
complete affected book24 products:

1. Samuel, including both source sub-books.
2. The Twelve, including all source sub-books.
3. Ezra-Nehemiah, including both source sub-books.
4. Chronicles, including both source sub-books.

All resulting raw/format-2/plain/plus/Google/protected JSON bytes remained
unchanged. Documentation verification reported 79 passed, zero failed, and
the existing pending claim `mp.plain.docs.book39-skeleton.common`.
The existing downloader fixture file was adapted to the production interfaces;
no tracked test cases or path configuration were added.

Reproduce the matrix from the development checkout with a new scratch label
on each run (the scripts preserve earlier case directories):

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_efficiency_phase2_offline_20260910.py offline-recheck
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/ws_efficiency_phase2_hooks_20260910.py hooks-recheck
```

The measured labels were `offline-2` and `hooks`; the first matrix invocation
stopped at a scratch-script syntax error before execution. The initial adapted
fixture run exposed a progress-message `Path`/string mismatch, corrected before
the corpus matrix. Final command logs live under
`.novc/ws-efficiency-phase2-20260910/`; the durable receipt records their paths
and the verification scripts' hashes. The old Phase 1 measuring script calls
helpers replaced in Phase 2: retain its captures as evidence, and adapt live
measurement to `ws_revision_api`/`ws_chapter_download` in Phase 3 instead of
restoring obsolete downloader helpers.

All 38 maintained local mega steps passed in 314.33 seconds, with only the
private writer `near-aleppo-census` omitted. The independent `ws-products`
candidate matched all 48 production plain/plus JSON files byte for byte.
The separate documentation, diagrams, Google parse, and WS/Google comparison
commands also passed. Their exact commands and logs are in the durable receipt;
`.novc/ws_efficiency_phase2_extras_20260910.py` runs those commands in sequence
and asserts candidate equality.

The full suite passed: **990 passed, 5 skipped, 65 subtests passed in 125.42
seconds**. The skips remain the Phase 1 semantic controls. Black at defaults
left all changed Python files formatted. After staging the new files, the
prose/Unicode/sibling-reach lints passed 9 tests in 22.88 seconds; their exact
command is in the receipt. `git diff --cached --check` also passed.
No raw book, production product,
Google input/product, bot output, or historical input has a tracked difference.
The only regenerated report differences were the same vendoring reports and
exact hashes recorded in Phase 1. Their generated versions are preserved under
`.novc/ws-efficiency-phase2-20260910/preserved-generated/`; the committed versions
were restored. The mega receipt's broad changed-file comparison also includes
the execution-plan edits made while generators ran; those are authored Phase 2
changes, not generator output.

The Phase 3 successor must verify the actual Phase 2 commit supplied in its
handoff, then perform the live equality and performance work below. Phase 2
does not authorize a production refresh to eliminate the known upstream
differences. Commit locally before dispatch, keep `ws-direct` on this exact
worktree, and reserve main integration for the archival procedure.

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

### Phase 3 execution record (2026-09-10)

Task `01a08d5d-48ae-75c2-8c4c-888047b3fd87` verified the exact development
checkout and `codex-worktree-3a6b` branch, clean status, and Phase 2 starting
commit `1ca7c3f903806d15bd82aec7136ff6e36e97b6a3`. The required-commit ancestry
check passed. The private input remained at
`55252b834d28a6c241e75758aff5d15836621f56`. The shared interpreter required
approved elevated execution; all commands and writes stayed in the development
worktree. No worktree or virtual environment was created.

The durable receipt is
[efficient-wikisource-downloads-phase3-validation.json](efficient-wikisource-downloads-phase3-validation.json).
Its command receipts, response hashes, per-book hashes, revision IDs, exact
upstream edits, product comparisons, and protected-tree hashes establish the
figures below. Captures and scripts are under
`C:/Users/BenDe/.codex/worktrees/3a6b/MAM-basics/.novc/`.

The forced download retrieved paired IDs/content for every chapter. The
equality gate compared each fetched array with the corresponding committed
`HEAD` array and admitted 909 records. An incremental scratch run started
from copies of the committed books and that partial manifest: 909 chapters
were reused and 20 were fetched. The forced, incremental, and unchanged
manifests contain exactly the same 929 identities and content hashes.

A separate full retrieval requested those frozen revision IDs, decoded the
responses with independently written validation, and serialized the books
without `ChapterClient`, `download_books`, or the production JSON writer.
All 929 arrays and 39 serialized books matched. API `maxlag` interruptions
remained visible and their responses were preserved. The incremental run
was repeated from the baseline. The first independent run was preserved
and repeated; after the independent retry stopped, its 53 successful
response pairs were hash-verified and decoded again, and the remaining
17 content batches were fetched. The completed independent retrieval has
70 unique content batches, 71 logical query invocations, and 71 transport
attempts, including the interrupted query. The earlier abandoned independent
run is recorded separately. No failed response supplied chapter content.
The production throttle, timeout, retries, User-Agent, and `maxlag=1` stayed
unchanged throughout.

The implemented download measurements were:

| Run, all 929 chapters | Reused / fetched | Metadata / content logical batches | Metadata / content attempts | Compressed body bytes | Download seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Forced full download | 0 / 929 | 0 / 70 | 0 / 70 | 2,065,356 | 224.76 |
| Migration from the 909-record seed | 909 / 20 | 19 / 11 | 19 / 11 | 95,505 | 96.02 |
| Unchanged repeat with complete scratch metadata | 929 / 0 | 19 / 0 | 19 / 0 | 24,940 | 67.15 |

Relative to the forced run, the unchanged repeat used **72.9% fewer requests**,
**98.8% fewer compressed body bytes**, and **70.1% less elapsed download time**.
Those are separate observations from single runs with the original random
throttle. They do not establish a fixed speedup. Each measured run used a
fresh session. Timing includes throttling, response decoding/capture recording,
hashing, book/metadata persistence, and a Git HEAD read; it excludes process
startup, scratch setup, and parsing/products. No product regeneration ran
during these performance samples. Compressed body bytes were read before
decompression and exclude headers, TLS, and chunk framing. Every successful
measurement response was HTTP 200 with gzip encoding. Chapter requests used
`allow_cache=False`; no generic cache files supplied responses.

The unchanged repeat preserved raw and metadata bytes and modification times.
The production manifest covers 909 chapters, so the 929-chapter unchanged
sample describes a fully populated scratch corpus. A normal all-book run
against the committed partial seed would fetch the 20 excluded chapters.

Correction recorded 2026-09-11, for finding 6 of the 2026-09-10 review: since `209b4c05` the
production manifest covers all 929 chapters, so the partial seed this paragraph describes no
longer exists; see "Production refresh of the 20 chapters, 2026-09-10" below.
`doc/efficient-wikisource-downloads-phase3-validation.json` still says "20 unequal chapters have
no seeded record"; it is Phase 3's receipt and stays as written.

Both live retrievals independently regenerated format-2, plain/plus, support
files, documentation, MAM-with-doc, MAM-simple, Sefaria/AJF, and OSIS. All
628 product paths and hashes matched:

| Product root | Matched files |
| --- | ---: |
| `out` | 39 |
| `MAM-parsed` | 50 |
| `MAM-simple` | 262 |
| `MAM-for-Sefaria` | 160 |
| `MAM-OSIS` | 25 |
| `gh-pages` | 91 |
| `doc` | 1 |

The scratch driver used the original worktree modules with explicit raw input
and scratch output paths. A file-write guard confined generation to each
scratch product directory. The guard exposed the claims index's relative
destination; scratch setup also needed the MAM-with-doc and OSIS page
directories. The scratch driver was corrected and the complete product chain
rerun. Documentation and assets whose generators verified identical bytes
without rewriting were included in both product manifests.

Compared with production, the live scratch products differ in 129 files;
their paths and hashes are recorded in the receipt. Those differences come
from the 20 upstream chapter differences, whose local/live hashes and exact
edits still match Phase 1. The production raw books were never replaced to
make the gate pass. Only the 909 equality-backed records were atomically
written to `in/mam-ws-revisions.json`, using real Phase 3 revision IDs.
No synthetic fixture ID or ID-less Phase 1 response supplied a seed record.

The seeded production selection then ran through the real
`download_wikisource.run` and its mandatory hook. All 909 selected chapters
were reused after 19 live metadata attempts; no content request occurred.
The download took 46.42 seconds and transferred 24,323 compressed body bytes.
The hook separately took 15.55 seconds, rebuilt all 39 format-2 books and
24 complete product groups, and passed documentation verification: 79 passed,
zero failed, and the existing pending claim
`mp.plain.docs.book39-skeleton.common`. Production raw bytes/modification
times and metadata bytes were unchanged by that run.

All 38 maintained local mega steps passed in 293.88 seconds; only the private
writer `near-aleppo-census` was omitted. The separate documentation, diagrams,
Google parse, and WS/Google comparison commands passed. An independently
generated candidate matched all 48 production plain/plus files. Protected
Wikisource raw, Google raw, bot-output, and historical-input hashes remained
unchanged. The only regenerated tracked differences were the same vendoring
reports with exactly the Phase 1/2 hashes; generated copies were preserved
and committed report bytes restored.

The full suite passed: **990 passed, 5 skipped, and 65 subtests passed in
112.97 seconds**. The skips are the same semantic controls recorded in
Phase 1. The staged prose/Unicode/sibling-reach lints passed **9 tests in
21.15 seconds**, and `git diff --cached --check` passed. No tracked Python
or test file changed in Phase 3; Black at defaults formatted the scratch
verification scripts. The final tracked changes are the partial metadata seed,
the Phase 3 receipt, and this execution record. No production raw book,
product, Google file, bot output, or historical input has a tracked difference.

For a new measurement, retain the earlier captures, adapt the scratch drivers
to a fresh output directory and the executor's verified starting commit, and
remeasure against that commit. The commands recorded in the receipt ran
`.novc/ws_efficiency_phase3_live_20260910.py` in this order: `forced`,
`candidate`, `incremental`, `unchanged`, `independent`, and `seed`.
`independent-resume` completed the interrupted exact-revision retrieval;
it accepts only hash-verified responses from that independent retrieval.
`.novc/ws_efficiency_phase3_products_20260910.py` generated each live product
set, and `.novc/ws_efficiency_phase3_compare_20260910.py all` compared every
array, serialization, and product manifest. The seeded-hook driver, local
mega driver, extras driver, and full-suite command are recorded separately.
The drivers refuse to overwrite earlier run directories unless an explicit
continuation is selected. Reusing a receipt is not a new measurement.

The programme has no remaining implementation phase and creates no successor.
The unresolved production-text decision concerns the 20 excluded chapters.
Chapter revisions establish raw wikitext freshness, not transcluded-template
freshness or one simultaneous whole-corpus snapshot. Commit locally; main
integration remains scheduled for the archival procedure below.

Correction recorded 2026-09-11, for finding 6 of the 2026-09-10 review: that production-text
decision was taken and carried out on 2026-09-10, in `209b4c05`; the next section records it.

## Production refresh of the 20 chapters, 2026-09-10

Recorded by a Claude session on 2026-09-11, for finding 6 of the 2026-09-10 review
(`doc/review-findings-2026-09-10.md`, on branch `dual-agent-review-2026-09-10` until that review
round integrates). Until this section, the refresh was recorded only in its commit message,
"Refresh Wikisource products. Download current Wikisource data and regenerate the complete
pipeline." No document records who decided to make it, or when.

The refresh is `209b4c05` (2026-09-10 20:53, co-authored by Codex), whose parent is `b2052ab9`,
the Phase 3 seed commit. It reached `main` through the merge `a0a2e3ab` at 21:22. Every figure
below compares `209b4c05` with its parent; re-establish each with the command given, and treat a
mismatch as a finding.

1. **All 20 chapters Phase 3 left unseeded were downloaded**, in 11 books: Genesis 43;
   Deuteronomy 28 and 32; Joshua 19; Judges 10; 1 Samuel 1 and 22; 2 Kings 6 and 17; Isaiah 22,
   24, 42 and 50; Zephaniah 3; Psalms 4, 71 and 84; Daniel 3; 2 Chronicles 26 and 28.
   `in/mam-ws-revisions.json` went from 909 records to 929
   (`git diff --stat 209b4c05^ 209b4c05 -- in/mam-ws/ in/mam-ws-revisions.json`).
2. **The same 11 books changed in the three intermediates written from `in/mam-ws/`**:
   `out/mam-ws-bot/proto/`, `out/mam-ws-bot/proto-fmt-2/` and `out/mam-ws-parsed-fmt-2/`.
3. **21 verses changed in `MAM-parsed/plus/`, and the same 21 in `MAM-parsed/plain/`**, all in
   those chapters:
   1. eleven meteg changes, nine removals (Joshua 19:8, 1 Samuel 1:6 and 22:22, 2 Kings 6:23,
      Isaiah 22:5, 42:24 and 50:7, Zephaniah 3:13, 2 Chronicles 26:15) and two additions
      (Isaiah 24:18, 2 Chronicles 28:19);
   2. ten changes to notes and templates (Genesis 43:28, Deuteronomy 28:30 and 32:18, Judges
      10:11, 2 Kings 17:15, Psalms 4:3, 71:9 and 84:4, Daniel 3:5, 2 Chronicles 28:23).
4. **Only the eleven meteg changes reached `MAM-simple/xml-vtrad-mam/`**
   (`git diff 209b4c05^ 209b4c05 -- MAM-simple/xml-vtrad-mam/`), and `MAM-for-Sefaria/csv/` and
   `MAM-OSIS/MAPM-24/` changed only in the six books holding those eleven verses.
5. **Two downstream outputs were left stale and caught up on 2026-09-11**: the mpplus change log
   under `gh-pages/MAM-with-doc/change-log/`, in `6b45ad0f`, once `f11ecaf8` had fixed the diff
   defect that the Isaiah 24:18 meteg exposed (findings 1 and 2 of the same review); and the
   post-stress-meteg survey, in `aedac688`, which also moved the page's pinned counts.

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
