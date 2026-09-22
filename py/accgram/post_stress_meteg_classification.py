"""Classification and aggregation for the post-stress-meteg survey."""

from __future__ import annotations

from collections import Counter

from accgram.uni_to_marks import is_accent
from mb_cmn import hebrew_accents as ha
from mb_cmn import hebrew_letters as hl
from mb_cmn import hebrew_points as hpo

from accgram.post_stress_meteg_model import (
    FIT_TYPE_1_A,
    FIT_TYPE_1_B,
    FIT_TYPE_2_AF,
    FIT_TYPE_2_BF,
    FIT_TYPE_3,
    METEG,
    PASOLEG,
    SUBTYPE_MISC_VAYOMER,
    SYSTEM_POETIC,
    SYSTEM_PROSE,
    SurveyProblem,
    TYPE_1_SUBTYPE_A,
    TYPE_1_SUBTYPE_B,
    TYPE_1_SUBTYPE_C,
    TYPE_CLOSED_TSERE,
    TYPE_GUTTURAL,
    TYPE_OPEN,
    _FIT_TYPES,
    _NON_STRESS_ACCENTS,
    _STRESS_ACCENT_CONJUNCTIVES,
    _TYPE_1_SUBTYPES,
    _accent_name,
    _bare,
    _chanted_word_is_closed_by_a_guttural,
    _first_syllable_is_stressed,
    _has_a_disjunctive_accent,
    _intervening_punctuation,
    _letters,
    _misc_subtype,
    _starts_with_a_vocal_shewa,
    _stress_letter_accent,
    _stress_syllable_has_conjunctive_accent,
    _structural_type,
    _syllable_is_open,
    _type_1_subtype,
    _vowel_name,
)

from accgram.post_stress_meteg_sources import (
    _attach_mam_forms,
)


def stress_accent_classification(post_stress: list[dict]) -> dict:
    """The legacy table's weak, reproducible conclusion about MAS stress accents.

    The classification deliberately stops at conjunctive versus disjunctive.  A raw U+05C0
    cannot distinguish a narrow-sense paseq from legarmeh, so only the structurally identified
    ``misc-vayomer`` records are allowed to have it. A poetic U+05A5 whose chanted word or
    preceding chanted word has ole is likewise refused as an oleh-we-yored question instead of
    being guessed to be normal merkha.
    """
    for record in post_stress:
        preceding_chanted_word = record.pop("_preceding_chanted_word")
        punctuation = record.get("intervening_punctuation", ())
        if punctuation:
            if not (
                record["subtype"] == SUBTYPE_MISC_VAYOMER and punctuation == (PASOLEG,)
            ):
                raise SurveyProblem(
                    f"{record['bcv']}: the stress-accent check cannot classify its U+05C0"
                )
        elif record["subtype"] == SUBTYPE_MISC_VAYOMER:
            raise SurveyProblem(
                f"{record['bcv']}: misc-vayomer lacks its narrow-sense paseq"
            )

        accent = _stress_letter_accent(record)
        if (
            record["system"] == SYSTEM_POETIC
            and accent == ha.MER
            and (ha.OLE in record["chanted_word"] or ha.OLE in preceding_chanted_word)
        ):
            raise SurveyProblem(
                f"{record['bcv']}: poetic U+05A5 near ole needs an oleh-we-yored analysis"
            )
        if accent not in _STRESS_ACCENT_CONJUNCTIVES[record["system"]]:
            raise SurveyProblem(
                f"{record['bcv']}: stress-letter accent is not a regular conjunctive"
            )

    return {
        "exact_rule": (
            "Read the accents on the initial Hebrew letter of the one jta syllable marked !, "
            "the rule used by the 2026-09-03 census table."
        ),
        "conclusion": "Every MAS has a conjunctive accent on that stress letter.",
        "counts": {"conjunctive": len(post_stress), "disjunctive": 0},
    }


def _syllable_of(nuclei: list[tuple[int, str]], letter_index: int) -> int:
    """Which syllable a mark on ``letter_index`` is in: the last nucleus at or before it."""
    return max(
        (i for i, (onset, _point) in enumerate(nuclei) if onset <= letter_index),
        default=0,
    )


