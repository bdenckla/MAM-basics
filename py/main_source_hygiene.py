"""Exports main: the source-hygiene CLI the pre-commit hook runs (issues #22, #26).

Usage (run from the repo root, like the other py/main_*.py drivers):

    python py/main_source_hygiene.py

Scans hand-authored ``py/`` + ``tools/`` + ``doc/`` for orphan combining marks and
for decomposed base+mark pairs that have a precomposed NFC form, prints each
offender as ``path:line  U+XXXX NAME -- detail``, and exits non-zero when the tree
is dirty. The scanner itself lives in ``py/repo_hygiene/source_hygiene.py``; its
synthetic-control tests run under ``python py/main_test.py --source-hygiene``.
"""

import os
import sys

import repo_hygiene.source_hygiene as sh

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    """Scan the hand-authored source tree; exit non-zero on any offense."""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(sh.run(_REPO_ROOT))


if __name__ == "__main__":
    main()
