"""Lint: code under py/ reads the clock, and git's dates, with a zone.

Ben's decision of 2026-09-14, recorded in ``py/mb_cmn/new_york_time.py``: every date that
this repository's code shows on a page or in a report is its New York date and says so, and
a timestamp stored in data keeps its ISO 8601 offset. A clock read with no zone, or a git
date placeholder that drops the committer's offset, is how a date with no stated zone gets
written, so this lint fails on either in tracked Python under ``py/``:

* ``today()``, ``now()`` with no argument, ``utcnow()``, ``utcfromtimestamp()``, and
  ``fromtimestamp()`` without a zone;
* ``time.localtime``, ``time.strftime``, ``time.ctime`` and ``time.asctime``;
* a git ``--format=`` or ``--pretty=`` string with a date placeholder other than the strict
  ISO ``%cI`` and ``%aI`` or the Unix times ``%ct`` and ``%at``, and any ``--date=`` option.

The case that produced it: until 2026-09-14 the change log dated commits with ``%cs``, each
commit's date in whatever offset that commit recorded, which differs between Ben's machines
and a cloud container. This is a mechanical lint over the tree, one of the two test shapes
``CLAUDE.md`` sanctions, and a missing input fails rather than passing silently.
"""

import ast
import re
import subprocess

from mb_cmn import paths

_PYTHON_FILE_FLOOR = 100
_GIT_FORMAT_RE = re.compile(r"^(?:--format=|--pretty=)")
_GIT_DATE_PLACEHOLDER_RE = re.compile(r"%[ac][dDhiIrst]")
_ZONED_PLACEHOLDERS = frozenset({"%cI", "%aI", "%ct", "%at"})
_LOCAL_TIME_FUNCTIONS = frozenset({"localtime", "strftime", "ctime", "asctime"})


def _tracked_python_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files", "-z", "--", "py/*.py"],
        cwd=paths.repo_root(),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return [path for path in result.stdout.split("\0") if path]


def _call_problem(node: ast.Call) -> str | None:
    func = node.func
    if not isinstance(func, ast.Attribute):
        return None
    name = func.attr
    has_arguments = bool(node.args or node.keywords)
    if name == "today" and not has_arguments:
        return "today() reads the clock with no zone"
    if name == "now" and not has_arguments:
        return "now() with no argument reads the clock with no zone"
    if name in ("utcnow", "utcfromtimestamp"):
        return f"{name}() returns a datetime with no zone"
    if (
        name == "fromtimestamp"
        and len(node.args) < 2
        and not any(keyword.arg == "tz" for keyword in node.keywords)
    ):
        return "fromtimestamp() without tz returns a datetime with no zone"
    if (
        name in _LOCAL_TIME_FUNCTIONS
        and isinstance(func.value, ast.Name)
        and func.value.id == "time"
    ):
        return f"time.{name} works in local time with no zone"
    return None


def _string_problem(value: str) -> str | None:
    # An option with a value, as git takes one; a bare prefix string such as this
    # module's own pattern is not an option.
    if re.match(r"^--date=\S", value):
        return f"{value!r} formats a git date without its offset"
    if _GIT_FORMAT_RE.match(value):
        found = set(_GIT_DATE_PLACEHOLDER_RE.findall(value))
        dropped = sorted(found - _ZONED_PLACEHOLDERS)
        if dropped:
            return (
                f"{value!r} uses git date placeholders {dropped}, which drop the offset"
            )
    return None


def test_clock_and_git_date_reads_state_a_zone() -> None:
    python_paths = _tracked_python_files()
    assert len(python_paths) > _PYTHON_FILE_FLOOR, (
        f"Only {len(python_paths)} tracked Python files were listed under py/"
        f" (floor {_PYTHON_FILE_FLOOR}); the lint may have read the wrong tree."
    )
    problems = []
    for rel in python_paths:
        source = (paths.repo_root() / rel).read_text(encoding="utf-8")
        tree = ast.parse(source, filename=rel)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                problem = _call_problem(node)
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                problem = _string_problem(node.value)
            else:
                problem = None
            if problem is not None:
                problems.append(f"{rel}:{node.lineno}: {problem}")
    assert not problems, (
        "Read the clock with a zone, take git dates as %cI, %aI, %ct or %at, and show a"
        " date through py/mb_cmn/new_york_time.py:\n" + "\n".join(sorted(problems))
    )