def _record(
    *,
    bcv: str,
    system: str,
    word: str,
    jta: str,
    parsed: dict,
    syllable_index: int,
    letter_index: int,
    accents_here: list[str],
    before_qere: str | None,
    preceding_chanted_word: str,
    next_chanted_word: str | None,
    next_jta: str | None,
    next_chanted_word_accent_classification: str | None,
    intervening_punctuation: tuple[str, ...],
) -> dict:
    """One classified U+05BD, with everything the page's tables and counts derive from."""
    nuclei = parsed["nuclei"]
    letters = parsed["letters"]
    syllables = parsed["syllables"]
    syllable = syllables[syllable_index]
    is_last_syllable = syllable_index == len(syllables) - 1
    is_open = _syllable_is_open(syllable)
    vowel = nuclei[syllable_index][1]
    chanted_word_is_closed_by_a_guttural = _chanted_word_is_closed_by_a_guttural(parsed)
    structural_type, subtype = _structural_type(
        chanted_word_is_closed_by_a_guttural=chanted_word_is_closed_by_a_guttural,
        is_last_syllable=is_last_syllable,
        is_open=is_open,
        vowel=vowel,
    )
    if subtype is None:
        subtype = _misc_subtype(
            structural_type=structural_type,
            chanted_word=word,
            intervening_punctuation=intervening_punctuation,
        )
    record = {
        "bcv": bcv,
        "system": system,
        "chanted_word": word,
        "_preceding_chanted_word": preceding_chanted_word,
        "next_chanted_word": next_chanted_word,
        "snapshot_before_qere": before_qere,
        "accents_and_letters": _bare(word),
        "jta": jta,
        "syllables_after_the_stress": syllable_index - parsed["stressed"],
        "syllable": syllable,
        "syllable_is_open": is_open,
        "vowel": _vowel_name(vowel),
        "is_the_last_syllable": is_last_syllable,
        "chanted_word_is_closed_by_a_guttural": (chanted_word_is_closed_by_a_guttural),
        "next_chanted_word_is_initially_stressed": (
            _first_syllable_is_stressed(next_jta) if next_jta is not None else None
        ),
        "next_chanted_word_starts_with_a_vocal_shewa": (
            _starts_with_a_vocal_shewa(next_jta) if next_jta is not None else None
        ),
        "next_chanted_word_accent_classification": (
            next_chanted_word_accent_classification
        ),
        "has_sof_pasuq": parsed["has_sof_pasuq"],
        "shares_its_letter_with": [_accent_name(one) for one in accents_here],
        "structural_type": structural_type,
        "subtype": subtype,
        "type_1_subtype": (
            _type_1_subtype(next_chanted_word, next_jta)
            if structural_type == TYPE_OPEN
            else None
        ),
        "atom": 1 + sum(1 for one in letters[:letter_index] if one[2]),
    }
    if intervening_punctuation:
        record["intervening_punctuation"] = intervening_punctuation
    return record


