"""Differential and disclosure-shape checks for the independent public survey.

The full tracked analysis is the golden. The public display corpus is the only
input to its regeneration; the one-time migration oracles are not test inputs.
"""

import json

from accgram import meteg_before_stress
from mb_cmn import bib_locales
from phonetic_mam import analysis_reader
from yeivin_itm import claims


def _tracked():
    return json.loads(
        meteg_before_stress.default_json_out_path().read_text(encoding="utf-8")
    )


def test_public_survey_reproduces_tracked_analysis():
    assert meteg_before_stress.build_survey() == _tracked()


def test_cases_have_only_public_display_and_independent_classification_fields():
    survey = _tracked()
    assert set(survey) == {
        "schema",
        "input",
        "projection",
        "ordinary",
        "samekh",
        "selections",
    }
    allowed = {
        "bcv",
        "hebrew",
        "transcription",
        "qamats_variant",
        "pattern",
        "fine_pattern",
        "accent_class",
        "target_meteg",
        "accent_on_target",
        "other_meteg_count",
    }
    public_pairs = set()
    for book in bib_locales.ALL_BK39_IDS:
        for (chapter, verse_number), verse in analysis_reader.read_book(book).items():
            bcv = bib_locales.short_bcv_of_bcvt(
                bib_locales.mk_bcvtmam(book, chapter, verse_number)
            )
            public_pairs.update(
                (bcv, reading.hebrew, reading.transcription, reading.qamats)
                for reading in verse.readings()
            )
    for population in ("ordinary", "samekh"):
        assert set(survey[population]) == {"cases", "counts", "reshaped_counts"}
        for case in survey[population]["cases"]:
            assert set(case) == allowed
            assert (
                case["bcv"],
                case["hebrew"],
                case["transcription"],
                case["qamats_variant"],
            ) in public_pairs
    assert survey["selections"] == meteg_before_stress.select_cases(
        survey["ordinary"]["cases"]
    )
    serialized = json.dumps(survey, ensure_ascii=False)
    assert not set(map(chr, (0x05AF, 0x05C4, 0x05C8, 0x05C9))) & set(serialized)


def test_approved_claims_reproduce_exact_public_analysis_fractions():
    comparison = claims.from_analysis()
    assert comparison == claims.read()
    assert comparison["schema"] == "yeivin-meteg-claims-v1"
    assert set(comparison["measurements"]) == set(comparison["populations"])
    for name, fraction in comparison["measurements"].items():
        assert type(fraction["numerator"]) is int
        assert type(fraction["denominator"]) is int
        assert 0 <= fraction["numerator"] <= fraction["denominator"]
        assert (
            fraction["percentage"]
            == 100 * fraction["numerator"] / fraction["denominator"]
        )
        assert comparison["populations"][name]["definition"]
        assert comparison["populations"][name]["exclusions"]
