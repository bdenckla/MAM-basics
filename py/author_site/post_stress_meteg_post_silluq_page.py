"""Render the post-silluq comparative evidence page."""

from __future__ import annotations

from html import escape

from accgram import post_stress_meteg_model as psm
from accgram.almost_errors_html_shared import wrap_hebrew_runs
from author_site import site_data
from mb_author import author
from mb_misc import mb_html

from author_site.post_stress_meteg_shared import (
    _FIRST_KINGS_14_ALEPPO_CROP_URL,
    _FIRST_KINGS_14_CAIRO_COTP_CROP_URL,
    _FIRST_KINGS_14_LENINGRAD_CROP_URL,
    _FIRST_KINGS_14_SASSOON_CROP_URL,
    _FIRST_KINGS_14_SASSOON_SOURCE_URL,
    _FNAME,
    _HEBREW_CELL,
    _JOB_4_ALEPPO_CROP_URL,
    _JOB_4_CAM1753_CROP_URL,
    _JOB_4_LENINGRAD_CROP_URL,
    _JOB_4_REF,
    _JOB_4_SASSOON_CROP_URL,
    _JOB_4_SASSOON_SOURCE_URL,
    _MAM_POST_SILLUQ_ALEPPO_CROP_URL,
    _MAM_POST_SILLUQ_CAIRO_COTP_CROP_URL,
    _MAM_POST_SILLUQ_LENINGRAD_CROP_URL,
    _MAM_POST_SILLUQ_REF,
    _MAM_POST_SILLUQ_SASSOON_CROP_URL,
    _MAM_POST_SILLUQ_SASSOON_SOURCE_URL,
    _MAM_POST_SILLUQ_VERSE,
    _METSIL,
    _PLAUT_STEIN_TORAH_URL,
    _POST_SILLUQ_ALEPPO_CROP_URL,
    _POST_SILLUQ_BCV_CELL,
    _POST_SILLUQ_CAIRO_COTP_CROP_URL,
    _POST_SILLUQ_CAIRO_COTP_SOURCE_URL,
    _POST_SILLUQ_DISTINCT_STROKE_FOOTNOTE_ID,
    _POST_SILLUQ_FNAME,
    _POST_SILLUQ_FOOTNOTE_ID,
    _POST_SILLUQ_LC_CROP_SOURCE_URL,
    _POST_SILLUQ_LC_CROP_URL,
    _POST_SILLUQ_MAM_POLICY_FOOTNOTE_ID,
    _POST_SILLUQ_REF,
    _POST_SILLUQ_SASSOON_CROP_URL,
    _POST_SILLUQ_SASSOON_SOURCE_URL,
    _POST_SILLUQ_SOURCE_CODES,
    _POST_SILLUQ_TITLE,
    _POST_SILLUQ_VERSE,
    _PSALMS_60_ALEPPO_CROP_URL,
    _PSALMS_60_CAM1753_CROP_URL,
    _PSALMS_60_LENINGRAD_CROP_URL,
    _PSALMS_60_REF,
    _PSALMS_60_SASSOON_CROP_URL,
    _PSALMS_60_SASSOON_SOURCE_URL,
    _PSALMS_70_ALEPPO_CROP_URL,
    _PSALMS_70_CAM1753_CROP_URL,
    _PSALMS_70_LENINGRAD_CROP_URL,
    _PSALMS_70_REF,
    _PSALMS_70_SASSOON_CROP_URL,
    _PSALMS_70_SASSOON_SOURCE_URL,
    _PSALMS_72_ALEPPO_CROP_URL,
    _PSALMS_72_CAM1753_CROP_URL,
    _PSALMS_72_LENINGRAD_CROP_URL,
    _PSALMS_72_REF,
    _PSALMS_72_SASSOON_CROP_URL,
    _PSALMS_72_SASSOON_SOURCE_URL,
    _ROM_METEG,
    _ROM_SILLUQ,
    _TITLE,
    _URJ_DISTINCT_STROKE_CROP_URL,
    _URJ_DISTINCT_STROKE_REF,
    _URJ_DISTINCT_STROKE_VERSE,
    _UXLC_CHANGE_REF,
    _UXLC_CHANGE_URL,
    _UXLC_CHANGE_VERSE,
    _footnote_callout,
    _hebrew_cell,
    _hebrew_spacing_option,
    _post_silluq_sources_for_bcv,
    _ref_link,
    _scriptural_bcv_key,
    _table,
    _visible_title,
    chb,
    cos,
)

from author_site.post_stress_meteg_post_silluq_data import (
    _case_forms,
    _letters_of,
    _mam_final_forms,
)


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
        ' rel="noopener">phonetic-hbo #78</a>.</figcaption></figure>'
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
        "digital image 103; photograph from the "
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
        "<figcaption>Aleppo, leaf 83r.</figcaption></figure>"
    )


def _first_kings_14_leningrad_crop() -> object:
    """The Leningrad Codex crop at 1 Kings 14:14."""
    return mb_html.raw_html(
        f'<figure><img src="{_FIRST_KINGS_14_LENINGRAD_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Leningrad", _UXLC_CHANGE_REF, "later-meteg")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;">'
        "<figcaption>Leningrad, folio 195B, column 2, line 27."
        "</figcaption></figure>"
    )


