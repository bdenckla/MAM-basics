from __future__ import annotations

import re

from wlc_cmn.wlc_book_codes import wlc_bb_codes

_TROUBLEMAKER_REF_RE = re.compile(r"^(?P<bb>[0-9a-z]{2})\s+(?P<ch>\d+):(?P<vr>\d+)$")

# Standard MAM book order, derived from the single source of truth for WLC book codes.
_WLC_BB_READING_ORDER = {bb: index for index, bb in enumerate(wlc_bb_codes())}


def parse_ref(ref: str, *, row_kind: str = "troublemaker") -> tuple[str, int, int]:
    match = _TROUBLEMAKER_REF_RE.match(ref.strip())
    if match is None:
        raise ValueError(f"Malformed {row_kind} ref: {ref}")
    bb = match.group("bb")
    chnu = int(match.group("ch"))
    vrnu = int(match.group("vr"))
    return bb, chnu, vrnu


def to_compact_bcv(bb: str, chnu: int, vrnu: int) -> str:
    return f"{bb}{chnu}:{vrnu}"


def to_ref(bb: str, chnu: int, vrnu: int) -> str:
    return f"{bb} {chnu}:{vrnu}"


def reading_order_key(
    ref: str, *, row_kind: str = "troublemaker"
) -> tuple[int, int, int]:
    """Sort key putting refs in standard reading order: MAM book, chapter, verse."""
    bb, chnu, vrnu = parse_ref(ref, row_kind=row_kind)
    book_index = _WLC_BB_READING_ORDER.get(bb)
    if book_index is None:
        raise ValueError(f"Unknown WLC book code in {row_kind} ref: {ref}")
    return (book_index, chnu, vrnu)
