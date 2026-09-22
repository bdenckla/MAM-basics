"""Filterable case-page rendering for the post-stress-meteg pages."""

from __future__ import annotations


from accgram import post_stress_meteg as psm
from mb_author import author
from mb_cmn import hebrew_accents as ha
from mb_misc import mb_html

from author_site.post_stress_meteg_shared import (
    _CASES_FNAME,
    _CASES_TITLE,
    _CASE_FILTER_OPTIONS,
    _CASE_FILTER_SCRIPT,
    _CASE_SELECTED_COUNT_ID,
    _CASE_TABLE_CLASS,
    _CASE_TABLE_ID,
    _CASE_TYPE_FILTER_ID,
    _FIT_FOR_MAS_CRITERIA,
    _FIT_FOR_MAS_SECTION_ID,
    _FNAME,
    _HEBREW_CELL,
    _LACKS_MAS_FILTER_OPTIONS,
    _LACKS_MAS_FILTER_SCRIPT,
    _LACKS_MAS_SELECTED_COUNT_ID,
    _LACKS_MAS_SUBTYPE_FILTER_ID,
    _LACKS_MAS_TABLE_ID,
    _LACKS_MAS_TITLE,
    _MISC_TABLE_ID,
    _MISC_TITLE,
    _NEXT_WORD_CLASS,
    _NOT_FIT_FAILURE_CLASS,
    _NOT_FIT_FILTER_OPTIONS,
    _NOT_FIT_FILTER_SCRIPT,
    _NOT_FIT_SELECTED_COUNT_ID,
    _NOT_FIT_TABLE_ID,
    _NOT_FIT_TITLE,
    _NOT_FIT_TYPE_FILTER_ID,
    _RED_X,
    _ROM_GAYA,
    _ROM_HOLAM,
    _ROM_PASEQ,
    _ROM_TSERE,
    _ROM_VAYOMER,
    _SUBTYPE_DESCRIPTIONS,
    _TITLE,
    _TYPE_1_SUBTYPE_CODES,
    _TYPE_2_SUBTYPE_CODE_BY_FILTER_GROUP,
    _TYPE_CODES,
    _hebrew_cell,
    _hebrew_spacing_option,
    _para,
    _ref_link,
    _spelled,
    _table,
    _visible_title,
    cos,
    itm,
    itm_sections,
)

from author_site.post_stress_meteg_survey import (
    _by_subtype_count,
    _lacks_mas_records,
    _misc_almost_type_3_only_member,
    _not_fit_for_mas_records,
)


def _case_type_code(kind: str) -> str:
    return _TYPE_CODES.get(kind, ("other", ""))[0]


def _case_type_cell(kind: str, *, misc_label: bool = False) -> object:
    """A type label, with the subpages' shorter vocabulary and misc label when requested."""
    if kind in _TYPE_CODES:
        code, gloss = _TYPE_CODES[kind]
        return mb_html.abbr(code, {"title": f"Type {code}: {gloss}."})
    if misc_label:
        return "misc"
    return mb_html.abbr("—", {"title": "Not one of types 1, 2, or 3."})


def _fit_type_cell(fit_type: str) -> object:
    """One Fit-for-MAS table label, including the two admitted type-1 subtypes."""
    titles = {
        psm.FIT_TYPE_1_A: (
            "Type 1A: type 1 where the next word has initial stress and an initial"
            " vocal shewa."
        ),
        psm.FIT_TYPE_1_B: (
            "Type 1B: type 1 where the next word has a pashta stress helper on its"
            " first letter, and so no initial vocal shewa."
        ),
        psm.FIT_TYPE_2_AF: (
            "Fit for MAS type 2Af: the word is closed by a guttural; the next word"
            " begins with ל (lamed) and does not begin with vocal shewa."
        ),
        psm.FIT_TYPE_2_BF: (
            "Fit for MAS type 2Bf: the word is closed by a guttural; the next word"
            " begins with a guttural and does not begin with vocal shewa."
        ),
        psm.FIT_TYPE_3: "Type 3: the MAS syllable is closed, final, and tsere-voweled.",
    }
    return mb_html.abbr(fit_type, {"title": titles[fit_type]})


