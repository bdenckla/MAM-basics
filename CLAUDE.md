# Claude Instructions

## Python Environment — MANDATORY venv-qualified commands

Always use a virtual environment (venv) for Python work in this project. Never install packages into the global Python environment.

- The venv is located at `.venv/` in the project root.
- **Always use explicit venv paths** when running Python or pip. Do not rely on a previously activated venv in the terminal — always use the explicit path, even if it seems redundant.

**Platform-specific venv paths:**

| | Windows | Linux / macOS |
|---|---|---|
| Python | `.venv\Scripts\python.exe` | `.venv/bin/python` |
| pip | `.venv\Scripts\pip.exe` | `.venv/bin/pip` |

**FORBIDDEN — bare `python` / `pip` commands:**
Never run `python`, `python3`, `pip`, or `pip3` as a bare command, even if the venv appears to be activated. Every invocation must use the fully-qualified path:

| Forbidden | Required (Windows) | Required (Linux/macOS) |
|-----------|----------|----------|
| `python script.py` | `.venv\Scripts\python.exe script.py` | `.venv/bin/python script.py` |
| `pip install X` | `.venv\Scripts\pip.exe install X` | `.venv/bin/pip install X` |
| `python -m pytest` | `.venv\Scripts\python.exe -m pytest` | `.venv/bin/python -m pytest` |

This rule applies everywhere: terminal commands, code blocks in chat, examples in documentation, and tool invocations. No exceptions.

## Running Python Main Scripts — Always From the Repo Root

All `py/main_*.py` scripts use paths like `../MAM-parsed` that are relative to the **repo root** (`~/GitRepos/MAM-basics`), not to the `py/` subdirectory. Always `cd` to the repo root before running a script:

```bash
cd ~/GitRepos/MAM-basics && PYTHONUTF8=1 .venv/Scripts/python.exe py/main_mam_simple.py
```

**Why the explicit `cd`:** The Bash tool's working directory persists between commands. If a prior command did `cd py && ...`, all subsequent commands run from `py/`, making `../MAM-parsed` resolve to `MAM-basics/MAM-parsed` (wrong) instead of the sibling repo at `GitRepos/MAM-parsed` (correct). The explicit `cd ~/GitRepos/MAM-basics` at the start of each run command resets this reliably.

## No `python -c` — Use `.novc/` Scripts Instead

**Never use `python -c`** for any reason, not even for short one-liners. Always write a temporary `.py` file in `./.novc/` (which is gitignored) and run it:

```bash
PYTHONUTF8=1 .venv/Scripts/python.exe .novc/my_script.py
```

(`PYTHONUTF8=1` is used here because `.novc/` scripts are throwaway — see the UTF-8 section for why it is **not** used with git-tracked scripts.)

**Why:** The Claude Code permissions glob uses `*` which does not match newline characters. Multi-line `-c` strings therefore fail to match the allow rule and trigger an approval prompt every time. Banning `-c` entirely avoids the problem — every invocation is a simple single-line command that matches the glob.

## No Multi-Line Shell Commands (General Principle)

The `python -c` ban above is a specific instance of a general rule: **never write a Bash command that spans multiple lines.** Many "one-liners" are only conceptually one-liners — they use heredocs, multi-line strings, or subshell constructs that produce multi-line commands. Claude Code's permission globs use `*` which does not match newlines, so any multi-line command breaks glob matching and triggers an approval prompt. Keep every Bash invocation to a single line; when the payload is inherently multi-line (a Python snippet, a commit message, etc.), write it to a file and reference the file.

**Common instances of this pattern:**

- **Git commit messages** — write to a uniquely-named file in `.novc/` with the Write tool, then `git commit -F .novc/commit_msg_<slug>.txt` (documented below).
- **GitHub issue/PR bodies** — write to `.novc/issue_body.md` (or similar) with the Write tool, then `gh issue create --body-file .novc/issue_body.md` or `gh pr create --body-file .novc/pr_body.md`.
- **Python snippets** — write to `.novc/my_script.py` with the Write tool, then run with the venv Python (documented above).

