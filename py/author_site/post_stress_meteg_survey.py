"""Survey projections used by the post-stress-meteg page generators."""

from __future__ import annotations


from accgram import post_stress_meteg_model as psm

from author_site.post_stress_meteg_shared import (
    _POETIC,
    _PROSE,
)

# --- the numbers, all of them read off the survey ------------------------------


def _count(survey: dict, system: str, category: str) -> int:
    return survey["counts"][system][category]


def _both(survey: dict, category: str) -> int:
    return _count(survey, _PROSE, category) + _count(survey, _POETIC, category)


def _type_2_type_3_overlap(survey: dict) -> dict:
    """The all-corpus set that could satisfy both type-2 and type-3 conditions."""
    return survey["type_2_type_3_overlap"]


def _dual_cantillation_facts(survey: dict, bcv: str) -> dict:
    """The source-derived facts for one numbered verse with both cantillation strands."""
    return survey["dual_cantillation"]["facts_by_numbered_verse"][bcv]


def _dual_cantillation(survey: dict) -> dict:
    """The one-reading method and cant-alef/cant-bet comparison."""
    return survey["dual_cantillation"]


def _by_type_count(survey: dict, kind: str) -> int:
    return sum(
        survey["post_stress_by_structural_type"][system][kind]
        for system in (_PROSE, _POETIC)
    )


def _fit_for_mas(survey: dict) -> dict:
    """The survey's candidate analysis of syllables fit for MAS."""
    return survey["fit_for_mas"]


def _actual_type_1_mas(survey: dict) -> dict:
    """The survey's complete structural type-1 MAS analysis."""
    return survey["actual_type_1_mas"]


def _lacks_mas_records(survey: dict) -> list[dict]:
    """Every chanted-word pair fit for MAS but lacking MAS, in corpus order."""
    return [
        record for record in _fit_for_mas(survey)["records"] if not record["has_mas"]
    ]


def _not_fit_for_mas_records(survey: dict) -> list[dict]:
    """Every MAS chanted word not fit for MAS, in corpus order."""
    return _fit_for_mas(survey)["not_fit_records"]


def _nonfinal_mas_syllable_records(survey: dict) -> list[dict]:
    """MAS records where a further final syllable follows the MAS syllable."""
    return [
        record for record in survey["post_stress"] if not record["is_the_last_syllable"]
    ]


def _noninitial_next_stress_records(survey: dict) -> list[dict]:
    """MAS records whose next chanted word does not have initial stress."""
    return [
        record
        for record in survey["post_stress"]
        if not record["next_chanted_word_is_initially_stressed"]
    ]


def _next_conjunctive_records(survey: dict) -> list[dict]:
    """MAS records whose next chanted word has a conjunctive accent."""
    records = [
        record
        for record in survey["post_stress"]
        if record["next_chanted_word_accent_classification"] == "conjunctive"
    ]
    assert all(record["next_chanted_word"] for record in records)
    return records


def _by_subtype_count(survey: dict, subtype: str) -> int:
    return sum(
        survey["post_stress_by_subtype"][system][subtype]
        for system in (_PROSE, _POETIC)
    )


def _subtype_records(survey: dict, subtype: str) -> list[dict]:
    """The post-stress records whose finer classification is ``subtype``."""
    return [one for one in survey["post_stress"] if one["subtype"] == subtype]


def _example_of(survey: dict, kind: str) -> dict:
    """The first record of a type, in the corpus's order, as that type's specimen.

    First rather than chosen: a hand-picked specimen is a claim with nothing behind it, and
    the whole set is on the page below anyway.
    """
    for record in survey["post_stress"]:
        if record["structural_type"] == kind:
            return record
    raise AssertionError(f"no post-stress record of type {kind!r} to show")


def _misc_almost_type_3_only_member(survey: dict) -> dict:
    """The only chanted word that fits CoS type (a), but not this survey's tsere-restricted type 3: Job 15:35."""
    records = [
        one
        for one in _subtype_records(survey, psm.SUBTYPE_MISC_ALMOST_TYPE_3)
        if one["bcv"] == "jb15:35"
    ]
    assert len(records) == 1, records
    return records[0]
