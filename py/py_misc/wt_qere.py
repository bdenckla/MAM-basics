from pycmn import str_defs as sd
from pycmn import ws_tmpl2 as wtp
from pycmn import template_names as tmpln
from pycmn import hebrew_punctuation as hpu
from pycmn.shrink import shrink
from pycmn.my_utils import first_and_only_and_str
from pycmn.my_utils import sum_of_map
from pycmn.my_utils import sum_of_seqs
from pycmn.my_utils import intersperse
from py_misc.split import my_re_split


def get_verse(hnds, mroge):
    minirow = mroge.get("mroge-minirow")
    if not minirow:
        assert mroge.get("mroge-good-ending")
        return []
    #
    return do_one_wtseq(hnds, minirow.EP)


def get_verse_as_wordstrs(hnds, mroge):
    custom_qere = get_verse(hnds, mroge)
    if not custom_qere:
        return []
    whole_verse_as_str = first_and_only_and_str(custom_qere)
    return my_re_split(r"[ ]+", whole_verse_as_str)


def do_one_wtseq(hnds, wtseq):
    return shrink(sum_of_map((_do_one_wtel, hnds), wtseq))


def hnd_recurse_on_arg_0(hnds, tmpl):
    return do_one_wtseq(hnds, wtp.template_element(tmpl, 1))


def hnd_recurse_on_param_dalet(hnds, tmpl):
    return do_one_wtseq(hnds, wtp.template_param_val(tmpl, "ד"))


def hnd_recurse_on_param_alef(hnds, tmpl):
    return do_one_wtseq(hnds, wtp.template_param_val(tmpl, "א"))


def hnd_recurse_on_param_bet(hnds, tmpl):
    return do_one_wtseq(hnds, wtp.template_param_val(tmpl, "ב"))


def hnd_identity(_1, tmpl):
    return [tmpl]


def hnd_return_plain_space(_1, _2):
    return [" "]


def hnd_return_doub_vert_line_plus_space(_1, _2):
    return [sd.DOUB_VERT_LINE + " "]


def hnd_recurse_on_param_vals_and_ca(hnds, tmpl):
    """ca: concatenate alternatives (separated by plain space)"""
    mapped = sum_of_seqs(wtp.map_params((do_one_wtseq, hnds), tmpl))
    return intersperse(" ", mapped)


def mktmpl_mp(hnds, tmpl):
    return [wtp.mktmpl_mp((do_one_wtseq, hnds), tmpl)]


######################################################################
######################################################################


def _do_one_wtel(hnds, wtel):
    if isinstance(wtel, str):
        return [wtel]
    tmpl_name = wtp.template_name(wtel)
    return hnds[tmpl_name](hnds, wtel)


def _hnd_recurse_on_arg_1(hnds, tmpl):
    return do_one_wtseq(hnds, wtp.template_element(tmpl, 2))


def _hnd_recurse_on_params(hnds, tmpl):
    return [wtp.mktmpl_mp((do_one_wtseq, hnds), tmpl)]


def _hnd_return_empty_list(_1, _2):
    return []


def _hnd_return_leg_str(_1, tmpl):
    return [hpu.PASOLEG]


def _hnd_return_maq_str(_1, tmpl):
    return [hpu.MAQ]


HANDLERS = {
    "נוסח": hnd_recurse_on_arg_0,
    tmpln.SCRDFF_TAR: hnd_recurse_on_arg_0,
    'קו"כ-אם': hnd_recurse_on_arg_0,
    #
    "קרי ולא כתיב": _hnd_recurse_on_arg_1,  # {{קרי ולא כתיב|[בְּנֵ֣י]|בְּנֵ֣י}}
    "מ:דחי": _hnd_recurse_on_params,
    "מ:צינור": _hnd_recurse_on_params,
    "מ:קמץ": _hnd_recurse_on_params,
    "מ:כפול": _hnd_recurse_on_params,
    tmpln.SLH_WORD: hnd_recurse_on_arg_0,
    "מ:אות-ג": hnd_recurse_on_arg_0,
    "מ:אות-ק": hnd_recurse_on_arg_0,
    "מ:אות תלויה": hnd_recurse_on_arg_0,
    #
    **tmpln.map_all_std_kq_to_a_constant(_hnd_recurse_on_arg_1),
    #
    **tmpln.map_all_whitespace_to_a_constant(hnd_return_plain_space),
    #
    "מ:פסק": hnd_identity,
    "מ:לגרמיה-2": _hnd_return_leg_str,
    "מ:מקף אפור": _hnd_return_maq_str,
    #
    "כתיב ולא קרי": _hnd_return_empty_list,
    tmpln.SCRDFF_NO_TAR: _hnd_return_empty_list,
    'מ:נו"ן הפוכה': _hnd_return_empty_list,
}
