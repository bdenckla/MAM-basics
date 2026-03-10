from pycmn import mam_bknas
from pycmn import ws_tmpl1 as wtp1
from pycmn import ws_tmpl_named_params as wtnp
from pytmpl_survey import column_d_alirec as ar
from pycmn.my_utils import first_and_only
from pycmn.my_utils import first_and_only_and_str


def store_the_mpasuq_call(io_weeklies, bscv, wtseq):
    """Store the mpasuq call, if any, found in the given wtseq."""
    _bk24na, _sub_bkna, _chnu, psv_psn = bscv
    if psv_psn in ("0", "תתת"):  # pseudo-verse pseudo-number zero or תתת
        assert not wtseq  # we expect an empty list
        return
    _store_the_mpasuq_call_itw(io_weeklies, bscv, first_and_only(wtseq))


def _store_the_mpasuq_call_itw(io_weeklies, bscv, wtel):
    """
    Store the mpasuq call, if any, found in the given wtel.
    itw: in the wtel
    """
    tmpl_args = wtp1.template_arguments(wtel)
    if wtp1.is_template_with_name(wtel, "נוסח"):
        store_the_mpasuq_call(io_weeklies, bscv, tmpl_args[0])
        return
    assert wtp1.is_template_with_name(wtel, "מ:פסוק")
    # bk24na is "24 books" book name, e.g. ['ספר שמואל']
    # Or, more precisely, bk24na is the column A book name.
    #
    # bk39na is "39 books" book name, e.g. ['שמואל א']
    # Or, more precisely, bk39na is the מ:פסוק first arg book name.
    bk24na, sub_bkna, chnu, psv_psn = bscv
    bk39na = mam_bknas.he_bk39_name(bk24na, sub_bkna)
    assert tmpl_args[0] == [bk39na]  # e.g. ['שמואל א']
    assert tmpl_args[1] == [chnu]  # e.g. ['א']
    assert tmpl_args[2] == [psv_psn]  # e.g. ['א']
    bar_bcv = "|".join((bk39na, chnu, psv_psn))
    _store_the_mpasuq_call_itta(io_weeklies, bar_bcv, tmpl_args)


def _store_the_mpasuq_call_itta(io_weeklies, bar_bcv, tmpl_args):
    """
    Store the mpasuq call, if any, found in the given tmpl_args.
    itta: in the tmpl_args
    """
    named_params = wtnp.get_tmpl_params_ss(tmpl_args)
    if "עלייה" not in named_params:
        return
    alyyh_val = named_params["עלייה"]
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
    fao = first_and_only(alyyh_val)
    assert wtp1.is_template_with_name(fao, "מ:עלייה")
    named_params = wtnp.get_tmpl_params_ss(wtp1.template_arguments(fao))
    return {
        "classic": first_and_only_and_str(named_params["א"]),
        #
        "spar": _faoasq(named_params, "ב0"),
        "sord": _faoasq(named_params, "ב1"),
        "stea_brac": _faoasq(named_params, "ב2", "[]"),
        "smaf": _faoasq(named_params, "ב3"),
        #
        "dpar": _faoasq(named_params, "ג0"),
        "dord_brac": _faoasq(named_params, "ג1", "()"),
        "dtea_brac": _faoasq(named_params, "ג2", "[]"),
        "dmaf": _faoasq(named_params, "ג3"),
    }


def _faoasq(named_params, param_name, brac=None):
    """
    faoas: first and only and string
    q: maybe
    """
    valq = named_params.get(param_name)
    if valq is None:
        return None
    bare = first_and_only_and_str(valq)
    if brac is None:
        return bare
    return brac[0] + bare + brac[1]
