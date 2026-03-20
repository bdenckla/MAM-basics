"""Exports render_to_xml, handle_survey_results"""

from py_misc import ren_html_for_renel as hfr
from py_misc import ren_tag_survey as rts
from pycmn import my_utils
from pyrender import render_wikitext as rwt


def render_to_xml(books_mpp, bkid):
    """Render MAM XML"""
    # rv: rendered verses
    bcvt_to_veraf = rwt.render(bkid, books_mpp, _RENOPTS_MAM_XML)
    verafs = tuple(bcvt_to_veraf.values())
    survey = rts.make()
    hfr_ctx = hfr.HfrCtx(_HT_TAC_FOR_RT_FOR_MAM_XML, survey)
    html_verafs = rwt.map_over_verafs((hfr.html_for_ren_el, hfr_ctx), verafs)
    bcvts = tuple(bcvt for bcvt in bcvt_to_veraf.keys())
    book_rendered = my_utils.l_szip(bcvts, html_verafs)
    return book_rendered, survey


def handle_survey_results(bkids, survey):
    """Handle the results of the render tag survey."""
    if len(bkids) != 39:
        return
    ren_tags_seen = rts.get_ren_tags_seen(survey)
    ren_tags_wets = set(_HT_TAC_FOR_RT_FOR_MAM_XML)
    _survey_results_helper(ren_tags_seen, ren_tags_wets, "render tags")


def _survey_results_helper(seen, wets, name):
    diff = wets - seen
    if diff:
        print(f"{name} expected but not seen: ", sorted(diff))
    assert not diff


_RENOPTS_MAM_XML = {
    #
    "ro_cantillation": "rv-cant-all-three",
    "ro_qamats_var": "rv-dalet",
    "ro_no_varika": True,
    "ro_no_doc": True,
    #
    "ro_render_style": "abstract",
}
_HT_TAC_FOR_RT_FOR_MAM_XML = {
    #
    "mam-good-ending": ("good-ending", None),
    "mam-letter-small": ("letter-small", None),
    "mam-letter-large": ("letter-large", None),
    "mam-letter-hung": ("letter-hung", None),
    "mam-kq-q-velo-k": ("kq-q-velo-k", None),
    "mam-kq-k-velo-q": ("kq-k-velo-q", None),
    "mam-kq-k-velo-q-maq": ("kq-k-velo-q-maq", None),
    "mam-kq-sep-space": ("kq", None),
    "mam-kq-sep-maqaf": ("kq", "sep-maqaf"),
    "mam-kq-k": ("kq-k", None),
    "mam-kq-q": ("kq-q", None),
    "mam-kq-trivial": ("kq-trivial", None),
    #
    "spi-samekh2": ("spi-samekh2", None),
    "spi-samekh3": ("spi-samekh3", None),
    "spi-samekh3-nu10-invnun-neighbor": ("spi-samekh3", "nu10-invnun-neighbor"),
    "spi-pe2": ("spi-pe2", None),
    "spi-pe3": ("spi-pe3", None),
    #
    "spi-invnun": ("spi-invnun", None),
    "spi-invnun-including-trailing-space": ("spi-invnun", "including-trailing-space"),
    #
    "shirah-space": ("shirah-space", None),
    #
    "lp-legarmeih": ("lp-legarmeih", None),
    "lp-paseq": ("lp-paseq", None),
    #
    "implicit-maqaf": ("implicit-maqaf", None),
    #
    "cant-alef": ("cant-alef", None),
    "cant-all-three": ("cant-all-three", None),
    "cant-bet": ("cant-bet", None),
    "cant-combined": ("cant-combined", None),
    #
    "scrdfftar": ("scrdfftar", None),
    "sdt-target": ("sdt-target", None),
    "sdt-note": ("sdt-note", None),
    #
    "slh-word": ("slh-word", None),
    #
}
