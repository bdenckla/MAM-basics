"""Exports convert"""

from mb_cmn import ws_tmpl2 as wtp
from mb_cmn import template_names as tmpln
from py_misc import unbury_doc_parts as unbury
from py_misc import true_gershayim as true_g2
from mb_cmn import my_utils


def convert(wtseq):  # wtseq: Wikitext sequence (list or tuple)
    """
    For each scrdfftar at the top level of wtseq,
    turn that scrdfftar into a doc.

    For each doc at the top level of wtseq,
    if that doc's target is a scrdfftar,
    fold that scrdfftar's contents into the doc.

    Fail fast if any non-targeted scrdff appears at top level.

    We only care about top level because other code
    recurses and ends up calling this again at lower
    levels.
    """
    _assert_no_non_targeted_scrdff_at_top_level(wtseq)
    return my_utils.ss_map(_convert, wtseq)


def _convert(wtel):
    if _is_scrdfftar_tmpl(wtel):
        return _make_doc_tmpl(wtel, [])
    if _is_doc_of_scrdfftar(wtel):
        return _convert_doc_of_scrdfftar(wtel)
    return wtel


def _make_doc_tmpl(scrdfftar, existing_doc_parts):
    scrdfftar_targ = wtp.template_element(scrdfftar, wtp.SDT_EL_IDX_FOR_TARG)
    scrdfftar_note = wtp.template_element(scrdfftar, wtp.SDT_EL_IDX_FOR_NOTE)
    # In this context, we don't care about starpos
    new_doc_tmpl_els = [["נוסח"], scrdfftar_targ]
    new_doc_tmpl_els.append(_tweak_scrdfftar_text(scrdfftar_note))
    if existing_doc_parts:
        existing_doc_parts = unbury.unbury_parts(existing_doc_parts)
        new_doc_tmpl_els.extend(existing_doc_parts)
    return wtp.mktmpl(new_doc_tmpl_els, ignore_equals=True)


def _tweak_scrdfftar_text(scrdfftar_text):
    return _add_provenance(true_g2.in_seq(scrdfftar_text))


def _convert_doc_of_scrdfftar(doc_tmpl):
    # Turn this:
    #     doc(
    #         [scrdfftar(scrdfftar_targ, scrdfftar_text)],
    #         doc_part1,
    #         doc_part2, ...)
    # into this:
    #     doc(
    #         scrdfftar_targ,
    #         scrdfftar_text,
    #         doc_part1,
    #         doc_part2, ...)
    doc_tmpl_pvs = wtp.template_param_vals(doc_tmpl)
    scrdfftar = my_utils.first_and_only(doc_tmpl_pvs[0])
    return _make_doc_tmpl(scrdfftar, doc_tmpl_pvs[1:])


def _assert_no_non_targeted_scrdff_at_top_level(wtseq):
    for wtel in wtseq:
        if wtp.is_scrdff_template(wtel):
            raise RuntimeError(
                "Unexpected non-targeted scroll-difference template "
                f"{tmpln.SCRDFF_NO_TAR} in plus scrdfftar-to-doc conversion"
            )


def _is_doc_of_scrdfftar(wtel):
    if not wtp.is_doc_template(wtel):
        return False
    doc1 = wtp.template_element(wtel, 1)
    return len(doc1) == 1 and _is_scrdfftar_tmpl(doc1[0])


def _is_scrdfftar_tmpl(wtel):
    return wtp.is_template_with_name(wtel, tmpln.SCRDFF_TAR)


def _add_provenance(scrdfftar_text):
    assert isinstance(scrdfftar_text[0], str)
    new_scrdfftar_text_0 = "(מ:הערה) " + scrdfftar_text[0]
    return [new_scrdfftar_text_0, *scrdfftar_text[1:]]
