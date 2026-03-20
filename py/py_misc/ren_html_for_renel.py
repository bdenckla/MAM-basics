"""Exports HfrCtx, html_for_ren_el"""

from dataclasses import dataclass
from typing import Union

from pyrender import render_element as renel
from pycmn import str_defs as sd
from py_misc import my_html
from pycmn import shrink
from py_misc import ren_tag_survey as rts


@dataclass
class HfrCtx:
    """Context needed for a html_from_ren_el call."""

    ht_tag_and_class_for_ren_tag: dict[str, tuple[str, Union[str, None]]]
    survey: Union[dict, None] = None


def html_for_ren_el(hfr_ctx: HfrCtx, ren_el):
    """
    Converts rendered element ren_el to an abstract form of HTML.
    Like, a rendered element with tag ren-tag and contents ren-c
    might become an (abstract) span with class ren-tag, where that
    span's contents is a converted version of ren-c.
    """
    if isinstance(ren_el, str):
        return ren_el
    if isinstance(ren_el, (tuple, list)):
        out_tup = tuple(html_for_ren_el(hfr_ctx, r) for r in ren_el)
        return shrink.shrink(out_tup)
    if isinstance(ren_el, dict):
        ren_tag = renel.get_ren_el_tag(ren_el)
        ren_con = renel.get_ren_el_contents(ren_el)
        ren_att = renel.get_ren_el_attr(ren_el) or {}
        ht_tag, ht_cla = hfr_ctx.ht_tag_and_class_for_ren_tag[ren_tag]
        if survey := hfr_ctx.survey:
            rts.record_ren_tag_seen(survey, ren_tag)
        ht_att_cla = {"class": ht_cla} if ht_cla else {}
        ht_att = {**ht_att_cla, **ren_att}
        ht_con = ren_con and html_for_ren_el(hfr_ctx, ren_con)
        return _html_fun(ht_tag, ht_att, ht_con)
    assert False, type(ren_el)


_SPECIAL_SPACES = {
    "html-tag-octo-space": sd.OCTO_NBSP,
    "html-tag-thin-space": sd.THSP,
    "html-tag-no-break-space": sd.NBSP,
}


def _html_fun(ht_tag, ht_att, ht_con):
    if special_space := _SPECIAL_SPACES.get(ht_tag):
        return special_space
    return my_html.htel_mk(ht_tag, ht_att, ht_con)
