"""Synchronize full clone forests using the workspace roster and each source origin.

Checks fetch remote refs, but never change checkout files or environments. A write
creates missing full clones, fast-forwards eligible main branches, and creates
missing environments. A write refuses a dirty, off-main, mid-operation, locked or
occupied clone before fetching it, and an ahead or diverged clone after a fetch that
adds any missing objects, rewrites FETCH_HEAD, and creates or fast-forwards
refs/remotes/origin/main; either way the clone's local branches, checkout and
environments stay untouched. Every repository failure is reported while the remaining
roster runs.
"""

from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess

from mb_cmn import paths, provenance
from repo_util.forest_environments import (
    GIT_TIMEOUT_SECONDS,
    ForestError,
    require_unlinked,
    synchronize_environments,
)
from repo_util.user_config_sync import _run_git, _command_error
from repo_util.worktree_owners import runtime_facts
from repo_util.worktree_retirement_git import RetirementError, _list_worktrees
from repo_util.worktree_retirement_inspection import _operation_markers, _status_entries

_FOREST_NAME = re.compile(r"GitRepos(?:[2-9]|[1-9][0-9]+)?\Z")


def _git(repo: Path, *arguments: str) -> str:
    result = _run_git(repo, *arguments, timeout_seconds=GIT_TIMEOUT_SECONDS)
    if result.returncode:
        raise ForestError(_command_error(result))
    return result.stdout.strip()


def _roster(source: Path) -> tuple[Path, list[str]]:
    home = provenance.home_clone_dir(source)
    if home is None or home.name != "MAM-basics":
        raise ForestError(f"cannot identify the MAM-basics home clone: {source}")
    names = []
    workspace = json.loads(
        (source / "all-repos.code-workspace").read_text(encoding="utf-8")
    )
    for folder in workspace["folders"]:
        relative = folder["path"]
        if relative == ".":
            name = "MAM-basics"
        elif relative.startswith("../") and re.fullmatch(
            r"[A-Za-z0-9_.-]+", relative[3:]
        ):
            name = relative[3:]
            if name in {".", ".."}:
                raise ForestError(f"noncanonical workspace folder: {relative}")
        else:
            raise ForestError(f"noncanonical workspace folder: {relative}")
        if name.casefold() in {value.casefold() for value in names}:
            raise ForestError(f"duplicate workspace repository: {name}")
        names.append(name)
    if "MAM-basics" not in names:
        raise ForestError("the workspace roster must include MAM-basics")
    return home.resolve().parent, names


def _full_clone(repo: Path) -> None:
    require_unlinked(repo)
    require_unlinked(repo / ".git")
    if not (repo / ".git").is_dir():
        raise ForestError(f"not a full independent clone: {repo}")
    if Path(_git(repo, "rev-parse", "--show-toplevel")).resolve() != repo.resolve():
        raise ForestError(f"not the exact repository root: {repo}")
    if (
        Path(
            _git(repo, "rev-parse", "--path-format=absolute", "--git-common-dir")
        ).resolve()
        != (repo / ".git").resolve()
    ):
        raise ForestError(f"shared Git directory: {repo}")
    if _git(repo, "rev-parse", "--is-shallow-repository") != "false":
        raise ForestError(f"shallow clone: {repo}")
    if (repo / ".git/objects/info/alternates").exists():
        raise ForestError(f"shared object storage: {repo}")
    objects = repo / ".git/objects"
    require_unlinked(objects)
    for entry in objects.rglob("*"):
        if entry.is_symlink() or entry.is_junction():
            raise ForestError(f"linked object storage: {entry}")
    if _git(repo, "config", "--get", "core.bare") != "false":
        raise ForestError(f"bare repository: {repo}")


