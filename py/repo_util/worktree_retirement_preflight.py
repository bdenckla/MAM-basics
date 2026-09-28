"""Retirement-plan preparation: destinations, fingerprints, the preflight and receipts.

``prepare_retirement`` audits without changing the target and writes the reviewed plan.
The fingerprints and the citation review defined here are what execution checks that plan
against.  The JSON writers here also write the retained-data sidecars, so the preflight
and every sidecar are written the same two ways: exclusively when created, and
atomically when replaced.
"""

from __future__ import annotations

import hashlib
import json
import os
import secrets
from datetime import datetime
from pathlib import Path
from typing import Any, Sequence

from mb_cmn.new_york_time import NEW_YORK
from repo_util import worktree_owners
from repo_util.worktree_retirement_git import RetirementError, _inside
from repo_util.worktree_retirement_inspection import _safety_snapshot

SCHEMA_VERSION = 2


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


def _fingerprint(snapshot: dict[str, Any]) -> str:
    encoded = json.dumps(
        snapshot, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _preflight_plan_fingerprint(preflight: dict[str, Any]) -> str:
    plan = dict(preflight)
    plan.pop("execution", None)
    plan.pop("plan_fingerprint", None)
    return _fingerprint(plan)


def _citation_review(
    citations: Sequence[dict[str, Any]], *, reviewed: bool, note: str | None
) -> dict[str, Any]:
    review: dict[str, Any] = {
        "citations": list(citations),
        "reviewed": reviewed,
        "note": note,
    }
    review["fingerprint"] = _fingerprint(review)
    return review


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
    citation_review = _citation_review(
        citations, reviewed=citations_reviewed, note=citation_note
    )
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
        "citation_review": citation_review,
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
    print(
        "ready for execution: "
        + ("yes" if ready else "no; review references to relocated .novc paths")
    )
    for item in snapshot["novc_directories"]:
        inventory = item["inventory"]
        print(
            f"retain {item['path']}: {inventory['file_count']} file(s), "
            f"{inventory['total_bytes']} byte(s)"
        )
    if citations:
        print(f"tracked references to relocated .novc paths: {len(citations)}")
        for citation in citations:
            print(
                f"  {citation['checkout']}/{citation['path']}:{citation['line']}: "
                f"{citation['text']} (relocates {citation['matched_source']})"
            )
    return preflight


def _write_sidecar(path: Path, metadata: dict[str, Any]) -> None:
    _write_json_exclusive(path, metadata)


def _update_sidecar(path: Path, metadata: dict[str, Any]) -> None:
    temporary = path.with_name(path.name + f".tmp-{secrets.token_hex(4)}")
    _write_json_exclusive(temporary, metadata)
    os.replace(temporary, path)
