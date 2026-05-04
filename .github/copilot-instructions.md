# Copilot Instructions for MAM-basics

## Book Names and Identifiers

- Reuse already-defined book names and identifiers whenever possible.
- Prefer canonical symbolic book ids from shared code, such as `1Samuel` and `Levit`, even in display contexts unless the user explicitly asks otherwise.
- Do not invent a new parallel set of book names that is more verbose, more abbreviated, or only slightly different from existing names.
- When a book-name mapping is genuinely needed, derive it from existing shared definitions in `mb_cmn` or another established module rather than hard-coding a fresh local mapping.

## Python Environment — MANDATORY venv-qualified commands

Always use `.venv/` for Python work. **Never run bare `python`, `python3`, `pip`, or `pip3`** — always use the explicit venv path:

- **Windows:** `.venv\Scripts\python.exe` / `.venv\Scripts\pip.exe`
- **Linux/macOS:** `.venv/bin/python` / `.venv/bin/pip`

This rule applies everywhere — terminal, chat examples, documentation. No exceptions.

## Running Python Main Scripts — Always From the Repo Root

For execution, all `py/main_*.py` scripts use paths like `../MAM-parsed` that are relative to the **repo root**. Always run from the repo root:

```
.venv\Scripts\python.exe py\main_mam_simple.py
```

Do not `cd` into `py/` before running — `../MAM-parsed` would then resolve to the wrong location.

## Running Tests — Canonical Harness

Use `py/main_test.py` as the canonical test entrypoint. Test modules now live under `py/tests/test_*.py`.

Run all tests from the repo root:

```
.venv\Scripts\python.exe py\main_test.py
```

Run a selected subset with flags (or list available flags):

```
.venv\Scripts\python.exe py\main_test.py --list
.venv\Scripts\python.exe py\main_test.py --ws-urls-encoding
```

## Wikisource Bot Runs — Explicit Pywikibot Config Dir Required

When running `py/main_ws_bot.py real`, always provide the pywikibot config
directory explicitly, either by:

- passing `-dir:<path-to-.pywikibot>` (preferred), or
- setting `PYWIKIBOT_DIR`.

Do not rely on pywikibot defaults. Default discovery can place runtime
artifacts (for example `apicache/` and `throttle.ctrl`) in the current
working directory and can trigger interactive auth prompts that stall
automation.

With an explicit `-dir:` or `PYWIKIBOT_DIR`, those runtime artifacts are
written under that pywikibot base directory instead of whichever working
directory happened to be active (unless you intentionally point `-dir` to
the working directory).

Required command shape (Windows):

```
.venv\Scripts\python.exe py\main_ws_bot.py real --edits <path> -dir:$env:USERPROFILE/.pywikibot
```

Alternative:

```
$env:PYWIKIBOT_DIR = "$env:USERPROFILE/.pywikibot"
.venv\Scripts\python.exe py\main_ws_bot.py real --edits <path>
```

## Temporary Python Scripts

Put reusable Python scripts that should be tracked under `py/`.

When a throwaway Python script is needed and it imports from modules under `py/`, create it as `py/novc_<slug>.py` and run it from the repo root:

```
.venv\Scripts\python.exe py\novc_<slug>.py
```

Files matching `novc_*.py` should be gitignored via `py/.gitignore`. The `novc_` prefix keeps these files visually separate from tracked `main_*` scripts.

For PowerShell throwaway scripts and non-Python artifacts (commit messages, issue bodies, JSON diagnostics, screenshots, and similar scratch files), keep using `.novc/`.

## No `python -c` — Use `py/novc_<slug>.py` Instead

**Never use `python -c`** for any reason. Shell escaping of multi-line strings and Hebrew Unicode text is unreliable. Write a throwaway script as `py/novc_<slug>.py` and run it from the repo root.

## No Multi-Line PowerShell Payloads — Use `.novc/<slug>.ps1` Instead

For throwaway PowerShell logic, prefer a script file in `.novc/` over a massive command line with embedded multi-line payloads. This is the PowerShell analogue of avoiding `python -c`: once the payload is more than a short one-liner, write `.novc/<slug>.ps1` and run the script instead.

