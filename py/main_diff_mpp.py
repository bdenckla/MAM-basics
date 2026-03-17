"""
Compare two git revisions of MAM-parsed plus/ JSON and generate an HTML
diff report with category filtering.

Usage:
    .venv/Scripts/python.exe py/main_diff_mpp.py --old <rev> --new <rev>
    .venv/Scripts/python.exe py/main_diff_mpp.py --all

The revisions are git refs in the ../MAM-parsed repo (commits, tags, branches).
Output goes to ../MAM-with-doc/docs/change-log/ by default.  If the hash range
matches an entry in releases.json, the release name is used as the filename;
otherwise the sanitised hash range is used.

The --all flag generates reports for every named release in releases.json
and regenerates index.html.
"""

import argparse
import json
import os
import subprocess
from pydiff_mpp import mpp_extract, mpp_classify, mpp_html, mpp_index

MAM_PARSED_DIR = "../MAM-parsed"
CHANGE_LOG_DIR = "../MAM-with-doc/docs/change-log"
RELEASES_JSON = f"{CHANGE_LOG_DIR}/releases.json"


def _commit_date(rev):
    """Return the commit date (YYYY-MM-DD) for a revision in MAM-parsed."""
    result = subprocess.run(
        ["git", "-C", MAM_PARSED_DIR, "log", "-1", "--format=%cs", rev],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def _sanitize_rev(rev):
    """Make a revision string safe for use in a filename."""
    return (
        rev.replace("/", "_")
        .replace("\\", "_")
        .replace("..", "_")
        .replace("^", "-")[:20]
    )


def _lookup_release_name(old_rev, new_rev):
    """Return the release name if this hash range is in releases.json, else None."""
    if not os.path.isfile(RELEASES_JSON):
        return None
    with open(RELEASES_JSON, "r", encoding="utf-8") as f:
        releases = json.load(f)
    for entry in releases["releases"]:
        if entry["old"] == old_rev and entry["new"] == new_rev:
            return entry["name"]
    return None


def _default_output_path(old_rev, new_rev):
    """Build the default output path inside the change-log directory."""
    name = _lookup_release_name(old_rev, new_rev)
    if name is not None:
        slug = name
    else:
        slug = f"{_sanitize_rev(old_rev)}_{_sanitize_rev(new_rev)}"
    return f"{CHANGE_LOG_DIR}/{slug}.html"


def _generate_report(old_rev, new_rev, output):
    """Generate one diff report. Returns the expanded diff count."""
    print(f"Comparing {old_rev} -> {new_rev} ...")
    diffs = mpp_extract.diff_all_books(old_rev, new_rev)
    print(f"  {len(diffs)} raw changes found")
    mpp_classify.classify_diffs(diffs)
    old_date = _commit_date(old_rev)
    new_date = _commit_date(new_rev)
    os.makedirs(os.path.dirname(output), exist_ok=True)
    total = mpp_html.write_report(diffs, old_rev, new_rev, output, old_date, new_date)
    print(f"  Report written to {output}")
    return total


def _run_all():
    """Generate reports for all named releases and write index.html."""
    with open(RELEASES_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    release_info = []
    for entry in data["releases"]:
        output = f"{CHANGE_LOG_DIR}/{entry['name']}.html"
        count = _generate_report(entry["old"], entry["new"], output)
        release_info.append({"name": entry["name"], "count": count})
    mpp_index.write_index(release_info, CHANGE_LOG_DIR)


def main():
    parser = argparse.ArgumentParser(
        description="Compare two revisions of MAM-parsed plus/ and generate an HTML report."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Generate all named releases from releases.json and regenerate index.html",
    )
    parser.add_argument("--old", help="Old git revision (in ../MAM-parsed repo)")
    parser.add_argument("--new", help="New git revision (in ../MAM-parsed repo)")
    parser.add_argument(
        "--output",
        default=None,
        help="Output HTML path (default: auto from releases.json or hash range)",
    )
    args = parser.parse_args()

    if args.all:
        if args.old or args.new or args.output:
            parser.error("--all cannot be combined with --old, --new, or --output")
        _run_all()
    else:
        if not args.old or not args.new:
            parser.error("--old and --new are required unless --all is given")
        output = args.output or _default_output_path(args.old, args.new)
        _generate_report(args.old, args.new, output)


if __name__ == "__main__":
    main()
