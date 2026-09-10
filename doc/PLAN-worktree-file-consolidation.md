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
| 3 | Historical snapshots | Complete at `32fa7da66ef6174f2459e23afc2d28baab5c6f07` in the Phase 3 branch described below |
| 4 | Job records | Complete at `f5d060d2faa32e4d1f7de36aee5922562a4d0e8d` in the Phase 4 branch described below |
| 5 | Combined verification | Complete in the Phase 5 branch described below; result commit is identified by the Phase 6 handoff |
| 6 | Benchmark and close-out | Complete in the Phase 6 branch described below; the timing did not demonstrate a speedup |

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

### Phase 3 execution receipt

Phase 3 task: `01a08c92-d999-70f1-8809-72c8a1c4406f`. Its verified
development checkout is
`C:/Users/BenDe/.codex/worktrees/3169/MAM-basics`, on branch
`codex-worktree-3169`. The checkout started clean and detached at the exact
Phase 2 commit `09d008809cd0a79267ea790b0b126e9f2af98f3c`; the branch did not
exist elsewhere and was created at that commit before implementation. The
required Phase 1 commit `b080a01a87f29f2140144a1247c45c654d240224` is an
ancestor. The Phase 2 predecessor remained HEAD through implementation and all
pre-documentation verification. At the startup measurement, `main` and
`origin/main` were both `31318dd4b68065efe515b478e10d4bff2c72053e`.

The Phase 3 result commit is
`32fa7da66ef6174f2459e23afc2d28baab5c6f07`. Phase 4 verified that exact
commit as its clean starting HEAD and verified the Phase 2 and Phase 1 commits
as ancestors. Re-establish the Phase 3 result independently with:

```powershell
git -C C:/Users/BenDe/.codex/worktrees/3169/MAM-basics log -1 --format=%H -- MAM-parsed/historical py/mb_diff_mpu/mpplus_revisions.py
```

The immutable evidence file retained SHA-256
`f04b2d9f0e60ed35794218c444bb88ea4ec5245302efcbe71c049d413d60c3fa`.
The historical manifest remained byte-identical to Phase 1, with SHA-256
`235bb25d08280667a0d2f9b2097524a2f58bc9a9d4d0e3683959385dadcc908c`.
Its complete revision order, member order, dates, paths, sizes, Git blob
identifiers, commit distances, source repository, and migration object are
unchanged.

Startup remeasurement found 5,208 tracked files. The historical tree had 146
tracked files: `README.md`, `manifest.json`, and 144 data files in six source
commit directories. Each source commit had 24 manifest-listed files. Every
source file matched the size and Git blob named by the Phase 1 manifest. Phase 3
replaces the 144 data files with six archives, producing 5,070 tracked files: a
reduction of 138 from Phase 2, 578 from the Phase 1 tree, and 576 from the
original 5,646-file baseline.

Each archive was built twice before the source directories were removed, and
the two complete byte strings matched. An independent post-removal build from
the Phase 1 Git blobs also matched each archive byte for byte. All 144 archive
members retain their original `plus/...` names, ordering from the manifest at
the reader boundary, and exact bytes. The six archives contain 84,572,003 member
bytes and 84,589,095 total archive bytes. The archive members use `ZIP_STORED`,
sorted names, the fixed timestamp 1980-01-01 00:00:00, Unix creator metadata,
mode 100644, and empty comments and extra fields.

| Source commit | Members | Archive bytes | Archive SHA-256 |
| --- | ---: | ---: | --- |
| `b5e8f942c62574647a7ec14b15fdeba52107e840` | 24 | 12,724,353 | `66f7ddcbe383b3dbedf97229a0e45f4d89358e54c7edca2bba7e3050e05a3ed9` |
| `3d5ecfd83f9a6e943f51e3d316b8345b762aa483` | 24 | 15,329,458 | `4277e65a695db890064ed1ee66d719e34c47feb79820c605acd959a67e36c8e1` |
| `049e636beeaee721f64fd958f670ffe29a9f1e5c` | 24 | 15,238,479 | `235e313ead3b027e7a95d2d5f204b8b202272071774c5df19042086a496c3b9a` |
| `cc43fe04ebc01122de1082cd4ea849fb657d528f` | 24 | 15,298,161 | `2d80271e019d70588e40a9d06e7af991fa6b3e434871c52e1bf76a3bb6544179` |
| `1880cbbda9a769c90126f74cf4c406452af5b209` | 24 | 12,993,464 | `eaebf98a9e3b7d38cad791da84315a5bcc3d3cff5b9a835fe9ed7db905fb74fb` |
| `9ce6ee5d2d611f034208bd2a72d8acb064dd5f19` | 24 | 13,005,180 | `73b17cbc962d2b08185ef63eafa60cae7dab88aacc47bd8d5750eae7a383a0dc` |

