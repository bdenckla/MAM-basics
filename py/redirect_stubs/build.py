"""``build``: write a redirect stub per frozen old URL, plus the ``404.html`` catch-all.

The destination defaults to a gitignored scratch directory, so the safe target is the one
you get by saying nothing and publishing into a source redirect host takes ``--publish``.
``--repo`` selects a frozen-manifest row from ``stubs.py``'s table. What the stubs are,
why they carry the target three times over, and why the URL list is frozen rather than
derived from the live site are all ``stubs.py``'s docstring.
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
            "source redirect host to build; each row is added only when its frozen"
            " manifest has been captured"
        ),
    )
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument(
        "--out",
        type=Path,
        help=(
            "directory to write the stubs into; defaults to the gitignored"
            " .novc/<subtree>-redirect-stubs/ for the selected row"
        ),
    )
    destination.add_argument(
        "--publish",
        action="store_true",
        help=(
            "write into the selected source repo's gh-pages/ instead, which takes a"
            " temporary clone"
        ),
    )


def run(args: argparse.Namespace) -> None:
    repo = stubs.redirect_repo(args.repo)
    out_dir = _destination(args, repo)
    written = stubs.write_stubs(paths.repo_root(), repo, out_dir)
    print(f"Wrote {len(written)} files to {out_dir}")
    print(f"  {len(written) - 1} page stubs and {stubs.NOT_FOUND_NAME}")
    print("Deleted nothing. Run `check` to find a stub whose page has since gone.")


def _destination(args: argparse.Namespace, repo: stubs.RedirectRepo) -> Path:
    if args.publish:
        return stubs.source_pages_dir(repo)
    return args.out if args.out is not None else stubs.default_out_dir(repo)
