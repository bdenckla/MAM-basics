"""Shared preflight, preservation, retirement and resume policy for all owners.

Selection and runtime adapters live in worktree_owners. Only
worktree_retirement_execution removes a reviewed worktree or its eligible merged
branch. Inspection never prunes Git registrations or sweeps unregistered folders.
Retained data disposal is separate.

This module is the public API. The implementation is five modules; each imports, from
among the five, only those listed before it:

1. ``worktree_retirement_git``: the Git runner and path and registration primitives.
2. ``worktree_retirement_inspection``: read-only inspection and the safety snapshot.
3. ``worktree_retirement_preflight``: plan preparation, fingerprints and receipts.
4. ``worktree_retirement_relocation``: verified ``.novc`` relocation.
5. ``worktree_retirement_execution``: the destructive, resumable execution.
"""

from repo_util.worktree_retirement_execution import execute_retirement
from repo_util.worktree_retirement_git import RetirementError
from repo_util.worktree_retirement_inspection import inspect_worktrees, select_worktrees
from repo_util.worktree_retirement_preflight import SCHEMA_VERSION, prepare_retirement

__all__ = [
    "SCHEMA_VERSION",
    "RetirementError",
    "execute_retirement",
    "inspect_worktrees",
    "prepare_retirement",
    "select_worktrees",
]
