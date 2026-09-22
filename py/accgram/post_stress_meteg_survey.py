"""Corpus scanning and survey assembly for post-stress meteg."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

from accgram import poetic_filter
from accgram import prose_scanner
from accgram.uni_to_marks import is_accent
from mb_cmn import hebrew_punctuation as hpu
from mb_cmn import paths

from accgram.post_stress_meteg_model import (
    CANT_ALEF,
    CANT_BET,
    MAQAF,
    METEG,
    PASOLEG,
    SILLUQ_RULE,
    SOF_PASUQ,
    SYSTEM_POETIC,
    SYSTEM_PROSE,
    SurveyProblem,
    TYPE_OPEN,
    _CANTILLATION_BRANCH_INDEX,
    _COUNT_CATEGORIES,
    _DUAL_CANTILLATION_COMPARISON_CATEGORIES,
    _LEGACY_BASELINE,
    _SUBTYPES,
    _TYPES,
    _VERSE_KEY,
    _accent_grammar_tokens_by_entry,
    _assert_type_2_next_filter_coverage,
    _atom_keys,
    _bb_of_stem,
    _chanted_word_events,
    _chanted_words,
    _consonant_key,
    _dual_cantillation_facts,
    _dual_template_entry_ids,
    _has_a_disjunctive_accent,
    _has_dual_cantillation,
    _has_final_tsere_syllable_closed_by_guttural,
    _intervening_punctuation,
    _parse,
    _qamats_variant_facts,
    _qamats_variant_grouping_differences,
    _select_cantillation_strand,
    _select_qamats_reading,
)

from accgram.post_stress_meteg_sources import (
    _attach_mam_forms,
    _focus_verses,
    _mam_context_by_bcv,
    _mam_words_by_bcv,
)

from accgram.post_stress_meteg_classification import (
    _actual_type_1_mas_summary,
    _census_chanted_word_summary,
    _classify_one_word,
    _fit_for_mas_candidate,
    _fit_for_mas_summary,
    _mark_candidates_with_mas,
    stress_accent_classification,
)


def _scan(
    phon_dir: Path, cantillation: str = CANT_ALEF, *, dual_templates_only: bool = False
) -> dict:
    """Every U+05BD of one cantillation strand, optionally only inside its templates."""
    assert cantillation in _CANTILLATION_BRANCH_INDEX, cantillation
    found = {
        "counts": Counter(),
        "checked_chanted_words_by_bcv": Counter(),
        "pre_stress": [],
        "post_stress": [],
        "in_stressed": [],
        "overlaps": [],
        "mismatches": [],
        "same_letter_failures": [],
        "entries_without_jta_or_fva": 0,
        "last_entry_lacks_sof_pasuq": [],
        "metegs_by_verse": {},
        "dual_cant_verses": set(),
        "dual_cantillation": {},
        "dual_cantillation_chanted_words": {},
        "dual_template_entries": {},
        "source_chanted_word_entries_by_system": Counter(),
        "mam_chanted_words_by_system": Counter(),
        "qamats_variant_rows_by_system": Counter(),
        "qamats_variant_duplicate_entries_by_system": Counter(),
        "qamats_variant_distinct_groupings": [],
        "type_2_type_3_overlap_by_book": Counter(),
        "type_2_type_3_overlap_by_final_letter": Counter(),
        "type_2_type_3_overlap_example": None,
        "fit_for_mas_candidates": [],
        "chanted_word_occurrences": [],
    }
    bb_of_stem = _bb_of_stem()
    for path in sorted(phon_dir.glob("*.json")):
        bb = bb_of_stem[path.stem]
        has_legarmeh = prose_scanner.HasLegarmeh()
        data = json.loads(path.read_text(encoding="utf-8"))
        for vkey, verse in data.items():
            chnu, vrnu = (int(one) for one in _VERSE_KEY.match(vkey).groups())
            dual = _has_dual_cantillation(verse)
            if dual_templates_only and not dual:
                continue
            cantillation_verse = _select_cantillation_strand(verse, cantillation)
            _one_verse(
                f"{bb}{chnu}:{vrnu}",
                bb,
                chnu,
                vrnu,
                _select_qamats_reading(cantillation_verse),
                found,
                has_legarmeh=has_legarmeh,
                dual_cantillation=dual,
                dual_facts=_dual_cantillation_facts(verse) if dual else None,
                template_entry_ids=(
                    _dual_template_entry_ids(verse, cantillation)
                    if dual_templates_only
                    else None
                ),
                source_verse=cantillation_verse,
            )
    # The per-chanted-word grouping holds every pre-stress and post-stress record once, so
    # a census counting occurrences and a census counting records read the same scan.
    occurrences = found["chanted_word_occurrences"]
    assert sum(len(one["pre_stress"]) for one in occurrences) == len(
        found["pre_stress"]
    )
    assert sum(len(one["post_stress"]) for one in occurrences) == len(
        found["post_stress"]
    )
    return found


def _one_verse(
    bcv: str,
    bb: str,
    chnu: int,
    vrnu: int,
    verse,
    found: dict,
    *,
    has_legarmeh: prose_scanner.HasLegarmeh,
    dual_cantillation: bool | None = None,
    dual_facts: dict | None = None,
    template_entry_ids: set[int] | None = None,
    source_verse: object | None = None,
) -> None:
    system = (
        SYSTEM_POETIC
        if poetic_filter.should_keep_line(bb, chnu, vrnu)
        else SYSTEM_PROSE
    )
    dual = (
        _has_dual_cantillation(verse)
        if dual_cantillation is None
        else dual_cantillation
    )
    if dual:
        found["dual_cant_verses"].add(bcv)
        found["dual_cantillation"][bcv] = (
            _dual_cantillation_facts(verse) if dual_facts is None else dual_facts
        )
    events: list[object] = []
    _chanted_word_events(verse, events)
    accent_grammar_tokens = _accent_grammar_tokens_by_entry(
        bb=bb,
        chnu=chnu,
        vrnu=vrnu,
        system=system,
        events=events,
        has_legarmeh=has_legarmeh,
    )
    entries = [one for one in events if isinstance(one, dict)]
    scoped_entries = (
        entries
        if template_entry_ids is None
        else [one for one in entries if id(one) in template_entry_ids]
    )
    usable = [one for one in scoped_entries if one.get("jta") and one.get("fva")]
    all_usable = [one for one in entries if one.get("jta") and one.get("fva")]
    if template_entry_ids is None:
        assert source_verse is not None
        source_entries: list[dict] = []
        _chanted_words(source_verse, source_entries)
        source_usable = [
            one for one in source_entries if one.get("jta") and one.get("fva")
        ]
        qamats_facts = _qamats_variant_facts(source_verse)
        assert qamats_facts["source_entries"] == (
            qamats_facts["mam_chanted_words"] + qamats_facts["duplicate_entries"]
        )
        assert qamats_facts["rows"] <= qamats_facts["mam_chanted_words"]
        assert qamats_facts["rows"] <= qamats_facts["duplicate_entries"]
        assert len(source_usable) == (
            len(all_usable) + qamats_facts["duplicate_entries"]
        )
        found["source_chanted_word_entries_by_system"][system] += len(source_usable)
        found["mam_chanted_words_by_system"][system] += len(all_usable)
        found["qamats_variant_rows_by_system"][system] += qamats_facts["rows"]
        found["qamats_variant_duplicate_entries_by_system"][system] += qamats_facts[
            "duplicate_entries"
        ]
        found["qamats_variant_distinct_groupings"].extend(
            {
                "bcv": bcv,
                "system": system,
                **difference,
            }
            for difference in _qamats_variant_grouping_differences(source_verse)
        )
    found["entries_without_jta_or_fva"] += len(scoped_entries) - len(usable)
    if not usable:
        return
    if dual:
        found["dual_cantillation_chanted_words"][bcv] = [
            one["fva"].split(" ")[0] for one in usable
        ]
    if template_entry_ids is not None:
        found["dual_template_entries"][bcv] = usable
    if template_entry_ids is None:
        last_word = usable[-1]["fva"].split(" ")[0]
        if SOF_PASUQ not in last_word:
            found["last_entry_lacks_sof_pasuq"].append(
                {
                    "bcv": bcv,
                    "chanted_word": last_word,
                    "dual_cantillation": dual,
                    "has_a_meteg": METEG in last_word,
                }
            )
    metegs = 0
    event_index_by_entry_id = {
        id(entry): index
        for index, entry in enumerate(events)
        if isinstance(entry, dict)
    }
    for index, entry in enumerate(all_usable):
        if template_entry_ids is not None and id(entry) not in template_entry_ids:
            continue
        word = entry["fva"].split(" ")[0]
        jta = entry["jta"]
        previous_entry = all_usable[index - 1] if index else None
        preceding_chanted_word = (
            previous_entry["fva"].split(" ")[0] if previous_entry is not None else ""
        )
        next_entry = all_usable[index + 1] if index + 1 < len(all_usable) else None
        next_chanted_word = (
            next_entry["fva"].split(" ")[0] if next_entry is not None else None
        )
        next_jta = next_entry["jta"] if next_entry is not None else None
        next_jta_for_analysis = next_jta
        if next_chanted_word is not None and next_jta is not None:
            try:
                _parse(next_chanted_word, next_jta)
            except SurveyProblem:
                # The next entry records the mismatch when the scan reaches it. The
                # current entry remains countable, but no next-word stress claim may use the
                # mismatched pair.
                next_jta_for_analysis = None
        next_accent_grammar_tokens = (
            accent_grammar_tokens[id(next_entry)] if next_entry is not None else ()
        )
        next_chanted_word_accent_classification = (
            (
                "disjunctive"
                if _has_a_disjunctive_accent(system, next_accent_grammar_tokens)
                else "conjunctive"
            )
            if next_entry is not None
            else None
        )
        intervening_material = (
            tuple(
                events[
                    event_index_by_entry_id[id(entry)]
                    + 1 : event_index_by_entry_id[id(next_entry)]
                ]
            )
            if next_entry is not None
            else ()
        )
        metegs += word.count(METEG)
        try:
            parsed = _parse(word, jta)
        except SurveyProblem as problem:
            found["mismatches"].append(
                {"bcv": bcv, "chanted_word": word, "jta": jta, "why": str(problem)}
            )
            continue
        found["counts"][(system, "chanted words checked")] += 1
        found["checked_chanted_words_by_bcv"][bcv] += 1
        if _has_final_tsere_syllable_closed_by_guttural(parsed):
            found["type_2_type_3_overlap_by_book"][bb] += 1
            found["type_2_type_3_overlap_by_final_letter"][
                parsed["letters"][-1][0]
            ] += 1
            if found["type_2_type_3_overlap_example"] is None:
                found["type_2_type_3_overlap_example"] = {
                    "bcv": bcv,
                    "chanted_word": word,
                    "next_chanted_word": None,
                    "snapshot_before_qere": entry.get("before_qfikq"),
                }
        fit_for_mas_candidate = _fit_for_mas_candidate(
            bcv=bcv,
            system=system,
            entry_index=index,
            word=word,
            jta=jta,
            parsed=parsed,
            before_qere=entry.get("before_qfikq"),
            next_chanted_word=next_chanted_word,
            next_jta=next_jta_for_analysis,
            next_accent_grammar_tokens=next_accent_grammar_tokens,
            accent_grammar_tokens=accent_grammar_tokens[id(entry)],
            intervening_punctuation=_intervening_punctuation(
                bcv=bcv,
                chanted_word=word,
                material=intervening_material,
            ),
        )
        if fit_for_mas_candidate is not None:
            found["fit_for_mas_candidates"].append(fit_for_mas_candidate)
        _classify_one_word(
            bcv=bcv,
            system=system,
            entry_index=index,
            word=word,
            jta=jta,
            parsed=parsed,
            found=found,
            before_qere=entry.get("before_qfikq"),
            preceding_chanted_word=preceding_chanted_word,
            next_chanted_word=next_chanted_word,
            next_jta=next_jta_for_analysis,
            next_chanted_word_accent_classification=(
                next_chanted_word_accent_classification
            ),
            intervening_material=intervening_material,
        )
    found["metegs_by_verse"][bcv] = metegs


def _currency(found: dict, words_by_bcv: dict[str, list[str]]) -> dict:
    """How far the surveyed snapshot of MAM stands from the MAM-simple beside it.

    A per-numbered-verse U+05BD count on each side, in MAM's versification so the verse keys line
    up, and every verse where the two disagree.  This needs no chanted-word alignment and so
    survives the places where the two texts group atoms differently.

    DUAL-CANTILLATION VERSES ARE LEFT OUT, and would otherwise dominate the list: Phonetic MAM
    has both strands where MAM-simple's loader yields the combined stream once, so the two
    counts differ there for a structural reason rather than because either text moved.
    """
    today = {
        bcv: sum(word.count(METEG) for word in words)
        for bcv, words in words_by_bcv.items()
    }
    surveyed = found["metegs_by_verse"]
    compared = sorted((set(surveyed) & set(today)) - found["dual_cant_verses"])
    differences = [
        {
            "bcv": bcv,
            "surveyed_snapshot": surveyed[bcv],
            "mam_simple_today": today[bcv],
        }
        for bcv in compared
        if surveyed[bcv] != today[bcv]
    ]
    return {
        "what": (
            "The Phonetic MAM standard set is regenerated when al-hatorah's pipeline runs,"
            " so it is a snapshot of MAM rather than MAM's current state. This"
            " counts U+05BD per numbered verse on both sides and names every numbered verse"
            " where they differ, so the page can say which MAM its figures describe."
        ),
        "how": (
            "Per NUMBERED verse, in MAM's versification, which is the numbering both"
            " sides use. Nothing here aligns chanted words, so it survives the places where the two"
            " texts group atoms differently. Dual-cantillation numbered verses are left out:"
            " Phonetic MAM has both strands where MAM-simple's loader yields the combined"
            " stream once. Every other numbered verse ends on a chanted word with sof pasuq,"
            " measured 2026-09-04, so no chanted verse in the comparison runs past a"
            " numbered verse's end."
        ),
        "surveyed_snapshot": paths.display_path(paths.al_hatorah_phonetic_dir()),
        "compared_against": paths.display_path(paths.mam_simple_vtrad_mam_dir()),
        "focus_verses": _focus_verses(words_by_bcv),
        "verses_compared": len(compared),
        "verses_on_one_side_only": sorted(set(surveyed) ^ set(today)),
        "dual_cantillation_verses_left_out": len(found["dual_cant_verses"]),
        "metegs_in_the_surveyed_snapshot": sum(surveyed[bcv] for bcv in compared),
        "metegs_in_mam_simple_today": sum(today[bcv] for bcv in compared),
        "verses_differing": len(differences),
        "differences": differences,
    }


def _legacy_baseline(counts: Counter) -> dict:
    """Every difference between this run and the 2026-09-03 census, category by category."""
    differences = [
        {
            "system": system,
            "category": category,
            "census_2026_09_03": baseline,
            "measured": counts[(system, category)],
            "difference": counts[(system, category)] - baseline,
        }
        for system, categories in _LEGACY_BASELINE.items()
        for category, baseline in categories.items()
        if counts[(system, category)] != baseline
    ]
    return {
        "what": (
            "The 2026-09-03 census, doc/post-stress-meteg-census-2026-09-03.md, whose script"
            " is untracked and treats a verse's last parsed entry as verse-final whether or"
            " not it has sof pasuq. A comparison baseline, not a second measurement."
        ),
        "baseline": _LEGACY_BASELINE,
        "differences": differences,
    }


def _problems(found: dict) -> list[str]:
    """What makes a run unable to finish honestly, all of it, rather than the first of it."""
    out = []
    if found["same_letter_failures"]:
        refs = [one["bcv"] for one in found["same_letter_failures"][:20]]
        out.append(
            f"{len(found['same_letter_failures'])} metegs share a letter with a"
            f" accent on the stress letter, whose order is undefined: {refs}"
        )
    if found["mismatches"]:
        refs = [one["bcv"] for one in found["mismatches"][:20]]
        out.append(
            f"{len(found['mismatches'])} chanted words where the jta and the Hebrew count"
            f" syllables differently: {refs}"
        )
    unexplained = [
        one
        for one in found["last_entry_lacks_sof_pasuq"]
        if not one["dual_cantillation"] or one["has_a_meteg"]
    ]
    if unexplained:
        refs = [one["bcv"] for one in unexplained[:20]]
        out.append(
            f"{len(unexplained)} verses whose last chanted word lacks sof pasuq outside a"
            f" dual-cantillation span, or lacks it while having a meteg: {refs}"
        )
    return out


def _total_counts(found: dict, categories: tuple[str, ...]) -> dict[str, int]:
    """The two verse systems' totals for the specified census categories."""
    return {
        category: sum(
            found["counts"][(system, category)]
            for system in (SYSTEM_PROSE, SYSTEM_POETIC)
        )
        for category in categories
    }


