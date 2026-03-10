from pycmn import mam_bknas
from pycmn import ws_tmpl2 as wtp2
from pytmpl_survey import column_d_alirec as ar


def store_the_mpasuq_call(io_weeklies, bscv, wtseq):
    """Store the mpasuq call, if any, found in the given wtseq."""
    if not wtseq:
        return
    assert len(wtseq) == 1
    _store_the_mpasuq_call_itw(io_weeklies, bscv, wtseq[0])


def _store_the_mpasuq_call_itw(io_weeklies, bscv, wtel):
    """
    Store the mpasuq call, if any, found in the given wtel.
    itw: in the wtel
    """
    if wtp2.is_template_with_name(wtel, "נוסח"):
        inner = wtp2.template_param_val(wtel, "1")
        store_the_mpasuq_call(io_weeklies, bscv, inner)
        return
    assert wtp2.is_template_with_name(wtel, "מ:פסוק")
    bk24na, sub_bkna, chnu, psv_psn = bscv
    bk39na = mam_bknas.he_bk39_name(bk24na, sub_bkna)
    params = wtel["tmpl_params"]
    assert params["1"] == bk39na
    assert params["2"] == chnu
    assert params["3"] == psv_psn
    bar_bcv = "|".join((bk39na, chnu, psv_psn))
    _store_the_mpasuq_call_itp(io_weeklies, bar_bcv, params)


def _store_the_mpasuq_call_itp(io_weeklies, bar_bcv, params):
    """
    Store the mpasuq call, if any, found in the given params.
    itp: in the tmpl_params
    """
    alyyh_val = params.get("עלייה")
    if alyyh_val is None:
        return
    parsed = _parse_aliyah_val(alyyh_val)
    alirec = ar.make_alirec(bar_bcv, parsed)
    if parsed["sord"] == "ראשון":
        io_weeklies.append(_make_weekly(parsed["spar"], alirec))
    else:
        _append_alirec_to_weekly(io_weeklies[-1], alirec)


def _make_weekly(portion_name, initial_alirec):
    return {
        "weekly-portion-name": portion_name,
        "alirecs": [initial_alirec],
    }


def _append_alirec_to_weekly(io_weekly, alirec):
    io_weekly["alirecs"].append(alirec)


def _parse_aliyah_val(alyyh_val):
    assert wtp2.is_template_with_name(alyyh_val, "מ:עלייה")
    named_params = alyyh_val["tmpl_params"]
    return {
        "classic": named_params["א"],
        #
        "spar": named_params.get("ב0"),
        "sord": named_params.get("ב1"),
        "stea_brac": _maybe_bracket(named_params.get("ב2"), "[]"),
        "smaf": named_params.get("ב3"),
        #
        "dpar": named_params.get("ג0"),
        "dord_brac": _maybe_bracket(named_params.get("ג1"), "()"),
        "dtea_brac": _maybe_bracket(named_params.get("ג2"), "[]"),
        "dmaf": named_params.get("ג3"),
    }


def _maybe_bracket(val, brac):
    if val is None:
        return None
    return brac[0] + val + brac[1]
