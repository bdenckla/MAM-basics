"""Mechanical safety lint across the finite worktree-retirement implementation."""

import ast
import re
from pathlib import Path

from repo_util import worktree_retirement as retirement

_ADAPTER_MODULES = (
    "repo_util/git_worktree_cleanup.py",
    "repo_util/codex_worktree_retirement.py",
    "repo_util/clean_worktrees.py",
    "repo_util/worktree_owners.py",
    "main_repo_util.py",
    "main_repo_maintenance.py",
)
_ENGINE = "repo_util/worktree_retirement_execution.py"
_RELOCATION = "repo_util/worktree_retirement_relocation.py"
_SHORT_OPTION_CLUSTER = re.compile(r"-[A-Za-z]+")
# Git writes object and pack files read-only, which Windows will not delete, so the one
# admitted keyword is the shared handler that clears that attribute and retries;
# ignore_errors, onerror and any other handler stay refused.
_READ_ONLY_RETRY = "repo_util.common.clear_read_only_and_retry"


def _short_options(token):
    """The option letters of a single-dash cluster such as -df; none for any other token."""
    if isinstance(token, str) and _SHORT_OPTION_CLUSTER.fullmatch(token):
        return frozenset(token[1:])
    return frozenset()


def _long_option(token, option):
    """Whether Git reads ``token`` as the long ``option``.

    Git accepts the whole name or any prefix that no other option of the command
    shares: ``git worktree remove`` reads ``--f`` to ``--forc`` as ``--force``, and
    ``git branch`` reads ``--d`` to ``--delet`` as ``--delete`` and ``--forc`` as
    ``--force``.  A prefix that Git finds ambiguous is refused here as well.
    """
    return (
        isinstance(token, str)
        and len(token) > 2
        and token.startswith("--")
        and option.startswith(token)
    )


def _forces(token):
    """--force or an abbreviation of it, or a short-option cluster holding f or D."""
    return _long_option(token, "--force") or bool(_short_options(token) & {"f", "D"})


def _deletes_branch(token):
    """--delete or an abbreviation of it, or a short-option cluster holding d or D."""
    return _long_option(token, "--delete") or bool(_short_options(token) & {"d", "D"})


