"""Exports ht_kq, handle_kq_ketiv_velo_qere"""

from pycmn import hebrew_punctuation as hpu
from pyrender import render_element as renel
from pyrender import render_wikitext_helpers as wt_help
from pycmn import ws_tmpl2 as wtp
from pycmn import template_names as tmpln
from pycmn.shrink import shrink


def handle_kq(hctx, tmpl):
    kq_type = tmpln.LATIN_SHORTS[wtp.template_name(tmpl)]
    k_wtseq, q_wtseq = _ht_kq_unpack_args(tmpl)
    k_renseq_1 = wt_help.render_wtseq(hctx, k_wtseq)
    q_renseq_1 = wt_help.render_wtseq(hctx, q_wtseq)
    k_renseq_2 = _maybe_paren(hctx, k_renseq_1)
    q_renseq_2 = _maybe_sqbrac(hctx, q_renseq_1)
    kq_separator, kq_tag = _maybe_kq_separator(hctx, kq_type)
    kq_contents = (
        renel.mk_ren_el_tc("mam-kq-k", k_renseq_2),
        *kq_separator,
        renel.mk_ren_el_tc("mam-kq-q", q_renseq_2),
    )
    if not _PUT_KETIV_1ST[kq_type]:
        kq_contents = tuple(reversed(kq_contents))
    return renel.mk_ren_el_tc(kq_tag, kq_contents)


def handle_kq_ketiv_velo_qere(hctx, tmpl):
    """Handle a ketiv velo qere."""
    assert wtp.template_len(tmpl) in (3, 4)
    ketiv_1 = wt_help.render_tmpl_el(hctx, tmpl, 2)
    ketiv_2 = _maybe_paren(hctx, ketiv_1)
    main_part = renel.mk_ren_el_tc("mam-kq-k-velo-q", ketiv_2)
    if wtp.template_len(tmpl) == 3:
        return (main_part,)
    assert wtp.template_i0(tmpl, 3) == hpu.MAQ
    if _style_is_abstract(hctx):
        maq_part = renel.mk_ren_el_t("mam-kq-k-velo-q-maq")
    else:
        maq_part = renel.mk_ren_el_tc("mam-kq-k-velo-q-maq", hpu.MAQ)
    return main_part, maq_part


def handle_kq_qere_velo_ketiv(hctx, tmpl):
    """Handle a qere velo ketiv."""
    assert wtp.template_len(tmpl) == 3
    qere_1 = wt_help.render_tmpl_el(hctx, tmpl, 2)
    qere_2 = _maybe_sqbrac(hctx, qere_1)
    return (renel.mk_ren_el_tc("mam-kq-q-velo-k", qere_2),)


def _style_is_abstract(hctx):
    style = wt_help.get_renopt(hctx, "ro_render_style")
    return style == "abstract"


def _maybe_kq_separator(hctx, kq_type):
    ketiv_maqaf = set(("k1q1-mcom", "k1q2-sr-bcom"))
    sep_is_maq = kq_type in ketiv_maqaf
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
    assert wtp.template_len(tmpl) == 3
    ketiv = wtp.template_element(tmpl, 1)
    qere = wtp.template_element(tmpl, 2)
    return ketiv, qere


def _paren(seq):
    return shrink(["(", *seq, ")"])


def _sqbrac(seq):
    return shrink(["[", *seq, "]"])


def _maybe_sqbrac(hctx, wtseq):
    return wtseq if _style_is_abstract(hctx) else _sqbrac(wtseq)


def _maybe_paren(hctx, wtseq):
    return wtseq if _style_is_abstract(hctx) else _paren(wtseq)