def _first_kings_14_cairo_cotp_crop() -> object:
    """The Cairo CoTP crop at 1 Kings 14:14, as interpreted by Ben."""
    return mb_html.raw_html(
        f'<figure><a href="{_POST_SILLUQ_CAIRO_COTP_SOURCE_URL}" target="_blank"'
        f' rel="noopener"><img src="{_FIRST_KINGS_14_CAIRO_COTP_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Cairo", _UXLC_CHANGE_REF, "no-later-mark")}"'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        "</a><figcaption>Cairo, digital image 204; "
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
        "<figcaption>Aleppo, leaf 251r.</figcaption></figure>"
    )


def _psalms_60_leningrad_crop() -> object:
    """The Leningrad Codex crop at Psalms 60:10."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_60_LENINGRAD_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Leningrad", _PSALMS_60_REF, "later-meteg")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;">'
        "<figcaption>Leningrad, folio 377B.</figcaption></figure>"
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
        "<figcaption>Aleppo, leaf 253r.</figcaption></figure>"
    )


def _psalms_70_leningrad_crop() -> object:
    """The Leningrad Codex crop at Psalms 70:2."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_70_LENINGRAD_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Leningrad", _PSALMS_70_REF, "later-meteg")}"'
        ' loading="lazy"'
        ' style="max-width: 100%; height: auto;">'
        "<figcaption>Leningrad, folio 379B.</figcaption></figure>"
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
        "<figcaption>Aleppo, leaf 253v.</figcaption></figure>"
    )


def _psalms_72_leningrad_crop() -> object:
    """The Leningrad Codex crop at Psalms 72:15."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_72_LENINGRAD_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Leningrad", _PSALMS_72_REF, "later-meteg")}"'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        "<figcaption>Leningrad, folio 380A, line 3."
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
        "<figcaption>Aleppo, leaf 271r, column 2, line 5."
        "</figcaption></figure>"
    )


def _job_4_leningrad_crop() -> object:
    """The Leningrad Codex crop at Job 4:12."""
    return mb_html.raw_html(
        f'<figure><img src="{_JOB_4_LENINGRAD_CROP_URL}"'
        f' alt="{_post_silluq_crop_alt("Leningrad", _JOB_4_REF, "both-strokes")}"'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        "<figcaption>Leningrad, folio 398A.</figcaption></figure>"
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


def _post_silluq_table_row(contents: tuple, attrs: tuple) -> object:
    """Build one row without the shared helper's silent ``zip`` truncation."""
    if len(contents) != len(attrs):
        raise ValueError(
            f"post-silluq table row has {len(contents)} cells and {len(attrs)} attributes"
        )
    return mb_html.table_row_of_data(contents, attrs)


def _post_silluq_source_state(state: str) -> object:
    """The visible, exhaustive source-state dispatch."""
    if state == "later-meteg":
        return ("later ", _ROM_METEG)
    if state == "no-later-mark":
        return "no later mark"
    if state == "both-strokes":
        return "both strokes"
    if state == "first-position-only":
        return "first position only"
    if state == "not-recorded":
        return "not recorded"
    if state == "tracked-observation":
        raise ValueError("tracked-observation needs the Koren observation dispatch")
    raise ValueError(f"Unknown post-silluq source state: {state!r}")


def _complete_koren_by_ref(observations: list[dict]) -> dict[str, dict]:
    """Index only completed observations for case-register joins."""
    return {
        observation["ref"]: observation
        for observation in observations
        if observation["status"] == "complete"
    }


def _case_source_mask_flags(
    case: dict, source: str, complete_koren_by_ref: dict[str, dict]
) -> tuple[bool, bool]:
    """Return the mutually exclusive has/does-not-have flags for one source."""
    state = case["sources"][source]
    if state in {"later-meteg", "both-strokes"}:
        flags = (True, False)
    elif state in {"no-later-mark", "first-position-only"}:
        flags = (False, True)
    elif state == "not-recorded":
        flags = (False, False)
    elif state == "tracked-observation":
        if source != "koren":
            raise ValueError(f"{case['ref']}: tracked observation assigned to {source}")
        observation = complete_koren_by_ref.get(case["ref"])
        if observation is None:
            raise ValueError(f"{case['ref']}: missing completed Koren observation")
        position = observation["koren"]
        if position == "first":
            flags = (False, True)
        elif position in {"last", "both"}:
            flags = (True, False)
        else:
            raise ValueError(f"Unknown Koren position: {position!r}")
    else:
        raise ValueError(
            f"{case['ref']}: cannot compare the last metsil for {source}: {state!r}"
        )
    if flags == (True, True):
        raise ValueError(f"{case['ref']}: {source} appears in both source masks")
    return flags


def _case_source_masks(case: dict, complete_koren_by_ref: dict[str, dict]) -> object:
    """Render the AL5CKS or AL57KS masks and their hover explanations."""
    return _source_mask_pair(*_case_source_mask_data(case, complete_koren_by_ref))


def _source_name_list(source_names: tuple[str, ...]) -> str:
    """Join source names for a compact hover explanation."""
    if len(source_names) == 1:
        return source_names[0]
    if len(source_names) == 2:
        return " and ".join(source_names)
    return f"{', '.join(source_names[:-1])}, and {source_names[-1]}"


def _source_mask_explanation(
    source_names: tuple[str, ...], *, has_later_meteg: bool
) -> str:
    """Explain one source-mask line in short manuscript and edition names."""
    if not source_names:
        return "No manuscript or edition is classified on this line"
    relation = (
        "a meteg after the silluq" if has_later_meteg else "no meteg after the silluq"
    )
    if len(source_names) == 1:
        return f"{source_names[0]} has {relation}"
    return (
        f"The following manuscripts and editions have {relation}: "
        f"{_source_name_list(source_names)}"
    )


