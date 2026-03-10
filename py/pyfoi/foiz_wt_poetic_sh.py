from pycmn import ws_tmpl2 as wtp
from pyfoi import foi_wikitext_helpers as fwh
from pycmn.my_utils import sum_of_seqs


def find_fois_wt(mroge):
    """
    Find certain interesting uses of "dexnor" stress helpers.
    (We use "dexnor" to mean dexi or tsinnor.)
    """
    return fwh.find_fois_in_minirow_ep(_FOILERS, mroge)


def _handle_tsinnor(_foilers, _stack, tmpl):
    if wtp.template_len(tmpl) == 2:
        return []  # E.g. {{מ:צינור|רַבִּים֮}} is not interesting to us
    arg_1 = wtp.template_element(tmpl, 2)
    if arg_1 == []:
        return []  # {{מ:צינור|לְרָשָׁע֮|}} is not interesting to us
    assert len(arg_1) == 1
    assert isinstance(arg_1[0], str)
    foi_path = "poetic-stress-helpers", "tsinnor"
    foi_target = arg_1[0]
    foi = foi_path, foi_target
    return [foi]


def _handle_dexi(_foilers, stack, tmpl):
    args = [wtp.template_param_val(tmpl, "1"), wtp.template_param_val(tmpl, "2")]
    fois_for_tmpls_below = _get_fois_for_tmpls_below(args)
    fois_for_tmpls_above = _get_fois_for_tmpls_above(stack)
    return fois_for_tmpls_below + fois_for_tmpls_above


def _get_fois_for_tmpls_above(stack):
    if not stack:
        return []
    foi_path = "poetic-stress-helpers", "dexi-with-tmpl-above"
    foi_target = str(stack)
    foi = foi_path, foi_target
    fois = [foi]
    return fois


def _get_fois_for_tmpls_below(args):
    tmpls_in_args = sum_of_seqs(map(_tmpls_in_arg, args))
    if not tmpls_in_args:
        return []
    tmpl_names = list(map(_stringify_tmpl, tmpls_in_args))
    foi_path = "poetic-stress-helpers", "dexi-with-tmpl-below"
    fois = [(foi_path, foi_target) for foi_target in tmpl_names]
    return fois


def _tmpls_in_arg(wtels):
    return filter(wtp.is_template, wtels)


def _stringify_tmpl(wtel):
    assert wtp.is_template(wtel)
    return wtp.template_name(wtel)


_FOILERS = {
    "מ:דחי": _handle_dexi,
    "מ:צינור": _handle_tsinnor,
}
