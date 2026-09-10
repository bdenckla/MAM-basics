# Reduce MAM-basics worktree creation time by consolidating tracked files

Ben authorized this programme on 2026-09-10 in task
`01a08c45-a1ec-79f2-9399-1293caa62c9c`, **Plan faster MAM-basics worktrees**.
The objective is to reduce full worktree creation time while preserving data,
ordinary commands, generated products, and published URLs. The programme changes
storage for UXLC notes, historical MAM-parsed inputs, and Job quirk records.
The file-count estimate is not a prediction of the timing improvement.

## Execution status and checkout ownership

| Phase | Scope | Status on 2026-09-10 |
| --- | --- | --- |
| 1 | Inventory and verification preparation | Complete; evidence and plan are in the Phase 1 commit identified below |
| 2 | UXLC notes | Complete in the Phase 2 branch head identified below |
| 3 | Historical snapshots | Next task; created only after the Phase 2 commit |
| 4 | Job records | Pending Phase 3 |
| 5 | Combined verification | Pending Phase 4 |
| 6 | Benchmark and close-out | Pending Phase 5 |

Phase 1 task: `01a08c68-10a6-7442-8ff7-1e5ac0303211`.
Its verified development checkout is
`C:/Users/BenDe/.codex/worktrees/2665/MAM-basics`, on branch
`codex-worktree-2665`. The starting commit is
`dc043165f98b8a75ee3faa34314b70d0b2171a8f`. Both `main` and `origin/main`
matched that commit at startup and at the pre-documentation check. HEAD was
detached and the checkout was clean before the branch was created.

