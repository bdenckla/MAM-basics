from __future__ import annotations

from dataclasses import dataclass
import re

from mb_cmn import bib_locales as tbn


@dataclass(frozen=True)
class WlcBookCodeInfo:
    bk39id: str
    accents_book_name: str | None = None


_ACCENTS_BOOK_HEADER_RE = re.compile(r"^(?:[1234][ \t]*)?[A-Z][a-z]+[ \t]*$")


# Single source of truth for WLC 4.22 2-char book codes used by accgram.
_WLC_BB_INFO = {
    "gn": WlcBookCodeInfo(bk39id=tbn.BK_GENESIS),
    "ex": WlcBookCodeInfo(bk39id=tbn.BK_EXODUS),
    "lv": WlcBookCodeInfo(bk39id=tbn.BK_LEVIT),
    "nu": WlcBookCodeInfo(bk39id=tbn.BK_NUMBERS),
    "dt": WlcBookCodeInfo(bk39id=tbn.BK_DEUTER),
    "js": WlcBookCodeInfo(bk39id=tbn.BK_JOSHUA),
    "ju": WlcBookCodeInfo(bk39id=tbn.BK_JUDGES),
    "1s": WlcBookCodeInfo(bk39id=tbn.BK_FST_SAM),
    "2s": WlcBookCodeInfo(bk39id=tbn.BK_SND_SAM),
    "1k": WlcBookCodeInfo(bk39id=tbn.BK_FST_KGS),
    "2k": WlcBookCodeInfo(bk39id=tbn.BK_SND_KGS),
    "is": WlcBookCodeInfo(bk39id=tbn.BK_ISAIAH),
    "je": WlcBookCodeInfo(bk39id=tbn.BK_JEREM),
    "ek": WlcBookCodeInfo(bk39id=tbn.BK_EZEKIEL),
    "ho": WlcBookCodeInfo(bk39id=tbn.BK_HOSHEA),
    "jl": WlcBookCodeInfo(bk39id=tbn.BK_JOEL),
    "am": WlcBookCodeInfo(bk39id=tbn.BK_AMOS),
    "ob": WlcBookCodeInfo(bk39id=tbn.BK_OVADIAH),
    "jn": WlcBookCodeInfo(bk39id=tbn.BK_JONAH),
    "mi": WlcBookCodeInfo(bk39id=tbn.BK_MIKHAH),
    "na": WlcBookCodeInfo(bk39id=tbn.BK_NAXUM),
    "hb": WlcBookCodeInfo(bk39id=tbn.BK_XABA),
    "zp": WlcBookCodeInfo(bk39id=tbn.BK_TSEF),
    "hg": WlcBookCodeInfo(bk39id=tbn.BK_XAGGAI),
    "zc": WlcBookCodeInfo(bk39id=tbn.BK_ZEKHAR),
    "ma": WlcBookCodeInfo(bk39id=tbn.BK_MALAKHI),
    "ps": WlcBookCodeInfo(bk39id=tbn.BK_PSALMS),
    "pr": WlcBookCodeInfo(bk39id=tbn.BK_PROV),
    "jb": WlcBookCodeInfo(bk39id=tbn.BK_JOB),
    "ca": WlcBookCodeInfo(bk39id=tbn.BK_SONG, accents_book_name="Song"),
    "ru": WlcBookCodeInfo(bk39id=tbn.BK_RUTH),
    "lm": WlcBookCodeInfo(bk39id=tbn.BK_LAMENT),
    "ec": WlcBookCodeInfo(bk39id=tbn.BK_QOHELET),
    "es": WlcBookCodeInfo(bk39id=tbn.BK_ESTHER),
    "da": WlcBookCodeInfo(bk39id=tbn.BK_DANIEL),
    "er": WlcBookCodeInfo(bk39id=tbn.BK_EZRA),
    "ne": WlcBookCodeInfo(bk39id=tbn.BK_NEXEM),
    "1c": WlcBookCodeInfo(bk39id=tbn.BK_FST_CHR),
    "2c": WlcBookCodeInfo(bk39id=tbn.BK_SND_CHR),
}


def wlc_bb_to_bk39id(bb: str) -> str:
    info = _WLC_BB_INFO.get(bb)
    if info is None:
        raise ValueError(f"Unknown WLC book code in input: {bb}")
    return info.bk39id


def wlc_bb_to_accents_book_name(bb: str) -> str:
    info = _WLC_BB_INFO.get(bb)
    if info is None:
        raise ValueError(f"Unknown WLC book code in input: {bb}")
    book_name = info.accents_book_name or info.bk39id
    if _ACCENTS_BOOK_HEADER_RE.match(book_name) is None:
        raise ValueError(
            "Book name does not conform to accents header expectations: "
            f"bb={bb} name={book_name}"
        )
    return book_name