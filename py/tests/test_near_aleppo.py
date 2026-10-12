"""Differential checks for the local near-Aleppo products."""

import copy

import pytest

import main_near_aleppo
from near_aleppo import doc_figures, qere_without_ketiv
from near_aleppo import ketiv_checks
from near_aleppo import phase2_templates as phase2
from py_misc import orphan_marks


def test_dataset_and_population_baselines_are_current():
    assert main_near_aleppo.almost_main(["--census", "--check"]) == 0
    assert main_near_aleppo.almost_main(["--build", "--check"]) == 0


def test_all_changed_note_presentations_match_the_source_inventory():
    assert main_near_aleppo.almost_main(["--check-note-review"]) == 0


def test_qere_only_calls_and_body_templates_match_independent_sources():
    """Compare complete qere calls with MAM and body templates with image records."""
    rows = qere_without_ketiv.records()
    by_ref = {qere_without_ketiv.build_reference(row["reference"]): row for row in rows}
    assert len(by_ref) == len(rows)
    seen = set()
    for verse in doc_figures._Corpus().verses:
        source = [
            template
            for _, template in doc_figures._templates(
                verse.mam[2], verse.ref, doc_figures._MAM
            )
            if template["tmpl_name"] == qere_without_ketiv.QERE_TEMPLATE
        ]
        data = [
            template
            for _, template in doc_figures._templates(
                verse.data[2], verse.ref, doc_figures._DATASET
            )
        ]
        qeres = [
            template
            for template in data
            if template["tmpl_name"] == qere_without_ketiv.QERE_TEMPLATE
        ]
        assert qeres == source, verse.ref
        if verse.ref not in by_ref:
            continue
        row = by_ref[verse.ref]
        assert len(source) == 1, verse.ref
        assert source[0]["tmpl_params"]["2"] == row["reading"]["qere"]
        expected = row["intended_encoding"]["template"]
        bodies = [
            template
            for template in data
            if template["tmpl_name"] in qere_without_ketiv.BODY_NAMES.values()
        ]
        assert bodies == ([expected] if expected is not None else []), verse.ref
        seen.add(verse.ref)
    assert seen == set(by_ref)


@pytest.mark.parametrize(
    "pointing, error",
    (
        ("אבג", "consonants"),
        ("\N{HEBREW POINT PATAH}אב", "raw mark"),
        ("א \N{HEBREW POINT PATAH}ב", "raw mark"),
        (
            [
                "א",
                {
                    "tmpl_name": orphan_marks.MARKS_WITHOUT_LETTER,
                    "tmpl_params": {"1": "ו"},
                },
                "ב",
            ],
            "carrier alef",
        ),
        (
            [
                "א",
                {
                    "tmpl_name": orphan_marks.MARKS_WITHOUT_LETTER_OR_SPACE,
                    "tmpl_params": {
                        "1": orphan_marks.GV_CARRIER,
                        "unexpected": "unapproved",
                    },
                },
                "ב",
            ],
            "template shape",
        ),
    ),
)
def test_producer_rejects_corrupted_pointings_without_changing_them(pointing, error):
    target = {
        "tmpl_name": "כו״ק",
        "tmpl_params": {
            "1": "אב",
            "2": "אָב",
            phase2.POINTED_KETIV_PARAMETER: pointing,
        },
    }
    cell = [{"tmpl_name": "נוסח", "tmpl_params": {"1": target, "2": []}}]
    before = copy.deepcopy(cell)
    with pytest.raises(AssertionError, match=error):
        ketiv_checks.check_e_cell(cell, ("test", "1", "1"))
    assert cell == before
