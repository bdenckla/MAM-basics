from __future__ import annotations

import argparse
from pathlib import Path

from mb_cmn import bib_locales as tbn


# WLC 4.22 two-character book code -> mb_cmn bk39id
_WLC_BB_TO_BK39ID = {
    "gn": tbn.BK_GENESIS,
    "ex": tbn.BK_EXODUS,
    "lv": tbn.BK_LEVIT,
    "nu": tbn.BK_NUMBERS,
    "dt": tbn.BK_DEUTER,
    "js": tbn.BK_JOSHUA,
    "ju": tbn.BK_JUDGES,
    "1s": tbn.BK_FST_SAM,
    "2s": tbn.BK_SND_SAM,
    "1k": tbn.BK_FST_KGS,
    "2k": tbn.BK_SND_KGS,
    "is": tbn.BK_ISAIAH,
    "je": tbn.BK_JEREM,
    "ek": tbn.BK_EZEKIEL,
    "ho": tbn.BK_HOSHEA,
    "jl": tbn.BK_JOEL,
    "am": tbn.BK_AMOS,
    "ob": tbn.BK_OVADIAH,
    "jn": tbn.BK_JONAH,
    "mi": tbn.BK_MIKHAH,
    "na": tbn.BK_NAXUM,
    "hb": tbn.BK_XABA,
    "zp": tbn.BK_TSEF,
    "hg": tbn.BK_XAGGAI,
    "zc": tbn.BK_ZEKHAR,
    "ma": tbn.BK_MALAKHI,
    "ps": tbn.BK_PSALMS,
    "pr": tbn.BK_PROV,
    "jb": tbn.BK_JOB,
    "ca": tbn.BK_SONG,
    "ru": tbn.BK_RUTH,
    "lm": tbn.BK_LAMENT,
    "ec": tbn.BK_QOHELET,
    "es": tbn.BK_ESTHER,
    "da": tbn.BK_DANIEL,
    "er": tbn.BK_EZRA,
    "ne": tbn.BK_NEXEM,
    "1c": tbn.BK_FST_CHR,
    "2c": tbn.BK_SND_CHR,
}


def default_out_dir(repo_root: Path) -> Path:
    return repo_root / ".novc" / "wlc_422_psf"


def add_args(parser: argparse.ArgumentParser, default_input_path: Path, repo_root: Path) -> None:
    parser.add_argument(
        "--input",
        type=Path,
        default=default_input_path,
        help="Path to source wlc422_ps.txt file.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=default_out_dir(repo_root),
        help="Directory for output files (default: .novc/wlc_422_psf under this repo).",
    )


def run(args: argparse.Namespace, split_wlc_to_books_fn) -> None:
    result = split_wlc_to_books_fn(
        input_path=args.input,
        out_dir=args.out_dir,
        keep_line_fn=should_keep_line,
    )
    print(f"Input: {args.input}")
    print(f"Output directory: {args.out_dir}")
    print(f"Verses seen: {result.verses_seen}")
    print(f"Verses excluded: {result.verses_excluded}")
    print(f"Books written: {result.books_written}")
    print(f"Verses written: {result.verses_written}")
    print(f"Book order: {','.join(result.book_order)}")


def _wlc_bb_to_bk39id(bb: str) -> str:
    bk39id = _WLC_BB_TO_BK39ID.get(bb)
    if bk39id is None:
        raise ValueError(f"Unknown WLC book code in input: {bb}")
    return bk39id


def should_keep_line(bb: str, chnu: int, vrnu: int) -> bool:
    # Exclude Psalms and Proverbs wholesale.
    if bb in ("ps", "pr"):
        return False

    bk39id = _wlc_bb_to_bk39id(bb)
    bcvtmam = tbn.mk_bcvtmam(bk39id, chnu, vrnu)

    # Exclude all dual-cantillation locales (Gen 35:22, Ex 20:2-13, Deut 5:6-17).
    if tbn.has_dualcant(bcvtmam):
        return False

    # Exclude Job verses that use poetic cantillation.
    if bk39id == tbn.BK_JOB and tbn.is_poetcant(bcvtmam):
        return False

    return True