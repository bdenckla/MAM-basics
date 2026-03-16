"""
Compare two git revisions of MAM-parsed plus/ JSON and generate an HTML
diff report with category filtering.

Usage:
    .venv/Scripts/python.exe py/main_diff_mpp.py --old <rev> --new <rev>

The revisions are git refs in the ../MAM-parsed repo (commits, tags, branches).
Output goes to out/diff_mpp/<old>_<new>.html by default.
"""

import argparse
import os
from pydiff_mpp import mpp_extract, mpp_classify, mpp_html


def _sanitize_rev(rev):
    """Make a revision string safe for use in a filename."""
    return (
        rev.replace("/", "_")
        .replace("\\", "_")
        .replace("..", "_")
        .replace("^", "-")[:20]
    )


def main():
    parser = argparse.ArgumentParser(
        description="Compare two revisions of MAM-parsed plus/ and generate an HTML report."
    )
    parser.add_argument(
        "--old", required=True, help="Old git revision (in ../MAM-parsed repo)"
    )
    parser.add_argument(
        "--new", required=True, help="New git revision (in ../MAM-parsed repo)"
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Output HTML path (default: out/diff_mpp/<old>_<new>.html)",
    )
    args = parser.parse_args()

    if args.output is None:
        out_dir = "out/diff_mpp"
        os.makedirs(out_dir, exist_ok=True)
        slug = f"{_sanitize_rev(args.old)}_{_sanitize_rev(args.new)}"
        args.output = f"{out_dir}/{slug}.html"

    print(f"Comparing {args.old} -> {args.new} ...")
    diffs = mpp_extract.diff_all_books(args.old, args.new)
    print(f"  {len(diffs)} raw changes found")

    mpp_classify.classify_diffs(diffs)

    mpp_html.write_report(diffs, args.old, args.new, args.output)
    print(f"  Report written to {args.output}")


if __name__ == "__main__":
    main()
