"""Exports img_html."""

from collections import namedtuple

import py_html.wlc_utils_html as wlc_utils_html
import mb_cmn.my_utils as my_utils

# A highlight box in the scan's own pixel coordinates (= the SVG viewBox units).
# rx is the rectangle's corner radius (also in pixel space).
Box = namedtuple("Box", ["x", "y", "w", "h", "rx"], defaults=[6])

# Default location of images relative to the page being generated.  Pages that sit
# one level below their sub-folder root (e.g. gh-pages/wlc/420422/full-record/*, the
# wlc-a-notes pages) resolve this to their own sub-folder's img/ dir and so keep the
# default.  Pages that sit directly in their sub-folder (the accgram pages) pass
# img_base="img/" so they reference their own accgram/img/ dir rather than escaping
# up to the top-level gh-pages/img/.
_DEFAULT_IMG_BASE = "../img/"


def html_for_imgs(record, *, img_para_attr=None, img_base=_DEFAULT_IMG_BASE):
    """Return HTML for image or images in record."""
    if "img" in record:
        return [
            html_for_single_img(
                record["img"], img_para_attr=img_para_attr, img_base=img_base
            )
        ]
    if "imgs" in record:
        imgs_items = record["imgs"].items()
        list_of_lists = [
            _html_for_imgs_item(
                imgs_item, img_para_attr=img_para_attr, img_base=img_base
            )
            for imgs_item in imgs_items
        ]
        return my_utils.sum_of_seqs(list_of_lists)
    return []


def html_for_single_img(img_path, *, img_para_attr=None, img_base=_DEFAULT_IMG_BASE):
    img_element = wlc_utils_html.img({"src": f"{img_base}{img_path}"})
    return wlc_utils_html.para(img_element, img_para_attr)


def _html_for_imgs_item(imgs_item, *, img_para_attr=None, img_base=_DEFAULT_IMG_BASE):
    img_label, img_path = imgs_item
    return [
        wlc_utils_html.para(img_label),
        html_for_single_img(img_path, img_para_attr=img_para_attr, img_base=img_base),
    ]


def annotated_img(
    img_attr,
    boxes,
    *,
    viewbox_w,
    viewbox_h,
    overlay_class="scan-annot-overlay",
):
    """<img> with a filled-highlight SVG overlaid, in a positioned wrapper.

    ``boxes`` are Box instances in the scan's own pixel space, which is also the
    SVG viewBox space -- so the highlights scale with the responsively-sized img.
    The overlay is a SIBLING of the <img> (not a child): the img's dark-mode
    ``filter: invert(1)`` (class="ink-on-white") therefore never touches the
    overlay, whose fill is instead chosen per-mode via ``light-dark()`` in CSS.
    ``aria-hidden`` because the highlighted word is already named in the
    figcaption prose -- the overlay is decorative reinforcement, not the sole
    carrier of meaning.
    """
    rects = tuple(
        wlc_utils_html.rect(
            {
                "x": str(box.x),
                "y": str(box.y),
                "width": str(box.w),
                "height": str(box.h),
                "rx": str(box.rx),
            }
        )
        for box in boxes
    )
    overlay = wlc_utils_html.svg(
        rects,
        {
            "class": overlay_class,
            "viewBox": f"0 0 {viewbox_w} {viewbox_h}",
            "preserveAspectRatio": "none",
            "aria-hidden": "true",
        },
    )
    return wlc_utils_html.div(
        (wlc_utils_html.img(img_attr), overlay), {"class": "scan-annot"}
    )


