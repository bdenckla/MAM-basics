"""Differential checks for the local near-Aleppo products."""

import main_near_aleppo


def test_dataset_and_population_baselines_are_current():
    assert main_near_aleppo.almost_main(["--census", "--check"]) == 0
    assert main_near_aleppo.almost_main(["--build", "--check"]) == 0


def test_all_changed_note_presentations_match_the_source_inventory():
    assert main_near_aleppo.almost_main(["--check-note-review"]) == 0


def test_requested_punctuation_extract_matches_edition_renderer():
    assert main_near_aleppo.almost_main(["--punctuation-review", "--check"]) == 0
