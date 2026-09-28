"""Render the post-silluq manuscript-image pages, one per case.

A page shows one case's manuscript crops in the ledger's order, each under a heading naming
its manuscript and a paragraph saying what the crop shows, and then any recorded absence of
an expected image.  ``build_post_silluq_image_body`` is the only entry point, and
``author_site.post_stress_meteg.gen_html_files`` its only caller.
``post_stress_meteg_post_silluq_page``'s docstring says how the two post-silluq modules
divide the work.
"""

from __future__ import annotations

from html import escape

from accgram.almost_errors_html_shared import wrap_hebrew_runs
from author_site import site_data
from mb_misc import mb_html
from py_html import my_html_for_img as mhi

from author_site.post_stress_meteg_shared import (
    _FIRST_KINGS_14_ALEPPO_CROP_URL,
    _FIRST_KINGS_14_CAIRO_COTP_CROP_URL,
    _FIRST_KINGS_14_LENINGRAD_CROP_URL,
    _FIRST_KINGS_14_PETERSBURG_CROP_URL,
    _FIRST_KINGS_14_PETERSBURG_SOURCE_URL,
    _FIRST_KINGS_14_SASSOON_CROP_URL,
    _FIRST_KINGS_14_SASSOON_SOURCE_URL,
    _JOB_4_ALEPPO_CROP_URL,
    _JOB_4_CAM1753_CROP_URL,
    _JOB_4_LENINGRAD_CROP_URL,
    _JOB_4_PETERSBURG_CROP_URL,
    _JOB_4_REF,
    _JOB_4_SASSOON_CROP_URL,
    _JOB_4_SASSOON_SOURCE_URL,
    _MAM_POST_SILLUQ_ALEPPO_CROP_URL,
    _MAM_POST_SILLUQ_CAIRO_COTP_CROP_URL,
    _MAM_POST_SILLUQ_LENINGRAD_CROP_URL,
    _MAM_POST_SILLUQ_REF,
    _MAM_POST_SILLUQ_SASSOON_CROP_URL,
    _MAM_POST_SILLUQ_SASSOON_SOURCE_URL,
    _PETERSBURG_CONTINUATION_NAME,
    _PETERSBURG_FULL_NAME,
    _PETERSBURG_RECORD_URL,
    _PETERSBURG_SHORT_NAME,
    _PETERSBURG_SURVIVING_TEXT_GAP,
    _POST_SILLUQ_ALEPPO_CROP_URL,
    _POST_SILLUQ_CAIRO_COTP_CROP_URL,
    _POST_SILLUQ_CAIRO_COTP_SOURCE_URL,
    _POST_SILLUQ_FNAME,
    _POST_SILLUQ_LC_CROP_SOURCE_URL,
    _POST_SILLUQ_LC_CROP_URL,
    _POST_SILLUQ_PETERSBURG_CROP_URL,
    _POST_SILLUQ_PETERSBURG_SOURCE_URL,
    _POST_SILLUQ_REF,
    _POST_SILLUQ_SASSOON_CROP_URL,
    _POST_SILLUQ_SASSOON_SOURCE_URL,
    _POST_SILLUQ_TITLE,
    _PSALMS_60_ALEPPO_CROP_URL,
    _PSALMS_60_CAM1753_CROP_URL,
    _PSALMS_60_LENINGRAD_CROP_URL,
    _PSALMS_60_PETERSBURG_CROP_URL,
    _PSALMS_60_REF,
    _PSALMS_60_SASSOON_CROP_URL,
    _PSALMS_60_SASSOON_SOURCE_URL,
    _PSALMS_70_ALEPPO_CROP_URL,
    _PSALMS_70_CAM1753_CROP_URL,
    _PSALMS_70_LENINGRAD_CROP_URL,
    _PSALMS_70_PETERSBURG_CROP_URL,
    _PSALMS_70_REF,
    _PSALMS_70_SASSOON_CROP_URL,
    _PSALMS_70_SASSOON_SOURCE_URL,
    _PSALMS_72_ALEPPO_CROP_URL,
    _PSALMS_72_CAM1753_CROP_URL,
    _PSALMS_72_LENINGRAD_CROP_URL,
    _PSALMS_72_PETERSBURG_CROP_URL,
    _PSALMS_72_REF,
    _PSALMS_72_SASSOON_CROP_URL,
    _PSALMS_72_SASSOON_SOURCE_URL,
    _ROM_METEG,
    _ROM_SILLUQ,
    _UXLC_CHANGE_REF,
    _post_silluq_sources_for_bcv,
    _visible_title,
)

