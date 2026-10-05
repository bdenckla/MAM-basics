"""Lint: every process the forest synchronizer launches is bounded in time.

A mechanical lint over the syntax trees of ``py/repo_util/forest_sync.py`` and
``py/repo_util/forest_environments.py``, added for finding 25 of the 2026-09-29 review,
whose remediation plan Ben approved on 2026-09-30.  It passes only if:

1. every ``subprocess.run`` passes ``timeout=`` and ``env=``;
2. every ``_run_git`` call passes ``timeout_seconds=``;
3. every call of ``_list_worktrees``, ``_status_entries`` or ``_operation_markers``
   passes ``timeout_seconds=`` and ``noninteractive=``;
4. every other launch is a call of one of the modules' own wrappers,
   ``forest_sync._git`` or ``forest_environments._run_python``, whose bodies are calls
   that items 1 and 2 check.

Each launch that the scan records is then checked for its values.  A ``timeout=`` or
``timeout_seconds=`` value is a positive, finite ``int`` or ``float`` literal, ``True``
excluded, or a name or module attribute that a module under ``py/`` binds at its top
level only to such literals, directly or through ``from ... import``:
``GIT_TIMEOUT_SECONDS = 60`` counts, but a name that its module also binds to ``None``
or to anything else, or declares ``global`` in a function, does not, and neither does a
name that the calling function binds itself, as a parameter or otherwise.
``noninteractive=`` is the literal ``True``, and ``env=`` is not the literal ``None``.

Any other launcher fails it: a ``subprocess`` function other than ``run``;
``os.system``, ``os.popen`` or ``os.startfile``, or an ``os.spawn*``, ``os.exec*``,
``os.posix_spawn*`` or ``os.fork*`` function; ``asyncio``'s ``create_subprocess_*``; or
a function of ``repo_util.user_config_sync``, ``repo_util.worktree_retirement_git`` or
``repo_util.worktree_retirement_inspection`` other than ``_run_git``, ``_command_error``
and the three helpers.  Each of these is recognized whether it is called by a name
that a ``from ... import`` names explicitly or through a module or package that an
import statement binds, such as ``g._git`` after
``from repo_util import worktree_retirement_git as g`` or
``repo_util.user_config_sync._run_git`` after ``import repo_util.user_config_sync``;
a name that a star import binds, and a module reached through ``getattr``,
``__import__`` or ``importlib``, are not recognized.
A relative import is resolved against the scanned file's package, so in
``repo_util`` both ``from .user_config_sync import _run_git`` and
``from . import user_config_sync`` name ``repo_util.user_config_sync``.

This syntax lint does not follow a call through a name bound other than by an import,
such as a local alias or a ``functools.partial`` object, and it does not see a launch
inside a function of a module it does not list.  A scan that finds no launch fails.
The lint checks only these launch bounds; no test exercises either module's behaviour.
"""

import ast
import math
from pathlib import Path

from mb_cmn import paths

# Each scanned module and its own process wrapper.
_MODULES = {
    "py/repo_util/forest_sync.py": "_git",
    "py/repo_util/forest_environments.py": "_run_python",
}
_IMPORTED_LAUNCHER_MODULES = frozenset(
    {
        "repo_util.user_config_sync",
        "repo_util.worktree_retirement_git",
        "repo_util.worktree_retirement_inspection",
    }
)
_HELPERS = frozenset({"_list_worktrees", "_status_entries", "_operation_markers"})
_OS_LAUNCHERS = frozenset({"system", "popen", "startfile"})
_OS_LAUNCHER_PREFIXES = ("spawn", "exec", "posix_spawn", "fork")
_ASYNCIO_MODULES = frozenset({"asyncio", "asyncio.subprocess"})
_FUNCTIONS = (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)
_COMPREHENSIONS = (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)


def _package(rel):
    """The dotted package of a scanned file under ``py/``, such as ``repo_util``."""
    parts = rel.split("/")
    assert parts[0] == "py", rel
    return ".".join(parts[1:-1])


def _absolute_module(node, package):
    """The absolute module that an ``ImportFrom`` names, its level resolved in ``package``."""
    if not node.level:
        return node.module
    base = package.split(".") if package else []
    assert node.level <= len(base), (package, node.level, node.module)
    parts = base[: len(base) - node.level + 1]
    return ".".join([*parts, node.module] if node.module else parts)


