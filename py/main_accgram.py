"""Accent grammar utilities.

Subcommands:
    split-wlc   Split wlc422_ps.txt into per-book files named
                wlc_422_ps_bb.txt where bb is a two-character WLC book code.
    filter-split-wlc
                Split like split-wlc, but exclude Psalms/Proverbs entirely,
                exclude poetically-cantillated verses of Job, and exclude
                all dual-cantillation verses.
    run-orig    Run accents (via WSL) on split files and write *_ag outputs.

Examples:
    .venv/Scripts/python.exe py/main_accgram.py split-wlc
    .venv/Scripts/python.exe py/main_accgram.py split-wlc --out-dir .novc/wlc_422_ps
    .venv/Scripts/python.exe py/main_accgram.py split-wlc --input C:/path/to/wlc422_ps.txt
    .venv/Scripts/python.exe py/main_accgram.py filter-split-wlc
    .venv/Scripts/python.exe py/main_accgram.py run-orig
"""

from __future__ import annotations

import argparse
from pathlib import Path

from accgram import filter_split_wlc, run_orig, split_wlc


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _default_input_path() -> Path:
    # Sibling checkout expected by the user:
    #   GitRepos/wlc-utils-io/in/wlc422/wlc422_ps.txt
    return _repo_root().parent / "wlc-utils-io" / "in" / "wlc422" / "wlc422_ps.txt"


def _run_split_wlc(args: argparse.Namespace) -> None:
    split_wlc.run(args)


def _run_filter_split_wlc(args: argparse.Namespace) -> None:
    filter_split_wlc.run(args, split_wlc.split_wlc_to_books)


def _run_orig(args: argparse.Namespace) -> None:
    run_orig.run(args)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="subcommand", metavar="SUBCOMMAND")
    subparsers.required = True

    split_wlc_parser = subparsers.add_parser(
        "split-wlc",
        help="Split wlc422_ps.txt into per-book files in a target directory.",
    )
    split_wlc.add_args(
        split_wlc_parser,
        default_input_path=_default_input_path(),
        repo_root=_repo_root(),
    )
    split_wlc_parser.set_defaults(func=_run_split_wlc)

    filter_split_wlc_parser = subparsers.add_parser(
        "filter-split-wlc",
        help=(
            "Split wlc422_ps.txt while filtering out Psalms/Proverbs, "
            "poetic Job verses, and dual-cantillation verses."
        ),
    )
    filter_split_wlc.add_args(
        filter_split_wlc_parser,
        default_input_path=_default_input_path(),
        repo_root=_repo_root(),
    )
    filter_split_wlc_parser.set_defaults(func=_run_filter_split_wlc)

    run_orig_parser = subparsers.add_parser(
        "run-orig",
        help=(
            "Run accents (via WSL) on split input files and write *_ag.txt outputs "
            "plus stderr sidecars (default: out/accgram/orig-stderr)."
        ),
    )
    run_orig.add_args(run_orig_parser, repo_root=_repo_root())
    run_orig_parser.set_defaults(func=_run_orig)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
