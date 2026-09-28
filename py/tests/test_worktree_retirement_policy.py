"""Cheap static policy lint for worktree-retirement mutations."""

import ast
from pathlib import Path

from repo_util import codex_worktree_retirement
from repo_util import git_worktree_cleanup
from repo_util import worktree_retirement as retirement
from repo_util import worktree_retirement_execution as execution


def test_only_shared_engine_contains_nonforced_git_retirement():
    # Every module of the retirement family, found by name so that a module added to it is
    # linted too, and the two compatibility modules.  The operational simulation is a test,
    # not part of the engine, so it is left out.
    family = sorted(
        path
        for path in Path(retirement.__file__).parent.glob("worktree_retirement*.py")
        if not path.stem.endswith("_test")
    )
    sources = (
        *family,
        Path(git_worktree_cleanup.__file__),
        Path(codex_worktree_retirement.__file__),
    )
    mutations = []
    for source in sources:
        tree = ast.parse(source.read_text(encoding="utf-8"))
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
                mutations.append((source.stem, constants[:2]))
    engine = Path(execution.__file__).stem
    assert mutations == [
        (engine, ["worktree", "remove"]),
        (engine, ["branch", "-d"]),
    ]
