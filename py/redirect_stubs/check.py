"""``check``: lint a stub tree against the site it stands in for.

The selected table row supplies the frozen manifest, source repository and MAM-basics
subtree. Each stub's expected target is a prefix rewrite of its own path, so this needs
editing only when the frozen set shrinks. It is the second of the two test shapes
``CLAUDE.md`` sanctions, a mechanical lint over generated text, and it is deliberately
not a pytest module: the tree it lints is another repository's, and a test that built one
to a temp directory first would be checking the generator against itself. The one
direction that needs no stub tree -- a frozen URL whose page is no longer published here
-- is ``py/tests/test_redirect_manifest.py``, which is the only part of this lint that
still runs with no source clone on the disk.

The default target is the selected source repo's committed ``gh-pages/``, so with no clone
on the disk this subcommand needs either ``--dir`` or a fresh clone;
``stubs.source_pages_dir`` says how to get one.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from mb_cmn import paths
from redirect_stubs import stubs


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    # repo_root is unused: the frozen URL list is read at run time from the manifest under
    # paths.repo_root(). The parameter is here so the entry point wires both subcommands
    # the same way.
    del repo_root
    parser.add_argument(
        "--repo",
        choices=stubs.redirect_repo_names(),
        default=stubs.default_redirect_repo().source_repo,
        help=(
            "source redirect host to check; each row is added only when its frozen"
            " manifest has been captured"
        ),
    )
    parser.add_argument(
        "--dir",
        dest="stub_dir",
        type=Path,
        help=(
            "the tree of stubs to check; defaults to the selected source repo's"
            " gh-pages/, which takes a temporary clone"
        ),
    )


def run(args: argparse.Namespace) -> int:
    repo = stubs.redirect_repo(args.repo)
    stub_dir = (
        args.stub_dir if args.stub_dir is not None else stubs.source_pages_dir(repo)
    )
    problems = stubs.check_problems(paths.repo_root(), repo, stub_dir)
    if problems:
        print(f"{len(problems)} problems checking the stubs in {stub_dir}:")
        for problem in problems:
            print(f"  {problem}")
        return 1
    pages = stubs.redirected_pages(paths.repo_root(), repo)
    print(f"{stub_dir}: {len(pages)} stubs and {stubs.NOT_FOUND_NAME}, all correct")
    return 0
