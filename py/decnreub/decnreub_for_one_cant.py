from pycmn.my_utils import intersperse, sum_of_seqs, sum_of_map
from pycmn import hebrew_punctuation as hpu
from pycmn import ws_tmpl2 as wtp


def do_one_wtseq(wtseq):
    return sum_of_map(_do_one_wtel, wtseq)


def _do_one_wtel(wtel):
    if isinstance(wtel, str):
        return _HANDLERS_INSIDE_ONE_CANT["string"](wtel)
    if tmpl_name := wtp.template_name(wtel):
        return _HANDLERS_INSIDE_ONE_CANT[tmpl_name](wtel)
    assert False, wtel


def _hnd_ioc_recurse_on_arg_0(tmpl):
    return do_one_wtseq(wtp.template_element(tmpl, 1))


def _hnd_ioc_recurse_on_param_vals(tmpl):
    mapped = sum_of_seqs(wtp.map_params(do_one_wtseq, tmpl))
    return intersperse(" ", mapped)  # pretend alternatives are sequential


def _hnd_ioc_return_leg_str(_1):
    return [hpu.PASOLEG]


def _hnd_ioc_identity(wtel):
    return [wtel]


_HANDLERS_INSIDE_ONE_CANT = {
    "נוסח": _hnd_ioc_recurse_on_arg_0,
    "מ:קמץ": _hnd_ioc_recurse_on_param_vals,
    "מ:לגרמיה-2": _hnd_ioc_return_leg_str,
    #
    "string": _hnd_ioc_identity,
    "מ:פסק": _hnd_ioc_identity,
    "סס": _hnd_ioc_identity,
    "פפ": _hnd_ioc_identity,
}
