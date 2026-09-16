"""Shared preflight, preservation, retirement and resume policy for all owners.

Selection and runtime adapters live in worktree_owners. Only this module removes
a reviewed worktree or its eligible merged branch. Inspection never prunes Git
registrations or sweeps unregistered folders. Retained data disposal is separate.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
import shutil
import stat
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Sequence

from mb_cmn.git_process import git_command
from mb_cmn.new_york_time import NEW_YORK
from repo_util import worktree_owners

SCHEMA_VERSION = 2

_DISPOSABLE_CACHE_DIRS = frozenset(
    {"__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache"}
)
_COMPARE_FILE_BUDGET = 500
_GIT_OPERATION_MARKERS = (
    "MERGE_HEAD",
    "CHERRY_PICK_HEAD",
    "REVERT_HEAD",
    "REBASE_HEAD",
    "BISECT_LOG",
    "rebase-merge",
    "rebase-apply",
    "sequencer",
)


class RetirementError(RuntimeError):
    """A safety gate refused worktree retirement."""


@dataclass(frozen=True)
class _Worktree:
    path: Path
    head: str | None
    branch: str | None
    locked: bool


def _git(
    repo_dir: Path, *args: str, text: bool = True
) -> subprocess.CompletedProcess[Any]:
    """Run Git with the exact local trust exception Windows worktrees need."""
    command = git_command(repo_dir, "--no-optional-locks", *args)
    return subprocess.run(
        command,
        capture_output=True,
        text=text,
        encoding="utf-8" if text else None,
        errors="replace" if text else None,
    )


def _git_ok(repo_dir: Path, *args: str) -> str:
    result = _git(repo_dir, *args)
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


def _list_worktrees(repo_dir: Path) -> list[_Worktree]:
    output = _git_ok(repo_dir, "worktree", "list", "--porcelain", "-z")
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


def _status_entries(worktree: Path) -> list[str]:
    output = _git_ok(
        worktree, "status", "--porcelain=v1", "-z", "--untracked-files=all"
    )
    return [entry for entry in output.split("\0") if entry]


def _ignored_entries(worktree: Path) -> list[str]:
    output = _git_ok(
        worktree,
        "status",
        "--porcelain=v1",
        "--ignored",
        "-z",
        "--untracked-files=all",
    )
    return [entry[3:] for entry in output.split("\0") if entry.startswith("!! ")]


def _is_disposable_cache(relative: str) -> bool:
    return any(
        component in _DISPOSABLE_CACHE_DIRS
        for component in PurePosixPath(relative).parts
    )


def _raise_walk_error(error: OSError) -> None:
    raise error


def _content_exists_elsewhere(here: Path, there: Path) -> bool:
    if here.is_symlink() or _is_reparse_point(here):
        return False
    try:
        if here.is_file():
            return (
                there.is_file()
                and not there.is_symlink()
                and not _is_reparse_point(there)
                and _file_digest(here) == _file_digest(there)
            )
        if not here.is_dir():
            return False
        seen = 0
        for directory, directory_names, file_names in os.walk(
            here, onerror=_raise_walk_error
        ):
            for name in directory_names:
                child = Path(directory) / name
                if child.is_symlink() or _is_reparse_point(child):
                    return False
            for file_name in file_names:
                seen += 1
                if seen > _COMPARE_FILE_BUDGET:
                    return False
                mine = Path(directory) / file_name
                theirs = there / mine.relative_to(here)
                if not _content_exists_elsewhere(mine, theirs):
                    return False
    except OSError:
        return False
    return True


def _file_digest(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
            size += len(chunk)
    return size, digest.hexdigest()


def _find_novc_directories(worktree: Path) -> list[Path]:
    found: list[Path] = []
    try:
        for directory, directory_names, _file_names in os.walk(
            worktree, onerror=_raise_walk_error
        ):
            parent = Path(directory)
            kept_names: list[str] = []
            for name in directory_names:
                child = parent / name
                if child.is_symlink() or _is_reparse_point(child):
                    raise RetirementError(f"refusing linked directory: {child}")
                if name == ".novc":
                    found.append(child)
                    continue
                kept_names.append(name)
            directory_names[:] = kept_names
    except OSError as exc:
        raise RetirementError(f"cannot inventory .novc directories: {exc}") from exc
    return sorted(found, key=lambda path: path.as_posix().casefold())


def _under_novc(path: Path, novc_directories: Sequence[Path]) -> bool:
    return any(_inside(path, novc) for novc in novc_directories)


def _ignored_classification(
    worktree: Path,
    primary: Path,
    ignored: Sequence[str],
    novc_directories: Sequence[Path],
) -> tuple[list[str], list[str]]:
    disposable: list[str] = []
    blockers: list[str] = []
    for relative in ignored:
        relative_path = Path(*PurePosixPath(relative.rstrip("/")).parts)
        path = worktree / relative_path
        if path.is_symlink() or _is_reparse_point(path):
            blockers.append(relative)
            continue
        if _under_novc(path, novc_directories):
            continue
        if _is_disposable_cache(relative):
            disposable.append(relative)
            continue
        if _content_exists_elsewhere(path, primary / relative_path):
            disposable.append(relative)
            continue
        blockers.append(relative)
    return disposable, blockers


def _is_reparse_point(path: Path) -> bool:
    try:
        attributes = path.lstat().st_file_attributes
    except (AttributeError, OSError):
        return False
    return bool(attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def _inventory(directory: Path) -> dict[str, Any]:
    files: list[dict[str, Any]] = []
    directories: list[str] = []
    if not directory.is_dir() or directory.is_symlink() or _is_reparse_point(directory):
        raise RetirementError(f"refusing reparse point: {directory}")
    try:
        for current, directory_names, file_names in os.walk(
            directory, onerror=_raise_walk_error
        ):
            parent = Path(current)
            relative_parent = parent.relative_to(directory)
            for name in sorted(directory_names):
                child = parent / name
                if child.is_symlink() or _is_reparse_point(child):
                    raise RetirementError(f"refusing reparse point: {child}")
                relative = (relative_parent / name).as_posix()
                directories.append(relative)
            for name in sorted(file_names):
                child = parent / name
                mode = child.lstat().st_mode
                if (
                    child.is_symlink()
                    or _is_reparse_point(child)
                    or not stat.S_ISREG(mode)
                ):
                    raise RetirementError(f"refusing non-regular file: {child}")
                digest = hashlib.sha256()
                size = 0
                with child.open("rb") as handle:
                    while chunk := handle.read(1024 * 1024):
                        digest.update(chunk)
                        size += len(chunk)
                files.append(
                    {
                        "path": (relative_parent / name).as_posix(),
                        "bytes": size,
                        "sha256": digest.hexdigest(),
                    }
                )
    except OSError as exc:
        raise RetirementError(f"cannot inventory {directory}: {exc}") from exc
    files.sort(key=lambda item: item["path"])
    directories.sort()
    membership = {"directories": directories, "files": files}
    encoded = json.dumps(
        membership, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return {
        **membership,
        "file_count": len(files),
        "total_bytes": sum(item["bytes"] for item in files),
        "tree_sha256": hashlib.sha256(encoded).hexdigest(),
        "verification_algorithm": "sha256-file-manifest-v1",
    }


def _tracked_novc_citations(worktree: Path) -> list[dict[str, Any]]:
    result = _git(
        worktree,
        "grep",
        "-l",
        "-z",
        "-I",
        "-e",
        ".novc",
        "--",
        text=False,
    )
    if result.returncode not in (0, 1):
        message = result.stderr.decode("utf-8", errors="replace").strip()
        raise RetirementError(f"git grep for .novc citations failed: {message}")
    paths = [entry for entry in result.stdout.split(b"\0") if entry]
    citations: list[dict[str, Any]] = []
    for encoded_path in paths:
        relative = encoded_path.decode("utf-8", errors="surrogateescape")
        try:
            lines = (worktree / relative).read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError) as exc:
            raise RetirementError(
                f"cannot review tracked citation {relative}: {exc}"
            ) from exc
        for line_number, line in enumerate(lines, start=1):
            if ".novc" in line:
                citations.append(
                    {
                        "path": PurePosixPath(relative).as_posix(),
                        "line": line_number,
                        "text": line[:500],
                    }
                )
    return citations


def _operation_markers(worktree: Path) -> list[str]:
    present: list[str] = []
    for marker in _GIT_OPERATION_MARKERS:
        path_text = _git_ok(worktree, "rev-parse", "--git-path", marker).strip()
        marker_path = Path(path_text)
        if not marker_path.is_absolute():
            marker_path = worktree / marker_path
        if path_text and marker_path.exists():
            present.append(marker)
    return present


def _head_reflog_protection(worktree: Path, primary: Path) -> list[dict[str, Any]]:
    result = _git(worktree, "reflog", "show", "--format=%H", "HEAD")
    if result.returncode != 0:
        raise RetirementError(
            "cannot audit the worktree HEAD reflog: "
            + (result.stderr.strip() or "git reflog failed")
        )
    commits = list(
        dict.fromkeys(line.strip() for line in result.stdout.splitlines() if line)
    )
    protected: list[dict[str, Any]] = []
    for commit in commits:
        refs = _git_ok(
            primary,
            "for-each-ref",
            "--format=%(refname)",
            "--contains",
            commit,
            "refs/heads/",
            "refs/remotes/",
            "refs/tags/",
        ).splitlines()
        durable_refs = sorted(ref for ref in refs if ref.strip())
        if not durable_refs:
            raise RetirementError(
                f"HEAD reflog commit {commit} has no durable branch, remote, or tag ref"
            )
        protected.append({"commit": commit, "durable_refs": durable_refs})
    return protected


def _per_worktree_ref_protection(worktree: Path, primary: Path) -> list[dict[str, Any]]:
    """Verify that per-worktree refs do not uniquely preserve a commit."""
    output = _git_ok(
        worktree,
        "for-each-ref",
        "--format=%(refname)%00%(objectname)",
        "refs/bisect/",
        "refs/worktree/",
        "refs/rewritten/",
    )
    fields = [field for field in output.replace("\n", "\0").split("\0") if field]
    if len(fields) % 2:
        raise RetirementError("cannot parse per-worktree refs")
    protected: list[dict[str, Any]] = []
    for index in range(0, len(fields), 2):
        refname, object_name = fields[index : index + 2]
        object_type = _git_ok(primary, "cat-file", "-t", object_name).strip()
        if object_type != "commit":
            raise RetirementError(
                f"per-worktree ref {refname} preserves unsupported {object_type} object"
            )
        refs = _git_ok(
            primary,
            "for-each-ref",
            "--format=%(refname)",
            "--contains",
            object_name,
            "refs/heads/",
            "refs/remotes/",
            "refs/tags/",
        ).splitlines()
        durable_refs = sorted(ref for ref in refs if ref.strip())
        if not durable_refs:
            raise RetirementError(
                f"per-worktree ref {refname} is the only ref protecting {object_name}"
            )
        protected.append(
            {
                "ref": refname,
                "commit": object_name,
                "durable_refs": durable_refs,
            }
        )
    return protected


def _shadow_parts(path: Path) -> tuple[str, ...]:
    resolved = path.resolve()
    drive = resolved.drive
    if drive.startswith("\\\\"):
        unc_parts = tuple(part for part in drive.lstrip("\\").split("\\") if part)
        remainder = resolved.parts[1:]
        return ("unc", *unc_parts, *remainder)
    if drive:
        label = drive.rstrip(":\\/").upper()
        return (f"drive-{label}", *resolved.parts[1:])
    if resolved.is_absolute():
        return ("root", *resolved.parts[1:])
    raise RetirementError(f"retirement source is not absolute: {path}")


def _retirement_id() -> str:
    timestamp = datetime.now(NEW_YORK).strftime("%Y%m%dT%H%M%S%z")
    return f"{timestamp}-{secrets.token_hex(4)}"


def _destinations(
    retirement_root: Path, novc_directories: Sequence[Path]
) -> tuple[str, list[dict[str, str]]]:
    for _attempt in range(20):
        identifier = _retirement_id()
        destinations: list[dict[str, str]] = []
        collision = False
        for source in novc_directories:
            parent = retirement_root.joinpath(*_shadow_parts(source.parent))
            destination = parent / f".novc--{identifier}"
            sidecar = parent / f".novc--{identifier}.json"
            if os.path.lexists(destination) or os.path.lexists(sidecar):
                collision = True
                break
            destinations.append(
                {
                    "source": str(source),
                    "destination": str(destination),
                    "sidecar": str(sidecar),
                }
            )
        if not collision:
            return identifier, destinations
    raise RetirementError("could not allocate collision-free retirement destinations")


def _safety_snapshot(worktree_path: Path) -> dict[str, Any]:
    worktree_path = worktree_path.resolve()
    root = Path(_git_ok(worktree_path, "rev-parse", "--show-toplevel").strip())
    if not _same_path(root, worktree_path):
        raise RetirementError(
            f"target is not the exact worktree root: {worktree_path} (root is {root})"
        )

    worktrees = _list_worktrees(worktree_path)
    primary = worktrees[0].path.resolve()
    common_directory = Path(
        _git_ok(
            worktree_path,
            "rev-parse",
            "--path-format=absolute",
            "--git-common-dir",
        ).strip()
    )
    primary_common_directory = Path(
        _git_ok(
            primary, "rev-parse", "--path-format=absolute", "--git-common-dir"
        ).strip()
    )
    if not _same_path(common_directory, primary_common_directory):
        raise RetirementError(
            "worktree does not share the primary repository's object directory"
        )
    matches = [record for record in worktrees if _same_path(record.path, worktree_path)]
    if len(matches) != 1:
        raise RetirementError(
            "target is not exactly one linked worktree of its repository"
        )
    worktree = matches[0]
    if _same_path(worktree.path, primary):
        raise RetirementError("refusing to retire the primary worktree")
    found_owners = worktree_owners.owners(worktree.path, worktree.branch, primary)
    if len(found_owners) > 1:
        raise RetirementError(
            "conflicting worktree ownership: " + ", ".join(found_owners)
        )
    for other in worktrees:
        if not _same_path(other.path, worktree_path) and _inside(
            other.path, worktree_path
        ):
            raise RetirementError(
                f"target contains another registered worktree: {other.path}"
            )
    runtime = _check_runtime(worktree_path)
    if worktree.locked:
        raise RetirementError("worktree is locked")
    if _inside(Path.cwd(), worktree_path) or _inside(Path(__file__), worktree_path):
        raise RetirementError("refusing to retire the checkout running this command")
    if worktree.head is None:
        raise RetirementError("worktree has no readable HEAD")

    status_entries = _status_entries(worktree_path)
    if status_entries:
        raise RetirementError(
            "worktree has tracked or untracked changes: "
            + ", ".join(status_entries[:10])
        )
    markers = _operation_markers(worktree_path)
    if markers:
        raise RetirementError(
            "worktree has an in-progress Git operation: " + ", ".join(markers)
        )

    default = _default_branch(primary)
    if not _is_ancestor(primary, worktree.head, default):
        raise RetirementError(f"worktree HEAD is not integrated into {default}")
    if worktree.branch is not None:
        branch_head = _git_ok(primary, "rev-parse", worktree.branch).strip()
        if branch_head != worktree.head:
            raise RetirementError(
                f"branch {worktree.branch} does not point at worktree HEAD"
            )
        if not _is_ancestor(primary, worktree.branch, default):
            raise RetirementError(
                f"branch {worktree.branch} is not merged into {default}"
            )

    reflog = _head_reflog_protection(worktree_path, primary)
    per_worktree_refs = _per_worktree_ref_protection(worktree_path, primary)
    administration = _administration_protection(
        worktree_path,
        primary,
        (
            worktree.branch
            if worktree_owners.deletable_branch(worktree.branch, found_owners)
            else None
        ),
    )
    novc_directories = _find_novc_directories(worktree_path)
    for novc in novc_directories:
        relative_novc = novc.relative_to(worktree_path).as_posix()
        tracked = _git_ok(worktree_path, "ls-files", "-z", "--", relative_novc)
        if tracked:
            raise RetirementError(f".novc directory contains tracked files: {novc}")
        ignored = _git(worktree_path, "check-ignore", "-q", "--", relative_novc)
        if ignored.returncode != 0 and any(novc.iterdir()):
            raise RetirementError(
                f"content-bearing .novc directory is not ignored: {novc}"
            )

    ignored_entries = _ignored_entries(worktree_path)
    disposable, ignored_blockers = _ignored_classification(
        worktree_path, primary, ignored_entries, novc_directories
    )
    if ignored_blockers:
        raise RetirementError(
            "unique ignored content outside .novc blocks retirement: "
            + ", ".join(ignored_blockers[:10])
        )

    novc = [
        {"path": str(directory), "inventory": _inventory(directory)}
        for directory in novc_directories
    ]
    return {
        "owners": found_owners,
        "delete_branch": worktree_owners.deletable_branch(
            worktree.branch, found_owners
        ),
        "runtime": runtime,
        "primary_repository_path": str(primary),
        "git_common_directory": str(common_directory),
        "worktree_path": str(worktree_path),
        "head": worktree.head,
        "branch": worktree.branch,
        "detached": worktree.branch is None,
        "locked": worktree.locked,
        "default_branch": default,
        "status_entries": status_entries,
        "git_operation_markers": markers,
        "head_reflog_protection": reflog,
        "per_worktree_ref_protection": per_worktree_refs,
        "administration_protection": administration,
        "novc_directories": novc,
        "disposable_ignored_entries": disposable,
        "ignored_blockers": ignored_blockers,
        "tracked_novc_citations": [
            {"checkout": str(checkout), **citation}
            for checkout in (worktree_path, primary)
            for citation in _tracked_novc_citations(checkout)
        ],
    }


def _fingerprint(snapshot: dict[str, Any]) -> str:
    encoded = json.dumps(
        snapshot, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _check_runtime(worktree: Path) -> dict[str, Any]:
    if _inside(Path.cwd(), worktree) or _inside(Path(__file__), worktree):
        raise RetirementError("refusing to retire the checkout running this command")
    facts = worktree_owners.runtime_facts(worktree)
    if facts["blockers"]:
        raise RetirementError("; ".join(facts["blockers"]))
    return facts


def _administration_protection(
    worktree: Path, primary: Path, deleting_branch: str | None
) -> list[dict[str, Any]]:
    """Protect recovery evidence that vanishes with the worktree administration."""
    admin = Path(_git_ok(worktree, "rev-parse", "--absolute-git-dir").strip())
    for name in ("objects", "lost-found"):
        local = admin / name
        if local.exists() and any(local.iterdir()):
            raise RetirementError(
                f"worktree administration holds local objects: {local}"
            )
    commits = set()
    logs = admin / "logs"
    log_files = []
    if logs.exists():
        for directory, _directories, files in os.walk(logs, onerror=_raise_walk_error):
            log_files.extend(Path(directory) / name for name in files)
    if deleting_branch:
        commits.update(_branch_recovery_commits(primary, deleting_branch))
    for log in log_files:
        for line in log.read_text(encoding="utf-8").splitlines():
            fields = line.split()
            if len(fields) < 2:
                raise RetirementError(f"cannot parse worktree or branch reflog: {log}")
            commits.update(fields[:2])
    for name in ("ORIG_HEAD", "FETCH_HEAD", "AUTO_MERGE"):
        pseudoref = admin / name
        if pseudoref.exists():
            for line in pseudoref.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    commits.add(line.split()[0])
    return _protect_recovery_commits(primary, commits, deleting_branch)


def _branch_recovery_commits(primary: Path, branch: str) -> set[str]:
    """Read both sides of the current branch reflog, including during resume."""
    common = Path(
        _git_ok(
            primary, "rev-parse", "--path-format=absolute", "--git-common-dir"
        ).strip()
    )
    branch_log = common / "logs" / "refs" / "heads" / branch
    commits = set()
    if branch_log.exists():
        for line in branch_log.read_text(encoding="utf-8").splitlines():
            fields = line.split()
            if len(fields) < 2:
                raise RetirementError(f"cannot parse branch reflog: {branch_log}")
            commits.update(fields[:2])
    return commits


def _protect_recovery_commits(
    primary: Path, commits: set[str], deleting_branch: str | None
) -> list[dict[str, Any]]:
    protected = []
    for commit in sorted(commits):
        if set(commit) == {"0"}:
            continue
        kind = _git_ok(primary, "cat-file", "-t", commit).strip()
        if kind != "commit":
            raise RetirementError(
                f"administration uniquely records {kind} object {commit}"
            )
        refs = _git_ok(
            primary,
            "for-each-ref",
            "--format=%(refname)",
            "--contains",
            commit,
            "refs/heads/",
            "refs/remotes/",
            "refs/tags/",
        ).splitlines()
        refs = [ref for ref in refs if ref != f"refs/heads/{deleting_branch}"]
        if not refs:
            raise RetirementError(f"administration commit has no durable ref: {commit}")
        protected.append({"commit": commit, "durable_refs": sorted(refs)})
    return protected


def select_worktrees(
    repo_dir: Path, *, owner: str = "both", exact: Path | None = None
) -> list[_Worktree]:
    """Select registrations only; do not inspect or mutate unselected checkouts."""
    records = _list_worktrees(repo_dir)
    if exact is not None:
        matches = [record for record in records if _same_path(record.path, exact)]
        if len(matches) != 1:
            raise RetirementError(f"not an exact registered worktree: {exact}")
        return matches
    return [
        record
        for record in records[1:]
        if worktree_owners.selected(
            worktree_owners.owners(record.path, record.branch, records[0].path), owner
        )
    ]


def inspect_worktrees(
    repo_dir: Path, *, owner: str = "both", exact: Path | None = None
) -> list[dict[str, Any]]:
    """Read safety facts and blockers. A clean inspection is not an ended task."""
    reports = []
    for record in select_worktrees(repo_dir, owner=owner, exact=exact):
        try:
            snapshot = _safety_snapshot(record.path)
            reports.append(
                {"worktree": str(record.path), "snapshot": snapshot, "blocker": None}
            )
        except (RetirementError, OSError) as exc:
            reports.append({"worktree": str(record.path), "blocker": str(exc)})
    return reports


def _preflight_plan_fingerprint(preflight: dict[str, Any]) -> str:
    plan = dict(preflight)
    plan.pop("execution", None)
    plan.pop("plan_fingerprint", None)
    return _fingerprint(plan)


def _write_json_exclusive(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def prepare_retirement(
    worktree_path: Path,
    *,
    retirement_root: Path,
    preflight_file: Path,
    task_ended: bool,
    codex_task_ids: Sequence[str] = (),
    owner_selector: str | None = None,
    citations_reviewed: bool = False,
    citation_note: str | None = None,
) -> dict[str, Any]:
    """Audit without changing the target and write a collision-safe preflight."""
    if not task_ended:
        raise RetirementError("preflight requires an explicit ended-task attestation")
    worktree_path = worktree_path.resolve()
    retirement_root = retirement_root.resolve()
    preflight_file = preflight_file.resolve()
    if _inside(retirement_root, worktree_path):
        raise RetirementError("retirement root must be outside the retiring worktree")
    if _inside(preflight_file, worktree_path):
        raise RetirementError("preflight file must be outside the retiring worktree")
    snapshot = _safety_snapshot(worktree_path)
    if owner_selector is not None and not worktree_owners.selected(
        snapshot["owners"], owner_selector
    ):
        raise RetirementError(f"target is outside {owner_selector} selection")
    citations = snapshot["tracked_novc_citations"]
    if (
        citations_reviewed
        and citations
        and not (citation_note and citation_note.strip())
    ):
        raise RetirementError("reviewed citations require a non-empty citation note")
    identifier, destinations = _destinations(
        retirement_root,
        [Path(item["path"]) for item in snapshot["novc_directories"]],
    )
    ready = not citations or citations_reviewed
    preflight = {
        "schema_version": SCHEMA_VERSION,
        "kind": "worktree-retirement-preflight",
        "created_at": datetime.now(NEW_YORK).isoformat(),
        "task_ended_attested": True,
        "owner_selector": owner_selector,
        "codex_task_ids": sorted(
            set(codex_task_ids) | set(snapshot["runtime"]["codex_task_ids"])
        ),
        "claude_session_ids": snapshot["runtime"]["claude_session_ids"],
        "citations_reviewed": citations_reviewed,
        "citation_note": citation_note,
        "ready_for_execution": ready,
        "retirement_root": str(retirement_root),
        "retirement_id": identifier,
        "destinations": destinations,
        "snapshot": snapshot,
        "safety_fingerprint": _fingerprint(snapshot),
    }
    preflight["plan_fingerprint"] = _preflight_plan_fingerprint(preflight)
    _write_json_exclusive(preflight_file, preflight)
    print(f"Worktree retirement preflight: {preflight_file}")
    print(f"ready for execution: {'yes' if ready else 'no; review .novc citations'}")
    for item in snapshot["novc_directories"]:
        inventory = item["inventory"]
        print(
            f"retain {item['path']}: {inventory['file_count']} file(s), "
            f"{inventory['total_bytes']} byte(s)"
        )
    if citations:
        print(f"tracked .novc citations: {len(citations)}")
        for citation in citations:
            print(
                f"  {citation['checkout']}/{citation['path']}:{citation['line']}: {citation['text']}"
            )
    return preflight


def _same_volume(left: Path, right: Path) -> bool:
    return os.path.normcase(left.resolve().drive) == os.path.normcase(
        right.resolve().drive
    )


def _write_sidecar(path: Path, metadata: dict[str, Any]) -> None:
    _write_json_exclusive(path, metadata)


def _update_sidecar(path: Path, metadata: dict[str, Any]) -> None:
    temporary = path.with_name(path.name + f".tmp-{secrets.token_hex(4)}")
    _write_json_exclusive(temporary, metadata)
    os.replace(temporary, path)


def _measure_residue(path: Path) -> dict[str, Any]:
    """Measure an unregistered directory without requiring access to every entry."""
    residue: dict[str, Any] = {
        "path": str(path),
        "exists": os.path.lexists(path),
        "file_count_readable": 0,
        "total_bytes_readable": 0,
        "file_count_is_lower_bound": False,
        "total_bytes_is_lower_bound": False,
        "unreadable_entry_count": 0,
        "unreadable_entries": [],
    }
    if not residue["exists"]:
        return residue

    unreadable: list[str] = []

    def record_unreadable(candidate: Path | str) -> None:
        unreadable.append(str(candidate))

    def on_error(error: OSError) -> None:
        record_unreadable(error.filename or path)

    try:
        for directory, directory_names, file_names in os.walk(
            path, followlinks=False, onerror=on_error
        ):
            parent = Path(directory)
            kept_directories = []
            for name in directory_names:
                child = parent / name
                try:
                    if child.is_symlink() or _is_reparse_point(child):
                        record_unreadable(child)
                    else:
                        kept_directories.append(name)
                except OSError:
                    record_unreadable(child)
            directory_names[:] = kept_directories
            for name in file_names:
                child = parent / name
                try:
                    file_stat = child.lstat()
                    if child.is_symlink() or _is_reparse_point(child):
                        record_unreadable(child)
                        continue
                    if not stat.S_ISREG(file_stat.st_mode):
                        record_unreadable(child)
                        continue
                    with child.open("rb") as handle:
                        handle.read(1)
                    residue["file_count_readable"] += 1
                    residue["total_bytes_readable"] += file_stat.st_size
                except OSError:
                    record_unreadable(child)
    except OSError:
        record_unreadable(path)

    unique_unreadable = list(dict.fromkeys(unreadable))
    residue["unreadable_entry_count"] = len(unique_unreadable)
    residue["unreadable_entries"] = unique_unreadable[:20]
    lower_bound = bool(unique_unreadable)
    residue["file_count_is_lower_bound"] = lower_bound
    residue["total_bytes_is_lower_bound"] = lower_bound
    return residue


def _is_registered(primary: Path, worktree: Path) -> bool:
    return any(
        _same_path(record.path, worktree) for record in _list_worktrees(primary)[1:]
    )


def _snapshot_after_relocations(
    old_snapshot: dict[str, Any], completed_sources: set[str]
) -> dict[str, Any]:
    expected = json.loads(json.dumps(old_snapshot))
    expected["novc_directories"] = [
        item
        for item in expected["novc_directories"]
        if item["path"] not in completed_sources
    ]
    return expected


def _reconcile_relocations(
    preflight: dict[str, Any],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    inventories = {
        item["path"]: item["inventory"]
        for item in preflight["snapshot"]["novc_directories"]
    }
    pending: list[dict[str, str]] = []
    completed: list[dict[str, str]] = []
    for item in preflight["destinations"]:
        source = Path(item["source"])
        destination = Path(item["destination"])
        sidecar = Path(item["sidecar"])
        source_exists = source.exists()
        destination_exists = destination.exists()
        sidecar_exists = sidecar.exists()
        if source_exists and not destination_exists and not sidecar_exists:
            pending.append(item)
            continue
        if not source_exists and destination_exists and sidecar_exists:
            if _inventory(destination) != inventories[item["source"]]:
                raise RetirementError(
                    f"retained destination no longer verifies: {destination}"
                )
            try:
                metadata = json.loads(sidecar.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                raise RetirementError(
                    f"cannot verify sidecar {sidecar}: {exc}"
                ) from exc
            if (
                metadata.get("original_novc_path") != item["source"]
                or metadata.get("destination") != item["destination"]
                or metadata.get("disposition") != "retained"
                or metadata.get("retirement_id") != preflight["retirement_id"]
                or metadata.get("original_worktree_path")
                != preflight["snapshot"]["worktree_path"]
                or metadata.get("primary_repository_path")
                != preflight["snapshot"]["primary_repository_path"]
                or metadata.get("head") != preflight["snapshot"]["head"]
                or metadata.get("branch") != preflight["snapshot"]["branch"]
                or metadata.get("verification") != inventories[item["source"]]
            ):
                raise RetirementError(
                    f"sidecar does not verify retained data: {sidecar}"
                )
            completed.append(item)
            continue
        raise RetirementError(
            "ambiguous partial .novc relocation; leave both paths in place and inspect: "
            f"source={source} destination={destination} sidecar={sidecar}"
        )
    return pending, completed


def _relocate_novc(
    source: Path,
    destination: Path,
    sidecar: Path,
    *,
    inventory: dict[str, Any],
    common_metadata: dict[str, Any],
) -> dict[str, Any]:
    if os.path.lexists(destination) or os.path.lexists(sidecar):
        raise RetirementError(f"retirement destination collision: {destination}")
    if _inventory(source) != inventory:
        raise RetirementError(f".novc source drift before relocation: {source}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    method = (
        "same-volume-rename"
        if _same_volume(source, destination)
        else "copy-verify-remove"
    )
    metadata = {
        **common_metadata,
        "original_novc_path": str(source),
        "destination": str(destination),
        "file_count": inventory["file_count"],
        "total_bytes": inventory["total_bytes"],
        "verification": inventory,
        "relocation_method": method,
        "disposition": "relocation_pending",
        "worktree_registered": True,
        "worktree_removed": False,
        "branch_deleted": False,
    }
    _write_sidecar(sidecar, metadata)
    try:
        if method == "same-volume-rename":
            source.rename(destination)
            verified = _inventory(destination)
            if verified != inventory:
                raise RetirementError(f"post-move verification failed for {source}")
        else:
            shutil.copytree(source, destination)
            verified = _inventory(destination)
            if verified != inventory:
                raise RetirementError(
                    f"cross-volume copy verification failed; source retained at {source}"
                )
            if _inventory(source) != inventory:
                raise RetirementError(
                    f"cross-volume source changed; source retained at {source}"
                )
            shutil.rmtree(source)
    except Exception as exc:
        if (
            method == "same-volume-rename"
            and not source.exists()
            and destination.exists()
        ):
            destination.rename(source)
        metadata["disposition"] = "relocation_failed"
        metadata["failure"] = str(exc)
        _update_sidecar(sidecar, metadata)
        if isinstance(exc, RetirementError):
            raise
        raise RetirementError(f".novc relocation failed for {source}: {exc}") from exc
    metadata["disposition"] = "retained"
    _update_sidecar(sidecar, metadata)
    print(
        f"retained {source} -> {destination} "
        f"({inventory['file_count']} file(s), {inventory['total_bytes']} byte(s))"
    )
    return metadata


def execute_retirement(
    preflight_file: Path, *, confirm_task_ended: bool, owner_selector: str | None = None
) -> dict[str, Any]:
    """Revalidate, retain ``.novc``, and make the best ordinary-token cleanup."""
    if not confirm_task_ended:
        raise RetirementError("execution requires a fresh ended-task confirmation")
    preflight_file = preflight_file.resolve()
    try:
        preflight = json.loads(preflight_file.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise RetirementError(f"cannot read preflight {preflight_file}: {exc}") from exc
    if preflight.get("schema_version") != SCHEMA_VERSION:
        raise RetirementError("unsupported retirement preflight schema")
    if preflight.get("kind") != "worktree-retirement-preflight":
        raise RetirementError("file is not a Worktree retirement preflight")
    if not preflight.get("ready_for_execution"):
        raise RetirementError(
            "preflight is not ready; its .novc citation audit is pending"
        )
    if preflight.get("plan_fingerprint") != _preflight_plan_fingerprint(preflight):
        raise RetirementError("preflight plan changed after it was prepared")

    old_snapshot = preflight["snapshot"]
    if owner_selector is not None and not worktree_owners.selected(
        old_snapshot["owners"], owner_selector
    ):
        raise RetirementError(f"preflight is outside {owner_selector} selection")
    worktree = Path(old_snapshot["worktree_path"])
    primary = Path(old_snapshot["primary_repository_path"])
    if _inside(preflight_file, worktree):
        raise RetirementError("preflight file is inside the retiring worktree")
    if preflight.get("safety_fingerprint") != _fingerprint(old_snapshot):
        raise RetirementError("preflight safety snapshot changed after preparation")
    expected_sources = {
        item["path"]: item["inventory"] for item in old_snapshot["novc_directories"]
    }
    destinations = preflight["destinations"]
    if {item["source"] for item in destinations} != set(expected_sources):
        raise RetirementError(
            "preflight destination set does not match .novc inventory"
        )
    retirement_root = Path(preflight["retirement_root"])
    for item in destinations:
        destination = Path(item["destination"])
        sidecar = Path(item["sidecar"])
        if (
            not _inside(destination, retirement_root)
            or not _inside(sidecar, retirement_root)
            or _inside(destination, worktree)
            or _inside(sidecar, worktree)
        ):
            raise RetirementError("preflight contains an unsafe retirement destination")

    _check_runtime(worktree)
    pending, completed = _reconcile_relocations(preflight)
    completed_sources = {item["source"] for item in completed}
    registered = _is_registered(primary, worktree)
    if registered:
        current_snapshot = _safety_snapshot(worktree)
        expected_snapshot = _snapshot_after_relocations(old_snapshot, completed_sources)
        if _fingerprint(current_snapshot) != _fingerprint(expected_snapshot):
            raise RetirementError(
                "worktree safety facts drifted since preflight; create and review a new preflight"
            )
    elif not preflight.get("execution", {}).get("removal_authorized"):
        raise RetirementError(
            "target unregistered outside this preflight; cannot resume"
        )
    elif pending:
        raise RetirementError(
            "worktree is already unregistered but some .novc sources were not relocated; "
            "leave the residue in place and inspect it"
        )

    execution = preflight.setdefault("execution", {})
    execution.setdefault("started_at", datetime.now(NEW_YORK).isoformat())
    execution["ordinary_token"] = True
    execution["elevation_requested"] = False
    execution["worktree_registered_before_attempt"] = registered
    execution["stage"] = "relocating_novc"
    execution["relocated_sources"] = sorted(completed_sources)
    _update_sidecar(preflight_file, preflight)

    retired_at = execution["started_at"]
    common_metadata = {
        "schema_version": SCHEMA_VERSION,
        "kind": "worktree-retired-novc",
        "retirement_id": preflight["retirement_id"],
        "original_worktree_path": old_snapshot["worktree_path"],
        "primary_repository_path": old_snapshot["primary_repository_path"],
        "git_common_directory": old_snapshot["git_common_directory"],
        "head": old_snapshot["head"],
        "branch": old_snapshot["branch"],
        "detached": old_snapshot["detached"],
        "owners": old_snapshot["owners"],
        "codex_task_ids": preflight.get("codex_task_ids", []),
        "claude_session_ids": preflight.get("claude_session_ids", []),
        "retired_at": retired_at,
        "citation_review": {
            "citations": old_snapshot["tracked_novc_citations"],
            "note": preflight.get("citation_note"),
        },
    }
    for item in pending:
        source = Path(item["source"])
        sidecar = Path(item["sidecar"])
        _relocate_novc(
            source,
            Path(item["destination"]),
            sidecar,
            inventory=expected_sources[item["source"]],
            common_metadata=common_metadata,
        )
        completed_sources.add(item["source"])
        execution["relocated_sources"] = sorted(completed_sources)
        _update_sidecar(preflight_file, preflight)

    pending, completed = _reconcile_relocations(preflight)
    if pending:
        raise RetirementError("not every .novc relocation completed")

    if registered:
        # This is the last safety read before the first Git mutation.  The only
        # expected difference from the reviewed preflight is that its .novc
        # directories now live at their verified retained destinations.
        current_snapshot = _safety_snapshot(worktree)
        expected_snapshot = _snapshot_after_relocations(
            old_snapshot, set(expected_sources)
        )
        if _fingerprint(current_snapshot) != _fingerprint(expected_snapshot):
            raise RetirementError(
                "worktree drifted after .novc relocation; worktree left registered"
            )
        execution["stage"] = "removing_worktree"
        execution["removal_authorized"] = True
        _update_sidecar(preflight_file, preflight)
        remove = _git(primary, "worktree", "remove", str(worktree))
        remove_error = (
            None
            if remove.returncode == 0
            else (remove.stderr.strip() or "git worktree remove failed")
        )
    else:
        remove_error = None

    registered_after = _is_registered(primary, worktree)
    residue = _measure_residue(worktree)
    execution["worktree_registered"] = registered_after
    execution["residue"] = residue
    if remove_error is not None:
        execution["git_worktree_remove_message"] = remove_error

    sidecars: list[tuple[Path, dict[str, Any]]] = []
    for item in completed:
        sidecar = Path(item["sidecar"])
        metadata = json.loads(sidecar.read_text(encoding="utf-8"))
        metadata["worktree_registered"] = registered_after
        metadata["worktree_removed"] = not residue["exists"]
        metadata["residue"] = residue
        _update_sidecar(sidecar, metadata)
        sidecars.append((sidecar, metadata))

    if registered_after:
        execution["stage"] = "worktree_removal_failed"
        _update_sidecar(preflight_file, preflight)
        detail = remove_error or "worktree remains registered"
        raise RetirementError(
            "ordinary-token worktree removal did not unregister the target; "
            f"it remains in place ({detail})"
        )

    if residue["exists"]:
        qualifier = "at least " if residue["total_bytes_is_lower_bound"] else ""
        print(
            f"Worktree unregistered; residue retained at {residue['path']}: "
            f"{qualifier}{residue['file_count_readable']} readable file(s), "
            f"{qualifier}{residue['total_bytes_readable']} readable byte(s), "
            f"{residue['unreadable_entry_count']} unreadable entry or subtree path(s)"
        )
    else:
        print(f"removed Worktree {worktree}")

    branch = old_snapshot["branch"]
    branch_deleted = False
    if branch is not None and old_snapshot["delete_branch"]:
        if not worktree_owners.deletable_branch(branch, old_snapshot["owners"]):
            raise RetirementError(
                f"branch is not eligible for the recorded owner: {branch}"
            )
        exists = _git(
            primary, "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"
        )
        if exists.returncode not in (0, 1):
            raise RetirementError(
                f"cannot determine whether worktree branch still exists: {branch}"
            )
        if exists.returncode == 0:
            branch_tip = _git_ok(primary, "rev-parse", branch).strip()
            if branch_tip != old_snapshot["head"]:
                raise RetirementError(
                    f"worktree branch moved after preflight and will not be deleted: {branch}"
                )
            if not _is_ancestor(primary, branch, old_snapshot["default_branch"]):
                raise RetirementError(
                    f"worktree branch is no longer merged into {old_snapshot['default_branch']}"
                )
            # A resumed removal may run long after its original audit. Recheck
            # recovery commits against refs that survive deleting this branch.
            recovery_commits = {
                item["commit"] for item in old_snapshot["administration_protection"]
            }
            recovery_commits.update(_branch_recovery_commits(primary, branch))
            _protect_recovery_commits(primary, recovery_commits, branch)
            delete = _git(primary, "branch", "-d", branch)
            if delete.returncode != 0:
                execution["stage"] = "branch_deletion_failed"
                execution["branch_error"] = (
                    delete.stderr.strip() or "git branch -d failed"
                )
                _update_sidecar(preflight_file, preflight)
                raise RetirementError(
                    f"worktree unregistered, but safe branch deletion failed for {branch}: "
                    + execution["branch_error"]
                )
            print(f"deleted merged worktree branch {branch}")
        branch_deleted = True

    if branch_deleted:
        for sidecar, metadata in sidecars:
            metadata["branch_deleted"] = True
            _update_sidecar(sidecar, metadata)
    execution["branch_deleted"] = branch_deleted
    execution["stage"] = "complete_with_residue" if residue["exists"] else "complete"
    execution["completed_at"] = datetime.now(NEW_YORK).isoformat()
    _update_sidecar(preflight_file, preflight)
    return {
        "worktree_registered": False,
        "worktree_removed": not residue["exists"],
        "residue": residue,
        "branch_deleted": branch if branch_deleted else None,
        "retained_novc": [item["destination"] for item in destinations],
    }