def _snapshot(repo: Path) -> tuple[str, str, tuple[str, ...], tuple[str, ...]]:
    branch = _run_git(
        repo,
        "symbolic-ref",
        "--quiet",
        "--short",
        "HEAD",
        timeout_seconds=GIT_TIMEOUT_SECONDS,
    )
    if branch.returncode not in (0, 1):
        raise ForestError(_command_error(branch))
    locks = []
    for name in (
        "index.lock",
        "HEAD.lock",
        "config.lock",
        "refs/heads/main.lock",
        "refs/remotes/origin/main.lock",
    ):
        lock = Path(
            _git(repo, "rev-parse", "--path-format=absolute", "--git-path", name)
        )
        if lock.exists():
            locks.append(name)
    return (
        _git(repo, "rev-parse", "HEAD"),
        branch.stdout.strip() if branch.returncode == 0 else "detached",
        tuple(
            _status_entries(
                repo, timeout_seconds=GIT_TIMEOUT_SECONDS, noninteractive=True
            )
        ),
        tuple(
            _operation_markers(
                repo, timeout_seconds=GIT_TIMEOUT_SECONDS, noninteractive=True
            )
            + locks
        ),
    )


def _runtime(repo: Path) -> list[str]:
    facts = runtime_facts(repo)
    blockers = list(facts["blockers"])
    for worktree in _list_worktrees(
        repo, timeout_seconds=GIT_TIMEOUT_SECONDS, noninteractive=True
    ):
        if worktree.path.resolve() != repo.resolve():
            external = runtime_facts(worktree.path)
            if external["blockers"]:
                print(
                    f"FOREST_WORKTREE_OCCUPIED: {worktree.path}: {'; '.join(external['blockers'])}"
                )
                blockers.extend(
                    f"{worktree.path}: {entry}" for entry in external["blockers"]
                )
    print(
        f"FOREST_RUNTIME: {repo}: {'; '.join(blockers) if blockers else 'no active session record'}"
    )
    return blockers


def _fetch_main(repo: Path) -> str:
    """Advance the tracking ref only after proving remote ancestry."""
    reference = "refs/remotes/origin/main"
    symbolic = _run_git(
        repo,
        "symbolic-ref",
        "--quiet",
        reference,
        timeout_seconds=GIT_TIMEOUT_SECONDS,
    )
    if symbolic.returncode == 0:
        raise ForestError("origin/main must be a direct tracking ref")
    if symbolic.returncode != 1:
        raise ForestError(_command_error(symbolic))
    previous = _run_git(
        repo,
        "rev-parse",
        "--verify",
        "--quiet",
        reference,
        timeout_seconds=GIT_TIMEOUT_SECONDS,
    )
    if previous.returncode not in (0, 1):
        raise ForestError(_command_error(previous))
    old = previous.stdout.strip() if previous.returncode == 0 else None
    # An empty refmap prevents configured tracking updates during this fetch.
    _git(
        repo,
        "fetch",
        "--no-tags",
        "--no-recurse-submodules",
        "--no-auto-maintenance",
        "--refmap=",
        "origin",
        "refs/heads/main",
    )
    fetched = _git(repo, "rev-parse", "--verify", "FETCH_HEAD^{commit}")
    if old is not None:
        ancestry = _run_git(
            repo,
            "merge-base",
            "--is-ancestor",
            old,
            fetched,
            timeout_seconds=GIT_TIMEOUT_SECONDS,
        )
        if ancestry.returncode == 1:
            raise ForestError(
                "origin/main history was rewritten; tracking ref retained"
            )
        if ancestry.returncode:
            raise ForestError(_command_error(ancestry))
    _git(
        repo, "update-ref", "--no-deref", reference, fetched, old or "0" * len(fetched)
    )
    return fetched


