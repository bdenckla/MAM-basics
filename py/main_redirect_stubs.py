"""Redirect stubs standing in for published pages that now live in MAM-basics.

``bdenckla.github.io/wlc-utils/<path>`` moved to
``bdenckla.github.io/MAM-basics/wlc/<path>``, a pure prefix rewrite.  Some of the old URLs
are cited from places Ben cannot edit -- five citations in the tanach.us change list
vendored into UXLC-utils above all -- so wlc-utils stays alive as a redirect host rather
than being archived or deleted, holding one stub per published page plus a ``404.html``
catch-all.  This program builds that set and lints it.

``py/redirect_stubs/stubs.py`` records one row per redirect host: its source repository,
MAM-basics subtree, old URL prefix, frozen manifest and clone URL.  The table has only the
wlc-utils row today.  A later lane adds a row only with that source repo's frozen manifest,
so a missing manifest fails rather than producing an empty stub set.

WITH JAVASCRIPT OFF, A DEEP LINK LOSES ITS FRAGMENT.  Each stub carries its target three
times and the three do different work: the canonical link names the current copy for a
search engine, the meta refresh is the no-JavaScript path and takes a fixed URL, and only
the script can re-append ``location.search`` and ``location.hash`` -- a fragment such as
``#supplied-dt5v6-bet-atnax`` never reaches the server and is arbitrary besides.  So
UXLC-utils' four published deep links land on the right page at its top, rather than at
the anchor, for a reader who has disabled JavaScript.  ``py/redirect_stubs/stubs.py``'s
docstring states this and the rest of the design in full.

Subcommands:
    build
                Write a stub per frozen old URL plus the 404.html catch-all. ``--repo``
                selects a table row; --out names the destination and defaults to a
                gitignored subtree-specific directory, so the safe target is the one
                received by saying nothing. --publish writes into that source repo's
                gh-pages/ instead. It deletes nothing.
    check
                Lint a selected row's stub tree against its frozen URLs: every URL has a
                stub, every stub answers one, every URL is still published under its
                MAM-basics subtree, 404.html is present, and each stub names its own
                path's prefix rewrite and no other target. --dir names the tree; its
                default, the selected source repo's gh-pages/, takes a clone. Exits
                non-zero on any problem.

Examples:
    .venv/Scripts/python.exe py/main_redirect_stubs.py build --out .novc/stubs
    .venv/Scripts/python.exe py/main_redirect_stubs.py check --dir .novc/stubs
    .venv/Scripts/python.exe py/main_redirect_stubs.py check
"""

from __future__ import annotations

import argparse
from pathlib import Path

from wlc_cmn.utf8_io import force_utf8_io
from redirect_stubs import build as build_stubs
from redirect_stubs import check as check_stubs

from mb_cmn import paths


def _repo_root() -> Path:
    return paths.repo_root()


def _run_build(args: argparse.Namespace) -> None:
    build_stubs.run(args)


def _run_check(args: argparse.Namespace) -> int:
    # The one subcommand with an exit code to return: check is a gate.
    return check_stubs.run(args)


def build_parser() -> argparse.ArgumentParser:
    """The fully-configured parser, so a test can read the subcommands off it."""
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="subcommand", metavar="SUBCOMMAND")
    subparsers.required = True

    # Named build_subparser, not build_parser: this function is build_parser().
    build_subparser = subparsers.add_parser(
        "build",
        help=(
            "Write a selected redirect host's frozen stubs plus 404.html. --out names the "
            "destination; --publish writes into the selected source repo's gh-pages/. "
            "Deletes nothing."
        ),
    )
    build_stubs.add_args(build_subparser, repo_root=_repo_root())
    build_subparser.set_defaults(func=_run_build)

    check_parser = subparsers.add_parser(
        "check",
        help=(
            "Lint a selected redirect host's stubs: the two sets correspond and each "
            "stub names its own path's prefix rewrite. --dir defaults to the source "
            "repo's gh-pages/. Exits non-zero on any problem."
        ),
    )
    check_stubs.add_args(check_parser, repo_root=_repo_root())
    check_parser.set_defaults(func=_run_check)

    return parser


def main() -> None:
    args = build_parser().parse_args()
    # `or 0` because build returns None on success; check's non-zero has to reach the
    # shell, it being a gate.
    raise SystemExit(args.func(args) or 0)


if __name__ == "__main__":
    force_utf8_io()
    main()