def _source_mask_pair(
    has_mask: str,
    does_not_have_mask: str,
    has_names: tuple[str, ...] = (),
    does_not_have_names: tuple[str, ...] = (),
) -> object:
    """Color and hover-explain both lines of one source-mask pair."""
    has_title = escape(
        _source_mask_explanation(has_names, has_later_meteg=True), quote=True
    )
    does_not_have_title = escape(
        _source_mask_explanation(
            does_not_have_names,
            has_later_meteg=False,
        ),
        quote=True,
    )
    return mb_html.raw_html(
        f'<code><span class="post-silluq-mask-with-later" title="{has_title}">'
        f"{has_mask}</span>"
        f'<br><span class="post-silluq-mask-without-later"'
        f' title="{does_not_have_title}">'
        f"{does_not_have_mask}</span></code>"
    )


_POST_SILLUQ_SHORT_SOURCE_NAMES = {
    "aleppo": "Aleppo",
    "leningrad": "Leningrad",
    "cairo_cotp": "Cairo",
    "cam1753": "Cambridge",
    "sassoon_1053": "Sassoon",
    "koren": "Koren",
    "simanim": "Simanim",
}


def _case_source_mask_data(
    case: dict, complete_koren_by_ref: dict[str, dict]
) -> tuple[str, str, tuple[str, ...], tuple[str, ...]]:
    """Derive both source-mask lines and the short names that explain them."""
    sources = _post_silluq_sources_for_bcv(case["bcv"])
    flags_by_source = {
        source: _case_source_mask_flags(case, source, complete_koren_by_ref)
        for source in sources
    }
    has_later = any(flags[0] for flags in flags_by_source.values())
    lacks_later = any(flags[1] for flags in flags_by_source.values())
    if case["status"] == "last-metsil-contrast" and not (has_later and lacks_later):
        raise ValueError(
            f"{case['ref']}: sources do not establish a last-metsil position contrast"
        )
    has_mask = "".join(
        _POST_SILLUQ_SOURCE_CODES[source] if flags_by_source[source][0] else "-"
        for source in sources
    )
    does_not_have_mask = "".join(
        _POST_SILLUQ_SOURCE_CODES[source] if flags_by_source[source][1] else "-"
        for source in sources
    )
    has_names = tuple(
        _POST_SILLUQ_SHORT_SOURCE_NAMES[source]
        for source in sources
        if flags_by_source[source][0]
    )
    does_not_have_names = tuple(
        _POST_SILLUQ_SHORT_SOURCE_NAMES[source]
        for source in sources
        if flags_by_source[source][1]
    )
    return has_mask, does_not_have_mask, has_names, does_not_have_names


def _case_source_mask_values(
    case: dict, complete_koren_by_ref: dict[str, dict]
) -> tuple[str, str]:
    """Derive both source-mask strings from the classified source states."""
    has_mask, does_not_have_mask, _has_names, _does_not_have_names = (
        _case_source_mask_data(case, complete_koren_by_ref)
    )
    return has_mask, does_not_have_mask


# Each pair gives the first letter of the stressed syllable and the first letter of the
# later-meteg syllable. The pointed forms themselves come from tracked corpora, and the
# renderer checks their letters and the position of each mark before applying color.
_POST_SILLUQ_SYLLABLES = {
    "1s17:5": ("נחשת", 1, 2),
    "1k7:37": ("לכלהנה", 2, 4),
    "1k14:14": ("גםעתה", 2, 3),
    "ps60:10": ("התרעעי", 3, 4),
    "ps70:2": ("חושה", 0, 2),
    "ps72:15": ("יברכנהו", 3, 5),
    "jb4:12": ("מנהו", 0, 2),
}


def _colored_post_silluq_form(form: str, bcv: str, *, later_meteg: bool) -> object:
    """Color the stressed syllable and, when present, the later-meteg syllable."""
    if bcv not in _POST_SILLUQ_SYLLABLES:
        raise ValueError(f"Unknown post-silluq syllable boundaries: {bcv}")
    expected_letters, stressed_start, later_start = _POST_SILLUQ_SYLLABLES[bcv]
    if not form.endswith(psm.SOF_PASUQ):
        raise ValueError(f"{bcv}: expected a verse-final form")
    core = form.removesuffix(psm.SOF_PASUQ)
    letter_positions = [index for index, char in enumerate(core) if "א" <= char <= "ת"]
    letters = "".join(core[index] for index in letter_positions)
    if letters != expected_letters or not 0 <= stressed_start < later_start < len(
        letters
    ):
        raise ValueError(f"{bcv}: post-silluq syllable boundaries drifted")
    stressed_index = letter_positions[stressed_start]
    later_index = letter_positions[later_start]
    prefix, stressed, later = (
        core[:stressed_index],
        core[stressed_index:later_index],
        core[later_index:],
    )
    if (
        form.count(psm.METEG) != 1 + int(later_meteg)
        or stressed.count(psm.METEG) != 1
        or later.count(psm.METEG) != int(later_meteg)
    ):
        raise ValueError(
            f"{bcv}: post-silluq marks no longer match the colored syllables"
        )
    contents = [
        prefix,
        mb_html.span((stressed,), {"class": "post-silluq-stressed-syllable"}),
    ]
    if later_meteg:
        contents.append(
            mb_html.span((later,), {"class": "post-silluq-later-meteg-syllable"})
        )
    else:
        contents.append(later)
    contents.append(psm.SOF_PASUQ)
    return mb_html.span(tuple(contents), {"lang": "hbo"})


