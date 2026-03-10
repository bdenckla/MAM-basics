from pycmn import bib_locales as tbn
from py_misc import mam_csv_in
from pycmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from pycmn import mam_bknas
from pycmn.my_utils import sum_of_map
from pycmn.my_utils import sl_map
from pycmn.my_utils import dv_map


def get_chapter_plans(book_plan):
    # he_bn_sbn: Hebrew book name and sub-book name (a pair) (aka mam_he_book_name_pair)
    he_bn_sbn, he_chnus = book_plan
    return sl_map((_get_chapter_plan, he_bn_sbn), he_chnus)


def get_book_plans(args_bkid=None, args_secid=None):
    if args_bkid:
        assert args_secid is None, args_secid
        assert args_bkid in tbn.ALL_BK39_IDS, args_bkid
        mam_he_book_name_pair = mbkn_a_sbkn.BK39ID_TO_MAM_HBNP[args_bkid]
        plan = sum_of_map((_get_zoo_book_plans, mam_he_book_name_pair), tbn.ALL_SECIDS)
        assert plan, args_bkid
        return plan
    if args_secid:
        assert args_secid in tbn.ALL_SECIDS, args_secid
        secids = [args_secid]
    else:
        secids = tbn.ALL_SECIDS
    return sum_of_map(_get_book_plans_for_one_section, secids)


def _get_zoo_book_plans(mam_he_book_name_pair, secid):  # zero or one
    light_books = mam_csv_in.read_section_from_csv_lightly(secid)
    if light_book := light_books.get(mam_he_book_name_pair):
        return [(mam_he_book_name_pair, _get_he_chnus(light_book))]
    return []


def _get_book_plans_for_one_section(secid):
    light_books = mam_csv_in.read_section_from_csv_lightly(secid)
    out = dv_map(_get_he_chnus, light_books)
    return out.items()


def _get_he_chnus(light_book):
    return list(light_book.keys())


def _get_chapter_plan(he_bn_sbn, he_chnu):
    # he_bn_sbn: Hebrew book name and sub-book name (a pair) (aka mam_he_book_name_pair)
    bk39na = mam_bknas.he_bk39_name(*he_bn_sbn)
    bk39na_and_he_chnu = "_".join((bk39na, he_chnu))  # יהושע_א
    title = "/".join((bk39na_and_he_chnu, "טעמים"))  # 'יהושע_א/טעמים'
    return he_chnu, title
