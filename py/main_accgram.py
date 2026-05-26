"""Accent grammar utilities.

Subcommands:
    split-wlc   Split wlc422_ps.txt into per-book files named
                wlc_422_ps_bb.txt where bb is a two-character WLC book code.

Examples:
    .venv/Scripts/python.exe py/main_accgram.py split-wlc
    .venv/Scripts/python.exe py/main_accgram.py split-wlc --out-dir .novc/wlc_422_ps
    .venv/Scripts/python.exe py/main_accgram.py split-wlc --input C:/path/to/wlc422_ps.txt
"""

from __future__ import annotations

import argparse
import re
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path


_BOOK_LINE_RE = re.compile(r"^([0-9a-z]{2})\d+:\d+\b")


@dataclass(frozen=True)
class SplitResult:
    books_written: int
    verses_written: int
    book_order: list[str]


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _default_input_path() -> Path:
    # Sibling checkout expected by the user:
    #   GitRepos/wlc-utils-io/in/wlc422/wlc422_ps.txt
    return _repo_root().parent / "wlc-utils-io" / "in" / "wlc422" / "wlc422_ps.txt"


def _default_out_dir() -> Path:
    return _repo_root() / ".novc" / "wlc_422_ps"


def _split_wlc_to_books(input_path: Path, out_dir: Path) -> SplitResult:
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    out_dir.mkdir(parents=True, exist_ok=True)

    per_book: OrderedDict[str, list[str]] = OrderedDict()
    malformed: list[str] = []

    with input_path.open("r", encoding="utf-8") as f_in:
        for line_no, raw_line in enumerate(f_in, start=1):
            stripped = raw_line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            m = _BOOK_LINE_RE.match(stripped)
            if m is None:
                if len(malformed) < 10:
                    malformed.append(f"line {line_no}: {stripped[:120]}")
                continue

            bb = m.group(1)
            per_book.setdefault(bb, []).append(raw_line)

    if malformed:
        preview = "\n".join(malformed)
        raise ValueError(
            "Encountered malformed non-comment lines while splitting input. "
            f"First {len(malformed)} examples:\n{preview}"
        )

    verses_written = 0
    for bb, lines in per_book.items():
        out_path = out_dir / f"wlc_422_ps_{bb}.txt"
        with out_path.open("w", encoding="utf-8", newline="") as f_out:
            f_out.writelines(lines)
        verses_written += len(lines)

    return SplitResult(
        books_written=len(per_book),
        verses_written=verses_written,
        book_order=list(per_book.keys()),
    )


def _add_split_wlc_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--input",
        type=Path,
        default=_default_input_path(),
        help="Path to source wlc422_ps.txt file.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=_default_out_dir(),
        help="Directory for output files (default: .novc/wlc_422_ps under this repo).",
    )


def _run_split_wlc(args: argparse.Namespace) -> None:
    result = _split_wlc_to_books(input_path=args.input, out_dir=args.out_dir)
    print(f"Input: {args.input}")
    print(f"Output directory: {args.out_dir}")
    print(f"Books written: {result.books_written}")
    print(f"Verses written: {result.verses_written}")
    print(f"Book order: {','.join(result.book_order)}")


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
    _add_split_wlc_args(split_wlc_parser)
    split_wlc_parser.set_defaults(func=_run_split_wlc)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
