"""Entry point for the scan-pages index. See doc/scan-pages.md.

Subcommands:
    survey
        Walk the five scan folders, classify every file, and write the tracked
        indexes at in/scan-pages/. Refuses, naming names, on any file it cannot
        classify or that OneDrive has left as a cloud-only placeholder.
    check
        Lint the tracked indexes. Needs the landed MAM-parsed product, and fails rather
        than skipping without it.

    lookup
        lookup <book> <chapter>:<verse>[t|e] [phrase] prints exact local scan
        links. Refuse each uncensused edition or strand.
    census
        census <edition> <book> <edge-json> adopts a whole book's observed
        edges after phrase and contiguity checks.
"""

import argparse
import sys
import json
import re

from scan_pages import check
from scan_pages import survey
from scan_pages import census
from scan_pages import editions
from scan_pages import index_io
from scan_pages import lookup
from mb_cmn import bib_locales


def _run_survey(_args):
    reports = survey.survey_all()
    for report in reports:
        kinds = ", ".join(f"{k}={v}" for k, v in sorted(report["kinds"].items()))
        print(f"{report['edition']}: {report['files']} files; {kinds}")
        print(
            f"  books with body pages: {len(report['body_pages_per_book'])};"
            f" seeded recs: {report['recs']} on {report['rec_pages']} pages"
        )
        for anomaly in report["anomalies"]:
            print(f"  anomaly: {anomaly}")
    total = sum(report["files"] for report in reports)
    print(f"Wrote {len(reports)} indexes covering {total} files.")


def _run_check(_args):
    counts = check.check_all()
    print(
        f"check: {counts['editions']} editions, {counts['pages']} pages re-classified,"
        f" {counts['recs']} recs, {counts['segments']} segments. No problems."
    )


def _run_lookup(args):
    match = re.fullmatch(r"([1-9][0-9]*):([1-9][0-9]*)([te]?)", args.cv)
    if match is None:
        raise ValueError("Expected chapter:verse with optional t/e strand suffix")
    c, v, suffix = match.groups()
    found = False
    for edition in args.edition or editions.ALL_EDITION_IDS:
        try:
            recs = lookup.resolve(
                index_io.read_index(edition),
                args.book,
                int(c),
                int(v),
                args.phrase,
                suffix or None,
            )
        except lookup.UncensusedError as error:
            print(error, file=sys.stderr)
            continue
        for rec in recs:
            print((editions.edition_dir(edition) / rec["page"]).as_uri())
            found = True
    return 0 if found else 1


def _run_census(args):
    with open(args.edges, encoding="utf-8") as source:
        edges = json.load(source)
    count = census.run(args.edition, args.book, edges)
    print(f"{args.edition}: adopted {count} exact page records for {args.book}")


def build_parser():
    """Return the argument parser, buildable without running the program."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    subparsers.add_parser("survey", help="classify the scan folders, write the indexes")
    subparsers.add_parser("check", help="lint the tracked indexes")
    lookup_parser = subparsers.add_parser(
        "lookup", help="print exact scan links for censused ranges"
    )
    lookup_parser.add_argument("book", choices=bib_locales.ALL_BK39_IDS)
    lookup_parser.add_argument("cv")
    lookup_parser.add_argument("phrase", nargs="?")
    lookup_parser.add_argument(
        "--edition", action="append", choices=editions.ALL_EDITION_IDS
    )
    census_parser = subparsers.add_parser(
        "census", help="adopt a complete book's observed page edges"
    )
    census_parser.add_argument("edition", choices=editions.ALL_EDITION_IDS)
    census_parser.add_argument("book", choices=bib_locales.ALL_BK39_IDS)
    census_parser.add_argument("edges")
    return parser


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="backslashreplace")
    args = build_parser().parse_args()
    return {
        "survey": _run_survey,
        "check": _run_check,
        "lookup": _run_lookup,
        "census": _run_census,
    }[args.subcommand](args)


if __name__ == "__main__":
    sys.exit(main())
