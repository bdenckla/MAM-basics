"""Discovery and runtime facts, independent of worktree retirement policy.

Runtime records are advisory blockers, never permission to remove a checkout.
Claude exposes cwd records and desktop leases. Codex exposes task cwd records in
its SQLite state and writer-lease files. These private formats may change: an
unreadable installed format fails closed. Absence of records still requires the
caller's explicit ended-session attestation in the shared executor.
"""

from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any

BRANCH_PREFIXES = {"claude": ("claude/",), "codex": ("codex/", "codex-")}
SELECTORS = ("claude", "codex", "both")


def path_key(path: Path | str) -> str:
    return os.path.normcase(os.path.abspath(path))


def inside(path: Path | str, directory: Path | str) -> bool:
    key, parent = path_key(path), path_key(directory)
    return key == parent or key.startswith(parent + os.sep)


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))


def owners(path: Path, branch: str | None, primary: Path) -> list[str]:
    found = set()
    for owner, prefixes in BRANCH_PREFIXES.items():
        if branch and branch.startswith(prefixes):
            found.add(owner)
    if inside(path, primary / ".claude" / "worktrees"):
        found.add("claude")
    if inside(path, codex_home() / "worktrees"):
        found.add("codex")
    return sorted(found)


def selected(found: list[str], selector: str) -> bool:
    if selector not in SELECTORS:
        raise ValueError(f"unknown worktree owner selector: {selector}")
    return bool(found) if selector == "both" else selector in found


def deletable_branch(branch: str | None, found: list[str]) -> bool:
    return bool(
        branch and len(found) == 1 and branch.startswith(BRANCH_PREFIXES[found[0]])
    )


def _present(path: Path) -> bool:
    """Distinguish missing runtime data from inaccessible runtime data."""
    try:
        path.lstat()
    except FileNotFoundError:
        return False
    return True


def runtime_facts(worktree: Path) -> dict[str, Any]:
    """Read both runtimes: a session can occupy a checkout owned by either agent."""
    blockers: list[str] = []
    claude_ids: list[str] = []
    codex_ids: list[str] = []
    basis: list[str] = []
    sessions = Path.home() / ".claude" / "sessions"
    try:
        if _present(sessions):
            for record in sorted(p for p in sessions.iterdir() if p.suffix == ".json"):
                data = json.loads(record.read_text(encoding="utf-8"))
                if inside(data["cwd"], worktree):
                    identifier = str(data.get("sessionId", record.stem))
                    claude_ids.append(identifier)
                    blockers.append(f"running Claude session {identifier}")
        basis.append(f"Claude session records: {sessions}")
        appdata = os.environ.get("APPDATA")
        register = Path(appdata) / "Claude" / "git-worktrees.json" if appdata else None
        if register is not None and _present(register):
            entries = json.loads(register.read_text(encoding="utf-8"))["worktrees"]
            for entry in entries.values():
                if entry.get("leasedBy") and inside(entry["path"], worktree):
                    identifier = str(entry["leasedBy"])
                    claude_ids.append(identifier)
                    blockers.append(f"leased by Claude session {identifier}")
        basis.append(f"Claude desktop register: {register}")
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        blockers.append(f"cannot audit Claude runtime records: {exc}")

    home = codex_home()
    try:
        databases = (
            sorted(
                path
                for path in home.iterdir()
                if path.name.startswith("state_") and path.suffix == ".sqlite"
            )
            if _present(home)
            else []
        )
        for database in databases:
            with sqlite3.connect(
                database.resolve().as_uri() + "?mode=ro", uri=True
            ) as db:
                rows = db.execute("SELECT id, cwd FROM threads").fetchall()
            for identifier, cwd in rows:
                if inside(cwd, worktree):
                    codex_ids.append(identifier)
                    lease = home / "thread-writer-locks" / f"{identifier}.lock"
                    if _present(lease):
                        blockers.append(
                            f"Codex writer lease for task {identifier}: {lease}"
                        )
        basis.append("Codex task databases: " + ", ".join(str(p) for p in databases))
    except (OSError, sqlite3.Error, ValueError, TypeError) as exc:
        blockers.append(f"cannot audit Codex runtime records: {exc}")
    return {
        "blockers": blockers,
        "claude_session_ids": sorted(set(claude_ids)),
        "codex_task_ids": sorted(set(codex_ids)),
        "basis": basis,
    }