def _structural_subtype_cell(record: dict) -> object:
    """One structural (sub)type label, the taxonomy the cases page's Subtype column uses.

    Ben's decision of 2026-09-08, on the Methods page's table of MAS words that also have a
    meteg before the stress: the fit-for-MAS codes 2Af and 2Bf are reserved for a fit-for-MAS
    context, and that table sits under Census definitions, which never mentions fitness.  Only
    1 Samuel 22:17 shows the difference -- the rest of that table is 1A and 3, which read the
    same in either taxonomy.
    """
    subtype = _case_filter_subtype(record)
    if subtype is None:
        return _case_type_cell(record["structural_type"], misc_label=True)
    return mb_html.abbr(subtype, {"title": _SUBTYPE_DESCRIPTIONS[subtype]})


def _case_subtype_cell(subtype: str | None) -> object:
    """The subtype only where a misc record has a named nearer condition."""
    if subtype is None:
        return ""
    gloss_by_subtype = {
        psm.SUBTYPE_MISC_VAYOMER: (
            "A vayomer case with one intervening paseq before the next word."
        ),
        psm.SUBTYPE_MISC_ALMOST_TYPE_3: (
            "A final closed ḥolam syllable: CoS's long-vowel type (a), but not"
            " our type 3, which is restricted to tsere."
        ),
    }
    visible_label: object = subtype
    if subtype == psm.SUBTYPE_MISC_VAYOMER:
        visible_label = ("misc-", _ROM_VAYOMER)
    return mb_html.abbr(visible_label, {"title": gloss_by_subtype[subtype]})


def _next_chanted_word_span(
    next_word: str, punctuation: tuple[dict[str, str], ...] | list[dict[str, str]] = ()
) -> object:
    """The next chanted word and each preceding native narrow-sense paseq."""
    demoted = []
    for marker in punctuation:
        assert marker["kind"] == "paseq", marker
        demoted.extend((*_hebrew_cell(marker["glyph"]), " "))
    demoted.extend(_hebrew_cell(next_word))
    return mb_html.span(
        tuple(demoted),
        {"class": _NEXT_WORD_CLASS},
    )


def _native_mam_punctuation_parts(
    punctuation: tuple[dict[str, str], ...] | list[dict[str, str]],
) -> tuple[list[str], list[dict[str, str]]]:
    """The marks MAM attaches visually to the preceding and the next chanted words."""
    preceding = []
    next_marks = []
    for marker in punctuation:
        kind = marker["kind"]
        if kind == "legarmeh":
            preceding.append(marker["glyph"])
        elif kind == "paseq":
            next_marks.append(marker)
        else:
            raise AssertionError(
                f"unclassified MAM punctuation in page data: {marker!r}"
            )
    return preceding, next_marks


def _paired_chanted_word_cell(
    current_form: str,
    next_form: str,
    punctuation: tuple[dict[str, str], ...] | list[dict[str, str]] = (),
) -> tuple:
    """One MAM chanted-word pair, with punctuation placed by MAM's native category."""
    preceding_punctuation, next_punctuation = _native_mam_punctuation_parts(punctuation)
    return (
        *_hebrew_cell(current_form),
        *[part for glyph in preceding_punctuation for part in _hebrew_cell(glyph)],
        " ",
        _next_chanted_word_span(
            next_form,
            next_punctuation,
        ),
    )


def _mam_form(record: dict) -> str:
    """The record's MAM form, from the survey and from nowhere else.

    RENDERING NEVER READS MAM-PRIVATE, so a displayed record with no ``mam_form`` stops the
    render instead of being given a substitute spelling.  The survey lists such records under
    ``diagnostics.records_without_a_mam_form``.  Until 2026-09-10 this module looked a spelling
    up in MAM-private's Phonetic MAM for them, which made a render from the tracked survey
    depend on the private clone whenever such a record was displayed.  CLAUDE.md's section "A
    code path reads MAM-private every time it runs, or never" states the rule that retired it.
    """
    mam_form = record["mam_form"]
    if not mam_form:
        raise psm.SurveyProblem(
            f"{record['bcv']}: a displayed record has no mam_form (listed under the survey's"
            " diagnostics.records_without_a_mam_form); the page does not look one up in"
            " MAM-private"
        )
    return mam_form