_FIRST_KINGS_14_PETERSBURG_VIEWBOX = (374, 208)
_FIRST_KINGS_14_PETERSBURG_FOCUS_BOXES = (
    mhi.Box(x=0, y=36, w=190, h=90, rx=0),
    mhi.Box(x=220, y=104, w=154, h=104, rx=0),
)
# Twenty-five percent darker than the crop's Otsu light-class mean in sRGB.
_FIRST_KINGS_14_PETERSBURG_BACKGROUND_COLOR = (184, 184, 184)


def _post_silluq_crop_alt(source: str, ref: str, state: str) -> str:
    """Give every manuscript crop the same short-name and claim structure."""
    if state == "later-meteg":
        claim = "it has a meteg after the silluq"
    elif state == "no-later-mark":
        claim = "it has no meteg after the silluq"
    elif state == "both-strokes":
        claim = "it has both strokes"
    else:
        raise ValueError(f"Unknown post-silluq crop state: {state!r}")
    return f"{source} crop of the verse-final word at {ref}; {claim}."


def _mam_post_silluq_aleppo_crop() -> object:
    """The Aleppo Codex crop at the MAM post-silluq site."""
    return mb_html.raw_html(
        f'<figure><img src="{_MAM_POST_SILLUQ_ALEPPO_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Aleppo", _MAM_POST_SILLUQ_REF, "later-meteg")}"'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        "<figcaption>Aleppo.</figcaption></figure>"
    )


def _mam_post_silluq_leningrad_crop() -> object:
    """The Leningrad Codex crop at the MAM post-silluq site."""
    return mb_html.raw_html(
        f'<figure><img src="{_MAM_POST_SILLUQ_LENINGRAD_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Leningrad", _MAM_POST_SILLUQ_REF, "no-later-mark")}"'
        ' loading="lazy" style="width: 300px; max-width: 100%; height: auto;">'
        "<figcaption>Leningrad.</figcaption></figure>"
    )


def _mam_post_silluq_cairo_cotp_crop() -> object:
    """The Cairo CoTP crop at 1 Kings 7:37, as interpreted by Ben."""
    return mb_html.raw_html(
        f'<figure><a href="{_POST_SILLUQ_CAIRO_COTP_SOURCE_URL}" target="_blank"'
        f' rel="noopener"><img src="{_MAM_POST_SILLUQ_CAIRO_COTP_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Cairo", _MAM_POST_SILLUQ_REF, "no-later-mark")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;"></a>'
        "<figcaption>Cairo, digital page 186 "
        "(no manuscript page number is visible); photograph from the Archivo "
        "del Centro de Ciencias Humanas y Sociales (CSIC), "
        f'<a href="{_POST_SILLUQ_CAIRO_COTP_SOURCE_URL}" target="_blank"'
        ' rel="noopener">source record</a> (CC BY-NC-SA 4.0).'
        "</figcaption></figure>"
    )


def _mam_post_silluq_sassoon_crop() -> object:
    """The Codex Sassoon 1053 crop at 1 Kings 7:37, as interpreted by Ben."""
    href = escape(_MAM_POST_SILLUQ_SASSOON_SOURCE_URL, quote=True)
    return mb_html.raw_html(
        f'<figure><a href="{href}" target="_blank" rel="noopener">'
        f'<img src="{_MAM_POST_SILLUQ_SASSOON_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Sassoon", _MAM_POST_SILLUQ_REF, "no-later-mark")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;"></a>'
        "<figcaption>Sassoon; "
        f'<a href="{href}" target="_blank" rel="noopener">Masoretica source</a>.'
        "</figcaption></figure>"
    )


def _post_silluq_lc_crop() -> object:
    """The directly inspectable LC line for 1 Samuel 17:5's post-silluq question."""
    return mb_html.raw_html(
        f'<figure><a href="{_POST_SILLUQ_LC_CROP_SOURCE_URL}" target="_blank"'
        f' rel="noopener"><img src="{_POST_SILLUQ_LC_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Leningrad", _POST_SILLUQ_REF, "later-meteg")}"'
        ' loading="lazy"></a><figcaption>Leningrad, F159A, column 3, line 8;'
        " crop attached to "
        f'<a href="{_POST_SILLUQ_LC_CROP_SOURCE_URL}" target="_blank"'
        ' rel="noopener">phonetic-hbo#78</a>.</figcaption></figure>'
    )


def _post_silluq_aleppo_crop() -> object:
    """The Aleppo crop showing no meteg after the silluq in 1 Samuel 17:5."""
    return mb_html.raw_html(
        f'<figure><img src="{_POST_SILLUQ_ALEPPO_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Aleppo", _POST_SILLUQ_REF, "no-later-mark")}"'
        ' loading="lazy">'
        "<figcaption>Aleppo.</figcaption></figure>"
    )