def _post_silluq_example_form(form: object, *, direction: str = "rtl") -> object:
    """Center a pointed Hebrew form or a two-line source mask."""
    return mb_html.para(
        (form,), {"class": "post-silluq-example-form", "dir": direction}
    )


def _post_silluq_source_code_table() -> object:
    """List the one-character codes in the introductory mask's source order."""
    rows = [
        _post_silluq_table_row(
            (mb_html.code(code), source, source_range),
            (None, None, None),
        )
        for code, source, source_range in (
            ("A", "Aleppo Codex", ""),
            ("L", "Leningrad Codex", ""),
            ("5", "Sassoon 1053", ""),
            ("C", "Cairo CoTP", "Prophets"),
            ("7", "Cambridge 1753", "Writings"),
            ("K", "Koren Classic Tanakh", ""),
            ("S", "Simanim Tanakh", ""),
        )
    ]
    return _table(("code", "manuscript or edition", "range"), rows)


def _post_silluq_first_samuel_example(
    cases: list[dict],
    forms: dict[str, str],
    mam_forms: dict[str, str],
    observations: list[dict],
) -> list:
    """Introduce the two forms, syllable colors, and AL5CKS at 1 Samuel 17:5."""
    cases_by_bcv = {case["bcv"]: case for case in cases}
    first_samuel = cases_by_bcv.get(_POST_SILLUQ_VERSE)
    if first_samuel is None:
        raise ValueError("The source-mask example requires 1 Samuel 17:5")
    expected_sources = {
        "aleppo": "no-later-mark",
        "leningrad": "later-meteg",
        "cairo_cotp": "no-later-mark",
        "sassoon_1053": "no-later-mark",
        "koren": "no-later-mark",
        "simanim": "no-later-mark",
    }
    if (
        first_samuel["status"] != "last-metsil-contrast"
        or first_samuel["sources"] != expected_sources
    ):
        raise ValueError("1 Samuel 17:5: source-mask example drifted")
    leningrad_form = forms[_POST_SILLUQ_VERSE]
    aleppo_form = mam_forms[_POST_SILLUQ_VERSE]
    if leningrad_form.count(psm.METEG) != 2 or aleppo_form.count(psm.METEG) != 1:
        raise ValueError("1 Samuel 17:5: expected two and one metsil, respectively")
    later_mark_index = leningrad_form.rfind(psm.METEG)
    if (
        leningrad_form[:later_mark_index] + leningrad_form[later_mark_index + 1 :]
        != aleppo_form
    ):
        raise ValueError("1 Samuel 17:5: the two forms differ beyond the later meteg")
    mask_data = _case_source_mask_data(
        first_samuel, _complete_koren_by_ref(observations)
    )
    masks = mask_data[:2]
    if masks != ("-L----", "A-5CKS"):
        raise ValueError("1 Samuel 17:5: introductory source masks drifted")
    return [
        mb_html.para(
            (
                "For example, Jacobson, in his ",
                chb(),
                " (p. 31), brought a case at ",
                _ref_link(_POST_SILLUQ_VERSE),
                " to our attention. In the Leningrad Codex, and in the many editions "
                "that, for better or for worse, try to stick close to that manuscript, "
                "the final word (letters ",
                wrap_hebrew_runs("".join(_letters_of(leningrad_form))),
                ") has a ",
                _ROM_METEG,
                " after the ",
                _ROM_SILLUQ,
                ":",
            )
        ),
        _post_silluq_example_form(wrap_hebrew_runs(leningrad_form)),
        mb_html.para(
            (
                "Or, coloring its stressed syllable green and the syllable of its later ",
                _ROM_METEG,
                " yellow (for “caution”):",
            )
        ),
        _post_silluq_example_form(
            _colored_post_silluq_form(
                leningrad_form, _POST_SILLUQ_VERSE, later_meteg=True
            )
        ),
        mb_html.para(
            (
                "In contrast, in other manuscripts and editions, there is no such ",
                _ROM_METEG,
                " after the ",
                _ROM_SILLUQ,
                ":",
            )
        ),
        _post_silluq_example_form(
            _colored_post_silluq_form(
                aleppo_form, _POST_SILLUQ_VERSE, later_meteg=False
            )
        ),
        mb_html.para("These other manuscripts and editions include the following:"),
        mb_html.unordered_list(
            (
                "The Aleppo Codex",
                "The Cairo CoTP (Codex of the Prophets)",
                "The Sassoon 1053 Codex",
                "Various editions of Tanakh that are not so slavishly devoted to the "
                "Leningrad Codex, such as the editions of Koren and the Simanim.",
            )
        ),
        mb_html.para("We might compactly represent the situation like this:"),
        _post_silluq_example_form(
            _source_mask_pair(*mask_data),
            direction="ltr",
        ),
        mb_html.para(
            (
                "That notation uses one-character manuscript/edition codes to show, "
                "on its first line, who has a ",
                _ROM_METEG,
                " after ",
                _ROM_SILLUQ,
                ", and on the second line, who doesn't. The codes are as follows:",
            )
        ),
        _post_silluq_source_code_table(),
        mb_html.para(
            "So, for cases in The Prophets, the full possible array of codes is "
            "AL5CKS, and for cases in The Writings, the full possible array is "
            "AL57KS. Note that in the array for The Writings, there is a '7' "
            "where for The Prophets we had a 'C'."
        ),
    ]


