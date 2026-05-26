from __future__ import annotations

import argparse
import json
from pathlib import Path

from mb_cmn import bib_locales as tbn
from py_misc import get_cvm_rec_from_bcvt as gcrfb


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
    seen_refs: dict[str, set[tuple[int, int]]] = {}
    excluded_refs: dict[str, set[tuple[int, int]]] = {}

    def keep_line_with_logging(bb: str, chnu: int, vrnu: int) -> bool:
        seen_refs.setdefault(bb, set()).add((chnu, vrnu))
        keep = should_keep_line(bb, chnu, vrnu)
        if not keep:
            excluded_refs.setdefault(bb, set()).add((chnu, vrnu))
        return keep

    result = split_wlc_to_books_fn(
        input_path=args.input,
        out_dir=args.out_dir,
        keep_line_fn=keep_line_with_logging,
    )
    filtered_out_path = args.out_dir / "filtered-out.json"
    _write_filtered_out_json(
        filtered_out_path=filtered_out_path,
        input_path=args.input,
        out_dir=args.out_dir,
        verses_seen=result.verses_seen,
        verses_excluded=result.verses_excluded,
        seen_refs=seen_refs,
        excluded_refs=excluded_refs,
    )

    print(f"Input: {args.input}")
    print(f"Output directory: {args.out_dir}")
    print(f"Verses seen: {result.verses_seen}")
    print(f"Verses excluded: {result.verses_excluded}")
    print(f"Books written: {result.books_written}")
    print(f"Verses written: {result.verses_written}")
    print(f"Book order: {','.join(result.book_order)}")
    print(f"Exclusion log: {filtered_out_path}")


def _format_int_ranges(sorted_values: list[int]) -> list[str]:
    if not sorted_values:
        return []
    ranges: list[str] = []
    start = sorted_values[0]
    prev = start
    for value in sorted_values[1:]:
        if value == prev + 1:
            prev = value
            continue
        ranges.append(str(start) if start == prev else f"{start}-{prev}")
        start = value
        prev = value
    ranges.append(str(start) if start == prev else f"{start}-{prev}")
    return ranges


def _to_chapter_verse_map(refs: set[tuple[int, int]]) -> dict[int, set[int]]:
    by_chapter: dict[int, set[int]] = {}
    for chnu, vrnu in refs:
        by_chapter.setdefault(chnu, set()).add(vrnu)
    return by_chapter


def _summarize_partial_book(
    seen_book_refs: set[tuple[int, int]], excluded_book_refs: set[tuple[int, int]]
) -> dict[str, object]:
    seen_by_chapter = _to_chapter_verse_map(seen_book_refs)
    excluded_by_chapter = _to_chapter_verse_map(excluded_book_refs)

    fully_excluded_chapters: list[int] = []
    partial_chapters: dict[str, list[str]] = {}

    for chnu in sorted(excluded_by_chapter.keys()):
        excluded_verses = excluded_by_chapter[chnu]
        seen_verses = seen_by_chapter.get(chnu, set())
        if seen_verses and excluded_verses == seen_verses:
            fully_excluded_chapters.append(chnu)
            continue
        partial_chapters[str(chnu)] = _format_int_ranges(sorted(excluded_verses))

    summary: dict[str, object] = {}
    if fully_excluded_chapters:
        summary["full_chapters"] = _format_int_ranges(fully_excluded_chapters)
    if partial_chapters:
        summary["partial_chapters"] = partial_chapters
    return summary


def _write_filtered_out_json(
    filtered_out_path: Path,
    input_path: Path,
    out_dir: Path,
    verses_seen: int,
    verses_excluded: int,
    seen_refs: dict[str, set[tuple[int, int]]],
    excluded_refs: dict[str, set[tuple[int, int]]],
) -> None:
    books_fully_excluded: list[str] = []
    books_partially_excluded: dict[str, dict[str, object]] = {}

    for bb in sorted(excluded_refs.keys()):
        seen_book_refs = seen_refs.get(bb, set())
        excluded_book_refs = excluded_refs[bb]
        if seen_book_refs and excluded_book_refs == seen_book_refs:
            books_fully_excluded.append(bb)
            continue
        books_partially_excluded[bb] = _summarize_partial_book(seen_book_refs, excluded_book_refs)

    payload: dict[str, object] = {
        "input": str(input_path),
        "out_dir": str(out_dir),
        "summary": {
            "verses_seen": verses_seen,
            "verses_excluded": verses_excluded,
            "books_with_exclusions": len(excluded_refs),
            "books_fully_excluded": len(books_fully_excluded),
            "books_partially_excluded": len(books_partially_excluded),
        },
        "books_fully_excluded": books_fully_excluded,
        "books_partially_excluded": books_partially_excluded,
    }

    filtered_out_path.parent.mkdir(parents=True, exist_ok=True)
    with filtered_out_path.open("w", encoding="utf-8", newline="\n") as f_out:
        json.dump(payload, f_out, ensure_ascii=False, indent=2, sort_keys=True)
        f_out.write("\n")


def _wlc_bb_to_bk39id(bb: str) -> str:
    bk39id = _WLC_BB_TO_BK39ID.get(bb)
    if bk39id is None:
        raise ValueError(f"Unknown WLC book code in input: {bb}")
    return bk39id


def _wlc_bhs_to_mam_bcvt(bk39id: str, chnu: int, vrnu: int):
    """Convert a WLC verse ref (BHS versification) to MAM bcvt."""
    bcvtbhs = tbn.mk_bcvtbhs(bk39id, chnu, vrnu)
    cvm_rec = gcrfb.get_cvm_rec_from_bcvt(bcvtbhs)
    if cvm_rec is None:
        return tbn.mk_bcvtmam(bk39id, chnu, vrnu)
    _, cvtmam = gcrfb.cvm_rec_get_parts(cvm_rec)
    return tbn.mk_bcvt(bk39id, cvtmam)


def should_keep_line(bb: str, chnu: int, vrnu: int) -> bool:
    # Exclude Psalms and Proverbs wholesale.
    if bb in ("ps", "pr"):
        return False

    bk39id = _wlc_bb_to_bk39id(bb)
    bcvtmam = _wlc_bhs_to_mam_bcvt(bk39id, chnu, vrnu)

    # Exclude all dual-cantillation locales, reckoned from WLC/BHS refs.
    # These map to MAM locales internally before checking has_dualcant.
    if tbn.has_dualcant(bcvtmam):
        return False

    # Exclude Job verses that use poetic cantillation.
    if bk39id == tbn.BK_JOB and tbn.is_poetcant(bcvtmam):
        return False

    return True