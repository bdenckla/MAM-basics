"""Exports make, flatten_many1, ..."""

import re
import py_uxlc.my_uxlc_cvp as cvp


def make(pgid, bkid, cvp_range, note):
    """Construct an lci_rec with coli_range == None."""
    return _make2((pgid, None), (bkid, cvp_range), note)


def unflatten_many(lci_recs_f):
    """Give structure to flat lci_recs read in from JSON."""
    return tuple(map(_unflatten_one, lci_recs_f))


def get_pgid(lci_rec):
    """Get page ID."""
    return lci_rec["_lcir_concrete"][0]


def get_coli_range(lci_rec):
    """Get coli range (coli: column and line)"""
    return lci_rec["_lcir_concrete"][1]


def get_bkid(lci_rec):
    """Get book ID, e.g. 'Levit'."""
    return lci_rec["_lcir_abstract"][0]


def get_cvp_range(lci_rec):
    """Get cvp range (cvp: chapter, verse, & part of verse)"""
    return lci_rec["_lcir_abstract"][1]


def get_note(lci_rec):
    """Get note (if any)."""
    return lci_rec["_lcir_note"]


def get_cvp_start(lci_rec):
    """Get start of cvp range."""
    cvp_range = get_cvp_range(lci_rec)
    return cvp_range and cvp_range[0]


def get_cvp_stop(lci_rec):
    """Get stop of cvp range."""
    cvp_range = get_cvp_range(lci_rec)
    return cvp_range and cvp_range[1]


def set_povrs(lcir, new_start_povr, new_stop_povr):
    """Refine the "part of verse" field of the start and/or stop"""
    pgid = get_pgid(lcir)
    bkid = get_bkid(lcir)
    cvp_start = get_cvp_start(lcir)
    cvp_stop = get_cvp_stop(lcir)
    note = get_note(lcir)
    new_cvp_start = cvp_start
    new_cvp_stop = cvp_stop
    if new_start_povr:
        new_cvp_start = cvp.set_povr(cvp_start, new_start_povr)
    if new_stop_povr:
        new_cvp_stop = cvp.set_povr(cvp_stop, new_stop_povr)
    new_cvp_range = new_cvp_start, new_cvp_stop
    return make(pgid, bkid, new_cvp_range, note)


def flines(coli_range):
    """
    Return the number of flat lines in a coli (column/line) range,
    assuming 27 lines per column.
    """
    coli_start, coli_stop = coli_range
    co_diff = coli_stop[0] - coli_start[0]
    li_diff = coli_stop[1] - coli_start[1]
    return 27 * co_diff + li_diff + 1


def fline_of_start(coli_range):
    """
    Return the number of flat lines into a page that a coli (column/line)
    range starts at, assuming 27 lines per column.
    """
    coli_start, _coli_stop = coli_range
    co_start, li_start = coli_start
    pre_co_start = co_start - 1
    return 27 * pre_co_start + li_start


def parse_pgid(pgid: str):
    """Parse page ID string into a leaf int and 'A' or 'B'"""
    patt = r"(\d\d\d)([AB])"
    match = re.fullmatch(patt, pgid)
    assert match
    leaf_str, ca_or_cb = match.groups(0)
    leaf_int = int(leaf_str)
    return leaf_int, ca_or_cb


def unparse_pgid(leaf_int, ca_or_cb):
    """Turn a leaf int and an 'A' or 'B' into a string like 007B"""
    return f"{leaf_int:03d}{ca_or_cb}"


def _make2(concrete, abstract, note):
    """Construct an lci_rec."""
    return {"_lcir_concrete": concrete, "_lcir_abstract": abstract, "_lcir_note": note}


def _unflatten_one(lci_rec_f):
    pgid = lci_rec_f["page"]
    coli_range = _unflatten_coli_range(lci_rec_f)
    concrete = pgid, coli_range
    #
    bkid = lci_rec_f["bkid"]
    cvp_range = _unflatten_cvp_range(lci_rec_f)
    abstract = bkid, cvp_range
    #
    note = lci_rec_f["note"]
    #
    return _make2(concrete, abstract, note)


def _unflatten_coli_range(lci_rec_f):
    startco = lci_rec_f["startco"]
    startli = lci_rec_f["startli"]
    stopco = lci_rec_f["stopco"]
    stopli = lci_rec_f["stopli"]
    coli_start = startco, startli
    coli_stop = stopco, stopli
    coli_range_4tuple = *coli_start, *coli_stop
    if not any(coli_range_4tuple):
        return None
    assert all(coli_range_4tuple)
    return coli_start, coli_stop


def _unflatten_cvp_range(lci_rec_f):
    startc = lci_rec_f["startc"]
    startv = lci_rec_f["startv"]
    startp = lci_rec_f["startp"]
    stopc = lci_rec_f["stopc"]
    stopv = lci_rec_f["stopv"]
    stopp = lci_rec_f["stopp"]
    cvp_start = startc, startv, startp
    cvp_stop = stopc, stopv, stopp
    cvp_range_6tuple = *cvp_start, *cvp_stop
    if not any(cvp_range_6tuple):
        return None
    assert all(cvp_range_6tuple)
    return cvp_start, cvp_stop
