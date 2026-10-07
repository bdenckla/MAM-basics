"""Exports convert"""

from mb_cmn import ws_tmpl2 as wtp
from mb_cmn import template_names as tmpln  # near-aleppo
from py_misc import near_aleppo_params as nap  # near-aleppo
from py_misc import unbury_doc_parts as unbury
from mb_cmn import my_utils
from mb_cmn import shrink


def convert(bcvt, wtseq, io_renlog=None):
    """
    For each trivial ketiv/qere at the top level of Wikitext sequence
    wtseq, turn that trivial ketiv/qere into a doc.

    For each doc at the top level of wtseq,
    if that doc's target includes a trivial ketiv/qere,
    fold that trivial ketiv/qere's pseudo-doc into the doc parts.

    We only care about top level because other code
    recurses and ends up calling this again at lower
    levels.
    """
    io_renlog = _prep_log(io_renlog)
    return my_utils.ss_map((_convert, bcvt, io_renlog), wtseq)


def _convert(bcvt, io_renlog, wtel):
    if _is_trivial_ketiv_qere_tmpl(wtel):
        io_renlog["undocumented_trivial_ketiv_qere"].append(bcvt)
        return _make_doc_tmpl(0, [wtel], [])
    if _is_doc_whose_targ_includes_trivial_ketiv_qere(wtel):
        return _convert_doc_of_trivial_ketiv_qere(bcvt, io_renlog, wtel)
    return wtel


def _make_doc_tmpl(
    tkq_idx, existing_doc_targ, existing_doc_parts, doc_name="נוסח", doc_added=None
):
    # near-aleppo: doc_name and doc_added are the enclosing note's name and the
    # parameters the near-aleppo dataset adds to it, which the new note keeps, after
    # the trivial ketiv/qere's own added parameters, its flags. Each is shown as a
    # line of the note (render_wikitext_handlers._handle_doc).
    trivial_ketiv_qere = existing_doc_targ[tkq_idx]
    _tkq_keys, tkq_added = nap.split_params(trivial_ketiv_qere, _TKQ_KEYS, nap.FLAGS)
    tkq_targ = wtp.template_param_val(trivial_ketiv_qere, "1")
    new_doc_targ = (
        existing_doc_targ[0:tkq_idx] + tkq_targ + existing_doc_targ[tkq_idx + 1 :]
    )
    new_doc_tmpl_els = [[doc_name], new_doc_targ]
    prov = _add_provenance(trivial_ketiv_qere)
    if doc_name == nap.RENAMED_DOC:
        if any(existing_doc_parts):
            raise ValueError(
                "Changed trivial-qere conversions require framed MAM content"
            )
        extra = dict(doc_added or {})
        stored = extra.pop(nap.MAM_NOTE)
        stored = stored if isinstance(stored, list) else [stored]
        extra[nap.MAM_NOTE] = [*prov, {"tmpl_name": "ש"}, *stored]
        new_doc = wtp.mktmpl([[doc_name], new_doc_targ, []], ignore_equals=True)
        new_doc = nap.with_params(new_doc, extra)
        return nap.with_params(new_doc, nap.raw_params(trivial_ketiv_qere, tkq_added))
    new_doc_tmpl_els.append(prov)
    if existing_doc_parts:
        unburied = unbury.unbury_parts(existing_doc_parts)
        new_doc_tmpl_els.extend(unburied)
    new_doc = wtp.mktmpl(new_doc_tmpl_els, ignore_equals=True)
    new_doc = nap.with_params(new_doc, doc_added or {})
    return nap.with_params(new_doc, nap.raw_params(trivial_ketiv_qere, tkq_added))


