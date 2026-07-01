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
