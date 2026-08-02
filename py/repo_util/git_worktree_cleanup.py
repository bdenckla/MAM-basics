"""Remove finished agent git worktrees and the branches they left behind.

REPO-AGNOSTIC BY DESIGN, and filed here rather than in a ``wlc_``-prefixed package
for that reason.  It was written in wlc-utils and moved here with the rest of that
repo's Python on 2026-08-01, but ``repo_util/check_repo_standards.py`` already called
it the reference implementation for the cross-repo ``worktree_hygiene`` standard, and
a repo-specific-looking home would have contradicted the point.  It takes the repo to
clean as an argument and imports nothing from either repo.

Agent sessions that run in isolation create a worktree plus, usually, a matching
``claude/<name>`` branch, and clean up neither when the session ends, so both
accumulate: at the time this module was written wlc-utils carried two orphaned
worktrees and three orphaned branches, every one of them clean and already
merged into main.  They are not harmless clutter -- a worktree is a second full
checkout, and a stale one is a place where a later session can do real work in
the wrong tree.

TWO LOCATIONS, BOTH IN SCOPE.  The harness default is
``<repo>/.claude/worktrees/<name>``, whose nesting depth breaks the
``../<sibling>`` lookups this codebase's cross-repo code depends on (see
``mb_cmn.paths``, whose ``REPOS_ROOT`` / ``REPO_<NAME>_DIR`` overrides are the other
answer to the same problem).  The workaround for that is a worktree placed as a
SIBLING of the repo instead, ``GitRepos/<repo>-<topic>``, where those lookups resolve --
a deliberate practice, not a mistake, and the one that accumulates in the more
annoying place.  Removal is driven off ``git worktree list``, so it covers both
without caring which is which.  The empty-husk sweep below is the sole exception
and stays confined to ``.claude/worktrees/``: it deletes directories by
enumeration rather than by asking git, which is safe inside a directory that
exists only to hold worktrees and would not be safe loose in ``GitRepos``.

REMOVAL IS CONSERVATIVE, AND NEVER USES ``--force``.  Several conditions each
spare a worktree, and every spared one is reported with its reason rather than
passed over in silence:

- The main worktree (the repo clone itself) is never a candidate.
- Neither is whichever worktree is running this code -- an agent housekeeping
  its own checkout must not delete the ground it stands on.
- A worktree locked with ``git worktree lock`` is skipped.  That is git's own
  sanctioned "leave this alone" flag and the right way to protect a worktree
  indefinitely; ``git worktree remove`` refuses a locked one, so never passing
  ``--force`` honours it automatically.  It is still checked explicitly, so a
  deliberately locked worktree reports as a considered decision instead of
  failing noisily every single run.
- A worktree with recent git activity is skipped -- see
  ``_seconds_since_activity``.
- A worktree with any uncommitted change, tracked or untracked, is left alone,
  as is one whose HEAD is not an ancestor of the default branch.  Untracked
  files count deliberately: git's own ``worktree remove`` refuses on them too,
  and in a repo whose real deliverables are generated files, an unexpected
  untracked file is exactly the kind of thing worth looking at before it is
  destroyed.
- A worktree holding gitignored content that exists ONLY there is left alone
  too, with the surviving entries named in the reason.  Ignored files are the
  one class a plain ``git status --porcelain`` does not list AND
  ``git worktree remove`` does not check for -- so without this condition a
  clean, merged, idle worktree would be removed together with, say, a
  ``.novc/`` report that exists nowhere else, silently.  This is the same class
  of file whose loss step 1 of ``main_repo_maintenance`` warns about at length;
  step 1 wipes it on purpose and announces itself, and this step must not wipe
  it by accident.

WHAT COUNTS AS IGNORED CONTENT, and why the condition is narrower than "any
``!!`` entry".  Read the sentence above literally: the thing worth sparing a
worktree for is content that **exists nowhere else**.  Two kinds of ``!!`` entry
plainly are not that, and ``_unique_ignored`` drops both before the condition
is applied:

- **Tool caches** -- ``__pycache__/``, ``.pytest_cache/``, ``.ruff_cache/``,
  ``.mypy_cache/``.  Running the tool again writes them.
- **A copy of what the main worktree already has**, compared file by file and
  byte for byte, one-directionally: every file here must sit identical there,
  while extra files there are irrelevant.  An agent worktree's ``.claude/``
  holding a ``settings.local.json`` copied from the clone is the standing case.

This is not a softening of the rule, it is the rule stated exactly, and it fixes
a gap that made the condition permanent rather than conservative: a
``__pycache__`` never expires, so before 2026-08-02 a worktree that had merely
been run once could not be collected by any later pass.  Measured that day, all
three of wlc-utils' orphaned worktrees -- clean, detached, fully merged into
main -- were held by exactly this: bytecode, ``.pytest_cache/``, and a 73-byte
``.claude/settings.local.json`` byte-identical to the clone's own.

NOTE THAT A ``--force`` WOULD NOT HAVE HELPED, and the idea is worth retiring
rather than re-proposing.  Forwarding ``--force`` to ``git worktree remove``
reaches nothing: every condition above is decided here, in Python, and skips the
worktree before git is ever invoked.  Nor is git the obstacle -- it removes
ignored files without complaint, as the ``--ignored`` note under
``_worktree_status`` records.  A flag would have had to override this module's
own judgement, which is the one thing that must not become routine.

Branch deletion is likewise narrow.  Only branches under ``claude/`` are
considered -- the prefix the agent harness uses -- so a topic branch created by
hand is never a candidate however merged it may be.  Deletion goes through
``git branch -d``, which refuses an unmerged branch on its own; the ancestor
check here is for the report, not for safety.

Worktrees are removed before branches, because a branch checked out in a
worktree cannot be deleted while that worktree exists.  That ordering matters
in practice: the worktree and the branch it holds often do not share a name.

THE CASE THE ACTIVITY CHECK EXISTS FOR is a worktree another session is using
right now.  Git has no notion of a worktree being "in use", so this cannot be
known, only estimated.  The dirty check catches nearly all of it and is not a
theoretical safeguard: a concurrent session held ``wlc-utils-decalogue-claims``
while this module was being written, sitting exactly on the default branch's
tip, and nine modified files plus one untracked new module are the only reason
it was spared.  What that leaves is a narrow window -- a live session momentarily
between commits, with a clean tree -- which is what ``_seconds_since_activity``
closes.

Be exact about the stakes rather than alarmed: once every condition above has
passed, the worktree holds nothing git can see that does not also exist in the
repo -- no uncommitted change, no unmerged commit, no gitignored content -- so
what a removal costs is the session's workspace, never its work.  The
gitignored-content condition is load-bearing in that sentence: "clean and
fully merged" alone still leaves room for an ignored file that exists nowhere
else, which is exactly what an earlier version of this module would have
removed without a word.

Do NOT count the operating system as a further line of defence.  An earlier
version of this docstring did, on the grounds that a held file handle makes the
removal fail -- true on Windows, but it fails LATE.  Git deletes the worktree's
contents and only then cannot unlink the directory, which is exactly how the
husk that ``_sweep_empty_dirs`` now collects came to exist.  A held handle turns
a silent removal into a noisy one; it does not prevent it.
"""

