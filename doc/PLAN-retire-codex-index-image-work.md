# Retire the codex-index image-work pipelines

State: ready for execution; recorded 2026-09-12

## Purpose

Remove the programs and page-sized source images that supported:

1. creating and editing line-break and column-coordinate data;
2. finding words in manuscript page images and creating crop-editor inputs; and
3. making additional Book-of-Job crops from the page images and the line-break
   data.

Preserve the line-break data and the rest of each codex index. Preserve every
existing Book-of-Job page and image. This plan removes the machinery for future
image-based work; it does not flatten the indexes to one resolution and does not
remove the results of the completed Book-of-Job work.

## Decisions recorded on 2026-09-12

1. Preserve all current page-level and below-page-level index data. Aleppo is
   intentionally uneven: much of the Tanakh is indexed at page level, while Job
   and some other retained material have finer detail. Cambridge Add. 1753 is
   also broader than Job alone: its line-break data begin in Psalms and continue
   through Job, and its page index also includes Lamentations. Do not narrow
   either corpus to Job.
2. Preserve all of `gh-pages/book-of-job/` byte-for-byte, including the finished
   Aleppo, Leningrad, and Cambridge Add. 1753 crops used by the published HTML.
   Existing Book-of-Job pages must continue to work after the programs and source
   page images are removed.
3. Preserve all six small evidence crops under `aleppo/page-snips/`,
   `cam1753/page-snips/`, and `leningrad/page-snips/`, together with their
   READMEs.
4. Preserve `book-of-job/out/cam1753-crops.json`. The coordinate data remains a
   part of the Book-of-Job record even though no current program will create or
   apply additional entries.
5. Preserve the line-break check reports and the other derived JSON that document
   the retained indexes. They become frozen artifacts rather than outputs that a
   maintained program is expected to regenerate.
6. Remove no Leningrad file. The current `leningrad/` tree contains no page-sized
   images, Python, line-break editor, or crop editor. Its README and three
   `page-snips/` PNGs stay. The broader below-page Leningrad location data under
   `uxlc/` and the programs that consume that location data also stay.
7. Do not recreate or modify the former `codex-index-aleppo`,
   `codex-index-cam1753`, or `codex-index-leningrad` checkouts or GitHub
   repositories. Their maintained contents moved into MAM-basics on 2026-09-04;
   this plan changes MAM-basics only.

## Execution setup

- Work in the exact MAM-basics checkout assigned to the executing task. Before
  editing, record `git rev-parse --show-toplevel`, `git rev-parse HEAD`, the branch
  or detached-HEAD state, `git status --porcelain`, and `git worktree list`. Do not
  assume that `C:/Users/BenDe/GitRepos/MAM-basics` is the development checkout.
- Read `C:/Users/BenDe/.codex/AGENTS.md`, the development checkout's
  `CLAUDE.md`, this entire plan, and `py/product_scopes.py` before editing.
- Load the `hebrew-prose` skill before changing prose in the manuscript READMEs,
  the page-snips notes, or `doc/meteg-after-silluq-job-4-12.md`.
- Use
  `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe` as the shared
  interpreter. Run scripts, Git commands, formatting, and tests from the verified
  development checkout.
- Preserve an existing worktree branch. If a newly allocated Codex worktree is
  detached, create `codex-worktree-<worktree-id>` at the current HEAD after
  confirming that the name is unused.

## Planning snapshot and preconditions

The planning snapshot was a clean primary checkout on `main` at
`068745779405ca38ec079ca25db9c8842195fd37`. Re-measure every figure before
editing and treat a mismatch as a finding rather than silently adjusting the
scope.

