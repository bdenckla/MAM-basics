"""Exports ht_kq, handle_kq_ketiv_velo_qere"""

from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import hebrew_points as hpo
from mb_cmn import kq_special_templates as kqst
from py_misc import near_aleppo_params as nap  # near-aleppo
from render_wt import render_element as renel
from render_wt import render_wikitext_added_lines as added_lines  # near-aleppo
from render_wt import render_wikitext_helpers as wt_help
from mb_cmn import ws_tmpl2 as wtp
from mb_cmn import template_names as tmpln
from mb_cmn.shrink import shrink
from mb_cmn import uni_denorm
import unicodedata
from collections import Counter


def handle_kq(hctx, tmpl):
    kq_type = _kq_type_for_tmpl(tmpl)
    k_wtseq, q_wtseq = _ht_kq_unpack_args(tmpl)
    k_renseq_1 = wt_help.render_wtseq(hctx, k_wtseq)
    q_renseq_1 = wt_help.render_wtseq(hctx, q_wtseq)
    if ruby_enabled(hctx):
        ruby = _ruby(k_renseq_1, q_renseq_1)
        return _flagged(hctx, tmpl, ruby, (ruby,))
    k_renseq_2 = _maybe_paren(hctx, k_renseq_1)
    q_renseq_2 = _maybe_sqbrac(hctx, q_renseq_1)
    pointed_final_maqaf = (
        nap.POINTED_KETIV in wtp.template_param_keys(tmpl)
        and isinstance(k_wtseq[-1], str)
        and k_wtseq[-1].endswith(hpu.MAQ)
    )
    kq_separator, kq_tag = _maybe_kq_separator(hctx, kq_type, pointed_final_maqaf)
    kq_contents = (
        renel.mk_ren_el_tc("mam-kq-k", k_renseq_2),
        *kq_separator,
        renel.mk_ren_el_tc("mam-kq-q", q_renseq_2),
    )
    if not _PUT_KETIV_1ST[kq_type]:
        kq_contents = tuple(reversed(kq_contents))
    kq_ren_el = renel.mk_ren_el_tc(kq_tag, kq_contents)
    return _flagged(hctx, tmpl, kq_ren_el, (kq_ren_el,))  # near-aleppo


def handle_kq_ketiv_velo_qere(hctx, tmpl):
    """Handle a ketiv velo qere."""
    # near-aleppo: the arity is MAM's parameters', the near-aleppo dataset's flags
    # apart, which _flagged shows.
    mam_keys, _flags = nap.split_params(tmpl, _KVLQ_KEYS, nap.FLAGS)
    assert 1 + len(mam_keys) in (3, 4)
    ketiv_1 = wt_help.render_tmpl_el(hctx, tmpl, 2)
    if ruby_enabled(hctx):
        main_part = _ruby(ketiv_1, None)
    else:
        ketiv_2 = _maybe_paren(hctx, ketiv_1)
        main_part = renel.mk_ren_el_tc("mam-kq-k-velo-q", ketiv_2)
    if 1 + len(mam_keys) == 3:
        return _flagged(hctx, tmpl, (main_part,), (main_part,))  # near-aleppo
    assert wtp.template_i0(tmpl, 3) == hpu.MAQ
    if _style_is_abstract(hctx):
        maq_part = renel.mk_ren_el_t("mam-kq-k-velo-q-maq")
    else:
        maq_part = renel.mk_ren_el_tc("mam-kq-k-velo-q-maq", hpu.MAQ)
    return _flagged(hctx, tmpl, (main_part, maq_part), (main_part,))  # near-aleppo


def handle_kq_qere_velo_ketiv(hctx, tmpl):
    """Handle a qere velo ketiv."""
    # near-aleppo: as in handle_kq_ketiv_velo_qere.
    mam_keys, _flags = nap.split_params(tmpl, _QVLK_KEYS, nap.FLAGS)
    assert 1 + len(mam_keys) == 3
    qere_1 = wt_help.render_tmpl_el(hctx, tmpl, 2)
    if ruby_enabled(hctx):
        qvlk = _ruby(None, qere_1)
    else:
        qere_2 = _maybe_sqbrac(hctx, qere_1)
        qvlk = renel.mk_ren_el_tc("mam-kq-q-velo-k", qere_2)
    return _flagged(hctx, tmpl, (qvlk,), (qvlk,))  # near-aleppo