`Revision` now reads stored members directly from the archives without
extraction. It preserves manifest filename order, returned UTF-8 text, source
dates, stored-revision abbreviation resolution, the migration-source mapping,
current MAM-basics refs, and explicit `legacy:` reads. Archive validation rejects
a missing archive, a corrupt archive or member, duplicate members, unlisted
members, manifest-listed missing members, duplicate manifest paths, unsorted
members, and noncanonical archive metadata. A scratch Git repository verified
the actual read-only `legacy:` path, date, filenames, text, and commit-distance
behavior. No external MAM-parsed clone was required or read.

The real `py/main_diff.py mpp --all` command completed in 5.43 seconds with the same five named
release comparisons and the same unpinned comparison. All 13 change-log outputs
matched the saved Phase 1 sizes and SHA-256 values, and Git status was unchanged.
The relevant tests passed 30 of 30. `py/check_all.py` reported all 7 checks
passed. The prose mark-order and Latin-diacritic hygiene selection passed 7 of
7. The full suite reported **989 passed, 5 skipped, 65 subtests passed** in
109.72 seconds; the five skips remain the expected edition-transcription
differences. Python was 3.13.15 and Git was 2.43.0.windows.1.

Commands ran from the verified Phase 3 worktree. Commands that invoked Git from
Python used a process-local `safe.directory` entry for that worktree. The exact
commands were:

