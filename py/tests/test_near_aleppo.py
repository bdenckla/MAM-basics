"""Differential checks for the local near-Aleppo products."""

import copy

import pytest

import main_near_aleppo
from near_aleppo import ketiv_checks
from near_aleppo import phase2_templates as phase2
from py_misc import orphan_marks


def test_dataset_and_population_baselines_are_current():
    assert main_near_aleppo.almost_main(["--census", "--check"]) == 0
    assert main_near_aleppo.almost_main(["--build", "--check"]) == 0


def test_all_changed_note_presentations_match_the_source_inventory():
    assert main_near_aleppo.almost_main(["--check-note-review"]) == 0


def test_requested_punctuation_extract_matches_edition_renderer():
    assert main_near_aleppo.almost_main(["--punctuation-review", "--check"]) == 0


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
                    "tmpl_params": {"1": "ו", "carrier": orphan_marks.GV_VARIANT},
                },
                "ב",
            ],
            "GV requires exactly",
        ),
        (
            [
                "א",
                {
                    "tmpl_name": orphan_marks.MARKS_WITHOUT_LETTER_OR_SPACE,
                    "tmpl_params": {
                        "1": orphan_marks.GV_CARRIER,
                        "carrier": orphan_marks.GV_VARIANT,
                    },
                },
                "ב",
            ],
            "unsupported orphan-template shape",
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
