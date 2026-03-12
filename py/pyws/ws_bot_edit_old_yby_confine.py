from functools import partial
import re
from pycmn import ws_tmpl1 as wtp1
from pycmn import hebrew_accents as ha
from pycmn import ws_tmpl1 as wtp1
from pyws import ws_get_bk_in_both_fmts as wsin
from pyws import ws_fmt_2_back_to_wikitext as btw
from pycmn.my_utils import sum_of_map
from pycmn.my_utils import sl_map
from pycmn.shrink import shrink
from pycmn.my_utils import dv_dispatch
from pycmn.my_utils import dv_map
from pycmn.my_utils import first_and_only_and_str


def edit_page_text(he_chnu: str, page_text: str):
    cif2 = wsin.get_chap_in_fmt_2(page_text.splitlines())
    _out_cif2, big_str = edit_cif2(he_chnu, cif2)
    return big_str


def edit_cif2(he_chnu, cif2):
    out_cif2 = _edit_wsf2_chap(_CANDLERS, cif2)
    return out_cif2, btw.big_str(he_chnu, out_cif2)


def _edit_wsf2_chap(candlers, wsf2_chap):
    return dv_dispatch(candlers, wsf2_chap)


def _pass_thru(val):
    return val


def _pass_thru_as_singleton(val):
    return [val]


def _edit_a_chap_body(vandlers, chap_body):
    return dv_map((_edit_a_plb_verse, vandlers), chap_body)


def _edit_a_plb_verse(vandlers, plb_verse):
    return dv_dispatch(vandlers, plb_verse)


def _edit_wtseq(wandlers, wtseq):
    standard = shrink(sum_of_map((_edit_wtel, wandlers), wtseq))
    return _edit_wtseq_2(standard)


_ORIG_TMPL_NAME = "ירח בן יומו"
_NEW_TMPL_NAME = "ירח בן יומו-2"


def _edit_wtseq_2(wtseq):
    ot_idx = None  # ot: orig tmpl
    for idx, wtel in enumerate(wtseq):
        if wtp1.is_template_with_name(wtel, _ORIG_TMPL_NAME):
            ot_idx = idx
    if ot_idx is None:
        return wtseq
    assert 0 < ot_idx < len(wtseq) - 1
    pre = wtseq[:ot_idx]
    post = wtseq[ot_idx + 1 :]
    newseq_q = _confine(pre, post)
    if newseq_q is None:
        return wtseq
    return newseq_q


def _confine(pre, post):
    spre = _split_pre(pre)
    spost = _split_post(post)
    assert spre is not None and spost is not None
    pre0, pre1 = spre
    post0, post1 = spost
    foo_args = shrink([pre1, ha.YBY, post0])
    foo_arg = first_and_only_and_str(foo_args)
    assert "=" not in foo_arg
    foo = wtp1.mktmpl([[_NEW_TMPL_NAME], [foo_arg]])
    return [*pre0, foo, *post1]


def _split_pre(pre):
    if isinstance(pre[-1], str):
        if match := re.fullmatch("(.* )?(.*)", pre[-1]):
            if mg1 := match.group(1):
                pre0 = [*pre[:-1], mg1]
            else:
                pre0 = pre[:-1]
            pre1 = match.group(2)
            return pre0, pre1
    return None


def _split_post(post):
    if isinstance(post[0], str):
        if match := re.fullmatch("(.*?)( .*)?", post[0]):
            post0 = match.group(1)
            if mg2 := match.group(2):
                post1 = [mg2, *post[1:]]
            else:
                post1 = post[1:]
            return post0, post1
    return None


def _edit_wtel(wandlers, wtel):
    if isinstance(wtel, str):
        return wandlers["string"](wtel)
    if wtp1.is_abtag(wtel):
        return [wtel]
    return _edit_tmpl_call(wandlers, wtel)


def _edit_tmpl_call(wandlers, tmpl):
    if wandler := wandlers.get(wtp1.template_name(tmpl)):
        return wandler(tmpl)
    return _recurse_on_args(_get_wandlers, tmpl)


def _recurse_on_args(get_wandlers_fn, tmpl):
    tmpl_els_in = wtp1.template_elements(tmpl)
    assert isinstance(tmpl_els_in, list)
    wandlers = get_wandlers_fn()
    tmpl_args_out = sl_map((_edit_wtseq, wandlers), tmpl_els_in[1:])
    tmpl_els_out = [tmpl_els_in[0], *tmpl_args_out]
    return [wtp1.mktmpl(tmpl_els_out)]


def _get_wandlers():
    return _WANDLERS


_WANDLERS = {
    "string": _pass_thru_as_singleton,
}
_VANDLERS = {
    "prefix": _pass_thru,
    #
    "location": _pass_thru,
    #
    # "verse-body": _pass_thru,
    "verse-body": partial(_edit_wtseq, _WANDLERS),
}
_CANDLERS = {
    "ws-chap-noinclude-header": _pass_thru,
    "ws-chap-body": partial(_edit_a_chap_body, _VANDLERS),
    "ws-chap-good-ending": _pass_thru,
    "ws-chap-noinclude-footer": _pass_thru,
    "ws-chap-category": _pass_thru,
}
