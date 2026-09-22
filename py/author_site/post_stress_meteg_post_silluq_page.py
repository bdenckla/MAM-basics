"""Render the post-silluq comparative evidence page."""

from __future__ import annotations


from accgram import post_stress_meteg_model as psm
from accgram.almost_errors_html_shared import wrap_hebrew_runs
from mb_author import author
from mb_misc import mb_html

from author_site.post_stress_meteg_shared import (
    _FIRST_KINGS_14_ALEPPO_CROP_URL,
    _FIRST_KINGS_14_LENINGRAD_CROP_URL,
    _FNAME,
    _HEBREW_CELL,
    _JOB_4_ALEPPO_CROP_URL,
    _JOB_4_LENINGRAD_CROP_URL,
    _JOB_4_REF,
    _MAM_POST_SILLUQ_ALEPPO_CROP_URL,
    _MAM_POST_SILLUQ_LENINGRAD_CROP_URL,
    _MAM_POST_SILLUQ_REF,
    _MAM_POST_SILLUQ_VERSE,
    _PLAUT_STEIN_TORAH_URL,
    _POST_SILLUQ_ALEPPO_CROP_URL,
    _POST_SILLUQ_BCV_CELL,
    _POST_SILLUQ_DISTINCT_STROKE_FOOTNOTE_ID,
    _POST_SILLUQ_FOOTNOTE_ID,
    _POST_SILLUQ_LC_CROP_SOURCE_URL,
    _POST_SILLUQ_LC_CROP_URL,
    _POST_SILLUQ_REF,
    _POST_SILLUQ_SOURCES,
    _POST_SILLUQ_SOURCE_CODES,
    _POST_SILLUQ_TITLE,
    _POST_SILLUQ_VERSE,
    _PSALMS_60_ALEPPO_CROP_URL,
    _PSALMS_60_LENINGRAD_CROP_URL,
    _PSALMS_60_REF,
    _PSALMS_70_ALEPPO_CROP_URL,
    _PSALMS_70_CAM1753_CROP_URL,
    _PSALMS_70_LENINGRAD_CROP_URL,
    _PSALMS_70_REF,
    _PSALMS_72_ALEPPO_CROP_URL,
    _PSALMS_72_LENINGRAD_CROP_URL,
    _PSALMS_72_REF,
    _ROM_METEG,
    _ROM_METSIL,
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


def _mam_post_silluq_aleppo_crop() -> object:
    """The Aleppo Codex crop at the MAM post-silluq site."""
    return mb_html.raw_html(
        f'<figure><img src="{_MAM_POST_SILLUQ_ALEPPO_CROP_URL}"'
        f' alt="Aleppo Codex crop of the verse-final word at {_MAM_POST_SILLUQ_REF};'
        ' it has a meteg after the silluq."'
        ' loading="lazy" style="max-width: 100%; height: auto;">'
        f"<figcaption>Aleppo Codex, {_MAM_POST_SILLUQ_REF}.</figcaption></figure>"
    )


def _mam_post_silluq_leningrad_crop() -> object:
    """The Leningrad Codex crop at the MAM post-silluq site."""
    return mb_html.raw_html(
        f'<figure><img src="{_MAM_POST_SILLUQ_LENINGRAD_CROP_URL}"'
        f' alt="Leningrad Codex crop of the verse-final word at {_MAM_POST_SILLUQ_REF};'
        ' it lacks a meteg after the silluq."'
        ' loading="lazy" style="width: 300px; max-width: 100%; height: auto;">'
        f"<figcaption>Leningrad Codex, {_MAM_POST_SILLUQ_REF}.</figcaption></figure>"
    )


def _post_silluq_lc_crop() -> object:
    """The directly inspectable LC line for 1 Samuel 17:5's post-silluq question."""
    return mb_html.raw_html(
        f'<figure><a href="{_POST_SILLUQ_LC_CROP_SOURCE_URL}" target="_blank"'
        f' rel="noopener"><img src="{_POST_SILLUQ_LC_CROP_URL}"'
        f' alt="Leningrad Codex, F159A, column 3, line 8: {_POST_SILLUQ_REF}."'
        ' loading="lazy"></a><figcaption>Leningrad Codex, F159A, column 3, line 8'
        f" ({_POST_SILLUQ_REF}); crop attached to "
        f'<a href="{_POST_SILLUQ_LC_CROP_SOURCE_URL}" target="_blank"'
        ' rel="noopener">phonetic-hbo #78</a>.</figcaption></figure>'
    )


def _post_silluq_aleppo_crop() -> object:
    """The Aleppo crop showing no meteg after the silluq in 1 Samuel 17:5."""
    return mb_html.raw_html(
        f'<figure><img src="{_POST_SILLUQ_ALEPPO_CROP_URL}"'
        f' alt="Aleppo Codex crop of the verse-final word in {_POST_SILLUQ_REF}; it has'
        ' no meteg after the silluq." loading="lazy">'
        f"<figcaption>Aleppo Codex, {_POST_SILLUQ_REF}.</figcaption></figure>"
    )


def _first_kings_14_aleppo_crop() -> object:
    """The Aleppo Codex crop at 1 Kings 14:14."""
    return mb_html.raw_html(
        f'<figure><img src="{_FIRST_KINGS_14_ALEPPO_CROP_URL}"'
        f' alt="Aleppo Codex crop of the verse-final word at {_UXLC_CHANGE_REF}; it has'
        ' the silluq alone, without a second metsil." loading="lazy"'
        ' style="max-width: 100%; height: auto;">'
        f"<figcaption>Aleppo Codex, leaf 83r ({_UXLC_CHANGE_REF}).</figcaption></figure>"
    )


def _first_kings_14_leningrad_crop() -> object:
    """The Leningrad Codex crop at 1 Kings 14:14."""
    return mb_html.raw_html(
        f'<figure><img src="{_FIRST_KINGS_14_LENINGRAD_CROP_URL}"'
        f' alt="Leningrad Codex crop of the verse-final word at {_UXLC_CHANGE_REF}; it has'
        ' a second metsil after the silluq." loading="lazy"'
        ' style="max-width: 100%; height: auto;">'
        "<figcaption>Leningrad Codex, folio 195B, column 2, line 27 "
        f"({_UXLC_CHANGE_REF}).</figcaption></figure>"
    )


def _psalms_60_aleppo_crop() -> object:
    """The Aleppo Codex crop at Psalms 60:10."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_60_ALEPPO_CROP_URL}"'
        f' alt="Aleppo Codex crop of the verse-final word at {_PSALMS_60_REF}; it has the'
        ' silluq alone." loading="lazy" style="max-width: 100%; height: auto;">'
        f"<figcaption>Aleppo Codex, leaf 251r ({_PSALMS_60_REF}).</figcaption></figure>"
    )


def _psalms_60_leningrad_crop() -> object:
    """The Leningrad Codex crop at Psalms 60:10."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_60_LENINGRAD_CROP_URL}"'
        f' alt="Leningrad Codex crop of the verse-final word at {_PSALMS_60_REF}; it has'
        ' the silluq and a second metsil." loading="lazy"'
        ' style="max-width: 100%; height: auto;">'
        f"<figcaption>Leningrad Codex, folio 377B ({_PSALMS_60_REF}).</figcaption></figure>"
    )