def _case_chanted_word_cell(record: dict) -> tuple:
    """The MAM MAS form followed by its next chanted word."""
    # _mam_form first: a record with no MAM form has no next MAM form either, so the
    # assertion below would otherwise fire first and name the wrong cause.
    mam_form = _mam_form(record)
    next_word = record["next_mam_form"]
    assert next_word is not None, f"{record['bcv']}: no next MAM chanted word"
    return _paired_chanted_word_cell(
        mam_form,
        next_word,
        record.get("intervening_mam_punctuation", ()),
    )


def _oleh_chanted_word_cell(record: dict) -> tuple:
    """The oleh context, extending into the next chanted word only for a yored there."""
    current_form = _mam_form(record)
    if ha.MER in current_form:
        return _hebrew_cell(current_form)
    next_word = record["next_mam_form"]
    assert next_word is not None, f"{record['bcv']}: no MAM form after oleh"
    assert ha.MER in next_word, f"{record['bcv']}: no yored after oleh"
    return _paired_chanted_word_cell(
        current_form,
        next_word,
        record.get("intervening_mam_punctuation", ()),
    )


def _case_row(record: dict) -> object:
    subtype = _case_filter_subtype(record)
    attrs = {"data-type": _case_type_code(record["structural_type"])}
    if subtype is not None:
        attrs["data-subtype"] = subtype
    return mb_html.table_row(
        (
            mb_html.table_datum(_ref_link(record["bcv"])),
            mb_html.table_datum(_case_chanted_word_cell(record), _HEBREW_CELL),
            mb_html.table_datum(
                _case_type_cell(record["structural_type"], misc_label=True)
            ),
            mb_html.table_datum(
                subtype
                if subtype is not None
                else _case_subtype_cell(record["subtype"])
            ),
        ),
        attrs,
    )


def _case_type_filter(case_count: int) -> object:
    option_html = "".join(
        f'<option value="{value}">{label}</option>'
        for value, label in _CASE_FILTER_OPTIONS
    )
    return mb_html.raw_html(
        f'<p><label for="{_CASE_TYPE_FILTER_ID}">Show </label>'
        f'<select id="{_CASE_TYPE_FILTER_ID}">{option_html}</select>. '
        f'<output id="{_CASE_SELECTED_COUNT_ID}" aria-live="polite">'
        f"Showing {case_count:,} rows.</output></p>\n"
    )


def _type_2_records(survey: dict) -> list[dict]:
    """The survey's type-2 records, in the corpus's order."""
    return [
        record
        for record in survey["post_stress"]
        if record["structural_type"] == psm.TYPE_GUTTURAL
    ]


def _misc_records(survey: dict) -> list[dict]:
    """The survey's misc records, in the corpus's order."""
    return [
        record
        for record in survey["post_stress"]
        if record["structural_type"] == psm.TYPE_UNCLASSIFIED
    ]


def _type_2_next_group(record: dict) -> str:
    """The detailed type-2 group set by the next chanted word's first consonant."""
    next_word = record["next_mam_form"]
    assert next_word is not None, f"{record['bcv']}: no next MAM chanted word"
    return psm.type_2_next_filter_group(next_word)


def _type_2_filter_group(record: dict) -> str:
    """The coarser type-2 filter group shown on the cases page."""
    detailed_group = _type_2_next_group(record)
    if detailed_group in ("lamed", "guttural"):
        return detailed_group
    return "not-lamed-or-guttural"


def _type_1_subtype_code(record: dict) -> str:
    """The reader-facing subtype code for one structural type-1 record."""
    assert record["structural_type"] == psm.TYPE_OPEN, record
    return _TYPE_1_SUBTYPE_CODES[record["type_1_subtype"]]