| Purpose | Command |
| --- | --- |
| Build every archive twice from the verified source directories | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/build_historical_archives_phase3.py` |
| Verify members, metadata, deterministic reconstruction, failures, current refs, and legacy reads | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/verify_historical_archives_phase3.py` |
| Regenerate and compare every change-log output | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/run_and_verify_mpp_phase3.py` |
| Run the focused MPP tests | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider py/tests/test_mpplus_extract.py py/tests/test_diff_mpp_unpinned_latest.py` |
| Run all source and HTML checks | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/check_all.py` |
| Check changed prose and Latin-diacritic hygiene | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider py/tests/test_prose_mark_order.py py/tests/test_h_dot_below_nfc.py` |
| Run the full suite | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider` |

The shared interpreter and linked-worktree Git metadata required scoped
elevation in the desktop sandbox. Scratch-verifier assumptions were
corrected without tracked-data consequences: the evidence names its historical
count `verified_members`, and the longstanding current-ref Git reader strips
surrounding whitespace. A repeated verifier run could not delete an earlier
elevated scratch Git repository because Windows assigned its object files to the
desktop owner account; later runs use unique task-local scratch directories.
These are execution-environment findings, not repository defects.

No published path, product layout, image collection, Wikisource input, format 1
output, Pages workflow, or MAM-private input changed. Phase 3 did not read
MAM-private. The Phase 4 task must record its returned task ID, allocated
checkout, branch, and exact Phase 3 predecessor in this receipt after verifying
them; Phase 3 creates that task only after its result is committed and clean.

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

### Phase 4 execution receipt

Phase 4 task: `01a08cb2-16f0-7520-9ae4-67b1e8dae669`, titled
**Consolidate Job record modules**. Its verified development checkout is
`C:/Users/BenDe/.codex/worktrees/ffc9/MAM-basics`, on branch
`codex-worktree-ffc9`. The checkout started clean and detached at the exact
Phase 3 commit `32fa7da66ef6174f2459e23afc2d28baab5c6f07`; the branch did not
exist elsewhere and was created at that commit before implementation. The
Phase 2 commit `09d008809cd0a79267ea790b0b126e9f2af98f3c` and Phase 1 commit
`b080a01a87f29f2140144a1247c45c654d240224` are ancestors. At startup,
`main` and `origin/main` were both
`31318dd4b68065efe515b478e10d4bff2c72053e`.

The Phase 4 result commit is
`f5d060d2faa32e4d1f7de36aee5922562a4d0e8d`. Phase 5 task
`01a08cd3-ea1e-7ac0-89c9-470efdb93ee2`, titled **Verify combined file
consolidation**, verified that exact commit as its clean detached starting HEAD
in `C:/Users/BenDe/.codex/worktrees/3f2e/MAM-basics`, then created branch
`codex-worktree-3f2e` at that commit. Re-establish the Phase 4 result
independently with:

```powershell
git -C C:/Users/BenDe/.codex/worktrees/ffc9/MAM-basics log -1 --format=%H -- py/author_boj_qr py/author_boj_util/job_quirkrecs.py py/check_qr_consistency.py
```

The immutable Phase 1 evidence retained SHA-256
`f04b2d9f0e60ed35794218c444bb88ea4ec5245302efcbe71c049d413d60c3fa`.
Phase 4 replaced 160 per-record modules with 39 populated-chapter modules.
The replacement preserves all 160 `RECORD_*` assignments in exact loader
order. It preserves all 278 original top-level assignment source segments and
all 74 comment tokens in source order, apart from the seven necessary helper
renames named below. Import consolidation reduced 91 original import statements
to 67 equivalent grouped imports.

Seven colliding helpers in four records gained record-qualified names:

1. Record `1916_BMV0PY` uses `_GENCOM_PARA_1_1916_BMV0PY`,
   `_GENCOM_PARA_2_1916_BMV0PY`, and `_GENCOM_PARA_3_1916_BMV0PY`.
2. Record `3422` uses `_COMMENT_PARA1_3422`.
3. Record `3433_HM3M5` uses `_COMMENT_PARA2_3433_HM3M5` and
   `_COMMENT_PARA3_3433_HM3M5`.
4. Record `3913` uses `_COMMENT_3913`.

The complete recursively type-tagged runtime sequence has SHA-256
`380d32bc7114735166e07cc77bdcab11eebff6500d5106d138ef99ae6efff95b`,
the Phase 1 value. Every individual record hash, dictionary key and value order,
list and tuple order, value, and Python type matches Phase 1. The aggregate
recursive value counts remain 21 booleans, 870 dictionaries, 1,005 integers,
393 lists, 5,897 strings, and 4 tuples.

`job_quirkrecs.py` now imports the 39 chapter modules and constructs
`RAW_QUIRKRECS` in the original record order. `check_qr_consistency.py` now
discovers only exact `qr_CC.py` chapter names and inspects every record
assignment for identifier, chapter, verse, and word-ID agreement. It also
rejects empty discovery, duplicate file discovery, duplicate record identifiers,
and malformed filenames. Four independent negative probes exercised those four
failure classes. The existing cross-record relation remained valid.

The real `py/main_gen_misc_authored_english_documents.py` command completed in
5.34 seconds. All 183 declared outputs matched the Phase 1 path set and SHA-256
values, including all 160 Job detail pages, and Git status was unchanged. The
QR consistency check passed all 39 chapter modules and 160 records in 0.15
seconds. The one relation passed in 0.40 seconds. `py/check_all.py` reported all
7 checks passed in 3.82 seconds. The prose mark-order and Latin-diacritic hygiene
selection passed 7 of 7 both before and after the receipt edit; one
post-receipt run took 14.91 seconds. Black 26.5.1 left all 43 changed Python
files unchanged.

The first full-suite run occurred before the replacement directory was staged.
The sibling-reach lint obtains its path set from `git ls-files`, so that run
passed 987 tests and then reported two `FileNotFoundError` failures while the
index still named the deleted per-record files. This was a verification-order
finding, not a source defect: staging only `py/author_boj_qr/` made the index
describe the intended tree. The focused sibling-reach selection then passed 2
of 2 in 4.20 seconds. The complete rerun reported **989 passed, 5 skipped, 65
subtests passed** in 100.47 seconds, with unchanged Git status.

The staged tree contains 4,949 tracked files. That is 121 fewer than Phase 3,
699 fewer than Phase 1, and 697 fewer than the original 5,646-file baseline.
The three consolidation phases themselves removed the estimated 700 storage
files; the programme added three durable support files: the plan, immutable
evidence, and `py/clc/clc_note_storage.py`.

Commands ran from the verified Phase 4 worktree with
`REPOS_ROOT=C:/Users/BenDe/GitRepos`. The exact principal commands were:

| Purpose | Command |
| --- | --- |
| Compare sources, comments, imports, runtime values and failure probes | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/verify_job_records_phase4.py` |
| Regenerate and compare all authored-English outputs | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_gen_misc_authored_english_documents.py` |
| Check every chapter module and record | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/check_qr_consistency.py` |
| Check cross-record relations | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/check_qr_relations.py` |
| Run all source and HTML checks | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/check_all.py` |
| Check changed prose and Latin-diacritic hygiene | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider py/tests/test_prose_mark_order.py py/tests/test_h_dot_below_nfc.py` |
| Recheck the tracked-file scanner after staging the replacement directory | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider py/tests/test_sibling_reach.py` |
| Run the full suite | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider` |

The shared interpreter and linked-worktree Git metadata required scoped
elevation in the desktop sandbox. Git commands also used a process-local
`safe.directory` entry for this worktree. At the pre-receipt check, the primary
clone carried four in-progress paths owned by the unrelated Phase 6E publication
and vendoring task `01a08c94-01be-73d0-9d6a-29a5664a9585`; Phase 4 left all
four paths untouched. No published path, generated output, product layout,
image collection, Wikisource input, historical archive, Pages workflow, or
MAM-private content changed. Phase 4 performed no integration or push. The
Phase 5 task must record its returned task ID, allocated checkout, branch, and
exact Phase 4 predecessor in this receipt after verifying them; Phase 4 creates
that task only after its result is committed and clean.

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

### Phase 5 execution receipt

Phase 5 task: `01a08cd3-ea1e-7ac0-89c9-470efdb93ee2`, titled **Verify
combined file consolidation**. Its verified development checkout is
`C:/Users/BenDe/.codex/worktrees/3f2e/MAM-basics`, on branch
`codex-worktree-3f2e`. The checkout started clean and detached at the exact
Phase 4 commit `f5d060d2faa32e4d1f7de36aee5922562a4d0e8d`; the branch did not
exist elsewhere and was created at that commit before verification. Phase 3
`32fa7da66ef6174f2459e23afc2d28baab5c6f07`, Phase 2
`09d008809cd0a79267ea790b0b126e9f2af98f3c`, and Phase 1
`b080a01a87f29f2140144a1247c45c654d240224` are ancestors. At the
pre-receipt measurement, `main`, `origin/main`, and the primary checkout were
all `3e3a93ef82615710a2520bd85a3086e9ae4fbc9d`. The primary checkout's
three in-progress paths belong to the unrelated Phase 6E publication and
vendoring task; Phase 5 left them untouched. The declared MAM-private sibling
input was clean at `55252b834d28a6c241e75758aff5d15836621f56`.

The immutable evidence file is 154,023 bytes and retains compressed SHA-256
`f04b2d9f0e60ed35794218c444bb88ea4ec5245302efcbe71c049d413d60c3fa`.
The baseline commit contains 5,646 tracked files and 831,571,756 Git blob
bytes. The Phase 4 commit contains 4,949 tracked files and 831,863,819 Git blob
bytes: 697 fewer files than the baseline. The compact-JSON SHA-256 of the
sorted tracked path list is
`17c0ca43ef4a15a5e33ba72e94d78d78882b5f666ecca439eb7313a5c6a4f40d`
at the baseline and
`c1e10f7d9933d530e198c7e3a1836d39bdd9280e672193c954d2cfd754fbd4eb`
at Phase 4. Directory prefixes fell from 356 to 308. The removed set is
exactly the 36 old UXLC note-book directories and the twelve historical
revision/`plus` directories. The compact-JSON SHA-256 values of the sorted
directory-path sets are
`f8ccdbbff161d3bf32ea9702017991f67c6d462368d34f04b6c22e6e73cac319`
and `4d686e010dc06e5f45f36a55e931f171f7f9eef28be7a1d95c3001e684353499`.

All 881 baseline-to-Phase-4 path changes are accounted for:

| Change group | Paths |
| --- | ---: |
| Deleted UXLC note pages | 477 |
| Added per-book UXLC note objects | 36 |
| Deleted historical JSON members | 144 |
| Added historical ZIP archives | 6 |
| Deleted per-record Job modules | 160 |
| Added Job chapter modules | 39 |
| Added plan, evidence, and note-storage support files | 3 |
| Modified files named below | 16 |

The modified files divide by consolidation phase:

| Phase | Modified paths |
| --- | --- |
| 2 | `py/clc/clc_collect.py`, `py/clc/clc_note_pages.py`, `py/main_clc_download_notes.py`, `py/main_verify_notes_zip.py`, `py/tests/clc_note_pages_test.py`, `py/tests/test_prose_mark_order.py`, `py/uxlc_misc/my_uxlc.py`, `py/uxlc_paths.py` |
| 3 | `.gitattributes`, `MAM-parsed/historical/README.md`, `py/mb_diff_mpu/mpplus_revisions.py` |
| 4 | `doc/boj-quirkrec-comments.md`, `py/author_boj_util/job_quirkrecs.py`, `py/boj_paths.py`, `py/check_all.py`, `py/check_qr_consistency.py` |

The 36 note JSON objects reconstruct the complete 477-path corpus and all
925,517 source bytes. Every size, SHA-256, Git blob identity, and extracted
prose string matches the immutable evidence. The compact-JSON SHA-256 of the
sorted `[path, size, SHA-256]` rows is
`d131832ed3b052757877f5d9c3d9c6cf1bdd6d2e5b30b349c97ad2ed2b73f7e0`.
Two reads through one operation loaded their book once. An existing page made
zero requests; a successful addition made one request, retained an unrelated
entry, preserved CRLF-bearing non-ASCII HTML and sorted keys, and was visible
to a fresh operation; its repeat made zero requests. A failed request and a
simulated atomic-write failure left bytes and cache unchanged. Six malformed
or unexpected storage shapes failed, while an absent key returned `None`.
The production ZIP verifier, run against a fresh replay archive made from the
committed objects, reported 477 `IDENTICAL` and zero
`NO-PROSE-EXTRACTED`.

The historical manifest retains SHA-256
`235bb25d08280667a0d2f9b2097524a2f58bc9a9d4d0e3683959385dadcc908c`
and matches the complete evidence object. The six archives contain all 144
declared members and 84,572,003 member bytes in 84,589,095 archive bytes.
Every name, manifest order at the reader boundary, sorted archive order, size,
Git blob identity, byte string, timestamp, storage method, creator platform,
permission mode, and empty metadata field matches. Independently rebuilding
every archive from the baseline Git blobs produced the exact committed bytes:

| Source commit | Members | Archive bytes | Archive SHA-256 |
| --- | ---: | ---: | --- |
| `b5e8f942c62574647a7ec14b15fdeba52107e840` | 24 | 12,724,353 | `66f7ddcbe383b3dbedf97229a0e45f4d89358e54c7edca2bba7e3050e05a3ed9` |
| `3d5ecfd83f9a6e943f51e3d316b8345b762aa483` | 24 | 15,329,458 | `4277e65a695db890064ed1ee66d719e34c47feb79820c605acd959a67e36c8e1` |
| `049e636beeaee721f64fd958f670ffe29a9f1e5c` | 24 | 15,238,479 | `235e313ead3b027e7a95d2d5f204b8b202272071774c5df19042086a496c3b9a` |
| `cc43fe04ebc01122de1082cd4ea849fb657d528f` | 24 | 15,298,161 | `2d80271e019d70588e40a9d06e7af991fa6b3e434871c52e1bf76a3bb6544179` |
| `1880cbbda9a769c90126f74cf4c406452af5b209` | 24 | 12,993,464 | `eaebf98a9e3b7d38cad791da84315a5bcc3d3cff5b9a835fe9ed7db905fb74fb` |
| `9ce6ee5d2d611f034208bd2a72d8acb064dd5f19` | 24 | 13,005,180 | `73b17cbc962d2b08185ef63eafa60cae7dab88aacc47bd8d5750eae7a383a0dc` |

Eleven independent negative probes rejected a missing or corrupt archive,
duplicate, missing, unlisted or unsorted members, noncanonical member metadata,
an archive comment, duplicate manifest paths, an unlisted read, and invalid
UTF-8. All six stored revisions resolved by full and abbreviated commit,
reported their declared dates and commit distances, and returned all 24 files'
exact bytes. `HEAD` resolved to the Phase 4 commit with 24 current files. The
migration source `51082036e5907991d0d322cb6dfcc6404802099f` resolved to landing
commit `63cf6c98b8c4daba7d0f90c6fa9b0a10b72d9a96` with source date
2026-09-04. A fresh task-local two-commit Git repository verified an explicit
`legacy:` resolution, filename and byte read, and one-newer-commit distance;
no external MAM-parsed clone was read.

The 39 Job chapter modules retain all 160 records in exact
`RAW_QUIRKRECS` order. All 278 original top-level assignment source segments
and all 74 comment tokens match in sequence after the seven recorded helper
renames. The 91 original import statements reduce to 67 grouped statements
with the exact same imported binding set. The recursively typed value tree,
every individual record hash, dictionary key/value order, list and tuple order,
value, and Python type match. The whole sequence retains SHA-256
`380d32bc7114735166e07cc77bdcab11eebff6500d5106d138ef99ae6efff95b`.
The remeasured recursive totals are 21 booleans, 870 dictionaries, 1,005
integers, 393 lists, 5,897 strings, and 4 tuples. All 160 original Job detail
page paths remain present; their sorted path-list SHA-256 is
`244a97e5a7a3160d69939771283a67a2d14d6d867f26ad3933e36e557aa8a0da`.

Every one of the baseline's 1,859 published `gh-pages/` paths and Git blobs is
unchanged. The compact-JSON SHA-256 of sorted `[path, Git blob]` rows is
`000b2896e9980df1a5e06dd6d710db91b4143b85b9d599821b6e72a961e6828e`.
The real generators reproduced the complete output path and SHA-256 maps from
Phase 1. The table's combined hashes are SHA-256 values of compact UTF-8 JSON
arrays of sorted `[path, size, SHA-256]` rows:

| Generator or check | Outputs | Combined hash | Wall seconds |
| --- | ---: | --- | ---: |
| `py/main_clc.py all` | 12 | `b2b2372538120680c226575bfd0bcd66e8d99dd8da01e0f95a932c1b6fa98f8e` | 1.059 |
| `py/main_diff.py mpp --all` | 13 | `a8b309adf2676626b10b94c1c9c69f3bcf0fe14522014ca2d210c739a82b0381` | 6.337 |
| `py/main_gen_misc_authored_english_documents.py` | 183 | `91412f37f10f864ca3f0d9501732a1db3c199b1aa10c8e93def5ca2639bf7e5b` | 4.594 |
| `py/check_all.py` | 2 | `e495aee301c42d008482513fda2588e631664e3aba4058975fb2ed69d583d07b` | 2.588 |

The exact commands ran from the Phase 5 worktree with
`REPOS_ROOT=C:/Users/BenDe/GitRepos`, Python 3.13.15, and Git
2.43.0.windows.1. Every row began and ended with empty
`git status --porcelain=v1 --untracked-files=all`; every command exited zero.

| Purpose | Exact command after the worktree cwd | Wall seconds | Result |
| --- | --- | ---: | --- |
| Static corpus, source, inventory, failure, path, and URL verification | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/verify_worktree_file_consolidation_phase5.py static` | 35.264 | passed |
| Regenerate CLC | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_clc.py all` | 1.059 | 12 outputs match |
| Exercise the production notes ZIP verifier | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_verify_notes_zip.py C:/Users/BenDe/.codex/worktrees/3f2e/MAM-basics/.novc/worktree-file-consolidation-phase5/Notes-phase5-replay.zip` | 0.289 | 477 identical; 0 without prose |
| Focused CLC tests | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider py/tests/clc_attribution_test.py py/tests/clc_collect_test.py py/tests/clc_dual_cant_test.py py/tests/clc_kq_test.py py/tests/clc_note_pages_test.py py/tests/clc_versification_test.py` | 1.794 | 45 passed |
| Regenerate MPP change logs | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_diff.py mpp --all` | 6.337 | 13 outputs match |
| Focused MPP tests | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider py/tests/test_mpplus_extract.py py/tests/test_diff_mpp_unpinned_latest.py` | 0.698 | 30 passed |
| Regenerate authored English documents | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_gen_misc_authored_english_documents.py` | 4.594 | 183 outputs match |
| Check Job chapter and record consistency | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/check_qr_consistency.py` | 0.120 | 39 modules and 160 records pass |
| Check Job record relations | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/check_qr_relations.py` | 0.299 | 1 relation passes |
| Check tracked sibling-path reach | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider py/tests/test_sibling_reach.py` | 8.285 | 2 passed |
| Run all source and HTML checks | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/check_all.py` | 2.588 | all 7 checks passed |
| Check prose mark order and Latin-diacritic hygiene | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider py/tests/test_prose_mark_order.py py/tests/test_h_dot_below_nfc.py` | 21.599 | 7 passed |
| Run the full suite | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider` | 113.721 | 989 passed, 5 skipped, 65 subtests passed |
| Recheck all output maps, HEAD, inventory, and status | `C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe .novc/verify_worktree_file_consolidation_phase5.py post` | 0.221 | passed |