def _dual_template_counts(found: dict) -> dict[str, int]:
    """The three appendix counts restricted to dual-cantillation templates."""
    return {
        "chanted words checked": sum(found["checked_chanted_words_by_bcv"].values()),
        "meteg before the stressed syllable": len(found["pre_stress"]),
        "meteg after the stressed syllable": len(found["post_stress"]),
    }


def _mam_form_for_dual_cantillation_atom(raw_atom: str, mam_atoms: list[str]) -> str:
    """The MAM atom with only the cantillation marks of ``raw_atom``'s branch.

    Phonetic MAM uses U+05C8 where MAM has U+05B0 when it resolves a shewa as vocal.  The raw
    atom therefore decides only which accent and meteg marks its cantillation branch selects;
    its letters and points never reach the reader-facing form.
    """
    candidates = [
        atom for atom in mam_atoms if _consonant_key(atom) == _consonant_key(raw_atom)
    ]
    assert len(candidates) == 1, (raw_atom, candidates)
    selected_marks = {char for char in raw_atom if is_accent(char) or char == METEG}
    return "".join(
        char
        for char in candidates[0]
        if not (is_accent(char) or char == METEG) or char in selected_marks
    )


def _mam_forms_for_dual_cantillation_difference(
    raw_words: list[str], words_by_bcv: dict[str, list[str]], bcv: str
) -> list[str]:
    """The MAM forms selected by one branch's Phonetic-MAM grouping and accents."""
    mam_atoms = [
        atom
        for word in words_by_bcv[bcv]
        for atom in re.split(f"[{MAQAF}{hpu.NU_GMAQ}]", word)
    ]
    return [
        MAQAF.join(
            _mam_form_for_dual_cantillation_atom(atom, mam_atoms)
            for atom in re.split(f"[{MAQAF}{hpu.NU_GMAQ}]", raw_word)
        )
        for raw_word in raw_words
    ]


