"""Repository selection and reporting for shared worktree retirement inspection.

This module never retires anything. Preparation targets one exact audited path;
execution consumes its reviewed preflight through worktree_retirement.
"""

from collections.abc import Sequence
from pathlib import Path

from repo_util import git_worktree_cleanup, worktree_retirement
from repo_util.repo_selection import RepoInfo


def problem_repos(reports: list[tuple[str, list[str]]]) -> list[str]:
    return [name for name, errors in reports if errors]


def unknown_worktrees(
    repo_infos: list[RepoInfo], named: Sequence[Path], *, owner: str = "claude"
) -> list[Path]:
    candidates = [
        record.path
        for info in repo_infos
        for record in worktree_retirement.select_worktrees(info.path, owner=owner)
    ]
    return [
        path
        for path in named
        if not any(
            worktree_retirement._same_path(path, candidate) for candidate in candidates
        )
    ]


def run_clean_worktrees_across_repos(
    repo_infos: list[RepoInfo],
    *,
    sessions_ended: Sequence[Path] = (),
    owner: str = "claude",
) -> list[tuple[str, list[str]]]:
    reports = []
    stranded = []
    for info in repo_infos:
        # Flush progress so a captured long-running audit remains observable.
        print(f"=== {info.name} ===", flush=True)
        try:
            report = git_worktree_cleanup.clean_worktrees(
                info.path, sessions_ended=sessions_ended, owner=owner
            )
            git_worktree_cleanup.print_report(report)
            reports.append((info.name, report.errors))
            stranded.extend(info.name for _ in report.stranded_branches)
        except (RuntimeError, OSError) as exc:
            print(f"worktrees: ERROR {exc}")
            reports.append((info.name, [str(exc)]))
    print(f"REPO_COUNT={len(reports)}")
    problems = problem_repos(reports)
    if problems:
        print(f"WORKTREE_PROBLEM_COUNT={len(problems)}; REPOS={', '.join(problems)}")
    if stranded:
        print(
            f"STRANDED_BRANCH_COUNT={len(stranded)}; REPOS={', '.join(dict.fromkeys(stranded))}"
        )
    return reports
