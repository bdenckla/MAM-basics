"""Build exact-path Git trust for elevated Windows worktrees."""

from __future__ import annotations

from collections.abc import MutableMapping
import os
from pathlib import Path


def _resolved_repo(repo_dir: Path) -> Path:
    resolved = repo_dir.resolve(strict=True)
    if not resolved.is_dir():
        raise NotADirectoryError(f"Git repository path is not a directory: {resolved}")
    return resolved


def git_command(repo_dir: Path, *args: str) -> list[str]:
    """Return Git arguments with an exact command-local trust exception."""
    resolved = _resolved_repo(repo_dir)
    return [
        "git",
        "-c",
        f"safe.directory={resolved.as_posix()}",
        "-C",
        str(resolved),
        *args,
    ]


def add_windows_safe_directory(
    environment: MutableMapping[str, str], repo_dir: Path
) -> None:
    """Append exact repository trust to a child-process environment on Windows."""
    if os.name != "nt":
        return

    resolved_text = _resolved_repo(repo_dir).as_posix()
    raw_count = environment.get("GIT_CONFIG_COUNT")
    if raw_count is None:
        count = 0
    else:
        try:
            count = int(raw_count)
        except ValueError as exc:
            raise ValueError(
                f"GIT_CONFIG_COUNT must be a nonnegative integer, got {raw_count!r}"
            ) from exc
        if count < 0:
            raise ValueError(
                f"GIT_CONFIG_COUNT must be a nonnegative integer, got {raw_count!r}"
            )

    for index in range(count):
        key_name = f"GIT_CONFIG_KEY_{index}"
        value_name = f"GIT_CONFIG_VALUE_{index}"
        missing = [name for name in (key_name, value_name) if name not in environment]
        if missing:
            raise ValueError(
                "GIT_CONFIG_COUNT declares an incomplete entry at index "
                f"{index}: missing {', '.join(missing)}"
            )
        if (
            environment[key_name].lower() == "safe.directory"
            and environment[value_name] == resolved_text
        ):
            return

    environment[f"GIT_CONFIG_KEY_{count}"] = "safe.directory"
    environment[f"GIT_CONFIG_VALUE_{count}"] = resolved_text
    environment["GIT_CONFIG_COUNT"] = str(count + 1)