Black 26.5.1 formatted the task-local verifier. Phase 5 changed no tracked
Python file, so no tracked Python file required formatting.

Verification found no repository defect and required no consolidation fix.
Three task-local verifier assumptions failed before the final passing run:

1. The evidence stores populated chapter identifiers as zero-padded strings;
   the first draft converted current filenames to integers. The verifier now
   compares the zero-padded identifiers.
2. The evidence's source-blob object is keyed lexicographically, while the
   explicit 160-record list defines loader order. The verifier now orders
   original sources by that explicit list.
3. Git quoted the ḥ in one historical filename and reported 14 deleted Job
   modules as similarity-based renames. The verifier now uses
   `core.quotepath=false` and `--no-renames` for exact path accounting.

No published path, generated output, product layout, image collection,
Wikisource input, historical member, Job record value or prose, format 1
output, Pages workflow, or MAM-private content was expected to change; none
changed. Phase 5 used only committed inputs plus fresh task-local probes, did
not read earlier phase scratch, did not extract a historical archive, and did
not begin Phase 6 benchmarking. Phase 5 performed no integration or push.
The Phase 5 result commit is necessarily not self-identifying inside the commit
that contains this receipt. The Phase 6 creation prompt and Phase 5 final
response carry its full hash, and Phase 6 must verify that exact predecessor.

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