def _psalms_70_aleppo_crop() -> object:
    """The Aleppo Codex crop at Psalms 70:2."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_70_ALEPPO_CROP_URL}"'
        f' alt="Aleppo Codex crop of the verse-final word at {_PSALMS_70_REF}; it has the'
        ' silluq alone." loading="lazy" style="max-width: 100%; height: auto;">'
        f"<figcaption>Aleppo Codex, leaf 253r ({_PSALMS_70_REF}).</figcaption></figure>"
    )


def _psalms_70_leningrad_crop() -> object:
    """The Leningrad Codex crop at Psalms 70:2."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_70_LENINGRAD_CROP_URL}"'
        f' alt="Leningrad Codex crop of the verse-final word at {_PSALMS_70_REF}; it has'
        ' the silluq and a second metsil." loading="lazy"'
        ' style="max-width: 100%; height: auto;">'
        f"<figcaption>Leningrad Codex, folio 379B ({_PSALMS_70_REF}).</figcaption></figure>"
    )


def _psalms_70_cam1753_crop() -> object:
    """The Cambridge Add. 1753 crop at Psalms 70:2."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_70_CAM1753_CROP_URL}"'
        f' alt="Cambridge Add. 1753 crop of the verse-final word at {_PSALMS_70_REF}; it has'
        ' the silluq alone." loading="lazy" style="max-width: 100%; height: auto;">'
        f"<figcaption>Cambridge Add. 1753 ({_PSALMS_70_REF}).</figcaption></figure>"
    )


def _psalms_72_aleppo_crop() -> object:
    """The Aleppo Codex crop at Psalms 72:15."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_72_ALEPPO_CROP_URL}"'
        f' alt="Aleppo Codex crop of the verse-final word at {_PSALMS_72_REF}; it lacks'
        ' a meteg after the silluq." loading="lazy" style="max-width: 100%; height: auto;">'
        f"<figcaption>Aleppo Codex, leaf 253v ({_PSALMS_72_REF}).</figcaption></figure>"
    )


