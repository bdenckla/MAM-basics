"""
Exports:
    default_hctx(bcvt=None, renopts=None)
    col_c_hctx(hctx: wt_help.Hctx)
"""

from py_misc import get_cvm_rec_from_bcvt as gcrfb
from py_misc import mam_doc_utils as doc_utils
from py_misc import true_gershayim as true_g2
from py_misc import unbury_doc_parts as unbury
from pycmn import bib_locales as tbn
from pycmn import hebrew_letters as hl
from pycmn import hebrew_points as hpo
from pycmn import hebrew_punctuation as hpu
from pycmn import str_defs as sd
from pycmn import template_names as tmpln
from pycmn import ws_tmpl2 as wtp
from pyrender import render_element as renel
from pyrender import render_wikitext_dispatch as dispatch
from pyrender import render_wikitext_handlers_for_qamats as qamats_variation
from pyrender import render_wikitext_helpers as wt_help
from pyrender import render_wikitext_kq as kq
from pyrender import render_wikitext_spacing_concerns as spacing
from pycmn.my_utils import dv_map
from pycmn.my_utils import first_and_only_and_str
from pycmn.my_utils import st_map


def default_hctx(bcvt=None, renopts=None, io_renlog=None):
    """Return the default Hctx."""
    return wt_help.Hctx(_GEN_WT_HANDLERS, bcvt, renopts, io_renlog)


def col_c_hctx(hctx: wt_help.Hctx):
    """Return a new version of hctx with column C handlers active."""
    return hctx.mk_new_with_handler(_COL_C_HANDLERS)


def _handle_doc(hctx, tmpl):
    assert wtp.template_len(tmpl) >= 3
    doc_target_wtseq = wtp.template_param_val(tmpl, "1")
    doc_target_renseq = wt_help.render_wtseq(hctx, doc_target_wtseq)
    if wt_help.get_renopt(hctx, "ro_no_doc"):
        return doc_target_renseq
    tr_space, doc_target_stripped = spacing.isolate_trailing(doc_target_renseq)
    doc_parts_wtseqs = wtp.template_param_vals(tmpl)[1:]
    doc_parts_wtseqs = unbury.unbury_parts(doc_parts_wtseqs)
    main_out = renel.mk_ren_el_tc_and_doc(
        doc_target_stripped,
        _doc_lemma_subhandler(hctx, doc_target_wtseq),
        _doc_parts_subhandler(hctx, doc_parts_wtseqs),
    )
    return main_out, tr_space


def _handle_bold(hctx, tmpl):
    assert wtp.template_len(tmpl) == 2
    contents = wt_help.render_wtseq(hctx, wtp.template_element(tmpl, 1))
    return renel.mk_ren_el_tc("mam-bold", contents)


def _handle_anchor_with_href_yyy(href_prefix, hctx, tmpl):
    assert wtp.template_len(tmpl) == 3
    href_param_val = wtp.template_param_val(tmpl, "1")
    anchor_contents = wtp.template_param_val(tmpl, "2")
    href_str = first_and_only_and_str(href_param_val)
    acr = wt_help.render_wtseq(hctx, anchor_contents)
    attr = {"href": href_prefix + href_str}
    return renel.mk_ren_el_tc_and_attr("mam-anchor", acr, attr)


def _handle_anchor_with_href_external(hctx, tmpl):
    return _handle_anchor_with_href_yyy("", hctx, tmpl)


def _handle_anchor_with_href_internal(hctx, tmpl):
    return _handle_anchor_with_href_yyy("https://he.wikisource.org/wiki/", hctx, tmpl)


def _ignore(_hctx, _tmpl):
    return ""


