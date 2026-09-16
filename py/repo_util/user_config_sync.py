"""Check or deploy Ben's user-level agent configuration from ``origin/main``.

The live Claude and Codex files sit outside Git, so the source for every operation is
the freshly fetched ``refs/remotes/origin/main`` of the primary MAM-basics clone.  A
failed fetch stops before any live destination changes.  The cloud-session bootstrap
hook is deliberately separate: it sources the cloud session's checked-out branch.

Every skill under ``dot-claude/skills`` deploys to Claude, every skill under
``dot-Codex/skills`` deploys to Codex, the user-level Codex hook is installed,
and the names in
``dot-claude/shared-skills.txt`` deploy from the Claude tree to Codex as well.  Building
that complete mapping and validating every source precedes any destination write.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tarfile
import tempfile
from typing import Iterator, Literal
import uuid

from mb_cmn import paths, provenance

_SOURCE_REF = "refs/remotes/origin/main"
_FETCH_TIMEOUT_SECONDS = 60
_SHARED_SKILLS = Path("dot-claude/shared-skills.txt")
_GENERATED_USER_AGENTS_FINGERPRINT = Path(".generated/expected-user-wide-AGENTS.sha256")
_ARCHIVE_PATHS = (
    Path("dot-claude/user-wide-CLAUDE.md"),
    Path("dot-claude/skills"),
    Path("dot-Codex/user-wide-AGENTS.md"),
    Path("dot-Codex/hooks.json"),
    Path("dot-Codex/hooks/check_project_doc_budget.py"),
    Path("dot-Codex/skills"),
    _SHARED_SKILLS,
)
_Kind = Literal["file", "directory"]


class UserConfigSyncError(RuntimeError):
    """A source, fetch, deployment, or rollback failure."""


@dataclass(frozen=True)
class ConfigMapping:
    source_rel: Path
    destination_rel: Path
    kind: _Kind


@dataclass(frozen=True)
class Comparison:
    mapping: ConfigMapping
    status: Literal["clean", "drift", "not installed"]
    detail: str = ""


@dataclass(frozen=True)
class _Staged:
    mapping: ConfigMapping
    destination: Path
    staged_path: Path


@dataclass(frozen=True)
class _Installed:
    destination: Path
    backup_path: Path | None


def run_user_config_sync(
    *, check: bool, repo_root: Path | None = None, home: Path | None = None
) -> bool:
    """Fetch, then check or deploy the complete user-level configuration.

    Deployment is accepted only from the primary clone.  A check may run from a linked
    worktree, which lets ``main_repo_maintenance.py`` retain a useful failure mode if it
    is invoked from the wrong checkout without letting that checkout deploy anything.
    """
    current_root = (repo_root or paths.repo_root()).resolve()
    live_home = (home or Path.home()).resolve()
    try:
        primary = _primary_clone(current_root)
        if not check and current_root != primary:
            raise UserConfigSyncError(
                "deployment must run from the primary MAM-basics clone: "
                f"{primary}; current checkout is {current_root}"
            )
        _fetch_origin(primary)
        with _source_tree(primary) as (source_root, source_commit):
            mappings = _build_mappings(source_root)
            comparisons = _compare_all(source_root, live_home, mappings)
            print(f"USER_CONFIG_SOURCE={primary} {_SOURCE_REF}@{source_commit}")
            if check:
                _print_comparisons(comparisons)
                problems = [item for item in comparisons if item.status != "clean"]
                print(f"USER_CONFIG_PROBLEM_COUNT={len(problems)}")
                return not problems

            changed = [item.mapping for item in comparisons if item.status != "clean"]
            if not changed:
                _print_comparisons(comparisons)
                print("USER_CONFIG_DEPLOYED_COUNT=0")
                return True
            _deploy_transaction(source_root, live_home, changed)
            verified = _compare_all(source_root, live_home, mappings)
            _print_comparisons(verified)
            problems = [item for item in verified if item.status != "clean"]
            if problems:
                raise UserConfigSyncError(
                    f"post-deployment verification found {len(problems)} problem(s)"
                )
            print(f"USER_CONFIG_DEPLOYED_COUNT={len(changed)}")
            return True
    except (
        OSError,
        subprocess.SubprocessError,
        tarfile.TarError,
        UserConfigSyncError,
    ) as exc:
        operation = "CHECK" if check else "DEPLOY"
        print(f"USER_CONFIG_{operation}_FAILED: {exc}")
        return False


def _primary_clone(repo_root: Path) -> Path:
    primary = provenance.home_clone_dir(repo_root)
    if primary is None:
        raise UserConfigSyncError(
            f"cannot identify the primary MAM-basics clone from {repo_root}"
        )
    primary = primary.resolve()
    if primary.name.casefold() != "mam-basics":
        raise UserConfigSyncError(
            f"expected the primary clone to be named MAM-basics, found {primary}"
        )
    return primary


def _fetch_origin(primary: Path) -> None:
    try:
        result = _run_git(
            primary,
            "fetch",
            "--no-tags",
            "origin",
            "+refs/heads/main:refs/remotes/origin/main",
            timeout_seconds=_FETCH_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise UserConfigSyncError(
            f"git fetch origin exceeded {_FETCH_TIMEOUT_SECONDS} seconds; "
            "no live destination was changed"
        ) from exc
    if result.returncode != 0:
        raise UserConfigSyncError(
            "git fetch origin failed; no live destination was changed: "
            + _command_error(result)
        )
    verify = _run_git(primary, "rev-parse", "--verify", f"{_SOURCE_REF}^{{commit}}")
    if verify.returncode != 0:
        raise UserConfigSyncError(
            f"fresh fetch left no {_SOURCE_REF}: {_command_error(verify)}"
        )


@contextmanager
def _source_tree(primary: Path) -> Iterator[tuple[Path, str]]:
    commit_result = _run_git(
        primary, "rev-parse", "--verify", f"{_SOURCE_REF}^{{commit}}"
    )
    if commit_result.returncode != 0:
        raise UserConfigSyncError(_command_error(commit_result))
    source_commit = commit_result.stdout.strip()
    with tempfile.TemporaryDirectory(prefix="mam-user-config-source-") as tmp:
        temp_root = Path(tmp)
        archive_path = temp_root / "source.tar"
        result = _run_git(
            primary,
            "archive",
            "--format=tar",
            f"--output={archive_path}",
            _SOURCE_REF,
            "--",
            *(path.as_posix() for path in _ARCHIVE_PATHS),
        )
        if result.returncode != 0:
            raise UserConfigSyncError(
                f"cannot read user-level configuration from {_SOURCE_REF}: "
                + _command_error(result)
            )
        source_root = temp_root / "tree"
        source_root.mkdir()
        _extract_regular_files(archive_path, source_root)
        yield source_root, source_commit


def _run_git(
    primary: Path, *args: str, timeout_seconds: int | None = None
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment["GIT_TERMINAL_PROMPT"] = "0"
    environment["GCM_INTERACTIVE"] = "Never"
    return subprocess.run(
        ["git", "-C", str(primary), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        env=environment,
        timeout=timeout_seconds,
    )


def _command_error(result: subprocess.CompletedProcess[str]) -> str:
    return (
        result.stderr.strip()
        or result.stdout.strip()
        or f"Git exited {result.returncode}"
    )


def _extract_regular_files(archive_path: Path, destination: Path) -> None:
    destination = destination.resolve()
    with tarfile.open(archive_path, "r") as archive:
        members = archive.getmembers()
        for member in members:
            member_path = (destination / member.name).resolve()
            if not member_path.is_relative_to(destination):
                raise UserConfigSyncError(
                    f"source archive path escapes its root: {member.name}"
                )
            if not (member.isdir() or member.isfile()):
                raise UserConfigSyncError(
                    f"source archive contains a non-file entry: {member.name}"
                )
        archive.extractall(destination, members=members, filter="data")


def _build_mappings(source_root: Path) -> tuple[ConfigMapping, ...]:
    claude_instructions = ConfigMapping(
        Path("dot-claude/user-wide-CLAUDE.md"), Path(".claude/CLAUDE.md"), "file"
    )
    codex_instructions = ConfigMapping(
        Path("dot-Codex/user-wide-AGENTS.md"), Path(".codex/AGENTS.md"), "file"
    )
    hook_script = ConfigMapping(
        Path("dot-Codex/hooks/check_project_doc_budget.py"),
        Path(".codex/hooks/check_project_doc_budget.py"),
        "file",
    )
    hook_config = ConfigMapping(
        Path("dot-Codex/hooks.json"), Path(".codex/hooks.json"), "file"
    )
    for mapping in (
        claude_instructions,
        codex_instructions,
        hook_script,
        hook_config,
    ):
        _require_source(source_root / mapping.source_rel, mapping.kind)

    fingerprint_source = source_root / _GENERATED_USER_AGENTS_FINGERPRINT
    fingerprint_source.parent.mkdir(exist_ok=True)
    fingerprint_source.write_text(
        _sha256(source_root / "dot-Codex/user-wide-AGENTS.md") + "\n",
        encoding="ascii",
    )

    claude_skills = _skill_names(source_root / "dot-claude" / "skills")
    codex_skills = _skill_names(source_root / "dot-Codex" / "skills")
    shared_skills = _read_shared_skills(source_root / _SHARED_SKILLS)
    missing_shared = sorted(set(shared_skills) - set(claude_skills))
    if missing_shared:
        raise UserConfigSyncError(
            "shared skill(s) absent from dot-claude/skills: "
            + ", ".join(missing_shared)
        )

    mappings = [
        claude_instructions,
        codex_instructions,
        hook_script,
        ConfigMapping(
            _GENERATED_USER_AGENTS_FINGERPRINT,
            Path(".codex/hooks/expected-user-wide-AGENTS.sha256"),
            "file",
        ),
    ]
    mappings.extend(
        ConfigMapping(
            Path("dot-claude/skills") / name,
            Path(".claude/skills") / name,
            "directory",
        )
        for name in claude_skills
    )
    mappings.extend(
        ConfigMapping(
            Path("dot-Codex/skills") / name,
            Path(".agents/skills") / name,
            "directory",
        )
        for name in codex_skills
    )
    mappings.extend(
        ConfigMapping(
            Path("dot-claude/skills") / name,
            Path(".agents/skills") / name,
            "directory",
        )
        for name in shared_skills
    )
    # Activate the hook only after its script and fingerprint are in place on a
    # first installation. Existing sessions can still see individual replacements,
    # but every replacement has already been staged and rollback remains complete.
    mappings.append(hook_config)
    _reject_duplicate_destinations(mappings)
    return tuple(mappings)


def _skill_names(skills_root: Path) -> tuple[str, ...]:
    _require_source(skills_root, "directory")
    names: list[str] = []
    for child in sorted(skills_root.iterdir(), key=lambda path: path.name.casefold()):
        if not child.is_dir() or child.is_symlink():
            raise UserConfigSyncError(
                f"unexpected non-directory in tracked skill root: {child}"
            )
        _require_source(child / "SKILL.md", "file")
        names.append(child.name)
    return tuple(names)


def _read_shared_skills(path: Path) -> tuple[str, ...]:
    _require_source(path, "file")
    names = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        name = raw_line.strip()
        if not name or name.startswith("#"):
            continue
        if Path(name).name != name or name in {".", ".."}:
            raise UserConfigSyncError(f"invalid shared skill name: {name!r}")
        names.append(name)
    duplicates = sorted(name for name in set(names) if names.count(name) > 1)
    if duplicates:
        raise UserConfigSyncError(
            "duplicate shared skill name(s): " + ", ".join(duplicates)
        )
    return tuple(sorted(names, key=str.casefold))


def _require_source(path: Path, kind: _Kind) -> None:
    if path.is_symlink():
        raise UserConfigSyncError(f"tracked source must not be a symlink: {path}")
    if kind == "file" and not path.is_file():
        raise UserConfigSyncError(f"tracked source file is missing: {path}")
    if kind == "directory" and not path.is_dir():
        raise UserConfigSyncError(f"tracked source directory is missing: {path}")


def _reject_duplicate_destinations(mappings: list[ConfigMapping]) -> None:
    seen: dict[str, ConfigMapping] = {}
    for mapping in mappings:
        key = mapping.destination_rel.as_posix().casefold()
        previous = seen.get(key)
        if previous is not None:
            raise UserConfigSyncError(
                "two tracked sources select the same live destination: "
                f"{previous.source_rel} and {mapping.source_rel} -> "
                f"{mapping.destination_rel}"
            )
        seen[key] = mapping


def _compare_all(
    source_root: Path, home: Path, mappings: tuple[ConfigMapping, ...]
) -> tuple[Comparison, ...]:
    return tuple(_compare_one(source_root, home, mapping) for mapping in mappings)


def _compare_one(source_root: Path, home: Path, mapping: ConfigMapping) -> Comparison:
    source = source_root / mapping.source_rel
    destination = home / mapping.destination_rel
    if not destination.exists() and not destination.is_symlink():
        return Comparison(mapping, "not installed")
    if destination.is_symlink():
        return Comparison(mapping, "drift", "live destination is a symlink")
    if mapping.kind == "file":
        if not destination.is_file():
            return Comparison(mapping, "drift", "live destination is not a file")
        if source.read_bytes() == destination.read_bytes():
            return Comparison(mapping, "clean")
        return Comparison(mapping, "drift", "file content differs")
    if not destination.is_dir():
        return Comparison(mapping, "drift", "live destination is not a directory")
    source_entries = _directory_entries(source)
    destination_entries = _directory_entries(destination)
    if source_entries == destination_entries:
        return Comparison(mapping, "clean")
    only_source = sorted(set(source_entries) - set(destination_entries))
    only_live = sorted(set(destination_entries) - set(source_entries))
    changed = sorted(
        name
        for name in set(source_entries) & set(destination_entries)
        if source_entries[name] != destination_entries[name]
    )
    details = []
    if only_source:
        details.append("missing live: " + ", ".join(only_source))
    if only_live:
        details.append("live only: " + ", ".join(only_live))
    if changed:
        details.append("different: " + ", ".join(changed))
    return Comparison(mapping, "drift", "; ".join(details))


def _directory_entries(root: Path) -> dict[str, tuple[str, str]]:
    entries: dict[str, tuple[str, str]] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root).as_posix()
        if path.is_symlink():
            entries[relative] = ("symlink", "")
        elif path.is_dir():
            entries[relative] = ("directory", "")
        elif path.is_file():
            entries[relative] = ("file", _sha256(path))
        else:
            entries[relative] = ("other", "")
    return entries


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_obj:
        for chunk in iter(lambda: file_obj.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _print_comparisons(comparisons: tuple[Comparison, ...]) -> None:
    labels = {
        "clean": "USER_CONFIG_CLEAN",
        "drift": "USER_CONFIG_DRIFT",
        "not installed": "USER_CONFIG_NOT_INSTALLED",
    }
    for comparison in comparisons:
        mapping = comparison.mapping
        detail = f" ({comparison.detail})" if comparison.detail else ""
        print(
            f"{labels[comparison.status]}: ~/{mapping.destination_rel.as_posix()}"
            f" <- {mapping.source_rel.as_posix()}{detail}"
        )


def _deploy_transaction(
    source_root: Path, home: Path, mappings: list[ConfigMapping]
) -> None:
    _validate_destinations(home, mappings)
    staged: list[_Staged] = []
    installed: list[_Installed] = []
    try:
        for mapping in mappings:
            staged.append(_stage_one(source_root, home, mapping))
        for item in staged:
            destination = item.destination
            backup = None
            if destination.exists():
                backup = _unique_sibling(destination, "backup")
                _replace_path(destination, backup)
            try:
                _replace_path(item.staged_path, destination)
            except OSError:
                if backup is not None:
                    try:
                        _replace_path(backup, destination)
                    except OSError:
                        installed.append(_Installed(destination, backup))
                        raise
                raise
            installed.append(_Installed(destination, backup))
    except (OSError, UserConfigSyncError) as exc:
        rollback_errors = _rollback(installed)
        stage_cleanup_errors = _remove_staged_paths(staged)
        detail = f"deployment failed and was rolled back: {exc}"
        if rollback_errors:
            detail += "; rollback failures: " + "; ".join(rollback_errors)
        if stage_cleanup_errors:
            detail += "; staging cleanup failures: " + "; ".join(stage_cleanup_errors)
        raise UserConfigSyncError(detail) from exc

    cleanup_errors = _remove_staged_paths(staged)
    for item in installed:
        if item.backup_path is None:
            continue
        try:
            _remove_path(item.backup_path)
        except OSError as exc:
            cleanup_errors.append(f"{item.backup_path}: {exc}")
    if cleanup_errors:
        raise UserConfigSyncError(
            "deployment succeeded but backup cleanup failed: "
            + "; ".join(cleanup_errors)
        )


def _validate_destinations(home: Path, mappings: list[ConfigMapping]) -> None:
    home = home.resolve()
    for mapping in mappings:
        destination = home / mapping.destination_rel
        if not destination.resolve(strict=False).is_relative_to(home):
            raise UserConfigSyncError(
                f"live destination escapes the selected home: {destination}"
            )
        current = destination.parent
        while current != home:
            if current.is_symlink():
                raise UserConfigSyncError(
                    f"live destination parent must not be a symlink: {current}"
                )
            current = current.parent
        if destination.is_symlink():
            raise UserConfigSyncError(
                f"live destination must not be a symlink: {destination}"
            )


def _stage_one(source_root: Path, home: Path, mapping: ConfigMapping) -> _Staged:
    source = source_root / mapping.source_rel
    destination = home / mapping.destination_rel
    destination.parent.mkdir(parents=True, exist_ok=True)
    staged_path = _unique_sibling(destination, "stage")
    try:
        if mapping.kind == "file":
            shutil.copy2(source, staged_path)
        else:
            shutil.copytree(source, staged_path)
    except OSError as exc:
        try:
            _remove_path(staged_path)
        except OSError as cleanup_exc:
            raise UserConfigSyncError(
                f"staging {source} failed: {exc}; incomplete staging path remains at "
                f"{staged_path}: {cleanup_exc}"
            ) from exc
        raise
    return _Staged(mapping, destination, staged_path)


def _unique_sibling(path: Path, role: str) -> Path:
    return path.parent / f".{path.name}.user-config-{role}-{uuid.uuid4().hex}"


def _rollback(installed: list[_Installed]) -> list[str]:
    errors = []
    for item in reversed(installed):
        try:
            _remove_path(item.destination)
            if item.backup_path is not None:
                _replace_path(item.backup_path, item.destination)
        except OSError as exc:
            errors.append(f"{item.destination}: {exc}")
    return errors


def _remove_staged_paths(staged: list[_Staged]) -> list[str]:
    errors = []
    for item in staged:
        try:
            _remove_path(item.staged_path)
        except OSError as exc:
            errors.append(f"{item.staged_path}: {exc}")
    return errors


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
    elif path.is_dir():
        shutil.rmtree(path)


def _replace_path(source: Path, destination: Path) -> None:
    os.replace(source, destination)