def _case_register_source_cell(
    case: dict, complete_koren_by_ref: dict[str, dict]
) -> object:
    """Render either recorded source masks or an unresolved candidate label."""
    status = case["status"]
    if status == "last-metsil-contrast":
        return _case_source_masks(case, complete_koren_by_ref)
    if status == "open-candidate":
        masks = (
            _case_source_masks(case, complete_koren_by_ref)
            if "sources" in case
            else _source_mask_pair("----", "----")
        )
        return (
            masks,
            mb_html.line_break(),
            mb_html.small(("candidate: ", ", ".join(case["transcriptions"]))),
        )
    raise ValueError(f"{case['ref']}: unknown case status {status!r}")


def _post_silluq_case_register(
    cases: list[dict],
    forms: dict[str, str],
    observations: list[dict],
) -> list:
    """The cross-source contrasts and unresolved candidates in one table."""
    complete_koren_by_ref = _complete_koren_by_ref(observations)
    headers = (
        "",
        mb_html.abbr(
            "bcv & img", {"title": "book-chapter-verse as a link to manuscript images"}
        ),
        "Sources",
    )
    attrs = (
        _HEBREW_CELL,
        _POST_SILLUQ_BCV_CELL,
        None,
    )
    sorted_cases = sorted(cases, key=lambda case: _scriptural_bcv_key(case["bcv"]))
    rows = [
        _post_silluq_table_row(
            (
                _colored_post_silluq_form(
                    forms[case["bcv"]], case["bcv"], later_meteg=True
                ),
                mb_html.anchor_h(
                    site_data.POST_STRESS_METEG_POST_SILLUQ_IMAGE_PAGES[case["bcv"]][1],
                    site_data.POST_STRESS_METEG_POST_SILLUQ_IMAGE_PAGES[case["bcv"]][0],
                ),
                _case_register_source_cell(case, complete_koren_by_ref),
            ),
            attrs,
        )
        for case in sorted_cases
    ]
    contents = [
        mb_html.heading_level_2("Case register", {"id": "case-register"}),
        mb_html.para(
            "Having introduced our notations through the 1 Sam. 17:5 example above, "
            "we now present all our cases of concern. In the table below, the "
            '"bcv & img" column contains links to pages showing crops of the '
            "relevant manuscript images."
        ),
        _table(
            headers,
            rows,
            {"class": "post-stress-meteg-table post-silluq-register"},
        ),
    ]
    unclassified_mask_data = None
    for case in sorted_cases:
        if "sources" not in case:
            continue
        mask_data = _case_source_mask_data(case, complete_koren_by_ref)
        if any(
            top == bottom == "-" for top, bottom in zip(*mask_data[:2], strict=True)
        ):
            unclassified_mask_data = mask_data
            break
    if unclassified_mask_data is not None:
        contents.extend(
            (
                mb_html.para("In entries such as:"),
                _post_silluq_example_form(
                    _source_mask_pair(*unclassified_mask_data), direction="ltr"
                ),
                mb_html.para(
                    "A dash in both lines at the same position means that no "
                    "classification is recorded for that source."
                ),
            )
        )
    return contents


def _post_silluq_source_notes(cases: list[dict], forms: dict[str, str]) -> list:
    """Subordinate provenance and editorial notes not encoded by the source masks."""
    cases_by_bcv = {case["bcv"]: case for case in cases}
    required = {_MAM_POST_SILLUQ_VERSE, _UXLC_CHANGE_VERSE}
    if not required <= set(cases_by_bcv):
        raise ValueError(
            "The post-silluq source notes require "
            f"{sorted(required - set(cases_by_bcv))}"
        )

    first_kings_seven = cases_by_bcv[_MAM_POST_SILLUQ_VERSE]
    expected_first_kings_seven_sources = {
        "aleppo": "later-meteg",
        "leningrad": "no-later-mark",
        "cairo_cotp": "no-later-mark",
        "sassoon_1053": "no-later-mark",
        "koren": "tracked-observation",
        "simanim": "no-later-mark",
    }
    if (
        first_kings_seven["status"] != "last-metsil-contrast"
        or first_kings_seven["form_source"] != "mam"
        or first_kings_seven["sources"] != expected_first_kings_seven_sources
        or first_kings_seven.get("mam_editorial_basis") != "aleppo-default"
    ):
        raise ValueError("1 Kings 7:37: MAM editorial note drifted")
    first_kings_seven_form = forms[_MAM_POST_SILLUQ_VERSE]
    if first_kings_seven_form.count(psm.METEG) != 2:
        raise ValueError("1 Kings 7:37: expected silluq and later meteg in MAM")

    first_kings_fourteen = cases_by_bcv[_UXLC_CHANGE_VERSE]
    if (
        first_kings_fourteen["sources"]["leningrad"] != "later-meteg"
        or first_kings_fourteen["sources"]["cairo_cotp"] != "no-later-mark"
    ):
        raise ValueError("1 Kings 14:14: manuscript classifications drifted")
    first_kings_fourteen_form = forms[_UXLC_CHANGE_VERSE]
    if (
        psm.MAQAF not in first_kings_fourteen_form
        or first_kings_fourteen_form.count(psm.METEG) != 2
    ):
        raise ValueError("1 Kings 14:14: UXLC form drifted")

    return [
        mb_html.para(
            (
                "MAM's note at ",
                _ref_link(_MAM_POST_SILLUQ_VERSE),
                " reports both manuscript readings: Aleppo has the later ",
                _ROM_METEG,
                ", while Leningrad has the ",
                _ROM_SILLUQ,
                " alone. MAM's body text has the ",
                _ROM_METEG,
                " after ",
                _ROM_SILLUQ,
                ", following Aleppo. This choice retains MAM's general policy of "
                "following Aleppo (",
                _footnote_callout(2, _POST_SILLUQ_MAM_POLICY_FOOTNOTE_ID),
                ").",
            )
        ),
        mb_html.para(
            (
                "At ",
                _ref_link(_UXLC_CHANGE_VERSE),
                ", UXLC acquired a ",
                _ROM_METEG,
                " after the ",
                _ROM_SILLUQ,
                " through ",
                mb_html.anchor_h(
                    "Daniel Holman's change proposal 2022.08.31-17",
                    _UXLC_CHANGE_URL,
                ),
                ".",
            )
        ),
    ]


