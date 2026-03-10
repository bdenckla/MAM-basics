"""
This module provides maps (dicts) in both directions between:

    a standard book name like '1Samuel'
    and
    a MAM book name pair like (str('ספר שמואל'), str('שמ"א'))

Note that MAM book names are pairs!
I.e., MAM book names are tuples of length 2.
"""

from pycmn import mam_bknas
from pycmn import bib_locales as tbn


def he_bk39_name(bk39id):
    """
    Given a bk39id, return the corresponding Hebrew bk39 name.
    """
    mam_he_book_name_pair = BK39ID_TO_MAM_HBNP[bk39id]
    return mam_bknas.he_bk39_name(*mam_he_book_name_pair)


def wikisource_book_path_fr_bk39id(path, bk39id):
    """
    Given bk39id, return the path to the corresponding JSON-format file
    downloaded from Wikisource.
    """
    osdf = tbn.ordered_short_dash_full_39(bk39id)
    return f"{path}/{osdf}.json"  # E.g. "in/mam-ws/A1-Genesis.json"


def _flip(pair):
    return pair[1], pair[0]


_PAIRS = (
    (mam_bknas.BS_GENESIS, tbn.BK_GENESIS),
    (mam_bknas.BS_EXODUS, tbn.BK_EXODUS),
    (mam_bknas.BS_LEVIT, tbn.BK_LEVIT),
    (mam_bknas.BS_NUMBERS, tbn.BK_NUMBERS),
    (mam_bknas.BS_DEUTER, tbn.BK_DEUTER),
    (mam_bknas.BS_JOSHUA, tbn.BK_JOSHUA),
    (mam_bknas.BS_JUDGES, tbn.BK_JUDGES),
    (mam_bknas.BS_FST_SAM, tbn.BK_FST_SAM),
    (mam_bknas.BS_SND_SAM, tbn.BK_SND_SAM),
    (mam_bknas.BS_FST_KGS, tbn.BK_FST_KGS),
    (mam_bknas.BS_SND_KGS, tbn.BK_SND_KGS),
    (mam_bknas.BS_ISAIAH, tbn.BK_ISAIAH),
    (mam_bknas.BS_JEREM, tbn.BK_JEREM),
    (mam_bknas.BS_EZEKIEL, tbn.BK_EZEKIEL),
    (mam_bknas.BS_HOSEA, tbn.BK_HOSHEA),
    (mam_bknas.BS_JOEL, tbn.BK_JOEL),
    (mam_bknas.BS_AMOS, tbn.BK_AMOS),
    (mam_bknas.BS_OBADIAH, tbn.BK_OVADIAH),
    (mam_bknas.BS_JONAH, tbn.BK_JONAH),
    (mam_bknas.BS_MICAH, tbn.BK_MIKHAH),
    (mam_bknas.BS_NAXUM, tbn.BK_NAXUM),
    (mam_bknas.BS_XABA, tbn.BK_XABA),
    (mam_bknas.BS_TSEF, tbn.BK_TSEF),
    (mam_bknas.BS_XAGGAI, tbn.BK_XAGGAI),
    (mam_bknas.BS_ZEKHAR, tbn.BK_ZEKHAR),
    (mam_bknas.BS_MALAKHI, tbn.BK_MALAKHI),
    (mam_bknas.BS_PSALMS, tbn.BK_PSALMS),
    (mam_bknas.BS_PROV, tbn.BK_PROV),
    (mam_bknas.BS_JOB, tbn.BK_JOB),
    (mam_bknas.BS_SONG, tbn.BK_SONG),
    (mam_bknas.BS_RUTH, tbn.BK_RUTH),
    (mam_bknas.BS_LAMENT, tbn.BK_LAMENT),
    (mam_bknas.BS_QOHELET, tbn.BK_QOHELET),
    (mam_bknas.BS_ESTHER, tbn.BK_ESTHER),
    (mam_bknas.BS_DANIEL, tbn.BK_DANIEL),
    (mam_bknas.BS_EZRA, tbn.BK_EZRA),
    (mam_bknas.BS_NEXEM, tbn.BK_NEXEM),
    (mam_bknas.BS_FST_CHR, tbn.BK_FST_CHR),
    (mam_bknas.BS_SND_CHR, tbn.BK_SND_CHR),
)
BK39ID_TO_MAM_HBNP = dict(map(_flip, _PAIRS))
MAM_HBNP_TO_BK39ID = dict(_PAIRS)