from __future__ import annotations

import filecmp
import os
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

_AGENT_BRANCH_PREFIX = "claude/"

# Ignored directories that hold only tool output, regenerated by running the tool
# again. See "WHAT COUNTS AS IGNORED CONTENT" in this module's docstring.
_REGENERABLE_CACHE_DIRS = frozenset(
    {"__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache"}
)

# How many files _content_exists_elsewhere will read before giving up and sparing
# the worktree. Generous for a .claude/ or a stray report, far short of a .venv.
_COMPARE_FILE_BUDGET = 500

# Where the agent harness puts its worktrees. Emptied of its last worktree, this
# directory is removed too, so a clean repo shows no trace of the machinery.
_WORKTREE_PARENT = Path(".claude") / "worktrees"

# How long after its last git command a worktree is presumed still in use. An
# hour is deliberately generous: the cost of waiting is one more maintenance run
# before an abandoned worktree goes, while the cost of being wrong is deleting a
# live session's checkout. A session idling on a prompt for over an hour and
# holding a clean tree is the residual case, and `git worktree lock` is the
# answer for anyone who wants a guarantee rather than a heuristic.
_ACTIVITY_GRACE_SECONDS = 60 * 60


@dataclass
class CleanupReport:
    """What one ``clean_worktrees`` pass did, for printing by the caller."""

    pruned: bool = False
    removed_worktrees: list[str] = field(default_factory=list)
    kept_worktrees: list[tuple[str, str]] = field(default_factory=list)
    deleted_branches: list[str] = field(default_factory=list)
    kept_branches: list[tuple[str, str]] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class _Worktree:
    path: Path
    head: str | None
    branch: str | None  # short name, or None when detached
    locked: bool = False


