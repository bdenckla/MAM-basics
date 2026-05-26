from __future__ import annotations

from dataclasses import dataclass

from mb_cmn import bib_locales as tbn


@dataclass(frozen=True)
class WlcBookCodeInfo:
    bk39id: str
    accents_book_name: str


# Single source of truth for WLC 4.22 2-char book codes used by accgram.
_WLC_BB_INFO = {
    "gn": WlcBookCodeInfo(bk39id=tbn.BK_GENESIS, accents_book_name="Genesis"),
    "ex": WlcBookCodeInfo(bk39id=tbn.BK_EXODUS, accents_book_name="Exodus"),
    "lv": WlcBookCodeInfo(bk39id=tbn.BK_LEVIT, accents_book_name="Leviticus"),
    "nu": WlcBookCodeInfo(bk39id=tbn.BK_NUMBERS, accents_book_name="Numbers"),
    "dt": WlcBookCodeInfo(bk39id=tbn.BK_DEUTER, accents_book_name="Deuteronomy"),
    "js": WlcBookCodeInfo(bk39id=tbn.BK_JOSHUA, accents_book_name="Joshua"),
    "ju": WlcBookCodeInfo(bk39id=tbn.BK_JUDGES, accents_book_name="Judges"),
    "1s": WlcBookCodeInfo(bk39id=tbn.BK_FST_SAM, accents_book_name="1 Samuel"),
    "2s": WlcBookCodeInfo(bk39id=tbn.BK_SND_SAM, accents_book_name="2 Samuel"),
    "1k": WlcBookCodeInfo(bk39id=tbn.BK_FST_KGS, accents_book_name="1 Kings"),
    "2k": WlcBookCodeInfo(bk39id=tbn.BK_SND_KGS, accents_book_name="2 Kings"),
    "is": WlcBookCodeInfo(bk39id=tbn.BK_ISAIAH, accents_book_name="Isaiah"),
    "je": WlcBookCodeInfo(bk39id=tbn.BK_JEREM, accents_book_name="Jeremiah"),
    "ek": WlcBookCodeInfo(bk39id=tbn.BK_EZEKIEL, accents_book_name="Ezekiel"),
    "ho": WlcBookCodeInfo(bk39id=tbn.BK_HOSHEA, accents_book_name="Hosea"),
    "jl": WlcBookCodeInfo(bk39id=tbn.BK_JOEL, accents_book_name="Joel"),
    "am": WlcBookCodeInfo(bk39id=tbn.BK_AMOS, accents_book_name="Amos"),
    "ob": WlcBookCodeInfo(bk39id=tbn.BK_OVADIAH, accents_book_name="Obadiah"),
    "jn": WlcBookCodeInfo(bk39id=tbn.BK_JONAH, accents_book_name="Jonah"),
    "mi": WlcBookCodeInfo(bk39id=tbn.BK_MIKHAH, accents_book_name="Micah"),
    "na": WlcBookCodeInfo(bk39id=tbn.BK_NAXUM, accents_book_name="Nahum"),
    "hb": WlcBookCodeInfo(bk39id=tbn.BK_XABA, accents_book_name="Habakkuk"),
    "zp": WlcBookCodeInfo(bk39id=tbn.BK_TSEF, accents_book_name="Zephaniah"),
    "hg": WlcBookCodeInfo(bk39id=tbn.BK_XAGGAI, accents_book_name="Haggai"),
    "zc": WlcBookCodeInfo(bk39id=tbn.BK_ZEKHAR, accents_book_name="Zechariah"),
    "ma": WlcBookCodeInfo(bk39id=tbn.BK_MALAKHI, accents_book_name="Malachi"),
    "ps": WlcBookCodeInfo(bk39id=tbn.BK_PSALMS, accents_book_name="Psalms"),
    "pr": WlcBookCodeInfo(bk39id=tbn.BK_PROV, accents_book_name="Proverbs"),
    "jb": WlcBookCodeInfo(bk39id=tbn.BK_JOB, accents_book_name="Job"),
    "ca": WlcBookCodeInfo(bk39id=tbn.BK_SONG, accents_book_name="Song"),
    "ru": WlcBookCodeInfo(bk39id=tbn.BK_RUTH, accents_book_name="Ruth"),
    "lm": WlcBookCodeInfo(bk39id=tbn.BK_LAMENT, accents_book_name="Lamentations"),
    "ec": WlcBookCodeInfo(bk39id=tbn.BK_QOHELET, accents_book_name="Ecclesiastes"),
    "es": WlcBookCodeInfo(bk39id=tbn.BK_ESTHER, accents_book_name="Esther"),
    "da": WlcBookCodeInfo(bk39id=tbn.BK_DANIEL, accents_book_name="Daniel"),
    "er": WlcBookCodeInfo(bk39id=tbn.BK_EZRA, accents_book_name="Ezra"),
    "ne": WlcBookCodeInfo(bk39id=tbn.BK_NEXEM, accents_book_name="Nehemiah"),
    "1c": WlcBookCodeInfo(bk39id=tbn.BK_FST_CHR, accents_book_name="1 Chronicles"),
    "2c": WlcBookCodeInfo(bk39id=tbn.BK_SND_CHR, accents_book_name="2 Chronicles"),
}


def wlc_bb_to_bk39id(bb: str) -> str:
    info = _WLC_BB_INFO.get(bb)
    if info is None:
        raise ValueError(f"Unknown WLC book code in input: {bb}")
    return info.bk39id


def wlc_bb_to_accents_book_name(bb: str) -> str | None:
    info = _WLC_BB_INFO.get(bb)
    if info is None:
        return None
    return info.accents_book_name