"""``check``: lint a stub tree against the site it stands in for.

Both sides are derived -- the page set from ``git ls-files gh-pages/wlc``, each stub's
expected target from the stub's own path -- so this never needs editing when a page is
added, renamed or dropped.  It is the second of the two test shapes ``CLAUDE.md``
sanctions, a mechanical lint over generated text, and it is deliberately not a pytest
module: until Phase 9 lands there is no committed stub tree for it to run against, and a
test that built one to a temp directory first would be checking the generator against
itself.

The default target is wlc-utils' committed ``gh-pages/``, which is what Phase 9's
verification runs.  Before that flip those 154 files are still the real pages, so at Phase
8 point ``--dir`` at the scratch tree ``build`` just wrote.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from mb_cmn import paths
from wlc_redirect import stubs


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    # repo_root is unused: the page list is read at run time from paths.repo_root().  The
    # parameter is here so the entry point wires both subcommands the same way.
    del repo_root
    parser.add_argument(
        "--dir",
        dest="stub_dir",
        type=Path,
        help=(
            "the tree of stubs to check; defaults to wlc-utils' own gh-pages/, which"
            " holds the real pages until Phase 9 flips them"
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
    pages = stubs.page_paths(paths.repo_root())
    print(f"{stub_dir}: {len(pages)} stubs and {stubs.NOT_FOUND_NAME}, all correct")
    return 0
