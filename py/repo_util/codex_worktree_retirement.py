"""Compatibility API: Codex selection uses the shared retirement mechanism.

Schema-1 plans must be prepared again: they lack shared runtime and object gates.
"""

from repo_util.worktree_retirement import RetirementError
from repo_util.worktree_retirement import execute_retirement as _execute_retirement
from repo_util.worktree_retirement import prepare_retirement as _prepare_retirement

__all__ = ["RetirementError", "prepare_retirement", "execute_retirement"]


def prepare_retirement(worktree_path, **kwargs):
    """Preserve the old Codex selector without preserving a separate policy."""
    return _prepare_retirement(worktree_path, owner_selector="codex", **kwargs)


def execute_retirement(preflight_file, **kwargs):
    """Keep the old Codex selection guard while executing the shared policy."""
    return _execute_retirement(preflight_file, owner_selector="codex", **kwargs)
