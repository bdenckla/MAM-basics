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

**`py/main_test.py` is the only runner — a bare `pytest` is not supported from anywhere,
including the repo root.** `fd2241a` migrated this repo onto that single entrypoint on
purpose. It needs no path configuration because CPython prepends a script's own directory
to `sys.path`, which is exactly why the entrypoint lives in `py/` and not at the root. So
`pytest py/tests` failing with ~34 `ModuleNotFoundError` collection errors (`No module
named 'mb_author'`, ...) is the designed state, not a defect: **do not "fix" it** with a
`pytest.ini` `pythonpath`, a root `conftest.py`, a `.pth`, or `PYTHONPATH`. Each re-creates
the second entrypoint the migration removed. This was reported as a bug on 2026-07-30 and
the report was wrong. The cross-repo rule is user-level CLAUDE.md's "No `sys.path` surgery"
section, which this repo is the worked example for — it is what settled the standard at zero
inserts per repo rather than one. `py/versification_and_cantillation/doc.py`'s module
docstring says the same thing.

**There is no test registry any more, and no file to add a new test to.** `main_test.py`
was a hand-maintained `TEST_MODULE_SPECS` tuple plus a `unittest` loader until 2026-08-01;
it is now a `pytest.main()` wrapper, so pytest discovers `py/tests/test_*.py` itself. Drop
a new test file in and it runs. The registry is gone because of the failure mode it had:
an unregistered file does not skip, it reports nothing at all — worse than the silent-green
skip the global rules warn about — and two files went unrun that way here from the
2026-05-03 migration until 2026-07-30, one of them edited four times meanwhile.

Arguments pass straight through to pytest, so `-k`, `-x`, `-q`, `--lf` and `--collect-only`
all work; naming a file replaces the default target of the whole `py/tests` tree:

```bash
.venv/Scripts/python.exe py/main_test.py --collect-only -q
```

Both test styles collect natively — this repo's `unittest.TestCase` classes and the
module-level `def test_` functions that arrived with the wlc-utils code — so no test file
was rewritten in either direction.

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
