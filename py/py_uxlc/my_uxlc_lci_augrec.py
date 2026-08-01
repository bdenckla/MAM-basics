"""Exports augment_lci_recs, flatten_many2, ..."""

import py_uxlc.my_uxlc_lci_rec as lci_rec
import py_uxlc.my_uxlc_bibdist as bibdist
import py_uxlc.my_uxlc_verlen as verlen
import py_uxlc.my_uxlc_lci_rec_flatten as lci_rec_flatten


def augment_lci_recs(uxlc, lci_recs):
    """Augment page break records with bibdists"""
    ctx = {"uxlc": uxlc, "page_lengths": {}, "prev_lci_rec": None}
    lci_augrecs = tuple(_make(ctx, lcir) for lcir in lci_recs)
    return lci_augrecs, ctx["page_lengths"]


def flatten_many2(lci_augrecs):
    """Make an augmented break more suitable for JSON export"""
    return tuple(map(_flatten_one, lci_augrecs))


def flatten_page_lengths(page_lengths):
    """Flatten page lengths for output to JSON"""
    return tuple(map(_flatten_page_length, page_lengths.items()))


def get_pgid(lci_augrec):
    """Get page ID"""
    return lci_rec.get_pgid(get_lci_rec(lci_augrec))


def get_bkid(lci_augrec):
    """Get book ID"""
    return lci_rec.get_bkid(get_lci_rec(lci_augrec))


def get_cvp_range(lci_augrec):
    """Get cvp range (cvp: chapter, verse, and part of verse)"""
    return lci_rec.get_cvp_range(get_lci_rec(lci_augrec))


def get_note(lci_augrec):
    """Get note (if any)"""
    return lci_rec.get_note(get_lci_rec(lci_augrec))


def get_cvp_start(lci_augrec):
    """Get the start of the cvp range"""
    return lci_rec.get_cvp_start(get_lci_rec(lci_augrec))


def get_coli_range(lci_augrec):
    """Tell whether the lci_augrec has column & line entries."""
    return lci_rec.get_coli_range(get_lci_rec(lci_augrec))


def get_lci_rec(lci_augrec):
    """Get LC Index record."""
    return lci_augrec["_lciar_lci_rec"]


def get_bibdists_stasto(lci_augrec):
    """Get start and stop bibdists."""
    return lci_augrec["_lciar_bibdists"]


def get_bibdist_start(lci_augrec):
    """Get bibdist from start of page to the start of this lci_augrec."""
    return get_bibdists_stasto(lci_augrec)[0]


def get_bibdist_stop(lci_augrec):
    """Get bibdist from start of page to the stop of this lci_augrec."""
    return get_bibdists_stasto(lci_augrec)[1]


def is_real(lci_augrec):
    """
    Tell whether this lci_augrec is for a Biblical chunk,
    as opposed to a Masoretic list or some other non-Biblical chunk of text.
    """
    bkid = get_bkid(lci_augrec)
    return bkid is not None


def _get_verlens_stasto(lci_augrec):
    """Get start and stop verlens."""
    return lci_augrec["_lciar_verlens"]


def _flatten_one(lci_augrec):
    lci_rec_f = lci_rec_flatten.flatten(get_lci_rec(lci_augrec))
    bibdists_f = _flatten_bibdists(get_bibdists_stasto(lci_augrec))
    verlens_f = _flatten_verlens(_get_verlens_stasto(lci_augrec))
    lci_augrec_f = {**lci_rec_f, **bibdists_f, **verlens_f}
    return lci_augrec_f


def _flatten_verlens(verlens_stasto):
    vrl_start, vrl_stop = verlens_stasto
    return {
        "startl": vrl_start,
        "stopl": vrl_stop,
    }


def _flatten_bibdists(bibdists):
    bd_start, bd_stop = bibdists
    bd_start_rk = bibdist.rekey(bd_start, "start_word_count")
    bd_stop_rk = bibdist.rekey(bd_stop, "stop_word_count")
    return {**bd_start_rk, **bd_stop_rk}


def _flatten_page_length(page_and_length):
    pgid, the_bibdist = page_and_length
    the_bibdist_rk = bibdist.rekey(the_bibdist, "word_count")
    return {"page": pgid, **the_bibdist_rk}


def _make(ctx, lcir):
    ctx["prev_lci_rec"] = lcir
    return {
        "_lciar_lci_rec": lcir,
        "_lciar_bibdists": _get_bibdists(ctx, lcir),
        "_lciar_verlens": _get_verlens(ctx, lcir),
    }


def _get_bibdists(ctx, lcir):
    bkid = lci_rec.get_bkid(lcir)
    if bkid is None:
        return bibdist.make_none(), bibdist.make_none()
    pgid = lci_rec.get_pgid(lcir)
    cvp_range = lci_rec.get_cvp_range(lcir)
    the_bibdist = bibdist.calc(ctx["uxlc"], bkid, cvp_range)
    ctxp = ctx["page_lengths"]
    if pgid not in ctxp:
        ctxp[pgid] = bibdist.make_zero()
    bibdist_start = ctxp[pgid]
    bibdist_stop = bibdist.add(bibdist_start, the_bibdist)
    ctxp[pgid] = bibdist_stop
    return bibdist_start, bibdist_stop


def _get_verlens(ctx, lcir):
    bkid = lci_rec.get_bkid(lcir)
    if bkid is None:
        return None, None
    cvp_start, cvp_stop = lci_rec.get_cvp_range(lcir)
    vrl_start = verlen.get_verlen(ctx["uxlc"], bkid, cvp_start)
    vrl_stop = verlen.get_verlen(ctx["uxlc"], bkid, cvp_stop)
    return vrl_start, vrl_stop
