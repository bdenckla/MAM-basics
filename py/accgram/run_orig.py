from __future__ import annotations

import argparse
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path

from accgram.wlc_book_codes import wlc_bb_to_accents_book_name


_INPUT_FILE_RE = re.compile(r"^wlc_422_ps_([0-9a-z]{2})\.txt$")
_LINE_REF_RE = re.compile(r"^([0-9a-z]{2})(\d+:\d+\s+.*)$")


@dataclass(frozen=True)
class RunResult:
    input_count: int
    output_count: int
    nonempty_output_count: int
    stderr_nonempty_count: int
    nonzero_exit_count: int


def default_in_dir(repo_root: Path) -> Path:
    return repo_root / ".novc" / "wlc_422_psf"


def default_out_dir(repo_root: Path) -> Path:
    return repo_root / "out" / "accgram" / "orig"


def default_stderr_dir(repo_root: Path) -> Path:
    return repo_root / "out" / "accgram" / "orig-stderr"


def default_accents_bin(repo_root: Path) -> Path:
    return repo_root / "accents-1.1.4" / "accents"


def add_args(parser: argparse.ArgumentParser, repo_root: Path) -> None:
    parser.add_argument(
        "--in-dir",
        type=Path,
        default=default_in_dir(repo_root),
        help="Directory containing input files named wlc_422_ps_bb.txt.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=default_out_dir(repo_root),
        help="Directory for outputs named *_ag.txt.",
    )
    parser.add_argument(
        "--stderr-dir",
        type=Path,
        default=default_stderr_dir(repo_root),
        help="Directory for stderr sidecars named *_ag.stderr.txt.",
    )
    parser.add_argument(
        "--accents-bin",
        type=Path,
        default=default_accents_bin(repo_root),
        help="Path to Linux accents binary (invoked via WSL).",
    )
    parser.add_argument(
        "--skip-normalize",
        action="store_true",
        help=(
            "Pipe input files to accents as-is. By default, run-orig normalizes "
            "wlc_422_ps_bb.txt lines to the headings/reference style expected by accents."
        ),
    )


def _to_wsl_path(path: Path) -> str:
    resolved = path.resolve()
    drive = resolved.drive.rstrip(":")
    if not drive:
        return str(resolved).replace("\\", "/")
    rest = resolved.as_posix().split(":", 1)[1]
    return f"/mnt/{drive.lower()}{rest}"


def _book_code_from_name(name: str) -> str | None:
    m = _INPUT_FILE_RE.match(name)
    if m is None:
        return None
    return m.group(1)


def _normalize_for_accents(raw_text: str, bb: str | None) -> str:
    lines: list[str] = []
    if bb is not None:
        book_name = wlc_bb_to_accents_book_name(bb)
        if book_name is not None:
            lines.append(book_name)

    for raw_line in raw_text.splitlines():
        if not raw_line.strip():
            continue
        m = _LINE_REF_RE.match(raw_line)
        if m is None:
            lines.append(raw_line)
            continue
        lines.append(m.group(2))

    return "\n".join(lines) + "\n"


def run(args: argparse.Namespace) -> None:
    result = run_orig(
        in_dir=args.in_dir,
        out_dir=args.out_dir,
        stderr_dir=args.stderr_dir,
        accents_bin=args.accents_bin,
        normalize=(not args.skip_normalize),
    )
    print(f"Input directory: {args.in_dir}")
    print(f"Output directory: {args.out_dir}")
    print(f"Stderr directory: {args.stderr_dir}")
    print(f"Inputs processed: {result.input_count}")
    print(f"Outputs written: {result.output_count}")
    print(f"Non-empty outputs: {result.nonempty_output_count}")
    print(f"Files with non-empty stderr sidecars: {result.stderr_nonempty_count}")
    print(f"Nonzero accents exit codes: {result.nonzero_exit_count}")


def run_orig(
    in_dir: Path,
    out_dir: Path,
    stderr_dir: Path,
    accents_bin: Path,
    normalize: bool = True,
) -> RunResult:
    if not in_dir.is_dir():
        raise FileNotFoundError(f"Input directory not found: {in_dir}")
    if not accents_bin.is_file():
        raise FileNotFoundError(f"accents binary not found: {accents_bin}")

    out_dir.mkdir(parents=True, exist_ok=True)
    stderr_dir.mkdir(parents=True, exist_ok=True)

    input_paths = sorted(p for p in in_dir.iterdir() if p.is_file() and p.suffix.lower() == ".txt")
    nonempty_output_count = 0
    stderr_nonempty_count = 0
    nonzero_exit_count = 0

    accents_wsl_path = _to_wsl_path(accents_bin)
    for input_path in input_paths:
        stem = input_path.stem
        output_path = out_dir / f"{stem}_ag.txt"
        stderr_path = stderr_dir / f"{stem}_ag.stderr.txt"

        raw_text = input_path.read_text(encoding="utf-8")
        payload = raw_text
        if normalize:
            payload = _normalize_for_accents(raw_text=raw_text, bb=_book_code_from_name(input_path.name))

        cp = subprocess.run(
            ["wsl", accents_wsl_path, "-p"],
            input=payload.encode("utf-8"),
            capture_output=True,
            check=False,
        )

        stdout_text = cp.stdout.decode("utf-8", errors="replace")
        stderr_text = cp.stderr.decode("utf-8", errors="replace")

        output_path.write_text(stdout_text, encoding="utf-8", newline="\n")
        if stdout_text:
            nonempty_output_count += 1

        if cp.returncode != 0:
            nonzero_exit_count += 1
            if not stderr_text:
                stderr_text = (
                    f"accents exited with code {cp.returncode} and produced no stderr output.\n"
                )

        stderr_path.write_text(stderr_text, encoding="utf-8", newline="\n")
        if stderr_text:
            stderr_nonempty_count += 1

    return RunResult(
        input_count=len(input_paths),
        output_count=len(input_paths),
        nonempty_output_count=nonempty_output_count,
        stderr_nonempty_count=stderr_nonempty_count,
        nonzero_exit_count=nonzero_exit_count,
    )