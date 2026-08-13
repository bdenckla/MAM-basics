"""Redirect stubs standing in for wlc-utils' published pages, which now live here.

``bdenckla.github.io/wlc-utils/<path>`` moved to
``bdenckla.github.io/MAM-basics/wlc/<path>``, a pure prefix rewrite.  Some of the old URLs
are cited from places Ben cannot edit -- five citations in the tanach.us change list
vendored into UXLC-utils above all -- so wlc-utils stays alive as a redirect host rather
than being archived or deleted, holding one stub per published page plus a ``404.html``
catch-all.  This program builds that set and lints it.

The stub set is derived from the site rather than from a list: ``git ls-files
gh-pages/wlc`` filtered to ``*.html``, whose path below that prefix is at once the old
wlc-utils path and the new MAM-basics suffix.  So the stubs cannot drift from what is
published, and neither subcommand has a hand-maintained side.

WITH JAVASCRIPT OFF, A DEEP LINK LOSES ITS FRAGMENT.  Each stub carries its target three
times and the three do different work: the canonical link names the current copy for a
search engine, the meta refresh is the no-JavaScript path and takes a fixed URL, and only
the script can re-append ``location.search`` and ``location.hash`` -- a fragment such as
``#supplied-dt5v6-bet-atnax`` never reaches the server and is arbitrary besides.  So
UXLC-utils' four published deep links land on the right page at its top, rather than at
the anchor, for a reader who has disabled JavaScript.  ``py/wlc_redirect/stubs.py``'s
docstring states this and the rest of the design in full.

Subcommands:
    build
                Write a stub per published page plus the 404.html catch-all.  --out
                names the destination and defaults to the gitignored
                .novc/wlc-redirect-stubs/, so the safe target is the one you get by
                saying nothing; --publish writes into wlc-utils' own gh-pages/ instead,
                which is what Phase 9 of doc/PLAN-evacuate-the-rest-of-wlc-utils.md
                commits.  It deletes nothing, wlc-utils' non-HTML assets being a git rm
                that phase does by hand.
    check
                Lint a stub tree against the site it stands in for: every published page
                has a stub, every stub has a published page, 404.html is present, and
                each stub names its own path's prefix rewrite and no other target.
                --dir defaults to wlc-utils' gh-pages/, which is what Phase 9 verifies
                against; before that flip those files are still the real pages, so point
                it at the tree build just wrote.  Exits non-zero on any problem.

Examples:
    .venv/Scripts/python.exe py/main_wlc_redirect_stubs.py build --out .novc/stubs
    .venv/Scripts/python.exe py/main_wlc_redirect_stubs.py check --dir .novc/stubs
    .venv/Scripts/python.exe py/main_wlc_redirect_stubs.py check
"""

from __future__ import annotations

import argparse
from pathlib import Path

from wlc_cmn.utf8_io import force_utf8_io
from wlc_redirect import build as build_stubs
from wlc_redirect import check as check_stubs

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
            "Write a stub per published page plus 404.html. --out names the destination "
            "and defaults to the gitignored .novc/wlc-redirect-stubs/; --publish writes "
            "into wlc-utils' own gh-pages/ instead. Deletes nothing."
        ),
    )
    build_stubs.add_args(build_subparser, repo_root=_repo_root())
    build_subparser.set_defaults(func=_run_build)

    check_parser = subparsers.add_parser(
        "check",
        help=(
            "Lint a stub tree against the site it stands in for: the two sets "
            "correspond and each stub names its own path's prefix rewrite. --dir "
            "defaults to wlc-utils' gh-pages/. Exits non-zero on any problem."
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
