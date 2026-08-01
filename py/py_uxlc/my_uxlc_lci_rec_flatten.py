"""Exports flatten_one"""

import py_uxlc.my_uxlc_lci_rec as lci_rec
import py_uxlc.my_uxlc_cvp as cvp


def flatten(lcir):
    """Make one lci_rec more suitable for JSON export"""
    cvp_range = lci_rec.get_cvp_range(lcir)
    cvp_range_f = _flatten_cvp_range(cvp_range)
    coli_range = lci_rec.get_coli_range(lcir)
    coli_range_f = _flatten_coli_range(coli_range)
    retval = {
        "page": lci_rec.get_pgid(lcir),
        **coli_range_f,
        "bkid": lci_rec.get_bkid(lcir),
        **cvp_range_f,
        "note": lci_rec.get_note(lcir),
    }
    return retval


def _flatten_cvp_range(cvp_range):
    cvp_start = cvp_range and cvp_range[0]
    cvp_stop = cvp_range and cvp_range[1]
    start2 = _flatten_cvp(("startc", "startv", "startp"), cvp_start)
    stop2 = _flatten_cvp(("stopc", "stopv", "stopp"), cvp_stop)
    return {**start2, **stop2}


def _flatten_coli_range(coli_range):
    coli_start = coli_range and coli_range[0]
    coli_stop = coli_range and coli_range[1]
    start2 = _flatten_coli(("startco", "startli"), coli_start)
    stop2 = _flatten_coli(("stopco", "stopli"), coli_stop)
    return {**start2, **stop2}


def _flatten_cvp(keys, the_cvp):
    if the_cvp is None:
        full_vals = (None,) * len(keys)
    else:
        full_vals = *cvp.chapnver(the_cvp), cvp.get_povr(the_cvp)
    return dict(zip(keys, full_vals))


def _flatten_coli(keys, the_coli):
    if the_coli is None:
        full_vals = (None,) * len(keys)
    else:
        full_vals = the_coli
    return dict(zip(keys, full_vals))
