from pycmn import template_names as tmpln
from py_misc import ren_html_for_renel as hfr
from pycmn import ws_tmpl2 as wtp
from pyrender import render_wikitext_handlers as handlers
from pyrender import render_wikitext_helpers as wt_help
from py_misc import ren_html_from_ren_el_mapping as hfrm
from pyfoi import foi_wikitext_helpers as fwh
from pyfoi import foi_struct as fct
from pycmn.my_utils import intersperse
from pycmn.my_utils import sum_of_tuples
from pycmn.my_utils import first_and_only
from pycmn.my_utils import first_and_only_and_str


def find_fois_wt(mroge):
    """Find uses of rare templates."""
    # mroge: minirow or good ending
    if minirow := mroge.get("mroge-minirow"):
        fois_cp = fwh.find_fois_in_wtseq(_FOILERS_FOR_COLUMN_C, minirow.CP)
        fois_ep = fwh.find_fois_in_wtseq(_FOILERS_FOR_COLUMN_E, minirow.EP)
        return fois_cp + fois_ep
    return _find_fois_in_good_ending(mroge)


def _find_fois_in_good_ending(mroge):
    gewe = mroge["mroge-good-ending"]["wikitext_element"]
    return fwh.find_fois_in_wtseq(_FOILERS_FOR_COLUMN_E, [gewe])


def _record_scrdff_in_col_e(foilers, stack, tmpl):
    return _record_scrdff_in_col_x("E", foilers, stack, tmpl)


def _record_scrdff_in_col_c(foilers, stack, tmpl):
    return _record_scrdff_in_col_x("C", foilers, stack, tmpl)


def _record_scrdff_in_col_x(column, foilers, stack, tmpl):
    # column is a string, expected to be either 'E' or 'C'
    assert (
        wtp.template_len(tmpl) == 4
    )  # length 2 means one argument beyond the template name
    args = [
        wtp.template_param_val(tmpl, "1"),
        wtp.template_param_val(tmpl, "2"),
        wtp.template_param_val(tmpl, "3"),
    ]
    foi_display_parts = [_html_for_wtseq(arg, column=column) for arg in args]
    foi_display = intersperse((" / ",), foi_display_parts)
    foi_display = sum_of_tuples(foi_display)
    # XXX TODO qualify with column
    this_result = _FP_RT_NA_NOTE, foi_display
    recursion_result = fwh.label_args_of_scrdfftar(foilers, stack, tmpl)
    return [this_result, *recursion_result]


def _record_inverted_nun(_foilers, _stack, _tmpl):
    return [(_FP_RT_WP_INVNUN, "")]


def _record_good_ending(_foilers, _stack, _tmpl):
    return [(_FP_RT_NA_GE, "")]


def _record_implicit_maqaf(_foilers, _stack, _tmpl):
    return [(_FP_RT_IM, "")]


_FP_RT_NA_NOTE = "rare-tmpls", "na-note"
_FP_RT_NA_GE = "rare-tmpls", "na-good-ending"
_FP_RT_WP_INVNUN = "rare-tmpls", "wp-invnun"
_FP_RT_IM = "rare-tmpls", "implicit-maqaf"
_FP_RT_CES = "rare-tmpls", "col-e-sampe"


def _record_sampe_in_col_e(_foilers, stack, tmpl):
    tmpl_name = wtp.template_name(tmpl)  # e.g. סס, פפ, ...
    assert (
        wtp.template_len(tmpl) <= 2
    )  # length 1 means no arguments beyond the template name
    if wtp.template_len(tmpl) == 2:
        mid_verse_sampe = wtp.template_param_val(tmpl, "1")
    else:
        mid_verse_sampe = None
    stack_summary = fwh.stack_summary(_STACK_SUMMARIES, stack)
    if mid_verse_sampe:
        fao_mvs = first_and_only_and_str(mid_verse_sampe)
        assert fao_mvs == "פסקא באמצע פסוק"
    qualifier = {
        "פסקא באמצע פסוק": "פסקא באמצע פסוק" if mid_verse_sampe else None,
        "stack_str": stack_summary,
    }
    qual_target = fct.make_qtarget(tmpl_name, qualifier)
    return [(_FP_RT_CES, qual_target)]


def _html_for_wtseq(wtseq, column="E"):
    hctx = handlers.default_hctx()
    if column == "C":
        if tuple(wtseq) == ("__",):
            return ("__",)
        hctx = handlers.col_c_hctx(hctx)
    else:
        assert column == "E"
    renseq = wt_help.render_wtseq(hctx, wtseq)
    hfr_ctx = hfr.HfrCtx(hfrm.HT_TAC_FOR_RT_FOR_RARE_TMPLS_FOI)
    return hfr.html_for_ren_el(hfr_ctx, renseq)


_FOILERS_FOR_COLUMN_E = {
    tmpln.SCRDFF_TAR: _record_scrdff_in_col_e,
    'מ:נו"ן הפוכה': _record_inverted_nun,
    "מ:סיום בטוב": _record_good_ending,
    "מ:מקף אפור": _record_implicit_maqaf,
    "סס": _record_sampe_in_col_e,
    "ססס": _record_sampe_in_col_e,
    "פפ": _record_sampe_in_col_e,
    "פפפ": _record_sampe_in_col_e,
    #
    "מ:כפול": fwh.label_args_of_dualcant,
    "נוסח": fwh.label_args_of_doc,
    # label_args_of_scrdfftar is called in _record_scrdff_in_col_x
    # tmpln.SCRDFF_TAR: fwh.label_args_of_scrdfftar,
    tmpln.SCRDFF_NO_TAR: fwh.ignore,
}
_FOILERS_FOR_COLUMN_C = {
    tmpln.SCRDFF_TAR: _record_scrdff_in_col_c,
}
_STACK_SUMMARIES = {
    tuple(): None,
    ("doc-target",): None,
    (fwh.DUALCANT_ARG_COMBINED, "doc-target"): -2,
    (fwh.DUALCANT_ARG_COMBINED,): -1,
    (fwh.DUALCANT_ARG_ALEF,): -1,
    (fwh.DUALCANT_ARG_BET,): -1,
}
