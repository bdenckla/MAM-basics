"""``build``: write a redirect stub per published page, plus the ``404.html`` catch-all.

The destination defaults to a gitignored scratch directory, so the safe target is the one
you get by saying nothing and publishing into wlc-utils takes ``--publish``.  What the
stubs are and why they carry the target three times over is ``stubs.py``'s docstring.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from mb_cmn import paths
from wlc_redirect import stubs


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    # repo_root is unused: the page list is read at run time from paths.repo_root(), which
    # is where the published pages are.  The parameter is here so the entry point wires
    # both subcommands the same way.
    del repo_root
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument(
        "--out",
        type=Path,
        help=(
            "directory to write the stubs into; defaults to the gitignored"
            " .novc/wlc-redirect-stubs/"
        ),
    )
    destination.add_argument(
        "--publish",
        action="store_true",
        help=(
            "write into wlc-utils' own gh-pages/ instead, which is what Phase 9 of"
            " doc/PLAN-evacuate-the-rest-of-wlc-utils.md commits"
        ),
    )


def run(args: argparse.Namespace) -> None:
    out_dir = _destination(args)
    written = stubs.write_stubs(paths.repo_root(), out_dir)
    print(f"Wrote {len(written)} files to {out_dir}")
    print(f"  {len(written) - 1} page stubs and {stubs.NOT_FOUND_NAME}")
    print("Deleted nothing. Run `check` to find a stub whose page has since gone.")


def _destination(args: argparse.Namespace) -> Path:
    if args.publish:
        return stubs.wlc_utils_pages_dir()
    return args.out if args.out is not None else stubs.default_out_dir()
