def glirec(flirec):
    s_parashah = flirec["s_parashah"]
    s_ord_nc, s_tea_nc_nb, s_maf = _d_or_s_fields(flirec, "s_ord", "s_tea_maf")
    #
    d_ord_nc, d_tea_nc_nb, d_maf = _d_or_s_fields(flirec, "d_ord", "d_tea_maf")
    d_ord_nc_nb = _rm_brac("()", d_ord_nc)
    #
    unparsed = _unparse_atoms(s_parashah, s_ord_nc, d_ord_nc_nb, s_tea_nc_nb, s_maf)
    assert unparsed == flirec["orig_str"]
    #
    return {
        "gr-bcv": flirec["bcv"],
        "gr-orig_str": flirec["orig_str"],
        #
        "gr-s_parashah": s_parashah,
        "gr-s_ord": s_ord_nc,
        "gr-s_tea": s_tea_nc_nb,
        "gr-s_maf": s_maf,
        #
        "gr-d_parashah": _d_parashah(flirec, d_ord_nc_nb or d_tea_nc_nb or d_maf),
        "gr-d_ord": d_ord_nc_nb,
        "gr-d_tea": d_tea_nc_nb,
        "gr-d_maf": d_maf,
    }


def _d_parashah(flirec, has_data):
    if not has_data:
        return None
    prev_p = flirec["prev"]
    single = flirec["s_parashah"]
    next_p = flirec["next"]
    if prev_p:
        assert next_p is None
        return _pjoin(prev_p, single)
    if next_p:
        return _pjoin(single, next_p)
    return None


def _pjoin(parasha_1, parasha_2):
    return parasha_1 + "\N{EN DASH}" + parasha_2  # –


def _d_or_s_fields(flirec, ord, x_tea_maf_key):
    x_ord_nc = _no_continuation(flirec[ord])
    x_tea_maf_nc = _no_continuation(flirec[x_tea_maf_key])
    x_tea_nc, x_maf = _tm_tea(x_tea_maf_nc), _tm_maf(x_tea_maf_nc)
    x_tea_nc_nb = _rm_brac("[]", x_tea_nc)
    return x_ord_nc, x_tea_nc_nb, x_maf


def _tm_maf(s_tea_maf):
    return s_tea_maf if s_tea_maf == "מפטיר" else None


def _tm_tea(s_tea_maf):
    return s_tea_maf if s_tea_maf != "מפטיר" else None


def _no_continuation(strq):
    return strq if strq and "..." not in strq else None


def _rm_brac(brac_oc, strq):
    if strq is None:
        return None
    assert strq[0] == brac_oc[0] and strq[-1] == brac_oc[-1]
    return strq[1:-1]


def _unparse_atoms(s_parashah, s_ord, d_ord, tea, maf):
    pasa = _pasa(s_parashah, s_ord)
    pasa_maf = _jtwo(" " + "ו", pasa, maf)
    d_ord_b = _d_ord_b(d_ord)
    pasa_maf_da = _jtwo(" ", pasa_maf, d_ord_b)
    return _jtwo(" ", pasa_maf_da, _tea_b(s_ord, tea))


def _pasa(s_parashah, s_ord):
    return s_parashah if s_ord == "ראשון" else s_ord


def _d_ord_b(d_ord):
    return f"({d_ord})" if d_ord and d_ord != "ראשון" else None


def _tea_b(s_ord, tea):
    return f"[{tea}]" if _tea_worthy(s_ord, tea) else None


def _tea_worthy(s_ord, tea):
    return tea and tea != "כהן" and (s_ord, tea) != ("שני", 'ע"כ ישראל')


def _jtwo(joi, sta, stb):
    if sta and stb:
        return sta + joi + stb
    return sta or stb