def _git(repo_dir: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo_dir), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _list_worktrees(repo_dir: Path) -> list[_Worktree]:
    """Parse ``git worktree list --porcelain``.

    The main worktree is always the first record, which is how the caller
    identifies it -- there is no per-record flag saying so.
    """
    result = _git(repo_dir, "worktree", "list", "--porcelain")
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git worktree list failed")

    worktrees: list[_Worktree] = []
    path: Path | None = None
    head: str | None = None
    branch: str | None = None
    locked = False
    for line in result.stdout.splitlines():
        if line.startswith("worktree "):
            path = Path(line[len("worktree ") :])
            head = None
            branch = None
            locked = False
        elif line.startswith("HEAD "):
            head = line[len("HEAD ") :]
        elif line.startswith("branch "):
            branch = line[len("branch refs/heads/") :]
        elif line == "locked" or line.startswith("locked "):
            # Bare when `git worktree lock` was given no reason, else
            # "locked <reason>". Either way the flag is what matters.
            locked = True
        elif not line.strip() and path is not None:
            worktrees.append(_Worktree(path, head, branch, locked))
            path = None
    if path is not None:
        worktrees.append(_Worktree(path, head, branch, locked))
    return worktrees


def _default_branch(repo_dir: Path) -> str | None:
    """The branch everything is measured as merged into, or None if unresolvable.

    ``origin/HEAD`` is the honest answer where a remote exists; ``main`` is the
    fallback, and is itself verified rather than assumed, so a repo with neither
    disables the merged-ness checks instead of comparing against nothing.
    """
    result = _git(repo_dir, "symbolic-ref", "--short", "refs/remotes/origin/HEAD")
    if result.returncode == 0 and "/" in result.stdout:
        return result.stdout.strip().split("/", 1)[1]
    if _git(repo_dir, "rev-parse", "--verify", "--quiet", "main").returncode == 0:
        return "main"
    return None


def _is_ancestor(repo_dir: Path, commit: str, of: str) -> bool:
    return _git(repo_dir, "merge-base", "--is-ancestor", commit, of).returncode == 0


def _admin_dir(worktree: Path) -> Path | None:
    """A linked worktree's per-worktree git directory, or None.

    Read out of the worktree's own ``.git``, which for a linked worktree is a
    FILE holding ``gitdir: <path>``, rather than guessed as
    ``<repo>/.git/worktrees/<basename>``: git disambiguates colliding basenames
    by suffixing them, so the guess is wrong exactly when two worktrees are
    named alike, and silently wrong at that.
    """
    dot_git = worktree / ".git"
    if not dot_git.is_file():
        return None
    try:
        text = dot_git.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    if not text.startswith("gitdir:"):
        return None
    path = Path(text[len("gitdir:") :].strip())
    return path if path.is_dir() else None


def _seconds_since_activity(worktree: Path) -> float | None:
    """Seconds since the last git command in ``worktree``, or None if unknown.

    Times the per-worktree ``index``, which every ordinary git command in a
    worktree rewrites -- verified for a bare ``git status``, the cheapest thing
    a session does. One ``stat``, no directory walk, so it stays cheap on a
    checkout of this size.

    MUST BE READ BEFORE ``_worktree_status``, whose own ``git status``
    refreshes the very index being timed and would therefore report every
    worktree as active.  That probe restores the mtime it perturbs, but only
    best-effort, so the ordering stays load-bearing.

    ``HEAD`` is the fallback for a worktree with no index yet, which is what a
    just-created one looks like for the moment before anything stages.
    """
    admin = _admin_dir(worktree)
    if admin is None:
        return None
    for name in ("index", "HEAD"):
        candidate = admin / name
        try:
            return max(0.0, time.time() - candidate.stat().st_mtime)
        except OSError:
            continue
    return None


