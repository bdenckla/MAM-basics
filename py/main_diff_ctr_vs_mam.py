""" Exports main """

import json
from itertools import zip_longest
from pydiff_ctr_vs_mam.massage_ctr_verse import massage_ctr_verse
from pydiff_ctr_vs_mam.massage_mpp_verse import massage_mpp_verse
from pycmn import my_diffs
from pycmn import uni_heb as uh
from pycmn import read_books_from_mam_parsed_plus as plus
from pycmn import file_io
from pycmn import bib_locales as tbn


def _make_dump(diff):
    # Make a diff suitable for dumping to a JSON file.
    return diff


def _read_ctr_bk39s(books_of_sec):
    ctr_bk39s = {}
    for bkid in books_of_sec:
        if bkid not in _CTR_BOOKS:
            ctr_bk39s[bkid] = None
            continue
        osdf = tbn.ordered_short_dash_full_39(bkid)
        ctr_path = f"in/chabad-ctr/{osdf}.json"
        with open(ctr_path, encoding="utf-8") as ctr_json_in_fp:
            ctr_data = json.load(ctr_json_in_fp)
        ctr_bk39s[bkid] = ctr_data
    return ctr_bk39s


def _massage_ctr_book(ctr_book_raw):
    return ctr_book_raw


def _chnu_colon_vrnu(bcvt):
    int_chnu, int_vrnu = tbn.bcvt_get_chnu_vrnu(bcvt)
    return f"{int_chnu}:{int_vrnu}"


def _get_book_diffs(ctr_book, mpp_book):
    diffs_struct = _diffs_struct_mk()
    for bcvt, mpp_verse_body_raw in mpp_book["verses_plus"].items():
        ccv = _chnu_colon_vrnu(bcvt)
        if ccv not in ctr_book["verses"]:
            continue
        ctr_verse_body_raw = ctr_book["verses"][ccv]
        ctr_words = massage_ctr_verse(ctr_verse_body_raw)
        mpp_words = massage_mpp_verse(mpp_verse_body_raw)
        zl = list(zip_longest(ctr_words, mpp_words))
        for i, (ctr_word, mpp_word) in enumerate(zl):
            if ctr_word != mpp_word:
                diff = _get_word_diff(bcvt, i, ctr_word, mpp_word)
                diffs_struct["diffs_list"].append(diff)
    return diffs_struct


def _get_word_diff(bcvt, i, ctr_word, mpp_word):
    return {
        "bcvi": _bcvj(bcvt, i),
        "ctr": ctr_word,
        "mam": mpp_word,
        "refined": _refine(ctr_word, mpp_word),
    }


def _refine(ctr_word, mpp_word):
    ctr_shunnas = uh.t_shunnas(ctr_word)
    mpp_shunnas = uh.t_shunnas(mpp_word)
    return my_diffs.get(ctr_shunnas, mpp_shunnas)


def _bcvj(bcvt, i):
    """Convert a bcvt and a 0-based index to a bcvj string, where j=i+1."""
    return f"{tbn.short_bcv_of_bcvt(bcvt)}.{i+1}"


_CTR_BOOKS = (tbn.BK_PSALMS, tbn.BK_PROV)


def _do_one_section_of_tanakh(secid):
    sec_diffs = _diffs_struct_mk()
    if secid != tbn.SEC_SIF_EM:
        return sec_diffs
    books_of_sec = tbn.bk39s_of_sec(secid)
    books_mpp = plus.read_parsed_plus_bk39s(books_of_sec)
    books_ctr = _read_ctr_bk39s(books_of_sec)
    for bkid in books_of_sec:
        if bkid not in _CTR_BOOKS:
            continue
        ctr_book_raw = books_ctr[bkid]
        mpp_book_raw = books_mpp[bkid]
        ctr_book = _massage_ctr_book(ctr_book_raw)
        mpp_book = mpp_book_raw
        bk_diffs = _get_book_diffs(ctr_book, mpp_book)
        _diffs_struct_extend(sec_diffs, bk_diffs)
    return sec_diffs


def _diffs_struct_dump(all_diffs):
    the_dump = tuple(map(_make_dump, all_diffs["diffs_list"]))
    file_io.json_dump_to_file_path(the_dump, "out/diff_ctr_mam.json")


def _diffs_struct_mk():
    return {"diffs_list": []}


def _diffs_struct_extend(accum_ds, new_ds):
    accum_ds["diffs_list"].extend(new_ds["diffs_list"])


def main():
    """Compute differences between CTR & MAM"""
    all_diffs = _diffs_struct_mk()
    for secid in tbn.ALL_SECIDS:
        sec_diffs = _do_one_section_of_tanakh(secid)
        _diffs_struct_extend(all_diffs, sec_diffs)
    _diffs_struct_dump(all_diffs)


if __name__ == "__main__":
    main()
