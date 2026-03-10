""" Exports convert """

from pycmn import ws_tmpl2 as wtp
from py_misc import unbury_doc_parts as unbury
from pycmn import my_utils
from pycmn import shrink


def convert(bcvt, wtseq, io_renlog=None):
    """
    For each trivial qere at the top level of Wikitext sequence wtseq,
    turn that trivial qere into a doc.

    For each doc at the top level of wtseq,
    if that doc's target includes a trivial qere,
    fold that trivial qere's pseudo-doc into the doc parts.

    We only care about top level because other code
    recurses and ends up calling this again at lower
    levels.
    """
    io_renlog = _prep_log(io_renlog)
    return my_utils.ss_map((_convert, bcvt, io_renlog), wtseq)


def _convert(bcvt, io_renlog, wtel):
    if _is_trivial_qere_tmpl(wtel):
        io_renlog["undocumented_trivial_qere"].append(bcvt)
        return _make_doc_tmpl(0, [wtel], [])
    if _is_doc_whose_targ_includes_trivial_qere(wtel):
        return _convert_doc_of_trivial_qere(bcvt, io_renlog, wtel)
    return wtel


def _make_doc_tmpl(trqr_idx, existing_doc_targ, existing_doc_parts):
    trivial_qere = existing_doc_targ[trqr_idx]
    trqr_targ = wtp.template_param_val(trivial_qere, "1")
    trqr_note = wtp.template_param_val(trivial_qere, "2")
    new_doc_targ = (
        existing_doc_targ[0:trqr_idx] + trqr_targ + existing_doc_targ[trqr_idx + 1 :]
    )
    new_doc_tmpl_els = [["נוסח"], new_doc_targ]
    prov = _add_provenance(existing_doc_targ, trqr_targ, trqr_note)
    new_doc_tmpl_els.append(prov)
    if existing_doc_parts:
        unburied = unbury.unbury_parts(existing_doc_parts)
        new_doc_tmpl_els.extend(unburied)
    return wtp.mktmpl(new_doc_tmpl_els, ignore_equals=True)


def _convert_doc_of_trivial_qere(bcvt, io_renlog, doc_tmpl):
    # Turn this:
    #     doc(
    #         [..., trqr(trqr_targ, trqr_pseudo_doc), ...]
    #         doc_part1,
    #         doc_part2, ...)
    # into this:
    #     doc(
    #         [..., *trqr_targ, ...]
    #         trqr_pseudo_doc,
    #         doc_part1,
    #         doc_part2, ...)
    doc_tmpl_pvs = wtp.template_param_vals(doc_tmpl)
    doc_tmpl_pv0 = doc_tmpl_pvs[0]
    _log(bcvt, io_renlog, doc_tmpl_pv0)
    trqr_idx = _find_index_of_trivial_qere_within_doc_targ(doc_tmpl)
    return _make_doc_tmpl(trqr_idx, doc_tmpl_pv0, doc_tmpl_pvs[1:])


def _is_doc_whose_targ_includes_trivial_qere(wtel):
    if not wtp.is_doc_template(wtel):
        return False
    trqr_idx = _find_index_of_trivial_qere_within_doc_targ(wtel)
    return trqr_idx is not None


def _find_index_of_trivial_qere_within_doc_targ(doc_wtel):
    doc_targ = wtp.template_param_val(doc_wtel, "1")
    trivial_qere_index = None
    for i, doc_targ_wtel in enumerate(doc_targ):
        if _is_trivial_qere_tmpl(doc_targ_wtel):
            assert trivial_qere_index is None
            trivial_qere_index = i
    return trivial_qere_index


def _is_trivial_qere_tmpl(wtel):
    return wtp.is_template_with_name(wtel, 'קו"כ-אם')


def _add_provenance(existing_doc_targ, trqr_targ, trqr_note):
    wtseq = []
    wtseq.append("(קו״כ-אם")
    if len(existing_doc_targ) > 1:
        wtseq.append(" ")
        wtseq.extend(trqr_targ)
    wtseq.append(")")
    # at this point, wtseq is either ['(קו״כ-אם)'] or ['(קו״כ-אם מָרִ֥אי)']
    wtseq.append(" ")
    wtseq.extend(trqr_note)
    wtseq = shrink.shrink(wtseq)
    return wtseq


def _prep_log(io_renlog):
    if io_renlog is None:
        io_renlog = {}
    if io_renlog is not None:
        my_utils.maybe_init_at_key(io_renlog, "undocumented_trivial_qere", [])
        my_utils.maybe_init_at_key(io_renlog, "doc_of_trivial_qere_only", [])
        my_utils.maybe_init_at_key(io_renlog, "doc_of_trivial_qere_and_other_stuff", [])
    return io_renlog


def _log(bcvt, io_renlog, doc1):
    if len(doc1) == 1:
        # Deut 22:16 is a current case of this
        io_renlog["doc_of_trivial_qere_only"].append(bcvt)
    else:
        # Daniel 4:21 is the only current case of this
        io_renlog["doc_of_trivial_qere_and_other_stuff"].append(bcvt)