def _sync_repo(repo: Path, origin: str, *, check: bool) -> bool:
    require_unlinked(repo)
    if not repo.exists():
        if check:
            raise ForestError(f"missing clone: {repo}")
        repo.parent.mkdir(parents=True, exist_ok=True)
        print(f"FOREST_CLONE: {repo}", flush=True)
        result = _run_git(
            repo.parent,
            "clone",
            "--no-local",
            "--origin",
            "origin",
            "--",
            origin,
            str(repo),
            timeout_seconds=600,
        )
        if result.returncode:
            raise ForestError(_command_error(result))
    _full_clone(repo)
    if _git(repo, "remote", "get-url", "origin") != origin:
        raise ForestError(f"origin differs from the source clone: {repo}")
    before = _snapshot(repo)
    blockers = _runtime(repo)
    head, branch, status, markers = before
    reasons = []
    if branch != "main":
        reasons.append(f"branch is {branch}")
    if status:
        reasons.append("checkout is dirty")
    if markers:
        reasons.append("Git operation in progress")
    if not check:
        # A write judges the clone's own state before any fetch, so a clone it
        # refuses for that state is not fetched at all.
        reasons.extend(blockers)
        if reasons:
            print(
                f"FOREST_REPO: {repo}: branch={branch} changes={len(status)} operations={','.join(markers) or 'none'}"
            )
            raise ForestError(
                "; ".join(reasons)
                + "; not fetched; checkout and environments left untouched"
            )
    fetched = _fetch_main(repo)
    ahead, behind = (
        int(value)
        for value in _git(
            repo,
            "rev-list",
            "--left-right",
            "--count",
            f"HEAD...{fetched}",
        ).split()
    )
    print(
        f"FOREST_REPO: {repo}: branch={branch} ahead={ahead} behind={behind} changes={len(status)} operations={','.join(markers) or 'none'}"
    )
    if ahead:
        reasons.append("unpushed or divergent commits")
    if check:
        environments = synchronize_environments(repo, check=True)
        if reasons:
            print(f"FOREST_REPO_INELIGIBLE: {repo}: {'; '.join(reasons)}")
        return environments and behind == 0 and not reasons
    if reasons:
        raise ForestError(
            "; ".join(reasons)
            + "; fetched origin/main (any missing objects, FETCH_HEAD, and"
            " refs/remotes/origin/main created or fast-forwarded); local branches,"
            " checkout and environments left untouched"
        )
    if _snapshot(repo) != before or _runtime(repo):
        raise ForestError("checkout or writer state changed during inspection")
    _git(repo, "merge", "--ff-only", fetched)
    return synchronize_environments(repo, check=False)


def run_forest_sync(root: Path, *, check: bool, source: Path | None = None) -> bool:
    """Use the complete roster; never enumerate repositories or delete loose paths."""
    current = (source or paths.repo_root()).resolve()
    try:
        source_forest, names = _roster(current)
        require_unlinked(root)
        root = root.resolve(strict=False)
        if any(root.is_relative_to(source_forest / name) for name in names):
            raise ForestError(
                "a clone forest cannot be nested inside a source repository"
            )
    except (OSError, ValueError, ForestError) as exc:
        print(f"FOREST_FAILED: {root}: {exc}")
        return False
    print(f"FOREST_ROOT: {root}; mode={'fetch and check' if check else 'synchronize'}")
    problems = 0
    for name in names:
        try:
            source_repo = source_forest / name
            _full_clone(source_repo)
            origin = _git(source_repo, "remote", "get-url", "origin")
            if not _sync_repo(root / name, origin, check=check):
                problems += 1
                print(
                    f"FOREST_REPO_FAILED: {root / name}: behind origin/main or environment drift"
                )
        except (
            OSError,
            ValueError,
            subprocess.SubprocessError,
            ForestError,
            RetirementError,
        ) as exc:
            print(f"FOREST_REPO_FAILED: {root / name}: {exc}")
            problems += 1
    print(f"FOREST_PROBLEM_COUNT: {problems}")
    return problems == 0


def run_forest_status(*, home: Path | None = None) -> bool:
    """Discover primary and numbered secondary forests in the account home."""
    account = home or Path.home()
    roots = [account / "GitRepos"]
    try:
        roots.extend(
            sorted(
                (
                    child
                    for child in account.iterdir()
                    if child.name != "GitRepos"
                    and _FOREST_NAME.fullmatch(child.name)
                    and child.is_dir()
                ),
                key=lambda child: int(child.name.removeprefix("GitRepos")),
            )
        )
    except OSError as exc:
        print(f"FOREST_DISCOVERY_FAILED: {exc}")
        return False
    success = True
    for root in roots:
        success = run_forest_sync(root, check=True) and success
    return success
