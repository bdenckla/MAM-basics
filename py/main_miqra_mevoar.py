"""Turn Rabbi David Kokhav's Word files of Miqra Mevoar into Hebrew Wikisource pages.

Avi keeps Rabbi Kokhav's Word files, one book each, in a pCloud folder. This hand-run
converter extracts each verse's heading and paraphrase into the tracked JSON under
in/miqra-mevoar/, checks it against MAM-simple, and writes the base-chapter pages that
`py/main_ws_bot.py miqra-mevoar` creates on Hebrew Wikisource. Neither the Word files
nor the pages are tracked. in/miqra-mevoar/README.md says how to regenerate the JSON,
and doc/PLAN-miqra-mevoar.md is the plan of record. The Torah's base chapters were made
on Wikisource before this converter, from no Word file that it reads, so base-headings
reads the places of their headings from Wikisource instead, for the Torah's display
pages; in/miqra-mevoar-base-headings/README.md says how.

Subcommands:
    fetch
        Download every file of the pCloud folder whose public link --link-file holds
        into a new directory, .novc/miqra-mevoar/pcloud/<timestamp>/, with
        manifest.json. The link is written nowhere.
    extract
        Write in/miqra-mevoar/<stem>.json from every .docx in DIRECTORY, refusing an
        unknown book, row or element, a numbering gap, or a heading or paraphrase with
        a line break or wikitext. A book's JSON holds the whole book, or only the
        chapters that its entry in py/miqra_mevoar/books.py declares, as Isaiah's
        declares 40 to 66.
    check
        Extract the .docx files in DIRECTORY again and require them to equal the
        tracked JSON, their versification to equal MAM-simple's, and each row's Bible
        column to match MAM-simple's verse. DIRECTORY's Word files must be exactly the
        tracked books', or, with --book STEM, repeatable, exactly those books', and the
        report then names the tracked books that the check leaves out. Writes a report
        under .novc/miqra-mevoar/checks/ and nothing tracked; exits non-zero on a
        failure.
    pages
        Write each chapter's page from the tracked JSON into the new directory --out,
        as MediaWiki would store it, with titles.tsv.
    base-headings
        Read the latest revision of every base chapter of the Torah on Hebrew
        Wikisource, anonymously, parse it by a closed parser, and write the verses
        before which it has a heading to in/miqra-mevoar-base-headings/<OSIS>.json.
        With --check, write nothing: list each chapter whose revision changed since
        those records, and exit non-zero if a heading's place differs from them or if
        a page does not parse.

Examples:
    .venv/Scripts/python.exe py/main_miqra_mevoar.py fetch --link-file path/to/link.txt
    .venv/Scripts/python.exe py/main_miqra_mevoar.py extract .novc/miqra-mevoar/pcloud/<timestamp>
    .venv/Scripts/python.exe py/main_miqra_mevoar.py check .novc/miqra-mevoar/pcloud/<timestamp>
    .venv/Scripts/python.exe py/main_miqra_mevoar.py check .novc/miqra-mevoar/pcloud/<timestamp> --book yeshayahu
    .venv/Scripts/python.exe py/main_miqra_mevoar.py pages --out .novc/miqra-mevoar/pages/<timestamp>
    .venv/Scripts/python.exe py/main_miqra_mevoar.py base-headings
    .venv/Scripts/python.exe py/main_miqra_mevoar.py base-headings --check
"""

import argparse
import sys

from miqra_mevoar import base_headings
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
    check_parser.add_argument(
        "--book",
        action="append",
        dest="books",
        metavar="STEM",
        help=(
            "check this book only, repeatable: the directory must hold the Word files"
            " of the books named and no others"
        ),
    )
    pages_parser = subparsers.add_parser(
        "pages", help="write the pages from the tracked JSON"
    )
    pages_parser.add_argument("--out", required=True, help="a directory to create")
    base_headings_parser = subparsers.add_parser(
        "base-headings",
        help="record the places of the headings in the Torah's base chapters",
    )
    base_headings_parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "write nothing; fail if a heading's place differs from the records or a"
            " page does not parse"
        ),
    )
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
        sys.exit(check.run(args.directory, args.books))
    elif args.subcommand == "pages":
        pages.run(args.out)
    elif args.subcommand == "base-headings":
        sys.exit(base_headings.run(check=args.check))
    else:
        raise ValueError(f"unknown subcommand {args.subcommand}")


if __name__ == "__main__":
    main()
