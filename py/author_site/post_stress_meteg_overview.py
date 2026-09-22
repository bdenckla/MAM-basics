"""Main explanatory sections for the post-stress-meteg pages."""

from __future__ import annotations


from accgram import post_stress_meteg as psm
from mb_author import author
from mb_misc import mb_html

from author_site.post_stress_meteg_shared import (
    _CASES_FNAME,
    _COS_CH_14_BY_TYPE,
    _COS_CH_14_PAGES_BY_TYPE,
    _COS_CH_8_PAGE_GLOSS,
    _COS_PAGE_STARTS_BY_TYPE,
    _HEBREW_CELL,
    _JEREMIAH_FOOTNOTE_ID,
    _MAS_CENSUS_GLOSS,
    _MBS_O_CENSUS_GLOSS,
    _METHODS_FNAME,
    _MISC_FNAME,
    _NEXT_CONJUNCTIVE_FOOTNOTE_ID,
    _NONFINAL_MAS_FOOTNOTE_ID,
    _NUMERIC_CELL,
    _PASHTA_STRESS_HELPER_FOOTNOTE_ID,
    _POETIC,
    _POST_SILLUQ_FOOTNOTE_ID,
    _PROSE,
    _ROM_MAQAF,
    _ROM_METEG,
    _ROM_PASHTA,
    _ROM_SHEWA,
    _ROM_TSERE,
    _SOURCES_FOR_TYPES_FOOTNOTE_ID,
    _TYPE_2_SUBTYPE_SPECS,
    _TYPE_2_TYPE_3_FOOTNOTE_ID,
    _TYPE_SOURCES,
    _VOCAL_SHEWA_FOOTNOTE_ID,
    _footnote_callout,
    _ref_link,
    _singleton_example_table,
    _spelled,
    _table,
    cos,
    itm,
    itm_sections,
)

from author_site.post_stress_meteg_survey import (
    _actual_type_1_mas,
    _both,
    _by_type_count,
    _count,
    _example_of,
    _next_conjunctive_records,
    _nonfinal_mas_syllable_records,
    _noninitial_next_stress_records,
)

from author_site.post_stress_meteg_cases import (
    _case_chanted_word_cell,
    _case_type_cell,
    _structural_subtype_cell,
    _type_2_filter_group,
    _type_2_records,
)

# --- the sections --------------------------------------------------------------


def _opening(survey: dict) -> list:
    """Section 1: what is counted, and where the silluq boundary falls."""
    total = _both(survey, "meteg after the stressed syllable")
    example = _example_of(survey, psm.TYPE_OPEN)
    return [
        mb_html.para(
            (
                "A ",
                _ROM_METEG,
                " almost always comes before the stressed syllable of its word, but it can"
                " also come after the stress. MAM has ",
                f"{total:,} cases of ",
                _ROM_METEG,
                " after the stress (MAS). For example:",
            )
        ),
        _singleton_example_table(example["bcv"], _case_chanted_word_cell(example)),
        mb_html.para(
            (
                "In this document, by "
                f"{author.dquote('word')} we mean either a simple word (having just one"
                " atom) or a compound word (having two or more atoms"
                " connected by ",
                _ROM_MAQAF,
                " marks). By "
                f"{author.dquote('atom')} we mean a sequence of pointed letters uninterrupted by"
                " space, ",
                _ROM_MAQAF,
                ", or any other punctuation.",
            )
        ),
    ]


