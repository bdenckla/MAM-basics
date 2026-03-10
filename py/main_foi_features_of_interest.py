"""
Identify and catalog features of interest (FOI) in the MAM corpus.

Scans MAM-parsed-plus for linguistic and textual patterns (e.g. ketiv-qere
pairs, unusual cantillation) and writes the findings to JSON. Supports
parallel and single-threaded execution modes.

Usage:
    [program] --foi args-foi-kq-2
    [program] --single-threaded
    [program] --foi args-foi-kq-2 --single-threaded
"""

import argparse
import multiprocessing

from pyfoi import foi_finals
from pyfoi import foi_struct as fct
from pyfoi.foi_find_wt_fois_for_1_bk import find_wt_fois_for_1_bk

from pyfoi import foiz_wt_alef_vav as foi_alef_vav
from pyfoi import foiz_wt_kq_1 as foi_kq_1
from pyfoi import foiz_wt_kq_2 as foi_kq_2
from pyfoi import foiz_wt_oleh_yored as foi_oleh_yored
from pyfoi import foiz_wt_sec_merk_and_friends as foi_sec_merk
from pyfoi import foiz_wt_tsinnorit as foi_tsinnorit
from pyfoi import foiz_wt_pasoleg_1 as foi_pasoleg_1
from pyfoi import foiz_wt_pasoleg_2 as foi_pasoleg_2
from pyfoi import foiz_wt_poetic_len as foi_poetic_len
from pyfoi import foiz_wt_poetic_sh as foi_poetic_sh
from pyfoi import foiz_wt_qamats_var as foi_qamats_var
from pyfoi import foiz_wt_quick_brown as foi_quick_brown
from pyfoi import foiz_wt_rare_tmpls as foi_rare_tmpls
from pyfoi import foiz_wt_rev_mug as foi_rev_mug
from pyfoi import foiz_wt_slh_word as foi_slh_word
from pyfoi import foiz_wt_mtgmtg as foi_mtgmtg
from pyfoi import foiz_wt_unicode as foi_unicode

from pycmn import read_books_from_mam_parsed_plus as plus
from pycmn import bib_locales as tbn


def _do_wikitext_features_of_interest(foi, single_threaded, books_mpp, all_fois):
    fois_funs = _fois_funs_for_wt(foi)
    the_arg_triple = [(fois_funs, books_mpp[bkid], bkid) for bkid in tbn.ALL_BK39_IDS]
    out_for_all_bks = {}
    if single_threaded:
        for bkid, out_for_this_bk in map(find_wt_fois_for_1_bk, the_arg_triple):
            out_for_all_bks[bkid] = out_for_this_bk
    else:
        with multiprocessing.Pool(processes=8) as pool:
            for bkid, out_for_this_bk in pool.imap_unordered(
                find_wt_fois_for_1_bk, the_arg_triple
            ):
                out_for_all_bks[bkid] = out_for_this_bk
    for bkid in tbn.ALL_BK39_IDS:
        fct.record_fois_for_1_bk(all_fois, out_for_all_bks[bkid])


def _fois_funs_for_wt(clargs_foi):
    if clargs_foi:
        return [_WIKITEXT_FOIS_FUN_FOR_CLARG[clargs_foi]]
    return _WIKITEXT_FOIS_FNS


def _make_intermediates(foi, single_threaded, books_mpp):
    all_fois = fct.make_empty_all_fois()
    _do_wikitext_features_of_interest(foi, single_threaded, books_mpp, all_fois)
    return all_fois


_WIKITEXT_FOIS_FUN_FOR_CLARG = {
    "args-foi-alef-vav": foi_alef_vav.find_fois_wt,
    "args-foi-kq-1": foi_kq_1.find_fois_wt,
    "args-foi-kq-2": foi_kq_2.find_fois_wt,
    "args-foi-oleh-yored": foi_oleh_yored.find_fois_wt,
    "args-foi-sec-merk": foi_sec_merk.find_fois_wt,
    "args-foi-tsinnorit": foi_tsinnorit.find_fois_wt,
    "args-foi-pasoleg-1": foi_pasoleg_1.find_fois_wt,
    "args-foi-pasoleg-2": foi_pasoleg_2.find_fois_wt,
    "args-foi-poetic-len": foi_poetic_len.find_fois_wt,
    "args-foi-poetic-sh": foi_poetic_sh.find_fois_wt,
    "args-foi-qamats-var": foi_qamats_var.find_fois_wt,
    "args-foi-quick-brown": foi_quick_brown.find_fois_wt,
    "args-foi-rare-tmpls": foi_rare_tmpls.find_fois_wt,
    "args-foi-rev-mug": foi_rev_mug.find_fois_wt,
    "args-foi-slh-word": foi_slh_word.find_fois_wt,
    "args-foi-mtgmtg": foi_mtgmtg.find_fois_wt,
    "args-foi-unicode": foi_unicode.find_fois_wt,
}
_WIKITEXT_CLARGS = list(_WIKITEXT_FOIS_FUN_FOR_CLARG.keys())
_WIKITEXT_FOIS_FNS = list(_WIKITEXT_FOIS_FUN_FOR_CLARG.values())


def almost_main(foi=None, single_threaded=False):
    """Collect features of interest from MAM."""
    books_mpp = plus.read_parsed_plus_bk39s()
    all_fois = _make_intermediates(foi, single_threaded, books_mpp)
    foi_finals.write(foi, all_fois)


def main():
    """Collect features of interest from MAM."""
    parser = argparse.ArgumentParser()
    foi_choices = _WIKITEXT_CLARGS  # CLARG: command-line arg
    parser.add_argument("--foi", choices=foi_choices)
    parser.add_argument("--single-threaded", action="store_true")
    clargs = parser.parse_args()
    almost_main(foi=clargs.foi, single_threaded=clargs.single_threaded)


if __name__ == "__main__":
    main()
