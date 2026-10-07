"""Independent-oracle differentials, regeneration and disclosure-shape checks.

The full tracked analysis is the golden for regeneration. Two of its fields are also
checked against oracles that share none of the classifier's code: the accent class
against accgram's prose and poetic scanners, which read each chanted word's displayed
Hebrew, and the target meteg against accgram's nucleus parser. The public display
corpus is the only input; the one-time migration oracles are not test inputs.
"""

from collections import Counter
from functools import lru_cache
import json
from types import MappingProxyType

import pytest

from accgram import chanted_word_accents_units as cwa
from accgram import meteg_before_stress
from accgram import poetic_accent_names as pan
from accgram import poetic_filter
from accgram import poetic_scanner
from accgram import post_stress_meteg_model
from accgram import prose_scanner
from accgram import uni_to_marks
from mb_cmn import bib_locales
from mb_cmn import hebrew_points as hpo
from mb_cmn import hebrew_punctuation as hpu
from phonetic_mam import analysis_reader
from wlc_cmn.wlc_book_codes import bk39id_to_wlc_bb
from yeivin_itm import claims

_POPULATIONS = ("ordinary", "samekh")

# The records whose accent class the scanners give differently from the survey, keyed by
# population, verse and the chanted word's scanner tokens. In each the survey's disjunctive
# is right: the chanted word has a dexi and its stress helper, and the poetic scanner reads
# the two dexi marks as the pair DEXI_DEXI, which is not a grammar token.
_DECLARED_ACCENT_CLASS_DISAGREEMENTS = (
    ("ordinary", "Ps24:7", ("DEXI_DEXI",)),
    ("ordinary", "Ps37:36", ("DEXI_DEXI",)),
    ("ordinary", "Ps77:20", ("DEXI_DEXI",)),
    ("ordinary", "Ps78:31", ("DEXI_DEXI",)),
    ("ordinary", "Ps78:35", ("DEXI_DEXI",)),
    ("ordinary", "Ps78:57", ("DEXI_DEXI",)),
    ("ordinary", "Ps94:20", ("DEXI_DEXI",)),
    ("ordinary", "Ps99:5", ("DEXI_DEXI",)),
    ("ordinary", "Ps99:9", ("DEXI_DEXI",)),
    ("ordinary", "Ps105:3", ("DEXI_DEXI",)),
    ("ordinary", "Ps106:24", ("DEXI_DEXI",)),
    ("ordinary", "Ps107:25", ("DEXI_DEXI",)),
    ("ordinary", "Ps136:18", ("DEXI_DEXI",)),
    ("ordinary", "Jb11:17", ("DEXI_DEXI",)),
    ("ordinary", "Jb16:8", ("DEXI_DEXI",)),
    ("ordinary", "Jb22:4", ("DEXI_DEXI", "MUNAX")),
    ("ordinary", "Jb32:13", ("DEXI_DEXI", "MUNAX")),
    ("samekh", "Jb11:17", ("DEXI_DEXI",)),
)


@pytest.fixture(scope="module", autouse=True)
def _shared_public_display_corpus():
    """Load each book once; keep all classifier and oracle comparisons separate."""
    read_book = analysis_reader.read_book

    @lru_cache(maxsize=len(bib_locales.ALL_BK39_IDS))
    def cached_book(book):
        return MappingProxyType(read_book(book))

    with pytest.MonkeyPatch.context() as patch:
        patch.setattr(analysis_reader, "read_book", cached_book)
        try:
            yield
        finally:
            cached_book.cache_clear()


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


