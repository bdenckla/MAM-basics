from lenin_wiki import image_urls as iu
from mb_cmn.my_utils import sum_of_map


def masorah_finalis_lines():
    page_ddas = sum_of_map(_get_page_ddas, range(464, 492))
    core = list(map(_line_for_page, page_ddas))
    return ["", _SECTION_HEADER, *core]


def _get_page_ddas(ddd):
    return [f"{ddd}A", f"{ddd}B"]


def _line_for_page(page_ddda):
    return _line_for_vis_and_page(_vis_for_page(page_ddda), page_ddda)


def _vis_for_page(page_ddda):
    ddda_ddd, ddda_a = page_ddda[:3], page_ddda[3]
    ddd_int = int(ddda_ddd)
    n_mafi = ddd_int - 462
    dd_mafi = f"{n_mafi:02}"  # E.g. "03" if n_mafi == 3
    hahb = iu.CACB_HAHB[ddda_a]
    visible = f"מסורה סופית {dd_mafi} ({hahb})"
    # E.g. visible == "מסורה סופית 03 (ב)"
    return visible


def _line_for_vis_and_page(visible, page_ddda):
    urls = iu.image_urls(page_ddda)
    anchor_lcci = f"[{urls['lcci']} {visible}]"
    anchor_sefa = f"[{urls['sefa']} ספריא]"
    daf_num_ab = iu.cacb_hahb(page_ddda)
    daf = f"({daf_num_ab})"
    return f"#{anchor_lcci} / {anchor_sefa} {daf}"


_SECTION_HEADER = "=== Masorah finalis folios 02 and beyond (skipping 01 because it is not simple) ==="
