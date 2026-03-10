""" Exports add_heb_bcv """

import re
from pycmn import hebrew_verse_numerals as hvn
from pycmn import bib_locales as tbn
from pycmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from pycmn import mam_bknas as mbknas


def add_heb_bcv(go_go_diff):
    """Add Hebrew bcv as "heb_bcv" """
    bcv_str = go_go_diff["bcv"]
    bcv_patt = r"([A-z0-9][A-z]?)" + r"(\d+)" + ":" + r"(\d+)"
    match = re.fullmatch(bcv_patt, bcv_str)
    bcv_book_name_short, bcv_chnu_str, bcv_vrnu_str = match.groups()
    bcv_chnu_int = int(bcv_chnu_str)
    bcv_vrnu_int = int(bcv_vrnu_str)
    he_chnu = hvn.INT_TO_STR_DIC[bcv_chnu_int]
    he_vrnu = hvn.INT_TO_STR_DIC[bcv_vrnu_int]
    book_name_std = tbn.std_from_short(bcv_book_name_short)
    mam_he_book_name_pair = mbkn_a_sbkn.BK39ID_TO_MAM_HBNP[book_name_std]
    he_bk39na = mbknas.he_bk39_name(*mam_he_book_name_pair)
    heb_bcv_str = f"{he_bk39na} {he_chnu},{he_vrnu}"
    return {**go_go_diff, "heb_bcv": heb_bcv_str}