def _scanner_tokens(book, chapter, verse_number, verse, has_legarmeh):
    """Each displayed reading of one selected verse, with its accgram scanner tokens.

    The scanners read each chanted word's plain displayed Hebrew, with the display's
    paseq marker appended to the chanted word before it, as
    post_stress_meteg_model._accent_grammar_tokens_by_entry appends it.
    """
    bb = bk39id_to_wlc_bb(book)
    entries, fragments = [], []
    for event in verse.events():
        if isinstance(event, analysis_reader.Reading):
            entries.append(event)
            fragments.append(
                cwa.Frag(event.hebrew, uni_to_marks.word_to_marks(event.hebrew), True)
            )
        elif event == post_stress_meteg_model._PHONETIC_MAM_PASOLEG:
            prior = fragments[-1]
            fragments[-1] = cwa.Frag(prior.text, prior.marks + hpu.PASOLEG, True)
    body, units = cwa._verse_units(fragments)
    assert len(units) == len(entries)
    poetic = poetic_filter.should_keep_line(bb, chapter, verse_number)
    tokens = (
        poetic_scanner.scan_accent_tokens(body)
        if poetic
        else prose_scanner.scan_accents(body, bb, chapter, verse_number, has_legarmeh)
    )
    disjunctives = (
        pan.POETIC_DISJUNCTIVES
        if poetic
        else post_stress_meteg_model._PROSE_DISJUNCTIVE_TOKENS
    )
    by_chanted_word = cwa._by_chanted_word(units, tokens)
    assert len(by_chanted_word) == len(entries)
    for entry, (_unit, word_tokens, _unfolded) in zip(
        entries, by_chanted_word, strict=True
    ):
        yield entry, tuple(token.type for token in word_tokens), disjunctives


def test_accent_class_agrees_with_accgram_scanners_but_for_declared_records():
    survey = _tracked()
    cases = {population: survey[population]["cases"] for population in _POPULATIONS}
    matched = Counter()
    disagreements = []
    for book in bib_locales.ALL_BK39_IDS:
        verses = analysis_reader.read_book(book)
        for qamats, population in (
            (analysis_reader.QAMATS_DAL, "ordinary"),
            (analysis_reader.QAMATS_SAM, "samekh"),
        ):
            # One per book and qamats sequence, as prose_scanner.scan_book holds one.
            has_legarmeh = prose_scanner.HasLegarmeh()
            for (chapter, verse_number), verse in verses.items():
                bcv = bib_locales.short_bcv_of_bcvt(
                    bib_locales.mk_bcvtmam(book, chapter, verse_number)
                )
                selected = verse.select(
                    qamats=qamats, cantillation=analysis_reader.CANT_ALEF
                )
                for entry, tokens, disjunctives in _scanner_tokens(
                    book, chapter, verse_number, selected, has_legarmeh
                ):
                    if (entry.qamats == analysis_reader.QAMATS_SAM) != (
                        population == "samekh"
                    ):
                        continue
                    index = matched[population]
                    if index == len(cases[population]):
                        continue
                    case = cases[population][index]
                    if (bcv, entry.hebrew, entry.transcription, entry.qamats) != (
                        case["bcv"],
                        case["hebrew"],
                        case["transcription"],
                        case["qamats_variant"],
                    ):
                        continue
                    matched[population] += 1
                    scanner_disjunctive = bool(set(tokens) & disjunctives)
                    if scanner_disjunctive != (case["accent_class"] == "disj"):
                        disagreements.append((population, bcv, tokens))
    for population, population_cases in cases.items():
        assert population_cases, f"no {population} records to compare"
        assert matched[population] == len(population_cases), population
    assert sorted(disagreements) == sorted(_DECLARED_ACCENT_CLASS_DISAGREEMENTS)


def test_target_meteg_agrees_with_accgram_nucleus_parser():
    survey = _tracked()
    compared = 0
    records = 0
    for population in _POPULATIONS:
        for case in survey[population]["cases"]:
            records += 1
            parsed = post_stress_meteg_model._parse(
                case["hebrew"], case["transcription"]
            )
            # A syllable holding a hataf vowel is reduced; the target is the main
            # syllable two main syllables before the stressed one.
            main = [
                (index, letter)
                for index, (letter, point) in enumerate(parsed["nuclei"])
                if point not in post_stress_meteg_model._XATAFS
            ]
            stressed = [
                position
                for position, (index, _letter) in enumerate(main)
                if index == parsed["stressed"]
            ]
            assert len(stressed) == 1 and stressed[0] >= 2, case
            target_letter = main[stressed[0] - 2][1]
            target_marks = parsed["letters"][target_letter][1]
            assert (hpo.MTGOSLQ in target_marks) == case["target_meteg"], case
            compared += 1
    assert compared == records and compared


def test_approved_claims_reproduce_exact_public_analysis_fractions():
    comparison = claims.from_analysis()
    assert comparison == claims.read()
    assert comparison["schema"] == "yeivin-meteg-claims-v2"
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
