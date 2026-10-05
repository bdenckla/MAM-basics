"""Mechanical ownership and no-file-I/O checks for the transient compute core."""

import ast

from mb_cmn.paths import repo_root

_CORE = repo_root() / "py" / "phonetic_mam" / "core"
_COMPUTE = _CORE.parent / "compute.py"
_ALLOWED_IMPORTS = {"re", "functools", "itertools", "mb_cmn", "phonetic_mam.core"}
_FILE_CALLS = {
    "open",
    "read_text",
    "read_bytes",
    "write_text",
    "write_bytes",
    "unlink",
    "mkdir",
    "rename",
    "replace",
    "system",
    "Popen",
    "run",
}


def test_core_imports_stay_inside_the_algorithm_boundary():
    paths = sorted(_CORE.glob("*.py"))
    assert paths, "the canonical computation core is missing"
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                assert node.level == 0, path
                modules = [node.module]
            else:
                continue
            for module in modules:
                assert any(
                    module == allowed or module.startswith(allowed + ".")
                    for allowed in _ALLOWED_IMPORTS
                ), (path, module)


def test_core_has_no_filesystem_or_process_calls():
    paths = sorted(_CORE.glob("*.py"))
    assert paths
    for path in paths:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if isinstance(node.func, ast.Name):
                assert node.func.id not in _FILE_CALLS, (path, node.lineno)
            elif isinstance(node.func, ast.Attribute):
                # String replacement is an algorithm, not filesystem mutation.
                assert node.func.attr not in _FILE_CALLS - {"replace"}, (
                    path,
                    node.lineno,
                )


def test_core_contains_no_quality_marked_text_examples():
    paths = sorted(_CORE.glob("*.py"))
    assert paths
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert chr(0x05C8) not in text and chr(0x05C9) not in text, path


def test_compute_dispatch_is_literal_and_filesystem_free():
    tree = ast.parse(_COMPUTE.read_text(encoding="utf-8"))
    dispatch = [
        node.value
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "_OPERATIONS"
            for target in node.targets
        )
    ]
    assert len(dispatch) == 1
    assert isinstance(dispatch[0], ast.Dict)
    keys = [key.value for key in dispatch[0].keys if isinstance(key, ast.Constant)]
    assert len(keys) == len(dispatch[0].keys) == len(set(keys)) > 0
    assert all(isinstance(value, ast.Name) for value in dispatch[0].values)
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        # A bare name such as open(...), or an attribute such as io.open(...).
        if isinstance(node.func, ast.Name):
            called = node.func.id
        elif isinstance(node.func, ast.Attribute):
            called = node.func.attr
        else:
            continue
        forbidden = called in {"open", "eval", "exec", "getattr", "__import__"}
        assert not forbidden, node.lineno
