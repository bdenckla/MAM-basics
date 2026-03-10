from pytmpl_survey import column_d_alirec as ar
from pytmpl_survey import column_d_glirec as cdg


def process_all_mpasuq_calls(weeklies):
    """
    Process alirecs into flirecs.
    Then, process flirecs into glirecs.
    Output both flirecs & glirecs.
    """
    flirecs = _flirecs(weeklies)
    return {
        "flirecs": flirecs,
        "glirecs": list(map(cdg.glirec, flirecs)),
    }


def _flirecs(weeklies):
    flirecs = []
    _add_dual_names(weeklies)
    contvals = {}
    for weekly in weeklies:
        for alirec in weekly["alirecs"]:
            flirecs.append(_make_flirec(weekly, alirec, contvals))
    return flirecs


def _add_dual_names(weeklies):
    prev_names_x = dict()
    for weekly in weeklies:
        parna = weekly["weekly-portion-name"]
        spar0, spar1 = ar.alirec_dpar_parts(weekly["alirecs"][0])
        weekly["weekly-next"] = spar1
        prev_names_x[spar1] = spar0
    for weekly in weeklies:
        parna = weekly["weekly-portion-name"]
        weekly["weekly-prev"] = prev_names_x.get(parna)


def _contval_bigkey(row, key, par_name_fn):
    return par_name_fn(row), key


def _dual_name(row):
    if row["prev"]:
        return "-".join((row["prev"], row["s_parashah"]))
    if row["next"]:
        return "-".join((row["s_parashah"], row["next"]))
    return None


_CONT_KEYS = {
    "s_ord": lambda r: r["s_parashah"],
    "s_tea_maf": lambda r: r["s_parashah"],
    "d_ord": _dual_name,
    "d_tea_maf": _dual_name,
}


def _update_contvals(contvals, row):
    for key, par_name_fn in _CONT_KEYS.items():
        rowkey = row[key]
        if rowkey is not None:
            big_key = _contval_bigkey(row, key, par_name_fn)
            contvals[big_key] = rowkey


def _add_contvals(row, contvals):
    outrow = dict(row)
    for key, par_name_fn in _CONT_KEYS.items():
        if row[key] is None:
            big_key = _contval_bigkey(row, key, par_name_fn)
            contval = contvals.get(big_key)
            if contval is not None and contval != '[ע"כ ישראל]':
                outrow[key] = contval + "..."
    return outrow


def _make_flirec(weekly, alirec, contvals):
    flirec = {
        "bcv": ar.alirec_bar_bcv(alirec),
        "prev": weekly["weekly-prev"],
        "s_parashah": weekly["weekly-portion-name"],
        "next": weekly["weekly-next"],
        "s_ord": ar.alirec_sa(alirec),
        "s_tea_maf": ar.alirec_s_tea_maf(alirec),
        "d_ord": ar.alirec_dord_brac(alirec),
        "d_tea_maf": ar.alirec_d_tea_maf(alirec),
        "orig_str": ar.alirec_classic(alirec),
    }
    _update_contvals(contvals, flirec)
    return _add_contvals(flirec, contvals)
