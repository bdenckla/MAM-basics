""" Exports add_eng_bcv """

import re
from pycmn import hebrew_verse_numerals as hvn
from pycmn import bib_locales as tbn
from pycmn import mam_bknas_and_std_bknas as mbkn_a_sbkn
from pycmn import mam_bknas as mbknas


def add_eng_bcv(change_log_entry):
    """Add English short bcv as "where2" """
    where = _unspace(change_log_entry.where)
    heb_num_patt = r"(ק?[א-צ]?[א-צ])"
    hbcv_patt = r'([א-ת"]+) ' + heb_num_patt + "[, ]" + heb_num_patt
    if match := re.fullmatch(hbcv_patt, where):
        hbcv_triple = match.groups()
        assert len(hbcv_triple) == 3
        book_name_std = _HE_NO_SPACE_NAME_TO_STD_NAME[hbcv_triple[0]]
        chnu_int = hvn.STR_TO_INT_DIC[hbcv_triple[1]]
        vrnu_int = hvn.STR_TO_INT_DIC[hbcv_triple[2]]
        bcv = book_name_std, chnu_int, vrnu_int
        short_bcv = tbn.short_bcv(bcv)
    else:
        short_bcv = None
    return {
        "when": change_log_entry.when,
        "who": change_log_entry.who,
        "where": change_log_entry.where,
        "where2": short_bcv,
        "what": change_log_entry.what,
        "what_x_heb": change_log_entry.what_x_heb,
        "what_y_heb": change_log_entry.what_y_heb,
    }


def _unspace(where):
    for space, unspace in _UNSPACE_DIC.items():
        if where.startswith(space):
            return where.replace(space, unspace)
    return where


def _make_he_no_space_to_std_dic():
    items = mbkn_a_sbkn.BK39ID_TO_MAM_HBNP.items()
    no_space_b39s = {
        mbknas.he_bk39_name(*mam_he_book_name_pair): bkid
        for bkid, mam_he_book_name_pair in items
        if " " not in mbknas.he_bk39_name(*mam_he_book_name_pair)
    }
    # subs = {
    #     str('שמ"א'): '1Samuel',
    #     str('שמ"ב'): '2Samuel',
    #     str('מל"א'): '1Kings',
    #     str('מל"ב'): '2Kings',
    #     str('עבדיה'): 'Obadiah',
    #     str('דה"א'): '1Chronicles',
    #     str('דה"ב'): '2Chronicles'
    # }
    sub_names = {
        pair[1]: std for std, pair in items if pair[1] and pair[1] not in no_space_b39s
    }
    song_of_songs = {'שיר"ם': tbn.BK_SONG}
    return {**no_space_b39s, **sub_names, **song_of_songs}


def _make_unspace_dic():
    mam_he_book_name_pairs = mbkn_a_sbkn.BK39ID_TO_MAM_HBNP.values()
    # unspace_dic = {
    #     'שמואל א': 'שמ"א',
    #     'שמואל ב': 'שמ"ב',
    #     'מלכים א': 'מל"א',
    #     'מלכים ב': 'מל"ב',
    #     'עובדיה': 'עבדיה',
    #     'דברי הימים א': 'דה"א',
    #     'דברי הימים ב': 'דה"ב'
    # }
    unspace_dic = {
        mbknas.he_bk39_name(*mam_he_book_name_pair): mam_he_book_name_pair[1]
        for mam_he_book_name_pair in mam_he_book_name_pairs
        if mam_he_book_name_pair[1]
        and mbknas.he_bk39_name(*mam_he_book_name_pair) != mam_he_book_name_pair[1]
    }
    song_of_songs = {"שיר השירים": 'שיר"ם'}
    return {**unspace_dic, **song_of_songs}


_UNSPACE_DIC = _make_unspace_dic()
_HE_NO_SPACE_NAME_TO_STD_NAME = _make_he_no_space_to_std_dic()
