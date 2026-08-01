"""
Exports:
    read_in
    read_lci_recs_dot_json
    get_lci_augrecs
    get_lci_augrecs_real
    get_page_lengths
    get_book_order
"""

import json
import py_uxlc.my_uxlc_lci_rec as lci_rec
import py_uxlc.my_uxlc_lci_augrec as lci_augrec
import wlc_paths


def read_in(uxlc):
    """Read in page break info"""
    lcirs = _get_lcirs_at_high_resolution()
    lciars, page_lens = lci_augrec.augment_lci_recs(uxlc, lcirs)
    lciars_r = tuple(filter(lci_augrec.is_real, lciars))
    book_order = _get_book_order(lciars_r)
    pbi = {
        "_pbi_lci_augrecs": lciars,
        "_pbi_lci_augrecs_real": lciars_r,
        "_pbi_page_lengths": page_lens,
        "_pbi_book_order": book_order,
    }
    return pbi


def get_lci_augrecs(pbi):
    """Return the LC Index augmented records."""
    return pbi["_pbi_lci_augrecs"]


def get_lci_augrecs_real(pbi):
    """
    Return the LC Index augmented records that are real, i.e.
    the ones that are for Biblical chunks, not Masoretic chunks.
    """
    return pbi["_pbi_lci_augrecs_real"]


def get_page_lengths(pbi):
    """Get the lengths of all pages."""
    return pbi["_pbi_page_lengths"]


def get_book_order(pbi):
    """
    Get the map from book ID to book number, where
    book number reflects the order of books as they appear
    in the LC. I particular, the two books of Chronicles
     are  in a somewhat expected place (they are not final).
    """
    return pbi["_pbi_book_order"]


def read_lci_recs_dot_json():
    """Read in lci_recs.json, raw"""
    lci_recs_path = wlc_paths.data_dir() / "lci_recs.json"
    with open(lci_recs_path, encoding="utf-8") as lci_recs_json_in_fp:
        return json.load(lci_recs_json_in_fp)


def _get_lcirs_at_high_resolution():
    lci_recs_dot_json = read_lci_recs_dot_json()
    lci_recs = lci_rec.unflatten_many(lci_recs_dot_json["body"])
    return lci_recs


def _get_book_order(lci_augrecs_real):
    bknu = 1  # one-based (doesn't have to be)
    book_order = {}
    for lcia_r in lci_augrecs_real:
        bkid = lci_augrec.get_bkid(lcia_r)
        if bkid in book_order:
            continue
        book_order[bkid] = bknu
        bknu += 1
    return book_order
