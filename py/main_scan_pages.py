"""Entry point for the scan-pages index. See doc/scan-pages.md.

Subcommands:
    survey
        Walk the five scan folders, classify every file, and write the tracked
        indexes at in/scan-pages/. Refuses, naming names, on any file it cannot
        classify or that OneDrive has left as a cloud-only placeholder.
    check
        Lint the tracked indexes. Needs the landed MAM-parsed product, and fails rather
        than skipping without it; from a worktree, set REPOS_ROOT.

``lookup`` and ``census`` arrive with Phase 1.
"""

import argparse
import sys

from scan_pages import check
from scan_pages import survey


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


def build_parser():
    """Return the argument parser, buildable without running the program."""
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)
    subparsers.add_parser("survey", help="classify the scan folders, write the indexes")
    subparsers.add_parser("check", help="lint the tracked indexes")
    return parser


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    args = build_parser().parse_args()
    {"survey": _run_survey, "check": _run_check}[args.subcommand](args)


if __name__ == "__main__":
    main()
