"""Single __file__-relative source of truth for repo-root paths.

See GitHub issue #75: this replaces both cwd-relative literals
(e.g. "../MAM-parsed") and scattered Path(__file__).resolve().parents[N]
call sites, each of which encoded its own magic depth number. Every
sibling-repo path should be built by /-chaining off repo_root() or
repos_root() instead.
"""

from pathlib import Path

_THIS_FILE = Path(__file__).resolve()


def repo_root() -> Path:
    """Return the MAM-basics repo root (parent of the py/ directory)."""
    return _THIS_FILE.parents[2]


def repos_root() -> Path:
    """Return the GitRepos/ directory containing the sibling MAM-* repos."""
    return repo_root().parent


def sibling_repo(name: str) -> Path:
    """Return the path to a sibling repo under GitRepos/, e.g. "MAM-parsed"."""
    return repos_root() / name