def _psalms_72_leningrad_crop() -> object:
    """The Leningrad Codex crop at Psalms 72:15."""
    return mb_html.raw_html(
        f'<figure><img src="{_PSALMS_72_LENINGRAD_CROP_URL}"'
        f' alt="Leningrad Codex crop of the verse-final word at {_PSALMS_72_REF}; it has'
        ' a meteg after the silluq." loading="lazy" style="max-width: 100%; height: auto;">'
        f"<figcaption>Leningrad Codex, folio 380A, line 3 ({_PSALMS_72_REF})."
        "</figcaption></figure>"
    )


def _job_4_aleppo_crop() -> object:
    """The Aleppo Codex crop at Job 4:12."""
    return mb_html.raw_html(
        f'<figure><img src="{_JOB_4_ALEPPO_CROP_URL}"'
        f' alt="Aleppo Codex crop of the verse-final word at {_JOB_4_REF}; it has both'
        ' strokes." loading="lazy" style="max-width: 100%; height: auto;">'
        f"<figcaption>Aleppo Codex, leaf 271r, column 2, line 5 ({_JOB_4_REF})."
        "</figcaption></figure>"
    )


def _job_4_leningrad_crop() -> object:
    """The Leningrad Codex crop at Job 4:12."""
    return mb_html.raw_html(
        f'<figure><img src="{_JOB_4_LENINGRAD_CROP_URL}"'
        f' alt="Leningrad Codex crop of the verse-final word at {_JOB_4_REF}; it has both'
        ' strokes." loading="lazy" style="max-width: 100%; height: auto;">'
        f"<figcaption>Leningrad Codex, folio 398A ({_JOB_4_REF}).</figcaption></figure>"
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
    """Render the ALKS masks, requiring a contrast only for classified cases."""
    flags_by_source = {
        source: _case_source_mask_flags(case, source, complete_koren_by_ref)
        for source in _POST_SILLUQ_SOURCES
    }
    has_later = any(flags[0] for flags in flags_by_source.values())
    lacks_later = any(flags[1] for flags in flags_by_source.values())
    if case["status"] == "last-metsil-contrast" and not (has_later and lacks_later):
        raise ValueError(
            f"{case['ref']}: sources do not establish a last-metsil position contrast"
        )
    has_mask = "".join(
        _POST_SILLUQ_SOURCE_CODES[source] if flags_by_source[source][0] else "-"
        for source in _POST_SILLUQ_SOURCES
    )
    does_not_have_mask = "".join(
        _POST_SILLUQ_SOURCE_CODES[source] if flags_by_source[source][1] else "-"
        for source in _POST_SILLUQ_SOURCES
    )
    return mb_html.raw_html(f"<code>{has_mask}<br>{does_not_have_mask}</code>")


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
            else mb_html.raw_html("<code>----<br>----</code>")
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
    mam_forms: dict[str, str],
    observations: list[dict],
) -> list:
    """The cross-source contrasts and unresolved candidates in one table."""
    complete_koren_by_ref = _complete_koren_by_ref(observations)
    headers = ("Form", "Reference", "Sources")
    attrs = (
        _HEBREW_CELL,
        _POST_SILLUQ_BCV_CELL,
        None,
    )
    rows = [
        _post_silluq_table_row(
            (
                _hebrew_cell(forms[case["bcv"]]),
                _ref_link(case["bcv"]),
                _case_register_source_cell(case, complete_koren_by_ref),
            ),
            attrs,
        )
        for case in sorted(cases, key=lambda case: _scriptural_bcv_key(case["bcv"]))
    ]
    cases_by_bcv = {case["bcv"]: case for case in cases}
    first_samuel = cases_by_bcv.get(_POST_SILLUQ_VERSE)
    if first_samuel is None:
        raise ValueError("The source-mask example requires 1 Samuel 17:5")
    expected_first_samuel_sources = {
        "aleppo": "no-later-mark",
        "leningrad": "later-meteg",
        "koren": "no-later-mark",
        "simanim": "no-later-mark",
    }
    if first_samuel["sources"] != expected_first_samuel_sources:
        raise ValueError("1 Samuel 17:5: source-mask example drifted")
    first_samuel_form = mam_forms[_POST_SILLUQ_VERSE]
    if first_samuel_form.count(psm.METEG) != 1:
        raise ValueError("1 Samuel 17:5: expected one metsil in the printed form")
    return [
        mb_html.heading_level_2("Case register"),
        mb_html.para(
            (
                "Each classified case below has at least one source—a manuscript or printed "
                "edition—whose last ",
                _ROM_METSIL,
                " is later than the last ",
                _ROM_METSIL,
                " in at least one other source.",
            )
        ),
        mb_html.para(
            (
                "In each monospace cell, the first line marks sources that have the later ",
                _ROM_METSIL,
                " and the second line marks sources that do not. The four positions are "
                "A = Aleppo Codex, L = Leningrad Codex, K = Koren, and S = the Simanim "
                "Tanakh. In either line, a dash means that the source is not assigned to "
                "that line; only dashes in both lines at the same position mean that no "
                "classification is recorded for that source.",
            )
        ),
        mb_html.para(
            (
                "For example, at ",
                _ref_link(_POST_SILLUQ_VERSE),
                ", ",
                mb_html.raw_html("<code>-L--</code>"),
                " on the first line means that the Leningrad Codex has the later ",
                _ROM_METSIL,
                ", while ",
                mb_html.raw_html("<code>A-KS</code>"),
                " on the second line means that the Aleppo Codex, Koren, and the Simanim "
                "Tanakh do not. In other words, Aleppo, Koren and Simanim each have only one ",
                _ROM_METSIL,
                " and therefore it must be a ",
                _ROM_SILLUQ,
                ". That ",
                _ROM_METSIL,
                " is on ",
                wrap_hebrew_runs("ח"),
                ", i.e. they have ",
                wrap_hebrew_runs(first_samuel_form),
                ".",
            )
        ),
        mb_html.para(
            (
                "Rows labeled candidate record a later ",
                _ROM_METSIL,
                " in the named transcriptions, not in the Leningrad Codex manuscript itself. "
                "No Leningrad Codex classification is recorded until the manuscript is read.",
            )
        ),
        _table(
            headers,
            rows,
            {"class": "post-stress-meteg-table post-silluq-register"},
        ),
    ]


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
    if first_kings_fourteen["sources"]["leningrad"] != "later-meteg":
        raise ValueError("1 Kings 14:14: the LC classification drifted")
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
                " reports both manuscript readings: the Aleppo Codex has the later ",
                _ROM_METEG,
                ", while the Leningrad Codex has the ",
                _ROM_SILLUQ,
                " alone. MAM's body text has ",
                wrap_hebrew_runs(first_kings_seven_form),
                ", following the Aleppo Codex. This choice retains MAM's general "
                "policy of following the Aleppo Codex. MAM diverges from Aleppo when a "
                "specific editorial policy requires a different form or, in a rare case, "
                "when the Aleppo Codex is fairly clearly erroneous or fairly clearly "
                "outside the manuscript tradition of which the Aleppo Codex is generally "
                "the greatest example. Because ",
                _ROM_METEG,
                " after ",
                _ROM_SILLUQ,
                " is so rare, such a judgment is difficult here, so MAM follows the "
                "Aleppo Codex.",
            )
        ),
        mb_html.para(
            (
                "At ",
                _ref_link(_UXLC_CHANGE_VERSE),
                ", UXLC acquired a second ",
                _ROM_METSIL,
                " through ",
                mb_html.anchor_h(
                    "Daniel Holman's change proposal 2022.08.31-17",
                    _UXLC_CHANGE_URL,
                ),
                "; Breuer also notes the second ",
                _ROM_METSIL,
                " in ",
                mb_html.emphasis("Da'at Miqra"),
                ".",
            )
        ),
    ]


