"""Differential checks for process-local Git repository trust."""

from __future__ import annotations

import os
from pathlib import Path
import subprocess
import sys

from mb_cmn.git_process import add_windows_safe_directory, git_command


def _isolated_git_environment() -> dict[str, str]:
    environment = {
        key: value
        for key, value in os.environ.items()
        if key != "GIT_CONFIG_COUNT"
        and not key.startswith("GIT_CONFIG_KEY_")
        and not key.startswith("GIT_CONFIG_VALUE_")
    }
    environment["GIT_CONFIG_GLOBAL"] = os.devnull
    environment["GIT_CONFIG_NOSYSTEM"] = "1"
    return environment


def _init_repository(path: Path, *, environment: dict[str, str]) -> Path:
    subprocess.run(
        ["git", "init", "--quiet", str(path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
        env=environment,
    )
    return path.resolve()


def _git_config_values(
    repo: Path, key: str, *, environment: dict[str, str] | None = None
) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(repo), "config", "--get-all", key],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
        env=environment,
    )
    return result.stdout.splitlines()


def test_git_command_exposes_only_the_resolved_repository_as_safe(
    tmp_path: Path,
) -> None:
    environment = _isolated_git_environment()
    repo = _init_repository(tmp_path / "repository", environment=environment)
    safe_result = subprocess.run(
        git_command(repo, "config", "--get-all", "safe.directory"),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
        env=environment,
    )
    root_result = subprocess.run(
        git_command(repo / ".", "rev-parse", "--show-toplevel"),
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
        env=environment,
    )

    assert safe_result.stdout.splitlines() == [repo.as_posix()]
    assert Path(root_result.stdout.strip()).resolve() == repo


def test_environment_helper_preserves_git_settings_without_duplication(
    tmp_path: Path,
) -> None:
    environment = _isolated_git_environment()
    repo = _init_repository(tmp_path / "repository", environment=environment)
    environment.update(
        {
            "GIT_CONFIG_COUNT": "1",
            "GIT_CONFIG_KEY_0": "codex.existing",
            "GIT_CONFIG_VALUE_0": "preserved",
        }
    )

    if sys.platform != "win32":
        expected = environment.copy()
        add_windows_safe_directory(environment, repo)
        assert environment == expected
        return

    add_windows_safe_directory(environment, repo)
    add_windows_safe_directory(environment, repo)

    assert _git_config_values(repo, "codex.existing", environment=environment) == [
        "preserved"
    ]
    assert _git_config_values(repo, "safe.directory", environment=environment) == [
        repo.as_posix()
    ]
