"""
Compare two git revisions of MAM-parsed plus/ JSON and generate an HTML
diff report with category filtering.

Usage:
    .venv/Scripts/python.exe py/main_diff_mpp.py
    .venv/Scripts/python.exe py/main_diff_mpp.py --old <rev> --new <rev>
    .venv/Scripts/python.exe py/main_diff_mpp.py --all

The revisions are git refs in the ../MAM-parsed repo (commits, tags, branches).
Output goes to ../MAM-with-doc/docs/change-log/ by default.  If the hash range
matches an entry in releases.json, the release name is used as the filename;
otherwise the sanitised hash range is used.

The --all flag generates reports for every named release in releases.json
and regenerates index.html, including unnamed-latest when unreleased diffs exist.

When run with no arguments, the script compares the latest named release
(the release boundary closest to HEAD) against HEAD. If commits exist beyond
that release and produce diffs, it writes
../MAM-with-doc/docs/change-log/unnamed-latest.html.
"""

import argparse
import json
import os
import subprocess
from pydiff_mpp import mpp_extract, mpp_classify, mpp_html, mpp_json, mpp_index

MAM_PARSED_DIR = "../MAM-parsed"
CHANGE_LOG_DIR = "../MAM-with-doc/docs/change-log"
RELEASES_JSON = f"{CHANGE_LOG_DIR}/releases.json"
UNNAMED_LATEST_HTML = f"{CHANGE_LOG_DIR}/unnamed-latest.html"


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


def _latest_release_entry():
    """Return the release entry whose `new` boundary is closest to HEAD."""
    with open(RELEASES_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    best_entry = None
    best_distance = None
    for entry in data["releases"]:
        distance = _count_newer_commits(entry["new"])
        if best_distance is None or distance < best_distance:
            best_distance = distance
            best_entry = entry
    return best_entry


def _count_newer_commits(base_rev):
    """Return how many commits exist in MAM-parsed between base_rev and HEAD."""
    result = subprocess.run(
        ["git", "-C", MAM_PARSED_DIR, "rev-list", "--count", f"{base_rev}..HEAD"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
    )
    return int(result.stdout.strip())


def _default_output_path(old_rev, new_rev):
    """Build the default output path inside the change-log directory."""
    name = _lookup_release_name(old_rev, new_rev)
    if name is not None:
        slug = name
    else:
        slug = f"{_sanitize_rev(old_rev)}_{_sanitize_rev(new_rev)}"
    return f"{CHANGE_LOG_DIR}/{slug}.html"


def _generate_report(old_rev, new_rev, output, *, write_when_empty=True):
    """Generate one diff report. Returns the expanded diff count."""
    print(f"Comparing {old_rev} -> {new_rev} ...")
    diffs = mpp_extract.diff_all_books(old_rev, new_rev)
    print(f"  {len(diffs)} raw changes found")
    if not diffs and not write_when_empty:
        print("  No diffs found; not writing report")
        return 0, _commit_date(old_rev)
    mpp_classify.classify_diffs(diffs)
    old_date = _commit_date(old_rev)
    new_date = _commit_date(new_rev)
    os.makedirs(os.path.dirname(output), exist_ok=True)
    json_path = output.removesuffix(".html") + ".json"
    mpp_json.write_json(diffs, old_rev, new_rev, json_path)
    print(f"  JSON written to {json_path}")
    total = mpp_html.write_report(diffs, old_rev, new_rev, output, old_date, new_date)
    print(f"  Report written to {output}")
    return total, old_date


def _run_all():
    """Generate reports for named releases plus unnamed-latest, then write index."""
    with open(RELEASES_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    release_info = []
    for entry in data["releases"]:
        output = f"{CHANGE_LOG_DIR}/{entry['name']}.html"
        count, old_date = _generate_report(entry["old"], entry["new"], output)
        release_info.append(
            {"name": entry["name"], "count": count, "old_date": old_date}
        )
    unnamed_info = _run_unnamed_latest()
    if unnamed_info is not None:
        release_info.append(unnamed_info)
    mpp_index.write_index(release_info, CHANGE_LOG_DIR)


def _run_unnamed_latest():
    """Generate unnamed-latest report and return its index entry, else None."""
    latest_release = _latest_release_entry()
    old_rev = latest_release["new"]
    commit_count = _count_newer_commits(old_rev)
    if commit_count == 0:
        print(
            f"No commits after latest named release ({old_rev}); "
            "skipping unnamed-latest report"
        )
        return None
    count, old_date = _generate_report(
        old_rev,
        "HEAD",
        UNNAMED_LATEST_HTML,
        write_when_empty=False,
    )
    if count == 0:
        print("No diffs in unreleased commit range; skipped unnamed-latest report")
        return None
    return {"name": "unnamed-latest", "count": count, "old_date": old_date}


def almost_main():
    """Generate an unreleased-diffs report (if there are any)."""
    _run_unnamed_latest()


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
        if args.old or args.new:
            if not args.old or not args.new:
                parser.error("--old and --new must be provided together")
            output = args.output or _default_output_path(args.old, args.new)
            _generate_report(args.old, args.new, output)
        else:
            if args.output:
                parser.error("--output requires --old and --new")
            _run_unnamed_latest()


if __name__ == "__main__":
    main()