def _classify_one_word(
    *,
    bcv: str,
    system: str,
    entry_index: int,
    word: str,
    jta: str,
    parsed: dict,
    found: dict,
    before_qere: str | None,
    preceding_chanted_word: str,
    next_chanted_word: str | None,
    next_jta: str | None,
    next_chanted_word_accent_classification: str | None,
    intervening_material: tuple[object, ...],
) -> None:
    """Classify every U+05BD of one chanted word, filling the tallies and the lists.

    Also groups this chanted word's own pre-stress and post-stress records into one
    ``chanted_word_occurrences`` entry, which is what the census counts.  ``entry_index``
    is the chanted word's position among its numbered verse's usable entries, and
    ``(bcv, entry_index)`` is therefore an OCCURRENCE identity where the chanted word's
    form is not: one form can occur twice in one numbered verse, and 21 forms do, each
    time carrying one meteg on each occurrence.
    """
    counts = found["counts"]
    stressed = parsed["stressed"]
    pre_stress: list[dict] = []
    post_stress: list[dict] = []
    for letter_index, (_letter, marks, _atom_final) in enumerate(parsed["letters"]):
        if METEG not in marks:
            continue
        syllable_index = _syllable_of(parsed["nuclei"], letter_index)
        accents_here = [mark for mark in marks if is_accent(mark)]
        if syllable_index == stressed and parsed["has_sof_pasuq"]:
            counts[(system, "silluq")] += 1
            continue
        if accents_here and (
            syllable_index == stressed
            or not all(one in _NON_STRESS_ACCENTS for one in accents_here)
        ):
            found["same_letter_failures"].append(
                {
                    "bcv": bcv,
                    "chanted_word": word,
                    "jta": jta,
                    "accents_on_that_letter": [_accent_name(a) for a in accents_here],
                    "where": (
                        "in the stressed syllable"
                        if syllable_index == stressed
                        else "outside the stressed syllable"
                    ),
                }
            )
            continue
        record = _record(
            bcv=bcv,
            system=system,
            word=word,
            jta=jta,
            parsed=parsed,
            syllable_index=syllable_index,
            letter_index=letter_index,
            accents_here=accents_here,
            before_qere=before_qere,
            preceding_chanted_word=preceding_chanted_word,
            next_chanted_word=next_chanted_word,
            next_jta=next_jta,
            next_chanted_word_accent_classification=(
                next_chanted_word_accent_classification
            ),
            intervening_punctuation=(
                _intervening_punctuation(
                    bcv=bcv,
                    chanted_word=word,
                    material=intervening_material,
                )
                if syllable_index > stressed
                else ()
            ),
        )
        if accents_here:
            key = "meteg sharing a letter with a non-stress-marking accent"
            counts[(system, key)] += 1
            found["overlaps"].append(record)
        if syllable_index < stressed:
            counts[(system, "meteg before the stressed syllable")] += 1
            found["pre_stress"].append(record)
            pre_stress.append(record)
        elif syllable_index == stressed:
            counts[(system, "meteg in the stressed syllable, no sof pasuq")] += 1
            found["in_stressed"].append(record)
        else:
            counts[(system, "meteg after the stressed syllable")] += 1
            found["post_stress"].append(record)
            post_stress.append(record)
    if pre_stress or post_stress:
        found["chanted_word_occurrences"].append(
            {
                "bcv": bcv,
                "entry_index": entry_index,
                "system": system,
                "pre_stress": pre_stress,
                "post_stress": post_stress,
            }
        )


def _fit_for_mas_candidate(
    *,
    bcv: str,
    system: str,
    entry_index: int,
    word: str,
    jta: str,
    parsed: dict,
    before_qere: str | None,
    next_chanted_word: str | None,
    next_jta: str | None,
    next_accent_grammar_tokens: tuple[str, ...],
    accent_grammar_tokens: tuple[str, ...],
    intervening_punctuation: tuple[str, ...],
) -> dict | None:
    """One potential MAS syllable, or ``None`` when no syllable follows the stress.

    Phonetic MAM's ``jta`` supplies the chanted word's one primary-stress position; a raw
    Unicode accent count cannot supply that information.  The potential syllable is directly
    after a nonfinal stress.  The table calls it fit for MAS only when the stress is penultimate
    and its syllable has exactly one regular conjunctive accent, the next chanted word has
    initial stress and a disjunctive accent-grammar token, and the candidate meets one of the
    Fit-for-MAS types.
    """
    stressed = parsed["stressed"]
    if stressed == len(parsed["syllables"]) - 1:
        return None
    potential_syllable = stressed + 1
    stress_is_penultimate = potential_syllable == len(parsed["syllables"]) - 1
    is_open = _syllable_is_open(parsed["syllables"][potential_syllable])
    vowel = parsed["nuclei"][potential_syllable][1]
    types = []
    if is_open and stress_is_penultimate:
        types.append(TYPE_OPEN)
    if _chanted_word_is_closed_by_a_guttural(parsed):
        types.append(TYPE_GUTTURAL)
    if stress_is_penultimate and not is_open and vowel == hpo.TSERE:
        types.append(TYPE_CLOSED_TSERE)
    potential_syllable_meteg_count = sum(
        marks.count(METEG)
        for letter_index, (_letter, marks, _atom_final) in enumerate(parsed["letters"])
        if _syllable_of(parsed["nuclei"], letter_index) == potential_syllable
    )
    next_chanted_word_is_initially_stressed = (
        _first_syllable_is_stressed(next_jta) if next_jta is not None else False
    )
    candidate = {
        "bcv": bcv,
        "system": system,
        # Not emitted: every public candidate record is built field by field below.  It is
        # here so that a candidate can be matched to its own chanted word rather than to
        # every chanted word of that form in the numbered verse.
        "entry_index": entry_index,
        "chanted_word": word,
        "jta": jta,
        "snapshot_before_qere": before_qere,
        "next_chanted_word": next_chanted_word,
        "intervening_punctuation": intervening_punctuation,
        "structural_types": types,
        "stress_is_penultimate": stress_is_penultimate,
        "has_u05bd": bool(potential_syllable_meteg_count),
        "word_has_another_meteg": (word.count(METEG) > potential_syllable_meteg_count),
        "next_chanted_word_is_initially_stressed": (
            next_chanted_word_is_initially_stressed
        ),
        "next_chanted_word_starts_with_a_vocal_shewa": (
            _starts_with_a_vocal_shewa(next_jta) if next_jta is not None else None
        ),
        "next_chanted_word_has_disjunctive_accent": _has_a_disjunctive_accent(
            system, next_accent_grammar_tokens
        ),
        "stress_syllable_has_conjunctive_accent": (
            _stress_syllable_has_conjunctive_accent(system, parsed)
        ),
        "accent_grammar_token_count": len(accent_grammar_tokens),
        "type_1_subtype": (
            _type_1_subtype(next_chanted_word, next_jta)
            if TYPE_OPEN in types and next_chanted_word_is_initially_stressed
            else None
        ),
    }
    return candidate