def _case_filter_subtype(record: dict) -> str | None:
    """The subtype used by the all-cases page's flat filter list."""
    structural_type = record["structural_type"]
    if structural_type == psm.TYPE_OPEN:
        return _type_1_subtype_code(record)
    if structural_type == psm.TYPE_GUTTURAL:
        return _TYPE_2_SUBTYPE_CODE_BY_FILTER_GROUP[_type_2_filter_group(record)]
    return None


def _lacks_mas_case_row(record: dict) -> object:
    """One MAM chanted-word pair fit for MAS but lacking MAS."""
    fit_type = record["fit_type"]
    return mb_html.table_row(
        (
            mb_html.table_datum(_ref_link(record["bcv"])),
            mb_html.table_datum(_case_chanted_word_cell(record), _HEBREW_CELL),
            mb_html.table_datum(_fit_type_cell(fit_type)),
        ),
        {"data-subtype": fit_type},
    )


def _misc_case_row(record: dict) -> object:
    return mb_html.table_row(
        (
            mb_html.table_datum(_ref_link(record["bcv"])),
            mb_html.table_datum(_case_chanted_word_cell(record), _HEBREW_CELL),
            mb_html.table_datum(_case_subtype_cell(record["subtype"])),
        )
    )


def _lacks_mas_subtype_filter(case_count: int) -> object:
    """The unified lacks-MAS table's subtype filter."""
    option_html = "".join(
        f'<option value="{value}">{label}</option>'
        for value, label in (("all", "All subtypes"), *_LACKS_MAS_FILTER_OPTIONS)
    )
    return mb_html.raw_html(
        f'<p><label for="{_LACKS_MAS_SUBTYPE_FILTER_ID}">Show </label>'
        f'<select id="{_LACKS_MAS_SUBTYPE_FILTER_ID}">{option_html}</select>. '
        f'<output id="{_LACKS_MAS_SELECTED_COUNT_ID}" aria-live="polite">'
        f"Showing {case_count:,} rows.</output></p>\n"
    )


def _not_fit_for_mas_type_filter(case_count: int) -> object:
    """The not-fit-for-MAS table's (sub)type filter."""
    option_html = "".join(
        f'<option value="{value}">{label}</option>'
        for value, label in _NOT_FIT_FILTER_OPTIONS
    )
    return mb_html.raw_html(
        f'<p><label for="{_NOT_FIT_TYPE_FILTER_ID}">Show </label>'
        f'<select id="{_NOT_FIT_TYPE_FILTER_ID}">{option_html}</select>. '
        f'<output id="{_NOT_FIT_SELECTED_COUNT_ID}" aria-live="polite">'
        f"Showing {case_count:,} rows.</output></p>\n"
    )


def _back_to_fit_for_mas_table() -> object:
    """A standard return link for the unified Fit-for-MAS case page."""
    return mb_html.para(
        (
            "← Back to ",
            mb_html.anchor_h(_visible_title(_TITLE), _FNAME),
            " and the ",
            mb_html.anchor_h(
                f"{author.dquote('fit for MAS')} table",
                f"{_FNAME}#{_FIT_FOR_MAS_SECTION_ID}",
            ),
            ".",
        )
    )


def build_lacks_mas_body(survey: dict) -> list:
    """Every chanted-word pair fit for MAS but lacking MAS, filterable by subtype."""
    records = _lacks_mas_records(survey)
    return [
        mb_html.heading_level_1(_visible_title(_LACKS_MAS_TITLE)),
        _hebrew_spacing_option(),
        _back_to_fit_for_mas_table(),
        mb_html.heading_level_2("Every case fit for MAS that lacks MAS"),
        _para(f"The table lists all {len(records):,} cases fit for MAS that lack MAS."),
        _lacks_mas_subtype_filter(len(records)),
        _table(
            ("Verse", "Word", "Subtype"),
            [_lacks_mas_case_row(record) for record in records],
            {
                "class": f"accent-pair-table post-stress-meteg-table {_CASE_TABLE_CLASS}",
                "id": _LACKS_MAS_TABLE_ID,
            },
        ),
        mb_html.raw_html(_LACKS_MAS_FILTER_SCRIPT),
    ]


