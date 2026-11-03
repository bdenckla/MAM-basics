"""Turn Rabbi David Kokhav's Word files of Miqra Mevoar into Hebrew Wikisource pages.

Avi keeps Rabbi Kokhav's Word files, one book each, in a pCloud folder. This hand-run
converter extracts each verse's heading and paraphrase into the tracked JSON under
in/miqra-mevoar/, checks it against MAM-simple, and writes the base-chapter pages that
`py/main_ws_bot.py miqra-mevoar` creates on Hebrew Wikisource. Neither the Word files
nor the pages are tracked. in/miqra-mevoar/README.md says how to regenerate the JSON,
and doc/PLAN-miqra-mevoar.md is the plan of record.

Subcommands:
    fetch
        Download every file of the pCloud folder whose public link --link-file holds
        into a new directory, .novc/miqra-mevoar/pcloud/<timestamp>/, with
        manifest.json. The link is written nowhere.
    extract
        Write in/miqra-mevoar/<stem>.json from every .docx in DIRECTORY, refusing an
        unknown book, row or element, a numbering gap, or a heading or paraphrase with
        a line break or wikitext.
    check
        Extract the .docx files in DIRECTORY again and require them to equal the
        tracked JSON, their versification to equal MAM-simple's, and each row's Bible
        column to match MAM-simple's verse. Writes a report under
        .novc/miqra-mevoar/checks/ and nothing tracked; exits non-zero on a failure.
    pages
        Write each chapter's page from the tracked JSON into the new directory --out,
        as MediaWiki would store it, with titles.tsv.

Examples:
    .venv/Scripts/python.exe py/main_miqra_mevoar.py fetch --link-file path/to/link.txt
    .venv/Scripts/python.exe py/main_miqra_mevoar.py extract .novc/miqra-mevoar/pcloud/<timestamp>
    .venv/Scripts/python.exe py/main_miqra_mevoar.py check .novc/miqra-mevoar/pcloud/<timestamp>
    .venv/Scripts/python.exe py/main_miqra_mevoar.py pages --out .novc/miqra-mevoar/pages/<timestamp>
"""

import argparse
import sys

from miqra_mevoar import check
from miqra_mevoar import extract
from miqra_mevoar import fetch
from miqra_mevoar import pages


def build_parser():
    """Return the argument parser, buildable without running the program."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    fetch_parser = subparsers.add_parser(
        "fetch", help="download the pCloud folder into a new directory"
    )
    fetch_parser.add_argument(
        "--link-file", required=True, help="a file holding the folder's public link"
    )
    extract_parser = subparsers.add_parser(
        "extract", help="write the tracked JSON from the Word files"
    )
    extract_parser.add_argument("directory", help="a directory of Word files")
    check_parser = subparsers.add_parser(
        "check", help="check the Word files against the JSON and MAM-simple"
    )
    check_parser.add_argument("directory", help="a directory of Word files")
    pages_parser = subparsers.add_parser(
        "pages", help="write the pages from the tracked JSON"
    )
    pages_parser.add_argument("--out", required=True, help="a directory to create")
    return parser


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = build_parser().parse_args()
    if args.subcommand == "fetch":
        fetch.run(args.link_file)
    elif args.subcommand == "extract":
        extract.run(args.directory)
    elif args.subcommand == "check":
        sys.exit(check.run(args.directory))
    elif args.subcommand == "pages":
        pages.run(args.out)
    else:
        raise ValueError(f"unknown subcommand {args.subcommand}")


if __name__ == "__main__":
    main()