def _has_first_fit_for_mas_criterion(candidate: dict) -> bool:
    """Whether the chanted word has penultimate stress from a conjunctive accent."""
    return (
        candidate["stress_is_penultimate"]
        and candidate["stress_syllable_has_conjunctive_accent"]
    )


def _has_second_fit_for_mas_criterion(candidate: dict) -> bool:
    """Whether the next chanted word has initial stress from a disjunctive accent."""
    return (
        candidate["next_chanted_word_is_initially_stressed"]
        and candidate["next_chanted_word_has_disjunctive_accent"]
    )


def _has_non_type_specific_conditions_for_mas(candidate: dict) -> bool:
    """Whether a candidate meets the first two Fit-for-MAS criteria."""
    return _has_first_fit_for_mas_criterion(
        candidate
    ) and _has_second_fit_for_mas_criterion(candidate)


def _type_2_fit_type_from_initial(next_chanted_word: str | None) -> str | None:
    """The type-2 Fit-for-MAS class selected by the next word's initial."""
    if next_chanted_word is None:
        return None
    letters = _letters(next_chanted_word)
    assert letters, f"no Hebrew letter in next chanted word: {next_chanted_word!r}"
    initial = letters[0][0]
    if initial == hl.LAMED:
        return FIT_TYPE_2_AF
    if initial in (hl.ALEF, hl.HE, hl.XET, hl.AYIN):
        return FIT_TYPE_2_BF
    return None


def _type_2_fit_type(candidate: dict) -> str | None:
    """The 2Af or 2Bf class, including the condition that the next word lacks IVS."""
    if candidate["next_chanted_word_starts_with_a_vocal_shewa"] is not False:
        return None
    return _type_2_fit_type_from_initial(candidate["next_chanted_word"])


def _fit_type(candidate: dict) -> str | None:
    """The one Fit-for-MAS class that a candidate meets, if it has one."""
    structural_types = candidate["structural_types"]
    fit_types = []
    if (
        TYPE_OPEN in structural_types
        and candidate["type_1_subtype"] == TYPE_1_SUBTYPE_A
    ):
        fit_types.append(FIT_TYPE_1_A)
    if (
        TYPE_OPEN in structural_types
        and candidate["type_1_subtype"] == TYPE_1_SUBTYPE_B
    ):
        fit_types.append(FIT_TYPE_1_B)
    if TYPE_GUTTURAL in structural_types:
        type_2_fit_type = _type_2_fit_type(candidate)
        if type_2_fit_type is not None:
            fit_types.append(type_2_fit_type)
    if TYPE_CLOSED_TSERE in structural_types:
        fit_types.append(FIT_TYPE_3)
    assert len(fit_types) <= 1, candidate
    return fit_types[0] if fit_types else None


def _is_fit_for_mas(candidate: dict) -> bool:
    """Whether a candidate meets the non-type-specific conditions and a Fit-for-MAS class."""
    return _has_non_type_specific_conditions_for_mas(candidate) and bool(
        _fit_type(candidate)
    )