Create a uniquely named UTF-8 throwaway script at
`.novc/measure_codex_index_image_retirement.py`. The script should use
`git ls-files -z` for tracked-path inventories, `Path.stat()` for checked-out byte
sizes, and `hashlib.sha256` for protected-file manifests. It should also inspect
the ignored `cam1753/cam1753-pages/` directory directly and expand the grouped
Python deletion rules stated below. Run it from the verified checkout with:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/measure_codex_index_image_retirement.py
```

That command measured the page-sized image inputs as follows on the planning
snapshot:

| Path | Status | Files | Bytes |
| --- | --- | ---: | ---: |
| `aleppo/aleppo-pages/` | tracked source JPEGs | 37 | 29,668,155 |
| `cam1753/cam1753-spreads/` | tracked source JPEGs | 14 | 25,262,600 |
| `cam1753/cam1753-pages/` | ignored derived JPEGs | 28 | 50,316,747 |

The same command measured the retained fine-grained index and crop material:

| Material | Planning-snapshot count |
| --- | ---: |
| `aleppo/line-breaks/*.json` | 35 |
| `aleppo/column-coordinates/*.json` | 35 |
| `aleppo/ds-flat-stream/*.json` | 8 |
| `cam1753/cam1753-line-breaks/*.json` | 27 |
| `cam1753/cam1753-col-quads/*.json` | 28 |
| `cam1753/cam1753-spread-splits-doc/*.json` | 15 |
| retained `page-snips/*.png` across the three codex trees | 6 |
| finished codex crops in `gh-pages/book-of-job/jobn/img/` | 480: 160 per codex |

The measurement script must write a protected-file manifest for:

- all tracked files under `gh-pages/book-of-job/`;
- all retained JSON under `aleppo/`, `cam1753/`, and `book-of-job/out/`;
- `aleppo/check_line_breaks.html` and `cam1753/check_line_breaks.html`;
- `cam1753/cam1753-gutter-profiles.png`; and
- all three `page-snips/` trees.

Compare that manifest after the removal. A changed protected file is a finding.
Documentation files within a protected tree may be deliberately edited only when
this plan names the edit; exclude those named Markdown files from the byte-identity
comparison and inspect their diffs separately.

The planning run collected 1,000 tests. A full run without a writable explicit
temporary directory reached 994 passed and 5 skipped, then had one setup error
because the sandbox denied pytest's default directory under
`C:/Users/BenDe/AppData/Local/Temp`. The affected six-test module passed with the
explicit writable temporary directory used below. The expected fresh baseline is
therefore 995 passed and 5 skipped, but the executing task must establish the
current count with this command before editing:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py --basetemp .novc/pytest-retire-codex-index-image-work -p no:cacheprovider
```

## Remove the page-sized source images

- Remove the tracked `aleppo/aleppo-pages/` tree.
- Remove the tracked `cam1753/cam1753-spreads/` tree.
- Move the ignored, derived `cam1753/cam1753-pages/` tree to the Windows Recycle
  Bin after resolving and checking its exact absolute path. This ignored tree is
  not preserved by Git, so do not delete it permanently.
- Keep `cam1753/cam1753-gutter-profiles.png`. It is a compact retained record, not
  a page-sized source scan and not an input needed by the published Book-of-Job
  pages.
- Before removing the tracked JPEGs, record the then-current pre-removal commit in
  `aleppo/aleppo-pages-provenance.md` and
  `cam1753/cam1753-spreads-provenance.md`. Preserve the existing source and rights
  information. State that Git history can restore the exact tracked files and that
  the recorded external sources can supply a fresh source copy.

No full-page image is needed at build time. The published Book-of-Job HTML reads
the finished crops already under `gh-pages/book-of-job/`; it does not read the
Aleppo page JPEGs, Cambridge spread JPEGs, or ignored Cambridge page JPEGs.

## Remove the image-work Python

Expand the deletion set from tracked paths before removing anything. The planning
snapshot has 48 Python files in the set below. A different expansion is a finding
to investigate.

### Aleppo and shared Aleppo Book-of-Job code

- Delete every `py/main_ac_*.py` except
  `py/main_ac_gen_index_flat_annotated.py`.
- Delete `py/check_ac_all.py`.
- Delete the seven files under `py/py_ac_loc/`.
- Delete the six files under `py/py_ac_word_image_helper/`.
- Delete `py/main_list_missing_aleppo_imgs.py`.

`py/main_ac_gen_index_flat_annotated.py` stays because it maintains the page-level
Aleppo index from retained JSON without using manuscript images.

### Cambridge Add. 1753 and shared Cambridge Book-of-Job code

- Delete `py/cam1753_paths.py`.
- Delete every `py/main_cam1753_*.py`.
- Delete every `py/check_cam1753_*.py`.
- Delete the eight files under `py/py_cam1753_loc/`.
- Delete the four files under `py/py_cam1753_word_image/`.
- Delete `py/main_gen_cam1753_crop_editor.py`.
- Delete `py/main_apply_cam1753_crops.py`.

Do not add replacement commands. The purpose is to stop maintaining a workflow
that Ben does not plan to use again, not to preserve the workflow behind a new
interface.

### Leningrad code

Delete nothing for Leningrad. No Leningrad line-break or crop-editor program is
present. Keep `py/main_uxlc_estimate_atom_loc.py`, `py/main_verse_links.py`,
`py/uxlc_misc/my_uxlc_find_atom.py`, the Leningrad location modules they use, and
`uxlc/data/lci_augrecs.json`. Those files support current below-page location
lookups rather than the retired Book-of-Job crop workflow.

## Simplify the surviving path and scope declarations

- Reduce `py/ac_paths.py` to the retained Aleppo data root, corrected and annotated
  flat-index paths, and the surviving Aleppo code scope. Remove accessors and prose
  for page scans, line-break editors, column editors, scratch editor output, flat
  streams, and the frozen check report when no surviving program calls them.
- Update `py/main_ac_gen_index_flat_annotated.py` so its documentation names the
  current MAM-basics paths and retained index purpose without describing removed
  image programs.
- Remove the deleted packages and top-level programs from `py/boj_paths.py`'s code
  scope. Keep the Book-of-Job published-image paths and
  `cam1753_crops_path()`, because the surviving authoring pipeline reads the
  finished crops and retained coordinates. State explicitly that these are
  retained inputs with no maintained producer.
- Remove the Cambridge code scope and `cam1753_paths` import from
  `py/repo_scopes.py`. Keep the Cambridge data root in `corpus_roots()` so the
  retained hand-authored JSON remains covered by the mark-order check.
- Remove the deleted hand-run programs from `py/tests/test_mega_coverage.py`'s
  `NOT_IN_MEGA` declarations and delete reason constants that become unused.
- Remove the `cam1753_paths` import from
  `py/tests/test_h_dot_below_nfc.py`; address the retained Cambridge corpus through
  the repository root. Remove exclusions that existed only for the deleted image
  directories, while preserving the exemptions required by retained external data.
- Remove the obsolete image-helper `strip_heb` discussion from
  `py/product_scopes.py`. Keep the product-tier rule itself unchanged.
- Remove only the stale synchronization claim from
  `py/uxlc_misc/my_uxlc_find_atom.py`; do not change the lookup's behavior.
- Search `.vscode/launch.json`, test registries, import sites, help text, and source
  lints for the deleted names. Remove every live reference. Do not edit a historical
  receipt merely because it names a file that once existed.

## Rewrite current documentation as a retained-data description

- Update `README.md`, `aleppo/README.md`, `cam1753/README.md`,
  `cam1753/CLAUDE.md`, and `leningrad/README.md`. Describe the retained index data,
  state that the image programs and page-sized source images were retired, and make
  clear that Leningrad had no such program or page-sized image to remove.
- Convert `aleppo/doc/aleppo-line-breaks.md` and
  `cam1753/doc/cam1753-line-break-task.md` from runnable procedures into static
  coverage, schema, provenance, and interpretation notes. Preserve facts needed to
  understand the retained JSON. Remove Kraken and editor instructions that can no
  longer run.
- Retain `aleppo/check_line_breaks.html` and
  `cam1753/check_line_breaks.html`, but document each as a frozen report. Do not
  regenerate either report during this removal.
- Delete the obsolete future-crop procedures
  `doc/boj-aleppo-word-crops.md`, `doc/boj-cam1753-word-crops.md`, and
  `doc/boj-leningrad-word-crops.md`.
- Retain `doc/boj-image-crop-reproducibility.md`,
  `doc/boj-viewing-image-metadata.md`, and
  `doc/boj-leningrad-image-scaling.md`. They explain the metadata and display of
  preserved images; rewrite only claims that a removed program is still available.
- Update `doc/book-of-job-artifacts.md` so the artifact register says that all
  current images and Cambridge crop coordinates are retained source data and that
  no crop-producing program remains.
- Update the three `page-snips/README.md` files and
  `doc/meteg-after-silluq-job-4-12.md` only where current prose claims that a
  page-sized local source image remains. Preserve each statement supported by the
  retained crop.
- Update `DATA-LICENSES.md` so it accurately describes retained crops and removed
  full-page scans without weakening the rights statements.
- Preserve finished dated plans, reviews, and execution records as historical
  receipts. In particular, do not rewrite the 2026-09 evacuation plans or
  `in/mam_products_phase6*.json` to hide paths that existed when those records were
  made.

## Verification

### Protected data and published pages

- Re-run `.novc/measure_codex_index_image_retirement.py` and compare the protected
  SHA-256 manifest with the pre-edit manifest. Every unapproved difference is a
  failure.
- Confirm that `aleppo/aleppo-pages/`, `cam1753/cam1753-spreads/`, and
  `cam1753/cam1753-pages/` are absent.
- Confirm that every retained line-break, coordinate, split-record, page-index,
  flat-stream, page-snip, Book-of-Job crop, and Book-of-Job HTML file remains.
- Run the Book-of-Job checks, including the broken-local-image-reference check:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/check_all.py
```

### Source and documentation

- Search tracked files for every deleted module, package, entry point, and image
  directory. Current code, current instructions, command examples, imports, and
  path declarations must have no live reference. Historical plans and reviews may
  retain factual references to the removed material.
- Search current documentation for claims that new line-break data or new
  Book-of-Job crops can be made locally. The retained data may be described and
  inspected, but no runnable procedure should point at deleted code or scans.
- Format only the surviving Python files changed by the implementation:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe -m black py/main_ac_gen_index_flat_annotated.py py/ac_paths.py py/boj_paths.py py/repo_scopes.py py/tests/test_mega_coverage.py py/tests/test_h_dot_below_nfc.py py/product_scopes.py py/uxlc_misc/my_uxlc_find_atom.py
```

- Run the full suite with a repository-local temporary directory:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py --basetemp .novc/pytest-retire-codex-index-image-work -p no:cacheprovider
```

- Run `git diff --check` and inspect the complete diff before committing.

### Mega pipeline and product diff

`py/ac_paths.py` and `py/main_ac_gen_index_flat_annotated.py` remain in the mega
pipeline's generator tier. The implementation therefore owes a mega run even
though no product change is intended. Commit the implementation locally before
the mega run, because some mega checks compare the committed revision rather than
the working tree:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_0_mega.py
```

A successful mega run leaves no product or data diff. Any change under
`gh-pages/`, `MAM-parsed/`, `MAM-simple/`, `MAM-for-Sefaria/`, `MAM-with-doc/`,
`MAM-OSIS/`, `aleppo/*.json`, `cam1753/*.json`, or `book-of-job/out/` is a failure
until explained. This plan expects no such change.

## Expected final diff

- The expected tracked deletions are the remeasured 48 Python files, the 37
  Aleppo page JPEGs, the 14 Cambridge spread JPEGs, and the three obsolete crop
  procedures.
- The expected untracked removal is the remeasured 28 ignored Cambridge page
  JPEGs, moved to the Recycle Bin.
- The expected edits are surviving path and scope declarations plus current
  documentation and provenance.
- No Leningrad file is deleted.
- No retained index JSON, line-break JSON, coordinate JSON, crop-coordinate JSON,
  page-snip PNG, finished Book-of-Job image, Book-of-Job HTML, or published product
  changes.

## Integration and risk

In a primary checkout, commit directly to `main`, run the mega pipeline against
the committed implementation, commit any explained follow-up needed to restore a
clean generated tree, and push only after all checks pass. In a secondary
worktree, commit on its existing branch; immediately before archival, merge
`main` into the branch, run the mega pipeline and inspect its diff, then
fast-forward the primary checkout and push `main`.

This work touches both risk axes:

1. **Products.** The removal changes hand-run programs that formerly could create
   published Book-of-Job images and changes a path module used by the mega
   generator tier. No published or distributed product is intended to change.
   Protected-file hashes, the Book-of-Job checks, and the mega diff enforce that
   boundary.
2. **Hard-to-undo acts.** The implementation deletes tracked code and JPEGs,
   removes ignored local JPEGs, and ultimately pushes `main`. Resolve every target
   before deletion, use the Recycle Bin for the ignored files, record the
   pre-removal commit and external sources, and rely on Git history for exact
   recovery of tracked files. Do not rewrite history or alter the old GitHub
   repositories.
