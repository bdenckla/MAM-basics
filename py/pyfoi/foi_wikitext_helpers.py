from pycmn import ws_tmpl2 as wtp
from pycmn.my_utils import szip
from pycmn.my_utils import sum_of_map


def find_fois_in_minirow_ep(foilers, mroge):
    # mroge: minirow or good ending
    if minirow := mroge.get("mroge-minirow"):
        return find_fois_in_wtseq(foilers, minirow.EP)
    assert mroge.get("mroge-good-ending")
    return []


def find_fois_in_wtseq(foilers, wtseq):
    """Find features of interest in Wikitext."""
    return _sum_map_find_in_wtel(foilers, _stack_make_empty(), wtseq)


def stack_summary(summary_dic, stack):
    """
    Summarize a stack by using a dict to pick one of the stack's elements.
    """
    index = summary_dic[stack]
    return stack[index] if index is not None else None


def find_fois_in_slh_word_arg_1(foilers, stack, tmpl):
    """arg 1 meaning the second arg, a list whose one and only element is a string"""
    new_stack = _stack_push(stack, wtp.template_name(tmpl))
    wtseq = wtp.template_element(tmpl, 2)
    return _sum_map_find_in_wtel(foilers, new_stack, wtseq)


def label_args_of_doc(foilers, stack, tmpl):
    """Label the arguments of the doc template."""
    # Also checked in an earlier stage of the multi-program pipeline:
    # check_mpp, called by main_download_fr_google.
    assert wtp.template_len(tmpl) == 3
    pnpv_dic = {
        "doc-target": wtp.template_param_val(tmpl, "1"),
        "doc-part-n": wtp.template_param_val(tmpl, "2"),
    }
    return _find_fois_with_labelled_args(foilers, stack, pnpv_dic)


def label_args_of_kq_triv(foilers, stack, tmpl):
    """Label the arguments of the doc template."""
    assert wtp.template_len(tmpl) == 3
    pnpv_dic = {
        "kq-triv-target": wtp.template_param_val(tmpl, "1"),
        "kq-triv-doc": wtp.template_param_val(tmpl, "2"),
    }
    return _find_fois_with_labelled_args(foilers, stack, pnpv_dic)


def label_args_of_scrdfftar(foilers, stack, tmpl):
    """Label the arguments of the scrdfftar (targeted scrdff) template."""
    pnpv_dic = {
        "scrdfftar-tar": wtp.template_param_val(tmpl, "1"),
        "scrdfftar-note": wtp.template_param_val(tmpl, "2"),
        "scrdfftar-starpos": wtp.template_param_val(tmpl, "3"),
    }
    return _find_fois_with_labelled_args(foilers, stack, pnpv_dic)


def label_args_of_ketiv_qere(foilers, stack, tmpl):
    """Label the arguments of the ketiv/qere template."""
    pnpv_dic = {
        "kq-ketiv": wtp.template_param_val(tmpl, "1"),
        "kq-qere": wtp.template_param_val(tmpl, "2"),
    }
    return _find_fois_with_labelled_args(foilers, stack, pnpv_dic)


DUALCANT_ARG_COMBINED = "כפול-כפול"
DUALCANT_ARG_ALEF = "כפול-א/תחתון/פשוטה"
DUALCANT_ARG_BET = "כפול-ב/עליון/מדרשית"


def label_args_of_dualcant(foilers, stack, tmpl):
    """Label the arguments of the dual cantillation template."""
    pnpv_dic = {
        DUALCANT_ARG_COMBINED: wtp.template_param_val(tmpl, "כפול"),
        DUALCANT_ARG_ALEF: wtp.template_param_val(tmpl, "א"),
        DUALCANT_ARG_BET: wtp.template_param_val(tmpl, "ב"),
    }
    return _find_fois_with_labelled_args(foilers, stack, pnpv_dic)


def ignore(_foilers, _stack, _tmpl):
    """Handle a template by ignoring it."""
    return []


######################################################################
######################################################################


def _ignore_str(_stack, _tmpl):
    """Handle a string by ignoring it."""
    return []


def _find_fois_in_wtel(foilers, stack, wtel):
    if isinstance(wtel, str):
        str_handler = foilers.get(str) or _ignore_str
        return str_handler(stack, wtel)
    tmpl_name = wtp.template_name(wtel)
    handler = foilers.get(tmpl_name) or _foiler_for_misc
    return handler(foilers, stack, wtel)


def _find_fois_with_labelled_args(foilers, stack, pnpv_dic):
    # pnpv: param name and param value
    the_sum = []
    for param_name, param_val in pnpv_dic.items():
        new_stack = _stack_push(stack, param_name)
        the_sum += _sum_map_find_in_wtel(foilers, new_stack, param_val)
    return the_sum


def _stack_push(stack, obj):
    """Push an object (probably a string) on the stack."""
    return *stack, obj


def _stack_make_empty():
    return tuple()


def _foiler_for_misc(foilers, stack, tmpl):
    new_stack = _stack_push(stack, wtp.template_name(tmpl))
    lis_wtseq = wtp.template_param_vals(tmpl)
    return sum_of_map((_sum_map_find_in_wtel, foilers, new_stack), lis_wtseq)


def _sum_map_find_in_wtel(foilers, stack, wtseq):
    return sum_of_map((_find_fois_in_wtel, foilers, stack), wtseq)
