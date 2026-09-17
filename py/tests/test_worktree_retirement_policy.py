"""Cheap static policy lint for worktree-retirement mutations."""

import ast
from pathlib import Path

from repo_util import codex_worktree_retirement
from repo_util import git_worktree_cleanup
from repo_util import worktree_retirement as retirement


def test_only_shared_engine_contains_nonforced_git_retirement():
    modules = (retirement, git_worktree_cleanup, codex_worktree_retirement)
    mutations = []
    for module in modules:
        tree = ast.parse(Path(module.__file__).read_text(encoding="utf-8"))
        assert not any(
            isinstance(node, ast.Constant) and node.value in ("--force", "-D")
            for node in ast.walk(tree)
        )
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            constants = [
                arg.value for arg in node.args if isinstance(arg, ast.Constant)
            ]
            if constants[:2] in (["worktree", "remove"], ["branch", "-d"]):
                mutations.append((module.__name__, constants[:2]))
    assert mutations == [
        (retirement.__name__, ["worktree", "remove"]),
        (retirement.__name__, ["branch", "-d"]),
    ]
