"""Consistency and claim checks for the post-stress-meteg pages."""

from __future__ import annotations

from collections import Counter

from accgram import final_stress
from accgram import post_stress_meteg_model as psm

from author_site.post_stress_meteg_shared import (
    _CHRONICLES_8_11_VERSE,
    _EXCERPTS,
    _MAM_POST_SILLUQ_VERSE,
    _MAX_WORDS_IN_ALL_EXCERPTS,
    _MAX_WORDS_PER_EXCERPT,
    _POETIC,
    _POST_SILLUQ_VERSE,
    _PROSE,
    _TYPE_2_SUBTYPE_SPECS,
    _TYPE_SOURCES,
    _split,
)

from author_site.post_stress_meteg_survey import (
    _actual_type_1_mas,
    _both,
    _by_subtype_count,
    _by_type_count,
    _dual_cantillation,
    _dual_cantillation_facts,
    _example_of,
    _fit_for_mas,
    _lacks_mas_records,
    _misc_almost_type_3_only_member,
    _nonfinal_mas_syllable_records,
    _noninitial_next_stress_records,
    _not_fit_for_mas_records,
    _subtype_records,
    _type_2_type_3_overlap,
)

from author_site.post_stress_meteg_cases import (
    _misc_records,
    _type_2_filter_group,
    _type_2_records,
)

from author_site.post_stress_meteg_post_silluq_data import (
    _post_silluq_comparison,
)


def _assert_exact_keys(mapping: dict, expected_keys: set[str], label: str) -> None:
    """Require a summary mapping to name every category and no unknown category."""
    actual_keys = set(mapping)
    assert actual_keys == expected_keys, (label, actual_keys, expected_keys)


def pin_claims(survey: dict) -> None:
    """Validate the survey and every categorical or relational statement in the prose."""
    _check_survey_consistency(survey)
    _pin_prose_claims(survey)