def _handle_scrdfftar(hctx, tmpl):
    """
    This is displayed on Wikisource as a footnote.
    Don't confuse this template with the much more common
    documentation template (נוסח).
    """
    assert wtp.template_len(tmpl) == 4
    targ_ren_el = _mrel_fr_tel("sdt-target", hctx, tmpl, wtp.SDT_EL_IDX_FOR_TARG)
    note_renseq = wt_help.render_tmpl_el(hctx, tmpl, wtp.SDT_EL_IDX_FOR_NOTE)
    starpos_in = wtp.template_i0(tmpl, wtp.SDT_EL_IDX_FOR_STARPOS)
    #
    note_renseq = true_g2.in_seq(note_renseq)
    #
    note_ren_el = renel.mk_ren_el_tc("sdt-note", note_renseq)
    contents = targ_ren_el, note_ren_el
    attr = {"sdt-starpos": _ATTR_VAL_FROM_ALEFS[starpos_in]}
    return renel.mk_ren_el_tc_and_attr("scrdfftar", contents, attr)


_ATTR_VAL_FROM_ALEFS = {
    "*אאא": "before-word",
    "אאא*": "after-word",
}


def _mrel_fr_tel(tag, hctx, tmpl, index):
    # Make ren_el from tmpl_el
    return renel.mk_ren_el_tc(tag, wt_help.render_tmpl_el(hctx, tmpl, index))


def _ren_to_str(hctx, tmpl, index):
    ren_el = wt_help.render_tmpl_el(hctx, tmpl, index)
    return first_and_only_and_str(ren_el)


def _handle_slh_word(hctx, tmpl):
    assert wtp.template_len(tmpl) == 6
    targ_renseq = wt_help.render_tmpl_el(hctx, tmpl, wtp.SLHW_EL_IDX_FOR_TARG)
    if wt_help.get_renopt(hctx, "ro_no_slh_word"):
        return targ_renseq
    kais = (  # kai: key and index
        ("slhw-desc-0", wtp.SLHW_EL_IDX_FOR_DESC0),
        ("slhw-desc-1", wtp.SLHW_EL_IDX_FOR_DESC1),
        ("slhw-desc-2", wtp.SLHW_EL_IDX_FOR_DESC2),
        ("slhw-desc-3", wtp.SLHW_EL_IDX_FOR_DESC3),
    )
    attr = {kai[0]: _ren_to_str(hctx, tmpl, kai[1]) for kai in kais}
    return renel.mk_ren_el_tc_and_attr("slh-word", targ_renseq, attr)


_THSP = renel.mk_ren_el_t("ren-tag-thin-space")
_NBSP = renel.mk_ren_el_t("ren-tag-no-break-space")