def _fit_for_mas_record(candidate: dict) -> dict:
    """The complete public-data record for one chanted-word pair fit for MAS."""
    assert _is_fit_for_mas(candidate), candidate
    fit_type = _fit_type(candidate)
    assert fit_type is not None, candidate
    assert candidate["mam_form"] is not None, candidate
    assert candidate["next_mam_form"] is not None, candidate
    return {
        "bcv": candidate["bcv"],
        "system": candidate["system"],
        "chanted_word": candidate["chanted_word"],
        "jta": candidate["jta"],
        "next_chanted_word": candidate["next_chanted_word"],
        "intervening_punctuation": candidate["intervening_punctuation"],
        "mam_form": candidate["mam_form"],
        "next_mam_form": candidate["next_mam_form"],
        "intervening_mam_punctuation": candidate["intervening_mam_punctuation"],
        "types": candidate["structural_types"],
        "fit_type": fit_type,
        "type_1_subtype": candidate["type_1_subtype"],
        "has_mas": candidate["has_mas"],
        "word_has_another_meteg": candidate["word_has_another_meteg"],
        "stress_syllable_has_conjunctive_accent": candidate[
            "stress_syllable_has_conjunctive_accent"
        ],
        "next_chanted_word_is_initially_stressed": candidate[
            "next_chanted_word_is_initially_stressed"
        ],
        "next_chanted_word_starts_with_a_vocal_shewa": candidate[
            "next_chanted_word_starts_with_a_vocal_shewa"
        ],
        "next_chanted_word_has_disjunctive_accent": candidate[
            "next_chanted_word_has_disjunctive_accent"
        ],
    }


def _not_fit_for_mas_record(candidate: dict) -> dict:
    """The complete public-data record for one MAS chanted word not fit for MAS."""
    assert candidate["has_mas"] and not _is_fit_for_mas(candidate), candidate
    assert candidate["mam_form"] is not None, candidate
    assert candidate["next_mam_form"] is not None, candidate
    return {
        "bcv": candidate["bcv"],
        "system": candidate["system"],
        "chanted_word": candidate["chanted_word"],
        "jta": candidate["jta"],
        "next_chanted_word": candidate["next_chanted_word"],
        "intervening_punctuation": candidate["intervening_punctuation"],
        "mam_form": candidate["mam_form"],
        "next_mam_form": candidate["next_mam_form"],
        "intervening_mam_punctuation": candidate["intervening_mam_punctuation"],
        "types": candidate["structural_types"],
        "type_1_subtype": candidate["type_1_subtype"],
        "next_chanted_word_starts_with_a_vocal_shewa": candidate[
            "next_chanted_word_starts_with_a_vocal_shewa"
        ],
        "meets_first_fit_for_mas_criterion": _has_first_fit_for_mas_criterion(
            candidate
        ),
        "meets_second_fit_for_mas_criterion": _has_second_fit_for_mas_criterion(
            candidate
        ),
        "meets_third_fit_for_mas_criterion": _fit_type(candidate) is not None,
    }


def _occurrence_key(occurrence: dict) -> tuple[str, int]:
    """One chanted word of one numbered verse, identified by position and not by form.

    A form is not an identity.  Twenty-one forms occur twice in one numbered verse with
    one meteg on each occurrence -- Exodus 26:5's לֻֽלָאֹ֗ת and Judges 1:33's בֵֽית־שֶׁ֙מֶשׁ֙
    among them -- so a key of (bcv, chanted word, jta) read each such pair as one chanted
    word carrying two metegs.  That is what put
    ``mbs_only_chanted_words_with_multiple_mbs`` at 143 rather than 122, and the MBS_O
    counts 21 above the chanted words they were described as counting, until 2026-09-09.
    The independent oracle is the features-of-interest survey ``foi/foiz_wt_mtgmtg.py``,
    which counts U+05BD per chanted word straight from MAM-parsed-plus with no stress
    oracle at all.
    """
    return occurrence["bcv"], occurrence["entry_index"]


