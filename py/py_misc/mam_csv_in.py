"""
Exports:
    read_section_from_csv_lightly
    csv_path
"""

import csv
import collections

from pycmn import my_utils
from pycmn import bib_locales as tbn
from pycmn import mam_bknas
from pyws import ws_tmpl_n_tag_parser as ttp
from pycmn.minirow import Minirow


def read_section_from_csv_lightly(secid, mam_info=None):
    """Read a single section "lightly" (without much processing)"""
    light_books_out = {}
    _read_csv_lightly(secid, light_books_out, mam_info)
    return light_books_out


def csv_path(secid, alt_mam_dir=None):
    """Return path to CSV file for the named section."""
    csv_name = _MAM_CSV_NAME[secid]
    mam_dir = alt_mam_dir or "in/mam-go"
    return mam_dir + "/" + csv_name


_ROW = collections.namedtuple("_ROW", "A, B, C, D, E")
_MAM_CSV_NAME = {
    secid: f"{tbn.ORDERED_SHORT_SECTION_CODE_DASH_SECID[secid]}.csv"
    for secid in tbn.ALL_SECIDS
}


def _read_csv_lightly(secid, io_light_books, mam_info=None):
    # he_pverse_pnum: Hebrew pseudo-verse pseudo-numeral
    # We call it a pseudo-numeral because it is not always a real Hebrew numeral:
    #    it can be 0 or תתת (zero or triple-tav)
    # We call it a pseudo-verse because it is not always a real verse:
    #    it can be
    #       chapter-start contents (pnum 0) or
    #       chapter-end contents (pnum תתת)
    alt_mam_dir = mam_info and mam_info["mi-csv_dir"]
    the_csv_path = csv_path(secid, alt_mam_dir)
    with open(the_csv_path, encoding="utf-8") as csv_in_fp:
        for row in map(_ROW._make, csv.reader(csv_in_fp)):
            skip_hccs = mam_info and mam_info.get("mi-skip_hard_c_cells")
            light_keys, minirow = _process_one_row_lightly(row, skip_hccs)
            he_bn_sbn, he_chnu, he_pverse_pnum = light_keys
            if he_pverse_pnum == "0":
                if he_chnu == "א":
                    my_utils.init_at_key(io_light_books, he_bn_sbn, {})
                my_utils.init_at_key(io_light_books[he_bn_sbn], he_chnu, {})
            my_utils.init_at_key(
                io_light_books[he_bn_sbn][he_chnu], he_pverse_pnum, minirow
            )


def _process_one_row_lightly(row, skip_hard_c_cells):
    he_bn_sbn, he_chnu = _he_bn_sbn_chnu(row.A)
    light_keys = he_bn_sbn, he_chnu, row.B
    c_parsed = _parse_cell_c(light_keys, row.C, skip_hard_c_cells)
    d_parsed = ttp.parse(row.D)
    e_parsed = ttp.parse(row.E)
    return light_keys, Minirow(c_parsed, d_parsed, e_parsed)


def _parse_cell_c(light_keys, cell_c, skip_hard_c_cells):
    # If the cell for column C is too hard to parse in this particular row
    if skip_hard_c_cells and light_keys in _LIGHT_KEYS_WITH_HARD_CELL_C:
        return ({"unparseable": True},)
    return ttp.parse(cell_c)


_LIGHT_KEYS_WITH_HARD_CELL_C = set(
    (  # "hard" meaning "too hard to parse"
        # (miqra_book_names.BS_EXODUS, str('טו'), 'תתת'),
        (mam_bknas.BS_DEUTER, str("לב"), "תתת"),
        (mam_bknas.BS_JOSHUA, str("יב"), "תתת"),
        (mam_bknas.BS_JUDGES, str("ה"), "תתת"),
        (mam_bknas.BS_SND_SAM, str("כב"), "תתת"),
        (mam_bknas.BS_QOHELET, str("ג"), "תתת"),
        (mam_bknas.BS_ESTHER, str("ט"), "תתת"),
        (mam_bknas.BS_FST_CHR, str("טז"), "תתת"),
    )
)


def _he_bn_sbn_chnu(cell_a):
    # See "Note on _he_bn_sbn_chnu" below.
    he_book_name, he_chap_id = cell_a.split("/")
    maybe_sbncn = he_chap_id.split()
    if len(maybe_sbncn) == 2:
        sbncn = maybe_sbncn
        return (he_book_name, sbncn[0]), sbncn[1]
    assert len(maybe_sbncn) == 1
    chap_num = he_chap_id
    return (he_book_name, None), chap_num


# Note on _he_bn_sbn_chnu
#
# An input of 'book24/sub_book chap_num', e.g. 'ספר שמואל/שמ"א ג'
#    gives an output of bk24, sub_book, chap_num
#    e.g. (str('ספר שמואל'), str('שמ"א')), str('ג')
# An input of 'book24/chap_num', e.g. 'ספר בראשית/ג'
#    gives an output of bk24, None, chap_num
#    e.g. str('ספר בראשית'), None, str('ג')
# Below, he_chap_id is something like 'ג' or 'שמ"א ג'.
# I.e. it can be a he_cn_str (Hebrew cn string)
#    where cn means chapter number.
# Or, it can be a he_sbncn_str (Hebrew sbncn string)
#    where sbncn means sub-book name and chapter num.
# If he_chap_id is
#    'ג', that means chapter 3
#     of a book without sub-books, like Genesis.
# If he_chap_id is
#    'שמ"א ג', that means chapter 3
#    of the the sub-book 'שמ"א' of the book of Samuel.
#

# The following 5 bk24s are the only ones with sub-books:
#    Samuel, Kings, & Chronicles (2 sub-books each)
#    Ezra-Nehemiah (2 sub-books)
#    The 12 minor prophets (12 sub-books)
# Note that names of the sub-books of Samuel, Kings, & Chronicles
#    are not just 'א' or 'ב'.
# The names of those sub-books also contain their bk24 name,
#    in an abbreviated form.
# E.g. the 1st half of Samuel is notated as 'שמ"א', not just 'א'.
# I.e. 'שמ"א' is an abbreviated form of 'שמואל א'.
# Considering cell A as a whole, this gives cell A some redundancy,
#    for such books.
# E.g. cell A might be 'ספר שמואל/שמ"א ג' (sefer shmuel/shm1 3)
#    (some redundancy).
# Or, cell A might simply be 'ספר בראשית/ג' (sefer bereshit/3)
#    (no redundancy).
# Such redundancy is not necessarily a bad thing.
# For one thing, for bk24s with sub-books, it means you can
#    just ignore the bk24 name, in many contexts, since the
#    sub-book name is unique.
