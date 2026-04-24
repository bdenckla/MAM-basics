def alirec_sa(alirec):
    return _alirec_parsed(alirec)["sord"]


def alirec_dord_brac(alirec):
    return _alirec_parsed(alirec)["dord_brac"]


def alirec_bar_bcv(alirec):
    return alirec["_alirec"][0]


def alirec_s_tea_maf(alirec):
    stea_brac = _alirec_stea_brac(alirec)
    smaf = _alirec_smaf(alirec)
    assert not (stea_brac and smaf)
    return stea_brac or smaf


def alirec_d_tea_maf(alirec):
    dtea_brac = _alirec_dtea_brac(alirec)
    dmaf = _alirec_dmaf(alirec)
    assert not (dtea_brac and dmaf)
    return dtea_brac or dmaf


def alirec_dpar_parts(alirec):
    dpar = _alirec_parsed(alirec)["dpar"]
    return dpar.split("\N{EN DASH}") if dpar else (None, None)  # –


def alirec_classic(alirec):
    return _alirec_parsed(alirec)["classic"]


def make_alirec(bar_bcv, parsed):
    return {"_alirec": (bar_bcv, parsed)}


def _alirec_parsed(alirec):
    return alirec["_alirec"][1]


def _alirec_stea_brac(alirec):
    return _alirec_parsed(alirec)["stea_brac"]


def _alirec_smaf(alirec):
    return _alirec_parsed(alirec)["smaf"]


def _alirec_dtea_brac(alirec):
    return _alirec_parsed(alirec)["dtea_brac"]


def _alirec_dmaf(alirec):
    return _alirec_parsed(alirec)["dmaf"]