### Phase 6 execution receipt

Phase 6 task: `01a08cf3-20c2-7e91-a4d8-b4430c96c195`. Its verified
development checkout is
`C:/Users/BenDe/.codex/worktrees/3f99/MAM-basics`, on branch
`codex-worktree-3f99`. The checkout started clean and detached at the exact
Phase 5 commit `dbef49317ec91cac1e792e94a9140f7522b38efe`; the required branch
name was unused and was created at that commit before benchmarking. The Phase
4 commit `f5d060d2faa32e4d1f7de36aee5922562a4d0e8d` and baseline
`dc043165f98b8a75ee3faa34314b70d0b2171a8f` are ancestors of the Phase 5
commit.

The benchmark ran on 2026-09-10 under Git 2.43.0.windows.1. All six trials
used the same disk and the resolved task-owned parent
`C:/Users/BenDe/.codex/worktrees/3f99/MAM-basics/.novc/worktree-file-benchmark`.
The task-local driver was
`C:/Users/BenDe/.codex/worktrees/3f99/MAM-basics/.novc/benchmark_worktree_file_consolidation_phase6.py`.
The driver used `time.perf_counter()` immediately around only
`subprocess.run(["git", "worktree", "add", "--detach", fresh_path,
commit], ...)`, captured both output streams, and wrote the complete record
after every trial. It did not clear caches, change persistent Git
configuration, run a generator, extract an archive, or create a `.venv` path.

