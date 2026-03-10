from pycmn import my_utils
from pycmn import bib_locales as tbn
from pycmn import ws_tmpl2 as wtp
from pycmn import template_names as tmpln
from py_misc import vtrad_helpers as helpers
from py_misc import vtrad_data
from pycmn.minirow import MinirowExt


def convert_to_bhs(bkids, books_mpp):
    """Run convert_from_mam targeting the BHS vtrad"""
    return _convert_from_mam(bkids, books_mpp, tbn.VT_BHS)


def convert_to_sef(bkids, books):
    """Run convert_from_mam targeting the Sefaria vtrad"""
    return _convert_from_mam(bkids, books, tbn.VT_SEF)


def _convert_from_mam(bk39ids, books_mpp, vtrad):
    """
    1. Expand the set of book IDs to include "next" books.
    2. For each book in "books" whose ID is in that expanded set of book
       IDs, return the equivalent of that book in the given vtrad.
    """
    ebk39ids = tbn.add_part2_bk39ids(bk39ids)
    return {b: _convert_book(books_mpp[b], vtrad) for b in ebk39ids}


# bcvtmam: a 4-element tuple consisting of:
#     bk39id: tbn bk39 ID
#     chnu: chapter number
#     vrnu: verse number
#     vtrad: expected to be tbn.VT_MAM


def _identity(bcvtmam, vtrad):
    chnu = tbn.bcvt_get_chnu(bcvtmam)
    vrnu = tbn.bcvt_get_vrnu(bcvtmam)
    cvtxxx = tbn.mk_cvt(chnu, vrnu, vtrad)
    return helpers.mk_maprec_1_to_1(cvtxxx)


def _get_minirows(bcvtmam, mam_minirow, vtrad):
    """
    Possibly split up mam_minirow into multiple minirows appropriate for
    the versification.
    """
    if saf_fun := _SPLITTERS_AND_FRIENDS[vtrad].get(bcvtmam):
        return saf_fun(mam_minirow)
    return (mam_minirow,)


def _convert_book(book_mpp, vtrad):
    xxx_verses = {}
    for bcvtmam, mam_minirow in book_mpp["verses_plus"].items():
        maprec = _get_maprec(bcvtmam, vtrad)
        xxx_minirows = _get_minirows(bcvtmam, mam_minirow, vtrad)
        for cvve, xxx_minirow in my_utils.szip(maprec, xxx_minirows):
            cvtxxx = helpers.cvve_get_cvv(cvve)
            bcvtxxx = tbn.mk_bcvt(tbn.bcvt_get_bk39id(bcvtmam), cvtxxx)
            assert bcvtxxx not in xxx_verses
            xxx_verses[bcvtxxx] = xxx_minirow
    out_book_mpp = dict(book_mpp)
    gek = "good_ending_with_bcvt"
    out_book_mpp[gek] = _convert_ge(book_mpp[gek], vtrad)
    out_book_mpp["verses_plus"] = xxx_verses
    return out_book_mpp


def _convert_ge(good_ending, vtrad):
    if good_ending is None:
        return None
    bcvtmam = good_ending["last_bcvt"]
    maprec = _get_maprec(bcvtmam, vtrad)
    cvve = my_utils.first_and_only(maprec)
    cvtxxx = helpers.cvve_get_cvv(cvve)
    # The assert below asserts that we're not actually
    # changing the chnu or vrnu, we're just changing the vtrad.
    # (No vtrads differ in their cv for good endings.)
    assert tbn.eq_mod_vtrad(tbn.bcvt_get_cvt(bcvtmam), cvtxxx)
    bcvtxxx = tbn.mk_bcvt(tbn.bcvt_get_bk39id(bcvtmam), cvtxxx)
    return {**good_ending, "last_bcvt": bcvtxxx}


def _one_to_many_v01decalogue(mam_minirow):
    # v01decalogue: verse 1 of a Decalogue (E 20:2 or D 5:6)
    mra_cde = mam_minirow.CP, None, (mam_minirow.EP[0],)
    assert mam_minirow.EP[1] == " "
    mrb_cde = None, None, (mam_minirow.EP[2],)
    assert len(mam_minirow.EP) == 3
    assert isinstance(mam_minirow, MinirowExt)
    mra = MinirowExt(*mra_cde, tuple())
    mrb = MinirowExt(*mrb_cde, mam_minirow.next_CP)
    return mra, mrb


