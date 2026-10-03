"""Render and validate selected Yeivin excerpts and survey Ben's meteg claims.

Subcommands:
    render
        Render from the tracked approved claim data, without private inputs.
    survey-meteg-claims
        Project the independent public meteg analysis into the minimized claims.
    check
        Check the claims, pages, and assets without writing.
    review-claims
        Report the claim population, pins, and page lines that the current
        analysis would change, without writing.
"""

import argparse
import sys


def build_parser():
    """Describe the closed command set without running an operation."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("render", help="Render from the tracked approved claims")
    commands.add_parser(
        "survey-meteg-claims", help="Project the independent public meteg analysis"
    )
    commands.add_parser("check", help="Check data and outputs without writing")
    commands.add_parser(
        "review-claims", help="Report what a changed analysis would change"
    )
    return parser


def almost_main(argv=None):
    """Dispatch exactly one public-only operation."""
    args = build_parser().parse_args(argv)
    if args.command == "survey-meteg-claims":
        from yeivin_itm.claims import survey

        return survey()
    if args.command == "render":
        from yeivin_itm.publication import render

        return render()
    if args.command == "check":
        from yeivin_itm.publication import check

        return check()
    if args.command == "review-claims":
        from yeivin_itm.publication import review_claims

        return review_claims()
    raise ValueError("Unknown Yeivin operation")


def main():
    """Use UTF-8 for both Windows and POSIX pipes."""
    # The check operation is write-neutral, including Python import caches. Set
    # here, before almost_main imports anything, rather than at import, so that an
    # importer such as py/main_0_mega.py keeps its own bytecode caching.
    sys.dont_write_bytecode = True
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    return almost_main()


if __name__ == "__main__":
    main()