Do not embed multi-line PowerShell code in `pwsh -Command`, here-strings passed on the command line, or other long inline invocations when a script file would do. Quoting, escaping, and Unicode handling get fragile quickly; a `.ps1` file is clearer and more reliable.

## Multi-Line Content — Write to `.novc/` Files

When the payload is inherently multi-line (commit messages, GitHub issue/PR bodies, etc.), write it to a file in `.novc/` and reference the file. Do not pass multi-line content as a command argument — the Windows shell mangles it.

- **Git commit messages** — write to `.novc/commit_msg_<slug>.txt`, then `git commit -F .novc/commit_msg_<slug>.txt`
- **GitHub issue/PR bodies** — write to `.novc/issue_body.md` (or similar), then `gh issue create --body-file .novc/issue_body.md`

## UTF-8 Everywhere

This project processes Hebrew text. On Windows, Python defaults to the system ANSI code page, not UTF-8 — this causes `charmap` errors.

1. Every `open()` call must include `encoding="utf-8"`.
2. `json.dump()` / `json.dumps()` must pass `ensure_ascii=False`.
3. `subprocess` output: pass `encoding="utf-8"`.
4. Never rely on the system default encoding.
5. Prefer writing non-ASCII output to a file rather than stdout/stderr. When a script must print non-ASCII, reconfigure at the top of `main()`:
   ```python
   import sys
   sys.stdout.reconfigure(encoding="utf-8")
   sys.stderr.reconfigure(encoding="utf-8")
   ```
6. `$env:PYTHONUTF8="1"` is only for throwaway scripts where changing the code is not an option. For Python, prefer `py/novc_<slug>.py`; for PowerShell and non-Python scratch artifacts, use `.novc/`. (`PYTHONIOENCODING` is deprecated in favor of `PYTHONUTF8`.)

## Path Style

In git-tracked files, prefer repo-relative paths for files in this repository.

For references to sibling repositories, prefer sibling-relative paths such as `../repo-name/`.

Avoid hard-coded machine-specific absolute paths in tracked content unless the path is intentionally machine-specific.

Transient commands, scratch scripts, and `.novc/` helpers are not subject to this path-style rule unless a section explicitly says otherwise.

## Literal UTF-8 in Python Source — No Unnecessary `\uXXXX` Escapes

Write Hebrew letters, punctuation (maqaf, gershayim, etc.), em/en dashes, and other displayable characters as literal UTF-8. Do not use `\uXXXX` escapes for them.

When a character cannot be literal (zero-width chars like ZWJ, ZWNJ, CGJ; invisible whitespace like NBSP), prefer `\N{...}` named escapes over `\uXXXX`:
```python
_NDASH = "\N{EN DASH}"
_ZWJ = "\N{ZERO WIDTH JOINER}"
```

**Exception — curly quotes:** LLM tools persistently convert literal curly quotes to straight ASCII. For curly quotes, `\uXXXX` escapes are preferable, or use a utility function that wraps in curly quotes.

## No Unsolicited Git Operations

Never run `git commit` or `git push` without explicit permission from the user. Staging and status checks are fine.

## Never Amend Commits

Never use `git commit --amend` or `git rebase` unless the user explicitly asks. Always make new commits.

## Git Commit Messages — Use `-F`, Unique Slug

Never pass multi-line commit messages as a `-m` string — the Windows shell mangles multi-line or Hebrew-containing messages. Write to a uniquely-named file and commit with `-F`:

```
git commit -F .novc\commit_msg_<slug>.txt
```

Use a unique slug per commit (e.g. `commit_msg_add_2eq_check.txt`) — a stale generic filename silently produces the wrong message.

## Don't Close Issues Prematurely

Never close a GitHub issue until work is both committed **and** pushed. Closing before pushing leaves the issue marked resolved while the fix is only local.

## Before Discarding Work