def _census(survey: dict) -> list:
    """Section 2: the counts, prose verses beside poetic verses."""
    census_chanted_word_summary = survey["census_chanted_word_summary"]
    headers = (
        mb_html.abbr("cant-sys", {"title": "cantillation system"}),
        mb_html.abbr("words", {"title": "count of words"}),
        mb_html.abbr(
            "MBS_O",
            {"title": _MBS_O_CENSUS_GLOSS},
        ),
        mb_html.abbr(
            "MAS",
            {"title": _MAS_CENSUS_GLOSS},
        ),
        mb_html.abbr(
            "% MAS",
            {"title": "MAS/(MAS+MBS_O)"},
        ),
    )
    numeric = (None, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL)
    labels = {_PROSE: "prose", _POETIC: "poetic"}
    counts_by_system = {
        system: {
            "chanted_words": _count(survey, system, "chanted words checked"),
            **census_chanted_word_summary["by_system"][system],
        }
        for system in (_PROSE, _POETIC)
    }
    all_counts = {
        category: sum(counts[category] for counts in counts_by_system.values())
        for category in ("chanted_words", "mbs_only", "mas")
    }

    def row(label: str, counts: dict[str, int]) -> object:
        mbs_only = counts["mbs_only"]
        mas = counts["mas"]
        return mb_html.table_row_of_data(
            (
                label,
                f"{counts['chanted_words']:,}",
                f"{mbs_only:,}",
                f"{mas:,}",
                f"{mas / (mbs_only + mas):.1%}",
            ),
            numeric,
        )

    rows = [
        row(labels[system], counts_by_system[system]) for system in (_PROSE, _POETIC)
    ]
    rows.append(row("all", all_counts))
    mbs_only = all_counts["mbs_only"]
    mas = all_counts["mas"]
    return [
        mb_html.heading_level_2("MAS census by cantillation system"),
        _table(headers, rows),
        mb_html.para(
            (
                "So, among words with at least one ",
                _ROM_METEG,
                " mark, there are ",
                f"{mas:,}",
                " words where one of the ",
                _ROM_METEG,
                " marks is after the stress and ",
                f"{mbs_only:,}",
                " words where none of the ",
                _ROM_METEG,
                " marks is after the stress. (There is never more than one ",
                _ROM_METEG,
                " mark after the stress.) See the ",
                mb_html.anchor_h("Methods", _METHODS_FNAME),
                " page for more details.",
            )
        ),
    ]


def _census_definitions(survey: dict) -> list:
    """The chanted-word definitions that govern the main census table."""
    census_chanted_word_summary = survey["census_chanted_word_summary"]
    multiple_mbs = census_chanted_word_summary[
        "mbs_only_chanted_words_with_multiple_mbs"
    ]
    more_than_two_mbs = census_chanted_word_summary[
        "mbs_only_chanted_words_with_more_than_two_mbs"
    ]
    assert more_than_two_mbs == 0
    records = census_chanted_word_summary["mas_chanted_words_with_mbs"]
    # The (sub)type column shows the structural taxonomy, so the label comes off the
    # post-stress record; the census section makes no Fit-for-MAS claim.
    post_stress_by_bcv_and_mam_form = {
        (one["bcv"], one["mam_form"]): one for one in survey["post_stress"]
    }
    assert len(post_stress_by_bcv_and_mam_form) == len(survey["post_stress"])
    assert {(record["bcv"], record["mam_form"]) for record in records} <= set(
        post_stress_by_bcv_and_mam_form
    )
    return [
        mb_html.heading_level_2("Census definitions"),
        mb_html.para(
            (
                mb_html.abbr("MBS_O", {"title": _MBS_O_CENSUS_GLOSS}),
                " counts words that have one or more ",
                _ROM_METEG,
                " marks before the"
                f" stress and none after it. The {author.dquote('O')} means"
                f" {author.dquote('only')}. ",
                mb_html.abbr("MAS", {"title": _MAS_CENSUS_GLOSS}),
                " counts words that have one or more ",
                _ROM_METEG,
                " marks after the stress, whether the word has zero or more ",
                _ROM_METEG,
                " marks before the stress.",
            )
        ),
        mb_html.para(
            "The % MAS column is the MAS count divided by the sum of the MBS_O and MAS counts.",
        ),
        mb_html.para(
            (
                f"{multiple_mbs:,} MBS_O words have more than one ",
                _ROM_METEG,
                " mark. Every such MBS_O word has exactly two ",
                _ROM_METEG,
                " marks.",
            )
        ),
        mb_html.para(
            (
                "No MAS word has more than one ",
                _ROM_METEG,
                " mark after the stress: every MAS word has exactly one ",
                _ROM_METEG,
                " mark after the stress.",
            ),
        ),
        mb_html.para(
            (
                f"There are {_spelled(len(records))} MAS words that also have one ",
                _ROM_METEG,
                " mark before the stress. They are listed below. (There are no MAS words with more than one ",
                _ROM_METEG,
                " before the stress.)",
            ),
        ),
        _table(
            ("", "", "(sub)types"),
            [
                mb_html.table_row_of_data(
                    (
                        _ref_link(record["bcv"]),
                        _case_chanted_word_cell(
                            post_stress_by_bcv_and_mam_form[
                                (record["bcv"], record["mam_form"])
                            ]
                        ),
                        _structural_subtype_cell(
                            post_stress_by_bcv_and_mam_form[
                                (record["bcv"], record["mam_form"])
                            ]
                        ),
                    ),
                    (None, _HEBREW_CELL, None),
                )
                for record in records
            ],
        ),
    ]


