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
from dataclasses import dataclass
import importlib.util
from pathlib import PurePosixPath
import re
import subprocess

from mb_cmn import paths

_HEBREW_LETTER_RE = re.compile(r"[\u05D0-\u05EA]")
_TRACKED_FILE_FLOOR = 4000


@dataclass(frozen=True)
class _Wrapper:
    fixed_count: int
    literal_prefix: tuple[str, ...]


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
    if "git" in command and "grep" in command:
        grep_index = command.index("grep")
        filename_modes = {
            "-l",
            "-L",
            "--files-with-matches",
            "--files-without-match",
        }
        if any(part in filename_modes for part in command[grep_index + 1 :]):
            return True
    return "worktree" in command and "list" in command


def _module_name(rel: str) -> str:
    parts = list(PurePosixPath(rel).with_suffix("").parts)
    if parts and parts[0] == "py":
        parts.pop(0)
    if parts and parts[-1] == "__init__":
        parts.pop()
    return ".".join(parts)


def _import_bindings(tree: ast.AST, module_name: str) -> dict[str, str]:
    bindings = {}
    package = module_name.rpartition(".")[0]
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            imported_module = node.module or ""
            if node.level:
                if not package:
                    continue
                imported_module = importlib.util.resolve_name(
                    "." * node.level + imported_module, package
                )
            for alias in node.names:
                if alias.name == "*":
                    continue
                local_name = alias.asname or alias.name
                bindings[local_name] = f"{imported_module}.{alias.name}"
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    bindings[alias.asname] = alias.name
    return bindings


def _callable_name(
    node: ast.AST, module_name: str, bindings: dict[str, str]
) -> str | None:
    if isinstance(node, ast.Name):
        return bindings.get(node.id, f"{module_name}.{node.id}")
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
        imported_module = bindings.get(node.value.id)
        if imported_module is not None:
            return f"{imported_module}.{node.attr}"
    return None


def _expands_vararg(node: ast.AST, vararg: str) -> bool:
    return (
        isinstance(node, ast.Starred)
        and isinstance(node.value, ast.Name)
        and node.value.id == vararg
    )


def _git_wrappers(trees: dict[str, ast.AST]) -> dict[str, _Wrapper]:
    functions: dict[
        str,
        tuple[
            ast.FunctionDef | ast.AsyncFunctionDef,
            str,
            dict[str, str],
        ],
    ] = {}
    wrappers: dict[str, _Wrapper] = {}
    for rel, tree in trees.items():
        module_name = _module_name(rel)
        bindings = _import_bindings(tree, module_name)
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            vararg = node.args.vararg
            if vararg is None:
                continue
            qualified_name = f"{module_name}.{node.name}"
            functions[qualified_name] = node, module_name, bindings
            for candidate in ast.walk(node):
                if not isinstance(candidate, (ast.List, ast.Tuple)):
                    continue
                if not any(
                    _expands_vararg(item, vararg.arg) for item in candidate.elts
                ):
                    continue
                literals = tuple(
                    item.value
                    for item in candidate.elts
                    if isinstance(item, ast.Constant) and isinstance(item.value, str)
                )
                if "git" not in literals:
                    continue
                wrappers[qualified_name] = _Wrapper(
                    fixed_count=len(node.args.posonlyargs) + len(node.args.args),
                    literal_prefix=literals,
                )
                break

    unresolved = set(functions) - set(wrappers)
    while unresolved:
        progress = False
        for qualified_name in tuple(unresolved):
            node, module_name, bindings = functions[qualified_name]
            vararg = node.args.vararg
            assert vararg is not None
            for candidate in ast.walk(node):
                if not isinstance(candidate, ast.Call):
                    continue
                if not any(
                    _expands_vararg(item, vararg.arg) for item in candidate.args
                ):
                    continue
                callee_name = _callable_name(candidate.func, module_name, bindings)
                callee = wrappers.get(callee_name or "")
                if callee is None:
                    continue
                forwarded = candidate.args[callee.fixed_count :]
                literal_arguments = tuple(
                    item.value
                    for item in forwarded
                    if isinstance(item, ast.Constant) and isinstance(item.value, str)
                )
                wrappers[qualified_name] = _Wrapper(
                    fixed_count=len(node.args.posonlyargs) + len(node.args.args),
                    literal_prefix=(*callee.literal_prefix, *literal_arguments),
                )
                unresolved.remove(qualified_name)
                progress = True
                break
        if not progress:
            break
    return wrappers


def _wrapped_command(
    node: ast.AST,
    module_name: str,
    bindings: dict[str, str],
    wrappers: dict[str, _Wrapper],
) -> list[str] | None:
    if not isinstance(node, ast.Call):
        return None
    callable_name = _callable_name(node.func, module_name, bindings)
    wrapper = wrappers.get(callable_name or "")
    if wrapper is None:
        return None
    passed_varargs = node.args[wrapper.fixed_count :]
    literal_arguments = [
        argument.value
        for argument in passed_varargs
        if isinstance(argument, ast.Constant) and isinstance(argument.value, str)
    ]
    return [*wrapper.literal_prefix, *literal_arguments]


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
    trees = {}
    for rel in python_paths:
        source = (paths.repo_root() / rel).read_text(encoding="utf-8")
        trees[rel] = ast.parse(source, filename=rel)
    wrappers = _git_wrappers(trees)
    offenders = []
    for rel, tree in trees.items():
        module_name = _module_name(rel)
        bindings = _import_bindings(tree, module_name)
        for node in ast.walk(tree):
            command = _literal_command(node) or _wrapped_command(
                node, module_name, bindings, wrappers
            )
            if command is None or not _returns_filenames(command) or "-z" in command:
                continue
            offenders.append(f"{rel}:{node.lineno}")
    assert not offenders, (
        "Programmatic Git commands return filenames without NUL delimiters. Add -z"
        f" and split stdout on \\0 rather than lines: {sorted(offenders)}"
    )