def _check_survey_consistency(survey: dict) -> None:
    """Reconcile computed summaries without freezing their current populations."""
    systems = {_PROSE, _POETIC}
    count_categories = {
        "chanted words checked",
        "meteg before the stressed syllable",
        "meteg in the stressed syllable, no sof pasuq",
        "meteg after the stressed syllable",
        "silluq",
        "meteg sharing a letter with a non-stress-marking accent",
    }
    counts = survey["counts"]
    _assert_exact_keys(counts, systems, "count systems")
    for system in systems:
        _assert_exact_keys(
            counts[system], count_categories, f"{system} count categories"
        )

    post_stress = survey["post_stress"]
    assert len(post_stress) == _both(
        survey, "meteg after the stressed syllable"
    ), "the post-stress records and the post-stress count disagree"
    assert all(record["system"] in systems for record in post_stress)

    census = survey["census_chanted_word_summary"]
    _assert_exact_keys(census["by_system"], systems, "census systems")
    for system in systems:
        system_census = census["by_system"][system]
        _assert_exact_keys(system_census, {"mbs_only", "mas"}, f"{system} census")
        mas_records = sum(record["system"] == system for record in post_stress)
        assert system_census["mas"] == mas_records
    assert (
        census["mbs_only_chanted_words_with_more_than_two_mbs"]
        <= census["mbs_only_chanted_words_with_multiple_mbs"]
    )

    qamats = survey["qamats_variant_census"]
    _assert_exact_keys(qamats["by_system"], systems, "qamats-variant systems")
    grouping_entry_differences = Counter()
    for record in qamats["distinct_phonetic_groupings"]:
        assert record["system"] in systems
        grouping_entry_differences[record["system"]] += len(record["qamats-sam"]) - len(
            record["qamats-dal"]
        )
    qamats_categories = {
        "source_entries",
        "variant_rows",
        "duplicate_phonetic_reading_entries",
        "mam_chanted_words_counted",
    }
    for system in systems:
        system_qamats = qamats["by_system"][system]
        _assert_exact_keys(
            system_qamats, qamats_categories, f"{system} qamats-variant census"
        )
        assert system_qamats["source_entries"] == (
            system_qamats["mam_chanted_words_counted"]
            + system_qamats["duplicate_phonetic_reading_entries"]
        )
        assert system_qamats["duplicate_phonetic_reading_entries"] == (
            system_qamats["variant_rows"] + grouping_entry_differences[system]
        )
        assert (
            system_qamats["mam_chanted_words_counted"]
            == counts[system]["chanted words checked"]
        )

    structural_types = {*_TYPE_SOURCES, psm.TYPE_UNCLASSIFIED}
    by_type = survey["post_stress_by_structural_type"]
    _assert_exact_keys(by_type, systems, "structural-type systems")
    for system in systems:
        _assert_exact_keys(
            by_type[system], structural_types, f"{system} structural types"
        )
    assert Counter(
        (record["system"], record["structural_type"]) for record in post_stress
    ) == Counter(
        {
            (system, kind): by_type[system][kind]
            for system in systems
            for kind in structural_types
        }
    )

    subtypes = {psm.SUBTYPE_MISC_VAYOMER, psm.SUBTYPE_MISC_ALMOST_TYPE_3}
    by_subtype = survey["post_stress_by_subtype"]
    _assert_exact_keys(by_subtype, systems, "subtype systems")
    for system in systems:
        _assert_exact_keys(by_subtype[system], subtypes, f"{system} subtypes")
    assert Counter(
        (record["system"], record["subtype"])
        for record in post_stress
        if record["subtype"] is not None
    ) == Counter(
        {
            (system, subtype): by_subtype[system][subtype]
            for system in systems
            for subtype in subtypes
        }
    )

    actual_type_1_mas = _actual_type_1_mas(survey)
    type_1_patterns = {
        psm.TYPE_1_SUBTYPE_A,
        psm.TYPE_1_SUBTYPE_B,
        psm.TYPE_1_SUBTYPE_C,
        "not_initially_stressed",
    }
    pattern_counts = actual_type_1_mas["by_initial_stress_pattern"]
    _assert_exact_keys(pattern_counts, type_1_patterns, "type-1 patterns")
    for pattern, pattern_count in pattern_counts.items():
        _assert_exact_keys(
            pattern_count, {"cases", "by_system"}, f"type-1 pattern {pattern}"
        )
        _assert_exact_keys(
            pattern_count["by_system"], systems, f"type-1 pattern {pattern} systems"
        )
        assert pattern_count["cases"] == sum(pattern_count["by_system"].values())
        assert pattern_count["cases"] > 0
    assert actual_type_1_mas["cases"] == sum(
        pattern_count["cases"] for pattern_count in pattern_counts.values()
    )
    assert actual_type_1_mas["cases"] == _by_type_count(survey, psm.TYPE_OPEN)
    example_keys = actual_type_1_mas["example_keys_by_initial_stress_pattern"]
    _assert_exact_keys(example_keys, type_1_patterns, "type-1 example patterns")
    assert all(
        set(example_key) == {"bcv", "chanted_word", "jta"}
        for example_key in example_keys.values()
    )

    fit_for_mas = _fit_for_mas(survey)
    type_1_subtypes = {
        psm.TYPE_1_SUBTYPE_A,
        psm.TYPE_1_SUBTYPE_B,
        psm.TYPE_1_SUBTYPE_C,
    }
    _assert_exact_keys(
        fit_for_mas["by_type_1_subtype"], type_1_subtypes, "fit type-1 subtypes"
    )
    for subtype, counts_by_subtype in fit_for_mas["by_type_1_subtype"].items():
        _assert_exact_keys(
            counts_by_subtype,
            {"candidates", "with_mas", "without_mas", "with_mas_by_system"},
            f"fit type-1 subtype {subtype}",
        )
        _assert_exact_keys(
            counts_by_subtype["with_mas_by_system"],
            systems,
            f"fit type-1 subtype {subtype} systems",
        )
        assert counts_by_subtype["candidates"] == (
            counts_by_subtype["with_mas"] + counts_by_subtype["without_mas"]
        )
        assert counts_by_subtype["with_mas"] == sum(
            counts_by_subtype["with_mas_by_system"].values()
        )

    fit_types = {
        psm.FIT_TYPE_1_A,
        psm.FIT_TYPE_1_B,
        psm.FIT_TYPE_2_AF,
        psm.FIT_TYPE_2_BF,
        psm.FIT_TYPE_3,
    }
    by_fit_type = fit_for_mas["by_fit_type"]
    _assert_exact_keys(by_fit_type, fit_types, "fit types")
    for fit_type, fit_counts in by_fit_type.items():
        _assert_exact_keys(
            fit_counts,
            {"candidates", "with_mas", "without_mas"},
            f"fit type {fit_type}",
        )
        assert fit_counts["candidates"] == (
            fit_counts["with_mas"] + fit_counts["without_mas"]
        )
    assert fit_for_mas["fitting_any_type"] == sum(
        fit_counts["candidates"] for fit_counts in by_fit_type.values()
    )
    assert fit_for_mas["with_mas"] == sum(
        fit_counts["with_mas"] for fit_counts in by_fit_type.values()
    )
    assert fit_for_mas["without_mas"] == sum(
        fit_counts["without_mas"] for fit_counts in by_fit_type.values()
    )
    assert (
        fit_for_mas["with_mas"] + fit_for_mas["without_mas"]
        == fit_for_mas["fitting_any_type"]
    )
    assert (
        fit_for_mas["candidate_chanted_words"]
        >= fit_for_mas["non_type_specific_conditions"]
        >= fit_for_mas["fitting_any_type"]
    )
    assert (
        sum(fit_for_mas["accent_grammar_token_counts"].values())
        == fit_for_mas["candidate_chanted_words"]
    )

    fitting_records = fit_for_mas["records"]
    assert len(fitting_records) == fit_for_mas["fitting_any_type"]
    expected_fit_record_counts = Counter()
    for fit_type, fit_counts in by_fit_type.items():
        expected_fit_record_counts[(fit_type, True)] = fit_counts["with_mas"]
        expected_fit_record_counts[(fit_type, False)] = fit_counts["without_mas"]
    assert (
        Counter((record["fit_type"], record["has_mas"]) for record in fitting_records)
        == expected_fit_record_counts
    )
    assert len(_lacks_mas_records(survey)) == fit_for_mas["without_mas"]

    mas_not_in_the_table = fit_for_mas["mas_not_in_the_table"]
    _assert_exact_keys(
        mas_not_in_the_table,
        {
            "outside_the_three_types",
            "stress_not_penultimate",
            "next_word_not_disjunctive",
            "next_word_not_initially_stressed",
            "type_1_subtype_C",
            "type_2_subtype_C",
        },
        "MAS outside the fit table",
    )
    not_fit_records = _not_fit_for_mas_records(survey)
    assert sum(mas_not_in_the_table.values()) == len(not_fit_records)
    assert fit_for_mas["with_mas"] + len(not_fit_records) == len(post_stress)
    assert len(not_fit_records) == len(post_stress) - fit_for_mas["with_mas"]

    mas_with_mbs = census["mas_chanted_words_with_mbs"]
    mas_with_mbs_keys = {(record["bcv"], record["mam_form"]) for record in mas_with_mbs}
    assert len(mas_with_mbs_keys) == len(mas_with_mbs)
    post_stress_keys = {(record["bcv"], record["mam_form"]) for record in post_stress}
    assert len(post_stress_keys) == len(post_stress)
    assert mas_with_mbs_keys <= post_stress_keys

    type_2_groups = Counter(
        _type_2_filter_group(record) for record in _type_2_records(survey)
    )
    _assert_exact_keys(
        type_2_groups,
        {group for group, _code, _description in _TYPE_2_SUBTYPE_SPECS},
        "type-2 subtypes",
    )
    assert sum(type_2_groups.values()) == _by_type_count(survey, psm.TYPE_GUTTURAL)