def _post_silluq_discovery_credits(cases: list[dict]) -> list:
    """Credit the publications and searches through which the cases became known."""
    bcvs = {case["bcv"] for case in cases}
    required = {_POST_SILLUQ_VERSE, _MAM_POST_SILLUQ_VERSE}
    if not required <= bcvs:
        raise ValueError(
            "The meteg-after-silluq discovery credits require "
            f"{sorted(required - bcvs)}"
        )

    # The CoS citation follows Ben's print reference. The OCR export attaches the same note
    # to section 46 as its internal note [^81], which does not replace the printed citation.
    return [
        mb_html.heading_level_2("Notes on the cases"),
        mb_html.para(
            (
                "We became aware of ",
                _ref_link(_POST_SILLUQ_VERSE),
                " from Jacobson, ",
                chb(),
                ", p. 31, and of ",
                _ref_link(_MAM_POST_SILLUQ_VERSE),
                " from Breuer, ",
                cos(),
                ", ch. 8 §47, footnote 54 (p. 355 in the Wengrov English translation). The "
                "remaining entries came from systematic "
                "candidate searches.",
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
    """Curated observations outside the four main source columns."""
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


def _post_silluq_image_nodes(image_id: str) -> list:
    """The fixed claim and existing deployed figure for one known image identifier."""
    if image_id == "lc-1s17-5":
        return [
            mb_html.para(
                (
                    "The Leningrad Codex has a ",
                    _ROM_METEG,
                    " after its ",
                    _ROM_SILLUQ,
                    f" at {_POST_SILLUQ_REF}.",
                )
            ),
            _post_silluq_lc_crop(),
        ]
    if image_id == "aleppo-1s17-5":
        return [
            mb_html.para(
                (
                    "The Aleppo Codex lacks the later ",
                    _ROM_METEG,
                    f" at {_POST_SILLUQ_REF}.",
                )
            ),
            _post_silluq_aleppo_crop(),
        ]
    if image_id == "aleppo-1k14-14":
        return [
            mb_html.para(
                (
                    "At ",
                    _ref_link(_UXLC_CHANGE_VERSE),
                    ", the Aleppo Codex lacks the second ",
                    _ROM_METSIL,
                    " that the Leningrad Codex has. The Leningrad Codex's second ",
                    _ROM_METSIL,
                    " is the likely ",
                    _ROM_METEG,
                    " after the ",
                    _ROM_SILLUQ,
                    ".",
                )
            ),
            _first_kings_14_aleppo_crop(),
        ]
    if image_id == "leningrad-1k14-14":
        return [_first_kings_14_leningrad_crop()]
    if image_id == "aleppo-ps60-10":
        return [
            mb_html.para(
                (
                    "At ",
                    _PSALMS_60_REF,
                    ", the Aleppo Codex has the ",
                    _ROM_SILLUQ,
                    " alone, while the Leningrad Codex has the ",
                    _ROM_SILLUQ,
                    " and a second ",
                    _ROM_METSIL,
                    ". The second Leningrad ",
                    _ROM_METSIL,
                    " is the likely ",
                    _ROM_METEG,
                    " after the ",
                    _ROM_SILLUQ,
                    ".",
                )
            ),
            _psalms_60_aleppo_crop(),
        ]
    if image_id == "leningrad-ps60-10":
        return [_psalms_60_leningrad_crop()]
    if image_id == "aleppo-ps70-2":
        return [
            mb_html.para(
                (
                    "At ",
                    _PSALMS_70_REF,
                    ", the Aleppo Codex and Cambridge Add. 1753 have the ",
                    _ROM_SILLUQ,
                    " alone, while the Leningrad Codex has the ",
                    _ROM_SILLUQ,
                    " and a second ",
                    _ROM_METSIL,
                    ". The second Leningrad ",
                    _ROM_METSIL,
                    " is the likely ",
                    _ROM_METEG,
                    " after the ",
                    _ROM_SILLUQ,
                    ".",
                )
            ),
            _psalms_70_aleppo_crop(),
        ]
    if image_id == "leningrad-ps70-2":
        return [_psalms_70_leningrad_crop()]
    if image_id == "cam1753-ps70-2":
        return [_psalms_70_cam1753_crop()]
    if image_id == "aleppo-ps72-15":
        return [
            mb_html.para(
                (
                    "The Aleppo Codex lacks the later ",
                    _ROM_METEG,
                    f" at {_PSALMS_72_REF}.",
                )
            ),
            _psalms_72_aleppo_crop(),
        ]
    if image_id == "leningrad-ps72-15":
        return [
            mb_html.para(
                (
                    "The Leningrad Codex has a later ",
                    _ROM_METEG,
                    f" at {_PSALMS_72_REF}.",
                )
            ),
            _psalms_72_leningrad_crop(),
        ]
    if image_id == "aleppo-1k7-37":
        return [
            mb_html.para(
                (
                    "The Aleppo Codex has a later ",
                    _ROM_METEG,
                    f" at {_MAM_POST_SILLUQ_REF}.",
                )
            ),
            _mam_post_silluq_aleppo_crop(),
        ]
    if image_id == "leningrad-1k7-37":
        return [
            mb_html.para(
                (
                    "The Leningrad Codex lacks the later ",
                    _ROM_METEG,
                    f" at {_MAM_POST_SILLUQ_REF}.",
                )
            ),
            _mam_post_silluq_leningrad_crop(),
        ]
    if image_id == "aleppo-jb4-12":
        return [
            mb_html.para(("The Aleppo Codex has both strokes at ", _JOB_4_REF, ".")),
            _job_4_aleppo_crop(),
        ]
    if image_id == "leningrad-jb4-12":
        return [
            mb_html.para(("The Leningrad Codex has both strokes at ", _JOB_4_REF, ".")),
            _job_4_leningrad_crop(),
        ]
    raise ValueError(f"Unknown post-silluq image identifier: {image_id!r}")


def _post_silluq_image_evidence(cases: list[dict]) -> list:
    """Render each case's ordered set of deployed manuscript crops and conclusions."""
    with_images = [case for case in cases if case["images"]]
    if not with_images:
        return []
    contents = [mb_html.heading_level_2("Image evidence")]
    for case in with_images:
        contents.append(mb_html.heading_level_3(_ref_link(case["bcv"])))
        for image_id in case["images"]:
            contents.extend(_post_silluq_image_nodes(image_id))
    return contents


def build_post_silluq_body(
    survey: dict, cases: list[dict], observations: list[dict]
) -> list:
    """The maintained page for cases and candidates of meteg after silluq."""
    mam_bcvs = {case["bcv"] for case in cases}
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
                _ROM_SILLUQ,
                " and ",
                _ROM_METEG,
                " (",
                _footnote_callout(1, _POST_SILLUQ_DISTINCT_STROKE_FOOTNOTE_ID),
                "). Here we call that stroke ",
                _ROM_METSIL,
                ". A verse-final word always has at least one ",
                _ROM_METSIL,
                ". If it has only one ",
                _ROM_METSIL,
                ", that ",
                _ROM_METSIL,
                " must be the ",
                _ROM_SILLUQ,
                ". But if it has more than one ",
                _ROM_METSIL,
                ", it is not clear which one is the ",
                _ROM_SILLUQ,
                ". Fortunately, in all but a handful of cases, the last ",
                _ROM_METSIL,
                " is the ",
                _ROM_SILLUQ,
                ". This document discusses the handful of cases in which the last ",
                _ROM_METSIL,
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
        mb_html.para(
            (
                "In this investigation, the printed tradition helps clarify marks in the "
                "manuscript tradition. Although printed editions generally have an excess of ",
                _ROM_METEG,
                " marks, the printed editions considered here sometimes have the ",
                _ROM_SILLUQ,
                " alone where a manuscript has a later ",
                _ROM_METSIL,
                ". The printed editions' lack of the later mark helps identify the "
                "corresponding manuscript mark as ",
                _ROM_METEG,
                " rather than ",
                _ROM_SILLUQ,
                ".",
            )
        ),
        *_post_silluq_case_register(cases, forms, mam_forms, observations),
        *_post_silluq_discovery_credits(cases),
        *_post_silluq_source_notes(cases, forms),
        *_post_silluq_additional_sources(cases),
        *_post_silluq_image_evidence(cases),
        mb_html.heading_level_2(
            ("φ1 — A distinct form for ", _ROM_SILLUQ),
            {"id": _POST_SILLUQ_DISTINCT_STROKE_FOOTNOTE_ID},
        ),
        mb_html.para(
            (
                "One exception is the 2005 revised edition of ",
                mb_html.anchor_h(
                    author.book_title("The Torah: A Modern Commentary"),
                    _PLAUT_STEIN_TORAH_URL,
                ),
                " (W. Gunther Plaut, original editor; David E. S. Stein,"
                " revised-edition editor), whose typography distinguishes ",
                _ROM_SILLUQ,
                " from ",
                _ROM_METEG,
                ".",
            )
        ),
        mb_html.para(
            (
                "In the last word of ",
                _ref_link(_URJ_DISTINCT_STROKE_VERSE),
                ", ",
                wrap_hebrew_runs(_urj_distinct_stroke_mam_form()),
                ", the ",
                _ROM_SILLUQ,
                " stroke is longer than the ",
                _ROM_METEG,
                " stroke. Each stroke is beside a segol, providing a direct visual"
                " yardstick.",
            )
        ),
        _urj_distinct_stroke_figure(),
    ]