def _argument_tokens(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value.split()
    if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
        return [token for item in node.elts for token in _argument_tokens(item)]
    if isinstance(node, ast.Starred):
        return _argument_tokens(node.value)
    if isinstance(node, ast.JoinedStr):
        return [token for item in node.values for token in _argument_tokens(item)]
    return []


def _qualified_name(node, imports):
    if isinstance(node, ast.Name):
        return imports.get(node.id, node.id)
    if isinstance(node, ast.Attribute):
        return _qualified_name(node.value, imports) + "." + node.attr
    return ""


class _PolicyVisitor(ast.NodeVisitor):
    def __init__(self, module, tree):
        self.module = module
        self.functions = []
        self.mutations = set()
        self.recursive_removals = set()
        self.imports = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    self.imports[alias.asname or alias.name] = alias.name
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    self.imports[alias.asname or alias.name] = (
                        f"{node.module}.{alias.name}"
                    )
        self.parents = {
            child: parent
            for parent in ast.walk(tree)
            for child in ast.iter_child_nodes(parent)
        }

    def visit_FunctionDef(self, node):
        self.functions.append(node.name)
        self.generic_visit(node)
        self.functions.pop()

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Constant(self, node):
        # These finite retirement modules have no use for a literal force flag, alone or
        # in a short-option cluster such as -df. This also catches flags in separately
        # assigned argument sequences.
        assert not _forces(node.value), (
            self.module,
            node.lineno,
            node.value,
        )

    def _check_tokens(self, node, tokens):
        worktree = "worktree" in tokens
        branch_delete = "branch" in tokens and any(
            _deletes_branch(token) for token in tokens
        )
        assert not (worktree and "prune" in tokens), (
            self.module,
            node.lineno,
            tokens,
        )
        worktree_remove = worktree and "remove" in tokens
        if worktree_remove or branch_delete:
            assert not any(_forces(token) for token in tokens), (
                self.module,
                node.lineno,
                tokens,
            )
            assert self.module == _ENGINE, (self.module, node.lineno, tokens)
            operation = "worktree remove" if worktree_remove else "branch -d"
            self.mutations.add((node.lineno, operation))
        lowered = [token.casefold() for token in tokens]
        recursive_shell = (
            ("remove-item" in lowered and "-recurse" in lowered)
            or (
                any(command in lowered for command in ("rd", "rmdir"))
                and "/s" in lowered
            )
            or (
                "rm" in lowered
                and any(
                    token.startswith("-") and "r" in token[1:].casefold()
                    for token in tokens
                )
            )
        )
        assert not recursive_shell, (self.module, node.lineno, tokens)

    def visit_Call(self, node):
        tokens = [
            token
            for argument in (*node.args, *(keyword.value for keyword in node.keywords))
            for token in _argument_tokens(argument)
        ]
        self._check_tokens(node, tokens)
        name = _qualified_name(node.func, self.imports)
        if name in ("shutil.rmtree", "os.removedirs"):
            function = self.functions[-1] if self.functions else None
            expected = {
                (_RELOCATION, "_relocate_novc"): "source",
                ("main_repo_maintenance.py", "_clean_one_novc"): "novc",
            }.get((self.module, function))
            assert name == "shutil.rmtree" and expected is not None, (
                self.module,
                function,
                node.lineno,
                name,
            )
            assert len(node.args) == 1 and [k.arg for k in node.keywords] == [
                "onexc"
            ], (
                self.module,
                function,
                node.lineno,
            )
            handler = _qualified_name(node.keywords[0].value, self.imports)
            assert handler == _READ_ONLY_RETRY, (
                self.module,
                function,
                node.lineno,
                handler,
            )
            assert isinstance(node.args[0], ast.Name) and node.args[0].id == expected, (
                self.module,
                function,
                node.lineno,
            )
            self.recursive_removals.add((node.lineno, function, expected))
        self.generic_visit(node)

    def _visit_sequence(self, node):
        # Calls inspect their argument containers; inspect assigned command lists
        # separately so subprocess.run(command) cannot hide their contents.
        ancestor = self.parents.get(node)
        while ancestor is not None and not isinstance(ancestor, ast.Call):
            ancestor = self.parents.get(ancestor)
        if ancestor is None:
            self._check_tokens(node, _argument_tokens(node))
        self.generic_visit(node)

    visit_List = _visit_sequence
    visit_Tuple = _visit_sequence
    visit_Set = _visit_sequence


def test_only_shared_engine_contains_nonforced_git_retirement():
    source_root = Path(retirement.__file__).resolve().parent.parent
    mutations = []
    recursive_removals = []
    # Discover the whole retirement family so later engine modules stay covered.
    family = tuple(
        path.relative_to(source_root).as_posix()
        for path in sorted((source_root / "repo_util").glob("worktree_retirement*.py"))
        if not path.stem.endswith("_test")
    )
    assert family
    modules = (*family, *_ADAPTER_MODULES)
    assert len(modules) == len(set(modules))
    for module in modules:
        source = source_root / module
        assert source.is_file(), source
        tree = ast.parse(source.read_text(encoding="utf-8"), filename=str(source))
        visitor = _PolicyVisitor(module, tree)
        visitor.visit(tree)
        mutations.extend((module, operation) for _, operation in visitor.mutations)
        recursive_removals.extend(
            (module, function, argument)
            for _, function, argument in visitor.recursive_removals
        )
    assert sorted(mutations) == sorted(
        [(_ENGINE, "worktree remove"), (_ENGINE, "branch -d")]
    )
    assert sorted(recursive_removals) == sorted(
        [
            (_RELOCATION, "_relocate_novc", "source"),
            ("main_repo_maintenance.py", "_clean_one_novc", "novc"),
        ]
    )