def _census_chanted_word_summary(occurrences: list[dict]) -> dict:
    """The MBS_O and MAS census categories, which count chanted words."""
    assert len({_occurrence_key(one) for one in occurrences}) == len(occurrences)
    mbs_only = [
        one for one in occurrences if one["pre_stress"] and not one["post_stress"]
    ]
    mas = [one for one in occurrences if one["post_stress"]]
    mas_with_mbs_occurrences = [one for one in mas if one["pre_stress"]]
    assert all(
        len(one["pre_stress"]) == 1 for one in mas_with_mbs_occurrences
    ), mas_with_mbs_occurrences
    assert all(len(one["post_stress"]) == 1 for one in mas), mas
    mas_with_mbs = [one["post_stress"][0] for one in mas_with_mbs_occurrences]
    assert all(record["mam_form"] is not None for record in mas_with_mbs)
    return {
        "what": (
            "MBS_O counts chanted words with one or more U+05BD meteg marks before"
            " the stress and none after it. MAS counts chanted words with one or"
            " more U+05BD meteg marks after the stress, irrespective of the number"
            " before it."
        ),
        "by_system": {
            system: {
                "mbs_only": sum(one["system"] == system for one in mbs_only),
                "mas": sum(one["system"] == system for one in mas),
            }
            for system in (SYSTEM_PROSE, SYSTEM_POETIC)
        },
        "mbs_only_chanted_words_with_multiple_mbs": sum(
            len(one["pre_stress"]) > 1 for one in mbs_only
        ),
        "mbs_only_chanted_words_with_more_than_two_mbs": sum(
            len(one["pre_stress"]) > 2 for one in mbs_only
        ),
        "mas_chanted_words_with_mbs": [
            {
                "bcv": record["bcv"],
                "system": record["system"],
                "mam_form": record["mam_form"],
            }
            for record in mas_with_mbs
        ],
    }


def _mark_candidates_with_mas(candidates: list[dict], occurrences: list[dict]) -> int:
    """Mark each candidate according to whether it has a MAS, and return the MAS count.

    Keyed by ``_occurrence_key`` for the reason that function gives: a candidate is one
    chanted word, and matching it on its form would give every chanted word of that form
    in the numbered verse the MAS that one of them has.  No MAS chanted word shares a
    numbered verse with another of the same form today, so this key changes no count; the
    form-based key was the same defect as the census's, unfired.
    """
    mas_keys = {
        _occurrence_key(one)
        for one in occurrences
        if any(
            record["syllables_after_the_stress"] == 1 for record in one["post_stress"]
        )
    }
    for candidate in candidates:
        key = (candidate["bcv"], candidate["entry_index"])
        candidate["has_mas"] = key in mas_keys
        assert candidate["has_u05bd"] == candidate["has_mas"], candidate
    assert {
        (candidate["bcv"], candidate["entry_index"])
        for candidate in candidates
        if candidate["has_mas"]
    } == mas_keys
    return len(mas_keys)


def _actual_type_1_mas_summary(candidates: list[dict]) -> dict:
    """All structurally type-1 MAS cases, regardless of Fit-for-MAS conditions."""
    actual_type_1_mas = [
        candidate
        for candidate in candidates
        if candidate["has_mas"] and TYPE_OPEN in candidate["structural_types"]
    ]
    by_initial_stress_pattern = {}
    example_keys_by_initial_stress_pattern = {}
    for subtype in _TYPE_1_SUBTYPES:
        members = [
            candidate
            for candidate in actual_type_1_mas
            if candidate["type_1_subtype"] == subtype
        ]
        assert members, subtype
        by_initial_stress_pattern[subtype] = {
            "cases": len(members),
            "by_system": {
                system: sum(candidate["system"] == system for candidate in members)
                for system in (SYSTEM_PROSE, SYSTEM_POETIC)
            },
        }
        example_keys_by_initial_stress_pattern[subtype] = {
            key: members[0][key] for key in ("bcv", "chanted_word", "jta")
        }
    not_initially_stressed = [
        candidate
        for candidate in actual_type_1_mas
        if candidate["type_1_subtype"] is None
    ]
    assert all(
        not candidate["next_chanted_word_is_initially_stressed"]
        for candidate in not_initially_stressed
    )
    assert not_initially_stressed
    by_initial_stress_pattern["not_initially_stressed"] = {
        "cases": len(not_initially_stressed),
        "by_system": {
            system: sum(
                candidate["system"] == system for candidate in not_initially_stressed
            )
            for system in (SYSTEM_PROSE, SYSTEM_POETIC)
        },
    }
    example_keys_by_initial_stress_pattern["not_initially_stressed"] = {
        key: not_initially_stressed[0][key] for key in ("bcv", "chanted_word", "jta")
    }
    assert sum(counts["cases"] for counts in by_initial_stress_pattern.values()) == len(
        actual_type_1_mas
    )
    return {
        "cases": len(actual_type_1_mas),
        "by_initial_stress_pattern": by_initial_stress_pattern,
        "example_keys_by_initial_stress_pattern": (
            example_keys_by_initial_stress_pattern
        ),
    }


