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

Any other launcher fails it: a ``subprocess`` function other than ``run``,
``os.system``, ``os.popen``, an ``os.spawn*`` or ``os.exec*`` function, or a function
imported from ``repo_util.user_config_sync``, ``repo_util.worktree_retirement_git`` or
``repo_util.worktree_retirement_inspection`` other than ``_run_git``, ``_command_error``
and the three helpers.  A scan that finds no launch fails.  The lint checks only these
launch bounds; no test exercises either module's behaviour.
"""

import ast

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
_OS_LAUNCHER_PREFIXES = ("spawn", "exec")


def _imported_names(tree):
    """Map each name bound by an import to (module, original name or None)."""
    names = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                names[alias.asname or alias.name] = (node.module, alias.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names[alias.asname or alias.name.split(".")[0]] = (alias.name, None)
    return names


def _keywords(call):
    return {keyword.arg for keyword in call.keywords}


def _check_module_call(module, attribute, call, where, launches, problems):
    if module == "subprocess":
        if attribute != "run":
            problems.append(f"{where}: subprocess.{attribute} is not allowed")
            return
        launches.append(where)
        missing = {"timeout", "env"} - _keywords(call)
        if missing:
            problems.append(f"{where}: subprocess.run lacks {sorted(missing)}")
    elif module == "os" and (
        attribute in ("system", "popen") or attribute.startswith(_OS_LAUNCHER_PREFIXES)
    ):
        problems.append(f"{where}: os.{attribute} is not allowed")


def _check_imported_call(module, name, call, where, launches, problems):
    if module not in _IMPORTED_LAUNCHER_MODULES:
        return
    if name == "_command_error":
        return
    if name == "_run_git":
        launches.append(where)
        if "timeout_seconds" not in _keywords(call):
            problems.append(f"{where}: _run_git lacks timeout_seconds")
    elif name in _HELPERS:
        launches.append(where)
        missing = {"timeout_seconds", "noninteractive"} - _keywords(call)
        if missing:
            problems.append(f"{where}: {name} lacks {sorted(missing)}")
    else:
        problems.append(f"{where}: {module}.{name} is not an allowed launcher")


def _scan(rel, wrapper):
    tree = ast.parse(
        (paths.repo_root() / rel).read_text(encoding="utf-8"), filename=rel
    )
    assert any(
        isinstance(node, ast.FunctionDef) and node.name == wrapper for node in tree.body
    ), f"{rel} no longer defines its wrapper {wrapper}"
    imports = _imported_names(tree)
    launches = []
    problems = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        where = f"{rel}:{node.lineno}"
        func = node.func
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            module, original = imports.get(func.value.id, (None, None))
            if module is not None and original is None:
                _check_module_call(module, func.attr, node, where, launches, problems)
        elif isinstance(func, ast.Name):
            if func.id == wrapper and func.id not in imports:
                launches.append(where)
            elif func.id in imports:
                module, original = imports[func.id]
                if module in ("subprocess", "os") and original is not None:
                    _check_module_call(
                        module, original, node, where, launches, problems
                    )
                else:
                    _check_imported_call(
                        module, original, node, where, launches, problems
                    )
    return launches, problems


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