def _extra_metegs_before_stress(records: list[dict], other: list[dict]) -> list[dict]:
    """The before-stress records in ``records`` that have no matching chanted word in ``other``."""
    unmatched = Counter(_consonant_key(one["chanted_word"]) for one in other)
    out = []
    for record in records:
        key = _consonant_key(record["chanted_word"])
        if unmatched[key]:
            unmatched[key] -= 1
        else:
            out.append(record)
    return out


def _meteg_before_stress_difference(
    found_alef: dict,
    found_bet: dict,
    words_by_cantillation: dict[str, dict[str, list[str]]],
) -> dict:
    """The single dually-cantillated chanted-word difference in meteg-before-stress count."""
    dual_bcv = found_alef["dual_cant_verses"]
    assert dual_bcv == found_bet["dual_cant_verses"]
    alef_by_bcv = Counter(
        one["bcv"] for one in found_alef["pre_stress"] if one["bcv"] in dual_bcv
    )
    bet_by_bcv = Counter(
        one["bcv"] for one in found_bet["pre_stress"] if one["bcv"] in dual_bcv
    )
    different_bcv = [bcv for bcv in dual_bcv if alef_by_bcv[bcv] != bet_by_bcv[bcv]]
    assert len(different_bcv) == 1, different_bcv
    bcv = different_bcv[0]
    assert bet_by_bcv[bcv] == alef_by_bcv[bcv] + 1
    alef_records = [one for one in found_alef["pre_stress"] if one["bcv"] == bcv]
    bet_records = [one for one in found_bet["pre_stress"] if one["bcv"] == bcv]
    extra_bet = _extra_metegs_before_stress(bet_records, alef_records)
    assert not _extra_metegs_before_stress(alef_records, bet_records)
    assert len(extra_bet) == 1, extra_bet
    bet_record = extra_bet[0]
    assert bet_record["bcv"] == bcv
    target_atom_keys = {
        _consonant_key(atom)
        for atom in re.split(f"[{MAQAF}{hpu.NU_GMAQ}]", bet_record["chanted_word"])
    }
    alef_counterparts = [
        word
        for word in found_alef["dual_cantillation_chanted_words"][bcv]
        if target_atom_keys
        & {_consonant_key(atom) for atom in re.split(f"[{MAQAF}{hpu.NU_GMAQ}]", word)}
    ]
    assert len(alef_counterparts) == 2, alef_counterparts
    assert all(METEG not in word for word in alef_counterparts), alef_counterparts
    counterpart_atom_keys = {
        _consonant_key(atom)
        for word in alef_counterparts
        for atom in re.split(f"[{MAQAF}{hpu.NU_GMAQ}]", word)
    }
    bet_counterparts = [
        word
        for word in found_bet["dual_cantillation_chanted_words"][bcv]
        if counterpart_atom_keys
        & {_consonant_key(atom) for atom in re.split(f"[{MAQAF}{hpu.NU_GMAQ}]", word)}
    ]
    assert len(bet_counterparts) == 2, bet_counterparts
    assert bet_record["chanted_word"] in bet_counterparts, bet_counterparts
    return {
        "bcv": bcv,
        CANT_ALEF: {
            "chanted_words": _mam_forms_for_dual_cantillation_difference(
                alef_counterparts, words_by_cantillation[CANT_ALEF], bcv
            )
        },
        CANT_BET: {
            "chanted_words": _mam_forms_for_dual_cantillation_difference(
                bet_counterparts, words_by_cantillation[CANT_BET], bcv
            )
        },
    }