def _post_silluq_cairo_cotp_crop() -> object:
    """The Cairo CoTP crop at 1 Samuel 17:5, as interpreted by Ben."""
    return mb_html.raw_html(
        f'<figure><a href="{_POST_SILLUQ_CAIRO_COTP_SOURCE_URL}" target="_blank"'
        f' rel="noopener"><img src="{_POST_SILLUQ_CAIRO_COTP_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Cairo", _POST_SILLUQ_REF, "no-later-mark")}"'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        "</a><figcaption>Cairo, manuscript page 110, "
        "digital page 103; photograph from the "
        "Archivo del Centro de Ciencias Humanas y Sociales (CSIC), "
        f'<a href="{_POST_SILLUQ_CAIRO_COTP_SOURCE_URL}" target="_blank"'
        ' rel="noopener">source record</a> (CC BY-NC-SA 4.0).'
        "</figcaption></figure>"
    )


def _post_silluq_sassoon_crop() -> object:
    """The Codex Sassoon 1053 crop at 1 Samuel 17:5, as interpreted by Ben."""
    href = escape(_POST_SILLUQ_SASSOON_SOURCE_URL, quote=True)
    return mb_html.raw_html(
        f'<figure><a href="{href}" target="_blank" rel="noopener">'
        f'<img src="{_POST_SILLUQ_SASSOON_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Sassoon", _POST_SILLUQ_REF, "no-later-mark")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;"></a>'
        "<figcaption>Sassoon; "
        f'<a href="{href}" target="_blank" rel="noopener">Masoretica source</a>.'
        "</figcaption></figure>"
    )


def _first_kings_14_aleppo_crop() -> object:
    """The Aleppo Codex crop at 1 Kings 14:14."""
    return mb_html.raw_html(
        f'<figure><img src="{_FIRST_KINGS_14_ALEPPO_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Aleppo", _UXLC_CHANGE_REF, "no-later-mark")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;">'
        "<figcaption>Aleppo, page 83r.</figcaption></figure>"
    )


def _first_kings_14_leningrad_crop() -> object:
    """The Leningrad Codex crop at 1 Kings 14:14."""
    return mb_html.raw_html(
        f'<figure><img src="{_FIRST_KINGS_14_LENINGRAD_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Leningrad", _UXLC_CHANGE_REF, "later-meteg")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;">'
        "<figcaption>Leningrad, page F195B, column 2, line 27."
        "</figcaption></figure>"
    )


def _first_kings_14_cairo_cotp_crop() -> object:
    """The Cairo CoTP crop at 1 Kings 14:14, as interpreted by Ben."""
    return mb_html.raw_html(
        f'<figure><a href="{_POST_SILLUQ_CAIRO_COTP_SOURCE_URL}" target="_blank"'
        f' rel="noopener"><img src="{_FIRST_KINGS_14_CAIRO_COTP_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Cairo", _UXLC_CHANGE_REF, "no-later-mark")}"'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        "</a><figcaption>Cairo, digital page 204; "
        "photograph from the Archivo del Centro de Ciencias Humanas y Sociales "
        "(CSIC), "
        f'<a href="{_POST_SILLUQ_CAIRO_COTP_SOURCE_URL}" target="_blank"'
        ' rel="noopener">source record</a> (CC BY-NC-SA 4.0).'
        "</figcaption></figure>"
    )


def _first_kings_14_sassoon_crop() -> object:
    """The Codex Sassoon 1053 crop at 1 Kings 14:14, as interpreted by Ben."""
    href = escape(_FIRST_KINGS_14_SASSOON_SOURCE_URL, quote=True)
    return mb_html.raw_html(
        f'<figure><a href="{href}" target="_blank" rel="noopener">'
        f'<img src="{_FIRST_KINGS_14_SASSOON_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Sassoon", _UXLC_CHANGE_REF, "no-later-mark")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;"></a>'
        "<figcaption>Sassoon; "
        f'<a href="{href}" target="_blank" rel="noopener">Masoretica source</a>.'
        "</figcaption></figure>"
    )


def _psalms_60_aleppo_crop() -> object:
    """The Aleppo Codex crop at Psalms 60:10."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_60_ALEPPO_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Aleppo", _PSALMS_60_REF, "no-later-mark")}"'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        "<figcaption>Aleppo, page 251r.</figcaption></figure>"
    )


def _psalms_60_leningrad_crop() -> object:
    """The Leningrad Codex crop at Psalms 60:10."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_60_LENINGRAD_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Leningrad", _PSALMS_60_REF, "later-meteg")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;">'
        "<figcaption>Leningrad, page F377B.</figcaption></figure>"
    )