The baseline commit has 5,646 tracked files. The Phase 5 commit has 4,949
tracked files, including the programme's plan, compact baseline evidence, and
note-storage support module. The completed layout therefore has 697 fewer
tracked files, a 12.3% reduction. Updating this already tracked plan does not
change the 4,949-file count.

The trials alternated baseline and completed revisions. Every child path was
fresh, every command exited zero, and the commands ran in the order shown:

| Order | Revision | Exact child path under the benchmark parent | Seconds |
| ---: | --- | --- | ---: |
| 1 | baseline `dc043165f98b8a75ee3faa34314b70d0b2171a8f` | `baseline-1` | 15.599635 |
| 2 | completed `dbef49317ec91cac1e792e94a9140f7522b38efe` | `completed-1` | 14.537181 |
| 3 | baseline `dc043165f98b8a75ee3faa34314b70d0b2171a8f` | `baseline-2` | 12.721164 |
| 4 | completed `dbef49317ec91cac1e792e94a9140f7522b38efe` | `completed-2` | 15.715834 |
| 5 | baseline `dc043165f98b8a75ee3faa34314b70d0b2171a8f` | `baseline-3` | 20.357231 |
| 6 | completed `dbef49317ec91cac1e792e94a9140f7522b38efe` | `completed-3` | 21.053379 |