def _template_mam_forms(
    entries: list[dict], words_by_bcv: dict[str, list[str]], bcv: str
) -> list[str]:
    """The selected template span's chanted words, as MAM has them today.

    A template can include a qere, so the raw Phonetic-MAM form alone cannot identify MAM's
    form.  ``_attach_mam_forms`` already settles that relation, including its qere spelling,
    and refuses an ambiguous match.
    """
    records = [
        {
            "bcv": bcv,
            "chanted_word": entry["fva"].split(" ")[0],
            "next_chanted_word": None,
            "snapshot_before_qere": entry.get("before_qfikq"),
        }
        for entry in entries
    ]
    unjoined = _attach_mam_forms(records, words_by_bcv)
    assert not unjoined, unjoined
    forms = [record["mam_form"] for record in records]
    assert all(forms), forms
    return forms


def _different_chanted_word_spans(
    alef_words: list[str], bet_words: list[str]
) -> list[tuple[slice, slice]]:
    """The aligned spans whose atom grouping differs between two template branches."""
    alef_index = 0
    bet_index = 0
    out = []
    while alef_index < len(alef_words) and bet_index < len(bet_words):
        if _atom_keys(alef_words[alef_index]) == _atom_keys(bet_words[bet_index]):
            alef_index += 1
            bet_index += 1
            continue
        alef_start = alef_index
        bet_start = bet_index
        alef_atoms: list[str] = []
        bet_atoms: list[str] = []
        while not alef_atoms or not bet_atoms or alef_atoms != bet_atoms:
            if len(alef_atoms) <= len(bet_atoms):
                assert alef_index < len(alef_words), (alef_words, bet_words)
                alef_atoms.extend(_atom_keys(alef_words[alef_index]))
                alef_index += 1
            else:
                assert bet_index < len(bet_words), (alef_words, bet_words)
                bet_atoms.extend(_atom_keys(bet_words[bet_index]))
                bet_index += 1
        out.append((slice(alef_start, alef_index), slice(bet_start, bet_index)))
    assert alef_index == len(alef_words), (alef_words, bet_words)
    assert bet_index == len(bet_words), (alef_words, bet_words)
    return out


