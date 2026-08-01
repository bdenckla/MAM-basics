"""Exports prep, estimate, page_and_guesses."""

import py_uxlc.my_uxlc_cvp as cvp
import py_uxlc.my_uxlc_lci_augrec as lci_augrec
import py_uxlc.my_uxlc_lci_rec as lci_rec
import py_uxlc.my_uxlc_bibdist as bibdist
import py_uxlc.my_uxlc_page_break_info as page_break_info
import py_uxlc.my_uxlc as my_uxlc
import mb_cmn.bib_locales as tbn


def prep():
    uxlc = my_uxlc.read_all_books()
    pbi = page_break_info.read_in(uxlc)
    return uxlc, pbi


def estimate(uxlc, pbi, std_bcvp_quad):
    """
    Given the atom specified by std_bcvp_quad (std book, chapter, verse, and atom),
    estimate the location of that atom in the LC (page and "flat line").
    """
    lciar = _find_lciar_for_cite(pbi, std_bcvp_quad)
    page = lci_augrec.get_pgid(lciar)
    fline = _guess_fline(uxlc, pbi, lciar, std_bcvp_quad)
    return page, fline


def page_and_guesses(uxlc, pbi, std_bcvp_quad):
    page, fline_guess = estimate(uxlc, pbi, std_bcvp_quad)
    if fline_guess > 55:
        line_guess = fline_guess - 54
        col_guess = 3
    elif fline_guess >= 28:
        line_guess = fline_guess - 27
        col_guess = 2
    else:
        line_guess = fline_guess
        col_guess = 1
    line_guess_str = f"{line_guess:.1f}"
    fline_guess_str = f"{fline_guess:.1f}"
    return {
        "page": page,
        "fline-guess": fline_guess_str,
        "line-guess": line_guess_str,
        "column-guess": col_guess,
    }


def _find_lciar_for_cite(pbi, citation):
    lci_augrecs = page_break_info.get_lci_augrecs_real(pbi)
    start_mid_stop = _add_mid(0, len(lci_augrecs))
    index = _find(pbi, citation, start_mid_stop)
    lciar = lci_augrecs[index]
    return lciar


def _find(pbi, citation, start_mid_stop):
    start, mid, stop = start_mid_stop
    if _degenerate(start_mid_stop):
        lci_augrecs = page_break_info.get_lci_augrecs_real(pbi)
        _lci_augrec = lci_augrecs[mid]
        assert _cite_is_in_range(pbi, citation, mid)
        return mid
    cmps = _get_comparables(pbi, citation, mid)
    if cmps[0] < cmps[1]:
        new_start_mid_stop = _add_mid(start, mid)
    else:
        new_start_mid_stop = _add_mid(mid, stop)
    return _find(pbi, citation, new_start_mid_stop)


def _degenerate(start_mid_stop):
    start, mid, stop = start_mid_stop
    degen = start == mid
    assert not degen or stop == start + 1
    return degen


def _add_mid(start_incl, stop_excl):
    difference = stop_excl - start_incl
    half_d = difference // 2
    mid = start_incl + half_d
    start_mid_stop = start_incl, mid, stop_excl
    return start_mid_stop


def _get_comparables(pbi, citation, index, stasto="start"):
    lci_augrecs = page_break_info.get_lci_augrecs_real(pbi)
    book_order = page_break_info.get_book_order(pbi)
    ncva_from_cite = _get_ncva1(book_order, citation)
    lciar = lci_augrecs[index]
    ncva_from_lci_rec = _get_ncva2(book_order, lciar, stasto)
    return ncva_from_cite, ncva_from_lci_rec


def _get_ncva1(book_order, citation):
    bkid, chnu, vrnu, atnu = citation
    bknu = book_order[bkid]
    ncva = bknu, chnu, vrnu, atnu
    return ncva


def _get_ncva2(book_order, lciar, stasto_str: str):
    bkid = lci_augrec.get_bkid(lciar)
    cvp_range = lci_augrec.get_cvp_range(lciar)
    stasto_01 = {"start": 0, "stop": 1}
    bknu = book_order[bkid]
    the_cvp = cvp_range[stasto_01[stasto_str]]
    chapnver = cvp.chapnver(the_cvp)
    povr = cvp.get_povr(the_cvp)
    assert isinstance(povr, int)
    ncva = bknu, *chapnver, povr
    return ncva


def _cite_is_in_range(pbi, citation, index):
    cmps = _get_comparables(pbi, citation, index, "stop")
    return cmps[0] <= cmps[1]


def _guess_fline(uxlc, pbi, lciar, std_bcvp_quad):
    sd_fr_p0_to_cite = _sd_fr_p0_to_cite(uxlc, lciar, std_bcvp_quad)  # E.g. 270
    sd_fr_p0_to_p1 = _sd_fr_p0_to_p1(pbi, lciar)  # E.g. 300
    sd_fr_p0_to_cite_n = sd_fr_p0_to_cite / sd_fr_p0_to_p1
    # [0..1), e.g. 0.9
    flines_fr_p0_to_p1 = _flines_fr_p0_to_p1(lciar)
    flines_fr_p0_to_cite = sd_fr_p0_to_cite_n * flines_fr_p0_to_p1
    fline_of_p0 = _fline_of_p0(lciar)
    fline_of_cite = fline_of_p0 + flines_fr_p0_to_cite
    return fline_of_cite


def _flines_fr_p0_to_p1(lciar):
    if coli_range := lci_augrec.get_coli_range(lciar):
        return lci_rec.flines(coli_range)
    bkid = lci_augrec.get_bkid(lciar)
    pcc = _page_column_count(bkid)
    return 27 * pcc


def _page_column_count(bkid):
    if tbn.get_secid(bkid) == tbn.SEC_SIF_EM:
        return 2
    return 3


def _fline_of_p0(lciar):
    if coli_range := lci_augrec.get_coli_range(lciar):
        return lci_rec.fline_of_start(coli_range)
    return 1


def _sd_fr_p0_to_cite(uxlc, lciar, std_bcvp_quad):
    """Scalar distance from waypoint 0 to the citation."""
    # dist_12: distance from start of lciar to cite
    dist_12 = _calc_bibdist(uxlc, lciar, std_bcvp_quad)
    if lci_augrec.get_coli_range(lciar):
        return bibdist.get_word_count(dist_12)
    # dist_01: distance from start of page to start of lciar
    # dist_02: distance from start of page to cite
    dist_01 = lci_augrec.get_bibdist_start(lciar)
    dist_02 = bibdist.add(dist_01, dist_12)
    return bibdist.get_word_count(dist_02)


def _sd_fr_p0_to_p1(pbi, lciar):
    """Scalar distance from waypoint 0 to waypoint 1."""
    if lci_augrec.get_coli_range(lciar):
        bd_start = lci_augrec.get_bibdist_start(lciar)
        bd_stop = lci_augrec.get_bibdist_stop(lciar)
        bd_diff = bibdist.subtract(bd_stop, bd_start)
        return bibdist.get_word_count(bd_diff)
    guess_pgid = lci_augrec.get_pgid(lciar)
    length_of_guess_page = page_break_info.get_page_lengths(pbi)[guess_pgid]
    return bibdist.get_word_count(length_of_guess_page)


def _calc_bibdist(uxlc, lciar, std_bcvp_quad):
    std_bkid = std_bcvp_quad[0]
    cvp_start = lci_augrec.get_cvp_start(lciar)
    cvp_stop = cvp.make(*std_bcvp_quad[1:4])
    cvp_range = cvp_start, cvp_stop
    the_bibdist = bibdist.calc(uxlc, std_bkid, cvp_range)
    return the_bibdist
