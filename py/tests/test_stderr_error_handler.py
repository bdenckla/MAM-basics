"""Lint: every reconfiguration of stderr keeps its ``backslashreplace`` error handler.

``TextIOWrapper.reconfigure`` resets a stream's error handler to ``strict`` whenever it
is given an encoding and no ``errors``, so ``sys.stderr.reconfigure(encoding="utf-8")``
turns stderr's default ``backslashreplace`` into ``strict``, and a traceback that quotes
a lone surrogate then fails while it is being reported.  The 2026-10-02 review found
that form in eleven programs (its item C15.4); on 2026-10-03, at Ben's request, the
other 34 entry points under ``py/``, ``wlc_cmn.utf8_io.force_utf8_io`` and a Codex hook
were corrected too.

A mechanical lint over every tracked Python file.  It passes only if every call of a
``reconfigure`` method names its stream directly, as ``sys.stdin``, ``sys.stdout`` or
``sys.stderr``, so that no loop, alias or ``getattr`` hides which stream it is, and
every ``sys.stderr`` call passes ``errors="backslashreplace"``.  A scan that finds no
stderr call fails.
"""

import ast
import subprocess

from mb_cmn import paths
from mb_cmn.git_process import git_command

_STREAMS = frozenset({"sys.stdin", "sys.stdout", "sys.stderr"})


def _problems(rel, tree):
    """The problems of one module's reconfigure calls, and its count of stderr calls."""
    problems = []
    stderr_calls = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        where = f"{rel}:{node.lineno}"
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr == "reconfigure":
            stream = ast.unparse(func.value)
            if stream not in _STREAMS:
                problems.append(f"{where}: reconfigure on {stream}, not a named stream")
            elif stream == "sys.stderr":
                stderr_calls += 1
                errors = [k.value for k in node.keywords if k.arg == "errors"]
                if not (
                    len(errors) == 1
                    and isinstance(errors[0], ast.Constant)
                    and errors[0].value == "backslashreplace"
                ):
                    problems.append(
                        f"{where}: sys.stderr.reconfigure without"
                        ' errors="backslashreplace"'
                    )
        elif isinstance(func, ast.Name) and func.id == "reconfigure":
            problems.append(f"{where}: reconfigure called through a name")
        elif (
            isinstance(func, ast.Name)
            and func.id == "getattr"
            and len(node.args) >= 2
            and isinstance(node.args[1], ast.Constant)
            and node.args[1].value == "reconfigure"
        ):
            problems.append(f"{where}: reconfigure looked up with getattr")
    return problems, stderr_calls


def test_every_stderr_reconfigure_keeps_backslashreplace():
    root = paths.repo_root()
    raw = subprocess.run(
        git_command(root, "ls-files", "-z", "--", "*.py"),
        capture_output=True,
        check=True,
    ).stdout
    rels = [part.decode("utf-8") for part in raw.split(b"\0") if part]
    assert rels, "git ls-files listed no tracked .py -- the lint has no input"
    problems = []
    stderr_calls = 0
    for rel in rels:
        source = (root / rel).read_text(encoding="utf-8")
        if "reconfigure" not in source:
            continue
        module_problems, module_calls = _problems(rel, ast.parse(source, filename=rel))
        problems.extend(module_problems)
        stderr_calls += module_calls
    assert stderr_calls, "the scan found no sys.stderr.reconfigure call -- no input"
    assert not problems, "\n".join(problems)