def _pin_prose_claims(survey: dict) -> None:
    """Raise when corpus movement falsifies a statement rather than changing a figure."""
    post_stress = survey["post_stress"]
    census_chanted_word_summary = survey["census_chanted_word_summary"]
    assert (
        census_chanted_word_summary["mbs_only_chanted_words_with_more_than_two_mbs"]
        == 0
    )
    mbs_only = sum(
        counts["mbs_only"]
        for counts in census_chanted_word_summary["by_system"].values()
    )
    mas = sum(
        counts["mas"] for counts in census_chanted_word_summary["by_system"].values()
    )
    assert mbs_only > mas, "the prose says a meteg almost always precedes the stress"
    qamats_grouping_differences = survey["qamats_variant_census"][
        "distinct_phonetic_groupings"
    ]
    assert {record["bcv"] for record in qamats_grouping_differences} == {
        "ps35:10",
        "pr19:7",
    }
    assert len(qamats_grouping_differences) == 2
    assert all(
        len(record["qamats-dal"]) == 1 and len(record["qamats-sam"]) == 2
        for record in qamats_grouping_differences
    )
    assert _both(survey, "meteg in the stressed syllable, no sof pasuq") == 0
    stress_accent_classification = survey["stress_accent_classification"]
    assert stress_accent_classification["counts"] == {
        "conjunctive": len(post_stress),
        "disjunctive": 0,
    }
    assert (
        stress_accent_classification["conclusion"]
        == "Every MAS has a conjunctive accent on that stress letter."
    )
    assert all(record["syllables_after_the_stress"] == 1 for record in post_stress)
    next_accent_classification = Counter(
        record["next_chanted_word_accent_classification"] for record in post_stress
    )
    assert set(next_accent_classification) <= {"disjunctive", "conjunctive"}
    assert sum(next_accent_classification.values()) == len(post_stress)
    fit_for_mas = _fit_for_mas(survey)
    mbs_and_mas = census_chanted_word_summary["mas_chanted_words_with_mbs"]
    assert all(
        record["mam_form"] is not None and record["mam_form"].count(psm.METEG) == 2
        for record in mbs_and_mas
    )
    not_fit_for_mas_records = _not_fit_for_mas_records(survey)
    assert all(
        record["chanted_word"]
        and record["next_chanted_word"]
        and record["mam_form"]
        and record["next_mam_form"]
        and not (
            record["meets_first_fit_for_mas_criterion"]
            and record["meets_second_fit_for_mas_criterion"]
            and record["meets_third_fit_for_mas_criterion"]
        )
        for record in not_fit_for_mas_records
    )
    fitting_records = fit_for_mas["records"]
    assert all(
        record["stress_syllable_has_conjunctive_accent"]
        and record["next_chanted_word_is_initially_stressed"]
        and record["next_chanted_word_has_disjunctive_accent"]
        and (
            record["fit_type"] not in {psm.FIT_TYPE_2_AF, psm.FIT_TYPE_2_BF}
            or not record["next_chanted_word_starts_with_a_vocal_shewa"]
        )
        and len(record["types"]) == 1
        and record["chanted_word"]
        and record["next_chanted_word"]
        and record["mam_form"]
        and record["next_mam_form"]
        for record in fitting_records
    )
    lacks_mas_records = _lacks_mas_records(survey)
    assert all(record["chanted_word"] for record in lacks_mas_records)
    misc_records = _misc_records(survey)
    assert all(one["structural_type"] == psm.TYPE_UNCLASSIFIED for one in misc_records)
    for subtype in (
        psm.SUBTYPE_MISC_VAYOMER,
        psm.SUBTYPE_MISC_ALMOST_TYPE_3,
    ):
        subtype_records = _subtype_records(survey, subtype)
        assert all(
            one["structural_type"] == psm.TYPE_UNCLASSIFIED for one in subtype_records
        )
    misc_almost_type_3 = _misc_almost_type_3_only_member(survey)
    assert _by_subtype_count(survey, psm.SUBTYPE_MISC_ALMOST_TYPE_3) == 1
    assert (
        misc_almost_type_3["vowel"] == "ḥolam"
        and misc_almost_type_3["is_the_last_syllable"]
        and not misc_almost_type_3["syllable_is_open"]
        and not misc_almost_type_3["chanted_word_is_closed_by_a_guttural"]
    )
    misc_vayomer_records = _subtype_records(survey, psm.SUBTYPE_MISC_VAYOMER)
    assert [
        one for one in post_stress if one.get("intervening_punctuation")
    ] == misc_vayomer_records
    # Both punctuation fields are normalized before comparison because a freshly built survey
    # carries tuples where a JSON round trip carries lists, and this routine has to accept
    # either: gen_html_files reads the tracked JSON only when trust_survey is on.
    assert all(
        tuple(one.get("intervening_punctuation", ())) == (psm.PASOLEG,)
        and list(one.get("intervening_mam_punctuation") or ())
        == [{"kind": "paseq", "glyph": psm.PASOLEG}]
        and one["next_mam_form"] is not None
        for one in misc_vayomer_records
    )
    type_2_records = _type_2_records(survey)
    assert all(
        record["chanted_word_is_closed_by_a_guttural"]
        and record["next_chanted_word_is_initially_stressed"]
        and not record["next_chanted_word_starts_with_a_vocal_shewa"]
        for record in type_2_records
    ), "the type-2 guttural, next-word-stress, or no-IVS fact has moved"
    assert all(
        record["syllables_after_the_stress"] == 1 for record in type_2_records
    ), "the type-2 penultimate-stress fact has moved"
    nonfinal_mas_syllable_records = _nonfinal_mas_syllable_records(survey)
    assert {record["bcv"] for record in nonfinal_mas_syllable_records} == {
        "is63:12",
        "pr1:19",
        "pr11:26",
        "jb5:10",
    }
    assert len(nonfinal_mas_syllable_records) == 4
    assert all(
        record["syllables_after_the_stress"] == 1
        and record["structural_type"] == psm.TYPE_GUTTURAL
        and record["syllable_is_open"]
        and record["vowel"] == "tsere"
        and record["chanted_word_is_closed_by_a_guttural"]
        and final_stress.ends_in_furtive_patax(record["chanted_word"])
        for record in nonfinal_mas_syllable_records
    ), "the four nonfinal-MAS type-2 cases have moved"
    type_2_final_mas_records = [
        record for record in type_2_records if record["is_the_last_syllable"]
    ]
    assert all(
        not record["syllable_is_open"] and record["vowel"] == "pataḥ"
        for record in type_2_final_mas_records
    ), "the final-MAS type-2 cases have moved"
    type_3_records = [
        record
        for record in post_stress
        if record["structural_type"] == psm.TYPE_CLOSED_TSERE
    ]
    assert all(
        record["is_the_last_syllable"]
        and not record["syllable_is_open"]
        and record["vowel"] == "tsere"
        and record["next_chanted_word_is_initially_stressed"]
        for record in type_3_records
    ), "the type-3 finality or next-chanted-word-stress fact has moved"
    type_1_records = [
        record for record in post_stress if record["structural_type"] == psm.TYPE_OPEN
    ]
    assert all(record["is_the_last_syllable"] for record in type_1_records)
    noninitial_next_stress_records = _noninitial_next_stress_records(survey)
    assert len(noninitial_next_stress_records) == 1
    assert noninitial_next_stress_records[0]["bcv"] == "je46:14"
    assert noninitial_next_stress_records[0]["structural_type"] == psm.TYPE_OPEN
    type_2_type_3_overlap = _type_2_type_3_overlap(survey)
    assert type_2_type_3_overlap["chanted_words"] == sum(
        type_2_type_3_overlap["by_book"].values()
    )
    assert type_2_type_3_overlap["chanted_words"] == sum(
        type_2_type_3_overlap["by_final_letter"].values()
    )
    assert set(type_2_type_3_overlap["by_book"]) == {"da", "er"}
    assert set(type_2_type_3_overlap["by_final_letter"]) == {"\N{HEBREW LETTER HE}"}
    assert type_2_type_3_overlap["example"]["mam_form"] is not None
    assert _split(type_2_type_3_overlap["example"]["bcv"])[0] in {"da", "er"}
    assert survey["post_silluq"]["in_mam"] == sum(
        1 for one in post_stress if one["has_sof_pasuq"]
    ), "the post-silluq count and the records disagree"
    post_silluq_forms = dict(_post_silluq_comparison(survey))
    assert post_silluq_forms["MAM"].count(psm.METEG) == 1
    assert post_silluq_forms["BHS"].count(psm.METEG) == 2
    exodus = _dual_cantillation_facts(survey, "ex20:2")
    assert exodus["same_chanted_word_group_count"]
    assert all(len(branch) == 1 for branch in exodus["first_same_chanted_word_group"])
    genesis = _dual_cantillation_facts(survey, "gn35:22")
    assert genesis["same_chanted_word_group_count"] == 5
    dual_cantillation = _dual_cantillation(survey)
    whole_census_comparison = dual_cantillation["whole_census_comparison_counts"]
    template_comparison = dual_cantillation["template_counts"]
    cantillations = {psm.CANT_ALEF, psm.CANT_BET}
    comparison_categories = {
        "chanted words checked",
        "meteg before the stressed syllable",
        "meteg after the stressed syllable",
    }
    _assert_exact_keys(
        whole_census_comparison, cantillations, "whole-census cantillations"
    )
    _assert_exact_keys(template_comparison, cantillations, "template cantillations")
    for cantillation in cantillations:
        _assert_exact_keys(
            whole_census_comparison[cantillation],
            comparison_categories,
            f"{cantillation} whole-census comparison",
        )
        _assert_exact_keys(
            template_comparison[cantillation],
            comparison_categories,
            f"{cantillation} template comparison",
        )
    assert dual_cantillation["counted_cantillation"] == psm.CANT_ALEF
    for category in comparison_categories:
        assert whole_census_comparison[psm.CANT_ALEF][category] == _both(
            survey, category
        )
    assert (
        whole_census_comparison[psm.CANT_ALEF]["meteg after the stressed syllable"]
        == whole_census_comparison[psm.CANT_BET]["meteg after the stressed syllable"]
    )
    assert template_comparison[psm.CANT_ALEF]["meteg after the stressed syllable"] == 0
    assert template_comparison[psm.CANT_BET]["meteg after the stressed syllable"] == 0
    for category in (
        "chanted words checked",
        "meteg before the stressed syllable",
    ):
        assert (
            abs(
                template_comparison[psm.CANT_ALEF][category]
                - template_comparison[psm.CANT_BET][category]
            )
            == 1
        )
    assert survey["post_silluq"]["in_mam"] == 0
    difference = dual_cantillation["meteg_before_stress_difference"]
    assert difference["bcv"] == "dt5:6"
    assert len(difference[psm.CANT_ALEF]["chanted_words"]) == 2
    assert len(difference[psm.CANT_BET]["chanted_words"]) == 2
    chanted_word_difference = dual_cantillation["chanted_word_count_difference"]
    assert chanted_word_difference["bcv"] == "dt5:14"
    assert len(chanted_word_difference[psm.CANT_ALEF]["chanted_words"]) == 2
    assert len(chanted_word_difference[psm.CANT_BET]["chanted_words"]) == 1
    for kind in (*_TYPE_SOURCES, psm.TYPE_UNCLASSIFIED):
        if _by_type_count(survey, kind):
            _example_of(survey, kind)
    for bcv in (
        _POST_SILLUQ_VERSE,
        _MAM_POST_SILLUQ_VERSE,
        _CHRONICLES_8_11_VERSE,
    ):
        assert bcv in survey["currency"]["focus_verses"], (
            f"{bcv} is named in the page's prose but the survey records no chanted word"
            " for it; add it to post_stress_meteg._FOCUS_VERSES"
        )
    _excerpt_accounting()


def _excerpt_accounting() -> tuple[int, int]:
    """The page's quotation accounting: every excerpt's length, and the sum of them.

    The plan's decision 2 caps one excerpt at 150 words and all of them together at 300, and
    requires the generator to enforce both whenever it has excerpts.  This page has none, so
    what is enforced is that the list is empty and the accounting reads zero.
    """
    lengths = [len(text.split()) for _source, text in _EXCERPTS]
    for (source, _text), length in zip(_EXCERPTS, lengths):
        assert length <= _MAX_WORDS_PER_EXCERPT, f"{source}: {length} words"
    assert sum(lengths) <= _MAX_WORDS_IN_ALL_EXCERPTS, sum(lengths)
    assert not _EXCERPTS, "this page quotes neither book; see the module docstring"
    return len(_EXCERPTS), sum(lengths)