## Prefer Built-in Tools over Bash Equivalents

**Default to using Claude Code's built-in tools** (Read, Write, Edit, Grep, Glob) instead of accomplishing the same thing via Bash. Only fall back to Bash when the built-in tool genuinely cannot do the job or is radically slower. The built-in tools handle paths and permissions correctly, produce output that is easier for the user to review, and — crucially — do not require Bash permission globs.

- **Read files** — use the Read tool, not `cat`/`head`/`tail` in Bash.
- **Write/create files** — use the Write tool, not `echo >` / `cat <<EOF >` / redirection in Bash.
- **Edit files** — use the Edit tool, not `sed` or `awk` in Bash.
- **Search file contents** — use the Grep tool, not `grep` or `rg` in Bash.
- **Find files by pattern** — use the Glob tool, not `find` or `ls` in Bash.

Every Bash command the user has not pre-allowed triggers an approval prompt. Each new Bash pattern the user must allow is friction that a built-in tool would have avoided entirely.

## UTF-8 Everywhere

This project processes Hebrew text. On Windows, Python defaults to the system ANSI code page (e.g. `cp1252`), **not** UTF-8, which causes `charmap` codec errors.

**Rules:**

1. **Every `open()` call** must include `encoding="utf-8"` — for both reading and writing. No exceptions, even for JSON or plain-text files that "should" be ASCII.
2. **`json.dump()` / `json.dumps()`** — always pass `ensure_ascii=False` so Hebrew characters are written directly rather than escaped to `\uXXXX`.
3. **`subprocess` output** — when capturing output from subprocesses, pass `encoding="utf-8"` (or use `text=True` with `encoding="utf-8"`).
4. **Never rely on the system default encoding.** Do not assume `PYTHONIOENCODING` or `PYTHONUTF8` is set. Be explicit in code.
5. **`PYTHONUTF8=1` is only for `.novc/` scripts.** When running a git-tracked script, do **not** set `PYTHONUTF8=1` — if the script crashes with a codec error, that is a bug in the script and should be fixed, not masked. Only use `PYTHONUTF8=1` when running throwaway scripts you generate into `.novc/`, where adding explicit `encoding="utf-8"` to every `open()` call is not worth the effort. (Note: the shell is **Git Bash**, not PowerShell — use `VAR=value cmd` syntax, not `$env:VAR="value"; cmd`.)

```python
# CORRECT
with open(path, "r", encoding="utf-8") as f: ...
with open(path, "w", encoding="utf-8") as f: ...
json.dump(data, f, ensure_ascii=False, indent=2)

# WRONG — will fail on Windows with Hebrew text
with open(path, "r") as f: ...
with open(path) as f: ...
```

## No Unsolicited Git Operations

Never run `git commit` or `git push` without explicit permission from the user. It is fine to stage files or check status, but committing and especially pushing must be requested or approved first.

## Never Amend Commits

Never use `git commit --amend` or `git rebase` to modify an existing commit unless the user explicitly asks for it. Always make changes as new commits on top of the current history.

## Git Commit Messages — Use `-F`, Not Heredocs

**Never pass multi-line commit messages inline** via heredocs (`<<'EOF'`), `$(cat ...)` subshells, or multi-line `-m` strings. Instead, write the message to a **uniquely-named** file in `.novc/` using the **Write tool** and then commit with `-F`:

```bash
git commit -F .novc/commit_msg_<short_slug>.txt
```

**IMPORTANT — use a unique file name for every commit.** Do **not** reuse a fixed name like `commit_msg.txt`. A stale file from a previous session will silently produce the wrong commit message. Use a short slug derived from the work, e.g. `.novc/commit_msg_add_2eq_check.txt`. The name doesn't need to be long — it just needs to differ from any previous commit-message file.

The file must be created with the Write tool, **not** with `echo … > .novc/...` or any other Bash redirection — that would just be another Bash invocation requiring its own permission glob. This follows both the general multi-line command ban and the "prefer built-in tools" rule.