def ruby_enabled(hctx):
    return wt_help.get_renopt(hctx, "ro_ketiv_qere_ruby")


def handle_kq_trivial_ruby(hctx, tmpl):
    """Keep the trivial template's pointed ketiv below its pointed qere."""
    keys, _flags = nap.split_params(tmpl, _TRIVIAL_KEYS, nap.FLAGS)
    if not {"1", "2", "3"}.issubset(keys):
        raise ValueError("Trivial ketiv/qere lacks a reading parameter")
    ketiv = wt_help.render_tmpl_el(hctx, tmpl, 1)
    qere = wt_help.render_tmpl_el(hctx, tmpl, 3)
    annotation_attrs = {"dir": "rtl", "title": "Qere"}
    if "מקורות" in keys:
        sources = wtp.template_param_val(tmpl, "מקורות")
        if not all(isinstance(item, str) for item in sources):
            raise ValueError("Trivial ketiv/qere sources must be text")
        annotation_attrs["title"] = "Qere; sources: " + "".join(sources)
    ruby = _ruby(ketiv, qere, annotation_attrs)
    return _flagged(hctx, tmpl, ruby, (ruby,))


def _ruby(ketiv, qere, annotation_attrs=None):
    """CLC's ruby structure with ketiv on the baseline and qere above it.

    Missing readings have CLC's explicit editorial placeholders in their own slots.
    Reading contents, including final punctuation, are rendered without serial
    separators. Punctuation outside the template remains outside the ruby.
    """
    baseline = (
        renel.mk_ren_el_tc_and_attr("mam-kq-k", ketiv, {"title": "Ketiv"})
        if ketiv is not None
        else renel.mk_ren_el_tc("near-aleppo-kq-none", "[אין כתיב]")
    )
    annotation = (
        renel.mk_ren_el_tc("mam-kq-q", qere)
        if qere is not None
        else renel.mk_ren_el_tc("near-aleppo-kq-none", "[אין קרי]")
    )
    contents = (
        baseline,
        renel.mk_ren_el_tc("near-aleppo-kq-rp", "("),
        renel.mk_ren_el_tc_and_attr(
            "near-aleppo-kq-q",
            (annotation,),
            annotation_attrs or {"dir": "rtl", "title": "Qere"},
        ),
        renel.mk_ren_el_tc("near-aleppo-kq-rp", ")"),
    )
    return renel.mk_ren_el_tc_and_attr("near-aleppo-kq", contents, {"dir": "rtl"})


def _flagged(hctx, tmpl, rendered, lemma):
    """
    near-aleppo: ``rendered`` as it stands, or, where the template has a flag of the
    near-aleppo dataset, as the target of a note whose parts are the flags' lines,
    labelled ``lemma``. A ketiv/qere template has a flag only where no note is about
    the site, so this note is the only place the flag is shown, and the flag's value
    is one of the dataset's fixed English sentences. The same wrapper preserves
    flags when near-Aleppo displays a trivial ketiv/qere as ruby rather than
    converting its qere to a note. Punctuation outside an unread ketiv remains
    part of the target but outside the lemma.
    """
    flags = [key for key in wtp.template_param_keys(tmpl) if key in nap.FLAGS]
    if not flags:
        return rendered
    target = rendered if isinstance(rendered, tuple) else (rendered,)
    lines = added_lines.english_flag_lines(hctx, flags, tmpl)
    return (renel.mk_ren_el_tc_and_doc(target, lemma, lines),)


def _style_is_abstract(hctx):
    style = wt_help.get_renopt(hctx, "ro_render_style")
    return style == "abstract"


def _maybe_kq_separator(hctx, kq_type, pointed_final_maqaf):
    ketiv_maqaf = set(("k1q1-mcom", "k1q2-sr-bcom"))
    # A pointed ketiv's stored final maqaf is already inside its parentheses.
    # Keep the readings separated without adding another maqaf outside them.
    sep_is_maq = kq_type in ketiv_maqaf and not pointed_final_maqaf
    dic = {
        True: (hpu.MAQ, "mam-kq-sep-maqaf"),
        False: (" ", "mam-kq-sep-space"),
    }
    sep_char, abstract_tag = dic[sep_is_maq]
    if _style_is_abstract(hctx):
        return tuple(), abstract_tag
    return (sep_char,), "mam-kq"