def _fit_for_mas_summary(
    candidates: list[dict],
    mas_count: int,
    words_by_bcv: dict[str, list[str]],
    context_by_bcv: dict[str, list[object]],
) -> dict:
    """The fit-for-MAS candidates, their type membership, and whether each has MAS."""
    non_type_specific_conditions = [
        candidate
        for candidate in candidates
        if _has_non_type_specific_conditions_for_mas(candidate)
    ]
    type_1_candidates = [
        candidate
        for candidate in non_type_specific_conditions
        if TYPE_OPEN in candidate["structural_types"]
    ]
    assert all(
        candidate["type_1_subtype"] in _TYPE_1_SUBTYPES
        for candidate in type_1_candidates
    ), type_1_candidates
    fitting = [
        candidate
        for candidate in non_type_specific_conditions
        if _fit_type(candidate) is not None
    ]
    unjoined = _attach_mam_forms(fitting, words_by_bcv, context_by_bcv)
    assert not unjoined, unjoined
    by_type_1_subtype = {}
    for subtype in _TYPE_1_SUBTYPES:
        members = [
            candidate
            for candidate in type_1_candidates
            if candidate["type_1_subtype"] == subtype
        ]
        with_mas = sum(candidate["has_mas"] for candidate in members)
        by_type_1_subtype[subtype] = {
            "candidates": len(members),
            "with_mas": with_mas,
            "without_mas": len(members) - with_mas,
            "with_mas_by_system": {
                system: sum(
                    candidate["has_mas"] and candidate["system"] == system
                    for candidate in members
                )
                for system in (SYSTEM_PROSE, SYSTEM_POETIC)
            },
        }
    by_fit_type = {}
    for fit_type in _FIT_TYPES:
        members = [
            candidate for candidate in fitting if _fit_type(candidate) == fit_type
        ]
        with_mas = sum(candidate["has_mas"] for candidate in members)
        by_fit_type[fit_type] = {
            "candidates": len(members),
            "with_mas": with_mas,
            "without_mas": len(members) - with_mas,
        }
    with_mas = sum(candidate["has_mas"] for candidate in fitting)
    mas_candidates = [candidate for candidate in candidates if candidate["has_mas"]]
    type_2_mas_with_initial_vocal_shewa = [
        candidate
        for candidate in mas_candidates
        if TYPE_GUTTURAL in candidate["structural_types"]
        and candidate["next_chanted_word_starts_with_a_vocal_shewa"]
    ]
    assert not type_2_mas_with_initial_vocal_shewa, type_2_mas_with_initial_vocal_shewa
    mas_after_first_criterion = [
        candidate
        for candidate in mas_candidates
        if _has_first_fit_for_mas_criterion(candidate)
    ]
    mas_with_nonpenultimate_stress = [
        candidate
        for candidate in mas_candidates
        if candidate["has_mas"] and not candidate["stress_is_penultimate"]
    ]
    mas_with_nonconjunctive_stress_syllable = [
        candidate
        for candidate in mas_candidates
        if not candidate["stress_syllable_has_conjunctive_accent"]
    ]
    assert (
        not mas_with_nonconjunctive_stress_syllable
    ), mas_with_nonconjunctive_stress_syllable
    mas_failing_first_criterion = [
        candidate
        for candidate in mas_candidates
        if not _has_first_fit_for_mas_criterion(candidate)
    ]
    assert len(mas_failing_first_criterion) == len(mas_with_nonpenultimate_stress)

    mas_after_second_criterion = [
        candidate
        for candidate in mas_after_first_criterion
        if _has_second_fit_for_mas_criterion(candidate)
    ]
    mas_with_non_disjunctive_next_word = [
        candidate
        for candidate in mas_after_first_criterion
        if not candidate["next_chanted_word_has_disjunctive_accent"]
    ]
    mas_with_noninitial_next_word = [
        candidate
        for candidate in mas_after_first_criterion
        if (
            candidate["next_chanted_word_has_disjunctive_accent"]
            and not candidate["next_chanted_word_is_initially_stressed"]
        )
    ]
    mas_failing_second_criterion = [
        candidate
        for candidate in mas_after_first_criterion
        if not _has_second_fit_for_mas_criterion(candidate)
    ]
    assert len(mas_failing_second_criterion) == (
        len(mas_with_non_disjunctive_next_word) + len(mas_with_noninitial_next_word)
    )

    mas_with_type_1_subtype_c = [
        candidate
        for candidate in mas_after_second_criterion
        if (
            TYPE_OPEN in candidate["structural_types"]
            and candidate["type_1_subtype"] == TYPE_1_SUBTYPE_C
        )
    ]
    mas_with_type_2_subtype_c = [
        candidate
        for candidate in mas_after_second_criterion
        if (
            TYPE_GUTTURAL in candidate["structural_types"]
            and _type_2_fit_type_from_initial(candidate["next_chanted_word"]) is None
        )
    ]
    mas_outside_the_three_types = [
        candidate
        for candidate in mas_after_second_criterion
        if not candidate["structural_types"]
    ]
    mas_failing_third_criterion = [
        candidate
        for candidate in mas_after_second_criterion
        if _fit_type(candidate) is None
    ]
    assert len(mas_failing_third_criterion) == (
        len(mas_with_type_1_subtype_c)
        + len(mas_with_type_2_subtype_c)
        + len(mas_outside_the_three_types)
    )
    excluded_mas = (
        mas_failing_first_criterion
        + mas_failing_second_criterion
        + mas_failing_third_criterion
    )
    assert len(
        {(candidate["bcv"], candidate["entry_index"]) for candidate in excluded_mas}
    ) == len(excluded_mas), excluded_mas
    assert with_mas + len(excluded_mas) == mas_count, (with_mas, excluded_mas)
    mas_not_fit_for_mas = [
        candidate for candidate in mas_candidates if not _is_fit_for_mas(candidate)
    ]
    assert len(mas_not_fit_for_mas) == len(excluded_mas)
    unjoined = _attach_mam_forms(mas_not_fit_for_mas, words_by_bcv, context_by_bcv)
    assert not unjoined, unjoined
    return {
        "what": (
            "Every syllable immediately after a penultimate primary stress with exactly one"
            " regular conjunctive accent, with a next chanted word that has initial stress"
            " and a disjunctive accent-grammar token, classified by the three MAS structural"
            " predicates and Type 1's A/B/C initial-stress subtypes. The potential syllable"
            " is checked for U+05BD."
            " Fit for MAS includes types 1A, 1B, 2Af, 2Bf, and 3; 2Af and 2Bf require"
            " that the next word not begin with vocal shewa."
            " Primary-stress position comes independently from Phonetic MAM's jta field."
        ),
        "records_what": (
            "Every chanted-word pair fit for MAS. Each record has the chanted word whose"
            " post-stress syllable is classified, the next chanted word, the applicable"
            " structural types and Fit-for-MAS class, and whether the first chanted word has"
            " MAS."
        ),
        "not_fit_records_what": (
            "Every MAS chanted word that is not fit for MAS. Each record has the MAS chanted"
            " word, its next chanted word, and whether it meets each of the three Fit-for-MAS"
            " criteria."
        ),
        "candidate_chanted_words": len(candidates),
        "non_type_specific_conditions": len(non_type_specific_conditions),
        "fitting_any_type": len(fitting),
        "with_mas": with_mas,
        "without_mas": len(fitting) - with_mas,
        "by_type_1_subtype": by_type_1_subtype,
        "by_fit_type": by_fit_type,
        "mas_not_in_the_table": {
            "stress_not_penultimate": len(mas_with_nonpenultimate_stress),
            "next_word_not_disjunctive": len(mas_with_non_disjunctive_next_word),
            "next_word_not_initially_stressed": len(mas_with_noninitial_next_word),
            "type_1_subtype_C": len(mas_with_type_1_subtype_c),
            "type_2_subtype_C": len(mas_with_type_2_subtype_c),
            "outside_the_three_types": len(mas_outside_the_three_types),
        },
        "accent_grammar_token_counts": dict(
            sorted(
                Counter(
                    candidate["accent_grammar_token_count"] for candidate in candidates
                ).items()
            )
        ),
        "records": [_fit_for_mas_record(candidate) for candidate in fitting],
        "not_fit_records": [
            _not_fit_for_mas_record(candidate) for candidate in mas_not_fit_for_mas
        ],
    }
