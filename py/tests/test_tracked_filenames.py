"""Lint tracked filenames and programmatic Git filename parsing.

Finding 18.2 of ``doc/review-findings-2026-09-10.md`` reported two Holman
pages as untracked. Both pages were tracked: line-based parsing had treated
Git's quoted output as paths. Ben's decision of 2026-09-12 addresses the
failure on two independent sides:

* Tracked filenames contain no Hebrew letters. Hebrew labels are converted by
  ``py/py_ac_word_image_helper/alef_bet_to_ascii.py``.
* Programmatic Git commands that return filenames still request NUL delimiters.

The first check is a mechanical lint over the index. The second is a mechanical
lint over tracked Python syntax. Both are lint-shaped tests sanctioned by
``CLAUDE.md``. A missing input fails rather than passing silently.
"""

import ast
import re
import subprocess

from mb_cmn import paths

_HEBREW_LETTER_RE = re.compile(r"[\u05D0-\u05EA]")
_TRACKED_FILE_FLOOR = 4000


def _tracked_paths(*pathspecs: str) -> list[str]:
    command = ["git", "ls-files", "-z"]
    if pathspecs:
        command.extend(["--", *pathspecs])
    result = subprocess.run(
        command,
        cwd=paths.repo_root(),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return [path for path in result.stdout.split("\0") if path]


def _literal_command(node: ast.AST) -> list[str] | None:
    if not isinstance(node, (ast.List, ast.Tuple)):
        return None
    values = []
    for element in node.elts:
        if isinstance(element, ast.Constant) and isinstance(element.value, str):
            values.append(element.value)
    return values if "git" in values else None


def _returns_filenames(command: list[str]) -> bool:
    if "ls-files" in command:
        return True
    if "ls-tree" in command and any(
        part == "--name-only" or part.startswith("--name-only=") for part in command
    ):
        return True
    if "status" in command and any(part.startswith("--porcelain") for part in command):
        return True
    if "diff" in command and "--numstat" in command:
        return True
    return "worktree" in command and "list" in command


def test_tracked_filenames_contain_no_hebrew_letters() -> None:
    tracked = _tracked_paths()
    assert len(tracked) >= _TRACKED_FILE_FLOOR, (
        f"Only {len(tracked)} tracked files were listed (floor {_TRACKED_FILE_FLOOR});"
        " the filename lint may have read the wrong tree."
    )
    offenders = sorted(path for path in tracked if _HEBREW_LETTER_RE.search(path))
    assert not offenders, (
        "Tracked filenames contain Hebrew letters. Convert each Hebrew portion with"
        " py/py_ac_word_image_helper/alef_bet_to_ascii.py and update controlled"
        f" references: {offenders}"
    )


def test_git_filename_commands_request_nul_delimiters() -> None:
    python_paths = _tracked_paths("*.py")
    assert len(python_paths) > 100, (
        f"Only {len(python_paths)} tracked Python files were listed; the Git-command"
        " lint may have read the wrong tree."
    )
    offenders = []
    for rel in python_paths:
        source = (paths.repo_root() / rel).read_text(encoding="utf-8")
        tree = ast.parse(source, filename=rel)
        for node in ast.walk(tree):
            command = _literal_command(node)
            if command is None or not _returns_filenames(command) or "-z" in command:
                continue
            offenders.append(f"{rel}:{node.lineno}")
    assert not offenders, (
        "Programmatic Git commands return filenames without NUL delimiters. Add -z"
        f" and split stdout on \\0 rather than lines: {sorted(offenders)}"
    )