Each exact command was `git worktree add --detach <absolute-child-path>
<full-commit>`, with `<absolute-child-path>` equal to the benchmark parent plus
the child name in the table. Baseline stdout was exactly `HEAD is now at
dc043165 Verify Phase 6B parsing, surveys and MAM-simple regeneration`; its
stderr began with `Preparing worktree (detached HEAD dc043165)` and ended with
`Updating files: 100% (5646/5646), done.` Completed stdout was exactly `HEAD
is now at dbef4931 Verify combined worktree file consolidation`; its stderr
began with `Preparing worktree (detached HEAD dbef4931)` and ended with
`Updating files: 100% (4949/4949), done.` The task-local result file retains
every intermediate progress line, exact command array, revision, absolute
path, output stream, return code, and unrounded duration. After verified
cleanup its SHA-256 is
`e5d20129bbf87c509ddf64d540f0e39be67a2741d5b929f2926eaaad55b5d311`.

| Revision | Individual seconds | Median seconds | Range seconds |
| --- | --- | ---: | --- |
| baseline | 15.599635, 12.721164, 20.357231 | 15.599635 | 12.721164–20.357231 |
| completed | 14.537181, 15.715834, 21.053379 | 15.715834 | 14.537181–21.053379 |

The completed median is 0.116199 seconds, or 0.7%, slower than the baseline
median. The ranges overlap from 14.537181 through 20.357231 seconds and the
within-revision variation is much larger than the median difference. These six
trials do not demonstrate either a speedup or a regression. The tracked-file
reduction is established independently, but it is not a substitute for the
timing result.

