"""Exports convert"""

from mb_cmn import ws_tmpl2 as wtp
from mb_cmn import template_names as tmpln
from py_misc import near_aleppo_params as nap  # near-aleppo
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


def _make_doc_tmpl(scrdfftar, existing_doc_parts, existing_added=None):
    # near-aleppo: a scroll-difference note of the near-aleppo dataset's own name,
    # RENAMED_SCRDFFTAR, becomes a note of its own name, RENAMED_DOC, keeping its
    # MAM_TARGET; existing_added are the enclosing note's added parameters, which
    # follow. render_wikitext_handlers._handle_doc shows each as a line of the note.
    scrdfftar_keys, scrdfftar_added = nap.split_params(
        scrdfftar, _SCRDFFTAR_KEYS, _SCRDFFTAR_ADDED[wtp.template_name(scrdfftar)]
    )
    assert len(scrdfftar_keys) == 3, scrdfftar_keys
    scrdfftar_targ = wtp.template_element(scrdfftar, wtp.SDT_EL_IDX_FOR_TARG)
    scrdfftar_note = wtp.template_element(scrdfftar, wtp.SDT_EL_IDX_FOR_NOTE)
    # In this context, we don't care about starpos
    doc_name = _DOC_NAME_FOR[wtp.template_name(scrdfftar)]  # near-aleppo
    if doc_name == nap.RENAMED_DOC:
        nap.validate_baked_note(scrdfftar)
        if scrdfftar_note != [] or any(existing_doc_parts):
            raise ValueError(
                "Changed scroll-note conversions require framed MAM content"
            )
        mam_body = wtp.template_param_val(scrdfftar, nap.MAM_NOTE)
        mam_parts = [_tweak_scrdfftar_text(mam_body)]
        extra = dict(existing_added or {})
        if nap.MAM_NOTE in extra:
            mam_parts.extend(unbury.unbury_parts([_sequence(extra.pop(nap.MAM_NOTE))]))
        new_doc = wtp.mktmpl([[doc_name], scrdfftar_targ, []], ignore_equals=True)
        added = nap.raw_params(scrdfftar, scrdfftar_added)
        added[nap.MAM_NOTE] = _body(mam_parts)
        return nap.with_params(nap.with_params(new_doc, added), extra)
    new_doc_tmpl_els = [[doc_name], scrdfftar_targ]
    new_doc_tmpl_els.append(_tweak_scrdfftar_text(scrdfftar_note))
    if existing_doc_parts:
        existing_doc_parts = unbury.unbury_parts(existing_doc_parts)
        new_doc_tmpl_els.extend(existing_doc_parts)
    new_doc = wtp.mktmpl(new_doc_tmpl_els, ignore_equals=True)
    new_doc = nap.with_params(new_doc, nap.raw_params(scrdfftar, scrdfftar_added))
    return nap.with_params(new_doc, existing_added or {})  # near-aleppo


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
    #
    # near-aleppo: the note's own numbered parameters, apart from those the near-aleppo
    # dataset adds, which the new note keeps as they are, after the scroll-difference
    # note's. A note of the dataset's own name, RENAMED_DOC, holds one of its own name,
    # RENAMED_SCRDFFTAR, and each has MAM_TARGET: the note's is MAM's מ:הערה-2, and
    # that one's target is the other's MAM_TARGET, which the new note keeps.
    numbered, added = nap.split_doc_params(doc_tmpl)
    doc_tmpl_pvs = [wtp.template_param_val(doc_tmpl, key) for key in numbered]
    scrdfftar = my_utils.first_and_only(doc_tmpl_pvs[0])
    doc_name, scrdfftar_name = wtp.template_name(doc_tmpl), wtp.template_name(scrdfftar)
    if _DOC_NAME_FOR[scrdfftar_name] != doc_name:
        raise ValueError(f"{doc_name} of {scrdfftar_name}")
    if nap.MAM_TARGET in added:
        _assert_mam_targets_agree(doc_tmpl, scrdfftar)
        added = [key for key in added if key != nap.MAM_TARGET]
    return _make_doc_tmpl(scrdfftar, doc_tmpl_pvs[1:], nap.raw_params(doc_tmpl, added))


def _assert_mam_targets_agree(doc_tmpl, scrdfftar):
    # near-aleppo: the note's MAM_TARGET is MAM's מ:הערה-2, whose own parameters are
    # the renamed one's, but for its target, MAM's, the renamed one's MAM_TARGET.
    (mam_scrdfftar,) = wtp.template_param_val(doc_tmpl, nap.MAM_TARGET)
    mam_params = mam_scrdfftar["tmpl_params"]
    own = scrdfftar["tmpl_params"]
    expected = {"1": own[nap.MAM_TARGET], "2": own[nap.MAM_NOTE], "3": own["3"]}
    if wtp.template_name(mam_scrdfftar) != tmpln.SCRDFF_TAR or mam_params != expected:
        raise ValueError(f"MAM's targets disagree: {mam_scrdfftar!r} and {scrdfftar!r}")


# near-aleppo: the note that each scroll-difference note becomes, and the parameters
# the near-aleppo dataset adds to each.
_DOC_NAME_FOR = {tmpln.SCRDFF_TAR: "נוסח", nap.RENAMED_SCRDFFTAR: nap.RENAMED_DOC}
_SCRDFFTAR_KEYS = ("1", "2", "3")
_SCRDFFTAR_ADDED = {
    tmpln.SCRDFF_TAR: (),
    nap.RENAMED_SCRDFFTAR: (nap.MAM_TARGET, nap.MAM_NOTE, *nap.FLAGS),
}


def _sequence(value):
    return value if isinstance(value, list) else [value]


def _body(parts):
    elements = []
    for index, part in enumerate(parts):
        if index:
            elements.append({"tmpl_name": "ש"})
        elements.extend(part)
    return elements[0] if len(elements) == 1 else elements


def _assert_no_non_targeted_scrdff_at_top_level(wtseq):
    for wtel in wtseq:
        if wtp.is_scrdff_template(wtel):
            raise RuntimeError(
                "Unexpected non-targeted scroll-difference template "
                f"{tmpln.SCRDFF_NO_TAR} in plus scrdfftar-to-doc conversion"
            )


def _is_doc_of_scrdfftar(wtel):
    if not nap.is_doc_template(wtel):  # near-aleppo: either note name
        return False
    doc1 = wtp.template_element(wtel, 1)
    return len(doc1) == 1 and _is_scrdfftar_tmpl(doc1[0])


def _is_scrdfftar_tmpl(wtel):
    # near-aleppo: either scroll-difference note name
    return wtp.is_template_with_name_in(wtel, _DOC_NAME_FOR)


def _add_provenance(scrdfftar_text):
    assert isinstance(scrdfftar_text[0], str)
    new_scrdfftar_text_0 = "(מ:הערה) " + scrdfftar_text[0]
    return [new_scrdfftar_text_0, *scrdfftar_text[1:]]