def _convert_doc_of_trivial_ketiv_qere(bcvt, io_renlog, doc_tmpl):
    # Turn this:
    #     doc(
    #         [..., tkq(tkq_targ, tkq_pseudo_doc), ...]
    #         doc_part1,
    #         doc_part2, ...)
    # into this:
    #     doc(
    #         [..., *tkq_targ, ...]
    #         tkq_pseudo_doc,
    #         doc_part1,
    #         doc_part2, ...)
    #
    # near-aleppo: the note's own numbered parameters, apart from those the near-aleppo
    # dataset adds, which the new note keeps under the note's own name.
    numbered, added = nap.split_doc_params(doc_tmpl)
    doc_tmpl_pvs = [wtp.template_param_val(doc_tmpl, key) for key in numbered]
    doc_tmpl_pv0 = doc_tmpl_pvs[0]
    _log(bcvt, io_renlog, doc_tmpl_pv0)
    tkq_idx = _find_index_of_trivial_ketiv_qere_within_doc_targ(doc_tmpl)
    return _make_doc_tmpl(
        tkq_idx,
        doc_tmpl_pv0,
        doc_tmpl_pvs[1:],
        wtp.template_name(doc_tmpl),
        nap.raw_params(doc_tmpl, added),
    )


def _is_doc_whose_targ_includes_trivial_ketiv_qere(wtel):
    if not nap.is_doc_template(wtel):  # near-aleppo: either note name
        return False
    tkq_idx = _find_index_of_trivial_ketiv_qere_within_doc_targ(wtel)
    return tkq_idx is not None


def _find_index_of_trivial_ketiv_qere_within_doc_targ(doc_wtel):
    doc_targ = wtp.template_param_val(doc_wtel, "1")
    trivial_ketiv_qere_index = None
    for i, doc_targ_wtel in enumerate(doc_targ):
        if _is_trivial_ketiv_qere_tmpl(doc_targ_wtel):
            assert trivial_ketiv_qere_index is None
            trivial_ketiv_qere_index = i
    return trivial_ketiv_qere_index


def _is_trivial_ketiv_qere_tmpl(wtel):
    return wtp.is_template_with_name(wtel, "מ:קו״כ-אם-2")


# near-aleppo: MAM's parameters of the trivial ketiv/qere, as MAM-basics'
# mb_cmn/template_names.py's CURRENT_PLUS_PARAM_POLICY allows them.
_TKQ_KEYS = tmpln.CURRENT_PLUS_PARAM_POLICY[tmpln.TRIVIAL_QERE][1]


def _add_provenance(trivial_ketiv_qere_2):
    """Build a provenance wtseq for a trivial ketiv/qere template."""
    pointed_qere_seq = wtp.template_param_val(trivial_ketiv_qere_2, "3")
    mqorot_raw = (trivial_ketiv_qere_2.get("tmpl_params") or {}).get("מקורות")
    paren = _mqorot_paren(mqorot_raw)
    wtseq = ["קרי="] + list(pointed_qere_seq) + [f" {paren}"]
    return shrink.shrink(wtseq)


def _mqorot_paren(mqorot_raw):
    if mqorot_raw is None:
        return "(מקורות=אין)"
    assert isinstance(mqorot_raw, str), type(mqorot_raw)
    sources = mqorot_raw.split(",")
    if len(sources) == 1:
        return f"(מקור={sources[0]})"
    return f"(מקורות={mqorot_raw})"


def _prep_log(io_renlog):
    if io_renlog is None:
        io_renlog = {}
    if io_renlog is not None:
        my_utils.maybe_init_at_key(io_renlog, "undocumented_trivial_ketiv_qere", [])
        my_utils.maybe_init_at_key(io_renlog, "doc_of_trivial_ketiv_qere_only", [])
        my_utils.maybe_init_at_key(
            io_renlog, "doc_of_trivial_ketiv_qere_and_other_stuff", []
        )
    return io_renlog


def _log(bcvt, io_renlog, doc1):
    if len(doc1) == 1:
        # Deut 22:16 is a current case of this
        io_renlog["doc_of_trivial_ketiv_qere_only"].append(bcvt)
    else:
        # Daniel 4:21 is the only current case of this
        io_renlog["doc_of_trivial_ketiv_qere_and_other_stuff"].append(bcvt)