Before any destructive git operation (`git reset`, `git checkout -- .`, `git stash drop`, etc.), run `git status` and `git diff --stat` first. If there are uncommitted changes beyond the current experiment, alert the user and ask them to commit or stash before proceeding.

Before a series of experiments that might need to be thrown away, ask the user to commit the current clean state first so there is a safe baseline to return to.

## File Organization

- All Python code lives under `py/`.
- **Main scripts** have a `main_` prefix (e.g. `py/main_mam4sef.py`, `py/main_parse.py`). These are the entry points run directly.
- **Library modules** live in package directories under `py/` (e.g. `py/mb_cmn/`, `py/mb_xml/`, `py/render_wt/`). These are imported by main scripts.
- **No `__init__.py` files.** This project does not use `__init__.py` in its package directories. Do not create one.

## Module Size Limit

If any Python file (main script or library module) grows beyond **300 lines**, spin off self-contained functions or classes into a new module under the appropriate package directory in `py/`. Keep each file focused and under the limit whenever practical.

## New Features as Modules

When adding a new self-contained feature, implement it as a new module under the appropriate `py/py*/` directory rather than appending the code to an existing file. The existing file should contain only a thin import and call; the feature's logic lives entirely in the new module. Do this even if the feature is small enough to fit within the size limit of the host file — module boundaries reflect conceptual separation, not just line counts.

**Exception:** Add directly to an existing file only when the new code depends on private helpers in that file **and** extracting those helpers into a shared module is prohibitively difficult. Even then, consider whether the helpers can be promoted to a shared module first.

## Extraction Structure Preference

When extracting helpers during a refactor, prefer one self-contained helper module per extracted concern rather than grouping multiple unrelated helpers into a generic shared utility module.

## Preserve Documentation During Refactors

Do not drop module docstrings, usage examples, function docstrings, explanatory variable names, or meaningful inline comments during refactors, extractions, moves, renames, or file splits unless they are truly obsolete.

Treat non-executable context as part of the implementation, not optional decoration. When reorganizing code, prefer starting from the original file text and trimming or moving it rather than re-synthesizing a fresh version that preserves behavior but loses explanation.

If you use AST/CST-assisted edits or other automated transforms, verify afterward that comments and docstrings survived. Before deleting or replacing the original file, compare old and new specifically for information loss, not just behavioral equivalence.

## Cross-Module Private Symbol Access

Do not access underscored symbols from other modules in production code. By convention, an underscore prefix means the symbol is private to its defining module.

If another module needs that symbol, do not mechanically reach in to the private name. First decide whether this would cross an architectural boundary:

- If the symbol is a stable shared concept that belongs in the module's public contract, make it public (remove underscore) and update callers.
- If exposing it would leak an implementation detail or cross an undesirable boundary, keep it private and solve the need differently (for example: local duplication of a tiny constant, a focused public helper/accessor, or ownership refactor).

Treat this as an architecture decision, not just a naming change.

## Fail Fast — No Silent Error Smoothing

Do **not** write defensive code that swallows errors or returns `None` on unexpected conditions. Only catch exceptions when there is a concrete recovery strategy. These are batch pipelines; a crash with a clear traceback is the correct response.

## Dict Access Style

- `d[key]` — when the key is **required** (a `KeyError` is a bug you want immediately)
- `d.get(key)` — when the key is **genuinely optional** and `None` is meaningful
- `d.get(key, default)` — when the key is optional and there is a natural default

## Key Constants: Prefer Explicit String Literals Over Clever Synthesis

For key identifiers that engineers must be able to search for reliably (template names, mapping keys, enum-like values, protocol tokens, and similar constants), prefer explicit string literals in canonical mapping tables.

Do not synthesize such strings from prefixes/suffixes, slicing, concatenation, or other "clever" derivations (for example deriving one key by stripping or adding `"מ:"` to another) unless there is a compelling, documented reason.

Rationale: explicit literals preserve searchability, make audits/refactors safer, and prevent hidden coupling between values that are intended to evolve independently.

## JSON Lists: Prepend, Don't Append

When adding to a semantically unordered JSON array, **prepend** rather than append. Appending requires a two-line diff; prepending is a clean one-line diff.