**No pre-write checks.** Do **not** run `ls`, `test -f`, or any other Bash command to check whether `.novc/` or the file exists before writing. The Write tool creates the file (and any intermediate directories) unconditionally — no existence check is needed. Just call Write directly.

## Don't Redundantly Re-assert the Repo Directory

The working directory is already the project root. Do not `cd` into it or pass it via `git -C` — just run `git` directly:

| Unnecessary | Just do this |
|---|---|
| `cd ~/GitRepos/MAM-basics && git log` | `git log` |
| `git -C ~/GitRepos/MAM-basics log` | `git log` |

If you genuinely need to run `git` in a **different** directory (e.g. a sibling repo), prefer `git -C <path>` over `cd <path> && git`. Use `cd && git` only as a last resort — compound commands are harder to match with permission globs.

## Don't Close Issues Prematurely

Never close (or suggest closing) a GitHub issue until its work has been both committed **and** pushed to the remote. Closing before pushing leaves the issue marked resolved while the fix is still only local.

## File Organization

- All Python code lives under the `py/` directory at the project root.
- **Main scripts** are named with a `main_` prefix (e.g. `py/main_mam4sef.py`, `py/main_parse_go.py`). These are the entry points that are run directly.
- **Library modules** live in `py/py*/` directories (e.g. `py/pycmn/`, `py/pyxml/`, `py/pyrender/`). These are imported by main scripts but are not run on their own.

## Fail Fast — No Silent Error Smoothing

Do **not** write defensive code that swallows errors or returns `None` / a default when an unexpected condition occurs. Let exceptions happen — they should be loud, immediate, and informative.

Specifically:

- **No `try`/`except` to paper over bugs.** Only catch exceptions when there is a concrete recovery strategy. Never catch broad `Exception` or `KeyError` just to return `None`.
- **No bounds-checking to return `None`.** If an index or key is expected to exist, access it directly. An `IndexError` or `KeyError` is more useful than a silent `None` that causes a confusing failure downstream.
- **Prefer crashing to guessing.** A traceback at the point of the bug is far easier to diagnose than a wrong result produced silently.

This applies throughout the codebase. The data-processing pipelines in this project are batch jobs, not user-facing services — a crash with a clear traceback is the correct response to unexpected input.

## Dict Access Style

Do **not** default to `dict.get()` for every dictionary access. Be intentional about which style you use:

- **`d[key]`** — when the key is **required** (always expected to be present). A `KeyError` on a missing required key is a bug you want to hear about immediately.
- **`d.get(key)`** — when the key is **genuinely optional** and `None` is a meaningful "absent" signal.
- **`d.get(key, default)`** — when the key is optional and there is a natural default (e.g. `d.get("layout", "")`, `d.get("count", 0)`).

The wrong choice in either direction is harmful: using `.get()` on a required key hides bugs (silent `None` propagation); using `d[key]` on a truly optional key forces unnecessary `key in d` guards.

## JSON Lists: Prepend, Don't Append

When adding an item to a JSON array whose order is semantically meaningless, **prepend** (insert at the beginning) rather than append. JSON forbids trailing commas, so appending always produces a two-line diff (add comma to the old last element + add the new element), whereas prepending produces a clean one-line diff. This applies to configuration files, permission lists, and similar unordered arrays throughout the project.

## Format Python with Black

After writing or editing any Python file, run **black** to format it before committing. Black is installed in the venv.

```bash
.venv/Scripts/python.exe -m black <file_or_directory>
```

Format only the files you changed — do not reformat the entire repository unless asked. When editing multiple files, pass them all in a single invocation:

```bash
.venv/Scripts/python.exe -m black py/py_misc/foo.py py/main_bar.py
```

This is a mandatory step, not optional. Every Python file touched during a session must be black-formatted before it is committed.

## Editing Python with Concrete Syntax Trees