def _worktree_status(worktree: Path) -> tuple[bool, list[str]]:
    """One ``git status --porcelain --ignored`` probe: ``(dirty, ignored)``.

    ``dirty`` is True on any uncommitted change, tracked or untracked -- and on
    a status failure, since unreadable state is not a state to delete on.
    ``ignored`` holds the ``!!``-prefixed entries: gitignored files, plus each
    wholly-ignored directory as one ``dir/`` entry, worktree-relative with the
    forward slashes porcelain output uses on every platform, Windows included.
    ``--ignored`` matters because a plain ``git status --porcelain`` omits
    ignored files and ``git worktree remove`` does not check for them either
    (verified: it removes them without complaint), so this probe is the only
    thing standing between a gitignored report and silent deletion.

    The probe restores the index mtime it refreshes.  ``git status`` rewrites
    the per-worktree index, the very file ``_seconds_since_activity`` times,
    so without the restore the NEXT maintenance run inside the grace hour
    would report every worktree this run probed as "git activity N min ago;
    may be in use" -- conservative direction, misleading reason.  Setting an
    mtime backward only makes git treat index entries as racily clean and
    re-verify their contents, so the restore cannot make git wrong, and it is
    best-effort: a worktree only reaches this probe after the grace hour of
    idleness, so a concurrent git command racing the restore is already the
    residual case the activity check bounds.
    """
    admin = _admin_dir(worktree)
    index = None if admin is None else admin / "index"
    try:
        before = None if index is None else index.stat()
    except OSError:
        before = None
    result = _git(worktree, "status", "--porcelain", "--ignored")
    if before is not None:
        try:
            os.utime(index, ns=(before.st_atime_ns, before.st_mtime_ns))
        except OSError:
            pass  # restore is best-effort; failing leaves the conservative side
    if result.returncode != 0:
        return True, []
    dirty = False
    ignored: list[str] = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue
        if line.startswith("!!"):
            ignored.append(line[3:])
        else:
            dirty = True
    return dirty, ignored


def _ignored_summary(entries: list[str]) -> str:
    """Name what was found, capped so one worktree cannot flood the report."""
    shown = ", ".join(entries[:3])
    extra = len(entries) - 3
    return shown if extra <= 0 else f"{shown}, and {extra} more"


def _is_regenerable_cache(entry: str) -> bool:
    """Whether an ignored entry is a tool cache and nothing else.

    Bytecode and test/lint caches are written by running the tool again, so they
    are not content in the sense the ignored-content condition cares about. See
    "WHAT COUNTS AS IGNORED CONTENT" in this module's docstring.
    """
    return any(part in _REGENERABLE_CACHE_DIRS for part in PurePosixPath(entry).parts)


def _content_exists_elsewhere(here: Path, there: Path) -> bool:
    """Whether every file under ``here`` also sits byte-identical under ``there``.

    Deliberately ONE-DIRECTIONAL: extra files under ``there`` are irrelevant, since
    the question is only whether removing ``here`` loses anything. A worktree's
    ``.claude/settings.local.json`` is typically a copy of the clone's, while the
    clone's ``.claude/`` also holds ``worktrees/`` -- a both-ways "are these
    directories equal" test would answer no and spare the worktree forever.

    An empty directory answers True: there is nothing in it to lose. A subtree
    larger than ``_COMPARE_FILE_BUDGET`` answers False without reading it, so a
    maintenance run cannot turn into a byte-compare of somebody's ``.venv``; that
    errs toward sparing, which is the safe direction.
    """
    if here.is_file():
        return there.is_file() and filecmp.cmp(here, there, shallow=False)
    if not here.is_dir():
        return False  # a symlink or something stranger: not ours to judge
    seen = 0
    for dir_path, _dir_names, file_names in os.walk(here):
        for file_name in file_names:
            seen += 1
            if seen > _COMPARE_FILE_BUDGET:
                return False
            mine = Path(dir_path) / file_name
            theirs = there / mine.relative_to(here)
            if not theirs.is_file() or not filecmp.cmp(mine, theirs, shallow=False):
                return False
    return True


