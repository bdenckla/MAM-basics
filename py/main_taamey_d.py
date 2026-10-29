"""Taamey D's documentation pages and shaping checks, in the py/taamey_d/ packages.

Subcommands:
    doc
        Write Taamey_D.html and Xolam_xaser_for_alef.html under gh-pages/taamey-d/,
        refusing if a comparison cell no longer matches its frozen image's record.
    qa
        Run the anchor-family lint and the four shaping checks of py/taamey_d/qa/ on
        the tracked Taamey-D/font-m-TaD/Taamey_D.ttf and the corpus in
        Taamey-D/qa-in/, printing every result and rewriting the tracked reports in
        Taamey-D/qa-out/Taamey_D/.  --one-check {mrun,plac,regr,coll} runs one shaping
        check alone.  A SKIP, an unknown status or an anchor-family FAIL raises; a
        shaping check's FAIL does not, since its report is a tracked file.
"""

import argparse
import sys


def build_parser():
    """Describe the closed command set without running an operation."""
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doc", help="Write Taamey D's documentation pages")
    qa = commands.add_parser(
        "qa", help="Run Taamey D's shaping checks and rewrite their reports"
    )
    qa.add_argument(
        "--one-check",
        choices=("mrun", "plac", "regr", "coll"),
        help="run only the shaping check with this short name",
    )
    return parser


def almost_main(argv=None):
    """Dispatch one explicit operation, importing only what that operation needs."""
    args = build_parser().parse_args(argv)
    if args.command == "doc":
        from taamey_d.doc.gen_doc import write_pages

        return write_pages()
    if args.command == "qa":
        from taamey_d.qa.run_checks import run_checks

        return run_checks(args.one_check)
    raise ValueError("unknown Taamey D operation")


def main():
    """Use UTF-8 for both Windows and POSIX pipes."""
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    return almost_main()


if __name__ == "__main__":
    main()
