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
        links. The Simanim Tiqqun accepts --rite for an approved reading.
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


def _run_survey(args):
    reports = (
        survey.survey_editions(args.edition) if args.edition else survey.survey_all()
    )
    for report in reports:
        kinds = ", ".join(f"{k}={v}" for k, v in sorted(report["kinds"].items()))
        print(f"{report['edition']}: {report['files']} files; {kinds}")
        print(
            f"  books with body pages: {len(report['body_pages_per_book'])};"
            f" records: {report['recs']} on {report['rec_pages']} pages"
        )
        for anomaly in report["anomalies"]:
            print(f"  anomaly: {anomaly}")
    total = sum(report["files"] for report in reports)
    print(f"Wrote {len(reports)} indexes covering {total} files.")


def _run_check(_args):
    density_warnings = []
    counts = check.check_all(density_warnings=density_warnings)
    for warning in density_warnings:
        print(f"  density advisory: {warning}")
    print(
        f"check: {counts['editions']} editions, {counts['pages']} pages re-classified,"
        f" {counts['recs']} recs, {counts['segments']} segments. No problems."
    )


def _run_lookup(args):
    match = re.fullmatch(r"([1-9][0-9]*):([1-9][0-9]*)([te]?)", args.cv)
    if match is None:
        raise ValueError("Expected chapter:verse with optional t/e strand suffix")
    c, v, suffix = match.groups()
    if args.printed_form and (not args.phrase or suffix or args.rite):
        raise ValueError(
            "Printed-form lookup requires a phrase without a strand or rite"
        )
    selected = args.edition or editions.ALL_EDITION_IDS
    if args.rite:
        if args.edition and set(args.edition) != {editions.SIMANIM_TIQQUN}:
            raise ValueError("Rite lookup is available only for the Simanim Tiqqun")
        selected = (editions.SIMANIM_TIQQUN,)
    found = False
    for edition in selected:
        try:
            index = index_io.read_index(edition)
            reference = (args.book, int(c), int(v), args.phrase)
            if args.printed_form:
                recs = lookup.resolve_printed_forms(index, *reference)
            else:
                recs = lookup.resolve(index, *reference, suffix or None, rite=args.rite)
        except lookup.UncensusedError as error:
            print(error, file=sys.stderr)
            continue
        for page in dict.fromkeys(rec["page"] for rec in recs):
            print((editions.edition_dir(edition) / page).as_uri())
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
    survey_parser = subparsers.add_parser(
        "survey", help="classify scan folders and refresh their indexes"
    )
    survey_parser.add_argument(
        "--edition", action="append", choices=editions.ALL_EDITION_IDS
    )
    subparsers.add_parser("check", help="lint the tracked indexes")
    lookup_parser = subparsers.add_parser(
        "lookup", help="print exact scan links for censused ranges"
    )
    lookup_parser.add_argument("book", choices=bib_locales.ALL_BK39_IDS)
    lookup_parser.add_argument("cv")
    lookup_parser.add_argument("phrase", nargs="?")
    lookup_parser.add_argument("--rite", help="approved Simanim Tiqqun reading ID")
    lookup_parser.add_argument(
        "--printed-form", action="store_true", help="match a recorded edition spelling"
    )
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