## Format Python with Black

After writing or editing any Python file, run black before committing. Format only files you changed:

```
.venv\Scripts\python.exe -m black py\py_misc\foo.py py\main_bar.py
```

This is mandatory — not optional.

## Editing Python with Concrete Syntax Trees

For complex or numerous edits to Python files, consider [libcst](https://libcst.readthedocs.io/) rather than fragile text replacements. Especially useful for refactors that rename symbols or restructure imports.

## Minimum Font Size for Pointed Hebrew

Never use smaller than **20pt** for pointed Hebrew in generated HTML. All CSS rules for pointed-Hebrew elements must use `font-size: 20pt` or larger.

## Opening HTML in a Browser

Open HTML files directly via the filesystem:

```
Start-Process "path\to\file.html"
```

## GitHub Repository Owner

The owner is **bdenckla**. Use this for GitHub MCP queries. Confirm via `git remote -v` if unsure.

## Graphviz

Graphviz is installed but not on the PATH. Look for it at `%ProgramFiles%\Graphviz\bin\` (e.g. `dot.exe`). The `survey_dot.py` module handles this fallback automatically.

## Local Sibling Repositories

Most repos are cloned as siblings at `../repo-name`. In git-tracked files, use relative sibling paths when referencing other repos (e.g. `../MAM-parsed/...`) rather than hard-coded absolute paths.

## Navigating MAM-parsed-plus JSON

See [mpplus-navigation.md](../doc/mpplus-navigation.md) for a quick-reference guide to the MAM-parsed-plus JSON structure. Full upstream docs: `../MAM-parsed/doc-under-readme/reading-mam-parsed-plus.md`.

## Terminology: "Varika"

**Varika** = **U+FB1E HEBREW POINT JUDEO-SPANISH VARIKA** (Alphabetic Presentation Forms block), **not** U+05BF HEBREW POINT RAFE (main Hebrew block). Do not confuse them.

**Important for code:** The MAM-parsed plus data actually uses U+05BF (RAFE) for the rafeh/varika mark on consonants. Do not assume the data contains U+FB1E — always check actual code points. `hpo.RAFE` (U+05BF) is what appears in the data; `hpo.VARIKA` (U+FB1E) is used in other contexts.

## Hebrew Unicode Mark Order — No NFC Normalization

This project uses a deliberate combining-mark order that differs from Unicode canonical (NFC) ordering. The standard order places these four marks first within each base-letter cluster:

1. Shin dot (U+05C1)
2. Sin dot (U+05C2)
3. Dagesh / mapiq / shuruq dot (U+05BC)
4. Rafeh (U+05BF)

In practice: **base letter → shin/sin dot → dagesh → rafeh → vowels / meteg / accents**.

The authoritative implementation is `py/mb_cmn/uni_denorm.py` (`give_std_mark_order`).

**Never apply Unicode normalization (NFC, NFD, etc.) to Hebrew text.** NFC reorders combining marks, destroying the project's intentional mark order. If strings that should be equal aren't matching, ensure both use the project's standard mark order — do not paper over with `unicodedata.normalize`.

## Do Not Mention Private Repos in Public Repos

Some sibling repositories are private. Never reference a private repo by name in commits, code, documentation, or issue/PR text destined for a public repo.

## Screenshots

When the user refers to "the most recent screenshot" or similar, this means the most recent file (by last-write time) in:

```
C:\Users\BenDe\OneDrive\Pictures\Screenshots
```

## Authorship Marking

When generating a new version-controlled file (Python script, Markdown doc, etc.), include an authorship comment as the **first line**:

- **Python:** `# Initially generated by GitHub Copilot.`
- **Markdown/HTML:** `<!-- Initially generated by GitHub Copilot. -->`

This does not apply to throwaway files in `.novc/`.

## Markdown Formatting

Do not use bare tildes (`~`) as an abbreviation for "approximately." Markdown renderers interpret text between two `~` characters as strikethrough. Instead, write out "approx." or "approximately," or escape the tilde (`\~`).