def _handle_paseq(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    nbsp_dvl_sp = _NBSP, sd.DOUB_VERT_LINE + " "
    return _abstract_default(hctx, renel.mk_ren_el_t("lp-paseq"), nbsp_dvl_sp)


def _handle_legarmeih_2(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    ren_el_abst = renel.mk_ren_el_t("lp-legarmeih")
    thin_pas = _THSP, hpu.PASOLEG
    return _abstract_default(hctx, (ren_el_abst,), thin_pas)


def _handle_gray_maqaf(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    return _abstract_default(
        hctx,
        renel.mk_ren_el_t("implicit-maqaf"),
        renel.mk_ren_el_tc("mam-implicit-maqaf", hpu.MAQ),
    )


def _handle_stress_of_dexi_word(hctx, tmpl):
    assert wtp.template_len(tmpl) in (2, 3)
    return wt_help.render_tmpl_el(hctx, tmpl, 1)


def _handle_stress_of_tsinnor_word(hctx, tmpl):
    assert wtp.template_len(tmpl) in (2, 3)
    return wt_help.render_tmpl_el(hctx, tmpl, 1)


def _handle_dualcant(hctx, tmpl):
    assert wtp.template_len(tmpl) == 4
    # {{מ:כפול|כפול=גגג|א=דדד|ב=ההה}}
    rv_cant = wt_help.get_renopt(hctx, "ro_cantillation") or "rv-cant-combined"
    all_3_cant_dab_values = "rv-cant-combined", "rv-cant-alef", "rv-cant-bet"
    if rv_cant == "rv-cant-all-three":
        cant_ren_els = tuple(
            _ren_el_for_cant(hctx, tmpl, cant_dab) for cant_dab in all_3_cant_dab_values
        )
        cant_ren_els_cont = _contents(cant_ren_els)
        if _equal(cant_ren_els_cont):
            return cant_ren_els_cont[0]
        return renel.mk_ren_el_tc("cant-all-three", cant_ren_els)
    assert rv_cant in all_3_cant_dab_values
    ren_el = _ren_el_for_cant(hctx, tmpl, rv_cant)
    return ren_el["contents"]


def _contents(ren_els):
    return tuple(map(renel.get_ren_el_contents, ren_els))


def _equal(seq):
    if seq[0] != seq[1]:
        return False
    if len(seq) > 2:
        return _equal(seq[1:])
    return True


def _ren_el_for_cant(hctx, tmpl, cant_dab):
    param_name, cant_tag = _DUALCANT_ARG_HELPER_DIC[cant_dab]
    rendered_cant = wt_help.render_named_param_val(hctx, tmpl, param_name)
    return renel.mk_ren_el_tc(cant_tag, rendered_cant)


def _doc_lemma_subhandler(hctx: wt_help.Hctx, doc_target_wtseq):
    # XXX TODO Above, would it be better to return something like '{רווח}'?
    # See https://github.com/bdenckla/MAM-for-Acc/issues/33.
    if doc_lemma := _map_doc_target_to_doc_lemma(doc_target_wtseq):
        return doc_lemma
    tmp_hctx = hctx.mk_new_with_handler(_DOC_LEMMA_HANDLERS)
    doc_lemma = wt_help.render_wtseq(tmp_hctx, doc_target_wtseq)
    assert doc_lemma and doc_lemma != (" ",)
    assert not spacing.general_endswith(doc_lemma[-1], " ")
    return doc_lemma


def _map_doc_target_to_doc_lemma(doc_target_wtseq):
    if len(doc_target_wtseq) != 1:
        return None
    wtel = doc_target_wtseq[0]
    if wtp.is_template(wtel):
        el1_00 = wtp.template_i0(wtel, 0)
        if remap := doc_utils.LEMMA_FROM_TMPL.get(el1_00):
            return remap
    elif isinstance(wtel, str):
        # we no longer support (or need to support) "doc of nothing" (doc of the empty string)
        assert wtel != ""
        if remap := doc_utils.LEMMA_FROM_STR.get(wtel):
            return remap
    return None


def _handle_kq_trivial_qere(hctx, tmpl):
    """
    Handle a ketiv/qere that is trivial: contains only a qere and a note.
    """
    assert wtp.template_len(tmpl) == 3
    qere = wt_help.render_tmpl_el(hctx, tmpl, 1)
    # note = wt_help.render_tmpl_el(hctx, tmpl, 2)  # e.g. ל-קרי=חֲטָאָֽיו.
    return renel.mk_ren_el_tc("mam-kq-trivial", qere)


def _doc_parts_subhandler(hctx: wt_help.Hctx, doc_parts_wtseqs):
    tmp_hctx = hctx.mk_new_with_handler(_DOC_PARTS_HANDLERS)
    return st_map((wt_help.render_wtseq, tmp_hctx), doc_parts_wtseqs)


def _sampe_args_okay(tmpl):
    return wtp.template_len(tmpl) <= 2 and (
        wtp.template_len(tmpl) == 1
        or wtp.template_param_val(tmpl, "1") == ["פסקא באמצע פסוק"]
    )


def _handle_samekh2_in_c(hctx, tmpl):
    assert _sampe_args_okay(tmpl)
    return _render_sampe(hctx, "samekh2", in_c=True)


def _handle_samekh2_in_e(hctx, tmpl):
    assert _sampe_args_okay(tmpl)
    return _render_sampe(hctx, "samekh2")


def _is_nu10_35_or_36(hctx: wt_help.Hctx):
    """Return whether hctx.bcvt is Numbers 10:35 or 10:36"""
    bcvt = hctx.bcvt
    vtrad = tbn.bcvt_get_vtrad(bcvt)
    out = bcvt in (tbn.nu10(35, vtrad), tbn.nu10(36, vtrad))
    if out:
        cvm_rec = gcrfb.get_cvm_rec_from_bcvt(bcvt)
        # Below we assert that bcvt is the same in the MAM vtrad.
        assert cvm_rec is None
    return out


def _handle_samekh3_in_c(hctx, tmpl):
    assert _sampe_args_okay(tmpl)
    return _render_sampe(hctx, "samekh3", in_c=True)


def _handle_samekh3_in_e(hctx, tmpl):
    assert _sampe_args_okay(tmpl)
    if _is_nu10_35_or_36(hctx):
        return _abstract_default(
            hctx,
            renel.mk_ren_el_t("spi-samekh3-nu10-invnun-neighbor"),
            _NBSP,
        )
    return _render_sampe(hctx, "samekh3")


def _handle_pe2_in_c(hctx, tmpl):
    assert _sampe_args_okay(tmpl)
    return _render_sampe(hctx, "pe2", in_c=True)


def _handle_pe2_in_e(hctx, tmpl):
    assert _sampe_args_okay(tmpl)
    return _render_sampe(hctx, "pe2")


def _handle_pe3_in_c(hctx, tmpl):
    assert _sampe_args_okay(tmpl)
    return _render_sampe(hctx, "pe3", in_c=True)


def _handle_pe3_in_e(hctx, tmpl):
    assert _sampe_args_okay(tmpl)
    return _render_sampe(hctx, "pe3")


def _render_sampe(hctx, sampe, in_c=False):
    tag_abst = {
        "samekh2": "spi-samekh2",
        "samekh3": "spi-samekh3",
        "pe2": "spi-pe2",
        "pe3": "spi-pe3",
    }
    return _abstract_default(
        hctx,
        renel.mk_ren_el_t(tag_abst[sampe]),
        _render_sampe_default(sampe, in_c),
    )


def _sampe_dic2_el(sp1val):
    he_sam_or_he_pe, tag_defa, postwh = sp1val
    core = "{" + he_sam_or_he_pe + "}"
    ren_el_defa = renel.mk_ren_el_tc(tag_defa, core)
    return ren_el_defa, postwh


_REN_EL_BR_AFTER_PE = renel.mk_ren_el_t("mam-br-after-pe")
_REN_EL_OCTO_SPACE = renel.mk_ren_el_t("ren-tag-octo-space")
_SAMPE_DIC = {
    "samekh2": (hl.SAMEKH, "mam-spi-samekh", _REN_EL_OCTO_SPACE),
    "samekh3": (hl.SAMEKH, "mam-spi-samekh", _REN_EL_OCTO_SPACE),
    "pe2": (hl.PE, "mam-spi-pe", _REN_EL_BR_AFTER_PE),
    "pe3": (hl.PE, "mam-spi-pe", _REN_EL_BR_AFTER_PE),
}
_SAMPE_DIC2 = dv_map(_sampe_dic2_el, _SAMPE_DIC)


def _render_sampe_default(sampe, in_c):
    ren_el_defa, whitespace = _SAMPE_DIC2[sampe]
    if in_c:
        return ren_el_defa
    return " ", ren_el_defa, whitespace


def _handle_large_letter(hctx, tmpl):
    return _slh_letter_subhandler("large", hctx, tmpl)


def _handle_small_letter(hctx, tmpl):
    return _slh_letter_subhandler("small", hctx, tmpl)


def _handle_hung_letter(hctx, tmpl):  # aka raised or suspended
    return _slh_letter_subhandler("hung", hctx, tmpl)


def _slh_letter_subhandler(slh_type, hctx, tmpl):
    assert wtp.template_len(tmpl) == 2
    inner_handled = wt_help.render_tmpl_el(hctx, tmpl, 1)  # e.g. ('בְּ',)
    if wt_help.get_renopt(hctx, "ro_no_formatting_for_slh"):
        return inner_handled
    type_to_tag = {
        "small": "mam-letter-small",
        "large": "mam-letter-large",
        "hung": "mam-letter-hung",
    }
    return renel.mk_ren_el_tc(type_to_tag[slh_type], inner_handled)


def _handle_poetic_space_resh0123(_hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    return " "


def _handle_shirah_space(hctx, tmpl):
    assert wtp.template_len(tmpl) == 1
    return _abstract_default(hctx, renel.mk_ren_el_t("shirah-space"), sd.OCTO_NBSP)


def _handle_inverted_nun(hctx, tmpl):
    assert wtp.template_len(tmpl) == 2
    t10 = wtp.template_i0(tmpl, 1)
    add_tr_space = t10 == hpu.NUN_HAF + "__"
    assert add_tr_space or t10 == hpu.NUN_HAF
    if not add_tr_space:
        assert _is_nu10_35_or_36(hctx)
    maybe_nbsp = _NBSP if add_tr_space else ""
    ren_el_defa = renel.mk_ren_el_tc("mam-spi-invnun", hpu.NUN_HAF)
    defa_maybe_nbsp = ren_el_defa, maybe_nbsp
    return _abstract_default(
        hctx,
        _ren_el_abst_for_inverted_nun(add_tr_space),
        defa_maybe_nbsp,
    )


def _abstract_default(hctx, abst, defa):
    style = wt_help.get_renopt(hctx, "ro_render_style")
    dic = {"abstract": abst, None: defa}
    return dic[style]


def _ren_el_abst_for_inverted_nun(add_tr_space):
    tagmap = {True: "spi-invnun-including-trailing-space", False: "spi-invnun"}
    return renel.mk_ren_el_t(tagmap[add_tr_space])


def _handle_wikitext_str(hctx, string):
    if wt_help.get_renopt(hctx, "ro_no_varika"):
        return string.translate(hpo.DROP_VARIKA)
    return string


def _handle_wikitext_str_in_doc_part(_hctx, string):
    return true_g2.in_str(string)


def _handle_good_ending_in_body(hctx, tmpl):
    assert wtp.template_len(tmpl) == 2
    inner_handled = wt_help.render_tmpl_el(hctx, tmpl, 1)
    the_ren_el_c = renel.mk_ren_el_tc("mam-good-ending", inner_handled)
    style = wt_help.get_renopt(hctx, "ro_render_style")
    if style == "abstract":
        return the_ren_el_c
    assert style is None  # i.e., the default style
    br_before_good_ending = renel.mk_ren_el_t("mam-br-before-good-ending")
    return br_before_good_ending, the_ren_el_c


def _handle_good_ending_in_doc_lemma(hctx, tmpl):
    assert wtp.template_len(tmpl) == 2
    inner_handled = wt_help.render_tmpl_el(hctx, tmpl, 1)
    ih0 = first_and_only_and_str(inner_handled)
    words = ih0.split(" ")
    abbrev = words[0] + " ... " + words[-1]
    return (abbrev,)


_MASK_E = "e"  # cell E
_MASK_C = "c"  # cell C
_MASK_L = "l"  # doc lemma
_MASK_P = "p"  # doc part
_MASK_EC = "ec"
_MASK_EL = "el"
_MASK_ECL = "ecl"
_MASK_ELP = "elp"
_HANDLER_SPECS_FOR_KETIV_QERE = {
    **tmpln.map_all_std_kq_to_a_constant({_MASK_EL: kq.handle_kq}),
    'קו"כ-אם': {_MASK_EL: _handle_kq_trivial_qere},
    "קרי ולא כתיב": {_MASK_EL: kq.handle_kq_qere_velo_ketiv},
    "כתיב ולא קרי": {_MASK_EL: kq.handle_kq_ketiv_velo_qere},
}
_HANDLER_SPECS_FOR_WHITESPACE = {
    "ססס": {_MASK_C: _handle_samekh3_in_c, _MASK_E: _handle_samekh3_in_e},
    "סס": {_MASK_C: _handle_samekh2_in_c, _MASK_E: _handle_samekh2_in_e},
    "פפפ": {_MASK_C: _handle_pe3_in_c, _MASK_E: _handle_pe3_in_e},
    "פפ": {_MASK_C: _handle_pe2_in_c, _MASK_E: _handle_pe2_in_e},
    "ר4": {_MASK_C: _ignore},
    "ר3": {_MASK_E: _handle_poetic_space_resh0123},
    "ר2": {_MASK_E: _handle_poetic_space_resh0123},
    "ר1": {_MASK_EL: _handle_poetic_space_resh0123, _MASK_C: _ignore},
    "ר0": {_MASK_EL: _handle_poetic_space_resh0123},
    "מ:ששש": {_MASK_EC: _handle_shirah_space},
    tmpln.NO_PAR_AT_STA_OF_CHAP21: {_MASK_C: _ignore},
    tmpln.NO_PAR_AT_STA_OF_CHAP03: {_MASK_C: _ignore},
    tmpln.NO_PAR_AT_STA_OF_WEEKLY: {_MASK_C: _ignore},
    "מ:רווח לספר בתהלים בפסוק הראשון": {_MASK_C: _ignore},
    "מ:רווח בתרי עשר בפסוק הראשון": {_MASK_C: _ignore},
}
_HANDLER_SPECS_FOR_MISC = {
    str: {_MASK_ECL: _handle_wikitext_str, _MASK_P: _handle_wikitext_str_in_doc_part},
    "מודגש": {_MASK_P: _handle_bold},
    "מ:קישור בהערה": {_MASK_P: _handle_anchor_with_href_external},
    "מ:קישור פנימי בהערה": {_MASK_P: _handle_anchor_with_href_internal},
    "__": {_MASK_C: _ignore},
    "נוסח": {_MASK_EC: _handle_doc},
    tmpln.SCRDFF_NO_TAR: {_MASK_EC: _ignore},
    tmpln.SCRDFF_TAR: {_MASK_EC: _handle_scrdfftar},
    tmpln.SLH_WORD: {_MASK_ELP: _handle_slh_word},
    "מ:לגרמיה-2": {_MASK_ELP: _handle_legarmeih_2},
    "מ:פסק": {_MASK_ELP: _handle_paseq},
    "מ:מקף אפור": {_MASK_EL: _handle_gray_maqaf},
    "מ:דחי": {_MASK_EL: _handle_stress_of_dexi_word},
    "מ:צינור": {_MASK_EL: _handle_stress_of_tsinnor_word},
    "מ:קמץ": {_MASK_EL: qamats_variation.handle},
    "מ:אות-ק": {_MASK_ELP: _handle_small_letter},
    "מ:אות-ג": {_MASK_ELP: _handle_large_letter},
    "מ:אות תלויה": {_MASK_EL: _handle_hung_letter},
    'מ:נו"ן הפוכה': {_MASK_EL: _handle_inverted_nun},
    "מ:כפול": {_MASK_EC: _handle_dualcant},
    "מ:סיום בטוב": {
        _MASK_E: _handle_good_ending_in_body,
        _MASK_L: _handle_good_ending_in_doc_lemma,
    },
}
_HANDLER_SPECS = {
    **_HANDLER_SPECS_FOR_KETIV_QERE,
    **_HANDLER_SPECS_FOR_WHITESPACE,
    **_HANDLER_SPECS_FOR_MISC,
}
_GEN_WT_HANDLERS = dispatch.make_handler_table(_HANDLER_SPECS, "e")
_COL_C_HANDLERS = dispatch.make_handler_table(_HANDLER_SPECS, "c")
_DOC_PARTS_HANDLERS = dispatch.make_handler_table(_HANDLER_SPECS, "p")
_DOC_LEMMA_HANDLERS = dispatch.make_handler_table(_HANDLER_SPECS, "l")
_DUALCANT_ARG_HELPER_DIC = {
    "rv-cant-combined": (str("כפול"), "cant-combined"),
    "rv-cant-alef": (str("א"), "cant-alef"),
    "rv-cant-bet": (str("ב"), "cant-bet"),
}
#######################################################################
# Notes on ignored templates:
#
# We ignore plain scrdff templates in favor of (synthesized)
# scrdfftar templates.
#
# resh1_in_col_c happens only two times:
#    between verses 1 and 2 of Psalm 70 and
#    between verses 1 and 2 of Psalm 108.
#
# We ignore resh4, as we do '__'.
#
#######################################################################
#
# The כפול argument has the combined cantillation.
# The א argument has the cantillation known as
#     תחתון in the Decalogues and פשוטה in G35:22.
# The ב argument has the cantillation known as
#     עליון in the Decalogues and מדרשית in G35:22.
# I.e.:
#     In the Decalogues, א/ב is תחתון/עליון.
#     In G35:22,         א/ב is פשוטה/מדרשית.
#
#######################################################################