def _not_fit_for_mas_criterion_cell(meets_criterion: bool, criterion: str) -> object:
    """A blank cell for a met criterion or a column-specific red-cross gloss."""
    return (
        ""
        if meets_criterion
        else mb_html.span(
            _RED_X,
            {
                "class": _NOT_FIT_FAILURE_CLASS,
                "title": f"does not meet: {criterion}",
            },
        )
    )


def _not_fit_for_mas_type_codes(record: dict) -> tuple[str, ...]:
    """Every (sub)type that makes one not-fit-for-MAS chanted word selectable."""
    structural_types = record["types"]
    codes = []
    if psm.TYPE_OPEN in structural_types:
        codes.extend(("1", _TYPE_1_SUBTYPE_CODES[record["type_1_subtype"]]))
    if psm.TYPE_GUTTURAL in structural_types:
        codes.extend(
            (
                "2",
                _TYPE_2_SUBTYPE_CODE_BY_FILTER_GROUP[_type_2_filter_group(record)],
            )
        )
    if psm.TYPE_CLOSED_TSERE in structural_types:
        codes.append("3")
    if not codes:
        codes.append("other")
    assert set(structural_types) <= set(_TYPE_CODES), record
    return tuple(codes)


def _not_fit_for_mas_case_row(record: dict) -> object:
    """One MAS chanted word, with a result for each Fit-for-MAS criterion."""
    return mb_html.table_row(
        (
            mb_html.table_datum(_ref_link(record["bcv"])),
            mb_html.table_datum(_case_chanted_word_cell(record), _HEBREW_CELL),
            mb_html.table_datum(
                _not_fit_for_mas_criterion_cell(
                    record["meets_first_fit_for_mas_criterion"],
                    _FIT_FOR_MAS_CRITERIA[0],
                ),
                {"class": "centered"},
            ),
            mb_html.table_datum(
                _not_fit_for_mas_criterion_cell(
                    record["meets_second_fit_for_mas_criterion"],
                    _FIT_FOR_MAS_CRITERIA[1],
                ),
                {"class": "centered"},
            ),
            mb_html.table_datum(
                _not_fit_for_mas_criterion_cell(
                    record["meets_third_fit_for_mas_criterion"],
                    _FIT_FOR_MAS_CRITERIA[2],
                ),
                {"class": "centered"},
            ),
        ),
        {"data-type-codes": " ".join(_not_fit_for_mas_type_codes(record))},
    )


def build_not_fit_body(survey: dict) -> list:
    """Every MAS chanted word that is not fit for MAS, with each failed criterion marked."""
    records = _not_fit_for_mas_records(survey)
    criterion_headers = tuple(
        mb_html.abbr(str(number), {"title": criterion})
        for number, criterion in enumerate(_FIT_FOR_MAS_CRITERIA, start=1)
    )
    return [
        mb_html.heading_level_1(_visible_title(_NOT_FIT_TITLE)),
        _hebrew_spacing_option(),
        _back_to_fit_for_mas_table(),
        mb_html.heading_level_2("Every MAS case not fit for MAS"),
        _para(
            f"The table lists all {len(records):,} MAS cases that are not fit for MAS."
        ),
        _para(
            f"The columns headed 1–3 correspond to the three {author.dquote('fit for MAS')}"
            " criteria. A red"
            f" {_RED_X} marks each criterion that a word does not meet; blank cells mark"
            " criteria that the word meets."
        ),
        _not_fit_for_mas_type_filter(len(records)),
        _table(
            ("Verse", "Word", *criterion_headers),
            [_not_fit_for_mas_case_row(record) for record in records],
            {
                "class": f"accent-pair-table post-stress-meteg-table {_CASE_TABLE_CLASS}",
                "id": _NOT_FIT_TABLE_ID,
            },
        ),
        mb_html.raw_html(_NOT_FIT_FILTER_SCRIPT),
    ]