_PUT_KETIV_1ST = {
    "k1q1-kq": True,
    "k1q1-mcom": True,
    "k1q2-sr-kqq": True,
    "k1q2-sr-bcom": True,
    "k1q2-wr-kqq": True,
    "k2q1": True,
    "k2q2": True,
    "k3q3": True,
    #
    "k1q1-qk": False,
    "k1q2-sr-qqk": False,
    "k1q2-ur-qqk": False,
}


def _ht_kq_unpack_args(tmpl):
    # near-aleppo: a parameter that is neither MAM's nor one the near-aleppo dataset
    # adds raises. The dataset's POINTED_KETIV, where a
    # template has it, supplies the ketiv display. MAM-with-doc keeps parentheses
    # and square brackets; near-Aleppo selects ruby. A flag is shown by _flagged.
    name = wtp.template_name(tmpl)
    mam_keys, added = nap.split_params(
        tmpl, _KQ_KEYS[name], (nap.POINTED_KETIV, *nap.FLAGS)
    )
    keys = set(mam_keys)
    assert {"1", "2"}.issubset(keys), keys
    if nap.POINTED_KETIV in added:
        ketiv = _pointing_display_order(wtp.template_param_val(tmpl, nap.POINTED_KETIV))
    else:
        ketiv = wtp.template_element(tmpl, 1)
    qere = wtp.template_element(tmpl, 2)
    return ketiv, qere


def _pointing_display_order(value):
    """Order display marks without changing the stored pointed-ketiv input.

    Only the added pointed-ketiv branch is processed. Template boundaries and the
    exact marks on each letter are preserved; MAM templates take their own branch.
    """
    if isinstance(value, str):
        result = uni_denorm.give_std_mark_order(value)
        if _cluster_inventory(result) != _cluster_inventory(value):
            raise ValueError("Display ordering changed the pointed-ketiv content")
        return result
    if isinstance(value, (list, tuple)):
        return type(value)(_pointing_display_order(item) for item in value)
    nap.orphan_marks.carriers(value, "pointed-ketiv display")
    return {
        "tmpl_name": value["tmpl_name"],
        "tmpl_params": {
            **value["tmpl_params"],
            "1": _pointing_display_order(value["tmpl_params"]["1"]),
        },
    }


def _cluster_inventory(string):
    """Compare letter order and each letter's mark inventory without normalization."""
    clusters = []
    for char in string:
        if unicodedata.combining(char) or char == hpo.DAGESH_XAZAQ:
            if not clusters:
                clusters.append((None, Counter()))
            clusters[-1][1][char] += 1
        else:
            clusters.append((char, Counter()))
    return clusters


# near-aleppo: MAM's parameters of each ketiv/qere template these handlers show, as
# MAM-basics' mb_cmn/template_names.py's CURRENT_PLUS_PARAM_POLICY allows them.
_KQ_KEYS = {
    name: tmpln.CURRENT_PLUS_PARAM_POLICY[name][1] for name in tmpln.STD_KQ_TMPL_NAMES
}
_KVLQ_KEYS = tmpln.CURRENT_PLUS_PARAM_POLICY["כתיב ולא קרי"][1]
_QVLK_KEYS = tmpln.CURRENT_PLUS_PARAM_POLICY["קרי ולא כתיב"][1]
_TRIVIAL_KEYS = tmpln.CURRENT_PLUS_PARAM_POLICY[tmpln.TRIVIAL_QERE][1]


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


def _paren(seq):
    return shrink(["(", *seq, ")"])


def _sqbrac(seq):
    return shrink(["[", *seq, "]"])


def _maybe_sqbrac(hctx, wtseq):
    return wtseq if _style_is_abstract(hctx) else _sqbrac(wtseq)


def _maybe_paren(hctx, wtseq):
    return wtseq if _style_is_abstract(hctx) else _paren(wtseq)
