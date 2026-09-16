"""Run this repo's test suite.

Examples:
    .venv/Scripts/python.exe py/main_test.py
    .venv/Scripts/python.exe py/main_test.py -k printed_decalogue -x
    .venv/Scripts/python.exe py/main_test.py py/tests/test_transliterations.py -q

With no arguments this runs everything under ``py/tests``.  Whatever arguments are
given go straight through to pytest, so its own options (``-k``, ``-x``, ``-q``,
``--lf``, ``--collect-only``, ...) work unchanged; naming a file or directory
replaces the default target rather than adding to it.  Use the venv's own
interpreter -- the system Python has neither pytest nor PLY.

WHY THIS FILE EXISTS, AND WHY A BARE ``pytest`` FAILS TO COLLECT

``.venv/Scripts/pytest.exe py/tests`` does not collect: every test imports
``mb_cmn.*``, ``accgram.*``, ``uxlc_paths`` or the like, and collection dies on the
first of them with ``ModuleNotFoundError``.  That is the designed state, not a defect
to repair.  Import path here is decided by how a program is entered: CPython puts a
script's own directory at ``sys.path[0]``, so running ``py/main_<x>.py`` -- this file
included -- puts ``py/`` on the path, and the in-process ``pytest.main()`` call below
inherits it.  Nothing is added by hand anywhere.

So do not "fix" that collection failure by reintroducing a path shim.  A root
``conftest.py``, a ``pythonpath`` setting in ``pytest.ini``, a ``.pth`` file, an
exported ``PYTHONPATH``, a ``sitecustomize.py`` -- all the same mistake in different
spellings, and the count of them in this repo is zero, not one.  Run the tests through
this entry point instead.

WHY THE ``TEST_MODULE_SPECS`` REGISTRY IS GONE

Until 2026-08-01 this file was a hand-maintained tuple of module names plus a
``unittest`` loader.  A registry has a failure mode pytest does not: an unlisted test
file does not skip, it reports nothing at all.  Two files went unrun that way here from
the 2026-05-03 migration until 2026-07-30, one of them edited four times meanwhile.
pytest discovers files itself, so there is no registry to fall out of sync.

The flip also let wlc-utils' ~299 module-level ``def test_`` functions arrive without
being rewritten: pytest collects both those and this repo's ``unittest.TestCase``
classes natively, so zero test files changed on either side.  What the cross-repo
standard actually forbids is path configuration, which this file has none of either
way.

WHY WINDOWS TEST TEMP FILES ARE WORKTREE-LOCAL

A Codex elevated Windows sandbox can run commands under a dedicated Windows account
while preserving another account's ``TEMP``, ``TMP``, and ``USERNAME``.  Python 3.13
gives directories created with mode ``0o700`` a private Windows ACL, while pytest
names its shared temporary root from ``USERNAME``.  A root created by one identity
can therefore block the next identity before a test using ``tmp_path`` even starts.

On Windows this entry point redirects ``TEMP`` and ``TMP`` to the gitignored
``.novc/pytest-temp-root`` in the current checkout before importing pytest.  Pytest
still creates its normal numbered run directories below that writable parent, so
simultaneous runs do not share a fixed ``--basetemp`` that either run could clear.
Other operating systems retain their normal temporary-directory behavior.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from mb_cmn import paths


def _configure_windows_temp_root() -> None:
    """Give Windows test processes a disposable temp parent in this checkout."""
    if sys.platform != "win32":
        return

    temp_root = paths.repo_root() / ".novc" / "pytest-temp-root"
    temp_root.mkdir(parents=True, exist_ok=True)
    temp_root_text = str(temp_root)
    os.environ["TEMP"] = temp_root_text
    os.environ["TMP"] = temp_root_text


def _default_target() -> str:
    """The whole suite, absolute, so the command does not depend on the cwd."""
    return str(paths.repo_root() / "py" / "tests")


def main(argv: list[str] | None = None) -> int:
    """Run pytest over ``argv`` (default ``sys.argv[1:]``) and return its exit code."""
    _configure_windows_temp_root()

    # Import after redirecting TEMP and TMP so Python and pytest cannot cache the
    # inherited user temp directory first.
    import pytest

    args = list(sys.argv[1:] if argv is None else argv)
    # Supply the default target only when nothing given already names one.  An option's
    # value -- the expression after -k, say -- is not an existing path, so `-k <expr>`
    # still selects from the whole suite rather than from nothing.
    if not any(Path(arg).exists() for arg in args):
        args.append(_default_target())
    return int(pytest.main(args))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    sys.exit(main())