def _chanted_word_count_difference(
    found_alef: dict,
    found_bet: dict,
    words_by_cantillation: dict[str, dict[str, list[str]]],
) -> dict:
    """The template grouping that makes cant-alef's chanted-word count one larger."""
    dual_bcv = found_alef["dual_cant_verses"]
    assert dual_bcv == found_bet["dual_cant_verses"]
    different_bcv = [
        bcv
        for bcv in dual_bcv
        if (
            found_alef["checked_chanted_words_by_bcv"][bcv]
            != found_bet["checked_chanted_words_by_bcv"][bcv]
        )
    ]
    assert len(different_bcv) == 1, different_bcv
    bcv = different_bcv[0]
    alef_words = found_alef["dual_cantillation_chanted_words"][bcv]
    bet_words = found_bet["dual_cantillation_chanted_words"][bcv]
    spans = _different_chanted_word_spans(alef_words, bet_words)
    assert len(spans) == 1, spans
    alef_span, bet_span = spans[0]
    assert (alef_span.stop - alef_span.start) == (bet_span.stop - bet_span.start) + 1
    alef_forms = _template_mam_forms(
        found_alef["dual_template_entries"][bcv][alef_span],
        words_by_cantillation[CANT_ALEF],
        bcv,
    )
    bet_forms = _template_mam_forms(
        found_bet["dual_template_entries"][bcv][bet_span],
        words_by_cantillation[CANT_BET],
        bcv,
    )
    return {
        "bcv": bcv,
        CANT_ALEF: {"chanted_words": alef_forms},
        CANT_BET: {"chanted_words": bet_forms},
    }