def _unique_ignored(
    worktree: Path, main_worktree: Path, entries: list[str]
) -> list[str]:
    """The ignored entries that exist ONLY in this worktree, in report order.

    What is left is what removing the worktree would actually destroy, and so what
    the ignored-content condition should spare it for.
    """
    unique: list[str] = []
    for entry in entries:
        if _is_regenerable_cache(entry):
            continue
        rel = entry.rstrip("/")
        if _content_exists_elsewhere(worktree / rel, main_worktree / rel):
            continue
        unique.append(entry)
    return unique


def _agent_branches(repo_dir: Path) -> list[str]:
    result = _git(
        repo_dir,
        "for-each-ref",
        "--format=%(refname:short)",
        f"refs/heads/{_AGENT_BRANCH_PREFIX}",
    )
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def _self_worktree(worktrees: list[_Worktree]) -> Path | None:
    """The worktree this module is executing from, if it is one of ``worktrees``."""
    here = Path(__file__).resolve()
    for worktree in worktrees:
        try:
            if here.is_relative_to(worktree.path.resolve()):
                return worktree.path.resolve()
        except OSError:
            continue
    return None


def _sweep_empty_dirs(checkout_root: Path, report: CleanupReport) -> None:
    """Delete empty directories left under ``.claude/worktrees/``, then the parent.

    ``checkout_root`` is the root of a checkout whose ``.claude/worktrees/`` is
    to be swept.  The caller passes the MAIN worktree's root (the first record
    of ``git worktree list``), not merely the checkout the tool happens to be
    running from: run from a linked worktree, the running checkout's own
    ``.claude/worktrees/`` is not where the main repo's husks live, and they
    would otherwise never be swept.

    Git never removes these, and two ordinary paths produce them, both seen on
    the first real run of this module: ``worktree prune`` drops the admin record
    of a worktree whose directory was deleted by hand but leaves any surviving
    directory skeleton, and on Windows a ``worktree remove`` that trips over a
    held file handle can empty the directory and still fail to unlink it
    ("Permission denied"), leaving a husk that no later pass would ever revisit.

    Only a LITERALLY empty directory is removed, which is what makes this safe
    against a session concurrently setting one up: a live worktree holds a
    checkout within moments of being created.

    A husk that will not unlink is noted, not counted as an error.  It holds no
    work and no git state, and the handle pinning it belongs to some process
    that will exit -- letting that raise the whole run's exit status would mean
    a red maintenance run every time until someone hunts down a locked empty
    folder.  ``report.errors`` stays reserved for failing to remove a real
    worktree or a real branch.
    """
    parent = checkout_root / _WORKTREE_PARENT
    if not parent.is_dir():
        return
    for child in sorted(parent.iterdir()):
        if not child.is_dir() or any(child.iterdir()):
            continue
        try:
            child.rmdir()
            report.removed_worktrees.append(f"{child} (empty leftover directory)")
        except OSError as exc:
            report.kept_worktrees.append((str(child), f"empty but unremovable: {exc}"))
    try:
        if not any(parent.iterdir()):
            parent.rmdir()
    except OSError:
        pass  # the parent surviving is the normal case, not a finding


