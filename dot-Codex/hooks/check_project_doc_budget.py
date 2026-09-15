"""Warn when Codex project instructions exceed their configured byte budget.

This is a user-level ``SessionStart`` hook.  It also verifies that the base
user-wide ``AGENTS.md`` matches the origin-derived fingerprint installed by
MAM-basics' ``--sync-user-config`` action.  The global file is deliberately not
added to the project byte total: Codex loads it outside
``project_doc_max_bytes``.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import sys
import tomllib

_DEFAULT_PROJECT_DOC_MAX_BYTES = 32 * 1024
_DEFAULT_PROJECT_ROOT_MARKERS = (".git",)
_PRIMARY_FILENAMES = ("AGENTS.override.md", "AGENTS.md")
_EXPECTED_USER_AGENTS_SHA256 = "expected-user-wide-AGENTS.sha256"


class InstructionCheckError(RuntimeError):
    """A configuration or filesystem problem that prevents a reliable check."""


@dataclass(frozen=True)
class Settings:
    project_doc_max_bytes: int
    project_doc_fallback_filenames: tuple[str, ...]
    project_root_markers: tuple[str, ...]


@dataclass(frozen=True)
class ProjectReport:
    cwd: Path
    project_root: Path
    selected_files: tuple[Path, ...]
    selected_sizes: tuple[int, ...]
    total_bytes: int
    max_bytes: int


@dataclass(frozen=True)
class UserAgentsReport:
    path: Path
    size: int | None
    matches_expected: bool
    override_path: Path | None


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--maintenance",
        action="store_true",
        help="print a complete labeled report and use the exit status",
    )
    parser.add_argument(
        "--cwd",
        type=Path,
        help="directory whose project-instruction chain should be checked",
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        help="Codex home containing config.toml and AGENTS.md",
    )
    return parser.parse_args()


def _codex_home(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit.resolve()
    configured = os.environ.get("CODEX_HOME")
    if configured:
        return Path(configured).resolve()
    return (Path.home() / ".codex").resolve()


def _read_settings(codex_home: Path) -> Settings:
    config_path = codex_home / "config.toml"
    if config_path.is_file():
        with config_path.open("rb") as file_obj:
            config = tomllib.load(file_obj)
    else:
        config = {}

    max_bytes = config.get("project_doc_max_bytes", _DEFAULT_PROJECT_DOC_MAX_BYTES)
    if isinstance(max_bytes, bool) or not isinstance(max_bytes, int) or max_bytes < 0:
        raise InstructionCheckError(
            f"{config_path}: project_doc_max_bytes must be a nonnegative integer"
        )

    fallbacks = _string_list(
        config_path,
        "project_doc_fallback_filenames",
        config.get("project_doc_fallback_filenames", []),
    )
    markers = _string_list(
        config_path,
        "project_root_markers",
        config.get("project_root_markers", list(_DEFAULT_PROJECT_ROOT_MARKERS)),
    )
    return Settings(max_bytes, fallbacks, markers)


def _string_list(config_path: Path, key: str, value: object) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise InstructionCheckError(f"{config_path}: {key} must be a list of strings")
    return tuple(value)


def _read_hook_input() -> dict[str, object]:
    try:
        value = json.load(sys.stdin)
    except (json.JSONDecodeError, OSError) as exc:
        raise InstructionCheckError(f"cannot read SessionStart input: {exc}") from exc
    if not isinstance(value, dict):
        raise InstructionCheckError("SessionStart input must be a JSON object")
    return value


def _effective_cwd(explicit: Path | None, hook_input: dict[str, object]) -> Path:
    raw_cwd: object = explicit if explicit is not None else hook_input.get("cwd")
    if not isinstance(raw_cwd, (str, os.PathLike)):
        raise InstructionCheckError("SessionStart input has no string cwd")
    cwd = Path(raw_cwd).resolve()
    if not cwd.is_dir():
        raise InstructionCheckError(f"SessionStart cwd is not a directory: {cwd}")
    return cwd


def _project_root(cwd: Path, markers: tuple[str, ...]) -> Path:
    if not markers:
        return cwd
    for directory in (cwd, *cwd.parents):
        if any((directory / marker).exists() for marker in markers):
            return directory
    return cwd


def _candidate_filenames(fallbacks: tuple[str, ...]) -> tuple[str, ...]:
    names = list(_PRIMARY_FILENAMES)
    for name in fallbacks:
        if name and name not in names:
            names.append(name)
    return tuple(names)


def _search_directories(project_root: Path, cwd: Path) -> tuple[Path, ...]:
    directories = []
    cursor = cwd
    while True:
        directories.append(cursor)
        if cursor == project_root:
            break
        parent = cursor.parent
        if parent == cursor:
            raise InstructionCheckError(
                f"project root {project_root} is not an ancestor of {cwd}"
            )
        cursor = parent
    directories.reverse()
    return tuple(directories)


def _project_report(cwd: Path, settings: Settings) -> ProjectReport:
    root = _project_root(cwd, settings.project_root_markers)
    filenames = _candidate_filenames(settings.project_doc_fallback_filenames)
    selected_files = []
    selected_sizes = []
    for directory in _search_directories(root, cwd):
        selected = next(
            (directory / name for name in filenames if (directory / name).is_file()),
            None,
        )
        if selected is None:
            continue
        data = selected.read_bytes()
        if not data.decode("utf-8", errors="replace").strip():
            continue
        selected_files.append(selected)
        selected_sizes.append(len(data))
    return ProjectReport(
        cwd,
        root,
        tuple(selected_files),
        tuple(selected_sizes),
        sum(selected_sizes),
        settings.project_doc_max_bytes,
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _user_agents_report(codex_home: Path) -> UserAgentsReport:
    expected_path = codex_home / "hooks" / _EXPECTED_USER_AGENTS_SHA256
    if not expected_path.is_file():
        raise InstructionCheckError(
            f"origin-derived user-wide AGENTS.md fingerprint is missing: {expected_path}"
        )
    expected = expected_path.read_text(encoding="ascii").strip()
    if len(expected) != 64 or any(char not in "0123456789abcdef" for char in expected):
        raise InstructionCheckError(
            f"origin-derived user-wide AGENTS.md fingerprint is invalid: {expected_path}"
        )

    agents_path = codex_home / "AGENTS.md"
    size = agents_path.stat().st_size if agents_path.is_file() else None
    matches = agents_path.is_file() and _sha256(agents_path) == expected
    override = codex_home / "AGENTS.override.md"
    override_path = None
    if (
        override.is_file()
        and override.read_text(encoding="utf-8", errors="replace").strip()
    ):
        override_path = override
    return UserAgentsReport(agents_path, size, matches, override_path)


def _problems(project: ProjectReport, user_agents: UserAgentsReport) -> tuple[str, ...]:
    problems = []
    if project.total_bytes > project.max_bytes:
        problems.append(
            "Codex project instructions exceed project_doc_max_bytes: "
            f"{project.total_bytes:,} > {project.max_bytes:,} bytes for {project.cwd}. "
            "Later project instructions will be truncated."
        )
    if user_agents.size is None:
        problems.append(
            f"User-wide Codex instructions are not installed: {user_agents.path}"
        )
    elif not user_agents.matches_expected:
        problems.append(
            "User-wide Codex instructions differ from the origin/main-derived "
            f"fingerprint installed by MAM-basics: {user_agents.path}"
        )
    if user_agents.override_path is not None:
        problems.append(
            "A nonempty user-wide override masks the installed AGENTS.md: "
            f"{user_agents.override_path}"
        )
    return tuple(problems)


def _print_maintenance_report(
    project: ProjectReport,
    user_agents: UserAgentsReport,
    problems: tuple[str, ...],
) -> None:
    print(f"CODEX_PROJECT_DOC_CWD={project.cwd}")
    print(f"CODEX_PROJECT_DOC_ROOT={project.project_root}")
    for path, size in zip(project.selected_files, project.selected_sizes, strict=True):
        print(f"CODEX_PROJECT_DOC_FILE={path} BYTES={size}")
    print(
        "CODEX_PROJECT_DOC_BYTES="
        f"{project.total_bytes} PROJECT_DOC_MAX_BYTES={project.max_bytes}"
    )
    user_size = "not installed" if user_agents.size is None else str(user_agents.size)
    print(
        f"CODEX_USER_AGENTS={user_agents.path} BYTES={user_size} "
        f"MATCHES_ORIGIN_FINGERPRINT={str(user_agents.matches_expected).lower()}"
    )
    if user_agents.override_path is not None:
        print(f"CODEX_USER_AGENTS_OVERRIDE={user_agents.override_path}")
    for problem in problems:
        print(f"CODEX_INSTRUCTION_PROBLEM: {problem}")
    print(f"CODEX_INSTRUCTION_PROBLEM_COUNT={len(problems)}")


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = _parse_args()
    try:
        hook_input = {} if args.cwd is not None else _read_hook_input()
        codex_home = _codex_home(args.codex_home)
        cwd = _effective_cwd(args.cwd, hook_input)
        settings = _read_settings(codex_home)
        project = _project_report(cwd, settings)
        user_agents = _user_agents_report(codex_home)
        problems = _problems(project, user_agents)
        if args.maintenance:
            _print_maintenance_report(project, user_agents, problems)
            raise SystemExit(1 if problems else 0)
        if problems:
            print(json.dumps({"systemMessage": "\n".join(problems)}))
    except (InstructionCheckError, OSError, tomllib.TOMLDecodeError) as exc:
        problem = f"Codex instruction startup check could not complete: {exc}"
        if args.maintenance:
            print(f"CODEX_INSTRUCTION_CHECK_FAILED: {exc}")
            raise SystemExit(1) from exc
        print(json.dumps({"systemMessage": problem}))


if __name__ == "__main__":
    main()