def _mas_facts(survey: dict) -> list:
    """Section 3: the facts shared by every MAS, before structural classification."""
    exceptions = _noninitial_next_stress_records(survey)
    assert len(exceptions) == 1
    nonfinal_mas_syllable_records = _nonfinal_mas_syllable_records(survey)
    assert len(nonfinal_mas_syllable_records) == 4
    next_conjunctive = _next_conjunctive_records(survey)
    total = len(survey["post_stress"])
    assert (
        len(next_conjunctive)
        + sum(
            record["next_chanted_word_accent_classification"] == "disjunctive"
            for record in survey["post_stress"]
        )
        == total
    )
    return [
        mb_html.heading_level_2("Facts about MAS"),
        mb_html.unordered_list(
            (
                (
                    "In every MAS case, the stressed syllable has a conjunctive accent (",
                    _footnote_callout(1, _POST_SILLUQ_FOOTNOTE_ID),
                    ").",
                ),
                "In every MAS case, the MAS syllable comes right after the stressed syllable.",
                (
                    "In every MAS case except four (",
                    _footnote_callout(2, _NONFINAL_MAS_FOOTNOTE_ID),
                    "), the MAS syllable is final.",
                ),
                (
                    "In every MAS case but one (",
                    _footnote_callout(3, _JEREMIAH_FOOTNOTE_ID),
                    "), the next word has initial stress.",
                ),
                (
                    f"In {(total - len(next_conjunctive)) / total:.1%} of MAS cases (",
                    _footnote_callout(4, _NEXT_CONJUNCTIVE_FOOTNOTE_ID),
                    "), the next word has a disjunctive accent.",
                ),
            )
        ),
    ]


def _by_type(survey: dict) -> list:
    """Section 4: the three types the two books describe, and what is left over."""
    headers = (
        "Type",
        "Prose",
        "Poetic",
        "All",
        "Example",
    )
    unclassified = psm.TYPE_UNCLASSIFIED
    unclassified_count = _by_type_count(survey, unclassified)
    rows = []
    for kind, (yeivin, breuer) in _TYPE_SOURCES.items():
        example = _example_of(survey, kind)
        rows.append(
            mb_html.table_row_of_data(
                (
                    _case_type_cell(kind),
                    str(survey["post_stress_by_structural_type"][_PROSE][kind]),
                    str(survey["post_stress_by_structural_type"][_POETIC][kind]),
                    str(_by_type_count(survey, kind)),
                    _case_chanted_word_cell(example),
                ),
                (
                    None,
                    _NUMERIC_CELL,
                    _NUMERIC_CELL,
                    _NUMERIC_CELL,
                    _HEBREW_CELL,
                ),
            )
        )
    rows.append(
        mb_html.table_row_of_data(
            (
                "misc",
                str(survey["post_stress_by_structural_type"][_PROSE][unclassified]),
                str(survey["post_stress_by_structural_type"][_POETIC][unclassified]),
                str(unclassified_count),
                _case_chanted_word_cell(_example_of(survey, unclassified)),
            ),
            (
                None,
                _NUMERIC_CELL,
                _NUMERIC_CELL,
                _NUMERIC_CELL,
                _HEBREW_CELL,
            ),
        )
    )
    all_prose_count = sum(survey["post_stress_by_structural_type"][_PROSE].values())
    all_poetic_count = sum(survey["post_stress_by_structural_type"][_POETIC].values())
    all_count = all_prose_count + all_poetic_count
    assert all_count == len(survey["post_stress"])
    rows.append(
        mb_html.table_row_of_data(
            (
                mb_html.abbr("all", {"title": "All cases: types 1, 2, 3, and misc."}),
                str(all_prose_count),
                str(all_poetic_count),
                str(all_count),
                "",
            ),
            (None, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL, _HEBREW_CELL),
        )
    )
    return [
        mb_html.heading_level_2("The three types of MAS"),
        mb_html.para(
            (
                f"All but {unclassified_count} cases of MAS can be sorted into one of the three"
                " following types: (",
                _footnote_callout(5, _SOURCES_FOR_TYPES_FOOTNOTE_ID),
                ")",
            )
        ),
        mb_html.ordered_list(
            (
                "The MAS syllable is open and final.",
                "The MAS word is closed by a guttural.",
                (
                    "The MAS syllable is closed, final, and ",
                    _ROM_TSERE,
                    "-voweled. (",
                    _footnote_callout(6, _TYPE_2_TYPE_3_FOOTNOTE_ID),
                    ")",
                ),
            )
        ),
        _table(headers, rows),
    ]


