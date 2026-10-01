import mb_cmn.uni_heb as uh
import mb_cmn.hebrew_accents as ha


def get_hccvec_from_bccvec(bccvec):
    assert isinstance(bccvec, tuple)
    return ",".join(map(get_hcc_from_bcc, bccvec))


def get_hcc_from_bcc(bcc):
    if bcc in ha.NON_UNICODE_ACCENTS:
        return bcc
    return uh.join_shunnas(bcc, "-")