def _post_silluq_discovery_credits(cases: list[dict]) -> list:
    """Credit the publications and searches through which the cases became known."""
    bcvs = {case["bcv"] for case in cases}
    expected_bcvs = {
        _POST_SILLUQ_VERSE,
        _MAM_POST_SILLUQ_VERSE,
        _UXLC_CHANGE_VERSE,
        "ps60:10",
        "ps70:2",
        "ps72:15",
        "jb4:12",
    }
    if bcvs != expected_bcvs:
        raise ValueError(
            "The Da'at Miqra five-of-seven account requires exactly these cases: "
            f"missing {sorted(expected_bcvs - bcvs)}; "
            f"unexpected {sorted(bcvs - expected_bcvs)}"
        )

    # The CoS citation follows Ben's print reference. The OCR export attaches the same note
    # to section 46 as its internal note [^81], which does not replace the printed citation.
    return [
        mb_html.heading_level_2("Notes on the cases"),
        mb_html.para(
            (
                "As mentioned above, we became aware of ",
                _ref_link(_POST_SILLUQ_VERSE),
                " from Jacobson, ",
                chb(),
                ", p. 31. We became aware of ",
                _ref_link(_MAM_POST_SILLUQ_VERSE),
                " from Breuer, ",
                cos(),
                ", ch. 8 §47, footnote 54 (p. 355 in the Wengrov English translation). "
                "We became aware of the remaining five entries from various searches "
                "of our own. After finding those five, we learned that reference works "
                "also record them. We catalog those references below.",
            )
        ),
    ]


def _post_silluq_catalog_x(kind: str) -> object:
    """Render an accessible gray or red X for an expected or questioned omission."""
    if kind == "expected":
        color = "gray"
        explanation = "not recorded; absence expected"
    elif kind == "questioned":
        color = "red"
        explanation = "not recorded; omission questioned"
    else:
        raise ValueError(f"Unknown post-silluq catalog X kind: {kind!r}")
    return mb_html.span(
        "\N{BALLOT X}",
        {
            "style": f"color: {color}; font-weight: 700;",
            "title": explanation,
            "aria-label": explanation,
        },
    )


def _post_silluq_reference_catalog(cases: list[dict]) -> list:
    """Catalog where Breuer and Dotan record the seven post-silluq cases."""
    expected_bcvs = {
        _POST_SILLUQ_VERSE,
        _MAM_POST_SILLUQ_VERSE,
        _UXLC_CHANGE_VERSE,
        "ps60:10",
        "ps70:2",
        "ps72:15",
        "jb4:12",
    }
    bcvs = {case["bcv"] for case in cases}
    if bcvs != expected_bcvs:
        raise ValueError(
            "The Breuer-Dotan catalog requires exactly these cases: "
            f"missing {sorted(expected_bcvs - bcvs)}; "
            f"unexpected {sorted(bcvs - expected_bcvs)}"
        )

    centered = {"class": "centered"}
    catalog_rows = [
        _post_silluq_table_row(
            (_ref_link("1s17:5"), mb_html.code("DM"), mb_html.code("BHL AppA")),
            (None, centered, centered),
        ),
        _post_silluq_table_row(
            (
                _ref_link("1k7:37"),
                cos(),
                _post_silluq_catalog_x("expected"),
            ),
            (None, centered, centered),
        ),
        _post_silluq_table_row(
            (
                _ref_link("1k14:14"),
                mb_html.code("DM"),
                _post_silluq_catalog_x("questioned"),
            ),
            (None, centered, centered),
        ),
        *(
            _post_silluq_table_row(
                (_ref_link(bcv), mb_html.code("DM"), mb_html.code("BHL body")),
                (None, centered, centered),
            )
            for bcv in ("ps60:10", "ps70:2", "ps72:15")
        ),
        _post_silluq_table_row(
            (
                _ref_link("jb4:12"),
                _post_silluq_catalog_x("questioned"),
                mb_html.code("BHL body"),
            ),
            (None, centered, centered),
        ),
    ]
    decoding_rows = [
        _post_silluq_table_row(
            ("Breuer", mb_html.code("DM"), author.book_title("Da'at Miqra")),
            (None, centered, None),
        ),
        _post_silluq_table_row(
            (
                "Breuer",
                mb_html.code("CoS"),
                author.book_title("The Cantillation of Scripture"),
            ),
            (None, centered, None),
        ),
        _post_silluq_table_row(
            (
                "Dotan",
                mb_html.code("BHL AppA"),
                (
                    author.book_title("Biblia Hebraica Leningradensia"),
                    ", Appendix A",
                ),
            ),
            (None, centered, None),
        ),
        _post_silluq_table_row(
            (
                "Dotan",
                mb_html.code("BHL body"),
                (
                    author.book_title("Biblia Hebraica Leningradensia"),
                    ", body (non-Appendix) text",
                ),
            ),
            (None, centered, None),
        ),
    ]
    return [
        mb_html.para(
            "Below we catalog how these seven cases are or are not recorded in "
            "works by Breuer and Dotan."
        ),
        _table(("bcv", "Breuer", "Dotan"), catalog_rows),
        _table(("scholar", "code", "decoding"), decoding_rows),
        mb_html.para("Further notes on the first table:"),
        mb_html.unordered_list(
            (
                (
                    "The gray ",
                    _post_silluq_catalog_x("expected"),
                    " in Dotan's column marks BHL's expected omission at ",
                    _ref_link(_MAM_POST_SILLUQ_VERSE),
                    ": BHL follows Leningrad here, and Leningrad has no ",
                    _ROM_METEG,
                    " after the ",
                    _ROM_SILLUQ,
                    ".",
                ),
                (
                    "The red ",
                    _post_silluq_catalog_x("questioned"),
                    " in Dotan's column marks BHL's omission at ",
                    _ref_link(_UXLC_CHANGE_VERSE),
                    ". BHL's body has only the ",
                    _ROM_SILLUQ,
                    ", and Appendix A has no entry. I regard that combined omission "
                    "as an error.",
                ),
                (
                    "The red ",
                    _post_silluq_catalog_x("questioned"),
                    " in Breuer's column marks the absence of ",
                    _ref_link("jb4:12"),
                    " from both ",
                    author.book_title("Da'at Miqra"),
                    " and ",
                    cos(),
                    ". The omission may be intentional because the Aleppo and "
                    "Leningrad codices agree there, so there might seem to be nothing "
                    "to note. But Koren has the ",
                    _ROM_SILLUQ,
                    " alone, and the Second Rabbinic Bible (the Venice Mikra'ot "
                    "Gedolot of 1524–25) appears to have the ",
                    _ROM_SILLUQ,
                    " alone. Koren would probably not be noted in either work, but "
                    "Breuer typically notes the Second Rabbinic Bible with his sigil ",
                    wrap_hebrew_runs("ד"),
                    " (dalet).",
                ),
            )
        ),
    ]