When making complex or numerous edits to Python files, consider using [libcst](https://libcst.readthedocs.io/) (Concrete Syntax Tree) to programmatically transform the code rather than doing fragile line-level text replacements. `libcst` preserves formatting, comments, and whitespace while allowing precise AST-level edits. This is especially useful for refactors that touch many call sites, rename symbols, or restructure imports.

## Minimum Font Size for Pointed Hebrew

Never use a font size smaller than **20pt** for pointed (vocalized/cantillated) Hebrew text in generated HTML. At smaller sizes the diacritical marks (nikkud, cantillation) become illegible. All CSS rules for elements that display pointed Hebrew must use `font-size: 20pt` (or larger).

## Opening HTML in a Browser

When asked to open an HTML file in the browser, prefer opening it directly via the filesystem rather than spinning up an HTTP server. The generated reports use only relative links and work correctly from `file://` URLs. Since the shell is Git Bash (not PowerShell), call through PowerShell explicitly:

```bash
powershell.exe -Command "Start-Process 'path/to/file.html'"
```

## GitHub Repository Owner

The owner of this repository is **bdenckla**. When making GitHub MCP queries (e.g. listing issues, creating PRs), use `bdenckla` as the owner. If in doubt, confirm by running `git remote -v` and extracting the owner from the remote URL.

## Graphviz

Graphviz is installed but not on the PATH. Look for it at `%ProgramFiles%\Graphviz\bin\` (e.g. `dot.exe`). The `survey_dot.py` module handles this fallback automatically.

## Local Sibling Repositories

Most of the owner's GitHub repos are cloned locally as siblings of this repo — i.e. at `../repo-name` (relative to this repo's root). When you need to read or search files in another repo (e.g. `MAM-parsed`, `MAM-simple`, `MAM-OSIS`), use relative paths like `../MAM-parsed/...` rather than hard-coding an absolute path. This keeps instructions portable across machines.

## Navigating MAM-parsed plus (MPP) JSON

See [mpp-navigation.md](mpp-navigation.md) for a quick-reference guide to the MPP JSON structure (file naming, verse lookup by chapter:verse, template format). Full upstream docs live at `../MAM-parsed/doc-under-readme/reading-mam-parsed-plus.md`.

## Terminology: "Varika"

When the user says **varika**, they mean **U+FB1E HEBREW POINT JUDEO-SPANISH VARIKA** (in the Alphabetic Presentation Forms block), **not** U+05BF HEBREW POINT RAFE (in the main Hebrew block). These are distinct characters — do not confuse them.

**Important for code:** Despite the terminology above, the MAM-parsed plus/ data **actually uses U+05BF** (HEBREW POINT RAFE) for the rafeh/varika mark on consonants (e.g. the quiescent alef in ראובני words). Do not assume the data contains U+FB1E — always check the actual code points. The Python constant `hpo.RAFE` (U+05BF) is what appears in the data; `hpo.VARIKA` (U+FB1E) is used in other contexts (e.g. the mark-order normalization layer).

## Hebrew Unicode Mark Order — No NFC Normalization

This project uses a deliberate combining-mark order for Hebrew text that differs from Unicode's canonical (NFC) ordering. The standard order places these four marks first within each base-letter cluster (in this order), followed by all other marks in their original relative order:

1. Shin dot (U+05C1)
2. Sin dot (U+05C2)
3. Dagesh / mapiq / shuruq dot (U+05BC)
4. Rafeh (U+05BF)

In practice: **base letter → shin/sin dot → dagesh → rafeh → vowels / meteg / accents**.

The authoritative implementation is `py/pycmn/uni_denorm.py` (`give_std_mark_order`).

**Never apply Unicode normalization (NFC, NFD, etc.) to Hebrew text in this project.** NFC reorders combining marks into canonical order, which destroys the project's intentional mark order. If two strings that should be equal are not matching, the fix is to ensure both sides use the project's standard mark order — not to paper over the difference with `unicodedata.normalize`.

When hand-authoring Hebrew strings in JSON input files, ensure they match the mark order used in MAM-parsed plus (MPP) data exactly. When in doubt, copy the string from MPP output or pass it through `give_std_mark_order`.

## Do Not Mention Private Repos in Public Repos

Some sibling repositories are private. Never reference a private repo by name in commits, code, documentation, or issue/PR text destined for a public repo. If you need to describe a pattern that originates in a private repo, describe the pattern itself without naming the source.
