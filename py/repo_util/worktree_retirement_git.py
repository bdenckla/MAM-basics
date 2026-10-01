"""Git process, path and registration primitives for worktree retirement.

The family's other implementation modules import these, as do the compatibility
inspection modules ``git_worktree_cleanup`` and ``clean_worktrees``.  Nothing here
decides whether a worktree may be retired.
"""

from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from mb_cmn.git_process import git_command


class RetirementError(RuntimeError):
    """A safety gate refused worktree retirement."""


@dataclass(frozen=True)
class _Worktree:
    path: Path
    head: str | None
    branch: str | None
    locked: bool


def _git(
    repo_dir: Path,
    *args: str,
    text: bool = True,
    timeout_seconds: int | None = None,
    noninteractive: bool = False,
) -> subprocess.CompletedProcess[Any]:
    """Run Git with the exact local trust exception Windows worktrees need.

    ``timeout_seconds`` bounds the process, and ``noninteractive`` forbids Git and its
    credential manager to prompt, as ``user_config_sync._run_git`` does; by default
    neither applies.
    """
    command = git_command(repo_dir, "--no-optional-locks", *args)
    environment = None
    if noninteractive:
        environment = os.environ.copy()
        environment["GIT_TERMINAL_PROMPT"] = "0"
        environment["GCM_INTERACTIVE"] = "Never"
    return subprocess.run(
        command,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
        errors="replace" if text else None,
        env=environment,
        timeout=timeout_seconds,
    )


def _git_ok(
    repo_dir: Path,
    *args: str,
    timeout_seconds: int | None = None,
    noninteractive: bool = False,
) -> str:
    result = _git(
        repo_dir,
        *args,
        timeout_seconds=timeout_seconds,
        noninteractive=noninteractive,
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "git failed"
        raise RetirementError(f"git {' '.join(args)}: {message}")
    return result.stdout


def _path_key(path: Path | str) -> str:
    return os.path.normcase(os.path.abspath(path))


def _same_path(left: Path | str, right: Path | str) -> bool:
    return _path_key(left) == _path_key(right)


def _inside(path: Path, directory: Path) -> bool:
    key = _path_key(path)
    parent = _path_key(directory)
    return key == parent or key.startswith(parent + os.sep)


def _list_worktrees(
    repo_dir: Path,
    *,
    timeout_seconds: int | None = None,
    noninteractive: bool = False,
) -> list[_Worktree]:
    output = _git_ok(
        repo_dir,
        "worktree",
        "list",
        "--porcelain",
        "-z",
        timeout_seconds=timeout_seconds,
        noninteractive=noninteractive,
    )
    records: list[_Worktree] = []
    path: Path | None = None
    head: str | None = None
    branch: str | None = None
    locked = False
    for field in output.split("\0"):
        if field.startswith("worktree "):
            path = Path(field.removeprefix("worktree "))
            head = None
            branch = None
            locked = False
        elif field.startswith("HEAD "):
            head = field.removeprefix("HEAD ")
        elif field.startswith("branch refs/heads/"):
            branch = field.removeprefix("branch refs/heads/")
        elif field == "locked" or field.startswith("locked "):
            locked = True
        elif not field.strip() and path is not None:
            records.append(_Worktree(path, head, branch, locked))
            path = None
    if path is not None:
        records.append(_Worktree(path, head, branch, locked))
    if not records:
        raise RetirementError("git listed no worktrees")
    return records


def _default_branch(repo_dir: Path) -> str:
    symbolic = _git(repo_dir, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    if symbolic.returncode == 0 and "/" in symbolic.stdout:
        return symbolic.stdout.strip().split("/", 1)[1]
    main = _git(repo_dir, "rev-parse", "--verify", "--quiet", "main")
    if main.returncode == 0:
        return "main"
    raise RetirementError("no default branch is available for the integration check")


def _is_ancestor(repo_dir: Path, commit: str, descendant: str) -> bool:
    return (
        _git(repo_dir, "merge-base", "--is-ancestor", commit, descendant).returncode
        == 0
    )