def _urj_distinct_stroke_mam_form() -> str:
    """MAM's final word at Numbers 23:26, lifted for the printed-edition example."""
    form = _mam_final_forms({_URJ_DISTINCT_STROKE_VERSE})[_URJ_DISTINCT_STROKE_VERSE]
    assert _letters_of(form) == ("אעשה",), form
    assert form.count("\N{HEBREW POINT SEGOL}" + psm.METEG) == 2, form
    assert form.endswith(psm.SOF_PASUQ), form
    return form.removesuffix(psm.SOF_PASUQ)


def _urj_distinct_stroke_figure() -> object:
    """The supplied crop illustrating the URJ edition's two stroke lengths."""
    return mb_html.raw_html(
        f'<figure><img src="{_URJ_DISTINCT_STROKE_CROP_URL}"'
        f' alt="The last word of {_URJ_DISTINCT_STROKE_REF} in the 2005 revised URJ'
        " ḥumash; the silluq stroke is longer than the meteg stroke, and each is beside"
        ' a segol." loading="lazy" style="max-width: 100%; height: auto;">'
        "<figcaption>The 2005 revised URJ ḥumash, "
        f"{_URJ_DISTINCT_STROKE_REF}.</figcaption></figure>"
    )


def _post_silluq_additional_sources(cases: list[dict]) -> list:
    """Curated observations outside the case-register source masks."""
    cases_with_additions = [case for case in cases if case.get("additional_sources")]
    if not cases_with_additions:
        return []
    contents = [mb_html.heading_level_2("Additional source observations")]
    for case in cases_with_additions:
        contents.extend(
            (
                mb_html.heading_level_3(_ref_link(case["bcv"])),
                mb_html.unordered_list(
                    tuple(
                        (
                            addition["source"],
                            ": ",
                            _post_silluq_source_state(addition["state"]),
                            ".",
                        )
                        for addition in case["additional_sources"]
                    )
                ),
            )
        )
    return contents


def _post_silluq_image_intro(source: str, ref: str, state: str) -> list:
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
        mb_html.para((source, *claim, " at ", ref, ".")),
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
            *_post_silluq_image_intro("Cairo", _POST_SILLUQ_REF, "no-later-mark"),
            _post_silluq_cairo_cotp_crop(),
            mb_html.para(
                (
                    "A stroke attached to the lamed ascender in the crop may look "
                    "like a ",
                    _ROM_METEG,
                    ", but it is part of the scribe's lamed. Ben notes that the "
                    "other lameds on the manuscript page have the same feature.",
                )
            ),
        ]
    if image_id == "sassoon-1053-1s17-5":
        return [
            *_post_silluq_image_intro("Sassoon", _POST_SILLUQ_REF, "no-later-mark"),
            _post_silluq_sassoon_crop(),
        ]
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
            *_post_silluq_image_intro("Sassoon", _JOB_4_REF, "both-strokes"),
            _job_4_sassoon_crop(),
            mb_html.para(
                (
                    "Sassoon's later stroke is far from vertical: it slants northeast "
                    "to southwest. I have no idea whether that slant is meaningful, but "
                    "it is too conspicuous to leave unmentioned.",
                )
            ),
        ]
    raise ValueError(f"Unknown post-silluq image identifier: {image_id!r}")


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
    for image_id in case["images"]:
        contents.extend(_post_silluq_image_nodes(image_id))
    if bcv == "jb4:12":
        # Ben's placement observations are recorded in the Job report and its update.
        contents.extend(
            (
                mb_html.heading_level_2("Position of the two strokes"),
                mb_html.para(
                    (
                        "We usually regard the position of an “early ",
                        _ROM_METEG,
                        "”—a ",
                        _ROM_METEG,
                        " to the right of its vowel—as meaningless. Yet the stroke under "
                        "the mem is to the right of its segol in both Aleppo and "
                        "Leningrad. On this page's interpretation, both manuscripts "
                        "therefore have an “early ",
                        _ROM_SILLUQ,
                        "” here, which seems an extraordinary coincidence. In Cambridge, the ",
                        _ROM_SILLUQ,
                        " under the mem is to the left of its segol, in the normal position.",
                    )
                ),
            )
        )
    return contents


