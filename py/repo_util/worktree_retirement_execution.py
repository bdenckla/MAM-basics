"""Destructive retirement: the one non-forced worktree removal and branch deletion.

``execute_retirement`` is the only code in the retirement family, or in its compatibility
modules, that removes a worktree registration or deletes a branch;
``py/tests/test_worktree_retirement_policy.py`` lints that it stays so.
"""

from __future__ import annotations

import json
import os
import stat
from datetime import datetime
from pathlib import Path
from typing import Any

from mb_cmn.new_york_time import NEW_YORK
from repo_util import worktree_owners
from repo_util.worktree_retirement_git import (
    RetirementError,
    _git,
    _git_ok,
    _inside,
    _is_ancestor,
    _list_worktrees,
    _same_path,
)
from repo_util.worktree_retirement_inspection import (
    _branch_recovery_commits,
    _check_runtime,
    _is_reparse_point,
    _protect_recovery_commits,
    _safety_snapshot,
)
from repo_util.worktree_retirement_preflight import (
    SCHEMA_VERSION,
    _citation_review,
    _fingerprint,
    _preflight_plan_fingerprint,
    _update_sidecar,
)
from repo_util.worktree_retirement_relocation import (
    _reconcile_relocations,
    _relocate_novc,
)


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
            "preflight is not ready; its relocated .novc reference audit is pending"
        )
    if preflight.get("plan_fingerprint") != _preflight_plan_fingerprint(preflight):
        raise RetirementError("preflight plan changed after it was prepared")
    expected_citation_review = _citation_review(
        preflight["snapshot"]["tracked_novc_citations"],
        reviewed=bool(preflight.get("citations_reviewed")),
        note=preflight.get("citation_note"),
    )
    if preflight.get("citation_review") != expected_citation_review:
        raise RetirementError("preflight citation review is incomplete or changed")

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
        current_snapshot = _safety_snapshot(
            worktree,
            citation_sources=old_snapshot["novc_directories"],
        )
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
    # Ordinary-token execution is required; elevation measurement remains deferred.
    execution["ordinary_token_required"] = True
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
        "citation_review": preflight["citation_review"],
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
        current_snapshot = _safety_snapshot(
            worktree,
            citation_sources=old_snapshot["novc_directories"],
        )
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
