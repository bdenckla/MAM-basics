"""Compatibility inspection API; shared retirement requires a reviewed preflight.

The historical Claude sweep name selects Claude candidates by default. It never
prunes registrations, removes directories, or deletes orphan branches. Ownership
selects candidates; worktree_retirement owns every safety and preservation gate.
Remote-only work is reported from cached refs without fetching or changing refs.
"""

from dataclasses import dataclass, field
from pathlib import Path
from collections.abc import Collection

from repo_util import worktree_owners, worktree_retirement


@dataclass
class CleanupReport:
    """Inspection results, including blockers and remote-only work."""

    kept_worktrees: list[tuple[str, str]] = field(default_factory=list)
    stranded_branches: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


def is_linked_worktree(repo_dir: Path, path: Path) -> bool:
    return any(
        worktree_retirement._same_path(record.path, path)
        for record in worktree_retirement._list_worktrees(repo_dir)[1:]
    )


def clean_worktrees(
    repo_dir: Path, *, sessions_ended: Collection[Path] = (), owner: str = "claude"
) -> CleanupReport:
    """Inspect the selected scope. Ended-path arguments never authorize removal."""
    selected = worktree_retirement.select_worktrees(repo_dir, owner=owner)
    for path in sessions_ended:
        if is_linked_worktree(repo_dir, path) and not any(
            worktree_retirement._same_path(record.path, path) for record in selected
        ):
            raise worktree_retirement.RetirementError(
                f"ended path outside {owner} selection: {path}"
            )
    report = CleanupReport()
    for item in worktree_retirement.inspect_worktrees(repo_dir, owner=owner):
        reason = (
            item["blocker"] or "audit passed; prepare and review a retirement preflight"
        )
        report.kept_worktrees.append((item["worktree"], reason))
    default = worktree_retirement._default_branch(repo_dir)
    prefixes = [
        prefix
        for selected_owner, values in worktree_owners.BRANCH_PREFIXES.items()
        if owner == "both" or selected_owner == owner
        for prefix in values
    ]
    output = worktree_retirement._git_ok(
        repo_dir,
        "for-each-ref",
        "--format=%(refname) %(objectname)",
        *[f"refs/remotes/origin/{prefix}*" for prefix in prefixes],
    )
    for line in output.splitlines():
        ref, tip = line.split()
        branch = ref.removeprefix("refs/remotes/origin/")
        local = worktree_retirement._git(
            repo_dir, "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"
        )
        if local.returncode == 1 and not worktree_retirement._is_ancestor(
            repo_dir, tip, default
        ):
            report.stranded_branches.append(branch)
    return report


def print_report(report: CleanupReport) -> None:
    for path, reason in report.kept_worktrees:
        print(f"worktrees: inspected {path} ({reason})")
    for branch in report.stranded_branches:
        print(
            f"worktrees: remote-only work in {branch} (cached refs; fetch separately to refresh)"
        )
    for error in report.errors:
        print(f"worktrees: ERROR {error}")
    if not report.kept_worktrees:
        print("worktrees: no selected candidates")