def _imported_names(tree, package):
    """Map each name bound by an import to (module, original name or None).

    ``import a.b.c`` binds ``a`` to the package ``a``; ``import a.b.c as m`` binds
    ``m`` to the module ``a.b.c``; a relative ``from`` import names the module that
    its level gives in ``package``.
    """
    names = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = _absolute_module(node, package)
            for alias in node.names:
                names[alias.asname or alias.name] = (module, alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    names[alias.asname] = (alias.name, None)
                else:
                    root = alias.name.split(".")[0]
                    names[root] = (root, None)
    return names


def _call_target(func, imports):
    """Return (module, function) for a call of an imported function, else None.

    A name that ``from M import f`` binds gives (M, f).  An attribute chain whose root
    an import binds gives the dotted module the chain names and its last attribute:
    ``g.f`` after ``import M as g`` gives (M, f), ``g.f`` after ``from P import m as g``
    gives (P.m, f), and ``p.m.f`` after ``import p.m`` gives (p.m, f).  A value such as
    ``fe.GIT_TIMEOUT_SECONDS`` resolves the same way.
    """
    chain = []
    while isinstance(func, ast.Attribute):
        chain.append(func.attr)
        func = func.value
    if not isinstance(func, ast.Name) or func.id not in imports:
        return None
    module, original = imports[func.id]
    if not chain:
        return None if original is None else (module, original)
    chain.reverse()
    base = module if original is None else f"{module}.{original}"
    return ".".join([base, *chain[:-1]]), chain[-1]


def _module_path(module):
    """The file under ``py/`` that defines the dotted ``module``, or None."""
    if not module:
        return None
    base = paths.repo_root() / "py" / Path(*module.split("."))
    for candidate in (base.parent / f"{base.name}.py", base / "__init__.py"):
        if candidate.is_file():
            return candidate
    return None


def _positive_literal(node):
    return (
        isinstance(node, ast.Constant)
        and type(node.value) in (int, float)
        and node.value > 0
        and math.isfinite(node.value)
    )


def _module_scope(tree):
    """The nodes of a module's own scope, outside every function, class or lambda body."""
    stack = list(tree.body)
    while stack:
        node = stack.pop()
        yield node
        if not isinstance(node, (*_FUNCTIONS, ast.ClassDef)):
            stack.extend(ast.iter_child_nodes(node))


def _binds(node, name):
    """Whether ``node`` binds ``name`` in the scope that holds it."""
    if isinstance(node, ast.Name):
        return node.id == name and not isinstance(node.ctx, ast.Load)
    if isinstance(node, ast.Import):
        return any(
            (alias.asname or alias.name.split(".")[0]) == name for alias in node.names
        )
    if isinstance(node, ast.ImportFrom):
        return any(
            alias.name == "*" or (alias.asname or alias.name) == name
            for alias in node.names
        )
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return node.name == name
    if isinstance(node, (ast.ExceptHandler, ast.MatchAs, ast.MatchStar)):
        return node.name == name
    if isinstance(node, ast.MatchMapping):
        return node.rest == name
    return False


def _constant(module, name, seen=frozenset()):
    """Whether ``module`` binds ``name`` at its top level only to positive literals.

    A binding by ``from ... import`` counts when the module it names binds the imported
    name the same way.  Any other binding, or a ``global`` declaration of the name
    anywhere in the module, disqualifies the name.
    """
    path = _module_path(module)
    if path is None or (module, name) in seen:
        return False
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    package = module if path.name == "__init__.py" else module.rpartition(".")[0]
    if any(
        isinstance(node, ast.Global) and name in node.names for node in ast.walk(tree)
    ):
        return False
    literal_targets = set()
    annotations_only = set()
    for node in _module_scope(tree):
        if isinstance(node, ast.Assign) and _positive_literal(node.value):
            literal_targets.update(
                id(target) for target in node.targets if isinstance(target, ast.Name)
            )
        elif isinstance(node, ast.AnnAssign):
            if node.value is None:
                annotations_only.add(id(node.target))
            elif _positive_literal(node.value):
                literal_targets.add(id(node.target))
    bindings = [
        node
        for node in _module_scope(tree)
        if _binds(node, name) and id(node) not in annotations_only
    ]
    if not bindings:
        return False
    for node in bindings:
        if id(node) in literal_targets:
            continue
        if isinstance(node, ast.ImportFrom) and all(
            alias.name != "*" for alias in node.names
        ):
            source = _absolute_module(node, package)
            if all(
                _constant(source, alias.name, seen | {(module, name)})
                for alias in node.names
                if (alias.asname or alias.name) == name
            ):
                continue
        return False
    return True


def _local_names(scope):
    """The names that a function, lambda or comprehension binds for its own body."""
    if isinstance(scope, _COMPREHENSIONS):
        return {
            node.id
            for generator in scope.generators
            for node in ast.walk(generator.target)
            if isinstance(node, ast.Name)
        }
    arguments = scope.args
    names = {
        argument.arg
        for argument in (
            *arguments.posonlyargs,
            *arguments.args,
            *arguments.kwonlyargs,
            arguments.vararg,
            arguments.kwarg,
        )
        if argument is not None
    }
    body = scope.body if isinstance(scope.body, list) else [scope.body]
    for statement in body:
        for node in ast.walk(statement):
            if isinstance(node, ast.Name):
                if not isinstance(node.ctx, ast.Load):
                    names.add(node.id)
            elif isinstance(node, ast.Import):
                names.update(
                    alias.asname or alias.name.split(".")[0] for alias in node.names
                )
            elif isinstance(node, ast.ImportFrom):
                names.update(alias.asname or alias.name for alias in node.names)
            elif isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            ):
                names.add(node.name)
            elif isinstance(node, (ast.ExceptHandler, ast.MatchAs, ast.MatchStar)):
                if node.name:
                    names.add(node.name)
    return names