At the final Phase 1 pre-commit check, `main` and `origin/main` had advanced to
`d612f71c9794d8d480c7bbc3b18768d7d7003838` ("Verify Phase 6C MAM-with-doc
regeneration"). Phase 1 HEAD remained at the required baseline. No integration
was performed during implementation; recheck `main` before archival integration.

The Phase 1 commit is the commit that first adds this plan and
`doc/worktree-file-consolidation-baseline.json.gz`. Find it without relying on a
self-referential hash in its contents:

```powershell
git -C C:/Users/BenDe/.codex/worktrees/2665/MAM-basics log --diff-filter=A --format=%H -- doc/PLAN-worktree-file-consolidation.md
```

The Phase 2 creation prompt must give the actual full Phase 1 hash. The Phase 1
task's final response records the returned Phase 2 task ID; the Phase 2 executor
records its verified ID, checkout, starting commit, and result in this plan.
Creating the successor is the predecessor's final action that assigns work;
the predecessor makes no further development edits after creation.

The primary clone is `C:/Users/BenDe/GitRepos/MAM-basics`. Development takes
place only in each task's verified worktree. Use the shared interpreter at
`C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe`; create no `.venv`,
junction, or symlink inside a worktree. The suite's remaining sibling input is
`C:/Users/BenDe/GitRepos/MAM-private`; Phase 1 measured its clean checkout at
`55252b834d28a6c241e75758aff5d15836621f56`.

Task `01a08c47-b5d5-7193-b500-480af9d9d427` was independently writing in
`C:/Users/BenDe/.codex/worktrees/3a6b/MAM-basics` when Phase 1 began. Preserve
that checkout. Concurrent tasks may advance `main`; recheck it before integration.
One writer per checkout is the rule, rather than requiring every other task to end.

Ben's phased-execution decision, 2026-09-10: each fresh task executes exactly one
phase, verifies and commits locally, updates this plan with measured results and
unexpected findings, and creates only the next phase as its final action. If
unexpected work threatens context capacity, stop at a clean committed checkpoint
and record the remaining acceptance criteria before creating a continuation for
the same phase. Do not silently combine phases or skip acceptance criteria.

Ben's model decision, 2026-09-10: continue Phase 1 with its current model. Create
Phase 2 and any later continuation tasks with **Sol at extra high effort**
(`model: gpt-5.6-sol`, `thinking: xhigh`). Carry this preference in successor
prompts; do not switch the model of an already running task.

Before every phase, read:

1. `C:/Users/BenDe/.Codex/AGENTS.md`, the live user instructions.
2. `CLAUDE.md` under the verified development checkout.
3. `C:/Users/BenDe/.agents/skills/hebrew-prose/SKILL.md` and its
   `references/verifying.md` before writing about the Job records' accentuation
   prose. Apply additional references when the prose being edited needs them.
4. For Phase 4, `doc/boj-quirkrec-comments.md` under the verified checkout before
   touching `py/author_boj*`; its old shell examples do not override live instructions.

Verify `git rev-parse --show-toplevel`, `git rev-parse HEAD`,
`git branch --show-current`, and `git status --porcelain` before editing and
again when analysis becomes implementation. The required predecessor commit must
equal HEAD or be an ancestor of a deliberately newer starting point. Investigate
any mismatch. For a new managed worktree with detached HEAD, use
`codex-worktree-<actual-worktree-id>`; preserve an existing checked-out branch.
Do not overwrite an existing proposed branch name.

When creating a successor, inspect saved project paths first. If the intended
worktree is a saved project, use that exact path directly with the local
environment. Otherwise a fresh managed worktree may start from the exact named
local predecessor branch: specify the branch as the starting state, never the
primary checkout's working tree or an omitted default. A separate checkout also
allows the predecessor's later archival integration while the successor works.
Require the successor to verify the allocated path and predecessor ancestry.
Record a provisional `clientThreadId` as pending setup, never as a usable task ID.
Do not repeat task creation merely because a listing omits a pending task.

## Content and behavior that must remain unchanged

- Every committed UXLC HTML capture's exact bytes, including Unicode, whitespace,
  and line endings; every result of `clc_note_pages.local_note_prose`.
- Every historical manifest source commit, date, filename, byte size, Git blob
  identifier, release order, and migration identity.
- Every Job `RECORD_*` identifier, expression, comment, value, Python value type,
  and the exact order of `job_quirkrecs.RAW_QUIRKRECS`; record relations and
  generated detail-page names.
- Generated output bytes, published files and URLs, image collections, ordinary
  CLI arguments, current MAM product layouts, and the Pages deployment workflow.
- Wikisource downloads: 929 chapters in 39 per-book files under `in/mam-ws/`.
  Partial downloads already merge into the containing book through
  `download_wikisource._merge_book_contents`. Tracked format 1 output is already
  absent; `parse_ws` writes optional format 1 output under `.novc/`.

Generated-output retention and sparse worktrees are separate possible projects.
Do not refresh downloads, accept source-data changes, revise historical data,
normalize Hebrew, or extract release archives as part of ordinary generation.

## Phase 1 measurements and verification receipt

All baseline measurements use MAM-basics
`dc043165f98b8a75ee3faa34314b70d0b2171a8f` on 2026-09-10. Re-measure instead
of treating the following figures as current facts after another commit.

The baseline contains **5,646 tracked files**, totaling **831,571,756 Git blob
bytes**. The inventory aggregates **356 directory prefixes including the root**.
These are committed blob sizes, not disk allocation or checkout byte sizes;
`.gitattributes` intentionally checks CSV files out with CRLF.

| Largest top-level directories | Tracked files |
| --- | ---: |
| `gh-pages` | 1,859 |
| `py` | 1,225 |
| `uxlc` | 547 |
| `MAM-simple` | 383 |
| `out` | 341 |
| `in` | 319 |
| `MAM-parsed` | 204 |
| `MAM-for-Sefaria` | 164 |

| Collection | Baseline files | Planned files | Reduction before support files |
| --- | ---: | ---: | ---: |
| UXLC notes | 477 | 36 populated-book JSON files | 441 |
| Historical release data | 144 | 6 ZIP archives | 138 |
| Job record modules | 160 | 39 populated-chapter modules | 121 |
| Total reduction | | | 700 |

The estimated reduction is 700 / 5,646 = about 12.4%, before support files.
The historical directory also contains `README.md` and `manifest.json`; neither
file is part of the 144 data files. Phase 1 adds this plan and one evidence file.
Later phases must count all additions when reporting the actual net reduction.

The scratch driver used for the original measurement is
`C:/Users/BenDe/.codex/worktrees/2665/MAM-basics/.novc/worktree_file_consolidation_phase1.py`.
Its `inventory` operation reads `git ls-tree -r -l -z <commit>` and aggregates
every directory prefix. Its `oracle` operation verifies the source captures,
historical data, and Job records. Its `clc`, `mpp`, `job`, `suite`, and `checks`
operations run the real commands below. Logs and all-file before/after snapshots
remain in
`C:/Users/BenDe/.codex/worktrees/2665/MAM-basics/.novc/worktree-file-consolidation-phase1/`.
Scratch files are conveniences; the committed evidence and reproduction method
below are sufficient for a fresh checkout.

| Real command after the absolute interpreter path | Tracked files rewritten | Byte changes | Exit |
| --- | ---: | ---: | ---: |
| `py/main_clc.py all` | 12 | 0 | 0 |
| `py/main_diff.py mpp --all` | 13 | 0 | 0 |
| `py/main_gen_misc_authored_english_documents.py` | 183 | 0 | 0 |
| `py/main_test.py -q -p no:cacheprovider` | 0 | 0 | 0 |
| `py/check_all.py` | 2 | 0 | 0 |

Each generator started with empty `git status --porcelain`. The driver hashed
every tracked file before and after each command, recorded the paths whose
timestamps changed, and checked Git status afterward. All tracked bytes matched,
and every run left Git status empty. There is **no pre-existing generated drift**
in the affected commands at the measured commit. No source or generated files
were accepted, corrected, or restored during Phase 1.

The full suite result was **989 passed, 5 skipped, 65 subtests passed**, with
112.81 seconds reported by pytest and 114.843 seconds for the subprocess.
The source and HTML command reported **All 7 checks passed**. The suite's existing
skips concern edition-transcription differences; they are not missing-input skips.
No tests or tracked Python files were added or changed in Phase 1. The scratch
scripts were formatted with Black. The new plan is also checked after staging
with the existing prose mark-order and Latin-diacritic lints: **7 passed in
16.05 seconds**. The command was:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider py/tests/test_prose_mark_order.py py/tests/test_h_dot_below_nfc.py
```

The inventory reproduction script printed below was extracted into a scratch file
and executed against the baseline commit. Its complete directory map and all
collection figures matched the evidence. An independent readback also confirmed
the hashes of all 208 unique affected output paths. The receipt records Python
3.13.15 and Git 2.43.0.windows.1. The original verification command was:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/verify_worktree_file_consolidation_phase1_plan.py
```

The environment required escalated execution of the shared interpreter and Git
metadata writes because the sandbox account could not execute the interpreter
or write the primary clone's shared `.git` storage. No primary-checkout source
or generated files were written. A process-local `safe.directory` entry named
only the verified worktree; no global Git configuration was changed. These were
execution-environment findings, not repository defects.

## Compact baseline evidence and comparison method

Evidence in the Phase 1 checkout:
`C:/Users/BenDe/.codex/worktrees/2665/MAM-basics/doc/worktree-file-consolidation-baseline.json.gz`.
The same repository-relative file travels with every successor commit. It is a
single gzip-compressed UTF-8 JSON document, schema 1, written with compression
level 9 and `mtime=0`. It is **154,023 bytes**, representing **651,637 uncompressed
bytes**. Its SHA-256 is
`f04b2d9f0e60ed35794218c444bb88ea4ec5245302efcbe71c049d413d60c3fa`;
the uncompressed document's SHA-256 is
`6a09b6beb096e853b9e78ddb88fce46952e8127a635693073379136bc4a8bffb`.
Preserve this baseline file unchanged throughout the programme.

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath C:/Users/BenDe/.codex/worktrees/2665/MAM-basics/doc/worktree-file-consolidation-baseline.json.gz
```

Read it in a real scratch Python file with
`json.loads(gzip.decompress(path.read_bytes()))`; do not use inline Python or
extract anything into a product directory. The evidence contains:

1. `inventory`: the baseline commit, total count and bytes, and every directory
   prefix mapped to `[file_count, blob_bytes]`.
2. `uxlc_notes.entries`: every original path, mode, Git blob identity, size,
   SHA-256, and complete extracted prose string. All 477 pages in 36 populated
   books produced nonempty prose. The exact raw bytes are retained by the named
   Git blobs in the baseline commit; they are not duplicated inside the evidence.
3. `historical`: the complete original manifest, its path and blob identity,
   SHA-256, and verified member count. Every listed file was checked against
   its declared size and Git blob identity, with duplicate and unlisted data
   members rejected. Original source commit dates and migration metadata are
   preserved inside the copied manifest.
4. `job`: the complete ordered, recursively type-tagged `RAW_QUIRKRECS`, ordered
   record identifiers and per-record digests, original source paths and blob
   identities, populated chapters, and type counts. The data includes 393 lists,
   870 dictionaries, 5,897 strings, 1,005 integers, 21 booleans, and 4 tuples.
5. `runs`: command, checkout, HEAD, exit code, elapsed time, output paths with
   baseline blob identity, size and SHA-256, unchanged-byte results, and log
   digests. `measurement` records the interpreter/Git versions and sibling input
   commit. `wikisource` records book/chapter counts and absent tracked format 1.

The type encoding is `[fully_qualified_builtin_type, payload]` at **every node**,
including dictionary keys. Dictionary payloads are insertion-ordered lists of
`[encoded_key, encoded_value]` pairs; list and tuple payloads are ordered encoded
elements. Strings, integers, booleans, and null retain their JSON values; floats,
if encountered in a later comparison, use `float.hex()`. Unsupported types fail.
Serialize encoded values with `json.dumps(value, ensure_ascii=False,
separators=(",", ":"))`, encode as UTF-8, and hash with SHA-256, without a trailing
newline. The complete ordered Job value digest is
`380d32bc7114735166e07cc77bdcab11eebff6500d5106d138ef99ae6efff95b`.
Phase 1 decoded the complete stored values, compared them to the imported records,
and re-encoded both to confirm equality including types and dictionary order.

For future comparisons, use these independent checks:

1. Reconstruct each UXLC entry as UTF-8 bytes. Compare the exact path/key set,
   size, SHA-256, and Git blob identity against `uxlc_notes.entries`. Compare
   `local_note_prose` to the stored prose string for every entry. For any mismatch,
   read the original bytes with `git cat-file blob <baseline-blob>` into a scratch
   file and inspect the actual difference. No network download is an oracle.
2. Compare the current historical manifest to the complete stored manifest.
   Verify every archive member with its manifest size and Git blob identity:
   SHA-1 of `b"blob " + ascii_decimal_length + b"\0" + member_bytes`.
   Compare the complete member-name set and reject duplicates before reading.
3. Import current `author_boj_util.job_quirkrecs.RAW_QUIRKRECS` and encode the
   entire list using the preceding type algorithm. Compare the encoded tree,
   ordered identifiers, per-record hashes, and whole-list hash. The original
   record source blobs also permit independent expression/comment comparisons.
   A plain JSON conversion that merges tuples into lists is insufficient.
4. Run the real affected generator from the task's worktree. Compare every path
   in the corresponding `runs.<command>.outputs` map to its stored SHA-256 and
   size; check the whole checkout for unexpected additional, missing, or changed
   files. Inspect generated diffs, never update the baseline to make a failure pass.

## Commands and inventory reproduction

Run commands from the task's **verified worktree root**. For Phase 1 that root is
`C:/Users/BenDe/.codex/worktrees/2665/MAM-basics`. A fresh task substitutes its
verified allocated path for that development root, leaving the interpreter and
sibling root unchanged. Record the actual paths and commits in the phase receipt.

```powershell
$env:REPOS_ROOT = "C:/Users/BenDe/GitRepos"
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_clc.py all
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py mpp --all
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_gen_misc_authored_english_documents.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/check_all.py
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider
```

Format only changed Python files with the absolute interpreter and `-m black`,
at its defaults. Do not prefix tracked commands with `PYTHONUTF8`. Use explicit
UTF-8 file I/O and reconfigure stdout/stderr in scratch scripts. Existing checks
and whole-corpus comparisons are sufficient; add a test only when it provides
an independent differential oracle or a mechanical source lint. Missing data
must fail rather than skip.

To re-establish all inventory figures in a fresh checkout, write the following
as `.novc/recheck_worktree_file_consolidation_inventory.py` with the file-editing
tool, then run the command below. This scratch script reads the requested commit,
not the checkout's possibly modified files. It writes every directory prefix to
an explicit UTF-8 report; pass the completed commit in Phase 6 as well.

```python
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")
commit = sys.argv[1]
raw = subprocess.run(
    ["git", "ls-tree", "-r", "-l", "-z", commit],
    check=True, capture_output=True,
).stdout
counts, sizes = Counter(), Counter()
files = {}
for record in raw.split(b"\0"):
    if not record:
        continue
    meta, name = record.split(b"\t", 1)
    mode, kind, sha, size = meta.decode("ascii").split()
    assert kind == "blob"
    name = name.decode("utf-8")
    files[name] = [sha, int(size)]
    parts = name.split("/")
    for index in range(len(parts)):
        prefix = "/".join(parts[:index]) or "."
        counts[prefix] += 1
        sizes[prefix] += int(size)
notes = [p for p in files if p.startswith("uxlc/in/UXLC-notes/")]
history = [p for p in files if p.startswith("MAM-parsed/historical/")
           and p.endswith(".json") and not p.endswith("/manifest.json")]
records = [p for p in files if p.startswith("py/author_boj_qr/qr_")]
ws = [p for p in files if p.startswith("in/mam-ws/")]
chapters = 0
for path in ws:
    blob = subprocess.run(
        ["git", "cat-file", "blob", files[path][0]],
        check=True, capture_output=True,
    ).stdout
    chapters += len(json.loads(blob))
report = {
    "commit": commit, "files": len(files), "blob_bytes": sizes["."],
    "directories": {p: [counts[p], sizes[p]] for p in sorted(counts)},
    "notes": len(notes), "note_books": len({p.split('/')[3] for p in notes}),
    "historical_data_files": len(history),
    "historical_revisions": len({p.split('/')[2] for p in history}),
    "record_modules": len(records),
    "record_chapters": len({Path(p).name[3:5] for p in records}),
    "wikisource_books": len(ws), "wikisource_chapters": chapters,
    "tracked_format_1": sum(p.startswith("out/mam-ws-parsed-fmt-1/") for p in files),
}
target = Path(".novc") / f"worktree-file-inventory-{commit[:12]}.json"
target.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {target}; {len(files)} tracked files")
```

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/recheck_worktree_file_consolidation_inventory.py dc043165f98b8a75ee3faa34314b70d0b2171a8f
```

Collection figures in that report describe the old layout only when run at the
baseline commit. For a consolidated commit, classify the new JSON files, ZIP
archives, and chapter modules explicitly, and compare their internal entry counts
against the baseline evidence. Never interpret an empty old-layout discovery as
successful preservation.

## Phase 2: UXLC note storage

### Phase 2 execution receipt

Phase 2 task: `01a08c7b-59b5-7e43-ab66-570e4c651ba0`. Its verified
development checkout is
`C:/Users/BenDe/.codex/worktrees/4378/MAM-basics`, on branch
`codex-worktree-4378`. The checkout started clean and detached at the required
Phase 1 commit `b080a01a87f29f2140144a1247c45c654d240224`; the branch did not
exist elsewhere and was created at that commit before any edit. The required
Phase 1 commit remained HEAD through implementation and the pre-staging checks.
At the last receipt measurement, `main` and `origin/main` were both
`d612f71c9794d8d480c7bbc3b18768d7d7003838`. The sibling MAM-private
checkout was clean at `55252b834d28a6c241e75758aff5d15836621f56`.

The implementation replaces the 477 raw HTML paths with 36 per-book JSON
objects and adds `py/clc/clc_note_storage.py`. `NoteStorageOperation` is the
single storage interface used by the reader, downloader, and ZIP verifier. One
operation loads a book once. A successful addition atomically replaces the
book JSON before updating the operation cache; an operation created afterward
reads the new value. There is no process-global cache. Missing keys still
produce `None` for `local_note_prose`, while malformed JSON, duplicate keys,
non-object roots, invalid filenames, non-string page values, and unexpected
storage entries fail.

The immutable evidence file retained its compressed SHA-256
`f04b2d9f0e60ed35794218c444bb88ea4ec5245302efcbe71c049d413d60c3fa`.
The offline migration read every source byte string from the Git blob recorded
by that evidence rather than from a network source. Production-code readback
then verified the complete reconstructed path/key set, all 477 sizes and
SHA-256 hashes, and all 477 `local_note_prose` strings. Every per-book object has
sorted keys; subsequent additions use the same ordering and the repository's
atomic temporary-file replacement helper.

The downloader replay used a task-local copy of the complete committed corpus.
Calling the real `_download_one` path for all 477 stored entries made zero
requests. One simulated successful download added a CRLF-bearing non-ASCII HTML
string, kept every unrelated entry unchanged, left sorted keys, and was visible
to a fresh operation. Repeating the successful page through the writing
operation and through the fresh operation made zero requests. Two simulated
failed requests left the containing JSON bytes unchanged. Two reads through one
operation invoked the book loader once. Six malformed/missing-storage cases
had the required failure or missing-key result.

The frozen `C:/Users/BenDe/Downloads/Notes.zip` was absent. No download or
replacement-data refresh was attempted. The production ZIP verifier was instead
run against the explicitly identified scratch replay archive
`C:/Users/BenDe/.codex/worktrees/4378/MAM-basics/.novc/uxlc-note-storage-phase2-fxko1ywz/Notes-phase2-replay.zip`.
That replay reported 477 `IDENTICAL` and zero `NO-PROSE-EXTRACTED`. This result
exercises the verifier against the consolidated store; it is not the historical
ZIP comparison.

`py/main_clc.py all` rewrote the same 12 paths Phase 1 recorded. Every path,
size, and SHA-256 matched the immutable evidence, and no generated file appeared
in `git status`. The existing CLC tests passed 45 of 45. `py/check_all.py`
reported all 7 checks passed. The full suite reported **989 passed, 5 skipped,
65 subtests passed** in 121.72 seconds; the five skips remain the expected
edition-transcription differences. The prose mark-order and Latin-diacritic
hygiene selection passed 7 of 7 in 15.83 seconds. Python was 3.13.15 and Git was
2.43.0.windows.1.

Commands ran from the verified Phase 2 worktree. Commands that read sibling
inputs used `REPOS_ROOT=C:/Users/BenDe/GitRepos`. The exact commands were:

| Purpose | Command |
| --- | --- |
| Migrate committed blobs and verify before removing legacy paths | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/migrate_uxlc_note_storage_phase2.py` |
| Verify corpus, downloader behavior, operation lifetime, and malformed storage | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/verify_uxlc_note_storage_phase2.py` |
| Exercise ZIP verifier with the scratch replay archive | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_verify_notes_zip.py C:/Users/BenDe/.codex/worktrees/4378/MAM-basics/.novc/uxlc-note-storage-phase2-fxko1ywz/Notes-phase2-replay.zip` |
| Regenerate CLC | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_clc.py all` |
| Compare the 12 regenerated outputs with Phase 1 | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/verify_worktree_file_consolidation_phase2_outputs.py` |
| Run the existing CLC tests | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider py/tests/clc_attribution_test.py py/tests/clc_collect_test.py py/tests/clc_dual_cant_test.py py/tests/clc_kq_test.py py/tests/clc_note_pages_test.py py/tests/clc_versification_test.py` |
| Run all source and HTML checks | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/check_all.py` |
| Run the full suite | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider` |
| Check changed prose and Latin-diacritic hygiene | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider py/tests/test_prose_mark_order.py py/tests/test_h_dot_below_nfc.py` |
| Measure the prospective tracked-file inventory | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/measure_worktree_file_consolidation_phase2_inventory.py` |

The Phase 1 tree has 5,648 tracked files: the 5,646-file baseline plus the plan
and compressed evidence. Phase 2 removes 477 legacy HTML files, adds 36 JSON
files, and adds one support module. The resulting 5,208-file tree is a net
reduction of 440 files from Phase 1 and 438 files from the original baseline.
No published path, product layout, image collection, Wikisource input, format 1
output, or Pages workflow changed.

Unexpected findings were limited to the missing optional historical ZIP, the
now-stale prose-lint explanation that classified the 36 captures by their old
HTML container, and the sandbox's inability to write linked-worktree Git
metadata or execute the shared interpreter without scoped elevation. The lint
explanation and downloader host warning now describe the JSON storage. The
execution environment used command-local `safe.directory` settings only; no
global Git configuration changed.

### Phase 2 authorized scope

Replace `uxlc/in/UXLC-notes/<book>/<page>.html` with one JSON object per populated
book at `uxlc/in/UXLC-notes/<book>.json`, mapping each existing HTML filename to
its complete original HTML string. Preserve UTF-8 round-trip bytes, whitespace,
Unicode sequences, and line endings. Write deterministically ordered keys with
atomic replacement. Migrate only committed captures, entirely offline.

Share storage access among `py/clc/clc_note_pages.py`,
`py/main_clc_download_notes.py`, and `py/main_verify_notes_zip.py`. Preserve
`local_note_prose` and all existing CLI arguments. Load a book once per operation;
make the operation's lifetime explicit so a later operation sees newly written
entries. Preserve already-present behavior and resumable atomic addition of
successful downloads without losing unrelated entries. Missing notes retain
current behavior; malformed JSON or a malformed storage shape must fail.

`Notes.zip` remains a verification aid, never replacement data. Do not run a live
download: `main_clc_download_notes` documents unresolved differences between the
default host's newer template and the committed captures. Missing `Notes.zip`
must not be hidden by a skip or mistaken for permission to download replacements;
the committed Phase 1 oracle provides the required independent baseline.

Acceptance: verify every reconstructed HTML byte and every extracted prose
string; replay the downloader offline over the committed corpus, confirming no
requests for existing entries, successful addition, retries/failures without
lost entries, repeat-run behavior, and merging with unrelated stored entries.
Exercise shared storage through the zip verifier as well as the reader and
downloader. Use a scratch verification archive if the optional frozen archive is
unavailable and clearly distinguish that replay from the historical zip check.
Regenerate `py/main_clc.py all`, compare all its output paths and bytes, run
relevant checks, Black on changed Python, and the full suite. Update this plan,
commit locally, verify clean status and ancestry, then create only Phase 3 last.

## Phase 3: historical release archives

Replace each historical commit directory with
`MAM-parsed/historical/<full-source-commit>.zip`. Use uncompressed ZIP storage,
sorted member names, fixed timestamps and fixed platform/permission metadata.
Preserve each original `plus/...` member name and exact bytes. Add an explicit
binary Git attribute for these archives. Preserve the manifest's full contents,
including source commits, dates, names, sizes, blob identifiers and order.

Adapt `py/mb_diff_mpu/mpplus_revisions.py`, searchable anchor `class Revision`,
to read archives directly without extraction. Preserve `filenames()`, `read()`,
revision resolution, ordering, ordinary CLI behavior, source dates, and explicit
legacy-history behavior. Missing/corrupt archives and duplicate/missing members
must fail. Check the complete declared member set, including unlisted members.
Keep current-repository Git refs and the optional `legacy:` reader working.

Acceptance: verify all members against the immutable Phase 1 manifest's names,
sizes, and Git blob identities; verify archive metadata and deterministic output.
Regenerate `py/main_diff.py mpp --all`, compare every change-log output against
Phase 1, run relevant checks, Black on changed Python, and the full suite.
Update the historical README to describe the final storage. Update this plan,
commit locally, verify clean status and ancestry, then create only Phase 4 last.

## Phase 4: Job chapter modules

Replace the individual `py/author_boj_qr/qr_*.py` record modules with chapter
modules `qr_CC.py` for the populated chapters. Preserve every `RECORD_*`
identifier, expression, comment, value, and the exact `RAW_QUIRKRECS` order.
Combine identical imports. Rename conflicting helper bindings using the
originating record identifier and update all references; do not use a binding
from a neighboring record merely because the identifier matches.

Update `py/author_boj_util/job_quirkrecs.py` imports. Adapt
`py/check_qr_consistency.py` to inspect **every record assignment** for chapter
agreement, record identifiers, verse values, and word-ID suffixes. Empty
discovery and duplicate identifiers must fail. Preserve relation checks and
generated detail-page names. Do not retain compatibility record modules.

Acceptance: compare the complete ordered type-tagged records to Phase 1, and
compare original source expressions/comments to their new locations, accounting
explicitly for necessary helper renames and import consolidation. Regenerate
`py/main_gen_misc_authored_english_documents.py`; compare all output paths and
bytes. Run `py/check_all.py`, relevant checks, Black on changed Python, and the
full suite. Apply hebrew-prose to any prose change. Update this plan, commit
locally, verify clean status and ancestry, then create only Phase 5 last.

## Phase 5: combined verification from a fresh checkout

Start from a fresh checkout containing the committed result of Phases 2 through
4. Verify the source commit and ancestry before work. Run without migration
scratch files or extracted archives. Use only committed inputs, the shared
interpreter, and the declared sibling inputs. Run all affected generators,
whole-corpus comparisons described above, source checks, and the full suite.
Account for every changed file and verify preserved contents, commands, products,
detail-page names, and published URLs. Compare directory/path sets as well as
file hashes; old URLs must not disappear behind matching surviving files.

Commit only necessary fixes and a compact verification receipt in this plan.
Verify clean status and ancestry, then create only Phase 6 last. The Phase 6
prompt must identify the exact verified combined commit for benchmarking.

## Phase 6: benchmark and close-out

Use baseline `dc043165f98b8a75ee3faa34314b70d0b2171a8f` and the exact completed
commit verified by Phase 5. Create three fresh detached benchmark worktrees per
revision, alternating baseline/completed revisions. Use the same disk, Git
configuration, and parent directory for all trials. A suitable task-owned parent
is `C:/Users/BenDe/.codex/worktrees/<phase-6-id>/MAM-basics/.novc/worktree-file-benchmark`;
resolve and record its concrete absolute path before running. Every trial uses
a new child path that does not already exist.

Write a narrowly scoped scratch Python driver using `time.perf_counter()` around
`subprocess.run(["git", "worktree", "add", "--detach", fresh_path, commit],
check=True, ...)`. Retain each command, revision, path, output, and duration.
Run no generators or archive extraction during creation. Record Git version,
relevant Git configuration, order of trials, and any environmental interruption.
Do not clear caches or change configuration between trials. Report the individual
durations, median, range, and tracked-file count for each revision, with all
support-file additions included in the final count.

Remove only verified clean benchmark worktrees, without force. Verify their
resolved absolute paths are children of the recorded benchmark parent, their
commits match the recorded trials, and their Git status is empty. Remove from
outside the target directories using `git worktree remove <exact-path>`; never
recursively delete a computed Windows path. Do not remove any live task's
worktree or branch. No `.venv` link may exist in a benchmark worktree.

Report measured improvement. If the distributions overlap substantially, state
that a speedup has not been demonstrated. Commit the benchmark record and finish
this plan's status. Do not substitute the predicted file-count reduction for a
timing measurement. No successor phase is needed after Phase 6.

## Commit, successor, and archival integration discipline

Before each commit, confirm HEAD still contains the verified starting commit,
read `git status --porcelain`, stage only intended paths, and inspect the staged
diff. Run applicable prose/source checks and:

```powershell
git diff --cached --check
```

Write a unique commit-message file under `.novc/`, including a Codex
co-authorship trailer, and commit with `git commit -F <absolute-message-path>`.
Confirm the checkout is clean at the resulting local phase commit before
creating the successor. Pass the exact source path, branch, commit, plan path,
phase scope, and verification/integration responsibilities in the new prompt.
Do not push a routine worktree branch or merge it just to create a successor.

Integration is scheduled immediately before the responsible task is archived,
or earlier only when Ben asks or a concrete dependency requires it. Once both
trees are clean, follow the live user-wide four-step rule:

1. Merge current `main` into the worktree branch with `git merge --no-edit main`.
   Resolve conflicts and commit fixes in the worktree.
2. Run the suite in the worktree with `REPOS_ROOT` set. Verify the merged tree,
   including affected generators if integration changes their inputs or code.
3. In `C:/Users/BenDe/GitRepos/MAM-basics`, fast-forward `main` with
   `git merge --ff-only <verified-worktree-branch>`. If it refuses because `main`
   advanced, return to step 1. Do not create a merge in the primary checkout.
4. Push `main` normally. Report the clean worktree, branch head, and pushed main
   head as evidence. Leave worktree removal and branch deletion to the authorized
   post-session cleanup; history rewriting and discarding work still require Ben.