def _sources_for_types_footnote() -> list:
    """Footnote 5: sources for the three types."""
    source_rows = [
        mb_html.table_row_of_data(
            (
                _case_type_cell(kind),
                itm_sections(yeivin),
                breuer,
                _COS_CH_14_BY_TYPE[kind],
            ),
            (None, None, None, None),
        )
        for kind, (yeivin, breuer) in _TYPE_SOURCES.items()
    ]
    cos_page_rows = [
        mb_html.table_row_of_data(
            (
                _case_type_cell(kind),
                _COS_PAGE_STARTS_BY_TYPE[kind],
                _COS_CH_14_PAGES_BY_TYPE[kind],
            ),
            (None, None, None),
        )
        for kind in _TYPE_SOURCES
    ]
    return [
        mb_html.heading_level_3(
            "φ5 — Sources for types 1–3", {"id": _SOURCES_FOR_TYPES_FOOTNOTE_ID}
        ),
        mb_html.para(
            (
                "The three types of MAS are described in both ",
                itm(),
                " and ",
                cos(),
                ". Exactly what words are included in and excluded from these three types"
                " varies among ITM, CoS, and our document here, but they broadly agree.",
            )
        ),
        _table(
            (
                "Type",
                itm(),
                (cos(), " Ch. 8"),
                (cos(), " Ch. 14 §8"),
            ),
            source_rows,
        ),
        mb_html.para(
            (
                "For those using the Wengrov translation of ",
                cos(),
                ", below is a table of the page numbers corresponding to the section"
                " identifiers in the table above:",
            )
        ),
        _table(
            (
                "Type",
                mb_html.abbr("CoS Ch. 8 pg", {"title": _COS_CH_8_PAGE_GLOSS}),
                mb_html.abbr(
                    "CoS Ch. 14 §8 pg",
                    {
                        "title": (
                            "printed page in Wengrov's English translation of CoS on which"
                            " the cited Ch. 14 §8 item begins"
                        )
                    },
                ),
            ),
            cos_page_rows,
        ),
    ]


def _case_list_link(survey: dict) -> list:
    """The main page's link to the long list of individual cases."""
    misc_count = _by_type_count(survey, psm.TYPE_UNCLASSIFIED)
    return [
        mb_html.para(
            (
                "The ",
                mb_html.anchor_h(
                    f"{len(survey['post_stress']):,} individual cases", _CASES_FNAME
                ),
                " are listed separately and can be filtered by (sub)type. The ",
                mb_html.anchor_h(f"{misc_count:,} misc cases", _MISC_FNAME),
                " appear in that large list, but are also further discussed on a page of"
                " their own.",
            )
        )
    ]


def _type_2_facts(survey: dict) -> list:
    """The type-2 subtype section."""
    return _type_2_subtypes(survey)