def build_post_silluq_body(
    survey: dict, cases: list[dict], observations: list[dict]
) -> list:
    """The maintained page for cases and candidates of meteg after silluq."""
    mam_bcvs = {case["bcv"] for case in cases}
    if len(cases) != 7 or {
        case["bcv"]
        for case in cases
        if case["sources"]["aleppo"] in {"later-meteg", "both-strokes"}
    } != {_MAM_POST_SILLUQ_VERSE, "jb4:12"}:
        raise ValueError("The MAM policy footnote's two-of-seven claim drifted")
    if mam_bcvs != set(site_data.POST_STRESS_METEG_POST_SILLUQ_IMAGE_PAGES):
        raise ValueError(
            "Manuscript-image page declarations differ from the case ledger"
        )
    mam_forms = _mam_final_forms(mam_bcvs)
    forms = _case_forms(cases, mam_forms)
    return [
        mb_html.heading_level_1(_visible_title(_POST_SILLUQ_TITLE)),
        _hebrew_spacing_option(),
        mb_html.para(
            (
                "← Back to ",
                mb_html.anchor_h(
                    _visible_title(_TITLE), f"{_FNAME}#{_POST_SILLUQ_FOOTNOTE_ID}"
                ),
                ".",
            )
        ),
        mb_html.para(
            (
                "With very few exceptions, manuscripts and printed editions use the same"
                " vertical stroke for both ",
                _ROM_METEG,
                " and ",
                _ROM_SILLUQ,
                " (",
                _footnote_callout(1, _POST_SILLUQ_DISTINCT_STROKE_FOOTNOTE_ID),
                "). Here we coin a portmanteau “",
                _METSIL,
                "” to describe that ambiguous stroke. A verse-final word always has at least one ",
                _METSIL,
                ". If it has only one ",
                _METSIL,
                ", that ",
                _METSIL,
                " must be the ",
                _ROM_SILLUQ,
                ". But if it has more than one ",
                _METSIL,
                ", it is not clear which one is the ",
                _ROM_SILLUQ,
                ". Fortunately, in all but a handful of cases, the last ",
                _METSIL,
                " is the ",
                _ROM_SILLUQ,
                ". This document discusses the handful of cases in which the last ",
                _METSIL,
                " is a ",
                _ROM_METEG,
                " rather than the ",
                _ROM_SILLUQ,
                ". That is to say, in these cases there is a ",
                _ROM_METEG,
                " after the ",
                _ROM_SILLUQ,
                ".",
            )
        ),
        *_post_silluq_first_samuel_example(cases, forms, mam_forms, observations),
        *_post_silluq_case_register(cases, forms, observations),
        *_post_silluq_discovery_credits(cases),
        *_post_silluq_source_notes(cases, forms),
        *_post_silluq_reference_catalog(cases),
        *_post_silluq_additional_sources(cases),
        mb_html.heading_level_2(
            ("φ1 — A distinct form for ", _ROM_SILLUQ),
            {"id": _POST_SILLUQ_DISTINCT_STROKE_FOOTNOTE_ID},
        ),
        mb_html.para(
            (
                "One book whose typography distinguishes ",
                _ROM_SILLUQ,
                " from ",
                _ROM_METEG,
                " is the 2005 revised edition of ",
                mb_html.anchor_h(
                    author.book_title("The Torah: A Modern Commentary"),
                    _PLAUT_STEIN_TORAH_URL,
                ),
                " (W. Gunther Plaut, original editor; David E. S. Stein,"
                " revised-edition editor). There are thousands of examples that could "
                "be used, but let's use its version of the last word of ",
                _ref_link(_URJ_DISTINCT_STROKE_VERSE),
                " (letters ",
                wrap_hebrew_runs("".join(_letters_of(_urj_distinct_stroke_mam_form()))),
                "), because in this word both the ",
                _ROM_SILLUQ,
                " and the ",
                _ROM_METEG,
                " appear next to a segol, providing an obvious visual yardstick:",
            )
        ),
        _urj_distinct_stroke_figure(),
        mb_html.heading_level_2(
            ("φ2 — MAM's use of Aleppo"),
            {"id": _POST_SILLUQ_MAM_POLICY_FOOTNOTE_ID},
        ),
        mb_html.para(
            (
                "MAM diverges from Aleppo only when a specific editorial policy requires "
                "a different form or, in a rare case, when Aleppo is fairly clearly "
                "erroneous or fairly clearly outside the manuscript tradition of which "
                "Aleppo is generally the greatest example. Because ",
                _ROM_METEG,
                " after ",
                _ROM_SILLUQ,
                " is so rare, such a judgment is difficult here, so it makes sense that "
                "MAM follows Aleppo in the two of our seven cases in which Aleppo has ",
                _ROM_METEG,
                " after ",
                _ROM_SILLUQ,
                ": ",
                _ref_link(_MAM_POST_SILLUQ_VERSE),
                " and ",
                _ref_link("jb4:12"),
                ".",
            )
        ),
    ]
