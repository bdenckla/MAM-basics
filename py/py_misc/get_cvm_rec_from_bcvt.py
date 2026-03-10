from pycmn import bib_locales as tbn
from py_misc import vtrad_data
from py_misc import vtrad_helpers as helpers


def get_cvm_rec_from_bcvt(bcvt):
    """Get a cvm_rec from an a bcvt in any vtrad"""
    vtrad = tbn.bcvt_get_vtrad(bcvt)
    if vtrad == tbn.VT_MAM:
        return None
    return _DIC_FROM_BCVT_TO_CVM_REC[vtrad].get(bcvt)


def cvm_rec_get_parts(cvm_rec):
    """Extract the type and cvm part of a cvm_rec."""
    return cvm_rec["_cvm_rec"]


def _mk_dic_from_bcvt_to_cvm_rec(vtrad):
    out = {}
    bcv_dic_from_mam_to_xxx = vtrad_data.BCV_DIC_FROM_MAM_TO_YYY[vtrad]
    for bcvtmam, maprec in bcv_dic_from_mam_to_xxx.items():
        bk39id = tbn.bcvt_get_bk39id(bcvtmam)
        for cvve_xxx in maprec:
            cvtxxx = helpers.cvve_get_cvv(cvve_xxx)
            cvve_type = helpers.cvve_get_type(cvve_xxx)
            bcvtxxx = tbn.mk_bcvt(bk39id, cvtxxx)
            cvtmam = tbn.bcvt_get_cvt(bcvtmam)
            if cvve_type == helpers.CVVE_TYPE_SAME_CONTENTS:
                if tbn.eq_mod_vtrad(cvtxxx, cvtmam):
                    continue
            # It just so happens that the mapping from
            # non-mam vtrads to mam is always many-to-one.
            # The assert below asserts that.
            assert bcvtxxx not in out
            out[bcvtxxx] = helpers.cvm_rec_mk(cvve_type, cvtmam)
    return out


_DIC_FROM_BCVT_TO_CVM_REC = {
    tbn.VT_SEF: _mk_dic_from_bcvt_to_cvm_rec(tbn.VT_SEF),
    tbn.VT_BHS: _mk_dic_from_bcvt_to_cvm_rec(tbn.VT_BHS),
}
