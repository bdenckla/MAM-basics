from pycmn import bib_locales as tbn


def mk_dic_for_shifted_spans(ss_recs):
    """
    Make a dictionary for shifted verse spans,
    given ssrecs (shifted span records)
    """
    dic = {}
    for shift_rec in ss_recs:
        span_start_bcvt, span_len, shift = shift_rec
        bk39id, chnu, span_start_v = tbn.bcvt_get_bcv_triple(span_start_bcvt)
        vtrad = tbn.bcvt_get_vtrad(span_start_bcvt)
        # shift is amount to shift the other tradition's verse number to get
        # the MAM verse number
        for span_v in range(span_start_v, span_start_v + span_len):
            mam_v = span_v + shift
            bcvtmam = tbn.mk_bcvtmam(bk39id, chnu, mam_v)
            dic[bcvtmam] = mk_maprec_1_to_1(tbn.mk_cvt(chnu, span_v, vtrad))
    return dic


def mk_maprec_1_to_1(cvt):
    """Make a mapping of 1 verse to 1 verse"""
    return (_mk_cvve_f(cvt),)


def mk_maprec_1_to_many(*cvts):
    """Make a mapping of 1 verse to many verses"""
    return tuple(_mk_cvve_p(cvt) for cvt in cvts)


def mk_maprec_1_to_1_and_empties(cv_nonempty, cv_empty1, cv_empty2):
    """
    Make a mapping of 1 verse to 3 verses,
    the first of which has contents and
    the next two of which are empty.
    """
    return (_mk_cvve_f(cv_nonempty), _mk_cvve_e(cv_empty1), _mk_cvve_e(cv_empty2))


def cvve_get_cvv(cvve):
    """Return the cvt part of a cvve"""
    return cvve[0]


def cvve_get_type(cvve):
    """
    Returns the type part of a cvve:
    same contents, no contents, or partial contents
    """
    return cvve[1]


def cvm_rec_mk(cvm_rec_type, cvm):
    """Make a cvm_rec"""
    return {"_cvm_rec": (cvm_rec_type, cvm)}


def _mk_cvve_e(cvt):  # e for empty
    return _mk_cvve(cvt, CVVE_TYPE_NO_CONTENTS)


def _mk_cvve_p(cvt):  # p for partial
    return _mk_cvve(cvt, CVVE_TYPE_PARTIAL_CONTENTS)


def _mk_cvve_f(cvt):  # f for full
    return _mk_cvve(cvt, CVVE_TYPE_SAME_CONTENTS)


def _mk_cvve(cvt, cvve_type):
    return cvt, cvve_type


CVVE_TYPE_SAME_CONTENTS = 1
# In the foreign vtrad, the verse has the same contents
# that it has in the native (MAM) vtrad.
CVVE_TYPE_NO_CONTENTS = 2
# In the foreign vtrad, the verse has no contents,
# since it has only a nominal source verse (Joshua 21:25)
# in the native (MAM) vtrad.
CVVE_TYPE_PARTIAL_CONTENTS = 3
# In the foreign vtrad, the verse has only part of the contents
# of its (Decalogue) source verse in the native (MAM) vtrad.
