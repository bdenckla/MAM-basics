#!/usr/bin/env python3
"""
Check that all public functions (not starting with _) are defined before
any private functions (starting with _) in Python files.

Exit codes:
  0 - No violations found
  1 - Violations found

Usage:
  python check_function_ordering.py [paths...]

If no paths given, checks all .py files under the repo root recursively,
whatever the working directory.
"""

import ast
import sys
from pathlib import Path

import boj_paths


def get_function_defs(filepath: Path) -> list[tuple[str, int]]:
    """Return list of (function_name, line_number) for top-level functions."""
    try:
        source = filepath.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(filepath))
    except (SyntaxError, UnicodeDecodeError) as e:
        print(f"Warning: Could not parse {filepath}: {e}", file=sys.stderr)
        return []

    functions = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append((node.name, node.lineno))
    return functions


def check_file(filepath: Path) -> list[str]:
    """Check a single file. Returns list of violation messages."""
    functions = get_function_defs(filepath)
    if not functions:
        return []

    violations = []
    first_private_line = None
    first_private_name = None

    for name, lineno in functions:
        is_private = name.startswith("_")
        if is_private:
            if first_private_line is None:
                first_private_line = lineno
                first_private_name = name
        else:
            if first_private_line is not None:
                violations.append(
                    f"  Line {lineno}: public function `{name}` "
                    f"after private `{first_private_name}` at line {first_private_line}"
                )

    return violations


def main():
    if len(sys.argv) > 1:
        paths = [Path(p) for p in sys.argv[1:]]
    else:
        # book-of-job's own code, not the working directory and not this repo:
        # public-before-private is that review's house style, and MAM-basics' py/
        # reports 1172 violations against it where these packages report 0.
        paths = boj_paths.code_paths()

    files_to_check = []
    for path in paths:
        if path.is_file() and path.suffix == ".py":
            files_to_check.append(path)
        elif path.is_dir():
            files_to_check.extend(
                f
                for f in path.rglob("*.py")
                if "__pycache__" not in f.parts
                and ".venv" not in f.parts
                and ".novc" not in f.parts
            )

    total_violations = 0
    for filepath in sorted(files_to_check):
        violations = check_file(filepath)
        if violations:
            print(f"{filepath}:")
            for v in violations:
                print(v)
            total_violations += len(violations)

    if total_violations:
        print(f"\nFound {total_violations} violation(s).")
        return 1
    else:
        print("No function ordering violations found.")
        return 0


if __name__ == "__main__":
    sys.exit(main())