def focus_fade_img(
    img_attr,
    focus_boxes,
    *,
    viewbox_w,
    viewbox_h,
    svg_id,
    overlay_class="scan-annot-overlay focus-fade-overlay",
    fade_color=(200, 180, 60),
    max_alpha=200,
    exponent=0.6,
    feather=22,
    clear_margin=14,
):
    """<img> with a responsive SVG fade around one or more clear focus boxes.

    ``focus_boxes`` use the image's natural pixel coordinates. The boxes remain
    fully clear; beyond them, a muted tint becomes progressively stronger with
    distance from the nearer box. The SVG is a sibling of the unchanged image,
    so the treatment is nondestructive and scales with responsive image sizing.

    ``svg_id`` must be unique within the rendered document because the mask and
    filter use fragment references. The color, maximum alpha, and exponent keep
    the defaults of the former crop editor's focus fade. ``clear_margin`` adds
    breathing room before the feathered transition begins.
    """
    focus_boxes = tuple(focus_boxes)
    if not focus_boxes:
        raise ValueError("focus_fade_img requires at least one focus box")
    if not (viewbox_w > 0 and viewbox_h > 0):
        raise ValueError("focus_fade_img requires positive viewBox dimensions")
    if any(
        box.x < 0
        or box.y < 0
        or box.w <= 0
        or box.h <= 0
        or box.x + box.w > viewbox_w
        or box.y + box.h > viewbox_h
        for box in focus_boxes
    ):
        raise ValueError("focus_fade_img focus boxes must fit inside the viewBox")
    if not (0 <= max_alpha <= 255):
        raise ValueError("focus_fade_img max_alpha must be between 0 and 255")
    if feather <= 0 or clear_margin < 0 or exponent <= 0:
        raise ValueError("focus_fade_img fade geometry must be positive")

    filter_id = f"{svg_id}-filter"
    mask_id = f"{svg_id}-mask"
    filter_pad = 4 * feather + clear_margin

    def svg_el(tag, contents=(), attr=None):
        return wlc_utils_html.htel_mk(tag, attr, contents)

    expanded_cutouts = tuple(
        wlc_utils_html.rect(
            {
                "class": "focus-fade-mask-cutout",
                "x": str(box.x - clear_margin),
                "y": str(box.y - clear_margin),
                "width": str(box.w + 2 * clear_margin),
                "height": str(box.h + 2 * clear_margin),
                "rx": str(box.rx + clear_margin),
            }
        )
        for box in focus_boxes
    )
    solid_cutouts = tuple(
        wlc_utils_html.rect(
            {
                "class": "focus-fade-mask-cutout",
                "x": str(box.x),
                "y": str(box.y),
                "width": str(box.w),
                "height": str(box.h),
                "rx": str(box.rx),
            }
        )
        for box in focus_boxes
    )
    fade_filter = svg_el(
        "filter",
        (
            svg_el("feGaussianBlur", attr={"stdDeviation": str(feather)}),
            svg_el(
                "feComponentTransfer",
                tuple(
                    svg_el(
                        f"feFunc{channel}",
                        attr={"type": "linear", "slope": "2", "intercept": "-1"},
                    )
                    for channel in "RGB"
                ),
            ),
            svg_el(
                "feComponentTransfer",
                tuple(
                    svg_el(
                        f"feFunc{channel}",
                        attr={
                            "type": "gamma",
                            "amplitude": "1",
                            "exponent": str(exponent),
                            "offset": "0",
                        },
                    )
                    for channel in "RGB"
                ),
            ),
        ),
        {
            "id": filter_id,
            "x": str(-filter_pad),
            "y": str(-filter_pad),
            "width": str(viewbox_w + 2 * filter_pad),
            "height": str(viewbox_h + 2 * filter_pad),
            "filterUnits": "userSpaceOnUse",
            "color-interpolation-filters": "sRGB",
        },
    )
    fade_field = svg_el(
        "g",
        (
            wlc_utils_html.rect(
                {
                    "class": "focus-fade-mask-base",
                    "x": str(-filter_pad),
                    "y": str(-filter_pad),
                    "width": str(viewbox_w + 2 * filter_pad),
                    "height": str(viewbox_h + 2 * filter_pad),
                }
            ),
            *expanded_cutouts,
        ),
        {"filter": f"url(#{filter_id})"},
    )
    fade_mask = svg_el(
        "mask",
        (fade_field, *solid_cutouts),
        {
            "id": mask_id,
            "x": "0",
            "y": "0",
            "width": str(viewbox_w),
            "height": str(viewbox_h),
            "maskUnits": "userSpaceOnUse",
            "maskContentUnits": "userSpaceOnUse",
            "style": "mask-type: luminance;",
        },
    )
    tint = wlc_utils_html.rect(
        {
            "class": "focus-fade-tint",
            "x": "0",
            "y": "0",
            "width": str(viewbox_w),
            "height": str(viewbox_h),
            "mask": f"url(#{mask_id})",
            "style": (
                f"--focus-fade-color: rgb({fade_color[0]}, {fade_color[1]}, "
                f"{fade_color[2]}); --focus-fade-max-alpha: {max_alpha / 255:.6f};"
            ),
        }
    )
    overlay = wlc_utils_html.svg(
        (svg_el("defs", (fade_filter, fade_mask)), tint),
        {
            "class": overlay_class,
            "viewBox": f"0 0 {viewbox_w} {viewbox_h}",
            "preserveAspectRatio": "none",
            "aria-hidden": "true",
        },
    )
    return wlc_utils_html.div(
        (wlc_utils_html.img(img_attr), overlay), {"class": "scan-annot"}
    )