def _type_1_example(survey: dict, example_key: dict) -> dict:
    """The MAM-backed post-stress record identified by a type-1 summary example key."""
    matches = [
        record
        for record in survey["post_stress"]
        if all(record[key] == value for key, value in example_key.items())
    ]
    assert len(matches) == 1, (example_key, matches)
    return matches[0]


def _type_1_subtypes(survey: dict) -> list:
    """The complete structural type-1 MAS population by next-chanted-word-stress subtype."""
    type_1_mas = _actual_type_1_mas(survey)
    pattern_counts = type_1_mas["by_initial_stress_pattern"]
    example_keys = type_1_mas["example_keys_by_initial_stress_pattern"]
    headers = (
        "Subtype",
        "Prose",
        "Poetic",
        "All",
        "Example",
    )
    labels = {
        psm.TYPE_1_SUBTYPE_A: "1A",
        psm.TYPE_1_SUBTYPE_B: "1B",
        psm.TYPE_1_SUBTYPE_C: "1C",
        "not_initially_stressed": "1D",
    }
    rows = [
        mb_html.table_row_of_data(
            (
                labels[pattern],
                str(counts["by_system"][_PROSE]),
                str(counts["by_system"][_POETIC]),
                str(counts["cases"]),
                _case_chanted_word_cell(_type_1_example(survey, example_keys[pattern])),
            ),
            (None, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL, _HEBREW_CELL),
        )
        for pattern, counts in pattern_counts.items()
    ]
    total = sum(counts["cases"] for counts in pattern_counts.values())
    assert total == type_1_mas["cases"]
    return [
        mb_html.heading_level_2("The four subtypes of MAS type 1"),
        mb_html.para(
            "Based on properties of the next word, all cases of MAS type 1 can be sorted"
            " into one of the four following subtypes:"
        ),
        mb_html.unordered_list(
            (
                (
                    "1A: The next word has initial stress and an initial vocal ",
                    _ROM_SHEWA,
                    ". (",
                    _footnote_callout(7, _VOCAL_SHEWA_FOOTNOTE_ID),
                    ")",
                ),
                (
                    "1B: The next word has a ",
                    _ROM_PASHTA,
                    " stress helper on its first letter. (",
                    _footnote_callout(8, _PASHTA_STRESS_HELPER_FOOTNOTE_ID),
                    ")",
                ),
                ("1C: Like 1B, but with some accent other than ", _ROM_PASHTA, "."),
                "1D: The next word does not have initial stress.",
            )
        ),
        _table(headers, rows),
    ]


def _type_2_subtypes(survey: dict) -> list:
    """The complete structural type-2 MAS population by next-chanted-word initial consonant."""
    records_by_group = {
        group: [] for group, _code, _description in _TYPE_2_SUBTYPE_SPECS
    }
    for record in _type_2_records(survey):
        records_by_group[_type_2_filter_group(record)].append(record)
    rows = []
    for group, code, _description in _TYPE_2_SUBTYPE_SPECS:
        records = records_by_group[group]
        assert records, group
        rows.append(
            mb_html.table_row_of_data(
                (
                    code,
                    str(sum(record["system"] == _PROSE for record in records)),
                    str(sum(record["system"] == _POETIC for record in records)),
                    str(len(records)),
                    _case_chanted_word_cell(records[0]),
                ),
                (None, _NUMERIC_CELL, _NUMERIC_CELL, _NUMERIC_CELL, _HEBREW_CELL),
            )
        )
    total = sum(len(records) for records in records_by_group.values())
    assert total == _by_type_count(survey, psm.TYPE_GUTTURAL)
    return [
        mb_html.heading_level_2("The three subtypes of MAS type 2"),
        mb_html.para(
            "Based on properties of the next word, all cases of MAS type 2 can be sorted"
            " into one of the three following subtypes:"
        ),
        mb_html.unordered_list(
            tuple(description for _group, _code, description in _TYPE_2_SUBTYPE_SPECS)
        ),
        _table(("Subtype", "Prose", "Poetic", "All", "Example"), rows),
    ]
