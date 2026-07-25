# CLAUDE.md

## Running tests — always from the repo root

Run tests via the canonical entrypoint, from the repo root (`~/GitRepos/MAM-basics`), never from `py/`:

```bash
.venv/Scripts/python.exe py/main_test.py
```

Sibling-repo paths (MAM-parsed, MAM-simple, MAM-with-doc, MAM-OSIS, MAM-for-Sefaria)
are built from `mb_cmn.paths.repo_root()` / `repos_root()` / `sibling_repo(name)` — a
single `__file__`-relative utility (issue #75), not cwd-relative `"../MAM-parsed"`
literals or ad hoc `Path(__file__).resolve().parents[N]` chains. New path-construction
code should use it too. Exception: a handful of files that get vendored/copied verbatim
into sibling repos (`mb_cmn/read_books_from_mam_parsed_plus.py`, `mb_cmn/provenance.py`,
`mb_misc/write_utils.py`, `mb_sefaria/mam4sef_or_ajf.py`) intentionally keep their
existing cwd-relative or self-contained `__file__`-relative logic instead, so they stay
portable when copied elsewhere without also requiring `mb_cmn/paths.py` to travel with them.

Even so, still run from the repo root, never from `py/`: some in-repo paths (e.g.
`in/mam-ws-bot-edits/...`) remain cwd-relative by design, and the venv itself
(`.venv/Scripts/python.exe`) is a repo-root-relative path. Running pytest from `py/`
(e.g. `cd py && pytest tests/`) breaks these with a plain `FileNotFoundError`, which reads
as a real test failure rather than a wrong-invocation-directory error. On 2026-07-01 this
exact mistake produced 17 misleading test failures that got misdiagnosed as
pre-existing/unrelated bugs.

If a shell has already `cd`'d into `py/` from an earlier command, explicitly `cd` back to
the repo root before running tests — a persistent-cwd shell keeps resolving
repo-root-relative paths wrong otherwise.

## Writing tests — differential and lint-shaped only

An audit of git history, comments, and issues across all of Ben's repos (2026-07-25) found
four occasions where a test demonstrably found something, and **zero** recorded cases of a
pre-existing example-based unit test failing later and thereby catching a regression. All
four have one of two shapes. Do not add a test unless it is one of them, or Ben asks.

- **A differential check against an independent oracle** — regenerate the corpus and compare
  against a frozen reference or a second derivation of the same fact.
- **A mechanical lint over the tree** — a decidable property of the *source text* rather than
  of behavior (`py/tests/test_h_dot_below_nfc.py` and the `check_repo_standards.py` scans are
  this shape).

Otherwise the generated, git-tracked artifact is the test: regenerate it with the real command
and read the diff. Unexplained diffs are failures until explained. This is how the real bugs
here were actually found — `1ef8f51` (#199, a top-level ketiv/qere silently dropped from a
strand) surfaced as wrong text in generated output, not as a red test.

Do not write an example-based unit test that pins one hand-picked case, a string, or a name.
Nothing in the record shows one catching anything, and they have to be dragged through every
terminology rename.

**The `ws_bot` tests are a deliberate exception.** A Wikisource edit is an irreversible,
outward-facing action against a live wiki, and there is no regeneratable artifact to diff
after the fact — so pinning an edit payload before it is sent is worth its cost on those
grounds, not because the general rule has an escape hatch.

The fullest statement of this rule, with the evidence behind it, is in the sibling repo:
`wlc-utils/doc/agent-planning-principles.md` §"Generated Outputs Are the Tests".

Note that this belongs in **`CLAUDE.md`**, the file you are reading — not in the *disabled*
`CLAUDE-disabled.md` / `.github/copilot-instructions-disabled.md`, which do not load.
