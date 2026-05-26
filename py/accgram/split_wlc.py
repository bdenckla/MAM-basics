from __future__ import annotations

import re
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path

from accgram.wlc_book_codes import wlc_bb_to_accents_book_name


_BOOK_LINE_RE = re.compile(r"^([0-9a-z]{2})(\d+):(\d+)\b")
_LINE_REF_RE = re.compile(r"^([0-9a-z]{2})(\d+:\d+\s+.*)$")


@dataclass(frozen=True)
class SplitResult:
    books_written: int
    verses_seen: int
    verses_written: int
    verses_excluded: int
    book_order: list[str]


def split_wlc_to_books(
    input_path: Path,
    out_dir: Path,
    keep_line_fn=None,
) -> SplitResult:
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    out_dir.mkdir(parents=True, exist_ok=True)

    per_book: OrderedDict[str, list[str]] = OrderedDict()
    malformed: list[str] = []
    verses_seen = 0
    verses_excluded = 0

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
            chnu = int(m.group(2))
            vrnu = int(m.group(3))
            verses_seen += 1

            if keep_line_fn is not None and not keep_line_fn(bb, chnu, vrnu):
                verses_excluded += 1
                continue

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
        output_lines = []
        book_name = wlc_bb_to_accents_book_name(bb)
        output_lines.append(f"{book_name}\n")

        for raw_line in lines:
            stripped = raw_line.strip()
            if not stripped:
                continue
            # Core transformation: "gn1:2 ..." -> "1:2 ..." (drop 2-char WLC book code).
            m = _LINE_REF_RE.match(stripped)
            if m is None:
                raise ValueError(
                    "Unexpected verse line format during accents normalization: "
                    f"bb={bb} line={stripped[:120]}"
                )
            output_lines.append(f"{m.group(2)}\n")

        with out_path.open("w", encoding="utf-8", newline="") as f_out:
            f_out.writelines(output_lines)
        verses_written += len(lines)

    return SplitResult(
        books_written=len(per_book),
        verses_seen=verses_seen,
        verses_written=verses_written,
        verses_excluded=verses_excluded,
        book_order=list(per_book.keys()),
    )