def _one_to_many_v11decalogue(mam_minirow):
    # v11decalogue: verse 11 of a Decalogue (E 20:12 or D 5:16)
    mr0_e = (mam_minirow.EP[0],)  # Minirow 0, column E
    #
    mr1_c = (mam_minirow.EP[1],)  # Minirow 1, column c
    mr1_e = (mam_minirow.EP[2],)  # Minirow 1, column e
    #
    mr2_c = (mam_minirow.EP[3],)  # Minirow 2, column c
    mr2_e = (mam_minirow.EP[4],)  # Minirow 2, column e
    #
    mr3_c = (mam_minirow.EP[5],)  # Minirow 3, column c
    mr3_e = (mam_minirow.EP[6],)  # Minirow 3, column e
    assert len(mam_minirow.EP) == 7
    assert isinstance(mam_minirow, MinirowExt)
    mr0 = MinirowExt(mam_minirow.CP, None, mr0_e, mr1_c)
    mr1 = MinirowExt(mr1_c, None, mr1_e, mr2_c)
    mr2 = MinirowExt(mr2_c, None, mr2_e, mr3_c)
    mr3 = MinirowExt(mr3_c, None, mr3_e, mam_minirow.next_CP)
    return mr0, mr1, mr2, mr3


def _one_to_many_joshua_21_35(mam_minirow):
    return mam_minirow, None, None


def _one_to_one_numbers_25_18(mam_minirow):
    assert isinstance(mam_minirow, MinirowExt)
    tmpl = wtp.mktmpl([[tmpln.NO_PAR_AT_STA_OF_CHAP21]])
    assert mam_minirow.next_CP == (tmpl,)
    mra = MinirowExt(mam_minirow.CP, mam_minirow.DP, mam_minirow.EP, tuple())
    return (mra,)


def _one_to_many_numbers_26_1(mam_minirow):
    tmpl = wtp.mktmpl([[tmpln.NO_PAR_AT_STA_OF_CHAP21]])
    assert mam_minirow.CP == (tmpl,)
    mra_cde = None, None, (mam_minirow.EP[0],)
    ep1 = mam_minirow.EP[1]
    assert _is_doc_of_double_pe(ep1)
    double_pe = wtp.mktmpl([["פפ"]])
    mrb_cde = (double_pe,), None, (mam_minirow.EP[2],)
    assert len(mam_minirow.EP) == 3
    assert isinstance(mam_minirow, MinirowExt)
    mra = MinirowExt(*mra_cde, mrb_cde[0])
    mrb = MinirowExt(*mrb_cde, mam_minirow.next_CP)
    return mra, mrb


def _is_doc_of_double_pe(wtel):
    # Return whether wtel is doc(pp,...)
    # Or, (אאא added to address RTL issues):
    # אאא {{נוסח|{{פפ}}|...}} אאא
    if not wtp.is_doc_template(wtel):
        return False
    doc_target = wtp.template_i0(wtel, 1)
    if not wtp.is_template_with_name(doc_target, "פפ"):
        return False
    return True


_SPLITTERS_AND_FRIENDS_SEF = {
    vtrad_data.EXODUS_20_2_MAM: _one_to_many_v01decalogue,
    vtrad_data.DEUTER_5_6_MAM: _one_to_many_v01decalogue,
    vtrad_data.JOSHUA_21_35_MAM: _one_to_many_joshua_21_35,
}
_SPLITTERS_AND_FRIENDS_BHS = {
    **_SPLITTERS_AND_FRIENDS_SEF,
    vtrad_data.EXODUS_20_12_MAM: _one_to_many_v11decalogue,
    vtrad_data.NUMBERS_25_18_MAM: _one_to_one_numbers_25_18,
    vtrad_data.NUMBERS_26_1_MAM: _one_to_many_numbers_26_1,
    vtrad_data.DEUTER_5_16_MAM: _one_to_many_v11decalogue,
}
_SPLITTERS_AND_FRIENDS = {
    tbn.VT_SEF: _SPLITTERS_AND_FRIENDS_SEF,
    tbn.VT_BHS: _SPLITTERS_AND_FRIENDS_BHS,
}


def _get_maprec(bcvtmam, vtrad):
    """
    Given bcvtmam (see comment above), returns a maprec.
    A maprec is tuple of pairs where those pairs consist of:
        a cvt
        a boolean telling whether that verse is empty
    (The "empty or not" boolean is only for Joshua 21:36 & 21:37.)
    """
    assert tbn.bcvt_is_tmam(bcvtmam)
    maprec = vtrad_data.BCV_DIC_FROM_MAM_TO_YYY[vtrad].get(bcvtmam)
    return maprec or _identity(bcvtmam, vtrad)
