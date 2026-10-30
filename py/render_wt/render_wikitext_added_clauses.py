"""Label preserved MAM context and the edition's evidence flags.

MAM_TARGET introduces the original note and is rendered in Scripture context.
Each flag follows as labelled clauses of the note: one for each preserved source
clause, or one for its fixed English sentence. The JSON value remains unchanged.
"""

from mb_cmn import ws_tmpl2 as wtp
from py_misc import near_aleppo_params as nap
from py_misc import unbury_doc_parts as unbury
from render_wt import render_element as renel
from render_wt import render_wikitext_helpers as wt_help
from render_wt import render_wikitext_spacing_concerns as spacing

# The language of each label: the flags' names are English, MAM_TARGET is Hebrew.
_LABEL_LANG = {
    nap.MAM_TARGET: None,
    nap.APPLIED_AND_FLAGGED: "en",
    nap.FLAGGED_NOT_APPLIED: "en",
}


def labelled_clause(name, renseq, separator=": "):
    """A note part: ``name`` as a label, a colon, and ``renseq``, less a trailing
    space."""
    _trailing, stripped = spacing.isolate_trailing(tuple(renseq))
    if not stripped:
        raise ValueError(f"an empty clause labelled {name}")
    lang = _LABEL_LANG[name]
    attr = {"lang": lang} if lang else {}
    label = renel.mk_ren_el_tc_and_attr(nap.LABEL_TAG, (name,), attr)
    return (label, separator, *stripped)


def flag_clauses(hctx, name, tmpl, parts_hctx):
    """The flag ``name`` of ``tmpl`` as labelled clauses, one per clause of its value.

    A clause that is one of the build's fixed English sentences, the render option
    ro_english_flag_values, is shown as English; any other is rendered as a note
    part is, with ``parts_hctx``.
    """
    labelled = []
    for clause in unbury.unbury_parts([wtp.template_param_val(tmpl, name)]):
        if english := _english(hctx, clause):
            labelled.append(labelled_clause(name, (english,)))
        else:
            labelled.append(
                labelled_clause(name, wt_help.render_wtseq(parts_hctx, clause))
            )
    return tuple(labelled)


def english_flag_clauses(hctx, names, tmpl):
    """The labelled clauses of the flags ``names`` of a template that is no note.

    Such a flag stands where no note has a clause about the site, so its value is
    one of the fixed English sentences, and anything else raises.
    """
    labelled = []
    for name in names:
        (clause,) = unbury.unbury_parts([wtp.template_param_val(tmpl, name)])
        english = _english(hctx, clause)
        if not english:
            raise ValueError(f"{name} of a template that is no note: {clause!r}")
        labelled.append(labelled_clause(name, (english,)))
    return tuple(labelled)


def _english(hctx, clause):
    """``clause`` as an English run if it is one of the fixed sentences, else None."""
    sentences = wt_help.get_renopt(hctx, "ro_english_flag_values")
    if sentences is None:
        raise ValueError("a flag, and no ro_english_flag_values to read it by")
    if len(clause) == 1 and clause[0] in sentences:
        return renel.mk_ren_el_tc_and_attr(
            nap.ENGLISH_TAG, (clause[0],), {"lang": "en"}
        )
    if not any(_has_hebrew_letter(el) for el in clause if isinstance(el, str)):
        raise ValueError(
            f"a flag's value is neither a clause nor a sentence: {clause!r}"
        )
    return None


def _has_hebrew_letter(string):
    return any(
        "\N{HEBREW LETTER ALEF}" <= char <= "\N{HEBREW LETTER TAV}" for char in string
    )
