"""Plan Wikisource chapter downloads from book metadata without reading inputs."""

from mb_cmn import bib_locales as tbn
from mb_cmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from mb_cmn import mam_bknas
from mb_cmn import hebrew_verse_numerals as hvn
from mb_cmn.my_utils import sum_of_map
from mb_cmn.my_utils import sl_map
from ws.ws_chapter_counts import BOOK39_CHAPTER_COUNTS


def get_chapter_plans(book_plan):
    # he_bn_sbn: Hebrew book name and sub-book name (a pair) (aka mam_he_book_name_pair)
    he_bn_sbn, he_chnus = book_plan
    return sl_map((_get_chapter_plan, he_bn_sbn), he_chnus)


def get_book_plans(args_bkid=None, args_secid=None):
    if args_bkid:
        assert args_secid is None, args_secid
        assert args_bkid in tbn.ALL_BK39_IDS, args_bkid
        return [_get_book_plan(args_bkid)]
    if args_secid:
        assert args_secid in tbn.ALL_SECIDS, args_secid
        secids = [args_secid]
    else:
        secids = tbn.ALL_SECIDS
    return sum_of_map(_get_book_plans_for_one_section, secids)


def _get_book_plans_for_one_section(secid):
    return sl_map(_get_book_plan, tbn.bk39s_of_sec(secid))


def _get_book_plan(bk39id):
    he_bn_sbn = mbkn_a_sbkn.BK39ID_TO_MAM_HBNP[bk39id]
    he_chnus = [
        hvn.INT_TO_STR_DIC[chapter]
        for chapter in range(1, BOOK39_CHAPTER_COUNTS[bk39id] + 1)
    ]
    return he_bn_sbn, he_chnus


def _get_chapter_plan(he_bn_sbn, he_chnu):
    # he_bn_sbn: Hebrew book name and sub-book name (a pair) (aka mam_he_book_name_pair)
    bk39na = mam_bknas.he_bk39_name(*he_bn_sbn)
    bk39na_and_he_chnu = "_".join((bk39na, he_chnu))  # יהושע_א
    title = "/".join((bk39na_and_he_chnu, "טעמים"))  # 'יהושע_א/טעמים'
    return he_chnu, title