def scan_figure(
    src: str,
    alt: str,
    caption: object,
    *,
    img_class: str,
    width: str | None = None,
    boxes: tuple[Box, ...] | None = None,
    viewbox: tuple[int, int] | None = None,
) -> object:
    """<figure> holding a page scan, optionally with a highlight overlay, plus its caption.

    ``img_class`` is keyword-only and has NO default, deliberately. The class that
    matters here is ``ink-on-white``, which opts a scan into the stylesheet's
    dark-mode CSS inversion -- right for black ink on white paper, and wrong for
    the manuscript photos elsewhere in the tree, which are ink on parchment and
    must NOT invert (see the rule's comment in style.css). Every caller therefore
    names the class it wants, so no page can inherit inversion silently.

    Every ``alt`` passed here names the strands in ROMANIZED form ("taxton"/"elyon")
    while the figcaption beside it uses Hebrew letters. That is deliberate, not
    drift: attribute contexts are exempt by design (issue wlc-utils#65, finding T1) -- see
    printed_decalogue_strands' module docstring.
    """
    # No inline style here: gh-pages/wlc/style.css already declares `img { max-width: 100% }` and
    # `figure img { height: auto }`, so an inline copy only duplicated the stylesheet and
    # outranked it (issue wlc-utils#65, finding C4b). Don't reintroduce it.
    img_attr = {"src": src, "alt": alt, "class": img_class}
    if width:
        img_attr["width"] = width
    # When boxes are given, the <img> is wrapped in a positioned <div> alongside an inline-SVG
    # word-highlight overlay (annotated_img above). The overlay is a sibling of the img, so the
    # img's dark-mode invert never touches it -- see the .scan-annot rules and the ink-on-white
    # comment in style.css. The caller's img_class stays on the img either way.
    #
    # `viewbox` must equal the committed image's OWN natural size, since the boxes are in that
    # pixel space. Getting it wrong is silent -- the page still builds and the highlights just
    # land elsewhere -- so py/tests/test_scan_overlay_viewboxes.py lints every rendered figure's
    # viewBox against Image.open(scan).size. It reads the pair off the HTML, where the img and
    # the overlay sit side by side, so a page that grows an overlay later is covered without
    # being registered anywhere.
    if boxes:
        assert viewbox is not None, "boxes require a viewbox=(w, h)"
        img_node = annotated_img(
            img_attr, boxes, viewbox_w=viewbox[0], viewbox_h=viewbox[1]
        )
    else:
        img_node = wlc_utils_html.img(img_attr)
    return wlc_utils_html.figure((img_node, wlc_utils_html.figcaption(caption)))