def _psalms_60_cam1753_crop() -> object:
    """The Cambridge Add. 1753 crop at Psalms 60:10."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_60_CAM1753_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Cambridge", _PSALMS_60_REF, "no-later-mark")}"'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        "<figcaption>Cambridge.</figcaption></figure>"
    )


def _psalms_60_sassoon_crop() -> object:
    """The Codex Sassoon 1053 crop at Psalms 60:10, as interpreted by Ben."""
    href = escape(_PSALMS_60_SASSOON_SOURCE_URL, quote=True)
    return mb_html.raw_html(
        f'<figure><a href="{href}" target="_blank" rel="noopener">'
        f'<img src="{_PSALMS_60_SASSOON_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Sassoon", _PSALMS_60_REF, "no-later-mark")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;"></a>'
        "<figcaption>Sassoon; "
        f'<a href="{href}" target="_blank" rel="noopener">Masoretica source</a>.'
        "</figcaption></figure>"
    )


def _psalms_70_aleppo_crop() -> object:
    """The Aleppo Codex crop at Psalms 70:2."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_70_ALEPPO_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Aleppo", _PSALMS_70_REF, "no-later-mark")}"'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        "<figcaption>Aleppo, page 253r.</figcaption></figure>"
    )


def _psalms_70_leningrad_crop() -> object:
    """The Leningrad Codex crop at Psalms 70:2."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_70_LENINGRAD_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Leningrad", _PSALMS_70_REF, "later-meteg")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;">'
        "<figcaption>Leningrad, page F379B.</figcaption></figure>"
    )


def _psalms_70_cam1753_crop() -> object:
    """The Cambridge Add. 1753 crop at Psalms 70:2."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_70_CAM1753_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Cambridge", _PSALMS_70_REF, "no-later-mark")}"'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        "<figcaption>Cambridge.</figcaption></figure>"
    )


def _psalms_70_sassoon_crop() -> object:
    """The Codex Sassoon 1053 crop at Psalms 70:2, as interpreted by Ben."""
    href = escape(_PSALMS_70_SASSOON_SOURCE_URL, quote=True)
    return mb_html.raw_html(
        f'<figure><a href="{href}" target="_blank" rel="noopener">'
        f'<img src="{_PSALMS_70_SASSOON_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Sassoon", _PSALMS_70_REF, "no-later-mark")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;"></a>'
        "<figcaption>Sassoon; "
        f'<a href="{href}" target="_blank" rel="noopener">Masoretica source</a>.'
        "</figcaption></figure>"
    )


def _psalms_72_aleppo_crop() -> object:
    """The Aleppo Codex crop at Psalms 72:15."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_72_ALEPPO_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Aleppo", _PSALMS_72_REF, "no-later-mark")}"'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        "<figcaption>Aleppo, page 253v.</figcaption></figure>"
    )


def _psalms_72_leningrad_crop() -> object:
    """The Leningrad Codex crop at Psalms 72:15."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_72_LENINGRAD_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Leningrad", _PSALMS_72_REF, "later-meteg")}"'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        "<figcaption>Leningrad, page F380A, line 3."
        "</figcaption></figure>"
    )


