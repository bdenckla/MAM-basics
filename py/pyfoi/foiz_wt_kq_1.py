from pyfoi import foi_struct as fct
from pyfoi import foi_wikitext_helpers as fwh
from py_misc import ren_html_from_ren_el_mapping as hfrm
from py_misc import ren_html_for_renel as hfr
from pycmn import ws_tmpl2 as wtp
from pyrender import render_wikitext_handlers as handlers
from pyrender import render_wikitext_helpers as wt_help
from pycmn import template_names as tmpln


def find_fois_wt(mroge):
    """Find ketiv/qere template uses: they are the feature of interest."""
    return fwh.find_fois_in_minirow_ep(_FOILERS, mroge)


def _record_kq_as_foi(_foilers, stack, tmpl):
    tmpl_name = wtp.template_name(tmpl)
    foi_path = "kq-simple", _FOI_PATH[tmpln.LATIN_SHORTS[tmpl_name]]
    stack_summary = fwh.stack_summary(_STACK_SUMMARIES, stack)
    foi_target_proper = _html_for_wtseq((tmpl,))
    if stack_summary:
        foi_qualifier = {"stack_str": stack_summary}
        foi_target = fct.make_qtarget(foi_target_proper, foi_qualifier)
    else:
        foi_target = foi_target_proper
    return [(foi_path, foi_target)]


def _html_for_wtseq(wtseq):
    hctx = handlers.default_hctx()
    renseq = wt_help.render_wtseq(hctx, wtseq)
    hfr_ctx = hfr.HfrCtx(hfrm.HT_TAC_FOR_RT_FOR_KETIV_QERE_FOI)
    return hfr.html_for_ren_el(hfr_ctx, renseq)


_FOI_PATH = {
    "kq-q-velo-k": "x-velo-y-q-velo-k",
    "kq-k-velo-q": "x-velo-y-k-velo-q",
    "k1q1-kq": "k1q1",
    "k1q1-qk": "k1q1←",
    "k1q1-mcom": "k1q1-mcom",
    "k1q2-sr-kqq": "k1q2sr",
    "k1q2-sr-qqk": "k1q2sr",
    "k1q2-sr-bcom": "k1q2sr",
    "k1q2-wr-kqq": "k1q2wr",
    "k1q2-ur-qqk": "k1q2ur",
    "k2q1": "k2q1",
    "k2q2": "k2q2",
    "k3q3": "k3q3",
    #
    "kq-trivial": "z-trivial",
}
_FOILERS_FOR_KETIV_QERE = {
    **tmpln.map_all_std_kq_to_a_constant(_record_kq_as_foi),
    'קו"כ-אם': _record_kq_as_foi,
    "קרי ולא כתיב": _record_kq_as_foi,
    "כתיב ולא קרי": _record_kq_as_foi,
}
_FOILERS = {
    **_FOILERS_FOR_KETIV_QERE,
    #
    "מ:כפול": fwh.label_args_of_dualcant,
    "נוסח": fwh.label_args_of_doc,
    tmpln.SCRDFF_TAR: fwh.label_args_of_scrdfftar,
    tmpln.SCRDFF_NO_TAR: fwh.ignore,
}
_STACK_SUMMARIES = {
    tuple(): None,
    ("doc-target",): None,
    ("doc-target", 'קו"כ-אם'): None,
    ("doc-target", 'כו"ק'): None,
    ('כו"ק',): None,
    ("מ:דחי",): None,
    (fwh.DUALCANT_ARG_COMBINED, "doc-target"): -2,
    (fwh.DUALCANT_ARG_ALEF,): -1,
    (fwh.DUALCANT_ARG_BET,): -1,
}
