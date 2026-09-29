"""Create independent environments and check the approved dependency constraints."""

from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name
from packaging.version import Version

from product_scopes import product_dirs
from repo_util.user_config_sync import _run_git, _command_error


class ForestError(RuntimeError):
    """A forest cannot be synchronized without violating its declared rules."""


def require_unlinked(path: Path) -> None:
    """Reject redirected directories before writing environments or repositories."""
    for candidate in (path, *path.parents):
        if candidate.is_symlink() or candidate.is_junction():
            raise ForestError(
                f"linked path is not an independent forest path: {candidate}"
            )


def _run_python(interpreter: Path, directory: Path, *arguments: str) -> str:
    environment = os.environ.copy()
    environment["PIP_NO_INPUT"] = "1"
    environment["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    environment["PYTHONIOENCODING"] = "utf-8"
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [str(interpreter), *arguments],
        cwd=directory,
        env=environment,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=300,
        check=False,
    )
    if result.returncode:
        raise ForestError(result.stderr.strip() or result.stdout.strip())
    return result.stdout


def _requirements(path: Path) -> list[Requirement]:
    entries = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            entry = Requirement(line)
            if entry.url or entry.extras:
                raise ForestError(f"unsupported requirement URL or extras: {entry}")
            entries.append(entry)
    if not entries:
        raise ForestError(f"empty dependency declaration: {path}")
    return entries


def _pins(path: Path) -> dict[str, Version]:
    pins = {}
    for entry in _requirements(path):
        specs = list(entry.specifier)
        if (
            entry.url
            or entry.extras
            or entry.marker
            or len(specs) != 1
            or specs[0].operator != "=="
            or "*" in specs[0].version
        ):
            raise ForestError(
                f"constraints must contain exact named version pins: {entry}"
            )
        name = canonicalize_name(entry.name)
        if name in pins:
            raise ForestError(f"duplicate constraint: {entry.name}")
        pins[name] = Version(specs[0].version)
    return pins


def _check_environment(directory: Path) -> None:
    venv = directory / ".venv"
    require_unlinked(venv)
    interpreter = venv / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    if not interpreter.is_file() or not (venv / "pyvenv.cfg").is_file():
        raise ForestError(f"missing or incomplete environment: {venv}")
    configuration = (venv / "pyvenv.cfg").read_text(encoding="utf-8")
    for line in configuration.splitlines():
        key, separator, value = line.partition("=")
        if (
            separator
            and key.strip().casefold() == "include-system-site-packages"
            and value.strip().casefold() != "false"
        ):
            raise ForestError(f"environment admits system-site packages: {venv}")
    prefix, base_prefix = json.loads(
        _run_python(
            interpreter,
            directory,
            "-c",
            "import json, sys; print(json.dumps([sys.prefix, sys.base_prefix]))",
        )
    )
    if Path(prefix).resolve() == Path(base_prefix).resolve():
        raise ForestError(f"interpreter is not a virtual environment: {interpreter}")
    if Path(prefix).resolve() != venv.resolve():
        raise ForestError(f"interpreter belongs to {prefix}, expected {venv}")
    pins = _pins(directory / "constraints.txt")
    inventory = json.loads(
        _run_python(interpreter, directory, "-m", "pip", "inspect", "--local")
    )
    installed = {
        canonicalize_name(item["metadata"]["name"]): Version(
            item["metadata"]["version"]
        )
        for item in inventory["installed"]
    }
    problems = []
    for requirement in _requirements(directory / "requirements.txt"):
        if requirement.marker and not requirement.marker.evaluate(
            inventory["environment"]
        ):
            continue
        name = canonicalize_name(requirement.name)
        if name not in pins:
            problems.append(f"unconstrained direct requirement {requirement.name}")
        if name not in installed:
            problems.append(f"missing direct requirement {requirement.name}")
        elif installed[name] not in requirement.specifier:
            problems.append(
                f"installed {name}=={installed[name]} does not satisfy {requirement}"
            )
    for name, version in installed.items():
        if name in pins and version != pins[name]:
            problems.append(f"{name}=={version}, expected {pins[name]}")
        elif name not in pins and name not in {"pip", "setuptools", "wheel"}:
            problems.append(f"unconstrained installed package {name}=={version}")
    if problems:
        raise ForestError("; ".join(problems))
    _run_python(interpreter, directory, "-m", "pip", "check")


def synchronize_environments(repo: Path, *, check: bool) -> bool:
    """Inspect development requirements, excluding distributed product inputs."""
    tracked = _run_git(
        repo, "ls-files", "-z", "--", "requirements.txt", "**/requirements.txt"
    )
    if tracked.returncode:
        raise ForestError(_command_error(tracked))
    requirements = [name for name in tracked.stdout.split("\0") if name]
    product_names = (
        {directory.name for directory in product_dirs()}
        if repo.name == "MAM-basics"
        else set()
    )
    success = True
    for name in requirements:
        if Path(name).parts[0] in product_names:
            print(f"FOREST_CONSUMER_REQUIREMENTS: {repo / name}")
            continue
        requirement_path = repo / name
        directory = requirement_path.parent
        try:
            require_unlinked(directory)
            if requirement_path.is_symlink():
                raise ForestError(f"linked requirement file: {requirement_path}")
            if not directory.resolve().is_relative_to(repo.resolve()):
                raise ForestError(f"requirement escapes checkout: {name}")
            constraints = directory / "constraints.txt"
            if not constraints.is_file() or constraints.is_symlink():
                raise ForestError(f"missing regular constraints file: {constraints}")
            indexed = _run_git(
                repo,
                "ls-files",
                "--error-unmatch",
                "-z",
                "--",
                constraints.relative_to(repo).as_posix(),
            )
            if indexed.returncode:
                raise ForestError(f"constraints are not tracked: {constraints}")
            _pins(constraints)
            _requirements(requirement_path)
            venv = directory / ".venv"
            require_unlinked(venv)
            if not venv.exists():
                if check:
                    raise ForestError(f"missing environment: {venv}")
                print(f"FOREST_ENV_CREATE: {venv}", flush=True)
                _run_python(Path(sys.executable), directory, "-m", "venv", str(venv))
                interpreter = venv / (
                    "Scripts/python.exe" if os.name == "nt" else "bin/python"
                )
                _run_python(
                    interpreter,
                    directory,
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    "requirements.txt",
                    "-c",
                    "constraints.txt",
                )
            _check_environment(directory)
            print(f"FOREST_ENV_CLEAN: {venv}")
        except (OSError, ValueError, subprocess.SubprocessError, ForestError) as exc:
            print(f"FOREST_ENV_FAILED: {directory}: {exc}")
            success = False
    return success
