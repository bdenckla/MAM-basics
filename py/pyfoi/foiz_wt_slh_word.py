from pyfoi import foi_struct as fct
from pyfoi import foi_wikitext_helpers as fwh
from py_misc import ren_html_from_ren_el_mapping as hfrm
from py_misc import ren_html_for_renel as hfr
from pycmn import ws_tmpl2 as wtp
from pyrender import render_element as renel
from pyrender import render_wikitext_handlers as handlers
from pyrender import render_wikitext_helpers as wt_help
from py_misc import slh_description
from pycmn import template_names as tmpln
from pycmn.my_utils import first_and_only


def find_fois_wt(mroge):
    """Find slh word templates: they are the feature of interest."""
    return fwh.find_fois_in_minirow_ep(_FOILERS, mroge)


def _record_slh_word_as_foi(_foilers, stack, tmpl):
    desc_parts = slh_description.get_parts(wtp.template_element(tmpl, 1))
    desc_str = slh_description.desc_parts_shown_as_a_str(desc_parts)
    slh_count = len(desc_parts[2])
    assert slh_count > 0
    slh_parts_htseq = (desc_str,)
    stack_summary = fwh.stack_summary(_STACK_SUMMARIES, stack)
    foi_qualifier = {
        "html": _html_for_wtseq((tmpl,)),
        "stack_str": stack_summary,
    }
    foi_target = fct.make_qtarget(slh_parts_htseq, foi_qualifier)
    foi1_path = "slh-word", "slh-letter-count", str(slh_count)
    foi2_path = "slh-word", "stack", str(stack_summary)
    foi3_path = "slh-word", "non-note", str(slh_count), desc_parts[2]
    foi1 = foi1_path, foi_target
    foi2 = foi2_path, foi_target
    foi3 = foi3_path, foi_target
    return [foi1, foi2, *_maybe_foi3(foi3, stack)]


def _maybe_foi3(foi3, stack):
    if _STACK_INDICATES_A_NOTE[stack]:
        return []
    return [foi3]


def _html_for_wtseq(wtseq):
    hctx = handlers.default_hctx()
    renseq = wt_help.render_wtseq(hctx, wtseq)
    hfr_ctx = hfr.HfrCtx(hfrm.HT_TAC_FOR_RT_FOR_SLH_WORD_FOI)
    the_renel = first_and_only(renseq)
    attr = renel.get_ren_el_attr(the_renel)
    new_attr = {**attr, "lang": "hbo"}
    tag_and_contents = renel.get_ren_el_tc(the_renel)
    new_renel = renel.mk_ren_el_tc_and_attr(*tag_and_contents, new_attr)
    new_renseq = (new_renel,)
    return hfr.html_for_ren_el(hfr_ctx, new_renseq)


_FOILERS = {
    tmpln.SLH_WORD: _record_slh_word_as_foi,
    'כו"ק': fwh.label_args_of_ketiv_qere,
    "נוסח": fwh.label_args_of_doc,
    tmpln.SCRDFF_TAR: fwh.label_args_of_scrdfftar,
    tmpln.SCRDFF_NO_TAR: fwh.ignore,
}
_STACK_SUMMARIES = {
    tuple(): None,
    ("doc-target",): None,
    ("doc-target", "scrdfftar-tar"): None,
    ("doc-target", "מ:דחי"): None,
    #
    ("doc-target", "scrdfftar-note"): -1,
    ("doc-target", "kq-ketiv"): -1,
    ("scrdfftar-note",): -1,
    ("doc-part-n",): -1,
}
_STACK_INDICATES_A_NOTE = {
    tuple(): False,
    ("doc-target",): False,
    ("doc-target", "scrdfftar-tar"): False,
    ("doc-target", "מ:דחי"): False,
    #
    ("doc-target", "scrdfftar-note"): True,
    ("doc-target", "kq-ketiv"): False,
    ("scrdfftar-note",): True,
    ("doc-part-n",): True,
}