def build_misc_body(survey: dict) -> list:
    """The misc cases and the named subsets that remain outside types 1–3."""
    records = _misc_records(survey)
    unnamed_misc = [record for record in records if record["subtype"] is None]
    assert len(unnamed_misc) == 2, unnamed_misc
    misc_almost_type_3_count = _by_subtype_count(survey, psm.SUBTYPE_MISC_ALMOST_TYPE_3)
    misc_almost_type_3_only_member = _misc_almost_type_3_only_member(survey)
    vayomer_count = _by_subtype_count(survey, psm.SUBTYPE_MISC_VAYOMER)
    return [
        mb_html.heading_level_1(_visible_title(_MISC_TITLE)),
        _hebrew_spacing_option(),
        mb_html.para(
            (
                "← Back to ",
                mb_html.anchor_h(_visible_title(_TITLE), _FNAME),
                " or the ",
                mb_html.anchor_h(
                    f"{len(survey['post_stress']):,} individual cases", _CASES_FNAME
                ),
                ".",
            )
        ),
        mb_html.heading_level_2("Every misc case in MAM"),
        _para(
            "Each word in the table has MAS but does not meet the definition of"
            " types 1, 2, or 3."
        ),
        _table(
            ("Verse", "Word", "Subtype"),
            [_misc_case_row(record) for record in records],
            {
                "class": f"accent-pair-table post-stress-meteg-table {_CASE_TABLE_CLASS}",
                "id": _MISC_TABLE_ID,
            },
        ),
        mb_html.para(
            (
                "Within misc, ",
                psm.SUBTYPE_MISC_ALMOST_TYPE_3,
                f" has {_spelled(misc_almost_type_3_count)} word",
                "s" if misc_almost_type_3_count != 1 else "",
                ", at ",
                _ref_link(misc_almost_type_3_only_member["bcv"]),
                ": ",
                *_case_chanted_word_cell(misc_almost_type_3_only_member),
                ", whose MAS syllable is final and closed with ",
                _ROM_HOLAM,
                ", a long vowel. That syllable fits ",
                cos(),
                "'s long-vowel type (a), but not our type 3, which is restricted to ",
                _ROM_TSERE,
                ".",
            )
        ),
        mb_html.para(
            (
                "Within misc, misc-",
                _ROM_VAYOMER,
                f" has {_spelled(vayomer_count)} word",
                "s" if vayomer_count != 1 else "",
                ". Each has a ",
                _ROM_PASEQ,
                " between the MAS word and the next word. This is the ",
                _ROM_GAYA,
                "-before-",
                _ROM_PASEQ,
                " pattern described in ",
                itm(),
                " ",
                *itm_sections("§325"),
                ".",
            )
        ),
        mb_html.para(
            (
                "The remaining ",
                _spelled(len(unnamed_misc)),
                " misc cases, at ",
                _ref_link(unnamed_misc[0]["bcv"]),
                " and ",
                _ref_link(unnamed_misc[1]["bcv"]),
                ", belong to no named subset. There is not much to say about them beyond their having MAS without meeting the definition of type 1, 2, or 3.",
            )
        ),
    ]


def build_cases_body(survey: dict) -> list:
    """The individual cases, outside the main page's explanatory sections."""
    headers = ("Verse", "Word", "Type", "Subtype")
    rows = [_case_row(record) for record in survey["post_stress"]]
    return [
        mb_html.heading_level_1(_visible_title(_CASES_TITLE)),
        _hebrew_spacing_option(),
        mb_html.para(
            ("← Back to ", mb_html.anchor_h(_visible_title(_TITLE), _FNAME), ".")
        ),
        mb_html.heading_level_2("Every MAS in MAM"),
        _case_type_filter(len(rows)),
        _table(
            headers,
            rows,
            {
                "class": f"accent-pair-table post-stress-meteg-table {_CASE_TABLE_CLASS}",
                "id": _CASE_TABLE_ID,
            },
        ),
        mb_html.raw_html(_CASE_FILTER_SCRIPT),
    ]
