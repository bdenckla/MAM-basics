"""Read-only worktree inspection, and the safety snapshot a retirement plan records.

Preparation records ``_safety_snapshot`` in the preflight, and execution derives it again
and requires it unchanged apart from the ``.novc`` relocations the plan made.  Selection
and inspection read registrations and working trees; they never prune a registration or
sweep a folder.
"""

from __future__ import annotations

import hashlib
import json
import os
import stat
from pathlib import Path, PurePosixPath
from typing import Any, Sequence

from repo_util import worktree_owners
from repo_util.worktree_retirement_git import (
    RetirementError,
    _Worktree,
    _default_branch,
    _git,
    _git_ok,
    _inside,
    _is_ancestor,
    _list_worktrees,
    _path_key,
    _same_path,
)

_DISPOSABLE_CACHE_DIRS = frozenset(
    {"__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache"}
)
# py/main_test.py's _add_windows_basetemp puts pytest's per-process base temporary
# directories below this child of a checkout's root .novc on Windows. Retirement
# relocates it with the rest of that .novc, but it is disposable cache: no spelling
# of it, or of anything below it, is a citation that gates retirement.
_SUITE_BASETEMP_NOVC_CHILD = "t"


def _is_suite_basetemp(relative: str) -> bool:
    return PurePosixPath(relative).parts[:1] == (_SUITE_BASETEMP_NOVC_CHILD,)


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


def _status_entries(
    worktree: Path,
    *,
    timeout_seconds: int | None = None,
    noninteractive: bool = False,
) -> list[str]:
    output = _git_ok(
        worktree,
        "status",
        "--porcelain=v1",
        "-z",
        "--untracked-files=all",
        timeout_seconds=timeout_seconds,
        noninteractive=noninteractive,
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


def _normalized_reference(path: Path) -> str:
    return os.path.normcase(str(path.resolve())).replace("\\", "/")


def _reference_matches(line: str, reference: str, *, directory: bool) -> bool:
    normalized_line = os.path.normcase(line).replace("\\", "/")
    path_characters = frozenset("._~-:/%")
    delimiters = frozenset(" \t\r\n`'\"<>|()[]{};,")
    start = 0
    while (index := normalized_line.find(reference, start)) >= 0:
        before = normalized_line[index - 1] if index else ""
        tail = normalized_line[index + len(reference) :]
        if (
            directory
            and tail.startswith("/")
            and (len(tail) == 1 or tail[1] in delimiters or tail[1] in ".!")
        ):
            tail = tail[1:]
        punctuation = 0
        while punctuation < len(tail) and tail[punctuation] in ".!?:":
            punctuation += 1
        boundary = (
            not tail
            or tail[0] in delimiters
            or (
                punctuation > 0
                and (punctuation == len(tail) or tail[punctuation] in delimiters)
            )
        )
        before_is_path = bool(
            before and (before.isalnum() or before in path_characters)
        )
        if not before_is_path and boundary:
            return True
        start = index + 1
    return False


def _citation_references(
    checkout: Path,
    primary: Path,
    retirement_target: Path,
    relocation_records: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Name only source roots and members of the frozen relocation inventory."""
    references: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    retirement_target = retirement_target.resolve()
    for item in relocation_records:
        source = Path(item["path"]).resolve()
        if not _inside(source, retirement_target):
            raise RetirementError(
                f".novc source is outside the retirement target: {source}"
            )
        root_novc = _same_path(source, retirement_target / ".novc")
        retained = [(source, True)]
        retained.extend(
            (source / relative, True)
            for relative in item["inventory"]["directories"]
            if not (root_novc and _is_suite_basetemp(relative))
        )
        retained.extend(
            (source / file["path"], False)
            for file in item["inventory"]["files"]
            if not (root_novc and _is_suite_basetemp(file["path"]))
        )
        for path, directory in retained:
            spellings = [
                (_normalized_reference(path), "absolute"),
                (path.as_uri(), "file-url"),
            ]
            for base, kind in (
                (retirement_target, "relative"),
                (primary, "primary-relative"),
                (checkout, "checkout-relative"),
            ):
                try:
                    relative = os.path.relpath(path, base).replace("\\", "/")
                except ValueError:
                    continue
                # A bare relative root is generic policy; actual child paths
                # and explicit absolute source-root citations remain auditable.
                if relative != ".novc":
                    spellings.append((relative, kind))
            for spelling, kind in spellings:
                reference = os.path.normcase(spelling).replace("\\", "/")
                key = (str(source), reference)
                if key in seen:
                    continue
                seen.add(key)
                references.append(
                    {
                        "source": str(source),
                        "reference": reference,
                        "kind": kind,
                        "directory": directory,
                    }
                )
    return references


def _tracked_relocation_citations(
    checkout: Path,
    primary: Path,
    retirement_target: Path,
    relocation_records: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    references = _citation_references(
        checkout, primary, retirement_target, relocation_records
    )
    if not references:
        return []
    result = _git(
        checkout,
        "grep",
        "-l",
        "-z",
        "-I",
        "-i",
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
    seen: set[tuple[str, int, str]] = set()
    for encoded_path in paths:
        relative = encoded_path.decode("utf-8", errors="surrogateescape")
        source_file = checkout / relative
        try:
            lines = source_file.read_text(encoding="utf-8").splitlines()
            source_bytes, source_sha256 = _file_digest(source_file)
        except (OSError, UnicodeDecodeError) as exc:
            raise RetirementError(
                f"cannot review tracked citation {relative}: {exc}"
            ) from exc
        for line_number, line in enumerate(lines, start=1):
            for reference in references:
                if not _reference_matches(
                    line,
                    reference["reference"],
                    directory=reference["directory"],
                ):
                    continue
                key = (relative, line_number, reference["source"])
                if key in seen:
                    continue
                seen.add(key)
                citations.append(
                    {
                        "path": PurePosixPath(relative).as_posix(),
                        "line": line_number,
                        "text": line[:500],
                        "matched_source": reference["source"],
                        "matched_reference": reference["reference"],
                        "reference_kind": reference["kind"],
                        "tracked_file_bytes": source_bytes,
                        "tracked_file_sha256": source_sha256,
                    }
                )
    return sorted(
        citations,
        key=lambda item: (
            item["path"],
            item["line"],
            item["matched_source"],
            item["reference_kind"],
        ),
    )


def _operation_markers(
    worktree: Path,
    *,
    timeout_seconds: int | None = None,
    noninteractive: bool = False,
) -> list[str]:
    present: list[str] = []
    for marker in _GIT_OPERATION_MARKERS:
        path_text = _git_ok(
            worktree,
            "rev-parse",
            "--git-path",
            marker,
            timeout_seconds=timeout_seconds,
            noninteractive=noninteractive,
        ).strip()
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


def _safety_snapshot(
    worktree_path: Path, *, citation_sources: Sequence[dict[str, Any]] | None = None
) -> dict[str, Any]:
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
    sources = list(citation_sources) if citation_sources is not None else novc
    checkouts: list[Path] = []
    seen_checkouts: set[str] = set()
    for checkout in (
        worktree_path,
        primary,
        *(record.path.resolve() for record in worktrees),
    ):
        key = _path_key(checkout)
        if key not in seen_checkouts:
            seen_checkouts.add(key)
            checkouts.append(checkout)
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
            for checkout in checkouts
            for citation in _tracked_relocation_citations(
                checkout, primary, worktree_path, sources
            )
        ],
    }


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
