"""Lint: Taamey D's build imports nothing but the standard library and itself.

By Ben's decision of 2026-10-28, the scripts that are to ship in Taamey D's source archives,
py/main_taamey_d_build.py and its package py/taamey_d_build/, are licensed GPL-2.0-or-later,
while the rest of py/, mb_cmn included, is GPL-3.0. So these files may import nothing
GPL-3.0: such an import would make the shipped build a GPL-3.0 program, and the archive,
which carries only these files, would not run without the imported module besides. They
import only the standard library, as sys.stdlib_module_names lists it, and taamey_d_build
and its modules. A relative import counts as the module it resolves to, and a dynamic
import, through __import__ or importlib.import_module, must name its module with a string
literal that this lint can read.

Taamey-D/font-m-TaD/ffscript_generate_sfd_n_ttf.py, which the archives carry too, is
outside this lint: FontForge runs it, and it imports fontforge.

This is a mechanical lint over source text, one of the two test shapes AGENTS.md sanctions.
It reads the files from disk, so a module not yet staged is checked as well, and it fails
rather than skips: a missing entry point or a package with no module fails.

Run:
    .venv/Scripts/python.exe py/main_test.py py/tests/test_taamey_d_build_imports.py
"""

from __future__ import annotations

import ast
import importlib.util
import sys

from mb_cmn import paths

_PACKAGE = "taamey_d_build"
_ENTRY_POINT = "main_taamey_d_build"
_ALLOWED_TOP_LEVEL = sys.stdlib_module_names | {_PACKAGE}
_DYNAMIC_IMPORTERS = frozenset({"__import__", "import_module"})


def _scanned_files() -> list[tuple[str, str]]:
    """(repo-relative path, module name) for the entry point and each package module."""
    py_root = paths.repo_root() / "py"
    entry_point = py_root / f"{_ENTRY_POINT}.py"
    assert entry_point.is_file(), f"py/{_ENTRY_POINT}.py is missing: nothing to lint"
    modules = sorted(
        path
        for path in (py_root / _PACKAGE).rglob("*.py")
        if "__pycache__" not in path.parts
    )
    assert modules, f"py/{_PACKAGE}/ holds no module: the lint would read no package"
    scanned = [(f"py/{_ENTRY_POINT}.py", _ENTRY_POINT)]
    for path in modules:
        rel = path.relative_to(py_root)
        scanned.append((f"py/{rel.as_posix()}", ".".join(rel.with_suffix("").parts)))
    return scanned


def _imported_names(node: ast.AST, package: str) -> list[str] | str | None:
    """The modules one node imports, why they cannot be read, or None for no import."""
    if isinstance(node, ast.Import):
        return [alias.name for alias in node.names]
    if isinstance(node, ast.ImportFrom):
        if not node.level:
            return [node.module or ""]
        try:
            relative = "." * node.level + (node.module or "")
            return [importlib.util.resolve_name(relative, package)]
        except ImportError as error:
            return f"a relative import that resolves to no module ({error})"
    if isinstance(node, ast.Call):
        callee = getattr(node.func, "attr", None) or getattr(node.func, "id", None)
        if callee not in _DYNAMIC_IMPORTERS:
            return None
        first = node.args[0] if node.args else None
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            return [first.value]
        return (
            f"a dynamic import, {ast.unparse(node)}, whose module this lint cannot read"
        )
    return None


def _import_problems(rel: str, module: str, source: str) -> list[str]:
    """Every import in one file of the build that names a module outside the rule."""
    package = module.rpartition(".")[0]
    problems = []
    for node in ast.walk(ast.parse(source, filename=rel)):
        names = _imported_names(node, package)
        if names is None:
            continue
        where = f"{rel}:{node.lineno}"
        if isinstance(names, str):
            problems.append(f"{where}: {names}")
            continue
        for name in names:
            if name.partition(".")[0] not in _ALLOWED_TOP_LEVEL:
                problems.append(
                    f"{where}: imports {name}, which is neither in the standard"
                    f" library nor in {_PACKAGE}"
                )
    return problems


def test_taamey_d_build_imports_only_the_standard_library_and_itself() -> None:
    root = paths.repo_root()
    problems = []
    for rel, module in _scanned_files():
        source = (root / rel).read_text(encoding="utf-8")
        problems.extend(_import_problems(rel, module, source))
    assert not problems, (
        "Taamey D's build ships under GPL-2.0-or-later, so it may import only the"
        f" standard library and {_PACKAGE} (Ben's decision of 2026-10-28):\n  "
        + "\n  ".join(problems)
    )