def _psalms_72_cam1753_crop() -> object:
    """The Cambridge Add. 1753 crop at Psalms 72:15."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_72_CAM1753_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Cambridge", _PSALMS_72_REF, "no-later-mark")}"'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        "<figcaption>Cambridge.</figcaption></figure>"
    )


def _psalms_72_sassoon_crop() -> object:
    """The Codex Sassoon 1053 crop at Psalms 72:15, as interpreted by Ben."""
    href = escape(_PSALMS_72_SASSOON_SOURCE_URL, quote=True)
    return mb_html.raw_html(
        f'<figure><a href="{href}" target="_blank" rel="noopener">'
        f'<img src="{_PSALMS_72_SASSOON_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Sassoon", _PSALMS_72_REF, "no-later-mark")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;"></a>'
        "<figcaption>Sassoon; "
        f'<a href="{href}" target="_blank" rel="noopener">Masoretica source</a>.'
        "</figcaption></figure>"
    )


def _job_4_aleppo_crop() -> object:
    """The Aleppo Codex crop at Job 4:12."""
    return mb_html.raw_html(
        f'<figure><img src="{_JOB_4_ALEPPO_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Aleppo", _JOB_4_REF, "both-strokes")}"'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        "<figcaption>Aleppo, page 271r, column 2, line 5."
        "</figcaption></figure>"
    )


def _job_4_leningrad_crop() -> object:
    """The Leningrad Codex crop at Job 4:12."""
    return mb_html.raw_html(
        f'<figure><img src="{_JOB_4_LENINGRAD_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Leningrad", _JOB_4_REF, "both-strokes")}"'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        "<figcaption>Leningrad, page F398A.</figcaption></figure>"
    )


def _job_4_cam1753_crop() -> object:
    """The Cambridge Add. 1753 crop at Job 4:12."""
    return mb_html.raw_html(
        f'<figure><img src="{_JOB_4_CAM1753_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Cambridge", _JOB_4_REF, "both-strokes")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;">'
        "<figcaption>Cambridge, page 0073B, column 2, line 13."
        "</figcaption></figure>"
    )


def _job_4_sassoon_crop() -> object:
    """The Codex Sassoon 1053 crop at Job 4:12, as interpreted by Ben."""
    href = escape(_JOB_4_SASSOON_SOURCE_URL, quote=True)
    return mb_html.raw_html(
        f'<figure><a href="{href}" target="_blank" rel="noopener">'
        f'<img src="{_JOB_4_SASSOON_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Sassoon", _JOB_4_REF, "both-strokes")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;"></a>'
        "<figcaption>Sassoon; "
        f'<a href="{href}" target="_blank" rel="noopener">Masoretica source</a>.'
        "</figcaption></figure>"
    )


def _petersburg_crop(
    crop_url: str,
    ref: str,
    *,
    source_url: str = _PETERSBURG_RECORD_URL,
    location: str = "",
    focus_fade: bool = False,
) -> object:
    """One St. Petersburg Evr. II B 55 crop, optionally focused in HTML."""
    href = escape(source_url, quote=True)
    location_clause = f", {escape(location)}" if location else ""
    img_attr = {
        "src": crop_url,
        "alt": _post_silluq_crop_alt(_PETERSBURG_SHORT_NAME, ref, "no-later-mark"),
        "loading": "lazy",
        "style": "display: block; max-width: 100%; height: auto;",
    }
    image = (
        f'<img src="{crop_url}"'
        f' alt="{_post_silluq_crop_alt(_PETERSBURG_SHORT_NAME, ref, "no-later-mark")}"'
        ' loading="lazy" style="display: block; max-width: 100%; height: auto;">'
    )
    focus_fade_note = ""
    if focus_fade:
        # The two boxes keep גם־עתה clear at the end of line 18 and start of line 19.
        # The pixel-space viewBox is checked against the source PNG by
        # test_scan_overlay_viewboxes.py.
        image = mb_html.el_to_str_for_sef(
            mhi.focus_fade_img(
                img_attr,
                _FIRST_KINGS_14_PETERSBURG_FOCUS_BOXES,
                viewbox_w=_FIRST_KINGS_14_PETERSBURG_VIEWBOX[0],
                viewbox_h=_FIRST_KINGS_14_PETERSBURG_VIEWBOX[1],
                svg_id="post-silluq-1k14v14-focus-fade",
                fade_color=_FIRST_KINGS_14_PETERSBURG_BACKGROUND_COLOR,
            )
        )
        focus_fade_note = (
            " A focus-of-attention fade subdues the surrounding text rather than "
            "covering it; the underlying crop is unchanged."
        )
    return mb_html.raw_html(
        f'<figure><a href="{href}" target="_blank" rel="noopener">{image}</a>'
        f"<figcaption>{_PETERSBURG_SHORT_NAME}, "
        f'MAM siglum <span dir="rtl">ל-א</span>{location_clause}; '
        f'<a href="{href}" target="_blank" rel="noopener">'
        f"National Library of Israel manuscript record</a>.{focus_fade_note}"
        "</figcaption></figure>"
    )


def _post_silluq_image_intro(
    source: str, ref: str, state: str, continuation: tuple = ()
) -> list:
    """Render one source heading and one uniformly phrased image claim."""
    if state == "later-meteg":
        claim = (" has a ", _ROM_METEG, " after the ", _ROM_SILLUQ)
    elif state == "no-later-mark":
        claim = (" has no ", _ROM_METEG, " after the ", _ROM_SILLUQ)
    elif state == "both-strokes":
        claim = (" has both strokes",)
    else:
        raise ValueError(f"Unknown post-silluq image state: {state!r}")
    return [
        mb_html.heading_level_2(source),
        mb_html.para((source, *claim, " at ", ref, ".", *continuation)),
    ]


def _petersburg_image_nodes(
    ref: str,
    crop_url: str,
    continuation: tuple = (),
    *,
    source_url: str = _PETERSBURG_RECORD_URL,
    location: str = "",
    focus_fade: bool = False,
) -> list:
    """Render the shared identification and one L-A silluq-only crop."""
    sentence_end = continuation or (".",)
    return [
        mb_html.heading_level_2(_PETERSBURG_SHORT_NAME),
        mb_html.para(
            (
                _PETERSBURG_FULL_NAME,
                ", identified in MAM by the siglum ",
                wrap_hebrew_runs("ל-א"),
                ", is a manuscript of the Prophets and Writings close to the "
                "Aleppo Codex. The National Library of Israel presents it together "
                "with its direct continuation, ",
                _PETERSBURG_CONTINUATION_NAME,
                ", but this crop belongs to Evr. II B 55. At ",
                ref,
                " it has the ",
                _ROM_SILLUQ,
                " alone in this word",
                *sentence_end,
            )
        ),
        _petersburg_crop(
            crop_url,
            ref,
            source_url=source_url,
            location=location,
            focus_fade=focus_fade,
        ),
    ]


def _post_silluq_image_nodes(image_id: str) -> list:
    """The fixed claim and existing deployed figure for one known image identifier."""
    if image_id == "lc-1s17-5":
        return [
            *_post_silluq_image_intro("Leningrad", _POST_SILLUQ_REF, "later-meteg"),
            _post_silluq_lc_crop(),
        ]
    if image_id == "aleppo-1s17-5":
        return [
            *_post_silluq_image_intro("Aleppo", _POST_SILLUQ_REF, "no-later-mark"),
            _post_silluq_aleppo_crop(),
        ]
    if image_id == "cairo-cotp-1s17-5":
        return [
            *_post_silluq_image_intro(
                "Cairo",
                _POST_SILLUQ_REF,
                "no-later-mark",
                (
                    " A stroke attached to the lamed ascender in the crop may look "
                    "like a ",
                    _ROM_METEG,
                    ", but it is part of the scribe's lamed. Ben notes that the "
                    "other lameds on the manuscript page have the same feature.",
                ),
            ),
            _post_silluq_cairo_cotp_crop(),
        ]
    if image_id == "sassoon-1053-1s17-5":
        return [
            *_post_silluq_image_intro("Sassoon", _POST_SILLUQ_REF, "no-later-mark"),
            _post_silluq_sassoon_crop(),
        ]
    if image_id == "petersburg-evr-ii-b-55-1s17-5":
        return _petersburg_image_nodes(
            _POST_SILLUQ_REF,
            _POST_SILLUQ_PETERSBURG_CROP_URL,
            source_url=_POST_SILLUQ_PETERSBURG_SOURCE_URL,
            location="page 57a, column 2, line 7 (digital page 120)",
        )
    if image_id == "aleppo-1k14-14":
        return [
            *_post_silluq_image_intro("Aleppo", _UXLC_CHANGE_REF, "no-later-mark"),
            _first_kings_14_aleppo_crop(),
        ]
    if image_id == "leningrad-1k14-14":
        return [
            *_post_silluq_image_intro("Leningrad", _UXLC_CHANGE_REF, "later-meteg"),
            _first_kings_14_leningrad_crop(),
        ]
    if image_id == "cairo-cotp-1k14-14":
        return [
            *_post_silluq_image_intro("Cairo", _UXLC_CHANGE_REF, "no-later-mark"),
            _first_kings_14_cairo_cotp_crop(),
        ]
    if image_id == "sassoon-1053-1k14-14":
        return [
            *_post_silluq_image_intro("Sassoon", _UXLC_CHANGE_REF, "no-later-mark"),
            _first_kings_14_sassoon_crop(),
        ]
    if image_id == "petersburg-evr-ii-b-55-1k14-14":
        return _petersburg_image_nodes(
            _UXLC_CHANGE_REF,
            _FIRST_KINGS_14_PETERSBURG_CROP_URL,
            source_url=_FIRST_KINGS_14_PETERSBURG_SOURCE_URL,
            location="digital page 186, column 1, lines 18–19",
            focus_fade=True,
        )
    if image_id == "aleppo-ps60-10":
        return [
            *_post_silluq_image_intro("Aleppo", _PSALMS_60_REF, "no-later-mark"),
            _psalms_60_aleppo_crop(),
        ]
    if image_id == "leningrad-ps60-10":
        return [
            *_post_silluq_image_intro("Leningrad", _PSALMS_60_REF, "later-meteg"),
            _psalms_60_leningrad_crop(),
        ]
    if image_id == "cam1753-ps60-10":
        return [
            *_post_silluq_image_intro("Cambridge", _PSALMS_60_REF, "no-later-mark"),
            _psalms_60_cam1753_crop(),
        ]
    if image_id == "sassoon-1053-ps60-10":
        return [
            *_post_silluq_image_intro("Sassoon", _PSALMS_60_REF, "no-later-mark"),
            _psalms_60_sassoon_crop(),
        ]
    if image_id == "petersburg-evr-ii-b-55-ps60-10":
        return _petersburg_image_nodes(
            _PSALMS_60_REF,
            _PSALMS_60_PETERSBURG_CROP_URL,
            source_url="https://www.nli.org.il/en/manuscripts/NNL_ALEPH990000991240205171/NLI?volumeItem=2#$FL48719462",
        )
    if image_id == "aleppo-ps70-2":
        return [
            *_post_silluq_image_intro("Aleppo", _PSALMS_70_REF, "no-later-mark"),
            _psalms_70_aleppo_crop(),
        ]
    if image_id == "leningrad-ps70-2":
        return [
            *_post_silluq_image_intro("Leningrad", _PSALMS_70_REF, "later-meteg"),
            _psalms_70_leningrad_crop(),
        ]
    if image_id == "cam1753-ps70-2":
        return [
            *_post_silluq_image_intro("Cambridge", _PSALMS_70_REF, "no-later-mark"),
            _psalms_70_cam1753_crop(),
        ]
    if image_id == "sassoon-1053-ps70-2":
        return [
            *_post_silluq_image_intro("Sassoon", _PSALMS_70_REF, "no-later-mark"),
            _psalms_70_sassoon_crop(),
        ]
    if image_id == "petersburg-evr-ii-b-55-ps70-2":
        return _petersburg_image_nodes(
            _PSALMS_70_REF,
            _PSALMS_70_PETERSBURG_CROP_URL,
            (
                ". A hard-to-explain mark appears just to the left of the ",
                _ROM_SILLUQ,
                " and touches the ",
                _ROM_SILLUQ,
                ". The mark looks intentional, but I have no idea what it might be.",
            ),
            source_url="https://www.nli.org.il/en/manuscripts/NNL_ALEPH990000991240205171/NLI?volumeItem=2#$FL48719471",
        )
    if image_id == "aleppo-ps72-15":
        return [
            *_post_silluq_image_intro("Aleppo", _PSALMS_72_REF, "no-later-mark"),
            _psalms_72_aleppo_crop(),
        ]
    if image_id == "leningrad-ps72-15":
        return [
            *_post_silluq_image_intro("Leningrad", _PSALMS_72_REF, "later-meteg"),
            _psalms_72_leningrad_crop(),
        ]
    if image_id == "cam1753-ps72-15":
        return [
            *_post_silluq_image_intro("Cambridge", _PSALMS_72_REF, "no-later-mark"),
            _psalms_72_cam1753_crop(),
        ]
    if image_id == "sassoon-1053-ps72-15":
        return [
            *_post_silluq_image_intro("Sassoon", _PSALMS_72_REF, "no-later-mark"),
            _psalms_72_sassoon_crop(),
        ]
    if image_id == "petersburg-evr-ii-b-55-ps72-15":
        return _petersburg_image_nodes(
            _PSALMS_72_REF,
            _PSALMS_72_PETERSBURG_CROP_URL,
            source_url="https://www.nli.org.il/en/manuscripts/NNL_ALEPH990000991240205171/NLI?volumeItem=2#$FL48719473",
        )
    if image_id == "aleppo-1k7-37":
        return [
            *_post_silluq_image_intro("Aleppo", _MAM_POST_SILLUQ_REF, "later-meteg"),
            _mam_post_silluq_aleppo_crop(),
        ]
    if image_id == "leningrad-1k7-37":
        return [
            *_post_silluq_image_intro(
                "Leningrad", _MAM_POST_SILLUQ_REF, "no-later-mark"
            ),
            _mam_post_silluq_leningrad_crop(),
        ]
    if image_id == "cairo-cotp-1k7-37":
        return [
            *_post_silluq_image_intro("Cairo", _MAM_POST_SILLUQ_REF, "no-later-mark"),
            _mam_post_silluq_cairo_cotp_crop(),
        ]
    if image_id == "sassoon-1053-1k7-37":
        return [
            *_post_silluq_image_intro("Sassoon", _MAM_POST_SILLUQ_REF, "no-later-mark"),
            _mam_post_silluq_sassoon_crop(),
        ]
    if image_id == "aleppo-jb4-12":
        return [
            *_post_silluq_image_intro("Aleppo", _JOB_4_REF, "both-strokes"),
            _job_4_aleppo_crop(),
        ]
    if image_id == "leningrad-jb4-12":
        return [
            *_post_silluq_image_intro("Leningrad", _JOB_4_REF, "both-strokes"),
            _job_4_leningrad_crop(),
        ]
    if image_id == "cam1753-jb4-12":
        return [
            *_post_silluq_image_intro("Cambridge", _JOB_4_REF, "both-strokes"),
            _job_4_cam1753_crop(),
        ]
    if image_id == "sassoon-1053-jb4-12":
        return [
            *_post_silluq_image_intro(
                "Sassoon",
                _JOB_4_REF,
                "both-strokes",
                (
                    " Sassoon's later stroke is far from vertical: it slants northeast "
                    "to southwest. I have no idea whether that slant is meaningful, but "
                    "it is too conspicuous to leave unmentioned.",
                ),
            ),
            _job_4_sassoon_crop(),
        ]
    if image_id == "petersburg-evr-ii-b-55-jb4-12":
        return _petersburg_image_nodes(
            _JOB_4_REF,
            _JOB_4_PETERSBURG_CROP_URL,
            ("—the only manuscript represented on this page that has that form.",),
            source_url="https://www.nli.org.il/en/manuscripts/NNL_ALEPH990000991240205171/NLI?volumeItem=2#$FL48719553",
        )
    raise ValueError(f"Unknown post-silluq image identifier: {image_id!r}")


_POST_SILLUQ_MANUSCRIPT_SOURCES = frozenset(
    {
        "aleppo",
        "leningrad",
        "cairo_cotp",
        "cam1753",
        "sassoon_1053",
        "petersburg_evr_ii_b_55",
    }
)


def _post_silluq_missing_image_nodes(case: dict, ref: str) -> list:
    """Render every explicitly recorded absence of an expected manuscript image."""
    records = case.get("missing_expected_images", [])
    records_by_source = {record["source"]: record for record in records}
    if len(records_by_source) != len(records):
        raise ValueError(f"{case['ref']}: duplicate missing-image source")
    required_sources = {
        source
        for source in _post_silluq_sources_for_bcv(case["bcv"])
        if source in _POST_SILLUQ_MANUSCRIPT_SOURCES
        and case["sources"][source] == "not-recorded"
    }
    if set(records_by_source) != required_sources:
        raise ValueError(
            f"{case['ref']}: missing-image records differ from unclassified manuscripts"
        )
    contents = []
    for source in _post_silluq_sources_for_bcv(case["bcv"]):
        if source not in records_by_source:
            continue
        record = records_by_source[source]
        if (
            source != "petersburg_evr_ii_b_55"
            or record.get("reason") != "verse-absent-from-surviving-text"
        ):
            raise ValueError(f"{case['ref']}: unknown missing-image record {record!r}")
        if any(
            image_id.startswith("petersburg-evr-ii-b-55-")
            for image_id in case["images"]
        ):
            raise ValueError(
                f"{case['ref']}: EVR-II-B-55 image is both present and absent"
            )
        contents.extend(
            (
                mb_html.heading_level_2(_PETERSBURG_SHORT_NAME),
                mb_html.para(
                    (
                        "No image of ",
                        _PETERSBURG_SHORT_NAME,
                        " contains ",
                        ref,
                        ": ",
                        _PETERSBURG_SURVIVING_TEXT_GAP,
                    )
                ),
            )
        )
    return contents


def build_post_silluq_image_body(case: dict) -> list:
    """Render one case's ordered manuscript images on its own page."""
    bcv = case["bcv"]
    if not case["images"]:
        raise ValueError(f"{bcv}: image page needs manuscript images")
    if bcv not in site_data.POST_STRESS_METEG_POST_SILLUQ_IMAGE_PAGES:
        raise ValueError(f"{bcv}: no manuscript-image page is declared")
    _fname, ref = site_data.POST_STRESS_METEG_POST_SILLUQ_IMAGE_PAGES[bcv]
    contents = [
        mb_html.heading_level_1(
            (
                _visible_title(_POST_SILLUQ_TITLE),
                ": manuscript images for the verse-final word at ",
                ref,
            )
        ),
        mb_html.para(
            (
                "← Back to the ",
                mb_html.anchor_h(
                    "case register", f"{_POST_SILLUQ_FNAME}#case-register"
                ),
                ".",
            )
        ),
    ]
    if bcv == "jb4:12":
        # Ben's placement observations are recorded in the Job report and its update.
        contents.extend(
            (
                mb_html.heading_level_2(
                    ("Early ", _ROM_SILLUQ, " in Leningrad and Aleppo?")
                ),
                mb_html.para(
                    (
                        "We usually regard an “early ",
                        _ROM_METEG,
                        "”—a ",
                        _ROM_METEG,
                        " to the right of its vowel—as meaningless. Should we also treat "
                        "“early ",
                        _ROM_SILLUQ,
                        "” as meaningless? In both Aleppo and Leningrad, the stroke under "
                        "the mem is to the right of its segol. This seems an extraordinary "
                        "coincidence. (In Cambridge and Sassoon, the stroke under the mem "
                        "is in its normal position: to the left of its segol.)",
                    )
                ),
            )
        )
    for image_id in case["images"]:
        contents.extend(_post_silluq_image_nodes(image_id))
    contents.extend(_post_silluq_missing_image_nodes(case, ref))
    return contents
