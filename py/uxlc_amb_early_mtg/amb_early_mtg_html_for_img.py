"""Exports img_html."""

from mb_cmn import my_utils
import uxlc_misc.uxlc_utils_html as uxlc_utils_html


def html_for_imgs(record):
    """Return HTML for image or images in record."""
    if "img" in record:
        return [html_for_single_img(record["img"])]
    if "imgs" in record:
        imgs_items = record["imgs"].items()
        list_of_lists = list(map(_html_for_imgs_item, imgs_items))
        return my_utils.sum_of_seqs(list_of_lists)
    return []


def html_for_single_img(img_path):
    img_element = uxlc_utils_html.img({"src": f"../img/{img_path}"})
    return uxlc_utils_html.para(img_element)


def _html_for_imgs_item(imgs_item):
    img_label, img_path = imgs_item
    return [uxlc_utils_html.para(img_label), html_for_single_img(img_path)]