def build_survey() -> dict:
    """The whole survey: every U+05BD of the Phonetic MAM standard set, classified.

    Raises ``SurveyProblem`` at the END of the scan rather than at the first offending mark,
    so a run that cannot finish still says everything it found.  Collecting before failing is
    what makes the list usable: a run that raises on first sight can never enumerate the rest.
    """
    phon_dir = paths.require_al_hatorah_phonetic_dir()
    found = _scan(phon_dir, CANT_ALEF)
    found_bet = _scan(phon_dir, CANT_BET)
    template_found = _scan(phon_dir, CANT_ALEF, dual_templates_only=True)
    template_found_bet = _scan(phon_dir, CANT_BET, dual_templates_only=True)
    assert found["dual_cant_verses"] == found_bet["dual_cant_verses"]
    assert template_found["dual_cant_verses"] == found["dual_cant_verses"]
    assert template_found_bet["dual_cant_verses"] == found["dual_cant_verses"]
    words_by_bcv = _mam_words_by_bcv()
    context_by_bcv = _mam_context_by_bcv()
    assert set(context_by_bcv) == set(words_by_bcv), set(context_by_bcv) ^ set(
        words_by_bcv
    )
    assert {
        bcv: [item for item in stream if isinstance(item, str)]
        for bcv, stream in context_by_bcv.items()
    } == {
        bcv: [word for word in words if word != PASOLEG]
        for bcv, words in words_by_bcv.items()
    }
    words_by_cantillation = {
        CANT_ALEF: _mam_words_by_bcv(CANT_ALEF),
        CANT_BET: _mam_words_by_bcv(CANT_BET),
    }
    unjoined = _attach_mam_forms(
        found["post_stress"] + found["in_stressed"] + found["overlaps"],
        words_by_bcv,
        context_by_bcv,
    )
    problems = _problems(found) + _problems(found_bet)
    if problems:
        raise SurveyProblem("; ".join(problems))
    counts = found["counts"]
    qamats_variant_census = {}
    for system in (SYSTEM_PROSE, SYSTEM_POETIC):
        source_entries = found["source_chanted_word_entries_by_system"][system]
        mam_chanted_words = found["mam_chanted_words_by_system"][system]
        duplicate_entries = found["qamats_variant_duplicate_entries_by_system"][system]
        variant_rows = found["qamats_variant_rows_by_system"][system]
        grouping_entry_difference = sum(
            len(one["qamats-sam"]) - len(one["qamats-dal"])
            for one in found["qamats_variant_distinct_groupings"]
            if one["system"] == system
        )
        assert source_entries == mam_chanted_words + duplicate_entries
        assert duplicate_entries == variant_rows + grouping_entry_difference
        assert mam_chanted_words == counts[(system, "chanted words checked")]
        qamats_variant_census[system] = {
            "source_entries": source_entries,
            "variant_rows": variant_rows,
            "duplicate_phonetic_reading_entries": duplicate_entries,
            "mam_chanted_words_counted": mam_chanted_words,
        }
    post_stress = found["post_stress"]
    _assert_type_2_next_filter_coverage(post_stress)
    occurrences = found["chanted_word_occurrences"]
    mas_count = _mark_candidates_with_mas(found["fit_for_mas_candidates"], occurrences)
    census_chanted_word_summary = _census_chanted_word_summary(occurrences)
    mas_candidates_with_another_meteg = [
        candidate
        for candidate in found["fit_for_mas_candidates"]
        if candidate["has_mas"] and candidate["word_has_another_meteg"]
    ]
    assert len(mas_candidates_with_another_meteg) == len(
        census_chanted_word_summary["mas_chanted_words_with_mbs"]
    )
    actual_type_1_mas = _actual_type_1_mas_summary(found["fit_for_mas_candidates"])
    fit_for_mas = _fit_for_mas_summary(
        found["fit_for_mas_candidates"],
        mas_count,
        words_by_bcv,
        context_by_bcv,
    )
    by_type = Counter((one["system"], one["structural_type"]) for one in post_stress)
    assert actual_type_1_mas["cases"] == sum(
        by_type[(system, TYPE_OPEN)] for system in (SYSTEM_PROSE, SYSTEM_POETIC)
    )
    by_subtype = Counter(
        (one["system"], one["subtype"])
        for one in post_stress
        if one["subtype"] is not None
    )
    type_2_type_3_overlap_by_book = found["type_2_type_3_overlap_by_book"]
    type_2_type_3_overlap_by_final_letter = found[
        "type_2_type_3_overlap_by_final_letter"
    ]
    type_2_type_3_overlap_count = sum(type_2_type_3_overlap_by_book.values())
    assert type_2_type_3_overlap_count == sum(
        type_2_type_3_overlap_by_final_letter.values()
    )
    type_2_type_3_overlap_example = found["type_2_type_3_overlap_example"]
    assert type_2_type_3_overlap_example is not None
    unjoined_overlap_example = _attach_mam_forms(
        [type_2_type_3_overlap_example], words_by_bcv, context_by_bcv
    )
    assert not unjoined_overlap_example, unjoined_overlap_example
    assert type_2_type_3_overlap_example["mam_form"] is not None
    return {
        "what": (
            "Every U+05BD in MAM, classified by whether its syllable falls before, in, or"
            " after the chanted word's one primary stress. A U+05BD in the stressed syllable"
            " of a chanted word with sof pasuq is the silluq, and is counted as that"
            " rather than as a meteg."
        ),
        "stress_oracle": (
            "Phonetic MAM's jta field, whose ! marks the one stressed syllable. A U+05BD's"
            " position is never used to infer the stress. The Hebrew's nuclei are counted"
            " independently and the two counts must agree per chanted word, a furtive patax"
            " counting as a syllable on both sides."
        ),
        "silluq_boundary": SILLUQ_RULE,
        "scope": (
            "Every chanted word of every numbered verse. Prose verses and poetic verses are routed by"
            " accgram.poetic_filter, so Job's prose frame goes with the 21 books. A dual"
            " cantillation passage is counted with the cant-alef cantillation strand, as"
            " though it were read once."
        ),
        "dual_cantillation": {
            "counted_cantillation": CANT_ALEF,
            "numbered_verses": sorted(found["dual_cant_verses"]),
            "facts_by_numbered_verse": found["dual_cantillation"],
            "whole_census_comparison_counts": {
                CANT_ALEF: _total_counts(
                    found, _DUAL_CANTILLATION_COMPARISON_CATEGORIES
                ),
                CANT_BET: _total_counts(
                    found_bet, _DUAL_CANTILLATION_COMPARISON_CATEGORIES
                ),
            },
            "template_counts": {
                CANT_ALEF: _dual_template_counts(template_found),
                CANT_BET: _dual_template_counts(template_found_bet),
            },
            "meteg_before_stress_difference": _meteg_before_stress_difference(
                template_found, template_found_bet, words_by_cantillation
            ),
            "chanted_word_count_difference": _chanted_word_count_difference(
                template_found, template_found_bet, words_by_cantillation
            ),
        },
        "counts": {
            system: {one: counts[(system, one)] for one in _COUNT_CATEGORIES}
            for system in (SYSTEM_PROSE, SYSTEM_POETIC)
        },
        "qamats_variant_census": {
            "what": (
                "A qamats-variant row contains qamats-dal and qamats-sam readings of one MAM"
                " template row. The source-entry count includes both readings; the MAM chanted-word"
                " count selects the qamats-dal sequence once. The fatal survey"
                " invariants require source entries to equal MAM chanted words counted plus"
                " duplicate phonetic-reading entries, and connect duplicate entries to row counts"
                " and measured grouping differences, in each system."
            ),
            "by_system": qamats_variant_census,
            "distinct_phonetic_groupings": found["qamats_variant_distinct_groupings"],
        },
        "census_chanted_word_summary": census_chanted_word_summary,
        "post_stress_by_structural_type": {
            system: {one: by_type[(system, one)] for one in _TYPES}
            for system in (SYSTEM_PROSE, SYSTEM_POETIC)
        },
        "post_stress_by_subtype": {
            system: {one: by_subtype[(system, one)] for one in _SUBTYPES}
            for system in (SYSTEM_PROSE, SYSTEM_POETIC)
        },
        "actual_type_1_mas": actual_type_1_mas,
        "fit_for_mas": fit_for_mas,
        "stress_accent_classification": stress_accent_classification(post_stress),
        "type_2_type_3_overlap": {
            "chanted_words": type_2_type_3_overlap_count,
            "by_book": dict(sorted(type_2_type_3_overlap_by_book.items())),
            "by_final_letter": dict(
                sorted(type_2_type_3_overlap_by_final_letter.items())
            ),
            "example": {
                "bcv": type_2_type_3_overlap_example["bcv"],
                "mam_form": type_2_type_3_overlap_example["mam_form"],
            },
        },
        "post_stress": post_stress,
        "post_silluq": {
            "what": (
                "A meteg on a syllable AFTER the silluq, which would put two U+05BD in one"
                " verse-final chanted word and make telling the meteg from the silluq a"
                " question about syllables rather than about position."
            ),
            "in_mam": sum(1 for one in post_stress if one["has_sof_pasuq"]),
            "how_it_is_counted": (
                "A post-stress record whose chanted word has sof pasuq is one: the"
                " silluq is in the stressed syllable and this mark is after it. The census"
                " of 2026-09-03 could not support this count, its verse-final test having"
                " been position-based, and the claim was withdrawn from"
                " doc/holman-meteg-m23-isaiah-23-12.md on that ground."
            ),
        },
        "diagnostics": {
            "meteg_in_the_stressed_syllable_without_sof_pasuq": found["in_stressed"],
            "sharing_a_letter_with_a_non_stress_marking_accent": found["overlaps"],
            "entries_without_jta_or_fva": found["entries_without_jta_or_fva"],
            "numbered_verses_whose_last_entry_lacks_sof_pasuq": found[
                "last_entry_lacks_sof_pasuq"
            ],
            "records_without_a_mam_form": [
                {
                    "bcv": one["bcv"],
                    "chanted_word": one["chanted_word"],
                    "candidate_forms_in_mam_simple": one["mam_form_candidates"],
                }
                for one in unjoined
            ],
        },
        "legacy_baseline": _legacy_baseline(counts),
        "currency": _currency(found, words_by_bcv),
    }
