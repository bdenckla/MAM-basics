"""``check``: lint a stub tree against the site it stands in for.

The old URLs come from ``in/wlc_redirect_pages.json`` and each stub's expected target
from the stub's own path, so this needs editing only when the frozen set shrinks.  It is
the second of the two test shapes ``CLAUDE.md`` sanctions, a mechanical lint over
generated text, and it is deliberately not a pytest module: the tree it lints is another
repository's, and a test that built one to a temp directory first would be checking the
generator against itself.  The one direction that needs no stub tree -- a frozen URL whose
page is no longer published here -- is ``py/tests/test_wlc_redirect_manifest.py``, which
is the only part of this lint that still runs with no wlc-utils clone on the disk.

The default target is wlc-utils' committed ``gh-pages/``, so with no clone on the disk
(Ben's decision, 2026-08-22) this subcommand needs either ``--dir`` or a fresh clone;
``stubs.wlc_utils_pages_dir`` says how to get one.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from mb_cmn import paths
from wlc_redirect import stubs


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    # repo_root is unused: the frozen URL list is read at run time from the manifest under
    # paths.repo_root().  The parameter is here so the entry point wires both subcommands
    # the same way.
    del repo_root
    parser.add_argument(
        "--dir",
        dest="stub_dir",
        type=Path,
        help=(
            "the tree of stubs to check; defaults to wlc-utils' own gh-pages/, which"
            " takes a clone of that repo, there being none on the disk"
        ),
    )


def run(args: argparse.Namespace) -> int:
    stub_dir = (
        args.stub_dir if args.stub_dir is not None else stubs.wlc_utils_pages_dir()
    )
    problems = stubs.check_problems(paths.repo_root(), stub_dir)
    if problems:
        print(f"{len(problems)} problems checking the stubs in {stub_dir}:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    pages = stubs.redirected_pages(paths.repo_root())
    print(f"{stub_dir}: {len(pages)} stubs and {stubs.NOT_FOUND_NAME}, all correct")
    return 0
