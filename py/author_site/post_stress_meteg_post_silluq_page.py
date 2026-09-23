"""Render the post-silluq comparative evidence page."""

from __future__ import annotations


from accgram import post_stress_meteg_model as psm
from accgram.almost_errors_html_shared import wrap_hebrew_runs
from author_site import site_data
from mb_author import author
from mb_misc import mb_html

from author_site.post_stress_meteg_shared import (
    _FIRST_KINGS_14_ALEPPO_CROP_URL,
    _FIRST_KINGS_14_LENINGRAD_CROP_URL,
    _FNAME,
    _HEBREW_CELL,
    _JOB_4_ALEPPO_CROP_URL,
    _JOB_4_CAM1753_CROP_URL,
    _JOB_4_LENINGRAD_CROP_URL,
    _JOB_4_REF,
    _MAM_POST_SILLUQ_ALEPPO_CROP_URL,
    _MAM_POST_SILLUQ_LENINGRAD_CROP_URL,
    _MAM_POST_SILLUQ_REF,
    _MAM_POST_SILLUQ_VERSE,
    _METSIL,
    _PLAUT_STEIN_TORAH_URL,
    _POST_SILLUQ_ALEPPO_CROP_URL,
    _POST_SILLUQ_BCV_CELL,
    _POST_SILLUQ_DISTINCT_STROKE_FOOTNOTE_ID,
    _POST_SILLUQ_FNAME,
    _POST_SILLUQ_FOOTNOTE_ID,
    _POST_SILLUQ_LC_CROP_SOURCE_URL,
    _POST_SILLUQ_LC_CROP_URL,
    _POST_SILLUQ_MAM_POLICY_FOOTNOTE_ID,
    _POST_SILLUQ_REF,
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


def _job_4_cam1753_crop() -> object:
    """The Cambridge Add. 1753 crop at Job 4:12."""
    return mb_html.raw_html(
        f'<figure><img src="{_JOB_4_CAM1753_CROP_URL}"'
        f' alt="Cambridge Add. 1753 crop of the verse-final word at {_JOB_4_REF}; it has'
        ' both strokes, with the silluq to the left of its segol." loading="lazy"'
        ' style="max-width: 100%; height: auto;">'
        f"<figcaption>Cambridge Add. 1753, page 0073B, column 2, line 13 ({_JOB_4_REF})."
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
    """Render the ALKS or AL7KS masks for one case."""
    has_mask, does_not_have_mask = _case_source_mask_values(case, complete_koren_by_ref)
    return _source_mask_pair(has_mask, does_not_have_mask)


def _source_mask_pair(has_mask: str, does_not_have_mask: str) -> object:
    """Color the later-metsil mask yellow and the no-later mask green."""
    return mb_html.raw_html(
        f'<code><span class="post-silluq-mask-with-later">{has_mask}</span>'
        f'<br><span class="post-silluq-mask-without-later">'
        f"{does_not_have_mask}</span></code>"
    )


def _case_source_mask_values(
    case: dict, complete_koren_by_ref: dict[str, dict]
) -> tuple[str, str]:
    """Derive both source-mask lines from the classified source states."""
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


def _post_silluq_first_samuel_example(
    cases: list[dict],
    forms: dict[str, str],
    mam_forms: dict[str, str],
    observations: list[dict],
) -> list:
    """Introduce the two forms, syllable colors, and ALKS notation at 1 Samuel 17:5."""
    cases_by_bcv = {case["bcv"]: case for case in cases}
    first_samuel = cases_by_bcv.get(_POST_SILLUQ_VERSE)
    if first_samuel is None:
        raise ValueError("The source-mask example requires 1 Samuel 17:5")
    expected_sources = {
        "aleppo": "no-later-mark",
        "leningrad": "later-meteg",
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
    masks = _case_source_mask_values(first_samuel, _complete_koren_by_ref(observations))
    if masks != ("-L--", "A-KS"):
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
                "Or, coloring its stressed syllable (its syllable of primary stress) "
                "green and the syllable of its later ",
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
                "In contrast, in the Aleppo Codex, and in editions of Tanakh that "
                "are not so slavishly devoted to the Leningrad Codex, such as Koren "
                "and the Simanim Tanakh, there is no such ",
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
        mb_html.para("We might compactly represent the situation like this:"),
        _post_silluq_example_form(
            _source_mask_pair(*masks),
            direction="ltr",
        ),
        mb_html.para(
            (
                "The first line means that the Leningrad Codex (L) has the later ",
                _METSIL,
                ", while the second line means that the Aleppo Codex (A), Koren (K), "
                "and the Simanim Tanakh (S) do not.",
            )
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
            "we now present all our cases of concern, using those notations:"
        ),
        _table(
            headers,
            rows,
            {"class": "post-stress-meteg-table post-silluq-register"},
        ),
        mb_html.para(
            (
                "In the three Psalms rows and the Job row, the source order is ",
                mb_html.code("AL7KS"),
                "; ",
                mb_html.code("7"),
                " represents Cambridge Add. 1753. The 1 Sam. 17:5 example above "
                "uses ",
                mb_html.code("ALKS"),
                " and does not include this source.",
            )
        ),
    ]
    unclassified_masks = None
    for case in sorted_cases:
        if "sources" not in case:
            continue
        masks = _case_source_mask_values(case, complete_koren_by_ref)
        if any(top == bottom == "-" for top, bottom in zip(*masks, strict=True)):
            unclassified_masks = masks
            break
    if unclassified_masks is not None:
        contents.extend(
            (
                mb_html.para("In entries such as:"),
                _post_silluq_example_form(
                    _source_mask_pair(*unclassified_masks), direction="ltr"
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
                " alone. MAM's body text has the ",
                _ROM_METEG,
                " after ",
                _ROM_SILLUQ,
                ", following the Aleppo Codex. This choice retains MAM's general "
                "policy of following the Aleppo Codex (",
                _footnote_callout(2, _POST_SILLUQ_MAM_POLICY_FOOTNOTE_ID),
                ").",
            )
        ),
        mb_html.para(
            (
                "At ",
                _ref_link(_UXLC_CHANGE_VERSE),
                ", UXLC acquired a second ",
                _METSIL,
                " through ",
                mb_html.anchor_h(
                    "Daniel Holman's change proposal 2022.08.31-17",
                    _UXLC_CHANGE_URL,
                ),
                "; Breuer also notes the second ",
                _METSIL,
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
                "of our own.",
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
                    _METSIL,
                    " that the Leningrad Codex has. The Leningrad Codex's second ",
                    _METSIL,
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
                    _METSIL,
                    ". The second Leningrad ",
                    _METSIL,
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
                    _METSIL,
                    ". The second Leningrad ",
                    _METSIL,
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
    if image_id == "cam1753-jb4-12":
        return [
            mb_html.para(
                (
                    "Cambridge Add. 1753 has a ",
                    _ROM_METEG,
                    " after the ",
                    _ROM_SILLUQ,
                    " at ",
                    _JOB_4_REF,
                    ".",
                )
            ),
            _job_4_cam1753_crop(),
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
        contents.append(
            mb_html.para(
                (
                    "We usually regard the position of an “early ",
                    _ROM_METEG,
                    "”—a ",
                    _ROM_METEG,
                    " to the right of its vowel—as meaningless. Yet the stroke under "
                    "the mem is to the right of its segol in both the Aleppo Codex and "
                    "the Leningrad Codex. On this page's interpretation, both codices "
                    "therefore have an “early ",
                    _ROM_SILLUQ,
                    "” here, which seems an extraordinary coincidence. In Cambridge Add. "
                    "1753, the ",
                    _ROM_SILLUQ,
                    " under the mem is to the left of its segol, in the normal position.",
                )
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
            ("φ2 — MAM's use of the Aleppo Codex"),
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
