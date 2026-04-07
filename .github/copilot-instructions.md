# Copilot Instructions for MAM-basics

## Book Names and Identifiers

- Reuse already-defined book names and identifiers whenever possible.
- Prefer canonical symbolic book ids from shared code, such as `1Samuel` and `Levit`, even in display contexts unless the user explicitly asks otherwise.
- Do not invent a new parallel set of book names that is more verbose, more abbreviated, or only slightly different from existing names.
- When a book-name mapping is genuinely needed, derive it from existing shared definitions in `pycmn` or another established module rather than hard-coding a fresh local mapping.

## Python Environment — MANDATORY venv-qualified commands

Always use `.venv/` for Python work. **Never run bare `python`, `python3`, `pip`, or `pip3`** — always use the explicit venv path:

- **Windows:** `.venv\Scripts\python.exe` / `.venv\Scripts\pip.exe`
- **Linux/macOS:** `.venv/bin/python` / `.venv/bin/pip`

This rule applies everywhere — terminal, chat examples, documentation. No exceptions.

## Running Python Main Scripts — Always From the Repo Root

All `py/main_*.py` scripts use paths like `../MAM-parsed` that are relative to the **repo root**. Always run from the repo root:

```
.venv\Scripts\python.exe py\main_mam_simple.py
```

Do not `cd` into `py/` before running — `../MAM-parsed` would then resolve to the wrong location.

## No `python -c` — Use `.novc/` Scripts Instead

**Never use `python -c`** for any reason. Shell escaping of multi-line strings and Hebrew Unicode text is unreliable. Write a `.py` file in `.novc/` (gitignored) and run it:

```
.venv\Scripts\python.exe .novc\my_script.py
```

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
6. `$env:PYTHONUTF8="1"` is only for `.novc/` throwaway scripts where changing the code is not an option. (`PYTHONIOENCODING` is deprecated in favor of `PYTHONUTF8`.)

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

## Don't Redundantly Re-assert the Repo Directory

The terminal's working directory is already the project root. Run `git` directly without `cd` or `git -C <this-repo>`. For a sibling repo, use `git -C <path>`.

## Don't Close Issues Prematurely

Never close a GitHub issue until work is both committed **and** pushed. Closing before pushing leaves the issue marked resolved while the fix is only local.

## Before Discarding Work

Before any destructive git operation (`git reset`, `git checkout -- .`, `git stash drop`, etc.), run `git status` and `git diff --stat` first. If there are uncommitted changes beyond the current experiment, alert the user and ask them to commit or stash before proceeding.

Before a series of experiments that might need to be thrown away, ask the user to commit the current clean state first so there is a safe baseline to return to.

## File Organization

- All Python code lives under `py/`.
- **Main scripts** have a `main_` prefix (e.g. `py/main_mam4sef.py`, `py/main_parse_go.py`). These are the entry points run directly.
- **Library modules** live in `py/py*/` directories (e.g. `py/pycmn/`, `py/pyxml/`, `py/pyrender/`). These are imported by main scripts.

## Fail Fast — No Silent Error Smoothing

Do **not** write defensive code that swallows errors or returns `None` on unexpected conditions. Only catch exceptions when there is a concrete recovery strategy. These are batch pipelines; a crash with a clear traceback is the correct response.

## Dict Access Style

- `d[key]` — when the key is **required** (a `KeyError` is a bug you want immediately)
- `d.get(key)` — when the key is **genuinely optional** and `None` is meaningful
- `d.get(key, default)` — when the key is optional and there is a natural default

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

Most repos are cloned as siblings at `../repo-name`. Use relative paths when referencing other repos (e.g. `../MAM-parsed/...`) — do not hard-code absolute paths.

## Navigating MAM-parsed plus (MPP) JSON

See [mpp-navigation.md](mpp-navigation.md) for a quick-reference guide to the MPP JSON structure. Full upstream docs: `../MAM-parsed/doc-under-readme/reading-mam-parsed-plus.md`.

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

The authoritative implementation is `py/pycmn/uni_denorm.py` (`give_std_mark_order`).

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