def clean_worktrees(
    repo_dir: Path, *, activity_grace_seconds: float = _ACTIVITY_GRACE_SECONDS
) -> CleanupReport:
    """Prune, remove finished agent worktrees, then delete their merged branches.

    Nothing here raises on a per-item failure: a worktree that will not remove
    or a branch that will not delete lands in ``report.errors`` and the pass
    continues, so one wedged leftover cannot block the rest of the cleanup.
    """
    report = CleanupReport()

    prune = _git(repo_dir, "worktree", "prune")
    report.pruned = prune.returncode == 0
    if not report.pruned:
        report.errors.append(f"worktree prune: {prune.stderr.strip()}")

    worktrees = _list_worktrees(repo_dir)
    default = _default_branch(repo_dir)
    self_path = _self_worktree(worktrees)

    # worktrees[0] is the main worktree; the rest are the linked ones.
    for worktree in worktrees[1:]:
        name = str(worktree.path)
        if self_path is not None and worktree.path.resolve() == self_path:
            report.kept_worktrees.append((name, "is the running checkout"))
            continue
        if not worktree.path.is_dir():
            report.kept_worktrees.append((name, "directory is gone but prune kept it"))
            continue
        if worktree.locked:
            report.kept_worktrees.append((name, "locked via `git worktree lock`"))
            continue
        # Before _worktree_status, whose probe refreshes the index this reads
        # (its mtime restore is only best-effort). See _seconds_since_activity.
        idle = _seconds_since_activity(worktree.path)
        if idle is None:
            report.kept_worktrees.append((name, "cannot read its git activity stamp"))
            continue
        if idle < activity_grace_seconds:
            report.kept_worktrees.append(
                (name, f"git activity {int(idle // 60)} min ago; may be in use")
            )
            continue
        dirty, ignored = _worktree_status(worktree.path)
        if dirty:
            report.kept_worktrees.append((name, "has uncommitted or untracked changes"))
            continue
        unique_ignored = _unique_ignored(worktree.path, worktrees[0].path, ignored)
        if unique_ignored:
            report.kept_worktrees.append(
                (name, f"holds gitignored content ({_ignored_summary(unique_ignored)})")
            )
            continue
        if default is None:
            report.kept_worktrees.append((name, "no default branch to compare against"))
            continue
        if worktree.head is None or not _is_ancestor(repo_dir, worktree.head, default):
            report.kept_worktrees.append((name, f"HEAD is not merged into {default}"))
            continue
        result = _git(repo_dir, "worktree", "remove", str(worktree.path))
        if result.returncode == 0:
            report.removed_worktrees.append(name)
        else:
            report.errors.append(f"worktree remove {name}: {result.stderr.strip()}")

    # Sweep the MAIN worktree's husks (worktrees[0] -- see _list_worktrees),
    # wherever the tool is running from; keep sweeping the running checkout's
    # own .claude/worktrees/ too when that is a different place.
    _sweep_empty_dirs(worktrees[0].path, report)
    if repo_dir.resolve() != worktrees[0].path.resolve():
        _sweep_empty_dirs(repo_dir, report)

    # Re-list: a branch held by a worktree removed above is only now deletable.
    still_checked_out = {
        worktree.branch for worktree in _list_worktrees(repo_dir) if worktree.branch
    }
    for branch in _agent_branches(repo_dir):
        if branch in still_checked_out:
            report.kept_branches.append((branch, "still checked out in a worktree"))
            continue
        if default is None:
            report.kept_branches.append(
                (branch, "no default branch to compare against")
            )
            continue
        if not _is_ancestor(repo_dir, branch, default):
            report.kept_branches.append((branch, f"not merged into {default}"))
            continue
        result = _git(repo_dir, "branch", "-d", branch)
        if result.returncode == 0:
            report.deleted_branches.append(branch)
        else:
            report.errors.append(f"branch -d {branch}: {result.stderr.strip()}")

    return report


def print_report(report: CleanupReport) -> None:
    """Print the pass in the one-line-per-fact style the maintenance script uses."""
    for name in report.removed_worktrees:
        print(f"worktrees: removed {name}")
    for name, reason in report.kept_worktrees:
        print(f"worktrees: kept {name} ({reason})")
    for branch in report.deleted_branches:
        print(f"worktrees: deleted branch {branch}")
    for branch, reason in report.kept_branches:
        print(f"worktrees: kept branch {branch} ({reason})")
    for error in report.errors:
        print(f"worktrees: ERROR {error}")
    if not (
        report.removed_worktrees
        or report.kept_worktrees
        or report.deleted_branches
        or report.kept_branches
        or report.errors
    ):
        print("worktrees: nothing to clean")