Relevant Git configuration stayed fixed: system `core.autocrlf=true`, system
`core.fscache=true`, repository `core.filemode=false`, repository
`core.ignorecase=true`, system and repository `core.symlinks=false`, and
repository `extensions.worktreeconfig=true`. The selected `core.eol`,
`core.safecrlf`, `core.longpaths`, `core.preloadindex`,
`core.untrackedcache`, `core.sparsecheckout`, `core.sparsecheckoutcone`,
`index.threads`, `checkout.workers`, `checkout.thresholdforparallelism`,
`feature.manyfiles`, and `submodule.recurse` values were unset. A process-local
`safe.directory` value named only the verified Phase 6 checkout because the
desktop sandbox account could not otherwise use the linked repository; no
global Git configuration changed.

No trial failed or had a user-driven interruption. The before/after worktree
records nevertheless show concurrent activity in two unrelated worktrees:
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/eloquent-ritchie-0e4c6c`
advanced from `a8c9fe619409466560a1823847c1e4c4e7ed96d5` to
`29bcdbe023f3b42f1bb7405db666737470b071f6`, and
`C:/Users/BenDe/GitRepos/MAM-basics/.claude/worktrees/mega-coverage` advanced
from `9dba5d4ff579ea56ed5566a13f5a00988eca3772` to
`7509c388462f5f7f9ab02d38a8a5516c9018062b`. That concurrent repository and
disk activity, the deliberately uncontrolled filesystem cache, and the sample
of only three trials per revision limit the timing conclusion.

Before cleanup, the driver resolved each recorded child and required the path
to be a direct child of the recorded benchmark parent. It verified the exact
trial commit, empty `git status --porcelain=v1 --untracked-files=all`, and the
absence of any `.venv` path. It then ran plain `git worktree remove
<exact-absolute-path>` from the Phase 6 checkout, without `--force`. All six
removals exited zero with empty stdout and stderr. Each child path was absent
and each registration was absent immediately after removal; the final `git
worktree list --porcelain` names no benchmark child. The cleanup command
completed in 14.604 seconds. No live task worktree or branch was removed or
modified.

After the receipt edit, the applicable prose mark-order and Latin-diacritic
hygiene selection passed 7 of 7 in 53.25 seconds reported by pytest and
54.707450 wall seconds. The command ran from the Phase 6 checkout with
`REPOS_ROOT=C:/Users/BenDe/GitRepos`:

```powershell
C:/Users/BenDe/GitRepos/MAM-basics/.venv/Scripts/python.exe py/main_test.py -q -p no:cacheprovider py/tests/test_prose_mark_order.py py/tests/test_h_dot_below_nfc.py
```

The programme is complete. Phase 6 changes only this plan, creates no successor
task, and performs no merge or push before archival-time integration. Ben's
corrected handoff decision, 2026-09-10: Phase 6 task
`01a08cf3-20c2-7e91-a4d8-b4430c96c195` owns archival-time integration of
the complete Phase 6 branch. When Ben asks whether Phase 6 can be archived,
merge current `main` into `codex-worktree-3f99`, run the required suite in the
Phase 6 worktree with `REPOS_ROOT=C:/Users/BenDe/GitRepos`, fast-forward
primary `main` to the verified Phase 6 branch, and push `main`. If `main`
advances before the fast-forward, return to the merge-and-verification step.
Report the clean Phase 6 worktree, Phase 6 branch head, and pushed `main` head.
Phase 5 task `01a08cd3-ea1e-7ac0-89c9-470efdb93ee2` no longer owns
integration and may be archived after this correction.

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
