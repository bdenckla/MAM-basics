import mb_cmn.bib_locales as tbn
import re

_XLK_KEY_FOR_DLOC = "xlk-dloc-data"
_XLK_KEY_FOR_AELOC = "xlk-aeloc-data"


def make_dloc(sloc1, sloc2):
    assert sloc_okay(sloc1)
    assert sloc_okay(sloc2)
    return {_XLK_KEY_FOR_DLOC: (sloc1, sloc2)}


def get_pair_inside_dloc(xloc):
    return isinstance(xloc, dict) and xloc.get(_XLK_KEY_FOR_DLOC)


def make_aeloc(sloc):
    assert sloc_okay(sloc)
    return {_XLK_KEY_FOR_AELOC: sloc}


def get_sloc_inside_aeloc(xloc):
    return isinstance(xloc, dict) and xloc.get(_XLK_KEY_FOR_AELOC)


def sloc_okay(sloc):
    assert isinstance(sloc, str)
    if sloc[0] != "@":
        return False
    sloc_proper = sloc[1:]
    bcv_patt = r"([A-zḥḤ0-9][A-zḥḤ]{1,3}) " + r"(\d+)" + ":" + r"(\d+)"
    match = re.fullmatch(bcv_patt, sloc_proper)
    assert match is not None
    ybkid, chnu_str, vrnu_str = match.groups()
    _chnu_int = int(chnu_str)
    _vrnu_int = int(vrnu_str)
    if ybkid not in _YEIVIN_BOOK_IDS:
        return False
    return True


YBKID_AND_STD_BKID_PAIRS = [
    ("Gen", tbn.BK_GENESIS),
    ("Ex", tbn.BK_EXODUS),
    ("Lev", tbn.BK_LEVIT),
    ("Nu", tbn.BK_NUMBERS),
    ("Dt", tbn.BK_DEUTER),
    ("Jos", tbn.BK_JOSHUA),
    ("Jud", tbn.BK_JUDGES),
    ("1S", tbn.BK_FST_SAM),
    ("2S", tbn.BK_SND_SAM),
    ("1K", tbn.BK_FST_KGS),
    ("2K", tbn.BK_SND_KGS),
    ("Is", tbn.BK_ISAIAH),
    ("Jer", tbn.BK_JEREM),
    ("Ez", tbn.BK_EZEKIEL),  # Ezek = Ez & Ezra = Ezra seems like a bad idea
    ("Ho", tbn.BK_HOSHEA),  # removed 's' to avoid Hosea vs. Hoshea dispute
    ("Joel", tbn.BK_JOEL),
    ("Amos", tbn.BK_AMOS),
    ("???", tbn.BK_OVADIAH),
    ("???", tbn.BK_JONAH),
    ("Mi", tbn.BK_MIKHAH),  # removed 'c' to avoid Micah vs. Mikhah dispute
    ("Naḥ", tbn.BK_NAXUM),
    ("Ḥab", tbn.BK_XABA),
    ("Zeph", tbn.BK_TSEF),
    ("Ḥag", tbn.BK_XAGGAI),
    ("Zech", tbn.BK_ZEKHAR),
    ("???", tbn.BK_MALAKHI),
    ("Ps", tbn.BK_PSALMS),
    ("Prov", tbn.BK_PROV),
    ("Job", tbn.BK_JOB),
    ("Song", tbn.BK_SONG),
    ("Rut", tbn.BK_RUTH),
    ("Lam", tbn.BK_LAMENT),
    ("Qoh", tbn.BK_QOHELET),
    ("Est", tbn.BK_ESTHER),
    ("Dan", tbn.BK_DANIEL),
    ("Ezra", tbn.BK_EZRA),  # Ezek = Ez & Ezra = Ezra seems like a bad idea
    ("Neḥ", tbn.BK_NEXEM),
    ("1C", tbn.BK_FST_CHR),
    ("2C", tbn.BK_SND_CHR),
]
_YEIVIN_BOOK_IDS = set(pair[0] for pair in YBKID_AND_STD_BKID_PAIRS)
