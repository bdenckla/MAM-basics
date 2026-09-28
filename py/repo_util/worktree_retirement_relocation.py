"""Verified relocation of a retiring worktree's ``.novc`` directories.

A relocation is verified against the inventory the preflight recorded, and writes its
own sidecar before it moves anything.  ``_reconcile_relocations`` reads those sidecars
back on every execution, which is what lets an interrupted one resume.
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path
from typing import Any

from repo_util.worktree_retirement_git import RetirementError
from repo_util.worktree_retirement_inspection import _inventory
from repo_util.worktree_retirement_preflight import _update_sidecar, _write_sidecar


def _same_volume(left: Path, right: Path) -> bool:
    return os.path.normcase(left.resolve().drive) == os.path.normcase(
        right.resolve().drive
    )


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
                or metadata.get("citation_review") != preflight.get("citation_review")
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
