from foi import foi_struct as fct
from foi import foi_wikitext_helpers as fwh
from py_misc import ren_html_from_ren_el_mapping as hfrm
from py_misc import ren_html_for_renel as hfr
from mb_cmn import ws_tmpl2 as wtp
from render_wt import render_wikitext_handlers as handlers
from render_wt import render_wikitext_helpers as wt_help
from mb_cmn import kq_special_templates as kqst
from mb_cmn import template_names as tmpln
from foi import kq_trivial_types
from foi import kq_trivial_sug


def find_fois_wt(mroge):
    """Find ketiv/qere template uses: they are the feature of interest."""
    return fwh.find_fois_in_minirow_ep(_FOILERS, mroge)


def _record_kq_as_foi(_foilers, stack, tmpl):
    tmpl_name = wtp.template_name(tmpl)
    kq_type = _kq_type_for_tmpl(tmpl)
    foi_path = "kq-simple", _FOI_PATH[kq_type]
    stack_summary = fwh.stack_summary(_STACK_SUMMARIES, stack)
    foi_target_proper = _html_for_wtseq((tmpl,))
    foi_qualifier = {}
    if kqst.is_special_kq_template_name(tmpl_name):
        foi_qualifier["kq_type_full"] = kq_type
    if tmpl_name == "מ:קו״כ-אם-2":
        reconciled_subtype, reconciled_qualifier = (
            kq_trivial_sug.reconcile_subtype_for_foi(tmpl)
        )
        foi_path = *foi_path, reconciled_subtype
        foi_qualifier["pqere"] = kq_trivial_types.pointed_qere_text(tmpl)
        foi_qualifier.update(reconciled_qualifier)
    if stack_summary:
        foi_qualifier["stack_str"] = stack_summary
    if not foi_qualifier:
        foi_target = foi_target_proper
    else:
        foi_target = fct.make_qtarget(foi_target_proper, foi_qualifier)
    return [(foi_path, foi_target)]


def _html_for_wtseq(wtseq):
    hctx = handlers.default_hctx()
    renseq = wt_help.render_wtseq(hctx, wtseq)
    hfr_ctx = hfr.HfrCtx(hfrm.HT_TAC_FOR_RT_FOR_KETIV_QERE_FOI)
    return hfr.html_for_ren_el(hfr_ctx, renseq)


def _sug_text_if_present(tmpl):
    if "סוג" not in wtp.template_param_keys(tmpl):
        return None
    sug_val = wtp.template_param_val(tmpl, "סוג")
    assert len(sug_val) == 1 and isinstance(sug_val[0], str), sug_val
    return sug_val[0]


def _kq_type_for_tmpl(tmpl):
    tmpl_name = wtp.template_name(tmpl)
    if kqst.is_special_kq_template_name(tmpl_name):
        assert kqst.is_unified_special_kq_template_name(tmpl_name), tmpl_name
        sug_text = _sug_text_if_present(tmpl)
        assert sug_text is not None, tmpl
        return kqst.canonical_special_kq_type_from_name_and_sug(tmpl_name, sug_text)
    return tmpln.LATIN_SHORTS[tmpl_name]


_FOI_PATH = {
    "kq-q-velo-k": "x-velo-y-q-velo-k",
    "kq-k-velo-q": "x-velo-y-k-velo-q",
    "k1q1-kq": "k1q1",
    "k1q1-qk": "k1q1-qk",
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
    "כו״ק": _record_kq_as_foi,
    "קו״כ": _record_kq_as_foi,
    kqst.UNIFIED_SPECIAL_KQ_TEMPLATE_NAME: _record_kq_as_foi,
    "מ:קו״כ-אם-2": _record_kq_as_foi,
    "קרי ולא כתיב": _record_kq_as_foi,
    "כתיב ולא קרי": _record_kq_as_foi,
}
_FOILERS = {
    **_FOILERS_FOR_KETIV_QERE,
    #
    "מ:כפול": fwh.label_args_of_dualcant,
    "נוסח": fwh.label_args_of_doc,
    tmpln.SCRDFF_TAR: fwh.label_args_of_scrdfftar,
    tmpln.SCRDFF_NO_TAR: fwh.fail_on_unexpected_template_in_plus,
}
_STACK_SUMMARIES = {
    tuple(): None,
    ("doc-target",): None,
    ("doc-target", "מ:קו״כ-אם-2"): None,
    ("doc-target", "כו״ק"): None,
    ("doc-target", kqst.UNIFIED_SPECIAL_KQ_TEMPLATE_NAME): None,
    ("כו״ק",): None,
    (kqst.UNIFIED_SPECIAL_KQ_TEMPLATE_NAME,): None,
    ("מ:דחי",): None,
    (fwh.DUALCANT_ARG_COMBINED, "doc-target"): -2,
    (fwh.DUALCANT_ARG_ALEF,): -1,
    (fwh.DUALCANT_ARG_BET,): -1,
}