class _Context:
    """What a value check needs to know about the scanned module and one call in it."""

    def __init__(self, module, imports, parents, call):
        self.module = module
        self.imports = imports
        self.local_names = set()
        ancestor = parents.get(call)
        while ancestor is not None:
            if isinstance(ancestor, (*_FUNCTIONS, *_COMPREHENSIONS)):
                self.local_names |= _local_names(ancestor)
            ancestor = parents.get(ancestor)


def _bounded(value, context):
    """A positive literal, or a name or module attribute bound only to such literals."""
    if _positive_literal(value):
        return True
    root = value
    while isinstance(root, ast.Attribute):
        root = root.value
    if not isinstance(root, ast.Name) or root.id in context.local_names:
        return False
    if isinstance(value, ast.Name):
        return _constant(context.module, value.id)
    target = _call_target(value, context.imports)
    return target is not None and _constant(*target)


def _is_true(value, _context):
    return isinstance(value, ast.Constant) and value.value is True


def _not_none(value, _context):
    return not (isinstance(value, ast.Constant) and value.value is None)


# The keywords each kind of launch must pass, with the rule that each one's value meets.
_RULES = {
    "subprocess.run": {"timeout": _bounded, "env": _not_none},
    "_run_git": {"timeout_seconds": _bounded},
    "helper": {"timeout_seconds": _bounded, "noninteractive": _is_true},
    "wrapper": {},
}


def _check_module_call(module, attribute, call, where, launches, problems):
    if module == "subprocess":
        if attribute != "run":
            problems.append(f"{where}: subprocess.{attribute} is not allowed")
            return
        launches.append((where, "subprocess.run", call))
    elif module == "os" and (
        attribute in _OS_LAUNCHERS or attribute.startswith(_OS_LAUNCHER_PREFIXES)
    ):
        problems.append(f"{where}: os.{attribute} is not allowed")
    elif module in _ASYNCIO_MODULES and attribute.startswith("create_subprocess_"):
        problems.append(f"{where}: {module}.{attribute} is not allowed")


def _check_imported_call(module, name, call, where, launches, problems):
    if module not in _IMPORTED_LAUNCHER_MODULES:
        return
    if name == "_command_error":
        return
    if name == "_run_git":
        launches.append((where, "_run_git", call))
    elif name in _HELPERS:
        launches.append((where, "helper", call))
    else:
        problems.append(f"{where}: {module}.{name} is not an allowed launcher")


def _check_launch(where, kind, call, context):
    """The problems of one recorded launch: a missing keyword or a value out of bounds."""
    label = ast.unparse(call.func)
    values = {keyword.arg: keyword.value for keyword in call.keywords if keyword.arg}
    rules = _RULES[kind]
    problems = []
    missing = sorted(set(rules) - set(values))
    if missing:
        problems.append(f"{where}: {label} lacks {missing}")
    for keyword, rule in rules.items():
        if keyword in values and not rule(values[keyword], context):
            problems.append(
                f"{where}: {label} passes {keyword}={ast.unparse(values[keyword])}"
            )
    return problems


def _scan(rel, wrapper):
    tree = ast.parse(
        (paths.repo_root() / rel).read_text(encoding="utf-8"), filename=rel
    )
    assert any(
        isinstance(node, ast.FunctionDef) and node.name == wrapper for node in tree.body
    ), f"{rel} no longer defines its wrapper {wrapper}"
    package = _package(rel)
    module = ".".join([package, Path(rel).stem] if package else [Path(rel).stem])
    imports = _imported_names(tree, package)
    parents = {
        child: parent
        for parent in ast.walk(tree)
        for child in ast.iter_child_nodes(parent)
    }
    launches = []
    problems = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        where = f"{rel}:{node.lineno}"
        func = node.func
        if isinstance(func, ast.Name) and func.id == wrapper and func.id not in imports:
            launches.append((where, "wrapper", node))
            continue
        target = _call_target(func, imports)
        if target is None:
            continue
        callee, name = target
        if callee in ("subprocess", "os", *_ASYNCIO_MODULES):
            _check_module_call(callee, name, node, where, launches, problems)
        else:
            _check_imported_call(callee, name, node, where, launches, problems)
    for where, kind, call in launches:
        context = _Context(module, imports, parents, call)
        problems.extend(_check_launch(where, kind, call, context))
    return [where for where, _, _ in launches], problems


def test_every_forest_process_launch_is_bounded():
    launches = []
    problems = []
    for rel, wrapper in _MODULES.items():
        module_launches, module_problems = _scan(rel, wrapper)
        assert module_launches, f"the scan found no process launch in {rel}"
        launches.extend(module_launches)
        problems.extend(module_problems)
    assert launches, "the scan found no process launch -- it has no input"
    assert not problems, "Unbounded or unrecognized launches:\n  " + "\n  ".join(
        problems
    )
